"""
test_designer.py — the conductor's CLI (plan item 19, 21.E; the 1c auto-approve decision):
`new` rolls blank dials, initialises the manifest, writes the P0 card, arms the guard and, for a
test campaign, approves P0 on its own; `preroll` makes every labelled roll of a phase, secret rolls
stay out of design.json, the draws are reproducible from the seed and honour the tables' closed
lists; `phase begin / merge / check / card / approve / rerun` drive the fixture through a phase;
`abandon` disarms and drops the campaign's used.json rows.
"""

import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

from _campaign import TestCampaign, SCRIPTS, PROJECT, CAMPAIGNS

sys.path.insert(0, str(SCRIPTS))
import design_tables as dt  # noqa: E402
from design_io import is_fragment  # noqa: E402
from paths import runtime_dir  # noqa: E402

MARKER = runtime_dir() / "active-design.json"
USED = PROJECT / "used.json"


def run(*args, check=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "designer.py"), *args],
                          capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"designer {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


class MarkerGuard:
    """Keep the real runtime marker out of the tests' way."""

    def __enter__(self):
        self.backup = MARKER.read_bytes() if MARKER.is_file() else None
        if MARKER.is_file():
            MARKER.unlink()
        return self

    def __exit__(self, *exc):
        if MARKER.is_file():
            MARKER.unlink()
        if self.backup is not None:
            MARKER.write_bytes(self.backup)


class NewBirth(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.names = []

    def tearDown(self):
        for n in self.names:
            shutil.rmtree(CAMPAIGNS / n, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def birth(self, seed="TEST-0001", **dials):
        name = f"_test-birth-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        self.names.append(name)
        args = ["new", name, "--party-size", "2", "--seed", seed, "--lang", "tr"]
        for k, v in dials.items():
            args += [f"--{k.replace('_', '-')}", v]
        proc = run(*args, check=True)
        return name, proc

    def manifest(self, name):
        return json.loads((CAMPAIGNS / name / "design" / "design.json").read_text(encoding="utf-8"))

    def test_new_rolls_blank_dials_and_auto_approves_p0(self):
        name, proc = self.birth()
        m = self.manifest(name)
        self.assertTrue(m["_meta"]["auto_approve"], "a _test- campaign auto-approves")
        for dial in ("scale", "tone", "magic", "era", "danger"):
            self.assertIn(m["dials"][dial], dt.dial_values(dial))
        self.assertEqual(len(m["dials"]["content_mix"]), 3)
        self.assertEqual(len(set(m["dials"]["content_mix"])), 3)
        labels = [r["label"] for r in m["dice_log"]]
        self.assertEqual(labels[:8], ["dial.scale", "dial.tone", "dial.magic", "dial.era", "dial.danger",
                                      "content_mix.1", "content_mix.2", "content_mix.3"])
        self.assertEqual(m["phases"]["P0"]["status"], "approved")
        self.assertTrue((CAMPAIGNS / name / "design" / "_approval" / "P0.card.md").is_file())
        self.assertIsNone(m["phases"]["P0"]["approval"]["commit"], "a git-ignored test campaign is never committed")
        marker = json.loads(MARKER.read_text(encoding="utf-8"))
        self.assertEqual((marker["campaign"], marker["mode"]), (name, "birth"))
        self.assertIn("zar: dial.scale", proc.stdout)

    def test_given_dials_are_not_rolled_and_a_real_birth_waits_for_onay(self):
        name = f"_test-real-birth-{os.getpid()}-{uuid.uuid4().hex[:6]}"   # git-ignored: nothing is ever committed
        self.names.append(name)
        proc = run("new", name, "--scale", "short", "--tone", "horror", "--magic", "low", "--era", "nautical",
                   "--danger", "gritty", "--content-mix", "mystery,horror,exploration", "--party-size", "1",
                   "--seed", "REAL-0001", "--ask-approval", check=True)
        m = self.manifest(name)
        self.assertFalse(m["_meta"]["auto_approve"])
        self.assertEqual(m["dials"]["tone"], "horror")
        self.assertEqual(m["dice_log"], [])
        self.assertEqual(m["phases"]["P0"]["status"], "awaiting_approval")
        self.assertIn("awaits `onay`", proc.stdout)
        refused = run("-c", name, "phase", "P0", "approve")
        self.assertEqual(refused.returncode, 1)
        run("-c", name, "phase", "P0", "approve", "--onay", check=True)
        m = self.manifest(name)
        self.assertEqual(m["phases"]["P0"]["status"], "approved")
        self.assertIsNone(m["phases"]["P0"]["approval"]["commit"], "an --ask-approval test birth never commits")

    def test_preroll_p1_labels_secrets_and_closed_lists(self):
        name, _ = self.birth(scale="short")
        proc = run("-c", name, "preroll", "--phase", "P1", check=True)
        m = self.manifest(name)
        pub = {r["label"]: r for r in m["dice_log"] if r["phase"] == "P1"}
        self.assertIn("tension.1", pub)
        self.assertIn("tension.second", pub)
        self.assertEqual(sum(1 for l in pub if l.startswith("break.")), 1, "short rolls one trope break")
        for sub in ("phenomenon", "people", "institution"):
            self.assertTrue(pub[f"sig_{sub}"]["row_id"].startswith("sig_"))
        fams = [r["row_id"] for l, r in pub.items() if l.startswith("naming_family.")]
        self.assertEqual(len(fams), 2)
        self.assertEqual(len(set(fams)), 2)
        self.assertEqual(pub["mechanic"]["row_id"], "no", "short never rolls the signature mechanic")
        for secret_label in ("secret_archetype", "secret_twist", "secret_trail"):
            self.assertNotIn(secret_label, pub, "secret rolls never enter design.json")
            self.assertIn(secret_label, m["dice_log_secret"]["labels"])
        secret = json.loads((CAMPAIGNS / name / "design" / "dm-only" / "dice-log.json").read_text(encoding="utf-8"))
        self.assertEqual(m["dice_log_secret"]["count"], len(secret["rolls"]))
        self.assertTrue(any(r["label"] == "secret_archetype" and r["row_id"].startswith("secret_") for r in secret["rolls"]))
        self.assertEqual(m["phases"]["P1"]["status"], "prerolled")
        self.assertIn("prerolled", proc.stdout)
        again = run("-c", name, "preroll", "--phase", "P1")
        self.assertEqual(again.returncode, 1, "a second preroll of the same attempt is refused")

    def test_preroll_is_reproducible_from_the_seed(self):
        a, _ = self.birth(seed="SAME-0001", scale="standard")
        b, _ = self.birth(seed="SAME-0001", scale="standard")
        for name in (a, b):
            run("-c", name, "preroll", "--phase", "P1", check=True)
            run("-c", name, "preroll", "--phase", "P2", check=True)
        ma, mb = self.manifest(a), self.manifest(b)
        self.assertEqual(ma["dials"], mb["dials"])
        rows_a = [(r["label"], r["row_id"], r["raw"]) for r in ma["dice_log"]]
        rows_b = [(r["label"], r["row_id"], r["raw"]) for r in mb["dice_log"]]
        self.assertEqual(rows_a, rows_b)
        self.assertGreater(len(rows_a), 30)
        c, _ = self.birth(seed="OTHER-0002", scale="standard")
        run("-c", c, "preroll", "--phase", "P1", check=True)
        self.assertNotEqual([(r["label"], r["row_id"]) for r in self.manifest(c)["dice_log"] if r["phase"] == "P1"],
                            [(r["label"], r["row_id"]) for r in ma["dice_log"] if r["phase"] == "P1"])

    def test_every_phase_prerolls_and_forbidden_rows_never_come_up(self):
        name, _ = self.birth(seed="ALL-0003", scale="short")
        for phase in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"):
            run("-c", name, "preroll", "--phase", phase, check=True)
        m = self.manifest(name)
        secret = json.loads((CAMPAIGNS / name / "design" / "dm-only" / "dice-log.json").read_text(encoding="utf-8"))
        forbidden = set()
        for _, _, r in ((n, s, r) for n in dt.list_tables() for s, rows in dt.all_row_lists(dt.load(n)).items() for r in rows):
            if r.get("forbidden"):
                forbidden.add(r["id"])
        for rec in m["dice_log"] + secret["rolls"]:
            self.assertNotIn(rec.get("row_id"), forbidden, rec["label"])
        pub = {r["label"]: r for r in m["dice_log"]}
        self.assertIn("pantheon_type", pub)
        self.assertIn("wild_shape", pub)
        self.assertGreaterEqual(sum(1 for l in pub if l.startswith("region.1.")), 10)
        self.assertGreaterEqual(sum(1 for l in pub if l.startswith("faction.1.")), 5)
        self.assertGreaterEqual(sum(1 for l in pub if l.startswith("npc.1.")), 7)
        self.assertGreaterEqual(sum(1 for l in pub if l.startswith("site.1.")), 9)
        self.assertEqual(sum(1 for l in pub if l.startswith("beat.")), 3, "short: three beats")
        self.assertEqual(sum(1 for l in pub if l.startswith("socket.")), 4, "2 PCs × 2 sockets in short")
        sec = {r["label"] for r in secret["rolls"]}
        self.assertTrue({"bbeg_visibility", "bbeg_shape", "bbeg_origin", "front_template", "doom_shape", "pc.1.truth"} <= sec)
        for rec in m["dice_log"]:
            if rec["label"].startswith("faction.") and rec["label"].endswith(".rung.1"):
                self.assertNotEqual(rec["row_id"], "rung_war", "the first rung is never war")
        tics = [r["row_id"] for r in m["dice_log"] if r["label"].endswith(".tic")]
        self.assertTrue(all(tics.count(t) <= 2 for t in set(tics)), "no tic seed more than twice")
        self.assertIn(self.manifest(name)["phases"]["P9"]["status"], ("prerolled",))
        st = run("-c", name, "status", "--json", check=True)
        self.assertTrue(json.loads(st.stdout)["armed"])

    def test_abandon_disarms_and_drops_used_rows(self):
        name, _ = self.birth(seed="ABAN-0004")
        run("-c", name, "preroll", "--phase", "P1", check=True)
        subprocess.run([sys.executable, str(SCRIPTS / "design_dice.py"), "-c", name, "used", "add", "--table", "tensions.yaml",
                        "--row", "tension_power_self"], capture_output=True)
        proc = run("-c", name, "abandon", "--reason", "test", check=True)
        self.assertIn("abandoned", proc.stdout)
        self.assertFalse(MARKER.is_file())
        used = json.loads(USED.read_text(encoding="utf-8")) if USED.is_file() else {"campaigns": {}}
        self.assertNotIn(name, used.get("campaigns", {}))
        self.assertEqual(self.manifest(name)["_meta"]["mode"], "abandoned")


class FixturePhase(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("designer")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)   # the fixture's manifest is in play mode
        merged = self.c.path("design/_staging/P6/merged")
        for f in merged.glob("*.json"):
            shutil.copy(f, merged.parent / f.name)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_begin_merge_check_card_approve_and_rerun(self):
        self.c.reopen("P6", "prerolled")
        begin = run("-c", self.c.name, "phase", "P6", "begin", "--json", check=True)
        out = json.loads(begin.stdout[begin.stdout.index("{"):])
        self.assertEqual(out["phase"], "P6")
        self.assertTrue(MARKER.is_file())
        merge = run("-c", self.c.name, "phase", "P6", "merge", check=True)
        self.assertIn("merge", merge.stdout)
        left = [p.name for p in self.c.path("design/_staging/P6").glob("*.json") if is_fragment(p)]
        self.assertEqual(left, [], "fragments moved to merged/ (the merge report is not a fragment)")
        check = run("-c", self.c.name, "phase", "P6", "check", check=True)
        self.assertIn("0 errors", check.stdout)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P6"]["validator"]["errors"], 0)
        card = run("-c", self.c.name, "phase", "P6", "card", check=True)
        self.assertIn("card", card.stdout)
        card_path = self.c.path("design/_approval/P6.card.md")
        self.assertTrue(card_path.is_file())
        text = card_path.read_text(encoding="utf-8")
        self.assertNotIn("Nerun", text, "the card never carries a secret name")
        refused = run("-c", self.c.name, "phase", "P6", "approve")
        self.assertEqual(refused.returncode, 1, "the fixture is not auto-approve; onay is required")
        run("-c", self.c.name, "phase", "P6", "approve", "--onay", check=True)
        m = self.c.json("design/design.json")
        self.assertEqual(m["phases"]["P6"]["status"], "approved")
        self.assertEqual(m["phases"]["P6"]["approval"]["card_sha256"][:4] != "0000", True)
        rerun = run("-c", self.c.name, "phase", "P6", "rerun", "--reason", "odalar dar", check=True)
        self.assertIn("attempt 3", rerun.stdout)
        m = self.c.json("design/design.json")
        self.assertEqual(m["phases"]["P6"]["status"], "pending")
        self.assertEqual(m["phases"]["P7"]["status"], "stale")
        self.assertTrue(self.c.path("design/_staging/P6.attempt-1").is_dir())
        self.assertIn("odalar dar", m["phases"]["P6"]["directions"])

    def test_begin_refuses_when_the_previous_phase_is_not_approved(self):
        self.c.reopen("P6", "prerolled")
        m = self.c.json("design/design.json")
        m["phases"]["P5"]["status"] = "awaiting_approval"
        self.c.path("design/design.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        proc = run("-c", self.c.name, "phase", "P6", "begin")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not approved", proc.stderr)

    def test_begin_refuses_an_approved_phase(self):
        proc = run("-c", self.c.name, "phase", "P6", "begin")
        self.assertEqual(proc.returncode, 1, "an approved phase is closed; rerun reopens it (tuning birth 1, 3.5)")
        self.assertIn("rerun", proc.stderr)


if __name__ == "__main__":
    unittest.main()
