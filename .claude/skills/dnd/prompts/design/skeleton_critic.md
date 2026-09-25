---
phase: all
role: critic
kind: critique
effort: high
critics: 1
schema: critic
rubric_scope: phase
---
{{common}}

## Your task — critique a phase skeleton before the fan-out reads it

Campaign **{{campaign}}** at `{{campaign_dir}}`. Phase {{phase}}, attempt {{attempt}}. You are critic {{critic_order}} of the skeleton; you have no generation context and share no notes. Read `design/_staging/{{phase}}/skeleton.json`, every stub fragment beside it, the skeleton's notes file, `design/entities.json`, and the phase's rolls in `design/design.json` (`dice_log`, phase {{phase}}). Read the dm-only skeleton files only if the phase has them (P4's antagonists, P5's secret web).

Roster of the phase: {{roster}}

### What a skeleton must get right (tuning birth 1)
- **Every count roll is honoured**: a `<thing>_count` line with `value` N means exactly N of that thing, every ordinal roll (`region.3.*`, `settlement.4.*`, `npc.11.*`) is assigned to an id in `assignments`, none is left unused, none is invented.
- **Every fan-out entity is on the roster** with a stub fragment: factions in P4, major and supporting NPCs in P5, sites in P6, chapters in P7; batches (`villagebatch_`, `npcbatch_`, `seedbatch_`) name their members.
- **Stubs carry their stamps** (`tier`, `polity`, `faction`, `danger_tier`, `act` …) and `status: pending` with `owner_phase`; ids are `<type>_<slug>` and the secret ones are opaque (`npc_s01`-style).
- **No secret name is public**: a secret entity's `name` and `aliases` are words that appear nowhere in the public files or the public registry; a hidden identity is a `dm_only` relation, never an alias.
- **Naming**: English fantasy names from the campaign's naming languages, no blacklist hit, no first-name collision across the roster; every id is the slug of the entity's **own** name (a faction called the Tidewell Company is `faction_tidewell_company`, not `faction_margin_house`).
- **The map and the matrices are consistent** (P3: one hub per region, edges with days; P4: every pair has a stance and one reason line; P5: every NPC has ≥2 edges).

### The rubric
{{rubrics}}

Give a verdict per rubric row and per bullet above: `pass`, `fix` (the skeleton agent can repair it in one loop), `rerun`, or `note`. `findings[]` carry rubric ids (use `rubric_skeleton_<bullet>` for the bullets: `counts`, `roster`, `stubs`, `secret_names`, `naming`, `structure`), the entity ids concerned, verdicts and a `reason_code` slug; the reasoning goes to `design/_staging/{{phase}}/skeleton.critique.md` (under `design/dm-only/_staging/{{phase}}/` if you read a secret file). **Never quote names or text in your return.**

The overall verdict is `rerun` if any row says rerun, `fix` if any says fix, else `pass`. Save your return as `design/_staging/{{phase}}/skeleton.critic{{critic_order}}.json` before returning it.

Return, as `{{agent_label}}`:
```json
{{schema}}
```
