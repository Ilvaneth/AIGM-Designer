"""
test_foundation_tables.py — P1's foundation tables (plan item 25; docs/p1-foundation-rows.md): the owner-approved
counts and families, the columns every seed carries, the links between the sub-tables (the spine's forced kinds,
the ruin source's sites, phenomenon families and palette additions), the magic gates, the waits the arbiter reads,
and no attractor cluster in any row.
"""

import re
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_tables as dt  # noqa: E402

DOC = dt.load("foundation.yaml")
PALETTE = {r["id"]: r for r in dt.rows("foundation.yaml#palette")}
SPINE = dt.rows("foundation.yaml#spine")
RUIN = dt.rows("foundation.yaml#ruin_source")
BIOMES = {r["id"] for r in dt.rows("regions.yaml#biome")}
SITE_TYPES = {r["id"] for r in dt.rows("sites.yaml#site_type")}
LIFE = dt.rows("foundation.yaml#lifeline")
CONTEST = dt.rows("foundation.yaml#contest")
ARCHETYPES = {r["id"][len("archetype_"):] for r in dt.rows("factions.yaml#archetype")}

# the attractor clusters item 25 keeps out of every foundation table: a table decision, not a word ban (#18)
ATTRACTORS = re.compile(r"\b(mum|balmumu|lamba|fener|kandil|don yağı|çan(?!ak)|sessiz|defter|geçiş ücreti|haraç|"
                        r"mahkeme|yargı|gelgit|tuz(?!ak)|ölülerin hak)", re.IGNORECASE)


def texts(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from texts(v)
    elif isinstance(node, list):
        for v in node:
            yield from texts(v)


class Palette(unittest.TestCase):

    def test_fourteen_ordinary_and_eight_fantastic_kinds(self):
        fantastic = [r for r in PALETTE.values() if r.get("fantastic")]
        self.assertEqual(len(PALETTE), 22)
        self.assertEqual(len(fantastic), 8)

    def test_biomes_heights_and_waters(self):
        for r in PALETTE.values():
            with self.subTest(kind=r["id"]):
                self.assertTrue(r["text"]["name"])
                self.assertFalse(set(r.get("biomes") or []) - BIOMES)
                self.assertFalse(set(r.get("implies") or []) - set(PALETTE))
                if not r.get("fantastic"):
                    self.assertTrue(r.get("biomes"), "an ordinary kind lives in the existing biomes")
        self.assertEqual({k for k, r in PALETTE.items() if r.get("height")}, {"land_mountain", "land_highland", "land_volcanic"})
        self.assertEqual({k for k, r in PALETTE.items() if r.get("water") and not r.get("fantastic")},
                         {"land_river", "land_lake", "land_coast"})

    def test_the_magic_gate(self):
        """Low admits only the thin place; the cap per magic value is in the roll header."""
        for r in PALETTE.values():
            if r.get("fantastic") and not r.get("thin_place"):
                self.assertEqual(r.get("requires"), {"dial": {"magic": ["medium", "high"]}}, r["id"])
        self.assertEqual(DOC["tables"]["palette"]["roll"]["fantastic_cap_by_magic"], {"low": 0, "medium": 1, "high": 2})
        self.assertEqual(DOC["tables"]["palette"]["roll"]["count_by_scale"],
                         {"short": [4, 5], "standard": [6, 8], "epic": [9, 12]})

    def test_the_thin_place_never_counts_toward_the_cap(self):
        """Owner review of item 3: 'low: only the thin place' — it is a plane's touch, drawable at every magic level
        and outside the fantastic cap."""
        thin = PALETTE["land_thin_place"]
        self.assertTrue(thin.get("cap_exempt"))
        self.assertEqual([k for k, r in PALETTE.items() if r.get("cap_exempt")], ["land_thin_place"])
        res = arb.arbitrate("foundation.yaml#palette", list(PALETTE.values()), arb.Context(dials={"magic": "low"}))
        drawable_fantastic = [r["id"] for r in res["pool"] if r.get("fantastic")]
        self.assertEqual(drawable_fantastic, ["land_thin_place"])

    def test_underground_is_forced_and_the_unreadable_kinds_weigh_half(self):
        """Owner, 2026-09-28: 'underground: the surface is rare'."""
        self.assertEqual(DOC["tables"]["palette"]["roll"]["forces_by_dial"],
                         {"era": {"underground": ["land_underground"], "nautical": ["land_coast"]}})
        half = {"land_plain", "land_steppe", "land_forest", "land_marsh", "land_desert", "land_cold", "land_coast",
                "land_island", "land_highland", "land_floating_isles", "land_sky_river", "land_crystal_forest",
                "land_stone_sea", "land_glass_desert", "land_giant_bones"}
        ug = arb.Context(dials={"era": "underground"})
        other = arb.Context(dials={"era": "medieval"})
        for k, r in PALETTE.items():
            with self.subTest(kind=k):
                ratio = arb.weight_of(r, ug) / arb.weight_of(r, other)
                self.assertEqual(ratio, 0.5 if k in half else (3 if k == "land_underground" else 1))

    def test_palettes_are_never_excluded_across_campaigns(self):
        head = dt.roll_header("foundation.yaml#palette")
        self.assertFalse(head.get("avoid_used") or head.get("family_wait") or head.get("row_wait"))
        self.assertFalse(dt.records_usage("foundation.yaml#palette"))


class Spine(unittest.TestCase):

    def test_thirty_in_six_families_of_five(self):
        self.assertEqual(len(SPINE), 30)
        self.assertEqual(Counter(r["family"] for r in SPINE),
                         {f: 5 for f in ("line", "centred", "fragmented", "layered", "frontier", "fantastic")})

    def test_every_spine_carries_its_columns(self):
        for r in SPINE:
            with self.subTest(spine=r["id"]):
                tr = r["text"]
                for col in ("name", "heart", "key_place", "travel"):
                    self.assertTrue(tr.get(col))
                self.assertTrue(len(tr.get("ends") or []) == 2 or tr.get("ends_both"), "two ends, or one phrase for both")
                self.assertIn(r["key_kind"], DOC["key_kinds"])

    def test_forced_kinds_are_palette_kinds_and_their_magic_holds(self):
        magic_of = {"high": {"high"}, "medium": {"medium", "high"}}
        for r in SPINE:
            forced = list(r.get("forces") or []) + list(r.get("forces_one_of") or [])
            with self.subTest(spine=r["id"]):
                self.assertFalse(set(forced) - set(PALETTE))
                for k in forced:
                    need = set(((PALETTE[k].get("requires") or {}).get("dial") or {}).get("magic") or [])
                    if need:
                        mine = set(((r.get("requires") or {}).get("dial") or {}).get("magic") or ["low", "medium", "high"])
                        self.assertTrue(mine <= need, f"{r['id']} forces {k} but may roll at magic {mine - need}")

    def test_the_owner_rules_on_the_fantastic_spines(self):
        by = {r["id"]: r for r in SPINE}
        for sid in ("spine_titan_back", "spine_floating_archipelago"):
            self.assertEqual(by[sid]["requires"], {"dial": {"magic": ["high"]}})
        for sid in ("spine_void_ring", "spine_giant_tree", "spine_world_edge", "spine_two_worlds"):
            self.assertEqual(by[sid]["requires"], {"dial": {"magic": ["medium", "high"]}})
        self.assertIn("land_thin_place", by["spine_two_worlds"]["forces"])
        self.assertNotIn("forces", by["spine_star_crater"], "the crater is a P3 landmark, not a palette kind")

    def test_the_spines_unreadable_underground_weigh_a_quarter(self):
        quarter = {"spine_river_to_sea", "spine_mountain_passes", "spine_long_coast", "spine_barren_corridor",
                   "spine_oasis_ring", "spine_archipelago", "spine_forest_clearings", "spine_mesa_land", "spine_terraces",
                   "spine_above_below_sea", "spine_peninsula", "spine_strait_two_continents", "spine_long_wall",
                   "spine_climate_belt", "spine_edge_of_civilisation", "spine_titan_back", "spine_floating_archipelago",
                   "spine_giant_tree", "spine_world_edge"}
        heavy = {"spine_great_rift", "spine_valley_maze", "spine_lake_chain", "spine_three_depths", "spine_mountain_within"}
        ug = arb.Context(dials={"era": "underground"})
        other = arb.Context(dials={"era": "medieval"})
        for r in SPINE:
            with self.subTest(spine=r["id"]):
                ratio = arb.weight_of(r, ug) / arb.weight_of(r, other)
                self.assertEqual(ratio, 0.25 if r["id"] in quarter else (3 if r["id"] in heavy else 1))

    def test_the_merge_rules_name_real_ruins(self):
        """Owner, 2026-09-28: one crater, and the rift is the two worlds' crossing point (applied at step 1)."""
        ruins = {r["id"] for r in RUIN}
        merges = {r["id"]: set(r["merges_with"]) for r in SPINE if r.get("merges_with")}
        self.assertEqual(merges, {"spine_star_crater": {"ruin_fallen_star", "ruin_celestial_war"},
                                  "spine_two_worlds": {"ruin_planar_rift"}})
        for m in merges.values():
            self.assertFalse(m - ruins)

    def test_every_spine_names_its_parts(self):
        """Build item 6b: each part's preferred kinds; the crossroads has four ends; the key place's kinds stand on
        its key kind; every forced kind is some part's preference."""
        lands = DOC["key_kind_lands"]
        self.assertFalse(set(lands) - set(DOC["key_kinds"]))
        for r in SPINE:
            with self.subTest(spine=r["id"]):
                parts = r["parts"]
                want = {"heart", "end_a", "end_b", "key_place"} | ({"end_c", "end_d"} if r["id"] == "spine_crossroads" else set())
                self.assertEqual(set(parts), want)
                for kinds in parts.values():
                    self.assertFalse(set(kinds) - set(PALETTE))
                if r["key_kind"] in lands:
                    self.assertFalse(set(parts["key_place"]) - set(lands[r["key_kind"]]))
                preferred = set().union(*(set(v) for v in parts.values()))
                for k in list(r.get("forces") or []) + list(r.get("forces_one_of") or []):
                    self.assertIn(k, preferred, f"{r['id']} forces {k} but no part wants it")

    def test_the_family_waits_three_births(self):
        head = dt.roll_header("foundation.yaml#spine")
        self.assertTrue(head["avoid_used"])
        self.assertEqual(head["family_wait"], 3)


class RuinSource(unittest.TestCase):

    def test_fifty_three_in_eight_families(self):
        """Forty of the foundation's first build, five to a family, and the thirteen of the general themes (16b)."""
        self.assertEqual(len(RUIN), 53)
        self.assertEqual(Counter(r["family"] for r in RUIN),
                         {"fallen_kingdoms": 7, "wars": 7, "gods": 5, "magic": 7, "catastrophe": 6, "toil": 5, "old_peoples": 8, "planes": 8})

    def test_every_ruin_carries_its_columns(self):
        for r in RUIN:
            with self.subTest(ruin=r["id"]):
                for col in ("name", "what", "remnant", "sites", "strangeness"):
                    self.assertTrue(r["text"].get(col))
                self.assertIn(r["remnant_kind"], DOC["remnant_kinds"])
                self.assertTrue(r["sites"])
                self.assertFalse(set(r["sites"]) - SITE_TYPES)

    def test_the_phenomenon_families_fit_the_strangeness(self):
        """Item 25 review #6: 2-3 rule families per ruin, never family 8 (born of the break: only with the scar)."""
        families = set(DOC["phenomenon_rule_families"]) - {"born_of_break"}
        seen = Counter()
        for r in RUIN:
            with self.subTest(ruin=r["id"]):
                fams = r["olgu_families"]
                self.assertTrue(2 <= len(fams) <= 3 or r["id"] == "ruin_broken_time" and len(fams) >= 2)
                self.assertFalse(set(fams) - families)
                seen.update(fams)
        for f in families:
            self.assertGreaterEqual(seen[f], 3, f"rule family {f} is reachable from at least three ruins")

    def test_the_palette_additions(self):
        """The rows file: mage war → glass desert, dead god → giant's bones, flood → drowned lands, city states →
        dead-city lands; the fallen star and the fallen sky city bring P3 landmarks (review #4)."""
        by = {r["id"]: r for r in RUIN}
        self.assertEqual(by["ruin_mage_war"]["adds_palette"], "land_glass_desert")
        self.assertEqual(by["ruin_dead_god"]["adds_palette"], "land_giant_bones")
        self.assertEqual(by["ruin_great_flood"]["adds_biome"], "biome_drowned_lands")
        self.assertEqual(by["ruin_city_states"]["adds_biome"], "biome_dead_city_lands")
        self.assertEqual(by["ruin_fallen_star"]["landmark"], "crater")
        self.assertEqual(by["ruin_fallen_sky_city"]["landmark"], "floating_fragments")
        for r in RUIN:
            if r.get("adds_palette"):
                self.assertTrue(PALETTE[r["adds_palette"]].get("fantastic"))
            if r.get("adds_biome"):
                self.assertIn(r["adds_biome"], BIOMES)

    def test_giants_and_dragons_fit_the_inverted_element(self):
        """Owner review of item 3: 'fire burns otherwise near the bones' is closest to the inverted-element rule."""
        by = {r["id"]: r for r in RUIN}
        self.assertEqual(by["ruin_giants_and_dragons"]["olgu_families"], ["magic_behaviour", "matter"])

    def test_the_tombs_are_the_khans_and_the_undying_kings(self):
        self.assertEqual([r["id"] for r in RUIN if "site_dungeon_tomb" in r["sites"]], ["ruin_steppe_union", "ruin_kingdom_of_the_dead"])

    def test_the_family_waits_three_births(self):
        head = dt.roll_header("foundation.yaml#ruin_source")
        self.assertTrue(head["avoid_used"])
        self.assertEqual(head["family_wait"], 3)


class Lifeline(unittest.TestCase):

    def test_sixty_one_in_seven_families(self):
        self.assertEqual(len(LIFE), 61)
        self.assertEqual(Counter(r["family"] for r in LIFE),
                         {"water": 8, "passage": 9, "creatures": 9, "mine": 9, "crop": 9, "craft": 9, "treaty": 8})

    def test_every_lifeline_carries_its_columns(self):
        for r in LIFE:
            with self.subTest(life=r["id"]):
                for col in ("name", "who", "yields", "weak_point"):
                    self.assertTrue(r["text"].get(col))
                self.assertEqual(bool(r["text"].get("sense")), r["family"] != "treaty", "only the treaties have no sense line")

    def test_only_rows_the_palette_can_hold_are_drawn(self):
        """The rows file: the script draws only lifelines whose `where` kinds the palette brought; 'everywhere' rows
        need none."""
        for r in LIFE:
            with self.subTest(life=r["id"]):
                where = r.get("where") or []
                self.assertFalse(set(where) - set(PALETTE))
                req = r.get("requires")
                if not where:
                    self.assertTrue(req is None or set(req) == {"dial"}, "an everywhere row needs no land; a dial gate may stand")
                    continue
                conds = req if isinstance(req, list) else [req]
                for c in conds:
                    self.assertTrue(set(c.get("any_of") or c.get("all_of") or []) == set(where))

    def test_the_magic_gates(self):
        by = {r["id"]: r for r in LIFE}
        gi = by["life_giant_insects"]["requires"]
        self.assertEqual([c["dial"] for c in gi], [{"magic": ["medium", "high"]}, {"era": ["underground"]}])
        self.assertEqual(by["life_griffon_eyries"]["requires"][0]["dial"], {"magic": ["medium", "high"]})

    def test_the_family_waits_three_births(self):
        self.assertEqual(dt.roll_header("foundation.yaml#lifeline")["family_wait"], 3)


class Contest(unittest.TestCase):

    def test_fifty_one_in_eight_families(self):
        """Forty of the foundation's first build, five to a family, and the eleven of the general themes (16b)."""
        self.assertEqual(len(CONTEST), 51)
        self.assertEqual(Counter(r["family"] for r in CONTEST),
                         {"two_hands": 6, "old_new": 5, "strong_weak": 9, "open_close": 6, "race": 6, "kin": 5, "nonhuman": 8, "hidden_hand": 6})

    def test_every_contest_carries_its_roles_prize_and_escalation(self):
        for r in CONTEST:
            with self.subTest(contest=r["id"]):
                self.assertEqual(set(r["roles"]), {"a", "b", "third", "fourth"})
                for role in r["roles"].values():
                    self.assertTrue(role["text"])
                    self.assertTrue(role["hint"] is None or role["hint"] in ARCHETYPES, role)
                self.assertIn(r["prize"], ("lifeline", "heart", "remnant", "new", "thin_place"))
                self.assertGreaterEqual(len(r["escalation"]), 2)
                for k, v in (r.get("seats") or {}).items():
                    self.assertIn(k, ("a", "b", "third", "fourth", "prize"))
                    self.assertIn(v, ("heart", "end", "key_place", "beside_key_place", "thin_place"))

    def test_roles_by_scale_and_the_epic_second_contest(self):
        head = DOC["tables"]["contest"]["roll"]
        self.assertEqual(head["roles_by_scale"], {"short": ["a", "b", "third"], "standard": ["a", "b", "third", "fourth"],
                                                  "epic": ["a", "b", "third", "fourth"]})
        self.assertEqual(head["contests_by_scale"], {"short": 1, "standard": 1, "epic": 2})
        self.assertEqual(head["family_wait"], 3)

    def test_the_owner_rules(self):
        by = {r["id"]: r for r in CONTEST}
        self.assertEqual(by["contest_open_close_gate"]["requires"], {"any_of": ["land_thin_place"]})
        self.assertTrue(all(r.get("third_is_rumour") for r in CONTEST if r["family"] == "hidden_hand"))
        self.assertFalse(any(r.get("third_is_rumour") for r in CONTEST if r["family"] != "hidden_hand"))
        for r in CONTEST:
            flat = " ".join(texts(r))
            self.assertNotRegex(flat, r"kötü tarikat|fısıldayan|doğuştan kötü", r["id"])

    def test_every_role_hint_is_a_faction_archetype_the_institution_can_take(self):
        """Review #5: the institution is drawn only from a hinted role; every contest has one inside the scale's role
        count, short included (owner, 2026-09-28: the shapeshifter's village or family sides are state, the hunter martial)."""
        roles = DOC["tables"]["contest"]["roll"]["roles_by_scale"]
        for scale, keys in roles.items():
            for r in CONTEST:
                with self.subTest(scale=scale, contest=r["id"]):
                    self.assertTrue(any(r["roles"][k]["hint"] for k in keys))

    def test_the_thin_place_prize_needs_the_thin_place(self):
        for r in CONTEST:
            if r["prize"] == "thin_place":
                self.assertEqual(r.get("requires"), {"any_of": ["land_thin_place"]}, r["id"])
        self.assertEqual({r["id"] for r in CONTEST if r["prize"] == "thin_place"}, {"contest_open_close_gate"})

    def test_the_treaty_lifelines_weigh_their_contests_double(self):
        """Owner, 2026-09-28: a weight bond, no forcing."""
        by = {r["id"]: r for r in CONTEST}
        for cid, life in (("contest_humans_giants", "life_giant_peace"), ("contest_humans_dragon", "life_dragon_protection"),
                          ("contest_humans_fey", "life_fey_bargain")):
            base = arb.weight_of(by[cid], arb.Context())
            self.assertEqual(arb.weight_of(by[cid], arb.Context(rolled={life: False})), base * 2)


ACTIONS = dt.rows("foundation.yaml#action")
SCARS = dt.rows("foundation.yaml#scar")
PIECES = ("lifeline", "remnant", "key_place", "heart", "role", "thin_place")


class Break(unittest.TestCase):

    def test_six_targets_the_thin_place_only_with_the_palette(self):
        targets = {r["piece"]: r for r in dt.rows("foundation.yaml#break_target")}
        self.assertEqual(set(targets), set(PIECES))
        self.assertEqual(targets["thin_place"]["requires"], {"any_of": ["land_thin_place"]})

    def test_twenty_one_actions_each_with_three_forms(self):
        """Item 25 step 1 #7: every action carries its past, present and imminent form; a missing one is caught."""
        self.assertEqual(len(ACTIONS), 21)
        for r in ACTIONS:
            with self.subTest(action=r["id"]):
                self.assertEqual(set(r["forms"]), {"past", "present", "imminent"})
                for f in r["forms"].values():
                    self.assertTrue(f.strip())
                    self.assertFalse(f[0].isupper(), "a predicate the sentence places after the target")
                self.assertTrue(set(r["targets"]) <= set(PIECES))

    def test_the_compatibility_tables(self):
        """Review #8: per lifeline family, remnant kind and key-place kind; each listed exactly when the action can
        strike that piece, and every value from its closed list."""
        closed = {"lifeline": {r["family"] for r in LIFE}, "remnant": set(DOC["remnant_kinds"]), "key_place": set(DOC["key_kinds"])}
        for r in ACTIONS:
            with self.subTest(action=r["id"]):
                fits = r["fits"]
                self.assertEqual(set(fits), {t for t in r["targets"] if t in closed})
                for piece, values in fits.items():
                    self.assertTrue(values)
                    self.assertFalse(set(values) - closed[piece])
                self.assertTrue(set(r.get("destroys") or []) <= set(r["targets"]))
        for piece, values in closed.items():
            reach = set().union(*(set(r["fits"].get(piece) or []) for r in ACTIONS))
            self.assertEqual(reach, values, f"every {piece} kind can be struck by some action")

    def test_no_table_row_carries_an_example(self):
        """Owner, 2026-09-28: examples anchor births; they stay in docs/p1-foundation-rows.md only."""
        for sub, rows in dt.all_row_lists(DOC).items():
            for r in rows:
                self.assertFalse({k for k in r if "example" in k}, r["id"])

    def test_the_owner_rules_on_the_actions(self):
        by = {r["id"]: r for r in ACTIONS}
        self.assertIn("treaty", by["act_corrupted"]["fits"]["lifeline"])
        self.assertTrue(by["act_rose"]["winner_is_target_role"])
        self.assertEqual(by["act_closed"]["bars_scars_on_target"], {"thin_place": ["scar_plane_thinned"]})
        self.assertEqual({r["id"] for r in ACTIONS if r.get("concretise")}, {"act_fell_from_sky", "act_gave_birth"})
        self.assertEqual({r["id"] for r in ACTIONS if r.get("leaves_ruins")},
                         {"act_sank", "act_burned", "act_fell_from_sky", "act_corrupted"})
        for r in dt.rows("foundation.yaml#time"):
            self.assertEqual(set(r["text"]), {"name", "name_note"}, "the lead phrases went with the Turkish sentence (build item 13a)")
        for r in ACTIONS:
            self.assertEqual(set(r["forms"]), {"past", "present", "imminent"}, r["id"])
            self.assertTrue(r["forms"]["present"].startswith(("is ", "are ")) and r["forms"]["imminent"].startswith("is about to "), r["id"])

    def test_actions_and_scars_are_grammar(self):
        """A used verb or scar waits three births; they are never exhausted."""
        for ref in ("foundation.yaml#action", "foundation.yaml#scar"):
            head = dt.roll_header(ref)
            self.assertEqual(head.get("row_wait"), 3)
            self.assertFalse(head.get("avoid_used") or head.get("family_wait"))

    def test_eighteen_scars_each_a_column(self):
        self.assertEqual(len(SCARS), 18)
        self.assertEqual(DOC["tables"]["scar"]["roll"]["count_by_scale"], {"short": 1, "standard": 2, "epic": 3})
        for r in SCARS:
            with self.subTest(scar=r["id"]):
                self.assertTrue(r["floors"])
                self.assertEqual({h["phase"] for h in r["hooks"]}, set(r["floors"]))
                self.assertNotRegex(r["text"]["name"], r"\bdead\b|\bdeath\b", "the dead returning is left out on purpose")
        new_land = next(r for r in SCARS if r["id"] == "scar_new_land_kind")
        self.assertTrue(new_land["needs_fantastic_room"])

    def test_four_times_with_their_tense(self):
        times = {r["id"]: r["tense"] for r in dt.rows("foundation.yaml#time")}
        self.assertEqual(times, {"time_just_now": "past", "time_generation_ago": "past", "time_unfolding": "present",
                                 "time_coming": "imminent"})

    def test_the_escalation_is_the_four_tiers_of_play(self):
        tiers = dt.rows("foundation.yaml#escalation_tier")
        self.assertEqual([t["levels"] for t in tiers], [[1, 4], [5, 10], [11, 16], [17, 20]])


def sentence_texts(node, key=""):
    """Every string the rendering may place: the `text` values, minus the notes (`*_note`, `text_note`)."""
    if isinstance(node, str):
        yield key, node
    elif isinstance(node, dict):
        for k, v in node.items():
            if not str(k).endswith("_note"):
                yield from sentence_texts(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from sentence_texts(v, key)


class CleanPhrases(unittest.TestCase):
    """Owner, 2026-09-28: a design note never enters the foundation's rendering; it lives beside the phrase."""

    def test_no_parenthesis_in_any_phrase_a_template_places(self):
        for sub, rows in dt.all_row_lists(DOC).items():
            for r in rows:
                phrases = list(sentence_texts(r.get("text")))
                for role in (r.get("roles") or {}).values():
                    phrases.append(("text", role["text"]))
                phrases += [("form", f) for f in (r.get("forms") or {}).values()]
                for key, t in phrases:
                    with self.subTest(row=r["id"], field=key):
                        self.assertNotIn("(", t)
                        self.assertNotIn(")", t)

    def test_the_notes_are_kept_beside_their_phrase(self):
        by = {r["id"]: r for r in LIFE}
        self.assertEqual(by["life_giant_peace"]["text"], {"name": "peace with the giants",
                                                         "name_note": "the giants on the mountain, the humans on the plain",
                                                         "who": "border envoys", "yields": "safety, barter",
                                                         "weak_point": "if the word is broken"})
        scars = {r["id"]: r for r in dt.rows("foundation.yaml#scar")}
        self.assertEqual(scars["scar_time_flow_changed"]["text"]["name"], "the flow of time changed in a region")
        sea = next(r for r in CONTEST if r["id"] == "contest_land_sea_folk")["roles"]["b"]
        self.assertEqual(sea["text"], "the sea folk")
        self.assertNotIn("triton", sea["text_note"].lower(), "tritons are not in SRD 5.1")
        self.assertEqual(next(r for r in SPINE if r["id"] == "spine_star_crater")["text"]["ends"][0], "the changed inside of the crater")

    def test_no_ruin_repeats_the_templates_time(self):
        """The rendering's label says "The past"; a ruin's `what` never says when again."""
        for r in RUIN:
            self.assertNotRegex(r["text"]["what"], r"(?i)\blong ago\b|\bonce upon\b|\bin the old days\b|\bformerly\b", r["id"])


class TagReview(unittest.TestCase):
    """Build item 7c-2 (docs/p1-build-7c.md): the foundation rows as the tag review left them."""

    def test_the_claims(self):
        by = {r["id"]: r for r in CONTEST}
        want = {"contest_two_heirs": {"nobility": "exists", "rule": "hereditary"}, "contest_empty_throne": {"nobility": "exists", "rule": "hereditary"},
                "contest_sibling_rulers": {"rule": "hereditary"}, "contest_old_order_reform": {"nobility": "exists"},
                "contest_capital_marches": {"nobility": "exists"}, "contest_lords_peasants": {"nobility": "exists"},
                "contest_treasure_race": {"rule": "throne"}, "contest_first_settlers": {"rule": "throne"},
                "contest_humans_giants": {"rule": "throne"}, "contest_war_fed_company": {"war": "by_armies"}}
        self.assertEqual({k: r["claims"] for k, r in by.items() if r.get("claims")}, want)
        roles = {(k, key): role["claims"] for k, r in by.items() for key, role in r["roles"].items() if role.get("claims")}
        self.assertEqual(roles, {("contest_occupier_resistance", "third"): {"nobility": "exists"},
                                 ("contest_humans_fey", "fourth"): {"nobility": "exists"}})
        self.assertEqual({r["id"]: r["claims"] for r in LIFE if r.get("claims")},
                         {"life_binding_marriage": {"nobility": "exists", "rule": "hereditary"}})
        self.assertEqual({r["id"]: r["claims"] for r in RUIN if r.get("claims")}, {"ruin_age_of_mages": {"magic": "faded"}})

    def test_the_prize_and_the_lifeline(self):
        by = {r["id"]: r for r in CONTEST}
        craft = [r["id"] for r in LIFE if r["family"] == "craft"]
        passage = [r["id"] for r in LIFE if r["family"] == "passage"]
        for cid in ("contest_old_new_craft", "contest_share_keep_knowledge", "contest_split_family"):
            self.assertEqual(by[cid]["requires"], {"any_of": craft})
        self.assertEqual(by["contest_open_close_road"]["requires"], {"any_of": passage + ["life_pilgrim_road"]})
        self.assertEqual(by["contest_one_harbour"]["requires"]["all"][0], {"any_of": ["land_coast"]}, "the palette requirement stays")
        for cid in ("contest_one_harbour", "contest_one_pasture", "contest_two_banks", "contest_mine_owners_miners"):
            palette, lifes = by[cid]["requires"]["all"]
            self.assertTrue(all(x.startswith("land_") for x in palette["any_of"]))
            self.assertIn({"when": {"any_of": lifes["any_of"]}, "x": 3}, by[cid]["weight_by"], "as likely as before inside its heading")
        self.assertIsNone(by["contest_one_shrine"].get("requires"))
        gods = [r["id"] for r in RUIN if r["family"] == "gods"]
        self.assertIn({"when": {"any_of": gods}, "x": 2}, by["contest_one_shrine"]["weight_by"])

    def test_the_peoples_roles_and_the_other_contest_changes(self):
        by = {r["id"]: r for r in CONTEST}
        people = {(k, key): role for k, r in by.items() for key, role in r["roles"].items() if role.get("people_role")}
        self.assertEqual(len(people), 11, "ten of the tag review and the slavers' fourth (16b)")
        self.assertEqual({k: v.get("lineage_forced") for k, v in people.items() if v.get("lineage_forced")},
                         {("contest_humans_giants", "b"): "lineage_giant_kin", ("contest_humans_fey", "b"): "lineage_fey",
                          ("contest_land_sea_folk", "b"): "lineage_merfolk"})
        weigh = {"lineage_dwarf": 3, "lineage_gnome": 3, "lineage_goblinoid": 3}
        self.assertEqual({k: v["lineage_weight"] for k, v in people.items() if v.get("lineage_weight")},
                         {("contest_surface_deep", "b"): weigh, ("contest_mine_owners_miners", "fourth"): weigh})
        self.assertEqual(by["contest_two_branches"]["roles"]["a"]["text"], "the branch that counts the old collapse a punishment")
        self.assertEqual(by["contest_two_branches"]["roles"]["b"]["text"], "the branch that counts it an opportunity")
        self.assertEqual([o["default"] for o in by["contest_casters_casterless"]["overrides"]], ["regulator_identity", "regulator_strictness"])

    def test_the_break_rows(self):
        times = {r["id"]: r for r in dt.rows("foundation.yaml#time")}
        self.assertEqual(times["time_coming"]["conflicts_with"], ["scar_new_people", "scar_magic_rule_changed"])
        surface = {"dial": {"era": ["medieval", "renaissance", "ancient", "nautical"]}}
        scars = {r["id"]: r for r in SCARS}
        acts = {r["id"]: r for r in ACTIONS}
        for row in (scars["scar_sky_changed"], scars["scar_seasons_broken"], acts["act_fell_from_sky"]):
            self.assertEqual(row["requires"], surface, row["id"])
        generic = ("carry this scar", "the identity takes this scar")
        for r in SCARS:
            for h in r["hooks"]:
                self.assertFalse(any(g in h["must"] for g in generic), (r["id"], h["must"]))
        self.assertEqual(scars["scar_new_taboo"]["floors"], ["P1", "P3"])
        plane = "this row's plane is chosen among the touched planes; the planes the foundation names are shared to fit the scale's count"
        ruins = {r["id"]: r for r in RUIN}
        for row in (ruins["ruin_planar_rift"], ruins["ruin_planar_invasion"], ruins["ruin_celestial_war"], ruins["ruin_elven_withdrawal"],
                    acts["act_merged_with_plane"], scars["scar_plane_thinned"]):
            self.assertTrue(any(plane in h["must"] and h["phase"] == "P2" for h in row["hooks"]), row["id"])
        self.assertEqual(PALETTE["land_glass_desert"]["text"]["what"], "a desert whose sand has turned to glass")
        self.assertEqual(PALETTE["land_giant_bones"]["text"]["what"], "land settled on and inside a giant skeleton")
        common = [h["must"] for h in DOC["tables"]["palette"]["hooks_common"]]
        self.assertIn("the origin of every fantastic kind the ruin source did not bring is written", common)


class Attractors(unittest.TestCase):

    def test_no_attractor_cluster_in_any_row(self):
        for sub, rows in dt.all_row_lists(DOC).items():
            for r in rows:
                for t in texts({k: v for k, v in r.items() if k not in ("id", "label", "hooks")}):
                    with self.subTest(row=r["id"]):
                        self.assertIsNone(ATTRACTORS.search(t), t)


if __name__ == "__main__":
    unittest.main()
