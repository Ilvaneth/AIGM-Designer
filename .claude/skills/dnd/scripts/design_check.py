#!/usr/bin/env python3
"""
design_check.py — the structural validator of a designed campaign (no LLM).

Plan item 15.1, errata 24.2 #9 / #10, decisions 24.6 #5. Slice 1 ships the core
modules: refs, stamps, secrecy, overlay, map, sites. The rest (scale, factions,
npcs, arc, threads, budget, signatures, seeds) follow in later commits.

CLI:
  design_check.py -c CAMP                         every module
  design_check.py -c CAMP --modules refs,stamps   some modules
  design_check.py -c CAMP --fast                  refs + stamps + secrecy; reports, never fails (save-time)
  design_check.py -c CAMP --only site_sunken_pier   one entity (after `detail`)
  design_check.py -c CAMP --phase P3              accept `status: pending` rows owned by later phases
  design_check.py -c CAMP --fixture               relax scale bands (also read from _meta.fixture)
  design_check.py -c CAMP --json                  findings as JSON
  design_check.py -c CAMP --redact                accepted for the conductor; output is redacted in every mode

Output is redacted in every mode: a finding names an entity by id, a field, a
file and a code — never a name of a secret entity, never a sentence of prose.
Errors stop a phase; warnings are reported and the phase goes on.

Exit codes: 0 no errors · 1 errors (0 under --fast) · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_io import (ENTITY_TYPES, OVERLAY_FIELDS, OVERLAY_WRITERS, SCRATCH_DIRS, SECRECY, campaign_dir,  # noqa: E402
                       design_dir, dm_only_dir, front_matter, id_type, read_json, wiki_links)
from paths import _root as data_root  # noqa: E402

CORE_MODULES = ("refs", "stamps", "secrecy", "overlay", "map", "sites")
FAST_MODULES = ("refs", "stamps", "secrecy")

TELEGRAPH_DISTANCES = ("far", "near", "threshold")
ATTITUDES = ("kill", "capture", "enslave", "ignore", "negotiate", "test")
PAYOFFS = ("treasure", "lore", "ally", "plot_item", "access")
ROOM_CATEGORIES = ("combat", "trap", "special", "structural")
CONTENT_BANDS = {"combat": (40, 60), "trap": (5, 15), "special": (8, 20), "structural": (10, 25)}
MINOR_TOLERANCE = 20
MAP_ONLY_PREFIXES = ("landmark_", "waypoint_")
PUBLIC_EXTRA_FILES = ("world.md", "npcs.md", "state.md", "graph.json", "factions.json", "goals.json",
                      "common-knowledge.json", "design/news.json", "design/naming.json",
                      "design/entities.json", "design/index.md", "design/player-primer.md")

ROOM_ROW = re.compile(r"^\| (\d+) \| (.+?) \| (\w+) \| .*? \| (.+?) \| (\d+) \|$", re.M)
EXIT_ID = re.compile(r"^\s*(\d+)")


@dataclass
class Finding:
    module: str
    severity: str          # error | warning
    entity: str | None
    code: str
    message: str

    def line(self) -> str:
        mark = "✗" if self.severity == "error" else "!"
        who = f"{self.entity}: " if self.entity else ""
        return f"  {mark} [{self.module}] {who}{self.message}"


@dataclass
class Bible:
    """Everything the modules read, loaded once. Names of secret entities never leave it."""
    campaign: str
    root: Path
    canonical: dict
    projection: dict | None
    snapshot: dict | None
    overlay: dict | None
    map: dict | None
    phase: str | None = None
    fixture: bool = False
    prose: dict = field(default_factory=dict)     # Path -> text, every design/**/*.md except _staging
    fm: dict = field(default_factory=dict)        # Path -> front matter

    @property
    def entities(self) -> dict:
        return self.canonical.get("entities", {})

    def is_public_path(self, path: Path) -> bool:
        return dm_only_dir(self.campaign).resolve() not in path.resolve().parents

    def is_pending(self, ent: dict) -> bool:
        return ent.get("status") == "pending" or (ent.get("file") is None and self.phase is not None)

    def status_of(self, eid: str) -> str | None:
        entry = (self.overlay or {}).get("entries", {}).get(eid, {})
        rec = entry.get("status")
        return rec["value"] if rec else None


def load_bible(campaign: str, phase: str | None, fixture: bool) -> Bible:
    root = campaign_dir(campaign)
    canonical = read_json(dm_only_dir(campaign) / "entities.json") or {"entities": {}}
    b = Bible(
        campaign=campaign, root=root, canonical=canonical,
        projection=read_json(design_dir(campaign) / "entities.json"),
        snapshot=read_json(dm_only_dir(campaign) / "_snapshots" / "stamps.json"),
        overlay=read_json(design_dir(campaign) / "overlay.json"),
        map=read_json(design_dir(campaign) / "map.json"),
        phase=phase,
        fixture=fixture or bool(canonical.get("_meta", {}).get("fixture")),
    )
    for p in sorted(design_dir(campaign).rglob("*.md")):
        if any(s in p.parts for s in SCRATCH_DIRS):
            continue        # cards, rendered prompts, staging and revised copies are not bible prose (tuning birth 1)
        text = p.read_text(encoding="utf-8")
        b.prose[p] = text
        b.fm[p] = front_matter(p)
    return b


def relpath(b: Bible, path: Path) -> str:
    try:
        return path.resolve().relative_to(b.root.resolve()).as_posix()
    except ValueError:
        return str(path)


# ── refs ──────────────────────────────────────────────────────────────────────

def check_refs(b: Bible, only: str | None) -> list[Finding]:
    out: list[Finding] = []
    ents = b.entities
    E = lambda eid, code, msg: out.append(Finding("refs", "error", eid, code, msg))
    W = lambda eid, code, msg: out.append(Finding("refs", "warning", eid, code, msg))

    # ids, types, secrecy
    for eid, ent in ents.items():
        if only and eid != only:
            continue
        if ent.get("id") != eid:
            E(eid, "id_mismatch", "row id differs from its key")
        if ent.get("type") not in ENTITY_TYPES or id_type(eid) != ent.get("type"):
            E(eid, "bad_type", f"type {ent.get('type')!r} does not match the id prefix")
        if ent.get("secrecy") not in SECRECY:
            E(eid, "no_secrecy", "secrecy tier missing or unknown")
        for ref in ent.get("refs", []):
            if ref not in ents:
                E(eid, "dangling_ref", f"refs names {ref}, which does not exist")

    # wiki-links in prose
    for path, text in b.prose.items():
        fm = b.fm.get(path, {})
        owner = fm.get("entity")
        if only and owner != only and only not in (fm.get("covers") or []):
            continue
        for ref in wiki_links(text):
            if ref not in ents:
                E(owner if owner and owner != "none" else None, "dangling_link",
                  f"[[{ref}]] in {relpath(b, path)} does not resolve")

    # every entity's file exists and claims it
    claims: dict[str, set] = {}
    for path, fm in b.fm.items():
        r = relpath(b, path)
        for c in [fm.get("entity")] + list(fm.get("covers") or []):
            if c and c != "none":
                claims.setdefault(c, set()).add(r)
    for eid, ent in ents.items():
        if only and eid != only:
            continue
        f = ent.get("file")
        if not f:
            if b.is_pending(ent):
                continue
            E(eid, "no_file", "no prose file and not pending")
            continue
        p = b.root / f
        if not p.is_file():
            if b.is_pending(ent):
                continue
            E(eid, "file_missing", f"file {f} does not exist")
            continue
        if p.suffix == ".md" and "characters/" not in f and f not in claims.get(eid, set()):
            E(eid, "file_unclaimed", f"{f} names neither entity: {eid} nor covers: {eid}")

    # roles have holders
    for eid, ent in ents.items():
        if only and eid != only:
            continue
        t = ent.get("type")
        if t == "faction":
            for role in ("leader", "heir", "hq"):
                target = ent.get(role)
                if not target:
                    if not b.is_pending(ent):        # a P3 faction stub is filled by P4 (birth 2)
                        E(eid, "role_unfilled", f"{role} is empty")
                elif target not in ents:
                    E(eid, "role_dangling", f"{role} names {target}, which does not exist")
                elif role != "hq" and ents[target].get("type") != "npc":
                    E(eid, "role_not_npc", f"{role} {target} is not an npc")
                elif role != "hq" and alive_state(b, target) == "dead":
                    E(eid, "role_dead", f"{role} {target} is dead in the overlay")
        if t == "settlement":
            ruler = ent.get("ruler_at_birth")
            if ruler and ruler not in ents:
                E(eid, "role_dangling", f"ruler_at_birth {ruler} does not exist")
        if t == "site":
            for k in ent.get("key_npcs", []):
                if k not in ents:
                    E(eid, "role_dangling", f"key_npcs names {k}, which does not exist")
            thread = ent.get("thread")
            if thread and thread not in ents:
                E(eid, "thread_dangling", f"thread {thread} does not exist")
            elif thread and ents[thread].get("type") not in ("faction", "npc", "seed", "beat"):
                E(eid, "thread_kind", f"thread {thread} is a {ents[thread].get('type')}, not faction/npc/seed/beat")

    # name collisions
    first_names: dict[str, list] = {}
    for eid, ent in ents.items():
        if ent.get("type") in ("npc", "pc") and ent.get("name"):
            first_names.setdefault(ent["name"].split()[0].lower(), []).append(eid)
    for fn, ids in first_names.items():
        if len(ids) > 1:
            E(None, "first_name_collision", f"first name shared by {', '.join(sorted(ids))}")
    registry = read_json(data_root() / ".name_registry.json") or {}
    used = {e.get("name", "").lower(): e for e in (registry.get("entries") or {}).values()}
    for eid, ent in ents.items():
        if ent.get("type") in ("npc", "pc"):
            hit = used.get(ent.get("name", "").lower())
            if hit and b.campaign not in hit.get("currently_active_in", []):
                W(eid, "name_used_elsewhere",
                  f"name already used in campaign {hit.get('first_campaign')}")
    return out


def alive_state(b: Bible, eid: str) -> str | None:
    rec = ((b.overlay or {}).get("entries", {}).get(eid, {})).get("alive")
    return rec["value"] if rec else None


# ── stamps ────────────────────────────────────────────────────────────────────

def stamps_of(ent: dict) -> dict:
    dm = ent.get("dm_only") or {}
    return {**ent.get("stamped", {}), **{k: dm[k] for k in dm.get("stamped_fields", []) if k in dm}}


def check_stamps(b: Bible, only: str | None) -> list[Finding]:
    out: list[Finding] = []
    snap = (b.snapshot or {}).get("stamps", {})
    for eid, ent in b.entities.items():
        if only and eid != only:
            continue
        if not isinstance(ent.get("stamped"), dict):
            out.append(Finding("stamps", "error", eid, "no_stamped", "stamped object missing"))
            continue
        for k in ("secret_tr", "truth_tr"):
            if k in ent["stamped"]:
                out.append(Finding("stamps", "error", eid, "secret_in_public_stamps",
                                   f"{k} is a public stamp; it belongs under dm_only.stamped_fields"))
        have = stamps_of(ent)
        want = snap.get(eid)
        if want is None:
            if not b.is_pending(ent):
                out.append(Finding("stamps", "warning", eid, "no_snapshot", "no stamp snapshot yet"))
        elif want != have:
            changed = sorted(k for k in set(want) | set(have) if want.get(k) != have.get(k))
            out.append(Finding("stamps", "error", eid, "stamp_drift",
                               f"stamped field(s) differ from birth: {', '.join(changed)}"))
        if ent.get("type") == "site" and not b.is_pending(ent):     # a site stub reserved by P2/P3 is stamped by P6
            tier = ent.get("danger_tier")
            if not isinstance(tier, int) or not 1 <= tier <= 5:
                out.append(Finding("stamps", "error", eid, "bad_tier", "danger_tier must be an integer 1-5"))
            elif ent["stamped"].get("danger_tier") != tier:
                out.append(Finding("stamps", "error", eid, "tier_unstamped", "danger_tier is not stamped"))
            for k in ("room_count", "act"):
                if ent["stamped"].get(k) != ent.get(k):
                    out.append(Finding("stamps", "error", eid, f"{k}_unstamped", f"{k} is not stamped"))
    return out


# ── secrecy ───────────────────────────────────────────────────────────────────

def check_secrecy(b: Bible, only: str | None) -> list[Finding]:
    out: list[Finding] = []
    E = lambda eid, code, msg: out.append(Finding("secrecy", "error", eid, code, msg))
    ents = b.entities
    public_prose = {p: t for p, t in b.prose.items() if b.is_public_path(p)}

    for path, text in public_prose.items():
        if re.search(r"^## Secret\b", text, re.M):
            E(b.fm[path].get("entity"), "secret_heading_public", f"{relpath(b, path)} carries a ## Secret heading")

    # mirrors point at each other
    for path, fm in b.fm.items():
        if not b.is_public_path(path):
            if fm.get("secrecy") != "secret":
                E(fm.get("entity"), "mirror_not_secret", f"{relpath(b, path)} is under dm-only but not secrecy: secret")
            continue
        mirror = fm.get("mirror")
        if mirror:
            mp = b.root / mirror
            if not mp.is_file():
                E(fm.get("entity"), "mirror_missing", f"mirror {mirror} does not exist")
            elif b.fm.get(mp, {}).get("mirror_of") != relpath(b, path):
                E(fm.get("entity"), "mirror_backlink", f"{mirror} does not name {relpath(b, path)} as mirror_of")

    # secret entities: file under dm-only, absent from projection; projection has no dm_only
    proj = (b.projection or {}).get("entities", {})
    for eid, ent in ents.items():
        if ent.get("secrecy") == "secret":
            if ent.get("file") and not str(ent["file"]).startswith("design/dm-only/"):
                E(eid, "secret_file_public", "secret entity's file is outside design/dm-only/")
            if eid in proj:
                E(eid, "secret_in_projection", "secret entity present in the public projection")
    for eid, row in proj.items():
        if "dm_only" in row:
            E(eid, "dm_only_in_projection", "projection row carries dm_only")
        if eid not in ents:
            E(eid, "projection_orphan", "projection row has no canonical entity")

    # leak grep: secret names and secret lines in public files
    haystacks = dict((relpath(b, p), t) for p, t in public_prose.items())
    for extra in PUBLIC_EXTRA_FILES:
        p = b.root / extra
        if p.is_file():
            haystacks[extra] = p.read_text(encoding="utf-8")
    secret_names = [(eid, ent["name"]) for eid, ent in ents.items()
                    if ent.get("secrecy") == "secret" and ent.get("name")]
    secret_lines = []
    for eid, ent in ents.items():
        dm = ent.get("dm_only") or {}
        for k in ("secret_tr", "truth_tr", "happened_tr", "true_rule_tr"):
            v = dm.get(k)
            if isinstance(v, str) and len(v) > 12 and v != "yok":
                secret_lines.append((eid, k, v))
    for where, text in haystacks.items():
        for eid, name in secret_names:
            if only and eid != only:
                continue
            if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text):
                E(eid, "secret_name_leak", f"secret entity's name appears in {where}")
        for eid, k, v in secret_lines:
            if only and eid != only:
                continue
            if v in text:
                E(eid, "secret_line_leak", f"dm_only.{k} appears verbatim in {where}")

    # the big secret's three clues are placed, in act order
    for eid, ent in ents.items():
        if ent.get("type") != "premise":
            continue
        clues = (ent.get("dm_only") or {}).get("clues") or []
        if len(clues) != 3:
            E(eid, "clue_count", f"{len(clues)} clues in the trail, need 3")
        last_act = 0
        for c in clues:
            where = c.get("placed_in")
            if where not in ents:
                E(eid, "clue_unplaced", f"clue {c.get('n')} placed_in {where} does not exist")
            elif ents[where].get("type") not in ("site", "npc", "item"):
                E(eid, "clue_place_kind", f"clue {c.get('n')} sits on a {ents[where].get('type')}, not a site/npc/item")
            if isinstance(c.get("act"), int):
                if c["act"] < last_act:
                    E(eid, "clue_order", f"clue {c.get('n')} is in act {c['act']}, after act {last_act}")
                last_act = c["act"]

    # every entity has a tier (already in refs) — and every prose file names one
    for path, fm in b.fm.items():
        rp = relpath(b, path)
        if rp == "design/player-primer.md" or rp.startswith("design/player/"):
            continue        # rendered player files carry no front matter; they are still leak haystacks (birth 2, R.4)
        if fm.get("secrecy") not in SECRECY:
            E(fm.get("entity"), "file_no_secrecy", f"{rp} has no secrecy in its front matter")
    return out


# ── overlay ───────────────────────────────────────────────────────────────────

def check_overlay(b: Bible, only: str | None) -> list[Finding]:
    out: list[Finding] = []
    E = lambda eid, code, msg: out.append(Finding("overlay", "error", eid, code, msg))
    if b.overlay is None:
        out.append(Finding("overlay", "warning", None, "no_overlay", "design/overlay.json missing"))
        return out
    ents = b.entities
    for eid, fields in b.overlay.get("entries", {}).items():
        if only and eid != only:
            continue
        if eid not in ents:
            E(eid, "overlay_orphan", "overlay entry has no registry entity")
            continue
        for fname, rec in fields.items():
            if fname not in OVERLAY_FIELDS:
                E(eid, "overlay_field", f"{fname} is not an overlay field")
                continue
            if fname in stamps_of(ents[eid]):
                E(eid, "overlay_stamped", f"{fname} is stamped; the overlay may not override it")
            if not isinstance(rec, dict):
                E(eid, "overlay_bare_value", f"{fname} is a bare value, not a record")
                continue
            for key in ("value", "birth", "writer", "day"):
                if key not in rec:
                    E(eid, "overlay_record", f"{fname} record lacks {key}")
            if rec.get("writer") not in OVERLAY_WRITERS:
                E(eid, "overlay_writer", f"{fname} written by {rec.get('writer')!r}, not a sanctioned writer")
            allowed = OVERLAY_FIELDS[fname]
            if allowed is not None and rec.get("value") not in allowed:
                E(eid, "overlay_value", f"{fname}={rec.get('value')!r} is not in {allowed}")
            if allowed is None and rec.get("value") not in (None, "party") and rec.get("value") not in ents:
                E(eid, "overlay_id", f"{fname} points at {rec.get('value')!r}, not a registry id")
    for scene in b.overlay.get("pending_scenes", []):
        for key in ("id", "day", "actor", "target", "why", "status"):
            if key not in scene:
                E(scene.get("id"), "pending_scene", f"pending scene lacks {key}")
    doom = b.overlay.get("_meta", {}).get("doom_day")
    arcs = [e for e in ents.values() if e.get("type") == "arc"]
    if arcs and doom is not None and arcs[0].get("doom_day") not in (None, doom):
        E(arcs[0]["id"], "doom_mismatch", f"overlay doom_day {doom} differs from the arc's {arcs[0].get('doom_day')}")
    return out


# ── map ───────────────────────────────────────────────────────────────────────

def check_map(b: Bible, only: str | None) -> list[Finding]:
    out: list[Finding] = []
    E = lambda eid, code, msg: out.append(Finding("map", "error", eid, code, msg))
    W = lambda eid, code, msg: out.append(Finding("map", "warning", eid, code, msg))
    if b.map is None:
        E(None, "no_map", "design/map.json missing")
        return out
    ents = b.entities
    nodes = {n.get("id"): n for n in b.map.get("nodes", [])}
    regions = b.map.get("regions", {})
    for eid, ent in ents.items():
        if ent.get("type") in ("site", "settlement") and eid not in nodes and not b.is_pending(ent):
            E(eid, "node_missing", "no map node")
    for nid, n in nodes.items():
        if not nid.startswith(MAP_ONLY_PREFIXES) and nid not in ents:
            E(nid, "node_orphan", "map node has no registry entity")
        if n.get("region") not in ents:
            E(nid, "node_region", f"region {n.get('region')} does not exist")
        bbox = regions.get(n.get("region"), {}).get("bbox")
        if bbox and not (bbox[0] <= n.get("x", -1) <= bbox[2] and bbox[1] <= n.get("y", -1) <= bbox[3]):
            E(nid, "node_outside_region", "coordinates fall outside the region bbox")
    adj: dict[str, set] = {nid: set() for nid in nodes}
    for e in b.map.get("edges", []):
        a, c = e.get("from"), e.get("to")
        if a not in nodes or c not in nodes:
            E(e.get("id"), "edge_dangling", "edge endpoint is not a node")
            continue
        adj[a].add(c)
        adj[c].add(a)
        if not isinstance(e.get("days"), (int, float)) or e["days"] <= 0:
            E(e.get("id"), "edge_days", "days must be a positive number")
    if nodes:
        seen: set = set()
        todo = deque([next(iter(nodes))])
        while todo:
            cur = todo.popleft()
            if cur in seen:
                continue
            seen.add(cur)
            todo.extend(adj[cur])
        for nid in set(nodes) - seen:
            E(nid, "node_unreachable", "not connected to the rest of the map")
    # hubs: exactly one per region
    per_region: dict[str, int] = {}
    for n in nodes.values():
        if n.get("hub"):
            per_region[n.get("region")] = per_region.get(n.get("region"), 0) + 1
    for rid in regions:
        if per_region.get(rid, 0) != 1:
            E(rid, "hub_count", f"{per_region.get(rid, 0)} hub nodes, need exactly 1")
    # drawn length monotone with days inside a region (warning)
    by_region: dict[str, list] = {}
    for e in b.map.get("edges", []):
        a, c = nodes.get(e.get("from")), nodes.get(e.get("to"))
        if a and c and isinstance(e.get("days"), (int, float)):
            length = ((a["x"] - c["x"]) ** 2 + (a["y"] - c["y"]) ** 2) ** 0.5
            by_region.setdefault(e.get("region"), []).append((e["days"], length, e.get("id")))
    for rid, edges in by_region.items():
        for d1, l1, id1 in edges:
            for d2, l2, id2 in edges:
                if d1 < d2 and l1 > l2 * 1.6:
                    W(id1, "length_not_monotone", f"drawn longer than {id2} although it takes fewer days")
    return out


# ── sites ─────────────────────────────────────────────────────────────────────

def parse_rooms(text: str) -> list[dict]:
    rooms = []
    for num, name, cat, exits_cell, xp in ROOM_ROW.findall(text):
        exits = [EXIT_ID.match(part).group(1) for part in exits_cell.split(",") if EXIT_ID.match(part)]
        rooms.append({"id": num, "name": name, "category": cat, "exits": exits, "xp": int(xp),
                      "entrance": "[Entrance]" in name, "payoff": "[Payoff]" in name})
    return rooms


def min_depth(rooms: list[dict]) -> int | None:
    adj = {r["id"]: r["exits"] for r in rooms}
    payoffs = [r["id"] for r in rooms if r["payoff"]]
    if len(payoffs) != 1:
        return None
    best = None
    for start in (r["id"] for r in rooms if r["entrance"]):
        dist = {start: 1}
        todo = deque([start])
        while todo:
            cur = todo.popleft()
            for nxt in adj.get(cur, []):
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    todo.append(nxt)
        if payoffs[0] in dist and (best is None or dist[payoffs[0]] < best):
            best = dist[payoffs[0]]
    return best


def check_sites(b: Bible, only: str | None) -> list[Finding]:
    out: list[Finding] = []
    E = lambda eid, code, msg: out.append(Finding("sites", "error", eid, code, msg))
    W = lambda eid, code, msg: out.append(Finding("sites", "warning", eid, code, msg))
    ents = b.entities
    progress = read_json(b.root / "site-progress.json") or {"sites": {}}
    for eid, ent in ents.items():
        if ent.get("type") != "site" or (only and eid != only) or b.is_pending(ent):
            continue
        tele = ent.get("telegraphs") or []
        if len(tele) != 3 or [t.get("distance") for t in tele] != list(TELEGRAPH_DISTANCES):
            E(eid, "telegraphs", "needs exactly three telegraphs: far, near, threshold")
        if not ent.get("escape_tr"):
            E(eid, "no_escape", "escape geometry missing")
        if ent.get("attitude") not in ATTITUDES:
            E(eid, "attitude", f"attitude must be one of {ATTITUDES}")
        if ent.get("payoff") not in PAYOFFS:
            E(eid, "payoff", f"payoff must be one of {PAYOFFS}")
        if not ent.get("thread"):
            E(eid, "no_thread", "no thread: no site exists to fill a count")
        if not ent.get("if_never_visited_tr"):
            E(eid, "no_if_never_visited", "what happens if never visited is missing")
        if not isinstance(ent.get("room_count"), int) or ent["room_count"] < 1:
            E(eid, "room_count", "room_count must be a positive integer")
        # later-act references (errata 24.2 #9)
        path = b.root / ent["file"] if ent.get("file") else None
        text = b.prose.get(path.resolve() if path else None) if path else None
        if text is None and path:
            text = next((t for p, t in b.prose.items() if p.resolve() == path.resolve()), None)
        site_act = ent.get("act")
        if text and isinstance(site_act, int):
            for ref in wiki_links(text):
                other = ents.get(ref, {})
                other_act = other.get("stamped", {}).get("act", other.get("act"))
                if isinstance(other_act, int) and other_act > site_act and other.get("type") != "chapter":
                    E(eid, "later_act_ref", f"references {ref}, stamped to act {other_act}")
        # detailed sites: the room table
        status = b.status_of(eid)
        if status in ("detailed", "detailed-stale", "played") and text:
            rooms = parse_rooms(text)
            if not rooms:
                E(eid, "no_room_table", "status is detailed but no room table found")
                continue
            n, want = len(rooms), ent.get("room_count", 0)
            if want and abs(n - want) > max(1, round(want * 0.1)):
                E(eid, "room_count_drift", f"room table has {n} rooms, stamp says {want} (±10 %)")
            ids = {r["id"] for r in rooms}
            entrances = [r["id"] for r in rooms if r["entrance"]]
            payoffs = [r["id"] for r in rooms if r["payoff"]]
            if len(entrances) < 2:
                E(eid, "entrances", f"{len(entrances)} [Entrance] rooms, need at least 2")
            if len(payoffs) != 1:
                E(eid, "payoff_room", f"{len(payoffs)} [Payoff] rooms, need exactly 1")
            for r in rooms:
                if r["category"] not in ROOM_CATEGORIES:
                    E(eid, "room_category", f"room {r['id']} category {r['category']!r} unknown")
                for x in r["exits"]:
                    if x not in ids:
                        E(eid, "exit_dangling", f"room {r['id']} exits to {x}, which is not a room")
                if not r["exits"]:
                    E(eid, "room_dead", f"room {r['id']} has no exits")
            depth = min_depth(rooms)
            if depth is None:
                E(eid, "no_path", "no entrance reaches the payoff room")
            elif ent.get("min_depth") not in (None, depth):
                E(eid, "min_depth", f"shortest entrance→payoff path is {depth} rooms, registry says {ent.get('min_depth')}")
            xp = sum(r["xp"] for r in rooms)
            budget = ent.get("xp_budget")
            if budget and abs(xp - budget) > budget * 0.1:
                W(eid, "xp_budget", f"room XP {xp} vs budget {budget}")
            shares = {c: 100 * sum(1 for r in rooms if r["category"] == c) / n for c in ROOM_CATEGORIES}
            tol = MINOR_TOLERANCE if ent.get("role") == "minor" else 0
            for c, (lo, hi) in CONTENT_BANDS.items():
                if not lo - tol <= shares[c] <= hi + tol:
                    W(eid, "content_ratio", f"{c} rooms {shares[c]:.0f} %, band {lo}-{hi} %")
            rec = progress.get("sites", {}).get(eid)
            if rec:
                if sorted(rec.get("entrances", [])) != sorted(entrances):
                    E(eid, "progress_entrances", "site-progress entrances differ from the room table")
                if rec.get("payoff_room") != (payoffs[0] if payoffs else None):
                    E(eid, "progress_payoff", "site-progress payoff_room differs from the room table")
                if set(rec.get("rooms", {})) != ids:
                    E(eid, "progress_rooms", "site-progress room ids differ from the room table")
                for rid, state in rec.get("rooms", {}).items():
                    if state.get("state") == "skipped" and not state.get("reason"):
                        E(eid, "skip_unreasoned", f"room {rid} skipped without a reason")
    return out


MODULES = {
    "refs": check_refs, "stamps": check_stamps, "secrecy": check_secrecy,
    "overlay": check_overlay, "map": check_map, "sites": check_sites,
}


# ── run ───────────────────────────────────────────────────────────────────────

def run(campaign: str, modules: tuple, only: str | None = None, phase: str | None = None,
        fixture: bool = False) -> list[Finding]:
    b = load_bible(campaign, phase, fixture)
    findings: list[Finding] = []
    for m in modules:
        findings.extend(MODULES[m](b, only))
    return findings


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Structural validator of a designed campaign")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    p.add_argument("--modules", help="comma-separated subset of " + ",".join(MODULES))
    p.add_argument("--fast", action="store_true", help="refs+stamps+secrecy; never fails")
    p.add_argument("--only", metavar="ID", help="check one entity")
    p.add_argument("--phase", metavar="PN", help="per-phase run: pending rows of later phases are accepted")
    p.add_argument("--fixture", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--redact", action="store_true", help="accepted; output is redacted in every mode")
    args = p.parse_args(argv)

    if args.fast:
        modules = FAST_MODULES
    elif args.modules:
        modules = tuple(m.strip() for m in args.modules.split(",") if m.strip())
        unknown = [m for m in modules if m not in MODULES]
        if unknown:
            print(f"design_check: unknown module(s) {', '.join(unknown)}", file=sys.stderr)
            return 2
    else:
        modules = CORE_MODULES

    findings = run(args.campaign, modules, args.only, args.phase, args.fixture)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    if args.json:
        print(json.dumps([f.__dict__ for f in findings], indent=2, ensure_ascii=False))
    else:
        for m in modules:
            mine = [f for f in findings if f.module == m]
            print(f"[{m}] {len([f for f in mine if f.severity == 'error'])} errors, "
                  f"{len([f for f in mine if f.severity == 'warning'])} warnings")
            for f in mine:
                print(f.line())
        print(f"design_check: {len(errors)} errors, {len(warnings)} warnings"
              + (" (fast run: reported, not blocking)" if args.fast else ""))
    if args.fast:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
