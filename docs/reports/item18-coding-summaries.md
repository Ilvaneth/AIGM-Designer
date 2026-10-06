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
