# Tags and grouping — analysis 1 (2026-09-29 / 2026-10-02)

*Written by the development (design and review) tab. The owner asked whether "tags + grouping" can remove the inconsistencies between rolled rows. This report holds the audit that raised the question, the analysis, the critic's holes, three faults found in committed code, the system the development tab proposes, and where the work stands. **Nothing here is decided: the owner wants to discuss this report first.** Raw material: `docs/reports/tags-grouping-analysis-1/workflow-result.json` (the six agents' full returns; table row ids, not for the owner's reading) and `…/scripts/` (the audit and simulation helpers; they are scratch scripts, not tests).*

## 1. How the question arose

- **The audit of build items 2 and 7 (2026-09-29).** The arbiter (item 2) works: 2,164 rows with no duplicate id and no dangling reference, symmetric conflicts, and 1,500 seeds of foundation + question + trope break + secret rolled together with no empty pool, no conflicting set and no forbidden row.
- **The data gap.** The whole system holds five conflict pairs. Rows that contradict each other literally carry no conflict. In 3,000 seeds, 104 births (3.5 %) held one of four groups:
  - "going underground is forbidden" with an underground foundation (era underground, the layered spines, the deep lifelines, the surface-and-deep contest): 43;
  - "no lords, guilds rule" with contests about heirs, a throne, lords or nobles, or the marriage lifeline: 43;
  - "rulers are drawn by lot" with two heirs or sibling rulers: 11;
  - "iron is sacred and rare" with the iron-and-coal or famous-steel lifelines: 7.
- **A first pass over P0 found four more:**
  - magic high with the ruin "age of mages";
  - era renaissance with "writing is unknown";
  - era underground with "the moon trades";
  - era underground with "night is safe, day is dangerous".
- **Why they were missed.** Design and build both checked conflicts inside the table at hand; nobody read each identity row against every foundation row. Pairwise reading does not scale: 545 public P1 rows make 139,369 cross-table pairs.
- **The owner's steps.**
  1. Every row carries tags; the script reads tags, never text.
  2. Tags plus grouping: "the tags of earlier rolls become the group headings of the next rolls; a roll drawn inside its own heading is compatible by construction".
  3. The owner wants to settle the tag system first, then apply it item by item, checking every tagged item together with the development tab.

## 2. The analysis (six agents, one workflow, about 1.08 M tokens)

Four independent lenses (structure, coverage, variety, implementation), one synthesis, one adversarial critic. All ran model-free simulations on the committed tables with the real arbiter and foundation roller.

**The answer.** The idea is feasible and is the right model when a group means *every row compatible with everything already rolled*, computed by the arbiter at draw time. That is how the arbiter already works, and where headings exist (lifeline by palette, phenomenon rule by the ruin's families, action by target) no contradiction occurs. Every audited contradiction sits on an edge with no heading, mostly the trope break, the one P1 roll keyed on nothing.

**Three literal readings fail.**

| Reading | Measured result |
|---|---|
| A physical sub-table per heading | rows are copied: 38 of the 56 keyed lifelines fit two or more headings; 13 of 22 headings hold fewer than 5 rows of their own |
| One heading per roll | the trope break clashes with five parents (dials 62 %, main contest 19 %, spine 14 %, second contest 6 %, lifeline 4 %); a heading tree needs about 295 hand-built combinations |
| Every theme link made a hard group | pools shrink 4-7× (trope 27.7 → 6.9 effective rows, institution form 12.6 → 1.8); 4 % of births hit an empty pool; campaigns with the same contest family share a trope break 26 % of the time instead of 7 % |

**The working form, measured.**
- Births with a modelled clash: 4.9-5.7 % (7.2 % on an extended set) → 0 in 3,000 seeds and across all 45 scale × magic × era combinations.
- No empty pool; the trope pool keeps at least 19 of 33 rows (median 30).
- Variety: about 0.1 bit lost of about 153 per birth; trope entropy 5.040 → 5.036 bits (maximum 5.044).
- Soft weights never guarantee consistency: at ×3 on the same links the clash rate stays 5.0 %.

**The synthesis's rules, condensed** (full text in the raw result, `synthesis.design_rules`, R1-R16):
- Three strengths:
  - `claims: {topic: value}`: hard, by exclusion;
  - `requires`: hard, by inclusion, only where the heading is a specific row of a large rotating table;
  - `weight_by`: soft, for theme.
- A closed registry of topics and values; a claim is written only where two rows' sentences contradict literally.
- The dial rows carry claims and are the root.
- Claims become tokens in the arbiter's context, so `arbitrate()` does not change; about 70 lines of new code.
- `families_distinct` is enforced by the roller.
- A graded usage fallback, and pool floors in the tests.
- Completeness is a review (each table against each topic), not a mechanism.

## 3. The critic's holes (they change the proposal)

1. **"0 contradictions" is circular.** It counts only tagged pairs. Untagged literal pairs remain:
   - "war is fought by champions" with war in the content mix: 2.7 % of births;
   - "crossing the border is forbidden" with the foreign envoy, the newcomers or the marriage lifeline: 0.67 %;
   - "going underground is forbidden" with the mining rows: up to 0.6 %.
2. **A second class: promises, not sentences.** Clashes live in rows' hooks, dial effects, scale parameters and forced quotas; at least one in 17.6 % of births:
   - "no lords" against P4's forced state faction: 5.2 %;
   - "magic is nobility" against every magic dial's own regulator: 4.9 %;
   - "war is ritual" against the war mix: 3.0 %;
   - "dungeons are inhabited" against the horror mix: 3.0 %;
   - "the world is young" against the epic scale's 500-year history: 1.9 %.

   Exclusion is the wrong tool here: the trope would yield to the very default it exists to invert. An **overrides** relation is missing.
3. **Presuppositions.** A row names something never rolled: the institution practice "they worship in the departed god's temples" without that ruin (about 2.4 %); "the break's orphans" and "the break's wound" under a break still coming (about 1.9 %). This is what the owner's positive grouping catches; the row must *require* its antecedent.
4. **Two starter claims were wrong.**
   - `sky: none` on the underground era contradicts the owner's ruling that the surface is rare, not gone, and empties P2's moon table in every underground birth.
   - `below_ground: lived` on the palette kind `land_underground` creates false clashes: the forbidden-descent trope falls from 144 to 73 per 3,000 births, not the quoted -20 %.
5. **Registry semantics.** Values of one topic must not clash by default (a magic nobility is also hereditary; printed implies written). Clashes are declared one by one. Theme lists (dragons, craft) must not become hard claims.
6. **Scope.** A people's own order ("the youngest rule") and a land-wide rule ("rulers by lottery") are not about the same thing; a claim needs to say whom it is about (land, people, region, foreign polity).
7. **The prohibition draw.** The six prohibition rows form a small hard group: 3-4 rows in 40 % of taboo draws, and 55 % fall back to used rows. Whether it is the first or the second trope is undecided.
8. **Maintenance.**
   - A per-table review stamp lets a new row pass unreviewed (use a per-row stamp).
   - Tokens share the context with row ids.
   - Family tokens sit outside the closed registry.
   - Later forced rows (P4's quota archetypes) would stop a preroll at runtime with no static test.

## 4. Three faults in committed code (verified by the development tab)

The audit of item 2 had called it correct and missed these:

1. **Secrecy leak through the die size.** `design_arbiter.pick` writes `d{len(pool)}` and the pick's position to the public record. A secret row that removes two rows of a five-row public table shows as a `d3` with no public exclusion.
2. **A rerun's context runs backward.** `design_dice.prior_rolls` skips only the phase being prerolled, so a P1 rerun is filtered by the stale P2-P4 rolls, secret ones included (`design_manifest.stale` only relabels). "What was rolled first stays" is inverted.
3. **Actions and scars are excluded for good.** Their roll headers say `avoid_used: false, row_wait: 3`, but `design_dice.usage` reads the caller's `avoid` argument (default true), not the header. Scars run out by birth 11, with 20.5 % near-repeats.

Also: the arbiter's usage fallback drops every usage exclusion at once (it should drop `used_elsewhere` first and keep the waits), and `families_distinct` is read by no script (about 4 % of standard and epic births draw two governance tropes; build item 10 was to enforce it).

## 5. The system the development tab proposes (for discussion)

Four relations between rows, all read from tags, never from text:

| Relation | What it does | Strength |
|---|---|---|
| **clashes** | a row whose claim contradicts a claim already rolled leaves the pool | hard |
| **requires** | a row is drawn only when what it refers to was rolled (the owner's "roll inside its heading") | hard |
| **overrides** | a rolled trope break rewrites the default it inverts (a dial effect, a quota, a scale parameter) | hard |
| **fits** | a theme link raises a row's weight | soft |

The tables stay; rows gain tags; the new code is small. Completeness comes from the review the owner asked for: every table, item by item, together, reading hooks and dial effects as well as row sentences.

## 6. Open decisions (the owner's)

1. Are the four relations the base of the system?
2. Are the three code faults of §4 fixed first, independently of tags?
3. Does the item-by-item review restart at P0, this time reading hooks and dial effects too?
4. Details the review will have to settle:
   - the registry's semantics (no default clash; scope);
   - whether the underground era claims anything about the sky;
   - where the "below ground" claim sits;
   - whether the prohibition draw is the first or the second trope;
   - whether the trope break stays step 2's first roll.

**Decided by the owner on 2026-10-02:**
1. The four relations (clashes, requires, overrides, fits) are the base of the system.
2. The three code faults of §4, with the graded usage fallback and `families_distinct`, are fixed first, as build item "7a": its own commit, which leaves item 8's uncommitted files untouched. The instruction was handed to the owner for the coding tab the same day.
3. The item-by-item review restarts at P0 and reads hooks and dial effects too. It follows the roll order (P0 dials; spine, palette, ruin source, lifeline, contest, break; trope break, people, institution, phenomenon, question; secret and villain as counts only). Each table comes in small parts, the owner approves row by row, and the approved tags go to `docs/p1-tags.md`, the source of item 7c's instruction.
4. The details of #4 are settled inside the review, each at its own table. Before the review, the development tab brings a one-page proposal of the tag rules (how the four relations are written, the first topic list, no default clash, scope).

## 7. Where the build stands

- **Committed:** build items 1-7 and 6b (`bbef39c`, `a49f32f`, `da18cdb`, `0e7425b`, `5e63f5b`, `431d409`, `9e9ab89`, `b2c8019`, `b7d148b`). 437 tests at `b7d148b`.
- **The coding tab is paused.** Build item 8 (the three signature tables) sits uncommitted in the working tree: `signatures.yaml`, `design_compare.py`, `test_design_tables.py`, `test_identity_tables.py`, and the plan's item-8 note. Its summary reported 450 tests green.
- **Never sent to the coding tab:** the "7b" message (the four literal conflict groups, the cross-table scan rule, the item 8 decisions). It is superseded by whatever the tag system becomes.
- **Planned as a new build item before 8 ("7c: claims"),** not yet agreed in detail.
- **Still open from the P0 pass:** the four tag rules and the P0 tags proposed on 2026-09-29 were never answered; two of those tags are now known to be wrong (§3 #4).
- **Cleanup list additions:** the underground era's calendar note names bells and tides.

## 8. The build list, whole (the plan's 24.3 records only the delivered items)

The owner approved fifteen items on 2026-09-28, one green commit each, P0 and P1 only; 6b was added on 2026-09-29. The owner approves tables at items 3, 4, 5, 6b, 7, 8 and 11; at item 9 the owner sees counts only. The owner raises the session effort to extra for item 12 (it was extra for item 2) and keeps high elsewhere.

| Item | What | State |
|---|---|---|
| 1 | P0's magic dial never takes `none` | committed `bbef39c` |
| 2 | The arbiter: conflicts, requirements, weights, usage waits, `table_until` gone from every phase | committed `a49f32f`; three faults found since (§4) |
| 3 | Foundation tables, group A: palette, spine, ruin source | committed `da18cdb`, review fixes `0e7425b` |
| 4 | Group B: lifeline, contest | committed `5e63f5b` |
| 5 | Group C: the break (target, action, scar, time), the escalation | committed `431d409` |
| 6 | P1 step 1 by script, the foundation sentence, the many-seeds test, legacy births, the tests' own used.json | committed `9e9ab89` |
| 6b | The layout: palette kinds on the spine's parts; the lifeline, the remnant, the break and the contest roles seated | committed `b2c8019` |
| 7 | Trope break (33 rows with the four added prohibitions) and question (33) tables | committed `b7d148b` |
| **7c** | **The claims system: proposed, not agreed (this report)** | **under discussion** |
| 8 | The three signature tables (people, institution, phenomenon) | **written, uncommitted; the owner's decisions pending** |
| 9 | Secret and villain tables, built by the coding tab, counts only to the owner | not started |
| 10 | P1 step 2's rolls | not started |
| 11 | Names: sound families, lexicon, patterns, languages, pools | not started |
| 12 | The promise ledger | not started |
| 13 | The door | not started |
| 14 | The writer, the critics, the card | not started |
| 15 | The attractor cleanup | not started |
| then | The Opus tab's instructions for a test birth that runs P1 alone | not started |

**Item 8, the development tab's recommendations (written, never sent to the coding tab):**
- half-elf and half-orc as two rows: yes;
- the lineage, practice and rule weights: yes;
- "rows that assume the break has happened are not drawn while the break is still coming": yes;
- form words: Cloister and Confederacy yes; Caravan, Fleet or Troupe instead of "Travelling company";
- literal conflicts to add: "writing is unknown" with the institution's charter power and its royal-monopoly practice; "going underground is forbidden" with the people trait "below ground by day";
- no conflict, by the owner's rule (a reading that makes a story is no conflict): illegal maps with the map-making institution; sacred iron with the people who think iron unlucky; no writing with the institution that deciphers old scripts; dragon rulers with dragon hunters; drawn signs as magic with no writing.

**Notes already agreed for the later items (they exist nowhere else):**
- *Item 9:*
  - the "letter" trail conflicts with "writing is unknown";
  - the chooser and the villain's tie are an equivalence (the chooser is the villain exactly when the tie is "caused it");
  - the coding tab builds the conflict lists and reports counts.
- *Item 10:*
  - roll order: trope break → people → institution → phenomenon → question → secret → villain → the signature-mechanic gate;
  - two trope breaks come from different families (`families_distinct` is unread today);
  - the lineage roll reads "lineage homes are inverted" and "humans are a minority" by script, since a promise cannot override a roll;
  - the question is weighted ×3 by the contest's family, and the d2 second-question roll goes;
  - at epic, the villain's pole and the institution's role come from the main contest;
  - P4 stops rolling the villain's visibility, shape and origin and reads P1's;
  - a test proves that no known contradicting pair co-occurs over thousands of seeds.
- *Item 11:*
  - 20-24 sound families, mutated by script;
  - a lexicon of 300-400 roots with neutral glosses;
  - patterns without examples;
  - languages by scale;
  - roots weighted by the foundation;
  - the name pool built at the end of P1's rolls, with 3-5 candidates for each place, institution, signature, month and day name.
- *Item 12:*
  - the ledger record in `design.json`, its four sources and the due phases;
  - open promises on the card;
  - `EXPECTED_UNTIL` goes, and each validator module names its first phase;
  - `docs/tuning-births.md` loses its "`clue_unplaced` before P6 is expected" exception;
  - the legacy births stay untouched;
  - the writer must make concrete what fell from the sky and what was born (the two reworded actions).
- *Item 13:*
  - each signature carries its home's id;
  - the foundation's stamps are untouched;
  - the final set is rechecked for conflicts;
  - every proper noun is pooled;
  - the promises are recorded;
  - no secret in the public file;
  - the legacy births are respected.
- *Item 14:*
  - `P1.premise.md` rewritten;
  - the earlier-campaigns block moves to the critics;
  - new rubrics and a verdict per promise;
  - the new card;
  - `SKILL-design.md`'s P1 line.
- *Item 15:*
  - the signature seeds' examples and the mutation prompts;
  - the history rows (`age_silence` and the like);
  - the three attractor naming patterns;
  - the lexicon glosses;
  - the underground era's calendar note.
- *Every item:* a contradiction found between rows is settled by the script from data, never by the model; `test_regression_births` stays green.
