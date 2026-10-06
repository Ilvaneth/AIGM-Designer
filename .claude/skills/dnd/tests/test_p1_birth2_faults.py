"""
test_p1_birth2_faults.py — build item 19a (docs/p1-build-19.md, Part 19a): what the second P1-only test birth showed. The
hand that is a side of the contest is named by its role, and no public surface says it was deceived; the public "No
people evil by birth — checked" section is gone; no plane is named at P1; the pitch carries the campaign's question; a
critic judges its rubrics' questions only. Failure messages name no secret row.
"""

import json
import sys
import unittest

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import _corpus  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402
from test_p1_dry_walk import Base, Walker  # noqa: E402

TELLS = ("unwitting", "deceived", "does not know what it did")
TEMPLATE = (SCRIPTS.parent / "templates" / "design" / "premise.md").read_text(encoding="utf-8")
PROMPT = (SCRIPTS.parent / "prompts" / "design" / "P1.premise.md").read_text(encoding="utf-8")


def tells(text: str) -> list[str]:
    low = text.lower()
    return [w for w in TELLS if w in low]


class TheSideOfTheContest(unittest.TestCase):
    """#1: the hand's public face names only what the world sees."""

    def test_the_hand_row_says_nothing_of_the_deceit(self):
        row = dt.row("antagonists.yaml#hand", "hand_contest_side")
        self.assertEqual(tells(json.dumps(row)), [])
        self.assertEqual(dt.row("antagonists.yaml#hand", "hand_deceived_side")["id"], "hand_contest_side", "a legacy birth's id reads")
        for h in dt.rows("antagonists.yaml#hand"):
            self.assertEqual(tells(h["text"]["subject"] + " " + h["label"]), [], h["id"])

    def test_the_corpus_births_with_the_side_as_hand(self):
        tenses = {r["id"]: r["tense"] for r in dt.rows("foundation.yaml#time")}
        seen = 0
        for d, R in _corpus.births(3000):
            f = R.foundation
            if f["move"]["hand"] != "hand_contest_side":
                continue
            seen += 1
            role = f["move"]["hand_role"]
            if f["move"].get("state") == "move_unnoticed":
                self.assertTrue(f["spine_sentence"].lower().replace("a generation ago, ", "").startswith("someone "), "unnoticed: no hand named")
                continue
            main = f["contests"][0]
            contest = dt.row("foundation.yaml#contest", main["id"])
            self.assertIn(role, main["roles"])
            self.assertNotEqual(role, f["break"].get("target_role"), "the side never strikes itself")
            subject = fd.role_short(contest, role)
            lead = "A generation ago, " if f["break"]["time"] == "time_generation_ago" else ""
            s = f["spine_sentence"]
            self.assertTrue(s.lower().startswith((lead + subject + " ").lower()), "the role is the subject")
            if tenses[f["break"]["time"]] != "past":
                verb = "are " if fd.role_number(contest, role) == "plural" else "is "
                self.assertTrue(s[len(lead + subject) + 1:].startswith(verb), "the verb agrees with the role")
            public, _ = dp.build(d, R.public, R.secret, R.foundation, R.identity, R.identity_secret)
            for where, text in (("the sentence", s), ("the rendering", json.dumps(f["rendering"])), ("the public ledger", json.dumps(public)),
                                ("the public rolls", json.dumps(R.public)), ("the foundation", json.dumps(f))):
                self.assertEqual(tells(text), [], where)
        self.assertGreater(seen, 50)

    def test_an_unnoticed_move_names_no_hand(self):
        """The audit's correction: an unnoticed move's sentence says "someone" (a hand of people) or "something"; the
        records keep the hand."""
        seen = 0
        for d, R in _corpus.births(3000):
            m = R.foundation["move"]
            if m.get("state") != "move_unnoticed":
                continue
            seen += 1
            hidden = R.threat["hand"]
            want = "someone " if "humanoid" in hidden["families"] else "something "
            body = R.foundation["spine_sentence"].lower().replace("a generation ago, ", "")
            self.assertTrue(body.startswith(want), "the subject")
            self.assertFalse(body.startswith(want + "are "), "singular")
            # the refined correction: the hand is a secret roll; no public surface carries it
            self.assertEqual((m["hand"], m["hand_role"], m["families"]), (None, None, []))
            self.assertEqual(R.threat["families"]["public"], [])
            hand = dt.row("antagonists.yaml#hand", hidden["id"])
            public, _ = dp.build(d, R.public, R.secret, R.foundation, R.identity, R.identity_secret)
            for where, text in (("the rendering", json.dumps(R.foundation["rendering"])), ("the public ledger", json.dumps(public)),
                                ("the public rolls", json.dumps(R.public)), ("the foundation", json.dumps(R.foundation))):
                self.assertNotIn(hidden["id"], text, where)
                self.assertFalse(any(f"hand_family:{x}" in text for x in hidden["families"]), where)
            self.assertNotIn(hand["text"]["subject"], body.split("; now ")[0], "the hand is not named")
            self.assertTrue(any(r.get("row_id") == hidden["id"] for r in R.secret), "the roll is in dm-only")
        self.assertGreater(seen, 300)
        self.assertEqual(dt.row("antagonists.yaml#hand", "hand_bound_elemental")["text"]["subject"], "an elemental")

    def test_the_writer_is_told(self):
        self.assertIn("never say it was deceived", PROMPT)
        self.assertIn("`move.hand_role`", PROMPT)
        self.assertIn("only \"someone\" or \"something\"", PROMPT)


class Texts(unittest.TestCase):

    def test_the_check_line_is_gone(self):
        """#2: the template and the prompt hold no public "checked" line; the rubric judges the prose."""
        self.assertNotIn("No people evil by birth — checked", TEMPLATE)
        self.assertNotIn("evil by birth — checked", PROMPT)
        rubric = dt.row("rubrics.yaml#phase_rubric", "rubric_p1_forbidden")
        self.assertIn("no line that says it was checked", rubric["question"])

    def test_the_pitch_carries_the_question(self):
        """#4: the pitch's three jobs, in the prompt, the template and the legibility rubric."""
        for text in (PROMPT, TEMPLATE):
            self.assertIn("the campaign's question, asked in this world's words and never answered", text)
        rubric = dt.row("rubrics.yaml#phase_rubric", "rubric_p1_legible")
        self.assertIn("ask the campaign's question", rubric["question"])
        self.assertIn("does not ask the question", rubric["fails_when"])

    def test_no_plane_in_the_prompt_s_bars(self):
        self.assertIn("No plane is named at P1", PROMPT)

    def test_the_critics_judge_their_rubrics_only(self):
        for name in ("critic.md", "phase_critic.md"):
            text = (SCRIPTS.parent / "prompts" / "design" / name).read_text(encoding="utf-8")
            self.assertIn("a fault no rubric of yours asks about is a `note`, never a `fix`", text, name)


class Births(Base):

    def walk_to_the_side(self) -> Walker:
        """A birth whose hand is a side of the contest (seeds tried in order; the dials are the seed's own)."""
        for n in range(120):
            w = Walker("standard", f"SIDE-{n:03d}")
            w.born()
            if dm.load(w.name)["foundation"]["move"]["hand"] == "hand_contest_side":
                self.walkers.append(w)
                return w
            w.remove()
        self.fail("no seed of 120 drew the side of the contest as the hand")

    def test_the_card_and_the_ledger_of_a_side_s_birth(self):
        w = self.walk_to_the_side()
        w.write()
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "card")
        card = (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        m = dm.load(w.name)
        self.assertIn(m["foundation"]["spine_sentence"], card, "the story sentence, its subject the side")
        for where, text in (("the card", card), ("the public ledger", json.dumps(m["promises"])),
                            ("design.json", (w.dir / "design/design.json").read_text(encoding="utf-8"))):
            self.assertEqual(tells(text), [], where)

    def test_a_legacy_premise_with_the_check_section_merges(self):
        w = self.walker()
        w.write(public_extra="\n### No people evil by birth — checked\n*The keepers and the road folk are people like any other.*\n")
        merge = w.d("phase", "P1", "merge")
        self.assertIn(w.premise_id, w.merged(), merge.stderr[-800:])

    def test_a_plane_named_in_the_public_prose_is_refused(self):
        w = self.walker()
        w.write(public_extra="\nThe old gate is said to open on the Astral Plane.\n")
        proc = w.d("phase", "P1", "merge", check=False)
        refused = w.json("design/_staging/P1/merge.report.json").get("refused") or {}
        self.assertTrue(any("names a plane (Astral Plane)" in l and "chosen at P2" in l for l in refused.get(w.premise_id, [])),
                        proc.stderr[-800:])
        self.assertNotIn(w.premise_id, w.merged())

    def test_a_plane_named_in_the_mirror_is_refused_by_count(self):
        w = self.walker()
        w.write(mirror_extra="The thin place opens on the Nine Hells.\n")
        proc = w.d("phase", "P1", "merge", check=False)
        refused = w.json("design/_staging/P1/merge.report.json").get("refused") or {}
        lines = refused.get(w.premise_id, [])
        self.assertTrue(any("the dm-only prose names 1 plane(s)" in l for l in lines), proc.stderr[-800:])
        self.assertFalse(any("Nine Hells" in l for l in lines), "the dm-only name stays in the door log")
        log = json.loads((w.dir / "design/dm-only/door-log.json").read_text(encoding="utf-8"))
        self.assertIn("Nine Hells", json.dumps(log))

    def test_a_fix_on_a_rubric_the_critic_was_not_given_is_refused(self):
        """#5: the phase critic is not given the secret trail's rubric at P1, the entity critic no P2 rubric; a `note` on
        either is recorded."""
        w = self.walker()
        w.write()
        w.d("phase", "P1", "merge")
        for name, entity, rubric in (("phase.critic1.json", "P1", "rubric_p1_secret_trail"),
                                     (f"{w.premise_id}.critic1.json", w.premise_id, "rubric_p2_gods_carry_question")):
            ret = {"entity_id": entity, "verdict": "fix",
                   "findings": [{"rubric_id": rubric, "entity_id": w.premise_id, "verdict": "fix", "reason_code": "my_own_taste"}]}
            (w.staging / name).write_text(json.dumps(ret), encoding="utf-8")
            proc = w.d("phase", "P1", "merge", check=False)
            self.assertIn(f"a fix names a rubric this critic was not given ({rubric}), refused", proc.stdout + proc.stderr)
            self.assertTrue((w.staging / name).is_file(), "the refused return stays in staging")
            ret["verdict"], ret["findings"][0]["verdict"] = "pass", "note"
            (w.staging / name).write_text(json.dumps(ret), encoding="utf-8")
            w.d("phase", "P1", "merge")
            self.assertFalse((w.staging / name).is_file(), "a note is recorded")


class FromTheReport(Base):
    """The addendum (docs/p1-build-19.md, "Added from the birth's report"): 6, 7, 8."""

    def test_the_agents_use_their_file_tools(self):
        """6: the common block every writer and critic reads: Glob, Read, Write; Bash only for the given commands."""
        import design_prompts as dpm
        rule = "list files with Glob, read them with Read, write them with Write"
        w = self.walker()
        begin = json.loads(w.begin.stdout[w.begin.stdout.index("{"):])
        entry = begin["entities"][0]
        texts = {"writer": open(entry["prompt_file"], encoding="utf-8").read(), "critic": open(entry["critic_file"], encoding="utf-8").read(),
                 "phase critic": dpm.render(w.name, "phase_critic", None, 1, phase_override="P1")}
        for who, text in texts.items():
            self.assertIn(rule, text, who)
            self.assertIn("never on a path under `design/`", text, who)

    def test_the_report_says_who_asked_a_fix(self):
        """7: the fix reasons grouped by the critic that gave them."""
        w = self.walker()
        w.write()
        w.d("phase", "P1", "merge")
        returns = {f"{w.premise_id}.critic1.json": (w.premise_id, "rubric_p1_legible", "no_face"),
                   "phase.critic1.json": ("P1", "rubric_p1_only_true_here", "too_general")}
        for name, (entity, rubric, code) in returns.items():
            ret = {"entity_id": entity, "verdict": "fix",
                   "findings": [{"rubric_id": rubric, "entity_id": w.premise_id, "verdict": "fix", "reason_code": code}]}
            (w.staging / name).write_text(json.dumps(ret), encoding="utf-8")
        w.d("phase", "P1", "merge")
        report = w.d("phase", "P1", "report").stdout
        self.assertIn("- fix reasons: entity critic 1: rubric_p1_legible/no_face ×1; phase critic: rubric_p1_only_true_here/too_general ×1", report)

    def test_a_promise_judged_not_kept_then_kept_is_shown(self):
        """8: one line in the report: judged not kept, then kept after fix N."""
        w = self.walker()
        w.write()
        w.d("phase", "P1", "merge")
        due = w.critics(verdict="fix", promises="not_kept")
        w.d("phase", "P1", "merge")
        w.critics(verdict="pass", promises="kept")
        w.d("phase", "P1", "merge")
        public = {p["id"] for p in dm.load(w.name)["promises"]}
        flipped = sorted(p["id"] for p in due if p["id"] in public)
        self.assertTrue(flipped, "a public promise due at P1 the critic judges")
        report = w.d("phase", "P1", "report").stdout
        line = next(l for l in report.splitlines() if l.startswith("- judged not kept, then kept after fix 1: "))
        for pid in flipped:
            self.assertIn(pid, line)
        self.assertEqual(next(p for p in dm.load(w.name)["promises"] if p["id"] == flipped[0])["flipped"]["after_fix"], 1)


if __name__ == "__main__":
    unittest.main()
