"""
test_identity_tables.py — the identity's three signatures (plan item 25 step 2; docs/p1-build-8.md, after the tag
review in docs/p1-tags.md): the approved counts and families, a visible and a behaving piece, the archetype headings
of the form, the practice and the power, the rule kinds, the gates, the rows that need a break that has happened, the
phenomenon rule families every ruin source can reach, the waits, clean phrases, no
claim, no removed id, every named row real, every row stamped.
"""

import re
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_compare  # noqa: E402
import design_tables as dt  # noqa: E402

S = "signatures.yaml#"
rows = lambda sub: dt.rows(S + sub)
FOUNDATION = dt.load("foundation.yaml")
ARCHETYPES = {r["id"][len("archetype_"):] for r in dt.rows("factions.yaml#archetype")}
HEADINGS = ("state", "religious", "martial", "guild", "trade", "scholarly", "criminal", "resistance")
NEW = ("people_lineage", "people_trait", "people_attitude", "institution_form", "institution_practice", "institution_sign",
       "institution_power", "phenomenon_rule", "phenomenon_sign", "phenomenon_limit", "phenomenon_user")
REMOVED = (
    "trait_adult_names", "trait_lies_foul_the_air", "trait_iron_is_unlucky", "trait_winter_sleep", "trait_two_homes",
    "trait_never_stop", "trait_seven_year_rotation", "trait_one_great_building", "trait_guest_three_days", "trait_one_envoy",
    "trait_herd_dreams", "trait_live_on_water",
    "practice_wall_builders", "practice_empty_temples", "practice_guard_the_herds", "practice_lifeline_craft",
    "practice_raise_the_orphans", "practice_mend_the_wound", "practice_watch_the_sky",
    "practice_royal_monopoly", "practice_dragon_giant_hunters", "power_charter",          # renamed
    "isign_unarmed", "isign_no_marriage", "isign_own_no_land", "isign_kneel_to_no_one", "isign_no_night_travel",
    "limit_remnant_matter_absorbs", "limit_underground_only", "limit_once_a_day", "limit_a_day_from_remnant")


def per_heading(sub):
    return Counter(h for r in rows(sub) for h in r["hints"])


def weights(r):
    """{row id: factor} over the row's `weight_by` lines that name rows."""
    return {x: w["x"] for w in r.get("weight_by") or [] for x in (w["when"].get("any_of") or [])}
ATTRACTORS = re.compile(r"(candle|wax|lamp|lantern|bell|hush|silent|silence|ledger|toll|tribute|court|judgement|tide|"
                        r"salt|the dead|rights of the dead)s?", re.IGNORECASE)


def phrases(r):
    tr = r.get("text") or {}
    return [v for k, v in tr.items() if not k.endswith("_note") and isinstance(v, str)]


class People(unittest.TestCase):

    def test_lineages(self):
        lin = {r["id"]: r for r in rows("people_lineage")}
        self.assertEqual(len(lin), 16, "15 in the rows file, the half-elf and half-orc as two rows")
        self.assertEqual({k for k, r in lin.items() if not r["playable"]},
                         {"lineage_giant_kin", "lineage_merfolk", "lineage_lizardfolk", "lineage_centaur", "lineage_goblinoid", "lineage_fey"})
        self.assertEqual(max(lin.values(), key=lambda r: r.get("weight", 1))["id"], "lineage_human")
        self.assertEqual(dt.roll_header(S + "people_lineage").get("row_wait"), 1, "the previous birth's lineage waits one birth")
        self.assertFalse(dt.roll_header(S + "people_lineage").get("avoid_used"))
        ctx = arb.Context(rolled={"land_forest": False})
        self.assertEqual(arb.weight_of(lin["lineage_elf"], ctx), 3)

    def test_the_lineages_fit_their_foundation_rows(self):
        lin = {r["id"]: r for r in rows("people_lineage")}
        for rid, fits in {
            "lineage_giant_kin": ["life_giant_peace", "contest_humans_giants", "ruin_giants_land", "ruin_giants_and_dragons"],
            "lineage_fey": ["life_fey_bargain", "contest_humans_fey", "ruin_elven_withdrawal"],
            "lineage_merfolk": ["life_sea_folk_hunt", "contest_land_sea_folk", "spine_above_below_sea", "ruin_great_flood"],
            "lineage_goblinoid": ["break_monsters_have_treaties"],
        }.items():
            for other in fits:
                self.assertEqual(arb.weight_of(lin[rid], arb.Context(rolled={other: False})), 3, f"{rid} with {other}")
        self.assertFalse(any(r.get("requires") or r.get("conflicts_with") for r in lin.values()), "weights only")

    def test_traits_thirty_nine_in_seven_families(self):
        traits = rows("people_trait")
        self.assertEqual(len(traits), 39)
        fams = Counter(r["family"] for r in traits)
        self.assertEqual(fams, {"body": 7, "custom": 5, "creature_bond": 6, "belief": 6, "social_order": 5,
                                "break_relation": 7, "place_movement": 3})
        self.assertEqual(Counter(r["kind"] for r in traits), {"visible": 16, "behaving": 23})
        for r in traits:
            want = "visible" if r["family"] in ("body", "creature_bond", "place_movement") else "behaving"
            self.assertEqual(r["kind"], want, r["id"])
            self.assertTrue(r["text"]["at_table"])
            self.assertFalse(r.get("conflicts_with"), f"{r['id']}: no trait carries a clash")
        self.assertTrue(dt.roll_header(S + "people_trait")["avoid_used"])

    def test_the_sacred_animal(self):
        r = dt.row(S + "people_trait", "trait_sacred_animal")
        self.assertEqual((r["family"], r["kind"]), ("belief", "behaving"))
        self.assertEqual(r["hooks"], [{"phase": "P5", "must": "the sacred animal is never the one the lifeline kills"}])

    def test_the_trait_weights(self):
        traits = {r["id"]: r for r in rows("people_trait")}
        craft = [r["id"] for r in dt.rows("foundation.yaml#lifeline") if r.get("family") == "craft"]
        self.assertTrue(craft)
        want = {
            "trait_underground_by_day": ({"break_night_is_safe"}, 2),
            "trait_fled_the_break": ({"scar_people_displaced"}, 3),
            "trait_first_changed": ({"scar_new_people"}, 3),
            "trait_bee_council": ({"life_bee_forests"}, 3),
            "trait_giant_insect_homes": ({"life_giant_insects"}, 3),
            "trait_giant_birds": ({"life_griffon_eyries"}, 3),
            "trait_hunt_with_wolves": ({"life_deer_migration"}, 2),
            "trait_dolphin_fishers": ({"life_fish_run", "life_oyster_beds"}, 2),
            "trait_mountain_spirits": ({"life_copper_mine", "life_iron_coal", "life_quarry", "life_gemstones"}, 2),
            "trait_workshops_not_families": (set(craft), 2),
            "trait_history_danced": ({"break_no_writing"}, 2),
        }
        for rid, (others, x) in want.items():
            self.assertEqual(weights(traits[rid]), {o: x for o in others}, rid)
        self.assertEqual({k for k, r in traits.items() if r.get("weight_by")}, set(want), "no other trait is weighted")

    def test_attitudes(self):
        att = {r["id"]: r for r in rows("people_attitude")}
        self.assertEqual(len(att), 6)
        self.assertEqual(weights(att["stranger_merchant"]), {"trait_haggling_art": 2}, "the attitude is rolled after the traits")
        self.assertEqual([k for k, r in att.items() if r.get("weight_by") or r.get("requires")], ["stranger_merchant"])


class Institution(unittest.TestCase):

    def test_the_archetype_is_the_heading(self):
        """The form, the practice and the power are drawn only from the rows under the role's archetype (item 10
        applies it): every row lists its archetypes, and no heading runs short."""
        self.assertFalse(set(HEADINGS) - ARCHETYPES, "the eight headings are faction archetypes")
        for sub in ("institution_form", "institution_practice", "institution_power"):
            for r in rows(sub):
                self.assertTrue(r.get("hints"), f"{r['id']} lists no archetype")
                self.assertFalse(set(r["hints"]) - set(HEADINGS), r["id"])
                self.assertEqual(len(r["hints"]), len(set(r["hints"])), r["id"])
        self.assertEqual(per_heading("institution_practice"),
                         {"guild": 19, "religious": 12, "trade": 11, "martial": 10, "state": 9, "scholarly": 9, "criminal": 6,
                          "resistance": 5})
        for sub, floor in (("institution_practice", 5), ("institution_form", 3), ("institution_power", 3)):
            got = per_heading(sub)
            for h in HEADINGS:
                self.assertGreaterEqual(got[h], floor, f"{sub}: {h}")
        self.assertNotIn("hint_weight", dt.roll_header(S + "institution_form"), "the hints are a requirement, not a weight")

    def test_forms_carry_their_word_and_hints(self):
        forms = {r["id"]: r for r in rows("institution_form")}
        self.assertEqual(len(forms), 14)
        for r in forms.values():
            self.assertTrue(r["form_word"])
        self.assertEqual({k: sorted(r["hints"]) for k, r in forms.items()}, {k: sorted(v.split()) for k, v in {
            "form_order": "religious martial scholarly", "form_guild": "guild trade", "form_company": "martial",
            "form_house": "state guild trade criminal", "form_council": "state", "form_league": "trade guild criminal",
            "form_school": "scholarly", "form_brotherhood": "resistance religious guild martial criminal",
            "form_cloister": "religious scholarly", "form_travelling": "guild trade criminal resistance",
            "form_society": "criminal scholarly resistance", "form_chartered": "trade",
            "form_confederacy": "state martial resistance", "form_militia": "martial resistance"}.items()})
        self.assertEqual((forms["form_chartered"]["label"], forms["form_chartered"]["form_word"]),
                         ("Privileged company", "Trading Company"), "a written charter clashed with a land without writing")

    def test_practices_thirty_three(self):
        pr = {r["id"]: r for r in rows("institution_practice")}
        self.assertEqual(len(pr), 34, "33 after the tag review and the enchanted goods (16b)")
        self.assertEqual(Counter(r["family"] for r in pr.values()),
                         {"guard": 3, "carry": 5, "make": 4, "know": 4, "care": 4, "war": 5, "trade": 5, "faith": 4})
        for r in pr.values():
            self.assertTrue(r["text"]["gives"], r["id"])
        self.assertTrue(dt.roll_header(S + "institution_practice")["avoid_used"])
        self.assertEqual({k: r["conflicts_with"] for k, r in pr.items() if r.get("conflicts_with")},
                         {"practice_hold_the_remnant_gate": ["contest_sealed_remnant"],
                          "practice_guard_the_holy_place": ["contest_one_shrine"]}, "two clashes, no more")
        self.assertEqual({k: r["form"] for k, r in pr.items() if r.get("form")},
                         {"practice_players": "form_travelling", "practice_free_company": "form_company",
                          "practice_smugglers_union": "form_society", "practice_foreign_house": "form_house"})
        forms = {r["id"]: r for r in rows("institution_form")}
        for k, r in pr.items():
            if r.get("form"):
                self.assertFalse(set(r["hints"]) - set(forms[r["form"]]["hints"]),
                                 f"{k}: the form it names stands under every archetype the practice fits")
        self.assertEqual(sorted(pr["practice_free_company"]["hints"]), ["martial"])
        self.assertEqual(sorted(pr["practice_smugglers_union"]["hints"]), ["criminal"])

    def test_the_practice_weights_and_texts(self):
        pr = {r["id"]: r for r in rows("institution_practice")}
        dragons = {"life_dragon_protection", "contest_humans_dragon", "ruin_age_of_dragons", "ruin_giants_and_dragons", "break_dragons_rule"}
        want = {"practice_pilots": {"break_maps_are_illegal"}, "practice_border_riders": {"break_border_forbidden"},
                "practice_sell_the_remnant": {"break_ruins_forbidden"}, "practice_hold_the_remnant_gate": {"break_ruins_forbidden"},
                "practice_champions": {"break_war_is_ritual"}, "practice_pilgrim_guides": {"life_pilgrim_road"},
                "practice_worship_the_break": {"scar_new_belief"}, "practice_seek_the_lost": {"scar_lost_knowledge"},
                "practice_dragon_hunters": dragons}
        for rid, others in want.items():
            self.assertEqual(weights(pr[rid]), {o: 3 for o in others}, rid)
        self.assertEqual(weights(pr["practice_enchanted_goods"]), {"break_magic_sold": 2})
        self.assertEqual(pr["practice_enchanted_goods"]["requires"], {"dial": {"magic": ["medium", "high"]}})
        self.assertEqual({k for k, r in pr.items() if r.get("weight_by")}, set(want) | {"practice_enchanted_goods"})
        self.assertEqual(pr["practice_champions"]["text"]["name"], "they are champions who settle disputes by single combat")
        self.assertEqual(pr["practice_monopoly"]["text"]["name"], "they hold the monopoly of one good")
        self.assertNotIn("royal", pr["practice_monopoly"]["label"].lower())
        self.assertEqual(pr["practice_study_the_remnant"]["text"]["gives"], "excavation tasks, the deciphering of old knowledge")
        self.assertEqual(pr["practice_keep_the_old_works"]["text"]["name"], "they repair the remnant's works and keep them running")
        self.assertEqual(pr["practice_couriers"]["text"]["gives"], "news, urgent errands that must arrive in time")
        self.assertEqual((pr["practice_dragon_hunters"]["text"]["name"], pr["practice_dragon_hunters"]["text"]["gives"]),
                         ("they hunt dragons", "the great hunt, the dragon's hoard"))

    def test_signs_and_powers(self):
        signs = {r["id"]: r for r in rows("institution_sign")}
        self.assertEqual(len(signs), 13)
        self.assertEqual(signs["isign_own_language"]["requires"], {"dial": {"scale": ["standard", "epic"]}},
                         "their own language needs a third language: never at short (review #10)")
        self.assertEqual([k for k, r in signs.items() if set(r) & {"requires", "weight_by", "conflicts_with", "hints"}],
                         ["isign_own_language"], "the signs are rolled freely")
        powers = {r["id"]: r for r in rows("institution_power")}
        self.assertEqual(len(powers), 10)
        self.assertTrue(all(r["p4"] for r in powers.values()))
        self.assertEqual({k: sorted(r["hints"]) for k, r in powers.items()}, {k: sorted(v.split()) for k, v in {
            "power_monopoly": "trade guild state", "power_place": "state martial religious scholarly",
            "power_knowledge": "scholarly criminal guild trade resistance", "power_arms": "martial state criminal resistance",
            "power_love": "resistance religious guild", "power_sanctity": "religious", "power_treasure": "trade guild state criminal",
            "power_creature_bond": "martial religious scholarly resistance", "power_privilege": "guild trade scholarly martial",
            "power_fear": "criminal martial state"}.items()})
        self.assertEqual(powers["power_privilege"]["text"]["name"], "privilege: a right granted by the rulers")


class Phenomenon(unittest.TestCase):

    def test_rules_forty_in_eight_families(self):
        rules = rows("phenomenon_rule")
        self.assertEqual(len(rules), 40)
        fams = Counter(r["family"] for r in rules)
        self.assertEqual(set(fams), set(FOUNDATION["phenomenon_rule_families"]))
        self.assertTrue(all(v == 5 for v in fams.values()))
        self.assertTrue(dt.roll_header(S + "phenomenon_rule")["avoid_used"])

    def test_every_ruin_source_reaches_rules(self):
        """Review #6: the rule pool is filtered to the ruin's olgu_families; it is never empty."""
        rules = rows("phenomenon_rule")
        for ruin in dt.rows("foundation.yaml#ruin_source"):
            pool = [r for r in rules if r["family"] in ruin["olgu_families"]]
            self.assertGreaterEqual(len(pool), 5, ruin["id"])

    def test_low_magic_halves_three_families(self):
        low, high = arb.Context(dials={"magic": "low"}), arb.Context(dials={"magic": "high"})
        for r in rows("phenomenon_rule"):
            ratio = arb.weight_of(r, low) / arb.weight_of(r, high)
            self.assertEqual(ratio, 0.5 if r["family"] in ("magic_behaviour", "word_sign", "born_of_break") else 1, r["id"])

    def test_every_rule_carries_its_kind(self):
        """Whoever casts uses a spell rule, no one a rule that happens by itself; the user is rolled for the usable
        six alone (item 10)."""
        rules = {r["id"]: r for r in rows("phenomenon_rule")}
        self.assertEqual(Counter(r["kind"] for r in rules.values()), {"spell": 15, "usable": 6, "self": 19})
        self.assertEqual({k for k, r in rules.items() if r["kind"] == "usable"},
                         {"rule_mirror_doors", "rule_true_names", "rule_signs_are_spells", "rule_tongue_of_magic", "rule_metal_wakes",
                          "rule_shared_wounds"})
        self.assertEqual({k for k, r in rules.items() if r["kind"] == "spell"},
                         {"rule_echo", "rule_rebound", "rule_inverted_element", "rule_spells_grow_life", "rule_spell_twins",
                          "rule_kin_doubles", "rule_spell_marks", "rule_delayed_spells", "rule_casting_ages", "rule_gesture_magic",
                          "rule_monsters_smell_magic", "rule_one_way_magic", "rule_spells_feed_the_break", "rule_geography_of_power",
                          "rule_half_spells"})
        self.assertEqual({k: r["users"] for k, r in rules.items() if r.get("users")},
                         {"rule_tongue_of_magic": ["user_the_people"], "rule_shared_wounds": ["user_the_people", "user_the_institution"]})
        self.assertTrue(all(r["kind"] == "usable" for r in rules.values() if r.get("users")))

    def test_four_rules_carry_a_rule(self):
        rules = {r["id"]: r for r in rows("phenomenon_rule")}
        self.assertEqual({k: r["conflicts_with"] for k, r in rules.items() if r.get("conflicts_with")},
                         {"rule_beasts_sense_lies": ["break_no_direct_lies"]})
        eras = {r["id"][len("era_"):] for r in dt.rows("dials.yaml#era")}
        below = {"rule_night_distances", "rule_seasons_bound_to_a_beast", "rule_feelings_make_weather"}
        for k in below:
            self.assertEqual(set(rules[k]["requires"]["dial"]["era"]), eras - {"underground"}, f"{k}: every era but underground")
            self.assertFalse(arb.holds(rules[k]["requires"], arb.Context(dials={"era": "underground"})))
            self.assertTrue(arb.holds(rules[k]["requires"], arb.Context(dials={"era": "nautical"})))
        gated = {k for k, r in rules.items() if r.get("requires") and not r.get("after_the_break")}
        self.assertEqual(gated, below)

    def test_the_rule_and_limit_weights(self):
        rules = {r["id"]: r for r in rows("phenomenon_rule")}
        self.assertEqual({k: weights(r) for k, r in rules.items() if weights(r)},
                         {"rule_echo": {"break_casting_forbidden": 2}, "rule_tongue_of_magic": {"break_no_common_tongue": 2}})
        limits = {r["id"]: r for r in rows("phenomenon_limit")}
        self.assertEqual({k: weights(r) for k, r in limits.items() if r.get("weight_by")}, {"limit_iron_cuts": {"break_iron_is_sacred": 2}})

    def test_signs_limits_users(self):
        self.assertEqual(len(rows("phenomenon_sign")), 16)
        self.assertEqual(len(rows("phenomenon_limit")), 8)
        self.assertEqual(len(rows("phenomenon_user")), 8)
        for sub in ("phenomenon_sign", "phenomenon_user"):
            for r in rows(sub):
                self.assertFalse(set(r) & {"weight_by", "conflicts_with", "hints", "claims"}, f"{r['id']}: no tags")


class Rules(unittest.TestCase):

    def every(self):
        doc = dt.load("signatures.yaml")
        for sub in doc["tables"]:
            yield from rows(sub)

    def test_the_eleven_sub_tables(self):
        self.assertEqual(set(dt.load("signatures.yaml")["tables"]), set(NEW), "the old three went with build item 10")

    def test_the_removed_ids_are_gone(self):
        """Nothing in the committed data names a row the tag review removed or renamed."""
        for path in sorted(dt.tables_dir().iterdir()):
            if path.suffix not in (".yaml", ".json", ".md"):
                continue
            text = path.read_text(encoding="utf-8")
            for rid in REMOVED:
                self.assertNotRegex(text, rf"\b{rid}\b", f"{path.name} still names {rid}")

    def test_every_named_row_exists(self):
        """A weight, a requirement, a clash, a `users` or a `form` field names only real rows."""
        ids = {r["id"] for name in dt.list_tables() for lst in dt.all_row_lists(dt.load(name)).values() for r in lst}

        def named(cond):
            if isinstance(cond, list):
                for c in cond:
                    yield from named(c)
            elif isinstance(cond, dict):
                for key in ("any_of", "all_of", "none_of"):
                    yield from cond.get(key) or []
                for key in ("all", "any"):
                    yield from named(cond.get(key) or [])

        users = {r["id"] for r in rows("phenomenon_user")}
        forms = {r["id"] for r in rows("institution_form")}
        for r in self.every():
            refs = set(r.get("conflicts_with") or []) | set(named(r.get("requires")))
            for w in r.get("weight_by") or []:
                refs |= set(named(w.get("when")))
            self.assertFalse({x for x in refs if not x.startswith(dt.CLAIM)} - ids, f"{r['id']} names a row that does not exist")
            self.assertFalse(set(r.get("users") or []) - users, r["id"])
            if r.get("form"):
                self.assertIn(r["form"], forms, r["id"])

    def test_no_signature_row_carries_a_claim(self):
        """A trait tells one people's own order, never the land's; the same holds for the institution and the
        phenomenon (docs/p1-tags.md)."""
        for r in self.every():
            self.assertFalse(r.get("claims") or r.get("overrides"), r["id"])

    def test_the_stamps_cover_the_eleven_sub_tables(self):
        covered = dt.reviewed_rows()
        for sub in NEW:
            self.assertIn(S + sub, dt.REVIEWED_TABLES)
            for r in rows(sub):
                self.assertEqual(covered.get(r["id"]), dt.row_hash(r), r["id"])

    def test_design_compare_reads_the_same_usage(self):
        for sub in NEW:
            self.assertEqual(design_compare.is_unique_table(S + sub), sub in ("people_trait", "institution_practice", "phenomenon_rule"), sub)

    def test_a_break_that_is_still_coming_bars_the_since_the_break_rows(self):
        for r in self.every():
            if r.get("after_the_break"):
                req = r["requires"]
                for c in (req if isinstance(req, list) else [req]):
                    self.assertIn("time_coming", c.get("none_of") or [], r["id"])
                self.assertFalse(arb.holds(req, arb.Context(dials={"magic": "high", "era": "underground"},
                                                            rolled={"time_coming": False, "land_underground": False})))

    def test_clean_phrases_no_attractor_no_magic_for_sale(self):
        for r in self.every():
            for t in phrases(r):
                with self.subTest(row=r["id"]):
                    self.assertNotIn("(", t)
                    self.assertIsNone(ATTRACTORS.search(t), t)

    def test_the_usage_the_owner_set(self):
        """A trait, a practice, a rule another campaign drew is not drawn again; the rest may repeat."""
        unique = {"people_trait", "institution_practice", "phenomenon_rule"}
        for sub in dt.load("signatures.yaml")["tables"]:
            self.assertEqual(bool(dt.roll_header(S + sub).get("avoid_used")), sub in unique, sub)


if __name__ == "__main__":
    unittest.main()
