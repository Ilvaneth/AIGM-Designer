# PreToolUse payload probe (slice 0, item B)

*Reference material behind plan item 19.1 and risk 24.1 #12. The plan wins on any conflict; the probe result is folded into 19.1 as a dated paragraph.*

## Question

`design_read_guard.py` (slice 1) must tell the **conductor** (the main session, which may never read `design/dm-only/**`) from a **generation agent** (a fresh-context subagent that must read it). Plan item 19.1 assumed the hook could discriminate by `transcript_path` (`agent-*.jsonl` for subagents). Risk 24.1 #12 said: probe the payload first, design on what is observed.

## Method

Three temporary lines in `hooks/dice_guard.py` (the only hook already registered on `Bash`; a new hook registration does not take effect until the session restarts) appended every payload plus the hook process's `DND_*` / `CLAUDE*` environment and the `paths.runtime_dir()` it resolved to `.runtime/probe/payloads.jsonl`. Then one `echo` through Bash from each caller kind:

| # | Caller | How |
|---|---|---|
| 1 | conductor | the main session's own Bash call |
| 2 | Agent-tool subagent | `Agent` tool, `general-purpose`, one Bash call |
| 3 | Workflow agent | `Workflow` tool, one `agent()` with one Bash call |

Instrumentation reverted and the dump deleted afterwards (it carries the session's messaging token). Claude Code desktop 2.7032.0, Agent SDK 0.3.280, Windows 11.

## Observed payloads

Fields present, by caller (values are ids or paths; identical across callers unless noted):

| Field | conductor | Agent-tool subagent | Workflow agent |
|---|---|---|---|
| `hook_event_name` | `PreToolUse` | same | same |
| `tool_name`, `tool_input`, `tool_use_id` | yes | yes | yes |
| `session_id` | the session | **same** | **same** |
| `transcript_path` | `<project-dir>/<session_id>.jsonl` | **same file** | **same file** |
| `prompt_id` | the turn | same | same |
| `cwd`, `scratchpad_dir`, `permission_mode` | project dir / scratchpad / `auto` | same | same |
| `effort` | `{"level": "xhigh"}` | absent | `{"level": "low"}` (the agent's own) |
| **`agent_id`** | **absent** | `a2b0…` | `abae…` |
| **`agent_type`** | **absent** | `general-purpose` | `workflow-subagent` |

Environment seen by the hook process (same for all three): `CLAUDECODE=1`, `CLAUDE_PROJECT_DIR=<this project>`, `CLAUDE_CODE_SESSION_ID=<session>`, `CLAUDE_EFFORT` (conductor and workflow agent only), assorted `CLAUDE_CODE_*` flags, **no `CLAUDE_SKILL_DIR`**, no agent-related variable, and `DND_CAMPAIGN_ROOT=<Ashen Crown>` (the machine-wide leak). `paths.runtime_dir()` inside the hook resolved to `<this project>/.runtime` in all three records: A0's project scoping holds in the hook process, with the leaked variable present.

## Findings

1. **`transcript_path` does not discriminate.** All three callers report the main session's transcript. The `agent-*.jsonl` assumption in 19.1 is wrong on this version; a guard keyed on it would treat every agent as the conductor and block the whole birth.
2. **`agent_id` presence does.** The conductor's payload has no `agent_id` / `agent_type`; every subagent's payload has both. This is a structural field of the payload, not a path convention.
3. **`agent_type` names the kind of agent.** `general-purpose` for the Agent tool's default, `workflow-subagent` for Workflow's default; the Workflow `agentType` option and the Agent tool's `subagent_type` resolve custom types from the same registry, so a custom agent definition would surface under its own name here. That is the natural key for item 22.5's playtest allowlist (a `player` agent type is denied dm-only regardless of `mode`) and for narrowing which agents may read dm-only at all.
4. **Nothing in the environment discriminates.** The hook cannot be armed or keyed through env; the `active-design.json` marker (19.1) remains the arming mechanism.
5. **`session_id` and `prompt_id` are shared** by the conductor and its agents, so a marker written per designer command can be matched to the session that armed it, which stops a marker from one tab acting on another tab's hooks.
6. **`CLAUDE_SKILL_DIR` is not set for hooks.** `paths.skill_root()` falls back to the file's own location, as A0 requires.

## Decision (folded into plan 19.1)

`design_read_guard.py` discriminates on **`agent_id` presence**: absent → conductor → dm-only denied while armed; present → agent → allowed, subject to `mode` and the `agent_type` allowlist in `active-design.json` (`playtest` denies the player agent type; `birth` / `detail` allow the designer's agent types and deny others, `general-purpose` included, so an ad-hoc agent from the play tab cannot become a leak channel). The same test serves `dice_guard`'s "agents never roll during birth" extension (21.F). The 24.1 #12 fallback (conductor-side deny with pre-copied inputs) is not needed. The hook tests in slice 1 add both payload shapes as cases, and a re-probe is due if a Claude Code upgrade changes the payload (the version is recorded above).
