# Test birth P2-1 — P0, P1 and P2 at the standard scale, after items 21 and 22 (the protocol for the Opus tab)

*Written by the design and review tab, 2026-10-09, after build items 21 (the short question, the named sides, the guard, the pitch) and 22 (P2 bound to the foundation: the cosmos rolled in the threat's order, the ledger, the frame and the door, the names, the writer, critics and card). The Opus tab runs it; the design tab never does. It stands on `docs/p1-test-birth-4.md` and `docs/tuning-births.md` where this file says nothing; where they differ, this file holds.*

**What it is for.** The first birth that runs P2 on the new machinery, and the first look at item 21's fixes in a real birth. P0 and P1 run as in birth 4 (with their review stops); then P2: the cosmos the script rolled (the gods, the planes, magic, history, the calendar, where the dead go), written by the model on the frame, judged by the new critics, shown on the new P2 card. It measures whether the writer builds on the frame without inventing, whether the door and the critics catch what they should, and whether the card reads as a D&D cosmos a player could use. Standard scale: the most common birth and a moderate cost (the weekly limit is near its top). P0, P1 and P2 only; the campaign is kept for P3.

**Nothing is hidden from the owner for now** (owner, 2026-10-05): the conductor may show him the cards and the report; it still never reads dm-only itself (the guard refuses it), and a refused read is recorded, never worked around.

## What counts as clean

The report's first line says **clean** or **not clean** for P1 and for P2 separately, and why. A phase is clean when: no traceback; no door refusal; no refused read and no permission refusal (guard or classifier); no Workflow returning `failed` or nothing; the gate open (P1: every `D&D:` piece ticked); the leak check clean; the critics' fix loops, if any, ended in `pass`. A critic's fix loop is the system working, not a fault; record it.

## Before the first command

Everything in `docs/p1-test-birth-4.md` "Before the first command" holds (read `docs/tuning-births.md` and `SKILL-design.md`; the Workflow opt-in "workflow kullan" in the starting message; nobody edits the working tree while the birth runs; no dm-only or staging path in a Bash command; never edit what the preroll wrote; no search from a folder that holds dm-only while armed; no `designer.py commit`). Also: read `docs/methods.md`'s index, the row "Running or reading a test birth".

## P0 and P1

```bash
py .claude/skills/dnd/scripts/designer.py new _test-p2-1 --scale standard --party-size 1 --seed P2T-0001 --lang tr --ask-approval
```

Run P0 and P1 exactly as `docs/p1-test-birth-4.md` "The birth", "The stop check" and "The review stop" say, with `_test-p2-1` for the campaign: the P0 review stop, then `preroll --phase P1`, `begin --json`, the Workflow, the merge with `--run-dir`, check, card, report, the P1 review stop. **The P1 review block also carries the premise's question and pitch verbatim** (item 21: one sentence per contest, at most about 35 words; three short pitch sentences; the sides named by their seats in the story sentence).

On `devam` at the P1 review stop: `phase P1 approve --onay`; **do not run P1's end block**; go on to P2.

## P2

```bash
py .claude/skills/dnd/scripts/designer.py -c _test-p2-1 preroll --phase P2
py .claude/skills/dnd/scripts/designer.py -c _test-p2-1 phase P2 begin --json
```

Record the preroll's printed lines verbatim (public rolls only; the secret ones show as labels).

- **S1:** `begin --json` lists exactly one entity, `doc_cosmology`, with `"workflow": "design-fanout"`. Anything else is a stop.
- Call the Workflow tool with `name: "design-fanout"` and `args` = that JSON object.
- After the Workflow returns: `phase P2 merge --tokens <output tokens> --seconds <duration> --run-dir "<the Transcript dir>"`.
- A Workflow that completed but lists `doc_cosmology` under `failed`, or returned nothing: record its cost with `design_cost.py -c _test-p2-1 record --phase P2 --run-dir "<its Transcript dir>"`, then `begin --json` and the Workflow again.
- **The door.** A line `refused N: …` means the cosmos door refused rows of the fragment (a frame field changed or missing, a name not from the pool, a script rule such as the god count or a festival per greater god, a secret word in public). Record the lines verbatim, run `begin --json` and the Workflow once more, then merge again. A second refusal of the same fragment is a stop (`door`).
- A traceback ends the birth there: record it and stop; do not patch.
- Then, as separate commands, never chained: `phase P2 check`, `phase P2 card`, `phase P2 report`.

The stop check is P1's table (S1, S3-S7, door) read for P2; S8 (`D&D:`) does not apply to P2. A gate item `phase_fix_due` is not a stop: run `phase P2 begin --json` (it serves the fix to the writer), the Workflow, the merge, then check, card and report again; record the round.

## The P2 review stop (always, stop or not)

After the card, before `approve`: `disarm`; send the block below to the design tab with SendMessage and wait; `arm --mode birth` before acting on the answer.

```text
REVIEW · _test-p2-1 · P2 · attempt <n> · <open | S1-S7 | door>
card: <campaigns/_test-p2-1/design/_approval/P2.card.md, verbatim>
report: <phase P2 report, verbatim>
merge: <the merge lines, verbatim; refusals included>
last command: <command> → exit <code>
runs: <the Workflow run ids, failed ones too>
```

The answers are P1's (`devam`, `düzelt: <one sentence>` with `--entity doc_cosmology`, `vazgeç <promise id>: …`, `yeniden koş P2`, `bitir`), read for P2.

## The end (after `devam` at P2)

```bash
py .claude/skills/dnd/scripts/designer.py -c _test-p2-1 phase P2 approve --onay
py .claude/skills/dnd/scripts/designer.py -c _test-p2-1 phase P2 report
py .claude/skills/dnd/scripts/design_approval.py -c _test-p2-1 leak-check campaigns/_test-p2-1/design/_approval/P1.card.md
py .claude/skills/dnd/scripts/design_approval.py -c _test-p2-1 leak-check campaigns/_test-p2-1/design/_approval/P2.card.md
py .claude/skills/dnd/scripts/designer.py -c _test-p2-1 status --json
py .claude/skills/dnd/scripts/designer.py -c _test-p2-1 disarm
```

Do not start P3.

## The report — `docs/reports/p2-test-birth-1.md`

English; ids, codes, counts and exact error text; the story sentence, the question and the pitch verbatim (they are public). First line: clean or not clean, for P1 and for P2. 1. **Run:** campaign, seed, dials, model, effort, times, the Workflow run ids and transcript directories. 2. **P0** as birth 4. **P1** as birth 4, plus the question's and the pitch's word counts. **P2:** agents, null returns, fix loops, every critic return's verdicts by rubric id and reason code, the door's refusals, the promise counts (P1's promises due at P2 kept or not), the validator, the real cost per role, wall-clock per round. 3. **Failures**, verbatim with their commands. 4. **The review rounds.** 5. **Leak tests** (both cards). 6. **Observations**, one line each (anything the conductor had to guess).

## What the design tab reads at the P2 review stop

The cosmology file against the frame and the cosmos record (nothing changed, nothing invented: every name from the pool, every rolled field as rolled); the mirror against the secret record (the threat's god seats, the origin's true layer, the hidden names, the epic home if any); the Discoverable section (the divergences, the god story); the card as the player reads it (could a cleric choose a god and a domain; are the planes, magic and the calendar usable at the table); the critics' notes against the new rubrics (did `rubric_p2_dnd_legible` judge; did the mirror-reading rubrics reach the critic that reads the mirror).
