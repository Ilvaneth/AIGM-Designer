---
entity: era_<current era slug>
type: era
secrecy: public
phase: P2
stamped: [pantheon_type, months, start_date]
mirror: design/dm-only/cosmology.md
---

# Cosmology — <campaign name>

*Plan item 5. Pantheon, planes, magic, history, calendar. The gods carry the premise's question: one god embodies the villain's answer, one the world's. What common folk believe goes under Public; what is true goes to the mirror.*

## Public

### Pantheon — `<pantheon type>`
*One block per god. Rank ∈ greater / lesser / power (saints, archfey, demon lords and primordials are the same entity class). Domains come from the SRD cleric list so clerics and paladins work mechanically.*

#### [[god_<slug>]] — <Name>, "<epithet>"
- **Rank:** <greater / lesser / power> · **Domains:** <SRD domains> · **Alignment:** <align> · **Symbol:** <symbol>
- **As worshipped:** <what a native knows and does — rites, taboos, what the god is asked for>
- **Church / cult:** [[faction_<id>]] or <institution name> *(the `church` field is filled for every god; separate church factions exist only in `epic`)*
- **Disposition to mortals:** <one line>
- **Relations:** <rivalry / alliance / silence with [[god_<id>]]>

#### [[god_<slug>]] — …

### Planes
- **Baseline:** the SRD cosmology, with these changes: <renamed / altered / removed by the trope break>
- **Touched planes** *(0-1 / 1-2 / 3+ by scale)*: [[plane_<id>]] — way in: <how>; cost: <what>; site: [[site_<id>]]; time rate: <ratio> (`calendar.py plane enter --rate`)
- **Untouched planes** still exist for spells; **rule for the primer:** <how Banishment / Plane Shift behave in this world>

### Magic
- **Availability:** <from the dial> · **Source:** <arcane / divine / wild / pact / other> · **Visibility:** <what casting looks like to onlookers>
- **Constraints and cost:** <what limits magic>
- **Taboos:** <what is forbidden, by whom>
- **Regulator:** [[faction_<id>]] — <how licences, punishments and exceptions work>
- **Signature phenomenon:** **<name from the premise>** — <the rule as a native understands it>
- **Wild magic:** <yes / no, rolled> — <one line if yes>

### History
*Ages first, then dated events. Each event is an `event_` entity with two layers: "as taught" here, "as it happened" in the mirror when they differ.*

#### Ages
| Order | Age | Span | What the age is remembered for |
|---|---|---|---|
| 1 | [[era_<id>]] <name> | <from – to> | <one line> |

#### Events — as taught
| Year / day | Event | Public account | Witnesses still alive |
|---|---|---|---|
| <year> | [[event_<id>]] <name> | <what everyone is taught> | [[npc_<id>]], … |
*(8-12 events in the last 200 years, plus 3-5 deep-past events; the villain's origin and the big secret are pinned here, in the mirror)*

### Calendar
- **Months (30 days each):** <name>, <name>, … *(from the naming language)*
- **Day names:** <seven or fewer>
- **Seasons and their felt tone, per month:** <month>: <temperature, sky, smell> · <month>: … *(the "felt season" rule reads this)*
- **Moon(s):** <name, cycle, phase on day 0>
- **Festivals:** <name> (<month, day>) — for [[god_<id>]]: <what people do>
- **Start date:** <day month year> = campaign day 0 (`calendar.py init --date "<…>" --months "<…>" --day-names "<…>"`)

## Discoverable

- <what a scholar, priest or elder could tell: the ages' true lengths, a god's older name, an event's second version that is not yet the secret>

## Secret
*(written to `design/dm-only/cosmology.md`)*

- **The god behind the villain's answer:** [[god_<id>]] — <how>
- **The silenced / erased / lying god, if any:** <the truth>
- **Events — as they happened:** [[event_<id>]]: <the true account>; …
- **Where the big secret hides in this layer:** <one paragraph tying clue placements to gods, events or planes>
