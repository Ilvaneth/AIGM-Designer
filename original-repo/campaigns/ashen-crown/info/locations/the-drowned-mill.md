# The Drowned Mill

**Where**: Half a day downriver from Gallowmere, where the river shifted course a decade ago and swallowed the old mill's ground floor
**Level range**: 1-3 (this two-character party should read it as roughly +2 — see `two-player-scaling.md`)
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard (upgraded from a "Small site" sketch 2026-09-02; never played, room count and content variety are new)
**Location class**: Dungeon
**Dungeon Type**: **Ruins** — a functioning river mill until the river shifted a decade ago and flooded the ground floor; nothing built here since, only occupied.
**Payoff type**: **Treasure-heavy** — the smuggler's cache is the site's real, central reward.

---

## Phase 1 — Concept & ecology

**What it was**: A working river mill, its wheel and grinding floor flooded when the river shifted course a decade ago. Abandoned the same season — not worth rebuilding for a mill with no working wheel.

**Who holds it now**: **Stirges**, nested in the dry upper rafters after the flooding emptied the building of people — an easy, undisturbed roost. Below the waterline, something worse: **ghouls** — the remains of a smuggling crew who used the flooded ground floor as a hideout and died there, violently, and didn't stay down.

**Ecology**: The stirges and ghouls don't interact — one roosts high and dry, the other lurks in the dark flooded spaces below, and neither has any reason to cross the other's territory. A cautious party can take the mill without ever waking both threats at once; a loud one gets both.

## Phase 2 — Map (non-linear)

**Entrances**: the mill's main door (now waist-to-chest deep in water, the obvious way in) and the old grain chute — narrow, vertical, the mill's own original mechanism for moving grain to the upper floor, usable as an alternate route that bypasses the flooded ground floor almost entirely.

**Verticality**: a genuinely flooded ground floor (the grinding machinery, waist-deep water, poor footing) against dry, intact upper floors — the fight and exploration space differs sharply between the two.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Flooded Entry** | The main door, waist-to-chest deep water — the first signs of the ghouls (drag marks, old gnaw damage) visible before either creature is encountered. | Entrance | — |
| 2 | **The Grinding Floor** | The old millstone, still submerged — difficult terrain throughout. 1 ghoul, encountered alone. | Combat | — |
| 3 | **The Grain Chute** | Narrow, vertical, the mill's original mechanism — a real alternate route to the upper floor. 1-2 stray stirges nest here too, a preview of the larger roost above. | Combat | — |
| 4 | **The Smugglers' Corner** | Where the crew actually died — real signs of a struggle, worth reading rather than just fighting through. The second ghoul. | Combat | — |
| 5 | **The Stair Landing** | The one dry-to-flooded transition point — rotted stairs, a genuine footing hazard. Investigation/Perception to notice the rot before it gives way; a Dexterity save if it does. | Trap | — |
| 6 | **The Rafters** | The stirge roost proper — the real threat this site was originally built around, a genuine swarm. | Combat | — |
| 7 | **The Storage Room** | The smuggler's sealed strongbox — coin, three casks of genuinely good southern brandy (worth more as a gift than as coin), and a set of forged trade seals still usable for moving goods without inspection. | Treasure | — |
| 8 | **The Loft** | The last, quiet space — a dead smuggler's hidden note, water-damaged but legible, naming who they were moving goods for and hinting at an unpaid debt to someone in Gallowmere. A real, findable thread into "Why it matters beyond loot" below, not just flavor. | Lore | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, checked before finalizing, per `dungeon-design.md`'s standing rule): Combat 4/8 (**50%, in band ✓**), Trap 1/8 (**12.5%, in band ✓**), Special (Treasure) 1/8 (**12.5%, in band ✓**), Structural (Entrance+Lore) 2/8 (**25%, above the 15-20% target** — accepted, a small 8-room site needs at least one true entrance and one closing beat; the same defensible shape already accepted for "The Maker's Undoing" and "The Chalk Warrens").

- **Combat**: 2 ghouls (Rooms 2, 4, encountered separately — never together), the stirge swarm (Room 6) plus a smaller preview cluster (Room 3)
- **Hazard**: the rotted stair landing (Room 5)
- **Exploration/lore**: the smugglers' corner's own evidence (Room 4, alongside its fight), the dead smuggler's note (Room 8)
- **Treasure**: the sealed strongbox (Room 7) — coin, brandy, forged trade seals, each with its own onward use, not flat gold

## Why it matters beyond loot

- **Mother Vey** knows the cache is there. The smuggler who hid it owed her, died out there, and she has never told anyone — she's been saving it. See `info/npcs/mother-vey.md`.
- **Captain Kell** also knows, or suspects, and wants it for his escape fund. He cannot be seen retrieving it. **This is a job he will hire the party for** — and if they take it, they are now holding something Vey considers hers. See `info/npcs/doreth-kell.md`.
- The forged trade seals are a direct enabler for taking over the docks smuggling route. See `info/power-base.md`.
- **Room 8's note** (new, 2026-09-02) gives a third thread: the smuggler's actual unpaid debt in Gallowmere, unconnected to Vey or Kell specifically — a loose end the DM can attach to whichever NPC needs a hook when the party finally reads it.

## The interweave

The mill looks like a simple monster-and-treasure site and is one. It is also a three-way collision: Kell wants it, Vey owns it, and whoever the party hands it to becomes an ally at the exact cost of making the other one a problem. There is no neutral way to loot this building.

## Connections

- `gazetteer.md` — Region I, The Marches, half a day downriver from Gallowmere
- `info/npcs/mother-vey.md`, `info/npcs/doreth-kell.md` — the interweave above
- `info/power-base.md` — the forged trade seals' onward use
