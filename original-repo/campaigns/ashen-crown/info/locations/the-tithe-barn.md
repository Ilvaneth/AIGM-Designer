# The Tithe Barn

**Region**: II. The Thornlands
**Level range**: 3-5 (this two-character party should read it as roughly +2 — see `two-player-scaling.md`; effectively 5-7)
**Site type**: Small dungeon, single structure with a basement level (expanded to 10 rooms, upgraded to full `.claude/rules/dungeon-design.md` standard 2026-09-02)
**Location class**: Dungeon
**Dungeon Type**: **Ruins** — an abandoned tithe collection point, occupied but never rebuilt by anything living here now.
**Payoff type**: **Treasure-heavy** — the grain itself, a trade good with a real destination rather than flat coin.

An abandoned granary that once collected the crown's grain tithe from the surrounding farms — abandoned when the collecting authority stopped sending anyone to claim it, years into the succession war. Three seasons' worth of grain sits inside, hoarded and untouched, while the refugee camps in Gallowmere and elsewhere go hungry.

**⚠ Two-character party check** (`two-player-scaling.md`): the ochre jelly (CR 2, 450 raw) solo-adjusts to 675 — fair for this range. The swarm is a nuisance-tier threat, not a real damage risk. Neither should be fought simultaneously — they occupy different rooms by design. **The Shambling Mound (Room 10, CR 5, 1,800 raw) solo-adjusts to 2,700 — Deadly at level 5.** Re-run `py .claude/scripts/solo_burst_check.py ashen-crown --vs plant --full-nova` against the party's real sheet before running this fight — do not lock in HP/Legendary Resistance now against numbers that will be stale by the time this site is actually played, per the same principle already applied to "The Maker's Undoing"'s Clay Golem.

## Phase 1 — Concept & ecology

**What it was**: A functioning tithe collection point, built solidly enough that it survived years of neglect intact. **What lives here now**: an **ochre jelly** that got in through a damaged wall seam and has been slowly consuming the barn's spoiled outer grain stores, a **swarm** (insects, drawn by the rot) nesting in the upper loft, and — deeper, beneath the root cellar, where nobody has looked in years — a **shambling mound** that grew from the same rot and rainwater seepage the jelly has been feeding on, now large enough to be a real threat. None of the three coordinate or even know about each other; each just lives in the part of the barn its own ecology suits.

## Phase 2 — Map (non-linear)

**Entrance**: the damaged outer wall — the same breach the ochre jelly used, obvious once noticed.

**Verticality**: ground floor (the main grain hall), a loft above (swarm territory), a root cellar below (the preserved grain), and — new, 2026-09-02 — a flooded foundation level beneath even the cellar, where the mound has grown undisturbed for years.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Damaged Wall** | The ochre jelly's entry point — visible acid-scarring on the wood, a clear warning sign for anyone who checks before walking in | Entrance | — |
| 2 | **The Main Grain Hall** | Mostly spoiled, rot-blackened grain — the ochre jelly's territory, sluggish and slow-moving, avoidable with caution | Combat | — |
| 3 | **The Loft Stair** | A rickety ladder up — disturbing it risks waking the swarm before the party's ready | Trap | — |
| 4 | **The Loft** | The insect swarm's nest — unpleasant, not deadly, a nuisance encounter rather than a real threat at this level | Combat | — |
| 5 | **The Root Cellar Door** | Sealed, undisturbed — a DC check or the right tool opens it cleanly, bypassing the ochre jelly's contamination entirely | Puzzle | — |
| 6 | **The Root Cellar** | The real prize: three seasons of properly preserved grain, untouched by rot or jelly — a direct, mechanical power-base resource, not just coin | Treasure | — |
| 7 | **The Flooded Foundation** | The barn's original footing, reached through a second, damp-swollen door at the back of the cellar — ankle-deep standing water, rotted support beams (a real structural hazard, Investigation to notice which are safe to touch). A strongbox here, from whoever the crown last sent to check on this barn years ago and never recovered, holds personal effects and a short, unfinished report ending "the floor moves" — a real, findable clue for Room 8, not a blind ambush. Added 2026-09-02, per DM request. | Trap | — |
| 8 | **The Rotted Heart** | **Boss fight — a shambling mound**, grown from years of rot and seepage, large enough now to be the real reason nobody who came looking ever reported back. Guards nothing on purpose — it doesn't know or care what it's sitting on, same design principle as Chalk Warrens' otyugh. Added 2026-09-02, DM-requested addition. | Combat | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02): Combat 3/8 (**37.5%, below the 50-60% target**), Trap 2/8 (**25%, above the 10-15% target**), Special 2/8 (**25%, above the 10-15% target**), Structural 1/8 (**12.5%, below the 15-20% target**). **Accepted as a deliberate deviation, DM decision 2026-09-02** — the DM specifically requested one new room plus a boss (Room 7-8) rather than a ratio-driven expansion, consistent with this site's own established philosophy that "a careful party can potentially avoid one or both [threats] entirely" — a low-combat-pressure design in the same spirit already accepted for `the-weeping-wood.md`.

- **Combat**: the ochre jelly (Room 2), the swarm (Room 4), the shambling mound boss (Room 8)
- **Hazard**: the loft stair's waking risk (Room 3), the flooded foundation's rotted beams (Room 7)
- **Puzzle/exploration**: the root cellar door (Room 5)
- **Treasure**: the preserved grain (Room 6), the dead collector's strongbox (Room 7, alongside its hazard)

## What the grain is worth

Not gold — **supply**. A refugee camp (Alis Wend's, or any other the party invests in) fed from this cellar is a real, integrated change to that thread, not a coin value. This is the campaign's clearest example of a reward that matters more as leverage than as loot.

## Connections

- `gazetteer.md` — Region II, the Thornlands
- `npcs/alis-wend.md`, `power-base.md` — a direct resource for either the refugee thread or a Gallowmere power base
