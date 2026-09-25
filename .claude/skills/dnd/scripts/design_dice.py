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
one row by weight; until then, or for a plain notation, --notation rolls dice.
`--avoid-used` excludes rows that earlier campaigns in this root drew, as
recorded in <root>/used.json; the exclusions are logged on the record.

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
from design_io import dm_only_dir, now_iso, read_json, stamp_meta, write_json_atomic  # noqa: E402
from design_manifest import append_roll, load as load_manifest  # noqa: E402
from design_tables import rows as table_rows  # noqa: E402
from paths import _root as data_root  # noqa: E402



def used_path() -> Path:
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


def rows_used_elsewhere(campaign: str, table: str) -> set:
    used = load_used()
    out: set = set()
    for camp, tables in used["campaigns"].items():
        if camp != campaign:
            out.update(tables.get(table, []))
    return out


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
        gone = rows_used_elsewhere(campaign, table) if avoid_used else set()
        record.update(draw(rng, rows, gone))
        excluded.extend(record.pop("excluded_rows"))
    else:
        if not notation:
            raise SystemExit(f"design_dice: no table rows for {table!r} and no --notation given")
        result = dice_mod.run(notation, silent=True, rng=rng)
        record.update({"notation": notation, "raw": result})
    append_roll(campaign, record, secret=secret)
    return record


def draw(rng: random.Random, rows: list[dict], gone: set | None = None, exclude: set | None = None) -> dict:
    """One weighted draw from `rows`, skipping ids in `gone` (used elsewhere, logged) and `exclude`
    (a caller's own constraint, not logged); the pool falls back to every row when nothing is left."""
    gone = gone or set()
    exclude = exclude or set()
    excluded_rows = sorted(r["id"] for r in rows if r["id"] in gone)
    pool = [r for r in rows if r["id"] not in gone and r["id"] not in exclude] or            [r for r in rows if r["id"] not in exclude] or rows
    weights = [float(r.get("weight", 1)) for r in pool]
    total = sum(weights)
    raw = rng.uniform(0, total)
    acc, chosen = 0.0, pool[-1]
    for r, w in zip(pool, weights):
        acc += w
        if raw <= acc:
            chosen = r
            break
    return {"notation": f"d{len(pool)}", "raw": pool.index(chosen) + 1, "row_id": chosen["id"],
            "row_label": chosen.get("label"), "excluded_rows": excluded_rows}


def show_log(campaign: str, secret: bool) -> int:
    if secret:
        log = read_json(dm_only_dir(campaign) / "dice-log.json") or {"rolls": []}
        rolls = log["rolls"]
    else:
        rolls = load_manifest(campaign)["dice_log"]
    for r in rolls:
        what = r.get("row_id") or r.get("raw")
        print(f"  {r['phase']:<3} {r['table']:<28} {r['label']:<24} {r['notation']:<8} → {what}"
              + (f"  (excluded {', '.join(r['excluded'])})" if r.get("excluded") else ""))
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
