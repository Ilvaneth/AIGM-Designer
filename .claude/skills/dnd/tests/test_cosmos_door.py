"""
test_cosmos_door.py — build item 22c (docs/p2-build-22.md part 22c): P2 keeps its promises. On a `_test-` campaign
whose P1 the stand-ins of the P1 dry walk wrote and approved: P2's preroll adds its rows to the ledger and seals the
cosmos; `phase P2 begin` writes the frame; a stand-in writer fills it and the door passes it; each refusal by name;
P1's promises due at P2 close (the pinned god on the pinned seat's god, the move dated); a P2 promise to P3 stands in
the ledger. The merge reserves a pooled name a row holds as a field's value, at P1 too.

The stand-in writer invents nothing: it copies every framed row and fills its text fields with plain words.
"""

import copy
import json
import shutil
import sys
import unittest

from _campaign import SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_cosmos_door as cd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_promises as dp  # noqa: E402
from design_io import is_fragment  # noqa: E402
import test_p1_dry_walk as walk  # noqa: E402

TEXT = "a plain line the stand-in writer wrote"


def fill(entry: dict) -> dict:
    """A framed row with its text fields filled (a stand-in writer's work)."""
    row = copy.deepcopy(entry["registry"])
    for f in entry["fill"]:
        head, _, rest = f.partition(".")
        if f in ("aliases", "refs") or head in ("aliases", "refs"):
            continue
        if rest:
            row.setdefault(head, {})[rest] = TEXT
        else:
            row[f] = TEXT
    return row


class P2Walk:
    """A `_test-` campaign: P1 walked and approved, P2 prerolled and begun."""

    def __init__(self, scale: str, seed: str):
        self.w = walk.Walker(scale, seed).born().write()
        w = self.w
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "check")
        w.critics()
        w.d("phase", "P1", "merge")
        w.d("phase", "P1", "approve")
        self.preroll = w.d("preroll", "--phase", "P2")
        self.begin = w.d("phase", "P2", "begin", "--json")
        self.staging = w.dir / "design/_staging/P2"
        self.frame = w.json(cd.frame_rel())

    def write(self, change=None, prose_extra: str = "") -> dict:
        w, frame = self.w, self.frame
        rows = {eid: fill(e) for eid, e in cd.framed_rows(frame).items()}
        c = frame["container"]
        cal = copy.deepcopy(c["calendar"])
        cal["seasons"] = TEXT
        frag = {"schema_version": 1, "id": cd.UNIT, "type": "document", "phase": "P2", "attempt": 1, "agent": "P2.cosmos.a1",
                "mode": "birth", "container": True, "registry": None, "prose": {"file": cd.PROSE}, "dm_only_prose": {"file": cd.DM_PROSE},
                "notes": None, "rows": list(rows.values()), "graph": {"nodes": [], "edges": []}, "seeds": copy.deepcopy(c["seeds"]),
                "calendar": cal, "counts": {}, "status": "staged"}
        if change:
            change(frag)
        covers = ", ".join(r["id"] for r in frag["rows"] if r.get("secrecy") != "secret")
        public = (f"---\nentity: none\ntype: cosmology\nsecrecy: public\nphase: P2\nstamped: []\ncovers: [{covers}]\n"
                  f"mirror: {cd.DM_PROSE}\n---\n\n# Cosmology\n\nthe gods are many and they quarrel.\n{prose_extra}\n")
        hidden = ", ".join(r["id"] for r in frag["rows"] if r.get("secrecy") == "secret")
        mirror = (f"---\nentity: none\ntype: cosmology\nsecrecy: secret\nphase: P2\nstamped: []\n"
                  + (f"covers: [{hidden}]\n" if hidden else "") + f"mirror_of: {cd.PROSE}\n---\n\n"
                  "the truth of the cosmos is written here.\n")
        (w.dir / cd.PROSE).write_text(public, encoding="utf-8", newline="\n")
        (w.dir / cd.DM_PROSE).write_text(mirror, encoding="utf-8", newline="\n")
        self.staging.mkdir(parents=True, exist_ok=True)
        for f in self.staging.glob("*.json"):
            if is_fragment(f):
                f.unlink()
        (self.staging / f"{cd.UNIT}.json").write_text(json.dumps(frag, ensure_ascii=False), encoding="utf-8")
        return frag

    def merge(self, check=False):
        return self.w.d("phase", "P2", "merge", check=check)


class Door(unittest.TestCase):
    """The frame, the door's refusals by name and the ledger, on one standard birth."""

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        if USED.is_file():
            USED.unlink()
        cls.p2 = P2Walk("standard", "COSMOS-PIN-17")       # a seed whose P1 pins a god (the threat is a god)
        cls.snapshot = cls.p2.w.dir.parent / (cls.p2.w.name + ".snap")
        shutil.copytree(cls.p2.w.dir, cls.snapshot)

    @classmethod
    def tearDownClass(cls):
        cls.p2.w.remove()
        shutil.rmtree(cls.snapshot, ignore_errors=True)
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def setUp(self):
        # every test starts from the state after begin
        shutil.rmtree(self.p2.w.dir, ignore_errors=True)
        shutil.copytree(self.snapshot, self.p2.w.dir)

    def refused(self, proc) -> str:
        self.assertIn("✗", proc.stderr, proc.stdout[-500:])
        return proc.stderr

    def test_the_preroll_seals_and_extends_the_ledger(self):
        m = dm.load(self.p2.w.name)
        self.assertTrue(m.get(cd.SEAL))
        self.assertIn("designer: promises — ", self.p2.preroll.stdout)
        p2 = [p for p in m["promises"] if any(s["from_phase"] == "P2" for s in dp.sources(p))]
        self.assertTrue(p2, "P2's rows are sources")
        self.assertTrue(any(p["due"] == "P3" for p in p2), "a P2 promise to P3 stands in the ledger")
        self.assertFalse([p for p in p2 if p["source"] == "hook" and p["due"] in ("P0", "P1", "P2")], "only forward hooks")
        self.assertTrue((self.p2.w.dir / cd.frame_rel()).is_file(), "begin wrote the frame")

    def test_the_stand_in_writer_passes_and_p1s_p2_promises_close(self):
        self.p2.write()
        proc = self.p2.merge()
        self.assertNotIn("✗", proc.stderr, proc.stderr[-2500:])
        merged = self.p2.w.merged()
        self.assertLessEqual(set(cd.framed_rows(self.p2.frame)), set(merged))
        check = self.p2.w.d("phase", "P2", "check")
        m = dm.load(self.p2.w.name)
        due = [p for p in m["promises"] + dp.load_secret(self.p2.w.name) if p["check"] != "critic" and p["due"] == "P2"]
        self.assertTrue(due, check.stdout)
        self.assertEqual([p["text"] for p in due if p["status"] != "kept"], [], "every script promise due at P2 is kept")
        placed = [p for p in dp.load_secret(self.p2.w.name) if p["source"] == "placement" and p["due"] == "P2"]
        self.assertTrue(placed and all(p["status"] == "kept" for p in placed), "the premise's god and event are in the history")

    def test_the_pinned_name_is_the_pinned_gods_true_name_only(self):
        """The 22c audit: a pinned god is named from the secret stock; the name is that god's true name in dm-only, and
        the god's public face is the gods' next name, so nothing public moves with the pin."""
        m = dm.load(self.p2.w.name)
        canon = self.p2.w.merged()
        premise = next(r for r in canon.values() if r["type"] == "premise")
        pinned = ((premise.get("dm_only") or {}).get("pinned") or {}).get("god")
        self.assertTrue(pinned, "the seed pins a god")
        secret_stock = {e["name"] for L in self.p2.w.json("design/dm-only/name-pool-secret.json")["languages"].values() for e in L.get("god", [])}
        self.assertIn(pinned, secret_stock, "P1 pins a secret-stock name")
        cosmos_secret = self.p2.w.json("design/dm-only/dice-log.json")["cosmos"]
        seat = cosmos_secret["seats"]["threat_god"] or cosmos_secret["seats"]["power_god"]
        self.assertEqual(cosmos_secret["hidden_names"][str(seat)], pinned)
        self.assertNotIn(pinned, json.dumps(m), "the true name is in no public record")
        god = next(g for g in m["cosmos"]["gods"] if g["n"] == seat)
        self.assertEqual(self.p2.frame["rows"][god["id"]]["registry"]["dm_only"]["true_name"], pinned)
        langs = {g["lang"] for g in m["cosmos"]["gods"]}
        self.assertEqual(len(langs), 1, "every god is named in one language, the pinned one too")

    def test_each_refusal_by_name(self):
        frame = self.p2.frame
        god = next(e for e in frame["rows"] if e.startswith("god_"))
        event_move = next(e for e, x in frame["rows"].items() if x["registry"].get("seat") == "move")
        plane = next(e for e in frame["rows"] if e.startswith("plane_"))
        cases = {
            "a frame field changed": (lambda f: next(r for r in f["rows"] if r["id"] == god).update(rank="power"), "`rank` differs"),
            "a framed row left out": (lambda f: f.__setitem__("rows", [r for r in f["rows"] if r["id"] != event_move]), f"the framed row {event_move} is missing"),
            "a seated event dropped": (lambda f: f.__setitem__("rows", [r for r in f["rows"] if r["id"] != event_move]), "four seated story events"),
            "a festival missing": (lambda f: f["calendar"].__setitem__("festivals", [x for x in f["calendar"]["festivals"] if x["god"] is None]), "has no festival"),
            "the month changed": (lambda f: f["seeds"][0]["args"].__setitem__("month_length", 30), "`seeds` must be the calendar seed"),
            "a reshaped stamp": (lambda f: next(r for r in f["rows"] if r["id"] == god).__setitem__("stamped", "rank"), "`stamped` must be an object"),
            "an extra god": (lambda f: f["rows"].append(dict(next(r for r in f["rows"] if r["id"] == god), id="god_extra")), "no such god"),
            # build item 22n: every name comes from the pool; the writer neither blanks nor renames one
            "a plane renamed": (lambda f: next(r for r in f["rows"] if r["id"] == plane).update(name="the Invented Realm"), "`name` differs"),
            "an event left nameless": (lambda f: next(r for r in f["rows"] if r["id"] == event_move).update(name=""), "`name` differs"),
            "a festival renamed": (lambda f: f["calendar"]["festivals"][0].update(name="the Invented Feast"), "`calendar.festivals"),
        }
        for what, (change, words) in cases.items():
            with self.subTest(what):
                self.setUp()
                self.p2.write(change)
                self.assertIn(words, self.refused(self.p2.merge()), what)

    def test_a_secret_word_in_the_public_prose_is_refused(self):
        log = self.p2.w.json("design/dm-only/dice-log.json")
        p1_secret = next(r["row_id"] for r in log["rolls"] if r.get("phase") == "P1" and r.get("row_id") and ".yaml" in str(r.get("table")))
        self.p2.write(prose_extra=f"the {p1_secret} stands here.")
        err = self.refused(self.p2.merge())
        self.assertIn("a secretly rolled row's id", err)
        self.assertNotIn(p1_secret, err, "the refusal names the kind, never the row")

    def test_every_name_comes_from_the_pool_and_is_reserved_under_its_id(self):
        """Build item 22n: the frame names every plane, age, event, festival and the moon from the pool's cosmos section;
        each name is reserved there under the id that carries it; a frame with a nameless row is refused."""
        frame = self.p2.frame
        pool = self.p2.w.json("design/dm-only/name-pool.json")
        held = {e["name"]: e.get("used_by") for v in pool["cosmos"].values() for e in v}
        for eid, entry in frame["rows"].items():
            name = entry["registry"]["name"]
            self.assertTrue(name, f"{eid} is named")
            self.assertNotIn("name", entry["fill"], f"{eid}: the writer fills no name")
            if eid.startswith("plane_"):
                self.assertEqual(held.get(name), eid, f"{eid}'s name is reserved under its id")
        block = frame["container"]["calendar"]
        for f in block["festivals"]:
            self.assertEqual(held.get(f["name"]), f"calendar.festival.{f['n']}")
        self.assertEqual(cd.name_errors(frame), [])
        nameless = copy.deepcopy(frame)
        eid = next(e for e in nameless["rows"] if e.startswith("era_"))
        nameless["rows"][eid]["registry"]["name"] = ""
        self.assertEqual(cd.name_errors(nameless), [f"{eid}: the pool gave it no name; rerun the P2 preroll (every name P2 makes comes from the pool)"])
        names = [entry["registry"]["name"].lower() for entry in frame["rows"].values() if not entry["registry"]["id"].startswith("god_")]
        names += [f["name"].lower() for f in block["festivals"]] + [n.lower() for n in block["moon"]["names"]]
        self.assertEqual(len(names), len(set(names)), "no two names of the campaign collide")

    def test_an_edited_cosmos_breaks_the_seal(self):
        m = dm.load(self.p2.w.name)
        m["cosmos"]["counts"]["gods"] += 1
        dm.save(self.p2.w.name, m, "test")
        self.p2.write()
        self.assertIn("design.json#cosmos differs", self.refused(self.p2.merge()))


class EpicHome(unittest.TestCase):
    """At epic the threat's home of its own is a secret row with an opaque id (option d of 22b; the 22c audit): framed,
    promised to P6 in the secret ledger, merged through the door, and named by nothing the conductor reads."""

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        if USED.is_file():
            USED.unlink()
        cls.p2 = P2Walk("epic", "COSMOS-HOME-1")       # a seed whose threat's home is no touched plane

    @classmethod
    def tearDownClass(cls):
        cls.p2.w.remove()
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def test_the_home_of_its_own_stays_secret(self):
        w = self.p2.w
        home = w.json("design/dm-only/dice-log.json")["cosmos"]["home_plane"]
        self.assertTrue(home and home["own"], "the seed's home is a plane of its own")
        self.assertEqual(list(self.p2.frame["secret_rows"]), [cd.HOME_ID])
        self.assertEqual(self.p2.frame["secret_rows"][cd.HOME_ID]["registry"]["secrecy"], "secret")
        placed = [p for p in dp.load_secret(w.name) if p.get("kind") == "home_plane"]
        self.assertEqual([(p["due"], p["source"]) for p in placed], [("P6", "placement")])
        self.assertFalse([p for p in dm.load(w.name)["promises"] if p.get("kind") == "home_plane"], "never in the public ledger")
        self.p2.write()
        merge = self.p2.merge()
        self.assertNotIn("✗", merge.stderr, merge.stderr[-2000:])
        self.assertIn(cd.HOME_ID, w.merged())
        short = home["baseline"].removeprefix("baseline_")
        outputs = merge.stdout + merge.stderr + w.d("phase", "P2", "check").stdout + w.d("phase", "P2", "report", check=False).stdout
        self.assertNotIn(home["baseline"], outputs)
        self.assertNotIn(f"plane_{short}", outputs.replace(f"plane_{short}_", ""), "the home's id names nothing")
        public = json.dumps(dm.load(w.name)) + (w.dir / cd.PROSE).read_text(encoding="utf-8")
        self.assertNotIn(home["baseline"], public, "the opaque id may stand in public; what it is may not")
        # build item 22n: its name comes from the secret stock, reserved under its opaque id, and stands nowhere public
        name = self.p2.frame["secret_rows"][cd.HOME_ID]["registry"]["name"]
        secret = {e["name"]: e["used_by"] for e in w.json("design/dm-only/name-pool-secret.json")["cosmos"]["planes"]}
        self.assertEqual(secret.get(name), cd.HOME_ID)
        self.assertNotIn(name, public + json.dumps(w.json("design/dm-only/name-pool.json")))


class Reserve(unittest.TestCase):
    """One rule at every merge: a pooled name a row holds as a field's whole value is reserved under that row; a name in
    prose is not."""

    def test_a_field_value_is_reserved_and_prose_is_not(self):
        import design_names as dn
        pool = {"languages": {"common": {"god": [{"name": "Arvelin", "used_by": None}, {"name": "Tessaro", "used_by": None}],
                                         "person": [{"name": "Morwick", "used_by": None}]}}}
        row = {"id": "premise_x", "type": "premise", "summary": "Morwick will speak of Tessaro", "dm_only": {"pinned": {"god": "Arvelin"}}}
        self.assertEqual(dn.reserve_named(pool, None, row, "premise_x"), 1)
        names = {e["name"]: e["used_by"] for L in pool["languages"].values() for v in L.values() for e in v}
        self.assertEqual(names, {"Arvelin": "premise_x", "Tessaro": None, "Morwick": None})


if __name__ == "__main__":
    unittest.main()
