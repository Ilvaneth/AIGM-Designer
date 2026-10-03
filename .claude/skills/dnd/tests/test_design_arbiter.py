"""
test_design_arbiter.py — the script is the only arbiter of conflicts (plan item 25, "Common rules"; the owner's
corrections A-C of 2026-09-28): conflicts are symmetric and filtered before the die; requirements, forbidden rows
and zero weights are constraints; a pool the constraints empty stops the draw; a pool only usage empties falls back
(family waits first); every exclusion carries its reason and a public record never names the secret layer; the
birth order and the waits count real births apart from test births; the small-pool constraints of P3, P4 and P6
always leave a row; the two holes of 2026-09-28 are closed.
"""

import random
import sys
import unittest

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

ROWS = [{"id": "a", "label": "A", "family": "f1"}, {"id": "b", "label": "B", "family": "f1"},
        {"id": "c", "label": "C", "family": "f2"}, {"id": "d", "label": "D", "family": "f3"}]
CONFLICTS = {"a": frozenset({"x"}), "x": frozenset({"a"})}      # a lists x; symmetric as the index makes it


def ids(res):
    return [r["id"] for r in res["pool"]]


class Conflicts(unittest.TestCase):

    def test_a_conflict_bars_both_ways_before_the_die(self):
        ctx = arb.Context(rolled={"x": False})
        res = arb.arbitrate("t", ROWS, ctx, conflicts=CONFLICTS, secret_ids=set())
        self.assertNotIn("a", ids(res))
        self.assertIn({"row": "a", "why": "conflict", "with": "x"}, res["excluded"])
        # and the other direction: x after a
        res = arb.arbitrate("t", [{"id": "x", "label": "X"}, {"id": "y", "label": "Y"}], arb.Context(rolled={"a": False}),
                            conflicts=CONFLICTS, secret_ids=set())
        self.assertEqual(ids(res), ["y"])

    def test_the_committed_index_is_symmetric(self):
        idx = dt.conflict_index()
        for a, others in idx.items():
            for b in others:
                self.assertIn(a, idx.get(b, ()), f"{a} bars {b} but not the reverse")

    def test_the_trope_break_hole_is_closed(self):
        """2026-09-28: the trope-break draw never checked a candidate's own conflicts against the question."""
        ctx = arb.Context(rolled={"tension_inheritance_merit": False})
        res = arb.arbitrate("trope-breaks.yaml", dt.rows("trope-breaks.yaml"), ctx)
        self.assertNotIn("break_rule_by_lottery", ids(res))

    def test_the_redraw_loop_is_gone(self):
        """2026-09-28: `table_until` kept a conflicting row after eight tries."""
        self.assertFalse(hasattr(designer.Roller, "table_until"))

    def test_a_forced_row_is_held_to_the_conflicts(self):
        with self.assertRaises(arb.EmptyPool):
            arb.check_forced("a", arb.Context(rolled={"x": False}), conflicts=CONFLICTS)
        arb.check_forced("b", arb.Context(rolled={"x": False}), conflicts=CONFLICTS)

    def test_conflicting_pairs_finds_every_pair(self):
        self.assertEqual(arb.conflicting_pairs(["x", "a", "b"], conflicts=CONFLICTS), [("a", "x")])
        self.assertEqual(arb.conflicting_pairs(["tension_inheritance_merit", "break_rule_by_lottery"]),
                         [("break_rule_by_lottery", "tension_inheritance_merit")])


class Constraints(unittest.TestCase):

    def test_requires_reads_dials_and_rolled_rows(self):
        ctx = arb.Context(dials={"magic": "medium", "content_mix": ["war", "mystery"]}, rolled={"r1": False})
        self.assertTrue(arb.holds({"dial": {"magic": ["medium", "high"]}}, ctx))
        self.assertFalse(arb.holds({"dial": {"magic": ["high"]}}, ctx))
        self.assertTrue(arb.holds({"dial": {"content_mix": ["mystery"]}}, ctx), "a list dial holds on any value")
        self.assertTrue(arb.holds({"any_of": ["r1", "r2"]}, ctx))
        self.assertFalse(arb.holds({"all_of": ["r1", "r2"]}, ctx))
        self.assertFalse(arb.holds({"none_of": ["r1"]}, ctx))
        self.assertTrue(arb.holds([{"any_of": ["r9"]}, {"dial": {"magic": ["medium"]}}], ctx), "a list is an or")
        with self.assertRaises(ValueError):
            arb.holds({"palette": ["x"]}, ctx)

    def test_requirements_forbidden_rows_and_zero_weights_are_constraints(self):
        rows = [{"id": "p", "label": "P", "requires": {"dial": {"magic": ["high"]}}},
                {"id": "q", "label": "Q", "forbidden": True, "allowed_via": ["s1"]},
                {"id": "z", "label": "Z", "weight": 0},
                {"id": "ok", "label": "OK"}]
        res = arb.arbitrate("t", rows, arb.Context(dials={"magic": "low"}), conflicts={}, secret_ids=set())
        self.assertEqual(ids(res), ["ok"])
        self.assertEqual({e["row"]: e["why"] for e in res["excluded"]},
                         {"p": "requires", "q": "forbidden", "z": "weight_zero"})
        res = arb.arbitrate("t", rows, arb.Context(dials={"magic": "high"}, rolled={"s1": True}), conflicts={},
                            secret_ids=set(), secret=True)
        self.assertEqual(ids(res), ["p", "q", "ok"], "allowed_via admits a forbidden row")

    def test_weight_by_multiplies_while_its_condition_holds(self):
        row = {"id": "w", "label": "W", "weight": 2, "weight_by": [{"when": {"dial": {"era": ["nautical"]}}, "x": 3},
                                                                   {"when": {"any_of": ["r1"]}, "x": 0.5}]}
        self.assertEqual(arb.weight_of(row, arb.Context(dials={"era": "nautical"})), 6)
        self.assertEqual(arb.weight_of(row, arb.Context(dials={"era": "nautical"}, rolled={"r1": False})), 3)
        self.assertEqual(arb.weight_of(row, arb.Context(dials={"era": "medieval"})), 2)

    def test_an_empty_constraint_pool_stops_the_draw(self):
        """Correction A: a pool conflicts or requirements empty is a table fault."""
        with self.assertRaises(arb.EmptyPool):
            arb.arbitrate("t", ROWS, arb.Context(), exclude={"a", "b", "c", "d"}, conflicts={}, secret_ids=set())
        with self.assertRaises(arb.EmptyPool):
            arb.arbitrate("t", ROWS, arb.Context(), where=lambda r: False, why="distance", conflicts={}, secret_ids=set())


class Usage(unittest.TestCase):

    def test_usage_excludes_and_logs_its_reason(self):
        res = arb.arbitrate("t", ROWS, arb.Context(), usage={"used_elsewhere": {"a"}, "family_wait": {"f2"}},
                            conflicts={}, secret_ids=set())
        self.assertEqual(ids(res), ["b", "d"])
        self.assertIn({"row": "a", "why": "used_elsewhere"}, res["excluded"])
        self.assertIn({"row": "c", "why": "family_wait", "family": "f2"}, res["excluded"])
        self.assertIsNone(res["usage_fallback"])

    def test_an_exhausted_table_falls_back_family_waits_first(self):
        """Correction A: a pool only usage empties does not stop; the family waits go first, then all usage."""
        res = arb.arbitrate("t", ROWS, arb.Context(), usage={"used_elsewhere": {"c", "d"}, "family_wait": {"f1"}},
                            conflicts={}, secret_ids=set())
        self.assertEqual(ids(res), ["a", "b"])
        self.assertEqual(res["usage_fallback"], "dropped: family_wait")
        res = arb.arbitrate("t", ROWS, arb.Context(), usage={"used_elsewhere": {"a", "b", "c", "d"}}, conflicts={},
                            secret_ids=set())
        self.assertEqual(ids(res), ["a", "b", "c", "d"])
        self.assertEqual(res["usage_fallback"], "dropped: used_elsewhere")

    def test_pairs_and_row_waits(self):
        res = arb.arbitrate("t", ROWS, arb.Context(), usage={"row_wait": {"a"}, "pair": {"b"}}, conflicts={},
                            secret_ids=set())
        self.assertEqual(ids(res), ["c", "d"])


class Secrecy(unittest.TestCase):

    def test_a_public_draw_never_names_the_secret_layer(self):
        conflicts = {"a": frozenset({"s"}), "s": frozenset({"a"}), "b": frozenset({"x"}), "x": frozenset({"b"})}
        ctx = arb.Context(rolled={"s": True, "x": False})
        res = arb.arbitrate("t", ROWS, ctx, conflicts=conflicts, secret_ids=set())
        self.assertEqual([e["row"] for e in res["excluded"]], ["b"])
        self.assertEqual(res["excluded_secret"], [{"row": "a", "why": "conflict", "with": "s"}])
        # a row of a secret table names the secret layer even before it is rolled
        rows = [{"id": "p", "label": "P", "requires": {"any_of": ["secret_row"]}}, {"id": "ok", "label": "OK"}]
        res = arb.arbitrate("t", rows, arb.Context(), conflicts={}, secret_ids={"secret_row"})
        self.assertEqual(res["excluded"], [])
        self.assertEqual(res["excluded_secret"], [{"row": "p", "why": "requires"}])
        # a secret draw keeps its own reasons
        res = arb.arbitrate("t", ROWS, ctx, conflicts=conflicts, secret_ids=set(), secret=True)
        self.assertEqual(res["excluded_secret"], [])

    def test_a_public_reason_is_named_before_a_secret_one(self):
        conflicts = {"a": frozenset({"s", "x"}), "s": frozenset({"a"}), "x": frozenset({"a"})}
        res = arb.arbitrate("t", ROWS, arb.Context(rolled={"s": True, "x": False}), conflicts=conflicts, secret_ids=set())
        self.assertIn({"row": "a", "why": "conflict", "with": "x"}, res["excluded"])


class BirthOrder(unittest.TestCase):

    def used(self):
        return {"campaigns": {"_test-old-1": {"t.yaml": ["a"]}, "_test-old-2": {"t.yaml": ["c"]},
                              "real-1": {"t.yaml": ["d"]}, "_test-new": {"t.yaml": ["b"]}},
                "births": {"real-1": {"first_approved": "2026-10-01T10:00:00Z"},
                           "_test-new": {"first_approved": "2026-10-02T10:00:00Z"}}}

    def test_archived_births_come_first_then_by_time(self):
        self.assertEqual(dd.birth_order(self.used()), ["_test-old-1", "_test-old-2", "real-1", "_test-new"])

    def test_windows_count_real_births_apart_from_test_births(self):
        u = self.used()
        self.assertEqual(dd.recent_births("_test-now", 3, u), ["_test-old-2", "real-1", "_test-new"])
        self.assertEqual(dd.recent_births("real-2", 3, u), ["real-1"], "a real birth never counts the test births")
        self.assertEqual(dd.recent_births("real-1", 3, u), [], "only the births before it")
        self.assertEqual(dd.rows_used_by(dd.recent_births("_test-now", 2, u), "t.yaml", u), {"d", "b"})


class Hardening(unittest.TestCase):

    def test_the_table_signature_sees_a_change_at_once(self):
        """Owner, 2026-09-28: the index follows the files' mtimes, not a clock; a table changed inside one process is
        never read stale."""
        import os
        import tempfile
        from pathlib import Path
        tmp = Path(tempfile.mkdtemp())
        (tmp / "t.yaml").write_text("rows: []", encoding="utf-8")
        real = dt.tables_dir
        dt.tables_dir = lambda: tmp
        try:
            first = dt._signature()
            st = (tmp / "t.yaml").stat()
            os.utime(tmp / "t.yaml", ns=(st.st_atime_ns, st.st_mtime_ns + 10 ** 9))
            self.assertNotEqual(dt._signature(), first)
        finally:
            dt.tables_dir = real

    def test_the_test_used_path_must_live_in_the_temp_dir(self):
        """Owner, 2026-09-28: the DND_CAMPAIGN_ROOT leak's class; an outside path is ignored with a warning."""
        import io
        import os
        import tempfile
        from contextlib import redirect_stderr
        from pathlib import Path
        saved = os.environ.get(dd.TEST_USED_ENV)
        try:
            inside = Path(tempfile.mkdtemp()) / "used.json"
            os.environ[dd.TEST_USED_ENV] = str(inside)
            self.assertEqual(dd.used_path(), inside.resolve())
            os.environ[dd.TEST_USED_ENV] = str(SCRIPTS.parent / "used.json")
            err = io.StringIO()
            with redirect_stderr(err):
                path = dd.used_path()
            self.assertNotEqual(path, (SCRIPTS.parent / "used.json").resolve())
            self.assertEqual(path.name, "used.json")
            self.assertIn("outside the system temp directory; ignored", err.getvalue())
        finally:
            if saved is None:
                os.environ.pop(dd.TEST_USED_ENV, None)
            else:
                os.environ[dd.TEST_USED_ENV] = saved


class SmallPools(unittest.TestCase):
    """Correction C: table_until left P3, P4, P6, P7 and P9 with the same constraints; the pools they filter must
    never be empty, or the preroll stops."""

    def test_every_climate_has_a_biome(self):
        for c in dt.rows("calendar.yaml#climate"):
            with self.subTest(climate=c["id"]):
                arb.arbitrate("regions.yaml#biome", dt.rows("regions.yaml#biome"), arb.Context(),
                              where=lambda row, c=c: c["id"] in (row.get("climates") or []), why="climate")

    def test_every_telegraph_distance_has_a_row(self):
        for d in ("far", "near", "threshold"):
            with self.subTest(distance=d):
                arb.arbitrate("sites.yaml#telegraph", dt.rows("sites.yaml#telegraph"), arb.Context(),
                              where=lambda row, d=d: row.get("distance") == d, why="distance")

    def test_every_scale_quota_pool_has_a_drawable_archetype(self):
        for scale in dt.dial_values("scale"):
            pool = {f"archetype_{a}" for a in (dt.scale_row(scale)["factions"].get("pool") or [])}
            if not pool:
                continue
            with self.subTest(scale=scale):
                res = arb.arbitrate("factions.yaml#archetype", dt.rows("factions.yaml#archetype"), arb.Context(),
                                    where=lambda row: row["id"] in pool, why="quota_pool")
                self.assertEqual(set(ids(res)), pool)

    def test_every_forbidden_bearing_table_keeps_a_drawable_row(self):
        for ref in ("antagonists.yaml#villain_shape", "antagonists.yaml#origin", "antagonists.yaml#bbeg_faction_archetype",
                    "arc.yaml#opening_scene_type", "arc.yaml#plot_engine", "factions.yaml#fracture",
                    "factions.yaml#cult_doctrine", "threads.yaml#truth_kind", "threads.yaml#mission_verb"):
            with self.subTest(table=ref):
                res = arb.arbitrate(ref, dt.rows(ref), arb.Context())
                self.assertTrue(res["pool"])
                self.assertFalse(any(r.get("forbidden") for r in res["pool"]))

    def test_an_even_spread_never_empties_a_pool(self):
        uses: dict = {}
        rows = [f"r{i}" for i in range(5)]
        rng = random.Random(1)
        for n in range(23):
            spent = designer.spread_exclude(uses, len(rows))
            free = [r for r in rows if r not in spent]
            self.assertTrue(free)
            pick = rng.choice(free)
            uses[pick] = uses.get(pick, 0) + 1
            self.assertLessEqual(max(uses.values()) - min(uses.get(r, 0) for r in rows), 1)


if __name__ == "__main__":
    unittest.main()
