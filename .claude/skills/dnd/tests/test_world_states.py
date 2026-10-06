"""
test_world_states.py — build item 18b (docs/p1-build-18.md, Part 18b; docs/p1-build-18-rows.md sections 6 and 7): the
eight world-state trope breaks are story and join a story piece (never drawn without one, never tied to the lifeline,
a join to the threat kept in dm-only); the two bent rows; the P8 hook on the rows that touch the players; the palette's
count by the spine's breadth at every scale; a legacy birth's palette loads.
"""

import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid
from collections import Counter

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_identity as di  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402
import _corpus  # noqa: E402  (build item 18f-1: the shared many-seed corpus)

SEEDS = 3000
SPAN = {"short": 4, "standard": 11, "epic": 19}
BREAKS = {r["id"]: r for r in dt.rows("trope-breaks.yaml")}
WORLD = {"break_rule_by_lottery", "break_no_kings_only_guilds", "break_magic_is_nobility", "break_dragons_rule",
         "break_beasts_own_land", "break_moon_trades", "break_gods_among_mortals", "break_the_enemy_won"}
P8 = "the player files and character creation state it"
TIGHT = {"spine_lone_mountain", "spine_giant_tree", "spine_three_depths", "spine_mountain_within", "spine_oasis_ring",
         "spine_star_crater", "spine_void_ring", "spine_titan_back", "spine_floating_archipelago", "spine_terraces",
         "spine_lake_basin", "spine_forest_clearings", "spine_mesa_land", "spine_valley_maze", "spine_above_below_sea"}


class Rows(unittest.TestCase):

    def test_the_eight_world_states(self):
        self.assertEqual({k for k, r in BREAKS.items() if r.get("layer") == "story"}, WORLD)
        self.assertEqual(len(BREAKS) - len(WORLD), 28, "the other 28 are rules of life, texture")
        for rid in WORLD:
            with self.subTest(row=rid):
                self.assertEqual(dt.layer("trope-breaks.yaml", rid), "story")
                self.assertTrue(BREAKS[rid]["joins"])
                for j in BREAKS[rid]["joins"]:
                    self.assertTrue(j["how"])
                    self.assertTrue(arb.slot_accepts("world_state_tie", j["piece"]), j)
                    self.assertEqual(len({"always", "any_of", "prize", "people_side", "palette", "ruin_family", "threat", "hand", "ruins"} & set(j)), 1, j)
                self.assertFalse(arb._condition_ids([w["when"] for w in BREAKS[rid].get("weight_by") or []]) & {r["id"] for r in dt.rows("foundation.yaml#lifeline")},
                                 "no lifeline weighs a world state")
        self.assertFalse(any(r.get("joins") for k, r in BREAKS.items() if k not in WORLD))
        self.assertEqual([j["piece"] for j in BREAKS["break_dragons_rule"]["joins"]], ["contest", "hand", "ruin_source", "threat"],
                         "build item 18c-2: the dragon hand and the dragons' ruins")
        self.assertEqual({BREAKS[k].get("weight") for k in ("break_dragons_rule", "break_gods_among_mortals")}, {3})
        self.assertEqual(BREAKS["break_gods_among_mortals"]["joins"][0]["scales"], ["standard", "epic"], "no god family at short")
        self.assertEqual(BREAKS["break_the_enemy_won"]["joins"][0]["ruin_family"], ["wars", "fallen_kingdoms"])

    def test_the_two_bent_rows(self):
        w, g = BREAKS["break_no_writing"], BREAKS["break_divine_magic_holy_ground"]
        self.assertEqual(w["label"], "Writing is sacred")
        self.assertEqual(w["statement"], "Only the ordained may write; a caster writes their own spellbook and scrolls by right "
                                         "of the art; letters, maps and records are an ordained hand's work, and everything else lives in memory.")
        self.assertTrue(w["text"]["at_table"].startswith("a wizard keeps their spellbook and scrolls by right of the art"))
        self.assertEqual(g["label"], "Divine magic is strongest on holy ground")
        self.assertIn("keeps every feature", g["text"]["at_table"])
        self.assertNotIn("only", g["text"]["name"])
        for r in (w, g):
            self.assertIn(P8, [h["must"] for h in r["hooks"] if h["phase"] == "P8"])

    def test_the_rows_that_touch_the_players(self):
        """docs/reports/item18-fits.md, list 2: the fifteen, and three more at the 18b audit (maps, dreams, the gods among
        mortals); night, the border, magic sold and the chosen (P9's) carry none."""
        have = {k for k, r in BREAKS.items() if any(h["must"] == P8 for h in r["hooks"])}
        self.assertEqual(have, {"break_weapons_one_class", "break_magic_is_nobility", "break_lineage_homes_inverted",
                                "break_god_name_forbidden", "break_divine_magic_holy_ground", "break_underground_forbidden",
                                "break_ruins_forbidden", "break_dead_month", "break_iron_is_sacred", "break_no_direct_lies",
                                "break_no_writing", "break_no_common_tongue", "break_casting_forbidden", "break_dead_rise",
                                "break_oath_curse", "break_maps_are_illegal", "break_dreams_are_a_place", "break_gods_among_mortals"})
        for rid in ("break_night_forbidden", "break_border_forbidden", "break_magic_sold", "break_chosen_are_many"):
            self.assertNotIn(rid, have)
        self.assertNotIn("prohibition", BREAKS["break_no_common_tongue"])
        self.assertTrue(BREAKS["break_casting_forbidden"]["prohibition"], "casting is forbidden stays as it is")

    def test_the_palette_counts_by_spine(self):
        head = dt.roll_header("foundation.yaml#palette")
        self.assertNotIn("count_by_scale", head)
        self.assertEqual(head["count_by_spine"], {"tight": {"short": [2, 3], "standard": [3, 4], "epic": [4, 5]},
                                                  "wide": {"short": [3, 4], "standard": [4, 6], "epic": [6, 8]}})
        spines = dt.rows("foundation.yaml#spine")
        self.assertEqual(len(spines), 30)
        self.assertEqual({s["id"] for s in spines if s["breadth"] == "tight"}, TIGHT)
        self.assertEqual(Counter(s["breadth"] for s in spines), {"tight": 15, "wide": 15})


class ManySeeds(unittest.TestCase):
    """3,000 seeds over every scale × magic × era × tone: no world state without a join, no world state tied to the
    lifeline, a threat join only in dm-only, every palette inside its spine's band but for the needs."""

    @classmethod
    def setUpClass(cls):
        # the shared corpus (build item 18f-1); the roll's raw output is no longer kept, and no test here reads it
        cls.runs = [(d, R, None, R.foundation, R.identity) for d, R in _corpus.births(SEEDS)]

    def test_no_world_state_without_a_join(self):
        drawn = Counter()
        import design_threat as dth
        for d, R, out, f, ident in self.runs:
            self.assertNotIn("world_state_secret", ident)
            for b in ident["trope_breaks"]:
                if b["id"] not in WORLD:
                    self.assertNotIn("join", b)
                    continue
                drawn[b["id"]] += 1
                self.assertNotEqual(b["tie"], "tie_lifeline", "a world state is never tied to the lifeline")
                self.assertIn("join", b, "every world state's join is public (the 18c-1 audit)")
                if b["join"]["piece"] == "threat":
                    self.assertIn(R.threat["visibility"], dth.PUBLIC_VISIBILITY, "the villain itself is public")
                self.assertTrue(arb.slot_accepts("world_state_tie", b["join"]["piece"]))
                if b["id"] == "break_gods_among_mortals" and d["scale"] == "short":
                    self.assertIn(b["join"]["piece"], ("contest", "ruin_source"), "at short no god family: a faith contest or a gods' ruin")
                if b["id"] == "break_beasts_own_land":
                    self.assertIn(b["join"]["piece"], ("disputed_land", "role"))
        self.assertEqual(set(drawn), WORLD, "every world state is still drawn")
        type(self).drawn = drawn

    @classmethod
    def report(cls) -> str:
        cls.setUpClass()
        drawn = Counter(b["id"] for *_, ident in cls.runs for b in ident["trope_breaks"] if b["id"] in WORLD)
        pieces = Counter((b["id"], b["join"]["piece"]) for *_, ident in cls.runs for b in ident["trope_breaks"] if b["id"] in WORLD)
        return "\n".join([f"{SEEDS} seeds; births with a world state: {sum(1 for *_, i in cls.runs if any(b['id'] in WORLD for b in i['trope_breaks']))}"]
                         + [f"  {k}: {v} ({', '.join(f'{p} {n}' for (r, p), n in sorted(pieces.items()) if r == k)})" for k, v in sorted(drawn.items())])

    def test_the_palette_counts_by_spine_at_every_scale(self):
        head = dt.roll_header("foundation.yaml#palette")["count_by_spine"]
        spines = fd.rows_by_id("spine")
        counts, over = {}, 0
        for d, R, out, f, ident in self.runs:
            br = spines[f["spine"]]["breadth"]
            lo, hi = head[br][d["scale"]]
            count = R.by_label["foundation.palette_count"]["value"]
            self.assertTrue(lo <= count <= hi, (f["spine"], d["scale"], count))
            counts.setdefault((br, d["scale"]), set()).add(count)
            scar = sum(1 for r in R.public if r["label"] == "foundation.palette.scar")
            k = len(f["palette"]) - scar           # the scar's new kind and the ruin's come on top, as before
            before = R.by_label["foundation.palette_count"]["before_fill"]
            implied = sum(1 for r in R.public if str(r.get("forced_by", "")).startswith("implied by"))
            self.assertTrue(max(count, before) <= k <= max(count, before) + implied,
                            "the fill stops at the count; the forced kinds, the needs and an implied kind stand")
            over += k > hi
        self.assertLess(over, SEEDS * 0.03, "over the band's top: when the forced kinds and the needs alone pass it")
        type(self).over = over
        for (br, scale), seen in counts.items():
            lo, hi = head[br][scale]
            want = set(range(lo, hi + 1))
            self.assertEqual(seen, want, (br, scale))
        self.assertEqual(len(counts), 6)


def run(script, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n{proc.stdout[-1500:]}\n{proc.stderr[-1500:]}")
    return proc


class Births(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-world18b-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run("designer.py", "new", self.name, "--party-size", "2", "--seed", "WORLD-18B", "--lang", "tr", "--scale", "epic")
        run("designer.py", "-c", self.name, "preroll", "--phase", "P1")

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_no_join_lives_in_dm_only(self):
        """The 18c-1 audit: every world state's join is public; dm-only holds none."""
        log = json.loads((CAMPAIGNS / self.name / "design/dm-only/dice-log.json").read_text(encoding="utf-8"))
        self.assertNotIn("world_states", log["identity"])
        public = dm.load(self.name)["identity"]
        self.assertNotIn("world_state_secret", public)
        self.assertNotIn("pending", json.dumps(public))
        self.assertFalse([b for b in public["trope_breaks"] if (b.get("join") or {}).get("piece") == "hidden"])

    def test_a_legacy_birth_s_palette_loads(self):
        """A birth rolled before 18b drew 9 to 12 kinds at epic: it loads, its prompt and its card render."""
        m = dm.load(self.name)
        f = m["foundation"]
        extra = [r["id"] for r in dt.rows("foundation.yaml#palette") if r["id"] not in f["palette"] + f["palette_extra"] and not r.get("fantastic")]
        f["palette"] = f["palette"] + extra[:12 - len(f["palette"])]
        f["layout"]["along"] = [k for k in f["palette"] if k not in f["layout"]["parts"].values()]
        dm.save(self.name, m, "test: a legacy palette")
        self.assertGreaterEqual(len(dm.load(self.name)["foundation"]["palette"]), 9)
        run("designer.py", "-c", self.name, "phase", "P1", "begin", "--json")
        run("designer.py", "-c", self.name, "phase", "P1", "card")
        self.assertTrue((CAMPAIGNS / self.name / "design/_approval/P1.card.md").is_file())


if __name__ == "__main__":
    if "--report" in sys.argv:
        print(ManySeeds.report())
    else:
        unittest.main()
