"""
test_p1_birth_faults.py — build item 18f (docs/p1-build-18.md, Part 18f; docs/reports/p1-test-birth-1.md section 6): the
test birth's pipeline faults, each on a `_test-` campaign walked by the dry walk's stand-ins: a refusal a later fragment
answered never reaches the next prompt; the card shows a correction round and what it changed; a critic's reason code is
a slug, never null on a finding that is not a pass, and one carrying a secret term never reaches the public record; the
preroll's old tongue says why it has no roots; the writer's and the critics' prompts read dm-only with the Read tool;
`phase rerun` clears the validator's last result. Failure messages name no secret row.
"""

import json
import sys
import unittest

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_manifest as dm  # noqa: E402
import design_prompts as dpm  # noqa: E402
from test_p1_dry_walk import Base, run  # noqa: E402


def revise(w, text: str):
    return run("design_revise.py", "-c", w.name, "round", "--phase", "P1", "--scope", "entity", "--entity", w.premise_id,
               "--action", "replace", "--text", text)


class Faults(Base):

    def good(self):
        w = self.walker()
        w.write()
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "check")
        return w

    def test_a_refusal_a_later_fragment_answered_never_reaches_the_next_prompt(self):
        """#7: the door refused a unit, the writer's next fragment merged; the old refusal leaves the entity's row, and the
        prompt of the next round carries none."""
        w = self.walker()

        def change(rows, picked):
            next(r for r in rows.values() if r.get("slot") == "people")["name"] = "Zarvothkin"
        w.write(change)
        w.d("phase", "P1", "merge", check=False)
        sig = next(e for e, r in w.rows.items() if r.get("slot") == "people")
        self.assertTrue(dm.load(w.name)["entities"][sig].get("last_error"), "the refusal is recorded")
        # the test birth's writer owned the refused unit (one agent wrote every row): its own row carried the refusal
        m = dm.load(w.name)
        m["entities"][w.premise_id]["last_error"] = m["entities"][sig]["last_error"]
        dm.save(w.name, m, "test: the writer owned the refused unit")
        w.write()
        w.d("phase", "P1", "merge")
        m = dm.load(w.name)
        for eid in (sig, w.premise_id):
            self.assertEqual((m["entities"][eid]["status"], m["entities"][eid].get("last_error")), ("merged", None), eid)
        w.critics()
        w.d("phase", "P1", "merge")
        revise(w, "Say the pitch in fewer words.")
        begin = w.d("phase", "P1", "begin", "--json")
        out = json.loads(begin.stdout[begin.stdout.index("{"):])
        prompt = open(out["entities"][0]["prompt_file"], encoding="utf-8").read()
        self.assertNotIn("was refused by the registry", prompt)

    def test_the_card_shows_a_correction_round_and_what_it_changed(self):
        """#10, #11: the header names the round beside the attempt; a section lists what the round reran and which public
        files changed since the card before it; that card is kept."""
        w = self.good()
        w.critics()
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "card")
        before = (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        self.assertNotIn("correction round", before)
        revise(w, "Say the pitch in fewer words.")
        w.d("phase", "P1", "begin", "--json")
        w.write(public_extra="\nThe road is kept, and nobody asks why.\n")
        w.d("phase", "P1", "merge")
        w.critics()
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "card")
        card = (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        self.assertIn("attempt 1 · correction round 1", card.splitlines()[0])
        self.assertIn("## CHANGES FROM THE PREVIOUS CARD (correction round 0 → 1)", card)
        self.assertIn(f"  rewritten: {w.premise_id}", card)
        self.assertIn("  public files changed: design/premise.md", card)
        self.assertTrue((w.dir / "design/_approval/P1.attempt-1.round-0.card.md").is_file(), "the card before the round is kept")
        rounds = dm.load(w.name)["phases"]["P1"]["approval"]["rounds"]
        self.assertEqual(rounds[-1]["rerun"], [w.premise_id])

    def test_a_reason_code_is_a_slug_never_null_and_never_secret(self):
        """#8: a finding that is not a pass with no reason code is refused at the record; #6: a code that carries a secret
        term is recorded as `secret_term`, so the report never shows it."""
        w = self.good()
        rid = "rubric_p1_legible"
        ret = lambda code: {"entity_id": w.premise_id, "verdict": "fix",
                            "findings": [dict({"rubric_id": rid, "entity_id": w.premise_id, "verdict": "fix"}, **({"reason_code": code} if code else {}))]}
        (w.staging / f"{w.premise_id}.critic1.json").write_text(json.dumps(ret(None)), encoding="utf-8")
        proc = w.d("phase", "P1", "merge", check=False)
        self.assertIn("names its reason code (a slug), refused", proc.stdout + proc.stderr)
        self.assertTrue((w.staging / f"{w.premise_id}.critic1.json").is_file(), "the refused return stays in staging")
        log = w.json("design/dm-only/dice-log.json")
        secret_id = log["threat"]["goal"]["id"]                       # never printed: a secret row
        (w.staging / f"{w.premise_id}.critic1.json").write_text(json.dumps(ret(f"{secret_id}_unclear")), encoding="utf-8")
        w.d("phase", "P1", "merge")
        recs = dm.load(w.name)["phases"]["P1"]["critique"]["records"]
        codes = [f["reason_code"] for r in recs for f in r["findings"]]
        self.assertEqual(codes, ["secret_term"])
        self.assertFalse(secret_id in json.dumps(dm.load(w.name)), "the public manifest holds no secret row id")
        report = w.d("phase", "P1", "report").stdout
        self.assertIn("secret_term", report)
        self.assertFalse(secret_id in report, "the report names no secret row")

    def test_the_old_tongue_says_why_it_has_no_roots(self):
        """#13: the preroll's names line gives the old tongue no "0 roots" but the reason."""
        w = self.walker()
        line = next(l for l in w.preroll.stdout.splitlines() if l.startswith("designer: names — "))
        self.assertIn("no roots (the old tongue names its sites from its bag's parts)", line)
        self.assertNotIn(", 0 roots", line)

    def test_the_writer_and_the_critics_read_dm_only_with_the_read_tool(self):
        """#1: the auto-mode classifier refused a Bash read of the dice log; the writer's and the critics' prompts say Read."""
        w = self.walker()
        begin = json.loads(w.begin.stdout[w.begin.stdout.index("{"):])
        prompt = open(begin["entities"][0]["prompt_file"], encoding="utf-8").read()
        self.assertIn("with the Read tool and never with Bash", prompt)
        lines = dpm.critic_lines(dm.load(w.name), "P1")
        for key in ("critic_reads", "phase_reads"):
            self.assertIn("Read every dm-only file with the Read tool, never with Bash", lines[key], key)

    def test_a_phase_critic_s_fix_on_a_covered_row_reaches_the_premise_s_writer(self):
        """#5 (the audit's addition): the phase critic said fix on a signature row the premise's fragment writes; P1's
        roster holds only the premise, and no fix was sent. Now the next `begin --json` lists the premise with the phase
        fix (its findings in the prompt), once per attempt: PHASE_FIX_LOOP's limit."""
        w = self.good()
        sig = next(e for e, r in w.rows.items() if r.get("slot") == "phenomenon")
        w.critics()
        path = w.staging / "phase.critic1.json"
        ret = json.loads(path.read_text(encoding="utf-8"))
        ret["verdict"] = "fix"
        ret["findings"][0].update({"rubric_id": "rubric_p1_legible", "entity_id": sig, "verdict": "fix",
                                    "reason_code": "play_floor_unrepresentable"})      # 19a: a rubric the phase critic is given
        path.write_text(json.dumps(ret), encoding="utf-8")
        rubric = ret["findings"][0]["rubric_id"]
        w.d("phase", "P1", "merge")
        import design_approval as da
        self.assertEqual(next(i for i in da.gate(w.name, "P1") if i["code"] == "phase_fix_due")["ids"], [w.premise_id])
        begin = w.d("phase", "P1", "begin", "--json")
        out = json.loads(begin.stdout[begin.stdout.index("{"):])
        entry = next(e for e in out["entities"] if e["id"] == w.premise_id)
        self.assertEqual(entry["phase_fix"], [{"rubric_id": rubric, "entity_id": sig, "reason_code": "play_floor_unrepresentable"}])
        self.assertIn(sig, entry["covers"], "the workflow can route a later phase fix on the row itself")
        prompt = open(entry["prompt_file"], encoding="utf-8").read()
        self.assertIn(f"**The phase critic's fix:** {rubric} on {sig} (play_floor_unrepresentable)", prompt)
        attempt = dm.load(w.name)["entities"][w.premise_id]["attempt"]
        w.d("phase", "P1", "begin", "--json")
        self.assertEqual(dm.load(w.name)["entities"][w.premise_id]["attempt"], attempt, "a second begin serves nothing again")
        self.assertNotIn("phase_fix_due", {i["code"] for i in da.gate(w.name, "P1")})
        # the writer repairs it (its fragments carry the attempt it was rendered for); the phase critic says fix once
        # more: the unit had its phase fix this attempt
        w.write()
        for frag in w.staging.glob("*.json"):
            data = json.loads(frag.read_text(encoding="utf-8"))
            if "registry" in data:
                data["attempt"] = entry["render_attempt"]
                frag.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        w.d("phase", "P1", "merge")
        self.assertEqual(dm.load(w.name)["entities"][w.premise_id]["status"], "merged")
        w.critics()
        path.write_text(json.dumps(ret), encoding="utf-8")
        w.d("phase", "P1", "merge")
        out = json.loads((lambda p: p.stdout[p.stdout.index("{"):])(w.d("phase", "P1", "begin", "--json")))
        self.assertEqual(out["entities"], [], "one phase fix per unit and attempt; the owner decides the rest")
        self.assertNotIn("phase_fix_due", {i["code"] for i in da.gate(w.name, "P1")})

    def test_rerun_clears_the_validator_s_last_result(self):
        """Item 17's note: a rerun's new attempt never shows the last attempt's "0 errors"."""
        w = self.good()
        self.assertIsInstance(dm.load(w.name)["phases"]["P1"]["validator"]["errors"], int)
        w.d("phase", "P1", "rerun", "--reason", "a test of the rerun")
        ph = dm.load(w.name)["phases"]["P1"]
        self.assertEqual((ph["attempt"], ph["validator"], ph["door"]), (2, None, None))


if __name__ == "__main__":
    unittest.main()
