"""
test_design_read_guard.py — the read guard keys on agent_id and the marker.

Cases in both directions (plan item 22.1): the conductor is denied dm-only
while armed and free when unarmed; an allowed agent type reads dm-only; an
ad-hoc agent does not; Bash paths and the registry verbs that print dm-only;
another session's marker; playtest confines the player agent to the
allowlist and frees the DM; dice_guard refuses an agent's roll during birth.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from _layouts import bash_payload, clean_env, make_project, run_hook, skill_of

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "tuzlu-fener"
SESSION = "sess-A"


def payload(tool: str, agent: str | None = None, session: str = SESSION, **inp) -> dict:
    p = {"tool_name": tool, "tool_input": inp, "session_id": session, "transcript_path": "/x/y.jsonl"}
    if agent:
        p["agent_id"] = "a1b2c3"
        p["agent_type"] = agent
    return p


class ReadGuard(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dnd-read-guard-"))
        self.project = make_project(self.tmp, "proj")
        self.camp = self.project / "campaigns" / "tuzlu-fener"
        shutil.copytree(FIXTURE, self.camp)
        self.skill = skill_of(self.project)
        self.env = clean_env()
        self.dm_only = str(self.camp / "design" / "dm-only" / "npcs" / "npc_s01.md")
        self.public = str(self.camp / "design" / "npcs" / "npc_yesra.md")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def arm(self, mode="birth", session=SESSION, campaign="tuzlu-fener", **extra):
        marker = {"campaign": campaign, "mode": mode, "session_id": session, **extra}
        (self.project / ".runtime" / "active-design.json").write_text(json.dumps(marker), encoding="utf-8")

    def guard(self, p: dict) -> int:
        return run_hook(self.skill, "design_read_guard.py", p, self.env).returncode

    # --- unarmed / armed conductor -----------------------------------------

    def test_unarmed_everything_is_allowed(self):
        self.assertEqual(self.guard(payload("Read", file_path=self.dm_only)), 0)
        self.assertEqual(self.guard(bash_payload(f'cat "{self.dm_only}"') | {"session_id": SESSION}), 0)

    def test_armed_conductor_is_denied_dm_only_and_staging_but_not_public(self):
        self.arm()
        self.assertEqual(self.guard(payload("Read", file_path=self.dm_only)), 2)
        self.assertEqual(self.guard(payload("Read", file_path=str(self.camp / "design/_staging/P5/x.json"))), 2)
        self.assertEqual(self.guard(payload("Read", file_path=self.public)), 0)
        self.assertEqual(self.guard(payload("Grep", pattern="x", path=str(self.camp / "design" / "dm-only"))), 2)
        self.assertEqual(self.guard(payload("Grep", pattern="x", path=str(self.camp / "design"))), 0)

    def test_armed_conductor_bash_paths_and_registry_verbs(self):
        self.arm()
        proc = run_hook(self.skill, "design_read_guard.py",
                        payload("Bash", command=f'sed -n "1,20p" "{self.dm_only}"'), self.env)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("conductor", proc.stderr)
        self.assertNotIn("Nerun", proc.stderr)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c tuzlu-fener show npc_s01 --dm")), 2)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c tuzlu-fener export")), 2)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c tuzlu-fener export --public")), 0)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c tuzlu-fener show npc_yesra")), 0)
        self.assertEqual(self.guard(payload("Bash", command="py design_dice.py -c tuzlu-fener log --secret")), 2)
        self.assertEqual(self.guard(payload("Bash", command="py design_dice.py -c tuzlu-fener log")), 0)
        self.assertEqual(self.guard(payload("Bash", command="ls design/")), 0)

    # --- agents --------------------------------------------------------------

    def test_allowed_agent_type_reads_dm_only_and_others_do_not(self):
        self.arm()
        self.assertEqual(self.guard(payload("Read", agent="workflow-subagent", file_path=self.dm_only)), 0)
        self.assertEqual(self.guard(payload("Read", agent="design-writer", file_path=self.dm_only)), 0)
        self.assertEqual(self.guard(payload("Read", agent="general-purpose", file_path=self.dm_only)), 2)
        self.assertEqual(self.guard(payload("Read", agent="general-purpose", file_path=self.public)), 0)
        self.arm(agent_types_allowed=["my-writer"])
        self.assertEqual(self.guard(payload("Read", agent="workflow-subagent", file_path=self.dm_only)), 2)
        self.assertEqual(self.guard(payload("Read", agent="my-writer", file_path=self.dm_only)), 0)

    def test_another_sessions_marker_does_not_apply(self):
        self.arm(session="sess-B")
        self.assertEqual(self.guard(payload("Read", file_path=self.dm_only)), 0)
        self.arm(campaign="another")
        self.assertEqual(self.guard(payload("Read", file_path=self.dm_only)), 0, "marker for a campaign that is not this one")

    def test_detail_mode_arms_the_same_way(self):
        self.arm(mode="detail")
        self.assertEqual(self.guard(payload("Read", file_path=self.dm_only)), 2)
        self.assertEqual(self.guard(payload("Read", agent="workflow-subagent", file_path=self.dm_only)), 0)

    # --- playtest ------------------------------------------------------------

    def test_playtest_confines_the_player_agent_and_frees_the_dm(self):
        self.arm(mode="playtest", playtest_allowlist=["design/player-primer.md", "characters/"])
        self.assertEqual(self.guard(payload("Read", file_path=self.dm_only)), 0, "the DM reads freely")
        primer = str(self.camp / "design" / "player-primer.md")
        sheet = str(self.camp / "characters" / "Selen.md")
        self.assertEqual(self.guard(payload("Read", agent="player", file_path=primer)), 0)
        self.assertEqual(self.guard(payload("Read", agent="player", file_path=sheet)), 0)
        self.assertEqual(self.guard(payload("Read", agent="player", file_path=self.public)), 2)
        self.assertEqual(self.guard(payload("Read", agent="player", file_path=self.dm_only)), 2)
        self.assertEqual(self.guard(payload("Bash", agent="player", command="py registry.py -c tuzlu-fener export")), 2)
        self.assertEqual(self.guard(payload("Read", agent="workflow-subagent", file_path=self.dm_only)), 0)
        self.assertEqual(self.guard(payload("Read", agent="general-purpose", file_path=self.dm_only)), 2)


class DiceGuardDuringDesign(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dnd-dice-design-"))
        self.project = make_project(self.tmp, "proj", campaign="live", session="open", pcs=["Selen"])
        self.skill = skill_of(self.project)
        self.env = clean_env()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def roll(self, agent: str | None) -> int:
        p = bash_payload('py .claude/skills/dnd/scripts/dice.py d20 --owner "Bone Devil" --label "attack"')
        p["session_id"] = SESSION
        if agent:
            p["agent_id"] = "abc"
            p["agent_type"] = agent
        return run_hook(self.skill, "dice_guard.py", p, self.env).returncode

    def test_agents_never_roll_while_a_designer_run_is_armed(self):
        self.assertEqual(self.roll("workflow-subagent"), 0, "unarmed: an agent's NPC roll is fine")
        (self.project / ".runtime" / "active-design.json").write_text(
            json.dumps({"campaign": "live", "mode": "birth", "session_id": SESSION}), encoding="utf-8")
        self.assertEqual(self.roll("workflow-subagent"), 2)
        self.assertEqual(self.roll(None), 0, "the conductor still rolls (owner rules apply as ever)")
        (self.project / ".runtime" / "active-design.json").write_text(
            json.dumps({"campaign": "live", "mode": "playtest", "session_id": SESSION}), encoding="utf-8")
        self.assertEqual(self.roll("workflow-subagent"), 0, "playtest is not a designer run")


if __name__ == "__main__":
    unittest.main()
