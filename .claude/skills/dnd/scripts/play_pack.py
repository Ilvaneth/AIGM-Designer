#!/usr/bin/env python3
"""
play_pack.py — the designer in play: the load pack, the scene pack, the prep step, `detail` through the
birth machinery, the spotlight ledger, the end pack.

Plan items 13.1-13.6, 12.3, 16.3, 24.6 #5; slice 1d. Everything here reads the public projection, the
overlay, the map, the news feed, site-progress and state.md; nothing here reads design/dm-only/ (it only
names the dm-only file the DM may read lazily). `detail` arms the guard, hands the fan-out JSON to the
conductor and merges the agent's fragment afterwards; the play tab never authors the file.

  designer.py -c CAMP load-pack [--day N] [--session N] [--intent TEXT] [--json]
  designer.py -c CAMP scene --enter ID [--hours N] [--present a,b] [--session N] [--json]
  designer.py -c CAMP prep [--day N] [--level L] [--intent TEXT] [--max 3] [--note TEXT] [--json]
  designer.py -c CAMP detail ID [--trigger prep|approach|hand] [--day N] [--session-id S] [--json]
  designer.py -c CAMP detail ID --finish [--day N]
  designer.py -c CAMP spotlight --session N --scenes thread_a=3,thread_b=1
  designer.py -c CAMP end-pack --day N --session N [--intent TEXT] [--note TEXT]
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
import map_travel as mt  # noqa: E402
from design_io import campaign_dir, design_dir, dm_only_dir, load_overlay, now_iso, read_json, rel  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
DETAIL_KINDS = {"site": "detail.site", "settlement": "detail.settlement", "npc": "detail.npc", "chapter": "detail.chapter"}
BIRTH_PHASE = {"site": "P6", "settlement": "P3", "npc": "P5", "chapter": "P7"}


# ── sources ───────────────────────────────────────────────────────────────────

def projection(campaign: str) -> dict:
    return (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})


def current_day(campaign: str) -> int:
    cal = read_json(campaign_dir(campaign) / "calendar.json") or {}
    return int(cal.get("day_counter") or 0)


def state_text(campaign: str) -> str:
    p = campaign_dir(campaign) / "state.md"
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def state_line(text: str, label: str) -> str | None:
    m = re.search(r"^- \*\*" + re.escape(label) + r":\*\*\s*(.+?)\s*$", text, re.M)
    return m.group(1) if m else None


def match_entity(pub: dict, phrase: str, types: tuple = ("settlement", "site", "place", "region")) -> str | None:
    """A name (or id) from state.md or the DM's intent → an entity id; longest name match wins."""
    if not phrase:
        return None
    if phrase in pub:
        return phrase
    low = phrase.lower()
    best = None
    for eid, e in pub.items():
        if e.get("type") not in types:
            continue
        for n in [e.get("name")] + list(e.get("aliases") or []):
            if isinstance(n, str) and n and n.lower() in low and (best is None or len(n) > len(best[1])):
                best = (eid, n)
    return best[0] if best else None


def party_location(campaign: str, pub: dict) -> str | None:
    """The settlement (or the settlement of the place) state.md's Location line names; else the map hub."""
    loc = state_line(state_text(campaign), "Location") or ""
    eid = match_entity(pub, loc.split("(")[0], ("settlement", "place", "site"))
    if eid and pub[eid].get("type") == "place":
        eid = pub[eid].get("settlement") or eid
    if eid:
        return eid
    mp = mt.load_map(campaign) or {}
    return next((n["id"] for n in mp.get("nodes", []) if n.get("hub")), None)


def party_level(campaign: str) -> int:
    levels = []
    chars = campaign_dir(campaign) / "characters"
    if chars.is_dir():
        for p in chars.glob("*.md"):
            m = re.search(r"\*\*Level:\*\*\s*(\d+)", p.read_text(encoding="utf-8", errors="replace"))
            if m:
                levels.append(int(m.group(1)))
    if levels:
        return max(levels)
    return int(((dm.load(campaign).get("dials") or {}).get("start_level")) or 1)


def band_of_level(level: int) -> int:
    return 1 if level <= 4 else 2 if level <= 10 else 3 if level <= 16 else 4


def news_records(campaign: str) -> list[dict]:
    return (read_json(design_dir(campaign) / "news.json") or {}).get("records", [])


def region_of(pub: dict, eid: str | None) -> str | None:
    e = pub.get(eid or "", {})
    return e.get("region") or pub.get(e.get("settlement") or "", {}).get("region")


def news_for(campaign: str, pub: dict, here: str | None, day: int, days_back: int = 7, limit: int = 5) -> list[dict]:
    reach = {here, region_of(pub, here)} - {None}
    out = []
    for r in news_records(campaign):
        if not (day - days_back <= int(r.get("day", 0)) <= day):
            continue
        if r.get("visibility") not in ("public", "rumored"):
            continue
        rr = set(r.get("reach") or [])
        if reach and not ((rr & reach) if rr else (r.get("region") in reach)):
            continue        # a record's reach is where it is heard; the region is only a fallback for reach-less records
        out.append(r)
    out.sort(key=lambda r: (-int(r.get("day", 0)), r.get("id", "")))
    return out[:limit]


def site_status(overlay: dict, sid: str) -> str:
    rec = ((overlay.get("entries") or {}).get(sid) or {}).get("status")
    return rec.get("value") if rec else "skeleton"


def status_day(overlay: dict, sid: str) -> int:
    rec = ((overlay.get("entries") or {}).get(sid) or {}).get("status")
    return int(rec.get("day") or 0) if rec else 0


# ── detail needed / re-check ──────────────────────────────────────────────────

def detail_needed(campaign: str, pub: dict, overlay: dict, day: int, intent: str | None) -> list[dict]:
    """Item 13.1: skeleton sites the party is approaching — within a day, stated, or pointed at by news."""
    here = party_location(campaign, pub)
    near = {r["id"]: r["days"] for r in mt.near(campaign, here, 1.0, {"site"})} if here else {}
    stated: set = set()
    for phrase in filter(None, [intent, state_line(state_text(campaign), "Stated destination")]):
        for part in re.split(r"[;,/]| ve | and ", phrase):
            eid = match_entity(pub, part.strip(), ("site", "settlement"))
            if eid:
                stated.add(eid)
    pointed: dict[str, str] = {}
    for r in news_records(campaign):
        if int(r.get("day", 0)) <= day:
            for ref in r.get("refs") or []:
                if ref.startswith("site_"):
                    pointed.setdefault(ref, r.get("id"))
    rows = []
    for sid, s in sorted(pub.items()):
        if s.get("type") != "site":
            continue
        status = site_status(overlay, sid)
        reasons = []
        if sid in near:
            reasons.append(f"{mt.fmt_days(near[sid])} gün uzakta")
        if sid in stated:
            reasons.append("hedef olarak söylendi")
        if sid in pointed:
            reasons.append(f"söylenti işaret ediyor ({pointed[sid]})")
        if not reasons:
            continue
        rows.append({"id": sid, "name": s.get("name"), "tier": s.get("danger_tier"), "status": status,
                     "days": near.get(sid), "reasons": reasons,
                     "needs_detail": status in ("skeleton", "detailed-stale")})
    rows.sort(key=lambda r: (not r["needs_detail"], "hedef olarak söylendi" not in r["reasons"], r["days"] if r["days"] is not None else 99, r["id"]))
    return rows


def recheck(campaign: str, pub: dict, overlay: dict, day: int) -> list[dict]:
    """Risk 24.1 #15: a detailed-unplayed site touched by later news is flagged RE-CHECK."""
    out = []
    for sid, s in pub.items():
        if s.get("type") != "site" or site_status(overlay, sid) != "detailed":
            continue
        since = status_day(overlay, sid)
        touching = [r["id"] for r in news_records(campaign)
                    if since < int(r.get("day", 0)) <= day and (sid in (r.get("refs") or []) or (s.get("faction") and s["faction"] in (r.get("refs") or [])))]
        if touching:
            out.append({"id": sid, "name": s.get("name"), "news": touching})
    return out


# ── spotlight ledger ──────────────────────────────────────────────────────────

def spotlight_summary(campaign: str, m: dict) -> dict:
    ledger = m.get("spotlight") or []
    last = ledger[-3:]
    totals: dict[str, int] = {}
    for entry in last:
        for tid, n in (entry.get("scenes") or {}).items():
            totals[tid] = totals.get(tid, 0) + int(n)
    flag = None
    if len(totals) >= 2:
        hi, lo = max(totals.values()), min(totals.values())
        limit = float(dt.scale_shared().get("thread_imbalance_max") or 0.35)
        if hi and (hi - lo) / hi > limit:
            flag = f"spotlight dengesiz: {', '.join(f'{k} {v}' for k, v in sorted(totals.items()))} (son {len(last)} oturum; sınır %{int(limit * 100)})"
    return {"sessions": [e.get("session") for e in last], "totals": totals, "flag": flag}


# ── the load pack ─────────────────────────────────────────────────────────────

def load_pack(campaign: str, day: int | None, session: int | None, intent: str | None) -> dict:
    pub = projection(campaign)
    overlay = load_overlay(campaign)
    m = dm.load(campaign)
    day = current_day(campaign) if day is None else day
    here = party_location(campaign, pub)
    text = state_text(campaign)
    chapter = None
    cm = re.search(r"^current_chapter:\s*(\S+)", text, re.M)
    if cm:
        chapter = cm.group(1)
    if not chapter:
        chapter = next((cid for cid, c in sorted(((k, v) for k, v in pub.items() if v.get("type") == "chapter"), key=lambda kv: kv[1].get("order") or 99)), None)
    chapter_file = pub.get(chapter or "", {}).get("file")
    threads = [{"id": tid, "file": t.get("file"), "pc": t.get("pc"), "face": f"design/player/{tid}.md" if (design_dir(campaign) / "player" / f"{tid}.md").is_file() else None}
               for tid, t in sorted(pub.items()) if t.get("type") == "thread"]
    progress = read_json(campaign_dir(campaign) / "site-progress.json") or {}
    opened = [{"id": sid, "current_room": rec.get("current_room"), "opened_day": rec.get("opened_day")}
              for sid, rec in (progress.get("sites") or {}).items() if rec.get("opened_day") is not None]
    prep = m.get("prep") or {}
    pack = {
        "campaign": campaign, "day": day, "session": session, "mode": (m.get("_meta") or {}).get("mode"),
        "location": here, "location_name": pub.get(here or "", {}).get("name"),
        "pending_scenes": [s for s in (overlay.get("pending_scenes") or []) if s.get("status") == "pending"],
        "detail_needed": [r for r in detail_needed(campaign, pub, overlay, day, intent) if r["needs_detail"]],
        "prepped": prep.get("candidates") or [], "prep_note": prep.get("note_tr"), "prep_day": prep.get("day"),
        "recheck": recheck(campaign, pub, overlay, day),
        "chapter": chapter, "chapter_file": chapter_file,
        "threads": threads,
        "news": [{"id": r.get("id"), "day": r.get("day"), "line_tr": r.get("line_tr")} for r in news_for(campaign, pub, here, day)],
        "sites_open": opened,
        "spotlight": spotlight_summary(campaign, m),
        "threat_stage": (overlay.get("_meta") or {}).get("threat_stage", 1),
        "simulated_to_day": (overlay.get("_meta") or {}).get("simulated_to_day", 0),
    }
    return pack


def load_pack_text(p: dict) -> str:
    L = [f"designer load-pack — {p['campaign']} · gün {p['day']}" + (f" · oturum {p['session']}" if p.get("session") else "")
         + f" · konum {p.get('location_name') or p.get('location') or '?'} · tehdit aşaması {p['threat_stage']}"]
    if p["pending_scenes"]:
        L.append("BEKLEYEN SAHNELER (önce bunlar):")
        for s in p["pending_scenes"]:
            L.append(f"  - {s.get('id')} gün {s.get('day')}: {s.get('line_tr')}")
    if p["recheck"]:
        L.append("RE-CHECK (detaylı ama sonraki haberler dokundu; ekoloji/içerik yeniden detaylanmalı):")
        for r in p["recheck"]:
            L.append(f"  - {r['id']} ({r['name']}): {', '.join(r['news'])}")
    L.append("Detail gerekli:" if p["detail_needed"] else "Detail gerekli: (yok)")
    for r in p["detail_needed"]:
        L.append(f"  - {r['id']} ({r['name']}, T{r['tier']}, {r['status']}): {'; '.join(r['reasons'])} → `designer.py -c {p['campaign']} detail {r['id']} --trigger approach`")
    if p["prepped"]:
        L.append(f"Son `end`'de hazırlananlar (gün {p.get('prep_day')}): " + ", ".join(c.get("id") if isinstance(c, dict) else str(c) for c in p["prepped"]))
    if p.get("prep_note"):
        L.append(f"Hazırlık notu: {p['prep_note']}")
    L.append(f"Bölüm: {p.get('chapter') or '?'} → {p.get('chapter_file') or '(dosya yok)'} (yalnız bu bölüm okunur)")
    L.append("İplikler (hepsi okunur): " + (", ".join(f"{t['id']} → {t['file']}" for t in p["threads"]) or "(henüz yok — design integrate)"))
    if p["sites_open"]:
        L.append("Açık mekânlar: " + ", ".join(f"{s['id']} (oda {s.get('current_room')})" for s in p["sites_open"]))
    L.append("Haberler (bölge, son 7 gün):" if p["news"] else "Haberler: (yok)")
    for n in p["news"]:
        L.append(f"  - gün {n['day']} {n['id']}: {n['line_tr']}")
    sp = p.get("spotlight") or {}
    if sp.get("totals"):
        L.append("Spotlight (son 3 oturum): " + ", ".join(f"{k} {v}" for k, v in sorted(sp["totals"].items())) + (f" — ⚠ {sp['flag']}" if sp.get("flag") else ""))
    return "\n".join(L)


# ── the scene pack ────────────────────────────────────────────────────────────

def scene_enter(campaign: str, target: str, hours: int | None, present: list[str], session: int | None, day: int | None) -> dict:
    pub = projection(campaign)
    overlay = load_overlay(campaign)
    day = current_day(campaign) if day is None else day
    eid = target if target in pub else match_entity(pub, target, ("place", "site", "settlement", "district", "region"))
    if not eid:
        raise SystemExit(f"play_pack: no public place, site or settlement matches {target!r}")
    e = pub[eid]
    settlement = e.get("settlement") if e.get("type") in ("place", "district") else (eid if e.get("type") == "settlement" else None)
    here = settlement or eid
    npcs = []
    for nid, n in sorted(pub.items()):
        if n.get("type") != "npc":
            continue
        loc_rec = ((overlay.get("entries") or {}).get(nid) or {}).get("location")
        loc = loc_rec.get("value") if loc_rec else n.get("location_at_birth")
        alive_rec = ((overlay.get("entries") or {}).get(nid) or {}).get("alive")
        alive = alive_rec.get("value") if alive_rec else "alive"
        if loc == eid or nid in present:
            npcs.append({"id": nid, "name": n.get("name"), "role": n.get("role"), "faction": n.get("faction"), "alive": alive,
                         "file": n.get("file"), "here": loc == eid})
    pack = {"campaign": campaign, "day": day, "session": session, "id": eid, "type": e.get("type"), "name": e.get("name"),
            "summary": e.get("summary"), "kind": e.get("kind"), "settlement": settlement, "region": region_of(pub, eid),
            "file": e.get("file"), "dm_only_file": None, "npcs": npcs,
            "news": [{"id": r.get("id"), "day": r.get("day"), "line_tr": r.get("line_tr")} for r in news_for(campaign, pub, here, day, limit=3)],
            "hours": hours}
    if e.get("file"):
        mirror = dm_only_dir(campaign) / Path(e["file"]).relative_to("design") if str(e["file"]).startswith("design/") else None
        if mirror and mirror.is_file():
            pack["dm_only_file"] = rel(campaign, mirror)
    if e.get("type") == "site":
        progress = (read_json(campaign_dir(campaign) / "site-progress.json") or {}).get("sites", {}).get(eid)
        pack["site"] = {"danger_tier": e.get("danger_tier"), "status": site_status(overlay, eid), "room_count": e.get("room_count"),
                        "escape_tr": e.get("escape_tr"), "attitude": e.get("attitude"),
                        "telegraphs": [t.get("text_tr") for t in (e.get("telegraphs") or [])],
                        "progress": {"current_room": progress.get("current_room"), "opened_day": progress.get("opened_day")} if progress else None,
                        "party_band": band_of_level(party_level(campaign))}
        if pack["site"]["status"] in ("skeleton", "detailed-stale"):
            pack["warning"] = f"{eid} is {pack['site']['status']}: run `designer.py -c {campaign} detail {eid} --trigger approach` before the scene opens (SKILL.md: a designed site is never improvised from its skeleton)"
    # play marks what the party has seen (item 16.5)
    seen = ((overlay.get("entries") or {}).get(eid) or {}).get("seen_in_play")
    if not (seen and seen.get("value") is True):
        subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "registry.py"), "-c", campaign, "play-set", eid, "seen_in_play", "true",
                        "--day", str(day), "--reason", "scene --enter"], capture_output=True, text=True, encoding="utf-8")
        pack["seen_marked"] = True
    return pack


def scene_text(p: dict) -> str:
    L = [f"designer scene --enter {p['id']} — {p['name']} ({p['type']}{', ' + p['kind'] if p.get('kind') else ''}) · gün {p['day']}"]
    if p.get("summary"):
        L.append(f"  {p['summary']}")
    if p.get("warning"):
        L.append(f"  ⚠ {p['warning']}")
    if p.get("site"):
        s = p["site"]
        L.append(f"  Mekân: T{s['danger_tier']} (parti bandı T{s['party_band']}{', ÜST KADEME' if (s['danger_tier'] or 0) > s['party_band'] else ''}), {s['room_count']} oda, durum {s['status']}"
                 + (f", oda {s['progress']['current_room']}" if s.get("progress") and s["progress"].get("current_room") else ""))
        for t in s.get("telegraphs") or []:
            L.append(f"    - telegraf: {t}")
        if s.get("escape_tr"):
            L.append(f"    - kaçış: {s['escape_tr']}")
    L.append("  Burada: " + (", ".join(f"{n['name']} ({n['role'] or '—'}{'' if n['alive'] == 'alive' else ', ' + n['alive']}{'' if n['here'] else ', getirildi'})" for n in p["npcs"]) or "(kayıtlı kimse yok)"))
    for n in p["news"]:
        L.append(f"  - haber gün {n['day']}: {n['line_tr']}")
    L.append(f"  Oku: {p.get('file') or '—'}" + (f" · sır gerekirse: {p['dm_only_file']}" if p.get("dm_only_file") else ""))
    if p.get("hours"):
        L.append(f"  Sahne bitince: calendar.py -c {p['campaign']} advance --hours {p['hours']}")
    return "\n".join(L)


# ── prep ──────────────────────────────────────────────────────────────────────

def prep(campaign: str, day: int | None, level: int | None, intent: str | None, max_n: int, note: str | None) -> dict:
    pub = projection(campaign)
    overlay = load_overlay(campaign)
    day = current_day(campaign) if day is None else day
    level = level or party_level(campaign)
    band = band_of_level(level)
    rows = detail_needed(campaign, pub, overlay, day, intent)
    rc = {r["id"]: r for r in recheck(campaign, pub, overlay, day)}
    candidates = []
    for r in rows:
        if r["needs_detail"] or r["id"] in rc:
            r = dict(r)
            if r["id"] in rc:
                r["reasons"].append("RE-CHECK: " + ", ".join(rc[r["id"]]["news"]))
            if (r.get("tier") or 0) > band:
                r["warning"] = f"üst kademe (T{r['tier']} > parti bandı T{band}): üç telegraf ve kaçış geometrisi sahnede yer almalı, yumuşatma yok"
            candidates.append(r)
    candidates = candidates[:max_n]
    m = dm.load(campaign)
    m["prep"] = {"day": day, "at": now_iso(), "level": level, "intent": intent, "note_tr": note,
                 "candidates": [{"id": c["id"], "reasons": c["reasons"], "tier": c.get("tier")} for c in candidates]}
    dm.save(campaign, m, "designer.py prep")
    return {"campaign": campaign, "day": day, "level": level, "band": band, "location": party_location(campaign, pub), "candidates": candidates}


def prep_text(p: dict) -> str:
    L = [f"designer prep — gün {p['day']}, parti seviye {p['level']} (bant T{p['band']}), konum {p.get('location') or '?'}"]
    if not p["candidates"]:
        L.append("  Hazırlanacak mekân yok: yakında, söylenmiş ya da söylentinin işaret ettiği iskelet yok.")
    for c in p["candidates"]:
        L.append(f"  - {c['id']} ({c['name']}, T{c['tier']}, {c['status']}): {'; '.join(c['reasons'])}")
        if c.get("warning"):
            L.append(f"      ⚠ {c['warning']}")
        L.append(f"      → designer.py -c {p['campaign']} detail {c['id']} --trigger prep --day {p['day']}")
    return "\n".join(L)


# ── detail through the birth machinery ────────────────────────────────────────

def detail_begin(campaign: str, eid: str, trigger: str, day: int | None, session_id: str | None) -> dict:
    import designer  # local import: designer imports nothing from here
    import design_prompts as dp
    pub = projection(campaign)
    if eid not in pub:
        raise SystemExit(f"play_pack: {eid} is not a public entity (a secret entity is detailed through `revise --dm-only`)")
    etype = pub[eid].get("type")
    if etype not in DETAIL_KINDS:
        raise SystemExit(f"play_pack: detail works on site / settlement / npc / chapter, not {etype}")
    overlay = load_overlay(campaign)
    day = current_day(campaign) if day is None else day
    status = site_status(overlay, eid) if etype in ("site", "settlement") else None
    warning = None
    if status in ("detailed", "played"):
        warning = f"{eid} is already {status}; a second detail only re-runs ecology and contents (detailed-stale)"
    if status == "played":
        raise SystemExit(f"play_pack: {eid} has been played; the bible is not rewritten under the party's feet")
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    files = dm.read_budget(campaign, canonical, eid)
    for extra in ("design/news.json", "design/overlay.json", "state.md", "site-progress.json"):
        if (campaign_dir(campaign) / extra).is_file():
            files.append(extra)
    files = list(dict.fromkeys(files))
    designer.arm(campaign, "detail", session_id)
    staging = design_dir(campaign) / "_staging" / "detail"
    staging.mkdir(parents=True, exist_ok=True)
    prompts_dir = design_dir(campaign) / "_prompts" / "detail"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    name = DETAIL_KINDS[etype]
    text = dp.render(campaign, name, eid, 1, phase_override="detail")
    (prompts_dir / f"{eid}.md").write_text(text, encoding="utf-8", newline="\n")
    crit = dp.render(campaign, "critic", eid, 1, 1, phase_override="detail")
    (prompts_dir / f"{eid}.critic.md").write_text(crit, encoding="utf-8", newline="\n")
    entry = {"id": eid, "status": "pending", "attempt": 0, "render_attempt": 1, "last_error": None, "files": files,
             "prompt": name, "prompt_cmd": designer.render_cmd(campaign, name, eid, 1, phase="detail"),
             "prompt_file": str(prompts_dir / f"{eid}.md"), "critics": 1, "effort": "medium",
             "critic_cmd": designer.render_cmd(campaign, "critic", eid, 1, phase="detail"), "critic_file": str(prompts_dir / f"{eid}.critic.md")}
    m = dm.load(campaign)
    m.setdefault("detail_log", []).append({"id": eid, "at": now_iso(), "day": day, "trigger": trigger, "status": "begun",
                                           "snapshot": dict((canonical.get(eid) or {}).get("stamped") or {}), "commit": None})
    dm.save(campaign, m, f"designer.py detail {eid}")
    return {"campaign": campaign, "phase": "detail", "attempt": 1, "auto_approve": True, "entity": eid, "trigger": trigger, "day": day,
            "warning": warning, "skeleton": {"status": "n/a"}, "directions": [], "seed": m["seed"]["master"],
            "entities": [entry], "phase_critic": None, "wishes_critic": None, "workflow": "design-fanout",
            "next": f"Workflow design-fanout with this JSON as args (or the Agent tool on prompt_cmd), then `designer.py -c {campaign} detail {eid} --finish --day {day}`"}


def detail_finish(campaign: str, eid: str, day: int | None) -> int:
    import designer
    day = current_day(campaign) if day is None else day
    staging = design_dir(campaign) / "_staging" / "detail"
    merged = staging / "merged"
    merged.mkdir(parents=True, exist_ok=True)
    critics = 0
    for path in sorted(staging.glob(f"{eid}.critic*.json")):
        path.replace(merged / path.name)
        critics += 1
    proc = designer.run_script("registry.py", campaign, "merge", "--phase", "detail", "--day", str(day))
    print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    report = read_json(staging / "merge.report.json") or {}
    ok = eid in (report.get("merged") or []) or any(u == eid for u in (report.get("units") or []))
    if not ok:
        print(f"designer: {eid} did not merge ({'; '.join((report.get('refused') or {}).get(eid) or ['no fragment in design/_staging/detail/'])}); "
              "the guard stays armed — run the agent again, then --finish", file=sys.stderr)
        return 1
    seed = designer.run_script("design_seed.py", campaign, "--phase", "detail")
    print(seed.stdout.strip())
    check = designer.run_script("design_check.py", campaign, "--only", eid, "--redact", "--json")
    try:
        findings = json.loads(check.stdout or "[]")
    except json.JSONDecodeError:
        findings = []
    errors = [f for f in findings if f.get("severity") == "error"]
    for line in designer.summarise_findings(findings):
        print(line)
    sha = designer.design_commit(campaign, f"detail {eid} (day {day})")
    m = dm.load(campaign)
    for entry in reversed(m.get("detail_log") or []):
        if entry.get("id") == eid and entry.get("status") == "begun":
            entry.update({"status": "finished", "finished_at": now_iso(), "errors": len(errors), "critics": critics, "commit": sha})
            break
    dm.save(campaign, m, f"designer.py detail {eid} --finish")
    designer.disarm()
    overlay = load_overlay(campaign)
    print(f"designer: detail {eid} finished — status {site_status(overlay, eid)}, validator {len(errors)} error(s), {critics} critic return(s), "
          f"commit {sha or 'none'}; guard disarmed. Read the file lazily when the scene opens.")
    return 1 if errors else 0


# ── spotlight / end pack ──────────────────────────────────────────────────────

def spotlight(campaign: str, session: int, scenes: dict) -> dict:
    m = dm.load(campaign)
    ledger = m.setdefault("spotlight", [])
    ledger = [e for e in ledger if e.get("session") != session]
    ledger.append({"session": session, "at": now_iso(), "scenes": {k: int(v) for k, v in scenes.items()}})
    m["spotlight"] = sorted(ledger, key=lambda e: e.get("session") or 0)
    dm.save(campaign, m, "designer.py spotlight")
    return spotlight_summary(campaign, m)


def end_pack(campaign: str, day: int, session: int, intent: str | None, note: str | None) -> int:
    """The fixed order of `end` (risk 24.1 #15): tick → sweep → prep; then the fast validator and the ledger."""
    import designer
    print(f"designer end-pack — gün {day}, oturum {session}")
    for verb in ("tick", "sweep"):
        proc = designer.run_script("factions.py", campaign, verb, "--day", str(day))
        out = (proc.stdout or proc.stderr).strip()
        print(f"[factions {verb}]\n{out}" if out else f"[factions {verb}] (nothing)")
    p = prep(campaign, day, None, intent, 3, note)
    print(prep_text(p))
    m = dm.load(campaign)
    sp = spotlight_summary(campaign, m)
    if sp.get("totals"):
        print("Spotlight: " + ", ".join(f"{k} {v}" for k, v in sorted(sp["totals"].items())) + (f" — ⚠ {sp['flag']}" if sp.get("flag") else ""))
    else:
        print(f"Spotlight: (henüz kayıt yok — `designer.py -c {campaign} spotlight --session {session} --scenes thread_x=N,...`)")
    fast = designer.run_script("design_check.py", campaign, "--fast")
    tail = (fast.stdout or "").strip().splitlines()
    print("[design_check --fast] " + (tail[-1] if tail else "(no output)"))
    state = campaign_dir(campaign) / "state.md"
    if state.is_file():
        n = len(state.read_text(encoding="utf-8", errors="replace").splitlines())
        if n > 600:
            print(f"⚠ state.md is {n} lines (limit 600): what was designed belongs in design/, not here")
    return 0


# ── argparse glue (called by designer.py) ─────────────────────────────────────

def add_subparsers(sub) -> None:
    lp = sub.add_parser("load-pack")
    lp.add_argument("--day", type=int)
    lp.add_argument("--session", type=int)
    lp.add_argument("--intent")
    lp.add_argument("--json", action="store_true")
    sc = sub.add_parser("scene")
    sc.add_argument("--enter", required=True, metavar="ID")
    sc.add_argument("--hours", type=int)
    sc.add_argument("--present", default="")
    sc.add_argument("--session", type=int)
    sc.add_argument("--day", type=int)
    sc.add_argument("--json", action="store_true")
    pr = sub.add_parser("prep")
    pr.add_argument("--day", type=int)
    pr.add_argument("--level", type=int)
    pr.add_argument("--intent")
    pr.add_argument("--max", type=int, default=3)
    pr.add_argument("--note")
    pr.add_argument("--json", action="store_true")
    de = sub.add_parser("detail")
    de.add_argument("id")
    de.add_argument("--trigger", default="hand", choices=("prep", "approach", "hand"))
    de.add_argument("--day", type=int)
    de.add_argument("--session-id")
    de.add_argument("--finish", action="store_true")
    de.add_argument("--json", action="store_true")
    sp = sub.add_parser("spotlight")
    sp.add_argument("--session", type=int, required=True)
    sp.add_argument("--scenes", required=True, help="thread_a=3,thread_b=1")
    ep = sub.add_parser("end-pack")
    ep.add_argument("--day", type=int, required=True)
    ep.add_argument("--session", type=int, required=True)
    ep.add_argument("--intent")
    ep.add_argument("--note")


def dispatch(campaign: str, a) -> int:
    if a.verb == "load-pack":
        p = load_pack(campaign, a.day, a.session, a.intent)
        print(json.dumps(p, ensure_ascii=False, indent=2) if a.json else load_pack_text(p))
        return 0
    if a.verb == "scene":
        present = [x.strip() for x in (a.present or "").split(",") if x.strip()]
        p = scene_enter(campaign, a.enter, a.hours, present, a.session, a.day)
        print(json.dumps(p, ensure_ascii=False, indent=2) if a.json else scene_text(p))
        return 0
    if a.verb == "prep":
        p = prep(campaign, a.day, a.level, a.intent, a.max, a.note)
        print(json.dumps(p, ensure_ascii=False, indent=2) if a.json else prep_text(p))
        return 0
    if a.verb == "detail":
        if a.finish:
            return detail_finish(campaign, a.id, a.day)
        out = detail_begin(campaign, a.id, a.trigger, a.day, a.session_id)
        if a.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"designer: detail {a.id} begun (trigger {a.trigger}, day {out['day']}); guard armed for detail")
            if out.get("warning"):
                print(f"  ⚠ {out['warning']}")
            print(f"  agent → {out['entities'][0]['prompt_cmd']}")
            print(f"  then → {out['next']}")
        return 0
    if a.verb == "spotlight":
        scenes = {}
        for part in a.scenes.split(","):
            if "=" in part:
                k, v = part.split("=", 1)
                scenes[k.strip()] = int(v)
        s = spotlight(campaign, a.session, scenes)
        print("designer: spotlight recorded — " + ", ".join(f"{k} {v}" for k, v in sorted(s["totals"].items())) + (f" — ⚠ {s['flag']}" if s.get("flag") else ""))
        return 0
    if a.verb == "end-pack":
        return end_pack(campaign, a.day, a.session, a.intent, a.note)
    return 2
