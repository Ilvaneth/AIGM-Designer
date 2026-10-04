# Build item 15 — the attractor cleanup, what is left of it

*Written by the development (design and review) tab for the coding tab, 2026-10-04. The list is the diagnosis of plan item 25 and the notes of `docs/reports/tags-grouping-analysis-1.md` section 8. Most of it was done on the way; this item closes the rest. One green commit: `Plan item 25, build 15: the attractor cleanup closed`. No commit before the audit, no push; run nothing that calls a model.*

## Where each entry of the list stands

| Entry | State |
|---|---|
| the lexicon's glosses | gone with item 11 (the `meaning` field is deleted) |
| the three attractor naming patterns ("Court of…", "…Assize", "…tide") | gone with item 11 |
| the signature seeds' examples and the mutation prompts | gone with item 10 (the old signature sub-tables); the development tab searched the P0 and P1 tables on 2026-10-04 and found none left |
| the underground era's calendar note (bells, tides) | to verify here (section 1) |
| the history rows (`age_silence`, `age_dimming`, `age_lanterns`, `age_reckoning`, `evtype_silencing`) | **the owner keeps them** (section 2) |

## 1. Verify and delete what is left in P0 and P1

Search `dials.yaml`, `scale.yaml`, `foundation.yaml`, `trope-breaks.yaml`, `signatures.yaml`, `tensions.yaml` and `naming.yaml` (the lexicon's roots excepted: errata 24.2 #18) for an example list, a sample name or a note that names the attractor's matter: light as a fuel or a commodity, hush and bells, ledgers and tolls, the rights or the voices of the dead, a court or a tribunal, tides, salt. In particular the underground era's calendar note. Delete what you find and list it in the summary; change no approved row's meaning. If something found is a row's own substance and not an example or a note, do not delete it: stop and report it.

## 2. The history table stays as it is

The owner ruled on 2026-10-04 that no row of `history.yaml` is removed: "The Silence", "The Dimming", "The Reckoning", "A silencing", "The dead, if they can be read" and "The price was hidden" all stay. His reason: these are general criteria of a general Campaign Designer, not the mark of one campaign, and are not to be excluded. The development tab had proposed removing five of them; the proposal is withdrawn and is not to be made again.

One change, which touches no row's text: the id `age_lanterns` (label "The Age of {Thing}") becomes `age_of_thing`; every reference follows; a legacy birth that holds the old id still loads.

## 3. The later floors

The eight attractor rows the review counted in P4's own tables, and whatever P2, P3, P5 and P6 hold, are looked at with the owner at those floors' turn, under the same ruling: a row is the owner's to keep or remove, and "it recurred in the test births" alone is no ground to remove a general row.

## Tests

- No `examples` or sample-name field in the P0 and P1 tables (the tests of items 10 and 11 already hold most of this; add what is missing).
- `age_of_thing` is drawn; a legacy birth with `age_lanterns` loads.
- The archived births and the fixture pass as before.

## The summary

Changed files; what section 1 found and deleted; the suite's count and exit code.
