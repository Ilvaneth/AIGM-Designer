"""
test_design_revise.py — the birth-round revise (plan item 14.1-14.3, 19.6; slice 1c item 4): a
correction is one sentence with a scope. A direction is stored on the phase (or on the wishes with
--world) and names the entities to rerun; a fact changes one registry field, regenerates the
projection and snapshot, and lists the entities whose refs reach the changed one as affected; an
entity is removed or marked for replacement; a phase rerun goes through designer.py. Every round is
recorded on the phase (max three) and in the revision log; --reseed changes the master seed.
"""

import json
import sys
import unittest

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))


class Rounds(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("revise")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def manifest(self):
        return self.c.json("design/design.json")

    def test_direction_is_stored_and_names_the_rerun_set(self):
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "direction",
                          "--text", "odalar daha ıslak ve dar olsun", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertEqual(out["scope"], "direction")
        self.assertIn("site_sunken_pier", out["rerun"])
        m = self.manifest()
        self.assertIn("odalar daha ıslak ve dar olsun", m["phases"]["P6"]["directions"])
        self.assertEqual(m["phases"]["P6"]["approval"]["rounds"][-1]["scope"], "direction")
        self.assertEqual(m["revision_log"][-1]["scope"], "direction")
        self.assertEqual(m["entities"]["site_sunken_pier"]["status"], "pending", "a direction reruns the phase's entities")
        self.assertEqual(m["entities"]["site_sunken_pier"]["attempt"], 3)

    def test_world_direction_amends_the_wishes(self):
        self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "direction", "--world",
                   "--text", "her yerde tuz kokusu", check=True)
        m = self.manifest()
        self.assertIn("her yerde tuz kokusu", m["dials"]["wishes"]["must"])

    def test_fact_changes_a_field_and_lists_the_affected(self):
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "fact", "--entity", "site_sunken_pier",
                          "--field", "name", "--value", "Drowned Pier", "--text", "iskelenin adı Drowned Pier olsun",
                          "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertEqual(out["scope"], "fact")
        canon = self.c.json("design/dm-only/entities.json")["entities"]["site_sunken_pier"]
        proj = self.c.json("design/entities.json")["entities"]["site_sunken_pier"]
        self.assertEqual(canon["name"], "Drowned Pier")
        self.assertEqual(proj["name"], "Drowned Pier")
        self.assertIn("Sunken Pier", canon["aliases"], "the old name survives as an alias")
        self.assertIn("npc_kortan", out["affected"], "entities whose refs reach the site")
        self.assertIn("region_saltmere", out["affected"])
        self.assertNotIn("npc_s01", out["affected"], "a secret referrer is counted, never listed")
        self.assertIn("site_sunken_pier", out["rerun"])
        m = self.manifest()
        self.assertEqual(m["revision_log"][-1]["scope"], "fact")
        self.assertGreaterEqual(m["revision_log"][-1]["affected"], 2)

    def test_stamped_fact_changes_move_the_snapshot_during_birth(self):
        self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "fact", "--entity", "site_sunken_pier",
                   "--field", "danger_tier", "--value", "2", "--text", "iskele T2 olsun", check=True)
        snap = self.c.json("design/dm-only/_snapshots/stamps.json")["stamps"]["site_sunken_pier"]
        self.assertEqual(snap["danger_tier"], 2)
        self.assertEqual(self.c.run("registry.py", "check-stamps").returncode, 0)

    def test_fact_refuses_unknown_entity_or_secret_field(self):
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "fact", "--entity", "site_nowhere",
                          "--field", "name", "--value", "X", "--text", "x")
        self.assertEqual(proc.returncode, 1)
        proc = self.c.run("design_revise.py", "round", "--phase", "P5", "--scope", "fact", "--entity", "npc_yesra",
                          "--field", "secret_tr", "--value", "X", "--text", "x")
        self.assertEqual(proc.returncode, 1, "dm-only fields are slice 3's --dm-only path, never a public round")

    def test_entity_remove_and_replace(self):
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "entity", "--entity", "site_tide_cave",
                          "--action", "remove", "--text", "mağarayı kaldır", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertNotIn("site_tide_cave", self.c.json("design/dm-only/entities.json")["entities"])
        self.assertNotIn("site_tide_cave", self.c.json("design/entities.json")["entities"])
        self.assertTrue(self.c.path("design/_revised/site_tide_cave.md").is_file(), "removed prose is archived, not deleted")
        self.assertFalse(self.c.path("design/sites/site_tide_cave.md").is_file())
        self.assertTrue(len(out["affected"]) >= 1)
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "entity", "--entity", "site_blind_lantern",
                          "--action", "replace", "--text", "feneri baştan yaz", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertEqual(out["rerun"], ["site_blind_lantern"])
        m = self.manifest()
        self.assertEqual(m["entities"]["site_blind_lantern"]["status"], "pending")
        self.assertIn("feneri baştan yaz", m["phases"]["P6"]["directions"][-1])

    def test_phase_scope_reruns_through_designer_and_reseed_changes_the_seed(self):
        before = self.manifest()["seed"]["master"]
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "phase", "--reseed",
                          "--text", "mekânlar baştan", check=True)
        self.assertIn("attempt 3", proc.stdout)
        m = self.manifest()
        self.assertNotEqual(m["seed"]["master"], before)
        self.assertEqual(m["phases"]["P6"]["status"], "pending")
        self.assertEqual(m["phases"]["P7"]["status"], "stale")

    def test_three_rounds_then_refused(self):
        already = len(self.manifest()["phases"]["P6"]["approval"]["rounds"])   # the fixture carries one round
        for n in range(3 - already):
            self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "direction", "--text", f"yön {n}", check=True)
        proc = self.c.run("design_revise.py", "round", "--phase", "P6", "--scope", "direction", "--text", "yön 4")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("three", proc.stderr)

    def test_affected_lists_referrers(self):
        proc = self.c.run("design_revise.py", "affected", "--entity", "npc_yesra", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertIn("faction_court_of_mourners", out["affected"])
        self.assertNotIn("npc_s01", out["affected"], "a secret referrer is reported by count, never by id")
        self.assertGreaterEqual(out["hidden"], 0)


if __name__ == "__main__":
    unittest.main()
