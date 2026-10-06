"""
test_claims.py — build item 7c-1: claims, tokens, overridable defaults (docs/p1-build-7c.md; docs/p1-tags.md).

The registry is closed; a clash pair excludes in both directions and nothing clashes by default inside a topic; a
contest role's claim is silent when the role is not seated; the layout's two tokens appear only in their cases; a
secret row's token never shows in a public record; conditions nest; overrides name registered defaults and two
overrides of one default that can be rolled together carry a combine line; every P0 and P1 row is stamped; no unique
table's pool falls under five.
"""

import itertools
import json
import random
import sys
import unittest

from _campaign import SCRIPTS, TestCampaign
import _floor

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

REG = dt.claims_registry()
TOPICS = REG["topics"]
TABLE = SCRIPTS.parent / "data" / "design" / "_test_claims.yaml"


def every_row():
    for name in dt.list_tables():
        for sub, rows in dt.all_row_lists(dt.load(name)).items():
            for r in rows:
                yield (f"{name}#{sub}" if sub else name), r


def every_claims():
    """(where, claims) for every row and every contest role that carries claims."""
    for ref, r in every_row():
        if r.get("claims"):
            yield r["id"], r["claims"]
        for key, role in (r["roles"].items() if isinstance(r.get("roles"), dict) else ()):
            if isinstance(role, dict) and role.get("claims"):
                yield f"{r['id']}.{key}", role["claims"]


def known_token(tok: str) -> bool:
    if tok in (REG.get("tokens") or {}):
        return True
    if not tok.startswith(dt.CLAIM):
        return False
    topic, _, value = tok[len(dt.CLAIM):].partition("=")
    return topic in TOPICS and value in [str(v) for v in TOPICS[topic]["values"]]


class Registry(unittest.TestCase):

    def test_six_topics_and_seven_clash_pairs(self):
        self.assertEqual({t: v["values"] for t, v in TOPICS.items()},
                         {"rule": ["hereditary", "throne", "by_lot", "guild_council", "dragon_sovereign"],
                          "nobility": ["exists", "none"], "below_ground": ["lived_in"], "writing": ["printed"],
                          "magic": ["scarce", "middling", "plentiful", "faded"], "war": ["by_armies", "by_champions"]})
        self.assertEqual(len(REG["clashes"]), 7)
        for a, b in REG["clashes"]:
            self.assertTrue(known_token(dt.CLAIM + a) and known_token(dt.CLAIM + b), (a, b))

    def test_the_registry_is_closed(self):
        for where, claims in every_claims():
            for topic, value in claims.items():
                self.assertTrue(known_token(dt.token(topic, value)), f"{where} claims {topic}={value}, which is not in claims.yaml")
        self.assertFalse(known_token("claim:rule=by_committee"))
        self.assertFalse(known_token("claim:weather=owned"))

    def test_every_token_a_row_names_is_registered(self):
        for ref, r in every_row():
            named = list(r.get("conflicts_with") or [])
            conds = [r.get("requires")] + [w.get("when") for w in r.get("weight_by") or []]
            for c in conds:
                named += list(arb._condition_ids(c))
            for x in named:
                if ":" in str(x):
                    self.assertTrue(known_token(x), f"{r['id']} names {x}")

    def test_a_clash_excludes_both_ways_and_nothing_clashes_by_default(self):
        cm = dt.clash_map()
        for a, others in cm.items():
            for b in others:
                self.assertIn(a, cm[b])
        self.assertIn("claim:rule=by_lot", cm["claim:rule=hereditary"])
        self.assertNotIn("claim:rule=by_lot", cm.get("claim:rule=throne", ()), "throne clashes with neither by_lot...")
        self.assertNotIn("claim:rule=dragon_sovereign", cm.get("claim:rule=throne", ()), "...nor dragon_sovereign")
        self.assertNotIn("claim:magic=scarce", cm.get("claim:magic=plentiful", ()), "two values of one topic never clash by default")
        self.assertEqual(dt.clashing_tokens({"magic": "middling"}), set())

    def test_the_overridable_defaults(self):
        self.assertEqual(len(REG["defaults"]), 24)
        for did, d in REG["defaults"].items():
            self.assertTrue(d["phase"] and d["what"], did)


class P0AndSpineClaims(unittest.TestCase):

    def test_the_rows_that_claim(self):
        want = {"era_renaissance": {"writing": "printed"}, "era_underground": {"below_ground": "lived_in"},
                "magic_low": {"magic": "scarce"}, "magic_medium": {"magic": "middling"}, "magic_high": {"magic": "plentiful"},
                "spine_three_depths": {"below_ground": "lived_in"}, "spine_mountain_within": {"below_ground": "lived_in"}}
        got = {}
        for name in ("dials.yaml",):
            for sub, rows in dt.all_row_lists(dt.load(name)).items():
                got.update({r["id"]: r["claims"] for r in rows if r.get("claims")})
        for sub in ("spine", "palette"):
            got.update({r["id"]: r["claims"] for r in dt.rows(f"foundation.yaml#{sub}") if r.get("claims")})
        self.assertEqual(got, want)

    def test_the_dial_rows_claims_enter_with_the_context(self):
        ctx = arb.Context(dials={"magic": "high", "era": "renaissance", "scale": "short"})
        self.assertEqual(ctx.tokens, {"claim:magic=plentiful": False, "claim:writing=printed": False})
        self.assertEqual(ctx.rolled, {}, "tokens never pose as rolled rows")
        ctx.add("spine_three_depths", False)
        self.assertTrue(ctx.has("claim:below_ground=lived_in"))


class Tokens(unittest.TestCase):

    ROWS = [{"id": "r_heir", "label": "heir", "claims": {"rule": "hereditary"}},
            {"id": "r_throne", "label": "throne", "claims": {"rule": "throne"}},
            {"id": "r_ban", "label": "ban", "conflicts_with": ["claim:below_ground=lived_in"]},
            {"id": "r_plain", "label": "plain"}]

    def conflicts(self):
        idx: dict = {}
        cm = dt.clash_map()
        for r in self.ROWS:
            for other in list(r.get("conflicts_with") or []) + [t for c in dt.claim_tokens(r.get("claims")) for t in cm.get(c, ())]:
                idx.setdefault(r["id"], set()).add(other)
                idx.setdefault(other, set()).add(r["id"])
        return {k: frozenset(v) for k, v in idx.items()}

    def pool(self, ctx, **kw):
        res = arb.arbitrate("t", self.ROWS, ctx, conflicts=self.conflicts(), secret_ids=set(), **kw)
        return [r["id"] for r in res["pool"]], res

    def test_a_row_conflicts_with_the_tokens_its_claims_clash_with(self):
        ctx = arb.Context()
        ctx.add_token("claim:rule=by_lot", False)
        ids, res = self.pool(ctx)
        self.assertEqual(ids, ["r_throne", "r_ban", "r_plain"], "hereditary clashes with by_lot; the throne does not")
        self.assertIn({"row": "r_heir", "why": "conflict", "with": "claim:rule=by_lot"}, res["excluded"])
        ctx = arb.Context()
        ctx.add_token("claim:rule=guild_council", False)
        self.assertEqual(self.pool(ctx)[0], ["r_ban", "r_plain"])

    def test_a_row_may_name_a_token_directly(self):
        ctx = arb.Context(dials={"era": "underground"})
        self.assertNotIn("r_ban", self.pool(ctx)[0], "a prohibition claims nothing, yet clashes with the token")
        self.assertTrue(arb.holds({"any_of": ["claim:below_ground=lived_in"]}, ctx))
        self.assertFalse(arb.holds({"none_of": ["claim:below_ground=lived_in"]}, ctx))
        row = {"id": "w", "label": "w", "weight_by": [{"when": {"any_of": ["claim:below_ground=lived_in"]}, "x": 3}]}
        self.assertEqual(arb.weight_of(row, ctx), 3)

    def test_a_secret_token_never_shows_in_a_public_record(self):
        ctx = arb.Context()
        ctx.add_token("claim:rule=by_lot", True)
        ids, res = self.pool(ctx)
        self.assertNotIn("r_heir", ids)
        self.assertEqual(res["excluded"], [])
        self.assertEqual(res["excluded_secret"], [{"row": "r_heir", "why": "conflict", "with": "claim:rule=by_lot"}])
        picked = arb.pick(random.Random(3), res["pool"], res["weights"])
        shown, real = arb.public_view(res, picked)
        self.assertEqual((shown["notation"], real["notation"]), ("d4", "d3"), "the die's size gives nothing away either")
        # a token a public row also sets is public
        ctx.add_token("claim:rule=by_lot", False)
        self.assertFalse(ctx.secret_of("claim:rule=by_lot"))

    def test_conflicting_pairs_expands_tokens(self):
        pairs = arb.conflicting_pairs(["r_heir", "r_plain"], conflicts=self.conflicts(), tokens=["claim:rule=by_lot"])
        self.assertEqual(pairs, [("claim:rule=by_lot", "r_heir")])
        self.assertEqual(arb.conflicting_pairs([], tokens=["claim:magic=plentiful", "claim:magic=faded"]),
                         [("claim:magic=faded", "claim:magic=plentiful")])
        self.assertEqual(arb.conflicting_pairs(["magic_high"], tokens=["claim:magic=faded"]),
                         [("claim:magic=faded", "claim:magic=plentiful"), ("claim:magic=faded", "magic_high")],
                         "a committed row's claims are expanded")

    def test_tokens_survive_in_the_dice_log_for_the_later_phases(self):
        c = TestCampaign("claims")
        try:
            m = c.json("design/design.json")
            m["dice_log"] = [{"phase": "P1", "table": "tokens", "label": "foundation.contest.1.claims", "attempt": 1,
                              "tokens": ["claim:rule=hereditary"]},
                             {"phase": "P1", "table": "foundation.yaml#spine", "label": "foundation.spine", "attempt": 1,
                              "row_id": "spine_three_depths"}]
            c.write_json("design/design.json", m)
            c.write_json("design/dm-only/dice-log.json", {"rolls": [
                {"phase": "P1", "table": "tokens", "label": "s", "attempt": 1, "tokens": ["claim:nobility=none"]}]})
            ctx = dd.context(c.name, "P2")
            self.assertEqual(ctx.tokens["claim:rule=hereditary"], False)
            self.assertEqual(ctx.tokens["claim:nobility=none"], True, "a secret record's token keeps the secret flag")
            self.assertIn("claim:below_ground=lived_in", ctx.tokens, "a rolled row's claims are expanded")
            self.assertNotIn("claim:rule=hereditary", dd.context(c.name, "P1").tokens, "a phase stands on the phases before it")
        finally:
            c.remove()


class Conditions(unittest.TestCase):

    def test_all_and_any_nest(self):
        ctx = arb.Context(rolled={"land_forest": False, "life_bee_forests": False})
        both = {"all": [{"any_of": ["land_forest", "land_marsh"]}, {"any_of": ["life_bee_forests", "life_timber_forest"]}]}
        self.assertTrue(arb.holds(both, ctx))
        self.assertFalse(arb.holds(both, arb.Context(rolled={"land_forest": False})))
        self.assertTrue(arb.holds({"any": [{"all_of": ["x"]}, {"any_of": ["land_forest"]}]}, ctx))
        self.assertFalse(arb.holds({"any": [{"all_of": ["x"]}, {"any_of": ["y"]}]}, ctx))
        self.assertEqual(arb._condition_ids(both), {"land_forest", "land_marsh", "life_bee_forests", "life_timber_forest"})
        # the existing forms stay valid
        self.assertTrue(arb.holds([{"any_of": ["x"]}, {"any_of": ["land_forest"]}], ctx))
        with self.assertRaises(ValueError):
            arb.holds({"every": []}, ctx)


class Roles(unittest.TestCase):
    """A role's claim counts only when the scale seats that role."""

    def run_contest(self, scale, roles_claims):
        rows = fd.rows_by_id("contest")
        real = fd.rows_by_id
        cid = "contest_two_heirs"
        patched = dict(rows[cid], roles={k: dict(v, **({"claims": roles_claims[k]} if k in roles_claims else {}))
                                         for k, v in rows[cid]["roles"].items()})

        def fake(sub):
            got = real(sub)
            return dict(got, **{cid: patched}) if sub == "contest" else got
        fd.rows_by_id = fake
        try:
            for i in range(400):
                d = {"scale": scale, "magic": "medium", "era": "medieval", "tone": "shadowed", "content_mix": ["war", "mystery", "horror"],
                     "level_band": [1, 12]}
                R = designer.Roller.in_memory(f"ROLE-{scale}-{i}", d)
                out = fd.roll(R, d)
                if out["contests"][0]["id"] == cid:
                    return R
        finally:
            fd.rows_by_id = real
        self.fail("no seed drew the contest")

    def test_a_seated_roles_claim_becomes_a_token_and_an_unseated_one_is_silent(self):
        claims = {"a": {"rule": "hereditary"}, "fourth": {"nobility": "none"}}
        short = self.run_contest("short", claims)
        self.assertIn("claim:rule=hereditary", short.ctx.tokens)
        self.assertNotIn("claim:nobility=none", short.ctx.tokens, "short seats three roles: the fourth's claim is silent")
        self.assertEqual(short.by_label["foundation.contest.1.claims"]["tokens"], ["claim:rule=hereditary"])
        standard = self.run_contest("standard", claims)
        self.assertEqual(standard.by_label["foundation.contest.1.claims"]["tokens"], ["claim:nobility=none", "claim:rule=hereditary"])

    def test_a_contest_whose_seated_role_clashes_with_the_context_is_not_drawn(self):
        ctx = arb.Context()
        ctx.add_token("claim:rule=by_lot", False)
        self.assertEqual(ctx.clashes({"rule": "hereditary"}), ["claim:rule=by_lot"])
        self.assertEqual(ctx.clashes({"rule": "throne"}), [])


class LayoutTokens(unittest.TestCase):

    def test_the_two_tokens_appear_only_in_their_cases(self):
        seen = {"below": 0, "remnant": 0}
        combos = list(itertools.product(("short", "standard", "epic"), ("low", "medium", "high"), ("medieval", "underground", "nautical")))
        for i in range(1500):
            scale, magic, era = combos[i % len(combos)]
            d = {"scale": scale, "magic": magic, "era": era, "tone": "bright", "content_mix": ["war", "mystery", "horror"],
                 "level_band": [1, 1 + _floor.SPAN[scale]]}
            R = designer.Roller.in_memory(f"LAY-{i}", d)
            out = fd.roll(R, d)
            rec = R.by_label.get("foundation.layout.tokens") or {}
            toks = set(rec.get("tokens") or [])
            heart_below = out["layout"]["parts"]["heart"] == "land_underground"
            self.assertEqual("claim:below_ground=lived_in" in toks, heart_below, R.master)
            self.assertEqual("layout:remnant_on_heart" in toks, out["layout"]["remnant"] == "heart", R.master)
            seen["below"] += heart_below
            seen["remnant"] += out["layout"]["remnant"] == "heart"
            self.assertEqual(arb.conflicting_pairs([r["row_id"] for r in R.public if r.get("row_id")], tokens=R.ctx.tokens), [],
                             "the final set holds on claims too")
        self.assertGreater(seen["below"], 0)
        self.assertGreater(seen["remnant"], 0)


class Overrides(unittest.TestCase):

    def rows_overriding(self):
        out: dict = {}
        for ref, r in every_row():
            ov = r.get("overrides")
            if isinstance(ov, list):
                for o in ov:
                    out.setdefault(o["default"], []).append((ref, r))
        return out

    def together(self, a, b) -> bool:
        """Can the two rows be rolled in one birth?"""
        (ra, a_row), (rb, b_row) = a, b
        idx = dt.conflict_index()
        if b_row["id"] in idx.get(a_row["id"], ()):
            return False
        toks_a, toks_b = dt.claim_tokens(a_row.get("claims")), dt.claim_tokens(b_row.get("claims"))
        cm = dt.clash_map()
        clash = (any(tb in cm.get(ta, ()) for ta in toks_a for tb in toks_b)
                 or any(t in idx.get(b_row["id"], ()) for t in toks_a)
                 or any(t in idx.get(a_row["id"], ()) for t in toks_b))
        if clash:
            return False
        if ra != rb:
            return True
        head = dt.roll_header(ra)
        counts = list((head.get("count_by_scale") or {}).values())
        counts += [v for by in (head.get("count_by_spine") or {}).values() for v in by.values()]     # the palette (18b)
        many = max((dt.band(v)[1] for v in counts), default=1) > 1
        if not many:
            return False
        return not (head.get("families_distinct") and a_row.get("family") == b_row.get("family"))

    def test_every_override_names_a_registered_default(self):
        for default, users in self.rows_overriding().items():
            self.assertIn(default, REG["defaults"], [r["id"] for _, r in users])
            for _, r in users:
                for o in r["overrides"]:
                    self.assertTrue("to" in o, r["id"])

    def test_two_overrides_of_one_default_carry_a_combine_line(self):
        written = {(c["default"], frozenset(c["rows"])) for c in REG.get("combines") or [] if c.get("combine")}
        for default, users in self.rows_overriding().items():
            for a, b in itertools.combinations(users, 2):
                if self.together(a, b):
                    self.assertIn((default, frozenset({a[1]["id"], b[1]["id"]})), written,
                                  f"{a[1]['id']} and {b[1]['id']} both override {default} and can be rolled together")

    def test_the_combine_lines_name_real_rows_and_defaults(self):
        ids = {r["id"] for _, r in every_row()}
        for c in REG.get("combines") or []:
            self.assertIn(c["default"], REG["defaults"])
            self.assertFalse(set(c["rows"]) - ids)


class Inspection(unittest.TestCase):

    def test_every_p0_and_p1_row_is_stamped(self):
        """`design_tables.py stamp` writes reviewed.json after the development tab's audit; a row with no stamp, or
        changed since its stamp, fails here."""
        state = dt.unreviewed()
        self.assertEqual(state, {"missing": [], "changed": [], "gone": []},
                         "run `py .claude/skills/dnd/scripts/design_tables.py stamp` after the audit")

    def test_a_changed_row_loses_its_stamp(self):
        row = {"id": "x", "label": "X", "tr": {"name": "bir"}}
        self.assertNotEqual(dt.row_hash(row), dt.row_hash(dict(row, label="Y")))
        self.assertEqual(dt.row_hash(row), dt.row_hash({"tr": {"name": "bir"}, "label": "X", "id": "x"}), "key order does not matter")

    def test_no_unique_table_falls_under_the_floor(self):
        pools = _floor.smallest_pools(900)
        self.assertIn("foundation.yaml#spine", pools)
        self.assertFalse(_floor.unique("trope-breaks.yaml#tie") or _floor.unique("foundation.yaml#time")
                         or _floor.unique("foundation.yaml#palette"), "the repeatable tables are exempt")
        self.assertEqual(_floor.under_the_floor(pools), {}, "a table whose rows are not drawn again keeps five rows")

    def test_the_floor_helper_reports_a_small_pool(self):
        self.assertEqual(_floor.under_the_floor({"foundation.yaml#spine": 4, "foundation.yaml#time": 2, "foundation.yaml#ruin_source": 9}),
                         {"foundation.yaml#spine": 4})


if __name__ == "__main__":
    unittest.main()
