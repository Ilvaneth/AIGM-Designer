# Build item 16c — the secret and villain rows of the general themes (SPOILER: the owner does not open this file)

*Written by the coding tab, 2026-10-04, for the development tab's audit (`docs/p1-build-16.md`, Part 16c). It names rows of the secret and villain tables.*

## Rows added

### Archetypes (`secrets.yaml#archetype`, 26 → 31)

**`secret_death_refused` — A death was refused** (class `cosmology`)

- statement: {Someone} should have died and was not let go; what holds them here is fed by {what}, and it has to be fed again.
- cause: the break is what the holding cost: {the chooser} gave {the target} so that one death would not stand
- clues: act1: someone who was seen to die and is seen again · act2: the one who feeds the holding, and what it eats · act3: the held one, and whether they wish to stay
- conflicts_with: none
- hooks: P5: the held one is an NPC with a dossier; one NPC who loved them knows

**`secret_mind_from_outside` — Someone is worn by a mind from outside** (class `creature`)

- statement: {A trusted person} let a mind from outside the world in, for {a reason that seemed good}; it has worn them for {years} and learns the land through their eyes.
- cause: the break is the mind's first act with a borrowed hand: {the chooser} opened themselves to it, and it moved them against {the target}
- clues: act1: a trusted person whose small habits are all a little wrong · act2: others who met the same mind and were let go · act3: the mind itself, and what it came to learn
- conflicts_with: ['break_no_direct_lies']
- hooks: P6: one site is where the mind was first met; its ecology is not of this world

**`secret_restoration` — It clears the ground for an old order** (class `polity`)

- statement: {An old order: an empire, a dynasty, a sworn order, a faith} never accepted its end; the break removes what was built over it.
- cause: the break is a clearing: {the chooser} broke {the target} because it stood where the old order means to stand again
- clues: act1: old emblems kept clean in a place that should have forgotten them · act2: those who still hold the old ranks, and who pays them · act3: the one who would sit in the old seat
- conflicts_with: none
- hooks: P4: one faction holds the old order's ranks in secret; its endgame is the restoration

**`secret_curse_fell_due` — A curse fell due** (class `history`)

- statement: {Someone} broke {a sworn thing} or wronged {a power} knowing what it would call down, and judged it worth it.
- cause: the break is the curse landing: {the chooser} did the wrong, and {the target} is where it fell
- clues: act1: the harm spares one house, one field, one name · act2: the sworn thing, and who witnessed its breaking · act3: the wronged power, and what would end the curse
- conflicts_with: ['break_oath_curse']
- hooks: P2: the wronged power is a god, a plane's keeper or a named force with the curse in its secret field

**`secret_dreamed_into_being` — It was dreamed first** (class `cosmology`)

- statement: {A sleeper} dreamed the break before it happened; {who} learned how a dream of theirs is made to hold on waking.
- cause: the break is a dream made to hold: {the chooser} put {the target} into the sleeper's dream, and woke them at the right moment
- clues: act1: people who dreamed the harm the night before it came · act2: the sleeper, kept and tended · act3: the next dream, being prepared
- conflicts_with: ['break_dreams_are_a_place']
- hooks: P5: the sleeper is an NPC who does not know what their dreams are used for

### Villain shapes (`antagonists.yaml#villain_shape`, 19 → 21)

- **`shape_outlaw_lord` — The lord of the lawless**: rules what the realm abandoned (a sea, a quarter, a road, a people nobody would defend); built the only order those people have, and will burn the realm before handing it back · hooks: P4: the BBEG's faction gives its own people a real order the realm never did; one NPC owes it their life
- **`shape_bargainer` — The bargainer**: gives people what they ask for at a cost they agreed to; holds that no one is wronged who chose, and collects without mercy · hooks: P5: three NPCs have struck a bargain with them: one glad of it, one ruined, one about to be collected from

Both joined `vis_process_or_institution`'s conflict list (a person, not a body or a working).

### Origins (`antagonists.yaml#origin`, 10 → 13)

- **`origin_refused_death` — They would not die**: conflicts_with ['shape_institution'] · hooks: P2: the day they should have died is a dated event; what keeps them is named, with what it costs others
- **`origin_cursed` — A curse was laid on them**: conflicts_with none · hooks: P2: who laid the curse, for what wrong, and what would lift it are written; the one who laid it is in the history or the roster
- **`origin_changed_from_outside` — Something from outside changed them**: conflicts_with ['shape_institution'] · hooks: P6: the place where it happened is a site; what changed them left more than one mark there

## Theme by theme: what carries it

| Theme | The break's true cause | The villain |
|---|---|---|
| the dead, the undead | **added** `secret_death_refused` | **added** `origin_refused_death` (any shape) |
| fiends | carried: `secret_the_hero_failed` with `chooser_bargainer` | carried: `origin_bargain`; **added** `shape_bargainer` |
| aberrations | **added** `secret_mind_from_outside` | **added** `origin_changed_from_outside` |
| elementals | carried: `secret_land_is_a_body` | carried: `origin_bargain`, `shape_warden` |
| artifacts and relics | carried: `secret_artifact_is_seal`, `secret_artifact_is_alive`, `secret_cover_for_a_taking` | carried: `shape_collector` |
| prophecy, the chosen | carried: `secret_prophecy_is_engineered` | carried: `shape_oathkeeper`, `shape_reformer` |
| empire | **added** `secret_restoration` | carried: `shape_heir`, `shape_dark_lord` |
| curses | **added** `secret_curse_fell_due` | **added** `origin_cursed` |
| plague | carried: `secret_cure_is_the_cause`, `secret_magic_is_a_disease`, `secret_enemy_is_us` | carried: `shape_process` |
| lycanthropes, shapeshifters | carried: `secret_king_is_a_copy` | carried: **added** `origin_cursed` serves it too |
| witches, hags | carried: `secret_set_someone_free`, `secret_the_hero_failed` | **added** `shape_bargainer` |
| pirates, thieves, assassins, slavers, hordes | carried: `secret_cover_for_a_taking`, `secret_wrong_target` | **added** `shape_outlaw_lord` |
| sea monsters | carried: `secret_land_is_a_body`, `secret_monsters_were_made` | carried: `origin_awakened_ancient` |
| dreams | **added** `secret_dreamed_into_being` | carried: `shape_process` |
| time | carried: `secret_planes_are_one`, `secret_history_looping` | carried: `origin_awakened_ancient` |
| knightly orders | carried: `secret_lesser_harm`, `secret_done_from_inside` | carried: `shape_oathkeeper`, `shape_champion` |
| slavery | carried: `secret_set_someone_free` | **added** `shape_outlaw_lord` |
| the dark lord | carried by any archetype | carried: `shape_dark_lord` (freed in 16a), with the rule below |
| the sleeper | carried: `secret_gods_are_prisoners`, `secret_artifact_is_seal` | carried: `origin_awakened_ancient` (freed in 16a) |

## The public dark lord and the secret villain

`shape_dark_lord` carries `same_figure_with: {contest_dark_lord: {visibility: vis_known_untouchable, role: a}}`. `design_identity.roll_secret` reads the field on every shape row:

- the contest is among the rolled contests and the visibility is `vis_known_untouchable` → the villain **is** the public dark lord: `bbeg_shape` is forced to `shape_dark_lord` (not rolled), the record's `public_figure` names the contest and role `a`, and when that contest is the main one `bbeg_pole` is fixed to `a`;
- the contest is rolled and the visibility is any other → the villain is another figure: `shape_dark_lord` is out of the shape pool and `public_figure` is null;
- the contest is not rolled → nothing changes; `shape_dark_lord` is an ordinary shape.

The rule is generic: another shape may name another public row the same way.

## The conflicts written in 16a on the freed rows

- `shape_dark_lord`: conflicts_with none
- `shape_whispering_advisor`: conflicts_with none
- `shape_secretly_evil_ruler`: conflicts_with ['vis_known_untouchable']
- `origin_awakened_ancient`: conflicts_with ['bond_product_of_it']
- `vis_process_or_institution` gained `shape_dark_lord`, `shape_whispering_advisor`, `shape_secretly_evil_ruler` (16a) and the two new shapes (16c): ['shape_heir', 'shape_rival', 'shape_parent', 'shape_convert', 'shape_survivor', 'shape_beloved', 'shape_stranger', 'shape_champion', 'shape_oathkeeper', 'shape_dark_lord', 'shape_whispering_advisor', 'shape_secretly_evil_ruler', 'shape_outlaw_lord', 'shape_bargainer']
- `secret_prophecy_is_engineered` lost its conflict with the deleted `forbidden_prophecy` and its hook was rewritten (16a).

## The new rows' conflicts with public rows

- `secret_mind_from_outside` with `break_no_direct_lies` (a worn person lives a lie, as the replacement does).
- `secret_curse_fell_due` with `break_oath_curse` (the trope break shows in public that a broken oath calls a curse down).
- `secret_dreamed_into_being` with `break_dreams_are_a_place` (the trope break shows in public that what is done in a dream holds on waking).
- `secret_death_refused` and `secret_restoration`: none. Read against `break_dead_rise`, `ruin_kingdom_of_the_dead`, `contest_living_dead`, `ruin_empire`, `contest_two_empires`: each public row tells a different thing from what the archetype hides.

## The word list

The test's attractor list lost `dead`, `undead`, `ghost`, `grave`, `tomb`, `funeral`, `corpse` (ruling 1: the dead are general material). It keeps the families of ruling 4.

## Corrected at the audit (2026-10-04)

- `secret_death_refused` conflicts with `break_dead_rise` and `contest_living_dead` (where the risen are an ordinary sight its trail has no first step).
- `origin_changed_from_outside`'s hook now names the choice: they went to it, or someone brought them to it, a dated act by a person in the history or the roster.
