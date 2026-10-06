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

Campaign **{{campaign}}** at `{{campaign_dir}}`. Phase {{phase}}, attempt {{attempt}}. {{phase_reads}}

Roster of the phase: {{roster}}

### The rubric
{{rubrics}}

{{prior_campaigns}}

The registry door already refused the structural leaks and naming faults (a mirror sentence in a public file or the public notes, a secret name outside dm-only, blacklisted or duplicate names); `rubric_leak` here is about what a door cannot see — a secret *hinted* in public wording, a truth restated in other words.

Answer each row across the whole phase (are these regions distinct only by name; do two NPCs share a voice; is any entity a reskin of another). {{verdict_options}} {{verdict_overall}} Each finding names the rubric whose question the text fails; a fault no rubric of yours asks about is a `note`, never a `fix` (a `fix` on a rubric you were not given is refused at the record). `findings[]` name the entity ids concerned with a `reason_code` slug (every finding that is not a pass has one; it never names a secret row or a secret name); the reasoning goes to `design/_staging/{{phase}}/phase.critique.md`. No quoted text in the return.

Return, as `{{agent_label}}`:
```json
{{schema}}
```
