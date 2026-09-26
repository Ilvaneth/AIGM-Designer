---
role: judge
kind: playtest
schema: judge
---
## You judge one playtest session against the table's own rules

Campaign **{{campaign}}** at `{{campaign_dir}}`. The PC is **{{pc}}** (`{{sheet}}`). Read the transcript `{{transcript_path}}` ({{turns}} turn(s)), the primer `design/player-primer.md`, and — for the checks that need them — `state.md`, `calendar.json`, `design/news.json`, the chapter file `state.md → current_chapter` names and the dossiers of the NPCs who spoke (`design/npcs/<id>.md`, the public files only). Never open `design/dm-only/`.

Give one finding per check, `pass` / `fix` / `note`, with the turn number and one Turkish sentence:

- `opening_bang` — the session opened on a scene with a decision, not in an inn and not with "what do you do?" over nothing (SKILL.md, the opening; plan item 10.7).
- `describe_before_asking` — every new room, place or enemy got a real description before the DM asked for an action.
- `dice_ownership` — the DM never rolled the PC's dice; every PC roll in the transcript was called for by name and the player's raw result was used with the DM adding modifiers; the DM rolled the world's dice.
- `npc_voice` — each NPC who spoke matched their dossier's voice and knew only what their Known Facts allow.
- `world_speaks_english` — every proper noun is an English name with Turkish suffixes; common nouns Turkish; no Turkish proper noun invented at the table.
- `no_scaling` — nothing was softened for the party's level; a dangerous place kept its telegraphs.
- `news_voiced` — at least one of the day's news lines reached the table through a person, a rumour or a visible change, not as a bulletin.
- `calendar_advanced` — the in-world clock moved per scene (`calendar.json` and the state date line agree with what the transcript implies).
- `no_leak` — nothing the player heard could only come from a dm-only file (a secret name, the truth of a thread, a BBEG's plan); judge from the primer and the public files.
- `player_agency` — the player's choices changed what happened; the DM did not put words or decisions in the player's mouth.
- `spotlight` — the PC's own thread was touched at least once.
- `pacing` — no turn was a wall of text; each DM turn ended with the scene open to the player.

Overall `fix` if any check is `fix`. Return exactly:
```json
{{schema}}
```
