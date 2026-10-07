"""
test_p1_polish.py — build item 21a (docs/p1-build-21.md): the polish the fourth test birth asked for. The question is
one short sentence per contest: the door refuses one past forty-five words, naming the contest and the count; the
prompt and the question rubric say so. A generic side (a placeholder role) is named by its noun and its seat.
"""

import re
import sys
import unittest

from _campaign import SCRIPTS
from test_p1_dry_walk import Base

sys.path.insert(0, str(SCRIPTS))
import design_door as door  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_prompts as dpm  # noqa: E402
import design_tables as dt  # noqa: E402


class TheShortQuestion(Base):

    def test_the_door_counts_each_contest_s_question(self):
        self.assertEqual([n for _, n in door.question_sentences("Is the throne worth a war? Or is a fed mountain enough?")], [6, 6])
        self.assertEqual(door.question_sentences(""), [])

    def test_a_question_past_the_limit_is_refused_with_its_count(self):
        w = self.walker()
        long_q = "Is the empty throne " + " ".join(["a prize"] * 25) + " worth the war?"
        words = door.question_sentences(long_q)[0][1]
        self.assertGreater(words, door.QUESTION_WORDS)

        def change(rows, picked):
            p = rows[w.premise_id]
            p["question"] = p["stamped"]["question"] = long_q
        w.write(change)
        w.d("phase", "P1", "merge", check=False)
        refused = w.json("design/_staging/P1/merge.report.json").get("refused") or {}
        contest = dm.load(w.name)["identity"]["questions"][0]["contest"]
        self.assertIn(f"{w.premise_id}: `question` holds a question of {words} words for {contest}", " ".join(refused.get(w.premise_id) or []))
        self.assertNotIn(w.premise_id, w.merged())
        w.write()                                       # the stand-in's short question passes
        w.d("phase", "P1", "merge")
        self.assertIn(w.premise_id, w.merged())

    def test_the_prompt_and_the_rubric_ask_for_it(self):
        w = self.walker()
        text = dpm.render(w.name, "P1.premise", w.premise_id)
        self.assertIn("**One sentence per contest, at most about thirty-five words**", text)
        self.assertIn("three short sentences", text)
        rubric = dt.row("rubrics.yaml#phase_rubric", "rubric_p1_question_concrete")
        self.assertIn("cannot be read in one breath", rubric["fails_when"])


class TheNamedSides(unittest.TestCase):
    """Build item 21a part 2 (docs/p1-build-21.md, the amendment): a generic side is named by its noun and its seat."""

    GENERIC = {"contest_divided_city": "ab", "contest_merchant_house_divides": "ab", "contest_foreign_envoy": "ab",
               "contest_war_fed_company": "ab", "contest_fallen_state_remnant": "ab", "contest_shapeshifter": "ab",
               "contest_relic_pieces": "ab", "contest_two_empires": "ab", "contest_fiend_pact": "b"}

    def test_the_tables_carry_the_approved_rows(self):
        rows = {r["id"]: r for r in dt.rows("foundation.yaml#contest")}
        marked = {(c, k) for c, r in rows.items() for k, role in r["roles"].items() if role.get("generic")}
        self.assertEqual(marked, {(c, k) for c, ks in self.GENERIC.items() for k in ks})
        self.assertTrue(all(rows[c]["roles"][k].get("noun") for c, k in marked))
        self.assertEqual({k: rows["contest_divided_city"]["roles"][k].get("toward") for k in "ab"}, {"a": "end_a", "b": "end_b"})
        spines = dt.rows("foundation.yaml#spine")
        self.assertEqual(len(spines), 30)
        for s in spines:
            ends = s["text"].get("ends_short")
            self.assertTrue(isinstance(ends, list) and len(ends) == 2 and all(ends) and ends[0] != ends[1], s["id"])

    def test_over_the_corpus_a_generic_side_reads_through_its_noun_and_seat(self):
        import _corpus
        import design_foundation as fd
        rows = {r["id"]: r for r in dt.rows("foundation.yaml#contest")}
        generic = [role for r in rows.values() for role in r["roles"].values() if role.get("generic")]
        # a label that is its role's noun too (fiend_pact's "the rival house") is read through the noun check above
        placeholders = {role.get("short") or role["text"] for role in generic} - {role["noun"] for role in generic}
        seen = 0
        for _, R in _corpus.births():
            if R is None:
                continue
            f = R.foundation
            sentence = f["spine_sentence"].lower()
            main = f["layout"]["contests"][0]
            contest = rows[main["contest"]]
            phrases = {k: fd.side_phrase(f, contest, k, main["seats"]) for k in ("a", "b")}
            self.assertNotEqual(phrases["a"], phrases["b"], f["spine_sentence"])
            for k, role in contest["roles"].items():
                if k in "ab" and role.get("generic"):
                    seen += 1
                    self.assertTrue(phrases[k].startswith(role["noun"] + (" toward " if role.get("toward") else " of ")), phrases[k])
                    self.assertIn(phrases[k].lower(), sentence)
            for ph in placeholders:
                self.assertNotRegex(sentence, r"(?<![\w-])" + re.escape(ph.lower()) + r"(?![\w-])", f["spine_sentence"])
        self.assertGreater(seen, 100, "the corpus draws generic sides")


if __name__ == "__main__":
    unittest.main()
