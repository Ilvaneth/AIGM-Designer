#!/usr/bin/env python3
"""
burst_check.py — solo-boss nova ceiling check

Reads each party member's own "## Burst Reference" table (a hand-maintained
section on their character sheet — see templates/character-sheet.md) and
sums the single worst-case burst per character into a party-wide "what's the
most damage this table can do to one target in one round" figure.

Why this exists: a solo boss fight left deliberately unfinalized (e.g. The
Debased Mint's Room 18) needs its actual HP/Legendary Resistance set against
the REAL party at the time of the fight, not a number picked in the abstract
months earlier. Re-run this immediately before such a fight.

Burst Reference table format expected on each character sheet:

    ## Burst Reference

    | Scenario | Target | Total (avg) | Formula |
    |----------|--------|-------------|---------|
    | Full Attack, vs undead | Single | 34.0 | 2×(1d12+6+1d8) |
    | Action Surge + full maneuvers, vs undead | Single | 86.0 | ... |
    ...

Usage:
    python3 burst_check.py --campaign ashen-crown
        Worst single-round burst per character (all scenarios), summed.

    python3 burst_check.py --campaign ashen-crown --vs undead
        Only scenarios whose Scenario/Target text mentions "undead" —
        use this against an undead boss so non-undead-bonus rows don't
        inflate the estimate.

    python3 burst_check.py --campaign ashen-crown --target-hp 150
        Also reports the margin against a specific boss HP total.

    python3 burst_check.py --campaign ashen-crown --characters "Kriv Shestendeliath,Ilvaneth Duskmere"
        Restrict to named characters instead of every sheet in characters/.
"""

from __future__ import annotations

import sys
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

import argparse
import os
import re

from paths import find_campaign as _find_campaign


def _characters_dir(campaign: str) -> str:
    return os.path.join(str(_find_campaign(campaign)), "characters")


def _extract_burst_section(text: str) -> str | None:
    m = re.search(r'^##\s*Burst Reference\s*$(.*?)(?=^##\s|\Z)',
                  text, flags=re.MULTILINE | re.DOTALL)
    return m.group(1) if m else None


def _parse_burst_table(section: str) -> list[dict]:
    """Parse the '| Scenario | Target | Total (avg) | Formula |' table."""
    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if re.match(r'^:?-+:?$', cells[0]):
            continue
        if cells[0].lower() in ("scenario",):  # header row
            continue
        try:
            total = float(cells[2].replace(",", ""))
        except ValueError:
            continue
        rows.append({
            "scenario": cells[0],
            "target": cells[1],
            "total": total,
            "formula": cells[3] if len(cells) > 3 else "",
        })
    return rows


def _load_character_burst(path: str) -> tuple[str, list[dict]] | None:
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    name_m = re.search(r'^#\s+(.+)$', text, flags=re.MULTILINE)
    name = name_m.group(1).strip() if name_m else os.path.splitext(os.path.basename(path))[0]
    section = _extract_burst_section(text)
    if section is None:
        return name, []
    return name, _parse_burst_table(section)


def _matches_vs(row: dict, vs: str) -> bool:
    needle = vs.lower()
    return needle in row["scenario"].lower() or needle in row["target"].lower()


def cmd_check(campaign: str, characters: list[str] | None, vs: str | None,
               target_hp: float | None, single_target_only: bool) -> None:
    chars_dir = _characters_dir(campaign)
    if not os.path.isdir(chars_dir):
        print(f"  ! No characters/ directory for campaign '{campaign}'.")
        return

    if characters:
        paths = []
        for name in characters:
            p = os.path.join(chars_dir, f"{name}.md")
            if os.path.isfile(p):
                paths.append(p)
            else:
                # case-insensitive fallback
                match = None
                for fname in os.listdir(chars_dir):
                    if fname.lower() == f"{name.lower()}.md":
                        match = os.path.join(chars_dir, fname)
                        break
                if match:
                    paths.append(match)
                else:
                    print(f"  ! No sheet found for '{name}', skipping.")
    else:
        paths = [os.path.join(chars_dir, f) for f in sorted(os.listdir(chars_dir))
                 if f.lower().endswith(".md")]

    print(f"\n{'='*68}")
    print(f"  SOLO BOSS NOVA-CEILING CHECK — {campaign}")
    if vs:
        print(f"  Filter: scenarios matching \"{vs}\"")
    print(f"{'='*68}")

    party_total = 0.0
    any_data = False

    for path in paths:
        result = _load_character_burst(path)
        if result is None:
            continue
        name, rows = result
        if not rows:
            print(f"\n  {name}: no '## Burst Reference' table on this sheet — skipped.")
            print(f"    (Add one, or this character's burst isn't counted toward the ceiling.)")
            continue

        candidates = rows
        if single_target_only:
            candidates = [r for r in candidates if "single" in r["target"].lower()
                          or "aoe" not in r["target"].lower()]
        if vs:
            filtered = [r for r in candidates if _matches_vs(r, vs)]
            if filtered:
                candidates = filtered
            # if the vs-filter matches nothing, fall back to all candidates
            # rather than silently reporting 0 for this character

        if not candidates:
            print(f"\n  {name}: no matching scenarios — skipped.")
            continue

        best = max(candidates, key=lambda r: r["total"])
        party_total += best["total"]
        any_data = True
        print(f"\n  {name} — worst single-round burst:")
        print(f"    {best['scenario']}  →  {best['total']:.1f} avg dmg")
        print(f"    Formula: {best['formula']}")

    if not any_data:
        print("\n  ! No usable Burst Reference data found for anyone — nothing to report.")
        return

    print(f"\n{'-'*68}")
    print(f"  PARTY COMBINED WORST-CASE, ONE ROUND, ONE TARGET:  {party_total:.1f} avg dmg")

    if target_hp is not None:
        margin = target_hp - party_total
        print(f"  Target HP: {target_hp:.0f}")
        if margin <= 0:
            print(f"  ⚠ DIES TO THE OPENING ROUND — target HP is {abs(margin):.0f} below the party's "
                  f"combined nova. Add HP, Legendary Resistance, or a hard escape/phase trigger before running this fight.")
        elif margin < target_hp * 0.25:
            print(f"  ⚠ Survives, barely — only {margin:.0f} HP ({margin/target_hp*100:.0f}%) of "
                  f"margin left after the opening round. Consider Legendary Resistance or a defensive reaction.")
        else:
            print(f"  Survives the opening round with {margin:.0f} HP ({margin/target_hp*100:.0f}%) to spare.")
    print()


def main() -> None:
    p = argparse.ArgumentParser(description="Solo boss nova-ceiling check from party Burst Reference tables.")
    p.add_argument("--campaign", required=True)
    p.add_argument("--characters", help="Comma-separated character names (default: everyone in characters/)")
    p.add_argument("--vs", help="Only count scenarios whose Scenario/Target text matches this (e.g. 'undead')")
    p.add_argument("--target-hp", type=float, help="Boss HP to check the margin against")
    p.add_argument("--single-target-only", action="store_true",
                   help="Exclude AoE-only scenarios (a solo boss usually only eats single-target rows anyway, "
                        "but AoE rows are included by default since a boss can still stand in one)")
    args = p.parse_args()

    characters = [c.strip() for c in args.characters.split(",")] if args.characters else None
    cmd_check(args.campaign, characters, args.vs, args.target_hp, args.single_target_only)


if __name__ == "__main__":
    main()
