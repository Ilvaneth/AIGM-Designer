#!/usr/bin/env python3
"""
design_names.py — the campaign's names, rolled by script (root-cause analysis 1, RC-13; the owner's ruling
2026-09-27: a generator gives the name and the pipeline uses it; no agent invents a person's or a god's name).

Person and god given names come from the campaign's naming languages (design/naming.json: onsets, nuclei, codas,
length), drawn with the campaign seed and spread within the campaign: an ending or an opening is shared by few names,
no name sits within a near-typo of another, and every candidate passes the door's own naming rules (the blacklists,
Turkish letters, names another campaign registered). dry-2 showed why: ten of its twenty-two person names ended in
-an, drawn by agents from one narrow bank.

The pool lives in design/dm-only/name-pool.json (the conductor never reads it). Every rendered prompt lists the unused
names; the registry door refuses a new public person or god whose given name is not on its language's list, marks a
used name, and refuses a secret entity a pool name (the lists are printed in conductor-readable prompts). Place names
are offered as candidates compounded from the language's roots; the writer picks one or composes in the same shape.

  design_names.py -c CAMP pool [--phase P2] [--attempt N]     draw the pool, or top it up; idempotent
  design_names.py -c CAMP show                                  the unused names per language
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_dice as dd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import design_dir, dm_only_dir, now_iso, read_json, stamp_meta, write_json_atomic  # noqa: E402

PERSON_TYPES = ("npc", "god", "pc")
SPARE_PERSONS = 6          # beyond the named-NPC band's top: P9 headroom, detail, a refused unit's retry
SPARE_GODS = 1
PLACE_CANDIDATES = 16
TOP_UP_BELOW = 5           # a language list with fewer unused names is topped up at the next preroll


def pool_path(campaign: str) -> Path:
    return dm_only_dir(campaign) / "name-pool.json"


def load_pool(campaign: str) -> dict | None:
    return read_json(pool_path(campaign))


def save_pool(campaign: str, pool: dict, written_by: str) -> None:
    stamp_meta(pool, campaign, written_by)
    write_json_atomic(pool_path(campaign), pool)


def languages(campaign: str) -> dict:
    return (read_json(design_dir(campaign) / "naming.json") or {}).get("languages") or {}


def given_of(name: str) -> str:
    words = re.split(r"[\s'’-]+", str(name or "").strip())
    return words[0] if words else ""


def distance(a: str, b: str) -> int:
    """Levenshtein distance, case-insensitive."""
    a, b = a.lower(), b.lower()
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


VOWELS = set("aeiouy")


def _raw_name(rng, lang: dict) -> str:
    """Syllables from the banks. An empty or vowel-led onset opens only the word, and a coda that carries a vowel
    (-ia, -us, -an) closes only the word: mid-word they stacked vowels (a first draft gave `Auroaureia`)."""
    lo, hi = dt.band(lang.get("length") or [2, 3])
    if lo == hi:
        lo = max(2, lo - 1)            # a fixed length made dry-2's names one shape; one syllable of play either way
    n = rng.randint(lo, hi)
    onsets = lang.get("onsets") or [""]
    inner = [o for o in onsets if o and o[0] not in VOWELS] or onsets
    codas = lang.get("codas") or [""]
    closed = [c for c in codas if c and not (set(c) & VOWELS)]
    word = ""
    for i in range(n):
        word += rng.choice(onsets if i == 0 else inner) + rng.choice(lang.get("nuclei") or ["a"])
        if i == n - 1:
            word += rng.choice(codas)
        elif closed and rng.random() < 0.2:
            word += rng.choice(closed)
    return word


def acceptable(name: str, lang: dict, taken: list[str], caps: dict, kind: str) -> bool:
    """The candidate's shape, the door's naming rules and the campaign's spread."""
    import registry
    low = name.lower()
    if not 3 <= len(low) <= 9 or not low.isalpha() or re.search(r"(.)\1\1", low) or re.search(r"[aeiouy]{3,}", low):
        return False
    if any(c and c in low for c in (lang.get("forbidden_clusters") or [])):
        return False
    if any(len(o) > 1 and low.count(o) > 1 for o in (lang.get("onsets") or [])):
        return False                                    # `Seraleotti`: one onset twice reads as a stutter
    if registry.naming_errors("probe", {"type": "npc" if kind == "person" else "god", "name": name},
                              registry.naming_blacklist(), registry.registered_elsewhere("")):
        return False
    if any(t.lower() == low for t in taken):
        return False
    near = 1 if len(low) < 5 else 2
    if any(distance(t, low) <= near for t in taken):
        return False
    if sum(1 for t in taken if t.lower()[-2:] == low[-2:]) >= caps["ending"]:
        return False
    if sum(1 for t in taken if t.lower()[:2] == low[:2]) >= caps["opening"]:
        return False
    return True


def draw_names(rng, lang: dict, n: int, taken: list[str], kind: str = "person") -> list[str]:
    """n given names from one language, spread against `taken` (the campaign's names so far) and each other."""
    total = max(1, n + len(taken))
    caps = {"ending": max(2, math.ceil(total * 0.12)), "opening": max(2, math.ceil(total * 0.15))}
    out: list[str] = []
    tries = 0
    while len(out) < n and tries < 6000:
        tries += 1
        if tries % 800 == 0:              # a narrow bank: loosen the spread one step rather than stop short
            caps = {k: v + 1 for k, v in caps.items()}
        raw = _raw_name(rng, lang)
        name = raw[:1].upper() + raw[1:]
        if acceptable(name, lang, taken + out, caps, kind):
            out.append(name)
    return out


def place_candidates(rng, lang: dict, n: int, taken: list[str]) -> list[str]:
    """Compounds of two roots of the language (`{Head}{tail}`, naming.yaml patterns.place), not yet a place name."""
    roots = [r for r in (lang.get("roots") or {}) if isinstance(r, str) and r.isalpha()]
    pairs = [(a, b) for a in roots for b in roots if a != b]
    rng.shuffle(pairs)
    have = {t.lower() for t in taken}
    out = []
    for a, b in pairs:
        name = a.capitalize() + b.lower()
        if len(name) > 12 or re.search(r"(.)\1\1", name.lower()):
            continue                                    # `Stilllantern`, `Lanternsilver`
        if name.lower() not in have and name not in out:
            out.append(name)
        if len(out) >= n:
            break
    return out


def campaign_names(campaign: str) -> tuple[list[str], list[str]]:
    """(the given names of every person and god in the registry, every place-like name)."""
    canon = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    persons = [given_of(e.get("name")) for e in canon.values() if e.get("type") in PERSON_TYPES and e.get("name")]
    places = [str(e.get("name")) for e in canon.values()
              if e.get("type") in ("place", "settlement", "region", "site", "district") and e.get("name")]
    return [p for p in persons if p], places


def ensure_pool(campaign: str, phase: str, attempt: int = 1) -> dict | None:
    """Draw the pool once the languages exist (P1 writes them), and top up a language that runs low."""
    langs = languages(campaign)
    if not langs:
        return None
    m = dm.load(campaign)
    sc = dt.scale_row(m["dials"]["scale"])
    want = {"person": dt.band(sc["named_npcs"])[1] + SPARE_PERSONS, "god": dt.band(sc["gods"])[1] + SPARE_GODS}
    pool = load_pool(campaign) or {"_meta": {"schema_version": 1, "campaign": campaign}, "languages": {}, "places": {}}
    persons, places = campaign_names(campaign)
    taken = persons + [e["name"] for L in pool["languages"].values() for k in ("person", "god") for e in L.get(k, [])]
    changed = False
    for lid, lang in langs.items():
        entry = pool["languages"].setdefault(lid, {"person": [], "god": []})
        for kind, n in want.items():
            unused = [e for e in entry[kind] if not e.get("used_by")]
            if entry[kind] and len(unused) >= TOP_UP_BELOW:
                continue
            need = n if not entry[kind] else n - len(unused)
            rng = dd.derive(m["seed"]["master"], phase, "names", f"{lid}.{kind}.{len(entry[kind])}", attempt)
            fresh = draw_names(rng, lang, need, taken, kind)
            entry[kind] += [{"name": x, "used_by": None, "drawn": phase} for x in fresh]
            taken += fresh
            changed = changed or bool(fresh)
        if lid not in pool["places"]:
            rng = dd.derive(m["seed"]["master"], phase, "names", f"{lid}.place", attempt)
            pool["places"][lid] = place_candidates(rng, lang, PLACE_CANDIDATES, places)
            changed = True
    if changed:
        save_pool(campaign, pool, f"design_names.py pool --phase {phase}")
    return pool


def pool_names(pool: dict, lang: str | None, kind: str) -> dict:
    """{name: used_by} for one language (or every language when the row names none) and kind."""
    out = {}
    for lid, L in (pool.get("languages") or {}).items():
        if lang and lang in pool["languages"] and lid != lang:
            continue
        for e in L.get(kind, []):
            out[e["name"]] = e.get("used_by")
    return out


def all_pool_names(pool: dict) -> set:
    return {e["name"].lower() for L in (pool.get("languages") or {}).values() for k in ("person", "god") for e in L.get(k, [])}


def mark_used(pool: dict, lang: str | None, kind: str, name: str, eid: str) -> None:
    for lid, L in (pool.get("languages") or {}).items():
        if lang and lang in pool["languages"] and lid != lang:
            continue
        for e in L.get(kind, []):
            if e["name"] == name and not e.get("used_by"):
                e["used_by"] = eid
                e["used_at"] = now_iso()
                return


def prompt_text(campaign: str, entity_id: str | None) -> str:
    """The prompts' Names paragraph: every language's unused names, rotated per entity so parallel writers start apart."""
    pool = load_pool(campaign)
    if not pool:
        return ""
    lines = ["**Names (rolled, never invented).** Give a new public person or god the next unused given name of their "
             "language from these lists, in order (a byname from the language's roots may follow: `Ilme Lampwright`); "
             "the door refuses a given name that is not on its language's list. A secret entity never takes a name from "
             "these lists (they are printed where the conductor can read them). A place takes one of its language's "
             "place candidates, or a compound of the language's roots in the same shape."]
    shift = sum(map(ord, entity_id or "")) if entity_id else 0
    for lid, L in (pool.get("languages") or {}).items():
        for kind in ("person", "god"):
            unused = [e["name"] for e in L.get(kind, []) if not e.get("used_by")]
            if unused:
                k = shift % len(unused)
                lines.append(f"- {lid} {kind}s: " + ", ".join(unused[k:] + unused[:k]))
        if pool.get("places", {}).get(lid):
            lines.append(f"- {lid} place candidates: " + ", ".join(pool["places"][lid]))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the campaign's rolled names (RC-13)")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    p = sub.add_parser("pool")
    p.add_argument("--phase", default="P2")
    p.add_argument("--attempt", type=int, default=1)
    sub.add_parser("show")
    a = ap.parse_args(argv)
    if a.verb == "pool":
        pool = ensure_pool(a.campaign, a.phase, a.attempt)
        if pool is None:
            print("design_names: no naming languages yet (P1 writes design/naming.json)", file=sys.stderr)
            return 1
    pool = load_pool(a.campaign) or {}
    for lid, L in (pool.get("languages") or {}).items():
        for kind in ("person", "god"):
            unused = sum(1 for e in L.get(kind, []) if not e.get("used_by"))
            print(f"design_names: {lid} {kind}s — {len(L.get(kind, []))} drawn, {unused} unused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
