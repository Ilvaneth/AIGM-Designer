# Build item 12 — the promise ledger

*Written by the development (design and review) tab for the coding tab, 2026-10-04. The design is plan item 25 (the principle's third rule; "Common rules"), errata 24.2 #23, the notes of `docs/reports/tags-grouping-analysis-1.md` section 8, rule 9 and "A limit" of `docs/p1-tags.md`, and three owner rulings of 2026-10-04 (below). Where a source and this file differ, stop and report. The owner raises the coding tab's effort to extra for this item.*

**What it closes.** P1 promises the later floors a great deal and nothing carries it there. Counted on the tables as they stand: the P0 and P1 tables hold about 220 hooks aimed at a later phase (dials 31, scale 9, foundation 65, trope breaks 85, signatures 25, questions 5; counted by script on 2026-10-04), the diagnosis of item 25 put a birth's share at about 80, and no script reads one. An override is data that nobody applies. The gate forgives two validator codes by a hand-kept exception list (`EXPECTED_UNTIL`).

**The owner's rulings (2026-10-04).**
1. A promise a **script** checks closes the gate when it is due and not kept. A promise a **critic** judges "not kept" does not close the gate: it is shown on the card and the owner decides at the review stop (accept it, or rerun).
2. **Secret promises show as counts only** on the card ("gizli vaat: 5 açık, 2 tutuldu, 1 tutulmadı"). The development tab reads the detail; the owner never sees a secret promise's text.
3. **The secret's three clue stages are bound to the campaign's level band, not to acts:** the first in the first third of the band, the second in the middle third, the third on the escalation's top step. One rule for every scale; a one-act campaign keeps all three clues.

**Two green commits, in this order.** After each: the full suite green (the exit code), no commit before the audit, no push.

| Part | What | Commit message |
|---|---|---|
| 12a | the ledger: the record, its sources, the validator's first phases, the card's counts | `Plan item 25, build 12a: the promise ledger` |
| 12b | delivery and inspection: the prompts' block, a verdict per promise, the gate, the owner's waiver | `Plan item 25, build 12b: promises delivered and inspected` |

**Limits.**
- P0 and P1 only: the rows rolled in P0 and P1 are the ledger's sources now. The mechanism is general (any phase's preroll can add its rows' hooks), but the hooks of the P2-P8 tables are unreviewed (rule 9) and stay out until each floor's turn. Say in the summary where a later floor plugs in.
- An override is still not applied here: it becomes a promise due at the phase that owns the default (`claims.yaml#defaults.<id>.phase`). The one P2 already applies stays applied, and its promise is kept by script.
- The writer's prompt, the critics' rubrics and the new card are item 14: here the least change that carries the block and the verdicts; list what you adapted.
- Legacy births (no ledger in `design.json`) are left as they were built: no ledger is made for them, their gate and card behave as today, `test_regression_births` stays green.
- Run nothing that calls a model. No secret promise's text in a summary, a public file, a rendered public prompt or the card.

---

## Part 12a

### 1. The record

- **Public:** `design.json#promises`, a list. **Secret:** a dm-only file beside the secret identity record. A promise is secret when its source row is a secret roll, or when its text names one.
- **A promise:** a stable `id` (the same birth and seed give the same ids); `source` (one of the kinds of section 2); `from` (the row id, the entity id or the foundation piece); `from_phase`; `due` (a phase, or `validator`, or `play`); `text` (the hook's `must` sentence or the generated sentence, in English as the tables hold it); `tr` (the source row's Turkish name, for the card); `check` (`script:<rule id>` or `critic`); `status` (`open`, `kept`, `not_kept`, `waived`); the verdict's phase and attempt; for a waiver the owner's one sentence.
- A phase's rerun reopens the promises that phase judged; a P1 rerun with a reseed rebuilds the ledger.

### 2. The sources (built at P1's preroll, after the naming rolls of item 11)

1. **Hooks.** Every hook of every row rolled in P0 and P1 (the dial rows and the scale row included) and the `hooks_common` its table and sub-table give it. `phase: PN` is the due phase (a `P1` hook is due at P1 itself); `validator` is due at the full validator run; `play` is recorded and never gates a birth.
2. **Overrides.** Every override of a rolled row (`design.json#identity.overrides`, the foundation rows' own): due at the default's phase, the text built from the default's `what` and the override's `to`; where `claims.yaml` gives a `combines` line for two rolled rows, one promise carries the combined sentence.
3. **The foundation's columns.** What the layout seated is promised to P3's map: the lifeline's part, each contest role's seat, the remnant's place, where the break struck, each prize's place. Every scar's named floors (the targets build 7c-2 gave the eighteen scars). The escalation's steps to P7. The break as a dated event to P2, the opening to P7 and the day-0 news to P8 (plan item 25, step 1, piece 5).
4. **Stubs and placements.** Every registry stub with an `owner_phase` (the orphan-stub gate keeps checking them; the ledger lists them). The non-entity placements P1 makes: the god and the event the premise names (due P2), each premise clue's place (due P6).
5. **What the writer must make concrete.** An action row with `concretise: true` (what fell from the sky, what was born): due P1.
6. **The secret's clue stages** (ruling 3; secret): three promises from the archetype's clue shape and the trail row, each with the level range it must sit in, computed from `dials.level_band`: the first third, the middle third, the top escalation step's levels. Due P6 (a clue's place is a site or a node whose levels meet the range). The trail row's `acts` field is no longer read for the placing; say in the summary what else reads it.

Two promises with the same due phase and the same text are one promise with two sources.

### 3. The script rules that exist today

`check: script:<rule>` only where a script can decide now; everything else is `critic`. At this item: `stub_written` (the orphan-stub check), `clue_placed` (the validator's `clue_unplaced`), `god_registered` and `event_dated` (the god and the event P1 names exist in the registry or the history by P2's approve), `override_applied` for the one override P2 applies. A later floor turns a critic promise into a script rule when it is bound; the rule registry is one small table in the new module, so that a floor adds a rule in one place.

### 4. The validator names its phases; `EXPECTED_UNTIL` goes

- Each validator module, and each finding code that a later phase resolves by design, names the first phase it speaks at (`no_map`: P3; `clue_unplaced`: P6). The gate and the card read that; `design_approval.EXPECTED_UNTIL` is deleted.
- The per-phase validator accepts a `status: pending` row only when its `owner_phase` is later than the phase being checked (errata #23).
- `docs/tuning-births.md` loses the sentence "`map no_map` before P3 and `clue_unplaced` before P6 are expected" (row S4); the card no longer shows such a finding before its phase at all.

### 5. The card's counts (the present card, the least change)

One block: the promises due at this phase (how many, how many kept, not kept, waived); the open ones by due phase, as counts; the secret ones as three counts only (ruling 2). Before its due phase a promise is open work, never an error.

### Tests of 12a (thousands of seeds, every scale, magic, era and tone)

- The ledger is deterministic: the same seed gives the same ids, and a rolled row's every hook is in it exactly once.
- Every promise has a due phase that exists; no promise is due before the phase that made it; every override names a default of `claims.yaml` and takes its phase.
- No secret row's id, label or sentence is in `design.json`, the public dice log or the card; the secret ledger holds the three clue stages in every birth, with level ranges that are inside the level band, in order, the third on the top step, at every scale and every level band.
- The counts, reported per scale: promises per birth (smallest, median, largest), by source and by due phase.
- `no_map` before P3 and `clue_unplaced` before P6 neither close the gate nor show on the card, on the archived births as on a new one; with `EXPECTED_UNTIL` gone.
- A legacy birth gets no ledger and loads as before.

## Part 12b

### 6. Delivery

`phase PN begin` gives the phase's writers (the single writer, or the skeleton agent of a fan-out phase) and its phase critic a block "Promises due at this phase": id, source row's name, the sentence. The secret promises never enter a rendered public prompt: the agents that already read dm-only material get them by a command they run (as item 11's secret names are given). P1's own due promises go to P1's writer.

### 7. The verdict

The phase critic's return gains one entry per critic-judged promise due at the phase: `{id, verdict: kept | not_kept, note}`; `designer.py phase merge` stores id and verdict (the note stays in the critic's own file, as today's critiques do). The script rules are run at `phase check`. The secret promises are judged by a critic that reads dm-only; their verdicts are stored in the secret ledger.

### 8. The gate

- A **script** promise due at or before the phase and not kept closes the gate (code `promise`, with the ids).
- A due critic promise **without a verdict** closes the gate (code `promise_unjudged`): the critic did not do its work.
- A critic's **`not_kept`** does not close the gate (ruling 1). The card lists each public one (the source row's Turkish name, the due phase, the sentence) under "tutulmayan vaatler"; a secret one adds one to the secret count.
- The Opus protocol's stop list (`docs/tuning-births.md`, the dry-run protocol) gains "a promise judged not kept": a test birth, which approves itself, stops there for the owner as it does for the list's other entries.

### 9. The owner's waiver

`designer.py promise waive <id> "<one sentence>"`: the owner accepts a not-kept promise as it stands; recorded with the sentence in the ledger and the revision log; outside `_test-*` it asks for `--onay`; no prompt or workflow calls it. `designer.py promise list [--phase PN] [--status ...]` prints the public ledger (and, with the dm-only flag the development tab uses, the secret one).

### Tests of 12b

- A due script promise not kept closes the gate; kept, it does not; an unjudged critic promise closes it; a `not_kept` one leaves it open and appears on the card; a waiver is recorded and takes the promise off the card's list.
- The block reaches the writer and the critic of the due phase and only them; a secret promise's text is in no rendered public prompt and on no card; the secret counts are right.
- A rerun reopens what the phase judged.
- The archived births and the fixture pass as before.

## The summary (each part)

Changed files; new and changed tests; the suite's count and exit code; the counts of section "Tests of 12a"; what was adapted in the prompts, the critic's return schema and the card; where a later floor adds its sources and its script rules; anything unexpected.
