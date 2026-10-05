#!/usr/bin/env python3
"""
design_dice.py — labelled, seeded, logged dice for the designer.

Plan item 19.9, 17 #26, 22.1; docs/schemas/design-manifest.md (dice_log).

Every designer roll derives its own random.Random from
    f"{master seed}:{phase}:{table}:{label}"   (+ ":a{attempt}" on a rerun)
so the same roll gives the same result whatever order the rolls are made in,
a `fix` keeps the seed and a `rerun` (attempt+1) redraws. Public rolls are
appended to design.json's dice_log; secret ones (the big-secret archetype, the
BBEG's visibility) go to design/dm-only/dice-log.json, and design.json keeps
only their labels and count. Agents never roll: the conductor pre-rolls a
phase, and the results travel in the agents' inputs.

Table rolls read data/design/<table>.yaml (or <table>.yaml#subtable) through design_tables.py and roll
one row by weight, after design_arbiter.py has filtered the pool against the campaign's earlier rolls
(conflicts both ways, requirements, forbidden rows); for a plain notation, --notation rolls dice.
`--avoid-used` excludes rows that earlier campaigns in this root drew, as recorded in <root>/used.json;
a table's `family_wait: N` / `row_wait: N` make a family / a row wait N births. Every exclusion is logged
on the record with its reason.

used.json keeps, beside each campaign's rows, the birth order (`births`: the time a campaign's first
phase was approved), which the waits count in; a real campaign never counts the `_test-*` births.

CLI:
  design_dice.py -c CAMP roll --phase P1 --label tension.1 [--table tensions.yaml] [--notation d30]
                 [--secret] [--avoid-used] [--attempt N] [--json]
  design_dice.py -c CAMP log [--secret]
  design_dice.py -c CAMP used list | used add --table T --row ROW_ID
Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dice as dice_mod  # noqa: E402
import design_arbiter as arb  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import dm_only_dir, now_iso, read_json, stamp_meta, write_json_atomic  # noqa: E402
from design_manifest import append_roll, load as load_manifest  # noqa: E402
from design_tables import rows as table_rows  # noqa: E402
from paths import _root as data_root  # noqa: E402



TEST_USED_ENV = "DESIGN_USED_PATH"   # tests only: tests/_campaign.py points it at a temporary file


def used_path() -> Path:
    """<data root>/used.json; the test suite reads and writes its own temporary file instead, so no test ever
    touches the owner's store."""
    override = os.environ.get(TEST_USED_ENV)
    if override:
        import tempfile
        temp = Path(tempfile.gettempdir()).resolve()
        path = Path(override).resolve()
        if path == temp or temp in path.parents:
            return path
        # the DND_CAMPAIGN_ROOT leak's class: an environment value must never redirect a real store
        print(f"design_dice: {TEST_USED_ENV}={override} is outside the system temp directory; ignored", file=sys.stderr)
    return data_root() / "used.json"


def load_used() -> dict:
    data = read_json(used_path())
    if data is None:
        data = {"_meta": {"schema_version": 1, "written_by": "", "written_at": ""}, "campaigns": {}}
    data.setdefault("campaigns", {})
    return data


def save_used(data: dict) -> None:
    meta = data.setdefault("_meta", {})
    meta["schema_version"] = 1
    meta["written_by"] = "design_dice.py used"
    meta["written_at"] = now_iso()
    write_json_atomic(used_path(), data)


def hashed(row_id: str) -> str:
    """A secret roll's row as used.json keeps it: used.json sits where the owner reads, and a campaign's secret
    archetype is a spoiler; the next campaign still avoids the row by matching the hash."""
    import hashlib
    return "h:" + hashlib.sha256(str(row_id).encode("utf-8")).hexdigest()[:16]


def rows_used_elsewhere(campaign: str, table: str) -> set:
    """Rows other campaigns used from `table`; a real campaign ignores the `_test-*` births, a test birth sees all."""
    used = load_used()
    return rows_used_by([c for c in used["campaigns"] if _visible(campaign, c)], table, used)


def _visible(campaign: str, other: str) -> bool:
    """Another campaign's rows count for `campaign`: never itself, and a real campaign ignores the test births."""
    return other != campaign and not (not campaign.startswith("_test-") and other.startswith("_test-"))


def _resolve(entries, table: str) -> set:
    """Row ids from used.json entries, a secret row's hash matched against the table's rows."""
    plain = {dt.ROW_ALIASES.get(x, x) for x in entries if not str(x).startswith("h:")}     # a renamed row is still spent
    hashes = {x for x in entries if str(x).startswith("h:")}
    if hashes:
        plain |= {r["id"] for r in load_table(table) if hashed(r["id"]) in hashes}
    return plain


def birth_order(used: dict | None = None) -> list[str]:
    """Campaigns in birth order: the archived births used.json kept before the order existed come first, in the
    order they were written; every later birth by the time its first phase was approved."""
    used = used or load_used()
    births = used.get("births") or {}
    names = list(dict.fromkeys(list(used["campaigns"]) + list(births)))
    unstamped = [n for n in names if not (births.get(n) or {}).get("first_approved")]
    stamped = sorted((n for n in names if n not in unstamped), key=lambda n: births[n]["first_approved"])
    return unstamped + stamped


def recent_births(campaign: str, n: int, used: dict | None = None) -> list[str]:
    """The last `n` births before `campaign` that count for it (a real campaign skips the test births)."""
    used = used or load_used()
    order = birth_order(used)
    if campaign in order:
        order = order[:order.index(campaign)]
    return [c for c in order if _visible(campaign, c)][-n:] if n > 0 else []


def rows_used_by(campaigns: list[str], table: str, used: dict | None = None) -> set:
    used = used or load_used()
    out: set = set()
    for camp in campaigns:
        out |= _resolve((used["campaigns"].get(camp) or {}).get(table, []), table)
    return out


def usage(campaign: str, table: str, avoid: bool = True) -> dict:
    """The usage exclusions of one draw: rows used elsewhere, and the table's own waits. A table whose own header
    states `avoid_used` is held to it; the caller's `avoid` is read only when the header is silent (the actions and
    scars say `avoid_used: false, row_wait: 3`: they wait three births and are never exhausted)."""
    used = load_used()
    head = dt.roll_header(table)
    own = dt.own_roll_header(table)
    if "avoid_used" in own:
        avoid = bool(own["avoid_used"])
    out: dict = {}
    if avoid:
        out["used_elsewhere"] = rows_used_elsewhere(campaign, table)
    if head.get("row_wait"):
        out["row_wait"] = rows_used_by(recent_births(campaign, int(head["row_wait"]), used), table, used)
    if head.get("family_wait"):
        fams = {r["id"]: r.get("family") for r in load_table(table)}
        rows = rows_used_by(recent_births(campaign, int(head["family_wait"]), used), table, used)
        out["family_wait"] = {fams[r] for r in rows if fams.get(r) is not None}
    return out


def used_values(campaign: str, key: str, window: int | None = None) -> set:
    """Values other campaigns recorded under a used.json key that is no table (a target + action pair);
    `window` limits them to the last N births."""
    used = load_used()
    camps = recent_births(campaign, window, used) if window else [c for c in used["campaigns"] if _visible(campaign, c)]
    out: set = set()
    for camp in camps:
        out |= set((used["campaigns"].get(camp) or {}).get(key, []))
    return out


def prior_rolls(campaign: str, phase: str | None = None, with_tokens: bool = False):
    """Row id -> rolled secretly, for every roll a draw of `phase` stands on: the phases BEFORE it (P0 < P1 < ... <
    P9), each at its latest attempt only (a rerun's earlier draws are superseded). The phase itself and every later
    one are left out: a rerolled P1 is never filtered by the stale P2-P4 rolls built on its old self. A caller
    outside the birth order (in-play `detail`, no phase) sees every birth phase."""
    order = {p: i for i, p in enumerate(dt.PHASES)}
    limit = order.get(phase)
    m = load_manifest(campaign)
    recs = [(r, False) for r in m.get("dice_log") or []]
    recs += [(r, True) for r in (read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("rolls", [])]
    latest: dict = {}
    for r, _ in recs:
        latest[r.get("phase")] = max(latest.get(r.get("phase"), 0), int(r.get("attempt") or 1))
    out: dict = {}
    toks: dict = {}
    for r, secret in recs:
        ph = r.get("phase")
        if int(r.get("attempt") or 1) != latest.get(ph):
            continue
        if limit is not None and order.get(ph, -1) >= limit:
            continue
        for t in r.get("tokens") or []:          # a seated role's claims, the layout's tokens
            toks[t] = toks[t] and secret if t in toks else secret
        if r.get("row_id"):
            out[r["row_id"]] = out.get(r["row_id"], False) or secret
    return (out, toks) if with_tokens else out


def context(campaign: str, phase: str | None = None) -> arb.Context:
    rolled, toks = prior_rolls(campaign, phase, with_tokens=True)
    return arb.Context(dials=dict(load_manifest(campaign).get("dials") or {}), rolled=rolled, tokens=toks)


def taken_families(table: str, drawn_rows) -> set:
    """Families already drawn from a table whose header says `families_distinct`: the next draw of the same roll
    leaves them out (a constraint, never relaxed)."""
    if not dt.roll_header(table).get("families_distinct"):
        return set()
    fams = {r["id"]: r.get("family") for r in load_table(table)}
    return {fams[x] for x in drawn_rows if fams.get(x) is not None}


def distinct_filter(table: str, drawn_rows, where=None, why: str = "where"):
    """(where, why) with the families_distinct constraint folded in."""
    taken = taken_families(table, drawn_rows)
    if not taken:
        return where, why

    def both(row):
        return row.get("family") not in taken and (where is None or where(row))
    return both, ("family_taken" if where is None else f"family_taken or {why}")


def append_secret_exclusions(campaign: str, notes: list[dict]) -> None:
    """Exclusions of public draws that name the secret layer: kept in dm-only, never in design.json."""
    if not notes:
        return
    path = dm_only_dir(campaign) / "dice-log.json"
    log = read_json(path) or {"_meta": {"schema_version": 1, "campaign": campaign}, "rolls": []}
    log.setdefault("exclusions", []).extend(notes)
    stamp_meta(log, campaign, "design_dice.py (secret exclusions)")
    write_json_atomic(path, log)


def load_table(table: str) -> list[dict]:
    """Rows of data/design/<table> (`file.yaml` or `file.yaml#subtable`), [] when the file is missing."""
    return table_rows(table)


def derive(master: str, phase: str, table: str, label: str, attempt: int) -> random.Random:
    key = f"{master}:{phase}:{table}:{label}" + (f":a{attempt}" if attempt and attempt > 1 else "")
    return random.Random(key)


def roll(campaign: str, phase: str, label: str, table: str | None, notation: str | None,
         secret: bool, avoid_used: bool, attempt: int) -> dict:
    manifest = load_manifest(campaign)
    master = manifest["seed"]["master"]
    table_key = table or "dice"
    rng = derive(master, phase, table_key, label, attempt)
    excluded: list = []
    record = {"phase": phase, "table": table_key, "label": label, "notation": None, "raw": None,
              "row_id": None, "excluded": excluded, "attempt": attempt, "ts": now_iso()}

    rows = load_table(table) if table else []
    if rows:
        try:
            same = [r["row_id"] for r in manifest.get("dice_log") or []
                    if r.get("phase") == phase and r.get("table") == table and int(r.get("attempt") or 1) == attempt and r.get("row_id")]
            where, why = distinct_filter(table, same)
            # the phases before this one, and what this phase's own attempt has already rolled: the earlier roll stays
            ctx = context(campaign, phase)
            mine = [(r, False) for r in manifest.get("dice_log") or []]
            mine += [(r, True) for r in (read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("rolls", [])]
            for r, was_secret in mine:
                if r.get("phase") == phase and int(r.get("attempt") or 1) == attempt:
                    ctx.add(r.get("row_id"), was_secret)
                    for t in r.get("tokens") or []:
                        ctx.add_token(t, was_secret)
            res = arb.arbitrate(table, rows, ctx, where=where, why=why,
                                usage=usage(campaign, table, avoid_used), secret=secret)
        except arb.EmptyPool as exc:
            raise SystemExit(f"design_dice: {label}: {exc}")
        picked = arb.pick(rng, res["pool"], res["weights"])
        shown, real = (picked, None) if secret else arb.public_view(res, picked)
        record.update(shown)
        excluded.extend(res["excluded"])
        if res["usage_fallback"]:
            record["usage_fallback"] = res["usage_fallback"]
        if res["excluded_secret"]:
            append_secret_exclusions(campaign, [dict({"phase": phase, "label": label, "attempt": attempt,
                                                      "excluded": res["excluded_secret"]}, **(real or {}))])
    else:
        if not notation:
            raise SystemExit(f"design_dice: no table rows for {table!r} and no --notation given")
        result = dice_mod.run(notation, silent=True, rng=rng)
        record.update({"notation": notation, "raw": result})
    append_roll(campaign, record, secret=secret)
    return record


def draw(rng: random.Random, rows: list[dict], exclude: set | None = None) -> dict:
    """One weighted draw with no campaign behind it (P0's blank dials): the dial tables carry no conflicts,
    so only the caller's own exclusions apply."""
    res = arb.arbitrate("dials", rows, arb.Context(), exclude=exclude)
    return arb.pick(rng, res["pool"], res["weights"])


def excluded_text(entries) -> str:
    """A record's exclusions for the log: `t3 (used_elsewhere)`."""
    out = []
    for e in entries or []:
        if isinstance(e, dict):
            extra = e.get("with") or e.get("family")
            out.append(f"{e.get('row')} ({e.get('why', '')}{': ' + extra if extra else ''})")
        else:
            out.append(str(e))
    return ", ".join(out)


def show_log(campaign: str, secret: bool) -> int:
    if secret:
        log = read_json(dm_only_dir(campaign) / "dice-log.json") or {"rolls": []}
        rolls = log["rolls"]
    else:
        rolls = load_manifest(campaign)["dice_log"]
    for r in rolls:
        what = r.get("row_id") or r.get("raw")
        print(f"  {r['phase']:<3} {r['table']:<28} {r['label']:<24} {r['notation']:<8} → {what}"
              + (f"  (excluded {excluded_text(r['excluded'])})" if r.get("excluded") else ""))
    print(f"  {len(rolls)} {'secret ' if secret else ''}rolls")
    return 0


def used_cmd(campaign: str, a) -> int:
    used = load_used()
    if a.used_cmd == "list":
        for camp, tables in used["campaigns"].items():
            for table, rows in tables.items():
                print(f"  {camp:<24} {table:<24} {', '.join(rows)}")
        return 0
    used["campaigns"].setdefault(campaign, {}).setdefault(a.table, [])
    if a.row not in used["campaigns"][campaign][a.table]:
        used["campaigns"][campaign][a.table].append(a.row)
    save_used(used)
    print(f"design_dice: used {a.table}#{a.row} recorded for {campaign}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Seeded, labelled, logged designer dice")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("roll")
    r.add_argument("--phase", required=True)
    r.add_argument("--label", required=True)
    r.add_argument("--table")
    r.add_argument("--notation")
    r.add_argument("--secret", action="store_true")
    r.add_argument("--avoid-used", action="store_true")
    r.add_argument("--attempt", type=int, default=1)
    r.add_argument("--json", action="store_true")

    lg = sub.add_parser("log")
    lg.add_argument("--secret", action="store_true")

    u = sub.add_parser("used")
    us = u.add_subparsers(dest="used_cmd", required=True)
    us.add_parser("list")
    ua = us.add_parser("add")
    ua.add_argument("--table", required=True)
    ua.add_argument("--row", required=True)

    a = p.parse_args(argv)
    if a.cmd == "roll":
        if not a.table and not a.notation:
            print("design_dice: give --table or --notation", file=sys.stderr)
            return 2
        rec = roll(a.campaign, a.phase, a.label, a.table, a.notation, a.secret, a.avoid_used, a.attempt)
        if a.json:
            print(json.dumps(rec, ensure_ascii=False))
        else:
            what = rec.get("row_id") or rec.get("raw")
            print(f"design_dice: {a.phase} {rec['table']}#{a.label} {rec['notation']} → {what}"
                  + ("  [secret]" if a.secret else ""))
        return 0
    if a.cmd == "log":
        return show_log(a.campaign, a.secret)
    if a.cmd == "used":
        return used_cmd(a.campaign, a)
    return 2


if __name__ == "__main__":
    sys.exit(main())
