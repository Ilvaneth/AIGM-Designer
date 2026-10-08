"""
test_p1_story.py — build item 18e (docs/p1-build-18.md, Part 18e): the spine sentence in every birth and first on the
card; the writer's prompt on the chain's records with none of the removed decisions; the door refuses a texture piece
in a clue's place or the pin, and a hidden truth that serves no clue; the rubrics' texts; the card's secret line, its
D&D line and the gate `dnd_incomplete`; the god pin and the mechanic's shape rolled; the twists that name a piece
require it. Failure messages give counts and positions only.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
import uuid

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard

sys.path.insert(0, str(SCRIPTS))
import design_approval as da  # noqa: E402
import design_arbiter as arb  # noqa: E402
import design_door as door  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_prompts as dpm  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402
import _corpus  # noqa: E402  (build item 18f-1: the shared many-seed corpus)

PROMPT = (SCRIPTS.parent / "prompts" / "design" / "P1.premise.md").read_text(encoding="utf-8")
SPAN = {"short": 4, "standard": 11, "epic": 19}


class Tables(unittest.TestCase):

    def test_the_rubrics(self):
        by = {r["id"]: r for r in dt.rows("rubrics.yaml#phase_rubric")}
        self.assertIn("four facts", by["rubric_p1_secret_trail"]["question"])
        self.assertIn("any one of its three clues", by["rubric_p1_secret_trail"]["question"])
        self.assertIn("prize", by["rubric_p1_question_concrete"]["question"])
        self.assertIn("goal", by["rubric_p1_question_concrete"]["question"])
        self.assertEqual(by["rubric_p1_legible"]["question"],
                         "Does the player pitch show a threat with a face, ask the campaign's question in this world's words without answering it, "
                         "and give the party something to do in the first session? When the villain is known to the world (known and untouchable, "
                         "or known but no one knows where), does the public premise show its public face, what the world knows it as, and never "
                         "its hidden part?")      # build item 19a: the pitch carries the question; 20a: a known villain's public face
        self.assertFalse([r for r in by.values() if r["phase"] == "P1" and re.search(r"\bthe break\b|\bchooser\b", r["question"])])

    def test_the_small_tables(self):
        self.assertEqual({r["label"] for r in dt.rows("secrets.yaml#god_relation")},
                         {"Deceived", "Impersonated", "Complicit", "Silent", "Opposed"})
        self.assertTrue(dt.roll_header("secrets.yaml#god_relation").get("secret"))
        shapes = dt.rows("signatures.yaml#mechanic_shape")
        self.assertEqual(len(shapes), 6)
        self.assertTrue(all(r.get("bands") for r in shapes))
        self.assertIn("never originates the main thread", json.dumps(dt.load("signatures.yaml"), ensure_ascii=False))

    def test_the_twists_that_name_a_piece_require_it(self):
        by = {r["id"]: r for r in dt.rows("secrets.yaml#twist")}
        self.assertEqual(by["secret_artifact_is_seal"]["requires"], {"any_of": ["prize:new", "prize:remnant"]})
        self.assertEqual(by["secret_artifact_is_alive"]["requires"], {"any_of": ["goal_piece:remnant", "goal_piece:new"]})
        self.assertTrue(by["secret_history_looping"]["requires"]["any_of"])
        self.assertTrue(all(t.startswith("hand_family:") for t in by["secret_monsters_were_made"]["requires"]["any_of"]))

    def test_the_short_names_and_the_hands(self):
        """Build item 18e-2: every contest role the sentence may name reads in five words or fewer; every hand is a
        subject with a number; the greater power's kinds are a secret table, one of them a god."""
        for c in dt.rows("foundation.yaml#contest"):
            for key in c["roles"]:
                self.assertLessEqual(len(fd.role_short(c, key).split()), 5, f"{c['id']}.{key}")
                self.assertIn(fd.role_kind(c, key), ("group", "settlement", "person", "creature"))
        for h in dt.rows("antagonists.yaml#hand"):
            self.assertIn(h["number"], ("singular", "plural"), h["id"])
            self.assertTrue(h["text"]["subject"] and h["text"]["subject"][0].islower(), h["id"])
        self.assertTrue(dt.roll_header("secrets.yaml#greater_power").get("secret"))
        self.assertEqual(len(dt.rows("secrets.yaml#greater_power")), 6)     # build item 22c: the archfey, the elemental prince
        self.assertEqual(sum(1 for r in dt.rows("secrets.yaml#greater_power") if r.get("god")), 1)

    def test_the_door_s_story_fields(self):
        self.assertEqual(set(door.STORY_FIELDS.values()), {"clue_place", "secret_pin"})
        self.assertIn("secret_pin", arb.STORY_SLOTS)
        row = {"type": "premise", "dm_only": {"clues": [{"piece": "remnant"}, {"piece": "lifeline"}], "pinned": {"piece": "scar_new_people"}}}
        self.assertEqual(len(door.story_field_errors("premise_x", row)), 2)


def births(n):
    """The first n births of the shared corpus (build item 18f-1), as (dials, R)."""
    return _corpus.births(n)


def subject_of(R):
    """The hand as the sentence's subject (lower case) and its number; the villain itself by its family's label."""
    hand = dt.row("antagonists.yaml#hand", R.foundation["move"]["hand"])
    if R.foundation["move"].get("state") == "move_unnoticed":       # build item 19a: nobody ties it to anyone
        return ("someone" if "humanoid" in R.threat["hand"]["families"] else "something"), "singular"
    if hand["id"] == "hand_villain_itself":
        return dt.row("antagonists.yaml#villain_family", R.threat["family"])["text"]["name"].lower(), "singular"
    if hand["id"] == "hand_contest_side":            # build item 19a: the side of the contest by its role
        contest = dt.row("foundation.yaml#contest", R.foundation["contests"][0]["id"])
        role = R.foundation["move"]["hand_role"]
        return fd.side_phrase(R.foundation, contest, role).lower(), fd.role_number(contest, role)      # 21a: a generic side by its seat
    return hand["text"]["subject"].lower(), hand["number"]


class ManySeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = births(1500)

    def test_the_spine_sentence(self):
        for d, R in self.runs:
            s = R.foundation["spine_sentence"]
            self.assertTrue(s and s[0].isupper() and s.endswith("."))
            self.assertIn("; now ", s)
            self.assertIn(subject_of(R)[0], s.lower())
            self.assertNotIn("lifeline", s)

    def test_the_sentence_reads_as_d_and_d(self):
        """Build item 18e-2: 300 sentences in active voice: the hand opens it (after "A generation ago," for a
        generation-old move) and its verb agrees with its number; the sides and the prize by their short names."""
        tenses = {r["id"]: r["tense"] for r in dt.rows("foundation.yaml#time")}
        for d, R in self.runs[:300]:
            f = R.foundation
            s = f["spine_sentence"]
            subject, number = subject_of(R)
            lead = "a generation ago, " if f["break"]["time"] == "time_generation_ago" else ""
            body = s.lower()
            self.assertTrue(body.startswith(lead + subject + " "), "the hand is the subject")
            rest = body[len(lead + subject) + 1:]
            if tenses[f["break"]["time"]] != "past":
                self.assertTrue(rest.startswith("are " if number == "plural" else "is "), "the verb agrees with the hand")
            self.assertNotIn(", by ", s, "active voice: the hand is no agent phrase")
            self.assertNotIn("{", s)
            contest = dt.row("foundation.yaml#contest", f["contests"][0]["id"])
            seats = f["layout"]["contests"][0]["seats"]            # build item 21a: a generic side by its noun and seat
            self.assertTrue(s.endswith(f"; now {fd.side_phrase(f, contest, 'a', seats)} and {fd.side_phrase(f, contest, 'b', seats)} fight over "
                                       f"{fd.prize_phrase({**f, 'ruin': f['ruin_source']}, f['layout']['contests'][0])}."))

    def test_the_pin_and_the_mechanic(self):
        gods = 0
        for d, R in self.runs:
            pin = R.identity_secret["secret"]["pin"]
            power = R.identity_secret["secret"]["greater_power"]        # 18e-2: one rule for the twist and the patron
            self.assertEqual(power is not None, R.identity_secret["secret"]["twist"] == "twist_greater_power"
                             or R.threat["goal"]["id"] == "goal_patron_will")
            needs = R.threat["family"] == "family_god" or bool(power and dt.row("secrets.yaml#greater_power", power).get("god"))
            self.assertEqual(pin["god"], needs)
            self.assertEqual(pin["event"], "the move")
            if needs:
                gods += 1
                self.assertIsNotNone(dt.row("secrets.yaml#god_relation", pin["relation"]))
            else:
                self.assertIn(pin["piece"], ("thin_place", "remnant"))
                self.assertTrue(arb.slot_accepts("secret_pin", pin["piece"]))
            self.assertEqual("mechanic" in R.identity, R.by_label["mechanic"]["row_id"] == "yes")
        self.assertGreater(gods, 0)

    def test_a_twist_s_piece_is_there(self):
        for d, R in self.runs:
            t = R.identity_secret["secret"]["twist"]
            main = R.foundation["layout"]["contests"][0]["prize"]["kind"]
            if t == "secret_artifact_is_seal":
                self.assertIn(main, ("new", "remnant"))
            if t == "secret_artifact_is_alive":
                self.assertIn(R.threat["goal"]["piece"], ("remnant", "new"))

    def test_the_twists_floor(self):
        smallest = min(R.pools["secrets.yaml#twist"] for d, R in self.runs if "secrets.yaml#twist" in R.pools)
        self.assertGreaterEqual(smallest, 5)
        type(self).twist_floor = smallest


def run(script, *args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / script), *args], capture_output=True, text=True, env=env, encoding="utf-8")
    if check and proc.returncode != 0:
        raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode})")
    return proc


class Birth(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.used_backup = USED.read_bytes() if USED.is_file() else None
        self.name = f"_test-story18e-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run("designer.py", "new", self.name, "--party-size", "2", "--seed", "STORY-18E", "--lang", "tr", "--scale", "standard")
        run("designer.py", "-c", self.name, "preroll", "--phase", "P1")
        run("designer.py", "-c", self.name, "phase", "P1", "begin", "--json")

    def tearDown(self):
        shutil.rmtree(CAMPAIGNS / self.name, ignore_errors=True)
        if self.used_backup is not None:
            USED.write_bytes(self.used_backup)
        elif USED.is_file():
            USED.unlink()
        self.guard.__exit__(None, None, None)

    def test_the_card(self):
        run("designer.py", "-c", self.name, "phase", "P1", "card")
        card = (CAMPAIGNS / self.name / "design/_approval/P1.card.md").read_text(encoding="utf-8")
        m = dm.load(self.name)
        self.assertLess(card.index("## THE STORY"), card.index("## THE FOUNDATION"), "the spine sentence first")
        self.assertIn(m["foundation"]["spine_sentence"], card)
        self.assertRegex(card, r"the threat: rolled, hidden · hidden facts: [34] of 4 · twist: (yes|no) · stages: 3 × 3 clues")
        self.assertIn("D&D: ✓ villain · ✓ hand · ✓ goal · ✓ weakness · ✓ lair · ✓ start · ✓ families · ✓ stages 3×3 · ✓ breaks bend", card)
        self.assertNotIn("dnd_incomplete", {i["code"] for i in da.gate(self.name, "P1")})

    def test_a_missing_piece_closes_the_gate(self):
        path = CAMPAIGNS / self.name / "design/dm-only/dice-log.json"
        log = json.loads(path.read_text(encoding="utf-8"))
        log["threat"]["lair"] = {"form": None, "where": None}
        path.write_text(json.dumps(log), encoding="utf-8")
        item = next(i for i in da.gate(self.name, "P1") if i["code"] == "dnd_incomplete")
        self.assertIn("lair", item["detail"])
        self.assertEqual(item["ids"], [])

    def test_the_prompt(self):
        begin = run("designer.py", "-c", self.name, "phase", "P1", "begin", "--json")
        text = dpm.render(self.name, "P1.premise")
        for needle in ("spine_sentence", "under `threat`", "the four `facts`", "`stages`", "`pin`", "`identity.mechanic.shape`",
                       "its `phase` and its `hook`", "`dm_only.serves_clue`",       # build item 20a: the frame gives the notes "with the Read tool and never with Bash",
                       "You decide nothing the rolls decide"):
            self.assertIn(needle, text, needle)
        for gone in ("concretise", "the chooser as the person", "archetype row's `cause`", "fell from the sky", "the break's true cause"):
            self.assertNotIn(gone, text, gone)
        self.assertIn("Read every dm-only file with the Read tool, never with Bash", dpm.P1_ROLLS)


if __name__ == "__main__":
    unittest.main()
