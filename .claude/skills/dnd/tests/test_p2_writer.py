"""
test_p2_writer.py — build item 22d (docs/p2-build-22.md part 22d; docs/p2-tags.md S7): the cosmos writer, its critics
and its card.

- The prompt and the template are written on the frame: the writer copies every rolled field and every pooled name,
  fills only `fill`, runs `registry.py check`, invents no proper noun and decides nothing; "the big secret usually hides
  in this layer" and "all months 30 days" are gone; a villain's god appears only when the threat pins one.
- The rubrics as S7 #2 says: the threat in the cosmos, the threat on the timeline, the calendar felt, legible at a D&D
  table; a script-rolled P2's critics judge craft only (pass or fix; a `rerun` is refused) and a fix on a rubric the
  critic was not given is refused (19a).
- The P2 card, built by script: the gods with their ranks and domains, the planes, magic in words, the ages, the
  calendar and the start date; no die, no row id, no secret seat.
- A birth whose P1 predates the foundation keeps the old prompt, the old template and the old card.
"""

import json
import re
import shutil
import sys
import unittest

from _campaign import SCRIPTS, SKILL, USED, MarkerGuard, TestCampaign

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_cosmos_door as cd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_prompts as dpm  # noqa: E402
import design_tables as dt  # noqa: E402
from test_cosmos_door import P2Walk  # noqa: E402

PROMPT = (SKILL / "prompts" / "design" / "P2.cosmos.md").read_text(encoding="utf-8")
TEMPLATE = (SKILL / "templates" / "design" / "cosmology.md").read_text(encoding="utf-8")
P2_TABLES = ("pantheon.yaml", "planes.yaml", "magic.yaml", "history.yaml", "calendar.yaml")


class Words(unittest.TestCase):
    """The prompt, the template and the rubrics, as written."""

    def test_the_prompt_is_written_on_the_frame(self):
        for words in ("{{frame_path}}", "fill the fields `fill` names", "copy every other field unchanged",
                      "You invent no proper noun", "You decide nothing the rolls decide",
                      "registry.py -c {{campaign}} check --phase {{staging_phase}} --id {{entity_id}}",
                      "A villain's god appears only when the threat seats one", "the 2014 rules"):
            self.assertIn(words, PROMPT)
        for gone in ("big secret", "30 days", "usually hides", "a secret with a tier"):
            self.assertNotIn(gone, PROMPT)
            self.assertNotIn(gone, TEMPLATE)
        self.assertIn("twelve months of 28 days, a seven-day week", TEMPLATE)
        # the 22d audit: divergences are discoverable, the god story too; the mirror holds every seated god; the
        # underground count; churches by the temple pattern; the pilgrim road's god; spans and ages are the script's
        for words in ("a divergence is discoverable, never secret", "`as_happened`", "the god story (here only",
                      "each god the threat seats", "`underground_count`", "the <building word> of <the god's name>",
                      "never by a new name: P4 names the factions", "its road, its holy place", "an age's `span`, an event's `era`"):
            self.assertIn(words, PROMPT)
        self.assertNotIn("A story the priests do not tell", TEMPLATE)
        discoverable = TEMPLATE.split("## Discoverable")[1].split("## Secret")[0]
        self.assertIn("The god story", discoverable)
        self.assertIn("Events — as they happened", discoverable)
        secret = TEMPLATE.split("## Secret")[1]
        self.assertIn("The gods the threat seats", secret)
        self.assertNotIn("divergence", secret, "only the villain's origin's truth stays in the mirror")
        self.assertIn("Below ground", TEMPLATE)

    def test_the_rubrics(self):
        rows = {r["id"]: r for r in dt.rows("rubrics.yaml#phase_rubric") if r["phase"] == "P2"}
        self.assertEqual(sorted(rows), ["rubric_p2_calendar_felt", "rubric_p2_dnd_legible", "rubric_p2_gods_carry_question",
                                        "rubric_p2_history_diverges"])
        gods = rows["rubric_p2_gods_carry_question"]["question"]
        for words in ("pins a god", "the planes P1 names", "each side of the premise's question"):
            self.assertIn(words, gods)
        # the 22d audit: the two rubrics that judge the mirror are read by the critic given the mirror
        self.assertEqual({k: r["scope"] for k, r in rows.items()},
                         {"rubric_p2_gods_carry_question": "dm-only", "rubric_p2_history_diverges": "dm-only",
                          "rubric_p2_calendar_felt": "phase", "rubric_p2_dnd_legible": "phase"})
        entity = {r["id"] for r in dpm.rubric_rows("P2", "entity")}
        self.assertLessEqual({"rubric_p2_gods_carry_question", "rubric_p2_history_diverges"}, entity)
        self.assertIn("the cosmos's secret half", dpm.P2_ROLLS)
        self.assertNotIn("villain's answer", gods, "rewritten on the threat (S7 #2)")
        hist = rows["rubric_p2_history_diverges"]["question"]
        for words in ("the move, the ruin's age and the villain's origin", "second secret"):
            self.assertIn(words, hist)
        legible = rows["rubric_p2_dnd_legible"]["question"]
        for words in ("cleric or paladin", "plane spells", "a character's spells", "the threat's dates"):
            self.assertIn(words, legible)
        self.assertIn("Could a player tell which month it is", rows["rubric_p2_calendar_felt"]["question"], "kept")
        craft = dt.load("rubrics.yaml")["tables"]["phase_rubric"]["p2_craft_only"]
        self.assertIn("pass or fix", craft)


class OnDisk(unittest.TestCase):
    """One standard birth whose P1 pins a god, walked to a merged P2."""

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        if USED.is_file():
            USED.unlink()
        cls.p2 = P2Walk("standard", "COSMOS-PIN-17")
        cls.p2.write()
        merge = cls.p2.merge()
        assert "✗" not in merge.stderr, merge.stderr[-2000:]
        cls.name = cls.p2.w.name

    @classmethod
    def tearDownClass(cls):
        cls.p2.w.remove()
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def test_the_writer_prompt_renders_on_the_frame(self):
        text = dpm.render(self.name, "P2.cosmos", "doc_cosmology")
        self.assertIn(cd.frame_rel(), text)
        self.assertIn("templates/design/cosmology.md", text)
        self.assertNotIn("cosmology.legacy.md", text)
        # the 22d audit: "produce exactly this many" after the counts only, never after a year or a day
        counts = {r["label"] for r in dm.load(self.name)["dice_log"] if r.get("phase") == "P2" and r.get("count")}
        said = re.findall(r"`([^`<]+)` = \*\*[^*]+\*\* — produce exactly this many", text)
        self.assertTrue(said)
        self.assertEqual(set(said), counts)
        self.assertRegex(text, r"`event\.\d+\.years_ago` = \*\*\d+\*\*\n")

    def test_the_critics_judge_craft_only(self):
        for name in ("critic", "phase_critic"):
            text = dpm.render(self.name, name, "doc_cosmology", phase_override="P2")
            self.assertIn("**Craft only.**", text, name)
            self.assertIn("doc_cosmology.frame.json", text, name)
            self.assertNotIn('"rerun"', text, f"{name}: the schema offers no rerun")
        staging = self.p2.staging
        f = staging / "doc_cosmology.critic1.json"
        cases = (({"entity_id": "doc_cosmology", "verdict": "rerun", "findings": []}, "says `rerun`, refused"),
                 ({"entity_id": "doc_cosmology", "verdict": "fix", "findings": [
                     {"rubric_id": "rubric_p1_legible", "entity_id": "doc_cosmology", "verdict": "fix", "reason_code": "my_taste"}]},
                  "a fix names a rubric this critic was not given"))
        for ret, words in cases:
            f.write_text(json.dumps(ret), encoding="utf-8")
            import contextlib
            import io
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(da.record_critique(self.name, "P2", str(f), 1), 1)
            self.assertIn(words, err.getvalue())
        f.unlink()

    def test_the_card(self):
        card = da.build_card(self.name, "P2")
        m = dm.load(self.name)
        cos = m["cosmos"]
        for head in ("# P2 — THE COSMOS", "## THE PANTHEON", "Where the dead go", "## THE PLANES", "## MAGIC", "## HISTORY",
                     "## THE CALENDAR", "The start", "## PROMISES", "## CHECKS", "## YOUR MOVES"):
            self.assertIn(head, card)
        domains = {r["id"]: r["label"] for r in dt.rows("pantheon.yaml#domain_scaffold")}
        for g in cos["gods"]:
            self.assertIn(g.get("name") or "(its name is not spoken)", card)
            for d in g["domains"]:
                self.assertIn(domains[d], card)
        for pl in cos["planes"]:
            self.assertIn(pl["name"], card)
        for a in cos["ages"]:
            self.assertIn(a["name"], card)
        for x in cos["calendar"]["month_names"] + cos["calendar"]["day_names"]:
            self.assertIn(x, card)
        self.assertIn("12 months of 28 days, a 7-day week", card)
        visible = "\n".join(l for l in card.splitlines() if not l.startswith("<!--"))
        self.assertFalse(re.search(r"\bd\d{1,3}\b", visible), "no die on the card")
        ids = {r["id"] for name in P2_TABLES for rows in dt.all_row_lists(dt.load(name)).values() for r in rows}
        self.assertEqual(sorted(i for i in ids if re.search(r"(?<![\w-])" + re.escape(i) + r"(?![\w-])", visible)), [],
                         "no row id on the card")
        secret = json.loads((self.p2.w.dir / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))["cosmos"]
        for name in (secret.get("hidden_names") or {}).values():
            self.assertNotIn(name, card, "no hidden name")
        self.assertTrue(secret.get("hidden_names"), "the seed pins a god")
        for words in ("seat", "threat", "mirror", "pinned", "home"):
            self.assertNotIn(words, visible.lower(), f"no secret seat ({words})")
        # the 22d audit: grammar, names for the regulator and the keepers, the festivals in calendar order
        self.assertNotIn("power(s)", visible)
        self.assertNotIn("The signature institution", visible)
        fest = next(l for l in visible.splitlines() if l.strip().startswith("Festivals"))
        months = cos["calendar"]["month_names"]
        dates = [(months.index(mo) + 1, int(d)) for d, mo in re.findall(r"\((\d+) (\w+)\)", fest)]
        self.assertEqual(dates, sorted(dates))
        for pl in cos["planes"]:
            creature = (pl.get("keeper") or {}).get("creature")
            if creature:
                import design_cosmos as dcos
                self.assertIn(dcos.creature_name(creature), card)
        da.write_card(self.name, "P2", None)                      # the leak scan passes
        self.assertTrue((self.p2.w.dir / "design/_approval/P2.card.md").is_file())


class Legacy(unittest.TestCase):
    """A birth whose P1 predates the foundation keeps its P2 prompt, template and card."""

    def test_the_legacy_prompt_template_and_card(self):
        guard = MarkerGuard().__enter__()
        c = TestCampaign("p2writer")
        try:
            m = dm.load(c.name)
            self.assertFalse(m.get("foundation") or cd.applies(m))
            text = dpm.render(c.name, "P2.cosmos", "doc_cosmology")
            self.assertIn("templates/design/cosmology.legacy.md", text)
            self.assertIn("big secret usually hides", text, "the legacy prompt as it was")
            card = da.build_card(c.name, "P2")
            self.assertIn("# Phase card — P2", card)
            self.assertNotIn("THE COSMOS", card)
            self.assertNotIn("Craft only", dpm.render(c.name, "critic", "doc_cosmology", phase_override="P2"))
        finally:
            c.remove()
            guard.__exit__(None, None, None)
        legacy = (SKILL / "templates" / "design" / "cosmology.legacy.md").read_text(encoding="utf-8")
        self.assertIn("Months (30 days each)", legacy, "the legacy template as it was")


if __name__ == "__main__":
    unittest.main()
