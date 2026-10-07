# Test birth P1-4 — P0 and P1 at the epic scale, after items 19 and 20 (the protocol for the Opus tab)

*Written by the development (design and review) tab, 2026-10-07, after build items 18, 19 and 20. The Opus tab runs it; the development tab never does. It stands on `docs/tuning-births.md` (the loop, the stop check, the review stop) where this file says nothing. Where the two differ, this file holds.*

**What it is for.** The owner's fourth look, and the check of items 19 and 20 (the frame of P1's rows, the writer's own fragment check, the deceived hand's public face, the pitch's question, the known villain's public face, the P0 card without dice) at the **epic** scale, with **P0**: the dials rolled live and shown at a review stop of their own, then P1 rebuilt around the threat (`docs/p1-threat-first.md`, build item 18): the layers, the threat chain (family and creature, goal, weakness, lair, the hand and the move), the secret as the threat's hidden half (four facts, three stages with three clues each, an optional twist), the writer who writes and never decides, the new rubrics and the card that opens on the story sentence with its `D&D:` line. It measures whether the story now reads as a D&D campaign, whether the writer builds on the chain without inventing, and whether the critics and the door catch what they should. At the epic scale the chain draws two contests (two questions), the villain from the CR window of a band's top near 20 (dragons, fiends, the god family), four tiers of escalation and the largest name stocks; watch them. P0 and P1 only; the campaign is kept for P2.

**Nothing is hidden from the owner for now** (owner, 2026-10-05): the conductor may show him the card and the report; it still never reads dm-only itself (the guard refuses it), and a refused read is recorded, never worked around.

## What counts as a clean birth

The owner moves to P2 only after a P1 birth with no pipeline fault. The report's first line says **clean** or **not clean**, and why. A birth is clean when: no traceback; no door refusal; no refused read and no permission refusal (guard or classifier); no Workflow returning `failed` or nothing; the gate open with every `D&D:` piece ticked; the leak check clean; and the critics' fix loops, if any, ended in `pass`. A critic's fix loop is the system working, not a fault; record it.

## Before the first command

1. Read `docs/tuning-births.md` ("Before the first command", "The stop check", "Phase by phase") and `.claude/skills/dnd/SKILL-design.md`; script syntax `.claude/skills/dnd/SKILL-scripts.md`.
2. The Workflow tool needs the owner's opt-in in this tab ("workflow kullan"), given in the starting message.
3. While the birth runs or waits at a stop, nobody edits the working tree from another tab; the development tab only reads.
4. Never put a `design/dm-only/…` or `design/_staging/…` path into a Bash command. Agents read dm-only with the Read tool, never with Bash (the prompts say so since build 18e).
5. Never edit `design/design.json`, `design/naming.json` or anything the preroll wrote: the seal refuses every unit after it.
6. While the guard is armed, a search (Grep, Glob, or a recursive Bash or PowerShell listing) from a folder that holds the campaign's `design/dm-only` is refused (build 19d); if you must search, name a path outside the campaign (the skill's folder, `docs/`).
7. Do not run `designer.py commit` in a test birth: a test campaign is git-ignored and the command has nothing to commit (the permission classifier refused it once).

## The birth

```bash
py .claude/skills/dnd/scripts/designer.py new _test-p1-4 --scale epic --party-size 1 --seed P1T-0004 --lang tr --ask-approval
```

`--ask-approval` keeps this test birth waiting for the approval words, so P0 is not approved on its own.

**The P0 review stop.** `new` prints its rolls and the P0 card's path. Send the design tab, with SendMessage:

```text
REVIEW · _test-p1-4 · P0
rolls: <the `roll:` lines new printed, verbatim>
card: <campaigns/_test-p1-4/design/_approval/P0.card.md, verbatim>
```

and wait. On `devam`: `py .claude/skills/dnd/scripts/designer.py -c _test-p1-4 phase P0 approve --onay`, then:

```bash
py .claude/skills/dnd/scripts/designer.py -c _test-p1-4 preroll --phase P1
py .claude/skills/dnd/scripts/designer.py -c _test-p1-4 phase P1 begin --json
```

Record the preroll's printed lines verbatim and the card's story sentence once the card exists.

- **S1:** `begin --json` lists exactly one entity, the premise, with `"workflow": "design-fanout"`. Anything else is a stop.
- Call the Workflow tool with `name: "design-fanout"` and `args` = that JSON object (a real JSON value).
- After the Workflow returns, before any text to the owner: `phase P1 merge --tokens <output tokens> --seconds <duration> --run-dir "<the Transcript dir the result printed>"`.
- **A Workflow that completed but lists the premise under `failed`** (or returned nothing) is not merged: record its cost with `py .claude/skills/dnd/scripts/design_cost.py -c _test-p1-4 record --phase P1 --run-dir "<its Transcript dir>"` (since build 18f a run not merged is counted, and marked so), then run `begin --json` and the Workflow again.
- **The door.** A line `refused N: …` means the door refused one or more *units of the premise's fragment* (the premise row, a signature row or a break row); the premise is relisted with them. Record the refusal lines verbatim, run `begin --json` and the Workflow once more, then merge again. A second refusal of the same fragment is a stop (`door`), with both refusals' lines.
- A critic return refused at the merge is recorded verbatim; it is a stop only when the gate then shows `critic_missing`.
- A traceback ends the birth there: record it and stop; do not patch.
- Then, as separate commands, never chained: `phase P1 check`, `phase P1 card`, `phase P1 report`.

## The stop check

| Id | Stop when |
|---|---|
| S1 | as above |
| S3 critic missing | CHECKS reads `phase —` or `wishes —`, or the gate names `critic_missing` |
| S4 validator | CHECKS reads `validator:` with more than 0 errors, or the gate names `validator` |
| S5 seed | the gate names `seed` |
| S6 orphan stub | the gate names `orphan_stub` |
| S7 promise | the gate names `promise` or `promise_unjudged`, or PROMISES shows a `not kept:` line or a secret not kept |
| S8 D&D | the gate names `dnd_incomplete`, or the `D&D:` line shows a missing piece |
| door | the same fragment refused twice |

A critic chain that ended at `fix` after its loops is recorded, not a stop. **A gate item `phase_fix_due` is not a stop either** (build 18f): the phase critic asked a fix on a row the premise writes; run `phase P1 begin --json` (it serves the fix to the premise's writer, the entry carrying `phase_fix`), the Workflow, the merge with `--run-dir`, then check, card and report again; record the round.

## The review stop (always, stop or not)

After the card, before `approve`:

1. `designer.py -c _test-p1-4 disarm` (so the development tab can read the secret layer; the guard covers every tab);
2. send the owner the block below, and wait;
3. before acting on the answer: `designer.py -c _test-p1-4 arm --mode birth`.

```text
REVIEW · _test-p1-4 · P1 · attempt <n> · <open | S1-S8 | door>
story: <the card's first line, verbatim>
card: <the card, verbatim>
report: <phase P1 report, verbatim>
merge: <the merge lines, verbatim; refusals included>
last command: <command> → exit <code>
runs: <the Workflow run ids, failed ones too>
```

Send the block to the development tab (the design and review tab) with SendMessage; it reads the campaign (dm-only included) and answers, carrying the owner's word, with one of these:

- **`devam`**: `phase P1 approve --onay` (this birth waits for the word: `--ask-approval`), then the end block.
- **`düzelt: <one sentence>`**: `design_revise.py -c _test-p1-4 round --phase P1 --scope entity --entity <the premise id> --action replace --text "<the sentence>"`, then `begin --json`, the Workflow, merge (with `--run-dir`), check, card, report, and the review block again.
- **`isim yenile <people | institution | phenomenon>`**: `design_names.py -c _test-p1-4 reroll --slot <slot> --onay`, then the `düzelt` path with the sentence the development tab gives.
- **`vazgeç <promise id>: <one sentence>`**: `designer.py -c _test-p1-4 promise waive <id> "<the sentence>" --onay`, then card, report, and the review block again.
- **`yeniden koş P1`**: `phase P1 rerun --reason "<the stop>"` (`--reseed` only if the answer says so), `preroll --phase P1`, and the birth from `begin` again.
- **`bitir`**: `status --json`, `disarm`, and the report up to here; the campaign is kept as a case.

## The end (after `devam`)

```bash
py .claude/skills/dnd/scripts/designer.py -c _test-p1-4 phase P1 report
py .claude/skills/dnd/scripts/design_approval.py -c _test-p1-4 leak-check campaigns/_test-p1-4/design/_approval/P1.card.md
py .claude/skills/dnd/scripts/designer.py -c _test-p1-4 status --json
py .claude/skills/dnd/scripts/designer.py -c _test-p1-4 disarm
```

Do not start P2.

## The report — `docs/reports/p1-test-birth-4.md`

English; ids, codes, counts and exact error text; the story sentence verbatim (it is public). 1. **Run:** campaign, seed, dials, model, effort, times, the Workflow run ids and transcript directories. 2. **P0:** the dials rolled, the card, the answer. **P1:** agents, null returns, fix loops (entity and phase: did a phase `fix` reach the writer?), every critic return's verdicts by rubric id and reason code, the door's refusals, the promise counts, the `D&D:` line, the validator, the real cost per role (unmerged runs included), wall-clock per round. 3. **Failures**, verbatim with their commands. 4. **The review rounds.** 5. **Leak test.** 6. **Observations**, one line each.

## What the development tab reads at the review stop

The story sentence and the pitch as a D&D hook (a threat with a face, something to do in session one); the premise against the chain's records (nothing changed, nothing invented: the stakes are the prize and the goal, the clues at the chain's pieces, the god pin as rolled); the mirror's four facts, three stages and nine clues against the secret record; the twist if rolled; the critics' notes against the new rubrics (did `rubric_p1_legible` judge, did the phase critic's fix reach the writer); the card as the player reads it.
