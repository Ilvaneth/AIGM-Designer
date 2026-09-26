#!/usr/bin/env python3
"""
playtest.py — the first-session playtest with a player agent (plan item 22.5, slice 1e).

The DM (the main session, /dm:dnd load) runs a throwaway campaign's session 1 against a **player agent**:
a subagent with a persona and the PC's sheet, spawned each turn with the player-facing transcript so far.
The agent may read only player-facing artifacts — the primer, its own sheet, the thread faces under
design/player/, the transcript, the persona — never design/ or dm-only/: `start` arms the read guard in
`playtest` mode with exactly that allowlist. It rolls its own dice (dice.py --player) and reports the raw
result; the DM adds the modifiers. After the session the judges read the transcript against a checklist.

  playtest.py -c CAMP start --pc NAME --persona TEXT [--session N] [--session-id S]
  playtest.py -c CAMP turn --dm TEXT            append the DM's narration; print the player agent's prompt
  playtest.py -c CAMP turn --player TEXT        append the player's message (the agent's return)
  playtest.py -c CAMP prompt                    the player agent's prompt for the next turn (Agent tool, subagent_type player)
  playtest.py -c CAMP judge playtest|readability|uniqueness [--against CAMP2] [--record FILE]
  playtest.py -c CAMP status | stop

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
import designer  # noqa: E402
from design_io import campaign_dir, design_dir, now_iso, read_json, write_json_atomic  # noqa: E402
from paths import runtime_dir, skill_root  # noqa: E402

PLAY_PROMPTS = skill_root() / "prompts" / "play"
JUDGES = ("playtest", "readability", "uniqueness")


def folder(campaign: str) -> Path:
    return campaign_dir(campaign) / "playtest"


def meta_path(campaign: str) -> Path:
    return folder(campaign) / "playtest.json"


def load_meta(campaign: str) -> dict:
    m = read_json(meta_path(campaign))
    if not m:
        raise SystemExit("playtest: no playtest started (playtest.py start --pc NAME --persona TEXT)")
    return m


def sheet_of(campaign: str, pc: str) -> Path | None:
    chars = campaign_dir(campaign) / "characters"
    if not chars.is_dir():
        return None
    for p in chars.glob("*.md"):
        if p.stem.lower() == pc.lower() or p.stem.lower().split()[0] == pc.lower():
            return p
    return None


def render(name: str, ctx: dict) -> str:
    text = (PLAY_PROMPTS / f"{name}.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2].lstrip("\n")
    for k, v in ctx.items():
        text = text.replace("{{" + k + "}}", str(v))
    left = sorted(set(re.findall(r"\{\{([a-z_]+)\}\}", text)))
    if left:
        raise SystemExit(f"playtest: prompt {name} has unfilled placeholders: {', '.join(left)}")
    return text


def schema_text(name: str) -> str:
    p = PLAY_PROMPTS / "schemas" / f"{name}.json"
    return p.read_text(encoding="utf-8").strip() if p.is_file() else "{}"


# ── start / turn / prompt ─────────────────────────────────────────────────────

def start(campaign: str, pc: str, persona: str, session: int, session_id: str | None) -> int:
    sheet = sheet_of(campaign, pc)
    if sheet is None:
        print(f"playtest: no character sheet for {pc!r} under characters/", file=sys.stderr)
        return 1
    root = campaign_dir(campaign)
    f = folder(campaign)
    f.mkdir(parents=True, exist_ok=True)
    (f / "persona.md").write_text(f"# {sheet.stem} — the player's persona\n\n{persona.strip()}\n", encoding="utf-8", newline="\n")
    transcript = f / "transcript.md"
    if not transcript.is_file():
        transcript.write_text(f"# Playtest transcript — {campaign}, session {session}\n\n"
                              f"*PC: {sheet.stem} (`{sheet.relative_to(root).as_posix()}`). The player-facing record: the DM's narration and the "
                              f"player's messages, in order. Nothing else is ever pasted here.*\n\n", encoding="utf-8", newline="\n")
    faces = design_dir(campaign) / "player"
    allow = ["design/player-primer.md", sheet.relative_to(root).as_posix(), "playtest/transcript.md", "playtest/persona.md"]
    if faces.is_dir():
        allow.append("design/player/")
    designer.arm(campaign, "playtest", session_id)
    marker = runtime_dir() / "active-design.json"
    data = read_json(marker) or {}
    data["playtest_allowlist"] = allow
    data["playtest_agent_types"] = ["player"]
    write_json_atomic(marker, data)
    write_json_atomic(meta_path(campaign), {"campaign": campaign, "pc": sheet.stem, "sheet": sheet.relative_to(root).as_posix(),
                                            "session": session, "started": now_iso(), "turns": 0, "allowlist": allow})
    print(f"playtest: started for {sheet.stem} (session {session}); guard armed in playtest mode, the player agent may read: {', '.join(allow)}")
    print(f"playtest: transcript {transcript.relative_to(root).as_posix()} — `playtest.py -c {campaign} turn --dm \"...\"` after each narration, then spawn the player agent with the printed prompt")
    return 0


def turn(campaign: str, dm_text: str | None, player_text: str | None) -> int:
    m = load_meta(campaign)
    transcript = folder(campaign) / "transcript.md"
    if dm_text:
        m["turns"] = int(m.get("turns") or 0) + 1
        with transcript.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(f"## Tur {m['turns']}\n\n**DM:** {dm_text.strip()}\n\n")
        write_json_atomic(meta_path(campaign), m)
        print(f"playtest: turn {m['turns']} — the DM's narration recorded; the player agent's prompt:\n")
        print(prompt_text(campaign, m))
        return 0
    if player_text:
        with transcript.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(f"**{m['pc']}:** {player_text.strip()}\n\n")
        write_json_atomic(meta_path(campaign), m)
        print(f"playtest: turn {m.get('turns')} — the player's message recorded")
        return 0
    print("playtest: turn needs --dm TEXT or --player TEXT", file=sys.stderr)
    return 2


def prompt_text(campaign: str, m: dict | None = None) -> str:
    m = m or load_meta(campaign)
    root = campaign_dir(campaign)
    faces = sorted(p.relative_to(root).as_posix() for p in (design_dir(campaign) / "player").glob("*.md")) if (design_dir(campaign) / "player").is_dir() else []
    ctx = {"campaign": campaign, "campaign_dir": str(root).replace("\\", "/"), "pc": m["pc"], "sheet": m["sheet"],
           "persona_path": "playtest/persona.md", "transcript_path": "playtest/transcript.md",
           "primer_path": "design/player-primer.md", "faces": ", ".join(faces) or "(no thread face yet)",
           "turn": m.get("turns", 0), "dice_cmd": f"py -X utf8 {(skill_root() / 'scripts' / 'dice.py').as_posix()} <notation> --owner \"{m['pc']}\" --player --campaign {campaign} --label \"<what for>\"",
           "schema": schema_text("player")}
    return render("player", ctx)


# ── judges ────────────────────────────────────────────────────────────────────

def judge(campaign: str, kind: str, against: str | None, record: str | None) -> int:
    if kind not in JUDGES:
        print(f"playtest: judge kind must be one of {JUDGES}", file=sys.stderr)
        return 2
    if record:
        try:
            ret = json.loads(Path(record).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"playtest: cannot read the judge's return: {exc}", file=sys.stderr)
            return 1
        f = folder(campaign)
        f.mkdir(parents=True, exist_ok=True)
        write_json_atomic(f / f"judge-{kind}.json", ret)
        findings = ret.get("findings") or []
        fails = [x for x in findings if x.get("verdict") in ("fix", "fail")]
        print(f"playtest: judge {kind} recorded — {ret.get('verdict')}; {len(findings)} finding(s), {len(fails)} not passed")
        for x in fails[:12]:
            print(f"  ✗ {x.get('check')}: {x.get('note_tr') or ''}")
        return 0
    root = campaign_dir(campaign)
    ctx = {"campaign": campaign, "campaign_dir": str(root).replace("\\", "/"), "schema": schema_text("judge")}
    if kind == "playtest":
        m = load_meta(campaign)
        ctx.update({"pc": m["pc"], "sheet": m["sheet"], "transcript_path": "playtest/transcript.md", "turns": m.get("turns", 0)})
    elif kind == "readability":
        pub = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
        chapter = next((e.get("file") for e in sorted(pub.values(), key=lambda e: e.get("order") or 99) if e.get("type") == "chapter" and e.get("file")), "(no chapter file)")
        overlay = read_json(design_dir(campaign) / "overlay.json") or {}
        detailed = [eid for eid, rec in (overlay.get("entries") or {}).items() if (rec.get("status") or {}).get("value") == "detailed" and eid in pub]
        first_site = pub[detailed[0]].get("file") if detailed else "(no detailed site)"
        ctx.update({"chapter_file": chapter, "site_file": first_site, "primer_path": "design/player-primer.md",
                    "session1_path": "design/session-1.md" if (design_dir(campaign) / "session-1.md").is_file() else "(no session-1 pack yet)"})
    else:
        if not against:
            print("playtest: judge uniqueness needs --against CAMP2", file=sys.stderr)
            return 2
        import design_compare as dc
        r = dc.compare(campaign, against)
        lines = []
        for side in ("a", "b"):
            p = r["premises"][side]
            lines.append(f"[{side}] {p.get('name')}\n- question: {p.get('question_tr')}\n- pitch: {p.get('pitch_tr') or p.get('summary')}\n"
                         f"- signatures: {', '.join(filter(None, p.get('signatures') or []))}\n- breaks: {', '.join(filter(None, p.get('breaks') or []))}\n"
                         f"- gods: {', '.join(filter(None, p.get('gods') or []))}")
        ctx.update({"against": against, "premises": "\n\n".join(lines), "script_verdicts": json.dumps(r["verdicts"], ensure_ascii=False)})
    print(render(f"judge_{kind}", ctx))
    return 0


def status(campaign: str) -> int:
    m = read_json(meta_path(campaign))
    marker = read_json(runtime_dir() / "active-design.json") or {}
    if not m:
        print("playtest: none started")
        return 0
    print(f"playtest: {m['pc']} session {m.get('session')} — {m.get('turns', 0)} turn(s); guard "
          + (f"armed ({marker.get('mode')})" if marker.get("campaign") == campaign else "not armed"))
    for kind in JUDGES:
        p = folder(campaign) / f"judge-{kind}.json"
        if p.is_file():
            print(f"  judge {kind}: {(read_json(p) or {}).get('verdict')}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the first-session playtest with a player agent")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    s = sub.add_parser("start")
    s.add_argument("--pc", required=True)
    s.add_argument("--persona", required=True)
    s.add_argument("--session", type=int, default=1)
    s.add_argument("--session-id")
    t = sub.add_parser("turn")
    t.add_argument("--dm")
    t.add_argument("--player")
    sub.add_parser("prompt")
    j = sub.add_parser("judge")
    j.add_argument("kind", choices=JUDGES)
    j.add_argument("--against")
    j.add_argument("--record")
    sub.add_parser("status")
    sub.add_parser("stop")
    a = ap.parse_args(argv)
    if a.verb == "start":
        return start(a.campaign, a.pc, a.persona, a.session, a.session_id)
    if a.verb == "turn":
        return turn(a.campaign, a.dm, a.player)
    if a.verb == "prompt":
        print(prompt_text(a.campaign))
        return 0
    if a.verb == "judge":
        return judge(a.campaign, a.kind, a.against, a.record)
    if a.verb == "status":
        return status(a.campaign)
    if a.verb == "stop":
        print("playtest: guard disarmed" if designer.disarm() else "playtest: guard was not armed")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
