---
phase: detail
role: writer
kind: settlement
effort: medium
critics: 1
schema: writer
---
{{common}}

## Your task — fill a settlement's small points during play

Campaign **{{campaign}}** at `{{campaign_dir}}`. Entity **{{entity_id}}** ({{entity_name}}: {{entity_summary}}). Directions from the DM's prep step:
{{directions}}

Read exactly these files:
{{files}}

The anchors exist since birth; you fill the **small-point budget** (item 13.3): shops, inns, district characters from `data/design/settlements.yaml#small_point_kind`, each a `place_` entity with settlement, district, kind, owner (a roster NPC or a new minor NPC registered in the fragment) and services; a price table from the current economy (the overlay's modifiers, the wealth ladder, SRD prices); local rumours from `news.json` records whose reach includes this settlement. Small points are **permanent** once named (errata 24.2 #14): an inn named once is that inn forever; never rename or remove an existing `place_`. Stamped facts (scale, polity, ruler at birth) never change; the current ruler is the overlay's.

Fragment `{{fragment_path}}` under `design/_staging/detail/`: the settlement row unchanged except the small-point table's status, the new `place_` and `npc_` rows, `mode: detail`, `counts` (`places`, `prices`, `rumours`).

Notes to `{{notes_path}}`. Return, as `{{agent_label}}`:
```json
{{schema}}
```
