"""
test_p2_dry_walk.py — build item 22e (docs/p2-build-22.md part 22e): the dry walk of P2. Model-free, with the real
commands, on `_test-` campaigns whose P1 the stand-ins of the P1 dry walk wrote and approved: preroll P2 → begin →
the stand-in writer on the frame → merge (the door) → check (the script rules, the ledger) → the stand-in critics →
card (the gate) → approve (used.json), at each scale. Then the wrong turns the specification names, each from the
state after begin: a frame field changed, a P1-named plane left untouched, a festival missing for a greater god, a
dated day outside the span, a secret seat's name in a public file.

The stand-ins (test_cosmos_door.P2Walk, test_p1_dry_walk.Walker) invent nothing: every row is the frame's, every
text field a plain line.
"""

import copy
import json
import shutil
import sys
import unittest

from _campaign import SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_cosmos_door as cd  # noqa: E402
import design_dice as dd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402
from test_cosmos_door import P2Walk  # noqa: E402

SEEDS = {"short": "WALK-P2-SHORT", "standard": "COSMOS-PIN-17", "epic": "COSMOS-HOME-1"}
NAMED_SEED = "WALK-P2-STANDARD-1"          # a standard birth whose P1 names a plane (a ruin's)


def critics(p2: P2Walk, verdict: str = "pass") -> list[dict]:
    """The stand-in critics of P2: the entity critic on the cosmology (every rubric it is given), the phase critic with
    a verdict for every critic-judged promise due at P2, the wishes critic."""
    import design_prompts as dpm
    name = p2.w.name
    entity = sorted(dpm.given_rubrics("P2", "entity"))
    phase = sorted(dpm.given_rubrics("P2", "phase") - {"rubric_wishes"})
    due = [p for p in dm.load(name)["promises"] + dp.load_secret(name) if p["check"] == "critic" and p["due"] == "P2"]
    finding = lambda rid, eid: {"rubric_id": rid, "entity_id": eid, "verdict": "pass"}
    files = {f"{cd.UNIT}.critic1.json": {"entity_id": cd.UNIT, "verdict": verdict, "findings": [finding(r, cd.UNIT) for r in entity]},
             "phase.critic1.json": {"entity_id": "P2", "verdict": verdict, "findings": [finding(r, "P2") for r in phase],
                                    "promises": [{"id": p["id"], "verdict": "kept", "note": "as_written"} for p in due]},
             "wishes.critic1.json": {"entity_id": "P2", "verdict": "pass", "findings": []}}
    for fname, ret in files.items():
        (p2.staging / fname).write_text(json.dumps(ret), encoding="utf-8")
    return due


class Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        if USED.is_file():
            USED.unlink()

    @classmethod
    def tearDownClass(cls):
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)


class Walk(Base):
    """The walk at each scale, P2 approved at its end."""

    def walk(self, scale: str):
        p2 = P2Walk(scale, SEEDS[scale])
        w = p2.w
        try:
            m = dm.load(w.name)
            # 1. the preroll: the cosmos, the seal, the frame, P2's rows in the ledger
            self.assertTrue(cd.applies(m) and m.get(cd.SEAL))
            self.assertEqual(cd.seal_errors(w.name, m), [])
            self.assertTrue((w.dir / cd.frame_rel()).is_file())
            self.assertEqual(cd.name_errors(p2.frame), [], "every framed row, festival and moon named from the pool")
            begin = json.loads(p2.begin.stdout[p2.begin.stdout.index("{"):])
            self.assertEqual([e["id"] for e in begin["entities"]], [cd.UNIT])
            prompt = open(begin["entities"][0]["prompt_file"], encoding="utf-8").read()
            self.assertIn(cd.frame_rel(), prompt)
            self.assertIn("**Promises due at this phase.**", prompt)
            # 2. the stand-in writer; the door passes it
            p2.write()
            merge = p2.merge()
            self.assertNotIn("✗", merge.stderr, merge.stderr[-2500:])
            self.assertLessEqual(set(cd.framed_rows(p2.frame)), set(w.merged()))
            self.assertEqual(cd.seal_errors(w.name, dm.load(w.name)), [], "the merge left the cosmos as rolled")
            # 3. check: the script rules run, every script promise due at P2 is kept, P1's promises to P2 close
            check = w.d("phase", "P2", "check")
            self.assertRegex(check.stdout, r"P2 validator — 0 errors")
            m = dm.load(w.name)
            ruled = [p for p in m["promises"] + dp.load_secret(w.name) if p["check"] != "critic" and p["due"] == "P2"]
            self.assertTrue(ruled and all(p["status"] == "kept" for p in ruled), [p["text"] for p in ruled if p["status"] != "kept"])
            # 4. the stand-in critics: every critic-judged promise due at P2 kept
            due = critics(p2)
            recorded = w.d("phase", "P2", "merge")
            self.assertIn("critic return(s) recorded", recorded.stdout)
            judged = {p["id"]: p for p in dm.load(w.name)["promises"] + dp.load_secret(w.name)}
            self.assertTrue(all(judged[p["id"]]["status"] == "kept" for p in due))
            left = [p for p in judged.values() if p["due"] == "P2" and p["status"] == "open"]
            self.assertEqual(left, [], "every promise due at P2 is closed")
            # 5. the card: the gate is open; no secret, no die
            self.assertEqual(da.gate(w.name, "P2"), [], "the gate is open")
            w.d("phase", "P2", "card")
            card = (w.dir / "design/_approval/P2.card.md").read_text(encoding="utf-8")
            for words in ("# P2 — THE COSMOS", "Gate:** open", "  secret: checked by script: all kept", "  door: passed · "):
                self.assertIn(words, card)
            self.assertNotIn("not run yet", card)
            secret = json.loads((w.dir / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))["cosmos"]
            for hidden in (secret.get("hidden_names") or {}).values():
                self.assertNotIn(hidden, card)
            # 6. approve: P2 approved, its unique rows in used.json
            approve = w.d("phase", "P2", "approve")
            self.assertIn("P2 approved", approve.stdout)
            self.assertEqual(dm.load(w.name)["phases"]["P2"]["status"], "approved")
            mine = dd.load_used()["campaigns"][w.name]
            p2_tables = {r["table"] for r in dm.load(w.name)["dice_log"] if r.get("phase") == "P2" and r.get("row_id")
                         and ".yaml" in str(r.get("table")) and dt.records_usage(r["table"])}
            self.assertTrue(p2_tables and p2_tables <= set(mine), sorted(p2_tables - set(mine)))
        finally:
            w.remove()

    def test_the_walk_at_short(self):
        self.walk("short")

    def test_the_walk_at_standard(self):
        self.walk("standard")

    def test_the_walk_at_epic(self):
        self.walk("epic")


class WrongTurns(Base):
    """Each from the state after begin, on a standard birth whose P1 names a plane."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.p2 = P2Walk("standard", NAMED_SEED)
        cls.snapshot = cls.p2.w.dir.parent / (cls.p2.w.name + ".snap")
        shutil.copytree(cls.p2.w.dir, cls.snapshot)

    @classmethod
    def tearDownClass(cls):
        cls.p2.w.remove()
        shutil.rmtree(cls.snapshot, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        shutil.rmtree(self.p2.w.dir, ignore_errors=True)
        shutil.copytree(self.snapshot, self.p2.w.dir)

    def refused(self, change=None, prose_extra: str = "") -> str:
        self.p2.write(change, prose_extra=prose_extra)
        proc = self.p2.merge()
        self.assertIn("✗", proc.stderr, proc.stdout[-500:])
        return proc.stderr

    def test_the_good_write_passes(self):
        self.p2.write()
        self.assertNotIn("✗", self.p2.merge().stderr)

    def test_a_frame_field_changed(self):
        god = next(e for e in self.p2.frame["rows"] if e.startswith("god_"))
        err = self.refused(lambda f: next(r for r in f["rows"] if r["id"] == god).update(alignment="CE" if "CE" != self.p2.frame["rows"][god]["registry"]["alignment"] else "LG"))
        self.assertIn(f"{god}: `alignment` differs", err)

    def test_a_p1_named_plane_left_untouched(self):
        named = [e for e, x in self.p2.frame["rows"].items() if x["registry"].get("type") == "plane" and x["registry"].get("named_by")]
        self.assertTrue(named, "the seed's P1 names a plane")
        err = self.refused(lambda f: [r.__setitem__("named_by", []) for r in f["rows"] if r["id"] in named])
        self.assertIn("`named_by` differs", err)
        self.assertIn("names a plane, and no touched plane carries it", err)

    def test_a_festival_missing_for_a_greater_god(self):
        err = self.refused(lambda f: f["calendar"].__setitem__("festivals", [x for x in f["calendar"]["festivals"] if x["god"] is None]))
        self.assertIn("has no festival; every greater god has one", err)

    def test_a_dated_day_outside_the_span(self):
        st = self.p2.frame["container"]["calendar"]["start"]
        far = {"year": st["year"] + 5, "month": st["month"], "day": st["day"]}

        def change(f):
            f["calendar"] = copy.deepcopy(f["calendar"])
            f["calendar"]["dated"]["lawless_day"] = far
        err = self.refused(change)
        self.assertIn("`calendar.dated", err)

    def test_a_secret_seats_name_in_a_public_file(self):
        secret = json.loads((self.p2.w.dir / "design/dm-only/name-pool-secret.json").read_text(encoding="utf-8"))
        name = next(e["name"] for L in secret["languages"].values() for e in L.get("god", []))
        err = self.refused(prose_extra=f"some say {name} still listens.")
        self.assertIn("carries a secret name", err)
        self.assertNotIn(name, err, "the refusal names the kind, never the name")


if __name__ == "__main__":
    unittest.main()
