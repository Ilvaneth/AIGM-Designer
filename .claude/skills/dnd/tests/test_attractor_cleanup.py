"""
test_attractor_cleanup.py — build item 15 (docs/p1-build-15.md): what was left of the attractor cleanup. The P0 and
P1 tables hold no example list, no sample name and no note that names the attractor's matter; the history table keeps
every row (the owner's ruling of 2026-10-04) and one id changes: `age_lanterns` is `age_of_thing`, and a legacy
birth that holds the old id still loads.
"""

import random
import re
import sys
import unittest

from _campaign import SCRIPTS, MarkerGuard, TestCampaign

sys.path.insert(0, str(SCRIPTS))
import design_dice as dd  # noqa: E402
import design_tables as dt  # noqa: E402

TABLES = ("dials.yaml", "scale.yaml", "foundation.yaml", "trope-breaks.yaml", "signatures.yaml", "tensions.yaml", "naming.yaml")
SAMPLE_KEYS = re.compile(r"^(examples?|samples?|samples_.*|sample_.*|mutations?|mutation_prompts?|feel)$")
# the attractor's matter, as a note or an example would name it (a row's own substance and the lexicon's roots are no note)
MATTER = re.compile(r"\b(lanterns?|lamps?|candles?|tallow|hush|bells?|ledgers?|tolls?|tribunals?|assizes?|tides?|tidal|salt)\b", re.I)


def keys_of(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield f"{path}.{k}" if path else str(k), str(k)
            yield from keys_of(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for v in node:
            yield from keys_of(v, path)


class Tables(unittest.TestCase):

    def test_no_example_and_no_sample_name_field(self):
        for name in TABLES:
            hits = [path for path, key in keys_of(dt.load(name)) if SAMPLE_KEYS.match(key)]
            self.assertEqual(hits, [], name)

    def test_no_note_or_comment_names_the_attractors_matter(self):
        for name in TABLES:
            text = (dt.tables_dir() / name).read_text(encoding="utf-8")
            comments = "\n".join(line.split("#", 1)[1] for line in text.split("\n") if line.lstrip().startswith("#"))
            self.assertIsNone(MATTER.search(comments.replace("promise ledger", "")), f"{name}: a comment names the attractor's matter")
            doc = dt.load(name)
            notes = [str(v) for path, key in keys_of(doc) if key in ("note", "calendar_note", "text_note", "name_note")
                     for v in [self.dig(doc, path)] if isinstance(v, str)]
            for note in notes:
                self.assertIsNone(MATTER.search(note), f"{name}: a note names the attractor's matter")
        era = dt.dial_row("era", "underground")
        self.assertEqual(era["effects"]["calendar_note"], "the sun and the moon are known but seldom seen; those below count time by what the deep gives")

    def dig(self, node, path):
        for part in path.split("."):
            if isinstance(node, dict):
                node = node.get(part)
            else:
                return None
        return node

    def test_the_lexicon_keeps_its_roots(self):
        roots = {r["root"] for r in dt.load("naming.yaml")["lexicon"]["roots"]}
        self.assertTrue({"lantern", "lamp", "candle", "hush", "bell", "tide", "salt", "toll"} <= roots, "errata 24.2 #18: no word is banned")


class History(unittest.TestCase):

    def test_no_row_left_the_history_table_and_one_id_changed(self):
        ages = {r["id"]: r for r in dt.rows("history.yaml#age_template")}
        self.assertIn("age_of_thing", ages)
        self.assertNotIn("age_lanterns", ages)
        self.assertEqual(ages["age_of_thing"]["label"], "The Age of {Thing}")
        self.assertEqual(ages["age_of_thing"]["span_hint"], "an age named for what was built in it (roads, walls, mills)", "the owner's wording of 2026-10-05")
        self.assertTrue({"age_silence", "age_dimming", "age_reckoning"} <= set(ages), "the owner keeps them")
        self.assertIn("evtype_silencing", {r["id"] for r in dt.rows("history.yaml#event_type")})
        labels = {r["label"] for sub in ("age_template", "event_type", "divergence", "memory") for r in dt.rows(f"history.yaml#{sub}")}
        self.assertTrue({"The Silence", "The Dimming", "The Reckoning", "A silencing"} <= labels)

    def test_age_of_thing_is_drawn(self):
        rows = dt.rows("history.yaml#age_template")
        drawn = {dd.draw(random.Random(seed), rows)["row_id"] for seed in range(400)}
        self.assertIn("age_of_thing", drawn)
        self.assertEqual(drawn, {r["id"] for r in rows}, "every age is drawn")

    def test_a_legacy_birth_with_the_old_id_loads(self):
        self.assertEqual(dt.row("history.yaml#age_template", "age_lanterns")["id"], "age_of_thing")
        self.assertEqual(dt.ROW_ALIASES, {"age_lanterns": "age_of_thing"})
        self.assertEqual(dd._resolve(["age_lanterns", "age_silence"], "history.yaml#age_template"), {"age_of_thing", "age_silence"},
                         "a row another campaign drew under the old id is still spent")
        guard = MarkerGuard().__enter__()
        c = TestCampaign("cleanup")
        try:
            m = c.json("design/design.json")
            m["dice_log"].append({"phase": "P2", "table": "history.yaml#age_template", "label": "age.1", "notation": "d8", "raw": 3,
                                  "row_id": "age_lanterns", "excluded": [], "attempt": 1, "ts": "2026-09-25T10:00:00Z"})
            c.write_json("design/design.json", m)
            import design_prompts as dpm
            text = dpm.render(c.name, "P2.cosmos")
            self.assertIn("`age.1` → **age_lanterns**", text, "the birth keeps the id it rolled")
            self.assertIn("age_lanterns", dd.prior_rolls(c.name, "P3"))
            self.assertEqual(c.run("design_manifest.py", "status").returncode, 0)
        finally:
            c.remove()
            guard.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
