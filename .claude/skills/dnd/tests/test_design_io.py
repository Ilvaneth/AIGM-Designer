"""
test_design_io.py — the shared store I/O keeps its promises.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import design_io as io  # noqa: E402


class AtomicWrite(unittest.TestCase):

    def test_writes_json_with_lf_and_trailing_newline_and_no_temp_left(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            io.write_json_atomic(path, {"b": 1, "a": "şçğ"})
            raw = path.read_bytes()
            self.assertNotIn(b"\r\n", raw)
            self.assertTrue(raw.endswith(b"}\n"))
            self.assertIn("şçğ".encode("utf-8"), raw)
            self.assertEqual(json.loads(raw), {"b": 1, "a": "şçğ"})
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["store.json"])

    def test_overwrite_replaces_the_whole_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            io.write_json_atomic(path, {"long": "x" * 1000})
            io.write_json_atomic(path, {"short": 1})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"short": 1})

    def test_stamp_meta_sets_the_shared_keys_and_keeps_the_rest(self):
        data = {"_meta": {"simulated_to_day": 4}, "x": 1}
        io.stamp_meta(data, "camp", "test.py verb", extra=True)
        meta = data["_meta"]
        self.assertEqual(meta["campaign"], "camp")
        self.assertEqual(meta["written_by"], "test.py verb")
        self.assertEqual(meta["schema_version"], 1)
        self.assertEqual(meta["simulated_to_day"], 4)
        self.assertTrue(meta["extra"])
        self.assertRegex(meta["written_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")


class Parsers(unittest.TestCase):

    def test_front_matter_lists_nulls_and_values(self):
        text = "---\nentity: npc_x\nstamped: [faction, secret_tr]\nmirror: null\ncovers: []\n---\n# body\n"
        fm = io.parse_front_matter(text)
        self.assertEqual(fm["entity"], "npc_x")
        self.assertEqual(fm["stamped"], ["faction", "secret_tr"])
        self.assertIsNone(fm["mirror"])
        self.assertEqual(fm["covers"], [])

    def test_front_matter_tolerates_crlf_and_missing_block(self):
        self.assertEqual(io.parse_front_matter("---\r\nentity: a_b\r\n---\r\nx")["entity"], "a_b")
        self.assertEqual(io.parse_front_matter("# no block"), {})

    def test_wiki_links_are_distinct_and_ordered(self):
        self.assertEqual(io.wiki_links("[[npc_a]] x [[site_b]] y [[npc_a]]"), ["npc_a", "site_b"])

    def test_slug_transliterates_turkish(self):
        self.assertEqual(io.slug("Kör Fener"), "kor_fener")
        self.assertEqual(io.slug("İlme Kandilci"), "ilme_kandilci")
        self.assertEqual(io.slug("Yaşlı Çınar'ın Gölgesi"), "yasli_cinar_in_golgesi")

    def test_id_type(self):
        self.assertEqual(io.id_type("npc_s01"), "npc")
        self.assertEqual(io.id_type("beat_1a"), "beat")
        self.assertIsNone(io.id_type("landmark_x"))


class OverlayRecords(unittest.TestCase):

    def test_set_validates_field_value_and_writer(self):
        ov = io.empty_overlay("camp")
        rec = io.overlay_set(ov, "site_x", "status", "detailed", writer="registry.py merge",
                             day=0, birth="skeleton")
        self.assertEqual(rec["birth"], "skeleton")
        rec2 = io.overlay_set(ov, "site_x", "status", "played", writer="site_progress.py", day=12)
        self.assertEqual(rec2["birth"], "skeleton", "birth is kept from the first record")
        self.assertEqual(ov["entries"]["site_x"]["status"]["value"], "played")
        with self.assertRaises(ValueError):
            io.overlay_set(ov, "site_x", "danger_tier", 3, writer="site_progress.py", day=1)
        with self.assertRaises(ValueError):
            io.overlay_set(ov, "site_x", "status", "burned", writer="site_progress.py", day=1)
        with self.assertRaises(ValueError):
            io.overlay_set(ov, "site_x", "status", "played", writer="the DM by hand", day=1)


if __name__ == "__main__":
    unittest.main()
