---
phase: detail
role: writer
kind: chapter
effort: high
critics: 1
schema: writer
---
{{common}}

## Your task — make a chapter's nodes concrete on entering a new act

Campaign **{{campaign}}** at `{{campaign_dir}}`. Entity **{{entity_id}}** ({{entity_name}}: {{entity_summary}}). Directions from the DM (the day, where the party is, what the last act decided):
{{directions}}

Read exactly these files (the chapter, its nodes, the arc, the faction operations, `news.json`, the overlay, the threads):
{{files}}

On entering a new act the chapter's nodes are made concrete (item 13.3): who is where today, each site's current state (skeleton / detailed / played, from the overlay), everything the simulation has done up to this day applied (control flips, dead or fled NPCs, moved assets, the threat stage), the beats that landed or were pre-empted and which fallback the DM chose (`arc fallback` records in `state.md`), the news records that reach the chapter's places. Rewrite the chapter file's node sections with today's facts; the stamped act and level band and the node ids never change; no entity of a later act is referenced.

Fragment `{{fragment_path}}` under `design/_staging/detail/`: the chapter row unchanged in its stamps, the node rows updated (`stake_tr`, `if_never_arrives_tr` re-dated), `mode: detail`, `counts` (`nodes`, `news_applied`).

Notes to `{{notes_path}}`. Return, as `{{agent_label}}`:
```json
{{schema}}
```
