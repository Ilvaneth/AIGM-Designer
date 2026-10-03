"""
test_identity_roll.py — build item 10a (docs/p1-build-10.md): P1's second step by script, the public identity. Over
thousands of seeds on every scale, magic, era and tone: no conflicting set, no empty pool, the people's role and its
lineage agree, the institution sits under its role's archetype, the user follows the rule's kind, every question is
of its contest's family, the trope breaks' ties follow their rules, and the public log names no secret row.
"""

import itertools
import json
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS
import _floor

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_identity as di  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

S = "signatures.yaml#"
SEEDS = 2700
CONTEST = fd.rows_by_id("contest")
BREAKS = {r["id"]: r for r in dt.rows("trope-breaks.yaml")}
PRACTICE = {r["id"]: r for r in dt.rows(S + "institution_practice")}
FORM = {r["id"]: r for r in dt.rows(S + "institution_form")}
POWER = {r["id"]: r for r in dt.rows(S + "institution_power")}
RULE = {r["id"]: r for r in dt.rows(S + "phenomenon_rule")}
TRAIT = {r["id"]: r for r in dt.rows(S + "people_trait")}
QUESTION = {r["id"]: r for r in dt.rows("tensions.yaml")}
RUIN = fd.rows_by_id("ruin_source")
FLOOR = 5
# the draws of tables whose rows are not drawn again across campaigns, and the group each draw's floor is reported by
UNIQUE_DRAWS = ("break.1", "break.2", "people.trait.visible", "people.trait.behaving", "institution.practice",
                "phenomenon.rule", "tension.1", "tension.2")


def run(i, combos, mixes, tag="IDENT"):
    scale, magic, era, tone = combos[i % len(combos)]
    dials = {"scale": scale, "magic": magic, "era": era, "tone": tone, "content_mix": list(mixes[i % len(mixes)]),
             "party_size": 2, "level_band": [1, 1 + _floor.SPAN[scale]]}
    R = designer.Roller.in_memory(f"{tag}-{i}", dials)
    designer.preroll_p1(R, {"dials": dials})
    return dials, R


class ManySeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        combos = _floor.dial_sets()
        mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
        cls.runs, cls.empty = [], []
        for i in range(SEEDS):
            try:
                cls.runs.append(run(i, combos, mixes))
            except SystemExit as exc:
                cls.empty.append(str(exc))

    def test_no_pool_is_empty(self):
        self.assertEqual(self.empty, [])
        self.assertEqual(len(self.runs), SEEDS)

    def test_no_conflicting_set(self):
        for d, R in self.runs:
            rows = [r["row_id"] for r in R.public if r.get("row_id")]
            self.assertEqual(arb.conflicting_pairs(rows, tokens=[t for t, s in R.ctx.tokens.items() if not s], exempt=R.exempt), [], R.master)
            self.assertLessEqual(R.exempt, {frozenset(("tie_break", "time_coming"))}, "the one exception")

    def test_the_identity_is_recorded(self):
        for d, R in self.runs:
            idn = R.identity
            self.assertTrue(idn["stamped"])
            self.assertEqual(set(idn), {"stamped", "trope_breaks", "role_hints", "people", "institution", "phenomenon", "questions", "overrides"})
            self.assertEqual(idn["people"]["lineage"], R.row("people.lineage"))
            self.assertEqual(idn["institution"]["practice"], R.row("institution.practice"))
            self.assertEqual(idn["phenomenon"]["rule"], R.row("phenomenon.rule"))
            for label in ("tension.second", "sig_phenomenon", "sig_people", "sig_institution"):
                self.assertNotIn(label, R.by_label)

    # ── the trope breaks ──

    def test_the_break_count_and_families(self):
        for d, R in self.runs:
            ids = [b["id"] for b in R.identity["trope_breaks"]]
            self.assertEqual(len(ids), {"short": 1, "standard": 2, "epic": 2}[d["scale"]])
            self.assertEqual(len({BREAKS[b]["family"] for b in ids}), len(ids), R.master)

    def test_the_new_prohibition_scar(self):
        seen = coming = 0
        for d, R in self.runs:
            scars, time = R.foundation["break"]["scars"], R.foundation["break"]["time"]
            first = R.identity["trope_breaks"][0]
            if "scar_new_taboo" in scars:
                seen += 1
                self.assertTrue(BREAKS[first["id"]].get("prohibition"), R.master)
                self.assertEqual((first["tie"], first["tie_by"]), ("tie_break", "scar"), R.master)
                self.assertEqual(R.by_label["break_tie.1"]["notation"], "forced")
                if time == "time_coming":
                    coming += 1
                    self.assertEqual(R.by_label["break_tie.1"]["conflict_exempt"], ["time_coming"])
            for n, b in enumerate(R.identity["trope_breaks"]):
                if b["tie"] == "tie_break" and time == "time_coming":
                    self.assertTrue(n == 0 and b["tie_by"] == "scar", f"{R.master}: the break's tie under a break still coming")
        self.assertGreater(seen, 50)
        self.assertGreater(coming, 5, "the exception was exercised")

    def test_a_fit_sets_the_tie(self):
        by = Counter()
        for d, R in self.runs:
            f = R.foundation
            pieces = {"lifeline": [f["lifeline"]["id"]], "contest": [c["id"] for c in f["contests"]], "ruin_source": [f["ruin_source"]]}
            for n, b in enumerate(R.identity["trope_breaks"], 1):
                by[b["tie_by"]] += 1
                rec = R.by_label[f"break_tie.{n}"]
                self.assertEqual(rec["row_id"], b["tie"])
                if b["tie_by"] == "scar":
                    continue
                fits = []                                     # (weight, piece order, tie) for every fit that holds
                for rule in BREAKS[b["id"]].get("weight_by") or []:
                    ids = set(di.named(rule["when"]))
                    for order, (piece, tie) in enumerate(di.TIE_OF_PIECE):
                        if float(rule["x"]) > 1 and ids & set(pieces[piece]):
                            fits.append((-float(rule["x"]), order, tie))
                if fits:
                    self.assertEqual((b["tie_by"], b["tie"]), ("fit", min(fits)[2]), R.master)
                    self.assertEqual(rec["notation"], "forced")
                else:
                    self.assertEqual(b["tie_by"], "rolled", R.master)
                    self.assertNotEqual(rec["notation"], "forced")
        self.assertGreater(by["fit"], 100)
        self.assertGreater(by["rolled"], 1000)

    def test_the_merges(self):
        seen = Counter()
        for d, R in self.runs:
            rolled = {r["row_id"] for r in R.public if r.get("row_id")}
            for b in R.identity["trope_breaks"]:
                want = {o for o in (BREAKS[b["id"]].get("merges_with") or {}) if o in rolled}
                self.assertEqual({m["with"] for m in b["merges"]}, want, R.master)
                for m in b["merges"]:
                    seen[(b["id"], m["with"])] += 1
            hints = R.identity["role_hints"]
            for c in R.foundation["contests"]:
                base = {k: CONTEST[c["id"]]["roles"][k].get("hint") for k in c["roles"]}
                if c["id"] == "contest_humans_dragon" and any(b["id"] == "break_dragons_rule" for b in R.identity["trope_breaks"]):
                    base.update(a="resistance", b="state")
                self.assertEqual(hints[c["id"]], base, R.master)

    def test_the_two_merges_that_change_or_keep_the_hints(self):
        """Forced by hand: the many seeds rarely roll the pair."""
        self.assertEqual(BREAKS["break_dragons_rule"]["merge_role_hints"], {"contest_humans_dragon": {"a": "resistance", "b": "state"}})
        self.assertNotIn("merge_role_hints", BREAKS["break_the_enemy_won"])
        self.assertIn("role a", BREAKS["break_the_enemy_won"]["merges_with"]["contest_occupier_resistance"])

    # ── the people ──

    def test_the_peoples_role_and_its_lineage_agree(self):
        seen = Counter()
        for d, R in self.runs:
            f, p = R.foundation, R.identity["people"]
            main = f["contests"][0]
            row = CONTEST[main["id"]]
            destroyed = di.destroyed_role(f)
            marked = [k for k in main["roles"] if row["roles"][k].get("people_role") and k != destroyed]
            self.assertLessEqual(len(marked), 1)
            self.assertEqual(p["role"], marked[0] if marked else None, R.master)
            if p["role"]:
                seen["role"] += 1
                role = row["roles"][p["role"]]
                if role.get("lineage_forced"):
                    seen["forced"] += 1
                    self.assertEqual((p["lineage"], p["lineage_by"]), (role["lineage_forced"], "role"), R.master)
                else:
                    self.assertEqual(p["lineage_by"], "rolled")
            self.assertEqual(p["home"], "scar_new_people" if "scar_new_people" in f["break"]["scars"] else "lifeline")
        self.assertGreater(seen["role"], 100)
        self.assertGreater(seen["forced"], 30)

    def test_the_traits(self):
        won = 0
        for d, R in self.runs:
            p = R.identity["people"]
            self.assertEqual((TRAIT[p["traits"]["visible"]]["kind"], TRAIT[p["traits"]["behaving"]]["kind"]), ("visible", "behaving"))
            if p["traits"]["behaving"] == "trait_won_by_the_break":
                won += 1
                self.assertTrue(p["role"] is None or p["role"] == R.foundation["break"]["winner"], R.master)
        self.assertGreater(won, 0)

    def test_the_lineage_weights(self):
        lin = {r["id"]: r for r in dt.rows(S + "people_lineage")}
        forest = arb.Context(rolled={"land_forest": False})
        self.assertEqual(di.inverted_weight(lin["lineage_elf"], forest), 1, "at home: no weight under inverted homes")
        self.assertEqual(di.inverted_weight(lin["lineage_elf"], arb.Context()), 3, "away from home: the weight")
        self.assertEqual(di.inverted_weight(lin["lineage_human"], arb.Context()), 4, "the base weight stands")
        dragon = arb.Context(rolled={"break_dragons_rule": False})
        self.assertEqual(di.inverted_weight(lin["lineage_dragonborn"], dragon), 3, "a weight on other rows is not inverted")
        self.assertEqual(di.inverted_weight(lin["lineage_dragonborn"], arb.Context()), 1)
        deep = Counter()                                       # a role's lineage_weight is read
        for d, R in self.runs:
            role = R.identity["people"]["role"]
            if role and CONTEST[R.foundation["contests"][0]["id"]]["roles"][role].get("lineage_weight"):
                deep[R.identity["people"]["lineage"]] += 1
        if sum(deep.values()) >= 20:
            self.assertGreater(sum(deep[k] for k in ("lineage_dwarf", "lineage_gnome", "lineage_goblinoid")), sum(deep.values()) * 0.4)

    # ── the institution ──

    def test_the_institution_sits_under_its_roles_archetype(self):
        """Every birth has a home role for the institution; its practice, form and power sit under that role's
        archetype in every seed, the form a practice names included. No exemption."""
        named_form = 0
        for d, R in self.runs:
            f, ins, p = R.foundation, R.identity["institution"], R.identity["people"]
            main = f["contests"][0]
            hints = R.identity["role_hints"][main["id"]]
            homes = [k for k in main["roles"] if hints.get(k) and k != p["role"] and k != di.destroyed_role(f)]
            self.assertIsNotNone(ins["role"], R.master)
            self.assertIn(ins["role"], homes, R.master)
            self.assertEqual(ins["archetype"], hints[ins["role"]], R.master)
            self.assertIn(ins["archetype"], di.HEADINGS)
            self.assertIn(ins["archetype"], PRACTICE[ins["practice"]]["hints"], R.master)
            self.assertIn(ins["archetype"], FORM[ins["form"]]["hints"], R.master)
            self.assertIn(ins["archetype"], POWER[ins["power"]]["hints"], R.master)
            self.assertNotIn("institution.archetype", R.by_label, "nothing is made up for a homeless institution")
            own = PRACTICE[ins["practice"]].get("form")
            named_form += bool(own)
            self.assertEqual((ins["form"], ins["form_by"]), (own, "practice") if own else (ins["form"], "rolled"), R.master)
        self.assertGreater(named_form, 30)
        type(self).report = {"named_form": named_form}

    def test_the_break_never_destroys_the_institutions_last_home(self):
        """design_foundation: an action that destroys a role never strikes the last seated role of the main contest
        that carries an archetype hint and is no people's role; the protected role is on the action's record."""
        protected = struck_last = 0
        for d, R in self.runs:
            f = R.foundation
            main = f["contests"][0]
            homes = fd.institution_homes(CONTEST[main["id"]], main["roles"])
            self.assertTrue(homes, R.master)
            rec = R.by_label["foundation.break.action"]
            last = f["break"].get("target_role") if homes == [f["break"].get("target_role")] else None
            self.assertEqual((rec.get("protected_role") or {}).get("role"), last, R.master)
            if last:
                struck_last += 1
                self.assertIsNone(di.destroyed_role(f), R.master)
                protected += any("never destroys role" in e["why"] for e in rec["excluded"])
        self.assertGreater(struck_last, 0, "the case was exercised")
        self.assertEqual(protected, struck_last, "the excluded actions carry the reason")
        type(self).protection = {"last_home_struck": struck_last}

    # ── the phenomenon ──

    def test_the_rule_and_its_user(self):
        kinds = Counter()
        for d, R in self.runs:
            f, ph = R.foundation, R.identity["phenomenon"]
            rule = RULE[ph["rule"]]
            if "scar_magic_rule_changed" in f["break"]["scars"]:
                self.assertEqual((ph["home"], rule["family"]), ("break", "born_of_break"), R.master)
            else:
                self.assertEqual(ph["home"], "ruin_source")
                self.assertIn(rule["family"], RUIN[f["ruin_source"]]["olgu_families"], R.master)
            kinds[rule["kind"]] += 1
            self.assertEqual(ph["kind"], rule["kind"])
            rec = R.by_label["phenomenon.user"]
            if rule["kind"] == "spell":
                self.assertEqual((ph["user"], rec["notation"]), ("user_casters", "forced"), R.master)
            elif rule["kind"] == "self":
                self.assertEqual((ph["user"], rec["notation"]), ("user_no_one", "forced"), R.master)
            else:
                self.assertNotEqual(rec["notation"], "forced")
                self.assertNotEqual(ph["user"], "user_no_one", R.master)
                if rule.get("users"):
                    self.assertIn(ph["user"], rule["users"], R.master)
            if d["era"] == "underground":
                self.assertNotIn(ph["rule"], ("rule_night_distances", "rule_seasons_bound_to_a_beast", "rule_feelings_make_weather"))
        self.assertEqual(set(kinds), {"spell", "self", "usable"})

    # ── the question ──

    def test_every_question_is_of_its_contests_family(self):
        for d, R in self.runs:
            qs = R.identity["questions"]
            self.assertEqual([q["contest"] for q in qs], [c["id"] for c in R.foundation["contests"]])
            self.assertEqual(len(qs), {"short": 1, "standard": 1, "epic": 2}[d["scale"]])
            self.assertEqual(len({q["id"] for q in qs}), len(qs))
            for q in qs:
                self.assertEqual(q["family"], CONTEST[q["contest"]]["family"])
                self.assertIn(q["family"], QUESTION[q["id"]]["families"], R.master)
        self.assertNotIn("family_weight", dt.load("tensions.yaml")["roll"])

    # ── the overrides, the secret layer, the floor ──

    def test_the_overrides_are_collected_as_data(self):
        seen = 0
        index = {r["id"]: r for name in dt.list_tables() for lst in dt.all_row_lists(dt.load(name)).values() for r in lst}
        for d, R in self.runs:
            want = [(rid, o["default"]) for rid in (r["row_id"] for r in R.public if r.get("row_id"))
                    for o in (index.get(rid, {}).get("overrides") if isinstance(index.get(rid, {}).get("overrides"), list) else [])]
            got = [(o["row"], o["default"]) for o in R.identity["overrides"]]
            self.assertEqual(sorted(got), sorted(want), R.master)
            seen += bool(got)
        self.assertGreater(seen, 500)

    def test_the_public_log_names_no_secret_row(self):
        secret = dt.secret_row_ids()
        leaks = 0
        for d, R in self.runs:
            text = json.dumps(R.public, ensure_ascii=False) + json.dumps(R.identity, ensure_ascii=False)
            leaks += sum(1 for rid in secret if f'"{rid}"' in text)
        self.assertEqual(leaks, 0, f"{leaks} secret row id(s) in a public record or the identity")

    def floors(self):
        """The smallest pool after the constraints, per group of each table whose rows are not drawn again."""
        out: dict = {}

        def low(key, n):
            out[key] = min(out.get(key, n), n)
        for d, R in self.runs:
            f, idn = R.foundation, R.identity
            taboo = "scar_new_taboo" in f["break"]["scars"]
            low("break.1 (prohibition rows, the scar's draw)" if taboo else "break.1", R.pool_of["break.1"])
            if "break.2" in R.pool_of:
                low("break.2", R.pool_of["break.2"])
            low("trait, visible", R.pool_of["people.trait.visible"])
            low("trait, behaving", R.pool_of["people.trait.behaving"])
            low(f"practice under {idn['institution']['archetype']}", R.pool_of["institution.practice"])
            low(f"rule from {'the break' if idn['phenomenon']['home'] == 'break' else f['ruin_source']}", R.pool_of["phenomenon.rule"])
            for n, q in enumerate(idn["questions"], 1):
                low(f"question of {q['family']}" + (" (second)" if n == 2 else ""), R.pool_of[f"tension.{n}"])
        return out

    def test_the_floor(self):
        """A table whose rows are not drawn again keeps five rows in every group after the constraints. The report is
        printed by `py tests/test_identity_roll.py --floor`; a group under five fails here and is never waved through."""
        floors = self.floors()
        under = {k: v for k, v in floors.items() if v < FLOOR}
        self.assertEqual(under, {}, "a non-repeating table falls under five: stop and report the number")
        self.assertEqual(len([k for k in floors if k.startswith("practice under ")]), 8)
        self.assertEqual(len([k for k in floors if k.startswith("question of ") and not k.endswith("(second)")]), 8)


if __name__ == "__main__":
    if "--floor" in sys.argv:
        ManySeeds.setUpClass()
        t = ManySeeds("floors")
        fl = t.floors()
        rules = [v for k, v in fl.items() if k.startswith("rule from ")]
        for k, v in sorted(fl.items()):
            if not k.startswith("rule from "):
                print(f"{v:>3}  {k}")
        print(f"{min(rules):>3}  rule, the smallest over {len(rules)} ruin sources and the break")
        print("empty pools:", len(ManySeeds.empty), "seeds:", len(ManySeeds.runs))
        for name in ("test_the_institution_sits_under_its_roles_archetype", "test_the_break_never_destroys_the_institutions_last_home"):
            getattr(ManySeeds(name), name)()
        print(ManySeeds.report, ManySeeds.protection)
    else:
        unittest.main()
