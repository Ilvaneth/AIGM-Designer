"""
test_dry_run.py — slice 1e, the dry run and the playtest (plan item 22.2-22.5): the automated leak scan
over every conductor-visible artifact; two births compared (names, unique-table rows, map, roster); the
load budget; the playtest harness (persona, transcript, the player agent's prompt and allowlist, the
player's own dice under the guards, the judges' prompts and records); P9's read lists and thread faces.
"""

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, MarkerGuard, SCRIPTS, PROJECT
from _layouts import run_hook, bash_payload

sys.path.insert(0, str(SCRIPTS))

from paths import runtime_dir  # noqa: E402


def payload(tool: str, agent: str | None = None, **inp) -> dict:
    p = {"tool_name": tool, "tool_input": inp, "session_id": "sess-dry", "transcript_path": "/x/y.jsonl"}
    if agent:
        p["agent_id"] = "a1b2c3"
        p["agent_type"] = agent
    return p


class LeakScan(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("leak")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_a_clean_bible_passes_and_a_planted_sentence_is_found_without_being_printed(self):
        proc = self.c.run("design_leak_scan.py", check=True)
        self.assertIn("CLEAN", proc.stdout)
        import design_approval as da
        _, sentences = da.secret_terms(self.c.name)
        sentence = max(sentences, key=len)
        world = self.c.path("world.md")
        world.write_text(world.read_text(encoding="utf-8") + "\n" + sentence + "\n", encoding="utf-8")
        proc = self.c.run("design_leak_scan.py")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("world.md", proc.stdout)
        self.assertIn("dm-only sentence", proc.stdout)
        self.assertNotIn(sentence[:30], proc.stdout, "a hit is reported by length, never by text")
        out = json.loads(self.c.run("design_leak_scan.py", "--json").stdout)
        self.assertGreaterEqual(out["hits"], 1)
        world.write_text(world.read_text(encoding="utf-8").replace(sentence, ""), encoding="utf-8")
        prompts = self.c.path("design/_prompts/P1")
        prompts.mkdir(parents=True, exist_ok=True)
        (prompts / "premise.md").write_text("## Secret\n\nthe rendered instructions say the word\n", encoding="utf-8")
        self.assertEqual(self.c.run("design_leak_scan.py").returncode, 0, "rendered prompts are not artifacts (dry run 1: 76 false hits)")
        self.assertEqual([r["file"] for r in out["results"]], ["world.md"], "one artifact leaks, and it is the one we planted in")


class ValidatorAfterDryRun(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("val1")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_map_only_links_resolve_and_generated_files_need_no_front_matter(self):
        f = self.c.path("design/factions/faction_reedmarch.md")
        f.write_text(f.read_text(encoding="utf-8") + "\n- Dalgakıran: [[landmark_broken_breakwater]] (haritada bir simge yer).\n", encoding="utf-8")
        self.c.run("render_dm.py", "index", "report", check=True)
        self.c.run("map_travel.py", "travel-times", check=True)
        findings = json.loads(self.c.run("design_check.py", "--modules", "refs,secrecy", "--json", check=True).stdout)
        self.assertFalse([x for x in findings if x["code"] in ("dangling_link", "dangling_ref") and "landmark_" in x["message"]])
        self.assertFalse([x for x in findings if x["code"] == "file_no_secrecy" and any(g in x["message"] for g in ("index.md", "report.md", "travel-times.md"))])


class Compare(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.a = TestCampaign("cmp-a")
        self.b = TestCampaign("cmp-b")

    def tearDown(self):
        self.a.remove()
        self.b.remove()
        self.guard.__exit__(None, None, None)

    def test_the_same_birth_twice_is_not_distinct_and_the_premises_are_printed_for_the_judge(self):
        proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "design_compare.py"), self.a.name, self.b.name],
                              capture_output=True, text=True, env=self.a.env, encoding="utf-8")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("NOT DISTINCT", proc.stdout)
        self.assertIn("names          ", proc.stdout)
        self.assertIn("premises for the judge", proc.stdout)
        self.assertIn("Salt Lantern", proc.stdout)
        out = json.loads(subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "design_compare.py"), self.a.name, self.b.name, "--json"],
                                        capture_output=True, text=True, env=self.a.env, encoding="utf-8").stdout)
        self.assertFalse(out["distinct"])
        self.assertTrue(out["shared_names"])
        self.assertEqual(out["verdicts"]["map"], "IDENTICAL SHAPE")
        self.assertIn("gods", out["premises"]["a"])


class LoadBudget(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("budget")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_the_fixture_is_light_and_a_tiny_budget_trips(self):
        proc = self.c.run("load_budget.py", check=True)
        self.assertIn("under budget", proc.stdout)
        for item in ("designer load-pack", "chapter chapter_1", "thread thread_selen", "character Selen", "npcs.md (index rows)"):
            self.assertIn(item, proc.stdout, item)
        over = self.c.run("load_budget.py", "--budget-tokens", "100")
        self.assertEqual(over.returncode, 1)
        self.assertIn("OVER BUDGET", over.stdout)


class Playtest(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("playtest")
        self.active = runtime_dir() / "active-campaign.json"
        self.active_backup = self.active.read_bytes() if self.active.is_file() else None
        self.active.write_text(json.dumps({"name": self.c.name}), encoding="utf-8")

    def tearDown(self):
        self.c.remove()
        if self.active_backup is not None:
            self.active.write_bytes(self.active_backup)
        elif self.active.is_file():
            self.active.unlink()
        self.guard.__exit__(None, None, None)

    def dice(self, *args):
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "dice.py"), *args], capture_output=True, text=True,
                              env=self.c.env, encoding="utf-8")

    def hook(self, name, p):
        return run_hook(SCRIPTS.parent, name, p, self.c.env).returncode

    def test_the_harness_from_start_to_judges(self):
        proc = self.c.run("playtest.py", "start", "--pc", "Selen", "--persona", "Temkinli, borcunu ödemek isteyen bir hırsız; az konuşur, çok bakar.", check=True)
        self.assertIn("guard armed in playtest mode", proc.stdout)
        marker = json.loads((runtime_dir() / "active-design.json").read_text(encoding="utf-8"))
        self.assertEqual(marker["mode"], "playtest")
        self.assertIn("characters/Selen.md", marker["playtest_allowlist"])
        self.assertIn("playtest/transcript.md", marker["playtest_allowlist"])
        self.assertEqual(marker["playtest_agent_types"], ["player"])
        self.assertTrue(self.c.path("playtest/persona.md").is_file())
        # the player agent may read its files and nothing else; the DM reads freely
        sheet = str(self.c.path("characters/Selen.md"))
        dossier = str(self.c.path("design/npcs/npc_sarven.md"))
        self.assertEqual(self.hook("design_read_guard.py", payload("Read", "player", file_path=sheet)), 0)
        self.assertEqual(self.hook("design_read_guard.py", payload("Read", "player", file_path=dossier)), 2)
        self.assertEqual(self.hook("design_read_guard.py", payload("Read", None, file_path=dossier)), 0)
        # the player's own die: dice.py --player passes while the playtest is armed, the DM's roll of a PC die never does
        ok = self.dice("d20", "--owner", "Selen", "--player", "--campaign", self.c.name, "--silent")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertTrue(ok.stdout.strip().isdigit())
        self.assertEqual(self.dice("d20", "--owner", "Selen", "--campaign", self.c.name).returncode, 3)
        cmd = f'py -X utf8 {SCRIPTS.as_posix()}/dice.py d20 --owner "Selen" --player --campaign {self.c.name}'
        self.assertEqual(self.hook("dice_guard.py", dict(bash_payload(cmd), agent_id="a1", agent_type="player", session_id="s")), 0)
        self.assertEqual(self.hook("dice_guard.py", dict(bash_payload(cmd.replace(" --player", "")), agent_id="a1", agent_type="player", session_id="s")), 2)
        self.assertEqual(self.hook("dice_guard.py", dict(bash_payload(cmd), agent_id="a1", agent_type="general-purpose", session_id="s")), 2)
        self.assertEqual(self.hook("dice_guard.py", bash_payload(cmd)), 2, "the DM may not use --player")
        # turns and the prompt
        proc = self.c.run("playtest.py", "turn", "--dm", "Weary Gull'un ocağı sönmek üzere; Tolvan tezgâhın ardından sana bakıyor. Ne yaparsın?", check=True)
        self.assertIn("turn 1", proc.stdout)
        self.assertIn("--player", proc.stdout)
        self.assertIn("characters/Selen.md", proc.stdout)
        self.assertIn("message_tr", proc.stdout)
        self.assertNotIn("{{", proc.stdout)
        self.c.run("playtest.py", "turn", "--player", "Tolvan'a başımla selam verir, tezgâha yaslanırım. \"Sandık işi. Anlat.\"", check=True)
        text = self.c.path("playtest/transcript.md").read_text(encoding="utf-8")
        self.assertIn("## Tur 1", text)
        self.assertIn("**DM:** Weary Gull", text)
        self.assertIn("**Selen:** Tolvan", text)
        prompt = self.c.run("playtest.py", "prompt", check=True).stdout
        self.assertIn("playtest/transcript.md", prompt)
        # the judges
        j = self.c.run("playtest.py", "judge", "playtest", check=True).stdout
        for check in ("opening_bang", "dice_ownership", "no_leak", "calendar_advanced"):
            self.assertIn(check, j)
        self.assertNotIn("{{", j)
        r = self.c.run("playtest.py", "judge", "readability", check=True).stdout
        self.assertIn("design/chapters/chapter_1.md", r)
        self.assertIn("design/sites/site_sunken_pier.md", r)
        ret = self.c.path("playtest/judge-return.json")
        ret.write_text(json.dumps({"kind": "playtest", "verdict": "fix", "findings": [
            {"check": "opening_bang", "verdict": "pass"}, {"check": "calendar_advanced", "verdict": "fix", "turn": 3, "note_tr": "Saat ilerlemedi."}]}), encoding="utf-8")
        rec = self.c.run("playtest.py", "judge", "playtest", "--record", str(ret), check=True)
        self.assertIn("1 not passed", rec.stdout)
        self.assertTrue(self.c.path("playtest/judge-playtest.json").is_file())
        status = self.c.run("playtest.py", "status", check=True).stdout
        self.assertIn("1 turn(s)", status)
        self.assertIn("judge playtest: fix", status)
        stop = self.c.run("playtest.py", "stop", check=True)
        self.assertIn("disarmed", stop.stdout)
        self.assertEqual(self.dice("d20", "--owner", "Selen", "--player", "--campaign", self.c.name).returncode, 3, "no playtest, no --player")
        self.assertTrue((PROJECT / ".claude" / "agents" / "player.md").is_file(), "the player agent type the Agent tool spawns")

    def test_uniqueness_judge_prompt_carries_both_premises(self):
        other = TestCampaign("playtest-b")
        try:
            j = self.c.run("playtest.py", "judge", "uniqueness", "--against", other.name, check=True).stdout
            self.assertIn("[a] Salt Lantern", j)
            self.assertIn("[b] Salt Lantern", j)
            self.assertIn("same_campaign", j)
            self.assertNotIn("{{", j)
        finally:
            other.remove()


class Integrate(unittest.TestCase):
    """P9, design integrate: the thread writer reads the PC's sheet and the sockets' people; the merge renders the faces."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("p9")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_thread_reads_and_thread_faces(self):
        m = self.c.json("design/design.json")
        m["entities"]["thread_selen"] = {"phase": "P9", "status": "pending", "attempt": 2, "rerun": True, "critique_loops": 0,
                                         "last_error": None, "file": None, "stage_file": None, "agent": None}
        m["phases"]["P9"]["status"] = "prerolled"
        m["phases"]["P9"]["roster"] = ["thread_selen", "doc_session1"]
        self.c.write_json("design/design.json", m)
        proc = self.c.run("designer.py", "phase", "P9", "begin", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        thread = next(e for e in out["entities"] if e["id"] == "thread_selen")
        for f in ("characters/Selen.md", "design/arc.md", "design/factions/faction_tide_brotherhood.md", "design/npcs/npc_tolvan.md"):
            self.assertIn(f, thread["files"], f)
        pack = next(e for e in out["entities"] if e["id"] == "doc_session1")
        for f in ("design/settlements/settlement_lanternside.md", "design/chapters/chapter_1.md", "design/sites/site_sunken_pier.md", "design/news.json"):
            self.assertIn(f, pack["files"], f)
        self.assertIn("render P9.thread --id thread_selen", thread["prompt_cmd"])
        self.c.reopen("P9", "partial", roster=[])
        self.c.run("designer.py", "phase", "P9", "merge", check=True)
        self.assertTrue(self.c.path("design/player/thread_selen.md").is_file(), "the thread's public face is rendered at P9's merge")
        self.assertTrue(self.c.path("design/index.md").is_file())


if __name__ == "__main__":
    unittest.main()
