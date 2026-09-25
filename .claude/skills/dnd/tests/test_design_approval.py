"""
test_design_approval.py — the phase card and the critique record (plan item 19.6, 24.6 #6, slice 1c
item 3): a card is built from the public projection and the manifest, carries counts against the
scale band, the wishes' ticks, the validator summary and the public names, never a secret entity's
name nor a dm-only sentence; the premise card carries the spoiler-safe abstract; a rerun's card
diffs against the previous one; a critic's return is stored as ids, verdicts and codes only, and a
return carrying free text is refused; the leak scan refuses a leaking file.
"""

import json
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402


class Cards(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("approval")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def card(self, phase):
        self.c.run("design_approval.py", "card", "--phase", phase, check=True)
        return self.c.path(f"design/_approval/{phase}.card.md").read_text(encoding="utf-8")

    def test_site_card_shows_public_entities_and_nothing_secret(self):
        text = self.card("P6")
        self.assertIn("Faz kartı — P6", text)
        self.assertIn("Sunken Pier", text)
        self.assertIn("site: 4 açık, bant 6-8", text)
        self.assertIn("Ölçek bandı", text)
        self.assertIn("Doğrulayıcı", text)
        self.assertIn("Dilekler:", text)
        self.assertIn("deniz ve tuz kokusu ?", text, "no wishes critique recorded yet → ?")
        self.assertIn("<!-- ids:", text)
        self.assertNotIn("Nerun", text)
        self.assertNotIn("## Secret", text)
        self.assertNotIn("npc_s01", text, "a hidden entity appears in no form")
        self.assertIn("`onay`", text)

    def test_premise_card_carries_the_spoiler_safe_abstract(self):
        text = self.card("P1")
        self.assertIn("Sır katmanı", text)
        self.assertIn("arketip sınıfı *magic*", text)
        self.assertIn("perde 1: 3", text)
        self.assertNotIn("borrowed", text, "the archetype id itself never shows")
        self.assertNotIn("Nerun", text)

    def test_lands_card_lists_the_public_map(self):
        text = self.card("P3")
        self.assertIn("Oyuncu haritası", text)
        self.assertIn("settlement_lanternside", text)
        self.assertIn("region: 1 açık, bant 1-2", text)

    def test_wish_ticks_come_from_the_wishes_critic(self):
        ret = {"entity_id": "P6", "verdict": "pass", "findings": [
            {"rubric_id": "rubric_wishes", "entity_id": "wish:must:1", "verdict": "pass"},
            {"rubric_id": "rubric_wishes", "entity_id": "wish:must:2", "verdict": "pass"},
            {"rubric_id": "rubric_wishes", "entity_id": "wish:must_not:1", "verdict": "fix", "reason_code": "prophecy_shape"},
            {"rubric_id": "rubric_wishes", "entity_id": "wish:must_not:2", "verdict": "pass"}]}
        f = self.c.path("design/_staging/P6/critic.json")
        f.write_text(json.dumps(ret), encoding="utf-8")
        proc = self.c.run("design_approval.py", "critique", "--phase", "P6", "--file", str(f), check=True)
        self.assertIn("4 findings recorded", proc.stdout)
        text = self.card("P6")
        self.assertIn("olsun: deniz ve tuz kokusu ✓", text)
        self.assertIn("olmasın: kader/kehanet ✗", text)
        m = self.c.json("design/design.json")
        rec = m["phases"]["P6"]["critique"]["records"][-1]
        self.assertEqual(rec["verdict"], "pass")
        self.assertEqual(set(rec["findings"][2]), {"rubric_id", "entity_id", "verdict", "reason_code"})
        self.assertEqual(m["phases"]["P6"]["critique"]["verdicts"][-1], "pass")

    def test_entity_critique_counts_loops_and_refuses_free_text(self):
        good = {"entity_id": "site_sunken_pier", "verdict": "fix", "findings": [
            {"rubric_id": "rubric_p6_danger_legible", "entity_id": "site_sunken_pier", "verdict": "fix", "reason_code": "escape_needs_luck"}]}
        f = self.c.path("design/_staging/P6/site_sunken_pier.critic.json")
        f.write_text(json.dumps(good), encoding="utf-8")
        self.c.run("design_approval.py", "critique", "--phase", "P6", "--file", str(f), "--critic", "2", check=True)
        m = self.c.json("design/design.json")
        self.assertEqual(m["entities"]["site_sunken_pier"]["critique_loops"], 2, "the fixture had one loop already")
        self.assertEqual(m["phases"]["P6"]["critique"]["entity_loops_total"], 3)
        bad = {"entity_id": "site_sunken_pier", "verdict": "fix", "findings": [
            {"rubric_id": "rubric_p6_danger_legible", "entity_id": "site_sunken_pier", "verdict": "fix",
             "reason_code": "the escape line reads: Cezirde 4. odadan kumsala"}]}
        f.write_text(json.dumps(bad), encoding="utf-8")
        proc = self.c.run("design_approval.py", "critique", "--phase", "P6", "--file", str(f))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("free text", proc.stderr)

    def test_rerun_card_diffs_against_the_previous_one(self):
        first = self.card("P6")
        self.assertNotIn("Önceki karta göre", first)
        m = self.c.json("design/design.json")
        m["phases"]["P6"]["attempt"] = 3
        self.c.path("design/design.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        proj = self.c.json("design/entities.json")
        proj["entities"]["site_tide_cave"]["name"] = "Tide Hollow"
        del proj["entities"]["site_bottomless_well"]
        self.c.path("design/entities.json").write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")
        second = self.card("P6")
        self.assertIn("Önceki karta göre değişiklik (deneme 2 → 3)", second)
        self.assertIn("çıkarıldı: site_bottomless_well", second)
        self.assertIn("adı değişti: site_tide_cave", second)
        self.assertTrue(self.c.path("design/_approval/P6.attempt-2.card.md").is_file(), "the previous card is archived")

    def test_leak_scan_refuses_a_secret_name_and_a_dm_only_sentence(self):
        names, sentences = da.secret_terms(self.c.name)
        self.assertIn("Nerun", names)
        self.assertGreater(len(sentences), 10)
        leaky = self.c.path("design/_approval/leaky.md")
        leaky.parent.mkdir(parents=True, exist_ok=True)
        leaky.write_text("Kartta bir isim: Nerun kâtiptir.\n", encoding="utf-8")
        proc = self.c.run("design_approval.py", "leak-check", str(leaky))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("LEAK", proc.stdout)
        leaky.write_text("Sunken Pier kırık bir iskeledir.\n" + sentences[0] + "\n", encoding="utf-8")
        proc = self.c.run("design_approval.py", "leak-check", str(leaky))
        self.assertEqual(proc.returncode, 1)
        clean = self.c.path("design/_approval/clean.md")
        clean.write_text("Sunken Pier kırık bir iskeledir.\n", encoding="utf-8")
        self.assertEqual(self.c.run("design_approval.py", "leak-check", str(clean)).returncode, 0)

    def test_designer_card_and_approve_use_the_real_card(self):
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)
        proc = self.c.run("designer.py", "phase", "P6", "card", check=True)
        self.assertIn("leak scan clean", proc.stdout)
        text = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("Faz kartı — P6", text)
        self.c.run("designer.py", "phase", "P6", "approve", "--onay", check=True)
        m = self.c.json("design/design.json")
        self.assertEqual(m["phases"]["P6"]["status"], "approved")
        import hashlib
        digest = hashlib.sha256(self.c.path("design/_approval/P6.card.md").read_bytes()).hexdigest()
        self.assertEqual(m["phases"]["P6"]["approval"]["card_sha256"], digest, "what was approved is the card on disk")


if __name__ == "__main__":
    unittest.main()
