# Build 18c-1: the threat's fit lists (SPOILER)

*Drafted by the coding tab from docs/p1-build-18.md Part 18c and docs/p1-build-18-rows.md sections 4 and 8; generated from the tables as committed. The villain tables are secret: the owner, who is also the player, should not read this file unless he chooses to.*

## List 1: family → SRD creatures and reskin bases (CR window: max(2, L-2) to L+4, to 30 once L reaches 17)

| Family | Scales | SRD creatures (CR) | Reskin bases | Power source | Weights |
|---|---|---|---|---|---|
| `family_mage` | short, standard, epic | mage (6), archmage (12) | archmage | above short | x2 when ruin_age_of_mages, ruin_sorcerer_kings, ruin_mage_war, ruin_failed_experiment |
| `family_ruler` | short, standard, epic | knight (3), veteran (3), gladiator (5) | knight | above short | x2 when ruin_empire, ruin_dark_lords_fall |
| `family_shadow` | short, standard, epic | assassin (8), spy (1), bandit-captain (2) | assassin | above short | — |
| `family_dark_priest` | short, standard, epic | priest (2), druid (2), cult-fanatic (2) | priest | above short | — |
| `family_undead` | short, standard, epic | wight (3), ghost (4), mummy (3), wraith (5), vampire-spawn (5), vampire-vampire (13), mummy-lord (15), lich (21) | lich | — | x2 when ruin_kingdom_of_the_dead, ruin_plague; x2 when content mix horror |
| `family_chromatic_dragon` | short, standard, epic | young-black-dragon (7), young-blue-dragon (9), young-green-dragon (8), young-red-dragon (10), young-white-dragon (6), adult-black-dragon (14), adult-blue-dragon (16), adult-green-dragon (15), adult-red-dragon (17), adult-white-dragon (13), ancient-black-dragon (21), ancient-blue-dragon (23), ancient-green-dragon (22), ancient-red-dragon (24), ancient-white-dragon (20) | — | — | — |
| `family_metallic_dragon` | short, standard, epic | young-brass-dragon (6), young-bronze-dragon (8), young-copper-dragon (7), young-gold-dragon (10), young-silver-dragon (9), adult-brass-dragon (13), adult-bronze-dragon (15), adult-copper-dragon (14), adult-gold-dragon (17), adult-silver-dragon (16), ancient-brass-dragon (20), ancient-bronze-dragon (22), ancient-copper-dragon (21), ancient-gold-dragon (24), ancient-silver-dragon (23) | — | — | — |
| `family_devil` | short, standard, epic | bearded-devil (3), barbed-devil (5), chain-devil (8), bone-devil (9), erinyes (12), horned-devil (11), ice-devil (14), pit-fiend (20) | pit-fiend | — | x2 when ruin_devils_bargain; x2 when content mix horror |
| `family_demon` | short, standard, epic | vrock (6), hezrou (8), glabrezu (9), nalfeshnee (13), marilith (16), balor (19) | balor | — | x2 when ruin_demon_gate; x2 when content mix horror |
| `family_deceiver_fiend` | short, standard, epic | succubus-incubus (4), night-hag (5), rakshasa (13) | rakshasa | — | x2 when content mix horror |
| `family_from_beyond` | short, standard, epic | cloaker (8), aboleth (10) | aboleth | — | x2 when ruin_deep_minds; x2 when content mix horror |
| `family_giant` | short, standard, epic | hill-giant (5), stone-giant (7), frost-giant (8), fire-giant (9), cloud-giant (9), storm-giant (13) | storm-giant | — | x2 when ruin_giants_land, ruin_giants_and_dragons |
| `family_hag_fey` | short, standard, epic | sea-hag (2), green-hag (3) | green-hag | — | x2 when ruin_elven_withdrawal, ruin_sleeping_realm |
| `family_monstrous_mind` | short, standard, epic | lamia (4), medusa (6), spirit-naga (8), guardian-naga (10), gynosphinx (11), androsphinx (17) | androsphinx | — | — |
| `family_genie_elemental` | standard, epic | djinni (11), efreeti (11) | efreeti, djinni | — | x2 when ruin_bound_elements |
| `family_lycanthrope` | short, standard | wererat-hybrid (2), werewolf-hybrid (3), wereboar-hybrid (4), weretiger-hybrid (4), werebear-hybrid (5) | werebear-hybrid | above short | x2 when ruin_beast_blood |
| `family_fallen_celestial` | standard, epic | deva (10), planetar (16), solar (21) | solar | — | x2 when ruin_celestial_war |
| `family_sea_titan` | epic | dragon-turtle (17), kraken (23) | kraken | — | x2 when ruin_great_flood, ruin_water_kingdom |
| `family_god` | standard, epic | — (an avatar) | deva, planetar, solar | — | x2 when ruin_dead_god, ruin_gods_quarrel, ruin_departed_god, ruin_imprisoned_god, ruin_failed_apotheosis |

Band coverage (a creature in the window, else the reskin): every family at every band top from 5 to 20 (tested).

## List 2: weakness → families (absent: every family but the god, whose own list holds seven)

- `weak_hidden_object`: every family
- `weak_weapon_or_metal`: every family
- `weak_true_name`: family_devil, family_demon, family_deceiver_fiend, family_hag_fey, family_genie_elemental, family_god; the god
- `weak_loved_person`: every family
- `weak_vow_or_bargain`: every family; the god
- `weak_place_bound`: every family; the god
- `weak_vulnerable_time`: every family
- `weak_old_rival`: every family
- `weak_plan_flaw`: every family
- `weak_prophecy`: every family; the god
- `weak_enemy_forgiveness`: every family
- `weak_source_cut`: every family; the god
- `weak_cannot_refuse_challenge`: every family
- `weak_secret_turns_followers`: every family
- `weak_law_of_nature`: family_undead, family_hag_fey
- `weak_sacred_relic`: family_undead, family_devil, family_demon, family_deceiver_fiend, family_hag_fey, family_genie_elemental, family_fallen_celestial, family_god; the god
- `weak_drawn_from_lair`: family_chromatic_dragon, family_metallic_dragon, family_undead, family_from_beyond, family_monstrous_mind, family_sea_titan, family_fallen_celestial, family_god
- `weak_rite_binds_again`: family_devil, family_demon, family_deceiver_fiend, family_hag_fey, family_genie_elemental, family_from_beyond, family_sea_titan, family_god; the god
- `weak_army_by_compulsion`: every family

## List 3: lair form → families (`built`: a place it built may be it; `mobile`: only on the move)

- `lair_castle`: family_ruler, family_undead, family_devil, family_mage, family_metallic_dragon, family_shadow, family_deceiver_fiend, family_hag_fey, family_genie_elemental, family_god · built
- `lair_tower`: family_mage, family_undead, family_fallen_celestial, family_ruler, family_devil · built
- `lair_tomb`: family_undead, family_god, family_monstrous_mind, family_dark_priest
- `lair_temple`: family_dark_priest, family_god, family_demon, family_monstrous_mind, family_fallen_celestial, family_devil, family_deceiver_fiend, family_sea_titan · built
- `lair_cavern`: family_chromatic_dragon, family_metallic_dragon, family_giant, family_from_beyond, family_monstrous_mind, family_lycanthrope, family_demon, family_hag_fey, family_sea_titan
- `lair_ruined_fortress`: family_ruler, family_undead, family_giant, family_lycanthrope, family_fallen_celestial, family_monstrous_mind, family_chromatic_dragon, family_metallic_dragon, family_shadow, family_demon, family_sea_titan
- `lair_sunken_temple`: family_from_beyond, family_sea_titan, family_monstrous_mind, family_chromatic_dragon, family_metallic_dragon, family_dark_priest, family_genie_elemental · built
- `lair_volcano`: family_chromatic_dragon, family_genie_elemental, family_giant, family_demon
- `lair_ice_fortress`: family_chromatic_dragon, family_giant · built
- `lair_swamp`: family_chromatic_dragon, family_hag_fey, family_lycanthrope, family_dark_priest, family_deceiver_fiend
- `lair_grove`: family_hag_fey, family_dark_priest, family_chromatic_dragon, family_lycanthrope
- `lair_hidden_quarter`: family_shadow, family_deceiver_fiend, family_lycanthrope, family_mage, family_devil, family_from_beyond · built
- `lair_demiplane`: family_undead, family_devil, family_demon, family_deceiver_fiend, family_hag_fey, family_fallen_celestial, family_god, family_mage, family_from_beyond, family_genie_elemental
- `lair_flying_citadel`: family_giant, family_genie_elemental, family_chromatic_dragon, family_fallen_celestial, family_metallic_dragon, family_god · built · mobile
- `lair_ship`: family_ruler, family_sea_titan, family_shadow · mobile
- `lair_mines`: family_giant, family_from_beyond, family_mage, family_ruler, family_shadow · built

## List 4: lair where

On the move only with a mobile form (and a mobile form only on the move); a place it built only with a `built` form; the thin place only with `land_thin_place` in the palette; the other four always.

## List 5: the goal and its join

A goal whose pieces hold the main contest's prize weighs x2 (a seat counts as a role). The join: `prize` (its piece is the prize), `role_goal` (`goal_side_as_weapon`, `goal_destroy_bloodline`, `goal_avenge_wrong`), else `move` (18c-2).

## Questions

1. Creatures chosen where the rows name none in the SRD: the cloaker beside the aboleth (from beyond); the spy and the bandit captain beside the assassin (shadow); the hill giant beside the five named giants; the hybrid form of each lycanthrope; the succubus or incubus beside the night hag and the rakshasa.
2. The family weights are the coding tab's reading of "weighted by the ruin" (List 1); the world states no longer weigh the family (G4: the threat comes first).
3. `weak_law_of_nature` fits the undead alone (the vampire's sunlight and running water). Does a lycanthrope's silver count (it is a weapon or a metal, already its own row)?
4. Lair forms where the rows name no family: the lycanthrope (hidden quarter, grove), the fallen celestial (temple, demiplane), the monstrous mind (temple, cavern, sunken temple), the mage (tower, mines).
5. The chromatic dragon fits every lair the rows give a colour (volcano red, ice white, swamp black, grove green, flying citadel blue, cavern); the colour of the rolled creature is not matched to its lair. Should it be?
6. A world state that joins the threat (dragons rule, the gods among mortals) is drawn only where the rolled threat or a public piece holds the join: when no dragon contest is rolled, a public "dragons rule" now tells that the villain is a dragon. Accepted, or should such a world state also need a public join?
7. Reskins are common above short (about half at standard, three fifths at epic): the SRD has few creatures at CR 17-30 outside the dragons. Accepted as the rows foresaw?

## The audit's answers (the development tab, 2026-10-05), applied

1, 2, 7: stand as drafted. 3: the law of its nature fits the undead and the fey. 4: the four families' lair forms as the development tab listed them. 5: the dragon's colour weighs its lair x3 (`dragon_colours`; the chromatic and metallic families gained the forms the colours name). 6: every world state's join is public; a join to the threat counts only when the villain's visibility is known (`design_threat.PUBLIC_VISIBILITY`); the dm-only join record is gone.

**Widened by the coding tab to the floor of five** (every family's lair-form pool now 5, the chromatic dragon 8, the giant 6), for the audit: the ruler + tower, mines; the shadow + castle, ruined fortress, ship, mines; the dark priest + tomb, sunken temple, swamp; the devil + temple, hidden quarter, tower; the demon + cavern, ruined fortress, volcano; the deceiver fiend + castle, swamp, temple; from beyond + demiplane, hidden quarter; the hag or fey + cavern, castle; the genie + demiplane, castle, sunken temple; the sea titan + cavern, ruined fortress, temple; the god + flying citadel, castle.
