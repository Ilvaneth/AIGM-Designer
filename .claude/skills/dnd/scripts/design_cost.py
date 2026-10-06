#!/usr/bin/env python3
"""
design_cost.py — what a phase really cost, from the Workflow run's own agent transcripts (root-cause analysis 1, RC-09).

Every card, report and design_critique_stats.py called the Workflow tool's totalTokens "output tokens"; it is the sum of
each agent's peak context (dry-1: 19.1 M reported, 2.9 M real output, 319 M read back from the cache). This script reads
the run's transcript folder (the Workflow result names it: "Transcript dir: …"), counts each API request once (a request
with a text and a tool block is stored as two records with its usage repeated), and records per role and in total:
agents, requests, output, input, cache writes, cache reads, the peak context.

  design_cost.py -c CAMP record --phase PN --run-dir DIR     record one run on the phase (idempotent per run id); for a
                                                             run that was not merged (a Workflow that returned failed or
                                                             was stopped): `merge --run-dir` records the merged ones
  design_cost.py -c CAMP show [--phase PN]                    print what the manifest holds
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
from design_io import now_iso  # noqa: E402

FIELDS = ("agents", "requests", "output", "input", "cache_write", "cache_read")


def role_of(label: str) -> str:
    """The agent's role from its workflow label (`P5.npc_irn.critic1.loop2`, `P6.skeleton.fix1`, `P7.phase_critic`)."""
    parts = label.split(".")
    tail = ".".join(parts[1:])
    if tail.startswith("phase_critic"):
        return "phase_critic"
    if tail.startswith("wishes_critic"):
        return "wishes_critic"
    if tail.startswith("skeleton"):
        return "skeleton_critic" if ".critic" in tail else "skeleton"
    if re.search(r"\.critic2", "." + tail):
        return "critic2"
    if re.search(r"\.critic1", "." + tail):
        return "critic"
    if re.search(r"\.fix\d", "." + tail):
        return "fix"
    return "writer"


def agent_usage(path: Path) -> dict:
    reqs: dict = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("type") != "assistant":
                continue
            msg = r.get("message") or {}
            usage = msg.get("usage")
            if usage:
                reqs[r.get("requestId") or msg.get("id") or len(reqs)] = usage
    out = {"requests": len(reqs), "output": 0, "input": 0, "cache_write": 0, "cache_read": 0, "peak": 0}
    for u in reqs.values():
        o, i = int(u.get("output_tokens") or 0), int(u.get("input_tokens") or 0)
        cw, cr = int(u.get("cache_creation_input_tokens") or 0), int(u.get("cache_read_input_tokens") or 0)
        out["output"] += o
        out["input"] += i
        out["cache_write"] += cw
        out["cache_read"] += cr
        out["peak"] = max(out["peak"], o + i + cw + cr)
    return out


def run_usage(run_dir: Path) -> dict:
    """{run, by_role: {role: fields}, totals: fields + peak_sum} for one Workflow run's transcript folder."""
    by_role: dict = {}
    peak_sum = 0
    for f in sorted(run_dir.glob("agent-*.jsonl")):
        meta = {}
        m = f.with_name(f.name.replace(".jsonl", ".meta.json"))
        if m.is_file():
            try:
                meta = json.loads(m.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {}
        role = role_of(str(meta.get("description") or ""))
        u = agent_usage(f)
        slot = by_role.setdefault(role, dict.fromkeys(FIELDS, 0))
        slot["agents"] += 1
        for k in FIELDS[1:]:
            slot[k] += u[k]
        peak_sum += u["peak"]
    totals = {k: sum(v[k] for v in by_role.values()) for k in FIELDS}
    totals["peak_sum"] = peak_sum
    return {"run": run_dir.name, "by_role": by_role, "totals": totals}


def record(campaign: str, phase: str, run_dir: str, merged: bool = False) -> int:
    """One run's cost on the phase's ledger. `merged` is set by `designer.py phase PN merge --run-dir`; a run recorded
    by itself is one that was not merged (build item 18f: the test birth's failed Workflow cost 95,155 tokens no ledger
    held), and the report counts it apart."""
    rd = Path(run_dir)
    if not rd.is_dir():
        print(f"design_cost: no transcript folder {run_dir}", file=sys.stderr)
        return 1
    usage = run_usage(rd)
    data = dm.load(campaign)
    ph = data["phases"][phase]
    cost = ph.setdefault("cost", {"runs": {}, "totals": {}})
    cost["runs"][usage["run"]] = dict(usage, at=now_iso(), merged=bool(merged or (cost["runs"].get(usage["run"]) or {}).get("merged")))
    cost["totals"] = {k: sum(r["totals"].get(k, 0) for r in cost["runs"].values()) for k in FIELDS + ("peak_sum",)}
    dm.save(campaign, data, f"design_cost.py record --phase {phase}")
    t = usage["totals"]
    print(f"design_cost: {phase} run {usage['run']}{'' if merged else ' (not merged)'}: {t['agents']} agents, {t['requests']} requests, output {t['output']:,}, "
          f"cache read {t['cache_read']:,} (peak context summed {t['peak_sum']:,})".replace(",", "."))
    return 0


def show(campaign: str, phase: str | None) -> int:
    data = dm.load(campaign)
    for pn, ph in data["phases"].items():
        if phase and pn != phase:
            continue
        t = (ph.get("cost") or {}).get("totals")
        if t:
            print(f"design_cost: {pn}: {t.get('agents', 0)} agents, output {t.get('output', 0):,}, cache read "
                  f"{t.get('cache_read', 0):,}".replace(",", "."))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="a phase's real cost from its Workflow transcripts (RC-09)")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    r = sub.add_parser("record")
    r.add_argument("--phase", required=True)
    r.add_argument("--run-dir", required=True)
    s = sub.add_parser("show")
    s.add_argument("--phase")
    a = ap.parse_args(argv)
    if a.verb == "record":
        return record(a.campaign, a.phase, a.run_dir)
    return show(a.campaign, a.phase)


if __name__ == "__main__":
    sys.exit(main())
