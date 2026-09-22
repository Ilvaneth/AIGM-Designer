# TODO — Build the 5 map-derived Karsgate locations

**Why this file exists**: session 7 (2026-08-29) generated a final campaign map (`info/images/Ashen_Crown_MAP.png`, moved into `info/images/` session 9) using GPT after three earlier Gemini attempts. The GPT version invented five small features clustered around Karsgate that don't exist in any campaign file yet: **Mill, Outer Farm, Riverside Docks, Caravan Halt, Stonebridge**. The DM wants these built out as real locations, not left as map decoration. This task was deliberately deferred to a fresh session — the prior session was at ~92% context and finishing this properly (to today's own standard) needed a clean budget, not a rushed tail end.

**Start with `/dm-start-session ashen-crown`** as normal — this loads `two-player-scaling.md`, `dungeon-design.md`, `faction-design.md`, and everything else this task depends on, per the mandatory list fixed earlier this same session (see `system-register.md`, 2026-08-29, "Full cross-system audit" entry).

---

## Step 0 — Ground truth check, before building anything

**The map (`info/images/Ashen_Crown_MAP.png`) is a visual reference only, not authoritative data.** Across four generation attempts this session, the image models repeatedly hallucinated names, dropped a real established location (Millward Crossing never once appeared), and produced inconsistent/garbled legend text. Treat the map as "here's roughly where five unnamed features could sit," not as a source of truth for anything else on it. **Do not silently trust any other detail on the map** (troop positions, extra unlabeled icons, exact distances) without cross-checking it against the actual campaign files the same way this step already flags for the five names.

Before writing anything:
1. Read `locations/karsgate.md` in full, specifically the Riverside district's existing entries (**The Long Quay**, **Vantor Shipping's Warehouse**, **Smuggler's Row**, etc.) — **"Riverside Docks" is very likely the same thing as Karsgate's already-built Riverside district**, not a new location. Confirm this and fold it in as a cross-reference rather than building a duplicate. This is the single most important check in this whole task — a duplicate/near-duplicate location is exactly the kind of naming collision `name_collision_check.py` was built to catch, but a *conceptual* duplicate (two locations that are really the same place) won't show up in that script's word-based scan, so it has to be caught by actually reading the file first.
2. Check `gazetteer.md`'s Karsgate entry and `locations/karsgate.md`'s own opportunities/connections sections for anything already implying a mill, farm, or bridge near the city that these four remaining names might already overlap with.

## Step 1 — Decide scope per site (a real DM judgment call, not automatic)

Per `dm-notes.md`'s "nothing is purely side content" standing rule, default to giving each site real narrative substance — but not everything needs the full multi-room `dungeon-design.md` treatment. Ask the DM directly (don't assume) which tier fits each:
- **A full site file** (`locations/<name>.md`), for anything with a real hook, a fight, or a recurring purpose.
- **A short entry inside `locations/karsgate.md`'s own location tables** (matching how the five neutral sites and the casino/dirty-contractor additions were handled earlier this session), for something that's genuinely just a piece of Karsgate's immediate hinterland rather than its own destination.

Suggested starting read (confirm with the DM, don't build silently):
- **The Mill** and **Outer Farm** — plausibly light entries in `karsgate.md`'s own tables (working countryside just outside the walls), unless the DM wants a real hook for one of them.
- **Stonebridge** — plausibly a landmark/waypoint (a literal stone bridge crossing), unless the DM wants an encounter or a toll/checkpoint angle for it.
- **Caravan Halt** — the strongest candidate for a genuine small site with real content (a rest stop draws travelers, rumors, maybe a job) — consider building this one closer to the standard already used for `the-driftway-fair.md` (recurring, low-stakes, real content) rather than a combat dungeon.

## Step 2 — Build to the established standards, per site

For anything that becomes a real site file:
- Follow `.claude/rules/dungeon-design.md`'s four phases if it has any real room/combat structure.
- Add the `two-player-scaling.md` scaling check box immediately if there's any fight potential at all — do not skip this the way 12 of 13 sites did earlier this session before being caught and fixed. Apply the corrected guidance directly (HP sized to this party's actual burst for anything solo, spread/sentry/leader techniques for anything a group) — don't reintroduce the mistake that was just fixed.
- Any named NPC with real substance gets a full file per `.claude/rules/npc-consistency.md` and is tiered per `.claude/rules/npc-tiers.md` (Important vs. Minor, a Class & Level line, a Move List if it gets a `consequences.md` threshold) — the `npc_tier_hook.py`/`npc_tier_check.py` enforcement will catch an incomplete NPC file automatically, but tier the NPC correctly from the start rather than relying on the hook to catch a shortcut.
- Check faction ties honestly — these sites sit right next to Karsgate, where all three factions now have a real presence (`factions/*.md`). Don't force a faction connection if none makes sense, but don't default to "faction-free" just because the other five Karsgate-area sites happened to be neutral, either.

## Step 3 — Update the index and cross-references

- Add each finished site to `gazetteer.md`'s Karsgate entry, matching the format already used for the five neutral sites and Karsgate's own casino/underworld additions.
- If "Riverside Docks" is confirmed as the same thing as the existing Riverside district (per Step 0), add a note to `locations/karsgate.md` itself clarifying this is what the campaign map's "Riverside Docks" label refers to, so a future session doesn't get confused by the same ambiguity.
- Update `info/images/Ashen_Crown_MAP.png`'s standing (if the DM wants) — no action needed on the image itself, just make sure the text files are the actual source of truth going forward, per Step 0.

## Step 4 — Close it out

- Run `py .claude/scripts/name_collision_check.py ashen-crown` after all new names are in — check the output by hand, most hits will be expected generic-word recurrence (per this session's own established pattern), but read every line.
- Run `py .claude/scripts/session_state_gate.py` (or just let the `Stop` hook do it) to confirm nothing's left in a broken state.
- Log the batch to `system-register.md` (a new capability/content entry). Only add a `bug-log.md` entry if something was actually found wrong along the way (per `bug-protocol.md`'s own test: would this need to behave the same way next time?) — building new content isn't itself a bug, per `bug-log.md`'s own "What this log is not" section.
