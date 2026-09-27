"""
test_regression_births.py — the regression pack of root-cause analysis 1 (plan 24.3; docs/reports/root-cause-analysis-1.md
§5.3): the approve gate replayed over the archived test births, model-free. Each birth is copied (the originals are never
written), RC-02's marking is replayed from the merged fragments' agent labels, the approved phases are unfrozen for
reconcile, and the gate is read phase by phase.

It asserts both sides: the faults the births carried close the gate at the phase that owned them, and the phases that
were sound stay open (a gate that stops every phase would be ignored). The births are git-ignored; on a checkout
without them the pack skips. `_test-tune-1` is left out: it predates the per-unit merge (4e3486c) and its manifest
shapes are not the pipeline's any more.
"""

import shutil
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_manifest as dm  # noqa: E402
import designer  # noqa: E402
from design_io import design_dir, read_json, sha256_file  # noqa: E402


def replayed_gate(birth: str) -> dict:
    """{phase: {code: ids}} for every phase the birth reached, on a throwaway copy."""
    src = CAMPAIGNS / birth
    name = f"_test-regress-{birth[6:]}-{uuid.uuid4().hex[:6]}"
    shutil.copytree(src, CAMPAIGNS / name)
    try:
        data = dm.load(name)
        for pn in dm.SKELETON_PHASES:
            ph = data["phases"].get(pn) or {}
            merged = design_dir(name) / "_staging" / pn / "merged"
            sk = read_json(merged / "skeleton.json") or {}
            for eid in ph.get("roster") or []:
                own = merged / f"{eid}.json"
                if own.is_file() and designer.written_by_skeleton(read_json(own) or {}, sk, eid):
                    data["entities"].setdefault(eid, {"phase": pn})["writer_owed"] = {"phase": pn, "sha256": sha256_file(own)}
        for ph in data["phases"].values():
            if ph.get("status") == "approved":
                ph["status"] = "awaiting_approval"      # reconcile leaves an approved phase frozen
        dm.save(name, data, "test_regression_births")
        dm.reconcile(name, quiet=True)
        out = {}
        for pn in dm.PHASES[1:]:
            if (data["phases"].get(pn) or {}).get("status") in (None, "pending", "prerolled"):
                continue
            out[pn] = {i["code"]: i["ids"] for i in da.gate(name, pn)}
        return out
    finally:
        shutil.rmtree(CAMPAIGNS / name, ignore_errors=True)


class Births(unittest.TestCase):

    def births(self, name):
        if not (CAMPAIGNS / name / "design" / "design.json").is_file():
            self.skipTest(f"{name} is not on disk (the archived births are git-ignored)")
        return replayed_gate(name)

    def test_dry_2_stops_where_its_faults_were_made(self):
        g = self.births("_test-dry-2")
        for pn in ("P1", "P2", "P3"):
            self.assertEqual(g[pn], {}, f"{pn} was sound; the gate stays open")
        self.assertIn("orphan_stub", g["P4"], "a faction stub P4 owned and never wrote")
        self.assertIn("band", g["P5"], "21 NPCs against 14-18")
        self.assertIn("orphan_stub", g["P5"], "seven P3 npc stubs P5 owned and never rostered")
        self.assertTrue({"site_candlewake_wreck", "site_stillgate"} <= set(g["P6"].get("incomplete", [])),
                        "the two roster sites the skeleton filled wait for writers that never ran")
        self.assertIn("critic_missing", g["P6"], "no phase or wishes critic ran on P6")

    def test_dry_1_stops_on_its_bands_and_passes_its_sound_phases(self):
        g = self.births("_test-dry-1")
        for pn in ("P1", "P2", "P3", "P4"):
            self.assertEqual(g[pn], {}, f"{pn} was sound; clue placement is P6's, the map is P3's")
        self.assertIn("band", g["P5"], "20 NPCs against 14-18")
        self.assertIn("band", g["P7"], "11 seeds against 6-8: the P3 seed stubs were never netted")
        self.assertIn("orphan_stub", g["P6"], "a secret npc stub carrying a clue, never written")

    def test_tune_2_passes_its_resumed_phases(self):
        g = self.births("_test-tune-2")
        for pn in ("P5", "P6", "P7", "P8"):
            self.assertEqual(g[pn], {}, f"{pn}: no false stop on the resumed birth")
        for pn in ("P1", "P2", "P3", "P4"):
            # before 6ed2f98 the wishes critic's return was recorded as a phase verdict: the only item left is that shape
            self.assertEqual(set(g[pn]), {"critic_missing"}, pn)


if __name__ == "__main__":
    unittest.main()
