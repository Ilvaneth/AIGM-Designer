# Build item 18 — the night of 2026-10-05/06

*The design and review tab's log of the parts built and audited while the owner slept (his approval, 2026-10-05: the two tabs work through 18f together, test, audit and commit; nothing is pushed until he has looked). The coding tab's own summaries are in `docs/reports/item18-coding-summaries.md`.*

**Protocol:** the coding tab builds a part and runs the full suite; the design tab reads the diff and runs the full suite in a clean checkout (`.runtime/wt-audit`) of the commit; a part is accepted only on a green suite read from its log. Messages between the tabs go through the session messaging (verified: the coding tab answered "received").

**Before going to sleep the owner was told:** the keep-awake setting could not be checked from this session (no settings tool); he checks it himself.

## 18a — the layers; texture fills no story slot (`c0dfc40`)

Audited 2026-10-05 (see `docs/p1-tags.md` section 8 for the note): the 23 prizes, the two retired contests, no lifeline left in any contest, target or action, the layers on every P0/P1 table, the two corrections (`prize_at` on four rows, `key_kinds` on six) checked by script. The coding tab's suite: 769 tests, exit 0. The clean run at `c0dfc40`: 769 tests, OK, exit code 0, five skipped (read from the log). **Accepted.** 18b was sent to the coding tab at the same time (it builds in the main tree; the audit runs in its own checkout).

## 18b — trope breaks bend; the palette follows the spine

Audited from the working tree and the coding tab's summary (777 tests, exit 0): the eight world states with `layer: story` and `joins`, never tied to the lifeline, never drawn without a join (3,000 seeds; 900 births hold one); the two bent rows; the P8 hook on fifteen rows; the palette's count by the spine's breadth (every value of every band seen; the crossroads never under its four ends; 1.6 % over the band where forced kinds pass it). **Accepted with corrections:** the public record omits a join to the threat; the enemy won also joins a fallen-kingdoms ruin; the P8 hook on three more rows (maps forbidden, dreams a place, the gods among mortals); the writing row states the caster's spellbook and scrolls by right of the art.

**A decision taken tonight (the order of 18b and 18c), weighed:** (a) the trope breaks first and a world state weighing the threat's rolls, as part 18b's text said; (b) the threat first, as G4's order says, and a world state drawn only where its join holds on the rolled threat. Chosen (b): story first and texture or world state hanging on it, as the layers say; no pending requirement; nothing about the villain can leak through a waiting join; world states a little rarer, which is accepted. The specification's sentence in part 18b is superseded by this note. Also decided: the moon's join to a hand needs a trading hand or things from beyond (a `moon` fit on the hand rows, 18c).

**Committed as `cc37145`; the clean run on it: 777 tests, OK, exit code 0, five skipped (read from the log). Accepted.**

## 18c-1 — the threat (in progress)

**Two questions answered tonight, weighed:**
- *The god family's weakness pool was four, under the floor of five for an `avoid_used` table.* Options: give the god more weaknesses; exempt its pool from the floor; drop `avoid_used` from the weakness. Chosen: more weaknesses by genuine fit (the approved four were a short list): a prophecy or riddle that names its end, a vow or bargain it must keep, a place it cannot leave (the imprisoned form); the pool becomes 7, and every other fit pool of 18c is checked against the floor. An exemption would be a patch; dropping `avoid_used` would cost variety.
- *The goal matched the main contest's prize in only 21 % of 300 births; forcing the move onto a contest role in the rest collapsed the move's targets.* Options: weigh the prize goals heavily; widen what counts as joining; force the move. Chosen: the threat joins the contest when the goal's piece is the prize, or the goal is a role goal (destroy, turn or avenge on a side), or the move strikes the prize's piece or a contest role; the prize goals weigh ×2; only when neither of the first two holds is the move's target drawn among the prize's piece and the roles. The join shares and the move targets' spread are measured before the commit.
