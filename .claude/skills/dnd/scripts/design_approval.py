#!/usr/bin/env python3
"""
design_approval.py — the phase card and the critique record (plan item 19.6, 15.2, 24.6 #6).

The card is the one thing the owner reads to approve a phase. It is built from the PUBLIC
projection, the manifest and the tables — never from agent returns — and the only figures that
touch the canonical registry are computed counts (the scale band, the clue count per act). Hidden
entities appear in no form. Before the card is written it is scanned for every secret entity's
name and for any sentence of a dm-only file; a hit refuses the card.

CLI:
  design_approval.py -c CAMP card --phase PN [--out FILE]          write design/_approval/PN.card.md (Turkish)
  design_approval.py -c CAMP critique --phase PN --file RETURN.json [--critic N]
                                                                     store a critic's return: ids, verdicts, codes only
  design_approval.py -c CAMP leak-check FILE                         exit 1 if FILE carries a secret name or dm-only sentence

Exit codes: 0 ok · 1 refused (a leak, a bad return) · 2 usage
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
import design_tables as dt  # noqa: E402
from design_io import CONTAINER_PREFIXES, campaign_dir, design_dir, dm_only_dir, now_iso, read_json, text_field  # noqa: E402

# Rows of these types are the arc: DM-open, player-avoid. The card counts them and never prints their names or
# one-liners (birth 2, R.6: the P7 card read as a plot synopsis to the owner, who is also the player).
SPOILER_TYPES = ("arc", "beat", "chapter", "node", "socket", "thread")

PHASE_TITLES = {"P0": "dials", "P1": "premise", "P2": "cosmos", "P3": "lands", "P4": "powers",
                "P5": "people", "P6": "sites", "P7": "arc", "P8": "primer and closing", "P9": "integration"}
BAND_KEYS = {"P2": [("god", "gods")], "P3": [("polity", "polities"), ("region", "regions")],
             "P4": [("faction", "factions.count")], "P5": [("npc", "named_npcs")], "P6": [("site", "sites.count")],
             "P7": [("seed", "quest_seeds")]}
VERDICTS = ("pass", "fix", "rerun")
FINDING_VERDICTS = ("pass", "fix", "rerun", "note")
SLUG = re.compile(r"^[A-Za-z0-9_:.\-]+$")   # ids, phase ids (P6), wish slots (wish:must:1), reason codes


# ── sources ───────────────────────────────────────────────────────────────────

def projection(campaign: str) -> dict:
    return (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})


def canonical(campaign: str) -> dict:
    """Read for COUNTS only; nothing from it is printed."""
    return (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})


def dig(obj, dotted: str):
    for part in dotted.split("."):
        obj = obj.get(part) if isinstance(obj, dict) else None
    return obj


def language_of(eid: str, ent: dict, assignments: dict, proj: dict, default: str = "—") -> str:
    """The naming language of an entity: its own field, its assignment, or the assignment of the polity /
    faction / region / settlement it belongs to (two hops); else the campaign's only language, else —."""
    for key in ("lang", "naming_language", "language"):
        if isinstance(ent.get(key), str) and ent[key]:
            return ent[key]
    if eid in assignments:
        return assignments[eid]
    for key in ("polity", "faction", "region", "settlement", "location_at_birth"):
        ref = ent.get(key)
        if isinstance(ref, str) and ref in assignments:
            return assignments[ref]
        if isinstance(ref, str) and ref in proj:
            for k2 in ("polity", "region", "settlement"):
                r2 = proj[ref].get(k2)
                if isinstance(r2, str) and r2 in assignments:
                    return assignments[r2]
    return default


def critique_chains(ph: dict) -> tuple[dict, str, list, str, list]:
    """(entity -> ['c1:fix', 'c1:pass', 'c2:pass'], phase verdict, phase finding lines, wishes verdict, skeleton verdicts)."""
    crit = ph.get("critique") or {}
    chains: dict = {}
    phase_verdict, wishes_verdict = "—", "—"
    phase_lines: list = []
    phase_chain: list = []
    for rec in crit.get("records") or []:
        eid = rec.get("entity_id") or ""
        findings = rec.get("findings") or []
        kind = rec.get("kind")
        if kind is None:            # records written before birth 2 carried no kind
            if eid.startswith("skeleton"):
                kind = "skeleton"
            elif eid == ph.get("id") or (eid.startswith("P") and len(eid) == 2):
                kind = "wishes" if any(f.get("rubric_id") == "rubric_wishes" for f in findings) else "phase"
            else:
                kind = "entity"
        if kind == "skeleton":
            continue
        if kind == "wishes":
            wishes_verdict = rec.get("verdict") or "—"
            continue
        if kind == "phase":
            phase_chain.append(rec.get("verdict") or "—")
            phase_lines = [f"{f.get('rubric_id')} → {f.get('entity_id')} ({f.get('verdict')}{', ' + f['reason_code'] if f.get('reason_code') else ''})"
                           for f in findings if f.get("verdict") in ("fix", "rerun")]
            continue
        chains.setdefault(eid, []).append(f"c{rec.get('critic', 1)}:{rec.get('verdict')}")
    if phase_chain:
        phase_verdict = " → ".join(phase_chain)
    return chains, phase_verdict, phase_lines, wishes_verdict, list(crit.get("skeleton_verdicts") or [])


def elapsed_minutes(ph: dict) -> str:
    if ph.get("wall_s"):
        return str(round(int(ph["wall_s"]) / 60))
    if ph.get("started"):
        try:
            from datetime import datetime, timezone
            t0 = datetime.fromisoformat(str(ph["started"]).replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(str(ph.get("finished") or now_iso()).replace("Z", "+00:00"))
            return str(max(0, round((t1 - t0).total_seconds() / 60)))
        except ValueError:
            return "—"
    return "—"


# ── leak scan ─────────────────────────────────────────────────────────────────

def secret_terms(campaign: str) -> tuple[set, list]:
    """Every secret entity's name and aliases, and every sentence of every dm-only prose file (≥ 40 chars)."""
    names = set()
    for ent in canonical(campaign).values():
        if ent.get("secrecy") == "secret":
            for n in [ent.get("name")] + list(ent.get("aliases") or []):
                if n and len(n) >= 3:
                    names.add(n)
    sentences = []
    dm_dir = dm_only_dir(campaign)
    # build item 14b: the secret stock's names, and the secretly rolled rows' ids and own sentences (a row's label is
    # ordinary words a public line may carry: the reasoning of build 12a)
    for L in ((read_json(dm_dir / "name-pool-secret.json") or {}).get("languages") or {}).values():
        names |= {e["name"] for v in L.values() for e in v if len(e.get("name", "")) >= 3}
    for r in (read_json(dm_dir / "dice-log.json") or {}).get("rolls") or []:
        row = dt.row(r["table"], r["row_id"]) if r.get("row_id") and ".yaml" in str(r.get("table")) else None
        if row:
            names.add(row["id"])
            sentences += [row[k] for k in ("statement", "cause", "rule") if isinstance(row.get(k), str) and len(row[k]) >= 24]
    for path in dm_dir.rglob("*.md"):
        if "_snapshots" in path.relative_to(dm_dir).parts:
            continue        # dry-3: an approval snapshot copies design/ whole; its public half is not secret text
        text = path.read_text(encoding="utf-8", errors="replace")
        for s in re.split(r"(?<=[.!?])\s+|\n", text):
            s = s.strip().strip("-*# ").strip()
            if len(s) >= 40 and not s.startswith(("|", "`", "[[", "entity:", "mirror", "covers", "stamped")):
                sentences.append(s)
    return names, sentences


def secret_code_terms(campaign: str) -> set:
    """The secret terms a reason code is checked against (build item 18f): every secret name of `secret_terms` as a
    slug (a secret entity's, the secret stock's) and every secretly rolled row's id with its tail after the table's
    prefix when the tail is distinctive (two words, or eight letters: `goal_patron_will` → `patron_will`)."""
    names, _ = secret_terms(campaign)
    out = set()
    for n in names:
        slug = re.sub(r"[^a-z0-9]+", "_", str(n).lower()).strip("_")
        if len(slug) >= 3:
            out.add(slug)
        tail = slug.split("_", 1)[1] if "_" in slug else ""
        if tail and ("_" in tail or len(tail) >= 8):
            out.add(tail)
    return out


def carries_secret(code: str, terms: set) -> bool:
    """A slug carries a term when the term's words stand in it as a run of whole words."""
    padded = "_" + re.sub(r"[^a-z0-9]+", "_", code.lower()).strip("_") + "_"
    return any(f"_{t}_" in padded for t in terms)


def leaks_in(text: str, names: set, sentences: list) -> list[str]:
    hits = []
    for n in sorted(names):
        if re.search(r"(?<![\w'])" + re.escape(n) + r"(?![\w])", text):
            hits.append(f"secret name: {n[:1]}…")
    for s in sentences:
        if s in text:
            hits.append(f"dm-only sentence ({len(s)} chars)")
    if "## Secret" in text:
        hits.append("a Secret heading")
    return hits


# ── the card ──────────────────────────────────────────────────────────────────

def previous_card(path: Path) -> dict | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    ids = re.search(r"<!-- ids: (.*?) -->", text)
    names = re.search(r"<!-- names: (.*?) -->", text)
    attempt = re.search(r"<!-- attempt: (\d+) -->", text)
    rnd = re.search(r"<!-- round: (\d+) -->", text)
    files = re.search(r"<!-- files: (.*?) -->", text)
    return {"ids": set(filter(None, (ids.group(1).split(",") if ids else []))),
            "names": dict(x.split("=", 1) for x in (names.group(1).split("|") if names and names.group(1) else []) if "=" in x),
            "attempt": int(attempt.group(1)) if attempt else 0, "text": text,
            "round": int(rnd.group(1)) if rnd else 0,
            "files": dict(x.split("=", 1) for x in (files.group(1).split("|") if files and files.group(1) else []) if "=" in x)}


# build item 18f (test birth P1-1, #10-11): a correction round shows on the card: its number beside the attempt, and what
# it changed (the entities it reran, the public files whose text changed since the previous card)

def card_round(ph: dict) -> int:
    return len((ph.get("approval") or {}).get("rounds") or [])


def public_file_digests(campaign: str, rows: dict) -> dict:
    """{public prose file: its digest} for the files the card's rows live in (never a dm-only file)."""
    import hashlib
    out = {}
    for e in rows.values():
        path = str(e.get("file") or "")
        full = campaign_dir(campaign) / path
        if path and "dm-only" not in path and full.is_file():
            out[path] = hashlib.sha256(full.read_bytes()).hexdigest()[:12]
    return dict(sorted(out.items()))


def round_marks(rnd: int, files: dict) -> list[str]:
    return [f"<!-- round: {rnd} -->", "<!-- files: " + "|".join(f"{p}={s}" for p, s in files.items()) + " -->"]


def round_changes(prev: dict | None, ph: dict, rows: dict, files: dict, attempt: int, rnd: int, heading: str) -> list[str]:
    """The card's section for a correction round, when the previous card was this attempt before the round."""
    if not prev or prev["attempt"] != attempt or prev.get("round", 0) == rnd or not rnd:
        return []
    last = ((ph.get("approval") or {}).get("rounds") or [])[-1]
    rerun = list(last.get("rerun") or [])
    reran = [e for e in rerun if e in rows]
    hidden = len([e for e in rerun if e not in rows and e != "*"])
    changed = [p for p, s in files.items() if prev["files"].get(p) != s]
    same = [p for p in files if p not in changed]
    return [heading.format(a=prev.get("round", 0), b=rnd),
            f"  the round: {last.get('scope', '—')}" + (f" ({last['revision']})" if last.get("revision") else ""),
            "  rewritten: " + (", ".join(reran) or ("the whole phase" if "*" in rerun else "—")) + (f" (+{hidden} hidden)" if hidden else ""),
            f"  public files changed: {', '.join(changed) or '—'} · unchanged: {', '.join(same) or '—'}", ""]


def validator_summary(campaign: str, phase: str) -> tuple[dict, list]:
    import subprocess
    proc = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).with_name("design_check.py")), "-c", campaign,
                           "--phase", phase, "--redact", "--json"], capture_output=True, text=True, encoding="utf-8")
    try:
        findings = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        findings = []
    if not isinstance(findings, list):
        findings = findings.get("findings") or []
    per_module: dict = {}
    for f in findings:
        m = per_module.setdefault(f.get("module", "?"), {"error": 0, "warning": 0})
        if f.get("severity") in m:
            m[f["severity"]] += 1
    return per_module, findings


def wish_ticks(ph: dict, wishes: dict) -> list[str]:
    findings = [f for rec in (ph.get("critique", {}).get("records") or []) for f in rec.get("findings", [])
                if f.get("rubric_id") == "rubric_wishes"]
    verdict_by = {f["entity_id"]: f["verdict"] for f in findings}
    lines = []
    for kind, label in (("must", "must"), ("must_not", "must not")):
        for i, w in enumerate(wishes.get(kind) or [], 1):
            v = verdict_by.get(f"wish:{kind}:{i}")
            mark = "✓" if v == "pass" else "✗" if v in ("fix", "rerun") else "?"
            lines.append(f"{label}: {w} {mark}")
    return lines


def secret_abstract(campaign: str, ph: dict) -> list[str]:
    """P1 only: archetype class, novelty vs used.json, clue count per act, critic agreement — no text."""
    log = read_json(dm_only_dir(campaign) / "dice-log.json") or {"rolls": []}
    arche = next((r.get("row_id") for r in log["rolls"] if r.get("label") in ("secret_archetype", "P1.secret_archetype")), None)
    row = dt.row("secrets.yaml#archetype", arche) if arche else None
    klass = (row or {}).get("hides_in", "unknown")
    try:
        import design_dice as dd
        gone = dd.rows_used_elsewhere(campaign, "secrets.yaml#archetype")
    except Exception:
        gone = set()
    novel = "yes" if arche and arche not in gone else "no" if arche else "?"
    clues_by_act: dict = {}
    for ent in canonical(campaign).values():
        if ent.get("type") == "premise":
            for c in (ent.get("dm_only") or {}).get("clues") or []:
                clues_by_act[c.get("act")] = clues_by_act.get(c.get("act"), 0) + 1
    clue_line = ", ".join(f"act {a}: {n}" for a, n in sorted(clues_by_act.items(), key=lambda x: str(x[0]))) or "not placed yet"
    recs = [r for r in (ph.get("critique", {}).get("records") or []) if r.get("entity_id", "").startswith("premise_")]
    by_critic = {r.get("critic"): r.get("verdict") for r in recs}
    agreement = "agree" if len(by_critic) >= 2 and len(set(by_critic.values())) == 1 else "differ" if len(by_critic) >= 2 else "one critic"
    return [f"- **The secret layer (spoiler-safe):** archetype class *{klass}* · new (used.json): {novel} · clues: {clue_line} · critics: {agreement}"]


def map_lines(campaign: str) -> list[str]:
    mp = read_json(design_dir(campaign) / "map.json") or {}
    nodes = [n for n in mp.get("nodes") or [] if n.get("secrecy", "public") == "public"]
    hubs = [n["id"] for n in nodes if n.get("hub")]
    lines = [f"- **Player map (text):** {len(nodes)} public nodes, hubs: {', '.join(hubs) or '—'}"]
    for n in nodes[:20]:
        lines.append(f"  - {n['id']} ({n.get('kind')}, {n.get('terrain', '')}) @ {n.get('x')},{n.get('y')}")
    return lines


GATE_LABELS = {"render": "the player files could not be rendered", "incomplete": "roster incomplete", "band": "outside the band", "critic_missing": "a critic did not run",
               "validator": "validator error", "seed": "seed error", "orphan_stub": "orphan stub",
               "promise": "a due promise a script checks is not kept", "promise_unjudged": "a due promise has no critic's verdict",
               "dnd_incomplete": "a D&D campaign's piece is missing", "phase_fix_due": "the phase critic's fix waits for its writer"}

# the loop of the re-critique after a phase critic's fix (.claude/workflows/design-fanout.js: MAX_FIX_LOOPS + 2)
PHASE_FIX_LOOP = 4


def unit_of(eid: str, roster: list, rows: dict) -> str | None:
    """The roster unit that writes an entity: itself, or the unit whose prose file the entity's row lives in (P1's
    roster is the premise; its signature and break rows are written beside it in design/premise.md)."""
    if eid in roster:
        return eid
    path = (rows.get(eid) or {}).get("file")
    return next((u for u in roster if path and (rows.get(u) or {}).get("file") == path), None)


def phase_fixes_due(campaign: str, phase: str, manifest: dict | None = None) -> dict:
    """{roster unit: its findings} — build item 18f (test birth P1-1, #5): the latest phase critic return of this attempt
    says fix (or rerun) on entities a unit writes, itself or a row it covers; each finding goes to that unit's writer as
    {rubric_id, entity_id, reason_code}. A unit that already had its phase fix this attempt (the workflow's re-critique
    at PHASE_FIX_LOOP, or one `phase begin` served) is left to the gate's other items and the owner."""
    m = manifest if manifest is not None else dm.load(campaign)
    ph = m["phases"].get(phase) or {}
    attempt = int(ph.get("attempt") or 1)
    recs = [r for r in (ph.get("critique") or {}).get("records") or [] if r.get("attempt") == attempt]
    last = next((r for r in reversed(recs) if r.get("kind") == "phase"), None)
    if not last or last.get("verdict") not in ("fix", "rerun"):
        return {}
    roster, rows = ph.get("roster") or [], canonical(campaign)
    out: dict = {}
    for f in last.get("findings") or []:
        if f.get("verdict") not in ("fix", "rerun"):
            continue
        unit = unit_of(str(f.get("entity_id")), roster, rows)
        if unit:
            out.setdefault(unit, []).append({k: f.get(k) for k in ("rubric_id", "entity_id", "reason_code")})
    served = {r["entity_id"] for r in recs if r.get("kind") == "entity" and r.get("loop") == PHASE_FIX_LOOP}
    served |= {u for u in out if ((m["entities"].get(u) or {}).get("phase_fix") or {}).get("attempt") == attempt}
    return {u: fs for u, fs in out.items() if u not in served}


def dnd_ticks(campaign: str, m: dict) -> list[tuple[str, bool]]:
    """The D&D campaign's completeness (build item 18e, G9), read from the records: a villain kind and creature, a hand,
    a goal, a weakness, a lair, a start, the creature families, three stages with three clues each, trope breaks that
    bend. Names the pieces only, never what they hold."""
    f = m.get("foundation") or {}
    move = f.get("move") or {}
    log = read_json(dm_only_dir(campaign) / "dice-log.json") or {}
    threat = log.get("threat") or {}
    stages = ((log.get("identity") or {}).get("secret") or {}).get("stages") or []
    removes = [b for b in (m.get("identity") or {}).get("trope_breaks") or [] if (dt.row("trope-breaks.yaml", b["id"]) or {}).get("removes")]
    hidden = threat.get("hand") or {}            # build item 19a: an unnoticed move's hand is in the threat's dm-only record
    return [("villain", bool(threat.get("family") and threat.get("creature"))), ("hand", bool(move.get("hand") or hidden.get("id"))),
            ("goal", bool((threat.get("goal") or {}).get("id"))), ("weakness", bool(threat.get("weakness"))),
            ("lair", bool((threat.get("lair") or {}).get("form") and (threat.get("lair") or {}).get("where"))),
            ("start", bool(f.get("start")) and f.get("start") != "heart"), ("families", bool(move.get("families") or hidden.get("families"))),
            ("stages 3×3", len(stages) == 3 and all(len(s.get("clues") or []) == 3 for s in stages)),
            ("breaks bend", not removes)]
PROMISE_VERDICTS = ("kept", "not_kept")


def gate(campaign: str, phase: str, findings: list | None = None) -> list[dict]:
    """The approve gate (root-cause analysis 1, RC-01): the facts the card already computes, read by approve in test and
    real births alike; [] when open. Items carry a code, the ids concerned and an English detail."""
    m = dm.load(campaign)
    ph = m["phases"].get(phase) or {}
    if phase not in dm.PHASES or phase == "P0":
        return []
    import design_prompts as dp
    roster = ph.get("roster") or []
    canon = canonical(campaign)
    out: list[dict] = []
    incomplete = [e for e in roster
                  if dm.ENTITY_RANK.get(m["entities"].get(e, {}).get("status", "pending"), 0) < dm.ENTITY_RANK["merged"]]
    if incomplete:
        out.append({"code": "incomplete", "ids": incomplete, "detail": f"not complete ({', '.join(incomplete)} not merged)"})
    if not m["_meta"].get("fixture"):           # the hand-written fixture is a micro bible, below every band by design
        scale = dt.scale_row(m["dials"]["scale"])
        for etype, key in BAND_KEYS.get(phase, []):
            lo, hi = dt.band(dig(scale, key))
            if not lo <= sum(1 for e in canon.values() if e.get("type") == etype) <= hi:
                out.append({"code": "band", "ids": [], "detail": f"{etype} outside band {lo}-{hi}"})
    if roster:
        chains, phase_verdict, _, wishes_verdict, _ = critique_chains(dict(ph, id=phase))
        missing = [n for n, v in (("phase critic", phase_verdict), ("wishes critic", wishes_verdict)) if v == "—"]
        silent = [e for e in roster if e not in incomplete and dp.prompt_for(phase, e) and not chains.get(e)]
        if missing or silent:
            out.append({"code": "critic_missing", "ids": silent,
                        "detail": ", ".join(missing + ([f"{len(silent)} roster item(s) never critiqued"] if silent else []))})
    if findings is None:
        _, findings = validator_summary(campaign, phase)
    # an error a later phase resolves by design never reaches here: the per-phase validator names each module's and each
    # such code's first phase (design_check.MODULE_FROM, CODE_FROM; errata 24.2 #23)
    owned = sorted({str(f.get("entity")) for f in findings if f.get("severity") == "error"
                    and (f.get("entity") in roster or (canon.get(f.get("entity")) or {}).get("created_phase") == phase)})
    if owned:
        out.append({"code": "validator", "ids": owned, "detail": f"validator errors on {len(owned)} entit(ies) of this phase"})
    render = (ph.get("render") or {}).get("failed")
    if render:
        out.append({"code": "render", "ids": [], "detail": f"the player's files did not render ({render})"})
    failed = int((ph.get("seed") or {}).get("failed") or 0)
    if failed:
        out.append({"code": "seed", "ids": [], "detail": f"{failed} seed call(s) failed at the last merge"})
    orphans = [e for e in dm.orphan_stubs(campaign, phase, dm.BLOCKING_STUB_TYPES) if e not in roster]
    if orphans:
        out.append({"code": "orphan_stub", "ids": orphans, "detail": f"{len(orphans)} owned stub(s) never written"})
    if phase == "P1" and (m.get("foundation") or {}).get("move"):          # build item 18e (G9); a legacy birth has no move
        missing = [k for k, ok in dnd_ticks(campaign, m) if not ok]
        if missing:
            out.append({"code": "dnd_incomplete", "ids": [], "detail": f"the D&D campaign misses: {', '.join(missing)}"})
    due = phase_fixes_due(campaign, phase, m)
    if due:
        out.append({"code": "phase_fix_due", "ids": sorted(due),
                    "detail": f"the phase critic's fix waits for its writer: run `phase {phase} begin --json` and the Workflow"})
    # build item 12b: a due promise a script checks and that is not kept closes the gate, and so does a due promise
    # the critic gave no verdict; a critic's `not_kept` does not (the card lists it, the owner decides). A secret
    # promise is an id and a count here, never a sentence. A legacy birth has no ledger: nothing is added.
    import design_promises as dpr
    for code, (public, secret), what in (("promise", dpr.script_failures(campaign, phase), "a script checks not kept"),
                                         ("promise_unjudged", dpr.unjudged(campaign, phase), "without the critic's verdict")):
        if public or secret:
            out.append({"code": code, "ids": public + secret, "secret": len(secret),
                        "detail": f"{len(public) + len(secret)} due promise(s) {what} ({len(secret)} of them secret)"})
    return out


def minor_orphans(campaign: str, phase: str) -> dict:
    """Owned stubs of the non-blocking types, counted by type for the card (a warning, not a refusal)."""
    canon = canonical(campaign)
    counts: dict = {}
    for eid in dm.orphan_stubs(campaign, phase):
        t = canon.get(eid, {}).get("type")
        if t not in dm.BLOCKING_STUB_TYPES:
            counts[t] = counts.get(t, 0) + 1
    return counts


def gate_text(items: list[dict]) -> str:
    """The conductor's refusal line: codes, details and ids."""
    return "; ".join(f"{i['code']}: {i['detail']}"
                     + (f" [{', '.join(i['ids'][:12])}]" if i["ids"] and i["code"] != "incomplete" else "")
                     for i in items)


def gate_card_line(items: list[dict], proj: dict) -> str:
    """The card's line: public, non-arc ids by id; secret and arc rows only as a count (the card is the player's surface)."""
    if not items:
        return "- **Gate:** open ✓"
    parts = []
    for i in items:
        if i["code"].startswith("promise"):         # a promise is no registry row: the public ones' count (the 22d audit:
            public = len(i["ids"]) - int(i.get("secret") or 0)       # a secret one adds no number, only the closed gate)
            parts.append(GATE_LABELS[i["code"]] + (f" ({public})" if public else ""))
            continue
        shown = [e for e in i["ids"] if e in proj and proj[e].get("type") not in SPOILER_TYPES
                 and proj[e].get("secrecy", "public") == "public"]
        ids = ", ".join(shown[:6]) + (f" +{len(shown) - 6}" if len(shown) > 6 else "")
        extra = ids                                 # the 22d audit: a hidden record adds no count to the line
        parts.append(GATE_LABELS.get(i["code"], i["code"]) + (f" ({extra})" if extra else ""))
    return ("- ⛔ **Gate closed:** " + " · ".join(parts)
            + " — approval is refused; passing needs `--force` and a reason.")


LINK = re.compile(r"\[\[([a-z]+_[a-z0-9_]+)\]\]")


def readable(text: str, proj: dict) -> str:
    """The card is the player's surface: a [[link]] reads as its public name, a secret or unknown one as '…'
    (dry-3: seed hooks printed [[settlement_greyreach]], [[npc_ord]] raw)."""
    def name(m):
        e = proj.get(m.group(1)) or {}
        return e.get("name") if e.get("name") and e.get("secrecy", "public") == "public" else "…"
    return LINK.sub(name, str(text or ""))


def real_cost_text(ph: dict) -> str:
    """The run transcripts' real cost (design_cost.py, RC-09) beside the Workflow's context figure."""
    t = (ph.get("cost") or {}).get("totals") or {}
    if not t.get("requests"):
        return ""
    fmt = lambda n: f"{int(n):,}".replace(",", ".")
    return f" · **Real output:** {fmt(t['output'])} · **read from cache:** {fmt(t['cache_read'])} · **agents:** {t['agents']}"


def band_lines_of(campaign: str, phase: str) -> list[str]:
    """The phase's scale bands: the full count decides the tick, the public count is what the line prints."""
    m = dm.load(campaign)
    scale = dt.scale_row(m["dials"]["scale"])
    canon, proj = canonical(campaign), projection(campaign)
    out = []
    for etype, key in BAND_KEYS.get(phase, []):
        full = sum(1 for e in canon.values() if e.get("type") == etype)
        public = sum(1 for e in proj.values() if e.get("type") == etype)
        lo, hi = dt.band(dig(scale, key))
        out.append(f"{etype}: {public} public, band {lo}-{hi} {'✓' if lo <= full <= hi else '✗'}")
    return out


def phase_written_ids(campaign: str, phase: str) -> set:
    """Ids of every row this phase merged: the fragments in its merged folder and the rows of its containers."""
    from design_io import is_fragment
    merged = design_dir(campaign) / "_staging" / phase / "merged"
    out: set = set()
    for f in (merged.glob("*.json") if merged.is_dir() else []):
        if not is_fragment(f):
            continue
        frag = read_json(f) or {}
        if frag.get("registry") and frag.get("id"):
            out.add(frag["id"])
        out |= {r.get("id") for r in frag.get("rows") or [] if isinstance(r, dict) and r.get("id")}
    return out


def build_card(campaign: str, phase: str) -> str:
    m = dm.load(campaign)
    if phase == "P1" and scripted_p1(m):
        return p1_card(campaign)
    import design_cosmos_door as cd
    if phase == "P2" and cd.applies(m):
        return p2_card(campaign)            # build item 22d; a legacy birth's P2 card is built as before
    ph = m["phases"][phase]
    proj = projection(campaign)
    canon = canonical(campaign)
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    assignments = naming.get("assignments") or {}
    scale = dt.scale_row(m["dials"]["scale"])
    roster = ph.get("roster") or []
    # dry-3: the P5 card listed 7 NPCs of 17; the ten minors were P3 stubs filled inside two batches, and the table
    # took only rows created in this phase or on its roster; every row this phase merged is the phase's
    written = phase_written_ids(campaign, phase)
    mine = {eid: e for eid, e in proj.items() if e.get("created_phase") == phase or eid in roster or eid in written}
    spoilers = {eid: e for eid, e in mine.items() if e.get("type") in SPOILER_TYPES}
    shown_rows = {eid: e for eid, e in mine.items() if eid not in spoilers}
    attempt = int(ph.get("attempt") or 1)
    rnd, files = card_round(ph), public_file_digests(campaign, shown_rows)

    lines = [f"# Phase card — {phase} ({PHASE_TITLES.get(phase, phase)}) · {campaign} · attempt {attempt}"
             + (f" · correction round {rnd}" if rnd else ""),
             f"<!-- attempt: {attempt} -->", *round_marks(rnd, files), f"<!-- ids: {','.join(sorted(mine))} -->",
             "<!-- names: " + "|".join(f"{eid}={e.get('name', '')}" for eid, e in sorted(shown_rows.items())) + " -->", ""]
    val = ph.get("validator") or {}
    crit = ph.get("critique") or {}
    failed = [e for e in roster if m["entities"].get(e, {}).get("status") == "failed"]
    incomplete = [e for e in roster if dm.ENTITY_RANK.get(m["entities"].get(e, {}).get("status", "pending"), 0) < dm.ENTITY_RANK["merged"]]
    missing = sum(1 for v in crit.get("verdicts") or [] if v == "critique_missing")
    chains, phase_verdict, phase_lines, wishes_verdict, skeleton_verdicts = critique_chains(dict(ph, id=phase))
    tokens_out = int((ph.get("tokens") or {}).get("out") or 0)
    per_module, findings = validator_summary(campaign, phase)
    gate_items = gate(campaign, phase, findings=findings)
    lines.append(f"- **Status:** {ph['status']} · **Validator:** {val.get('errors', '—')} errors, {val.get('warnings', '—')} warnings · "
                 f"**Failed:** {', '.join(failed) or '—'} · **Time:** {elapsed_minutes(ph)} min · "
                 f"**Context (Workflow):** {f'{tokens_out:,}'.replace(',', '.') + ' tokens' if tokens_out else '—'}"
                 + real_cost_text(ph))
    lines.append(f"- **Critique:** phase critic {phase_verdict} · wishes critic {wishes_verdict}"
                 + (f" · skeleton {' → '.join(skeleton_verdicts)}" if skeleton_verdicts else "")
                 + f" · entity fix loops {crit.get('entity_loops_total', 0)}"
                 + (f" · critiques missing {missing}" if missing else ""))
    for pl in phase_lines[:8]:
        lines.append(f"  - phase critic: {pl}")
    if incomplete:
        lines.append(f"- ⚠ **Incomplete:** {', '.join(incomplete)} — the phase is not complete; an entity never reached the registry, this card cannot be approved "
                     "(`phase begin --json` + fan-out, ya da `drop`).")
    not_passed = [eid for eid, ch in chains.items() if ch and ch[-1].split(":")[-1] in ("fix", "rerun")]
    if phase_verdict.split(" → ")[-1] in ("fix", "rerun"):
        not_passed.append("phase critic")
    if skeleton_verdicts and skeleton_verdicts[-1] in ("fix", "rerun"):
        not_passed.append("skeleton")
    if not_passed:
        lines.append(f"- ⚠ **A critic did not pass:** {', '.join(not_passed)} — the last verdict is `fix`; the fix loops are spent, "
                     "the owner decides (one correction sentence, or approval).")
    lines.append(gate_card_line(gate_items, proj))
    minor = minor_orphans(campaign, phase) if phase in dm.PHASES and phase != "P0" else {}
    if minor:
        lines.append("- ⚠ **Unwritten minor stubs:** " + ", ".join(f"{t} ×{n}" for t, n in sorted(minor.items()))
                     + " — owned by this phase or an earlier one; it does not stop the approval.")
    # scale band, script-side with the full count; the card prints the public count and a tick
    band_lines = band_lines_of(campaign, phase)
    if band_lines:
        lines.append("- **Scale band:** " + " · ".join(band_lines))
    wl = wish_ticks(ph, m["dials"].get("wishes") or {})
    if wl:
        lines.append("- **Wishes:** " + " · ".join(wl))
    if phase == "P1":
        lines += secret_abstract(campaign, ph)
    import design_promises as dpr
    lines += dpr.card_lines(campaign, phase)        # build item 12a: the ledger's counts; a legacy birth has none
    if ph.get("directions"):
        lines.append("- **Directions (from earlier rounds):** " + " · ".join(ph["directions"]))
    lines.append("")

    languages = list((naming.get("languages") or {}).keys())
    default_lang = languages[0] if len(languages) == 1 else "—"
    lines.append("## Born in this phase (public)")
    lines.append("| id | name | type | language | critique | one line |")
    lines.append("|---|---|---|---|---|---|")
    for eid, e in sorted(shown_rows.items()):
        one = readable(e.get("hook_tr") if e.get("type") == "seed" and e.get("hook_tr") else (e.get("summary") or ""), proj)
        lines.append(f"| {eid} | {e.get('name', '')} | {e.get('type', '')} | {language_of(eid, e, assignments, proj, default_lang)} | "
                     f"{' → '.join(chains.get(eid) or []) or '—'} | {one.replace('|', '/')} |")
    if spoilers:
        counts = {}
        for e in spoilers.values():
            counts[e.get("type")] = counts.get(e.get("type"), 0) + 1
        lines.append("| — | — | " + ", ".join(f"{t} ×{n}" for t, n in sorted(counts.items())) + " | — | "
                     + (" · ".join(f"{t}: {' → '.join(chains[eid])}" for eid in sorted(spoilers) for t in [eid] if chains.get(eid)) or "—")
                     + " | (the arc's content is open to the DM and closed to the player; the card shows counts and critique verdicts only) |")
    docs = []
    for rid in roster:
        if not rid.startswith(CONTAINER_PREFIXES):
            continue
        frag = read_json(design_dir(campaign) / "_staging" / phase / "merged" / f"{rid}.json") or {}
        prose = frag.get("prose")
        pfile = prose.get("file") if isinstance(prose, dict) else (prose if isinstance(prose, str) else None)
        counts = frag.get("counts") or {}
        status = m["entities"].get(rid, {}).get("status", "pending")
        docs.append(f"- `{rid}` — {status}" + (f" · {pfile}" if pfile else "")
                    + (" · " + ", ".join(f"{k} {v}" for k, v in counts.items()) if counts else "")
                    + (f" · critique {' → '.join(chains[rid])}" if chains.get(rid) else ""))
    if not mine and not docs:
        lines.append("| — | — | — | — | — | (this phase has produced no entity yet) |")
    if docs:
        lines.append("")
        lines.append("## Documents (this phase's files)")
        lines += docs
        if phase == "P8":
            primer = design_dir(campaign) / "player-primer.md"
            lines.append(f"- the player primer: `design/player-primer.md`"
                         + (f" ({len(primer.read_text(encoding='utf-8')):,} characters)".replace(",", ".") if primer.is_file() else " (not rendered yet)"))
    lines.append("")

    if phase == "P3":
        lines += map_lines(campaign)
        lines.append("")

    lines.append("## What a native knows")
    shown = 0
    for eid, e in sorted(shown_rows.items()):
        if e.get("summary") and e.get("secrecy", "public") == "public":
            lines.append(f"- {e['name']}: {readable(e['summary'], proj)}")
            shown += 1
            if shown >= 8:
                break
    if not shown:
        lines.append("- (nothing yet)")
    lines.append("")

    lines.append("## Validator (summary, shortened)")
    if per_module:
        for mod, c in sorted(per_module.items()):
            lines.append(f"- {mod}: {c['error']} errors, {c['warning']} warnings")
        for f in findings[:30]:
            msg = str(f.get("message") or "")
            tail = "" if ("dm-only" in msg or not msg) else f" — {msg[:90]}"
            lines.append(f"  - {f.get('severity', '?')} · {f.get('entity') or '—'} · `{f.get('code', '')}`{tail}")
    else:
        lines.append("- temiz")
    lines.append("")

    prev = previous_card(design_dir(campaign) / "_approval" / f"{phase}.card.md")
    if prev and prev["attempt"] != attempt:
        added = sorted(set(mine) - prev["ids"])
        removed = sorted(prev["ids"] - set(mine))
        renamed = sorted(eid for eid in set(mine) & prev["ids"] if prev["names"].get(eid, "") != (mine[eid].get("name") or ""))
        lines.append(f"## Changes from the previous card (attempt {prev['attempt']} → {attempt})")
        lines.append(f"- eklendi: {', '.join(added) or '—'}")
        lines.append(f"- removed: {', '.join(removed) or '—'}")
        lines.append(f"- renamed: {', '.join(renamed) or '—'}")
        lines.append("")
    lines += round_changes(prev, ph, shown_rows, files, attempt, rnd, "## Changes from the previous card (correction round {a} → {b})")

    lines.append("## Onay")
    if m["_meta"].get("auto_approve"):
        lines.append("- A test birth: the card is approved automatically (owner ruling 2026-09-25).")
    else:
        lines.append("- To approve, type exactly `onay`; a correction is one sentence (three rounds at most). The next phase starts with `devam`.")
    lines.append(f"- Produced: {now_iso()}")
    return "\n".join(lines) + "\n"


# ── P1's card (build item 14b; the layout the owner approved on 2026-10-04) ──────────────────────────────────

P1_MOVES = (("approve", 'designer.py -c {c} phase P1 approve --onay'),
            ("rerun", 'designer.py -c {c} phase P1 rerun --reason "<why>" [--reseed]'),
            ("reroll a name (people | institution | phenomenon)", 'design_names.py -c {c} reroll --slot <slot> --onay'),
            ("waive a promise", 'designer.py -c {c} promise waive <id> "<one sentence>" --onay'))


def scripted_p1(manifest: dict) -> bool:
    """A birth whose P1 the script rolled and sealed: it gets P1's own card. A legacy birth's card is built as before."""
    return all(isinstance(manifest.get(k), (dict, list)) for k in ("foundation", "identity", "promises", "p1_seal"))


def p1_card(campaign: str) -> str:
    """English, built by script, no dice on it: no roll label, no row id, no candidate list. What the writer has not
    written yet stands as an empty line."""
    import design_promises as dpr
    m = dm.load(campaign)
    ph = m["phases"]["P1"]
    f, ident = m["foundation"], m["identity"]
    proj = projection(campaign)
    attempt = int(ph.get("attempt") or 1)
    mine = {eid: e for eid, e in proj.items() if e.get("created_phase") == "P1" and e.get("type") not in SPOILER_TYPES}
    rnd, files = card_round(ph), public_file_digests(campaign, mine)
    label = lambda ref, rid: (dt.row(ref, rid) or {}).get("label") or "—"
    row = lambda lab, text: f"  {lab:<19} {text}"
    empty = "(not written yet)"
    L = [f"# P1 — THE FOUNDATION AND THE IDENTITY            campaign: {campaign}   attempt {attempt}"
         + (f" · correction round {rnd}" if rnd else ""),
         f"<!-- attempt: {attempt} -->", *round_marks(rnd, files), f"<!-- ids: {','.join(sorted(mine))} -->",
         "<!-- names: " + "|".join(f"{eid}={e.get('name', '')}" for eid, e in sorted(mine.items())) + " -->", ""]
    if f.get("spine_sentence"):              # build item 18e: the story's skeleton first, before a word of prose
        L += ["## THE STORY", f"  {f['spine_sentence']}", ""]

    by = {l["label"]: l["text"] for l in f.get("rendering") or []}
    L += ["## THE FOUNDATION", row("The world's shape", f"{by.get('The world\'s shape', '—')}; lands: {by.get('The lands', '—')}"),
          row("The past", by.get("The past", "—")), row("The value", by.get("The value", "—")), row("The conflict", by.get("The conflict", "—"))]
    if by.get("The second conflict"):
        L.append(row("", by["The second conflict"]))
    brk = by.get("The break", "—").split("; ")
    L.append(row("The break", brk[0]))
    L += [row("", part) for part in brk[1:]]
    band = f["escalation"]["level_band"]
    L += [row("The escalation", f"{f['escalation']['steps']} steps (levels {band[0]}-{band[1]})"), ""]

    sig = {e.get("slot"): e for e in proj.values() if e.get("type") == "signature"}
    premise = next((e for e in proj.values() if e.get("type") == "premise"), {})
    line = lambda slot: readable(text_field(sig[slot], "rule") or sig[slot].get("summary") or "", proj) if slot in sig else empty
    name = lambda slot: sig[slot].get("name") if slot in sig else "(not named yet)"
    questions = " · ".join(label("tensions.yaml", q["id"]) for q in ident["questions"])
    L += ["## THE IDENTITY", row("The question", questions + (f" — {readable(text_field(premise, 'question'), proj)}" if text_field(premise, "question") else "")),
          row("The people", f"{name('people')} — {label('signatures.yaml#people_lineage', ident['people']['lineage'])}; {line('people')}"),
          row("The institution", f"{name('institution')} — {label('signatures.yaml#institution_form', ident['institution']['form'])}; {line('institution')}"),
          row("The phenomenon", f"{name('phenomenon')} — {line('phenomenon')}"),
          row("Trope breaks", " · ".join(f"{label('trope-breaks.yaml', b['id'])} (tied to {label('trope-breaks.yaml#tie', b['tie']).lower()})" for b in ident["trope_breaks"]))]
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    import design_names as dnames
    people_name = sig["people"].get("name") if "people" in sig else None
    L += [row("Languages", " · ".join(dnames.language_label(lid, x, people_name) for lid, x in (naming.get("languages") or {}).items())), ""]

    L += ["## THE PLAYER PITCH", f"  {readable(text_field(premise, 'pitch'), proj) if text_field(premise, 'pitch') else empty}", ""]
    wishes = wish_ticks(ph, m["dials"].get("wishes") or {})
    if wishes:
        L += ["## WISHES"] + [f"  {w}" for w in wishes] + [""]

    log = read_json(dm_only_dir(campaign) / "dice-log.json") or {}
    sec = (log.get("identity") or {}).get("secret") or {}
    if sec.get("facts"):                     # build item 18e: the threat's hidden half, in counts
        n_st = len(sec.get("stages") or [])
        n_cl = min((len(s.get("clues") or []) for s in sec.get("stages") or []), default=0)
        L += ["## THE SECRET (spoiler-safe)", f"  the threat: rolled, hidden · hidden facts: {sec['facts']['hidden']} of 4 · "
              f"twist: {'yes' if sec.get('twist') else 'no'} · stages: {n_st} × {n_cl} clues", ""]
    else:
        arch = dt.row("secrets.yaml#archetype", sec.get("archetype") or "") or {}
        L += ["## THE SECRET (spoiler-safe)", f"  class: {arch.get('hides_in', 'unknown')}     the villain: rolled, hidden", ""]

    import design_names as dn
    pool = dn.load_pool(campaign) or {}
    kinds = {}
    for stocks in (pool.get("languages") or {}).values():
        for key, entries in stocks.items():
            a = kinds.setdefault(key, [0, 0])
            a[0] += sum(1 for e in entries if not e.get("used_by"))
            a[1] += len(entries)
    for key, entries in (pool.get("calendar") or {}).items():
        kinds[key] = [sum(1 for e in entries if not e.get("used_by")), len(entries)]
    L += ["## NAMES", "  " + (" · ".join(f"{dn.STOCK_WORDS.get(k, k)} {u} / {d}" for k, (u, d) in kinds.items() if d) or "—") + "   (unused / drawn)", ""]

    L += card_tail(campaign, "P1", m, ph, mine, files, attempt, rnd, proj, P1_MOVES,
                   ["  D&D: " + " · ".join(("✓ " if ok else "✗ ") + k for k, ok in dnd_ticks(campaign, m))] if f.get("move") else [])
    return "\n".join(L) + "\n"


def card_tail(campaign: str, phase: str, m: dict, ph: dict, mine: dict, files: dict, attempt: int, rnd: int, proj: dict,
              moves: tuple, extra_checks: list) -> list[str]:
    """The promises, the checks, the changes and the owner's moves: the closing sections of a script-built card (P1's
    since build item 14b, P2's since 22d)."""
    import design_promises as dpr
    c = dpr.counts(m["promises"], dpr.load_secret(campaign), phase)
    d = c["due"]
    L = ["## PROMISES", f"  due at {phase}: {d['total']} — kept {d['kept']}, not kept {d['not_kept']}, waived {d['waived']}" + (f", open {d['open']}" if d["open"] else "")]
    L += [f"    not kept: {p['name']} → {p['text']}   (`{p['id']}`)" for p in m["promises"] if p["status"] == "not_kept" and p.get("due") == phase]
    # the 22d audit (the owner): the secret layer as a status only, never a count
    sec = dpr.load_secret(campaign)
    if any(p.get("status") == "not_kept" for p in sec):
        shut = any(i["code"].startswith("promise") and i.get("secret") for i in gate(campaign, phase))
        status = "a secret promise is not kept" + (": the gate stays closed" if shut else " (a critic's verdict: the owner decides)")
    elif any(p.get("status") == "open" and p.get("due") == phase for p in sec):
        status = "not checked yet"
    else:
        status = "checked by script: all kept"
    L += ["  open: " + (" · ".join(f"{k} {v}" for k, v in c["open_by_due"].items()) or "—"), f"  secret: {status}", ""]

    door = ph.get("door")          # build item 17: recorded by each merge the door ran; the report file is the fallback
    if door is None and "door" not in ph:
        report = read_json(design_dir(campaign) / "_staging" / phase / "merge.report.json")
        door = None if report is None else {"refused": len(report.get("refused") or {})}
    door_line = "not run yet" if not door else "passed" if not door["refused"] else f"{door['refused']} unit(s) refused"
    validator_line = "not run yet" if not isinstance((ph.get("validator") or {}).get("errors"), int) else f"{ph['validator']['errors']} errors"
    chains, phase_verdict, _, wishes_verdict, _ = critique_chains(dict(ph, id=phase))
    crit = ph.get("critique") or {}
    per_module, findings = validator_summary(campaign, phase)
    closed = gate(campaign, phase, findings=findings)
    tokens_out = int((ph.get("tokens") or {}).get("out") or 0)
    L += ["## CHECKS", f"  door: {door_line} · critics: {crit.get('entity_loops_total') or 0} fix loop(s), "
          f"phase {phase_verdict}, wishes {wishes_verdict} · validator: {validator_line}",
          *extra_checks,
          "  " + gate_card_line(closed, proj).lstrip("- "),
          f"  cost: {f'{tokens_out:,}'.replace(',', '.') + ' tokens' if tokens_out else '—'}, {elapsed_minutes(ph)} min" + real_cost_text(ph), ""]

    prev = previous_card(design_dir(campaign) / "_approval" / f"{phase}.card.md")
    if prev and prev["attempt"] != attempt:
        L += [f"## CHANGES FROM THE PREVIOUS CARD (attempt {prev['attempt']} → {attempt})",
              f"  added: {', '.join(sorted(set(mine) - prev['ids'])) or '—'}", f"  removed: {', '.join(sorted(prev['ids'] - set(mine))) or '—'}",
              "  renamed: " + (", ".join(sorted(e for e in set(mine) & prev["ids"] if prev["names"].get(e, "") != (mine[e].get("name") or ""))) or "—"), ""]
    L += round_changes(prev, ph, mine, files, attempt, rnd, "## CHANGES FROM THE PREVIOUS CARD (correction round {a} → {b})")

    L += ["## YOUR MOVES", "  " + " · ".join(what for what, _ in moves)]
    L += [f"    {what}: `{cmd.format(c=campaign)}`" for what, cmd in moves]
    if m["_meta"].get("auto_approve"):
        L.append("  (a test birth: the card is approved automatically)")
    L.append(f"  produced: {now_iso()}")
    return L


# ── P2's card (build item 22d; docs/p2-tags.md S7 #4): English, built by script, no dice and no row id ──────────

P2_MOVES = (("approve", 'designer.py -c {c} phase P2 approve --onay'),
            ("rerun", 'designer.py -c {c} phase P2 rerun --reason "<why>" [--reseed]'),
            ("waive a promise", 'designer.py -c {c} promise waive <id> "<one sentence>" --onay'))


def p2_card(campaign: str) -> str:
    """The cosmos in words: the gods with their ranks and domains, where the dead go, the touched planes, magic, the
    ages and the dated events, the calendar and the start date. Built from the public records (`design.json#cosmos`)
    and the rows' labels: no die, no row id, nothing of the cosmos's dm-only half (the threat's seats, its own home plane,
    the mirror relation, a hidden name)."""
    m = dm.load(campaign)
    ph = m["phases"]["P2"]
    cos = m["cosmos"]
    proj = projection(campaign)
    attempt = int(ph.get("attempt") or 1)
    mine = {eid: e for eid, e in proj.items() if e.get("created_phase") == "P2" and e.get("type") not in SPOILER_TYPES
            and e.get("secrecy", "public") != "secret"}
    rnd, files = card_round(ph), public_file_digests(campaign, mine)
    label = lambda ref, rid: (dt.row(ref, rid) or {}).get("label") or "—"
    row = lambda lab, text: f"  {lab:<19} {text}"
    P, PL, M, H, C = "pantheon.yaml#", "planes.yaml#", "magic.yaml#", "history.yaml#", "calendar.yaml#"
    gods = {g["n"]: g for g in cos["gods"]}
    gname = lambda n: (gods[n].get("name") or gods[n].get("epithet") or "—") if n in gods else "—"
    domains = {r["id"]: r["label"] for r in dt.rows(P + "domain_scaffold")}
    L = [f"# P2 — THE COSMOS            campaign: {campaign}   attempt {attempt}" + (f" · correction round {rnd}" if rnd else ""),
         f"<!-- attempt: {attempt} -->", *round_marks(rnd, files), f"<!-- ids: {','.join(sorted(mine))} -->",
         "<!-- names: " + "|".join(f"{eid}={e.get('name', '')}" for eid, e in sorted(mine.items())) + " -->", ""]

    c = cos["counts"]
    n_of = lambda n, one, many: f"{n} {one if n == 1 else many}"
    L += ["## THE PANTHEON", row("The gods", f"{label(P + 'type', cos['type'])} · {label(P + 'presence', cos['presence'])}"),
          row("", f"{n_of(c['gods'], 'god', 'gods')}: {c['greater']} greater, {c['lesser']} lesser, "
                  f"{n_of(c['power'], 'power', 'powers')}; {c['great']} great")]
    for g in cos["gods"]:
        name = g.get("name") or "(its name is not spoken)"
        great = ", great" if g.get("great") else ""
        L.append(row("", f"{name}, \"{g.get('epithet') or '—'}\" — {g['rank']}{great}; "
                         f"{', '.join(domains.get(d, d) for d in g['domains'])}; {g['alignment']}"))
    after = cos.get("afterlife") or {}
    dead = label(P + "afterlife", after.get("row"))
    if after.get("judge") is not None:
        dead += f" (the judge: {gname(after['judge'])})"
    if after.get("plane") is not None:
        dead += f" (the land: {next((pl.get('name') for pl in cos['planes'] if pl['n'] == after['plane']), '—')})"
    L += [row("Where the dead go", dead), ""]

    L += ["## THE PLANES"]
    for pl in cos["planes"]:
        keeper = pl.get("keeper") or {}
        import design_cosmos as dcos
        kept = gname(keeper["god"]) if "god" in keeper else dcos.creature_name(keeper["creature"]) if keeper.get("creature") else "—"
        base = "the moon" if pl["baseline"] == "moon" else label(PL + "baseline", pl["baseline"])
        dev = label(PL + "deviation", pl["deviation"]).lower()
        if pl.get("merged_with"):
            partner = label(PL + "baseline", pl["merged_with"])
            partner = ("the " + partner[4:] if partner.startswith("The ")
                       else "the plane " + partner[0].lower() + partner[1:] if partner.startswith("Between ") else partner)
            dev += f" with {partner}"
        L.append(row(pl.get("name") or "—", f"{base} — {dev}; time: "
                                           f"{label(PL + 'time_rate', pl['rate']).lower()}; way in: {label(PL + 'way_in', pl['way']).lower()}; "
                                           f"cost: {label(PL + 'cost', pl['cost']).lower()}; keeper: {kept}"))
    L.append("")

    mag = cos["magic"]
    reg = mag.get("regulator") or {}
    # the roller writes a church as "the church of god <n>": the card says the god's name
    services = re.sub(r"\bgod (\d+)\b", lambda x: gname(int(x.group(1))), str(mag.get("services") or "—"))
    # the 22d audit: the signature institution by its name; the services once, when the regulator gives them
    inst = next((e.get("name") for e in proj.values() if e.get("type") == "signature" and e.get("slot") == "institution"), None)
    who = inst if reg.get("row") == "regulator_signature_institution" and inst else str(reg.get("who") or "—")
    if services in (str(reg.get("who")), who):
        services = "the regulator itself"
    L += ["## MAGIC", row("Source", label(M + "source", mag["source"])), row("Limits", label(M + "constraint", mag["constraint"])),
          row("Casting looks", label(M + "visibility", mag["visibility"])),
          row("Taboos", " · ".join(label(M + "taboo", t) for t in mag["taboos"])),
          row("Regulator", f"{who} ({mag.get('strictness') or '—'}); the services: {readable(services, proj)}"),
          row("Wild magic", label(M + "wild", mag["wild"])), ""]

    cal = cos["calendar"]
    year0 = int(cal["start_year"])
    st = cal["start"]
    L += ["## HISTORY", row("The ages", " → ".join(a.get("name") or "—" for a in cos["ages"]))]
    for e in sorted(cos["events"], key=lambda e: -(e.get("years_ago") or 0)):
        ago = e.get("years_ago")
        to_come = f"to come, in {st['days_to_next_step']} days" if st.get("days_to_next_step") else "to come"
        when = f"year {year0 - int(ago)}" if ago is not None else to_come if e.get("seat") == "move" else "—"
        L.append(row("", f"{when}: {e.get('name') or '—'}"))
    if cos.get("deep_events"):
        L.append(row("Before the record", " · ".join(e.get("name") or "—" for e in cos["deep_events"])))
    L.append("")

    months = cal.get("month_names") or []
    month = lambda n: months[n - 1] if months and 1 <= n <= len(months) else str(n)
    fests = " · ".join(f"{f.get('name') or '—'} ({f['day']} {month(f['month'])})"
                       for f in sorted((f for f in cal["festivals"] if f.get("month")), key=lambda f: (f["month"], f["day"])))
    dated = []
    for key, d in (cal.get("dated") or {}).items():
        when = f"{month(d['month'])} {d['year']}" if "day" not in d else f"{d['day']} {month(d['month'])} {d['year']}"
        dated.append(f"{key.replace('_', ' ')}: {when}")
    L += ["## THE CALENDAR", row("The year", f"{cal['months']} months of {cal['month_length']} days, a {cal['week_days']}-day week"),
          row("Months", ", ".join(months) or "—"), row("Days", ", ".join(cal.get("day_names") or []) or "—"),
          row("Climate", label(C + "climate", cal["climate"])),
          row("Moon", label(C + "moon", cal["moon"]) + (f": {', '.join(cal.get('moon_names') or [])}" if cal.get("moon_names") else "")),
          *([row("Months counted by", label(C + "underground_count", cal["underground_count"]))] if cal.get("underground_count") else []),
          row("Festivals", fests or "—")]
    if dated:
        L.append(row("Dated days", " · ".join(dated)))
    # the anchor once, with its day count where it has one (the 22d re-audit)
    anchor = (f"{st['after_move_days']} days after the move's last step" if st.get("after_move_days")
              else f"{st['days_to_next_step']} days before the move's next step" if st.get("days_to_next_step")
              else label(C + "start_anchor", cal["start_anchor"]).lower())
    L += [row("The start", f"{st['day']} {month(st['month'])} {st['year']} — {anchor}"), ""]

    L += card_tail(campaign, "P2", m, ph, mine, files, attempt, rnd, proj, P2_MOVES, [])
    return "\n".join(L) + "\n"


def write_card(campaign: str, phase: str, out: str | None) -> int:
    if phase not in dm.PHASES:
        print(f"design_approval: unknown phase {phase}", file=sys.stderr)
        return 2
    text = build_card(campaign, phase)
    names, sentences = secret_terms(campaign)
    hits = leaks_in(text, names, sentences)
    if hits:
        print("design_approval: card refused, it would leak: " + "; ".join(hits[:5]), file=sys.stderr)
        return 1
    path = Path(out) if out else design_dir(campaign) / "_approval" / f"{phase}.card.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    prev = previous_card(path)
    m = dm.load(campaign)
    attempt = int(m["phases"][phase].get("attempt") or 1)
    if prev and prev["attempt"] and prev["attempt"] != attempt:
        (path.parent / f"{phase}.attempt-{prev['attempt']}.card.md").write_text(prev["text"], encoding="utf-8", newline="\n")
    elif prev and prev["attempt"] == attempt and prev.get("round", 0) != card_round(m["phases"][phase]):
        (path.parent / f"{phase}.attempt-{attempt}.round-{prev.get('round', 0)}.card.md").write_text(prev["text"], encoding="utf-8", newline="\n")
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"design_approval: {phase} card written to {path} ({len(text)} chars, leak scan clean)")
    return 0


# ── the critique record ───────────────────────────────────────────────────────

def return_kind(file: str, entity: str, phase: str) -> str:
    """A critic return's kind, by the file it was saved as (birth 2: the skeleton critics returned entity_id "P4" and were
    counted as phase verdicts, the wishes critic's pass overwrote the phase critic's fix on the card)."""
    stem = Path(file).name.split(".critic", 1)[0]
    kind = "skeleton" if stem == "skeleton" else "wishes" if stem == "wishes" else "phase" if stem == "phase" \
        else "phase" if (entity == phase or entity.startswith("phase")) else "entity"
    return "skeleton" if kind == "entity" and entity.startswith("skeleton") else kind


def record_critique(campaign: str, phase: str, file: str, critic: int) -> int:
    try:
        ret = json.loads(Path(file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"design_approval: cannot read the return: {exc}", file=sys.stderr)
        return 1
    verdict = ret.get("verdict")
    entity = ret.get("entity_id")
    if verdict not in VERDICTS or not isinstance(entity, str) or not SLUG.match(entity):
        print("design_approval: a critic return needs entity_id and a verdict of pass / fix / rerun", file=sys.stderr)
        return 1
    # build item 14c: P1 of a birth whose rolls the script sealed has no `rerun`: only the owner rerolls; build item 22d: nor
    # has a script-rolled P2
    import design_cosmos_door as cd
    m_now = dm.load(campaign)
    sealed = (phase == "P1" and scripted_p1(m_now)) or (phase == "P2" and cd.applies(m_now))
    if sealed and (verdict == "rerun" or any(isinstance(f, dict) and f.get("verdict") == "rerun" for f in ret.get("findings") or [])):
        what = "premise" if phase == "P1" else "cosmology"
        print(f"design_approval: a {phase} critic return says `rerun`, refused: the rolls are sealed and only the owner rerolls; "
              f"the verdict is pass or fix (the {what} is rewritten on the same rolls)", file=sys.stderr)
        return 1
    findings = []
    terms = None
    redacted = 0
    for f in ret.get("findings") or []:
        if not isinstance(f, dict) or f.get("verdict") not in FINDING_VERDICTS:
            continue
        rid, fid, code = str(f.get("rubric_id", "")), str(f.get("entity_id", "")), str(f.get("reason_code", "") or "")
        if not (SLUG.match(rid) and SLUG.match(fid) and (not code or SLUG.match(code))):
            print(f"design_approval: a finding carries free text, refused ({rid[:20]}…)", file=sys.stderr)
            return 1
        # build item 18f (test birth P1-1, #8): a finding that is not a pass names its reason, a slug; null is refused
        if f["verdict"] != "pass" and not code:
            print(f"design_approval: a {f['verdict']} finding names its reason code (a slug), refused ({rid[:20]}…)", file=sys.stderr)
            return 1
        # ...and (#6) a code that carries a secret term never reaches the public record: it is kept as `secret_term`
        if code:
            terms = secret_code_terms(campaign) if terms is None else terms
            if carries_secret(code, terms):
                code, redacted = "secret_term", redacted + 1
        findings.append({"rubric_id": rid, "entity_id": fid, "verdict": f["verdict"], "reason_code": code or None})
    if redacted:
        print(f"design_approval: {redacted} reason code(s) carried a secret term; recorded as `secret_term`")
    # build item 19a (test birth P1-2): a critic judges its rubrics' questions only; a `fix` on a rubric it was not given is
    # its own taste, refused here (a fault no rubric asks about is a `note`)
    import design_prompts as dpm
    kind = return_kind(file, entity, phase)
    given = dpm.given_rubrics(phase, kind)
    if given is not None:
        stray = sorted({f["rubric_id"] for f in findings if f["verdict"] in ("fix", "rerun") and f["rubric_id"] not in given
                        and not (kind == "skeleton" and f["rubric_id"].startswith("rubric_skeleton_"))})
        if stray:
            print(f"design_approval: a fix names a rubric this critic was not given ({', '.join(stray)}), refused: a critic judges "
                  "its rubrics' questions only; a fault no rubric asks about is a `note`", file=sys.stderr)
            return 1
    # build item 12b: one entry per promise the critic judged: an id, a verdict and a slug; never prose (the reasoning
    # stays in the critic's own file, a secret promise's under dm-only)
    promises = []
    for e in ret.get("promises") or []:
        pid, note = str((e or {}).get("id", "")), str((e or {}).get("note", "") or "")
        if not isinstance(e, dict) or e.get("verdict") not in PROMISE_VERDICTS or not SLUG.match(pid) or (note and not SLUG.match(note)):
            print(f"design_approval: a promise verdict carries free text or no verdict, refused ({pid[:20]}…)", file=sys.stderr)
            return 1
        promises.append({"id": pid, "verdict": e["verdict"]})
    data = dm.load(campaign)
    ph = data["phases"].get(phase)
    if ph is None:
        return 2
    crit = ph.setdefault("critique", {"phase_loops": 0, "verdicts": [], "entity_loops_total": 0})
    stem = Path(file).name.split(".critic", 1)[0]       # the kind (return_kind, above) is the file the return was saved as
    loop = re.search(r"\.loop(\d+)\.json$", Path(file).name)
    crit.setdefault("records", []).append({"entity_id": entity if kind == "entity" else stem, "critic": critic, "verdict": verdict,
                                           "findings": findings, "kind": kind, "at": now_iso(),
                                           # build item 18f: the attempt and the loop, so a phase fix is served once
                                           "attempt": int(ph.get("attempt") or 1), "loop": int(loop.group(1)) if loop else 1})
    if kind == "skeleton":
        crit.setdefault("skeleton_verdicts", []).append(verdict)
    elif kind == "wishes":
        crit.setdefault("wishes_verdicts", []).append(verdict)
    elif kind == "phase":
        crit["verdicts"].append(verdict)
        if verdict == "fix":
            crit["phase_loops"] = int(crit.get("phase_loops") or 0) + 1
    else:
        row = data["entities"].setdefault(entity, {"phase": phase, "status": "pending", "attempt": 0, "critique_loops": 0,
                                                   "last_error": None, "file": None, "stage_file": None, "agent": None})
        if verdict == "fix":
            row["critique_loops"] = int(row.get("critique_loops") or 0) + 1
            crit["entity_loops_total"] = int(crit.get("entity_loops_total") or 0) + 1
        elif verdict == "pass" and row.get("status") in ("merged", "validated"):
            row["status"] = "critiqued"
    dm.save(campaign, data, f"design_approval.py critique --phase {phase}")
    print(f"design_approval: {phase} critic {critic} on {entity}: {verdict} ({len(findings)} findings recorded, ids and codes only)")
    if promises:
        import design_promises as dpr
        stored, ignored = dpr.judge(campaign, phase, promises)
        print(f"design_approval: {phase} promise verdicts: {stored} stored"
              + (f", {ignored} ignored (not this phase's critic-judged promises)" if ignored else ""))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="phase cards and critique records")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    c = sub.add_parser("card")
    c.add_argument("--phase", required=True)
    c.add_argument("--out")
    k = sub.add_parser("critique")
    k.add_argument("--phase", required=True)
    k.add_argument("--file", required=True)
    k.add_argument("--critic", type=int, default=1)
    lk = sub.add_parser("leak-check")
    lk.add_argument("file")
    a = ap.parse_args(argv)
    if a.verb == "card":
        return write_card(a.campaign, a.phase, a.out)
    if a.verb == "critique":
        return record_critique(a.campaign, a.phase, a.file, a.critic)
    if a.verb == "leak-check":
        names, sentences = secret_terms(a.campaign)
        hits = leaks_in(Path(a.file).read_text(encoding="utf-8"), names, sentences)
        print("design_approval: " + ("clean" if not hits else "LEAK: " + "; ".join(hits[:5])))
        return 1 if hits else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
