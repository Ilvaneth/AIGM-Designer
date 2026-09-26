"""
test_skill_docs.py — the skill's reference files after the designer landed (plan item 21.A-C,
slice 1c item 7): SKILL-design.md exists and names every designer script, every phase and the
workflow loop; SKILL-commands.md carries the designer's `new` and the `design` family and no longer
the retired wizard; SKILL.md carries the blind-conductor section the read guard cites, the
world-does-not-scale standard, the refreshed routing table and the layout lines.
"""

import re
import sys
import unittest
from pathlib import Path

from _campaign import SKILL, SCRIPTS, PROJECT

sys.path.insert(0, str(SCRIPTS))


def read(name: str) -> str:
    return (SKILL / name).read_text(encoding="utf-8")


class Docs(unittest.TestCase):

    def test_skill_design_covers_scripts_phases_and_the_loop(self):
        text = read("SKILL-design.md")
        for script in ("designer.py", "design_prompts.py", "design_approval.py", "design_revise.py", "render_player.py",
                       "design_check.py", "registry.py", "design_manifest.py"):
            self.assertIn(script, text, script)
        for phase in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"):
            self.assertRegex(text, r"\| %s " % phase)
        for step in ("preroll", "phase PN begin --json", "design-skeleton", "design-fanout", "phase PN merge", "phase PN check",
                     "phase PN card", "approve --onay", "`devam`"):
            self.assertIn(step, text, step)
        for command in ("design status", "design phase", "design detail", "design check", "design integrate", "design primer",
                        "design revise", "design ask", "design abandon", "arc fallback"):
            self.assertIn(f"`{command}", text, command)
        self.assertIn("The blind conductor", text)
        self.assertIn("The world does not scale", text)
        self.assertIn("errata 24.2 #19", text, "the gods appendix rule")
        self.assertIn("auto-approves", text)

    def test_skill_commands_new_is_the_designer_and_the_wizard_is_gone(self):
        text = read("SKILL-commands.md")
        self.assertIn("## `/dm:dnd new <campaign-name>` — the Campaign Designer", text)
        self.assertIn("## `/dm:dnd design <status", text)
        self.assertNotIn("Tone/Genre Wizard", text)
        self.assertNotIn("Generate a committed narrative arc? [y/n", text)
        self.assertIn("designer.py new", text)
        self.assertIn("SKILL-design.md", text)
        self.assertLess(text.index("## `/dm:dnd new"), text.index("## `/dm:dnd load"), "the designer section keeps `new`'s place before `load`")

    def test_skill_md_carries_the_conductor_the_standard_and_the_layout(self):
        text = read("SKILL.md")
        self.assertIn("## The blind conductor — the Campaign Designer", text)
        self.assertIn("### 15. The World Does Not Scale", text)
        self.assertIn("SKILL-design.md", text)
        self.assertIn("prompts/design/", text)
        self.assertIn("data/design/", text)
        self.assertIn(".claude/workflows/", text)
        self.assertNotIn("claude-sonnet-4-6", text, "routing ids refreshed")
        self.assertNotIn("claude-opus-4-6", text)
        self.assertIn("claude-opus-5-5", text)
        self.assertIn("claude-fable-5-1", text)
        self.assertIn("design/overlay.json", text)

    def test_slice_1d_play_integration_is_documented(self):
        commands = read("SKILL-commands.md")
        for key in ("designer.py -c <campaign-name> load-pack", "scene --enter", "end-pack --day", "registry.py -c <name> add --type pc",
                    "registry.py -c <name> add --type npc", "render_dm.py -c <name> world npcs index", "Stated destination"):
            self.assertIn(key, commands, key)
        self.assertIn("threat stage", read("SKILL-travel.md"))
        self.assertIn("map_travel.py -c <name> encounters", read("SKILL-travel.md"))
        self.assertIn("site_progress.py -c <name> enter", read("SKILL-combat.md"))
        self.assertIn("--reference --tier", read("SKILL-encounter-design.md"))
        design = read("SKILL-design.md")
        self.assertIn("## In play", design)
        self.assertIn("detail ID --finish", design)
        scripts = read("SKILL-scripts.md")
        for key in ("map_travel.py", "render_dm.py", "play_pack.py", "--reference --tier"):
            self.assertIn(key, scripts, key)
        self.assertIn("load-pack", read("SKILL.md"))

    def test_slice_1e_dry_run_and_playtest_are_documented(self):
        scripts = read("SKILL-scripts.md")
        for key in ("design_leak_scan.py", "design_compare.py", "load_budget.py", "playtest.py", "subagent_type: player", "--player"):
            self.assertIn(key, scripts, key)
        self.assertIn("--player", read("SKILL.md"))
        self.assertIn("phase P9 begin --json", read("SKILL-design.md"))
        self.assertTrue((PROJECT / "docs" / "dry-run-and-playtest.md").is_file())
        self.assertTrue((PROJECT / ".claude" / "agents" / "player.md").is_file())
        for name in ("player", "judge_playtest", "judge_readability", "judge_uniqueness"):
            self.assertTrue((SKILL / "prompts" / "play" / f"{name}.md").is_file(), name)

    def test_critique_analysis_is_documented(self):
        self.assertIn("design_critique_stats.py", read("SKILL-scripts.md"))
        self.assertIn("The registry door", read("SKILL-scripts.md"))
        self.assertIn("at the registry door", read("SKILL-design.md"))
        self.assertTrue((PROJECT / "docs" / "reports" / "critique-analysis-1.md").is_file())

    def test_guard_cites_a_heading_that_exists(self):
        guard = (SCRIPTS / "hooks" / "design_read_guard.py").read_text(encoding="utf-8")
        m = re.search(r'RULE_REF = \'SKILL\.md, "([^"]+)"\'', guard)
        self.assertTrue(m)
        self.assertIn(m.group(1), read("SKILL.md"))

    def test_workflow_scripts_are_where_skill_md_says(self):
        for name in ("design-skeleton", "design-fanout"):
            self.assertTrue((PROJECT / ".claude" / "workflows" / f"{name}.js").is_file(), name)


if __name__ == "__main__":
    unittest.main()
