# Build item 13a — the rows that gained English text

*Written by the coding tab, 2026-10-04, for the development tab's audit (`docs/p1-build-13.md` §3).*

Every `tr` field of the P0 and P1 tables is gone. A row listed here carries its English in a field named `text` (the same keys the Turkish had: `name`, `heart`, `ends`, `key_place`, `travel`, `what`, `remnant`, `sites`, `strangeness`, `who`, `yields`, `weak_point`, `sense`, `at_table`, `gives`, and the `*_note` keys), a contest role in `roles.<key>.text` (its note in `text_note`), a contest's steps in `escalation`, an action's three forms in `forms`.

Not listed, because nothing was added: 46 rows whose only Turkish was a `name` equal to the English `label` (lineages, forms, phenomenon signs and users, the ties, the three tone values): the `tr` field was removed and the label stands. The 33 questions: their English `poles` already stood; the Turkish pair was removed.

**The secret and villain tables** (`secrets.yaml`, `antagonists.yaml`) held no Turkish field; no row of them was touched.

## `foundation.yaml` — 245 rows

`land_mountain`, `land_highland`, `land_plain`, `land_steppe`, `land_forest`, `land_marsh`, `land_desert`, `land_cold`, `land_volcanic`, `land_river`, `land_lake`, `land_coast`, `land_island`, `land_underground`, `land_floating_isles`, `land_crystal_forest`, `land_stone_sea`, `land_giant_bones`, `land_sky_river`, `land_glass_desert`, `land_giant_fungus`, `land_thin_place`, `spine_river_to_sea`, `spine_great_rift`, `spine_mountain_passes`, `spine_long_coast`, `spine_barren_corridor`, `spine_lake_basin`, `spine_lone_mountain`, `spine_star_crater`, `spine_oasis_ring`, `spine_crossroads`, `spine_archipelago`, `spine_valley_maze`, `spine_forest_clearings`, `spine_mesa_land`, `spine_lake_chain`, `spine_three_depths`, `spine_terraces`, `spine_two_worlds`, `spine_mountain_within`, `spine_above_below_sea`, `spine_peninsula`, `spine_strait_two_continents`, `spine_long_wall`, `spine_climate_belt`, `spine_edge_of_civilisation`, `spine_titan_back`, `spine_floating_archipelago`, `spine_void_ring`, `spine_giant_tree`, `spine_world_edge`, `ruin_road_kingdom`, `ruin_water_kingdom`, `ruin_sorcerer_kings`, `ruin_city_states`, `ruin_steppe_union`, `ruin_mage_war`, `ruin_giants_and_dragons`, `ruin_besieged_land`, `ruin_kin_war`, `ruin_celestial_war`, `ruin_dead_god`, `ruin_gods_quarrel`, `ruin_departed_god`, `ruin_imprisoned_god`, `ruin_failed_apotheosis`, `ruin_age_of_mages`, `ruin_failed_experiment`, `ruin_made_peoples`, `ruin_golem_army`, `ruin_dried_source`, `ruin_great_flood`, `ruin_eruption`, `ruin_ice_age`, `ruin_plague`, `ruin_fallen_star`, `ruin_mine_rush`, `ruin_endless_building`, `ruin_merchant_hoards`, `ruin_returning_forest`, `ruin_alchemy_spill`, `ruin_dwarf_city`, `ruin_elven_withdrawal`, `ruin_giants_land`, `ruin_age_of_dragons`, `ruin_winged_mountains`, `ruin_planar_rift`, `ruin_fallen_sky_city`, `ruin_planar_invasion`, `ruin_broken_time`, `ruin_star_kingdom`, `life_snowmelt`, `life_river_flood`, `life_deep_lake`, `life_oasis_springs`, `life_hot_springs`, `life_rain_season`, `life_glacier`, `life_fog_nets`, `life_winter_pass`, `life_river_ford`, `life_natural_harbour`, `life_caravan_inn`, `life_rift_bridge`, `life_strait_crossing`, `life_deep_mouth`, `life_marsh_boardwalk`, `life_ice_road`, `life_yak_herds`, `life_fish_run`, `life_silk_gardens`, `life_bee_forests`, `life_horse_herds`, `life_deer_migration`, `life_oyster_beds`, `life_giant_insects`, `life_griffon_eyries`, `life_copper_mine`, `life_iron_coal`, `life_timber_forest`, `life_peat_bog`, `life_quarry`, `life_gemstones`, `life_dye_sources`, `life_pitch_tar`, `life_amber_shores`, `life_terrace_rice`, `life_olive_groves`, `life_vineyards`, `life_flax_fields`, `life_wheat_plain`, `life_date_fig_gardens`, `life_spice_gardens`, `life_mushroom_fields`, `life_tea_slopes`, `life_famous_steel`, `life_glassblowing`, `life_carpet_weaving`, `life_shipbuilding`, `life_tile_ceramics`, `life_leather_armour`, `life_potions_medicine`, `life_bowyery`, `life_giant_peace`, `life_dragon_protection`, `life_fey_bargain`, `life_sea_folk_hunt`, `life_hired_guard`, `life_binding_marriage`, `life_shared_water_right`, `life_pilgrim_road`, `contest_two_heirs`, `contest_one_harbour`, `contest_one_pasture`, `contest_one_shrine`, `contest_two_banks`, `contest_settlers_newcomers`, `contest_old_order_reform`, `contest_old_new_craft`, `contest_old_gods_new_faith`, `contest_returners_stayers`, `contest_occupier_resistance`, `contest_capital_marches`, `contest_lords_peasants`, `contest_mine_owners_miners`, `contest_casters_casterless`, `contest_sealed_remnant`, `contest_open_close_road`, `contest_forbidden_lands`, `contest_share_keep_knowledge`, `contest_open_close_gate`, `contest_treasure_race`, `contest_empty_throne`, `contest_first_settlers`, `contest_monster_bounty`, `contest_new_resource`, `contest_two_branches`, `contest_order_schism`, `contest_divided_city`, `contest_sibling_rulers`, `contest_split_family`, `contest_humans_giants`, `contest_humans_dragon`, `contest_humans_fey`, `contest_surface_deep`, `contest_land_sea_folk`, `contest_merchant_house_divides`, `contest_foreign_envoy`, `contest_war_fed_company`, `contest_fallen_state_remnant`, `contest_shapeshifter`, `target_lifeline`, `target_remnant`, `target_key_place`, `target_heart`, `target_role`, `target_thin_place`, `act_vanished`, `act_seized`, `act_reversed`, `act_split`, `act_corrupted`, `act_awakened`, `act_fell_from_sky`, `act_stopped`, `act_opened`, `act_closed`, `act_merged_with_plane`, `act_true_face`, `act_turned_on_keepers`, `act_spread_unbounded`, `act_migrated`, `act_burned`, `act_rose`, `act_sank`, `act_twinned`, `act_forgotten`, `act_gave_birth`, `scar_new_land_kind`, `scar_roads_changed`, `scar_cursed_belt`, `scar_unreachable_region`, `scar_magic_rule_changed`, `scar_god_changed`, `scar_plane_thinned`, `scar_sky_changed`, `scar_seasons_broken`, `scar_time_flow_changed`, `scar_people_displaced`, `scar_new_people`, `scar_state_fell`, `scar_creatures_changed`, `scar_new_resource`, `scar_lost_knowledge`, `scar_new_taboo`, `scar_new_belief`, `time_just_now`, `time_generation_ago`, `time_unfolding`, `time_coming`, `tier_local`, `tier_regional`, `tier_continental`, `tier_world`

## `signatures.yaml` — 164 rows

`lineage_merfolk`, `lineage_goblinoid`, `lineage_mixed`, `trait_skin_of_the_land`, `trait_horns_with_age`, `trait_no_shadows`, `trait_breathe_water`, `trait_cold_proof`, `trait_lifeline_marks`, `trait_old_at_forty`, `trait_never_own_table`, `trait_haggling_art`, `trait_decided_by_race`, `trait_hidden_faces`, `trait_history_danced`, `trait_raised_with_a_beast`, `trait_giant_birds`, `trait_bee_council`, `trait_giant_insect_homes`, `trait_hunt_with_wolves`, `trait_dolphin_fishers`, `trait_break_is_punishment`, `trait_break_is_a_gift`, `trait_world_turns_back`, `trait_mountain_spirits`, `trait_worship_the_lifeline`, `trait_sacred_animal`, `trait_rulers_by_contest`, `trait_decisions_in_the_open`, `trait_the_young_rule`, `trait_workshops_not_families`, `trait_two_chiefs`, `trait_remember_before`, `trait_first_changed`, `trait_carry_the_wound`, `trait_fled_the_break`, `trait_foresaw_the_break`, `trait_won_by_the_break`, `trait_break_site_sacred`, `trait_live_vertically`, `trait_underground_by_day`, `trait_live_in_treetops`, `stranger_hospitable`, `stranger_merchant`, `stranger_wary`, `stranger_closed`, `stranger_hostile_for_cause`, `stranger_divided`, `form_house`, `form_travelling`, `form_society`, `form_confederacy`, `practice_hold_the_key_place`, `practice_keep_the_one_road`, `practice_hold_the_remnant_gate`, `practice_players`, `practice_pilots`, `practice_couriers`, `practice_caravan_masters`, `practice_ferrymen`, `practice_keep_the_old_works`, `practice_golem_founders`, `practice_ship_and_bridge`, `practice_mapmakers`, `practice_study_the_remnant`, `practice_seek_the_lost`, `practice_keep_the_dying`, `practice_healers`, `practice_keep_the_granaries`, `practice_midwives`, `practice_herd_healers`, `practice_monster_hunters`, `practice_border_riders`, `practice_champions`, `practice_free_company`, `practice_dragon_hunters`, `practice_monopoly`, `practice_sell_the_remnant`, `practice_sole_seller`, `practice_foreign_house`, `practice_smugglers_union`, `practice_keep_the_lifeline_rite`, `practice_pilgrim_guides`, `practice_guard_the_holy_place`, `practice_worship_the_break`, `isign_painted_mark`, `isign_one_colour`, `isign_animal_mask`, `isign_tool_of_the_trade`, `isign_initiation_scar`, `isign_animal_companion`, `isign_travel_in_pairs`, `isign_never_leave`, `isign_give_half_away`, `isign_own_language`, `isign_one_secret_each`, `isign_yearly_gathering`, `power_monopoly`, `power_place`, `power_knowledge`, `power_arms`, `power_love`, `power_sanctity`, `power_treasure`, `power_creature_bond`, `power_privilege`, `power_fear`, `rule_echo`, `rule_rebound`, `rule_inverted_element`, `rule_spells_grow_life`, `rule_spell_twins`, `rule_shared_wounds`, `rule_slow_change`, `rule_beasts_sense_lies`, `rule_kin_doubles`, `rule_spell_marks`, `rule_visible_currents`, `rule_mirror_doors`, `rule_roads_lead_where_needed`, `rule_night_distances`, `rule_shifting_doors`, `rule_remnant_drinks_magic`, `rule_weightless_stone`, `rule_water_remembers`, `rule_metal_wakes`, `rule_smoke_shows_shape`, `rule_time_differs`, `rule_shadows_of_the_future`, `rule_repeating_moment`, `rule_delayed_spells`, `rule_casting_ages`, `rule_true_names`, `rule_signs_are_spells`, `rule_gesture_magic`, `rule_tongue_of_magic`, `rule_names_shape_places`, `rule_feelings_make_weather`, `rule_monsters_smell_magic`, `rule_seasons_bound_to_a_beast`, `rule_land_guards_lifeline`, `rule_shadows_move`, `rule_one_way_magic`, `rule_spells_feed_the_break`, `rule_born_with_magic`, `rule_geography_of_power`, `rule_half_spells`, `psign_smell`, `psign_frost`, `psign_restless_beasts`, `psign_compasses`, `psign_late_reflections`, `psign_wrong_shadows`, `psign_leaning_plants`, `psign_metal_taste`, `psign_hanging_dust`, `limit_not_on_sleepers`, `limit_cold_strengthens`, `limit_height_strengthens`, `limit_bloodline_resists`, `limit_institution_sign_stops`, `user_no_one`, `user_the_institution`, `user_born_here`

## `trope-breaks.yaml` — 31 rows

`break_rule_by_lottery`, `break_no_kings_only_guilds`, `break_war_is_ritual`, `break_weapons_one_class`, `break_magic_is_nobility`, `break_dragons_rule`, `break_border_forbidden`, `break_monsters_have_treaties`, `break_beasts_own_land`, `break_lineage_homes_inverted`, `break_gods_are_ancestors_known`, `break_moon_trades`, `break_divine_magic_holy_ground`, `break_god_name_forbidden`, `break_gods_among_mortals`, `break_night_is_safe`, `break_cities_dangerous`, `break_dungeons_inhabited`, `break_slayer_inherits`, `break_underground_forbidden`, `break_ruins_forbidden`, `break_night_forbidden`, `break_the_enemy_won`, `break_dead_month`, `break_lawless_day`, `break_iron_is_sacred`, `break_maps_are_illegal`, `break_no_direct_lies`, `break_no_writing`, `break_no_common_tongue`, `break_casting_forbidden`

## Readings the translation had to choose (for the audit)

Each line: the row, the field, the reading taken. The Turkish is in git history (the commit before build 13a) and in `docs/p1-foundation-rows.md`.

**Palette, spine, break**
- `land_*` names: the Turkish generic singular kept singular ("mountain", "lake"), not the plural labels; `land_volcanic` "volkanik" → "volcanic land".
- `spine_terraces` name "basamaklar" → "terraces"; travel "basamak basamak" → "step by step".
- `spine_barren_corridor`: "konaktan konağa" → "from halt to halt"; "han-şehir" → "caravanserai-city".
- `spine_above_below_sea` heart: "kıyı şehri ya da bir resif" → "the coastal city or a reef".
- `act_fell_from_sky`: "altında kaldı" → "was buried under" (the label says "crushed").
- `act_corrupted`: "bozuldu" → "was corrupted" (after the label).
- `scar_new_taboo`: "yasak" → "ban" (the label says "law").
- Every action keeps three English forms (past, present, imminent): the rendering's break line needs the tense.
- The time rows' `lead` phrases are gone with the Turkish sentence; `name` and `name_note` stay.

**Ruin source**
- `ruin_giants_and_dragons` what: a verbless fragment, rendered "there was war between two great lineages".
- `ruin_gods_quarrel` strangeness: "alan" → the god's domain.
- `ruin_great_flood` strangeness: "sualtı halkları" → "underwater peoples" (not narrowed to merfolk).
- `ruin_winged_mountains` strangeness: "yollarını" → "their roads", literally.
- `ruin_steppe_union` sites: "han mezarları" → khans' tombs; "at kaleleri" → "horse forts".
- `ruin_besieged_land` sites: "lağım tünelleri" → sappers' tunnels.
- `ruin_age_of_dragons` strangeness: "ejderha soyundan gelenler" → "those descended from dragons" (not narrowed to dragonborn).
- `ruin_dried_source` name: "the source that ran dry" (the label says "spring").

**Lifeline**
- `life_sea_folk_hunt`: "deniz halkı" → "the sea folk".
- `life_iron_coal`: "kömür" → "charcoal" (the weak point speaks of forests used up; the label says "coal").
- `life_winter_pass`, `life_caravan_inn`: "konak" → "lodging" / "the halt".
- `life_natural_harbour`, `life_strait_crossing`: "kılavuzlar" → "pilots".
- `life_flax_fields` yields "keten" → "linen"; in `life_river_flood` the same word → "flax".
- `life_tile_ceramics`: "çini" → "tile".
- `life_fey_bargain`: "karşılık aksarsa" → "if the payment falters"; "bereket" → "plenty".
- `life_dye_sources`: "kök boyaları" → "root dyes" (the label says "madder").
- `life_copper_mine`: "yeşil pas" → "green rust".

**Contest**
- `contest_capital_marches` b: "korucular" → "rangers"; "sınırın kopması" → "the marches breaking away".
- `contest_casters_casterless` third: "kaçak ustalar" → "illicit masters"; `contest_merchant_house_divides` fourth: "bir kaçak" → "a fugitive".
- `contest_shapeshifter`: "kılık değiştiren" → "the one in another guise" (the label says "The shapeshifter").
- `contest_fallen_state_remnant` name: "artığı" → "the leftover of a fallen state", to keep "the remnant" for the ruin's.
- `contest_land_sea_folk`: name "the people of the land and of the sea"; role b "the merfolk" (after its note).
- `contest_order_schism`, `contest_monster_bounty`: "tarikat" → "order".
- `contest_two_banks` third: "bent ustaları" → "weir masters".
- `contest_settlers_newcomers` escalation: "mahalle yangınları" → "quarter fires".
- `contest_sibling_rulers` fourth: "kız vermiş" → "has given a daughter in marriage to both siblings".
- `contest_lords_peasants` escalation: "angarya" → "forced labour".

**Signatures**
- `trait_first_changed` name_note: "merges with the 'new people' wound".
- `form_chartered`, `power_privilege`: "privileged company", "privilege: a right obtained from the government".
- `form_confederacy`: "confederacy of clans".
- `trait_giant_birds`, `trait_giant_insect_homes` name_note: "magic medium and above" (", or underground").
- `trait_raised_with_a_beast` at_table: "whoever harms someone's animal has harmed that person".
- `power_place` name_note: "a presence in a place".
- `practice_keep_the_one_road` gives: "caravan escorts". `practice_midwives` gives: "the marks of the children who are born".
- "görev" is "tasks" throughout the `gives` fields.

**Trope breaks**
- `break_beasts_own_land` at_table: "the forest has an owner, and a say".
- `break_divine_magic_holy_ground`: "rahip bir PC" → "a cleric PC"; "büyücü bir PC" elsewhere → "a spellcaster PC".

## Corrected at the audit (2026-10-04)

- `act_fell_from_sky`: the three forms say "crushed by something that fell from the sky" (the owner's approved wording).
- `contest_land_sea_folk` role b: "the sea folk"; merfolk stays in the note only.
- `contest_shapeshifter` name: "the shapeshifter", as its label.
- `life_iron_coal`: the label follows the text, "Iron and charcoal".
