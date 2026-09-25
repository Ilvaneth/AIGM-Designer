"""
test_tuning_birth_1.py — regressions from the first tuning birth (docs/reports/tuning-birth-1.md,
2026-09-25). Each test is named after the report section it closes: the registry accepts container
fragments (documents and batches) and merges per unit, a refused unit never blocks the others and comes
back as `failed` with its reason on the next `begin --json`; a stub row is filled without stamp drift
and never counts as merged; a secret name that is already public, a `## Secret` heading in a public
file and a mirror without `secrecy: secret` / `mirror_of` are refused at the door; an approved phase
is frozen and cannot `begin`; approve refuses an incomplete roster; `drop` retires a roster item;
merge records tokens and seconds.
"""

import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import TestCampaign, MarkerGuard, SCRIPTS, PROJECT, CAMPAIGNS

sys.path.insert(0, str(SCRIPTS))

FRONT = "---\nentity: {eid}\ntype: {etype}\nsecrecy: {secrecy}\nphase: {phase}\nstamped: []\n{link}\n---\n\n# {eid}\n\n## Public\n\n- one line\n"


def row(eid, etype, name, secrecy="public", **extra):
    r = {"id": eid, "type": etype, "name": name, "aliases": [], "summary": f"{name} — bir satır.",
         "file": None, "secrecy": secrecy, "created_phase": "P5", "origin": "birth", "stamped": {}, "refs": []}
    r.update(extra)
    return r


def fragment(eid, registry, phase="P5", **extra):
    f = {"schema_version": 1, "id": eid, "type": registry.get("type") if registry else "batch", "phase": phase, "attempt": 1,
         "agent": f"{phase}.{eid}.a1", "mode": "birth", "prose": None, "dm_only_prose": None,
         "notes": f"design/_staging/{phase}/{eid}.notes.md", "registry": registry, "graph": {"nodes": [], "edges": []},
         "seeds": [], "counts": {}, "status": "staged"}
    f.update(extra)
    return f


class Registry(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("tune1")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)
        self.staging = self.c.path("design/_staging/P5")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def canonical(self):
        return self.c.json("design/dm-only/entities.json")["entities"]

    def test_3_2_container_fragment_merges_its_rows_and_counts_as_merged(self):
        self.c.write_json("design/_staging/P5/npcbatch_7.json", fragment("npcbatch_7", None, rows=[
            row("npc_tunetest_a", "npc", "Wender Hask"), row("npc_tunetest_b", "npc", "Ilsa Rook")],
            counts={"npcs": 2}))
        proc = self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("container, 2 row(s)", proc.stdout)
        self.assertIn("npc_tunetest_a", self.canonical())
        self.assertTrue((self.staging / "merged" / "npcbatch_7.json").is_file())
        report = self.c.json("design/_staging/P5/merge.report.json")
        self.assertEqual(report["containers"], ["npcbatch_7"])
        self.assertEqual(report["refused"], {})
        # the manifest sees the container as merged, so a roster that names it completes
        self.c.reopen("P5", "partial", roster=["npcbatch_7"])
        self.c.run("design_manifest.py", "reconcile", check=True)
        m = self.c.json("design/design.json")
        self.assertEqual(m["entities"]["npcbatch_7"]["status"], "merged")
        self.assertEqual(m["phases"]["P5"]["status"], "merged")

    def test_3_2_a_refused_unit_never_blocks_the_others(self):
        self.c.write_json("design/_staging/P5/npc_tunetest_good.json", fragment("npc_tunetest_good", row("npc_tunetest_good", "npc", "Orrin Vale")))
        self.c.write_json("design/_staging/P5/calculus_tune.json", fragment("calculus_tune", {"id": "calculus_tune", "type": "calculus", "name": "x", "secrecy": "public", "stamped": {}}))
        self.c.write_json("design/_staging/P5/npc_tunetest_bad.json", fragment("npc_tunetest_bad", row("npc_tunetest_bad", "wizardry", "Bad Row")))
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("refused 1: npc_tunetest_bad", proc.stdout)
        self.assertIn("npc_tunetest_good", self.canonical())
        self.assertNotIn("npc_tunetest_bad", self.canonical())
        self.assertTrue((self.staging / "merged" / "calculus_tune.json").is_file(), "a document container with no rows still merges")
        self.assertTrue((self.staging / "refused" / "npc_tunetest_bad.attempt-1.json").is_file())
        report = self.c.json("design/_staging/P5/merge.report.json")
        self.assertIn("unknown type", report["refused"]["npc_tunetest_bad"][0])
        # the conductor's merge marks it failed with the reason; the next begin renders attempt 2 with that reason
        self.c.reopen("P5", "partial", roster=["npc_tunetest_good", "npc_tunetest_bad"])
        self.c.write_json("design/_staging/P5/npc_tunetest_bad.json", fragment("npc_tunetest_bad", row("npc_tunetest_bad", "wizardry", "Bad Row")))
        merge = self.c.run("designer.py", "phase", "P5", "merge")
        self.assertEqual(merge.returncode, 1)
        self.assertIn("marked failed", merge.stderr)
        m = self.c.json("design/design.json")
        self.assertEqual(m["entities"]["npc_tunetest_bad"]["status"], "failed")
        self.assertIn("unknown type", m["entities"]["npc_tunetest_bad"]["last_error"])
        self.assertEqual(m["phases"]["P5"]["status"], "partial")
        begin = self.c.run("designer.py", "phase", "P5", "begin", "--json", check=True)
        out = json.loads(begin.stdout[begin.stdout.index("{"):])
        self.assertEqual([e["id"] for e in out["entities"]], ["npc_tunetest_bad"])
        self.assertEqual(out["entities"][0]["render_attempt"], 2)
        self.assertIn("--attempt 2", out["entities"][0]["prompt_cmd"])
        rendered = self.c.path("design/_prompts/P5/npc_tunetest_bad.md").read_text(encoding="utf-8")
        self.assertIn("refused by the registry", rendered)
        self.assertIn("unknown type", rendered)

    def test_3_1_a_stub_is_filled_without_stamp_drift_and_never_counts_as_merged(self):
        stub = row("npc_tunetest_stub", "npc", "Hollin Marr", status="pending", owner_phase="P5", reserved_by="P4.skeleton.a1")
        self.c.write_json("design/_staging/P4/npc_tunetest_stub.json", fragment("npc_tunetest_stub", stub, phase="P4"))
        self.c.run("registry.py", "merge", "--phase", "P4", check=True)
        self.c.reopen("P5", "partial", roster=["npc_tunetest_stub"])
        self.c.run("design_manifest.py", "reconcile", check=True)
        m = self.c.json("design/design.json")
        self.assertEqual(m["entities"]["npc_tunetest_stub"]["status"], "pending", "a stub row is a reservation, not a merged entity")
        self.assertEqual(m["phases"]["P5"]["status"], "partial")
        filled = row("npc_tunetest_stub", "npc", "Hollin Marr", faction="faction_tidewardens", stamped={"faction": "faction_tidewardens"})
        self.c.write_json("design/_staging/P5/npc_tunetest_stub.json", fragment("npc_tunetest_stub", filled))
        proc = self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("(stub filled)", proc.stdout)
        snap = self.c.json("design/dm-only/_snapshots/stamps.json")["stamps"]["npc_tunetest_stub"]
        self.assertEqual(snap, {"faction": "faction_tidewardens"})
        self.c.run("design_manifest.py", "reconcile", check=True)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P5"]["status"], "merged")
        # a filled row's stamps are frozen from here on
        drift = dict(filled, stamped={"faction": "faction_other"}, faction="faction_other")
        self.c.write_json("design/_staging/P5/npc_tunetest_stub.json", fragment("npc_tunetest_stub", drift))
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("stamped field(s) changed without --revise: faction", proc.stderr)

    def test_4_a_secret_name_or_alias_that_is_public_is_refused(self):
        public_name = next(e["name"] for e in self.c.json("design/entities.json")["entities"].values() if e.get("type") == "npc")
        secret = row("npc_s77", "npc", "Opaque Slug", secrecy="secret", aliases=[public_name])
        self.c.write_json("design/_staging/P5/npc_s77.json", fragment("npc_s77", secret))
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("is already public", proc.stderr)
        self.assertIn("never a public word in name/aliases", proc.stderr)
        self.assertNotIn("npc_s77", self.canonical())
        ok = row("npc_s78", "npc", "Opaque Slug Two", secrecy="secret")
        self.c.write_json("design/_staging/P5/npc_s78.json", fragment("npc_s78", ok))
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("npc_s78", self.canonical())

    def test_4_secret_heading_in_public_prose_and_bad_mirror_front_matter_are_refused(self):
        pub = self.c.path("design/npcs/npc_tunetest_p.md")
        mir = self.c.path("design/dm-only/npcs/npc_tunetest_p.md")
        pub.write_text(FRONT.format(eid="npc_tunetest_p", etype="npc", secrecy="public", phase="P5",
                                    link="mirror: design/dm-only/npcs/npc_tunetest_p.md") + "\n## Secret\n\n- leaked here\n", encoding="utf-8")
        mir.write_text(FRONT.format(eid="npc_tunetest_p", etype="npc", secrecy="public", phase="P5",
                                    link="public: design/npcs/npc_tunetest_p.md"), encoding="utf-8")
        frag = fragment("npc_tunetest_p", row("npc_tunetest_p", "npc", "Perrin Gale", file="design/npcs/npc_tunetest_p.md"),
                        prose={"file": "design/npcs/npc_tunetest_p.md"}, dm_only_prose={"file": "design/dm-only/npcs/npc_tunetest_p.md"})
        self.c.write_json("design/_staging/P5/npc_tunetest_p.json", frag)
        proc = self.c.run("registry.py", "merge", "--phase", "P5")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("carries a `## Secret` heading", proc.stderr)
        self.assertIn("needs `secrecy: secret`", proc.stderr)
        self.assertIn("must name `mirror_of:", proc.stderr)
        # repaired: the public file loses its Secret section, the mirror gets the right front matter
        pub.write_text(FRONT.format(eid="npc_tunetest_p", etype="npc", secrecy="public", phase="P5",
                                    link="mirror: design/dm-only/npcs/npc_tunetest_p.md"), encoding="utf-8")
        mir.write_text(FRONT.format(eid="npc_tunetest_p", etype="npc", secrecy="secret", phase="P5",
                                    link="mirror_of: design/npcs/npc_tunetest_p.md").replace("## Public", "## Secret"), encoding="utf-8")
        self.c.write_json("design/_staging/P5/npc_tunetest_p.json", frag)
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("npc_tunetest_p", self.canonical())


class PhaseState(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("tune1p")
        self.c.run("design_manifest.py", "set-mode", "birth", check=True)

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_3_5_an_approved_phase_is_frozen_by_reconcile(self):
        self.c.reopen("P3", "approved", roster=["region_saltmere", "region_never_written"])
        self.c.run("design_manifest.py", "reconcile", check=True)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P3"]["status"], "approved")

    def test_3_5_approve_refuses_an_incomplete_roster_unless_forced(self):
        merged = self.c.path("design/_staging/P6/merged")
        for f in merged.glob("*.json"):
            shutil.copy(f, merged.parent / f.name)
        self.c.reopen("P6", "prerolled")
        self.c.run("designer.py", "phase", "P6", "begin", "--json", check=True)
        self.c.run("designer.py", "phase", "P6", "merge", check=True)
        m = self.c.json("design/design.json")
        m["phases"]["P6"]["roster"] = list(m["phases"]["P6"].get("roster") or []) + ["site_never_written"]
        self.c.write_json("design/design.json", m)
        self.c.run("designer.py", "phase", "P6", "card", check=True)
        proc = self.c.run("designer.py", "phase", "P6", "approve", "--onay")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("site_never_written", proc.stderr)
        self.assertIn("not complete", proc.stderr)
        self.c.run("designer.py", "phase", "P6", "approve", "--onay", "--force", check=True)
        self.assertEqual(self.c.json("design/design.json")["phases"]["P6"]["status"], "approved")

    def test_3_2_drop_retires_a_roster_item_that_never_reached_the_registry(self):
        self.c.reopen("P3", "partial", roster=["region_saltmere", "villagebatch_9"])
        proc = self.c.run("designer.py", "phase", "P3", "drop", "--id", "villagebatch_9", "--reason", "failed twice", check=True)
        self.assertIn("dropped villagebatch_9", proc.stdout)
        m = self.c.json("design/design.json")
        self.assertNotIn("villagebatch_9", m["phases"]["P3"]["roster"])
        self.assertEqual(m["phases"]["P3"]["dropped"]["villagebatch_9"]["reason"], "failed twice")
        refused = self.c.run("designer.py", "phase", "P3", "drop", "--id", "region_saltmere", "--reason", "x")
        self.assertEqual(refused.returncode, 1, "a registry entity is removed through design_revise, not drop")
        self.assertIn("design_revise", refused.stderr)

    def test_observations_merge_records_tokens_and_seconds_for_the_card(self):
        self.c.reopen("P6", "partial")
        before = self.c.json("design/design.json")["phases"]["P6"]
        tokens0, wall0 = int((before.get("tokens") or {}).get("out") or 0), int(before.get("wall_s") or 0)
        self.c.run("designer.py", "phase", "P6", "merge", "--tokens", "405000", "--seconds", "642", check=True)
        self.c.run("designer.py", "phase", "P6", "merge", "--tokens", "1000", "--seconds", "58", check=True)
        ph = self.c.json("design/design.json")["phases"]["P6"]
        self.assertEqual(ph["tokens"]["out"], tokens0 + 406000)
        self.assertEqual(ph["wall_s"], wall0 + 700)


USED = PROJECT / "used.json"


class Preroll(unittest.TestCase):
    """Observations, preroll: count rolls say the count, P5 secret kinds are secret and distinct."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-tune-pre-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
        self.env = env
        self.run_designer("new", self.name, "--scale", "short", "--party-size", "1", "--seed", "TUNE-T1", "--lang", "tr")

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def run_designer(self, *args, script="designer.py"):
        proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True,
                              env=self.env, encoding="utf-8")
        if proc.returncode != 0:
            raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}): {proc.stdout} {proc.stderr}")
        return proc

    def manifest(self):
        return json.loads((CAMPAIGNS / self.name / "design" / "design.json").read_text(encoding="utf-8"))

    def test_count_rolls_carry_the_count_they_produced(self):
        proc = self.run_designer("-c", self.name, "preroll", "--phase", "P2")
        recs = {r["label"]: r for r in self.manifest()["dice_log"] if r["phase"] == "P2"}
        ages = recs["ages_count"]
        self.assertIn("value", ages)
        drawn = sorted(l for l in recs if l.startswith("age."))
        self.assertEqual(len(drawn), ages["value"], "the count roll bounds the rows drawn")
        self.assertIn("→ count", proc.stdout)
        rendered = self.run_designer("-c", self.name, "render", "P2.cosmos", script="design_prompts.py").stdout
        self.assertIn(f"`ages_count` = **{ages['value']}** — produce exactly this many", rendered)

    def test_p5_secret_kinds_are_secret_and_distinct(self):
        self.run_designer("-c", self.name, "preroll", "--phase", "P5")
        m = self.manifest()
        public = [r["label"] for r in m["dice_log"] if r["phase"] == "P5"]
        self.assertFalse([l for l in public if l.endswith(".secret")], "npc secret kinds never enter design.json")
        self.assertIn("npc.1.secret", m["dice_log_secret"]["labels"])
        secret = json.loads((CAMPAIGNS / self.name / "design" / "dm-only" / "dice-log.json").read_text(encoding="utf-8"))
        kinds = [r["row_id"] for r in secret["rolls"] if r["phase"] == "P5" and r["label"].endswith(".secret")]
        self.assertEqual(len(kinds), len(set(kinds)), f"{len(kinds)} npcs, 21 secret kinds: no kind twice")
        self.assertTrue(all(k.startswith("npcsecret_") for k in kinds))


if __name__ == "__main__":
    unittest.main()
