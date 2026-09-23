# Dev Queue — Ashen Crown

*Skill-level findings from play, waiting for a development pass. Written during a session (or at `/dm:dnd end`), worked through afterwards in a fresh tab whose whole context is the tool.*

*Play tabs append here. They do not edit the skill — a hook blocks that while a session is open, on purpose: development inside a running session fills the play tab with refactoring, and the change gets written with the campaign in view instead of the tool.*

**Format:** one entry per finding. When it happened, what the tool or rule actually did, and what it should have done. Enough that a tab with no memory of the session can act on it.

---

## Open

- **Campaign content, not tool: rename the Bonewrights' spokesperson in `npcs-full.md` and the graph.** The entry "Vashti Coldharrow (Bonewrights — lich)" collides with the Vashti Coldharrow of Sylandra's test (destroyed, session 27). `reference/bonewrights-hall.md` (written session 39) uses **Thessaly Ondrel** for the Bonewrights' lich; `npcs-full.md`, `npcs.md` and `graph.json` still say Vashti. *(noted 2026-09-23)*

- **`xp.py award` cannot write XP into the character sheets.** Session 39 (gün 222): it warned "no XP field found in kriv shestendeliath.md" and reported "0 + 3,600 = 3,600 / 300 LEVEL 2 UP" for two level-18 characters. The sheet's `| **Experience Points** | 290942 (...long annotation...) |` row has a long parenthetical after the number, which the field parser evidently cannot read. It should parse the leading integer and ignore the annotation, and refuse to print a level-up banner when it found no XP. XP was written by hand this time. *(noted 2026-09-23)*

- **Kriv's combat shorthand note in `state.md → DM Style Notes` gives a stale flat modifier.** It says "+9 (STR 7 + weapon 2)", written when his STR was 25. The sheet's Attacks table (STR 29, Wardensteel) says 1d12+11. The table is right, the note is not; whatever the DM Style Notes mean by "already summed on the sheet" should not carry its own number. *(noted 2026-09-23)*

- **Save gaps from session 38 that the next load could not recover.** (a) The Umm-Halad road entrance ("found on the way to Ivrathax, Ilvaneth wrote a detailed description in her spellbook") appears nowhere in the sheet or logs; state.md only says "standing stone clue, not visited". (b) The verification method Ilvaneth proposed to Ashen Corwyn at the coronation feast is not written anywhere. Both were only recoverable because the player restated them. `/dm:dnd save` should ask for "what did the party learn about routes, entrances and offers made to strangers". *(noted 2026-09-23)*

- **No LICENSE or README.** Needed only if the GitHub repo ever goes public: OGL 1.0a notice for `data/srd-5.1-yaml/` and the JSON built from it, attribution for the upstream fork (`neuralinitiative/claude-dnd-skill`), and a README describing the AIGM vision. *(noted 2026-09-23, repo is private for now)*

## Done

- **Duplicate graph nodes merged.** `npc_solenne_kavash` folded into `npc_kavash`, `npc_iskra_vantrel` into `npc_iskra` (both dead — confirmed by the table), with the other name kept as an alias. `add-node` now refuses a name that already exists, alias included, unless `--allow-duplicate-name` says they really are different people. *(closed 2026-09-23)*

- **Chancellery rewritten for the Kingdom.** The old "keep the three houses balanced" objective ended when Kriv was crowned. Veskin is now a Regent-Chancellor kept in post under supervision after confessing two years of embezzlement (47,000 gp to the Treasury), so his objective is to become necessary to the Crown he stole from before someone else becomes the King's instrument. Power 3 → 2, stance toward the party -1 → +1, and the day-208 confession recorded as his move. *(closed 2026-09-23)*

- **`factions.py check` now flags a faction that has never moved**, once it has been on the board longer than a fortnight — a future-dated step no longer counts as activity. New `created_day` field sets the grace period; backfilled to day 204 for the existing board. It immediately caught House Corr, House Sablewood and House Varn sitting silent for 18 days. *(closed 2026-09-23)*

- **The nested `AIGM/` clone is out of the project.** Moved to `Desktop/AIGM-yedek` on 2026-09-23 — kept as a working backup with its git history and `origin` intact, so the tree no longer holds two different "now". The only remaining second `state.md` is `original-repo/.../party/state.md`, the session-19 archive in the old format, which cannot be confused with the live one. *(closed 2026-09-23)*
