#!/usr/bin/env python3
"""
designer.py — the conductor's CLI: the deterministic half of every designer command
(plan item 19, 21.E; 24.6 #6; the slice-1c auto-approve decision of 2026-09-25).

The main session is a blind conductor: it asks the Phase 0 dials, runs these verbs, launches
one Workflow per phase, shows the script-built phase card and records approvals. It never
writes bible prose and never reads design/dm-only/ or design/_staging/; `arm` raises the read
guard so that stays true while a run is live.

CLI:
  designer.py new NAME --scale S --tone T --magic M --era E --danger D --party-size N
              [--start-level 1] --content-mix a,b,c [--must ..] [--must-not ..] [--lang tr]
              [--seed S] [--concurrency 8] [--economy] [--fixture] [--ask-approval] [--session-id ID]
        a dial given as `?` is rolled live (dials.yaml weights, logged); then design_manifest init,
        the arc skeleton, the P0 card, and the guard is armed for `birth`
  designer.py -c CAMP arm --mode birth|detail|playtest [--session-id ID] | disarm
  designer.py -c CAMP preroll --phase PN [--attempt N]      every labelled roll of the phase
  designer.py -c CAMP phase PN begin [--json]               reconcile, arm, roster with read budgets and prompts
  designer.py -c CAMP phase PN merge [--day N] [--tokens N] [--seconds S]
                                                             registry merge (per unit) + design_seed + statuses;
                                                             refused units become `failed` with their reason
  designer.py -c CAMP phase PN drop --id ID --reason TEXT    drop a roster item that never reached the registry
  designer.py -c CAMP phase PN check                        design_check --phase (redacted)
  designer.py -c CAMP phase PN card                         the phase card (design_approval.py)
  designer.py -c CAMP phase PN approve [--card F] [--onay] [--force] [--round TEXT --scope S]
                                                             record approval (+ path-scoped commit) or a correction round;
                                                             refused while a roster item is not merged unless --force
  designer.py -c CAMP phase PN rerun --reason TEXT [--reseed]
  designer.py -c CAMP status [--json]
  designer.py -c CAMP abandon --reason TEXT                 retire names and used rows, disarm
  designer.py -c CAMP commit --message TEXT                 design(<campaign>): commit, path-scoped
  designer.py -c CAMP load-pack | scene --enter ID | prep | detail ID [--finish] | spotlight | end-pack
                                                             the designer in play (play_pack.py; slice 1d)

Auto-approve (owner decision 2026-09-25): a campaign initialised with --fixture or named
`_test-*` carries `_meta.auto_approve: true`; `approve` then needs no `onay` and no `devam`.
`--ask-approval` turns that off for one test birth that should exercise the approval loop
(the campaign stays git-ignored, so nothing is committed).
A real birth requires `--onay` on `approve` (the conductor passes it only after the player
typed the word) and the conductor waits for `devam` before the next `phase begin`.

Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dice as dice_mod  # noqa: E402
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_prompts as dp  # noqa: E402
import design_tables as dt  # noqa: E402
import play_pack  # noqa: E402
from design_io import (campaign_dir, design_dir, dm_only_dir, is_fragment, now_iso, read_json,  # noqa: E402
                       sha256_file, stamp_meta, write_json_atomic)
from paths import runtime_dir  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
MARKER = "active-design.json"
AGENT_TYPES = ["workflow-subagent", "design-writer", "design-critic", "design-skeleton", "design-merge"]
PLAYTEST_ALLOWLIST = ["design/player-primer.md", "characters/", "design/threads/", "state.md"]
CARD_DIR = "_approval"


# ── helpers ───────────────────────────────────────────────────────────────────

def run_script(name: str, campaign: str, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / name), "-c", campaign, *args],
                          capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode not in (0,):
        raise SystemExit(f"designer: {name} {' '.join(args)} failed ({proc.returncode}):\n{proc.stderr.strip()}")
    return proc


def auto_approve(manifest: dict) -> bool:
    return bool(manifest.get("_meta", {}).get("auto_approve"))


def band(value) -> tuple[int, int]:
    return dt.band(value)


def marker_path() -> Path:
    return runtime_dir() / MARKER


def arm(campaign: str, mode: str, session_id: str | None) -> dict:
    data = {"campaign": campaign, "mode": mode, "session_id": session_id or None,
            "agent_types_allowed": AGENT_TYPES, "playtest_allowlist": PLAYTEST_ALLOWLIST, "armed_at": now_iso()}
    write_json_atomic(marker_path(), data)
    return data


def disarm() -> bool:
    p = marker_path()
    if p.is_file():
        p.unlink()
        return True
    return False


def git_ignored(path: Path, git_root: str | None) -> bool:
    if not git_root:
        return True
    proc = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=git_root, capture_output=True)
    return proc.returncode == 0


def design_commit(campaign: str, message: str) -> str | None:
    """A path-scoped commit in the enclosing repository (item 19.10); None when nothing to commit."""
    manifest = dm.load(campaign)
    root = manifest["_meta"].get("git_root")
    cdir = campaign_dir(campaign)
    if not root or git_ignored(cdir, root):
        return None
    rel = os.path.relpath(cdir, root).replace("\\", "/")
    subprocess.run(["git", "add", "-A", "--", rel], cwd=root, capture_output=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", rel], cwd=root)
    if staged.returncode == 0:
        return None
    subprocess.run(["git", "commit", "-q", "-m", f"design({campaign}): {message}", "--", rel], cwd=root,
                   capture_output=True, check=True)
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    return sha or None


# ── rolling: the same derivation as design_dice, batched ─────────────────────────

class Roller:
    """Batched, labelled, seeded draws; public records go to design.json, secret ones to dm-only. Every table draw
    goes through design_arbiter: the pool is filtered against every roll the campaign stands on (the earlier
    phases' latest attempts and this batch), then the die is thrown; the redraw-until-ok loop is gone."""

    def __init__(self, campaign: str, phase: str, attempt: int = 1):
        self.campaign, self.phase, self.attempt = campaign, phase, attempt
        self.manifest = dm.load(campaign)
        self.master = self.manifest["seed"]["master"]
        self.public: list[dict] = []
        self.secret: list[dict] = []
        self.secret_notes: list[dict] = []
        self.by_label: dict[str, dict] = {}
        self.ctx = dd.context(campaign, phase)        # the phases before this one, each at its latest attempt
        self.foundation: dict | None = None
        self.identity: dict | None = None
        self.identity_secret: dict | None = None      # the secret and the villain: dm-only alone
        self.naming: dict | None = None               # the languages and the calendar's roots (design/naming.json)
        self.exempt: set = set()                      # conflict pairs a forced roll was allowed to stand in
        self.pools: dict[str, int] = {}               # table → its smallest pool after the constraints (the floor)
        self.pool_of: dict[str, int] = {}             # label → that draw's pool after the constraints

    @classmethod
    def in_memory(cls, master: str, dials: dict, phase: str = "P1", attempt: int = 1) -> "Roller":
        """A Roller with no campaign behind it (the many-seeds tests): no disk, no used.json, the same draws."""
        R = cls.__new__(cls)
        R.campaign, R.phase, R.attempt, R.master = None, phase, attempt, master
        R.manifest = {"dials": dials, "dice_log": []}
        R.public, R.secret, R.secret_notes, R.by_label = [], [], [], {}
        R.ctx = arb.Context(dials=dict(dials))
        R.foundation, R.identity, R.identity_secret, R.naming, R.exempt = None, None, None, None, set()
        R.pools, R.pool_of = {}, {}
        return R

    def _usage(self, ref: str, avoid: bool) -> dict:
        return dd.usage(self.campaign, ref, avoid) if self.campaign else {}

    def _record(self, label: str, table: str | None) -> dict:
        return {"phase": self.phase, "table": table or "dice", "label": label, "notation": None, "raw": None,
                "row_id": None, "excluded": [], "attempt": self.attempt, "ts": now_iso()}

    def table(self, label: str, ref: str, secret: bool = False, avoid: bool = True, exclude: set | None = None,
              where=None, why: str = "where", also_used: set | None = None, used_keys: dict | None = None,
              weigh=None) -> dict:
        """One draw. `exclude` and `where` (with its reason `why`) are constraints; `also_used` marks values spent
        like rows used elsewhere (a pair that never repeats); `used_keys` go to used.json at approve; `weigh(row,
        ctx)` replaces the rows' own weights for this draw."""
        rows = dt.rows(ref)
        if not rows:
            raise SystemExit(f"designer: no rows in {ref}")
        rng = dd.derive(self.master, self.phase, ref, label, self.attempt)
        use = self._usage(ref, avoid)
        if also_used:
            use["pair"] = set(also_used)
        # a table whose header says families_distinct: the families this batch already drew from it are out
        drawn = [r["row_id"] for r in self.public + self.secret if r.get("table") == ref and r.get("row_id")]
        where, why = dd.distinct_filter(ref, drawn, where, why)
        try:
            res = arb.arbitrate(ref, rows, self.ctx, exclude=exclude, where=where, why=why, usage=use, secret=secret,
                                weigh=weigh)
        except arb.EmptyPool as exc:
            raise SystemExit(f"designer: {self.phase} {label}: {exc}" if not secret else
                             f"designer: {self.phase} {label} (secret): the pool is empty after the constraints — a table fault")
        self.pools[ref] = min(self.pools.get(ref, res["allowed"]), res["allowed"])
        self.pool_of[label] = res["allowed"]
        rec = self._record(label, ref)
        picked = arb.pick(rng, res["pool"], res["weights"])
        shown, real = (picked, None) if secret else arb.public_view(res, picked)
        rec.update(shown)
        rec["excluded"] = res["excluded"]
        if res["usage_fallback"]:
            rec["usage_fallback"] = res["usage_fallback"]
        if used_keys:
            rec["used_keys"] = dict(used_keys)
        if res["excluded_secret"]:
            self.secret_notes.append(dict({"phase": self.phase, "label": label, "attempt": self.attempt,
                                           "excluded": res["excluded_secret"]}, **(real or {})))
        self._keep(rec, secret)
        return rec

    def notation(self, label: str, notation: str, secret: bool = False) -> dict:
        rng = dd.derive(self.master, self.phase, "dice", label, self.attempt)
        rec = self._record(label, None)
        rec.update({"notation": notation, "raw": dice_mod.run(notation, silent=True, rng=rng)})
        self._keep(rec, secret)
        return rec

    def add_tokens(self, label: str, tokens, reason: str, secret: bool = False) -> dict | None:
        """Tokens no row carries by itself (a seated contest role's claims, the layout's): kept on a record of their
        own so every later phase's context finds them again."""
        tokens = [t for t in tokens if t]
        if not tokens:
            return None
        rec = self._record(label, "tokens")
        rec.update({"notation": "derived", "tokens": sorted(set(tokens)), "derived_from": reason})
        (self.secret if secret else self.public).append(rec)
        self.by_label[label] = rec
        for t in rec["tokens"]:
            self.ctx.add_token(t, secret)
        return rec

    def forced(self, label: str, ref: str, row_id: str, reason: str, secret: bool = False, exempt: set | None = None) -> dict:
        """A row the tables set without a die. It is held to the conflicts too; `exempt` names the rolled rows it
        may stand beside all the same (one case: the scar's prohibition is tied to the break even when the break is
        still coming). The pair is kept on `self.exempt` and on the record."""
        waived = sorted(x for x in dt.conflict_index().get(row_id, ()) if x in (exempt or ()) and self.ctx.has(x))
        try:
            if not waived:
                arb.check_forced(row_id, self.ctx)
            elif any(self.ctx.has(x) and x not in waived for x in dt.conflict_index().get(row_id, ())):
                raise arb.EmptyPool(f"the forced row {row_id} conflicts with a row already rolled — a table fault")
        except arb.EmptyPool as exc:
            raise SystemExit(f"designer: {self.phase} {label}: {exc}")
        rec = self._record(label, ref)
        rec.update({"notation": "forced", "raw": None, "row_id": row_id, "forced_by": reason})
        if waived:
            rec["conflict_exempt"] = waived
            self.exempt |= {frozenset((row_id, x)) for x in waived}
        self._keep(rec, secret)
        return rec

    def _keep(self, rec: dict, secret: bool) -> None:
        (self.secret if secret else self.public).append(rec)
        self.by_label[rec["label"]] = rec
        self.ctx.add(rec.get("row_id"), secret)

    def row(self, label: str):
        rec = self.by_label.get(label)
        return rec["row_id"] if rec else None

    def count(self, label: str, value) -> int:
        """A band → an exact count rolled once (d(hi-lo+1)); an exact number → itself. The record carries
        `value`, the count produced: the die face alone misled the conductor and the P3 skeleton (tuning birth 1)."""
        lo, hi = band(value)
        if lo == hi:
            rec = self._record(label, None)
            rec.update({"notation": "fixed", "raw": None, "value": lo})
            self._keep(rec, False)
            return lo
        rec = self.notation(label, f"d{hi - lo + 1}")
        rec["value"] = lo + int(rec["raw"]) - 1
        return rec["value"]

    def flush(self) -> tuple[int, int]:
        data = dm.load(self.campaign)
        data["dice_log"].extend(self.public)
        if self.secret:
            path = dm_only_dir(self.campaign) / "dice-log.json"
            log = read_json(path) or {"_meta": {"schema_version": 1, "campaign": self.campaign}, "rolls": []}
            log["rolls"].extend(self.secret)
            if self.identity_secret is not None:
                log["identity"] = self.identity_secret       # the secret and the villain as P1 rolled them
            stamp_meta(log, self.campaign, "designer.py preroll (secret)")
            write_json_atomic(path, log)
            dls = data["dice_log_secret"]
            dls["count"] = len(log["rolls"])
            for rec in self.secret:
                if rec["label"] not in dls["labels"]:
                    dls["labels"].append(rec["label"])
        dd.append_secret_exclusions(self.campaign, self.secret_notes)
        dm.save(self.campaign, data, f"designer.py preroll --phase {self.phase}")
        return len(self.public), len(self.secret)


def dials_of(manifest: dict) -> dict:
    return manifest["dials"]


def scale_of(manifest: dict) -> dict:
    return dt.scale_row(dials_of(manifest)["scale"])


def rolled_rows(manifest: dict, table_prefix: str) -> list[str]:
    """Row ids already rolled from a table (public log), for cross-phase constraints."""
    return [r["row_id"] for r in manifest["dice_log"]
            if (r.get("table") == table_prefix or r.get("table", "").startswith(table_prefix + "#")) and r.get("row_id")
            and not (table_prefix == "trope-breaks.yaml" and r.get("table") != table_prefix)]     # never the breaks' ties


def spread_exclude(uses: dict, n_rows: int) -> set:
    """Rows spent for an even spread: unique while the table has unused rows, then at most twice, and so on
    (the old caps fell back to the whole table once every row was spent; the arbiter stops on an empty pool)."""
    cap = sum(uses.values()) // max(1, n_rows) + 1
    return {x for x, c in uses.items() if c >= cap}


# ── preroll plans per phase ───────────────────────────────────────────────────

def preroll_p1(R: Roller, m: dict) -> None:
    """Step 1, the foundation (design_foundation.py); step 2, the identity (design_identity.py): the trope breaks,
    the people, the institution, the phenomenon and the question(s), then the secret and the villain (secret rolls,
    build item 10b), the signature-mechanic gate and, last, the names (design_names.py, build item 11b): the
    languages, their bags and roots, the calendar's roots."""
    import design_foundation as fd
    import design_identity as di
    import design_names as dn
    used_pairs = dd.used_values(R.campaign, fd.PAIR_KEY) if R.campaign else set()
    out = fd.roll(R, dials_of(m), used_pairs)
    R.foundation = fd.build(out, dials_of(m)["level_band"])
    sc = scale_of(m)
    ident = di.roll(R, dials_of(m), R.foundation)
    R.identity = di.build(ident, [r["row_id"] for r in R.public if r.get("row_id")])
    R.identity_secret = di.roll_secret(R, dials_of(m), R.foundation, R.identity)     # every roll secret; dm-only alone
    chance = int(sc["signature_mechanic_chance"])
    if chance <= 0:
        R.forced("mechanic", "dice", "no", "scale never rolls the signature mechanic")
    elif chance >= 100:
        R.forced("mechanic", "dice", "yes", "scale always rolls the signature mechanic")
    else:
        hit = R.notation("mechanic_gate", "d100")["raw"] <= chance
        R.forced("mechanic", "dice", "yes" if hit else "no", f"d100 against {chance}")
    R.naming = dn.roll(R, dials_of(m), R.foundation, R.identity)


def preroll_p2(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    breaks = rolled_rows(m, "trope-breaks.yaml")
    override = None
    for b in breaks:
        row = dt.row("trope-breaks.yaml", b) or {}
        # the one override applied today: a trope break that names a pantheon type forces it (the ancestor gods).
        # Every other override is data for the floor that owns the default (claims.yaml).
        for o in row.get("overrides") or []:
            if o.get("default") == "pantheon_type" and dt.row("pantheon.yaml#type", str(o.get("to"))):
                override = (b, o["to"])
    if override:
        R.forced("pantheon_type", "pantheon.yaml#type", override[1], f"override by {override[0]}")
    else:
        R.table("pantheon_type", "pantheon.yaml#type", avoid=False)
    R.table("pantheon_presence", "pantheon.yaml#presence", avoid=False)
    for sub in ("source", "constraint", "visibility", "regulator"):
        R.table(f"magic_{sub}", f"magic.yaml#{sub}")
    R.table("magic_taboo.1", "magic.yaml#taboo")
    if R.notation("taboo.second", "d2")["raw"] == 2 and R.row("magic_taboo.1") != "taboo_none":
        R.table("magic_taboo.2", "magic.yaml#taboo", exclude={R.row("magic_taboo.1"), "taboo_none"})
    gate = (dt.dial_row("magic", dials_of(m)["magic"]) or {}).get("effects", {}).get("wild_magic_roll", {})
    raw = R.notation("wild_gate", gate.get("notation", "d6"))["raw"]
    if raw in (gate.get("on") or []):
        R.table("wild_shape", "magic.yaml#wild", avoid=False, exclude={"wild_no"})
    else:
        R.forced("wild_shape", "magic.yaml#wild", "wild_no", f"gate {gate.get('notation', 'd6')}={raw} not in {gate.get('on')}")
    for sub in ("climate", "year_shape", "week", "moon", "start_anchor"):
        R.table(sub, f"calendar.yaml#{sub}", avoid=(sub == "climate"))
    hist = sc["history"]
    ages: list[str] = []
    for n in range(1, R.count("ages_count", hist["ages"]) + 1):
        ages.append(R.table(f"age.{n}", "history.yaml#age_template", exclude=set(ages))["row_id"])
    for n in range(1, R.count("events_count", hist["dated_events"]) + 1):
        R.table(f"event.{n}", "history.yaml#event_type", avoid=False)
        R.table(f"divergence.{n}", "history.yaml#divergence", avoid=False)
        R.table(f"memory.{n}", "history.yaml#memory", avoid=False)
    for n in range(1, R.count("deep_count", hist["deep_past_events"]) + 1):
        R.table(f"deep.{n}", "history.yaml#event_type", avoid=False)
    fests: list[str] = []
    for n in range(1, band(sc["gods"])[1] + 1):
        fests.append(R.table(f"festival.{n}", "calendar.yaml#festival_type", avoid=False, exclude=set(fests))["row_id"])


def preroll_p3(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    climate = None
    for rec in m["dice_log"]:
        if rec.get("label") == "climate":
            climate = rec.get("row_id")
    regions = R.count("regions_count", sc["regions"])
    idents: list[str] = []
    for i in range(1, regions + 1):
        R.table(f"region.{i}.biome", "regions.yaml#biome",
                where=lambda row: climate is None or climate in (row.get("climates") or []), why="climate")
        idents.append(R.table(f"region.{i}.identity", "regions.yaml#identity", exclude=set(idents))["row_id"])
        for k in range(1, R.count(f"region.{i}.landmarks_count", [2, 4]) + 1):
            R.table(f"region.{i}.landmark.{k}", "regions.yaml#landmark_kind", avoid=False)
        seen: set = set()
        for k in range(1, 7):
            seen.add(R.table(f"region.{i}.social.{k}", "regions.yaml#social_seed", avoid=False, exclude=set(seen))["row_id"])
        seen = set()
        for k in range(1, 7):
            seen.add(R.table(f"region.{i}.presence.{k}", "regions.yaml#faction_presence", avoid=False, exclude=set(seen))["row_id"])
    j = 0
    kinds = {r["id"]: r for r in dt.rows("settlements.yaml#kind")}
    for kind in ("metropolis", "city", "town", "village"):
        n = R.count(f"{kind}_count", sc["settlements"][kind])
        for _ in range(n):
            j += 1
            R.forced(f"settlement.{j}.kind", "settlements.yaml#kind", f"kind_{kind}", "scale.yaml settlements")
            R.table(f"settlement.{j}.problem", "settlements.yaml#problem")
            if kind == "village":
                continue
            R.table(f"settlement.{j}.fear", "settlements.yaml#fear")
            goods: set = set()
            for k in range(1, R.count(f"settlement.{j}.goods_count", [1, 3]) + 1):
                goods.add(R.table(f"settlement.{j}.goods.{k}", "settlements.yaml#economy_good", avoid=False, exclude=set(goods))["row_id"])
            districts: set = set()
            for k in range(1, R.count(f"settlement.{j}.districts_count", kinds[f"kind_{kind}"]["districts"]) + 1):
                districts.add(R.table(f"settlement.{j}.district.{k}", "settlements.yaml#district_type", avoid=False, exclude=set(districts))["row_id"])


def preroll_p4(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    fac = sc["factions"]
    total = R.count("factions_count", fac["count"])
    quota = fac["quota"]
    slots: list[str] = []
    for arche, cnt in quota.items():
        lo, hi = band(cnt)
        n = lo if lo == hi else R.count(f"quota.{arche}", cnt)
        slots += [f"archetype_{arche}"] * n
    pool = {f"archetype_{a}" for a in (fac.get("pool") or [])}
    for n in range(1, total + 1):
        if n <= len(slots):
            R.forced(f"faction.{n}.archetype", "factions.yaml#archetype", slots[n - 1], "scale.yaml quota")
        elif pool:
            R.table(f"faction.{n}.archetype", "factions.yaml#archetype", avoid=False,
                    where=lambda row: row.get("id") in pool, why="quota_pool")
        else:
            R.table(f"faction.{n}.archetype", "factions.yaml#archetype", avoid=False)
        R.table(f"faction.{n}.fracture", "factions.yaml#fracture")      # never `none`: the fracture table's own rule
        R.table(f"faction.{n}.endgame", "factions.yaml#endgame")
        R.table(f"faction.{n}.secret", "factions.yaml#secret_kind", secret=True)
        if R.row(f"faction.{n}.archetype") == "archetype_cult":
            R.table(f"faction.{n}.cult_doctrine", "factions.yaml#cult_doctrine")   # never `unspecified`: the doctrine table's own rule
        rungs: list[str] = []
        for k in range(1, R.count(f"faction.{n}.rungs_count", [3, 4]) + 1):
            excl = set(rungs) | ({"rung_war"} if k == 1 else set())
            rungs.append(R.table(f"faction.{n}.rung.{k}", "factions.yaml#provocation_rung", avoid=False, exclude=excl)["row_id"])
        links: list[str] = []
        for k in range(1, R.count(f"faction.{n}.links_count", [2, 4]) + 1):
            links.append(R.table(f"faction.{n}.link.{k}", "factions.yaml#access_link", avoid=False, exclude=set(links))["row_id"])
    # antagonists — every roll secret. Visibility, shape and origin are P1's since build item 10b: P4 stands on them
    # through its context. A birth whose P1 was rolled before that (a legacy birth) still rolls them here.
    import design_identity as di
    if not di.villain_in_context(R.ctx):
        R.table("bbeg_visibility", "antagonists.yaml#visibility", secret=True)
        R.table("bbeg_shape", "antagonists.yaml#villain_shape", secret=True)
        R.table("bbeg_origin", "antagonists.yaml#origin", secret=True)
    # religious only when a rolled secret or break admits it (`allowed_via`): the arbiter reads every rolled row
    R.table("bbeg_faction_archetype", "antagonists.yaml#bbeg_faction_archetype", secret=True, avoid=False)
    R.table("front_template", "antagonists.yaml#front_template", secret=True)
    R.table("doom_shape", "antagonists.yaml#doom_shape", secret=True)
    roles: list[str] = []
    for n in range(1, R.count("lieutenants_count", sc["antagonists"]["lieutenants"]) + 1):
        roles.append(R.table(f"lieutenant.{n}.role", "antagonists.yaml#lieutenant_role", secret=True, avoid=False, exclude=set(roles))["row_id"])
    R.count("regional_count", sc["antagonists"]["regional"])


def registry_rows(campaign: str, etype: str) -> tuple[int, int]:
    """(rows of `etype` in the canonical registry, of which stubs): the reservations a count roll nets out (RC-03)."""
    canon = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    rows = [r for r in canon.values() if r.get("type") == etype]
    return len(rows), sum(1 for r in rows if r.get("status") == "pending")


def net_count(R: Roller, label: str, band_value, existing: int, what: str) -> tuple[int, int]:
    """The band roll as the total, never below what the registry already holds, and `<label>_new` = total − existing as
    an exact count line of its own (RC-03: P5 rolled the total from the die alone and the skeleton was told both 'fill
    every stub' and 'exactly N')."""
    total = R.count(label, band_value)
    if existing > total:
        R.by_label[label]["value"] = total = existing
        R.by_label[label]["raised_to_reserved"] = f"{existing} {what} already in the registry"
    rec = R._record(label.replace("_count", "_new_count"), None)
    rec.update({"notation": "derived", "raw": None, "value": total - existing,
                "derived_from": f"{label} {total} − {existing} already in the registry"})
    R._keep(rec, False)
    return total, total - existing


def preroll_p5(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    n_npcs, _ = net_count(R, "npcs_count", sc["named_npcs"], registry_rows(R.campaign, "npc")[0], "npcs")
    tic_uses: dict[str, int] = {}
    reg_uses: dict[str, int] = {}
    secret_uses: dict[str, int] = {}
    secret_rows = len(dt.rows("npcs.yaml#secret"))
    for n in range(1, n_npcs + 1):
        for axis in ("trust", "ambition", "loyalty", "courage"):
            R.notation(f"npc.{n}.axis.{axis}", "d5")
        # the secret kind is dm-only (tuning birth 1: P5 printed all 14 to the conductor as public);
        # no kind twice while the table still has unused rows, never more than twice
        spent_secrets = spread_exclude(secret_uses, secret_rows)
        srec = R.table(f"npc.{n}.secret", "npcs.yaml#secret", secret=True, avoid=False, exclude=spent_secrets)
        secret_uses[srec["row_id"]] = secret_uses.get(srec["row_id"], 0) + 1
        # a tic twice needs a differentiator the writers rarely give (rubric_p5_voice_distinct failed 9 of 18 times):
        # unique while npcs.yaml#speech_tic has unused rows, never more than twice
        spent = spread_exclude(tic_uses, len(dt.rows("npcs.yaml#speech_tic")))
        rec = R.table(f"npc.{n}.tic", "npcs.yaml#speech_tic", avoid=False, exclude=spent)
        tic_uses[rec["row_id"]] = tic_uses.get(rec["row_id"], 0) + 1
        # the voice's register, unique while the table has rows (every birth's P5 phase critic flagged shared registers)
        spent_reg = spread_exclude(reg_uses, len(dt.rows("npcs.yaml#voice_register")))
        reg = R.table(f"npc.{n}.register", "npcs.yaml#voice_register", avoid=False, exclude=spent_reg)
        reg_uses[reg["row_id"]] = reg_uses.get(reg["row_id"], 0) + 1
        R.notation(f"npc.{n}.species", "d100")
        R.notation(f"npc.{n}.gender", "d100")


def preroll_p6(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    bands = dt.scale_shared()["room_bands"]
    tele = {d: [r["id"] for r in dt.rows("sites.yaml#telegraph") if r["distance"] == d] for d in ("far", "near", "threshold")}
    n = 0
    for role, cnt in sc["sites"]["roles"].items():
        for _ in range(int(cnt)):
            n += 1
            R.forced(f"site.{n}.role", "sites.yaml#role_band", f"role_{role}", "scale.yaml sites.roles")
            R.table(f"site.{n}.type", "sites.yaml#site_type", avoid=False)
            for d in ("far", "near", "threshold"):
                R.table(f"site.{n}.telegraph.{d}", "sites.yaml#telegraph", avoid=False,
                        where=lambda row, d=d: row.get("distance") == d, why="distance")
            R.table(f"site.{n}.escape", "sites.yaml#escape", avoid=False)
            R.table(f"site.{n}.attitude", "sites.yaml#attitude", avoid=False)
            R.table(f"site.{n}.payoff", "sites.yaml#payoff", avoid=False)
            R.table(f"site.{n}.never_visited", "sites.yaml#never_visited", avoid=False)
            R.count(f"site.{n}.rooms", bands[role])
            R.table(f"site.{n}.hoard", "loot-budget.yaml#hoard_flavour", avoid=False)


def preroll_p7(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    scale = dials_of(m)["scale"]
    for b in dt.rows("arc.yaml#beat_template"):
        if scale in b["scales"]:
            R.table(f"beat.{b['id']}.change", "arc.yaml#change_kind", avoid=False)
    for ch in m.get("arc_skeleton") or []:
        nodes: list[str] = []
        for k in range(1, R.count(f"{ch['chapter']}.nodes_count", [3, 5]) + 1):
            nodes.append(R.table(f"{ch['chapter']}.node.{k}", "arc.yaml#node", avoid=False, exclude=set(nodes))["row_id"])
    for act in range(1, int(sc["acts"]) + 1):
        for k in range(1, R.count(f"act.{act}.hooks_count", dt.scale_shared()["planted_hooks_per_act"]) + 1):
            R.table(f"act.{act}.hook.{k}", "arc.yaml#planted_hook_kind", avoid=False)
    existing, stubs = registry_rows(R.campaign, "seed")
    _, new = net_count(R, "seeds_count", sc["quest_seeds"], existing, "seeds")
    for k in range(1, stubs + new + 1):      # a shape for every seed stub to fill and every new seed; filled seeds keep theirs
        R.table(f"seed.{k}", "arc.yaml#seed_shape", avoid=False)
    R.table("opening", "arc.yaml#opening_scene_type", avoid=False)
    R.table("plot_engine", "arc.yaml#plot_engine", avoid=False)
    socket_uses: dict[str, int] = {}
    n_sockets = len(dt.rows("threads.yaml#socket_type"))
    for k in range(1, int(dials_of(m)["party_size"]) * int(sc["sockets_per_pc"]) + 1):
        sid = R.table(f"socket.{k}", "threads.yaml#socket_type", avoid=False,
                      exclude=spread_exclude(socket_uses, n_sockets))["row_id"]
        socket_uses[sid] = socket_uses.get(sid, 0) + 1


def preroll_p8(R: Roller, m: dict) -> None:
    R.count("rumours_count", [3, 5])


def preroll_p9(R: Roller, m: dict) -> None:
    party = int(dials_of(m)["party_size"])
    sc = scale_of(m)
    for n in range(1, party + 1):
        R.table(f"pc.{n}.truth", "threads.yaml#truth_kind", secret=True, avoid=False)
        R.table(f"pc.{n}.antagonist", "threads.yaml#antagonist_binding", secret=True, avoid=False)
        R.table(f"pc.{n}.mission_verb", "threads.yaml#mission_verb", avoid=False)   # never find-out-who: the verb table's own rule
    if party > 1:
        for act in range(1, int(sc["acts"]) + 1):
            R.table(f"crossing.{act}", "threads.yaml#crossing", avoid=False)


PREROLL = {"P1": preroll_p1, "P2": preroll_p2, "P3": preroll_p3, "P4": preroll_p4, "P5": preroll_p5,
           "P6": preroll_p6, "P7": preroll_p7, "P8": preroll_p8, "P9": preroll_p9}


def preroll(campaign: str, phase: str, attempt: int | None) -> int:
    m = dm.load(campaign)
    if phase not in dm.PHASES:
        print(f"designer: unknown phase {phase}", file=sys.stderr)
        return 2
    ph = m["phases"][phase]
    if attempt is None:
        attempt = max(1, int(ph.get("attempt") or 1))
    if any(r.get("phase") == phase and r.get("attempt") == attempt for r in m["dice_log"]):
        print(f"designer: {phase} attempt {attempt} already prerolled ({sum(1 for r in m['dice_log'] if r.get('phase') == phase)} public rolls); "
              "use --attempt N to redraw", file=sys.stderr)
        return 1
    R = Roller(campaign, phase, attempt)
    fn = PREROLL.get(phase)
    if fn:
        fn(R, m)
    n_pub, n_sec = R.flush()
    if R.foundation is not None:
        data = dm.load(campaign)
        data["foundation"] = R.foundation        # public and stamped: the identity builds on it, never changes it
        dm.save(campaign, data, f"designer.py preroll --phase {phase} (foundation)")
        print("designer: foundation")
        for line in R.foundation["rendering"]:
            print(f"  {line['label']}: {line['text']}")
        print(f"designer: escalation — {R.foundation['escalation']['steps']} step(s)")
    if R.identity is not None:
        import design_identity as di
        data = dm.load(campaign)
        data["identity"] = R.identity            # public and stamped, like the foundation
        dm.save(campaign, data, f"designer.py preroll --phase {phase} (identity)")
        print(f"designer: identity — {di.line(R.identity)}")
    import design_names as dn
    if R.naming is not None:
        # build item 11b: the script writes design/naming.json, the stocks, the secret stock and the candidates
        naming = dn.write_rolled(campaign, R.naming, phase, attempt)
        print("designer: names — " + "; ".join(f"{lid}: {L['bag']} (group {L['group']}), {len(L['roots'])} roots"
                                                for lid, L in naming["languages"].items()))
        print("designer: candidates — " + "; ".join(f"{slot}: {', '.join(c['name'] for c in s['names'])}"
                                                     for slot, s in naming["candidates"].items()))
        # build item 12a: the promise ledger, built from the rolls after the naming rolls (errata 24.2 #23)
        import design_promises as dpr
        n_open, n_hidden = dpr.build_for(campaign)
        print(f"designer: promises — {n_open} public, {n_hidden} secret (counts only)")
        import design_door
        design_door.seal(campaign)              # build item 13b: what the preroll wrote is the writer's ground
    elif phase not in ("P0", "P1"):
        # root-cause analysis 1, RC-13: person and god names are rolled, never invented
        if dn.ensure_pool(campaign, phase, attempt) is not None:
            print("designer: " + "; ".join(f"{lid}: {sum(1 for e in L['person'] if not e.get('used_by'))} person / "
                                            f"{sum(1 for e in L['god'] if not e.get('used_by'))} god names unused"
                                            for lid, L in dn.load_pool(campaign)["languages"].items()))
    data = dm.load(campaign)
    if data["phases"][phase]["status"] in ("pending", "stale", "failed"):
        data["phases"][phase]["status"] = "prerolled"
        data["phases"][phase]["attempt"] = attempt
        dm.save(campaign, data, f"designer.py preroll --phase {phase}")
    print(f"designer: {phase} prerolled — {n_pub} public rolls, {n_sec} secret (labels only in design.json)")
    for rec in R.public:
        what = rec.get("row_id") or (f"{rec.get('raw')} → count {rec['value']}" if "value" in rec else
                                     ", ".join(rec["items"]) if rec.get("items") else rec.get("raw"))
        print(f"  {rec['label']:<32} {rec['table']:<32} {rec['notation'] or '':<7} → {what}")
    return 0


# ── new ───────────────────────────────────────────────────────────────────────

def roll_blank_dials(seed: str, given: dict) -> tuple[dict, list[dict]]:
    """Blank dials (`?`) are rolled with dials.yaml weights; the records are logged after init."""
    resolved, records = dict(given), []
    for dial in ("scale", "tone", "magic", "era", "danger"):
        if given.get(dial) in (None, "?", ""):
            ref = f"dials.yaml#{dial}"
            rng = dd.derive(seed, "P0", ref, f"dial.{dial}", 1)
            rec = {"phase": "P0", "table": ref, "label": f"dial.{dial}", "attempt": 1, "ts": now_iso(), "excluded": []}
            rec.update(dd.draw(rng, dt.rows(ref)))
            rec.pop("excluded_rows", None)
            resolved[dial] = (dt.row(ref, rec["row_id"]) or {})["value"]
            records.append(rec)
    mix = given.get("content_mix")
    if mix in (None, "?", ""):
        chosen: list[str] = []
        for n in (1, 2, 3):
            ref = "dials.yaml#content_mix"
            rng = dd.derive(seed, "P0", ref, f"content_mix.{n}", 1)
            rec = {"phase": "P0", "table": ref, "label": f"content_mix.{n}", "attempt": 1, "ts": now_iso(), "excluded": []}
            rec.update(dd.draw(rng, dt.rows(ref), exclude=set(chosen)))
            rec.pop("excluded_rows", None)
            chosen.append(rec["row_id"])
            records.append(rec)
        resolved["content_mix"] = ",".join((dt.row("dials.yaml#content_mix", c) or {})["value"] for c in chosen)
    return resolved, records


def p0_card(campaign: str, manifest: dict, records: list[dict]) -> Path:
    d = manifest["dials"]
    lines = [f"# Phase 0 — the dials ({campaign})", "",
             f"- **Scale:** {d['scale']} · **Tone:** {d['tone']} · **Magic:** {d['magic']} · **Era:** {d['era']} · **Danger:** {d['danger']}",
             f"- **Party:** {d['party_size']} characters, level {d['start_level']} → band {d['level_band'][0]}-{d['level_band'][1]}",
             f"- **Content mix:** {', '.join(d['content_mix'])}",
             f"- **Seed:** `{manifest['seed']['master']}`",
             f"- **Wishes:** must: {', '.join(d['wishes']['must']) or '—'}; must not: {', '.join(d['wishes']['must_not']) or '—'}", ""]
    if records:
        lines.append("## Rolls (blank dials)")
        for r in records:
            lines.append(f"- `{r['label']}` {r['notation']} → {r['raw']} = **{r['row_id']}**")
        lines.append("")
    lines.append("## The arc skeleton")
    for ch in manifest["arc_skeleton"]:
        lines.append(f"- {ch['chapter']} — act {ch['act']}, levels {ch['level_band'][0]}-{ch['level_band'][1]}")
    path = design_dir(campaign) / CARD_DIR / "P0.card.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def new(a) -> int:
    name = a.name
    seed = a.seed or dm.new_seed(name)
    given = {"scale": a.scale, "tone": a.tone, "magic": a.magic, "era": a.era, "danger": a.danger, "content_mix": a.content_mix}
    resolved, records = roll_blank_dials(seed, given)
    init_args = argparse.Namespace(scale=resolved["scale"], tone=resolved["tone"], magic=resolved["magic"], era=resolved["era"],
                                   danger=resolved["danger"], party_size=a.party_size, start_level=a.start_level,
                                   content_mix=resolved["content_mix"], must=a.must, must_not=a.must_not, lang=a.lang,
                                   seed=seed, concurrency=a.concurrency, economy=a.economy, fixture=a.fixture)
    rc = dm.init(name, init_args)
    if rc != 0:
        return rc
    data = dm.load(name)
    data["_meta"]["auto_approve"] = bool((a.fixture or name.startswith("_test-")) and not a.ask_approval)
    data["dice_log"].extend(records)
    data["phases"]["P0"]["status"] = "awaiting_approval"
    data["phases"]["P0"]["started"] = data["phases"]["P0"].get("started") or now_iso()
    dm.save(name, data, "designer.py new")
    card = p0_card(name, data, records)
    arm(name, "birth", a.session_id)
    for r in records:
        print(f"  roll: {r['label']} {r['notation']} → {r['raw']} = {r['row_id']}")
    print(f"designer: {name} initialised (seed {seed}, auto_approve {data['_meta']['auto_approve']}); guard armed for birth")
    print(f"designer: P0 card {card}")
    if data["_meta"]["auto_approve"]:
        return approve_phase(name, "P0", str(card), onay=True)
    print("designer: P0 awaits `onay`")
    return 0


# ── phase verbs ───────────────────────────────────────────────────────────────

def phase_begin(campaign: str, phase: str, as_json: bool, session_id: str | None) -> int:
    m = dm.load(campaign)
    if m["_meta"].get("mode") != "birth":
        print("designer: manifest mode is not birth; use set-mode birth or `detail`", file=sys.stderr)
        return 1
    prev = dm.PHASES[dm.PHASES.index(phase) - 1] if phase != "P0" else None
    if prev and m["phases"][prev]["status"] != "approved":
        print(f"designer: {prev} is {m['phases'][prev]['status']}, not approved; {phase} cannot begin", file=sys.stderr)
        return 1
    if m["phases"][phase]["status"] == "approved":
        print(f"designer: {phase} is approved; `phase {phase} rerun --reason …` reopens it", file=sys.stderr)
        return 1
    arm(campaign, "birth", session_id)
    dm.reconcile(campaign, quiet=True)
    data = dm.load(campaign)
    ph = data["phases"][phase]
    staged = [e for e in ph.get("roster") or [] if data["entities"].get(e, {}).get("status") == "staged"]
    if staged:
        # birth 2: a stopped Workflow leaves finished fragments in staging; they are merged, not rewritten
        print(f"designer: {phase} has {len(staged)} staged fragment(s) not merged yet ({', '.join(staged)}); "
              f"run `phase {phase} merge` first", file=sys.stderr)
        return 1
    if ph["status"] in ("pending", "prerolled", "stale", "failed", "partial"):
        ph["status"] = "running"
        ph["started"] = ph.get("started") or now_iso()
        ph["attempt"] = max(1, int(ph.get("attempt") or 1))
    if not ph.get("roster") and dp.prompt_for(phase, None) is None:
        ph["roster"] = document_roster(campaign, phase)
        ph["skeleton"] = {"status": "n/a", "agent": None}
    dm.save(campaign, data, f"designer.py phase {phase} begin")
    out = pending_with_prompts(campaign, phase)
    if as_json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"designer: {phase} attempt {out['attempt']}, skeleton {out['skeleton'].get('status')}, "
              f"{len(out['entities'])} pending of {len(ph.get('roster') or [])}")
        if out["skeleton"].get("prompt"):
            print(f"  skeleton -> {out['skeleton']['prompt_cmd']}")
        for e in out["entities"]:
            print(f"  {e['id']:<28} {e['status']:<8} {e.get('prompt') or '?':<16} files {len(e['files'])}")
    return 0


def document_roster(campaign: str, phase: str) -> list[str]:
    """Single-writer phases have no skeleton: the roster is the document(s) the phase writes."""
    slug = campaign.replace("-", "_")
    proj = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
    if phase == "P1":
        return [f"premise_{slug}"]
    if phase == "P2":
        return ["doc_cosmology"]
    if phase == "P8":
        cultures = [eid for eid, e in proj.items() if e.get("type") == "polity"]
        return [f"primer_{eid}" for eid in cultures] or ["primer_all"]
    if phase == "P9":
        threads = [f"thread_{eid[3:]}" for eid, e in proj.items() if e.get("type") == "pc"]
        return threads + ["doc_session1"]
    return []


def rel_path(campaign: str, p: Path) -> str:
    return p.resolve().relative_to(campaign_dir(campaign).resolve()).as_posix()


def document_reads(campaign: str, phase: str, eid: str, proj: dict) -> list[str]:
    """Default read list of a document-roster item (no skeleton names its files; birth 2 gave the primer `files: []`)."""
    root = campaign_dir(campaign)
    if phase == "P2":
        want = ["design/premise.md", "design/dm-only/premise-secret.md", "design/naming.json", "design/entities.json"]
    elif phase == "P8":
        pid = eid[len("primer_"):] if eid.startswith("primer_") else None
        want = ["design/premise.md", "design/cosmology.md", "design/naming.json", "design/entities.json", "design/map.json",
                "calendar.json", "design/news.json", "design/common-knowledge.json"]
        for kind in ("region", "settlement", "faction"):
            for oid, e in proj.items():
                if e.get("type") == kind and (pid is None or pid == "all" or e.get("polity") == pid or oid == pid) and e.get("file"):
                    want.append(e["file"])
        for oid, e in proj.items():
            if e.get("type") == "polity" and e.get("file"):
                want.append(e["file"])
    elif phase == "P9":
        want = ["design/premise.md", "design/arc.md", "design/entities.json", "design/player-primer.md", "design/naming.json"]
        if eid.startswith("thread_"):
            pcid = "pc_" + eid[len("thread_"):]
            pc = proj.get(pcid) or {}
            for f in (pc.get("sheet"), pc.get("file")):
                if f:
                    want.append(f)
            for sid, s in proj.items():
                if s.get("type") == "socket" and (s.get("bound_to") == pcid or not s.get("bound_to")):
                    for ref in (s.get("npc"), s.get("faction")):
                        if ref and proj.get(ref, {}).get("file"):
                            want.append(proj[ref]["file"])
            for fid, f in proj.items():
                if f.get("type") == "faction" and f.get("file"):
                    want.append(f["file"])
            for oid, e in proj.items():
                if e.get("type") == "thread" and e.get("file") and oid != eid:
                    want.append(e["file"])
        else:   # the session-1 pack
            mp = read_json(design_dir(campaign) / "map.json") or {}
            hub = next((n["id"] for n in mp.get("nodes", []) if n.get("hub")), None)
            if hub and proj.get(hub, {}).get("file"):
                want.append(proj[hub]["file"])
            chapters = sorted(((cid, c) for cid, c in proj.items() if c.get("type") == "chapter"), key=lambda kv: kv[1].get("order") or 99)
            if chapters and chapters[0][1].get("file"):
                want.append(chapters[0][1]["file"])
            for p in sorted((design_dir(campaign) / "player").glob("*.md")) if (design_dir(campaign) / "player").is_dir() else []:
                want.append(rel_path(campaign, p))
            overlay = read_json(design_dir(campaign) / "overlay.json") or {}
            for sid, rec in (overlay.get("entries") or {}).items():
                if (rec.get("status") or {}).get("value") == "detailed" and proj.get(sid, {}).get("file"):
                    want.append(proj[sid]["file"])
            want += ["design/news.json", "calendar.json"]
    else:
        want = []
    return [w for w in dict.fromkeys(want) if (root / w).is_file()]


def render_cmd(campaign: str, name: str, entity_id: str | None, attempt: int, order: int = 1, phase: str | None = None) -> str:
    # root-cause analysis 1, RC-16: a Windows path's backslashes collapse in the agents' bash, and 402 of 523 agents
    # lost their first call to it; the command an agent runs verbatim carries forward slashes
    cmd = f"py -X utf8 {(SCRIPTS / 'design_prompts.py').as_posix()} -c {campaign} render {name}"
    if entity_id:
        cmd += f" --id {entity_id}"
    cmd += f" --attempt {attempt}"
    if phase:
        cmd += f" --phase {phase}"
    if order != 1:
        cmd += f" --critic-order {order}"
    return cmd


def prompt_bundle(campaign: str, phase: str, name: str, entity_id: str | None, attempt: int) -> dict:
    """The render command, a rendered copy under design/_prompts/ (readable by the conductor) and the critic count."""
    out_dir = design_dir(campaign) / "_prompts" / phase
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = entity_id or "skeleton"
    text = dp.render(campaign, name, entity_id, attempt, phase_override=phase)
    path = out_dir / f"{stem}.md"
    path.write_text(text, encoding="utf-8", newline="\n")
    fm, _ = dp.load(name)
    bundle = {"prompt": name, "prompt_cmd": render_cmd(campaign, name, entity_id, attempt, phase=phase), "prompt_file": str(path),
              "prompt_chars": len(text), "critics": int(fm.get("critics") or 1), "effort": fm.get("effort", "medium")}
    critic_name = "critic" if entity_id else "skeleton_critic"
    crit = dp.render(campaign, critic_name, entity_id or "skeleton", attempt, 1, phase_override=phase)
    cpath = out_dir / f"{stem}.critic.md"
    cpath.write_text(crit, encoding="utf-8", newline="\n")
    bundle["critic_cmd"] = render_cmd(campaign, critic_name, entity_id or "skeleton", attempt, phase=phase)
    bundle["critic_file"] = str(cpath)
    if bundle["critics"] > 1:
        bundle["critic2_cmd"] = render_cmd(campaign, critic_name, entity_id or "skeleton", attempt, 2, phase=phase)
    return bundle


def heavy_entity(row: dict) -> bool:
    """A registry row that earns two critics at high effort: majors, the BBEG and the lieutenants."""
    return row.get("tier") == "major" or str(row.get("role") or "") in ("bbeg", "lieutenant") or bool(row.get("goal_tracked"))


def pending_with_prompts(campaign: str, phase: str) -> dict:
    data = dm.load(campaign)
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    ph = data["phases"][phase]
    attempt = max(1, int(ph.get("attempt") or 1))
    reads = ph.get("reads") or {}
    rows = []
    for eid in ph.get("roster") or []:
        row = data["entities"].get(eid, {"status": "pending", "attempt": 0})
        if dm.ENTITY_RANK.get(row.get("status", "pending"), 0) >= dm.ENTITY_RANK["merged"]:
            continue
        budget = dm.read_budget(campaign, canonical, eid) if eid in canonical else []
        files = list(dict.fromkeys(budget + list(reads.get(eid) or [])))
        if not files:
            proj = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
            files = document_reads(campaign, phase, eid, proj)
        recorded = int(row.get("attempt") or 0)
        render_attempt = recorded + 1 if row.get("status") == "failed" and recorded else max(attempt, recorded or attempt)
        files = [dm.rel(campaign, Path(f)) if os.path.isabs(f) else f for f in files]
        files = list(dict.fromkeys(files))
        entry = {"id": eid, "status": row.get("status", "pending"), "attempt": recorded, "render_attempt": render_attempt,
                 "last_error": row.get("last_error"), "files": files}
        name = dp.prompt_for(phase, eid)
        if name:
            entry.update(prompt_bundle(campaign, phase, name, eid, render_attempt))
            if heavy_entity(canonical.get(eid, {})) and entry.get("critic_cmd"):
                # plan item 19.3: two critics at high effort on the BBEG, the lieutenants and every major (birth 2:
                # the P5 roster carried none; the prompt's front matter is the floor, the registry row raises it)
                entry["critics"] = 2
                entry["effort"] = "high"
                entry["critic2_cmd"] = render_cmd(campaign, "critic", eid, render_attempt, 2, phase=phase)
        rows.append(entry)
    skeleton = dict(ph.get("skeleton") or {})
    sk_name = dp.prompt_for(phase, None)
    if sk_name and skeleton.get("status") in (None, "pending"):
        skeleton.update(prompt_bundle(campaign, phase, sk_name, None, attempt))
    phase_critic = {"prompt": "phase_critic", "prompt_cmd": render_cmd(campaign, "phase_critic", None, attempt, phase=phase)}
    wishes_critic = {"prompt": "wishes_critic", "prompt_cmd": render_cmd(campaign, "wishes_critic", None, attempt, phase=phase)}
    return {"campaign": campaign, "phase": phase, "attempt": attempt, "auto_approve": auto_approve(data),
            "skeleton": skeleton, "directions": ph.get("directions", []), "seed": data["seed"]["master"],
            "entities": rows, "phase_critic": phase_critic, "wishes_critic": wishes_critic,
            "workflow": "design-skeleton" if (skeleton.get("prompt") and skeleton.get("status") in (None, "pending")) else "design-fanout"}


def record_critics(campaign: str, phase: str) -> int:
    """Critic returns saved as <id>.critic<N>[.loopK].json in staging go to the manifest, ids and codes only."""
    staging = design_dir(campaign) / "_staging" / phase
    if not staging.is_dir():
        return 0
    merged = staging / "merged"
    n = 0
    for path in sorted(staging.glob("*.critic*.json")):
        m = re.match(r"^(?P<stem>.+?)\.critic(?P<order>\d)(?:\.loop\d+)?\.json$", path.name)
        order = int(m.group("order")) if m else 1
        proc = run_script("design_approval.py", campaign, "critique", "--phase", phase, "--file", str(path), "--critic", str(order))
        if proc.returncode == 0:
            merged.mkdir(exist_ok=True)
            path.replace(merged / path.name)
            n += 1
        else:
            print(f"designer: critic return {path.name} refused: {proc.stderr.strip()}", file=sys.stderr)
    if n:
        print(f"designer: {phase} {n} critic return(s) recorded")
    return n


def code_sha() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(SCRIPTS), capture_output=True, text=True)
        return out.stdout.strip() or None
    except OSError:
        return None


SEED_LINE = re.compile(r"(\d+) call\(s\) made, (\d+) already seeded, (\d+) failed")


def seed_result(proc: subprocess.CompletedProcess) -> dict:
    """design_seed's last line as numbers; the approve gate reads `failed` (RC-08: failures were printed and ignored)."""
    m = SEED_LINE.search(proc.stdout or "")
    made, skipped, failed = (int(x) for x in m.groups()) if m else (0, 0, 0 if proc.returncode == 0 else 1)
    return {"made": made, "skipped": skipped, "failed": failed,
            "unsupported": (proc.stderr or "").count("unsupported seed skipped")}


def refusal_owner(campaign: str, phase: str, uid: str, roster: list) -> str:
    """The entity that answers for a refused unit: itself when it has a writer prompt, else the roster entity named by
    the refused fragment's agent label (`P7.chapter_2.a1` → chapter_2)."""
    if dp.prompt_for(phase, uid):
        return uid
    refused_dir = design_dir(campaign) / "_staging" / phase / "refused"
    frags = sorted(refused_dir.glob(f"{uid}.attempt-*.json"), key=lambda p: p.stat().st_mtime) if refused_dir.is_dir() else []
    agent = str((read_json(frags[-1]) or {}).get("agent") or "") if frags else ""
    parts = agent.split(".")
    writer = parts[1] if len(parts) >= 3 else ""
    return writer if writer in roster and dp.prompt_for(phase, writer) else uid


def phase_merge(campaign: str, phase: str, day: int, tokens: int | None = None, seconds: int | None = None,
                run_dirs: list | None = None) -> int:
    record_critics(campaign, phase)
    # root-cause analysis 1, RC-09: the Workflow's totalTokens is summed peak context, not output; the run's own
    # transcripts say what the phase cost, per role
    for rd in run_dirs or []:
        import design_cost as dc
        dc.record(campaign, phase, rd)
    report_path = design_dir(campaign) / "_staging" / phase / "merge.report.json"
    if report_path.is_file():
        report_path.unlink()            # birth 2: never read a previous run's report
    proc = run_script("registry.py", campaign, "merge", "--phase", phase, "--day", str(day))
    print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    fragments_waiting = any(is_fragment(p) for p in (design_dir(campaign) / "_staging" / phase).glob("*.json")) \
        if (design_dir(campaign) / "_staging" / phase).is_dir() else False
    if proc.returncode not in (0, 1) or (fragments_waiting and not report_path.is_file()):
        # birth 2 (3.1): registry.py died on a fragment and the conductor saw exit 0 and 77 seed calls
        print(f"designer: registry.py merge crashed (exit {proc.returncode}); nothing seeded, {phase} unchanged — "
              "the traceback above is a development finding; fix the script, then run this merge again", file=sys.stderr)
        return 1
    report = read_json(report_path) or {}
    refused: dict = report.get("refused") or {}
    # root-cause analysis 1, RC-08: design_seed reads merged/ only, and skeleton.json moved there after the seed ran,
    # so a skeleton's graph was seeded one merge late or never; absorb first, then seed, and keep the result
    absorbed = absorb_skeleton(campaign, phase)
    import design_promises as dpr
    promised = dpr.sync(campaign, phase)          # the stubs and placements this merge reserved join the ledger
    if promised:
        print(f"designer: promises — {promised} added by this merge (stubs and placements)")
    seed = run_script("design_seed.py", campaign, "--phase", phase)
    print(seed.stdout.strip())
    if seed.returncode != 0:
        print(seed.stderr.strip(), file=sys.stderr)
    dm.reconcile(campaign, quiet=True)
    data = dm.load(campaign)
    ph = data["phases"][phase]
    ph["seed"] = dict(seed_result(seed), at=now_iso())
    sha = code_sha()
    if sha and sha not in (ph.get("code") or []):
        ph.setdefault("code", []).append(sha)     # the code each merge ran under: a mixed-code phase shows two (RC-10)
    merged_now = bool(report.get("units"))
    skeleton_missing = phase in dm.SKELETON_PHASES and (ph.get("skeleton") or {}).get("status") == "pending"
    if not merged_now and not absorbed and not refused and skeleton_missing:
        # birth 2 (R.5): a Workflow that died before writing anything left "P6 merged" with nothing in it
        if tokens:
            ph.setdefault("tokens", {"out": 0})["out"] = int((ph.get("tokens") or {}).get("out") or 0) + int(tokens)
        if seconds:
            ph["wall_s"] = int(ph.get("wall_s") or 0) + int(seconds)
        dm.save(campaign, data, f"designer.py phase {phase} merge")
        print(f"designer: {phase} nothing merged and no skeleton absorbed — status stays {ph['status']}; "
              f"run `phase {phase} begin --json` and the Workflow again", file=sys.stderr)
        return 1
    for uid, reasons in refused.items():
        # dry-3 P7: the chapter writers re-emitted five node rows, the door refused them, and the nodes (no writer
        # prompt of their own) were listed nowhere; a writerless unit's refusal goes to the roster entity whose
        # writer produced it, with the unit's id in the reason
        owner = refusal_owner(campaign, phase, uid, ph.get("roster") or [])
        if owner != uid:
            reasons = [f"{uid}: {r}" if not r.startswith(uid) else r for r in reasons]
        row = data["entities"].setdefault(owner, {"phase": phase, "status": "pending", "attempt": 0, "critique_loops": 0,
                                                  "last_error": None, "file": None, "stage_file": None, "agent": None})
        row["status"] = "failed"
        row["last_error"] = "; ".join(reasons)[:600]
        row["attempt"] = max(int(row.get("attempt") or 0), 1)
        # ...and stays failed until a fragment newer than the one merged before the refusal replaces it: reconcile
        # used to rank the older merged fragment as proof and flip the refusal back to merged
        prior = design_dir(campaign) / "_staging" / phase / "merged" / f"{owner}.json"
        row["failed_over"] = {"phase": phase, "sha256": sha256_file(prior) if prior.is_file() else None}
        if owner not in (ph.get("roster") or []) and not (ph.get("skeleton") or {}).get("status") in (None, "pending"):
            ph.setdefault("roster", []).append(owner)
    if tokens:
        ph.setdefault("tokens", {"out": 0})["out"] = int((ph.get("tokens") or {}).get("out") or 0) + int(tokens)
    if seconds:
        ph["wall_s"] = int(ph.get("wall_s") or 0) + int(seconds)
    if ph["status"] in ("running", "generated", "partial"):
        ph["status"] = "merged" if not any(data["entities"].get(e, {}).get("status") in ("pending", "staged", "failed")
                                           for e in ph.get("roster") or []) else "partial"
    dm.save(campaign, data, f"designer.py phase {phase} merge")
    if phase == "P9" and ph["status"] == "merged":
        # design integrate: every thread's public face for the player, the npc index and the master index refreshed
        proj9 = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
        for tid, t in sorted(proj9.items()):
            if t.get("type") == "thread":
                tf = run_script("render_player.py", campaign, "thread-face", tid)
                tail = (tf.stdout or tf.stderr).strip().splitlines()
                print(tail[-1] if tail else f"thread-face {tid}: ok")
        for args in (("npcs",), ("index",)):
            rd = run_script("render_dm.py", campaign, *args)
            tail = (rd.stdout or rd.stderr).strip().splitlines()
            print(tail[-1] if tail else f"render_dm {args[0]}: ok")
    if phase == "P8" and ph["status"] == "merged":
        # the primer phase's real output is the player's file set; the loop renders it here, not the conductor by hand
        for verb, extra in (("facts", ()), ("news", ("--day", "0")), ("primer", ())):
            rp = run_script("render_player.py", campaign, verb, *extra)
            print((rp.stdout or rp.stderr).strip().splitlines()[-1] if (rp.stdout or rp.stderr).strip() else f"render_player {verb}: ok")
            if rp.returncode != 0:
                print(f"designer: render_player {verb} failed (exit {rp.returncode}); the P8 card cannot be approved until it passes", file=sys.stderr)
                ph["status"] = "partial"
                # dry-3: `check` turned partial back to validated and the gate read no render result, so P8 was
                # approved with no primer and no DM files; the failure is now a fact the gate reads
                ph["render"] = {"failed": verb, "at": now_iso()}
                dm.save(campaign, data, f"designer.py phase {phase} merge")
                break
        else:
            if ph.pop("render", None):
                dm.save(campaign, data, f"designer.py phase {phase} merge")
            # the DM's generated files and the map's derived files (slice 1d): world, npcs, index, report, a lean state.md
            # when none exists, travel-times.md and the encounter tables
            for script, args in (("render_dm.py", ("all",)), ("map_travel.py", ("travel-times",)), ("map_travel.py", ("encounters",))):
                rd = run_script(script, campaign, *args)
                tail = (rd.stdout or rd.stderr).strip().splitlines()
                print(tail[-1] if tail else f"{script} {' '.join(args)}: ok")
    if refused:
        print(f"designer: {phase} {len(refused)} unit(s) refused and marked failed — the next `phase {phase} begin --json` "
              f"lists them with the reason: {', '.join(sorted(refused))}", file=sys.stderr)
    print(f"designer: {phase} {data['phases'][phase]['status']}")
    return 1 if (refused or seed.returncode != 0) else 0


def phase_drop(campaign: str, phase: str, entity_id: str, reason: str) -> int:
    """Drop a roster item that never reached the registry (a failed batch or document); registry entities go through design_revise."""
    data = dm.load(campaign)
    ph = data["phases"][phase]
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    if entity_id in canonical:
        print(f"designer: {entity_id} is in the registry; remove it with design_revise.py round --scope entity --action remove",
              file=sys.stderr)
        return 1
    if entity_id not in (ph.get("roster") or []):
        print(f"designer: {entity_id} is not on {phase}'s roster", file=sys.stderr)
        return 1
    ph["roster"] = [e for e in ph["roster"] if e != entity_id]
    ph.setdefault("dropped", {})[entity_id] = {"reason": reason, "at": now_iso()}
    data["entities"].pop(entity_id, None)
    dm.save(campaign, data, f"designer.py phase {phase} drop {entity_id}")
    print(f"designer: {phase} dropped {entity_id} ({reason}); roster {len(ph['roster'])}")
    return 0


def written_by_skeleton(frag: dict, sk: dict, eid: str) -> bool:
    """A merged fragment the skeleton produced (its agent label), not one its entity's own writer produced earlier."""
    agent = str(frag.get("agent") or "")
    if ".skeleton." in agent or (sk.get("agent") and agent == sk.get("agent")):
        return True
    listed = {Path(str(p)).stem for p in sk.get("fragments") or []}
    return not agent and eid in listed


def absorb_skeleton(campaign: str, phase: str) -> bool:
    """A skeleton agent's skeleton.json (roster, assignments, reads) becomes the phase's plan; the file moves to merged/."""
    staging = design_dir(campaign) / "_staging" / phase
    src = staging / "skeleton.json"
    if not src.is_file():
        return False
    sk = read_json(src) or {}
    data = dm.load(campaign)
    ph = data["phases"][phase]
    roster = [x for x in (sk.get("roster") or []) if isinstance(x, str)]
    ph["roster"] = roster
    ph["assignments"] = {k: v for k, v in (sk.get("assignments") or {}).items() if isinstance(v, str)}
    ph["reads"] = {k: list(v) for k, v in (sk.get("reads") or {}).items() if isinstance(v, list)}
    ph["skeleton"] = {"status": "merged", "agent": sk.get("agent") or (ph.get("skeleton") or {}).get("agent")}
    for eid in roster:
        row = data["entities"].setdefault(eid, {"phase": phase, "status": "pending", "attempt": 0, "critique_loops": 0,
                                                "last_error": None, "file": None, "stage_file": None, "agent": None})
        # root-cause analysis 1, RC-02: a roster id whose fragment the skeleton itself merged in this phase is owed to
        # its own writer, whatever status the skeleton wrote (dry-2 P6: two P1 stubs filled by the skeleton counted as
        # merged and no site writer ran); reconcile keeps it pending until a different fragment replaces this one
        own = staging / "merged" / f"{eid}.json"
        if own.is_file() and written_by_skeleton(read_json(own) or {}, sk, eid):
            row["writer_owed"] = {"phase": phase, "sha256": sha256_file(own)}
    dm.save(campaign, data, f"designer.py phase {phase} merge (skeleton)")
    merged = staging / "merged"
    merged.mkdir(exist_ok=True)
    src.replace(merged / "skeleton.json")
    print(f"designer: {phase} skeleton absorbed - roster {len(roster)}, assignments {len(ph['assignments'])}")
    return True


def summarise_findings(findings: list, full: bool = False) -> list[str]:
    """Grouped by module and code with counts and up to four examples; `full` lists every line (tuning birth 1: the
    conductor saw 40 truncated lines without entity or file, and could not say what failed)."""
    if full:
        out = []
        for f in findings:
            msg = str(f.get("message") or "")
            where = "" if ("dm-only" in msg or not msg) else f"  {msg[:110]}"
            out.append(f"  {f.get('severity', '?'):<8} {f.get('module', ''):<9} {f.get('entity', '') or '-':<30} {f.get('code', '')}{where}")
        return out
    groups: dict = {}
    for f in findings:
        key = (f.get("severity", "?"), f.get("module", ""), f.get("code", ""))
        msg = str(f.get("message") or "")
        example = f.get("entity") or ("" if "dm-only" in msg else msg[:70]) or "-"
        groups.setdefault(key, []).append(example)
    out = []
    for (sev, mod, code), examples in sorted(groups.items(), key=lambda kv: (kv[0][0] != "error", kv[0][1], -len(kv[1]))):
        shown = list(dict.fromkeys(examples))[:4]
        more = f" (+{len(examples) - len(shown)} more)" if len(examples) > len(shown) else ""
        out.append(f"  {sev:<8} {mod:<9} {code:<28} ×{len(examples):<3} {', '.join(shown)}{more}")
    return out


def phase_check(campaign: str, phase: str, full: bool = False) -> int:
    proc = run_script("design_check.py", campaign, "--phase", phase, "--redact", "--json")
    try:
        findings = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        print(proc.stdout.strip())
        print(proc.stderr.strip(), file=sys.stderr)
        return 1
    if not isinstance(findings, list):
        findings = findings.get("findings") or []
    errors = sum(1 for f in findings if f.get("severity") == "error")
    warnings = sum(1 for f in findings if f.get("severity") == "warning")
    result = {"findings": findings}
    data = dm.load(campaign)
    ph = data["phases"][phase]
    ph["validator"] = {"at": now_iso(), "errors": errors, "warnings": warnings}
    if ph["status"] in ("merged", "partial") and errors == 0:
        ph["status"] = "validated"
    dm.save(campaign, data, f"designer.py phase {phase} check")
    print(f"designer: {phase} validator — {errors} errors, {warnings} warnings" + ("" if full or not findings else " (grouped; --full for every line)"))
    import design_promises as dpr
    ruled = dpr.run_rules(campaign, phase)        # build item 12b: every script promise due by now is decided
    if ruled:
        print(f"designer: {phase} promises a script checks — {ruled['kept']} kept, {ruled['not_kept']} not kept")
    for line in summarise_findings(result.get("findings") or [], full):
        print(line)
    return 0 if errors == 0 else 1


def phase_card(campaign: str, phase: str) -> int:
    script = SCRIPTS / "design_approval.py"
    path = design_dir(campaign) / CARD_DIR / f"{phase}.card.md"
    if script.is_file():
        proc = run_script("design_approval.py", campaign, "card", "--phase", phase, "--out", str(path))
        print(proc.stdout.strip())
        if proc.returncode != 0:
            print(proc.stderr.strip(), file=sys.stderr)
            return 1
    else:
        data = dm.load(campaign)
        ph = data["phases"][phase]
        roster = ph.get("roster") or []
        lines = [f"# {phase} — phase card ({campaign})", "", f"- **Status:** {ph['status']} · **Attempt:** {ph.get('attempt')}",
                 f"- **Entities:** {len(roster)} (" + ", ".join(sorted(roster)) + ")",
                 f"- **Validator:** {ph.get('validator') or '—'}", ""]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    data = dm.load(campaign)
    ph = data["phases"][phase]
    if ph["status"] in ("validated", "critiqued", "merged"):
        ph["status"] = "awaiting_approval"
        dm.save(campaign, data, f"designer.py phase {phase} card")
    print(f"designer: {phase} card {path}")
    return 0


def record_used(campaign: str, phase: str) -> int:
    """The rows an approved phase rolled from the tables that record usage (`avoid_used`, `family_wait`,
    `row_wait`) go to used.json, so the next campaigns avoid them or let them wait (dry-3: design_compare read NOT
    DISTINCT because no birth ever wrote used.json). Only the phase's current attempt counts. A secret roll's row
    is kept as a hash, and so are its `used_keys`. The first approval stamps the birth order the waits count in.
    The hand-written fixture records nothing."""
    m = dm.load(campaign)
    if m["_meta"].get("fixture"):
        return 0
    attempt = int((m["phases"].get(phase) or {}).get("attempt") or 1)
    recs = [(r, False) for r in m.get("dice_log") or [] if r.get("phase") == phase]
    recs += [(r, True) for r in (read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("rolls", []) if r.get("phase") == phase]
    recs = [(r, sec) for r, sec in recs if int(r.get("attempt") or 1) == attempt]
    used = dd.load_used()
    mine = used["campaigns"].get(campaign) or {}
    born = used.setdefault("births", {})
    stamped = campaign not in born
    born.setdefault(campaign, {"first_approved": now_iso()})
    added = 0

    def put(key: str, entry) -> None:
        nonlocal added
        if entry not in mine.setdefault(key, []):
            mine[key].append(entry)
            used["campaigns"][campaign] = mine
            added += 1
    for r, secret in recs:
        ref, row = r.get("table"), r.get("row_id")
        if row and ref and dt.records_usage(ref):
            put(ref, dd.hashed(row) if secret else row)
        for key, value in (r.get("used_keys") or {}).items():
            for v in value if isinstance(value, list) else [value]:        # a draw of several values (the names' roots)
                put(key, dd.hashed(v) if secret else v)
    if added or stamped:
        dd.save_used(used)
    return added


def phase_report(campaign: str, phase: str) -> int:
    """The review stop's report (docs/tuning-births.md, phase by phase): what the owner and the development tab judge
    before approve, in ids, codes and counts; the conductor pastes it as printed."""
    from collections import Counter
    import design_approval as da
    m = dm.load(campaign)
    ph = m["phases"].get(phase) or {}
    roster = ph.get("roster") or []
    status = Counter(m["entities"].get(e, {}).get("status", "pending") for e in roster)
    owed = [e for e in roster if m["entities"].get(e, {}).get("writer_owed")]
    gate = da.gate(campaign, phase)
    chains, phase_v, phase_lines, wishes_v, sk_v = da.critique_chains(dict(ph, id=phase))
    recs = (ph.get("critique") or {}).get("records") or []
    entity_recs = [r for r in recs if r.get("kind") == "entity"]
    reasons = Counter(f"{f['rubric_id']}/{f.get('reason_code') or '-'}" for r in recs for f in r.get("findings") or []
                      if f.get("verdict") in ("fix", "rerun"))
    ended_fix = sorted(e for e, ch in chains.items() if ch and ch[-1].split(":")[-1] in ("fix", "rerun"))
    val = ph.get("validator") or {}
    cost = (ph.get("cost") or {}).get("totals") or {}
    fmt = lambda n: f"{int(n or 0):,}".replace(",", ".")
    lines = [f"PHASE REPORT · {campaign} · {phase} · attempt {ph.get('attempt') or 1}",
             f"- status: {ph.get('status')} · gate: " + ("open" if not gate else "closed — " + da.gate_text(gate)),
             f"- roster: {len(roster)} (" + ", ".join(f"{k} {v}" for k, v in sorted(status.items())) + (f"; owed to their writers: {', '.join(owed)}" if owed else "") + ")",
             f"- critics: entity returns {len(entity_recs)}, fix {sum(1 for r in entity_recs if r['verdict'] == 'fix')}"
             f"{', chains ending fix: ' + ', '.join(ended_fix) if ended_fix else ''} · phase {phase_v} · wishes {wishes_v}"
             f" · skeleton {' → '.join(sk_v) if sk_v else '—'}",
             "- fix reasons: " + (", ".join(f"{k} ×{v}" for k, v in reasons.most_common(8)) or "—"),
             f"- validator: {val.get('errors', '—')} errors, {val.get('warnings', '—')} warnings",
             "- band: " + (" · ".join(da.band_lines_of(campaign, phase)) or "—")]
    pool = None
    if phase not in ("P0", "P1"):
        import design_names as dn
        pool = dn.load_pool(campaign)
    if pool:
        lines.append("- names: " + " · ".join(f"{lid} {sum(1 for e in L['person'] + L['god'] if e.get('used_by'))} used / "
                                               f"{sum(1 for e in L['person'] + L['god'] if not e.get('used_by'))} unused"
                                               for lid, L in pool["languages"].items()))
    import design_promises as dpr
    promised = dpr.report_line(campaign, phase)
    if promised:
        lines.append(promised)
    lines.append(f"- cost: " + (f"{cost.get('agents', 0)} agents, {fmt(cost.get('requests'))} requests, output {fmt(cost.get('output'))}, "
                                f"cache read {fmt(cost.get('cache_read'))}" if cost else "no run recorded (merge --run-dir)")
                 + f" · Workflow context {fmt((ph.get('tokens') or {}).get('out'))} · wall {round(int(ph.get('wall_s') or 0) / 60)} min")
    look = [f"phase critic: {x}" for x in phase_lines[:4]] + [f"chain ended fix: {e}" for e in ended_fix[:4]]
    minor = da.minor_orphans(campaign, phase) if phase in dm.PHASES and phase != "P0" else {}
    if minor:
        look.append("unwritten minor stubs: " + ", ".join(f"{k} ×{v}" for k, v in sorted(minor.items())))
    lines.append("- look at: " + ("; ".join(look) if look else "—"))
    lines.append(f"- card: design/{CARD_DIR}/{phase}.card.md")
    print("\n".join(lines))
    return 0


def approve_phase(campaign: str, phase: str, card: str | None, onay: bool, round_text: str | None = None,
                  scope: str | None = None, force: bool = False, reason: str | None = None) -> int:
    m = dm.load(campaign)
    if round_text:
        rc = dm.approve(campaign, argparse.Namespace(phase=phase, card=None, commit=None, round=round_text,
                                                    scope=scope or "fact", affected=None))
        return rc
    if not (auto_approve(m) or onay):
        print("designer: a real birth is approved only with the player's explicit `onay` (pass --onay after they typed it)",
              file=sys.stderr)
        return 1
    # root-cause analysis 1, RC-01: approve read no quality signal; the gate reads what the card computes, in every mode
    import design_approval as da
    closed = da.gate(campaign, phase)
    if closed and not force:
        print(f"designer: {phase} gate closed — {da.gate_text(closed)}. Fix the cause, or approve --force --reason TEXT "
              "(a tuning birth never forces: it stops and reports)", file=sys.stderr)
        return 1
    if card is None:
        card = str(design_dir(campaign) / CARD_DIR / f"{phase}.card.md")
        if not Path(card).is_file():
            rc = phase_card(campaign, phase)
            if rc != 0:
                return rc
    sha = design_commit(campaign, f"{phase} approved")
    rc = dm.approve(campaign, argparse.Namespace(phase=phase, card=card, commit=sha, round=None, scope=None, affected=None,
                                                force=force))
    if rc == 0:
        snapshot_stores(campaign, phase)
        record_used(campaign, phase)
    if rc == 0 and closed:
        data = dm.load(campaign)
        data["phases"][phase]["approval"]["forced"] = {"gate": [{"code": i["code"], "ids": i["ids"]} for i in closed],
                                                        "reason": reason or "", "at": now_iso()}
        dm.save(campaign, data, f"designer.py phase {phase} approve --force")
    if rc == 0:
        print(f"designer: {phase} approved ({'auto' if auto_approve(m) else 'onay'}; commit {sha or 'none'})")
        if not auto_approve(m):
            print("designer: waiting for `devam` before the next phase")
    return rc


# ── RC-14: the stores an approval froze, so a rerun has a clean way back ──────────
# design/ is the store of record (the registry, the projection, the stamp snapshot, the overlay, the map, naming, the
# prose); the campaign root's *.json are the play-time stores the seeds write (graph, factions, goals, channels ...).
# Scratch folders and the manifest itself are not store state: rerun edits the manifest, and restores only its ledger.
SNAPSHOT_SKIP = ("_staging", "_prompts", "_approval", "_revised")


def snapshot_root(campaign: str) -> Path:
    return dm_only_dir(campaign) / "_snapshots" / "approved"


def _store_ignore(ddir: Path):
    def ignore(dirpath, names):
        rel = Path(dirpath).resolve().relative_to(ddir.resolve())
        if rel == Path("."):
            return {n for n in names if n in SNAPSHOT_SKIP or n == "design.json"}
        if rel == Path("dm-only") / "_snapshots":
            return {"approved"} & set(names)
        return set()
    return ignore


def snapshot_stores(campaign: str, phase: str) -> Path:
    """The stores as they stand when `phase` is approved (root-cause analysis 1, RC-14: rerun had no rollback)."""
    root = snapshot_root(campaign)
    root.mkdir(parents=True, exist_ok=True)
    # a real birth commits design/; copies of dm-only never enter git
    (root / ".gitignore").write_text("*\n", encoding="utf-8", newline="\n")
    dest = root / phase
    if dest.exists():
        shutil.rmtree(dest)
    ddir = design_dir(campaign)
    shutil.copytree(ddir, dest / "design", ignore=_store_ignore(ddir))
    (dest / "root").mkdir(parents=True, exist_ok=True)
    for f in campaign_dir(campaign).glob("*.json"):
        shutil.copy2(f, dest / "root" / f.name)
    (dest / "seeded.json").write_text(json.dumps(dm.load(campaign).get("seeded", []), ensure_ascii=False),
                                      encoding="utf-8", newline="\n")
    return dest


def restore_stores(campaign: str, phase: str) -> tuple[str | None, list | None]:
    """Put back the stores of the latest approval before `phase`; the snapshots of `phase` and later are dropped.
    Returns (the phase restored from, its seed ledger), or (None, None) when no earlier approval left a snapshot."""
    snaps = snapshot_root(campaign)
    idx = dm.PHASES.index(phase)
    source = next((p for p in reversed(dm.PHASES[:idx]) if (snaps / p / "design").is_dir()), None)
    for p in dm.PHASES[idx:]:
        if (snaps / p).exists():
            shutil.rmtree(snaps / p)
    if source is None:
        return None, None
    src = snaps / source
    ddir = design_dir(campaign)
    for child in list(ddir.iterdir()):
        if child.name in SNAPSHOT_SKIP or child.name == "design.json":
            continue
        if child.name == "dm-only":
            for sub in list(child.iterdir()):
                if sub.name == "_snapshots":
                    for s2 in list(sub.iterdir()):
                        if s2.name != "approved":
                            shutil.rmtree(s2) if s2.is_dir() else s2.unlink()
                    continue
                shutil.rmtree(sub) if sub.is_dir() else sub.unlink()
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    shutil.copytree(src / "design", ddir, dirs_exist_ok=True)
    root = campaign_dir(campaign)
    kept = {f.name for f in (src / "root").glob("*.json")}
    for f in root.glob("*.json"):
        if f.name not in kept:
            f.unlink()
    for f in (src / "root").glob("*.json"):
        shutil.copy2(f, root / f.name)
    return source, json.loads((src / "seeded.json").read_text(encoding="utf-8"))


def phase_rerun(campaign: str, phase: str, reason: str, reseed: bool, direction: str | None = None) -> int:
    source, seeded = restore_stores(campaign, phase)
    data = dm.load(campaign)
    if source:
        data["seeded"] = seeded
        print(f"designer: {phase} rerun restored the stores of {source}'s approval")
    else:
        print(f"designer: no approval snapshot before {phase}; the registry and the stores keep this phase's rows "
              "(births approved before RC-14 have none)", file=sys.stderr)
    ph = data["phases"][phase]
    ph["attempt"] = int(ph.get("attempt") or 1) + 1
    ph["status"] = "pending"
    ph["skeleton"] = {"status": "pending", "agent": None}
    # dry-3: the conductor's rerun reason ("STOP P7 attempt 1: …; fixed in 9cb4002") reached every writer as a creative
    # direction and the player's card; a reason is a record, a direction is the owner's correction sentence
    ph.setdefault("reruns", []).append({"attempt": ph["attempt"], "reason": reason, "at": now_iso()})
    if direction:
        ph.setdefault("directions", []).append(direction)
    if reseed:
        data["seed"]["master"] = dm.new_seed(campaign)
        data["seed"]["reseeded_at"] = now_iso()
    for eid in ph.get("roster") or []:
        data["entities"].pop(eid, None)
    ph["roster"] = []
    import design_promises as dpr
    dpr.reopen(campaign, phase, manifest=data)    # what this phase judged is open again; P1's preroll rebuilds the ledger
    dm.save(campaign, data, f"designer.py phase {phase} rerun")
    if phase != dm.PHASES[-1]:
        dm.stale(campaign, argparse.Namespace(from_phase=phase, reason=f"{phase} rerun: {reason}"))
    staging = design_dir(campaign) / "_staging" / phase
    if staging.is_dir():
        k = 1
        while (staging.parent / f"{phase}.attempt-{k}").exists():
            k += 1
        staging.rename(staging.parent / f"{phase}.attempt-{k}")
    print(f"designer: {phase} reset to attempt {ph['attempt']}{' with a new seed' if reseed else ''}; preroll it again")
    return 0


# ── the owner's hand on the promise ledger (build item 12b) ────────────────────

def promise_cmd(campaign: str, a) -> int:
    """`promise waive <id> "<one sentence>"`: the owner accepts a not-kept promise as it stands (outside `_test-*` it
    asks for `--onay`; no prompt or workflow calls it). `promise list`: the public ledger; with `--dm-only` the secret
    one after it, for the development tab."""
    import design_promises as dpr
    if a.step == "list":
        for line in dpr.listing(campaign, a.phase, a.status, False):
            print(line)
        if a.dm_only:
            # the secret ledger is the development tab's, once the birth is disarmed: while the read guard is armed
            # (a birth, a detail run, a playtest) the conductor's shell would print it
            armed = read_json(marker_path()) or {}
            if armed.get("mode") in ("birth", "detail", "playtest"):
                print(f"designer: promise list --dm-only is refused while the read guard is armed ({armed.get('mode')}); "
                      "disarm first", file=sys.stderr)
                return 1
            print("— secret (dm-only) —")
            for line in dpr.listing(campaign, a.phase, a.status, True):
                print(line)
        return 0
    if not (a.id and a.sentence):
        print("designer: promise waive needs the id and the owner's one sentence", file=sys.stderr)
        return 2
    if not (campaign.startswith("_test-") or a.onay):
        print("designer: a waiver is the owner's own decision (pass --onay after they gave it)", file=sys.stderr)
        return 1
    try:
        p = dpr.waive(campaign, a.id, a.sentence)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"designer: promise {p['id']} waived (due {p['due']}); recorded in the ledger and the revision log")
    return 0


# ── status / abandon / commit ───────────────────────────────────────────────

def status(campaign: str, as_json: bool) -> int:
    m = dm.load(campaign)
    marker = read_json(marker_path()) or None
    out = {"campaign": campaign, "mode": m["_meta"].get("mode"), "auto_approve": auto_approve(m),
           "armed": bool(marker and marker.get("campaign") == campaign), "marker_mode": (marker or {}).get("mode"),
           "seed": m["seed"]["master"], "dials": m["dials"],
           "phases": {p: {"status": v["status"], "attempt": v.get("attempt"), "roster": len(v.get("roster") or [])}
                      for p, v in m["phases"].items()},
           "public_rolls": len(m["dice_log"]), "secret_rolls": m["dice_log_secret"]["count"],
           "tables": len(dt.list_tables())}
    if as_json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    print(f"designer: {campaign} — mode {out['mode']}, auto_approve {out['auto_approve']}, guard {'armed' if out['armed'] else 'unarmed'}, seed {out['seed']}")
    for p, v in out["phases"].items():
        print(f"  {p}  {v['status']:<18} attempt {v['attempt'] or 0}  roster {v['roster']}")
        for eid in m["phases"][p].get("roster") or []:
            row = m["entities"].get(eid, {})
            if row.get("status") == "failed":
                print(f"      failed {eid}: {(row.get('last_error') or '?')[:160]}")
        for eid, info in (m["phases"][p].get("dropped") or {}).items():
            print(f"      dropped {eid}: {info.get('reason')}")
    print(f"  rolls: {out['public_rolls']} public, {out['secret_rolls']} secret · tables {out['tables']}")
    return 0


def abandon(campaign: str, reason: str) -> int:
    data = dm.load(campaign)
    for ph in data["phases"].values():
        if ph["status"] != "approved":
            ph["status"] = "failed"
    data["_meta"]["abandoned"] = {"at": now_iso(), "reason": reason}
    data["_meta"]["mode"] = "abandoned"
    dm.save(campaign, data, "designer.py abandon")
    used = dd.load_used()
    dropped = len(used.get("campaigns", {}).pop(campaign, {}) or {})
    (used.get("births") or {}).pop(campaign, None)
    dd.save_used(used)
    retired = 0
    try:
        import name_registry as nr
        for e in list(nr.list_entries(campaign) or []):
            if nr.retire(e.get("name", ""), campaign):
                retired += 1
    except Exception:
        pass
    marker = read_json(marker_path()) or {}
    if marker.get("campaign") == campaign:
        disarm()
    print(f"designer: {campaign} abandoned — {dropped} used.json tables dropped, {retired} names retired, guard disarmed")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the conductor's CLI")
    ap.add_argument("-c", "--campaign", metavar="NAME")
    sub = ap.add_subparsers(dest="verb", required=True)

    n = sub.add_parser("new")
    n.add_argument("name")
    for dial in ("scale", "tone", "magic", "era", "danger"):
        n.add_argument(f"--{dial}", default="?")
    n.add_argument("--party-size", type=int, required=True)
    n.add_argument("--start-level", type=int, default=1)
    n.add_argument("--content-mix", default="?")
    n.add_argument("--must", action="append")
    n.add_argument("--must-not", action="append")
    n.add_argument("--lang", default="tr")
    n.add_argument("--seed")
    n.add_argument("--concurrency", type=int, default=8)
    n.add_argument("--economy", action="store_true")
    n.add_argument("--fixture", action="store_true")
    n.add_argument("--ask-approval", action="store_true", help="a test birth that still waits for onay / devam")
    n.add_argument("--session-id")

    ar = sub.add_parser("arm")
    ar.add_argument("--mode", choices=("birth", "detail", "playtest"), required=True)
    ar.add_argument("--session-id")
    sub.add_parser("disarm")

    pr = sub.add_parser("preroll")
    pr.add_argument("--phase", required=True)
    pr.add_argument("--attempt", type=int)

    ph = sub.add_parser("phase")
    ph.add_argument("phase")
    ph.add_argument("step", choices=("begin", "merge", "check", "card", "report", "approve", "rerun", "drop"))
    ph.add_argument("--json", action="store_true")
    ph.add_argument("--day", type=int, default=0)
    ph.add_argument("--tokens", type=int, help="merge: output tokens the Workflow reported, added to the phase")
    ph.add_argument("--seconds", type=int, help="merge: wall-clock seconds the Workflow reported, added to the phase")
    ph.add_argument("--run-dir", action="append", help="merge: the Workflow result's transcript folder; records the real cost (repeatable)")
    ph.add_argument("--force", action="store_true", help="approve: pass a closed gate (with --reason, recorded)")
    ph.add_argument("--full", action="store_true", help="check: every validator line instead of the grouped summary")
    ph.add_argument("--id", help="drop: the roster item")
    ph.add_argument("--card")
    ph.add_argument("--onay", action="store_true")
    ph.add_argument("--round", help="approve: record a correction round instead of approving")
    ph.add_argument("--scope", choices=("fact", "entity", "phase", "direction"))
    ph.add_argument("--reason")
    ph.add_argument("--direction", help="rerun: an owner's correction the writers receive (the reason is only recorded)")
    ph.add_argument("--reseed", action="store_true")
    ph.add_argument("--session-id")

    pm = sub.add_parser("promise", help="the promise ledger: the owner's waiver, the list")
    pm.add_argument("step", choices=("waive", "list"))
    pm.add_argument("id", nargs="?", help="waive: the promise id")
    pm.add_argument("sentence", nargs="?", help="waive: the owner's one sentence")
    pm.add_argument("--onay", action="store_true", help="waive: outside a test birth, the owner's explicit word")
    pm.add_argument("--phase")
    pm.add_argument("--status")
    pm.add_argument("--dm-only", action="store_true", help="list: the secret ledger too (the development tab; never the conductor)")
    st = sub.add_parser("status")
    st.add_argument("--json", action="store_true")
    ab = sub.add_parser("abandon")
    ab.add_argument("--reason", required=True)
    cm = sub.add_parser("commit")
    cm.add_argument("--message", required=True)
    play_pack.add_subparsers(sub)

    a = ap.parse_args(argv)
    if a.verb == "new":
        return new(a)
    if not a.campaign:
        print("designer: -c CAMP is required", file=sys.stderr)
        return 2
    c = a.campaign
    if a.verb == "arm":
        arm(c, a.mode, a.session_id)
        print(f"designer: guard armed for {c} ({a.mode})")
        return 0
    if a.verb == "disarm":
        print("designer: guard disarmed" if disarm() else "designer: guard was not armed")
        return 0
    if a.verb == "preroll":
        return preroll(c, a.phase, a.attempt)
    if a.verb == "phase":
        if a.phase not in dm.PHASES:
            print(f"designer: unknown phase {a.phase}", file=sys.stderr)
            return 2
        if a.step == "begin":
            return phase_begin(c, a.phase, a.json, a.session_id)
        if a.step == "merge":
            return phase_merge(c, a.phase, a.day, a.tokens, a.seconds, a.run_dir)
        if a.step == "drop":
            if not (a.id and a.reason):
                print("designer: drop needs --id and --reason", file=sys.stderr)
                return 2
            return phase_drop(c, a.phase, a.id, a.reason)
        if a.step == "check":
            return phase_check(c, a.phase, a.full)
        if a.step == "card":
            return phase_card(c, a.phase)
        if a.step == "report":
            return phase_report(c, a.phase)
        if a.step == "approve":
            return approve_phase(c, a.phase, a.card, a.onay, a.round, a.scope, a.force, a.reason)
        if a.step == "rerun":
            if not a.reason:
                print("designer: rerun needs --reason", file=sys.stderr)
                return 2
            return phase_rerun(c, a.phase, a.reason, a.reseed, a.direction)
    if a.verb == "promise":
        return promise_cmd(c, a)
    if a.verb == "status":
        return status(c, a.json)
    if a.verb == "abandon":
        return abandon(c, a.reason)
    if a.verb == "commit":
        sha = design_commit(c, a.message)
        print(f"designer: commit {sha}" if sha else "designer: nothing to commit (or the campaign is git-ignored)")
        return 0
    if a.verb in ("load-pack", "scene", "prep", "detail", "spotlight", "end-pack"):
        return play_pack.dispatch(c, a)
    return 2


if __name__ == "__main__":
    sys.exit(main())
