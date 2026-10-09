#!/usr/bin/env python3
"""
measure_p2_after.py — build item 22e (docs/p2-build-22.md part 22e): the whole-P2 measurement over the shared corpus,
and the measurement after: the tag pass's figure before (measure_p2.py: 91.5 % of 3,000 births held a declared clash,
an override no roll applies or a requires left unmet) taken again on the P2 roller of build 22b-22d.

Over the shared corpus (tests/_corpus.py: 3,000 P1 prerolls in memory), `design_cosmos.roll` runs on a copy of each
birth's context and its P1 records (the corpus births are never changed). Counted:
  - the counts' spread per scale (gods, greater, lesser, powers, great, touched planes), the type and presence spread,
    every domain reached, the evil god held at standard and epic, the divergences per scale;
  - the measurement before's three kinds, on the new records: D the declared pairs (and the climate against the era
    and the palette), O an override no roll applies, Q a requires left unmet;
  - the arbiter's own check: any pair the claims and the rows rule out among the birth's P0-P2 rolls.
Model-free; nothing is written.

    py docs/reports/p2-tags-draft/measure_p2_after.py [n]
"""

import copy
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_p2 as before  # noqa: E402  (its tables: DECLARED, ANCHOR_BY_TIME, NO_OVERFLOW, REGULATOR_OVERRIDES)
import _corpus  # noqa: E402
import design_arbiter as arb  # noqa: E402
import design_cosmos as dc  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402


def main(n: int) -> None:
    births = _corpus.births(n)
    total = len(births)
    counts, causes = Counter(), Counter()
    spread: dict = defaultdict(lambda: defaultdict(Counter))
    types, presence, domains = Counter(), Counter(), Counter()
    evil = Counter()
    for d, R1 in births:
        R = designer.Roller.in_memory(R1.master, d, phase="P2")
        R.ctx = copy.deepcopy(R1.ctx)
        pub, sec = dc.roll(R, d, dc.p1_of(R1))
        sc = d["scale"]
        c = pub["counts"]
        for k in ("gods", "greater", "lesser", "power", "great"):
            spread[sc][k][c[k]] += 1
        spread[sc]["planes"][len(pub["planes"])] += 1
        spread[sc]["divergences"][sum(1 for e in pub["events"] + pub["deep_events"] if e.get("divergence") not in (None, "div_none"))] += 1
        types[pub["type"]] += 1
        presence[pub["presence"]] += 1
        for g in pub["gods"]:
            domains.update(g["domains"])
        if sc in ("standard", "epic"):
            evil["held" if any(g["alignment"] in dc.EVIL for g in pub["gods"]) else "missing"] += 1
        # the measurement before's three kinds, read on the new records
        p2 = {rec["label"]: rec.get("row_id") for rec in R.public}
        have = set(R.ctx.rolled) | set(R.ctx.tokens) | {v for v in p2.values() if v}
        have |= {dt.dial_row(k, v)["id"] for k, v in d.items() if k in dt.DIAL_NAMES and isinstance(v, str) and dt.dial_row(k, v)}
        found = {"D": set(), "O": set(), "Q": set(), "A": set()}
        for label, a, b in before.DECLARED:
            if a in have and b in have:
                found["D"].add(label)
        climate, era = p2.get("climate"), d["era"]
        if climate == "climate_underground" and era != "underground":
            found["D"].add("D12 underground climate outside the underground era")
        if era == "underground" and climate != "climate_underground":
            found["D"].add("D13 the underground era without the underground climate")
        allowed = before.allowed_climates(R1.foundation) - ({"climate_underground"} if era != "underground" else set())
        if era != "underground" and allowed and climate not in allowed:
            found["D"].add("D14 a climate the palette does not allow")
        reg = R.by_label.get("magic_regulator") or {}
        if before.REGULATOR_OVERRIDES & have and reg.get("notation") != "forced":
            found["O"].add("O1 the regulator rolled although a row overrides who")
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
        if p2.get("wild_shape") == "wild_overflow" and before.NO_OVERFLOW & have:
            found["Q"].add("Q3 overflow of a phenomenon that cannot overflow")
        time_row = next((t for t in before.ANCHOR_BY_TIME if t in have), None)
        if time_row and p2.get("start_anchor") not in before.ANCHOR_BY_TIME[time_row]:
            found["Q"].add("Q4 a start anchor against the move's time")
        if arb.conflicting_pairs(list(R.ctx.rolled), tokens=list(R.ctx.tokens), exempt=set(R1.exempt) | set(R.exempt)):
            found["A"].add("A a pair the claims and the rows rule out")
        for k, v in found.items():
            if v:
                counts[k] += 1
            for x in v:
                causes[x] += 1
        if found["D"] or found["O"] or found["Q"] or found["A"]:
            counts["any"] += 1
    pct = lambda x: f"{x:,} ({100 * x / total:.1f} %)"  # noqa: E731
    print(f"births: {total:,}")
    for sc in ("short", "standard", "epic"):
        print(f"{sc}:")
        for k, cnt in spread[sc].items():
            print(f"  {k}: " + ", ".join(f"{v}×{cnt[v]}" for v in sorted(cnt)))
    print("type: " + ", ".join(f"{k} {v}" for k, v in types.most_common()))
    print("presence: " + ", ".join(f"{k} {v}" for k, v in presence.most_common()))
    print(f"domains reached: {len(domains)} of {len(dt.rows('pantheon.yaml#domain_scaffold'))}: " + ", ".join(f"{k} {v}" for k, v in domains.most_common()))
    print(f"the evil god at standard and epic: held {evil['held']}, missing {evil['missing']}")
    print(f"D a declared clash: {pct(counts['D'])}")
    print(f"O an override no roll applies: {pct(counts['O'])}")
    print(f"Q a requires left unmet: {pct(counts['Q'])}")
    print(f"A the arbiter's own check: {pct(counts['A'])}")
    print(f"any: {pct(counts['any'])}")
    for c, x in sorted(causes.items(), key=lambda kv: -kv[1]):
        print(f"  {c}: {pct(x)}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else _corpus.SEEDS)
