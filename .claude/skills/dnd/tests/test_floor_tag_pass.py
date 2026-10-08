"""
test_floor_tag_pass.py — the tag pass is enforced for every floor (errata 24.2 #33; docs/p2-build-22.md part 22c #4).

A phase stands in `design_promises.SOURCE_PHASES` only when its tag pass is done: every row of every table it rolls
carries its reviewed stamp (the row as it stands now), and the shared corpus holds no birth with a declared clash among
that phase's rolls. The tables a phase rolls are read from the corpus itself (P0: the dials and the scale; P1: the
corpus's P1 prerolls; P2: their cosmos, rolled in memory), so a phase the corpus does not roll (P3-P8 today) cannot be
bound: it needs its own tag pass and its own corpus roll first.
"""

import sys
import unittest

from _campaign import SCRIPTS
import _corpus
import test_cosmos_roll as cosmos

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402


def rolled_per_phase() -> dict:
    """phase -> (the table refs its records name, [(rolled row ids, tokens, exempt pairs)] per corpus birth)."""
    out = {"P0": (set(), []), "P1": (set(), []), "P2": (set(), [])}
    for name in ("scale", "tone", "magic", "era", "danger", "content_mix"):
        out["P0"][0].add(f"dials.yaml#{name}")
    out["P0"][0].add("scale.yaml")
    for d, R1, R, _, _ in cosmos.rolled():
        p0 = arb.Context(dials=dict(d))
        out["P0"][1].append((set(), set(p0.tokens), set()))
        for phase, roller, ctx in (("P1", R1, R1.ctx), ("P2", R, R.ctx)):
            out[phase][0].update(r["table"] for r in roller.public + roller.secret if ".yaml" in str(r.get("table")) and r.get("row_id"))
            out[phase][1].append((set(ctx.rolled), set(ctx.tokens), set(R1.exempt) | set(roller.exempt)))
    return out


def stamp_faults(refs, stamps: dict) -> list[str]:
    """Every row of every table in `refs` without a stamp that matches it as it stands."""
    out = []
    naming = dt.naming_stamps()
    for ref in sorted(refs):
        if ref.startswith("naming.yaml") and ref != "naming.yaml#family":
            out += [f"{ref}: {k} unstamped" for k, h in naming.items() if stamps.get(k) != h]
            continue
        secret = bool(dt.roll_header(ref).get("secret"))
        for r in dt.rows(ref):
            if stamps.get(dt.stamp_key(r["id"], secret)) != dt.row_hash(r):
                out.append(f"{ref}: a row unstamped or changed since its stamp" + ("" if secret else f" ({r['id']})"))
    return list(dict.fromkeys(out))


def clash_count(births: list) -> int:
    """Births holding a declared clash (a row pair or a claims pair) among their rolls."""
    return sum(1 for rows, tokens, exempt in births if arb.conflicting_pairs(list(rows), tokens=list(tokens), exempt=exempt))


class Floors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.per_phase = rolled_per_phase()

    def test_every_bound_floor_has_its_tag_pass(self):
        stamps = dt.read_stamps()
        for phase in dp.SOURCE_PHASES:
            with self.subTest(phase):
                self.assertIn(phase, self.per_phase, f"{phase} is bound to the ledger, and the corpus rolls none of it: its tag "
                                                     "pass and its corpus roll come first (errata 24.2 #33)")
                refs, births = self.per_phase[phase]
                self.assertTrue(refs, phase)
                self.assertEqual(stamp_faults(refs, stamps), [], f"{phase}'s tables are not all stamped")
                self.assertEqual(clash_count(births), 0, f"{phase}: corpus births hold a declared clash")

    def test_p2_is_bound_and_its_tables_are_the_cosmos(self):
        self.assertIn("P2", dp.SOURCE_PHASES)
        refs, _ = self.per_phase["P2"]
        files = {r.split("#")[0] for r in refs}
        self.assertLessEqual({"pantheon.yaml", "planes.yaml", "magic.yaml", "history.yaml", "calendar.yaml"}, files)

    def test_a_removed_stamp_turns_it_red(self):
        stamps = dict(dt.read_stamps())
        refs, _ = self.per_phase["P2"]
        victim = dt.rows("pantheon.yaml#afterlife")[0]["id"]
        del stamps[victim]
        self.assertIn(f"pantheon.yaml#afterlife: a row unstamped or changed since its stamp ({victim})", stamp_faults(refs, stamps))
        changed = dict(dt.read_stamps())
        changed[victim] = "0" * 16
        self.assertTrue(stamp_faults(refs, changed), "a stamp that no longer matches its row is red too")

    def test_a_clash_in_the_corpus_turns_it_red(self):
        # one birth holding a declared pair (the dead gods and a god behind the villain, D19)
        self.assertEqual(clash_count([({"pantheon_dead_gods", "power_god"}, set(), set())]), 1)


if __name__ == "__main__":
    unittest.main()
