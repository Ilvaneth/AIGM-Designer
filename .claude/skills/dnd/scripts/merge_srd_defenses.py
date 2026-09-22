#!/usr/bin/env python3
"""
merge_srd_defenses.py — add monster defenses to the bundled SRD dataset.

`build_srd.py`'s normalisers dropped every defensive field on the way from the
upstream sources into `data/dnd5e_srd.json`: all 334 monster records carried
AC, HP, speed and ability scores, but no damage immunities, resistances,
vulnerabilities or condition immunities. Silence in a lookup then read as "this
creature has none", and fights were resolved with immunities never applied --
devils taking fire damage, most visibly.

This script repairs the dataset from the SRD 5.1 text bundled at
`data/srd-5.1-yaml/` (OGL 1.0a -- see `00-legal.yaml`), which carries the full
stat blocks. It only ADDS fields to existing monster records; nothing else in
the dataset is touched.

Usage:
    python3 merge_srd_defenses.py [--dry-run] [--add-missing] [--quiet]

    --dry-run      report what would change, write nothing
    --add-missing  also append stat blocks that have no record in the JSON
    --quiet        summary only, no per-monster lines

A timestamped backup of the JSON is written before any change.
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import skill_root  # noqa: E402

YAML_FILES = ["11-monsters.yaml", "15-creatures.yaml", "16-npcs.yaml"]

# Stat-block line -> JSON field. Keys are the bold labels used by the SRD text.
FIELD_MAP = {
    "Damage Immunities": "damage_immunities",
    "Damage Resistances": "damage_resistances",
    "Damage Vulnerabilities": "damage_vulnerabilities",
    "Condition Immunities": "condition_immunities",
    "Saving Throws": "saving_throws",
    "Skills": "skills",
    "Senses": "senses",
}

_LABEL_RE = re.compile(r"^\*\*(?P<label>[^*]+)\*\*\s*(?P<value>.+)$")

# The two datasets name a handful of SRD entries differently.
ALIASES = {
    "elfdrow": "drow",
    "gnomedeepsvirfneblin": "deepgnomesvirfneblin",
}


def _norm(name: str) -> str:
    """Normalised key for matching names across the two datasets."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _is_stat_block(node) -> bool:
    """A stat block is a dict whose 'content' list opens with the italic
    'Size type, alignment' line and includes an Armor Class line."""
    if not isinstance(node, dict):
        return False
    content = node.get("content")
    if not isinstance(content, list) or not content:
        return False
    first = content[0]
    if not (isinstance(first, str) and first.startswith("*") and first.endswith("*")):
        return False
    return any(isinstance(x, str) and x.startswith("**Armor Class**") for x in content)


def _parse_block(content: list) -> dict:
    """Pull the defensive fields out of one stat block's content list."""
    out = {}
    for item in content:
        if not isinstance(item, str):
            continue
        m = _LABEL_RE.match(item.strip())
        if not m:
            continue
        field = FIELD_MAP.get(m.group("label").strip())
        if field:
            out[field] = m.group("value").strip()
    return out


def collect_blocks(yaml_dir: Path) -> dict:
    """{normalised name: {name, fields...}} for every stat block in the YAML."""
    import yaml  # imported here so --help works without PyYAML installed

    blocks = {}

    def walk(node, key=None):
        if _is_stat_block(node) and key:
            fields = _parse_block(node["content"])
            if fields:
                blocks[_norm(key)] = {"name": key, **fields}
            return
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, k)

    for fname in YAML_FILES:
        path = yaml_dir / fname
        if not path.is_file():
            print(f"  ! missing source file: {path}", file=sys.stderr)
            continue
        walk(yaml.safe_load(path.read_text(encoding="utf-8")))

    return blocks


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--add-missing", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    data_dir = skill_root() / "data"
    json_path = data_dir / "dnd5e_srd.json"
    blocks = collect_blocks(data_dir / "srd-5.1-yaml")
    print(f"  SRD YAML: {len(blocks)} stat blocks with defensive fields")

    dataset = json.loads(json_path.read_text(encoding="utf-8"))
    monsters = dataset["monsters"]
    by_name = {_norm(m["name"]): m for m in monsters}

    # The JSON splits some creatures into one record per form ("Vampire, Bat
    # Form"); the SRD text keeps a single stat block ("Vampire"). Index those
    # so one block can update every form that shares its defenses.
    by_base = {}
    for m in monsters:
        if "," in m["name"]:
            by_base.setdefault(_norm(m["name"].split(",")[0]), []).append(m)

    updated = unmatched = added = 0
    for key, block in sorted(blocks.items()):
        fields = {k: v for k, v in block.items() if k != "name"}
        key = ALIASES.get(key, key)
        record = by_name.get(key)

        if record is None and key in by_base:
            forms = by_base[key]
            changed_any = False
            for form in forms:
                if any(form.get(f) != v for f, v in fields.items()):
                    form.update(fields)
                    changed_any = True
            if changed_any:
                updated += 1
                if not args.quiet:
                    print(f"    + {block['name']} -> {len(forms)} form records")
            continue

        if record is None:
            unmatched += 1
            if args.add_missing:
                record = {"name": block["name"], "index": re.sub(r"[^a-z0-9]+", "-", block["name"].lower()).strip("-")}
                monsters.append(record)
                by_name[key] = record
                added += 1
            else:
                if not args.quiet:
                    print(f"    (no JSON record) {block['name']}")
                continue
        changed = [f for f, v in fields.items() if record.get(f) != v]
        if changed:
            record.update(fields)
            updated += 1
            if not args.quiet:
                print(f"    + {record['name']}: {', '.join(changed)}")

    print(f"\n  updated: {updated}   unmatched in JSON: {unmatched}"
          + (f"   added: {added}" if args.add_missing else ""))

    if args.dry_run:
        print("  --dry-run: nothing written")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = json_path.with_suffix(f".json.backup-{stamp}")
    shutil.copy2(json_path, backup)
    dataset.setdefault("_meta", {})["defenses_merged_at"] = datetime.now().isoformat(timespec="seconds")
    json_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  wrote {json_path}\n  backup {backup.name}")


if __name__ == "__main__":
    main()
