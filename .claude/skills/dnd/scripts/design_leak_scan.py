#!/usr/bin/env python3
"""
design_leak_scan.py — the automated leak test of plan item 22.2 (slice 1e).

No sentence of any dm-only file and no secret entity's name or alias may appear in any artifact the
conductor, the DM's hot path or the player can see: the phase cards, the report, world.md, npcs.md, the
index, the primer and the player faces, travel-times.md, design.json, state.md, the session log, a playtest
transcript, and any file passed with --extra (a conductor's report, a Workflow journal). Hits are reported
as file + kind + length or first letter, never the text.

  design_leak_scan.py -c CAMP [--extra FILE ...] [--journal DIR] [--json]

Exit codes: 0 clean · 1 at least one hit · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_approval as da  # noqa: E402
from design_io import campaign_dir, design_dir  # noqa: E402

VISIBLE = ("world.md", "npcs.md", "state.md", "session-log.md", "design/report.md", "design/index.md",
           "design/player-primer.md", "design/travel-times.md", "design/design.json", "design/entities.json",
           "playtest/transcript.md", "playtest/persona.md")
VISIBLE_GLOBS = ("design/_approval/*.md", "design/player/*.md", "design/_prompts/**/*.md", "playtest/*.md")


def artifacts(campaign: str, extra: list[str], journal: str | None) -> list[Path]:
    root = campaign_dir(campaign)
    out: list[Path] = []
    for rel in VISIBLE:
        p = root / rel
        if p.is_file():
            out.append(p)
    for pattern in VISIBLE_GLOBS:
        out += sorted(p for p in root.glob(pattern) if p.is_file())
    for e in extra:
        p = Path(e)
        if p.is_file():
            out.append(p)
    if journal:
        out += sorted(p for p in Path(journal).rglob("*.jsonl") if p.is_file())
    seen: list[Path] = []
    for p in out:
        if p not in seen:
            seen.append(p)
    return seen


def scan(campaign: str, extra: list[str], journal: str | None) -> dict:
    names, sentences = da.secret_terms(campaign)
    results = []
    for path in artifacts(campaign, extra, journal):
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = da.leaks_in(text, names, sentences)
        results.append({"file": str(path.relative_to(campaign_dir(campaign))) if str(path).startswith(str(campaign_dir(campaign))) else str(path),
                        "hits": hits})
    total = sum(len(r["hits"]) for r in results)
    return {"campaign": campaign, "secret_names": len(names), "secret_sentences": len(sentences),
            "files": len(results), "hits": total, "results": [r for r in results if r["hits"]]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the automated leak test over every conductor-visible artifact")
    ap.add_argument("-c", "--campaign", required=True)
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--journal", help="a Workflow transcript folder: every .jsonl under it is scanned")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not (design_dir(a.campaign) / "dm-only").is_dir():
        print("design_leak_scan: no design/dm-only/ — nothing secret to protect", file=sys.stderr)
        return 2
    r = scan(a.campaign, a.extra, a.journal)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"design_leak_scan: {r['files']} artifact(s) against {r['secret_names']} secret name(s) and {r['secret_sentences']} dm-only sentence(s) — "
              + ("CLEAN" if not r["hits"] else f"{r['hits']} HIT(S)"))
        for res in r["results"]:
            print(f"  ✗ {res['file']}: " + "; ".join(res["hits"][:6]) + (" …" if len(res["hits"]) > 6 else ""))
    return 1 if r["hits"] else 0


if __name__ == "__main__":
    sys.exit(main())
