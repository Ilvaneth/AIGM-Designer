# World Reactivity — Design Discussion (in progress, not yet built)

**Status: PLANNING ONLY.** Nothing in this file is implemented yet except the one item marked ✅ below. This is a design conversation moved to its own file because the originating session's context window filled up. Pick up here in the new session — read this whole file first, then continue the discussion or move to implementation, whichever the DM wants.

**Started**: session 6, 2026-08-27, triggered by the Orell Tain incident (see `bug-log.md`, `npc-inconsistency`, 5th instance — an NPC was played offering free help with no basis in his character file).

---

## What's already built (✅ done, not part of this discussion anymore)

**NPC Consistency system** — `.claude/rules/npc-consistency.md` + `npc_consistency_reminder.py` (a `PostToolUse` hook). Every NPC file now carries two living sections: "Current knowledge & stance" (what they currently know, updated as they learn things) and "Decision logic" (how new information could redirect them). Retrofitted to Orell Tain, Sarelle Duskbourne, Sefwyn Marrow, Coren Ashvale, Corvin Thale, Odric Fenn. Other NPCs get it at their next actual appearance.

This is the piece that answers "does this individual NPC act in character." The rest of this document is about the layer above that: **does the world as a whole react to what the party does, and does it keep moving even when they're not looking.**

---

## The diagnosis

Three layers currently exist for "the world moves":

1. **`campaign-clock.md`** — TIME-based triggers ("day N passes, X happens"). Works, but when the party disrupts one of these clocks, the fix is a manual one-off note ("disrupted, day 19-20") — not a system, just a sentence written each time.
2. **NPC files** (just built) — CHARACTER-based reactions. An individual NPC's stance, checked when that NPC is on-screen. Doesn't catch anything accumulating in the background.
3. **Nothing** — there is no layer that (a) accumulates the cumulative damage/benefit the party has done to a faction or NPC over time and escalates a reaction once a threshold is crossed, and (b) generates world events that happen **independent of the party entirely**, so the setting doesn't feel like it only moves when they poke it.

**The DM's litmus test, stated directly in this conversation**: any new mechanic here must produce a **real, integrated change** — new prices, new NPC attitudes, a closed road, a changed map, a spawned side-quest — never just a logged note that gets read once and forgotten. This is the same standard already applied throughout this project (see `bug-protocol.md`'s escalation ladder: a note that depends on being remembered is not a fix).

**Confirmed by checking the actual files** (not assumed): `faction-subplots.md` (73 lines) has good depth on each faction's internal fracture (Sarelle vs. Tain, Coren's Ashvale grievance, the Choir's manufactured-returner problem) but every fracture is **static** — nothing progresses it on its own. `gazetteer.md` already seeds some of what's wanted (e.g. Riverwatch: "kobolds have been stripping the road and accumulated a genuinely odd pile of loot" — exactly a monster-hoard event, but placed once, not a recurring category). **There is no succession-war territory tracker at all** — the war is background flavor, not a tracked state.

---

## The worked example that anchored this discussion — Sarelle

Sarelle Duskbourne has now had **two** fragment-bearing convoys vanish without a trace (session 3, session 6). Per her own character file (`npcs/sarelle-duskbourne.md`) — precise, controlled, "never raises her voice, has people killed the way she'd correct a mis-shelved book" — her reaction to this should **not** be an emotional escalation (that would violate the NPC-consistency rule just built). It should be an **operational** one, proportional to how enormous a loss this actually is to her specific project:

- **Pattern recognition**: two losses is not coincidence to someone this methodical. She should now treat this as deliberate enemy action.
- **Operational hardening**: future shipments get real security changes — larger escorts, decoys, secrecy about routes/timing. This should make the party's *next* fragment-ambush attempt genuinely harder, not just narratively implied to be harder.
- **Convergence risk**: she already holds physical descriptions ("an elf and a dragonborn," day ~5). A sharp administrator cross-referencing two ambush locations against that description is the natural way this campaign's long-simmering "the party is hunted" thread finally pays off — this should be a real, trackable risk, not a DM fiat moment.
- **The planted evidence**: Ilvaneth forged Ironclad Compact evidence at the second ambush site (Forgery 26). This is a live variable — it might work (Concordat-Compact friction opens up, a real and valuable consequence) or it might not survive Sarelle's own scrutiny (she's established as sharp). Whichever way this resolves should be a tracked outcome, not something decided in the moment with no memory of the setup.

This example is the reason the discussion generalized: Sarelle isn't the only person in this world capable of noticing a pattern and reacting to it. The system needs to work for *any* faction or major NPC, not be hand-built once for Sarelle and left as a one-off.

---

## Proposed system 1 — the Consequence Ledger

A new file, `campaigns/ashen-crown/info/consequences.md`. Structure (draft, open to revision):

- **Per faction (Concordat, Compact, Choir) and per major NPC**: a running log of every significant thing the party has done *to* them — losses inflicted, secrets stolen, plans foiled, trust built or broken. Dated, like `bug-log.md`'s own log table.
- **Escalation thresholds, defined per faction/NPC and matched to their own established character** (this is where it plugs into the NPC-consistency work already done): e.g., for Sarelle, 2 unexplained convoy losses = pattern threshold, triggers the operational hardening described above. The Compact might never "escalate" emotionally at all, but would quietly stop extending certain contracts, or raise their price for anyone matching the party's description. The Choir might read repeated interference as proof of heresy needing punishment, on their own doctrinal terms.
- **Checked at session start**, alongside `campaign-clock.md`'s day-advance step — "has any faction/NPC's cumulative consequence count crossed a threshold since we last checked?"

## Proposed system 2 — World Events (things that happen with zero party involvement)

A `d10`/`d12` table (or several, regional or campaign-wide — undecided) rolled at session start, structurally similar to `travel-encounters.md`'s regional tables but for world/politics scale. Discussed categories, each with the DM's own refinement attached:

- **Succession war developments** — a battle won or lost, a region's control changing hands, new hostility opening between two groups that weren't at war before. **Must have real mechanical teeth**: proposed a **Region Control tracker** over `gazetteer.md`'s 8 regions (who currently holds/influences each one) — when this changes, prices, available NPCs, and which faction has visible presence in a region all update for real, not just in prose.
- **Faction-internal maneuvers** — all three factions are chasing the Crown; each fracture in `faction-subplots.md` needs to be capable of progressing **on its own**, not just when the party pokes it. Proposed: a simple staged-progress marker per fracture (e.g., quiet → tension → open break) that World Events rolls can advance even with zero party involvement.
- **Rumors/prophecies** — `rumors.md` already exists (d12 pool, true/false tagged) but is currently only triggered when the party asks around; it should also feed off World Events rolls, and needs a documented "if this rumor is true, what actually happens" consequence for each entry, not just flavor. **Prophecy Threads** proposed as a distinct sub-category: an item, a belief, or a quest that people are chasing, capable of reshaping the world in a specific way — giving the setting more mystery, and echoing the Cinder Choir's own "seeking a returner" doctrine model as a template for how a prophecy-driven thread can work.
- **Monster/hoard activity** — goblins/orcs hoarding somewhere, a dragon claiming a lair, etc. `gazetteer.md` already has a working example of this shape (Riverwatch) — the ask is to make it a recurring, rollable category instead of a single hand-placed instance.
- **Other actors** — rival adventuring parties, bounty hunters, competing fragment-seekers. Explicitly must use the full NPC template (including the new Current knowledge & stance / Decision logic sections) the moment they're generated — never a throwaway sentence with no real file behind it.
- **DM's additional proposed category, agreed on in discussion**: **reputation feedback** — as the party's power base (`power-base.md`) grows, the world should notice and react (rivals emerging, factions taking them more seriously) — currently a one-way street (party affects world; world doesn't yet respond to the party's *growth* specifically, as distinct from their specific actions).

## Resolved — 2026-08-28, before any build work

Every open question below is now decided. Nothing in this section is built yet (that's the next step) — this is the locked spec the build has to follow, written down *before* implementation specifically so `consequences.md`'s format and `consequence_check.py`'s parser are designed together instead of the rule being written first and the script retrofitted after (the exact trap `standing_rule_hook.py` now catches generally, see `bug-protocol.md`).

### Region Control
Lives **inside `gazetteer.md`**, not a separate file — same reasoning as `state.md`'s single-source-of-truth fix for HP/gold/XP: two files tracking the same fact is how `state-drift` became the project's single most common bug category.

### Faction-fracture progress markers
Live **inside `faction-subplots.md`** (current state), not `consequences.md`. `consequences.md` only logs the dated event that moved a fracture's stage — mirroring the existing `bug-log.md` (dated log) / `system-register.md` (current status) split.

### Escalation thresholds — where the number lives
**The numeric threshold and its status live only in `consequences.md`** — not duplicated into each NPC/faction file. Reasoning: an exact number ("2 losses") is a mechanical tracking fact, the same category as HP or a day-counter, not narrative content. Each entity's own file (`npcs/*.md` Decision logic, or `faction-subplots.md`) keeps the **qualitative** reaction already written there (Sarelle: "pattern recognition, operational hardening") — `consequences.md`'s threshold line points back to it by name instead of restating it, so the reaction's substance still has exactly one home.

### `consequences.md` format (parseable — this is what makes `consequence_check.py` possible)

```markdown
### <Entity Name>
**Threshold**: <N> → <short label> (see `<path to file>`, Decision logic)
**Status**: pending | crossed-unapplied | applied (day <D>)

| Date | Event | Weight |
|------|-------|--------|
| Day <D> | <what happened, one line> | <integer> |
```

- **Weight is a plain integer**, never a unit-labeled string ("1 loss") — the unit belongs only in the `**Threshold**` line's label, so the Weight column stays trivially summable.
- The script never trusts a separately-written cumulative total — it **sums the Weight column itself** every time, the same reason `state.md`'s party block is generated from character files rather than hand-maintained: a second hand-written number is a second thing that can drift.
- `consequence_check.py` (to build alongside the file, not after): for every `### Entity` block, sum Weight, compare to Threshold. If sum ≥ threshold and Status is still `pending`, flag it — same shape as `clock_check.py`'s overdue-clock check. Once actually applied in play, Status flips to `applied (day D)` by hand (a deliberate assistant action, matching `rest_check.py`'s "never auto-apply silently" precedent) and the script stops flagging that entity unless a second threshold tier is later added as its own block.

### Retroactive backfill — required before the system goes live
Sarelle Duskbourne already has 2 convoy losses in the fiction (day 20, day 39) — per her own file, that already crosses a 2-loss pattern threshold. Building `consequences.md` starting from zero would silently erase history the same way Sefwyn's "re-initiate contact" clock sat forgotten for 12 days before it was made a real clock (`bug-log.md`, 2026-08-27). **Day-1 task**: backfill Sarelle's entry with both historical events already at `crossed-unapplied` status, so her operational-hardening reaction is owed *immediately* on build, not from some hypothetical future third loss. Sweep for any other faction/NPC with comparable accumulated history before considering the system live (Fennick's confession, Odric Fenn's turning, etc. — check each against whatever threshold gets defined for it, don't assume only Sarelle qualifies).

### Write-immediately hook — extend, don't duplicate
**Extend `knowledge_sync_reminder.py`'s existing message** (it already fires on every `session-N-combat-*.md` / `session-N-npc-*.md` write) to also ask whether the event affects a faction/NPC's `consequences.md` entry — do **not** build a second near-identical `PostToolUse` hook. This project already has a logged `hook-fragility` incident from two hooks sharing near-duplicate logic without sharing code (the `APPROACH_WORDS` false-positive fixed in one script and not the other, `bug-log.md` 2026-08-27) — one hook, two reminders in its message, is the fix that doesn't reintroduce that risk.

### `campaign-clock.md` vs. `consequences.md` — deliberate separation, not overlap
`campaign-clock.md` keeps **scheduled/time clocks** (when does X happen if nothing intervenes, and how did an event delay/deny a tick — it already does this for Sarelle's "Sarelle collects" clock). `consequences.md` keeps only the **cumulative reaction count** toward a threshold. The same real event can appear in both, but each file states only what's relevant to its own question, and cross-references the other by name instead of restating it — the same pointer convention already used between `bug-log.md` and `system-register.md`.

### World Events cadence — locked: every 7 in-fiction days
Rolled at session start, scaled by elapsed days, not once per session regardless of day count — matching `travel-encounters.md`'s per-night logic at a larger scale. Tracking mechanism, mirroring `rest_check.py`'s `**Last Long Rest**: Day N` pattern exactly: a new `**Last World Events Roll**: Day N` line in `state.md`, next to the existing Last Long Rest line. At session start: `rolls = floor((current_day - last_rolled_day) / 7)`; after rolling, advance the marker by `rolls * 7` (not to the current day), so leftover days under 7 carry forward instead of being lost. A future `world_events_check.py` reads this the same way `rest_check.py` reads its own marker.

## Where to resume

**Design is locked.** Next step is building, together, in one pass so the rule and its script are never separated in time:
1. `consequences.md`, seeded with Sarelle's backfilled entry (and any others the sweep finds).
2. `consequence_check.py`, wired into `session_state_gate.py` the same way `clock_check.py` already is.
3. The `**Last World Events Roll**: Day N` line in `state.md`, plus `world_events_check.py`.
4. Extend `knowledge_sync_reminder.py`'s message text (one line, not a new script).
5. The actual World Events d10/d12 table content itself (regional vs. campaign-wide — still genuinely open, decide when writing it).
6. Region Control table inside `gazetteer.md`.

Nothing here is committed until it's actually written into a real system file — this document is the locked spec, not the system itself.
