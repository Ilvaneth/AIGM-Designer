#!/usr/bin/env python3
"""
character.py — D&D 5e character stat calculator

Derives all secondary stats from raw inputs. Used by the DM (Claude)
to verify and generate character sheets without manual arithmetic.

Usage:
    python3 character.py calc --class fighter --level 1 \\
        STR=15 DEX=10 CON=15 INT=9 WIS=11 CHA=14 \\
        --proficient STR CON Athletics Intimidation Perception Survival

    python3 character.py levelup --class fighter --from 1 \\
        --hp-roll 6 --con-mod 2 [--subclass "battle master"]
        Prints HP, a loud flag if the proficiency-bonus band just changed
        (level 13, 17, etc. — this WILL touch nearly every derived number on
        the sheet, don't skip recomputing them), ASI/feat eligibility, every
        class feature gained at exactly this level (from CLASS_FEATURES —
        currently populated for fighter/wizard; extend it before guessing a
        new class from memory), subclass features if --subclass is given
        (currently: battle master, school of necromancy), and spell slot
        changes for casters (currently: wizard). Added 2026-09-14 after a
        proficiency-bonus band change got missed at the table entirely.

    python3 character.py xp --level 1 --gained 150
        Print XP total and whether level-up threshold is reached.
"""

import sys
import re


# ─── Proficiency bonus by level ──────────────────────────────────────────────
PROF_BONUS = {1:2, 2:2, 3:2, 4:2, 5:3, 6:3, 7:3, 8:3,
              9:4, 10:4, 11:4, 12:4, 13:5, 14:5, 15:5, 16:5,
              17:6, 18:6, 19:6, 20:6}

# ─── XP thresholds (total XP needed to reach level) ─────────────────────────
XP_THRESHOLDS = {
    1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500, 6: 14000,
    7: 23000, 8: 34000, 9: 48000, 10: 64000, 11: 85000,
    12: 100000, 13: 120000, 14: 140000, 15: 165000,
    16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000,
}

# ─── Hit dice by class ───────────────────────────────────────────────────────
HIT_DICE = {
    "barbarian": 12, "fighter": 10, "paladin": 10, "ranger": 10,
    "bard": 8, "cleric": 8, "druid": 8, "monk": 8, "rogue": 8, "warlock": 8,
    "sorcerer": 6, "wizard": 6,
}

# ─── ASI/Feat levels by class ────────────────────────────────────────────────
# Standard is 4/8/12/16/19; Fighter gets two extra (6, 14), Rogue gets one
# extra (10). Levels not listed for a class fall back to the standard set.
ASI_LEVELS_STANDARD = {4, 8, 12, 16, 19}
ASI_LEVELS = {
    "fighter": {4, 6, 8, 12, 14, 16, 19},
    "rogue":   {4, 8, 10, 12, 16, 19},
}


# ─── Class feature table, level → list of feature strings ───────────────────
# Deliberately built out for the classes actually in play first (see
# SKILL.md's level-up discipline note, added 2026-09-14) rather than
# attempting a from-memory guess at level-up time — extend this table when a
# new class shows up at the table instead of reasoning from memory again.
CLASS_FEATURES = {
    "fighter": {
        1: ["Fighting Style", "Second Wind"],
        2: ["Action Surge (1 use)"],
        3: ["Martial Archetype"],
        4: ["Ability Score Improvement"],
        5: ["Extra Attack — 2 attacks per Attack action"],
        6: ["Ability Score Improvement"],
        7: ["Martial Archetype feature"],
        8: ["Ability Score Improvement"],
        9: ["Indomitable (1 use)"],
        10: ["Martial Archetype feature"],
        11: ["Extra Attack — 3 attacks per Attack action"],
        12: ["Ability Score Improvement"],
        13: ["Indomitable (2 uses)"],
        14: ["Ability Score Improvement"],
        15: ["Martial Archetype feature"],
        16: ["Ability Score Improvement"],
        17: ["Action Surge (2 uses)", "Indomitable (3 uses)"],
        18: ["Martial Archetype feature"],
        19: ["Ability Score Improvement"],
        20: ["Extra Attack — 4 attacks per Attack action"],
    },
    "wizard": {
        1: ["Spellcasting", "Ritual Casting", "Arcane Recovery"],
        2: ["Arcane Tradition"],
        3: [],
        4: ["Ability Score Improvement"],
        5: [],
        6: ["Arcane Tradition feature"],
        7: [],
        8: ["Ability Score Improvement"],
        9: [],
        10: ["Arcane Tradition feature"],
        11: [],
        12: ["Ability Score Improvement"],
        13: [],
        14: ["Arcane Tradition feature"],
        15: [],
        16: ["Ability Score Improvement"],
        17: [],
        18: ["Spell Mastery"],
        19: ["Ability Score Improvement"],
        20: ["Signature Spells"],
    },
}

# ─── Subclass feature table, keyed (class, subclass) → level → features ─────
SUBCLASS_FEATURES = {
    ("fighter", "battle master"): {
        3: ["Combat Superiority — 4 superiority dice (d8), Student of War, 3 maneuvers known"],
        7: ["Know Your Enemy", "Combat Superiority: +1 die (5 dice)", "+2 maneuvers known (5 total)"],
        10: ["Improved Combat Superiority — dice become d10", "+2 maneuvers known (7 total)"],
        15: ["Relentless — regain 1 superiority die if you have none left when you roll initiative",
             "Combat Superiority: +1 die (6 dice)", "+2 maneuvers known (9 total)"],
        18: ["Improved Combat Superiority — dice become d12"],
    },
    ("wizard", "school of necromancy"): {
        2: ["Necromancy Savant — half gold/time to copy Necromancy spells", "Grim Harvest"],
        6: ["Undead Thralls — Animate Dead targets one extra corpse; your Necromancy-created undead gain bonus HP + your proficiency bonus to weapon damage"],
        10: ["Inured to Undeath — resistance to necrotic damage, immune to max-HP-reducing effects"],
        14: ["Command Undead — magically overwrite another creature's control of an undead"],
    },
}

# ─── Wizard spell slots by level (cumulative table, index 0 = 1st-level slots) ─
WIZARD_SLOTS = {
    1:  [2],
    2:  [3],
    3:  [4, 2],
    4:  [4, 3],
    5:  [4, 3, 2],
    6:  [4, 3, 3],
    7:  [4, 3, 3, 1],
    8:  [4, 3, 3, 2],
    9:  [4, 3, 3, 3, 1],
    10: [4, 3, 3, 3, 2],
    11: [4, 3, 3, 3, 2, 1],
    12: [4, 3, 3, 3, 2, 1],
    13: [4, 3, 3, 3, 2, 1, 1],
    14: [4, 3, 3, 3, 2, 1, 1],
    15: [4, 3, 3, 3, 2, 1, 1, 1],
    16: [4, 3, 3, 3, 2, 1, 1, 1],
    17: [4, 3, 3, 3, 2, 1, 1, 1, 1],
    18: [4, 3, 3, 3, 3, 1, 1, 1, 1],
    19: [4, 3, 3, 3, 3, 2, 1, 1, 1],
    20: [4, 3, 3, 3, 3, 2, 2, 1, 1],
}


# ─── Saving throw proficiencies by class ─────────────────────────────────────
SAVE_PROFS = {
    "fighter":   ["STR", "CON"],
    "barbarian": ["STR", "CON"],
    "ranger":    ["STR", "DEX"],
    "paladin":   ["WIS", "CHA"],
    "rogue":     ["DEX", "INT"],
    "bard":      ["DEX", "CHA"],
    "cleric":    ["WIS", "CHA"],
    "druid":     ["INT", "WIS"],
    "monk":      ["STR", "DEX"],
    "warlock":   ["WIS", "CHA"],
    "sorcerer":  ["CON", "CHA"],
    "wizard":    ["INT", "WIS"],
}

# ─── All skills with governing ability ───────────────────────────────────────
SKILLS = {
    "Acrobatics": "DEX", "Animal Handling": "WIS", "Arcana": "INT",
    "Athletics": "STR", "Deception": "CHA", "History": "INT",
    "Insight": "WIS", "Intimidation": "CHA", "Investigation": "INT",
    "Medicine": "WIS", "Nature": "INT", "Perception": "WIS",
    "Performance": "CHA", "Persuasion": "CHA", "Religion": "INT",
    "Sleight of Hand": "DEX", "Stealth": "DEX", "Survival": "WIS",
}

STATS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]


def mod(score: int) -> int:
    return (score - 10) // 2


def fmt(n: int) -> str:
    return f"+{n}" if n >= 0 else str(n)


def parse_scores(args: list[str]) -> dict[str, int]:
    scores = {}
    for a in args:
        if "=" in a:
            k, v = a.split("=", 1)
            if k.upper() in STATS:
                scores[k.upper()] = int(v)
    return scores


def parse_proficient(args: list[str]) -> list[str]:
    """Everything after --proficient until next -- flag."""
    if "--proficient" not in args:
        return []
    idx = args.index("--proficient")
    profs = []
    for a in args[idx + 1:]:
        if a.startswith("--"):
            break
        profs.append(a)
    return profs


def do_calc(args: list[str]):
    cls = args[args.index("--class") + 1].lower() if "--class" in args else "fighter"
    lvl = int(args[args.index("--level") + 1]) if "--level" in args else 1
    scores = parse_scores(args)
    proficient = parse_proficient(args)  # list of stat names + skill names

    prof = PROF_BONUS.get(lvl, 2)
    hd = HIT_DICE.get(cls, 8)
    con_mod = mod(scores.get("CON", 10))
    hp = hd + con_mod  # level 1 max
    save_profs = SAVE_PROFS.get(cls, [])

    print(f"\n{'='*50}")
    print(f"  {cls.title()} Level {lvl}  |  Proficiency Bonus: +{prof}")
    print(f"{'='*50}")

    print(f"\n  Ability Scores:")
    print(f"  {'Stat':<6} {'Score':>6} {'Mod':>5}")
    print(f"  {'-'*20}")
    for s in STATS:
        score = scores.get(s, 10)
        print(f"  {s:<6} {score:>6} {fmt(mod(score)):>5}")

    print(f"\n  Combat Stats:")
    print(f"  HP (level 1): {hp}  ({hd} + CON {fmt(con_mod)})")
    print(f"  Hit Dice: {lvl}d{hd}")
    print(f"  Initiative: {fmt(mod(scores.get('DEX', 10)))}")

    print(f"\n  Saving Throws (* = proficient):")
    for s in STATS:
        score = scores.get(s, 10)
        is_prof = s in save_profs or s in proficient
        bonus = mod(score) + (prof if is_prof else 0)
        marker = "*" if is_prof else " "
        print(f"  {marker} {s:<4} {fmt(bonus)}")

    print(f"\n  Skills (* = proficient):")
    for skill, ability in sorted(SKILLS.items()):
        score = scores.get(ability, 10)
        is_prof = skill in proficient or skill.lower() in [p.lower() for p in proficient]
        bonus = mod(score) + (prof if is_prof else 0)
        marker = "*" if is_prof else " "
        print(f"  {marker} {skill:<22} ({ability})  {fmt(bonus)}")

    print(f"\n  XP to next level: {XP_THRESHOLDS.get(lvl+1, 'MAX')} total")
    print()


def do_levelup(args: list[str]):
    cls = args[args.index("--class") + 1].lower() if "--class" in args else "fighter"
    subclass = args[args.index("--subclass") + 1].lower() if "--subclass" in args else None
    from_lvl = int(args[args.index("--from") + 1]) if "--from" in args else 1
    to_lvl = from_lvl + 1
    hp_roll = int(args[args.index("--hp-roll") + 1]) if "--hp-roll" in args else None
    con_mod_val = int(args[args.index("--con-mod") + 1]) if "--con-mod" in args else 0

    hd = HIT_DICE.get(cls, 8)
    prof_old = PROF_BONUS.get(from_lvl, 2)
    prof_new = PROF_BONUS.get(to_lvl, 2)

    print(f"\n{'='*68}")
    print(f"  LEVEL UP: {cls.title()} {from_lvl} -> {to_lvl}"
          + (f" ({subclass.title()})" if subclass else ""))
    print(f"{'='*68}")

    if prof_new != prof_old:
        print(f"  *** PROFICIENCY BONUS CHANGED: +{prof_old} -> +{prof_new} ***")
        print(f"      Recompute EVERY proficient skill, save, weapon/spell attack")
        print(f"      bonus, spell save DC, and maneuver/breath-weapon DC on the")
        print(f"      sheet now — this touches nearly every derived number.")
    else:
        print(f"  Proficiency bonus: +{prof_new} (unchanged)")

    if hp_roll is not None:
        hp_gained = hp_roll + con_mod_val
        print(f"  HP gained: d{hd}({hp_roll}) + CON({fmt(con_mod_val)}) = {hp_gained}")
    else:
        avg = (hd // 2 + 1) + con_mod_val
        print(f"  HP gained (avg): {avg}  ({hd//2+1} + CON {fmt(con_mod_val)})")

    # ASI/Feat eligibility
    asi_levels = ASI_LEVELS.get(cls, ASI_LEVELS_STANDARD)
    if to_lvl in asi_levels:
        print(f"  *** ASI / FEAT available at level {to_lvl} — ask the player now. ***")

    # Class features gained at exactly this level
    class_feats = CLASS_FEATURES.get(cls, {}).get(to_lvl, [])
    if class_feats:
        print(f"  Class features gained at {cls.title()} {to_lvl}:")
        for feat in class_feats:
            print(f"    - {feat}")
    elif cls not in CLASS_FEATURES:
        print(f"  (No feature table for class '{cls}' yet — SKILL.md's level-up")
        print(f"   discipline still applies: verify features manually against the")
        print(f"   SRD/PHB rather than from memory, and consider adding this class")
        print(f"   to CLASS_FEATURES in character.py while you're at it.)")

    # Subclass features gained at exactly this level
    if subclass:
        sub_table = SUBCLASS_FEATURES.get((cls, subclass))
        if sub_table is not None:
            sub_feats = sub_table.get(to_lvl, [])
            if sub_feats:
                print(f"  Subclass features gained ({subclass.title()}, level {to_lvl}):")
                for feat in sub_feats:
                    print(f"    - {feat}")
        else:
            print(f"  (No subclass feature table for '{subclass}' yet — verify manually.)")

    # Spell slots (casters only, currently Wizard)
    if cls == "wizard":
        old_slots = WIZARD_SLOTS.get(from_lvl, [])
        new_slots = WIZARD_SLOTS.get(to_lvl, [])
        if new_slots != old_slots:
            print(f"  Spell slots changed:")
            print(f"    Old (level {from_lvl}): {old_slots}")
            print(f"    New (level {to_lvl}):   {new_slots}")
            if len(new_slots) > len(old_slots):
                print(f"    *** New spell level unlocked: {len(new_slots)}th level slots ***")
        else:
            print(f"  Spell slots: unchanged ({new_slots})")

    print(f"  XP threshold for level {to_lvl}: {XP_THRESHOLDS.get(to_lvl, 'MAX')}")
    print(f"{'='*68}\n")


def do_xp(args: list[str]):
    lvl = int(args[args.index("--level") + 1]) if "--level" in args else 1
    gained = int(args[args.index("--gained") + 1]) if "--gained" in args else 0
    current = XP_THRESHOLDS.get(lvl, 0)
    next_lvl = XP_THRESHOLDS.get(lvl + 1)
    new_total = current + gained

    print(f"\n  XP: {current} + {gained} gained = {new_total}")
    if next_lvl:
        if new_total >= next_lvl:
            print(f"  *** Level up available! Reached {next_lvl} (Level {lvl+1} threshold) ***")
        else:
            print(f"  Next level ({lvl+1}) at: {next_lvl}  ({next_lvl - new_total} XP remaining)")
    else:
        print("  Maximum level reached.")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "calc":
        do_calc(args)
    elif cmd == "levelup":
        do_levelup(args)
    elif cmd == "xp":
        do_xp(args)
    else:
        print(f"Unknown command: {cmd}. Use: calc | levelup | xp")
        sys.exit(1)
