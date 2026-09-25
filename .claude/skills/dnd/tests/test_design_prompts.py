"""
test_design_prompts.py — the prompt library (slice 1c item 2): every prompt parses with its front
matter and known placeholders; every generative phase has a writer or a skeleton; rendering for a
fixture entity fills every placeholder from the manifest and the public projection only (no secret
name ever enters a prompt); critics embed their phase's rubric rows and the second critic reads
them in reverse; the ask prompt carries the question; designer.py's `phase begin --json` hands out
the render commands and rendered copies, and `merge` absorbs a skeleton's roster and assignments.
"""

import json
import shutil
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_prompts as dp  # noqa: E402
import design_tables as dt  # noqa: E402


class Library(unittest.TestCase):

    def test_every_prompt_checks_clean(self):
        self.assertEqual(dp.check(), [])
        self.assertGreaterEqual(len(dp.list_prompts()), 25)

    def test_every_generative_phase_has_a_writer_or_a_skeleton(self):
        for phase in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"):
            skeleton, writers = dp.PROMPT_BY_PHASE[phase]
            self.assertTrue(skeleton or writers, phase)
            for _, name in writers:
                self.assertIn(name, dp.list_prompts(), name)
            if skeleton:
                self.assertIn(skeleton, dp.list_prompts())
        self.assertEqual(dp.prompt_for("P6", "site_sunken_pier"), "P6.site")
        self.assertEqual(dp.prompt_for("P5", "npcbatch_2"), "P5.minors")
        self.assertEqual(dp.prompt_for("P5", "npc_yesra"), "P5.npc")
        self.assertEqual(dp.prompt_for("P3", None), "P3.skeleton")
        self.assertIsNone(dp.prompt_for("P1", None))
        self.assertEqual(dp.prompt_for("detail", "settlement_lanternside"), "detail.settlement")

    def test_front_matter_effort_and_critics_follow_item_19_7(self):
        for name in dp.list_prompts():
            fm, body = dp.load(name)
            with self.subTest(prompt=name):
                self.assertIn(fm["effort"], ("high", "medium"))
                self.assertIn(int(fm.get("critics") or 1), (1, 2))
                if fm["role"] != "ask":
                    self.assertIn("{{common}}", body, "every agent prompt carries the preamble")
                self.assertIn("{{schema}}", body, "every prompt ends with its return schema")
        self.assertEqual(dp.load("P1.premise")[0]["critics"], 2, "24.6 #6: two critics on the premise secret")
        self.assertEqual(dp.load("P4.skeleton")[0]["critics"], 2)
        self.assertEqual(dp.load("P1.premise")[0]["effort"], "high")

    def test_preamble_states_the_rules(self):
        common = dp.common_text()
        for phrase in ("English-language fantasy name", "never roll dice", "## Secret", "Prose", "fragment"):
            self.assertIn(phrase, common)


class Rendering(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("prompts")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_site_writer_renders_from_the_projection_only(self):
        text = dp.render(self.c.name, "P6.site", "site_sunken_pier")
        self.assertNotIn("{{", text)
        self.assertIn("Sunken Pier", text)
        self.assertIn("design/sites/site_sunken_pier.md", text)
        self.assertIn("design/dm-only/sites/site_sunken_pier.md", text)
        self.assertIn("design/_staging/P6/site_sunken_pier.json", text)
        self.assertIn("templates/design/site-detailed.md", text)
        self.assertIn("scale short", text)
        self.assertNotIn("Nerun", text, "a secret entity's name never enters a prompt")
        self.assertIn("How every design agent works", text)
        self.assertIn('"entity_id"', text)

    def test_skeleton_and_document_prompts_render_without_an_entity(self):
        text = dp.render(self.c.name, "P3.skeleton")
        self.assertNotIn("{{", text)
        self.assertIn("lands skeleton", text)
        self.assertIn("skeleton.json", text)
        self.assertIn("polities 1", text)
        text = dp.render(self.c.name, "P1.premise")
        self.assertIn("trope breaks 1", text)
        self.assertIn("secret_archetype", text)

    def test_critic_embeds_the_phase_rubric_and_the_second_critic_reverses_it(self):
        one = dp.render(self.c.name, "critic", "site_sunken_pier", critic_order=1)
        two = dp.render(self.c.name, "critic", "site_sunken_pier", critic_order=2)
        # the entity prompt's phase is `all`; the phase-specific rubric comes through the campaign's manifest phase of the entity
        self.assertIn("rubric_cliche", one)
        self.assertIn("rubric_english_names", one)
        self.assertNotEqual(one, two)
        self.assertIn("You are critic 2", two)

    def test_ask_prompt_carries_the_question_and_nothing_else_variable(self):
        text = dp.render(self.c.name, "ask", question="Yesra Court'un başı mı?")
        self.assertIn("Yesra Court'un başı mı?", text)
        self.assertIn("spoiler vermeden cevaplanamaz", text)
        self.assertNotIn("{{", text)

    def test_designer_begin_hands_out_prompts_and_merge_absorbs_a_skeleton(self):
        proc = self.c.run("designer.py", "phase", "P6", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertEqual(out["phase"], "P6")
        self.assertIn("phase_critic", out)
        # a skeleton.json in staging is absorbed by merge: roster, assignments, reads; a roster id that is not
        # in the registry yet stays pending (disk is truth) and gets its prompt bundle
        staging = self.c.path("design/_staging/P6")
        (staging / "skeleton.json").write_text(json.dumps({
            "phase": "P6", "status": "staged", "roster": ["site_sunken_pier", "site_new_cove"],
            "assignments": {"site.1": "site_sunken_pier", "site.2": "site_new_cove"},
            "reads": {"site_new_cove": ["design/regions/region_saltmere.md"]}, "fragments": []}), encoding="utf-8")
        merge = self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.assertIn("skeleton absorbed", merge.stdout)
        self.assertTrue((staging / "merged" / "skeleton.json").is_file())
        m = self.c.json("design/design.json")
        self.assertEqual(m["phases"]["P6"]["assignments"]["site.2"], "site_new_cove")
        self.assertEqual(m["phases"]["P6"]["skeleton"]["status"], "merged")
        self.assertEqual(m["phases"]["P6"]["status"], "partial", "a pending roster entity keeps the phase partial")
        proc = self.c.run("designer.py", "phase", "P6", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        pend = {e["id"]: e for e in out["entities"]}
        self.assertNotIn("site_sunken_pier", pend, "disk is truth: the merged site is not pending")
        self.assertIn("site_new_cove", pend)
        e = pend["site_new_cove"]
        self.assertEqual(e["prompt"], "P6.site")
        self.assertIn("render P6.site --id site_new_cove", e["prompt_cmd"])
        self.assertTrue(Path(e["prompt_file"]).is_file())
        self.assertTrue(Path(e["critic_file"]).is_file())
        self.assertIn("design/regions/region_saltmere.md", e["files"], "the skeleton's reads join the budget")
        rendered = Path(e["prompt_file"]).read_text(encoding="utf-8")
        self.assertIn("site_new_cove", rendered)
        self.assertNotIn("Nerun", rendered)


if __name__ == "__main__":
    unittest.main()
