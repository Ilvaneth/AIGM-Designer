"""
test_design_manifest.py — design_manifest.py: init, reconcile from disk,
pending with read budgets, mark, approve, stale, tokens, logs, mode.
"""

import json
import shutil
import unittest
from pathlib import Path

from _campaign import TestCampaign, CAMPAIGNS, SCRIPTS
import os
import subprocess
import sys
import uuid


class FreshCampaign(unittest.TestCase):
    """init on an empty campaign folder."""

    def setUp(self):
        self.name = f"_test-manifest-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        self.dir = CAMPAIGNS / self.name
        self.dir.mkdir(parents=True)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_m(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "design_manifest.py"), "-c", self.name, *args],
                              capture_output=True, text=True, env=self.env, encoding="utf-8")

    def test_init_creates_the_tree_and_a_manifest_with_a_derived_arc(self):
        proc = self.run_m("init", "--scale", "short", "--tone", "horror", "--magic", "low", "--era", "nautical",
                          "--danger", "gritty", "--party-size", "2", "--content-mix", "mystery,exploration,politics",
                          "--must", "deniz", "--must-not", "kehanet", "--seed", "TT-00000001")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        m = json.loads((self.dir / "design" / "design.json").read_text(encoding="utf-8"))
        self.assertEqual(m["_meta"]["mode"], "birth")
        self.assertEqual(m["dials"]["level_band"], [1, 5])
        self.assertEqual(m["dials"]["wishes"], {"must": ["deniz"], "must_not": ["kehanet"]})
        self.assertEqual(m["seed"]["master"], "TT-00000001")
        self.assertEqual([c["chapter"] for c in m["arc_skeleton"]], ["chapter_1", "chapter_2", "chapter_3"])
        self.assertEqual(m["arc_skeleton"][-1]["level_band"][1], 5)
        self.assertEqual(set(m["phases"]), {f"P{i}" for i in range(10)})
        for sub in ("design/dm-only/_snapshots", "design/_staging", "design/dm-only/npcs", "characters"):
            self.assertTrue((self.dir / sub).is_dir(), sub)
        self.assertEqual(self.run_m("init", "--scale", "short", "--tone", "horror", "--magic", "low",
                                    "--era", "nautical", "--danger", "gritty", "--party-size", "2",
                                    "--content-mix", "mystery,exploration,politics").returncode, 1,
                         "a second init refuses to overwrite")

    def test_init_validates_the_dials(self):
        proc = self.run_m("init", "--scale", "huge", "--tone", "horror", "--magic", "low", "--era", "nautical",
                          "--danger", "gritty", "--party-size", "2", "--content-mix", "mystery,exploration,politics")
        self.assertEqual(proc.returncode, 2)
        proc = self.run_m("init", "--scale", "epic", "--tone", "horror", "--magic", "low", "--era", "nautical",
                          "--danger", "gritty", "--party-size", "2", "--content-mix", "mystery,mystery,politics")
        self.assertEqual(proc.returncode, 2)

    def test_standard_and_epic_arc_shapes(self):
        sys.path.insert(0, str(SCRIPTS))
        import design_manifest as dm
        std = dm.arc_skeleton("standard", 1)
        self.assertEqual(len(std), 7)
        self.assertEqual(sorted({c["act"] for c in std}), [1, 2, 3])
        self.assertEqual(std[0]["level_band"][0], 1)
        self.assertEqual(std[-1]["level_band"][1], 12)
        epic = dm.arc_skeleton("epic", 3)
        self.assertEqual(len(epic), 10)
        self.assertEqual(epic[-1]["level_band"][1], 22)


class OnTheFixture(unittest.TestCase):

    def setUp(self):
        self.c = TestCampaign("manifest")

    def tearDown(self):
        self.c.remove()

    def m(self, *args, check=False):
        return self.c.run("design_manifest.py", *args, check=check)

    def test_status_reads_the_fixture(self):
        proc = self.m("status", check=True)
        self.assertIn("mode play", proc.stdout)
        self.assertIn("P6  approved", proc.stdout)
        data = json.loads(self.m("status", "--json", check=True).stdout)
        self.assertEqual(data["phases"]["P9"]["status"], "approved")

    def test_reconcile_downgrades_an_entity_whose_fragment_is_still_staged(self):
        # a crash after the agent wrote its fragment but before merge
        src = self.c.path("design/_staging/P5/merged/npc_yesra.json")
        shutil.copy(src, self.c.path("design/_staging/P5/npc_yesra.json"))
        src.unlink()
        self.m("mark", "--phase", "P5", "--roster", "npc_yesra,npc_ilme", check=True)
        self.c.reopen("P5", "merged")    # an approved phase is frozen; the crash happened before approval
        proc = self.m("reconcile", check=True)
        self.assertIn("changed from disk", proc.stdout)
        data = self.c.json("design/design.json")
        self.assertEqual(data["entities"]["npc_yesra"]["status"], "staged")
        self.assertEqual(data["entities"]["npc_ilme"]["status"], "validated", "merged rows keep their rank")
        self.assertEqual(data["phases"]["P5"]["status"], "partial")
        pend = json.loads(self.m("pending", "--phase", "P5", "--json", check=True).stdout)
        self.assertEqual([e["id"] for e in pend["entities"]], ["npc_yesra"])
        self.assertTrue(any(f.endswith("npc_yesra.md") for f in pend["entities"][0]["files"]))

    def test_reconcile_picks_up_a_fragment_the_manifest_never_saw(self):
        frag = self.c.json("design/_staging/P5/merged/npc_yesra.json")
        frag["id"] = frag["registry"]["id"] = "npc_yeni"
        self.c.write_json("design/_staging/P5/npc_yeni.json", frag)
        self.m("reconcile", check=True)
        row = self.c.json("design/design.json")["entities"]["npc_yeni"]
        self.assertEqual((row["status"], row["phase"]), ("staged", "P5"))

    def test_pending_is_the_roster_minus_merged_with_a_two_hop_read_budget(self):
        self.m("mark", "--phase", "P5", "--roster", "npc_yesra,npc_ilme,npc_hayalet", check=True)
        pend = json.loads(self.m("pending", "--phase", "P5", "--json", check=True).stdout)
        self.assertEqual([e["id"] for e in pend["entities"]], ["npc_hayalet"])
        self.assertEqual(pend["entities"][0]["status"], "pending")
        # a merged entity's budget: own file first, mirror next, then neighbours within two hops
        sys.path.insert(0, str(SCRIPTS))
        import design_manifest as dm
        canonical = self.c.json("design/dm-only/entities.json")["entities"]
        files = dm.read_budget(self.c.name, canonical, "npc_yesra")
        self.assertTrue(files[0].endswith("npc_yesra.md"))
        self.assertTrue(any(f.endswith(str(Path("dm-only") / "npcs" / "npc_yesra.md")) for f in files))
        self.assertTrue(any(f.endswith("faction_court_of_mourners.md") for f in files), "one hop")
        self.assertTrue(any(f.endswith("site_blind_lantern.md") for f in files), "two hops via faction_court_of_mourners")
        self.assertFalse(any(f.endswith("settlement_reedham.md") for f in files), "three hops away")

    def test_mark_running_bumps_the_attempt_and_records_entity_failures(self):
        self.m("mark", "--phase", "P7", "--status", "running", "--roster", "chapter_1,chapter_2", check=True)
        self.m("mark", "--phase", "P7", "--entity", "chapter_2", "--status", "failed", "--attempt", "2",
               "--agent", "P7.chapter_2.a2", "--error", "returned null twice", check=True)
        data = self.c.json("design/design.json")
        self.assertEqual(data["phases"]["P7"]["attempt"], 2)
        self.assertEqual(data["phases"]["P7"]["status"], "running")
        row = data["entities"]["chapter_2"]
        self.assertEqual((row["status"], row["attempt"], row["last_error"]), ("failed", 2, "returned null twice"))
        proc = self.m("approve", "--phase", "P7", "--card", "design/report.md", "--commit", "abc1234")
        self.assertEqual(proc.returncode, 1, "a phase with a failed entity cannot be approved")

    def test_approve_records_card_and_registry_hashes_and_the_commit(self):
        card = self.c.path("design/_approval/P8.md")
        card.parent.mkdir(exist_ok=True)
        card.write_text("# P8 card\n", encoding="utf-8")
        proc = self.m("approve", "--phase", "P8", "--round", "Reedham daha küçük olsun", "--scope", "entity",
                      "--affected", "1", check=True)
        self.assertIn("round 1", proc.stdout)
        proc = self.m("approve", "--phase", "P8", "--card", str(card), "--commit", "deadbee", check=True)
        ph = self.c.json("design/design.json")["phases"]["P8"]
        self.assertEqual(ph["status"], "approved")
        self.assertEqual(len(ph["approval"]["card_sha256"]), 64)
        self.assertEqual(len(ph["approval"]["registry_sha256"]), 64)
        self.assertEqual(ph["approval"]["commit"], "deadbee")
        self.assertEqual(ph["approval"]["rounds"][0]["scope"], "entity")

    def test_three_rounds_is_the_limit(self):
        for i in range(3):
            self.m("approve", "--phase", "P4", "--round", f"düzeltme {i}", check=True)
        self.assertEqual(self.m("approve", "--phase", "P4", "--round", "dördüncü").returncode, 1)

    def test_stale_marks_later_phases_by_mode(self):
        self.m("stale", "--from", "P3", "--reason", "P3 rerun attempt 2", check=True)
        data = self.c.json("design/design.json")
        self.assertEqual(data["phases"]["P4"]["status"], "needs-check", "fixture is in play mode")
        self.assertEqual(data["phases"]["P4"]["stale_reason"], "P3 rerun attempt 2")
        self.assertEqual(data["phases"]["P2"]["status"], "approved", "earlier phases untouched")
        self.m("set-mode", "birth", check=True)
        self.m("stale", "--from", "P1", "--reason", "reseed", check=True)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P2"]["status"], "stale")

    def test_set_mode_play_needs_every_phase_approved(self):
        self.m("mark", "--phase", "P6", "--status", "running", check=True)
        self.assertEqual(self.m("set-mode", "play").returncode, 1)

    def test_tokens_add_deltas_to_phase_and_totals(self):
        before = self.c.json("design/design.json")["totals"]["tokens_out"]
        self.m("tokens", "--phase", "P5", "--out", "1200", "--model", "claude-fable-5-1", "--wall", "30",
               "--agents", "2", check=True)
        data = self.c.json("design/design.json")
        self.assertEqual(data["totals"]["tokens_out"], before + 1200)
        self.assertEqual(data["phases"]["P5"]["tokens"]["by_model"]["claude-fable-5-1"]["out"], 15100 + 1200)
        self.assertEqual(data["totals"]["agents"], 33)

    def test_logs_ask_detail_and_revision(self):
        self.assertEqual(self.m("ask", "--question", "Lantern yanacak mı?", "--answer", "belki", "--agent", "x").returncode, 2)
        self.m("ask", "--question", "Lantern yanacak mı?", "--answer", "spoiler vermeden cevaplanamaz",
               "--agent", "ask.a1", check=True)
        self.m("detail-log", "--id", "site_blind_lantern", "--day", "40", "--trigger", "destination", check=True)
        proc = self.m("revision", "--scope", "fact", "--reason", "Reedham nüfusu 120", "--affected", "2", check=True)
        self.assertEqual(proc.stdout.strip(), "rev_0002")
        data = self.c.json("design/design.json")
        self.assertEqual(data["ask_log"][-1]["answer"], "spoiler vermeden cevaplanamaz")
        self.assertEqual(data["detail_log"][-1]["id"], "site_blind_lantern")
        self.assertEqual(data["revision_log"][-1]["id"], "rev_0002")

    def test_roll_appends_public_and_secret_records(self):
        self.m("roll", "--record", json.dumps({"phase": "P6", "table": "sites.yaml#x", "label": "l", "notation": "d6",
                                                "raw": 4, "row_id": None, "excluded": [], "ts": "t"}), check=True)
        self.m("roll", "--record", json.dumps({"phase": "P4", "table": "antagonists.yaml#doom", "label": "P4.doom",
                                                "notation": "d4", "raw": 2, "row_id": "doom_x", "excluded": [], "ts": "t"}),
               "--secret", check=True)
        data = self.c.json("design/design.json")
        self.assertEqual(data["dice_log"][-1]["label"], "l")
        self.assertEqual(data["dice_log_secret"]["count"], 4)
        self.assertIn("P4.doom", data["dice_log_secret"]["labels"])
        self.assertNotIn("doom_x", json.dumps(data), "secret results never enter design.json")
        secret = self.c.json("design/dm-only/dice-log.json")
        self.assertEqual(secret["rolls"][-1]["row_id"], "doom_x")


if __name__ == "__main__":
    unittest.main()
