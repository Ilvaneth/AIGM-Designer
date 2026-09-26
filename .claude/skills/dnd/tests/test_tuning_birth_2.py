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


class Resume(unittest.TestCase):
    """The resume addendum (R.3-R.6): the primer, the seed call, an empty merge, P8's player files, the P7 and P8
    cards, critics that never passed, the seed batches' own file, the primer's default read list."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("tune2r")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def primer_container(self, pid="polity_reedmarch"):
        merged = self.c.path("design/_staging/P8/merged")
        merged.mkdir(parents=True, exist_ok=True)
        section = self.c.path(f"design/_staging/P8/primer_{pid}.section.md")
        self.c.write_json(f"design/_staging/P8/merged/primer_{pid}.json", dict(
            fragment(f"primer_{pid}", None, phase="P8"), prose={"file": f"design/_staging/P8/primer_{pid}.section.md"},
            counts={"words": 640, "sayings": 3}))
        return section

    def test_r6_primer_strips_section_front_matter_and_speaks_turkish(self):
        section = self.c.path("design/_staging/P8/primer_polity_reedmarch.section.md")
        section.parent.mkdir(parents=True, exist_ok=True)
        section.write_text("---\nentity: none\ntype: primer_section\nsecrecy: public\nphase: P8\n---\n\n"
                           "Reedmarch'ta dogan bilir: tuz her seyi hatirlar.\n", encoding="utf-8")
        self.c.run("render_player.py", "primer", check=True)
        text = self.c.path("design/player-primer.md").read_text(encoding="utf-8")
        self.assertNotIn("type: primer_section", text, "the section's front matter never reaches the player")
        self.assertIn("tuz her seyi hatirlar", text)
        self.assertIn("## Kısa tanıtım", text)
        self.assertIn("### Takvim ve bayramlar", text)
        self.assertNotIn("The pitch", text)
        self.assertNotIn("Famous places", text)
        findings = json.loads(self.c.run("design_check.py", "--modules", "secrecy", "--json", check=True).stdout)
        self.assertFalse([f for f in findings if f["code"] == "file_no_secrecy" and "player-primer" in str(f.get("message"))])

    def test_r5_site_progress_open_speaks_the_cli_flags(self):
        import design_seed
        argv = design_seed.argv_for("site_progress", "open", {"site": "site_x", "payoff_room": 11, "room_count": 18, "entrances": ["1", "2"]}, "camp", 0)
        self.assertEqual(argv[:5], ["site_progress.py", "-c", "camp", "open", "site_x"])
        joined = " ".join(argv)
        self.assertIn("--payoff 11", joined)
        self.assertIn("--rooms 18", joined)
        self.assertIn("--entrances", joined)
        self.assertNotIn("payoff-room", joined)
        self.assertNotIn("room-count", joined)

    def test_r5_a_merge_that_merged_nothing_keeps_the_phase_open(self):
        self.c.reopen("P6", "running", roster=[], skeleton={"status": "pending", "agent": None})
        proc = self.c.run("designer.py", "phase", "P6", "merge", "--tokens", "197838", "--seconds", "146")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("nothing merged", proc.stderr)
        ph = self.c.json("design/design.json")["phases"]["P6"]
        self.assertEqual(ph["status"], "running", "a Workflow that died before writing anything leaves no merged phase")

    def test_r4_p8_merge_renders_the_player_files(self):
        self.primer_container()
        primer = self.c.path("design/player-primer.md")
        if primer.is_file():
            primer.unlink()
        self.c.reopen("P8", "partial", roster=["primer_polity_reedmarch"])
        proc = self.c.run("designer.py", "phase", "P8", "merge", check=True)
        self.assertTrue(primer.is_file(), "P8's merge renders facts, news and the primer once the roster is complete")
        self.assertIn("primer", proc.stdout)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P8"]["status"], "merged")

    def test_r6_the_p7_card_counts_the_arc_instead_of_printing_it(self):
        self.c.run("design_approval.py", "card", "--phase", "P7", check=True)
        text = self.c.path("design/_approval/P7.card.md").read_text(encoding="utf-8")
        rows = [l for l in text.splitlines() if l.startswith("| ")]
        self.assertFalse([r for r in rows if r.startswith(("| chapter_", "| beat_", "| node_", "| socket_"))], "arc rows are never printed")
        self.assertIn("chapter ×", text)
        self.assertIn("oyuncuya kapalı", text)
        names_comment = next(l for l in text.splitlines() if l.startswith("<!-- names:"))
        self.assertNotIn("beat_", names_comment)

    def test_r6_the_p8_card_lists_its_documents_and_the_primer(self):
        self.primer_container()
        self.c.reopen("P8", "partial", roster=["primer_polity_reedmarch"])
        self.c.run("designer.py", "phase", "P8", "merge", check=True)
        self.c.run("design_approval.py", "card", "--phase", "P8", check=True)
        text = self.c.path("design/_approval/P8.card.md").read_text(encoding="utf-8")
        self.assertIn("## Belgeler", text)
        self.assertIn("`primer_polity_reedmarch` — merged", text)
        self.assertIn("words 640", text)
        self.assertIn("oyuncu primer'ı: `design/player-primer.md` (", text)
        self.assertNotIn("(bu faz henüz varlık üretmedi)", text)

    def test_r6_critics_that_never_passed_are_loud_on_the_card(self):
        records = [{"entity_id": "site_sunken_pier", "critic": 1, "verdict": "fix", "findings": [], "kind": "entity"},
                   {"entity_id": "phase", "critic": 1, "verdict": "fix", "findings": [], "kind": "phase"}]
        self.c.reopen("P6", "partial", roster=["site_sunken_pier"],
                      critique={"phase_loops": 1, "verdicts": ["fix"], "entity_loops_total": 2, "records": records, "skeleton_verdicts": ["fix", "fix"]})
        self.c.run("design_approval.py", "card", "--phase", "P6", check=True)
        text = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("⚠ **Eleştirmen geçmedi:** site_sunken_pier, faz eleştirmeni, iskelet", text)

    def test_r5_seed_batches_write_their_own_file(self):
        rendered = self.c.run("design_prompts.py", "render", "P7.seeds", "--id", "seedbatch_1", "--attempt", "1", check=True).stdout
        self.assertIn("design/seeds/seedbatch_1.md", rendered)
        self.assertIn("Never write into `design/arc.md`", rendered)

    def test_r6_a_primer_section_gets_a_default_read_list(self):
        self.c.reopen("P8", "prerolled", roster=["primer_polity_newland"])
        m = self.c.json("design/design.json")
        m["entities"]["primer_polity_newland"] = {"phase": "P8", "status": "pending", "attempt": 0, "critique_loops": 0,
                                                 "last_error": None, "file": None, "stage_file": None, "agent": None}
        self.c.write_json("design/design.json", m)
        proc = self.c.run("designer.py", "phase", "P8", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        e = next(x for x in out["entities"] if x["id"] == "primer_polity_newland")
        self.assertIn("design/cosmology.md", e["files"])
        self.assertIn("design/premise.md", e["files"])
        self.assertFalse([f for f in e["files"] if "dm-only" in f], "a primer writer reads public files only")


if __name__ == "__main__":
    unittest.main()
