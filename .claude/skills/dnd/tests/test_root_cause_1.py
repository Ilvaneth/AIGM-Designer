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
RC-13  person and god names are rolled from the campaign's languages, spread, listed in every prompt and taken from
       the pool at the door; a secret entity never takes a pool name
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
        self.assertIn("Unwritten minor stubs:** place ×1", card)
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
        self.assertIn("phase critic fix → pass", card)
        self.assertNotIn("A critic did not pass:** phase critic", card)


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
        self.assertIn("⛔ **Gate closed:** a critic did not run", card)

    def test_a_failed_seed_call_closes_the_gate(self):
        self.c.reopen("P6", "validated", seed={"made": 3, "skipped": 0, "failed": 2, "unsupported": 0})
        refused = self.approve("P6")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("seed: 2 seed call(s) failed", refused.stderr)

    def test_a_validator_error_on_the_phases_own_entity_closes_the_gate(self):
        # the door now refuses a dangling ref (RefsAtTheDoor); the row is written past it to probe the gate's reading
        bad = row("npc_rcadangle", "npc", "Merrow Tallis", created_phase="P6", refs=["npc_rcanobody"])
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["npc_rcadangle"] = bad
        self.c.write_json("design/dm-only/entities.json", canon)
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

    def test_the_door_refuses_an_npc_reservation_past_the_budget_before_p5(self):
        room = 15 - self.count("npc")          # short: named_npcs 14-18 less p5_room 3 (dry-3: P5 had no room left)
        proc = self.reserve("npc", room + 1, "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn(f"npc_rcabudget{room:02d}: 1 new npc row(s) would pass the npc budget before P5 (15:", proc.stderr)
        self.assertEqual(self.count("npc"), 15, "every reservation inside the budget merged")

    def test_the_p5_roll_nets_out_the_reserved_npcs(self):
        self.reserve("npc", 14 - self.count("npc"), "P5").check_returncode()
        self.c.reopen("P5", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P5", "--attempt", "9", check=True)
        r = self.rolls("P5")
        total = r["npcs_count"]["value"]
        self.assertGreaterEqual(total, 14, "the total never drops below what the registry holds")
        self.assertEqual(r["npcs_new_count"]["value"], total - 14)
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


class Names(Base):
    """RC-13: person and god names are rolled from the campaign's languages, spread, and taken from the pool at the door."""

    # dry-2's lampcourt, the bank that gave ten of twenty-two names an -an ending
    LAMPCOURT = {"onsets": ["c", "v", "l", "aur", "ott", "ser", ""], "nuclei": ["a", "e", "i", "o"],
                 "codas": ["n", "r", "l", "us", "ia", "an", ""], "length": [3, 3], "forbidden_clusters": ["uu", "ii", "cc", "rl"]}

    def test_a_narrow_bank_still_gives_spread_names_the_door_accepts(self):
        import random
        from collections import Counter
        import design_names as dn
        import registry
        names = dn.draw_names(random.Random("rca-names"), self.LAMPCOURT, 24, [])
        self.assertEqual(len(names), 24)
        self.assertLessEqual(max(Counter(n[-2:] for n in names).values()), 3, "no ending carries the campaign")
        self.assertGreaterEqual(min(dn.distance(a, b) for i, a in enumerate(names) for b in names[i + 1:]), 3)
        for n in names:
            self.assertEqual(registry.naming_errors("probe", {"type": "npc", "name": n}, registry.naming_blacklist(), set()), [], n)
            self.assertNotRegex(n.lower(), r"[aeiouy]{3}")
            self.assertGreaterEqual(len(n), 4, "dry-3: Sta, Ord, Ske")
        self.assertFalse([(a, b) for a in names for b in names if a != b and b.lower().startswith(a.lower())],
                         "no name is the head of another (dry-3: Ske, Skeik)")

    def test_a_one_syllable_bank_still_gives_two_syllables_and_turkish_words_are_refused(self):
        import random
        import design_names as dn
        import registry
        short = {"onsets": ["sk", "st", "", "d"], "nuclei": ["a", "e", "o"], "codas": ["", "rd", "k"], "length": [1, 2]}
        for n in dn.draw_names(random.Random("rca-short"), short, 12, []):
            self.assertGreaterEqual(len(n), 4, n)
        self.assertTrue(registry.naming_errors("god_x", {"type": "god", "name": "Sivil"}, registry.naming_blacklist(), set()),
                        "dry-3's god Sivil is a Turkish word")

    def pool(self):
        self.c.reopen("P2", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P2", "--attempt", "9", check=True)
        return self.c.json("design/dm-only/name-pool.json")

    def test_the_pool_is_rolled_at_preroll_and_every_prompt_lists_it_rotated(self):
        import design_prompts as dp
        pool = self.pool()
        langs = set(self.c.json("design/naming.json")["languages"])
        self.assertEqual(set(pool["languages"]), langs)
        self.assertTrue(all(len(L["person"]) >= 18 for L in pool["languages"].values()), "the band's top and a margin")
        one = dp.render(self.c.name, "P5.npc", "npc_draskun")
        two = dp.render(self.c.name, "P5.npc", "npc_kortan")
        self.assertIn("Names (rolled, never invented)", one)
        line = lambda t: next(x for x in t.splitlines() if x.startswith("- ") and " persons: " in x)
        self.assertNotEqual(line(one), line(two), "parallel writers start their lists apart")

    def test_the_door_takes_a_public_persons_name_from_the_pool_once(self):
        pool = self.pool()
        lang = sorted(pool["languages"])[0]
        first = pool["languages"][lang]["person"][0]["name"]
        self.c.reopen("P5", "running")
        invented = row("npc_rcainvented", "npc", "Quintarro Vale", created_phase="P5", lang=lang)
        self.c.write_json("design/_staging/P5/npc_rcainvented.json", fragment("npc_rcainvented", invented))
        refused = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertIn("is not on the rolled person list", refused.stderr)
        rolled = row("npc_rcarolled", "npc", f"{first} Lampwright", created_phase="P5", lang=lang)
        self.c.write_json("design/_staging/P5/npc_rcarolled.json", fragment("npc_rcarolled", rolled))
        self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertIn("npc_rcarolled", self.c.json("design/dm-only/entities.json")["entities"])
        used = {e["name"]: e["used_by"] for e in self.c.json("design/dm-only/name-pool.json")["languages"][lang]["person"]}
        self.assertEqual(used[first], "npc_rcarolled")
        secret = row("npc_s77", "npc", first, created_phase="P5", secrecy="secret", lang=lang)
        self.c.write_json("design/_staging/P5/npc_s77.json", fragment("npc_s77", secret))
        refused = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertIn("a secret entity may not take a pool name", refused.stderr)

    def test_the_courtly_bag_carries_no_banned_opening_and_no_family_is_mutated(self):
        """In the part-bag shape (build item 11a): no opening of any bag starts the owner's banned stems, and no
        family row tells the writer to mutate it (decision 16; dry-2's fixed length came from a mutation hook)."""
        import design_tables as dt
        fams = dt.rows("naming.yaml#family")
        courtly = next(r for r in fams if r["id"] == "family_courtly")
        for stem in ("cass", "corv", "corw", "corr"):
            self.assertFalse([o for r in fams for o in r["openings"] if o.lower().startswith(stem)], f"{stem}- is the owner's banned stem")
        self.assertNotIn("Cass", courtly["openings"])
        self.assertFalse(any("hooks" in r or "length" in r for r in fams))


class ExitNotes(unittest.TestCase):
    """The first live stop (dry-3 P6): a comma inside an exit's parenthesised note made its distance a room number."""

    def test_a_parenthesised_note_in_the_exits_cell_is_never_an_exit(self):
        import design_check
        text = ("| 4 | Gedik Ağzı | combat | içerik | 2 (çöken gövdeden ateşe, 30 ft), 3 (ip merdiven, sur yolu), "
                "5 (sekiye yarım kat iniş), 7 (merdiven başı) | 100 |\n"
                "| 1 | Son Mil Taşı [Entrance] | structural | içerik | 2 (patika; 300 ft yokuş) | 0 |\n")
        rooms = {r["id"]: r["exits"] for r in design_check.parse_rooms(text)}
        self.assertEqual(rooms["4"], ["2", "3", "5", "7"])
        self.assertEqual(rooms["1"], ["2"])


class Refusals(Base):
    """dry-3's second stop: a refused re-emission flipped back to merged and a writerless unit's refusal was listed nowhere."""

    def node(self, eid, chapter, agent):
        r = row(eid, "node", "The Quill Hearing" if eid.endswith("one") else "The Salt Vote", created_phase="P7",
                chapter=chapter, stamped={"chapter": chapter})
        self.c.write_json(f"design/_staging/P7/{eid}.json", fragment(eid, r, phase="P7", agent=agent))
        return self.c.run("registry.py", "merge", "--phase", "P7")

    def test_a_refused_node_goes_back_to_the_chapter_writer_that_emitted_it_and_stays_failed(self):
        self.c.reopen("P7", "running", roster=["chapter_1"], skeleton={"status": "merged", "agent": "P7.skeleton.a1"})
        self.node("node_rcaone", "chapter_1", "P7.skeleton.a1").check_returncode()
        self.c.write_json("design/_staging/P7/node_rcaone.json", fragment(
            "node_rcaone", row("node_rcaone", "node", "The Quill Hearing", created_phase="P7", chapter="chapter_2",
                               stamped={"chapter": "chapter_2"}), phase="P7", agent="P7.chapter_1.a1"))
        self.assertEqual(self.c.run("designer.py", "phase", "P7", "merge").returncode, 1)
        m = self.c.json("design/design.json")
        self.assertEqual(m["entities"]["chapter_1"]["status"], "failed", "the writer that emitted the node answers for it")
        self.assertIn("node_rcaone: ", m["entities"]["chapter_1"]["last_error"])
        self.assertNotIn("node_rcaone", m["phases"]["P7"]["roster"], "a node has no writer of its own to rerun")
        listed = {e["id"]: e for e in begin_json(self.c, "P7")["entities"]}
        self.assertIn("chapter_1", listed, "begin re-lists the refused writer instead of an empty list")
        self.assertIn("prompt_cmd", listed["chapter_1"])
        self.assertEqual(self.c.json("design/design.json")["entities"]["chapter_1"]["status"], "failed",
                         "reconcile keeps the refusal until a newer fragment replaces the old one")

    def test_link_syntax_in_a_stamp_is_not_drift(self):
        self.c.reopen("P7", "running")
        self.node("node_rcatwo", "chapter_1", "P7.skeleton.a1").check_returncode()
        self.node("node_rcatwo", "[[chapter_1]]", "P7.chapter_1.a1").check_returncode()

    def test_the_arc_template_links_no_id_that_cannot_exist(self):
        text = (SCRIPTS.parent / "templates" / "design" / "arc.md").read_text(encoding="utf-8")
        self.assertNotIn("thread_premise", text, "dry-3's skeleton copied it; threads are per PC and born in P9")
        self.assertIn("[[premise_<slug>]]", text)


class P8Render(Base):
    """dry-3's P8 stop: the approval snapshots made every public sentence a 'dm-only sentence', the primer was refused,
    and the gate, reading no render result, let P8 through with no primer and no DM files."""

    def test_an_approval_snapshot_is_not_the_secret_corpus(self):
        import re
        import design_approval as da
        text = self.c.path("design/sites/site_sunken_pier.md").read_text(encoding="utf-8")
        public = next(s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if len(s.strip()) >= 60 and not s.startswith(("|", "#", "-")))
        self.c.reopen("P5", "validated")
        self.c.run("designer.py", "phase", "P5", "approve", "--onay", check=True)
        self.assertTrue(self.c.path("design/dm-only/_snapshots/approved/P5/design/sites/site_sunken_pier.md").is_file())
        _, sentences = da.secret_terms(self.c.name)
        self.assertNotIn(public, sentences, "a public sentence copied into a snapshot is still public")

    def test_a_failed_p8_render_closes_the_gate(self):
        self.c.reopen("P8", "validated", render={"failed": "primer", "at": "2026-09-27T00:00:00Z"})
        refused = self.c.run("designer.py", "phase", "P8", "approve", "--onay")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("render: the player's files did not render (primer)", refused.stderr)


class UsedRows(Base):
    """dry-3: design_compare read NOT DISTINCT; no birth ever wrote the rows it used to used.json."""

    def setUp(self):
        super().setUp()
        import tempfile
        import design_dice as dd
        self.dd = dd
        self.tmp = Path(tempfile.mkdtemp()) / "used.json"
        self.real_path = dd.used_path
        dd.used_path = lambda: self.tmp

    def tearDown(self):
        self.dd.used_path = self.real_path
        super().tearDown()

    def test_an_approved_phase_records_its_avoid_used_rows_and_hides_the_secret_ones(self):
        import designer
        import design_tables as dt
        secrets = dt.load("secrets.yaml")["tables"]
        sub = next(k for k, v in secrets.items() if isinstance(v, dict) and v.get("rows"))
        secret_ref, secret_row = f"secrets.yaml#{sub}", secrets[sub]["rows"][0]["id"]
        m = self.c.json("design/design.json")
        self.assertEqual(designer.record_used(self.c.name, "P2"), 0, "the micro fixture records nothing")
        m["_meta"]["fixture"] = False
        m["dice_log"].append({"phase": "P2", "table": "pantheon.yaml#presence", "label": "presence", "row_id": "presence_walking"})
        self.c.write_json("design/design.json", m)
        log = self.c.json("design/dm-only/dice-log.json") if self.c.path("design/dm-only/dice-log.json").is_file() else {"rolls": []}
        log["rolls"].append({"phase": "P2", "table": secret_ref, "label": "secret.kind", "row_id": secret_row})
        self.c.write_json("design/dm-only/dice-log.json", log)
        self.assertGreaterEqual(designer.record_used(self.c.name, "P2"), 2, "the fixture's own P2 rolls come along")
        mine = json.loads(self.tmp.read_text(encoding="utf-8"))["campaigns"][self.c.name]
        self.assertIn("presence_walking", mine["pantheon.yaml#presence"])
        self.assertNotIn(secret_row, json.dumps(mine), "the secret row id never reaches used.json in clear")
        self.assertTrue(mine[secret_ref][0].startswith("h:"), "a secret row is kept as a hash")
        self.assertIn("presence_walking", self.dd.rows_used_elsewhere("_test-next", "pantheon.yaml#presence"))
        self.assertIn(secret_row, self.dd.rows_used_elsewhere("_test-next", secret_ref), "the hash still excludes the row")
        self.assertEqual(self.dd.rows_used_elsewhere("real-campaign", "pantheon.yaml#presence"), set(),
                         "a real campaign is never narrowed by a test birth")


class RefsAtTheDoor(Base):
    """dry-3 P7 attempt 2: a ref to an id nothing answers is refused at the unit, not found by the validator later."""

    def test_a_ref_nothing_answers_is_refused_and_a_known_one_passes(self):
        self.c.reopen("P7", "running")
        bad = row("node_rcaref", "node", "The Ledger Hearing", created_phase="P7", refs=["calculus_act_1", "[[chapter_1]]"])
        self.c.write_json("design/_staging/P7/node_rcaref.json", fragment("node_rcaref", bad, phase="P7"))
        refused = self.c.run("registry.py", "merge", "--phase", "P7")
        self.assertIn("refs name calculus_act_1, which no registry row answers", refused.stderr)
        good = row("node_rcaref", "node", "The Ledger Hearing", created_phase="P7", refs=["[[chapter_1]]", "node_rcaother"])
        other = row("node_rcaother", "node", "The Salt Hearing", created_phase="P7")
        self.c.write_json("design/_staging/P7/node_rcaref.json", fragment("node_rcaref", good, phase="P7"))
        self.c.write_json("design/_staging/P7/node_rcaother.json", fragment("node_rcaother", other, phase="P7"))
        self.c.run("registry.py", "merge", "--phase", "P7").check_returncode()


class CriticLoopPath(Base):
    """dry-3: P1's premise showed c1:pass → c1:pass for fix → pass; the loop critic saved to the path its prompt named."""

    def test_a_loop_critic_prompt_names_its_own_save_path_and_the_workflows_pass_the_loop(self):
        import design_prompts as dp
        first = dp.render(self.c.name, "critic", "site_sunken_pier", phase_override="P6")
        second = dp.render(self.c.name, "critic", "site_sunken_pier", phase_override="P6", loop=2)
        self.assertIn("site_sunken_pier.critic1.json", first)
        self.assertIn("site_sunken_pier.critic1.loop2.json", second)
        self.assertNotIn("site_sunken_pier.critic1.json`", second)
        for wf in ("design-fanout.js", "design-skeleton.js"):
            js = (SCRIPTS.parents[3] / ".claude" / "workflows" / wf).read_text(encoding="utf-8")
            self.assertIn("(loop > 1 ? ' --loop ' + loop : '')", js, wf)


class Dry3Small(Base):
    """dry-3's small findings: the rerun reason, raw links on the card, the day-0 news twice."""

    def test_a_rerun_reason_is_recorded_not_handed_to_the_writers(self):
        before = list(self.c.json("design/design.json")["phases"]["P6"].get("directions") or [])
        self.c.run("designer.py", "phase", "P6", "rerun", "--reason", "STOP P6: pipeline fix abc123", check=True)
        ph = self.c.json("design/design.json")["phases"]["P6"]
        self.assertEqual(ph.get("directions") or [], before, "a pipeline reason is no creative direction")
        self.assertEqual(ph["reruns"][-1]["reason"], "STOP P6: pipeline fix abc123")
        self.c.run("designer.py", "phase", "P6", "rerun", "--reason", "owner", "--direction", "Daha az deniz.", check=True)
        self.assertIn("Daha az deniz.", self.c.json("design/design.json")["phases"]["P6"]["directions"])

    def test_the_card_reads_links_as_public_names(self):
        import design_approval as da
        proj = {"settlement_greyreach": {"name": "Greyreach", "secrecy": "public"}, "npc_s01": {"name": "x", "secrecy": "secret"}}
        self.assertEqual(da.readable("[[settlement_greyreach]]'da biri [[npc_s01]] ve [[npc_nobody]] arar", proj),
                         "Greyreach'da biri … ve … arar")

    def test_the_day_0_news_is_written_once(self):
        self.c.write_json("design/_staging/P8/primer_rca.news.json",
                          {"records": [{"visibility": "public", "line_tr": "Liman kapısı bu sabah kapandı.", "refs": []}]})
        for _ in range(2):
            self.c.run("render_player.py", "news", "--day", "0", check=True)
        lines = [r["line_tr"] for r in self.c.json("design/news.json")["records"] if r.get("day") == 0]
        self.assertEqual(lines.count("Liman kapısı bu sabah kapandı."), 1)


class RealCost(Base):
    """RC-09: the Workflow figure is summed peak context; the run's transcripts say the real cost, per role."""

    def run_dir(self):
        import tempfile
        d = Path(tempfile.mkdtemp()) / "wf_rca-cost"
        d.mkdir()
        def agent(name, label, usages):
            (d / f"agent-{name}.meta.json").write_text(json.dumps({"description": label}), encoding="utf-8")
            with (d / f"agent-{name}.jsonl").open("w", encoding="utf-8") as fh:
                for rid, (o, cr) in usages:
                    rec = {"type": "assistant", "requestId": rid, "message": {"usage": {"output_tokens": o, "input_tokens": 2,
                           "cache_creation_input_tokens": 10, "cache_read_input_tokens": cr}}}
                    fh.write(json.dumps(rec) + "\n")
                    fh.write(json.dumps(rec) + "\n")           # a request with a text and a tool block: stored twice
        agent("a", "P6.site_x.a1", [("r1", (100, 1000)), ("r2", (50, 2000))])
        agent("b", "P6.site_x.critic1.loop2", [("r3", (20, 500))])
        agent("c", "P6.phase_critic", [("r4", (30, 800))])
        return d

    def test_merge_records_the_runs_real_cost_per_role_and_the_card_shows_it(self):
        self.c.reopen("P6", "running")
        self.c.run("designer.py", "phase", "P6", "merge", "--run-dir", str(self.run_dir()), check=True)
        cost = self.c.json("design/design.json")["phases"]["P6"]["cost"]
        self.assertEqual(cost["totals"]["output"], 200, "each request counted once")
        self.assertEqual(cost["totals"]["requests"], 4)
        by_role = cost["runs"]["wf_rca-cost"]["by_role"]
        self.assertEqual(set(by_role), {"writer", "critic", "phase_critic"})
        self.c.run("designer.py", "phase", "P6", "card", check=True)
        card = self.c.path("design/_approval/P6.card.md").read_text(encoding="utf-8")
        self.assertIn("**Real output:** 200", card)
        self.assertIn("**Context (Workflow):**", card)

    def test_a_run_no_merge_recorded_reaches_the_ledger(self):
        """Build item 18f (test birth P1-1, #2): a Workflow that returned failed is not merged; `design_cost.py record`
        puts its cost on the phase's ledger, marked not merged, and the report counts it apart."""
        self.c.reopen("P6", "running")
        self.c.run("design_cost.py", "record", "--phase", "P6", "--run-dir", str(self.run_dir()), check=True)
        cost = self.c.json("design/design.json")["phases"]["P6"]["cost"]
        self.assertEqual((cost["totals"]["output"], cost["runs"]["wf_rca-cost"]["merged"]), (200, False))
        out = self.c.run("designer.py", "phase", "P6", "report", check=True).stdout
        self.assertIn("(1 run(s), 1 not merged)", out)


class PhaseReport(Base):
    """The review stop: `phase PN report` prints what the owner and the development tab judge before approve."""

    def test_the_report_prints_the_gate_the_critics_the_band_and_the_card(self):
        self.c.reopen("P6", "validated", roster=["site_sunken_pier"])
        out = self.c.run("designer.py", "phase", "P6", "report", check=True).stdout
        for part in ("PHASE REPORT", "- status: validated · gate: closed — critic_missing", "- roster: 1",
                     "- band:", "- cost: no run recorded", "- card: design/_approval/P6.card.md"):
            self.assertIn(part, out)


class P5AfterDry3(Base):
    """dry-3's P5: the card listed 7 NPCs of 17, and a critic that read a mirror wrote its reasoning to public staging."""

    def test_the_card_lists_every_row_the_phase_merged_batch_members_included(self):
        stub = row("npc_rcaminor", "npc", "Tobin Quarrel", created_phase="P3", status="pending", owner_phase="P5", reserved_by="P3.region_x.a1")
        self.c.write_json("design/_staging/P3/npc_rcaminor.json", fragment("npc_rcaminor", stub, phase="P3"))
        self.c.run("registry.py", "merge", "--phase", "P3", check=True)
        self.c.reopen("P5", "running", roster=["npcbatch_9"])
        filled = row("npc_rcaminor", "npc", "Tobin Quarrel", created_phase="P3", tier="minor")
        self.c.write_json("design/_staging/P5/npcbatch_9.json", fragment("npcbatch_9", None, phase="P5", rows=[filled]))
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.c.run("designer.py", "phase", "P5", "card", check=True)
        card = self.c.path("design/_approval/P5.card.md").read_text(encoding="utf-8")
        self.assertIn("| npc_rcaminor | Tobin Quarrel |", card, "a P3 stub filled inside a P5 batch is P5's")

    def test_a_mirrored_entitys_critique_notes_are_named_in_dm_only(self):
        import design_prompts as dp
        text = dp.render(self.c.name, "critic", "npc_draskun", phase_override="P5")
        mirror = self.c.path("design/dm-only/npcs/npc_draskun.md").is_file()
        self.assertIn("design/dm-only/_staging/P5/npc_draskun.critique.md" if mirror else "design/_staging/P5/npc_draskun.critique.md", text)
        self.assertTrue(mirror, "the fixture's npc_draskun has a secret layer")


class VoiceRegisters(Base):
    """Every birth's P5 phase critic flagged shared registers; the register is rolled, one per NPC while rows last."""

    def test_p5_rolls_a_distinct_register_for_every_npc_and_the_writer_is_told(self):
        import design_prompts as dp
        import design_tables as dt
        rows = dt.rows("npcs.yaml#voice_register")
        self.assertGreaterEqual(len(rows), 16)
        self.assertTrue(all(r.get("sound") and r.get("words") and r.get("never") for r in rows))
        self.c.reopen("P5", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P5", "--attempt", "9", check=True)
        regs = [r["row_id"] for r in self.c.json("design/design.json")["dice_log"]
                if r.get("phase") == "P5" and r.get("attempt") == 9 and r["label"].endswith(".register")]
        self.assertGreaterEqual(len(regs), 14, "one per NPC ordinal")
        first = regs[:len(rows)]
        self.assertEqual(len(first), len(set(first)), "no register twice while the table has unused rows")
        self.assertIn("npc.<n>.register", dp.load("P5.npc")[1])


class Anchors(Base):
    """dry-4's P1 review: four births built on candles, hush and the dead, from the naming table's own examples."""

    RECURRING = ("lantern", "lamp", "candle", "hush", "still", "mourn", "bell", "tallow", "wick", "salt", "ash", "warden", "tribunal")

    def test_no_example_an_agent_reads_carries_the_recurring_words(self):
        import design_tables as dt
        nm = dt.load("naming.yaml")
        shown = [s for s in nm["rules"]["modes"].values()]
        shown += [x for rows in nm["patterns"].values() for r in rows for x in r.get("examples", [])]
        import yaml
        play = yaml.safe_load((SCRIPTS.parent / "data" / "play" / "turkish-suffixing.yaml").read_text(encoding="utf-8"))
        shown += [r["example"] for r in play["turkish_suffixing"]["ending_table"]]
        low = " ".join(str(s).lower() for s in shown)
        self.assertFalse([w for w in self.RECURRING if w in low], "examples show a shape, not a campaign's words")
        common = (SCRIPTS.parent / "prompts" / "design" / "_common.md").read_text(encoding="utf-8")
        self.assertNotIn("Lanternside", common)

    def test_the_p1_prompt_lists_the_earlier_campaigns_to_avoid(self):
        import design_prompts as dp
        other = TestCampaign("rca1other")
        try:
            text = dp.render(self.c.name, "P1.premise")
            self.assertIn("### Earlier campaigns — never echo them", text)
            self.assertIn(f"({other.name})", text)
            self.assertNotIn(f"({self.c.name})", text, "a campaign never lists itself")
            self.assertNotIn("Earlier campaigns", dp.render(self.c.name, "P3.skeleton"), "P1 only")
        finally:
            other.remove()


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
