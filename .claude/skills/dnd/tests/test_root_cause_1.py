"""
test_root_cause_1.py — the class invariants of root-cause analysis 1 (docs/reports/root-cause-analysis-1.md).
Each test pins a gate for a class of fault, fed with the shapes that broke it, not one birth's instance.

RC-16  every agent command in the begin JSON is bash-safe: forward slashes, a script that exists
RC-08  a skeleton's graph is seeded by the merge that absorbs it; the seed result is kept on the manifest
RC-02  a roster id the skeleton wrote stays owed to its own writer until that writer's fragment merges
RC-04  approve refuses a stub its phase, or an earlier one, owns and never wrote
RC-05  the post-phase-fix critique has a file of its own; the phase critic's second reading is the phase's verdict
RC-01  approve reads the gate (band, missing critics, the phase's own validator errors, seed failures, orphans) in every
       mode; --force passes it with a recorded reason
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


class CritiqueLoop(Base):
    """RC-05: the post-phase-fix critique has a file of its own, and the phase critic judges once more after its fixes."""

    FANOUT = SCRIPTS.parents[3] / ".claude" / "workflows" / "design-fanout.js"

    def test_the_post_phase_fix_critique_never_shares_an_entity_loop_file(self):
        js = self.FANOUT.read_text(encoding="utf-8")
        self.assertIn("const PHASE_FIX_LOOP = MAX_FIX_LOOPS + 2", js)
        self.assertIn("critique(e, 1, PHASE_FIX_LOOP)", js)
        self.assertNotIn("critique(e, 1, 3)", js, "loop 3 is an entity's second re-critique when MAX_FIX_LOOPS is 2")
        self.assertIn("phase.critic1.loop2.json", js, "the phase critic's second reading is saved beside the first")

    def test_the_phase_critic_second_reading_is_the_phase_outcome_on_the_card(self):
        self.c.reopen("P6", "running")
        finding = {"rubric_id": "rubric_p6_only_here", "entity_id": "site_sunken_pier", "verdict": "fix", "reason_code": "generic_rooms"}
        self.c.write_json("design/_staging/P6/phase.critic1.json", {"entity_id": "P6", "verdict": "fix", "findings": [finding]})
        self.c.write_json("design/_staging/P6/phase.critic1.loop2.json",
                          {"entity_id": "P6", "verdict": "pass", "findings": [dict(finding, verdict="pass")]})
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        records = self.c.json("design/design.json")["phases"]["P6"]["critique"]["records"]
        self.assertEqual([(r["kind"], r["verdict"]) for r in records], [("phase", "fix"), ("phase", "pass")])
        self.c.run("designer.py", "phase", "P6", "card", check=True)
        card = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("faz eleştirmeni fix → pass", card)
        self.assertNotIn("Eleştirmen geçmedi:** faz eleştirmeni", card)


class ApproveGate(Base):
    """RC-01: approve reads the facts the card computes, identically in test and real births; --force records why."""

    def approve(self, phase, *extra):
        return self.c.run("designer.py", "phase", phase, "approve", "--onay", *extra)

    def test_a_band_miss_closes_the_gate_and_force_records_the_reason(self):
        m = self.c.json("design/design.json")
        m["_meta"]["fixture"] = False           # a birth, not the micro fixture: the short band applies (npc 14-18)
        self.c.write_json("design/design.json", m)
        self.c.reopen("P5", "validated")
        refused = self.approve("P5")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("gate closed", refused.stderr)
        self.assertIn("npc outside band 14-18", refused.stderr)
        self.approve("P5", "--force", "--reason", "fixture below band").check_returncode()
        forced = self.c.json("design/design.json")["phases"]["P5"]["approval"]["forced"]
        self.assertEqual([g["code"] for g in forced["gate"]], ["band"])
        self.assertEqual(forced["reason"], "fixture below band")

    def test_a_roster_nobody_critiqued_closes_the_gate_and_the_card_says_so(self):
        self.c.reopen("P6", "validated", roster=["site_sunken_pier"])
        refused = self.approve("P6")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("critic_missing: phase critic, wishes critic, 1 roster item(s) never critiqued", refused.stderr)
        self.assertIn("site_sunken_pier", refused.stderr)
        self.c.run("designer.py", "phase", "P6", "card", check=True)
        card = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("⛔ **Kapı kapalı:** eleştirmen çalışmadı", card)

    def test_a_failed_seed_call_closes_the_gate(self):
        self.c.reopen("P6", "validated", seed={"made": 3, "skipped": 0, "failed": 2, "unsupported": 0})
        refused = self.approve("P6")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("seed: 2 seed call(s) failed", refused.stderr)

    def test_a_validator_error_on_the_phases_own_entity_closes_the_gate(self):
        bad = row("npc_rcadangle", "npc", "Merrow Tallis", created_phase="P6", refs=["[[npc_rcanobody]]"])
        self.c.write_json("design/_staging/P6/npc_rcadangle.json", fragment("npc_rcadangle", bad, phase="P6"))
        self.c.run("registry.py", "merge", "--phase", "P6")
        self.c.reopen("P6", "validated")
        check = self.c.run("design_check.py", "--phase", "P6", "--json")
        errors = [f for f in json.loads(check.stdout or "[]") if f.get("severity") == "error" and f.get("entity") == "npc_rcadangle"]
        self.assertTrue(errors, "the probe needs a validator error on the phase's own row")
        refused = self.approve("P6")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("validator: validator errors on", refused.stderr)
        self.assertIn("npc_rcadangle", refused.stderr)


if __name__ == "__main__":
    unittest.main()
