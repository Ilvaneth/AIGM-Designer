---
phase: detail
role: writer
kind: npc
effort: medium
critics: 1
schema: writer
---
{{common}}

## Your task — promote a minor NPC to a full dossier during play

Campaign **{{campaign}}** at `{{campaign_dir}}`. Entity **{{entity_id}}** ({{entity_name}}: {{entity_summary}}). Directions from the DM (why the player latched on, what has happened between them):
{{directions}}

Read exactly these files:
{{files}}

The player latched onto a minor NPC; SKILL.md's Standard 5 promotes them (item 13.3). Write the full dossier from `templates/design/npc.md` exactly as the P5 NPC writer does: appearance, role, faction, demeanor, speech quirk kept from the three lines already written (the tic is a stamped habit in play), two or three voice samples consistent with every line the NPC has already said in the session log, schedule, offer and want, attitude as it currently stands, the four axes, ≥2 relationships, Known Facts from the witness lists and from what the NPC has seen in play (the session log, the news feed), the discoverable layer (motivation with history, weakness, what changes if they die), and the secret layer in the mirror if the registry stub carries a secret kind.

Raise `tier` to `supporting` (or `major` with a goals record if the directions say so): that is the one registry field `detail` may raise (errata 24.2 #14). Stamped `faction` never changes.

Fragment `{{fragment_path}}` under `design/_staging/detail/`: the NPC row with the raised tier, `dm_only` if a secret exists, `mode: detail`, `seeds[]` for `graph` edges and, for major, `goals`, `counts`.

Notes to `{{notes_path}}`. Return, as `{{agent_label}}`:
```json
{{schema}}
```
