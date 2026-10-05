# Build item 14 — the writer, the critics, the card

*Written by the development (design and review) tab for the coding tab, 2026-10-04. The design is plan item 25 ("The writer", "The door, the critics and the card"), the notes of `docs/reports/tags-grouping-analysis-1.md` section 8, the handoff notes of `docs/p1-tags.md` section 5, and the owner's approval of the card's layout on 2026-10-04 (below). It stands on items 11 (names), 12 (promises) and 13 (English, the door). Where a source and this file differ, stop and report.*

**What it closes.** `P1.premise.md` still asks the writer to decide what the script now rolls (the naming languages, the question's poles, the clues "by act"), still shows it the earlier campaigns (a steer that primes what it names, RC-11), and names neither the archetype's `cause` field nor the chooser. The critics' P1 rubrics speak of fields the tables no longer have and call a failed premise "a rerun", which would throw away rolls the owner reviewed. The card shows a Turkish sentence and no promises.

**Two green commits, in this order.** After each: the full suite green (the exit code), no commit before the audit, no push.

| Part | What | Commit message |
|---|---|---|
| 14a | the writer: `P1.premise.md`, the premise template, the registry fields | `Plan item 25, build 14a: the P1 writer builds on the rolls` |
| 14b | the critics' rubrics and the card | `Plan item 25, build 14b: the P1 critics and the card` |

**Limits.** P1 only: P2-P9's prompts, rubrics and cards wait for their floors (the common preamble was item 13's). Legacy births render and load as before. Run nothing that calls a model; the first live run of these prompts is the test birth that runs P1 alone, in the Opus tab.

---

## Part 14a — the writer

### 1. What the writer is given

The dials and wishes; `design.json#foundation` and `#identity` (the structured records with the rows' English fields: the script's English rendering of the foundation is for the card, the writer reads the records); the recorded merges and overrides; the languages and who speaks them (`naming.json`); the four candidates of each signature name and the stocks' Names paragraph (item 11); the promises due at P1 (item 12); the directions of earlier rounds. For the secret layer it reads dm-only itself, as today: the secret rolls, and the names of the secret stock by the command of item 11.

It is **not** given the earlier-campaigns block: `{{prior_campaigns}}` leaves `P1.premise.md` and stays in the critics' prompts.

### 2. What it writes

**The public premise** (`design/premise.md`, from the rewritten template):
- the question made concrete: the rolled pole pair as this world's two sides hold it, at this world's stakes (at epic, both questions, each on its contest);
- the three signatures, each under the name it picked from its four candidates, with one paragraph in a native's voice: the rule, how it shows, how it touches daily life; the people's paragraph shows both rolled traits and the attitude; the institution's its form, practice, sign and power; the phenomenon's its rule, sign, limit and who uses it;
- the trope breaks, each stated as a native would state it and explained through its recorded tie; each recorded merge said in one line; each override said as the fact it makes true here;
- the languages and who speaks them, by the labels the script gave;
- where an action row says `concretise`, what fell from the sky or what was born, named from a stock and described;
- the player pitch: three sentences, no secret;
- three sentences that could only be true in this world.

**The mirror** (`design/dm-only/premise-secret.md`):
- the secret as the break's true cause, from the archetype's `cause` field, with the chooser as the person who chose it and the twist;
- the three clues by stage: for each, the level range the ledger gives it, its kind, and the kind of place that will hold it (a promise; the place itself is P6's);
- the villain: shape, origin, tie to the break, and its answer: the rolled pole carried to its extreme;
- the god and the event the secret is pinned to (the god named from the gods' stock; both are promises to P2);
- the DM pitch;
- the signature mechanic's sketch when its gate rolled yes.

**The notes:** for each signature, where it will appear, one entry per floor its table promised (`appears`: a phase and a sentence). The door turns them into promises (item 13, section 10).

**The registry rows:** as today, with the fields in English names (`question`, `rule`, `true_rule` in place of `question_tr`, `rule_tr`, `true_rule_tr`; `docs/schemas/entities.md` follows; a legacy row keeps its old field names and still loads). Each signature row carries `home` and the ids of its rolled rows; each break row its row id and tie.

### 3. What it never does

It changes no field of the foundation or the identity; it picks or rerolls no row; it invents no proper noun (every name is a candidate, a stock name, or pattern 6 or 7 built from pooled parts); it writes no example name and no `naming.json`; it adds no faction, god, place or person the rolls did not call for beyond what the template asks. The prompt says each of these once, plainly, with the reason (the door refuses them).

### 4. The template and the skill

`templates/design/premise.md` is rewritten to the sections above. `SKILL-design.md`'s P1 line and its phase-table row say what P1 produces now (the script's foundation, identity, names and promises; the writer's premise and mirror).

### Tests of 14a

- The rendered prompt of a new birth holds the records' references, the candidates, the due promises and no earlier-campaigns block; it names the `cause` field and the chooser; it holds no secret row and no secret-stock name (they are read from dm-only by the agent).
- The prompt carries no instruction to write `naming.json`, to choose roots, to mutate a family or to place clues "by act".
- A legacy birth's P1 prompt renders as before.
- The schema test: the new field names are accepted, the old ones still load for a legacy row.

## Part 14b — the critics and the card

### 5. The critics judge craft only

The critics' P1 prompts say: the rolled rows are given; judge what the writer made of them, never the rolls. A failed rubric sends the premise back to be **rewritten on the same rolls** (the fix loop, at most two rounds, as today); a critic never asks for a reroll, and "a fail is a rerun" leaves the P1 rubrics. Only the owner rerolls (a name, or the phase with a reseed).

### 6. The P1 rubrics (`rubrics.yaml`)

| Rubric | Scope | The question | Fails when |
|---|---|---|---|
| the question is concrete | public | Is the question stated as this world's two sides hold it, with something at stake a native could name? | it is an abstract pair, has an obvious right answer, or could be asked of any world |
| only true here | public | Show the three sentences that could only be true in this world. | fewer than three rest on this foundation's and identity's pieces |
| differs from the earlier campaigns | public | Does the matter the writer added (what the signatures are made of, the images, the concrete question) differ from every earlier campaign's? Read the earlier-campaigns block. | an earlier campaign's motif returns in other words |
| the signatures pervade | public | Does each signature change something a native would notice daily, and does each note say where it will appear? | a signature is decoration, or a floor its table promised has no note |
| the secret and its trail | dm-only, two critics | Is the secret told as the break's true cause with a person who chose it, and could a party find the three clues, stage by stage, without the DM's help? | a clue needs the secret to be recognised, or a clue's stage and level range disagree with the ledger |
| no people is evil by birth | public | Is any people told as evil by nature? (`forbidden.yaml` holds this one row since item 16; the owner's unchanging rule: everyone stays neutral while the campaign is formed, and alignments are set when good and evil are placed) | a people, a lineage or a culture is evil as such |

The old rows `rubric_p1_question_not_adjective` (it reads `villain_answer` and `world_default`, which `tensions.yaml` no longer has) and the old wording of the others are replaced by these. The phase critic also gives the verdict per promise due at P1 (item 12).

### 7. The card (layout approved by the owner on 2026-10-04)

English, built by script, in this order:

```text
P1 — THE FOUNDATION AND THE IDENTITY            campaign: <name>   attempt <n>

THE FOUNDATION
  The world's shape   <the spine; the palette's kinds>
  The past            <the ruin source; what it left>
  The value           <the lifeline; who lives on it>
  The conflict        <the contest; the role count> (at epic, both)
  The break           <target and action, the time>
                      scars: <...>
  The escalation      <n> steps (levels <a>-<b>)

THE IDENTITY
  The question        <the pole pair> (at epic, both)
  The people          <name> — <lineage>; <the writer's one line>
  The institution     <name> — <form>; <one line>
  The phenomenon      <name> — <one line>
  Trope breaks        <label> (tied to <piece>)
  Languages           <label> · <label> · the old tongue

THE PLAYER PITCH
  <three sentences>

THE SECRET (spoiler-safe)
  class: <the archetype's class only>     the villain: rolled, hidden

NAMES
  <per kind: unused / drawn>

PROMISES
  due at P1: <n> — kept <a>, not kept <b>, waived <c>
    not kept: <source row> → <the sentence>
  open: P2 <n> · P3 <n> · ...
  secret: <n> open, <n> kept, <n> not kept

CHECKS
  door: <passed | the refusals' count> · critics: <loops>, <verdict> · validator: <errors>
  cost: <tokens>, <minutes>

YOUR MOVES
  approve · rerun · reroll a name (people | institution | phenomenon) · waive a promise
```

- **No dice on the card** (owner): no roll label, no row id, no die. The public dice log holds them.
- The candidates a name was picked from are not shown (item 11, decision 39).
- A `WISHES` block with the per-wish ticks stands between the pitch and the secret when the owner gave wishes; it is left out when there are none.
- On a rerun the diff against the archived previous card stays, as today.
- The card's leak scan stays and gains the secret stock's names and the secret rows' ids, labels and statements; a leaking card is refused.
- A legacy birth's card is built as before.

### Tests of 14b

- The rubrics table holds the six P1 rows above and none of the replaced ones; no P1 rubric says "rerun".
- The card of a script-built P1 (no writer; the writer's lines empty) holds every section in order, in English, without a roll label, a row id, a secret row or a secret-stock name; with a writer's stub output the lines are filled.
- The promise counts on the card equal the ledger's; a not-kept public promise shows with its sentence, a secret one only in the count.
- The `YOUR MOVES` line names only commands that exist.
- A legacy card is unchanged.

## The summary (each part)

Changed files; new and changed tests; the suite's count and exit code; the rendered P1 prompt's length in words before and after; anything of the old prompt you kept and why; anything unexpected.

## Added after the audit of 14a (2026-10-05), for Part 14b

- **The premise row's last `_tr` names go:** `pitch_tr` → `pitch`, `secret_tr` → `secret`, `villain_answer_tr` → `villain_answer`, `dm_pitch_tr` → `dm_pitch`, `secret_class_tr` → `secret_class`; `world_default_tr` too where it is still written. Through `design_io.text_field`, so that a legacy row's old names still load; the writer's prompt, the template's front matter, the door (`secret_class`), the leak scan, the renderers and `docs/schemas/entities.md` follow. Other entity types keep their names until their floors.
- **The card's secret line** no longer counts clues per act (the new `clues[]` has no `act`): the approved card shows the archetype's class and "the villain: rolled, hidden", nothing more.

## Corrections from the audit of 14b (2026-10-05; before its commit)

Found by reading the three script-built cards.

1. **The card's language line reads as words, not keys.** It printed "people · the common tongue · other_side · the old tongue". Each language shows its label: "the <people's name> tongue" once the people is named and "the people's tongue" before; "the common tongue"; "the other side's tongue"; "the institution's tongue"; "the old tongue". The same labels go into `naming.json` (item 11's label rule), so the writer and the card say the same.
2. **The checks line says what has not run.** A card built before any merge printed "door: passed" and "validator: None errors". Before a merge the door reads "not run yet"; a validator that has not run reads "not run yet", never `None`.
3. **The rubric "differs from the earlier campaigns" does not punish a rolled theme** (errata 24.2 #31: a general theme is not left out because an earlier campaign used it). Its `fails_when` becomes: "what the writer added (the images, what the signatures are made of, the concrete question) repeats an earlier campaign's; a rolled row or a general theme that recurs is no fault".

Accepted as the coding tab reported them: the sixth rubric's question as two sentences; the gate line under CHECKS; "open N" in the due line when it is not zero; the promise id at the end of a not-kept line (the waiver needs it); the leak scan reads a secret row's id and sentences, not its label; the new card is P1's alone; the craft-only note lives in `rubrics.yaml`.

## Part 14c — the critics' prompts and the rubrics of every phase (2026-10-05; one green commit before item 17)

Commit message: `Plan item 25, build 14c: the critics know the rolls`. Found when the owner asked whether what the critics criticise had been brought up to date: the six P1 rubrics and the craft-only note were (14b), the critics' own prompts and the rubrics that run at every phase were not. No commit before the audit, no push.

1. **No `rerun` from a P1 critic of a new birth.** `critic.md` and `phase_critic.md` offer the verdict `rerun` ("the entity is wrong at the root") and `rubrics.yaml#rules.verdict` says a rerun redraws; the craft-only note says "pass or fix". For P1 of a birth with a foundation the rendered critic prompts offer `pass`, `fix` and `note` only and say why (the rolls are sealed; only the owner rerolls), and `design_approval.py critique` refuses a P1 return that carries `rerun`. Other phases and legacy births keep the three verdicts until their floors.
2. **The critics are told what was rolled.** A critic that must judge "what the writer made of the rolls, never the rolls" has to know the rolls: for P1 of a new birth the entity critic and the phase critic are told to read `design.json#foundation` and `#identity` and the candidates of `naming.json`; the critics whose scope is dm-only also the secret identity record. The phase critic's line about "the phase's skeleton" does not apply to P1 (it has none): say what it reads instead (the premise, the mirror when its scope allows, the three signature rows and the break rows).
3. **The naming rubric is the second net behind the door.** `rubric_english_names` asks about Turkish proper nouns and banned stems, which the door and the pools now decide. It becomes: "Is every proper noun one the pools gave: a signature candidate, a stock name, or a name composed from pooled parts? Look also where the door cannot: a name that opens a sentence, a heading or a list item." Fails when "a name stands in the text that no pool holds". Its id may stay.
4. **The cliché rubric goes** (owner, 2026-10-05; errata 24.2 #31): `rubric_cliche` is deleted from `rubrics.yaml` with every reference (`phase_critic.md`'s "is the cliché's one saving detail present", tests, documents). Each phase keeps its own "only here" rubric.
5. **`history.yaml`, `age_of_thing`:** the hint's example list loses its first word: "(roads, walls, mills)" (owner, 2026-10-05). Nothing else of the row changes.

**Tests:** a P1 critic prompt of a new birth offers no `rerun` and names the records; a P1 return with `rerun` is refused, a legacy one is not; the naming rubric's new question; no `rubric_cliche` anywhere; the hint's text. **Summary:** changed files, the suite's count and exit code, the rendered P1 critic prompts' length in words.

