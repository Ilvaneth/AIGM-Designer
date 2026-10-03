# Build item 8 — the three signature tables, redone to the tag review

*Written by the development (design and review) tab for the coding tab, 2026-10-03. The rulings are in `docs/p1-tags.md` (sections "the people signature", "the institution signature", "the phenomenon signature"); this file restates them with row ids. Where the two differ, stop and report.*

**The starting point** is the first version of item 8, written on 2026-09-29 and never committed. It sits in the stash `item8-signature-tables`: `data/design/signatures.yaml` (the new sub-tables `people_lineage`, `people_trait`, `people_attitude`, `institution_form`, `institution_practice`, `institution_sign`, `institution_power`, `phenomenon_rule`, `phenomenon_sign`, `phenomenon_limit`, `phenomenon_user`), `scripts/design_compare.py`, `tests/test_design_tables.py`, `tests/test_identity_tables.py`, and a note in `docs/campaign-designer-plan.md`. Bring it back, change it as below, and commit the whole as item 8.

**One green commit:** `Plan item 25, build 8: the signature tables`. The full suite green (the exit code), no commit before the development tab's audit, no push.

**Limits.**
- No roll logic: the people's role, the archetype heading, the forced form, the user roll for usable rules only are item 10. Item 8 is data and static tests.
- The old sub-tables `phenomenon`, `people` and `institution` stay until item 10 removes them with the old rolls.
- Legacy births keep loading; `test_regression_births` stays green.
- Run nothing that calls a model. The secret and villain tables are not touched.
- The stamp (`design_tables.py stamp`) now covers the eleven new sub-tables too: add them to the reviewed tables, write the stamps before the summary, commit them after the audit.

---

## The people signature

### Lineage (`people_lineage`, 16 rows; `avoid_used: false`, `row_wait: 1`)

No claims; weights only. The present weights stand. Added weights, ×3:

| Row | Weighs ×3 with |
|---|---|
| `lineage_giant_kin` | `life_giant_peace`, `contest_humans_giants`, `ruin_giants_land`, `ruin_giants_and_dragons` |
| `lineage_fey` | `life_fey_bargain`, `contest_humans_fey`, `ruin_elven_withdrawal` |
| `lineage_merfolk` | `life_sea_folk_hunt`, `contest_land_sea_folk`, `spine_above_below_sea`, `ruin_great_flood` |
| `lineage_goblinoid` | `break_monsters_have_treaties` |

(The forced and weighted lineages of a people's role are already data on the contest roles, build 7c-2; item 10 applies them and "lineage homes are inverted".)

### Traits (`people_trait`: 39 rows)

**Twelve rows leave:** `trait_adult_names`, `trait_lies_foul_the_air`, `trait_iron_is_unlucky`, `trait_winter_sleep`, `trait_two_homes`, `trait_never_stop`, `trait_seven_year_rotation`, `trait_one_great_building`, `trait_guest_three_days`, `trait_one_envoy`, `trait_herd_dreams`, `trait_live_on_water`.

**One row joins:** `trait_sacred_animal`, family `belief`, kind `behaving`; `tr.name` "bir hayvanı kutsal sayarlar; onu öldüren sürülür"; `tr.at_table` "kutsal hayvana dokunan bütün halkı karşısında bulur"; a hook `{phase: P5, must: "the sacred animal is never the one the lifeline kills"}`.

By family afterwards: body 7, custom 5, creature bond 6, belief 6, social order 5, relation to the break 7, place and movement 3; 16 visible and 23 behaving.

No claims and no clash on any trait. The requirements already in the data stay (palette kinds, the magic gate, the "since the break" rows not drawn under `time_coming`).

**Weights:**

| Row | Weight |
|---|---|
| `trait_underground_by_day` | ×2 with `break_night_is_safe` |
| `trait_fled_the_break` | ×3 with `scar_people_displaced` |
| `trait_first_changed` | ×3 with `scar_new_people` (in the data) |
| `trait_bee_council` | ×3 with `life_bee_forests` |
| `trait_giant_insect_homes` | ×3 with `life_giant_insects` |
| `trait_giant_birds` | ×3 with `life_griffon_eyries` |
| `trait_hunt_with_wolves` | ×2 with `life_deer_migration` |
| `trait_dolphin_fishers` | ×2 with `life_fish_run`, `life_oyster_beds` |
| `trait_mountain_spirits` | ×2 with `life_copper_mine`, `life_iron_coal`, `life_quarry`, `life_gemstones` |
| `trait_workshops_not_families` | ×2 with a lifeline of the family `craft` |
| `trait_history_danced` | ×2 with `break_no_writing` |

### Attitude (`people_attitude`, 6 rows)

No tags. One weight: `stranger_merchant` ×2 with `trait_haggling_art` (the attitude is rolled after the traits).

---

## The institution signature

**The role's archetype is the heading.** The institution is a contest role; its form, its practice and its power are drawn only from the rows that list the role's archetype (`state`, `religious`, `martial`, `guild`, `trade`, `scholarly`, `criminal`, `resistance`). In the data that is one field per row, `hints: [...]`, read as a requirement (item 10 applies it). The form table's `hint_weight` goes.

### Forms (`institution_form`, 14 rows; may repeat)

| Row | `hints` |
|---|---|
| `form_order` | religious, martial, scholarly |
| `form_guild` | guild, trade |
| `form_company` | martial |
| `form_house` | state, guild, trade, criminal |
| `form_council` | state |
| `form_league` | trade, guild, criminal |
| `form_school` | scholarly |
| `form_brotherhood` | resistance, religious, guild, martial, criminal |
| `form_cloister` | religious, scholarly |
| `form_travelling` | guild, trade, criminal, resistance |
| `form_society` | criminal, scholarly, resistance |
| `form_chartered` | trade |
| `form_confederacy` | state, martial, resistance |
| `form_militia` | martial, resistance |

`form_chartered`: `tr.name` → "imtiyazlı şirket" (a written charter clashed with "writing is unknown"); `form_word` → "Trading Company". The English form words are settled with the names (item 11); list in your summary any you think collide.

### Practices (`institution_practice`: 33 rows; not drawn again across campaigns)

**Seven rows leave:** `practice_wall_builders`, `practice_empty_temples`, `practice_guard_the_herds`, `practice_lifeline_craft`, `practice_raise_the_orphans`, `practice_mend_the_wound`, `practice_watch_the_sky`.

**`hints` of the 33:**

| Row | `hints` |
|---|---|
| `practice_hold_the_key_place` | state, martial, guild |
| `practice_keep_the_one_road` | state, martial, guild |
| `practice_hold_the_remnant_gate` | religious, martial, scholarly |
| `practice_players` | guild, resistance, criminal |
| `practice_pilots` | guild, trade, criminal |
| `practice_couriers` | state, guild, trade |
| `practice_caravan_masters` | trade, guild |
| `practice_ferrymen` | guild, trade, criminal |
| `practice_keep_the_old_works` | guild, scholarly, state |
| `practice_golem_founders` | guild, scholarly, martial |
| `practice_ship_and_bridge` | guild, trade |
| `practice_mapmakers` | scholarly, guild, state, criminal |
| `practice_study_the_remnant` | scholarly, religious |
| `practice_seek_the_lost` | scholarly, religious |
| `practice_keep_the_dying` | scholarly, religious, resistance |
| `practice_healers` | religious, guild, scholarly, resistance |
| `practice_keep_the_granaries` | state, religious, guild |
| `practice_midwives` | religious, guild |
| `practice_herd_healers` | guild, religious |
| `practice_monster_hunters` | martial, guild, resistance |
| `practice_border_riders` | martial, state |
| `practice_champions` | martial, state |
| `practice_free_company` | martial, trade, criminal |
| `practice_dragon_giant_hunters` | martial |
| `practice_royal_monopoly` | trade, guild, state |
| `practice_sell_the_remnant` | trade, criminal, scholarly |
| `practice_sole_seller` | trade, guild |
| `practice_foreign_house` | trade |
| `practice_smugglers_union` | criminal, trade |
| `practice_keep_the_lifeline_rite` | religious |
| `practice_pilgrim_guides` | religious, trade |
| `practice_guard_the_holy_place` | religious, martial |
| `practice_worship_the_break` | religious, resistance |

Rows per archetype, to hold in a test: guild 18, religious 12, trade 12, martial 10, state 9, scholarly 9, criminal 7, resistance 5. None may fall under five.

**Text changes** (so that no rule is needed):

| Row | Change |
|---|---|
| `practice_champions` | `tr.name` → "anlaşmazlıkları teke tek dövüşle çözen şampiyonlardır" |
| `practice_royal_monopoly` | `tr.name` → "bir malın tekelini tutarlar"; rename the id `practice_monopoly`, the label without "royal" |
| `practice_study_the_remnant` | what it gives the party → "kazı görevleri, eski bilginin çözülmesi" |
| `practice_keep_the_old_works` | `tr.name` → "kalıntının yapılarını onarıp çalışır tutarlar" |
| `practice_couriers` | what it gives the party → "haberler, yetiştirilmesi gereken acil işler" |
| `practice_dragon_giant_hunters` | `tr.name` → "ejderha avlarlar"; what it gives → "büyük av, ejderhanın hazinesi"; rename the id `practice_dragon_hunters`; its weight list keeps the dragon rows only (`life_dragon_protection`, `contest_humans_dragon`, `ruin_age_of_dragons`, `ruin_giants_and_dragons`, `break_dragons_rule`) |

**Two clashes:** `practice_hold_the_remnant_gate` conflicts with `contest_sealed_remnant` (its side b already holds the gate); `practice_guard_the_holy_place` conflicts with `contest_one_shrine`.

**Weights, ×3:** `practice_pilots` with `break_maps_are_illegal`; `practice_border_riders` with `break_border_forbidden`; `practice_sell_the_remnant` and `practice_hold_the_remnant_gate` with `break_ruins_forbidden`; `practice_champions` with `break_war_is_ritual`; `practice_pilgrim_guides` with `life_pilgrim_road`; `practice_worship_the_break` with `scar_new_belief` (in the data).

**Four practices name their own form** (a field `form`, applied by item 10: the form is then not rolled): `practice_players` → `form_travelling`; `practice_free_company` → `form_company`; `practice_smugglers_union` → `form_society`; `practice_foreign_house` → `form_house`.

### Signs (`institution_sign`: 13 rows; may repeat; rolled freely, no tags)

**Five rows leave:** `isign_unarmed`, `isign_no_marriage`, `isign_own_no_land`, `isign_kneel_to_no_one`, `isign_no_night_travel`. `isign_own_language` keeps its requirement (standard and epic).

### Power sources (`institution_power`, 10 rows; may repeat)

| Row | `hints` |
|---|---|
| `power_monopoly` | trade, guild, state |
| `power_place` | state, martial, religious, scholarly |
| `power_knowledge` | scholarly, criminal, guild, trade, resistance |
| `power_arms` | martial, state, criminal, resistance |
| `power_love` | resistance, religious, guild |
| `power_sanctity` | religious |
| `power_treasure` | trade, guild, state, criminal |
| `power_creature_bond` | martial, religious, scholarly, resistance |
| `power_charter` | guild, trade, scholarly, martial |
| `power_fear` | criminal, martial, state |

`power_charter`: `tr.name` → "imtiyaz: yönetimden alınmış bir hak"; rename the id `power_privilege`.

---

## The phenomenon signature

### Rules (`phenomenon_rule`, 40 rows; all stay)

**Every rule carries its kind** (a field `kind`; item 10 rolls the user for the usable ones only):

| Kind | Rows |
|---|---|
| `spell` (15): whoever casts uses it | `rule_echo`, `rule_rebound`, `rule_inverted_element`, `rule_spells_grow_life`, `rule_spell_twins`, `rule_kin_doubles`, `rule_spell_marks`, `rule_delayed_spells`, `rule_casting_ages`, `rule_gesture_magic`, `rule_monsters_smell_magic`, `rule_one_way_magic`, `rule_spells_feed_the_break`, `rule_geography_of_power`, `rule_half_spells` |
| `usable` (6): the user is rolled | `rule_mirror_doors`, `rule_true_names`, `rule_signs_are_spells`, `rule_tongue_of_magic`, `rule_metal_wakes`, `rule_shared_wounds` |
| `self` (19): no one uses it | the other nineteen |

Two usable rules fix their user (a field `users`, the allowed user rows): `rule_tongue_of_magic` → `user_the_people`; `rule_shared_wounds` → `user_the_people`, `user_the_institution`.

**Four rules carry a rule:**
- `rule_beasts_sense_lies` conflicts with `break_no_direct_lies`.
- `rule_night_distances`, `rule_seasons_bound_to_a_beast`, `rule_feelings_make_weather` are not drawn when the era is `underground`.

**Weights, ×2:** `rule_echo` with `break_casting_forbidden`; `rule_tongue_of_magic` with `break_no_common_tongue`.

**Cleanup:** `rule_true_names` loses its weight on `trait_adult_names` (the trait left).

### Limits (`phenomenon_limit`: 8 rows; may repeat)

**Four rows leave:** `limit_remnant_matter_absorbs`, `limit_underground_only`, `limit_once_a_day`, `limit_a_day_from_remnant`. One weight: `limit_iron_cuts` ×2 with `break_iron_is_sacred`.

### Signs and users (`phenomenon_sign` 16 rows, `phenomenon_user` 8 rows)

Unchanged, no tags.

---

## Tests

- The removed ids appear nowhere in the committed data.
- The counts above (39 traits by family and kind; 33 practices per archetype; 13 signs; 8 limits; the rule kinds 15, 6 and 19).
- Every `hints` value is one of the eight archetypes; every archetype holds at least five practices, at least three forms and at least three powers.
- Every row id a weight, a clash or a `users` / `form` field names exists.
- The claims tests of 7c still pass with the new sub-tables loaded (no trait, practice, sign, power, rule, limit or user carries a claim).
- `design_compare.py` treats the traits, the practice and the rule as tables whose rows are not drawn again (as the first version did).
- The stamps cover every row of the eleven sub-tables.

## The summary

Changed files; new and changed tests; the suite's count and exit code; the stamp's changed rows; anything unexpected; the form words you think collide.
