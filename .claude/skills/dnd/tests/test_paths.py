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

Each case builds a throwaway layout in a temp dir, copies the real paths.py and
hooks into it, and drives them as subprocesses with a controlled environment,
so nothing here depends on the machine's env or on any real campaign.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCRIPTS = SKILL / "scripts"

PC_NAME = "Kriv Shestendeliath"
ROLL_PC = 'py .claude/skills/dnd/scripts/dice.py d20+4 --owner Kriv --label "initiative"'


def clean_env() -> dict:
    """The process env minus everything the skill or Claude Code could key on."""
    return {k: v for k, v in os.environ.items()
            if not k.startswith(("DND_", "CLAUDE_"))}


def install_skill(skill_dir: Path) -> None:
    """Copy the real scripts under test into a layout's skill directory."""
    (skill_dir / "scripts" / "hooks").mkdir(parents=True)
    shutil.copy(SCRIPTS / "paths.py", skill_dir / "scripts" / "paths.py")
    for hook in ("dice_guard.py", "skill_edit_guard.py"):
        shutil.copy(SCRIPTS / "hooks" / hook, skill_dir / "scripts" / "hooks" / hook)
    (skill_dir / "SKILL.md").write_text("# stub skill file\n", encoding="utf-8")


def make_project(base: Path, name: str, campaign: str = None,
                 session: str = None, pcs=()) -> Path:
    """A project layout: <base>/<name>/.claude/skills/dnd + campaigns/ + .runtime/."""
    project = base / name
    install_skill(project / ".claude" / "skills" / "dnd")
    (project / "campaigns").mkdir()
    (project / ".runtime").mkdir()
    if campaign:
        cdir = project / "campaigns" / campaign
        (cdir / "characters").mkdir(parents=True)
        (cdir / "state.md").write_text(
            f"# Campaign: {campaign}\n\n## Session Flags\n- session_status: {session}\n",
            encoding="utf-8")
        for pc in pcs:
            (cdir / "characters" / f"{pc}.md").write_text(f"# {pc}\n", encoding="utf-8")
        (project / ".runtime" / "active-campaign.json").write_text(
            json.dumps({"name": campaign}), encoding="utf-8")
    return project


def make_plugin(base: Path) -> Path:
    """A non-project layout: a `.claude/` ancestor exists but carries no campaign data."""
    holder = base / "plugin-host"
    (holder / ".claude").mkdir(parents=True)
    skill = holder / "skills" / "dnd"
    install_skill(skill)
    return skill


def skill_of(project: Path) -> Path:
    return project / ".claude" / "skills" / "dnd"


def run_paths(skill: Path, verb: str, env: dict, *args: str) -> str:
    out = subprocess.run([sys.executable, str(skill / "scripts" / "paths.py"), verb, *args],
                         capture_output=True, text=True, env=env, check=True)
    return out.stdout.strip()


def run_hook(skill: Path, hook: str, payload: dict, env: dict) -> int:
    proc = subprocess.run([sys.executable, str(skill / "scripts" / "hooks" / hook)],
                          input=json.dumps(payload), capture_output=True, text=True, env=env)
    return proc.returncode


def edit_payload(path: Path) -> dict:
    return {"tool_name": "Edit", "tool_input": {"file_path": str(path)}}


def bash_payload(command: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": command}}


def same(a: str, b: Path) -> bool:
    return Path(a).resolve() == b.resolve()


class ProjectScopedRoot(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dnd-paths-"))
        self.decoy = self.tmp / "decoy-root"
        (self.decoy / ".runtime").mkdir(parents=True)
        self.leaked = clean_env()
        self.leaked["DND_CAMPAIGN_ROOT"] = str(self.decoy)
        self.leaked["DND_RUNTIME_DIR"] = str(self.decoy / "elsewhere")

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
        env = clean_env()
        env["DND_CAMPAIGN_ROOT"] = str(other)
        code = run_hook(skill_of(mine), "skill_edit_guard.py",
                        edit_payload(skill_of(mine) / "SKILL.md"), env)
        self.assertEqual(code, 0)

    def test_edit_guard_still_blocks_inside_its_own_open_session(self):
        other = make_project(self.tmp, "other", campaign="live", session="open")
        code = run_hook(skill_of(other), "skill_edit_guard.py",
                        edit_payload(skill_of(other) / "SKILL.md"), self.leaked)
        self.assertEqual(code, 2)

    def test_edit_guard_allows_inside_its_own_closed_session(self):
        other = make_project(self.tmp, "other", campaign="live", session="closed")
        code = run_hook(skill_of(other), "skill_edit_guard.py",
                        edit_payload(skill_of(other) / "SKILL.md"), self.leaked)
        self.assertEqual(code, 0)

    def test_edit_guard_outside_a_project_follows_the_environment(self):
        other = make_project(self.tmp, "other", campaign="live", session="open")
        plugin = make_plugin(self.tmp)
        env = clean_env()
        env["DND_CAMPAIGN_ROOT"] = str(other)
        code = run_hook(plugin, "skill_edit_guard.py", edit_payload(plugin / "SKILL.md"), env)
        self.assertEqual(code, 2)

    # --- the dice guard -----------------------------------------------------

    def test_dice_guard_reads_pc_names_from_its_own_project_only(self):
        other = make_project(self.tmp, "other", campaign="live", session="open", pcs=[PC_NAME])
        mine = make_project(self.tmp, "mine")
        env = clean_env()
        env["DND_CAMPAIGN_ROOT"] = str(other)
        self.assertEqual(run_hook(skill_of(mine), "dice_guard.py", bash_payload(ROLL_PC), env), 0)
        self.assertEqual(run_hook(skill_of(other), "dice_guard.py", bash_payload(ROLL_PC), env), 2)


if __name__ == "__main__":
    unittest.main()
