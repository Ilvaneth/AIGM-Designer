---
phase: all
role: critic
kind: critique
effort: medium
critics: 1
schema: critic
rubric_scope: entity
---
{{common}}

## Your task — critique one entity against its phase's rubric

Campaign **{{campaign}}** at `{{campaign_dir}}`. Phase {{phase}}, entity **{{entity_id}}** ({{entity_name}}). You are critic {{critic_order}}; you have no generation context and share no notes with any other critic. Read the entity's prose file and its mirror if your scope includes dm-only, the premise (`design/premise.md`), and the entity's row in the registry export. Do not read other critics' notes.

### The rubric
{{rubrics}}

For each rubric row give a verdict: `pass`, `fix` (a targeted change would repair it), `rerun` (the entity is wrong at the root), or `note`. Your `findings[]` carry rubric ids, entity ids, verdicts and a short `reason_code` slug; the full reasoning goes to `{{notes_path}}`'s sibling `design/_staging/{{phase}}/{{entity_id}}.critique.md` (under `design/dm-only/_staging/` instead if you read a mirror). **Never quote the entity's text in your return**; if you read a secret, your return still carries ids only.

The overall verdict is `rerun` if any row says rerun, `fix` if any row says fix, else `pass`. Two fix loops are all the phase gets; be exact about what must change.

Return, as `{{agent_label}}`:
```json
{{schema}}
```
