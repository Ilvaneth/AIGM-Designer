#!/usr/bin/env python3
"""
dice_guard.py — PreToolUse hook: stop a die that belongs to a player.

Installed as a Claude Code PreToolUse hook on Bash (see .claude/settings.json).
Reads the hook payload on stdin, inspects the command, and blocks it (exit 2,
reason on stderr) when it would roll a die the skill's dice-ownership rule
gives to the player, or would produce a roll outside dice.py entirely.

This is deliberately redundant with dice.py's own --owner guard. dice.py
protects the path that goes through dice.py; this protects the paths that do
not -- an inline `python -c "import random"`, a bare `$RANDOM`, a `shuf`. Both
layers exist because the rule has been broken in live play in more than one
way, and prose alone never held.

Blocks:
  * dice.py without --owner
  * dice.py --owner <a PC in the active campaign>
  * inline RNG (python -c random / $RANDOM / shuf / jot -r) in this project

Allows everything else, including dice.py for NPCs, traps and tables.

Exit codes: 0 allow, 2 block (stderr is shown to Claude).
"""

import json
import os
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_SCRIPTS))


def _pc_names() -> list:
    """Character-sheet names for the campaign marked active at /dm:dnd load."""
    try:
        from paths import runtime_dir, find_campaign
        marker = runtime_dir() / "active-campaign.json"
        if not marker.is_file():
            return []
        name = json.loads(marker.read_text(encoding="utf-8")).get("name")
        if not name:
            return []
        chars = find_campaign(name) / "characters"
        return [f.stem for f in chars.glob("*.md")] if chars.is_dir() else []
    except Exception:
        return []


def _owner_is_pc(owner: str) -> "str | None":
    who = owner.strip().strip("\"'").lower()
    if not who:
        return None
    for sheet in _pc_names():
        name = sheet.lower()
        if who == name or name.startswith(who + " ") or who.startswith(name + " "):
            return sheet
        if who == name.split()[0]:
            return sheet
    return None


# One dice.py invocation, with whatever follows it on that command segment.
# The script name has to be run by an interpreter (or be a path) AND be followed
# by a dice notation -- otherwise "dice.py" is just a word in a commit message,
# a heredoc or a doc edit, which is not a roll and must not be blocked.
_DICE_CALL = re.compile(
    r"(?:python3?|py)\s+(?:\S*[/\\])?dice\.py\b([^\n;&|]*)"
    r"|(?<![\w.])(?:\S*[/\\])dice\.py\b([^\n;&|]*)")
_DICE_NOTATION = re.compile(r"(?<![\w])\d*d\d+")
_OWNER_ARG = re.compile(r"--owner\s+(\"[^\"]*\"|'[^']*'|\S+)")

# Rolling a die without the script at all. Split by where the construct lives:
# shell expansions are only real outside quotes, while `python -c "..."` runs
# the quoted text, so it has to be matched against the raw command.
_SHELL_RNG = [
    # $RANDOM, and the arithmetic form $(( RANDOM % 20 + 1 )) where the $ is
    # attached to the expression rather than the variable.
    (re.compile(r"\$RANDOM|\$\(\([^)]*\bRANDOM\b"), "$RANDOM"),
    (re.compile(r"\bshuf\b\s+-i"), "shuf -i"),
    (re.compile(r"\bjot\b\s+-r"), "jot -r"),
]
_INTERPRETER_RNG = [
    (re.compile(r"(?:python3?|py)\s+-c[^\n]*\brandom\b"), "an inline python random call"),
    (re.compile(r"(?:python3?|py)\s+-c[^\n]*\bsecrets\b"), "an inline python secrets call"),
]

RULE_REF = 'SKILL.md, "Dice ownership"'


_QUOTED = re.compile(r"\"[^\"]*\"|'[^']*'", re.DOTALL)


def _executable_part(command: str) -> str:
    """The part of a command that actually runs.

    Everything from the first heredoc operator on is data being written --
    a commit message, a file body, a doc edit -- not commands. Scanning it
    produces false blocks on any text that merely mentions rolling dice.
    """
    return command.split("<<", 1)[0]


def check(command: str) -> "str | None":
    """Return a block reason, or None to allow."""
    command = _executable_part(command)
    for call in _DICE_CALL.finditer(command):
        args = call.group(1) or call.group(2) or ""
        if not _DICE_NOTATION.search(args):
            continue  # no dice notation: not a roll (a --help, a doc line, a path)
        owner = _OWNER_ARG.search(args)
        if not owner:
            return ("dice.py was called without --owner. Name whose die this is "
                    "(an NPC, a monster, \"trap\", \"environment\", \"table\"). "
                    "If it belongs to a player character, do not roll it at all: "
                    f"ask the player for their raw result. See {RULE_REF}.")
        pc = _owner_is_pc(owner.group(1))
        if pc:
            return (f"This die belongs to {pc}, a player character, so it is the "
                    "player's roll. Call for it by name, wait for the raw number, "
                    "then add the modifiers yourself and state the total. "
                    "(Damage arriving AT them from a trap or hazard is yours: "
                    f"roll it with --owner trap instead.) See {RULE_REF}.")

    # Quoted spans are strings being passed around (a commit message, a label,
    # a grep pattern), not shell expansions that produce a number.
    unquoted = _QUOTED.sub(" ", command)
    for patterns, target in ((_SHELL_RNG, unquoted), (_INTERPRETER_RNG, command)):
        for pattern, label in patterns:
            if pattern.search(target):
                return (f"Dice must come from scripts/dice.py, not {label}. "
                        "Re-run it as: dice.py <notation> --owner \"<whose die>\" "
                        f"--label \"<what for>\". See {RULE_REF}.")
    return None


def agent_roll_during_design(payload: dict, command: str) -> "str | None":
    """Agents never roll (plan item 19.9): while a designer command is armed
    (<runtime-dir>/active-design.json, mode birth or detail), a dice.py call
    from a subagent transcript (payload carries agent_id) is refused. The
    conductor pre-rolls every labelled die with design_dice.py and the results
    travel in the agents' inputs."""
    if not payload.get("agent_id"):
        return None
    try:
        from paths import runtime_dir
        marker = runtime_dir() / "active-design.json"
        if not marker.is_file():
            return None
        data = json.loads(marker.read_text(encoding="utf-8"))
    except Exception:
        return None
    if data.get("mode") not in ("birth", "detail"):
        return None
    if data.get("session_id") and payload.get("session_id") and data["session_id"] != payload["session_id"]:
        return None
    exe = _executable_part(command)
    for call in _DICE_CALL.finditer(exe):
        if _DICE_NOTATION.search(call.group(1) or call.group(2) or ""):
            return ("Agents never roll during a designer run. Every die of this phase was pre-rolled "
                    "by the conductor (design_dice.py) and its result is in your inputs; use that value. "
                    f"See {RULE_REF} and plan item 19.9.")
    return None


def player_roll_in_playtest(payload: dict, command: str) -> bool:
    """Slice 1e (plan item 22.5): while a playtest is armed, the player agent (a subagent of a
    `playtest_agent_types` type) may roll its own PC's die with dice.py --player. Nobody else may."""
    if not payload.get("agent_id") or "--player" not in _executable_part(command):
        return False
    try:
        from paths import runtime_dir
        marker = runtime_dir() / "active-design.json"
        if not marker.is_file():
            return False
        data = json.loads(marker.read_text(encoding="utf-8"))
    except Exception:
        return False
    if data.get("mode") != "playtest":
        return False
    types = tuple(data.get("playtest_agent_types") or ("player",))
    return str(payload.get("agent_type") or "") in types


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # unreadable payload: never block on our own error

    if payload.get("tool_name") != "Bash":
        sys.exit(0)
    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        sys.exit(0)

    if player_roll_in_playtest(payload, command):
        reason = None                       # the player's own die, rolled by the player
    else:
        reason = agent_roll_during_design(payload, command) or check(command)
    if reason:
        print(f"BLOCKED by dice_guard: {reason}", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
