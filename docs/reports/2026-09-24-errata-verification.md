# Errata pass and verification (plan 24.2 → items 1-23)

> **Agent output, not a decision.** Produced on 2026-09-24 by a read-only multi-agent pass during the planning session. Where anything here disagrees with `docs/campaign-designer-plan.md`, the plan is authoritative. Kept as reference for the build (schemas, measurements, the full finding lists the plan condensed).

Workflow 1: one editor folded the 16 errata of plan 24.2 and the six decisions of 24.6 into the item texts (57 targeted edits, provenance markers). Workflow 2: two checkers (coverage, fidelity against the pre-edit backup) and one fixer. All material issues were applied; two nits were closed by hand.

## Editor — edits applied

- 24.2 #1 / 24.6 #1 → item Standing principles: Data-first bullet now names the canonical dm-only registry and the public+discoverable projection
- 24.2 #2 → item Standing principles: Added bullet: Immutable = stamped fields; play-time truth lives in the overlay (design/overlay.json)
- 24.2 #1 / 24.6 #1 → item 3: File bullet: canonical registry at design/dm-only/entities.json; design/entities.json is the generated projection regenerated on every merge, the only form the conductor and campaign_search see
- 24.2 #1 / 24.6 #1 → item 11.2: Replaced 'reads design/ freely' with the owner's free-reading surface (primer, player map, approval cards, PC thread public faces); rest of design/ outside dm-only is DM-open, player-avoid (CLAUDE.md line); canonical registry lives in dm-only
- 24.2 #1 → item 16.2: campaign_search.py excludes dm-only (and the canonical registry) by default, searching only the projection
- 24.2 #1 / 24.6 #1 → item 19.1: Added: the conductor reads only the projection design/entities.json; the canonical dm-only registry is never opened by it
- 24.2 #2 → item 1: 'Immutable' defined as stamped fields; listed overlay fields and the overlay's only writers (simulate, site_progress.py, campaign_graph.py, factions.py, registry.py play-set)
- 24.2 #2 → item 14.1: World events touching a designed entity's current state go to design/overlay.json (writers named); immutable covers stamped fields only
- 24.2 #2 → item 14.3: Clarified that the seen_in_play flag is held in the overlay, not the registry (consistency with 16.5)
- 24.2 #2 → item 16.1: world.md/npcs.md render design ⊕ overlay with a 'changed since birth' marker on overlaid values
- 24.2 #2 → item 16.5: seen_in_play lives in design/overlay.json, not in the registry
- 24.2 #2 → item 3: Registry field list: status, seen_in_play, npc location and settlement ruler declared overlay fields (registry keeps birth value, overlay the play-time one)
- 24.2 #2 → item 15.1: Added the `overlay` validator module row (keys resolve, only overlay fields overridden, writer+day recorded)
- 24.2 #3 / 24.6 #4 → item 7.5: Only BBEG and lieutenants are major tier with goals.py records; regional villains are supporting tier (dossier, no tracker, front lives on the faction's operation)
- 24.2 #3 / 24.6 #4 → item 8.1: Caps re-derived to 14-18 / 30-40 / 60-80 with P9 headroom; stacking rules added (≤2 roles per person, ruler = polity leader, lieutenant = faction leader, heir/betrayal/anchor owner default minor or stub, socket NPCs from roster, sockets party×2 in short); validator counts roles per person and unfilled
- 24.2 #3 / 24.6 #4 → item 8.2: Tier counts marked as predating the re-derived caps, rescaled in scale.yaml; major tier = BBEG + lieutenants only, regional villains supporting
- 24.2 #3 / 24.6 #4 → item 2 (scale table): Named NPCs row replaced with 14-18 / 30-40 / 60-80; derivation note added after the table
- 24.2 #3 / 24.6 #4 → item 10.7: Sockets party×3 (party×2 in short); socket NPC drawn from the existing roster, never added on top
- 24.2 #4 / 24.6 #5 → item 13.2: Every detail (prep at end, mid-session, hand-called) runs through the birth machinery, play tab reads the finished file lazily, validator output redacted; tiered improvise exception for minor unlinked skeleton sites marked played-improvised and backfilled at end
- 24.2 #4 / 24.6 #5 → item 13.3: Heading line states every product is written by the birth machinery (agent → staging fragment → registry.py merge → single-entity check), never by the play tab
- 24.2 #4 / 24.6 #5 → item 19.1: 'does not arm it' replaced: guard arms for the duration of the detail run (mode: detail) and stays unarmed for the DM's reads
- 24.2 #4 / 24.6 #5 → item 19.3: In-play detail follows the staging protocol (_staging/detail/<id>.json, registry.py merge as the only path into the registry)
- 24.2 #5 → item 15.1 (factions row): 'doctrine for ≥3 triggers' → all six triggers, canonical list in factions.yaml
- 24.2 #6 → item 9.5: Role band declared the allowed range; XP formula picks inside it for intended-path sites; off-path sites roll inside the band
- 24.2 #6 → item 9.6: Room-count formula clamped to the role band; off-path room counts rolled, not computed
- 24.2 #6 → item 9.10: 'first 2-3 sites' → item 2's numbers 2 / 3 / 3-4 by scale
- 24.2 #7 → item 1: revise = canon change only; play-time fallback pick is the separate `arc fallback` command the DM may call
- 24.2 #7 → item 10.3: Play-time command named `arc fallback`, `arc revise` retired
- 24.2 #7 → item 21.C: Command row renamed `arc revise` → `arc fallback` with the canon-only note
- 24.2 #8 → item 2 (dial table): Danger row: touches only non-CR knobs (over-tier Act 1 site count/proximity, rest pressure, telegraph explicitness, rumour visibility, reference-party step-up for 1-2 PC tables), never a tier; Starting-level row: band = start .. start + span, span 4/11/19; note after scale table that Level range assumes start 1
- 24.2 #8 → item 17 #1 / #2: dials.yaml: danger maps only to non-CR knobs; scale.yaml: carries the level-band span 4/11/19
- 24.2 #9 → item 9.2: Sites carry a stamped `act` field that 13.4's later-act check keys to
- 24.2 #9 → item 13.4: Later-act validator check keyed to the site's own stamped act
- 24.2 #10 → item 19.2: P0/P3 skeleton reserves polity_ ids and npc_ stubs for rulers, anchor owners, village NPCs; per-phase validator accepts status: pending from a later phase; only P8's full run demands files
- 24.2 #11 → item 5 (pantheon): church field filled for every god at every scale; separate faction_ church entities per god only in epic
- 24.2 #11 → item 19.2 (P2): P2 note: separate church entities only in epic, the church field on every god
- 24.2 #12 → item 12.2: Crossing points skipped for a solo party
- 24.2 #12 → item 12.3: Imbalance and crossing checks skipped for a one-PC table
- 24.2 #12 → item 15.1 (threads row): Solo party: crossing and imbalance checks skipped
- 24.2 #12 → item 16.3(d): 'both PC thread files' → 'all PC thread files'
- 24.2 #13 → item 19.1: active-design.json gains mode: birth | detail | playtest, playtest carrying an allowlist of player-facing artifacts
- 24.2 #13 → item 22.5: Player agent runs under mode: playtest whose allowlist confines it despite being an agent-* transcript
- 24.2 #14 → item 3: Added place_ and pc_ entity types; npc gains a tier field (major/supporting/minor) that detail may raise
- 24.2 #14 → item 6.4: Each filled small point is a place_ entity
- 24.2 #14 → item 13.3: Settlement small points enter the registry as place_ entities; NPC promotion raises the registry tier field
- 24.2 #14 → item 12.2: The PC is a pc_ registry entity referenced by its thread and sockets
- 24.2 #15 → item 10.8: foreshadowing_check.py is rewritten from its description; no code exists in the archive
- 24.2 #16 → item 3: 'a rename touches only the registry' → touches the registry and regenerates the files the link scan lists
- 24.2 #16 → item 19.5: 'design_manifest.py update' → mark / tokens (no update verb, per 19.4)
- 24.2 #16 → item 7.7: News records carry refs[] (registry ids touched) so 13.1(c) can match a record to a site
- 24.6 #3 → item 7 §7: Appended the five-rule simulation charter bullet (load-bearing armour, doom fixed at birth, brake = park, party faction never auto-moved, deterministic engine + volatility budget)
- 24.6 #3 → item 10.5: Threat step resolves in the deterministic engine; doom day fixed at birth, moved only by a party-caused structured block; current stage is an overlay value
- 24.6 #6 → item 14.4: Added revise --dm-only --role bbeg | big-secret | pc-truth:<pc> (script-resolved) and the design ask yes/no proxy (evet / hayır / spoiler vermeden cevaplanamaz, logged)
- 24.6 #6 → item 15.2: wishes rubric over dm-only text with per-wish ✓ on the card; two independent critics for BBEG, lieutenant and premise-secret files
- 24.6 #6 → item 19.7: BBEG, lieutenant and premise-secret files at effort high with two independent critics
- 24.6 #6 → item 19.6: Premise card carries a spoiler-safe abstract (archetype class, novelty vs used.json, clue count per act, critic agreement) plus the wishes per-wish ✓
- 24.2 (closing line) → item 24.2: Appended: Folded into the item texts on 2026-09-24; markers '(errata 24.2 #n)' show where.

**Not applied by the editor:**
- 24.2 #2 (side effect, out of scope): Item 21.E still says `design_check.py (13 modules)`; with the new `overlay` row in 15.1 the count is 14. 21.E is not named by any erratum, so it was left untouched — flag for the owner's next pass.

## Checkers


### COVERAGE — every 24.2 erratum and 24.6 decision checked against its target items — verdict: needs-fixes

- **[missing / item 21.C, `load` row (line 478)]** Errata 24.2 #12 changed 16.3(d) to "all PC thread files are always read", but 21.C's `load` row — the consolidated SKILL-commands change list that mirrors 16.3 — still says "both PC threads", re-introducing the two-PC assumption the erratum removed.
  - *fix:* old_string: "the current chapter file; both PC threads; the last prep note" -> new_string: "the current chapter file; all PC thread files (errata 24.2 #12); the last prep note"
- **[new-contradiction / item 7 §7, "Two brakes" bullet (line 200) vs the appended simulation charter rule (3) (line 202)]** The new charter bullet (24.6 #3) says "**Brake = park**, never halt", but the pre-existing "Two brakes" bullet two lines above still says "the simulation stops and tells the DM" — the item now states both halt and park for the same brake.
  - *fix:* old_string: "when a move targets an asset that matters to the party (an allied NPC, the party's own holding) the simulation stops and tells the DM \"this belongs in a scene\" (the same threshold rule as the dead-time skip)" -> new_string: "when a move targets an asset that matters to the party (an allied NPC, the party's own holding) the move is parked as a `pending_scene` for the DM (\"this belongs in a scene\") and the simulation continues — charter rule 3 below (the same threshold rule as the dead-time skip)"
- **[missing / item 1 command list (lines 60-68); item 21.C `design …` row (line 477); item 21.E `designer.py` verb list (line 489)]** 24.6 #6(d) adds a new command, `design ask "<yes/no question>"` (folded into 14.4 and listed in 24.3 slice 3), but the command surface in item 1, the SKILL-commands row in 21.C and the conductor CLI verb list in 21.E were not updated, so the plan's declared command surface omits it.
  - *fix:* item 1: add after the `design revise` bullet -> "  - `/dm:dnd design ask \"<yes/no question>\"` — the blind proxy over dm-only content: a fresh agent answers only `evet / hayır / spoiler vermeden cevaplanamaz`, logged in `design.json` (item 14.4; 24.6 #6)."; 21.C: old_string "| `design status / phase / detail / check / integrate / primer / revise` | new section |" -> new_string "| `design status / phase / detail / check / integrate / primer / revise / ask` | new section (`ask` per 24.6 #6) |"; 21.E: old_string "preroll, status, phase, detail, revise, integrate, primer, abandon" -> new_string "preroll, status, phase, detail, revise, integrate, primer, ask, abandon"
- **[missing / item 21.A, SKILL.md rules table, row from item 13 (line 465)]** 24.6 #5 replaced the flat "improvising from a skeleton is forbidden" rule with a tiered one (minor unlinked skeleton site may run live, marked `played-improvised`, backfilled at `end`) and routed every `detail` through the agent pipeline; 13.2 carries this, but 21.A — the consolidated list of SKILL.md rule changes — still states the flat rule only.
  - *fix:* old_string: "| Improvising a designed site from its skeleton is forbidden; `detail` on approach; the prep step at `end` | 13 |" -> new_string: "| Improvising a designed site from its skeleton is forbidden, with one tiered exception (a minor, unlinked skeleton site may run live, marked `played-improvised`, backfilled by `detail` at `end`); `detail` on approach, always through the agent pipeline; the prep step at `end` (24.6 #5) | 13 |"
- **[nit / item 10.5 (line 247)]** 10.5 is a named target of errata 24.2 #2 ("1, 14.1 vs 3, 13, 16.1, 16.5, 10.5") and now correctly says "the current stage is an overlay value", but the marker cites only 24.6 #3, so the #2 trail does not lead to it.
  - *fix:* old_string: "and the current stage is an overlay value (24.6 #3)." -> new_string: "and the current stage is an overlay value (errata 24.2 #2; 24.6 #3)."
- **[nit / item 24 status line (line 521)]** The item-24 status line still reads "discussed — risk review complete, six owner questions pending", contradicting the master-list row ("decided (errata in 24.2 folded into the items)"), 24.6's "Owner decisions (2026-09-24)" and the new closing line of 24.2.
  - *fix:* old_string: "**Status (2026-09-24): discussed — risk review complete, six owner questions pending.**" -> new_string: "**Status (2026-09-24): decided — risk review complete, the six owner questions answered in 24.6, the 24.2 errata folded into items 1-23.**"

### FIDELITY — verdict: needs-fixes

- **[new-contradiction / item 7.5 (docs/campaign-designer-plan.md line 191)]** The original sentence 'Each antagonist is an `npc_` with a faction, a goal-tracker record (...) and a front' was kept verbatim, and the new sentence 'regional villains are supporting tier — a full dossier, no goal-tracker record' was appended after it. Regional villains are antagonists, so 7.5 now says in one breath that every antagonist has a goals.py record and that regional villains have none. Erratum 24.2 #3 / 24.6 #4 resolves this in favour of 'no record'; the first sentence should have been narrowed.
  - *fix:* old_string: "Each antagonist is an `npc_` with a faction, a goal-tracker record (`goals.py add` with threatened / blocked / permanent-loss pre-written) and a **front**: 4-6 grim portents"  ->  new_string: "Each antagonist is an `npc_` with a faction and a **front** (the BBEG and lieutenants additionally a goal-tracker record, `goals.py add` with threatened / blocked / permanent-loss pre-written): 4-6 grim portents"
- **[changed-decision / item 8.2 (line 214) and item 7.5 (line 191)]** Erratum 24.2 #3 and decision 24.6 #4 say only that regional villains drop to supporting tier; they do not say the major tier consists of antagonists alone. 8.2's new clause 'the major tier holding only the BBEG and the lieutenants' turns that into a global rule, excluding e.g. a faction leader or ruler from major tier. The plan's own risk row (24.1, 'per-antagonist trackers fill 67-100% of the major tier') treats the major tier as also holding non-antagonists, which is exactly why the caps were re-derived. 7.5's 'Only the BBEG and the lieutenants are major tier' reads as scoped to the antagonist hierarchy but should say so explicitly.
  - *fix:* 8.2 old_string: "the major tier holding only the BBEG and the lieutenants (regional villains are supporting tier, dossier without tracker)"  ->  new_string: "with, of the antagonists, only the BBEG and the lieutenants in the major tier (regional villains are supporting tier, dossier without tracker)".  7.5 old_string: "Only the BBEG and the lieutenants are major tier with a `goals.py` record"  ->  new_string: "Of the antagonists, only the BBEG and the lieutenants are major tier with a `goals.py` record"
- **[new-contradiction / item 7, 'Two brakes' bullet (line 200) vs the new 'Simulation charter' bullet (line 202)]** The inserted charter bullet (24.6 #3, rule 3) states 'Brake = park, never halt: a move that touches a party asset becomes a pending_scene'. Two lines above, the untouched 'Two brakes' bullet still says 'the simulation stops and tells the DM'. 24.6 #3 was decided precisely to replace halt with park, so item 7 now carries both behaviours.
  - *fix:* old_string: "the simulation stops and tells the DM \"this belongs in a scene\""  ->  new_string: "the simulation parks the move as a `pending_scene` and tells the DM \"this belongs in a scene\" (24.6 #3)"
- **[nit / item 3, registry field list (line 124)]** `status` is now declared an overlay field 'not a registry field' with a closed writer list (simulate, site_progress.py, campaign_graph.py, factions.py, registry.py play-set). But the skeleton -> detailed transition of `status` is written at `detail` time by `registry.py merge` (13.3, 19.3), which is not on that list; only the `played` value is play-time. The enumeration follows 24.1's overlay row, so this is inherited rather than invented, but item 3 is where the reader will trip over it.
  - *fix:* old_string: "Of these, `status`, `seen_in_play`, an npc's current `location`"  ->  new_string: "Of these, `status` (its play-time `played` value — skeleton → detailed is written by `registry.py merge` at `detail`), `seen_in_play`, an npc's current `location`"
- **[nit / item 19.1 (line 418)]** The kept phrase 'never reads ... raw `entities.json`' now sits immediately before the new sentence 'The conductor reads only the generated projection `design/entities.json`'. Since `design/entities.json` is now the projection, 'raw `entities.json`' no longer names a distinct file; the forbidden file is the canonical one in dm-only.
  - *fix:* old_string: "`design/_staging/**` or raw `entities.json`, and holds only"  ->  new_string: "`design/_staging/**` or the canonical `design/dm-only/entities.json`, and holds only"

## Fixer

- item 21.C, `load` row: "both PC threads" -> "all PC thread files (errata 24.2 #12)", aligning the SKILL-commands change list with the erratum applied to 16.3(d).
- item 7, "Two brakes" bullet (issues 2 and 7, same sentence): Replaced "the simulation stops and tells the DM ..." with the park behaviour: the move is parked as a `pending_scene` for the DM ("this belongs in a scene") and the simulation continues, cross-referenced to charter rule 3 with a (24.6 #3) marker; the same-threshold-as-dead-time-skip clause kept. Applied once as a merged fix since both issues targeted the identical string.
- item 1 command list: Added the `/dm:dnd design ask "<yes/no question>"` bullet after `design revise` (blind proxy over dm-only content, fixed evet/hayır/cannot-answer replies, logged in design.json; item 14.4; 24.6 #6).
- item 21.C, `design ...` row: Command list now ends "... / revise / ask" with the note "(`ask` per 24.6 #6)".
- item 21.E, `designer.py` verb list: Conductor CLI verbs now include `ask` (inserted before `abandon`).
- item 21.A, SKILL.md rules table, row from item 13: Flat improvise-forbidden rule replaced with the tiered version: one exception for a minor, unlinked skeleton site run live, marked `played-improvised`, backfilled by `detail` at `end`; `detail` on approach always through the agent pipeline; marked (24.6 #5).
- item 7.5, first antagonist sentence: Narrowed so every antagonist has a faction and a front, while only the BBEG and lieutenants additionally get a goals.py record — removes the contradiction with the appended 'regional villains have no tracker' sentence.
- item 8.2, major-tier clause: "the major tier holding only the BBEG and the lieutenants" -> "with, of the antagonists, only the BBEG and the lieutenants in the major tier", so the clause scopes to the antagonist hierarchy and no longer excludes non-antagonists (e.g. rulers, faction leaders) from major tier, consistent with 24.6 #4 and the 24.1 risk row.
- item 7.5, 'Only the BBEG and the lieutenants are major tier' sentence: Prefixed with "Of the antagonists," to make the antagonist-hierarchy scope explicit.
