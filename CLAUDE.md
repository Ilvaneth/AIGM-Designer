# AIGM — Campaign Designer (development project)

This folder is the **development project** for the D&D 5e (2014) DM skill and its Campaign Designer. No live campaign lives here.

- **Skill engine:** `.claude/skills/dnd/` (project-scoped). This is what gets developed.
- **The plan:** `docs/campaign-designer-plan.md` — 24 items, all decided on 2026-09-24. Every development session starts by reading item 24 (risk register, errata, build order 24.3, cut list 24.4, strengths to preserve 24.5) and then the slice being built. v3.0 = slices 0-2 (birth pipeline + living world); the user starts the next campaign only after v3.0 is complete.
- **Ashen Crown is played elsewhere:** `C:\Users\armag\Desktop\Ashen-Crown_New_DM` is a separate project with its own tab and its own copy of the skill. Never read or edit that folder from here, and never copy changes into it by hand; the two skills are synced deliberately, at the user's request, once a slice is done.
- **History:** this repository was split from the Ashen Crown project on 2026-09-24 (`git clone`, then `campaigns/` and `original-repo/` removed). Older commits still contain campaign files; `origin` was removed at the split — add a remote only when the user asks. The original repository is github.com/Ilvaneth/AIGM.

## DND_CAMPAIGN_ROOT — always explicit

The skill's scripts and hooks resolve campaign data through `DND_CAMPAIGN_ROOT`. The user's machine-wide `setx` value points at the **Ashen Crown** folder; this project sets its own value in `.claude/settings.json` (`env`), but do not rely on inheritance. **Prefix every script call explicitly:**

```bash
DND_CAMPAIGN_ROOT="C:/Users/armag/Desktop/Campaign-Designer" py "C:/Users/armag/Desktop/Campaign-Designer/.claude/skills/dnd/scripts/<script>.py" ...
```

If a script ever reports `ashen-crown` as an active campaign, the variable leaked from the machine-wide value; re-run with the prefix. Test campaigns generated during development live under `campaigns/_test-*/` (gitignored, plan item 22.6). `.name_registry.json` at the root is kept on purpose: it holds every name Ashen Crown used, so new campaigns never reuse them (plan items 4.6, 8.7).

## Rules of this project

- Ruleset 2014 (SRD 5.1) only; 2024 support is scheduled for removal (plan item 21.G).
- Development artifacts (code, tables, plan, commit messages) in English; conversation with the user in Turkish.
- The user's stated rules are the spec: a conflicting upstream behaviour is deleted, never kept as a default.
- `unittest` (stdlib), run by `scripts/run_tests.py` once it exists; keep the existing hook tests green.
- Commit only when the user asks.
