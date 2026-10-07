"""
test_p1_frame.py — build item 20a (docs/p1-build-20.md): the script frames P1's registry rows. `phase P1 begin` writes
the frame of every row the writer owes, with every rolled field in place and `stamped` an object; a writer that fills
only the text fields merges (the dry walk's stand-in writer works on the frame); a `stamped` written as a list, a break
row without its name, a changed rolled field are refused with the field named, and the refusal never prints a
frame value.
"""

import copy
import json
import sys
import unittest

from _campaign import SCRIPTS
from test_p1_dry_walk import Base, run

sys.path.insert(0, str(SCRIPTS))
import design_door as door  # noqa: E402
import design_frame as dfr  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import is_fragment  # noqa: E402


class TheFrame(Base):

    def check_frame(self, scale: str):
        w = self.walker(scale, f"FRAME-{scale.upper()}")
        path = w.dir / dfr.frame_rel(w.name)
        self.assertTrue(path.is_file(), "begin writes the frame")
        self.assertFalse(is_fragment(path), "a frame is no fragment")
        frame = json.loads(path.read_text(encoding="utf-8"))
        rebuilt = dfr.build(w.name)
        self.assertEqual({k: v for k, v in frame.items() if k != "_meta"}, {k: v for k, v in rebuilt.items() if k != "_meta"})
        m = dm.load(w.name)
        ident, found = m["identity"], m["foundation"]
        secret = w.json("design/dm-only/dice-log.json")["identity"]["secret"]
        naming = w.json("design/naming.json")
        # the premise
        p = frame["premise"]["registry"]
        self.assertEqual(p["id"], w.premise_id)
        self.assertEqual((p["type"], p["name"], p["file"], p["secrecy"], p["created_phase"]), ("premise", "The premise", "design/premise.md", "public", "P1"))
        self.assertEqual(p["tensions"], [q["id"] for q in ident["questions"]])
        self.assertEqual(p["trope_breaks"], [b["id"] for b in ident["trope_breaks"]])
        self.assertIsInstance(p["stamped"], dict)
        self.assertEqual(sorted(p["stamped"]), ["question", "signatures", "trope_breaks"])
        twist = secret["twist"]
        self.assertEqual(p["secret_class"], dt.row("secrets.yaml#twist", twist)["hides_in"] if twist else "threat")
        d = p["dm_only"]
        self.assertEqual(d["secret_twist"], twist)
        self.assertEqual(d["stamped_fields"], ["secret_twist"])
        self.assertEqual([(c["n"], c["levels"], c["piece"]) for c in d["clues"]],
                         [(s["n"], list(s["levels"]), s["clues"][0]["piece"]) for s in secret["stages"]])
        pin = secret["pin"]
        self.assertEqual(d["pinned"], {"god": "", "relation": pin["relation"], "event": pin["event"]} if pin["god"]
                         else {"piece": pin["piece"], "event": pin["event"]})
        self.assertEqual("dm_only.pinned.god" in frame["premise"]["fill"], bool(pin["god"]))
        # the signatures
        self.assertEqual(sorted(frame["signatures"]), sorted(door.SLOTS))
        for slot, e in frame["signatures"].items():
            r = e["registry"]
            self.assertEqual(e["candidates"], [c["name"] for c in naming["candidates"][slot]["names"]])
            self.assertEqual(len(e["candidates"]), 4)
            self.assertEqual((r["slot"], r["kind"], r["lang"]), (slot, dfr.SIGNATURE_KIND[slot], naming["candidates"][slot]["language"]))
            self.assertEqual(r["home"], door.home_id_of(ident, found, slot))
            self.assertEqual(r["rolled"], door.rolled_of_identity(ident, slot))
            self.assertEqual(r["stamped"], {"kind": dfr.SIGNATURE_KIND[slot], "slot": slot})
            hooks = door.hooks_by_floor_of(ident, slot)
            self.assertEqual([(n["phase"], n["hook"]) for n in r["appears"]], [(ph, h) for ph in sorted(hooks) for h in sorted(hooks[ph])])
            self.assertTrue(all(n["text"] == "" for n in r["appears"]))
            self.assertIn("appears[].text", e["fill"])
        # the breaks
        self.assertEqual(list(frame["breaks"]), [b["id"] for b in ident["trope_breaks"]])
        for b in ident["trope_breaks"]:
            r = frame["breaks"][b["id"]]["registry"]
            self.assertEqual((r["id"], r["name"], r["row"], r["tie"], r["stamped"]),
                             (b["id"], dt.row("trope-breaks.yaml", b["id"])["label"], b["id"], b["tie"], {"row": b["id"]}))
        # the prompt points the writer at it
        begin = json.loads(w.begin.stdout[w.begin.stdout.index("{"):])
        prompt = open(begin["entities"][0]["prompt_file"], encoding="utf-8").read()
        self.assertIn(f"`{dfr.frame_rel(w.name)}`", prompt)
        self.assertIn("copy every other field unchanged", prompt)
        return w

    def test_the_frame_at_short(self):
        self.check_frame("short")

    def test_the_frame_at_standard(self):
        self.check_frame("standard")

    def test_the_frame_at_epic(self):
        w = self.check_frame("epic")
        self.assertEqual(len(dm.load(w.name)["identity"]["questions"]), len(json.loads((w.dir / dfr.frame_rel(w.name)).read_text(encoding="utf-8"))["premise"]["registry"]["tensions"]))


class TheDoorOnTheFrame(Base):

    def refused(self, w, change) -> str:
        w.write(change)
        proc = w.d("phase", "P1", "merge", check=False)
        refused = w.json("design/_staging/P1/merge.report.json").get("refused") or {}
        return proc.stdout + proc.stderr + json.dumps(refused)

    def test_a_writer_that_fills_only_the_text_merges(self):
        w = self.walker()
        w.write()
        merge = w.d("phase", "P1", "merge")
        self.assertEqual(set(w.merged()), set(w.rows), merge.stderr[-2000:])
        self.assertTrue((w.dir / dfr.frame_rel(w.name)).is_file(), "the frame stays beside the fragments")

    def test_stamped_as_a_list_is_refused_by_its_name(self):
        w = self.walker()
        out = self.refused(w, lambda rows, picked: rows[w.premise_id].update(stamped=["question", "signatures", "trope_breaks"]))
        self.assertIn("stamped must be an object", out)
        self.assertIn("`stamped` must be an object, as the script's frame has it", out)
        self.assertNotIn(w.premise_id, w.merged())

    def test_a_break_without_its_name_is_refused(self):
        w = self.walker()
        brk = next(b["id"] for b in dm.load(w.name)["identity"]["trope_breaks"])
        out = self.refused(w, lambda rows, picked: rows[brk].pop("name"))
        self.assertIn(f"{brk}: name missing", out)
        self.assertIn(f"{brk}: `name` is missing; the script's frame sets it", out)
        self.assertNotIn(brk, w.merged())

    def test_a_changed_rolled_field_is_refused_by_its_name_and_never_its_value(self):
        w = self.walker()
        piece = None

        def change(rows, picked):
            nonlocal piece
            sig = next(r for r in rows.values() if r.get("slot") == "institution")
            sig["kind"] = "magic"
            sig["appears"] = sig["appears"][:-1]
            p = rows[w.premise_id]
            piece = p["dm_only"]["clues"][0]["piece"]
            p["dm_only"]["clues"][0]["levels"] = [1, 20]
            p["dm_only"]["pinned"]["event"] = "another event"
            p["tensions"] = list(reversed(p["tensions"])) + ["tension_more"]
            p["stamped"]["question"] = "a question the row does not ask"
        out = self.refused(w, change)
        sig = next(e for e, r in w.rows.items() if r.get("slot") == "institution")
        self.assertIn(f"{sig}: `kind` differs from the script's frame", out)
        self.assertIn(f"{sig}: `appears` differs from the script's frame", out)
        self.assertIn(f"{w.premise_id}: `dm_only.clues[].levels` differs from the script's frame", out)
        self.assertIn(f"{w.premise_id}: `dm_only.pinned.event` differs from the script's frame", out)
        self.assertIn(f"{w.premise_id}: `tensions` differs from the script's frame", out)
        self.assertIn(f"{w.premise_id}: `stamped.question` must equal the row's own `question`", out)
        self.assertNotIn(piece, out, "a refusal names the field, never a frame value")

    def test_ids_and_the_premise_s_signatures_agree(self):
        w = self.walker()

        def change(rows, picked):
            old = next(e for e, r in rows.items() if r.get("slot") == "phenomenon")
            rows["signature_somewhere_else"] = dict(rows.pop(old), id="signature_somewhere_else")
        out = self.refused(w, change)
        self.assertIn("signature_somewhere_else: a signature's id is `signature_<slug of its name>`", out)
        self.assertIn(f"{w.premise_id}: `signatures` lists the ids of the three signature rows beside it", out)


class TheAddendum(Base):
    """docs/p1-build-20.md, "Added from the birth's report": the writer's own check (5), the known villain's public face
    (6), the lifeline that sets no side (7), the cost of a fully refused run (8)."""

    def check(self, w, *extra):
        return run("registry.py", "-c", w.name, "check", "--phase", "P1", *extra, check=False)

    def test_the_check_judges_the_staged_fragments_and_writes_nothing(self):
        w = self.walker()
        w.write(lambda rows, picked: rows[w.premise_id].update(stamped=["question"]))
        staged = sorted(f.name for f in w.staging.glob("*.json"))
        proc = self.check(w, "--id", w.premise_id)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(f"  ✗ {w.premise_id}: stamped must be an object", proc.stdout)
        self.assertIn("(nothing written)", proc.stdout)
        self.assertEqual(sorted(f.name for f in w.staging.glob("*.json")), staged, "every fragment stays staged")
        self.assertFalse((w.staging / "merge.report.json").exists())
        self.assertEqual(w.merged(), {})
        self.assertEqual(self.check(w, "--id", "premise_nothing").returncode, 1)
        w.write()
        proc = self.check(w, "--id", w.premise_id)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(f"registry: check P1 — {len(w.rows)} staged unit(s), 0 with faults; the merge would take them all", proc.stdout)
        self.assertEqual(w.merged(), {}, "a check merges nothing")

    def test_the_prompts_carry_the_check_the_face_and_the_lifeline(self):
        import design_prompts as dpm
        w = self.walker()
        text = dpm.render(w.name, "P1.premise", w.premise_id)
        self.assertIn(f"registry.py -c {w.name} check --phase P1 --id {w.premise_id}`", text)
        self.assertIn("The villain's public face", text)
        self.assertIn("never decides a side's stance or its means", text)
        self.assertIn("check --phase <PN> --id <your id>", (SCRIPTS.parent / "prompts/design/_common.md").read_text(encoding="utf-8"))
        flow = (SCRIPTS.parents[2] / "workflows/design-fanout.js").read_text(encoding="utf-8")
        self.assertIn("run the registry check your prompt gives", flow)
        rubric = dt.row("rubrics.yaml#phase_rubric", "rubric_p1_legible")
        self.assertIn("public face", rubric["question"])
        self.assertIn("has no public face in the public premise", rubric["fails_when"])

    def test_a_fully_refused_run_is_not_merged(self):
        import tempfile
        from pathlib import Path
        w = self.walker()
        w.write()
        m = dm.load(w.name)
        m["identity"]["people"]["attitude"] = "stranger_edited"          # the seal refuses every unit
        dm.save(w.name, m, "test")
        d = Path(tempfile.mkdtemp()) / "wf_refused"
        d.mkdir()
        (d / "agent-a.meta.json").write_text(json.dumps({"description": f"P1.{w.premise_id}.a1"}), encoding="utf-8")
        (d / "agent-a.jsonl").write_text(json.dumps({"type": "assistant", "requestId": "r1", "message": {"usage": {
            "output_tokens": 100, "input_tokens": 2, "cache_creation_input_tokens": 10, "cache_read_input_tokens": 1000}}}) + "\n", encoding="utf-8")
        w.d("phase", "P1", "merge", "--run-dir", str(d), check=False)
        run_rec = dm.load(w.name)["phases"]["P1"]["cost"]["runs"]["wf_refused"]
        self.assertEqual((run_rec["merged"], run_rec["units"]), (False, {"merged": 0, "refused": len(w.rows)}))


class TheTwistsClass(unittest.TestCase):
    """The door reads a twist's class in the twist table (build item 20a): the archetype table lacks
    twist_greater_power, and the door then asked `threat` of a birth that rolled it."""

    def test_every_twist_has_its_class_in_the_twist_table(self):
        for r in dt.rows("secrets.yaml#twist"):
            self.assertTrue(r.get("hides_in"), r["id"])
        self.assertIsNone(dt.row("secrets.yaml#archetype", "twist_greater_power"))

    def test_the_door_asks_the_twist_s_class(self):
        d = object.__new__(door.Door)
        d.identity = {"questions": [], "trope_breaks": []}
        d.rows = {}
        d.secret_identity = {"secret": {"twist": "twist_greater_power", "facts": {"who": "x"}}}
        row = {"tensions": [], "secret_class": dt.row("secrets.yaml#twist", "twist_greater_power")["hides_in"]}
        errs = [e for e in door.Door.premise_errors(d, "premise_x", row) if "secret_class" in e]
        self.assertEqual(errs, [])
        errs = [e for e in door.Door.premise_errors(d, "premise_x", dict(row, secret_class="threat")) if "secret_class" in e]
        self.assertEqual(len(errs), 1)


if __name__ == "__main__":
    unittest.main()
