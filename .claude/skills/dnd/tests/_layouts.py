"""
_layouts.py — throwaway project layouts for the path and hook tests.

Every test that touches root resolution or a PreToolUse hook builds one of
these in a temp dir, copies the real `paths.py` and hooks into it, and drives
them as subprocesses with a controlled environment. Nothing depends on the
machine's DND_* variables, on a session being open, or on any real campaign.

Layouts:
    make_project(base, name, ...)  <base>/<name>/.claude/skills/dnd + campaigns/ + .runtime/
                                   optionally with an active campaign, its session
                                   flag and its PCs
    make_plugin(base)              a skill copy whose `.claude/` ancestor carries no
                                   campaign data, i.e. not project-scoped
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCRIPTS = SKILL / "scripts"
HOOKS = ("dice_guard.py", "skill_edit_guard.py")


def clean_env(**overrides) -> dict:
    """The process env minus everything the skill or Claude Code could key on."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("DND_", "CLAUDE_"))}
    env.update({k: str(v) for k, v in overrides.items()})
    return env


def install_skill(skill_dir: Path) -> None:
    """Copy the real scripts under test into a layout's skill directory."""
    (skill_dir / "scripts" / "hooks").mkdir(parents=True)
    shutil.copy(SCRIPTS / "paths.py", skill_dir / "scripts" / "paths.py")
    for hook in HOOKS:
        shutil.copy(SCRIPTS / "hooks" / hook, skill_dir / "scripts" / "hooks" / hook)
    (skill_dir / "SKILL.md").write_text("# stub skill file\n", encoding="utf-8")


def skill_of(project: Path) -> Path:
    return project / ".claude" / "skills" / "dnd"


def add_campaign(project: Path, name: str, session: str = "open", pcs=()) -> Path:
    """A campaign folder with a state.md session flag and one sheet per PC."""
    cdir = project / "campaigns" / name
    (cdir / "characters").mkdir(parents=True)
    (cdir / "state.md").write_text(
        f"# Campaign: {name}\n\n## Session Flags\n- session_status: {session}\n",
        encoding="utf-8")
    for pc in pcs:
        (cdir / "characters" / f"{pc}.md").write_text(f"# {pc}\n", encoding="utf-8")
    return cdir


def make_project(base: Path, name: str, campaign: str = None,
                 session: str = "open", pcs=()) -> Path:
    """A project layout; with `campaign` it is also marked active, as /dm:dnd load does."""
    project = base / name
    install_skill(skill_of(project))
    (project / "campaigns").mkdir()
    (project / ".runtime").mkdir()
    if campaign:
        add_campaign(project, campaign, session, pcs)
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


def run_paths(skill: Path, verb: str, env: dict, *args: str) -> str:
    out = subprocess.run([sys.executable, str(skill / "scripts" / "paths.py"), verb, *args],
                         capture_output=True, text=True, env=env, check=True)
    return out.stdout.strip()


def run_hook(skill: Path, hook: str, payload: dict, env: dict) -> subprocess.CompletedProcess:
    """Run a hook the way Claude Code does: payload on stdin, verdict in the exit code."""
    return subprocess.run([sys.executable, str(skill / "scripts" / "hooks" / hook)],
                          input=json.dumps(payload), capture_output=True, text=True, env=env)


def edit_payload(path: Path, tool: str = "Edit") -> dict:
    return {"tool_name": tool, "tool_input": {"file_path": str(path)}}


def bash_payload(command: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": command}}


def same(a: str, b: Path) -> bool:
    return Path(a).resolve() == b.resolve()
