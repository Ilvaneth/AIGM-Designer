"""
test_p1_critics.py — build item 14c (docs/p1-build-14.md, Part 14c): the critics know the rolls. For P1 of a new
birth the rendered critic prompts offer no `rerun` and name the records they read; `design_approval.py critique`
refuses a P1 return that says `rerun` (a legacy birth's is recorded as before). The naming rubric is the second net
behind the door, the cliché rubric is gone, and the age row's hint lost its first example.

  py test_p1_critics.py --words     the rendered P1 critic prompts' length in words
"""

import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign

sys.path.insert(0, str(SCRIPTS))
import design_prompts as dpm  # noqa: E402
import design_tables as dt  # noqa: E402

RECORDS = ("`design/design.json#foundation` and `#identity`", "the signature candidates in `design/naming.json`",
           "the secret identity record too (`design/dm-only/dice-log.json`, under `identity`)")


def run(script, *args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


class NewBirth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        cls.name = f"_test-critics-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run("designer.py", "new", cls.name, "--party-size", "2", "--seed", "CRITICS-0001", "--lang", "tr", "--scale", "standard")
        run("designer.py", "-c", cls.name, "preroll", "--phase", "P1")
        slug = cls.name.replace("-", "_")
        cls.entity = dpm.render(cls.name, "critic", f"premise_{slug}", phase_override="P1")
        cls.phase = dpm.render(cls.name, "phase_critic", phase_override="P1")
        cls.wishes = dpm.render(cls.name, "wishes_critic", phase_override="P1")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CAMPAIGNS / cls.name, ignore_errors=True)
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def test_a_p1_critic_is_offered_no_rerun_and_is_told_why(self):
        for name, text in (("critic", self.entity), ("phase_critic", self.phase)):
            self.assertIn("give a verdict: `pass`, `fix` (a targeted change would repair it) or `note`", text, name)
            self.assertIn("There is no `rerun` here: the rolls are sealed and only the owner rerolls", text, name)
            self.assertIn("The overall verdict is `fix` if any row says fix, else `pass`.", text, name)
            self.assertNotIn("the entity is wrong at the root", text, name)
            self.assertNotIn("`rerun` if any row says rerun", text, name)
            self.assertIn("**Craft only.**", text, name)
            self.assertNotIn("{{", text)
        for name, text in (("critic", self.entity), ("phase_critic", self.phase), ("wishes_critic", self.wishes)):
            self.assertIn('"enum": ["pass", "fix"]', text, name)
            self.assertIn('"enum": ["pass", "fix", "note"]', text, name)
            self.assertNotIn('"rerun"', text, f"{name}: the return schema offers no rerun")

    def test_the_critics_are_told_what_was_rolled(self):
        for name, text in (("critic", self.entity), ("phase_critic", self.phase)):
            for needle in RECORDS:
                self.assertIn(needle, text, f"{name}: {needle}")
            self.assertIn("so that you judge what the writer made of it and never the rolls", text)
        self.assertIn("P1 has no skeleton. You read the premise (`design/premise.md`), its mirror when a rubric's scope is dm-only, the three "
                      "signature rows and the break rows", self.phase)
        self.assertNotIn("skeleton.json", self.phase)
        self.assertNotIn("cliché", self.phase)
        self.assertIn("### Earlier campaigns", self.phase + "### Earlier campaigns", "the block stays with the critics when another birth exists")

    def test_a_p1_return_that_says_rerun_is_refused(self):
        staging = CAMPAIGNS / self.name / "design/_staging/P1"
        staging.mkdir(parents=True, exist_ok=True)
        for n, ret in enumerate(({"entity_id": "P1", "verdict": "rerun", "findings": []},
                                 {"entity_id": "P1", "verdict": "fix", "findings": [{"rubric_id": "rubric_p1_question_concrete", "entity_id": "P1", "verdict": "rerun"}]})):
            f = staging / f"phase.critic1.loop{n + 2}.json"
            f.write_text(json.dumps(ret), encoding="utf-8")
            proc = run("design_approval.py", "-c", self.name, "critique", "--phase", "P1", "--file", str(f), check=False)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("a P1 critic return says `rerun`, refused", proc.stderr)
        ok = staging / "phase.critic1.json"
        ok.write_text(json.dumps({"entity_id": "P1", "verdict": "fix", "findings": [{"rubric_id": "rubric_p1_question_concrete", "entity_id": "P1", "verdict": "fix", "reason_code": "abstract_pair"}]}), encoding="utf-8")
        self.assertEqual(run("design_approval.py", "-c", self.name, "critique", "--phase", "P1", "--file", str(ok)).returncode, 0)


class LegacyAndRubrics(unittest.TestCase):

    def test_a_legacy_birth_and_the_other_phases_keep_the_three_verdicts(self):
        guard = MarkerGuard().__enter__()
        c = TestCampaign("critics")
        try:
            for name, eid, phase in (("critic", "premise_salt_lantern", "P1"), ("phase_critic", None, "P1"), ("phase_critic", None, "P6")):
                text = dpm.render(c.name, name, eid, phase_override=phase)
                self.assertIn("`rerun` (the entity is wrong at the root)", text, f"{name} {phase}")
                self.assertIn('"enum": ["pass", "fix", "rerun"]', text)
            self.assertIn(f"you read the phase's skeleton (`design/_staging/P6/skeleton.json`", dpm.render(c.name, "phase_critic", phase_override="P6"))
            c.reopen("P1", "merged")
            f = c.path("design/_staging/P1/phase.critic1.json")
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps({"entity_id": "P1", "verdict": "rerun", "findings": []}), encoding="utf-8")
            proc = c.run("design_approval.py", "critique", "--phase", "P1", "--file", str(f))
            self.assertEqual(proc.returncode, 0, "a legacy birth's rerun is recorded as before")
        finally:
            c.remove()
            guard.__exit__(None, None, None)

    def test_the_naming_rubric_is_the_second_net_and_the_cliche_rubric_is_gone(self):
        special = {r["id"]: r for r in dt.rows("rubrics.yaml#special")}
        naming = special["rubric_english_names"]
        self.assertEqual(naming["question"], "Is every proper noun one the pools gave: a signature candidate, a stock name, or a name composed from pooled parts? "
                                             "Look also where the door cannot: a name that opens a sentence, a heading or a list item.")
        self.assertEqual(naming["fails_when"], "a name stands in the text that no pool holds")
        self.assertNotIn("rubric_cliche", special)
        skill = SCRIPTS.parent
        files = [p for pat in ("data/design/*", "scripts/*.py", "prompts/design/*.md", "prompts/play/*.md", "templates/design/*.md", "SKILL*.md")
                 for p in sorted(skill.glob(pat)) if p.is_file()] + sorted((skill.parents[1] / "workflows").glob("*.js"))
        for p in files:
            text = p.read_text(encoding="utf-8", errors="replace")
            self.assertNotIn("rubric_cliche", text, p.name)
            self.assertNotIn("saving detail", text, p.name)
        self.assertNotIn("cliché", (skill / "SKILL-design.md").read_text(encoding="utf-8"))
        lines = dpm.rubric_lines("P3", None, 1)
        self.assertIn("rubric_english_names", lines)
        self.assertIn("rubric_leak", lines)

    def test_the_age_rows_hint(self):
        row = dt.row("history.yaml#age_template", "age_of_thing")
        self.assertEqual(row["span_hint"], "an age named for what was built in it (roads, walls, mills)")
        self.assertEqual(row["label"], "The Age of {Thing}")


if __name__ == "__main__":
    if "--words" in sys.argv:
        NewBirth.setUpClass()
        try:
            for name in ("entity", "phase", "wishes"):
                print(f"{name} critic: {len(getattr(NewBirth, name).split())} words")
        finally:
            NewBirth.tearDownClass()
    else:
        unittest.main()
