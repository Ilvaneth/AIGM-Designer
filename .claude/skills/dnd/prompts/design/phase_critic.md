---
phase: all
role: phase_critic
kind: critique
effort: high
critics: 1
schema: critic
rubric_scope: phase
---
{{common}}

## Your task — the phase-level critique

Campaign **{{campaign}}** at `{{campaign_dir}}`. Phase {{phase}}, attempt {{attempt}}. Cross-entity rubrics cannot be answered per entity: you read the phase's skeleton (`design/_staging/{{phase}}/skeleton.json` and the phase's fragments), the premise, and each entity's one-line identity / telegraph / voice lines from the registry export (`registry.py export --public`), not the full files, unless a rubric below says entity or dm-only.

Roster of the phase: {{roster}}

### The rubric
{{rubrics}}

Answer each row across the whole phase (are these regions distinct only by name; do two NPCs share a voice; is any entity a reskin of another; is the cliché's one saving detail present). `findings[]` name the entity ids concerned with a `reason_code`; the reasoning goes to `design/_staging/{{phase}}/phase.critique.md`. No quoted text in the return.

Return, as `{{agent_label}}`:
```json
{{schema}}
```
