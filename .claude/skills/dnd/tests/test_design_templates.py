"""
test_design_templates.py — the design/ templates keep the shape the scripts parse.

Slice 1's validator and the `sites` / `travel` parsers rely on a few fixed
anchors in generated files: the front-matter block, the three secrecy headings,
the room table's `Exits` column with its `[Entrance]` / `[Payoff]` markers, the
beat fields `change_kind` / `state_before` / `state_after`, the travel table's
six categories. These cases pin those anchors in the templates themselves.
"""

import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates" / "design"

EXPECTED = {"README.md", "premise.md", "cosmology.md", "region.md", "settlement.md",
            "faction.md", "npc.md", "site-skeleton.md", "site-detailed.md", "chapter.md",
            "arc.md", "consequence-calculus.md", "thread.md", "primer.md", "report.md"}
ENTITY_TEMPLATES = EXPECTED - {"README.md"}
THREE_HEADINGS = ("## Public", "## Discoverable", "## Secret")
TRAVEL_CATEGORIES = ("Quiet/Texture", "Social", "Environmental", "Combat", "Discovery",
                     "Faction/Political")

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def read(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


class DesignTemplates(unittest.TestCase):

    def test_every_expected_template_exists(self):
        present = {p.name for p in TEMPLATES.glob("*.md")}
        self.assertEqual(EXPECTED - present, set())

    def test_front_matter_names_the_entity_and_its_secrecy(self):
        for name in sorted(ENTITY_TEMPLATES):
            with self.subTest(name):
                m = FRONT_MATTER.match(read(name))
                self.assertIsNotNone(m, "front matter block missing")
                block = m.group(1)
                self.assertRegex(block, r"\Aentity: \w+", "entity: line missing")
                self.assertRegex(block, r"(?m)^type: \w+$", "type: line missing")
                self.assertRegex(block, r"(?m)^secrecy: (public|discoverable|secret)$")
                self.assertRegex(block, r"(?m)^phase: P\d$")
                self.assertRegex(block, r"(?m)^stamped: \[")
                self.assertRegex(block, r"(?m)^mirror: ")

    def test_three_secrecy_headings_in_order(self):
        # The primer is the one file fully open to the player: public by
        # construction, no secrecy split, so it is the one exception here.
        for name in sorted(ENTITY_TEMPLATES - {"primer.md"}):
            with self.subTest(name):
                text = read(name)
                positions = [text.find(h) for h in THREE_HEADINGS]
                self.assertTrue(all(p >= 0 for p in positions), f"missing heading in {name}")
                self.assertEqual(positions, sorted(positions), "headings out of order")

    def test_detailed_site_room_table_is_machine_readable(self):
        text = read("site-detailed.md")
        self.assertIn("| # | Room | Category | Content | Exits | XP |", text)
        self.assertIn("[Entrance]", text)
        self.assertIn("[Payoff]", text)
        self.assertIn("Minimum depth", text)
        for category in ("combat", "trap", "special", "structural"):
            self.assertIn(category, text)

    def test_skeleton_site_carries_the_directory_fields(self):
        text = read("site-skeleton.md")
        for anchor in ("Telegraphs", "far", "near", "threshold", "Escape geometry",
                       "If never visited", "Attitude to intruders", "Reoccupation"):
            self.assertIn(anchor, text, anchor)

    def test_beats_are_consequence_shaped_by_structure(self):
        text = read("arc.md")
        for field in ("change_kind", "state_before", "state_after", "world_pressure",
                      "delivery paths", "fallbacks", "*cost:*", "*secondary:*", "*deferred:*"):
            self.assertIn(field, text, field)
        for ending in ("**Win:**", "**Loss:**", "**Pyrrhic:**"):
            self.assertIn(ending, text, ending)

    def test_region_travel_table_has_six_categories_and_hook_marks(self):
        text = read("region.md")
        for category in TRAVEL_CATEGORIES:
            self.assertIn(f"##### {category} (d6)", text, category)
        self.assertIn("[KANCA]", text)
        self.assertIn("Early tier", text)
        self.assertIn("Late tier", text)

    def test_faction_has_the_six_doctrine_triggers_and_stances(self):
        text = read("faction.md")
        for trigger in ("alliance", "loss", "gain", "exposure", "death", "betrayal"):
            self.assertRegex(text, rf"\| {trigger} \|")
        for anchor in ("Stances", "First operation", "Abandon if", "Heir", "Betrayal candidate",
                       "Internal fracture", "Endgame"):
            self.assertIn(anchor, text, anchor)

    def test_npc_dossier_carries_the_standard_and_the_minor_variant(self):
        text = read("npc.md")
        for anchor in ("Voice samples", "Known Facts", "Personality", "Relationships",
                       "Surfacing path", "What changes if they die", "### Minor",
                       "What they can offer the party"):
            self.assertIn(anchor, text, anchor)

    def test_readme_lists_every_template(self):
        readme = read("README.md")
        for name in sorted(ENTITY_TEMPLATES):
            self.assertIn(f"`{name}`", readme, name)


if __name__ == "__main__":
    unittest.main()
