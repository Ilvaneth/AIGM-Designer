"""
test_tuning_birth_2.py — regressions from the second tuning birth (docs/reports/tuning-birth-2.md,
2026-09-25, the resume test): a prose field given as a path string merges and a wrong shape is a
refusal, never a crash; the conductor's merge never reads a stale report; `begin` refuses while
staged fragments wait unmerged; graph nodes are seeded before edges and a missing endpoint is
synthesised from the registry; the validator asks no roles or tier of a stub a later phase fills;
critic records take their kind from the file they were saved as, so the card shows the phase, wishes
and skeleton verdicts apart; majors get two critics at high effort; read budgets are relative and deduped.
"""

import json
import shutil
import sys
import unittest

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))

from test_tuning_birth_1 import FRONT, fragment, row  # noqa: E402


class Birth2(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("tune2")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def canonical(self):
        return self.c.json("design/dm-only/entities.json")["entities"]

    def test_3_1_a_prose_path_string_merges_and_a_wrong_shape_is_refused_not_crashed(self):
        pub = self.c.path("design/npcs/npc_tune_str.md")
        pub.write_text(FRONT.format(eid="npc_tune_str", etype="npc", secrecy="public", phase="P5", link="tier: minor"), encoding="utf-8")
        ok = fragment("npc_tune_str", row("npc_tune_str", "npc", "Ansel Rook", file="design/npcs/npc_tune_str.md"),
                      prose="design/npcs/npc_tune_str.md")
        bad = fragment("npc_tune_num", row("npc_tune_num", "npc", "Bram Vell"), prose=42)
        self.c.write_json("design/_staging/P5/npc_tune_str.json", ok)
        self.c.write_json("design/_staging/P5/npc_tune_num.json", bad)
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertIn("npc_tune_str", self.canonical(), "a bare path string is accepted as the file")
        self.assertIn("prose must be an object {file, bytes, sha256} or a path string (got int)", proc.stderr)
        self.assertNotIn("npc_tune_num", self.canonical())

    def test_3_1_the_conductor_never_reads_a_stale_merge_report(self):
        self.c.reopen("P6", "partial", roster=["site_sunken_pier"])
        self.c.write_json("design/_staging/P6/merge.report.json", {"phase": "P6", "refused": {"npc_stale": ["an old run's reason"]}})
        proc = self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.assertIn("nothing to merge", proc.stdout)
        m = self.c.json("design/design.json")
        self.assertNotIn("npc_stale", m["entities"])
        self.assertFalse(self.c.path("design/_staging/P6/merge.report.json").is_file())

    def test_begin_refuses_while_staged_fragments_wait_unmerged(self):
        merged = self.c.path("design/_staging/P6/merged/site_sunken_pier.json")
        shutil.copy(merged, merged.parent.parent / "site_sunken_pier.json")
        self.c.reopen("P6", "partial", roster=["site_sunken_pier"])
        proc = self.c.run("designer.py", "phase", "P6", "begin", "--json")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not merged yet", proc.stderr)
        self.assertIn("site_sunken_pier", proc.stderr)
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.c.run("designer.py", "phase", "P6", "begin", "--json", check=True)

    def test_3_2_graph_nodes_seed_before_edges_and_missing_endpoints_come_from_the_registry(self):
        self.c.write_json("design/_staging/P6/npc_tune_graph.json", fragment("npc_tune_graph", row("npc_tune_graph", "npc", "Wren Tallow"), phase="P6"))
        self.c.run("registry.py", "merge", "--phase", "P6", check=True)
        merged = self.c.path("design/_staging/P6/merged")
        self.c.write_json("design/_staging/P6/merged/aaa_edges.json", dict(fragment("aaa_edges", None, phase="P6"), graph={
            "nodes": [], "edges": [{"from": "npc_tune_late", "to": "npc_tune_graph", "type": "knows", "since_session": 0}]}))
        self.c.write_json("design/_staging/P6/merged/zzz_node.json", dict(fragment("zzz_node", None, phase="P6"), graph={
            "nodes": [{"id": "npc_tune_late", "name": "Late Node", "type": "npc"}], "edges": []}))
        proc = self.c.run("design_seed.py", "--phase", "P6", "--stores", "graph", check=True)
        self.assertIn("0 failed", proc.stdout)
        graph = self.c.json("graph.json")
        nodes = graph.get("nodes") if isinstance(graph, dict) else graph
        ids = {n.get("id") for n in (nodes if isinstance(nodes, list) else nodes.values())}
        self.assertIn("npc_tune_late", ids, "the node a later fragment defines exists before the edge")
        self.assertIn("npc_tune_graph", ids, "an endpoint with no node block is synthesised from the registry")

    def test_validator_asks_no_roles_or_tier_of_a_stub_a_later_phase_fills(self):
        fac = row("faction_tune_stub", "faction", "Lamp Wardens", status="pending", owner_phase="P4", reserved_by="P3.skeleton.a1")
        site = row("site_tune_stub", "site", "Moon Ford", status="pending", owner_phase="P6", reserved_by="doc_cosmology")
        self.c.write_json("design/_staging/P3/faction_tune_stub.json", fragment("faction_tune_stub", fac, phase="P3"))
        self.c.write_json("design/_staging/P3/site_tune_stub.json", fragment("site_tune_stub", site, phase="P3"))
        self.c.run("registry.py", "merge", "--phase", "P3", check=True)
        proc = self.c.run("design_check.py", "--modules", "refs,stamps", "--phase", "P3", "--json")
        findings = json.loads(proc.stdout)
        mine = [f for f in findings if f.get("entity") in ("faction_tune_stub", "site_tune_stub")]
        self.assertFalse([f for f in mine if f["code"] in ("role_unfilled", "bad_tier")], mine)

    def test_critic_records_take_their_kind_from_the_file_and_the_card_shows_them_apart(self):
        staging = self.c.path("design/_staging/P6")
        (staging / "skeleton.critic1.json").write_text(json.dumps({"entity_id": "P6", "verdict": "fix", "findings": []}), encoding="utf-8")
        (staging / "wishes.critic1.json").write_text(json.dumps({"entity_id": "P6", "verdict": "pass", "findings": []}), encoding="utf-8")
        (staging / "phase.critic1.json").write_text(json.dumps({"entity_id": "P6", "verdict": "fix", "findings": [
            {"rubric_id": "rubric_p6_only_here", "entity_id": "site_sunken_pier", "verdict": "fix", "reason_code": "twin_rooms"}]}), encoding="utf-8")
        self.c.reopen("P6", "partial", roster=["site_sunken_pier"], critique={"phase_loops": 0, "verdicts": [], "entity_loops_total": 0})
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        crit = self.c.json("design/design.json")["phases"]["P6"]["critique"]
        self.assertEqual({r["kind"] for r in crit["records"]}, {"skeleton", "wishes", "phase"})
        self.assertEqual(crit["skeleton_verdicts"], ["fix"])
        self.assertEqual(crit["wishes_verdicts"], ["pass"])
        self.assertEqual(crit["verdicts"], ["fix"], "the skeleton's fix is not a phase verdict")
        self.c.run("design_approval.py", "card", "--phase", "P6", check=True)
        text = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("faz eleştirmeni fix", text)
        self.assertIn("dilek eleştirmeni pass", text)
        self.assertIn("iskelet fix", text)
        self.assertIn("rubric_p6_only_here → site_sunken_pier (fix, twin_rooms)", text)

    def test_majors_get_two_critics_at_high_effort_and_the_files_are_relative_and_unique(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["npc_yesra"]["tier"] = "major"
        self.c.write_json("design/dm-only/entities.json", canon)
        m = self.c.json("design/design.json")
        m["entities"]["npc_yesra"] = {"phase": "P5", "status": "pending", "attempt": 2, "rerun": True, "critique_loops": 0,
                                      "last_error": None, "file": None, "stage_file": None, "agent": None}
        m["phases"]["P5"]["status"] = "prerolled"
        m["phases"]["P5"]["roster"] = ["npc_yesra"]
        self.c.write_json("design/design.json", m)
        proc = self.c.run("designer.py", "phase", "P5", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        e = next(x for x in out["entities"] if x["id"] == "npc_yesra")
        self.assertEqual((e["critics"], e["effort"]), (2, "high"))
        self.assertIn("--critic-order 2", e["critic2_cmd"])
        self.assertEqual(e["render_attempt"], 2, "a revise-marked rerun keeps its bumped attempt")
        self.assertTrue(e["files"])
        self.assertEqual(len(e["files"]), len(set(e["files"])))
        self.assertFalse([f for f in e["files"] if ":" in f or f.startswith("/")], e["files"])


if __name__ == "__main__":
    unittest.main()
