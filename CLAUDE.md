# AIGM — Campaign Designer (development project)

This folder is the **development project** for the D&D 5e (2014) DM skill and its Campaign Designer. No live campaign lives here.

- **Skill engine:** `.claude/skills/dnd/` (project-scoped). This is what gets developed.
- **The plan:** `docs/campaign-designer-plan.md` — 24 items, all decided on 2026-09-24. Every development session starts by reading item 24 (risk register, errata, build order 24.3, cut list 24.4, strengths to preserve 24.5) and then the slice being built. v3.0 = slices 0-2 (birth pipeline + living world); the user starts the next campaign only after v3.0 is complete.
- **Ashen Crown is played elsewhere:** `C:\Users\armag\Desktop\Ashen-Crown_New_DM` is a separate project with its own tab and its own copy of the skill. Never read or edit that folder from here, and never copy changes into it by hand; the two skills are synced deliberately, at the user's request, once a slice is done.
- **History:** this repository was split from the Ashen Crown project on 2026-09-24 (`git clone`, then `campaigns/` and `original-repo/` removed). Older commits still contain campaign files, so never read them for content (a headings-only look already leaked a few Ashen Crown labels into a dev transcript). `origin` is github.com/Ilvaneth/AIGM-Designer; the original repository is github.com/Ilvaneth/AIGM. Push only when the user asks (their rule: one green commit per work item, push when a slice is done).
- **Status:** slices 0, 1a and 1b delivered (plan 24.3; 1b on 2026-09-25: the 25 `data/design/*.yaml` tables, `design_tables.py`, `build_design_index.py` → `srd-index-2014.json`); slice 1c items 1-7 delivered 2026-09-25 (`designer.py`, the prompt library, `design_approval.py`, `design_revise.py`, `render_player.py`, the two Workflows under `.claude/workflows/`, `SKILL-design.md`); item 8, the tuning births, waits for the user's `workflow` go (test births auto-approve). Then slice 1d, play integration. The fixture bible is `.claude/skills/dnd/tests/fixtures/salt-lantern/`, the schemas `docs/schemas/`.

## Data root — project-scoped, never the environment

The skill's scripts and hooks resolve campaign data through `paths.py`. Since slice 0 (A0) a copy of the skill inside a project uses **that project** as its data root: `paths.project_root()` walks up from the skill to the folder holding `.claude/`, and if that folder carries `campaigns/` or `.runtime/` the environment is ignored. `DND_CAMPAIGN_ROOT` only decides the root for a plugin or standalone install. The user's machine-wide `setx` value points at the **Ashen Crown** folder and leaks into every tool shell and hook subprocess; before A0 that made this project's edit guard read Ashen Crown's open session. `campaigns/.gitkeep` is committed so the project marker survives a fresh clone (`.runtime/` is gitignored). Check with:

```bash
py .claude/skills/dnd/scripts/paths.py project-root
```

If a script ever reports `ashen-crown` as an active campaign, the project marker is missing; restore `campaigns/` and re-run. Test campaigns generated during development live under `campaigns/_test-*/` (gitignored, plan item 22.6). `.name_registry.json` at the root is kept on purpose: it holds the names Ashen Crown registered from session 38 on, so new campaigns never reuse them (plan items 4.6, 8.7); the earlier Ashen Crown names the owner tired of (Cassivar, Corvina and every Corv-/Corw- derivative, Emberhold, Cinder Choir) are banned outright in `data/design/naming.yaml`'s owner blacklist, beside a list of the model's favourite fantasy names.

Tests: `py .claude/skills/dnd/scripts/run_tests.py` (stdlib `unittest`, discovers `.claude/skills/dnd/tests/`).

## Rules of this project

- Ruleset 2014 (SRD 5.1) only; 2024 support was removed on 2026-09-24 (plan item 21.G). The `**Ruleset:** 2014` state.md header line stays as a harmless stamp.
- Development artifacts (code, tables, plan, commit messages) in English; conversation with the user in Turkish.
- **The narration is Turkish, the world is not** (owner ruling 2026-09-25, errata 24.2 #17): every proper noun a campaign produces — persons, places, institutions, gods, ships, signature phenomena and creatures, months — is an English-language fantasy name, carried into Turkish prose with an apostrophe suffix (Lanternside'a). Common nouns stay Turkish. No word-stem blacklist: uniqueness is on full names and table rows (errata #18).
- The user's stated rules are the spec: a conflicting upstream behaviour is deleted, never kept as a default.
- `unittest` (stdlib), run by `scripts/run_tests.py` once it exists; keep the existing hook tests green.
- Commit only when the user asks.
