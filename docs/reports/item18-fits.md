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

## 18d — the secret's choices (rows in `docs/reports/item18d-secret-SPOILER.md`)

1. **The keeping's count:** `docs/p1-build-18-rows.md` section 5 says 17 rows and lists 16 (the fourteen old twists left after "a PC is involved", the two rewritten among them, and the two new). Built with 16; is a row missing from the list?
2. **The hand's base** (stage 1's chain clue): the far end, end_b (end_a when the move struck end_b); a coming move starts there too.
3. **Stage 2's chain clue** is where the move struck (the layout's `break_at`), not with the stronger role.
4. **Stage 3's chain clue** is at the lair's where when it is a part of the layout (the remnant, the thin place, the heart, the key place, the far end; a place it built: along the spine); a lair on the move falls back to the goal's piece.
5. **The weakness's floors** are the coding tab's (the SPOILER file lists them): a thing at a site P6, a person P5, a name, a god, a time or a lore P2.
6. **The twist's ids** stay the archetypes' (`secret_*`), so an earlier birth's archetype and a new birth's twist share their id; the keeping keeps the old twists' ids (`twist_*`), its two new rows are `keep_*`. Rename them?
7. **The twists' texts** were moved onto the chain mechanically; read them in the SPOILER file: a rewrite by hand may read better.
8. **The trails' third element** carries the weakness by a suffix (`…_and_how_it_is_stopped`).
9. **clue_order:** the act reading stays only for a legacy birth without a ledger (item 23); every birth with a ledger reads stages.

## 18e — the writer's choices

1. **The spine sentence's grammar:** "<the target> <the verb's form>, by <the hand>; now <side a> and <side b> fight over <the prize>". The verbs' forms are singular ("was", "is being"), so a plural target reads "the march lords was enslaved"; the rows' forms would need a plural or the sentence a rewording. Accept, or reword the forms?
2. **W1, when a god is pinned:** the god family, the goal "carry out a patron's will", or the twist "a greater power stands behind the villain" (the greater power may be no god: a fiend lord or an elder mind). Otherwise the pin is the thin place when the palette holds one, else the remnant.
3. **The monsters were people** requires a hand of reshaped kinds: monstrosity, undead, lycanthrope, plant, aberration, construct. **It was done before** requires a ruin of the fallen kingdoms or the wars (14 rows).
4. **The card's secret line** shows the hidden facts' count (3 when the villain is known): a player who sees "3 of 4" learns the villain is known, which a known villain already is.
5. **The D&D line** ticks "breaks bend" when no rolled trope break carries `removes: true`; no row carries it today (18b bent the two).
6. **The mechanic's shapes** (summaries file) and their bands are the coding tab's; the owner reads them.

## 18e-2 — the verb × kind list, the short names, the hands' subjects

**The principle used:** a verb fits a kind when its phrase reads true for every row of that kind (a remnant's `remnant_kind`, the spine's `key_kind`, a role's `kind`); the old actions' `fits` were the start, narrowed where a phrase read false and widened only where it read true. The heart is a settlement and the thin place itself. Every phrase is active, the hand its subject: `{be}` takes the hand's number, `{target}` the target's short name. The role kinds: `group` (absent), `settlement` (a town, a realm or a state), `person` and `creature` (a role that is one being).

### List 1: the verbs and the kinds they strike

| Verb | Remnant kinds | Key-place kinds | Role kinds | Heart | Thin place |
|---|---|---|---|---|---|
| Carried off | object | — | group, settlement, person | yes | — |
| Seized | network, structure, city, body, wasteland, machine, object, source, rift | crossing, bridge, water, gate, descent, crossroad, network, landmark | — | yes | yes |
| Divided | — | — | group, settlement | yes | — |
| Corrupted | network, structure, city, body, wasteland, source, rift | crossing, water, gate, network, landmark | — | yes | — |
| Woke | body, machine, structure, object, network | bridge, gate, descent, landmark | — | — | — |
| Besieged / cut off | — | crossing, water, crossroad, network | — | yes | — |
| Opened | city, structure, body, source, rift | gate, descent, network | — | — | yes |
| Sealed | — | crossing, bridge, gate, descent, network | — | — | yes |
| Dragged into another plane | — | gate, descent, crossroad, network, landmark | — | yes | yes |
| Drove out | — | — | group, settlement, person, creature | yes | — |
| Burned | — | bridge, crossroad | — | yes | — |
| Raised in revolt | — | — | group, settlement | yes | — |
| Drowned | network, structure, city | gate, crossroad | — | yes | — |
| Killed | — | — | group, settlement, person, creature | yes | — |
| Poisoned | — | — | group, settlement, person, creature | yes | — |
| Cursed | — | crossing, bridge, water, gate, descent, crossroad, network, landmark | group, settlement, person, creature | yes | — |
| Plundered | structure, city, body, machine, wasteland | — | — | — | — |
| Summoned | — | crossing, bridge, water, gate, descent, crossroad, network, landmark | — | yes | yes |
| Spread a plague | — | — | group, settlement | yes | — |
| Replaced | — | — | group, settlement, person | yes | — |
| Possessed | — | — | group, settlement, person, creature | yes | — |
| Enslaved / took hostage | — | — | group, settlement, person, creature | — | — |
| Betrayed | — | — | group, settlement, person, creature | yes | — |

**Changed from the old fits:** carried off strikes an object remnant only (it carried off cities and wastes); seized also a wasteland; opened no object remnant and no landmark (a cape, a trunk); burned only a bridge or the crossroads among key places (a ford, a strait, a pass, tunnels do not burn); drowned no body or object remnant and no crossing, bridge or landmark (a strait does not drown); plundered no object or source remnant (one plunders a place) and also a wasteland; woke keeps its kinds through two phrases ("woke what sleeps in" a structure or a road network, "woke what sleeps beneath" a key place). The role kinds are new: divided, raised in revolt and a plague strike groups and settlements only; carried off and replaced no creature.

### List 2: the phrases (`foundation.yaml#action`, `phrases`; a `piece.kind` entry comes before its piece's)

| Verb | For | Past | Present | Imminent |
|---|---|---|---|---|
| Carried off | remnant | carried off {target} | {be} carrying off {target} | {be} about to carry off {target} |
| Carried off | role.person | carried off {target} | {be} trying to carry off {target} | {be} about to carry off {target} |
| Carried off | role | carried off the leader of {target} | {be} carrying off the leaders of {target} | {be} about to carry off the leader of {target} |
| Carried off | heart | carried off the ruler of {target} | {be} carrying off the leaders of {target} | {be} about to carry off the ruler of {target} |
| Seized | heart, key_place, remnant, thin_place | seized {target} | {be} seizing {target} | {be} about to seize {target} |
| Divided | role | split {target} in two | {be} splitting {target} in two | {be} about to split {target} in two |
| Divided | heart | divided {target} against itself | {be} dividing {target} against itself | {be} about to divide {target} against itself |
| Corrupted | remnant, key_place, heart | corrupted {target} | {be} corrupting {target} | {be} about to corrupt {target} |
| Woke | remnant.body, remnant.machine, remnant.object | woke {target} | {be} waking {target} | {be} about to wake {target} |
| Woke | remnant | woke what sleeps in {target} | {be} waking what sleeps in {target} | {be} about to wake what sleeps in {target} |
| Woke | key_place | woke what sleeps beneath {target} | {be} waking what sleeps beneath {target} | {be} about to wake what sleeps beneath {target} |
| Besieged / cut off | key_place | cut off {target} | {be} cutting off {target} | {be} about to cut off {target} |
| Besieged / cut off | heart | besieged {target} | {be} besieging {target} | {be} about to besiege {target} |
| Opened | remnant, key_place, thin_place | opened {target} | {be} opening {target} | {be} about to open {target} |
| Sealed | key_place, thin_place | sealed {target} | {be} sealing {target} | {be} about to seal {target} |
| Dragged into another plane | thin_place | dragged {target} into the plane beyond it | {be} dragging {target} into the plane beyond it | {be} about to drag {target} into the plane beyond it |
| Dragged into another plane | heart, key_place | dragged {target} into another plane | {be} dragging {target} into another plane | {be} about to drag {target} into another plane |
| Drove out | role | drove {target} out | {be} driving {target} out | {be} about to drive {target} out |
| Drove out | heart, role.settlement | drove the people out of {target} | {be} driving the people out of {target} | {be} about to drive the people out of {target} |
| Burned | key_place, heart | burned {target} | {be} burning {target} | {be} about to burn {target} |
| Raised in revolt | role, heart | raised {target} in revolt | {be} raising {target} in revolt | {be} about to raise {target} in revolt |
| Drowned | remnant, key_place, heart | drowned {target} | {be} drowning {target} | {be} about to drown {target} |
| Killed | role.person, role.creature | killed {target} | {be} hunting {target} | {be} about to kill {target} |
| Killed | role | killed the leader of {target} | {be} killing the leaders of {target} | {be} about to kill the leader of {target} |
| Killed | heart | killed the ruler of {target} | {be} killing the leaders of {target} | {be} about to kill the ruler of {target} |
| Poisoned | role.person, role.creature | poisoned {target} | {be} slowly poisoning {target} | {be} about to poison {target} |
| Poisoned | role | poisoned the leader of {target} | {be} poisoning the leaders of {target} | {be} about to poison the leader of {target} |
| Poisoned | heart | poisoned the wells of {target} | {be} poisoning the wells of {target} | {be} about to poison the wells of {target} |
| Cursed | heart, key_place, role | cursed {target} | {be} laying a curse on {target} | {be} about to curse {target} |
| Plundered | remnant | plundered {target} | {be} plundering {target} | {be} about to plunder {target} |
| Summoned | thin_place | summoned something terrible through {target} | {be} summoning something terrible through {target} | {be} about to summon something terrible through {target} |
| Summoned | heart, key_place | summoned something terrible into {target} | {be} summoning something terrible into {target} | {be} about to summon something terrible into {target} |
| Spread a plague | role | spread a plague among {target} | {be} spreading a plague among {target} | {be} about to loose a plague among {target} |
| Spread a plague | heart, role.settlement | spread a plague through {target} | {be} spreading a plague through {target} | {be} about to loose a plague on {target} |
| Replaced | role.person | replaced {target} with an impostor | {be} replacing {target} with an impostor | {be} about to replace {target} with an impostor |
| Replaced | role | replaced the leader of {target} with an impostor | {be} replacing the leaders of {target} with impostors | {be} about to replace the leader of {target} with an impostor |
| Replaced | heart | replaced the ruler of {target} with an impostor | {be} replacing the leaders of {target} with impostors | {be} about to replace the ruler of {target} with an impostor |
| Possessed | role.person, role.creature | possessed {target} | {be} taking hold of {target} | {be} about to possess {target} |
| Possessed | role | possessed the leader of {target} | {be} possessing the leaders of {target} | {be} about to possess the leader of {target} |
| Possessed | heart | possessed the ruler of {target} | {be} possessing the leaders of {target} | {be} about to possess the ruler of {target} |
| Enslaved / took hostage | role.settlement | enslaved the people of {target} | {be} enslaving the people of {target} | {be} about to enslave the people of {target} |
| Enslaved / took hostage | role.person | took {target} hostage | {be} holding {target} hostage | {be} about to take {target} hostage |
| Enslaved / took hostage | role | enslaved {target} | {be} enslaving {target} | {be} about to enslave {target} |
| Betrayed | role, heart | betrayed {target} | {be} betraying {target} | {be} about to betray {target} |

### List 3: the contest roles' short names and kinds (a `short` where the text runs past five words or leans on another phrase: it, its, the other)

| Role | Text | Short | Kind |
|---|---|---|---|
| two_heirs.a | the elder heir |  | person |
| two_heirs.b | the younger heir and their army | the younger heir | person |
| two_heirs.third | the regent who holds the crown and the treasury | the regent | person |
| two_heirs.fourth | a foreign kingdom that wants the throne | a foreign kingdom | settlement |
| one_harbour.a | the old harbour city |  | settlement |
| one_harbour.b | the newly founded rival city |  | settlement |
| one_harbour.third | the smugglers who use the harbour | the harbour smugglers |  |
| one_pasture.b | the lowland villages widening their fields | the lowland villages | settlement |
| one_pasture.third | the merchants selling horses and weapons to both sides | the horse and arms merchants |  |
| one_pasture.fourth | the keepers of the holy place in the middle of the pasture | the holy place's keepers |  |
| one_shrine.a | the old keepers of the holy place | the shrine's old keepers |  |
| one_shrine.b | the new faith that counts the same place as its own god's | the new faith |  |
| one_shrine.third | the town that lives off the pilgrims | the pilgrim town | settlement |
| one_shrine.fourth | the scholars who want to dig up the place | the scholars |  |
| two_banks.third | the weir masters who steer the water | the weir masters |  |
| two_banks.fourth | a people living in the river | the river folk |  |
| settlers_newcomers.a | the old owners of the land | the land's old owners |  |
| settlers_newcomers.third | the merchants who profit from both | the profiteering merchants |  |
| settlers_newcomers.fourth | someone organising the frightened people |  | person |
| old_order_reform.b | the young ruler or council that wants reform | the reformers |  |
| old_order_reform.third | the guilds that stand to gain from the reform | the guilds |  |
| old_order_reform.fourth | the soldiers of the old order | the old order's soldiers |  |
| old_gods_new_faith.third | the ruler forced to choose a side | the torn ruler | person |
| old_gods_new_faith.fourth | the mages who reject both faiths | the faithless mages |  |
| returners_stayers.a | the people driven out years ago and now returned | the returned exiles |  |
| returners_stayers.b | those who have settled on their lands | those who stayed |  |
| returners_stayers.third | a foreign power backing the return | a foreign power |  |
| returners_stayers.fourth | the mixed families married from both sides | the mixed families |  |
| occupier_resistance.a | the outside power holding the region | the occupiers |  |
| occupier_resistance.fourth | the smugglers who profit from both sides | the smugglers |  |
| capital_marches.a | the capital |  | settlement |
| capital_marches.b | the march lords and rangers | the march lords |  |
| capital_marches.third | the people on the other side of the border | the people across the border |  |
| capital_marches.fourth | the mercenary company hiring out soldiers to both sides | the mercenary company |  |
| lords_peasants.third | a religious leader who is thinking of arming the peasants | a firebrand preacher | person |
| mine_owners_miners.a | the family that holds the mine | the mine-owning family |  |
| mine_owners_miners.third | the outside merchants who buy the ore | the ore merchants |  |
| mine_owners_miners.fourth | a deep people angered by the mine's expansion | an angered deep people |  |
| casters_casterless.a | a bloodline or institution that holds magic as its monopoly | the magic-holding bloodline |  |
| casters_casterless.third | the illicit masters who teach magic in secret | the secret magic teachers |  |
| casters_casterless.fourth | a faith that wants to ban magic altogether | a magic-banning faith |  |
| sealed_remnant.a | those who want to open the remnant | the would-be openers |  |
| sealed_remnant.b | the keepers who want to keep it sealed | the keepers of the seal |  |
| sealed_remnant.third | the looters who take pieces out in secret | the secret looters |  |
| sealed_remnant.fourth | an outside power that gains if it is opened | an outside power |  |
| open_close_road.a | those who want to open the road to trade | the open-road traders |  |
| open_close_road.b | those who want to keep the stranger out | the road-closers |  |
| open_close_road.third | those who smuggle on the closed road | the road's smugglers |  |
| open_close_road.fourth | the country at the other end of the road | the country beyond the road | settlement |
| forbidden_lands.a | those who want to explore the forbidden lands | the would-be explorers |  |
| forbidden_lands.b | those who bar the way in | the wardens of the way |  |
| forbidden_lands.third | those who sell the things that come from there | the forbidden-goods traders |  |
| forbidden_lands.fourth | those who live in the forbidden lands | the forbidden lands' folk |  |
| share_keep_knowledge.a | those who want to open a craft or a magic to everyone | the sharers of the secret |  |
| share_keep_knowledge.b | the guild that keeps it secret | the secret-keeping guild |  |
| share_keep_knowledge.third | the spies who steal the knowledge and sell it | the knowledge thieves |  |
| share_keep_knowledge.fourth | a state that wants to turn the knowledge into a weapon | a warlike state | settlement |
| open_close_gate.a | those who want to keep the planar gate open | the gate-openers |  |
| open_close_gate.b | those who want to close it | the gate-closers |  |
| open_close_gate.third | those who come from the other plane | the visitors from beyond |  |
| open_close_gate.fourth | the villages beside the gate |  | settlement |
| treasure_race.third | the hunters of the native people | the native hunters |  |
| empty_throne.fourth | an outsider the people love |  | person |
| first_settlers.third | the native people of the land | the land's native people |  |
| monster_bounty.third | the villagers who protect the monster | the monster's protectors |  |
| monster_bounty.fourth | the alchemists who want the monster's parts | the alchemists |  |
| new_resource.a | the state |  | settlement |
| new_resource.third | the people living on top of the resource | the people on the resource |  |
| two_branches.a | the branch that counts the old collapse a punishment | the penitent branch |  |
| two_branches.b | the branch that counts it an opportunity | the ambitious branch |  |
| two_branches.third | the elders trying to unite the two branches | the uniting elders |  |
| two_branches.fourth | an outside power using one of the branches | an outside power |  |
| order_schism.b | the young branch that breaks away | the breakaway branch |  |
| order_schism.third | the steward who holds the order's treasury | the order's steward | person |
| order_schism.fourth | a rival faith that gains from the split | a rival faith |  |
| divided_city.a | one half of the city |  | settlement |
| divided_city.b | the other half |  | settlement |
| divided_city.third | the keepers of the gate that joins the two halves | the middle gate's keepers |  |
| divided_city.fourth | the young who want to reunite | the young reunifiers |  |
| sibling_rulers.a | the elder sibling who rules half of the country | the elder sibling | person |
| sibling_rulers.b | the younger sibling who rules the other half | the younger sibling | person |
| sibling_rulers.third | the old ruler who still lives, their mother or father | the old ruler | person |
| sibling_rulers.fourth | the neighbouring kingdom that has given a daughter in marriage to both siblings | the neighbouring kingdom | settlement |
| humans_giants.a | the kingdom spreading into the plain | the spreading kingdom | settlement |
| humans_giants.b | the giant clans defending their old rights in the mountains | the giant clans |  |
| humans_giants.third | those who trade with both sides | the go-between traders |  |
| humans_giants.fourth | the border villages that have learned to live with the giants | the border villages | settlement |
| humans_dragon.a | the league of towns |  | settlement |
| humans_dragon.b | the dragon that counts the region its home, and its servants | the dragon | creature |
| humans_dragon.third | a faith that bows to the dragon and is protected | the dragon's faithful |  |
| humans_fey.a | the villages clearing the forest |  | settlement |
| humans_fey.b | the fey owners of the forest | the forest fey |  |
| humans_fey.third | the druids who mediate between the two worlds | the mediating druids |  |
| humans_fey.fourth | a noble who bargains with the fey in secret | a fey-dealing noble | person |
| surface_deep.b | the people living in the deeps | the deep people |  |
| surface_deep.third | those who work as carriers between the two worlds | the carriers between worlds |  |
| surface_deep.fourth | those who fled the deep people and took refuge on the surface | the refugees from below |  |
| land_sea_folk.a | the coastal cities |  | settlement |
| land_sea_folk.third | the coastal families married from both peoples | the mixed coastal families |  |
| land_sea_folk.fourth | the merchants who want to dig up the sea bed | the sea-bed diggers |  |
| merchant_house_divides.third | the merchant house that gives weapons and money to both | the merchant house |  |
| merchant_house_divides.fourth | a fugitive who knows the truth | a fugitive witness | person |
| foreign_envoy.third | the envoy of a distant kingdom who seems a friend to both | the foreign envoy | person |
| foreign_envoy.fourth | a spy ring that senses the envoy's plan | a wary spy ring |  |
| war_fed_company.a | a country |  | settlement |
| war_fed_company.b | its neighbour | the neighbouring country | settlement |
| war_fed_company.third | the mercenary company that hires out to both sides and prolongs the war | the war-fed company |  |
| fallen_state_remnant.b | the other | the other new power |  |
| fallen_state_remnant.third | the old state's secret admirers, who want to found it again | the old state's admirers |  |
| fallen_state_remnant.fourth | someone who does not know they are the heir | an unknowing heir | person |
| shapeshifter.a | a village or family | one household |  |
| shapeshifter.b | the other | the other household |  |
| shapeshifter.third | a creature or fey in another guise that sets the two sides at each other | a creature in disguise | creature |
| shapeshifter.fourth | a hunter who suspects it | a suspicious hunter | person |
| living_dead.b | the undying lord and its risen subjects | the undying lord | creature |
| living_dead.third | the priests who can lay the dead | the dead-laying priests |  |
| living_dead.fourth | those who trade across the line | the traders across the line |  |
| fiend_pact.b | its rival | the rival house |  |
| fiend_pact.third | the fiend's envoy |  | creature |
| elemental_lord.b | the elemental lord whose domain they farm | the elemental lord | creature |
| elemental_lord.third | those who serve it | the elemental's servants |  |
| elemental_lord.fourth | the binders who would chain it again | the would-be binders |  |
| relic_pieces.a | a house that holds one piece | a house with one piece |  |
| relic_pieces.b | a house that holds another | a house with another |  |
| relic_pieces.third | the order sworn to keep the pieces apart | the sworn order |  |
| relic_pieces.fourth | a finder with no banner |  | person |
| prophecy.a | those who work to fulfil it | the prophecy's heralds |  |
| prophecy.b | those who work to prevent it | the prophecy's foes |  |
| prophecy.fourth | the one it names | the one the prophecy names | person |
| dark_lord.a | the dark lord's dominion |  | settlement |
| dark_lord.b | the last free realm |  | settlement |
| two_empires.a | one empire |  | settlement |
| two_empires.b | its rival | the rival empire | settlement |
| two_empires.third | the kingdom between them |  | settlement |
| two_empires.fourth | that kingdom's exiles | the border kingdom's exiles |  |
| coven.a | the villages bound by it | the bound villages | settlement |
| coven.b | those who would break it | the bargain-breakers |  |
| coven.fourth | the child that was promised |  | person |
| pirates.b | the league of harbour towns |  | settlement |
| slavers.b | the escaped and those who hide them | the escaped slaves |  |
| thieves_guild.a | the guild that runs the streets | the street guild |  |
| thieves_guild.b | the city's rulers, most of them on its payroll | the bought rulers |  |
| thieves_guild.fourth | the watch captain no one can buy | the honest watch captain | person |

### List 4: the places' short names (a `*_short` where the text runs past six words, offers an alternative with "or", lists with a comma, or names a structure as the heart)

| Row | Field | Text | Short |
|---|---|---|---|
| spine_great_rift | heart | the bridge that joins the two sides | the bridge-town over the rift |
| spine_great_rift | key_place | the bridge or the stair that goes down to the floor | the way down to the floor |
| spine_long_coast | key_place | the cape that splits the coast in two | the cape that splits the coast |
| spine_barren_corridor | heart | the caravanserai-city in the middle of the corridor | the caravanserai-city |
| spine_barren_corridor | key_place | the only water source on the road | the road's only water source |
| spine_lake_basin | key_place | the only pass out of the basin | the basin's only pass |
| spine_lone_mountain | key_place | the road up to the summit or the mouth that goes down into the mountain | the road into the mountain |
| spine_star_crater | heart | the stone at the centre of the crater | the town by the crater's stone |
| spine_star_crater | key_place | the only road down from the rim | the road down from the rim |
| spine_archipelago | key_place | the only safe strait that links the islands | the only safe strait |
| spine_valley_maze | key_place | the tunnels and passes that link the valleys | the tunnels between the valleys |
| spine_mesa_land | heart | the city on top of the largest mesa | the city on the great mesa |
| spine_mesa_land | key_place | the bridges and ropeways that link the mesas | the bridges between the mesas |
| spine_lake_chain | heart | the city on the strait that joins two lakes | the city on the strait |
| spine_three_depths | key_place | the great shaft or lift that links the layers | the great shaft |
| spine_terraces | key_place | the stairs and waterfalls between the terraces | the stairs between the terraces |
| spine_two_worlds | heart | the city where the two worlds overlap | the city between the worlds |
| spine_above_below_sea | heart | the coastal city or a reef | the coastal city |
| spine_peninsula | key_place | the neck, the only land crossing | the neck of the peninsula |
| spine_strait_two_continents | heart | the twin city on the two shores | the twin city |
| spine_long_wall | heart | the main gate of the wall | the town at the main gate |
| spine_long_wall | key_place | the gates | the gates of the wall |
| spine_climate_belt | heart | the city in the middle of the belt | the city at the belt's middle |
| spine_edge_of_civilisation | key_place | the border fortress or the last bridge | the border fortress |
| spine_floating_archipelago | key_place | the chains and wind roads that link the islands | the chains and wind roads |
| spine_void_ring | heart | the city that looks onto the void | the city above the void |
| spine_world_edge | heart | the city at the edge of the cliff | the city at the cliff's edge |
| spine_world_edge | key_place | the only road down from the edge | the road down from the edge |
| ruin_road_kingdom | remnant | the stone road network and the road forts | the stone roads and their forts |
| ruin_mage_war | remnant | the glass desert and the war towers | the glass desert |
| ruin_celestial_war | remnant | fallen war machines, scarred land | the fallen war machines |
| ruin_dead_god | remnant | a god's body the size of a mountain | the god's mountain-sized body |
| ruin_age_of_mages | remnant | a city that ran on magic and now stands still | the stilled city of magic |
| ruin_plague | remnant | quarantine cities, hospital-fortresses | the quarantine cities |
| ruin_fallen_star | remnant | the crater and the sky stone | the sky stone |
| ruin_dwarf_city | remnant | the deep city and its great gate | the deep city |
| ruin_devils_bargain | remnant | the gilded halls where the contracts were signed | the gilded contract halls |
| ruin_demon_gate | remnant | the closed gate and the scoured land around it | the closed demon gate |
| ruin_bound_elements | remnant | the binding works: mills, furnaces and channels with nothing left in them | the empty binding works |
| ruin_dark_lords_fall | remnant | the black fortress, his captains' strongholds and his weapon | the black fortress |
| ruin_empire | remnant | the imperial roads, forts and milestones that still cross every border | the imperial roads and forts |
| ruin_beast_blood | remnant | the clans' hill-forts and marked stones in the wilds | the clans' hill-forts |

The thin place is named "the thin place" (the palette's name carries no article).

### List 5: the contests' own prize names (`text.prize`, for a new or a seat prize; else "a new thing both want" or "the seat of <side a>")

| Contest | Prize | `text.prize` |
|---|---|---|
| contest_share_keep_knowledge | new | the guarded knowledge |
| contest_first_settlers | new | the new land |
| contest_new_resource | new | the new resource |
| contest_shapeshifter | seat | an inheritance |
| contest_relic_pieces | new | the pieces of the relic |
| contest_prophecy | new | the prophecy |
| contest_slavers | new | the people taken |

### List 6: the hands as subjects (`number`, `text.subject`)

| Hand | Name | Subject | Number |
|---|---|---|---|
| hand_villain_itself | the villain itself, openly | the villain itself | singular |
| hand_war_band | a war band, a part of its people | a war band | singular |
| hand_sea_raiders | sea raiders | sea raiders | plural |
| hand_cult | a cult | a cult | singular |
| hand_thieves_guild | a guild of thieves and assassins | a guild of thieves and assassins | singular |
| hand_traitor | a traitor inside | a traitor within | singular |
| hand_deceived_side | a side that does not know what it did | an unwitting faction | singular |
| hand_hired_company | a hired company | a hired company | singular |
| hand_foreign_army | a foreign army | a foreign army | singular |
| hand_dragon | a dragon and its servants | a dragon | singular |
| hand_risen_dead | the risen dead | the risen dead | plural |
| hand_ruin_power | the ruin's power, woken | the woken power of the ruin | singular |
| hand_fiends | fiends, summoned or bargained with | fiends | plural |
| hand_from_beyond | things from beyond | things from beyond | plural |
| hand_giants | giants | giants | plural |
| hand_monstrous_beast | a monstrous beast | a monstrous beast | singular |
| hand_fey_court | a fey court's emissaries | a fey court's emissaries | plural |
| hand_bound_elemental | a bound elemental | a bound elemental | singular |
| hand_werewolves | a cursed pack | a cursed pack | singular |
| hand_golem_army | a golem army | a golem army | singular |
| hand_hag_coven | a coven of hags | a coven of hags | singular |
| hand_brigands | brigands | brigands | plural |
| hand_slavers | slavers | slavers | plural |
| hand_zealous_order | a zealous order | a zealous order | singular |
| hand_rival_band | a rival band of adventurers | a rival band of adventurers | singular |
| hand_shapechangers | shapechangers wearing trusted faces | shapechangers | plural |
| hand_druid_circle | a corrupted druid circle and its blights | a corrupted druid circle | singular |

The villain itself is named by its family's public label (`villain_family.text.name`, singular), which the sentence shows only with a known visibility (the hand's requirement).

### Questions (18e-2)

1. **A fourth role kind, `settlement`** (27 roles: a city, villages, a realm, a state). With the hand as the subject the target is the object and no verb agrees with its number, so roles carry a kind, not a number; but "drove the capital out" and "enslaved the capital" read false, so a settlement takes the heart's phrase for drove out and a plague and "enslaved the people of". Accept the kind, or record a number as the specification says?
2. **Short names for places** (16 key places, 12 hearts, 14 remnants): the specification names short labels for roles only. Three hearts name a structure, not a settlement (the great rift's bridge, the crater's stone, the wall's main gate): their shorts make them towns ("the bridge-town over the rift").
3. **`text.prize` on seven contests** (six new prizes and the shapeshifter's seat): "a new thing both want" read as no hook.
4. **Seized is the most common verb** (494 of 3,000 births, 16.5 %; next carried off 293), since the narrowed verbs leave more remnants and key places to it. `row_wait: 3` keeps it from a run of births. Accept, or weigh it down?
5. **A patron's will** (the goal) still pins a god; only the greater power's kind was rolled, as item 5 says.

### The audit's corrections (2026-10-06)

1. **Remnant shorts for every ruin whose text is no clean object** in "<hand> <verb> <target>" (a description, an alternative, a plural with no article that reads oddly): 23 more, 37 of 53 now. The sixteen without a short read as they stand ("the prison-temple", "the treasure vaults", "the tomb-palaces of the undying kings").

| Ruin | Remnant | Short |
|---|---|---|
| ruin_water_kingdom | aqueducts and cisterns | the old aqueducts and cisterns |
| ruin_sorcerer_kings | palace-towers | the sorcerer kings' towers |
| ruin_city_states | walled, empty cities | the empty walled cities |
| ruin_steppe_union | palace-cities and stone monuments | the steppe palace-cities |
| ruin_giants_and_dragons | dragon bones and giant strongholds | the dragon bones |
| ruin_besieged_land | walls within walls and siege tunnels | the old siege walls |
| ruin_kin_war | twin fortresses on the two banks | the twin fortresses |
| ruin_gods_quarrel | gods' weapons stuck in the earth | the gods' fallen weapons |
| ruin_departed_god | empty temples and holy cities | the empty holy cities |
| ruin_golem_army | a waiting golem army | the dormant golem army |
| ruin_great_flood | cities under the water | the drowned cities |
| ruin_eruption | a city frozen by the lava | the lava-frozen city |
| ruin_mine_rush | an abandoned mining city | the abandoned mining city |
| ruin_endless_building | a giant building left half finished | the half-finished giant building |
| ruin_elven_withdrawal | empty tree-cities | the empty tree-cities |
| ruin_giants_land | buildings giant by human measure | the giants' buildings |
| ruin_age_of_dragons | lairs and hoards | the old dragon lairs |
| ruin_winged_mountains | peak cities reached only by flying | the peak cities |
| ruin_fallen_sky_city | the pieces of the city | the fallen sky city |
| ruin_broken_time | a city whose time is frozen | the time-frozen city |
| ruin_deep_minds | the sunken cities of the deep minds | the sunken cities |
| ruin_sleeper | the empty watch-posts over the sleeper | the sleeper's watch-posts |
| ruin_sleeping_realm | the sleeping realm and its dreamers | the sleeping realm |

2. **One rule for a power behind the villain:** the goal "a patron's will" rolls its patron's kind from `secrets.yaml#greater_power` as the twist does (once, when either names one; label `P1.secret_power`); the secret is pinned to a god only when the family is the god or that kind is a god.

**The answers:** Q1 the `settlement` kind stands (kind, not number); Q2 the place shorts and the structure hearts as towns stand; Q3 `text.prize` stands; Q4 seized at 16.5 % with `row_wait: 3` stands; Q5 answered by correction 2.
