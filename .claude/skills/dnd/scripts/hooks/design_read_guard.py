#!/usr/bin/env python3
"""
design_read_guard.py — PreToolUse hook: the conductor never reads dm-only.

Plan item 19.1, errata 24.2 #4 and #13, 24.6 #5, docs/reports/2026-09-24-payload-probe.md.

Installed on Read | Grep | Bash (see .claude/settings.json). Armed only while a
designer command runs, through the marker <runtime-dir>/active-design.json:

    {"campaign": "<slug>", "mode": "birth" | "detail" | "playtest",
     "session_id": "<the session that armed it>",
     "agent_types_allowed": ["workflow-subagent", "design-writer", "design-critic"],
     "playtest_allowlist": ["design/player-primer.md", "characters/", ...]}

Who is calling comes from the payload (probed 2026-09-24): a subagent's
payload carries `agent_id` and `agent_type`; the conductor's carries neither.
`transcript_path` is the same for every caller and is never used.

Rules while armed for the marked campaign, for the marked session:
  * birth / detail — the conductor is denied every path under design/dm-only/
    and design/_staging/, and the registry verbs that print dm-only content;
    a subagent of an allowed type may read them; any other agent is denied.
  * playtest — the conductor (the DM at the table) reads freely; an agent of
    a `playtest_agent_types` type (default: player) may read only the
    allowlisted player-facing paths; other agents follow the birth rule.
Unarmed, or armed by another session, everything is allowed: the DM's own
reads of a finished file are never guarded (24.6 #5).

Exit codes: 0 allow, 2 block (stderr is shown to Claude).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_SCRIPTS))

GUARDED_TOOLS = {"Read", "Grep", "Bash"}
PROTECTED = re.compile(r"(?:^|/)design/(?:dm-only|_staging)(?:/|$)")
DEFAULT_AGENT_TYPES = ("workflow-subagent", "design-writer", "design-critic", "design-skeleton")
DEFAULT_PLAYTEST_TYPES = ("player",)
RULE_REF = 'SKILL.md, "The blind conductor"'

# Bash: a path token that points into a protected folder, or a registry verb that prints dm-only.
_PATH_TOKEN = re.compile(r"[\w./\\:~-]*(?:design[/\\](?:dm-only|_staging)[/\\]?[\w./\\-]*)")
_REGISTRY_DM = re.compile(r"registry\.py\b[^\n;&|]*\bshow\b[^\n;&|]*--dm\b")
_REGISTRY_EXPORT = re.compile(r"registry\.py\b[^\n;&|]*\bexport\b(?![^\n;&|]*--public)")
_DICE_SECRET = re.compile(r"design_dice\.py\b[^\n;&|]*\blog\b[^\n;&|]*--secret\b")


def _marker() -> dict | None:
    try:
        from paths import runtime_dir
        p = runtime_dir() / "active-design.json"
        if not p.is_file():
            return None
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) and data.get("campaign") else None
    except Exception:
        return None


def _campaign_root(name: str) -> Path | None:
    try:
        from paths import find_campaign
        return Path(str(find_campaign(name))).resolve()
    except Exception:
        return None


def _norm(path: str) -> str:
    return path.replace("\\", "/")


def _is_protected(path: str, root: Path | None) -> bool:
    """A path under the marked campaign's dm-only or _staging folder."""
    p = _norm(path)
    if not PROTECTED.search(p):
        return False
    if root is None:
        return True
    try:
        resolved = Path(path).expanduser().resolve()
    except Exception:
        return True
    root_s = _norm(str(root)).lower()
    return _norm(str(resolved)).lower().startswith(root_s + "/") or not os.path.isabs(path)


def _paths_touched(payload: dict) -> list[str]:
    tool = payload.get("tool_name")
    inp = payload.get("tool_input") or {}
    if tool == "Read":
        return [inp.get("file_path", "")]
    if tool == "Grep":
        return [p for p in (inp.get("path", ""), inp.get("glob", "")) if p]
    if tool == "Bash":
        return _PATH_TOKEN.findall(inp.get("command", "") or "")
    return []


def _bash_prints_dm_only(command: str) -> str | None:
    if _REGISTRY_DM.search(command):
        return "registry.py show --dm"
    if _REGISTRY_EXPORT.search(command):
        return "registry.py export without --public"
    if _DICE_SECRET.search(command):
        return "design_dice.py log --secret"
    return None


def _allowlisted(path: str, root: Path | None, allow: list) -> bool:
    if root is None:
        return False
    try:
        rel = _norm(str(Path(path).expanduser().resolve().relative_to(root)))
    except Exception:
        return False
    return any(rel == a.rstrip("/") or rel.startswith(a.rstrip("/") + "/") for a in allow)


def check(payload: dict, marker: dict | None) -> str | None:
    """Return a block reason, or None to allow."""
    if payload.get("tool_name") not in GUARDED_TOOLS or not marker:
        return None
    if marker.get("session_id") and payload.get("session_id") and marker["session_id"] != payload["session_id"]:
        return None                                   # another tab's marker
    mode = marker.get("mode", "birth")
    agent_id = payload.get("agent_id")
    agent_type = payload.get("agent_type") or ""
    root = _campaign_root(marker["campaign"])
    touched = _paths_touched(payload)
    command = (payload.get("tool_input") or {}).get("command", "") if payload.get("tool_name") == "Bash" else ""
    verb = _bash_prints_dm_only(command) if command else None
    protected = [p for p in touched if _is_protected(p, root)]

    if mode == "playtest":
        if not agent_id:
            return None                               # the DM at the table reads freely
        if agent_type in tuple(marker.get("playtest_agent_types") or DEFAULT_PLAYTEST_TYPES):
            allow = list(marker.get("playtest_allowlist") or [])
            for p in touched:
                if p and not _allowlisted(p, root, allow) and (root is None or _norm(str(root)).lower() in _norm(str(Path(p).expanduser().resolve())).lower() if os.path.isabs(p) else True):
                    return (f"The player agent may read only player-facing artifacts "
                            f"({', '.join(allow) or 'none listed'}); {p} is not one of them. See {RULE_REF}.")
            if verb:
                return f"The player agent may not run {verb}. See {RULE_REF}."
            return None
        # other agents in a playtest follow the birth rule below

    allowed_types = tuple(marker.get("agent_types_allowed") or DEFAULT_AGENT_TYPES)
    if agent_id and agent_type in allowed_types:
        return None                                   # a designer agent, fresh context: may read dm-only
    if not protected and not verb:
        return None
    who = "an agent of type " + repr(agent_type) if agent_id else "the conductor"
    what = verb or ", ".join(protected[:3])
    return (f"Design mode '{mode}' is armed for {marker['campaign']}: {who} may not read dm-only content "
            f"({what}). The conductor holds only the public projection (registry.py export --public) and "
            f"the redacted validator output; only fresh-context designer agents open design/dm-only/ and "
            f"design/_staging/. If this is the DM's own read after the run, disarm the marker first. See {RULE_REF}.")


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    reason = check(payload, _marker())
    if reason:
        print(f"BLOCKED by design_read_guard: {reason}", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
