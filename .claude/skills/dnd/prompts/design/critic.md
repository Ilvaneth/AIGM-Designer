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

Campaign **{{campaign}}** at `{{campaign_dir}}`. Phase {{phase}}, entity **{{entity_id}}** ({{entity_name}}). You are critic {{critic_order}}; you have no generation context and share no notes with any other critic. Read the entity's prose file and its mirror if your scope includes dm-only, the premise (`design/premise.md`), and the entity's row in the registry export.{{critic_reads}} Do not read other critics' notes.

### The rubric
{{rubrics}}

{{prior_campaigns}}

The registry door already refused, before you, the structural faults: a mirror sentence repeated in the public file or in the public notes, a secret name or a `## Secret` heading outside dm-only, a name on the blacklist or shared with another entity, a stub without `status: pending`. What reached you passed that door; judge meaning and craft, and do not re-report those classes.

{{verdict_options}} Your `findings[]` carry rubric ids, entity ids, verdicts and a short `reason_code` slug; the full reasoning goes to `{{critique_path}}` (the dm-only path whenever the entity has a secret layer: reasoning about a mirror is secret text). **Never quote the entity's text in your return**; if you read a secret, your return still carries ids only.

{{verdict_overall}} Two fix loops are all the phase gets; be exact about what must change. Save your return as `design/_staging/{{staging_phase}}/{{entity_id}}.critic{{critic_order}}{{critic_loop}}.json` before returning it: `designer.py phase merge` records it from there.

Return, as `{{agent_label}}`:
```json
{{schema}}
```
