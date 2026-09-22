#!/usr/bin/env python3
"""
tracker.py — session-state tracker for conditions, concentration, effects, and death saves

Stores state per-campaign and prints formatted status to the terminal.

Usage:
    CAMPAIGN=my-campaign

    # Conditions (5e SRD: blinded, charmed, deafened, exhausted, frightened,
    #   grappled, incapacitated, invisible, paralyzed, petrified, poisoned,
    #   prone, restrained, stunned, unconscious)
    python3 tracker.py -c $CAMPAIGN condition add <entity> <condition>
    python3 tracker.py -c $CAMPAIGN condition remove <entity> <condition>
    python3 tracker.py -c $CAMPAIGN condition clear <entity>

    # Concentration (one spell at a time per caster; auto-clears previous)
    python3 tracker.py -c $CAMPAIGN concentrate <entity> "<spell name>"
    python3 tracker.py -c $CAMPAIGN concentrate <entity> break

    # Timed effects — duration formats: 10r (rounds), 60m (minutes), 8h (hours), indef
    python3 tracker.py -c $CAMPAIGN effect start <entity> "<spell>" <duration> [conc]
    python3 tracker.py -c $CAMPAIGN effect end   <entity> "<spell>"
    python3 tracker.py -c $CAMPAIGN effect tick  <entity>   # rounds-only; use `turn` instead for a PC's own turn

    # Death saves (PC only — 3 successes = stable, 3 failures = dead)
    python3 tracker.py -c $CAMPAIGN saves <entity> success
    python3 tracker.py -c $CAMPAIGN saves <entity> failure
    python3 tracker.py -c $CAMPAIGN saves <entity> stable   # manually mark stable
    python3 tracker.py -c $CAMPAIGN saves <entity> reset    # regain consciousness

    # Status display
    python3 tracker.py -c $CAMPAIGN status [entity]   # all entities or one

    # Clear (end of encounter — wipes conditions/concentrations/effects; preserves saves)
    python3 tracker.py -c $CAMPAIGN clear [--all]     # --all also clears saves

    # Combat Triggers — prints the "## Combat Triggers" section straight from a
    # PC's own character file. Run this for every PC the instant combat.py init
    # is called for a scene — it's the mechanical backstop for SKILL-combat.md's
    # "crit/kill bonus actions and reactions never offer themselves" rule: the
    # DM shouldn't have to remember a feature buried in a long sheet mid-fight
    # when a one-line command can just print it back.
    python3 tracker.py -c $CAMPAIGN triggers <character-name>   # one PC
    python3 tracker.py -c $CAMPAIGN triggers --all              # every PC in characters/

    # Turn start (PCs only) — THE mandatory call at the start of every PC turn.
    # Merges `effect tick` + `triggers <name>` into one command so there is no
    # longer a separate "did I remember to re-check triggers this round" step
    # to forget — running this IS how a PC's turn starts, full stop. Added
    # 2026-09-14 after the DM repeatedly re-read triggers once at combat start
    # and then stopped checking them turn-to-turn (feats/item passives/
    # Ascension gains getting missed mid-fight). No-ops gracefully (prints a
    # note, does nothing else) when called on an NPC/monster name with no
    # matching character sheet.
    python3 tracker.py -c $CAMPAIGN turn <character-name>

    # NPC/monster turn — prints the DEFENSES of the PCs it can act against, so a
    # Cloak of Displacement, a damage immunity or a Counterspell reaction cannot
    # be missed just because the actor is not a PC.
    python3 tracker.py -c $CAMPAIGN turn "Bone Devil" --targets "Kriv Shestendeliath"
    python3 tracker.py -c $CAMPAIGN defense "Ilvaneth Duskmere"
"""

import json
import os
import sys
import argparse
import time
import re
from datetime import datetime, timezone
from paths import find_campaign as _find_campaign

def _state_path(campaign: str) -> str:
    d = str(_find_campaign(campaign))
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "tracker.json")


def _load(campaign: str) -> dict:
    path = _state_path(campaign)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(campaign: str, state: dict) -> None:
    with open(_state_path(campaign), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _entity(state: dict, name: str) -> dict:
    """Get or create an entity entry."""
    key = name.lower()
    if key not in state:
        state[key] = {
            "name": name,
            "conditions": [],
            "concentration": None,
            "effects": [],
            "death_saves": {"successes": 0, "failures": 0, "stable": False},
        }
    # Backfill effects key for older entries
    state[key].setdefault("effects", [])
    return state[key]


def _parse_duration(dur_str: str) -> "dict | None":
    """Parse a duration string into an effect dict fragment.
    Formats: 10r (rounds), 60m (minutes), 8h (hours), indef (indefinite).
    Returns None on bad input.
    """
    d = dur_str.strip().lower()
    if d.endswith("r"):
        try:
            return {"duration_type": "rounds", "duration_remaining": int(d[:-1])}
        except ValueError:
            return None
    elif d.endswith("m"):
        try:
            secs = int(d[:-1]) * 60
            return {"duration_type": "minutes", "duration_seconds": secs, "started_at": time.time()}
        except ValueError:
            return None
    elif d.endswith("h"):
        try:
            secs = int(d[:-1]) * 3600
            return {"duration_type": "hours", "duration_seconds": secs, "started_at": time.time()}
        except ValueError:
            return None
    elif d == "indef":
        return {"duration_type": "indefinite"}
    return None


def _fmt_effect(eff: dict) -> str:
    """Return a short human-readable remaining-duration string."""
    dt = eff.get("duration_type", "indefinite")
    if dt == "rounds":
        r = eff.get("duration_remaining", 0)
        return f"{r} rnd"
    elif dt in ("minutes", "hours"):
        elapsed = time.time() - eff.get("started_at", time.time())
        remaining = max(0, eff.get("duration_seconds", 0) - elapsed)
        if remaining <= 0:
            return "expired"
        m, s = divmod(int(remaining), 60)
        if m >= 60:
            h, m = divmod(m, 60)
            return f"{h}h {m}m"
        return f"{m}:{s:02d}"
    return "∞"


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_effect(campaign: str, action: str, entity_name: str,
               spell: str = "", duration: str = "", is_conc: bool = False) -> None:
    state = _load(campaign)
    ent   = _entity(state, entity_name)

    if action == "start":
        if not spell or not duration:
            print("  error: effect start requires <entity> <spell> <duration>")
            return
        dur = _parse_duration(duration)
        if dur is None:
            print(f"  error: bad duration '{duration}' — use 10r / 60m / 8h / indef")
            return

        effect = {"name": spell, "concentration": is_conc, **dur}

        # Replace any existing effect with same name
        ent["effects"] = [e for e in ent["effects"] if e["name"].lower() != spell.lower()]
        ent["effects"].append(effect)

        # Mirror concentration into the concentrate field
        if is_conc:
            old = ent.get("concentration")
            ent["concentration"] = spell
            if old and old.lower() != spell.lower():
                print(f"  {entity_name}: dropped concentration on '{old}'")

        rem = _fmt_effect(effect)
        conc_tag = " [conc]" if is_conc else ""
        print(f"  + {entity_name}: {spell}{conc_tag} · {rem}")
        _save(campaign, state)

    elif action == "end":
        if not spell:
            print("  error: effect end requires <entity> <spell>")
            return
        before = len(ent["effects"])
        removed = [e for e in ent["effects"] if e["name"].lower() == spell.lower()]
        ent["effects"] = [e for e in ent["effects"] if e["name"].lower() != spell.lower()]
        if not removed:
            print(f"  ({entity_name} has no active effect '{spell}')")
            _save(campaign, state)
            return
        was_conc = any(e.get("concentration") for e in removed)
        if was_conc and (ent.get("concentration") or "").lower() == spell.lower():
            ent["concentration"] = None
            print(f"  - {entity_name}: {spell} ends (concentration broken)")
        else:
            print(f"  - {entity_name}: {spell} ends")
        _save(campaign, state)

    elif action == "tick":
        # Advance one round for this entity — decrement rounds, flag expired
        effects = ent.get("effects", [])
        kept, expired = [], []
        time_expired = []

        for e in effects:
            dt = e.get("duration_type")
            if dt == "rounds":
                e = dict(e)
                e["duration_remaining"] = max(0, e.get("duration_remaining", 1) - 1)
                if e["duration_remaining"] <= 0:
                    expired.append(e)
                else:
                    kept.append(e)
            elif dt in ("minutes", "hours"):
                elapsed = time.time() - e.get("started_at", time.time())
                remaining = e.get("duration_seconds", 0) - elapsed
                if remaining <= 0:
                    time_expired.append(e)
                else:
                    kept.append(e)
            else:
                kept.append(e)

        all_expired = expired + time_expired
        ent["effects"] = kept

        if not all_expired and not kept:
            # Nothing to report
            _save(campaign, state)
            return

        # Print tick summary
        if kept:
            lines = [f"⧗ {e['name']} · {_fmt_effect(e)}" for e in kept]
            print(f"  {entity_name} — effects: {', '.join(lines)}")

        for e in all_expired:
            was_conc = e.get("concentration", False)
            spell_name = e["name"]
            if was_conc and (ent.get("concentration") or "").lower() == spell_name.lower():
                ent["concentration"] = None
                print(f"  ! {entity_name}: {spell_name} EXPIRED — concentration ends")
            else:
                print(f"  ! {entity_name}: {spell_name} EXPIRED")

        _save(campaign, state)

    else:
        print(f"  error: unknown effect action '{action}' — use start / end / tick")


def cmd_condition(campaign: str, entity_name: str, action: str, condition: str = "") -> None:
    state = _load(campaign)
    ent   = _entity(state, entity_name)
    conds = ent["conditions"]

    if action == "add":
        cond = condition.lower()
        if cond not in conds:
            conds.append(cond)
            print(f"  + {entity_name}: {cond}")
        else:
            print(f"  (already has {cond})")

    elif action == "remove":
        cond = condition.lower()
        if cond in conds:
            conds.remove(cond)
            print(f"  - {entity_name}: {cond} removed")
        else:
            print(f"  ({entity_name} does not have {cond})")

    elif action == "clear":
        conds.clear()
        print(f"  {entity_name}: conditions cleared")

    ent["conditions"] = conds
    _save(campaign, state)


def cmd_concentrate(campaign: str, entity_name: str, spell_or_break: str) -> None:
    state = _load(campaign)
    ent   = _entity(state, entity_name)

    if spell_or_break.lower() == "break":
        old = ent.get("concentration")
        ent["concentration"] = None
        if old:
            print(f"  {entity_name}: concentration on '{old}' broken")
        else:
            print(f"  {entity_name}: was not concentrating")
    else:
        spell = spell_or_break
        old   = ent.get("concentration")
        ent["concentration"] = spell
        if old and old != spell:
            print(f"  {entity_name}: dropped '{old}', now concentrating on '{spell}'")
        else:
            print(f"  {entity_name}: concentrating on '{spell}'")

    _save(campaign, state)


def cmd_saves(campaign: str, entity_name: str, action: str) -> None:
    state = _load(campaign)
    ent   = _entity(state, entity_name)
    saves = ent["death_saves"]

    if action == "success":
        saves["successes"] = min(3, saves["successes"] + 1)
        if saves["successes"] >= 3:
            saves["stable"] = True
            msg = f"{entity_name} is STABLE (3 successes)"
            print(f"  ☑ {msg}")
        else:
            print(f"  {entity_name}: {saves['successes']} success(es), {saves['failures']} failure(s)")

    elif action == "failure":
        saves["failures"] = min(3, saves["failures"] + 1)
        if saves["failures"] >= 3:
            msg = f"{entity_name} — 3 FAILURES: character is DEAD"
            print(f"  ✗ {msg}")
        else:
            print(f"  {entity_name}: {saves['successes']} success(es), {saves['failures']} failure(s)")

    elif action == "stable":
        saves["stable"] = True
        print(f"  {entity_name}: marked stable")

    elif action == "reset":
        saves.update({"successes": 0, "failures": 0, "stable": False})
        print(f"  {entity_name}: death saves reset (regained consciousness)")

    ent["death_saves"] = saves
    _save(campaign, state)


def cmd_status(campaign: str, filter_name: str = "") -> None:
    state = _load(campaign)
    if not state:
        print("  (no tracked entities)")
        return

    entities = list(state.values())
    if filter_name:
        entities = [e for e in entities if filter_name.lower() in e["name"].lower()]

    for ent in entities:
        name   = ent["name"]
        conds  = ent.get("conditions", [])
        conc   = ent.get("concentration")
        saves  = ent.get("death_saves", {})

        effects = ent.get("effects", [])
        parts = []
        if conds:
            parts.append("Conditions: " + ", ".join(c.capitalize() for c in conds))
        if conc:
            parts.append(f"Concentrating: {conc}")
        if effects:
            eff_strs = []
            for e in effects:
                rem = _fmt_effect(e)
                tag = " [conc]" if e.get("concentration") else ""
                eff_strs.append(f"{e['name']}{tag} · {rem}")
            parts.append("Effects: " + ", ".join(eff_strs))
        s = saves.get("successes", 0)
        f = saves.get("failures", 0)
        if s or f:
            stable = " (stable)" if saves.get("stable") else ""
            parts.append(f"Death saves: {s}✓ {f}✗{stable}")

        if parts:
            print(f"  {name}:")
            for p in parts:
                print(f"    {p}")
        else:
            print(f"  {name}: clean")


def cmd_clear(campaign: str, clear_all: bool = False) -> None:
    state = _load(campaign)
    for ent in state.values():
        ent["conditions"] = []
        ent["concentration"] = None
        ent["effects"] = []
        if clear_all:
            ent["death_saves"] = {"successes": 0, "failures": 0, "stable": False}
    _save(campaign, state)
    scope = "all state" if clear_all else "conditions and concentration"
    print(f"  Cleared {scope} for {len(state)} entities.")


def _characters_dir(campaign: str) -> str:
    return os.path.join(str(_find_campaign(campaign)), "characters")


def _extract_section(text: str, heading: str) -> str | None:
    """Return the body of a '## <heading>' section, or None if absent."""
    m = re.search(r'^##\s*' + re.escape(heading) + r'\s*$(.*?)(?=^##\s|\Z)',
                  text, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return None
    return m.group(1).strip("\n")


def _extract_triggers_section(text: str) -> str | None:
    """Return the body of a '## Combat Triggers' section, or None if absent."""
    return _extract_section(text, "Combat Triggers")


def _print_one_triggers(name: str, path: str) -> bool:
    """Print one character's Combat Triggers + Passive Item Effects sections.
    Returns True if either was found."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"  ! Could not read {path}: {e}")
        return False

    combat_body = _extract_section(text, "Combat Triggers")
    items_body = _extract_section(text, "Passive Item Effects — Quick Reference")

    print(f"\n{'='*68}")
    print(f"  COMBAT TRIGGERS — {name}")
    print(f"{'='*68}")
    if combat_body:
        print(combat_body)
    else:
        print("  (no '## Combat Triggers' section in this character's sheet yet —")
        print("   nothing mechanical to check beyond the general SKILL-combat.md rules.)")
    print()

    print(f"{'='*68}")
    print(f"  PASSIVE ITEM EFFECTS — {name}")
    print(f"{'='*68}")
    if items_body:
        print(items_body)
    else:
        print("  (no '## Passive Item Effects — Quick Reference' section yet —")
        print("   nothing worn/attuned carries a passive mechanical effect, or the")
        print("   sheet predates this section; add one if that's not actually true.)")
    print()

    return combat_body is not None or items_body is not None


def _print_defenses(name: str, path: str) -> bool:
    """Print one character's incoming-attack defenses.

    Prefers the sheet's own `## Defenses` quick-reference. Falls back to the
    passive/trigger sections when a sheet predates that section, with a loud
    note — an absent section means "nobody has written it yet", never "this
    character has no defenses".
    """
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"  ! Could not read {path}: {e}")
        return False

    print(f"\n{'='*68}")
    print(f"  DEFENSES — {name}   (check BEFORE rolling anything against them)")
    print(f"{'='*68}")

    body = _extract_section(text, "Defenses")
    if body:
        print(body)
        print()
        return True

    print("  (no '## Defenses' section on this sheet yet — falling back to the")
    print("   passive/trigger sections. Add one: see templates/character-sheet.md.)")
    for heading in ("Passive Item Effects — Quick Reference", "Combat Triggers"):
        section = _extract_section(text, heading)
        if section:
            print(f"\n  -- from '{heading}' --")
            print(section)
    print()
    return False


def cmd_defense(campaign: str, entity_name: str, show_all: bool = False) -> None:
    """Print the defenses of one PC, or of every PC in the campaign."""
    chars_dir = _characters_dir(campaign)
    if show_all:
        if not os.path.isdir(chars_dir):
            print(f"  ! No characters/ directory found for campaign '{campaign}'.")
            return
        for fname in sorted(os.listdir(chars_dir)):
            if fname.lower().endswith(".md"):
                _print_defenses(fname[:-3], os.path.join(chars_dir, fname))
        return

    path = _resolve_sheet(chars_dir, entity_name)
    if path:
        _print_defenses(entity_name, path)
    else:
        print(f"  ! No character sheet found for '{entity_name}' in {chars_dir}")


def _resolve_sheet(chars_dir: str, entity_name: str) -> "str | None":
    """Path to a character sheet by name, case-insensitively."""
    path = os.path.join(chars_dir, f"{entity_name}.md")
    if os.path.isfile(path):
        return path
    if os.path.isdir(chars_dir):
        for fname in os.listdir(chars_dir):
            if fname.lower() == f"{entity_name.lower()}.md":
                return os.path.join(chars_dir, fname)
    return None


def cmd_turn(campaign: str, entity_name: str, targets: "list[str] | None" = None) -> None:
    """The mandatory call at the start of EVERY combatant's turn, PC or NPC.

    For a PC it prints that character's own `## Combat Triggers` and
    `## Passive Item Effects` — what they can do on their turn.

    For an NPC/monster it prints the DEFENSES of every PC that turn can touch,
    because that is the half the actor-keyed version used to miss: the gate was
    keyed on who acts, while a defensive passive (Cloak of Displacement's
    disadvantage, a damage immunity, a reaction like Riposte or Counterspell)
    belongs to whoever is *targeted*. Pass `--targets "A,B"` to narrow it to
    the PCs actually in reach; with no --targets, every PC in the campaign is
    printed, since any of them could be the target.

    Nothing in this turn may be rolled or narrated before this has run.
    """
    print(f"\n{'#'*68}")
    print(f"  ▶ TURN START — {entity_name}")
    print(f"{'#'*68}")

    # Step 1: effect tick (existing behavior, silent if nothing to report)
    cmd_effect(campaign, "tick", entity_name)

    # Step 2: what this turn needs checked. A PC acting → their own triggers.
    # An NPC acting → the defenses of the PCs it can act against.
    chars_dir = _characters_dir(campaign)
    path = _resolve_sheet(chars_dir, entity_name)
    if path:
        _print_one_triggers(entity_name, path)
        if targets:
            for target in targets:
                target_path = _resolve_sheet(chars_dir, target)
                if target_path:
                    _print_defenses(target, target_path)
                else:
                    print(f"  ! No character sheet for target '{target}'")
        return

    # NPC/monster turn.
    print(f"  ({entity_name} has no character sheet — NPC/monster turn.)")
    names = targets or [f[:-3] for f in sorted(os.listdir(chars_dir))
                        if f.lower().endswith(".md")] if os.path.isdir(chars_dir) else []
    if not names:
        print("  ! No PC sheets found to check defenses against.")
        return
    print(f"  Anything this turn rolls against a PC must be checked against the")
    print(f"  defenses below FIRST — advantage/disadvantage before the attack roll,")
    print(f"  resistance/immunity before the damage total, reactions before moving on.")
    for target in names:
        target_path = _resolve_sheet(chars_dir, target)
        if target_path:
            _print_defenses(target, target_path)
        else:
            print(f"  ! No character sheet for target '{target}'")


def cmd_triggers(campaign: str, entity: str, show_all: bool) -> None:
    chars_dir = _characters_dir(campaign)
    if show_all:
        if not os.path.isdir(chars_dir):
            print(f"  ! No characters/ directory found for campaign '{campaign}'.")
            return
        found_any = False
        for fname in sorted(os.listdir(chars_dir)):
            if fname.lower().endswith(".md"):
                found_any = True
                _print_one_triggers(fname[:-3], os.path.join(chars_dir, fname))
        if not found_any:
            print(f"  ! No character sheets found in {chars_dir}")
        return

    if not entity:
        print("  ! Provide a character name, or pass --all for every PC.")
        return

    path = os.path.join(chars_dir, f"{entity}.md")
    if not os.path.isfile(path):
        # Case-insensitive fallback match
        match = None
        if os.path.isdir(chars_dir):
            for fname in os.listdir(chars_dir):
                if fname.lower() == f"{entity.lower()}.md":
                    match = os.path.join(chars_dir, fname)
                    break
        if match:
            path = match
        else:
            print(f"  ! No character sheet found for '{entity}' in {chars_dir}")
            return
    _print_one_triggers(entity, path)


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="Session condition/death-save tracker.")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME",
                   help="Campaign name (matches ~/.claude/dnd/campaigns/<name>/)")
    sub = p.add_subparsers(dest="cmd")

    # effect
    eff = sub.add_parser("effect", help="Track timed effects (rounds/minutes/hours/indefinite)")
    eff.add_argument("action", choices=["start", "end", "tick"])
    eff.add_argument("entity")
    eff.add_argument("spell", nargs="?", default="",
                     help="Spell or ability name")
    eff.add_argument("duration", nargs="?", default="",
                     help="Duration: 10r / 60m / 8h / indef")
    eff.add_argument("conc", nargs="?", default="",
                     help="Pass 'conc' to mark as concentration")

    # condition
    cond = sub.add_parser("condition", help="Add/remove/clear conditions")
    cond.add_argument("action", choices=["add", "remove", "clear"])
    cond.add_argument("entity")
    cond.add_argument("condition", nargs="?", default="")

    # concentrate
    conc = sub.add_parser("concentrate", help="Track spell concentration")
    conc.add_argument("entity")
    conc.add_argument("spell", help="Spell name, or 'break' to end concentration")

    # saves
    sav = sub.add_parser("saves", help="Track death saving throws")
    sav.add_argument("entity")
    sav.add_argument("action", choices=["success", "failure", "stable", "reset"])

    # status
    stat = sub.add_parser("status", help="Show current tracking state")
    stat.add_argument("entity", nargs="?", default="")

    # clear
    clr = sub.add_parser("clear", help="Clear encounter state")
    clr.add_argument("--all", action="store_true",
                     help="Also clear death saves (not just conditions/concentration)")

    # triggers
    trg = sub.add_parser("triggers", help="Print a PC's '## Combat Triggers' and '## Passive Item Effects — Quick Reference' sections from their sheet")
    trg.add_argument("entity", nargs="?", default="",
                     help="Character name (matches characters/<name>.md)")
    trg.add_argument("--all", action="store_true",
                     help="Print every character sheet's Combat Triggers + Passive Item Effects sections")

    # turn — mandatory start-of-turn call for PCs (effect tick + triggers, merged)
    trn = sub.add_parser("turn", help="Run at the start of EVERY combatant's turn — PC triggers, or (NPC turn) the targeted PCs' defenses")
    trn.add_argument("entity", help="Whoever is acting: a character name, or an NPC/monster name")
    trn.add_argument("--targets", default="",
                     help="Comma-separated PC names this turn can act against "
                          "(NPC turn: defaults to every PC in the campaign)")

    dfn = sub.add_parser("defense", help="Print a PC's incoming-attack defenses (resistances, passives, reactions)")
    dfn.add_argument("entity", nargs="?", default="", help="Character name")
    dfn.add_argument("--all", action="store_true", help="Every PC in the campaign")

    args = p.parse_args()

    if args.cmd == "effect":
        cmd_effect(args.campaign, args.action, args.entity,
                   spell=args.spell, duration=args.duration,
                   is_conc=(args.conc.lower() == "conc"))
    elif args.cmd == "condition":
        cmd_condition(args.campaign, args.entity, args.action, args.condition)
    elif args.cmd == "concentrate":
        cmd_concentrate(args.campaign, args.entity, args.spell)
    elif args.cmd == "saves":
        cmd_saves(args.campaign, args.entity, args.action)
    elif args.cmd == "status":
        cmd_status(args.campaign, args.entity)
    elif args.cmd == "clear":
        cmd_clear(args.campaign, getattr(args, "all", False))
    elif args.cmd == "triggers":
        cmd_triggers(args.campaign, args.entity, getattr(args, "all", False))
    elif args.cmd == "turn":
        targets = [t.strip() for t in args.targets.split(",") if t.strip()]
        cmd_turn(args.campaign, args.entity, targets)
    elif args.cmd == "defense":
        cmd_defense(args.campaign, args.entity, getattr(args, "all", False))
    else:
        p.print_help()


if __name__ == "__main__":
    main()
