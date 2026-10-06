"""
test_identity_secret_roll.py — build item 10b (docs/p1-build-10.md §8-10): the secret and the villain rolled in P1,
every roll secret; P4 reads the moved rolls.

The owner is also the player: no assertion here prints a secret row. A failure gives a count or a seed, never an id.
"""

import itertools
import json
import os
import shutil
import sys
import unittest
import uuid

from _campaign import SCRIPTS, CAMPAIGNS, USED
import _floor
import test_designer as td

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_identity as di  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

A, V = "secrets.yaml#", "antagonists.yaml#"
SEEDS = 1800
# build item 18c: the chooser and the tie are no longer rolled; the threat's rolls are secret too
P1_SECRET = ("secret_keeping", "secret_trail", "bbeg_visibility", "bbeg_shape", "bbeg_origin", "bbeg_pole",   # 18d: the twist only sometimes
             "threat.family", "threat.goal", "threat.weakness", "threat.lair_form", "threat.lair_where")
MOVED = ("bbeg_visibility", "bbeg_shape", "bbeg_origin")
SECRET_IDS = dt.secret_row_ids()


def dials_of(i, combos, mixes):
    scale, magic, era, tone = combos[i % len(combos)]
    return {"scale": scale, "magic": magic, "era": era, "tone": tone, "content_mix": list(mixes[i % len(mixes)]),
            "party_size": 2, "level_band": [1, 1 + _floor.SPAN[scale]]}


def p4_on(p1, dials, tag):
    p4 = designer.Roller.in_memory(tag, dials, phase="P4")
    p4.ctx = p1.ctx                                  # P4 stands on what P1 rolled, the secret rows too
    designer.preroll_p4(p4, {"dials": dials})
    return p4


class ManySeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        combos = _floor.dial_sets()
        mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
        cls.runs, cls.empty = [], 0
        for i in range(SEEDS):
            d = dials_of(i, combos, mixes)
            try:
                p1 = designer.Roller.in_memory(f"SECRET-{i}", d)
                designer.preroll_p1(p1, {"dials": d})
                cls.runs.append((d, p1, p4_on(p1, d, f"SECRET-{i}")))
            except SystemExit:
                cls.empty += 1

    def test_no_pool_is_empty(self):
        self.assertEqual(self.empty, 0, f"{self.empty} seed(s) stopped on an empty pool")

    def test_no_conflicting_set_across_the_public_and_the_secret_rows(self):
        bad = 0
        for d, p1, p4 in self.runs:
            rolled = [r["row_id"] for R in (p1, p4) for r in R.public + R.secret if r.get("row_id")]
            bad += bool(arb.conflicting_pairs(rolled, tokens=list(p4.ctx.tokens), exempt=p1.exempt))
        self.assertEqual(bad, 0, f"{bad} seed(s) rolled a conflicting set")

    def test_the_chooser_and_the_tie(self):
        """Build item 18c: the villain always chose; neither the chooser nor the tie is rolled."""
        for d, p1, _ in self.runs:
            s, v = p1.identity_secret["secret"], p1.identity_secret["villain"]
            self.assertEqual((s["chooser"], s["chooser_role"], v["tie"]), ("chooser_the_villain", None, None))
            self.assertFalse({"secret_chooser", "secret_chooser.role", "bbeg_tie"} & set(p1.by_label))
            self.assertEqual((v["visibility"], v["shape"], v["origin"]), (p1.threat["visibility"], p1.threat["shape"], p1.threat["origin"]))

    def test_every_shape_and_origin_is_drawn(self):
        """Build item 16a: no shape or origin is barred; over the seeds every row of the two tables comes up."""
        for label, sub in (("bbeg_shape", "villain_shape"), ("bbeg_origin", "origin")):
            self.assertFalse(any(r.get("forbidden") for r in dt.rows(V + sub)))
            drawn = {p1.by_label[label]["row_id"] for d, p1, p4 in self.runs}
            self.assertEqual(len(drawn), len(dt.rows(V + sub)), f"{sub}: {len(dt.rows(V + sub)) - len(drawn)} row(s) never drawn")

    def test_the_floor(self):
        """The secret's non-repeating tables keep five rows after the constraints; the villain's shape and origin
        may repeat (the pair is what never does) and are reported only."""
        low = {ref: min(p1.pools[ref] for _, p1, _ in self.runs if ref in p1.pools)      # a forced tie has no pool
               for ref in (A + "keeping", A + "twist", A + "trail", V + "villain_shape", V + "origin") if any(ref in p1.pools for _, p1, _ in self.runs)}
        type(self).floors = low
        for ref in (A + "keeping", A + "twist", A + "trail"):
            self.assertGreaterEqual(low[ref], 5, f"{ref}: the smallest pool is {low[ref]}")

    def test_the_pole_and_the_majority(self):
        sides = set()
        for d, p1, _ in self.runs:
            v = p1.identity_secret["villain"]
            sides.add(v["pole"]["role"])
            self.assertEqual(v["pole"]["question"], p1.identity["questions"][0]["id"])
            self.assertEqual(v["pole"]["contest"], p1.foundation["contests"][0]["id"], "epic: the main contest's question")
            self.assertEqual(v["majority_pole"], "villain" if d["tone"] == "dark" else "other")
        self.assertEqual(sides, {"a", "b"})

    def test_the_public_figure_and_the_secret_villain(self):
        """Build item 16c: beside a public row that shows a figure (the dark lord's contest), the villain is that figure
        exactly when the visibility says "known"; then the shape is not rolled and, in the main contest, the pole is
        that role's. With any other visibility the villain is someone else and never takes that shape."""
        rules = {(pid, row["id"]): rule for row in dt.rows(V + "villain_shape") for pid, rule in (row.get("same_figure_with") or {}).items()}
        self.assertEqual(len(rules), 1)
        beside = same = other = wrong = 0
        for d, p1, _ in self.runs:
            v = p1.identity_secret["villain"]
            contests = [c["id"] for c in p1.foundation["contests"]]
            hit = [(pid, sid, rule) for (pid, sid), rule in rules.items() if pid in contests]
            if not hit:
                wrong += v["public_figure"] is not None
                continue
            beside += 1
            pid, sid, rule = hit[0]
            if v["visibility"] == rule["visibility"]:
                same += 1
                wrong += v["shape"] != sid or v["public_figure"] != {"contest": pid, "role": rule["role"]}
                wrong += p1.by_label["bbeg_shape"]["notation"] != "forced"
                if contests[0] == pid:
                    wrong += v["pole"]["role"] != rule["role"] or p1.by_label["bbeg_pole"]["notation"] != "fixed"
            else:
                other += 1
                wrong += v["shape"] == sid or v["public_figure"] is not None
        self.assertEqual(wrong, 0, f"{wrong} breach(es) of the public figure rule")
        self.assertGreater(beside, 10)
        self.assertGreater(same, 0, "the same-figure case was exercised")
        self.assertGreater(other, 0, "the other-figure case was exercised")
        type(self).figure = {"beside": beside, "same": same, "other": other}

    def test_every_piece_is_secret_and_nothing_public_names_it(self):
        leaks = sizes = 0
        for d, p1, p4 in self.runs:
            for label in P1_SECRET:
                self.assertIn(p1.by_label[label], p1.secret)
            for R in (p1, p4):
                text = json.dumps(R.public, ensure_ascii=False) + json.dumps(R.identity or {}, ensure_ascii=False) \
                    + json.dumps(R.foundation or {}, ensure_ascii=False)
                leaks += sum(1 for rid in SECRET_IDS if f'"{rid}"' in text)
                leaks += sum(1 for r in R.public if r["label"] in P1_SECRET or r["label"].startswith("secret_"))
                for note in R.secret_notes:                      # a secret row took rows out of a public pool
                    shown = R.by_label[note["label"]]
                    if shown in R.public and note.get("notation"):
                        sizes += shown["notation"] == note["notation"]
        self.assertEqual(leaks, 0, f"{leaks} secret row(s) or label(s) in a public record")
        self.assertEqual(sizes, 0, f"{sizes} public die size(s) tell what the secret layer took out")

    def test_p4_reads_the_moved_rolls(self):
        for d, p1, p4 in self.runs:
            for label in MOVED + ("bbeg_tie", "bbeg_pole"):
                self.assertNotIn(label, p4.by_label, "no label is rolled twice")
            labels = [r["label"] for r in p1.public + p1.secret + p4.public + p4.secret]
            self.assertEqual(len(labels), len(set(labels)))
            for label in ("bbeg_faction_archetype", "front_template", "doom_shape"):
                self.assertIn(p4.by_label[label], p4.secret)
            self.assertTrue(p4.ctx.has(p1.by_label["bbeg_shape"]["row_id"]), "P4 stands on P1's villain")


class LegacyP4(unittest.TestCase):

    def test_a_birth_whose_p1_rolled_no_villain_still_rolls_it_in_p4(self):
        """A birth from before build item 10b: P1 holds no villain rolls, so P4 makes them as it did."""
        d = {"scale": "standard", "magic": "medium", "era": "medieval", "tone": "shadowed",
             "content_mix": ["war", "mystery", "horror"], "party_size": 2, "level_band": [1, 12]}
        p4 = designer.Roller.in_memory("LEGACY-P4", d, phase="P4")
        self.assertFalse(di.villain_in_context(p4.ctx))
        designer.preroll_p4(p4, {"dials": d})
        for label in MOVED:
            self.assertIn(p4.by_label[label], p4.secret)
        self.assertNotIn("bbeg_tie", p4.by_label)


class ThePair(unittest.TestCase):

    D = {"scale": "standard", "magic": "medium", "era": "medieval", "tone": "shadowed",
         "content_mix": ["war", "mystery", "horror"], "party_size": 2, "level_band": [1, 12]}

    def p1(self, used_pairs=None):
        import design_threat as dth                    # build item 18c: the shape and the origin are the threat's
        real = dth.roll
        if used_pairs is not None:
            dth.roll = lambda *a, **k: real(*a[:6], used_pairs=used_pairs)
        try:
            R = designer.Roller.in_memory("PAIR-1", self.D)
            designer.preroll_p1(R, {"dials": self.D})
            return R
        finally:
            dth.roll = real

    def test_a_pair_another_campaign_drew_is_not_drawn_again(self):
        first = self.p1()
        v = first.identity_secret["villain"]
        rec = first.by_label["bbeg_origin"]
        self.assertEqual(rec["used_keys"], {di.VILLAIN_PAIR_KEY: f"{v['shape']}|{v['origin']}"})
        again = self.p1(used_pairs={dd.hashed(f"{v['shape']}|{v['origin']}")})
        w = again.identity_secret["villain"]
        self.assertEqual(w["shape"], v["shape"], "the same seed draws the same shape")
        self.assertNotEqual(w["origin"], v["origin"], "the spent pair's origin waits")
        self.assertEqual(sum(1 for e in again.by_label["bbeg_origin"]["excluded"] if e["why"] == "pair"), 1)
        for sub in ("villain_shape", "origin"):
            self.assertIs(dt.own_roll_header(V + sub).get("avoid_used"), False, "the rows themselves may repeat")
            self.assertFalse(dt.records_usage(V + sub))


class RealBirth(unittest.TestCase):
    """One short test birth on disk: where the secret goes, what approve writes."""

    def setUp(self):
        self.guard = td.MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-secret-{os.getpid()}-{uuid.uuid4().hex[:6]}"

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_the_secret_goes_to_dm_only_and_the_pair_to_used_json_hashed(self):
        td.run("new", self.name, "--party-size", "2", "--seed", "SECRET-0001", "--lang", "tr", "--scale", "short", "--tone", "shadowed",
               "--magic", "medium", "--era", "medieval", "--danger", "balanced", "--content-mix", "war,mystery,horror", check=True)
        proc = td.run("-c", self.name, "preroll", "--phase", "P1", check=True)
        design = CAMPAIGNS / self.name / "design"
        public_text = (design / "design.json").read_text(encoding="utf-8")
        manifest = json.loads(public_text)
        log = json.loads((design / "dm-only" / "dice-log.json").read_text(encoding="utf-8"))
        ident = log["identity"]
        self.assertEqual(set(ident), {"secret", "villain"}, "the 18c-1 audit: no world state's join lives in dm-only")
        self.assertIn("threat", log, "build item 18c: the threat's record, dm-only")
        self.assertEqual(set(ident["secret"]), {"archetype", "chooser", "chooser_role", "twist", "keeping", "trail", "facts", "stages", "pin"})
        self.assertEqual(set(ident["villain"]), {"visibility", "shape", "origin", "tie", "pole", "public_figure", "majority_pole"})
        by_label = {r["label"]: r for r in log["rolls"] if r["phase"] == "P1"}
        for label in P1_SECRET:
            self.assertIn(label, by_label)
            self.assertIn(label, manifest["dice_log_secret"]["labels"])
        self.assertEqual(ident["villain"]["shape"], by_label["bbeg_shape"]["row_id"])
        # nothing public names a secret row: design.json (dice log, foundation, identity) and the preroll's printout
        named = sum(1 for rid in SECRET_IDS if rid in public_text or rid in proc.stdout)
        self.assertEqual(named, 0, f"{named} secret row(s) named in design.json or printed at preroll")
        self.assertNotIn("villain", manifest["identity"])
        self.assertNotIn("secret", manifest["identity"])
        # approve writes the shape and origin pair hashed; the rows themselves are not recorded
        self.assertGreater(designer.record_used(self.name, "P1"), 0)
        used_text = USED.read_text(encoding="utf-8")
        mine = json.loads(used_text)["campaigns"][self.name]
        pair = f"{ident['villain']['shape']}|{ident['villain']['origin']}"
        self.assertEqual(mine[di.VILLAIN_PAIR_KEY], [dd.hashed(pair)])
        self.assertNotIn(V + "villain_shape", mine)
        self.assertNotIn(V + "origin", mine)
        self.assertEqual(sum(1 for rid in SECRET_IDS if rid in used_text), 0, "used.json names a secret row in clear")
        self.assertIn(dd.hashed(pair), dd.used_values("_test-another-birth", di.VILLAIN_PAIR_KEY), "the next birth sees the spent pair")
        # P4 of this birth rolls no villain piece again
        ctx = dd.context(self.name, "P4")
        self.assertTrue(di.villain_in_context(ctx))


if __name__ == "__main__":
    if "--floor" in sys.argv:
        ManySeeds.setUpClass()
        ManySeeds("test_the_floor").test_the_floor()
        for ref, n in sorted(ManySeeds.floors.items()):
            print(f"{n:>3}  {ref}")
        print("empty pools:", ManySeeds.empty, "seeds:", len(ManySeeds.runs))
    else:
        unittest.main()
