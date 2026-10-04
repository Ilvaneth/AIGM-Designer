"""
test_forbidden_lifted.py — build item 16a (docs/p1-build-16.md; errata 24.2 #31): a general Campaign Designer excludes
no general D&D theme. The rows the forbidden list once barred are drawn like any other, over thousands of seeds and
with no conflicting set; the three rows that still never enter a pool guard a mechanism, not a taste.
"""

import sys
import unittest

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

FREED = {"arc.yaml#opening_scene_type": {"open_tavern", "open_stranger_job"},
         "arc.yaml#plot_engine": {"engine_prophecy", "engine_collect_pieces"},
         "threads.yaml#truth_kind": {"truth_chosen", "truth_destined", "truth_amnesia"},
         "factions.yaml#cult_doctrine": {"cultdoc_evil_for_its_own_sake"},
         "antagonists.yaml#villain_shape": {"shape_dark_lord", "shape_whispering_advisor", "shape_secretly_evil_ruler"},
         "antagonists.yaml#origin": {"origin_awakened_ancient"},
         "antagonists.yaml#bbeg_faction_archetype": {"bfa_religious"}}
OWN_RULE = {"factions.yaml#fracture": "fracture_none", "factions.yaml#cult_doctrine": "cultdoc_unspecified",
            "threads.yaml#mission_verb": "verb_find_out_who"}
DIALS = {"scale": "standard", "magic": "medium", "era": "medieval", "tone": "shadowed"}


class Lifted(unittest.TestCase):

    def test_the_freed_rows_are_whole_rows(self):
        for ref, ids in FREED.items():
            for rid in ids:
                r = dt.row(ref, rid)
                self.assertIsNotNone(r, f"{ref} lost a freed row")
                self.assertFalse(r.get("forbidden") or r.get("allowed_via"), ref)
                self.assertNotIn("forbidden", r["label"].lower(), ref)
                self.assertTrue(r["hooks"] and all(h["phase"] != "validator" for h in r["hooks"]), f"{ref}: a freed row says how it propagates")

    def test_every_freed_row_is_drawn_over_thousands_of_seeds(self):
        secret = dt.secret_row_ids()
        for ref, ids in FREED.items():
            drawn = set()
            for i in range(2000):
                R = designer.Roller.in_memory(f"FREED-{i}", DIALS, phase="P4")
                drawn.add(R.table("draw", ref, secret=ref.split("#")[0] == "antagonists.yaml", avoid=False)["row_id"])
                rolled = [r["row_id"] for r in R.public + R.secret if r.get("row_id")]
                self.assertEqual(arb.conflicting_pairs(rolled), [])
                if ids <= drawn:
                    break
            self.assertEqual(len(ids - drawn), 0, f"{ref}: {len(ids - drawn)} freed row(s) never drawn")
            self.assertEqual(any(x in secret for x in ids), ref.startswith("antagonists.yaml#v") or ref.endswith("#origin")
                             or ref.endswith("#bbeg_faction_archetype"))

    def test_the_three_own_rule_rows_never_enter_a_pool(self):
        everything = arb.Context(rolled={r["id"]: False for n in dt.list_tables() for l in dt.all_row_lists(dt.load(n)).values() for r in l})
        for ref, rid in OWN_RULE.items():
            for ctx in (arb.Context(), everything):
                try:
                    pool = {r["id"] for r in arb.arbitrate(ref, dt.rows(ref), ctx)["pool"]}
                except arb.EmptyPool:
                    pool = set()
                self.assertNotIn(rid, pool, ref)


if __name__ == "__main__":
    unittest.main()
