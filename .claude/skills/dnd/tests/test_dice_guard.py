"""
test_dice_guard.py — cases for the dice-ownership PreToolUse hook.

The cases live in this file rather than on a command line on purpose: the hook
inspects raw Bash command text, so passing them as arguments would trip the
very guard under test.

Each case is (command, should_block, label). "should_block" is what the hook
must do with that command; the live failures from sessions 22-36 are in here as
regression cases, so a future refactor that quietly loosens the guard fails
loudly instead.

Self-contained: the hook runs from a throwaway project whose active campaign
carries the two PCs the regression cases name. Before this the four PC cases
only passed on a machine where Ashen Crown was the active campaign.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from _layouts import add_campaign, bash_payload, clean_env, make_project, run_hook, skill_of

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


class DiceGuard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="dnd-dice-guard-"))
        cls.project = make_project(cls.tmp, "table", campaign="live", session="open",
                                   pcs=["Kriv Shestendeliath", "Ilvaneth Duskmere"])
        # A second campaign in the same project, not the active one.
        add_campaign(cls.project, "shelved", session="closed", pcs=["Orsik Blackfell"])
        cls.skill = skill_of(cls.project)
        cls.env = clean_env()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def guard(self, command: str, skill: Path = None) -> int:
        proc = run_hook(skill or self.skill, "dice_guard.py", bash_payload(command), self.env)
        self.assertIn(proc.returncode, (0, 2), proc.stderr)
        return proc.returncode

    def test_cases(self):
        for command, should_block, label in CASES:
            with self.subTest(label):
                self.assertEqual(self.guard(command) == 2, should_block, label)

    def test_only_the_active_campaigns_pcs_count(self):
        """A PC of a campaign that is not loaded is not a player's die."""
        self.assertEqual(self.guard(f'{S} d20 --owner Orsik --label "initiative"'), 0)

    def test_without_an_active_campaign_no_owner_is_a_pc(self):
        """No marker, no PC list: the same command passes in a project with nothing loaded."""
        empty = make_project(self.tmp, "empty")
        self.assertEqual(self.guard(f'{S} d20+4 --owner Kriv --label "initiative"',
                                    skill=skill_of(empty)), 0)

    def test_other_tools_pass(self):
        proc = run_hook(self.skill, "dice_guard.py",
                        {"tool_name": "Read", "tool_input": {"file_path": "x.md"}}, self.env)
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
