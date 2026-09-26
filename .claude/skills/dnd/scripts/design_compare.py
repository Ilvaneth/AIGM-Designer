#!/usr/bin/env python3
"""
design_compare.py — two births against each other (plan item 22.3, slice 1e).

Two `short` campaigns with different seeds must not be the same campaign: no name shared between their
registries (names and aliases, any type), no shared row of the tables that make a premise unique
(tensions, secrets, trope breaks, signatures, naming families, pantheon type), different map graphs and
different rosters. The script checks what a script can; it prints the two premises' public lines for the
LLM judge (prompts/play/judge_uniqueness.md) and never reads dm-only.

  design_compare.py A B [--json]

Exit codes: 0 distinct · 1 shared names or unique-table rows · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
from design_io import design_dir, read_json  # noqa: E402

UNIQUE_TABLES = ("tensions.yaml", "secrets.yaml", "trope-breaks.yaml", "signatures.yaml", "naming.yaml", "pantheon.yaml")


def projection(campaign: str) -> dict:
    return (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})


def names_of(pub: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for eid, e in pub.items():
        for n in [e.get("name")] + list(e.get("aliases") or []):
            if isinstance(n, str) and len(n.strip()) >= 3:
                out.setdefault(n.strip().lower(), eid)
    return out


def rows_of(campaign: str) -> set[tuple[str, str]]:
    m = dm.load(campaign)
    out = set()
    for r in m.get("dice_log") or []:
        table, row = r.get("table") or "", r.get("row_id")
        if not row or table in ("dice", "") or r.get("notation") in ("forced", "fixed") or str(r.get("label", "")).startswith(("dial.", "content_mix.")):
            continue
        out.add((table.split("#")[0], row))
    return out


def graph_shape(campaign: str) -> dict:
    mp = read_json(design_dir(campaign) / "map.json") or {}
    deg: Counter = Counter()
    for e in mp.get("edges", []):
        deg[e.get("from")] += 1
        deg[e.get("to")] += 1
    return {"nodes": len(mp.get("nodes", [])), "edges": len(mp.get("edges", [])), "regions": len(mp.get("regions") or {}),
            "degrees": sorted(deg.values(), reverse=True)}


def demographics(pub: dict) -> dict:
    species: Counter = Counter()
    gender: Counter = Counter()
    for e in pub.values():
        if e.get("type") == "npc":
            species[str(e.get("species") or "?").lower()] += 1
            gender[str(e.get("gender") or "?").lower()] += 1
    return {"species": dict(species), "gender": dict(gender)}


def premise_lines(pub: dict) -> dict:
    p = next((e for e in pub.values() if e.get("type") == "premise"), {})
    return {"name": p.get("name"), "question_tr": p.get("question_tr"), "pitch_tr": p.get("pitch_tr"), "summary": p.get("summary"),
            "signatures": [e.get("name") for e in pub.values() if e.get("type") == "signature"],
            "breaks": [e.get("name") for e in pub.values() if e.get("type") == "break"],
            "gods": [e.get("name") for e in pub.values() if e.get("type") == "god"]}


def compare(a: str, b: str) -> dict:
    pa, pb = projection(a), projection(b)
    na, nb = names_of(pa), names_of(pb)
    shared_names = sorted(set(na) & set(nb))
    ra, rb = rows_of(a), rows_of(b)
    shared_rows = sorted(ra & rb)
    unique_shared = [r for r in shared_rows if r[0] in UNIQUE_TABLES]
    ga, gb = graph_shape(a), graph_shape(b)
    da_, db_ = demographics(pa), demographics(pb)
    verdicts = {
        "names": "distinct" if not shared_names else f"{len(shared_names)} shared",
        "unique_tables": "distinct" if not unique_shared else f"{len(unique_shared)} shared row(s)",
        "other_tables": f"{len(shared_rows) - len(unique_shared)} shared row(s) of {len(ra | rb)} (tables that may repeat)",
        "map": "different" if ga != gb else "IDENTICAL SHAPE",
        "demographics": "different" if da_ != db_ else "IDENTICAL",
    }
    return {"a": a, "b": b, "shared_names": [(n, na[n], nb[n]) for n in shared_names], "shared_unique_rows": unique_shared,
            "shared_rows": shared_rows, "map": {"a": ga, "b": gb}, "demographics": {"a": da_, "b": db_},
            "premises": {"a": premise_lines(pa), "b": premise_lines(pb)}, "verdicts": verdicts,
            "distinct": not shared_names and not unique_shared}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="two births against each other")
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--json", action="store_true")
    x = ap.parse_args(argv)
    r = compare(x.a, x.b)
    if x.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"design_compare: {x.a} vs {x.b} — " + ("DISTINCT" if r["distinct"] else "NOT DISTINCT"))
        for k, v in r["verdicts"].items():
            print(f"  {k:<14} {v}")
        for n, ea, eb in r["shared_names"][:12]:
            print(f"    name {n!r}: {ea} / {eb}")
        for t, row in r["shared_unique_rows"][:12]:
            print(f"    row {t}: {row}")
        print("  premises for the judge (prompts/play/judge_uniqueness.md):")
        for side in ("a", "b"):
            p = r["premises"][side]
            print(f"    [{side}] {p.get('name')}: {p.get('question_tr') or p.get('summary')}")
            print(f"        signatures {', '.join(filter(None, p.get('signatures') or [])) or '—'} · breaks {', '.join(filter(None, p.get('breaks') or [])) or '—'}")
    return 0 if r["distinct"] else 1


if __name__ == "__main__":
    sys.exit(main())
