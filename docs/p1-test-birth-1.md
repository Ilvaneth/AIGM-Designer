# Test birth P1-1 — P1 alone (the protocol for the Opus tab)

*Written by the development (design and review) tab, 2026-10-05. The Opus tab runs it; the development tab never does. It stands on `docs/tuning-births.md` (the loop, the stop check, the review stop) and changes only what this file says. Where the two differ, this file holds.*

**What it is for.** The first live run of the new P1 (plan item 25, builds 1-17): the script's foundation, identity, names and promises, then the writer on `P1.premise.md` (about 3,400 words rendered), the door, the critics on the new rubrics, the promise verdicts, the English card. It measures whether the writer builds on the rolls without inventing, whether the door and the critics catch what they are meant to catch, and what P1 costs. It runs **P1 alone**: P2's rolls are not bound to the tables yet (plan item 25, "Floors" #11). The campaign is kept; after the development tab binds P2's rolls it continues from P2 on the owner's message.

**The owner is the player.** He reads the card and the phase report, both built to be spoiler-safe. The conductor never prints, quotes or summarises in the chat or in the report anything from dm-only, the mirror, a critic's reasoning file or a prompt file; the read guard refuses those reads anyway, and a refused read is recorded as a failure, never worked around.

## Before the first command

1. Read `docs/tuning-births.md` ("Before the first command", "The stop check", "Phase by phase") and `.claude/skills/dnd/SKILL-design.md`. Script syntax: `.claude/skills/dnd/SKILL-scripts.md`.
2. `py .claude/skills/dnd/scripts/paths.py project-root` must print this project, never Ashen Crown.
3. The Workflow tool needs the owner's opt-in in this tab ("workflow kullan"); it is given in the message that starts the birth.
4. While the birth runs or waits at a stop, nobody edits the working tree from another tab; the development tab only reads.
5. Never put a `design/dm-only/…` or `design/_staging/…` path into a Bash command (the read guard blocks it). Notes name ids.
6. Never edit `design/design.json`, `design/naming.json` or anything the preroll wrote: the seal refuses every unit after it.

## The birth

```bash
py .claude/skills/dnd/scripts/designer.py new _test-p1-1 --scale standard --party-size 1 --seed P1T-0001 --lang tr
py .claude/skills/dnd/scripts/designer.py -c _test-p1-1 preroll --phase P1
py .claude/skills/dnd/scripts/designer.py -c _test-p1-1 phase P1 begin --json
```

Blank dials are rolled live; `--lang tr` is the table's language, the campaign is written in English (errata 24.2 #28). `standard` because every earlier birth was `short`; the owner may name another scale in the starting message. Record the preroll's printed lines verbatim (counts, no rows).

- **S1:** `begin --json` lists exactly one entity, the premise, with `"workflow": "design-fanout"`. Anything else is a stop.
- Call the Workflow tool with `name: "design-fanout"` and `args` = that JSON object (a real JSON value, not a string).
- After the Workflow returns, before any text to the owner: `phase P1 merge --tokens <output tokens> --seconds <duration> --run-dir "<the Transcript dir the result printed>"`, then `commit --message "P1 fan-out"`.
- **The door.** A line `refused 1: …` means the door refused the premise: record the refusal lines verbatim, run `phase P1 begin --json` (the reason is now in the prompt) and the Workflow once more, then merge again. A second refusal is a stop (`door`), with both refusals' lines in the block. Never drop the premise.
- A critic return refused at the merge (for example a `rerun` at P1, refused since build 14c) is recorded verbatim; it is a stop only when the gate then shows `critic_missing`.
- A Workflow that returned `failed` or nothing is not merged: `begin --json` and the Workflow again. A traceback ends the birth there: record it and stop; do not patch.
- Then, as separate commands, never chained: `phase P1 check`, `phase P1 card`, `phase P1 report`.

## The stop check on the English card

The P1 card is English (build 14b); the Turkish lines `docs/tuning-births.md` names belong to the later phases' cards. Read P1's card so:

| Id | Stop when |
|---|---|
| S1 | as above |
| S2 band | the gate line names `band` (P1 has no band today; a band here is a fault) |
| S3 critic missing | CHECKS reads `phase —` or `wishes —`, or the gate line names `critic_missing` |
| S4 validator | CHECKS reads `validator:` with more than 0 errors, or the gate names `validator` |
| S5 seed | the gate names `seed` |
| S6 orphan stub | the gate names `orphan_stub` |
| S7 promise | the gate names `promise` or `promise_unjudged`, **or** PROMISES shows a `not kept:` line, **or** its secret line counts a not kept |
| door | the premise refused twice (above) |

A critic chain that ended at `fix` after its two loops is recorded, not a stop.

## The review stop (always, stop or not)

P1 alone runs *phase by phase*: after the card the conductor stops before `approve`, even with the gate open. It sends the owner:

```text
REVIEW · _test-p1-1 · P1 · attempt <n> · <open | S1-S7 | door>
card: <the card, verbatim>
report: <phase P1 report, verbatim>
merge: <the merge lines, verbatim; refusals included>
last command: <command> → exit <code>
runs: <the Workflow run ids>
```

and waits. The owner carries it to the development tab, which reads the campaign (dm-only included: a test birth is throwaway) and answers with one of these; the owner passes the answer back:

- **`devam`**: `phase P1 approve` (a test birth approves itself: no `--onay`), then the end block below.
- **`düzelt: <one sentence>`**: `design_revise.py -c _test-p1-1 round --phase P1 --scope entity --entity <the premise id> --action replace --text "<the sentence>"`, then `begin --json`, the Workflow, merge (with `--run-dir`), commit, check, card, report, and the review block again.
- **`isim yenile <people | institution | phenomenon>`** (the owner's reroll of one signature name): `design_names.py -c _test-p1-1 reroll --slot <slot> --onay`, then the `düzelt` path with the sentence the development tab gives (the premise is rewritten on the new four candidates; nothing else changes).
- **`vazgeç <promise id>: <one sentence>`** (the owner waives a promise a critic judged not kept): `designer.py -c _test-p1-1 promise waive <id> "<the sentence>" --onay`, then card, report, and the review block again.
- **`yeniden koş P1`**: `phase P1 rerun --reason "<the stop>"` (add `--reseed` only if the answer says so), `preroll --phase P1`, and the birth from `begin` again.
- **`bitir`**: `status --json`, `disarm`, and the report up to here; the campaign is kept as a case.

The code is not changed under a waiting P1 except by the rule of `docs/tuning-births.md` (a gate's false positive, fixed in the check alone, then check, card, report again).

## The end (after `devam`)

```bash
py .claude/skills/dnd/scripts/designer.py -c _test-p1-1 phase P1 report
py .claude/skills/dnd/scripts/design_approval.py -c _test-p1-1 leak-check campaigns/_test-p1-1/design/_approval/P1.card.md
py .claude/skills/dnd/scripts/designer.py -c _test-p1-1 status --json
py .claude/skills/dnd/scripts/designer.py -c _test-p1-1 disarm
```

The leak test passes when the card passes `leak-check`. Do not start P2. When the birth continues later, the owner's message gives `designer.py -c _test-p1-1 arm --mode birth` and the next phase.

## The report — `docs/reports/p1-test-birth-1.md`

English, ids, codes, counts and exact error text; no bible prose, no line of a prompt.

1. **Run:** campaign, seed, the rolled dials, model, session effort, start and end time, wall-clock, the Workflow run ids, the transcript directories.
2. **The phase:** agents launched, null returns, fix loops, second-critic count, the verdicts of every critic return by rubric id and reason code (the entity critics, the phase critic, the wishes critic), the door's refusals, the promise counts (due, kept, not kept, waived; secret as counts), validator errors and warnings, the real cost per role (`phase P1 report`), wall-clock per round.
3. **Failures:** every traceback, refusal and refused read, verbatim, with its command.
4. **The review rounds:** each answer the owner passed back, the commands it caused, and what changed on the next card.
5. **Leak test:** pass or fail.
6. **Observations:** anything the conductor had to guess, a command or prompt line that read ambiguously, a card line that was hard to read as the player. One line each.

## What the development tab reads at the review stop

For the next development tab, so the answer is measured, not guessed: the premise against `design.json#foundation` and `#identity` (every rolled row carried, nothing changed, nothing invented), each signature named from its candidates and carrying its `appears` notes, the trope breaks with their ties, the three sentences that are only true here; the mirror against the secret record (the cause, the chooser, the three clue stages with the ledger's level ranges, the villain's answer); the critics' notes against the rubrics (did they judge craft only, did the naming net look where the door cannot); the promise verdicts; the card as the player reads it. Secret and villain findings go to the owner as counts; row-level notes go to `docs/reports/p1-test-birth-1-SPOILER.md`.
