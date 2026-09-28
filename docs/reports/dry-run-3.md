# Dry run 3 — `_test-dry-4` (protocol `docs/tuning-births.md`, phase by phase; `docs/dry-run-and-playtest.md` part A loop)

*Written by the conductor tab (Opus) on 2026-09-27. The birth ran phase by phase, stopping for review after every card, and the owner ended it at the first review stop. Ids, codes, counts and script output only.*

**Outcome in one line:** P1 was written, merged, checked and carded, and the birth stopped at its review stop before `approve`. The gate was open, and S4 was also visible: three `clue_unplaced` errors on the premise. The owner answered **`bitir`**, so P1 was never approved, P2-P8 never ran, and the campaign is kept as a case.

## 1. Run

| | |
|---|---|
| Command | `designer.py new _test-dry-4 --scale short --party-size 1 --seed DRY-0004 --lang tr` |
| Dials (all rolled) | scale short · tone political · magic high · era underground · danger heroic · content mix war, politics, exploration · party 1 · no wishes |
| Model | Opus 5.5, conductor and agents |
| Code under test | `d73989d` |
| Start / end | 2026-09-27 21:37:58 → 23:56:18 (guard disarmed). The time after the P1 report was the review wait. |
| Workflow run | P1 fan-out `wf_89316dd3-f39` · persisted script `…/c0f7afc8-114d-4073-a311-d8ce77039510/workflows/scripts/design-fanout-wf_89316dd3-f39.js` · transcript dir `…/c0f7afc8-114d-4073-a311-d8ce77039510/subagents/workflows/wf_89316dd3-f39` (passed to `merge --run-dir`) |
| Registry after P1 | 8 rows: `premise__test_dry_4`, `signature_cairnkin`, `signature_hush_tribunal`, `signature_wickburn`, `break_tallowmark`, `event_stillwake`, `god_theashin`, `item_stillbook` |
| State at the end | P0 approved · P1 `awaiting_approval`, attempt 1, roster 1 · P2-P9 pending · guard unarmed |

## 2. Per phase (calibration)

| Phase | Status | Min | Agents | Workflow totalTokens (total context, not output) | Real output | Cache read | Requests | Roster | Units merged / refused | Critics | Validator | Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | awaiting_approval (ended) | 22 | 10 | 869.319 | 6.371 | 7.978.198 | 101 | 1 | 8 / 0 | premise fix → pass, c2 pass · phase fix → pass · wishes pass | 4E / 0W | open |

- **The cost line:** this is the first report with the `--run-dir` ledger. `design_cost` printed "P1 run wf_89316dd3-f39: 10 agents. 101 requests. output 6.371. cache read 7.978.198 (peak context summed 874.545)".
- **Real output:** 6.371 tokens, under 1 % of the Workflow context figure.
- **Against dry-3's P1:** there, 9 agents, 19 min and 765.949 of context.

## 3. Failures, stops and findings

No traceback, no null agent (10/10 done), no refused unit, no failed seed call (P1: 0 calls). S1 held: `begin` listed `premise__test_dry_4`, the roster being 1.

### 3.1 The stop

**Review stop — P1, attempt 1, with S4 present.** The gate was open, and the stop was the phase-by-phase review stop.

```text
phase P1 check → designer: P1 validator — 4 errors, 0 warnings (grouped; --full for every line)
  error    map       no_map                       ×1   design/map.json missing
  error    secrecy   clue_unplaced                ×3   premise__test_dry_4 (+2 more)
  (--full) premise__test_dry_4  clue_unplaced  clue 1 placed_in npc does not exist
           premise__test_dry_4  clue_unplaced  clue 2 placed_in npc does not exist
           premise__test_dry_4  clue_unplaced  clue 3 placed_in npc does not exist
phase P1 card → **Kapı:** açık ✓
phase P1 report → PHASE REPORT · _test-dry-4 · P1 · attempt 1
- status: awaiting_approval · gate: open
- roster: 1 (merged 1)
- critics: entity returns 4, fix 1 · phase fix → pass · wishes pass · skeleton —
- fix reasons: rubric_p1_signatures_pervade/summary_years_vs_rule_days_months ×1, rubric_p1_signatures_pervade/pitch_years_vs_rule_days_months ×1, rubric_p1_signatures_pervade/wickburn_tallowmark_contradiction ×1
- validator: 4 errors, 0 warnings
- band: —
- cost: 10 agents, 101 requests, output 6.371, cache read 7.978.198 · Workflow context 869.319 · wall 22 min
- look at: —
- card: design/_approval/P1.card.md
```

- **Why S4:** the `clue_unplaced` errors are new against dry-3's P1, which had only `no_map`. They also name this card's `premise__test_dry_4` row, which meets S4's own-id clause.
- **What the gate did:** it did not close on them. The conductor asked the development tab whether these clues are expected to wait for a later phase's placement.
- **Answer:** `bitir`. `status --json` was run and saved, then `disarm` printed "designer: guard disarmed". `approve` was never run.

### 3.2 Findings for the development tab

1. **`clue_unplaced` ×3 at P1 does not close the gate.**
   - The premise's three act-1 clues point `placed_in` at an NPC that does not exist yet.
   - Either the check should accept a clue whose holder a later phase places (errata 24.2 #10's `pending` pattern), or the gate should close on it.
   - Today the card shows 4 errors under an open gate, and only the stop check's S4 caught it.
2. **The premise lands close to dry-3's.**
   - **The concept:** a tribunal that acts for the dead again (`signature_hush_tribunal`, "ölüleri hukukta temsil eden mahkeme", against dry-3's `signature_cairn_tribunal`).
   - **The names:** Hush Tribunal, Cairnkin, Stillwake and Stillbook share roots with dry-3's the Cairn Tribunal, Hushgate, Cairnmarch, Stillcandle and Stilltongue. No full name repeats, so the door and `name_registry` pass them.
   - **Also:** a people who turn to stone (Cairnkin) and a ledger of the dead (Stillbook) sit beside dry-3's stone-carved debts.
   - **Why it matters:** errata 24.2 #18 allows roots to recur across campaigns. At the concept level, though, this is the regression to the mean that risk 24.1 #18 names, and a uniqueness judge would likely note it. It also connects to dry-2's finding 3.2 #6: `used.json` is not written at birth. The card nevertheless prints "yeni mi (used.json): evet".
3. **P1's critics disagreed on a pervasion rule.** The phase critic's three `rubric_p1_signatures_pervade` fixes flag years in the summary and pitch against the Wickburn rule's days and months, and a Wickburn/Tallowmark contradiction. The phase-level fix passed on its second pass.

## 4. Leak scan and load budget

Not run; the birth ended at P1. The P1 card's own scan printed "leak scan clean".

## 5. P9 — not run

## 6. The playtest — not run

## 7. Uniqueness

Not run: `design_compare` against `_test-dry-1` and `_test-dry-3`, and the uniqueness judge against `_test-dry-3`, were due after P8. Finding 3.2 #2 records the premise-level overlap with dry-3 visible on the P1 card.
