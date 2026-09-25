#!/usr/bin/env python3
"""
design_tables.py — the one reader of data/design/*.yaml, the designer's tables (plan item 17).

A table file is a YAML mapping: a header (`schema_version`, `table`, `consumed_by`, `plan`,
optional `roll`, `hooks_common`) and either a top-level `rows` list or a `tables` mapping of
named sub-tables, each with its own `rows`. A reference names a file and optionally a sub-table:

    rows("tensions.yaml")            the file's rows
    rows("dials.yaml#tone")          sub-table `tone`
    rows("_test_tensions.yaml")      any file under data/design/

Every row carries `id` (unique across all tables), `label` and `hooks`; `weight` is optional.
design_dice.py rolls through `rows`; design_manifest.py takes the dial value lists and the arc
shape from dials.yaml and scale.yaml; design_check.py reads the bands. Nothing else parses YAML.

CLI:
  design_tables.py list                     every table file with its sub-tables and row counts
  design_tables.py rows REF [--json]        the rows a reference resolves to
  design_tables.py show REF ROW_ID          one row
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import data_dir  # noqa: E402

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover - pyyaml is a stated dependency of the designer
    raise SystemExit("design_tables: pyyaml is required (py -m pip install pyyaml)") from exc

PHASES = tuple(f"P{i}" for i in range(10))
HOOK_TARGETS = PHASES + ("validator", "play")
DIAL_NAMES = ("scale", "tone", "magic", "era", "danger", "content_mix")


def tables_dir() -> Path:
    return data_dir() / "design"


def _file_name(name: str) -> str:
    return name if name.endswith(".yaml") else f"{name}.yaml"


def list_tables() -> list[str]:
    """Committed table files (test scratch files start with `_`)."""
    return sorted(p.name for p in tables_dir().glob("*.yaml") if not p.name.startswith("_"))


@lru_cache(maxsize=None)
def _load_cached(file_name: str, mtime_ns: int) -> dict:
    path = tables_dir() / file_name
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(doc, dict):
        raise ValueError(f"design_tables: {file_name} is not a mapping")
    return doc


def load(name: str) -> dict:
    """The parsed table file (cached by mtime); FileNotFoundError when it does not exist."""
    file_name = _file_name(name.split("#", 1)[0])
    path = tables_dir() / file_name
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return _load_cached(file_name, path.stat().st_mtime_ns)


def _rows_of(node) -> list[dict]:
    rows = node.get("rows") if isinstance(node, dict) else node
    return [r for r in (rows or []) if isinstance(r, dict) and r.get("id")]


def rows(ref: str) -> list[dict]:
    """Rows of `file.yaml` or `file.yaml#subtable`; [] when the file does not exist."""
    file_part, _, key = ref.partition("#")
    try:
        doc = load(file_part)
    except FileNotFoundError:
        return []
    if not key:
        return _rows_of(doc)
    node = (doc.get("tables") or {}).get(key)
    if node is None:
        node = doc.get(key)
    if node is None:
        raise KeyError(f"design_tables: {file_part} has no sub-table {key!r}")
    return _rows_of(node)


def all_row_lists(doc: dict) -> dict[str, list[dict]]:
    """Every row list in a parsed file, keyed by sub-table name ('' for top-level rows)."""
    out: dict[str, list[dict]] = {}
    if "rows" in doc:
        out[""] = _rows_of(doc)
    for key, node in (doc.get("tables") or {}).items():
        out[key] = _rows_of(node)
    return out


def row(ref: str, row_id: str) -> dict | None:
    return next((r for r in rows(ref) if r["id"] == row_id), None)


# ── the values other scripts derive from the tables ─────────────────────────────

def dial_values(dial: str) -> tuple:
    """The closed list a dial may take (dials.yaml#<dial>, each row's `value`)."""
    return tuple(r["value"] for r in rows(f"dials.yaml#{dial}"))


def dial_row(dial: str, value: str) -> dict | None:
    return next((r for r in rows(f"dials.yaml#{dial}") if r.get("value") == value), None)


def scale_row(scale: str) -> dict:
    found = next((r for r in rows("scale.yaml") if r.get("value") == scale), None)
    if found is None:
        raise KeyError(f"design_tables: scale.yaml has no row for scale {scale!r}")
    return found


def scale_shared() -> dict:
    return load("scale.yaml").get("shared") or {}


def arc_shape(scale: str) -> tuple[int, int, int]:
    """(acts, default chapter count, level-band span) for a scale."""
    r = scale_row(scale)
    return int(r["acts"]), int(r["chapters"]["default"]), int(r["level_span"])


def band(value) -> tuple[int, int]:
    """A scale.yaml number: [lo, hi] or a single exact count."""
    if isinstance(value, (list, tuple)):
        return int(value[0]), int(value[1])
    return int(value), int(value)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="read the designer's tables")
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("list")
    r = sub.add_parser("rows")
    r.add_argument("ref")
    r.add_argument("--json", action="store_true")
    s = sub.add_parser("show")
    s.add_argument("ref")
    s.add_argument("row_id")
    a = ap.parse_args(argv)

    if a.verb == "list":
        for name in list_tables():
            lists = all_row_lists(load(name))
            parts = ", ".join(f"{k or 'rows'}={len(v)}" for k, v in lists.items()) or "no rows"
            print(f"  {name:<22} {parts}")
        return 0
    if a.verb == "rows":
        found = rows(a.ref)
        if a.json:
            print(json.dumps(found, ensure_ascii=False, indent=2))
        else:
            for x in found:
                print(f"  {x['id']:<40} {x.get('label', '')}")
        return 0
    if a.verb == "show":
        found = row(a.ref, a.row_id)
        if found is None:
            print(f"design_tables: no row {a.row_id!r} in {a.ref}", file=sys.stderr)
            return 1
        print(json.dumps(found, ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
