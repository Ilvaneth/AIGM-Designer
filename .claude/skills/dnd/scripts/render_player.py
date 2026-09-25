#!/usr/bin/env python3
"""
render_player.py — the player-facing files, built from the PUBLIC projection (plan item 11.3-11.6,
16.2, risk 24.1 #10; slice 1c item 5). Player files never carry an id: every [[id]] resolves to
the entity's name, and a link to a discoverable or secret entity fails the build. Every file is
scanned for secret names and dm-only sentences before it is written.

CLI:
  render_player.py -c CAMP primer [--out FILE]     assemble design/player-primer.md: the pitch, one section
                                                   per polity (the P8 section file plus the registry-built
                                                   headings), the backstory questions, the player map
  render_player.py -c CAMP facts                   merge design/_staging/P8/*.facts.json → common-knowledge.json
  render_player.py -c CAMP news [--day N]          merge design/_staging/P8/*.news.json → news.json (the day-0 slice)
  render_player.py -c CAMP thread-face THREAD_ID   design/player/<thread>.md: the thread's public face
  render_player.py -c CAMP resolve FILE            rewrite [[id]] → name in place; exit 1 on a hidden or unknown id
  render_player.py -c CAMP check FILE              leak scan; no [[ left; no hidden id in the text

Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_approval as da  # noqa: E402
import design_manifest as dm  # noqa: E402
from design_io import campaign_dir, design_dir, dm_only_dir, now_iso, read_json, stamp_meta, write_json_atomic  # noqa: E402

LINK = re.compile(r"\[\[([a-z]+_[a-z0-9_]+)\]\]")
SECTION_HEADINGS = ["The land and who rules it", "The gods as worshipped", "Calendar and festivals", "Money and prices",
                    "Languages and peoples", "Magic and its keepers", "Famous places", "History as taught",
                    "What everyone says is dangerous", "What people are talking about (day 0)"]


# ── sources ───────────────────────────────────────────────────────────────────

def public(campaign: str) -> dict:
    proj = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
    return {eid: e for eid, e in proj.items() if e.get("secrecy", "public") == "public"}


def all_ids(campaign: str) -> set:
    return set((read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {}))


def name_of(pub: dict, eid: str) -> str:
    return pub[eid]["name"] if eid in pub else eid


def resolve_text(text: str, pub: dict) -> tuple[str, list[str]]:
    bad = []

    def sub(m):
        eid = m.group(1)
        if eid in pub:
            return pub[eid]["name"]
        bad.append(eid)
        return m.group(0)
    return LINK.sub(sub, text), sorted(set(bad))


def hidden_ids_in(text: str, campaign: str, pub: dict) -> list[str]:
    hidden = all_ids(campaign) - set(pub)
    return sorted(h for h in hidden if re.search(r"(?<![\w])" + re.escape(h) + r"(?![\w])", text))


def check_text(campaign: str, text: str, pub: dict) -> list[str]:
    names, sentences = da.secret_terms(campaign)
    problems = da.leaks_in(text, names, sentences)
    left = LINK.findall(text)
    if left:
        problems.append(f"unresolved links: {', '.join(sorted(set(left))[:5])}")
    hidden = hidden_ids_in(text, campaign, pub)
    if hidden:
        problems.append(f"hidden ids named: {len(hidden)}")
    return problems


def write_player_file(campaign: str, path: Path, text: str, pub: dict) -> int:
    problems = check_text(campaign, text, pub)
    if problems:
        print(f"render_player: {path.name} refused: " + "; ".join(problems), file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"render_player: wrote {path} ({len(text)} chars, clean)")
    return 0


def staged(campaign: str, phase: str, suffix: str) -> list[Path]:
    base = design_dir(campaign) / "_staging" / phase
    out = list(base.glob(f"*{suffix}")) + list((base / "merged").glob(f"*{suffix}")) if base.is_dir() else []
    return sorted(out)


# ── the primer ────────────────────────────────────────────────────────────────

def band_tier(manifest: dict) -> int:
    lo = int(manifest["dials"]["level_band"][0])
    return 1 if lo <= 4 else 2 if lo <= 10 else 3 if lo <= 16 else 4


def by_type(pub: dict, etype: str) -> list[tuple[str, dict]]:
    return sorted(((eid, e) for eid, e in pub.items() if e.get("type") == etype), key=lambda x: x[1].get("name", ""))


def primer_text(campaign: str) -> tuple[str, dict]:
    manifest = dm.load(campaign)
    pub = public(campaign)
    calendar = read_json(campaign_dir(campaign) / "calendar.json") or {}
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    news = (read_json(design_dir(campaign) / "news.json") or {}).get("records", [])
    mp = read_json(design_dir(campaign) / "map.json") or {}
    premise = next((e for _, e in by_type(pub, "premise")), {})
    title = premise.get("name") or campaign.replace("-", " ").title()
    lines = [f"# {title} — bir yerlinin bildikleri", "",
             "*Bu dosya oyuncuya tamamen açıktır: dünyayı bu dünyada büyümüş birinin bildiği kadar anlatır. Her bölüm bir ülke ya da halk içindir; bir yerli komşusunu daha az bilir.*", "",
             "## The pitch", "", premise.get("pitch_tr") or "(premise fazı henüz pitch yazmadı)", ""]
    problems: list[str] = []
    tier = band_tier(manifest)
    polities = by_type(pub, "polity")
    if not polities:
        polities = [("polity_all", {"name": "Bu diyar", "capital": None})]
    for pid, pol in polities:
        lines.append(f"## {pol.get('name')} — buradan olan karakterler için")
        lines.append("")
        section_files = [p for p in staged(campaign, "P8", ".section.md") if p.name.startswith(f"primer_{pid}")]
        if section_files:
            text, bad = resolve_text(section_files[-1].read_text(encoding="utf-8").replace("\r\n", "\n").strip(), pub)
            problems += [f"{section_files[-1].name}: {b}" for b in bad]
            lines += [text, ""]
        else:
            lines += ["*(bu kültürün bölümü henüz yazılmadı)*", ""]
        # the land
        regions = [(rid, r) for rid, r in by_type(pub, "region") if r.get("polity") == pid or pid == "polity_all"]
        settlements = [(sid, s) for sid, s in by_type(pub, "settlement") if s.get("polity") == pid or pid == "polity_all"]
        lines.append("### The land and who rules it")
        cap = name_of(pub, pol.get("capital")) if pol.get("capital") else "—"
        ruler = name_of(pub, pol.get("ruler_at_birth")) if pol.get("ruler_at_birth") else "—"
        lines.append(f"- **{pol.get('name')}**: yönetim {pol.get('government', '—')}, başkent {cap}, hükümdar {ruler}, hukuk {pol.get('law_level', '—')}.")
        for rid, r in regions:
            lines.append(f"- **{r['name']}** ({r.get('biome', '')}): {r.get('identity_tr', '')}")
        for sid, s in settlements:
            lines.append(f"- {s['name']} — {s.get('scale', '')}, ~{s.get('population', '?')} kişi, {name_of(pub, s['region']) if s.get('region') else ''}")
        lines.append("")
        # the gods
        lines.append("### The gods as worshipped")
        for gid, g in by_type(pub, "god"):
            epithet = f", \"{g['aliases'][0]}\"" if g.get("aliases") else ""
            church = name_of(pub, g["church"]) if isinstance(g.get("church"), str) else (g.get("church") or "—")
            lines.append(f"- **{g['name']}**{epithet} — {', '.join(g.get('domains') or [])}; simgesi {g.get('symbol', '—')}; {church}.")
        lines.append("")
        # calendar
        lines.append("### Calendar and festivals")
        if calendar.get("months"):
            lines.append(f"- Aylar (her biri {calendar.get('month_length', 30)} gün): {', '.join(calendar['months'])}")
        if calendar.get("day_names"):
            lines.append(f"- Günler: {', '.join(calendar['day_names'])}")
        for moon in calendar.get("moons") or []:
            lines.append(f"- Ay: {moon.get('name')}, {moon.get('cycle')} günlük döngü")
        for f in calendar.get("festivals") or []:
            god = name_of(pub, f["god"]) if f.get("god") else ""
            month = calendar["months"][f["month"] - 1] if calendar.get("months") and isinstance(f.get("month"), int) and 0 < f["month"] <= len(calendar["months"]) else f.get("month")
            lines.append(f"- **{f.get('name')}** ({f.get('day')} {month}{', ' + god if god else ''}): {f.get('note', '')}")
        lines.append("")
        # money
        lines.append("### Money and prices")
        for sid, s in settlements:
            eco = s.get("economy") or {}
            lines.append(f"- {s['name']}: satar {', '.join(eco.get('sells') or []) or '—'}; arar {', '.join(eco.get('needs') or []) or '—'}; fiyat çarpanı ×{eco.get('price_modifier', 1.0)}")
        lines.append("")
        # languages and peoples
        lines.append("### Languages and peoples")
        langs = naming.get("languages") or {}
        for lid, lang in langs.items():
            lines.append(f"- **{lid}**: {lang.get('label_tr', '')}")
        for cid, c in by_type(pub, "signature"):
            if c.get("kind") == "creature":
                lines.append(f"- **{c['name']}**: {c.get('rule_tr', '')}")
        lines.append("")
        # magic
        lines.append("### Magic and its keepers")
        for cid, c in by_type(pub, "signature"):
            if c.get("kind") in ("magic", "institution"):
                lines.append(f"- **{c['name']}**: {c.get('rule_tr', '')}")
        lines.append("")
        # famous places
        lines.append("### Famous places")
        for plid, pl in by_type(pub, "place")[:12]:
            lines.append(f"- **{pl['name']}** ({pl.get('kind', '')}, {name_of(pub, pl['settlement']) if pl.get('settlement') else ''})")
        for node in (mp.get("nodes") or []):
            if node.get("kind") == "landmark" and node.get("secrecy", "public") == "public":
                lines.append(f"- {node['id'].replace('landmark_', '').replace('_', ' ').title()} — bir simge yer")
        lines.append("")
        # taught history
        lines.append("### History as taught")
        for evid, ev in sorted(by_type(pub, "event"), key=lambda x: (x[1].get("year") if isinstance(x[1].get("year"), int) else -99999)):
            lines.append(f"- {ev.get('year', '?')} — **{ev['name']}**: {ev.get('taught_tr', '')}")
        lines.append("")
        # dangerous places
        lines.append("### What everyone says is dangerous")
        shown = 0
        for sid, s in by_type(pub, "site"):
            if int(s.get("danger_tier") or 0) > tier and s.get("telegraphs"):
                far = next((t for t in s["telegraphs"] if t.get("distance") == "far"), s["telegraphs"][0])
                lines.append(f"- {far.get('text_tr', '')}")
                shown += 1
        if not shown:
            lines.append("- (herkesin uzak durduğu bir yer henüz yok)")
        lines.append("")
        # rumours
        lines.append("### What people are talking about (day 0)")
        reach_ids = {pid} | {rid for rid, _ in regions} | {sid for sid, _ in settlements}
        shown = 0
        for rec in news:
            if rec.get("day", 0) == 0 and rec.get("visibility") in ("public", "rumored") and (set(rec.get("reach") or []) & reach_ids or pid == "polity_all"):
                lines.append(f"- {rec.get('line_tr', '')}")
                shown += 1
        if not shown:
            lines.append("- (henüz söylenti yok)")
        lines.append("")
    lines.append("## Questions for your backstory")
    lines.append("*İstediklerini cevapla; her biri DM'e hikâyeni bağlayacağı bir yer verir. Hiçbiri tuzak değildir.*")
    lines.append("")
    for sid, s in by_type(pub, "socket"):
        if s.get("question_tr"):
            lines.append(f"- {s['question_tr']}")
    lines.append("")
    lines.append("## The player map")
    for node in (mp.get("nodes") or []):
        if node.get("secrecy", "public") == "public" and node.get("kind") in ("settlement", "landmark", "waypoint", "site"):
            lines.append(f"- {name_of(pub, node['id']) if node['id'] in pub else node['id']} — {node.get('kind')}, {node.get('terrain', '')}, {name_of(pub, node['region']) if node.get('region') in pub else ''}")
    lines.append("")
    lines.append(f"*Üretildi: {now_iso()} — render_player.py primer*")
    text = "\n".join(lines) + "\n"
    text, bad = resolve_text(text, pub)
    problems += bad
    return text, {"problems": problems, "pub": pub}


def cmd_primer(campaign: str, out: str | None) -> int:
    text, info = primer_text(campaign)
    if info["problems"]:
        print("render_player: primer refused, links to hidden or unknown entities: " + ", ".join(info["problems"][:8]), file=sys.stderr)
        return 1
    path = Path(out) if out else design_dir(campaign) / "player-primer.md"
    return write_player_file(campaign, path, text, info["pub"])


# ── facts and news ────────────────────────────────────────────────────────────

def cmd_facts(campaign: str) -> int:
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    facts, n = [], 0
    for path in staged(campaign, "P8", ".facts.json"):
        doc = read_json(path) or {}
        for f in (doc.get("facts") if isinstance(doc, dict) else doc) or []:
            refs = list(f.get("refs") or [])
            for r in refs:
                if r not in canonical:
                    print(f"render_player: {path.name}: unknown ref {r}", file=sys.stderr)
                    return 1
                if canonical[r].get("secrecy") == "secret":
                    print(f"render_player: {path.name}: a common-knowledge fact may not reference a secret entity", file=sys.stderr)
                    return 1
            n += 1
            facts.append({"id": f"ck_{n:03d}", "keywords": [k.lower() for k in (f.get("keywords") or [])],
                          "text_tr": f.get("text_tr", ""), "origin": f.get("origin") or "all", "refs": refs})
    out = {"_meta": {}, "facts": facts}
    stamp_meta(out, campaign, "render_player.py facts")
    out["_meta"]["schema_version"] = 1
    write_json_atomic(campaign_dir(campaign) / "common-knowledge.json", out)
    print(f"render_player: common-knowledge.json written with {len(facts)} facts")
    return 0


def cmd_news(campaign: str, day: int) -> int:
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    path = design_dir(campaign) / "news.json"
    doc = read_json(path) or {"_meta": {"schema_version": 1, "campaign": campaign, "next_id": 1, "last_day": 0}, "records": []}
    next_id = int(doc["_meta"].get("next_id") or (len(doc["records"]) + 1))
    added = 0
    for frag in staged(campaign, "P8", ".news.json"):
        fdoc = read_json(frag) or {}
        for r in (fdoc.get("records") if isinstance(fdoc, dict) else fdoc) or []:
            if r.get("visibility") not in ("public", "rumored"):
                print(f"render_player: {frag.name}: a birth rumour is public or rumored, never secret", file=sys.stderr)
                return 1
            for ref in r.get("refs") or []:
                if ref not in canonical or canonical[ref].get("secrecy") == "secret":
                    print(f"render_player: {frag.name}: bad or secret ref {ref}", file=sys.stderr)
                    return 1
            doc["records"].append({"id": f"news_{next_id:04d}", "day": day, "source": "birth", "faction": r.get("faction"),
                                   "move": None, "outcome": None, "roll": None, "region": r.get("region"),
                                   "settlement": r.get("settlement"), "visibility": r["visibility"], "kind": r.get("kind") or "rumour",
                                   "line_tr": r.get("line_tr", ""), "refs": list(r.get("refs") or []),
                                   "reach": list(r.get("reach") or []), "secrecy": r["visibility"] if r["visibility"] == "public" else "discoverable",
                                   "seen_by_party": False, "parked_as": None, "step": None})
            next_id += 1
            added += 1
    doc["_meta"]["next_id"] = next_id
    doc["_meta"]["last_day"] = max(int(doc["_meta"].get("last_day") or 0), day)
    stamp_meta(doc, campaign, "render_player.py news")
    doc["_meta"]["schema_version"] = 1
    write_json_atomic(path, doc)
    print(f"render_player: news.json +{added} records (day {day}, next_id {next_id})")
    return 0


# ── thread face, resolve, check ─────────────────────────────────────────────────

def cmd_thread_face(campaign: str, thread_id: str) -> int:
    pub = public(campaign)
    src = design_dir(campaign) / "threads" / f"{thread_id}.md"
    if not src.is_file():
        print(f"render_player: no thread file {src}", file=sys.stderr)
        return 1
    text = src.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.search(r"^## Public\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    body = (m.group(1) if m else "").strip()
    title = re.search(r"^# (.+)$", text, re.M)
    face = f"# {title.group(1) if title else thread_id} — oyuncunun gördüğü yüz\n\n{body}\n\n*Üretildi: {now_iso()} — render_player.py thread-face*\n"
    face, bad = resolve_text(face, pub)
    if bad:
        print(f"render_player: the public face links to hidden entities: {', '.join(bad)}", file=sys.stderr)
        return 1
    return write_player_file(campaign, design_dir(campaign) / "player" / f"{thread_id}.md", face, pub)


def cmd_resolve(campaign: str, file: str) -> int:
    pub = public(campaign)
    path = Path(file)
    text, bad = resolve_text(path.read_text(encoding="utf-8"), pub)
    if bad:
        print(f"render_player: cannot resolve hidden or unknown ids: {', '.join(bad)}", file=sys.stderr)
        return 1
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"render_player: resolved {path.name}")
    return 0


def cmd_check(campaign: str, file: str) -> int:
    pub = public(campaign)
    problems = check_text(campaign, Path(file).read_text(encoding="utf-8"), pub)
    print("render_player: " + ("clean" if not problems else "PROBLEMS: " + "; ".join(problems)))
    return 1 if problems else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="player-facing files from the public projection")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    p = sub.add_parser("primer")
    p.add_argument("--out")
    sub.add_parser("facts")
    n = sub.add_parser("news")
    n.add_argument("--day", type=int, default=0)
    t = sub.add_parser("thread-face")
    t.add_argument("thread_id")
    r = sub.add_parser("resolve")
    r.add_argument("file")
    c = sub.add_parser("check")
    c.add_argument("file")
    a = ap.parse_args(argv)
    if a.verb == "primer":
        return cmd_primer(a.campaign, a.out)
    if a.verb == "facts":
        return cmd_facts(a.campaign)
    if a.verb == "news":
        return cmd_news(a.campaign, a.day)
    if a.verb == "thread-face":
        return cmd_thread_face(a.campaign, a.thread_id)
    if a.verb == "resolve":
        return cmd_resolve(a.campaign, a.file)
    if a.verb == "check":
        return cmd_check(a.campaign, a.file)
    return 2


if __name__ == "__main__":
    sys.exit(main())
