#!/usr/bin/env python3
"""
design_names.py — the campaign's names, rolled by script (root-cause analysis 1, RC-13; the owner's ruling
2026-09-27: a generator gives the name and the pipeline uses it; no agent invents a person's or a god's name).

Person and god given names come from the campaign's naming languages (design/naming.json), drawn with the campaign
seed and spread within the campaign. A language that names a `bag` (build item 11: a part bag of naming.yaml#family)
joins one opening, a middle by the bag's chance and one ending under the shape rules of naming.yaml#rules.join; a
legacy language (onsets, nuclei, codas, length, no bag) keeps the syllable generator it was born with. Either way: an ending or an opening is shared by few names,
no name sits within a near-typo of another, and every candidate passes the door's own naming rules (the blacklists,
Turkish letters, names another campaign registered). dry-2 showed why: ten of its twenty-two person names ended in
-an, drawn by agents from one narrow bank.

The languages themselves are rolled by script at the end of P1's rolls (build item 11b, docs/p1-build-11.md): whose
each living language is, one part bag each from different sound groups, the old tongue's bag, each language's roots
(half from the tags it calls) and settlement tails, the calendar's month pattern and its own roots. The preroll writes
design/naming.json (public, stamped; no agent writes it), the four candidates of each signature name
(`naming.json#candidates`) and the stocks.

The pool lives in design/dm-only/name-pool.json (the conductor never reads it): per living language persons, gods,
places, regions, inns, buildings, ships and god epithets; the old tongue's sites; the calendar's months and days; the
cosmos's planes, moons, festivals, the ages' parts and the referents an age or an event is named for (build item 22n,
drawn after every other stock; the P2 roller takes and reserves them). Every
rendered prompt lists the unused names; the registry door refuses a new public person or god whose given name is not
on its language's list, marks a used name, and refuses a secret entity a pool name (the lists are printed in
conductor-readable prompts). A secret entity is named from the secret stock, design/dm-only/name-pool-secret.json:
drawn under its own label, disjoint from the public stocks, printed in no prompt and on no card; an agent lists it with
the `secret` verb. A legacy birth (its naming.json written by the P1 writer) keeps its pool and the way it was drawn.

  design_names.py -c CAMP pool [--phase P2] [--attempt N]     draw the pool, or top it up; idempotent
  design_names.py -c CAMP show                                  the unused names per language and stock
  design_names.py -c CAMP secret --lang L --kind K              the unused secret-stock names (K: person, god, place, site)
  design_names.py -c CAMP reroll --slot S [--onay]              the owner's four fresh candidates for one signature slot
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import re
import sys
from collections import Counter
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


def within(a: str, b: str, limit: int) -> bool:
    """Is the Levenshtein distance of two lower-case words at most `limit`? The same answer as `distance(a, b) <=
    limit`, with a row that passed the limit everywhere ending the count early."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > limit:
            return False
        prev = cur
    return prev[-1] <= limit


VOWELS = set("aeiouy")


def _raw_name(rng, lang: dict) -> str:
    """Syllables from the banks. An empty or vowel-led onset opens only the word, and a coda that carries a vowel
    (-ia, -us, -an) closes only the word: mid-word they stacked vowels (a first draft gave `Auroaureia`)."""
    lo, hi = dt.band(lang.get("length") or [2, 3])
    lo, hi = max(2, lo), max(2, hi)    # dry-3: a [1, 2] bank gave Sta, Ord, Ske
    if lo == hi and lo > 2:
        lo -= 1                        # a fixed length made dry-2's names one shape; one syllable of play
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


def join(a: str, b: str, vowel_join: bool) -> str | None:
    """Two parts joined (naming.yaml#rules.join): a doubled letter at the join is dropped; a vowel never meets a
    vowel; a `vowel_join` bag never joins consonant to consonant."""
    if a[-1].lower() == b[0].lower():
        b = b[1:]
    if not b or (a[-1].lower() in VOWELS and b[0].lower() in VOWELS):
        return None
    if vowel_join and a[-1].lower() not in VOWELS and b[0].lower() not in VOWELS:
        return None
    return a + b


def bag_shape_ok(word: str) -> bool:
    """At least five letters; no four consonants in a row; no two-letter chunk repeated at once and no three-letter
    chunk repeated anywhere."""
    low = word.lower()
    return not (len(low) < 5 or re.search(r"[^aeiouy]{4}", low) or re.search(r"(..).?\1", low) or re.search(r"(...).*\1", low))


def bag_of(lang: dict) -> dict | None:
    """The part bag a language names (naming.yaml#family), or None for a legacy language."""
    key = (lang or {}).get("bag")
    return dt.row("naming.yaml#family", key) if key else None


def _bag_name(rng, bag: dict) -> str | None:
    """One opening, a middle by the bag's chance, one ending; None when a join or the shape refuses it."""
    vj = bool(bag.get("vowel_join"))
    word = rng.choice(bag["openings"])
    if bag.get("middles") and rng.random() < float(bag.get("middle_chance") or 0):
        word = join(word, rng.choice(bag["middles"]), vj)
        if not word:
            return None
    word = join(word, rng.choice(bag["endings"]), vj)
    return word if word and bag_shape_ok(word) else None


def real_given() -> frozenset:
    """naming.yaml#blacklist.real_given: real given names a bag can spell (the generator's filter; off for a
    `real_ok` bag)."""
    return frozenset(str(x).lower() for x in (dt.load("naming.yaml").get("blacklist") or {}).get("real_given") or [])


def plain_words() -> frozenset:
    """naming.yaml#blacklist.plain_words: plain words a bag can spell (the generator's filter; on for every bag)."""
    return frozenset(str(x).lower() for x in (dt.load("naming.yaml").get("blacklist") or {}).get("plain_words") or [])


def acceptable(name: str, lang: dict, taken: list[str], caps: dict, kind: str, bag: dict | None = None,
               registered: set | None = None, real: frozenset | None = None, plain: frozenset | None = None,
               near: int | None = None) -> bool:
    """The candidate's shape, the door's naming rules and the campaign's spread. For a bag language the plain-word
    filter too, and the real-name filter unless the bag says `real_ok`; a bag has no `forbidden_clusters` and no
    `onsets` to check. `near`: the near-typo distance kept from every taken name (persons: 2 from five letters on;
    the old tongue's site words keep 1, a stock three times the sites of an epic campaign must come from one bag)."""
    import registry
    low = name.lower()
    if not 4 <= len(low) <= 9 or not low.isalpha() or re.search(r"(.)\1\1", low) or re.search(r"[aeiouy]{3,}", low):
        return False
    if bag is not None and low in (plain_words() if plain is None else plain):
        return False
    if bag is not None and not bag.get("real_ok") and low in (real_given() if real is None else real):
        return False
    if any(c and c in low for c in (lang.get("forbidden_clusters") or [])):
        return False
    if any(len(o) > 1 and low.count(o) > 1 for o in (lang.get("onsets") or [])):
        return False                                    # `Seraleotti`: one onset twice reads as a stutter
    # the checks below are independent; the cheap ones stand first (build item 11a: a bag is asked thousands of times)
    if sum(1 for t in taken if t.lower()[-2:] == low[-2:]) >= caps["ending"]:
        return False
    if sum(1 for t in taken if t.lower()[:2] == low[:2]) >= caps["opening"]:
        return False
    if any(t.lower() == low or t.lower().startswith(low) or low.startswith(t.lower()) for t in taken):
        return False                                    # dry-3: Ske beside Skeik
    if registry.naming_errors("probe", {"type": "npc" if kind == "person" else "god", "name": name},
                              registry.naming_blacklist(), registry.registered_elsewhere("") if registered is None else registered):
        return False
    near = (1 if len(low) < 5 else 2) if near is None else near
    if any(abs(len(t) - len(low)) <= near and within(t.lower(), low, near) for t in taken):
        return False
    return True


def draw_names(rng, lang: dict, n: int, taken: list[str], kind: str = "person", near: int | None = None) -> list[str]:
    """n given names from one language, spread against `taken` (the campaign's names so far) and each other."""
    total = max(1, n + len(taken))
    caps = {"ending": max(2, math.ceil(total * 0.12)), "opening": max(2, math.ceil(total * 0.15))}
    import registry
    bag = bag_of(lang)
    registered, real, plain = registry.registered_elsewhere(""), real_given(), plain_words()
    out: list[str] = []
    tries = 0
    while len(out) < n and tries < (max(8000, 120 * n) if bag else 6000):
        tries += 1
        if not bag and tries % 800 == 0:  # a narrow legacy bank: loosen the spread one step rather than stop short
            caps = {k: v + 1 for k, v in caps.items()}
        raw = _bag_name(rng, bag) if bag else _raw_name(rng, lang)
        if not raw:
            continue
        name = raw[:1].upper() + raw[1:]
        if acceptable(name, lang, taken + out, caps, kind, bag=bag, registered=registered, real=real, plain=plain, near=near):
            out.append(name)
    return out


def place_candidates(rng, lang: dict, n: int, taken: list[str]) -> list[str]:
    """A legacy language's place candidates: compounds of two of its roots (`{Head}{tail}`), not yet a place name."""
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


# ── build item 11b: the languages, the roots and the calendar, rolled at the end of P1's rolls ────────────────

LEX = "naming.yaml#lexicon"
FAMILY = "naming.yaml#family"
ADJECTIVE_TAGS = ("colour", "direction and age")
NO_COMMON_TONGUE = "break_no_common_tongue"       # language 2 is the contest's other side's
OWN_LANGUAGE = "isign_own_language"               # language 3 is the institution's
# a language has no proper name (decision 31): its label says whose it is
LANGUAGE_LABELS = {"people": "the people's tongue", "common": "the common tongue", "other_side": "the other side's tongue",
                   "institution": "the institution's tongue", "old": "the old tongue"}


def language_label(lid: str, lang: dict, people_name: str | None = None) -> str:
    """A language's label; the people's is "the <name> tongue" once the people is named."""
    if lid == "people" and people_name:
        return f"the {people_name} tongue"
    return str((lang or {}).get("label") or LANGUAGE_LABELS.get(lid, lid))
SLOTS = ("people", "institution", "phenomenon")
# a living language's compound stocks: the stock, its patterns, the count of scale.yaml its size follows
STOCKS = (("places", ("pattern_place_settlement", "pattern_place_natural"), "settlements"),
          ("regions", ("pattern_place_region",), "regions"),
          ("inns", ("pattern_place_inn",), "settlements"),
          ("buildings", ("pattern_place_building",), "settlements"),
          ("ships", ("pattern_ship_root", "pattern_ship_colour_animal"), "settlements"),
          ("epithets", ("pattern_epithet_bearer", "pattern_epithet_parent", "pattern_epithet_lord", "pattern_epithet_one"), "gods"))
SECRET_KINDS = ("person", "god", "place", "site")
SECRET_SIZES = {"god": 2, "place": 4, "site": 6}  # per language; persons follow the scale's antagonists


def secret_path(campaign: str) -> Path:
    return dm_only_dir(campaign) / "name-pool-secret.json"


def naming_path(campaign: str) -> Path:
    return design_dir(campaign) / "naming.json"


def draw_rules() -> dict:
    return dt.load("naming.yaml")["rules"]["draw"]


def lexicon_roots() -> list[dict]:
    return dt.load("naming.yaml")["lexicon"]["roots"]


def is_adjective(root: dict) -> bool:
    """naming.yaml#rules.adjectives: a root whose first tag is `colour` or `direction and age`, or one marked so."""
    return bool(root.get("adjective")) or (bool(root["tags"]) and root["tags"][0] in ADJECTIVE_TAGS)


def slot_fits(root: dict, slot: str) -> bool:
    """A root for a slot of a draw or a pattern: `tail` (a natural tail), `any`, `head`, `noun` (a head, no adjective)."""
    if slot == "any":
        return True
    if slot == "tail":
        return root["pos"] in ("tail", "either")
    return root["pos"] in ("head", "either") and (slot == "head" or not is_adjective(root))


def _tag_rows() -> list[dict]:
    return dt.load("naming.yaml")["lexicon"]["tags"]


def land_tags() -> set:
    """The tags only a palette kind calls (decision 6's land tags; `animal` is a livelihood tag the giant bones also call)."""
    return {t["tag"] for t in _tag_rows() if (t.get("called_by") or {}).get("palette") and not (t.get("called_by") or {}).get("lifeline_family")}


def palette_tags(kinds) -> set:
    """Every tag one of these palette kinds calls."""
    kinds = set(kinds or [])
    return {t["tag"] for t in _tag_rows() if kinds & set((t.get("called_by") or {}).get("palette") or [])}


def lifeline_tags(family: str, seat_kinds) -> set:
    """The tag the lifeline's family calls; the water family calls fresh water or sea by the kind the lifeline sits on."""
    out = {t["tag"] for t in _tag_rows() if family in ((t.get("called_by") or {}).get("lifeline_family") or [])}
    by_seat = (dt.load("naming.yaml")["lexicon"].get("lifeline_by_seat") or {}).get(family) or []
    return out | (palette_tags(seat_kinds) & set(by_seat))


def kinds_at(foundation: dict, seat: str | None) -> list[str]:
    """The palette kind(s) a seat of the layout lies on: a part's kind, an `along:<kind>` node, or every kind along."""
    layout = foundation["layout"]
    if not seat:
        return []
    if seat.startswith("along:"):
        return [seat.split(":", 1)[1]]
    if seat == "along":
        return list(layout.get("along") or [])
    return [layout["parts"][seat]] if seat in layout["parts"] else []


def called_tags(owner: str, foundation: dict, identity: dict) -> set:
    """What a language calls (decision 8). The people's: the lifeline's family tag and the land tag(s) of the kind
    the people sits on (its role's seat when it holds a role, else the lifeline's part). Every other living
    language: every land tag a palette kind calls."""
    import design_foundation as fd
    if owner != "people":
        return palette_tags(list(foundation["palette"]) + list(foundation["palette_extra"]))
    life = foundation["lifeline"]
    life_kinds = kinds_at(foundation, life["seat"])
    role = identity["people"].get("role")
    seat = foundation["layout"]["contests"][0]["seats"].get(role) if role else None
    home = kinds_at(foundation, seat) or life_kinds
    return lifeline_tags(fd.rows_by_id("lifeline")[life["id"]]["family"], life_kinds) | palette_tags(home)


def _is_called(root: dict, called: set, barred: set) -> bool:
    """In the called half: the root carries a called tag, and no land tag the campaign's palette calls nowhere
    (`gull` is sea and animal: an animal lifeline does not bring it to a landlocked world's called half)."""
    tags = set(root["tags"])
    return bool(tags & called) and not (tags & barred)


def _pick_roots(rng, slots: list[str], quota: int, is_called, taken: set, used: set, extra=None):
    """One root per slot. While the quota lasts a slot is drawn among the called roots that fit it, else (and after)
    among every root that fits. A root another campaign drew waits while a fresh one fits. Returns (roots, the ones
    drawn as called, the quota the called pool could not fill, the slots drawn from spent roots)."""
    rows = lexicon_roots()
    picked: list[str] = []
    called: list[str] = []
    spent = 0
    for slot in slots:
        fit = [r for r in rows if r["root"] not in taken and r["root"] not in picked and slot_fits(r, slot)
               and (extra is None or extra(r))]
        if not fit:
            raise SystemExit(f"design_names: the lexicon holds no root for a `{slot}` slot — a table fault")
        fresh = [r for r in fit if r["root"] not in used]
        spent += 0 if fresh else 1
        pool = fresh or fit
        mine = [r for r in pool if is_called(r)] if quota > 0 else []
        if mine:
            quota -= 1
        r = rng.choice(mine or pool)
        picked.append(r["root"])
        if mine:
            called.append(r["root"])
    return picked, called, quota, spent


def joins(root: str, suffix: str, max_letters: int = 12) -> bool:
    """A root and a literal tail as one word: no doubled letter at the join, the two differ, the length holds."""
    word = root + suffix
    return root[-1] != suffix[0] and root != suffix and len(word) <= max_letters and not re.search(r"(.)\1\1", word)


def _items(R, label: str, items: list, notation: str = "draw", **extra) -> dict:
    """A public record of a draw that names no table row: its `items`."""
    rec = R._record(label, LEX)
    rec.update({"notation": notation, "items": list(items)}, **extra)
    R._keep(rec, False)
    return rec


def language_owners(scale: str, identity: dict) -> list[str]:
    """Whose the living languages are (section 8). Language 1: the signature people's. Language 2: the common
    tongue; with "there is no common tongue" rolled, the contest's other side's. Language 3 (standard, epic): the
    other side's; with "they speak only their own language" rolled, the institution's. When language 2 is already the
    other side's and the sign is not rolled, there is no third living language."""
    no_common = any(b["id"] == NO_COMMON_TONGUE for b in identity["trope_breaks"])
    owners = ["people", "other_side" if no_common else "common"]
    if int(draw_rules()["living_languages"][scale]) >= 3:
        if identity["institution"]["sign"] == OWN_LANGUAGE:
            owners.append("institution")
        elif not no_common:
            owners.append("other_side")
    return owners


def roll(R, dials: dict, foundation: dict, identity: dict) -> dict:
    """The naming rolls, all public, after the secret, the villain and the mechanic gate (docs/p1-build-11.md,
    sections 7-10): the living languages and whose they are, one part bag each from different sound groups, the old
    tongue's bag from a group none of them uses, each living language's roots and settlement tails, the calendar's
    month pattern and its own roots. Returns the languages and the calendar as `design/naming.json` keeps them."""
    rules = draw_rules()
    scale = dials["scale"]
    owners = language_owners(scale, identity)

    # the bags: through the arbiter, usage waits, the groups differ
    bags = {r["id"]: r for r in dt.rows(FAMILY)}
    groups: set = set()
    langs: dict = {}
    for n, owner in enumerate(owners + ["old"], 1):
        rec = R.table("naming_family.old" if owner == "old" else f"naming_family.{n}", FAMILY,
                      where=lambda r: r["group"] not in groups, why="a sound group no language of the campaign uses")
        bag = bags[rec["row_id"]]
        groups.add(bag["group"])
        langs[owner] = {"owner": owner, "label": LANGUAGE_LABELS.get(owner, owner), "bag": bag["id"], "group": bag["group"],
                        "roots": [], "called": [], "settlement_tails": []}
        if owner == "other_side":             # the main contest's side the people does not hold; role b when it holds none
            langs[owner]["role"] = {"a": "b", "b": "a"}.get(identity["people"].get("role"), "b")

    # the roots: half from the tags the language calls, the floor by construction, no root in two languages
    kinds = list(foundation["palette"]) + list(foundation["palette_extra"])
    barred = land_tags() - palette_tags(kinds)
    used = set(dd.used_values(R.campaign, LEX)) if R.campaign else set()
    n_roots, floor = int(rules["roots_per_language"][scale]), int(rules["head_floor"][scale])
    nouns, tails = int(rules["noun_heads"]), int(rules["natural_tails"])
    share = float(rules["called_share"])
    taken: set = set()
    all_tails = list(dt.load("naming.yaml")["lexicon"]["settlement_tails"])
    for owner in owners:
        calls = called_tags(owner, foundation, identity)
        slots = ["noun"] * nouns + ["head"] * (floor - nouns) + ["tail"] * tails + ["any"] * (n_roots - floor - tails)
        rng = dd.derive(R.master, R.phase, LEX, f"naming_roots.{owner}", R.attempt)
        rng.shuffle(slots)
        roots, called, short, spent = _pick_roots(rng, slots, math.ceil(n_roots * share),
                                                  lambda r, calls=calls: _is_called(r, calls, barred), taken, used)
        taken |= set(roots)
        _items(R, f"naming_roots.{owner}", roots, called=called, called_short=short, lexicon_spent=spent, used_keys={LEX: roots})
        langs[owner].update({"roots": roots, "called": called, "called_tags": sorted(calls), "called_short": short})
        rng = dd.derive(R.master, R.phase, LEX, f"naming_tails.{owner}", R.attempt)
        order = list(all_tails)
        rng.shuffle(order)
        mine: list[str] = []
        for t in order:
            if len(mine) < int(rules["settlement_tails"]) and all(
                    len(set(mine + [t]) & set(langs[o]["settlement_tails"])) <= int(rules["shared_tails_max"])
                    for o in owners if o != owner):
                mine.append(t)
        _items(R, f"naming_tails.{owner}", mine)
        langs[owner]["settlement_tails"] = mine

    # the calendar: one month pattern, then its own roots from the nature tags, never an adjective
    cal = rules["calendar"]
    patterns = dt.load("naming.yaml")["patterns"]
    rollable = [p for p in patterns["month"] if p.get("rollable")]
    rng = dd.derive(R.master, R.phase, LEX, "naming_calendar.pattern", R.attempt)
    face = rng.randint(1, len(rollable))
    pattern = rollable[face - 1]
    _items(R, "naming_calendar.pattern", [pattern["id"]], notation=f"d{len(rollable)}", raw=face)
    cal_tags, real_words, no_day = set(cal["tags"]), set(cal["real_words"]), set(cal["not_days"])
    seasons_barred = {"day": True, "month": pattern["id"] in (cal.get("not_months_under") or [])}
    calls = palette_tags(kinds)
    max_letters = int(rules["compound_max_letters"])
    out_cal = {"month_pattern": pattern["id"]}
    for key, count, suffix in (("month", int(cal["month_roots"]), _suffix(pattern)), ("day", int(cal["day_roots"]), _suffix(patterns["day"][0]))):
        rng = dd.derive(R.master, R.phase, LEX, f"naming_calendar.{key}s", R.attempt)
        roots, called, short, spent = _pick_roots(
            rng, ["noun"] * count, math.ceil(count * share), lambda r: _is_called(r, calls, barred), taken, used,
            extra=lambda r, suffix=suffix, key=key: bool(set(r["tags"]) & cal_tags) and joins(r["root"], suffix, max_letters)
            and (r["root"] + suffix) not in real_words and not (seasons_barred[key] and r["root"] in no_day))
        taken |= set(roots)
        _items(R, f"naming_calendar.{key}s", roots, called=called, called_short=short, lexicon_spent=spent, used_keys={LEX: roots})
        out_cal.update({f"{key}_roots": roots, f"{key}_called": called})
    return {"rolled": True, "languages": langs, "calendar": out_cal}


# ── the patterns filled: stocks and candidates ───────────────────────────────────────────────────────────────

def _suffix(pattern: dict) -> str:
    """The literal a joined pattern ends in (`month`, `moon`, `fall`, `day`)."""
    return next(p["lit"] for p in reversed(pattern["parts"]) if "lit" in p)


def _options(part: dict, pattern: dict, env: dict) -> list[tuple]:
    """What may fill one part of a pattern: (text, the root it is or stands on, capitalise it when written apart)."""
    if "lit" in part:
        return [(part["lit"], None, False)]
    if "one_of" in part:
        return [o for sub in part["one_of"] for o in _options(sub, pattern, env)]
    if "root" in part:
        out = []
        for r in env["whole"] if pattern.get("whole_lexicon") else env["roots"]:
            if not slot_fits(r, part["root"]) or (part.get("adjective") is False and is_adjective(r)):
                continue
            if part.get("tags") and not set(r["tags"]) & set(part["tags"]):
                continue
            if part.get("creature") and r.get("creature") is False:      # `bone`, `hoof`: of a creature, not one
                continue
            if part.get("only") and r["root"] not in part["only"]:
                continue
            out.append((r["root"], r["root"], True))
        return out
    if part.get("settlement_tail"):
        return [(t, None, False) for t in env.get("tails") or []]
    if "word" in part:
        kinds = set(env.get("kinds") or [])      # a word row with `requires` follows the campaign's palette
        words = [w if isinstance(w, str) else w["word"] for w in dt.load("naming.yaml")["words"][part["word"]]
                 if isinstance(w, str) or not w.get("requires") or kinds & set(w["requires"].get("any_of") or [])]
        if part.get("plural_ok"):
            words += [w + "s" for w in words]
        return [(w, None, bool(part.get("capital"))) for w in words]
    if part.get("form_word"):
        return [(w, None, False) for w in env.get("form_words") or []]
    if "name" in part:
        return [(name, head, False) for name, head in env.get(part["name"] + "s") or []]
    if part.get("bag_word"):
        return [(w, None, False) for w in env.get("bag_words") or []]
    return []


def _compose(pattern: dict, combo: tuple, max_letters: int) -> str | None:
    """One name from one choice per part. Joined: one word, no doubled letter at a join, the parts differ, the length
    holds (decision 37). Apart: the parts as written, a root capitalised."""
    if pattern["join"] == "joined":
        texts = [c[0].lower() for c in combo]
        if any(a[-1] == b[0] or a == b for a, b in zip(texts, texts[1:])):
            return None
        word = "".join(texts)
        if len(word) > max_letters or re.search(r"(.)\1\1", word):
            return None
        return (pattern.get("article") or "") + word.capitalize()
    return "".join(text[:1].upper() + text[1:] if cap else text for text, _, cap in combo)


def _names(pattern: dict, env: dict, rng, max_letters: int):
    """Every name a pattern gives in this environment, in a rolled order: (name, its head root or None)."""
    options = [_options(p, pattern, env) for p in pattern["parts"]]
    if any(not o for o in options):
        return
    combos = list(itertools.product(*options))
    rng.shuffle(combos)
    for combo in combos:
        roots = [c[1] for c in combo if c[1]]
        texts = [c[0].strip().lower() for c in combo if c[0].strip()]
        if len(set(roots)) < len(roots) or len(set(texts)) < len(texts):      # naming.yaml#rules.parts_differ
            continue
        name = _compose(pattern, combo, max_letters)
        if name:
            yield name, (roots[0] if roots else None)


def name_checker(registered: set | None = None):
    """Is a pooled compound allowed? The `real_places` filter, every naming rule of the door (the blacklists, Turkish
    letters) and the names another campaign registered."""
    import registry
    bl = registry.naming_blacklist()
    registered = registry.registered_elsewhere("") if registered is None else registered
    real = frozenset(str(x).lower() for x in bl.get("real_places") or [])

    def ok(name: str) -> bool:
        low = name.lower()
        bare = low[4:] if low.startswith("the ") else low
        if low in real or bare in real or low in registered or bare in registered:
            return False
        return not registry.naming_errors("probe", {"type": "place", "name": name}, bl, registered)
    return ok


def _draw_stock(rng, patterns: list[dict], env: dict, n: int, seen: set, ok, cap: int, uses: Counter | None = None,
                distinct_roots: bool = False) -> list[dict]:
    """n names, the patterns taking turns: no name twice in the campaign, one head root in at most `cap` names of the
    stock (in one name only with `distinct_roots`)."""
    max_letters = int(draw_rules()["compound_max_letters"])
    uses = Counter() if uses is None else uses
    cap = 1 if distinct_roots else cap
    streams = [_names(p, env, rng, max_letters) for p in patterns]
    ids = [p["id"] for p in patterns]
    out: list[dict] = []
    while streams and len(out) < n:
        for i in range(len(streams) - 1, -1, -1):
            if len(out) >= n:
                break
            for name, head in streams[i]:
                if name.lower() in seen or (head and uses[head] >= cap) or not ok(name):
                    continue
                seen.add(name.lower())
                if head:
                    uses[head] += 1
                out.append({"name": name, "head": head, "pattern": ids[i]})
                break
            else:
                del streams[i], ids[i]
    return out


def scale_needs(sc: dict) -> dict:
    """What a scale can use, from scale.yaml (the bands' tops)."""
    return {"settlements": sum(dt.band(v)[1] for v in sc["settlements"].values()), "regions": dt.band(sc["regions"])[1],
            "sites": dt.band(sc["sites"]["count"])[1], "gods": dt.band(sc["gods"])[1], "persons": dt.band(sc["named_npcs"])[1],
            "antagonists": sum(dt.band(v)[1] for v in sc["antagonists"].values())}


def stock_sizes(scale: str, living: int) -> dict:
    """The size of every stock. Per living language: persons as before item 11 (the band's top and the spares), and
    for the rest the language's share of `stock_factor` times the scale's need, so the campaign's languages together
    hold at least three times what the scale can use (decision 44). The old tongue's sites carry the whole of it."""
    rules = draw_rules()
    factor = int(rules["stock_factor"])
    need = scale_needs(dt.scale_row(scale))
    per = lambda key: math.ceil(factor * need[key] / max(1, living))
    out = {"person": need["persons"] + SPARE_PERSONS, "god": max(need["gods"] + SPARE_GODS, per("gods")),
           "sites": factor * need["sites"],
           "secret_person": max(4, math.ceil(factor * need["antagonists"] / max(1, living)))}
    for key, _, by in STOCKS:
        out[key] = per(by)
    out["ships"] = max(4, math.ceil(out["ships"] / 2))
    return out


def _want(entries: list, target: int) -> int:
    """How many names a stock draws now: all of them when empty, the gap when it runs low, else none."""
    if not entries:
        return target
    unused = sum(1 for e in entries if not e.get("used_by"))
    return target - unused if unused < min(TOP_UP_BELOW, target) else 0


def living_languages(naming: dict) -> list[str]:
    return [lid for lid, L in naming["languages"].items() if L.get("owner") != "old"]


def has_water(foundation: dict) -> bool:
    """Does the palette hold a sea or fresh-water kind? (ships, and the travelling form's `Fleet`)"""
    return bool(palette_tags(list(foundation["palette"]) + list(foundation["palette_extra"])) & {"sea", "fresh water"})


def _bag_entries(pool: dict) -> list[str]:
    out = [e["word"] if "word" in e else e["name"] for L in (pool.get("languages") or {}).values()
           for k in ("person", "god", "sites", "site") for e in L.get(k, [])]
    # build item 22n: the cosmos's bag words (referent persons, the old tongue's plane and ruin words)
    return out + [e["word"] for v in (pool.get("cosmos") or {}).values() for e in v if e.get("word")]


def _all_names(pool: dict) -> set:
    out = {e["name"].lower() for L in (pool.get("languages") or {}).values() for v in L.values() for e in v}
    out |= {e["name"].lower() for v in (pool.get("calendar") or {}).values() for e in v}
    return out | {e["name"].lower() for v in (pool.get("cosmos") or {}).values() for e in v}


def fill_pool(pool: dict, naming: dict, master: str, dials: dict, foundation: dict, phase: str, attempt: int = 1,
              taken_persons=(), secret: dict | None = None, registered: set | None = None, bag_names: bool = True) -> bool:
    """Draw every public stock that is empty or runs low (docs/p1-build-11.md, section 11). Per living language:
    persons and gods from the bag; places, regions, inns, buildings, ships (where the palette holds water) and god
    epithets from the patterns. For the old tongue: sites. For the calendar: a name per month root in the rolled
    pattern, the `High` / `Last` names, a name per day root. `bag_names=False` leaves the bag stocks out (the
    many-seeds tests of the compounds). True when something was drawn."""
    import registry
    rules = draw_rules()
    doc = dt.load("naming.yaml")
    patterns = {p["id"]: p for rows in doc["patterns"].values() for p in rows}
    living = living_languages(naming)
    sizes = stock_sizes(dials["scale"], len(living))
    registered = registry.registered_elsewhere("") if registered is None else registered
    ok = name_checker(registered)
    langs = pool.setdefault("languages", {})
    for lid in naming["languages"]:
        langs.setdefault(lid, {"person": [], "god": []})
    seen = _all_names(pool) | (_all_names(secret) if secret else set())
    stamp = lambda fresh: [dict(e, used_by=None, drawn=phase) for e in fresh]
    changed = False

    # the calendar first (build item 18a's suite found it): its names follow from the roots alone, so the stocks drawn
    # after it avoid them; a building "Last Well" once met the special month "Last Well" in one birth
    if not pool.get("calendar"):
        cal = naming["calendar"]
        month, day = _suffix(patterns[cal["month_pattern"]]), _suffix(patterns["pattern_day"])
        rng = dd.derive(master, phase, "names", "calendar.special", attempt)
        special = rng.sample(cal["month_roots"], min(int(rules["calendar"]["special_months"]), len(cal["month_roots"])))
        words = [o[0].strip() for o in _options(patterns["pattern_month_high_last"]["parts"][0], {}, {})]
        pool["calendar"] = {
            "months": stamp({"name": (r + month).capitalize(), "head": r} for r in cal["month_roots"]),
            "special": stamp({"name": f"{words[i % len(words)]} {r.capitalize()}", "head": r} for i, r in enumerate(special)),
            "days": stamp({"name": (r + day).capitalize(), "head": r} for r in cal["day_roots"])}
        changed = True
        seen |= {e["name"].lower() for v in pool["calendar"].values() for e in v}

    if bag_names:
        taken = list(taken_persons) + _bag_entries(pool) + (_bag_entries(secret) if secret else [])
        for lid in living:
            for kind in ("person", "god"):
                entries = langs[lid][kind]
                n = _want(entries, sizes[kind])
                if n > 0:
                    rng = dd.derive(master, phase, "names", f"{lid}.{kind}.{len(entries)}", attempt)
                    fresh = draw_names(rng, naming["languages"][lid], n, taken, kind)
                    entries += stamp({"name": x} for x in fresh)
                    taken += fresh
                    seen |= {x.lower() for x in fresh}
                    changed = changed or bool(fresh)
        for lid, L in naming["languages"].items():
            if L.get("owner") != "old":
                continue
            entries = langs[lid].setdefault("sites", [])
            n = _want(entries, sizes["sites"])
            if n > 0:
                rng = dd.derive(master, phase, "names", f"{lid}.sites.{len(entries)}", attempt)
                fresh = _site_names(rng, L, n, taken, seen, ok)
                entries += stamp(fresh)
                taken += [e["word"] for e in fresh]
                changed = changed or bool(fresh)

    whole = lexicon_roots()
    by_root = {r["root"]: r for r in whole}
    water = has_water(foundation)
    for lid in living:
        L = naming["languages"][lid]
        env = {"roots": [by_root[r] for r in L["roots"]], "tails": L["settlement_tails"], "whole": whole,
               "kinds": list(foundation["palette"]) + list(foundation["palette_extra"])}
        for key, pids, _ in STOCKS:
            if key == "ships" and not water:
                continue
            entries = langs[lid].setdefault(key, [])
            n = _want(entries, sizes[key])
            if n <= 0:
                continue
            cap = int(rules["head_uses_max"]) + (1 if entries else 0)       # a top-up may lean on a head once more
            uses = Counter(e.get("head") for e in entries if e.get("head"))
            rng = dd.derive(master, phase, "names", f"{lid}.{key}.{len(entries)}", attempt)
            fresh = _draw_stock(rng, [patterns[p] for p in pids], env, n, seen, ok, cap, uses)
            entries += stamp(fresh)
            changed = changed or bool(fresh)

    return changed


def _site_names(rng, lang: dict, n: int, taken: list[str], seen: set, ok) -> list[dict]:
    """The old tongue's site names (decision 30): a word of its bag, alone or with a site word (plural allowed)."""
    patterns = {p["id"]: p for p in dt.load("naming.yaml")["patterns"]["old_tongue"]}
    tails = [o[0] for o in _options(patterns["pattern_old_tongue_site"]["parts"][-1], {}, {})]
    out = []
    for i, word in enumerate(draw_names(rng, lang, n, taken, "person", near=1)):
        name = word if i % 2 == 0 else f"{word} {rng.choice(tails)}"
        if name.lower() in seen or not ok(name):
            continue
        seen.add(name.lower())
        out.append({"name": name, "word": word, "pattern": "pattern_old_tongue_word" if i % 2 == 0 else "pattern_old_tongue_site"})
    return out


def fill_secret(secret: dict, naming: dict, master: str, dials: dict, phase: str, attempt: int, pool: dict,
                registered: set | None = None) -> bool:
    """The secret stock (decision 41): per living language persons, gods and places, for the old tongue sites; drawn
    under its own rng label from the same bags and roots, disjoint from the public stocks."""
    import registry
    registered = registry.registered_elsewhere("") if registered is None else registered
    ok = name_checker(registered)
    doc = dt.load("naming.yaml")
    patterns = {p["id"]: p for rows in doc["patterns"].values() for p in rows}
    living = living_languages(naming)
    sizes = dict(SECRET_SIZES, person=stock_sizes(dials["scale"], len(living))["secret_person"])
    langs = secret.setdefault("languages", {})
    taken = _bag_entries(pool) + _bag_entries(secret)
    seen = _all_names(pool) | _all_names(secret)
    whole = lexicon_roots()
    by_root = {r["root"]: r for r in whole}
    stamp = lambda fresh: [dict(e, used_by=None, drawn=phase) for e in fresh]
    changed = False
    for lid, L in naming["languages"].items():
        mine = langs.setdefault(lid, {})
        for kind in SECRET_KINDS:
            if (kind == "site") != (L.get("owner") == "old"):
                continue
            entries = mine.setdefault(kind, [])
            n = _want(entries, sizes[kind])
            if n <= 0:
                continue
            rng = dd.derive(master, phase, "names-secret", f"{lid}.{kind}.{len(entries)}", attempt)
            if kind in ("person", "god"):
                fresh = [{"name": x} for x in draw_names(rng, L, n, taken, kind)]
                taken += [e["name"] for e in fresh]
                seen |= {e["name"].lower() for e in fresh}
            elif kind == "site":
                fresh = _site_names(rng, L, n, taken, seen, ok)
                taken += [e["word"] for e in fresh]
            else:
                env = {"roots": [by_root[r] for r in L["roots"]], "tails": L["settlement_tails"], "whole": whole}
                fresh = _draw_stock(rng, [patterns[p] for p in STOCKS[0][1]], env, n, seen, ok, int(draw_rules()["head_uses_max"]))
            entries += stamp(fresh)
            changed = changed or bool(fresh)
    return changed


# ── build item 22n: the cosmos's names, drawn after every other stock (public and secret) ───────────────────

COSMOS = "cosmos"
# stock → the patterns (naming.yaml#patterns) its names are drawn with; `referent_persons` are bag names of the common
# tongue (a person an age or an event is named for), `ruin_words` and the planes' old pattern words of the old tongue
COSMOS_STOCKS = {"planes": ("pattern_plane_word", "pattern_plane_old"), "moons": ("pattern_moon_word", "pattern_moon_fresh"),
                 "folk_festivals": ("pattern_festival_folk",), "things": ("pattern_age_thing",),
                 "rulers": ("pattern_age_rulers",), "ruin_words": ("pattern_age_ruin",),
                 "referent_places": ("pattern_place_settlement", "pattern_place_natural"), "referent_persons": ()}
BAG_STOCKS = ("ruin_words", "referent_persons")          # their entries are bag words (`word`)


def cosmos_language(naming: dict) -> str | None:
    """The language the cosmos's names are drawn in: the common tongue, else the other side's, else the people's."""
    langs = naming.get("languages") or {}
    return next((lid for lid in ("common", "other_side", "people") if lid in langs), None)


def gods_language(naming: dict) -> str | None:
    """The gods' language (the 22b ruling 1; design_cosmos.god_language): the common tongue, else the people's, else
    the first living language."""
    langs = naming.get("languages") or {}
    for lid in ("common", "people"):
        if lid in langs:
            return lid
    living = [lid for lid, L in langs.items() if L.get("owner") != "old"]
    return living[0] if living else None


def old_language(naming: dict) -> str | None:
    return next((lid for lid, L in (naming.get("languages") or {}).items() if L.get("owner") == "old"), None)


def cosmos_sizes(scale: str) -> dict:
    """The cosmos stocks (docs/p2-build-22.md part 22n): the planes the scale can touch (the band's top, the magic
    dial's +1, the moon's seat, two spare), two moons, the folk festivals (two and the unnamed god's), the ages' parts,
    one referent of each kind per dated and deep-past event and one more for an age."""
    sc = dt.scale_row(scale)
    hist = sc["history"]
    events = dt.band(hist["dated_events"])[1] + dt.band(hist["deep_past_events"])[1] + 1
    return {"planes": dt.band(sc["planes_touched"])[1] + 4, "moons": 2, "folk_festivals": 3, "things": 2, "rulers": 2,
            "ruin_words": 2, "referent_places": events, "referent_persons": events}


def _cosmos_names(pool: dict | None) -> set:
    out: set = set()
    for key, entries in ((pool or {}).get(COSMOS) or {}).items():
        for e in entries:
            out.add(e["name"].lower())
            if e.get("word"):
                out.add(e["word"].lower())
    return out


def _one_bag(rng, lang: dict, taken: list[str], seen: set, ok) -> str | None:
    """The next bag word of a language that no name of the campaign holds (near-typo 1, as the old tongue's sites)."""
    for _ in range(40):
        got = draw_names(rng, lang, 1, taken, "person", near=1)
        if not got:
            return None
        w = got[0]
        taken.append(w)
        if w.lower() not in seen and ok(w):
            return w
    return None


def _cosmos_draw(rng, key: str, n: int, envs: dict, langs: dict, taken: list[str], seen: set, ok, cap: int) -> list[dict]:
    """n names of one cosmos stock. With two patterns one is rolled per name (a d2); a bag pattern takes a bag word."""
    pats = {p["id"]: p for rows in dt.load("naming.yaml")["patterns"].values() for p in rows}
    max_letters = int(draw_rules()["compound_max_letters"])
    pids = COSMOS_STOCKS[key]
    uses: Counter = Counter()
    streams = {pid: _names(pats[pid], envs["common"], rng, max_letters) for pid in pids
               if not any(p.get("bag_word") for p in pats[pid]["parts"])}
    out: list[dict] = []
    for _ in range(n):
        order = list(pids) if pids else [None]
        if len(order) > 1:
            first = order.pop(rng.randint(1, len(order)) - 1)
            order.insert(0, first)
        for pid in order:
            if pid is None:                                       # a referent person: a common-tongue bag name
                w = _one_bag(rng, langs["common"], taken, seen, ok)
                entry = {"name": w, "word": w, "pattern": "bag"} if w else None
            elif pid not in streams:                              # a word of the old tongue's bag
                # (a ruin word is the word alone: the roller composes the age and the fall from it)
                w = _one_bag(rng, langs["old"], taken, seen, ok) if langs.get("old") else None
                entry = {"name": w, "word": w, "pattern": pid} if w else None
            else:
                entry = None
                for name, head in streams[pid]:
                    if name.lower() in seen or (head and uses[head] >= cap) or not ok(name):
                        continue
                    if head:
                        uses[head] += 1
                    entry = {"name": name, "head": head, "pattern": pid}
                    break
            if entry:
                seen.add(entry["name"].lower())
                if entry.get("word"):
                    seen.add(entry["word"].lower())
                out.append(entry)
                break
    return out


def _god_festivals(naming: dict, pool: dict, master: str, phase: str, attempt: int, seen: set, ok) -> list[dict]:
    """A festival name for each god name of the gods' language not yet given one: `<god>'s <Feast | Night | Day |
    Vigil>`, the word rolled per name."""
    lid = gods_language(naming)
    have = {e["god"] for e in (pool.get(COSMOS) or {}).get("god_festivals") or []}
    words = list(dt.load("naming.yaml")["words"]["festival_words"])
    out = []
    for g in ((pool.get("languages") or {}).get(lid) or {}).get("god") or []:
        if g["name"] in have:
            continue
        rng = dd.derive(master, phase, "names", f"cosmos.god_festival.{g['name']}", attempt)
        order = list(words)
        rng.shuffle(order)
        for w in order:
            name = f"{g['name']}'s {w}"
            if name.lower() not in seen and ok(name):
                seen.add(name.lower())
                out.append({"name": name, "god": g["name"], "festival_word": w, "pattern": "pattern_festival_god"})
                break
    return out


def fill_cosmos(pool: dict, naming: dict, master: str, dials: dict, foundation: dict, phase: str, attempt: int = 1,
                secret: dict | None = None, registered: set | None = None) -> bool:
    """The cosmos's stocks (build item 22n), drawn after every public and secret stock so no earlier name of a seed
    moves: planes, moons, folk festivals, the ages' things, rulers and ruin words, the referents (common-tongue persons
    and places an age or an event is named for), a festival per god name; in the secret stock, the planes a secret
    plane takes (the threat's own home). A legacy pool has none. True when something was drawn."""
    import registry
    lid, old = cosmos_language(naming), old_language(naming)
    if not lid:
        return False
    registered = registry.registered_elsewhere("") if registered is None else registered
    ok = name_checker(registered)
    L = naming["languages"][lid]
    whole = lexicon_roots()
    by_root = {r["root"]: r for r in whole}
    envs = {"common": {"roots": [by_root[r] for r in L["roots"]], "tails": L["settlement_tails"], "whole": whole,
                       "kinds": list(foundation["palette"]) + list(foundation["palette_extra"])}}
    langs = {"common": L, "old": naming["languages"].get(old) if old else None}
    seen = _all_names(pool) | (_all_names(secret) if secret else set())
    taken = _bag_entries(pool) + (_bag_entries(secret) if secret else [])
    cap = int(draw_rules()["head_uses_max"])
    stamp = lambda fresh: [dict(e, used_by=None, drawn=phase) for e in fresh]
    sizes = cosmos_sizes(dials["scale"])
    changed = False
    cos = pool.setdefault(COSMOS, {})
    for key in COSMOS_STOCKS:
        entries = cos.setdefault(key, [])
        n = _want(entries, sizes[key])
        if n > 0:
            rng = dd.derive(master, phase, "names", f"cosmos.{key}.{len(entries)}", attempt)
            fresh = _cosmos_draw(rng, key, n, envs, langs, taken, seen, ok, cap)
            entries += stamp(fresh)
            changed = changed or bool(fresh)
    fresh = _god_festivals(naming, pool, master, phase, attempt, seen, ok)
    cos.setdefault("god_festivals", []).extend(stamp(fresh))
    changed = changed or bool(fresh)
    if secret is not None:
        mine = secret.setdefault(COSMOS, {}).setdefault("planes", [])
        n = _want(mine, 1)
        if n > 0:
            rng = dd.derive(master, phase, "names-secret", f"cosmos.planes.{len(mine)}", attempt)
            fresh = _cosmos_draw(rng, "planes", n, envs, langs, taken, seen, ok, cap)
            mine += stamp(fresh)
            changed = changed or bool(fresh)
    return changed


def cosmos_take(pool: dict | None, key: str, eid: str, where=None) -> dict | None:
    """The next unused entry of a cosmos stock (that `where` accepts), reserved under `eid`."""
    for e in ((pool or {}).get(COSMOS) or {}).get(key) or []:
        if not e.get("used_by") and (where is None or where(e)):
            e["used_by"] = eid
            return e
    return None


def slot_language(slot: str, naming: dict) -> str:
    """Which language names a signature (decision 43). The people: the people's. The institution: its own language
    when it has one, else the common tongue, else the other side's. The phenomenon: the common tongue, else the people's."""
    langs = naming["languages"]
    if slot == "people":
        return "people"
    if slot == "institution":
        return next(l for l in ("institution", "common", "other_side") if l in langs)
    return "common" if "common" in langs else "people"


def draw_candidates(master: str, phase: str, slot: str, attempt: int, naming: dict, identity: dict, foundation: dict,
                    pool: dict, barred=(), registered: set | None = None) -> list[dict]:
    """The candidates of one signature slot (decision 38): they differ in root and, where the slot has several
    patterns, the patterns take turns. The institution's use the rolled form's name words (`Fleet` only where the
    palette holds water); the House form has its one pattern, with family names of the language's bag."""
    rules = draw_rules()
    n = int(rules["candidates"])
    pats = dt.load("naming.yaml")["patterns"]
    lid = slot_language(slot, naming)
    L = naming["languages"][lid]
    whole = lexicon_roots()
    by_root = {r["root"]: r for r in whole}
    env = {"roots": [by_root[r] for r in L["roots"]], "tails": L["settlement_tails"], "whole": whole}
    rng = dd.derive(master, phase, "names", f"candidates.{slot}", attempt)
    if slot == "institution":
        form = dt.row("signatures.yaml#institution_form", identity["institution"]["form"])
        kinds = set(foundation["palette"]) | set(foundation["palette_extra"])
        needs = form.get("name_word_requires") or {}
        env["form_words"] = [w for w in form["name_words"] if w not in needs or kinds & set(needs[w].get("any_of") or [])]
        own = [p for p in pats["institution"] if p.get("only_form") == form["id"]]
        patterns = own or [p for p in pats["institution"] if not p.get("only_form")]
        env["places"] = [(e["name"], e.get("head")) for e in (pool.get("languages") or {}).get(lid, {}).get("places", [])]
        if own:
            taken = _bag_entries(pool) + [str(b).split()[-1] for b in barred]
            env["bag_words"] = draw_names(rng, L, n, taken)
    else:
        patterns = list(pats[slot])
    patterns = list(patterns)
    rng.shuffle(patterns)
    ok = name_checker(registered)
    seen = {str(b).lower() for b in barred} | {c["name"].lower() for s in (naming.get("candidates") or {}).values() for c in s.get("names", [])}
    out = _draw_stock(rng, patterns, env, n, seen, ok, 1, distinct_roots=True)
    if len(out) < n:          # too few roots for a root each: the rest may share one
        out += _draw_stock(rng, patterns, env, n - len(out), seen, ok, n)
    return [{"name": e["name"], "pattern": e["pattern"], "root": e["head"]} for e in out]


# ── the pool on disk ─────────────────────────────────────────────────────────────────────────────────────────

def load_secret(campaign: str) -> dict | None:
    return read_json(secret_path(campaign))


def secret_given_names(campaign: str) -> set:
    """The secret stock's person and god names, lower-cased (the door: a public entity takes none of them)."""
    secret = load_secret(campaign) or {}
    return {e["name"].lower() for L in (secret.get("languages") or {}).values() for k in ("person", "god") for e in L.get(k, [])}


def mark_secret_used(campaign: str, name: str, eid: str) -> None:
    secret = load_secret(campaign)
    if not secret:
        return
    for L in secret["languages"].values():
        for k in ("person", "god"):
            for e in L.get(k, []):
                if e["name"] == name and not e.get("used_by"):
                    e["used_by"], e["used_at"] = eid, now_iso()
                    stamp_meta(secret, campaign, "registry.py merge (secret stock)")
                    write_json_atomic(secret_path(campaign), secret)
                    return


def write_rolled(campaign: str, naming: dict, phase: str, attempt: int) -> dict:
    """P1's preroll: `design/naming.json` (public, stamped, written by the script alone), the public pool, the
    secret stock, then the signature candidates into `naming.json#candidates`."""
    import registry
    m = dm.load(campaign)
    data = {"_meta": {"schema_version": 1, "campaign": campaign}, "stamped": True, "rolled": True,
            "languages": naming["languages"], "calendar": naming["calendar"], "candidates": {}, "assignments": {},
            "banned": sorted(registry.registered_elsewhere(campaign))}
    stamp_meta(data, campaign, f"designer.py preroll --phase {phase} (names)")
    write_json_atomic(naming_path(campaign), data)
    pool = ensure_pool(campaign, phase, attempt, fresh=True)
    for slot in SLOTS:
        names = draw_candidates(m["seed"]["master"], phase, slot, 1, data, m["identity"], m["foundation"], pool)
        data["candidates"][slot] = {"language": slot_language(slot, data), "attempt": 1, "names": names, "discarded": []}
    write_json_atomic(naming_path(campaign), data)
    return data


def reroll(campaign: str, slot: str) -> list[dict]:
    """The owner's reroll (decision 40): four fresh candidates for one signature slot, the next attempt of that draw;
    the old four stay in the record as discarded."""
    data = read_json(naming_path(campaign)) or {}
    if not data.get("rolled"):
        raise SystemExit("design_names: this campaign's names were not rolled by script (a legacy birth); nothing to reroll")
    m = dm.load(campaign)
    cur = data["candidates"][slot]
    barred = [c["name"] for c in cur["names"]] + [c["name"] for old in cur["discarded"] for c in old]
    attempt = int(cur["attempt"]) + 1
    names = draw_candidates(m["seed"]["master"], "P1", slot, attempt, data, m["identity"], m["foundation"],
                            load_pool(campaign) or {}, barred=barred)
    cur["discarded"].append(cur["names"])
    cur.update({"attempt": attempt, "names": names})
    stamp_meta(data, campaign, f"design_names.py reroll --slot {slot}")
    write_json_atomic(naming_path(campaign), data)
    import design_door
    if dm.load(campaign).get(design_door.SEAL):
        design_door.seal(campaign)              # the owner's reroll is the one sanctioned change of the candidates
    return names


def _ensure_legacy_pool(campaign: str, langs: dict, phase: str, attempt: int) -> dict:
    """A birth whose languages the writer wrote (before build item 11b): persons and gods per language, sixteen
    place candidates compounded from its roots."""
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


def ensure_pool(campaign: str, phase: str, attempt: int = 1, fresh: bool = False) -> dict | None:
    """Draw the pool once the languages exist, and top up a stock that runs low. A campaign whose names the script
    rolled (`naming.json#rolled`) gets every stock and the secret stock; `fresh` (P1's preroll) starts both anew. A
    legacy birth keeps the pool it has and the way it was drawn."""
    naming = read_json(naming_path(campaign)) or {}
    langs = naming.get("languages") or {}
    if not langs:
        return None
    if not naming.get("rolled"):
        return _ensure_legacy_pool(campaign, langs, phase, attempt)
    m = dm.load(campaign)
    blank = lambda: {"_meta": {"schema_version": 1, "campaign": campaign}, "rolled": True, "languages": {}}
    pool = (None if fresh else load_pool(campaign)) or dict(blank(), calendar={})
    secret = (None if fresh else load_secret(campaign)) or blank()
    persons, _ = campaign_names(campaign)
    master = m["seed"]["master"]
    if fill_pool(pool, naming, master, m["dials"], m["foundation"], phase, attempt, taken_persons=persons, secret=secret) or fresh:
        save_pool(campaign, pool, f"design_names.py pool --phase {phase}")
    if fill_secret(secret, naming, master, m["dials"], phase, attempt, pool) or fresh:
        stamp_meta(secret, campaign, f"design_names.py pool --phase {phase} (secret stock)")
        write_json_atomic(secret_path(campaign), secret)
    # build item 22n: the cosmos's stocks last, so no earlier name of the seed moves
    if fill_cosmos(pool, naming, master, m["dials"], m["foundation"], phase, attempt, secret=secret):
        save_pool(campaign, pool, f"design_names.py pool --phase {phase} (the cosmos)")
        stamp_meta(secret, campaign, f"design_names.py pool --phase {phase} (the cosmos, secret stock)")
        write_json_atomic(secret_path(campaign), secret)
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


def _string_values(node, skip=("id", "type", "file", "secrecy", "origin", "created_phase", "lang", "status")) -> set:
    out: set = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k not in skip:
                out |= _string_values(v, skip)
    elif isinstance(node, list):
        for v in node:
            out |= _string_values(v, skip)
    elif isinstance(node, str) and node.strip():
        out.add(node.strip())
    return out


def reserve_named(pool: dict | None, secret: dict | None, row: dict, eid: str) -> int:
    """Build item 22c: a pooled name that a merged row holds as the whole value of one of its fields (a premise's
    `dm_only.pinned.god`, a name field) is reserved under that row at the merge, at every phase, so no later row takes
    it. A name inside prose is never reserved: a summary that mentions a person to come must not block that person's
    row. Returns the names reserved."""
    values = _string_values(row)
    n = 0
    for stock in (pool, secret):
        lists = [entries for L in ((stock or {}).get("languages") or {}).values() for entries in L.values()]
        lists += list(((stock or {}).get("cosmos") or {}).values())          # build item 22n
        for entries in lists:
            for e in entries:
                if not e.get("used_by") and e.get("name") in values:
                    e["used_by"], e["used_at"] = eid, now_iso()
                    n += 1
    return n


STOCK_WORDS = {"person": "persons", "god": "gods", "places": "places", "regions": "regions", "inns": "inns",
               "buildings": "quarters, markets and buildings", "ships": "ships", "epithets": "god epithets", "sites": "ruin sites"}


def prompt_text(campaign: str, entity_id: str | None) -> str:
    """The prompts' Names paragraph: every stock's unused names, rotated per entity so parallel writers start apart.
    No name of the secret stock is printed: the paragraph gives the command that lists them."""
    pool = load_pool(campaign)
    if not pool:
        return ""
    shift = sum(map(ord, entity_id or "")) if entity_id else 0

    def rotated(entries) -> list[str]:
        unused = [e["name"] for e in entries if not e.get("used_by")]
        k = shift % len(unused) if unused else 0
        return unused[k:] + unused[:k]
    if not pool.get("rolled"):
        lines = ["**Names (rolled, never invented).** Give a new public person or god the next unused given name of their "
                 "language from these lists, in order (a byname from the language's roots may follow it); "
                 "the door refuses a given name that is not on its language's list. A secret entity never takes a name from "
                 "these lists (they are printed where the conductor can read them). A place takes one of its language's "
                 "place candidates, or a compound of the language's roots in the same shape."]
        for lid, L in (pool.get("languages") or {}).items():
            for kind in ("person", "god"):
                if rotated(L.get(kind, [])):
                    lines.append(f"- {lid} {kind}s: " + ", ".join(rotated(L[kind])))
            if pool.get("places", {}).get(lid):
                lines.append(f"- {lid} place candidates: " + ", ".join(pool["places"][lid]))
        return "\n".join(lines)
    naming = read_json(naming_path(campaign)) or {}
    words = dt.load("naming.yaml")["words"]
    by_root = {r["root"]: r for r in lexicon_roots()}
    script = f"py {Path(__file__).resolve().as_posix()} -c {campaign}"
    lines = ["**Names (rolled, never invented).** Every proper noun comes from the stocks below or from the signature "
             "candidates in `design/naming.json#candidates`; you invent none. Give a new public person or god the next unused "
             "given name of their language, in order; the door refuses a given name that is not on its language's list. A "
             "settlement or a natural place, a region, an inn, a quarter or building, a ship and a god's epithet take the "
             "next unused name of their language's stock; a site the ruin left takes one of the old tongue's; months and "
             "days take the calendar's. Two kinds of name you compose from pooled parts, and only these: `<a pooled person "
             "name>'s <a building word or one of the language's natural tails>` (a place called by its owner) and `<a "
             f"building word> of <a pooled god name>` (a temple); the building words: {', '.join(words['building_words'])}. "
             "A secret entity never takes a name from these lists (they are printed where the conductor can read them): "
             f"run `{script} secret --lang <language> --kind person|god|place|site` and take a name from its output."]
    for lid, L in (pool.get("languages") or {}).items():
        label = ((naming.get("languages") or {}).get(lid) or {}).get("label") or lid
        head = lid if label == lid else f"{lid} ({label})"
        for key, word in STOCK_WORDS.items():
            names = rotated(L.get(key, []))
            if names:
                lines.append(f"- {head} {word}: " + ", ".join(names))
        tails = [r for r in ((naming.get("languages") or {}).get(lid) or {}).get("roots") or [] if slot_fits(by_root[r], "tail")]
        if tails:
            lines.append(f"- {head} natural tails: " + ", ".join(tails))
    cal = pool.get("calendar") or {}
    for key, word in (("months", "months"), ("special", "special months and feasts"), ("days", "days")):
        if cal.get(key):
            lines.append(f"- calendar {word}: " + ", ".join(e["name"] for e in cal[key]))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the campaign's rolled names (RC-13; build item 11)")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    p = sub.add_parser("pool")
    p.add_argument("--phase", default="P2")
    p.add_argument("--attempt", type=int, default=1)
    sub.add_parser("show")
    p = sub.add_parser("secret", help="the unused names of the secret stock, for a secret entity (dm-only)")
    p.add_argument("--lang", required=True)
    p.add_argument("--kind", required=True, choices=SECRET_KINDS)
    p = sub.add_parser("reroll", help="the owner's tool: four fresh candidates for one signature slot")
    p.add_argument("--slot", required=True, choices=SLOTS)
    p.add_argument("--onay", action="store_true")
    a = ap.parse_args(argv)
    if a.verb == "secret":
        langs = (load_secret(a.campaign) or {}).get("languages") or {}
        if a.lang not in langs:
            print(f"design_names: no secret stock for the language {a.lang!r} (the languages: {', '.join(langs) or 'none'})", file=sys.stderr)
            return 1
        for e in langs[a.lang].get(a.kind, []):
            if not e.get("used_by"):
                print(e["name"])
        return 0
    if a.verb == "reroll":
        if not (a.campaign.startswith("_test-") or a.onay):
            print("design_names: a reroll is the owner's own choice at the review stop (pass --onay after they asked for it)", file=sys.stderr)
            return 1
        names = reroll(a.campaign, a.slot)
        print(f"design_names: {a.slot} — " + ", ".join(c["name"] for c in names))
        return 0
    if a.verb == "pool":
        pool = ensure_pool(a.campaign, a.phase, a.attempt)
        if pool is None:
            print("design_names: no naming languages yet (P1's preroll writes design/naming.json)", file=sys.stderr)
            return 1
    pool = load_pool(a.campaign) or {}
    for lid, L in (pool.get("languages") or {}).items():
        for kind, entries in L.items():
            unused = sum(1 for e in entries if not e.get("used_by"))
            print(f"design_names: {lid} {STOCK_WORDS.get(kind, kind)} — {len(entries)} drawn, {unused} unused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
