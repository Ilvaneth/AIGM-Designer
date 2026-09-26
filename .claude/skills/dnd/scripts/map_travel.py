#!/usr/bin/env python3
"""
map_travel.py — the map graph in play: travel times, the encounter tables, reachability.

Plan items 6.1-6.2, 15 (map module), 16.3, 13.1; slice 1d. `design/map.json` is the graph (nodes with
coordinates, edges with days on horseback); everything here derives from it and is never hand-edited.

  map_travel.py -c CAMP travel-times [--out FILE]   design/travel-times.md: per region, days from the hub to
                                                     every place (shortest path, via), the settlement matrix,
                                                     the route list. Public + discoverable nodes only; when
                                                     the map has secret nodes the full table goes to
                                                     design/dm-only/travel-times.md as well.
  map_travel.py -c CAMP encounters [--out FILE]     reference/travel-encounters.md for travel.py, compiled
                                                     from every region file's "### Travel table" section
                                                     (the designer writes the tables; travel.py rolls them).
                                                     An existing Roll Log is kept.
  map_travel.py -c CAMP days FROM TO                 shortest days and the path between two node ids
  map_travel.py -c CAMP near ID [--days 1.0] [--kind site,settlement] [--json]
                                                     every node within N days of ID (the "approaching" test
                                                     of item 13.1a)

Exit codes: 0 ok · 1 no map / unknown node / nothing to compile · 2 usage
"""

from __future__ import annotations

import argparse
import heapq
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_io import campaign_dir, design_dir, dm_only_dir, now_iso, read_json  # noqa: E402

CATEGORY_ORDER = ["Quiet/Texture", "Social", "Environmental", "Combat", "Discovery", "Faction/Political"]


# ── the graph ─────────────────────────────────────────────────────────────────

def load_map(campaign: str) -> dict | None:
    return read_json(design_dir(campaign) / "map.json")


def projection(campaign: str) -> dict:
    return (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})


def adjacency(mp: dict) -> dict[str, list[tuple[str, float, dict]]]:
    adj: dict[str, list[tuple[str, float, dict]]] = {n["id"]: [] for n in mp.get("nodes", []) if n.get("id")}
    for e in mp.get("edges", []):
        a, b, d = e.get("from"), e.get("to"), e.get("days")
        if not (a and b) or not isinstance(d, (int, float)):
            continue
        adj.setdefault(a, []).append((b, float(d), e))
        adj.setdefault(b, []).append((a, float(d), e))
    return adj


def dijkstra(adj: dict, src: str) -> tuple[dict[str, float], dict[str, str | None]]:
    dist: dict[str, float] = {src: 0.0}
    prev: dict[str, str | None] = {src: None}
    heap = [(0.0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue
        for v, w, _ in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def path_of(prev: dict, dst: str) -> list[str]:
    out = []
    cur: str | None = dst
    while cur is not None:
        out.append(cur)
        cur = prev.get(cur)
    return list(reversed(out))


def fmt_days(d: float) -> str:
    return str(int(d)) if float(d).is_integer() else f"{d:g}"


def name_of(pub: dict, nid: str) -> str:
    if nid in pub:
        return pub[nid].get("name") or nid
    for prefix in ("landmark_", "waypoint_"):
        if nid.startswith(prefix):
            return nid[len(prefix):].replace("_", " ").title()
    return nid


# ── travel-times ──────────────────────────────────────────────────────────────

def travel_times_text(campaign: str, mp: dict, pub: dict, include_secret: bool) -> str:
    nodes = [n for n in mp.get("nodes", []) if n.get("id")]
    if not include_secret:
        nodes = [n for n in nodes if n.get("secrecy", "public") != "secret"]
    ids = {n["id"] for n in nodes}
    adj = adjacency({"nodes": nodes, "edges": [e for e in mp.get("edges", []) if e.get("from") in ids and e.get("to") in ids]})
    lines = [f"# Travel times — {campaign}", "",
             f"*Generated from `design/map.json` ({mp.get('_meta', {}).get('unit', 'days on horseback')}, shortest paths) by "
             f"`map_travel.py travel-times`; never hand-edited. A place reached through a hub is never closer than the hub.*", ""]
    regions = mp.get("regions") or {}
    by_region: dict[str, list[dict]] = {}
    for n in nodes:
        by_region.setdefault(n.get("region") or "—", []).append(n)
    for rid, rnodes in by_region.items():
        hub = next((n for n in rnodes if n.get("hub")), None) or next((n for n in rnodes if n.get("kind") == "settlement"), None)
        tier = (regions.get(rid) or {}).get("danger_tier")
        lines.append(f"## {name_of(pub, rid)}" + (f" (T{tier})" if tier else "") + (f" — from {name_of(pub, hub['id'])}" if hub else ""))
        lines.append("")
        if not hub:
            lines += ["*(no hub settlement on this region's map)*", ""]
            continue
        dist, prev = dijkstra(adj, hub["id"])
        lines += ["| Place | Kind | Days | Via |", "|---|---|---|---|"]
        for n in sorted(rnodes, key=lambda x: (dist.get(x["id"], float("inf")), x["id"])):
            if n["id"] == hub["id"]:
                continue
            d = dist.get(n["id"])
            via = " → ".join(name_of(pub, p) for p in path_of(prev, n["id"])[1:-1]) if d is not None else ""
            lines.append(f"| {name_of(pub, n['id'])} | {n.get('kind', '')} | {fmt_days(d) if d is not None else 'unreachable'} | {via or '—'} |")
        lines.append("")
    settlements = [n for n in nodes if n.get("kind") == "settlement"]
    if len(settlements) > 1:
        lines += ["## Settlement to settlement", "", "| From \\ To | " + " | ".join(name_of(pub, s["id"]) for s in settlements) + " |",
                  "|---|" + "---|" * len(settlements)]
        for s in settlements:
            dist, _ = dijkstra(adj, s["id"])
            cells = [("—" if t["id"] == s["id"] else fmt_days(dist[t["id"]]) if t["id"] in dist else "∞") for t in settlements]
            lines.append(f"| {name_of(pub, s['id'])} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## Routes", "", "| From | To | Days | Terrain | Road | Note |", "|---|---|---|---|---|---|"]
    for e in mp.get("edges", []):
        if e.get("from") in ids and e.get("to") in ids:
            lines.append(f"| {name_of(pub, e['from'])} | {name_of(pub, e['to'])} | {fmt_days(float(e.get('days') or 0))} | "
                         f"{e.get('terrain', '')} | {e.get('road', '')} | {e.get('note_tr') or '—'} |")
    lines += ["", f"*Üretildi: {now_iso()} — map_travel.py travel-times*"]
    return "\n".join(lines) + "\n"


def cmd_travel_times(campaign: str, out: str | None) -> int:
    mp = load_map(campaign)
    if not mp or not mp.get("nodes"):
        print("map_travel: no design/map.json (or no nodes) — P3 has not run", file=sys.stderr)
        return 1
    pub = projection(campaign)
    public_text = travel_times_text(campaign, mp, pub, include_secret=False)
    path = Path(out) if out else design_dir(campaign) / "travel-times.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(public_text, encoding="utf-8", newline="\n")
    print(f"map_travel: {path} ({len(public_text)} chars)")
    if any(n.get("secrecy") == "secret" for n in mp.get("nodes", [])) and not out:
        full = travel_times_text(campaign, mp, pub, include_secret=True)
        dm_path = dm_only_dir(campaign) / "travel-times.md"
        dm_path.parent.mkdir(parents=True, exist_ok=True)
        dm_path.write_text(full, encoding="utf-8", newline="\n")
        print("map_travel: the map has secret nodes; the full table is under design/dm-only/")
    return 0


# ── encounter tables for travel.py ────────────────────────────────────────────

TABLE_HEADING = re.compile(r"^### Travel table — (?P<region>.+?)(?:, from (?P<hub>.+?))?\s*$", re.M)


def travel_table_section(text: str) -> str | None:
    m = TABLE_HEADING.search(text)
    if not m:
        return None
    start = m.end()
    stop = re.compile(r"^#{1,3}\s+", re.M).search(text, pos=start)
    return text[start:stop.start() if stop else len(text)]


def convert_table(region_name: str, body: str) -> str:
    """The region file's table (#### Category, #### Early tier / ##### subtables) → travel.py's shape
    (### Early tier holding #### Category and #### subtables; ### Late tier holding its own subtables)."""
    lines = body.replace("\r\n", "\n").split("\n")
    category: list[str] = []
    early: list[str] = []
    late: list[str] = []
    bucket: list[str] | None = None
    for line in lines:
        if line.startswith("#### Category"):
            bucket = category
            continue
        if line.startswith("#### Early tier"):
            bucket = early
            continue
        if line.startswith("#### Late tier"):
            bucket = late
            continue
        if line.startswith("##### "):
            name = re.sub(r"\s*\(d\d+\)\s*$", "", line[6:]).strip()
            if bucket is not None:
                bucket.append(f"#### {name}")
            continue
        if bucket is not None:
            bucket.append(line)
    out = [f"## {region_name}", "", "### Early tier", "", "#### Category"] + [l for l in category if l.strip() or True]
    out += early
    if late:
        out += ["", "### Late tier", ""] + late
    return "\n".join(l for l in out).rstrip() + "\n"


def cmd_encounters(campaign: str, out: str | None) -> int:
    pub = projection(campaign)
    root = campaign_dir(campaign)
    sections = []
    for rid, ent in sorted(pub.items()):
        if ent.get("type") != "region" or not ent.get("file"):
            continue
        f = root / ent["file"]
        if not f.is_file():
            continue
        body = travel_table_section(f.read_text(encoding="utf-8"))
        if body:
            sections.append(convert_table(ent.get("name") or rid, body))
    if not sections:
        print("map_travel: no region file carries a `### Travel table` section", file=sys.stderr)
        return 1
    path = Path(out) if out else root / "reference" / "travel-encounters.md"
    roll_log = "## Roll Log\n\n| When | Route | Rolls | Outcome |\n|------|-------|-------|---------|\n"
    if path.is_file():
        old = path.read_text(encoding="utf-8")
        m = re.search(r"^## Roll Log\s*$", old, re.M)
        if m:
            roll_log = old[m.start():].rstrip() + "\n"
    head = (f"# Travel encounters — {campaign}\n\n*Compiled by `map_travel.py encounters` from the designer's region files "
            f"(`design/regions/<id>.md`, the `### Travel table` sections); tiers follow the threat stage in `design/overlay.json` "
            f"(Early = stage 1-2, Late = 3+). Edit the region files, then recompile; the Roll Log below is kept.*\n\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head + "\n".join(sections) + "\n" + roll_log, encoding="utf-8", newline="\n")
    print(f"map_travel: {path} ({len(sections)} region table(s))")
    return 0


# ── days / near ───────────────────────────────────────────────────────────────

def cmd_days(campaign: str, src: str, dst: str) -> int:
    mp = load_map(campaign)
    if not mp:
        print("map_travel: no design/map.json", file=sys.stderr)
        return 1
    adj = adjacency(mp)
    if src not in adj or dst not in adj:
        print(f"map_travel: unknown node {src if src not in adj else dst}", file=sys.stderr)
        return 1
    dist, prev = dijkstra(adj, src)
    if dst not in dist:
        print(f"map_travel: {dst} is unreachable from {src}")
        return 1
    pub = projection(campaign)
    print(f"{fmt_days(dist[dst])} day(s): " + " → ".join(name_of(pub, p) for p in path_of(prev, dst)))
    return 0


def near(campaign: str, src: str, days: float, kinds: set | None = None) -> list[dict]:
    mp = load_map(campaign) or {}
    adj = adjacency(mp)
    if src not in adj:
        return []
    dist, _ = dijkstra(adj, src)
    kind_of = {n["id"]: n.get("kind") for n in mp.get("nodes", []) if n.get("id")}
    out = []
    for nid, d in sorted(dist.items(), key=lambda kv: (kv[1], kv[0])):
        if nid == src or d > days + 1e-9:
            continue
        if kinds and kind_of.get(nid) not in kinds:
            continue
        out.append({"id": nid, "kind": kind_of.get(nid), "days": d})
    return out


def cmd_near(campaign: str, src: str, days: float, kind: str | None, as_json: bool) -> int:
    kinds = {k.strip() for k in kind.split(",") if k.strip()} if kind else None
    rows = near(campaign, src, days, kinds)
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    pub = projection(campaign)
    if not rows:
        print(f"map_travel: nothing within {fmt_days(days)} day(s) of {src}")
        return 0
    for r in rows:
        print(f"  {fmt_days(r['days']):>5}  {r['kind']:<11} {r['id']:<32} {name_of(pub, r['id'])}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the map graph in play")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    t = sub.add_parser("travel-times")
    t.add_argument("--out")
    e = sub.add_parser("encounters")
    e.add_argument("--out")
    d = sub.add_parser("days")
    d.add_argument("src")
    d.add_argument("dst")
    n = sub.add_parser("near")
    n.add_argument("id")
    n.add_argument("--days", type=float, default=1.0)
    n.add_argument("--kind")
    n.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.verb == "travel-times":
        return cmd_travel_times(a.campaign, a.out)
    if a.verb == "encounters":
        return cmd_encounters(a.campaign, a.out)
    if a.verb == "days":
        return cmd_days(a.campaign, a.src, a.dst)
    if a.verb == "near":
        return cmd_near(a.campaign, a.id, a.days, a.kind, a.json)
    return 2


if __name__ == "__main__":
    sys.exit(main())
