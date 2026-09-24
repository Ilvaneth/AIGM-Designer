---
entity: region_<slug>
type: region
secrecy: public
phase: P3
stamped: [danger_tier, polity]
mirror: design/dm-only/regions/region_<slug>.md
---

# <Region name> — region

*Plan item 6.2, 6.5, SKILL-travel. Fixed danger tier set by the fiction, never by party level. The travel table is generated at birth; its Early / Late tier is keyed to the threat escalation stage.*

## Public

- **Identity in one line:** <the sentence that makes this region unlike every other — no reskins>
- **Biome / climate:** <biome>, <climate> · **Polity:** [[polity_<id>]] · **Danger tier:** **T<n>** (CR <band>)
- **Factions present:** [[faction_<id>]] (<how strongly>), …
- **Settlements:** [[settlement_<id>]] (hub), [[settlement_<id>]], …
- **Landmarks (2-4):** <name> — <one line>; …
- **Sites:** [[site_<id>]] (T<n>), … *(the over-tier ones are what "nobody goes there" is about)*
- **What everyone says about the dangerous places:** <the public telegraphs, as a native repeats them>

### Travel table — <region>, from <hub settlement>
*Six categories on a d12 (weights 4 / 1 / 1 / 1 / 3 / 2). `[KANCA]` marks a result that opens a hook. Each subtable has six rows and at least one result that could happen only in this region. Mounted travel by default.*

#### Category (d12)
| d12 | Category |
|---|---|
| 1-4 | Quiet/Texture |
| 5 | Social |
| 6 | Environmental |
| 7 | Combat |
| 8-10 | Discovery |
| 11-12 | Faction/Political |

#### Early tier (threat stage 1-2)
##### Quiet/Texture (d6)
| d6 | Result |
|---|---|
| 1 | <sensory line unique to this biome> |
| 2 | … |
| 3 | … |
| 4 | … |
| 5 | … |
| 6 | … |

##### Social (d6)
| d6 | Result |
|---|---|
| 1 | <a traveller with a reason — name from the roster or a minor stub> |
| … | … |

##### Environmental (d6)
| d6 | Result |
|---|---|
| 1 | <hazard with a DC and a cost> |
| … | … |

##### Combat (d6)
| d6 | Result |
|---|---|
| 1 | <SRD creatures from `monster-ecology.yaml` for this biome, at this tier, with a reason to be here> |
| … | … |

##### Discovery (d6)
| d6 | Result |
|---|---|
| 1 | <a place, a body, a sign — consults the news feed first (SKILL-travel rule 5)> `[KANCA]` |
| … | … |

##### Faction/Political (d6)
| d6 | Result |
|---|---|
| 1 | <a faction's presence on the road — consults the news feed first (SKILL-travel rule 1)> `[KANCA]` |
| … | … |

#### Late tier (threat stage 3+)
*Only the subtables that change: usually Combat and Faction/Political, harder and more frequent as the world darkens.*

##### Combat (d6)
| d6 | Result |
|---|---|
| 1 | … |

##### Faction/Political (d6)
| d6 | Result |
|---|---|
| 1 | … |

## Discoverable

- <what a local guide, a map or a season in the region teaches: safe passages, the real reason behind a landmark, which faction actually holds the road>

## Secret
*(written to `design/dm-only/regions/region_<slug>.md`)*

- <what the region hides: a clue placement, an over-tier site's true occupant, a faction's hidden asset>
