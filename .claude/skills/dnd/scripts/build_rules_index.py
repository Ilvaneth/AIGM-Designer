#!/usr/bin/env python3
"""
build_rules_index.py — build a searchable rules corpus from the bundled SRD text.

The dataset has always covered *things* (spells, monsters, items) but never the
rules prose itself: grappling, cover, falling, suffocation, exhaustion, resting,
travel pace, madness, curses. Those were answered from memory, which is exactly
where a ruleset drifts.

This reads the SRD 5.1 YAML at `data/srd-5.1-yaml/` (OGL 1.0a, see 00-legal.yaml)
and writes `data/dnd5e_rules.json`, which `lookup.py` exposes as the `rules`
category:

    python3 lookup.py rules "grapple"
    python3 lookup.py rules "cover"
    python3 lookup.py rules "exhaustion"

Usage:
    python3 build_rules_index.py [--dry-run] [--list]
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import skill_root  # noqa: E402

# Rule-bearing chapters. The monster/creature/NPC files are stat blocks and the
# class/race files are character options -- neither belongs in a rules lookup.
SOURCE_FILES = {
    "03-beyond1st.yaml": "Beyond 1st Level",
    "04-equipment.yaml": "Equipment",
    "06-mechanics.yaml": "Game Mechanics",
    "07-combat.yaml": "Combat",
    "08-spellcasting.yaml": "Spellcasting",
    "09-running.yaml": "Running the Game",
    "12-conditions.yaml": "Conditions",
    "14-planes.yaml": "Planes of Existence",
}

# A spell entry, not a rule: skip those in 08-spellcasting (they are already in
# the `spells` category, with structured fields).
_SPELL_MARKERS = ("**Casting Time:**", "**Range:**", "**Duration:**")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _render_table(table: dict) -> list:
    """Render a column-keyed table dict as aligned text rows."""
    if not isinstance(table, dict) or not table:
        return []
    headers = list(table.keys())
    columns = [table[h] if isinstance(table[h], list) else [table[h]] for h in headers]
    depth = max(len(c) for c in columns)
    rows = [headers]
    for i in range(depth):
        rows.append([str(c[i]) if i < len(c) else "" for c in columns])
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(headers))]
    out = []
    for n, row in enumerate(rows):
        out.append("  " + " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)).rstrip())
        if n == 0:
            out.append("  " + "-+-".join("-" * w for w in widths))
    return out


def _render(content) -> str:
    """Flatten a 'content' value (string, list, or nested table) into text."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return str(content)
    parts = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict) and "table" in item:
            parts.extend(_render_table(item["table"]))
        elif isinstance(item, dict):
            for k, v in item.items():
                parts.append(f"{k}: {_render(v)}")
    return "\n\n".join(p for p in parts if p)


def _is_spell(content) -> bool:
    text = _render(content)
    return sum(m in text for m in _SPELL_MARKERS) >= 2


def collect(yaml_dir: Path) -> list:
    import yaml  # imported here so --help works without PyYAML

    entries = []

    def walk(node, trail):
        if not isinstance(node, dict):
            return
        content = node.get("content")
        if content is not None and trail and not _is_spell(content):
            text = _render(content)
            if text.strip():
                entries.append({
                    "name": trail[-1],
                    "index": _slug("-".join(trail[-2:])),
                    "path": " > ".join(trail),
                    "source": trail[0],
                    "description": text,
                })
        for key, value in node.items():
            if key == "content" or not isinstance(value, dict):
                continue
            # The chapter label and the file's own top-level key are usually the
            # same words ("Combat" > "Combat"); don't repeat it in the path.
            if trail and _slug(key) == _slug(trail[-1]):
                walk(value, trail)
            else:
                walk(value, trail + [key])

    for fname, label in SOURCE_FILES.items():
        path = yaml_dir / fname
        if not path.is_file():
            print(f"  ! missing source file: {path}", file=sys.stderr)
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        # Each file is a single top-level chapter dict; label it by chapter.
        for key, value in (doc or {}).items():
            walk({key: value}, [label])

    return entries


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true", help="print every entry name")
    args = ap.parse_args()

    data_dir = skill_root() / "data"
    entries = collect(data_dir / "srd-5.1-yaml")

    # Deduplicate by path, keeping the longer text when a heading repeats.
    seen = {}
    for e in entries:
        prior = seen.get(e["path"])
        if prior is None or len(e["description"]) > len(prior["description"]):
            seen[e["path"]] = e
    entries = sorted(seen.values(), key=lambda e: e["path"])

    print(f"  {len(entries)} rule entries from {len(SOURCE_FILES)} SRD chapters")
    if args.list:
        for e in entries:
            print(f"    {e['path']}")

    if args.dry_run:
        print("  --dry-run: nothing written")
        return

    out = data_dir / "dnd5e_rules.json"
    out.write_text(json.dumps({
        "_meta": {
            "built_at": datetime.now().isoformat(timespec="seconds"),
            "source": "SRD 5.1 (OGL 1.0a) — data/srd-5.1-yaml/",
            "entries": len(entries),
        },
        "rules": entries,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
