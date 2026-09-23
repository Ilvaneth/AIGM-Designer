#!/usr/bin/env python3
"""
calendar.py — in-world date and time manager

Handles time advancement for any campaign calendar — including fully custom
systems (Harvestmoon, Deepwinter, etc.). Stores the current date/time as a
structured object so arithmetic is always consistent.

The calendar is defined per-campaign in world.md under ## World Foundations →
Calendar. Run `calendar.py init` once to register it; all subsequent commands
use the stored definition.

Time is tracked to the minute, because a day is spent in scenes that cost less
than an hour — a conversation, a walk across town, a shop visit. A tool that
could only count whole hours meant those scenes advanced nothing, and the clock
sat at breakfast while the party worked through a full day.

Usage:
    # One-time setup (from the world.md calendar block):
    python3 calendar.py -c <campaign> init \
        --date "15 Harvestmoon 1247" \
        --time "morning" \
        --months "Frostfall,Deepwinter,Thawmonth,Seedtime,Bloomtide,Highsun,Harvestmoon,Duskfall" \
        --month-length 30 \
        --day-names "Sunday,Moonday,Ironday,Windday,Earthday,Fireday,Starday"

    # Advance time
    python3 calendar.py -c <campaign> advance 45 minutes
    python3 calendar.py -c <campaign> advance 8 hours
    python3 calendar.py -c <campaign> advance 2 days

    # Advance by what a scene actually costs (see `scene --list`)
    python3 calendar.py -c <campaign> scene conversation
    python3 calendar.py -c <campaign> scene meeting
    python3 calendar.py -c <campaign> scene research --minutes 240

    # Rest shortcuts
    python3 calendar.py -c <campaign> rest short    # +1 hour
    python3 calendar.py -c <campaign> rest long     # +8 hours

    # Show current date/time (plus the campaign day counter and plane state)
    python3 calendar.py -c <campaign> now
    python3 calendar.py -c <campaign> stateline     # the line to paste into state.md
    python3 calendar.py -c <campaign> check         # compare state.md against this clock

    # Other planes — time may run at a different rate than the material plane
    python3 calendar.py -c <campaign> plane enter "The Ember Court" --rate 3
    python3 calendar.py -c <campaign> plane enter "Feywild" --rate-range 0.5:30
    python3 calendar.py -c <campaign> plane status
    python3 calendar.py -c <campaign> plane exit

    # Set date/time directly (use after manual world.md edits)
    python3 calendar.py -c <campaign> set "22 Harvestmoon 1247" midday --day-counter 203

    # Time of day only
    python3 calendar.py -c <campaign> time <morning|midday|afternoon|evening|night|midnight>

    # List upcoming events (from world.md — entered at init or updated manually)
    python3 calendar.py -c <campaign> events
"""

import json
import os
import random
import re
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

from paths import find_campaign as _find_campaign

# Time of day labels and approximate hour ranges
TIMES_OF_DAY = [
    ("midnight",    0,  1),
    ("early morning", 1, 5),
    ("morning",     6,  10),
    ("midday",      11, 13),
    ("afternoon",   14, 17),
    ("evening",     18, 21),
    ("night",       22, 23),
]

HOURS_PER_TIME = {
    "midnight":      0,
    "early morning": 3,
    "morning":       8,
    "midday":        12,
    "afternoon":     15,
    "evening":       19,
    "night":         22,
}

# What a scene costs in minutes. These are defaults to be overridden with
# --minutes whenever the fiction says otherwise; the point is that every scene
# has a cost and none of them is zero.
SCENE_COSTS = {
    "brief":         10,   # a greeting, a handoff, a question in passing
    "conversation":  30,   # sitting down with someone
    "negotiation":   60,   # haggling, terms, a deal being struck
    "meeting":       90,   # a formal audience, a council session
    "interrogation": 60,
    "search":        10,   # searching one room
    "investigation": 60,   # working a scene or a question properly
    "research":     180,   # a library, an archive, a laboratory
    "shopping":      45,
    "crosstown":     30,   # moving across a city or settlement
    "meal":          60,
    "summit":       240,   # a negotiation that decides something big
    "feast":        240,   # a banquet, a coronation, a public ceremony
    "ritual":        60,
    "craft":        240,
    "watch":        240,   # one watch of a night
    "combat":         5,   # a fight is minutes, but it is not zero
    "downtime":      60,   # generic hour of unstructured time
}


def _cal_path(campaign: str) -> str:
    d = str(_find_campaign(campaign))
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "calendar.json")


def _load(campaign: str) -> dict:
    try:
        with open(_cal_path(campaign), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(campaign: str, cal: dict) -> None:
    with open(_cal_path(campaign), "w", encoding="utf-8") as f:
        json.dump(cal, f, indent=2, ensure_ascii=False)


def _month_length(cal: dict) -> int:
    return cal.get("month_length", 30)


def _month_list(cal: dict) -> list:
    return cal.get("months", [])


def _day_names(cal: dict) -> list:
    return cal.get("day_names", [])


def _tod(hour: int) -> str:
    for label, lo, hi in TIMES_OF_DAY:
        if lo <= hour <= hi:
            return label
    return "night"


def _weekday(cal: dict) -> str:
    days = _day_names(cal)
    if not days:
        return ""
    return days[(cal.get("day", 1) - 1) % len(days)]


def _month_name(cal: dict) -> str:
    months = _month_list(cal)
    month = cal.get("month", 1)
    if months and 1 <= month <= len(months):
        return months[month - 1]
    return f"Month {month}"


def _clock(cal: dict) -> str:
    return f"{cal.get('hour', 8):02d}:{cal.get('minute', 0):02d}"


def _format_date(cal: dict) -> str:
    """Human-readable current date/time, with the campaign day counter."""
    weekday = _weekday(cal)
    prefix = f"{weekday}, " if weekday else ""
    line = (f"{prefix}{cal.get('day', 1)} {_month_name(cal)} {cal.get('year', 1)} — "
            f"{_tod(cal.get('hour', 8))} ({_clock(cal)})")
    if cal.get("day_counter") is not None:
        line += f"  [Day {cal['day_counter']}]"
    return line


def _abs_day(cal: dict) -> int:
    """Absolute day index, so two dates can be subtracted."""
    months = _month_list(cal)
    num_months = len(months) if months else 12
    month_len = _month_length(cal)
    return ((cal.get("year", 1) * num_months + (cal.get("month", 1) - 1)) * month_len
            + cal.get("day", 1))


def _advance_material(cal: dict, minutes: int) -> int:
    """Advance the material-plane clock. Returns the number of days rolled."""
    cal.setdefault("hour", 8)
    cal.setdefault("minute", 0)
    cal.setdefault("day", 1)
    cal.setdefault("month", 1)
    cal.setdefault("year", 1)

    cal["minute"] += int(minutes)
    days_rolled = 0

    cal["hour"] += cal["minute"] // 60
    cal["minute"] %= 60

    while cal["hour"] >= 24:
        cal["hour"] -= 24
        cal["day"] += 1
        days_rolled += 1
        if cal.get("day_counter") is not None:
            cal["day_counter"] += 1

    month_len = _month_length(cal)
    months = _month_list(cal)
    num_months = len(months) if months else 12
    while cal["day"] > month_len:
        cal["day"] -= month_len
        cal["month"] += 1
        if cal["month"] > num_months:
            cal["month"] = 1
            cal["year"] += 1

    return days_rolled


def _fmt_span(minutes: int) -> str:
    minutes = int(round(minutes))
    if minutes < 60:
        return f"{minutes}m"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {mins:02d}m" if mins else f"{hours}h"
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h" if hours else f"{days}d"


def _advance(cal: dict, minutes: int) -> str:
    """Advance time by `minutes` of EXPERIENCED (local) time.

    On the material plane local and material time are the same thing. On
    another plane the party experiences `minutes` while the material world
    advances `minutes * rate` — so a party that spends six hours in a plane
    running at rate 3 comes home eighteen hours later.
    """
    plane = cal.get("plane")
    before = (cal.get("hour", 8), _tod(cal.get("hour", 8)))

    if plane:
        rate = float(plane.get("rate", 1.0))
        plane["local_minutes"] = plane.get("local_minutes", 0) + int(minutes)
        material = minutes * rate
        plane["material_minutes"] = plane.get("material_minutes", 0) + material
        # Carry the fractional remainder so repeated small scenes do not erode.
        carry = plane.get("carry", 0.0) + material
        whole = int(carry)
        plane["carry"] = carry - whole
        _advance_material(cal, whole)
        note = (f"  {plane.get('name', 'plane')}: +{_fmt_span(minutes)} local "
                f"(rate x{rate:g} -> +{_fmt_span(material)} material)")
    else:
        _advance_material(cal, minutes)
        note = ""

    after_tod = _tod(cal.get("hour", 8))
    shift = f"  ({before[1]} -> {after_tod})" if before[1] != after_tod else ""
    return (note + ("\n" if note else "")) + f"  -> {_format_date(cal)}{shift}"


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_init(campaign: str, args) -> None:
    cal: dict = {}

    date_str = args.date
    try:
        parts = date_str.split()
        if len(parts) >= 3:
            month_name = parts[1]
            cal["day"]  = int(parts[0])
            cal["year"] = int(parts[2])
        elif len(parts) == 2:
            month_name = parts[1]
            cal["day"]  = int(parts[0])
            cal["year"] = 1
        else:
            cal["day"]  = 1
            month_name  = date_str
            cal["year"] = 1

        months = [m.strip() for m in args.months.split(",") if m.strip()] if args.months else []
        cal["months"] = months
        cal["month"] = 1
        for i, m in enumerate(months):
            if m.lower() == month_name.lower():
                cal["month"] = i + 1
                break
    except (ValueError, IndexError):
        cal.update({"day": 1, "month": 1, "year": 1, "months": []})

    cal["hour"]         = HOURS_PER_TIME.get(args.time or "morning", 8)
    cal["minute"]       = 0
    cal["month_length"] = int(args.month_length) if args.month_length else 30
    cal["day_names"]    = [d.strip() for d in args.day_names.split(",") if d.strip()] if args.day_names else []
    cal["day_counter"]  = int(args.day_counter) if getattr(args, "day_counter", None) else 1
    cal["events"]       = []
    cal["plane"]        = None

    _save(campaign, cal)
    print(f"Calendar initialised: {_format_date(cal)}")


UNIT_MINUTES = {
    "minute": 1, "minutes": 1, "min": 1, "mins": 1,
    "hour": 60, "hours": 60,
    "day": 1440, "days": 1440,
    "week": 10080, "weeks": 10080,
}


def _require(campaign: str) -> dict:
    cal = _load(campaign)
    if not cal:
        print("Calendar not initialised. Run `calendar.py -c <campaign> init` first.")
        sys.exit(1)
    return cal


def cmd_advance(campaign: str, amount: int, unit: str) -> None:
    cal = _require(campaign)
    minutes = amount * UNIT_MINUTES.get(unit, 60)
    out = _advance(cal, minutes)
    _save(campaign, cal)
    print(f"  +{amount} {unit}")
    print(out)


def cmd_scene(campaign: str, kind: str, minutes: "int | None") -> None:
    cal = _require(campaign)
    cost = minutes if minutes is not None else SCENE_COSTS.get(kind)
    if cost is None:
        print(f"  Unknown scene type '{kind}'. Known types:")
        for name, value in sorted(SCENE_COSTS.items(), key=lambda kv: kv[1]):
            print(f"    {name:<14} {_fmt_span(value)}")
        print("  Pass --minutes N for anything else.")
        sys.exit(1)
    out = _advance(cal, cost)
    _save(campaign, cal)
    print(f"  scene: {kind} (+{_fmt_span(cost)})")
    print(out)


def cmd_rest(campaign: str, rest_type: str) -> None:
    cal = _require(campaign)
    minutes = 60 if rest_type == "short" else 480
    out = _advance(cal, minutes)
    _save(campaign, cal)
    print(f"  {rest_type.capitalize()} rest (+{_fmt_span(minutes)})")
    print(out)


def cmd_now(campaign: str) -> None:
    cal = _load(campaign)
    if not cal:
        print("Calendar not initialised. Run `calendar.py -c <campaign> init` first.")
        return
    print(_format_date(cal))
    plane = cal.get("plane")
    if plane:
        print(f"  ON ANOTHER PLANE — {plane.get('name', '?')} "
              f"(rate x{float(plane.get('rate', 1)):g})")
        print(f"  local elapsed: {_fmt_span(plane.get('local_minutes', 0))}"
              f"   material elapsed: {_fmt_span(plane.get('material_minutes', 0))}")
        print(f"  entered at: {plane.get('entered_at', '?')}")


def cmd_stateline(campaign: str) -> None:
    """Print the canonical date line for state.md, so it is copied, not composed."""
    cal = _require(campaign)
    plane = cal.get("plane")
    line = f"- **In-world date:** {_format_date(cal)}"
    if plane:
        line += (f"  ·  on **{plane.get('name')}** (rate x{float(plane.get('rate', 1)):g}, "
                 f"local {_fmt_span(plane.get('local_minutes', 0))})")
    print(line)


_DATE_IN_LINE = re.compile(r"(\d{1,3})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(\d{3,4})")
_DAY_IN_LINE = re.compile(r"(?:Day|Gün|gün)\s*(\d{1,4})")


def cmd_check(campaign: str) -> None:
    """Compare state.md's stated date against this calendar and report drift."""
    cal = _require(campaign)
    state_path = os.path.join(str(_find_campaign(campaign)), "state.md")
    try:
        with open(state_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"  ! cannot read state.md: {e}")
        sys.exit(1)

    lines = [l for l in text.splitlines() if "In-world date" in l]
    if not lines:
        print("  ! state.md has no '**In-world date:**' line — add one from `stateline`.")
        sys.exit(1)

    problems = []
    for line in lines:
        date_m = _DATE_IN_LINE.search(line)
        day_m = _DAY_IN_LINE.search(line)
        if date_m:
            day, month, year = int(date_m.group(1)), date_m.group(2), int(date_m.group(3))
            if (day, month.lower(), year) != (cal.get("day"), _month_name(cal).lower(), cal.get("year")):
                problems.append(f"date in state.md: {day} {month} {year}  !=  calendar: "
                                f"{cal.get('day')} {_month_name(cal)} {cal.get('year')}")
        if day_m and cal.get("day_counter") is not None:
            if int(day_m.group(1)) != cal["day_counter"]:
                problems.append(f"day counter in state.md: {day_m.group(1)}  !=  "
                                f"calendar: {cal['day_counter']}")

    if problems:
        print("  " + "=" * 64)
        print("  !!! CLOCK DRIFT — state.md and calendar.json disagree")
        print("  " + "=" * 64)
        for p in dict.fromkeys(problems):
            print(f"    {p}")
        print("  Fix by advancing the calendar to the true time, or `set` it, then")
        print("  paste `calendar.py -c <campaign> stateline` into state.md.")
        sys.exit(2)
    print(f"  clock OK — {_format_date(cal)}")


def cmd_plane(campaign: str, args) -> None:
    cal = _require(campaign)
    action = args.action

    if action == "status":
        plane = cal.get("plane")
        if not plane:
            print("  Material plane — time runs 1:1.")
        else:
            rate = float(plane.get("rate", 1))
            print(f"  {plane.get('name')} — rate x{rate:g}")
            print(f"  local elapsed: {_fmt_span(plane.get('local_minutes', 0))}"
                  f"   material elapsed: {_fmt_span(plane.get('material_minutes', 0))}")
            print(f"  entered at: {plane.get('entered_at', '?')}")
        return

    if action == "rate":
        plane = cal.get("plane")
        if not plane:
            print("  ! not on another plane.")
            sys.exit(1)
        if not args.rate:
            print("  ! give the new rate: plane rate --rate 3")
            sys.exit(1)
        old = float(plane.get("rate", 1))
        plane["rate"] = float(args.rate)
        _save(campaign, cal)
        print(f"  {plane.get('name')} rate x{old:g} -> x{plane['rate']:g} "
              f"(applies to time from here on; elapsed so far is unchanged)")
        return

    if action == "enter":
        if cal.get("plane"):
            print(f"  ! already on {cal['plane'].get('name')} — exit first.")
            sys.exit(1)
        rate = float(args.rate) if args.rate else 1.0
        rolled = ""
        if args.rate_range:
            try:
                lo, hi = (float(x) for x in args.rate_range.split(":"))
            except ValueError:
                print("  ! --rate-range wants LOW:HIGH, e.g. 0.5:30")
                sys.exit(1)
            rate = round(random.uniform(lo, hi), 2)
            rolled = f" (rolled from {lo:g}:{hi:g})"
        cal["plane"] = {
            "name": args.name,
            "rate": rate,
            "local_minutes": 0,
            "material_minutes": 0,
            "carry": 0.0,
            "entered_at": _format_date(cal),
        }
        _save(campaign, cal)
        print(f"  Entered {args.name} — time runs x{rate:g} faster outside{rolled}.")
        print(f"  Material clock at entry: {_format_date(cal)}")
        print("  From here, `advance`/`scene` count the time the PARTY experiences;")
        print("  the material clock moves by that amount times the rate.")
        return

    # exit
    plane = cal.get("plane")
    if not plane:
        print("  ! not on another plane.")
        sys.exit(1)
    local = plane.get("local_minutes", 0)
    material = plane.get("material_minutes", 0)
    cal["plane"] = None
    _save(campaign, cal)
    print(f"  Left {plane.get('name')} (rate x{float(plane.get('rate', 1)):g})")
    print(f"  Experienced there: {_fmt_span(local)}")
    print(f"  Passed in the world: {_fmt_span(material)}")
    print(f"  Entered at: {plane.get('entered_at', '?')}")
    print(f"  Now:        {_format_date(cal)}")


def cmd_set(campaign: str, args) -> None:
    cal = _load(campaign)
    if not cal:
        cal = {"months": [], "day_names": [], "month_length": 30, "events": [], "plane": None}

    months = cal.get("months", [])
    had_date = cal.get("day") is not None
    before = _abs_day(cal) if had_date else None
    try:
        parts = args.date.split()
        if len(parts) >= 3:
            month_name = parts[1]
            cal["day"]  = int(parts[0])
            cal["year"] = int(parts[2])
            cal["month"] = 1
            for i, m in enumerate(months):
                if m.lower() == month_name.lower():
                    cal["month"] = i + 1
                    break
        elif len(parts) == 1:
            cal["day"] = int(parts[0])
    except (ValueError, IndexError):
        pass

    if args.time:
        cal["hour"] = HOURS_PER_TIME.get(args.time.lower(), cal.get("hour", 8))
        cal["minute"] = 0
    if args.clock:
        try:
            hh, mm = args.clock.split(":")
            cal["hour"], cal["minute"] = int(hh), int(mm)
        except ValueError:
            print("  ! --clock wants HH:MM")
            sys.exit(1)
    # The campaign day counter has to move with the date. Setting a date
    # forward without it silently desynchronises the two, which is exactly how
    # a declared "ten days from now" ends up dated wrong and then skipped twice.
    shift = 0
    if args.day_counter:
        cal["day_counter"] = int(args.day_counter)
    elif had_date and cal.get("day_counter") is not None:
        shift = _abs_day(cal) - before
        cal["day_counter"] += shift

    _save(campaign, cal)
    print(f"  Date set: {_format_date(cal)}")
    if shift:
        print(f"  day counter moved {shift:+d} with the date")
    if shift > 0:
        print(f"  NOTE: `set` jumps the clock without running anything else. For time the")
        print(f"        party actually lives through, use `advance {shift} days` instead —")
        print(f"        and run `factions.py tick` for the days just skipped, or the world")
        print(f"        stands still across the jump.")


def cmd_time(campaign: str, time_str: str) -> None:
    cal = _require(campaign)
    cal["hour"] = HOURS_PER_TIME.get(time_str.lower(), cal.get("hour", 8))
    cal["minute"] = 0
    _save(campaign, cal)
    print(f"  Time set: {_format_date(cal)}")


def cmd_events(campaign: str) -> None:
    cal = _load(campaign)
    events = cal.get("events", [])
    if not events:
        print("  No upcoming events registered.")
        print("  Add events by editing <campaign>/calendar.json")
        print('  Events format: [{"name": "Festival of Stars", "date": "1 Bloomtide 1248"}]')
    else:
        print("Upcoming events:")
        for e in events:
            print(f"  {e.get('date','?')} — {e.get('name','?')}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="In-world calendar manager")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    ini = sub.add_parser("init", help="Initialise campaign calendar (run once)")
    ini.add_argument("--date",         default="1 Month 1")
    ini.add_argument("--time",         default="morning")
    ini.add_argument("--months",       default="")
    ini.add_argument("--month-length", default="30")
    ini.add_argument("--day-names",    default="")
    ini.add_argument("--day-counter",  default="1",
                     help="Campaign day number for this date (day 1 = first day of play)")

    adv = sub.add_parser("advance", help="Advance time by amount")
    adv.add_argument("amount", type=int)
    adv.add_argument("unit", choices=sorted(UNIT_MINUTES))

    scn = sub.add_parser("scene", help="Advance by what a scene costs (see --list)")
    scn.add_argument("kind", nargs="?", default="",
                     help="brief | conversation | negotiation | meeting | interrogation | "
                          "search | investigation | research | shopping | crosstown | meal | "
                          "ritual | craft | watch | combat | downtime")
    scn.add_argument("--minutes", type=int, default=None, help="Override the default cost")
    scn.add_argument("--list", action="store_true", help="Print the cost table and exit")

    rst = sub.add_parser("rest", help="Advance time for a short or long rest")
    rst.add_argument("type", choices=["short", "long"])

    sub.add_parser("now", help="Print current date/time")
    sub.add_parser("stateline", help="Print the canonical date line for state.md")
    sub.add_parser("check", help="Compare state.md's date against this calendar")

    pln = sub.add_parser("plane", help="Track time on another plane")
    pln.add_argument("action", choices=["enter", "exit", "status", "rate"])
    pln.add_argument("name", nargs="?", default="", help="Plane name (for enter)")
    pln.add_argument("--rate", default="", help="Material minutes per local minute (1 = same)")
    pln.add_argument("--rate-range", default="", help="Roll the rate once, e.g. 0.5:30")

    st = sub.add_parser("set", help="Set the current date/time directly")
    st.add_argument("date", help="Date string, e.g. '22 Harvestmoon 1247'")
    st.add_argument("time", nargs="?", default="", help="Time of day label")
    st.add_argument("--clock", default="", help="Exact time as HH:MM")
    st.add_argument("--day-counter", default="", help="Campaign day number")

    tm = sub.add_parser("time", help="Set time of day without changing the date")
    tm.add_argument("tod", choices=sorted(HOURS_PER_TIME))

    sub.add_parser("events", help="List upcoming calendar events")

    args = p.parse_args()

    if args.cmd == "init":
        cmd_init(args.campaign, args)
    elif args.cmd == "advance":
        cmd_advance(args.campaign, args.amount, args.unit)
    elif args.cmd == "scene":
        if args.list or not args.kind:
            print("  Scene costs (override with --minutes N):")
            for name, value in sorted(SCENE_COSTS.items(), key=lambda kv: kv[1]):
                print(f"    {name:<14} {_fmt_span(value)}")
            return
        cmd_scene(args.campaign, args.kind, args.minutes)
    elif args.cmd == "rest":
        cmd_rest(args.campaign, args.type)
    elif args.cmd == "now":
        cmd_now(args.campaign)
    elif args.cmd == "stateline":
        cmd_stateline(args.campaign)
    elif args.cmd == "check":
        cmd_check(args.campaign)
    elif args.cmd == "plane":
        cmd_plane(args.campaign, args)
    elif args.cmd == "set":
        cmd_set(args.campaign, args)
    elif args.cmd == "time":
        cmd_time(args.campaign, args.tod)
    elif args.cmd == "events":
        cmd_events(args.campaign)


if __name__ == "__main__":
    main()
