#!/usr/bin/env python3
"""
design_critique_stats.py — what the critics said and what it cost, across births (slice 1e analysis).

Reads each campaign's design/design.json (phase tokens, wall time, rosters) and the critic returns kept
under design/_staging/<PN>/merged/*.critic<N>[.loopK].json (ids, verdicts, rubric ids, reason codes —
never prose). Answers: which rubrics fail most, whether a fix loop changes the verdict, how often the
second critic disagrees, where the tokens go.

  design_critique_stats.py CAMP [CAMP ...] [--json] [--top 15]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_tables as dt  # noqa: E402
from design_io import design_dir, read_json  # noqa: E402

CRITIC_FILE = re.compile(r"^(?P<stem>.+?)\.critic(?P<order>\d)(?:\.loop(?P<loop>\d+))?\.json$")
PHASES = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "detail")


def returns_of(campaign: str) -> list[dict]:
    """Every critic return on disk, with its stem, critic order and loop."""
    out = []
    staging = design_dir(campaign) / "_staging"
    for phase in PHASES:
        merged = staging / phase / "merged"
        if not merged.is_dir():
            continue
        for p in sorted(merged.glob("*.critic*.json")):
            m = CRITIC_FILE.match(p.name)
            if not m:
                continue
            ret = read_json(p) or {}
            out.append({"campaign": campaign, "phase": phase, "stem": m.group("stem"), "critic": int(m.group("order")),
                        "loop": int(m.group("loop") or 1), "verdict": ret.get("verdict"),
                        "findings": [f for f in (ret.get("findings") or []) if isinstance(f, dict)]})
    return out


def chains(rets: list[dict]) -> dict:
    """(campaign, phase, stem) -> ordered list of (critic, loop, verdict)."""
    out: dict = defaultdict(list)
    for r in sorted(rets, key=lambda r: (r["campaign"], r["phase"], r["stem"], r["critic"], r["loop"])):
        out[(r["campaign"], r["phase"], r["stem"])].append((r["critic"], r["loop"], r["verdict"]))
    return out


def analyse(campaigns: list[str], top: int) -> dict:
    rets = []
    cost = {}
    for c in campaigns:
        rets += returns_of(c)
        m = read_json(design_dir(c) / "design.json") or {}
        for pn, ph in (m.get("phases") or {}).items():
            cost.setdefault(pn, {"wall_s": 0, "tokens": 0, "roster": 0, "campaigns": 0})
            cost[pn]["wall_s"] += int(ph.get("wall_s") or 0)
            cost[pn]["tokens"] += int((ph.get("tokens") or {}).get("out") or 0)
            cost[pn]["roster"] += len(ph.get("roster") or [])
            cost[pn]["campaigns"] += 1
    kinds = {"skeleton": "skeleton", "phase": "phase", "wishes": "wishes"}
    entity_rets = [r for r in rets if r["stem"] not in kinds]
    ch = chains(entity_rets)
    first = Counter()
    final = Counter()
    conv = Counter()          # first fix -> final verdict
    loops_used = Counter()
    c2_disagree = 0
    c2_total = 0
    for key, seq in ch.items():
        c1 = [v for cr, lp, v in seq if cr == 1]
        c2 = [v for cr, lp, v in seq if cr == 2]
        if c1:
            first[c1[0]] += 1
            final[c1[-1]] += 1
            if c1[0] == "fix":
                conv[c1[-1]] += 1
            loops_used[len(c1) - 1] += 1
        if c1 and c2:
            c2_total += 1
            if c2[0] != c1[-1]:
                c2_disagree += 1
    rubric_fail = Counter()
    rubric_seen = Counter()
    reasons = defaultdict(Counter)
    per_phase_rubric_fail = defaultdict(Counter)
    for r in rets:
        for f in r["findings"]:
            rid = str(f.get("rubric_id") or "?")
            rubric_seen[rid] += 1
            if f.get("verdict") in ("fix", "rerun"):
                rubric_fail[rid] += 1
                per_phase_rubric_fail[r["phase"]][rid] += 1
                if f.get("reason_code"):
                    reasons[rid][str(f["reason_code"])] += 1
    phase_level = defaultdict(lambda: Counter())
    for r in rets:
        if r["stem"] in kinds:
            phase_level[(r["stem"], r["phase"])][r["verdict"]] += 1
    rows = {r["id"]: r for r in dt.rows("rubrics.yaml#phase_rubric")} | {r["id"]: r for r in dt.rows("rubrics.yaml#special")}
    top_rubrics = []
    for rid, n in rubric_fail.most_common(top):
        row = rows.get(rid, {})
        top_rubrics.append({"rubric": rid, "fails": n, "seen": rubric_seen[rid], "rate": round(n / rubric_seen[rid], 2) if rubric_seen[rid] else None,
                            "phase": row.get("phase"), "scope": row.get("scope"), "reasons": reasons[rid].most_common(4),
                            "question": (row.get("question") or "")[:110]})
    never_fail = sorted(rid for rid in rows if rubric_seen[rid] >= 5 and rubric_fail[rid] == 0)
    return {
        "campaigns": campaigns, "critic_returns": len(rets), "entities_critiqued": len(ch),
        "first_verdict": dict(first), "final_verdict": dict(final), "fix_converted_to": dict(conv),
        "fix_loops_used": dict(loops_used), "second_critic": {"pairs": c2_total, "disagree": c2_disagree},
        "phase_level": {f"{k[0]}:{k[1]}": dict(v) for k, v in sorted(phase_level.items())},
        "top_rubrics": top_rubrics, "never_failing_rubrics": never_fail,
        "per_phase_top": {p: c.most_common(3) for p, c in sorted(per_phase_rubric_fail.items())},
        "cost": {pn: dict(v, minutes=round(v["wall_s"] / 60), tokens_per_roster_item=round(v["tokens"] / v["roster"]) if v["roster"] else None)
                 for pn, v in cost.items() if v["tokens"]},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="critic verdicts and cost across births")
    ap.add_argument("campaigns", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args(argv)
    r = analyse(a.campaigns, a.top)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"design_critique_stats: {', '.join(r['campaigns'])} — {r['critic_returns']} critic returns over {r['entities_critiqued']} entities")
    print(f"  first verdict {r['first_verdict']} → final {r['final_verdict']}; a first `fix` ended as {r['fix_converted_to']}; loops used {r['fix_loops_used']}")
    sc = r["second_critic"]
    print(f"  second critic: {sc['pairs']} pair(s), disagreed with the first critic's final verdict {sc['disagree']} time(s)")
    print("  phase-level critics: " + "; ".join(f"{k} {v}" for k, v in r["phase_level"].items()))
    print("  rubrics that fail most (fails/seen, rate):")
    for t in r["top_rubrics"]:
        print(f"    {t['rubric']:<38} {t['fails']:>3}/{t['seen']:<3} {t['rate']}  {t['phase'] or '':<4} {t['scope'] or '':<8} {', '.join(f'{k}×{n}' for k, n in t['reasons'])}")
        if t["question"]:
            print(f"      {t['question']}")
    print(f"  rubrics seen ≥5 times that never failed: {', '.join(r['never_failing_rubrics']) or '—'}")
    print("  cost per phase (summed over the campaigns):")
    for pn, v in r["cost"].items():
        print(f"    {pn:<4} {v['minutes']:>5} min {v['tokens']:>12,} tok  roster {v['roster']:>3}  ≈ {v['tokens_per_roster_item'] or 0:,} tok per roster item".replace(",", "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
