"""
test_paths.py — root resolution is project-scoped.

A copy of the skill inside a project (<project>/.claude/skills/dnd, the project
carrying `campaigns/` or `.runtime/`) uses that project as its data root and
ignores DND_CAMPAIGN_ROOT / DND_RUNTIME_DIR. Outside a project (a plugin or
standalone install) the environment decides, as before.

The regression behind this: the machine-wide DND_CAMPAIGN_ROOT pointed at the
Ashen Crown project, every hook subprocess inherited it, and the edit guard of
the Campaign Designer project read Ashen Crown's open session and blocked every
skill edit there.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from _layouts import (bash_payload, clean_env, edit_payload, install_skill, make_plugin,
                      make_project, run_hook, run_paths, same, skill_of)

PC_NAME = "Kriv Shestendeliath"
ROLL_PC = 'py .claude/skills/dnd/scripts/dice.py d20+4 --owner Kriv --label "initiative"'


class ProjectScopedRoot(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dnd-paths-"))
        self.decoy = self.tmp / "decoy-root"
        (self.decoy / ".runtime").mkdir(parents=True)
        self.leaked = clean_env(DND_CAMPAIGN_ROOT=self.decoy,
                                DND_RUNTIME_DIR=self.decoy / "elsewhere")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # --- resolution ---------------------------------------------------------

    def test_project_copy_ignores_the_environment(self):
        project = make_project(self.tmp, "proj")
        skill = skill_of(project)
        self.assertTrue(same(run_paths(skill, "project-root", self.leaked), project))
        self.assertTrue(same(run_paths(skill, "data-root", self.leaked), project))
        self.assertTrue(same(run_paths(skill, "runtime-dir", self.leaked), project / ".runtime"))
        self.assertTrue(same(run_paths(skill, "campaign-dir", self.leaked, "x"),
                             project / "campaigns" / "x"))

    def test_a_campaigns_folder_alone_scopes_the_project(self):
        project = self.tmp / "proj-c"
        install_skill(skill_of(project))
        (project / "campaigns").mkdir()
        self.assertTrue(same(run_paths(skill_of(project), "data-root", self.leaked), project))

    def test_a_runtime_folder_alone_scopes_the_project(self):
        project = self.tmp / "proj-r"
        install_skill(skill_of(project))
        (project / ".runtime").mkdir()
        self.assertTrue(same(run_paths(skill_of(project), "data-root", self.leaked), project))

    def test_a_claude_folder_without_campaign_data_does_not_scope(self):
        project = self.tmp / "proj-bare"
        install_skill(skill_of(project))
        self.assertEqual(run_paths(skill_of(project), "project-root", self.leaked), "none")
        self.assertTrue(same(run_paths(skill_of(project), "data-root", self.leaked), self.decoy))

    def test_outside_a_project_the_environment_decides(self):
        skill = make_plugin(self.tmp)
        self.assertEqual(run_paths(skill, "project-root", self.leaked), "none")
        self.assertTrue(same(run_paths(skill, "data-root", self.leaked), self.decoy))
        self.assertTrue(same(run_paths(skill, "runtime-dir", self.leaked),
                             self.decoy / "elsewhere"))

    def test_outside_a_project_without_env_the_default_holds(self):
        skill = make_plugin(self.tmp)
        self.assertTrue(same(run_paths(skill, "data-root", clean_env()),
                             Path("~/.claude/dnd").expanduser()))

    # --- the edit guard -----------------------------------------------------

    def test_edit_guard_ignores_another_projects_open_session(self):
        """The regression: a leaked root with an open session must not lock this project."""
        other = make_project(self.tmp, "other", campaign="live", session="open")
        mine = make_project(self.tmp, "mine")
        env = clean_env(DND_CAMPAIGN_ROOT=other)
        proc = run_hook(skill_of(mine), "skill_edit_guard.py",
                        edit_payload(skill_of(mine) / "SKILL.md"), env)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_edit_guard_still_blocks_inside_its_own_open_session(self):
        other = make_project(self.tmp, "other", campaign="live", session="open")
        proc = run_hook(skill_of(other), "skill_edit_guard.py",
                        edit_payload(skill_of(other) / "SKILL.md"), self.leaked)
        self.assertEqual(proc.returncode, 2)

    def test_edit_guard_allows_inside_its_own_closed_session(self):
        other = make_project(self.tmp, "other", campaign="live", session="closed")
        proc = run_hook(skill_of(other), "skill_edit_guard.py",
                        edit_payload(skill_of(other) / "SKILL.md"), self.leaked)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_edit_guard_outside_a_project_follows_the_environment(self):
        other = make_project(self.tmp, "other", campaign="live", session="open")
        plugin = make_plugin(self.tmp)
        env = clean_env(DND_CAMPAIGN_ROOT=other)
        proc = run_hook(plugin, "skill_edit_guard.py", edit_payload(plugin / "SKILL.md"), env)
        self.assertEqual(proc.returncode, 2)

    # --- the dice guard -----------------------------------------------------

    def test_dice_guard_reads_pc_names_from_its_own_project_only(self):
        other = make_project(self.tmp, "other", campaign="live", session="open", pcs=[PC_NAME])
        mine = make_project(self.tmp, "mine")
        env = clean_env(DND_CAMPAIGN_ROOT=other)
        self.assertEqual(run_hook(skill_of(mine), "dice_guard.py",
                                  bash_payload(ROLL_PC), env).returncode, 0)
        self.assertEqual(run_hook(skill_of(other), "dice_guard.py",
                                  bash_payload(ROLL_PC), env).returncode, 2)


if __name__ == "__main__":
    unittest.main()
