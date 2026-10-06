"""
test_secret_layer.py — build item 18d (docs/p1-build-18.md, Part 18d; docs/p1-build-18-rows.md section 5): the secret
as the threat's hidden half. The tables (the twist, the keeping, the trails; the archetypes retired); the four facts
and the three stages with three clues each; the twist's rate with and without mystery; no retired row rolled; every
new row's promise reaches the ledger; the public ledger unchanged by the secret rolls; a legacy birth's secret.

Failure messages give counts and positions only: no row of a secret table is printed.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_foundation as fd  # noqa: E402
import design_identity as di  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402
import design_threat as dth  # noqa: E402
import designer  # noqa: E402
import _corpus  # noqa: E402  (build item 18f-1: the shared many-seed corpus)

S = "secrets.yaml#"
SEEDS = 3000
SPAN = {"short": 4, "standard": 11, "epic": 19}


def active_text(ref: str) -> str:
    return json.dumps(dt.rows(ref), ensure_ascii=False)


class Tables(unittest.TestCase):

    def test_the_counts(self):
        self.assertEqual(len(dt.rows(S + "archetype")), 0)
        self.assertEqual(len(dt.retired(S + "archetype")), 31)
        self.assertEqual(len(dt.rows(S + "twist")), 20)
        self.assertEqual(len(dt.rows(S + "keeping")), 16)
        self.assertEqual(len(dt.rows(S + "trail")), 11)
        self.assertIsNotNone(dt.row(S + "twist", "twist_greater_power"))
        self.assertIsNotNone(dt.row(S + "trail", "trail_omen_divination_dead"))
        self.assertIsNone(next((r for r in dt.rows(S + "keeping") if r["id"] == "twist_pc_is_involved"), None), "a PC is involved left")
        kept = {r["id"] for r in dt.rows(S + "twist")} - {"twist_greater_power"}
        retired = {r["id"] for r in dt.retired(S + "archetype")}
        self.assertEqual(len(kept), 19)
        self.assertTrue(kept <= retired, "the nineteen kept archetypes are the twists")
        self.assertIn("secret_gods_are_prisoners", retired - kept)
        self.assertIn("secret_god_erased", retired - kept)
        self.assertEqual(dt.row("antagonists.yaml#villain_family", "family_god")["forms"], ["imprisoned", "forgotten_returning"])

    def test_the_twists_written_by_hand(self):
        """The 18d audit's rules: no break and no destroying for the move; one sentence of what is true; the protector a
        story actor, never the institution; the old kingdom; the made people victims; the greater power's statement."""
        bad = re.compile(r"\bbreaks?\b|\bbroke\b|\bbroken\b|\bdestroy", re.I)
        for n, r in enumerate(dt.rows(S + "twist")):
            for text in (r["label"], r["cause"], r.get("statement") or ""):
                self.assertIsNone(bad.search(text), f"twist row {n}")
            self.assertEqual(r["cause"].count(". "), 0, f"twist row {n}: one sentence")
        by = {r["id"]: r for r in dt.rows(S + "twist")}
        self.assertNotIn("institution", by["secret_cure_is_the_cause"]["cause"])
        self.assertIn("old kingdom", by["secret_history_looping"]["cause"])
        self.assertIn("not a people evil by birth", by["secret_monsters_were_made"]["cause"])
        self.assertIn("believes it is the master", by["twist_greater_power"]["statement"])
        self.assertEqual({r["id"] for r in dt.rows("antagonists.yaml#hand") if r["base"] == "inside"},
                         {"hand_traitor", "hand_contest_side", "hand_shapechangers"})

    def test_the_words_of_the_chain(self):
        for ref in (S + "twist", S + "keeping", S + "trail"):
            text = active_text(ref)
            self.assertNotIn("{the chooser}", text, ref)
            self.assertIsNone(re.search(r"\b[Aa]cts?\b \d|\bActs\b", text), f"{ref}: the word act left the secret hooks")
        self.assertIsNone(re.search(r"\bActs?\b", json.dumps(dt.load("secrets.yaml")["hooks_common"])))
        for r in dt.rows(S + "trail"):
            self.assertEqual(set(r["stages"]), {"stage1", "stage2", "stage3"})
            self.assertTrue(r["stages"]["stage3"].endswith("how_it_is_stopped"), "the third element carries the weakness")
        for r in dt.rows(S + "twist"):
            self.assertTrue(r.get("cause") and r.get("hides_in"))

    def test_every_new_table_states_its_avoid_used(self):
        for ref in (S + "twist", S + "keeping", S + "trail", "antagonists.yaml#villain_family", "antagonists.yaml#power_source",
                    "antagonists.yaml#goal", "antagonists.yaml#weakness", "antagonists.yaml#lair_form", "antagonists.yaml#lair_where",
                    "antagonists.yaml#hand", "antagonists.yaml#move_state"):
            self.assertIn("avoid_used", dt.own_roll_header(ref), ref)

    def test_the_new_rows_carry_their_promises(self):
        V = "antagonists.yaml#"
        self.assertTrue(all(r.get("hooks") for r in dt.rows(V + "weakness")))
        self.assertTrue({h["phase"] for r in dt.rows(V + "weakness") for h in r["hooks"]} <= {"P2", "P5", "P6"})
        self.assertTrue(all(r.get("hooks") for r in dt.rows(V + "power_source")))
        doc = dt.load("antagonists.yaml")["tables"]
        self.assertEqual(doc["goal"]["hooks_common"][0]["phase"], "P4")
        self.assertEqual(doc["lair_form"]["hooks_common"][0]["phase"], "P6")
        self.assertEqual(doc["villain_family"]["hooks_common"][0]["phase"], "P9", "a hero bound to the threat")
        self.assertEqual(doc["hand"]["hooks_common"][0]["phase"], "P4")


def births(n):
    """The first n births of the shared corpus (build item 18f-1), as (dials, R)."""
    return _corpus.births(n)


class ManySeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = births(SEEDS)

    def test_the_four_facts(self):
        for d, R in self.runs:
            f = R.identity_secret["secret"]["facts"]
            self.assertEqual(set(f), {"who", "what_and_why", "where", "how_stopped", "creature_types", "hidden"})
            known = R.threat["visibility"] in dth.PUBLIC_VISIBILITY
            self.assertEqual(f["hidden"], 3 if known else 4)
            self.assertEqual(f["how_stopped"]["weakness"], R.threat["weakness"])
            self.assertEqual(f["where"], R.threat["lair"])
            self.assertEqual(f["what_and_why"]["goal"], R.threat["goal"]["id"])

    def test_three_stages_with_three_clues_each(self):
        for d, R in self.runs:
            stages = R.identity_secret["secret"]["stages"]
            self.assertEqual([s["n"] for s in stages], [1, 2, 3])
            f = R.foundation
            for s in stages:
                self.assertEqual([c["by"] for c in s["clues"]], ["chain", "P5", "P6"])
                self.assertEqual(s["conclusion"], di.CONCLUSIONS[s["n"]])
            self.assertEqual(stages[1]["clues"][0]["at"], f["layout"]["break_at"], "stage 2 where the move struck")
            hand = dt.row("antagonists.yaml#hand", f["move"]["hand"] or R.threat["hand"]["id"])      # 19a: an unnoticed move's
            if hand["base"] == "far_end":
                self.assertTrue(str(stages[0]["clues"][0]["at"]).startswith("end_"), "stage 1 at the hand's base, the far end")
            elif hand["id"] != "hand_contest_side":
                self.assertEqual(stages[0]["clues"][0]["at"], "heart", "a hand inside by nature: its base is the heart")
            self.assertEqual(stages[2]["reveals"], "how it is stopped")
            lo = [s["levels"][0] for s in stages]
            self.assertEqual(lo, sorted(lo))

    def test_the_twist_s_rate(self):
        with_m = [R.identity_secret["secret"]["twist"] is not None for d, R in self.runs if "mystery" in d["content_mix"]]
        without = [R.identity_secret["secret"]["twist"] is not None for d, R in self.runs if "mystery" not in d["content_mix"]]
        self.assertTrue(all(with_m), "always with mystery")
        self.assertTrue(0.4 < sum(without) / len(without) < 0.6, "else on a d2")

    def test_no_retired_row_is_rolled(self):
        retired = {ref: {r["id"] for r in dt.retired(ref)} for ref in (S + "twist", S + "keeping", S + "trail", S + "archetype", S + "chooser")}
        for d, R in self.runs:
            for rec in R.secret + R.public:
                if rec.get("table") in retired and rec.get("row_id"):
                    self.assertNotIn(rec["row_id"], retired[rec["table"]])
            self.assertFalse({r["label"] for r in R.secret} & {"secret_archetype", "secret_chooser"})

    def test_the_ledgers(self):
        secret_ids = dt.secret_row_ids()
        for d, R in self.runs[:600]:
            pub, sec = dp.build(d, R.public, R.secret, R.foundation, R.identity, R.identity_secret)
            self.assertEqual(sum(1 for p in sec if p["source"] in ("clue_stage", "clue")), 9, "nine clue promises")
            self.assertEqual({p["due"] for p in sec if p["source"] == "clue"}, {"P5", "P6"})
            origins = {p["from"] if isinstance(p.get("from"), str) else "" for p in sec}
            dues = {p["due"] for p in sec}
            self.assertIn("P9", dues, "a hero bound to the threat")
            self.assertIn("P4", dues, "the goal's front")
            self.assertTrue([p for p in pub if p["source"] == "foundation" and "start is a village" in p["text"]])
            if R.foundation["move"]["state"] != "move_unnoticed":
                self.assertTrue([p for p in pub if "creature families" in p["text"]])
            else:                       # build item 19a: an unnoticed move's hand and its families are secret
                self.assertFalse([p for p in pub if "creature families" in p["text"]])
                self.assertTrue([p for p in sec if "the hand nobody saw" in p["text"]])
            # the public ledger is the same whatever the secret holds, and names none of it
            pub0, _ = dp.build(d, R.public, [], R.foundation, R.identity, None)
            self.assertEqual([p["text"] for p in pub], [p["text"] for p in pub0])
            text = json.dumps(pub)
            self.assertEqual(sum(1 for rid in secret_ids if f'"{rid}"' in text or f" {rid} " in text), 0)


def run(script, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode})")
    return proc


class LegacySecret(unittest.TestCase):
    """A birth rolled before 18d: an archetype, an old twist, an old trail with `acts`, no facts and no stages."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-legacy18d-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run("designer.py", "new", self.name, "--party-size", "2", "--seed", "LEGACY-18D", "--lang", "tr", "--scale", "standard")
        run("designer.py", "-c", self.name, "preroll", "--phase", "P1")

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_it_renders(self):
        path = CAMPAIGNS / self.name / "design/dm-only/dice-log.json"
        log = json.loads(path.read_text(encoding="utf-8"))
        old_arch = dt.retired(S + "archetype")[0]["id"]
        old_twist = dt.retired(S + "twist")[0]["id"]
        log["identity"]["secret"] = {"archetype": old_arch, "chooser": "chooser_the_villain", "chooser_role": None,
                                     "twist": old_twist, "trail": dt.rows(S + "trail")[0]["id"]}
        path.write_text(json.dumps(log), encoding="utf-8")
        m = dm.load(self.name)
        pub, sec = dp.build(m["dials"], m["dice_log"], log["rolls"], m["foundation"], m["identity"], log["identity"])
        self.assertEqual(sum(1 for p in sec if p["source"] == "clue_stage"), 3, "the legacy archetype's three clues")
        run("designer.py", "-c", self.name, "phase", "P1", "card")
        self.assertTrue((CAMPAIGNS / self.name / "design/_approval/P1.card.md").is_file())


if __name__ == "__main__":
    unittest.main()
