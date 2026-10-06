"""
test_door.py — build item 13b (docs/p1-build-13.md, Part 13b): P1's door. On a new birth a well-formed P1 (three
signatures, the rolled trope breaks, the premise with its two files) merges; each rule of sections 7-12 is then
broken by one fragment that is refused with its line, and the corrected set passes. Over many seeds the script-built
P1 passes its own door: no conflict, every candidate and stock name accepted by the name rules. No refusal line
carries a secret row or a secret-stock name. A legacy birth is checked as it always was.

  py test_door.py --report     the capitalised-common list and what the archived births' names would trip on
"""

import copy
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
import uuid
from collections import Counter

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign
from test_tuning_birth_1 import fragment, row
_row = row

sys.path.insert(0, str(SCRIPTS))
import design_door as door  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_names as dn  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402

COMMON = dt.load("naming.yaml")["rules"]["capitalised_common"]


def run(script, *args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


class Scan(unittest.TestCase):
    """Section 9, the prose scan, as a function."""

    def test_a_capitalised_word_that_opens_nothing_must_be_known(self):
        known = {"Thornwick", "the Grey March", "Halvard"}
        scan = lambda text: [w for _, w in door.stray_capitals(text, known, set(COMMON))]
        self.assertEqual(scan("The road runs to Thornwick. Nobody sleeps there."), [])
        self.assertEqual(scan("They crossed the Grey March in a week; Halvard's mule died."), [])
        self.assertEqual(scan("The Grey March is cold."), [], "a name that opens a sentence")
        self.assertEqual(scan("The road runs to Zarvoth, and nobody sleeps there."), ["Zarvoth"])
        self.assertEqual(scan("They call it the Ashen Court."), ["Ashen", "Court"], "an invented institution")
        self.assertEqual(scan("# The question\n- Theme: a thing\n| Act | Layer |\n1. First item\n> Quoted line"), [])
        self.assertEqual(scan("# The Zarvoth Question"), ["Zarvoth", "Question"], "a heading opens once")
        self.assertEqual(scan("an Animal Handling check, or Sleight of Hand; due at P3, on d20"), [], "a term of several words; an id is no word")
        self.assertEqual(scan('He said: "Nobody comes back." *Then* silence — Then nothing.'), [])
        self.assertEqual(scan("A Wisdom check, DC 12, and I am sure of it; speak Common or Elvish."), [], "the closed list")
        self.assertEqual(scan("see [[npc_halvard]] and `Zarvoth` <!-- Zarvoth -->"), [], "links, code and comments carry no prose")
        self.assertEqual(door.stray_capitals("---\nentity: premise_x\n---\nline three\nto Zarvoth it goes", known, set()), [(5, "Zarvoth")],
                         "the line is the file's own")

    def test_the_closed_list_and_the_forbidden_row(self):
        self.assertEqual(COMMON[:10], ["I", "DC", "AC", "HP", "CR", "XP", "SRD", "DM", "BBEG", "Act"])
        self.assertEqual(len(COMMON), 53, "I; nine table terms; six abilities; eighteen skills; sixteen SRD languages; three planes")
        self.assertTrue({"Hells", "Nine Hells", "Abyss"} <= set(COMMON))
        self.assertFalse({"Court", "Order", "Guild", "March", "Hall", "Lord", "Lady", "Saint", "King", "Queen"} & set(COMMON),
                         "a form, region or building word stands inside its name; a title is no exception")
        rows = dt.rows("forbidden.yaml")
        self.assertEqual(len(rows), 1)
        self.assertEqual(set(rows[0]["lexical"]), {"en"}, "the Turkish patterns went (a new birth is written in English)")


class Tables(unittest.TestCase):
    """The audit of 13b: the writer may repeat what its rolled rows say. Every capitalised word inside a sentence of a
    public P0 or P1 row's own text is on the closed list, so no later row sets the trap."""

    EXEMPT = {"PC"}                                     # stands only in the rows' table notes (`at_table`), never in world text
    NOT_TEXT = ("id", "hooks", "name_words")            # ids; instructions to the floors (the ledger's sentences); words of a name

    def strings(self, node):
        if isinstance(node, str):
            yield node
        elif isinstance(node, dict):
            for k, v in node.items():
                if k not in self.NOT_TEXT:
                    yield from self.strings(v)
        elif isinstance(node, list):
            for v in node:
                yield from self.strings(v)

    def test_a_public_rows_own_text_holds_no_capital_outside_the_list(self):
        common = set(COMMON) | self.EXEMPT
        checked = 0
        for name in ("dials.yaml", "scale.yaml", "foundation.yaml", "trope-breaks.yaml", "signatures.yaml", "tensions.yaml"):
            for sub, rows in dt.all_row_lists(dt.load(name)).items():
                for r in rows:
                    for s in self.strings(r):
                        checked += 1
                        self.assertEqual([w for _, w in door.stray_capitals(s, set(), common)], [], f"{name}#{sub} {r['id']}")
        self.assertGreater(checked, 2000)
        self.assertEqual([w for _, w in door.stray_capitals("a gate to the Abyss, a devil from the Nine Hells, the Hells' own", set(), set(COMMON))], [])
        self.assertEqual([w for _, w in door.stray_capitals("each PC carries one", set(), set(COMMON))], ["PC"], "the exemption is the test's, not the list's")


class NewBirth(unittest.TestCase):
    """A new birth's P1 through the door."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-door-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run("designer.py", "new", self.name, "--party-size", "2", "--seed", "DOOR-0001", "--lang", "tr", "--scale", "standard")
        run("designer.py", "-c", self.name, "preroll", "--phase", "P1")
        self.dir = CAMPAIGNS / self.name
        self.m = dm.load(self.name)
        self.d = door.Door(self.name, {"entities": {}}, [])
        self.naming = json.loads((self.dir / "design/naming.json").read_text(encoding="utf-8"))
        self.pool = json.loads((self.dir / "design/dm-only/name-pool.json").read_text(encoding="utf-8"))
        self.secret = json.loads((self.dir / "design/dm-only/name-pool-secret.json").read_text(encoding="utf-8"))
        self.slug = self.name.replace("-", "_")
        self.staging = self.dir / "design/_staging/P1"
        self.staging.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    # a well-formed P1, as the script's own records give it
    def units(self) -> dict:
        ident = self.m["identity"]
        out = {}
        for slot in door.SLOTS:
            name = self.naming["candidates"][slot]["names"][0]["name"]
            eid = "signature_" + re.sub(r"[^a-z0-9]+", "_", door.bare(name).lower()).strip("_")
            out[eid] = row(eid, "signature", name, created_phase="P1", kind="institution" if slot == "institution" else "magic",
                           summary="what a native knows of it, in one line.", slot=slot, home=self.d.home_id(slot),
                           rolled=self.d.rolled_of(slot), stamped={"kind": "x"},
                           appears=[{"phase": p, "hook": sorted(h)[0], "text": f"it shows at this floor in its own way, among the {slot} of the land"}
                                    for p, h in sorted(self.d.hooks_by_floor(slot).items())])   # W4 (build item 18e): the hook restated
        for b in ident["trope_breaks"]:
            eid = "break_" + b["id"][len("break_"):]
            out[eid] = row(eid, "break", dt.row("trope-breaks.yaml", b["id"])["label"], created_phase="P1", row=b["id"], tie=b["tie"],
                           summary="the break as a native states it.", stamped={"row": b["id"]})
        arch = dt.row("secrets.yaml#archetype", json.loads((self.dir / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))["identity"]["secret"]["archetype"])
        pid = f"premise_{self.slug}"
        out[pid] = row(pid, "premise", "The premise", created_phase="P1", file="design/premise.md", summary="the question in one line.",
                       tensions=[q["id"] for q in ident["questions"]], secret_class=arch["hides_in"],
                       signatures=[e for e in out if e.startswith("signature_")], trope_breaks=[e for e in out if e.startswith("break_")],
                       question="what is owed to those who stayed?", dm_only={"clues": []})
        return out

    def stage(self, units: dict, public: str | None = None, mirror: str | None = None) -> subprocess.CompletedProcess:
        pid = f"premise_{self.slug}"
        people = self.naming["candidates"]["people"]["names"][0]["name"]
        text = public if public is not None else f"The land is old.\n\nNobody argues with the {people} about the road; they keep it.\n"
        (self.dir / "design/premise.md").write_text(
            f"---\nentity: {pid}\ntype: premise\nsecrecy: public\nmirror: design/dm-only/premise-secret.md\n---\n\n## Public\n\n{text}", encoding="utf-8")
        (self.dir / "design/dm-only").mkdir(parents=True, exist_ok=True)
        (self.dir / "design/dm-only/premise-secret.md").write_text(
            f"---\nentity: {pid}\ntype: premise\nsecrecy: secret\nmirror_of: design/premise.md\n---\n\n## Secret\n\n"
            + (mirror if mirror is not None else "The truth is written here and nowhere else in this birth of the world.\n"), encoding="utf-8")
        for f in list(self.staging.glob("*.json")):
            f.unlink()
        for eid, r in units.items():
            extra = {"prose": {"file": "design/premise.md"}, "dm_only_prose": {"file": "design/dm-only/premise-secret.md"}} if eid == pid else {}
            (self.staging / f"{eid}.json").write_text(json.dumps(fragment(eid, r, phase="P1", **extra), ensure_ascii=False), encoding="utf-8")
        return run("registry.py", "-c", self.name, "merge", "--phase", "P1", check=False)

    def merged(self) -> dict:
        p = self.dir / "design/dm-only/entities.json"
        return json.loads(p.read_text(encoding="utf-8"))["entities"] if p.is_file() else {}

    def refusal(self, units: dict, **kw) -> str:
        proc = self.stage(units, **kw)
        return proc.stderr

    def test_a_well_formed_p1_passes_and_its_notes_become_promises(self):
        self.assertTrue(door.applies(self.m, "P1") and not door.applies(self.m, "P2"))
        units = self.units()
        proc = self.stage(units)
        self.assertEqual(set(self.merged()), set(units), proc.stderr[:1500])
        self.assertNotIn("✗", proc.stderr)
        added = dp.sync(self.name, "P1")
        # W4 (build item 18e): a note binds the hook it restates, joining that hook's promise
        notes = [p for p in dm.load(self.name)["promises"] if p["source"] == "note" or any(a["source"] == "note" for a in p.get("also") or [])]
        written = [n for u in units.values() if u["type"] == "signature" for n in u["appears"]]
        self.assertEqual({(n["phase"], n["hook"]) for n in written}, {(p["due"], p["text"]) for p in notes})
        self.assertGreaterEqual(added, 0, "a note that restates a hook adds no new promise: it joins the hook's (18e)")
        self.assertTrue(all(p["check"] == "critic" and p["due"] != "P1" and any(str(s["from"]).startswith("signature_")
                                                                                for s in [p] + list(p.get("also") or [])) for p in notes))
        self.assertEqual(door.seal_errors(self.name, dm.load(self.name)), [], "a note is no change of the script-built ledger")

    def test_the_rolls_are_the_writers_ground(self):
        units = self.units()
        only = f"premise_{self.slug}"
        self.assertIn("needs exactly one people signature entity beside it (0 found)", self.refusal({only: units[only]}))
        sig = next(e for e, r in units.items() if r.get("slot") == "people")
        for change, line in (({"home": "life_somewhere_else"}, "`home` must be"), ({"rolled": dict(units[sig]["rolled"], lineage="lineage_other")}, "`rolled` must hold"),
                             ({"appears": units[sig]["appears"][1:]}, "no `appears` note for"), ({"appears": [{"phase": "P1", "text": "x"}]}, "`appears` is a list of"),
                             ({"slot": "other"}, "a signature names its slot"), ({"name": "Zarvothkin"}, "is none of its four candidates")):
            bad = copy.deepcopy(units)
            bad[sig].update(change)
            err = self.refusal(bad)
            self.assertIn(line, err, change)
            self.assertNotIn(sig, self.merged())
        brk = next(e for e in units if e.startswith("break_"))
        bad = copy.deepcopy(units)
        bad[brk]["tie"] = "tie_other"
        self.assertIn("`tie` must be", self.refusal(bad))
        bad = copy.deepcopy(units)
        other = next(r["id"] for r in dt.rows("trope-breaks.yaml") if r["id"] not in {b["id"] for b in self.m["identity"]["trope_breaks"]})
        bad[brk]["row"] = other
        err = self.refusal(bad)
        self.assertIn("is no trope break this campaign rolled", err)
        self.assertIn("needs exactly one break entity (0 found)", err, "and the premise misses the rolled one")
        pid = f"premise_{self.slug}"
        bad = copy.deepcopy(units)
        bad[pid]["tensions"] = ["tension_other"]
        bad[pid]["secret_class"] = "a long sentence that gives the secret away"
        err = self.refusal(bad)
        self.assertIn("`tensions` must be the rolled question id(s)", err)
        self.assertRegex(err, r"`secret_class` is (the twist's class|`threat` when no twist was rolled)")
        self.stage(units)
        self.assertEqual(set(self.merged()), set(units), "the corrected set passes")

    def test_the_prerolls_records_are_sealed(self):
        units = self.units()
        m = dm.load(self.name)
        m["identity"]["people"]["attitude"] = "stranger_changed"
        dm.save(self.name, m, "test")
        self.d = door.Door(self.name, {"entities": {}}, [])
        err = self.refusal(self.units())
        self.assertIn("design.json#identity differs from what the preroll stamped", err)
        self.assertEqual(self.merged(), {}, "a changed record refuses every unit")
        m["identity"] = self.m["identity"]
        m["foundation"]["spine"] = "spine_changed"
        dm.save(self.name, m, "test")
        self.assertIn("design.json#foundation differs", self.refusal(units))
        dm.save(self.name, self.m, "test")
        naming = dict(self.naming, candidates=dict(self.naming["candidates"], people={**self.naming["candidates"]["people"], "names": [{"name": "Zarvothkin"}]}))
        (self.dir / "design/naming.json").write_text(json.dumps(naming), encoding="utf-8")
        bad = copy.deepcopy(units)
        next(r for r in bad.values() if r.get("slot") == "people")["name"] = "Zarvothkin"
        self.assertIn("design/naming.json differs from what the preroll stamped", self.refusal(bad))
        (self.dir / "design/naming.json").write_text(json.dumps(self.naming), encoding="utf-8")
        m = dm.load(self.name)
        m["promises"][0]["text"] = "a promise an agent rewrote"
        dm.save(self.name, m, "test")
        self.assertIn("the promise ledger's script-built part differs", self.refusal(units))
        dm.save(self.name, self.m, "test")
        # the owner's reroll is the one sanctioned change of the candidates: the seal follows it
        run("design_names.py", "-c", self.name, "reroll", "--slot", "phenomenon")
        self.assertEqual(door.seal_errors(self.name, dm.load(self.name)), [])
        self.naming = json.loads((self.dir / "design/naming.json").read_text(encoding="utf-8"))
        self.d = door.Door(self.name, {"entities": {}}, [])
        proc = self.stage(self.units())
        self.assertEqual(len(self.merged()), len(units), proc.stderr[:1500])

    def test_every_registry_name_is_pooled(self):
        units = self.units()
        lang = "people"
        row = lambda *a, **k: _row(*a, **dict({"summary": "one line of what a native knows."}, **k))
        stock = lambda key, l=lang: [e["name"] for e in self.pool["languages"][l][key]]
        sec = lambda key, l=lang: [e["name"] for e in self.secret["languages"][l][key]]
        person, god, place = stock("person")[0], stock("god")[0], stock("places")[0]
        tail = next(iter(self.d.names.natural_tails))
        good = {
            "npc_keeper": row("npc_keeper", "npc", f"{person} Reedwright", created_phase="P1", status="pending", owner_phase="P5", lang=lang),
            "god_first": row("god_first", "god", god, created_phase="P1", lang=lang),
            "settlement_first": row("settlement_first", "settlement", place, created_phase="P1", status="pending", owner_phase="P3"),
            "region_first": row("region_first", "region", stock("regions")[0], created_phase="P1", status="pending", owner_phase="P3"),
            "place_owned": row("place_owned", "place", f"{person}'s {tail.capitalize()}", created_phase="P1"),
            "place_temple": row("place_temple", "place", f"Shrine of {god}", created_phase="P1"),
            "place_inn": row("place_inn", "place", stock("inns")[0], created_phase="P1"),
            "site_old": row("site_old", "site", self.pool["languages"]["old"]["sites"][0]["name"], created_phase="P1", status="pending", owner_phase="P6"),
            "npc_s01": row("npc_s01", "npc", sec("person")[0], secrecy="secret", created_phase="P1", status="pending", owner_phase="P5", lang=lang),
        }
        proc = self.stage({**units, **good})
        self.assertEqual(set(self.merged()), set(units) | set(good), proc.stderr[:2000])
        secret_person, secret_place = sec("person")[1], sec("place")[0]
        bad = {
            "npc_invented": (row("npc_invented", "npc", "Quintarro Vale", created_phase="P1", status="pending", owner_phase="P5"), "is not on a rolled person list"),
            "npc_borrowed": (row("npc_borrowed", "npc", secret_person, created_phase="P1", status="pending", owner_phase="P5"), "may not take a name of the secret stock"),
            "npc_s02": (row("npc_s02", "npc", stock("person")[1], secrecy="secret", created_phase="P1", status="pending", owner_phase="P5"), "is named from the secret stock"),
            "npc_s03": (row("npc_s03", "npc", "Zarvoth", secrecy="secret", created_phase="P1", status="pending", owner_phase="P5"), "is named from the secret stock"),
            "settlement_built": (row("settlement_built", "settlement", "Zarvothwick", created_phase="P1", status="pending", owner_phase="P3"), "is in no stock of its kind"),
            "settlement_secret": (row("settlement_secret", "settlement", secret_place, created_phase="P1", status="pending", owner_phase="P3"), "may not take a name of the secret stock"),
            "place_unpooled": (row("place_unpooled", "place", "Zarvoth's Hall", created_phase="P1"), "is in no stock of its kind"),
            "region_other": (row("region_other", "region", stock("places")[1], created_phase="P1", status="pending", owner_phase="P3"), "is in no stock of its kind"),
        }
        err = self.refusal({**units, **{k: v[0] for k, v in bad.items()}})
        for eid, (_, line) in bad.items():
            mine = [l for l in err.splitlines() if l.strip().startswith(f"✗ {eid}:")]
            self.assertTrue(any(line in l for l in mine), f"{eid}: {mine}")
            self.assertNotIn(eid, self.merged())
        for name in (secret_person, secret_place, sec("person")[0]):
            self.assertNotIn(name, err, "no refusal line carries a secret-stock name")

    def test_the_prose_scan_and_the_secret_layer(self):
        units = self.units()
        people = self.naming["candidates"]["people"]["names"][0]["name"]
        err = self.refusal(units, public=f"The land is old.\n\nThe {people} answer to the Ashen Tribunal, and nobody else.\n")
        self.assertIn("design/premise.md line 12: the capitalised word 'Ashen' is no pooled or registered name", err)
        self.assertIn("'Tribunal'", err)
        self.assertEqual(self.merged().get(f"premise_{self.slug}"), None)
        # the dm-only prose is scanned against the public and the secret pools: the conductor sees a count
        secret_person = self.secret["languages"]["people"]["person"][0]["name"]
        err = self.refusal(units, mirror=f"The truth is that {secret_person} chose it, with the help of Zarvoth and the Gloomhand.\n")
        self.assertIn("2 capitalised word(s) in the dm-only prose are no pooled or registered name", err)
        self.assertNotIn("Zarvoth", err)
        self.assertNotIn(secret_person, err)
        log = json.loads((self.dir / "design/dm-only/door-log.json").read_text(encoding="utf-8"))["entries"][-1]["found"]
        self.assertEqual([w["word"] for f in log if f["kind"] == "capitalised" for w in f["words"]], ["Zarvoth", "Gloomhand"])
        # no secret row's id or sentence, no secret-stock name, in the public file or a public field
        rolled = json.loads((self.dir / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))
        arch_id = rolled["identity"]["secret"]["keeping"]            # build item 18d: the keeping is rolled in every birth
        arch = dt.row("secrets.yaml#keeping", arch_id)
        err = self.refusal(units, public=f"The land is old; see {arch_id} for more.\n\nNobody knows that {secret_person.lower()} was here; {arch["rule"]}\n".replace(secret_person.lower(), secret_person))
        self.assertIn("names 1 secretly rolled row(s) by id", err)
        self.assertIn("repeats 1 sentence(s) of a secretly rolled row", err)
        self.assertIn("carries 1 name(s) of the secret stock", err)
        for hidden in (arch_id, arch["rule"], arch["label"]):
            self.assertNotIn(hidden, err.replace(f"capitalised word '{secret_person}'", ""), "a refusal line names the kind, never the row")
        bad = copy.deepcopy(units)
        sig = next(e for e in bad if e.startswith("signature_"))
        bad[sig]["summary"] = "a thing the Gloomhand keeps."
        self.assertIn(f"{sig}: field summary: the capitalised word 'Gloomhand'", self.refusal(bad))
        self.stage(units)
        self.assertEqual(set(self.merged()), set(units))

    def test_the_final_set_holds_no_conflict(self):
        self.assertEqual(door.conflict_errors(self.name), ([], []))
        index = dt.conflict_index()
        rolled = [r for r in self.m["dice_log"] if r["phase"] == "P1" and r.get("row_id") and index.get(r["row_id"])]
        victim = rolled[0]["row_id"]
        other = sorted(x for x in index[victim] if not x.startswith("claim:") and ":" not in x)[0]
        m = dm.load(self.name)
        m["dice_log"].append({"phase": "P1", "attempt": 1, "table": "x.yaml", "label": "test", "row_id": other})
        dm.save(self.name, m, "test")
        lines, hidden = door.conflict_errors(self.name)
        self.assertEqual((len(lines), hidden), (1, []))
        self.assertIn(victim, lines[0])
        self.assertIn("conflict", self.refusal(self.units()))
        dm.save(self.name, self.m, "test")
        path = self.dir / "design/dm-only/dice-log.json"
        log = json.loads(path.read_text(encoding="utf-8"))
        log["rolls"].append({"phase": "P1", "attempt": 1, "table": "x.yaml", "label": "test", "row_id": other})
        path.write_text(json.dumps(log), encoding="utf-8")
        lines, hidden = door.conflict_errors(self.name)
        self.assertEqual(lines, ["a conflict in the secret layer (the pair is in the dm-only door log)"])
        self.assertEqual(sorted(hidden[0]["pair"]), sorted([victim, other]))


class ManySeeds(unittest.TestCase):
    """The script-built P1 passes its own door: every candidate and stock name is accepted by the name rules."""

    def test_every_candidate_and_stock_name_is_accepted(self):
        import test_name_pools as tnp
        kinds = {"places": "settlement", "regions": "region", "buildings": "district", "inns": "place", "ships": "place", "sites": "site"}
        checked = 0
        births = tnp.births(tnp.POOL_SEEDS)
        full = {id(b) for scale in ("short", "standard", "epic") for b in [x for x in births if x["dials"]["scale"] == scale][:2]}
        for b in births:
            bag = id(b) in full
            pool = tnp.pooled(b, bag_names=bag)
            secret: dict = {}
            if bag:
                dn.fill_secret(secret, b["naming"], b["master"], b["dials"], "P1", 1, pool, registered=set())
            names = door.Names(None, dict(b["naming"], candidates=b["candidates"]), pool, secret)
            for slot in door.SLOTS:
                for c in b["candidates"][slot]["names"]:
                    checked += 1
                    self.assertEqual(door.name_errors("signature_x", {"type": "signature", "slot": slot, "name": c["name"]}, names, b["identity"]), [])
            for lid, L in pool["languages"].items():
                for key, etype in kinds.items():
                    for e in L.get(key, []):
                        checked += 1
                        self.assertEqual(door.name_errors("x", {"type": etype, "name": e["name"]}, names, b["identity"]), [], f"{key}: {e['name']}")
                for key, etype in (("person", "npc"), ("god", "god")):
                    for e in L.get(key, []):
                        checked += 1
                        self.assertEqual(door.name_errors("x", {"type": etype, "name": e["name"]}, names, b["identity"]), [])
            for lid, L in (secret.get("languages") or {}).items():
                for key, etype in (("person", "npc"), ("god", "god"), ("place", "settlement"), ("site", "site")):
                    for e in L.get(key, []):
                        self.assertEqual(len(door.name_errors("x", {"type": etype, "name": e["name"], "secrecy": "secret"}, names, b["identity"])), 0)
                        self.assertEqual(len(door.name_errors("x", {"type": etype, "name": e["name"]}, names, b["identity"])), 1, "a public entity takes no secret-stock name")
        self.assertGreater(checked, 50000)


class Legacy(unittest.TestCase):

    def test_a_legacy_birth_is_checked_as_it_was(self):
        guard = MarkerGuard().__enter__()
        c = TestCampaign("door")
        try:
            m = dm.load(c.name)
            self.assertFalse(door.applies(m, "P1"), "no foundation, no ledger, no seal: the door stands aside")
            c.run("design_manifest.py", "set-mode", "birth", check=True)
            c.reopen("P5", "running")
            r = row("npc_doorlegacy", "npc", "Quintarro Vale", created_phase="P5")
            c.path("design/npcs").mkdir(parents=True, exist_ok=True)
            c.write_json("design/_staging/P5/npc_doorlegacy.json", fragment("npc_doorlegacy", r))
            proc = c.run("registry.py", "merge", "--phase", "P5")
            self.assertNotIn("capitalised word", proc.stderr)
            self.assertNotIn("preroll stamped", proc.stderr)
        finally:
            c.remove()
            guard.__exit__(None, None, None)


if __name__ == "__main__":
    if "--report" in sys.argv:
        print("capitalised_common:", ", ".join(COMMON))
        words = Counter()
        for birth in sorted(p for p in CAMPAIGNS.glob("_test-*") if (p / "design/entities.json").is_file()):
            ents = json.loads((birth / "design/entities.json").read_text(encoding="utf-8")).get("entities", {})
            for e in ents.values():
                name = str(e.get("name") or "")
                if e.get("type") in ("break", "premise", "arc", "beat", "chapter", "node", "seed", "thread", "socket") or not name.isascii():
                    continue
                for w in door.WORD.findall(name)[1:] if " " in name else []:
                    if w[:1].isupper() and w not in COMMON:
                        words[w] += 1
        print(f"capitalised words inside the archived births' public multi-word names (a word, its count; {sum(words.values())} in all, {len(words)} distinct):")
        print("  " + ", ".join(f"{w} {n}" for w, n in words.most_common(60)))
    else:
        unittest.main()
