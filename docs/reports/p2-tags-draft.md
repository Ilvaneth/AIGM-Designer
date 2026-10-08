# P2 tag pass — draft (build item 22a-0)

*Written 2026-10-08 by the coding tab for the design tab's audit and the owner's review, on `docs/p2-build-22.md` (22a-0), `docs/p2-tags.md` (S0-S7) and `docs/reports/p2-survey.md`. The rows are read as `p2-tags.md` leaves them: its deletions are gone, its new rows are in. P1's nine tag rules (`docs/p1-tags.md` §1) hold. No table, prompt or script was changed. Not committed.*

**What the owner reviews** (as for P1, not each row's claims): **§1.1** the new topics; **§2** the clash pairs (each marked *ruled* where S1-S6 already ruled it, *new* where this pass found it); **§6.2** the `home_of` proposals; and the **§9** open points, which are things the rulings leave unsaid or where they met the data.

---

## 0. In short

- **Topics:** four new ones (`gods`, `gods_shown`, `casting`, `moon`) and one new value for an existing topic (`magic: running_out`). A fifth new topic (`reading`) is needed only if the owner declares pair C3.
- **Clash pairs:** §2.1 lists 23 entries recommended for declaration:
  - 11 are already ruled in S1-S6 (three of them are written as `requires`, one as an override);
  - 11 are new to the owner, two of them first seen by the survey;
  - 1 is the existing row pair (dead gods and silent gods), kept.
  §2.2 lists 9 more candidates with a recommendation not to declare them.
- **Overrides:** the four P2 defaults P1 already overrides stay. Four new defaults are proposed: the presence (gods among mortals), the moon (the moon trades), the festivals (the pantheon type) and the great and greater gods' counts (the dualist pantheon). P2 rows also reach P4, P6, P7 and the rest pressure; the chart (§5) flags those as second owners.
- **Requires:** 15 entries. R4-R6 are new, R7-R8 come from the survey, and the rest from the rulings or the rows' own hooks. Of the fifteen P1-phase hooks inside P2's tables, four become `requires`, three are deleted with a fit in their place, and eight are deleted (one with its row; §4.2).
- **Planes:**
  - Fits are given for the thirteen P1 rows that name a plane (the survey's L4; §6.1).
  - `home_of` is proposed for every threat family. Two corrections to S3: `family_shadow` is a spymaster, not a shadow creature, so it takes no home; and the genie family's home is per creature.
  - Two P1 rows name a plane without a P2 hook: the spine "two worlds" and the ruin "the kingdom that reached for the stars".
- **The measurement before** (§8), over 3,000 births with today's `preroll_p2`: **91.5 %** of births hold a declared clash, an override no roll applies, or a `requires` left unmet. The declared clashes alone are 53.4 %. The largest causes are the start anchor against the move's time (70.7 %) and the climate against the palette or the era (23.5 %, 18.1 %, 7.2 %).

---

## 1. Claims (rule 1)

### 1.1 The topics

| Topic | Label | Values | New? |
|---|---|---|---|
| `gods` | what the gods are now | `answering`, `dead`, `silent`, `among_mortals`, `spirits` | **new** |
| `gods_shown` | how the gods show themselves | `never`, `omens`, `ordained`, `at_places`, `walking`, `through_phenomenon` | **new** |
| `casting` | whether casting is allowed | `forbidden`, `licensed`, `by_caste`, `free` | **new** |
| `moon` | the moon | `none`, `unseen`, `one`, `two`, `place`, `face`, `tidal` | **new** |
| `magic` | how plentiful magic is | existing values + **`running_out`** | new value |
| `reading` | reading | `guarded` | **new, only if C3 is declared** |

The P0/P1 topics stay as they are (`rule`, `nobility`, `below_ground`, `writing`, `magic`, `war`). No P2 row claims `rule`, `nobility`, `below_ground` or `war`.

### 1.2 The P2 rows that claim something

Every other P2 row claims nothing: its sentence, hook or effect states no fact that a topic carries (rule 1: theme is never a claim).

| Row | Claim | The literal words |
|---|---|---|
| `pantheon_polytheist` | `gods: answering` | "many gods, all real enough to answer" |
| `pantheon_dead_gods` | `gods: dead` | "the gods died or were killed" |
| `pantheon_silent_gods` | `gods: silent` | "the gods exist and do not answer" |
| `pantheon_animist` (new) | `gods: spirits` | "spirits in every river, hill and beast; the land itself answers" |
| `presence_never` | `gods_shown: never` | "no manifestation in living memory" |
| `presence_omens` | `gods_shown: omens` | "read as the gods' speech" |
| `presence_clergy_only` | `gods_shown: ordained` | "miracles happen, only through the ordained" |
| `presence_in_places` | `gods_shown: at_places` | "a god answers only at its site" |
| `presence_walking` | `gods_shown: walking` | "gods or their avatars walk the land" |
| `presence_through_phenomenon` | `gods_shown: through_phenomenon` | "the signature magic phenomenon is the gods' only voice" |
| `constraint_caste` | `casting: by_caste` | "only the ordained, the born or the marked may cast" |
| `constraint_licence` | `casting: licensed` | "casting is legal with a licence" |
| `taboo_none` | `casting: free` | its hook: "nothing magical is forbidden" |
| `source_a_dying_thing` (S4 rewording) | `magic: running_out` | "everyone knows the source is running out" |
| `source_study` | `reading: guarded` *(only if C3)* | "reading is guarded" |
| `moon_none_stars` | `moon: none` | "No moon, only stars" |
| `moon_dark` | `moon: unseen` | "the moon is never seen" |
| `moon_one_thirty` | `moon: one` | "One moon" (**the label's "thirty-day cycle" must become 28**, S6) |
| `moon_two` | `moon: two` | "Two moons" |
| `moon_is_a_plane` | `moon: place` | "The moon is a place" |
| `moon_with_a_face` | `moon: face` | "A moon with a face" |
| `moon_tidal` | `moon: tidal` | "A moon that drives the phenomenon" |

**Rows that claim nothing, by table** (as `p2-tags.md` leaves them):
- **pantheon:** `pantheon_dualist`, `pantheon_ancestor_gods`; the 8 domains; the 3 ranks; the 11 church archetypes; the 11 relations; the 5 god secrets left.
- **planes:** the 29 baseline rows (26 and the fey echo, the shadow echo, the realm beyond); the 7 deviations; the 6 time rates; the 8 ways in; the 8 costs. A plane's facts hold for one plane, so a birth-wide topic cannot carry them; see §9.4.
- **magic:** sources except `source_a_dying_thing` (10); `constraint_components`, `constraint_echo` and the new `constraint_law_and_folk` ("the law and what the folk will bear" names no fact a topic holds); the 6 visibilities; taboos except `taboo_none` (11); the 9 regulators; the 7 wild rows.
- **history:** the 14 ages, the 16 event types, the 9 divergences and the 7 memories.
- **calendar:** the 8 climates, the 16 festivals, the 6 start anchors, and the 2 new `underground_count` rows.

### 1.3 The P0/P1 rows read as claims against P2

| Row | Claim (existing or proposed) | Note |
|---|---|---|
| `magic_low` / `_medium` / `_high` (dial) | `magic: scarce / middling / plentiful` | existing |
| `ruin_age_of_mages` | `magic: faded` | existing |
| `break_magic_sold` | `magic: plentiful` | existing |
| `era_renaissance` (dial) | `writing: printed` | existing |
| `era_underground` (dial) | `below_ground: lived_in` | existing; the climate rule (§4) reads the dial itself |
| `break_gods_among_mortals` | `gods: among_mortals` | **proposed**: "the gods live among mortals" |
| `break_casting_forbidden` | `casting: forbidden` | **proposed**: "casting a spell is a crime" |

The other P1 rows meet P2 through row-level pairs (§2), overrides (§3) or requires (§4), not through claims: a P1 row's sentence about the moon or the gods is about one thing P2 rolls, and a pair on the P2 row says it most plainly.

---

## 2. Clash pairs (rule 2)

**Where each pair lives:** a pair between two claims goes to `claims.yaml#clashes`; a pair between a P2 row and one P1 row goes on the P2 row's `conflicts_with`, so the P2 row leaves the pool and the sealed P1 tables stay unchanged. **Kind:** P2×P2, P2×P1 or P2×dial. **Measured:** the share of births holding the pair today (§8).

### 2.1 Recommended for declaration

| # | Pair | Kind | Ruled? | Declared as |
|---|---|---|---|---|
| D1 | `gods: dead` × `gods_shown: walking` | P2×P2 | survey D.16 | claims |
| D2 | `gods: silent` × `gods_shown: omens` | P2×P2 | **ruled** S1 | claims |
| D3 | `gods: silent` × `gods_shown: walking` | P2×P2 | **ruled** S1 | claims |
| D4 | `gods: among_mortals` × `gods: dead` | P2×P1 | **ruled** S1 ("removes dead and silent") | claims |
| D5 | `gods: among_mortals` × `gods: silent` | P2×P1 | **ruled** S1 | claims |
| D6 | `casting: forbidden` × `casting: free` | P2×P1 | survey D.16 | claims |
| D7 | `moon_none_stars` × `break_moon_trades` | P2×P1 | **ruled** S6 | `moon_none_stars.conflicts_with` |
| D8 | `moon_none_stars` × `break_night_is_safe` | P2×P1 | **ruled** S6 | idem |
| D9 | `moon_none_stars` × `weak_vulnerable_time` (secret) | P2×P1 | **ruled** S6 | idem (a secret pair, §9.6) |
| D10 | `moon_dark` × `break_night_is_safe` | P2×P1 | **new**: its hook "the moon marks the working hours" needs a moon that is seen | `moon_dark.conflicts_with` |
| D11 | `moon_dark` × `break_moon_trades` | P2×P1 | **new** (survey D.7): "ships go to the moon when it is full" needs a moon with phases | idem |
| D12-14 | the climate against the era and the palette | P2×dial / P2×P1 | **ruled** S6 | requires (§4.1 R10), not pairs |
| D15 | `pantheon_dead_gods` × `pantheon_silent_gods` | P2×P2 | existing row pair | stays as it is (one type a birth; kept for the record) |
| D17 | `break_divine_magic_holy_ground` × `presence_in_places` | P2×P1 | **new**: "beyond them it still answers" against "a god answers only at its site" | `presence_in_places.conflicts_with` |
| D18 | `break_chosen_are_many` × `gods: dead` | P2×P1 | **new**: "the gods mark a hundred chosen" every generation; dead gods mark no one | `pantheon_dead_gods.conflicts_with` |
| D18b | `break_chosen_are_many` × `gods_shown: never` | P2×P1 | **new**: a hundred marked a generation is a manifestation in living memory | `presence_never.conflicts_with` |
| D19 | `power_god` (secret) × `gods: dead` | P2×P1 | **new**: a god behind the villain is a living god | `pantheon_dead_gods.conflicts_with` (secret pair) |
| D20 | `family_god` (secret) × `gods: dead` | P2×P1 | **new**: an avatar, an imprisoned or a returning god is a living god (the antagonist row's forms) | idem (secret pair) |
| D21 | `constraint_licence` × `regulator_nobody` | P2×P2 | **new**: "the licence is a ledger entry the regulator keeps" against "nobody" | `regulator_nobody.conflicts_with` (the regulator is rolled after the constraint) |
| D22 | `break_magic_sold` × `taboo_healing_for_pay` | P2×P1 | **new**: "magic is bought and sold like bread" against "selling healing" as a taboo | `taboo_healing_for_pay.conflicts_with` |
| D23 | `gods: among_mortals` × `gods_shown: never` | P2×P1 | **ruled** S1 (presence forced to walking) | an override (§3.2), not a pair |

### 2.2 Candidates not recommended (the owner may declare any)

| # | Pair | Why not |
|---|---|---|
| C1 | `magic: plentiful` (dial high, magic sold) × `magic: running_out` | Plenty now and a source running out is the story of a world spending what it has. Recommend a **fit** (×2 with `ruin_dried_source`), no clash. |
| C2 | `magic: faded` (the age of mages) × a wild surge (any `wild_` but `wild_no`) | Faded magic whose dregs misbehave is coherent. The dial's gate already decides how often surges come. |
| C3 | `writing: printed` (renaissance) × `source_study` ("reading is guarded") | Printing makes the guard a story (banned presses, licensed printers). Recommend a fit (×2) instead. If the owner declares it, `source_study` needs the new topic `reading: guarded`. |
| C4 | `gods: dead` × `gods_shown: omens` | Omens "read as the gods' speech" is what people believe; the dead-gods type keeps the rites ("the gods are dead; the rites remain"). |
| C5 | `gods: dead` or `silent` × `gods_shown: through_phenomenon` | "The phenomenon is the gods' only voice" can be what the churches claim for a dead or silent pantheon. Owner's taste; recommend no clash for dead, a clash for silent (whose rule is that they do not answer). |
| C6 | `casting: forbidden` × `casting: licensed` | The `claims.yaml` combine already writes the ban's licensed exception (`contest_casters_casterless`): a licence under a ban is that exception. |
| C7 | `visibility_invisible` × `constraint_echo` | "Shows nothing" when cast, and "can be read afterwards": a sequence, not a contradiction (the survey marked it soft). |
| C8 | `break_casting_forbidden` × `visibility_loud` | Casters hide that they can cast; under loud magic they cannot cast unseen. A tension worth playing. |
| C9 | `constraint_caste` × `regulator_nobody` | "Everyone else who does is a criminal" against "nothing formal": nobody keeps a register, yet the folk punish. Owner's taste; recommend no clash. |

---

## 3. Overrides (rule 4)

### 3.1 The P2 defaults P0/P1 already override (`claims.yaml#defaults`, unchanged)

| Default | Overriders | Note |
|---|---|---|
| `regulator_identity` | `break_magic_is_nobility` (the nobility), `break_casting_forbidden` (the hunters), `contest_casters_casterless` (side a) | the combines are written; 22b forces the record |
| `regulator_strictness` | the magic dial (owner of the default); `break_casting_forbidden` (strictest), `contest_casters_casterless` (strict) | combine written |
| `pantheon_type` | `break_gods_are_ancestors_known` (forced); `break_gods_among_mortals` narrows (dead and silent leave: pairs D4, D5) | |
| `great_gods_floor` | `break_gods_among_mortals` (1); the religious contest roles (`hint: religious`, already ruled); the unnamed god's priests (`break_god_name_forbidden`, already ruled) | the last two are not written as `overrides` in the data: §9.7 |

### 3.2 New defaults proposed

| New default | Phase | Overrider | To | Why a default, not a pair |
|---|---|---|---|---|
| `pantheon_presence` | P2 | `break_gods_among_mortals` | `presence_walking` | S1 "forced"; same form as `pantheon_type` (D23 needs no pair then) |
| `moon` | P2 | `break_moon_trades` | `moon_is_a_plane` | its P2 hook: "the moon is a touched plane … one of the touched planes" |
| `festivals` | P2 | `pantheon_dead_gods` ("days of mourning"), `pantheon_silent_gods` ("vigils and readings"), `pantheon_ancestor_gods` ("the ancestors' days"), `pantheon_animist` ("festivals follow the land's seasons"), `pantheon_dualist` ("two great feasts, one per side") | the type's festival effect | S6 sets "one per greater god, plus one or two folk festivals"; the type rows also set festivals. **Proposed combine:** the S6 count holds; the type's effect sets the *kind* of the folk festivals (dead: a day of mourning, silent: a vigil, ancestors: the ancestors' day, animist: a festival of a season). Under dualist, the two greater gods' feasts are the two great feasts. |
| `great_gods`, `greater_gods` (counts) | P2 | `pantheon_dualist` | 2 and 2 at every scale | S1. **Combine with the floors (`great_gods_floor`):** each floor is at most 2 at every scale, so the dualist's 2 holds; a floor raise never takes it to 3 (§9.7). |

### 3.3 P2 rows that rewrite a later default (each a second owner, see §5)

| P2 row | Default it reaches | Proposed |
|---|---|---|
| `pantheon_dualist` | P4's faction list (two churches at short) | already one of P4's six sources ("the great gods' churches"); P4's tag pass weighs it (S1) |
| `fest_masks` ("attitude to intruders is `test`") | P6 `site_attitude_pool` | make it an override of `site_attitude_pool` for the masked-night site only, with a combine beside the two breaks' |
| `anchor_midwinter` ("rest pressure and food are the first problems") | rest pressure (the danger dial's) | rewrite the hook to name no pressure ("the hard season is on; food is short") |
| `climate` (`climate_underground`) | P3's region biomes (`designer.py:415-416` filters them by the climate) | consistent once the climate comes from the palette (S6): the filter and the palette agree; write the combine |
| `source_study` ("the regulator is a guild or a school") | P2's own regulator roll (`regulator_identity`) | a second owner: replace the P4 hook by a fit (`regulator_guild` ×3 under `source_study`) |
| `rel_trial` ("a beat's world_pressure or a doom"), `godsecret_fading` ("the fading is a clock"), `rate_fast` ("the doom clock is the danger of entering"), `age_now_named_for_fear` ("the taught form of the doom") | P7's doom and clocks (the threat's) | G10 (texture as the doom). S5 rewrote the present age's naming; the other three hooks are not yet ruled: rewrite each to name no doom or clock (§9.3) |

---

## 4. Requires (rule 5) and fits (rule 6)

### 4.1 Requires

| # | Row | Requires | Source |
|---|---|---|---|
| R1 | `wild_dead_god_static` | `any_of: [pantheon_dead_gods, ruin_dead_god]` | S4 (its rule's "or silent" leaves; §9.5) |
| R2 | `wild_overflow` | a phenomenon that can overflow: `none_of` the 8 rules that cannot happen "too much" (`rule_beasts_sense_lies`, `rule_roads_lead_where_needed`, `rule_night_distances`, `rule_true_names`, `rule_gesture_magic`, `rule_seasons_bound_to_a_beast`, `rule_land_guards_lifeline`, `rule_one_way_magic`) | S4; the list is this pass's reading |
| R3 | `taboo_the_phenomenon_unlicensed` | `none_of: [user_no_one]` | S4 |
| R4 | `presence_through_phenomenon` | `none_of: [user_no_one]` ("whoever controls the phenomenon") | **new** |
| R5 | `source_the_phenomenon` | `any_of: [user_everyone, user_casters]` (otherwise "every other casting is a use of it" takes a PC's spells from a caster who may not use it, against S4's principle) | **new** |
| R6 | `way_phenomenon` | `any_of: [rule_mirror_doors, rule_shifting_doors]` ("the phenomenon at full strength is the door") | **new**, replaces its P1 hook |
| R7 | `regulator_church` | a counted god with Knowledge or Light ("Law-adjacent" does not exist: reword) | survey D.9; P2-internal (the pantheon rolls first) |
| R8 | `regulator_the_dead` | `pantheon_ancestor_gods` or a counted Death god ("the ancestor lists or the grave wardens") | survey D.9; P2-internal |
| R9 | `rel_mirror` | a pinned god (`pin.god`) | S2 |
| R10 | `climate_underground` | `dial: {era: [underground]}`; every other climate `none_of` that dial; the pool among the palette's allowed climates (computed from the palette kinds' biomes, `regions.yaml`) | S6 |
| R11 | `moon_is_a_plane` | a free touched seat (P2-internal count) | S6 |
| R12 | the start anchors | `anchor_after_event`: `time_just_now` or `time_unfolding`; `anchor_days_before_doom` (reworded): `time_coming`; the four others (festival eve, season start, market day, midwinter): `time_generation_ago` | S6 |
| R13 | `taboo_casting_on_a_day` | a seated holy day: not a `requires`, since 22b step 7 seats it (S4) | S4 |
| R14 | `dev_reachable_by_death` | its plane's cost is `cost_the_way_back` or `cost_years` (one plane's scope: the roller narrows that plane's cost; §9.4) | the row's own hook |
| R15 | `source_the_gods` (S4 rewording) | none: the pantheon always exists | — |

### 4.2 The fifteen P1-phase hooks inside P2's tables (S0 #7)

| Row | Hook (due at P1) | Fate |
|---|---|---|
| `presence_through_phenomenon` | "the signature institution regulates the phenomenon" | **deleted** (S1); R4 instead |
| `godsecret_is_the_phenomenon` | — | the row is deleted (S2) |
| `way_mirror` | "rule_mirror_doors, if rolled, is this way" | **deleted**; a fit instead: ×3 with `rule_mirror_doors` |
| `way_phenomenon` | "the phenomenon's rule states the door" | **requires** R6 |
| `cost_name` | "naming.json's rite of naming can restore it" | **deleted** (S3 rewording) |
| `source_names` | "naming.json marks the binding language" | **deleted**; fit ×2 with `rule_true_names`, `rule_tongue_of_magic` |
| `source_the_phenomenon` | "the phenomenon's rule covers every caster class" | **requires** R5 |
| `taboo_naming` | "the naming language carries the taboo" | **deleted**; fit ×2 with `rule_true_names` |
| `taboo_the_phenomenon_unlicensed` | "the signature institution issues the leave" | **requires** R3 |
| `regulator_signature_institution` | "the institution's seed includes the licence…" | **deleted** (P1's seed is sealed) |
| `wild_overflow` | "the phenomenon's rule states its overflow" | **requires** R2 |
| `moon_tidal` | "the signature phenomenon's cycle is the moon's" | **deleted**: any phenomenon can follow the moon; no real dependency |
| `fest_naming` | "naming.json's rite of naming is this day" | **deleted** (no rite of naming exists) |
| `evtype_naming` | "naming.json records the old name as an alias" | **deleted** |
| `mem_the_dead` | "only if the signature phenomenon or institution reads the dead" | **deleted**: no P1 row reads the dead, and the SRD's *speak with dead* lets any cleric do it |

### 4.3 Fits (weights only)

| Fit | Weight | Note |
|---|---|---|
| the pantheon type under a gods-family ruin: `ruin_dead_god` → `pantheon_dead_gods`; `ruin_departed_god` → `pantheon_silent_gods`; `ruin_gods_quarrel` → `pantheon_polytheist`, `pantheon_dualist`; `ruin_imprisoned_god` → `pantheon_polytheist`; `ruin_failed_apotheosis` → `pantheon_ancestor_gods` | ×2 each | "the pantheon roll follows it" (`docs/p1-tags.md` §2, the ruin source); the proposed mapping is this pass's |
| `era_nautical` → `climate_maritime`; → `baseline_water` for a free touched seat | ×2 | the nautical era; `baseline_water`'s `touch_bias` |
| `era_underground` → `baseline_earth` (free touched seat) | ×2 | `touch_bias` kept |
| `baseline_fire`'s `touch_bias: [tone_shadowed]` | **deleted** | the tone's planes modifier left (`docs/p1-tags.md` §2) |
| `way_mirror` with `rule_mirror_doors` | ×3 | from §4.2 |
| `source_names` with `rule_true_names` or `rule_tongue_of_magic`; `taboo_naming` with `rule_true_names` | ×2 | from §4.2 |
| `constraint_caste` with `break_magic_is_nobility` or `contest_casters_casterless` | ×2 | the caste is the nobility or side a |
| `source_blood` with `break_magic_is_nobility` | ×2 | inherited magic |
| `source_study` with `era_renaissance` | ×2 | in place of C3 |
| `regulator_guild` with `source_study` | ×3 | in place of `source_study`'s P4 hook (§3.3) |
| `source_a_dying_thing` with `ruin_dried_source` | ×2 | in place of C1 |
| `way_dream` with `break_dreams_are_a_place`; `baseline_astral` as its plane | ×2 | the dream-land |
| a touched plane's non-`rate_same` time rate with `ruin_broken_time` or `scar_time_flow_changed` | ×2 | when that plane is the ruin's or the scar's |
| `church_pilgrimage` for the pilgrim road's greater god (`life_pilgrim_road`) | ×3 | S1: the pilgrim road's god is a greater god |
| the climate: weighted by how many of the palette's kinds allow it | ×n | S6 |
| the folk festivals by the greater gods' domains (`domain_affinity`) | ×2 | S6 |

---

## 5. Who sets what — P2's targets (rule 9)

`docs/p1-tags.md`'s chart, extended. ⚠ marks a second owner the owner must see; each proposes a combine.

| Target | Owner | Note |
|---|---|---|
| the god count | the scale's band | rolled (S1) |
| the greater gods and the rank split | the ranks' `share` bands, summing to the count | the greater count is never below the great gods' (22b) |
| the great gods' count | the scale's band | floors already ruled; **`pantheon_dualist` sets 2** (§3.2 combine) |
| the pantheon type | P2's roll | ancestors force it; gods among mortals narrow it; a gods-family ruin weighs it (§4.3) |
| the presence | P2's roll | **gods among mortals forces walking** (new default) |
| the domains and the coverage | the scale's coverage rule | each god 1-2 rolled |
| the evil god | the standard/epic rule (S2) | |
| a god's church form | P2's church row (greater: archetype; others: `church_shape`) | P4's faction follows its `faction_archetype` (S2) |
| the threat's god seat | P1's threat (`family_god`, `power_god`) | secret (S1) |
| the touched-plane count | the scale (1 / 1-2 / 3-6), the magic dial's modifier | P1-named planes share it; the moon (`moon_is_a_plane`) and, at epic, the threat's home take a seat |
| which plane a P1 row names | the fits (§6.1) | |
| a touched plane's deviation, rate, way in and cost | P2's rolls | `dev_reachable_by_death` narrows its cost (R14) |
| a touched plane's keeper | P2: a power-rank god that fits, else an SRD creature | |
| the regulator: who | P2's roll; three P1 rows override it | ⚠ `source_study`'s P4 hook also names it: replaced by a fit (§3.3) |
| the regulator: how strict; the wild gate | the magic dial; two P1 rows override the strictness | |
| the wild shape | P2's roll | R1, R2 |
| the climate | the palette (allowed climates); `era_underground` forces underground | ⚠ the climate also filters P3's biomes (`designer.py:415`): consistent once it comes from the palette; write the combine |
| the moon | P2's roll | a P1 row needing a moon excludes the moonless rows (D7-D11); the moon trades force the place (new default) |
| the year, the months, the week | fixed: 12 × 28, a seven-day week (S6) | `year_shape` and `week` leave the rolls |
| the festivals | one per greater god (its domain's kind) plus one or two folk festivals (S6) | ⚠ the pantheon type's `festivals` effect: combine in §3.2 |
| the dated days (the empty month, the lawless day, the taboo's holy day) | P1's rows and P2's taboo; inside the span from `scale.yaml` `doom` | |
| the start anchor | the move's time row (S6) | R12 |
| the history's ages | the ruin (one age), the first and the present in place, the middles rolled, the scale's count | |
| the dated events | the move (P1's time), the villain's origin (P1's chain, secret), the institution's founding, the rest rolled; the scale's count | |
| the divergences | the scale: exactly 1 / 2 / 3 (S5) | |
| the witness lists | the seated story events only (S5) | keeps P5's NPC cap |
| P4's faction list | (six sources, `docs/p1-tags.md`) | the great gods' churches: under dualist two at short (S1); ⚠ `presence_omens` "the omen readers are a faction or a service": keep "a service" only, or count it among the sources |
| P6's site attitude | P6's roll; two breaks narrow it | ⚠ `fest_masks` (§3.3) |
| rest pressure | the danger dial | ⚠ `anchor_midwinter` (§3.3) |
| P7's doom and clocks | the threat (goal, doom shape) | ⚠ `rel_trial`, `godsecret_fading`, `rate_fast`, `age_now_named_for_fear` (§3.3; G10) |
| P3's prices | the lifeline (P3's economy) | `taboo_healing_for_pay` (no healing line), `taboo_iron_or_metal` (a substitute), `fest_fair`, `fest_harvest` (modifiers): additive lines on the lifeline's table, no second owner if written so |

---

## 6. The planes

### 6.1 The P1 rows that name a plane: the baseline rows each fits

"Non-material" below means every baseline row except `baseline_material` and `baseline_demiplane`: the 2 transitive, the 4 inner and the Elemental Chaos, the 17 outer (16 and the hub), and the 3 new rows.

| P1 row | Its words | Fits |
|---|---|---|
| `land_thin_place`, `target_thin_place` | "the place where a plane touches the world" | any non-material |
| `ruin_celestial_war` | "a war between the planes was fought out in this world" | one upper-tier and one lower-tier outer plane (it names two sides); shared to fit the count, the upper first at short |
| `ruin_elven_withdrawal` | "the elves withdrew to another plane" | the fey echo (×3), `baseline_cg` |
| `ruin_planar_rift` | "the gate of a plane opened, then closed" | any non-material |
| `ruin_planar_invasion` | "an army that came from another plane" | the lower-tier outer rows, `baseline_le_ln` (the armies of the Colliding Iron), the four inner |
| `ruin_devils_bargain` | "bought its golden age from the Hells" | `baseline_nine_hells` only |
| `ruin_demon_gate` | "a gate to the Abyss" | `baseline_ce` only |
| `ruin_sleeping_realm` | "fell into one dream and did not wake" | `baseline_astral` (the table's "realm of thought and dream"), the fey echo |
| `act_merged_with_plane` | "dragged into another plane" | any non-material |
| `scar_plane_thinned` | "the border with a plane grew thin" | any non-material |
| `break_dreams_are_a_place` | "one shared dream-land" | `baseline_astral` |
| `break_moon_trades` | "the moon is a touched plane" | **the moon's own seat** (§9.2): no baseline row |

**Rows that name a plane without a P2 hook** (for the owner):
- **`spine_two_worlds`:** its end_b is "the other plane". Recommend a P2 hook "the other plane is touched and chosen among the non-material rows", seated like the others.
- **`ruin_star_kingdom`:** "called something from the stars". Not literally a plane; it fits the realm beyond if the owner gives it a plane.

### 6.2 `home_of` (the threat families each plane is home to)

| Family | `home_of` on | Status |
|---|---|---|
| `family_devil` | `baseline_nine_hells` | S3 |
| `family_demon` | `baseline_ce` | S3 |
| `family_hag_fey` | the fey echo | S3 |
| `family_from_beyond` | the realm beyond | S3 |
| `family_genie_elemental` | the plane of the creature's element: `djinni` → `baseline_air`, `efreeti` → `baseline_fire` (the family's SRD creatures); an elemental lord → any of the four inner | S3 ("its element"); **the home is per creature**, not one row |
| `family_fallen_celestial` | the upper-tier outer rows (one rolled) | S3 |
| `family_undead` | the shadow echo | S3 |
| `family_shadow` | **none** | S3 says the shadow echo, but this family is "a shadow (spymaster or guild master)": assassin, spy, bandit captain, no shadow creature. **Correction proposed.** |
| `family_deceiver_fiend` | the lower-tier outer rows, per creature: `rakshasa` → `baseline_nine_hells`, `night-hag` → `baseline_hades` (the Grey Country), `succubus-incubus` → any lower | proposed |
| `family_god` | the outer plane of its alignment (rolled at P2, a secret seat), else none | proposed; the owner may prefer none |
| `family_sea_titan` | none (`baseline_water` as the alternative: a kraken's deep) | proposed |
| `family_monstrous_mind`, `family_mage`, `family_ruler`, `family_dark_priest`, `family_chromatic_dragon`, `family_metallic_dragon`, `family_giant`, `family_lycanthrope` | none | native to the Material |

**The three new baseline rows**, for 22a (labels of the table's own; the `spells` lists from the SRD's plane-naming spells):
- **the fey echo:** `group: echo`; `spells: [dispel evil and good, plane shift]`; `home_of: [family_hag_fey]`.
- **the shadow echo:** `group: echo`; `spells: [dispel evil and good, plane shift]`; `home_of: [family_undead]`.
- **the realm beyond:** `group: beyond`; `spells: []` (no SRD spell names it); `home_of: [family_from_beyond]`.

---

## 7. Rule 8: which P2 tables may repeat across campaigns

| Table | Rows (after S1-S6) | `avoid_used` | The five-row floor |
|---|---|---|---|
| `pantheon#type` | 6 | false (S1; the roll already passes `avoid=False`) | exempt |
| `pantheon#presence` | 6 | false | exempt |
| `pantheon#domain_scaffold` | 8 | false (drawn per god) | exempt |
| `pantheon#rank` | 3 | not drawn (the split) | — |
| `pantheon#church_archetype`, `#relationship` | 11, 11 | false (several per birth) | exempt |
| `pantheon#god_secret` | 5 | **false recommended** (one per campaign; under `avoid_used` the five would run out in five campaigns) | exempt |
| `planes.yaml` (all five) | 29, 7, 6, 8, 8 | false (header) | exempt |
| `magic#source` | 11 | true | holds (11 ≥ 5 after R5) |
| `magic#constraint` | 5 | **false recommended** (5 rows: the classic "law and folk" should repeat) | exempt |
| `magic#visibility` | 6 | **false recommended** (survey: six births spend it) | exempt |
| `magic#taboo` | 12 | true | holds; under R3 and D22 a birth's pool stays ≥ 9 |
| `magic#regulator` | 9 | **false recommended** (three rows are forced by overrides; a guild and a church should repeat) | exempt |
| `magic#wild` | 7 | false (gated) | exempt |
| `history#age_template` | 14 (the middles: 11) | true | holds |
| `history#event_type`, `#divergence`, `#memory` | 16, 9, 7 | false | exempt |
| `calendar#climate` | 8 | false (S6: no cross-campaign avoid) | exempt |
| `calendar#moon`, `#festival_type`, `#start_anchor`, `#underground_count` | 7, 16, 6, 2 | false | exempt |

The headers of `pantheon.yaml`, `magic.yaml`, `history.yaml` and `calendar.yaml` say `avoid_used: true` for the whole file (survey D.15). Recommend per-table values as above, and `design_compare.py:30`'s whole-file uniqueness for `pantheon.yaml` dropped.

---

## 8. The measurement before

`docs/reports/p2-tags-draft/measure_p2.py` (model-free; 3,000 births of the shared corpus; today's `preroll_p2` run on a copy of each birth's P1 context). **D** counts the declared pairs of §2.1 (with D12-D14, the climate against the era and the palette, counted as pairs). **O** counts the overrides no roll applies today (the regulator under its three overriders; gods among mortals without walking; the moon trades without the moon as a place). **Q** counts the requires left unmet (R1-R5, R12). The candidates of §2.2 are counted apart and in no total.

```text
births: 3,000 (corpus stops on an empty pool: 0)
D a declared clash: 1,603 (53.4 %)
O an override no roll applies: 508 (16.9 %)
Q a requires left unmet: 2,332 (77.7 %)
D or Q: 2,698 (89.9 %)
D, O or Q: 2,746 (91.5 %)
by cause:
  Q4 a start anchor against the move's time: 2,120 (70.7 %)
  D14 a climate the palette does not allow: 706 (23.5 %)
  D13 the underground era without the underground climate: 544 (18.1 %)
  Q5 the gods speak through a phenomenon no one controls: 248 (8.3 %)
  D12 underground climate outside the underground era: 215 (7.2 %)
  Q6 the phenomenon is the only source, and only some may use it: 215 (7.2 %)
  Q2 an unlicensed-phenomenon taboo when no one uses it: 173 (5.8 %)
  D2 silent gods × omens: 167 (5.6 %)
  O1 the regulator rolled although break_casting_forbidden overrides who: 167 (5.6 %)
  O1 the regulator rolled although break_magic_is_nobility overrides who: 150 (5.0 %)
  Q1 dead-god static without dead gods: 138 (4.6 %)
  O1 the regulator rolled although contest_casters_casterless overrides who: 99 (3.3 %)
  O2 gods among mortals without the walking presence: 89 (3.0 %)
  D16 thirteen moons × two moons: 69 (2.3 %)
  D16 thirteen moons × no moon: 63 (2.1 %)
  D16 thirteen moons × a dark moon: 59 (2.0 %)
  D3 silent gods × the gods walk: 51 (1.7 %)
  O3 the moon trades without the moon as a place: 39 (1.3 %)
  Q3 overflow of a phenomenon that cannot overflow: 32 (1.1 %)
  D17 holy ground × answers only at its places: 31 (1.0 %)
  D1 dead gods × the gods walk: 28 (0.9 %)
  D21 licence and ledger × nobody regulates: 24 (0.8 %)
  D18b the chosen are many × never shown: 24 (0.8 %)
  D18 the chosen are many × dead gods: 21 (0.7 %)
  D9 no moon × a moon-night weakness: 21 (0.7 %)
  D5 gods among mortals × silent gods: 20 (0.7 %)
  D6 casting forbidden × no taboo: 19 (0.6 %)
  D22 magic sold like bread × selling healing is taboo: 16 (0.5 %)
  D4 gods among mortals × dead gods: 14 (0.5 %)
  D20 the threat is a god × dead gods: 10 (0.3 %)
  D11 dark moon × the moon trades: 8 (0.3 %)
  D10 dark moon × night is safe: 8 (0.3 %)
  D19 a god behind the villain × dead gods: 7 (0.2 %)
  D7 no moon × the moon trades: 6 (0.2 %)
  D8 no moon × night is safe: 5 (0.2 %)
candidates (not counted above):
  C1 plentiful magic × a dying source: 58 (1.9 %)
  C2 faded magic × wild surges: 5 (0.2 %)
  C3 printed writing × study alone: 77 (2.6 %)
  C4 dead gods × omens: 81 (2.7 %)
  C5 dead gods × the phenomenon speaks: 56 (1.9 %)
  C5 silent gods × the phenomenon speaks: 118 (3.9 %)
  C6 casting forbidden × licence: 18 (0.6 %)
  C7 invisible casting × every spell leaves a trace: 39 (1.3 %)
  C8 casting forbidden × loud casting: 28 (0.9 %)
  C9 a caste casts × nobody regulates: 23 (0.8 %)
```

**In one line:** 91.5 % of births hold a declared clash, an override no roll applies or a `requires` left unmet (P1's figure was 86.4 % before item 10). The declared clashes alone are 53.4 %, and the climate carries most of them (the palette 23.5 %, the underground era 18.1 % and 7.2 %). The largest single cause is the start anchor against the move's time (70.7 %).

**What the figure does and does not say** (as `docs/p1-tags.md` says of P1's): every counted case is removed by a rule the draft proposes, so after 22b the share is zero by construction. Rolls that do not exist today cannot be counted:
- no planes are rolled, so a P1-named plane left untouched is not counted, though every birth holding such a row leaves it untouched today;
- no gods are rolled, so R7, R8, the evil god, the domain coverage and the festivals per greater god are not counted;
- `year_thirteen_moons` against the moon rows (D16) is counted as today's fault, though the row leaves the rolls.

---

## 9. Open points for the owner

1. **The correction to S3:** `family_shadow` is a spymaster, so it has no home plane (§6.2).
2. **The moon as a plane:** `break_moon_trades` and `moon_is_a_plane` take a touched seat with no baseline row. Proposal: the moon is a seat of its own (its deviation `dev_is_this_world`; way in, cost and rate rolled like the others), named from the pool. Alternatively, add a baseline row "the moon".
3. **G10 hooks not yet ruled:** `rel_trial`, `godsecret_fading` and `rate_fast` set P7's doom or a clock (§3.3). Proposal: rewrite each to name no doom or clock.
4. **A plane's facts are per plane:** a deviation, cost or rate holds for one touched plane. Birth-wide topics cannot carry them, so the roller narrows them per plane (R14, the fits by the ruin's or the scar's plane). No new topic is proposed.
5. **`wild_dead_god_static`'s rule** reads "a dead or silent god's will", but S4 requires dead gods or a dead-god ruin. Reword it to "a dead god's will", or add `pantheon_silent_gods` to R1.
6. **The secret pairs** (D9, D19, D20) involve secret P1 rows. Under the owner's rule of 2026-10-05 they are shown here; in a real birth the refusal is said as "a conflict in the secret layer".
7. **The great gods' raisers:** the religious contest roles and the unnamed god's priests raise `great_gods_floor` by ruling, but only `break_gods_among_mortals` writes it as an `overrides` in the data. 22b reads `hint: religious` and `break_god_name_forbidden` for the others. Should these be written as `overrides` too, for the ledger's script check?
8. **Rows whose text needs the S6 calendar:** `moon_one_thirty` ("thirty-day cycle" → 28), `way_ritual_date` ("a festival or the dead days": the dead days leave with the fixed year), `anchor_midwinter` ("midwinter or the dead days"), `rate_seasonal` (unchanged).
9. **`rank_greater` "can … be the villain's god"** and the pantheon's `premise_binding` rule ("one god embodies the villain's answer") assume a villain's god in every birth. W1 pins one only when the threat calls for it (S1, S7). Both are to be reworded in 22a.
10. **C5:** a silent pantheon whose gods speak through the phenomenon. Recommend a clash; the owner's taste.
