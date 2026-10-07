"""
test_p1_writer.py — build item 14a (docs/p1-build-14.md, Part 14a): the P1 writer builds on the rolls. The rendered
prompt of a new birth points at the records, the candidates and the due promises, names the archetype's `cause` and
the chooser, shows no earlier campaign, asks for nothing the script now rolls and holds no secret row and no
secret-stock name. A legacy birth's P1 prompt renders as before. The registry's text fields take English names
(`question`, `rule`, `true_rule`); a legacy row's old names still load.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign

sys.path.insert(0, str(SCRIPTS))
import design_prompts as dpm  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import text_field  # noqa: E402

PROMPTS = SCRIPTS.parent / "prompts" / "design"
NEW = (PROMPTS / "P1.premise.md").read_text(encoding="utf-8")
TEMPLATE = (SCRIPTS.parent / "templates" / "design" / "premise.md").read_text(encoding="utf-8")


class Prompt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        cls.name = f"_test-writer-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
        for args in (["new", cls.name, "--party-size", "2", "--seed", "WRITER-0001", "--lang", "tr", "--scale", "standard"],
                     ["-c", cls.name, "preroll", "--phase", "P1"]):
            subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "designer.py"), *args], capture_output=True, text=True, env=env, check=True)
        cls.dir = CAMPAIGNS / cls.name
        cls.text = dpm.render(cls.name, "P1.premise")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CAMPAIGNS / cls.name, ignore_errors=True)
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def test_the_prompt_points_at_the_records_the_candidates_and_the_promises(self):
        t = self.text
        for needle in ("design/design.json#foundation", "design/design.json#identity", "`overrides`", "recorded merges",
                       "`design/naming.json`", "`candidates`", "**Names (rolled, never invented).**", "**Promises due at this phase.**",
                       "design/dm-only/dice-log.json", "under `threat`", "the four `facts`", "`spine_sentence`",   # build item 18e: the chain
                       # build item 20a: the rolled fields are the script's frame; the prompt names the frame and what the writer fills
                       ".frame.json`", "copy every other field unchanged", "`pinned.god`", "`signature_<slug of that name>`",
                       "`appears`", "`row` and `tie`", "`stamped` stays an object"):
            self.assertIn(needle, t, needle)
        m = json.loads((self.dir / "design/design.json").read_text(encoding="utf-8"))
        for p in m["promises"]:
            self.assertEqual(f"`{p['id']}`" in t, p["due"] == "P1", "the promises due at P1 and no other")
        self.assertIn("`stages`", t, "build item 18e: the clue stages come from the chain's secret record")
        self.assertIn("No people is evil by birth", t)
        self.assertNotIn("{{", t)

    def test_the_writer_sees_no_earlier_campaign_and_is_asked_for_nothing_the_script_rolls(self):
        self.assertNotIn("{{prior_campaigns}}", NEW)
        self.assertNotIn("Earlier campaigns", self.text)
        for name in ("critic", "phase_critic"):
            self.assertIn("{{prior_campaigns}}", (PROMPTS / f"{name}.md").read_text(encoding="utf-8"), "the block stays with the critics")
        low = NEW.lower()
        for gone in ("by act", "act 1", "choose roots", "roots chosen", "mutat", "{{phase_rolls}}", "sample name", "question_tr", "rule_tr"):
            self.assertNotIn(gone, low, gone)
        self.assertNotIn("from the rolled families", NEW)
        self.assertIn("you neither write nor edit `design/naming.json`", NEW)
        for never in ("You change no field of the foundation or the identity", "You invent no proper noun", "You write no example name",
                      "You add no faction, god, place or person", "The door refuses each of these"):
            self.assertIn(never, NEW)
        self.assertEqual(NEW.count("invent no proper noun"), 1, "said once, plainly")

    def test_no_secret_row_and_no_secret_stock_name_is_in_the_prompt(self):
        log = json.loads((self.dir / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))
        rows = [dt.row(r["table"], r["row_id"]) for r in log["rolls"] if r.get("row_id") and ".yaml" in str(r.get("table"))]
        self.assertGreaterEqual(len(rows), 8)
        for n, r in enumerate(x for x in rows if x):
            self.assertNotIn(r["id"], self.text, f"secret row {n}: its id is in the prompt")
            for key in ("statement", "cause", "rule"):
                if isinstance(r.get(key), str) and len(r[key]) > 20:
                    self.assertNotIn(r[key], self.text, f"secret row {n}: its {key} is in the prompt")
        stock = json.loads((self.dir / "design/dm-only/name-pool-secret.json").read_text(encoding="utf-8"))
        names = [e["name"] for L in stock["languages"].values() for v in L.values() for e in v]
        leaked = [n for n in names if re.search(rf"(?<![\w]){re.escape(n)}(?![\w])", self.text)]
        self.assertEqual(len(leaked), 0, f"{len(leaked)} secret-stock name(s) in the prompt")
        for p in dp.load_secret(self.name):
            self.assertNotIn(p["text"], self.text)
        for word in ("secret_", "chooser_", "twist_", "trail_", "shape_", "origin_", "bond_"):
            self.assertFalse(re.search(rf"\b{word}[a-z]+_[a-z_]+\b", NEW.replace("secret_archetype", "").replace("secret_twist", "").replace("secret_class", "").replace("secret_tr", "")),
                             f"the prompt file names a secret row ({word})")

    def test_the_template_follows_the_sections(self):
        for head in ("### The question", "### The three signatures", "### The trope break(s)", "### The languages",   # 18e: "What it was" gone (W5)
                     "### The player pitch", "### Only here", "### The secret", "### The three clues, by stage", "### The villain", "### DM pitch", "### Signature mechanic"):
            self.assertIn(head, TEMPLATE, head)
        self.assertIn("stamped: [question, signatures, trope_breaks]", TEMPLATE)
        self.assertNotIn("| # | Act |", TEMPLATE, "the clues are told by stage, not by act")
        self.assertNotIn("Naming languages", TEMPLATE)
        self.assertNotIn("samples:", TEMPLATE)
        self.assertIsNone(re.search("[çğıöşüÇĞİÖŞÜ]", TEMPLATE + NEW))
        skill = (SCRIPTS.parent / "SKILL-design.md").read_text(encoding="utf-8")
        self.assertIn("by script at the preroll: `design.json#foundation`, `#identity`, `#promises`, `design/naming.json`", skill)


class Legacy(unittest.TestCase):

    def test_a_legacy_births_p1_prompt_renders_as_before(self):
        guard = MarkerGuard().__enter__()
        c = TestCampaign("writer")
        try:
            text = dpm.render(c.name, "P1.premise")
            fm, body = dpm.load("P1.premise.legacy")
            self.assertIn("### Rolls you must honour", text, "the prompt it was written by")
            self.assertIn("{{prior_campaigns}}", body)
            self.assertNotIn("What you never do, and why", text)
            self.assertNotIn("Promises due at this phase", text, "a legacy birth has no ledger")
            self.assertEqual(dpm.prompt_for("P1", "premise_x"), "P1.premise")
        finally:
            c.remove()
            guard.__exit__(None, None, None)

    def test_the_new_field_names_are_read_and_the_old_ones_still_load(self):
        self.assertEqual(text_field({"question": "new"}, "question"), "new")
        self.assertEqual(text_field({"question_tr": "old"}, "question"), "old")
        self.assertEqual(text_field({"rule": "new", "rule_tr": "old"}, "rule"), "new")
        self.assertEqual(text_field({"true_rule_tr": "old"}, "true_rule"), "old")
        self.assertIsNone(text_field({}, "rule"))
        self.assertIsNone(text_field(None, "rule"))
        import render_dm
        import render_player
        import inspect
        for mod in (render_dm, render_player):
            src = inspect.getsource(mod)
            self.assertIn("text_field(", src)
            self.assertNotIn("['rule_tr']", src)
        docs = (SCRIPTS.parents[3] / "docs" / "schemas" / "entities.md").read_text(encoding="utf-8")
        self.assertIn("**`question`** (a legacy row: `question_tr`)", docs)
        self.assertIn("`dm_only.true_rule` (legacy: `true_rule_tr`)", docs)
        # the validator's verbatim-leak scan reads the new secret field as it reads the old
        import design_check
        self.assertIn('"true_rule"', inspect.getsource(design_check.check_secrecy))


if __name__ == "__main__":
    unittest.main()
