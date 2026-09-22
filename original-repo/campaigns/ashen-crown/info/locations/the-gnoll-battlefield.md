# The Gnoll Battlefield

**Region**: IV. Karsgate (a half-day's ride out, along a disused stretch of road)
**Level range**: 5-7 (this two-character party should read it as roughly +2 — see `two-player-scaling.md`; effectively 7-9)
**Site type**: Small dungeon, faction-free (expanded to 8 rooms, upgraded to full `.claude/rules/dungeon-design.md` standard 2026-09-02)
**Location class**: Dungeon
**Dungeon Type**: **Ruins** — an old skirmish site, wreckage and dead never fully cleared; the gnolls occupying it built nothing.
**Payoff type**: **Treasure-heavy** — modest but real, per this file's own established Treasure section.

**⚠ Two-character party check** (`two-player-scaling.md`): the gnoll pack is roughly half a dozen strong but split across the site by design — never fought as one group. A pack of 3 gnolls together is already ~450 raw XP at the 3-6 monster multiplier, bumped to ×2.5 for two PCs = 1,125 adjusted, Hard-to-Deadly at level 5 — fine as an occasional set piece (Room 8, the Den), never the default.

---

## Phase 1 — Concept & ecology

**What it was**: A supply column, ambushed and wiped out years ago during an earlier stretch of the succession war — the wreckage and dead never fully cleared, the road it once used now disused.

**Who holds it now**: A **gnoll** pack, moved in since to scavenge the battlefield's own dead and anything travelers leave behind — entirely their own opportunistic ecology, not tied to any faction's plans.

## Phase 2 — Map (non-linear)

**Entrance**: the disused road itself, the obvious approach — no hidden second entrance needed for a site this exposed, but the wreckage field itself offers multiple lines of approach rather than a single choke point.

**Verticality**: mostly flat (a surface battlefield), except the Den itself, dug into the collapsed underside of the wagon line — a real drop in ceiling height and footing once the party goes under.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Approach** | The disused road itself — the first wreckage visible from a distance, no immediate threat. | Entrance | — |
| 2 | **The Wagon Line** | Collapsed supply wagons, still loaded with rotted goods — 2 gnolls posted here as lookouts, genuinely on watch (gnolls have a keen sense of smell in their own right) — a real chance at least one notices the party regardless of Stealth, denying a clean full-group surprise. | Combat | — |
| 3 | **The Officer's Cairn** | A hastily-built grave marker for whoever commanded the original column — a DC check finds a signet or unit marking, a small lore hook about which faction lost this fight originally. | Lore | — |
| 4 | **The Bone Field** | The main battlefield proper — scattered remains, weapons rusted into the ground, difficult terrain from wreckage. A real footing hazard for anyone moving through carelessly (a DC check to avoid a nasty cut or a twisted ankle on buried debris). | Trap | — |
| 5 | **The Supply Cache** | What the gnolls have specifically hoarded from travelers, kept apart from their own den — scavenged battlefield loot (weapons, a little coin, nothing magical) plus a minor useful item (a potion, a scroll), the "picked clean from someone unlucky" theme made concrete. Added 2026-09-02 — the original file's Treasure section, given its own room. | Treasure | — |
| 6 | **The Collapsed Cart** | A single scavenging gnoll, encountered apart from the rest of the pack — rounds out the pack's stated "roughly half a dozen" total without concentrating them. Added 2026-09-02. | Combat | — |
| 7 | **The Den Approach** | 1-2 more gnolls, posted at the entrance to the pack's actual lair. Added 2026-09-02. | Combat | — |
| 8 | **The Den** | The gnoll pack's actual lair, dug into the wagon line's collapsed underside — **the pack leader runs at roughly double a normal gnoll's HP** (a real sergeant moment, not just better gear), and the rest of the pack (2-3) is spread across the den's own uneven floor, not clustered — no single 15-20 ft area effect catches more than 2. | Combat | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02, before finalizing): Combat 4/8 (**50%, in band ✓**), Trap 1/8 (**12.5%, in band ✓**), Special (Treasure) 1/8 (**12.5%, in band ✓**), Structural (Entrance+Lore) 2/8 (**25%, above the 15-20% target** — accepted, an exposed surface battlefield genuinely needs less "hidden entrance" structure than a built dungeon, and the Officer's Cairn's lore beat is worth keeping as its own room rather than cut for the sake of the number).

- **Combat**: gnoll lookouts (Room 2), a lone scavenger (Room 6), den guards (Room 7), the pack leader + remaining pack (Room 8) — never all together
- **Hazard**: the Bone Field's wreckage (Room 4)
- **Lore**: the Officer's Cairn (Room 3) — which faction lost this fight originally
- **Treasure**: the Supply Cache (Room 5) — modest, real, with real texture rather than flat gold

## Connections

- `gazetteer.md` — Region IV, near Karsgate
- No faction ties — a pure scavenger ecology, deliberately unconnected to the war's current politics
