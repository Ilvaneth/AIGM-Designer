"""
test_move.py — build item 18c, part 2 (docs/p1-build-18.md, Part 18c section 6; docs/p1-build-18-rows.md sections 1, 2
and 5 #8): the hand, the verbs (23, eight retired), the hand → verb fit, the target on the way to the goal and the
move's join, the time and the state, the timeline (`move.at`), the start (never the heart), the creature families; the
world states' public joins through the hand and the ruins; 3,000 seeds with no dead end; the move's variety.

  py test_move.py --report     the move's shares over 3,000 seeds
"""

import itertools
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_foundation as fd  # noqa: E402
import design_identity as di  # noqa: E402
import design_tables as dt  # noqa: E402
import design_threat as dth  # noqa: E402
import designer  # noqa: E402

SEEDS = 3000
SPAN = {"short": 4, "standard": 11, "epic": 19}
HANDS = {r["id"]: r for r in dt.rows("antagonists.yaml#hand")}
ACTIONS = {r["id"]: r for r in dt.rows("foundation.yaml#action")}
INTRIGUE = ("act_replaced", "act_possessed", "act_betrayed", "act_split")
CREATURE_HANDS = ("hand_dragon", "hand_risen_dead", "hand_ruin_power", "hand_giants", "hand_monstrous_beast", "hand_bound_elemental",
                  "hand_werewolves", "hand_golem_army", "hand_war_band", "hand_brigands", "hand_sea_raiders", "hand_slavers",
                  "hand_foreign_army", "hand_druid_circle")


class Tables(unittest.TestCase):

    def test_the_verbs(self):
        self.assertEqual(len(ACTIONS), 23)
        self.assertEqual({r["id"] for r in dt.retired("foundation.yaml#action")},
                         {"act_reversed", "act_true_face", "act_turned_on_keepers", "act_spread_unbounded", "act_twinned",
                          "act_forgotten", "act_gave_birth", "act_fell_from_sky"})
        self.assertFalse([r for r in ACTIONS.values() if r.get("concretise")], "the concretised object went with its verbs (W5)")
        self.assertEqual(ACTIONS["act_vanished"]["label"], "Carried off")
        self.assertEqual(set(ACTIONS["act_summoned"]["targets"]), {"thin_place", "heart", "key_place"}, "the 18c-2 answer")
        for r in ACTIONS.values():
            self.assertTrue(set(r["targets"]) <= set(fd.TARGET_PIECES))
            self.assertFalse(set(r.get("by") or []) - set(HANDS), r["id"])

    def test_the_hand(self):
        self.assertEqual(len(HANDS), 27)
        self.assertFalse(dt.roll_header("antagonists.yaml#hand").get("secret"), "the hand is public")
        self.assertFalse(dt.roll_header("antagonists.yaml#move_state").get("secret"))
        self.assertEqual({k for k, r in HANDS.items() if r.get("moon")},
                         {"hand_hired_company", "hand_sea_raiders", "hand_slavers", "hand_thieves_guild", "hand_from_beyond"})
        self.assertEqual(HANDS["hand_villain_itself"]["requires"], {"any_of": list(dth.PUBLIC_VISIBILITY)})
        self.assertEqual(HANDS["hand_golem_army"]["requires"], {"dial": {"magic": ["medium", "high"]}})
        self.assertEqual(len(dt.rows("antagonists.yaml#move_state")), 4)

    def test_a_creature_hand_makes_no_intrigue_move(self):
        for v in INTRIGUE:
            self.assertFalse(set(ACTIONS[v]["by"]) & set(CREATURE_HANDS), v)


def births(n: int, tag: str):
    combos = list(itertools.product(dt.dial_values("scale"), dt.dial_values("magic"), dt.dial_values("era"), dt.dial_values("tone")))
    mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
    out = []
    for i in range(n):
        sc, mg, era, tone = combos[i % len(combos)]
        lo = (1, 4, 7, 10)[(i // len(combos)) % 4]
        d = {"scale": sc, "magic": mg, "era": era, "tone": tone, "content_mix": list(mixes[i % len(mixes)]), "party_size": 2,
             "level_band": [lo, min(20, lo + SPAN[sc])]}
        R = designer.Roller.in_memory(f"{tag}-{i}", d)
        f = fd.build(fd.roll(R, d), d["level_band"])
        ident = di.roll(R, d, f)
        out.append((d, R, f, ident))
    return out


class ManySeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = births(SEEDS, "MOVE")

    def test_the_hand_makes_the_move_it_can(self):
        for d, R, f, ident in self.runs:
            m = f["move"]
            v = ACTIONS[m["verb"]]
            self.assertTrue(not v.get("by") or m["hand"] in v["by"])
            if m["hand"] == "hand_villain_itself":
                self.assertIn(R.threat["visibility"], dth.PUBLIC_VISIBILITY)
            self.assertEqual(f["break"]["action"], m["verb"])
            self.assertEqual(f["break"]["target"], m["target"])

    def test_the_target_is_on_the_way_and_the_move_joins(self):
        for d, R, f, ident in self.runs:
            m, g = f["move"], R.threat["goal"]
            piece = fd.PIECE_OF_TARGET[m["target"]]
            self.assertIn(piece, ACTIONS[m["verb"]]["targets"])
            self.assertEqual(m["goal_join"], g["join"])
            if g["join"] == "move":
                self.assertIn(m["join_by"], ("prize_piece", "role", "side_holding"))
                if m["join_by"] == "role":
                    self.assertEqual(piece, "role")
                if m["join_by"] == "side_holding":
                    self.assertIn(piece, ("remnant", "key_place", "thin_place"))
            else:
                self.assertIsNone(m["join_by"])
                self.assertIn(piece, fd.GOAL_TARGETS[g["piece"]])

    def test_the_time_the_state_and_the_timeline(self):
        for d, R, f, ident in self.runs:
            m = f["move"]
            coming = m["time"] == "time_coming"
            self.assertEqual(m["state"] is None, coming)
            self.assertEqual(m["at"], "end" if coming else "start")

    def test_the_start_is_never_the_heart(self):
        for d, R, f, ident in self.runs:
            self.assertNotEqual(f["start"], "heart")
            self.assertNotIn(f["start"], ("heart_ruins",))
            self.assertEqual(f["move"]["start"], f["start"])
            if f["move"]["time"] == "time_coming":
                base = fd.hand_base(f["layout"], f["move"]["hand"], f["break"]["winner"])
                self.assertEqual(f["start"], base if base != "heart" else "end_a")

    def test_the_creature_families(self):
        for d, R, f, ident in self.runs:
            fam = R.threat["families"]
            self.assertEqual(fam["public"], f["move"]["families"])
            self.assertEqual(fam["secret"], [R.threat["creature_type"]])
            hand = HANDS[f["move"]["hand"]]
            want = [R.threat["creature_type"] if x == "villain" else x for x in hand["families"]]
            self.assertEqual(fam["public"], want)

    def test_every_verb_and_hand_is_reached_and_no_target_is_starved(self):
        verbs = Counter(f["move"]["verb"] for *_, f, _ in [(r[0], r[1], r[2], r[3]) for r in self.runs])
        hands = Counter(f["move"]["hand"] for _, _, f, _ in self.runs)
        targets = Counter(f["move"]["target"] for _, _, f, _ in self.runs)
        self.assertEqual(set(verbs), set(ACTIONS))
        self.assertEqual(set(hands), set(HANDS))
        for t, n in targets.items():
            if t != "target_thin_place":
                self.assertGreaterEqual(n, SEEDS * 0.05, t)
        self.assertGreaterEqual(targets["target_remnant"], SEEDS * 0.10)

    def test_the_world_states_through_the_hand_and_the_ruins(self):
        drawn = Counter()
        for d, R, f, ident in self.runs:
            for b in ident["trope_breaks"]:
                j = b.get("join") or {}
                if j.get("piece") == "hand":
                    hand = HANDS[f["move"]["hand"]]
                    self.assertTrue(hand.get("moon") if b["id"] == "break_moon_trades" else "dragon" in hand["families"])
                if b["id"] in ("break_dragons_rule", "break_gods_among_mortals"):
                    drawn[b["id"]] += 1
        self.assertGreaterEqual(drawn["break_dragons_rule"], 40)
        self.assertGreaterEqual(drawn["break_gods_among_mortals"], 40)


def report() -> str:
    runs = births(SEEDS, "MOVE")
    n = len(runs)
    pct = lambda c: ", ".join(f"{k} {100 * v / n:.1f} %" for k, v in sorted(c.items(), key=lambda kv: -kv[1]))
    out = [f"{n} seeds"]
    out.append("targets: " + pct(Counter(f["move"]["target"][7:] for _, _, f, _ in runs)))
    out.append("joins: " + pct(Counter(f"{f['move']['goal_join']}/{f['move']['join_by']}" for _, _, f, _ in runs)))
    hands = Counter(f["move"]["hand"] for _, _, f, _ in runs)
    verbs = Counter(f["move"]["verb"] for _, _, f, _ in runs)
    out.append(f"hands: {len(hands)} of 27, {min(hands.values())}-{max(hands.values())} each; verbs: {len(verbs)} of 23, {min(verbs.values())}-{max(verbs.values())} each")
    out.append("start: " + pct(Counter(f["start"].split(":")[0] for _, _, f, _ in runs)))
    out.append("state: " + pct(Counter(str(f["move"]["state"]) for _, _, f, _ in runs)))
    ws = Counter(b["id"] for *_, ident in runs for b in ident["trope_breaks"] if "join" in b)
    out.append("world states: " + ", ".join(f"{k[6:]} {v}" for k, v in sorted(ws.items(), key=lambda kv: -kv[1])))
    return "\n".join(out)


if __name__ == "__main__":
    if "--report" in sys.argv:
        print(report())
    else:
        unittest.main()
