#!/usr/bin/env python3
"""
site_progress.py — a site is a graph, not a list: room-by-room play records.

Plan item 9.5 (play side), 13.3, 16.5, 21.D; docs/schemas/site-progress.md.
The site counterpart of tracker.json, at <campaign>/site-progress.json. Only
this script writes it, and only this script (with campaign_graph.py) writes the
overlay's `seen_in_play` and the `played` status of a site.

CLI:
  site_progress.py -c CAMP open SITE [--entrances 1,4 --payoff 6 --min-depth 3 --rooms 6]
                                       (defaults parsed from the site file's room table)
  site_progress.py -c CAMP enter SITE ROOM --day N --session N [--via ROOM]
  site_progress.py -c CAMP clear SITE ROOM --day N --session N
  site_progress.py -c CAMP skip  SITE ROOM --reason TEXT --day N --session N
  site_progress.py -c CAMP shortcut SITE --from ROOM --to ROOM --how TEXT --day N
  site_progress.py -c CAMP rest  SITE ROOM --kind short|long --day N
  site_progress.py -c CAMP note  SITE TEXT
  site_progress.py -c CAMP status [SITE]            "Batık İskele: 2/6 oda" for /dm:dnd save
Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_check import min_depth as graph_min_depth, parse_rooms  # noqa: E402
from design_io import (campaign_dir, dm_only_dir, load_overlay, overlay_set, read_json, save_overlay,  # noqa: E402
                       stamp_meta, write_json_atomic)

ROOM_STATES = ("unseen", "seen", "cleared", "skipped")


def store_path(campaign: str) -> Path:
    return campaign_dir(campaign) / "site-progress.json"


def load(campaign: str) -> dict:
    data = read_json(store_path(campaign))
    if data is None:
        data = {"_meta": {"schema_version": 1, "campaign": campaign}, "sites": {}}
    data.setdefault("sites", {})
    return data


def save(campaign: str, data: dict, verb: str) -> None:
    stamp_meta(data, campaign, f"site_progress.py {verb}")
    write_json_atomic(store_path(campaign), data)


def entity(campaign: str, site: str) -> dict | None:
    return (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {}).get(site)


def site_name(campaign: str, site: str) -> str:
    ent = entity(campaign, site)
    return ent["name"] if ent and ent.get("secrecy") != "secret" else site


def record_or_die(data: dict, site: str) -> dict:
    rec = data["sites"].get(site)
    if rec is None:
        print(f"site_progress: no record for {site}; run `open` first (a skeleton site has no rooms to track)",
              file=sys.stderr)
        raise SystemExit(1)
    return rec


def room_or_die(rec: dict, room: str) -> dict:
    if room not in rec["rooms"]:
        print(f"site_progress: room {room} is not in the table ({', '.join(rec['rooms'])})", file=sys.stderr)
        raise SystemExit(1)
    return rec["rooms"][room]


# ── verbs ─────────────────────────────────────────────────────────────────────

def cmd_open(campaign: str, a) -> int:
    data = load(campaign)
    if a.site in data["sites"] and not a.force:
        print(f"site_progress: {a.site} already open; --force to rebuild (progress is lost)", file=sys.stderr)
        return 1
    ent = entity(campaign, a.site)
    if ent is None or ent.get("type") != "site":
        print(f"site_progress: {a.site} is not a site in the registry", file=sys.stderr)
        return 1
    rooms: list[dict] = []
    if ent.get("file") and (campaign_dir(campaign) / ent["file"]).is_file():
        rooms = parse_rooms((campaign_dir(campaign) / ent["file"]).read_text(encoding="utf-8"))
    if rooms:
        entrances = [r["id"] for r in rooms if r["entrance"]]
        payoff = next((r["id"] for r in rooms if r["payoff"]), None)
        depth = graph_min_depth(rooms)
        ids = [r["id"] for r in rooms]
    else:
        if not (a.entrances and a.payoff and a.rooms):
            print(f"site_progress: {a.site} has no room table; give --entrances, --payoff and --rooms",
                  file=sys.stderr)
            return 1
        entrances = [x.strip() for x in a.entrances.split(",") if x.strip()]
        payoff, depth = a.payoff, a.min_depth
        ids = [str(i) for i in range(1, int(a.rooms) + 1)]
    if a.entrances:
        entrances = [x.strip() for x in a.entrances.split(",") if x.strip()]
    if a.payoff:
        payoff = a.payoff
    if a.min_depth is not None:
        depth = a.min_depth
    data["sites"][a.site] = {
        "opened_day": None, "opened_session": None, "entered_via": None,
        "entrances": entrances, "payoff_room": payoff, "min_depth": depth, "room_count": len(ids),
        "current_room": None,
        "rooms": {rid: {"state": "unseen", "day": None, "session": None, "reason": None} for rid in ids},
        "shortcuts_earned": [], "rests": [], "notes": [],
    }
    save(campaign, data, "open")
    print(f"site_progress: {site_name(campaign, a.site)} opened — {len(ids)} rooms, entrances "
          f"{', '.join(entrances)}, payoff {payoff}, minimum depth {depth}")
    return 0


def cmd_enter(campaign: str, a) -> int:
    data = load(campaign)
    rec = record_or_die(data, a.site)
    room = room_or_die(rec, a.room)
    first = rec["opened_day"] is None
    if first:
        via = a.via or a.room
        if via not in rec["entrances"]:
            print(f"site_progress: {via} is not an entrance ({', '.join(rec['entrances'])}); "
                  "a first entry comes through an entrance unless a shortcut was earned", file=sys.stderr)
            return 1
        rec.update({"opened_day": a.day, "opened_session": a.session, "entered_via": via})
    if room["state"] == "unseen":
        room.update({"state": "seen", "day": a.day, "session": a.session})
    rec["current_room"] = a.room
    save(campaign, data, "enter")
    if first:
        overlay = load_overlay(campaign)
        ent = entity(campaign, a.site) or {}
        overlay_set(overlay, a.site, "status", "played", writer="site_progress.py", day=a.day,
                    birth="skeleton", reason="first entry")
        overlay_set(overlay, a.site, "seen_in_play", True, writer="site_progress.py", day=a.day, birth=False)
        save_overlay(campaign, overlay, "site_progress.py enter")
    print(f"site_progress: {site_name(campaign, a.site)} — in room {a.room}" + ("  (first entry)" if first else ""))
    return 0


def cmd_clear(campaign: str, a) -> int:
    data = load(campaign)
    rec = record_or_die(data, a.site)
    room = room_or_die(rec, a.room)
    room.update({"state": "cleared", "day": a.day, "session": a.session})
    rec["current_room"] = a.room
    save(campaign, data, "clear")
    print(f"site_progress: room {a.room} cleared")
    return 0


def cmd_skip(campaign: str, a) -> int:
    if not a.reason.strip():
        print("site_progress: a skipped room needs a reason", file=sys.stderr)
        return 2
    data = load(campaign)
    rec = record_or_die(data, a.site)
    room = room_or_die(rec, a.room)
    room.update({"state": "skipped", "day": a.day, "session": a.session, "reason": a.reason.strip()})
    save(campaign, data, "skip")
    print(f"site_progress: room {a.room} skipped ({a.reason.strip()})")
    return 0


def cmd_shortcut(campaign: str, a) -> int:
    data = load(campaign)
    rec = record_or_die(data, a.site)
    for r in (a.from_room, a.to_room):
        room_or_die(rec, r)
    rec["shortcuts_earned"].append({"from": a.from_room, "to": a.to_room, "how_tr": a.how, "day": a.day})
    save(campaign, data, "shortcut")
    print(f"site_progress: shortcut {a.from_room} → {a.to_room} earned")
    return 0


def cmd_rest(campaign: str, a) -> int:
    data = load(campaign)
    rec = record_or_die(data, a.site)
    room_or_die(rec, a.room)
    rec["rests"].append({"room": a.room, "kind": a.kind, "day": a.day})
    save(campaign, data, "rest")
    print(f"site_progress: {a.kind} rest in room {a.room}")
    return 0


def cmd_note(campaign: str, a) -> int:
    data = load(campaign)
    rec = record_or_die(data, a.site)
    rec["notes"].append(a.text)
    save(campaign, data, "note")
    return 0


def summary(campaign: str, site: str, rec: dict) -> str:
    states = [r["state"] for r in rec["rooms"].values()]
    seen = sum(1 for s in states if s != "unseen")
    cleared = sum(1 for s in states if s == "cleared")
    skipped = sum(1 for s in states if s == "skipped")
    line = f"{site_name(campaign, site)}: {seen}/{len(states)} oda"
    if cleared:
        line += f", {cleared} temizlendi"
    if skipped:
        line += f", {skipped} atlandı"
    if rec.get("current_room"):
        line += f" — şu an oda {rec['current_room']}"
    if rec["opened_day"] is None:
        line += " (henüz girilmedi)"
    unreasoned = [rid for rid, r in rec["rooms"].items() if r["state"] == "skipped" and not r.get("reason")]
    if unreasoned:
        line += f"  !! sebepsiz atlanan oda: {', '.join(unreasoned)}"
    return line


def cmd_status(campaign: str, a) -> int:
    data = load(campaign)
    sites = {a.site: record_or_die(data, a.site)} if a.site else data["sites"]
    if not sites:
        print("site_progress: no site records yet")
        return 0
    for site, rec in sites.items():
        print("  " + summary(campaign, site, rec))
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Room-by-room progress records for designed sites")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("open")
    o.add_argument("site")
    o.add_argument("--entrances")
    o.add_argument("--payoff")
    o.add_argument("--min-depth", type=int)
    o.add_argument("--rooms")
    o.add_argument("--force", action="store_true")

    for verb in ("enter", "clear", "skip"):
        s = sub.add_parser(verb)
        s.add_argument("site")
        s.add_argument("room")
        s.add_argument("--day", type=int, required=True)
        s.add_argument("--session", type=int, required=True)
        if verb == "enter":
            s.add_argument("--via")
        if verb == "skip":
            s.add_argument("--reason", required=True)

    sc = sub.add_parser("shortcut")
    sc.add_argument("site")
    sc.add_argument("--from", dest="from_room", required=True)
    sc.add_argument("--to", dest="to_room", required=True)
    sc.add_argument("--how", required=True)
    sc.add_argument("--day", type=int, required=True)

    r = sub.add_parser("rest")
    r.add_argument("site")
    r.add_argument("room")
    r.add_argument("--kind", choices=("short", "long"), required=True)
    r.add_argument("--day", type=int, required=True)

    n = sub.add_parser("note")
    n.add_argument("site")
    n.add_argument("text")

    st = sub.add_parser("status")
    st.add_argument("site", nargs="?")

    a = p.parse_args(argv)
    return {"open": cmd_open, "enter": cmd_enter, "clear": cmd_clear, "skip": cmd_skip,
            "shortcut": cmd_shortcut, "rest": cmd_rest, "note": cmd_note, "status": cmd_status}[a.cmd](a.campaign, a)


if __name__ == "__main__":
    sys.exit(main())
