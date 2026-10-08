"""
test_p2_tables.py — build item 22a (docs/p2-build-22.md; the rows as docs/p2-tags.md S1-S6 and the tag pass's rulings
leave them): the new and the deleted rows, the layers, rule 8's `avoid_used`, the approved claims, `home_of` and the
named planes, no P2 hook due at P1, and no table, prompt, template, script or test naming a deleted row.
"""

import re
import sys
import unittest
from pathlib import Path

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_tables as dt  # noqa: E402

SKILL = SCRIPTS.parent
P2_FILES = ("pantheon.yaml", "planes.yaml", "magic.yaml", "history.yaml", "calendar.yaml")
DELETED = ["godsecret_is_dead", "godsecret_is_two_gods", "godsecret_villains_patron", "godsecret_bound", "godsecret_usurper",
           "godsecret_is_the_phenomenon", "godsecret_is_the_land", "dev_secret_holds", "constraint_time", "constraint_place",
           "constraint_price_in_self", "constraint_exhaustion", "constraint_witness", "constraint_none_known",
           "source_the_sleeper", "div_did_not_happen", "div_miracle_was_a_machine", "div_price_was_hidden",
           "year_twelve_months", "year_ten_plus_dead_days", "year_thirteen_moons", "year_eight_months",
           "week_six_day", "week_seven_day", "week_ten_day", "week_five_day"]
NEW = {"pantheon.yaml#type": ["pantheon_animist"], "planes.yaml#baseline": ["baseline_fey_echo", "baseline_shadow_echo", "baseline_beyond"],
       "magic.yaml#constraint": ["constraint_law_and_folk"], "calendar.yaml#underground_count": ["count_light_cycle", "count_great_clock"]}


def p2_rows():
    for name in P2_FILES:
        for sub, rows in dt.all_row_lists(dt.load(name)).items():
            for r in rows:
                yield f"{name}#{sub}", r


class TheRows(unittest.TestCase):

    def test_the_new_rows_and_the_deleted_ones(self):
        for ref, ids in NEW.items():
            have = [r["id"] for r in dt.rows(ref)]
            for rid in ids:
                self.assertIn(rid, have, ref)
        ids = {r["id"] for _, r in p2_rows()}
        self.assertFalse(set(DELETED) & ids)
        self.assertEqual([r["id"] for r in dt.rows("magic.yaml#constraint")],
                         ["constraint_components", "constraint_caste", "constraint_licence", "constraint_echo", "constraint_law_and_folk"])

    def test_nothing_names_a_deleted_row(self):
        names = re.compile(r"\b(" + "|".join(DELETED) + r")\b")
        roots = [SKILL / "data" / "design", SKILL / "scripts", SKILL / "prompts", SKILL / "templates", SKILL / "tests"]
        hits = []
        for root in roots:
            for f in root.rglob("*"):
                if f.suffix not in (".yaml", ".py", ".md", ".json") or f.name in ("test_p2_tables.py", "reviewed.json") or "__pycache__" in f.parts:
                    continue
                if names.search(f.read_text(encoding="utf-8", errors="replace")):
                    hits.append(str(f.relative_to(SKILL)))
        self.assertEqual(hits, [])

    def test_no_p2_hook_is_due_at_p1(self):
        """S0 #7: the hooks due at P1 (sealed before P2 rolls) became `requires`, fits or nothing."""
        for ref, r in p2_rows():
            for h in r.get("hooks") or []:
                self.assertNotEqual(h.get("phase"), "P1", f"{ref} {r['id']}")
        for name in P2_FILES:
            for h in dt.load(name).get("hooks_common") or []:
                self.assertNotEqual(h.get("phase"), "P1", name)

    def test_the_layers(self):
        """S0 #1: the planes P1 names and the climate are stage; the rest of P2's tables are texture."""
        for ref in dt.layered_refs():
            if ref.split("#")[0] in P2_FILES:
                want = "stage" if ref in ("planes.yaml#baseline", "calendar.yaml#climate") else "texture"
                self.assertEqual(dt.layer(ref), want, ref)

    def test_rule_8(self):
        """Which P2 tables avoid other campaigns' rows (the tag pass §7)."""
        unique = {"magic.yaml#source", "magic.yaml#taboo", "history.yaml#age_template"}
        for name in P2_FILES:
            for sub in dt.all_row_lists(dt.load(name)):
                ref = f"{name}#{sub}"
                self.assertEqual(bool(dt.roll_header(ref).get("avoid_used")), ref in unique, ref)

    def test_the_approved_claims(self):
        want = {"pantheon_polytheist": {"gods": "answering"}, "pantheon_dead_gods": {"gods": "dead"},
                "pantheon_silent_gods": {"gods": "silent"}, "pantheon_animist": {"gods": "spirits"},
                "presence_never": {"gods_shown": "never"}, "presence_omens": {"gods_shown": "omens"},
                "presence_clergy_only": {"gods_shown": "ordained"}, "presence_in_places": {"gods_shown": "at_places"},
                "presence_walking": {"gods_shown": "walking"}, "presence_through_phenomenon": {"gods_shown": "through_phenomenon"},
                "constraint_caste": {"casting": "by_caste"}, "constraint_licence": {"casting": "licensed"}, "taboo_none": {"casting": "free"},
                "source_a_dying_thing": {"magic": "running_out"}, "moon_none_stars": {"moon": "none"}, "moon_dark": {"moon": "unseen"},
                "moon_one_thirty": {"moon": "one"}, "moon_two": {"moon": "two"}, "moon_is_a_plane": {"moon": "place"},
                "moon_with_a_face": {"moon": "face"}, "moon_tidal": {"moon": "tidal"}}
        got = {r["id"]: r["claims"] for _, r in p2_rows() if r.get("claims")}
        self.assertEqual(got, want)
        self.assertEqual(dt.row("trope-breaks.yaml", "break_gods_among_mortals")["claims"], {"gods": "among_mortals"})
        self.assertEqual(dt.row("trope-breaks.yaml", "break_casting_forbidden")["claims"], {"casting": "forbidden"})

    def test_the_pairs_on_the_rows(self):
        cw = lambda ref, rid: set(dt.row(ref, rid).get("conflicts_with") or [])  # noqa: E731
        self.assertEqual(cw("pantheon.yaml#type", "pantheon_dead_gods"),
                         {"pantheon_silent_gods", "break_chosen_are_many", "power_god", "family_god"})
        self.assertEqual(cw("pantheon.yaml#presence", "presence_never"), {"break_chosen_are_many"})
        self.assertEqual(cw("pantheon.yaml#presence", "presence_in_places"), {"break_divine_magic_holy_ground"})
        self.assertEqual(cw("magic.yaml#regulator", "regulator_nobody"), {"constraint_licence"})
        self.assertEqual(cw("magic.yaml#taboo", "taboo_healing_for_pay"), {"break_magic_sold"})
        self.assertEqual(cw("calendar.yaml#moon", "moon_none_stars"), {"break_moon_trades", "break_night_is_safe", "weak_vulnerable_time"})
        self.assertEqual(cw("calendar.yaml#moon", "moon_dark"), {"break_night_is_safe", "break_moon_trades"})

    def test_home_of_and_the_named_planes(self):
        fams = {r["id"] for r in dt.rows("antagonists.yaml#villain_family")}
        base = {r["id"]: r for r in dt.rows("planes.yaml#baseline")}
        homes = {}
        for rid, r in base.items():
            for h in r.get("home_of") or []:
                fam = h if isinstance(h, str) else h["family"]
                self.assertIn(fam, fams, rid)
                homes.setdefault(fam, set()).add(rid)
        self.assertEqual(homes["family_devil"], {"baseline_nine_hells"})
        self.assertEqual(homes["family_demon"], {"baseline_ce"})
        self.assertEqual(homes["family_hag_fey"], {"baseline_fey_echo"})
        self.assertEqual(homes["family_undead"], {"baseline_shadow_echo"})
        self.assertEqual(homes["family_from_beyond"], {"baseline_beyond"})
        self.assertNotIn("family_shadow", homes, "a spymaster has no home plane (the tag pass's correction)")
        self.assertEqual({r["tier"] for r in base.values() if r.get("tier") and r["id"] in homes["family_fallen_celestial"]}, {"upper"})
        rules = dt.load("planes.yaml")["rules"]
        sets = set(rules["sets"]) | {"moon"}
        named = rules["named_planes"]
        p1_rows = {"land_thin_place", "target_thin_place", "ruin_celestial_war", "ruin_elven_withdrawal", "ruin_planar_rift",
                   "ruin_planar_invasion", "ruin_devils_bargain", "ruin_demon_gate", "ruin_sleeping_realm", "ruin_star_kingdom",
                   "act_merged_with_plane", "scar_plane_thinned", "break_dreams_are_a_place", "break_moon_trades", "spine_two_worlds"}
        self.assertEqual(set(named), p1_rows)
        for rid, spec in named.items():
            self.assertTrue(dt.ref_of_row(rid), rid)
            for x in spec["fits"]:
                self.assertTrue(x in sets or x in base, (rid, x))

    def test_the_history_amounts_by_scale(self):
        h = {s: dt.scale_row(s)["history"] for s in ("short", "standard", "epic")}
        self.assertEqual((h["short"]["ages"], h["short"]["dated_events"], h["short"]["deep_past_events"], h["short"]["divergences"]), (3, [5, 7], 2, 1))
        self.assertEqual((h["standard"]["ages"], h["standard"]["dated_events"], h["standard"]["deep_past_events"], h["standard"]["divergences"]),
                         ([3, 5], [8, 12], [3, 5], 2))
        self.assertEqual((h["epic"]["ages"], h["epic"]["dated_events"], h["epic"]["deep_past_events"], h["epic"]["divergences"]),
                         ([4, 6], [10, 14], [3, 5], 3))


if __name__ == "__main__":
    unittest.main()
