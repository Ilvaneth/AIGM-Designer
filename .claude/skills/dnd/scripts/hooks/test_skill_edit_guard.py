#!/usr/bin/env python3
"""
test_skill_edit_guard.py — cases for the skill-edit PreToolUse hook.

Run:  python3 test_skill_edit_guard.py

Drives the guard's decision function directly with a faked session state, so
the cases do not depend on whether a session happens to be open right now.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import skill_edit_guard as guard  # noqa: E402

SKILL = guard._skill_root()
CAMPAIGN_FILE = SKILL.parent.parent.parent / "campaigns" / "ashen-crown" / "state.md"

CASES = [
    # (file path, session open?, unlocked?, should_block, label)
    (SKILL / "SKILL.md", True, False, True, "skill file while a session is open"),
    (SKILL / "scripts" / "factions.py", True, False, True, "skill script while open"),
    (SKILL / "SKILL.md", False, False, False, "skill file in a dev tab (session closed)"),
    (SKILL / "SKILL.md", True, True, False, "skill file with the escape hatch set"),
    (CAMPAIGN_FILE, True, False, False, "campaign file during play"),
    (CAMPAIGN_FILE, False, False, False, "campaign file outside play"),
    (Path("C:/tmp/notes.md"), True, False, False, "unrelated file during play"),
]


def decide(path, is_open, unlocked) -> bool:
    """Reproduce main()'s decision without touching stdin or the real state."""
    if not guard._targets_skill(str(path)):
        return False
    if unlocked:
        return False
    return is_open


def main() -> int:
    failures = 0
    for path, is_open, unlocked, should_block, label in CASES:
        blocked = decide(path, is_open, unlocked)
        ok = blocked == should_block
        failures += not ok
        print(f"  [{'ok  ' if ok else 'FAIL'}] expected "
              f"{'block' if should_block else 'pass '} — {label}")
    print(f"\n  {len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
