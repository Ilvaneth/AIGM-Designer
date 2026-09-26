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

Exit codes: 0 ok · 1 at least one unit refused (the others are merged; see _staging/PN/merge.report.json) · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_io import (ENTITY_TYPES, NON_FRAGMENTS, NON_FRAGMENT_SUFFIXES, OVERLAY_FIELDS,  # noqa: E402,F401
                       SCRATCH_DIRS, SECRECY, campaign_dir, design_dir, dm_only_dir, id_type,
                       is_container, is_fragment, is_stub, load_overlay, now_iso, overlay_set,
                       parse_front_matter, read_json, save_overlay, slug, stamp_meta, write_json_atomic)

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
    """Drop every secret entity, then the dm_only object of every remaining one, then every secret id anywhere in a
    public row (refs, relations[].to, heir, public_face, key_npcs …): the canonical registry keeps the link, the
    projection never says a secret entity exists (critique analysis 2026-09-26: dm_only_relation_in_public_refs was
    a quarter of the critics' leak findings)."""
    secret = {eid for eid, ent in canonical["entities"].items() if ent.get("secrecy") == "secret"}

    def scrub(v):
        if isinstance(v, str):
            return None if v in secret else v
        if isinstance(v, list):
            out = []
            for x in v:
                if isinstance(x, str) and x in secret:
                    continue
                if isinstance(x, dict) and any(isinstance(x.get(k), str) and x.get(k) in secret for k in ("to", "id", "from", "npc")):
                    continue
                out.append(scrub(x))
            return out
        if isinstance(v, dict):
            return {k: scrub(x) for k, x in v.items() if not (isinstance(x, str) and x in secret)}
        return v

    return {eid: {k: scrub(v) for k, v in ent.items() if k != "dm_only"}
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

PROSE_TYPES = ("npc", "site", "settlement", "faction", "region", "chapter", "thread")
OPAQUE_SECRET_NPC = re.compile(r"^npc_s\d+$")
TURKISH_LETTERS = re.compile(r"[çğıöşüÇĞİÖŞÜ]")
NAME_GROUPS = {**{t: "person" for t in ("npc", "pc")},
               **{t: "place" for t in ("settlement", "site", "place", "district", "region", "polity")},
               "faction": "faction", "god": "god", "item": "item", "plane": "plane"}


def row_errors(eid: str, row: dict) -> list[str]:
    errs: list[str] = []
    if row.get("id") != eid:
        errs.append(f"{eid}: registry.id is {row.get('id')!r}")
    # the stub rule (skeleton critic: missing_status_skeleton ×6; P9 left three npc rows with no file)
    if row.get("file") is None and row.get("origin") != "play" and row.get("type") in PROSE_TYPES and row.get("status") != "pending":
        errs.append(f"{eid}: a {row.get('type')} row without a file is a stub — set `status: pending` and `owner_phase` (or write the file)")
    if row.get("secrecy") == "secret" and row.get("type") == "npc" and not OPAQUE_SECRET_NPC.match(eid):
        errs.append(f"{eid}: a secret npc's id is opaque (npc_s01-style); this id names it")
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
#
# Tuning birth 1 (2026-09-25) rewrote this: the merge is per unit, never all-or-nothing. A unit is one
# entity fragment, or one container fragment (a document or batch: `doc_`, `calculus_`, `primer_`,
# `villagebatch_`, `npcbatch_`, `seedbatch_`) whose `rows[]` are registry rows merged together. A unit
# that fails is refused alone, moved to `_staging/PN/refused/`, and named with its reasons in
# `_staging/PN/merge.report.json`; the good units are written. A stub row (`status: pending`, reserved
# by an earlier phase) has no frozen stamps: the phase that fills it sets them. Secrecy is checked
# here, at the door: a secret row's name or alias that is already public, a `## Secret` heading in a
# public file, a mirror without `secrecy: secret` / `mirror_of`, a public file without `mirror`.

SECRET_HEADING = re.compile(r"^## Secret\b", re.M)


def public_prose_files(campaign: str) -> list[Path]:
    root = design_dir(campaign)
    out = []
    for p in sorted(root.rglob("*.md")):
        parts = p.relative_to(root).parts
        if "dm-only" in parts or any(s in parts for s in SCRATCH_DIRS):
            continue
        out.append(p)
    return out


def public_words(canonical: dict, extra_rows: list[dict]) -> dict:
    """lower-cased public name/alias -> the id that owns it."""
    words: dict = {}
    for row in list(canonical["entities"].values()) + extra_rows:
        if row.get("secrecy") in ("public", "discoverable"):
            for n in [row.get("name")] + list(row.get("aliases") or []):
                if isinstance(n, str) and n.strip():
                    words.setdefault(n.strip().lower(), row.get("id"))
    return words


def naming_blacklist() -> dict:
    try:
        import design_tables as dt
        return dt.load("naming.yaml").get("blacklist") or {}
    except Exception:
        return {}


def registered_elsewhere(campaign: str) -> set:
    """Full names the project's .name_registry.json holds for other campaigns (plan items 4.6, 8.7)."""
    try:
        from paths import _root as data_root
        reg = read_json(data_root() / ".name_registry.json") or {}
    except Exception:
        return set()
    out = set()
    for entry in (reg.get("entries") or {}).values():
        if not isinstance(entry, dict) or not entry.get("name"):
            continue
        camps = set(entry.get("currently_active_in") or []) | ({entry.get("first_campaign")} - {None})
        if campaign not in camps:
            out.add(str(entry["name"]).strip().lower())
    return out


def naming_errors(eid: str, row: dict, bl: dict, registered: set) -> list[str]:
    """errata 24.2 #17 and the owner's blacklist at the door (critics: rubric_english_names 14 fails, skeleton naming 6)."""
    errs = []
    etype = row.get("type")
    name = str(row.get("name") or "").strip()
    aliases = [str(a).strip() for a in (row.get("aliases") or []) if isinstance(a, str) and a.strip()]
    if etype not in ("break", "premise") and name and TURKISH_LETTERS.search(name):
        errs.append(f"{eid}: name {name!r} carries Turkish letters; every proper noun is an English fantasy name (errata 24.2 #17); "
                    "a Turkish descriptor may be a lowercase alias")
    exact = {str(x).lower() for k in ("exact", "mythology", "llm_favourites") for x in (bl.get(k) or [])}
    exact |= {str(x).lower() for x in ((bl.get("owner_banned") or {}).get("exact") or [])}
    stems = [str(x).lower() for x in ((bl.get("owner_banned") or {}).get("stems") or [])]
    subs = [str(x).lower() for x in (bl.get("substrings") or [])]
    tr_names = {str(x).lower() for x in (bl.get("turkish_as_name") or [])}
    for n in [name] + aliases:
        if not n:
            continue
        low = n.lower()
        words = re.split(r"[\s'’-]+", low)
        first = words[0] if words else low
        if low in exact or first in exact:
            errs.append(f"{eid}: {n!r} is on naming.yaml's blacklist (mythology, the owner's banned names or the model's favourites)")
        if any(stem in w for stem in stems for w in words):
            errs.append(f"{eid}: {n!r} carries a banned stem ({', '.join(stems)})")
        if any(s in low for s in subs):
            errs.append(f"{eid}: {n!r} carries a blacklisted substring")
        if n[:1].isupper() and (low in tr_names or first in tr_names):
            errs.append(f"{eid}: {n!r} is a Turkish common noun used as a proper name; name it in the campaign's naming language")
        if registered and (low in registered) and etype in ("npc", "pc"):
            errs.append(f"{eid}: {n!r} is a name another campaign registered (.name_registry.json); new campaigns never reuse it")
    return errs


def duplicate_errors(eid: str, row: dict, canonical: dict, incoming: list[tuple[str, dict]]) -> list[str]:
    """No two persons, places, factions, gods, items or planes share a full name, and no two persons a first name."""
    group = NAME_GROUPS.get(row.get("type"))
    if not group:
        return []
    name = str(row.get("name") or "").strip().lower()
    aliases = {str(a).strip().lower() for a in (row.get("aliases") or []) if isinstance(a, str)}
    first = re.split(r"[\s'’-]+", name)[0] if name else ""
    others = list(canonical["entities"].items()) + list(incoming)
    errs = []
    seen = set()
    for oid, other in others:
        if oid == eid or oid in seen or NAME_GROUPS.get(other.get("type")) != group:
            continue
        seen.add(oid)
        oname = str(other.get("name") or "").strip().lower()
        if not oname:
            continue
        if name and (name == oname or oname in aliases):
            errs.append(f"{eid}: name {row.get('name')!r} is already {oid}'s (a {group}); every {group} has its own full name")
        elif group == "person" and first and first == re.split(r"[\s'’-]+", oname)[0]:
            errs.append(f"{eid}: first name {first!r} collides with {oid}'s; no two persons share a first name")
    return errs


def sentences_of(text: str) -> set:
    if text.startswith("---"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) == 3 else text
    return {s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if len(s.strip()) >= 40 and not s.strip().startswith(("|", "#"))}


def secret_name_errors(eid: str, row: dict, publics: dict, haystack: str) -> list[str]:
    """A secret entity may not carry a name or alias that is public anywhere: the identity link goes under dm_only."""
    errs = []
    if row.get("secrecy") != "secret":
        return errs
    for n in [row.get("name")] + list(row.get("aliases") or []):
        if not isinstance(n, str) or len(n.strip()) < 3:
            continue
        n = n.strip()
        owner = publics.get(n.lower())
        if (owner and owner != eid) or re.search(r"(?<![\w'])" + re.escape(n) + r"(?![\w])", haystack):
            errs.append(f"{eid}: secret entity's name/alias {n!r} is already public"
                        + (f" (the name of {owner})" if owner and owner != eid else " (in public prose)")
                        + "; a secret identity is a dm_only relation or secret_tr line, never a public word in name/aliases")
    return errs


def prose_errors(eid: str, frag: dict, root: Path, container: bool) -> tuple[list[str], list[str]]:
    """Existence, the three-heading split and the mirror front matter of the files a fragment names."""
    errs: list[str] = []
    warns: list[str] = []
    def info_of(key):
        # `{file, bytes, sha256}` is the shape; a bare path string is accepted (birth 2: npc_olavene wrote one);
        # anything else is refused with a reason instead of crashing the merge
        v = frag.get(key)
        if v in (None, "", {}):
            return {}, None
        if isinstance(v, str):
            return {"file": v}, None
        if isinstance(v, dict):
            return v, None
        return {}, f"{eid}: {key} must be an object {{file, bytes, sha256}} or a path string (got {type(v).__name__})"
    pub, e_pub = info_of("prose")
    mir, e_mir = info_of("dm_only_prose")
    errs += [e for e in (e_pub, e_mir) if e]
    pub_file = pub.get("file") if isinstance(pub, dict) else None
    mir_file = mir.get("file") if isinstance(mir, dict) else None
    for key, info in (("prose", pub), ("dm_only_prose", mir)):
        if not info:
            continue
        f = root / str(info.get("file", ""))
        if not f.is_file():
            errs.append(f"{eid}: {key} file missing: {info.get('file')}")
        elif info.get("bytes") not in (None, f.stat().st_size):
            warns.append(f"{eid}: {key} is {f.stat().st_size} bytes, fragment says {info['bytes']}")
    if pub_file and (root / pub_file).is_file():
        if str(pub_file).startswith("design/dm-only/"):
            errs.append(f"{eid}: prose.file is under design/dm-only/; the public file belongs outside it")
        else:
            text = (root / pub_file).read_text(encoding="utf-8", errors="replace")
            if SECRET_HEADING.search(text):
                errs.append(f"{eid}: public file {pub_file} carries a `## Secret` heading; the Secret section exists only in the mirror under design/dm-only/")
            fm = parse_front_matter(text)
            if fm.get("secrecy") not in ("public", "discoverable"):
                errs.append(f"{eid}: public file {pub_file} front matter needs secrecy: public|discoverable (has {fm.get('secrecy')!r})")
            if mir_file and fm.get("mirror") != mir_file:
                errs.append(f"{eid}: public file {pub_file} front matter must name `mirror: {mir_file}`")
            if not container and fm.get("entity") not in (None, eid):
                errs.append(f"{eid}: public file {pub_file} front matter says entity: {fm.get('entity')}")
    mirror_sentences: set = set()
    if mir_file and (root / mir_file).is_file():
        if not str(mir_file).startswith("design/dm-only/"):
            errs.append(f"{eid}: dm_only_prose.file must live under design/dm-only/")
        else:
            mtext = (root / mir_file).read_text(encoding="utf-8", errors="replace")
            fm = parse_front_matter(mtext)
            if fm.get("secrecy") != "secret":
                errs.append(f"{eid}: mirror {mir_file} front matter needs `secrecy: secret` (has {fm.get('secrecy')!r})")
            if pub_file and fm.get("mirror_of") != pub_file:
                errs.append(f"{eid}: mirror {mir_file} front matter must name `mirror_of: {pub_file}`")
            mirror_sentences = sentences_of(mtext)
    # the leak classes the critics spent most fix loops on (analysis 2026-09-26): a mirror sentence repeated in the
    # public file, a mirror sentence or a secret name in the public notes
    if mirror_sentences and pub_file and (root / pub_file).is_file():
        ptext = (root / pub_file).read_text(encoding="utf-8", errors="replace")
        shared = [s for s in mirror_sentences if s in ptext]          # contained, not only equal: a prefix hides nothing
        if shared:
            errs.append(f"{eid}: {len(shared)} sentence(s) of the mirror repeated verbatim in the public file {pub_file}; the Secret layer is written once, in the mirror")
    notes = frag.get("notes")
    if isinstance(notes, str) and notes and not notes.startswith("design/dm-only/") and (root / notes).is_file():
        ntext = (root / notes).read_text(encoding="utf-8", errors="replace")
        if mirror_sentences and any(s in ntext for s in mirror_sentences):
            errs.append(f"{eid}: the public notes file {notes} restates the mirror; notes that touch the secret layer go to design/dm-only/_staging/")
        if SECRET_HEADING.search(ntext):
            errs.append(f"{eid}: the public notes file {notes} carries a `## Secret` heading")
    return errs, warns


def stamp_check(eid: str, row: dict, canonical: dict, snapshot: dict, revise: str | None) -> tuple[list[str], list[str], list[str]]:
    """(errors, warnings, revised_fields): stamped drift on a filled row is refused; a stub's stamps are set by its filler."""
    existing = canonical["entities"].get(eid)
    if eid not in snapshot["stamps"] or is_stub(existing):
        old = snapshot["stamps"].get(eid) or {}
        new = stamps_of(row)
        changed = sorted(k for k in old if k in new and old[k] != new[k])
        return [], ([f"{eid}: stub's reserved stamp(s) {', '.join(changed)} changed by its filler"] if changed else []), []
    new_stamps = stamps_of(row)
    drift = sorted(k for k in set(snapshot["stamps"][eid]) | set(new_stamps)
                   if snapshot["stamps"][eid].get(k) != new_stamps.get(k))
    if drift and not revise:
        return [f"{eid}: stamped field(s) changed without --revise: {', '.join(drift)}"], [], []
    return [], [], drift


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
    haystack = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in public_prose_files(campaign))

    # first pass: parse every unit and collect the rows it wants to write
    units: list[dict] = []
    for frag_path in fragments:
        try:
            frag = json.loads(frag_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            units.append({"path": frag_path, "id": frag_path.stem, "container": False, "frag": {}, "rows": [],
                          "errors": [f"{frag_path.name}: not valid JSON ({e})"]})
            continue
        uid = frag.get("id") or frag_path.stem
        container = is_container(frag)
        rows: list[tuple[str, dict]] = []
        errors: list[str] = []
        if container:
            for r in frag.get("rows") or []:
                if isinstance(r, dict) and r.get("id"):
                    rows.append((r["id"], r))
                else:
                    errors.append(f"{uid}: a container row lacks `id`")
        else:
            row = frag.get("registry")
            if not frag.get("id") or not isinstance(row, dict):
                errors.append(f"{frag_path.name}: fragment needs `id` and a `registry` object "
                              "(a document or batch is a container: id doc_/calculus_/primer_/…batch_, registry null, rows[])")
            else:
                rows.append((uid, row))
        if frag.get("phase") not in (None, phase):
            errors.append(f"{uid}: fragment says phase {frag.get('phase')}, merging {phase}")
        units.append({"path": frag_path, "id": uid, "container": container, "frag": frag, "rows": rows, "errors": errors})

    incoming = [(eid, r) for u in units for eid, r in u["rows"]]
    publics = public_words(canonical, [r for _, r in incoming])
    bl = naming_blacklist()
    registered = registered_elsewhere(campaign)
    secret_names = {str(r.get("name")).strip() for r in list(canonical["entities"].values()) + [r for _, r in incoming]
                    if r.get("secrecy") == "secret" and r.get("name")}
    accepted: list[dict] = []
    refused: dict[str, list[str]] = {}
    for u in units:
        errs, warns = list(u["errors"]), []
        if u["frag"]:
            e2, w2 = prose_errors(u["id"], u["frag"], root, u["container"])
            errs += e2
            warns += w2
            notes = u["frag"].get("notes")
            if isinstance(notes, str) and notes and not notes.startswith("design/dm-only/") and (root / notes).is_file():
                ntext = (root / notes).read_text(encoding="utf-8", errors="replace")
                leaked = [n for n in secret_names if len(n) >= 3 and re.search(r"(?<![\w'])" + re.escape(n) + r"(?![\w])", ntext)]
                if leaked:
                    errs.append(f"{u['id']}: the public notes file {notes} names {len(leaked)} secret entit{'y' if len(leaked) == 1 else 'ies'}; "
                                "notes that touch the secret layer go to design/dm-only/_staging/")
        u["revised"] = {}
        for eid, row in u["rows"]:
            errs += row_errors(eid, row)
            errs += secret_name_errors(eid, row, publics, haystack)
            errs += naming_errors(eid, row, bl, registered)
            errs += duplicate_errors(eid, row, canonical, [(i, r) for i, r in incoming if i != eid])
            e3, w3, drift = stamp_check(eid, row, canonical, snapshot, revise)
            errs += e3
            warns += w3
            if drift:
                u["revised"][eid] = drift
        for w in warns:
            print(f"  ! {w}", file=sys.stderr)
        if errs:
            refused[u["id"]] = errs
            for e in errs:
                print(f"  ✗ {e}", file=sys.stderr)
        else:
            accepted.append(u)

    merged_dir = staging / "merged"
    merged_dir.mkdir(exist_ok=True)
    summary: list[str] = []
    merged_ids: list[str] = []
    for u in accepted:
        for eid, row in u["rows"]:
            is_new = eid not in canonical["entities"]
            was_stub = is_stub(canonical["entities"].get(eid))
            canonical["entities"][eid] = row
            new_stamps = stamps_of(row)
            if is_new or was_stub or eid not in snapshot["stamps"]:
                snapshot["stamps"][eid] = new_stamps
            elif u["revised"].get(eid):
                snapshot["_meta"]["revisions"].append(
                    {"id": eid, "log_id": revise, "at": now_iso(), "fields": u["revised"][eid],
                     "before": {k: snapshot["stamps"][eid].get(k) for k in u["revised"][eid]}})
                snapshot["stamps"][eid] = new_stamps
            if row["type"] in STATUS_TYPES:
                entry = overlay["entries"].get(eid, {})
                wanted = (u["frag"].get("overlay") or {}).get("status")
                if "status" not in entry:
                    overlay_set(overlay, eid, "status", wanted or "skeleton", writer="registry.py merge",
                                day=day, birth="skeleton", reason=f"{phase} merge")
                elif wanted and wanted != entry["status"]["value"]:
                    overlay_set(overlay, eid, "status", wanted, writer="registry.py merge",
                                day=day, reason=f"{phase} merge")
            merged_ids.append(eid)
            summary.append(f"  {'+' if is_new else '~'} {eid}"
                           + (f"  (stamps revised: {', '.join(u['revised'][eid])})" if u["revised"].get(eid) else "")
                           + ("  (stub filled)" if was_stub and not is_stub(row) else ""))
        if u["container"]:
            summary.append(f"  > {u['id']}  (container, {len(u['rows'])} row(s))")

    if accepted:
        write_all(campaign, canonical, snapshot, f"registry.py merge --phase {phase}")
        save_overlay(campaign, overlay, "registry.py merge")
        for u in accepted:
            os.replace(u["path"], merged_dir / u["path"].name)
    refused_dir = staging / "refused"
    for u in units:
        if u["id"] in refused and u["path"].is_file():
            refused_dir.mkdir(exist_ok=True)
            k = int((u["frag"] or {}).get("attempt") or 1)
            os.replace(u["path"], refused_dir / f"{u['path'].stem}.attempt-{k}.json")
    report = {"phase": phase, "at": now_iso(), "merged": merged_ids,
              "units": [u["id"] for u in accepted], "containers": [u["id"] for u in accepted if u["container"]],
              "refused": refused}
    write_json_atomic(staging / "merge.report.json", report)
    print(f"registry: merged {len(accepted)} unit(s) from {phase} ({len(merged_ids)} row(s))"
          + (f"; refused {len(refused)}: {', '.join(sorted(refused))}" if refused else ""))
    if summary:
        print("\n".join(summary))
    return 1 if refused else 0


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
