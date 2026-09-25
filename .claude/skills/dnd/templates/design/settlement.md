---
entity: settlement_<slug>
type: settlement
secrecy: public
phase: P3
status: skeleton
stamped: [scale, polity, ruler_at_birth]
covers: [district_<slug>, place_<slug>]
mirror: design/dm-only/settlements/settlement_<slug>.md
---

# <Settlement name> — <village / town / city / metropolis>

*Plan item 6.4, 13.3. Anchors are fixed at birth; the small-point budget is filled just in time and every filled small point becomes a permanent `place_` entity. A village is light: one sentence, one problem, one NPC.*

## Public

<Two or three sentences of atmosphere — what a rider sees, smells and hears arriving.>

- **Scale:** <scale> · **Population:** ~<n> · **Wealth:** <destitute / poor / modest / prosperous / wealthy> · **Law:** <1-5>, kept by <who>
- **Polity:** [[polity_<id>]] · **Ruler:** [[npc_<id>]] (<title>) · **Region:** [[region_<id>]]
- **Districts** *(city 5-8, town 2-3, village none)*: [[district_<id>]] <name> — <character in one line>; …
- **Economy:** sells <goods>; needs <goods>; price modifier ×<1.0> *(play-time changes live in the overlay)*
- **What the settlement fears:** <one line>
- **Local problem:** [[seed_<id>]] — <one line>

### Anchor locations *(fixed at birth)*
| Place | Kind | Owner | Services | Note |
|---|---|---|---|---|
| [[place_<id>]] <name> | temple | [[npc_<id>]] | <services> | <one line> |
| [[place_<id>]] <name> | inn | [[npc_<id>]] | rooms, meals, rumours | … |
| [[place_<id>]] <name> | market | — | <goods> | … |
| [[place_<id>]] <name> | seat | [[npc_<id>]] | audience, law | … |
| [[place_<id>]] <name> | guild_hall | [[npc_<id>]] | <faction services> | … |
| [[place_<id>]] <name> | signature | … | … | <the one place that could exist only here> |

### Small points *(budget <n>; filled by `detail`, permanent once named)*
| Place | District | Kind | Owner | Services | Filled |
|---|---|---|---|---|---|
| — | — | — | — | — | <day / session> |

### People here *(from the roster)*
- [[npc_<id>]] — <role>, usually at [[place_<id>]] (<schedule>)
- …

### Rumours on day 0
- <the day-0 news records that reach this settlement, one line each — from `news.json`>

## Discoverable

### Three truths
- **Obvious:** <what any visitor sees within an hour>
- **Discoverable:** <what a week or a friend reveals>

### Prices
| Item | Price | Note |
|---|---|---|
| <a local good> | <gp> | <from the economy line and the current modifier> |

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/settlements/settlement_<slug>.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: settlement_<slug>
type: settlement
secrecy: secret
phase: <PN>
stamped: [<the public stamps>, <the secret stamps>]
mirror_of: <this public file's path>
---
-->

## Secret

- **Secret truth:** <the third truth>
- **Who really holds power here:** <if not the ruler>
- <clue placements, hidden assets, the faction fracture that runs through this town>
