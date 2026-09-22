#!/usr/bin/env python3
"""
dice.py — D&D 5e dice roller

Rolls locally and prints the result. Used for DM-side dice only: NPC and
monster rolls, environmental/trap damage, and random tables. Dice belonging to
a player character are never rolled here — see SKILL.md "Dice ownership".

Every roll must declare its owner with --owner. If the owner matches a player
character in the active campaign, the script refuses to roll: that die belongs
to the player, who reports the raw result for the DM to add modifiers to.

Usage:
    python3 dice.py <notation> --owner "<who rolls this>" [--campaign N] [--silent] [--label "..."]

    python3 dice.py d20+8 --owner "Bone Devil" --label "Sting vs Kriv AC22"
    python3 dice.py 5d6 --owner "Bone Devil" --label "Sting poison damage"
    python3 dice.py 4d6 --owner trap --label "Falling rocks"

Exit codes:
    0  rolled
    2  no --owner given
    3  owner is a player character — ask the player for their raw roll

Notation supported:
    d20               single d20
    2d6               2 six-sided dice, sum
    d20+5             roll + flat modifier
    4d6kh3            roll 4d6, keep highest 3
    4d6kl3            roll 4d6, keep lowest 3
    d20 adv           advantage: roll twice, take higher  (→ 2d20kh1)
    d20 dis           disadvantage: roll twice, take lower (→ 2d20kl1)
    d20+3 adv         advantage with modifier
    2d6+3             multiple dice + modifier
"""

import json
import os
import random
import re
import sys

# Windows consoles default to a legacy codepage that mangles the glyphs used in
# this script's output; force UTF-8 where the streams support it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ── PC-ownership guard ───────────────────────────────────────────────────────
# A die a player character's own action produces is never rolled here. The
# guard is deliberately mechanical: the DM has to name an owner before rolling,
# and naming a PC stops the roll instead of quietly producing a number.

def _active_campaign() -> str | None:
    """Campaign marked active at /dm:dnd load, if any."""
    try:
        from paths import runtime_dir
        marker = runtime_dir() / "active-campaign.json"
        if marker.is_file():
            return json.loads(marker.read_text(encoding="utf-8")).get("name")
    except Exception:
        pass
    return None


def _pc_names(campaign: str | None) -> list[str]:
    """Character-sheet names for the campaign (empty list if none resolvable)."""
    if not campaign:
        return []
    try:
        from paths import find_campaign
        chars = find_campaign(campaign) / "characters"
        return [f.stem for f in chars.glob("*.md")] if chars.is_dir() else []
    except Exception:
        return []


def owner_is_pc(owner: str, campaign: str | None = None) -> str | None:
    """Return the matching PC's sheet name if `owner` names a player character."""
    who = owner.strip().lower()
    if not who:
        return None
    for sheet in _pc_names(campaign or _active_campaign()):
        name = sheet.lower()
        if who == name or name.startswith(who + " ") or who.startswith(name + " "):
            return sheet
        if who == name.split()[0]:          # "Kriv" matches "Kriv Shestendeliath"
            return sheet
    return None


def parse_notation(notation: str):
    notation = notation.strip().lower()
    adv = "adv" in notation or "advantage" in notation
    dis = "dis" in notation or "disadvantage" in notation
    notation = re.sub(r'\s*(adv|dis|advantage|disadvantage)\w*', '', notation).strip()

    pattern = r'^(\d*)d(\d+)(?:(kh|kl)(\d+))?([+-]\d+)?$'
    m = re.match(pattern, notation.replace(' ', ''))
    if not m:
        raise ValueError(f"Cannot parse dice notation: '{notation}'")

    num_dice = int(m.group(1)) if m.group(1) else 1
    die_size = int(m.group(2))
    keep_mode = m.group(3)
    keep_count = int(m.group(4)) if m.group(4) else None
    modifier = int(m.group(5)) if m.group(5) else 0
    return num_dice, die_size, modifier, keep_mode, keep_count, adv, dis


def roll_dice(num_dice, die_size):
    return [random.randint(1, die_size) for _ in range(num_dice)]


def format_modifier(mod):
    if mod == 0:
        return ""
    return f" + {mod}" if mod > 0 else f" - {abs(mod)}"


def run(notation: str, silent: bool = False, label: str = "") -> int:
    num_dice, die_size, modifier, keep_mode, keep_count, adv, dis = parse_notation(notation)

    if adv or dis:
        roll_a = roll_dice(num_dice, die_size)
        roll_b = roll_dice(num_dice, die_size)
        total_a = sum(roll_a) + modifier
        total_b = sum(roll_b) + modifier
        chosen = max(total_a, total_b) if adv else min(total_a, total_b)
        lbl = "ADV" if adv else "DIS"
        if not silent:
            print(f"[{lbl}] Roll A: {roll_a} = {total_a}{format_modifier(modifier)}")
            print(f"[{lbl}] Roll B: {roll_b} = {total_b}{format_modifier(modifier)}")
            taken = "A" if (adv and total_a >= total_b) or (dis and total_a <= total_b) else "B"
            print(f"Takes roll {taken} → Total: {chosen}")
        return chosen

    rolls = roll_dice(num_dice, die_size)

    if keep_mode and keep_count:
        sorted_rolls = sorted(rolls, reverse=(keep_mode == 'kh'))
        kept = sorted_rolls[:keep_count]
        dropped = sorted_rolls[keep_count:]
        result = sum(kept) + modifier
        if not silent:
            kept_str = " + ".join(str(r) for r in kept)
            drop_str = f"  (dropped: {dropped})" if dropped else ""
            print(f"Rolls: {rolls}{drop_str}")
            print(f"Kept ({keep_mode}{keep_count}): [{kept_str}]{format_modifier(modifier)} = {result}")
        return result

    result = sum(rolls) + modifier
    if not silent:
        if num_dice == 1 and die_size == 20:
            raw = rolls[0]
            flag = ""
            if raw == 20:
                flag = "  *** CRITICAL HIT (nat 20)! ***"
            elif raw == 1:
                flag = "  *** FUMBLE (nat 1)! ***"
            print(f"Roll: {raw}{format_modifier(modifier)} = {result}{flag}")
        else:
            print(f"Rolls: {rolls}{format_modifier(modifier)} = {result}")
    return result


if __name__ == "__main__":
    argv = sys.argv[1:]
    silent = "--silent" in argv
    label = ""
    owner = ""
    campaign = None
    for flag in ("--label", "--owner", "--campaign"):
        if flag in argv:
            i = argv.index(flag)
            if i + 1 < len(argv):
                value = argv[i + 1]
                if flag == "--label":
                    label = value
                elif flag == "--owner":
                    owner = value
                else:
                    campaign = value
                del argv[i:i + 2]
    args = [a for a in argv if a != "--silent"]

    if not args:
        print('Usage: python3 dice.py <notation> --owner "<who rolls this>"\n'
              '  e.g. dice.py d20+5 --owner "Goblin Boss" --label "attack vs Piper"')
        sys.exit(1)

    if not owner:
        print('dice.py: --owner is required — name whose die this is '
              '(an NPC, a monster, "trap", "environment", "table").\n'
              '  A player character\'s own die is never rolled here: ask the player '
              'for their raw roll instead (SKILL.md "Dice ownership").', file=sys.stderr)
        sys.exit(2)

    pc = owner_is_pc(owner, campaign)
    if pc:
        print(f'dice.py: REFUSED — "{owner}" is a player character ({pc}).\n'
              f'  This die belongs to the player. Call for it by name, wait for the raw '
              f'result, then add the modifiers yourself and state the total.\n'
              f'  (If this is damage arriving AT {pc} from a trap or hazard, roll it with '
              f'--owner trap / --owner environment instead.)', file=sys.stderr)
        sys.exit(3)

    notation = " ".join(args)
    result = run(notation, silent=silent, label=label)
    if silent:
        print(result)
