# Build item 20 — what the third P1-only test birth showed

*Written by the development (design and review) tab for the coding tab, 2026-10-07, after `_test-p1-3` (P0 and P1 at the epic scale; its story reads as an epic D&D campaign: an ancient green dragon, the untouchable warden of the low villages, secretly behind a cursed pack that eats the largest floating island, and spared the island a worse order). One fault cost a whole Workflow round; one card still breaks the owner's card rule. Where this file and earlier specifications differ, this file holds.*

**Two green commits, in this order.** After each: the full suite in the background with a long timeout, the exit code read, a summary appended to `docs/reports/item18-coding-summaries.md` under "20a" / "20b", a message to the design tab; no commit before its answer; never push.

| Part | What | Commit message |
|---|---|---|
| 20a | the script frames P1's registry rows; the writer fills only the text | `Plan item 25, build 20a: the script frames P1's rows` |
| 20b | the P0 card follows the owner's card rule | `Plan item 25, build 20b: the P0 card without dice` |

## Part 20a — the script frames P1's registry rows

**The fault.** The first run's door refused all six units of the premise's fragment: `stamped must be an object` on all six, `name missing` on three (the premise row and the two break rows). The writer had written `stamped` as a list, as the premise file's front matter writes it, while the registry row needs an object; the prompt says "stamp question, signatures, trope_breaks" without the shape, and for a break row lists only `row` and `tie`. The second birth's writer guessed right, the third's guessed wrong: the cause is the prompt, not the model. The cost: a full round (9 agents, 125,362 output tokens, about 23 minutes) thrown away.

**The fix at its cause.** Everything in these rows that is not prose is already decided by the rolls; by the rule "the writer writes, it does not decide", the script writes it:

1. At `phase P1 begin` the script writes the **frame** of every P1 registry row the writer owes: the premise row, one signature row per slot, one break row per rolled trope break; each with its id, type, secrecy, file, `stamped` as the object the registry expects, and every field the rolls set (a signature's `slot`, `home`, `rolled`; a break's `row`, `tie` and `name` (the trope break's label); the premise's `tensions`, `signatures`, `trope_breaks`, `secret_class`, and under `dm_only` the twist id, the `pinned` record as rolled, each stage's `levels` and chain `piece`). The frame goes where the prompt points the writer (a frame file beside the fragment path in staging); the text fields stand empty, named.
2. The prompt shows the frame's path and lists, per row type, the fields the writer fills (the premise's question, pitch and prose fields; a signature's `name` from its candidates, `rule`, `appears` notes; the clues' `kind` and `how`) and says the other fields are copied unchanged.
3. The door compares each row's frame fields with the script's frame: a changed or missing frame field is refused with the field's name (as the seal refuses a changed record); the text fields are judged as today.
4. The common preamble's general rule for registry rows (any phase) states `stamped` is an object; the other phases' frames wait for their floors.

**Tests of 20a:** the frame of a birth at each scale holds every row with its rolled fields and an object `stamped`; a stand-in writer that fills only the text fields merges; a fragment with `stamped` as a list, a break row without its `name`, or a changed rolled field is refused with the field named; the dry walk uses the frame.

## Part 20b — the P0 card follows the owner's card rule

The P0 card still prints the dice (`dial.tone d3 → 2 = tone_shadowed`) and row ids, which the owner ruled off the cards (build 14b: "no dice on the card"; the public dice log holds them). The P0 card shows the dials as words (scale, darkness, magic, era, danger, the content mix, the party and its band, the wishes), the arc skeleton as chapters by level range without the word "act" (the arc's acts are P7's to reshape: finding D5), and the seed; no roll, no die, no row id. The leak scan and the approval stay as they are; a legacy P0 card is not rebuilt.

**Tests of 20b:** the P0 card of a fresh birth holds no die notation and no row id, and names every dial in words; a legacy card is unchanged.

## The summary (each part)

Changed files; the suite's count, exit code and time; for 20a a frame printed for one birth and a list of the fields the writer fills per row type; for 20b one fresh P0 card.

## Added from the birth's report (2026-10-07; part of 20a)

`docs/reports/p1-test-birth-3.md` section 6 adds four faults:

5. **A shape fault survives the whole chain.** The critics judge the prose, so a fragment the door will refuse passes two critics and a fix writer before the merge finds it (a fix writer even rewrote the fragment's shape). Beside the frame: the writer and every fix writer run the door's row check on their fragment before they return (a `registry.py` or `designer.py` command that checks a staged fragment against the registry's rules and the frame, printing the faults), and fix what it prints; the Workflow's prompts say so.
6. **A known villain has a public face.** The villain's visibility was "known and untouchable" (the low villages' warden), yet the public premise never named it; three critics noted it and none asked a fix. When the visibility makes the villain known (known and untouchable, known but nowhere to be found), the public premise shows its public face (what the world knows it as), never its hidden part; the prompt says so and `rubric_p1_legible` checks it.
7. **The lifeline sets no side's stance.** The value ("hired guards") was written into the sides' stances and means, and the question pulled against itself (two fix rounds on `rubric_p1_question_concrete`). The prompt says: the sides' stances and the question's stakes come from the contest, the prize and the goal; the lifeline may colour the world they stand in, never decide a side's stance or its means.
8. **A fully refused run is not "merged".** The cost ledger's row for a run whose every unit the door refused says `merged: true`; it records the units merged and refused instead.
