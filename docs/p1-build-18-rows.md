# Build item 18 — the rows approved with the owner

*The row reviews of the threat-first redesign (`docs/p1-threat-first.md`), in the order they were held. Each table carries its sufficiency check (owner, 2026-10-05: are the counts enough, or basic?). Labels are the tables' English; the Turkish glosses of the review are in the conversation, not here. The fit lists (which hand can make which move, which verb strikes which target) are written in the specification of part 18b.*

## 1. The move's verbs (`foundation.yaml#action`; approved 2026-10-05)

A verb is something a hand does to a target and a table can fight or undo. The lifeline is no target.

| Verb | From | Targets |
|---|---|---|
| Seized | `act_seized`, kept | heart, key place, remnant, thin place |
| Carried off | `act_vanished`, rewritten | remnant (a relic), role (a leader), heart (its ruler) |
| Corrupted | `act_corrupted`, kept | remnant, key place, heart |
| Woke | `act_awakened`, rewritten | remnant, key place |
| Opened | `act_opened`, kept | remnant, key place, thin place |
| Sealed | `act_closed`, rewritten | key place, thin place |
| Burned | `act_burned`, kept | key place, heart |
| Drowned | `act_sank`, rewritten | remnant, key place, heart |
| Divided | `act_split`, rewritten (absorbs "turned on its keepers") | role, heart |
| Raised in revolt | `act_rose`, rewritten | role, heart |
| Drove out | `act_migrated`, rewritten | role, heart |
| Besieged / cut off | `act_stopped`, rewritten | key place, heart |
| Dragged into another plane | `act_merged_with_plane`, kept | heart, key place, thin place |
| Killed | new | role (its leader), heart (its ruler) |
| Poisoned | new | heart (its water, its ruler) |
| Cursed | new | heart, key place, role (a bloodline) |
| Plundered | new | remnant |
| Summoned | new | thin place |
| Spread a plague | new | heart |
| Replaced | new | role (its leader), heart (its ruler) |
| Possessed | new | role (its leader), heart (its ruler) |
| Enslaved / took hostage | new | role |
| Betrayed | new | role, heart |

Deleted: turned backwards, showed its true face, turned on its keepers, spread without bound, was twinned, was forgotten, gave birth to something new, crushed by what fell from the sky.

**Sufficiency:** 23 verbs cover the DMG's villain methods (murder, theft, captivity, impersonation, possession, curses, desecration, plague, betrayal, rebellion, warfare, magical mayhem); with 28 hands and five targets, the fit lists yield some hundreds of distinct moves.

## 2. The visible hand (new public table; approved 2026-10-05)

A hand is an organisation or a creature, never a whole people; a hand drawn from a people is a part of it, and another part of that people stands elsewhere. Each hand brings the campaign's creature family (finding D4).

| Hand | Creature family | Requires |
|---|---|---|
| the villain itself, openly | the villain's | the villain's visibility is known |
| a war band (a part of the orcs, gnolls or hobgoblins) | humanoid | |
| sea raiders, pirates | humanoid | coast or island |
| a cult | humanoid, and what it serves | |
| a guild of thieves and assassins | humanoid | |
| a traitor inside (a councillor, a general, a priest) | humanoid | |
| a deceived side (a contest role, not knowing what it did) | humanoid | |
| a hired company | humanoid | |
| a foreign army | humanoid | |
| a dragon (with its kobolds and dragonborn servants) | dragon | |
| the risen dead | undead | |
| the ruin's power, woken | the ruin's | a ruin source with a power |
| fiends (summoned or bargained with) | fiend | |
| things from beyond (mind flayers, aberrations) | aberration | |
| giants | giant | |
| a monstrous beast (a hydra, a behir, a purple worm) | monstrosity | |
| a fey court's emissaries | fey | |
| a bound elemental | elemental | |
| werewolves, a cursed pack | lycanthrope | |
| a golem army | construct | magic medium or high |
| a coven of hags | fey | |
| brigands, outlaws | humanoid | |
| slavers | humanoid | |
| a zealous order (a church militant, a knightly order) | humanoid | |
| a rival band of adventurers | humanoid | |
| shapechangers wearing trusted faces | monstrosity | |
| a corrupted druid circle and its blights | plant | |

(The guild of thieves and the assassins are one row; 27 rows.)

**Sufficiency:** every SRD creature type but oozes and celestials is a hand; the classic published campaigns' threats are reachable (dragons, giants, a vampire lord, demons, devils, elemental cults, mind flayers, hags, a criminal underworld, slavers).

## 3. The contests' prizes and gates (`foundation.yaml#contest`; approved 2026-10-05)

**A further leak found:** 8 contests could be drawn only with a given lifeline and 11 were weighted by one: texture chose the story. A contest's requirements and weights now come from the stage (the palette, the spine, the era) and the dials alone; the lifeline is rolled **last**, fitted to the story (texture hangs on the story).

**The prize kinds** (sufficiency: four left without the lifeline was basic): the heart (a throne, a capital), **the key place** (a pass, a harbour, a bridge, a trade road; new as a prize), **the disputed land** (new: an end or the land between), the remnant, the thin place, something new (an artifact, a secret, a formula), **the seat** (new: a house's hall or inheritance).

| Contest | New prize | Gate |
|---|---|---|
| `contest_one_harbour` | key place (the harbour) | coast |
| `contest_one_pasture` | disputed land | highland, plain or steppe |
| `contest_two_banks` | key place (the weir, the ford) | river |
| `contest_settlers_newcomers` | disputed land | (role b loses "who bring the thing the land needs") |
| `contest_old_new_craft` | **deleted** | |
| `contest_capital_marches` | disputed land (the marches) | |
| `contest_lords_peasants` | heart (the lord's seat) | |
| `contest_mine_owners_miners` | key place (the mine) | mountain, highland or underground |
| `contest_open_close_road` | key place (the road, the pass) | the spine |
| `contest_share_keep_knowledge` | something new (the secret, the book) | magic medium or high (no craft lifeline) |
| `contest_split_family` | **deleted** (two heirs covers it) | |
| `contest_humans_giants` | disputed land | |
| `contest_humans_dragon` | disputed land | |
| `contest_humans_fey` | disputed land (the forest) | |
| `contest_surface_deep` | key place (the tunnels) | |
| `contest_land_sea_folk` | disputed land (the shore) | |
| `contest_merchant_house_divides` | heart | |
| `contest_war_fed_company` | disputed land | |
| `contest_shapeshifter` | seat | |
| `contest_fiend_pact` | seat | |
| `contest_elemental_lord` | disputed land | |
| `contest_coven` | disputed land (the villages) | |
| `contest_pirates` | key place (the sea lanes) | |

The eleven lifeline weights go. **Sufficiency:** 49 contests in 8 families; the classic D&D conflicts are covered (a war of succession, a border war, a revolt, a land dispute with a monstrous people, a cult, pirates, a fiend's pact).
