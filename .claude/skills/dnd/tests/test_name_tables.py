"""
test_name_tables.py — build item 11a (docs/p1-build-11.md, Part 11a; the owner's decisions 1-45 there): the name
tables (seventeen part bags, 505 roots, the patterns without examples, the word lists, the three filter lists) and the
part-bag generator for person and god names: the yield and the overlap of every bag with every filter on, the
blacklists, and the legacy path a birth from before this item keeps.
"""

import random
import re
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_names as dn  # noqa: E402
import design_tables as dt  # noqa: E402
import registry  # noqa: E402

DOC = dt.load("naming.yaml")
TEXT = (dt.tables_dir() / "naming.yaml").read_text(encoding="utf-8")
BAGS = dt.rows("naming.yaml#family")
LEX = DOC["lexicon"]
ROOTS = LEX["roots"]
TAGS = [t["tag"] for t in LEX["tags"]]
SEEDS = 200
ADJECTIVE_TAGS = ("colour", "direction and age")


def need() -> int:
    """What one language must yield: the named-NPC band's top of the largest scale plus the spares (scale.yaml)."""
    return max(dt.band(s["named_npcs"])[1] for s in dt.rows("scale.yaml")) + dn.SPARE_PERSONS


def draw(bag: dict, seed: int, n: int) -> list[str]:
    return dn.draw_names(random.Random(f"{bag['id']}:{seed}"), {"bag": bag["id"]}, n, [])


class Bags(unittest.TestCase):

    def test_seventeen_bags_in_five_groups(self):
        self.assertEqual(len(BAGS), 17)
        self.assertEqual(Counter(b["group"] for b in BAGS), {"A": 4, "B": 4, "C": 3, "D": 3, "E": 3})
        self.assertEqual(DOC["roll"]["notation"], "d17")
        self.assertTrue(DOC["roll"]["avoid_used"])
        for b in BAGS:
            with self.subTest(bag=b["id"]):
                self.assertEqual(set(b), {"id", "label", "group", "openings", "middles", "middle_chance", "endings", "vowel_join", "real_ok"})
                self.assertTrue(b["id"].startswith("family_"))
                self.assertGreaterEqual(len(b["openings"]), 40)
                self.assertGreaterEqual(len(b["endings"]), 28)
                self.assertEqual(bool(b["middles"]), b["middle_chance"] > 0)
                for part in b["openings"] + b["middles"] + b["endings"]:
                    self.assertIsInstance(part, str, "YAML read a part as something else (On, No, Yes)")
                    self.assertRegex(part, r"^[A-Za-z]+$")
                self.assertEqual(len(set(b["openings"])), len(b["openings"]))
        self.assertEqual([b["id"] for b in BAGS if b["real_ok"]], ["family_rustic"])
        self.assertEqual({b["id"] for b in BAGS if b["vowel_join"]},
                         {"family_old_isle", "family_sibilant", "family_lake_folk", "family_old_mountain"})
        self.assertFalse(any(h["phase"] == "P1" for h in DOC["hooks_common"]), "no mutation: the P1 line went (decision 16)")

    def test_the_old_family_shape_is_gone(self):
        for word in ("onsets", "nuclei", "codas", "forbidden_clusters", "best_for", "samples_person", "samples_god", "feel:",
                     "examples", "meaning", "domains", "place_tails", "tr_suffix_friendly", "label_tr", "tr:"):
            self.assertNotIn(word, TEXT, word)

    def test_the_join_and_shape_rules(self):
        self.assertEqual(dn.join("Kor", "rik", False), "Korik", "a doubled letter at a join is dropped")
        self.assertIsNone(dn.join("Ka", "eni", False), "a vowel never meets a vowel")
        self.assertIsNone(dn.join("Aed", "kan", True), "a vowel_join bag never joins consonant to consonant")
        self.assertEqual(dn.join("Aed", "an", True), "Aedan")
        self.assertFalse(dn.bag_shape_ok("Tega"), "five letters at least")
        self.assertFalse(dn.bag_shape_ok("Karstgrad"), "no four consonants in a row")
        self.assertFalse(dn.bag_shape_ok("Lalana"), "no two-letter chunk repeated at once")
        self.assertFalse(dn.bag_shape_ok("Kormakor"), "no three-letter chunk repeated anywhere")
        self.assertTrue(dn.bag_shape_ok("Kelvdun"))
        self.assertEqual(DOC["rules"]["join"]["min_letters"], 5)


class Lexicon(unittest.TestCase):

    def test_505_roots(self):
        tails = LEX["settlement_tails"]
        self.assertEqual((len(ROOTS), len(tails)), (483, 22))
        tagged = [r for r in ROOTS if r["tags"]]
        self.assertEqual((len(tagged) + len(tails), len(ROOTS) - len(tagged)), (484, 21), "484 tagged, the tails among them; 21 untagged")
        names = [r["root"] for r in ROOTS] + list(tails)
        self.assertEqual(len(set(names)), 505, "no root twice")
        for r in ROOTS:
            self.assertEqual(set(r), {"root", "pos", "tags"}, r["root"])
            self.assertIsInstance(r["root"], str)
            self.assertRegex(r["root"], r"^[a-z]+$")
            self.assertIn(r["pos"], ("head", "tail", "either"))
            self.assertTrue(len(r["tags"]) <= 2 and not set(r["tags"]) - set(TAGS), r["root"])
            self.assertNotIn("settlement", r["tags"], "the settlement tails are their own list")
        self.assertEqual(Counter(r["pos"] for r in ROOTS if r["tags"]), {"head": 302, "tail": 118, "either": 42}, "302 heads, 140 tails with the 22, 42 either")
        untagged = {r["root"] for r in ROOTS if not r["tags"]}
        self.assertTrue({"salt", "tide", "lantern", "candle", "bell", "hush", "debt", "crown"} <= untagged, "the attractor's roots stay, called by nothing")
        self.assertTrue({"ash", "ember", "cinder"} <= {r["root"] for r in ROOTS if r["tags"][:1] == ["fire"]})

    def test_the_closed_tag_list_and_what_calls_each_tag(self):
        self.assertEqual(len(TAGS), 22)
        self.assertEqual(len(set(TAGS)), 22)
        palette = {r["id"] for r in dt.rows("foundation.yaml#palette")}
        families = {r["family"] for r in dt.rows("foundation.yaml#lifeline")}
        called_kinds, called_families = set(), set()
        for t in LEX["tags"]:
            called = t.get("called_by") or {}
            self.assertFalse(set(called) - {"palette", "lifeline_family"}, t["tag"])
            self.assertFalse(set(called.get("palette") or []) - palette, t["tag"])
            self.assertFalse(set(called.get("lifeline_family") or []) - families, t["tag"])
            called_kinds |= set(called.get("palette") or [])
            called_families |= set(called.get("lifeline_family") or [])
        self.assertEqual(palette - called_kinds, {"land_thin_place"}, "the thin place calls nothing")
        self.assertEqual(families - called_families, {"water", "treaty"}, "the water family calls by its seat; the treaty family calls nothing")
        self.assertEqual(LEX["lifeline_by_seat"], {"water": ["fresh water", "sea"]})
        uncalled = [t["tag"] for t in LEX["tags"] if not t.get("called_by")]
        self.assertEqual(uncalled, ["settlement", "colour", "direction and age", "weather and season", "war and watch", "holy and oath"])
        by_tag = {t["tag"]: t.get("called_by") or {} for t in LEX["tags"]}
        self.assertEqual(by_tag["animal"], {"lifeline_family": ["creatures"], "palette": ["land_giant_bones"]})

    def test_adjectives_are_derived(self):
        adjectives = [r["root"] for r in ROOTS if r["tags"][:1] and r["tags"][0] in ADJECTIVE_TAGS]
        self.assertEqual(len(adjectives), 32, "14 colour and 18 direction and age roots; none is hand-marked")
        self.assertNotIn("adjective:", "".join(str(r) for r in ROOTS))


class Patterns(unittest.TestCase):

    def test_the_patterns_by_kind(self):
        pats = DOC["patterns"]
        self.assertEqual({k: len(v) for k, v in pats.items()},
                         {"place": 7, "institution": 4, "people": 3, "phenomenon": 2, "month": 4, "day": 1, "old_tongue": 2,
                          "god_epithet": 4, "ship": 2})
        ids = [p["id"] for rows in pats.values() for p in rows]
        self.assertEqual(len(ids), len(set(ids)))
        for rows in pats.values():
            for p in rows:
                self.assertTrue(p["parts"] and p["join"] in ("joined", "apart"), p["id"])
                self.assertNotIn("pattern", p, "slots, not prose")
        self.assertEqual([p["id"] for p in pats["month"] if p.get("rollable")], ["pattern_month_month", "pattern_month_moon", "pattern_month_fall"])
        self.assertEqual(pats["institution"][3]["only_form"], "form_house")
        self.assertEqual({k: len(v) for k, v in DOC["words"].items()},
                         {"region_words": 12, "building_words": 12, "phenomenon_tails": 12, "site_words": 8})

    def test_which_slots_take_an_adjective(self):
        """Decision 35: no in "of the …", months, days, people, phenomenon; yes in place names, the + root + form word,
        inns, ships and "the … One"."""
        def root_slots(p):
            for part in p["parts"]:
                for x in [part] + list(part.get("one_of") or []):
                    if "root" in x:
                        yield x
        pats = DOC["patterns"]
        for kind in ("people", "phenomenon", "month", "day"):
            for p in pats[kind]:
                self.assertTrue(all(s.get("adjective") is False for s in root_slots(p)), p["id"])
        by = {p["id"]: p for rows in pats.values() for p in rows}
        self.assertTrue(all(s["adjective"] is False for s in root_slots(by["pattern_institution_form_of_root"])))
        self.assertTrue(all(s["adjective"] is True for s in root_slots(by["pattern_institution_root_form"])))
        for pid in ("pattern_place_settlement", "pattern_place_region", "pattern_place_building"):
            self.assertTrue(next(root_slots(by[pid]))["adjective"], pid)
        for pid in ("pattern_place_inn", "pattern_ship_colour_animal", "pattern_epithet_one"):
            self.assertIn("colour", next(root_slots(by[pid]))["tags"], pid)

    def test_the_deleted_patterns_are_gone(self):
        for gone in ("Court of", "Assize", "tide", "Keepers of", "bound", "Ones", " Who ", "Watch", "Guild of", "Fellowship", "{Head}", "{Noun}"):
            self.assertNotIn(gone, str(DOC["patterns"]), gone)
        self.assertNotIn("First", str(DOC["patterns"]["month"]))

    def test_every_form_has_its_name_words(self):
        forms = {r["id"]: r for r in dt.rows("signatures.yaml#institution_form")}
        self.assertEqual({k: r["name_words"] for k, r in forms.items()}, {
            "form_order": ["Order"], "form_guild": ["Guild"], "form_company": ["Company"], "form_house": ["House"],
            "form_council": ["Council"], "form_league": ["League"], "form_school": ["School"],
            "form_brotherhood": ["Brotherhood", "Sisterhood", "Fellowship"], "form_cloister": ["Cloister"],
            "form_travelling": ["Caravan", "Fleet", "Troupe"], "form_society": ["Society"], "form_chartered": ["Chartered Company"],
            "form_confederacy": ["Confederacy"], "form_militia": ["Militia"]})
        self.assertFalse(any("form_word" in r for r in forms.values()), "the old single word went")
        water = {"land_coast", "land_island", "land_stone_sea", "land_river", "land_lake", "land_marsh", "land_sky_river"}
        self.assertEqual(set(forms["form_travelling"]["name_word_requires"]["Fleet"]["any_of"]), water)
        self.assertEqual(forms["form_chartered"]["label"], "Privileged company", "the form's label stays what it is")


class Filters(unittest.TestCase):

    def test_the_three_lists(self):
        bl = DOC["blacklist"]
        self.assertEqual(len(bl["real_given"]), 599, "524 names and the 75 the audit of build 11a added")
        self.assertEqual(len(bl["plain_words"]), 118, "110 plain words and the 8 the audit added")
        self.assertGreater(len(bl["real_places"]), 100)
        for key in ("real_given", "plain_words", "real_places"):
            self.assertEqual(len(set(bl[key])), len(bl[key]), key)
            for w in bl[key]:
                self.assertIsInstance(w, str)
                self.assertEqual(w, w.lower())
        self.assertTrue({"pellet", "koran", "naval", "heathen", "mirror"} <= set(bl["plain_words"]))
        self.assertFalse({"pellet", "heathen", "mirror", "market"} & set(bl["real_given"]), "real_given holds names only")
        self.assertTrue({"torsten", "arwen", "gunhild", "ishan"} <= set(bl["real_given"]))
        door = (SCRIPTS / "registry.py").read_text(encoding="utf-8")
        for key in ("real_given", "plain_words", "real_places"):
            self.assertNotIn(key, door, "the door does not read the filters")

    def test_a_plain_word_is_refused_for_every_bag(self):
        plain = dn.plain_words()
        word = next(w for w in sorted(plain - dn.real_given()) if 5 <= len(w) <= 8 and w.isalpha() and
                    not registry.naming_errors("probe", {"type": "npc", "name": w.capitalize()}, registry.naming_blacklist(), set()))
        caps = {"ending": 9, "opening": 9}
        self.assertFalse(dn.acceptable(word.capitalize(), {}, [], caps, "person", bag={"real_ok": False}))
        self.assertFalse(dn.acceptable(word.capitalize(), {}, [], caps, "person", bag={"real_ok": True}), "real_ok lifts the names only")
        self.assertTrue(dn.acceptable(word.capitalize(), {}, [], caps, "person"), "a legacy language is not filtered")

    def test_the_real_name_filter_is_off_for_a_real_ok_bag(self):
        real = dn.real_given()
        word = next(w for w in sorted(real - dn.plain_words()) if 5 <= len(w) <= 8 and w.isalpha() and
                    not registry.naming_errors("probe", {"type": "npc", "name": w.capitalize()}, registry.naming_blacklist(), set()))
        caps = {"ending": 9, "opening": 9}
        strict, loose = {"real_ok": False}, {"real_ok": True}
        self.assertFalse(dn.acceptable(word.capitalize(), {}, [], caps, "person", bag=strict))
        self.assertTrue(dn.acceptable(word.capitalize(), {}, [], caps, "person", bag=loose))
        self.assertTrue(dn.acceptable(word.capitalize(), {}, [], caps, "person"), "a legacy language is not filtered")


class Yield(unittest.TestCase):
    """Every bag, every filter on: the epic need over 200 seeds, and two births on one bag stay apart."""

    @classmethod
    def setUpClass(cls):
        cls.n = need()
        cls.runs = {b["id"]: [draw(b, seed, cls.n) for seed in range(SEEDS)] for b in BAGS}

    def test_every_bag_gives_the_epic_need_on_every_seed(self):
        self.assertGreaterEqual(self.n, 86)
        worst = {bid: min(len(names) for names in runs) for bid, runs in self.runs.items()}
        type(self).worst_yield = worst
        self.assertEqual({k: v for k, v in worst.items() if v < self.n}, {}, f"a bag gave fewer than {self.n} names")

    def test_two_births_on_one_bag_share_few_names(self):
        worst = {}
        for bid, runs in self.runs.items():
            sets = [set(names[:100]) for names in runs]
            worst[bid] = max(len(sets[i] & sets[i + 1]) for i in range(len(sets) - 1))
        type(self).worst_overlap = worst
        self.assertEqual({k: v for k, v in worst.items() if v > 25}, {}, "two births on one bag share more than 25 of their names")

    def test_no_generated_name_is_on_a_blacklist(self):
        bl = registry.naming_blacklist()
        exact = {str(x).lower() for k in ("exact", "mythology", "llm_favourites", "turkish_as_name") for x in (bl.get(k) or [])}
        exact |= {str(x).lower() for x in bl["owner_banned"]["exact"]}
        stems = [s.lower() for s in bl["owner_banned"]["stems"] + bl["substrings"]]
        real, plain = dn.real_given(), dn.plain_words()
        ok = {b["id"]: b["real_ok"] for b in BAGS}
        self.assertIn("family_rustic", self.runs)
        for bid, runs in self.runs.items():
            names = {n.lower() for names in runs[:40] for n in names}
            self.assertFalse(names & exact, bid)
            self.assertFalse([n for n in names if any(s in n for s in stems)], bid)
            self.assertFalse({n.lower() for names in runs for n in names} & plain, f"{bid}: a plain word came through")
            if not ok[bid]:
                self.assertFalse(names & real, f"{bid}: a real given name came through")
            for n in list(names)[:200]:
                self.assertTrue(n.isalpha() and 5 <= len(n) <= 9, n)

    def test_the_same_seed_gives_the_same_names(self):
        b = BAGS[0]
        self.assertEqual(draw(b, 7, 30), draw(b, 7, 30))
        self.assertNotEqual(draw(b, 7, 30), draw(b, 8, 30))


class Legacy(unittest.TestCase):

    LANG = {"onsets": ["v", "m", "r", "l", "s", "n", "t", "k", ""], "nuclei": ["a", "e", "i", "o", "u"],
            "codas": ["n", "r", "l", "s", "m", ""], "length": [2, 3], "forbidden_clusters": ["rr", "ll"]}

    def test_a_legacy_language_draws_by_the_old_path(self):
        self.assertIsNone(dn.bag_of(self.LANG))
        names = dn.draw_names(random.Random(3), self.LANG, 20, [])
        self.assertEqual(len(names), 20)
        again = dn.draw_names(random.Random(3), self.LANG, 20, [])
        self.assertEqual(names, again)
        self.assertTrue(all("rr" not in n.lower() and "ll" not in n.lower() for n in names), "its own forbidden clusters still hold")

    def test_a_bag_language_names_its_bag(self):
        self.assertEqual(dn.bag_of({"bag": "family_sung"})["group"], "C")
        self.assertIsNone(dn.bag_of({}))


class Stamps(unittest.TestCase):

    def test_the_name_tables_are_stamped(self):
        covered = dt.reviewed_rows()
        self.assertIn("naming.yaml#family", dt.REVIEWED_TABLES)
        for b in BAGS:
            self.assertEqual(covered[b["id"]], dt.row_hash(b))
        naming = {k for k in covered if k.startswith("naming:")}
        self.assertEqual(len([k for k in naming if k.startswith("naming:root:")]), 483)
        self.assertEqual(len([k for k in naming if k.startswith("naming:tag:")]), 22)
        self.assertEqual(len([k for k in naming if k.startswith("naming:pattern:")]), 29)
        self.assertEqual(len([k for k in naming if k.startswith("naming:words:")]), 4)
        self.assertIn("naming:settlement_tails", naming)
        self.assertEqual(dt.unreviewed(), {"missing": [], "changed": [], "gone": []})


if __name__ == "__main__":
    if "--report" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--report") + 1]
        import os
        os.makedirs(out_dir, exist_ok=True)
        Yield.setUpClass()
        y = Yield("test_every_bag_gives_the_epic_need_on_every_seed")
        y.test_every_bag_gives_the_epic_need_on_every_seed()
        y.test_two_births_on_one_bag_share_few_names()
        real, plain = dn.real_given(), dn.plain_words()
        print(f"need per language: {Yield.n}; seeds: {SEEDS}")
        print(f"{'bag':<22} group  worst yield  worst overlap  dropped by the real-name and plain-word filters in 2,000 draws")
        for b in BAGS:
            rng = random.Random(f"{b['id']}:drops")
            made = [dn._bag_name(rng, b) for _ in range(2000)]
            dropped = sum(1 for w in made if w and (w.lower() in plain or (w.lower() in real and not b["real_ok"])))
            print(f"{b['id']:<22} {b['group']:<6} {Yield.worst_yield[b['id']]:<12} {Yield.worst_overlap[b['id']]:<14} {dropped}")
            names = dn.draw_names(random.Random(f"{b['id']}:sample"), {"bag": b["id"]}, 200, [])
            with open(os.path.join(out_dir, f"{b['id']}.txt"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(names) + "\n")
        print("samples:", out_dir)
    else:
        unittest.main()
