# Build item 18 — P1 rebuilt around the threat

*Written by the development (design and review) tab for the coding tab, 2026-10-05. The design is `docs/p1-threat-first.md` (errata 24.2 #32); the rows are `docs/p1-build-18-rows.md`, all approved by the owner; where this file and those two differ, stop and report. It changes item 25's P1 and stands on items 1-17.*

**What it closes.** The first P1-only test birth wrote a coherent but abstract story. Texture (the lifeline) filled story slots in 52.6 % of births, the break was a faceless target × verb, the secret was a second story stacked on it, the villain had no kind, no concrete goal, no weakness and no lair, and the writer decided what the tables did not. P1's story becomes one chain that starts from a villain who wants something, and texture only hangs on it.

**Six green commits, in this order.** After each: the full suite green (the exit code read, not a piped tail), a summary, no commit before the audit, no push. Run nothing that calls a model.

| Part | What | Commit message |
|---|---|---|
| 18a | the layers and the lifeline's leaks | `Plan item 25, build 18a: the layers; texture fills no story slot` |
| 18b | the trope breaks and the palette's size | `Plan item 25, build 18b: trope breaks bend; the palette follows the spine` |
| 18c | the threat and the move | `Plan item 25, build 18c: the threat chain` |
| 18d | the secret as the threat's hidden half, and the new rows' promises | `Plan item 25, build 18d: the secret is the threat's hidden half` |
| 18e | the writer, the rubrics and the card | `Plan item 25, build 18e: the writer, the rubrics and the card on the chain` |
| 18f | the dry walk, the measurements, the birth's pipeline faults | `Plan item 25, build 18f: the chain measured and walked` |

## Common rules (every part)

- **Compatibility (item 23):** a birth without the new records (every birth before 18c) loads, renders and validates as before; the regression pack over the archived births stays green. New fields are written beside the old ones; P2-P9 read the new fields at their own turn.
- **A removed row stays readable:** a deleted row moves to a `retired:` list of its sub-table (readable by id for legacy births, never rolled); a renamed row takes an entry in `design_tables.ROW_ALIASES` as build 15 did. Write the `retired:` reader once, in `design_tables.py`.
- **Every new table** carries a header with `layer` (18a), `roll` (labels, `secret`, `avoid_used`) and its rows' `hooks` to the floors that keep them (18d lists them); a new row is English, plain, and its label is what the owner approved.
- **Fit lists** (which hand makes which move, which weakness or lair fits which family, which creature fits which band) are drafted by the coding tab from the principles below into `docs/reports/item18-fits.md`, one table per list, before the part's commit; the development tab audits them with the part. Where a principle does not decide a pair, list it as a question rather than choosing.
- **Nothing is hidden from the owner for now** (2026-10-05), but the spoiler machinery stays working for real births: secret rolls stay in dm-only, the card stays spoiler-safe, the door and the leak scans keep their rules.

---

## Part 18a — the layers and the lifeline's leaks

### 1. The layers

Every P0 and P1 table header carries `layer`:

| Layer | Tables |
|---|---|
| `frame` (weighs tables, fills no slot) | `dials.yaml` scale, tone, magic, danger, content_mix |
| `stage` | `dials.yaml` era; `foundation.yaml` spine |
| `story` | `foundation.yaml` ruin_source, contest, break_target, action, time, escalation_tier; `tensions.yaml`; `antagonists.yaml` and `secrets.yaml` (all P1 sub-tables, and the new ones of 18c-18d) |
| `texture` | `foundation.yaml` palette, lifeline, scar; `signatures.yaml` (all); `trope-breaks.yaml` (rows may override to `story`: 18b); `naming.yaml` |

`design_tables.layer(ref, row_id=None)` returns a row's layer (the row's own `layer` first, else its sub-table's).

### 2. The story slots and the one-way rule

The story slots, as one constant in `design_arbiter.py`: the move's target, the contest's prize, the villain's goal piece, the lair's *where*, a world-state trope break's tie, the escalation's steps, the clues' places. A slot accepts only a `story` or `stage` piece. Texture may *hang on* the story (a scar the move left, a phenomenon born of the ruin, a trope break explained by the lifeline, a people the move displaced): the arrow points one way only.

- **The arbiter** excludes texture candidates from a story slot at the roll and refuses a set that holds one.
- **The door** refuses a writer's structured field that names a texture piece where a story piece is due (18e names the fields).
- **A many-seed test** (every scale × magic × era, 3,000 seeds) proves no story slot holds a texture piece.

### 3. The lifeline leaves the story

- `break_target`: `target_lifeline` retired; every action's `targets` loses `lifeline` (18c rewrites the verbs; this part only removes the target).
- **The contests** (`docs/p1-build-18-rows.md` section 3): the 23 new prizes; the new prize kinds `key_place`, `disputed_land` (an end or the land between) and `seat` (a role's house or inheritance), with the existing heart, remnant, thin place and new; the 8 lifeline `requires` become the stage gates of that table; the 11 lifeline `weight_by` go; `contest_old_new_craft` and `contest_split_family` retired. The contest's other references to the lifeline (role texts such as "who bring the thing the land needs") are rewritten without it.
- **The lifeline is rolled last** in `design_foundation.roll`, after the contest, the break and the scars, fitted to the story and the palette (its existing palette fit stays; it may weigh toward the contest's prize and the spine, never the other way).
- Everything that read the lifeline to decide a story piece (`prize_with`, the institution homes, the escalation texts, the foundation's rendering) is listed in the summary with how it now reads.

**Tests of 18a:** every table has a layer; the slot constant; the arbiter refuses a texture piece in each slot; 3,000 seeds with no texture in a story slot and no empty pool; no contest requires or is weighted by a lifeline; no `target_lifeline`; a legacy birth with the old target and prizes loads and renders.

---

## Part 18b — the trope breaks and the palette's size

`docs/p1-build-18-rows.md` sections 6 and 7.

- **The eight world states** carry `layer: story` on their rows: rulers by lot, guilds rule with no lords, magic is nobility, dragons rule the lands, a beast-person lords some lands, the moon is inhabited and trades, the gods live among mortals, the enemy won. Each is drawn only where it can join a story piece and records the join (`joins: {piece, how}`): the heart's rule and the contest; the dragon family or hand or a dragon contest; the disputed land or a contest side; the thin place or a hand; the god family or a side at the gods' level; the ruin or the villain. Their tie options exclude the lifeline. Where the threat (18c) is not yet rolled, the join to a family or a hand is a requirement 18c's roll honours (a world state that names dragons weighs the dragon families and hands); write the order so the arbiter can refuse a dead end.
- **Bend, never remove:** `break_no_writing` becomes "writing is sacred: only the ordained may write"; `break_divine_magic_holy_ground` becomes "divine magic is strongest on holy ground and costs something beyond it". Each row that touches the players gains a P8 hook ("the player files and character creation state it"). `break_casting_forbidden` and `break_no_common_tongue` stay, with that hook.
- **The palette** takes its count from the spine: each spine row gains `breadth: tight | wide` (the lists of section 7); `count_by_spine: {tight: {short: [2,3], standard: [3,4], epic: [4,5]}, wide: {short: [3,4], standard: [4,6], epic: [6,8]}}` replaces `count_by_scale`; the forced kinds (spine, era) count inside it, the ruin's extra kind on top as today; the P3 hook "every palette kind lives on at least one map node" stays.

**Tests of 18b:** the eight rows' layer and joins; no world state drawn without a join (3,000 seeds); the two bent rows' texts; the counts by spine at every scale; a legacy birth's palette loads.

---

## Part 18c — the threat and the move

`docs/p1-build-18-rows.md` sections 1, 2, 4 and 8; `docs/p1-threat-first.md` "The new core" and G1, G2, G4, G8.

### 4. The order of rolls (G4)

Written once, each roll filtered by the ones before it; the arbiter refuses a dead end:

1. spine; palette (18b); 2. ruin source; 3. contest(s); 4. **the threat** (secret): family → creature → power source (humanoid families above short) → shape → origin → visibility → goal → weakness → lair; 5. **the move** (public): hand → verb → target → time → state → the stronger role; 6. scars; 7. escalation and the start; 8. the secret (18d); 9. the identity (trope breaks with joins, people, institution, phenomenon, question, names); 10. the lifeline.

The threat's rolls move from `design_identity.roll_secret` into this chain (a new module, `design_threat.py`, called from `design_foundation.roll` or from the preroll between the foundation and the identity: the coding tab chooses and says why). The secret records stay in dm-only (`dice-log.json`, a new key `threat`); the move's records are public (`design.json#foundation.move`).

### 5. The threat

- **The family** (`antagonists.yaml#villain_family`, new; 19 rows: the 18 of section 4.1 and the god of 4.5). `avoid_used`: a family drawn in the last three births waits; never the same family twice in a row. The god family only at standard and epic. Weighted by the ruin (an undead-kings ruin weighs the undead family), the content mix (horror: undead, from beyond, fiends) and the world states (18b); the two dragon families together never exceed their share of two in the open families.
- **The creature:** an SRD creature of the family whose CR fits the band's top level *L*: CR from max(2, L−2) to L+4, and to 30 when L ≥ 17 (measured: short 3-9, standard 9-16, epic 15-30). The family → creature mapping by SRD type, subtype and name is a fit list. Where a family has no SRD creature in the window, the row records `reskin: {base, target_cr}` (the reskin rule of `sites.yaml`; the stat work is P5's). The god family's creature is always an avatar reskin.
- **The power source** (new, small; humanoid families above short): an artifact, a pact with a power, a curse it bears, what it serves (a god, a fiend, a patron), a stolen essence. The weakness may bind to it.
- **Shape, origin, visibility** (section 4.4): `shape_process`, `shape_institution`, `origin_taken_by_phenomenon`, `origin_made_by_institution` and `vis_process_or_institution` retired; added `origin_forbidden_knowledge` and `vis_known_unknown_where`. The shape `rule` texts that named an institution or a working as the villain are read once and listed in the summary.
- **The goal** (`antagonists.yaml#goal`, new; the 20 rows of 4.2): each row names its DMG family and the pieces it binds to; the roll binds it to a rolled piece (the heart, the key place, the disputed land, the remnant, the thin place where one exists, a role, something new). **The join:** the goal is the contest's prize, or the move (below) strikes a contest role. `avoid_used` across births.
- **The weakness** (`antagonists.yaml#weakness`, new; the 19 rows of 4.3) with a fit list by family (a true name: fiends, fey, genies and elementals only; a law of its nature: the undead and others whose SRD traits carry one; drawn from its lair: families with legendary or lair creatures). `avoid_used` across births.
- **The lair** (`antagonists.yaml#lair_where`, `#lair_form`, new; section 8): *where* bound to the chain (the thin place only where one exists), *what* with a fit list by family.
- **The tie and the chooser go:** `antagonists.yaml#break_tie` becomes `#move_state` (done, stopped short, backfired, unnoticed); its old rows retired. `secrets.yaml#chooser` is no longer rolled (the villain always chose); its rows retired. Every hook or conflict that named a retired row is rewritten or dropped and listed in the summary.

### 6. The move

- **The visible hand** (`antagonists.yaml#hand`, new, public; the 27 rows of section 2) with its creature family and requirements; "the villain itself" only when the visibility is known; a hand is an organisation or a creature, never a whole people (a hand drawn from a people is a part of it; its row says so).
- **The verb** (`foundation.yaml#action`; section 1): 23 verbs with their targets; the 8 deleted rows retired (`act_fell_from_sky` and `act_gave_birth` with their `concretise`); the hand → verb fit list (a creature hand makes no intrigue move: replaced, possessed, betrayed and divided belong to hands that can scheme; the coding tab drafts the list, questions marked).
- **The target** on the way to the goal: the goal's piece, or a piece that guards it, or a contest role (the join). Write the rule as a small relation (goal piece → acceptable targets) in the fit report.
- **Time and state:** the time table stays; the move's state from `#move_state`.
- **The timeline (G2):** the plan's steps always lead toward the goal; *a generation ago*: the move has ripened and step 1 comes as the campaign opens; *just now*: session 1 opens on its aftermath; *unfolding*: the party starts inside it and step 1 is its next phase; *coming*: the steps are its preparation and the move is the last step before the goal (the party can prevent it). Recorded as `move.at: start | end` and used by the escalation and the card.
- **The start** (finding D3): a small settlement at a spine part that is not the heart: the end or along-route part nearest the move's target, or the hand's base when the move is coming; P3 makes it a village or a small town and step 1 lands there. It replaces today's `start` (heart, heart ruins or end a); a legacy birth keeps its old value.
- **The creature families** (finding D4): `threat.families = {public: [the hand's], secret: [the villain's]}`; P6's occupant and travel-encounter weights read them at P6's turn (a promise, 18d).

**Tests of 18c:** the order; no dead end over 3,000 seeds at every scale × magic × era × content mix; every creature's CR inside the window; the god family absent at short; no humanoid family above short without a power source; the goal joined to the contest in every birth; the hand → verb and verb → target fits held; a true name only on its families; the start never the heart; **the variety report** over 1,000 seeds per scale (each family's share, consecutive repeats, distinct (family, creature, shape, goal) sets) printed in the summary; a legacy birth loads, renders and validates.

---

## Part 18d — the secret as the threat's hidden half, and the new rows' promises

`docs/p1-build-18-rows.md` section 5; `docs/p1-threat-first.md` G6, G8.

- **The four facts** (`secret.facts`): who (public when the visibility is known), what it wants and why, where (the lair), how it is stopped (the weakness).
- **The three stages** (the existing level ranges by tier stay) with the conclusions of section 5 and **three clues per conclusion** (finding D2): one placed by the chain (stage 1 at the hand's base, stage 2 at the move's target or with the stronger role, stage 3 at the goal's piece or the lair), two promised to P5 (a person) and P6 (a site). The third stage's clues reveal the weakness. The ledger holds nine clue promises; the word "act" leaves every secret hook (`secrets.yaml`'s P6 and P7 hooks, the validator's `clue_order`).
- **The twist** (`secrets.yaml#twist`, new meaning; the 20 rows): the 19 kept archetypes with their `cause` rewritten as the threat's hidden truth (no `{the chooser}` placeholder; the villain), and `twist_greater_power` new. Rolled always when the content mix holds mystery, else on a d2; `null` otherwise. The 12 world-lore archetypes retired; `secret_gods_are_prisoners` and `secret_god_erased` become the god family's two forms (an imprisoned god, a forgotten god returning).
- **The keeping** (`secrets.yaml#keeping`: today's twist table renamed; 17 rows): the two rewrites and two additions of section 5; `twist_pc_is_involved` retired from it.
- **The trails** (11): `trail_omen_divination_dead` new; each trail's third element carries the weakness.
- **A hero bound to the threat:** a P9 hook on the chain, in every campaign.
- **The promises of the new rows (G6):** the goal and the move → P4 (the front's steps and the doom: the goal achieved); the weakness → P6 (a hidden object's site), P5 (a rival, a loved one) or P2 (a true name, a god), by its row; the lair → P6 (the final site, with the form); the start → P3 (a village or small town where step 1 lands); the creature families → P6 (occupant and travel weights); the power source → P2 or P6 by kind; the god family → P2 (the god in the pantheon, its church a hand); the nine clues → P5 and P6; the hero bound → P9. Each kind is a script rule where a script can check it, a critic promise otherwise; the secret promises stay counts and ids on every public surface.
- **`avoid_used` (G8):** stated in each new table's header.

**Tests of 18d:** four facts in every birth; three stages with three clues each and the chain-placed clue's piece correct; the twist's rate with and without mystery; no retired row rolled; every new row's hook reaches the ledger; the public ledger unchanged by the secret rolls (the 12a test extended); a legacy birth's secret renders.

---

## Part 18e — the writer, the rubrics and the card

`docs/p1-threat-first.md` "The writer writes, it does not decide", G5, G9, findings 3, 4, 7.

- **The spine sentence:** the script composes it from the story pieces (the hand, the verb, the target, the contest's sides and prize) and stores it (`foundation.spine_sentence`); the card prints it first, the writer starts from it.
- **`P1.premise.md`** reads the chain's records (`#foundation.move`, the dm-only `threat` and `secret`). The writer: makes the question concrete with the prize and the goal as its stakes (W3); writes the signatures, the trope breaks (the world states with their joins), the pitch and the "only here" sentences; in the mirror tells the four facts, the villain (kind and creature, power source, shape, origin, goal and its justification, weakness, lair), the move's truth, the three stages with their conclusions and the chain-placed clue of each (its place a piece id), the twist if rolled, the keeping, the DM pitch. It no longer chooses: the god pin (W1: `dm_only.pinned.god` only when the family is the god or the goal or twist names a patron god, with the relation rolled from a small table: deceived, impersonated, complicit, silent, opposed; `pinned.event` is the move), the clues' places (W2), the concretised object (W5, gone with its verbs), what the villain builds and when it shows (W7). The signature mechanic (W6) is drawn from a small table of shapes (a meter that fills, a favour ledger, a corruption track, a reputation clock, a bargain's debt, a countdown) and the writer fills its numbers inside the shape's bands; list the shapes in the summary for the owner. An `appears` note (W4) carries the hook it restates (`{phase, hook, text}`); the promise binds the hook, the text is advice.
- **A signature's hidden truth** (finding 4): `dm_only.true_rule` only as the medium of a stage's clue, naming the clue it serves; the door refuses one that names none.
- **The institution's P7 hook** (finding 7) becomes "the institution offers or colours quests; it never originates the main thread".
- **The door's fields:** the clues' places and the god pin's piece are piece ids of the chain (the one-way rule of 18a); the threat's names come from the secret stock as today.
- **The P1 rubrics (G5):** `rubric_p1_secret_trail` becomes "the threat's hidden half": are the four facts told, does each stage's conclusion tell the party what to do next, could the party reach each conclusion from any one of its three clues; `rubric_p1_question_concrete` reads the prize and the goal as the stakes; **new `rubric_p1_legible`** (finding 3): "Does the player pitch show a threat with a face and something the party can do in the first session?"; the others stay. No P1 rubric judges a roll.
- **The card:** the spine sentence first; THE SECRET becomes "the threat: rolled, hidden · hidden facts: N of 4 · twist: yes / no · stages: 3 × 3 clues"; under CHECKS a line **"D&D:"** with the completeness ticks (G9): a villain kind and creature, a hand, a goal, a weakness, a lair, a start, the creature families, three stages with three clues each, the trope breaks bend; a missing piece closes the gate (`dnd_incomplete`). The critics' read list (14c's `P1_ROLLS`) adds the move and, for dm-only scopes, the threat and the secret.

**Tests of 18e:** the sentence in every birth and on the card; the prompt renders on the new records with none of the removed decisions; the door refuses a texture piece in a clue's place and a true rule with no clue; the rubrics' texts; the card's D&D line and its gate; a legacy birth's prompt, rubrics and card as before.

---

## Part 18f — the dry walk, the measurements, the birth's faults

- **The dry walk** (item 17) on the chain: the stand-in writer builds from the new records; new wrong turns: a texture piece in a clue's place; a true rule with no clue; a missing lair (the D&D gate).
- **The whole-P1 measurement** brought up to date: zero texture in story slots; the variety report of 18c; **twenty spine sentences** printed from fresh seeds (standard scale, mixed dials) for the owner to read before the test birth.
- **The test birth's pipeline faults** (`docs/reports/p1-test-birth-1.md` section 6): agents read dm-only with the Read tool, never with Bash (the writer's and the critics' prompts say so); an unmerged Workflow's cost reaches the ledger (`design_cost.py record` without a merge); the phenomenon's play floor gets an `appears` form the door accepts; a stale `last_error` no longer rides into the next prompt; the card shows what a correction round changed and the attempt it is; the old tongue's roots are reported correctly at the preroll (or the line says why 0); the critics' reason codes are slugs checked against secret terms before they reach a public report; a `null` reason code is refused at the record.
- **`rerun` clears the validator's last result** (item 17's note).

**The summary of each part:** changed and new files; the suite's count and exit code; for 18a-18d the many-seed figures; for 18c the variety report; for 18e the rendered prompt's length; every fit-list question; anything a principle here did not decide.

After 18f the development tab writes the protocol of the second P1-only test birth.
