"""
test_arbiter_faults.py — build item 7a: the arbiter's three faults and two additions (docs/reports/
tags-grouping-analysis-1.md §4).

1. A public die's size no longer tells what the secret layer took out of its pool: the public record counts the die
   over the rows not publicly excluded; the real size and face are in dm-only.
2. A phase's draw stands only on the phases before it: a rerolled P1 is never filtered by the stale P2-P4 rolls.
3. A table's own header decides `avoid_used`: the actions and scars wait three births and are never exhausted.
4. The usage fallback is relaxed one kind at a time: family_wait, used_elsewhere, row_wait, the pair last.
5. `families_distinct` is read: several rows drawn from such a table for one roll never share a family.
"""

import json
import random
import sys
import unittest

from _campaign import SCRIPTS, TestCampaign, USED

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

TABLE = SCRIPTS.parent / "data" / "design" / "_test_faults.yaml"
FIVE = "rows:\n" + "".join(f"  - {{id: pf{i}, label: public {i}}}\n" for i in range(1, 6))
ROWS5 = [{"id": f"pf{i}", "label": f"public {i}"} for i in range(1, 6)]
# a secret row that bars two of the five public rows
CONFLICTS = {"secret_x": frozenset({"pf2", "pf4"}), "pf2": frozenset({"secret_x"}), "pf4": frozenset({"secret_x"})}


class DieSize(unittest.TestCase):
    """7a-1."""

    def test_the_public_view_counts_the_die_over_the_rows_not_publicly_excluded(self):
        ctx = arb.Context(rolled={"secret_x": True})
        res = arb.arbitrate("t", ROWS5, ctx, conflicts=CONFLICTS, secret_ids={"secret_x"})
        self.assertEqual([r["id"] for r in res["pool"]], ["pf1", "pf3", "pf5"])
        self.assertEqual([r["id"] for r in res["visible"]], ["pf1", "pf2", "pf3", "pf4", "pf5"])
        for seed in range(20):
            picked = arb.pick(random.Random(seed), res["pool"], res["weights"])
            shown, real = arb.public_view(res, picked)
            self.assertEqual(shown["notation"], "d5")
            self.assertEqual(shown["row_id"], picked["row_id"], "the drawn row is the same")
            self.assertEqual(shown["raw"], int(picked["row_id"][2:]), "its face is its place among the visible rows")
            self.assertEqual(real, {"notation": "d3", "raw": picked["raw"]})

    def test_without_a_secret_exclusion_the_record_is_as_before(self):
        res = arb.arbitrate("t", ROWS5, arb.Context(), exclude={"pf2"}, conflicts={}, secret_ids=set())
        picked = arb.pick(random.Random(1), res["pool"], res["weights"])
        shown, real = arb.public_view(res, picked)
        self.assertIs(shown, picked)
        self.assertIsNone(real)
        self.assertEqual(picked["notation"], "d4")

    def test_a_birth_keeps_the_real_die_in_dm_only(self):
        c = TestCampaign("faults")
        TABLE.write_text(FIVE, encoding="utf-8")
        real_indexes = dt.indexes
        dt.indexes = lambda: (CONFLICTS, frozenset({"secret_x"}))
        try:
            plain = designer.Roller(c.name, "P2", attempt=7)
            before = plain.table("faults.plain", "_test_faults.yaml", avoid=False)
            self.assertEqual(before["notation"], "d5", "no secret exclusion: the record is today's")
            R = designer.Roller(c.name, "P2", attempt=8)
            R.ctx.add("secret_x", True)
            rec = R.table("faults.public", "_test_faults.yaml", avoid=False)
            R.flush()
            self.assertEqual(rec["notation"], "d5")
            self.assertEqual(rec["excluded"], [])
            public = c.path("design/design.json").read_text(encoding="utf-8")
            self.assertNotIn("secret_x", public, "the secret row is nowhere in design.json")
            log = c.json("design/dm-only/dice-log.json")
            note = next(n for n in log["exclusions"] if n["label"] == "faults.public")
            self.assertEqual(note["notation"], "d3", "the real die is in dm-only")
            self.assertEqual({e["row"] for e in note["excluded"]}, {"pf2", "pf4"})
            self.assertEqual([r["id"] for r in ROWS5 if r["id"] not in ("pf2", "pf4")][note["raw"] - 1], rec["row_id"])
            # a secret draw keeps its own record
            S = designer.Roller(c.name, "P2", attempt=9)
            S.ctx.add("secret_x", True)
            srec = S.table("faults.secret", "_test_faults.yaml", avoid=False, secret=True)
            self.assertEqual(srec["notation"], "d3")
        finally:
            dt.indexes = real_indexes
            TABLE.unlink()
            c.remove()


class PhaseOrder(unittest.TestCase):
    """7a-2."""

    def setUp(self):
        self.c = TestCampaign("faultorder")
        m = self.c.json("design/design.json")
        rec = lambda ph, row, att=1: {"phase": ph, "table": "t", "label": f"{ph}.{row}", "row_id": row, "attempt": att}
        m["dice_log"] = [rec("P1", "p1_old", 1), rec("P1", "p1_new", 2), rec("P2", "p2_pub"), rec("P3", "p3_pub")]
        self.c.write_json("design/design.json", m)
        self.c.write_json("design/dm-only/dice-log.json", {"rolls": [rec("P1", "p1_secret", 2), rec("P2", "p2_secret"), rec("P3", "p3_secret")]})

    def tearDown(self):
        self.c.remove()

    def test_a_rerolled_p1_never_sees_the_later_phases(self):
        self.assertEqual(dd.prior_rolls(self.c.name, "P1"), {})
        ctx = dd.context(self.c.name, "P1")
        conflicts = {"a": frozenset({"p2_pub"}), "b": frozenset({"p3_secret"}), "p2_pub": frozenset({"a"}), "p3_secret": frozenset({"b"})}
        res = arb.arbitrate("t", [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], ctx, conflicts=conflicts, secret_ids=set())
        self.assertEqual([r["id"] for r in res["pool"]], ["a", "b"], "no later phase is a reason for an exclusion in P1")
        self.assertEqual(res["excluded"] + res["excluded_secret"], [])

    def test_p3_stands_on_the_latest_attempts_of_p1_and_p2(self):
        self.assertEqual(dd.prior_rolls(self.c.name, "P3"), {"p1_new": False, "p1_secret": True, "p2_pub": False, "p2_secret": True})
        self.assertEqual(set(dd.prior_rolls(self.c.name, "P2")), {"p1_new", "p1_secret"})

    def test_a_caller_outside_the_birth_order_sees_every_phase(self):
        for phase in (None, "detail"):
            self.assertEqual(set(dd.prior_rolls(self.c.name, phase)),
                             {"p1_new", "p1_secret", "p2_pub", "p2_secret", "p3_pub", "p3_secret"})

    def test_the_roller_and_the_cli_roll_give_their_phase(self):
        R = designer.Roller(self.c.name, "P1", attempt=3)
        self.assertEqual(R.ctx.rolled, {})
        self.assertEqual(set(designer.Roller(self.c.name, "P3", attempt=2).ctx.rolled), {"p1_new", "p1_secret", "p2_pub", "p2_secret"})
        TABLE.write_text(FIVE, encoding="utf-8")
        real_indexes = dt.indexes
        dt.indexes = lambda: ({"pf1": frozenset({"p3_pub"}), "p3_pub": frozenset({"pf1"}),
                               "pf2": frozenset({"p1_new"}), "p1_new": frozenset({"pf2"})}, frozenset())
        try:
            rec = dd.roll(self.c.name, "P2", "faults.cli", "_test_faults.yaml", None, False, False, 5)
            self.assertEqual(rec["excluded"], [{"row": "pf2", "why": "conflict", "with": "p1_new"}],
                             "P2 is filtered by P1, never by P3")
        finally:
            dt.indexes = real_indexes
            TABLE.unlink()


class OwnPhase(unittest.TestCase):
    """7a-6: a hand roll stands on the earlier phases and on what its own phase's attempt already rolled."""

    def test_the_second_hand_roll_of_a_phase_sees_the_first(self):
        c = TestCampaign("faultown")
        TABLE.write_text(FIVE, encoding="utf-8")
        real_indexes = dt.indexes
        try:
            m = c.json("design/design.json")
            m["dice_log"] = [{"phase": "P3", "table": "t", "label": "P3.later", "row_id": "p3_later", "attempt": 1}]
            c.write_json("design/design.json", m)
            c.write_json("design/dm-only/dice-log.json", {"rolls": []})
            dt.indexes = lambda: ({}, frozenset())
            first = dd.roll(c.name, "P2", "own.1", "_test_faults.yaml", None, False, False, 4)["row_id"]
            other = next(r["id"] for r in ROWS5 if r["id"] != first)
            later = next(r["id"] for r in ROWS5 if r["id"] not in (first, other))
            dt.indexes = lambda: ({other: frozenset({first}), first: frozenset({other}),
                                   later: frozenset({"p3_later"}), "p3_later": frozenset({later})}, frozenset())
            second = dd.roll(c.name, "P2", "own.2", "_test_faults.yaml", None, False, False, 4)
            self.assertEqual(second["excluded"], [{"row": other, "why": "conflict", "with": first}],
                             "the first roll stays: its conflict leaves the second pool; the later phase is not seen")
            self.assertNotEqual(second["row_id"], other)
            # another attempt of the same phase does not count
            third = dd.roll(c.name, "P2", "own.3", "_test_faults.yaml", None, False, False, 5)
            self.assertEqual(third["excluded"], [])
            # a secret roll of the same attempt counts, and stays secret on the public record
            dd.roll(c.name, "P2", "own.secret", "_test_faults.yaml", None, True, False, 6)
            sec = c.json("design/dm-only/dice-log.json")["rolls"][-1]["row_id"]
            barred = next(r["id"] for r in ROWS5 if r["id"] != sec)
            dt.indexes = lambda: ({barred: frozenset({sec}), sec: frozenset({barred})}, frozenset())
            fourth = dd.roll(c.name, "P2", "own.4", "_test_faults.yaml", None, False, False, 6)
            self.assertEqual(fourth["excluded"], [], "a reason that names a secret roll goes to dm-only")
            self.assertEqual(fourth["notation"], "d5")
            self.assertNotEqual(fourth["row_id"], barred)
        finally:
            dt.indexes = real_indexes
            TABLE.unlink()
            c.remove()


class Waits(unittest.TestCase):
    """7a-3: fifteen births in a row on the suite's own used.json."""

    def setUp(self):
        self.backup = USED.read_bytes() if USED.is_file() else None

    def tearDown(self):
        if self.backup is not None:
            USED.write_bytes(self.backup)
        elif USED.is_file():
            USED.unlink()

    def births(self, ref, n=15):
        """Draw one row per birth; return [(birth, row, pool ids, fallback)]."""
        rows = dt.rows(ref)
        used = {"campaigns": {}, "births": {}}
        out = []
        for i in range(n):
            name = f"_test-seq-{i:02d}"
            dd.save_used(used)
            res = arb.arbitrate(ref, rows, arb.Context(dials={"magic": "high", "scale": "epic"}), usage=dd.usage(name, ref),
                                conflicts={}, secret_ids=set())
            row = arb.pick(random.Random(f"{ref}:{i}"), res["pool"], res["weights"])["row_id"]
            out.append((name, row, [r["id"] for r in res["pool"]], res["usage_fallback"]))
            used = dd.load_used()
            used["campaigns"][name] = {ref: [row]}
            used.setdefault("births", {})[name] = {"first_approved": f"2026-10-{i + 1:02d}T00:00:00Z"}
        return out

    def test_actions_and_scars_wait_three_births_and_are_never_exhausted(self):
        for ref in ("foundation.yaml#action", "foundation.yaml#scar"):
            seq = self.births(ref)
            n_rows = len(dt.rows(ref))
            for i, (name, row, pool, fallback) in enumerate(seq):
                with self.subTest(table=ref, birth=i):
                    self.assertIsNone(fallback, "the pool never empties")
                    waiting = {r for _, r, _, _ in seq[max(0, i - 3):i]}
                    self.assertFalse(waiting & set(pool), "the last three births' rows wait")
                    self.assertEqual(len(pool), n_rows - len(waiting), "nothing else is out: no permanent exclusion")
                    if i >= 4:
                        self.assertIn(seq[i - 4][1], pool, "a row may be drawn again at the fourth birth")
            self.assertNotIn("used_elsewhere", dd.usage("_test-next", ref), "the header's avoid_used: false holds")

    def test_the_header_wins_over_the_callers_argument(self):
        self.assertNotIn("used_elsewhere", dd.usage("_test-x", "foundation.yaml#scar", avoid=True))
        self.assertNotIn("used_elsewhere", dd.usage("_test-x", "foundation.yaml#time", avoid=True))
        self.assertIn("used_elsewhere", dd.usage("_test-x", "foundation.yaml#spine", avoid=False), "avoid_used: true holds too")

    def test_a_silent_header_leaves_the_caller_to_decide(self):
        # pantheon.yaml#type states no header of its own: the caller's argument is read, as before
        self.assertEqual(dt.own_roll_header("pantheon.yaml#type"), {})
        self.assertIn("used_elsewhere", dd.usage("_test-x", "pantheon.yaml#type", avoid=True))
        self.assertNotIn("used_elsewhere", dd.usage("_test-x", "pantheon.yaml#type", avoid=False))

    def test_an_avoid_used_table_behaves_as_before(self):
        seq = self.births("foundation.yaml#spine", n=6)
        for i, (name, row, pool, fallback) in enumerate(seq):
            self.assertFalse({r for _, r, _, _ in seq[:i]} & set(pool), "a used row is not drawn again while rows remain")


class GradedFallback(unittest.TestCase):
    """7a-4: nothing, then family_wait, + used_elsewhere, + row_wait, + pair."""

    ROWS = [{"id": "a", "label": "A", "family": "f1"}, {"id": "b", "label": "B", "family": "f2"},
            {"id": "c", "label": "C", "family": "f3"}, {"id": "d", "label": "D", "family": "f4"}]

    def run_(self, usage):
        res = arb.arbitrate("t", self.ROWS, arb.Context(), usage=usage, conflicts={}, secret_ids=set())
        return [r["id"] for r in res["pool"]], res["usage_fallback"]

    def test_nothing_dropped_while_a_row_is_left(self):
        self.assertEqual(self.run_({"family_wait": {"f1"}, "used_elsewhere": {"b"}, "row_wait": {"c"}}), (["d"], None))

    def test_family_wait_goes_first(self):
        self.assertEqual(self.run_({"family_wait": {"f1"}, "used_elsewhere": {"b"}, "row_wait": {"c"}, "pair": {"d"}}),
                         (["a"], "dropped: family_wait"))

    def test_used_elsewhere_goes_second_and_row_wait_still_holds(self):
        pool, fb = self.run_({"used_elsewhere": {"a", "b"}, "row_wait": {"c"}, "pair": {"d"}})
        self.assertEqual((pool, fb), (["a", "b"], "dropped: used_elsewhere"))
        self.assertNotIn("c", pool, "the row in row_wait is still out")
        pool, fb = self.run_({"family_wait": {"f4"}, "used_elsewhere": {"a", "b"}, "row_wait": {"c", "d"}})
        self.assertEqual((pool, fb), (["a", "b"], "dropped: family_wait, used_elsewhere"))

    def test_row_wait_goes_third_and_the_pair_last(self):
        self.assertEqual(self.run_({"row_wait": {"a", "b", "c"}, "pair": {"d"}}), (["a", "b", "c"], "dropped: row_wait"))
        self.assertEqual(self.run_({"pair": {"a", "b", "c", "d"}}), (["a", "b", "c", "d"], "dropped: pair"))
        self.assertEqual(self.run_({"used_elsewhere": {"a"}, "row_wait": {"b"}, "pair": {"a", "b", "c", "d"}}),
                         (["a", "b", "c", "d"], "dropped: used_elsewhere, row_wait, pair"))


class FamiliesDistinct(unittest.TestCase):
    """7a-5."""

    def test_the_header_is_read_by_a_general_path(self):
        self.assertTrue(dt.roll_header("trope-breaks.yaml")["families_distinct"])
        fam = {r["id"]: r["family"] for r in dt.rows("trope-breaks.yaml")}
        self.assertEqual(dd.taken_families("trope-breaks.yaml", ["break_rule_by_lottery"]), {"governance"})
        self.assertEqual(dd.taken_families("foundation.yaml#spine", ["spine_river_to_sea"]), set(), "only where the header says so")
        where, why = dd.distinct_filter("trope-breaks.yaml", ["break_rule_by_lottery"])
        res = arb.arbitrate("trope-breaks.yaml", dt.rows("trope-breaks.yaml"), arb.Context(), where=where, why=why)
        self.assertFalse(any(fam[r["id"]] == "governance" for r in res["pool"]))
        self.assertTrue(all(e["why"] == "family_taken" for e in res["excluded"] if fam[e["row"]] == "governance"),
                        "the exclusion is logged with its reason")

    def test_two_trope_breaks_never_share_a_family_in_thousands_of_seeds(self):
        fam = {r["id"]: r["family"] for r in dt.rows("trope-breaks.yaml")}
        for i in range(3000):
            scale = ("standard", "epic")[i % 2]
            R = designer.Roller.in_memory(f"FAM-{i}", {"scale": scale, "magic": "medium", "era": "medieval"})
            a = R.table("break.1", "trope-breaks.yaml")["row_id"]
            b = R.table("break.2", "trope-breaks.yaml", exclude={a})["row_id"]      # designer.py's own call
            self.assertNotEqual(fam[a], fam[b], (R.master, a, b))

    def test_the_real_p1_preroll_draws_two_families(self):
        fam = {r["id"]: r["family"] for r in dt.rows("trope-breaks.yaml")}
        for i in range(150):
            scale = ("standard", "epic")[i % 2]
            dials = {"scale": scale, "tone": "bright", "magic": "medium", "era": "medieval", "content_mix": ["war"],
                     "party_size": 2, "level_band": [1, 12 if scale == "standard" else 20]}
            R = designer.Roller.in_memory(f"P1FAM-{i}", dials)
            designer.preroll_p1(R, {"dials": dials})
            breaks = [r["row_id"] for r in R.public if r["label"].startswith("break.")]
            self.assertEqual(len(breaks), 2)
            self.assertEqual(len({fam[b] for b in breaks}), 2, (R.master, breaks))

    def test_it_is_a_constraint_never_relaxed(self):
        """An empty pool is a table fault, not a fallback."""
        rows = [{"id": "x1", "label": "X1", "family": "one"}, {"id": "x2", "label": "X2", "family": "one"}]
        with self.assertRaises(arb.EmptyPool):
            arb.arbitrate("t", rows, arb.Context(), where=lambda r: r["family"] not in {"one"}, why="family_taken",
                          usage={"used_elsewhere": {"x1"}}, conflicts={}, secret_ids=set())


if __name__ == "__main__":
    unittest.main()
