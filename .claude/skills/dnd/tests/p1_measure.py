"""
p1_measure.py — the whole-P1 measurement (build item 18f; docs/p1-threat-first.md, the findings and their measures),
over the shared many-seed corpus (tests/_corpus.py). A report for the owner and the development tab, not a test: the
rules it reports are asserted by test_layers, test_move, test_threat, test_world_states and test_p1_story.

  py p1_measure.py                        the measures, the move's and the threat's reports, twenty fresh sentences
  py p1_measure.py --seeds 1000           over fewer corpus births
  py p1_measure.py --sentences 20 --tag T only the sentences, from the seeds T-0 … T-19 (default: a fresh tag)
  py p1_measure.py --no-variety           without the threat's variety report (1,000 births per scale of its own)

Secret rows are counted, never named: the report gives the threat's families by count only.
"""

import argparse
import itertools
import os
import sys
import time
from collections import Counter

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import _corpus  # noqa: E402
import design_arbiter as arb  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

SPAN = {"short": 4, "standard": 11, "epic": 19}
WORLD = {r["id"] for r in dt.rows("trope-breaks.yaml") if r.get("joins")}


def pct(n: int, total: int) -> str:
    return f"{100 * n / total:.1f} %" if total else "—"


def measures(runs: list) -> list[str]:
    n = len(runs)
    out = [f"## The measures ({n} corpus births; docs/p1-threat-first.md's findings)"]
    # finding 1: no element had a rank; the lifeline filled story slots
    slot_bad = sum(1 for d, R in runs if arb.slot_errors(fd.slots(R.foundation)))
    life_target = sum(1 for d, R in runs if fd.PIECE_OF_TARGET[R.foundation["break"]["target"]] == "lifeline")
    life_prize = sum(1 for d, R in runs if any(c["prize"]["kind"] == "lifeline" for c in R.foundation["layout"]["contests"]))
    out.append(f"- 1. texture in a story slot: {slot_bad} births; the lifeline as the move's target {pct(life_target, n)}, as a prize "
               f"{pct(life_prize, n)} (before item 18: 17.8 % and 43 %, one or both 52.6 %)")
    # finding 2: the story's heart was a faceless event; now a hand strikes a target on the way to a goal
    hands = Counter(R.foundation["move"]["hand"] or R.threat["hand"]["id"] for d, R in runs)      # 19a: an unnoticed move's hand is secret
    joined = Counter(R.foundation["move"]["goal_join"] for d, R in runs)
    out.append(f"- 2. a move with a hand: {pct(sum(hands.values()), n)} ({len(hands)} of 27 hands); the goal joins the contest by "
               + ", ".join(f"{k} {pct(v, n)}" for k, v in joined.most_common()))
    # finding 5: the villain's motive was a value; now a goal on a piece of the chain, a weakness, a lair
    complete = sum(1 for d, R in runs if R.threat.get("goal") and R.threat.get("weakness") and (R.threat.get("lair") or {}).get("where"))
    out.append(f"- 5. a threat with a goal, a weakness and a lair: {pct(complete, n)}; its families drawn: "
               f"{len(Counter(R.threat['family'] for d, R in runs))} of 19 (rows not named: secret)")
    # finding 4 and the secret: the secret is the threat's hidden half
    stages = sum(1 for d, R in runs if [len(s["clues"]) for s in R.identity_secret["secret"]["stages"]] == [3, 3, 3])
    out.append(f"- 4. the secret's three stages with three clues each: {pct(stages, n)}")
    # finding 6: world states beside an unrelated contest made a second centre; now each is joined
    ws = [b for d, R in runs for b in R.identity["trope_breaks"] if b["id"] in WORLD]
    out.append(f"- 6. world states drawn: {len(ws)} in {sum(1 for d, R in runs if any(b['id'] in WORLD for b in R.identity['trope_breaks']))} "
               f"births; joined: {pct(sum(1 for b in ws if b.get('join')), len(ws))}")
    # finding 8: the palette's size followed the scale, not the spine
    head = dt.roll_header("foundation.yaml#palette")["count_by_spine"]
    spines = fd.rows_by_id("spine")
    by = {}
    for d, R in runs:
        f = R.foundation
        scar = sum(1 for r in R.public if r["label"] == "foundation.palette.scar")   # the scar's and the ruin's kinds come on top (18b)
        by.setdefault((spines[f["spine"]]["breadth"], d["scale"]), []).append(len(f["palette"]) - scar)
    parts, over = [], 0
    for (breadth, scale), counts in sorted(by.items()):
        lo, hi = head[breadth][scale]
        over += sum(1 for c in counts if c > hi)
        parts.append(f"{breadth} {scale} {sum(counts) / len(counts):.2f} (band {lo}-{hi})")
    out.append("- 8. the palette by the spine's breadth (the scar's and the ruin's kinds on top): " + "; ".join(parts)
               + f"; over the band's top {over} ({pct(over, n)}: the forced kinds and the needs alone)")
    # the story sentence (18e-2): every birth has one
    out.append(f"- the story sentence: {pct(sum(1 for d, R in runs if R.foundation.get('spine_sentence')), n)} of births")
    return out


def sentences(count: int, tag: str) -> list[str]:
    """Fresh seeds, the standard scale, mixed dials."""
    combos = list(itertools.product(dt.dial_values("magic"), dt.dial_values("era"), dt.dial_values("tone")))
    mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
    out = [f"## Twenty spine sentences (standard scale, mixed dials, seeds {tag}-0 … {tag}-{count - 1})"]
    for i in range(count):
        magic, era, tone = combos[(i * 7) % len(combos)]
        d = {"scale": "standard", "magic": magic, "era": era, "tone": tone, "content_mix": list(mixes[(i * 5) % len(mixes)]),
             "party_size": 4, "level_band": [1, 1 + SPAN["standard"]]}
        R = designer.Roller.in_memory(f"{tag}-{i}", d)
        designer.preroll_p1(R, {"dials": d})
        out.append(f"{i + 1:2}. {R.foundation['spine_sentence']}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the whole-P1 measurement")
    ap.add_argument("--seeds", type=int, default=_corpus.SEEDS)
    ap.add_argument("--sentences", type=int, default=20)
    ap.add_argument("--tag", default=f"FRESH-{time.strftime('%Y%m%d%H%M')}-{os.getpid()}")
    ap.add_argument("--no-variety", action="store_true")
    ap.add_argument("--only-sentences", action="store_true")
    a = ap.parse_args(argv)
    lines = sentences(a.sentences, a.tag) + [""]
    if not a.only_sentences:
        runs = _corpus.births(a.seeds)
        lines += measures(runs) + [""]
        import test_move
        lines += ["## The move (test_move --report, on the corpus)", test_move.report(), ""]
        if not a.no_variety:
            import test_threat
            lines += ["## The threat's variety (test_threat --report: its own births, the three-birth wait)", test_threat.report(), ""]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
