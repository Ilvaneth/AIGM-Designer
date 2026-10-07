#!/usr/bin/env python3
"""
design_read_guard.py — PreToolUse hook: the conductor never reads dm-only.

Plan item 19.1, errata 24.2 #4 and #13, 24.6 #5, docs/reports/2026-09-24-payload-probe.md.

Installed on Read | Grep | Glob | Bash | PowerShell (see .claude/settings.json). Armed only while a
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
  * a caller who may not read dm-only (the conductor in birth and detail, the
    player agent, an ad-hoc agent) may not search a folder that holds
    design/dm-only or design/_staging unless the search keeps them out: a
    Grep or Glob over a parent folder passes only with a glob or type that
    matches no file there now; a recursive shell search or listing (grep -r,
    rg, find, ls -R, tree, git grep, findstr /s, dir /s, Get-ChildItem or
    Select-String -Recurse) on a parent folder is refused (build 19d).
    Only command words are read: a heredoc's body, a quoted string's body and a
    comment are text (build item 21b). A wrapper is read through (build item
    21c): a prefix (env, sudo, time, nohup, command, exec, nice, timeout, xargs,
    PowerShell's `.`) is skipped to the real command, a command string (bash/sh
    -c, eval, powershell -Command, Invoke-Expression, cmd /c) is parsed again,
    a grouping and a process substitution are commands; -EncodedCommand is
    refused, since it cannot be read.
  * any mode, any session, any caller — a shell command that names a runtime
    override (AIGM_TEST_RUNTIME, DND_RUNTIME_DIR) is refused: it would move the
    scripts' own marker checks to an empty runtime (build 19c).

Exit codes: 0 allow, 2 block (stderr is shown to Claude).
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_SCRIPTS))

GUARDED_TOOLS = {"Read", "Grep", "Glob", "Bash", "PowerShell"}
SHELL_TOOLS = {"Bash", "PowerShell"}
PROTECTED = re.compile(r"(?:^|/)design/(?:dm-only|_staging)(?:/|$)")
DEFAULT_AGENT_TYPES = ("workflow-subagent", "design-writer", "design-critic", "design-skeleton")
DEFAULT_PLAYTEST_TYPES = ("player",)
RULE_REF = 'SKILL.md, "The blind conductor"'

# Bash: a path token that points into a protected folder, or a registry verb that prints dm-only.
_PATH_TOKEN = re.compile(r"[\w./\\:~-]*(?:design[/\\](?:dm-only|_staging)[/\\]?[\w./\\-]*)")
_REGISTRY_DM = re.compile(r"registry\.py\b[^\n;&|]*\bshow\b[^\n;&|]*--dm\b")
_REGISTRY_EXPORT = re.compile(r"registry\.py\b[^\n;&|]*\bexport\b(?![^\n;&|]*--public)")
_DICE_SECRET = re.compile(r"design_dice\.py\b[^\n;&|]*\blog\b[^\n;&|]*--secret\b")
# the variables that move paths.runtime_dir(): with one set, a script reads an empty runtime and its own marker checks
# (promise list --dm-only, the playtest-only dice, the used.json guard) see no birth (build 19c)
_RUNTIME_OVERRIDE = re.compile(r"\b(AIGM_TEST_RUNTIME|DND_RUNTIME_DIR)\b", re.IGNORECASE)


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
    if tool == "Glob":                                # a listing shows file names, which can carry secret ids
        path, pattern = inp.get("path", "") or "", inp.get("pattern", "") or ""
        joined = f"{path.rstrip('/').rstrip(chr(92))}/{pattern}" if path and pattern else ""
        return [p for p in (path, pattern, joined) if p]
    if tool in SHELL_TOOLS:
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


# ── a search through a parent folder (build 19d) ─────────────────────────────
# A Grep or Glob whose path holds the protected folders reads inside them unless its filter keeps them out; a filter
# is judged against the files there now (what the search could print at this moment). The shell forms are judged by
# their roots only: a recursive search or listing on a parent folder is refused, whatever its filters.

PROTECTED_DIRS = ("dm-only", "_staging")
# ripgrep's type names whose extensions the protected folders can hold; any other type is its own extension
TYPE_EXTS = {"md": {"md", "markdown", "mdx", "mkd", "mkdn", "mdwn"}, "markdown": {"md", "markdown", "mdx", "mkd", "mkdn", "mdwn"},
             "json": {"json", "jsonl", "geojson", "sarif"}, "yaml": {"yaml", "yml"}, "txt": {"txt"}, "csv": {"csv"}}
_GITBASH_DRIVE = re.compile(r"^/([a-zA-Z])(/|$)")
_HEREDOC = re.compile(r"<<(-?)[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")


def _close_paren(text: str, start: int) -> int:
    """The index of the `)` that closes the `(` at `start` (the end of the text when it never closes)."""
    depth, i = 0, start
    while i < len(text):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(text)


def _command_segments(command: str, posix: bool = True) -> list[str]:
    """The commands of a Bash or PowerShell line, each as its own text (build item 21b: the guard read a heredoc's body
    as commands and refused the design tab's `find` in it). The line splits on `;`, `&`, `|` and newlines outside
    quotes; a heredoc's body (`<<EOF` … `EOF`), a PowerShell here-string (`@'` … `'@`), a comment and a quoted
    string's body are text and never a command; a command substitution (`$(…)`, a backtick pair in Bash), quoted or
    not, is a command and its own segments are returned too."""
    segs: list[str] = []
    cur: list[str] = []
    heredocs: list[tuple[str, bool]] = []
    quote = None
    esc = "\\" if posix else "`"
    i, n = 0, len(command or "")
    text = command or ""

    def flush():
        s = "".join(cur).strip()
        if s:
            segs.append(s)
        cur.clear()

    while i < n:
        c = text[i]
        if quote:
            if c == esc and quote == '"' and i + 1 < n:
                cur.append(text[i:i + 2])
                i += 2
                continue
            if c == quote:
                if not posix and i + 1 < n and text[i + 1] == quote:      # PowerShell's doubled quote inside a string
                    cur.append(c * 2)
                    i += 2
                    continue
                quote = None
                cur.append(c)
                i += 1
                continue
            if quote == '"' and text.startswith("$(", i):
                j = _close_paren(text, i + 1)
                segs.extend(_command_segments(text[i + 2:j], posix))
                cur.append(text[i:j + 1])
                i = j + 1
                continue
            if quote == '"' and posix and c == "`":
                j = text.find("`", i + 1)
                j = n if j < 0 else j
                segs.extend(_command_segments(text[i + 1:j], posix))
                cur.append(text[i:j + 1])
                i = j + 1
                continue
            cur.append(c)
            i += 1
            continue
        if c == esc and i + 1 < n:
            cur.append(text[i:i + 2])
            i += 2
            continue
        if not posix and text.startswith(("@'", '@"'), i) and text[i + 2:i + 3] in ("\n", "\r"):
            end = text.find("\n" + text[i + 1] + "@", i + 2)
            i = n if end < 0 else end + 3                  # a here-string's body is text
            cur.append("''")
            continue
        if not posix and text.startswith("<#", i):
            end = text.find("#>", i + 2)
            i = n if end < 0 else end + 2
            continue
        if c == "#" and (not cur or cur[-1].isspace()):
            end = text.find("\n", i)
            i = n if end < 0 else end                       # a comment runs to the end of its line
            continue
        if c in "'\"":
            quote = c
            cur.append(c)
            i += 1
            continue
        if posix and text.startswith("<<", i) and not text.startswith("<<<", i):
            m = _HEREDOC.match(text, i)
            if m:
                heredocs.append((m.group(3), m.group(1) == "-"))
                cur.append(" ")
                i = m.end()
                continue
        if text.startswith(("$(", "<(", ">("), i):          # build item 21c: a process substitution too
            j = _close_paren(text, i + 1)
            segs.extend(_command_segments(text[i + 2:j], posix))
            cur.append(" ")
            i = j + 1
            continue
        if posix and c == "`":
            j = text.find("`", i + 1)
            j = n if j < 0 else j
            segs.extend(_command_segments(text[i + 1:j], posix))
            cur.append(" ")
            i = j + 1
            continue
        if c == "\n":
            flush()
            i += 1
            for delim, dash in heredocs:                   # each body runs to its delimiter's own line
                while i < n:
                    end = text.find("\n", i)
                    line = text[i:n if end < 0 else end].rstrip("\r")
                    i = n if end < 0 else end + 1
                    if (line.lstrip("\t") if dash else line) == delim:
                        break
            heredocs.clear()
            continue
        if c in ";&|":
            flush()
            i += 1
            continue
        cur.append(c)
        i += 1
    flush()
    return segs


def _abs(path: str, cwd: Path) -> Path:
    path = _GITBASH_DRIVE.sub(lambda m: f"{m.group(1)}:/", path.strip())
    p = Path(path).expanduser()
    try:
        return (p if p.is_absolute() else cwd / p).resolve()
    except Exception:
        return cwd / p


def _protected_files(search: Path, root: Path) -> list[str] | None:
    """The protected files a search rooted at `search` reaches, relative to it (posix); None when it holds none."""
    out, held = [], False
    for name in PROTECTED_DIRS:
        d = (root / "design" / name).resolve()
        if not d.is_dir():
            continue
        try:
            d.relative_to(search)                     # the search root holds this folder (or is it)
        except ValueError:
            try:
                search.relative_to(d)                 # or lies inside it
            except ValueError:
                continue
        held = True
        for f in d.rglob("*"):
            if f.is_file():
                try:
                    out.append(f.relative_to(search).as_posix())
                except ValueError:
                    out.append(f.name)
    return out if held else None


def _braces(glob: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", glob)
    if not m:
        return [glob]
    return [x for alt in m.group(1).split(",") for x in _braces(glob[:m.start()] + alt + glob[m.end():])]


def _glob_rx(glob: str) -> str:
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("**", i):
            out, i = out + ".*", i + 2
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif glob[i] == "?":
            out, i = out + "[^/]", i + 1
        elif glob[i] == "[" and glob.find("]", i + 1) > i:
            j = glob.find("]", i + 1)
            cls = glob[i + 1:j]
            out, i = out + "[" + ("^" + cls[1:] if cls.startswith("!") else cls) + "]", j + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return out


def _glob_hits(glob: str, rel: str) -> bool:
    """ripgrep's glob reading: no slash matches any one segment; a slash anchors it at the search root, and a glob
    that matches a folder takes in everything under it."""
    segs = rel.split("/")
    for alt in _braces(glob.replace("\\", "/")):
        g = alt.rstrip("/")
        if g.startswith("./"):
            g = g[2:]
        if "/" not in g:
            if any(fnmatch.fnmatchcase(s.lower(), g.lower()) for s in segs):
                return True
            continue
        rx = re.compile(_glob_rx(g.lstrip("/")), re.IGNORECASE)
        if any(rx.fullmatch("/".join(segs[:n])) for n in range(1, len(segs) + 1)):
            return True
    return False


def _filtered(files: list[str], glob: str, ftype: str) -> list[str]:
    """The protected files a Grep's glob and type (or a Glob's pattern) let through."""
    if glob:
        files = ([f for f in files if not _glob_hits(glob[1:], f)] if glob.startswith("!")
                 else [f for f in files if _glob_hits(glob, f)])
    if ftype:
        exts = TYPE_EXTS.get(ftype.lower(), {ftype.lower()})
        files = [f for f in files if f.rsplit(".", 1)[-1].lower() in exts and "." in f.rsplit("/", 1)[-1]]
    return files


# build item 21c: a search wrapped in another command is judged as the command it wraps. A prefix runs the command
# after it (its options, and the arguments its options take, skipped); a command string is parsed again as commands.
_PREFIXES = {"env": {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}, "sudo": {"-u", "-g", "-C", "-h", "-p", "-U", "-r", "-t"},
             "doas": {"-u", "-C"}, "time": {"-o", "-f"}, "nohup": set(), "command": set(), "exec": {"-a"}, "nice": {"-n"},
             "ionice": {"-c", "-n", "-p"}, "stdbuf": {"-i", "-o", "-e"}, "timeout": {"-s", "--signal", "-k", "--kill-after"},
             "xargs": {"-n", "-I", "-d", "-P", "-L", "-s", "-a", "-E", "--max-args", "--replace", "--delimiter",
                       "--max-procs", "--max-lines", "--arg-file", "--eof"},
             ".": set()}
_SHELLS = ("bash", "sh", "zsh", "dash", "ksh")
_PS = ("powershell", "pwsh")
_PS_COMMAND = re.compile(r"^-c(?:o(?:m(?:m(?:a(?:n(?:d)?)?)?)?)?)?$", re.IGNORECASE)
_PS_ENCODED = re.compile(r"^-(?:e|ec|en|enc|enco|encod|encode|encoded|encodedc\w*)$", re.IGNORECASE)
ENCODED = "an encoded command"


def _unwrap(toks: list[str]) -> list[str]:
    """The tokens from the real command word on: VAR=value assignments and the prefixes skipped, a grouping's brackets
    taken off."""
    while toks:
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]):
            toks = toks[1:]                           # VAR=value prefixes
            continue
        if toks[0] in ("(", "((", "{"):
            toks = toks[1:]
            continue
        if toks[0].startswith("(") and len(toks[0]) > 1:
            toks = [toks[0].lstrip("(")] + toks[1:]
            continue
        word = "." if toks[0] == "." else Path(toks[0].replace("\\", "/")).name.lower().removesuffix(".exe")
        if word not in _PREFIXES:
            break
        takes, rest = _PREFIXES[word], toks[1:]
        while rest and (rest[0].startswith("-") or (word == "env" and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", rest[0]))):
            opt = rest.pop(0)
            if opt in takes and rest:
                rest.pop(0)                           # the option's own argument
        if word == "timeout" and rest:
            rest = rest[1:]                           # the duration
        toks = rest
    while toks and toks[-1] in (")", "))", "}"):
        toks = toks[:-1]
    if toks and toks[-1].endswith(")") and toks[-1].count("(") < toks[-1].count(")"):
        toks = toks[:-1] + [toks[-1].rstrip(")")]
    return toks


def _command_string(word: str, args: list[str]) -> tuple[str, bool] | None:
    """(the command string a wrapper runs, read as POSIX or not), ENCODED for an unreadable one, or None."""
    if word in _SHELLS:
        for n, a in enumerate(args):
            if re.fullmatch(r"-[A-Za-z]*c[A-Za-z]*", a) and n + 1 < len(args):
                return args[n + 1], True
        return None
    if word == "eval":
        return " ".join(args), True
    if word in _PS:
        for n, a in enumerate(args):
            if _PS_ENCODED.match(a):
                return ENCODED, False
            if _PS_COMMAND.match(a):
                return " ".join(args[n + 1:]), False
        return None
    if word in ("invoke-expression", "iex"):
        return " ".join(a for a in args if not _PS_COMMAND.match(a)), False
    if word == "cmd":
        for n, a in enumerate(args):
            if a.lower() in ("/c", "/k"):
                return " ".join(args[n + 1:]), False
    return None


def _shell_roots(command: str, cwd: Path, posix: bool = True, depth: int = 0) -> list[tuple[str, Path | None]]:
    """(the command word, a root) for every recursive search or listing in a Bash or PowerShell command; a wrapper's
    command string is read too (build item 21c), and an encoded one is (word, None)."""
    out = []
    for seg in _command_segments(command or "", posix):
        try:
            toks = shlex.split(seg, posix=posix)
        except ValueError:
            toks = seg.split()
        if not posix:                                 # PowerShell: backslashes are path separators, quotes stay on
            toks = [t[1:-1] if len(t) > 1 and t[0] == t[-1] and t[0] in "\"'" else t for t in toks]
        toks = _unwrap(toks)
        if not toks:
            continue
        word = Path(toks[0].replace("\\", "/")).name.lower().removesuffix(".exe")
        args = toks[1:]
        wrapped = _command_string(word, args)
        if wrapped is not None:
            inner, inner_posix = wrapped
            if inner == ENCODED:
                out.append((f"{word} -EncodedCommand", None))
            elif depth < 8:
                out.extend(_shell_roots(inner, cwd, inner_posix, depth + 1))
            continue
        if word == "git" and args[:1] == ["grep"]:
            word, args = "git grep", args[1:]
        low = [a.lower() for a in args]
        short = [a[1:] for a in args if re.fullmatch(r"-[A-Za-z]+", a)]
        if word in ("grep", "egrep", "fgrep"):
            recursive = any(a in ("--recursive", "--dereference-recursive") for a in low) or any("r" in s.lower() for s in short)
        elif word in ("rg", "ripgrep", "find", "tree", "ag", "ack", "rgrep", "git grep"):
            recursive = True
        elif word in ("ls", "dir", "gci", "get-childitem", "select-string", "sls"):
            recursive = (any(re.fullmatch(r"-rec\w*", a) or a in ("--recursive", "/s") for a in low)
                         or (word in ("ls", "dir") and any("R" in s for s in short)))
        elif word == "findstr":
            recursive = any(re.fullmatch(r"/[a-z]*s[a-z]*", a) for a in low)
        else:
            recursive = False
        if not recursive:
            continue
        roots = []
        for a in args:
            if a.startswith("-") or (a.startswith("/") and len(a) <= 3 and word in ("findstr", "dir")):
                continue
            parts = re.split(r"[\\/]", a)
            cut = next((i for i, s in enumerate(parts) if any(c in s for c in "*?[")), None)
            base = "/".join(parts[:cut]) if cut is not None else a
            if cut is not None and not base:
                continue                              # a bare wildcard: the search root stays the working folder
            p = _abs(base or ".", cwd)
            if p.exists():
                roots.append(p)
        out.extend((word, r) for r in (roots or [cwd]))
    return out


def _ancestor_search(payload: dict, root: Path | None) -> str | None:
    """A description of a search that reaches the protected folders through a parent folder, or None."""
    if root is None:
        return None
    tool = payload.get("tool_name")
    inp = payload.get("tool_input") or {}
    cwd = Path(payload.get("cwd") or os.getcwd())
    if tool in ("Grep", "Glob"):
        search = _abs(inp.get("path") or ".", cwd)
        files = _protected_files(search, root)
        if files is None:
            return None
        glob = inp.get("glob", "") if tool == "Grep" else inp.get("pattern", "")
        ftype = inp.get("type", "") if tool == "Grep" else ""
        if tool == "Grep" and not glob and not ftype:
            return f"Grep over {search} with no glob or type"
        hit = _filtered(files, glob or "", ftype or "")
        if hit:
            return f"{tool} over {search} ({glob or ftype}) reaches {hit[0]}"
        return None
    if tool in SHELL_TOOLS:
        for word, r in _shell_roots(inp.get("command", "") or "", cwd, posix=tool == "Bash"):
            if r is None:
                return f"{word}, which cannot be read"      # build item 21c: an encoded command is refused while armed
            if _protected_files(r, root) is not None:
                return f"{word} over {r}"
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
    command = (payload.get("tool_input") or {}).get("command", "") if payload.get("tool_name") in SHELL_TOOLS else ""
    override = _RUNTIME_OVERRIDE.search(command or "")
    if override:
        return (f"A design marker is armed ({marker['campaign']}): a command may not name {override.group(1)}. "
                f"It moves the runtime directory, so the scripts' own marker checks would read an empty runtime "
                f"and see no birth. Run the command without it; the test suite sets its own runtime itself.")
    if marker.get("session_id") and payload.get("session_id") and marker["session_id"] != payload["session_id"]:
        return None                                   # another tab's marker
    mode = marker.get("mode", "birth")
    agent_id = payload.get("agent_id")
    agent_type = payload.get("agent_type") or ""
    root = _campaign_root(marker["campaign"])
    touched = _paths_touched(payload)
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
            search = _ancestor_search(payload, root)
            if search:
                return (f"The player agent may not search a folder that holds design/dm-only or design/_staging "
                        f"({search}). See {RULE_REF}.")
            return None
        # other agents in a playtest follow the birth rule below

    allowed_types = tuple(marker.get("agent_types_allowed") or DEFAULT_AGENT_TYPES)
    if agent_id and agent_type in allowed_types:
        return None                                   # a designer agent, fresh context: may read dm-only
    who = "an agent of type " + repr(agent_type) if agent_id else "the conductor"
    if not protected and not verb:
        search = _ancestor_search(payload, root)
        if not search:
            return None
        return (f"Design mode '{mode}' is armed for {marker['campaign']}: {who} may not search a folder that holds "
                f"design/dm-only or design/_staging unless the search keeps them out ({search}). Give a path outside "
                f"the campaign's design folder, or a Grep/Glob glob or type that matches no file there. See {RULE_REF}.")
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
