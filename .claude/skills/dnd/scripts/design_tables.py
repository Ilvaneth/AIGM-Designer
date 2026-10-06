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


@lru_cache(maxsize=1)
def tables_dir() -> Path:
    """data/design/ (resolved once per process: the skill does not move while a script runs)."""
    return data_dir() / "design"


def _file_name(name: str) -> str:
    return name if name.endswith(".yaml") else f"{name}.yaml"


REGISTRIES = ("claims.yaml",)      # no table: a registry the tables' rows name, never rolled


def list_tables() -> list[str]:
    """Committed table files (test scratch files start with `_`; a registry is no table)."""
    return sorted(p.name for p in tables_dir().glob("*.yaml") if not p.name.startswith("_") and p.name not in REGISTRIES)


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


# a row id that was renamed: a legacy birth that holds the old id still loads (build item 15: the age named for what
# was built in it lost the one built thing its id named)
ROW_ALIASES = {"age_lanterns": "age_of_thing",
               "hand_deceived_side": "hand_contest_side"}     # build item 19a: the hand's id names what the world sees


def _node(ref: str):
    """The mapping a reference names: the sub-table's for `file#sub`, the file's for a bare file; None if absent."""
    file_part, _, key = ref.partition("#")
    try:
        doc = load(file_part)
    except FileNotFoundError:
        return None
    if not key:
        return doc
    node = (doc.get("tables") or {}).get(key)
    return node if node is not None else doc.get(key)


def retired(ref: str) -> list[dict]:
    """A sub-table's `retired:` rows (build item 18): deleted from the roll, kept so a legacy birth that holds one
    still loads and renders. `rows()` never returns them; nothing draws them."""
    node = _node(ref)
    return [r for r in ((node or {}).get("retired") or []) if isinstance(r, dict) and r.get("id")] if isinstance(node, dict) else []


def rows_and_retired(ref: str) -> list[dict]:
    """The rows and the retired rows: the lookup of a rolled id, never a pool."""
    return rows(ref) + retired(ref)


def row(ref: str, row_id: str) -> dict | None:
    """One row by id; a retired row is found too (a legacy birth's)."""
    row_id = ROW_ALIASES.get(row_id, row_id)
    return next((r for r in rows_and_retired(ref) if r["id"] == row_id), None)


# ── the layers (build item 18a): what a table may fill ──

# frame: weighs tables, fills no slot · stage: where the story happens · story: a piece with a face, a want, an answer
# · texture: hangs on the story, never fills a story slot
LAYERS = ("frame", "stage", "story", "texture")


def layer(ref: str, row_id: str | None = None) -> str | None:
    """A row's layer: the row's own `layer` first, else its sub-table's, else its file's; a table's without a row."""
    if row_id is not None:
        r = row(ref, row_id)
        if r and r.get("layer"):
            return r["layer"]
    node = _node(ref) if "#" in ref else None
    if isinstance(node, dict) and node.get("layer"):
        return node["layer"]
    try:
        return load(ref.split("#", 1)[0]).get("layer")
    except FileNotFoundError:
        return None


def layered_refs() -> list[str]:
    """Every P0 and P1 table that must carry a layer: each file of REVIEWED_TABLES with its sub-tables, each
    `file#sub` entry as it stands."""
    out = []
    for name in REVIEWED_TABLES:
        if "#" in name:
            out.append(name)
            continue
        lists = all_row_lists(load(name))
        out += [f"{name}#{k}" if k else name for k in lists]
    return out


@lru_cache(maxsize=4)
def _row_refs_for(sig: tuple) -> dict:
    out = {}
    for name in list_tables():
        doc = load(name)
        for key, node in [("", doc)] + list((doc.get("tables") or {}).items()):
            if not isinstance(node, dict):
                continue
            ref = f"{name}#{key}" if key else name
            for r in list(_rows_of(node)) + [x for x in (node.get("retired") or []) if isinstance(x, dict) and x.get("id")]:
                out.setdefault(r["id"], ref)
    return out


def ref_of_row(row_id: str) -> str | None:
    """The table a row id belongs to (retired rows included)."""
    return _row_refs_for(_signature()).get(ROW_ALIASES.get(row_id, row_id))


# ── the arbiter's indexes (plan item 25: the script is the only arbiter of conflicts) ──

def _signature() -> tuple:
    """Committed table files and their mtimes, read on every call: an index is rebuilt the moment any table
    changes, even inside one process. One directory scan (os.scandir carries the mtimes) keeps it cheap enough for
    a many-seeds preroll."""
    with os.scandir(tables_dir()) as it:
        return tuple(sorted((e.name, e.stat().st_mtime_ns) for e in it
                            if e.name.endswith(".yaml") and not e.name.startswith("_")))


def _every_row():
    for name in list_tables():
        doc = load(name)
        for key, lst in all_row_lists(doc).items():
            ref = f"{name}#{key}" if key else name
            for r in lst:
                yield ref, r


# ── claims (build item 7c): tokens, the registry, the clashes ───────────────────────────────

CLAIM = "claim:"


def claims_registry() -> dict:
    """claims.yaml: topics and values, clash pairs, layout tokens, overridable defaults, combine lines."""
    try:
        return load("claims.yaml")
    except FileNotFoundError:
        return {}


def token(topic: str, value) -> str:
    return f"{CLAIM}{topic}={value}"


def claim_tokens(claims) -> list[str]:
    """`{topic: value}` (a row's or a role's `claims`) as context tokens."""
    return [token(t, v) for t, v in (claims or {}).items()]


@lru_cache(maxsize=4)
def _clash_map_for(sig: tuple) -> dict:
    out: dict[str, set] = {}
    for a, b in (claims_registry().get("clashes") or []):
        out.setdefault(CLAIM + a, set()).add(CLAIM + b)
        out.setdefault(CLAIM + b, set()).add(CLAIM + a)
    return {k: frozenset(v) for k, v in out.items()}


def clash_map() -> dict:
    """Token → the tokens it clashes with (declared pair by pair; nothing clashes by default)."""
    return _clash_map_for(_signature())


def clashing_tokens(claims) -> set:
    """Every token that clashes with one of these claims."""
    cm = clash_map()
    out: set = set()
    for t in claim_tokens(claims):
        out |= cm.get(t, frozenset())
    return out


@lru_cache(maxsize=4)
def _row_tokens_for(sig: tuple) -> dict:
    return {r["id"]: tuple(claim_tokens(r["claims"])) for _, r in _every_row() if r.get("claims")}


def row_tokens() -> dict:
    """Row id → the tokens its own `claims` set (a contest role's claims are added by the roller, when seated)."""
    return _row_tokens_for(_signature())


@lru_cache(maxsize=4)
def _conflicts_for(sig: tuple) -> dict:
    idx: dict[str, set] = {}
    cm = _clash_map_for(sig)
    for _, r in _every_row():
        others = list(r.get("conflicts_with") or [])
        for t in claim_tokens(r.get("claims")):          # a row conflicts with every token its claims clash with
            others += list(cm.get(t, ()))
        for other in others:
            idx.setdefault(r["id"], set()).add(other)
            idx.setdefault(other, set()).add(r["id"])
    return {k: frozenset(v) for k, v in idx.items()}


def conflict_index() -> dict:
    """Row id → the rows it may not appear with, made symmetric: A listing B also bars B after A."""
    return _conflicts_for(_signature())


def roll_header(ref: str) -> dict:
    """The `roll` header a reference draws under: the file's, overlaid by the sub-table's own."""
    file_part, _, key = ref.partition("#")
    try:
        doc = load(file_part)
    except FileNotFoundError:
        return {}
    head = dict(doc.get("roll") or {})
    node = (doc.get("tables") or {}).get(key) if key else None
    if isinstance(node, dict):
        head.update(node.get("roll") or {})
    return head


def own_roll_header(ref: str) -> dict:
    """The `roll` header the reference itself states: the sub-table's own for `file#sub`, the file's for a bare file.
    A file's header never speaks for a sub-table here (the caller's argument does, design_dice.usage)."""
    file_part, _, key = ref.partition("#")
    try:
        doc = load(file_part)
    except FileNotFoundError:
        return {}
    if not key:
        return dict(doc.get("roll") or {})
    node = (doc.get("tables") or {}).get(key)
    return dict(node.get("roll") or {}) if isinstance(node, dict) else {}


# ── the reviewed stamp (build item 7c: a row of a P0 or P1 table is stamped after the audit) ──

REVIEWED_TABLES = ("dials.yaml", "scale.yaml", "foundation.yaml", "trope-breaks.yaml", "tensions.yaml",
                   # build item 8: the signatures' new sub-tables (the old three leave with item 10, unstamped)
                   "signatures.yaml#people_lineage", "signatures.yaml#people_trait", "signatures.yaml#people_attitude",
                   "signatures.yaml#institution_form", "signatures.yaml#institution_practice",
                   "signatures.yaml#institution_sign", "signatures.yaml#institution_power",
                   "signatures.yaml#phenomenon_rule", "signatures.yaml#phenomenon_sign",
                   "signatures.yaml#phenomenon_limit", "signatures.yaml#phenomenon_user",
                   # build item 9: the secret and the villain (their stamps are kept under hashed keys, below)
                   "secrets.yaml#archetype", "secrets.yaml#chooser", "secrets.yaml#twist", "secrets.yaml#trail",
                   "secrets.yaml#keeping",     # build item 18d: the old twist table, renamed
                   "antagonists.yaml#visibility", "antagonists.yaml#villain_shape", "antagonists.yaml#origin",
                   "antagonists.yaml#break_tie",
                   # build item 18c: the threat
                   "antagonists.yaml#villain_family", "antagonists.yaml#power_source", "antagonists.yaml#goal",
                   "antagonists.yaml#weakness", "antagonists.yaml#lair_form", "antagonists.yaml#lair_where",
                   "antagonists.yaml#mask",     # build item 19b
                   # build item 11: the part bags; the lexicon, the patterns and the word lists are stamped by naming_stamps()
                   "naming.yaml#family")


def reviewed_path() -> Path:
    return tables_dir() / "reviewed.json"


def row_hash(row: dict) -> str:
    import hashlib
    body = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def stamp_key(row_id: str, secret: bool) -> str:
    """The key a row is stamped under: its id, or a hash of it for a row of a secret table. reviewed.json and the
    `unreviewed` listing sit where the owner, who is also the player, may read; neither names a secret row."""
    if not secret:
        return row_id
    import hashlib
    return "secret:" + hashlib.sha256(str(row_id).encode("utf-8")).hexdigest()[:16]


def reviewed_rows() -> dict:
    """Stamp key → the hash of the row's content, for every row of the P0 and P1 tables as they stand."""
    out = {}
    for name in REVIEWED_TABLES:                 # a whole file, or one sub-table as file#sub
        lists = {name: rows(name)} if "#" in name else {(f"{name}#{k}" if k else name): v for k, v in all_row_lists(load(name)).items()}
        for ref, lst in lists.items():
            secret = bool(roll_header(ref).get("secret"))
            for r in lst:
                out[stamp_key(r["id"], secret)] = row_hash(r)
    out.update(naming_stamps())
    return out


def naming_stamps() -> dict:
    """The name tables that are no row lists (build item 11): every root, the settlement tails, every tag, every
    pattern row and each word list, keyed `naming:<what>:<name>`."""
    doc = load("naming.yaml")
    lex = doc.get("lexicon") or {}
    out = {f"naming:root:{r['root']}": row_hash(r) for r in lex.get("roots") or []}
    out.update({f"naming:tag:{t['tag']}": row_hash(t) for t in lex.get("tags") or []})
    out["naming:settlement_tails"] = row_hash({"tails": lex.get("settlement_tails") or []})
    out["naming:lifeline_by_seat"] = row_hash(lex.get("lifeline_by_seat") or {})
    for kind, rows_ in (doc.get("patterns") or {}).items():
        out.update({f"naming:pattern:{r['id']}": row_hash(r) for r in rows_})
    out.update({f"naming:words:{k}": row_hash({"words": v}) for k, v in (doc.get("words") or {}).items()})
    return out


def read_stamps() -> dict:
    path = reviewed_path()
    return (json.loads(path.read_text(encoding="utf-8")).get("rows") or {}) if path.is_file() else {}


def unreviewed() -> dict:
    """Rows without a stamp or with a stamp that no longer matches: {'missing': [...], 'changed': [...], 'gone': [...]}."""
    now, stamps = reviewed_rows(), read_stamps()
    return {"missing": sorted(set(now) - set(stamps)),
            "changed": sorted(k for k in now if k in stamps and stamps[k] != now[k]),
            "gone": sorted(set(stamps) - set(now))}


def write_stamps() -> int:
    """`design_tables.py stamp`: run only after the development tab's audit of the tables."""
    rows_now = reviewed_rows()
    body = {"_meta": {"what": "row id -> hash of the row's content at its last audit (docs/p1-build-7c.md, inspection)",
                      "tables": list(REVIEWED_TABLES)},
            "rows": dict(sorted(rows_now.items()))}
    reviewed_path().write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(rows_now)


def records_usage(ref: str) -> bool:
    """Does an approved phase write this table's rows to used.json? (avoid-used, family waits, row waits)."""
    head = roll_header(ref)
    return bool(head.get("avoid_used") or head.get("family_wait") or head.get("row_wait"))


@lru_cache(maxsize=4)
def _secret_for(sig: tuple) -> frozenset:
    return frozenset(r["id"] for ref, r in _every_row() if roll_header(ref).get("secret"))


def secret_row_ids() -> frozenset:
    """Rows of the tables whose roll header says `secret: true`: a public log never names them."""
    return _secret_for(_signature())


def indexes() -> tuple[dict, frozenset]:
    """(conflict_index, secret_row_ids) on one signature read: the arbiter's per-draw lookup."""
    sig = _signature()
    return _conflicts_for(sig), _secret_for(sig)


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
    sub.add_parser("stamp")
    sub.add_parser("unreviewed")
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
    if a.verb == "stamp":
        print(f"design_tables: {write_stamps()} rows stamped in {reviewed_path().name}")
        return 0
    if a.verb == "unreviewed":
        state = unreviewed()
        for kind, ids in state.items():
            for rid in ids:
                print(f"  {kind:<8} {rid}")
        return 1 if any(state.values()) else 0
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
