# Coding tab handoff (2026-10-04)

*Written by the outgoing coding tab for the next one. No secret or villain row is named here.*

## 1. The working tree

Last commit: `bed5e0d` (build 16d). **Build 11a is finished, green (642 tests, exit code 0) and NOT committed**: it waits for the development tab's audit. Nothing was pushed (the coding tab never pushes).

Modified:
- `.claude/skills/dnd/data/design/naming.yaml` (rewritten: 17 bags, 505 roots, tags, patterns, word lists, two filter lists)
- `.claude/skills/dnd/data/design/signatures.yaml` (the 14 forms: `form_word` replaced by `name_words`; `name_word_requires` on the travelling form)
- `.claude/skills/dnd/data/design/reviewed.json` (stamps)
- `.claude/skills/dnd/prompts/design/P1.premise.md` (one sentence of the naming step)
- `.claude/skills/dnd/scripts/design_names.py` (the part-bag generator)
- `.claude/skills/dnd/scripts/design_tables.py` (`naming.yaml#family` reviewed; `naming_stamps()`)
- `.claude/skills/dnd/tests/test_design_tables.py`, `test_identity_tables.py`, `test_root_cause_1.py`

New (untracked):
- `.claude/skills/dnd/tests/test_name_tables.py`
- `docs/reports/coding-tab-handoff.md` (this file; the development tab decides whether it is committed)

Commit message when the audit passes: `Plan item 25, build 11a: the name tables and the part-bag generator`. Commit by path; `docs/p1-*.md` and the `*-SPOILER.md` audit files are the development tab's.

## 2. The 11a scripts

The one-off scripts live in the session scratchpad, outside the repository:
`C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\f92e0427-9c49-43a5-ad38-259702c75f37\scratchpad\`

- `item11a_build.py` builds `naming.yaml` from `docs/p1-build-11-bags.md` (it `exec`s the BAGS block), `-lexicon.md` (the tables and the untagged line) and `-filters.md` (the ```text blocks). It keeps the old file's `blacklist:` section and appends `real_given` / `real_places`. Re-runnable: `py <scratchpad>/item11a_build.py`. If the scratchpad is gone, the logic is small enough to rewrite from this description; the output is the committed-to-be `naming.yaml`.
- `item11a_code.py`, `item11a_tests.py`: the one-off edits (already applied; do not re-run).

The per-bag report and the 200-name samples (outside the repository):

```bash
cd .claude/skills/dnd/tests && PYTHONIOENCODING=utf-8 py test_name_tables.py --report <output dir>
```

It prints, per bag, the worst yield and worst overlap over 200 seeds and the count the real-name filter dropped in 2,000 draws, and writes `<bag id>.txt` (200 names, fixed seed) into the directory. The last run's output is `<scratchpad>/item11a-report.txt` and `<scratchpad>/item11a-bag-samples/`. It takes about 2.5 minutes.

## 3. The stamps

```bash
py .claude/skills/dnd/scripts/design_tables.py unreviewed    # lists missing / changed / gone
py .claude/skills/dnd/scripts/design_tables.py stamp         # rewrites reviewed.json
```

Order: finish every table edit → `stamp` → full suite → summary → (after the audit) commit `reviewed.json` with the item. A table edit after the stamp turns `test_claims.Inspection.test_every_p0_and_p1_row_is_stamped` red; stamp again. Rows of secret tables are stamped under hashed keys (`secret:<hash>`), so neither `reviewed.json` nor `unreviewed` names them. The name tables that are no row lists (roots, tags, pattern rows, word lists) are stamped by `design_tables.naming_stamps()` under `naming:<what>:<name>` keys.

## 4. The full suite

```bash
py .claude/skills/dnd/scripts/run_tests.py > <scratchpad>/suite.txt 2>&1; echo "exit=$?"
grep -E "^(FAIL|ERROR): |^Ran|^OK|^FAILED" <scratchpad>/suite.txt
```

It takes about 13 minutes now (the Bash tool's foreground limit is 10: run it with `run_in_background` and wait for the notification). Read the exit code, never a piped tail. To see a failure without printing rows: `grep -E "^(FAIL|ERROR)|Error:|^    self\.|^AssertionError" suite.txt | cut -c1-300`.

A commit tied to the exit code (used for every audited item):

```bash
py .claude/skills/dnd/scripts/run_tests.py > suite.txt 2>&1; rc=$?; echo "exit=$rc"
if [ $rc -eq 0 ]; then git add -- <paths>; git commit -q -m "<message>" -m "Co-Authored-By: ..." -- <paths>; fi
git log --oneline -1; git status --short
```

Do not start the next item's edits while such a background run is pending: `git add -A -- .claude/skills/dnd` would sweep them into the commit.

## 5. Traps met

- **YAML reads bare `On`, `No`, `Yes`, `on`, `no` as booleans.** Bag parts are quoted; a test asserts every part is a string. Quote any new list of short words.
- **Bash heredocs hang or break on text with many quotes or apostrophes.** Write the Python script with the Write tool and run the file. In a non-raw Python string inside such a script, `"\\n"` becomes a real `\n` in the target file only when intended; check the result (one script wrote a literal line break into a string).
- **The Windows console is cp1254:** run scripts that print non-ASCII with `PYTHONIOENCODING=utf-8`.
- **Line endings:** many files are CRLF in the working copy. Edit through bytes, normalise to `\n`, write back with the file's own ending (see the `edit()` helper in the scratch scripts). Git's "LF will be replaced by CRLF" warnings are harmless.
- **Old tests pin exact lists and counts** (row counts per family, exact `conflicts_with` / `merges_with` / claims maps, which rows carry a horror or politics weight, the craft lifeline list). A new row turns them red; update the pinned value and say so in the summary. Never lower a floor test: if a non-repeating table falls under five, stop and report.
- **Labels and prefixes are selectors.** Tests and code select by `label.startswith("break.")`, `id.startswith("life_")` and the like; a new label or id must not collide (the tie's label is `break_tie.N`; the lifeline id had to be `life_…`).
- **A forced roll has no pool record:** tests that read `R.pools[ref]` must skip runs where the draw was forced.
- **The secret layer:** the owner is also the player. No summary, commit message, test output or public file names a row of `secrets.yaml` or of the villain sub-tables of `antagonists.yaml`. Failure messages give a sub-table and a position or a count. Row-level lists go to a file whose name holds `SPOILER`, reported by path only. Tool calls that read or write those tables show rows in the transcript: warn the owner not to expand them.
- **13a holds over older wording:** tables carry no `tr` field and no Turkish letter; a row's prose is under `text`; the door refuses a Turkish letter in a new birth (`_meta.write_lang == "en"`). Where a build document asks for a Turkish field, do not write it.
- **`run_tests.py` leaves no test table behind** (`_test_tensions.yaml`, `_test_claims.yaml` are removed in `finally`); an interrupted run can leave one: delete it, never commit it.
- **A "stop and report" case is real:** when a source and the instruction differ, or a ruling has nothing to attach to, write nothing and report it; small deviations taken were always listed in the summary.

## 6. Build 11b

Nothing is written for 11b. Read so far: the whole of `docs/p1-build-11.md` (Part 11b, sections 7-13, and decisions 1-45). Points noted while reading:
- 11a's P1 prompt sentence (the writer writes `{bag, roots, label}` per language) is a stopgap: 11b deletes the task and the script writes `design/naming.json`.
- `design_names.bag_of(lang)` reads `lang["bag"]` (a family id); the bag's parts are read from `naming.yaml`, never copied into `naming.json`.
- The pattern rows are structured for a filler that does not exist yet (`parts` with `lit`, `root`, `settlement_tail`, `word`, `form_word`, `name`, `bag_word`, `one_of`; `join: joined|apart`; `whole_lexicon`, `composed_by: writer`, `only_form`, `rollable`). 11b writes the filler.
- The owner sets the session's effort to "extra" for item 12: remind him when item 12 starts.

## 7. Decisions of this session that no document states

Field and file names:
- `_meta.write_lang: "en"` marks a birth written in English; `design_manifest.writes_english(data)`; `lang` stays the play language.
- A row's English prose: `text: {...}` (same keys the Turkish had), a contest role's `text` / `text_note`. The foundation's English rendering: `design.json#foundation.rendering`, a list of `{label, text}`.
- The Turkish suffix rules: `data/play/turkish-suffixing.yaml`, pointed to from `SKILL.md`'s narration principles.
- Registry field names still end in `_tr` (`question_tr`, `rule_tr`, …); only their content is English.
- `design.json#identity` (public; `role_hints` per contest after merges) and the dm-only `dice-log.json#identity` (`secret`, `villain` with `pole`, `public_figure`, `majority_pole`).
- Roll labels: `break.N`, `break_tie.N`, `people.*`, `institution.*`, `phenomenon.*`, `tension.N`, `secret_archetype`, `secret_chooser`, `secret_chooser.role`, `secret_twist`, `secret_trail`, `bbeg_visibility`, `bbeg_shape`, `bbeg_origin`, `bbeg_tie`, `bbeg_pole`.
- Table fields added: `merge_role_hints` (trope break), `prize_with` (contest), `same_figure_with` (villain shape), `kind` / `users` (phenomenon rule), `form` (practice), `name_words` / `name_word_requires` (institution form), `statement` on the new ruin sources and the lifeline.
- used.json key for the villain's shape and origin pair: `antagonists.yaml#shape_origin_pair` (hashed).
- `naming.yaml`: `lexicon.tags[].called_by`, `lexicon.lifeline_by_seat`, `lexicon.settlement_tails`, top-level `words` and `patterns` (pattern ids `pattern_<kind>_<name>`), `rules.join`, `rules.adjectives`.

Helpers:
- `design_arbiter.arbitrate(..., weigh=)`, `conflicting_pairs(..., exempt=)`; `Roller.forced(..., exempt=)` records `conflict_exempt` and fills `Roller.exempt`; `Roller.table(..., weigh=)`.
- `design_foundation.institution_homes(contest, seated)`, `rendering(out)`; an action that destroys a role never strikes the institution's last home role (`protected_role` on the action's record).
- `design_identity.roll`, `build`, `roll_secret`, `villain_in_context`, `destroyed_role`, `fit_tie`, `inverted_weight`.
- `design_tables.stamp_key`, `naming_stamps`; `REVIEWED_TABLES` takes `file#sub` entries.
- `registry.language_errors`, `turkish_fields`.
- `design_names.join`, `bag_shape_ok`, `bag_of`, `_bag_name`, `real_given`, `within` (the same answer as `distance(a, b) <= limit`, faster); `acceptable(..., bag=, registered=, real=)`.

Rules kept as a table's own (not taste): `fracture_none`, `cultdoc_unspecified`, `verb_find_out_who` stay `forbidden: true`.

Test files by item: `test_identity_tables.py` (8), `test_secret_villain_tables.py` (9), `test_identity_roll.py` (10a, also the general themes' many-seeds test; `--floor` prints the floor report), `test_identity_secret_roll.py` (10b, 16c; `--floor`), `test_written_in_english.py` (13a), `test_forbidden_lifted.py` (16a), `test_general_themes.py` (16b, 16d), `test_name_tables.py` (11a; `--report <dir>`). `tests/_floor.py` holds the shared dial sets and the P1 many-seeds helper.

Audit files written for the development tab: `docs/reports/item13a-english-rows.md`, `item16b-technical-fields.md`, `item16c-rows-SPOILER.md`, `item9-burn-sample.md`.

## 8. Where the second coding tab stopped (2026-10-05)

Committed by this tab, none pushed by it: 11a `17ab33a`, 11b `f47caa2`, 11c `b51bd66`, 12a `634b8b2`, 12b `d82d0f6`, 13b `5dc49dd`, 14a `af3fca2`, 14b `0155af6`, 15 `ad8809b`, **14c `b534149`** (742 tests, exit code 0 on its tree).

**Build item 17 (the dry walk of P1) is written and was never run.** `.claude/skills/dnd/tests/test_p1_dry_walk.py` is untracked, on the owner's word: write it, do not run it. Nothing it asserts has been seen to pass; no fault of the product has been looked for with it yet. While the file sits in `tests/`, a full-suite run picks it up.

Run it alone (about 13 campaigns are born; it uses the read guard's marker, so never beside another test run):

```bash
cd .claude/skills/dnd/tests && PYTHONIOENCODING=utf-8 py -m unittest test_p1_dry_walk 2>&1 | tail -60
cd .claude/skills/dnd/tests && PYTHONIOENCODING=utf-8 py test_p1_dry_walk.py --times     # the three walks and how long each takes
```

Where the stand-ins live in that file:
- `Walker.born()`: steps 1-3 (`new`, `preroll --phase P1`, `phase P1 begin --json`).
- `Walker.write(change=None, public_extra="", mirror_extra="")`: the stand-in writer (step 4). It builds the three signature rows, the break rows and the premise row from the records, writes `design/premise.md` and its mirror, and stages one fragment per row. `change(rows, picked)` is the hook the wrong turns use.
- `Walker.critics(verdict="pass", promises="kept", skip=None)`: the stand-in critics (step 7): two entity returns on the premise, the phase critic's with one entry per critic-judged promise due at P1, the wishes critic's.
- `Walk.walk(scale)`: the ten steps; `WrongTurns`: the eight wrong turns, each from the state after `write()`.

Where the walk may stumble (suspected while writing, none verified):
1. **Step 3, the candidates.** The walk asserts that every candidate name is in the rendered writer prompt. The prompt points at `design/naming.json#candidates` and does not print the names; the Names paragraph (`design_names.prompt_text`) lists the stocks only. Expect this to fail: either the paragraph gains a line per slot, or the assertion is the wrong reading of "carries the candidates". A design question for the review tab if it is not a slip.
2. **Step 5, rows that are no prose type.** The signature and break rows carry `file: design/premise.md` and the premise's front matter lists them under `covers`. Untested against `registry.py`'s row checks, `stamp_check` (the premise stamps `question`) and the validator's `file_unclaimed`.
3. **Step 6, `phase P1 check` exits 1 on any validator error**, and the walk runs it with `check=True`. A `no_snapshot` or `clue_count` finding on the stand-in rows would stop it there.
4. **Step 7, the gate's own needs.** `critic_missing` reads a chain per roster item and the phase and wishes verdicts; the stand-in files are named as the workflow names them (`<premise id>.critic1.json`, `.critic2.json`, `phase.critic1.json`, `wishes.critic1.json`) but the roster's status after two merges was not checked.
5. **Step 8, the card's leak scan.** It reads every dm-only `.md` sentence of 40 characters or more and, since 14b, the secret rows' ids and sentences; the stand-in mirror's one long sentence must not be repeated on the card.
6. **Step 9, what `record_used` writes.** The walk expects `foundation.yaml#lifeline`, `secrets.yaml#archetype` (hashed), the lexicon key, `naming.yaml#family` and the villain's pair key; which tables record usage was read from the code, not run.
7. **Step 10, the second campaign.** It skips forced rows and rows with `usage_fallback`; a table whose unused rows ran out under a requirement may still trip it.
8. **The wrong turn "rerun at P1"** expects `critic_missing` on the gate after the refusal (a refused return is no verdict) and the refused file left in staging; `record_critics` was read, not run, for that.
9. The stand-in mirror names the pinned god from the public gods' stock inside a dm-only file; the door's dm-only scan knows public names, so it should pass.

## 9. Build 17 run (2026-10-05, the third coding tab)

`test_p1_dry_walk.py` ran: 11 tests green (walks: short 14.2 s, standard 14.4 s, epic 16.7 s; the file 105 s); full suite 753 tests, exit code 0. Of the nine suspicions in section 8, only the first was met, and it was the test's reading.

- **Product fault fixed:** the card printed `door: not run yet` after the merge that records the critics' returns. That merge has no fragment, deletes the last `merge.report.json` (birth 2, 3.1, pinned by `test_tuning_birth_2`) and writes none; the card read the file. Now `phase_merge` records `phases.PN.door = {at, units, refused}` whenever the door ran, `phase rerun` sets it to `None`, and the card reads it (the report file stays the fallback for births without the field).
- **Test fixes:** the candidates are pointed at (`naming.json#candidates`, as the audited 14a test reads it), not printed in the prompt; the assertions that could print a secret row, a secret-stock name or the prompt now give a short message only.
- **Noted, not fixed:** `phase rerun` keeps the previous attempt's `validator` result, so the new attempt's card can show the old "0 errors" until `check` runs.

## 10. The night of item 18 (2026-10-05/06, the third coding tab), for the next coding tab

*No secret or villain row is named here. Row-level lists are in the `*-SPOILER.md` files, reported by path only.*

**Committed (none pushed by this tab; the owner pushes):** 17 `4402177`; 18a `c0dfc40`; 18b `cc37145`; 18c-1 `35d1080`; 18c-2 `e512a4b`; 18d `f24f717`; 18e `53e66ca` (822 tests, exit 0). Each part's summary is in `docs/reports/item18-coding-summaries.md`, its fit lists and questions in `docs/reports/item18-fits.md` (secret ones in `item18c-fits-SPOILER.md`, `item18c-shapes-SPOILER.md`, `item18d-secret-SPOILER.md`).

**What 18a-18e built, in one line each:**
- 18a: `layer` on every P0/P1 table (`design_tables.layer`, `ref_of_row`), `retired:` lists (`design_tables.retired`, `rows_and_retired`; `row()` finds retired rows), `design_arbiter.STORY_SLOTS` (eight now, `secret_pin` added in 18e) and the one-way rule (`slot=` on `Roller.table`); the lifeline leaves the targets and prizes and is rolled last; 21 new prizes with `prize_at` and `key_kinds`.
- 18b: eight world states (`layer: story`, `joins`), every join public (a join to the threat counts only with a known villain, `design_threat.PUBLIC_VISIBILITY`); two bent rows; P8 hooks; `count_by_spine` with `breadth` on the spines.
- 18c-1: `design_threat.py` (family, SRD creature in the CR window or a reskin, power source, visibility, shape, origin, goal and its join `prize | role_goal | move`, weakness, lair); rolled inside `design_foundation.roll` after the contest; `dice-log.json#threat`; the chooser and the tie retired.
- 18c-2: the move: hand → target → verb (the hand table `antagonists.yaml#hand` is public and `own_hooks_only`), the goal → target relation with guards (`design_foundation.GOAL_TARGETS`, `move_targets`), `move_state`, `move.at`, the start never the heart (`start_part`, `hand_base`), the layout split in two (`lay_out_story` before the move, `lay_out_finish` after the lifeline).
- 18d: the secret as the threat's hidden half: `facts`, three `stages` × three clues (the chain's own `clue_stage` promises, six `clue` promises to P5/P6), the twist (optional), the keeping, the trails with `stages`; the archetypes retired; the hand's `base`; the new rows' hooks (G6).
- 18e: `spine_sentence`; the god pin (`secrets.yaml#god_relation`) and the mechanic's shape (`signatures.yaml#mechanic_shape`); `P1.premise.md` and the template on the chain; `appears` as `{phase, hook, text}` (a note joins its hook's promise and brings `advice`); `true_rule` only with `serves_clue`; `STORY_FIELDS`; the rubrics; the card (THE STORY, the secret in counts, the `D&D:` line) and the gate `dnd_incomplete`; the chain's tokens `prize:`, `goal_piece:` (secret), `hand_family:` registered in `claims.yaml`.

**Do first: 18e-2** (the development tab writes it in `docs/p1-build-18.md`): the spine sentence's grammar and meaning: active voice with the hand's number; each verb's phrase per target kind (the new verbs lack the target-kind fits the old actions had: "an abandoned mining city was carried off"); the greater power's own kind rolled, a god pinned only when it is a god. **Then 18f** (spec "Part 18f"): the dry walk on the chain with its new wrong turns (a texture piece in a clue's place, a true rule with no clue, a missing lair), the whole-P1 measurement and twenty spine sentences for the owner, the test birth's pipeline faults (report `docs/reports/p1-test-birth-1.md` §6; the Read-tool line is already in the writer's and the critics' prompts), and `rerun` clearing the validator's last result (item 17's note).

**The night's decisions a reader of the code needs** (each recorded in the summaries file): the order of rolls is spine, palette, ruin, contests, the story half of the layout, the threat, the hand, the target, the verb, scars, time, state, winner, the lifeline, the finish of the layout, escalation, then the identity, the secret and the names; the threat is rolled before the trope breaks (G4); no world state's join lives in dm-only; floors of five hold for every avoid_used fit pool (weaknesses, lair forms); dice-based shares over ~20 births are not asserted (test the mechanism instead); the twists' texts are hand-written under the development tab's rules and pinned by `test_p1_story`/`test_secret_layer`.

**Traps met tonight:**
- **Heredocs:** `\n` inside a heredoc-written Python string became a real line break; write scripts with the Write tool. `yaml.safe_dump` of a scalar ends with `...` (strip it).
- **Same ids in active and retired lists:** a regex on the first `- {id: X` finds the retired copy when its sub-table comes first (the twists' requirements went there once).
- **A public sub-table of a secret file** inherits the file's `hooks_common` unless it says `own_hooks_only: true`.
- **The ledger's sync** must save on any change (a merged source or advice), not only on a new key.
- **Editing during a running suite** invalidates it: stop it (TaskStop) and run again; never chain a commit to a run you have not read.
- **Secret rows in the transcript:** warn the owner before a call that prints them; failure messages give counts and positions only.

**How the two tabs worked tonight:** the development (design and review) tab, "Designer 6-Opus", sends a part with `SendMessage`; the coding tab replies "received", builds, runs the full suite, appends its summary to `item18-coding-summaries.md`, sends "18x ready: N tests, exit 0" and does not commit; the review tab audits (diff and its own clean-checkout suite) and answers "accepted" with corrections; the coding tab applies them, runs the suite, commits by path with the spec's message (`docs/reports/item18-night.md` is the review tab's, never committed by the coding tab), sends the hash. Design questions go to `item18-fits.md` and wait for the answer; small fit questions are decided by the spec's principles and listed. Find the peer with `ListAgents`; reply to the `from` of its message.

## 11. Item 18 finished (2026-10-06, the fourth coding tab), for the next coding tab

*No secret or villain row is named here.*

**Committed (none pushed by this tab):** 18e-2 `77d5339` (825 tests); 18f-1 `d8147bd` (826); 18f-2 `5f600c3` (837, exit 0). The summaries are in `docs/reports/item18-coding-summaries.md` (18e-2, 18f-1, 18f-2), the fit lists in `docs/reports/item18-fits.md` (18e-2 at the end), secret rows in `item18d-secret-SPOILER.md` (the greater power's at the end). After item 18 the development tab writes the second P1-only test birth's protocol (`docs/p1-test-birth-2.md` is its, untracked: never commit it).

**What the three parts built, in one line each:**
- 18e-2: the story sentence in active voice, the hand its subject (`number`, `text.subject` on the hands; the villain itself by its family's public label); every verb's `phrases` per target piece or `piece.kind` with `{be}` and `{target}`, and `fits` per kind, role kinds included (`role_kinds: group, settlement, person, creature`); short names (`short` on roles, `heart_short` / `key_place_short` on spines, `remnant_short` on ruins, `text.prize` on seven contests); `secrets.yaml#greater_power` (a power behind the villain, the twist's or the patron goal's, rolled once, label `P1.secret_power`; a god pinned only when it is a god); two villain family labels quoted (YAML cut them at a comma).
- 18f-1: `tests/_corpus.py`, one shared many-seed corpus (3,000 in-memory P1 prerolls, seed `CORPUS-<i>`, test_promises' dial scheme, read-only with a digest check); eleven users moved onto it; the suite went from 51 to about 24 minutes; `design_foundation.strikable_roles` / `strike_role` lifted out of `roll`, the last-home protection proved without dice.
- 18f-2: three dry-walk wrong turns on the chain; `tests/p1_measure.py` (the whole-P1 measurement and twenty fresh sentences: `py p1_measure.py`, about 10 minutes with the threat's variety report, `--no-variety` or `--only-sentences --tag T` for less); the test birth's faults: the play floor's note, a merged row drops `last_error`, the card's correction round, reason codes (null refused on a finding that is not a pass, a secret term recorded as `secret_term`), the old tongue's line, an unmerged run's cost, rerun clears the validator, and (the audit's addition) a phase critic's fix on a row a unit covers reaches that unit's writer (`design_approval.phase_fixes_due`, `designer.serve_phase_fixes`, the gate item `phase_fix_due`, `covers` in begin's entries and in `.claude/workflows/design-fanout.js`).

**Working notes:**
- **The full suite takes about 24 minutes** now (the corpus is rolled once per process). Run it with `run_in_background` and a timeout of 2 hours (the default 30-minute background cap stopped one run); watch it with `Monitor` on `tail -F <log> | grep --line-buffered "... FAIL$|... ERROR$|^Ran|^OK|^FAILED"` (`-F`, not `-f`: the log may not exist yet).
- **A test that needs many births reads `_corpus.births(n)`** and never writes into it; a test whose dials or mechanism the corpus does not hold keeps its own seeds (the list is in the 18f-1 summary).
- **Bash heredocs swallow one level of backslashes** in this tool (a `\\b` became a backspace, `\\n` a newline): every edit script with a backslash goes through the Write tool into the scratchpad and runs from there.
- **YAML reads a bare `on:` key as `True`** (the phrases' key is `for`).
- **The gate-and-commit script** of 18f-2 (`<scratchpad>/gate_18f2.sh`, this session's scratchpad) is the pattern: the full run, the exit code read, the summary's suite line filled, `git commit -- <paths>`.
- **How the two tabs worked:** the user asked for this order and protocol: a summary appended per part, a short `SendMessage` to the design and review tab (`local_39bf34e9-08ef-4d72-806d-3f2e75fc52d8`, "Designer 6-Opus"), no commit before its answer and a green gating run, never a push.

## 12. Item 19 (2026-10-06/07, the fourth coding tab), for the next coding tab

*No secret or villain row is named here. Row-level lists are in `docs/reports/item18d-secret-SPOILER.md` (19b at the end).*

**Committed (none pushed by this tab):** 19a `c585244` (853 tests, exit 0); 19b `aafa7eb` (860 tests, exit 0). The summaries are in `docs/reports/item18-coding-summaries.md` under "19a" and "19b". **Next: 19c**, "the tests never touch a live guard" (its specification is the design tab's, in `docs/p1-build-19.md`; the request as it reached this tab is below).

**What 19a and 19b built, in one line each:**
- 19a: the hand that is a side of the contest is `hand_contest_side` (the old id `hand_deceived_side` reads through `design_tables.ROW_ALIASES`; the id and label had leaked the deceit through the public dice log, design.json and the ledger); the side is a contest role, `foundation.move.hand_role`, named in the sentence by its short name with a role `number`; a move whose state is "unnoticed" has a secret hand (`dice-log.json#threat.hand`: id, role, families; the public move shows none; the sentence says "someone"/"something"); the time and the state are rolled before the hand; "an elemental"; the public "checked" section gone; the door refuses a plane's name in P1 prose (`design_door.plane_names`, `planes_in`); the pitch carries the question; a `fix` on a rubric the critic was not given is refused (`design_prompts.given_rubrics`, `design_approval.return_kind`); the agents' tools rule in `_common.md`; the report groups the fix reasons by critic and shows a flipped promise.
- 19b: a villain the visibility hides as a person among people passes as one (`design_threat.passes_as_person`: a humanoid; a shapeshifting feature that names a humanoid form; a disguise spell at will, by the day or from slots; the vampire in its own form) or wears a mask (`antagonists.yaml#mask`, secret, 4 rows, `own_hooks_only`); the mask is a fourth weakness candidate (`weak_strip_the_mask`, `by_mask`, `weakness_fits(row, family, mask)`); `build_design_index.py` records `spells_daily` and `takes_humanoid_form` in `srd-index-2014.json`.

**Decisions a reader of the code needs:**
- **The order of the move's rolls** is now time → state → hand → target → verb → struck role → scars → stronger role (19a: the state decides whether the hand is secret).
- **An unnoticed move's hand** lives only in `threat.hand`; every reader of the hand reads `move.hand or threat.hand.id` (the stage-1 clue's base, the card's D&D ticks); the world states' joins through a hand read the public hand only; its families are promised to P6 in the secret ledger (`facts.creature_types.hand`).
- **The side of the contest** (`hand_contest_side`): `design_foundation.deceived_role` (the stronger side, unless the move strikes it); its base and a coming move's start read `move.hand_role`.
- **Role numbers:** `design_foundation.role_number` (a group plural, every other kind singular, a role's own `number` over it).
- **A critic's rubrics:** `design_prompts.rubric_rows` is the one list the prompt renders and the record checks; a wishes return saved under another name reads as a phase return, so the phase kind also accepts `rubric_wishes`.
- **The phase critic's fix on a covered row** (18f-2) is served once per unit and attempt by `phase PN begin` (`designer.serve_phase_fixes`).
- **The mask:** only `vis_mystery_among_candidates` hides the villain as a person; the agent who wears its name does not fit the weakness of the mask (the design tab's reading).

**19c, as it reached this tab** (the design tab, 2026-10-06): a suite run in the main tree can remove a live birth's guard marker (`tests/_campaign.MarkerGuard` deletes `.runtime/active-design.json` at a campaign test's exit and restores only what it found at entry). Every test that arms, disarms or reads the marker works on its own runtime directory (a temporary project root, or an override the paths module honours in tests only), never the project's `.runtime`; prove it with a test that arms the real marker, runs a campaign test and finds the marker unchanged. This tab's reading, unbuilt: `paths.runtime_dir()` honours an override (say `AIGM_TEST_RUNTIME`, not prefixed `DND_` or `CLAUDE_`, which the tests strip from their subprocesses' environment) only when it points inside `tempfile.gettempdir()`; `tests/_campaign.py` sets it at import, so every test and every script a test starts inherits it; the proof test leaves a live marker as it is (it compares it before and after) and writes a sentinel only when none exists, removing it after.

**Working notes:**
- **The full suite takes about 31 minutes** (853+ tests; the corpus is rolled once per process). Run it with `run_in_background` and a 2-hour timeout; watch it with `Monitor` on `tail -n +1 -F <log> | grep --line-buffered ...` (start the monitor a few seconds after the run, or with `-F`, since the log may not exist yet; a monitor started on an old log reports its old lines).
- **A table edit invalidates a running suite**; a test-file edit does not reach the running process (the modules are imported at discovery), a script edit does reach its subprocesses.
- **Write every edit script with the Write tool**: the Bash heredoc swallows one level of backslashes (`\\b` became a backspace, `\\n` a newline, twice tonight).
- **The hub rule (the owner, 2026-10-06):** every report, summary pointer and question goes to the design and review tab by `SendMessage` (`local_39bf34e9-08ef-4d72-806d-3f2e75fc52d8`, "Designer 6-Opus"); no commit before its answer; never push. The coding tab writes its summaries under the part's heading in `docs/reports/item18-coding-summaries.md`.
- **`build_design_index.py`** rewrites `srd-index-2014.json` (and `monster-ecology.yaml`, unchanged so far); `--check` says whether they are current.
- **`monster-ecology.yaml` shows as modified** after `build_design_index.py` ran: line endings only (`git diff` shows nothing); it was left out of 19b's commit.
