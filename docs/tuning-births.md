# Tuning births — the protocol for slice 1c, item 8

*The birth runs in a separate **Opus** tab; the analysis and every fix happen in the Fable development tab afterwards. The Opus tab is a conductor with a notebook: it runs the loop below exactly, writes a report, and never edits the skill, the tables, the prompts or the plan. Findings are ids, codes, counts, paths and exact error text — the development tab reads the campaign files itself.*

## Before the first command

1. Read `docs/campaign-designer-plan.md` item 24 and `.claude/skills/dnd/SKILL-design.md`. Script syntax: `.claude/skills/dnd/SKILL-scripts.md`.
2. Every script is `py .claude/skills/dnd/scripts/<name>.py`. Check the data root first: `py .claude/skills/dnd/scripts/paths.py project-root` must print this project, never Ashen Crown.
3. The Workflow tool needs the user's opt-in in this tab ("workflow kullan"); it is given in the message that starts the birth.
4. Tab discipline: while a birth is running nobody edits the working tree from another tab; the development tab starts only after the report is written and the guard is disarmed.
5. Never put a `design/dm-only/…` or `design/_staging/…` path into a Bash command, not even inside a note, a `sed` pattern or a quoted error line: the read guard matches the token and blocks the command (birth 1, 3.7; birth 2, R.5). Notes name ids, never those paths.

## Birth 1 — straight through (`_test-tune-1`)

```bash
py .claude/skills/dnd/scripts/designer.py new _test-tune-1 --scale short --party-size 1 --seed TUNE-0001 --lang tr
```

Blank dials are rolled live (that exercises the roll path); the seed makes the birth reproducible. `_test-*` auto-approves every card and is git-ignored, so nothing is committed; `designer.py commit` is still run after every Workflow return, exactly as a real birth would, and prints "nothing to commit".

Then phases **P1 through P8**, each the same loop (P9 needs PCs and belongs to slice 1d; skip it):

```bash
py .claude/skills/dnd/scripts/designer.py -c _test-tune-1 preroll --phase P1
py .claude/skills/dnd/scripts/designer.py -c _test-tune-1 phase P1 begin --json
```

- If the JSON says `"workflow": "design-skeleton"`: call the Workflow tool with `name: "design-skeleton"` and `args` = that JSON object (as a real JSON value, not a string). Then `phase P1 merge`, `commit --message "P1 skeleton"`, and `phase P1 begin --json` again — it now prints the pending entities with `"workflow": "design-fanout"`.
- Call the Workflow tool with `name: "design-fanout"` and `args` = that JSON object.
- After **every** Workflow return, before any text to the user: `phase P1 merge --tokens <the output tokens the Workflow result reported> --seconds <its duration in seconds>`, then `commit --message "P1 fan-out"`. The merge is per unit: a line `refused N: …` means those units are now `failed` with their reason, and the next `phase P1 begin --json` lists exactly them (one attempt later, the reason in their prompt) — run `design-fanout` again with that JSON. Never hand-filter the JSON and never re-run a staged entity.
- `phase P1 check`, `phase P1 card` (show the card in the chat as the player would see it), `phase P1 approve` (auto; no `--onay`, no `devam` wait).
- A Workflow that returned `failed` or nothing (a session limit, a dead agent) is not merged: run `phase PN begin --json` and the Workflow again. `phase P8 merge` renders `facts`, `news` and the primer itself once the roster is complete; the after-P8 block only checks them.
- Note the wall-clock time of the phase, the number of agents the Workflow launched, how many returned null, how many fix loops ran, the critics' verdict counts, the validator's error and warning counts with rubric ids, and the exact text of anything that failed.

**Failures.** A null agent return or a refused unit: `phase PN begin --json` after the merge lists only what is still pending or failed; run `design-fanout` again with that JSON (once more). A unit still failing after the second run stays `failed`; `approve` refuses an incomplete roster, so retire it: a batch or document that never reached the registry with `designer.py -c _test-tune-1 phase PN drop --id ID --reason "tuning: failed twice"`, a registry entity with `design_revise.py -c _test-tune-1 round --phase PN --scope entity --entity ID --action remove --text "tuning: failed twice"`; then check, card, approve. Never `approve --force` in a tuning birth: record the refusal instead. An approved phase cannot `begin` again (that was birth 1's 3.5 regression; `rerun --reason` is the only way back). A script error (traceback) ends the phase: record the traceback in the report and stop the birth there; do not patch the script. When the development tab has fixed it, the same birth continues from that command (a `merge` is idempotent; nothing is restarted). `begin --json` refuses while staged fragments wait in `_staging/PN/`: merge first, always.

**After P8:**

```bash
py .claude/skills/dnd/scripts/design_check.py -c _test-tune-1
py .claude/skills/dnd/scripts/render_player.py -c _test-tune-1 check campaigns/_test-tune-1/design/player-primer.md
for f in campaigns/_test-tune-1/design/_approval/P*.card.md; do py .claude/skills/dnd/scripts/design_approval.py -c _test-tune-1 leak-check "$f"; done
py .claude/skills/dnd/scripts/designer.py -c _test-tune-1 status --json
py .claude/skills/dnd/scripts/designer.py -c _test-tune-1 disarm
```

The leak test passes when the full validator reports no `secrecy` error, the primer check is clean and every card passes `leak-check`.

## Birth 2 — the resume test (`_test-tune-2`)

Same command with `--seed TUNE-0002`. Run P1-P4 straight through. In **P5** (the roster, the widest fan-out): after the skeleton has merged and the fan-out Workflow has been running for a few minutes, stop it with TaskStop. Then:

1. `phase P5 merge --seconds <elapsed>` (a stopped Workflow reports no usage; pass no `--tokens`) — the fragments the finished agents wrote before the stop are merged; `phase P5 begin --json` must list only the entities still pending (record the count before and after).
2. Resume the same run with the Workflow tool's `resumeFromRunId`, the persisted script path from the first call's result **and the original `args` JSON** (without it the script throws `args.entities is missing`; birth 2) — finished writers come back from the cache, their critics and fixes and the unfinished writers run live, and the merge after it merges the fixed fragments a second time (idempotent). If resume is refused, run `design-fanout` fresh with the pending JSON instead, and record which of the two paths was taken.
3. Merge, check, card, approve, and continue P6-P8 as in birth 1, then the after-P8 block.

The resume test passes when no entity is written twice (the registry's `attempt` per id) and the phase card's counts match the skeleton's roster.

## Birth 3 — only if births 1 and 2 raised fixes

After the development tab has applied its fixes, one more straight birth (`_test-tune-3`, `--seed TUNE-0003`) confirms them. Same protocol as birth 1.

## The report — `docs/reports/tuning-birth-<n>.md`

English, written by the Opus tab at the end of the birth (or where it stopped), ids and codes only, never bible prose:

1. **Run** — campaign name, seed, the rolled dials, model, session effort, start and end time, total wall-clock, the Workflow run ids and their persisted script paths, the transcript directory if the tool result named one.
2. **Per phase** — a table: phase, workflow(s), agents launched, null returns, fix loops, second-critic count, critic verdicts (pass / fix / rerun, the skeleton's and the phase critic's too), merge units merged / refused (from `_staging/PN/merge.report.json`), validator errors and warnings (the grouped `phase PN check` output), wall-clock.
3. **Failures** — every traceback, refusal, blocked read and failed entity, verbatim in a code block, with the command that produced it.
4. **Leak test** and, for birth 2, **resume test** — pass or fail, with the counts.
5. **Observations** — anything the conductor had to guess, a prompt or command that read ambiguously, a card that was hard to read as the player, a Workflow that idled. One line each, with the phase and entity id.

The development tab then reads the report and the campaign under `campaigns/_test-tune-<n>/` (a test birth is throwaway, so its `dm-only/` may be read there for tuning), fixes prompts, tables, validator and scripts, runs the suite, and commits per work item.
