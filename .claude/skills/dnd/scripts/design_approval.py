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
from design_io import campaign_dir, design_dir, dm_only_dir, now_iso, read_json  # noqa: E402

PHASE_TITLES = {"P0": "kadranlar", "P1": "premise", "P2": "kozmos", "P3": "topraklar", "P4": "güçler",
                "P5": "insanlar", "P6": "mekânlar", "P7": "ark", "P8": "primer ve kapanış", "P9": "entegrasyon"}
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
    for path in dm_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for s in re.split(r"(?<=[.!?])\s+|\n", text):
            s = s.strip().strip("-*# ").strip()
            if len(s) >= 40 and not s.startswith(("|", "`", "[[", "entity:", "mirror", "covers", "stamped")):
                sentences.append(s)
    return names, sentences


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
    return {"ids": set(filter(None, (ids.group(1).split(",") if ids else []))),
            "names": dict(x.split("=", 1) for x in (names.group(1).split("|") if names and names.group(1) else []) if "=" in x),
            "attempt": int(attempt.group(1)) if attempt else 0, "text": text}


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
    for kind, label in (("must", "olsun"), ("must_not", "olmasın")):
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
    klass = (row or {}).get("hides_in", "bilinmiyor")
    try:
        import design_dice as dd
        gone = dd.rows_used_elsewhere(campaign, "secrets.yaml#archetype")
    except Exception:
        gone = set()
    novel = "evet" if arche and arche not in gone else "hayır" if arche else "?"
    clues_by_act: dict = {}
    for ent in canonical(campaign).values():
        if ent.get("type") == "premise":
            for c in (ent.get("dm_only") or {}).get("clues") or []:
                clues_by_act[c.get("act")] = clues_by_act.get(c.get("act"), 0) + 1
    clue_line = ", ".join(f"perde {a}: {n}" for a, n in sorted(clues_by_act.items(), key=lambda x: str(x[0]))) or "henüz yerleştirilmedi"
    recs = [r for r in (ph.get("critique", {}).get("records") or []) if r.get("entity_id", "").startswith("premise_")]
    by_critic = {r.get("critic"): r.get("verdict") for r in recs}
    agreement = "uyumlu" if len(by_critic) >= 2 and len(set(by_critic.values())) == 1 else "farklı" if len(by_critic) >= 2 else "tek eleştirmen"
    return [f"- **Sır katmanı (spoiler'sız):** arketip sınıfı *{klass}* · yeni mi (used.json): {novel} · ipuçları: {clue_line} · eleştirmenler: {agreement}"]


def map_lines(campaign: str) -> list[str]:
    mp = read_json(design_dir(campaign) / "map.json") or {}
    nodes = [n for n in mp.get("nodes") or [] if n.get("secrecy", "public") == "public"]
    hubs = [n["id"] for n in nodes if n.get("hub")]
    lines = [f"- **Oyuncu haritası (metin):** {len(nodes)} açık düğüm, merkez: {', '.join(hubs) or '—'}"]
    for n in nodes[:20]:
        lines.append(f"  - {n['id']} ({n.get('kind')}, {n.get('terrain', '')}) @ {n.get('x')},{n.get('y')}")
    return lines


def build_card(campaign: str, phase: str) -> str:
    m = dm.load(campaign)
    ph = m["phases"][phase]
    proj = projection(campaign)
    canon = canonical(campaign)
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    assignments = naming.get("assignments") or {}
    scale = dt.scale_row(m["dials"]["scale"])
    roster = ph.get("roster") or []
    mine = {eid: e for eid, e in proj.items() if e.get("created_phase") == phase or eid in roster}
    attempt = int(ph.get("attempt") or 1)

    lines = [f"# Faz kartı — {phase} ({PHASE_TITLES.get(phase, phase)}) · {campaign} · deneme {attempt}",
             f"<!-- attempt: {attempt} -->", f"<!-- ids: {','.join(sorted(mine))} -->",
             "<!-- names: " + "|".join(f"{eid}={e.get('name', '')}" for eid, e in sorted(mine.items())) + " -->", ""]
    val = ph.get("validator") or {}
    crit = ph.get("critique") or {}
    failed = [e for e in roster if m["entities"].get(e, {}).get("status") == "failed"]
    incomplete = [e for e in roster if dm.ENTITY_RANK.get(m["entities"].get(e, {}).get("status", "pending"), 0) < dm.ENTITY_RANK["merged"]]
    missing = sum(1 for v in crit.get("verdicts") or [] if v == "critique_missing")
    chains, phase_verdict, phase_lines, wishes_verdict, skeleton_verdicts = critique_chains(dict(ph, id=phase))
    tokens_out = int((ph.get("tokens") or {}).get("out") or 0)
    lines.append(f"- **Durum:** {ph['status']} · **Doğrulayıcı:** {val.get('errors', '—')} hata, {val.get('warnings', '—')} uyarı · "
                 f"**Başarısız:** {', '.join(failed) or '—'} · **Süre:** {elapsed_minutes(ph)} dk · "
                 f"**Çıktı:** {f'{tokens_out:,}'.replace(',', '.') + ' token' if tokens_out else '—'}")
    lines.append(f"- **Eleştiri:** faz eleştirmeni {phase_verdict} · dilek eleştirmeni {wishes_verdict}"
                 + (f" · iskelet {' → '.join(skeleton_verdicts)}" if skeleton_verdicts else "")
                 + f" · varlık düzeltme döngüsü {crit.get('entity_loops_total', 0)}"
                 + (f" · eleştiri eksik {missing}" if missing else ""))
    for pl in phase_lines[:8]:
        lines.append(f"  - faz eleştirmeni: {pl}")
    if incomplete:
        lines.append(f"- ⚠ **Eksik:** {', '.join(incomplete)} — faz tamamlanmadı; kayıt defterine girmeyen varlık var, bu kart onaylanamaz "
                     "(`phase begin --json` + fan-out, ya da `drop`).")
    # scale band, script-side with the full count; the card prints the public count and a tick
    band_lines = []
    for etype, key in BAND_KEYS.get(phase, []):
        full = sum(1 for e in canon.values() if e.get("type") == etype)
        public = sum(1 for e in proj.values() if e.get("type") == etype)
        lo, hi = dt.band(dig(scale, key))
        ok = lo <= full <= hi
        band_lines.append(f"{etype}: {public} açık, bant {lo}-{hi} {'✓' if ok else '✗'}")
    if band_lines:
        lines.append("- **Ölçek bandı:** " + " · ".join(band_lines))
    wl = wish_ticks(ph, m["dials"].get("wishes") or {})
    if wl:
        lines.append("- **Dilekler:** " + " · ".join(wl))
    if phase == "P1":
        lines += secret_abstract(campaign, ph)
    if ph.get("directions"):
        lines.append("- **Yönler (önceki turlardan):** " + " · ".join(ph["directions"]))
    lines.append("")

    languages = list((naming.get("languages") or {}).keys())
    default_lang = languages[0] if len(languages) == 1 else "—"
    lines.append("## Bu fazda doğanlar (herkese açık)")
    lines.append("| id | ad | tür | dil | eleştiri | bir satır |")
    lines.append("|---|---|---|---|---|---|")
    for eid, e in sorted(mine.items()):
        lines.append(f"| {eid} | {e.get('name', '')} | {e.get('type', '')} | {language_of(eid, e, assignments, proj, default_lang)} | "
                     f"{' → '.join(chains.get(eid) or []) or '—'} | {(e.get('summary') or '').replace('|', '/')} |")
    if not mine:
        lines.append("| — | — | — | — | — | (bu faz henüz varlık üretmedi) |")
    lines.append("")

    if phase == "P3":
        lines += map_lines(campaign)
        lines.append("")

    lines.append("## Bir yerlinin bildiği")
    shown = 0
    for eid, e in sorted(mine.items()):
        if e.get("summary") and e.get("secrecy", "public") == "public":
            lines.append(f"- {e['name']}: {e['summary']}")
            shown += 1
            if shown >= 8:
                break
    if not shown:
        lines.append("- (henüz yok)")
    lines.append("")

    per_module, findings = validator_summary(campaign, phase)
    lines.append("## Doğrulayıcı (özet, kısaltılmış)")
    if per_module:
        for mod, c in sorted(per_module.items()):
            lines.append(f"- {mod}: {c['error']} hata, {c['warning']} uyarı")
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
        lines.append(f"## Önceki karta göre değişiklik (deneme {prev['attempt']} → {attempt})")
        lines.append(f"- eklendi: {', '.join(added) or '—'}")
        lines.append(f"- çıkarıldı: {', '.join(removed) or '—'}")
        lines.append(f"- adı değişti: {', '.join(renamed) or '—'}")
        lines.append("")

    lines.append("## Onay")
    if m["_meta"].get("auto_approve"):
        lines.append("- Test doğumu: kart otomatik onaylanır (owner kararı 2026-09-25).")
    else:
        lines.append("- Onaylamak için tam olarak `onay` yaz; bir düzeltme tek cümledir (en çok üç tur). Sonraki faz `devam` ile başlar.")
    lines.append(f"- Üretildi: {now_iso()}")
    return "\n".join(lines) + "\n"


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
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"design_approval: {phase} card written to {path} ({len(text)} chars, leak scan clean)")
    return 0


# ── the critique record ───────────────────────────────────────────────────────

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
    findings = []
    for f in ret.get("findings") or []:
        if not isinstance(f, dict) or f.get("verdict") not in FINDING_VERDICTS:
            continue
        rid, fid, code = str(f.get("rubric_id", "")), str(f.get("entity_id", "")), str(f.get("reason_code", "") or "")
        if not (SLUG.match(rid) and SLUG.match(fid) and (not code or SLUG.match(code))):
            print(f"design_approval: a finding carries free text, refused ({rid[:20]}…)", file=sys.stderr)
            return 1
        findings.append({"rubric_id": rid, "entity_id": fid, "verdict": f["verdict"], "reason_code": code or None})
    data = dm.load(campaign)
    ph = data["phases"].get(phase)
    if ph is None:
        return 2
    crit = ph.setdefault("critique", {"phase_loops": 0, "verdicts": [], "entity_loops_total": 0})
    # birth 2: the skeleton critics returned entity_id "P4" and were counted as phase verdicts, the wishes critic's
    # pass overwrote the phase critic's fix on the card — the kind is the file the return was saved as
    stem = Path(file).name.split(".critic", 1)[0]
    kind = "skeleton" if stem == "skeleton" else "wishes" if stem == "wishes" else "phase" if stem == "phase" \
        else "phase" if (entity == phase or entity.startswith("phase")) else "entity"
    if kind == "entity" and entity.startswith("skeleton"):
        kind = "skeleton"
    crit.setdefault("records", []).append({"entity_id": entity if kind == "entity" else stem, "critic": critic, "verdict": verdict,
                                           "findings": findings, "kind": kind, "at": now_iso()})
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
