"""
goals.py — structured NPC/faction Goal Tracker, backed by <campaign>/goals.json.

Built 2026-09-17 (Ashen Crown, session 31) because free-text "remember this NPC's
motivation" reminders in state.md/npcs-full.md were not reliably acted on. This
gives the same treatment xp.py already gives character levels: a numeric or
boolean metric per major NPC/faction, and a LOUD, unmissable flag the instant a
threshold is crossed — never a silent update.

Each record in goals.json:
  {
    "id": "sarelle",                 # slug, matches npcs-full.md entry
    "name": "Sarelle Duskbourne",
    "kind": "npc" | "faction",
    "goal": "one-sentence goal",
    "metric_type": "numeric" | "boolean",
    "metric_label": "Crown parçası",  # numeric only
    "current": 5, "target": 9,        # numeric only
    "condition": "...",               # boolean only — the yes/no fact itself
    "achieved": false,                # boolean only
    "status": "on_track" | "threatened" | "blocked" | "permanent_loss",
    "responses": {
      "threatened": "pre-written move",
      "blocked": "pre-written move",
      "permanent_loss": "pre-written move"
    },
    "last_updated_session": 31
  }

CLI:
  python3 goals.py list    --campaign NAME [--kind npc|faction]
  python3 goals.py show    --campaign NAME --id ID
  python3 goals.py add     --campaign NAME --id ID --name NAME --kind npc|faction
                            --goal TEXT --metric-type numeric --target N
                            [--current N] --metric-label LABEL
                            --threatened TEXT --blocked TEXT --permanent-loss TEXT
  python3 goals.py add     --campaign NAME --id ID --name NAME --kind npc|faction
                            --goal TEXT --metric-type boolean --condition TEXT
                            --threatened TEXT --blocked TEXT --permanent-loss TEXT
  python3 goals.py set     --campaign NAME --id ID --current N [--session N]
  python3 goals.py achieve --campaign NAME --id ID [--session N]
  python3 goals.py status  --campaign NAME --id ID --value on_track|threatened|blocked|permanent_loss
  python3 goals.py check   --campaign NAME     # full board + flags empty/incomplete records
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from paths import find_campaign
except ImportError:  # pragma: no cover
    find_campaign = None  # type: ignore


def _goals_path(campaign: str) -> Path:
    if find_campaign is not None:
        base = find_campaign(campaign)
    else:  # pragma: no cover — fallback if paths.py unavailable
        base = Path.home() / ".claude" / "dnd" / "campaigns" / campaign
    return base / "goals.json"


def _load(campaign: str) -> list[dict]:
    p = _goals_path(campaign)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def _save(campaign: str, records: list[dict]) -> None:
    p = _goals_path(campaign)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def _find(records: list[dict], rid: str) -> dict | None:
    for r in records:
        if r["id"] == rid:
            return r
    return None


def _fmt_progress(r: dict) -> str:
    if r["metric_type"] == "numeric":
        return f"{r.get('current', 0)}/{r.get('target', '?')} {r.get('metric_label', '')}".strip()
    return ("✓ GERÇEKLEŞTİ" if r.get("achieved") else "henüz değil") + f" — {r.get('condition', '')}"


def cmd_list(args):
    records = _load(args.campaign)
    if args.kind:
        records = [r for r in records if r.get("kind") == args.kind]
    if not records:
        print(f"(goals.json boş ya da yok — {args.campaign})")
        return
    print(f"{'ID':<14} {'Ad':<28} {'Durum':<16} İlerleme")
    print("-" * 90)
    for r in records:
        print(f"{r['id']:<14} {r['name']:<28} {r.get('status', 'on_track'):<16} {_fmt_progress(r)}")


def cmd_show(args):
    records = _load(args.campaign)
    r = _find(records, args.id)
    if not r:
        print(f"error: id '{args.id}' bulunamadı", file=sys.stderr)
        sys.exit(1)
    print(f"## {r['name']} ({r['kind']})")
    print(f"Hedef: {r['goal']}")
    print(f"İlerleme: {_fmt_progress(r)}")
    print(f"Durum: {r.get('status', 'on_track')}")
    print("Eşik tepkileri:")
    for k in ("threatened", "blocked", "permanent_loss"):
        print(f"  {k} -> {r.get('responses', {}).get(k, '(yazılmamış)')}")
    print(f"Son güncelleme: session {r.get('last_updated_session', '?')}")


def cmd_add(args):
    records = _load(args.campaign)
    if _find(records, args.id):
        print(f"error: id '{args.id}' zaten var, 'set'/'status' kullan", file=sys.stderr)
        sys.exit(1)
    r = {
        "id": args.id,
        "name": args.name,
        "kind": args.kind,
        "goal": args.goal,
        "metric_type": args.metric_type,
        "status": "on_track",
        "responses": {
            "threatened": args.threatened,
            "blocked": args.blocked,
            "permanent_loss": args.permanent_loss,
        },
        "last_updated_session": args.session,
    }
    if args.metric_type == "numeric":
        if args.target is None or not args.metric_label:
            print("error: numeric tip için --target ve --metric-label gerekli", file=sys.stderr)
            sys.exit(1)
        r["current"] = args.current or 0
        r["target"] = args.target
        r["metric_label"] = args.metric_label
    else:
        if not args.condition:
            print("error: boolean tip için --condition gerekli", file=sys.stderr)
            sys.exit(1)
        r["condition"] = args.condition
        r["achieved"] = False
    records.append(r)
    _save(args.campaign, records)
    print(f"eklendi: {r['id']} ({r['name']})")


def cmd_set(args):
    records = _load(args.campaign)
    r = _find(records, args.id)
    if not r:
        print(f"error: id '{args.id}' bulunamadı", file=sys.stderr)
        sys.exit(1)
    if r["metric_type"] != "numeric":
        print("error: bu kayıt numeric değil, 'achieve' kullan", file=sys.stderr)
        sys.exit(1)
    old = r.get("current", 0)
    r["current"] = args.current
    if args.session is not None:
        r["last_updated_session"] = args.session
    crossed = old < r["target"] <= args.current
    _save(args.campaign, records)
    print(f"{r['name']}: {old} -> {args.current} / {r['target']} {r.get('metric_label', '')}")
    if crossed:
        print(f"\n⚠⚠⚠ {r['name']} — HEDEFE ULAŞILDI (Point of No Return tetiklendi) ⚠⚠⚠")
        print(f"Hedef: {r['goal']}")
        print("Bunu ŞİMDİ sahneye yansıt, session sonuna bırakma.")


def cmd_achieve(args):
    records = _load(args.campaign)
    r = _find(records, args.id)
    if not r:
        print(f"error: id '{args.id}' bulunamadı", file=sys.stderr)
        sys.exit(1)
    if r["metric_type"] != "boolean":
        print("error: bu kayıt boolean değil, 'set' kullan", file=sys.stderr)
        sys.exit(1)
    already = r.get("achieved", False)
    r["achieved"] = True
    if args.session is not None:
        r["last_updated_session"] = args.session
    _save(args.campaign, records)
    if not already:
        print(f"\n⚠⚠⚠ {r['name']} — HEDEFE ULAŞILDI (Point of No Return tetiklendi) ⚠⚠⚠")
        print(f"Koşul gerçekleşti: {r['condition']}")
        print("Bunu ŞİMDİ sahneye yansıt, session sonuna bırakma.")
    else:
        print(f"{r['name']}: zaten gerçekleşmişti, değişiklik yok.")


def cmd_status(args):
    records = _load(args.campaign)
    r = _find(records, args.id)
    if not r:
        print(f"error: id '{args.id}' bulunamadı", file=sys.stderr)
        sys.exit(1)
    old = r.get("status", "on_track")
    r["status"] = args.value
    _save(args.campaign, records)
    print(f"{r['name']}: durum {old} -> {args.value}")
    if args.value in ("threatened", "blocked", "permanent_loss") and old != args.value:
        resp = r.get("responses", {}).get(args.value)
        print(f"\n⚠ {r['name']} — {args.value.upper()} eşiği tetiklendi")
        print(f"Önceden yazılmış hamle: {resp or '(yazılmamış — şimdi biri yazılmalı)'}")


def cmd_check(args):
    records = _load(args.campaign)
    if not records:
        print("goals.json boş — henüz hiçbir NPC/faction kaydedilmedi.")
        return
    print("=" * 70)
    print("  GOAL TRACKER — TAM DURUM")
    print("=" * 70)
    cmd_list(args)
    incomplete = [
        r for r in records
        if not all(r.get("responses", {}).get(k) for k in ("threatened", "blocked", "permanent_loss"))
    ]
    flagged = [r for r in records if r.get("status") != "on_track"]
    if incomplete:
        print("\n⚠ Eksik eşik tepkisi olan kayıtlar (doldurulmalı):")
        for r in incomplete:
            print(f"  - {r['id']} ({r['name']})")
    if flagged:
        print("\n⚠ Şu an on_track DIŞINDA olan kayıtlar:")
        for r in flagged:
            print(f"  - {r['id']} ({r['name']}): {r['status']}")
    if not incomplete and not flagged:
        print("\nHer şey tam ve on_track — ek işlem gerekmiyor.")


def main():
    ap = argparse.ArgumentParser(prog="goals.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list")
    p.add_argument("--campaign", required=True)
    p.add_argument("--kind", choices=["npc", "faction"])
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show")
    p.add_argument("--campaign", required=True)
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("add")
    p.add_argument("--campaign", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--kind", required=True, choices=["npc", "faction"])
    p.add_argument("--goal", required=True)
    p.add_argument("--metric-type", required=True, choices=["numeric", "boolean"])
    p.add_argument("--target", type=int)
    p.add_argument("--current", type=int)
    p.add_argument("--metric-label")
    p.add_argument("--condition")
    p.add_argument("--threatened", required=True)
    p.add_argument("--blocked", required=True)
    p.add_argument("--permanent-loss", required=True)
    p.add_argument("--session", type=int)
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("set")
    p.add_argument("--campaign", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--current", type=int, required=True)
    p.add_argument("--session", type=int)
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("achieve")
    p.add_argument("--campaign", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--session", type=int)
    p.set_defaults(func=cmd_achieve)

    p = sub.add_parser("status")
    p.add_argument("--campaign", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--value", required=True, choices=["on_track", "threatened", "blocked", "permanent_loss"])
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("check")
    p.add_argument("--campaign", required=True)
    p.add_argument("--kind", choices=["npc", "faction"])
    p.set_defaults(func=cmd_check)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
