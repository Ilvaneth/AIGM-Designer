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
                     "The Nine Hells", "Elysium", "Hades"):
            self.assertIn(name, labels)
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
        # the SRD's historical deities sit on the plane of their alignment
        deities = {d["id"]: d for d in dt.rows("pantheon.yaml#srd_deities")}
        self.assertGreaterEqual(len(deities), 60)
        outer_ids = {r["id"]: r for r in outer}
        domains = set(dt.load("pantheon.yaml")["rules"]["domains"])
        for d in deities.values():
            self.assertIn(d["home_plane"], outer_ids, d["id"])
            self.assertEqual(outer_ids[d["home_plane"]]["alignment"], d["alignment"], d["id"])
            self.assertTrue(set(d["domains"]) <= domains, d["id"])
            self.assertIn(d["pantheon"], ("celtic", "greek", "egyptian", "norse"))
            self.assertTrue(d["symbol"] and d["epithet"], d["id"])
        for r in outer:
            for did in r["srd_deities"]:
                self.assertEqual(deities[did]["alignment"], r["alignment"], (r["id"], did))
        self.assertGreaterEqual(len(dt.rows("planes.yaml#deviation")), 6)
        rates = {r["id"]: r for r in dt.rows("planes.yaml#time_rate")}
        self.assertGreaterEqual(len(rates), 5)
        self.assertEqual(rates["rate_same"]["rate"], 1)
        self.assertGreaterEqual(len(dt.rows("planes.yaml#way_in")), 6)
        self.assertGreaterEqual(len(dt.rows("planes.yaml#cost")), 6)

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
        exact = {n.lower() for n in bl["exact"] + bl["owner_banned"]["exact"] + bl["llm_favourites"]}
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
        if not (TABLES / "rubrics.yaml").is_file():
            self.skipTest("rubrics.yaml lands in the last 1b batch")
        covered = {r.get("phase") for r in dt.rows("rubrics.yaml")}
        for phase in dt.PHASES[1:]:
            self.assertIn(phase, covered)


if __name__ == "__main__":
    unittest.main()
