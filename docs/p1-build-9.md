# Build item 9 — the secret and the villain tables

*Written by the development (design and review) tab for the coding tab, 2026-10-03. The design is plan item 25 (step 2, #6 and #7), errata 24.2 #22, `docs/p1-foundation-rows.md` sections 14, 15 and 18, and the notes `docs/p1-tags.md` gathered. This file holds the structure, the standard and the rules; it holds no row. Where the sources differ, stop and report.*

**Who sees what.** The owner is also the player. He never sees a row of these tables: not in a summary, not in a commit message, not in a test's output. The coding tab writes the rows, the development tab reads every row and audits it, the owner sees counts. The one exception is the burn sample at the end of this file.

**One green commit:** `Plan item 25, build 9: the secret and villain tables`. The full suite green (the exit code), no commit before the audit, no push.

**Limits.**
- Data and static tests, plus the many-seeds test on today's preroll. Moving the villain's rolls from P4 to P1, the chooser's and the pole's rolls, and the chooser and tie equivalence at roll time are item 10.
- P4's own tables (`front_template`, `doom_shape`, `lieutenant_role`, `buy_time_lever`, `escalation_stage`, `bbeg_faction_archetype`) are not redesigned here; only their references to rows this item removes or renames are kept true. They hold attractor rows (the count, the silence, the trial, the lamp, the dead rise); that is P4's turn, listed in your summary by count only.
- Legacy births keep loading; `test_regression_births` stays green; a `used.json` that names a removed row (hashed) must not break anything.
- Run nothing that calls a model.

---

## 1. The standard (owner-approved 2026-10-03)

Every archetype, twist and trail row, and every villain shape, origin and tie, is written and later audited against these seven:

| Criterion | Meaning |
|---|---|
| the legend test | big enough to carry the scale's whole level band |
| a living choice | a person's decision stands behind it; never "an ancient evil wakes" |
| tied to the break | the secret tells the break's true cause; it opens no second story beside it |
| playable | it can be opened step by step through clues; it is not one reveal scene |
| outside the attractor | no dead and their rights, no ledgers, registers, debts or tolls, no courts or trials, no light and fuel, no hush or bells, no tides, no salt: in the row's sentence, its clue shapes and its hooks |
| a deep villain | the villain has a defensible reason and carries one pole of the question to its extreme |
| a villain who can kill | a real threat; nothing in the row protects the party |

## 2. The secret (`secrets.yaml`, every roll secret)

**Home: the break.** The secret is the break's true cause: why it happened and who chose it. Four pieces.

### Archetype

- Today 24 rows. Every row is re-read against the standard: a row inside the attractor leaves or is rewritten (its sentence and its three clue shapes); a row that cannot be told as the cause of a break leaves. Rows may be added to the same standard. **No fewer than 22 rows** afterwards (the table is not drawn again across campaigns).
- Every row gains one line saying how it is the break's true cause (a field of its own), written so that it holds for any target and action the foundation can roll.
- **A row that makes a secret of something the foundation or a trope break already shows in public is excluded by conflict.** Build the conflict lists (`conflicts_with` on the secret row; the arbiter makes them symmetric and keeps the public record clean, build 7a). At least these public rows must be checked against every archetype: `spine_titan_back`, `spine_two_worlds`, `ruin_imprisoned_god`, `ruin_dead_god`, `ruin_departed_god`, `ruin_made_peoples`, `ruin_failed_experiment`, `ruin_broken_time`, `ruin_planar_rift`, `act_true_face`, `break_gods_are_ancestors_known` (in the data today), `break_gods_among_mortals`, `break_the_enemy_won`, `break_dragons_rule`, `break_rule_by_lottery`, `break_no_direct_lies`, `break_no_writing`, the phenomenon rules that state openly what a secret would hide (`rule_true_names` and the like), and the dial claims.
- The field `villain_relation` goes: the villain's tie to the break (below) replaces it. Its P4 hook goes with it.
- `hides_in` stays (the card's spoiler-safe class reads it, `design_approval.py`).
- The tone no longer biases the archetype (build 7b removed `secret_archetype_bias`). A weight by the break's action and time may be written where a row clearly fits one.
- The common P2 hook becomes: "the secret is pinned to the break's dated event and to one god". "Deep-past" goes.

### Chooser (new, six rows; the list is public, the roll is secret)

Who chose the break; always a person: the villain; a contest role; the signature institution; the signature people; an ordinary person now dead or forgotten; a mortal who bargained with a power. No row may make the chooser a thing, a god acting alone or an accident.

### Twist

- Today 12 rows; three join: the chooser did not know what they were doing; the chooser is now trying to undo it; the people know the secret and nobody believes it.
- A twist the foundation now makes true in every campaign (the secret is always recent) is replaced by one that still changes something. 15 rows afterwards.

### Trail

- Today 6 rows; the attractor row leaves; the table grows to about 10 (the approved examples of the kind: a trace, a wound and a survivor; an object, its maker and its owner; a hunting trail and a lair; a captured letter and a traitor).
- A trail that needs writing (a letter, a document) conflicts with `break_no_writing`.
- The three stages keep today's keys (`act1`, `act2`, `act3`); how they map to a one-act campaign is item 12's.

## 3. The villain (`antagonists.yaml`; rolled secretly in P1 from item 10 on)

**Home: the break and the question.**

| Piece | Rows | Rule |
|---|---|---|
| visibility | 5 today | re-read against the standard |
| shape | 12 usable today, 3 forbidden | the forbidden three (the dark lord, the whispering advisor, the secretly evil ruler) never enter a pool and stay only so that `forbidden.yaml` can name them; a few rows join to the standard; no fewer than 14 usable |
| origin | 9 usable today, 1 forbidden | the awakened ancient evil never enters a pool; "the phenomenon took them" is tied to the phenomenon signature |
| tie to the break (new, six rows; the list is public, the roll is secret) | caused it · exploits it · wants to complete it · wants to reverse it at a terrible price · tried to stop it, failed and is now enraged · is the break's product, born with it | |
| pole | no table | the script picks side a's or side b's pole (item 10); the darkness dial's `majority_pole` says where the majority stands |

**Conflict lists to build** (the development tab audits them; the owner sees their count):
- tie against the break's time: a tie that needs the break to have happened (its product; tried to stop it and failed; wants to reverse it) cannot stand with `time_coming`;
- tie against the chooser: the chooser is the villain exactly when the tie is "caused it" (the equivalence is enforced at roll time in item 10; write it as data here);
- shape against visibility, shape against origin, origin against tie: wherever two rows cannot describe one villain;
- any villain row against the public rows it would contradict (the list of section 2 is the place to start).

`bbeg_faction_archetype`'s `allowed_via` names secret rows: keep it true to the archetypes that remain.

## 4. Mechanism notes

- A secret row may carry claims; its tokens are secret (build 7c-1). If a topic is needed that only the secret layer uses, keep it in a registry of its own that no summary prints; prefer direct `conflicts_with` lists.
- The stamp covers the secret and villain sub-tables of this item.
- The floor: the archetype's smallest pool after the constraints, over many seeds, is not under five.

## 5. Tests

- Counts: archetypes ≥ 22, twists 15, trails 9 to 11, choosers 6, ties 6, visibilities 5, usable shapes ≥ 14, usable origins 9.
- No forbidden row can be drawn.
- The attractor's words appear in no row of these sub-tables (a word list in the test; say in your summary how many words it holds, not which rows it caught).
- Every id a conflict, a weight or `allowed_via` names exists; every conflict is symmetric after load.
- Many seeds over every scale, magic and era, with today's P1 and P4 preroll: no conflicting set, no empty pool, the floor holds, and the public dice log names no secret row (the die's size included).

## 6. The burn sample (for the owner's eyes)

So that the owner can judge the quality without being spoiled, write, to exactly the standard of the tables, **three archetype rows and three villain shape rows that are not in the tables and never will be**. Put them in `docs/reports/item9-burn-sample.md`, in Turkish, each with its sentence, its line as the break's cause (archetypes) or its rule (shapes), and for the archetypes the three clue shapes. A test proves that none of the six ids or sentences exists in `secrets.yaml` or `antagonists.yaml`. The owner reads this file; that is why these six are spent.

## 7. The summary (what the owner carries)

Counts only. Per sub-table: rows before, rows removed, rows rewritten, rows added, rows after. The number of conflict pairs per kind (secret against public, villain against public, inside the villain, tie against time). The smallest archetype pool. The stamp's changed rows as a number. The suite's count and exit code. Anything unexpected, described without naming or quoting a row. P4's attractor rows as a count.
