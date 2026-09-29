"""
test_foundation_roll.py — P1's first step by script (plan item 25; build item 6): thousands of seeds over every
scale, magic and era produce no conflicting set and hold every rule of the foundation tables — the spine's and the
era's forced kinds, a height and a water, the fantastic cap (the thin place outside it, the ruin's kind on top of
it), the requirements, the epic second contest, the action fitting its target, the scars' room and the closed thin
place, the winner rules, the escalation from the level band, the sentence's five templates with the tense of the
time. The low-magic mage war brings its glass desert; the merge rules; the pair that never repeats; the archived
births are recognised as foundationless.
"""

import itertools
import sys
import unittest

from _campaign import CAMPAIGNS, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

SPAN = {"short": 4, "standard": 11, "epic": 19}
CAP = {"low": 0, "medium": 1, "high": 2}
PAL = fd.rows_by_id("palette")
SPINE = fd.rows_by_id("spine")
RUIN = fd.rows_by_id("ruin_source")
LIFE = fd.rows_by_id("lifeline")
CONTEST = fd.rows_by_id("contest")
ACTION = fd.rows_by_id("action")
SCAR = fd.rows_by_id("scar")
TIME = fd.rows_by_id("time")


def dials(scale, magic, era, start=1):
    return {"scale": scale, "magic": magic, "era": era, "tone": "heroic", "content_mix": ["war", "mystery", "horror"],
            "level_band": [start, min(20, start + SPAN[scale])]}


def one(seed, d, used_pairs=None):
    R = designer.Roller.in_memory(seed, d)
    out = fd.roll(R, d, used_pairs)
    return R, out, fd.build(out, d["level_band"])


class ManySeeds(unittest.TestCase):
    """Item 25's common rules: a model-free test rolls P1 over thousands of seeds and proves no conflicting set."""

    @classmethod
    def setUpClass(cls):
        cls.runs = []
        combos = list(itertools.product(("short", "standard", "epic"), ("low", "medium", "high"),
                                        ("medieval", "renaissance", "ancient", "nautical", "underground")))
        for i in range(2250):
            scale, magic, era = combos[i % len(combos)]
            d = dials(scale, magic, era, start=1 + (i // len(combos)) % 4 * 3)
            R, out, f = one(f"MANY-{i}", d)
            cls.runs.append((d, R, out, f))

    def rolled(self, R):
        return [r["row_id"] for r in R.public + R.secret if r.get("row_id")]

    def test_no_conflicting_set_in_thousands_of_seeds(self):
        self.assertGreaterEqual(len(self.runs), 2000)
        for d, R, out, f in self.runs:
            self.assertEqual(arb.conflicting_pairs(self.rolled(R)), [], R.master)

    def test_the_palette(self):
        for d, R, out, f in self.runs:
            with self.subTest(seed=R.master):
                pal = f["palette"]
                spine = SPINE[f["spine"]]
                self.assertTrue(set(spine.get("forces") or []) <= set(pal))
                if spine.get("forces_one_of"):
                    self.assertTrue(set(spine["forces_one_of"]) & set(pal))
                if d["era"] == "underground":
                    self.assertIn("land_underground", pal)
                self.assertTrue(any(PAL[k].get("height") for k in pal))
                self.assertTrue(any(PAL[k].get("water") and not PAL[k].get("fantastic") for k in pal))
                self.assertLessEqual(sum(1 for k in pal if fd.is_capped(PAL[k])), CAP[d["magic"]])
                self.assertEqual(len(pal), len(set(pal)))
                count = R.by_label["foundation.palette_count"]["value"]
                self.assertGreaterEqual(len(pal), count)
                for k in pal:
                    self.assertTrue(arb.holds(PAL[k].get("requires"), arb.Context(dials=d)) or k in (spine.get("forces") or []),
                                    f"{k} at magic {d['magic']}")
                for imp in (PAL[k].get("implies") or [] for k in pal):
                    self.assertTrue(set(imp) <= set(pal))

    def test_the_requirements_hold(self):
        for d, R, out, f in self.runs:
            ctx = arb.Context(dials=d, rolled={k: False for k in self.rolled(R)})
            for table, rid in ((RUIN, f["ruin_source"]), (LIFE, f["lifeline"]["id"]), (SPINE, f["spine"])):
                self.assertTrue(arb.holds(table[rid].get("requires"), ctx), (R.master, rid))
            for c in f["contests"]:
                self.assertTrue(arb.holds(CONTEST[c["id"]].get("requires"), ctx), (R.master, c["id"]))

    def test_the_contests(self):
        for d, R, out, f in self.runs:
            cs = f["contests"]
            self.assertEqual(len(cs), 2 if d["scale"] == "epic" else 1)
            self.assertEqual(cs[0]["roles"], {"short": ["a", "b", "third"]}.get(d["scale"], ["a", "b", "third", "fourth"]))
            if len(cs) == 2:
                self.assertNotEqual(CONTEST[cs[0]["id"]]["family"], CONTEST[cs[1]["id"]]["family"])
                self.assertEqual(cs[1]["roles"], ["a", "b", "third"])

    def test_the_break(self):
        for d, R, out, f in self.runs:
            with self.subTest(seed=R.master):
                b = f["break"]
                piece = fd.PIECE_OF_TARGET[b["target"]]
                act = ACTION[b["action"]]
                self.assertIn(piece, act["targets"])
                fits = act.get("fits") or {}
                if piece == "lifeline":
                    self.assertIn(LIFE[f["lifeline"]["id"]]["family"], fits["lifeline"])
                if piece == "remnant":
                    self.assertIn(RUIN[f["ruin_source"]]["remnant_kind"], fits["remnant"])
                if piece == "key_place":
                    self.assertIn(SPINE[f["spine"]]["key_kind"], fits["key_place"])
                if piece == "thin_place":
                    self.assertIn("land_thin_place", f["palette"])
                self.assertEqual(len(b["scars"]), {"short": 1, "standard": 2, "epic": 3}[d["scale"]])
                self.assertEqual(len(set(b["scars"])), len(b["scars"]))
                if piece == "thin_place" and b["action"] == "act_closed":
                    self.assertNotIn("scar_plane_thinned", b["scars"])
                roles = f["contests"][0]["roles"]
                self.assertIn(b["winner"], roles)
                if piece == "role":
                    self.assertIn(b["target_role"], roles)
                    if "role" in (act.get("destroys") or []):
                        self.assertNotEqual(b["winner"], b["target_role"], "a destroyed role cannot win")
                    if act.get("winner_is_target_role"):
                        self.assertEqual(b["winner"], b["target_role"], "a role that rose is the winner")
                heart_gone = piece == "heart" and "heart" in (act.get("destroys") or [])
                want = ("heart_ruins" if act.get("leaves_ruins") else "end_a") if heart_gone else "heart"
                self.assertEqual(f["start"], want)
                action_rec = R.by_label["foundation.break.action"]
                self.assertEqual(action_rec["used_keys"], {fd.PAIR_KEY: f"{piece}|{b['action']}"})

    def test_every_rule_is_exercised(self):
        """The sweep must reach the rare branches it proves."""
        seen = {"rose_on_role": 0, "destroyed_role": 0, "closed_thin": 0, "new_land": 0, "ruin_extra": 0}
        for d, R, out, f in self.runs:
            b, act = f["break"], ACTION[f["break"]["action"]]
            piece = fd.PIECE_OF_TARGET[b["target"]]
            seen["rose_on_role"] += piece == "role" and bool(act.get("winner_is_target_role"))
            seen["destroyed_role"] += piece == "role" and "role" in (act.get("destroys") or [])
            seen["closed_thin"] += piece == "thin_place" and b["action"] == "act_closed"
            seen["new_land"] += "scar_new_land_kind" in b["scars"]
            seen["ruin_extra"] += bool(f["palette_extra"])
            seen["heart_ruins"] = seen.get("heart_ruins", 0) + (f["start"] == "heart_ruins")
            seen["heart_gone_bare"] = seen.get("heart_gone_bare", 0) + (f["start"] == "end_a")
        for k, v in seen.items():
            self.assertGreater(v, 0, k)

    def test_the_new_land_scar_adds_a_capped_kind_within_the_cap(self):
        for d, R, out, f in self.runs:
            if "scar_new_land_kind" in f["break"]["scars"]:
                self.assertNotEqual(d["magic"], "low")
                self.assertIn("foundation.palette.scar", R.by_label)
                self.assertLessEqual(sum(1 for k in f["palette"] if fd.is_capped(PAL[k])), CAP[d["magic"]])

    def test_the_layout(self):
        """Build item 6b: the ends on different kinds, the key place on its key kind, every kind placed once, the
        lifeline on a part of its kind, the contests' seats."""
        lands = dt.load("foundation.yaml")["key_kind_lands"]
        for d, R, out, f in self.runs:
            with self.subTest(seed=R.master):
                lay = f["layout"]
                parts, along = lay["parts"], lay["along"]
                spine = SPINE[f["spine"]]
                ends = [parts[p] for p in parts if p.startswith("end_")]
                self.assertEqual(len(ends), len(set(ends)), "the ends take different kinds")
                self.assertEqual(len(ends), 4 if f["spine"] == "spine_crossroads" else 2)
                if spine["key_kind"] in lands:
                    self.assertIn(parts["key_place"], lands[spine["key_kind"]])
                every = f["palette"] + f["palette_extra"]
                self.assertEqual(set(parts.values()) | set(along), set(every), "every kind on a part or along")
                self.assertFalse(set(parts.values()) & set(along))
                life = LIFE[f["lifeline"]["id"]]
                seat = lay["lifeline"]
                kind = seat.split(":", 1)[1] if seat.startswith("along:") else parts[seat]
                if life.get("where"):
                    self.assertIn(kind, life["where"], "the lifeline sits on a kind its where holds")
                else:
                    self.assertFalse(seat.startswith("along:"), "an everywhere row sits on a part")
                if life["family"] == "passage" and parts["key_place"] in (life.get("where") or []):
                    self.assertEqual(seat, "key_place")
                main = lay["contests"][0]
                row = CONTEST[main["contest"]]
                over = {k: v for k, v in (row.get("seats") or {}).items() if k != "prize"}
                default = {"a": "end_a", "b": "end_b", "third": "heart", "fourth": "along"}
                for role, where in main["seats"].items():
                    if role in over:
                        want = {"end": "end_a" if role == "a" else "end_b", "beside_key_place": "key_place"}.get(over[role], over[role])
                        self.assertEqual(where, want, (row["id"], role))
                    elif role != "third":
                        self.assertEqual(where, default[role], (row["id"], role))
                if "third" not in over:
                    self.assertNotIn(main["seats"]["third"], (main["seats"]["a"], main["seats"]["b"]))
                if row.get("seats", {}).get("prize") == "thin_place":
                    at = main["prize"]["at"]
                    self.assertEqual(at.split(":", 1)[1] if at.startswith("along:") else parts[at], "land_thin_place")
                if len(lay["contests"]) == 2:
                    first = {p for p in main["seats"].values() if p != "along"}
                    second = {p for p in lay["contests"][1]["seats"].values() if p != "along"}
                    self.assertFalse(first & second, "epic's second contest sits where the first did not")

    def test_the_variety_rule(self):
        """Owner, 2026-09-29: within a part's list, a kind no part holds yet comes first; never outside the list."""
        lands = dt.load("foundation.yaml")["key_kind_lands"]
        for d, R, out, f in self.runs:
            spine = SPINE[f["spine"]]
            parts = f["layout"]["parts"]
            every = f["palette"] + f["palette_extra"]
            placed: list = []
            order = ["key_place"] + [p for p in ("end_a", "end_b", "end_c", "end_d") if p in spine["parts"]] + ["heart"]
            for part in order:
                ends = [parts[p] for p in order[:order.index(part)] if p.startswith("end_")]
                ok = lambda k: not (part == "key_place" and spine["key_kind"] in lands and k not in lands[spine["key_kind"]])                     and not (part.startswith("end_") and k in ends)
                cand = [k for k in spine["parts"][part] if k in every and ok(k)]
                if cand:
                    self.assertIn(parts[part], cand, (R.master, part, "never outside the list when it has a kind"))
                    if any(k not in placed for k in cand):
                        self.assertNotIn(parts[part], placed, (R.master, part))
                placed.append(parts[part])

    def test_the_remnant_the_break_and_every_prize_have_a_place(self):
        """Owner, 2026-09-29: the remnant sits by the merge rules, else where the ruin's kind lies, else an end or an
        along node, never the heart without a merge; the break lies where its target is; no prize is placeless."""
        seen_merge = 0
        for d, R, out, f in self.runs:
            with self.subTest(seed=R.master):
                lay = f["layout"]
                parts = lay["parts"]
                ruin = RUIN[f["ruin_source"]]
                rem = lay["remnant"]
                if f["merges"]:
                    seen_merge += 1
                    self.assertEqual(rem, "key_place" if f["ruin_source"] == "ruin_planar_rift" else "heart")
                else:
                    self.assertNotEqual(rem, "heart", "the heart takes the remnant only by a merge")
                    own = ([ruin["adds_palette"]] if ruin.get("adds_palette") else []) + list((ruin.get("requires") or {}).get("any_of") or [])
                    kind = rem.split(":", 1)[1] if rem.startswith("along:") else parts[rem]
                    if any(k in own for k in [v for p, v in parts.items() if p != "heart"] + lay["along"]):
                        self.assertIn(kind, own)
                    else:
                        self.assertTrue(rem.startswith(("end_", "along:")))
                b = f["break"]
                piece = fd.PIECE_OF_TARGET[b["target"]]
                want = {"lifeline": lay["lifeline"], "remnant": rem, "key_place": "key_place", "heart": "heart",
                        "role": lay["contests"][0]["seats"].get(b.get("target_role"))}.get(piece)
                if piece == "thin_place":
                    at = lay["break_at"]
                    self.assertEqual(at.split(":", 1)[1] if at.startswith("along:") else parts[at], "land_thin_place")
                else:
                    self.assertEqual(lay["break_at"], want)
                self.assertTrue(lay["break_at"])
                for c in lay["contests"]:
                    self.assertTrue(c["prize"]["at"], (c["contest"], c["prize"]))
                    if c["prize"]["kind"] == "remnant" and not (CONTEST[c["contest"]].get("seats") or {}).get("prize"):
                        self.assertEqual(c["prize"]["at"], rem)
                    if c["prize"]["kind"] == "new":
                        self.assertEqual(c["prize"]["at"], lay["break_at"])
        self.assertGreater(seen_merge, 0, "the sweep reaches a merge")

    def test_the_escalation_follows_the_level_band(self):
        for d, R, out, f in self.runs:
            lo, hi = d["level_band"]
            want = [t for t, (a, b) in (("tier_local", (1, 4)), ("tier_regional", (5, 10)), ("tier_continental", (11, 16)),
                                        ("tier_world", (17, 20))) if a <= hi and b >= lo]
            self.assertEqual(f["escalation"]["tiers"], want)
            self.assertEqual(f["escalation"]["steps"], len(want))
        self.assertEqual(len(fd.tiers_touched([1, 5])), 2, "short from level 1: two steps")
        self.assertEqual(len(fd.tiers_touched([1, 12])), 3)
        self.assertEqual(len(fd.tiers_touched([1, 20])), 4)
        self.assertEqual(len(fd.tiers_touched([11, 15])), 1)

    def test_the_sentence(self):
        for d, R, out, f in self.runs:
            s = f["sentence_tr"]
            with self.subTest(seed=R.master):
                self.assertTrue(s.startswith("Dünya "))
                self.assertNotIn("None", s)
                self.assertNotIn("(", s, "no design note in the sentence")
                for marker in ("Çok önce", "Bugün halk", "arasında eski bir gerilim var", "Bundan güçlü çıkan:"):
                    self.assertIn(marker, s)
                self.assertIn("Yaraları:" if len(f["break"]["scars"]) > 1 else "Yarası:", s)
                t = TIME[f["break"]["time"]]
                self.assertIn(ACTION[f["break"]["action"]]["forms"][t["tense"]], s)
                if t["id"] == "time_coming":
                    self.assertIn("İşaretler belli: ", s)


class Rules(unittest.TestCase):

    def test_the_low_magic_mage_war_brings_its_glass_desert(self):
        """Owner, 2026-09-28: the ruin's kind skips the kind's own magic requirement and sits outside the cap."""
        for i in range(4000):
            d = dials("standard", "low", "medieval")
            R, out, f = one(f"GLASS-{i}", d)
            if f["ruin_source"] == "ruin_mage_war":
                self.assertEqual(f["palette_extra"], ["land_glass_desert"])
                self.assertNotIn("land_glass_desert", f["palette"], "on top of the count, not in it")
                self.assertEqual(sum(1 for k in f["palette"] if fd.is_capped(PAL[k])), 0, "low: the cap holds for the rest")
                return
        self.fail("no seed drew the mage war")

    def test_the_merge_rules(self):
        self.assertEqual(fd.merges("spine_star_crater", "ruin_fallen_star")[0]["ruin"], "ruin_fallen_star")
        self.assertEqual(fd.merges("spine_star_crater", "ruin_celestial_war")[0]["spine"], "spine_star_crater")
        self.assertEqual(fd.merges("spine_two_worlds", "ruin_planar_rift")[0]["ruin"], "ruin_planar_rift")
        self.assertEqual(fd.merges("spine_star_crater", "ruin_planar_rift"), [])
        self.assertEqual(fd.landmarks("spine_star_crater", "ruin_fallen_star"), ["crater"], "one crater, the heart's")
        self.assertEqual(fd.landmarks("spine_river_to_sea", "ruin_fallen_star"), ["crater"])
        self.assertEqual(fd.landmarks("spine_star_crater", "ruin_fallen_sky_city"), ["crater", "floating_fragments"])

    def test_a_used_pair_waits(self):
        """A target + action pair another birth used is usage: the draw moves to another action."""
        d = dials("standard", "medium", "medieval")
        moved = 0
        for i in range(60):
            R, out, f = one(f"PAIR-{i}", d)
            piece = fd.PIECE_OF_TARGET[f["break"]["target"]]
            R2, out2, f2 = one(f"PAIR-{i}", d, used_pairs={f"{piece}|{f['break']['action']}"})
            self.assertEqual(f2["break"]["target"], f["break"]["target"], "the same seed strikes the same target")
            if f2["break"]["action"] != f["break"]["action"]:
                moved += 1
            else:
                self.assertTrue(R2.by_label["foundation.break.action"].get("usage_fallback"))
        self.assertGreater(moved, 50)

    def test_the_same_seed_gives_the_same_foundation(self):
        d = dials("epic", "high", "nautical")
        self.assertEqual(one("SAME-1", d)[2], one("SAME-1", d)[2])
        self.assertNotEqual(one("SAME-1", d)[2]["sentence_tr"], one("SAME-2", d)[2]["sentence_tr"])


class LegacyBirths(unittest.TestCase):
    """The archived births have no foundation: every later gate that reads it leaves them as they were built."""

    def test_the_archived_births_and_the_fixture_are_foundationless(self):
        from _campaign import FIXTURE
        import json
        fixture = json.loads((FIXTURE / "design" / "design.json").read_text(encoding="utf-8"))
        self.assertTrue(dm.legacy_birth(fixture))
        found = 0
        for birth in ("_test-tune-2", "_test-dry-1", "_test-dry-2", "_test-dry-3", "_test-dry-4"):
            path = CAMPAIGNS / birth / "design" / "design.json"
            if path.is_file():
                found += 1
                self.assertTrue(dm.legacy_birth(json.loads(path.read_text(encoding="utf-8"))), birth)
        if not found:
            self.skipTest("the archived births are git-ignored and absent on this checkout")

    def test_a_new_birth_is_not(self):
        self.assertFalse(dm.legacy_birth({"phases": {"P1": {"status": "prerolled"}}, "foundation": {"stamped": True}}))
        self.assertFalse(dm.legacy_birth({"phases": {"P1": {"status": "pending"}}}))


if __name__ == "__main__":
    unittest.main()
