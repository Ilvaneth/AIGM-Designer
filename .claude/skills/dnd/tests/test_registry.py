"""
test_registry.py — registry.py against a throwaway copy of the fixture bible.

Covers: projection and snapshot regenerate byte-for-byte what the fixture
commits; merge is idempotent, refuses stamped drift without --revise, applies
it with one, refuses a fragment whose prose is missing and then writes nothing;
overlay status on merge; play-set with its refusals; add --origin play; export
--public carries no secret; no temp file survives any operation.
"""

import json
import shutil
import unittest

from _campaign import TestCampaign

ROLL_FRAGMENT = "design/_staging/P5/npc_yesra.json"


class Registry(unittest.TestCase):

    def setUp(self):
        self.c = TestCampaign("registry")
        # The fixture's fragments sit under merged/ (its birth completed); the merge
        # tests want them back in staging as if an agent had just written them.
        for phase, name in (("P5", "npc_yesra.json"), ("P6", "site_batik_iskele.json")):
            src = self.c.path(f"design/_staging/{phase}/merged/{name}")
            shutil.copy(src, self.c.path(f"design/_staging/{phase}/{name}"))
            src.unlink()

    def tearDown(self):
        self.c.remove()

    # --- projection --------------------------------------------------------

    def test_project_reproduces_the_committed_projection_and_snapshot(self):
        before_proj = self.c.json("design/entities.json")
        before_snap = self.c.json("design/dm-only/_snapshots/stamps.json")
        self.c.run("registry.py", "project", check=True)
        after_proj = self.c.json("design/entities.json")
        after_snap = self.c.json("design/dm-only/_snapshots/stamps.json")
        self.assertEqual(after_proj["entities"], before_proj["entities"])
        self.assertEqual(after_snap["stamps"], before_snap["stamps"])
        self.assertNotIn("npc_s01", after_proj["entities"])
        self.assertFalse(any("dm_only" in e for e in after_proj["entities"].values()))
        self.assertEqual(self.c.temp_files(), [])

    def test_export_public_prints_the_projection_without_secrets(self):
        proc = self.c.run("registry.py", "export", "--public", check=True)
        data = json.loads(proc.stdout)
        self.assertNotIn("npc_s01", data["entities"])
        self.assertNotIn("Nerun", proc.stdout)
        self.assertIn("npc_yesra", data["entities"])

    def test_show_hides_dm_only_unless_asked(self):
        public = json.loads(self.c.run("registry.py", "show", "npc_yesra", check=True).stdout)
        self.assertNotIn("dm_only", public)
        dm = json.loads(self.c.run("registry.py", "show", "npc_yesra", "--dm", check=True).stdout)
        self.assertIn("dm_only", dm)
        self.assertEqual(self.c.run("registry.py", "show", "npc_s01").returncode, 1)
        self.assertEqual(self.c.run("registry.py", "show", "npc_s01", "--dm").returncode, 0)

    # --- merge -------------------------------------------------------------

    def test_merge_is_idempotent_and_moves_the_fragment(self):
        before = self.c.json("design/dm-only/entities.json")["entities"]
        proc = self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("~ npc_yesra", proc.stdout)
        after = self.c.json("design/dm-only/entities.json")["entities"]
        self.assertEqual(after, before)
        self.assertFalse(self.c.path(ROLL_FRAGMENT).exists())
        self.assertTrue(self.c.path("design/_staging/P5/merged/npc_yesra.json").exists())
        self.assertEqual(self.c.temp_files(), [])
        # a second run finds nothing to do
        proc = self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("nothing to merge", proc.stdout)

    def test_merge_refuses_a_stamped_change_without_revise(self):
        frag = self.c.json(ROLL_FRAGMENT)
        frag["registry"]["stamped"]["faction"] = "faction_beylik"
        frag["registry"]["faction"] = "faction_beylik"
        self.c.write_json(ROLL_FRAGMENT, frag)
        before = self.c.path("design/dm-only/entities.json").read_bytes()
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("without --revise: faction", proc.stderr)
        self.assertEqual(self.c.path("design/dm-only/entities.json").read_bytes(), before)
        self.assertTrue(self.c.path(ROLL_FRAGMENT).exists(), "fragment stays in staging")

    def test_merge_refuses_a_secret_stamp_change_too(self):
        frag = self.c.json(ROLL_FRAGMENT)
        frag["registry"]["dm_only"]["secret_tr"] = "Başka bir sır."
        self.c.write_json(ROLL_FRAGMENT, frag)
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("secret_tr", proc.stderr)

    def test_merge_applies_a_stamped_change_with_revise_and_records_it(self):
        frag = self.c.json(ROLL_FRAGMENT)
        frag["registry"]["stamped"]["faction"] = "faction_beylik"
        frag["registry"]["faction"] = "faction_beylik"
        self.c.write_json(ROLL_FRAGMENT, frag)
        proc = self.c.run("registry.py", "merge", "--phase", "P5", "--revise", "rev_0001", check=True)
        self.assertIn("stamps revised: faction", proc.stdout)
        snap = self.c.json("design/dm-only/_snapshots/stamps.json")
        self.assertEqual(snap["stamps"]["npc_yesra"]["faction"], "faction_beylik")
        rev = snap["_meta"]["revisions"][-1]
        self.assertEqual((rev["id"], rev["log_id"], rev["fields"]), ("npc_yesra", "rev_0001", ["faction"]))
        self.assertEqual(rev["before"]["faction"], "faction_divan")
        self.assertEqual(self.c.run("registry.py", "check-stamps", check=True).returncode, 0)

    def test_merge_accepts_a_non_stamped_change(self):
        frag = self.c.json(ROLL_FRAGMENT)
        frag["registry"]["summary"] = "Yeni bir özet."
        self.c.write_json(ROLL_FRAGMENT, frag)
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertEqual(self.c.json("design/dm-only/entities.json")["entities"]["npc_yesra"]["summary"],
                         "Yeni bir özet.")
        self.assertEqual(self.c.json("design/entities.json")["entities"]["npc_yesra"]["summary"],
                         "Yeni bir özet.")

    def test_merge_refuses_when_the_prose_file_is_missing_and_writes_nothing(self):
        good = self.c.json(ROLL_FRAGMENT)
        good["registry"]["summary"] = "Değişti."
        self.c.write_json(ROLL_FRAGMENT, good)
        bad = json.loads(json.dumps(good))
        bad["id"] = bad["registry"]["id"] = "npc_hayalet"
        bad["registry"]["name"] = "Hayalet"
        bad["prose"]["file"] = "design/npcs/npc_hayalet.md"
        bad["dm_only_prose"] = None
        self.c.write_json("design/_staging/P5/npc_hayalet.json", bad)
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("prose file missing", proc.stderr)
        ents = self.c.json("design/dm-only/entities.json")["entities"]
        self.assertNotIn("npc_hayalet", ents)
        self.assertNotEqual(ents["npc_yesra"]["summary"], "Değişti.", "the good fragment was not applied either")

    def test_merge_rejects_a_secret_in_the_public_stamps(self):
        frag = self.c.json(ROLL_FRAGMENT)
        frag["registry"]["stamped"]["secret_tr"] = frag["registry"]["dm_only"]["secret_tr"]
        self.c.write_json(ROLL_FRAGMENT, frag)
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("sits in the public stamps", proc.stderr)

    def test_merge_writes_overlay_status_for_a_new_site(self):
        frag = self.c.json("design/_staging/P6/site_batik_iskele.json")
        frag["id"] = frag["registry"]["id"] = "site_yeni"
        frag["registry"]["name"] = "Yeni Yer"
        frag["registry"]["file"] = "design/sites/site_yeni.md"
        frag["prose"] = {"file": "design/sites/site_yeni.md", "bytes": None, "sha256": None}
        frag["dm_only_prose"] = None
        frag["overlay"] = {"status": "detailed"}
        self.c.path("design/sites/site_yeni.md").write_text("---\nentity: site_yeni\n---\n", encoding="utf-8")
        self.c.write_json("design/_staging/P6/site_yeni.json", frag)
        # the fixture's own fragment stays byte-identical, so it merges as a no-op
        self.c.run("registry.py", "merge", "--phase", "P6", "--day", "3", check=True)
        ov = self.c.json("design/overlay.json")["entries"]["site_yeni"]["status"]
        self.assertEqual((ov["value"], ov["birth"], ov["writer"], ov["day"]),
                         ("detailed", "skeleton", "registry.py merge", 3))
        self.assertEqual(self.c.json("design/overlay.json")["entries"]["site_batik_iskele"]["status"]["value"],
                         "detailed", "existing entries untouched")

    # --- play-set ----------------------------------------------------------

    def test_play_set_writes_an_overlay_record_with_birth_and_marker(self):
        proc = self.c.run("registry.py", "play-set", "settlement_fenerli", "ruler", "npc_olmar",
                          "--day", "40", "--reason", "Sarven öldü", "--news", "news_0009", check=True)
        self.assertIn("changed since birth", proc.stdout)
        rec = self.c.json("design/overlay.json")["entries"]["settlement_fenerli"]["ruler"]
        self.assertEqual(rec, {"value": "npc_olmar", "birth": "npc_sarven", "writer": "registry.py play-set",
                               "day": 40, "news": "news_0009", "reason": "Sarven öldü"})

    def test_play_set_refuses_stamped_fields_bad_values_and_unknown_ids(self):
        r = self.c.run("registry.py", "play-set", "site_kor_fener", "danger_tier", "5", "--day", "1", "--reason", "x")
        self.assertEqual(r.returncode, 1)
        self.assertIn("stamped", r.stderr)
        r = self.c.run("registry.py", "play-set", "npc_yesra", "alive", "ghost", "--day", "1", "--reason", "x")
        self.assertEqual(r.returncode, 1)
        r = self.c.run("registry.py", "play-set", "npc_yesra", "location", "place_nowhere", "--day", "1", "--reason", "x")
        self.assertEqual(r.returncode, 1)
        r = self.c.run("registry.py", "play-set", "npc_nobody", "alive", "dead", "--day", "1", "--reason", "x")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.c.json("design/overlay.json")["entries"].get("npc_yesra"), None)

    def test_play_set_seen_in_play_is_a_bool(self):
        self.c.run("registry.py", "play-set", "npc_tolvan", "seen_in_play", "true", "--day", "1",
                   "--reason", "session 1", check=True)
        self.assertIs(self.c.json("design/overlay.json")["entries"]["npc_tolvan"]["seen_in_play"]["value"], True)

    # --- add ---------------------------------------------------------------

    def test_add_registers_a_play_entity_with_a_transliterated_slug(self):
        proc = self.c.run("registry.py", "add", "--type", "place", "--name", "Kör Kandil",
                          "--summary", "Rıhtımda bir meyhane.", check=True)
        self.assertIn("+ place_kor_kandil", proc.stdout)
        row = self.c.json("design/dm-only/entities.json")["entities"]["place_kor_kandil"]
        self.assertEqual((row["origin"], row["created_phase"], row["secrecy"]), ("play", "play", "public"))
        self.assertIn("place_kor_kandil", self.c.json("design/entities.json")["entities"])
        self.assertEqual(self.c.json("design/dm-only/_snapshots/stamps.json")["stamps"]["place_kor_kandil"], {})
        # a second add with the same name is refused
        self.assertEqual(self.c.run("registry.py", "add", "--type", "place", "--name", "kör kandil",
                                    "--summary", "x").returncode, 1)

    def test_add_site_from_play_is_marked_played_improvised(self):
        self.c.run("registry.py", "add", "--type", "site", "--name", "Çürük Kayık",
                   "--summary", "Kıyıda küçük bir batık.", check=True)
        rec = self.c.json("design/overlay.json")["entries"]["site_curuk_kayik"]["status"]
        self.assertEqual(rec["value"], "played-improvised")

    # --- check-stamps ------------------------------------------------------

    def test_check_stamps_detects_drift_in_the_canonical_file(self):
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["site_kor_fener"]["stamped"]["danger_tier"] = 4
        self.c.write_json("design/dm-only/entities.json", canon)
        proc = self.c.run("registry.py", "check-stamps")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("site_kor_fener", proc.stdout)
        self.assertIn("danger_tier", proc.stdout)


if __name__ == "__main__":
    unittest.main()
