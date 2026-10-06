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

**18c-1 audited from the working tree** (789 tests, exit 0 by the coding tab; every threat roll secret; the variety report: 15-18 families per scale, shares 4.2-8.4 %, no consecutive repeat, 922-970 distinct (family, creature, shape, goal) sets of 1,000; the join prize 30-34 %, role goal 11-14 %, move 55-56 %). **Accepted with corrections:** the law of nature also fits the fey; lair forms for the four families the rows left without (each family's pool at five or more); a dragon's colour weighs its lair (×3, a weight, not a filter, so no pool falls under the floor).

**A leak found and closed tonight, weighed:** a world state joined to the secret threat ("dragons rule" with a dragon villain and no dragon contest) told the player what the villain is. Options: accept it; keep the join in dm-only (the public world state still betrays it); require every join to be public. Chosen: a world state joins only a public piece; the villain counts only when its visibility is known, a hand only through the public hand; otherwise the world state needs its public join or is not drawn. The dm-only join record goes.

**For the owner (a fact, not a fault):** about half the villains at standard and three fifths at epic are reskins of an SRD base (the SRD has few creatures above CR 17 outside the dragons); P5 does their stat work with the reskin rule.

**Committed as `35d1080` (the coding tab's suite: 790 tests, exit 0); the clean run on it: 790 tests, OK, exit code 0, five skipped (read from the log). Accepted.** With every world state's join public, 584 of 3,000 births hold one (900 before); dragons rule and the gods among mortals nearly vanished (9 and 17), which 18c-2 answers below.

## 18c-2 — the move (in progress)

**The coding tab stopped on three crossed thresholds; decided tonight, weighed:**
- *The move's targets were skewed* (role 47 %, heart 37 %, remnant 5 %, thin place 0.3 %). The cause: a move that joins the contest could strike only the prize's piece or a role, and the prize is mostly the heart. Options: add guard relations to the goal → target relation; weigh the goals; widen what joins. Chosen: both the guard relations and the cause: the move also joins when it strikes a piece standing on a side's part of the layout (striking a side's holding draws that side in), and the target is drawn among every joinable piece, weighted by the goal's relation.
- *`act_summoned` was never reached* (its only target was the rare thin place): it also strikes the heart and the key place.
- *Dragons rule and the gods among mortals stayed rare* (20 and 29) after their public joins widened (a dragon hand, a dragons' ruin, the gods' ruins): they weigh ×3; drawn only where a public join holds, the weight is prominence, not a leak.
Thresholds before the commit: every target but the thin place at 5 % or more (the thin place 3 %, the remnant 10 %), every verb reached, the two world states at 40 or more.
- *The thin place stayed at 0.9 % after the three answers* (the verb was drawn before the target, and only five verbs strike a thin place). Options: weigh the thin-place verbs ×3; draw the target before the verb; accept about 1 %. Chosen: hand → target → verb (the goal decides what is struck, the verb is how the hand strikes it; the cause fixed, not compensated); `docs/p1-build-18.md`'s order amended; the thin place's threshold relaxed to 2 % (it is in about 15 % of palettes). After the first three answers every verb and every hand was reached and the two rare world states stood at 45 and 88.
- *With the target first, the thin place reached 1.2 % and the heart fell to 14.7 %, leaving plague (9) and poison (13) rare, both striking the heart alone.* Chosen: the thin place weighs ×3 where it stands (measured: 3.1 %), as prominence; poison and plague also strike a role (a side's lord poisoned, a side's people struck by plague): their fit list was too narrow, the order was right.

**18c-2 audited from the working tree** (800 tests, exit 0 by the coding tab). Over 3,000 seeds: targets role 36.7 %, key place 29.6, remnant 16.6, heart 14.6, thin place 2.5 (3.1 at start level 1); every verb reached (19-407, the widened poison and plague above 40); all 27 hands (26-154); joins prize 33.8 %, side holding 27.3, move on a role 20.5, role goal 12.5, prize piece 5.8; the start never the heart; world states: magic nobility 125, lottery 120, guilds 110, the gods among mortals 83, the enemy won 76, dragons rule 54, the moon 54, the beast-lord 47. A fault the coding tab found and fixed: the public hand inherited `antagonists.yaml`'s file hooks into the public ledger. **Accepted with one correction:** carrying off destroys nothing (the side remains, with a cause); driving out destroys the heart, not the side (it lives on in exile).

**Committed as `e512a4b`; the clean run on it: 800 tests, OK, exit code 0, five skipped (read from the log). Accepted.** A brittle test noted for 18d: a lineage share asserted on about 20 births.

## 18d — the secret as the threat's hidden half (in progress)
