# Build item 16b — the technical fields the coding tab wrote

*Written by the coding tab, 2026-10-04, for the audit (`docs/p1-build-16.md`, Part 16b). The ids, families, labels, statements and roles are the approved ones; everything below is the coding tab's, in the pattern of each family's existing rows.*

## Ruin sources

| id | remnant_kind | sites | olgu_families | requires / hooks |
|---|---|---|---|---|
| `ruin_kingdom_of_the_dead` | city | site_dungeon_tomb, site_dungeon_planned, site_stronghold | body_blood, time | — |
| `ruin_devils_bargain` | structure | site_planar, site_stronghold, site_urban | word_sign, body_blood | the P2 plane hook |
| `ruin_demon_gate` | rift | site_planar, site_wilderness, site_dungeon_lair | nature_creatures, matter | the P2 plane hook |
| `ruin_deep_minds` | city | site_dungeon_natural, site_dungeon_planned, site_dungeon_lair | body_blood, word_sign | requires {"any_of": ["land_coast", "land_island", "land_lake", "land_underground"]} |
| `ruin_bound_elements` | machine | site_dungeon_planned, site_urban, site_wilderness | matter, nature_creatures | — |
| `ruin_sundered_relic` | object | site_dungeon_planned, site_stronghold, site_dungeon_ruin | matter, magic_behaviour | — |
| `ruin_dark_lords_fall` | structure | site_stronghold, site_dungeon_planned, site_dungeon_ruin | body_blood, matter | — |
| `ruin_sleeper` | structure | site_dungeon_planned, site_stronghold, site_dungeon_natural | time, place_path | — |
| `ruin_empire` | network | site_stronghold, site_urban, site_dungeon_ruin | word_sign, place_path | — |
| `ruin_great_curse` | wasteland | site_wilderness, site_dungeon_ruin, site_urban | nature_creatures, body_blood | — |
| `ruin_beast_blood` | structure | site_wilderness, site_dungeon_lair, site_stronghold | body_blood, nature_creatures | — |
| `ruin_sleeping_realm` | city | site_planar, site_urban, site_dungeon_planned | time, place_path | the P2 plane hook |
| `ruin_fallen_order` | structure | site_stronghold, site_dungeon_planned, site_dungeon_ruin | word_sign, body_blood | — |

Each also carries `text` (`name`, `what`, `remnant`, `sites`, `strangeness`), written from its statement:

- `ruin_kingdom_of_the_dead` — what: the kings who would not die ruled on as the undead until the living rose and broke them · remnant: the tomb-palaces of the undying kings · sites: tomb-palaces, sealed throne halls, the roads of the royal dead · strangeness: not all of the undying court was destroyed, and it still keeps its ranks
- `ruin_devils_bargain` — what: a kingdom bought its golden age from the Hells, and the devils took what was owed when the bargain came due · remnant: the gilded halls where the contracts were signed · sites: contract vaults, gilded palaces gone to ruin, the devils' embassies · strangeness: its contracts still bind whoever speaks their terms
- `ruin_demon_gate` — what: a gate to the Abyss stood open for a generation and the land around it was scoured · remnant: the closed gate and the scoured land around it · sites: the gate's ruin, the scoured waste, the lairs of what came through · strangeness: what came through was never all hunted down, and the land near the gate still warps what lives on it
- `ruin_deep_minds` — what: before the peoples, aberrant minds ruled from sunken cities and kept thralls, until their dominion broke · remnant: the sunken cities of the deep minds · sites: drowned cities, thrall pens, the chambers where the minds thought together · strangeness: the cities still think, and those who stay too long hear them
- `ruin_bound_elements` — what: a people chained elementals to turn their mills and warm their cities, and the bindings failed all at once · remnant: the binding works: mills, furnaces and channels with nothing left in them · sites: binding halls, stopped mills, the places where an elemental broke free · strangeness: some elementals never left, and the elements there still answer a binder's word
- `ruin_sundered_relic` — what: an artifact that held the land together was broken on purpose, and its pieces were carried apart and hidden · remnant: the pieces of the sundered relic · sites: the hiding places of the pieces, the hall where it was broken · strangeness: each piece still does a part of what the whole did
- `ruin_dark_lords_fall` — what: a conqueror ruled from a black fortress until an alliance threw him down · remnant: the black fortress, his captains' strongholds and his weapon · sites: the black fortress, the captains' strongholds, the field of the last alliance · strangeness: his weapon was never unmade, and what served him still knows its master's sign
- `ruin_sleeper` — what: something older than the gods was bound asleep, and the people that kept the watch is gone · remnant: the empty watch-posts over the sleeper · sites: watch-posts, the binding vault, the roads the watch walked · strangeness: the sleeper dreams, and near it the land does what it dreams
- `ruin_empire` — what: one throne held every land, and when it fell each province kept a piece of its law, its roads and its legions · remnant: the imperial roads, forts and milestones that still cross every border · sites: legion forts, provincial capitals, the fallen throne-city · strangeness: the empire's law still holds on its roads, whoever rules beside them
- `ruin_great_curse` — what: a wronged power cursed the land with its dying breath; crops, births and luck all turned, and the realm emptied · remnant: the emptied realm under the curse · sites: abandoned farms and towns, the place where the curse was spoken · strangeness: the curse still chooses: some who enter are spared and none can say why
- `ruin_beast_blood` — what: clans that took the shapes of beasts held the wilds until they were hunted out · remnant: the clans' hill-forts and marked stones in the wilds · sites: hill-forts, marked stones, the dens of those who never changed back · strangeness: their blood still surfaces: a child of any family may take the shape
- `ruin_sleeping_realm` — what: a whole realm fell into one dream and did not wake · remnant: the sleeping realm and its dreamers · sites: the sleeping city, the dream that can be entered, the border where waking ends · strangeness: the dream is still there, and whoever sleeps near it walks in it
- `ruin_fallen_order` — what: a sworn order held the frontier until it was betrayed and broken · remnant: the order's empty commanderies · sites: commanderies, chapter vaults, the field where it was broken · strangeness: its oaths were never released, and they still bind whoever takes up its arms

## Contests

| id | prize | hints (a, b, third, fourth) | seats / requires / other | escalation |
|---|---|---|---|---|
| `contest_living_dead` | heart | state, none, religious, trade | — | the unburied walk → the border forts fall → the living city besieged |
| `contest_fiend_pact` | lifeline | state, state, none, martial | third_is_rumour | favours that come too easily → the rival's ruin → the pact comes due |
| `contest_elemental_lord` | lifeline | state, none, religious, scholarly | — | offerings withheld → flood and fire → the binding attempted |
| `contest_relic_pieces` | new | state, state, religious, none | prize_with {"ruin_sundered_relic": "remnant"} | a piece changes hands → open raids for the pieces → two pieces joined |
| `contest_prophecy` | new | religious, state, scholarly, none | — | signs argued over → the named one hunted → the foretold day |
| `contest_dark_lord` | heart | state, state, trade, resistance | — | tribute demanded → the border overrun → the march on the last free city |
| `contest_two_empires` | heart | none, none, state, resistance | — | envoys and gifts → garrisons by invitation → war on the kingdom's soil |
| `contest_coven` | lifeline | state, resistance, none, none | — | a payment refused → blight on the fields → the coven comes to collect |
| `contest_pirates` | lifeline | criminal, trade, martial, criminal | requires {"any_of": ["land_coast", "land_island"]} | ships taken → a harbour blockaded → the fleet against the pirate port |
| `contest_slavers` | new | criminal, resistance, trade, none | fourth is a people's role | raids → hunts for the escaped → open revolt |
| `contest_thieves_guild` | heart | criminal, state, criminal, martial | seats {"a": "heart"} | a killing in daylight → war in the alleys → the guild names the next ruler |

## Trope breaks: the hooks

- `break_dead_rise`: P2: the rite that lays the dead is written, with the god or the order that owns it · P5: every settlement has someone who lays the dead · P6: a site's unlaid dead rose where they fell; its ecology says so · P8: the primer says what is done with a body, and how soon
- `break_chosen_are_many`: P2: each great god's mark and the rules it lays on the marked are written · P5: chosen NPCs are in the roster, some of them unwilling · P9: a PC may carry a mark; it is a burden with rules, never a destiny
- `break_dreams_are_a_place`: P2: the dream-land is a touched plane or a region of its own, with its rule of what holds on waking · P3: the dream-land has places that answer to places of the waking map · P6: one site can be entered only in sleep · play: a long rest may open a scene in the dream-land
- `break_oath_curse`: P4: factions bind by few and heavy oaths; who has broken one is known · P5: one NPC lives under a broken oath's curse · P8: the primer says how an oath is sworn and what its breaking brings · P9: an oath a PC has sworn is recorded with what its breaking would bring
- `break_magic_sold`: P3: every town's goods carry enchanted goods and spell services, with prices · P4: a trade or guild faction lives by the magic trade · P6: a site's loot is priced against the market · P8: the primer says what a spell and an enchanted thing cost

## The lifeline and the practice

- `life_enchanters`: no `where` (an everywhere row); requires {"dial": {"magic": ["medium", "high"]}}; text: name: the enchanters' workshops · who: enchanters and their apprentices · yields: enchanted goods, made to order and sold abroad · weak_point: the masters' formulae; the rare materials that must come from elsewhere · sense: the smell of hot metal and the hum of a working that has not yet settled
- `practice_enchanted_goods`: family `make`; hints ['guild', 'trade']; requires {"dial": {"magic": ["medium", "high"]}}; name: they make and sell enchanted goods; gives: enchanted goods to buy and to order

## The pairs, as data

- fits (weights): `break_dead_rise` ×2 with `contest_living_dead` and with `ruin_plague`; `contest_relic_pieces` ×3 with `ruin_sundered_relic`; `contest_dark_lord` ×2 with `ruin_dark_lords_fall`; `contest_sealed_remnant` ×3 with `ruin_sleeper` (on the existing row); `contest_order_schism` ×2 with `ruin_fallen_order` (on the existing row); `break_beasts_own_land` ×2 with `ruin_beast_blood` (on the existing row); `break_dreams_are_a_place` ×2 with `ruin_sleeping_realm`; `break_oath_curse` ×2 with `ruin_great_curse` and ×2 with the eight treaty lifelines; `break_magic_sold` ×2 with `life_enchanters`; `practice_enchanted_goods` ×2 with `break_magic_sold`.
- clashes: `break_magic_sold` conflicts with `ruin_dried_source`; it requires the magic dial at medium or high; it claims `magic: plentiful`.
- merges: `break_monsters_have_treaties` with `contest_living_dead`; `break_the_enemy_won` with `contest_dark_lord`; `contest_dark_lord` with `ruin_dark_lords_fall` (on the contest row).
- requires: `ruin_deep_minds` (coast, island, lake or underground); `contest_pirates` (coast or island); the enchanters' lifeline and practice (magic medium or high).

## Changed from the document, or added beside it

- The lifeline's id is `life_enchanters`, not `lifeline_enchanters`: every lifeline id carries the prefix `life_`, and code and tests select lifelines by it.
- `contest_relic_pieces` carries `prize: new` and `prize_with: {ruin_sundered_relic: remnant}`; `design_foundation.py` reads `prize_with` (one line).
- The eight lists that mean "a lifeline of the family craft" (the gnome lineage's weight, the workshops trait's weight, three contests' requirement and weight) gained `life_enchanters`.
- `contest_elemental_lord`'s ruling "as the other treaties: a treaty weighs its own contest ×2" has nothing to attach to: no treaty lifeline of the elementals exists (the bound-elemental lifeline was removed at the review). Nothing was written.
- The claim `magic: plentiful` on `break_magic_sold` also clashes, through the registry's own pair, with `magic: faded` (`ruin_age_of_mages`): a pair the document does not list.
- No content-mix weight was written on the new contests (36 of the 40 old ones carry one): none was ruled.
- The hints and prizes are the proposed ones, unchanged; all of them fit the tables' rules.
