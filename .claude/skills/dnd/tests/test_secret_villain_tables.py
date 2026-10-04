"""
test_secret_villain_tables.py — build item 9 (docs/p1-build-9.md): the secret (archetype, chooser, twist, trail) and
the villain (visibility, shape, origin, tie to the break).

The owner is also the player. No assertion here prints a row of these tables: a failure names a sub-table and a
position or a hash, never an id, a label or a sentence.
"""

import hashlib
import itertools
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

SECRET = ("secrets.yaml#archetype", "secrets.yaml#chooser", "secrets.yaml#twist", "secrets.yaml#trail")
VILLAIN = ("antagonists.yaml#visibility", "antagonists.yaml#villain_shape", "antagonists.yaml#origin", "antagonists.yaml#break_tie")
P4_OWN = ("front_template", "doom_shape", "lieutenant_role", "buy_time_lever", "escalation_stage", "bbeg_faction_archetype")
REPO = SCRIPTS.parents[3]
BURN = REPO / "docs" / "reports" / "item9-burn-sample.md"

# the row families that do not come back (owner, 2026-10-04, docs/p1-build-16.md ruling 4): ledgers, registers, debts
# and tolls; courts and trials; light as a fuel; hush and bells; tides; salt. The dead and the undead are general
# material since ruling 1 and left the list with build item 16c.
ATTRACTOR = ("ledger", "register", "registry", "census",
             "reckoning", "debt", "debtor", "toll", "tithe", "court", "trial", "tribunal", "judge", "verdict", "candle", "lamp",
             "lantern", "wick", "oil", "hush", "silence", "silent", "bell", "tide", "tidal", "salt", "wax")
ATTRACTOR_RE = re.compile(r"\b(" + "|".join(ATTRACTOR) + r")s?\b", re.IGNORECASE)
REFERENCE_KEYS = {"id", "value", "conflicts_with", "allowed_via", "requires", "weight_by", "hides_in", "forbidden"}
# rows this item removed or renamed, as hashes (sha256 of the id, 16 hex): the committed data names none of them
GONE = {"a80b63c9288875b8", "fef90a0460d75182", "e565cd256470dab7", "72225e83c819fb47", "ecbccb4d7f21e182", "7f1a8ee1902c7838", "7b1dabb0e6a2104c", "c5a97ecbf1cd4434"}


def h(text: str) -> str:
    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()[:16]


def rows(ref):
    return dt.rows(ref)


def usable(ref):
    return [r for r in rows(ref) if not r.get("forbidden")]


def where(ref, i):
    return f"{ref} row {i + 1}"


def strings(node, skip=REFERENCE_KEYS):
    """Every prose string of a row: labels, sentences, clue shapes, rules, hooks; never an id or a reference list."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for x in node:
            yield from strings(x, skip)
    elif isinstance(node, dict):
        for k, v in node.items():
            if k not in skip:
                yield from strings(v, skip)


def named(cond):
    if isinstance(cond, list):
        for c in cond:
            yield from named(c)
    elif isinstance(cond, dict):
        for key in ("any_of", "all_of", "none_of"):
            yield from cond.get(key) or []
        for key in ("all", "any"):
            yield from named(cond.get(key) or [])


def references(r):
    refs = set(r.get("conflicts_with") or []) | set(r.get("allowed_via") or []) | set(named(r.get("requires")))
    for w in r.get("weight_by") or []:
        refs |= set(named(w.get("when")))
    return refs


ALL_IDS = {r["id"] for name in dt.list_tables() for lst in dt.all_row_lists(dt.load(name)).values() for r in lst}
TABLE_OF = {r["id"]: ref for ref in SECRET + VILLAIN for r in rows(ref)}


def pairs_between(left, right):
    """Conflict pairs, after the symmetric load, between the rows of `left` refs and the ids `right` accepts."""
    idx = dt.conflict_index()
    out = set()
    for ref in left:
        for r in rows(ref):
            for other in idx.get(r["id"], ()):
                if right(other):
                    out.add(frozenset((r["id"], other)))
    return out


def is_public(other):
    return other not in TABLE_OF


class Counts(unittest.TestCase):

    def test_the_counts(self):
        self.assertGreaterEqual(len(rows("secrets.yaml#archetype")), 22)
        self.assertEqual(len(rows("secrets.yaml#twist")), 15)
        self.assertIn(len(rows("secrets.yaml#trail")), (9, 10, 11))
        self.assertEqual(len(rows("secrets.yaml#chooser")), 6)
        self.assertEqual(len(rows("antagonists.yaml#break_tie")), 6)
        self.assertEqual(len(rows("antagonists.yaml#visibility")), 5)
        self.assertGreaterEqual(len(usable("antagonists.yaml#villain_shape")), 14)
        self.assertEqual(len(rows("antagonists.yaml#villain_shape")), len(usable("antagonists.yaml#villain_shape")), "no shape is barred (16a)")
        self.assertGreaterEqual(len(usable("antagonists.yaml#origin")), 10)
        self.assertEqual(len(rows("antagonists.yaml#origin")), len(usable("antagonists.yaml#origin")), "no origin is barred (16a)")

    def test_every_roll_is_secret(self):
        for ref in SECRET + VILLAIN:
            self.assertTrue(dt.roll_header(ref).get("secret"), ref)
        secret_ids = dt.secret_row_ids()
        self.assertTrue(all(rid in secret_ids for rid in TABLE_OF))

    def test_the_archetype_tells_the_breaks_cause(self):
        for i, r in enumerate(rows("secrets.yaml#archetype")):
            at = where("archetype", i)
            self.assertIn("{the chooser}", r.get("cause") or "", f"{at}: the cause line names who chose")
            self.assertEqual(set(r["clue_shape"]), {"act1", "act2", "act3"}, at)
            self.assertTrue(r.get("hides_in") and r.get("statement") and r.get("hooks"), at)
            self.assertNotIn("villain_relation", r, f"{at}: the villain's tie to the break replaced it")
        common = " ".join(hk["must"] for hk in dt.load("secrets.yaml")["hooks_common"])
        self.assertIn("the break's dated event", common)
        self.assertNotIn("deep-past", common)
        self.assertNotIn("relation to the secret", common)

    def test_the_trail_keeps_its_three_stages(self):
        for i, r in enumerate(rows("secrets.yaml#trail")):
            self.assertEqual(list(r["acts"]), ["act1", "act2", "act3"], where("trail", i))
            needs_writing = any(w in v for v in r["acts"].values() for w in ("letter", "document"))
            self.assertEqual("break_no_writing" in (r.get("conflicts_with") or []), needs_writing, where("trail", i))

    def test_the_twists_and_the_rest_carry_a_rule_and_a_hook(self):
        for ref in ("secrets.yaml#twist", "secrets.yaml#chooser", "antagonists.yaml#visibility", "antagonists.yaml#break_tie"):
            for i, r in enumerate(rows(ref)):
                self.assertTrue(r.get("rule") and r.get("hooks"), where(ref, i))
        for i, r in enumerate(usable("antagonists.yaml#villain_shape")):
            self.assertTrue(r.get("rule") and r.get("value") and r.get("hooks"), where("villain_shape", i))
        values = [r["value"] for ref in ("antagonists.yaml#villain_shape", "antagonists.yaml#origin") for r in rows(ref)]
        self.assertEqual(len(values), len(set(values)))


class Forbidden(unittest.TestCase):

    def test_every_row_can_be_drawn(self):
        """Build item 16a: no shape, origin or villain faction archetype is barred; on an empty context every row of
        the three tables is in the pool."""
        for ref in ("antagonists.yaml#villain_shape", "antagonists.yaml#origin", "antagonists.yaml#bbeg_faction_archetype"):
            self.assertFalse(any(r.get("forbidden") or r.get("allowed_via") for r in rows(ref)), ref)
            pool = arb.arbitrate(ref, rows(ref), arb.Context(), secret=True)["pool"]
            self.assertEqual(len(pool), len(rows(ref)), ref)


class Attractor(unittest.TestCase):

    def test_no_row_holds_an_attractor_word(self):
        hits = 0
        for ref in SECRET + VILLAIN:
            for r in rows(ref):
                if r.get("forbidden"):
                    continue
                hits += sum(1 for s in strings(r) if ATTRACTOR_RE.search(s.replace("_", " ")))
        self.assertEqual(hits, 0, f"{hits} string(s) of the secret and villain rows hold an attractor word")


class References(unittest.TestCase):

    def test_every_named_id_exists(self):
        for ref in SECRET + VILLAIN + ("antagonists.yaml#bbeg_faction_archetype",):
            for i, r in enumerate(rows(ref)):
                unknown = {x for x in references(r) if not x.startswith(dt.CLAIM)} - ALL_IDS
                self.assertFalse(bool(unknown), f"{where(ref, i)} names {len(unknown)} id(s) that do not exist")

    def test_every_conflict_is_symmetric_after_load(self):
        idx = dt.conflict_index()
        for rid in TABLE_OF:
            for other in idx.get(rid, ()):
                self.assertIn(rid, idx.get(other, ()), "a conflict of the secret or villain tables is one-sided")

    def test_the_removed_rows_are_named_nowhere(self):
        token = re.compile(r"\b[a-z]+(?:_[a-z0-9]+)+\b")
        for path in sorted(dt.tables_dir().iterdir()):
            if path.suffix not in (".yaml", ".json", ".md"):
                continue
            found = {h(t) for t in token.findall(path.read_text(encoding="utf-8"))} & GONE
            self.assertFalse(bool(found), f"{path.name} still names {len(found)} removed row(s)")

    def test_the_public_rows_were_checked(self):
        """The public rows the specification lists exist, and the secret is barred from standing beside the ones
        that already show it (the count is the summary's; the audit reads the pairs)."""
        listed = ("spine_titan_back", "spine_two_worlds", "ruin_imprisoned_god", "ruin_dead_god", "ruin_departed_god",
                  "ruin_made_peoples", "ruin_failed_experiment", "ruin_broken_time", "ruin_planar_rift", "act_true_face",
                  "break_gods_are_ancestors_known", "break_gods_among_mortals", "break_the_enemy_won", "break_dragons_rule",
                  "break_rule_by_lottery", "break_no_direct_lies", "break_no_writing", "rule_true_names")
        self.assertFalse(set(listed) - ALL_IDS)
        secret_public = pairs_between(SECRET, is_public)
        self.assertGreaterEqual(len(secret_public), 31)
        barring = {o for p in pairs_between(SECRET + VILLAIN, is_public) for o in p} & set(listed)
        self.assertEqual(len(barring), 15,
                         "three listed rows bar nothing: each tells a different thing from what any archetype hides")


class OneVillain(unittest.TestCase):

    def test_the_tie_and_the_breaks_time(self):
        """A tie that needs the break to have happened cannot stand with a break still coming."""
        ties = {r["id"]: r for r in rows("antagonists.yaml#break_tie")}
        need = {"bond_wants_to_reverse", "bond_failed_to_stop", "bond_product_of_it"}
        self.assertEqual({k for k, r in ties.items() if "time_coming" in (r.get("conflicts_with") or [])}, need)
        coming = arb.Context(rolled={"time_coming": False, "chooser_bargainer": True})
        pool = {r["id"] for r in arb.arbitrate("antagonists.yaml#break_tie", rows("antagonists.yaml#break_tie"), coming, secret=True)["pool"]}
        self.assertEqual(pool, {"bond_exploits_it", "bond_wants_to_complete"})

    def test_the_chooser_is_the_villain_exactly_when_the_tie_is_caused_it(self):
        """Written as data here; the roll is build item 10's."""
        ref = "antagonists.yaml#break_tie"
        for chooser in (r["id"] for r in rows("secrets.yaml#chooser")):
            ctx = arb.Context(rolled={chooser: True, "time_just_now": False})
            pool = {r["id"] for r in arb.arbitrate(ref, rows(ref), ctx, secret=True)["pool"]}
            if chooser == "chooser_the_villain":
                self.assertEqual(pool, {"bond_caused_it"})
            else:
                self.assertEqual(len(pool), 5)
                self.assertNotIn("bond_caused_it", pool)
        for tie in (r["id"] for r in rows(ref)):                       # and the other way round
            ctx = arb.Context(rolled={tie: True})
            pool = {r["id"] for r in arb.arbitrate("secrets.yaml#chooser", rows("secrets.yaml#chooser"), ctx, secret=True)["pool"]}
            self.assertEqual("chooser_the_villain" in pool, tie == "bond_caused_it")

    def test_every_visibility_and_origin_leaves_shapes_to_draw(self):
        shapes = rows("antagonists.yaml#villain_shape")
        for i, vis in enumerate(rows("antagonists.yaml#visibility")):
            pool = arb.arbitrate("antagonists.yaml#villain_shape", shapes, arb.Context(rolled={vis["id"]: True}), secret=True)["pool"]
            self.assertGreaterEqual(len(pool), 5, where("visibility", i))
        self.assertIs(dt.own_roll_header("antagonists.yaml#visibility").get("avoid_used"), False, "the visibility may repeat")
        for i, shape in enumerate(usable("antagonists.yaml#villain_shape")):
            ctx = arb.Context(rolled={shape["id"]: True})
            pool = arb.arbitrate("antagonists.yaml#origin", rows("antagonists.yaml#origin"), ctx, secret=True)["pool"]
            self.assertGreaterEqual(len(pool), 5, where("villain_shape", i))

    def test_the_conflict_kinds_are_all_present(self):
        inside = pairs_between(VILLAIN, lambda o: TABLE_OF.get(o) in VILLAIN)
        self.assertTrue(inside and pairs_between(VILLAIN, is_public) and pairs_between(SECRET, is_public))
        self.assertEqual(len(pairs_between(("antagonists.yaml#break_tie",), lambda o: o == "time_coming")), 3)


class ManySeeds(unittest.TestCase):
    """Today's P1 and P4 preroll over every scale, magic and era: no conflicting set, no empty pool, the archetype's
    floor, and a public log that names no secret row."""

    SEEDS = 450

    @classmethod
    def setUpClass(cls):
        cls.secret_ids = dt.secret_row_ids()
        combos = list(itertools.product(dt.dial_values("scale"), dt.dial_values("magic"), dt.dial_values("era")))
        tones = dt.dial_values("tone")
        mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
        span = {"short": 4, "standard": 11, "epic": 19}
        cls.runs, cls.empty = [], 0
        for i in range(cls.SEEDS):
            scale, magic, era = combos[i % len(combos)]
            dials = {"scale": scale, "magic": magic, "era": era, "tone": tones[i % len(tones)],
                     "content_mix": list(mixes[i % len(mixes)]), "party_size": 2, "level_band": [1, 1 + span[scale]]}
            try:
                p1 = designer.Roller.in_memory(f"ITEM9-{i}", dials)
                designer.preroll_p1(p1, {"dials": dials})
                p4 = designer.Roller.in_memory(f"ITEM9-{i}", dials, phase="P4")
                p4.ctx = p1.ctx                                  # P4 stands on what P1 rolled, the secret rows too
                designer.preroll_p4(p4, {"dials": dials})
            except SystemExit:
                cls.empty += 1
                continue
            cls.runs.append((p1, p4))

    def test_no_pool_is_empty(self):
        self.assertEqual(self.empty, 0, f"{self.empty} seed(s) stopped on an empty pool")
        self.assertEqual(len(self.runs), self.SEEDS)

    def test_no_conflicting_set(self):
        bad = 0
        for p1, p4 in self.runs:
            rolled = [r["row_id"] for R in (p1, p4) for r in R.public + R.secret if r.get("row_id")]
            bad += bool(arb.conflicting_pairs(rolled, tokens=list(p4.ctx.tokens), exempt=p1.exempt))
        self.assertEqual(bad, 0, f"{bad} seed(s) rolled a conflicting set")

    def test_every_shape_origin_and_faction_archetype_is_drawn(self):
        """The freed rows come up like any other (build item 16a)."""
        for label, ref in (("bbeg_shape", "antagonists.yaml#villain_shape"), ("bbeg_origin", "antagonists.yaml#origin")):
            drawn = {p1.by_label[label]["row_id"] for p1, _ in self.runs}
            self.assertEqual(len(drawn), len(rows(ref)), f"{ref}: {len(rows(ref)) - len(drawn)} row(s) never drawn")
        drawn = {p4.by_label["bbeg_faction_archetype"]["row_id"] for _, p4 in self.runs}
        self.assertEqual(len(drawn), len(rows("antagonists.yaml#bbeg_faction_archetype")))

    def test_the_archetypes_floor(self):
        smallest = min(p1.pools["secrets.yaml#archetype"] for p1, _ in self.runs)
        self.assertGreaterEqual(smallest, 5, f"the archetype's smallest pool after the constraints is {smallest}")
        for ref in ("antagonists.yaml#villain_shape", "antagonists.yaml#origin"):
            self.assertGreaterEqual(min(p1.pools[ref] for p1, _ in self.runs if ref in p1.pools), 5, ref)      # a forced shape has no pool

    def test_the_public_log_names_no_secret_row(self):
        leaks = sizes = 0
        for p1, p4 in self.runs:
            for R in (p1, p4):
                text = json.dumps(R.public, ensure_ascii=False)
                leaks += sum(1 for rid in self.secret_ids if f'"{rid}"' in text)
                for note in R.secret_notes:                      # a secret row took rows out of a public pool
                    shown = R.by_label[note["label"]]
                    if shown in R.public and note.get("notation"):
                        sizes += shown["notation"] == note["notation"]
        self.assertEqual(leaks, 0, f"{leaks} secret row id(s) in a public record")
        self.assertEqual(sizes, 0, f"{sizes} public die size(s) tell what the secret layer took out")

    def test_every_secret_piece_is_rolled_secretly(self):
        for p1, p4 in self.runs[:45]:
            for label in ("secret_archetype", "secret_chooser", "secret_twist", "secret_trail",
                          "bbeg_visibility", "bbeg_shape", "bbeg_origin", "bbeg_tie", "bbeg_pole"):
                self.assertIn(p1.by_label[label], p1.secret)
                self.assertNotIn(label, p4.by_label, "P4 no longer rolls what P1 rolled")


class Legacy(unittest.TestCase):

    def test_a_used_file_that_names_a_removed_row_breaks_nothing(self):
        """An earlier birth drew a row this item removed; used.json keeps it hashed. The next draw ignores it."""
        real = dd.used_path
        tmp = Path(tempfile.mkdtemp()) / "used.json"
        tmp.write_text(json.dumps({"_meta": {"schema_version": 1}, "births": ["old-birth"], "campaigns": {"old-birth": {
            "secrets.yaml#archetype": ["h:" + next(iter(GONE)), dd.hashed("secret_no_such_row")],
            "antagonists.yaml#origin": [dd.hashed("origin_no_such_row")]}}}), encoding="utf-8")
        dd.used_path = lambda: tmp
        try:
            for ref in ("secrets.yaml#archetype", "antagonists.yaml#origin"):
                use = dd.usage("_test-item9", ref)
                res = arb.arbitrate(ref, rows(ref), arb.Context(), usage=use, secret=True)
                self.assertEqual(len(res["pool"]), len(usable(ref)), ref)
        finally:
            dd.used_path = real


class Stamps(unittest.TestCase):

    def test_the_stamps_cover_the_item_under_hashed_keys(self):
        covered = dt.reviewed_rows()
        for ref in SECRET + VILLAIN:
            self.assertIn(ref, dt.REVIEWED_TABLES)
            for i, r in enumerate(rows(ref)):
                self.assertEqual(covered.get(dt.stamp_key(r["id"], True)), dt.row_hash(r), where(ref, i))
                self.assertNotIn(r["id"], covered, f"{where(ref, i)} is stamped in clear")

    def test_the_stamp_file_and_the_listing_name_no_secret_row(self):
        text = dt.reviewed_path().read_text(encoding="utf-8")
        named_rows = sum(1 for rid in TABLE_OF if f'"{rid}"' in text)
        self.assertEqual(named_rows, 0, f"reviewed.json names {named_rows} secret row(s) in clear")
        listed = json.dumps(dt.unreviewed())
        self.assertEqual(sum(1 for rid in TABLE_OF if f'"{rid}"' in listed), 0)


class BurnSample(unittest.TestCase):
    """Six rows written to the tables' standard for the owner's eyes; they are spent: none is in the tables."""

    def test_the_six_are_in_no_table(self):
        text = BURN.read_text(encoding="utf-8")
        ids = re.findall(r"^- \*\*Kimlik:\*\* `([a-z_]+)`", text, re.MULTILINE)
        labels = re.findall(r"^- \*\*Etiket:\*\* (.+)$", text, re.MULTILINE)
        sentences = re.findall(r"^- \*\*Cümle:\*\* (.+)$", text, re.MULTILINE)
        self.assertEqual((len(ids), len(labels), len(sentences)), (6, 6, 6))
        self.assertEqual(sum(1 for x in ids if x.startswith("secret_")), 3)
        self.assertEqual(sum(1 for x in ids if x.startswith("shape_")), 3)
        tables = "\n".join((dt.tables_dir() / name).read_text(encoding="utf-8") for name in ("secrets.yaml", "antagonists.yaml")).lower()
        table_labels = {str(r.get("label", "")).lower() for ref in SECRET + VILLAIN for r in rows(ref)}
        table_values = {r.get("value") for ref in VILLAIN for r in rows(ref)}
        for rid, label, sentence in zip(ids, labels, sentences):
            self.assertNotIn(rid, ALL_IDS)
            self.assertNotIn(rid.split("_", 1)[1], table_values)
            self.assertNotIn(rid, tables)
            english = re.search(r"\(([^)]+)\)\s*$", label)
            self.assertIsNotNone(english, "every burned row gives its English label in brackets")
            self.assertNotIn(english.group(1).strip().lower(), table_labels)
            self.assertNotIn(sentence.strip().lower(), tables)


if __name__ == "__main__":
    unittest.main()
