# Methods that work

*Started 2026-10-08 on the owner's word: a method one tab finds and proves goes here, so every tab (design, coding, test birth) can use it. Each entry says what it catches, how to run it, and where it proved itself. Add to it when a method earns its place; never delete one without saying why.*

## Auditing a roller (the scripts that roll a phase)

### 1. The swap test (secret invariance)
- **Catches:** a public record that depends on a secret one, i.e. a leak: a public draw whose pool, weights or exclusions follow a secret roll; a secret label that appears only when a secret fact holds; a public count that moves with a secret seat.
- **How:** roll every corpus birth twice; the second time swap in another birth's secret records (the P1 bundle's `threat` and `secret`, not the arbiter context). The public records, the public dice log and the public file's secret labels and count must come out identical, at every scale.
- **Proved:** build 22b's audit (2026-10-08) found secret labels in the public `design.json` that appeared only when the threat was a god, a god stood behind the villain, a god was pinned or a vulnerable time held, and a public plane list chosen by the secret threat. It is a permanent test for P2 and **every later floor's roller gets one** (CLAUDE.md).

### 2. The order test over the whole corpus
- **Catches:** a later step that rewrites an earlier step's record.
- **How:** snapshot each step's records; after the roll, no earlier record has changed. Run it over all corpus births, not a sample.
- **Proved:** build 22b: 17 of 3,000 births had the touched-plane count rewritten by a later step; a 300-birth sample missed it.

### 3. Probing over the corpus in memory
- **Catches:** rules that hold in the tests' seeds but fail somewhere in 3,000 births; empty pools; impossible combinations.
- **How:** a scratch script imports the roller, runs the shared corpus (`tests/_corpus.py`) in memory, counts each rule's failures; nothing written to the repository.
- **Proved:** builds 18-22 (the whole-P1 and the P2 measurements; 22b's audit).

## Auditing a build

### 4. The suite in a clean checkout
- **Catches:** a green run that depended on an uncommitted file; line-ending drift.
- **How:** `git worktree add --detach .runtime/wt-audit <commit>`, run `py .runtime/wt-audit/.claude/skills/dnd/scripts/run_tests.py` without entering the folder, read the log's last lines before any note or push, then `git worktree remove` and `prune`.
- **Proved:** since build 13a; once a push followed an unread red log (2026-10-05), never since.

### 5. The ruling-by-ruling diff audit
- **Catches:** a ruling not built, built differently, or something built that no ruling asked for.
- **How:** an agent gets the rulings document (`docs/pN-tags.md`) and the diff, checks every ruling against the files, greps every deleted id across the skill, and reports misses, extras and stale references; the design tab then checks the main findings by hand.
- **Proved:** build 22a (fourteen fixes found before the commit).

## Before a specification leaves the design tab

### 6. The reference check and the last read
- **Catches:** a wrong id, path or table; a step that uses a later step's result; an impossible count; an empty pool; words that differ from the owner's ruling.
- **How:** `py docs/tools/spec_refs.py <spec>` (every not-found entry must be a new row the spec adds), then the eight-point last read in CLAUDE.md.
- **Proved:** build 22's specification (2026-10-08): the keepers before the gods, a monotheist epic against the great-gods band, an evil god from a domain with no evil alignment.

### 7. The sufficiency check (the coverage list)
- **Catches:** a gap nobody asked about.
- **How:** write the list of everything the proposal must cover before writing the proposal; tick each; compare with classic D&D (the DMG's lists, the SRD); say what was not checked.
- **Proved:** P2's names (the events had no pool) and P2's cosmos (no table said where the dead go), 2026-10-08.

## Designing a floor

### 8. The tag pass with a measurement before and after
- **Catches:** contradictions between rows of this floor, earlier floors and the dials.
- **How:** claims per row, clash pairs declared one by one, overrides, requires, fits, the "who sets what" chart; measure the share of births holding a declared clash with today's roller, then again after the build (zero). Errata 24.2 #33.
- **Proved:** P1 (86.4 % → 0), P2 (91.5 % before).

---

*The entries below were gathered on 2026-10-08 from the earlier tabs' reports (`docs/reports/`, `docs/p1-tags.md`, the protocols and the plan's delivery notes), each with where it proved itself.*

## Test births

### 9. The blind conductor's test-birth report
- **Catches:** pipeline faults no unit test reaches (merge shapes, state regressions, card errors, leaks, ambiguous protocol words).
- **How:** an Opus tab runs the protocol exactly (`docs/tuning-births.md`, `docs/p1-test-birth-N.md`) and never edits; the report holds ids, codes, counts and verbatim output: a per-phase table, Failures quoted with their commands, Observations ("anything the conductor had to guess"); the card is checked against the Workflow's raw return; the next birth lists "fixed since birth N, confirmed live". The report's first line says clean or not clean (a critic's fix loop is the system working, not a fault).
- **Proved:** tuning birth 1 (2026-09-25: all-or-nothing merge, stubs counted merged, no approve gate, card leaks, public P5 secrets); p1-test-birth-1 (14 observations); birth 4, the first clean P1 birth, unlocked P2.

### 10. The approve gate, the stop check and the STOP block
- **Catches:** a faulty phase approved and fed into the next.
- **How:** `phase PN approve` refuses with `gate closed`; check, card and approve are separate commands, never `--force`, never chained (dry-2's P6 was approved inside the command that logged its fault); the conductor sends the STOP block verbatim and the design tab answers through the owner (devam, bitir, yeniden koş, yeni doğum); a gate's false positive is fixed in the check alone.
- **Proved:** dry run 2 (2026-09-27): four stops, each at the phase that owned its fault; nothing propagated.

### 11. The review stop after every phase, with the read checklist
- **Catches:** content faults no gate sees (an abstract or echoing story, a leak by hint, something invented over the rolls).
- **How:** `phase PN report`, then the REVIEW block; the birth tab disarms so the design tab can read, and re-arms; the design tab reads the premise against `design.json#foundation` and `#identity` (nothing changed, nothing invented), the mirror against the secret record, the card as the player reads it.
- **Proved:** every P1 birth: dry run 3 led to item 25, birth 1 to item 18, birth 2 to 19a, birth 3 to 20a, birth 4 to item 21.

### 12. The resume test
- **How:** stop the widest fan-out mid-run (TaskStop), merge the partial with `--seconds` only, check that `begin --json` lists only what is pending, resume with `resumeFromRunId` and the original args; it passes when no id was attempted twice and the card's counts match the roster.
- **Proved:** tuning birth 2 (a registry crash under an exit code 0; resume needed the original args; wall time counted twice).

### 13. One code per phase
- **How:** record the code's commit per phase; never change code under a running birth (git and manifest times show it).
- **Proved:** RC-10: dry-2's P1 had run under mixed code.

## Analysis

### 14. Root-cause analysis by lenses
- **Catches:** the causes behind recurring symptoms; a fix cycle that treats symptoms only.
- **How:** read-only finders, one lens each (reports, cards, transcripts, code gates, prompts and tables, cost, process); two independent syntheses (mechanisms-first, actors-first), merged; a verifier per cause (a code lens, a data lens); completeness: every report finding maps to a cause. The same shape served the risk review, the pipeline design and the tags analysis (lenses plus an adversarial critic).
- **Proved:** root-cause analysis 1 (2026-09-27: 86 findings, 18 causes); the tags analysis (2026-09-29) found its own "0 contradictions" circular, a second clash class (17.6 %), and three faults in committed arbiter code an audit had passed.

### 15. Surveying a new floor before its review
- **How:** a read-only survey: what the floor rolls, what the writer decides freely, what earlier floors promise it; then its gaps against each method item (layers, requires, overrides, secrecy, pools, ledger, stamps, stale references).
- **Proved:** `docs/reports/p2-survey.md` (2026-10-08): no plane rolled, fifteen hooks that could never be kept, secret divergences rolled publicly, a rite that exists in no table.

### 16. The fold-in check
- **How:** after many decisions are folded into a document: a coverage checker (every target), a fidelity checker (no new contradiction, no changed decision) and a fixer; later re-read the whole file and check by count.
- **Proved:** the errata verification (2026-09-24); `docs/p1-tags.md` §4 (four open points).

### 17. Probing the platform before designing on an assumption
- **How:** instrument an existing hook to dump its payload per caller kind, then revert and record the version.
- **Proved:** the payload probe (2026-09-24): `transcript_path` does not tell the conductor from an agent; `agent_id` does.

## Measurement

### 18. Real cost from the transcripts
- **How:** `merge --run-dir DIR`; `design_cost.py record --run-dir DIR` for runs never merged; output, cache and requests per role, deduplicated by request id.
- **Proved:** RC-09: every report's "output tokens" was total context (dry run 1: 17.6 M reported, 2.9 M real); birth 3: 66 % of the real output went into a run the door refused whole.

### 19. A variety report with thresholds; fix the cause, not a weight
- **How:** `test_move.py --report`, `test_threat.py --report`: shares, every row reached, repeats, distinct sets, thresholds set before the commit; on a miss, prefer the cause (e.g. the draw order) to a compensating weight and log the decision; measure what a proposed constraint costs (pool sizes, empty pools, repeats across campaigns).
- **Proved:** 18c-2 (the thin place in 0.9 % of births and one action never: the order became hand, target, verb); 18c-1 (a weakness pool under the floor of five).

### 20. A zero is not vacuous
- **How:** beside each 0 %, say how often each measured case occurs in the sample and what the zero does not prove (only declared pairs; rolls that do not exist yet).
- **Proved:** build 10b; the tags critic's untagged pairs; the P2 tag draft §8.

### 21. Comparing two births
- **How:** `design_compare.py A B`, the uniqueness judge (`playtest.py -c A judge uniqueness --against B`), reading the new premise against the last birth's.
- **Proved:** dry run 2 read not distinct, showing `used.json` was never written; dry run 3's premise echoed dry-3's, which led to item 25.

## Tests and checks

### 22. Critique statistics turned into door rules
- **How:** `design_critique_stats.py CAMP` after every birth; a structural reason class that repeats becomes a `registry.py merge` refusal with the reason in the retry prompt, and the critics are told what the door refuses. A class closed by a script gate stays closed; a prompt fix comes back (RC-11).
- **Proved:** critique analysis 1 (2026-09-26): 29 of 46 first-critic fixes were structural leaks; after the door the first-verdict fix rate fell from 50 % to 35 %.

### 23. The regression pack over archived births, and backtesting a rule
- **How:** `tests/test_regression_births.py` replays the gates over the archived `_test-*` births, model-free; every new birth joins; a proposed stop rule is backtested before adoption. (A clean checkout skips it: the archived births are git-ignored.)
- **Proved:** 2026-09-27: dry-2 would stop at P4-P6, dry-1 at P5-P7, the sound phases open; "a critic ended at fix" would have stopped dry-2 in six of seven phases, so it is recorded, not a stop.

### 24. Reading fresh generated output
- **Catches:** grammar, meaning, real-world and obscene names, which assertions miss.
- **How:** print samples on fresh seeds and read them: `tests/p1_measure.py --only-sentences`, `test_name_tables.py --report DIR`, fresh cards.
- **Proved:** 11a (75 real names and an obscene word in 3,069); 18e (passive sentences, a city "carried off"); 21a (generic sides).

### 25. The model-free dry walk with wrong turns
- **How:** `tests/test_p1_dry_walk.py` runs the real commands from `new` to `approve` with a stand-in writer built from the records, at every scale, then a second campaign on the same `used.json`; each wrong turn changes one thing and asserts where it fails.
- **Proved:** build 17 (the card said "door: not run yet" after a door had passed); 18f-2's wrong turns on the threat chain.

### 26. Leak and readability checks on every visible artifact
- **How:** `design_leak_scan.py -c CAMP [--journal]` over a positive list of artifacts; `design_approval.py leak-check` per card; `render_player.py check`; `load_budget.py`; the playtest, readability and uniqueness judges. Every output is a leak surface: reason codes, rerun reasons, row ids, labels, a draw's die size, the secret labels.
- **Proved:** tuning birth 1 (43 secrecy errors); dry run 1 (design notes and raw ids in the primer).

### 27. Adversarial probing of a guard or a parser, old against new
- **How:** write the case list and run every case against the old and the new code at the audit.
- **Proved:** 19c (a search through dm-only's parent folder, which led to 19d); 21b (wrapped searches, which led to 21c); 21d (two splitter faults).

### 28. The writer checks its own fragment against the door
- **How:** `begin` writes each row's frame; the writer and every fix writer run `registry.py check` before returning. Critics judge prose, not shape: shape checks belong in the writer's own loop.
- **Proved:** birth 3 lost a whole run on its rows' shape; in birth 4 the door passed every unit on the first run.

### 29. The builder's audit sheet and per-row stamps
- **How:** the coding tab lists everything it wrote beyond the ruling; `design_tables.py unreviewed` and `stamp`; `test_claims` fails on an unstamped row; `git diff reviewed.json` shows the rows a commit changed.
- **Proved:** 13a (four meaning corrections); 16b (an undeclared clash).

### 30. The door run over the tables' own rows
- **How:** a test that no approved row holds a word the door would refuse.
- **Proved:** 13b (`Hells`, `Nine Hells`, `Abyss`).

### 31. Testing the mechanism, not luck
- **How:** never assert a share over a handful of births; prove a rare case without dice; read assertions for self-comparison; try every new `requires` on the legacy fixture as well as the corpus.
- **Proved:** 18f-1 (a case "exercised" by luck); 14c (an assertion compared a string with itself); 22a (the fixture's P2 preroll hit an empty pool).

**Variants of the first entries:** the swap test's earlier form rebuilt the public ledger without the secret rolls (12a, 18d); the ruling-by-ruling audit also compares the built data with the approved lists by script (11a, 16d, 21a); the clean checkout also means: commit on the exit code, never on a piped tail; no edit while the suite runs; `git status` clean in the worktree after it (line endings); no `aigm-*` folder left in the temporary directory.

**Lessons that are methods:** close a class with a gate and a class test; a parent's exit code carries its child's crash; checking within one table misses clashes across tables, so measure over many seeds; quantify the owner's diagnosis over seeds and list what was checked clean; stop and report when the source and the instruction differ, and never lower a floor test; write edit scripts with the Write tool and quote short YAML words.
