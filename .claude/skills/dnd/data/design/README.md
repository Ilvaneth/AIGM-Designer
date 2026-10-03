# `data/design/` — the designer's tables

Plan item 17. These tables are the Campaign Designer's creative DNA: the scripts orchestrate, the tables decide what can be rolled and how a rolled row must propagate. They are skill data, so they are English; generated content is in the narration language, and every proper noun the tables seed is an English-language fantasy name (errata 24.2 #17).

## Convention

Every file is a YAML mapping with a header and one or more row lists:

```yaml
schema_version: 1
table: tensions            # the file's stem
consumed_by: [P1]          # phases that read it (P0-P9, validator, play)
plan: "item 4.1, 17 #3"    # where the plan decides it
roll: {...}                # how design_dice.py draws from it, when it is rolled
rows: [...]                # a single-table file
tables:                    # or several sub-tables, addressed as file.yaml#name
  tone:
    rows: [...]
```

Every row carries:

- `id` — unique across **all** tables (`design.json.dice_log` and `used.json` record it), `[a-z0-9_]`, prefixed by its kind (`tone_`, `tension_`, `secret_`, `break_`, `sig_`, `family_`).
- `label` — the short English name shown on cards and in the dice log.
- `hooks` — a list of `{phase, must}` saying how the row must propagate into later phases; the phase critics and `design_check.py` read them. Table-level `hooks_common` apply to every row of that table.
- `weight` — optional, default 1; `design_dice.py` rolls weighted.

`design_tables.py` is the one reader (`rows("dials.yaml#tone")`); `design_dice.py roll --table` draws through it and `--avoid-used` skips rows `used.json` already lists for another campaign. `used.json` (item 17 #26) is not a table: it lives per user at the data root, written only at phase approval, with the birth order (`births`) the waits count in.

## The arbiter's fields (plan item 25: the script is the only arbiter of conflicts)

A row may also carry:

- `conflicts_with` — row ids, from any table, it may never appear with. `design_tables.conflict_index()` makes them symmetric: A listing B also bars B after A.
- `requires` — a condition that must hold before the row may be drawn: a mapping whose keys all hold (`dial: {magic: [medium, high]}`, `any_of`, `all_of`, `none_of` over rolled row ids), or a list of such mappings of which one must hold. A table's "needs" or "only" is a requirement.
- `weight_by` — `[{when: <condition>, x: factor}]`: the weight is multiplied while the condition holds. A table's "heavier in" is a weight, never a requirement.
- `forbidden: true` with an optional `allowed_via` — the row never enters a pool unless a rolled row in `allowed_via` admits it; the validator's closed lists still name it.
- `family` — the row's family, read by a table's `family_wait`.

A `roll` header (the file's, overlaid by a sub-table's own `roll`) may set `avoid_used` (a row another campaign drew waits while the table has rows), `family_wait: N` (a family the last N births drew waits; only the foundation's spine, ruin source, lifeline and contest), `row_wait: N` (a row the last N births drew waits; the break's actions and scars) and `secret: true` (the rows are dm-only; a public log never names them).

`design_arbiter.py` filters every draw before the die: constraints first (the caller's exclusions, forbidden, requires, conflicts with any row rolled before, zero weight) — a pool they empty stops the preroll as a table fault; then usage (used elsewhere, the waits, a caller's spent pairs) — a pool usage empties falls back one kind at a time: family waits, then used elsewhere, then row waits, the pair last; the record names what was dropped. A table whose own header states `avoid_used` is held to it; the caller's argument is read only when the header is silent. `families_distinct: true` makes several rows drawn from the table for one roll take different families (a constraint, never relaxed). Every exclusion is logged on the record with its reason; a public record counts its die over the rows not publicly excluded, so its size never tells what the secret layer took out.

## The tables (item 17)

| Batch | Files | Read by |
|---|---|---|
| A premise | `dials`, `scale`, `tensions`, `secrets`, `trope-breaks`, `forbidden`, `signatures`, `naming` | P0, P1 |
| B cosmos | `pantheon`, `planes`, `magic`, `history`, `calendar` | P2 |
| C lands | `regions`, `settlements` | P3 |
| D powers | `factions`, `antagonists`, `simulation` | P4, the slice-2 engine |
| E people and sites | `npcs`, `monster-ecology` (generated + curated), `loot-budget`, `sites`; `srd-index-2014.json` (generated) | P5, P6 |
| F arc | `arc`, `threads`, `rubrics` | P7, P9, every critic |

`tests/test_design_tables.py` enforces the convention, the plan's numbers in `scale.yaml`, the size floors of risk 24.1 #18 and the closed lists `design_manifest.py` validates dials against.
