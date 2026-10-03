"""
test_trope_claims.py — build item 7c-3: the trope breaks and the question under the claims (docs/p1-build-7c.md,
part 7c-3; docs/p1-tags.md). Eight rows left, six joined; claims, further clashes, overrides (data only), fits as
weights and merge rules row by row; the removed ids are nowhere in the committed data; thousands of seeds of today's
P1 preroll hold no clash pair, empty no pool and keep the trope break's two draws apart and above the floor.
"""

import itertools
import sys
import unittest

from _campaign import SCRIPTS
import _floor

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

BREAKS = {r["id"]: r for r in dt.rows("trope-breaks.yaml")}
REG = dt.claims_registry()
GONE = ("break_sacred_beast", "break_humans_minority", "break_world_is_young", "break_children_are_rare", "break_elves_are_new",
        "break_goblins_are_merchants", "break_gods_need_witnesses", "break_giants_are_peasants")
JOINED = ("break_no_common_tongue", "break_gods_among_mortals", "break_lawless_day", "break_casting_forbidden",
          "break_ruins_forbidden", "break_night_forbidden")
SURFACE = {"dial": {"era": ["medieval", "renaissance", "ancient", "nautical"]}}


class Rows(unittest.TestCase):

    def test_eight_left_and_six_joined(self):
        self.assertEqual(len(BREAKS), 31)
        self.assertFalse(set(GONE) & set(BREAKS))
        for rid in JOINED:
            r = BREAKS[rid]
            self.assertTrue(r["statement"] and r["tr"]["name"] and r["tr"]["at_table"], rid)
            self.assertGreaterEqual(len(r["hooks"]), 2, rid)
        self.assertEqual({k for k in JOINED if BREAKS[k].get("prohibition")},
                         {"break_casting_forbidden", "break_ruins_forbidden", "break_night_forbidden"})

    def test_the_removed_rows_are_nowhere_in_the_committed_data(self):
        for path in sorted(dt.tables_dir().iterdir()):
            if path.suffix in (".yaml", ".json") and not path.name.startswith("_"):
                text = path.read_text(encoding="utf-8")
                for rid in GONE:
                    self.assertNotIn(rid, text, path.name)

    def test_no_row_carries_the_unread_tags_or_the_old_override_shape(self):
        for rid, r in BREAKS.items():
            self.assertNotIn("tags", r, rid)
            self.assertIsInstance(r.get("overrides", []), list, rid)

    def test_the_claims(self):
        self.assertEqual({k: r["claims"] for k, r in BREAKS.items() if r.get("claims")},
                         {"break_rule_by_lottery": {"rule": "by_lot"},
                          "break_no_kings_only_guilds": {"nobility": "none", "rule": "guild_council"},
                          "break_war_is_ritual": {"war": "by_champions"}, "break_magic_is_nobility": {"nobility": "exists"},
                          "break_dragons_rule": {"rule": "dragon_sovereign"}})

    def test_the_further_clashes_and_requirements(self):
        self.assertEqual({k: r["conflicts_with"] for k, r in BREAKS.items() if r.get("conflicts_with")},
                         {"break_rule_by_lottery": ["tension_inheritance_merit"], "break_magic_is_nobility": ["break_casting_forbidden"],
                          "break_gods_are_ancestors_known": ["ruin_dead_god"],
                          "break_underground_forbidden": ["claim:below_ground=lived_in"],
                          "break_ruins_forbidden": ["layout:remnant_on_heart"], "break_no_writing": ["claim:writing=printed"],
                          "break_casting_forbidden": ["break_magic_is_nobility"]})
        self.assertEqual({k: r["requires"] for k, r in BREAKS.items() if r.get("requires")},
                         {"break_night_is_safe": SURFACE, "break_night_forbidden": SURFACE,
                          "break_casting_forbidden": {"dial": {"magic": ["low", "medium"]}}})
        tie = {r["id"]: r for r in dt.rows("trope-breaks.yaml#tie")}
        self.assertEqual(tie["tie_break"]["conflicts_with"], ["time_coming"])

    def test_the_overrides_name_their_defaults(self):
        got = {k: [o["default"] for o in r["overrides"]] for k, r in BREAKS.items() if r.get("overrides")}
        self.assertEqual(got, {
            "break_rule_by_lottery": ["state_succession", "ruler_heir", "politics_node_kinds"],
            "break_no_kings_only_guilds": ["forced_state_faction", "seat_of_rule_anchor", "politics_node_kinds"],
            "break_war_is_ritual": ["contest_last_step", "war_node_kinds", "martial_assets"],
            "break_magic_is_nobility": ["regulator_identity", "caster_share", "primer_public_casting"],
            "break_dragons_rule": ["state_leader"], "break_monsters_have_treaties": ["site_attitude_pool"],
            "break_lineage_homes_inverted": ["lineage_palette_weights"], "break_gods_are_ancestors_known": ["pantheon_type"],
            "break_gods_among_mortals": ["great_gods_floor", "pantheon_type"], "break_cities_dangerous": ["travel_danger"],
            "break_dungeons_inhabited": ["site_attitude_pool"], "break_the_enemy_won": ["state_identity"],
            "break_dead_month": ["weekly_volatility"], "break_iron_is_sacred": ["era_equipment"],
            "break_maps_are_illegal": ["player_map"], "break_no_writing": ["loot_writing"],
            "break_no_common_tongue": ["second_language"], "break_casting_forbidden": ["regulator_strictness", "regulator_identity"]})
        for defaults in got.values():
            self.assertFalse(set(defaults) - set(REG["defaults"]))

    def test_the_one_override_the_preroll_applies_is_the_ancestor_gods(self):
        """P2 forces the pantheon type a trope break names (unchanged behaviour, read from the list form); every
        other override is data only."""
        ov = BREAKS["break_gods_are_ancestors_known"]["overrides"]
        self.assertEqual(ov, [{"default": "pantheon_type", "to": "pantheon_ancestor_gods"}])
        self.assertIsNotNone(dt.row("pantheon.yaml#type", "pantheon_ancestor_gods"))
        dials = {"scale": "short", "tone": "shadowed", "magic": "low", "era": "medieval", "content_mix": ["war", "mystery", "horror"],
                 "party_size": 2, "level_band": [1, 5]}
        for forced, breaks in (("pantheon_ancestor_gods", ["break_gods_are_ancestors_known"]), (None, ["break_gods_among_mortals"])):
            R = designer.Roller.in_memory("P2-OVERRIDE", dials, phase="P2")
            m = {"dials": dials, "dice_log": [{"phase": "P1", "table": "trope-breaks.yaml", "label": "break.1", "row_id": b} for b in breaks]}
            designer.preroll_p2(R, m)
            rec = R.by_label["pantheon_type"]
            self.assertEqual(rec.get("notation") == "forced", forced is not None, breaks)
            if forced:
                self.assertEqual(rec["row_id"], forced)

    def test_the_fits_are_weights(self):
        def w(rid, **ctx):
            return arb.weight_of(BREAKS[rid], arb.Context(**ctx))
        self.assertEqual(w("break_border_forbidden", rolled={"contest_open_close_road": False}), 3)
        self.assertEqual(w("break_border_forbidden", rolled={"spine_long_wall": False, "contest_forbidden_lands": False}), 4)
        self.assertEqual(w("break_ruins_forbidden", rolled={"contest_sealed_remnant": False}), 3)
        self.assertEqual(w("break_the_enemy_won", rolled={"contest_occupier_resistance": False, "ruin_besieged_land": False}), 6)
        self.assertEqual(w("break_moon_trades", dials={"era": "nautical"}), 2)
        self.assertEqual(w("break_iron_is_sacred", dials={"era": "ancient"}, rolled={"life_iron_coal": False}), 4)
        self.assertEqual(w("break_maps_are_illegal", dials={"content_mix": ["exploration", "war", "horror"]}), 2)
        self.assertEqual(w("break_casting_forbidden", dials={"magic": "low"}, rolled={"contest_casters_casterless": False}), 4)
        self.assertEqual(w("break_underground_forbidden", rolled={"land_underground": False, "life_deep_lake": False}), 4)
        self.assertEqual(w("break_gods_among_mortals", rolled={"ruin_dead_god": False}), 2)
        self.assertEqual(w("break_monsters_have_treaties", rolled={"contest_humans_fey": False}), 2)
        guild = BREAKS["break_no_kings_only_guilds"]["weight_by"][0]["when"]["any_of"]
        contests = {r["id"]: r for r in dt.rows("foundation.yaml#contest")}
        self.assertEqual(set(guild), {k for k, r in contests.items() if "guild" in (r["roles"]["a"]["hint"], r["roles"]["b"]["hint"])})
        for rid in ("break_beasts_own_land", "break_lineage_homes_inverted", "break_night_is_safe", "break_lawless_day", "break_no_direct_lies"):
            self.assertNotIn("weight_by", BREAKS[rid], rid)

    def test_the_merge_rules_and_the_combine_lines(self):
        self.assertEqual({k: sorted(r["merges_with"]) for k, r in BREAKS.items() if r.get("merges_with")},
                         {"break_dragons_rule": ["contest_humans_dragon"], "break_the_enemy_won": ["contest_occupier_resistance"],
                          "break_iron_is_sacred": ["life_famous_steel", "life_iron_coal"],
                          "break_magic_is_nobility": ["contest_casters_casterless"], "break_casting_forbidden": ["contest_casters_casterless"]})
        combines = {(c["default"], frozenset(c["rows"])) for c in REG["combines"]}
        self.assertIn(("regulator_identity", frozenset({"break_magic_is_nobility", "contest_casters_casterless"})), combines)
        self.assertIn(("regulator_identity", frozenset({"break_casting_forbidden", "contest_casters_casterless"})), combines)
        self.assertIn(("regulator_strictness", frozenset({"break_casting_forbidden", "contest_casters_casterless"})), combines)

    def test_the_text_changes_on_kept_rows(self):
        beast = BREAKS["break_beasts_own_land"]
        self.assertEqual(beast["label"], "Some lands' lord is a beast-person")
        self.assertEqual(beast["tr"]["name"], "bazı toprakların beyi bir hayvan-insandır")
        for word in ("curse", "contagion", "alignment"):
            self.assertNotIn(word, beast["statement"])
        hooks = lambda rid: {h["phase"]: h["must"] for h in BREAKS[rid]["hooks"]}
        self.assertEqual(hooks("break_beasts_own_land")["P3"], "a beast-lord holds one part of the map; its travel table is negotiated passage")
        self.assertIn("sworn treaties", BREAKS["break_monsters_have_treaties"]["statement"])
        self.assertEqual(hooks("break_moon_trades")["P4"], "a trade faction holds the right to the moon trade")
        self.assertIn("the moon is one of the touched planes", hooks("break_moon_trades")["P2"])
        self.assertEqual(hooks("break_dungeons_inhabited")["P6"], "every site's inhabitants answer the door; no site's attitude is kill or ignore")
        self.assertEqual(hooks("break_night_is_safe")["P6"], "the ecology's apex hunts by day")

    def test_the_question_rows_gained_their_family(self):
        fam = {r["id"]: r["families"] for r in dt.rows("tensions.yaml")}
        for tid in ("tension_winning_being_right", "tension_ambition_contentment", "tension_justice_peace"):
            self.assertIn("two_hands", fam[tid])
        for tid in ("tension_power_self", "tension_one_many", "tension_security_freedom"):
            self.assertIn("hidden_hand", fam[tid])
        self.assertEqual(len(fam), 33)


class ManySeeds(unittest.TestCase):
    """Today's P1 preroll over every scale, magic and era."""

    @classmethod
    def setUpClass(cls):
        cls.runs = []
        cls.prohibition_floor = 99
        prohibitions = [r for r in BREAKS.values() if r.get("prohibition")]
        real = arb.arbitrate

        def spy(ref, rows, ctx, **kw):
            res = real(ref, rows, ctx, **kw)
            if ref == "trope-breaks.yaml":
                idx = dt.conflict_index()
                free = [r for r in prohibitions
                        if arb.constraint_reason(r, ctx, set(kw.get("exclude") or ()), kw.get("where"), kw.get("why", "where"), idx) is None]
                cls.prohibition_floor = min(cls.prohibition_floor, len(free))
            return res
        arb.arbitrate = spy
        try:
            combos = list(itertools.product(dt.dial_values("scale"), dt.dial_values("magic"), dt.dial_values("era"), dt.dial_values("tone")))
            mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
            for i in range(1620):
                scale, magic, era, tone = combos[i % len(combos)]
                dials = {"scale": scale, "magic": magic, "era": era, "tone": tone, "content_mix": list(mixes[i % len(mixes)]),
                         "party_size": 2, "level_band": [1, 1 + _floor.SPAN[scale]]}
                R = designer.Roller.in_memory(f"TROPE-{i}", dials)
                designer.preroll_p1(R, {"dials": dials})       # an empty pool would raise SystemExit
                cls.runs.append((dials, R))
        finally:
            arb.arbitrate = real

    def breaks(self, R):
        return [r["row_id"] for r in R.public if r["label"].startswith("break.")]

    def test_no_clash_pair_stands_together(self):
        seen = set()
        for dials, R in self.runs:
            rows = [r["row_id"] for r in R.public + R.secret if r.get("row_id")]
            self.assertEqual(arb.conflicting_pairs(rows, tokens=R.ctx.tokens, exempt=R.exempt), [], R.master)
            b = set(self.breaks(R))
            seen |= b
            if dials["era"] == "underground":
                self.assertFalse(b & {"break_night_is_safe", "break_night_forbidden", "break_underground_forbidden"}, R.master)
            if dials["era"] == "renaissance":
                self.assertNotIn("break_no_writing", b)
            if dials["magic"] == "high":
                self.assertNotIn("break_casting_forbidden", b)
            if "claim:below_ground=lived_in" in R.ctx.tokens:
                self.assertNotIn("break_underground_forbidden", b, R.master)
            if "layout:remnant_on_heart" in R.ctx.tokens:
                self.assertNotIn("break_ruins_forbidden", b, R.master)
        self.assertEqual(seen, set(BREAKS), "every trope break is still drawn")

    def test_the_two_draws_stay_above_the_floor_and_apart(self):
        first = min(R.pool_of["break.1"] for _, R in self.runs)
        second = min(R.pool_of["break.2"] for d, R in self.runs if d["scale"] != "short")
        self.assertGreaterEqual(first, 5)
        self.assertGreaterEqual(second, 5)
        fam = {k: r["family"] for k, r in BREAKS.items()}
        for dials, R in self.runs:
            b = self.breaks(R)
            self.assertEqual(len(b), 1 if dials["scale"] == "short" else 2)
            self.assertEqual(len({fam[x] for x in b}), len(b), "families_distinct holds")
        self.__class__.report = (first, second)

    def test_the_prohibition_rows_keep_a_pool(self):
        self.assertGreaterEqual(self.prohibition_floor, 1)
        self.assertLessEqual(self.prohibition_floor, 8)


if __name__ == "__main__":
    unittest.main()
