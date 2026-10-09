"""
test_cosmos_names.py — build item 22n (docs/p2-build-22.md part 22n; docs/p2-tags.md "The cosmos's names" and the 22n
answers): every proper noun P2 makes comes from the pool. Five pattern groups in naming.yaml (planes, festivals, moons,
ages, events) in its part grammar; the word lists and the per-row words (history.yaml#event_type, foundation.yaml#action
`name_word`); the pool's `cosmos` section drawn after every other stock; the roller names each plane, age, event,
festival and moon and reserves the name under its frame id; the threat's own home plane takes its name from the secret
stock.

Over the corpus (in memory): no cosmos stock runs short at any scale, epic included; every name the roller gives stands;
no two names of one campaign collide; no stock holds a blacklisted name; the secret plane names stand in no public stock.
"""

import copy
import sys
import unittest
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import _corpus  # noqa: E402
import design_cosmos as dc  # noqa: E402
import design_names as dn  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402
import registry  # noqa: E402
from test_cosmos_roll import pin_of, pools_of  # noqa: E402

DOC = dt.load("naming.yaml")
PATTERNS = {p["id"]: p for rows in DOC["patterns"].values() for p in rows}
GOD_TYPES = {"evtype_miracle", "evtype_heresy"}      # the 22d audit (the owner); a silencing only under `god_when`
BIRTHS = 150           # every other one of the first 150: the scale turns every 45 births, so all three stand


class Tables(unittest.TestCase):
    """The patterns and the words as the owner approved them (2026-10-08) and the design tab answered (22n)."""

    def test_the_word_lists(self):
        w = DOC["words"]
        self.assertEqual(w["plane_words"], ["Realm", "Reach", "Deep", "Expanse", "Hollow", "Vault", "Wild", "Shore", "Court", "Gulf"])
        self.assertEqual(w["moon_words"], ["Watcher", "Eye", "Wanderer", "Hound", "Shield", "Maiden", "Sickle", "Crown"])
        self.assertEqual(w["festival_words"], ["Feast", "Night", "Day", "Vigil"])
        self.assertEqual(w["folk_festival_words"], ["Feast", "Night", "Day", "Vigil", "Fair"])
        self.assertEqual(w["ruler_words"], ["Kings", "Queens", "Lords", "Princes"])

    def test_five_pattern_groups_in_the_part_grammar(self):
        for group in ("plane", "festival", "moon", "age", "event"):
            self.assertIn(group, DOC["patterns"])
        self.assertEqual([p["lang"] for p in DOC["patterns"]["plane"]], ["common", "old"])
        self.assertEqual(len(DOC["patterns"]["moon"]), 2)
        for stock, pids in dn.COSMOS_STOCKS.items():
            for pid in pids:
                self.assertIn(pid, PATTERNS, stock)
        grammar = {"lit", "root", "settlement_tail", "word", "form_word", "name", "bag_word", "one_of", "name_word"}
        for group in ("plane", "festival", "moon", "age", "event"):
            for p in DOC["patterns"][group]:
                for part in p["parts"]:
                    self.assertTrue(set(part) & grammar, (p["id"], part))
                    if "word" in part:
                        self.assertIn(part["word"], DOC["words"], p["id"])

    def test_no_finished_name_in_the_table(self):
        """A shown name anchors births: no pattern carries a capitalised word that is no literal frame word."""
        frame = {"the", "The", "of", "Age", "Eve", "Fall", "Founding", "Silencing", "Wreck", "Loss", "s"}
        for group in ("plane", "festival", "moon", "age", "event"):
            for p in DOC["patterns"][group]:
                for part in p["parts"]:
                    for word in str(part.get("lit") or "").replace("'", " ").split():
                        self.assertIn(word, frame, (p["id"], word))

    def test_every_event_type_has_its_word(self):
        want = {"evtype_founding": "Founding", "evtype_treaty": "Treaty", "evtype_disaster": ["Burning", "Drowning", "Ruin"],
                "evtype_war": "War", "evtype_succession": "Crowning", "evtype_discovery": "Finding", "evtype_plague": "Sickness",
                "evtype_miracle": "Miracle", "evtype_heresy": "Heresy", "evtype_exile": "Exile", "evtype_migration": "Crossing",
                "evtype_vanishing": "Vanishing", "evtype_naming": "Naming", "evtype_wreck_or_loss": "Wreck",
                "evtype_silencing": "Silencing", "evtype_building": "Raising"}
        self.assertEqual({r["id"]: r.get("name_word") for r in dt.rows("history.yaml#event_type")}, want)
        # the 22n audit: the referent's kind is the type's table fact; a god only where the story is a god's
        refs = {r["id"]: r.get("name_referent") for r in dt.rows("history.yaml#event_type")}
        self.assertEqual({k for k, v in refs.items() if "god" in v}, GOD_TYPES)
        self.assertEqual(refs["evtype_silencing"], ["person", "place"])
        self.assertEqual(dt.row("history.yaml#event_type", "evtype_silencing")["god_when"], ["pantheon_silent_gods", "rel_silenced_one"])
        self.assertEqual(refs["evtype_war"], ["place", "person"])
        self.assertEqual(refs["evtype_wreck_or_loss"], ["ship", "place"])
        for k in ("evtype_founding", "evtype_treaty", "evtype_disaster", "evtype_plague", "evtype_migration",
                  "evtype_vanishing", "evtype_naming", "evtype_building"):
            self.assertEqual(refs[k], ["place"], k)
        for k in ("evtype_succession", "evtype_discovery", "evtype_exile"):
            self.assertEqual(refs[k], ["person"], k)

    def test_every_move_has_its_word(self):
        words = [r.get("name_word") for r in dt.rows_and_retired("foundation.yaml#action")]
        self.assertEqual(len(words), 31)
        self.assertEqual(dt.row("foundation.yaml#action", "act_split")["name_word"], "Dividing", "not Sundering (the owner)")
        self.assertTrue(all(isinstance(w, str) and w[:1].isupper() for w in words), words)
        self.assertEqual(len(words), len(set(words)), "the move's words differ")

    def test_the_ages_that_name_themselves(self):
        self.assertEqual(dt.row("history.yaml#age_template", "age_before")["label"], "The Time Before")
        for r in dt.rows("history.yaml#age_template"):
            if r["id"] != "age_now_named_for_fear":
                self.assertTrue(r["label"].startswith("The "), r["id"])

    def test_the_words_are_stamped(self):
        stamps = dt.read_stamps()
        for key in ("plane_words", "moon_words", "festival_words", "folk_festival_words", "ruler_words"):
            self.assertIn(f"naming:words:{key}", stamps)
        for pid in ("pattern_plane_word", "pattern_event", "pattern_age_present", "pattern_festival_god"):
            self.assertIn(f"naming:pattern:{pid}", stamps)
        self.assertEqual(dt.unreviewed(), {"missing": [], "changed": [], "gone": []})


class Corpus(unittest.TestCase):
    """The stocks and the roller's names over the corpus, every scale."""

    @classmethod
    def setUpClass(cls):
        cls.births = []
        for d, R1 in _corpus.births(BIRTHS)[::2]:
            pool, secret = pools_of(d, R1)
            S = designer.Roller.in_memory(R1.master, d, phase="P2")
            S.ctx = copy.deepcopy(R1.ctx)
            p1 = dict(dc.p1_of(R1), pinned_god=pin_of(R1, secret), institution_name=None)
            pub, sec = dc.roll(S, d, p1, pool, secret)
            cls.births.append((d, R1, pool, secret, pub, sec))

    def test_no_stock_runs_short(self):
        scales = Counter()
        for d, R1, pool, secret, pub, sec in self.births:
            scales[d["scale"]] += 1
            sizes = dn.cosmos_sizes(d["scale"])
            for key, n in sizes.items():
                self.assertGreaterEqual(len(pool["cosmos"][key]), n, f"{R1.master} ({d['scale']}): {key}")
            gods = ((pool["languages"].get(dn.gods_language(R1.naming)) or {}).get("god")) or []
            self.assertEqual({e["god"] for e in pool["cosmos"]["god_festivals"]}, {g["name"] for g in gods}, R1.master)
            self.assertEqual(len(secret["cosmos"]["planes"]), 1, R1.master)
        self.assertEqual(set(scales), {"short", "standard", "epic"})

    def test_every_record_is_named(self):
        for d, R1, pool, secret, pub, sec in self.births:
            for x in pub["planes"] + pub["ages"] + pub["events"] + pub["deep_events"] + pub["calendar"]["festivals"]:
                self.assertTrue(x.get("name"), f"{R1.master}: {x}")
            want = {"moon_none_stars": 0, "moon_two": 2}.get(pub["calendar"]["moon"], 1)
            self.assertEqual(len(pub["calendar"]["moon_names"]), want, R1.master)
            own = (sec.get("home_plane") or {}).get("own")
            if own:
                self.assertTrue(own["name"], R1.master)

    def test_the_shapes(self):
        for d, R1, pool, secret, pub, sec in self.births:
            gods = {g["n"]: g for g in pub["gods"]}
            for f in pub["calendar"]["festivals"]:
                god = gods.get(f["god"]) if f["god"] is not None else None
                if god and god.get("name"):
                    self.assertTrue(f["name"].startswith(god["name"] + "'s "), f["name"])
                else:
                    self.assertTrue(f["name"].startswith("the ") and " of the " in f["name"], f["name"])
            ruin = next((a for a in pub["ages"] if a["ruin"]), None)
            fall = next((e for e in pub["events"] if e.get("seat") == "ruin"), None)
            if ruin:
                self.assertEqual(ruin["name"].removeprefix("The Age of "), fall["name"].removeprefix("the Fall of "))
            move = next((e for e in pub["events"] if e.get("seat") == "move"), None)
            present = pub["ages"][-1]
            if move and R1.ctx.has("time_coming") and ruin and present["from_ago"] > 30:
                # the 22d re-audit: a present begun long before a move still to come is the age after the fall
                self.assertEqual(present["name"], "The Age after " + ruin["name"].removeprefix("The Age of "))
            elif move:
                eve = "The Eve of the " if R1.ctx.has("time_coming") else "The Age of the "
                self.assertEqual(present["name"], eve + move["name"].removeprefix("the "))
            gods_named = {g["name"] for g in pub["gods"] if g.get("name")}
            for e in pub["events"] + pub["deep_events"]:
                typ = e.get("type") or e.get("taught_type")
                if typ == "evtype_silencing":
                    self.assertTrue(e["name"].startswith("the Silencing of "), e["name"])
                ref = e["name"].split(" of ", 1)[-1]
                if ref in gods_named and e.get("seat") in (None, "origin"):
                    if typ == "evtype_silencing":       # a silent pantheon, or the silenced god of the web
                        names = {g["n"]: g.get("name") for g in pub["gods"]}
                        silenced = {names[r["b"]] for r in pub["relations"] if r["relation"] == "rel_silenced_one"}
                        self.assertTrue(pub["type"] == "pantheon_silent_gods" or ref in silenced, f"{R1.master}: {e['name']}")
                    else:
                        self.assertIn(typ, GOD_TYPES, f"{R1.master}: a god referent outside the god types: {e['name']}")
                if typ == "evtype_wreck_or_loss" and e.get("seat") is None:
                    self.assertTrue(e["name"].startswith(("the Wreck of the ", "the Loss of ")), e["name"])
                if e["name"].startswith("the Fall of "):
                    self.assertEqual(e.get("seat"), "ruin", f"{R1.master}: only the ruin's event is a fall: {e['name']}")
            for pl in pub["planes"]:
                if pl["baseline"] == dc.MOON:
                    self.assertEqual(pub["calendar"]["moon_names"], [pl["name"]])
            # the 22d audit: a moon's second pattern is a person-like name of the common tongue, one word
            for e in pool["cosmos"]["moons"]:
                if e["pattern"] == "pattern_moon_fresh":
                    self.assertTrue(e["name"].isalpha() and e["name"] == e["word"], e)

    def test_no_two_names_collide_and_none_is_blacklisted(self):
        bl, ok = registry.naming_blacklist(), dn.name_checker(set())
        for d, R1, pool, secret, pub, sec in self.births:
            names = [pl["name"] for pl in pub["planes"]] + [a["name"] for a in pub["ages"]]
            names += [e["name"] for e in pub["events"] + pub["deep_events"]] + [f["name"] for f in pub["calendar"]["festivals"]]
            names += [n for n in pub["calendar"]["moon_names"] if not any(pl["name"] == n for pl in pub["planes"])]
            low = [n.lower() for n in names]
            self.assertEqual(len(low), len(set(low)), f"{R1.master}: {sorted(n for n, c in Counter(low).items() if c > 1)}")
            stock = [e["name"] for v in pool["cosmos"].values() for e in v]
            self.assertEqual(len(stock), len({n.lower() for n in stock}), R1.master)
            for name in stock:
                self.assertFalse(registry.naming_errors("probe", {"type": "place", "name": name}, bl, set()), name)
                self.assertTrue(ok(name), name)
            public = dn._all_names(pool)
            for e in secret["cosmos"]["planes"]:
                self.assertNotIn(e["name"].lower(), public, f"{R1.master}: a secret plane name in a public stock")

    def test_each_name_is_reserved_under_its_id(self):
        for d, R1, pool, secret, pub, sec in self.births:
            held = {e["name"]: e.get("used_by") for v in pool["cosmos"].values() for e in v}
            for pl in pub["planes"]:
                self.assertEqual(held[pl["name"]], dc.plane_id(pl["baseline"]))
            for f in pub["calendar"]["festivals"]:
                self.assertEqual(held[f["name"]], f"calendar.festival.{f['n']}")
            ruin = next((a for a in pub["ages"] if a["ruin"]), None)
            if ruin:
                self.assertEqual(held[ruin["name"].removeprefix("The Age of ")], f"era_{ruin['n']}")


if __name__ == "__main__":
    unittest.main()
