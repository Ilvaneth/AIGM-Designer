"""
test_root_cause_1.py — the class invariants of root-cause analysis 1 (docs/reports/root-cause-analysis-1.md).
Each test pins a gate for a class of fault, fed with the shapes that broke it, not one birth's instance.

RC-16  every agent command in the begin JSON is bash-safe: forward slashes, a script that exists
RC-08  a skeleton's graph is seeded by the merge that absorbs it; the seed result is kept on the manifest
RC-02  a roster id the skeleton wrote stays owed to its own writer until that writer's fragment merges
RC-04  approve refuses a stub its phase, or an earlier one, owns and never wrote
"""

import json
import sys
import unittest
from pathlib import Path

from _campaign import TestCampaign, MarkerGuard, SCRIPTS
from test_tuning_birth_1 import fragment, row  # the registry-row and fragment builders, shared

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


class RosterIntent(Base):
    """RC-02: a roster id is done when its own writer's fragment merged, never because of the status a skeleton wrote."""

    STUB, NEW = "site_rcaquenmarsh", "site_rcaoxlight"

    def site(self, eid, name, created_phase="P6", **extra):
        return row(eid, "site", name, created_phase=created_phase, **extra)

    def pending_ids(self) -> set:
        return {e["id"] for e in begin_json(self.c, "P6")["entities"]}

    def test_a_roster_id_the_skeleton_wrote_waits_for_its_own_writer(self):
        # a P1 reservation, as dry-2's premise reserved its two roster sites
        stub = self.site(self.STUB, "Quenmarsh Cellar", created_phase="P1", status="pending", owner_phase="P6",
                         reserved_by="P1.premise.a1")
        self.c.write_json(f"design/_staging/P1/{self.STUB}.json", fragment(self.STUB, stub, phase="P1"))
        self.c.run("registry.py", "merge", "--phase", "P1", check=True)
        self.c.reopen("P6", "running", skeleton={"status": "pending", "agent": None}, roster=[])
        # the skeleton writes both roster sites as skeleton rows, in the two shapes the births used:
        # dry-2's overlay status on the filled stub, dry-1's row status on a new id
        self.c.write_json(f"design/_staging/P6/{self.STUB}.json", fragment(
            self.STUB, self.site(self.STUB, "Quenmarsh Cellar", created_phase="P1"), phase="P6",
            agent="P6.skeleton.a1", overlay={"status": "skeleton"}))
        self.c.write_json(f"design/_staging/P6/{self.NEW}.json", fragment(
            self.NEW, self.site(self.NEW, "Oxlight Barrow", status="skeleton"), phase="P6", agent="P6.skeleton.a1"))
        self.c.write_json("design/_staging/P6/skeleton.json", {
            "phase": "P6", "status": "staged", "roster": [self.STUB, self.NEW],
            "assignments": {"site.1": self.STUB, "site.2": self.NEW}, "reads": {}, "fragments": []})
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.assertEqual(self.pending_ids(), {self.STUB, self.NEW}, "both roster sites are owed to their writers")
        # the writer of one site returns; only the other stays owed, and approve refuses the incomplete roster
        self.c.write_json(f"design/_staging/P6/{self.STUB}.json", fragment(
            self.STUB, self.site(self.STUB, "Quenmarsh Cellar", created_phase="P1"), phase="P6",
            agent=f"P6.{self.STUB}.a1", overlay={"status": "detailed"}))
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.assertEqual(self.pending_ids(), {self.NEW})
        refused = self.c.run("designer.py", "phase", "P6", "approve", "--onay")
        self.assertEqual(refused.returncode, 1)
        self.assertIn(self.NEW, refused.stderr)
        self.assertIn("not complete", refused.stderr)


class OrphanStubs(Base):
    """RC-04: a stub its owner phase never rostered is refused at that phase's approve, not left behind."""

    def reserve(self, eid, name, owner):
        stub = row(eid, "npc", name, created_phase="P3", status="pending", owner_phase=owner, reserved_by="P3.region_x.a1")
        self.c.write_json(f"design/_staging/P3/{eid}.json", fragment(eid, stub, phase="P3"))
        self.c.run("registry.py", "merge", "--phase", "P3", check=True)

    def test_approve_refuses_a_stub_owned_by_this_or_an_earlier_phase(self):
        self.reserve("npc_rcaorphan", "Tessaly Brune", "P5")
        self.reserve("npc_rcalater", "Odrin Vask", "P7")
        self.c.reopen("P6", "validated")
        refused = self.c.run("designer.py", "phase", "P6", "approve", "--onay")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("npc_rcaorphan", refused.stderr, "owned by P5, never written")
        self.assertNotIn("npc_rcalater", refused.stderr, "P7 owns it; P6 does not answer for it")
        self.c.run("designer.py", "phase", "P6", "approve", "--onay", "--force", check=True)


if __name__ == "__main__":
    unittest.main()
