# Dev Queue — Ashen Crown

*Skill-level findings from play, waiting for a development pass. Written during a session (or at `/dm:dnd end`), worked through afterwards in a fresh tab whose whole context is the tool.*

*Play tabs append here. They do not edit the skill — a hook blocks that while a session is open, on purpose: development inside a running session fills the play tab with refactoring, and the change gets written with the campaign in view instead of the tool.*

**Format:** one entry per finding. When it happened, what the tool or rule actually did, and what it should have done. Enough that a tab with no memory of the session can act on it.

---

## Open

- **No LICENSE or README.** Needed only if the GitHub repo ever goes public: OGL 1.0a notice for `data/srd-5.1-yaml/` and the JSON built from it, attribution for the upstream fork (`neuralinitiative/claude-dnd-skill`), and a README describing the AIGM vision. *(noted 2026-09-23, repo is private for now)*

## Done

- **Duplicate graph nodes merged.** `npc_solenne_kavash` folded into `npc_kavash`, `npc_iskra_vantrel` into `npc_iskra` (both dead — confirmed by the table), with the other name kept as an alias. `add-node` now refuses a name that already exists, alias included, unless `--allow-duplicate-name` says they really are different people. *(closed 2026-09-23)*

- **Chancellery rewritten for the Kingdom.** The old "keep the three houses balanced" objective ended when Kriv was crowned. Veskin is now a Regent-Chancellor kept in post under supervision after confessing two years of embezzlement (47,000 gp to the Treasury), so his objective is to become necessary to the Crown he stole from before someone else becomes the King's instrument. Power 3 → 2, stance toward the party -1 → +1, and the day-208 confession recorded as his move. *(closed 2026-09-23)*

- **`factions.py check` now flags a faction that has never moved**, once it has been on the board longer than a fortnight — a future-dated step no longer counts as activity. New `created_day` field sets the grace period; backfilled to day 204 for the existing board. It immediately caught House Corr, House Sablewood and House Varn sitting silent for 18 days. *(closed 2026-09-23)*

- **The nested `AIGM/` clone is out of the project.** Moved to `Desktop/AIGM-yedek` on 2026-09-23 — kept as a working backup with its git history and `origin` intact, so the tree no longer holds two different "now". The only remaining second `state.md` is `original-repo/.../party/state.md`, the session-19 archive in the old format, which cannot be confused with the live one. *(closed 2026-09-23)*
