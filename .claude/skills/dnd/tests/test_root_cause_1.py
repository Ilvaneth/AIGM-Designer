"""
test_root_cause_1.py — the class invariants of root-cause analysis 1 (docs/reports/root-cause-analysis-1.md).
Each test pins a gate for a class of fault, fed with the shapes that broke it, not one birth's instance.

RC-16  every agent command in the begin JSON is bash-safe: forward slashes, a script that exists
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


if __name__ == "__main__":
    unittest.main()
