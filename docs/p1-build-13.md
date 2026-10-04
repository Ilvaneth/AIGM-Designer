# Build item 13 — the campaign is written in English; the door

*Written by the development (design and review) tab for the coding tab, 2026-10-04. The design is plan item 25 ("The door, the critics and the card"; "Common rules"), errata 24.2 #17, #25, the notes of `docs/reports/tags-grouping-analysis-1.md` section 8, and the owner's ruling of 2026-10-04 below. Where a source and this file differ, stop and report.*

**The owner's ruling (2026-10-04).** "Bütün kampanya ENG yazılsın, TR oynatılır." Asked what that covers, the owner answered: everything. Every file the designer produces is English: the bible, the dm-only layer, the player's files (primer, common knowledge, news), the cards the owner reads at the review stops, the foundation's own text. Turkish is spoken at the table only: the DM narrates in Turkish at play. This replaces the "Turkish prose carrying English names" reading of errata #17 and the project rule "the narration is Turkish, the world is not" as far as the *written* campaign goes; the world's names stay English fantasy names as before.

**Why it sits here.** The door's last open question was how to catch an invented proper noun inside Turkish prose. In English prose a capitalised word inside a sentence is a proper noun; the question is gone.

**Two green commits, in this order.** After each: the full suite green (the exit code), no commit before the audit, no push.

| Part | What | Commit message |
|---|---|---|
| 13a | the written language: English everywhere in a new birth | `Plan item 25, build 13a: the campaign is written in English` |
| 13b | P1's door | `Plan item 25, build 13b: the door of P1` |

**Limits.**
- Legacy births (no foundation, or a foundation written before this item) keep their Turkish files and load as they are; `test_regression_births` stays green; the fixture stays as it is.
- The play side is untouched: the DM narrates in Turkish; the Turkish suffix rules belong to play.
- P2-P8's own prompts, tables and the player-file renderer are rewritten at their floors' turn. Here: what is global (the common preamble, the manifest's setting, the door, the card's strings) and everything of P0 and P1. Say in the summary what Turkish is left in the later phases' files, as a list for their turn.
- Run nothing that calls a model. No secret row in a summary.

---

## Part 13a — the written language

### 1. One setting

A new birth's writing language is English and is no dial: nothing in `designer.py new` asks for it. The play language (`tr`) stays what the campaign's play files use. A legacy birth keeps the language it was written in.

### 2. The prompts' common preamble (`prompts/design/_common.md`)

The Language paragraph says: prose and every one-line summary are written in English; every proper noun comes from the campaign's pools (item 11) and is written as it stands; nothing is transliterated or translated. The Turkish-suffix sentence goes. The meta-language rule stays (never "the player", "the party", "the table", "the campaign", "the PC", a phase id, "skeleton", "stub", "the designer" in a public field or public prose). "For a Turkish-speaking table" stays as the reader the DM will narrate to.

### 3. The tables of P0 and P1 lose their Turkish

- Every `tr` field of `dials.yaml`, `scale.yaml`, `foundation.yaml`, `trope-breaks.yaml`, `signatures.yaml`, `tensions.yaml`, `secrets.yaml`, `antagonists.yaml`'s P1 sub-tables and `naming.yaml` goes (the owner's rule: a superseded behaviour is deleted, never kept beside the new one).
- **Before a `tr` field goes, the row's English text must say everything the Turkish said** (the Turkish rows are what the owner approved; `docs/p1-foundation-rows.md` and `docs/p1-tags.md` are the record). Where the English `label` / `statement` / other field is thinner than the Turkish (a sense line, a weak point, a note, a table effect), write the missing English into a named field. List every row you added English text to, in a file for the audit; for the secret and villain tables give the list to the development tab only, by path, not in the summary.
- The foundation's Turkish sentence (the five templates, the three tense forms of each action, the `_note` fields, the lead phrases "Yaraları:", "İşaretler belli:", "İlk izleri:") goes with its tests. `design.json#foundation` keeps the structured record. In its place one short English rendering, built by script from the rows' English fields: a labelled list (the world's shape, the past, the value, the conflict, the break with its time), not an assembled sentence. Each action keeps one English form per time (past, present, imminent) only if the list needs it to read correctly; say what you chose.
- The stamps change on every touched row; they are written before the summary and committed after the audit, as before.

### 4. The cards and the logs

`design_approval.py`'s card, the gate labels, the P0 card and the public dice log's labels are English. The card's sections keep their order until item 14 gives the new card.

### 5. The door enforces the language

For a new birth: a Turkish letter (ç, ğ, ı, ö, ş, ü, İ and their capitals) in any prose file or registry text field is refused at merge, public and dm-only alike. `turkish_as_name` and the Turkish-letter check on names stay.

### 6. The documents

`SKILL-design.md`'s language lines; `naming.yaml#rules` (the `turkish_suffixing` block moves to the play skill's narration rules, where the DM reads it; say where you put it); item 11's language labels become English ("the <people's name> tongue", "the common tongue", "the old tongue"). The development tab updates `CLAUDE.md`, the plan's errata and its own notes.

### Tests of 13a

- No `tr` key and no Turkish letter in the P0 and P1 tables' rolled fields; a test turns red when one comes back.
- A new birth's preroll, card and public log hold no Turkish letter; the foundation's English rendering names every rolled piece.
- The door refuses a fragment with a Turkish letter in a new birth and accepts the same fragment in a legacy birth.
- The archived births and the fixture pass as before.

## Part 13b — P1's door

The door is the script between the writer's output and the phase's record (`phase P1 merge` and what it calls). A refusal names what is wrong, in one line per fault, and the writer's unit is retried as today. Everything below holds for a new birth; a legacy birth is checked as it is today.

### 7. The rolls are the writer's ground, not its choice

- The three signature entities exist, one each for the people, the institution and the phenomenon; each carries `home` equal to the identity record's home id, and the ids of its rolled rows equal `design.json#identity`'s. The trope-break entities are exactly the rolled ones, each with its recorded tie. The premise carries the rolled question ids.
- `design.json#foundation`, `#identity`, `#promises`' script-built part and `design/naming.json` are byte-identical to what the preroll stamped: a fragment that writes into them is refused.

### 8. The final set holds no conflict

The arbiter's `conflicting_pairs` is run over every row P1 stands on, public and secret together, tokens included. A pair refuses the merge. A pair that involves a secret row is reported to the dm-only log; the public refusal says only "a conflict in the secret layer".

### 9. Every proper noun is pooled

- **Registry names.** A signature's name is one of its slot's four candidates (the current attempt's, after a reroll). A person's or a god's given name is from its language's stock, as today. A place, region, inn, building, ship, month, day or ruin-site name is from the matching stock, or is built by pattern 6 or 7 from a pooled person or god name and a word of the pattern's list. A secret entity's name is from the secret stock and never from a public one; a public entity's never from the secret stock.
- **Prose.** In every public prose file and every public registry text field, each capitalised word that does not open a sentence, a heading, a list item or a table cell must belong to a name this campaign has pooled or registered (multi-word names matched whole), or stand on the closed list of capitalised common words. That list is data (`naming.yaml#rules.capitalised_common`): "I"; the form, region, building and site words when they stand in a name; the SRD's capitalised terms the prompts allow; nothing else. A miss is refused with the word and its line. The dm-only prose is scanned the same way against the public and the secret pools together; its refusals go to the dm-only log and the conductor sees a count.
- Report in the summary the list's first contents and every word the archived births' English-looking names would have tripped on, so that the list starts honest.

### 10. The promises are recorded

The ledger of item 12 exists for this attempt. Each signature's placement notes (where it will appear: the writer's `appears` entries, a phase and a sentence each) are structured, name a later phase, and enter the ledger as promises (source `note`). A signature without one note per floor its table promised is refused.

### 11. No secret in the public file

The existing leak scan, with three additions: no secret row's id, label or statement in any public file; no name of the secret stock in any public file; the premise's spoiler-safe abstract names the archetype's class and nothing else.

### 12. The rows' "never" lines

Where a rolled row carries a lexical `never` pattern, the door applies it to the public prose as `forbidden.yaml`'s patterns are applied; a non-lexical "never" is a promise judged by the critic (item 12). `forbidden.yaml`'s own Turkish patterns are translated or dropped for a new birth; list which.

### Tests of 13b

- Each rule above: one fragment that breaks it is refused with the right line, and the corrected fragment passes.
- A name outside the candidates, a place built from roots that is not in the stock, a public person with a secret-stock name, a capitalised invented word in the premise's prose: refused. A pattern 6 or 7 name from pooled parts: accepted.
- A fragment that rewrites a foundation or identity field: refused.
- Over thousands of seeds the script-built P1 (no writer) passes its own door: no conflict, every candidate and stock name accepted by the name rules.
- No refusal line printed to the conductor carries a secret row or a secret-stock name.
- The archived births and the fixture pass the legacy path.

## The summary (each part)

Changed files; new and changed tests; the suite's count and exit code; for 13a the list of rows that gained English text (the secret tables' list by path only) and the Turkish left for the later floors; for 13b the capitalised-common list and what tripped it; anything unexpected.
