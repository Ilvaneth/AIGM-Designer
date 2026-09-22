# Companions — recruited allies, deployed on tasks

**Why this exists**: `two-player-scaling.md` names companions as a fix for this party's action economy, and `power-base.md` lists "armed force" (the Sorrel's Hollow deserters) as a holding built around recruiting rather than clearing them. Neither file said how to actually run one at the table. Built 2026-08-25, at the point Roskel was recruited.

Status: **provisional** — first real test is Roskel himself.

---

## The core decision

**The party stays a two-person party.** A companion is not a third combatant bolted onto every fight — that would quietly turn this into a three-PC game and undercut the whole two-player identity the campaign is built around (`two-player-scaling.md`, `dm-notes.md`).

Instead, a companion is an **asset you deploy**, the way you'd use a hireling, a contact, or a spy — not a party member who happens to have fewer lines.

## What a companion actually does

### 1. Tasks — the default use

Send a companion to do something **instead of** the party doing it personally:

- Investigate a location, ask around, gather information
- Tail or surveil someone
- Run an errand — buy something, deliver a message, sell something without the party's face attached to it
- Watch/guard something while the party is elsewhere
- Anything else that's a job, not a fight

**Resolution**: one roll, using the companion's own relevant stat, made by the DM (companions aren't PCs — their rolls follow the same ownership rule as any NPC's: DM rolls via `roll.py`, never invented). State the task, the DC, and what's riding on it, roll once, narrate the outcome as success / partial success with a complication / failure. Don't turn a supply run into a five-exchange scene — that defeats the point of delegating it.

**Time cost**: tasks take real in-fiction time — state a rough duration when assigning one (hours for something local, a day or more for travel), and advance the campaign clock accordingly like any other time skip.

**Roskel specifically** is well-suited to: reading a military situation, intimidating or getting a straight answer out of soldiers/deserters/guards, physical tasks requiring Athletics, and anything trading on "I used to be a sergeant, people still listen to that."

### 2. Combat — opt-in, per encounter, not standing

A companion does **not** automatically fight alongside the party. By default they're wherever the party left them, or off on a task.

If the party wants a companion in a *specific* fight, they bring them along **before** it starts — a deliberate choice, made in the fiction, not a standing addition to the initiative order. When they do:

- **HP cap**: roughly one PC's worth, not their full source stat block. Roskel: **30**, not his Veteran 58.
- **One attack per turn**, even if their stat block has Multiattack. This is what actually prevents them from outshining a PC — Roskel's Multiattack alone did 17 damage to Kriv in one round during the fight where he was captured.
- **AC / to-hit / damage per hit**: unchanged from the source stat block.
- They act on their own initiative roll, run by the DM with simple, obvious tactics (protect whoever brought them, focus the clearest threat, disengage below a quarter HP) — a player can give them an order, but doesn't have to manage their turn in detail.
- **They can go down** — same 0 HP / death save rules as anyone. A companion dying in a fight the party chose to bring them into is a real consequence, not something the rules protect them from.

## Loyalty — fiction only, no mechanic

There's no loyalty score, no morale die, no relationship number. A companion does what fits who they are:

- Ask them for something reasonable, in line with their character → they do it.
- Ask them for something that violates who they are, or treat them badly → they refuse, argue, or eventually leave. That's a roleplay consequence, decided in the moment, not a subsystem.

Roskel is a proud, competent 20-year veteran who just watched everyone he commanded die and chose to follow the last legitimate heir of a house he respects. That's the read to run him from — not a hidden number.

## Knowledge — same discipline as any NPC

**Added 2026-09-04** after Roskel was given a line at Shestendeliath Hold claiming knowledge of Magus Orell Tain's attainder-research status — a thread he has no channel to (`bug-log.md`, `npc-inconsistency`, 15th instance). Root cause: standard NPCs (`info/npcs/*.md`) carry `## Current knowledge & stance` and `## Connections` sections per `.claude/rules/npc-consistency.md`, kept live and checked before writing any of that NPC's dialogue — this file's lighter template never adopted the same structure, so a companion had no equivalent boundary to check against.

Every companion file now carries the same two sections, same discipline as any other NPC:

- **`## Current knowledge & stance`** — what this companion actually knows, kept current, updated the moment they learn something new in play. Include explicit "does NOT know" boundaries for anything a player might plausibly have them reference, not just a positive list.
- **`## Connections`** — who they have a real channel to. Before writing any line where a companion references another NPC's business, check this list — if the NPC/thread isn't on it, they don't know it, per `npc-consistency.md`'s cross-NPC knowledge rule.

## File — one per companion, once they're a real character

A companion who's had one scene isn't worth a file. Once someone is actually recruited and being tracked (HP, tasks, ongoing relationship) — write `party/companions/[name].md`, **not** `party/characters/` (that folder is scanned by `update_character.py` and `sync_state.py` and would get the companion mistaken for a third PC in the party block). Same principle as PC sheets: this file is the single source of truth for their current HP and state — don't duplicate it in prose in `state.md`, link to it instead. See `party/companions/roskel.md` for the template this produced.

`update_character.py` doesn't know about this folder, so HP changes are edited by hand (`Edit` tool) rather than the script — acceptable for now since companions change state far less often than PCs; revisit if that stops being true.

## Multiple companions

If the party ends up with more than one, the same rules apply individually to each. Nothing here stops the party from having several companions active on different tasks simultaneously — that's the point of using them as a network rather than a single extra sword.

## Log

| Date | Change |
|------|--------|
| 2026-08-25 | Built at the table when Roskel was recruited: task-deployed assets by default, combat participation opt-in per encounter, no loyalty mechanic. |
| 2026-09-04 | Added the `## Current knowledge & stance` / `## Connections` requirement after a real Roskel incident (see above) — every companion file now carries the same knowledge-boundary discipline as a standard NPC file. |
