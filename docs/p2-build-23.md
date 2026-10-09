# Build item 23 — the first P2 test birth's polish

*Written by the design and review tab for the coding tab, 2026-10-09, after `_test-p2-1` (epic, a party of four): P1 and P2 ran clean on real writers, and the owner approved both. Five small faults read at the review stops (`docs/p2-tags.md`, the last two sections). None is a pipeline fault. The owner approved the work.*

**One green commit:** `Plan item 25, build 23: the first P2 birth's polish`. As always: the full suite in the background, the exit code read, a summary under "23" in `docs/reports/item18-coding-summaries.md`, a message to the design tab, the commit by path after its answer, never push. Re-stamp every changed row.

## 1. A trope break is stated in its own section, not in the pitch

`trope-breaks.yaml`'s common hook asks: "the break is stated in one sentence in the player pitch and explained through its tied foundation piece". Since build 21d the pitch is three short sentences with three jobs (the threat, the question, the first task), and an epic birth has two breaks, so the promise cannot be kept without breaking the pitch rule. The birth waived it.

The hook becomes: **"the break is stated in one sentence in the premise's trope-break section and explained through its tied foundation piece; it is public knowledge unless the row says otherwise; the pitch may echo it but need not"**. Its check reads the trope-break section. The P1 prompt's line on the breaks says the same.

**Tests:** a premise whose pitch names no break and whose trope-break section states both keeps the promise; a break missing from its section does not.

## 2. The present age's name

`_test-p2-1`'s present age was named "The Age after Thewein", although three ages stood between the ruin's age and the present. The 22d re-audit's rule meant a present that **directly follows the ruin's age** (always the case at short).

- **"The Age after <W>"** names a present that directly follows the ruin's age, began more than thirty years before the start, and comes before the move.
- **A present that follows any other age, before a coming move,** is "The Eve of the <word>", and its beginning is rolled within the thirty years before the start (the age before it runs until then).
- Every other case is unchanged.

**Tests:** over the corpus, "The Age after" appears only on a present whose previous age is the ruin's age; no "Eve" present spans more than thirty years.

## 3. The gods' gender and epithets

Read at the stop: two epithets shared a root ("Mother of the Monk", "Lady of the Monk"), and gendered epithets fell on names that read as the other gender. The writer also chose genders freely: Snorulf was written as an old woman. A god's gender is a fact the script decides.

- **Gender:** rolled per god, public, one of three: female, male, or neither. "Neither" is a classic D&D possibility for a god, a spirit or a power. The writer writes the god by that gender. The epithet follows it:
  - "Mother" or "Lady" for female;
  - "Father" or "Lord" for male;
  - for neither, the patterns without a gendered word (bearer, "the <colour> One").
- **Distinct epithet roots:** within one birth, no two epithets share a root.
- **The name itself carries no gender in the pool.** The pool generates no gendered names, so a name's sound may still read as the other gender. Say in the summary how often the corpus shows that, by a simple ending check per language family (e.g. "-ulf", "-heid"). Do not build gendered name generation in this item; it would be a naming item of its own.

**Tests:** epithets follow the gender over the corpus; no repeated root within a birth; the gender is in the frame and on the card.

## 4. The owner's tired images leave the tables

The lamp came back through `pantheon.yaml`: a symbol (a domain's `symbol_kinds`) and a church (the watch house). The owner has asked twice that candles and lamps not recur. Replace:
- **Knowledge's** "a lamp" with "a quill";
- **Light's** "a lamp" and "a candle" with "a dawn star" and "a golden disc";
- **Death's** "an extinguished lamp" with "a cold hearth";
- **`church_watch_house`'s** "towers or lamps as temples" with "towers and beacons as temples".

Search every P2 table, prompt and template for "lamp", "candle", "lantern" and "hush", and list what you found and replaced in the summary.

**Tests:** no P2 table row holds those words.

## 5. The moon's seat takes only the deviations that fit it

The moon's touched seat drew "is a place in this world", which means nothing for the moon. The moon's seat draws only among:
- `dev_unchanged`;
- `dev_renamed`;
- `dev_inverted`;
- `dev_reachable_by_death` (the moon as the land of the dead is a classic).

Write it as data on those rows, or as the moon seat's own list, and stamp it.

**Tests:** over the corpus, the moon seat holds only those deviations.
