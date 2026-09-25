#!/usr/bin/env python3
"""
design_manifest.py — the single writer of design/design.json, the birth manifest.

Plan item 19.4-19.6, 19.9, errata 24.2 #16, 24.6 #6; docs/schemas/design-manifest.md.

Disk is truth, the manifest is the index, the Workflow journal is an
accelerator: `reconcile` rebuilds every entity's status from the staging
fragments and the canonical registry before every run, and `pending` is the
roster minus what disk already proves merged.

CLI (all verbs take -c CAMP):
  init      --scale S --tone T --magic M --era E --danger D --party-size N --start-level N
            --content-mix a,b,c [--must ...] [--must-not ...] [--lang tr] [--seed SEED]
            [--concurrency 8] [--economy] [--fixture]
  reconcile                                  rebuild statuses from disk; exit 0
  pending   --phase PN [--json]              roster minus ≥merged, each with its read budget
  mark      --phase PN [--status S] [--roster a,b,c] [--skeleton S] [--started] [--finished]
            [--entity ID --status S [--attempt N] [--agent L] [--error TEXT] [--file F] [--stage-file F]]
            [--validator-errors N --validator-warnings N] [--direction TEXT] [--workflow-run ID]
  approve   --phase PN --card FILE --commit SHA [--round TEXT --scope fact|entity|phase|direction]
  stale     --from PN --reason TEXT           later phases become stale
  tokens    --phase PN --out N [--in N] [--cache-read N] [--model M] [--wall N]
  roll      --record JSON [--secret]          append a dice-log record (called by design_dice.py)
  ask       --question TEXT --answer A --agent L
  detail-log --id ID --day N --trigger T [--snapshot F] [--commit SHA]
  revision  --scope S --reason TEXT --affected N [--phase PN] [--commit SHA]
  set-mode  birth|play
  status    [--json]

Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import string
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_io import (campaign_dir, design_dir, dm_only_dir, is_container, is_fragment, is_stub,  # noqa: E402
                       now_iso, read_json, sha256_file, stamp_meta, write_json_atomic)
from design_tables import DIAL_NAMES, arc_shape, dial_values  # noqa: E402

PHASES = tuple(f"P{i}" for i in range(10))
PHASE_STATUSES = ("pending", "prerolled", "running", "generated", "merged", "validated", "critiqued",
                  "awaiting_approval", "approved", "partial", "failed", "stale", "needs-check")
ENTITY_STATUSES = ("pending", "staged", "merged", "validated", "critiqued", "failed")
SKELETON_PHASES = ("P3", "P4", "P5", "P6", "P7")     # the phases a skeleton agent opens (design_prompts.PROMPT_BY_PHASE)
ENTITY_RANK = {s: i for i, s in enumerate(("pending", "failed", "staged", "merged", "validated", "critiqued"))}
SCOPES = ("fact", "entity", "phase", "direction")
ANSWERS = ("evet", "hayır", "spoiler vermeden cevaplanamaz")

# Item 2's dial values and the arc shape come from data/design/dials.yaml and scale.yaml (slice 1b).
DIALS = {dial: dial_values(dial) for dial in DIAL_NAMES}
ARC_SHAPE = {scale: arc_shape(scale) for scale in DIALS["scale"]}   # acts, chapters, level-band span
DESIGNER_VERSION = "dnd 3.0.0-dev"


# ── store ─────────────────────────────────────────────────────────────────────

def manifest_path(campaign: str) -> Path:
    return design_dir(campaign) / "design.json"


def load(campaign: str) -> dict:
    data = read_json(manifest_path(campaign))
    if data is None:
        raise SystemExit(f"design_manifest: no manifest for {campaign}; run init first")
    return data


def save(campaign: str, data: dict, written_by: str) -> None:
    stamp_meta(data, campaign, written_by)
    write_json_atomic(manifest_path(campaign), data)


def empty_phase() -> dict:
    return {"status": "pending", "attempt": 0, "workflow_run_id": None, "started": None, "finished": None,
            "wall_s": 0, "roster": [], "skeleton": {"status": "pending", "agent": None},
            "critique": {"phase_loops": 0, "verdicts": [], "entity_loops_total": 0},
            "validator": {"at": None, "errors": None, "warnings": None},
            "approval": {"rounds": [], "approved_at": None, "card_sha256": None, "registry_sha256": None,
                         "commit": None},
            "directions": [], "tokens": {"in": 0, "out": 0, "cache_read": 0, "by_model": {}},
            "stale_reason": None}


# ── init ──────────────────────────────────────────────────────────────────────

def arc_skeleton(scale: str, start_level: int) -> list[dict]:
    """Chapter ids, acts and level bands derived by script, never generated (item 19.2)."""
    acts, chapters, span = ARC_SHAPE[scale]
    top = start_level + span
    per_act = [chapters // acts + (1 if i < chapters % acts else 0) for i in range(acts)]
    out, lo, n = [], start_level, 1
    for act, count in enumerate(per_act, 1):
        for _ in range(count):
            hi = max(lo, min(top, start_level + round(span * n / chapters)))
            out.append({"chapter": f"chapter_{n}", "act": act, "level_band": [lo, hi], "beats": []})
            lo, n = hi, n + 1
    out[-1]["level_band"][1] = top
    return out


def git_root(path: Path) -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(path), capture_output=True,
                             text=True, check=True)
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def new_seed(campaign: str) -> str:
    tag = "".join(ch for ch in campaign.upper() if ch.isalnum())[:2] or "CD"
    return f"{tag}-{''.join(random.choice(string.hexdigits.lower()) for _ in range(8))}"


def init(campaign: str, a) -> int:
    for dial in ("scale", "tone", "magic", "era", "danger"):
        value = getattr(a, dial)
        if value not in DIALS[dial]:
            print(f"design_manifest: {dial}={value!r} is not one of {DIALS[dial]}", file=sys.stderr)
            return 2
    mix = [m.strip() for m in a.content_mix.split(",") if m.strip()]
    if len(mix) != 3 or any(m not in DIALS["content_mix"] for m in mix) or len(set(mix)) != 3:
        print(f"design_manifest: content-mix needs three distinct entries from {DIALS['content_mix']}",
              file=sys.stderr)
        return 2
    if not 1 <= a.party_size <= 6 or not 1 <= a.start_level <= 20:
        print("design_manifest: party-size 1-6, start-level 1-20", file=sys.stderr)
        return 2
    if manifest_path(campaign).exists():
        print(f"design_manifest: {manifest_path(campaign)} exists; refusing to overwrite", file=sys.stderr)
        return 1

    for sub in ("dm-only/_snapshots", "_staging", "_approval", "npcs", "sites", "factions", "regions",
                "settlements", "chapters", "threads", "dm-only/npcs", "dm-only/sites", "dm-only/factions",
                "dm-only/regions", "dm-only/settlements", "dm-only/chapters", "dm-only/threads"):
        (design_dir(campaign) / sub).mkdir(parents=True, exist_ok=True)
    (campaign_dir(campaign) / "characters").mkdir(parents=True, exist_ok=True)

    span = ARC_SHAPE[a.scale][2]
    data = {
        "_meta": {"schema_version": 1, "campaign": campaign, "fixture": bool(a.fixture),
                  "designer_version": DESIGNER_VERSION, "ruleset": "2014", "lang": a.lang, "mode": "birth",
                  "git_root": git_root(campaign_dir(campaign)), "created": now_iso()},
        "dials": {"scale": a.scale, "tone": a.tone, "magic": a.magic, "era": a.era, "danger": a.danger,
                  "party_size": a.party_size, "start_level": a.start_level,
                  "level_band": [a.start_level, a.start_level + span], "content_mix": mix,
                  "wishes": {"must": a.must or [], "must_not": a.must_not or []}, "lang": a.lang,
                  "concurrency": a.concurrency, "economy": bool(a.economy)},
        "seed": {"master": a.seed or new_seed(campaign),
                 "derivation": "random.Random(f'{master}:{phase}:{table}:{label}')"},
        "arc_skeleton": arc_skeleton(a.scale, a.start_level),
        "dice_log": [],
        "dice_log_secret": {"file": "dm-only/dice-log.json", "count": 0, "labels": []},
        "phases": {p: empty_phase() for p in PHASES},
        "entities": {},
        "seeded": [],
        "detail_log": [],
        "revision_log": [],
        "ask_log": [],
        "totals": {"tokens_in": 0, "tokens_out": 0, "cache_read": 0, "wall_s": 0, "agents": 0},
        "validator_last": {"at": None, "errors": None, "warnings": None},
    }
    save(campaign, data, "design_manifest.py init")
    print(f"design_manifest: initialised {campaign} — scale {a.scale}, seed {data['seed']['master']}, "
          f"{len(data['arc_skeleton'])} chapters")
    return 0


# ── reconcile / pending ───────────────────────────────────────────────────────

def reconcile(campaign: str, quiet: bool = False) -> dict:
    data = load(campaign)
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    staging = design_dir(campaign) / "_staging"
    seen: dict[str, tuple[str, str, int]] = {}      # id -> (status, stage_file, attempt)
    if staging.is_dir():
        for phase_dir in sorted(p for p in staging.iterdir() if p.is_dir() and p.name in PHASES):
            for frag in sorted(phase_dir.glob("*.json")):
                if not is_fragment(frag):
                    continue
                info = read_json(frag) or {}
                if info.get("id"):
                    seen[info["id"]] = ("staged", rel(campaign, frag), int(info.get("attempt") or 1))
            merged = phase_dir / "merged"
            if merged.is_dir():
                for frag in sorted(merged.glob("*.json")):
                    if not is_fragment(frag):
                        continue
                    info = read_json(frag) or {}
                    if info.get("id") and seen.get(info["id"], ("",))[0] == "staged":
                        continue        # a newer fragment waits in the staging root: it is the truth (birth 2)
                    if info.get("id"):
                        # a container (document / batch) is merged once its file moved here; a stub row
                        # in the registry is a reservation, not a merged entity (tuning birth 1)
                        if is_container(info):
                            status = "merged"
                        elif info["id"] in canonical:
                            status = "pending" if is_stub(canonical[info["id"]]) else "merged"
                        else:
                            status = "staged"
                        seen[info["id"]] = (status, rel(campaign, frag), int(info.get("attempt") or 1))
    changed = 0
    for eid, row in data["entities"].items():
        recorded = row.get("status", "pending")
        # a revise round marked the entity for a rerun: disk evidence older than that attempt does not count
        if row.get("rerun"):
            fresh = eid in seen and seen[eid][2] >= int(row.get("attempt") or 0)
            if not fresh:
                if recorded != "pending":
                    row["status"] = "pending"
                    changed += 1
                continue
            row.pop("rerun", None)
        if eid in seen:
            disk, stage_file, attempt = seen[eid]
            row["stage_file"] = stage_file
            row["attempt"] = max(int(row.get("attempt") or 0), attempt)
            if disk == "staged":
                new = "staged"                       # disk proves less than the record: downgrade
            elif disk == "pending":
                new = "failed" if recorded == "failed" else "pending"   # a stub awaiting its filler
            else:
                new = recorded if ENTITY_RANK.get(recorded, 0) >= ENTITY_RANK["merged"] else "merged"
        elif eid in canonical and not is_stub(canonical[eid]):
            new = recorded if ENTITY_RANK.get(recorded, 0) >= ENTITY_RANK["merged"] else "merged"
        else:
            new = "failed" if recorded == "failed" else "pending"
        if new != recorded:
            row["status"] = new
            changed += 1
    for eid, (disk, stage_file, attempt) in seen.items():
        if eid not in data["entities"]:
            phase = Path(stage_file).parts[2] if len(Path(stage_file).parts) > 2 else None
            data["entities"][eid] = {"phase": phase, "status": disk, "file": canonical.get(eid, {}).get("file"),
                                     "stage_file": stage_file, "attempt": attempt, "critique_loops": 0,
                                     "last_error": None, "agent": None}
            changed += 1
    for pn, ph in data["phases"].items():
        roster = ph.get("roster") or []
        if not roster or ph["status"] == "approved":
            continue        # an approved phase is frozen; only `rerun` reopens it (tuning birth 1)
        statuses = [data["entities"].get(e, {}).get("status", "pending") for e in roster]
        done = all(ENTITY_RANK.get(s, 0) >= ENTITY_RANK["merged"] for s in statuses)
        if done and ph["status"] in ("running", "generated", "partial"):
            ph["status"] = "merged"
        elif not done and ph["status"] in ("merged", "validated", "critiqued", "awaiting_approval", "approved"):
            ph["status"] = "partial"        # disk shows less than the record claims
        elif not done and any(ENTITY_RANK.get(s, 0) >= ENTITY_RANK["merged"] for s in statuses) \
                and ph["status"] in ("running", "generated"):
            ph["status"] = "partial"
    save(campaign, data, "design_manifest.py reconcile")
    if not quiet:
        print(f"design_manifest: reconciled, {changed} entity status(es) changed from disk")
    return data


def rel(campaign: str, path: Path) -> str:
    return path.resolve().relative_to(campaign_dir(campaign).resolve()).as_posix()


def read_budget(campaign: str, canonical: dict, eid: str, hops: int = 2) -> list[str]:
    """Campaign-relative paths an agent may read for `eid`: its own files and those within `hops` refs (the agent
    runs in the campaign dir; birth 2's begin JSON mixed absolute and relative forms of the same file)."""
    root = campaign_dir(campaign)
    frontier, seen = {eid}, {eid}
    for _ in range(hops):
        nxt = set()
        for cur in frontier:
            for ref in canonical.get(cur, {}).get("refs", []):
                if ref not in seen:
                    seen.add(ref)
                    nxt.add(ref)
        frontier = nxt
    files: list[str] = []
    for other in sorted(seen, key=lambda x: (x != eid, x)):
        f = canonical.get(other, {}).get("file")
        if f and (root / f).is_file():
            files.append(f)
            mirror = root / "design" / "dm-only" / Path(f).relative_to("design") if f.startswith("design/") and not f.startswith("design/dm-only/") else None
            if mirror and mirror.is_file():
                files.append(rel(campaign, mirror))
    return files


def pending(campaign: str, phase: str, as_json: bool) -> int:
    data = reconcile(campaign, quiet=True)
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    ph = data["phases"].get(phase)
    if ph is None:
        print(f"design_manifest: unknown phase {phase}", file=sys.stderr)
        return 2
    rows = []
    for eid in ph.get("roster") or []:
        row = data["entities"].get(eid, {"status": "pending", "attempt": 0})
        if ENTITY_RANK.get(row.get("status", "pending"), 0) >= ENTITY_RANK["merged"]:
            continue
        rows.append({"id": eid, "status": row.get("status", "pending"), "attempt": int(row.get("attempt") or 0),
                     "last_error": row.get("last_error"), "files": read_budget(campaign, canonical, eid)})
    out = {"campaign": campaign, "phase": phase, "attempt": ph.get("attempt", 0),
           "skeleton": ph.get("skeleton", {}).get("status"), "directions": ph.get("directions", []),
           "seed": data["seed"]["master"], "entities": rows}
    if as_json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"design_manifest: {phase} attempt {out['attempt']}, skeleton {out['skeleton']}, "
              f"{len(rows)} pending of {len(ph.get('roster') or [])}")
        for r in rows:
            print(f"  {r['id']:<28} {r['status']:<8} attempt {r['attempt']}  files {len(r['files'])}")
    return 0


# ── mark / approve / stale / tokens ──────────────────────────────────────────

def mark(campaign: str, a) -> int:
    data = load(campaign)
    ph = data["phases"].get(a.phase)
    if ph is None:
        print(f"design_manifest: unknown phase {a.phase}", file=sys.stderr)
        return 2
    if a.entity:
        if a.status and a.status not in ENTITY_STATUSES:
            print(f"design_manifest: entity status must be one of {ENTITY_STATUSES}", file=sys.stderr)
            return 2
        row = data["entities"].setdefault(a.entity, {"phase": a.phase, "status": "pending", "file": None,
                                                     "stage_file": None, "attempt": 0, "critique_loops": 0,
                                                     "last_error": None, "agent": None})
        if a.status:
            row["status"] = a.status
        if a.attempt is not None:
            row["attempt"] = a.attempt
        if a.agent:
            row["agent"] = a.agent
        if a.error is not None:
            row["last_error"] = a.error or None
        if a.file:
            row["file"] = a.file
        if a.stage_file:
            row["stage_file"] = a.stage_file
        if a.critique_loop:
            row["critique_loops"] = int(row.get("critique_loops") or 0) + 1
        if a.entity not in (ph.get("roster") or []):
            ph.setdefault("roster", []).append(a.entity)
    else:
        if a.status:
            if a.status not in PHASE_STATUSES:
                print(f"design_manifest: phase status must be one of {PHASE_STATUSES}", file=sys.stderr)
                return 2
            ph["status"] = a.status
            if a.status == "running":
                ph["attempt"] = int(ph.get("attempt") or 0) + 1
                ph["started"] = now_iso()
                ph["finished"] = None
        if a.roster:
            ph["roster"] = [r.strip() for r in a.roster.split(",") if r.strip()]
            for eid in ph["roster"]:
                data["entities"].setdefault(eid, {"phase": a.phase, "status": "pending", "file": None,
                                                  "stage_file": None, "attempt": 0, "critique_loops": 0,
                                                  "last_error": None, "agent": None})
        if a.skeleton:
            ph["skeleton"]["status"] = a.skeleton
            if a.agent:
                ph["skeleton"]["agent"] = a.agent
        if a.workflow_run:
            ph["workflow_run_id"] = a.workflow_run
        if a.finished:
            ph["finished"] = now_iso()
        if a.validator_errors is not None:
            ph["validator"] = {"at": now_iso(), "errors": a.validator_errors, "warnings": a.validator_warnings or 0}
            data["validator_last"] = dict(ph["validator"])
        if a.direction:
            ph["directions"].append(a.direction)
        if a.critique_verdict:
            ph["critique"]["verdicts"].append(a.critique_verdict)
            ph["critique"]["phase_loops"] = len(ph["critique"]["verdicts"])
    save(campaign, data, f"design_manifest.py mark --phase {a.phase}")
    return 0


def approve(campaign: str, a) -> int:
    data = load(campaign)
    ph = data["phases"].get(a.phase)
    if ph is None:
        return 2
    if a.round:
        if len(ph["approval"]["rounds"]) >= 3:
            print("design_manifest: three correction rounds already spent; approve as-is or rerun the phase",
                  file=sys.stderr)
            return 1
        ph["approval"]["rounds"].append({"correction": a.round, "scope": a.scope or "fact",
                                         "affected_files": a.affected or 0, "applied": True, "at": now_iso()})
        save(campaign, data, f"design_manifest.py approve --phase {a.phase} (round)")
        print(f"design_manifest: {a.phase} correction round {len(ph['approval']['rounds'])} recorded")
        return 0
    failed = [e for e in ph.get("roster") or [] if data["entities"].get(e, {}).get("status") == "failed"]
    if failed:
        print(f"design_manifest: {a.phase} has failed entities ({', '.join(failed)}); rerun the pending list "
              "or drop them via revise before approving", file=sys.stderr)
        return 1
    incomplete = [e for e in ph.get("roster") or []
                  if ENTITY_RANK.get(data["entities"].get(e, {}).get("status", "pending"), 0) < ENTITY_RANK["merged"]]
    skeleton_pending = a.phase in SKELETON_PHASES and (ph.get("skeleton") or {}).get("status") == "pending"
    if (incomplete or skeleton_pending) and not getattr(a, "force", False):
        what = (["the skeleton"] if skeleton_pending else []) + incomplete
        print(f"design_manifest: {a.phase} is not complete ({', '.join(what)} not merged); run `phase {a.phase} begin --json` "
              "and the fan-out again, drop the item, or approve --force", file=sys.stderr)
        return 1
    card = Path(a.card)
    if not card.is_file():
        print(f"design_manifest: card {card} not found", file=sys.stderr)
        return 1
    proj = design_dir(campaign) / "entities.json"
    ph["approval"].update({"approved_at": now_iso(), "card_sha256": sha256_file(card),
                           "registry_sha256": sha256_file(proj) if proj.is_file() else None,
                           "commit": a.commit})
    ph["status"] = "approved"
    ph["finished"] = ph.get("finished") or now_iso()
    if not ph.get("wall_s") and ph.get("started"):
        try:
            from datetime import datetime
            t0 = datetime.fromisoformat(str(ph["started"]).replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(ph["finished"].replace("Z", "+00:00"))
            ph["wall_s"] = max(0, int((t1 - t0).total_seconds()))
        except ValueError:
            pass
    save(campaign, data, f"design_manifest.py approve --phase {a.phase}")
    print(f"design_manifest: {a.phase} approved (card {ph['approval']['card_sha256'][:12]}…, commit {a.commit})")
    return 0


def stale(campaign: str, a) -> int:
    data = load(campaign)
    if a.from_phase not in PHASES:
        return 2
    n = 0
    for pn in PHASES[PHASES.index(a.from_phase) + 1:]:
        ph = data["phases"][pn]
        if ph["status"] != "pending":
            ph["status"] = "stale" if data["_meta"].get("mode") == "birth" else "needs-check"
            ph["stale_reason"] = a.reason
            n += 1
    save(campaign, data, f"design_manifest.py stale --from {a.from_phase}")
    print(f"design_manifest: {n} phase(s) after {a.from_phase} marked "
          f"{'stale' if data['_meta'].get('mode') == 'birth' else 'needs-check'}")
    return 0


def tokens(campaign: str, a) -> int:
    data = load(campaign)
    ph = data["phases"].get(a.phase)
    if ph is None:
        return 2
    t = ph["tokens"]
    t["in"] += a.tokens_in or 0
    t["out"] += a.out
    t["cache_read"] += a.cache_read or 0
    if a.model:
        m = t["by_model"].setdefault(a.model, {"in": 0, "out": 0})
        m["in"] += a.tokens_in or 0
        m["out"] += a.out
    ph["wall_s"] = int(ph.get("wall_s") or 0) + (a.wall or 0)
    tot = data["totals"]
    tot["tokens_in"] += a.tokens_in or 0
    tot["tokens_out"] += a.out
    tot["cache_read"] += a.cache_read or 0
    tot["wall_s"] += a.wall or 0
    tot["agents"] += a.agents or 0
    save(campaign, data, f"design_manifest.py tokens --phase {a.phase}")
    return 0


# ── logs ──────────────────────────────────────────────────────────────────────

def append_roll(campaign: str, record: dict, secret: bool = False) -> None:
    """Public rolls go to design.json.dice_log; secret ones to dm-only/dice-log.json (labels only here)."""
    data = load(campaign)
    if secret:
        path = dm_only_dir(campaign) / "dice-log.json"
        log = read_json(path) or {"_meta": {"schema_version": 1, "campaign": campaign}, "rolls": []}
        log["rolls"].append(record)
        stamp_meta(log, campaign, "design_dice.py (secret)")
        write_json_atomic(path, log)
        dls = data["dice_log_secret"]
        dls["count"] = len(log["rolls"])
        if record.get("label") not in dls["labels"]:
            dls["labels"].append(record.get("label"))
    else:
        data["dice_log"].append(record)
    save(campaign, data, "design_manifest.py roll")


def mark_seeded(campaign: str, keys: list[str]) -> int:
    """Append idempotency-ledger keys (`<store>:<id>`); returns how many were new."""
    data = load(campaign)
    new = [k for k in keys if k and k not in data["seeded"]]
    data["seeded"].extend(new)
    if new:
        save(campaign, data, "design_manifest.py seeded")
    return len(new)


def ask(campaign: str, a) -> int:
    if a.answer not in ANSWERS:
        print(f"design_manifest: answer must be one of {ANSWERS}", file=sys.stderr)
        return 2
    data = load(campaign)
    data["ask_log"].append({"at": now_iso(), "question_tr": a.question, "answer": a.answer, "agent": a.agent})
    save(campaign, data, "design_manifest.py ask")
    return 0


def detail_log(campaign: str, a) -> int:
    data = load(campaign)
    data["detail_log"].append({"id": a.id, "at": now_iso(), "day": a.day, "trigger": a.trigger,
                               "snapshot": a.snapshot, "commit": a.commit})
    save(campaign, data, "design_manifest.py detail-log")
    return 0


def revision(campaign: str, a) -> int:
    if a.scope not in SCOPES:
        return 2
    data = load(campaign)
    entry = {"at": now_iso(), "scope": a.scope, "phase": a.phase, "reason": a.reason,
             "affected": a.affected, "commit": a.commit}
    data["revision_log"].append(entry)
    log_id = f"rev_{len(data['revision_log']):04d}"
    entry["id"] = log_id
    save(campaign, data, "design_manifest.py revision")
    print(log_id)
    return 0


def set_mode(campaign: str, mode: str) -> int:
    if mode not in ("birth", "play"):
        return 2
    data = load(campaign)
    if mode == "play":
        unapproved = [p for p in PHASES[:9] if data["phases"][p]["status"] != "approved"]
        if unapproved:
            print(f"design_manifest: cannot enter play mode, unapproved phases: {', '.join(unapproved)}",
                  file=sys.stderr)
            return 1
    data["_meta"]["mode"] = mode
    save(campaign, data, f"design_manifest.py set-mode {mode}")
    print(f"design_manifest: mode {mode}")
    return 0


def status(campaign: str, as_json: bool) -> int:
    data = load(campaign)
    if as_json:
        summary = {pn: {"status": ph["status"], "attempt": ph["attempt"], "roster": len(ph.get("roster") or [])}
                   for pn, ph in data["phases"].items()}
        print(json.dumps({"mode": data["_meta"].get("mode"), "seed": data["seed"]["master"],
                          "phases": summary, "totals": data["totals"], "validator_last": data["validator_last"]},
                         indent=2, ensure_ascii=False))
        return 0
    print(f"design_manifest: {campaign} — mode {data['_meta'].get('mode')}, scale {data['dials']['scale']}, "
          f"seed {data['seed']['master']}")
    for pn, ph in data["phases"].items():
        roster = ph.get("roster") or []
        counts: dict = {}
        for e in roster:
            s = data["entities"].get(e, {}).get("status", "pending")
            counts[s] = counts.get(s, 0) + 1
        detail = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) if counts else "—"
        print(f"  {pn}  {ph['status']:<18} attempt {ph['attempt']}  {detail}"
              + (f"  ({ph['stale_reason']})" if ph.get("stale_reason") else ""))
    v = data["validator_last"]
    print(f"  validator: {v.get('errors')} errors, {v.get('warnings')} warnings at {v.get('at')}")
    t = data["totals"]
    print(f"  tokens out {t['tokens_out']}, agents {t['agents']}, wall {t['wall_s']} s, "
          f"public rolls {len(data['dice_log'])}, secret rolls {data['dice_log_secret']['count']}")
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Single writer of design/design.json")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init")
    for dial in ("scale", "tone", "magic", "era", "danger"):
        i.add_argument(f"--{dial}", required=True)
    i.add_argument("--party-size", type=int, required=True)
    i.add_argument("--start-level", type=int, default=1)
    i.add_argument("--content-mix", required=True, help="three of exploration,politics,war,horror,mystery")
    i.add_argument("--must", action="append")
    i.add_argument("--must-not", action="append")
    i.add_argument("--lang", default="tr")
    i.add_argument("--seed")
    i.add_argument("--concurrency", type=int, default=8)
    i.add_argument("--economy", action="store_true")
    i.add_argument("--fixture", action="store_true")

    sub.add_parser("reconcile")
    pe = sub.add_parser("pending")
    pe.add_argument("--phase", required=True)
    pe.add_argument("--json", action="store_true")

    m = sub.add_parser("mark")
    m.add_argument("--phase", required=True)
    m.add_argument("--status")
    m.add_argument("--roster")
    m.add_argument("--skeleton")
    m.add_argument("--entity")
    m.add_argument("--attempt", type=int)
    m.add_argument("--agent")
    m.add_argument("--error")
    m.add_argument("--file")
    m.add_argument("--stage-file")
    m.add_argument("--critique-loop", action="store_true")
    m.add_argument("--critique-verdict", choices=("pass", "fix", "rerun", "critique_missing"))
    m.add_argument("--validator-errors", type=int)
    m.add_argument("--validator-warnings", type=int)
    m.add_argument("--direction")
    m.add_argument("--workflow-run")
    m.add_argument("--finished", action="store_true")

    ap = sub.add_parser("approve")
    ap.add_argument("--phase", required=True)
    ap.add_argument("--card")
    ap.add_argument("--commit")
    ap.add_argument("--round")
    ap.add_argument("--scope", choices=SCOPES)
    ap.add_argument("--affected", type=int)

    st = sub.add_parser("stale")
    st.add_argument("--from", dest="from_phase", required=True)
    st.add_argument("--reason", required=True)

    t = sub.add_parser("tokens")
    t.add_argument("--phase", required=True)
    t.add_argument("--out", type=int, required=True)
    t.add_argument("--in", dest="tokens_in", type=int)
    t.add_argument("--cache-read", type=int)
    t.add_argument("--model")
    t.add_argument("--wall", type=int)
    t.add_argument("--agents", type=int)

    r = sub.add_parser("roll")
    r.add_argument("--record", required=True, help="JSON record")
    r.add_argument("--secret", action="store_true")

    q = sub.add_parser("ask")
    q.add_argument("--question", required=True)
    q.add_argument("--answer", required=True)
    q.add_argument("--agent", required=True)

    d = sub.add_parser("detail-log")
    d.add_argument("--id", required=True)
    d.add_argument("--day", type=int, required=True)
    d.add_argument("--trigger", required=True)
    d.add_argument("--snapshot")
    d.add_argument("--commit")

    rv = sub.add_parser("revision")
    rv.add_argument("--scope", required=True)
    rv.add_argument("--reason", required=True)
    rv.add_argument("--affected", type=int, default=0)
    rv.add_argument("--phase")
    rv.add_argument("--commit")

    sm = sub.add_parser("set-mode")
    sm.add_argument("mode")

    sd = sub.add_parser("seeded", help="the idempotency ledger design_seed.py consults")
    sd.add_argument("--add", help="comma-separated keys")
    sd.add_argument("--list", action="store_true")

    s = sub.add_parser("status")
    s.add_argument("--json", action="store_true")

    a = p.parse_args(argv)
    c = a.campaign
    if a.cmd == "init":
        return init(c, a)
    if a.cmd == "reconcile":
        reconcile(c)
        return 0
    if a.cmd == "pending":
        return pending(c, a.phase, a.json)
    if a.cmd == "mark":
        return mark(c, a)
    if a.cmd == "approve":
        if not a.round and not (a.card and a.commit):
            print("design_manifest: approve needs --card and --commit, or --round", file=sys.stderr)
            return 2
        return approve(c, a)
    if a.cmd == "stale":
        return stale(c, a)
    if a.cmd == "tokens":
        return tokens(c, a)
    if a.cmd == "roll":
        append_roll(c, json.loads(a.record), a.secret)
        return 0
    if a.cmd == "ask":
        return ask(c, a)
    if a.cmd == "detail-log":
        return detail_log(c, a)
    if a.cmd == "revision":
        return revision(c, a)
    if a.cmd == "set-mode":
        return set_mode(c, a.mode)
    if a.cmd == "seeded":
        if a.add:
            n = mark_seeded(c, [k.strip() for k in a.add.split(",")])
            print(f"design_manifest: {n} new key(s) in the seeded ledger")
        else:
            for k in load(c)["seeded"]:
                print(f"  {k}")
        return 0
    if a.cmd == "status":
        return status(c, a.json)
    return 2


if __name__ == "__main__":
    sys.exit(main())
