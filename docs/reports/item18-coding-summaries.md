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
