# D&D Skill — The Campaign Designer

*Plan `docs/campaign-designer-plan.md` (items 1-24); this file is the procedure the DM follows for `/dm:dnd new` and the `design` command family. Load it when `new` or any `design` command is invoked; it is not read at `load`. Script syntax is in `SKILL-scripts.md`; the prompts the agents receive are under `prompts/design/`; the tables that decide what can exist are under `data/design/`.*

## What the designer is

`/dm:dnd new` builds a whole campaign bible before session 1 — premise, cosmos, lands, powers, people, sites, arc, primer — and reveals it progressively in play. The bible is **data-first**: the canonical registry `design/dm-only/entities.json` says what exists, the public projection `design/entities.json` is what the DM and the scripts see, prose files under `design/` reference entities with `[[id]]` links, and play-time truth lives in `design/overlay.json`. Stamped fields are immutable; everything else may deepen through `detail`.

Three rules shape every command here:

1. **The blind conductor.** The main session (you, at the table or at birth) never writes bible prose and never reads `design/dm-only/**`, `design/_staging/**` or the canonical registry. Fresh-context agents write files and return ids, statuses, counts and paths — never prose. `designer.py` arms `hooks/design_read_guard.py` for the run; while armed, a Read, Grep or Bash that touches those paths is refused. Unarmed, your own reads of a finished public file are free.
2. **The owner is a player.** The person running this table is also its sole player. Their free-reading surface is the primer, the player map, the approval cards and each PC thread's public face (`design/player/`). Everything else under `design/` outside `dm-only/` is DM-open, player-avoid; `dm-only/` they never open. Approval cards therefore show only the public projection, and the secret layer appears on them only as a spoiler-safe abstract.
3. **The world does not scale.** Danger tiers are the fiction's, set at birth and stamped; nothing derives from the party's level. The designer owes the party legibility (three telegraphs per site) and a way out (escape geometry), never softening. Bosses are sized against a reference party at the tier's intended level.

## Phase 0 — the dials

`new` is the designer's only questioning moment. Ask the dials in one message and accept `?` for any the player wants rolled:

| Dial | Values |
|---|---|
| scale | short / standard / epic |
| tone | grimdark / dark fantasy / heroic / horror / political / swashbuckling / cosmic |
| magic | none / low / medium / high |
| era | medieval / renaissance / ancient / nautical / underground |
| danger | lethal / gritty / standard / heroic (touches only non-CR knobs) |
| party size, starting level | 1-6; default 1 |
| content mix | the top three of exploration / politics / war / horror / mystery, in order |
| wishes | 1-3 must, 1-3 must-not, free text; hard constraints the wishes critic checks in every phase, secrets included |
| narration language | tr (default) / en |

Then run `designer.py new <name> --scale … --party-size N --content-mix a,b,c [--must … --must-not …] [--seed S]`. Blank dials are rolled in front of the player and logged; the manifest, the arc skeleton (chapter ids, acts, level bands from `scale.yaml`) and the Phase 0 card follow; the guard arms for `birth`. A real campaign waits for `onay` on the P0 card; a `--fixture` or `_test-*` campaign auto-approves every card (owner decision 2026-09-25) unless `new` was given `--ask-approval`; a test campaign is git-ignored and never committed.

## The phase loop

Phases P1-P9 in order, each the same loop. `designer.py` does the deterministic half; a Workflow runs the agents; you never fill a gap by hand.

```
designer.py -c CAMP preroll --phase PN            every labelled roll of the phase, from the tables
designer.py -c CAMP phase PN begin --json         reconcile, arm, the roster with read budgets and prompts
   → Workflow {name: "design-skeleton", args: <that JSON>}      when the JSON says workflow: design-skeleton
designer.py -c CAMP phase PN merge                absorb skeleton.json, merge fragments, seed the stores
designer.py -c CAMP phase PN begin --json         now the pending entities with their prompts
   → Workflow {name: "design-fanout", args: <that JSON>}        write → critique → fix (≤2) → second critic; phase + wishes critics
designer.py -c CAMP phase PN merge                record the critics' returns, merge, seed
designer.py -c CAMP phase PN check                the validator for this phase, redacted
designer.py -c CAMP phase PN card                 the Turkish phase card (design_approval.py)
   → show the card; wait for `onay` (or a one-sentence correction)
designer.py -c CAMP phase PN approve --onay       records the approval, commits path-scoped
   → wait for `devam` before the next phase's preroll
```

| Phase | Writes | Shape |
|---|---|---|
| P1 premise | `design/premise.md` + `dm-only/premise-secret.md`, `naming.json`, the `premise_` / `signature_` / `break_` rows | single writer, two critics on the secret |
| P2 cosmos | `design/cosmology.md` (+ mirror): gods, planes, magic, history, calendar; `calendar.py init` seeded | single writer |
| P3 lands | polities, regions with travel tables, settlements with anchors, villages in fives, `map.json` | skeleton → fan-out |
| P4 powers | factions (four-phase dossiers), the stance matrix, the antagonist hierarchy on a hard calendar, `factions.json` and `goals.json` seeded, the consequence calculus | skeleton → fan-out |
| P5 people | the roster: major and supporting dossiers, minors in sixes, the relationship web into `graph.json`, standing channels | skeleton → fan-out, two critics on the BBEG and lieutenants |
| P6 sites | the site directory with stamps, the first 2 / 3 / 3-4 intended-path sites detailed with the boss checklist | skeleton → fan-out |
| P7 arc | beats, chapters with nodes, quest seeds in sixes, planted hooks, sockets, endings, the doom day | skeleton → fan-out |
| P8 primer | one primer section per culture, then `render_player.py primer / facts / news`, the generated `world.md`, `npcs.md`, `index.md`, a lean `state.md`, `report.md`; the full validator; final approval = the report's public part + the primer | fan-out (document roster) |
| P9 integrate | after every `character new`: one thread per PC, the session-1 pack, `goals.py` pc records; `render_player.py thread-face` | fan-out (document roster), outside birth |

**Corrections.** A correction is one sentence. Classify it and run `design_revise.py -c CAMP round --phase PN --scope direction|fact|entity|phase --text "…"` (with `--entity`, `--field --value`, `--action remove|replace`, `--world`, `--reseed` as the scope needs); it records the round, marks the affected entities for a rerun and lists them. Rerun ≤3 entities with the Agent tool (each agent runs the render command `begin --json` printed for it) or the fan-out Workflow for more; then merge, check, a new card with its diff. Three rounds per phase, then approve as-is or `--scope phase`. A one-word correction gets one clarifying question first.

**Failures.** A null agent return retries once with the attempt in the prompt, then the entity is `failed`; a phase with failed ids is shown but cannot be approved (rerun the pending list, or drop the entity with an entity round). A missing critique is shown on the card as a count. Validator errors go to targeted fix agents inside the two loops, then to the player as "did not pass, because…" with the rubric ids.

**After every Workflow return**, before any text to the player: `designer.py phase PN merge` and `designer.py commit --message …` (compaction safety, item 19.5). `design.json` is the index; disk is the truth; `reconcile` runs inside `begin` and `merge`.

## Model routing and cost

Generation and critique inherit the session model; start `new` in an Opus-tier session (the conductor warns otherwise). Each prompt's front matter sets its effort (`high` for the premise, skeletons, sites and threads; `medium` for dossiers and fixes) and how many critics read it (two on the premise secret, the BBEG and the lieutenants: different rubric order, no shared notes). `--economy` (item 19.7) routes fan-out dossiers and their critique to the Sonnet tier. A `short` birth is roughly 70 agent calls and one to two machine hours; `standard` about 120 and two hours; `epic` about 190 and three. Approval waits dominate elapsed time.

## `design` commands

- **`design status`** — `designer.py status`: phases and their states, the guard, the roll counts; in play also the "detail needed" list (item 13.1) and the sites prepped at the last `end`.
- **`design phase <n> [--reseed]`** — `designer.py phase PN rerun --reason … [--reseed]`, then the loop above from `preroll`; later phases are stale until rerun.
- **`design detail <id>`** — JIT elaboration through the birth machinery (24.6 #5): `designer.py arm --mode detail`, `design_prompts.py render detail.<kind> --id ID` as the one entity of a `design-fanout` run (or the Agent tool), `registry.py merge --phase detail`, `design_check.py --only ID`, disarm. Triggered by the DM on approach (the party within a day or in the same settlement, a stated destination, a rumour pointing there), by the prep step at `end` (predict 1-3 sites, detail them, validate), or by hand; never once the party is inside. Improvising a designed site from its skeleton is forbidden, with the one tiered exception of a minor, unlinked skeleton (band 5-10, lore or treasure payoff, tier at or below the band, no clue / beat / thread / hook reference) run live and marked `played-improvised`, backfilled at `end`.
- **`design check`** — `design_check.py -c CAMP` (all modules) or `--fast` at every `save`; output is redacted in every mode.
- **`design integrate`** — P9 after all PCs exist: `preroll --phase P9`, `phase P9 begin --json`, the fan-out, merge, check, card, approve; then `render_player.py thread-face` per thread.
- **`design primer`** — `render_player.py primer` (and `facts`, `news` when P8's fragments changed).
- **`design revise "<change>"`** — player-only, a change of canon. During birth it is the correction round above. After session 1 (slice 3): unseen entities revise freely; a seen entity is revised only with an in-fiction explanation or refused; `--dm-only --role bbeg | big-secret | pc-truth:<pc>` regenerates secret content without showing it.
- **`design ask "<yes/no question>"`** — one fresh agent with the `ask` prompt (`design_prompts.py render ask --question "…"`) reading the dm-only projection, returning exactly `evet` / `hayır` / `spoiler vermeden cevaplanamaz`; logged with `design_manifest.py ask`.
- **`design abandon`** — `designer.py abandon --reason …`: names retired from the registry, the campaign's `used.json` rows dropped, the guard disarmed.
- **`arc fallback`** (play, the DM's call) — when a beat is pre-empted, pick one of its three designed fallbacks (cost / secondary / deferred) and log it in state.md's arc pointer; the bible is never rewritten for it.

## Phase → SRD map

Candidate lists come from `data/design/srd-index-2014.json`, filtered script-side before an agent chooses and reskins (item 18.2): P2 ← the eight cleric domains, the planes appendix, the spells by class and level; P3 ← equipment prices and trade goods; P4 ← the NPC appendix as typical forces; P5 ← the NPC appendix and monsters as stat anchors; P6 ← monsters through `monster-ecology.yaml` by habitat and tier, magic items by rarity through `loot-budget.yaml`, hazards by tier through `sites.yaml`; P8 ← backgrounds and languages for the primer; P9 ← class features for personal tracks. The gods appendix is never read (errata 24.2 #19). SRD monsters only at birth; variety comes from reskins and the signature creature; a reskin that moves HP, AC or damage more than 25% shifts CR one band.

## The critique pass

`data/design/rubrics.yaml` is the bar every campaign meets: one row per question the plan records under items 4-12, run by the same model in a separate call without the generation context, returning `pass` / `fix` / `rerun` with findings by rubric id. Two fix loops per entity; a third failure reaches the player. The special rubrics (wishes, leak, distinctness, cliché, naming, load lightness) run across phases. `design_approval.py critique` records every return as ids and codes only.

## Names and language

The narration is Turkish; the world is not. Every proper noun the designer produces — persons, places, institutions, gods, ships, signature phenomena and creatures, months — is an English-language fantasy name from the campaign's naming languages (`naming.json`, rolled from `naming.yaml`'s sound families and root lexicon), carried into Turkish prose with an apostrophe suffix (Lanternside'a, Saltmere'de). Common nouns stay Turkish. `naming.yaml`'s blacklist (brands, the owner's banned names, the model's favourites, real-world mythology) and `.name_registry.json` are checked at every phase approval; no stem is ever banned, only whole names.
