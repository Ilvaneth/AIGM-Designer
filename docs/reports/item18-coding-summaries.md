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
