"""
test_general_themes.py — build item 16b (docs/p1-build-16.md, Parts 1 to 3; errata 24.2 #31): the thirty-one public
rows of the general themes exist with their families, labels and statements as approved, carry their technical
fields in the pattern of their tables, and every ruled pair is data (a fit is a weight, a clash a conflict or a
claim, a merge a `merges_with` line, a requirement a `requires`). The many-seeds proof is in test_identity_roll.
"""

import sys
import unittest

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_foundation as fd  # noqa: E402
import design_tables as dt  # noqa: E402

F = "foundation.yaml#"
RUIN = {r["id"]: r for r in dt.rows(F + "ruin_source")}
CONTEST = {r["id"]: r for r in dt.rows(F + "contest")}
LIFE = {r["id"]: r for r in dt.rows(F + "lifeline")}
BREAK = {r["id"]: r for r in dt.rows("trope-breaks.yaml")}
PRACTICE = {r["id"]: r for r in dt.rows("signatures.yaml#institution_practice")}
DOC = dt.load("foundation.yaml")
REMNANT_KINDS = {r["remnant_kind"] for k, r in RUIN.items()}

RUINS = {"ruin_kingdom_of_the_dead": "fallen_kingdoms", "ruin_devils_bargain": "planes", "ruin_demon_gate": "planes",
         "ruin_deep_minds": "old_peoples", "ruin_bound_elements": "magic", "ruin_sundered_relic": "magic", "ruin_dark_lords_fall": "wars",
         "ruin_sleeper": "old_peoples", "ruin_empire": "fallen_kingdoms", "ruin_great_curse": "catastrophe", "ruin_beast_blood": "old_peoples",
         "ruin_sleeping_realm": "planes", "ruin_fallen_order": "wars"}
# contest: (family, prize, the four hints)
CONTESTS = {"contest_living_dead": ("nonhuman", "heart", ("state", None, "religious", "trade")),
            "contest_fiend_pact": ("hidden_hand", "lifeline", ("state", "state", None, "martial")),
            "contest_elemental_lord": ("nonhuman", "lifeline", ("state", None, "religious", "scholarly")),
            "contest_relic_pieces": ("race", "new", ("state", "state", "religious", None)),
            "contest_prophecy": ("open_close", "new", ("religious", "state", "scholarly", None)),
            "contest_dark_lord": ("strong_weak", "heart", ("state", "state", "trade", "resistance")),
            "contest_two_empires": ("two_hands", "heart", (None, None, "state", "resistance")),
            "contest_coven": ("nonhuman", "lifeline", ("state", "resistance", None, None)),
            "contest_pirates": ("strong_weak", "lifeline", ("criminal", "trade", "martial", "criminal")),
            "contest_slavers": ("strong_weak", "new", ("criminal", "resistance", "trade", None)),
            "contest_thieves_guild": ("strong_weak", "heart", ("criminal", "state", "criminal", "martial"))}
BREAKS = {"break_dead_rise": "danger", "break_chosen_are_many": "gods", "break_dreams_are_a_place": "danger",
          "break_oath_curse": "knowledge", "break_magic_sold": "knowledge"}


def weights(r):
    return {x: w["x"] for w in r.get("weight_by") or [] for x in (w["when"].get("any_of") or [])}


class Rows(unittest.TestCase):

    def test_thirty_one_rows(self):
        self.assertEqual(len(RUINS) + len(CONTESTS) + len(BREAKS) + 2, 31)
        self.assertEqual((len(RUIN), len(CONTEST), len(BREAK), len(LIFE), len(PRACTICE)), (53, 51, 36, 61, 34))

    def test_the_ruin_sources(self):
        old_kinds = {r["remnant_kind"] for k, r in RUIN.items() if k not in RUINS}
        for rid, family in RUINS.items():
            r = RUIN[rid]
            self.assertEqual(r["family"], family, rid)
            self.assertTrue(r["statement"].endswith("."), rid)
            self.assertIn(r["remnant_kind"], old_kinds, f"{rid}: a kind the break's compatibility tables know")
            self.assertTrue(2 <= len(r["olgu_families"]) <= 3, rid)
            self.assertFalse(set(r["olgu_families"]) - set(DOC["phenomenon_rule_families"]), rid)
            self.assertNotIn("born_of_break", r["olgu_families"], rid)
            self.assertTrue(r["sites"] and all(s.startswith("site_") for s in r["sites"]), rid)
            self.assertEqual(set(r["text"]), {"name", "what", "remnant", "sites", "strangeness"}, rid)
        self.assertEqual(RUIN["ruin_deep_minds"]["requires"], {"any_of": ["land_coast", "land_island", "land_lake", "land_underground"]})
        self.assertFalse([k for k in RUINS if RUIN[k].get("requires") and k != "ruin_deep_minds"])
        for rid in ("ruin_devils_bargain", "ruin_demon_gate", "ruin_sleeping_realm"):
            self.assertTrue(any(h["phase"] == "P2" and "touched planes" in h["must"] for h in RUIN[rid]["hooks"]), rid)
        self.assertFalse(any(RUIN[k].get("claims") for k in RUINS), "none carries a claim")

    def test_the_contests(self):
        for cid, (family, prize, hints) in CONTESTS.items():
            r = CONTEST[cid]
            self.assertEqual((r["family"], r["prize"]), (family, prize), cid)
            self.assertEqual(tuple(r["roles"][k]["hint"] for k in ("a", "b", "third", "fourth")), hints, cid)
            self.assertTrue(2 <= len(r["escalation"]) <= 3, cid)
            self.assertFalse(r.get("claims") or any(role.get("claims") for role in r["roles"].values()), f"{cid} carries no claim")
            for roles in fd.header("contest")["roles_by_scale"].values():
                self.assertTrue(fd.institution_homes(r, roles), f"{cid}: a seated role can house the institution")
        self.assertEqual(CONTEST["contest_relic_pieces"]["prize_with"], {"ruin_sundered_relic": "remnant"})
        self.assertTrue(CONTEST["contest_fiend_pact"]["third_is_rumour"])
        self.assertEqual(CONTEST["contest_elemental_lord"]["roles"]["fourth"]["text"], "the binders who would chain it again")
        self.assertTrue(CONTEST["contest_slavers"]["roles"]["fourth"]["people_role"])
        self.assertEqual(CONTEST["contest_pirates"]["requires"], {"any_of": ["land_coast", "land_island"]})
        self.assertEqual(CONTEST["contest_thieves_guild"]["seats"], {"a": "heart"})

    def test_the_trope_breaks(self):
        for bid, family in BREAKS.items():
            r = BREAK[bid]
            self.assertEqual(r["family"], family, bid)
            self.assertTrue(r["statement"] and r["text"]["name"] and r["text"]["at_table"], bid)
            self.assertGreaterEqual(len({h["phase"] for h in r["hooks"]}), 2, bid)
            self.assertFalse(r.get("prohibition"), bid)
        sold = BREAK["break_magic_sold"]
        self.assertEqual(sold["claims"], {"magic": "plentiful"})
        self.assertEqual(sold["requires"], {"dial": {"magic": ["medium", "high"]}}, "a clash against the dial at low: not drawn")
        self.assertEqual(sold["conflicts_with"], ["ruin_dried_source"])
        self.assertFalse([b for b in BREAKS if BREAK[b].get("conflicts_with") and b != "break_magic_sold"])

    def test_the_lifeline_and_the_practice(self):
        life, pr = LIFE["life_enchanters"], PRACTICE["practice_enchanted_goods"]
        self.assertEqual((life["family"], life["label"]), ("craft", "The enchanters' workshops"))
        self.assertEqual(life["requires"], {"dial": {"magic": ["medium", "high"]}})
        self.assertEqual(set(life["text"]), {"name", "who", "yields", "weak_point", "sense"})
        self.assertEqual((sorted(pr["hints"]), pr["requires"]), (["guild", "trade"], {"dial": {"magic": ["medium", "high"]}}))
        self.assertEqual(pr["text"]["gives"], "enchanted goods to buy and to order")


class Pairs(unittest.TestCase):
    """Every ruled pair of the three parts; a pair ruled "no clash" has nothing."""

    def test_the_fits(self):
        self.assertEqual(weights(BREAK["break_dead_rise"]), {"contest_living_dead": 2, "ruin_plague": 2})
        self.assertEqual(weights(CONTEST["contest_relic_pieces"]), {"ruin_sundered_relic": 3})
        self.assertEqual(weights(CONTEST["contest_dark_lord"]), {"ruin_dark_lords_fall": 2})
        self.assertEqual(weights(CONTEST["contest_sealed_remnant"]).get("ruin_sleeper"), 3)
        self.assertEqual(weights(CONTEST["contest_order_schism"]).get("ruin_fallen_order"), 2)
        self.assertEqual(weights(BREAK["break_beasts_own_land"]), {"ruin_beast_blood": 2})
        self.assertEqual(weights(BREAK["break_dreams_are_a_place"]), {"ruin_sleeping_realm": 2})
        oath = weights(BREAK["break_oath_curse"])
        self.assertEqual(oath.pop("ruin_great_curse"), 2)
        self.assertEqual(oath, {r["id"]: 2 for r in LIFE.values() if r["family"] == "treaty"})
        self.assertEqual(weights(BREAK["break_magic_sold"]), {"life_enchanters": 2})
        self.assertEqual(weights(PRACTICE["practice_enchanted_goods"]), {"break_magic_sold": 2})

    def test_the_merges(self):
        self.assertEqual(BREAK["break_monsters_have_treaties"]["merges_with"]["contest_living_dead"], "the treaty people is the dead")
        self.assertIn("role a", BREAK["break_the_enemy_won"]["merges_with"]["contest_dark_lord"])
        self.assertEqual(CONTEST["contest_dark_lord"]["merges_with"], {"ruin_dark_lords_fall": "the fallen lord's dominion has risen again"})

    def test_the_no_clash_pairs_have_nothing(self):
        idx = dt.conflict_index()
        new = set(RUINS) | set(CONTESTS) | set(BREAKS) | {"life_enchanters", "practice_enchanted_goods"}
        secret = dt.secret_row_ids()
        pairs = {frozenset((a, b)) for a in new for b in idx.get(a, ()) if b not in secret and not b.startswith(dt.CLAIM)}
        self.assertEqual(pairs, {frozenset(("break_magic_sold", "ruin_dried_source"))}, "the one ruled clash that is a conflict line")
        clash = dt.clash_map()
        self.assertEqual(set(clash.get("claim:magic=plentiful", ())), {"claim:magic=faded"}, "the claim's own clash, from the registry")

    def test_a_craft_lifeline_means_the_whole_family(self):
        craft = {r["id"] for r in LIFE.values() if r["family"] == "craft"}
        self.assertIn("life_enchanters", craft)
        gnome = dt.row("signatures.yaml#people_lineage", "lineage_gnome")
        self.assertTrue(any(set(w["when"].get("any_of") or []) == craft for w in gnome["weight_by"]))
        for cid in ("contest_old_new_craft", "contest_share_keep_knowledge", "contest_split_family"):
            req = CONTEST[cid]["requires"]
            named = [set(c.get("any_of") or []) for c in (req.get("all") or [req])]
            self.assertTrue(any(craft <= n for n in named), cid)


if __name__ == "__main__":
    unittest.main()
