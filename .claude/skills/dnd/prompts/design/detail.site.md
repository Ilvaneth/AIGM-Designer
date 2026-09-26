---
phase: detail
role: writer
kind: site
effort: medium
critics: 1
schema: writer
detailed: true
---
{{common}}

## Your task — detail a skeleton site during play

Campaign **{{campaign}}** at `{{campaign_dir}}`. Entity **{{entity_id}}** ({{entity_name}}: {{entity_summary}}). Directions from the DM's prep step:
{{directions}}

Read exactly these files (the skeleton, the stamped facts, the connected entities two hops out, the news feed and simulation state to date, the matching dm-only file, the relevant state.md section, `SKILL-encounter-design.md`):
{{files}}

This is the birth machinery run in play (item 13.3, 24.6 #5): the play tab never authors the file. Turn the skeleton into the four-phase detailed file exactly as the P6 site writer does (`templates/design/site-detailed.md`: concept and ecology, the map with ≥2 entrances and a loop, the room table with `[Entrance]` / `[Payoff]` markers at the stamped room count and minimum depth, the content variety check, running this well, connections, telegraphs, escape, attitude, the boss checklist against the reference party — `burst_check.py --campaign {{campaign}} --reference --tier <danger tier> --target-hp <boss HP>`, output pasted —, rest pressure), with three constraints of play:

- **Never a stamped fact changed**: danger tier, room count, act, thread, key NPCs stay; the validator diffs them.
- **Never a later act spent**: no entity stamped to an act later than this site's own act may be referenced (errata 24.2 #9).
- **The world as it is today**: apply every news record that touched this site or its faction since birth (a control flip, a dead keeper, a moved asset) before writing the ecology; the overlay's current values, not the birth values.

Then the detail-time critique's questions in your notes: three things that could exist only here; what a party three levels early sees and where it runs.

Fragment `{{fragment_path}}` under `design/_staging/detail/`: the site row with unchanged stamps, `overlay: {"status": "detailed"}`, `mode: detail`, `seeds[]` with `site_progress open`, any `item_` / `creature_` rows, `counts`.

Notes to `{{notes_path}}`. Return, as `{{agent_label}}`:
```json
{{schema}}
```
