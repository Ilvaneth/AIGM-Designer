---
entity: none
type: cosmology
secrecy: public
phase: P2
stamped: []
covers: [god_<slug>, plane_<short>, era_<n>, event_<n>, event_deep_<n>]
mirror: design/dm-only/cosmology.md
---

# Cosmology — <campaign name>

*Plan item 25, build item 22d. The script rolled the cosmos on the foundation and named every part of it from the pool (`design/design.json#cosmos`, the frame `design/_staging/P2/doc_cosmology.frame.json`); this file makes it concrete and decides nothing. What a native believes goes under Public; what is true goes to the mirror.*

## Public

### Pantheon — <the rolled type, as a native would say it>; the gods <the rolled presence, in words>
*One block per god of the frame, in its order. Rank, domains, alignment, name and epithet are the frame's; the rest is yours.*

#### [[god_<slug>]] — <name>, "<epithet>"
- **Rank:** <greater / lesser / power> <· one of the great gods> · **Domains:** <the frame's> · **Alignment:** <the frame's> · **Symbol:** <yours>
- **As worshipped:** <what a native knows and does: rites, taboos, what the god is asked for>
- **Church:** <the rolled archetype or church line, made concrete; called "the <building word> of <god>" or by a common noun, never a new name (P4 names the factions)>
- **Disposition to mortals:** <one line>
- **Relations:** <each relation of the web, with [[god_<id>]]>
- **The pilgrim road** (only the pilgrim road's god): <its road, its holy place at the road's end, its pilgrims and what they carry>

### Where the dead go
- <the rolled afterlife, as the folk believe it; the judge or the land when the row names one; raising the dead works by the rules>

### Planes
- **Touched planes:** for each, [[plane_<short>]] <its pooled name> — what changed: <the deviation; a merged plane names its partner>; time there: <the rate> (`calendar.py plane enter --rate`); the way in: <…>; the cost: <…>; the keeper: <a god of the pantheon, or a creature>; <for a plane P1 named: what P1 gave it>
- **The other planes** exist as the SRD has them. **For the primer:** <one line: how *plane shift*, *banishment*, *gate*, *etherealness* and *astral projection* answer in this world>

### Magic
- **Where it comes from:** <the source> · **What limits it:** <the constraint> · **What casting looks like:** <the visibility>
- **Taboos:** <each rolled taboo, and who enforces it>
- **The regulator:** <who, by a common noun or the signature institution's name, and how strictly> · **Magic services** (identify, raise dead, remove curse): <who gives them, at what price>
- **Wild magic:** <as rolled>
- *A character's spells work as the 2014 rules write them; the lines above say how the world sees, rules and prices magic.*

### History
*The ages first, then the dated events as taught. Names, spans, years, ages, types and the seated events are the frame's.*

#### Ages
| Order | Age | Span | What the age is remembered for |
|---|---|---|---|
| 1 | [[era_<n>]] <name> | <the frame's span> | <one line> |

#### Events — as taught
| Year | Event | Age | Public account | Witnesses still alive |
|---|---|---|---|---|
| <year> | [[event_<n>]] <name> | [[era_<n>]] | <what everyone is taught> | <roles, for the seated story events only> |

#### Before the record
- [[event_deep_<n>]] <name> — <what the tales say>

### Calendar
- **The year:** twelve months of 28 days, a seven-day week.
- **Months:** <the frame's twelve names, in order> · **Days of the week:** <the frame's seven names>
- **The months as they are felt:** <month>: <temperature, sky, smell, the work of the month> · <month>: … *(one line per month: `calendar.seasons`)*
- **Moon(s):** <the pooled name(s), and what the moon does>
- **Below ground** (only under the underground era): <how the months are counted, as rolled>
- **Festivals:** <name> (<day month>) — <for [[god_<id>]], or the folk's>: <what people do>
- **Dated days:** <the empty month, the lawless day, the holy day: each with its date, as rolled>
- **Start date:** <day month year> = campaign day 0, <why that day: its anchor> (`calendar.py init` takes the frame's seed)

## Discoverable

- **The god story:** <on the god the frame gives it: what a scholar or a priest could find out>
- **Events — as they happened:** [[event_<n>]]: <for each event whose divergence is not `div_none`: what really happened (its `as_happened`)>

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/cosmology.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: none
type: cosmology
secrecy: secret
phase: P2
stamped: []
covers: [<a secret row of the frame, when there is one>]
mirror_of: design/cosmology.md
---
-->

## Secret

- **The gods the threat seats** (the threat's god, a god behind it; each only when rolled): [[god_<id>]] — its part, exactly as P1's chain and pin give it; its true name when it has one; a seated god's mirror god and what the two share
- **The villain's origin, as it happened:** [[event_<n>]]: <its true layer, from P1's chain>
- **The unnamed god's hidden name** (only when one is rolled)
- **The threat's own home plane** (epic, only when it is a plane of its own): <its secret row, told here>
- **A vulnerable time** (only when the weakness keeps one): <its date>
