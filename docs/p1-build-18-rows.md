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

## 5. The secret layer (`secrets.yaml`, `antagonists.yaml#break_tie`; approved 2026-10-05)

**The secret is the threat's hidden half, not a separate object.** The archetypes were made when the break was an abstract event that needed a cause; on the threat chain, the campaign's great mystery is what D&D's always is: who stands behind the hand, what it wants and why, where it is, and how it can be stopped. A separate "hidden truth" on top of the chain bred a second story (this birth's mind from outside) and made every campaign a conspiracy, where the published campaigns range from open war with a known villain to deep mystery.

1. **The four hidden facts** (every campaign, from the chain): *who* (the villain; public when its visibility is known), *what it wants and why* (the goal and its justification), *where* (its lair or seat), *how it is stopped* (the weakness). A known villain leaves three; the visibility sets how deep the mystery runs.
2. **Three stages**, each with a conclusion that tells the party what to do next, and three clues for each conclusion (finding D2):

| Stage | Tier | The conclusion |
|---|---|---|
| 1 | the first | someone stands behind the hand; the hand's base is here |
| 2 | the second | it is this one, it wants this, for this reason |
| 3 | the last | it is there, and this is how it is stopped |

3. **The twist is optional:** the threat secrets below are no longer the main secret; one is rolled as a twist, always when the content mix holds mystery, otherwise one birth in two; it is revealed at stage 2 or at the final confrontation and recolours the threat.
   - **Removed from the secret** (world-lore secrets with no face, which competed with the threat): the gods are mortal ancestors, the gods are prisoners and a god erased from memory (the last two become the god family's two forms: an imprisoned god, a forgotten god returning), magic is borrowed, magic is a disease, the end is kept back, we feed it, the land is alive, the planes are one, two worlds overlaid, a curse fell due, dreamed into being.
   - **The twists** (20): the prize is a seal; the relic is a person; the move was a cure; the monsters were people; the protector makes the threat; someone is a replacement; the destiny was composed by someone alive; the move was spoken as a true name's command; the old victory was bought and its price comes due; it was meant for something else; something was taken under it; it was a rehearsal; it was the lesser of what was demanded; it was done from inside; it set someone free; a death was refused; someone is worn by a mind from outside; it clears the ground for an old order; it was done before (the villain repeats what felled the old kingdom); **new:** a greater power stands behind the villain (the villain is a pawn).
4. **The keeping** (today's "twists", renamed: how the truth is held; 17): two hold a half each; one faction knows; worse than the rumour; the keeper is kind; revealing it opens something; going with the last witness; the blamed are the harmed; half is public; the secret is owned; it can be undone; it cannot be undone; the move grew larger than the villain meant (was "the chooser did not know"); the villain works to undo it (only with "backfired", below); the people know and nobody believes; **new:** the one who sends the heroes is the hand itself; **new:** the pitied victim staged it all. ("A PC is involved" leaves the list: item 6.)
5. **The trails** (11; the clue shapes of each stage; the third stage's clues reveal the weakness): the ten of today and **new:** omen, divination, the testimony of the dead (*speak with dead*, *divination*).
6. **A hero bound to the threat is standard:** at P9 at least one player character is tied to the chain in every campaign (it was one twist in fifteen).
7. **The chooser table goes** (the villain always chose the move; two of its rows let texture choose the break: someone of the signature institution, someone of the signature people).
8. **The tie to the break becomes the move's state** (4 rows): done (the first step is taken; the plan moves on); stopped short (something stopped it; it will try again); backfired (it let loose something it did not intend and now fights that too); unnoticed (nobody ties the move to anyone). "Exploits it", "is its product", "tried to stop it" and "wants to reverse it" assumed a break apart from the villain and go. The time table stays (just now, a generation ago, unfolding, coming).

## 6. The trope breaks (`trope-breaks.yaml`; approved 2026-10-05)

The trope breaks stay (owner: they make the difference felt at the table; in the test birth they were the strongest part). Two guards:

- **The world states join the story.** Eight rows say who rules or what dominates the world and are `layer: story`: rulers by lot, guilds rule with no lords, magic is nobility, dragons rule the lands, a beast-person lords some lands, the moon is inhabited and trades, the gods live among mortals, the enemy won. Each is drawn only where it can join a story piece, and joins it: the heart's rule and the contest (lot, guilds, magic nobility); the dragon family or hand, or the contest with a dragon (dragons rule); the disputed land or a contest side (the beast-lord); the thin place or a hand (the moon); the god family or a side at the gods' level (the gods among mortals); the ruin or the villain (the enemy won). The other 28 are rules of life, texture. ("The dead rise unless laid" and "the chosen are many" were read and stay rules of life.)
- **A trope break bends a D&D assumption and never removes it.** Dungeons, each class's core features and the three pillars always stand; every break that touches the players is told in the P8 player files and at character creation. Two rows are bent: *writing is unknown* becomes **writing is sacred: only the ordained may write** (spellbooks, scrolls, maps and letters stay); *divine magic works only on holy ground* becomes **divine magic is strongest on holy ground and costs something beyond it** (the cleric and the paladin keep their core). *Casting is forbidden* (the caster is an outlaw, the magic works) and *there is no common tongue* stay as they are, told at session zero.

## 7. The palette's size (`foundation.yaml#palette`; approved 2026-10-05)

The count follows the spine. A **tight** spine (one feature dominates: the lone mountain, the giant tree, the three depths, the mountain within, the oasis ring, the star crater, the void ring, the titan's back, the floating archipelago, the terraces, the lake basin, the forest clearings, the mesas, the valley maze, above and below the sea) takes short 2-3, standard 3-4, epic 4-5 kinds; a **wide** spine (a journey across varied land: the river to the sea, the great rift, the mountain passes, the long coast, the barren corridor, the crossroads, the archipelago, the lake chain, the two worlds, the peninsula, the strait, the long wall, the climate belt, the edge of civilisation, the world's edge) takes short 3-4, standard 4-6, epic 6-8. (Today every spine takes 4-5, 6-8, 9-12.) **Sufficiency:** the published regions run from about four terrains (Barovia, Phandalin's land) through five (Chult) to eight or ten (the Savage Frontier); variety comes from 22 kinds × 30 spines, not from the count.
