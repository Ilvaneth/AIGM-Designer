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
RC-14  an approval snapshots the disk-is-truth stores; rerun restores the last approval's before the phase
RC-03  before P5 (npc) and P7 (seed) the registry stops at the band's top; the count rolls net out the reservations
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

    def test_a_minor_type_orphan_is_a_card_warning_not_a_refusal(self):
        stub = row("place_rcaquay", "place", "Tallow Quay", created_phase="P3", status="pending", owner_phase="P5",
                   reserved_by="P3.settlement_x.a1")
        self.c.write_json("design/_staging/P3/place_rcaquay.json", fragment("place_rcaquay", stub, phase="P3"))
        self.c.run("registry.py", "merge", "--phase", "P3", check=True)
        self.c.reopen("P6", "validated")
        self.c.run("designer.py", "phase", "P6", "card", check=True)
        card = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("Yazılmamış küçük taslak:** place ×1", card)
        self.c.run("designer.py", "phase", "P6", "approve", "--onay", check=True)

    def test_the_blocking_stub_types_are_the_registrys_prose_types(self):
        import design_manifest as dm
        import registry
        self.assertEqual(set(dm.BLOCKING_STUB_TYPES), set(registry.PROSE_TYPES))


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


class Budgets(Base):
    """RC-03: before its owning phase a type's rows stop at the band's top, and the count roll nets out what is reserved."""

    FIRST = ["Brannoc", "Dellis", "Fenwyr", "Gorrit", "Halvek", "Jossam", "Kelmar", "Lusken", "Merrit", "Norrab", "Pellin"]

    def count(self, etype):
        return sum(1 for e in self.c.json("design/dm-only/entities.json")["entities"].values() if e.get("type") == etype)

    def reserve(self, etype, n, owner):
        for i in range(n):
            eid = f"{etype}_rcabudget{i:02d}"
            name = f"{self.FIRST[i]} Quill" if etype == "npc" else f"The {self.FIRST[i]} Debt"
            stub = row(eid, etype, name, created_phase="P3", status="pending", owner_phase=owner, reserved_by="P3.region_x.a1")
            self.c.write_json(f"design/_staging/P3/{eid}.json", fragment(eid, stub, phase="P3"))
        return self.c.run("registry.py", "merge", "--phase", "P3")

    def rolls(self, phase):
        return {r["label"]: r for r in self.c.json("design/design.json")["dice_log"]
                if r.get("phase") == phase and r.get("attempt") == 9}

    def test_the_door_refuses_an_npc_reservation_past_the_band_top_before_p5(self):
        room = 18 - self.count("npc")                          # short: named_npcs 14-18
        proc = self.reserve("npc", room + 1, "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"npc_rcabudget{room:02d}: 1 new npc row(s) would pass the scale's band top (18) before P5", proc.stderr)
        self.assertEqual(self.count("npc"), 18, "every reservation inside the band merged")

    def test_the_p5_roll_nets_out_the_reserved_npcs(self):
        self.reserve("npc", 17 - self.count("npc"), "P5").check_returncode()
        self.c.reopen("P5", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P5", "--attempt", "9", check=True)
        r = self.rolls("P5")
        total = r["npcs_count"]["value"]
        self.assertGreaterEqual(total, 17, "the total never drops below what the registry holds")
        self.assertEqual(r["npcs_new_count"]["value"], total - 17)
        self.assertEqual(sum(1 for k in r if k.endswith(".tic")), total, "one ordinal per NPC, stubs included")

    def test_the_p7_roll_counts_the_seed_stubs_an_earlier_phase_reserved(self):
        filled = self.count("seed")
        self.reserve("seed", 4, "P7").check_returncode()
        self.c.reopen("P7", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P7", "--attempt", "9", check=True)
        r = self.rolls("P7")
        total = r["seeds_count"]["value"]
        self.assertGreaterEqual(total, filled + 4)
        self.assertEqual(r["seeds_new_count"]["value"], total - filled - 4)
        shapes = [k for k in r if k.startswith("seed.")]
        self.assertEqual(len(shapes), 4 + total - filled - 4, "a shape for every stub to fill and every new seed")


class RerunRollback(Base):
    """RC-14: an approval snapshots the disk-is-truth stores; rerun puts back the last approval's before the phase."""

    def test_rerun_restores_the_registry_and_the_stores_of_the_previous_approval(self):
        self.c.reopen("P5", "validated")
        self.c.run("designer.py", "phase", "P5", "approve", "--onay", check=True)
        self.assertTrue(self.c.path("design/dm-only/_snapshots/approved/P5/design/dm-only/entities.json").is_file())
        graph_before = self.c.path("graph.json").read_text(encoding="utf-8")
        # P6 merges a row and seeds its node, then is rerun
        self.c.reopen("P6", "running")
        probe = row("npc_rcarerun", "npc", "Hadric Vane", created_phase="P6")
        self.c.write_json("design/_staging/P6/npc_rcarerun.json", fragment(
            "npc_rcarerun", probe, phase="P6",
            graph={"nodes": [{"id": "npc_rcarerun", "type": "npc", "name": "Hadric Vane"}], "edges": []}))
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        self.assertIn("npc_rcarerun", self.c.json("design/dm-only/entities.json")["entities"])
        self.assertNotEqual(self.c.path("graph.json").read_text(encoding="utf-8"), graph_before)
        proc = self.c.run("designer.py", "phase", "P6", "rerun", "--reason", "rca probe", check=True)
        self.assertIn("restored the stores of P5's approval", proc.stdout)
        self.assertNotIn("npc_rcarerun", self.c.json("design/dm-only/entities.json")["entities"])
        self.assertNotIn("npc_rcarerun", self.c.json("design/entities.json")["entities"])
        self.assertEqual(self.c.path("graph.json").read_text(encoding="utf-8"), graph_before)
        self.assertNotIn("graph:node:npc_rcarerun", self.c.json("design/design.json").get("seeded", []),
                         "the ledger is restored too, so the rerun can seed again")


if __name__ == "__main__":
    unittest.main()
