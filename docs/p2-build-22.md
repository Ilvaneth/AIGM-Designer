# Build item 22 — P2, the cosmos, bound to the foundation

*Written by the design and review tab for the coding tab, 2026-10-08, after the owner's review of P2 (`docs/p2-tags.md`, sessions S0-S7; the survey it stands on is `docs/reports/p2-survey.md`). P2 is rebuilt the way P1 was in items 18-20: the script rolls everything a table decides, in the threat's order, and the writer writes prose on a frame. `docs/p2-tags.md` is the specification of the rows; this file is the build. Where the two seem to differ, `p2-tags.md` holds; ask the design tab.*

**First, the tag pass (22a-0, no code; owner-approved 2026-10-08).** P1's nine tag rules (`docs/p1-tags.md` §1) hold for P2 in full. Before any row is built, the coding tab writes a draft for review, `docs/reports/p2-tags-draft.md`:
1. **Claims:** for every P2 row (the rows as `docs/p2-tags.md` leaves them, new rows included), the `topic: value` claims its own sentence, hook or effect states literally (rule 1); new topics marked as new.
2. **Clash pairs**, declared one by one (rule 2): between P2 rows, and between P2 rows and P0/P1 rows (the dials included, rule 7). Candidates to weigh, at least: the magic dial's plenty against `source_a_dying_thing`; faded magic against wild magic; P1's printed writing against `source_study`; the trope breaks on gods, magic, the moon, time and death against the pantheon, magic and calendar rows; the clashes S1-S6 already named.
3. **Overrides** (rule 4): every P0/P1 row that rewrites a P2 default, and every P2 row that rewrites a later default.
4. **Requires** (rule 5) and **fits** (rule 6, weights only).
5. **The "who sets what" chart** (rule 9) extended with P2's targets; any second owner of one target is flagged.
6. **The measurement before:** over the shared corpus extended with today's `preroll_p2`, the share of births holding a clash the draft declares (P1's figure was 86.4 % before item 10).

The design tab audits the draft; the owner reviews the new topics and the clash pairs (not each row's claims), as for P1; then 22a builds the rows with the approved tags. Rule 8: the P2 tables whose rows may repeat across campaigns (`avoid_used: false`) are exempt from the five-row floor; say for each table which it is.

**Then five green commits, in order.** After each: the full suite in the background, the exit code read, a summary under "22a" … "22e" in `docs/reports/item18-coding-summaries.md`, a message to the design tab; no commit before its answer; never push.

| Part | What | Commit message |
|---|---|---|
| 22a | the P2 tables: rows, layers, requires, conflicts (S1-S6) | `Plan item 25, build 22a: the cosmos tables` |
| 22b | the P2 roller, in the threat's order | `Plan item 25, build 22b: the cosmos rolled on the foundation` |
| 22c | the ledger, the frame and the door for P2 | `Plan item 25, build 22c: P2 keeps its promises` |
| 22d | the writer, the critics and the card | `Plan item 25, build 22d: the cosmos writer, critics and card` |
| 22e | the dry walk of P2 and the whole-P2 measurement | `Plan item 25, build 22e: the dry walk of P2` |

**Throughout.** Every row and field is English (errata #28). Every proper noun comes from a pool (errata #25): gods, planes, ages (`{Name}`, `{Thing}`, `{Rulers}`), months, days of the week, festivals, moons. A legacy birth (P2 approved before this item) keeps its records and its card; the regression pack over the archived births stays green. The arbiter, the claims, the layers, `requires`, `conflicts_with` and `avoid_used` work as they do for P1; read `design_arbiter.py`, `design_foundation.py` and `design_identity.py` before writing.

## Part 22a — the tables

Edit `pantheon.yaml`, `planes.yaml`, `magic.yaml`, `history.yaml`, `calendar.yaml` and `scale.yaml` exactly as `docs/p2-tags.md` S1-S6 say. In short:

0. **The approved tags** from the tag pass: every row's claims, the clash pairs in `claims.yaml`, the overrides, requires and fits; the "who sets what" chart.
1. **Layers on every P2 table** (S0 #1): story for the seated history events and the pinned god's seat; stage for the planes P1 names and the climate; texture for the rest. The one-way rule holds as in P1 (texture never fills a story slot).
2. **Pantheon:** `pantheon_monotheist` and `pantheon_animist` (weight 1 each; their texts in S1; the monotheist row `conflicts_with: [ruin_gods_quarrel]` through the arbiter); `pantheon_silent_gods` conflicts with `presence_omens` and `presence_walking`; `break_gods_among_mortals` forces `presence_walking`; the polytheist hook rewritten; the dead gods' "what answers" is public or discoverable. `god_secret` keeps only its five discoverable rows; the domains' `secret_tendency` lists keep only those five. Light's "an order of lamplighters" becomes "a sun temple on a height".
3. **Planes:** three new baseline rows with labels of this table's own (the fey echo, the shadow echo, the realm beyond; `group` and `spells` filled from the SRD's plane-touching spells where they apply; each with the creature families it is home to); `dev_secret_holds` deleted; `cost_name` reworded; one common hook in place of the sixteen copies.
4. **Magic:** constraint rows time, place, price in self, exhaustion, witness and none known deleted; `constraint_law_and_folk` added; `source_the_sleeper` deleted; `source_the_gods` and `source_a_dying_thing` reworded (S4); `requires` on `taboo_casting_on_a_day`, `taboo_the_phenomenon_unlicensed`, `wild_dead_god_static`, `wild_overflow`.
5. **History:** the divergence rows as S5 says (three secret rows become discoverable, three deleted); `age_dimming` loses its doom hook; `scale.yaml` history amounts: short 3 ages / 5-7 events / 2 deep, standard unchanged, epic 4-6 / 10-14 / 3-5.
6. **Calendar:** `year_shape` and `week` leave the rolls: the year is twelve months of 28 days and a seven-day week (keep the tables' texts only if something still reads them; otherwise delete them and every reference); `anchor_days_before_doom` reworded to "a counted number of days before the move's next step"; the underground era's month count is a two-row table (the light's cycle, a great clock).
7. **The fifteen hooks inside P2's tables due at P1** (S0 #7): a real dependency becomes a `requires`; every other one is deleted. List each with its fate in the summary.
8. **Every reference to a deleted row** (in any table, prompt, template, script or test) is removed or rewritten; list them in the summary.
9. The tests that pin row lists (`tests/test_design_tables.py`, about lines 292-406) follow the rows. The P2 tables get their `reviewed.json` stamps in this commit (the owner reviewed them on 2026-10-08).

**Tests:** the new and deleted rows; every `requires` and `conflicts_with` resolves; no P2 hook is due at P1; no table, prompt or script names a deleted row.

## Part 22b — the roller

A new module (`design_cosmos.py`, or the name that fits the code) replaces `preroll_p2`; `designer.py preroll --phase P2` calls it. It reads the approved P0 and P1 records (the foundation, the identity, the threat chain, the public and secret dice) and rolls in this order; every roll is a labelled record, public or secret as stated.

1. **The counts** (public): the god count in the scale's band; the rank split within the ranks' `share` bands summing to it; the great gods in their band, with the floors already ruled (a religious contest role, `break_gods_among_mortals` at least one, the unnamed god's priests); the touched-plane count (short 1, standard 1-2, epic 3-6, plus the magic dial's `planes_touched_modifier`, never below 1).
2. **The threat's seats** (secret): when the threat is `family_god`, one lesser or power slot is reserved for it; when the power behind is a god (`power_god`), one slot of any rank. At epic, the threat's home plane (by its family: S3's list) takes one touched seat. The public records show only the counts.
3. **The planes P1 names** (public), seated as touched: the thin place's plane, the ruin's, a scar's, the move's; shared to fit the count (S3; at short one plane). Then the remaining touched seats are rolled from the baseline. For each touched plane: a deviation (excluding `dev_unchanged` only if a break says so), a time rate, a way in, a cost, a keeper (a power-rank god that fits the plane's alignment, else an SRD creature of that plane); a name from the pool.
4. **The pantheon** (public, except the seats of step 2): the type (the ancestor-gods override forced; `break_gods_among_mortals` removes dead and silent; a gods-family ruin weights as already ruled; the monotheist row's conflict), the presence (with its conflicts and the forced walking), then per god: rank (from the split), 1-2 domains to the scale's coverage, an alignment from the domain's list (at standard and epic at least one evil god: re-draw the last god's alignment among its domain's evil ones if none came), a name and an epithet from the pools. The great gods are drawn among the greater gods; the pilgrim road's god (the lifeline) is a greater god. Churches: an archetype for each greater god, a church line from the domain's `church_shape` for the others. Relations: a connected web (each god after the first to an earlier one, one more per greater god; at least one rivalry and one alliance in a polytheist web; `rel_mirror` only with a pinned god). The one discoverable god story at standard and epic, on a greater god.
5. **History** (public, except the origin's true layer): the seated events first (the move dated from P1's time row; the ruin's fall as an age named from the ruin source; the villain's origin, its true layer secret from P1's chain; the signature institution's founding), counted inside the scale's events; the first age and the present age in place (the present named for what the folk fear of the threat's public face), the ruin's age seated, the ages between rolled; the remaining events by type; divergences capped at 1 / 2 / 3 by scale, every other event `div_none`; a memory row per event; witness lists for the seated story events only.
6. **Magic** (public): source, constraint, visibility, taboo(s) with their `requires`, the regulator (the three overriding rows as forced records with their reason; the dial's strictness), wild magic through the dial's gate with its `requires`. Who gives the services under the regulator (already ruled) is written in the record.
7. **The calendar** (public), last: the fixed year (12 × 28, a seven-day week; the day and month names from the pools); the climate among the palette's allowed climates (underground era forced, excluded elsewhere); the moon with its `requires` (`moon_is_a_plane` only with a free touched seat, and then it fills it); the underground count; festivals, one per greater god by its domain's `festival_kind`, plus one or two folk festivals rolled; the dated days (the empty month, the lawless day, the taboo's day, any other) seated inside the campaign's span (the scale's sessions × days per session, with the slack; 40-60 days at short); the start anchor from the move's time (S6).

Every override a P1 row names for a P2 default (the regulator's identity and strictness, the pantheon type, the great gods' floor) is applied here as a forced record with its reason, and leaves the promise ledger as kept.

**Tests:** the order (a later step never changes an earlier record); every count inside its band; the secret seats absent from the public records and the card; over the shared corpus (P1 prerolls, extended to P2): no clash the arbiter rules out, every P1-named plane touched, the domain coverage and the evil god held, festivals equal to the greater gods plus one or two, every dated day inside the span, the start anchor matching the move's time, every regulator override applied.

## Part 22c — the ledger, the frame, the door

1. **P2 joins `SOURCE_PHASES`** in `design_promises.py`: P2's rolled rows' forward hooks enter the ledger as promises to P3-P8, and P1's promises to P2 are closed by P2's records (kept, not kept, waived) the way P1's are.
2. **The frame:** at `phase P2 begin` the script writes the frame of every P2 registry row (`god_`, `plane_`, `era_`, `event_` and the calendar seed: ids, types, an object `stamped`, every rolled field), as build 20a does for P1; the door refuses a missing, changed or reshaped frame field by name; the writer checks its fragment with `registry.py check` before returning.
3. **The door's checks** (S7 #3): the god count and the domain coverage; at least one evil god at standard and epic; a festival per greater god; the four seated story events; every plane P1 names touched; twelve months of 28 days and a seven-day week; a secret seat's id or fact never in a public file.

4. **The tag pass is enforced for every floor** (errata 24.2 #33): a test fails when a phase stands in `SOURCE_PHASES` while a row of a table it rolls lacks its reviewed stamp, or while the corpus holds a birth with a declared clash among that phase's rolls. P0, P1 and P2 pass it after this item; P3-P8 cannot be bound without their own tag pass.

**Tests:** each refusal by name; P1's P2 promises close; a P2 promise to P3 appears in the ledger; the floor test above (a stamp removed in a temporary copy turns it red).

## Part 22d — the writer, the critics, the card

1. **`prompts/design/P2.cosmos.md` and `templates/design/cosmology.md`** rewritten on the frame (as P1's in 18e): the writer reads the frame and the rolls, writes the prose and the public faces, invents no proper noun outside the pools and decides nothing a table decides; "the big secret usually hides in this layer" and "all months 30 days" are gone; a villain's god appears only when the threat pins one.
2. **Rubrics** (`rubrics.yaml`): `rubric_p2_gods_carry_question` and `rubric_p2_history_diverges` rewritten, `rubric_p2_calendar_felt` kept, `rubric_p2_dnd_legible` new, all as S7 #2 says.
3. **The P2 card**, without dice or row ids (build 20b's rule): the gods with their ranks and domains, the touched planes, magic in words, the ages, the calendar and the start date; a legacy card is never rebuilt.

**Tests:** the prompt's and the rubrics' words; the card holds no die, no row id and no secret seat; a legacy P2 card is untouched.

## Part 22e — the dry walk and the measurement

The model-free dry walk of P1 (`tests/test_p1_dry_walk.py`) extended to P2: a stand-in writer fills the frame, the door, the ledger and the card run, and wrong turns are refused (a frame field changed, a P1-named plane left untouched, a festival missing for a greater god, a dated day outside the span, a secret seat named in a public file). The whole-P2 measurement over the corpus, written into the summary: the counts' spread per scale, the type and presence spread, the touched planes per scale, every domain reached, the evil god held, the divergences per scale, every P1 promise to P2 closed, and **the measurement after**: the share of births holding a declared clash (the tag pass's figure before; zero after).

**After 22e:** the design tab writes the next test birth's protocol (P0, P1 and P2 with a review stop after each), which also shows build 21's fixes in a real birth.
