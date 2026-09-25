"""
test_design_seed.py — design_seed.py runs a fragment's store calls through the
stores' own CLIs, once: the seeded ledger makes a second run a no-op, a secret
entity's graph node carries its id, and the four stores now write atomically
with a _meta block.
"""

import json
import unittest

from _campaign import TestCampaign

FRAG = "design/_staging/P5/merged/npc_yesra.json"


class DesignSeed(unittest.TestCase):

    def setUp(self):
        self.c = TestCampaign("seed")
        # start from a board without the fixture's pre-seeded rows for these ids
        graph = self.c.json("graph.json")
        graph["nodes"] = [n for n in graph["nodes"] if n["id"] != "npc_yesra"]
        graph["edges"] = [e for e in graph["edges"] if "npc_yesra" not in (e["from"], e["to"])]
        self.c.write_json("graph.json", graph)
        manifest = self.c.json("design/design.json")
        manifest["seeded"] = [k for k in manifest["seeded"] if "npc_yesra" not in k and "e_3" not in k]
        self.c.write_json("design/design.json", manifest)

    def tearDown(self):
        self.c.remove()

    def test_seeds_graph_goals_and_channels_once(self):
        frag = self.c.json(FRAG)
        frag["seeds"] = [
            {"store": "goals", "op": "add", "args": {"id": "npc_yesra", "name": "Yesra Saltreader", "kind": "npc",
                                                     "goal": "Bir daha okumamak", "metric_type": "boolean",
                                                     "condition": "Yesra bir daha okumadı",
                                                     "threatened": "susar", "blocked": "kaçar", "permanent_loss": "okur"}},
            {"store": "channels", "op": "add", "args": {"id": "ch_masa", "name": "Köşe masası", "type": "private-meeting",
                                                        "participants": ["npc_yesra", "npc_tolvan"], "note": "her akşam"}},
            {"store": "factions", "op": "stance", "args": {"from": "faction_court_of_mourners", "to": "party", "level": -1}},
        ]
        self.c.write_json(FRAG, frag)
        proc = self.c.run("design_seed.py", "--phase", "P5", "--session", "0", check=True)
        self.assertIn("call(s) made", proc.stdout)
        graph = self.c.json("graph.json")
        self.assertTrue(any(n["id"] == "npc_yesra" and n["name"] == "Yesra Saltreader" for n in graph["nodes"]))
        self.assertEqual(sum(1 for e in graph["edges"] if e["from"] == "npc_yesra"), 3)
        self.assertEqual(graph["_meta"]["written_by"], "campaign_graph.py")
        goals = self.c.json("goals.json")
        self.assertIn("_meta", goals)
        self.assertTrue(any(g["id"] == "npc_yesra" and g["kind"] == "npc" for g in goals["goals"]))
        channels = self.c.json("channels.json")
        self.assertTrue(any(ch["id"] == "ch_masa" and ch["participants"] == ["npc_yesra", "npc_tolvan"]
                            for ch in channels["channels"]))
        self.assertEqual(self.c.json("factions.json")["factions"][1]["stances"]["party"], -1)
        ledger = self.c.json("design/design.json")["seeded"]
        for key in ("graph:node:npc_yesra", "goals:npc_yesra", "channels:ch_masa",
                    "factions:faction_court_of_mourners:party", "graph:edge:npc_yesra:faction_court_of_mourners:member_of"):
            self.assertIn(key, ledger, key)
        # second run: nothing is called again, nothing duplicated
        proc = self.c.run("design_seed.py", "--phase", "P5", check=True)
        self.assertIn("0 call(s) made", proc.stdout)
        self.assertEqual(sum(1 for n in self.c.json("graph.json")["nodes"] if n["id"] == "npc_yesra"), 1)
        self.assertEqual(sum(1 for g in self.c.json("goals.json")["goals"] if g["id"] == "npc_yesra"), 1)
        self.assertEqual(self.c.temp_files(), [])

    def test_secret_entity_node_carries_its_id_not_its_name(self):
        frag = self.c.json(FRAG)
        frag["graph"] = {"nodes": [{"id": "npc_s01", "type": "npc", "name": "Nerun", "summary": "gizli"}], "edges": []}
        frag["seeds"] = []
        self.c.write_json(FRAG, frag)
        graph = self.c.json("graph.json")
        graph["nodes"] = [n for n in graph["nodes"] if n["id"] != "npc_s01"]
        self.c.write_json("graph.json", graph)
        manifest = self.c.json("design/design.json")
        manifest["seeded"] = [k for k in manifest["seeded"] if k != "graph:node:npc_s01"]
        self.c.write_json("design/design.json", manifest)
        self.c.run("design_seed.py", "--phase", "P5", check=True)
        node = next(n for n in self.c.json("graph.json")["nodes"] if n["id"] == "npc_s01")
        self.assertEqual(node["name"], "npc_s01")
        self.assertNotIn("summary", node)
        self.assertNotIn("Nerun", self.c.path("graph.json").read_text(encoding="utf-8"))

    def test_names_store_only_when_asked(self):
        frag = self.c.json(FRAG)
        frag["seeds"] = [{"store": "names", "op": "add", "args": {"name": "Yesra Saltreader", "type": "npc"}}]
        self.c.write_json(FRAG, frag)
        manifest = self.c.json("design/design.json")
        manifest["seeded"] = [k for k in manifest["seeded"] if not k.startswith("names:")]
        self.c.write_json("design/design.json", manifest)
        proc = self.c.run("design_seed.py", "--phase", "P5", "--dry-run", check=True)
        self.assertNotIn("name_registry.py", proc.stdout)
        proc = self.c.run("design_seed.py", "--phase", "P5", "--stores", "names", "--dry-run", check=True)
        self.assertIn("name_registry.py add", proc.stdout)
        self.assertIn("--campaign", proc.stdout)

    def test_a_failing_call_is_reported_and_the_rest_still_run(self):
        frag = self.c.json(FRAG)
        frag["seeds"] = [
            {"store": "goals", "op": "add", "args": {"id": "npc_yesra", "name": "Y", "kind": "npc", "goal": "g",
                                                     "metric_type": "numeric"}},   # missing target: goals.py refuses
            {"store": "channels", "op": "add", "args": {"id": "ch_x", "name": "X", "participants": ["npc_yesra"]}},
        ]
        self.c.write_json(FRAG, frag)
        proc = self.c.run("design_seed.py", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("1 failed", proc.stdout)
        self.assertTrue(any(ch["id"] == "ch_x" for ch in self.c.json("channels.json")["channels"]))
        self.assertNotIn("goals:npc_yesra", self.c.json("design/design.json")["seeded"])

    def test_unknown_store_is_usage_error(self):
        self.assertEqual(self.c.run("design_seed.py", "--phase", "P5", "--stores", "vibes").returncode, 2)


if __name__ == "__main__":
    unittest.main()
