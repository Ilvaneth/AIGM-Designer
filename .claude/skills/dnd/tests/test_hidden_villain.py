"""
test_hidden_villain.py — build item 19b (docs/p1-build-19.md, Part 19b): a villain that hides among people can pass as
one. The visibility that hides it as a person among people needs a creature that passes (a humanoid; a Shapechanger,
Change Shape or Illusory Appearance that names a humanoid form; a disguise spell it casts at will, by the day or from
its slots; the vampire in its own form), else a mask is rolled, recorded in the threat and promised to P4 or P6; the
mask is a fourth candidate for the weakness where it fits. Failure messages give counts and positions, never a secret
row.
"""

import json
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import _corpus  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402
import design_threat as dth  # noqa: E402

V = "antagonists.yaml#"
FITTING = {"item", "possessed", "glamour"}       # the masks the weakness of the mask fits (the agent is no mask it stands behind)


class Rules(unittest.TestCase):

    def test_the_passing_rule_on_the_srd(self):
        passes = lambda k: dth.passes_as_person({"index": k})
        for k in ("doppelganger", "rakshasa", "lamia", "night-hag", "green-hag", "oni", "deva", "adult-gold-dragon",
                  "succubusincubus", "vampire-vampire", "bandit-captain"):
            if k in dth.srd_index():
                self.assertTrue(passes(k), k)
        for k in ("imp", "quasit", "mimic", "adult-red-dragon", "lich", "beholder"):
            if k in dth.srd_index():
                self.assertFalse(passes(k), k)
        self.assertTrue(dth.passes_as_person({"reskin": {"base": "doppelganger", "target_cr": 9}}), "a reskin passes by its base")

    def test_the_index_holds_what_the_rule_reads(self):
        idx = dth.srd_index()
        self.assertIn("disguise self", idx["rakshasa"]["spells_daily"])
        self.assertTrue(idx["doppelganger"]["takes_humanoid_form"])
        self.assertFalse(idx["imp"]["takes_humanoid_form"], "an imp's shapes are beasts")

    def test_the_mask_table(self):
        head = dt.roll_header(V + "mask")
        self.assertTrue(head.get("secret"))
        rows = dt.rows(V + "mask")
        self.assertEqual(len(rows), 4)
        claims = json.dumps(dt.load("claims.yaml"))
        for r in rows:
            self.assertIn(f"mask:{r['kind']}", claims, "the mask's token is registered")
            self.assertEqual({h["phase"] for h in r["hooks"]}, {"P6"} if r["kind"] in ("item", "glamour") else {"P4"}, "an item at a site, or a mortal")
        weak = dt.row(V + "weakness", "weak_strip_the_mask")
        self.assertEqual(set(weak["requires"]["any_of"]), {f"mask:{k}" for k in FITTING})
        self.assertEqual(dth.HIDDEN_AMONG_PEOPLE, ("vis_mystery_among_candidates",))


class ManySeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = _corpus.births(3000)

    def test_no_hidden_villain_without_a_way_to_pass(self):
        hidden = masked = 0
        for d, R in self.runs:
            th = R.threat
            if th["visibility"] in dth.HIDDEN_AMONG_PEOPLE:
                hidden += 1
                self.assertEqual(th["passes_as_person"], dth.passes_as_person(th["creature"]))
                self.assertTrue(th["passes_as_person"] or th["mask"], "a hidden villain that cannot pass wears a mask")
                self.assertEqual(bool(th["mask"]), not th["passes_as_person"])
                masked += bool(th["mask"])
            else:
                self.assertIsNone(th["mask"], "a mask only where the villain hides among people")
        self.assertGreater(hidden, 100)
        self.assertGreater(masked, 20)
        type(self).counts = {"hidden": hidden, "masked": masked}

    def test_the_mask_s_promise_is_in_the_secret_ledger(self):
        seen = 0
        for d, R in self.runs:
            mask = R.threat["mask"]
            if not mask:
                continue
            seen += 1
            public, secret = dp.build(d, R.public, R.secret, R.foundation, R.identity, R.identity_secret)
            mine = [p for p in secret if p["from"] == mask or any(a.get("from") == mask for a in p.get("also") or [])]
            self.assertTrue(mine, "the mask's promise")
            self.assertEqual({p["due"] for p in mine}, {"P6"} if dt.row(V + "mask", mask)["kind"] in ("item", "glamour") else {"P4"})
            self.assertFalse(mask in json.dumps(public), "the public ledger names no mask")
        self.assertGreater(seen, 20)

    def test_the_weakness_of_the_mask_only_with_its_mask(self):
        took = 0
        for d, R in self.runs:
            if R.threat["weakness"] == "weak_strip_the_mask":
                took += 1
                self.assertIn(dt.row(V + "mask", R.threat["mask"])["kind"], FITTING)
        self.assertGreater(took, 0, "the fourth candidate is drawn")

    def test_the_families_are_still_drawn(self):
        self.assertEqual(len(Counter(R.threat["family"] for d, R in self.runs)), len(dt.rows(V + "villain_family")))


if __name__ == "__main__":
    unittest.main()
