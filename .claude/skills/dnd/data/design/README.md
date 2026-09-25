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

`design_tables.py` is the one reader (`rows("dials.yaml#tone")`); `design_dice.py roll --table` draws through it and `--avoid-used` skips rows `used.json` already lists for another campaign. `used.json` (item 17 #26) is not a table: it lives per user at the data root, written only at phase approval.

`tests/test_design_tables.py` enforces the convention, the plan's numbers in `scale.yaml`, the size floors of risk 24.1 #18 and the closed lists `design_manifest.py` validates dials against.
