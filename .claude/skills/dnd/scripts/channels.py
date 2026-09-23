#!/usr/bin/env python3
"""
channels.py — private channels, and the facts that only travelled through them.

The source-of-knowledge rule fails hardest on facts the DM wrote minutes ago.
A troop count sent by Sending Stone, a plan agreed in a closed room, the
contents of a sealed letter: the DM knows it because they just authored it, so
an NPC "knowing" it feels natural, and the leak is invisible until a player
catches it.

A channel records who was actually party to a private exchange, and what passed
through it. Then the question "could this NPC know that?" has an answer that
can be looked up instead of recalled.

Stored in <campaign>/channels.json.

Usage:
    CAMP=my-campaign

    python3 channels.py -c $CAMP list
    python3 channels.py -c $CAMP add --id stone-sethra --type sending-stone \\
        --name "Sending Stone — Kriv/Sethra (Hold line)" \\
        --participants "Kriv Shestendeliath,Sethra Shestendeliath"
    python3 channels.py -c $CAMP fact stone-sethra --day 206 \\
        --text "Order to raise 200 soldiers for the Hold" --keywords "200 asker,200 soldiers"

    # Before an NPC says something that might not be theirs to know:
    python3 channels.py -c $CAMP check "Duyduğuma göre Hold'da 200 asker toplanıyor"
    python3 channels.py -c $CAMP who "200 asker"

Exit codes: 0 clear, 2 the text touches a private fact (check).
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

from paths import find_campaign as _find_campaign

CHANNEL_TYPES = ["sending-stone", "private-meeting", "letter", "spell", "other"]


def _path(campaign: str) -> str:
    return os.path.join(str(_find_campaign(campaign)), "channels.json")


def _load(campaign: str) -> dict:
    try:
        with open(_path(campaign), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"channels": []}


def _save(campaign: str, data: dict) -> None:
    with open(_path(campaign), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def _find(data: dict, cid: str):
    for c in data["channels"]:
        if c["id"] == cid:
            return c
    return None


def cmd_list(campaign: str, verbose: bool) -> None:
    data = _load(campaign)
    if not data["channels"]:
        print("  No private channels recorded.")
        return
    total = sum(len(c.get("facts", [])) for c in data["channels"])
    print(f"  {len(data['channels'])} private channel(s), {total} recorded fact(s).")
    print("  Nothing that passed through these is public knowledge — an NPC who was")
    print("  not party to the exchange cannot cite it, however obvious it feels.\n")
    for c in data["channels"]:
        print(f"  [{c['id']}] {c['name']}  ({c.get('type','other')})")
        print(f"      party to it: {', '.join(c.get('participants', [])) or '(unrecorded)'}")
        facts = c.get("facts", [])
        if facts and verbose:
            for fact in facts:
                print(f"      day {fact.get('day','?')}: {fact.get('text','')}")
        elif facts:
            print(f"      {len(facts)} fact(s) — `list --verbose` to see them")
        print()


def cmd_add(campaign: str, args) -> None:
    data = _load(campaign)
    if _find(data, args.id):
        print(f"  ! channel '{args.id}' already exists")
        sys.exit(1)
    data["channels"].append({
        "id": args.id,
        "name": args.name,
        "type": args.type,
        "participants": [p.strip() for p in args.participants.split(",") if p.strip()],
        "note": args.note,
        "facts": [],
    })
    _save(campaign, data)
    print(f"  + {args.name} [{args.id}] — {len(data['channels'][-1]['participants'])} participant(s)")


def cmd_fact(campaign: str, args) -> None:
    data = _load(campaign)
    c = _find(data, args.id)
    if not c:
        print(f"  ! no channel '{args.id}'")
        sys.exit(1)
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if not keywords:
        # Fall back to the longest words in the text, which is usually where the
        # give-away detail lives (a number, a name, a place).
        keywords = sorted(set(re.findall(r"[\w'’]{4,}", args.text)), key=len, reverse=True)[:4]
    c.setdefault("facts", []).append({"day": args.day, "text": args.text, "keywords": keywords})
    _save(campaign, data)
    print(f"  + {c['name']}: day {args.day} — {args.text}")
    print(f"    keywords: {', '.join(keywords)}")


def _matches(data: dict, text: str):
    """Private facts whose keywords appear in `text`."""
    low = text.lower()
    hits = []
    for c in data["channels"]:
        for fact in c.get("facts", []):
            for kw in fact.get("keywords", []):
                if kw.lower() in low:
                    hits.append((c, fact, kw))
                    break
    return hits


def cmd_check(campaign: str, text: str, speaker: str) -> None:
    data = _load(campaign)
    hits = _matches(data, text)
    if not hits:
        print("  clear — nothing in this line touches a recorded private fact.")
        return

    print("  " + "=" * 66)
    print(f"  !!! PRIVATE FACT TOUCHED ({len(hits)})")
    print("  " + "=" * 66)
    blocked = False
    for c, fact, kw in hits:
        who = c.get("participants", [])
        print(f"\n    \"{kw}\" — from {c['name']} (day {fact.get('day','?')})")
        print(f"      {fact.get('text','')}")
        print(f"      party to it: {', '.join(who) or '(unrecorded)'}")
        if speaker:
            ok = any(speaker.lower() in p.lower() or p.lower() in speaker.lower() for p in who)
            verdict = "may cite it" if ok else "CANNOT know this"
            print(f"      {speaker}: {verdict}")
            blocked = blocked or not ok
    if speaker and blocked:
        print("\n  Give the information a channel this speaker actually has, or let them")
        print("  not know it. Do not hand it over because it is convenient.")
    sys.exit(2)


def cmd_who(campaign: str, keyword: str) -> None:
    data = _load(campaign)
    hits = _matches(data, keyword)
    if not hits:
        print(f"  '{keyword}' is not recorded as passing through a private channel.")
        return
    for c, fact, kw in hits:
        print(f"  {fact.get('text','')}  (day {fact.get('day','?')}, {c['name']})")
        print(f"    known to: {', '.join(c.get('participants', [])) or '(unrecorded)'}")


def main() -> None:
    p = argparse.ArgumentParser(description="Private channels and the facts confined to them")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    lst = sub.add_parser("list", help="Every private channel and who is party to it")
    lst.add_argument("--verbose", action="store_true")

    add = sub.add_parser("add", help="Record a private channel")
    add.add_argument("--id", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--type", default="other", choices=CHANNEL_TYPES)
    add.add_argument("--participants", default="", help="Comma-separated")
    add.add_argument("--note", default="")

    fct = sub.add_parser("fact", help="Record something that passed through a channel")
    fct.add_argument("id")
    fct.add_argument("--day", type=int, required=True)
    fct.add_argument("--text", required=True)
    fct.add_argument("--keywords", default="", help="Comma-separated give-away phrases")

    chk = sub.add_parser("check", help="Does this line touch a private fact?")
    chk.add_argument("text")
    chk.add_argument("--speaker", default="", help="Who is about to say it")

    who = sub.add_parser("who", help="Who is allowed to know this")
    who.add_argument("keyword")

    args = p.parse_args()
    if args.cmd == "list":
        cmd_list(args.campaign, args.verbose)
    elif args.cmd == "add":
        cmd_add(args.campaign, args)
    elif args.cmd == "fact":
        cmd_fact(args.campaign, args)
    elif args.cmd == "check":
        cmd_check(args.campaign, args.text, args.speaker)
    elif args.cmd == "who":
        cmd_who(args.campaign, args.keyword)


if __name__ == "__main__":
    main()
