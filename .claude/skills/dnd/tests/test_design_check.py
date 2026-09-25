"""
test_design_check.py — the validator passes the fixture and each broken
fixture trips exactly the module it should (plan item 22.1).
"""

import json
import re
import unittest

from _campaign import TestCampaign


def codes(proc) -> list:
    return [(f["module"], f["severity"], f["code"]) for f in json.loads(proc.stdout)]


def errors_by_module(proc) -> dict:
    out: dict = {}
    for m, sev, code in codes(proc):
        if sev == "error":
            out.setdefault(m, []).append(code)
    return out


class DesignCheck(unittest.TestCase):

    def setUp(self):
        self.c = TestCampaign("check")

    def tearDown(self):
        self.c.remove()

    def check(self, *args):
        return self.c.run("design_check.py", "--json", *args)

    def test_fixture_passes_every_core_module(self):
        proc = self.check()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(errors_by_module(proc), {})

    def test_human_output_is_grouped_and_names_no_secret(self):
        proc = self.c.run("design_check.py", check=True)
        self.assertIn("[refs] 0 errors", proc.stdout)
        self.assertIn("design_check: 0 errors", proc.stdout)
        self.assertNotIn("Nerun", proc.stdout)

    # --- one broken fixture per module ------------------------------------

    def test_dangling_wiki_link_trips_refs_only(self):
        p = self.c.path("design/npcs/npc_tolvan.md")
        p.write_text(p.read_text(encoding="utf-8") + "\n[[npc_hayalet]]\n", encoding="utf-8")
        proc = self.check()
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(list(errors_by_module(proc)), ["refs"])
        self.assertIn("dangling_link", errors_by_module(proc)["refs"])

    def test_secret_heading_in_a_public_file_trips_secrecy_only(self):
        p = self.c.path("design/npcs/npc_tolvan.md")
        p.write_text(p.read_text(encoding="utf-8") + "\n## Secret\n- x\n", encoding="utf-8")
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["secrecy"])
        self.assertIn("secret_heading_public", errors_by_module(proc)["secrecy"])

    def test_secret_name_in_a_public_file_trips_secrecy_only(self):
        p = self.c.path("world.md")
        p.write_text(p.read_text(encoding="utf-8") + "\nNerun burada.\n", encoding="utf-8")
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["secrecy"])
        self.assertIn("secret_name_leak", errors_by_module(proc)["secrecy"])
        self.assertNotIn("Nerun", proc.stdout, "the finding does not repeat the name")

    def test_stamp_change_trips_stamps_only(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["site_blind_lantern"]["stamped"]["danger_tier"] = 3
        canon["entities"]["site_blind_lantern"]["danger_tier"] = 3
        self.c.write_json("design/dm-only/entities.json", canon)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["stamps"])
        self.assertIn("stamp_drift", errors_by_module(proc)["stamps"])

    def test_missing_telegraph_trips_sites_only(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["site_tide_cave"]["telegraphs"].pop()
        self.c.write_json("design/dm-only/entities.json", canon)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["sites"])
        self.assertIn("telegraphs", errors_by_module(proc)["sites"])

    def test_wrong_minimum_depth_trips_sites_only(self):
        p = self.c.path("design/sites/site_sunken_pier.md")
        text = p.read_text(encoding="utf-8")
        # room 4 no longer drops into 5: the shortest path grows to 5 rooms
        text = text.replace("| 1 (cezirde), 5 (tek yön, çukur) |", "| 1 (cezirde) |")
        p.write_text(text, encoding="utf-8")
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["sites"])
        self.assertIn("min_depth", errors_by_module(proc)["sites"])

    def test_later_act_reference_trips_sites_only(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["item_lamp_seal"]["act"] = 2
        canon["entities"]["item_lamp_seal"]["stamped"]["act"] = 2
        self.c.write_json("design/dm-only/entities.json", canon)
        snap = self.c.json("design/dm-only/_snapshots/stamps.json")
        snap["stamps"]["item_lamp_seal"]["act"] = 2
        self.c.write_json("design/dm-only/_snapshots/stamps.json", snap)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["sites"])
        self.assertIn("later_act_ref", errors_by_module(proc)["sites"])

    def test_illegal_overlay_field_trips_overlay_only(self):
        ov = self.c.json("design/overlay.json")
        ov["entries"]["site_blind_lantern"]["danger_tier"] = {"value": 5, "birth": 2, "writer": "registry.py play-set", "day": 1}
        self.c.write_json("design/overlay.json", ov)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["overlay"])
        self.assertIn("overlay_field", errors_by_module(proc)["overlay"])

    def test_unsanctioned_overlay_writer_trips_overlay_only(self):
        ov = self.c.json("design/overlay.json")
        ov["entries"]["site_blind_lantern"]["status"]["writer"] = "the DM by hand"
        self.c.write_json("design/overlay.json", ov)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["overlay"])

    def test_missing_map_node_trips_map_only(self):
        m = self.c.json("design/map.json")
        m["nodes"] = [n for n in m["nodes"] if n["id"] != "site_bottomless_well"]
        m["edges"] = [e for e in m["edges"] if "site_bottomless_well" not in (e["from"], e["to"])]
        self.c.write_json("design/map.json", m)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["map"])
        self.assertIn("node_missing", errors_by_module(proc)["map"])

    def test_disconnected_map_trips_map_only(self):
        m = self.c.json("design/map.json")
        m["edges"] = [e for e in m["edges"] if e["id"] != "r_reedham_well"]
        self.c.write_json("design/map.json", m)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["map"])
        self.assertIn("node_unreachable", errors_by_module(proc)["map"])

    def test_dead_faction_leader_trips_refs_only(self):
        ov = self.c.json("design/overlay.json")
        ov["entries"]["npc_draskun"] = {"alive": {"value": "dead", "birth": "alive", "writer": "factions.py simulate", "day": 30, "news": None, "reason": None}}
        self.c.write_json("design/overlay.json", ov)
        proc = self.check()
        self.assertEqual(list(errors_by_module(proc)), ["refs"])
        self.assertIn("role_dead", errors_by_module(proc)["refs"])

    # --- modes ---------------------------------------------------------------

    def test_fast_run_reports_but_exits_zero(self):
        p = self.c.path("design/npcs/npc_tolvan.md")
        p.write_text(p.read_text(encoding="utf-8") + "\n[[npc_hayalet]]\n", encoding="utf-8")
        proc = self.c.run("design_check.py", "--fast")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("does not resolve", proc.stdout)
        self.assertIn("not blocking", proc.stdout)

    def test_only_limits_the_run_to_one_entity(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["site_tide_cave"]["telegraphs"].pop()
        self.c.write_json("design/dm-only/entities.json", canon)
        proc = self.check("--only", "site_sunken_pier")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        proc = self.check("--only", "site_tide_cave")
        self.assertEqual(proc.returncode, 1)

    def test_phase_run_accepts_a_pending_stub(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["npc_stub"] = {
            "id": "npc_stub", "type": "npc", "name": "Stub", "aliases": [], "summary": "reserved by P3",
            "file": None, "secrecy": "public", "created_phase": "P3", "origin": "birth", "status": "pending",
            "stamped": {}, "refs": [],
        }
        self.c.write_json("design/dm-only/entities.json", canon)
        proc = self.check("--phase", "P3", "--modules", "refs,stamps")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        proc = self.check("--modules", "refs")
        self.assertEqual(proc.returncode, 0, "a pending row is accepted in every run; only P8's full run demands files")

    def test_unknown_module_is_usage_error(self):
        self.assertEqual(self.c.run("design_check.py", "--modules", "vibes").returncode, 2)


if __name__ == "__main__":
    unittest.main()
