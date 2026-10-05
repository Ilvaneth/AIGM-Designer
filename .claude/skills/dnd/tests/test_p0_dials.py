"""
test_p0_dials.py — build item 7b: the P0 dials as the tag review ruled them (docs/p1-tags.md, the "P0 — ..." sections
and section 3). Tone is the three-valued darkness dial and carries four things; scale gives every campaign a touched
plane and names the great gods instead of a church per god; magic sets how strict the regulator is, never who; the
eras lose their economy lists and their attractor hooks, nautical forces the coast and weighs the sea-less spines
down; danger's `standard` is `balanced`; politics loses the trial and the court becomes an audience. A legacy birth
keeps its old dial values; a new birth refuses them.
"""

import itertools
import json
import sys
import unittest

from _campaign import CAMPAIGNS, FIXTURE, SCRIPTS, TestCampaign

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

rows = lambda ref: {r["id"]: r for r in dt.rows(ref)}
SPINE = rows("foundation.yaml#spine")


def every_string(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from every_string(v)
    elif isinstance(node, list):
        for v in node:
            yield from every_string(v)


class Tone(unittest.TestCase):

    def test_three_values_with_the_blank_roll_weights(self):
        tone = dt.rows("dials.yaml#tone")
        self.assertEqual([(r["id"], r["value"], r["label"], r["weight"]) for r in tone],
                         [("tone_bright", "bright", "Bright", 2), ("tone_shadowed", "shadowed", "Shadowed", 3),
                          ("tone_dark", "dark", "Dark", 1)], "English labels like every dial row")
        self.assertFalse(any("tr" in r or "text" in r for r in tone), "the Turkish names went with build item 13a; the label stands")
        self.assertEqual(dt.load("dials.yaml")["tables"]["tone"]["notation"], "d3")

    def test_it_carries_four_things_and_nothing_else(self):
        tone = rows("dials.yaml#tone")
        for r in tone.values():
            self.assertEqual(set(r["effects"]), {"ending_bias", "sides", "majority_pole", "voice"}, r["id"])
        self.assertEqual([tone[t]["effects"]["ending_bias"] for t in ("tone_bright", "tone_shadowed", "tone_dark")],
                         [["win"], ["pyrrhic"], ["pyrrhic", "loss"]])
        self.assertEqual([tone[t]["effects"]["sides"] for t in ("tone_bright", "tone_shadowed", "tone_dark")],
                         ["allies won by deed exist", "mixed", "no faction is clean"])
        self.assertEqual([tone[t]["effects"]["majority_pole"] for t in ("tone_bright", "tone_shadowed", "tone_dark")],
                         ["other", "other", "villain"])
        self.assertEqual([tone[t]["effects"]["voice"] for t in ("tone_bright", "tone_shadowed", "tone_dark")],
                         ["clear, encouraging", "uneasy", "bleak and exact"])

    def test_the_surviving_hooks(self):
        tone = rows("dials.yaml#tone")
        phases = {t: [h["phase"] for h in tone[t]["hooks"]] for t in tone}
        self.assertEqual(phases, {"tone_bright": ["P4", "P7"], "tone_shadowed": ["P6"], "tone_dark": ["P4", "P5", "P7"]})
        text = " ".join(every_string([r["hooks"] for r in tone.values()]))
        self.assertNotIn("deep-past", text)
        self.assertNotIn("most of the world already lives by", text, "majority_pole replaced grimdark's P1 hook")

    def test_the_foundations_tone_weights_moved(self):
        """22 weights: heroic (2 ruins) → bright; horror (2 ruins) and political (15 contests) → the content mix;
        cosmic (3 ruins) deleted."""
        seen = {"tone": [], "horror": [], "politics": []}
        for sub in ("ruin_source", "contest", "spine", "palette", "lifeline"):
            for r in dt.rows(f"foundation.yaml#{sub}"):
                for w in r.get("weight_by") or []:
                    dial = (w["when"] or {}).get("dial") or {}
                    if "tone" in dial:
                        seen["tone"].append((r["id"], dial["tone"]))
                    for mix in ("horror", "politics"):
                        if mix in (dial.get("content_mix") or []):
                            seen[mix].append(r["id"])
        self.assertEqual(sorted(seen["tone"]), [("ruin_age_of_dragons", ["bright"]), ("ruin_giants_land", ["bright"])])
        # the two contests and the sixteenth politics weight came with the general themes (build item 16d); build item
        # 18a retired two contests that carried one (the old craft, the split family): 14
        self.assertEqual(sorted(seen["horror"]), ["contest_coven", "contest_living_dead", "ruin_failed_experiment", "ruin_plague"])
        self.assertEqual(len(seen["politics"]), 14)
        self.assertIn("contest_thieves_guild", seen["politics"])
        ruin = rows("foundation.yaml#ruin_source")
        for rid in ("ruin_celestial_war", "ruin_broken_time", "ruin_star_kingdom"):
            self.assertNotIn("weight_by", ruin[rid], "the cosmic weights are gone")
        ctx = arb.Context(dials={"content_mix": ["politics", "war", "mystery"], "tone": "bright"})
        self.assertEqual(arb.weight_of(rows("foundation.yaml#contest")["contest_old_order_reform"], ctx), 2)
        self.assertEqual(arb.weight_of(ruin["ruin_giants_land"], ctx), 3)

    def test_no_table_names_an_old_tone(self):
        old = ("tone_grimdark", "tone_dark_fantasy", "tone_heroic", "tone_horror", "tone_political", "tone_swashbuckling", "tone_cosmic")
        for name in dt.list_tables():
            text = (dt.tables_dir() / name).read_text(encoding="utf-8")
            for t in old:
                self.assertNotIn(t, text, name)
            self.assertNotRegex(text, r"tone: \[\"?(heroic|horror|political|cosmic|grimdark|swashbuckling)", name)


class Scale(unittest.TestCase):

    def test_a_touched_plane_at_every_scale_and_the_great_gods(self):
        sc = {r["value"]: r for r in dt.rows("scale.yaml")}
        self.assertEqual(sc["short"]["planes_touched"], 1)
        self.assertEqual({k: v["great_gods"] for k, v in sc.items()}, {"short": [0, 1], "standard": [1, 2], "epic": [2, 4]})
        for r in sc.values():
            self.assertNotIn("churches_as_factions", r)
            self.assertIn("the great gods' churches are factions inside the count; the quota's religious faction is the first great god's church",
                          [h["must"] for h in r["hooks"]])
            self.assertLessEqual(r["great_gods"][1], dt.band(r["gods"])[0], "the great gods are some of the gods")
        text = (dt.tables_dir() / "scale.yaml").read_text(encoding="utf-8") + (dt.tables_dir() / "dials.yaml").read_text(encoding="utf-8")
        self.assertNotIn("church faction per god", text)
        self.assertNotIn("church factions per god", text)


class Magic(unittest.TestCase):

    def test_the_dial_sets_how_strict_never_who(self):
        magic = rows("dials.yaml#magic")
        self.assertEqual([magic[m]["effects"]["regulator_strictness"] for m in ("magic_low", "magic_medium", "magic_high")],
                         ["strict", "loose", "free"])
        for r in magic.values():
            self.assertNotIn("regulator", r["effects"])
        hooks = {m: [h["must"] for h in r["hooks"]] for m, r in magic.items()}
        self.assertIn("the regulator P2 rolls has a fracture about the phenomenon", hooks["magic_low"])
        self.assertIn("at least one settlement's ward, lift or bridge runs on magic; it is nobody's property", hooks["magic_high"])
        text = " ".join(every_string(list(magic.values())))
        for word in ("mage guild", "bills", "lamp", "municipal"):
            self.assertNotIn(word, text)


class Era(unittest.TestCase):

    def test_the_lists_and_hooks_that_left(self):
        era = rows("dials.yaml#era")
        for r in era.values():
            self.assertNotIn("economy_bias", r["effects"], r["id"])
        ren = era["era_renaissance"]
        self.assertNotIn("exchange", ren["effects"]["anchor_variants"])
        self.assertIn("printing house", ren["effects"]["anchor_variants"])
        self.assertEqual(ren["effects"]["srd_equipment"], "as printed; books are trade goods")
        self.assertIn("a printing house is a faction asset someone wants", [h["must"] for h in ren["hooks"]])
        self.assertIn("temple", era["era_ancient"]["effects"]["anchor_variants"])
        self.assertNotIn("content_mix_bias", era["era_nautical"]["effects"])
        und = era["era_underground"]
        self.assertEqual(und["effects"]["calendar_note"],
                         "the sun and the moon are known but seldom seen; those below count time by what the deep gives")
        self.assertIn("the calendar names what those below count time by", [h["must"] for h in und["hooks"]])
        text = " ".join(every_string(list(era.values())))
        for word in ("bank", "credit", "exchange", "city-states", "tombs", "bells", "tides", "no sky"):
            self.assertNotIn(word, text)

    def test_nautical_forces_the_coast_and_weighs_the_spines(self):
        self.assertEqual(dt.load("foundation.yaml")["tables"]["palette"]["roll"]["forces_by_dial"]["era"]["nautical"], ["land_coast"])
        triple = {"spine_long_coast", "spine_archipelago", "spine_above_below_sea", "spine_peninsula", "spine_strait_two_continents"}
        plain = {"spine_river_to_sea", "spine_lake_chain", "spine_floating_archipelago"}
        naut, base = arb.Context(dials={"era": "nautical"}), arb.Context(dials={"era": "medieval"})
        for sid, r in SPINE.items():
            ratio = arb.weight_of(r, naut) / arb.weight_of(r, base)
            self.assertEqual(ratio, 3 if sid in triple else (1 if sid in plain else 0.25), sid)
        self.assertEqual(sum(1 for s in SPINE if s not in triple | plain), 22)

    def test_thousands_of_nautical_seeds_hold_every_rule(self):
        combos = list(itertools.product(("short", "standard", "epic"), ("low", "medium", "high")))
        span = {"short": 4, "standard": 11, "epic": 19}
        pal = rows("foundation.yaml#palette")
        cap = {"low": 0, "medium": 1, "high": 2}
        for i in range(2000):
            scale, magic = combos[i % len(combos)]
            d = {"scale": scale, "magic": magic, "era": "nautical", "tone": "shadowed", "content_mix": ["exploration", "mystery", "war"],
                 "level_band": [1, 1 + span[scale]]}
            R = designer.Roller.in_memory(f"NAUT-{i}", d)
            f = fd.build(fd.roll(R, d), d["level_band"])        # an empty pool would raise SystemExit
            self.assertIn("land_coast", f["palette"], R.master)
            self.assertEqual(arb.conflicting_pairs([r["row_id"] for r in R.public if r.get("row_id")]), [])
            self.assertLessEqual(sum(1 for k in f["palette"] if fd.is_capped(pal[k])), cap[magic])
            ends = [v for p, v in f["layout"]["parts"].items() if p.startswith("end_")]
            self.assertEqual(len(ends), len(set(ends)))
            self.assertNotIn("(", " ".join(x["text"] for x in f["rendering"]))


class DangerAndMix(unittest.TestCase):

    def test_standard_is_balanced_and_play_still_reads_the_same_difficulty(self):
        danger = rows("dials.yaml#danger")
        self.assertNotIn("danger_standard", danger)
        self.assertEqual((danger["danger_balanced"]["value"], danger["danger_balanced"]["label"]), ("balanced", "Balanced"))
        self.assertEqual(danger["danger_balanced"]["effects"]["state_difficulty"], "standard")

    def test_politics_and_exploration(self):
        mix = rows("dials.yaml#content_mix")
        self.assertEqual(mix["mix_politics"]["effects"]["node_kinds"], ["audience", "negotiation", "succession", "election"])
        nodes = {n["id"] for n in dt.rows("arc.yaml#node")}
        self.assertIn("node_audience", nodes)
        self.assertFalse({"node_court", "node_trial"} & nodes)
        self.assertIn("one part of the map is unmapped in the player map and named as such in the primer "
                      "(part of a region at short, a region above)", [h["must"] for h in mix["mix_exploration"]["hooks"]])


class LegacyBirths(unittest.TestCase):

    def test_an_old_birth_still_loads_with_its_old_dials(self):
        fixture = json.loads((FIXTURE / "design" / "design.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture["dials"]["tone"], "dark fantasy")
        self.assertTrue(dm.legacy_birth(fixture))
        c = TestCampaign("p0legacy")
        try:
            self.assertEqual(dm.load(c.name)["dials"]["tone"], "dark fantasy")
            self.assertEqual(c.run("design_manifest.py", "status").returncode, 0, "a legacy birth's manifest still reads")
            self.assertEqual(designer.Roller(c.name, "P9", attempt=9).ctx.dials["tone"], "dark fantasy")
        finally:
            c.remove()
        for birth in ("_test-tune-2", "_test-dry-1", "_test-dry-2", "_test-dry-3", "_test-dry-4"):
            path = CAMPAIGNS / birth / "design" / "design.json"
            if path.is_file():
                self.assertIn("dials", dm.load(birth))

    def test_a_new_birth_refuses_the_old_values(self):
        c = TestCampaign("p0new")
        try:
            base = ["init", "--scale", "short", "--magic", "low", "--era", "medieval", "--party-size", "2",
                    "--content-mix", "mystery,horror,exploration"]
            for tone in ("heroic", "dark fantasy", "grimdark", "horror", "political", "swashbuckling", "cosmic"):
                proc = c.run("design_manifest.py", *base, "--tone", tone, "--danger", "gritty")
                self.assertEqual(proc.returncode, 2, tone)
                self.assertIn("is not one of ('bright', 'shadowed', 'dark')", proc.stderr)
            proc = c.run("design_manifest.py", *base, "--tone", "shadowed", "--danger", "standard")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("danger='standard'", proc.stderr)
        finally:
            c.remove()


if __name__ == "__main__":
    unittest.main()
