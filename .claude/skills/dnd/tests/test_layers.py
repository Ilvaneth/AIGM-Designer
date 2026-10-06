"""
test_layers.py — build item 18a (docs/p1-build-18.md, Part 18a; docs/p1-threat-first.md, "The layers"): every P0 and
P1 table carries a layer; the story slots are one constant; a story slot takes a story or a stage piece only, at the
roll (the arbiter), at the set (the foundation) and at the door (a writer's structured field); 3,000 seeds hold no
texture piece in a story slot and empty no pool; the lifeline is no target and no prize and is rolled last; a legacy
birth with the old target and a retired contest loads and renders.
"""

import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_door as door  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402
import _corpus  # noqa: E402  (build item 18f-1: the shared many-seed corpus)

SEEDS = 3000
SPAN = {"short": 4, "standard": 11, "epic": 19}
SLOTS = {"move_target", "contest_prize", "goal_piece", "lair_where", "world_state_tie", "escalation_step", "clue_place",
         "secret_pin"}      # build item 18e: the pin is a piece of the chain when no god is pinned


class Layers(unittest.TestCase):

    def test_every_p0_and_p1_table_has_a_layer(self):
        refs = dt.layered_refs()
        self.assertGreaterEqual(len(refs), 30)
        for ref in refs:
            with self.subTest(ref=ref):
                self.assertIn(dt.layer(ref), dt.LAYERS)

    def test_the_layers_of_the_specification(self):
        want = {"dials.yaml#scale": "frame", "dials.yaml#tone": "frame", "dials.yaml#magic": "frame",
                "dials.yaml#danger": "frame", "dials.yaml#content_mix": "frame", "dials.yaml#era": "stage",
                "foundation.yaml#spine": "stage", "foundation.yaml#ruin_source": "story", "foundation.yaml#contest": "story",
                "foundation.yaml#break_target": "story", "foundation.yaml#action": "story", "foundation.yaml#time": "story",
                "foundation.yaml#escalation_tier": "story", "foundation.yaml#palette": "texture",
                "foundation.yaml#lifeline": "texture", "foundation.yaml#scar": "texture", "tensions.yaml": "story",
                "trope-breaks.yaml": "texture", "trope-breaks.yaml#tie": "texture", "naming.yaml#family": "texture"}
        for ref, layer in want.items():
            self.assertEqual(dt.layer(ref), layer, ref)
        for ref in dt.layered_refs():
            if ref.startswith("signatures.yaml"):
                self.assertEqual(dt.layer(ref), "texture", ref)
            if ref.startswith(("antagonists.yaml", "secrets.yaml")):
                self.assertEqual(dt.layer(ref), "story")    # the counts only: no row of these tables is named here

    def test_a_row_may_carry_its_own_layer(self):
        """18b's world states say `layer: story` on their rows; the row's own layer comes first."""
        row = dt.rows("trope-breaks.yaml")[0]
        self.assertEqual(dt.layer("trope-breaks.yaml", row["id"]), row.get("layer") or "texture")
        self.assertEqual(dt.ref_of_row("life_snowmelt"), "foundation.yaml#lifeline")
        self.assertEqual(dt.ref_of_row("target_lifeline"), "foundation.yaml#break_target", "a retired row is found")


class Slots(unittest.TestCase):

    def test_the_slot_constant(self):
        self.assertEqual(set(arb.STORY_SLOTS), SLOTS)
        self.assertEqual(arb.SLOT_LAYERS, {"story", "stage"})

    def test_the_pieces(self):
        for piece in ("heart", "key_place", "thin_place", "disputed_land", "remnant", "role", "seat", "new"):
            self.assertIn(arb.piece_layer(piece), ("story", "stage"), piece)
        for piece in ("lifeline", "scar", "people", "institution", "phenomenon", "life_snowmelt", "scar_new_people"):
            self.assertEqual(arb.piece_layer(piece), "texture", piece)
        self.assertEqual(arb.piece_layer(dt.rows("foundation.yaml#spine")[0]["id"]), "stage")
        self.assertEqual(arb.piece_layer(dt.rows("foundation.yaml#contest")[0]["id"]), "story")
        self.assertIsNone(arb.piece_layer("no_such_piece"))

    def test_the_arbiter_refuses_a_texture_piece_in_each_slot(self):
        rows = [{"id": "x_story", "label": "a story piece", "piece": "heart"},
                {"id": "x_texture", "label": "a texture piece", "piece": "lifeline"},
                {"id": "x_prize", "label": "a prize of texture", "prize": "remnant", "prize_with": {"ruin_x": "lifeline"}}]
        for slot in SLOTS:
            with self.subTest(slot=slot):
                res = arb.arbitrate("_test.yaml", rows, arb.Context(), slot=slot, conflicts={}, secret_ids=())
                self.assertEqual([r["id"] for r in res["pool"]], ["x_story"])
                why = {e["row"]: e["why"] for e in res["excluded"]}
                self.assertEqual(why, {"x_texture": "texture_in_slot", "x_prize": "texture_in_slot"})
                with self.assertRaises(arb.EmptyPool):
                    arb.arbitrate("_test.yaml", rows[1:2], arb.Context(), slot=slot, conflicts={}, secret_ids=())
                self.assertEqual(arb.slot_errors([(slot, "heart"), (slot, "remnant")]), [])
                self.assertEqual(len(arb.slot_errors([(slot, "lifeline"), (slot, "life_snowmelt"), (slot, "heart")])), 2)
        res = arb.arbitrate("_test.yaml", rows, arb.Context(), conflicts={}, secret_ids=())
        self.assertEqual(len(res["pool"]), 3, "a draw that fills no slot is not judged by layer")

    def test_the_foundation_refuses_a_set_that_holds_one(self):
        """The set check after the roll: a texture prize (a legacy table) stops the preroll as a table fault."""
        d = {"scale": "standard", "magic": "medium", "era": "medieval", "tone": "bright",
             "content_mix": ["war", "mystery", "horror"], "level_band": [1, 12]}
        R = designer.Roller.in_memory("LAYER-SET", d)
        out = fd.roll(R, d)
        f = fd.build(out, d["level_band"])
        self.assertEqual(arb.slot_errors(fd.slots(f)), [])
        f["layout"]["contests"][0]["prize"]["kind"] = "lifeline"
        f["break"]["target"] = "target_lifeline"
        self.assertEqual(len(arb.slot_errors(fd.slots(f))), 2)

    def test_the_door_refuses_a_texture_piece_in_a_story_field(self):
        """18e names the fields; the rule stands now, judged on any field it is given."""
        fields = {("premise", "dm_only.clues.place"): "clue_place", ("premise", "dm_only.pinned.piece"): "clue_place"}
        row = {"type": "premise", "dm_only": {"clues": [{"place": "remnant"}, {"place": "life_snowmelt"}, {"place": None}],
                                              "pinned": {"piece": "lifeline"}}}
        errs = door.story_field_errors("premise_x", row, fields)
        self.assertEqual(len(errs), 2, errs)
        self.assertTrue(all("takes a story or a stage piece" in e for e in errs))
        self.assertEqual(door.story_field_errors("sig_x", dict(row, type="signature"), fields), [])
        self.assertEqual(door.STORY_FIELDS, {("premise", "dm_only.clues.piece"): "clue_place", ("premise", "dm_only.pinned.piece"): "secret_pin"},
                         "build item 18e names the fields")


class ManySeeds(unittest.TestCase):
    """3,000 seeds over every scale × magic × era (and the tones and content mixes): no story slot holds a texture
    piece, no pool is empty (an empty pool stops the roll), the lifeline comes after the story."""

    @classmethod
    def setUpClass(cls):
        cls.found, cls.pools, cls.kinds, cls.targets = [], {}, {}, {}
        for d, R in _corpus.births(SEEDS):           # the shared corpus (build item 18f-1)
            f = R.foundation
            labels = [r["label"] for r in R.public]
            cls.found.append((d, f, labels))
            for ref, n in R.pools.items():
                cls.pools[ref] = min(cls.pools.get(ref, n), n)
            for slot, piece in fd.slots(f):
                cls.kinds.setdefault(slot, {}).setdefault(piece, 0)
                cls.kinds[slot][piece] += 1

    def test_no_texture_piece_in_a_story_slot(self):
        self.assertEqual(len(self.found), SEEDS)
        bad = [(d["scale"], e) for d, f, _ in self.found for e in arb.slot_errors(fd.slots(f))]
        self.assertEqual(bad, [])
        self.assertNotIn("lifeline", self.kinds["move_target"])
        self.assertNotIn("lifeline", self.kinds["contest_prize"])

    def test_every_new_prize_kind_is_drawn(self):
        self.assertTrue({"key_place", "disputed_land", "seat", "heart", "remnant", "new", "thin_place"} <= set(self.kinds["contest_prize"]),
                        self.kinds["contest_prize"])

    def test_no_pool_runs_dry(self):
        for ref, n in self.pools.items():
            self.assertGreater(n, 0, ref)
        self.assertGreaterEqual(self.pools["foundation.yaml#contest"], 20, "the contest pool after the key-place kinds")

    def test_a_key_place_prize_fits_the_spine(self):
        """The owner's correction at the 18a audit: a key-place prize stands on a key place of its kinds."""
        contests, spines = fd.rows_by_id("contest"), fd.rows_by_id("spine")
        seen = 0
        for d, f, _ in self.found:
            for c in f["layout"]["contests"]:
                if c["prize"]["kind"] == "key_place":
                    seen += 1
                    self.assertIn(spines[f["spine"]]["key_kind"], contests[c["contest"]]["key_kinds"])
        self.assertGreater(seen, 100)

    def test_the_lifeline_comes_last(self):
        for d, f, labels in self.found:
            life = labels.index("foundation.lifeline")
            self.assertFalse([x for x in labels[life:] if x.startswith(("foundation.contest", "foundation.break.", "foundation.ruin",
                                                                         "foundation.spine"))])

    @classmethod
    def report(cls) -> str:
        lines = [f"{SEEDS} seeds; the smallest pools: " + ", ".join(f"{r.split('#')[-1]} {n}" for r, n in sorted(cls.pools.items()))]
        for slot, kinds in cls.kinds.items():
            total = sum(kinds.values())
            lines.append(f"{slot}: " + ", ".join(f"{k} {100 * v / total:.1f} %" for k, v in sorted(kinds.items(), key=lambda kv: -kv[1])))
        return "\n".join(lines)


def run(script, *args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True,
                          env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout[-1500:]}\n{proc.stderr[-1500:]}")
    return proc


class LegacyBirth(unittest.TestCase):
    """A birth rolled before 18a: its break struck the lifeline and its contest was a retired one with the lifeline
    as its prize. It loads, its card and its writer's prompt render, its ledger reads it."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-legacy18a-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run("designer.py", "new", self.name, "--party-size", "2", "--seed", "LEGACY-18A", "--lang", "tr", "--scale", "standard")
        run("designer.py", "-c", self.name, "preroll", "--phase", "P1")
        m = dm.load(self.name)
        f = m["foundation"]
        f["break"]["target"] = "target_lifeline"
        f["layout"]["break_at"] = f["layout"]["lifeline"]
        main = f["contests"][0]
        main["id"] = f["layout"]["contests"][0]["contest"] = "contest_split_family"
        f["layout"]["contests"][0]["prize"] = {"kind": "lifeline", "at": f["layout"]["lifeline"]}
        dm.save(self.name, m, "test: a legacy foundation")

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_it_loads_and_renders(self):
        m = dm.load(self.name)
        self.assertEqual(fd.PIECE_OF_TARGET[m["foundation"]["break"]["target"]], "lifeline")
        self.assertEqual(fd.rows_by_id("contest")["contest_split_family"]["prize"], "lifeline")
        out = {"spine": m["foundation"]["spine"], "ruin": m["foundation"]["ruin_source"], "lifeline": m["foundation"]["lifeline"]["id"],
               "target": "target_lifeline", "contests": m["foundation"]["contests"]}
        self.assertTrue(fd.target_phrase(out))
        begin = run("designer.py", "-c", self.name, "phase", "P1", "begin", "--json")
        prompt = json.loads(begin.stdout[begin.stdout.index("{"):])["entities"][0]["prompt_file"]
        self.assertTrue(os.path.isfile(prompt))
        run("designer.py", "-c", self.name, "phase", "P1", "card")
        card = (CAMPAIGNS / self.name / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        self.assertIn("THE FOUNDATION", card.upper())
        import design_promises as dp
        self.assertTrue(dp.place_text(m["foundation"], m["foundation"]["layout"]["contests"][0]["prize"]["at"]))


if __name__ == "__main__":
    if "--report" in sys.argv:
        ManySeeds.setUpClass()
        print(ManySeeds.report())
    else:
        unittest.main()
