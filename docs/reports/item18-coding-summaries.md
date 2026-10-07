# Build item 18 — the coding tab's summaries

*One section per part, in the order of `docs/p1-build-18.md`. Written by the coding tab; audited by the development tab. No row of a secret table is named here: counts and positions only. The fit lists are `docs/reports/item18-fits.md`.*

## 18a — the layers; texture fills no story slot (committed `c0dfc40`, 769 tests, exit 0)

Summarised to the owner in the coding tab on 2026-10-05; the owner's two corrections at the audit (`prize_at` on four disputed lands, `key_kinds` on six key-place prizes) are in the commit. In short: every P0 and P1 table carries `layer`; `design_arbiter.STORY_SLOTS` (seven slots) and the one-way rule at the roll, at the set and at the door (`design_door.STORY_FIELDS`, filled by 18e); the lifeline left the targets and the prizes and is rolled last; 21 new prizes, two contests and `target_lifeline` retired (`retired:` lists, read by `design_tables.retired()`); 3,000 seeds with no texture in a story slot; the smallest contest pool 33 of 49. A product fault met on the way: a building and the calendar's special month could share a name (the calendar is now built first).

## 18b — trope breaks bend; the palette follows the spine

**Changed and new files.**
- Tables: `trope-breaks.yaml` (the eight world states: `layer: story` and `joins`; the dragons' lifeline weight removed; the two bent rows; the P8 hook on fifteen rows), `foundation.yaml` (`breadth` on the 30 spines; `count_by_spine` replaces the palette's `count_by_scale`), `reviewed.json` (restamped: 22 trope rows and 30 spines changed; no secret row changed).
- Scripts: `design_identity.py` (`is_world_state`, `joins_of`; a world state is drawn only where a join holds; its tie is never the lifeline, rolled with `slot="world_state_tie"`; the join is recorded; a join to the threat goes to dm-only), `designer.py` (`dice-log.json#identity.world_states`), `design_arbiter.py` (the piece kinds contest, ruin source, break, threat, hand, villain: story), `design_foundation.py` (the count by the spine's breadth; never under the spine's ends; `before_fill` on the count's record).
- Tests: new `test_world_states.py` (8 tests, 3,000 seeds, about 100 s); updated `test_foundation_tables.py` (the palette's count), `test_claims.py` (a table drawn many times reads `count_by_spine` too), `test_identity_secret_roll.py` (the dm-only identity's keys add `world_states`).
- Report: `docs/reports/item18-fits.md` (18b's two fit lists and their questions; 18a's key-place kinds for the record).

**The suite:** 777 tests, exit code 0 (the first run was red on one pinned key list, the dm-only identity's new `world_states`; fixed and run again).

**Many seeds (3,000, every scale × magic × era × tone):**
- No world state is drawn without a join; none is tied to the lifeline; a join to the threat is in dm-only only; every world state is still drawn. 900 of 3,000 births hold a world state. The joins: rulers by lot, guilds, magic nobility on the heart (104-119 each); dragons rule 3 on the dragon contest, 120 pending on the threat; the beast-lord 39 on a disputed land, 25 on a people side; the moon 20 on the thin place, 135 pending on a hand; the gods among mortals 14 on a faith contest, 109 pending on the threat; the enemy won 23 on a war ruin, 118 pending on the threat.
- The palette: every rolled count inside its band (tight short 2-3, standard 3-4, epic 4-5; wide short 3-4, standard 4-6, epic 6-8), every value of every band seen. Means: tight 2.85 / 3.56 / 4.55, wide 3.61 / 5.00 / 6.97. Over the band's top in 48 of 3,000 births (1.6 %), always when the forced kinds, the two needs (a height, a water) or an implied kind pass it; the scar's new kind and the ruin's kind come on top, as before.
- The smallest trope-break pool: 5 (the floor holds).

**Decisions a principle settled (listed for the audit):**
1. **The crossroads at short.** The spine has four ends and the layout seats the ends on different kinds (build item 6b); a count of 3 cannot. The count never falls under the spine's ends: the crossroads takes 4 at short, inside its band. No other spine has more than two ends.
2. **The two bent rows keep their ids** (`break_no_writing`, `break_divine_magic_holy_ground`): a secret table names one of them, and a rename would edit it. Their new wording (label, statement, `text`, the override, two hooks of the writing row, one of the holy ground) is the coding tab's from the rows document's meaning: please read it.
3. **The join recorded** is the first that holds on a rolled piece, in the row's order; else the threat's requirement.
4. **The dragons' lifeline weight** (`life_dragon_protection`) was removed: texture does not weigh a story row. The holy-ground row keeps its pilgrim-road weight (it is texture).

**Questions** (`docs/reports/item18-fits.md`): list 1 (six, the fifth is the one that matters for 18c: does the threat come before the trope breaks, as G4's order says, or does a world state weigh the threat's families, as part 18b says?), list 2 (the seven rows left without the P8 hook).

**The audit's corrections (the development tab, 2026-10-05), applied:** a join to the threat leaves the public record entirely (the world state stays public; its join lives in `dice-log.json#identity.world_states` alone); the enemy won also joins a ruin of the `fallen_kingdoms` family; the P8 hook added to maps are forbidden, dreams are a place and the gods among mortals (eighteen rows now); the writing row's statement and `at_table` as the development tab worded them. Answers recorded: the threat comes before the trope breaks in 18c (G4), and a join to the threat is then judged on the rolled threat; the hand rows carry a moon fit in 18c.

## 18c-1 — the threat (the first half of 18c, as the development tab allowed)

**Changed and new files.**
- Tables: `antagonists.yaml` (six new secret sub-tables: the family 19, the power source 5, the goal 20, the weakness 19, the lair's form 16 and where 7; two shapes, two origins and one visibility retired, one origin and one visibility added, as the specification names them; the tie's six rows retired; the conflicts that named a retired row removed; the god's weaknesses seven, as answered), `secrets.yaml` (the chooser's six rows retired; one twist's conflict with a retired tie removed), `reviewed.json` (restamped; the six new sub-tables join `REVIEWED_TABLES`).
- Scripts: new `design_threat.py` (the threat's rolls; the SRD creatures; the CR window; the fits); `design_foundation.py` (the threat rolled inside `roll` right after the contest and before the move, G4; kept on `R.threat`); `design_identity.py` (the visibility, the shape and the origin come from the threat; the chooser is `chooser_the_villain`, not rolled; the tie is not rolled, `None`; a world state's join to the threat is judged on the rolled threat, no pending state; a hand's join waits for 18c-2); `designer.py` (`R.threat`; `dice-log.json#threat`); `design_tables.py` (`REVIEWED_TABLES`).
- Tests: new `test_threat.py` (14 tests, 3,000 seeds and a 300-birth wait sequence; `--report` gives the variety report); updated `test_identity_secret_roll.py`, `test_secret_villain_tables.py`, `test_design_tables.py`, `test_world_states.py`.
- Reports: `docs/reports/item18c-fits-SPOILER.md` (the threat's fit lists and seven questions), `docs/reports/item18c-shapes-SPOILER.md` (the shape rows read: 3, of which 2 retired).

**The suite:** 789 tests, exit code 0.

**Many seeds (3,000: every scale × magic × era × tone, the content mixes, four start levels):** no dead end; the threat after the contest and before the move and the trope breaks; every creature inside its CR window or a reskin whose target is; the god never at short and always an avatar; a power source exactly on the five humanoid families above short; the goal on a piece the chain holds (the thin place only with the palette's); the weakness and the lair fitted; no chooser or tie rolled; a world state joined to the threat only when the rolled threat holds it; every family drawn.

**The variety report** (1,000 seeds per scale, the three-birth wait simulated): short 15 families, shares 5.3-8.4 %, no consecutive repeat, 970 distinct (family, creature, shape, goal) of 1,000, reskins 28.8 %, the join prize 34.0 % / role goal 11.3 % / move 54.7 %; standard 18 families, 4.3-7.9 %, none, 960, 48.9 %, 33.5 / 11.8 / 54.7; epic 18 families, 4.2-8.4 %, none, 922, 61.3 %, 30.5 / 13.6 / 55.9.

**Decisions (the development tab's answers applied):** the goal's join is `prize | role_goal | move`; a goal holding the prize weighs ×2; nothing forces 18c-1's break (the move of 18c-2 honours `move`); the visibility is rolled before the shape (16c's public figure); the order is family, creature, power source, visibility, shape, origin, goal, weakness, lair.

**A fault met while building:** forcing the old break onto a contest role whenever the goal missed the prize collapsed the move's targets (the closed thin place and two verbs were no longer reached); withdrawn, and the join recorded instead.

**Questions:** seven, in `docs/reports/item18c-fits-SPOILER.md`; one active shape row is listed in `docs/reports/item18c-shapes-SPOILER.md` for a reading.

**The audit's corrections (2026-10-05), applied:** the law of its nature fits the fey too; every family's lair-form pool reaches five (the development tab's four families, the dragons' colour forms, and the coding tab's widenings listed in the SPOILER fits file); the dragon's colour weighs its lair x3; every world state's join is public: a join to the threat counts only when the villain's visibility is known, and the dm-only join record is gone. **World states over 3,000 seeds after it:** 584 births hold one (900 before); rulers by lot 122, guilds 117, magic nobility 132 (all on the heart); the beast-lord 64 (disputed land 41, people side 23); the enemy won 107 (a war or fallen-kingdom ruin 55, a known villain 52); the moon 24 (the thin place; the hand comes with 18c-2); the gods among mortals 17 (a faith contest 13, a known god 4); dragons rule 9 (the dragon contest 3, a known dragon 6).

## 18c-2 — the move (the second half of 18c)

**Changed and new files.**
- Tables: `foundation.yaml#action` (23 verbs: 13 kept or rewritten with the rows' labels and targets, 10 new; 8 retired; `by` the hand → verb fit; `act_summoned` also strikes the heart and the key place, `act_poisoned` and `act_plague` also a role, as answered), `antagonists.yaml` (`#hand`, 27 public rows with their creature families, requirements and the moon fit; `#move_state`, 4 public rows; both `own_hooks_only`, so the file's antagonist hooks never reach the public ledger), `trope-breaks.yaml` (dragons rule: the dragon hand and the dragons' two ruins as public joins; the gods among mortals: a ruin of the gods' family; the moon: the trading and outside hands; both rare world states weigh x3), `secrets.yaml` (one weight that named only a retired verb removed), `reviewed.json` (restamped).
- Scripts: `design_foundation.py` (the move: hand → target → verb, as answered; the goal → target relation with the guards and the thin place's weight; the move's join `prize_piece | role | side_holding`; the move's state, none for a coming move; `move.at`; the start never the heart, `start_part`; `foundation.move` public with the hand's creature families; the threat's families secret; the layout split in two, `lay_out_story` before the move and `lay_out_finish` after the lifeline), `design_identity.py` (the hand and ruin joins of the world states), `design_promises.py` (`own_hooks_only`).
- Tests: new `test_move.py` (10 tests, 3,000 seeds; `--report`); updated `test_foundation_tables.py`, `test_foundation_roll.py`, `test_promises.py`, `test_trope_claims.py`, `test_world_states.py`, `test_identity_roll.py`, `test_secret_villain_tables.py`.

**The suite:** 800 tests, exit code 0.

**The order of the move, amended:** hand → target → verb → time → state → the stronger role (the development tab amends docs/p1-build-18.md).

**Faults met while building:** (1) the hand, a public sub-table of the secret `antagonists.yaml`, inherited the file's antagonist hooks, and they reached the public promise ledger (`test_promises` caught it); fixed with `own_hooks_only`. (2) With the verb drawn before the target, the target's weights could not act (thin place 0.9 %); fixed by the order.

**The move over 3,000 seeds** (`test_move.py --report`, start levels 1, 4, 7 and 10): targets role 36.7 %, key place 29.6 %, remnant 16.6 %, heart 14.6 %, thin place 2.5 % (3.1 % at start level 1 alone); joins prize 33.8 %, move/side holding 27.3 %, move/role 20.5 %, role goal 12.5 %, move/prize piece 5.8 %; all 27 hands (26-154 each), all 23 verbs (19-407 each); the start end_a 38.2 %, end_b 32.6 %, key place 25.2 %, along 3.9 %, never the heart; the state done 20.5 %, stopped short 20.7 %, backfired 18.8 %, unnoticed 20.2 %, none (coming) 19.7 %; world states magic nobility 125, lottery 120, guilds 110, gods among mortals 83, enemy won 76, dragons rule 54, moon 54, beast-lord 47.

**The variety report with the threat** (`test_threat.py --report`, unchanged by the move): short 15 families, 970 distinct (family, creature, shape, goal) of 1,000; standard 18, 960; epic 18, 922; no consecutive repeat.

**Questions:** three, in `docs/reports/item18-fits.md` (18c-2).

**The audit's correction (2026-10-05), applied:** carried off destroys nothing (the side remains, now with a cause); drove out destroys the heart only (the side lives on in exile). The answers: the cult's `served` and the ruin's `ruin` stay for P6; the verbs' forms stand.

**A test made steady after the correction:** `test_identity_roll`'s lineage share over the deep contests rests on about 20 births in these seeds, too few for a bound of 28 % to hold every time (the correction's new dice gave 4 of 20). The weight is now tested without dice (`design_identity.lineage_weigh`, extracted from the roll unchanged: the deep role's three lineages weigh x3), and the share only has to pass the no-weight baseline of 16 %.

## 18d — the secret is the threat's hidden half

**Changed and new files.**
- Tables: `secrets.yaml` (the header and its four common hooks on the chain; `archetype` retired whole (31, readable); `twist`, 20: the nineteen kept archetypes on the chain, their texts moved mechanically ({the chooser} → the villain, the break → the move, act → stage), and `twist_greater_power`; the old twists retired under it; `keeping`, 16: the old twists less "a PC is involved", the two rewrites (the move grew larger than the villain meant; the villain works to undo it, only with `move_backfired`) and the two additions; `trail`, 11: `stages` for `acts`, the third element carrying how the villain is stopped, `trail_omen_divination_dead` new; every header states its `avoid_used`), `antagonists.yaml` (the new rows' promises, G6: the goal → P4, the weakness by its row → P2/P5/P6, the lair → P6, the power source → P2/P6 by kind, the god → P2, the hand → P4, the hero bound to the threat → P9 on the family; the god family's two forms), `reviewed.json` (restamped; `secrets.yaml#keeping` joins `REVIEWED_TABLES`).
- Scripts: `design_identity.py` (`roll_secret`: the twist with mystery always, else on a d2; the keeping; the trail; `secret_facts`, the four facts (three when the villain is known); `secret_stages`, three stages with their conclusions, levels and three clues each: the chain's at the hand's base, where the move struck, the lair or the goal's piece; one to P5, one to P6; `archetype` keeps the twist's id for the readers of earlier births), `design_threat.py` (the god's form), `design_promises.py` (the nine clue promises: `clue_stage` for the chain's three, the validator's stages; `clue` for the six to P5 and P6; the start to P3 and the creature families to P6, public; the villain's own creatures to P6, secret; the legacy branch reads an old trail), `design_door.py` (`clue` is a script source), `design_check.py` (the clue_order comment: stages for every birth with a ledger), `design_tables.py`.
- Tests: new `test_secret_layer.py` (3,000 seeds; the legacy secret); updated `test_secret_villain_tables.py`, `test_identity_secret_roll.py`, `test_design_tables.py`, `test_promises.py`, `test_p1_dry_walk.py` (the stand-in reads the twist when one was rolled), `test_identity_roll.py` (the dice share dropped, as answered: the deterministic `lineage_weigh` test stands alone).
- Report: `docs/reports/item18d-secret-SPOILER.md` (the twists, the keeping, the trails and the weakness hooks, for the reading).

**The suite:** 810 tests, exit code 0 (the first run was red on one test that looked for the retired archetype's roll label; fixed).

**Many seeds (3,000):** four facts in every birth (three hidden when the villain is known); three stages with three clues each, the chain's clue of stage 2 where the move struck and of stage 1 never on the heart; the twist always with mystery, about half without; no retired row rolled; nine clue promises in every secret ledger, the clues to P5 and P6, the hero to P9, the goal to P4; the public ledger the same with and without the secret rolls and naming none of them.

**The lineage test (answered):** the dice share is dropped; the deterministic test of `lineage_weigh` stays.

**Questions:** in `docs/reports/item18-fits.md` (18d).

**The audit's corrections (2026-10-05), applied:** the keeping's 16 stands; the hand's base (`base: far_end | inside` on the 27 hands; the traitor, the deceived side and the shapechangers inside: the heart, or the deceived side's seat on the side the move made stronger), read by stage 1's clue and by a coming move's start (never the heart: a base in the heart starts at the first end); the twenty twists' texts written by hand under the development tab's rules (no break or destroying for the move, one sentence of what is true, the protector a story actor, the old kingdom, the made people victims, the greater power's statement), the old and the new side by side at the end of the SPOILER file. The other readings and the ids stand.

## 18e — the writer, the rubrics and the card on the chain

**Changed and new files.**
- Tables: `secrets.yaml` (`god_relation`, 5 secret rows (W1); four twists that name a piece require it: the prize is a seal needs a new or remnant prize, the relic is a person a remnant or new goal, it was done before a ruin of a fallen kingdom or a war, the monsters were people a hand of reshaped creatures), `signatures.yaml` (`mechanic_shape`, 6 rows (W6); the institution's P7 hook: it offers or colours quests and never originates the main thread), `rubrics.yaml` (`rubric_p1_secret_trail` as the threat's hidden half; `rubric_p1_question_concrete` with the prize and the goal as stakes; new `rubric_p1_legible`), `reviewed.json` (restamped).
- Scripts: `design_foundation.py` (the tokens `prize:<kind>` and `hand_family:<family>`; `spine_sentence`, `prize_phrase`; `foundation.spine_sentence`), `design_threat.py` (the token `goal_piece:<piece>`, secret), `design_identity.py` (the pin: a god with its rolled relation only for the god family, the patron's will or the greater power, else the thin place or the remnant; the event is the move; each stage's chain clue carries its `piece`), `designer.py` (the mechanic's shape rolled when the gate says yes: `identity.mechanic`), `design_arbiter.py` (the slot `secret_pin`), `design_door.py` (`STORY_FIELDS`: the clues' pieces and the pin's piece; `appears` as `{phase, hook, text}`, the hook restating a table hook word for word; `true_rule` only with `serves_clue`; `secret_class` is `threat` without a twist; the hook is no prose for the name scan), `design_promises.py` (a note binds the hook it restates and brings its text as `advice`; `sync` saves when any promise changed), `design_approval.py` (the card: THE STORY first, the secret line in counts, the `D&D:` line; the gate `dnd_incomplete`), `design_prompts.py` (`P1_ROLLS`: the move, the threat and the secret, read with the Read tool, never with Bash).
- Prompts: `P1.premise.md` rewritten on the chain (the writer makes concrete, never decides: W1-W7); `templates/design/premise.md` (the story sentence, the stakes, "What it was" gone, the secret as the threat's hidden half, the clues by stage at the chain's places, the mechanic from its shape).
- Tests: new `test_p1_story.py`; updated `test_p1_dry_walk.py` (the stand-in writer on the chain), `test_door.py`, `test_p1_writer.py`, `test_p1_critics.py`, `test_p1_card.py`, `test_layers.py`, `test_design_tables.py`.

**The suite:** 822 tests, exit code 0 (the first run was red on six: the chain's tokens were not in `claims.yaml`'s registry, now they are; pinned key lists and counts).

**Faults met while building:** (1) the door's name scan read an `appears` note's `hook` (a table's own sentence, with "NPCs" and "PC" in it) as invented proper nouns; the hook is no prose now. (2) A note that restates its hook joins that hook's promise; `design_promises.sync` saved the ledger only when a new promise appeared, so the note's source and advice were lost unless something else changed (the dry walk hid it, `test_door` showed it); it now saves on any change. (3) The table script put the twists' requirements on the retired archetype copies (the same ids), first in the file; moved onto the twist rows.

**The signature mechanic's shapes (W6), for the owner:** a meter that fills (4-8 steps, 2-3 thresholds); a favour ledger (2-4 sides, 3-6 favours to call); a corruption track (5-10 steps, 2-4 thresholds); a reputation clock (4-8 segments, 2-4 factions); a bargain's debt (3-6 debt, 1-3 payments); a countdown (6-12 ticks, 2-3 warnings).

**The god relations (W1):** five rows of a secret table; per this tab's standing rule they are not written in a summary: they are at the end of `docs/reports/item18d-secret-SPOILER.md`.

**The rendered prompt:** `P1.premise.md` is 8,217 characters before the common block and the Names and Promises paragraphs are rendered into it (it was about 7,600). The questions are in `docs/reports/item18-fits.md` (18e).

## 18e-2 — the story sentence reads as D&D (the fourth coding tab)

**Twenty sentences** (standard scale, mixed dials, fresh seeds `OWNER-18E2-0` … `-19`), for the owner:

 1. A generation ago, the risen dead killed a suspicious hunter; now one household and the other household fight over an inheritance.
 2. A bound elemental carried off the leader of the prophecy's heralds; now the prophecy's heralds and the prophecy's foes fight over the prophecy.
 3. A war band is driving the mercenary company out; now the capital and the march lords fight over the land of the march lords.
 4. A generation ago, a golem army killed the leader of the ambitious branch; now the penitent branch and the ambitious branch fight over the island-city in the lake.
 5. A hired company is about to betray the torn ruler; now the old temples and the fast-spreading new faith fight over the city inside the mountain.
 6. An unwitting faction is about to drive the people out of the capital; now the capital and the march lords fight over the land of the march lords.
 7. Things from beyond are possessing the leaders of the sworn order; now a house with one piece and a house with another fight over the pieces of the relic.
 8. Slavers are carrying off the leaders of the road-closers; now the open-road traders and the road-closers fight over the trails that link the clearings.
 9. A dragon opened the stairs between the terraces; now the strongest house and the richest house fight over the city on the middle terrace.
10. A cursed pack cursed the other new power; now one of the new powers and the other new power fight over the island-city in the lake.
11. Shapechangers seized the strait; now the bound villages and the bargain-breakers fight over the land of the bound villages.
12. Slavers are plundering the old dragon lairs; now the prophecy's heralds and the prophecy's foes fight over the prophecy.
13. Brigands are about to besiege the city on the strait; now a country and the neighbouring country fight over the land between them.
14. A generation ago, the risen dead seized the glass desert; now the old leadership and the breakaway branch fight over the glass desert.
15. A coven of hags is replacing the leaders of the would-be explorers with impostors; now the would-be explorers and the wardens of the way fight over the invaders' fortresses.
16. A hired company is betraying the old order's soldiers; now the old nobles and the reformers fight over the bridge-town over the rift.
17. A zealous order is seizing the gilded contract halls; now the bound villages and the bargain-breakers fight over the land of the bound villages.
18. A generation ago, a coven of hags opened the giants' buildings; now the old leadership and the breakaway branch fight over the giants' buildings.
19. Brigands killed the ruler of the crossroads city; now the magic-holding bloodline and the casterless majority fight over the crossroads city.
20. A generation ago, a foreign army opened the tunnels between the valleys; now the would-be explorers and the wardens of the way fight over the clans' hill-forts.


**Changed files.**
- Tables: `foundation.yaml` (`#action`: the passive `forms` replaced by `phrases`, active with the hand as subject, one entry per target piece or `piece.kind`, three tenses, `{be}` and `{target}`; `fits` now name the role kinds too and were narrowed where a phrase read false; the header's note; `role_kinds: [group, settlement, person, creature]`; `#contest`: a `short` on 121 of the 196 roles and a `kind` on 52 (27 settlements, 20 persons, 5 creatures), `text.prize` on seven contests, the header's note; `#spine`: `heart_short` on 12 rows and `key_place_short` on 16; `#ruin_source`: `remnant_short` on 14), `antagonists.yaml` (`#hand`: `number` and `text.subject` on the 27 hands; two villain family labels quoted, see below), `secrets.yaml` (new secret sub-table `greater_power`, 4 rows, one a god; the header's label list), `reviewed.json` (restamped).
- Scripts: `design_foundation.py` (`target_kind`, `role_kind`, `role_short`, `verb_phrase`, `subject_of`, `move_clause`; the verb's fit reads the role's kind among the roles it may strike, and the struck role is drawn among those; `spine_sentence` in active voice with "A generation ago," and the short names; `prize_phrase` by the short names and `text.prize`; the rendering's break line carries the move's clause; `out.villain_label` names the villain itself by its family's public label), `design_identity.py` (the greater power's kind rolled with its twist, `secret.greater_power`; a god pinned for it only when the kind is a god).
- Prompt: `P1.premise.md` (two clauses: `greater_power` in the secret layer's list and in the twist's line).
- Tests: `test_foundation_tables.py` (the phrases: every kind a verb fits has a phrase, `{be}`/`{target}`, active voice; the role kinds in the compatibility tables; three pinned fits), `test_foundation_roll.py` (the rendering's clause; the struck role's kind), `test_move.py` (no verb on a kind it does not fit, 3,000 seeds), `test_general_themes.py`, `test_identity_secret_roll.py`, `test_written_in_english.py` (the pinned values above), `test_p1_story.py` (the shorts at five words, the hands' subjects and numbers, the greater power's table; 300 sentences: the hand opens the sentence, its verb agrees with its number, no agent phrase, the sides and the prize by their short names; the pin by the power's kind).
- Reports: `docs/reports/item18-fits.md` (18e-2: the verb × kind list, the phrases, the shorts and kinds, the prize names, the hands' subjects, five questions); `docs/reports/item18d-secret-SPOILER.md` (the greater power's four rows).

**The suite:** 825 tests on the final product files (51.8 min, one process): red on four tests that pinned values the new fields change, no product fault: `test_foundation_tables` (two verbs' role kinds now hold `settlement`), `test_general_themes` (a ruin's text may hold `remnant_short`), `test_identity_secret_roll` (the dm-only secret holds `greater_power`), `test_written_in_english` (a spine's text may hold `heart_short` and `key_place_short`). Fixed in those test files alone; the four modules then: 84 tests, exit code 0. The full run that gates the commit was started at once; its count and exit code come with the commit. **The suite now takes about 50 minutes** (13 at build 11a): the many-seed tests of item 18; 18f takes the fix.

**Over 3,000 seeds** (`test_move.py`; start levels 1, 4, 7, 10): no verb on a kind it does not fit; the targets unchanged from 18c-2 (role 36.7 %, key place 29.6, remnant 16.6, heart 14.6, thin place 2.5); all 27 hands and all 23 verbs reached (19-494 each: seized 494, carried off 293, killed 277, drove out 270, opened 222, sealed 212, cut off 193, plundered 115, cursed 110, enslaved 90, corrupted 90, raised in revolt 74, betrayed 68, drowned 61, woke 60, summoned 57, a plague 57, burned 56, divided 54, poisoned 51, replaced 46, dragged into a plane 31, possessed 19). The kinds struck: a group role 829, the heart 439, a crossing 268, a descent 203, a structure remnant 195, a city remnant 148, a settlement role 136, a road network 126, a gate 119, a person 112, the thin place 75, then landmark 53, water 51, bridge 44, object, machine and network remnants 29 each, a creature 24, rift 24, wasteland 23, crossroad 23, body 16, source 5.

**Decisions a principle settled** (each listed with its rows in the fits file):
1. **A verb fits a kind when its phrase reads true for every row of that kind**; the narrowed fits: carried off (an object remnant, never a place), opened, burned, drowned, plundered. Woke keeps its kinds through two phrases ("woke what sleeps in" a structure, "woke what sleeps beneath" a key place).
2. **Role kinds, not numbers.** With the hand as the subject, the target is the object: no verb agrees with it. A role that is one being takes a person or creature phrase ("killed the elder heir", "possessed the dragon"); a settlement role (a city, villages, a realm, a state) takes the heart's phrase for drove out and a plague and "enslaved the people of". The specification's "a group with its number" is the first question.
3. **Short names beyond the roles:** places whose text runs past six words, offers an alternative ("the border fortress or the last bridge") or names a structure as the heart carry a `*_short`; a role's short where its text leans on another phrase ("its rival" → "the rival house") as well as past five words.
4. **The subject's phrase** is the hand's name cut to its subject on eight hands ("a traitor within", "an unwitting faction", "the woken power of the ruin", "fiends", "shapechangers", "a corrupted druid circle", "a war band", "a dragon").
5. **The greater power** is rolled at the pin (after the stages); since the audit for the patron's goal too, label `P1.secret_power` (below).

**A fault met on the way:** two villain family labels held a comma inside parentheses unquoted, so YAML cut the label at the first comma and read the rest as empty keys (stray `None` fields in the rows). Quoted; their rows' stamps changed with it.

**Questions:** five, in `docs/reports/item18-fits.md` (18e-2).

**The audit's corrections (2026-10-06), applied:** (1) a remnant short wherever the remnant text is no clean object in "<hand> <verb> <target>": 23 more ruins (37 of 53 now; listed in the fits file), so sentences 12 and 18 above read "plundering the old dragon lairs" and "opened the giants' buildings"; (2) one rule for a power behind the villain: the twist "a greater power stands behind the villain" and the goal "a patron's will" roll its kind once from `secrets.yaml#greater_power` (label `P1.secret_power`), and the secret is pinned to a god only when the family is the god or that kind is a god. The answers: the `settlement` role kind, the place shorts and the structure hearts as towns, `text.prize` and seized at 16.5 % stand.

## 18f-1 — the shared many-seed corpus (the fourth coding tab)

**The suite's time:** before (77d5339, 825 tests): 3,080 s, 51.3 min. After (825 tests, the same tree but for the replaced assertion below): 1,702 s, 28.4 min, 45 % less. The corpus is rolled once (3,000 prerolls, about 5 min of it); what remains is mostly the tests that keep their own seeds (about 17,000 foundation-only or P0/P4 rolls) and the campaign-making tests (the dry walk, the real births).

**What changed.** A new `tests/_corpus.py`: in-memory P1 prerolls (`designer.preroll_p1`), rolled once per test process and read by every many-seed test whose dials it holds; the i-th birth depends on i alone (seed `CORPUS-<i>`), so a test that asks for n births reads the first n, whoever asked first; it grows on demand to 3,000 and is never cached on disk (every birth is rolled from the tables and the code under test). The dials go round every scale × magic × era × tone (135), every content mix of three (60) and every danger; the start level goes round every band the scale's span allows (start = 1 + (i // 135) % (20 − span), the band [start, start + span]); a birth that stops on an empty pool is kept as an error (`_corpus.errors`), never skipped silently. The births are shared and read-only: each read checks a digest of every birth's records (foundation, identity, secret, threat, names, roll logs, pools, the arbiter's context) taken when it was rolled, and fails if an earlier reader changed one.

**The moved tests** (every assertion as it was, only the births' source changed; the corpus's dials are test_promises' scheme):

| Test (births) | Its dials before | Against the corpus |
|---|---|---|
| `test_promises` (2,400; ledgers built per birth, once) | every scale × magic × era × tone, content mix, danger, every start band | **the same dials**; its own seeds gone |
| `test_move` (3,000) and its `--report` | start levels 1, 4, 7, 10 (top capped at 20), no danger; foundation and identity only | wider: every band, the dangers; the full preroll |
| `test_threat` ManySeeds (3,000) | start levels 1, 4, 7, 10, capped | wider |
| `test_secret_layer` (3,000) | start levels 1, 4, 7, 10, capped | wider |
| `test_world_states` (3,000) | start level 1, no danger; foundation and identity only | wider; the full preroll (the roll's raw output, unread, is no longer kept) |
| `test_layers` ManySeeds (3,000) | start level 1, no party size, no danger; the foundation only | wider; the full preroll (its pools now hold every P1 table, all above 0) |
| `test_identity_roll` ManySeeds (2,700) | start level 1, no danger | wider |
| `test_identity_secret_roll` ManySeeds (1,800; P4 rolled on each) | start level 1, no danger | wider; P4 now stands on a copy of P1's context (it used to write its rolls into P1's, which the corpus shares) and is seeded with the P1 birth's own seed |
| `test_name_pools` (2,400, 600, 480, 120, 40) and `test_door` (480, through it) | start level 1, no danger | wider; one record per birth, shared by all sizes |
| `test_p1_story` ManySeeds (1,500) | start level 1, no danger | wider |
| `_floor.smallest_pools` (900; test_claims' floor) | start level 1, no danger | wider |

**Kept their own seeds** (dials or a mechanism the corpus does not hold): `test_threat` Variety (300, the family's three-birth wait simulated across the sequence) and its `--report` (1,000 per scale, the wait); `test_trope_claims` (1,620: it spies on the arbiter during the rolls); `test_foundation_roll` (2,250 and 4,000: its own eras and start levels, and it reads the roll's raw output); `test_arbiter_faults` (3,000, fixed magic and era, the foundation only); `test_claims`' role and layout loops (400 per scale, 1,500: fixed tone and mix, the foundation only); `test_forbidden_lifted` (2,000 P4 rolls); `test_p0_dials` (2,000 P0); `test_secret_villain_tables` (450 with P4).

**One assertion replaced, as answered:** `test_identity_roll`'s "the case was exercised" (a role-destroying verb on a role while the main contest has a single institution home) held by luck on the old seeds: over the corpus's 3,000 births the case occurs 0 times (single-home births 78, Divided on a role 60; 18e-2 narrowed Divided to group and settlement roles). `design_foundation.strikable_roles` and `strike_role` are lifted out of `roll` with no behaviour change; the many-seed check of every birth stays (no violation, the record when it applies); the new `test_the_last_home_is_protected_without_dice` proves the protection on every one-home contest and scale of the tables (4), with the Divided verb on six seeds each: the home is never among the roles it may strike, the struck role is another of a kind it fits, and the home is on the verb's record. It replaces the dice-dependent count.

**Changed files:** `tests/_corpus.py` (new), `tests/_floor.py`, `test_identity_roll.py`, `test_identity_secret_roll.py`, `test_layers.py`, `test_move.py`, `test_name_pools.py`, `test_p1_story.py`, `test_promises.py`, `test_secret_layer.py`, `test_threat.py`, `test_world_states.py`; `scripts/design_foundation.py` (the two lifted functions). The unused `itertools` imports and two helpers the move left dead (`run`, `dials_of`) are removed.

**The suite:** the timing run above (825 tests, 28.4 min) was red on one test only: the replaced "exercised" assertion, loaded before its fix. After the fix: the new test passes alone; the gating full run on the final tree: 826 tests, OK, exit code 0, 1,381 s (23.0 min).

## 18f-2 — the chain measured and walked (the fourth coding tab)

**Twenty spine sentences, for the owner** (standard scale, mixed dials, seeds FRESH-202610061840-4984-0 … FRESH-202610061840-4984-19):

 1. A generation ago, a monstrous beast besieged the city on the middle terrace; now the penitent branch and the ambitious branch fight over the city on the middle terrace.
 2. A generation ago, slavers enslaved the native hunters; now the crown's official expedition and a mercenary company fight over the tower of ascension.
 3. A generation ago, a cult replaced the leader of the exiles with an impostor; now the dark lord's dominion and the last free realm fight over the city in the middle layer.
 4. Brigands drove the collaborating local nobles out; now the occupiers and the resistance in the mountains fight over the largest island.
 5. A foreign army sealed the great shaft; now the old nobles and the reformers fight over the city in the middle layer.
 6. A coven of hags is about to poison the leader of one half of the city; now one half of the city and the other half fight over the town by the crater's stone.
 7. Sea raiders opened the way down to the floor; now the shrine's old keepers and the new faith fight over the gods' fallen weapons.
 8. A generation ago, fiends seized the thin place; now the open-road traders and the road-closers fight over the gates of the wall.
 9. Things from beyond are about to seize the only safe strait; now a country and the neighbouring country fight over the land between them.
10. A generation ago, shapechangers opened the stairs between the terraces; now the old temples and the fast-spreading new faith fight over the city on the middle terrace.
11. A traitor within is raising the native hunters in revolt; now the crown's official expedition and a mercenary company fight over the experiment centre.
12. A cursed pack is about to curse the neck of the peninsula; now the penitent branch and the ambitious branch fight over the city near the neck.
13. A coven of hags is corrupting the strait between the lakes; now the magic-holding bloodline and the casterless majority fight over the city on the strait.
14. A traitor within is seizing the thin place; now the crown's official expedition and a mercenary company fight over the stone roads and their forts.
15. A monstrous beast is about to seize the glass desert; now the landowning lords and the peasants' union fight over the city at the belt's middle.
16. A cursed pack is spreading a plague among the profiteering merchants; now the land's old owners and the newcomers fight over the land between them.
17. Shapechangers are about to seize the oasis's water; now the land's old owners and the newcomers fight over the land between them.
18. An unwitting faction carried off the order's steward; now the old leadership and the breakaway branch fight over the experiment centre.
19. A generation ago, a dragon seized the black fortress; now the house that signed and the rival house fight over the seat of the house that signed.
20. A cursed pack is about to burn the only bridge over the void; now the old temples and the fast-spreading new faith fight over the city above the void.

**The whole-P1 measurement** (`tests/p1_measure.py`, over the shared corpus):

**The measures (3000 corpus births; docs/p1-threat-first.md's findings)**

- 1. texture in a story slot: 0 births; the lifeline as the move's target 0.0 %, as a prize 0.0 % (before item 18: 17.8 % and 43 %, one or both 52.6 %)
- 2. a move with a hand: 100.0 % (27 of 27 hands); the goal joins the contest by move 53.9 %, prize 34.0 %, role_goal 12.0 %
- 5. a threat with a goal, a weakness and a lair: 100.0 %; its families drawn: 19 of 19 (rows not named: secret)
- 4. the secret's three stages with three clues each: 100.0 %
- 6. world states drawn: 726 in 702 births; joined: 100.0 %
- 8. the palette by the spine's breadth (the scar's and the ruin's kinds on top): tight epic 4.49 (band 4-5); tight short 2.81 (band 2-3); tight standard 3.55 (band 3-4); wide epic 7.06 (band 6-8); wide short 3.61 (band 3-4); wide standard 4.99 (band 4-6); over the band's top 45 (1.5 %: the forced kinds and the needs alone; 18b measured 1.6 %)
- the story sentence: 100.0 % of births

**The move (test_move --report, on the corpus)**

3000 seeds
targets: role 37.0 %, key_place 29.3 %, remnant 16.8 %, heart 14.1 %, thin_place 2.8 %
joins: prize/None 34.0 %, move/side_holding 27.0 %, move/role 20.8 %, role_goal/None 12.0 %, move/prize_piece 6.2 %
hands: 27 of 27, 31-151 each; verbs: 23 of 23, 23-512 each
start: end_a 40.6 %, end_b 30.7 %, key_place 25.1 %, along 3.5 %, end_c 0.1 %, end_d 0.0 %
state: move_backfired 20.9 %, move_unnoticed 20.6 %, move_stopped_short 20.2 %, move_done 19.6 %, None 18.6 %
world states: magic_is_nobility 151, rule_by_lottery 142, no_kings_only_guilds 99, gods_among_mortals 94, the_enemy_won 94, beasts_own_land 53, moon_trades 47, dragons_rule 46

**The threat's variety (test_threat --report: its own births, the three-birth wait)**

short: 15 families drawn; share max 8.4 %, min 5.3 %; consecutive repeats 0; distinct (family, creature, shape, goal) 970 of 1,000; reskins 28.8 %; the join: prize 34.0 %, role goal 11.3 %, move 54.7 %
standard: 18 families drawn; share max 7.9 %, min 4.3 %; consecutive repeats 0; distinct (family, creature, shape, goal) 960 of 1,000; reskins 48.9 %; the join: prize 33.5 %, role goal 11.8 %, move 54.7 %
epic: 18 families drawn; share max 8.4 %, min 4.2 %; consecutive repeats 0; distinct (family, creature, shape, goal) 922 of 1,000; reskins 61.3 %; the join: prize 30.5 %, role goal 13.6 %, move 55.9 %

**Changed and new files.**
- Scripts: `designer.py` (`phase rerun` clears the validator's last result beside the door's; the preroll's names line gives the old tongue "no roots (the old tongue names its sites from its bag's parts)"; the report counts the runs and the ones not merged; `merge --run-dir` records its runs as merged), `design_manifest.py` (a row whose status reaches merged drops its `last_error`: a refusal a later fragment answered never reaches the next prompt), `design_door.py` (`later_floor`: an `appears` note may name `play`, and the phenomenon's play hook asks for one like any floor), `design_promises.py` (a `play` note joins its hook's promise), `design_approval.py` (the cards: "attempt N · correction round K" in the header, a section for the round, the card before the round kept as `P1.attempt-N.round-K.card.md`; the critique record refuses a finding that is not a pass with no reason code and records a code that carries a secret term as `secret_term`: `secret_code_terms`, `carries_secret`), `design_revise.py` (the round's record names its revision, the entities it reran and the ones it affected), `design_cost.py` (`record` marks a run it records by itself as not merged), `design_prompts.py` (the writer's prompt carries the phase critic's fix), and `.claude/workflows/design-fanout.js` (a phase fix routed through `covers`, its findings in the fix agent's text): #5 below.
- Prompts: `critic.md`, `phase_critic.md` (every finding that is not a pass has a reason code slug that never names a secret row or a secret name).
- Tests: new `test_p1_birth_faults.py` (7 tests: the phase critic's fix on a covered row, the stale refusal, the correction round on the card, the reason codes, the old tongue's line, the Read tool in the three P1 prompts, rerun and the validator); `test_p1_dry_walk.py` (three wrong turns on the chain: a texture piece in a clue's place, a hidden truth that serves no clue, a missing lair closing the D&D gate through card and approve; the walk sees the phenomenon's play note accepted); `test_root_cause_1.py` (a run no merge recorded reaches the ledger, counted apart); new `p1_measure.py` (the report above; no test: the rules it reports are asserted by the many-seed tests).

**The test birth's faults (docs/reports/p1-test-birth-1.md section 6), one by one:**
1. The Bash read of dm-only refused by the classifier: the writer's prompt and both critics' read lines say "with the Read tool, never with Bash" (already since 18e); now pinned by a test.
2. An unmerged Workflow's cost: `design_cost.py -c CAMP record --phase PN --run-dir DIR` records it, marked `merged: false`; `merge --run-dir` marks its own merged; the report reads "(N run(s), M not merged)". The protocol has to say when the conductor runs it (a Workflow that returned failed or was stopped).
3. (The protocol's reading of a failed Workflow: the protocol's, not code.)
4. The phenomenon's play floor: the door accepts `{phase: play, hook, text}` and asks for it (the phenomenon rule's `hooks_common` has a play hook, so every birth's phenomenon carries one); the note joins the play promise, which closes no phase's gate (12b).
5. The phase critic's `fix` that reached no writer (the audit's addition): the cause was in `.claude/workflows/design-fanout.js`, which looked for the entities a phase `fix` names among the roster's units only; P1's roster is the premise, and the critic named a signature row and a break row the premise's fragment writes. Now (a) a phase fix on a row a unit writes beside itself (the same prose file) belongs to that unit: `design_approval.unit_of`, `phase_fixes_due`; (b) `phase PN begin --json` serves the due ones (`designer.serve_phase_fixes`): the unit goes back to its writer once per attempt (a unit whose re-critique at `PHASE_FIX_LOOP` (4) is recorded, or that begin served, is not served again), its entry carries `phase_fix` (the findings: rubric id, entity id, reason code) and `covers` (the rows it writes), and its prompt reads "**The phase critic's fix:** <rubric> on <entity> (<code>)" with the pointer to `phase.critique.md`; (c) the gate shows `phase_fix_due` until it is served; (d) the workflow routes an in-run phase fix through `covers` to the unit and puts the findings in the fix agent's text (a first run's rows are not known to it yet: begin serves those). The critique records now carry their `attempt` and `loop`. Proved model-free by `test_a_phase_critic_s_fix_on_a_covered_row_reaches_the_premise_s_writer`.
6. Reason codes checked against secret terms: a code whose words hold a secretly rolled row's id, its distinctive tail (two words, or eight letters) or a secret name is recorded as `secret_term`; the report and the public manifest never hold it.
7. The stale `last_error`: cleared when the row's status reaches merged (reconcile, at every merge and begin).
8. A null reason code: a finding that is not a pass with none is refused at the record; the return stays in staging.
10, 11. The card and the correction round: header "attempt 1 · correction round 1"; the section "CHANGES FROM THE PREVIOUS CARD (correction round 0 → 1)" with the round's scope and revision, what it reran (public ids; secret ones counted) and which public files changed since the card before (by digest); that card is kept.
13. The old tongue's 0 roots: the line says why.
And item 17's note: `phase rerun` clears the validator's last result.

**Decisions a principle settled:** a correction round's own text is not printed on the card (the owner's sentence may name a secret; the scope and the revision id stand for it); a reason code with a secret term is redacted, not refused (refusing would stop the critic's chain on a word); the secret terms leave out single short words of row ids (`lairat_remnant` → `remnant` is no term) to spare ordinary codes.

**The suite:** 836 tests, OK, exit code 0, 1,536 s (25.6 min, with the measurement running beside it), before the audit's addition (#5). The gating run on the final tree: 837 tests, OK, exit code 0, 1464 s (24 min).

## 19a — what the second test birth showed (the fourth coding tab)

**Two fresh births** (standard scale, mixed dials; the pitch is the writer's, so here are what it is made of: the story sentence, the campaign's question, the part where step 1 lands):

- `FRESH19A-60`, the hand a side of the contest (role a, its public face): "A generation ago, the bound villages opened the thin place; now the bound villages and the bargain-breakers fight over the land of the bound villages." · question: Flesh vs spirit · step 1 lands at the key place.
- `FRESH19A-0`: "A zealous order split the street guild in two; now the street guild and the bought rulers fight over the fortress-city in the greatest pass." · question: The one vs the many · step 1 lands at the first end.

**1. The deceived hand's public face.** The hand's row named the secret in every public record, not only in the sentence: its id (`hand_deceived_side`, in the public dice log, `design.json#foundation.move` and the ledger's `from`), its label (the public ledger's promise names) and its subject. Now:
- the row is `hand_contest_side` ("A side of the contest (a contest role makes the move)", words "a side of the contest"); `design_tables.ROW_ALIASES` reads the old id for legacy births; the deceit is said only in the writer's prompt (the mirror tells how) and the table's comment;
- the side is a contest role, `foundation.move.hand_role`: the side the move made stronger (the 18d answer), unless the move strikes that very role (then the main contest's first other role; `design_foundation.deceived_role`); the hand's base and a coming move's start read that role;
- the sentence's subject is the role's short name, its verb agreeing with the role's number: a new `number` on 56 contest roles where the kind's default is wrong (a group plural, every other kind singular): 50 singular groups (a guild, a faith, a house, a company, "a people", …) and 6 plural settlements (villages, the coastal cities); `design_foundation.role_number`;
- the writer's prompt: the public files name the side by its name (`move.hand_role`) and never say it was deceived.
The other hands' subjects, read for the same fault: none changed. "a traitor within" and "shapechangers" stay (the world knows a traitor struck, or faces were worn); for your reading: "a bound elemental" says someone bound it (the world sees an elemental; the binding may be its own secret), and a move whose state is "unnoticed" (nobody ties the move to anyone) still names its hand in the public sentence.

**2. The public "No people evil by birth — checked" section** is gone from the template; the prompt asked for no line (its bar keeps the rule); `rubric_p1_forbidden`'s question adds "Judged on the prose as written: the premise holds no line that says it was checked." A legacy premise holding the section still merges (tested).

**3. No plane is named at P1.** The prompt's bars say so; the door refuses a plane's name in P1 prose (`design_door.plane_names`, `planes_in`): every baseline plane's label of planes.yaml and its local name, but the Material Plane and the demiplanes; a name with "Plane" in any case, every other as a name is written (capitalised: "the grey country" and "what in the nine hells" are ordinary words). Public prose and public fields: the line names the plane; the dm-only prose: a count, the names in the dm-only door log. The refusal reaches the writer's next prompt as its `last_error`.

**4. The pitch carries the question.** The prompt and the template: "three sentences, no secret, three jobs: a threat with a face; the campaign's question, asked in this world's words and never answered; the first session's task, where step 1 lands"; the prompt's bar; `rubric_p1_legible`: "Does the player pitch show a threat with a face, ask the campaign's question in this world's words without answering it, and give the party something to do in the first session?" and fails when "the pitch does not ask the question, or …".

**5. A critic judges its rubrics only.** The critic and phase critic prompts: each finding names the rubric whose question the text fails; a fault no rubric asks about is a `note`, never a `fix`. `design_approval.py critique` refuses a `fix` (or `rerun`) finding on a rubric the critic was not given: `design_prompts.given_rubrics(phase, kind)` from the same `rubric_rows` the prompt renders (the entity critic, the phase critic, the skeleton critic with its `rubric_skeleton_*` bullets; no check where no rubric list is rendered: a detail critique, the wishes critic); `design_approval.return_kind` now gives a return's kind for both the check and the record; the phase kind also accepts `rubric_wishes` (a legacy wishes return saved as `critic.json` reads as a phase return).

**From the birth's report (6-8):**
6. `_common.md`, the block every writer and critic reads: "list files with Glob, read them with Read, write them with Write; Bash runs only the commands your prompt gives you, never on a path under `design/`, and you write no helper script of your own".
7. `phase PN report`: "fix reasons: entity critic 1: … ; entity critic 2: … ; phase critic: … ; wishes critic: …" (grouped by the critic that gave them, entity critics first).
8. A promise judged not kept and later kept: the ledger records `flipped: {from, after_fix, attempt}` (after_fix: the phase critic's `fix` verdicts so far); the report adds one line "judged not kept, then kept after fix N: <ids>" (a secret one by count).

**Changed files:** `data/design/antagonists.yaml` (the hand renamed and reworded), `foundation.yaml` (`by` lists; role `number`s; the contest note), `rubrics.yaml`, `reviewed.json`; `scripts/design_foundation.py`, `design_identity.py`, `design_tables.py`, `design_door.py`, `design_prompts.py`, `design_approval.py`, `design_promises.py`, `designer.py`; `prompts/design/P1.premise.md`, `critic.md`, `phase_critic.md`, `_common.md`; `templates/design/premise.md`; tests: new `test_p1_birth2_faults.py` (15 tests), `test_p1_birth_faults.py` (its phase-fix test on a rubric the phase critic is given), `test_move.py`, `test_foundation_roll.py`, `test_secret_layer.py`, `test_p1_story.py`, `test_attractor_cleanup.py` (pinned values).

**The suite:** 852 tests, OK, exit code 0, 1,851 s (30.8 min; the new tests make about 4 campaigns more). The run before it was red on three pinned values the change left behind (a wishes return saved under another name than `wishes.critic*` reads as a phase return: the wishes rubric is now allowed there; test_p1_story's own subject helper for the side of the contest); both fixed, then this clean run.

**The audit's corrections (2026-10-06), applied:** (1) "a bound elemental" has the public subject "an elemental" (the world sees an elemental, not its binding; the binding stays in the row's own text and dm-only). (2) A move whose state is "unnoticed" has a hand nobody knows (the refined correction): the hand is a secret roll; its id, label, role and creature families go to the threat's dm-only record (`dice-log.json#threat.hand`: `{id, role, families}`), its `hand_family:` tokens are secret, and every public record shows the move without it (`foundation.move.hand`, `hand_role` null, `families` empty; `threat.families.public` empty, the hand's families in `secret`). The sentence's subject is "someone" for a hand of people (its families hold `humanoid`), "something" for any other, singular; the writer's prompt says the public files and the pitch do the same and points at `threat.hand`. **The order:** the time and the move's state now come before the hand (neither reads it; a move still coming has no state): time → state → hand → target → verb → struck role → scars → stronger role (`docs/p1-build-18.md` G4 says hand → target → verb → time → state → the stronger role: yours to amend). The time's one conflict (`time_coming` with two scars) now works the other way: a coming move's scars leave those two out. **What read the public hand, and how it reads now:** the sentence and the rendering (the subject above, from the families held in memory, never written); the start (only a coming move reads the hand, and a coming move has no state: unchanged); the stage-1 clue at the hand's base (`secret_stages` reads `threat.hand`); the world states' join through the hand (the moon, dragons rule: the public hand only, so a hidden hand joins none); the card's D&D line (its hand and families ticks read `threat.hand`); the hand's own hooks (the P4 front) go to the secret ledger with the roll; the public promise of the creature families to P6 holds none of the hand's, and a new secret promise does (`facts.creature_types.hand`: "the creature families of the hand nobody saw"); the verbs' `by` filter reads the hand in memory. Test: over the corpus every unnoticed move opens with "someone" or "something" and no public surface (the rendering, the public ledger, the public rolls, the foundation) carries the hand's id, label or family token. The gating run on the final tree: 853 tests, OK, exit code 0, 1863 s (31 min).

## 19b — a hidden villain can pass as a person (the fourth coding tab)

*The visibility and mask rows are secret tables; they are named here by count and rule, the rows themselves in `docs/reports/item18d-secret-SPOILER.md` (19b, at the end).*

**The rule.** Of the five visibilities, one hides the villain as a person among people (its rule: three or four plausible candidates, the truth one of them); the two that put a face in front of it (a visible front; known but the wrong person) and the two that do not hide it (known and untouchable; known but nowhere to be found) need no mask (`design_threat.HIDDEN_AMONG_PEOPLE`). Such a villain must pass as a person at the table (`design_threat.passes_as_person`, reading the SRD index):
- a humanoid (50 SRD creatures);
- a Shapechanger, Change Shape or Illusory Appearance whose text names a humanoid form: the metallic dragons (adult and ancient bronze, gold, silver; ancient brass and copper), the couatl, the deva, the doppelganger, the green, sea and night hags, the oni, the succubus/incubus. **Read the spec's "Shapechanger trait" narrowly:** the imp's and quasit's shapes are beasts and the mimic's objects, so a Shapechanger alone does not pass;
- a disguise spell (disguise self, alter self, seeming) it casts at will, by the day or from its slots: the lamia, the rakshasa;
- the vampire in its own form: its shapes are a bat and a mist, its own form passes; the SRD text cannot say so, so the mask table names it (`passes_in_its_own_form`, three vampire entries) for the owner to read.
Otherwise a **mask** is rolled from a new secret table (`antagonists.yaml#mask`, 4 rows, rolled after the goal and before the weakness), recorded as `threat.mask` (and `threat.passes_as_person`), its token `mask:<kind>` secret; its hook promises it to P6 (an item at a site: the disguise item, the glamour's anchor) or P4 (a mortal among the candidates: the possessed or bound mortal, the agent who wears its name). The writer's prompt points at `threat.mask`.

**The weakness.** The mask is a fourth candidate where it fits: a new weakness row, strip its mask and the mystery breaks (`requires` the token of a disguise item, a possessed or bound mortal, or a glamour; every family; `by_mask` lets it past a family's own weakness list). The agent who wears its name is no mask the villain stands behind, so it does not fit (your reading).

**The index.** `build_design_index.py` records per monster the spells it casts at will, by the day or from its slots (`spells_daily`) and whether a shapeshifting feature names a humanoid form (`takes_humanoid_form`); `srd-index-2014.json` rebuilt (monster-ecology.yaml unchanged).

**Over the corpus (3,000 births):** the villain hides as a person among people in 599 (20.0 %); 255 of them pass as people (42.6 %), 344 wear a mask (11.5 % of all births): the disguise item 97, the glamour 83, the possessed or bound mortal 82, the agent who wears its name 82; no mask outside that visibility; all 19 families still drawn (the mask is rolled after the family, the creature and the visibility, so their shares do not move); the weakness of the mask is drawn in 14 of the 344 masked births (4 %), always with a mask it fits.

**Changed files:** `data/design/antagonists.yaml` (the mask table; the weakness row), `claims.yaml` (the four `mask:` tokens), `srd-index-2014.json`, `reviewed.json`; `scripts/build_design_index.py`, `design_threat.py`, `design_tables.py` (`REVIEWED_TABLES`); `prompts/design/P1.premise.md`; tests: new `test_hidden_villain.py`, `test_threat.py` (the pinned counts: weakness 20, mask 4).

**The suite:** 860 tests, OK, exit code 0, 1,941 s (32.3 min). Two faults met on the way, fixed before it: the mask table inherited the file's antagonist hooks into its promises (`own_hooks_only: true`, as the hand's in 18c-2); the weakness of the mask counted as a candidate for every family even without a mask (`weakness_fits(row, family, mask)`: only with a mask).

## 19c — the tests never touch a live guard (the fifth coding tab)

**The runtime.** `paths.runtime_dir()` honours `AIGM_TEST_RUNTIME` (the name avoids the `DND_` and `CLAUDE_` prefixes the tests strip from their subprocesses), but only when it points inside `tempfile.gettempdir()` and is not that directory itself (`paths.test_runtime()`); it then comes before the project's `.runtime` and `DND_RUNTIME_DIR`. `tests/_campaign.py` sets it at import to a fresh `aigm-runtime-*` directory before any test computes a path, and removes it at exit (only the process that made it; a test process started by a test inherits the parent's directory). Every test that arms, disarms or reads the marker therefore works on the suite's own `active-design.json`, as do the scripts and hooks those tests start (`TestCampaign.env` passes the variable on). `tests/_layouts.clean_env` drops it, so a throwaway layout project keeps its own `.runtime`. `MarkerGuard` (both copies) stays, now on the suite's marker. Every module that touches the runtime imports `_campaign` first; `test_designer.py`'s module-level `MARKER` comes after that import.

**The proof** (`tests/test_live_guard.py`, 8 tests): the suite's runtime is its own (in the temporary directory, not the project's; `MarkerGuard.marker` there; a script a test starts sees it); the override is ignored outside the temporary directory, for the temporary directory itself and when empty; a layout's environment drops it. `LiveMarker` leaves a live marker as it is, or writes a sentinel when none exists and removes it after, runs two campaign tests in a fresh process (one arms the guard with `designer.py new`, one disarms it with `abandon`) and finds the marker with the same bytes **and the same modification time**. Checked against the old `_campaign.py` by hand: same bytes, new modification time (the old guard removed the marker and wrote it back), so the test fails on the old code.

**Line endings.** `paths.write_text_keeping_eol(path, text)` writes in the endings the file already has (CRLF when it holds a CRLF, otherwise LF; a new file LF). Every script that rewrites a tracked file uses it: `build_design_index.py` (monster-ecology.yaml, the index; the two paths now come from `output_paths()`), `design_tables.py stamp` (reviewed.json), `merge_srd_defenses.py`, `build_rules_index.py`, `build_srd.py`, `build_supplemental.py`, `data_pull.py` (meta.json; its downloads stay raw bytes as fetched). `build_design_index.py` run in the main tree leaves `git status` clean (monster-ecology.yaml is `i/lf w/crlf` here). Tests: the helper keeps CRLF and LF and writes a new file in LF; an index build over a CRLF ecology copy and an LF index copy changes neither byte; no writer keeps a fixed `newline="\n"`.

**The override refused while armed** (your answer to my note; the owner's word on the matcher). `hooks/design_read_guard.py`: while a design marker is armed (any mode, any session, any caller: the conductor, a designer agent, the DM at the playtest table), a Bash or PowerShell command that names `AIGM_TEST_RUNTIME` or `DND_RUNTIME_DIR` is refused with the reason (it would move the scripts' own marker checks to an empty runtime). The guard now also reads PowerShell commands as it reads Bash (dm-only paths, the registry and secret-dice verbs) and Glob calls (its path, its pattern and the two joined, as the paths it touches; designer agents allowed, as for Read). `.claude/settings.json`: the read guard's matcher is `Read|Grep|Glob|Bash|PowerShell` (the owner approved both additions in this tab). Tests in `test_design_read_guard.py`: the override refused in Bash and PowerShell, for an agent, for another session and in playtest mode, allowed unarmed; PowerShell and Glob on dm-only refused for the conductor and an ad-hoc agent, allowed for a designer agent, a public Glob allowed.

**Left open, for your call:** a Glob or Grep whose path is an ancestor of `design/dm-only` (say `design/` with `**/*.md`) still passes, as the existing Grep test on `design/` expects; refusing it would need a rule for recursive patterns under an ancestor.

**Changed files:** `.claude/settings.json` (the matcher); `scripts/paths.py`, `hooks/design_read_guard.py`, `build_design_index.py`, `design_tables.py`, `merge_srd_defenses.py`, `build_rules_index.py`, `build_srd.py`, `build_supplemental.py`, `data_pull.py`; `tests/_campaign.py`, `tests/_layouts.py`, `tests/test_design_read_guard.py`; new `tests/test_live_guard.py`.

**The suite:** before the guard rule 868 tests, OK, exit 0, 1,906 s; the gating run after it 871 tests, OK, exit code 0, 1,878 s (31.3 min). The project's `.runtime` was empty before and after; no `aigm-runtime-*` directory was left in the temporary directory. (A run started before the Glob request was stopped and rerun; while cleaning up after it I also removed two older leftover fixture copies, `campaigns/_test-manifest-4224-5f4d17` and `_test-revise-8412-f62df6`.)

## 19d — no search reaches dm-only through a parent folder (the fifth coding tab)

**Who.** The rule binds a caller who may not read dm-only: the conductor in birth and detail mode, an ad-hoc agent in any mode and the player agent in a playtest. Designer agents of the allowed types and the DM at the playtest table stay free, as for Read. As before, another session's marker does not apply.

**Grep and Glob** (`design_read_guard._ancestor_search`). The search root is the call's `path`, or the payload's `cwd` when it has none. When that root holds the marked campaign's `design/dm-only` or `design/_staging` (or lies inside one), the call is judged against the files there now (`_protected_files`): what it could print at that moment.
- A Grep with no `glob` and no `type` is refused.
- Otherwise the filter is applied to those files, and the call is refused when any file gets through. A Glob's `pattern` is the filter.
- Globs are read as ripgrep reads them (`_glob_hits`). With no slash, a glob matches any one path segment, so `*.md` reaches `dm-only/arc.md`. With a slash, it is anchored at the search root, and a glob that matches a folder takes in everything under it. `{a,b}` is expanded, and a leading `!` excludes (`!{dm-only,_staging}` passes; `!dm-only/npcs/**` does not).
- A `type` keeps the files whose extension is the type's (`TYPE_EXTS` for md, markdown, json, yaml, txt and csv; any other type is its own extension).
- So `**`, `**/*.md`, `*/*.json`, `*.md`, type `md` or `json` over `design/` are refused; `npcs/*.md`, `*.py`, type `py`, and `design/*.md` from the campaign folder pass.

**Bash and PowerShell** (`_shell_roots`). The command is split on `;`, `&&`, `||`, `|` and newlines. Each part is tokenized: POSIX for Bash; for PowerShell, non-POSIX with the quotes stripped, so backslash paths survive. `VAR=` prefixes are skipped.
- Recursive forms: `grep`, `egrep` and `fgrep` with `-r`/`-R` (also inside a cluster such as `-rn`) or `--recursive`; `rg`, `find`, `tree`, `ag`, `ack`, `rgrep` and `git grep` always; `ls` and `dir` with `-R` or `/s`; `gci`, `Get-ChildItem`, `Select-String` and `sls` with `-Rec…`; `findstr` with `/s`.
- Roots: the arguments that exist as paths, a wildcard argument cut at its first wildcard segment, or the working folder when none is given. Git Bash `/c/…` paths are read as `C:/…`.
- A recursive form whose root holds a protected folder is refused, whatever its own filters (`--include`, `-g` and `-Filter` are not judged; the refusal names the Grep/Glob route). Non-recursive listings (`ls design`, `Get-ChildItem design`) and searches below the protected folders' parent (`grep -rn … design/npcs`) pass.

**Tests** (`test_design_read_guard.py`, 13 tests, 2 new). The old line that expected a Grep over `design/` to pass now expects a refusal; `design/npcs` passes. Each Grep and Glob form above is tested in both directions, with no path through `cwd` (the project refused, the skill folder allowed). A designer agent is allowed, an ad-hoc agent refused, and another session's marker does not apply. Thirteen shell forms are refused and seven allowed; `rg` with no path through `cwd` is tested both ways. A designer agent's `grep -rn` is allowed. In the playtest, the DM is free, while the player's shell and Grep searches are refused.

**The birth protocol** (`docs/p1-test-birth-2.md`). It has no conductor search step: the conductor runs `designer.py`, `design_cost.py`, `design_revise.py` and `design_names.py`, the Workflow and the review block. No rule here blocks a step it names. One friction: while the guard is armed, a conductor's Grep or Glob with no path in the project root is refused, since the project root holds the campaign. The reason says to give a path outside the campaign's design folder.

**Changed files:** `scripts/hooks/design_read_guard.py`, `tests/test_design_read_guard.py`.

**The suite:** 873 tests, OK, exit code 0, 2,258 s (37.6 min). `.runtime` empty after; no `aigm-runtime-*` left.

## 20a — the script frames P1's rows (the fifth coding tab)

**The frame** (new `scripts/design_frame.py`). At `phase P1 begin`, for a birth whose P1 the script rolled, the script writes `design/_staging/P1/<premise id>.frame.json` (`designer.phase_begin` → `design_frame.write`; a `.frame.json` is no fragment, `design_io.NON_FRAGMENT_SUFFIXES`). It holds every row the writer owes: the premise, one signature per slot and one break per rolled trope break. Each row is a `registry` with every field the rolls set and the text fields standing empty, plus `fill` (the fields the writer writes) and `fragment` (where the row goes). The door does not read the file an agent could edit: it rebuilds the frame from the records (`design_frame.build`) and compares every premise, signature and break row with it (`design_frame.frame_errors`, called in `Door.unit_errors`). A missing, changed or reshaped frame field is refused by its dotted name (`` `stamped` must be an object, as the script's frame has it ``; `` `dm_only.clues[].levels` differs from the script's frame; the rolls set it ``). A refusal never prints a frame value, since a dm-only field's value is secret. On top of that: each filled stamp must equal the row's own field (`stamped.question` = `question`); a signature's id must be `signature_<slug of its name>`; and the premise's `signatures` must be the three signature rows' ids.

**My readings, for your audit:**
- **A signature's id and name are the writer's.** The id follows the name it picks from the four candidates, as the common preamble's id rule has it, so the frame cannot fix them. For the same reason the premise's `signatures` (and its stamp) are filled, and the door checks that they agree.
- **`kind` is fixed by slot**, as both real writers chose it: people `creature`, institution `institution`, phenomenon `magic`.
- **Languages.** The premise's and the breaks' `lang` is the second living language (`common`, or `other_side` when "no common tongue" was rolled). A signature's `lang` is its candidates' language.
- **One `appears` note per hook.** The frame gives a note for each hook a signature's tables gave a later floor (the second birth's writer wrote two P4 notes for two P4 hooks); its `phase` and `hook` are the frame's, its text the writer's.
- **The pin.** `pinned.event` is the pin's rolled event ("the move"); `pinned.god` is filled only when the pin is a god's.

**The fields the writer fills, per row type:**
- **premise:** `summary`, `question`, `pitch`, `signatures`, `refs`, `stamped.question`, `stamped.signatures`, `dm_only.secret`, `dm_only.villain_answer`, `dm_only.dm_pitch`, `dm_only.clues[].kind`, `dm_only.clues[].how`, and `dm_only.pinned.god` when the pin is a god's. The writer may add prose fields such as `world_default`.
- **signature:** `id`, `name`, `aliases`, `summary`, `rule`, `refs`, `appears[].text`; `dm_only.true_rule` / `serves_clue` stay optional.
- **break:** `aliases`, `summary`, `refs`.

**A frame printed for one birth** (`design_frame.py -c _test-frame-demo show`, seed FRAME-DEMO, standard; a throwaway campaign, deleted after; the institution's signature and one break shown):

```json
"premise": {"fragment": "design/_staging/P1/premise__test_frame_demo.json", "registry": {"id": "premise__test_frame_demo", "type": "premise", "name": "The premise", "aliases": [], "summary": "", "file": "design/premise.md", "secrecy": "public", "created_phase": "P1", "origin": "birth", "lang": "other_side", "question": "", "pitch": "", "tensions": ["tension_ambition_contentment"], "signatures": [], "trope_breaks": ["break_lineage_homes_inverted", "break_no_common_tongue"], "secret_class": "polity", "stamped": {"question": "", "signatures": [], "trope_breaks": ["break_lineage_homes_inverted", "break_no_common_tongue"]}, "dm_only": {"secret_twist": "secret_restoration", "secret": "", "villain_answer": "", "dm_pitch": "", "pinned": {"piece": "thin_place", "event": "the move"}, "clues": [{"n": 1, "levels": [1, 4], "kind": "", "piece": "end", "how": "", "placed_in": null}, {"n": 2, "levels": [5, 8], "kind": "", "piece": "thin_place", "how": "", "placed_in": null}, {"n": 3, "levels": [11, 12], "kind": "", "piece": "end", "how": "", "placed_in": null}], "stamped_fields": ["secret_twist"]}, "refs": []}, "fill": ["summary", "question", "pitch", "signatures", "refs", "stamped.question", "stamped.signatures", "dm_only.secret", "dm_only.villain_answer", "dm_only.dm_pitch", "dm_only.clues[].kind", "dm_only.clues[].how"]}
"institution": {"fragment": "design/_staging/P1/signature_<slug of the name you pick>.json", "candidates": ["House Ghulgash", "House Krugurk", "House Thokmog", "House Grakog"], "registry": {"id": "", "type": "signature", "name": "", "aliases": [], "summary": "", "file": "design/premise.md", "secrecy": "public", "created_phase": "P1", "origin": "birth", "lang": "other_side", "kind": "institution", "slot": "institution", "home": "contest_two_empires.third", "rolled": {"form": "form_house", "practice": "practice_couriers", "sign": "isign_initiation_scar", "power": "power_place"}, "rule": "", "appears": [{"phase": "P3", "hook": "the institution sits in a central settlement", "text": ""}, {"phase": "P4", "hook": "the institution's assets follow its power source", "text": ""}, {"phase": "P4", "hook": "the role's faction is the institution: its power sets its assets, its practice its services", "text": ""}, {"phase": "P5", "hook": "its leader and members show its sign", "text": ""}, {"phase": "P5", "hook": "its members show the sign", "text": ""}, {"phase": "P6", "hook": "a site it holds or guards", "text": ""}, {"phase": "P7", "hook": "the institution offers or colours quests; it never originates the main thread", "text": ""}, {"phase": "P8", "hook": "what natives know of it", "text": ""}], "stamped": {"kind": "institution", "slot": "institution"}, "refs": []}, "fill": ["id", "name", "aliases", "summary", "rule", "refs", "appears[].text"]}
"break_lineage_homes_inverted": {"fragment": "design/_staging/P1/break_lineage_homes_inverted.json", "registry": {"id": "break_lineage_homes_inverted", "type": "break", "name": "The lineages' homes are inverted", "aliases": [], "summary": "", "file": "design/premise.md", "secrecy": "public", "created_phase": "P1", "origin": "birth", "lang": "other_side", "row": "break_lineage_homes_inverted", "tie": "tie_ruin_source", "stamped": {"row": "break_lineage_homes_inverted"}, "refs": []}, "fill": ["aliases", "summary", "refs"]}
```

**Three faults found on the way, fixed at their cause:**
- **`stamped` as a list crashed the merge.** `registry.stamps_of` assumed an object, so a `stamped` list stopped `registry.py merge` with a traceback before the row check's refusal. A malformed row now has no stamps and is refused by name.
- **The door asked the wrong table for `secret_class`.** `Door.premise_errors` looked the twist up in `secrets.yaml#archetype`, which lacks `twist_greater_power`. A birth that rolled that twist would have had its correct class (`cosmology`, as the prompt says) refused with "`threat` when no twist was rolled". The door now reads `secrets.yaml#twist`, as the prompt and the frame do.
- **An empty `lang`.** The first frame left the premise's and the breaks' `lang` empty when no common tongue was rolled (the language reading above).

**The prompts.**
- `P1.premise.md` section 3 points at `{{frame_path}}` (a new placeholder; `design_prompts.PLACEHOLDERS`), says to copy each row and fill only `fill`, and lists the writer's fields per row type.
- `_common.md` says `stamped` is an object `{field: value}`, never a list, and to copy a frame's shape where one exists.
- The door's other checks were moved, not changed: `home_id_of`, `rolled_of_identity` and `hooks_by_floor_of` are module functions, so the frame builds on them; the `Door` methods call them.

**The addendum (5-8):**
- **5, the writer's own check.** `registry.py -c CAMP check --phase PN [--id ID]` judges the staged fragments by the merge's own code (the registry's rules, the door, the frame), prints `✗` lines and writes nothing: no report, no door log, no move. `--id` keeps one fragment and its `members`. The P1 prompt says to run it before returning and after every fix, with the exact command; `_common.md` says the same for every writer; `design-fanout.js`'s fix writer is told to run the check its prompt gives.
- **6, a known villain's public face.** The prompt says that when the visibility makes the villain known (known and untouchable, or known but no one knows where: the rows' labels, never their ids, since the rendered prompt is readable by the conductor and the first full run's `test_p1_writer` caught the ids), the public premise shows what the world knows it as, never its hidden part. `rubric_p1_legible`'s question and `fails_when` now ask for it (rubrics carry no reviewed stamp).
- **7, the lifeline sets no side.** The prompt's question bullet: the sides' stances and means come from the contest, the prize and the goal; the lifeline colours the world and never decides a side's stance or its means.
- **8, the cost of a fully refused run.** `phase PN merge --run-dir` recorded each run as `merged: true` before `registry.py merge` ran. It now records after the merge, with `units: {merged, refused}`; a run whose every unit was refused is `merged: false`, and a crashed merge records the run as not merged. `design_cost.record` takes `units` and prints them.

**Tests.**
- New `tests/test_p1_frame.py` (13 tests): the frame at each scale (every rolled field, an object `stamped`, the candidates, the notes per hook, the pin, the clues; the frame on disk equals the one the door rebuilds; the prompt names its path); a fill-only writer merges; `stamped` as a list, a break without its name, changed rolled fields (kind, notes, clue levels, the pin's event, tensions, a stamp unequal to its field), a renamed signature id, and refusals that never print a frame value; the addendum's check (judges, writes nothing, `--id`), the prompts and the rubric, and a fully refused run's cost row; the twist's class.
- New `tests/_p1_frame.py`: the stand-in writer that fills a frame's `fill` fields.
- The dry walk's stand-in writer (`test_p1_dry_walk.Walker.write`) and `test_door.NewBirth.units` now build from the frame. The dry walk keeps the frame when it clears staging.
- Prompt needles updated in `test_p1_writer.py`, `test_p1_card.py`, `test_p1_story.py`.

**Changed files:** `scripts/design_frame.py` (new), `design_door.py`, `design_io.py`, `design_prompts.py`, `designer.py`, `registry.py`, `design_cost.py`; `prompts/design/P1.premise.md`, `_common.md`; `data/design/rubrics.yaml`; `.claude/workflows/design-fanout.js`; tests: `_p1_frame.py`, `test_p1_frame.py` (new), `test_door.py`, `test_p1_dry_walk.py`, `test_p1_writer.py`, `test_p1_card.py`, `test_p1_story.py`.

**For your notice:** every test process's `tests/_campaign.py` makes an `aigm-used-*` folder in the temporary directory and never removes it (several hundred are there now). This predates 19c; the fix is an `atexit` removal like the runtime folder's, which I left out of this item.

**The suite:** 886 tests, OK, exit code 0, 1,860 s (31.0 min). Two earlier runs were stopped (a script edit mid-run) or failed on my own wording (the visibility ids in the prompt, and a test that pinned the legibility rubric's old sentence); both were fixed before this run. `.runtime` was empty after, and no `aigm-runtime-*` folder was left.

## 20b — the P0 card without dice (the fifth coding tab)

**The card** (`designer.p0_card`, written once at `new`). It shows the dials in words: each value is printed as its row's label in `dials.yaml` (`designer.dial_word`), and the tone is printed as **Darkness**. Then the content mix, the party and its band, the wishes and the seed, and the arc's chapters by level range. It has no roll section, no die notation, no row id, and no "act" (the arc's acts are P7's to reshape: finding D5). The blank dials' rolls stay in the public dice log, and `new` still prints its `roll:` lines for the conductor. A legacy card is not rebuilt: nothing but `new` writes `P0.card.md`, and a test plants an old card and finds it unchanged after `preroll`, `phase P1 begin` and `status`. The leak scan and the approval are unchanged.

**One fresh P0 card** (`designer.py new _test-card-demo --scale epic --party-size 1 --seed CARD-DEMO`, the other dials rolled; a throwaway campaign, deleted after):

```markdown
# Phase 0 — the dials (_test-card-demo)

- **Scale:** Epic: 10 chapters, levels 1-20
- **Darkness:** Shadowed
- **Magic:** Low
- **Era:** Nautical
- **Danger:** Lethal
- **Content mix:** War, Mystery, Exploration
- **Party:** 1 character, starting at level 1; the band runs from level 1 to 20
- **Wishes:** must: none; must not: none
- **Seed:** `CARD-DEMO`

## The chapters
- Chapter 1: levels 1-3
- Chapter 2: levels 3-5
- Chapter 3: levels 5-7
- Chapter 4: levels 7-9
- Chapter 5: levels 9-11
- Chapter 6: levels 11-12
- Chapter 7: levels 12-14
- Chapter 8: levels 14-16
- Chapter 9: levels 16-18
- Chapter 10: levels 18-20
```

**The used.json folders** (your addition). `tests/_campaign.py` registers `atexit` removal of its `aigm-used-*` folder, as for the runtime folder: one per test process, isolation kept. Cleaned once by the exact prefix: **379 folders** removed before this run.

Two more were left during my gating run, at 17:04 and 17:25. They came from another suite on the 20a commit, which has no cleanup (your audit committed `129531e` at the same time). Two checks support that: my own short run of `test_live_guard.py`, which starts two child test processes, left the count unchanged; and the new test below passes. I removed those two by name as well; none remain.

**Tests:**
- `test_designer.NewBirth.test_the_p0_card_shows_the_dials_in_words_and_no_dice`: no die notation, no arrow, no "act", no `dial.` label and no `dials.yaml` row id; every dial in words, the party, the seed, the wishes, one line per chapter; the rolls still in the dice log.
- `test_a_legacy_p0_card_is_not_rebuilt`.
- `test_live_guard.SuiteRuntime.test_a_test_process_leaves_no_used_folder`: a fresh process that imports `_campaign` leaves neither its used folder nor its runtime folder.

**Changed files:** `scripts/designer.py`; `tests/_campaign.py`, `tests/test_designer.py`, `tests/test_live_guard.py`.

**The suite:** 889 tests, OK, exit code 0, 1,919 s (32.0 min).

## 21b — the guard reads command words, not text (the fifth coding tab)

**The splitter** (`hooks/design_read_guard._command_segments`, used by `_shell_roots`, 19d's search rule). A Bash or PowerShell line is split into its commands, aware of quotes, heredocs and comments:
- it splits on `;`, `&`, `|` and newlines outside quotes, so a quoted `a; grep -r …` stays one argument;
- a heredoc's body (`<<EOF`, `<<'EOF'`, `<<-EOF` … to its delimiter line, several per line in order), a PowerShell here-string (`@'`/`@"` … `'@`/`"@`), a `#` comment that opens a word, a PowerShell block comment (`<# … #>`) and a quoted string's body are text;
- the escapes are the backslash in Bash and the backtick in PowerShell, and PowerShell's doubled quote is honoured;
- a command substitution is still a command, quoted or not: `$( … )` and, in Bash, a backtick pair are returned as segments of their own.

**What stays as it was:** the dm-only path scan, the registry and secret-dice verbs, and the runtime-override rule still read the whole text, heredoc bodies included (a script fed through a heredoc can open dm-only or set the variable).

**Tests** (`test_design_read_guard.py`, `test_the_guard_reads_command_words_not_text`):
- These pass: seven text cases, namely a heredoc whose body holds `find`, `grep -r` and `ls -R` over a parent of dm-only (quoted delimiter, and `<<-` with tabs), a quoted `a; grep -r …` piped to `head`, a single-quoted `find …` with a comment holding `ls -R`, a commit message naming `grep -r`, and in PowerShell a here-string holding `Get-ChildItem -Recurse` and a quoted `gci -Recurse` with a `# dir /s` comment.
- These are still refused: five commands, namely a real `grep -rn` after a heredoc, `$(grep -r …)` inside double quotes, a backtick `find`, `ls -R` after `&&` with a comment after it, and PowerShell's `Get-ChildItem -Recurse` after a `;`.
- A dm-only path inside a heredoc's body is still refused.
- An unquoted path in the Bash cases is written with forward slashes, as Bash needs it (an unquoted Windows backslash path is mangled by Bash itself).

**Changed files:** `scripts/hooks/design_read_guard.py`, `tests/test_design_read_guard.py`.

**The suite:** 893 tests, OK, exit code 0, 1,798 s (30.0 min), run over 21b with 21a part 1 beside it (both uncommitted; 21b's commit takes its two files only). No `aigm-*` folder left.

## 21a — a short question and named sides (the fifth coding tab)

**Part 1, the short question.**
- The door: `design_door.question_sentences` splits the premise's `question` at its question marks and counts each sentence's words. `Door.premise_errors` refuses a sentence past `QUESTION_WORDS = 45`, naming the contest by its id (the identity's questions in order) and the count: `` `question` holds a question of N words for contest_x; one sentence per contest, at most about thirty-five words (refused past 45): say the costs in the sides' lines and the stakes ``. A refusal reaches the retry prompt through `last_error`, as before.
- The prompt: the question bullet asks for one sentence per contest of at most about thirty-five words, with the costs said elsewhere; the pitch is "three short sentences".
- The rubric: `rubric_p1_question_concrete`'s `fails_when` adds a question that cannot be read in one breath.

**Part 2, named sides** (the owner-approved rows of the amendment, exactly as listed).
- **The tables** (`foundation.yaml`):
  - every one of the 30 spine rows carries `text.ends_short: [end_a, end_b]`;
  - the 17 generic roles carry `generic: true` and their `noun` (divided_city, merchant_house_divides, foreign_envoy, war_fed_company, fallen_state_remnant, shapeshifter, relic_pieces and two_empires on a and b; fiend_pact on b);
  - divided_city's halves also carry `toward: end_a` / `end_b` and stay seated in the heart.
  - `reviewed.json` is restamped by `design_tables.py stamp`. Exactly those 39 rows changed (9 contests, 30 spines), and the file keeps its CRLF working copy. Undo it if the stamp must wait for your audit.
- **The code** (`design_foundation`):
  - `seat_short` gives a seated part's short name: an end's `ends_short`, the heart's or key place's short name, and none for an along node.
  - `side_phrase` names a generic side "<noun> of <seat>", a facing half "<noun> toward <end>", and every other side, or a seat with no short name, by its label.
  - It is used wherever the story sentence names a side: the two sides, the prize ("the land of …", "the seat of …"), a side that is the move's hand, and a side that is its target.
  - `rendering`'s owner lines keep the row texts.

**Over the corpus** (3,000 births): 678 story sentences carry a generic side (shapeshifter 75, foreign_envoy 70, relic_pieces 81, divided_city 86, war_fed_company 70, fiend_pact 70, merchant_house_divides 76, fallen_state_remnant 66, two_empires 84). Some of them:
- Sea raiders enslaved the household of the fjords; now the household of the fjords and the household of the warm bays fight over an inheritance.
- The risen dead are about to corrupt the bridge-city on the middle course; now the half of the city toward the source and the half of the city toward the delta fight over the bridge-city on the middle course.
- Slavers opened the way down to the floor; now the country of the rift floor and the country of the rims fight over the land between them.
- A generation ago, the fiend's envoy plundered the prison-temple; now the house that signed and the rival house of the deep sea fight over the seat of the house that signed.
- Someone sealed the road down from the edge; now the new power of the inner lands and the new power of the cloud sea fight over the city at the cliff's edge.

**For your reading:** fiend_pact's side a ("the house that signed") is not generic, so its two sides read unevenly ("the house that signed and the rival house of the deep sea"), as the list asks.

**Tests.**
- New `tests/test_p1_polish.py` (5 tests): the sentence counter; a question past the limit refused with its count and contest, the short one merging; the prompt and the rubric; the tables carry exactly the approved rows (the generic set, the nouns, the halves' `toward`, 30 spines each with two distinct `ends_short`); and the added test, over the corpus, that every generic side reads through its noun and a seat, the two sides never read the same, and no placeholder label stands in a story sentence.
- Tests that rebuilt the old sentence now build it with `side_phrase`: `test_p1_story` (`subject_of`, `test_the_sentence_reads_as_d_and_d`) and `test_p1_birth2_faults`.
- `test_written_in_english` allows `ends_short` among the spine's text keys.

**Changed files:** `data/design/foundation.yaml`, `reviewed.json`, `rubrics.yaml`; `prompts/design/P1.premise.md`; `scripts/design_door.py`, `design_foundation.py`; tests: `test_p1_polish.py` (new), `test_p1_story.py`, `test_p1_birth2_faults.py`, `test_written_in_english.py`.

**The suite:** 895 tests, OK, exit code 0, 2,664 s (44.4 min). An earlier run failed six tests that pinned the old sentence and the old stamps; those are updated above. No `aigm-*` folder left.

## 21c — the guard reads inside a wrapper (the fifth coding tab)

**The unwrapping** (`hooks/design_read_guard.py`, before 19d's search rule judges a command):
- **`_unwrap`** skips `VAR=value` assignments and the prefixes `env` (with its own `VAR=value` arguments), `sudo`, `doas`, `time`, `nohup`, `command`, `exec`, `nice`, `ionice`, `stdbuf`, `timeout` (and its duration), `xargs` and PowerShell's `.`, each with its options and the arguments its options take (`_PREFIXES`). It also takes off a grouping's `(`, `((`, `{` and their closers, including a `(` or `)` stuck to a word.
- **`_command_string`** reads the string a wrapper runs and parses it again as commands, recursively (eight levels at most): `bash`/`sh`/`zsh`/`dash`/`ksh -c` (also in a cluster such as `-lc`), `eval`, `powershell`/`pwsh -Command` (any abbreviation down to `-c`), `Invoke-Expression`/`iex`, and `cmd /c` / `/k`. A PowerShell `-EncodedCommand` (`-e`, `-ec`, `-enc` …) comes back as unreadable and is refused while a marker is armed ("… which cannot be read").
- PowerShell's `&` call operator was already split off by 21b's splitter, so `& { … }` reads as a grouping.
- **Process substitution:** `<( … )` and `>( … )` are commands like `$( … )` (`_command_segments`).

**Scope (my reading):** the encoded command is refused within the search rule's scope, which is the conductor in birth and detail, an ad-hoc agent and the playtest player. A designer agent and the DM at the table stay free, as for every other search; the test pins that. If "outright" means every caller (like the runtime-override rule), it is a one-line move.

**Tests** (`test_design_read_guard.py`, `test_the_guard_reads_inside_a_wrapper`):
- **Refused:** 29 commands over a parent folder of dm-only, each wrapped one way. They cover:
  - every command string (`bash -c`, `sh -c` after a `cd`, `zsh -c`, `bash -lc`, `eval`, `powershell -NoProfile -Command`, `pwsh -c`, `Invoke-Expression`, `iex`, `cmd /c dir /s`);
  - every prefix (`env FOO=1`, `env -u HOME FOO=1`, `sudo -u me`, `time`, `nohup … &`, `command`, `exec`, `nice -n 5`, `timeout 5`, `xargs -n 1` after a pipe), plus a prefix inside a command string (`bash -c "sudo find …"`);
  - every grouping (`( … )`, `(grep …)`, `{ …; }`, `<( … )`, `>( … )`, PowerShell's `& { … }` and `. { … }`);
  - `powershell -EncodedCommand`.
- **Passed:** the same words as text inside a command string's own quotes (`bash -c 'echo "grep -r …"'`, `powershell -Command "Write-Output 'gci -Recurse …'"`), a harmless `bash -c`, a non-recursive `sudo ls` and `pwsh -c "Get-ChildItem …"`, `env FOO=1 py designer.py …`, and a grouping that lists below the protected folders. The encoded refusal says "cannot be read"; a designer agent's encoded command passes.
- 21b's text cases still pass.

**On the way:** PowerShell's `.` prefix was missed at first (`Path(".").name` is empty); `_unwrap` now reads it as a word.

**Changed files:** `scripts/hooks/design_read_guard.py`, `tests/test_design_read_guard.py`.

**The suite:** 896 tests, OK, exit code 0, 1,998 s (33.3 min). No `aigm-*` folder left.
