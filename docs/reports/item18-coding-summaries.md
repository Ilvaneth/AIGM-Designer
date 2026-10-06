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
