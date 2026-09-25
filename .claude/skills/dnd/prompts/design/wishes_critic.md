---
phase: all
role: critic
kind: critique
effort: medium
critics: 1
schema: critic
rubric_scope: dm-only
---
{{common}}

## Your task — the wishes rubric over this phase, public and dm-only text alike

Campaign **{{campaign}}** at `{{campaign_dir}}`. Phase {{phase}}, attempt {{attempt}}. The owner is also the player and cannot read the secret layer, so you check their wishes on their behalf (plan 24.6 #6). Read the phase's fragments under `design/_staging/{{phase}}/`, the prose files they name, and the dm-only mirrors.

The wishes: {{wishes}}

For each `must` (numbered in order: `wish:must:1`, `wish:must:2`, …) decide whether this phase's output honours it where the phase can; for each `must_not` (`wish:must_not:1`, …) decide whether it appears anywhere, including in secrets. A `must` the phase cannot yet touch is a `note`, not a fail.

Return one finding per wish with `rubric_id` = `rubric_wishes`, `entity_id` = the wish slot, `verdict` = `pass` / `fix` / `note`, and a `reason_code` slug when it is not a pass; the overall verdict is `fix` if any wish fails, else `pass`. Your reasoning goes to `design/dm-only/_staging/{{phase}}/wishes.critique.md`. **Never quote secret text in your return.**

Return, as `{{agent_label}}`:
```json
{{schema}}
```
