# Build item 16 — the general themes

*Written by the development (design and review) tab for the coding tab, 2026-10-04, with the owner, part by part. The rulings and the approved rows are below the instruction. Where a source and this file differ, stop and report.*

**What it closes.** A survey of the 516 public P1 rows found no row at all for the undead, fiends, aberrations, elementals, artifacts and their pieces, prophecy, empire, pirates, witches, dreams or knightly orders, and `forbidden.yaml` refused twelve classic story shapes outright. The owner's ruling: a general Campaign Designer excludes no general D&D theme.

**Where it sits in the order.** After build 13a (the tables are English by then: the rows below carry no Turkish) and before item 11: 13a, **16a, 16b, 16c**, 11a, 11b, 12a, 12b, 13b, 14a, 14b, 15.

**Three green commits.** After each: the full suite green (the exit code), no commit before the audit, no push. Run nothing that calls a model. No secret or villain row in a summary.

| Part | What | Commit message |
|---|---|---|
| 16a | the forbidden list: twelve defaults go, one stays | `Plan item 25, build 16a: the forbidden defaults lifted` |
| 16b | thirty-one public rows | `Plan item 25, build 16b: the general themes, public rows` |
| 16c | the secret and villain rows the themes need | `Plan item 25, build 16c: the general themes, secret rows` |

## Part 16a — the forbidden list

- `forbidden.yaml` keeps one row, `forbidden_inherently_evil_races`, unchanged (ruling 3). The other twelve rows go with their `structural` checks, their `lexical` patterns and their `allowed_via` lists; every reference to them goes (rows' `forbidden: true` flags and `allowed_via` fields in `antagonists.yaml` and elsewhere, validators, rubrics, prompts, tests).
- The P1 rolls draw the three villain shapes, the one origin and the one faction archetype that were barred; the tests that assert "no forbidden shape or origin" assert instead that every row can be drawn.
- **One thing is not a cliché rule and stays as a table's own rule:** `factions.yaml#fracture` never takes `none`, because the living-world simulation needs a polity to have something to lose piece by piece. Keep that as the fracture table's own constraint, worded so, and say in the summary where you put it. If you find another barred value that guards a mechanism and not a taste, do the same and report it.
- The tables of P4, P7 and P9 that the freed values live in (`threads.yaml#truth_kind`, `arc.yaml#plot_engine`, `arc.yaml#opening_scene_type`, `factions.yaml#cult_doctrine`) simply lose the bar; nothing else of those floors changes here.
- Item 14's sixth rubric ("forbidden defaults") reads the one remaining row: is any people evil by birth?

**Tests of 16a:** the file holds one row; no reference to a deleted id anywhere; the freed rows are drawn over thousands of seeds with no conflicting set; the archived births pass.

## Part 16b — the public rows

- Add the thirty-one rows of Parts 1 to 3 below, with the ids, families, labels, statements and roles as written, in English only.
- **The technical fields are yours to write in the pattern of each family's existing rows, and to list for the audit:** a ruin source's `remnant_kind`, `sites`, `olgu_families` and any palette requirement or addition; a contest's `prize`, `seats`, `escalation` steps and role `hint`s; a trope break's hooks per phase and its tie weights; a lifeline's `where`; every row's `hooks`. The development tab's proposals for the hints and prizes are in the table "Proposed hints and prizes"; where one does not fit the tables' rules (every contest needs a hinted role among the roles a short campaign seats; a prize is one of lifeline, heart, remnant, new, thin place), change it and say so.
- **The pairs are rulings:** every "fits" is a `weight_by`, every "clash" a `conflicts_with` or a claim, every "merge" a `merges_with` line, every "requires" a `requires`. A pair ruled "no clash" gets nothing. No other conflict is added without a report.
- `break_magic_sold` carries the claim `magic: plentiful`. The enchanters' lifeline and practice require the magic dial at medium or high.
- "No row owns or sells magic" (plan item 25, the phenomenon signature) is lifted; delete the test that holds it, if one does.
- Reviewed stamps for the new rows, written before the summary and committed after the audit.

**Tests of 16b:** the rows exist with their families; over thousands of seeds every new row is drawn, no ruled clash stands together, every "requires" holds, no pool is empty; the floors of rule 8 hold; the whole-P1 measurement still reports zeros; `test_regression_births` is green.

## Part 16c — the secret and villain rows

For each theme of ruling 6 and of Parts 1 to 3, check whether the secret's archetypes and the villain's shapes and origins can carry it: could this theme be the break's true cause, and could its figure be the campaign's villain? Where none can, add a row, written and checked against the seven criteria of `docs/p1-build-9.md` section 1, with its conflicts against the public rows (old and new). In particular: when `contest_dark_lord` is rolled, decide by data how the public dark lord and the secret villain stand together (the same figure, or not), and make the visibility roll agree; report the rule's shape, not its rows.

The summary gives counts only: rows added per sub-table, per theme whether it was already carried. The row-level list goes to the development tab by path. The development tab reads every new row and reports counts to the owner.

**Tests of 16c:** as build 9's and 10b's: no conflicting set across public and secret rows over thousands of seeds; no empty pool; the chooser and tie equivalence; no secret row in a public file, the public dice log or a die's size; the archetype pool's floor.

## The summary (each part)

Changed files; new and changed tests; the suite's count and exit code; for 16b the technical fields you wrote, row by row, and every proposal you changed; for 16c the counts; anything unexpected.

---

## The owner's rulings (2026-10-04)

1. **A general Campaign Designer excludes no general D&D theme.** The dead and the undead, crowns, relics and their pieces, fiends, prophecies and the rest are general material, not the mark of one campaign (said of Ashen Crown's motifs). A theme is not left out because test births converged on it or because an earlier campaign used it.
2. **`forbidden.yaml`: twelve of the thirteen defaults go** (awakening ancient evil, the chosen one, prophecy as plot engine, the dark lord in a black tower, the generic evil cult, the corrupt church as default villain, the amnesiac hero, the tavern opening, the monolithic Empire, collect the N pieces, the whispering advisor, the ruler who is secretly evil), with their structural and lexical checks and their `allowed_via` lists. Plan item 25's line "no 'Empire', … no whispering advisor, no evil cult" is withdrawn.
3. **"No inherently evil people" stays, and is an unchanging rule** (`forbidden_inherently_evil_races`). The owner's wording: while a campaign is being formed everyone stays neutral in alignment; alignments are set when good and evil are placed, and good and evil are placed then. A people is never evil by birth. (Fiends and the undead are creatures, not peoples; a row about them does not touch the rule.)
4. **Not coming back** (owner, row families the tag review removed): courts, law and trials; money, debt, banks and tolls; light as a fuel or a commodity; hush and bells; tides and salt.
5. **"No row owns or sells magic" is lifted:** rows may make magic a trade.
6. **Every theme of the survey's list C gets rows:** fiends, aberrations, elementals, artifacts and relics, prophecy, empire, curses, plague, lycanthropes and shapeshifters, witches and hags, pirates, sea monsters, dreams, time, knightly orders, tribes and hordes, slavery, thieves and assassins. The owner approves the public rows one by one; the development tab adds the secret and villain rows the same themes need and reports counts only.

The survey (a keyword count over the 516 public P1 rows, 2026-10-04; a rough measure): zero rows for the undead, fiends, aberrations, elementals, artifacts, prophecy, empire, pirates, sea monsters, witches, dreams, knightly orders; one each for curse, plague, shapeshifters, slavery, thieves.

## Part 1 — the dead, fiends, aberrations, elementals (approved 2026-10-04)

**Ruin sources**

| id | family | label | statement |
|---|---|---|---|
| `ruin_kingdom_of_the_dead` | fallen_kingdoms | The kingdom of the dead | Its kings would not die: they ruled on as the undead until the living rose and broke them. The tombs are palaces, and not all of the court was destroyed. |
| `ruin_devils_bargain` | planes | The realm that bargained with devils | A kingdom bought its golden age from the Hells. When the bargain came due the devils took what was owed; its contracts still bind. |
| `ruin_demon_gate` | planes | The demon gate | A gate to the Abyss stood open for a generation. The land around it was scoured, and what came through was never all hunted down. |
| `ruin_deep_minds` | old_peoples | The drowned dominion of the deep minds | Before the peoples, aberrant minds ruled from sunken cities and kept thralls. Their dominion broke; their cities did not. |
| `ruin_bound_elements` | magic | The bound elements | A people chained elementals to turn their mills and warm their cities. The bindings failed all at once. |

`ruin_deep_minds` requires a sea, a lake or the underground in the palette.

**Contests**

| id | family | label | roles |
|---|---|---|---|
| `contest_living_dead` | nonhuman | The living and the dead | a: the living realm's lords · b: the undying lord and its risen subjects · third: the priests who can lay the dead · fourth: those who trade across the line |
| `contest_fiend_pact` | hidden_hand | The fiend behind the pact | a: the house that signed · b: its rival · third: the fiend's envoy (a rumour, like every hidden hand's third) · fourth: the fiend hunters |
| `contest_elemental_lord` | nonhuman | Mortals and the elemental lord | a: the settlers · b: the elemental lord whose domain they farm · third: those who serve it |

**Trope break**

| id | family | label | statement | at the table |
|---|---|---|---|---|
| `break_dead_rise` | danger | The dead rise unless they are laid | Anyone who dies without the rites rises within three nights. | every corpse is a task; a battlefield is a countdown |

Removed at the review: "The minds beneath" (a hidden-hand contest too like the fiend's and the shapeshifter's), "The bound elemental that serves the land" (a treaty lifeline; the same idea as the bound elements).

**Pairs (every one ruled)**

| Pair | Verdict |
|---|---|
| `break_dead_rise` with `contest_living_dead` | fits: ×2 |
| `break_dead_rise` with "Every ruin is someone's home" | no clash: the dead are the someone |
| `break_dead_rise` with "Night is safe and day is dangerous" | no clash: the risen walk by day |
| `break_dead_rise` with the ruin "The plague" | fits: ×2 |
| `ruin_kingdom_of_the_dead` with "The gods are the souls of mortal ancestors" | no clash: the undying kings wanted godhood |
| `contest_living_dead` with "The monsters hold treaties" | no clash; they merge: the treaty people is the dead |
| the priests of `contest_living_dead` with "Divine magic works only on holy ground" | no clash: the dead must be carried to holy ground |
| `contest_fiend_pact` with "Casting is forbidden" | no clash: a pact is signed, not cast |
| `contest_fiend_pact` with the other hidden-hand contests | never drawn together (one contest per family) |
| `contest_elemental_lord` with the treaty lifelines | as the other treaties: a treaty weighs its own contest ×2 |
| all of them with the six claim topics | none carries a claim |

## Part 2 — the relic and its pieces, prophecy, the chosen, the dark lord, the sleeper, the empire (approved 2026-10-04)

**Ruin sources**

| id | family | label | statement |
|---|---|---|---|
| `ruin_sundered_relic` | magic | The relic that was sundered | An artifact held the land together. It was broken on purpose, and its pieces were carried apart and hidden. |
| `ruin_dark_lords_fall` | wars | The dark lord's fall | A conqueror ruled from a black fortress until an alliance threw him down. His fortress, his captains' strongholds and his weapon remain. |
| `ruin_sleeper` | old_peoples | The sleeper under the land | Something older than the gods was bound asleep, and a people that is gone kept the watch. The watch-posts stand empty. |
| `ruin_empire` | fallen_kingdoms | The empire that ruled everything | One throne held every land. It fell, and each province kept a piece of its law, its roads and its legions. |

**Contests**

| id | family | label | roles |
|---|---|---|---|
| `contest_relic_pieces` | race | The pieces of the relic | a: a house that holds one piece · b: a house that holds another · third: the order sworn to keep the pieces apart · fourth: a finder with no banner |
| `contest_prophecy` | open_close | The prophecy's two readings | a: those who work to fulfil it · b: those who work to prevent it · third: the keepers of the prophecy · fourth: the one it names |
| `contest_dark_lord` | strong_weak | The dark lord and the free lands | a: the dark lord's dominion · b: the last free realm · third: those who have made terms · fourth: the exiles |
| `contest_two_empires` | two_hands | Two empires, one border kingdom | a: one empire · b: its rival · third: the kingdom between them · fourth: that kingdom's exiles |

**Trope break**

| id | family | label | statement | at the table |
|---|---|---|---|---|
| `break_chosen_are_many` | gods | The chosen are many | In every generation the gods mark a hundred chosen. Being chosen is common, known, and a burden with rules. | a PC may be chosen, and it does not make them special |

Removed at the review: "The cult that outgrew its cellar" (a contest; the cult is carried by the villain tables and P4's faction kinds), "A prophecy is law" (a trope break).

**Pairs (every one ruled)**

| Pair | Verdict |
|---|---|
| `ruin_sundered_relic` with `contest_relic_pieces` | fits: ×3; the relic is the ruin's remnant and the contest's prize |
| `contest_relic_pieces` without that ruin | no clash: the relic is a new prize |
| `contest_prophecy` with `break_chosen_are_many` | no clash: the one it names is one of the chosen |
| `contest_prophecy` with "Writing is unknown" | no clash: the role is "the keepers of the prophecy", not of a text |
| `contest_prophecy` with "No one can lie outright" | no clash: both readings can be honest |
| `ruin_dark_lords_fall` with `contest_dark_lord` | fits: ×2; they merge: the fallen lord's dominion has risen again |
| `contest_dark_lord` with "The enemy won and everyone is fine" | no clash; they merge: the enemy that won is the dark lord (role a) |
| `contest_dark_lord` with "Dragons rule the lands" | no clash: the dark lord may be one of the dragon sovereigns |
| `contest_dark_lord` with the secret villain rolls | no clash: the campaign's villain need not be the dark lord; the development tab rules the secret side |
| `ruin_sleeper` with the contest "The sealed remnant" | fits: ×3 |
| `ruin_sleeper` with "The imprisoned god" | one ruin source per campaign; never together |
| `ruin_empire` with "Guilds rule; there are no lords" | no clash: the empire is the past |
| `contest_two_empires` | both empires are foreign polities and carry no claim (rule 3) |
| the dominion of `contest_dark_lord` with "no inherently evil people" | no clash: a dominion is an organisation, not a people |

## Part 3 — curses, the beast-blood, the coven, pirates, dreams, knights, slavery, thieves, magic for sale (approved 2026-10-04)

**Ruin sources**

| id | family | label | statement |
|---|---|---|---|
| `ruin_great_curse` | catastrophe | The great curse | A wronged power cursed the land with its dying breath. Crops, births and luck all turned, and the realm emptied. |
| `ruin_beast_blood` | old_peoples | The beast-blood clans | Clans that took the shapes of beasts held the wilds until they were hunted out. Their blood still surfaces. |
| `ruin_sleeping_realm` | planes | The realm that fell asleep | A whole realm fell into one dream and did not wake. The dream is still there, and it can be entered. |
| `ruin_fallen_order` | wars | The fallen order of knights | A sworn order held the frontier until it was betrayed and broken. Its commanderies stand empty and its oaths were never released. |

**Contests**

| id | family | label | roles |
|---|---|---|---|
| `contest_coven` | nonhuman | The coven's bargain | a: the villages bound by it · b: those who would break it · third: the coven · fourth: the child that was promised |
| `contest_pirates` | strong_weak | The pirate lords and the harbour towns | a: the council of pirate captains · b: the league of harbour towns · third: a foreign navy · fourth: the smugglers who serve both |
| `contest_slavers` | strong_weak | Slavers and the chained | a: the slaver lords · b: the escaped and those who hide them · third: those who buy · fourth: a people taken whole |
| `contest_thieves_guild` | strong_weak | The thieves' guild that owns the city | a: the guild that runs the streets · b: the city's rulers, most of them on its payroll · third: a rival guild from outside · fourth: the watch captain no one can buy |

`contest_pirates` requires a coast or an island in the palette.

**Trope breaks**

| id | family | label | statement | at the table |
|---|---|---|---|---|
| `break_dreams_are_a_place` | danger | Dreams are a place | Sleepers walk one shared dream-land; what is done there holds on waking. | a long rest is a journey; an encounter can come in sleep |
| `break_oath_curse` | knowledge | A broken oath curses the breaker | Break a sworn oath and a curse falls on you. Everyone knows it, so oaths are few and heavy. | a promise the party gives is a mechanical burden |
| `break_magic_sold` | knowledge | Magic is bought and sold like bread | Spells and enchanted goods are ordinary trade, with shops and prices. | a magic item is bought at the market |

**Lifeline and institution practice**

| id | table | label | statement |
|---|---|---|---|
| `lifeline_enchanters` | lifeline, craft family | The enchanters' workshops | The land's wealth is enchanted goods, made to order and sold abroad. |
| `practice_enchanted_goods` | institution practice, guild and trade archetypes | They make and sell enchanted goods | Gives the party: enchanted goods to buy and to order. |

Removed at the review: "The horde at the wall" and "The shore folk and the beast of the deep" (contests too like existing rows), "The whale and sea-serpent hunt" (a lifeline).

**Pairs (every one ruled)**

| Pair | Verdict |
|---|---|
| `ruin_great_curse` with `break_oath_curse` | fits: ×2 |
| `ruin_beast_blood` with "Some lands' lord is a beast-person" | fits: ×2; no clash: the survivors rule |
| `ruin_beast_blood` with "no inherently evil people" | no clash: the row tells them as a hunted people, not as an evil one |
| `ruin_sleeping_realm` with `break_dreams_are_a_place` | fits: ×2 |
| `ruin_fallen_order` with the contest "An order splits" | fits: ×2 |
| `break_dreams_are_a_place` with "Going out at night is forbidden" | no clash: the ban holds the body, not the dream |
| `break_dreams_are_a_place` with "Night is safe and day is dangerous" | no clash |
| `break_oath_curse` with "No one can lie outright" | both of the knowledge family; never drawn together |
| `break_oath_curse` with the treaty lifelines | fits: ×2 |
| `break_magic_sold` with the magic dial at low | clash against a dial: the row is not drawn |
| `break_magic_sold` with the ruin "The spring that ran dry" | clash: the later row leaves the pool |
| `break_magic_sold` with "Casting is forbidden" | both of the knowledge family; never drawn together |
| `break_magic_sold` with "Magic is nobility" | no clash: the nobles sell it |
| `lifeline_enchanters`, `practice_enchanted_goods` | require the magic dial at medium or high |
| the same two with "Casting is forbidden" | no clash: a prohibition is not an impossibility; the workshops run unlicensed |
| the same two with `break_magic_sold` | fits: ×2 |
| `contest_coven` with the lifeline "The bargain with the fey" | no clash: two bargains, two powers |
| `contest_slavers`, `contest_thieves_guild` with the six claim topics | none carries a claim |

## Proposed hints and prizes (the development tab's; technical, not reviewed by the owner)

| Contest | a | b | third | fourth | prize |
|---|---|---|---|---|---|
| `contest_living_dead` | state | none | religious | trade | heart |
| `contest_fiend_pact` | state | state | none (a rumour) | martial | lifeline |
| `contest_elemental_lord` | state | none | religious | scholarly | lifeline |
| `contest_relic_pieces` | state | state | religious | none | remnant with `ruin_sundered_relic`, else new |
| `contest_prophecy` | religious | state | scholarly | none | new |
| `contest_dark_lord` | state | state | trade | resistance | heart |
| `contest_two_empires` | none (foreign) | none (foreign) | state | resistance | heart |
| `contest_coven` | state | resistance | none | none | lifeline |
| `contest_pirates` | criminal | trade | martial | criminal | lifeline |
| `contest_slavers` | criminal | resistance | trade | a people's role | new |
| `contest_thieves_guild` | criminal | state | criminal | martial | heart |

`contest_elemental_lord` was approved with three roles; a standard campaign seats four, so a fourth is added here: "the binders who would chain it again". Report it to the development tab if the wording should differ.

## The count

Thirty-one public rows: 13 ruin sources (the table goes from 40 to 53), 11 contests (40 to 51), 5 trope breaks (31 to 36), 1 lifeline (60 to 61), 1 institution practice (33 to 34).
