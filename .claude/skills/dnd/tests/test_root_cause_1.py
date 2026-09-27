"""
test_root_cause_1.py — the class invariants of root-cause analysis 1 (docs/reports/root-cause-analysis-1.md).
Each test pins a gate for a class of fault, fed with the shapes that broke it, not one birth's instance.

RC-16  every agent command in the begin JSON is bash-safe: forward slashes, a script that exists
RC-08  a skeleton's graph is seeded by the merge that absorbs it; the seed result is kept on the manifest
"""

import json
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))


def begin_json(c: TestCampaign, phase: str) -> dict:
    proc = c.run("designer.py", "phase", phase, "begin", "--json", check=True)
    return json.loads(proc.stdout[proc.stdout.index("{"):])


def commands(obj) -> list[str]:
    """Every value under a key ending in `_cmd`, at any depth."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.endswith("_cmd") and isinstance(v, str):
                out.append(v)
            else:
                out += commands(v)
    elif isinstance(obj, list):
        for v in obj:
            out += commands(v)
    return out


class Base(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("rca1")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)


class AgentCommands(Base):
    """RC-16: the workflows paste `prompt_cmd` into an agent's bash verbatim."""

    def test_every_agent_command_in_the_begin_json_is_bash_safe(self):
        self.c.reopen("P6", "prerolled", skeleton={"status": "pending", "agent": None})
        cmds = commands(begin_json(self.c, "P6"))
        self.assertGreaterEqual(len(cmds), 3, "skeleton, its critic, the phase and wishes critics")
        for cmd in cmds:
            self.assertNotIn("\\", cmd, cmd)
            script = cmd.split()[3]
            self.assertTrue(Path(script).is_file(), f"{script} does not resolve")


class Seeding(Base):
    """RC-08: design_seed reads merged/ only; the skeleton's graph must enter the ledger at the merge that absorbs it."""

    def test_the_skeleton_graph_is_seeded_by_the_merge_that_absorbs_it(self):
        self.c.reopen("P6", "running", skeleton={"status": "pending", "agent": None}, roster=[])
        self.c.write_json("design/_staging/P6/skeleton.json", {
            "phase": "P6", "status": "staged", "roster": [], "assignments": {}, "reads": {}, "fragments": [],
            "graph": {"nodes": [{"id": "site_rcaprobe", "type": "site", "name": "Quenmarsh Cellar"}], "edges": []}})
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        nodes = [n.get("id") for n in self.c.json("graph.json").get("nodes", [])]
        self.assertIn("site_rcaprobe", nodes, "seeded by the same merge, not the next one")
        seed = self.c.json("design/design.json")["phases"]["P6"]["seed"]
        self.assertGreaterEqual(seed["made"], 1)
        self.assertEqual(seed["failed"], 0, "the seed result is on the manifest for the approve gate")


if __name__ == "__main__":
    unittest.main()
