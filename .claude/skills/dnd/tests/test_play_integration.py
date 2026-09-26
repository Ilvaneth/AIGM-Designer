"""
test_play_integration.py — slice 1d, play integration (plan items 6.1, 13.1-13.3, 16.1-16.3, 16.6, 21.C):
travel times and encounter tables generated from map.json and the region files; world.md, npcs.md,
design/index.md, a lean state.md and the public report generated from the projection ⊕ overlay with
"changed since birth" markers.
"""

import json
import subprocess
import sys
import unittest

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))


def travel(c, *args):
    """travel.py takes --campaign, not -c."""
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "travel.py"), "--campaign", c.name, *args],
                          capture_output=True, text=True, env=c.env, encoding="utf-8")
    if proc.returncode != 0:
        raise AssertionError(f"travel.py {' '.join(args)} failed ({proc.returncode}): {proc.stdout} {proc.stderr}")
    return proc


class MapTravel(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("travel")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_travel_times_are_shortest_paths_from_the_hub(self):
        proc = self.c.run("map_travel.py", "travel-times", check=True)
        self.assertIn("travel-times.md", proc.stdout)
        text = self.c.path("design/travel-times.md").read_text(encoding="utf-8")
        self.assertIn("## Saltmere (T2) — from Lanternside", text)
        self.assertIn("| Reedham | settlement | 2 | Reed Road |", text, "via the waypoint, two days")
        self.assertIn("| Bottomless Well | site | 3.5 | Reed Road → Reedham |", text, "a place reached through a hub is never closer than the hub")
        self.assertIn("| Tide Cave | site | 1 | — |", text, "discoverable nodes are on the DM's table")
        self.assertIn("## Settlement to settlement", text)
        self.assertIn("## Routes", text)
        self.assertFalse(self.c.path("design/dm-only/travel-times.md").is_file(), "no secret node, no dm-only copy")

    def test_days_and_near_answer_the_approaching_question(self):
        proc = self.c.run("map_travel.py", "days", "settlement_lanternside", "site_bottomless_well", check=True)
        self.assertIn("3.5 day(s): Lanternside → Reed Road → Reedham → Bottomless Well", proc.stdout)
        proc = self.c.run("map_travel.py", "near", "settlement_lanternside", "--days", "1", "--kind", "site", "--json", check=True)
        ids = [r["id"] for r in json.loads(proc.stdout)]
        self.assertEqual(ids, ["site_sunken_pier", "site_tide_cave"])
        self.assertEqual(self.c.run("map_travel.py", "days", "settlement_lanternside", "site_nowhere").returncode, 1)

    def test_encounter_tables_compile_for_travel_py_and_keep_the_roll_log(self):
        proc = self.c.run("map_travel.py", "encounters", check=True)
        self.assertIn("1 region table(s)", proc.stdout)
        ref = self.c.path("reference/travel-encounters.md")
        text = ref.read_text(encoding="utf-8")
        self.assertIn("## Saltmere", text)
        self.assertIn("### Early tier", text)
        self.assertIn("#### Category", text)
        self.assertIn("#### Quiet/Texture", text)
        self.assertIn("### Late tier", text)
        self.assertIn("## Roll Log", text)
        self.assertNotIn("#####", text, "travel.py reads four-hash subtables")
        listing = travel(self.c, "--list-regions")
        self.assertIn("Saltmere", listing.stdout)
        roll = travel(self.c, "--region", "Saltmere", "--tier", "early", "--days", "1")
        self.assertTrue(roll.stdout.strip())
        text2 = ref.read_text(encoding="utf-8")
        self.assertGreater(len(text2), len(text), "a roll was logged")
        self.c.run("map_travel.py", "encounters", check=True)
        self.assertEqual(len(ref.read_text(encoding="utf-8")), len(text2), "recompiling keeps the roll log")


class RenderDm(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("renderdm")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_world_and_npcs_render_the_overlay_with_changed_markers(self):
        self.c.run("registry.py", "play-set", "settlement_lanternside", "ruler", "npc_olmar", "--day", "3", "--reason", "Sarven kaçtı", check=True)
        self.c.run("registry.py", "play-set", "npc_sarven", "alive", "fled", "--day", "3", "--reason", "gece kayıkla", check=True)
        self.c.run("render_dm.py", "all", check=True)
        world = self.c.path("world.md").read_text(encoding="utf-8")
        self.assertIn("## Campaign Tone & Genre", world)
        self.assertIn("## Factions (public face)", world)
        self.assertIn("| Sunken Pier | T1 | 6 | detailed |", world)
        self.assertIn("Olmar *(değişti: doğumda Sarven, gün 3)*", world)
        self.assertIn("## Changed since birth", world)
        self.assertIn("npc_sarven): alive alive → fled", world)
        self.assertNotIn("Nerun", world, "a secret entity never reaches the DM's glance file")
        npcs = self.c.path("npcs.md").read_text(encoding="utf-8")
        self.assertIn("| Sarven (Reeve Sarven) | npc_sarven | ruler | Reedmarch |", npcs)
        self.assertIn("fled *(değişti: doğumda alive, gün 3)*", npcs)
        self.assertIn("design/npcs/<id>.md", npcs)

    def test_index_lists_every_type_with_status_and_seen(self):
        self.c.run("registry.py", "play-set", "site_sunken_pier", "seen_in_play", "true", "--day", "1", "--reason", "girdiler", check=True)
        self.c.run("render_dm.py", "index", check=True)
        text = self.c.path("design/index.md").read_text(encoding="utf-8")
        for heading in ("## settlement (", "## npc (", "## site (", "## chapter ("):
            self.assertIn(heading, text)
        self.assertIn("| site_sunken_pier | Sunken Pier |", text)
        row = next(l for l in text.splitlines() if l.startswith("| site_sunken_pier |"))
        self.assertIn("| detailed | ✓ |", row)

    def test_lean_state_is_written_only_when_missing_or_forced(self):
        refused = self.c.run("render_dm.py", "state")
        self.assertEqual(refused.returncode, 1, "an existing state.md is what happened; never overwritten silently")
        self.c.run("render_dm.py", "state", "--force", check=True)
        text = self.c.path("state.md").read_text(encoding="utf-8")
        self.assertIn("type: designed", text)
        self.assertIn("current_chapter: chapter_1", text)
        self.assertIn("session_status: open", text)
        self.assertIn("- **Location:** Lanternside", text)
        self.assertIn("Selen", text)
        self.assertLess(len(text.splitlines()), 120, "lean")

    def test_report_carries_dials_counts_and_phases(self):
        self.c.run("render_dm.py", "report", check=True)
        text = self.c.path("design/report.md").read_text(encoding="utf-8")
        self.assertIn("## Dials", text)
        self.assertIn("scale short", text)
        self.assertIn("| site |", text)
        self.assertIn("| P6 | approved |", text)
        self.assertNotIn("Nerun", text)


if __name__ == "__main__":
    unittest.main()
