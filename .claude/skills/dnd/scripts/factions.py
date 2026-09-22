#!/usr/bin/env python3
"""
factions.py — the faction chessboard: standing plans, costs, intel, reactions.

A faction that only gets a one-line entry in a session-end log has memory but
no forward model. Asked "what did they do while the party was occupied?", the
honest answer each session is a reaction to the party -- because a
past-tense question cannot produce a plan. And when the party allies with one
power, the rivals cannot respond, because "who is that faction's rival" is not
written down anywhere a tool can read.

This file is that missing model. Every active faction carries:

  * an objective (what they want) and a running operation (the next concrete
    steps, each with an in-world due day),
  * move points -- a weekly budget spent to act, so standing still is a choice
    with a cost and losing assets visibly reduces what a faction can do,
  * an intel rating (0-3) that decides what they learn and how fast,
  * stances toward the other factions and the party (-3..+3), which is what
    makes `react` able to compute who answers a move and how.

Stored in <campaign>/factions.json.

Usage:
    CAMP=my-campaign

    # See the board
    python3 factions.py -c $CAMP list
    python3 factions.py -c $CAMP show whisper-court

    # Build it
    python3 factions.py -c $CAMP add --id house-corr --name "House Corr" \
        --objective "Hold the Ember Quarter seat without open war" --power 3 --intel 2
    python3 factions.py -c $CAMP stance --from house-corr --to house-ilvane --level -2
    python3 factions.py -c $CAMP op house-corr --name "Quiet succession" \
        --step "Buy the Chancellery clerk@206" --step "Table the claim@212"

    # Run it
    python3 factions.py -c $CAMP tick --day 204          # weekly budgets + due steps
    python3 factions.py -c $CAMP react --actor house-corr --trigger alliance \
        --event "House Corr publicly backed the party" --visibility public --day 204
    python3 factions.py -c $CAMP move whisper-court --spend 1 --text "..." --day 205
    python3 factions.py -c $CAMP sweep --day 204          # end of session
    python3 factions.py -c $CAMP check --day 204          # loud flags for load/save

Exit codes: 0 fine, 2 something needs the DM's attention (check/tick).
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

from paths import find_campaign as _find_campaign

WEEK = 7

STANCE_LABEL = {
    3: "sworn ally", 2: "ally", 1: "friendly", 0: "neutral",
    -1: "wary", -2: "rival", -3: "enemy",
}

# How long word takes to reach a faction, by how visible the event was and how
# good their intelligence is. Secret events only reach the well-informed.
VISIBILITY = {
    "public":  {"base": 2, "min_intel": 0},
    "rumored": {"base": 5, "min_intel": 1},
    "secret":  {"base": 9, "min_intel": 2},
}

TRIGGERS = ["alliance", "loss", "gain", "exposure", "death", "betrayal", "other"]

IDLE_DAYS = 14          # a faction silent this long is a flag, not a mood


def _path(campaign: str) -> str:
    return os.path.join(str(_find_campaign(campaign)), "factions.json")


def _load(campaign: str) -> dict:
    try:
        with open(_path(campaign), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"_meta": {"week_length": WEEK}, "factions": []}


def _save(campaign: str, data: dict) -> None:
    with open(_path(campaign), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def _find(data: dict, fid: str) -> "dict | None":
    for f in data["factions"]:
        if f["id"] == fid:
            return f
    return None


def _stance(f: dict, other: str) -> int:
    return int(f.get("stances", {}).get(other, 0))


def _mp(f: dict) -> dict:
    return f.setdefault("move_points", {"per_week": f.get("power", 2),
                                        "available": f.get("power", 2),
                                        "refreshed_day": 0})


def _last_move_day(f: dict) -> "int | None":
    history = f.get("history", [])
    return history[-1].get("day") if history else None


def _next_step(f: dict) -> "dict | None":
    op = f.get("operation") or {}
    for step in op.get("steps", []):
        if not step.get("done"):
            return step
    return None


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_list(campaign: str, show_all: bool) -> None:
    data = _load(campaign)
    rows = [f for f in data["factions"] if show_all or f.get("status", "active") == "active"]
    if not rows:
        print("  No factions recorded. Add one with `factions.py -c <campaign> add`.")
        return
    print(f"  {'ID':<20} {'MP':<7} {'INT':<4} {'STATUS':<9} NEXT STEP / OBJECTIVE")
    print(f"  {'-'*20} {'-'*7} {'-'*4} {'-'*9} {'-'*44}")
    for f in rows:
        mp = _mp(f)
        step = _next_step(f)
        tail = (f"-> {step['text']} (day {step.get('due_day','?')})" if step
                else f.get("objective", "")[:44])
        print(f"  {f['id']:<20} {mp['available']}/{mp['per_week']:<5} "
              f"{f.get('intel',1):<4} {f.get('status','active'):<9} {tail[:60]}")


def cmd_show(campaign: str, fid: str) -> None:
    data = _load(campaign)
    f = _find(data, fid)
    if not f:
        print(f"  ! no faction '{fid}'")
        sys.exit(1)
    mp = _mp(f)
    print(f"\n  {f['name']}  [{f['id']}]  — {f.get('status','active')}")
    print(f"  Objective : {f.get('objective','(none set)')}")
    print(f"  Power {f.get('power','?')}  ·  Move points {mp['available']}/{mp['per_week']} per week"
          f"  ·  Intel {f.get('intel',1)}/3")
    if f.get("assets"):
        print("  Assets    : " + "; ".join(f["assets"]))
    op = f.get("operation") or {}
    if op:
        print(f"\n  OPERATION: {op.get('name','(unnamed)')}")
        for i, step in enumerate(op.get("steps", []), 1):
            mark = "x" if step.get("done") else " "
            print(f"    [{mark}] {i}. {step['text']}  (day {step.get('due_day','?')})")
        if op.get("abandon_if"):
            print(f"    abandons if: {op['abandon_if']}")
    else:
        print("\n  OPERATION: none — this faction has no plan running.")
    if f.get("stances"):
        print("\n  Stances:")
        for other, level in sorted(f["stances"].items(), key=lambda kv: kv[1]):
            print(f"    {level:+d} {STANCE_LABEL.get(level, '?'):<10} {other}")
    if f.get("reactions"):
        print("\n  Reaction doctrine:")
        for trigger, text in f["reactions"].items():
            print(f"    {trigger:<10} {text}")
    if f.get("knows"):
        print("\n  Knows:")
        for k in f["knows"][-6:]:
            print(f"    day {k.get('day','?')}: {k.get('fact','')}  ({k.get('via','')})")
    if f.get("history"):
        print("\n  Recent moves:")
        for h in f["history"][-5:]:
            print(f"    day {h.get('day','?')}: {h.get('text','')}")
    print()


def cmd_add(campaign: str, args) -> None:
    data = _load(campaign)
    if _find(data, args.id):
        print(f"  ! faction '{args.id}' already exists")
        sys.exit(1)
    power = int(args.power)
    data["factions"].append({
        "id": args.id,
        "name": args.name,
        "status": args.status,
        "objective": args.objective,
        "power": power,
        "intel": int(args.intel),
        "move_points": {"per_week": power, "available": power, "refreshed_day": 0},
        "assets": [a.strip() for a in args.assets.split(";") if a.strip()],
        "stances": {},
        "operation": {},
        "reactions": {},
        "knows": [],
        "history": [],
    })
    _save(campaign, data)
    print(f"  + {args.name} [{args.id}] — power {power}, intel {args.intel}")


def cmd_set(campaign: str, args) -> None:
    data = _load(campaign)
    f = _find(data, args.id)
    if not f:
        print(f"  ! no faction '{args.id}'")
        sys.exit(1)
    if args.objective:
        f["objective"] = args.objective
    if args.status:
        f["status"] = args.status
    if args.intel:
        f["intel"] = int(args.intel)
    if args.power:
        f["power"] = int(args.power)
        _mp(f)["per_week"] = int(args.power)
    if args.assets:
        f["assets"] = [a.strip() for a in args.assets.split(";") if a.strip()]
    if args.reaction:
        trigger, _, text = args.reaction.partition("=")
        f.setdefault("reactions", {})[trigger.strip()] = text.strip()
    _save(campaign, data)
    print(f"  updated {f['name']}")


def cmd_stance(campaign: str, args) -> None:
    data = _load(campaign)
    f = _find(data, getattr(args, "from"))
    if not f:
        print(f"  ! no faction '{getattr(args, 'from')}'")
        sys.exit(1)
    level = max(-3, min(3, int(args.level)))
    f.setdefault("stances", {})[args.to] = level
    if args.mutual:
        other = _find(data, args.to)
        if other:
            other.setdefault("stances", {})[getattr(args, "from")] = level
    _save(campaign, data)
    print(f"  {f['id']} -> {args.to}: {level:+d} ({STANCE_LABEL.get(level,'?')})"
          + ("  [mutual]" if args.mutual else ""))


def cmd_op(campaign: str, args) -> None:
    data = _load(campaign)
    f = _find(data, args.id)
    if not f:
        print(f"  ! no faction '{args.id}'")
        sys.exit(1)
    steps = []
    for raw in args.step:
        text, _, day = raw.rpartition("@")
        if not text:
            text, day = raw, ""
        steps.append({"text": text.strip(), "due_day": int(day) if day.strip().isdigit() else None,
                      "done": False})
    f["operation"] = {"name": args.name or "(unnamed)", "steps": steps,
                      "abandon_if": args.abandon_if}
    _save(campaign, data)
    print(f"  {f['name']}: operation '{f['operation']['name']}' with {len(steps)} step(s)")
    for i, s in enumerate(steps, 1):
        print(f"    {i}. {s['text']}  (day {s['due_day']})")


def cmd_step(campaign: str, args) -> None:
    data = _load(campaign)
    f = _find(data, args.id)
    if not f or not f.get("operation"):
        print(f"  ! no operation for '{args.id}'")
        sys.exit(1)
    steps = f["operation"].get("steps", [])
    if not 1 <= args.number <= len(steps):
        print(f"  ! step {args.number} out of range (1-{len(steps)})")
        sys.exit(1)
    steps[args.number - 1]["done"] = not args.undo
    _save(campaign, data)
    state = "open again" if args.undo else "done"
    print(f"  {f['name']}: step {args.number} {state} — {steps[args.number-1]['text']}")
    nxt = _next_step(f)
    print(f"  next: {nxt['text']} (day {nxt.get('due_day','?')})" if nxt
          else "  operation complete — set the next one with `op`.")


def cmd_move(campaign: str, args) -> None:
    data = _load(campaign)
    f = _find(data, args.id)
    if not f:
        print(f"  ! no faction '{args.id}'")
        sys.exit(1)
    mp = _mp(f)
    spend = int(args.spend)
    if spend > mp["available"]:
        print(f"  ! {f['name']} has {mp['available']} move point(s) left this week, "
              f"not {spend}.")
        print("    A faction that is out of budget cannot also be acting everywhere:")
        print("    either this move waits, or something else it is doing stops.")
        sys.exit(2)
    mp["available"] -= spend
    f.setdefault("history", []).append({"day": args.day, "text": args.text, "cost": spend})
    _save(campaign, data)
    print(f"  {f['name']} (day {args.day}, -{spend} MP, {mp['available']} left): {args.text}")


def cmd_tick(campaign: str, day: int) -> None:
    """Refresh weekly budgets and surface everything that is due."""
    data = _load(campaign)
    week = data.get("_meta", {}).get("week_length", WEEK)
    refreshed, due, overdue, idle = [], [], [], []

    for f in data["factions"]:
        if f.get("status", "active") != "active":
            continue
        mp = _mp(f)
        if day - mp.get("refreshed_day", 0) >= week:
            mp["available"] = mp["per_week"]
            mp["refreshed_day"] = day
            refreshed.append(f["name"])
        step = _next_step(f)
        if step and step.get("due_day") is not None:
            if step["due_day"] < day:
                overdue.append((f, step))
            elif step["due_day"] <= day + 1:
                due.append((f, step))
        last = _last_move_day(f)
        if last is not None and day - last >= IDLE_DAYS:
            idle.append((f, day - last))
        elif last is None and not step:
            idle.append((f, None))

    data.setdefault("_meta", {})["ticked_day"] = day
    _save(campaign, data)

    print(f"  Faction tick — day {day}")
    if refreshed:
        print(f"  move points refreshed: {', '.join(refreshed)}")

    flagged = bool(due or overdue or idle)
    if overdue:
        print("\n  " + "=" * 64)
        print("  !!! FACTION STEPS OVERDUE — these should already have happened")
        print("  " + "=" * 64)
        for f, step in overdue:
            print(f"    {f['name']}: {step['text']}  (was due day {step['due_day']})")
    if due:
        print("\n  DUE NOW:")
        for f, step in due:
            print(f"    {f['name']}: {step['text']}  (day {step['due_day']})")
    if idle:
        print("\n  SILENT TOO LONG — give them a step or mark them dormant:")
        for f, gap in idle:
            print(f"    {f['name']}: " + (f"{gap} days since last move" if gap
                                          else "no operation, no moves on record"))
    if not flagged:
        print("  nothing due, nothing overdue, nobody idle.")
    sys.exit(2 if (overdue or idle) else 0)


def cmd_react(campaign: str, args) -> None:
    """The chessboard: who hears about this, who has to answer it, and with what."""
    data = _load(campaign)
    actor = _find(data, args.actor)
    if not actor:
        print(f"  ! no faction '{args.actor}'")
        sys.exit(1)
    vis = VISIBILITY[args.visibility]
    day = args.day

    print(f"\n  EVENT (day {day}, {args.visibility}): {args.event}")
    print(f"  Actor: {actor['name']}   Trigger: {args.trigger}")
    print("  " + "=" * 64)

    responders, bystanders, deaf = [], [], []
    for f in data["factions"]:
        if f["id"] == actor["id"] or f.get("status", "active") != "active":
            continue
        intel = int(f.get("intel", 1))
        if intel < vis["min_intel"]:
            deaf.append(f)
            continue
        delay = max(0, vis["base"] - intel)
        learns_on = day + delay
        stance_to_actor = _stance(f, actor["id"])
        stance_to_party = _stance(f, "party")
        # A faction answers when the actor is a rival, or when the event helps
        # the party and this faction is set against the party.
        must = stance_to_actor <= -1 or (args.trigger in ("alliance", "gain")
                                         and stance_to_party <= -1)
        (responders if must else bystanders).append((f, learns_on, stance_to_actor))

    if responders:
        print("\n  MUST ANSWER — write a move for each of these before moving on:")
        for f, learns_on, st in responders:
            mp = _mp(f)
            step = _next_step(f)
            print(f"\n    {f['name']}  [{f['id']}]")
            print(f"      hears on day {learns_on} (intel {f.get('intel',1)}) · "
                  f"stance to actor {st:+d} ({STANCE_LABEL.get(st,'?')}) · "
                  f"{mp['available']}/{mp['per_week']} MP")
            print(f"      objective: {f.get('objective','(none)')}")
            if step:
                print(f"      running op: {step['text']} (day {step.get('due_day','?')})"
                      " — does this event change it?")
            else:
                print("      running op: NONE — this is the moment to give them one.")
            doctrine = (f.get("reactions", {}).get(args.trigger)
                        or f.get("reactions", {}).get("other"))
            if doctrine:
                print(f"      doctrine: {doctrine}")
            print(f"      record it: factions.py -c <campaign> move {f['id']} "
                  f"--spend 1 --day {learns_on} --text \"...\"")
    if bystanders:
        print("\n  AWARE, NOT COMPELLED (a move here is optional, but they know):")
        for f, learns_on, st in bystanders:
            print(f"    {f['name']} — hears day {learns_on}, stance {st:+d}")
    if deaf:
        print("\n  DOES NOT LEARN (intel too low for a "
              f"{args.visibility} event): " + ", ".join(f['name'] for f in deaf))

    if args.record:
        for f, learns_on, _ in responders + bystanders:
            f.setdefault("knows", []).append({"day": learns_on, "fact": args.event,
                                              "via": f"{args.visibility} ({args.trigger})"})
        _save(campaign, data)
        print("\n  (recorded in each faction's Knows ledger)")
    print()


def cmd_sweep(campaign: str, day: int) -> None:
    """End-of-session pass: force the forward question for every active faction."""
    data = _load(campaign)
    active = [f for f in data["factions"] if f.get("status", "active") == "active"]
    print(f"\n  FACTION SWEEP — day {day}")
    print("  For each: what is their NEXT step, by WHEN, and what would make them")
    print("  abandon it? 'They watch and wait' is not an answer — it costs a week")
    print("  of move points and has to be written as a decision, with a reason.\n")
    for f in active:
        mp = _mp(f)
        step = _next_step(f)
        last = _last_move_day(f)
        print(f"  {f['name']}  [{f['id']}]  {mp['available']}/{mp['per_week']} MP"
              f"  · last move: " + (f"day {last}" if last else "never"))
        print(f"    objective : {f.get('objective','(none set)')}")
        print(f"    next step : " + (f"{step['text']} (day {step.get('due_day','?')})"
                                     if step else "NONE — set one now"))
        if f.get("assets"):
            print(f"    can spend : {'; '.join(f['assets'][:3])}")
        print()
    sys.exit(0)


def cmd_check(campaign: str, day: int) -> None:
    """Quiet unless something needs attention — for /dm:dnd load and save."""
    data = _load(campaign)
    active = [f for f in data["factions"] if f.get("status", "active") == "active"]
    if not active:
        print("  factions.json has no active factions — nothing to check.")
        return
    problems = []
    for f in active:
        step = _next_step(f)
        if not step:
            problems.append(f"{f['name']}: no operation running")
        elif step.get("due_day") is not None and step["due_day"] < day:
            problems.append(f"{f['name']}: step overdue since day {step['due_day']} — "
                            f"{step['text']}")
        last = _last_move_day(f)
        if last is not None and day - last >= IDLE_DAYS:
            problems.append(f"{f['name']}: no move in {day - last} days")
    if problems:
        print("  " + "=" * 64)
        print(f"  !!! FACTION BOARD NEEDS A MOVE ({len(problems)}) — day {day}")
        print("  " + "=" * 64)
        for p in problems:
            print(f"    {p}")
        print("  Run `factions.py -c <campaign> sweep --day N` to work through them.")
        sys.exit(2)
    print(f"  faction board OK — {len(active)} active, all with a live operation.")


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="Faction plans, costs, intel and reactions")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    lst = sub.add_parser("list", help="One line per faction")
    lst.add_argument("--all", action="store_true", help="Include dormant factions")

    shw = sub.add_parser("show", help="Full record for one faction")
    shw.add_argument("id")

    add = sub.add_parser("add", help="Create a faction record")
    add.add_argument("--id", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--objective", default="")
    add.add_argument("--power", default="2", help="1-5; sets the weekly move-point budget")
    add.add_argument("--intel", default="1", help="0-3; how fast they learn things")
    add.add_argument("--status", default="active", choices=["active", "dormant"])
    add.add_argument("--assets", default="", help="Semicolon-separated")

    st = sub.add_parser("set", help="Edit a faction record")
    st.add_argument("id")
    st.add_argument("--objective", default="")
    st.add_argument("--status", default="", choices=["", "active", "dormant"])
    st.add_argument("--intel", default="")
    st.add_argument("--power", default="")
    st.add_argument("--assets", default="")
    st.add_argument("--reaction", default="", metavar="TRIGGER=TEXT",
                    help="e.g. alliance=\"Answers an alliance by buying the other side's debt\"")

    stn = sub.add_parser("stance", help="Set how one faction stands toward another (or 'party')")
    stn.add_argument("--from", required=True, dest="from")
    stn.add_argument("--to", required=True)
    stn.add_argument("--level", required=True, help="-3..+3")
    stn.add_argument("--mutual", action="store_true", help="Set the reverse stance too")

    op = sub.add_parser("op", help="Set the running operation")
    op.add_argument("id")
    op.add_argument("--name", default="")
    op.add_argument("--step", action="append", default=[], metavar="TEXT@DAY")
    op.add_argument("--abandon-if", default="", dest="abandon_if")

    stp = sub.add_parser("step", help="Mark an operation step done")
    stp.add_argument("id")
    stp.add_argument("number", type=int)
    stp.add_argument("--undo", action="store_true")

    mv = sub.add_parser("move", help="Record a move and spend its cost")
    mv.add_argument("id")
    mv.add_argument("--text", required=True)
    mv.add_argument("--spend", default="1")
    mv.add_argument("--day", type=int, required=True)

    tk = sub.add_parser("tick", help="Refresh weekly budgets, surface due/overdue steps")
    tk.add_argument("--day", type=int, required=True)

    rc = sub.add_parser("react", help="Who hears this, who must answer it, and how")
    rc.add_argument("--actor", required=True, help="Faction id at the centre of the event")
    rc.add_argument("--event", required=True)
    rc.add_argument("--trigger", default="other", choices=TRIGGERS)
    rc.add_argument("--visibility", default="rumored", choices=sorted(VISIBILITY))
    rc.add_argument("--day", type=int, required=True)
    rc.add_argument("--record", action="store_true", help="Write it into each Knows ledger")

    sw = sub.add_parser("sweep", help="End-of-session pass over every active faction")
    sw.add_argument("--day", type=int, required=True)

    ck = sub.add_parser("check", help="Loud flags for /dm:dnd load and save")
    ck.add_argument("--day", type=int, required=True)

    args = p.parse_args()
    c = args.campaign

    if args.cmd == "list":      cmd_list(c, args.all)
    elif args.cmd == "show":    cmd_show(c, args.id)
    elif args.cmd == "add":     cmd_add(c, args)
    elif args.cmd == "set":     cmd_set(c, args)
    elif args.cmd == "stance":  cmd_stance(c, args)
    elif args.cmd == "op":      cmd_op(c, args)
    elif args.cmd == "step":    cmd_step(c, args)
    elif args.cmd == "move":    cmd_move(c, args)
    elif args.cmd == "tick":    cmd_tick(c, args.day)
    elif args.cmd == "react":   cmd_react(c, args)
    elif args.cmd == "sweep":   cmd_sweep(c, args.day)
    elif args.cmd == "check":   cmd_check(c, args.day)


if __name__ == "__main__":
    main()
