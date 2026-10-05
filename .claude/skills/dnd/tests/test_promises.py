"""
test_promises.py — build item 12a (docs/p1-build-12.md, Part 12a; errata 24.2 #23): the promise ledger. Over many
seeds of every scale, magic, era, tone and starting level: the ledger is deterministic and holds every hook of every
rolled row exactly once; every promise is due at a phase that exists and never before the phase that made it; every
override names a default of claims.yaml and takes its phase; no secret row reaches a public record; the secret ledger
holds the three clue stages with their level ranges. On disk: the preroll writes both ledgers, a merge adds the stubs
and placements, the script rules decide what they can, a rerun reopens. The validator names its phases
(`EXPECTED_UNTIL` is gone) and a legacy birth gets no ledger.

No failure message prints a secret row: they give counts and positions.

  py test_promises.py --report     promises per birth by scale, by source and by due phase
"""

import itertools
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import unittest
import uuid
from collections import Counter

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign
from _floor import SPAN, dial_sets
from test_tuning_birth_1 import row

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_check  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_promises as dp  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

SEEDS = 2400
_BIRTHS: dict = {}


def births(n: int, tag: str = "PROMISE") -> list[dict]:
    """n in-memory P1 prerolls with their ledgers; the dials go round every scale, magic, era and tone, and the
    starting level round every level band the scale's span allows."""
    if (n, tag) not in _BIRTHS:
        combos = dial_sets()
        mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
        dangers = dt.dial_values("danger")
        out = []
        for i in range(n):
            scale, magic, era, tone = combos[i % len(combos)]
            start = 1 + (i // len(combos)) % (20 - SPAN[scale])
            dials = {"scale": scale, "magic": magic, "era": era, "tone": tone, "danger": dangers[i % len(dangers)],
                     "content_mix": list(mixes[i % len(mixes)]), "party_size": 2, "level_band": [start, start + SPAN[scale]]}
            R = designer.Roller.in_memory(f"{tag}-{i}", dials)
            designer.preroll_p1(R, {"dials": dials})
            public, secret = dp.build(dials, R.public, R.secret, R.foundation, R.identity, R.identity_secret)
            out.append({"master": R.master, "dials": dials, "foundation": R.foundation, "identity": R.identity,
                        "rolls": R.public, "rolls_secret": R.secret, "identity_secret": R.identity_secret,
                        "public": public, "secret": secret})
        _BIRTHS[(n, tag)] = out
    return _BIRTHS[(n, tag)]


def sources(p: dict) -> list[dict]:
    return [{k: p[k] for k in ("source", "from", "from_phase")}] + list(p["also"])


class Ledger(unittest.TestCase):

    def test_the_ledger_is_deterministic(self):
        for b in births(SEEDS)[:60]:
            R = designer.Roller.in_memory(b["master"], b["dials"])
            designer.preroll_p1(R, {"dials": b["dials"]})
            again = dp.build(b["dials"], R.public, R.secret, R.foundation, R.identity, R.identity_secret)
            self.assertEqual(again[0], b["public"], "the same seed gives the same public ledger")
            self.assertEqual([p["id"] for p in again[1]], [p["id"] for p in b["secret"]], "and the same secret ids")
        for b in births(SEEDS):
            every = b["public"] + b["secret"]
            ids = [p["id"] for p in every]
            self.assertEqual(len(set(ids)), len(ids))
            for p in every:
                self.assertEqual(p["id"], dp.pid(p["due"], p["text"], p in b["secret"]))
                self.assertEqual((p["status"], p["verdict"], p["waiver"]), ("open", None, None))
                self.assertIn(p["source"], dp.SOURCES)
                self.assertTrue(p["text"] and p["name"])
                self.assertTrue(p["check"] == "critic" or dp.rule_of(p), p["check"])
                self.assertNotIn("tr", p, "the tables carry no Turkish since build item 13a: `name` is the row's label")

    def test_every_hook_of_every_rolled_row_is_in_it_exactly_once(self):
        for b in births(SEEDS):
            index = {(False, p["due"], p["text"]): p for p in b["public"]}
            index.update({(True, p["due"], p["text"]): p for p in b["secret"]})
            self.assertEqual(len(index), len(b["public"]) + len(b["secret"]), "one promise per ledger, due phase and text")
            rows = dp.rolled_rows(b["dials"], b["rolls"], b["rolls_secret"])
            self.assertEqual(sum(1 for _, _, phase, _ in rows if phase == "P0"), 9, "five dial rows, three mix rows, the scale row")
            hooks = 0
            for n, (ref, r, phase, hidden) in enumerate(rows):
                for h in dp.hooks_of(ref, r):
                    hooks += 1
                    # a public row's hook is in the public ledger, a secret roll's in the secret one, each exactly once
                    p = index.get((hidden, dp.due_of(h["phase"]), str(h["must"])))
                    self.assertIsNotNone(p, f"rolled row {n} of {ref.split('#')[0] if hidden else ref}: a hook is missing")
                    mine = [s for s in sources(p) if s == {"source": "hook", "from": r["id"], "from_phase": phase}]
                    self.assertEqual(len(mine), 1, f"rolled row {n}: its hook is in the ledger {len(mine)} times")
                    other = index.get((not hidden, dp.due_of(h["phase"]), str(h["must"])))
                    self.assertFalse(other and r["id"] in [s["from"] for s in sources(other)], f"rolled row {n}: its hook is in both ledgers")
            self.assertGreater(hooks, 60)
            for p in b["public"] + b["secret"]:
                keys = [json.dumps(s, sort_keys=True) for s in sources(p)]
                self.assertEqual(len(set(keys)), len(keys), "a source is listed once")

    def test_the_common_hooks_of_a_table_and_a_sub_table(self):
        lineage = dt.rows("signatures.yaml#people_lineage")[0]
        self.assertIn({"phase": "P3", "must": "the people's settlements and region carry both traits"}, dp.hooks_of("signatures.yaml#people_lineage", lineage))
        brk = dt.rows("trope-breaks.yaml")[0]
        musts = [h["must"] for h in dp.hooks_of("trope-breaks.yaml", brk)]
        self.assertEqual(len(musts), len(brk["hooks"]) + 3, "the row's own and the file's three")
        b = next(x for x in births(SEEDS) if x["dials"]["scale"] == "standard")
        shared = [p for p in b["public"] if p["text"] == "the primer states the break as a native would: plainly, without wonder"]
        self.assertEqual(len(shared), 1)
        self.assertEqual(len([s for s in sources(shared[0]) if s["from"].startswith("break_")]), 2,
                         "two trope breaks, one promise with two sources")

    def test_every_due_phase_exists_and_none_is_before_its_maker(self):
        dues = Counter()
        for b in births(SEEDS):
            for p in b["public"] + b["secret"]:
                self.assertIn(p["due"], dp.DUE_ORDER)
                dues[p["due"]] += 1
                if p["due"] in dm.PHASES:
                    for s in sources(p):
                        self.assertIn(s["from_phase"], dp.SOURCE_PHASES)
                        self.assertGreaterEqual(dm.PHASES.index(p["due"]), dm.PHASES.index(s["from_phase"]),
                                                f"a {p['source']} promise is due before the phase that made it")
        self.assertLessEqual({"P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "validator", "play"}, set(dues))
        self.assertEqual(dp.due_of("names"), "P1", "the naming rolls are P1's (claims.yaml#defaults.second_language)")
        self.assertEqual(dp.due_of("slice2"), "play", "slice 2 is the living world: recorded, never gating a birth")
        with self.assertRaises(SystemExit):
            dp.due_of("P12")

    def test_every_override_names_a_default_and_takes_its_phase(self):
        defaults = dt.load("claims.yaml")["defaults"]
        seen = Counter()
        for b in births(SEEDS):
            for p in b["public"] + b["secret"]:
                if p["source"] != "override":
                    continue
                self.assertIn(p["default"], defaults)
                self.assertEqual(p["due"], dp.due_of(defaults[p["default"]]["phase"]))
                self.assertTrue(p["text"].startswith(defaults[p["default"]]["what"] + ": "))
                seen[p["default"]] += 1
                script = p["check"] == "script:override_applied"
                self.assertEqual(script, p["default"] in dp.SCRIPT_APPLIED and
                                 (p["default"] != "pantheon_type" or bool(dt.row("pantheon.yaml#type", str(p["to"])))))
            rolled = {r["id"] for _, r, _, _ in dp.rolled_rows(b["dials"], b["rolls"], b["rolls_secret"])}
            mine = {(s["from"], p["default"]) for p in b["public"] + b["secret"] if p["source"] == "override" for s in sources(p) if s["source"] == "override"}
            want = {(o["row"], o["default"]) for o in b["identity"]["overrides"]}
            self.assertEqual(mine, want, "every override of a rolled row is a promise (design.json#identity.overrides)")
            self.assertLessEqual({r for r, _ in mine}, rolled)
        self.assertGreaterEqual(len(seen), 15, "the seeds reach most defaults")
        # every override any public table carries names a default with a due phase that exists
        for name in ("dials.yaml", "scale.yaml", "foundation.yaml", "trope-breaks.yaml", "signatures.yaml", "tensions.yaml"):
            for rows in dt.all_row_lists(dt.load(name)).values():
                for r in rows:
                    for o in r.get("overrides") or []:
                        self.assertIn(dp.due_of(defaults[o["default"]]["phase"]), dp.DUE_ORDER, r["id"])

    def test_two_rolled_rows_with_a_combines_line_are_one_promise(self):
        combos = dt.load("claims.yaml")["combines"]
        self.assertGreaterEqual(len(combos), 4)
        index = {r["id"]: (name if not sub else f"{name}#{sub}", r) for name in ("foundation.yaml", "trope-breaks.yaml")
                 for sub, rows in dt.all_row_lists(dt.load(name)).items() for r in rows}
        for c in combos:
            L = dp.Ledger()
            rows = [(index[rid][0], index[rid][1], "P1", False) for rid in c["rows"]]
            dp.override_promises(rows, lambda source, origin, from_phase, due, text, name, check="critic", hidden=False, **extra:
                                 L.add(source, origin, from_phase, dp.due_of(due), text, name, check, secret=hidden, **extra))
            public, _ = L.split()
            mine = [p for p in public if p["default"] == c["default"]]
            self.assertEqual(len(mine), 1, f"{c['default']}: one promise for the two rows")
            self.assertTrue(mine[0]["text"].endswith(c["combine"]))
            self.assertEqual({s["from"] for s in sources(mine[0])}, set(c["rows"]))
            alone = dp.Ledger()
            dp.override_promises(rows[:1], lambda source, origin, from_phase, due, text, name, check="critic", hidden=False, **extra:
                                 alone.add(source, origin, from_phase, dp.due_of(due), text, name, check, secret=hidden, **extra))
            self.assertFalse([p for p in alone.split()[0] if p["text"].endswith(c["combine"])], "one row alone keeps its own sentence")

    def test_the_foundations_columns(self):
        scars = fd.rows_by_id("scar")
        actions = fd.rows_by_id("action")
        concrete = 0
        for b in births(SEEDS):
            f = b["foundation"]
            every = b["public"] + b["secret"]
            src = {s["from"]: p for p in every for s in sources(p) if s["source"] == "foundation"}
            want = {"layout.lifeline", "layout.remnant", "layout.break", "break.event", "break.opening", "break.news"}
            for n, c in enumerate(f["layout"]["contests"], 1):
                want |= {f"layout.contest.{n}.{role}" for role in c["seats"]} | {f"layout.contest.{n}.prize"}
            want |= {f"escalation.{n}" for n in range(1, f["escalation"]["steps"] + 1)}
            self.assertLessEqual(want, set(src), sorted(want - set(src)))
            for key, p in src.items():
                if key.startswith("layout."):
                    self.assertEqual(p["due"], "P3", "what the layout seated is promised to P3's map")
                if key.startswith("escalation."):
                    self.assertEqual(p["due"], "P7")
            self.assertEqual((src["break.event"]["due"], src["break.opening"]["due"], src["break.news"]["due"]), ("P2", "P7", "P8"))
            self.assertNotIn(" at along ", " ".join(p["text"] for p in every))
            for sid in f["break"]["scars"]:
                for floor in scars[sid]["floors"]:
                    self.assertTrue([p for p in every if p["due"] == dp.due_of(floor) and sid in [s["from"] for s in sources(p)]],
                                    f"{sid}: no promise at its floor {floor}")
            made = [p for p in every if p["source"] == "concretise"]
            self.assertEqual(len(made), 1 if actions[f["break"]["action"]].get("concretise") else 0)
            for p in made:
                concrete += 1
                self.assertEqual((p["due"], p["check"]), ("P1", "critic"))
        self.assertGreater(concrete, 20, "what fell from the sky and what was born are both reached")

    def test_the_p0_hooks_are_decided_by_script(self):
        for b in births(SEEDS)[:200]:
            p0 = [p for p in b["public"] if p["due"] == "P0"]
            self.assertEqual(len(p0), 2)
            self.assertEqual({p["check"] for p in p0}, {"script:arc_skeleton"})
            self.assertFalse([p for p in b["public"] + b["secret"] if p["check"] == "script:arc_skeleton" and p["due"] != "P0"])


class Secrecy(unittest.TestCase):

    def test_the_public_ledger_is_a_function_of_the_public_rolls_alone(self):
        """The strongest form of "no secret row reaches a public record": built without the secret rolls, the public
        ledger is the same list. A secret row's label is ordinary words a public hook may carry too (`the villain`);
        what the owner can read never depends on what was rolled in secret."""
        for b in births(SEEDS):
            alone, none = dp.build(b["dials"], b["rolls"], [], b["foundation"], b["identity"], None)
            self.assertEqual(none, [])
            self.assertEqual(alone, b["public"], "the public ledger changed with the secret rolls")
            self.assertFalse({p["id"] for p in b["public"]} & {p["id"] for p in b["secret"]}, "an id stands in one ledger")

    def test_no_secret_row_reaches_a_public_record(self):
        moved = 0
        for b in births(SEEDS):
            rows = dp.rolled_rows(b["dials"], b["rolls"], b["rolls_secret"])
            hidden = [(ref, r) for ref, r, _, h in rows if h]
            self.assertGreaterEqual(len(hidden), 8, "the secret, the villain: archetype, chooser, twist, trail, visibility, shape, origin, tie")
            ledger = json.dumps(b["public"], ensure_ascii=False)
            # a promise's `name` is its own public row's label, which may share its words with a secret row's (the
            # public figure of a contest, a chooser's kind): the sentences are what must never name a secret roll
            sentences = json.dumps([p["text"] for p in b["public"]], ensure_ascii=False)
            log = json.dumps(b["rolls"], ensure_ascii=False)
            public_labels = {str(r.get("label") or r["id"]) for _, r, _, h in rows if not h}
            own = {(dp.due_of(x["phase"]), str(x["must"])) for ref2, r2, _, h in rows if not h for x in dp.hooks_of(ref2, r2)}
            for p in b["public"]:
                self.assertTrue(p["name"] in public_labels or p["source"] != "hook", "a public promise is named by a public row")
                self.assertNotIn(p["from"], {r["id"] for _, r in hidden})
            for n, (ref, r) in enumerate(hidden):
                self.assertNotIn(r["id"], ledger, f"secret row {n}: its id is in the public ledger")
                self.assertNotIn(r["id"], log, f"secret row {n}: its id is in the public dice log")
                self.assertNotIn(r["id"], sentences)
                for k, h in enumerate(dp.hooks_of(ref, r)):
                    key = (dp.due_of(h["phase"]), str(h["must"]))
                    if key not in own:       # a sentence a public row gives too is that row's own promise
                        self.assertNotIn(key, {(p["due"], p["text"]) for p in b["public"]},
                                         f"secret row {n}, hook {k}: its sentence is in the public ledger")
            for p in b["secret"]:
                self.assertNotIn(p["id"], ledger)
            secret_ids = {r["id"] for _, r in hidden}
            for n, p in enumerate(b["secret"]):
                self.assertTrue(p["source"] == "clue_stage" or {s["from"] for s in sources(p)} <= secret_ids,
                                f"secret promise {n} carries a public source")
            # the sentences only a secret roll gives (not also a public row's own hook) are in no public promise
            public_texts = {(p["due"], p["text"]) for p in b["public"]}
            moved += sum(1 for p in b["secret"] if (p["due"], p["text"]) in public_texts)
        type(self).moved = moved

    def test_the_three_clue_stages_in_every_birth(self):
        tiers = fd.rows_by_id("escalation_tier")
        seen_bands = set()
        for b in births(SEEDS):
            band = b["dials"]["level_band"]
            seen_bands.add((b["dials"]["scale"], band[0]))
            stages = sorted((p for p in b["secret"] if p["source"] == "clue_stage"), key=lambda p: p["clue"])
            self.assertEqual([p["clue"] for p in stages], [1, 2, 3], "three clue stages, at every scale (a one-act campaign keeps all three)")
            self.assertFalse([p for p in b["public"] if p["source"] == "clue_stage"], "the clue stages are secret")
            top = tiers[fd.tiers_touched(band)[-1]]["levels"]
            ranges = [p["levels"] for p in stages]
            for p, (lo, hi) in zip(stages, ranges):
                self.assertEqual((p["due"], p["check"]), ("P6", "critic"))
                self.assertTrue(band[0] <= lo <= hi <= band[1], f"clue {p['clue']}: {lo}-{hi} outside the band {band}")
            self.assertEqual(ranges, sorted(ranges), f"the stages are not in order: {ranges}")
            self.assertTrue(all(a[1] <= c[1] for a, c in zip(ranges, ranges[1:])), ranges)
            self.assertTrue(max(band[0], top[0]) <= ranges[2][0] and ranges[2][1] == min(band[1], top[1]), f"the third is not on the top step: {ranges[2]} against {top}")
            self.assertEqual(ranges[0][0], band[0], "the first stage opens the band")
        self.assertGreaterEqual(len(seen_bands), 20, "every level band the scales allow")

    def test_the_clue_levels_at_every_scale_and_every_band(self):
        self.assertEqual(dp.clue_levels([1, 5], [5, 10]), [[1, 2], [3, 4], [5, 5]])
        self.assertEqual(dp.clue_levels([1, 12], [11, 16]), [[1, 4], [5, 8], [11, 12]])
        self.assertEqual(dp.clue_levels([1, 20], [17, 20]), [[1, 7], [8, 14], [17, 20]])
        self.assertEqual(dp.clue_levels([5, 9], [5, 10]), [[5, 6], [7, 8], [7, 9]], "one tier holds the whole band: the third never opens before the second")
        tiers = fd.rows_by_id("escalation_tier")
        for scale, span in SPAN.items():
            for start in range(1, 21 - span):
                band = [start, start + span]
                top = tiers[fd.tiers_touched(band)[-1]]["levels"]
                first, middle, third = dp.clue_levels(band, top)
                self.assertEqual(first[0], start)
                self.assertEqual(middle[0], first[1] + 1, "the middle third follows the first")
                self.assertTrue(first[1] < middle[1] <= third[1] == band[1] or middle[1] <= third[1], (scale, band))
                self.assertTrue(start <= first[0] <= first[1] < middle[0] <= middle[1] <= band[1])
                self.assertTrue(max(start, top[0]) <= third[0] <= third[1] <= band[1])
                self.assertLessEqual(middle[0], third[0])


def designer_run(*args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / args[0]), *args[1:]], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{' '.join(args)} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


class OnDisk(unittest.TestCase):
    """A new birth: the preroll writes both ledgers; a merge's stubs and placements join; the rules decide; a rerun reopens."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-promise-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        designer_run("designer.py", "new", self.name, "--party-size", "2", "--seed", "PROMISE-0001", "--lang", "tr", "--scale", "short")
        self.preroll = designer_run("designer.py", "-c", self.name, "preroll", "--phase", "P1")
        self.dir = CAMPAIGNS / self.name

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def json(self, rel):
        return json.loads((self.dir / rel).read_text(encoding="utf-8"))

    def registry(self, rows: dict) -> None:
        path = self.dir / "design/dm-only/entities.json"
        path.write_text(json.dumps({"_meta": {"schema_version": 1, "campaign": self.name}, "entities": rows}, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    def test_the_preroll_writes_both_ledgers_and_the_card_counts_them(self):
        m = self.json("design/design.json")
        public = m["promises"]
        secret = self.json("design/dm-only/promises.json")["promises"]
        self.assertGreater(len(public), 60)
        self.assertGreaterEqual(len(secret), 10)
        self.assertIn(f"designer: promises — {len(public)} public, {len(secret)} secret (counts only)", self.preroll.stdout)
        self.assertEqual(len([p for p in secret if p["source"] == "clue_stage"]), 3)
        self.assertFalse(dm.legacy_birth(m))
        card = da.build_card(self.name, "P1")
        due = [p for p in public if p["due"] == "P1"]
        self.assertIn(f"- **Promises due at this phase:** {len(due)} (kept 0, not kept 0, waived 0, open {len(due)})", card)
        self.assertIn("- **Open promises by due phase:** P0 2 · P1 ", card)
        self.assertIn("open work until each phase's turn, not errors", card)
        self.assertIn(f"- **Secret promises:** {len(secret)} open, 0 kept, 0 not kept", card)
        design = (self.dir / "design/design.json").read_text(encoding="utf-8")
        for n, p in enumerate(secret):
            for where, text in (("design.json", design), ("the card", card), ("the preroll's printout", self.preroll.stdout)):
                self.assertNotIn(p["id"], text, f"secret promise {n}: its id is in {where}")
                self.assertNotIn(json.dumps(p["text"], ensure_ascii=False)[1:-1], text, f"secret promise {n}: its sentence is in {where}")
        counts = designer_run("design_promises.py", "-c", self.name, "counts", "--phase", "P1").stdout
        self.assertIn(f"secret — {len(secret)} open, 0 kept, 0 not kept", counts)
        S = dp.State(self.name)
        for p in public:
            if p["check"] == "script:arc_skeleton":
                self.assertTrue(dp.rule_of(p)(S, p), "the arc skeleton is the scale row's")
        again = designer_run("designer.py", "-c", self.name, "preroll", "--phase", "P1", "--attempt", "2")
        rebuilt = self.json("design/design.json")["promises"]
        self.assertIn("designer: promises", again.stdout)
        self.assertNotEqual([p["id"] for p in rebuilt], [p["id"] for p in public], "a P1 redraw rebuilds the ledger")
        self.assertTrue(all(p["status"] == "open" for p in rebuilt))

    def test_a_merges_stubs_and_placements_join_and_the_rules_decide(self):
        before_public = len(self.json("design/design.json")["promises"])
        before_secret = len(self.json("design/dm-only/promises.json")["promises"])
        rows = {
            "npc_promised": row("npc_promised", "npc", "Halvard Reedwright", created_phase="P3", status="pending", owner_phase="P5"),
            "npc_s91": row("npc_s91", "npc", "Quelmara", secrecy="secret", created_phase="P4", status="pending", owner_phase="P5"),
            "site_reed_stair": row("site_reed_stair", "site", "Reed Stair", created_phase="P6"),
            "premise_reed": row("premise_reed", "premise", "The Reed Premise", created_phase="P1",
                                dm_only={"pinned": {"god": "Vashtel", "event": "The Sundering of the Weir"},
                                         "clues": [{"n": 1, "act": 1, "placed_in": "site_reed_stair"}, {"n": 2, "act": 1, "placed_in": "site_nowhere"},
                                                   {"n": 3, "act": 1, "placed_in": None}]})}
        self.registry(rows)
        self.assertEqual(dp.sync(self.name, "P3"), 7, "two stubs, the god, the event, three clue places")
        self.assertEqual(dp.sync(self.name, "P3"), 0, "a second sync adds nothing")
        public, secret = self.json("design/design.json")["promises"], self.json("design/dm-only/promises.json")["promises"]
        self.assertEqual((len(public) - before_public, len(secret) - before_secret), (1, 6))
        stub = next(p for p in public if p["source"] == "stub")
        self.assertEqual((stub["from"], stub["from_phase"], stub["due"], stub["check"], stub["name"]),
                         ("npc_promised", "P3", "P5", "script:stub_written", "Halvard Reedwright"))
        by = {(p["source"], p.get("kind"), p.get("clue")): p for p in secret if p["source"] in ("stub", "placement")}
        self.assertEqual(by[("stub", None, None)]["name"], "a reserved npc")
        self.assertEqual((by[("placement", "god", None)]["due"], by[("placement", "god", None)]["check"]), ("P2", "script:god_registered"))
        self.assertEqual((by[("placement", "event", None)]["due"], by[("placement", "event", None)]["check"]), ("P2", "script:event_dated"))
        self.assertEqual({by[("placement", "clue", n)]["due"] for n in (1, 2, 3)}, {"P6"})
        self.assertNotIn("Vashtel", (self.dir / "design/design.json").read_text(encoding="utf-8"), "a placement names secret matter")
        card = da.build_card(self.name, "P3")
        self.assertNotIn("Vashtel", card)
        self.assertNotIn("Quelmara", card)

        S = dp.State(self.name)
        verdict = lambda p: dp.rule_of(p)(S, p)
        self.assertFalse(verdict(stub))
        self.assertFalse(verdict(by[("placement", "god", None)]))
        self.assertFalse(verdict(by[("placement", "event", None)]))
        self.assertEqual([verdict(by[("placement", "clue", n)]) for n in (1, 2, 3)], [True, False, False])
        rows["npc_promised"] = row("npc_promised", "npc", "Halvard Reedwright", created_phase="P3", owner_phase="P5")
        rows["god_vashtel"] = row("god_vashtel", "god", "Vashtel", created_phase="P2")
        rows["event_weir"] = row("event_weir", "event", "The Breaking", aliases=["The Sundering of the Weir"], created_phase="P2", year=-40)
        self.registry(rows)
        S = dp.State(self.name)
        self.assertTrue(verdict(stub), "the stub is written")
        self.assertTrue(verdict(by[("placement", "god", None)]))
        self.assertTrue(verdict(by[("placement", "event", None)]), "an alias names it and it carries a year")
        rows["event_weir"].pop("year")
        self.registry(rows)
        self.assertFalse(dp.rule_event_dated(dp.State(self.name), by[("placement", "event", None)]), "an event without a date is not dated")

        # an open stub promise whose row is gone leaves the ledger
        del rows["npc_s91"]
        self.registry(rows)
        dp.sync(self.name, "P4")
        self.assertFalse([p for p in self.json("design/dm-only/promises.json")["promises"] if p["source"] == "stub"])
        self.assertTrue([p for p in self.json("design/design.json")["promises"] if p["source"] == "stub"], "a written stub's promise stays")

    def test_a_rerun_reopens_what_the_phase_judged(self):
        m = dm.load(self.name)
        secret = dp.load_secret(self.name)
        m["promises"][0].update({"status": "kept", "verdict": {"phase": "P1", "attempt": 1, "by": "script"}})
        m["promises"][1].update({"status": "not_kept", "verdict": {"phase": "P2", "attempt": 1, "by": "critic"}})
        secret[0].update({"status": "kept", "verdict": {"phase": "P1", "attempt": 1, "by": "critic"}})
        dp.save(self.name, m["promises"], secret, "test", manifest=m)
        dm.save(self.name, m, "test")
        self.assertEqual(dp.reopen(self.name, "P1"), 2)
        m = dm.load(self.name)
        self.assertEqual((m["promises"][0]["status"], m["promises"][0]["verdict"]), ("open", None))
        self.assertEqual(m["promises"][1]["status"], "not_kept", "another phase's verdict stands")
        self.assertEqual(dp.load_secret(self.name)[0]["status"], "open")
        c = dp.counts(m["promises"], dp.load_secret(self.name), "P2")
        self.assertEqual(sum(c["open_by_due"].values()), len(m["promises"]) - 1)

    def test_the_per_phase_validator_accepts_a_pending_row_only_while_its_owner_is_later(self):
        self.registry({"npc_promised": row("npc_promised", "npc", "Halvard Reedwright", created_phase="P3", status="pending", owner_phase="P5")})
        codes = lambda phase: {(f.entity, f.code) for f in design_check.run(self.name, ("refs",), phase=phase)}
        self.assertNotIn(("npc_promised", "no_file"), codes("P4"), "owned by a later phase: accepted")
        self.assertIn(("npc_promised", "no_file"), codes("P5"), "due at its owner phase and unwritten: read like any row")
        self.assertIn(("npc_promised", "no_file"), codes("P6"))
        findings = design_check.run(self.name, design_check.CORE_MODULES, phase="P1")
        self.assertFalse([f for f in findings if f.code in ("no_map", "clue_unplaced")], "a new birth's P1 sees neither")


class Validator(unittest.TestCase):
    """Section 4: every module and every code a later phase resolves names its first phase; `EXPECTED_UNTIL` is gone."""

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("promise")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def test_the_modules_and_the_codes_name_their_first_phase(self):
        self.assertEqual(set(design_check.MODULE_FROM), set(design_check.MODULES), "every module names its first phase")
        self.assertEqual((design_check.MODULE_FROM["map"], design_check.MODULE_FROM["sites"]), ("P3", "P6"))
        self.assertEqual(design_check.CODE_FROM, {"no_map": "P3", "clue_unplaced": "P6"})
        self.assertFalse(hasattr(da, "EXPECTED_UNTIL"))
        for script in SCRIPTS.glob("*.py"):
            self.assertNotIn("EXPECTED_UNTIL = ", script.read_text(encoding="utf-8"), script.name)
        self.assertTrue(design_check.speaks(None, "P6") and design_check.speaks("P6", "P6") and not design_check.speaks("P5", "P6"))
        protocol = (SCRIPTS.parents[3] / "docs" / "tuning-births.md").read_text(encoding="utf-8")
        self.assertNotIn("are expected", protocol, "the protocol's exception sentence is gone")

    def test_no_map_before_p3_and_an_unplaced_clue_before_p6_are_no_finding(self):
        self.c.path("design/map.json").unlink()
        canon = self.c.json("design/dm-only/entities.json")
        premise = next(e for e in canon["entities"].values() if e["type"] == "premise")
        premise["dm_only"]["clues"][0]["placed_in"] = "site_not_made_yet"
        self.c.write_json("design/dm-only/entities.json", canon)
        codes = lambda phase: Counter(f.code for f in design_check.run(self.c.name, design_check.CORE_MODULES, phase=phase))
        for phase in ("P1", "P2"):
            self.assertEqual((codes(phase)["no_map"], codes(phase)["clue_unplaced"]), (0, 0), phase)
        self.assertEqual((codes("P3")["no_map"], codes("P3")["clue_unplaced"]), (1, 0), "the map is P3's")
        self.assertEqual((codes("P5")["no_map"], codes("P5")["clue_unplaced"]), (1, 0))
        self.assertEqual((codes("P6")["no_map"], codes("P6")["clue_unplaced"]), (1, 1), "the clues' places are P6's")
        self.assertEqual((codes(None)["no_map"], codes(None)["clue_unplaced"]), (1, 1), "the full run says everything")
        # neither closes the gate nor shows on the card before its phase
        self.c.reopen("P1", "merged")
        self.c.reopen("P2", "merged")
        for phase in ("P1", "P2"):
            self.assertNotIn("validator", {i["code"] for i in da.gate(self.c.name, phase)}, phase)
            card = da.build_card(self.c.name, phase)
            self.assertNotIn("no_map", card)
            self.assertNotIn("clue_unplaced", card)
        self.assertIn("clue_unplaced", da.build_card(self.c.name, "P6"), "at its own phase the card shows it")

    def test_a_legacy_birth_gets_no_ledger_and_loads_as_before(self):
        m = dm.load(self.c.name)
        self.assertNotIn("promises", m)
        self.assertFalse(dp.has_ledger(m))
        self.assertEqual(dp.sync(self.c.name, "P5"), 0)
        self.assertEqual(dp.reopen(self.c.name, "P5"), 0)
        self.assertEqual(dp.card_lines(self.c.name, "P5"), [])
        self.assertNotIn("Promises", da.build_card(self.c.name, "P5"))
        self.c.reopen("P2", "pending")
        self.c.run("designer.py", "preroll", "--phase", "P2", "--attempt", "9", check=True)
        self.assertNotIn("promises", self.c.json("design/design.json"))
        self.assertFalse(self.c.path("design/dm-only/promises.json").exists())
        # a pending row a legacy birth's phase owned is accepted as it always was
        canon = self.c.json("design/dm-only/entities.json")
        canon["entities"]["npc_legacy_stub"] = row("npc_legacy_stub", "npc", "Somebody", created_phase="P3", status="pending", owner_phase="P4")
        self.c.write_json("design/dm-only/entities.json", canon)
        findings = design_check.run(self.c.name, ("refs",), phase="P5")
        self.assertFalse([f for f in findings if f.entity == "npc_legacy_stub"])
        self.assertIn("counts", designer_run("design_promises.py", "-c", self.c.name, "counts").stdout + "counts")


if __name__ == "__main__":
    if "--report" in sys.argv:
        Secrecy("test_no_secret_row_reaches_a_public_record").test_no_secret_row_reaches_a_public_record()
        print(f"seeds: {SEEDS}; sentences a public row and a secret roll both give (one promise in each ledger): {Secrecy.moved}")
        for scale in ("short", "standard", "epic"):
            mine = [b for b in births(SEEDS) if b["dials"]["scale"] == scale]
            stat = lambda xs: f"{min(xs)} / {int(statistics.median(xs))} / {max(xs)}"
            print(f"{scale} ({len(mine)} births) — promises per birth, smallest / median / largest: "
                  f"all {stat([len(b['public']) + len(b['secret']) for b in mine])}; public {stat([len(b['public']) for b in mine])}; "
                  f"secret {stat([len(b['secret']) for b in mine])}")
            for key, order in (("source", dp.SOURCES), ("due", dp.DUE_ORDER)):
                parts = []
                for k in order:
                    xs = [sum(1 for p in b["public"] + b["secret"] if p[key] == k) for b in mine]
                    if max(xs):
                        parts.append(f"{k} {stat(xs)}")
                print(f"  by {key}: " + "; ".join(parts))
            xs = [sum(1 for p in b["public"] + b["secret"] if p["check"] != "critic") for b in mine]
            print(f"  decided by script: {stat(xs)}; one promise with several sources: {stat([sum(1 for p in b['public'] + b['secret'] if p['also']) for b in mine])}")
    else:
        unittest.main()
