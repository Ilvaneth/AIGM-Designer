# `prompts/design/` — the designer's agent prompts

Plan item 19.1-19.3, 15.2, 21.E; slice 1c item 2. One prompt per agent role and entity kind; `scripts/design_prompts.py` renders them for a campaign and `designer.py phase PN begin --json` hands the rendered text to the phase's Workflow, which passes it to fresh-context agents.

## Roles

| Role | Files | Returns |
|---|---|---|
| `skeleton` | `P3.skeleton`, `P4.skeleton`, `P5.skeleton`, `P6.skeleton`, `P7.skeleton` | `schemas/skeleton.json`: the roster of ids it reserved, the label → id assignments, its fragments |
| `writer` | `P1.premise`, `P2.cosmos`, `P3.region`, `P3.settlement`, `P3.villages`, `P4.faction`, `P4.calculus`, `P5.npc`, `P5.minors`, `P6.site`, `P7.chapter`, `P7.seeds`, `P8.primer`, `P9.thread`, `P9.session1`, `detail.*` | `schemas/writer.json`: entity id, `staged` or `failed`, the fragment path, counts |
| `critic` | `critic` (entity scope, rubric rows of the phase; `--critic-order 2` for the second critic) | `schemas/critic.json`: verdict `pass` / `fix` / `rerun` with findings by rubric id |
| `phase_critic` | `phase_critic` (cross-entity rubrics on the skeleton plus one-line identities) | `schemas/critic.json` |
| `ask` | `ask` (the blind proxy of `design ask`) | `schemas/ask.json`: one of `evet` / `hayır` / `spoiler vermeden cevaplanamaz` |

## Front matter

```
---
phase: P6            # P1-P9, or `detail`, `ask`
role: writer         # skeleton | writer | critic | phase_critic | ask
kind: site           # the entity type, or a document kind (premise, cosmology, calculus, primer, session1)
effort: high         # high | medium (item 19.7)
critics: 2           # how many independent critics the file gets (24.6 #6)
schema: writer       # schemas/<name>.json
detailed: true       # sites only: the detailed template instead of the skeleton
rubric_scope: entity # critics only: which rubric rows to embed
---
```

## Placeholders

`{{campaign}}`, `{{campaign_dir}}`, `{{skill_dir}}`, `{{phase}}`, `{{attempt}}`, `{{lang}}`, `{{dials}}`, `{{scale}}`, `{{scale_line}}`, `{{seed}}`, `{{party_size}}`, `{{level_band}}`, `{{content_mix}}`, `{{entity_id}}`, `{{entity_type}}`, `{{entity_name}}`, `{{entity_summary}}`, `{{files}}` (the two-hop read budget), `{{rolls}}` (this entity's public rolls through the skeleton's assignments), `{{phase_rolls}}` (every public roll of the phase), `{{directions}}`, `{{wishes}}`, `{{template}}`, `{{prose_path}}`, `{{mirror_path}}`, `{{fragment_path}}`, `{{notes_path}}`, `{{rubrics}}`, `{{common}}` (the `_common.md` preamble), `{{schema}}`, `{{agent_label}}`, `{{roster}}`, `{{critic_order}}`.

The renderer reads the manifest and the **public projection** only; secret names never enter a prompt through it. A writer that needs a secret roll reads `design/dm-only/dice-log.json` itself, as its prompt says.

## Rules the prompts enforce

- Prose first, fragment last; no free text outside the registry fields; notes go to the `.notes.md` file.
- Every proper noun is an English fantasy name from `design/naming.json`; prose is in the narration language (errata 24.2 #17); the blacklist and the no-mythology rule apply (#18, #19).
- The three headings; the `## Secret` section only in the dm-only mirror.
- The tables' `hooks` are obligations: a writer reads the rows its rolls name and does what their `must` lines say.
- Agents never roll dice; the rolls are in the prompt or in the dm-only dice log.
