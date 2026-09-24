"""
test_skill_edit_guard.py — cases for the skill-edit PreToolUse hook.

Drives the real hook as a subprocess against throwaway project layouts, so the
cases depend neither on a session being open on this machine nor on any real
campaign. (The earlier version re-implemented the hook's decision in the test
and never ran main() at all.)

Each case is (target, session, unlocked, tool, should_block, label):
    target    skill | script | campaign | unrelated — which file the tool call touches
    session   open | closed | None — the active campaign's flag; None = nothing loaded
    unlocked  whether .runtime/allow-skill-edit exists
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from _layouts import clean_env, edit_payload, make_project, run_hook, skill_of

CASES = [
    ("skill",     "open",   False, "Edit",  True,  "skill file while a session is open"),
    ("script",    "open",   False, "Write", True,  "skill script while open"),
    ("skill",     "closed", False, "Edit",  False, "skill file in a dev tab (session closed)"),
    ("skill",     None,     False, "Edit",  False, "skill file with no campaign loaded"),
    ("skill",     "open",   True,  "Edit",  False, "skill file with the escape hatch set"),
    ("campaign",  "open",   False, "Edit",  False, "campaign file during play"),
    ("campaign",  "closed", False, "Edit",  False, "campaign file outside play"),
    ("unrelated", "open",   False, "Edit",  False, "unrelated file during play"),
    ("skill",     "open",   False, "Read",  False, "reading a skill file during play"),
]


class SkillEditGuard(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dnd-edit-guard-"))
        self.env = clean_env()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def layout(self, name: str, session, unlocked: bool) -> Path:
        project = make_project(self.tmp, name, campaign="live" if session else None,
                               session=session or "open")
        if unlocked:
            (project / ".runtime" / "allow-skill-edit").touch()
        return project

    def target(self, project: Path, kind: str) -> Path:
        skill = skill_of(project)
        return {
            "skill": skill / "SKILL.md",
            "script": skill / "scripts" / "factions.py",
            "campaign": project / "campaigns" / "live" / "state.md",
            "unrelated": self.tmp / "notes.md",
        }[kind]

    def test_cases(self):
        for i, (kind, session, unlocked, tool, should_block, label) in enumerate(CASES):
            with self.subTest(label):
                project = self.layout(f"case{i}", session, unlocked)
                proc = run_hook(skill_of(project), "skill_edit_guard.py",
                                edit_payload(self.target(project, kind), tool), self.env)
                self.assertIn(proc.returncode, (0, 2), proc.stderr)
                self.assertEqual(proc.returncode == 2, should_block, label)

    def test_block_message_points_at_the_dev_queue(self):
        project = self.layout("msg", "open", False)
        proc = run_hook(skill_of(project), "skill_edit_guard.py",
                        edit_payload(self.target(project, "skill")), self.env)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("dev-queue.md", proc.stderr)


if __name__ == "__main__":
    unittest.main()
