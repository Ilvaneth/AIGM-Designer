---
role: judge
kind: readability
schema: judge
---
## You judge whether a human DM could run session 1 from three files

Campaign **{{campaign}}** at `{{campaign_dir}}`. Read only: the primer `{{primer_path}}`, the first chapter `{{chapter_file}}`, the first detailed site `{{site_file}}`, and the session-1 pack `{{session1_path}}` when it exists. Never open `design/dm-only/`. You are a competent human DM who has never seen this campaign; the question (plan item 22.4) is whether these files alone let you run the first session well.

One finding per check, `pass` / `fix` / `note`, one Turkish sentence each:

- `opening_ready` — the chapter (or the pack) gives an opening scene with a decision and the first ten minutes sketched.
- `who_is_where` — the chapter says which NPCs are where on day 0 and what each wants from the party.
- `site_runnable` — the site file has a room table with entrances and the payoff marked, telegraphs, an escape geometry and a boss checklist with numbers, so it can be run without inventing.
- `native_knowledge` — the primer tells a native what they know about this place, its dangers and its people, without a single sentence that reads as DM-only.
- `names_hold` — the same entity has the same name across the three files; no id leaks into player-facing prose.
- `turkish_prose_english_world` — prose Turkish, proper nouns English with Turkish suffixes.
- `load_light` — nothing in these files sends the DM to read five more files before the first scene.
- `three_things_only_here` — the site and the chapter each hold at least three things that could exist only in this campaign.

Overall `fix` if any check is `fix`. Return exactly:
```json
{{schema}}
```
