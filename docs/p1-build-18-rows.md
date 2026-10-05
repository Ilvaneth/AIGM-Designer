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

## 4. The threat (`antagonists.yaml`; approved 2026-10-05, nothing hidden from the owner)

**New findings at this review:** the villain had no kind (what it *is*: a lich, a dragon, a human archmage), which the writer decided; two shapes and one visibility made the villain faceless (a working or a body); two origins let texture make the villain (the phenomenon, the institution); and no rule tied the villain's strength to the level band's top.

### 4.1 The villain's kind: two layers (new)

1. **The family** (rolled; a family drawn in the latest births waits, and no family comes twice in a row):

| Family | Short / standard / epic (examples) |
|---|---|
| mage | mage / archmage / an ascending archmage (with a power source) |
| ruler or warlord | knight-based; standard and epic with a power source |
| shadow (spymaster, guild master) | spy / assassin / with a power source |
| dark priest, corrupted druid | priest / with a power source (what it serves) |
| undead | wight, ghost, banshee / vampire, mummy lord / lich |
| chromatic dragon (black, blue, green, red, white) | young / adult / ancient |
| metallic dragon gone wrong | young / adult / ancient |
| devil (contracts, order) | erinyes / horned, ice devil / pit fiend |
| demon (chaos) | vrock, hezrou / glabrezu, nalfeshnee / marilith, balor |
| deceiver fiend | night hag / rakshasa / reskinned |
| from beyond | aboleth / an elder aboleth (reskin) |
| giant | stone, frost / fire, cloud, storm / a storm king (legendary) |
| hag coven, fey | green or sea hag / a coven / a fey lord (reskin) |
| monstrous mind (medusa, lamia, naga, sphinx) | medusa, lamia / naga, gynosphinx / androsphinx |
| genie, elemental lord | — / efreeti, djinni / a reskinned elemental lord |
| lycanthrope | werewolf, weretiger / with a power source / — |
| fallen celestial | — / deva / planetar, solar |
| sea titan | — / — / kraken, dragon turtle |

2. **The creature:** an SRD creature of that family whose CR fits the level band's top (the final fight is at the top; measured candidates that speak and stand at CR 2 or more: 67 for short at CR 3-9, 37 for standard at CR 9-16, 25 for epic at CR 15-30, 17 of them dragons), or a reskin by the reskin rule where the family has none at that band. **A humanoid family above short carries a power source** (an artifact, a pact, a curse, what it serves): the DMG's human villains draw their strength from one, and the power source is a candidate for the weakness. The dragon families are two of the eighteen, so an epic campaign leans to dragons at most two in fourteen.

**Sufficiency:** 13 to 16 families stand open at each length; with shape (19), origin (12), goal (20), weakness (19), hand (27) and visibility (5) the villain repeats rarely. Measured at the build over 1,000 seeds: consecutive repeats, each family's share, distinct (family, creature, shape, goal) sets.

### 4.2 The goal (new, secret; 20 rows)

Power: take the throne (heart); become the power behind the throne (heart); conquer the land (disputed land); turn a side into its weapon (role). Wealth: control the key place and all that passes (key place); plunder the ruin's treasure (remnant). Magic: take the remnant's artifact (remnant); open the gate at the thin place (thin place); build a great device or construct (something new); carry out a patron's will (thin place, something new). Immortality: live forever through the remnant (remnant); ascend to godhood (thin place, remnant). Mayhem: destroy a bloodline or a side (role); overthrow the order and let it burn (heart); lay a curse or a plague on the land (heart, disputed land); fulfil an apocalyptic prophecy (something new). Passion: bring back a dead loved one (something new, thin place); keep a dying loved one alive (something new). Revenge: avenge an old wrong on a side (role); take back what was stolen and punish the thief (remnant, role).

**Sufficiency:** the DMG's eight villain objectives, each bound to a story piece.

### 4.3 The weakness (new, secret; 19 rows, each with the kinds it fits)

A hidden object holds its life; a weapon or a metal it cannot bear; its true name (fiends, fey, genies and elementals only: in D&D a demon's or devil's true name lets one summon, bind and command it, and the fey's names are power); a person it loves; a vow or a bargain it must keep; a place it cannot leave or must return to; a time it is vulnerable (a night, an eclipse, a season); an old rival who knows how; a flaw in its plan (the device's or the rite's missing piece); a prophecy or riddle that names its end; an ancient enemy's forgiveness; its source can be cut (its hand, its cult, its thin place); it cannot refuse a challenge; its secret, made public, turns its own followers; a law of its nature (sunlight, running water, no entry unbidden); a sacred relic or hallowed ground weakens it; drawn from its lair it is weaker; the rite that bound it once can bind it again; its army serves by compulsion and leaves when the compulsion breaks. The third clue stage reveals it.

**Sufficiency:** the DMG's eight weaknesses and eleven common to D&D; the fit lists keep "a tyrant's true name" from being drawn.

### 4.4 Changes to the existing rows

- **Shapes** (21 → 19): `shape_process` (the tender of a working) and `shape_institution` deleted; an institution is a hand now and a working is a verb.
- **Origins** (13 → 12): `origin_taken_by_phenomenon` and `origin_made_by_institution` deleted (texture made the villain); **added:** forbidden knowledge (it learned what should not be learned: the classic origin of a lich).
- **Visibility** (5 → 5): `vis_process_or_institution` deleted (faceless); **added:** known, but no one knows where (the hunt for a hidden lair).

### 4.5 The nineteenth family: a god (approved 2026-10-05)

**A god: an avatar, a fallen or an imprisoned god**, at standard and epic only (at short a god is too large). In 5e a god has no stat block and the party never fights one outright; the published god-villain campaigns are built three ways, and the family holds the first two (the third is the goal "ascend to godhood"): an imprisoned or fallen god whose cult works to bring it back (the final fight is its avatar or half-come form), and a living god acting through an avatar. The creature is the avatar, reskinned to a CR that fits the band's top. Its weaknesses fit: its source cut (the faithful, the cult), the rite that bound it once, its true name, a sacred relic. The god stands in P2's pantheon (a promise to P2), its church is a natural hand (a cult or a zealous order), and no god of real-world mythology (errata #19). The secret's pin to a god (opening W1) becomes a rolled family, not the writer's invention.
