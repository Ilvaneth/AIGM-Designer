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
                self.assertTrue(r["tr"]["name"])
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
        self.assertEqual(DOC["tables"]["palette"]["roll"]["forces_by_dial"], {"era": {"underground": ["land_underground"]}})
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
                tr = r["tr"]
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

    def test_the_family_waits_three_births(self):
        head = dt.roll_header("foundation.yaml#spine")
        self.assertTrue(head["avoid_used"])
        self.assertEqual(head["family_wait"], 3)


class RuinSource(unittest.TestCase):

    def test_forty_in_eight_families_of_five(self):
        self.assertEqual(len(RUIN), 40)
        self.assertEqual(Counter(r["family"] for r in RUIN),
                         {f: 5 for f in ("fallen_kingdoms", "wars", "gods", "magic", "catastrophe", "toil",
                                         "old_peoples", "planes")})

    def test_every_ruin_carries_its_columns(self):
        for r in RUIN:
            with self.subTest(ruin=r["id"]):
                for col in ("name", "what", "remnant", "sites", "strangeness"):
                    self.assertTrue(r["tr"].get(col))
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

    def test_the_only_tomb_is_the_khans(self):
        self.assertEqual([r["id"] for r in RUIN if "site_dungeon_tomb" in r["sites"]], ["ruin_steppe_union"])

    def test_the_family_waits_three_births(self):
        head = dt.roll_header("foundation.yaml#ruin_source")
        self.assertTrue(head["avoid_used"])
        self.assertEqual(head["family_wait"], 3)


class Attractors(unittest.TestCase):

    def test_no_attractor_cluster_in_any_row(self):
        for sub, rows in dt.all_row_lists(DOC).items():
            for r in rows:
                for t in texts(r.get("tr")):
                    with self.subTest(row=r["id"]):
                        self.assertIsNone(ATTRACTORS.search(t), t)


if __name__ == "__main__":
    unittest.main()
