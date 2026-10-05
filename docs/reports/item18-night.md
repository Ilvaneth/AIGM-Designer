# Build item 18 — the night of 2026-10-05/06

*The design and review tab's log of the parts built and audited while the owner slept (his approval, 2026-10-05: the two tabs work through 18f together, test, audit and commit; nothing is pushed until he has looked). The coding tab's own summaries are in `docs/reports/item18-coding-summaries.md`.*

**Protocol:** the coding tab builds a part and runs the full suite; the design tab reads the diff and runs the full suite in a clean checkout (`.runtime/wt-audit`) of the commit; a part is accepted only on a green suite read from its log. Messages between the tabs go through the session messaging (verified: the coding tab answered "received").

**Before going to sleep the owner was told:** the keep-awake setting could not be checked from this session (no settings tool); he checks it himself.

## 18a — the layers; texture fills no story slot (`c0dfc40`)

Audited 2026-10-05 (see `docs/p1-tags.md` section 8 for the note): the 23 prizes, the two retired contests, no lifeline left in any contest, target or action, the layers on every P0/P1 table, the two corrections (`prize_at` on four rows, `key_kinds` on six) checked by script. The coding tab's suite: 769 tests, exit 0. The clean run at `c0dfc40`: 769 tests, OK, exit code 0, five skipped (read from the log). **Accepted.** 18b was sent to the coding tab at the same time (it builds in the main tree; the audit runs in its own checkout).
