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
