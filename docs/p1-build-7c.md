# Build item 7c — the claims system and the table changes of the tag review

*Written by the development (design and review) tab for the coding tab, 2026-10-03. The rulings behind every line are in `docs/p1-tags.md` (the owner approved each of them); this file restates them with row ids so that nothing has to be mapped by guesswork. Where this file and `docs/p1-tags.md` differ, stop and report. Row ids are the committed ones (`foundation.yaml`, `trope-breaks.yaml`, `tensions.yaml`, `dials.yaml`).*

**Three parts, three green commits, in this order.** After each part: the full suite green (the exit code), no commit, a summary to the owner; the commit follows the development tab's audit.

| Part | What | Commit message |
|---|---|---|
| 7c-1 | the mechanism | `Plan item 25, build 7c-1: claims, tokens, overridable defaults` |
| 7c-2 | the foundation tables | `Plan item 25, build 7c-2: the foundation tables under the claims` |
| 7c-3 | the trope breaks and the question | `Plan item 25, build 7c-3: the trope breaks and the question under the claims` |

**Limits for all three parts.**
- Item 8's work (the signature tables) is not part of 7c; it is redone afterwards under its own instruction. Keep it out of these commits and keep it from being lost, as in 7b.
- No roll logic of step 2 is built here (the people's role, the institution's heading, the question's heading, the forced tie, the prohibition drawn first): that is item 10. 7c is data, the arbiter's reading of it, and tests.
- An override is data only. Nothing applies it yet; the floor that owns the overridden default applies it at its own turn.
- Legacy births and the fixture keep loading; `test_regression_births` and `test_foundation_roll` stay green. A `used.json` that names a removed row must not break anything.
- Do not write the plan. Run nothing that calls a model.
- The secret and villain tables are not touched; no secret row id is printed in a summary.

---

## Part 7c-1 — the mechanism

### 1. The registry: `data/design/claims.yaml`

A closed registry with three lists.

**Topics and values (six topics):**

| Topic | Values |
|---|---|
| `rule` (the land's rule) | `hereditary`, `throne`, `by_lot`, `guild_council`, `dragon_sovereign` |
| `nobility` | `exists`, `none` |
| `below_ground` | `lived_in` |
| `writing` | `printed` |
| `magic` (how plentiful) | `scarce`, `middling`, `plentiful`, `faded` |
| `war` | `by_armies`, `by_champions` |

**Clashes, declared pair by pair. Two values of one topic never clash by default.**

| Claim | Claim |
|---|---|
| `nobility=exists` | `nobility=none` |
| `rule=hereditary` | `rule=by_lot` |
| `rule=hereditary` | `rule=guild_council` |
| `rule=hereditary` | `rule=dragon_sovereign` |
| `rule=throne` | `rule=guild_council` |
| `magic=plentiful` | `magic=faded` |
| `war=by_armies` | `war=by_champions` |

`rule=throne` clashes with neither `by_lot` nor `dragon_sovereign`.

**Overridable defaults.** A default is something a dial effect, a scale number, a quota or a later phase's roll sets, which a rolled row may rewrite. Each has an id, the phase that owns it and one line of description. The ids this build needs (name them as you see fit, keep one list): the scale's forced state faction (P4); the state faction's leader, its identity and its succession rule (P4); the ruler NPC's heir field (P5); the caster share (P5); the magic regulator's strictness (P2); who the magic regulator is (P2); the pantheon type (P2); the great gods' lower bound (P2); the era's equipment rule (P3); the era's "seat of rule" anchor (P3); the travel tables' danger default (P3); the politics mix's node kinds (P7); the war mix's node kinds (P7); a contest's last escalation step (P7); martial factions' assets (P4); a site's attitude pool (P6); the loot's scrolls and the spellbook (P6); the player map (P8); the primer's line on casting in public (P8); the second language (names, item 11); the weekly volatility budget (slice 2); the lineage roll's palette weights (P1, item 10).

### 2. Claims on rows, tokens in the context

- A row may carry `claims: {topic: value, ...}`. A contest role may carry `claims` too (inside `roles.<key>`).
- A rolled row's claims enter the arbiter's context as tokens `claim:<topic>=<value>`. The dial rows' claims enter when the context is built from the dials. A token set by a secret row keeps the secret flag, with the same care 7a gave the die: an exclusion that names it goes to the secret side.
- A row conflicts with every token whose claim clashes with one of its own claims (derived from the registry when the tables load, into the same symmetric conflict index the arbiter already reads).
- A row may also name a token directly in `conflicts_with`, `requires`, `none_of` and `weight_by` (a prohibition row claims nothing, yet clashes with `claim:below_ground=lived_in`).
- **A role's claim counts only when the scale seats that role.** The foundation roller adds a role's tokens after the contest draw, for the seated roles only (epic's second contest: its three roles).
- **Two tokens come from the layout,** added after `lay_out`: `claim:below_ground=lived_in` when the heart sits on `land_underground`; `layout:remnant_on_heart` when the remnant lies on the heart.
- `conflicting_pairs` and the door's recheck expand tokens, so the final set is checked on claims too.
- `arbitrate()` keeps its signature.

### 3. The condition grammar

A `requires` must be able to say "the palette holds one of these kinds **and** the lifeline is one of these rows" (part 7c-2 needs it). Today a mapping holds one `any_of`. Extend the grammar as you judge best (document it in `data/design/README.md`), keep the existing forms valid.

### 4. Overrides as data

- A row may carry `overrides: [{default: <id>, to: <text or value>}]`.
- Tests: every `default` is in the registry; when two rows override the same default and can be rolled together, the registry holds a written `combine` line for the pair (or the two rows clash, or `families_distinct` keeps them apart).
- `trope-breaks.yaml` holds two old unread `overrides` fields: the ancestor gods' (`pantheon_type`) becomes the new relation in part 7c-3; the moon traders' (`era_bias`) is deleted there.

### 5. Inspection

- **A per-row reviewed stamp.** A stamp file (for example `data/design/reviewed.json`: row id → a hash of the row's content) and a command that writes it. A test fails when a row of a P0 or P1 table has no stamp or a stamp that no longer matches. The stamp is written only after the development tab's audit; say in your summary which command writes it.
- **The floor.** A test helper that rolls many seeds and reports each table's smallest pool after the constraints. For a table whose rows are not drawn again across campaigns, a pool under five is a failure. Tables whose rows may repeat (the tie, the time, the palette) are exempt.

### 6. The P0 claims and the spine's (data of this part)

| Row | Claim |
|---|---|
| `era_renaissance` | `writing=printed` |
| `era_underground` | `below_ground=lived_in` |
| `magic_low` / `magic_medium` / `magic_high` | `magic=scarce` / `middling` / `plentiful` |
| `spine_three_depths`, `spine_mountain_within` | `below_ground=lived_in` |

No other dial row and no other spine or palette row carries a claim.

### Tests of 7c-1

The registry is closed (a row's claim outside it fails); a clash pair excludes in both directions; no default clash inside a topic; a role's claim is silent when the role is not seated; the two layout tokens appear only in their cases; a secret row's token never shows in the public record; the stamp test; the floor helper.

---

## Part 7c-2 — the foundation tables

### Palette (`foundation.yaml#palette`)

- `land_glass_desert` `tr.what` → "kumu cama dönmüş bir çöl". `land_giant_bones` `tr.what` → "dev bir iskeletin üstünde ve içinde kurulmuş toprak". (They named an event that was never rolled.)
- A new common hook: `{phase: P2, must: "the origin of every fantastic kind the ruin source did not bring is written"}`.

### Ruin source (`#ruin_source`)

- `ruin_age_of_mages`: `claims: {magic: faded}`. It is then not drawn at magic `high`; its ×2 at `low` stays.
- The plane promise on four rows, `{phase: P2, must: "this row's plane is chosen among the touched planes; the planes the foundation names are shared to fit the scale's count"}`: `ruin_planar_rift` (replacing its present P2 hook), `ruin_planar_invasion`, `ruin_celestial_war`, `ruin_elven_withdrawal`.

### Lifeline (`#lifeline`)

- `life_binding_marriage`: `claims: {nobility: exists, rule: hereditary}`. No other lifeline carries a claim.

### Contest (`#contest`)

**Claims.**

| Row | Claims |
|---|---|
| `contest_two_heirs` | `nobility: exists`, `rule: hereditary` |
| `contest_empty_throne` | `nobility: exists`, `rule: hereditary` |
| `contest_sibling_rulers` | `rule: hereditary` |
| `contest_old_order_reform` | `nobility: exists` |
| `contest_occupier_resistance` | on the role `third`: `nobility: exists` |
| `contest_capital_marches` | `nobility: exists` |
| `contest_lords_peasants` | `nobility: exists` |
| `contest_treasure_race` | `rule: throne` |
| `contest_first_settlers` | `rule: throne` |
| `contest_humans_giants` | `rule: throne` |
| `contest_humans_fey` | on the role `fourth`: `nobility: exists` |
| `contest_war_fed_company` | `war: by_armies` |

**The prize and the lifeline.** Eight rows require one of the listed lifelines, in addition to the palette requirement they already carry, and weigh ×3 when the requirement holds (which, once required, is always: write it as the row's weight under that condition so the row stays as likely as today inside its heading).

| Row | Lifelines |
|---|---|
| `contest_one_harbour` | `life_natural_harbour`, `life_strait_crossing`, `life_shipbuilding`, `life_fish_run`, `life_oyster_beds`, `life_sea_folk_hunt`, `life_dye_sources`, `life_amber_shores` |
| `contest_one_pasture` | `life_yak_herds`, `life_horse_herds`, `life_deer_migration`, `life_wheat_plain`, `life_carpet_weaving`, `life_leather_armour`, `life_vineyards`, `life_flax_fields` |
| `contest_two_banks` | `life_snowmelt`, `life_river_flood`, `life_shared_water_right`, `life_river_ford`, `life_flax_fields`, `life_tile_ceramics`, `life_fish_run` |
| `contest_old_new_craft`, `contest_share_keep_knowledge`, `contest_split_family` | every lifeline of the family `craft` |
| `contest_mine_owners_miners` | `life_copper_mine`, `life_iron_coal`, `life_quarry`, `life_gemstones`, `life_peat_bog`, `life_famous_steel` |
| `contest_open_close_road` | every lifeline of the family `passage`, and `life_pilgrim_road` |

`contest_one_shrine` gets no requirement; it weighs ×2 when the ruin source is of the family `gods`.

The measurement to reproduce is `docs/reports/tags-grouping-analysis-1/scripts/prize_fit.py` (3,000 seeds: mismatches 18.6 % → 0, the contest pool never under 27 of 40, every row still drawn).

**Other changes.**
- `contest_two_branches`: role `a` `tr` → "eski çöküşü bir ceza sayan kol"; role `b` stays "onu bir fırsat sayan kol". (Its sides were defined by the break, which is rolled later.)
- `contest_casters_casterless`: `overrides` the regulator (who: side a) and the regulator's strictness (strict).
- **The people's role.** Ten roles get `people_role: true` (item 10 reads it):

| Row | Role | Lineage (item 10) |
|---|---|---|
| `contest_humans_giants` | `b` | `lineage_giant_kin`, forced |
| `contest_humans_fey` | `b` | `lineage_fey`, forced |
| `contest_land_sea_folk` | `b` | `lineage_merfolk`, forced |
| `contest_surface_deep` | `b` | `lineage_dwarf`, `lineage_gnome`, `lineage_goblinoid` ×3 |
| `contest_mine_owners_miners` | `fourth` | `lineage_dwarf`, `lineage_gnome`, `lineage_goblinoid` ×3 |
| `contest_treasure_race` | `third` | rolled |
| `contest_first_settlers` | `third` | rolled |
| `contest_new_resource` | `third` | rolled |
| `contest_two_banks` | `fourth` | rolled |
| `contest_forbidden_lands` | `fourth` | rolled |

Write the lineage column as data on the role (`lineage_forced` / `lineage_weight`); nothing reads it before item 10.

### The break (`#action`, `#scar`, `#time`)

- **"Coming" and the break's products.** `time_coming` conflicts with `scar_new_people` and `scar_magic_rule_changed` (time is rolled after the scars, so `time_coming` leaves the pool).
- **The underground era.** `scar_sky_changed`, `scar_seasons_broken` and `act_fell_from_sky` are not drawn when the era is `underground`.
- **The plane promise** (the same hook as the four ruin rows) on `act_merged_with_plane` and `scar_plane_thinned`.
- **Every scar names its targets.** The generic hooks ("the map, peoples, polities, economy or law carry this scar", "the cosmos carries this scar" and the like) are replaced, one hook per phase:

| Scar | Hooks |
|---|---|
| `scar_new_land_kind` | P1: a fantastic kind joins the palette. P3: the kind is a map node |
| `scar_roads_changed` | P3: the map's edges and main line show the change |
| `scar_cursed_belt` | P3: a region or belt is poisoned or cursed. P6: a site and its creatures stand in it |
| `scar_unreachable_region` | P3: a region is marked closed. P7: a later act opens it |
| `scar_magic_rule_changed` | P1: the phenomenon signature is this rule. P2: the magic system carries it |
| `scar_god_changed` | P2: that god is changed in the pantheon |
| `scar_plane_thinned` | P2: the touched plane's border is thin (with the plane promise) |
| `scar_sky_changed` | P2: the calendar carries the change |
| `scar_seasons_broken` | P2: the climate and the calendar carry the change |
| `scar_time_flow_changed` | P2: a magic or plane rule names it. P3: the region where time runs differently |
| `scar_people_displaced` | P3: a refugee settlement. P5: NPCs of that people |
| `scar_new_people` | P1: the people signature may be this people. P5: NPCs of that people |
| `scar_state_fell` | P3: one polity's status is fallen; the fallen state is never the polity a seated contest role rules, and P3 names it. P4: a faction wants the void |
| `scar_creatures_changed` | P6: the creature ecology carries the change |
| `scar_new_resource` | P3: the goods hold the new resource. P4: the contest's prize, when the prize is `new`, is this resource |
| `scar_lost_knowledge` | P3: a trade or good is missing. P6: a ruin keeps it |
| `scar_new_taboo` | P1: one trope break is drawn from the prohibition rows. P3: the law carries the taboo |
| `scar_new_belief` | P2: the belief has its place in the pantheon. P4: a faction holds it |

- **The foundation sentence** (`design_foundation.py`): under `time_coming` the scar label is "İlk izleri:" in place of "Yarası:" / "Yaraları:".

### Tests of 7c-2

`test_foundation_roll` grows: over its seeds no clash pair of this file stands together; no birth holds a prize contest with a lifeline outside its list; `time_coming` never stands with the two product scars; the underground era never draws the two scars or the action; magic `high` never draws `ruin_age_of_mages`; no pool is empty; the floor helper reports the contest pool.

---

## Part 7c-3 — the trope breaks and the question

### Rows that leave `trope-breaks.yaml` (eight)

`break_sacred_beast`, `break_humans_minority`, `break_world_is_young`, `break_children_are_rare`, `break_elves_are_new`, `break_goblins_are_merchants`, `break_gods_need_witnesses`, `break_giants_are_peasants`.

Every reference to them goes too: the `conflicts_with` on `break_elves_are_new`'s side of `ruin_elven_withdrawal`, any weight list that names one (item 8's uncommitted `signatures.yaml` names some; leave that file to item 8 and list the names in your summary), any test, `forbidden.yaml`'s exceptions if one names a removed row.

### Rows that join (six)

Each gets `tr` (name and at_table as given), a one-sentence English `statement`, and the hooks below.

| id | family | `tr.name` / `tr.at_table` | Hooks |
|---|---|---|---|
| `break_no_common_tongue` | knowledge | "ortak dil yoktur; her halk kendi dilini konuşur" / "dil ve tercüman her sosyal sahnede önem kazanır" | P5: every NPC carries the languages it speaks; at least one NPC is an interpreter. P8: the primer says which tongue is spoken where |
| `break_gods_among_mortals` | gods | "tanrılar ölümlülerin arasında yaşar; her birinin bir evi vardır ve kapısı çalınır" / "parti bir tanrıyla yüz yüze konuşabilir" | P2: each great god has a house and receives petitioners; a fallen god's house stands empty or shut. P3: the god's house is a map node. P6: a god's house is no dungeon and a god is no boss. P8: the primer says how a god is addressed |
| `break_lawless_day` | time | "yılda bir gün hiçbir yasa geçerli değildir" / "o gün takvimde bellidir; herkes ona göre plan yapar" | P2: the calendar names the day, inside the campaign's span. P4: every faction has a plan for the day. P7: one beat falls on it. P8: the primer says what natives do that day |
| `break_casting_forbidden` (prohibition) | knowledge | "büyü yapmak yasaktır; büyücüler gizlenir" / "büyücü bir PC suçludur; her büyü bir risk" | P3: the law ladder punishes casting; the gods' magic is outside the ban. P4: one faction hunts casters and another shelters them. P5: caster NPCs hide what they are. P8: the primer says what befalls a caught caster |
| `break_ruins_forbidden` (prohibition) | danger | "harabelere girmek yasaktır; kalıntıya dokunan suçludur" / "her zindana yasaya karşı girilir; ganimet kaçak maldır" | P3: the ways to the ruins are watched. P4: one faction guards the ruins and another sells what comes out. P6: every ruin site is entered against the law; its loot needs a fence. P8: the primer says what natives say of the ruins |
| `break_night_forbidden` (prohibition) | danger | "gece dışarı çıkmak yasaktır; gece nöbetçilerindir" / "gece sahneleri suç olur; devriyeler ve izinler oyuna girer" | P3: settlements shut their gates at dusk. P4: the night watch is a faction or a faction's asset. P5: an NPC works by night against the law |

The table then holds 31 rows: governance 7, peoples 3, gods 5, danger 7, time 3, knowledge 6; eight prohibitions (`break_weapons_one_class`, `break_border_forbidden`, `break_god_name_forbidden`, `break_underground_forbidden`, `break_ruins_forbidden`, `break_night_forbidden`, `break_maps_are_illegal`, `break_casting_forbidden`).

### Claims, clashes, overrides and fits, row by row

"Clashes" lists what is not already given by the registry. A fit is a weight (`weight_by`) on the trope row, read against the rolled foundation.

| Row | Claims | Further clashes | Overrides | Fits |
|---|---|---|---|---|
| `break_rule_by_lottery` | `rule: by_lot` | `tension_inheritance_merit` (in the data) | the state faction's succession rule; the ruler NPC's heir field; the politics mix's node kinds (`succession`, `election` → the day of the draw) | |
| `break_no_kings_only_guilds` | `nobility: none`, `rule: guild_council` | | the scale's forced state faction (archetype guild); the "seat of rule" anchor (a guild hall); the politics mix's node kinds (`succession` → the choosing of masters) | ×2 with a contest whose role `a` or `b` has the hint `guild` |
| `break_war_is_ritual` | `war: by_champions` | | a contest's last escalation step (a challenge of champions); the war mix's node kinds (duel, the choosing of champions, parley, raid); martial factions' assets (champions) | |
| `break_weapons_one_class` | | | | ×2 with `contest_lords_peasants` |
| `break_magic_is_nobility` | `nobility: exists` | `break_casting_forbidden` | who the regulator is (the nobility); the caster share (as many as the nobles); the primer's line (what a commoner risks by casting) | ×2 with `contest_casters_casterless` |
| `break_dragons_rule` | `rule: dragon_sovereign` | | the state faction's leader (a dragon) | ×2 with `life_dragon_protection` |
| `break_border_forbidden` | | | | ×2 `spine_long_wall`; ×3 `contest_open_close_road`; ×2 `contest_forbidden_lands` |
| `break_monsters_have_treaties` | | | a site's attitude pool on the treaty people's lairs (negotiate; the horror mix's "test or enslave" site is never one of them) | ×2 with `life_giant_peace`, `life_dragon_protection`, `life_fey_bargain`, `life_sea_folk_hunt` and the contests of the family `nonhuman` |
| `break_beasts_own_land` | | | | |
| `break_lineage_homes_inverted` | | | the lineage roll's palette weights (inverted) | |
| `break_gods_are_ancestors_known` | | `ruin_dead_god` | the pantheon type (ancestor gods) | ×2 with `ruin_failed_apotheosis` |
| `break_moon_trades` | | | | ×2 when the era is `nautical` |
| `break_divine_magic_holy_ground` | | | | ×2 with `contest_one_shrine`, `life_pilgrim_road` |
| `break_god_name_forbidden` | | | | ×2 with `ruin_imprisoned_god`, `ruin_departed_god` |
| `break_gods_among_mortals` | | | the great gods' lower bound (at least 1); the pantheon type (the silent-gods and dead-gods types leave) | ×2 with a ruin of the family `gods` |
| `break_night_is_safe` | | not drawn in the underground era | | |
| `break_cities_dangerous` | | | the travel tables' danger default (the wild is safe) | ×2 with `spine_edge_of_civilisation` |
| `break_dungeons_inhabited` | | | a site's attitude pool (`att_kill` and `att_ignore` leave) | |
| `break_slayer_inherits` | | | | ×2 with `contest_monster_bounty` |
| `break_underground_forbidden` | | the token `claim:below_ground=lived_in` (the underground era, the two spines, a heart on `land_underground`) | | ×2 when the palette holds `land_underground`; ×2 with `life_deep_lake`, `life_deep_mouth`, `life_mushroom_fields`, `life_giant_insects`, `life_gemstones` |
| `break_ruins_forbidden` | | the token `layout:remnant_on_heart` | | ×3 with `contest_sealed_remnant`; ×2 with `contest_forbidden_lands`, `contest_treasure_race` |
| `break_night_forbidden` | | not drawn in the underground era | | |
| `break_the_enemy_won` | | | the state faction's identity (the victors) | ×3 with `contest_occupier_resistance`; ×2 with `ruin_besieged_land` |
| `break_dead_month` | | | the weekly volatility budget (doubled in that month) | |
| `break_lawless_day` | | | | |
| `break_iron_is_sacred` | | | the era's equipment rule (iron goods ×5 and licensed) | ×2 with `life_copper_mine`, `life_iron_coal`, `life_famous_steel`, and when the era is `ancient` |
| `break_maps_are_illegal` | | | the player map (only the primer's named places) | ×2 when `exploration` is in the content mix; ×2 with `contest_treasure_race` |
| `break_no_direct_lies` | | | | |
| `break_no_writing` | | the token `claim:writing=printed` (the renaissance era) | the loot's scrolls and the spellbook (knots, memory or signs) | |
| `break_no_common_tongue` | | | the second language (the contest's other side's) | |
| `break_casting_forbidden` | | not drawn at magic `high`; `break_magic_is_nobility` | the regulator's strictness (strictest); who the regulator is (the hunters) | ×2 at magic `low`; ×2 with `contest_casters_casterless` |

### Merge rules, written as data on the trope row (`merges_with`, applied by item 10)

| Pair | The written answer |
|---|---|
| `break_dragons_rule` + `contest_humans_dragon` | role `b` takes the hint `state` (the sovereign dragon and its household); role `a` takes `resistance`; `third` and `fourth` stay |
| `break_the_enemy_won` + `contest_occupier_resistance` | the victors are role `a`; role `third` is the state faction under them |
| `break_iron_is_sacred` + `life_iron_coal` or `life_famous_steel` | the lifeline's smiths are the iron priesthood |
| `break_magic_is_nobility` + `contest_casters_casterless` | role `a` is the nobility; one regulator |
| `break_casting_forbidden` + `contest_casters_casterless` | role `a` is the ban's licensed exception and its enforcer; one regulator |

These five are also the `combine` lines of the registry where two rows override one default.

### Text and hook changes on kept rows

| Row | Change |
|---|---|
| `break_beasts_own_land` | becomes the beast-people. `label` "Some lands' lord is a beast-person"; `statement` "A born lineage is both beast and person and holds land; a wood may have a lord who is a stag and walks as a man."; `tr.name` "bazı toprakların beyi bir hayvan-insandır"; `tr.at_table` stays. The row says nothing of a curse, contagion or alignment. P3 hook: "a beast-lord holds one part of the map; its travel table is negotiated passage". P4 hook stays |
| `break_monsters_have_treaties` | `statement`: "sealed treaties" → "sworn treaties" |
| `break_moon_trades` | P4 hook: "a trade faction holds the right to the moon trade"; the P2 hook gains the plane promise (the moon is one of the touched planes; shared to fit the scale's count); the old `overrides: {era_bias: ...}` field is deleted |
| `break_dungeons_inhabited` | P6 hook: "every site's inhabitants answer the door; no site's attitude is kill or ignore". P5 hook: "a site detailed at birth has a named householder; every other site names its householder in one sentence of the site row" |
| `break_night_is_safe` | P6 hook: "the ecology's apex hunts by day" |
| `break_gods_are_ancestors_known` | its old `overrides: {pantheon_type: ...}` becomes the new relation |
| every row | the unread `tags` field is deleted; `prohibition: true` stays |

### The tie sub-table

- `tie_break` conflicts with `time_coming`. (Item 10 adds the two roll rules: a fit bond sets the tie; the scar's prohibition is tied to the break even under "coming".)

### The question (`tensions.yaml`)

Six rows gain one family each (no new row); the heading itself is item 10's roll.

| Row | Gains the family |
|---|---|
| `tension_winning_being_right` | `two_hands` |
| `tension_ambition_contentment` | `two_hands` |
| `tension_justice_peace` | `two_hands` |
| `tension_power_self` | `hidden_hand` |
| `tension_one_many` | `hidden_hand` |
| `tension_security_freedom` | `hidden_hand` |

### Tests of 7c-3

Thousands of seeds over every scale, magic and era with today's P1 preroll: no clash pair of this file stands together (the list above plus the registry's); no pool is empty; the trope break pool's smallest size is reported for the first and for the second draw, and neither is under five; `families_distinct` still holds; every override names a registered default; every pair that overrides one default has its `combine` line or cannot be rolled together; the removed row ids appear nowhere in the committed data; the stamps cover every row of the three files.
