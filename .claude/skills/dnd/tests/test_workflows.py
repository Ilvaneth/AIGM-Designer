"""
test_workflows.py — the designer's Workflow scripts (plan item 19.2, slice 1c item 6): both scripts
under .claude/workflows/ carry the pure-literal meta with phase titles that match their phase()
calls, embed the same return schemas the prompt library ships, read the JSON `designer.py phase PN
begin --json` prints, and never touch a forbidden API; the begin JSON names the workflow to run and
carries the phase and wishes critics; critic returns saved in staging are recorded at merge.
"""

import json
import re
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, MarkerGuard, SCRIPTS, PROJECT

sys.path.insert(0, str(SCRIPTS))

WORKFLOWS = PROJECT / ".claude" / "workflows"
SCHEMAS = SCRIPTS.parent / "prompts" / "design" / "schemas"


def js_object_literal(text: str, name: str) -> dict:
    """Extract `const NAME = {...}` (a JSON-compatible literal with single-quoted strings) as a dict."""
    m = re.search(r"const %s = (\{.*?\n\})\n" % name, text, re.S)
    assert m, f"no const {name}"
    literal = m.group(1)
    literal = re.sub(r"'((?:[^'\\]|\\.)*)'", lambda x: '"' + x.group(1).replace('"', '\\"') + '"', literal)
    literal = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', literal)
    literal = re.sub(r",(\s*[}\]])", r"\1", literal)
    return json.loads(literal)


class Scripts(unittest.TestCase):

    def script(self, name: str) -> str:
        path = WORKFLOWS / f"{name}.js"
        self.assertTrue(path.is_file(), path)
        return path.read_text(encoding="utf-8")

    def test_meta_is_first_and_phase_titles_match(self):
        for name in ("design-skeleton", "design-fanout"):
            text = self.script(name)
            with self.subTest(workflow=name):
                self.assertTrue(text.startswith("export const meta = {"), "meta must be the first statement")
                meta_block = text[:text.index("\n}\n") + 3]
                self.assertNotIn("${", meta_block, "meta is a pure literal")
                self.assertIn(f"name: '{name}'", meta_block)
                titles = re.findall(r"\{ title: '([^']+)'", meta_block)
                called = set(re.findall(r"phase\('([^']+)'\)", text)) | set(re.findall(r"phase: '([^']+)'", text))
                self.assertTrue(set(titles) <= called or called <= set(titles), (titles, called))
                for t in titles:
                    self.assertIn(t, called)

    def test_scripts_avoid_forbidden_apis_and_typescript(self):
        for name in ("design-skeleton", "design-fanout"):
            text = self.script(name)
            with self.subTest(workflow=name):
                for banned in ("Date.now(", "Math.random(", "new Date()", "require(", "import ", "fs.", "process."):
                    self.assertNotIn(banned, text, banned)
                self.assertNotIn(": string", text)
                self.assertIn("return {", text) if name == "design-fanout" else self.assertIn("return result", text)

    def test_embedded_schemas_equal_the_prompt_library_schemas(self):
        writer = json.loads((SCHEMAS / "writer.json").read_text(encoding="utf-8"))
        critic = json.loads((SCHEMAS / "critic.json").read_text(encoding="utf-8"))
        skeleton = json.loads((SCHEMAS / "skeleton.json").read_text(encoding="utf-8"))

        def strip(d):
            if isinstance(d, dict):
                return {k: strip(v) for k, v in d.items() if k != "description"}
            if isinstance(d, list):
                return [strip(x) for x in d]
            return d
        fan = self.script("design-fanout")
        self.assertEqual(js_object_literal(fan, "WRITER"), strip(writer))
        self.assertEqual(js_object_literal(fan, "CRITIC"), strip(critic))
        self.assertEqual(js_object_literal(self.script("design-skeleton"), "SKELETON"), strip(skeleton))

    def test_fanout_reads_the_begin_json_shape(self):
        fan = self.script("design-fanout")
        for key in ("a.entities", "e.prompt_cmd", "e.critic_cmd", "e.critic2_cmd", "e.critics", "a.phase_critic", "a.wishes_critic", "MAX_FIX_LOOPS = 2"):
            self.assertIn(key, fan)
        self.assertIn("pipeline(entities", fan, "no barrier between entities")
        sk = self.script("design-skeleton")
        self.assertIn("a.skeleton.prompt_cmd", sk)

    def test_tuning_birth_1_the_critics_verdicts_are_acted_on(self):
        fan = self.script("design-fanout")
        self.assertIn("fix (second critic)", fan, "the second critic's fix gets a loop")
        self.assertIn("critique(r.e, 2, 2)", fan)
        self.assertIn("fix (phase critic)", fan, "entities the phase critic names get one targeted fix")
        self.assertIn("critique(e, 1, 3)", fan)
        self.assertIn("phase_fixes", fan)
        sk = self.script("design-skeleton")
        for key in ("a.skeleton.critic_cmd", "a.skeleton.critic2_cmd", "skeleton.critic${order}", "skeleton.fix1", "result.verdicts = verdicts"):
            self.assertIn(key, sk)
        self.assertEqual(js_object_literal(sk, "CRITIC"), js_object_literal(fan, "CRITIC"))


class Wiring(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("workflows")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_begin_names_the_workflow_and_carries_both_phase_critics(self):
        self.c.reopen("P6", "prerolled")
        proc = self.c.run("designer.py", "phase", "P6", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertIn(out["workflow"], ("design-skeleton", "design-fanout"))
        self.assertIn("render phase_critic --attempt", out["phase_critic"]["prompt_cmd"])
        self.assertIn("--phase P6", out["phase_critic"]["prompt_cmd"], "an all-phase prompt is rendered for its phase (tuning birth 1)")
        self.assertIn("render wishes_critic", out["wishes_critic"]["prompt_cmd"])
        rendered = self.c.run("design_prompts.py", "render", "phase_critic", "--attempt", "1", "--phase", "P6", check=True).stdout
        self.assertIn("Phase P6", rendered)
        self.assertIn("rubric_p6", rendered.lower(), "the phase's own rubric rows, not only the three special ones")
        bare = self.c.run("design_prompts.py", "render", "phase_critic", "--attempt", "1")
        self.assertEqual(bare.returncode, 1)
        self.assertIn("pass --phase", bare.stderr)
        m = self.c.json("design/design.json")
        m["phases"]["P3"]["skeleton"] = {"status": "pending", "agent": None}   # the fixture's skeleton is merged; reset it
        m["phases"]["P3"]["status"] = "prerolled"
        self.c.path("design/design.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        proc = self.c.run("designer.py", "phase", "P3", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertEqual(out["workflow"], "design-skeleton", "a phase whose skeleton is pending starts with its skeleton")
        self.assertIn("render P3.skeleton", out["skeleton"]["prompt_cmd"])
        self.assertIn("render skeleton_critic --id skeleton", out["skeleton"]["critic_cmd"], "the skeleton has a critic (tuning birth 1)")
        rendered = self.c.path("design/_prompts/P3/skeleton.critic.md").read_text(encoding="utf-8")
        self.assertIn("Every count roll is honoured", rendered)
        self.assertIn("skeleton.critic1.json", rendered)

    def test_merge_records_critic_returns_saved_in_staging(self):
        staging = self.c.path("design/_staging/P6")
        ret = {"entity_id": "site_sunken_pier", "verdict": "pass", "findings": [
            {"rubric_id": "rubric_p6_only_here", "entity_id": "site_sunken_pier", "verdict": "pass"}]}
        (staging / "site_sunken_pier.critic2.json").write_text(json.dumps(ret), encoding="utf-8")
        wishes = {"entity_id": "P6", "verdict": "fix", "findings": [
            {"rubric_id": "rubric_wishes", "entity_id": "wish:must_not:1", "verdict": "fix", "reason_code": "prophecy_shape"}]}
        (staging / "wishes.critic1.json").write_text(json.dumps(wishes), encoding="utf-8")
        skel = {"entity_id": "skeleton", "verdict": "fix", "findings": [
            {"rubric_id": "rubric_skeleton_counts", "entity_id": "villagebatch_1", "verdict": "fix", "reason_code": "count_short"}]}
        (staging / "skeleton.critic1.json").write_text(json.dumps(skel), encoding="utf-8")
        proc = self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.assertIn("3 critic return(s) recorded", proc.stdout)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P6"]["critique"]["skeleton_verdicts"], ["fix"])
        self.assertTrue((staging / "merged" / "site_sunken_pier.critic2.json").is_file())
        m = self.c.json("design/design.json")
        recs = m["phases"]["P6"]["critique"]["records"]
        self.assertEqual({(r["entity_id"], r["critic"]) for r in recs[-3:]}, {("site_sunken_pier", 2), ("P6", 1), ("skeleton", 1)})
        self.assertEqual(m["phases"]["P6"]["critique"]["verdicts"][-1], "fix")


if __name__ == "__main__":
    unittest.main()
