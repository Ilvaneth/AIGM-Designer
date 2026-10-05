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
