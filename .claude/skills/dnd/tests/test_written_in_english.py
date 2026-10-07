"""
test_written_in_english.py — build item 13a (docs/p1-build-13.md; errata 24.2 #28): a campaign is written in English
and played in Turkish. The P0 and P1 tables hold no `tr` field and no Turkish letter; a new birth's preroll, cards and
public log hold none; the door refuses a Turkish letter in a new birth's fragment and leaves a legacy birth as it is.
"""

import json
import os
import re
import shutil
import sys
import unittest
import uuid

from _campaign import TestCampaign, MarkerGuard, SCRIPTS, CAMPAIGNS, USED
import test_designer as td

sys.path.insert(0, str(SCRIPTS))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
import registry  # noqa: E402

from test_tuning_birth_1 import FRONT, fragment, row  # noqa: E402

TURKISH = re.compile("[çğıöşüÇĞİÖŞÜ]")
# the tables of P0 and P1 (docs/p1-build-13.md §3); of antagonists.yaml the villain's sub-tables P1 rolls
WHOLE = ("dials.yaml", "scale.yaml", "foundation.yaml", "trope-breaks.yaml", "signatures.yaml", "tensions.yaml", "secrets.yaml")
SUBS = ("antagonists.yaml#visibility", "antagonists.yaml#villain_shape", "antagonists.yaml#origin", "antagonists.yaml#break_tie",
        "naming.yaml#family")
SKILL = SCRIPTS.parent
PLAY_FLAGS = ("tr_suffix_friendly",)     # naming.yaml#family: a flag for the table's narration, no Turkish text (item 11 reworks the table)


def row_lists():
    for name in WHOLE:
        for sub, rows in dt.all_row_lists(dt.load(name)).items():
            yield (f"{name}#{sub}" if sub else name), rows
    for ref in SUBS:
        yield ref, dt.rows(ref)


def walk(node, path=""):
    """(path, key or None, string or None) over a row: every key and every string."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield f"{path}.{k}", k, None
            yield from walk(v, f"{path}.{k}")
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, path)
    elif isinstance(node, str):
        yield path, None, node


class Tables(unittest.TestCase):

    def test_no_tr_key_and_no_turkish_letter_in_the_p0_and_p1_tables(self):
        """A failure names the table and the field's path, never a secret row."""
        keys = letters = rows_seen = 0
        where = set()
        for ref, rows in row_lists():
            for r in rows:
                rows_seen += 1
                for path, key, text in walk(r):
                    if isinstance(key, str) and key not in PLAY_FLAGS and (key == "tr" or key.startswith("tr_") or key.endswith("_tr")):
                        keys += 1
                        where.add(f"{ref}: key {path}")
                    if text is not None and TURKISH.search(text):
                        letters += 1
                        where.add(f"{ref}: text at {path}")
        self.assertGreater(rows_seen, 600)
        self.assertEqual((keys, letters), (0, 0), sorted(where)[:12])

    def test_the_table_files_hold_no_turkish_outside_the_name_blacklist(self):
        for name in WHOLE + ("antagonists.yaml", "claims.yaml"):
            text = (dt.tables_dir() / name).read_text(encoding="utf-8")
            self.assertIsNone(TURKISH.search(text), name)
            self.assertIsNone(re.search(r"(?m)\btr(_note)?:", text), name)
        naming = (dt.tables_dir() / "naming.yaml").read_text(encoding="utf-8")
        lines = [l for l in naming.split("\n") if TURKISH.search(l)]
        self.assertEqual(len(lines), 1, "only the blacklist of Turkish common nouns used as names")
        self.assertTrue(lines[0].strip().startswith("turkish_as_name:"))

    def test_the_english_fields_stand_where_the_turkish_stood(self):
        f = "foundation.yaml#"
        for r in dt.rows(f + "spine"):
            self.assertEqual(set(r["text"]) - {"ends", "ends_both", "heart_short", "key_place_short", "ends_short"}, {"name", "heart", "key_place", "travel"},
                             r["id"])      # build items 18e-2, 21a: the sentence's short names
            self.assertTrue(("ends" in r["text"]) != ("ends_both" in r["text"]), r["id"])
        for r in dt.rows(f + "ruin_source"):
            self.assertLessEqual({"name", "what", "remnant", "sites", "strangeness"}, set(r["text"]), r["id"])
        for r in dt.rows(f + "lifeline"):
            self.assertLessEqual({"name", "who", "yields", "weak_point"}, set(r["text"]), r["id"])
        for r in dt.rows(f + "contest"):
            self.assertTrue(r["text"]["name"] and all(isinstance(v["text"], str) and v["text"] for v in r["roles"].values()), r["id"])
            self.assertTrue(all(isinstance(x, str) and x for x in r["escalation"]), r["id"])
        for sub in ("palette", "break_target", "scar", "time", "escalation_tier"):
            for r in dt.rows(f + sub):
                self.assertTrue(r["text"]["name"], r["id"])
        for r in dt.rows("trope-breaks.yaml"):
            self.assertTrue(r["text"]["name"] and r["text"]["at_table"], r["id"])
        for sub, fields in (("people_trait", ("name", "at_table")), ("institution_practice", ("name", "gives")),
                            ("phenomenon_rule", ("name", "at_table"))):
            for r in dt.rows("signatures.yaml#" + sub):
                self.assertTrue(all(r["text"].get(k) for k in fields), r["id"])
        for r in dt.rows("tensions.yaml"):
            self.assertEqual(len(r["poles"]), 2)


class Setting(unittest.TestCase):

    def test_the_writing_language_is_no_dial(self):
        src = (SCRIPTS / "designer.py").read_text(encoding="utf-8")
        self.assertNotIn("--write-lang", src)
        self.assertEqual(dm.WRITE_LANG, "en")
        self.assertTrue(dm.writes_english({"_meta": {"write_lang": "en", "lang": "tr"}}))
        self.assertFalse(dm.writes_english({"_meta": {"lang": "tr"}}), "a birth from before build item 13a keeps its Turkish")

    def test_the_preamble_and_the_documents(self):
        common = (SKILL / "prompts" / "design" / "_common.md").read_text(encoding="utf-8")
        self.assertIn("The campaign is written in English", common)
        self.assertIn("nothing is transliterated or translated", common)
        self.assertIn("Turkish-speaking table", common, "the reader the DM narrates to")
        self.assertNotIn("apostrophe suffix", common)
        self.assertNotIn("Common nouns stay Turkish", common)
        self.assertIsNone(TURKISH.search(common))
        for phrase in ('"the player"', '"the party"', '"the table"', '"the campaign"', '"the PC"', '"skeleton"', '"stub"', '"the designer"'):
            self.assertIn(phrase, common, "the meta-language rule stays")
        design = (SKILL / "SKILL-design.md").read_text(encoding="utf-8")
        self.assertIn("written in English and played in Turkish", design)
        self.assertNotIn("The narration is Turkish; the world is not", design)


class NewBirth(unittest.TestCase):
    """One short test birth on disk: its P0 card, its P1 preroll, its public log and its P1 card hold no Turkish."""

    def setUp(self):
        self.guard = td.MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-english-{os.getpid()}-{uuid.uuid4().hex[:6]}"

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_preroll_cards_and_public_log_are_english(self):
        new = td.run("new", self.name, "--party-size", "2", "--seed", "ENGLISH-0001", "--scale", "standard", check=True)
        pre = td.run("-c", self.name, "preroll", "--phase", "P1", check=True)
        design = CAMPAIGNS / self.name / "design"
        manifest = json.loads((design / "design.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["_meta"]["write_lang"], "en")
        self.assertEqual(manifest["_meta"]["lang"], "tr", "the play language stays")
        cards = sorted(design.rglob("*.card.md"))
        self.assertTrue(cards, "the P0 card")
        card = td.run("-c", self.name, "phase", "P1", "card")
        texts = {"new": new.stdout, "preroll": pre.stdout, "the P1 card's printout": card.stdout,
                 "the public dice log": json.dumps(manifest["dice_log"], ensure_ascii=False),
                 "the foundation": json.dumps(manifest["foundation"], ensure_ascii=False),
                 "the identity": json.dumps(manifest["identity"], ensure_ascii=False)}
        for p in sorted(design.rglob("*.card.md")):
            texts[p.name] = p.read_text(encoding="utf-8")
        for what, text in texts.items():
            self.assertIsNone(TURKISH.search(text), what)
        for word in ("Faz", "kadranlar", "Tohum", "zar:", "Ölçek"):
            self.assertNotIn(word, texts["P0.card.md"] + new.stdout)
        self.assertIn("# Phase 0 — the dials", texts["P0.card.md"])
        for line in manifest["foundation"]["rendering"]:
            self.assertIn(f"{line['label']}: {line['text']}", pre.stdout)


class Door(unittest.TestCase):
    """The same fragment: refused in a birth written in English, accepted in a legacy birth."""

    LINE = "Sesi kısık, gözleri hep kapıda; yabancıya önce su ikram eder."

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("english")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def stage(self, summary, prose_line):
        pub = self.c.path("design/npcs/npc_tune_m.md")
        pub.write_text(FRONT.format(eid="npc_tune_m", etype="npc", secrecy="public", phase="P5", link="") + "\n" + prose_line + "\n", encoding="utf-8")
        r = row("npc_tune_m", "npc", "Marrow Quill", file="design/npcs/npc_tune_m.md")
        r["summary"] = summary
        self.c.write_json("design/_staging/P5/npc_tune_m.json", fragment("npc_tune_m", r, prose={"file": "design/npcs/npc_tune_m.md"}))

    def english(self, on: bool):
        m = self.c.json("design/design.json")
        if on:
            m["_meta"]["write_lang"] = "en"
        else:
            m["_meta"].pop("write_lang", None)
        self.c.write_json("design/design.json", m)

    def merge(self):
        return self.c.run("registry.py", "merge", "--phase", "P5")

    def test_a_turkish_letter_is_refused_in_a_new_birth_and_kept_in_a_legacy_one(self):
        self.english(True)
        self.stage("limanın kısık sesli hancısı", "A hoarse innkeeper who watches the door.")
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Turkish letters in 1 field(s) (summary)", proc.stderr)
        self.assertNotIn("kısık", proc.stderr, "the refusal names the field, never the text")
        self.stage("the harbour's hoarse innkeeper", self.LINE)
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        self.assertRegex(proc.stderr, r"prose file design/npcs/npc_tune_m\.md carries Turkish letters on 1 line\(s\) \(first: line \d+\)")
        self.stage("the harbour's hoarse innkeeper", "A hoarse innkeeper who watches the door.")
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)

    def test_the_same_fragment_passes_in_a_legacy_birth(self):
        self.english(False)
        self.stage("limanın kısık sesli hancısı", self.LINE)
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)

    def test_the_dm_only_layer_is_held_to_it_too(self):
        errs = registry.language_errors("npc_x", {"name": "Marrow Quill", "dm_only": {"secret_tr": "gerçekte kaçak bir büyücü"}}, None, self.c.path("."))
        self.assertEqual(len(errs), 1)
        self.assertIn("dm_only.secret_tr", errs[0])
        self.assertNotIn("büyücü", errs[0])
        self.assertEqual(registry.language_errors("npc_x", {"name": "Marrow Quill", "summary": "a runaway caster"}, None, self.c.path(".")), [])

    def test_a_turkish_common_noun_as_a_name_is_still_refused(self):
        bl = registry.naming_blacklist()
        self.assertTrue(any("Turkish common noun" in e for e in registry.naming_errors("faction_x", {"type": "faction", "name": "Lonca"}, bl, set())))
        self.assertTrue(any("Turkish letters" in e for e in registry.naming_errors("npc_x", {"type": "npc", "name": "Şahin Vale"}, bl, set())))


if __name__ == "__main__":
    unittest.main()
