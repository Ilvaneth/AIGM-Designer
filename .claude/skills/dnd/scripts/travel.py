#!/usr/bin/env python3
"""
travel.py — layered travel-encounter roller

Reads a campaign's own `reference/travel-encounters.md` (regional tables are
campaign content, not skill content — see SKILL-travel.md) and rolls, for
real, the two-layer result: a weighted d12 category, then a d6 result from
that category's own subtable. Appends every roll to the same file's own
Roll Log table, so the document and the actual rolls can never disagree.

Table format expected in the campaign's reference/travel-encounters.md:

    ## <Region Name> — levels X-Y

    ### Early tier

    #### Category

    | d12 | Category |
    |-----|----------|
    | 1-4 | Combat |
    | 5   | Quiet/Texture |
    ...

    #### Quiet/Texture

    | d6 | Result |
    |----|--------|
    | 1  | ... |
    ...

    ### Late tier

    #### Combat

    | d6 | Result |
    ...

    ## Roll Log

    | When | Route | Rolls | Outcome |
    |------|-------|-------|---------|

Usage:
    python3 travel.py --campaign ashen-crown --region "Karsgate Approaches" \\
        --tier early --days 3 [--route "Karsgate -> Gallowmere"] [--seed N]

    python3 travel.py --campaign ashen-crown --list-regions
"""

from __future__ import annotations

import sys
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

import argparse
import random
import re
from datetime import datetime, timezone
from pathlib import Path

from paths import find_campaign as _find_campaign


def _ref_path(campaign: str) -> Path:
    return _find_campaign(campaign) / "reference" / "travel-encounters.md"


def _parse_range(cell: str) -> tuple[int, int]:
    """'1-4' -> (1,4); '5' -> (5,5)."""
    cell = cell.strip()
    m = re.match(r'^(\d+)\s*-\s*(\d+)$', cell)
    if m:
        return int(m.group(1)), int(m.group(2))
    return int(cell), int(cell)


def _parse_md_table(block: str) -> list[tuple[str, str]]:
    """Parse a '| a | b |' markdown table (with a separator row) into
    [(col1, col2), ...], skipping the header and separator rows."""
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if re.match(r'^:?-+:?$', cells[0]):  # separator row
            continue
        rows.append((cells[0], cells[1]))
    return rows[1:] if rows else rows  # drop header row


def _section(text: str, heading_prefix: str, name_pattern: str) -> str | None:
    """Find a section starting at a heading like '## <name>' (case-insensitive
    substring match on name_pattern) and return its body up to the next
    heading of the same or higher level."""
    level = len(heading_prefix)
    pattern = re.compile(
        rf'^{re.escape(heading_prefix)}\s+(.*{re.escape(name_pattern)}.*)$',
        re.IGNORECASE | re.MULTILINE,
    )
    m = pattern.search(text)
    if not m:
        return None
    start = m.end()
    # Next heading at this level or shallower ends the section.
    stop_pattern = re.compile(rf'^#{{1,{level}}}\s+', re.MULTILINE)
    m2 = stop_pattern.search(text, pos=start)
    end = m2.start() if m2 else len(text)
    return text[start:end]


def list_regions(campaign: str) -> None:
    path = _ref_path(campaign)
    if not path.is_file():
        print(f"  ! No reference/travel-encounters.md found for '{campaign}' "
              f"(expected at {path}).")
        return
    text = path.read_text(encoding="utf-8")
    regions = re.findall(r'^##\s+(.+)$', text, flags=re.MULTILINE)
    regions = [r for r in regions if r.strip().lower() != "roll log"]
    if not regions:
        print("  ! No '## <Region>' sections found.")
        return
    print("Regions defined in travel-encounters.md:")
    for r in regions:
        print(f"  - {r.strip()}")


def _resolve_nested_roll(result_text: str) -> str:
    """A cell can embed its own sub-roll, e.g.
    'Undead — roll d4: 1) 3x Skeleton 2) 2x Specter 3) ... 4) ...'
    or, in a translated table, 'Olu-doga - d4 at: 1) ... 2) ...'.
    Language-agnostic: matches '(roll )?d<N> (at)?:' right before the
    numbered-option list, so any table language works as long as the
    numbered '1) ... 2) ...' marker convention is kept.
    Detect that pattern, roll it, and append the chosen option in place."""
    m = re.search(r'(?:roll\s+)?d(\d+)\s*(?:at)?\s*:\s*(.+)$',
                  result_text, flags=re.IGNORECASE)
    if not m:
        return result_text
    sides = int(m.group(1))
    options_text = m.group(2)
    # Split on "N)" markers
    parts = re.split(r'(\d+)\)\s*', options_text)
    options: dict[int, str] = {}
    for i in range(1, len(parts) - 1, 2):
        idx = int(parts[i])
        val = parts[i + 1].strip()
        val = re.split(r'\s+\d+\)\s*$', val)[0]  # trim trailing artifacts
        options[idx] = val.rstrip()
    if not options:
        return result_text
    roll = random.randint(1, sides)
    chosen = options.get(roll, f"(no option {roll} found)")
    prefix = result_text[:m.start()].rstrip(" —-")
    return f"{prefix} — sub-roll d{sides}({roll}): {chosen}"


def roll_one_leg(campaign: str, region: str, tier: str) -> dict:
    path = _ref_path(campaign)
    if not path.is_file():
        raise FileNotFoundError(
            f"No reference/travel-encounters.md for campaign '{campaign}' "
            f"(expected at {path}). Author the region's table there first — "
            f"see SKILL-travel.md."
        )
    text = path.read_text(encoding="utf-8")

    region_body = _section(text, "##", region)
    if region_body is None:
        raise ValueError(
            f"No '## ...{region}...' section found in {path}. "
            f"Run --list-regions to see what's defined."
        )

    tier_heading = "Early tier" if tier.lower().startswith("e") else "Late tier"
    tier_body = _section(region_body, "###", tier_heading)
    if tier_body is None:
        raise ValueError(
            f"No '### {tier_heading}' section found under region '{region}'."
        )

    # Category table always lives under the tier we resolved into, EXCEPT
    # Late tier conventionally only redefines Combat and inherits the rest —
    # fall back to Early tier's body for anything Late doesn't itself define.
    early_body = _section(region_body, "###", "Early tier") or ""

    cat_body = _section(tier_body, "####", "Category") or _section(early_body, "####", "Category")
    if cat_body is None:
        raise ValueError(f"No '#### Category' table found for region '{region}'.")
    cat_rows = _parse_md_table(cat_body)
    if not cat_rows:
        raise ValueError(f"'#### Category' table for '{region}' parsed empty.")

    cat_roll = random.randint(1, 12)
    category = None
    for rng, name in cat_rows:
        lo, hi = _parse_range(rng)
        if lo <= cat_roll <= hi:
            category = name.strip()
            break
    if category is None:
        raise ValueError(f"d12 roll {cat_roll} matched no row in Category table.")

    sub_body = _section(tier_body, "####", category)
    if sub_body is None:
        sub_body = _section(early_body, "####", category)
    if sub_body is None:
        raise ValueError(
            f"No '#### {category}' subtable found for region '{region}' "
            f"(tier {tier_heading} or Early tier)."
        )
    sub_rows = _parse_md_table(sub_body)
    if not sub_rows:
        raise ValueError(f"'#### {category}' table for '{region}' parsed empty.")

    sub_roll = random.randint(1, 6)
    result = None
    for rng, text_result in sub_rows:
        lo, hi = _parse_range(rng)
        if lo <= sub_roll <= hi:
            result = text_result.strip()
            break
    if result is None:
        raise ValueError(f"d6 roll {sub_roll} matched no row in '{category}' table.")

    result = _resolve_nested_roll(result)

    return {
        "region": region,
        "tier": tier_heading,
        "category_roll": cat_roll,
        "category": category,
        "result_roll": sub_roll,
        "result": result,
    }


def append_roll_log(campaign: str, route: str, legs: list[dict]) -> None:
    path = _ref_path(campaign)
    text = path.read_text(encoding="utf-8")

    when = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rolls_str = " · ".join(
        f"{'N' if i % 2 else 'D'}{i//2+1}: Cat {l['category_roll']}->{l['category']}, "
        f"Sub {l['result_roll']}"
        for i, l in enumerate(legs)
    )
    outcome_str = " · ".join(l["result"] for l in legs)
    new_row = f"| {when} | {route} | {rolls_str} | {outcome_str} — *pending resolution* |\n"

    m = re.search(r'^##\s+Roll Log\s*$', text, flags=re.MULTILINE)
    if not m:
        # No Roll Log section yet — create one at the end of the file.
        header = "\n## Roll Log\n\n| When | Route | Rolls | Outcome |\n|------|-------|-------|---------|\n"
        text = text.rstrip("\n") + "\n\n" + header + new_row
    else:
        # Insert after the last existing row of the table (or right after the
        # separator row if the table is currently empty).
        tail = text[m.end():]
        table_m = re.search(r'\|\s*When\s*\|.*\n\|[-:| ]+\|\n', tail)
        if not table_m:
            insert_at = m.end()
            text = text[:insert_at] + "\n\n| When | Route | Rolls | Outcome |\n|------|-------|-------|---------|\n" + new_row + text[insert_at:]
        else:
            # find end of table: consecutive lines starting with '|'
            after_header = tail[table_m.end():]
            lines = after_header.splitlines(keepends=True)
            consumed = 0
            for ln in lines:
                if ln.strip().startswith("|"):
                    consumed += len(ln)
                else:
                    break
            insert_pos = m.end() + table_m.end() + consumed
            text = text[:insert_pos] + new_row + text[insert_pos:]

    path.write_text(text, encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description="Layered travel-encounter roller.")
    p.add_argument("--campaign", required=True)
    p.add_argument("--region", help="Region name (substring match against '## <name>')")
    p.add_argument("--tier", choices=["early", "late"], default="early")
    p.add_argument("--days", type=int, default=1, help="Number of legs (days/nights) to roll")
    p.add_argument("--route", default="", help="Free-text route label for the roll log")
    p.add_argument("--seed", type=int, help="Seed the RNG (repeatable rolls, testing only)")
    p.add_argument("--list-regions", action="store_true")
    p.add_argument("--no-log", action="store_true", help="Don't append to the Roll Log table")
    args = p.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.list_regions:
        list_regions(args.campaign)
        return

    if not args.region:
        print("  ! --region is required (or pass --list-regions to see options).")
        sys.exit(1)

    legs = []
    try:
        for i in range(args.days):
            legs.append(roll_one_leg(args.campaign, args.region, args.tier))
    except (FileNotFoundError, ValueError) as e:
        print(f"  ! {e}")
        sys.exit(1)

    print(f"\n{'='*68}")
    print(f"  TRAVEL — {args.region} ({legs[0]['tier']})")
    print(f"{'='*68}")
    for i, leg in enumerate(legs):
        label = f"Night {i//2+1}" if i % 2 else f"Day {i//2+1}"
        print(f"  {label}: d12({leg['category_roll']}) -> {leg['category']}  |  "
              f"d6({leg['result_roll']}) -> {leg['result']}")
    print()

    if not args.no_log:
        append_roll_log(args.campaign, args.route or args.region, legs)
        print(f"  (logged to reference/travel-encounters.md)\n")


if __name__ == "__main__":
    main()
