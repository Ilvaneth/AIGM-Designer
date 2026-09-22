#!/usr/bin/env python3
"""
test_dice_guard.py — cases for the dice-ownership PreToolUse hook.

Run:  python3 test_dice_guard.py

The cases live in this file rather than on a command line on purpose: the hook
inspects raw Bash command text, so passing them as arguments would trip the
very guard under test.

Each case is (command, should_block, label). "should_block" is what the hook
must do with that command; the live failures from sessions 22-36 are in here as
regression cases, so a future refactor that quietly loosens the guard fails
loudly instead.
"""

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parent / "dice_guard.py"
S = "py .claude/skills/dnd/scripts/dice.py"

CASES = [
    # --- must be blocked: dice that belong to a player -----------------------
    (f'{S} d20+9 --owner "Kriv" --label "CON save vs poison DC16"', True,
     "session 36: PC saving throw rolled inside an NPC multiattack"),
    (f'{S} 3d12 --owner "Ilvaneth Duskmere" --label "Toll the Dead damage"', True,
     "session 35: PC cantrip damage rolled after the NPC's save"),
    (f'{S} d10 --owner "Kriv Shestendeliath" --label "level-up hit die"', True,
     "session 33: level-up hit die rolled for the player"),
    (f'{S} d20+4 --owner kriv --label "initiative"', True,
     "PC initiative, lowercase first name"),

    # --- must be blocked: no owner named, or no script at all ----------------
    (f'{S} 3d12 --label "Toll the Dead damage"', True, "dice.py with no --owner"),
    ('py -c "import random; print(random.randint(1,20))"', True, "inline python random"),
    ('echo $((RANDOM % 20 + 1))', True, "$RANDOM"),
    ('shuf -i 1-20 -n 1', True, "shuf -i"),

    # --- must pass: the DM's own dice ----------------------------------------
    (f'{S} d20+8 --owner "Bone Devil" --label "Sting vs Kriv AC22"', False, "NPC attack"),
    (f'{S} 5d6 --owner "Bone Devil" --label "Sting poison damage"', False, "NPC damage"),
    (f'{S} 4d6 --owner trap --label "Falling rocks onto Kriv"', False,
     "environmental damage arriving at a PC"),
    (f'{S} d100 --owner table --label "wild magic surge"', False, "random table"),
    (f'{S} d20 adv --owner "Erinyes" --label "WIS save"', False, "NPC save with advantage"),

    # --- must pass: not a roll at all ----------------------------------------
    ('git commit -m "docs: dice.py now requires --owner for every roll"', False,
     "commit message that mentions dice.py"),
    ('grep -n "dice.py d20" SKILL-scripts.md', False, "grep for a documented example"),
    (f'{S} --help', False, "help output"),
    ('ls -la campaigns/', False, "unrelated command"),
    ('git commit -m "hook: block $RANDOM and shuf -i as dice sources"', False,
     "commit message quoting a blocked construct"),
    ('git commit -F - <<\'EOF\'\nDocs: dice.py 3d12 --label x rolled a PC die in session 35\nEOF',
     False, "heredoc body describing a blocked call"),
    ('cat > notes.md <<\'EOF\'\nUse $RANDOM? No: dice.py d20 --owner "Goblin"\nEOF',
     False, "heredoc writing documentation about dice"),
    ('py .claude/skills/dnd/scripts/tracker.py -c ashen-crown turn "Kriv Shestendeliath"',
     False, "tracker turn for a PC"),
]


def main() -> int:
    failures = 0
    for command, should_block, label in CASES:
        result = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}),
            capture_output=True, text=True,
        )
        blocked = result.returncode == 2
        ok = blocked == should_block
        failures += not ok
        verdict = "ok  " if ok else "FAIL"
        expected = "block" if should_block else "pass "
        print(f"  [{verdict}] expected {expected} — {label}")
        if not ok and result.stderr:
            print(f"         {result.stderr.strip()[:160]}")

    total = len(CASES)
    print(f"\n  {total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
