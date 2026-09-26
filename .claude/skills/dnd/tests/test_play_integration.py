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
from pathlib import Path

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


class PlayPack(unittest.TestCase):
    """The designer in play (items 13.1-13.6, 12.3, 16.3): the load pack, the scene pack, prep, detail through the
    birth machinery, the spotlight ledger, the end pack's fixed order."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("play")
        from paths import runtime_dir
        self.marker = runtime_dir() / "active-design.json"

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def pub(self):
        return self.c.json("design/entities.json")["entities"]

    def test_load_pack_lists_what_load_must_not_miss(self):
        proc = self.c.run("designer.py", "load-pack", "--json", check=True)
        p = json.loads(proc.stdout)
        self.assertEqual(p["location"], "settlement_lanternside")
        ids = [r["id"] for r in p["detail_needed"]]
        self.assertEqual(ids[0], "site_tide_cave", "a skeleton one day away is the first detail needed")
        self.assertIn("site_bottomless_well", ids, "a rumour pointed at it (news_0003)")
        self.assertNotIn("site_sunken_pier", ids, "already detailed")
        self.assertEqual(p["chapter_file"], "design/chapters/chapter_1.md")
        self.assertEqual([x["id"] for x in p["threads"]], ["thread_selen", "thread_vorin"])
        news = {n["id"] for n in p["news"]}
        self.assertIn("news_0001", news)
        self.assertNotIn("news_0003", news, "reaches Reedham only")
        self.assertEqual(p["pending_scenes"], [])
        text = self.c.run("designer.py", "load-pack", check=True).stdout
        self.assertIn("Detail gerekli:", text)
        self.assertIn("site_tide_cave", text)
        self.assertIn("thread_selen → design/threads/thread_selen.md", text)

    def test_scene_enter_bundles_the_place_and_marks_it_seen(self):
        proc = self.c.run("designer.py", "scene", "--enter", "Weary Gull", "--hours", "2", "--json", check=True)
        p = json.loads(proc.stdout)
        self.assertEqual(p["id"], "place_weary_gull")
        here = [nid for nid, n in self.pub().items() if n.get("type") == "npc" and n.get("location_at_birth") == "place_weary_gull"]
        self.assertEqual({n["id"] for n in p["npcs"] if n["here"]}, set(here))
        self.assertTrue(p["news"])
        self.assertEqual(p["hours"], 2)
        ov = self.c.json("design/overlay.json")["entries"]["place_weary_gull"]["seen_in_play"]
        self.assertIs(ov["value"], True)
        site = json.loads(self.c.run("designer.py", "scene", "--enter", "site_tide_cave", "--json", check=True).stdout)
        self.assertEqual(site["site"]["status"], "skeleton")
        self.assertIn("detail site_tide_cave", site["warning"])
        self.assertTrue(site["site"]["telegraphs"])
        text = self.c.run("designer.py", "scene", "--enter", "site_tide_cave", check=True).stdout
        self.assertIn("⚠", text)
        self.assertIn("telegraf:", text)

    def test_prep_ranks_candidates_records_them_and_warns_over_tier(self):
        proc = self.c.run("designer.py", "prep", "--day", "0", "--intent", "Blind Lantern'e gidecekler", "--json", check=True)
        p = json.loads(proc.stdout)
        ids = [c["id"] for c in p["candidates"]]
        self.assertEqual(ids[0], "site_blind_lantern", "the stated destination comes first")
        self.assertIn("hedef olarak söylendi", p["candidates"][0]["reasons"])
        self.assertIn("site_tide_cave", ids)
        well = next((c for c in p["candidates"] if c["id"] == "site_bottomless_well"), None)
        self.assertIsNotNone(well)
        self.assertIn("üst kademe", well["warning"])
        recorded = self.c.json("design/design.json")["prep"]
        self.assertEqual([c["id"] for c in recorded["candidates"]], ids)
        pack = json.loads(self.c.run("designer.py", "load-pack", "--json", check=True).stdout)
        self.assertEqual([c["id"] for c in pack["prepped"]], ids)

    def test_detail_runs_through_the_birth_machinery(self):
        proc = self.c.run("designer.py", "detail", "site_tide_cave", "--trigger", "prep", "--day", "0", "--json", check=True)
        out = json.loads(proc.stdout[proc.stdout.index("{"):])
        self.assertEqual(out["workflow"], "design-fanout")
        self.assertIsNone(out["phase_critic"])
        e = out["entities"][0]
        self.assertIn("render detail.site --id site_tide_cave", e["prompt_cmd"])
        self.assertIn("--phase detail", e["prompt_cmd"])
        self.assertIn("design/news.json", e["files"])
        marker = json.loads(self.marker.read_text(encoding="utf-8"))
        self.assertEqual(marker["mode"], "detail")
        prompt = Path(e["prompt_file"]).read_text(encoding="utf-8")
        self.assertIn("design/_staging/detail/site_tide_cave.json", prompt)
        critic = Path(e["critic_file"]).read_text(encoding="utf-8")
        self.assertIn("rubric_p6", critic.lower(), "a detailed site is judged by P6's rubric")
        self.assertIn("design/_staging/detail/site_tide_cave.critic1.json", critic)
        log = self.c.json("design/design.json")["detail_log"][-1]
        self.assertEqual((log["id"], log["status"], log["trigger"]), ("site_tide_cave", "begun", "prep"))
        # the agent's fragment: the row with its stamps unchanged, the overlay asking for detailed
        row = dict(self.pub()["site_tide_cave"])
        frag = {"schema_version": 1, "id": "site_tide_cave", "type": "site", "phase": "detail", "attempt": 1, "mode": "detail",
                "agent": "detail.site_tide_cave.a1", "prose": {"file": row["file"]}, "dm_only_prose": None, "registry": row,
                "overlay": {"status": "detailed"}, "graph": {"nodes": [], "edges": []}, "seeds": [], "counts": {"rooms": 11}, "status": "staged"}
        self.c.write_json("design/_staging/detail/site_tide_cave.json", frag)
        fin = self.c.run("designer.py", "detail", "site_tide_cave", "--finish", "--day", "0")
        self.assertIn("detail site_tide_cave finished", fin.stdout, fin.stderr)
        ov = self.c.json("design/overlay.json")["entries"]["site_tide_cave"]["status"]["value"]
        self.assertEqual(ov, "detailed")
        log = self.c.json("design/design.json")["detail_log"][-1]
        self.assertEqual(log["status"], "finished")
        self.assertFalse(self.marker.is_file(), "the guard is disarmed after the merge")
        self.assertTrue(self.c.path("design/_staging/detail/merged/site_tide_cave.json").is_file())

    def test_spotlight_ledger_flags_imbalance(self):
        proc = self.c.run("designer.py", "spotlight", "--session", "1", "--scenes", "thread_selen=4,thread_vorin=1", check=True)
        self.assertIn("spotlight dengesiz", proc.stdout)
        proc = self.c.run("designer.py", "spotlight", "--session", "2", "--scenes", "thread_selen=2,thread_vorin=3", check=True)
        self.assertNotIn("dengesiz", proc.stdout, "6 vs 4 over two sessions is within 35%")
        pack = json.loads(self.c.run("designer.py", "load-pack", "--json", check=True).stdout)
        self.assertEqual(pack["spotlight"]["totals"], {"thread_selen": 6, "thread_vorin": 4})

    def test_end_pack_runs_tick_sweep_then_prep(self):
        proc = self.c.run("designer.py", "end-pack", "--day", "3", "--session", "1", "--note", "Tolvan'ın işi sürüyor", check=True)
        out = proc.stdout
        self.assertLess(out.index("[factions tick]"), out.index("[factions sweep]"))
        self.assertLess(out.index("[factions sweep]"), out.index("designer prep"))
        self.assertIn("[design_check --fast]", out)
        self.assertEqual(self.c.json("design/design.json")["prep"]["note_tr"], "Tolvan'ın işi sürüyor")


if __name__ == "__main__":
    unittest.main()
