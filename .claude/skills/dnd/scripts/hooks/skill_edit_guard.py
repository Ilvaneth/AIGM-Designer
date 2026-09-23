#!/usr/bin/env python3
"""
skill_edit_guard.py — PreToolUse hook: no skill development during play.

Development inside a running session costs twice. The play tab's context fills
with refactoring instead of fiction, and the change gets made with the campaign
in view rather than the skill — which is how a general rule ends up written as
a campaign note, or a fix lands half-finished because a scene was waiting.

So the rule is: while a session is open, the skill is read-only. Findings go to
the campaign's dev-queue.md; the fixes happen after `/dm:dnd end`, in a fresh
tab whose whole context is the tool.

Blocks Edit/Write/NotebookEdit against <skill>/ when the active campaign's
state.md says `session_status: open`. Campaign files are never blocked — the
session needs to write those.

Escape hatch, for a script that breaks mid-play:
    touch .runtime/allow-skill-edit      (delete it when done)

Exit codes: 0 allow, 2 block (stderr is shown to Claude).
"""

import json
import os
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_SCRIPTS))

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def _runtime_dir() -> "Path | None":
    try:
        from paths import runtime_dir
        return Path(str(runtime_dir()))
    except Exception:
        return None


def _skill_root() -> Path:
    return SKILL_SCRIPTS.parent            # <...>/skills/dnd


def _active_campaign_state() -> "Path | None":
    """state.md of the campaign marked active at /dm:dnd load."""
    rt = _runtime_dir()
    if rt is None:
        return None
    marker = rt / "active-campaign.json"
    if not marker.is_file():
        return None
    try:
        name = json.loads(marker.read_text(encoding="utf-8")).get("name")
        if not name:
            return None
        from paths import find_campaign
        path = Path(str(find_campaign(name))) / "state.md"
        return path if path.is_file() else None
    except Exception:
        return None


def session_is_open() -> bool:
    state = _active_campaign_state()
    if state is None:
        return False                       # no campaign loaded: not a play tab
    try:
        text = state.read_text(encoding="utf-8")
    except OSError:
        return False
    m = re.search(r"session_status:\s*(\w+)", text)
    return bool(m and m.group(1).lower() == "open")


def _targets_skill(file_path: str) -> bool:
    if not file_path:
        return False
    try:
        target = Path(file_path).resolve()
    except Exception:
        return False
    skill = _skill_root().resolve()
    return skill == target or skill in target.parents


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") not in EDIT_TOOLS:
        sys.exit(0)

    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not _targets_skill(file_path):
        sys.exit(0)                        # campaign files are always writable

    rt = _runtime_dir()
    if rt is not None and (rt / "allow-skill-edit").exists():
        sys.exit(0)                        # explicitly unlocked for this fix

    if not session_is_open():
        sys.exit(0)                        # no session running: this is a dev tab

    name = Path(file_path).name
    print(
        f"BLOCKED by skill_edit_guard: a session is open, so {name} is read-only.\n"
        "  Skill development does not happen inside a play session — it fills the\n"
        "  play tab's context with refactoring, and the change gets written with the\n"
        "  campaign in view instead of the tool.\n"
        "  Do this instead: append the finding to the campaign's dev-queue.md (a\n"
        "  campaign file, still writable), finish the session, run /dm:dnd end, and\n"
        "  make the fix in a fresh tab that starts by reading that queue.\n"
        "  If a script is broken mid-play and the session cannot continue without a\n"
        "  fix: create .runtime/allow-skill-edit, make the fix, then delete it.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
