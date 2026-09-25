#!/usr/bin/env python3
"""
registry.py — the campaign's entity registry: canonical file, public projection,
stamp snapshot, play-time overlay.

Plan items 3, 13, 14, 19.3; errata 24.2 #1 and #2; docs/schemas/entities.md,
overlay.md, staging-fragment.md.

Files, under <campaign>/design/:
  dm-only/entities.json            canonical registry — the conductor never opens it
  entities.json                    public projection: drop secret entities, drop dm_only
  dm-only/_snapshots/stamps.json   birth value of every stamped field (public ∪ dm_only.stamped_fields)
  overlay.json                     play-time truth: status, seen_in_play, alive, location, ruler, control
  _staging/<phase>/<id>.json       fragments written by agents; `merge` moves them to merged/

CLI:
  registry.py -c CAMP merge --phase P5 [--revise LOG_ID] [--day N]
  registry.py -c CAMP project                       regenerate projection + snapshot from canonical
  registry.py -c CAMP export --public [--out FILE]  print the projection (the only form the conductor sees)
  registry.py -c CAMP show ID [--dm]                one entity (dm_only shown only with --dm)
  registry.py -c CAMP list [--type T] [--secrecy S]
  registry.py -c CAMP play-set ID FIELD VALUE --day N --reason TEXT [--news NEWS_ID]
  registry.py -c CAMP add --type T --name NAME --summary TEXT [--slug S] [--file F] [--secrecy S]
  registry.py -c CAMP check-stamps                  canonical stamps vs snapshot; exit 1 on drift

`merge` is the single writer of the canonical file during birth and `detail`
(design_revise.py is the other sanctioned writer of stamped fields). It refuses
a change to any stamped field unless --revise carries a revision-log id, and it
writes nothing at all when any fragment is bad: disk is truth, and a half-merged
phase is worse than a failed one.

Exit codes: 0 ok · 1 refused (stamp drift, bad fragment, unknown id) · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_io import (ENTITY_TYPES, OVERLAY_FIELDS, SECRECY, campaign_dir, design_dir,  # noqa: E402
                       dm_only_dir, id_type, load_overlay, now_iso, overlay_set, read_json,
                       save_overlay, slug, stamp_meta, write_json_atomic)

STATUS_TYPES = ("site", "settlement")   # entities that carry an overlay `status`


# ── files ─────────────────────────────────────────────────────────────────────

def canonical_path(campaign: str) -> Path:
    return dm_only_dir(campaign) / "entities.json"


def projection_path(campaign: str) -> Path:
    return design_dir(campaign) / "entities.json"


def snapshot_path(campaign: str) -> Path:
    return dm_only_dir(campaign) / "_snapshots" / "stamps.json"


def load_canonical(campaign: str) -> dict:
    data = read_json(canonical_path(campaign))
    if data is None:
        data = {"_meta": {"schema_version": 1, "campaign": campaign}, "entities": {}}
    data.setdefault("entities", {})
    return data


def load_snapshot(campaign: str) -> dict:
    data = read_json(snapshot_path(campaign))
    if data is None:
        data = {"_meta": {"schema_version": 1, "campaign": campaign, "revisions": []}, "stamps": {}}
    data.setdefault("stamps", {})
    data["_meta"].setdefault("revisions", [])
    return data


# ── the two projection rules, the stamp union ────────────────────────────────

def projection_of(canonical: dict) -> dict:
    """Drop every secret entity, then drop the dm_only object of every remaining one."""
    return {eid: {k: v for k, v in ent.items() if k != "dm_only"}
            for eid, ent in canonical["entities"].items() if ent.get("secrecy") != "secret"}


def stamps_of(entity: dict) -> dict:
    """Public stamps plus the secret ones `dm_only.stamped_fields` names."""
    dm = entity.get("dm_only") or {}
    secret = {k: dm[k] for k in dm.get("stamped_fields", []) if k in dm}
    return {**entity.get("stamped", {}), **secret}


def counts_of(entities: dict) -> dict:
    counts: dict = {}
    for ent in entities.values():
        counts[ent["type"]] = counts.get(ent["type"], 0) + 1
    return counts


def write_all(campaign: str, canonical: dict, snapshot: dict, written_by: str) -> None:
    """Canonical, snapshot and projection, in that order, each atomically."""
    stamp_meta(canonical, campaign, written_by,
               stamp_snapshot="design/dm-only/_snapshots/stamps.json",
               projection="design/entities.json",
               counts=counts_of(canonical["entities"]))
    write_json_atomic(canonical_path(campaign), canonical)

    stamp_meta(snapshot, campaign, f"{written_by} (stamp snapshot)")
    write_json_atomic(snapshot_path(campaign), snapshot)

    public = projection_of(canonical)
    meta = {k: v for k, v in canonical["_meta"].items() if k not in ("stamp_snapshot", "projection")}
    proj = {"_meta": meta, "entities": public}
    stamp_meta(proj, campaign, f"{written_by} (projection)",
               projection_of="design/dm-only/entities.json", counts=counts_of(public))
    write_json_atomic(projection_path(campaign), proj)


# ── validation of one registry row ───────────────────────────────────────────

def row_errors(eid: str, row: dict) -> list[str]:
    errs: list[str] = []
    if row.get("id") != eid:
        errs.append(f"{eid}: registry.id is {row.get('id')!r}")
    if row.get("type") not in ENTITY_TYPES:
        errs.append(f"{eid}: unknown type {row.get('type')!r}")
    elif id_type(eid) != row["type"]:
        errs.append(f"{eid}: id prefix does not match type {row['type']!r}")
    if row.get("secrecy") not in SECRECY:
        errs.append(f"{eid}: secrecy must be one of {SECRECY}")
    if not isinstance(row.get("stamped"), dict):
        errs.append(f"{eid}: stamped must be an object")
    if not row.get("name"):
        errs.append(f"{eid}: name missing")
    if row.get("secrecy") == "secret" and row.get("file") and not str(row["file"]).startswith("design/dm-only/"):
        errs.append(f"{eid}: a secret entity's file must live under design/dm-only/")
    dm = row.get("dm_only")
    if dm is not None:
        if not isinstance(dm, dict):
            errs.append(f"{eid}: dm_only must be an object")
        else:
            for k in dm.get("stamped_fields", []):
                if k not in dm:
                    errs.append(f"{eid}: dm_only.stamped_fields names {k!r}, which dm_only lacks")
    for secret_key in ("secret_tr", "truth_tr"):
        if secret_key in (row.get("stamped") or {}):
            errs.append(f"{eid}: {secret_key} sits in the public stamps; move it under dm_only")
    return errs


# ── merge ─────────────────────────────────────────────────────────────────────

NON_FRAGMENTS = ("skeleton.json",)
NON_FRAGMENT_SUFFIXES = (".facts.json", ".critique.json", ".prompt.json")


def is_fragment(path: Path) -> bool:
    """A staging JSON that is a commit record; the skeleton's map, facts and critique files are not."""
    return path.name not in NON_FRAGMENTS and not path.name.endswith(NON_FRAGMENT_SUFFIXES)


def merge(campaign: str, phase: str, revise: str | None = None, day: int = 0) -> int:
    staging = design_dir(campaign) / "_staging" / phase
    if not staging.is_dir():
        print(f"registry: no staging folder {staging}", file=sys.stderr)
        return 1
    fragments = sorted(p for p in staging.glob("*.json") if is_fragment(p))
    if not fragments:
        print(f"registry: nothing to merge in {staging}")
        return 0

    canonical = load_canonical(campaign)
    snapshot = load_snapshot(campaign)
    overlay = load_overlay(campaign)
    root = campaign_dir(campaign)

    errors: list[str] = []
    warnings: list[str] = []
    plan: list[tuple[Path, dict]] = []
    for frag_path in fragments:
        try:
            frag = json.loads(frag_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{frag_path.name}: not valid JSON ({e})")
            continue
        eid = frag.get("id")
        row = frag.get("registry")
        if not eid or not isinstance(row, dict):
            errors.append(f"{frag_path.name}: fragment needs `id` and a `registry` object")
            continue
        errors.extend(row_errors(eid, row))
        if frag.get("phase") not in (None, phase):
            errors.append(f"{eid}: fragment says phase {frag.get('phase')}, merging {phase}")
        for key in ("prose", "dm_only_prose"):
            info = frag.get(key)
            if info:
                f = root / info.get("file", "")
                if not f.is_file():
                    errors.append(f"{eid}: {key} file missing: {info.get('file')}")
                elif info.get("bytes") not in (None, f.stat().st_size):
                    # Line-ending conversion on checkout changes byte counts, so
                    # a mismatch is a warning; a missing file is the error.
                    warnings.append(f"{eid}: {key} is {f.stat().st_size} bytes, fragment says {info['bytes']}")
        if eid in snapshot["stamps"]:
            new_stamps = stamps_of(row)
            drift = {k: (snapshot["stamps"][eid].get(k), new_stamps.get(k))
                     for k in set(snapshot["stamps"][eid]) | set(new_stamps)
                     if snapshot["stamps"][eid].get(k) != new_stamps.get(k)}
            if drift and not revise:
                fields = ", ".join(sorted(drift))
                errors.append(f"{eid}: stamped field(s) changed without --revise: {fields}")
            elif drift:
                frag["_revised_fields"] = sorted(drift)
        plan.append((frag_path, frag))

    for w in warnings:
        print(f"  ! {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        print(f"registry: merge refused, {len(errors)} problem(s); nothing written", file=sys.stderr)
        return 1

    merged_dir = staging / "merged"
    merged_dir.mkdir(exist_ok=True)
    summary: list[str] = []
    for frag_path, frag in plan:
        eid, row = frag["id"], frag["registry"]
        is_new = eid not in canonical["entities"]
        canonical["entities"][eid] = row
        new_stamps = stamps_of(row)
        if is_new or eid not in snapshot["stamps"]:
            snapshot["stamps"][eid] = new_stamps
        elif frag.get("_revised_fields"):
            snapshot["_meta"]["revisions"].append(
                {"id": eid, "log_id": revise, "at": now_iso(), "fields": frag["_revised_fields"],
                 "before": {k: snapshot["stamps"][eid].get(k) for k in frag["_revised_fields"]}})
            snapshot["stamps"][eid] = new_stamps
        if row["type"] in STATUS_TYPES:
            entry = overlay["entries"].get(eid, {})
            wanted = (frag.get("overlay") or {}).get("status")
            if "status" not in entry:
                overlay_set(overlay, eid, "status", wanted or "skeleton", writer="registry.py merge",
                            day=day, birth="skeleton", reason=f"{phase} merge")
            elif wanted and wanted != entry["status"]["value"]:
                overlay_set(overlay, eid, "status", wanted, writer="registry.py merge",
                            day=day, reason=f"{phase} merge")
        summary.append(f"  {'+' if is_new else '~'} {eid}"
                       + (f"  (stamps revised: {', '.join(frag['_revised_fields'])})"
                          if frag.get("_revised_fields") else ""))

    write_all(campaign, canonical, snapshot, f"registry.py merge --phase {phase}")
    save_overlay(campaign, overlay, "registry.py merge")
    for frag_path, _ in plan:
        os.replace(frag_path, merged_dir / frag_path.name)
    print(f"registry: merged {len(plan)} fragment(s) from {phase}")
    print("\n".join(summary))
    return 0


# ── other verbs ───────────────────────────────────────────────────────────────

def project(campaign: str) -> int:
    canonical = load_canonical(campaign)
    snapshot = load_snapshot(campaign)
    errors = [e for eid, row in canonical["entities"].items() for e in row_errors(eid, row)]
    if errors:
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    for eid, row in canonical["entities"].items():
        snapshot["stamps"].setdefault(eid, stamps_of(row))
    write_all(campaign, canonical, snapshot, "registry.py project")
    print(f"registry: projection and snapshot regenerated ({len(canonical['entities'])} entities)")
    return 0


def export_public(campaign: str, out: str | None) -> int:
    data = read_json(projection_path(campaign))
    if data is None:
        print("registry: no projection yet — run `project` or `merge`", file=sys.stderr)
        return 1
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


def show(campaign: str, eid: str, dm: bool) -> int:
    source = load_canonical(campaign)["entities"] if dm else (read_json(projection_path(campaign)) or {}).get("entities", {})
    row = source.get(eid)
    if row is None:
        print(f"registry: no entity {eid}" + ("" if dm else " in the public projection"), file=sys.stderr)
        return 1
    print(json.dumps(row, indent=2, ensure_ascii=False))
    return 0


def list_entities(campaign: str, etype: str | None, secrecy: str | None) -> int:
    public = (read_json(projection_path(campaign)) or {}).get("entities", {})
    rows = [r for r in public.values()
            if (etype is None or r["type"] == etype) and (secrecy is None or r["secrecy"] == secrecy)]
    for r in sorted(rows, key=lambda r: (r["type"], r["id"])):
        print(f"  {r['id']:<28} {r['secrecy']:<12} {r['name']}")
    print(f"  {len(rows)} entities (public projection)")
    return 0


def play_set(campaign: str, eid: str, field: str, value: str, day: int, reason: str,
             news: str | None) -> int:
    canonical = load_canonical(campaign)
    ent = canonical["entities"].get(eid)
    if ent is None:
        print(f"registry: no entity {eid}", file=sys.stderr)
        return 1
    if field in ent.get("stamped", {}) or field in (ent.get("dm_only") or {}).get("stamped_fields", []):
        print(f"registry: {field} is a stamped field of {eid}; the bible is not rewritten in play",
              file=sys.stderr)
        return 1
    if field == "seen_in_play":
        value_obj: object = value.lower() in ("true", "1", "yes", "evet")
    elif value in ("null", "none", "-"):
        value_obj = None
    else:
        value_obj = value
    if OVERLAY_FIELDS.get(field) is None and field in OVERLAY_FIELDS and value_obj not in (None, "party"):
        if value_obj not in canonical["entities"]:
            print(f"registry: {field}={value!r} is not a registry id", file=sys.stderr)
            return 1
    birth = ent.get(f"{field}_at_birth")
    overlay = load_overlay(campaign)
    try:
        rec = overlay_set(overlay, eid, field, value_obj, writer="registry.py play-set", day=day,
                          birth=birth, news=news, reason=reason)
    except ValueError as e:
        print(f"registry: {e}", file=sys.stderr)
        return 1
    save_overlay(campaign, overlay, "registry.py play-set")
    marker = "" if rec["birth"] in (None, value_obj) else "  (changed since birth)"
    print(f"registry: {eid}.{field} = {value_obj!r} on day {day}{marker}")
    return 0


def add(campaign: str, etype: str, name: str, summary: str, slug_arg: str | None,
        file: str | None, secrecy: str, origin: str) -> int:
    if etype not in ENTITY_TYPES:
        print(f"registry: unknown type {etype!r}", file=sys.stderr)
        return 2
    eid = f"{etype}_{slug_arg or slug(name)}"
    canonical = load_canonical(campaign)
    if eid in canonical["entities"]:
        print(f"registry: {eid} already exists", file=sys.stderr)
        return 1
    if any(e["name"].lower() == name.lower() for e in canonical["entities"].values()):
        print(f"registry: an entity named {name!r} already exists", file=sys.stderr)
        return 1
    row = {
        "id": eid, "type": etype, "name": name, "aliases": [], "summary": summary,
        "file": file, "secrecy": secrecy, "created_phase": "play" if origin == "play" else origin,
        "origin": origin, "stamped": {}, "refs": [],
    }
    canonical["entities"][eid] = row
    snapshot = load_snapshot(campaign)
    snapshot["stamps"].setdefault(eid, {})
    write_all(campaign, canonical, snapshot, f"registry.py add --origin {origin}")
    if etype in STATUS_TYPES:
        overlay = load_overlay(campaign)
        overlay_set(overlay, eid, "status", "played-improvised" if origin == "play" else "skeleton",
                    writer="registry.py merge", day=0, birth="skeleton", reason=f"registered from {origin}")
        save_overlay(campaign, overlay, "registry.py merge")
    print(f"registry: + {eid} ({secrecy}, origin {origin})")
    return 0


def check_stamps(campaign: str) -> int:
    canonical = load_canonical(campaign)
    snapshot = load_snapshot(campaign)
    drift = 0
    for eid, row in canonical["entities"].items():
        want = snapshot["stamps"].get(eid)
        have = stamps_of(row)
        if want is None:
            print(f"  ? {eid}: no snapshot entry")
            drift += 1
        elif want != have:
            changed = sorted(k for k in set(want) | set(have) if want.get(k) != have.get(k))
            print(f"  ✗ {eid}: stamped field(s) differ from birth: {', '.join(changed)}")
            drift += 1
    print(f"registry: {len(canonical['entities'])} entities, {drift} with stamp drift")
    return 1 if drift else 0


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Entity registry: merge fragments, project, overlay")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("merge", help="merge the staging fragments of one phase")
    m.add_argument("--phase", required=True)
    m.add_argument("--revise", metavar="LOG_ID", help="allow stamped-field changes under this revision id")
    m.add_argument("--day", type=int, default=0, help="campaign day for overlay writes")

    sub.add_parser("project", help="regenerate projection and snapshot from the canonical file")

    e = sub.add_parser("export", help="print the public projection")
    e.add_argument("--public", action="store_true", required=True)
    e.add_argument("--out")

    s = sub.add_parser("show")
    s.add_argument("id")
    s.add_argument("--dm", action="store_true", help="read the canonical file (dm-only)")

    ls = sub.add_parser("list")
    ls.add_argument("--type", dest="etype")
    ls.add_argument("--secrecy")

    ps = sub.add_parser("play-set", help="write one overlay field from play")
    ps.add_argument("id")
    ps.add_argument("field")
    ps.add_argument("value")
    ps.add_argument("--day", type=int, required=True)
    ps.add_argument("--reason", required=True)
    ps.add_argument("--news")

    a = sub.add_parser("add", help="register an entity that appeared in play")
    a.add_argument("--type", dest="etype", required=True)
    a.add_argument("--name", required=True)
    a.add_argument("--summary", required=True)
    a.add_argument("--slug")
    a.add_argument("--file")
    a.add_argument("--secrecy", default="public", choices=SECRECY)
    a.add_argument("--origin", default="play", choices=("play", "detail", "birth"))

    sub.add_parser("check-stamps")

    args = p.parse_args(argv)
    if args.cmd == "merge":
        return merge(args.campaign, args.phase, args.revise, args.day)
    if args.cmd == "project":
        return project(args.campaign)
    if args.cmd == "export":
        return export_public(args.campaign, args.out)
    if args.cmd == "show":
        return show(args.campaign, args.id, args.dm)
    if args.cmd == "list":
        return list_entities(args.campaign, args.etype, args.secrecy)
    if args.cmd == "play-set":
        return play_set(args.campaign, args.id, args.field, args.value, args.day, args.reason, args.news)
    if args.cmd == "add":
        return add(args.campaign, args.etype, args.name, args.summary, args.slug, args.file,
                   args.secrecy, args.origin)
    if args.cmd == "check-stamps":
        return check_stamps(args.campaign)
    return 2


if __name__ == "__main__":
    sys.exit(main())
