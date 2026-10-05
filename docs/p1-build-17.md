# Build item 17 — the dry walk of P1

*Written by the development (design and review) tab for the coding tab, 2026-10-05. The owner's ruling: before the test birth that runs P1 alone in the Opus tab, one model-free test walks the whole new P1 from the first command to the approval, so that the birth spends its tokens on the writer's and the critics' quality and not on plumbing faults.*

**What it closes.** Every piece of the new P1 has its tests, and several chains run together (foundation, identity and secret over 3,000 births; the names and the ledger over 2,400; the script-built P1 through its own door over 480; new campaign, preroll and card at each scale). What no test walks in one piece is the road after the writer: its output through the door, the script rules, the critics' verdicts, the gate, the card, the approval and what the approval records.

**One green commit:** `Plan item 25, build 17: the dry walk of P1`. No commit before the audit, no push. Run nothing that calls a model.

## The walk (one test per scale: short, standard, epic)

With the real commands, on a `_test-` campaign of its own, in this order, each step's exit code and effect asserted:

1. `designer.py new` (blank dials rolled, P0 approved as a test birth is).
2. `designer.py preroll --phase P1`: the foundation, the identity, the secret and the villain (dm-only), the names (`naming.json`, the stocks, the secret stock, the candidates), both ledgers, the seal.
3. `designer.py phase P1 begin`: the writer's prompt renders; it carries the candidates, the Names paragraph and the block of promises due at P1.
4. **The stand-in writer:** a helper builds what a writer would deliver, from the records alone and with no invention: each signature named with the first of its four candidates, `slot`, `home` and `rolled` copied from the identity record, one `appears` note for every floor its tables promised; one break row per rolled trope break with its tie; the premise row with the rolled question ids, `secret_class` from the archetype's class, `dm_only.pinned` with a god from the gods' stock and a plain event name, `clues[]` with the three stages' level ranges from the secret ledger; a public prose file and a mirror from the template whose sentences use only pooled names and lower-case common words. The helper lives in the tests; it is no part of the product.
5. `designer.py phase P1 merge`: the door passes every unit; the stubs and placements join the ledger; the `appears` notes are promises with source `note`.
6. `designer.py phase P1 check`: the script rules run; every script promise due by P1 is kept.
7. **The stand-in critics:** returns in the critic schema, saved where the real ones are saved: `pass` on every P1 rubric, and `kept` for every critic-judged promise due at P1, public and secret.
8. `designer.py phase P1 card`: the gate is open; the card shows the names the stand-in picked, the counts of the ledger, no "not run yet", no secret row, no secret-stock name.
9. `designer.py phase P1 approve`: the phase is approved; the rolled rows, the naming roots, the bags, and the villain's shape and origin pair (hashed) are in the test's own `used.json`.
10. A second campaign born right after it, on the same `used.json`, draws none of the first one's unique rows, roots or bags while the tables have others.

## The wrong turns (each its own short test, at one scale)

Each starts from the walk's state after step 4 and changes one thing:

- a signature named outside its candidates → the door refuses that unit, with the line that names the fault, and the other units are written;
- an invented capitalised word in the middle of a sentence of the public prose → refused with the word and its line;
- a field of `design.json#identity` edited after the preroll → every unit refused (the seal);
- a secret-stock name in the public prose → refused, and the line names no name;
- a signature without an `appears` note for a promised floor → refused;
- a critic's return that gives a due promise no verdict → the gate closes with `promise_unjudged`;
- a critic's `not_kept` on a public promise → the gate stays open, the card lists the promise, and `promise waive` takes it off the list;
- a critic's return with the verdict `rerun` at P1 → refused (build 14c).

## What the summary gives

Changed and new files; the suite's count and exit code; how long the three walks take; **every fault the walk found in the product** (a field name one script writes and the next does not read, a file expected and not written, a line the card prints wrong), each with its fix, listed one by one: finding them is this item's purpose. If the walk shows a fault that is a design question and not a slip, stop and report it.
