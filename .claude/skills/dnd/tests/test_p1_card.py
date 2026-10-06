"""
test_p1_card.py — build item 14b (docs/p1-build-14.md, Part 14b): the P1 critics judge craft only, on six rubrics;
the card of a script-built P1 follows the layout the owner approved: English, every section in order, no dice on it
(no roll label, no row id, no candidate list), secret promises as counts, and a `YOUR MOVES` line that names only
commands that exist. The premise row's last `_tr` names go, through `design_io.text_field`. A legacy card is unchanged.

  py test_p1_card.py --report <dir>     the card of a script-built P1 (no writer) at each scale
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign
from test_tuning_birth_1 import row

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_promises as dp  # noqa: E402
import design_prompts as dpm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import text_field  # noqa: E402

SECTIONS = ["# P1 — THE FOUNDATION AND THE IDENTITY", "## THE FOUNDATION", "## THE IDENTITY", "## THE PLAYER PITCH",
            "## THE SECRET (spoiler-safe)", "## NAMES", "## PROMISES", "## CHECKS", "## YOUR MOVES"]
P1_RUBRICS = ["rubric_p1_question_concrete", "rubric_p1_only_true_here", "rubric_p1_differs_from_earlier",
              "rubric_p1_signatures_pervade", "rubric_p1_secret_trail", "rubric_p1_forbidden", "rubric_p1_legible"]   # 18e


def run(script, *args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


def birth(scale: str, seed: str) -> str:
    name = f"_test-card-{os.getpid()}-{uuid.uuid4().hex[:6]}"
    run("designer.py", "new", name, "--party-size", "2", "--seed", seed, "--lang", "tr", "--scale", scale)
    run("designer.py", "-c", name, "preroll", "--phase", "P1")
    return name


class Rubrics(unittest.TestCase):

    def test_the_six_p1_rubrics_and_none_of_the_replaced_ones(self):
        rows = [r for r in dt.rows("rubrics.yaml#phase_rubric") if r["phase"] == "P1"]
        self.assertEqual([r["id"] for r in rows], P1_RUBRICS)
        by = {r["id"]: r for r in rows}
        self.assertEqual((by["rubric_p1_secret_trail"]["scope"], by["rubric_p1_secret_trail"]["critics"]), ("dm-only", 2))
        self.assertTrue(all(r["scope"] == "phase" and r["critics"] == 1 for r in rows if r["id"] != "rubric_p1_secret_trail"))
        self.assertIn("any one of its three clues", by["rubric_p1_secret_trail"]["question"], "build item 18e: the threat's hidden half")
        text = json.dumps(rows)
        for gone in ("rubric_p1_question_not_adjective", "rubric_p1_hundred_campaigns", "villain_answer", "world_default", "act order", "rerun"):
            self.assertNotIn(gone, text, gone)
        self.assertIn("each stage's conclusion", by["rubric_p1_secret_trail"]["question"])
        self.assertIn("Is any people told as evil by nature?", by["rubric_p1_forbidden"]["question"], "one question since build 16a")
        self.assertIn("earlier-campaigns block", by["rubric_p1_differs_from_earlier"]["question"])
        self.assertEqual(by["rubric_p1_differs_from_earlier"]["fails_when"],
                         "what the writer added (the images, what the signatures are made of, the concrete question) repeats an earlier "
                         "campaign's; a rolled row or a general theme that recurs is no fault", "errata 24.2 #31")

    def test_the_critics_judge_craft_only(self):
        lines = dpm.rubric_lines("P1", None, 1)
        self.assertTrue(lines.startswith("**Craft only.** The rolled rows are given: judge what the writer made of them, never the rolls."))
        self.assertIn("rewritten on the same rolls", lines)
        self.assertIn("Only the owner rerolls", lines)
        self.assertNotIn("rerun", lines)
        self.assertNotIn("Craft only", dpm.rubric_lines("P2", None, 1), "P1's note is P1's")
        for rid in P1_RUBRICS[:4] + P1_RUBRICS[5:]:
            self.assertIn(rid, lines)


class Card(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = birth("standard", "CARD-0001")
        self.dir = CAMPAIGNS / self.name

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_the_card_of_a_script_built_p1(self):
        card = da.build_card(self.name, "P1")
        at = [card.index(s) for s in SECTIONS]
        self.assertEqual(at, sorted(at), "every section, in the approved order")
        self.assertNotIn("## WISHES", card, "left out when the owner gave no wishes")
        for lab in ("The world's shape", "The past", "The value", "The conflict", "The break", "The escalation", "The question", "The people",
                    "The institution", "The phenomenon", "Trope breaks", "Languages"):
            self.assertRegex(card, rf"(?m)^  {re.escape(lab)} +\S", lab)
        self.assertIn("(not named yet)", card)
        self.assertIn("  (not written yet)", card, "the writer's lines stand empty")
        self.assertRegex(card, r"The escalation +3 steps \(levels 1-12\)")
        self.assertRegex(card, r"(?m)^  the threat: rolled, hidden · hidden facts: [34] of 4 · twist: (yes|no) · stages: 3 × 3 clues$")   # 18e
        self.assertNotIn("act ", card.split("## THE SECRET")[1].split("##")[0].lower(), "no clues per act")
        self.assertIsNone(re.search("[çğıöşüÇĞİÖŞÜ]", card))
        self.assertIn("the old tongue", card)
        # the audit of 14b: labels, never raw keys; what has not run says so; no "None" anywhere
        langs = next(l for l in card.splitlines() if l.startswith("  Languages"))
        naming0 = json.loads((self.dir / "design/naming.json").read_text(encoding="utf-8"))
        want = {"people": "the people's tongue", "common": "the common tongue", "other_side": "the other side's tongue",
                "institution": "the institution's tongue", "old": "the old tongue"}
        self.assertEqual(langs.split(None, 1)[1].split(" · "), [want[k] for k in naming0["languages"]])
        self.assertEqual([L["label"] for L in naming0["languages"].values()], [want[k] for k in naming0["languages"]], "naming.json says the same")
        self.assertNotRegex(langs, r"other_side|people ·")
        self.assertIn("  door: not run yet · ", card)
        self.assertIn("validator: not run yet", card)
        self.assertNotIn("None", card)
        run("designer.py", "-c", self.name, "phase", "P1", "check", check=False)
        self.assertRegex(da.build_card(self.name, "P1"), r"validator: \d+ errors")
        (self.dir / "design/_staging/P1").mkdir(parents=True, exist_ok=True)
        (self.dir / "design/_staging/P1/merge.report.json").write_text(json.dumps({"refused": {}}), encoding="utf-8")
        self.assertIn("  door: passed · ", da.build_card(self.name, "P1"))
        (self.dir / "design/_staging/P1/merge.report.json").write_text(json.dumps({"refused": {"x": ["y"]}}), encoding="utf-8")
        self.assertIn("  door: 1 unit(s) refused · ", da.build_card(self.name, "P1"))
        (self.dir / "design/_staging/P1/merge.report.json").unlink()
        card = da.build_card(self.name, "P1")
        # no dice: no roll label, no row id, no candidate list
        m = dm.load(self.name)
        log = json.loads((self.dir / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))
        for r in m["dice_log"]:
            if r["phase"] == "P1" and r.get("row_id") and "_" in str(r["row_id"]):
                self.assertNotIn(r["row_id"], card, "a row id is on the card")
            self.assertNotIn(f" {r['label']} ", card)
        naming = json.loads((self.dir / "design/naming.json").read_text(encoding="utf-8"))
        shown = sum(1 for s in naming["candidates"].values() for c in s["names"] if c["name"] in card)
        self.assertEqual(shown, 0, "the candidates a name is picked from are not shown")
        # no secret row, no secret-stock name
        for n, r in enumerate(log["rolls"]):
            secret_row = dt.row(r["table"], r["row_id"]) if r.get("row_id") and ".yaml" in str(r.get("table")) else None
            if secret_row:
                self.assertNotIn(secret_row["id"], card, f"secret row {n}")
                for key in ("statement", "cause", "rule"):
                    if isinstance(secret_row.get(key), str) and len(secret_row[key]) > 20:
                        self.assertNotIn(secret_row[key], card, f"secret row {n}: its {key}")
        stock = json.loads((self.dir / "design/dm-only/name-pool-secret.json").read_text(encoding="utf-8"))
        leaked = [e["name"] for L in stock["languages"].values() for v in L.values() for e in v if re.search(rf"(?<!\w){re.escape(e['name'])}(?!\w)", card)]
        self.assertEqual(len(leaked), 0, f"{len(leaked)} secret-stock name(s) on the card")
        self.assertEqual(run("designer.py", "-c", self.name, "phase", "P1", "card").returncode, 0, "the card passes its own leak scan")

    def test_the_promise_counts_are_the_ledgers(self):
        public, secret = dm.load(self.name)["promises"], dp.load_secret(self.name)
        c = dp.counts(public, secret, "P1")
        card = da.build_card(self.name, "P1")
        self.assertIn(f"  due at P1: {c['due']['total']} — kept 0, not kept 0, waived 0, open {c['due']['open']}", card)
        self.assertIn("  open: " + " · ".join(f"{k} {v}" for k, v in c["open_by_due"].items()), card)
        self.assertIn(f"  secret: {len(secret)} open, 0 kept, 0 not kept", card)
        mine = next(p for p in public if p["due"] == "P1" and p["check"] == "critic")
        hidden = next(p for p in secret if p["due"] == "P1" and p["check"] == "critic")
        dp.judge(self.name, "P1", [{"id": mine["id"], "verdict": "not_kept"}, {"id": hidden["id"], "verdict": "not_kept"}])
        card = da.build_card(self.name, "P1")
        self.assertIn(f"    not kept: {mine['name']} → {mine['text']}", card)
        self.assertRegex(card, r"  secret: \d+ open, 0 kept, 1 not kept")
        self.assertNotIn(hidden["text"], card)
        self.assertNotIn(hidden["id"], card)

    def test_with_a_writers_output_the_lines_are_filled(self):
        naming = json.loads((self.dir / "design/naming.json").read_text(encoding="utf-8"))
        slug = self.name.replace("-", "_")
        rows = {}
        for slot in ("people", "institution", "phenomenon"):
            name = naming["candidates"][slot]["names"][0]["name"]
            rows[f"signature_{slot}"] = row(f"signature_{slot}", "signature", name, created_phase="P1", slot=slot, rule=f"what a native knows of the {slot}.", summary="one line.")
        rows[f"premise_{slug}"] = row(f"premise_{slug}", "premise", "The premise", created_phase="P1", summary="one line.",
                                      question="who keeps the road when the keepers are gone?", pitch="One. Two. Three.")
        doc = {"_meta": {"schema_version": 1, "campaign": self.name}, "entities": rows}
        (self.dir / "design/dm-only").mkdir(parents=True, exist_ok=True)
        (self.dir / "design/dm-only/entities.json").write_text(json.dumps(doc), encoding="utf-8")
        (self.dir / "design/entities.json").write_text(json.dumps(doc), encoding="utf-8")
        card = da.build_card(self.name, "P1")
        people = rows["signature_people"]["name"]
        self.assertRegex(card, rf"The people +{re.escape(people)} — .+; what a native knows of the people\.")
        self.assertIn("— who keeps the road when the keepers are gone?", card)
        self.assertIn("  One. Two. Three.", card)
        self.assertNotIn("(not named yet)", card)
        self.assertIn(f"the {people} tongue", card, "once the people is named, its tongue is called by it")
        self.assertNotIn("the people's tongue", card)
        self.assertNotIn("None", card)
        self.assertNotIn("(not written yet)", card)
        other = naming["candidates"]["people"]["names"][1]["name"]
        self.assertNotIn(other, card, "the chosen name only")

    def test_your_moves_names_only_commands_that_exist(self):
        card = da.build_card(self.name, "P1")
        self.assertIn("  approve · rerun · reroll a name (people | institution | phenomenon) · waive a promise", card)
        moves = dict(da.P1_MOVES)
        self.assertEqual(run("designer.py", "-c", self.name, "phase", "P1", "approve", "--help").returncode, 0)
        help_phase = run("designer.py", "-c", self.name, "phase", "--help").stdout
        for word in ("approve", "rerun", "--reason", "--reseed", "--onay"):
            self.assertIn(word, help_phase, word)
        self.assertIn("phase P1 approve", moves["approve"])
        self.assertIn("phase P1 rerun", moves["rerun"])
        names_help = run("design_names.py", "-c", self.name, "reroll", "--help").stdout
        self.assertTrue("--slot" in names_help and "--onay" in names_help and "design_names.py" in moves["reroll a name (people | institution | phenomenon)"])
        promise_help = run("designer.py", "-c", self.name, "promise", "--help").stdout
        self.assertTrue("waive" in promise_help and "--onay" in promise_help and "promise waive" in moves["waive a promise"])
        for _, cmd in da.P1_MOVES:
            self.assertIn(cmd.format(c=self.name), card)


class LegacyAndFields(unittest.TestCase):

    def test_a_legacy_card_is_unchanged(self):
        guard = MarkerGuard().__enter__()
        c = TestCampaign("card")
        try:
            self.assertFalse(da.scripted_p1(dm.load(c.name)))
            card = da.build_card(c.name, "P1")
            self.assertIn("# Phase card — P1 (premise)", card)
            self.assertIn("## Born in this phase (public)", card)
            self.assertNotIn("THE FOUNDATION", card)
            self.assertNotIn("Craft only", dpm.render(c.name, "P1.premise"))
        finally:
            c.remove()
            guard.__exit__(None, None, None)

    def test_the_premise_rows_last_tr_names_go_and_the_old_ones_still_load(self):
        for name in ("pitch", "secret", "villain_answer", "dm_pitch", "secret_class", "world_default"):
            self.assertEqual(text_field({name: "new", f"{name}_tr": "old"}, name), "new")
            self.assertEqual(text_field({f"{name}_tr": "old"}, name), "old", "a legacy row's name still loads")
        prompt = (SCRIPTS.parent / "prompts" / "design" / "P1.premise.md").read_text(encoding="utf-8")
        for old in ("pitch_tr", "secret_tr", "villain_answer_tr", "dm_pitch_tr", "secret_class_tr", "world_default_tr"):
            self.assertNotIn(old, prompt, old)
        for new in ("`pitch`", "`secret_class`", "`secret`", "`villain_answer`", "`dm_pitch`"):
            self.assertIn(new, prompt, new)
        docs = (SCRIPTS.parents[3] / "docs" / "schemas" / "entities.md").read_text(encoding="utf-8")
        self.assertIn("read through `design_io.text_field`", docs)
        import inspect
        import design_check
        import design_door
        self.assertIn('"villain_answer", "dm_pitch"', inspect.getsource(design_check.check_secrecy), "the verbatim-leak scan reads the new names")
        self.assertIn('row.get("secret_class")', inspect.getsource(design_door.Door.premise_errors))


if __name__ == "__main__":
    if "--report" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--report") + 1]
        os.makedirs(out_dir, exist_ok=True)
        guard = MarkerGuard().__enter__()
        backup = USED.read_bytes() if USED.is_file() else None
        try:
            for scale in ("short", "standard", "epic"):
                name = birth(scale, f"CARD-{scale.upper()}")
                try:
                    text = da.build_card(name, "P1").replace(name, f"_test-card-{scale}")
                    with open(os.path.join(out_dir, f"p1-card-{scale}.md"), "w", encoding="utf-8") as fh:
                        fh.write(text)
                    print(f"{scale}: {len(text.split())} words, {text.count(chr(10))} lines")
                finally:
                    shutil.rmtree(CAMPAIGNS / name, ignore_errors=True)
        finally:
            if backup is not None:
                USED.write_bytes(backup)
            elif USED.is_file():
                USED.unlink()
            guard.__exit__(None, None, None)
        print("cards:", out_dir)
    else:
        unittest.main()
