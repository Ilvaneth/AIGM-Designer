#!/usr/bin/env python3
"""
design_revise.py — the birth-round revise (plan item 14.1-14.3, 19.6; slice 1c item 4).

During phase approval a correction is one sentence and revise is free: the conductor classifies
it and this script records and executes it. Four scopes:

  direction  a tonal direction: stored on the phase (`phases[PN].directions[]`, appended verbatim to
             every rerun prompt) or, with --world, on the wishes; the named entities (default: the
             phase's whole roster) are marked for a rerun
  fact       one public registry field of one entity changes; the projection and the birth snapshot
             follow (stamps move freely before birth completes); the entity and every entity whose
             refs reach it are marked for a rerun
  entity     --action remove: the entity leaves the registry, its prose is archived under
             design/_revised/, its referrers are marked for a rerun; --action replace: the entity is
             marked for a rerun with the sentence as its direction
  phase      the whole phase reruns through designer.py (attempt + 1, later phases stale), --reseed
             draws a new master seed

Every round is recorded on the phase (at most three per phase, then approve-as-is or a phase rerun)
and in the revision log. A rerun-marked entity stays pending until a fresher fragment appears
(design_manifest.py reconcile honours the `rerun` flag). Secret entities and dm-only fields are not
addressable here: that is slice 3's `revise --dm-only --role`.

CLI:
  design_revise.py -c CAMP round --phase PN --scope direction|fact|entity|phase --text SENTENCE
                   [--entity ID ...] [--field F --value V] [--action remove|replace] [--world] [--reseed] [--json]
  design_revise.py -c CAMP affected --entity ID [--json]

Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import registry  # noqa: E402
from design_io import campaign_dir, design_dir, now_iso  # noqa: E402

SCOPES = ("direction", "fact", "entity", "phase")
PROTECTED_FIELDS = ("dm_only", "secrecy", "id", "type", "created_phase", "origin", "refs", "stamped")


# ── helpers ───────────────────────────────────────────────────────────────────

def referrers(canonical: dict, eid: str) -> tuple[list[str], int]:
    """Public entities whose refs reach eid, and the count of secret ones (never their ids)."""
    public, hidden = [], 0
    for oid, row in canonical.items():
        if oid == eid or eid not in (row.get("refs") or []):
            continue
        if row.get("secrecy") == "secret":
            hidden += 1
        else:
            public.append(oid)
    return sorted(public), hidden


def mark_rerun(data: dict, eids: list[str], phase_hint: str) -> None:
    for eid in eids:
        row = data["entities"].setdefault(eid, {"phase": phase_hint, "status": "pending", "attempt": 0, "critique_loops": 0,
                                                "last_error": None, "file": None, "stage_file": None, "agent": None})
        row["status"] = "pending"
        row["attempt"] = int(row.get("attempt") or 0) + 1
        row["rerun"] = True


def parse_value(raw: str):
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


def rounds_left(data: dict, phase: str) -> bool:
    return len(data["phases"][phase]["approval"]["rounds"]) < 3


def record(campaign: str, phase: str, scope: str, text: str, affected: int) -> str:
    dm.approve(campaign, argparse.Namespace(phase=phase, card=None, commit=None, round=text, scope=scope, affected=affected))
    data = dm.load(campaign)
    entry = {"at": now_iso(), "scope": scope, "phase": phase, "reason": text, "affected": affected, "commit": None}
    data["revision_log"].append(entry)
    entry["id"] = f"rev_{len(data['revision_log']):04d}"
    dm.save(campaign, data, f"design_revise.py round --phase {phase} --scope {scope}")
    return entry["id"]


# ── scopes ────────────────────────────────────────────────────────────────────

def do_direction(campaign: str, phase: str, text: str, entities: list[str], world: bool) -> dict:
    data = dm.load(campaign)
    ph = data["phases"][phase]
    ph.setdefault("directions", []).append(text)
    if world:
        data["dials"]["wishes"].setdefault("must", []).append(text)
    roster = list(ph.get("roster") or [])
    if not roster:   # a phase without a recorded roster (a fixture, an old manifest): the phase's own public entities
        canonical = registry.load_canonical(campaign)["entities"]
        roster = sorted(eid for eid, row in canonical.items() if row.get("created_phase") == phase and row.get("secrecy") != "secret")
    rerun = entities or [e for e in roster
                         if dm.ENTITY_RANK.get(data["entities"].get(e, {}).get("status", "merged"), 0) >= dm.ENTITY_RANK["merged"]]
    mark_rerun(data, rerun, phase)
    dm.save(campaign, data, f"design_revise.py direction --phase {phase}")
    return {"affected": [], "hidden": 0, "rerun": rerun}


def do_fact(campaign: str, phase: str, text: str, eid: str, field: str, raw_value: str) -> dict | int:
    canonical = registry.load_canonical(campaign)
    snapshot = registry.load_snapshot(campaign)
    row = canonical["entities"].get(eid)
    if row is None:
        print(f"design_revise: no entity {eid}", file=sys.stderr)
        return 1
    if row.get("secrecy") == "secret":
        print("design_revise: a secret entity is addressed by role through `revise --dm-only` (slice 3), never here",
              file=sys.stderr)
        return 1
    if field in PROTECTED_FIELDS or field.startswith("secret") or field in (row.get("dm_only") or {}):
        print(f"design_revise: {field} is not a public fact a birth round may change", file=sys.stderr)
        return 1
    value = parse_value(raw_value)
    old = row.get(field)
    if field == "name" and old and old != value:
        aliases = list(row.get("aliases") or [])
        if old not in aliases:
            aliases.append(old)
        row["aliases"] = aliases
    row[field] = value
    if field in (row.get("stamped") or {}):
        row["stamped"][field] = value
    snapshot["stamps"][eid] = registry.stamps_of(row)
    registry.write_all(campaign, canonical, snapshot, "design_revise.py fact")
    affected, hidden = referrers(canonical["entities"], eid)
    data = dm.load(campaign)
    owner_phase = row.get("created_phase") if row.get("created_phase") in dm.PHASES else phase
    data["phases"][owner_phase].setdefault("directions", []).append(f"fact: {eid}.{field} = {json.dumps(value, ensure_ascii=False)} ({text})")
    mark_rerun(data, [eid] + affected, phase)
    dm.save(campaign, data, f"design_revise.py fact --phase {phase}")
    return {"affected": affected, "hidden": hidden, "rerun": [eid] + affected, "old": old, "new": value}


def do_entity(campaign: str, phase: str, text: str, eid: str, action: str) -> dict | int:
    canonical = registry.load_canonical(campaign)
    snapshot = registry.load_snapshot(campaign)
    row = canonical["entities"].get(eid)
    if row is None:
        print(f"design_revise: no entity {eid}", file=sys.stderr)
        return 1
    if row.get("secrecy") == "secret":
        print("design_revise: a secret entity is addressed by role through `revise --dm-only` (slice 3), never here",
              file=sys.stderr)
        return 1
    affected, hidden = referrers(canonical["entities"], eid)
    data = dm.load(campaign)
    if action == "remove":
        archive = design_dir(campaign) / "_revised"
        archive.mkdir(parents=True, exist_ok=True)
        root = campaign_dir(campaign)
        for rel_path in (row.get("file"), f"design/dm-only/{Path(row['file']).relative_to('design')}" if row.get("file") else None):
            if not rel_path:
                continue
            src = root / rel_path
            if src.is_file():
                dst = archive / (src.name if "dm-only" not in rel_path else f"dm-only_{src.name}")
                shutil.move(str(src), str(dst))
        del canonical["entities"][eid]
        snapshot["stamps"].pop(eid, None)
        registry.write_all(campaign, canonical, snapshot, "design_revise.py entity remove")
        for ph in data["phases"].values():
            if eid in (ph.get("roster") or []):
                ph["roster"] = [x for x in ph["roster"] if x != eid]
        data["entities"].pop(eid, None)
        data["phases"][phase].setdefault("directions", []).append(f"removed {eid} ({text})")
        mark_rerun(data, affected, phase)
        rerun = affected
    else:
        data["phases"][phase].setdefault("directions", []).append(f"replace {eid}: {text}")
        mark_rerun(data, [eid], phase)
        rerun = [eid]
    dm.save(campaign, data, f"design_revise.py entity {action} --phase {phase}")
    return {"affected": affected, "hidden": hidden, "rerun": rerun}


def do_phase(campaign: str, phase: str, text: str, reseed: bool) -> dict:
    import designer
    designer.phase_rerun(campaign, phase, text, reseed)
    return {"affected": [], "hidden": 0, "rerun": ["*"]}


def round_(campaign: str, a) -> int:
    if a.phase not in dm.PHASES:
        print(f"design_revise: unknown phase {a.phase}", file=sys.stderr)
        return 2
    if a.scope not in SCOPES:
        return 2
    data = dm.load(campaign)
    if not rounds_left(data, a.phase):
        print("design_revise: three correction rounds already spent on this phase; approve as-is or rerun the phase",
              file=sys.stderr)
        return 1
    entities = list(a.entity or [])
    if a.scope == "direction":
        result = do_direction(campaign, a.phase, a.text, entities, a.world)
    elif a.scope == "fact":
        if len(entities) != 1 or not a.field or a.value is None:
            print("design_revise: a fact round needs one --entity, --field and --value", file=sys.stderr)
            return 2
        result = do_fact(campaign, a.phase, a.text, entities[0], a.field, a.value)
    elif a.scope == "entity":
        if len(entities) != 1 or a.action not in ("remove", "replace"):
            print("design_revise: an entity round needs one --entity and --action remove|replace", file=sys.stderr)
            return 2
        result = do_entity(campaign, a.phase, a.text, entities[0], a.action)
    else:
        result = do_phase(campaign, a.phase, a.text, a.reseed)
    if isinstance(result, int):
        return result
    affected_n = len(result["affected"]) + result["hidden"] + (0 if result["rerun"] == ["*"] else len([r for r in result["rerun"] if r not in result["affected"]]))
    rev = record(campaign, a.phase, a.scope, a.text, affected_n)
    data = dm.load(campaign)
    out = {"campaign": campaign, "phase": a.phase, "scope": a.scope, "text": a.text, "entity": entities,
           "affected": result["affected"], "hidden": result["hidden"], "rerun": result["rerun"],
           "round": len(data["phases"][a.phase]["approval"]["rounds"]), "revision": rev}
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"design_revise: {a.phase} round {out['round']} ({a.scope}) recorded as {rev}; rerun "
              f"{', '.join(result['rerun']) or '—'}; affected {', '.join(result['affected']) or '—'}"
              + (f" (+{result['hidden']} hidden)" if result["hidden"] else ""))
    return 0


def affected(campaign: str, eid: str, as_json: bool) -> int:
    canonical = registry.load_canonical(campaign)
    if eid not in canonical["entities"]:
        print(f"design_revise: no entity {eid}", file=sys.stderr)
        return 1
    public, hidden = referrers(canonical["entities"], eid)
    out = {"entity": eid, "affected": public, "hidden": hidden}
    print(json.dumps(out, indent=2, ensure_ascii=False) if as_json else
          f"design_revise: {eid} is referenced by {', '.join(public) or '—'}" + (f" (+{hidden} hidden)" if hidden else ""))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="birth-round revise")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    r = sub.add_parser("round")
    r.add_argument("--phase", required=True)
    r.add_argument("--scope", required=True, choices=SCOPES)
    r.add_argument("--text", required=True)
    r.add_argument("--entity", action="append")
    r.add_argument("--field")
    r.add_argument("--value")
    r.add_argument("--action", choices=("remove", "replace"))
    r.add_argument("--world", action="store_true")
    r.add_argument("--reseed", action="store_true")
    r.add_argument("--json", action="store_true")
    af = sub.add_parser("affected")
    af.add_argument("--entity", required=True)
    af.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.verb == "round":
        return round_(a.campaign, a)
    if a.verb == "affected":
        return affected(a.campaign, a.entity, a.json)
    return 2


if __name__ == "__main__":
    sys.exit(main())
