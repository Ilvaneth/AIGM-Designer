"""
test_design_read_guard.py — the read guard keys on agent_id and the marker.

Cases in both directions (plan item 22.1): the conductor is denied dm-only
while armed and free when unarmed; an allowed agent type reads dm-only; an
ad-hoc agent does not; Bash paths and the registry verbs that print dm-only;
another session's marker; playtest confines the player agent to the
allowlist and frees the DM; dice_guard refuses an agent's roll during birth;
no search reaches dm-only through a parent folder (build 19d).
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from _layouts import bash_payload, clean_env, make_project, run_hook, skill_of

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "salt-lantern"
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
        self.camp = self.project / "campaigns" / "salt-lantern"
        shutil.copytree(FIXTURE, self.camp)
        self.skill = skill_of(self.project)
        self.env = clean_env()
        self.dm_only = str(self.camp / "design" / "dm-only" / "npcs" / "npc_s01.md")
        self.public = str(self.camp / "design" / "npcs" / "npc_yesra.md")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def arm(self, mode="birth", session=SESSION, campaign="salt-lantern", **extra):
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
        self.assertEqual(self.guard(payload("Grep", pattern="x", path=str(self.camp / "design" / "npcs"))), 0)
        self.assertEqual(self.guard(payload("Grep", pattern="x", path=str(self.camp / "design"))), 2,
                         "a parent folder with no filter reads inside dm-only (build 19d)")

    def test_armed_conductor_bash_paths_and_registry_verbs(self):
        self.arm()
        proc = run_hook(self.skill, "design_read_guard.py",
                        payload("Bash", command=f'sed -n "1,20p" "{self.dm_only}"'), self.env)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("conductor", proc.stderr)
        self.assertNotIn("Nerun", proc.stderr)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c salt-lantern show npc_s01 --dm")), 2)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c salt-lantern export")), 2)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c salt-lantern export --public")), 0)
        self.assertEqual(self.guard(payload("Bash", command="py registry.py -c salt-lantern show npc_yesra")), 0)
        self.assertEqual(self.guard(payload("Bash", command="py design_dice.py -c salt-lantern log --secret")), 2)
        self.assertEqual(self.guard(payload("Bash", command="py design_dice.py -c salt-lantern log")), 0)
        self.assertEqual(self.guard(payload("Bash", command="ls design/")), 0)

    def test_glob_is_guarded_on_its_path_and_pattern(self):
        self.arm()
        design, dm = str(self.camp / "design"), str(self.camp / "design" / "dm-only")
        self.assertEqual(self.guard(payload("Glob", pattern="**/*.md", path=dm)), 2)
        self.assertEqual(self.guard(payload("Glob", pattern="dm-only/**", path=design)), 2)
        self.assertEqual(self.guard(payload("Glob", pattern="campaigns/salt-lantern/design/dm-only/*")), 2)
        self.assertEqual(self.guard(payload("Glob", pattern="npcs/*.md", path=design)), 0)
        self.assertEqual(self.guard(payload("Glob", agent="design-critic", pattern="**/*.md", path=dm)), 0)
        self.assertEqual(self.guard(payload("Glob", agent="general-purpose", pattern="**/*.md", path=dm)), 2)

    def test_powershell_is_guarded_as_bash(self):
        self.arm()
        self.assertEqual(self.guard(payload("PowerShell", agent="design-writer", command=f'Get-Content "{self.dm_only}"')), 0)
        self.assertEqual(self.guard(payload("PowerShell", command=f'Get-Content "{self.dm_only}"')), 2)
        self.assertEqual(self.guard(payload("PowerShell", command="py registry.py -c salt-lantern export")), 2)
        self.assertEqual(self.guard(payload("PowerShell", command=f'Get-Content "{self.public}"')), 0)

    def test_a_command_naming_a_runtime_override_is_refused_while_armed(self):
        commands = ("AIGM_TEST_RUNTIME=/tmp/x py designer.py -c salt-lantern promise list --dm-only",
                    "export DND_RUNTIME_DIR=/tmp/x; py dice.py 1d20",
                    "env AIGM_TEST_RUNTIME=/tmp/x py design_dice.py -c salt-lantern log")
        self.assertEqual(self.guard(payload("Bash", command=commands[0])), 0, "unarmed: allowed")
        self.arm()
        for c in commands:
            proc = run_hook(self.skill, "design_read_guard.py", payload("Bash", command=c), self.env)
            self.assertEqual(proc.returncode, 2, c)
            self.assertIn("empty runtime", proc.stderr)
        ps = '$env:AIGM_TEST_RUNTIME = "C:/x"; py designer.py -c salt-lantern promise list --dm-only'
        self.assertEqual(self.guard(payload("PowerShell", command=ps)), 2)
        self.assertEqual(self.guard(payload("Bash", agent="design-writer", command=commands[0])), 2, "agents too")
        self.assertEqual(self.guard(payload("Bash", command=commands[0], session="sess-B")), 2, "any session")
        self.assertEqual(self.guard(payload("Bash", command="py designer.py -c salt-lantern promise list")), 0)
        self.arm(mode="playtest")
        self.assertEqual(self.guard(payload("Bash", command=commands[1])), 2, "the DM at the table too")

    # --- a search through a parent folder (build 19d) -------------------------

    def test_grep_and_glob_over_a_parent_folder_pass_only_when_their_filter_keeps_dm_only_out(self):
        self.arm()
        design, camp = str(self.camp / "design"), str(self.camp)
        grep = lambda **kw: self.guard(payload("Grep", pattern="x", **kw))  # noqa: E731
        glob = lambda **kw: self.guard(payload("Glob", **kw))  # noqa: E731
        self.assertEqual(grep(path=camp), 2)
        self.assertEqual(grep(path=design, glob="**"), 2)
        self.assertEqual(grep(path=design, glob="*.md"), 2, "a slashless glob matches at any depth")
        self.assertEqual(grep(path=design, type="md"), 2)
        self.assertEqual(grep(path=design, type="json"), 2, "dice-log.json")
        self.assertEqual(grep(path=design, glob="npcs/*.md"), 0)
        self.assertEqual(grep(path=design, glob="*.py"), 0)
        self.assertEqual(grep(path=design, type="py"), 0)
        self.assertEqual(grep(path=design, glob="!{dm-only,_staging}"), 0, "an exclusion of both folders")
        self.assertEqual(grep(path=design, glob="!dm-only/npcs/**"), 2, "an exclusion that leaves files in")
        self.assertEqual(glob(path=design, pattern="**/*.md"), 2)
        self.assertEqual(glob(path=design, pattern="dm-only/**"), 2)
        self.assertEqual(glob(path=design, pattern="*/*.json"), 2)
        self.assertEqual(glob(path=camp, pattern="design/*.md"), 0)
        self.assertEqual(glob(path=design, pattern="npcs/*.md"), 0)
        self.assertEqual(self.guard(payload("Grep", pattern="x") | {"cwd": str(self.project)}), 2, "no path: the working folder")
        self.assertEqual(self.guard(payload("Grep", pattern="x") | {"cwd": str(self.skill)}), 0)
        self.assertEqual(self.guard(payload("Glob", pattern="**/*.md") | {"cwd": str(self.project)}), 2)
        self.assertEqual(self.guard(payload("Grep", agent="design-critic", pattern="x", path=design)), 0)
        self.assertEqual(self.guard(payload("Glob", agent="workflow-subagent", pattern="**", path=camp)), 0)
        self.assertEqual(self.guard(payload("Grep", agent="general-purpose", pattern="x", path=design)), 2)
        self.arm(session="sess-B")
        self.assertEqual(grep(path=design), 0, "another session's marker")

    def test_the_guard_reads_command_words_not_text(self):
        """Build item 21b: a heredoc's body, a quoted string's body and a comment are text; a search command is still
        caught whatever text surrounds it."""
        self.arm()
        design = str(self.camp / "design")
        posix = design.replace("\\", "/")         # an unquoted path in Bash is written with forward slashes
        text = [("Bash", f'cat > notes.md <<\'EOF\'\nrun find "{design}" and grep -r foo "{design}"\nls -R "{design}"\nEOF\necho done'),
                ("Bash", f'cat <<-EOF > notes.md\n\tfind "{design}" -name x\n\tEOF'),
                ("Bash", f'echo "a; grep -r foo {design}" | head'),
                ("Bash", f"echo 'find {design} -name x'  # and ls -R {design}"),
                ("Bash", f'git commit -m "the guard now refuses grep -r over {design}"'),
                ("PowerShell", f"$t = @'\nGet-ChildItem -Recurse {design}\n'@\nWrite-Output $t"),
                ("PowerShell", f"Write-Output 'gci -Recurse {design}' # dir /s {design}")]
        for tool, command in text:
            self.assertEqual(self.guard(payload(tool, command=command)), 0, command)
        caught = [("Bash", f'cat > x.md <<EOF\nnotes\nEOF\ngrep -rn foo "{design}"'),
                  ("Bash", f'echo "found: $(grep -r foo {posix})"'),
                  ("Bash", f"x=`find {posix}`"),
                  ("Bash", f'echo "a" && ls -R "{design}" # a comment after'),
                  ("PowerShell", f"Write-Output 'x'; Get-ChildItem -Recurse {design}")]
        for tool, command in caught:
            self.assertEqual(self.guard(payload(tool, command=command)), 2, command)
        self.assertEqual(self.guard(payload("Bash", command=f'cat <<EOF\n{self.dm_only}\nEOF')), 2,
                         "a dm-only path is refused wherever it stands, a heredoc's body too")

    def test_the_guard_reads_inside_a_wrapper(self):
        """Build item 21c: a command string, a prefix, a grouping and a process substitution are read through to the
        command they wrap; an encoded PowerShell command is refused, since it cannot be read."""
        self.arm()
        design = str(self.camp / "design")
        d = design.replace("\\", "/")              # Bash paths, forward slashes
        refused = [("Bash", f'bash -c "grep -r x {d}"'), ("Bash", f"sh -c 'cd /tmp; ls -R {d}'"), ("Bash", f"zsh -c 'find {d}'"),
                   ("Bash", f"bash -lc 'find {d}'"), ("Bash", f'eval "find {d} -name x"'),
                   ("Bash", f"env FOO=1 grep -r x {d}"), ("Bash", f"env -u HOME FOO=1 find {d}"), ("Bash", f"sudo -u me find {d}"),
                   ("Bash", f"time ls -R {d}"), ("Bash", f"nohup grep -r x {d} &"), ("Bash", f"command find {d}"),
                   ("Bash", f"exec find {d}"), ("Bash", f"nice -n 5 ls -R {d}"), ("Bash", f"timeout 5 grep -r x {d}"),
                   ("Bash", f"echo a | xargs -n 1 grep -r x {d}"), ("Bash", f"( grep -r x {d} )"), ("Bash", f"(grep -r x {d})"),
                   ("Bash", f"{{ grep -r x {d}; }}"), ("Bash", f"diff <(ls -R {d}) notes.txt"), ("Bash", f"tee >(grep -r x {d}) < a"),
                   ("Bash", f'bash -c "sudo find {d}"'),
                   ("PowerShell", f'powershell -NoProfile -Command "Get-ChildItem -Recurse {design}"'),
                   ("PowerShell", f'pwsh -c "gci {design} -Recurse"'), ("PowerShell", f'Invoke-Expression "Get-ChildItem -Recurse {design}"'),
                   ("PowerShell", f"iex 'gci -Recurse {design}'"), ("PowerShell", f'cmd /c dir /s "{design}"'),
                   ("PowerShell", f"& {{ Get-ChildItem -Recurse {design} }}"), ("PowerShell", f". {{ gci -Recurse {design} }}"),
                   ("PowerShell", "powershell -EncodedCommand ZQBjAGgAbwAgAGgAaQA=")]
        for tool, command in refused:
            self.assertEqual(self.guard(payload(tool, command=command)), 2, command)
        passed = [("Bash", f"bash -c 'echo \"grep -r {d}\"'"), ("Bash", 'bash -c "echo hi"'), ("Bash", f"sudo ls {d}"),
                  ("Bash", f"env FOO=1 py designer.py -c salt-lantern status"), ("Bash", f"( cd {d}/npcs && ls )"),
                  ("PowerShell", f"powershell -Command \"Write-Output 'gci -Recurse {design}'\""),
                  ("PowerShell", f'pwsh -c "Get-ChildItem {design}"')]
        for tool, command in passed:
            self.assertEqual(self.guard(payload(tool, command=command)), 0, command)
        proc = run_hook(self.skill, "design_read_guard.py", payload("PowerShell", command="pwsh -ec ZQBjAGgAbwA="), self.env)
        self.assertIn("cannot be read", proc.stderr)
        self.assertEqual(self.guard(payload("PowerShell", agent="design-writer", command="pwsh -ec ZQBjAGgAbwA=")), 0, "a designer agent")

    def test_recursive_shell_searches_and_listings_over_a_parent_folder_are_refused(self):
        self.arm()
        design, camp, npcs = str(self.camp / "design"), str(self.camp), str(self.camp / "design" / "npcs")
        refused = [("Bash", f'grep -rn foo "{design}"'), ("Bash", f'grep -R foo "{camp}"'), ("Bash", f'rg foo "{design}"'),
                   ("Bash", f'find "{design}" -name "*.md"'), ("Bash", f'ls -R "{camp}"'), ("Bash", f'tree "{design}"'),
                   ("Bash", f'cd x; git grep foo -- "{camp}"'), ("Bash", f'echo a && grep -r foo "{design}" | head'),
                   ("PowerShell", f'Get-ChildItem -Recurse -Path "{design}"'), ("PowerShell", f"gci {design} -Rec -Filter *.md"),
                   ("PowerShell", f'Get-ChildItem "{design}" -Recurse | Select-String foo'),
                   ("PowerShell", f'findstr /s /i foo "{design}\\*.md"'), ("PowerShell", f'dir /s "{camp}"')]
        allowed = [("Bash", f'grep foo "{self.public}"'), ("Bash", f'ls "{design}"'), ("Bash", f'grep -rn foo "{npcs}"'),
                   ("Bash", f'rg foo "{self.skill}"'), ("PowerShell", f'Get-ChildItem "{design}"'),
                   ("PowerShell", f'Get-ChildItem -Recurse "{npcs}"'), ("Bash", "py designer.py -c salt-lantern status")]
        for tool, command in refused:
            proc = run_hook(self.skill, "design_read_guard.py", payload(tool, command=command), self.env)
            self.assertEqual(proc.returncode, 2, command)
            self.assertIn("may not search", proc.stderr)
        for tool, command in allowed:
            self.assertEqual(self.guard(payload(tool, command=command)), 0, command)
        self.assertEqual(self.guard(payload("Bash", command="rg foo") | {"cwd": str(self.project)}), 2, "no path: the working folder")
        self.assertEqual(self.guard(payload("Bash", command="rg foo") | {"cwd": str(self.skill)}), 0)
        self.assertEqual(self.guard(payload("Bash", agent="design-writer", command=f'grep -rn foo "{design}"')), 0)
        self.arm(mode="playtest", playtest_allowlist=["design/player-primer.md"])
        self.assertEqual(self.guard(payload("Bash", command=f'grep -rn foo "{design}"')), 0, "the DM at the table")
        self.assertEqual(self.guard(payload("Bash", agent="player", command=f'grep -rn foo "{design}"')), 2)
        self.assertEqual(self.guard(payload("Grep", agent="player", pattern="x", path=design)), 2)

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
        self.assertEqual(self.guard(payload("Bash", agent="player", command="py registry.py -c salt-lantern export")), 2)
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
