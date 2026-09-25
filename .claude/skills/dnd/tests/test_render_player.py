"""
test_render_player.py — the player-facing files (plan item 11.3-11.6, 16.2, risk 24.1 #10; slice 1c
item 5): the primer is assembled from the public projection, the section files, the calendar, the
map and the news, with every link resolved to a name and no hidden id, secret name or dm-only
sentence; a link to a discoverable or secret entity fails the build; facts and day-0 rumours merge
from staging into common-knowledge.json and news.json with their refs checked; a thread's public
face is extracted with links resolved.
"""

import json
import sys
import unittest

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))


class Primer(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("player")
        staging = self.c.path("design/_staging/P8")
        staging.mkdir(parents=True, exist_ok=True)
        (staging / "primer_polity_reedmarch.section.md").write_text(
            "Reedmarch'ta tuz her şeydir. [[settlement_lanternside]] limanında kandiller hiç sönmez; "
            "[[faction_court_of_mourners]] cenazelerde okur.\n", encoding="utf-8")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_primer_is_assembled_resolved_and_clean(self):
        proc = self.c.run("render_player.py", "primer", check=True)
        self.assertIn("clean", proc.stdout)
        text = self.c.path("design/player-primer.md").read_text(encoding="utf-8")
        self.assertIn("## The pitch", text)
        self.assertIn("## Reedmarch — buradan olan karakterler için", text)
        self.assertIn("Lanternside limanında kandiller hiç sönmez", text, "the section's link resolved to the name")
        self.assertIn("Court of Mourners cenazelerde okur", text)
        for heading in ("### The gods as worshipped", "### Calendar and festivals", "### History as taught",
                        "### What everyone says is dangerous", "## Questions for your backstory", "## The player map"):
            self.assertIn(heading, text)
        self.assertIn("Lamp Night", text)
        self.assertIn("Reedham'dan kimse o yola çıkmaz", text, "the over-tier site's far telegraph")
        self.assertIn("Vesper battığında ailenden biri o gemide miydi", text, "a socket question")
        self.assertNotIn("[[", text)
        self.assertNotIn("Nerun", text)
        self.assertNotIn("npc_s01", text)
        self.assertNotIn("## Secret", text)
        self.assertEqual(self.c.run("render_player.py", "check", str(self.c.path("design/player-primer.md"))).returncode, 0)

    def test_a_link_to_a_hidden_entity_fails_the_build(self):
        (self.c.path("design/_staging/P8/primer_polity_reedmarch.section.md")).write_text(
            "Kâtip [[npc_s01]] her şeyi bilir.\n", encoding="utf-8")
        proc = self.c.run("render_player.py", "primer")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("npc_s01", proc.stderr)
        self.assertFalse(self.c.path("design/player-primer.md").read_text(encoding="utf-8").count("Kâtip"),
                         "the fixture's primer is untouched when the build is refused")

    def test_resolve_and_check(self):
        f = self.c.path("design/_staging/P8/note.md")
        f.write_text("[[settlement_lanternside]] ve [[site_tide_cave]].\n", encoding="utf-8")
        proc = self.c.run("render_player.py", "resolve", str(f))
        self.assertEqual(proc.returncode, 1, "site_tide_cave is discoverable: not for the player")
        f.write_text("[[settlement_lanternside]] ve [[site_sunken_pier]].\n", encoding="utf-8")
        self.c.run("render_player.py", "resolve", str(f), check=True)
        self.assertEqual(f.read_text(encoding="utf-8").strip(), "Lanternside ve Sunken Pier.")
        f.write_text("Nerun kâtiptir.\n", encoding="utf-8")
        proc = self.c.run("render_player.py", "check", str(f))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("secret name", proc.stdout)

    def test_facts_and_news_merge_from_staging(self):
        staging = self.c.path("design/_staging/P8")
        (staging / "primer_polity_reedmarch.facts.json").write_text(json.dumps({"facts": [
            {"keywords": ["tuz", "vergi"], "text_tr": "Reedmarch vergisini tuzdan alır.", "origin": "polity_reedmarch", "refs": ["polity_reedmarch"]},
            {"keywords": ["fener"], "text_tr": "Blind Lantern kırk yıldır yanmıyor.", "origin": "all", "refs": ["site_blind_lantern"]}]}),
            encoding="utf-8")
        self.c.run("render_player.py", "facts", check=True)
        ck = self.c.json("common-knowledge.json")
        self.assertEqual([f["id"] for f in ck["facts"]], ["ck_001", "ck_002"])
        self.assertEqual(ck["_meta"]["written_by"], "render_player.py facts")
        (staging / "primer_polity_reedmarch.facts.json").write_text(json.dumps({"facts": [
            {"keywords": ["kâtip"], "text_tr": "x", "origin": "all", "refs": ["npc_s01"]}]}), encoding="utf-8")
        self.assertEqual(self.c.run("render_player.py", "facts").returncode, 1, "a fact may not reference a secret entity")
        (staging / "primer_polity_reedmarch.facts.json").unlink()
        before = self.c.json("design/news.json")["_meta"]["next_id"]
        (staging / "primer_polity_reedmarch.news.json").write_text(json.dumps({"records": [
            {"region": "region_saltmere", "settlement": "settlement_reedham", "visibility": "rumored", "kind": "rumour",
             "line_tr": "Reedham'da bir çoban düzlükte birini görmüş.", "refs": ["settlement_reedham"], "reach": ["settlement_reedham", "region_saltmere"]}]}),
            encoding="utf-8")
        proc = self.c.run("render_player.py", "news", check=True)
        self.assertIn("+1 records", proc.stdout)
        news = self.c.json("design/news.json")
        self.assertEqual(news["records"][-1]["id"], f"news_{before:04d}")
        self.assertEqual(news["records"][-1]["source"], "birth")
        self.assertEqual(news["_meta"]["next_id"], before + 1)
        text = self.c.path("design/player-primer.md")
        self.c.run("render_player.py", "primer", check=True)
        self.assertIn("Reedham'da bir çoban düzlükte birini görmüş", text.read_text(encoding="utf-8"))

    def test_thread_face_is_the_public_section_with_links_resolved(self):
        proc = self.c.run("render_player.py", "thread-face", "thread_selen", check=True)
        self.assertIn("clean", proc.stdout)
        face = self.c.path("design/player/thread_selen.md").read_text(encoding="utf-8")
        self.assertIn("oyuncunun gördüğü yüz", face)
        self.assertNotIn("[[", face)
        self.assertNotIn("## Secret", face)
        self.assertNotIn("Nerun", face)


if __name__ == "__main__":
    unittest.main()
