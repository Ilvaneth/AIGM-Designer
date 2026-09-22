# Ashen Crown — Self-Contained D&D Project

This directory is a fully self-contained D&D 5e campaign project:
- **Skill engine:** `.claude/skills/dnd/` (project-scoped — not installed globally)
- **Campaign data:** `campaigns/ashen-crown/` (state.md, world.md, npcs.md, npcs-full.md, characters/, reference/, graph.json)
- **Historical archive:** `original-repo/campaigns/ashen-crown/` (the full 19-session prior history in its original format — read on demand, never edited)

## Critical — always set DND_CAMPAIGN_ROOT explicitly

The skill's scripts (`paths.py` and everything that imports it) resolve campaign data via the `DND_CAMPAIGN_ROOT` environment variable. It was persisted via `setx` on 2026-09-06, but **that only takes effect for processes started after a full restart of the Claude Code application** (closing it completely, not just opening a new tab/conversation in an already-running instance) — a shell inherited from an already-running app instance will NOT see it.

**Do not assume the environment variable is set.** Before running ANY script under `.claude/skills/dnd/scripts/`, always prefix the command with the variable explicitly:

```bash
DND_CAMPAIGN_ROOT="C:/Users/armag/Desktop/Ashen-Crown_New_DM" py "C:/Users/armag/Desktop/Ashen-Crown_New_DM/.claude/skills/dnd/scripts/<script>.py" ...
```

If you skip this and a script reports the campaign as missing (or only shows unrelated campaigns like a legacy `kara-ahit`), this is why — it fell back to the default root (`~/.claude/dnd/`). Re-run with the explicit prefix above rather than concluding the campaign doesn't exist.

The campaign name for all `--campaign` flags is **`ashen-crown`**.

## Ruleset

2014 (SRD 5.1). See `campaigns/ashen-crown/state.md` header.
