# A review brief: the AIGM Campaign Designer, phases P0-P2

*Written 2026-10-09 by the design and review tab for an outside review. It is self-contained: answer from this text alone; do not run tools, workflows or agents. The owner asks four questions at the end, and the design tab adds a few of its own.*

## 1. What the system is

AIGM is a Dungeon Master skill for D&D 5e (2014 rules, SRD 5.1) running inside Claude Code. The **Campaign Designer** is its first half: before session 1 it builds a full campaign bible, phase by phase, then the DM skill plays it. The owner is both the person who approves the build and **the only player**, so the bible has a public layer (what the player may know) and a secret layer (the villain, the hidden truths) that must never reach him in a real birth.

A "birth" runs ten phases: **P0** the dials, **P1** the foundation and premise, **P2** the cosmos, P3 the lands, P4 the powers (factions), P5 the people (NPCs), P6 the sites (dungeons), P7 the arc, P8 the primer, P9 the player character's integration. **P0-P2 are rebuilt and finished; P3-P9 still run on the older, looser machinery** and will be rebuilt one by one the same way.

The campaign is *written* in English (every name, file and table) and *played* in Turkish at the table.

## 2. The architecture, in one page

- **The blind conductor.** The main session never writes bible prose and never reads the secret folder (`design/dm-only/`). A read guard (a hook) refuses such reads, including searches from a parent folder and commands wrapped in `bash -c`, `eval`, `xargs` and the like.
- **The script rolls, the model writes.** Every choice a table can make is rolled by Python from YAML tables with seeded dice (a public dice log and a secret one). The model writer gets a **frame**: every row's id, type and rolled fields, already filled. It may only write prose into the fields marked `fill`. It invents no proper noun: every name comes from a **name pool** built from rolled language families (root lexicons, patterns, blacklists including the model's favourite fantasy names and real-world mythology).
- **The door.** Every fragment the writer returns is checked at the merge by a script door: frame fields unchanged, names from the pool, no secret id or secret sentence in public text, no invented capitalised word, and phase rules (for example "one festival per greater god"). A refusal names the field and goes back into the writer's retry prompt.
- **Critics.** Model critics judge the prose against rubrics, giving pass or fix only; a fix loop runs at most twice. They judge craft, never the rolls; only the owner can reroll.
- **The promise ledger.** Every table row carries "hooks": promises to later phases ("the thin place's plane is touched at P2"). The ledger tracks each promise to its due phase and marks it kept or not kept, by a script check or a critic's verdict.
- **Gates and review stops.** `approve` refuses while a gate is open (a missing critic, a validator error, an unjudged promise). After every phase the test-birth conductor stops and sends a review block. The design tab reads it, secret layer included, and answers through the owner (continue, fix one sentence, waive a promise, rerun, end).
- **The card.** Each phase ends with a card the owner reads: the phase's public content in words, with no dice, no row ids and no secret counts.

**How the work is organised.** Separate Claude Code tabs:
- **The design and review tab** is the hub. It decides with the owner, writes the specifications, audits every commit and pushes.
- **The coding tab** builds.
- **The test-birth tab** runs real births on the Opus model.

The owner talks only to the design tab, which directs the others. A coding tab hands over to a fresh one when its context passes 85 %.

## 3. P0 — the dials

Six dials, each rolled or set by the owner:
- scale: short, standard or epic (chapters, level span, entity counts);
- tone: a three-value darkness dial;
- magic: low, medium or high;
- era: including nautical and underground;
- danger;
- the content mix: three of war, horror, politics, mystery and others.

The dials are the root of the tag system: no later roll may contradict them. The P0 card shows them in words.

## 4. P1 — the foundation and the premise

**Step 1, the foundation (script):** six "seeds", each a table:
- **the world's shape**: a palette of landform kinds and a *spine*, one of 30 skeletons such as "a chain of lakes" (a heart, two ends, a key place);
- **the ruin source**: the old fall and its remnant;
- **the lifeline**: what the land lives on;
- **the contest**: two sides fighting over a prize, plus third and fourth parties; two contests at epic;
- **the break**: what just happened (an action on a target, its scars and its time);
- **the escalation** over D&D's four tiers.

**Step 2, the identity (script):**
- signatures: a people, an institution and a phenomenon, with names drawn from candidates;
- the campaign's question, drawn from tension pairs placed on the contest's sides;
- trope breaks that invert a D&D assumption ("wars are fought by champions");
- **the threat chain.**

**The threat chain** (built after the first P1 birth wrote an abstract, non-D&D story):
- a villain family and an SRD creature in the scale's CR window;
- a concrete goal, a weakness and a lair;
- a visible **hand** that makes **the move** (the break) on the way to the goal;
- the contest flaring because of the move;
- the escalation as the villain's plan.

The secret is the threat's hidden half: four facts, three stages with three clues each (one placed by the chain, one promised to P5, one to P6), an optional twist and a mask for a villain hidden among people. The script prints a one-sentence story on the card, for example: "Giants are sealing the strait between the lakes; now the household of the upper lake and the household of the lower lake fight over an inheritance."

**Layers.** Every table is tagged *story*, *stage* or *texture*. A story slot takes only story or stage pieces. Texture never carries a secret of its own and never becomes the doom. The guiding rule: "every campaign is a D&D campaign: a threat with a face, a concrete goal and a weakness, dungeons and monsters tied to the threat, three clues per conclusion, a small start. Strangeness is texture, never the engine."

**The tag system** (nine rules). Each row carries the facts it states literally as claims (`topic: value`), and clashes are declared pair by pair in a closed registry. The relations between rows:
- **clashes**: a later row leaves the pool;
- **requires**: a row that names "the X" needs X;
- **overrides**: a row rewrites a default, such as P4's quota;
- **fits**: weights only.

Two further rules: one target, one owner; and per-row reviewed stamps, so a changed row turns the tests red until the owner reviews it. A single arbiter script applies all of this at every draw.

**Measured over 3,000 seeded births:** 86.4 % held a contradiction or heading miss before the tag system, and none after.

**P1's writer** writes the premise (the question, the signatures' paragraphs, the trope breaks, the player pitch) and the secret mirror, on the frame. Since item 21 the door limits the question to 45 words a contest and the pitch to three sentences of at most 40 words, because the fourth test birth's question ran to 110 words.

## 5. P2 — the cosmos (finished 2026-10-09)

**The method** (the owner's rulings, session S0):
- the same layers and the same tag system;
- the writer decides nothing; every count is rolled;
- P2 joins the promise ledger;
- **P2 holds no secret of its own**, only the threat's (the old design gave every god a secret and hid "the big secret" in P2, which competed with the campaign's real secret);
- **a tag pass is mandatory for every floor** before it is built: claims, clash pairs against all earlier phases, and the clash share measured before and after.

For P2 the share fell from **91.5 % of births with a declared clash, an unapplied override or an unmet requirement, to 0**.

**The roller's order:**
1. the type and the counts (gods, ranks, great gods, touched planes);
2. **the threat's secret seats**: a god threat or a god behind the villain takes a counted god's slot; at epic the villain's home plane;
3. the planes P1 names (the thin place's, the ruin's) and the rest, each with a deviation, a time rate, a way in and a cost;
4. the pantheon (type, presence, domains to a coverage rule, at least one evil god at standard and epic, churches, a connected relation web, where the dead go, the planes' keepers);
5. history (seated story events: the move, the ruin's fall, the villain's origin with a secret true layer, the signature institution's founding; ages and eras by script; one, two or three divergences by scale, all discoverable);
6. magic (source, constraint, visibility, taboos, regulator, services, wild magic);
7. the calendar: a fixed 12 months of 28 days and a 7-day week (the owner found a 45-day month confusing in play); the climate derived from the palette; the moon; festivals, one per greater god plus folk ones; dated days inside the campaign's span; the start date from the move's time.

**Principles kept:**
- **No magic row changes a character's spells by the rules.** Rows only say how the world sees, regulates and charges for magic. Rows that turned spells off (magic only at certain times, every spell costs years) were deleted.
- **Every proper noun comes from a pool**, including planes, festivals, moons, ages and events. Events are named "the <type word> of <referent>": a god's name only for a miracle or a heresy, because "the Vanishing of <god>" told a story about a god that no roll had decided.
- **Secrecy is proven, not hoped.** The *swap test* rolls every corpus birth twice, the second time with another birth's secret records. The public records, the public dice log and even the labels and counts of the secret log must come out identical, at every scale. It caught several real leaks:
  - secret labels that appeared only when a secret fact held;
  - a public plane list chosen by the secret villain, after which the villain's home became a separate secret record;
  - a pinned god standing out by its name's language;
  - a meaningful id such as `plane_nine_hells` for a secret row, after which every secret id is opaque.

  An *order test* proves no later step rewrites an earlier one.
- **Reading generated output.** The design tab reads fresh names and rendered cards, not only test results. It caught a silenced great god who still had a named festival, an "eve" lasting 147 years, a moon named like a village, and "the Sundering" (a Forgotten Realms event and a model favourite).

**Test coverage:**
- about 960 unit tests;
- a shared corpus of 3,000 in-memory P1 births;
- a model-free "dry walk" of P1 and P2 with stand-in writers and deliberate wrong turns;
- a regression pack replaying the gates over archived births.

## 6. History of real (model-driven) test births

| Birth | Run | Outcome |
|---|---|---|
| Tuning births 1-2, dry runs 1-4 (2026-09-25 to 09-28) | the old pipeline | found the structural faults (no machine gate before approval; leaks; cost mismeasured) that led to the gates, the door, the ledger and finally the P1 rebuild |
| P1 birth 1 | | an abstract, non-D&D story; led to the threat-first rebuild |
| P1 birth 2 | | the first on the chain (a marilith); a leaked deceit |
| P1 birth 3 | epic | a whole run lost to the rows' shape; led to the frame |
| P1 birth 4 | epic | the first pipeline-clean P1: one Workflow round of 18 minutes, 7 agents, about 87 k real output tokens, about 1 M context, the door passing every unit first time |

The text still had faults (a long question, sides named "one household and the other"), fixed in item 21. **Next:** the first birth that runs P0-P2 on the new machinery.

## 7. Known open items

- The critics as a whole are unreviewed; they judged their own taste twice before being restricted to the rubrics they are given.
- The arc's skeleton (P7) and "the doom" are not rebuilt.
- Cost: an epic P1 is about 1-2 M tokens of Workflow context. "Read bundles" (RC-06) and a skeleton (RC-07) are planned to cut it. The older pipeline's short birth (P0-P9) took about 5 hours of machine time.
- P3-P8 still let the writer decide much; each will get the same treatment: survey, owner review, tag pass, script roller, frame, door, writer, critics, card, dry walk, swap test.
- The living world (factions acting between sessions) waits until a birth whose every phase the owner accepted.

## 8. The owner's questions

1. **Is the system we built sound?**
2. **Do you see a fault or a gap?**
3. **Is there a place where you would say "doing it this way would have been better"?**
4. **Your general thoughts.**

## 9. Questions the design tab adds

5. **Variety against coherence.** With nearly every choice rolled from tables and the writer only filling prose, do you foresee births that feel combinatorial or samey after a dozen campaigns? Where should the model be given more room, and where less?
6. **The secrecy model.** The owner is the only player and also approves every phase. Is "public versus secret, proven by a swap test" the right model, or is there a simpler, safer one (for example the owner never approving the phases at all)? What leak surfaces might remain: cards, reason codes, counts, timing, the cost ledger?
7. **Does the tag system scale?** Rows declare claims, and clashes are listed pair by pair (14 pairs and 10 topics at P2; P1's tables hold hundreds of rows). With P3-P8 still to come, will the pairwise registry and the "one target, one owner" chart stay manageable, or should it become something else?
8. **D&D completeness.** A DM could run the threat, the clues, the cosmos and the calendar. What does a classic D&D campaign need that P0-P2 do not yet supply, and which belongs in P3-P8 (dungeon design, encounter balance, adventure structure, treasure)?
9. **Cost and speed.** One real phase is a Workflow fan-out of about 7 agents and about 1 M tokens of context. Is per-phase fan-out with critics the right shape for a birth that should finish in hours, or is a cheaper shape available?
10. **The process itself.** Separate tabs, a hub, an audit by an agent plus a clean-checkout suite for every commit, 8-point last reads, sufficiency checks. Is the overhead justified, or would you trim it?
