"""
test_threat.py — build item 18c, part 1 (docs/p1-build-18.md, Part 18c sections 4-5; docs/p1-build-18-rows.md
sections 4 and 8): the threat's tables; its roll after the contest and before the move; the creature inside the band's
CR window or a reskin; the god only above short; a power source on every humanoid family above short; the goal bound
to a piece and joined to the contest; the weakness and the lair fitted; the chooser and the tie retired; no dead end
over 3,000 seeds; the variety report.

Failure messages give counts and positions only: no row of a secret table is printed.

  py test_threat.py --report     the variety report (1,000 seeds per scale, a three-birth wait simulated)
"""

import itertools
import sys
import unittest
from collections import Counter, deque

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_tables as dt  # noqa: E402
import design_threat as dth  # noqa: E402
import designer  # noqa: E402
import _corpus  # noqa: E402  (build item 18f-1: the shared many-seed corpus)

V = "antagonists.yaml#"
SEEDS = 3000
SPAN = {"short": 4, "standard": 11, "epic": 19}
FAMILIES = {r["id"]: r for r in dt.rows(V + "villain_family")}
HUMANOID = {k for k, r in FAMILIES.items() if r.get("power_source")}


def dial_sets():
    return list(itertools.product(dt.dial_values("scale"), dt.dial_values("magic"), dt.dial_values("era"), dt.dial_values("tone")))


def births(n: int, tag: str, wait: bool = False, scale: str | None = None, start_levels=(1, 4, 7, 10)):
    """In-memory P1 prerolls; `wait` simulates the family's three-birth wait across the sequence."""
    combos = [c for c in dial_sets() if scale is None or c[0] == scale]
    mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
    last = deque(maxlen=3)
    out = []
    for i in range(n):
        sc, magic, era, tone = combos[i % len(combos)]
        lo = start_levels[(i // len(combos)) % len(start_levels)]
        d = {"scale": sc, "magic": magic, "era": era, "tone": tone, "content_mix": list(mixes[i % len(mixes)]),
             "party_size": 2, "level_band": [lo, min(20, lo + SPAN[sc])]}
        R = designer.Roller.in_memory(f"{tag}-{i}", d)
        if wait:
            R._usage = lambda ref, avoid, last=set(last): {"row_wait": set(last)} if ref == V + "villain_family" else {}
        designer.preroll_p1(R, {"dials": d})
        last.append(R.threat["family"])
        out.append((d, R))
    return out


class Tables(unittest.TestCase):

    def test_the_counts(self):
        want = {"villain_family": 19, "power_source": 5, "goal": 20, "weakness": 19, "lair_form": 16, "lair_where": 7,
                "villain_shape": 19, "origin": 12, "visibility": 5, "break_tie": 0}
        self.assertEqual({k: len(dt.rows(V + k)) for k in want}, want)
        self.assertEqual(len(dt.rows("secrets.yaml#chooser")), 0, "the villain always chose")
        self.assertEqual(len(dt.retired("secrets.yaml#chooser")), 6)
        self.assertEqual(len(dt.retired(V + "break_tie")), 6)
        for sub in want:
            self.assertTrue(dt.roll_header(V + sub).get("secret"), sub)

    def test_the_retired_and_the_added_rows_of_the_specification(self):
        """docs/p1-build-18.md, Part 18c section 5 names them."""
        self.assertEqual({r["id"] for r in dt.retired(V + "villain_shape")}, {"shape_process", "shape_institution"})
        self.assertEqual({r["id"] for r in dt.retired(V + "origin")}, {"origin_taken_by_phenomenon", "origin_made_by_institution"})
        self.assertEqual({r["id"] for r in dt.retired(V + "visibility")}, {"vis_process_or_institution"})
        self.assertIsNotNone(dt.row(V + "origin", "origin_forbidden_knowledge"))
        self.assertIsNotNone(dt.row(V + "visibility", "vis_known_unknown_where"))
        retired = {r["id"] for sub in ("villain_shape", "origin", "visibility", "break_tie") for r in dt.retired(V + sub)}
        retired |= {r["id"] for r in dt.retired("secrets.yaml#chooser")}
        for name in dt.list_tables():
            for lst in dt.all_row_lists(dt.load(name)).values():
                for r in lst:
                    self.assertFalse(set(r.get("conflicts_with") or []) & retired, "an active row names a retired one")

    def test_every_creature_is_srd_and_every_family_reaches_a_creature(self):
        srd = dth.srd_creatures()
        for n, (fid, f) in enumerate(FAMILIES.items()):
            for c in list(f.get("creatures") or []) + list(f.get("reskin") or []):
                self.assertIn(c, srd, f"family {n}: an index that is no SRD creature")
            self.assertTrue(f.get("creatures") or f.get("avatar"), f"family {n}")
            for top in range(5, 21):            # every band top a birth can have: a creature, or a reskin base
                self.assertTrue(dth.candidates(f, top) or f.get("reskin"), f"family {n} at level {top}: no creature and no reskin")
            self.assertIn(f["creature_type"], ("humanoid", "undead", "dragon", "fiend", "aberration", "giant", "fey",
                                               "monstrosity", "elemental", "celestial", "god"))
        self.assertEqual(len(HUMANOID), 5, "mage, ruler, shadow, dark priest, lycanthrope")
        self.assertEqual(sum(1 for f in FAMILIES.values() if f["creature_type"] == "dragon"), 2)
        self.assertFalse(any(f.get("weight_by") for f in FAMILIES.values() if f["creature_type"] == "dragon"), "the dragons' share")

    def test_the_cr_window(self):
        self.assertEqual(dth.cr_window(5), (3.0, 9.0))
        self.assertEqual(dth.cr_window(12), (10.0, 16.0))
        self.assertEqual(dth.cr_window(16), (14.0, 20.0))
        self.assertEqual(dth.cr_window(17), (15.0, 30.0))
        self.assertEqual(dth.cr_window(3), (2.0, 7.0))

    def test_every_family_has_a_lair_and_a_weakness(self):
        forms = dt.rows(V + "lair_form")
        weaks = dt.rows(V + "weakness")
        for n, (fid, f) in enumerate(FAMILIES.items()):
            self.assertTrue(any(fid in (r.get("fits") or []) for r in forms), f"family {n}: no lair form")
            self.assertGreaterEqual(sum(1 for r in weaks if dth.weakness_fits(r, f)), 4, f"family {n}: few weaknesses")
        forms = dt.rows(V + "lair_form")
        for n, f in enumerate(FAMILIES):
            self.assertGreaterEqual(sum(1 for r in forms if f in r["fits"]), 5, f"family {n}: the lair forms' floor")
        self.assertEqual(dt.row(V + "weakness", "weak_law_of_nature")["fits"], ["family_undead", "family_hag_fey"])
        god = FAMILIES["family_god"]
        self.assertEqual(sum(1 for r in weaks if dth.weakness_fits(r, god)), 7, "the god's seven (rows 4.5 and the 18c-1 answer)")
        for n, f in enumerate(FAMILIES.values()):
            self.assertGreaterEqual(sum(1 for r in weaks if dth.weakness_fits(r, f)), 5, f"family {n}: the floor")
        self.assertEqual({r["id"] for r in dt.rows(V + "goal") if r.get("role_goal")},
                         {"goal_side_as_weapon", "goal_destroy_bloodline", "goal_avenge_wrong"})
        true_name = dt.row(V + "weakness", "weak_true_name")
        self.assertEqual({FAMILIES[f]["creature_type"] for f in true_name["fits"]}, {"fiend", "fey", "elemental", "god"})


class ManySeeds(unittest.TestCase):
    """3,000 seeds over every scale × magic × era × tone × content mix and four start levels: no dead end (an empty
    pool stops the preroll), and every rule of the threat holds."""

    @classmethod
    def setUpClass(cls):
        cls.runs = _corpus.births(SEEDS)      # the shared corpus (build item 18f-1)

    def test_the_order(self):
        for d, R in self.runs:
            pos = {lab: i for i, lab in enumerate(R.by_label)}      # the order the rolls were kept in
            self.assertLess(pos["foundation.contest.1"], pos["threat.family"])
            self.assertLess(pos["threat.lair_where"], pos["foundation.break.target"])
            self.assertLess(pos["threat.family"], pos["break.1"], "the threat before the trope breaks (G4)")

    def test_the_creature_fits_the_band(self):
        srd = dth.srd_creatures()
        reskins = Counter()
        for d, R in self.runs:
            th = R.threat
            lo, hi = dth.cr_window(int(d["level_band"][1]))
            c = th["creature"]
            fam = FAMILIES[th["family"]]
            if "reskin" in c:
                reskins[d["scale"]] += 1
                self.assertTrue(lo <= c["reskin"]["target_cr"] <= hi)
                self.assertIn(c["reskin"]["base"], fam["reskin"])
                self.assertFalse(dth.candidates(fam, int(d["level_band"][1])) and not fam.get("avatar"), "a reskin only where none fits")
            else:
                self.assertTrue(lo <= srd[c["index"]]["cr"] <= hi)
                self.assertIn(c["index"], fam["creatures"])
        type(self).reskins = reskins

    def test_the_god_and_the_power_source(self):
        for d, R in self.runs:
            th = R.threat
            if d["scale"] == "short":
                self.assertNotEqual(th["family"], "family_god")
            if th["family"] == "family_god":
                self.assertTrue(th["creature"].get("avatar"))
            self.assertEqual(th["power_source"] is not None, th["family"] in HUMANOID and d["scale"] != "short")

    def test_the_goal_is_joined_to_the_contest(self):
        for d, R in self.runs:
            g = R.threat["goal"]
            row = dt.row(V + "goal", g["id"])
            self.assertIn(g["piece"], row["pieces"])
            if g["piece"] == "thin_place":
                self.assertIn("land_thin_place", R.foundation["palette"] + R.foundation["palette_extra"])
            main = R.foundation["layout"]["contests"][0]
            if g["join"] == "prize":
                self.assertEqual(dth.prize_piece(main["prize"]["kind"]), g["piece"])
            elif g["join"] == "role_goal":
                self.assertEqual(g["piece"], "role")
                self.assertTrue(row.get("role_goal"))
            else:
                # 18c-2's move honours it (it strikes the prize's piece or a contest role); 18c-1's break is not held to it
                self.assertEqual(g["join"], "move")
                self.assertNotIn(dth.prize_piece(main["prize"]["kind"]), row["pieces"])
                self.assertFalse(row.get("role_goal"))

    def test_the_weakness_and_the_lair_fit(self):
        for d, R in self.runs:
            th = R.threat
            fam = FAMILIES[th["family"]]
            self.assertTrue(dth.weakness_fits(dt.row(V + "weakness", th["weakness"]), fam))
            form = dt.row(V + "lair_form", th["lair"]["form"])
            where = dt.row(V + "lair_where", th["lair"]["where"])
            self.assertIn(th["family"], form["fits"])
            self.assertTrue(dth.where_fits(where, form, R.foundation["palette"] + R.foundation["palette_extra"]))

    def test_the_chooser_and_the_tie_are_not_rolled(self):
        for d, R in self.runs:
            labels = {r["label"] for r in R.secret}
            self.assertFalse(labels & {"secret_chooser", "secret_chooser.role", "bbeg_tie"})
            self.assertEqual(R.identity_secret["secret"]["chooser"], "chooser_the_villain")
            self.assertIsNone(R.identity_secret["villain"]["tie"])
            self.assertEqual(R.identity_secret["villain"]["shape"], R.threat["shape"])

    def test_a_world_state_joins_the_threat_only_when_the_villain_is_public(self):
        """The 18c-1 audit: a join to the threat counts only when the villain itself is known."""
        joined = Counter()
        for d, R in self.runs:
            self.assertNotIn("world_states", R.identity_secret)
            for b in R.identity["trope_breaks"]:
                j = b.get("join") or {}
                if j.get("piece") != "threat":
                    continue
                self.assertIn(R.threat["visibility"], dth.PUBLIC_VISIBILITY)
                req = j["threat"]
                if req.get("creature"):
                    self.assertEqual(R.threat["creature_type"], req["creature"])
                if req.get("family"):
                    self.assertEqual(R.threat["family"], "family_" + req["family"])
                joined[b["id"]] += 1
        self.assertTrue(joined, "some world state joins a known villain")

    def test_the_dragon_s_colour_weighs_its_lair(self):
        """The 18c-1 audit, answer 5: x3 on the colour's lairs, not a filter."""
        red = {r["id"] for r in dt.rows(V + "lair_form") if "red" in (r.get("dragon_colours") or [])}
        self.assertEqual(red, {"lair_volcano", "lair_cavern", "lair_ruined_fortress"})
        hits = total = 0
        for d, R in self.runs:
            idx = str(R.threat["creature"].get("index") or "")
            if "-red-dragon" in idx:
                total += 1
                hits += R.threat["lair"]["form"] in red
        self.assertGreater(total, 10)
        self.assertGreater(hits / total, 0.6, "the red dragon's lairs weigh x3")

    def test_every_family_is_drawn(self):
        drawn = Counter(R.threat["family"] for d, R in self.runs)
        self.assertEqual(set(drawn), set(FAMILIES))


class Variety(unittest.TestCase):
    """The variety report's own rule: with the three-birth wait, a family never comes twice in a row."""

    def test_no_family_twice_in_a_row(self):
        runs = births(300, "VARIETY", wait=True)
        fams = [R.threat["family"] for d, R in runs]
        self.assertEqual(sum(1 for a, b in zip(fams, fams[1:]) if a == b), 0)


def report() -> str:
    lines = []
    for scale in ("short", "standard", "epic"):
        runs = births(1000, f"VARIETY-{scale}", wait=True, scale=scale)
        fams = [R.threat["family"] for d, R in runs]
        share = Counter(fams)
        sets = {(R.threat["family"], str(R.threat["creature"].get("index") or R.threat["creature"]["reskin"]["base"]),
                 R.threat["shape"], R.threat["goal"]["id"]) for d, R in runs}
        reskin = sum(1 for d, R in runs if "reskin" in R.threat["creature"])
        prize = sum(1 for d, R in runs if R.threat["goal"]["join"] == "prize")
        role = sum(1 for d, R in runs if R.threat["goal"]["join"] == "role_goal")
        lines.append(f"{scale}: {len(share)} families drawn; share max {max(share.values()) / 10:.1f} %, min {min(share.values()) / 10:.1f} %; "
                     f"consecutive repeats {sum(1 for a, b in zip(fams, fams[1:]) if a == b)}; distinct (family, creature, shape, goal) "
                     f"{len(sets)} of 1,000; reskins {reskin / 10:.1f} %; the join: prize {prize / 10:.1f} %, role goal {role / 10:.1f} %, "
                     f"move {(1000 - prize - role) / 10:.1f} %")
    return "\n".join(lines)


if __name__ == "__main__":
    if "--report" in sys.argv:
        print(report())
    else:
        unittest.main()
