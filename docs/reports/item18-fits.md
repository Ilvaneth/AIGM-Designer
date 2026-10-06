# Build item 18 — the fit lists

*Drafted by the coding tab from the principles of `docs/p1-build-18.md` and `docs/p1-build-18-rows.md`; audited by the development tab with each part. Where a principle did not decide a pair it is listed as a question, not chosen. No row of a secret table is named here.*

## 18a — the key place a key-place prize stands on (owner's correction at the 18a audit)

The spines' eight key-place kinds: crossing, bridge, water, gate, descent, crossroad, network, landmark.

| Contest | `key_kinds` | The owner's words |
|---|---|---|
| `contest_one_harbour` | crossing, landmark | a harbour, a strait or a cape |
| `contest_two_banks` | crossing, bridge | a ford, a weir or a bridge |
| `contest_mine_owners_miners` | descent, network | a mine, a shaft or a deep mouth |
| `contest_surface_deep` | descent, network | the same |
| `contest_pirates` | crossing | the sea lanes |
| `contest_open_close_road` | all eight | every key place is a road |

Readings confirmed by the development tab (2026-10-05): crossing, landmark, network and gate as listed; `water` stays off the two banks.

## 18b — list 1: the world states' joins (`trope-breaks.yaml`, `joins`)

A world state is drawn only where one of its joins holds; the first join that holds on a rolled piece is recorded, in the row's order; a join to the threat holds as a pending requirement while no threat is rolled (build item 18c honours it) and is written to dm-only alone (`dice-log.json#identity.world_states`); the public record says `{piece: hidden}`.

| World state | Joins, in order | What makes it hold today |
|---|---|---|
| rulers by lot | the heart's rule (and the main contest under it) | always |
| guilds rule, no lords | the same | always |
| magic is nobility | the same | always |
| dragons rule | the contest with a dragon; the threat is a dragon or works through a dragon hand | `contest_humans_dragon` rolled; else pending `{creature: dragon}` |
| a beast-person lords some lands | the disputed land is the beast-lord's; the beast-lord's folk is the contest's people side | a disputed-land prize rolled; else a seated `people_role` the break did not destroy |
| the moon trades | the thin place is the way to the moon; the hand trades with the moon or comes from it | `land_thin_place` in the palette; else pending `{hand: any}` |
| the gods among mortals | the threat is a god (standard and epic only); a side of the contest is a god's house | pending `{family: god}` above short; else `contest_one_shrine` or `contest_old_gods_new_faith` |
| the enemy won | the old war of the ruin is the war the enemy won; the enemy that won is the villain's own | a ruin of the `wars` family; else pending `{villain: any}` |

**Questions (18b, list 1):**
1. *A side at the gods' level*: read as the two faith contests (`contest_one_shrine`, `contest_old_gods_new_faith`). `contest_order_schism` (an order's split) and `contest_living_dead` (priests who lay the dead) were left out.
2. *A contest side* for the beast-lord: read as the main contest's seated people's role (eleven contests carry one). Any side of any contest would always hold.
3. *The ruin* for the enemy won: read as a ruin of the `wars` family. `fallen_kingdoms` (an empire fell) could also be "the war the enemy won".
4. *A hand* for the moon: any hand (the requirement is that the hand trades with the moon or comes from it, which 18c's hand rows do not say). Should a hand row carry a `moon` fit, or is the requirement only the writer's?
5. **The order of 18b and 18c.** Part 18b says the join to a family or a hand is "a requirement 18c's roll honours (a world state that names dragons weighs the dragon families and hands)"; part 18c's order of rolls (G4) puts the threat at step 4 and the trope breaks at step 9, after it. Built so both can stand: `design_identity.joins_of(..., threat=)` takes a rolled threat and 18c can judge the join directly there (then no requirement waits), or 18c can read the pending requirements to weigh its own rolls if the breaks come first. Which order does 18c use?
6. A pending join is public as `{piece: hidden}`: the fact that the world state waits on the threat is visible, not what it waits for. Should the public record omit the join altogether?

## 18b — list 2: the rows that touch the players (the P8 hook)

**The principle used:** a row touches the players when it changes what a player character may be, carry, do or know at creation, a rule of the game a character runs into (spellcasting, rest, death, Deception), or makes the core adventure a crime. Each carries `{phase: P8, must: "the player files and character creation state it"}`.

| Row | Why |
|---|---|
| only one class may bear arms | a character's weapons |
| magic is nobility | a caster's status by birth |
| the lineages' homes are inverted | lineage at creation |
| naming a god is forbidden | the cleric's and the paladin's god |
| divine magic is strongest on holy ground (bent) | the cleric's and the paladin's magic |
| going below ground is forbidden | the dungeon is a crime |
| entering the ruins is forbidden | the dungeon is a crime |
| one month a year magic does not work | spellcasting |
| iron is sacred and rare | weapons and armour |
| no one can lie outright | Deception |
| writing is sacred (bent) | the spellbook, the scroll, the map |
| there is no common tongue | languages at creation |
| casting is forbidden | the caster is an outlaw |
| the dead rise unless they are laid | a character's death |
| a broken oath curses the breaker | the paladin's oath, every character's word |

**Questions (18b, list 2), left without the hook:** maps are forbidden (a character's map and cartographer's tools); going out at night is forbidden; crossing the border is forbidden (laws the party may break, not a rule of the game); magic is bought and sold (the economy of magic items); the chosen are many (a character may be one: a P9 matter); dreams are a place (a long rest); the gods live among mortals (a cleric may meet its god).

## 18b — the audit's answers (the development tab, 2026-10-05)

- Q1, Q2: the readings stand. Q3: the enemy won also joins a ruin of the `fallen_kingdoms` family. Q4: in 18c the trading hands (the hired company, sea raiders and pirates, slavers, the guild of thieves and assassins) carry a moon fit, and things from beyond come from it. Q5: G4's order holds; the threat is rolled before the trope breaks and a join to it is judged on the rolled threat. Q6: a join to the threat leaves the public record entirely.
- List 2: maps are forbidden, dreams are a place and the gods among mortals take the hook; night, the border, magic sold and the chosen are many (P9's) do not.

## 18c-1 — the threat's fit lists

The villain tables are secret: the threat's fit lists (family → creatures and reskin bases, the family weights, weakness → families, lair form → families, the lair's where, the goal's join) and their seven questions are in `docs/reports/item18c-fits-SPOILER.md`. The shape rows read for Part 18c section 5 are in `docs/reports/item18c-shapes-SPOILER.md`.

## 18c-2 — the move's fit lists (public tables)

**List 1: the hand → verb fit** (a verb's `by`; absent: every hand). An intrigue move (replaced, possessed, betrayed, divided) belongs to a hand that can scheme; a few verbs to the hands that can do the thing.

- `act_split` (Divided): villain_itself, traitor, cult, thieves_guild, deceived_side, zealous_order, fey_court, shapechangers, fiends, hag_coven
- `act_corrupted` (Corrupted): villain_itself, cult, fiends, from_beyond, druid_circle, hag_coven, risen_dead, ruin_power, dragon, fey_court, werewolves
- `act_awakened` (Woke): villain_itself, cult, ruin_power, from_beyond, fiends, druid_circle, bound_elemental, risen_dead, hag_coven, zealous_order, rival_band
- `act_merged_with_plane` (Dragged into another plane): villain_itself, cult, fiends, from_beyond, fey_court, ruin_power, bound_elemental, hag_coven
- `act_rose` (Raised in revolt): villain_itself, cult, traitor, deceived_side, zealous_order, thieves_guild, fiends, shapechangers, risen_dead, druid_circle
- `act_sank` (Drowned): villain_itself, sea_raiders, bound_elemental, monstrous_beast, ruin_power, from_beyond, dragon, giants, fiends, cult, druid_circle
- `act_poisoned` (Poisoned): villain_itself, cult, thieves_guild, traitor, druid_circle, dragon, hag_coven, fiends, shapechangers
- `act_cursed` (Cursed): villain_itself, cult, hag_coven, fiends, fey_court, druid_circle, risen_dead, ruin_power, werewolves, from_beyond
- `act_summoned` (Summoned): villain_itself, cult, fiends, from_beyond, hag_coven, druid_circle, ruin_power, bound_elemental, fey_court
- `act_plague` (Spread a plague): villain_itself, risen_dead, cult, druid_circle, fiends, from_beyond, hag_coven, ruin_power, werewolves
- `act_replaced` (Replaced): villain_itself, shapechangers, fey_court, hag_coven, fiends, cult, traitor
- `act_possessed` (Possessed): villain_itself, fiends, from_beyond, cult
- `act_enslaved` (Enslaved / took hostage): villain_itself, slavers, from_beyond, fiends, giants, war_band, dragon, foreign_army, sea_raiders, fey_court, hag_coven
- `act_betrayed` (Betrayed): villain_itself, traitor, deceived_side, cult, thieves_guild, hired_company, zealous_order, rival_band, shapechangers
- every other verb: every hand.

**List 2: the goal's piece → the targets on the way** (with the guards of the 18c-2 answer):

- heart: heart, role, key_place, remnant, thin_place
- key_place: key_place, role
- disputed_land: role, key_place
- remnant: remnant, key_place, role, thin_place
- thin_place: thin_place, remnant, key_place, role
- role: role, heart
- new: remnant, thin_place, key_place, role

A goal that joins through the move: every joinable piece (the prize's piece, a contest role, a piece standing on a side's part: the main contest's seats, and the key place, which borders the ends); the ones on the way to the goal weigh x3; the thin place weighs x3 more wherever it is allowed.

**List 3: the hand's requirements:** the villain itself only with a known visibility; sea raiders on a coast or an island; the golem army at magic medium or high; the ruin's power with one of sixteen ruins whose remnant can wake: ruin_dead_god, ruin_imprisoned_god, ruin_failed_apotheosis, ruin_golem_army, ruin_bound_elements, ruin_sundered_relic, ruin_dried_source, ruin_sleeper, ruin_deep_minds, ruin_planar_rift, ruin_demon_gate, ruin_devils_bargain, ruin_sleeping_realm, ruin_failed_experiment, ruin_great_curse, ruin_kingdom_of_the_dead.

**List 4: the start** (finding D3): the part where the move struck when it is an end, the key place or a place along the spine; else end_a (the nearest end to the heart); a coming move at end_b (the hand's base).

**Questions (18c-2):**
1. The hand's public creature families: the cult carries `served` (what it serves, left for P6 to read: it is not the villain's type, which would leak it); the ruin's power carries `ruin` (P6 reads the ruin). Right?
2. The new verbs' forms (killed, poisoned, cursed, plundered, summoned, plague, replaced, possessed, enslaved, betrayed) and the rewritten ones are the coding tab's wording: please read them in foundation.yaml#action.
3. `act_vanished` (carried off) keeps `destroys: [heart, role]` from the old "vanished": does carrying off a leader destroy the role?
