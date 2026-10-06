"""
test_p1_dry_walk.py — build item 17 (docs/p1-build-17.md): the dry walk of P1. Model-free, with the real commands, on
a `_test-` campaign of its own, at each scale: new → preroll → begin → the stand-in writer → merge (the door) → check
(the script rules) → the stand-in critics → card (the gate) → approve (used.json) → a second campaign on the same
used.json. Then eleven wrong turns, each from the state after the stand-in writer (three on the chain, build item 18f).

The stand-in writer and the stand-in critics live here; they are no part of the product. The writer invents nothing:
every name is a candidate or a stock name, every id is copied from the records.

  py test_p1_dry_walk.py --times     how long the three walks take
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_dice as dd  # noqa: E402
import design_door as door  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_names as dn  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402

TIMES: dict = {}


def run(script, *args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout[-1500:]}\n{proc.stderr[-2500:]}")
    return proc


class Walker:
    """One `_test-` campaign and the stand-ins that walk it."""

    def __init__(self, scale: str, seed: str):
        self.name = f"_test-walk-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        self.scale, self.seed = scale, seed
        self.dir = CAMPAIGNS / self.name
        self.slug = self.name.replace("-", "_")
        self.premise_id = f"premise_{self.slug}"
        self.staging = self.dir / "design/_staging/P1"

    def remove(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def d(self, *args, check=True):
        return run("designer.py", "-c", self.name, *args, check=check)

    def json(self, rel):
        return json.loads((self.dir / rel).read_text(encoding="utf-8"))

    # steps 1-3
    def born(self):
        self.new = run("designer.py", "new", self.name, "--party-size", "2", "--seed", self.seed, "--lang", "tr", "--scale", self.scale)
        self.preroll = self.d("preroll", "--phase", "P1")
        self.begin = self.d("phase", "P1", "begin", "--json")
        return self

    # step 4: the stand-in writer
    def write(self, change=None, public_extra: str = "", mirror_extra: str = ""):
        m = dm.load(self.name)
        ident = m["identity"]
        naming, pool = self.json("design/naming.json"), self.json("design/dm-only/name-pool.json")
        secret_ledger = self.json("design/dm-only/promises.json")["promises"]
        the_door = door.Door(self.name, {"entities": {}}, [])
        secret = self.json("design/dm-only/dice-log.json")["identity"]["secret"]
        twist = secret["twist"]                                                                   # build item 18d: optional
        arch = dt.row("secrets.yaml#twist", twist) if twist else {"id": None, "hides_in": "threat"}
        self.pin = pin = secret["pin"]                                                            # build item 18e (W1)
        base = lambda eid, etype, name, **extra: dict({
            "id": eid, "type": etype, "name": name, "aliases": [], "summary": "what a native would say of it, in one line.",
            "file": "design/premise.md", "secrecy": "public", "created_phase": "P1", "origin": "birth", "stamped": {}, "refs": []}, **extra)
        rows = {}
        picked = {}
        for slot in door.SLOTS:
            picked[slot] = naming["candidates"][slot]["names"][0]["name"]
            eid = "signature_" + re.sub(r"[^a-z0-9]+", "_", door.bare(picked[slot]).lower()).strip("_")
            rows[eid] = base(eid, "signature", picked[slot], kind="institution" if slot == "institution" else "magic", stamped={"kind": slot},
                             slot=slot, home=the_door.home_id(slot), rolled=the_door.rolled_of(slot), rule="how a native knows it, in a line.",
                             appears=[{"phase": p, "hook": sorted(hooks)[0], "text": f"at this floor the {slot} shows in what the natives do every day"}
                                      for p, hooks in sorted(the_door.hooks_by_floor(slot).items())])
        for b in ident["trope_breaks"]:
            eid = "break_" + b["id"][len("break_"):]
            rows[eid] = base(eid, "break", dt.row("trope-breaks.yaml", b["id"])["label"], row=b["id"], tie=b["tie"], stamped={"row": b["id"]})
        god = next(e["name"] for L in pool["languages"].values() for e in L.get("god", []))
        stages = sorted((p for p in secret_ledger if p["source"] == "clue_stage"), key=lambda p: p["clue"])
        sig_ids = [e for e in rows if e.startswith("signature_")]
        rows[self.premise_id] = base(
            self.premise_id, "premise", "The premise", question="who keeps what the old keepers left?", pitch="One thing is asked. Three things are only here. One rule is turned over.",
            tensions=[q["id"] for q in ident["questions"]], signatures=sig_ids, trope_breaks=[e for e in rows if e.startswith("break_")],
            secret_class=arch["hides_in"], stamped={"question": "who keeps what the old keepers left?"},
            refs=sig_ids,
            dm_only={"secret_twist": arch["id"], "secret": "the truth of the move, told once and only here.", "villain_answer": "the pole carried to its end.",
                     "dm_pitch": "what the keeper of the table steers toward.", "stamped_fields": ["secret_twist"],
                     "pinned": ({"god": god, "relation": pin["relation"], "event": "the move"} if pin["god"] else {"piece": pin["piece"], "event": "the move"}),
                     "clues": [{"n": p["clue"], "levels": p["levels"], "kind": "a thing seen", "piece": secret["stages"][p["clue"] - 1]["clues"][0]["piece"],
                                "how": "a search", "placed_in": None} for p in stages]})
        if change:
            change(rows, picked)
        self.rows, self.picked = rows, picked
        people = picked["people"]
        covers = ", ".join(e for e in rows if e != self.premise_id)
        public = (f"---\nentity: {self.premise_id}\ntype: premise\nsecrecy: public\nphase: P1\nstamped: [question, signatures, trope_breaks]\n"
                  f"covers: [{covers}]\nmirror: design/dm-only/premise-secret.md\n---\n\n# Premise\n\n## Public\n\n### The question\n"
                  f"- who keeps what the old keepers left?\n\n### The three signatures\n- **The people:** the {door.bare(people)} keep the road and ask nothing for it.\n"
                  f"- **The institution:** nobody argues with {picked['institution']} twice.\n- **The phenomenon:** when {picked['phenomenon']} comes, the natives stay indoors.\n\n"
                  f"### The player pitch\nOne thing is asked. Three things are only here. One rule is turned over.\n{public_extra}\n## Discoverable\n\n- a native could learn why the road is kept.\n")
        mirror = (f"---\nentity: {self.premise_id}\ntype: premise\nsecrecy: secret\nphase: P1\nmirror_of: design/premise.md\n---\n\n## Secret\n\n### The secret\n"
                  f"The truth of the move is written in this file and in no other file of this birth"
                  + (f"; {god} is the god it is pinned to.\n" if pin["god"] else ".\n") + mirror_extra)
        (self.dir / "design/dm-only").mkdir(parents=True, exist_ok=True)
        (self.dir / "design/premise.md").write_text(public, encoding="utf-8", newline="\n")
        (self.dir / "design/dm-only/premise-secret.md").write_text(mirror, encoding="utf-8", newline="\n")
        self.staging.mkdir(parents=True, exist_ok=True)
        for f in self.staging.glob("*.json"):
            f.unlink()
        for eid, r in rows.items():
            frag = {"schema_version": 1, "id": eid, "type": r["type"], "phase": "P1", "attempt": 1, "agent": f"P1.{eid}.a1", "mode": "birth",
                    "prose": {"file": "design/premise.md"} if eid == self.premise_id else None,
                    "dm_only_prose": {"file": "design/dm-only/premise-secret.md"} if eid == self.premise_id else None,
                    "notes": None, "registry": r, "graph": {"nodes": [], "edges": []}, "seeds": [], "counts": {}, "status": "staged"}
            if eid == self.premise_id:
                frag["members"] = [e for e in rows if e != eid]
            (self.staging / f"{eid}.json").write_text(json.dumps(frag, ensure_ascii=False), encoding="utf-8")
        return self

    # step 7: the stand-in critics
    def critics(self, verdict="pass", promises="kept", skip=None):
        rubrics = [r["id"] for r in dt.rows("rubrics.yaml#phase_rubric") if r["phase"] == "P1"]
        finding = lambda rid, eid: {"rubric_id": rid, "entity_id": eid, "verdict": "pass"}
        public, secret = dm.load(self.name)["promises"], dp.load_secret(self.name)
        due = [p for p in public + secret if p["check"] == "critic" and p["due"] == "P1"]
        entries = [{"id": p["id"], "verdict": promises, "note": "as_written"} for p in due if not (skip and skip(p))]
        self.staging.mkdir(parents=True, exist_ok=True)
        files = {
            f"{self.premise_id}.critic1.json": {"entity_id": self.premise_id, "verdict": verdict, "findings": [finding(r, self.premise_id) for r in rubrics]},
            f"{self.premise_id}.critic2.json": {"entity_id": self.premise_id, "verdict": verdict, "findings": [finding(r, self.premise_id) for r in reversed(rubrics)]},
            "phase.critic1.json": {"entity_id": "P1", "verdict": verdict, "findings": [finding(r, "P1") for r in rubrics], "promises": entries},
            "wishes.critic1.json": {"entity_id": "P1", "verdict": "pass", "findings": []}}
        for name, ret in files.items():
            (self.staging / name).write_text(json.dumps(ret), encoding="utf-8")
        return due

    def merged(self) -> dict:
        p = self.dir / "design/dm-only/entities.json"
        return json.loads(p.read_text(encoding="utf-8"))["entities"] if p.is_file() else {}

    def secret_names(self) -> list[str]:
        return [e["name"] for L in self.json("design/dm-only/name-pool-secret.json")["languages"].values() for v in L.values() for e in v]


class Base(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        if USED.is_file():
            USED.unlink()
        self.walkers: list[Walker] = []

    def tearDown(self):
        for w in self.walkers:
            w.remove()
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def walker(self, scale="standard", seed="WALK-0001") -> Walker:
        w = Walker(scale, seed)
        self.walkers.append(w)
        return w.born()


class Walk(Base):

    def walk(self, scale: str):
        t0 = time.time()
        w = self.walker(scale, f"WALK-{scale.upper()}")
        # 1. new: blank dials rolled, P0 approved as a test birth is
        m = dm.load(w.name)
        self.assertEqual(m["dials"]["scale"], scale)
        self.assertIn("roll: dial.tone", w.new.stdout)
        self.assertEqual(m["phases"]["P0"]["status"], "approved")
        # 2. preroll: the foundation, the identity, the secret layer, the names, both ledgers, the seal
        for key in ("foundation", "identity", "promises", "p1_seal"):
            self.assertTrue(m.get(key), key)
        log = w.json("design/dm-only/dice-log.json")
        self.assertTrue(log["identity"]["secret"]["keeping"] and log["identity"]["villain"]["shape"] and log["identity"]["secret"]["stages"])
        naming = w.json("design/naming.json")
        self.assertTrue(naming["rolled"] and len(naming["candidates"]) == 3)
        for rel in ("design/dm-only/name-pool.json", "design/dm-only/name-pool-secret.json", "design/dm-only/promises.json"):
            self.assertTrue((w.dir / rel).is_file(), rel)
        self.assertEqual(door.seal_errors(w.name, m), [])
        # 3. begin: the writer's prompt renders with the candidates, the Names paragraph and the promises due at P1
        begin = json.loads(w.begin.stdout[w.begin.stdout.index("{"):])
        self.assertEqual([e["id"] for e in begin["entities"]], [w.premise_id])
        prompt = open(begin["entities"][0]["prompt_file"], encoding="utf-8").read()
        # the prompt may carry the secret: no assertion here prints it
        self.assertTrue("**Names (rolled, never invented).**" in prompt, "the Names paragraph")
        self.assertTrue("**Promises due at this phase.**" in prompt, "the promises block")
        # the prompt points at the candidates (14a); the writer reads them from the public naming.json
        self.assertTrue("`design/naming.json`" in prompt and "`candidates`" in prompt, "the prompt points at the candidates")
        for slot in door.SLOTS:
            self.assertEqual(len(naming["candidates"][slot]["names"]), 4, slot)
        for p in m["promises"]:
            self.assertEqual(f"`{p['id']}`" in prompt, p["due"] == "P1", p["id"])
        self.assertEqual(dm.load(w.name)["phases"]["P1"]["status"], "running")
        # 4-5. the stand-in writer; merge: the door passes every unit, the notes are promises, the placements join
        w.write()
        merge = w.d("phase", "P1", "merge")
        self.assertEqual(set(w.merged()), set(w.rows), merge.stderr[-2500:])
        self.assertNotIn("✗", merge.stderr)
        report = w.json("design/_staging/P1/merge.report.json")
        self.assertFalse(report.get("refused"))
        m = dm.load(w.name)
        # W4 (build item 18e): a note restates its table's hook, so it joins that hook's promise as a further source and
        # brings its text as advice; every note is in the ledger
        notes = [p for p in m["promises"] if p["source"] == "note" or any(a["source"] == "note" for a in p.get("also") or [])]
        written = [n for r in w.rows.values() if r["type"] == "signature" for n in r["appears"]]
        # build item 18f (test birth P1-1, #4): the phenomenon's play floor has a note the door accepts
        self.assertIn("play", {n["phase"] for r in w.rows.values() if r.get("slot") == "phenomenon" for n in r["appears"]})
        self.assertEqual({(n["phase"], n["hook"]) for n in written}, {(p["due"], p["text"]) for p in notes})
        self.assertTrue(all(n["text"] in next(p for p in notes if p["text"] == n["hook"] and p["due"] == n["phase"])["advice"] for n in written))
        secret = dp.load_secret(w.name)
        placed = [p for p in secret if p["source"] == "placement"]
        self.assertEqual(sorted(str(p.get("kind")) for p in placed), ["clue", "clue", "clue", "event"] + (["god"] if w.pin["god"] else []))
        self.assertEqual(door.seal_errors(w.name, m), [], "the merge left the preroll's records as they were")
        self.assertEqual(m["entities"][w.premise_id]["status"], "merged")
        # 6. check: the script rules run; every script promise due by P1 is kept
        check = w.d("phase", "P1", "check")
        self.assertRegex(check.stdout, r"designer: P1 validator — 0 errors")
        self.assertRegex(check.stdout, r"promises a script checks — \d+ kept, 0 not kept")
        m = dm.load(w.name)
        ruled = [p for p in m["promises"] + dp.load_secret(w.name) if p["check"] != "critic" and p["due"] in ("P0", "P1")]
        self.assertTrue(ruled and all(p["status"] == "kept" for p in ruled))
        # 7. the stand-in critics: pass on every rubric, kept for every critic-judged promise due at P1
        due = w.critics()
        recorded = w.d("phase", "P1", "merge")
        self.assertIn("critic return(s) recorded", recorded.stdout)
        m = dm.load(w.name)
        judged = {p["id"]: p for p in m["promises"] + dp.load_secret(w.name)}
        self.assertTrue(all(judged[p["id"]]["status"] == "kept" for p in due))
        # 8. card: the gate is open; the card shows the picked names and the ledger's counts
        self.assertEqual(da.gate(w.name, "P1"), [], "the gate is open")
        w.d("phase", "P1", "card")
        card = (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        for slot, name in w.picked.items():
            self.assertIn(name, card, slot)
        self.assertIn(f"the {w.picked['people']} tongue", card)
        self.assertNotIn("not run yet", card)
        self.assertNotIn("(not named yet)", card)
        self.assertNotIn("(not written yet)", card)
        self.assertNotIn("None", card)
        self.assertIn("Gate:** open", card)
        c = dp.counts(m["promises"], dp.load_secret(w.name), "P1")
        self.assertIn(f"  due at P1: {c['due']['total']} — kept {c['due']['kept']}, not kept 0, waived 0", card)
        self.assertEqual(c["due"]["open"], 0, "nothing due at P1 is left open")
        self.assertIn(f"  secret: {c['secret']['open']} open, {c['secret']['kept']} kept, 0 not kept", card)
        self.assertIn("  door: passed · ", card)
        leaked = [n for n in w.secret_names() if re.search(rf"(?<!\w){re.escape(n)}(?!\w)", card)]
        self.assertEqual(len(leaked), 0, "a secret-stock name is on the card")
        for r in log["rolls"]:
            if r.get("row_id") and ".yaml" in str(r.get("table")):
                self.assertFalse(r["row_id"] in card, f"a rolled row of {r['label'].split('.')[0]} is on the card")
        # 9. approve: the phase is approved; the rows, the roots, the bags and the villain's pair are in used.json
        approve = w.d("phase", "P1", "approve")
        self.assertIn("P1 approved", approve.stdout)
        m = dm.load(w.name)
        self.assertEqual(m["phases"]["P1"]["status"], "approved")
        mine = dd.load_used()["campaigns"][w.name]
        roots = [r for L in naming["languages"].values() for r in L["roots"]] + naming["calendar"]["month_roots"] + naming["calendar"]["day_roots"]
        self.assertEqual(sorted(mine[dn.LEX]), sorted(roots))
        self.assertEqual(sorted(mine[dn.FAMILY]), sorted(L["bag"] for L in naming["languages"].values()))
        import design_identity as di
        villain = log["identity"]["villain"]
        self.assertEqual(mine[di.VILLAIN_PAIR_KEY], [dd.hashed(f"{villain['shape']}|{villain['origin']}")], "the pair, hashed")
        self.assertIn(m["foundation"]["lifeline"]["id"], mine["foundation.yaml#lifeline"])
        self.assertIn(dd.hashed(log["identity"]["secret"]["keeping"]), mine["secrets.yaml#keeping"])
        self.assertFalse(log["identity"]["secret"]["keeping"] in json.dumps(mine), "a secret row is kept as a hash")
        # 10. a second campaign on the same used.json draws none of the first one's unique rows, roots or bags
        second = self.walker(scale, f"WALK-{scale.upper()}-B")
        m2, naming2 = dm.load(second.name), second.json("design/naming.json")
        roots2 = {r for L in naming2["languages"].values() for r in L["roots"]} | set(naming2["calendar"]["month_roots"]) | set(naming2["calendar"]["day_roots"])
        self.assertFalse(roots2 & set(roots), "a root of the first campaign was drawn again")
        self.assertFalse({L["bag"] for L in naming2["languages"].values()} & {L["bag"] for L in naming["languages"].values()})
        for rec in m2["dice_log"]:
            ref = rec.get("table") or ""
            if rec.get("phase") == "P1" and rec.get("row_id") and ".yaml" in ref and dt.own_roll_header(ref).get("avoid_used") and not rec.get("usage_fallback") \
                    and rec.get("notation") != "forced":
                self.assertFalse(rec["row_id"] in mine.get(ref, []), f"{ref}: the second campaign drew the first one's row")
        TIMES[scale] = round(time.time() - t0, 1)

    def test_the_walk_at_short(self):
        self.walk("short")

    def test_the_walk_at_standard(self):
        self.walk("standard")

    def test_the_walk_at_epic(self):
        self.walk("epic")


class WrongTurns(Base):
    """Each from the state after the stand-in writer, with one thing changed."""

    def refused(self, w: Walker) -> tuple[str, dict]:
        proc = w.d("phase", "P1", "merge", check=False)
        return proc.stdout + proc.stderr, w.json("design/_staging/P1/merge.report.json").get("refused") or {}

    def test_a_signature_named_outside_its_candidates(self):
        w = self.walker()

        def change(rows, picked):
            sig = next(r for r in rows.values() if r.get("slot") == "people")
            sig["name"] = "Zarvothkin"
        w.write(change)
        out, refused = self.refused(w)
        sig = next(e for e, r in w.rows.items() if r.get("slot") == "people")
        self.assertIn("is none of its four candidates", " ".join(refused[sig]))
        self.assertIn("is none of its four candidates", out)
        merged = w.merged()
        self.assertNotIn(sig, merged)
        self.assertTrue({e for e, r in w.rows.items() if r["type"] == "break"} <= set(merged), "the other units are written")

    def test_an_invented_capitalised_word_in_the_public_prose(self):
        w = self.walker()
        w.write(public_extra="\nThe keepers answer to the Ashen Tribunal and to nobody else.\n")
        out, refused = self.refused(w)
        lines = refused[w.premise_id]
        self.assertTrue(any(re.search(r"design/premise\.md line \d+: the capitalised word 'Ashen'", l) for l in lines), lines)
        self.assertNotIn(w.premise_id, w.merged())

    def test_a_field_of_the_identity_edited_after_the_preroll(self):
        w = self.walker()
        w.write()
        m = dm.load(w.name)
        m["identity"]["people"]["attitude"] = "stranger_edited"
        dm.save(w.name, m, "test")
        out, refused = self.refused(w)
        self.assertEqual(set(refused), set(w.rows), "the seal refuses every unit")
        self.assertIn("design.json#identity differs from what the preroll stamped", out)
        self.assertEqual(w.merged(), {})

    def test_a_secret_stock_name_in_the_public_prose(self):
        w = self.walker()
        name = w.secret_names()[0]
        w.write(public_extra=f"\nNobody speaks of {name} on the road.\n")
        out, refused = self.refused(w)
        self.assertTrue(any("of the secret stock" in l for l in refused[w.premise_id]))
        self.assertFalse(name in out.replace(f"capitalised word '{name}'", ""), "the line names no name")
        self.assertFalse(name in json.dumps(refused).replace(f"capitalised word '{name}'", ""), "the report names no name")

    def test_a_signature_without_a_note_for_a_promised_floor(self):
        w = self.walker()

        def change(rows, picked):
            sig = next(r for r in rows.values() if r.get("slot") == "institution")
            sig["appears"] = sig["appears"][:-1]
        w.write(change)
        out, refused = self.refused(w)
        sig = next(e for e, r in w.rows.items() if r.get("slot") == "institution")
        self.assertTrue(any("no `appears` note for" in l for l in refused[sig]), refused[sig])

    # build item 18f: three wrong turns on the chain

    def test_a_texture_piece_in_a_clue_s_place(self):
        """A stage's chain clue stands on a piece of the chain; the lifeline (texture) there is refused at the door."""
        w = self.walker()

        def change(rows, picked):
            rows[w.premise_id]["dm_only"]["clues"][0]["piece"] = "lifeline"
        w.write(change)
        out, refused = self.refused(w)
        self.assertTrue(any("`dm_only.clues.piece` names 'lifeline', a texture piece" in l for l in refused[w.premise_id]),
                        "the door names the field and the layer")
        self.assertNotIn(w.premise_id, w.merged())

    def test_a_hidden_truth_that_serves_no_clue(self):
        """A signature's hidden truth exists only as the medium of a stage's clue; one that names no stage is refused."""
        w = self.walker()

        def change(rows, picked):
            sig = next(r for r in rows.values() if r.get("slot") == "phenomenon")
            sig["dm_only"] = {"true_rule": "what the natives do not know of the rule, in a line."}
        w.write(change)
        out, refused = self.refused(w)
        sig = next(e for e, r in w.rows.items() if r.get("slot") == "phenomenon")
        self.assertTrue(any("exists only as the medium of a stage's clue" in l for l in refused[sig]), "the door asks for `serves_clue`")
        self.assertNotIn(sig, w.merged())

    def test_a_missing_lair_closes_the_d_and_d_gate(self):
        """The D&D line (G9): a threat without its lair closes the gate; the card shows the cross, approve is refused."""
        w = self.good()
        w.critics()
        w.d("phase", "P1", "merge")
        self.assertEqual(da.gate(w.name, "P1"), [], "the gate is open before")
        path = w.dir / "design/dm-only/dice-log.json"
        log = json.loads(path.read_text(encoding="utf-8"))
        log["threat"]["lair"] = {"form": None, "where": None}
        path.write_text(json.dumps(log), encoding="utf-8")
        item = next(i for i in da.gate(w.name, "P1") if i["code"] == "dnd_incomplete")
        self.assertIn("lair", item["detail"])
        w.d("phase", "P1", "card")
        card = (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        self.assertIn("✗ lair", card)
        approve = w.d("phase", "P1", "approve", check=False)
        self.assertEqual(approve.returncode, 1)
        self.assertIn("dnd_incomplete", approve.stderr)

    def good(self) -> Walker:
        w = self.walker()
        w.write()
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "check")
        return w

    def test_a_due_promise_the_critic_gave_no_verdict(self):
        w = self.good()
        public = dm.load(w.name)["promises"]
        left = next(p for p in public if p["check"] == "critic" and p["due"] == "P1")
        w.critics(skip=lambda p: p["id"] == left["id"])
        w.d("phase", "P1", "merge")
        codes = {i["code"]: i for i in da.gate(w.name, "P1")}
        self.assertEqual(codes["promise_unjudged"]["ids"], [left["id"]])
        approve = w.d("phase", "P1", "approve", check=False)
        self.assertEqual(approve.returncode, 1)
        self.assertIn("promise_unjudged", approve.stderr)

    def test_a_critics_not_kept_on_a_public_promise(self):
        w = self.good()
        public = dm.load(w.name)["promises"]
        broken = next(p for p in public if p["check"] == "critic" and p["due"] == "P1")
        w.critics()
        ret = json.loads((w.staging / "phase.critic1.json").read_text(encoding="utf-8"))
        next(e for e in ret["promises"] if e["id"] == broken["id"])["verdict"] = "not_kept"
        (w.staging / "phase.critic1.json").write_text(json.dumps(ret), encoding="utf-8")
        w.d("phase", "P1", "merge")
        self.assertEqual(da.gate(w.name, "P1"), [], "the gate stays open")
        w.d("phase", "P1", "card")
        card = (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        self.assertIn(f"    not kept: {broken['name']} → {broken['text']}", card)
        self.assertIn("judged not kept 1", w.d("phase", "P1", "report").stdout)
        w.d("promise", "waive", broken["id"], "It stands as it is.")
        w.d("phase", "P1", "card")
        self.assertNotIn("    not kept:", (w.dir / "design/_approval/P1.card.md").read_text(encoding="utf-8"))

    def test_a_critics_rerun_at_p1(self):
        w = self.good()
        w.critics(verdict="rerun")
        proc = w.d("phase", "P1", "merge", check=False)
        self.assertIn("a P1 critic return says `rerun`, refused", proc.stdout + proc.stderr)
        self.assertIn("critic_missing", {i["code"] for i in da.gate(w.name, "P1")}, "a refused return is no verdict")
        self.assertTrue((w.staging / "phase.critic1.json").is_file(), "the refused return stays in staging")


if __name__ == "__main__":
    if "--times" in sys.argv:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Walk)
        result = unittest.TextTestRunner(verbosity=0).run(suite)
        print("the three walks:", ", ".join(f"{k} {v}s" for k, v in TIMES.items()), "| ok" if result.wasSuccessful() else "| FAILED")
    else:
        unittest.main()
