"""
test_name_pools.py — build item 11b (docs/p1-build-11.md, Part 11b, sections 7-13; the owner's decisions 33-45): the
names rolled by script. Over many seeds of every scale, magic, era and tone: the languages and whose they are, the
bags' groups, each language's roots (the count, the half share, the floor of heads and tails, no sharing), the
calendar's own roots, the settlement tails; the candidates and the compound stocks (the head spread, the sizes, the
form words, the filters); on disk: `design/naming.json` written by the preroll, the secret stock and its secrecy, the
owner's reroll, the door's mirror rule, and a legacy birth left as it was.

  py test_name_pools.py --report <dir>     the numbers of the summary and one full public pool per scale
"""

import copy
import itertools
import json
import math
import os
import re
import shutil
import sys
import unittest
import uuid
from collections import Counter

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign
from _floor import SPAN, dial_sets
from test_tuning_birth_1 import fragment, row  # the registry-row and fragment builders, shared

sys.path.insert(0, str(SCRIPTS))
import design_names as dn  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402
import _corpus  # noqa: E402  (build item 18f-1: the shared many-seed corpus)

SEEDS = 2400          # the rolls
POOL_SEEDS = 480      # the candidates and the compound stocks
RULES = dn.draw_rules()
ROOTS = {r["root"]: r for r in dn.lexicon_roots()}
SEA_KINDS = {"land_coast", "land_island", "land_stone_sea"}
LEX = dn.LEX
_BIRTHS: dict = {}


def births(n: int, tag: str = "NAMES") -> list[dict]:
    """n in-memory P1 prerolls, the dials going round every scale, magic, era and tone."""
    # the shared corpus (build item 18f-1); one record per birth, kept here (the pools a test builds stay on it)
    corpus = _corpus.births(n)
    while len(_BIRTHS.setdefault(tag, [])) < len(corpus):
        dials, R = corpus[len(_BIRTHS[tag])]
        _BIRTHS[tag].append({"master": R.master, "dials": dials, "foundation": R.foundation, "identity": R.identity,
                             "naming": R.naming, "public": R.public, "secret": R.secret})
    return _BIRTHS[tag][:len(corpus)]


def kinds_of(b: dict) -> set:
    return set(b["foundation"]["palette"]) | set(b["foundation"]["palette_extra"])


def living(b: dict) -> dict:
    return {lid: L for lid, L in b["naming"]["languages"].items() if L["owner"] != "old"}


def pooled(b: dict, bag_names: bool = False) -> dict:
    """The birth's public pool and candidates, built in memory (no name of another campaign registered)."""
    key = "pool_bag" if bag_names else "pool"
    if key not in b:
        pool: dict = {}
        dn.fill_pool(pool, b["naming"], b["master"], b["dials"], b["foundation"], "P1", registered=set(), bag_names=bag_names)
        naming = dict(b["naming"], candidates={})
        for slot in dn.SLOTS:
            naming["candidates"][slot] = {"names": dn.draw_candidates(b["master"], "P1", slot, 1, naming, b["identity"],
                                                                      b["foundation"], pool, registered=set())}
        b[key] = pool
        b["candidates"] = naming["candidates"]
    return b[key]


class Languages(unittest.TestCase):

    def test_whose_the_languages_are(self):
        ident = lambda breaks=(), sign="isign_seal": {"trope_breaks": [{"id": x} for x in breaks], "institution": {"sign": sign}}
        none, own = "break_no_common_tongue", "isign_own_language"
        self.assertEqual(dn.language_owners("short", ident()), ["people", "common"])
        self.assertEqual(dn.language_owners("short", ident([none])), ["people", "other_side"])
        for scale in ("standard", "epic"):
            self.assertEqual(dn.language_owners(scale, ident()), ["people", "common", "other_side"])
            self.assertEqual(dn.language_owners(scale, ident([none])), ["people", "other_side"], "no third living language")
            self.assertEqual(dn.language_owners(scale, ident(sign=own)), ["people", "common", "institution"])
            self.assertEqual(dn.language_owners(scale, ident([none], own)), ["people", "other_side", "institution"], "both at once")

    def test_the_count_the_groups_and_the_old_tongue_over_many_seeds(self):
        bags = {r["id"]: r for r in dt.rows(dn.FAMILY)}
        seen_owner_sets = Counter()
        for b in births(SEEDS):
            langs = b["naming"]["languages"]
            alive = living(b)
            scale = b["dials"]["scale"]
            self.assertEqual(list(alive), dn.language_owners(scale, b["identity"]))
            self.assertEqual(len(alive), 2 if scale == "short" or list(alive)[1:] == ["other_side"] else 3)
            self.assertEqual(list(langs)[-1], "old", "the old tongue stands beside the living ones in every campaign")
            self.assertEqual(len({L["bag"] for L in langs.values()}), len(langs))
            groups = [L["group"] for L in langs.values()]
            self.assertEqual(len(set(groups)), len(groups), "every language of a campaign from a sound group of its own")
            for L in langs.values():
                self.assertEqual(bags[L["bag"]]["group"], L["group"])
            self.assertEqual((langs["old"]["roots"], langs["old"]["settlement_tails"]), ([], []), "the old tongue has no roots")
            self.assertEqual(langs["old"]["label"], "the old tongue")
            if "common" in langs:
                self.assertEqual(langs["common"]["label"], "the common tongue")
            if "other_side" in langs:
                role = b["identity"]["people"]["role"]
                self.assertEqual(langs["other_side"]["role"], {"a": "b", "b": "a"}.get(role, "b"))
            self.assertFalse(any("label_tr" in L for L in langs.values()))
            seen_owner_sets[tuple(alive)] += 1
        self.assertGreaterEqual(len(seen_owner_sets), 3, seen_owner_sets)

    def test_the_naming_rolls_stand_at_the_end_of_p1(self):
        for b in births(120):
            labels = [r["label"] for r in b["public"]]
            first = min(i for i, l in enumerate(labels) if l.startswith("naming_"))
            self.assertGreater(first, labels.index("mechanic"), "after the mechanic gate")
            self.assertTrue(all(l.startswith("naming_") for l in labels[first:]), "and nothing after them")
            self.assertEqual(labels[first], "naming_family.1")
            self.assertIn("naming_family.old", labels)
            self.assertFalse(any(r["label"].startswith("naming") for r in b["secret"]), "the naming rolls are public")
            fams = [r for r in b["public"] if r["label"].startswith("naming_family.")]
            self.assertEqual(len(fams), len(b["naming"]["languages"]))
            self.assertTrue(all(r["table"] == dn.FAMILY and r["row_id"] for r in fams), "each through the arbiter, as a table draw")


class Roots(unittest.TestCase):

    def test_the_count_the_floor_and_no_sharing(self):
        for b in births(SEEDS):
            scale = b["dials"]["scale"]
            n, floor = RULES["roots_per_language"][scale], RULES["head_floor"][scale]
            self.assertEqual((n, floor), {"short": (10, 5), "standard": (18, 9), "epic": (24, 12)}[scale])
            every: list[str] = []
            for lid, L in living(b).items():
                rows = [ROOTS[r] for r in L["roots"]]
                self.assertEqual(len(rows), n, lid)
                heads = [r for r in rows if dn.slot_fits(r, "head")]
                self.assertGreaterEqual(len(heads), floor, f"{lid}: the head floor")
                self.assertGreaterEqual(sum(1 for r in heads if not dn.is_adjective(r)), 4, f"{lid}: four noun heads")
                self.assertGreaterEqual(sum(1 for r in rows if dn.slot_fits(r, "tail")), 2, f"{lid}: two natural tails")
                every += L["roots"]
            cal = b["naming"]["calendar"]
            self.assertEqual((len(cal["month_roots"]), len(cal["day_roots"])), (14, 9))
            every += cal["month_roots"] + cal["day_roots"]
            self.assertEqual(len(set(every)), len(every), "no root in two languages, or in a language and the calendar")
            self.assertFalse(set(every) & set(dt.load("naming.yaml")["lexicon"]["settlement_tails"]))

    def test_the_half_share(self):
        """At least half of a language's roots carry a called tag whenever the called pool allowed it."""
        short = 0
        total = 0
        for b in births(SEEDS):
            n = RULES["roots_per_language"][b["dials"]["scale"]]
            quota = math.ceil(n / 2)
            barred = dn.land_tags() - dn.palette_tags(kinds_of(b))
            for lid, L in living(b).items():
                total += 1
                calls = dn.called_tags(lid, b["foundation"], b["identity"])
                self.assertEqual(sorted(calls), L["called_tags"])
                for r in L["called"]:
                    self.assertTrue(set(ROOTS[r]["tags"]) & calls, f"{r} was drawn as called and carries no called tag")
                    self.assertFalse(set(ROOTS[r]["tags"]) & barred, r)
                self.assertEqual(len(L["called"]) + L["called_short"], quota)
                short += 1 if L["called_short"] else 0
                if not L["called_short"]:
                    self.assertGreaterEqual(sum(1 for r in L["roots"] if set(ROOTS[r]["tags"]) & calls), quota)
                if lid != "people":
                    self.assertEqual(calls, dn.palette_tags(kinds_of(b)), "every land tag a palette kind calls")
        type(self).short_rate = (short, total)
        self.assertLess(short / total, 0.05, "the called pool is rarely too small")

    def test_what_the_peoples_language_calls(self):
        import design_foundation as fd
        lifelines = fd.rows_by_id("lifeline")
        for b in births(600):
            f = b["foundation"]
            calls = set(b["naming"]["languages"]["people"]["called_tags"])
            family = lifelines[f["lifeline"]["id"]]["family"]
            life_kinds = dn.kinds_at(f, f["lifeline"]["seat"])
            role = b["identity"]["people"]["role"]
            seat = f["layout"]["contests"][0]["seats"].get(role) if role else None
            home = dn.kinds_at(f, seat) or life_kinds
            self.assertEqual(calls, dn.lifeline_tags(family, life_kinds) | dn.palette_tags(home))
            if family == "treaty":
                self.assertEqual(dn.lifeline_tags(family, life_kinds), set(), "the treaty family calls nothing")
            if family == "water":
                self.assertLessEqual(dn.lifeline_tags(family, life_kinds), {"fresh water", "sea"})
        self.assertEqual(dn.palette_tags(["land_thin_place"]), set())
        self.assertEqual(dn.palette_tags(["land_giant_bones"]), {"animal"})
        self.assertEqual(dn.lifeline_tags("water", ["land_coast"]), {"sea"})
        self.assertEqual(dn.lifeline_tags("water", ["land_river"]), {"fresh water"})
        self.assertEqual(dn.lifeline_tags("water", ["land_mountain"]), set())

    def test_a_landlocked_palette_gets_no_sea_root_in_the_called_half(self):
        landlocked = free = free_sea = off = 0
        for b in births(SEEDS):
            barred = dn.land_tags() - dn.palette_tags(kinds_of(b))
            cal = b["naming"]["calendar"]
            halves = [(L["roots"], L["called"]) for L in living(b).values()]
            halves += [(cal["month_roots"], cal["month_called"]), (cal["day_roots"], cal["day_called"])]
            for roots, called in halves:
                rest = [r for r in roots if r not in called]
                free += len(rest)
                off += sum(1 for r in rest if set(ROOTS[r]["tags"]) & barred)
                if not kinds_of(b) & SEA_KINDS:
                    self.assertFalse([r for r in called if "sea" in ROOTS[r]["tags"]], "a sea root in a landlocked world's called half")
                    free_sea += sum(1 for r in rest if "sea" in ROOTS[r]["tags"])
            landlocked += 0 if kinds_of(b) & SEA_KINDS else 1
        self.assertGreater(landlocked, 100)
        type(self).free_half = {"free roots": free, "off the palette": off, "landlocked births": landlocked, "sea roots in their free half": free_sea}

    def test_the_calendars_roots(self):
        tags = set(RULES["calendar"]["tags"])
        self.assertEqual(tags, {"crop", "weather and season", "cold", "animal", "forest", "sky", "fresh water"})
        patterns = Counter()
        suffix = {"pattern_month_month": "month", "pattern_month_moon": "moon", "pattern_month_fall": "fall"}
        for b in births(SEEDS):
            cal = b["naming"]["calendar"]
            patterns[cal["month_pattern"]] += 1
            calls = dn.palette_tags(kinds_of(b))
            for key, tail in (("month", suffix[cal["month_pattern"]]), ("day", "day")):
                for r in cal[f"{key}_roots"]:
                    self.assertTrue(set(ROOTS[r]["tags"]) & tags, r)
                    self.assertFalse(dn.is_adjective(ROOTS[r]), r)
                    self.assertTrue(dn.slot_fits(ROOTS[r], "head"), r)
                    self.assertTrue(dn.joins(r, tail), f"{r}{tail}")
                for r in cal[f"{key}_called"]:
                    self.assertTrue(set(ROOTS[r]["tags"]) & calls, r)
        self.assertEqual(set(patterns), set(suffix), "one of the three rollable month patterns, each of them drawn")

    def test_the_settlement_tails(self):
        all_tails = set(dt.load("naming.yaml")["lexicon"]["settlement_tails"])
        for b in births(SEEDS):
            sets = [L["settlement_tails"] for L in living(b).values()]
            for tails in sets:
                self.assertEqual(len(tails), 7)
                self.assertEqual(len(set(tails)), 7)
                self.assertLessEqual(set(tails), all_tails)
            for a, c in itertools.combinations(sets, 2):
                self.assertLessEqual(len(set(a) & set(c)), 2, "two languages of one campaign share at most two tails")

    def test_the_roots_go_to_used_json_and_wait(self):
        b = births(40)[7]
        recs = {r["label"]: r for r in b["public"] if r["label"].startswith(("naming_roots.", "naming_calendar."))}
        for lid, L in living(b).items():
            self.assertEqual(recs[f"naming_roots.{lid}"]["used_keys"], {LEX: L["roots"]})
            self.assertEqual(recs[f"naming_roots.{lid}"]["items"], L["roots"])
        self.assertEqual(recs["naming_calendar.months"]["used_keys"], {LEX: b["naming"]["calendar"]["month_roots"]})
        self.assertNotIn("used_keys", recs["naming_calendar.pattern"])
        # a root another campaign drew waits while a fresh one fits the slot
        import random
        used = {r for r in ROOTS if r not in ("oak", "elm", "yew", "ford", "mere")}
        got, _, _, spent = dn._pick_roots(random.Random(1), ["noun", "tail"], 0, lambda r: False, set(), used)
        self.assertTrue(set(got) <= {"oak", "elm", "yew", "ford", "mere"} and spent == 0, got)
        got, _, _, spent = dn._pick_roots(random.Random(1), ["noun"] * 4, 0, lambda r: False, set(), set(ROOTS))
        self.assertEqual((len(got), spent), (4, 4), "the lexicon turned over: the draw goes on")


class Pools(unittest.TestCase):
    """The candidates and the compound stocks over many seeds (the bag stocks are drawn in FullPools)."""

    @classmethod
    def setUpClass(cls):
        cls.births = births(POOL_SEEDS)
        for b in cls.births:
            pooled(b)

    def test_four_candidates_per_slot_differing_in_root(self):
        forms = {r["id"]: r for r in dt.rows("signatures.yaml#institution_form")}
        water = set(forms["form_travelling"]["name_word_requires"]["Fleet"]["any_of"])
        house = fleet = 0
        for b in self.births:
            cands = b["candidates"]
            every = [c["name"] for s in cands.values() for c in s["names"]]
            self.assertEqual(len(set(every)), 12, every)
            for slot in ("people", "phenomenon"):
                rows = cands[slot]["names"]
                self.assertEqual(len({c["root"] for c in rows}), 4, f"{slot}: {rows}")
                self.assertFalse([c for c in rows if dn.is_adjective(ROOTS[c["root"]])], "no adjective root in these slots")
                self.assertGreaterEqual(len({c["pattern"] for c in rows}), 2, "the patterns take turns")
                lang = b["naming"]["languages"][dn.slot_language(slot, b["naming"])]
                self.assertLessEqual({c["root"] for c in rows}, set(lang["roots"]))
            self.assertTrue(all(c["name"].startswith("the ") for c in cands["phenomenon"]["names"]))
            form = forms[b["identity"]["institution"]["form"]]
            rows = cands["institution"]["names"]
            for c in rows:
                words = [w for w in form["name_words"] if re.search(rf"\b{w}\b", c["name"])]
                self.assertTrue(words, f"{c['name']}: no name word of {form['id']}")
                if "Fleet" in c["name"].split():
                    fleet += 1
                    self.assertTrue(kinds_of(b) & water, "Fleet only where the palette holds water")
                if c["pattern"] == "pattern_institution_form_of_root":
                    self.assertFalse(dn.is_adjective(ROOTS[c["root"]]), c["name"])
            if form["id"] == "form_house":
                house += 1
                self.assertTrue(all(c["pattern"] == "pattern_institution_house" and c["name"].startswith("House ") for c in rows))
            else:
                self.assertNotIn("pattern_institution_house", {c["pattern"] for c in rows})
                roots = [c["root"] for c in rows if c["root"]]
                self.assertEqual(len(set(roots)), len(roots), rows)
        self.assertGreater(house, 0)

    def test_which_language_names_which_signature(self):
        langs = lambda *ids: {"languages": {i: {} for i in ids}}
        self.assertEqual(dn.slot_language("people", langs("people", "common", "old")), "people")
        self.assertEqual(dn.slot_language("institution", langs("people", "common", "other_side", "old")), "common")
        self.assertEqual(dn.slot_language("institution", langs("people", "common", "institution", "old")), "institution")
        self.assertEqual(dn.slot_language("institution", langs("people", "other_side", "old")), "other_side")
        self.assertEqual(dn.slot_language("phenomenon", langs("people", "common", "old")), "common")
        self.assertEqual(dn.slot_language("phenomenon", langs("people", "other_side", "old")), "people")

    def test_the_stocks_spread_their_heads_and_meet_the_scales_need(self):
        cap = RULES["head_uses_max"]
        self.assertEqual(cap, 3)
        smallest: dict = {}
        for b in self.births:
            pool = pooled(b)
            scale = b["dials"]["scale"]
            need = dn.scale_needs(dt.scale_row(scale))
            total = Counter()
            for lid in living(b):
                stocks = pool["languages"][lid]
                self.assertEqual(bool(stocks.get("ships")), dn.has_water(b["foundation"]), "ships where the palette holds water")
                for key, entries in stocks.items():
                    total[key] += len(entries)
                    heads = Counter(e["head"] for e in entries if e.get("head"))
                    self.assertLessEqual(max(heads.values(), default=0), cap, f"{lid} {key}: one head in more than three names")
                    self.assertTrue(all(e["used_by"] is None and e["drawn"] == "P1" for e in entries))
                for e in stocks["places"]:
                    word = e["name"]
                    self.assertTrue(word.isalpha() and len(word) <= RULES["compound_max_letters"], word)
                    self.assertIsNone(re.search(r"(.)\1", word.lower()[len(e["head"]) - 1:len(e["head"]) + 1]), f"{word}: a doubled letter at the join")
                for e in stocks["epithets"]:
                    if e["pattern"] != "pattern_epithet_one":
                        self.assertFalse(dn.is_adjective(ROOTS[e["head"]]), e["name"])
            self.assertEqual(pool["languages"]["old"], {"person": [], "god": []}, "no compound stock for the old tongue")
            for key, by in (("places", "settlements"), ("regions", "regions"), ("inns", "settlements"), ("buildings", "settlements")):
                self.assertGreaterEqual(total[key], 3 * need[by], f"{scale} {key}: under three times the scale's need")
                smallest[(scale, key)] = min(smallest.get((scale, key), 9999), total[key])
            smallest[(scale, "epithets")] = min(smallest.get((scale, "epithets"), 9999), total["epithets"])
            names = [e["name"].lower() for L in pool["languages"].values() for v in L.values() for e in v]
            names += [e["name"].lower() for v in pool["calendar"].values() for e in v]
            self.assertEqual(len(set(names)), len(names), "no name twice in a campaign's stocks")
        type(self).smallest = smallest

    def test_the_calendars_stock(self):
        for b in self.births[:200]:
            cal, stock = b["naming"]["calendar"], pooled(b)["calendar"]
            tail = {"pattern_month_month": "month", "pattern_month_moon": "moon", "pattern_month_fall": "fall"}[cal["month_pattern"]]
            self.assertEqual([e["name"] for e in stock["months"]], [(r + tail).capitalize() for r in cal["month_roots"]])
            self.assertEqual([e["name"] for e in stock["days"]], [(r + "day").capitalize() for r in cal["day_roots"]])
            self.assertEqual(len(stock["special"]), 4)
            for e in stock["special"]:
                self.assertRegex(e["name"], r"^(High|Last) [A-Z][a-z]+$")
                self.assertIn(e["head"], cal["month_roots"])

    def test_no_pooled_name_is_on_a_blacklist(self):
        import registry
        bl = registry.naming_blacklist()
        real = {str(x).lower() for x in bl["real_places"]}
        exact = {str(x).lower() for k in ("exact", "mythology", "llm_favourites", "turkish_as_name") for x in (bl.get(k) or [])}
        stems = [s.lower() for s in bl["owner_banned"]["stems"] + bl["substrings"]]
        for b in self.births:
            pool = pooled(b)
            names = [e["name"] for L in pool["languages"].values() for v in L.values() for e in v]
            names += [e["name"] for v in pool["calendar"].values() for e in v] + [c["name"] for s in b["candidates"].values() for c in s["names"]]
            for name in names:
                low = name.lower()
                bare = low[4:] if low.startswith("the ") else low
                self.assertFalse({low, bare} & real, name)
                self.assertFalse({low, low.split()[0]} & exact, name)       # as the door reads a name
                self.assertFalse([s for s in stems if s in low], name)
                self.assertIsNone(re.search("[çğıöşüÇĞİÖŞÜ]", name))
        ok = dn.name_checker({"thornwick", "the grey march"})
        self.assertFalse(ok("Thornwick"), "a name another campaign registered")
        self.assertFalse(ok("the Grey March"))
        self.assertFalse(ok("Oxford"), "a famous real place")
        self.assertFalse(ok("the Winterfell"))
        self.assertTrue(ok("Thornbury"), "an obscure real village passes (decision 42)")

    def test_the_join_rules_of_a_compound(self):
        self.assertFalse(dn.joins("hoof", "folk"), "no doubled letter at a join (Hooffolk)")
        self.assertFalse(dn.joins("moon", "moon"), "head and tail differ")
        self.assertFalse(dn.joins("heatherstone", "wick"), "twelve letters at most")
        self.assertTrue(dn.joins("thorn", "wick"))


class AuditCorrections(unittest.TestCase):
    """The seven corrections of the audit of build 11b (docs/p1-build-11.md, the end): each a rule in data."""

    @classmethod
    def setUpClass(cls):
        cls.births = births(POOL_SEEDS)
        for b in cls.births:
            pooled(b)
        cls.doc = dt.load("naming.yaml")
        cls.text = (dt.tables_dir() / "naming.yaml").read_text(encoding="utf-8")

    def stock(self, key):
        for b in self.births:
            for lid in living(b):
                for e in pooled(b)["languages"][lid].get(key, []):
                    yield b, e

    def test_1_eight_roots_are_heads_only(self):
        eight = "song root leaf wing brand smith wright bough".split()
        self.assertEqual({ROOTS[r]["pos"] for r in eight}, {"head"})
        for _, e in self.stock("places"):
            if e["pattern"] == "pattern_place_natural":
                self.assertFalse([x for x in eight if e["name"].lower().endswith(x) and e["head"] != x], e["name"])

    def test_2_a_region_word_follows_the_palette(self):
        rows = {w["word"]: set((w.get("requires") or {}).get("any_of") or []) for w in self.doc["words"]["region_words"]}
        sea, palette = {"land_coast", "land_island", "land_stone_sea"}, {r["id"] for r in dt.rows("foundation.yaml#palette")}
        self.assertEqual(rows, {
            "March": set(), "Reach": set(), "Vale": set(), "Coast": sea, "Isles": sea, "Fens": {"land_marsh", "land_river", "land_lake"},
            "Deeps": {"land_underground"} | sea, "Fells": {"land_mountain", "land_highland"}, "Heights": {"land_mountain", "land_highland"},
            "Wastes": {"land_desert", "land_glass_desert", "land_cold", "land_volcanic"},
            "Moors": {"land_plain", "land_steppe", "land_highland"}, "Wold": {"land_plain", "land_steppe", "land_highland"}})
        self.assertFalse(set().union(*rows.values()) - palette, "every kind a word asks for is a palette row")
        seen = Counter()
        for b, e in self.stock("regions"):
            word = e["name"].split()[-1]
            seen[word] += 1
            self.assertTrue(not rows[word] or rows[word] & kinds_of(b), f"{e['name']}: the palette holds no such land")
        self.assertEqual(set(seen), set(rows), "every region word is drawn somewhere")

    def test_3_a_buildings_root_is_not_its_word(self):
        self.assertIn("parts_differ", self.doc["rules"])
        for _, e in self.stock("buildings"):
            root, word = e["name"].split(" ", 1)
            self.assertNotEqual(root.lower(), word.lower(), e["name"])
        import random
        env = {"roots": [ROOTS["mill"], ROOTS["thorn"]], "tails": [], "whole": [], "kinds": []}
        pattern = next(p for p in self.doc["patterns"]["place"] if p["id"] == "pattern_place_building")
        names = [n for n, _ in dn._names(pattern, env, random.Random(1), 12)]
        self.assertIn("Thorn Mill", names)
        self.assertNotIn("Mill Mill", names)

    def test_4_the_one_root_ship_is_a_creature_or_one_of_five_words(self):
        parts = "bone antler fang claw talon hoof hide herd nest horn".split()
        five = {"wave", "pearl", "star", "dawn", "comet"}
        self.assertEqual({r for r, row in ROOTS.items() if row.get("creature") is False}, set(parts))
        one = both = 0
        for _, e in self.stock("ships"):
            if e["pattern"] == "pattern_ship_root":
                one += 1
                row = ROOTS[e["head"]]
                self.assertTrue(e["head"] in five or ("animal" in row["tags"] and row.get("creature") is not False), e["name"])
            else:
                both += 1
        self.assertTrue(one and both)

    def test_5_the_marked_adjectives_follow_the_adjective_rule(self):
        marked = {r for r, row in ROOTS.items() if row.get("adjective")}
        self.assertEqual(len(marked), 16)
        for b in self.births:
            for slot in ("people", "phenomenon"):
                self.assertFalse({c["root"] for c in b["candidates"][slot]["names"]} & marked)
            cal = b["naming"]["calendar"]
            self.assertFalse(set(cal["month_roots"] + cal["day_roots"]) & marked)
        for _, e in self.stock("epithets"):
            if e["pattern"] != "pattern_epithet_one":
                self.assertNotIn(e["head"], marked, e["name"])

    def test_6_the_epithets_take_the_singular_with_the(self):
        self.assertNotIn("plural: true", self.text)
        self.assertFalse(hasattr(dn, "PLURALS") or hasattr(dn, "plural"), "the plural table went with the pattern")
        shapes = Counter()
        for _, e in self.stock("epithets"):
            shape = next((k for k, rx in (("parent", r"^(Mother|Father) of the [A-Z][a-z]+$"), ("lord", r"^(Lord|Lady) of the [A-Z][a-z]+$"),
                                          ("bearer", r"^[A-Z][a-z]+bearer$"), ("one", r"^the [A-Z][a-z]+ One$")) if re.match(rx, e["name"])), None)
            self.assertIsNotNone(shape, e["name"])
            if shape in ("parent", "lord"):
                self.assertEqual(e["name"].split()[-1].lower(), e["head"], "the root as it stands, no plural")
            shapes[shape] += 1
        self.assertEqual(set(shapes), {"parent", "lord", "bearer", "one"})

    def test_7_no_season_names_a_day(self):
        cal = RULES["calendar"]
        self.assertEqual(cal["not_days"], ["spring", "summer", "autumn", "winter"])
        self.assertIn("hollyday", cal["real_words"])
        self.assertFalse(hasattr(dn, "REAL_CALENDAR"), "the list is the table's")
        for b in births(SEEDS):
            c = b["naming"]["calendar"]
            self.assertFalse(set(c["day_roots"]) & set(cal["not_days"]))
            suffix = {"pattern_month_month": "month", "pattern_month_moon": "moon", "pattern_month_fall": "fall"}[c["month_pattern"]]
            spelled = {r + suffix for r in c["month_roots"]} | {r + "day" for r in c["day_roots"]}
            self.assertFalse(spelled & set(cal["real_words"]), spelled & set(cal["real_words"]))


class SecondReading(unittest.TestCase):
    """Build 11c (docs/p1-build-11.md, Part 11c): two rules from the second reading of the pools."""

    def test_inn_is_a_head_only(self):
        self.assertEqual(ROOTS["inn"]["pos"], "head")
        for b in births(POOL_SEEDS):
            for lid in living(b):
                for e in pooled(b)["languages"][lid]["places"]:
                    self.assertFalse(e["name"].lower().endswith("inn") and e["head"] != "inn", e["name"])

    def test_a_season_names_no_month_under_the_fall_pattern(self):
        cal = RULES["calendar"]
        self.assertEqual(cal["not_months_under"], ["pattern_month_fall"])
        seasons = set(cal["not_days"])
        kept = Counter()
        for b in births(SEEDS):
            c = b["naming"]["calendar"]
            hit = seasons & set(c["month_roots"])
            if c["month_pattern"] == "pattern_month_fall":
                self.assertFalse(hit, f"{sorted(hit)} under the fall pattern")
            elif hit:
                kept[c["month_pattern"]] += 1
        self.assertEqual(set(kept), {"pattern_month_month", "pattern_month_moon"}, "under month and moon the seasons stay")


class FullPools(unittest.TestCase):
    """The bag stocks and the secret stock, on a few births of every scale (a full epic pool takes seconds)."""

    @classmethod
    def setUpClass(cls):
        by_scale: dict = {}
        for b in births(POOL_SEEDS):
            by_scale.setdefault(b["dials"]["scale"], []).append(b)
        cls.births = [b for rows in by_scale.values() for b in rows[:3]]
        cls.secrets = []
        for b in cls.births:
            secret: dict = {}
            dn.fill_secret(secret, b["naming"], b["master"], b["dials"], "P1", 1, pooled(b, bag_names=True), registered=set())
            cls.secrets.append(secret)

    def test_every_stock_meets_three_times_the_scale(self):
        for b in self.births:
            pool = pooled(b, bag_names=True)
            need = dn.scale_needs(dt.scale_row(b["dials"]["scale"]))
            alive = living(b)
            self.assertGreaterEqual(len(pool["languages"]["old"]["sites"]), 3 * need["sites"])
            self.assertGreaterEqual(sum(len(pool["languages"][l]["god"]) for l in alive), 3 * need["gods"])
            for lid in alive:
                self.assertGreaterEqual(len(pool["languages"][lid]["person"]), need["persons"] + dn.SPARE_PERSONS)
            self.assertEqual((pool["languages"]["old"]["person"], pool["languages"]["old"]["god"]), ([], []))
            sites = pool["languages"]["old"]["sites"]
            words = dt.load("naming.yaml")["words"]["site_words"]
            self.assertTrue(any(" " in e["name"] for e in sites) and any(" " not in e["name"] for e in sites), "alone, or with a site word")
            for e in sites:
                tail = e["name"].split(" ", 1)[1] if " " in e["name"] else None
                self.assertTrue(tail is None or tail in words or tail.rstrip("s") in words, e["name"])
            self.assertEqual(len({e["word"] for e in sites}), len(sites))

    def test_the_secret_stock_is_disjoint_from_the_public_stocks(self):
        for b, secret in zip(self.births, self.secrets):
            pool = pooled(b, bag_names=True)
            public = dn._all_names(pool) | {c["name"].lower() for s in b["candidates"].values() for c in s["names"]}
            for lid, L in b["naming"]["languages"].items():
                mine = secret["languages"][lid]
                kinds = {"site"} if L["owner"] == "old" else {"person", "god", "place"}
                self.assertEqual({k for k, v in mine.items() if v}, kinds, lid)
                for k, entries in mine.items():
                    self.assertFalse({e["name"].lower() for e in entries} & public, f"{lid} {k}: a secret name is in a public stock")
            public_words = {w.lower() for w in dn._bag_entries(pool)}
            self.assertFalse({w.lower() for w in dn._bag_entries(secret)} & public_words)


def designer_run(*args, check=True):
    import subprocess
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / args[0]), *args[1:]], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{' '.join(args)} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


class OnDisk(unittest.TestCase):
    """P1's preroll writes the record, the pool and the secret stock; the owner rerolls one slot."""

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        cls.name = f"_test-names-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        designer_run("designer.py", "new", cls.name, "--party-size", "2", "--seed", "NAMES-0001", "--lang", "tr", "--scale", "short")
        cls.preroll = designer_run("designer.py", "-c", cls.name, "preroll", "--phase", "P1")
        cls.dir = CAMPAIGNS / cls.name
        cls.written_by = json.loads((cls.dir / "design/naming.json").read_text(encoding="utf-8"))["_meta"]["written_by"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CAMPAIGNS / cls.name, ignore_errors=True)
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def json(self, rel):
        return json.loads((self.dir / rel).read_text(encoding="utf-8"))

    def secret_names(self):
        return [e["name"] for L in self.json("design/dm-only/name-pool-secret.json")["languages"].values() for v in L.values() for e in v]

    def test_the_preroll_writes_the_record_and_the_pools(self):
        naming = self.json("design/naming.json")
        self.assertTrue(naming["rolled"] and naming["stamped"])
        self.assertIn("preroll --phase P1", self.written_by, "the script writes it, no agent")
        self.assertEqual(list(naming["languages"])[0], "people")
        self.assertEqual(list(naming["languages"])[-1], "old")
        for lid, L in naming["languages"].items():
            self.assertLessEqual({"owner", "label", "bag", "group", "roots", "settlement_tails"}, set(L), lid)
            self.assertFalse({"openings", "endings", "onsets"} & set(L), "the bag's parts are read from the table, never copied")
        self.assertEqual(set(naming["candidates"]), set(dn.SLOTS))
        for slot, s in naming["candidates"].items():
            self.assertEqual(len(s["names"]), 4, slot)
            if slot != "phenomenon":          # the reroll test rerolls that slot
                self.assertEqual((s["attempt"], s["discarded"]), (1, []), slot)
            self.assertEqual(s["language"], dn.slot_language(slot, naming))
        self.assertEqual(naming["assignments"], {})
        m = self.json("design/design.json")
        labels = [r["label"] for r in m["dice_log"] if r["phase"] == "P1"]
        self.assertEqual(sum(1 for l in labels if l.startswith("naming_family.")), len(naming["languages"]))
        self.assertGreater(labels.index("naming_family.1"), labels.index("mechanic"))
        pool = self.json("design/dm-only/name-pool.json")
        self.assertTrue(pool["rolled"])
        self.assertEqual(set(pool["languages"]), set(naming["languages"]))
        self.assertTrue(pool["languages"]["people"]["person"] and pool["languages"]["people"]["places"] and pool["languages"]["old"]["sites"])
        self.assertEqual(len(pool["calendar"]["months"]), 14)
        self.assertIn("designer: names", self.preroll.stdout)
        self.assertIn("designer: candidates", self.preroll.stdout)
        before = (self.dir / "design/dm-only/name-pool.json").read_bytes()
        self.assertIsNotNone(dn.ensure_pool(self.name, "P2"))
        self.assertEqual((self.dir / "design/dm-only/name-pool.json").read_bytes(), before, "a full pool is left as it is")

    def test_no_secret_stock_name_reaches_a_public_output(self):
        import design_approval as da
        import design_prompts as dp
        secret = self.secret_names()
        self.assertGreaterEqual(len(secret), 20)
        prompt = dp.render(self.name, "P1.premise")
        self.assertIn("Names (rolled, never invented)", prompt)
        self.assertIn("secret --lang", prompt, "the prompt gives the command, not the names")
        self.assertIn("ruin sites:", prompt)
        self.assertIn("calendar months:", prompt)
        self.assertNotIn("in the same shape", prompt, "the writer composes no place name from roots")
        self.assertNotIn("**`design/naming.json`** from the rolled families", prompt, "the writer's naming task is gone")
        texts = {"design.json": (self.dir / "design/design.json").read_text(encoding="utf-8"),
                 "naming.json": (self.dir / "design/naming.json").read_text(encoding="utf-8"),
                 "name-pool.json": (self.dir / "design/dm-only/name-pool.json").read_text(encoding="utf-8"),
                 "the preroll's printout": self.preroll.stdout, "the P1 prompt": prompt, "the card": da.build_card(self.name, "P1")}
        for where, text in texts.items():
            leaked = [n for n in secret if re.search(rf"(?<![\w]){re.escape(n)}(?![\w])", text)]
            self.assertEqual(len(leaked), 0, f"{len(leaked)} secret-stock name(s) in {where}")
        listed = designer_run("design_names.py", "-c", self.name, "secret", "--lang", "people", "--kind", "person").stdout.split()
        self.assertTrue(listed and set(listed) <= set(secret), "the agent reads them from the command's output")
        self.assertEqual(designer_run("design_names.py", "-c", self.name, "secret", "--lang", "nowhere", "--kind", "person", check=False).returncode, 1)

    def test_the_owners_reroll(self):
        before = self.json("design/naming.json")["candidates"]["phenomenon"]
        proc = designer_run("design_names.py", "-c", self.name, "reroll", "--slot", "phenomenon")
        after = self.json("design/naming.json")["candidates"]["phenomenon"]
        old, new = [c["name"] for c in before["names"]], [c["name"] for c in after["names"]]
        self.assertEqual((len(new), after["attempt"]), (4, 2))
        self.assertFalse(set(old) & set(new), "four fresh candidates")
        self.assertEqual(after["discarded"], [before["names"]], "the old four stay in the record")
        self.assertIn(new[0], proc.stdout)
        self.assertEqual(dn.main(["-c", "a-real-campaign", "reroll", "--slot", "people"]), 1, "outside _test-* it asks for --onay")
        for folder in (SCRIPTS.parent / "prompts", SCRIPTS.parents[2] / "workflows"):
            for path in folder.rglob("*"):
                if path.is_file() and path.suffix in (".md", ".js", ".json"):
                    self.assertNotIn("reroll --slot", path.read_text(encoding="utf-8", errors="replace"), f"{path.name}: only the owner rerolls")

    def test_approve_records_the_roots(self):
        import design_dice as dd
        naming = self.json("design/naming.json")
        designer.record_used(self.name, "P1")
        mine = dd.load_used()["campaigns"][self.name]
        roots = [r for L in naming["languages"].values() for r in L["roots"]] + naming["calendar"]["month_roots"] + naming["calendar"]["day_roots"]
        self.assertEqual(sorted(mine[LEX]), sorted(roots))
        self.assertEqual(len(mine[dn.FAMILY]), len(naming["languages"]))


class Door(unittest.TestCase):
    """Section 12: a public person or god takes no secret-stock name (the fixture stands in: a legacy birth)."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("names")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_a_public_person_with_a_secret_stock_name_is_refused(self):
        self.c.reopen("P2", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P2", "--attempt", "9", check=True)
        pool = self.c.json("design/dm-only/name-pool.json")
        lang = sorted(pool["languages"])[0]
        self.c.write_json("design/dm-only/name-pool-secret.json",
                          {"_meta": {"schema_version": 1, "campaign": self.c.name},
                           "languages": {lang: {"person": [{"name": "Quelmara", "used_by": None}], "god": []}}})
        self.c.reopen("P5", "running")
        public = row("npc_namesmirror", "npc", "Quelmara Reedwright", created_phase="P5", lang=lang)
        self.c.write_json("design/_staging/P5/npc_namesmirror.json", fragment("npc_namesmirror", public))
        refused = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertIn("may not take a name of the secret stock", refused.stderr)
        self.assertNotIn("npc_namesmirror", self.c.json("design/dm-only/entities.json")["entities"])

    def test_a_legacy_birth_keeps_its_languages_and_its_pool(self):
        before = self.c.path("design/naming.json").read_bytes()
        self.assertNotIn("rolled", self.c.json("design/naming.json"))
        self.c.reopen("P2", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P2", "--attempt", "9", check=True)
        self.assertEqual(self.c.path("design/naming.json").read_bytes(), before, "nothing is re-rolled for it")
        pool = self.c.json("design/dm-only/name-pool.json")
        self.assertNotIn("rolled", pool)
        self.assertEqual(set(pool["places"]), set(pool["languages"]), "its place candidates, as before")
        self.assertFalse(self.c.path("design/dm-only/name-pool-secret.json").exists(), "and no secret stock")
        import design_prompts as dp
        self.assertIn("or a compound of the language's roots in the same shape", dp.render(self.c.name, "P5.npc", "npc_draskun"))


if __name__ == "__main__":
    if "--report" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--report") + 1]
        os.makedirs(out_dir, exist_ok=True)
        for name in ("test_the_half_share", "test_a_landlocked_palette_gets_no_sea_root_in_the_called_half"):
            getattr(Roots(name), name)()
        Pools.setUpClass()
        Pools("test_the_stocks_spread_their_heads_and_meet_the_scales_need").test_the_stocks_spread_their_heads_and_meet_the_scales_need()
        print(f"seeds: {SEEDS} (rolls), {POOL_SEEDS} (stocks)")
        short, total = Roots.short_rate
        print(f"the called pool was too small: {short} of {total} language draws ({100 * short / total:.2f} %)")
        fh = Roots.free_half
        print(f"free half: {fh['off the palette']} of {fh['free roots']} roots carry a land tag the palette calls nowhere "
              f"({100 * fh['off the palette'] / fh['free roots']:.1f} %); {fh['sea roots in their free half']} sea roots in the free halves of "
              f"{fh['landlocked births']} landlocked births")
        for scale in ("short", "standard", "epic"):
            need = dn.scale_needs(dt.scale_row(scale))
            print(f"{scale}: need {need}")
            for living_n in (2, 3):
                print(f"  per language with {living_n} living: {dn.stock_sizes(scale, living_n)}")
            print("  smallest campaign totals over the seeds: " + ", ".join(f"{k} {v}" for (s, k), v in sorted(Pools.smallest.items()) if s == scale))
            b = next(x for x in births(POOL_SEEDS) if x["dials"]["scale"] == scale)
            pool = pooled(b, bag_names=True)
            with open(os.path.join(out_dir, f"pool-{scale}.txt"), "w", encoding="utf-8") as fh_out:
                fh_out.write(f"seed {b['master']} · {scale}\n")
                for lid, L in b["naming"]["languages"].items():
                    fh_out.write(f"\n{lid} — {L['bag']} (group {L['group']}); calls {L.get('called_tags')}\n  roots: {' '.join(L['roots'])}\n"
                                 f"  called half: {' '.join(L.get('called', []))}\n  settlement tails: {' '.join(L['settlement_tails'])}\n")
                    for key, entries in pool["languages"][lid].items():
                        fh_out.write(f"  {key} ({len(entries)}): " + ", ".join(e["name"] for e in entries) + "\n")
                fh_out.write(f"\ncalendar — {b['naming']['calendar']['month_pattern']}\n")
                for key, entries in pool["calendar"].items():
                    fh_out.write(f"  {key}: " + ", ".join(e["name"] for e in entries) + "\n")
                for slot, s in b["candidates"].items():
                    fh_out.write(f"candidates {slot}: " + ", ".join(c["name"] for c in s["names"]) + "\n")
        print("pools:", out_dir)
    else:
        unittest.main()
