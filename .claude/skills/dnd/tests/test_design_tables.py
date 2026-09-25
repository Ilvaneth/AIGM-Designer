"""
test_design_tables.py — the designer's tables (plan item 17, 22.1): every data/design/*.yaml
parses with the header the README states; every row has id / label / hooks; ids are unique across
all tables; hooks name known phases; scale.yaml carries the plan's numbers; the size floors of
risk 24.1 #18 hold; naming.yaml produces English names (errata 24.2 #17) and bans exact names
only (#18); forbidden.yaml's lexical patterns compile; design_manifest's closed lists derive from
dials.yaml; rubrics.yaml, once it exists, covers every generative phase.
"""

import re
import sys
import unittest
from pathlib import Path

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_tables as dt  # noqa: E402
from paths import data_dir  # noqa: E402

TABLES = dt.tables_dir()
TURKISH = re.compile(r"[çğışöüÇĞİŞÖÜ]")

# the tables item 17 lists, by batch; the test only demands the ones that exist, but the README's
# convention applies to every file, and this list is what the last batch must complete
PLANNED = {
    "dials", "scale", "tensions", "secrets", "trope-breaks", "forbidden", "signatures", "naming",
    "pantheon", "planes", "magic", "history", "calendar", "regions", "settlements", "factions",
    "antagonists", "simulation", "npcs", "monster-ecology", "loot-budget", "sites", "arc", "threads",
    "rubrics",
}


def every_row():
    for name in dt.list_tables():
        for sub, rows in dt.all_row_lists(dt.load(name)).items():
            for r in rows:
                yield name, sub, r


class Convention(unittest.TestCase):

    def test_tables_dir_has_only_planned_files(self):
        names = {n[:-5] for n in dt.list_tables()}
        self.assertTrue(names, "no tables yet")
        self.assertFalse(names - PLANNED, f"unplanned tables: {names - PLANNED}")

    def test_every_table_has_the_header(self):
        for name in dt.list_tables():
            doc = dt.load(name)
            with self.subTest(table=name):
                self.assertEqual(doc.get("schema_version"), 1)
                self.assertEqual(doc.get("table"), name[:-5])
                consumed = doc.get("consumed_by")
                self.assertIsInstance(consumed, list)
                self.assertTrue(consumed)
                self.assertFalse(set(consumed) - set(dt.HOOK_TARGETS), consumed)
                self.assertIn("plan", doc)
                self.assertTrue(dt.all_row_lists(doc), "a table needs rows or tables.*.rows")

    def test_every_row_has_id_label_hooks(self):
        seen = 0
        for name, sub, r in every_row():
            seen += 1
            with self.subTest(table=name, sub=sub, row=r.get("id")):
                self.assertRegex(r["id"], r"^[a-z][a-z0-9_]*$")
                self.assertIsInstance(r.get("label"), str)
                self.assertTrue(r["label"].strip())
                hooks = r.get("hooks")
                self.assertIsInstance(hooks, list, "hooks must be a list")
                self.assertTrue(hooks, "a row needs at least one hook")
                for h in hooks:
                    self.assertIn(h.get("phase"), dt.HOOK_TARGETS, h)
                    self.assertTrue(str(h.get("must", "")).strip(), h)
                if "weight" in r:
                    self.assertGreater(float(r["weight"]), 0)
        self.assertGreater(seen, 100)

    def test_ids_unique_across_all_tables(self):
        ids = {}
        for name, sub, r in every_row():
            self.assertNotIn(r["id"], ids, f"{r['id']} in {name}#{sub} and {ids.get(r['id'])}")
            ids[r["id"]] = f"{name}#{sub}"

    def test_hooks_common_name_known_phases(self):
        for name in dt.list_tables():
            for h in dt.load(name).get("hooks_common") or []:
                self.assertIn(h.get("phase"), dt.HOOK_TARGETS, (name, h))
                self.assertTrue(h.get("must"))

    def test_subtable_addressing(self):
        self.assertEqual(len(dt.rows("dials.yaml#content_mix")), 5)
        self.assertEqual([r["value"] for r in dt.rows("dials.yaml#scale")], ["short", "standard", "epic"])
        self.assertGreaterEqual(len(dt.rows("naming.yaml#family")), 8)
        self.assertEqual(dt.rows("no-such-table.yaml"), [])
        with self.assertRaises(KeyError):
            dt.rows("dials.yaml#no_such_subtable")
        self.assertEqual(dt.row("tensions.yaml", "tension_power_self")["poles"], ["power", "self"])

    def test_cross_references_resolve_where_the_table_exists(self):
        """A row that names another table's row id (bias lists, conflicts, allowed_via) must name a real one."""
        ids = {r["id"] for _, _, r in every_row()}
        present = {n[:-5] for n in dt.list_tables()}
        for name, sub, r in every_row():
            refs = []
            for key in ("conflicts_with", "allowed_via"):
                refs += r.get(key) or []
            for key in ("secret_archetype_bias", "pantheon_type_bias", "era_bias"):
                refs += (r.get("effects") or {}).get(key) or []
            refs += r.get("touch_bias") or []
            refs += (r.get("overrides") or {}).get("pantheon_type_bias") or []
            if (r.get("overrides") or {}).get("pantheon_type"):
                refs.append(r["overrides"]["pantheon_type"])
            for ref in refs:
                table = ref.split("_", 1)[0]
                prefix_table = {"secret": "secrets", "break": "trope-breaks", "tension": "tensions",
                                "forbidden": "forbidden", "era": "dials", "pantheon": "pantheon",
                                "sig": "signatures", "mix": "dials", "tone": "dials"}.get(table)
                if prefix_table in present:
                    with self.subTest(table=name, row=r["id"], ref=ref):
                        self.assertIn(ref, ids)


class PlanNumbers(unittest.TestCase):

    def test_dials_closed_lists_match_item_2(self):
        self.assertEqual(dt.dial_values("scale"), ("short", "standard", "epic"))
        self.assertEqual(dt.dial_values("tone"), ("grimdark", "dark fantasy", "heroic", "horror", "political",
                                                  "swashbuckling", "cosmic"))
        self.assertEqual(dt.dial_values("magic"), ("none", "low", "medium", "high"))
        self.assertEqual(dt.dial_values("era"), ("medieval", "renaissance", "ancient", "nautical", "underground"))
        self.assertEqual(dt.dial_values("danger"), ("lethal", "gritty", "standard", "heroic"))
        self.assertEqual(dt.dial_values("content_mix"), ("exploration", "politics", "war", "horror", "mystery"))

    def test_design_manifest_derives_its_lists_from_the_tables(self):
        import design_manifest as dm
        self.assertEqual(dm.DIALS["tone"], dt.dial_values("tone"))
        self.assertEqual(dm.ARC_SHAPE, {"short": (1, 3, 4), "standard": (3, 7, 11), "epic": (3, 10, 19)})

    def test_danger_touches_only_non_cr_knobs(self):
        """Errata 24.2 #8: a danger row may not carry a tier, a CR or a level."""
        for r in dt.rows("dials.yaml#danger"):
            keys = set(r["effects"])
            self.assertFalse({"danger_tier", "cr", "level", "tier"} & keys, keys)
            self.assertLessEqual(r["effects"]["over_tier_sites_act1"], 3)
            self.assertGreaterEqual(r["effects"]["over_tier_sites_act1"], 2)

    def test_scale_matches_item_2(self):
        s, m, e = (dt.scale_row(x) for x in ("short", "standard", "epic"))
        self.assertEqual((s["level_span"], m["level_span"], e["level_span"]), (4, 11, 19))
        self.assertEqual((s["target_sessions"], m["target_sessions"], e["target_sessions"]), ([8, 12], [20, 30], [40, 60]))
        self.assertEqual((s["acts"], m["acts"], e["acts"]), (1, 3, 3))
        self.assertEqual((s["chapters"]["min"], s["chapters"]["max"]), (3, 3))
        self.assertEqual((m["chapters"]["min"], m["chapters"]["max"]), (6, 8))
        self.assertEqual((e["chapters"]["min"], e["chapters"]["max"]), (9, 12))
        self.assertEqual((s["beats"], m["beats"], e["beats"]), (3, 6, 6))
        self.assertEqual((s["polities"], m["polities"], e["polities"]), (1, [2, 3], [3, 5]))
        self.assertEqual((s["regions"], m["regions"], e["regions"]), ([1, 2], [4, 6], [8, 12]))
        self.assertEqual((s["factions"]["count"], m["factions"]["count"], e["factions"]["count"]), ([3, 4], [6, 10], [12, 16]))
        self.assertEqual((s["named_npcs"], m["named_npcs"], e["named_npcs"]), ([14, 18], [30, 40], [60, 80]))
        self.assertEqual((s["sites"]["count"], m["sites"]["count"], e["sites"]["count"]), ([6, 8], [15, 25], [30, 40]))
        self.assertEqual((s["sites"]["detailed_at_birth"], m["sites"]["detailed_at_birth"], e["sites"]["detailed_at_birth"]), (2, 3, [3, 4]))
        self.assertEqual((s["gods"], m["gods"], e["gods"]), ([3, 5], [6, 9], [9, 14]))
        self.assertEqual((s["planes_touched"][0], m["planes_touched"][0], e["planes_touched"][0]), (0, 1, 3))
        self.assertEqual((s["quest_seeds"], m["quest_seeds"], e["quest_seeds"][0]), ([6, 8], [15, 20], 30))
        self.assertEqual((s["antagonists"]["lieutenants"], m["antagonists"]["lieutenants"], e["antagonists"]["lieutenants"]), (1, [2, 3], [3, 4]))
        self.assertEqual((s["sockets_per_pc"], m["sockets_per_pc"], e["sockets_per_pc"]), (2, 3, 3))
        self.assertEqual((s["trope_breaks"], m["trope_breaks"], e["trope_breaks"]), (1, 2, 2))
        self.assertEqual((s["signature_mechanic_chance"], m["signature_mechanic_chance"], e["signature_mechanic_chance"]), (0, 50, 100))
        self.assertEqual((s["churches_as_factions"], e["churches_as_factions"]), (False, True))

    def test_scale_site_roles_and_npc_tiers_add_up(self):
        """Item 9.5's role split fits the site band; item 8.2's rescaled tiers fit the NPC cap."""
        for r in dt.rows("scale.yaml"):
            with self.subTest(scale=r["value"]):
                roles = r["sites"]["roles"]
                lo, hi = dt.band(r["sites"]["count"])
                self.assertTrue(lo <= sum(roles.values()) <= hi, (roles, lo, hi))
                tiers = r["npc_tiers"]
                nlo, nhi = dt.band(r["named_npcs"])
                mlo, mhi = dt.band(tiers["minor"])
                self.assertEqual(tiers["major"] + tiers["supporting"] + mlo, nlo)
                self.assertEqual(tiers["major"] + tiers["supporting"] + mhi, nhi)
                bbeg_and_lts = 1 + dt.band(r["antagonists"]["lieutenants"])[1]
                self.assertLessEqual(bbeg_and_lts, tiers["major"])
        shared = dt.scale_shared()
        self.assertEqual(shared["room_bands"], {"minor": [5, 10], "standard": [11, 19], "major": [20, 25], "capstone": [30, 30]})
        self.assertEqual(shared["xp"]["intended_path_share"], 0.7)
        self.assertEqual(shared["thread_imbalance_max"], 0.35)
        self.assertEqual(shared["demographic_drift_max"], 0.65)
        self.assertGreaterEqual(len(shared["stacking_rules"]), 5)
        for r in dt.rows("scale.yaml"):
            self.assertEqual(r["volatility"]["control_flips_per_week"], 1)


class Floors(unittest.TestCase):
    """Risk 24.1 #18: tiny felt-identity tables repeat by campaign three to five."""

    def test_tensions_at_least_30(self):
        self.assertGreaterEqual(len(dt.rows("tensions.yaml")), 30)
        for r in dt.rows("tensions.yaml"):
            self.assertEqual(len(r["poles"]), 2, r["id"])
            self.assertGreaterEqual(len(r["question_seeds"]), 2, r["id"])
            self.assertIn(r["villain_answer"]["pole"], r["poles"], r["id"])
            self.assertIn(r["world_default"]["pole"], r["poles"], r["id"])
            self.assertNotEqual(r["villain_answer"]["pole"], r["world_default"]["pole"], r["id"])

    def test_secrets_floor_and_shape(self):
        self.assertGreaterEqual(len(dt.rows("secrets.yaml#archetype")), 20)
        self.assertGreaterEqual(len(dt.rows("secrets.yaml#twist")), 8)
        self.assertGreaterEqual(len(dt.rows("secrets.yaml#trail")), 4)
        self.assertTrue(dt.load("secrets.yaml")["roll"]["secret"])
        for r in dt.rows("secrets.yaml#archetype"):
            self.assertEqual(set(r["clue_shape"]), {"act1", "act2", "act3"}, r["id"])
            self.assertTrue(set(r["villain_relation"]) <= {"knows", "is", "serves", "hunts", "denies"}, r["id"])

    def test_trope_breaks_at_least_40_and_touch_two_phases(self):
        breaks = dt.rows("trope-breaks.yaml")
        self.assertGreaterEqual(len(breaks), 40)
        for r in breaks:
            phases = {h["phase"] for h in r["hooks"]}
            self.assertGreaterEqual(len(phases), 2, r["id"])
            self.assertTrue(r.get("statement"))

    def test_signatures_at_least_15_per_type(self):
        for sub in ("phenomenon", "people", "institution"):
            rows = dt.rows(f"signatures.yaml#{sub}")
            self.assertGreaterEqual(len(rows), 15, sub)
            for r in rows:
                self.assertTrue(r.get("seed"), r["id"])
                self.assertGreaterEqual(len(r.get("mutations") or []), 2, r["id"])
        for r in dt.rows("signatures.yaml#people"):
            self.assertTrue(r.get("srd_reskin"), r["id"])

    # --- batch B: cosmos -------------------------------------------------------

    def test_pantheon_types_presence_and_the_srd_domains(self):
        self.assertEqual([r["id"] for r in dt.rows("pantheon.yaml#type")],
                         ["pantheon_polytheist", "pantheon_dualist", "pantheon_dead_gods", "pantheon_silent_gods",
                          "pantheon_ancestor_gods"])
        self.assertGreaterEqual(len(dt.rows("pantheon.yaml#presence")), 5)
        domains = [r["label"] for r in dt.rows("pantheon.yaml#domain_scaffold")]
        self.assertEqual(domains, ["Knowledge", "Life", "Light", "Nature", "Tempest", "Trickery", "War", "Death"])
        self.assertEqual(dt.load("pantheon.yaml")["rules"]["domains"], domains)
        self.assertEqual([r["id"] for r in dt.rows("pantheon.yaml#rank")], ["rank_greater", "rank_lesser", "rank_power"])
        self.assertGreaterEqual(len(dt.rows("pantheon.yaml#church_archetype")), 8)
        self.assertGreaterEqual(len(dt.rows("pantheon.yaml#relationship")), 8)
        secrets = dt.rows("pantheon.yaml#god_secret")
        self.assertGreaterEqual(len(secrets), 8)
        for r in secrets:
            self.assertIn(r["tier"], ("discoverable", "secret"), r["id"])
        # every scaffold row points at real festival and god-secret rows
        fest = {r["id"] for r in dt.rows("calendar.yaml#festival_type")}
        god_secret_ids = {r["id"] for r in secrets}
        for r in dt.rows("pantheon.yaml#domain_scaffold"):
            self.assertIn(r["festival_kind"], fest, r["id"])
            self.assertTrue(set(r["secret_tendency"]) <= god_secret_ids, r["id"])
            self.assertTrue(r["alignments"] and r["symbol_kinds"] and r["church_shape"] and r["folk_ask_for"])

    def test_planes_baseline_is_the_srd_and_deviations_exist(self):
        base = dt.rows("planes.yaml#baseline")
        labels = {r["label"] for r in base}
        for name in ("The Material Plane", "The Ethereal Plane", "The Astral Plane", "The Elemental Chaos",
                     "The Nine Hells"):
            self.assertIn(name, labels)
        by_id = {r["id"]: r for r in base}
        self.assertIn("Elysium", by_id["baseline_elysium"]["srd"])   # the SRD name stays a note, never a label
        self.assertIn("Hades", by_id["baseline_hades"]["srd"])
        for r in base:
            self.assertIn(r["group"], ("material", "transitive", "inner", "outer", "demiplane"), r["id"])
            self.assertTrue(r["srd"], r["id"])
        # the sixteen Outer Planes by alignment (the SRD's rule), plus the neutral hub
        outer = [r for r in base if r["group"] == "outer"]
        self.assertEqual(len(outer), 17)
        self.assertEqual({r["alignment"] for r in outer},
                         {"LG", "LG/NG", "NG", "NG/CG", "CG", "CG/CN", "CN", "CN/CE", "CE", "CE/NE", "NE", "NE/LE",
                          "LE", "LE/LN", "LN", "LN/LG", "N"})
        for r in outer:
            self.assertIn(r["tier"], ("upper", "lower", "neutral"), r["id"])
            self.assertTrue(r["shape"], r["id"])
        # no Product Identity plane name in the labels (the SRD's legal notice); the SRD text's own three stay
        pi = ("celestia", "bytopia", "beastlands", "arborea", "ysgard", "limbo", "pandemonium", "abyss", "carceri",
              "gehenna", "acheron", "mechanus", "arcadia", "outlands", "sigil")
        for r in outer:
            self.assertFalse(any(p in r["label"].lower() for p in pi), r["label"])
        # no real-world mythology deities anywhere (errata 24.2 #19): the scaffold is gone and the names are banned
        self.assertNotIn("srd_deities", dt.load("pantheon.yaml").get("tables", {}))
        for r in base:
            self.assertNotIn("srd_deities", r, r["id"])

    def test_no_real_world_mythology_deity_names(self):
        """Errata 24.2 #19: the SRD's historical deities are blacklisted and appear in no table."""
        import yaml as _yaml
        srd = _yaml.safe_load((data_dir() / "srd-5.1-yaml" / "13-gods.yaml").read_text(encoding="utf-8"))
        app = srd["Appendix PH-B: Fantasy-Historical Pantheons"]
        srd_names = set()
        for title in ("The Celtic Pantheon", "The Greek Pantheon", "The Egyptian Pantheon", "The Norse Pantheon"):
            sub = [k for k in app[title] if k != "content"][0]
            for line in app[title][sub]["table"]["Deity"]:
                srd_names.add(re.sub(r"^The\s+", "", str(line).partition(", ")[0].strip()).lower())
        banned = {n.lower() for n in dt.load("naming.yaml")["blacklist"]["mythology"]}
        self.assertTrue(srd_names <= banned, srd_names - banned)
        self.assertIn("thor", banned)
        for name, sub, r in every_row():
            # a label is a phrase ("Set by the keeper"), so only a whole-label match counts; a `name` field
            # is a name, so its first word counts too
            self.assertNotIn(str(r.get("label", "")).lower(), banned, (name, sub, r["id"]))
            val = str(r.get("name", "")).lower()
            if val:
                self.assertNotIn(val, banned, (name, sub, r["id"]))
                self.assertNotIn(val.split()[0], banned, (name, sub, r["id"]))

    def test_magic_tables_and_the_wild_gate(self):
        for sub, floor in (("source", 10), ("constraint", 8), ("visibility", 5), ("taboo", 10), ("regulator", 8), ("wild", 6)):
            self.assertGreaterEqual(len(dt.rows(f"magic.yaml#{sub}")), floor, sub)
        self.assertEqual(dt.rows("magic.yaml#wild")[0]["id"], "wild_no")
        for r in dt.rows("dials.yaml#magic"):
            gate = r["effects"]["wild_magic_roll"]
            self.assertEqual(gate["notation"], "d6")
            self.assertTrue(set(gate["on"]) <= {1, 2, 3, 4, 5, 6}, r["id"])

    def test_history_tables(self):
        for sub, floor in (("age_template", 12), ("event_type", 14), ("divergence", 10), ("memory", 6)):
            self.assertGreaterEqual(len(dt.rows(f"history.yaml#{sub}")), floor, sub)
        for r in dt.rows("history.yaml#divergence"):
            self.assertIn(r["tier"], ("public", "discoverable", "secret"), r["id"])
        self.assertEqual(dt.rows("history.yaml#divergence")[0]["id"], "div_none")
        self.assertGreaterEqual(dt.rows("history.yaml#divergence")[0]["weight"], 3)

    def test_calendar_months_are_thirty_days_and_climates_have_seasons(self):
        doc = dt.load("calendar.yaml")
        self.assertEqual(doc["rules"]["month_length"], 30)
        self.assertIn("--month-length 30", doc["rules"]["init_call"])
        climates = dt.rows("calendar.yaml#climate")
        self.assertGreaterEqual(len(climates), 6)
        for c in climates:
            self.assertGreaterEqual(len(c["seasons"]), 2, c["id"])
            for s in c["seasons"]:
                self.assertEqual(set(s["tone"]), {"temperature", "sky", "smell", "sound"}, c["id"])
            self.assertTrue(c["hazards"], c["id"])
        for y in dt.rows("calendar.yaml#year_shape"):
            self.assertEqual(y["year_days"], y["months"] * 30 + y["intercalary_days"], y["id"])
        self.assertGreaterEqual(len(dt.rows("calendar.yaml#festival_type")), 14)
        domains = set(dt.load("pantheon.yaml")["rules"]["domains"])
        for f in dt.rows("calendar.yaml#festival_type"):
            self.assertTrue(set(f["domain_affinity"]) <= domains, f["id"])
        self.assertGreaterEqual(len(dt.rows("calendar.yaml#moon")), 6)
        self.assertGreaterEqual(len(dt.rows("calendar.yaml#week")), 3)
        self.assertGreaterEqual(len(dt.rows("calendar.yaml#start_anchor")), 5)

    # --- batch C: lands ---------------------------------------------------------

    def test_regions_tiers_travel_weights_and_biomes(self):
        doc = dt.load("regions.yaml")
        self.assertEqual(doc["rules"]["danger_tiers"], {"T1": [0, 2], "T2": [3, 6], "T3": [7, 11], "T4": [12, 16], "T5": [17, 30]})
        d12 = doc["rules"]["travel_table"]["d12"]
        self.assertEqual(list(d12), ["Quiet/Texture", "Social", "Environmental", "Combat", "Discovery", "Faction/Political"])
        self.assertEqual([hi - lo + 1 for lo, hi in d12.values()], [4, 1, 1, 1, 3, 2])
        self.assertEqual({r["scale"] for r in dt.rows("regions.yaml#tier_distribution")}, {"short", "standard", "epic"})
        climates = {r["id"] for r in dt.rows("calendar.yaml#climate")}
        identities = {r["id"] for r in dt.rows("regions.yaml#identity")}
        biomes = dt.rows("regions.yaml#biome")
        self.assertGreaterEqual(len(biomes), 20)
        for b in biomes:
            with self.subTest(biome=b["id"]):
                self.assertTrue(set(b["climates"]) <= climates, b["climates"])
                self.assertTrue(set(b["identity_seeds"]) <= identities, b["identity_seeds"])
                self.assertTrue(b["ecology_tags"] and b["terrain_tr"])
                self.assertEqual(set(b["site_type_bias"]), {"dungeon", "stronghold", "wilderness", "urban", "planar", "social"})
                for key in ("texture_seeds", "environmental_seeds", "discovery_seeds"):
                    self.assertGreaterEqual(len(b[key]), 3, key)
                self.assertGreaterEqual(len(b["landmark_seeds"]), 2)
        self.assertGreaterEqual(len(identities), 20)
        for r in dt.rows("regions.yaml#identity"):
            self.assertIn(r["sense"], ("sound", "sight", "smell", "time", "temperature"), r["id"])
        self.assertGreaterEqual(len(dt.rows("regions.yaml#landmark_kind")), 12)
        self.assertGreaterEqual(len(dt.rows("regions.yaml#social_seed")), 10)
        self.assertGreaterEqual(len(dt.rows("regions.yaml#faction_presence")), 8)

    def test_settlements_kinds_anchors_and_goods(self):
        kinds = {r["id"]: r for r in dt.rows("settlements.yaml#kind")}
        self.assertEqual(list(kinds), ["kind_village", "kind_town", "kind_city", "kind_metropolis"])
        self.assertEqual(kinds["kind_village"]["districts"], 0)
        self.assertEqual(kinds["kind_town"]["districts"], [2, 3])
        self.assertEqual(kinds["kind_city"]["districts"], [5, 8])
        self.assertEqual(kinds["kind_city"]["small_point_budget"], [30, 40])
        for k in ("temple", "guild_hall", "inn", "market", "seat", "signature"):
            self.assertIn(k, kinds["kind_town"]["anchors"])
        anchors = dt.rows("settlements.yaml#anchor_kind")
        anchor_ids = {a["id"] for a in anchors}
        for k in ("anchor_temple", "anchor_guild_hall", "anchor_inn", "anchor_market", "anchor_seat", "anchor_signature"):
            self.assertIn(k, anchor_ids)
        eras = {r["id"] for r in dt.rows("dials.yaml#era")} | {"era_any"}
        for a in anchors:
            self.assertTrue(a["services"], a["id"])
            if "era" in a:
                self.assertIn(a["era"], eras, a["id"])
        biomes = {r["id"] for r in dt.rows("regions.yaml#biome")}
        goods = dt.rows("settlements.yaml#economy_good")
        self.assertGreaterEqual(len(goods), 20)
        for g in goods:
            self.assertTrue(set(g["sources"]) <= biomes, (g["id"], g["sources"]))
            self.assertTrue(g["pairs_with_need"], g["id"])
        self.assertGreaterEqual(len(dt.rows("settlements.yaml#district_type")), 14)
        for d in dt.rows("settlements.yaml#district_type"):
            self.assertIn(d["law_modifier"], (-2, -1, 0, 1, 2), d["id"])
            self.assertTrue(d["character"] and d["fear_seed"], d["id"])
        self.assertGreaterEqual(len(dt.rows("settlements.yaml#fear")), 14)
        self.assertGreaterEqual(len(dt.rows("settlements.yaml#problem")), 14)
        self.assertGreaterEqual(len(dt.rows("settlements.yaml#small_point_kind")), 16)
        wealth = dt.rows("settlements.yaml#wealth")
        self.assertEqual([w["price_modifier"] for w in wealth], [0.8, 0.9, 1.0, 1.2, 1.5])
        self.assertEqual(len(dt.rows("settlements.yaml#law")), 5)

    # --- batch D: powers ---------------------------------------------------------

    def test_factions_archetypes_triggers_and_closed_lists(self):
        archetypes = dt.rows("factions.yaml#archetype")
        self.assertEqual([a["value"] for a in archetypes],
                         ["state", "religious", "guild", "criminal", "martial", "scholarly", "resistance", "cult", "trade"])
        endgames = {r["id"] for r in dt.rows("factions.yaml#endgame")}
        fractures = {r["id"] for r in dt.rows("factions.yaml#fracture")}
        for a in archetypes:
            with self.subTest(archetype=a["id"]):
                self.assertTrue(a["typical_forces"] and a["services"] and a["hq_kinds"])
                self.assertTrue(set(a["endgame_bias"]) <= endgames, a["endgame_bias"])
                self.assertTrue(set(a["fracture_bias"]) <= fractures, a["fracture_bias"])
                self.assertIn(a["doctrine_default"]["aggression"], (0, 1, 2, 3))
                self.assertIn(a["doctrine_default"]["target_preference"], dt.load("factions.yaml")["rules"]["target_preference"])
        self.assertEqual([t["value"] for t in dt.rows("factions.yaml#trigger")],
                         ["alliance", "loss", "gain", "exposure", "death", "betrayal"])
        moves = {m["value"] for m in dt.rows("simulation.yaml#move")}
        for t in dt.rows("factions.yaml#trigger"):
            self.assertTrue(set(t["weights_template"]) <= moves, (t["id"], t["weights_template"]))
        self.assertEqual({r["value"] for r in dt.rows("factions.yaml#step_kind")}, {"timed", "contested", "party-only"})
        self.assertEqual(dt.rows("factions.yaml#provocation_rung")[0]["parks"], False)
        self.assertEqual(dt.rows("factions.yaml#provocation_rung")[-1]["id"], "rung_war")
        for sub, floor in (("fracture", 12), ("endgame", 12), ("secret_kind", 8), ("cult_doctrine", 8), ("access_link", 6),
                           ("service", 10), ("abandon_if", 5)):
            self.assertGreaterEqual(len(dt.rows(f"factions.yaml#{sub}")), floor, sub)
        for r in dt.rows("factions.yaml#secret_kind"):
            self.assertIn(r["tier"], ("discoverable", "secret"), r["id"])

    def test_forbidden_structural_checks_point_at_real_closed_lists(self):
        """Every forbidden row's structural field names a table row set whose `value`s include the forbidden ones, flagged."""
        present = {n[:-5] for n in dt.list_tables()}
        checked = 0
        for r in dt.rows("forbidden.yaml"):
            table, _, sub = r["structural"]["table"].partition("#")
            if table[:-5] not in present:
                continue
            rows = dt.rows(f"{table}#{sub}")
            if not rows or "value" not in rows[0]:
                continue   # a field on rows (npcs.yaml#demographic alignment_fixed), not a closed list
            values = {x["value"]: x for x in rows}
            for v in r["structural"]["forbidden_values"]:
                with self.subTest(forbidden=r["id"], value=v):
                    self.assertIn(v, values)
                    self.assertTrue(values[v].get("forbidden"), f"{v} must be flagged forbidden in {table}#{sub}")
                    checked += 1
        self.assertGreaterEqual(checked, 8)

    def test_antagonists_visibility_fronts_dooms_and_stages(self):
        self.assertEqual(len(dt.rows("antagonists.yaml#visibility")), 5)
        self.assertTrue(dt.load("antagonists.yaml")["roll"]["secret"])
        shapes = dt.rows("antagonists.yaml#villain_shape")
        self.assertGreaterEqual(len([s for s in shapes if not s.get("forbidden")]), 10)
        origins = dt.rows("antagonists.yaml#origin")
        self.assertGreaterEqual(len([o for o in origins if not o.get("forbidden")]), 8)
        bfa = {r["value"]: r for r in dt.rows("antagonists.yaml#bbeg_faction_archetype")}
        self.assertEqual(set(bfa), {a["value"] for a in dt.rows("factions.yaml#archetype")})
        self.assertTrue(bfa["religious"]["forbidden"])
        ids = {r["id"] for _, _, r in every_row()}
        self.assertTrue(set(bfa["religious"]["allowed_via"]) <= ids)
        kinds = {r["value"] for r in dt.rows("factions.yaml#step_kind")}
        fronts = dt.rows("antagonists.yaml#front_template")
        self.assertGreaterEqual(len(fronts), 6)
        for f in fronts:
            with self.subTest(front=f["id"]):
                ats = [p["at"] for p in f["portents"]]
                self.assertTrue(4 <= len(ats) <= 6, ats)
                self.assertEqual(ats, sorted(ats))
                self.assertEqual(ats[-1], 1.0)
                self.assertTrue(all(0 < a <= 1 for a in ats))
                self.assertTrue({p["kind"] for p in f["portents"]} <= kinds)
                self.assertTrue(any(p["kind"] == "party-only" for p in f["portents"]), "a front telegraphs the party at least once")
        levers = {r["id"] for r in dt.rows("antagonists.yaml#buy_time_lever")}
        self.assertGreaterEqual(len(levers), 5)
        dooms = dt.rows("antagonists.yaml#doom_shape")
        self.assertGreaterEqual(len(dooms), 8)
        for d in dooms:
            self.assertTrue(set(d["levers"]) <= levers, d["id"])
            self.assertTrue(d["stage5"], d["id"])
        stages = dt.rows("antagonists.yaml#escalation_stage")
        self.assertEqual([s["stage"] for s in stages], [1, 2, 3, 4, 5])
        self.assertEqual([s["travel_tier"] for s in stages], ["early", "early", "late", "late", "late"])
        self.assertGreaterEqual(len(dt.rows("antagonists.yaml#lieutenant_role")), 8)
        for lt in dt.rows("antagonists.yaml#lieutenant_role"):
            self.assertEqual(lt["tier"], "major", lt["id"])

    def test_simulation_moves_outcomes_and_brakes(self):
        moves = dt.rows("simulation.yaml#move")
        self.assertEqual({m["value"] for m in moves},
                         {"seize", "sabotage", "bribe", "spy", "persuade", "assassinate", "besiege", "negotiate", "hold", "consolidate"})
        outcomes = {o["id"] for o in dt.rows("simulation.yaml#outcome")}
        for m in moves:
            with self.subTest(move=m["id"]):
                self.assertIn(m["on_success"], outcomes)
                self.assertIn(m["on_failure"], outcomes)
                self.assertIn(m["visibility"], ("public", "rumored", "secret"))
                self.assertGreaterEqual(m["cost"], 0)
                if m["big_outcome"]:
                    self.assertTrue(m["contested"], "a big outcome is always contested")
        self.assertEqual(next(m for m in moves if m["value"] == "hold")["cost"], 0)
        move_ids = {m["id"] for m in moves}
        for n in dt.rows("simulation.yaml#news_template"):
            self.assertTrue(set(n["kinds"]) <= move_ids, n["id"])
            self.assertIn(n["visibility"], ("public", "rumored", "secret"))
        shifts = {s["id"]: s for s in dt.rows("simulation.yaml#stance_shift")}
        self.assertEqual(shifts["shift_betrayal"]["delta"], -2)
        self.assertEqual(shifts["shift_alliance"]["delta"], 1)
        self.assertTrue(shifts["shift_betrayal"]["large"])
        delay = next(c for c in dt.rows("simulation.yaml#cascade") if c["id"] == "cascade_intel_delay")["delay_days"]
        self.assertEqual(sorted(delay), [0, 1, 2, 3])
        self.assertEqual(next(c for c in dt.rows("simulation.yaml#cascade") if c["id"] == "cascade_cap")["max_chain"], 3)
        self.assertGreaterEqual(len(dt.rows("simulation.yaml#succession")), 5)
        self.assertGreaterEqual(len(dt.rows("simulation.yaml#economy_modifier")), 6)
        for e in dt.rows("simulation.yaml#economy_modifier"):
            self.assertTrue(e["goods"] and e["duration_days"] > 0, e["id"])
        brakes = {b["id"]: b["action"] for b in dt.rows("simulation.yaml#brake")}
        self.assertEqual(brakes["brake_party_asset"], "park")
        self.assertEqual(brakes["brake_controller_party"], "skip")
        self.assertEqual(brakes["brake_load_bearing"], "cap")
        rules = dt.load("simulation.yaml")["rules"]
        for key in ("opposed_check", "load_bearing", "brakes", "volatility", "determinism", "big_outcomes"):
            self.assertIn(key, rules)

    # --- batch E: people and sites, the SRD index -----------------------------------

    def _index(self):
        import json
        path = TABLES / "srd-index-2014.json"
        self.assertTrue(path.is_file(), "run build_design_index.py")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_srd_index_is_current_and_complete(self):
        import subprocess
        proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "build_design_index.py"), "--check"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        idx = self._index()
        self.assertEqual(idx["_meta"]["ruleset"], "2014")
        self.assertIn("Open Game License", idx["_meta"]["ogl_notice"])
        self.assertNotIn("gods", idx, "errata 24.2 #19: the gods appendix is not indexed")
        self.assertEqual(len(idx["monsters"]), 334)
        self.assertEqual(len(idx["items"]), 362)
        self.assertEqual(len(idx["spells"]), 319)
        by_rarity = {k: len(v) for k, v in idx["items_by_rarity"].items()}
        self.assertEqual(by_rarity, {"Rare": 119, "Uncommon": 94, "Very Rare": 90, "Legendary": 43, "Varies": 11, "Common": 4, "Artifact": 1})
        self.assertEqual(sum(1 for i in idx["items"].values() if i["attunement"]), 176)
        self.assertEqual(sum(1 for m in idx["monsters"].values() if m["source"] == "npcs"), 20)
        self.assertGreaterEqual(sum(1 for m in idx["monsters"].values() if m["yaml_matched"]), 330)
        self.assertGreaterEqual(sum(1 for m in idx["monsters"].values() if m["has_legendary"]), 25)
        self.assertEqual(idx["monsters"]["adult-red-dragon"]["damage_immunities"], ["fire"])
        self.assertTrue(idx["monsters"]["adult-red-dragon"]["legendary_resistance"])
        self.assertTrue(idx["monsters"]["mage"]["spellcaster"])
        haz = idx["hazards"]
        self.assertEqual([t["name"] for t in haz["traps"]], ["Collapsing Roof", "Falling Net", "Fire-Breathing Statue", "Pits",
                                                              "Poison Darts", "Poison Needle", "Rolling Sphere", "Sphere of Annihilation"])
        self.assertEqual([d["name"] for d in haz["diseases"]], ["Cackle Fever", "Sewer Plague", "Sight Rot"])
        self.assertEqual(len(haz["poisons"]), 14)
        self.assertEqual(set(haz["madness"]), {"short", "long", "indefinite"})
        self.assertEqual(idx["backgrounds"], ["Acolyte"])
        self.assertEqual(len(idx["languages"]["standard"]), 8)
        self.assertEqual(len(idx["languages"]["exotic"]), 8)
        self.assertEqual(len(idx["trade_goods"]), 13)
        self.assertIn("Cleric", idx["spells_by_class_level"])
        for m in idx["monsters"].values():
            self.assertIsNotNone(m["ecology"], m["name"])

    def test_monster_ecology_covers_every_srd_monster(self):
        import build_design_index as b
        idx = self._index()
        rows = dt.rows("monster-ecology.yaml")
        self.assertEqual(len(rows), 334)
        self.assertEqual({r["srd"] for r in rows}, set(idx["monsters"]))
        doc = dt.load("monster-ecology.yaml")
        self.assertEqual(doc["habitat_vocabulary"], b.HABITATS)
        archetypes = {a["value"] for a in dt.rows("factions.yaml#archetype")}
        region_tags = set()
        for biome in dt.rows("regions.yaml#biome"):
            region_tags |= set(biome["ecology_tags"])
        self.assertTrue(region_tags <= set(b.HABITATS), region_tags - set(b.HABITATS))
        curated = 0
        for r in rows:
            with self.subTest(row=r["id"]):
                self.assertTrue(r["habitats"], "every monster lives somewhere")
                self.assertTrue(set(r["habitats"]) <= set(b.HABITATS), r["habitats"])
                self.assertIn(r["social_role"], b.SOCIAL_ROLES)
                self.assertTrue(set(r["faction_affinity"]) <= archetypes, r["faction_affinity"])
                self.assertNotIn("alignment_fixed", r)
                if r["people"]:
                    self.assertIn(idx["monsters"][r["srd"]]["type"], ("humanoid", "giant", "monstrosity", "fey"),
                                  "a people is a culture: humanoids, giants, the horned folk, the fey")
                curated += bool(r["curated"])
                if idx["monsters"][r["srd"]]["source"] == "npcs":
                    self.assertTrue(r["curated"], "the NPC appendix is fully curated: it is the factions' forces")
        self.assertGreaterEqual(curated, 50, "item 24.3: v0 with 50-80 curated rows")

    def test_loot_budget_tiers_match_and_filler_ban_names_real_items(self):
        idx = self._index()
        tiers = dt.rows("loot-budget.yaml#tier")
        site_tiers = dt.load("sites.yaml")["rules"]["danger_tiers"]
        self.assertEqual([t["tier"] for t in tiers], ["T1", "T2", "T3", "T4", "T5"])
        rarities = {"common", "uncommon", "rare", "very_rare", "legendary"}
        last_major = 0
        for t in tiers:
            with self.subTest(tier=t["tier"]):
                self.assertEqual(t["cr"], site_tiers[t["tier"]])
                self.assertEqual(set(t["items"]), rarities)
                self.assertEqual(list(t["gp"]), ["minor", "standard", "major", "capstone"])
                self.assertGreater(t["gp"]["major"][0], last_major)
                last_major = t["gp"]["major"][0]
                self.assertTrue(0 < t["consumable_share"] <= 1)
                self.assertTrue(set(t["boss_rarity"].values()) <= rarities)
        shares = [t["consumable_share"] for t in tiers]
        self.assertEqual(shares, sorted(shares, reverse=True))
        for row in dt.rows("loot-budget.yaml#filler_ban"):
            for sid in row["srd"]:
                self.assertIn(sid, idx["items"], sid)
        self.assertIn("gauntlets-of-ogre-power", dt.rows("loot-budget.yaml#filler_ban")[0]["srd"])

    def test_sites_bands_attitudes_and_hazard_map(self):
        idx = self._index()
        doc = dt.load("sites.yaml")
        self.assertEqual(doc["rules"]["danger_tiers"], dt.load("regions.yaml")["rules"]["danger_tiers"])
        bands = {r["value"]: r["rooms"] for r in dt.rows("sites.yaml#role_band")}
        self.assertEqual(bands, dt.scale_shared()["room_bands"])
        self.assertEqual({a["value"] for a in dt.rows("sites.yaml#attitude")}, {"kill", "capture", "enslave", "ignore", "negotiate", "test"})
        self.assertEqual({p["value"] for p in dt.rows("sites.yaml#payoff")}, {"treasure", "lore", "ally", "plot_item", "access"})
        self.assertEqual(len(dt.rows("sites.yaml#site_type")), 10)
        distances = {}
        for t in dt.rows("sites.yaml#telegraph"):
            distances[t["distance"]] = distances.get(t["distance"], 0) + 1
        self.assertEqual(set(distances), {"far", "near", "threshold"})
        self.assertTrue(all(n >= 3 for n in distances.values()), distances)
        cats = {r["value"]: r["band"] for r in dt.rows("sites.yaml#room_category")}
        self.assertEqual(cats, {"combat": [40, 60], "trap": [5, 15], "special": [10, 15], "structural": [15, 20]})
        trap_names = {t["name"] for t in idx["hazards"]["traps"]}
        disease_names = {d["name"] for d in idx["hazards"]["diseases"]}
        poison_names = {p["name"].replace("’", "'") for p in idx["hazards"]["poisons"]}
        for h in dt.rows("sites.yaml#hazard_by_tier"):
            with self.subTest(tier=h["tier"]):
                for t in h["traps"]:
                    base = t.split(" (")[0]
                    self.assertTrue(base in trap_names or base.startswith("a trap"), t)
                for d in h["diseases"]:
                    self.assertTrue(d in disease_names or d.startswith("a disease"), d)
                for p in h["poisons"]:
                    self.assertIn(p, poison_names, p)
        self.assertGreaterEqual(len(dt.rows("sites.yaml#boss_checklist")), 7)
        self.assertGreaterEqual(len(dt.rows("sites.yaml#escape")), 6)
        self.assertGreaterEqual(len(dt.rows("sites.yaml#never_visited")), 5)

    def test_npcs_roles_axes_secrets_demographics_and_anchors(self):
        idx = self._index()
        roles = {r["id"] for r in dt.rows("npcs.yaml#role")}
        for needed in ("role_faction_leader", "role_heir", "role_betrayal_candidate", "role_ruler", "role_anchor_owner", "role_bbeg",
                       "role_lieutenant", "role_regional_villain", "role_ordinary", "role_socket", "role_free_radical"):
            self.assertIn(needed, roles)
        weaknesses = {w["id"] for w in dt.rows("npcs.yaml#weakness")}
        axes = dt.rows("npcs.yaml#axis")
        self.assertEqual(len(axes), 4)
        for a in axes:
            self.assertEqual(set(a["weakness_from"]), set(a["poles"]), a["id"])
            self.assertTrue(set(a["weakness_from"].values()) <= weaknesses, a["id"])
        secrets = {s["id"] for s in dt.rows("npcs.yaml#secret")}
        for tone in dt.rows("dials.yaml#tone"):
            for bias in tone["effects"]["npc_secret_bias"]:
                self.assertIn(f"npcsecret_{bias}", secrets, (tone["id"], bias))
        for s in dt.rows("npcs.yaml#secret"):
            self.assertIn(s["tier"], ("discoverable", "secret"), s["id"])
            self.assertTrue(s["path"], s["id"])
        tics = dt.rows("npcs.yaml#speech_tic")
        self.assertGreaterEqual(len(tics), 20)
        self.assertEqual(len({t["label"] for t in tics}), len(tics))
        srd_races = {"human", "dwarf", "elf", "halfling", "dragonborn", "gnome", "half-elf", "half-orc", "tiefling"}
        for d in dt.rows("npcs.yaml#demographic"):
            with self.subTest(demo=d["id"]):
                self.assertIs(d["alignment_fixed"], False, "forbidden_inherently_evil_races")
                self.assertEqual(sum(d["species"].values()), 100)
                if d["id"] != "demo_signature_people":
                    self.assertTrue(set(d["species"]) <= srd_races, set(d["species"]) - srd_races)
                    self.assertLessEqual(max(d["species"].values()), 65, "item 8.4 drift cap inside one template")
        for sa in dt.rows("npcs.yaml#stat_anchor"):
            if sa["srd"]:
                self.assertIn(sa["srd"], idx["monsters"], sa["id"])
                self.assertEqual(idx["monsters"][sa["srd"]]["cr"], sa["cr"], sa["id"])
        self.assertEqual([a["value"] for a in dt.rows("npcs.yaml#attitude")], ["hostile", "unfriendly", "neutral", "friendly", "allied"])
        kinds = {r["value"] for r in dt.rows("npcs.yaml#relationship_kind")}
        self.assertTrue({"knows", "owes", "hates", "fears", "allied", "controls", "commands", "heir_of"} <= kinds)

    def test_forbidden_defaults_from_item_4_5_are_all_present(self):
        ids = {r["id"] for r in dt.rows("forbidden.yaml")}
        for needed in ("forbidden_awakening_ancient_evil", "forbidden_chosen_one", "forbidden_prophecy",
                       "forbidden_dark_lord_black_tower", "forbidden_generic_evil_cult",
                       "forbidden_corrupt_church_default_villain", "forbidden_amnesiac_hero",
                       "forbidden_tavern_opening", "forbidden_monolithic_empire", "forbidden_inherently_evil_races"):
            self.assertIn(needed, ids)


class ForbiddenDetection(unittest.TestCase):

    def test_every_row_has_a_structural_check_and_compiling_patterns(self):
        for r in dt.rows("forbidden.yaml"):
            with self.subTest(row=r["id"]):
                s = r["structural"]
                self.assertTrue(s["field"] and s["table"] and s["forbidden_values"])
                self.assertIn("#", s["table"])
                for lang in ("en", "tr"):
                    for pat in r["lexical"][lang]:
                        re.compile(pat, re.IGNORECASE)
                self.assertIsInstance(r.get("allowed_via"), list)

    def test_lexical_patterns_catch_the_cliche_and_not_the_fixture(self):
        pats = [re.compile(p, re.IGNORECASE) for r in dt.rows("forbidden.yaml") for p in r["lexical"]["en"]]
        self.assertTrue(any(p.search("an ancient evil awakens from its slumber") for p in pats))
        self.assertTrue(any(p.search("you all meet in a tavern") for p in pats))
        clean = "Lanternside'ın eski iskelesi üç yıl önce çöktü; Court of Mourners okumayı reddetti."
        self.assertFalse(any(p.search(clean) for p in pats))


class Naming(unittest.TestCase):

    def test_families_have_banks_and_english_samples(self):
        for r in dt.rows("naming.yaml#family"):
            with self.subTest(family=r["id"]):
                for bank in ("onsets", "nuclei", "codas"):
                    self.assertTrue(r[bank], bank)
                self.assertEqual(len(r["length"]), 2)
                self.assertLessEqual(r["length"][0], r["length"][1])
                self.assertIsInstance(r["forbidden_clusters"], list)
                self.assertTrue(r["tr_suffix_friendly"])
                for s in r["samples_person"] + r["samples_god"]:
                    self.assertIsNone(TURKISH.search(s), s)
                    self.assertRegex(s, r"^[A-Z][A-Za-z' -]*$", s)

    def test_lexicon_is_english_and_large_enough(self):
        doc = dt.load("naming.yaml")
        roots = doc["lexicon"]["roots"]
        self.assertGreaterEqual(len(roots), 60)
        self.assertEqual(len({r["root"] for r in roots}), len(roots), "duplicate root")
        for r in roots:
            self.assertRegex(r["root"], r"^[a-z]+$")
            self.assertIn(r["pos"], ("head", "tail", "either"))
            self.assertTrue(r["domains"])
        self.assertGreaterEqual(len(doc["lexicon"]["place_tails"]), 20)
        for kind in ("place", "institution", "people", "god_epithet", "ship", "month", "day"):
            self.assertTrue(doc["patterns"][kind], kind)
            for p in doc["patterns"][kind]:
                for ex in p["examples"]:
                    self.assertIsNone(TURKISH.search(ex), ex)

    def test_worn_roots_are_allowed_and_only_names_are_banned(self):
        """Errata 24.2 #18: crown, hollow, ember may recur as roots; bans are names and name-stems."""
        doc = dt.load("naming.yaml")
        roots = {r["root"] for r in doc["lexicon"]["roots"]}
        self.assertTrue({"crown", "hollow", "ember"} <= roots)
        bl = doc["blacklist"]
        self.assertTrue(bl["lexicon_stems_are_never_banned"])
        for sub in bl["substrings"] + bl["owner_banned"]["stems"]:
            self.assertEqual(sub, sub.lower())
            self.assertGreaterEqual(len(sub), 4)
        self.assertIn("Mordor", bl["exact"])
        # the owner's ban of 2026-09-25: the Corv-/Cassiv- family and Ashen Crown's own names
        for name in ("Cassivar", "Corvina", "Corvin", "Corwyn", "Emberhold", "Cinder Choir"):
            self.assertIn(name, bl["owner_banned"]["exact"])
        self.assertTrue({"corv", "corw", "cassiv"} <= set(bl["owner_banned"]["stems"]))
        self.assertGreaterEqual(len(bl["llm_favourites"]), 40)

    def test_samples_and_examples_pass_the_blacklist_and_the_name_registry(self):
        """No table may teach a banned name: samples, pattern examples and suffix examples are all checked."""
        import json
        from _campaign import PROJECT
        doc = dt.load("naming.yaml")
        bl = doc["blacklist"]
        exact = {n.lower() for n in bl["exact"] + bl["owner_banned"]["exact"] + bl["llm_favourites"] + bl["mythology"]}
        stems = [s.lower() for s in bl["substrings"] + bl["owner_banned"]["stems"]]
        registry = PROJECT / ".name_registry.json"
        registered = set()
        if registry.is_file():
            entries = json.loads(registry.read_text(encoding="utf-8")).get("entries", {})
            registered = {e["name"].lower() for e in entries.values() if e.get("name")}
        names = []
        for fam in dt.rows("naming.yaml#family"):
            names += fam["samples_person"] + fam["samples_god"]
        for kind, pats in doc["patterns"].items():
            for p in pats:
                names += p["examples"]
        names += [ex["name"] for ex in doc["rules"]["turkish_suffixing"]["examples"]]
        for sub in ("phenomenon", "people", "institution"):
            names += [r["label"] for r in dt.rows(f"signatures.yaml#{sub}")]
        for n in names:
            low = n.lower()
            with self.subTest(name=n):
                self.assertNotIn(low, exact)
                self.assertNotIn(low.split()[0], exact)
                self.assertFalse(any(s in low for s in stems), n)
                self.assertNotIn(low, registered)

    def test_turkish_suffix_rules_are_documented_with_examples(self):
        rules = dt.load("naming.yaml")["rules"]["turkish_suffixing"]
        self.assertGreaterEqual(len(rules["examples"]), 4)
        for ex in rules["examples"]:
            for key in ("dative", "locative", "genitive"):
                self.assertTrue(ex[key].startswith(ex["name"] + "'"), ex)


class Rubrics(unittest.TestCase):

    def test_rubrics_cover_every_generative_phase(self):
        rows = dt.rows("rubrics.yaml#phase_rubric")
        covered = {r.get("phase") for r in rows}
        for phase in dt.PHASES[1:]:
            self.assertIn(phase, covered)
        self.assertIn("detail", covered, "item 13.5: the detail-time critique")
        for r in rows + dt.rows("rubrics.yaml#special"):
            with self.subTest(rubric=r["id"]):
                self.assertIn(r["scope"], ("phase", "entity", "dm-only"))
                self.assertIn(r["effort"], ("high", "medium"))
                self.assertIn(r["critics"], (1, 2))
                self.assertTrue(r["question"].endswith(("?", ".")), r["question"])
                self.assertTrue(r["fails_when"])
        two = {r["id"] for r in rows if r["critics"] == 2}
        self.assertTrue({"rubric_p1_secret_trail", "rubric_p4_bbeg_answer", "rubric_p5_lieutenant"} <= two, "24.6 #6: two critics")
        specials = {r["id"] for r in dt.rows("rubrics.yaml#special")}
        self.assertTrue({"rubric_wishes", "rubric_leak", "rubric_cliche", "rubric_distinctness"} <= specials)
        self.assertEqual({v["value"] for v in dt.rows("rubrics.yaml#verdict")}, {"pass", "fix", "rerun"})

    # --- batch F: arc and threads ---------------------------------------------------

    def test_arc_beats_changes_phrasings_nodes_and_seeds(self):
        beats = dt.rows("arc.yaml#beat_template")
        short = [b for b in beats if "short" in b["scales"]]
        long_ = [b for b in beats if "standard" in b["scales"]]
        self.assertEqual(len(short), 3)
        self.assertEqual(len(long_), 6)
        self.assertEqual([b["act"] for b in long_], [1, 1, 2, 2, 3, 3])
        changes = {c["id"] for c in dt.rows("arc.yaml#change_kind")}
        self.assertGreaterEqual(len(changes), 8)
        for b in beats:
            self.assertTrue(set(b["change_bias"]) <= changes, b["id"])
            self.assertTrue(b["portent"] == -1 or b["portent"] >= 1, b["id"])
        for c in dt.rows("arc.yaml#change_kind"):
            self.assertTrue(c["before"] and c["after"], c["id"])
        pats = [re.compile(p, re.IGNORECASE) for r in dt.rows("arc.yaml#forbidden_phrasing") for p in r["en"]]
        for r in dt.rows("arc.yaml#forbidden_phrasing"):
            for p in r["tr"]:
                re.compile(p, re.IGNORECASE)
        self.assertTrue(any(p.search("The festival happens and the party finds the ledger") for p in pats))
        self.assertFalse(any(p.search("The Court's reading licence is revoked and Yesra reads only in secret") for p in pats))
        self.assertEqual({f["id"] for f in dt.rows("arc.yaml#fallback")}, {"fallback_cost", "fallback_secondary", "fallback_deferred"})
        nodes = {n["id"] for n in dt.rows("arc.yaml#node")}
        seeds = {s["id"] for s in dt.rows("arc.yaml#seed_shape")}
        for mix in dt.rows("dials.yaml#content_mix"):
            for kind in mix["effects"]["node_kinds"]:
                self.assertIn(f"node_{kind}", nodes, (mix["id"], kind))
            for kind in mix["effects"]["seed_kinds"]:
                self.assertIn(f"seed_{kind}", seeds, (mix["id"], kind))
        for n in dt.rows("arc.yaml#node"):
            for key in ("here", "stake", "ways_in", "never"):
                self.assertTrue(n[key], (n["id"], key))
        self.assertEqual({e["id"] for e in dt.rows("arc.yaml#ending")}, {"ending_win", "ending_loss", "ending_pyrrhic"})
        self.assertGreaterEqual(len(dt.rows("arc.yaml#planted_hook_kind")), 5)
        opens = {o["value"]: o for o in dt.rows("arc.yaml#opening_scene_type")}
        self.assertTrue(opens["tavern"]["forbidden"] and opens["stranger_with_a_job"]["forbidden"])
        self.assertGreaterEqual(len([o for o in opens.values() if not o.get("forbidden")]), 6)
        engines = {e["value"]: e for e in dt.rows("arc.yaml#plot_engine")}
        self.assertTrue(engines["prophecy"]["forbidden"] and engines["collect_pieces"]["forbidden"])

    def test_threads_sockets_truths_missions_and_crossings(self):
        sockets = dt.rows("threads.yaml#socket_type")
        self.assertGreaterEqual(len(sockets), 10)
        for s in sockets:
            self.assertTrue(s["question"].endswith("?"), s["id"])
            self.assertTrue(s["binds"], s["id"])
        truths = {t["value"]: t for t in dt.rows("threads.yaml#truth_kind")}
        for v in ("chosen", "destined", "amnesia"):
            self.assertTrue(truths[v]["forbidden"], v)
        self.assertGreaterEqual(len([t for t in truths.values() if not t.get("forbidden")]), 8)
        layers = dt.rows("threads.yaml#layer")
        self.assertEqual([l["id"] for l in layers], ["layer_1", "layer_2", "layer_3"])
        self.assertEqual(layers[2]["tier"], "secret")
        verbs = {v["value"]: v for v in dt.rows("threads.yaml#mission_verb")}
        self.assertTrue(verbs["find_out_who"]["forbidden"])
        self.assertTrue({"take_back", "prove", "destroy"} <= set(verbs))
        self.assertGreaterEqual(len(dt.rows("threads.yaml#crossing")), 5)
        self.assertGreaterEqual(len(dt.rows("threads.yaml#antagonist_binding")), 5)
        stages = dt.rows("threads.yaml#track_stage")
        self.assertEqual([s["order"] for s in stages], list(range(1, len(stages) + 1)))
        for s in stages:
            self.assertTrue(s["gate"] and s["cost"], s["id"])
        self.assertEqual(len(dt.rows("threads.yaml#weight_metric")), 5)
        self.assertEqual(dt.load("threads.yaml")["rules"]["equal_weight"][:7], "per PC:")


if __name__ == "__main__":
    unittest.main()
