#!/usr/bin/env python3
"""
measure_p2.py — the tag pass's measurement before (docs/reports/p2-tags-draft.md, item 7; docs/p2-build-22.md 22a-0).

Over the shared corpus (tests/_corpus.py: 3,000 P1 prerolls in memory), today's `designer.preroll_p2` is run on a copy
of each birth's context (the corpus births are never changed), and each birth is checked for the pairs the draft
declares (D), the overrides no roll applies (O), the requires a roll leaves unmet (Q) and, apart, the candidate pairs
the draft does not recommend declaring (C). Model-free; nothing is written.

    py docs/reports/p2-tags-draft/measure_p2.py [n]
"""

import copy
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TESTS = ROOT / ".claude/skills/dnd/tests"
sys.path.insert(0, str(TESTS))
import _campaign  # noqa: E402,F401  (the suite's own used.json and runtime: nothing touches the project's)
import _corpus  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

# the phenomenon rules that cannot "happen too much" (the draft's proposal for wild_overflow's requires)
NO_OVERFLOW = {"rule_beasts_sense_lies", "rule_roads_lead_where_needed", "rule_night_distances", "rule_true_names",
               "rule_gesture_magic", "rule_seasons_bound_to_a_beast", "rule_land_guards_lifeline", "rule_one_way_magic"}
ANCHOR_BY_TIME = {"time_just_now": {"anchor_after_event"}, "time_unfolding": {"anchor_after_event"},
                  "time_coming": {"anchor_days_before_doom"},
                  "time_generation_ago": {"anchor_festival_eve", "anchor_season_start", "anchor_market_day", "anchor_midwinter"}}
REGULATOR_OVERRIDES = {"break_magic_is_nobility", "break_casting_forbidden", "contest_casters_casterless"}

DECLARED = [  # (label, a, b): a and b are row ids or claim tokens
    ("D1 dead gods × the gods walk", "pantheon_dead_gods", "presence_walking"),
    ("D2 silent gods × omens", "pantheon_silent_gods", "presence_omens"),
    ("D3 silent gods × the gods walk", "pantheon_silent_gods", "presence_walking"),
    ("D4 gods among mortals × dead gods", "break_gods_among_mortals", "pantheon_dead_gods"),
    ("D5 gods among mortals × silent gods", "break_gods_among_mortals", "pantheon_silent_gods"),
    ("D6 casting forbidden × no taboo", "break_casting_forbidden", "taboo_none"),
    ("D7 no moon × the moon trades", "moon_none_stars", "break_moon_trades"),
    ("D8 no moon × night is safe", "moon_none_stars", "break_night_is_safe"),
    ("D9 no moon × a moon-night weakness", "moon_none_stars", "weak_vulnerable_time"),
    ("D10 dark moon × night is safe", "moon_dark", "break_night_is_safe"),
    ("D11 dark moon × the moon trades", "moon_dark", "break_moon_trades"),
    ("D17 holy ground × answers only at its places", "break_divine_magic_holy_ground", "presence_in_places"),
    ("D18 the chosen are many × dead gods", "break_chosen_are_many", "pantheon_dead_gods"),
    ("D18b the chosen are many × never shown", "break_chosen_are_many", "presence_never"),
    ("D19 a god behind the villain × dead gods", "power_god", "pantheon_dead_gods"),
    ("D20 the threat is a god × dead gods", "family_god", "pantheon_dead_gods"),
    ("D21 licence and ledger × nobody regulates", "constraint_licence", "regulator_nobody"),
    ("D22 magic sold like bread × selling healing is taboo", "break_magic_sold", "taboo_healing_for_pay"),
    ("D16 thirteen moons × two moons", "year_thirteen_moons", "moon_two"),
    ("D16 thirteen moons × a dark moon", "year_thirteen_moons", "moon_dark"),
    ("D16 thirteen moons × no moon", "year_thirteen_moons", "moon_none_stars"),
]
CANDIDATES = [
    ("C1 plentiful magic × a dying source", "claim:magic=plentiful", "source_a_dying_thing"),
    ("C3 printed writing × study alone", "claim:writing=printed", "source_study"),
    ("C4 dead gods × omens", "pantheon_dead_gods", "presence_omens"),
    ("C5 dead gods × the phenomenon speaks", "pantheon_dead_gods", "presence_through_phenomenon"),
    ("C5 silent gods × the phenomenon speaks", "pantheon_silent_gods", "presence_through_phenomenon"),
    ("C6 casting forbidden × licence", "break_casting_forbidden", "constraint_licence"),
    ("C8 casting forbidden × loud casting", "break_casting_forbidden", "visibility_loud"),
    ("C9 a caste casts × nobody regulates", "constraint_caste", "regulator_nobody"),
    ("C7 invisible casting × every spell leaves a trace", "visibility_invisible", "constraint_echo"),
]


def allowed_climates(f: dict) -> set:
    kinds = list(f.get("palette") or []) + list(f.get("palette_extra") or [])
    rows = {r["id"]: r for r in dt.rows("foundation.yaml#palette")}
    biomes = {r["id"]: r for r in dt.rows("regions.yaml#biome")}
    out = set()
    for k in kinds:
        for b in (rows.get(k) or {}).get("biomes") or []:
            out |= set((biomes.get(b) or {}).get("climates") or [])
    return out


def main(n: int) -> None:
    counts, causes, cands = Counter(), Counter(), Counter()
    births = _corpus.births(n)
    total = len(births)
    for d, R in births:
        R2 = designer.Roller.in_memory(R.master, d, phase="P2")
        R2.ctx = copy.deepcopy(R.ctx)
        designer.preroll_p2(R2, {"dials": d, "dice_log": list(R.public)})
        p2 = {rec["label"]: rec.get("row_id") for rec in R2.public}
        have = set(R.ctx.rolled) | set(R.ctx.tokens) | {v for v in p2.values() if v}
        have |= {dt.dial_row(k, v)["id"] for k, v in d.items() if k in dt.DIAL_NAMES and isinstance(v, str) and dt.dial_row(k, v)}
        found = {"D": set(), "O": set(), "Q": set()}
        for label, a, b in DECLARED:
            if a in have and b in have:
                found["D"].add(label)
        climate, era = p2.get("climate"), d["era"]
        if climate == "climate_underground" and era != "underground":
            found["D"].add("D12 underground climate outside the underground era")
        if era == "underground" and climate != "climate_underground":
            found["D"].add("D13 the underground era without the underground climate")
        allowed = allowed_climates(R.foundation) - ({"climate_underground"} if era != "underground" else set())
        if era != "underground" and allowed and climate not in allowed:
            found["D"].add("D14 a climate the palette does not allow")
        reg = p2.get("magic_regulator")
        for o in sorted(REGULATOR_OVERRIDES & have):
            found["O"].add(f"O1 the regulator rolled although {o} overrides who")
        if "break_gods_among_mortals" in have and p2.get("pantheon_presence") != "presence_walking":
            found["O"].add("O2 gods among mortals without the walking presence")
        if "break_moon_trades" in have and p2.get("moon") != "moon_is_a_plane":
            found["O"].add("O3 the moon trades without the moon as a place")
        if p2.get("wild_shape") == "wild_dead_god_static" and not ({"pantheon_dead_gods", "ruin_dead_god"} & have):
            found["Q"].add("Q1 dead-god static without dead gods")
        if "user_no_one" in have and "taboo_the_phenomenon_unlicensed" in have:
            found["Q"].add("Q2 an unlicensed-phenomenon taboo when no one uses it")
        if "user_no_one" in have and p2.get("pantheon_presence") == "presence_through_phenomenon":
            found["Q"].add("Q5 the gods speak through a phenomenon no one controls")
        if p2.get("magic_source") == "source_the_phenomenon" and not ({"user_everyone", "user_casters"} & have):
            found["Q"].add("Q6 the phenomenon is the only source, and only some may use it")
        if p2.get("wild_shape") == "wild_overflow" and NO_OVERFLOW & have:
            found["Q"].add("Q3 overflow of a phenomenon that cannot overflow")
        time_row = next((t for t in ANCHOR_BY_TIME if t in have), None)
        if time_row and p2.get("start_anchor") not in ANCHOR_BY_TIME[time_row]:
            found["Q"].add("Q4 a start anchor against the move's time")
        for label, a, b in CANDIDATES:
            if a in have and b in have:
                cands[label] += 1
        if p2.get("wild_shape") not in (None, "wild_no") and "claim:magic=faded" in have:
            cands["C2 faded magic × wild surges"] += 1
        for k in found:
            if found[k]:
                counts[k] += 1
        if found["D"] or found["O"] or found["Q"]:
            counts["any"] += 1
        if found["D"] or found["Q"]:
            counts["D or Q"] += 1
        for k in found:
            for c in found[k]:
                causes[c] += 1
    pct = lambda x: f"{x:,} ({100 * x / total:.1f} %)"  # noqa: E731
    print(f"births: {total:,} (corpus stops on an empty pool: {len(_corpus.errors(n))})")
    print(f"D a declared clash: {pct(counts['D'])}")
    print(f"O an override no roll applies: {pct(counts['O'])}")
    print(f"Q a requires left unmet: {pct(counts['Q'])}")
    print(f"D or Q: {pct(counts['D or Q'])}")
    print(f"D, O or Q: {pct(counts['any'])}")
    print("by cause:")
    for c, x in sorted(causes.items(), key=lambda kv: -kv[1]):
        print(f"  {c}: {pct(x)}")
    print("candidates (not counted above):")
    for c, x in sorted(cands.items()):
        print(f"  {c}: {pct(x)}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else _corpus.SEEDS)
