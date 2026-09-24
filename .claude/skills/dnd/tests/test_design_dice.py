"""
test_design_dice.py — seeded, labelled, logged rolls: same seed and label give
the same result in any order; a rerun attempt redraws; secret rolls stay out of
design.json; used.json exclusions are honoured and logged; dice.py takes an
injected rng.
"""

import json
import random
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, SCRIPTS, PROJECT

sys.path.insert(0, str(SCRIPTS))
import dice as dice_mod  # noqa: E402
import design_dice as dd  # noqa: E402

USED = PROJECT / "used.json"


class InjectedRng(unittest.TestCase):

    def test_dice_run_is_reproducible_with_a_seeded_rng(self):
        a = dice_mod.run("4d6kh3+2", silent=True, rng=random.Random("x"))
        b = dice_mod.run("4d6kh3+2", silent=True, rng=random.Random("x"))
        c = dice_mod.run("4d6kh3+2", silent=True, rng=random.Random("y"))
        self.assertEqual(a, b)
        self.assertTrue(5 <= a <= 20)
        self.assertTrue(5 <= c <= 20)

    def test_derivation_is_order_independent_and_attempt_sensitive(self):
        r1 = dd.derive("S", "P1", "t", "a", 1).randint(1, 10 ** 6)
        r2 = dd.derive("S", "P1", "t", "b", 1).randint(1, 10 ** 6)
        r1_again = dd.derive("S", "P1", "t", "a", 1).randint(1, 10 ** 6)
        r1_attempt2 = dd.derive("S", "P1", "t", "a", 2).randint(1, 10 ** 6)
        self.assertEqual(r1, r1_again)
        self.assertNotEqual(r1, r2)
        self.assertNotEqual(r1, r1_attempt2)


class Rolls(unittest.TestCase):

    def setUp(self):
        self.c = TestCampaign("dice")
        self.used_backup = USED.read_bytes() if USED.exists() else None
        if USED.exists():
            USED.unlink()

    def tearDown(self):
        self.c.remove()
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.exists():
            USED.unlink()

    def roll(self, *args):
        proc = self.c.run("design_dice.py", "roll", "--json", *args, check=True)
        return json.loads(proc.stdout)

    def test_same_label_same_result_and_it_is_logged(self):
        a = self.roll("--phase", "P3", "--label", "region.1.tier", "--notation", "d5")
        b = self.roll("--phase", "P3", "--label", "region.1.tier", "--notation", "d5")
        other = self.roll("--phase", "P3", "--label", "region.2.tier", "--notation", "d5")
        self.assertEqual(a["raw"], b["raw"])
        self.assertTrue(1 <= a["raw"] <= 5 and 1 <= other["raw"] <= 5)
        log = self.c.json("design/design.json")["dice_log"]
        self.assertEqual([r["label"] for r in log[-3:]], ["region.1.tier", "region.1.tier", "region.2.tier"])

    def test_rerun_attempt_redraws(self):
        draws = {self.roll("--phase", "P1", "--label", "x", "--notation", "d1000", "--attempt", str(n))["raw"]
                 for n in (1, 2, 3)}
        self.assertGreater(len(draws), 1)

    def test_secret_roll_stays_out_of_the_manifest(self):
        rec = self.roll("--phase", "P1", "--label", "P1.secret_twist", "--notation", "d6", "--secret")
        data = self.c.json("design/design.json")
        self.assertEqual(data["dice_log_secret"]["count"], 4)
        self.assertNotIn("P1.secret_twist", [r["label"] for r in data["dice_log"]],
                         "a secret roll never enters the public dice_log")
        self.assertIn("P1.secret_twist", data["dice_log_secret"]["labels"])
        self.assertEqual(self.c.json("design/dm-only/dice-log.json")["rolls"][-1]["label"], "P1.secret_twist")

    def test_table_roll_with_used_exclusion(self):
        table_dir = SCRIPTS.parent / "data" / "design"
        table_dir.mkdir(exist_ok=True)
        table = table_dir / "_test_tensions.yaml"
        table.write_text("rows:\n" + "".join(f"  - id: t{i}\n    label: tension {i}\n" for i in range(1, 7)),
                         encoding="utf-8")
        try:
            self.c.run("design_dice.py", "used", "add", "--table", "_test_tensions.yaml", "--row", "t3", check=True)
            # mark it as another campaign's use
            used = json.loads(USED.read_text(encoding="utf-8"))
            used["campaigns"]["ashen-crown"] = used["campaigns"].pop(self.c.name)
            USED.write_text(json.dumps(used), encoding="utf-8")
            hits = set()
            for n in range(1, 30):
                rec = self.roll("--phase", "P1", "--label", f"tension.{n}", "--table", "_test_tensions.yaml",
                                "--avoid-used")
                hits.add(rec["row_id"])
                self.assertEqual(rec["excluded"], ["t3"])
            self.assertNotIn("t3", hits)
            self.assertGreater(len(hits), 2)
            proc = self.c.run("design_dice.py", "log", check=True)
            self.assertIn("excluded t3", proc.stdout)
        finally:
            table.unlink()

    def test_roll_needs_a_table_or_a_notation(self):
        self.assertEqual(self.c.run("design_dice.py", "roll", "--phase", "P1", "--label", "x").returncode, 2)


if __name__ == "__main__":
    unittest.main()
