# The Weeping Wood

**Region**: II. The Thornlands
**Level range**: 3-6
**Site type**: Full forest site, built to `.claude/rules/dungeon-design.md`'s standard (areas instead of rooms — a forest doesn't have walls, but the same density principles apply)
**Location class**: Dungeon
**Dungeon Type**: **Lair** (per Phase 0's DMG taxonomy, added 2026-09-02) — a natural space, unbuilt, currently held by ettercaps/giant spiders encroaching on Sylvenna's own long-unbuilt domain. Neither party constructed anything here.
**Payoff type**: **Strategic-info** — explicit in this file's own Phase 4 ("nothing hoarded in the traditional sense... Sylvenna's actual value is information, not gold"). Per the Payoff-type rule, this site's exploration/lore areas (6, 7, 8) are never optional connective tissue — Sylvenna's bargain *is* the reward.

**⚠ Two-character party check** (`two-player-scaling.md`): 3 ettercaps fought together is 1,350 raw XP → adjusted **3,375 XP**, Deadly for a level-9 party, let alone this site's stated range. **Never fight all 3 at once.** The Ettercap Nest (Area 4) holds at most 2 encountered together; the third should be elsewhere in the wood, encountered separately or not at all. Giant spiders (Area 5), fought in a group of 3-4, land around 2,000 adjusted — Hard-to-Deadly at level 5, acceptable for the top of this site's range but still worth telegraphing before the fight starts.

---

## Phase 1 — Concept & ecology

**What it is**: Old-growth forest between Thornwick and Harrowgate, older than either settlement, predating the current dynasty entirely. Locals give it a wide berth out of habit more than any specific fear.

**Who holds it**: A **dryad, Sylvenna** (`npcs/sylvenna.md`), tends the wood's healthy heart and has for longer than anyone can verify — she remembers the ash-kings personally, making her the oldest living witness to that era anywhere in the region. In recent years, **ettercaps** and **giant spiders** have spread from the wood's damp northern edge, webbing over parts of her domain faster than she alone can push back — she has not lost the wood, but she is losing ground.

## Phase 2 — Map (non-linear)

Three natural entrances (the Thornwick road edge, the Harrowgate road edge, and a deer trail from the north that the spiders themselves use), a rough loop around the wood's central clearing, and real verticality in the canopy itself — giant spiders move overhead as readily as on the ground, and a party that ignores the canopy is only fighting half the encounter space.

## Phase 3 — Area by area

| # | Area | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Thornwick Verge** | Entrance from the south — old, half-swallowed boundary stones mark where the wood was once deliberately kept back | Entrance | — |
| 2 | **The Harrowgate Verge** | Entrance from the east — more recently used, cart-tracks suggest woodcutters test this edge occasionally and don't come back twice | Entrance | — |
| 3 | **The Webbed Reach** | Northern entrance, thick with ettercap silk — the spiders' clearest territory, and the most obviously dangerous approach. A real encounter, not just atmosphere: 1-2 giant spiders patrol here (the "optional additional spider encounters" Phase 4 already named, made a firm part of the area rather than a maybe, 2026-09-02). | Combat | ✅ RESOLVED (session 16, day 69) — 2 Giant Spiders, full surprise on the party (Stealth 24), both killed by round 3, 25 total damage taken |
| 4 | **The Ettercap Nest** | 2 ettercaps (never 3 — see scaling note above), webbed high in the canopy — an ambush-first fight if the party doesn't spot the webs | Combat | ✅ RESOLVED (session 16, day 69) — full surprise on the party (Stealth 24), both killed by round 4. A real scare: Ilvaneth dropped to 1 HP, Invisibility'd and retreated, Kriv finished the survivor with a crit |
| 5 | **The Spider Hollow** | A sunken depression thick with giant spider webbing — several giant spiders, a real vertical fight | Combat | ✅ RESOLVED (session 17, day 69) — 4 Giant Spiders (2 floor, 2 web ceiling), no surprise either side. Ilvaneth's Fireball killed the ceiling pair in one blast; Kriv's Extra Attack + Goading Attack + GWM bonus + Action Surge killed both floor spiders same round. Zero rounds beyond Round 1, 4 poison damage taken total. See `party/session-17/session-17-combat-weeping-wood-area5-spider-hollow.md` |
| 6 | **The Old Boundary Stones** | Worn carvings, pre-dynastic — a DC check reveals they mark the wood's edge from an era before the current kingdom existed at all, environmental storytelling rather than a fight | Lore | — |
| 7 | **The Weeping Spring** | A small, clean spring at the wood's heart — safe ground, and where Sylvenna can usually be found if approached respectfully. Functions as this site's Sanctuary — a resource-drained party can genuinely rest here, Sylvenna's own presence keeping the area clear (2026-09-02, per the DMG content-ratio fix — this was implicit, now explicit). | Sanctuary | — |
| 8 | **The Dryad's Grove** | The wood's healthiest, oldest section — Sylvenna's true home, visibly healthier than anywhere else in the wood | Lore | — |
| 9 | **The Choked Grove** | Once as healthy as Area 8, now half-webbed — physical proof of what Sylvenna is losing, and the clearest argument for why she'd bargain. The actual bargain fight: clearing this area of its remaining ettercaps/spiders (2-3, the wood's own overflow) is what earns Sylvenna's answer. | Combat | ✅ RESOLVED (session 16, day 69) — Ilvaneth raised 2 Skeleton Archer thralls and torched the webbing with Fire Bolt, flushing 2 Giant Spiders into the open; both killed in round 1 via Kriv's Action Surge. **Sylvenna's bargain fulfilled.** |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02, re-verified after the same-day Payoff-type-aware band refinement): against this site's own **Strategic-info** bands (Combat 40-50%, Trap 10-15%, Special 10-15%, Structural 20-30%) — Combat 4/9 (**44.4%, in band ✓**), Trap 0/9 (**0%, below target**), Special 1/9 (**11.1%, in band ✓**), Structural 4/9 (**44.4%, above target**). Combat needed no correction once checked against the right band — the flat Treasure-heavy target this was first measured against was simply the wrong comparison for a Strategic-info site. Trap/Structural remain genuine deviations, **accepted as deliberate, DM decision 2026-09-02** — this site's identity is Sylvenna's bargain-not-fight design (the same principle already proven at `the-widows-hollow.md`), and forcing trap content or trimming lore to hit the bands exactly would work against that.

- **Combat**: ettercaps (Area 4), giant spiders (Area 5), optional additional spider encounters scattered through Areas 3/9 for a party that lingers
- **Exploration/lore**: the boundary stones (Area 6) — real, checkable pre-dynastic history
- **Social/bargain**: Sylvenna (Areas 7-8) — she'll trade genuine ash-king knowledge for help clearing the spiders from the Choked Grove (Area 9), the same bargain-not-fight design already proven at `the-widows-hollow.md`
- **Treasure**: nothing hoarded in the traditional sense — Sylvenna's actual value is information, not gold. **Revised session 17, 2026-09-04, direct DM feedback**: "modest, grim, not a windfall" undersold what 4 real fights across the whole wood should pay out — a Strategic-info Payoff type means the *big* reward is lore, not that combat effort goes uncompensated. A thorough search of Area 5 (Investigation 27, advantage) found a long-dead scout/relic-hunter's cocooned remains, fallen from the ceiling after the Fireball burned through the silk: 220 gp, sellable travel gear, and a Boots of Elvenkind. **Standing note for future Strategic-info sites**: give real, if modest, treasure proportional to combat effort even when the site's main payoff is lore — a zero-treasure combat-heavy site reads as a design gap at the table, not a deliberate restraint. See `bug-log.md`, `content-gap`.

## Sylvenna's actual price

She doesn't want payment, in the transactional sense established for the campaign's other NPCs — but per `.claude/rules/npc-consistency.md`, her willingness to talk still traces to her own self-interest: **clear the Choked Grove (Area 9) of ettercaps and spiders, and she'll answer honestly about what she remembers of the ash-kings** — genuine lore, not a fragment location handed over for free.

## Connections

- `gazetteer.md` — Region II, between Thornwick and Harrowgate
- `npcs/sylvenna.md` — full NPC file, Current knowledge & Decision logic
- No faction ties — Sylvenna predates all three factions and has no stake in the succession war
