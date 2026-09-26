#!/usr/bin/env python3
"""
load_budget.py — the load-lightness judge of plan item 22.4 (slice 1e), script-side.

What `/dm:dnd load` reads for a designed campaign (SKILL-commands.md, the load procedure): state.md,
world.md, the npcs.md index, every character sheet, the designer's load pack, the current chapter file,
every thread file, reference/full-campaign-history.md when present, plus the scene-context output the
graph prints. The sum must stay under a budget (default 40k tokens ≈ 140k characters of Turkish prose)
however large the bible grows: the bible is lazy, the hot path is not.

  load_budget.py -c CAMP [--budget-tokens 40000] [--json]

Exit codes: 0 under budget · 1 over budget · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import play_pack  # noqa: E402
from design_io import campaign_dir  # noqa: E402

CHARS_PER_TOKEN = 3.5


def measure(campaign: str) -> dict:
    root = campaign_dir(campaign)
    items: list[dict] = []

    def add(label: str, rel: str | None, text: str | None = None):
        if text is None:
            p = root / rel
            if not p.is_file():
                return
            text = p.read_text(encoding="utf-8", errors="replace")
        items.append({"what": label, "file": rel, "chars": len(text), "tokens": round(len(text) / CHARS_PER_TOKEN)})

    add("state.md", "state.md")
    add("world.md", "world.md")
    npcs = root / "npcs.md"
    if npcs.is_file():
        index_rows = "\n".join(l for l in npcs.read_text(encoding="utf-8", errors="replace").splitlines() if l.startswith("|"))
        add("npcs.md (index rows)", "npcs.md", index_rows)
    chars = root / "characters"
    if chars.is_dir():
        for p in sorted(chars.glob("*.md")):
            add(f"character {p.stem}", f"characters/{p.name}")
    add("reference/full-campaign-history.md", "reference/full-campaign-history.md")
    pack = play_pack.load_pack(campaign, None, None, None)
    add("designer load-pack", None, play_pack.load_pack_text(pack))
    if pack.get("chapter_file"):
        add(f"chapter {pack.get('chapter')}", pack["chapter_file"])
    for t in pack.get("threads") or []:
        if t.get("file"):
            add(f"thread {t['id']}", t["file"])
    total_chars = sum(i["chars"] for i in items)
    return {"campaign": campaign, "items": items, "chars": total_chars, "tokens": round(total_chars / CHARS_PER_TOKEN)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="what load reads, against a token budget")
    ap.add_argument("-c", "--campaign", required=True)
    ap.add_argument("--budget-tokens", type=int, default=40000)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    r = measure(a.campaign)
    r["budget_tokens"] = a.budget_tokens
    r["under_budget"] = r["tokens"] <= a.budget_tokens
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for i in sorted(r["items"], key=lambda x: -x["chars"]):
            print(f"  {i['tokens']:>7} tok  {i['what']}")
        print(f"load_budget: {r['tokens']:,} tokens ≈ {r['chars']:,} chars over {len(r['items'])} item(s); budget {a.budget_tokens:,} — "
              .replace(",", ".") + ("under budget" if r["under_budget"] else "OVER BUDGET"))
    return 0 if r["under_budget"] else 1


if __name__ == "__main__":
    sys.exit(main())
