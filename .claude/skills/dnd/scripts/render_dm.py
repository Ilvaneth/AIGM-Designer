#!/usr/bin/env python3
"""
render_dm.py — the DM's hot-path files, generated from the public projection ⊕ overlay.

Plan item 16.1-16.2, 16.6, P8 ("indexes, world.md, npcs.md, lean state.md, report.md by script"); slice 1d.
world.md and npcs.md are never hand-edited: the registry is the single source, the overlay carries what play
changed, and every overlaid value prints with a "changed since birth" marker. They are DM-open, player-avoid
(public + discoverable rows; secret entities never appear).

  render_dm.py -c CAMP world             world.md — the world at a glance
  render_dm.py -c CAMP npcs              npcs.md — the full NPC index table
  render_dm.py -c CAMP index             design/index.md — one table per type (id, name, aliases, file, status,
                                         seen_in_play, region, one line): "was this ever designed?" in one place
  render_dm.py -c CAMP state [--force]   a lean state.md (only when none exists, or --force)
  render_dm.py -c CAMP report            design/report.md — the birth report's public part
  render_dm.py -c CAMP all [--force]     all of the above (state only when missing, or --force)

Exit codes: 0 ok · 1 no projection · 2 usage
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import campaign_dir, design_dir, load_overlay, now_iso, read_json  # noqa: E402

BIRTH_DEFAULTS = {"alive": "alive", "status": "skeleton", "seen_in_play": False}
INDEX_ORDER = ("polity", "region", "settlement", "district", "place", "faction", "npc", "site", "item", "creature",
               "god", "plane", "era", "event", "premise", "signature", "break", "arc", "beat", "chapter", "node",
               "seed", "socket", "pc", "thread")


# ── sources ───────────────────────────────────────────────────────────────────

def projection(campaign: str) -> dict:
    return (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})


def by_type(pub: dict, etype: str) -> list[tuple[str, dict]]:
    return sorted(((eid, e) for eid, e in pub.items() if e.get("type") == etype), key=lambda kv: kv[0])


def name_of(pub: dict, eid) -> str:
    if isinstance(eid, str):
        return pub.get(eid, {}).get("name") or eid
    return "—"


def ov(overlay: dict, eid: str, field: str):
    """(value, changed, record) — the overlay's current value or None."""
    rec = ((overlay.get("entries") or {}).get(eid) or {}).get(field)
    if not rec:
        return None, False, None
    # the registry row may carry no value for the field (an npc is alive unless the overlay says otherwise), so a
    # None birth reads as the field's default; a birth-detailed site is written by registry.py merge with birth
    # "skeleton" and value "detailed", which is the birth, not a change: only play-time writers move the marker
    birth = rec.get("birth")
    if birth is None:
        birth = BIRTH_DEFAULTS.get(field)
    rec = dict(rec, birth=birth)
    changed = rec.get("value") != birth and rec.get("writer") != "registry.py merge"
    return rec.get("value"), changed, rec


def marked(pub: dict, overlay: dict, eid: str, field: str, birth_value, as_name: bool = True) -> str:
    """The current value with a marker when the overlay changed it since birth."""
    val, changed, rec = ov(overlay, eid, field)
    current = val if rec else birth_value
    text = name_of(pub, current) if as_name else (str(current) if current is not None else "—")
    if changed:
        was = name_of(pub, rec.get("birth")) if as_name else str(rec.get("birth"))
        return f"{text} *(değişti: doğumda {was}, gün {rec.get('day')})*"
    return text


def short(text, n: int = 90) -> str:
    text = str(text or "").replace("|", "/").replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def band_tier(manifest: dict) -> int:
    band = (manifest.get("dials") or {}).get("level_band") or [1, 5]
    return 1 if band[1] <= 5 else 2 if band[1] <= 10 else 3 if band[1] <= 15 else 4


def today_line(calendar: dict) -> str:
    months = calendar.get("months") or []
    m = calendar.get("month")
    mname = months[m - 1] if isinstance(m, int) and 0 < m <= len(months) else m
    return f"{calendar.get('day', '?')} {mname} {calendar.get('year', '?')}"


# ── world.md ──────────────────────────────────────────────────────────────────

def world_text(campaign: str) -> str:
    pub = projection(campaign)
    m = dm.load(campaign)
    overlay = load_overlay(campaign)
    calendar = read_json(campaign_dir(campaign) / "calendar.json") or {}
    factions_store = (read_json(campaign_dir(campaign) / "factions.json") or {}).get("factions") or {}
    d = m.get("dials") or {}
    premise = next((e for _, e in by_type(pub, "premise")), {})
    L = [f"# World: {campaign}", f"**Generated:** {date.today().isoformat()} (from the public projection ⊕ overlay; never hand-edited — `render_dm.py world`)", "",
         "## Campaign Tone & Genre",
         f"- **Tone:** {d.get('tone', '—')} · **Magic level:** {d.get('magic', '—')} · **Setting type:** {d.get('era', '—')} · **Danger level:** {d.get('danger', '—')} · **Scale:** {d.get('scale', '—')}"]
    if premise.get("summary"):
        L.append(f"- **Premise:** {premise['summary']}")
    if premise.get("question_tr"):
        L.append(f"- **The question:** {premise['question_tr']}")
    L += ["", "## World at a glance"]
    for pid, p in by_type(pub, "polity"):
        ruler = marked(pub, overlay, pid, "ruler", p.get("ruler_at_birth"))
        L.append(f"- **Polity:** {p['name']} — {p.get('government', '—')}, hükümdar {ruler}, başkent {name_of(pub, p.get('capital'))}"
                 + (f" (`{p['file']}`)" if p.get("file") else ""))
    for rid, r in by_type(pub, "region"):
        L.append(f"- **Region:** {r['name']}, T{r.get('danger_tier', '?')} — {r.get('biome', '')}; {short(r.get('identity_tr') or r.get('summary'), 120)}")
    settlements = by_type(pub, "settlement")
    if settlements:
        parts = []
        for sid, s in settlements:
            ctrl_val, ctrl_changed, _ = ov(overlay, sid, "control")
            ruler = marked(pub, overlay, sid, "ruler", s.get("ruler_at_birth"))
            parts.append(f"{s['name']} ({s.get('scale', '')}, {s.get('population', '?')}; {ruler}"
                         + (f"; kontrol {name_of(pub, ctrl_val)}" + (" *(değişti)*" if ctrl_changed else "") if ctrl_val else "") + ")")
        L.append("- **Settlements:** " + " · ".join(parts))
    gods = by_type(pub, "god")
    if gods:
        L.append("- **Gods:** " + ", ".join(f"{g['name']} ({', '.join(g.get('domains') or [])})" for _, g in gods) + " — `design/cosmology.md`")
    sigs = by_type(pub, "signature")
    if sigs:
        L.append("- **Signatures:** " + " · ".join(f"{s['name']}" + (f" ({short(s.get('rule_tr'), 60)})" if s.get("rule_tr") else "") for _, s in sigs))
    breaks = by_type(pub, "break")
    if breaks:
        L.append("- **Trope breaks:** " + " · ".join(b["name"] for _, b in breaks))
    if calendar.get("months"):
        fests = ", ".join(f"{f.get('name')} ({f.get('day')} {calendar['months'][f['month'] - 1] if isinstance(f.get('month'), int) and 0 < f['month'] <= len(calendar['months']) else f.get('month')})"
                          for f in (calendar.get("festivals") or [])[:4])
        L.append(f"- **Calendar:** {len(calendar['months'])} ay × {calendar.get('month_length', 30)} gün; bugün {today_line(calendar)}" + (f"; {fests}" if fests else ""))
    L.append(f"- **Threat arc stage:** {overlay.get('_meta', {}).get('threat_stage', 1)}" + (f" · doom day {overlay['_meta']['doom_day']}" if overlay.get("_meta", {}).get("doom_day") else ""))
    L += ["", "## Factions (public face)", "| Faction | Archetype | Leader | HQ | Stance to party |", "|---|---|---|---|---|"]
    for fid, f in by_type(pub, "faction"):
        store = factions_store.get(fid) if isinstance(factions_store, dict) else next((x for x in factions_store if x.get("id") == fid), None)
        stance = (store or {}).get("stances", {}).get("party", 0) if store else 0
        hq = marked(pub, overlay, f.get("hq"), "control", None) if False else name_of(pub, f.get("hq"))
        L.append(f"| {f['name']} | {f.get('archetype', '—')} | {name_of(pub, f.get('leader'))} | {hq} | {stance:+d} |" if isinstance(stance, int)
                 else f"| {f['name']} | {f.get('archetype', '—')} | {name_of(pub, f.get('leader'))} | {hq} | {stance} |")
    sites = by_type(pub, "site")
    if sites:
        L += ["", "## Sites (directory)", "| Site | Tier | Rooms | Status | Region | One line |", "|---|---|---|---|---|---|"]
        for sid, s in sites:
            status = marked(pub, overlay, sid, "status", "skeleton", as_name=False)
            L.append(f"| {s['name']} | T{s.get('danger_tier', '?')} | {s.get('room_count', '?')} | {status} | {name_of(pub, s.get('region'))} | {short(s.get('summary'), 80)} |")
    tier = band_tier(m)
    warnings = []
    for sid, s in sites:
        if int(s.get("danger_tier") or 0) > tier and s.get("telegraphs"):
            far = next((t for t in s["telegraphs"] if t.get("distance") == "far"), s["telegraphs"][0])
            if far.get("text_tr"):
                warnings.append(f"- {far['text_tr']} ({s['name']}, T{s.get('danger_tier')})")
    L += ["", "## What everyone says is dangerous"] + (warnings or ["- (herkesin uzak durduğu bir yer henüz yok)"])
    changes = []
    for eid, fields in (overlay.get("entries") or {}).items():
        for field in fields:
            _, changed, rec = ov(overlay, eid, field)
            if changed:
                changes.append(f"- {name_of(pub, eid)} ({eid}): {field} {rec.get('birth')} → {rec.get('value')} (gün {rec.get('day')}, {rec.get('writer')}"
                               + (f", {rec['reason']}" if rec.get("reason") else "") + ")")
    L += ["", "## Changed since birth"] + (changes or ["*(nothing yet — overlay empty beyond birth statuses)*"])
    L += ["", f"*Üretildi: {now_iso()} — render_dm.py world*"]
    return "\n".join(L) + "\n"


# ── npcs.md ───────────────────────────────────────────────────────────────────

def npcs_text(campaign: str) -> str:
    pub = projection(campaign)
    overlay = load_overlay(campaign)
    L = [f"# NPCs — {campaign}", "",
         "*Index generated from the public projection ⊕ overlay at every `save` (`render_dm.py npcs`). Full dossiers live in "
         "`design/npcs/<id>.md` (DM-open, player-avoid); their Secret sections in `design/dm-only/npcs/`. Never hand-edited.*", "",
         "| Name | Id | Role | Faction | Location | Tier | Alive | Notes |", "|------|----|------|---------|----------|------|-------|-------|"]
    for nid, n in by_type(pub, "npc"):
        title = f"{n['name']} ({n['aliases'][0]})" if n.get("aliases") else n["name"]
        location = marked(pub, overlay, nid, "location", n.get("location_at_birth"))
        alive = marked(pub, overlay, nid, "alive", "alive", as_name=False)
        role = n.get("role") or "—"
        notes = short(n.get("voice_seed") or n.get("summary"), 70)
        L.append(f"| {title} | {nid} | {role} | {name_of(pub, n.get('faction')) if n.get('faction') else '—'} | {location} | {n.get('tier', '—')} | {alive} | {notes} |")
    L += ["", f"*Üretildi: {now_iso()} — render_dm.py npcs*"]
    return "\n".join(L) + "\n"


# ── design/index.md ───────────────────────────────────────────────────────────

def index_text(campaign: str) -> str:
    pub = projection(campaign)
    overlay = load_overlay(campaign)
    L = [f"# Index — {campaign}", "",
         "*The master index, generated from the public projection ⊕ overlay (`render_dm.py index`; plan item 16.2). "
         "One table per type; `status` and `seen_in_play` come from the overlay. \"Was this ever designed?\" is answered here or by `campaign_search.py`.*", ""]
    types = [t for t in INDEX_ORDER if any(e.get("type") == t for e in pub.values())]
    types += sorted({e.get("type") for e in pub.values()} - set(types) - {None})
    for t in types:
        rows = by_type(pub, t)
        L += [f"## {t} ({len(rows)})", "", "| id | name | aliases | file | status | seen_in_play | region | one line |", "|---|---|---|---|---|---|---|---|"]
        for eid, e in rows:
            status, _, _ = ov(overlay, eid, "status")
            seen, _, _ = ov(overlay, eid, "seen_in_play")
            region = e.get("region") or (pub.get(e.get("settlement") or "", {}).get("region") if e.get("settlement") else None)
            L.append(f"| {eid} | {e.get('name', '')} | {', '.join(e.get('aliases') or []) or '—'} | {e.get('file') or '—'} | {status or '—'} | "
                     f"{'✓' if seen else '—'} | {name_of(pub, region) if region else '—'} | {short(e.get('summary'), 80)} |")
        L.append("")
    L.append(f"*Üretildi: {now_iso()} — render_dm.py index*")
    return "\n".join(L) + "\n"


# ── a lean state.md ───────────────────────────────────────────────────────────

def state_text(campaign: str) -> str:
    pub = projection(campaign)
    m = dm.load(campaign)
    overlay = load_overlay(campaign)
    calendar = read_json(campaign_dir(campaign) / "calendar.json") or {}
    mp = read_json(design_dir(campaign) / "map.json") or {}
    news = (read_json(design_dir(campaign) / "news.json") or {}).get("records", [])
    hub = next((n["id"] for n in mp.get("nodes", []) if n.get("hub")), None) or next((sid for sid, _ in by_type(pub, "settlement")), None)
    start = name_of(pub, hub) if hub else "—"
    party = []
    chars = campaign_dir(campaign) / "characters"
    if chars.is_dir():
        for p in sorted(chars.glob("*.md")):
            party.append(p.stem)
    chapters = by_type(pub, "chapter")
    first_chapter = next((cid for cid, c in sorted(chapters, key=lambda kv: kv[1].get("order") or 99)), None)
    beats = [bid for bid, _ in by_type(pub, "beat")]
    day0 = [r.get("id") for r in news if r.get("day", 0) == 0][:6]
    L = [f"# Campaign: {campaign}",
         f"**Created:** {date.today().isoformat()}  **Last session:** —  **Session count:** 1  **Ruleset:** 2014", "",
         "*Lean state.md generated by the designer (plan item 16.6): what happened lives here, what was designed lives in `design/`. "
         "Never paste design content into this file; the fast validator warns above 600 lines.*", "",
         "## Current Situation",
         f"- **Location:** {start}",
         f"- **In-world date/time:** {today_line(calendar)}, {calendar.get('time', 'morning')} (gün {calendar.get('day_counter', 0)})",
         f"- **Party:** {' | '.join(party) or '(no characters yet — /dm:dnd character new)'}",
         "- **Party status:** —", "",
         "## Pinned Facts", "*(none pinned yet)*", "",
         "## World State",
         f"- **In-world date:** {today_line(calendar)}",
         f"- **Threat arc stage:** {overlay.get('_meta', {}).get('threat_stage', 1)} — Now (overlay: `design/overlay.json`)",
         "- **Faction states:** see `factions.json` (rendered at load by `factions.py board`)", "",
         "## Active Quests", "*(none yet — seeds live in `design/arc.md` and `design/seeds/`)*", "",
         "## Open Threads & Rumours",
         ("- " + ", ".join(day0) + " reach the party's region on day 0 (`design/news.json`)") if day0 else "*(none yet)*", "",
         "## Faction Moves", "*(none yet — `simulate` starts at the first `end`)*", "",
         "## Recent Events", "*(session 1 has not been played)*", "",
         "## Active Combat", "*(none)*", "",
         "## Live State Flags", "", "**Cover:** *(none)*", "",
         "**Faction stances** *(only list factions with non-neutral standing toward the party)*: *(none)*", "",
         "**NPC dispositions** *(only list NPCs with changed or notable standing)*: *(none)*", "",
         "## Campaign Arc", "```yaml", "type: designed", "arc_file: design/arc.md", "arc_id: arc_1", "current_act: 1",
         f"current_chapter: {first_chapter or 'chapter_1'}", f"current_beat: {beats[0] if beats else 'beat_1a'}", "beats_status:"]
    L += [f"  {b}: pending" for b in beats] or ["  beat_1a: pending"]
    L += [f"doom_day: {overlay.get('_meta', {}).get('doom_day')}", "steering_notes: >", "  (the DM writes the first steering note at the first `end`)",
          "revision_log: []", "```", "", "## Arc History", "*(empty)*", "",
          "## Session Flags", "session_status: open", "", "## DM Notes (hidden from players)", "*(none yet)*", "",
          "### DM Style Notes", "*(calibration begins at the first `end`)*", ""]
    return "\n".join(L)


# ── design/report.md ──────────────────────────────────────────────────────────

def report_text(campaign: str) -> str:
    pub = projection(campaign)
    m = dm.load(campaign)
    d = m.get("dials") or {}
    scale = dt.scale_row(d.get("scale") or "short") or {}
    L = [f"# Birth report — {campaign} (public part)", "",
         "*Generated by `render_dm.py report` from `design/design.json` and the public projection. The DM's part of the report "
         "(the secret abstract, the critics' dm-only findings) is not written here; the owner reads this part and the primer.*", "",
         "## Dials",
         f"- scale {d.get('scale')} · tone {d.get('tone')} · magic {d.get('magic')} · era {d.get('era')} · danger {d.get('danger')} · "
         f"party {d.get('party_size')} at level {d.get('start_level', 1)} (band {'-'.join(str(x) for x in (d.get('level_band') or []))}) · "
         f"content mix {', '.join(d.get('content_mix') or [])} · narration {d.get('lang')} · seed `{(m.get('seed') or {}).get('master')}`",
         f"- wishes: must {', '.join((d.get('wishes') or {}).get('must') or []) or '—'}; must not {', '.join((d.get('wishes') or {}).get('must_not') or []) or '—'}", "",
         "## Counts (public rows) against the scale", "| type | public | band |", "|---|---|---|"]
    bands = {"polity": scale.get("polities"), "region": scale.get("regions"), "god": scale.get("gods"), "faction": (scale.get("factions") or {}).get("count") if isinstance(scale.get("factions"), dict) else scale.get("factions"),
             "npc": scale.get("named_npcs"), "site": (scale.get("sites") or {}).get("count") if isinstance(scale.get("sites"), dict) else None,
             "seed": scale.get("quest_seeds"), "chapter": scale.get("chapters")}
    counts: dict = {}
    for e in pub.values():
        counts[e.get("type")] = counts.get(e.get("type"), 0) + 1
    for t in INDEX_ORDER:
        if t in counts:
            b = bands.get(t)
            if isinstance(b, dict):
                b = b.get("count")
            btxt = "-".join(str(x) for x in dt.band(b)) if isinstance(b, (int, list, tuple)) else "—"
            L.append(f"| {t} | {counts[t]} | {btxt} |")
    L += ["", "## Phases", "| phase | status | attempt | rounds | minutes | tokens out | approved |", "|---|---|---|---|---|---|---|"]
    for pn, ph in (m.get("phases") or {}).items():
        approval = ph.get("approval") or {}
        L.append(f"| {pn} | {ph.get('status')} | {ph.get('attempt') or 0} | {len(approval.get('rounds') or [])} | "
                 f"{round(int(ph.get('wall_s') or 0) / 60)} | {int((ph.get('tokens') or {}).get('out') or 0):,}".replace(",", ".")
                 + f" | {(approval.get('approved_at') or '—')[:10]} |")
    val = m.get("validator_last") or {}
    L += ["", "## Validator (last full run)", f"- {val.get('errors', '—')} errors, {val.get('warnings', '—')} warnings at {val.get('at') or '—'}", "",
          "## Revisions", ] + ([f"- {r.get('at', '')[:10]} {r.get('scope', '')}: {short(r.get('reason') or r.get('text'), 100)}" for r in (m.get("revision_log") or [])] or ["*(none)*"])
    L += ["", f"*Üretildi: {now_iso()} — render_dm.py report*"]
    return "\n".join(L) + "\n"


# ── CLI ───────────────────────────────────────────────────────────────────────

def write(path: Path, text: str, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"render_dm: {label} → {path.name} ({len(text)} chars)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the DM's generated files")
    ap.add_argument("-c", "--campaign", required=True)
    ap.add_argument("verb", choices=("world", "npcs", "index", "state", "report", "all"))
    ap.add_argument("--force", action="store_true", help="state: overwrite an existing state.md")
    a = ap.parse_args(argv)
    if not projection(a.campaign):
        print("render_dm: no public projection (design/entities.json); nothing to render", file=sys.stderr)
        return 1
    root = campaign_dir(a.campaign)
    if a.verb in ("world", "all"):
        write(root / "world.md", world_text(a.campaign), "world")
    if a.verb in ("npcs", "all"):
        write(root / "npcs.md", npcs_text(a.campaign), "npcs")
    if a.verb in ("index", "all"):
        write(design_dir(a.campaign) / "index.md", index_text(a.campaign), "index")
    if a.verb in ("state", "all"):
        target = root / "state.md"
        if target.is_file() and not a.force:
            print("render_dm: state.md exists; --force to regenerate the lean file (what happened in play would be lost)"
                  if a.verb == "state" else "render_dm: state.md kept (exists)")
            if a.verb == "state":
                return 1
        else:
            write(target, state_text(a.campaign), "state")
    if a.verb in ("report", "all"):
        write(design_dir(a.campaign) / "report.md", report_text(a.campaign), "report")
    return 0


if __name__ == "__main__":
    sys.exit(main())
