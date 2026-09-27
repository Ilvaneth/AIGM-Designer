# Root-cause analysis 1 — four test births, one pass (2026-09-27)

*The owner asked for the root causes of every failure seen so far, not a fix list: "analyse the tests done so far and find all the root problems". Data: the four births on disk (`_test-tune-1`, `_test-tune-2`, `_test-dry-1`, `_test-dry-2`), their reports, manifests, cards, merged staging, the Opus tab's 53 workflow runs (523 agents) and its transcript, the code and git history. Written by the development tab. Ids, codes, counts, paths only. **No fix has been applied**; section 5 is the plan agreed with the owner.*

**Outcome in one line:** eighteen root causes, of which five explain almost every recurring symptom. The pipeline has **no machine gate between an agent's output and an approved phase**: approval reads no quality signal (RC-01). "Done" means "the registry row is no longer a stub" (RC-02). Stub ownership and scale bands are recorded but read by no script (RC-03, RC-04). The critique loop records verdicts and acts on none of them (RC-05). Auto-approve did not create these faults; it is the channel through which they spread. Critique analysis 1 reduced no critic role and removed no check that could have caught dry-2's P6. The cost figure every report used is total context, not output. Fixes after each report were per symptom; the script fixes held and the prompt fixes came back (RC-11).

## 1. Method and verification

- **Sweep:** seven read-only finders, one lens each: the reports, the manifests and cards, the agent and conductor transcripts, the gates in code, the prompts and tables, cost, and the process. They returned 86 findings.
- **Synthesis:** two independent syntheses, mechanisms-first and actors-first, returned 18 and 15 root causes. One merge reduced these to 18. The two syntheses agreed on every major cause.
- **Adversarial verification, partial:** 11 of the 36 planned verifier runs finished before the session limit. They covered RC-01, 02, 03, 05 and 07 with both a code lens and a data lens, and RC-04 with the code lens. All 11 returned `partly`: the mechanism is real, and the statement needed corrections, which are applied below. None returned `refuted`. The planned completeness pass and final revision did not run.
- **Development-tab checks, after the limit:** direct code reads, git, grep and one Python audit over all 523 agent transcripts, with usage deduplicated by request id (`cost_audit.py`, kept in the session scratchpad). These checks cover every root cause the verifiers did not reach.
- **Completeness check:** the reports lens catalogued 32 findings from the four reports. 28 are explained by a root cause below. The other four (R-1, R-21, R-32 and R-38) were fixed by a script gate the same day and never recurred.

| RC | Title (short) | Sev. | Checked by |
|---|---|---|---|
| 01 | Approval reads no quality signal | blocker | 2 verifiers, partly |
| 02 | Completion = "row is not a stub"; roster intent never asserted | blocker | 2 verifiers, partly |
| 03 | NPC band: writer-created stubs with no allowance or ledger | major | 2 verifiers, partly |
| 04 | `owner_phase` read by no gate; orphan stubs sanctioned | major | code verifier, partly |
| 05 | Critique loop is a log, not a state machine | major | 2 verifiers, partly; one new bug |
| 06 | Agents get a permission list, not their inputs or the fragment contract | major | dev-tab audit |
| 07 | Skeleton agents: the serial bottleneck, trusted without checks | major | 2 verifiers, partly |
| 08 | Graph seeding runs before the skeleton is absorbed, never asserted | major | dev tab: code read |
| 09 | The cost figure is total context, hand-copied; totals never written | major | dev-tab audit: confirmed |
| 10 | The two tabs have no lock; code changed under running births | major | dev tab: git and manifest times |
| 11 | The fix cycle is symptom-shaped | major | dev tab: git counts |
| 12 | Secrecy and distinctness are enforced by wording | major | dev tab: rates confirmed; mechanism inferred |
| 13 | Naming: narrow bank, no within-campaign spread, no candidate log | major | dev tab: partly; cluster found in dry-2 only |
| 14 | `rerun` has no rollback for the disk-is-truth stores | major (latent) | dev tab: code read |
| 15 | Rubric routing drops rows | minor | dev tab: code read |
| 16 | Bootstrap command carries a backslash Windows path through bash | minor | dev-tab audit: confirmed |
| 17 | Validator scope defined by exclusion | minor | dev tab: partly |
| 18 | Read guard matches the protected token anywhere in a command | minor | fired live on this tab |

## 2. The root causes

### Family A — nothing stops a bad phase

**RC-01 · Approval is bookkeeping, not a gate.** `design_manifest.approve` and `approve_phase` refuse on five facts: a failed roster item, a roster item below rank `merged`, a pending skeleton, a missing card, and a card that fails `leak-check`. None of the five reads validator counts, critic verdicts, bands or an empty fan-out. `approve` does not read the phase's status either, so tune-1's P2 was approved while still `running`. Several signals are printed on the card and read by no script: the validator counts, the critic chains and the band tick. Nothing consumes `phase_check`'s exit 1.
- *The P6 fault had no surface at all:* the card shows no site status. The only trace was two `—` cells in the critic column.
- *The plan made a human the quality gate:* 15.2 and `rubrics.yaml` say "never silently accepted", and SKILL-design says "karar oyuncunun". The 2026-09-25 decision removed that human from test births. The protocol tells the conductor to approve and to stop only on a traceback (`docs/tuning-births.md` lines 31 and 35).
- *Evidence:*
  - Seven `⚠ Eleştirmen geçmedi` lines sit on approved cards: dry-1 P4, P5 and P7, and dry-2 P1, P2, P4 and P5. tune-2's P5-P8 cards predate the ⚠ line, which b278320 introduced; eleven approved phases in all ended with a critic chain at `fix`.
  - 22 of 25 generative approvals followed their check within 0-8 seconds.
  - dry-1 approved every phase with 3-13 validator errors.
  - dry-2 P6 was approved in the same chained command in which the conductor logged "MAJOR … no site writer ran" (transcript lines 2178-2179).
- *The one predicate that exists works:* tune-2 P8 was refused for a failed entity and reworked before approval (transcript lines 990-1025).

**RC-02 · One-axis completion model; roster intent is transcribed, never asserted.** The pipeline's only test for "a writer still owes this entity" is `status == 'pending'` on the canonical row (`design_io.is_stub`). `absorb_skeleton` copies the roster from `skeleton.json` without checking it: not the scale's `detailed_at_birth`, not the ordinal coverage, not the fragment list against the folder. `reconcile` ranks any non-stub canonical row as `merged`, and `pending_with_prompts` skips it.
- *The dry-2 loss needs two conditions:* the roster id already exists as a stub, and the skeleton emits a non-pending row for it that the door accepts. `site_candlewake_wreck` and `site_stillgate` were P1 stubs.
- *Why P6 is the exposed phase:* `P6.skeleton.md` is the one skeleton prompt that asks for a non-pending `status: skeleton` on every site row (line 26), one fragment per site (line 32) and a prose file per site (line 29). `_common.md:16` tells any agent given a stub id to fill it. A file-bearing row never meets the door's stub rule, which checks only file-less rows (`registry.py:161-163`).
- *At P4 and P5 the precondition held for 34 of 36 named roster ids across three births, and nothing was lost.* Those skeletons re-emit stubs with `file: null`.
- *P3 reserves site stubs in every birth:* dry-1's and tune-2's P6 skeletons filled P3 stubs as skeleton-only sites and chose new ids for the roster. So the hole was open in every birth that reached P6. In two of them the agent's choice of ids avoided it; tune-1 never reached P6.
- *The skeleton critic could not see it:* it renders the roster as "(none yet)" in every birth. This is a standing gap, not a dry-2 regression.
- *Downstream:* `begin` listed `entities: []`. The workflow runs the phase and wishes critics only when `staged.length > 0`. `design_check` has no rule for an intended-path site left as a skeleton, and the band counts skeletons.
- *One test pins the opposite of the fix:* `test_design_prompts.py:135` asserts "the merged site is not pending".

**RC-04 · `owner_phase` is written by every stub and read by no gate.** Stub rows carry `owner_phase`, `reserved_by` and `created_phase`, and no script compares `owner_phase` with the phase being approved.
- `begin` lists the skeleton's roster, not the stubs the phase owns. `approve` reads only the roster.
- `design_check.is_pending` exempts every pending or file-less row under `--phase`. That exemption dates from 3606c77 (slice 1a); 6ed2f98 extended it to `role_unfilled` and `bad_tier`.
- The door's stub rule covers only prose types (npc, site, settlement, faction, region, chapter, thread). Place, district, polity, seed, event, god and item rows pass file-less with any status.
- *LLMs saw the orphans and reported them as `note`:* dry-2's P4 skeleton critic returned `p4_owned_stub_left_pending_offboard` and its P5 skeleton critic `upstream_overflow_seven_stub_tier_rows_pending`. A `note` has no consumer, because the workflow acts only on `fix`.
- *Scope:* no birth shows an orphan of a rostered id; the orphans are rows left off every roster. dry-2 ends with eight rows owned by already-approved phases still pending, among them seven `npc_` stubs from P3; one carries a clue (`npc_vorelan`).

**RC-05 · The critique loop records verdicts and acts on none of them.**
- *The phase critic runs once.* Its targeted fixes are re-critiqued only by entity critics, and `rubric_lines` hands those critics the entity-scope rubrics. So a phase-scope finding such as `rubric_p5_voice_distinct` is never re-judged after its fix: dry-2 P5 `npc_aurestan` was fixed for voice and re-critiqued without that rubric. Twelve phase-critic runs said `fix`, and each card ends at `fix`.
- *The skeleton gets one fix loop and its second critic none.* P7 skeletons never passed in three births. P4 skeletons passed critic 1 in dry-1 and dry-2, and critic 2 said `fix` in all three births.
- *New bug:* an entity's second re-critique and the re-critique after a phase-critic fix share the label and path `critic1.loop3`. The two sites are `design-fanout.js:108` and `:155`, and the path is built at `:78`. tune-2 P7 `chapter_1` had four returns and three files survived: a `fix` was overwritten by a `pass`. The comment at `:147`, "the record stays distinct", is false whenever the entity used two loops.
- *What reaches disk:* the verdicts reach the manifest through the saved files. The workflow's `failed`, `phase_fixes` and loop numbers never do.
- *Effort:* entity critics run at medium effort even when their writer runs at high.
- *Never observed:* the shared first/second-critic budget never bit in the 11 pairs, and no critic ever returned `rerun`.

**RC-08 · Graph seeding is a side effect that nobody checks.** `phase_merge` runs `design_seed.py` before `absorb_skeleton` moves `skeleton.json` into `merged/`, and `design_seed` reads only `merged/*.json`. A skeleton's graph therefore enters the ledger only if the agent happened to copy it into each fragment. Failed seed calls are printed and ignored, and the merge continues on return code 1. P7 seeded 0 calls in every birth, and `P7.skeleton.md` carries no graph instruction.

**RC-14 · `rerun` has no rollback.** `phase_rerun` resets the manifest phase, renames staging and marks later phases stale. It leaves the canonical registry, the projection, the stamp snapshot, the overlay, the seed ledger, graph, factions and goals, `used.json` and the name registry untouched. A re-emitted row with a changed stamp is then refused by `stamp_check`. No birth has run this path yet. Once a gate refuses a phase, there is no clean way back.

### Family B — counts and names nobody owns

**RC-03 · The NPC band is spent by writers with no allowance.** `named_npcs [14,18]` is checked in one place, the tick on the P5 card.
- *The skeletons stay inside the band:* reservations made by the P1, P3 and P4 skeletons before P5 were 13, 15, 14 and 11 in the four births.
- *The overflow is writer-created stubs:* dry-1 had +7 and dry-2 had +11.
  - The invitation is `P3.region.md:27`, which binds the six social seeds to "roster stubs or minor stubs by id", together with `templates/design/region.md:51`, both from 33f9062.
  - 6ed2f98's `_common.md:18` made every such name a canonical row.
  - The P1 premise writer also creates stubs.
- `preroll_p5` rolls the total count with no registry input. `P5.skeleton.md` says both "fill every stub" and "exactly N".
- Critics saw the overshoot and reported it as `note` only: dry-1 P4, P5 and P6, and dry-2 P5.
- tune-2 stayed in band because its P3 ran before 6ed2f98.
- *Seeds:* only dry-1 overshot. The tune-2 and dry-2 P7 skeletons netted the P3 seed stubs on their own initiative; the prompt is silent on them.
- *This is not plan risk 24.1 #4:* at short scale the role quota fits. The missing piece is a per-writer reservation allowance and a ledger against the band.

**RC-13 · Name clustering.** In dry-2, 10 of 22 person first names end in `-an`. The other births show at most 3 names sharing an ending, and openings are spread in all four births (dry-2: 17 distinct opening pairs in 22 names). The mechanism:
- *Bank:* dry-2's `lampcourt` bank has codas n, r, l, us, ia and an, at a length fixed at three syllables. Its effective single-consonant onsets are c, v and l.
- *No spread rule:* no prompt or door asks for spread within a language. The door checks exact names and the owner's literal stems; `skeleton_critic.md` asks only for "no first-name collision"; `rubric_distinctness` is never rendered (RC-15).
- *Anchoring:* every agent reads `naming.json` and its sample names.
- *No record:* no name candidates are rolled or logged, and `naming.json` records no per-person language. So the choice cannot be replayed, and the claim that almost all persons drew from one bank cannot be checked.
- This is a within-campaign spread problem. It is separate from cross-campaign uniqueness, where errata 24.2 #18 (no stem soft-ban) stays as ruled.

### Family C — cost and observability

**RC-09 · The cost figure is total context, not output.** Every card, report and `design_critique_stats.py` calls one figure "output tokens". It is the Workflow tool's `totalTokens`, copied by hand into `merge --tokens`. The development tab's audit shows that it equals the sum of each agent's peak context.

| Birth | Figure the reports used | Real output | Cache read | Cache write |
|---|---|---|---|---|
| tune-1 | 5.37 M | 0.95 M | 86.6 M | 4.6 M |
| tune-2 | 17.75 M | 2.85 M | 295.9 M | 16.1 M |
| dry-1 | 19.08 M | 2.89 M | 319.2 M | 14.6 M |
| dry-2 | 12.85 M | 2.02 M | 198.6 M | 10.0 M |

- *How the table was built:* the audit sums over every run of each birth, including dry-1's detail runs, which is why dry-1 shows 19.08 M against the report's 17.58 M for P1-P9. The ratio of `totalTokens` to the summed peak context is 0.996-0.997. tune-2 shows 0.851 because its stopped run reported no total.
- *The real driver is cache reads,* that is, turns × context.
- *The critics' share depends on the measure:* 29 % of real output, 36 % with the fix agents, and 46 % of the context measure.
- *What is never recorded:* `design_manifest.tokens()` is never called, so `in`, `cache_read` and `by_model` are zero in all four manifests. `merge.report.json` does not say who filled a stub. Name candidates are never logged.

**RC-06 · Agents get a permission list, not their inputs.**
- The read budget is a list of file names two hops wide, with no delivered bundle and no token cap. dry-2's P7 lists 23-46 files per entity.
- The fragment contract is one sentence in `_common.md`. The schema lives in `docs/schemas/` and the fixtures, which no read list names.
- Fix agents re-render the full writer prompt.
- The audit: median 10-12 tool calls per agent. 57 of 523 agents read the skill's own Python source to learn the row shape. 10 agents referenced another test campaign's files, and nothing fences an agent to its own campaign.
- This is the "read budget" lever that critique analysis 1 §2.6 deferred.

**RC-07 · Skeleton agents are the serial bottleneck and are trusted without checks.** There are five skeleton phases (P3-P7).
- *Share:* skeleton agents take 43-59 % of workflow wall-clock and 23-34 % of real output, all of it serial.
- *Size:* the first skeleton agents make 47-105 API requests each, with peak context up to 431 k. That context is filled by 54-81 serial script and query steps, not by whole-file reads.
- *No shared schema:* each run writes its own Python builder, and each birth puts the site status in a different field. The registry-row status is inconsistent in every birth.
- *Correction applied:* the remit is by plan (9.2, 9.10, 19.2, `sites.yaml` hooks); the skeleton did not grow into it. The skeleton-written sites are template-shaped, about a quarter of a detailed site.
- It is not the cause of the P6 fault (RC-02). Splitting it would be a design change against plan 9.2 and 19.2. The door on `absorb_skeleton` is a repair.

**RC-16 · The bootstrap command is broken on this platform.** `render_cmd` builds `py -X utf8 {SCRIPTS / 'design_prompts.py'}` from a Windows path with backslashes. The agents' Git Bash strips the separators, and the first call fails with `No such file`. This happened to 402 of 523 agents (77 %). Every agent recovers with a relative path, so no return was ever null and no report noticed.

### Family D — secrecy and craft by wording

**RC-12 · Secrecy and distinctness are enforced by wording.** One writer holds an entity's public prose, its dm-only mirror and its notes in one context. The doors refuse exact matches only. `rubric_leak` is the top failing rubric in every birth:

| Birth | tune-1 | tune-2 | dry-1 | dry-2 |
|---|---|---|---|---|
| `rubric_leak` fail rate | 0.16 | 0.30 | 0.24 | 0.19 |

- dry-2's leak codes are all of the hinted kind: `public_carrion_line_hints_corpse` and `meta_design_talk_in_public`. The door took the structural kind, as critique analysis 1 intended.
- The text-level distinctness checks the plan named, a shared opening 4-gram and a stance reason-line check, were never built.
- The mechanism is the analysis's inference; no experiment separated the layers.

**RC-15 · Rubric routing drops rows.** `design_prompts.rubric_lines` (line 164) filters by exact scope, with an `or rows` fallback, and appends only three special rows. The effects:
- dm-only-scope rows reach a critic only in P1, where the fallback fires.
- `rubric_distinctness` and `rubric_load_lightness` reach no critic.
- `wishes_critic.md` has no `{{rubrics}}` placeholder.
- A phase-scope finding is never re-judged after its fix (RC-05).

**RC-17 · Validator scope is defined by exclusion.** `design_check` treats everything under `design/` as bible prose except `design_io.SCRATCH_DIRS` and an explicit `GENERATED_FILES` list. Each new generated file failed until it was added: cards, the primer, the DM index, the report and travel times. The leak scan already moved to a positive list (`VISIBLE_GLOBS`) after dry-1.

**RC-18 · The read guard matches a token, not a read.** `design_read_guard` blocks any conductor command that contains a dm-only or _staging path string. That includes heredoc notes, echo lines and grep patterns. There were five blocks over three births, and two more on this tab on 2026-09-26/27 (a listing and a grep pattern). The mitigation after tune-1 was a protocol sentence asking the model to avoid the token.

### Family E — the development loop itself

**RC-10 · The two tabs have no lock.** Rule 4 of `docs/tuning-births.md` is prose, and the birth marker has no heartbeat.
- 4d48e95 (the door) and 24f16f5 landed at 13:43Z and 13:44Z on 2026-09-26. dry-2 was created at 13:29Z, and its P1 ran until 15:16Z. **dry-2 P1 is a mixed-code measurement:** its writers rendered their prompts before the door existed, and its merge ran through the door. §7 of dry-run-1 says "code 24f16f5" for the whole birth.
- 3f0e3d4 landed inside dry-1's end-pack `detail` run, per the journal lens. The development tab read that transient state as a stop, wrote `abandoned` into the manifest and "the conductor stopped" into the report.

**RC-11 · The fix cycle is symptom-shaped.**
- Each report's findings were closed the same day, from +10 min to +5 h after the report. The fix commits after the four reports touched 36 script or workflow files and more prompt, template and doc files than that.
- The tests are named after the instance (`test_3_1…`, `test_r6…`, a string-presence test on the JS). The tests that pin critic chains test their rendering, not a birth's verdicts.
- None of the class invariants the next birth broke has a test: roster ⇒ stub after the skeleton merge, `owner_phase` ⇒ approve, verdict ⇒ approve, count ⇒ reservations.
- No regression pack re-runs the checks over the archived births.
- The protocol's stop rules are prose, so the conductor filled its silences with guesses.
- *The record supports the other way:* the four report findings closed by a script gate never came back. The classes closed only in prompts or card text did come back: leak wording, stub status, critics at `fix`.
- Every configuration so far has one observation, so model variance and pipeline faults cannot be told apart. The playtest judge's two runs on dry-1 disagree between the report and the file on disk.

## 3. The owner's three questions

**1. Is auto-approve the problem?** It is the channel, not the fault. `approve` has no quality predicate, in test or real births alike. The card's warnings are text for a reader, and the protocol told the conductor to approve anyway. The owner's concern is correct: every faulty phase fed the next one. dry-2's P5 overshoot and P6's skeleton-only sites went into P7's read lists. But restoring `onay` alone would not have caught P6, because the card did not show the fault. The remedy is a machine gate on facts the manifest already holds, identical in both modes, with `--force` plus a recorded reason as the human override (RC-01). Auto-approve then means "approve when the gate is green, stop when it is red".

**2. Did reducing the critic roles cause it?** No critic role was reduced. 4d48e95 added one sentence each to `critic.md` and `phase_critic.md` ("do not re-report the door's classes"). It also added door rules to `registry.py` and a stats script. No critic count, loop cap, effort, rubric or workflow changed, and `skeleton_critic.md` was not touched.
- dry-2's critics ran in comparable numbers. P4 had 8 critics and 4 fixes against dry-1's 13 and 8; P5 had 19 and 5 against 22 and 10. Fewer loops is the door's intended effect.
- dry-2's first-verdict fix rate was 35 % against dry-1's 50 %. Its leak fail rate, 0.19, is the lowest after tune-1.
- The P6 fault is the completion model (RC-02). No critic in any birth could check roster against status, because the skeleton critic always saw the roster as "(none yet)". dry-1's `missing_status_skeleton` findings were about skeleton-only sites, not roster stubs.
- *One caveat:* the change landed during dry-2's P1 (RC-10).

**3. The token cost; enough data; root-cause first?** Yes to root-causing first. The data on disk was enough to reconstruct every dry-2 shape without another birth: the merged fragments, the merge reports, the manifests, the cards, the conductor transcript and the 523 agent transcripts. Naming is the exception, because no candidate list is logged.
- *The cost figure was total context, not output:* dry-1 produced 2.9 M output tokens, and its reported 17.6 M was context (RC-09).
- *Cost is turns × context:*
  - agents discovering their own inputs and row shape (RC-06);
  - serial skeletons of 54-81 steps (RC-07);
  - a first call that fails for 77 % of agents (RC-16);
  - critics and their fixes, a third to a half of the cost depending on the measure.
- *The recurrence record argues for invariants:* script gates held, prompt fixes came back (RC-11). Each invariant gets a class test and a regression pack over the four archived births, with no model tokens, before the next birth.

## 4. Not root-causable, or still open

- The naming choice cannot be replayed: no candidates are logged and no per-person language is recorded (RC-13).
- Agents' reasoning is not on disk; the thinking blocks are redacted in the transcripts.
- The noise of critics and judges cannot be sized, because no birth has been repeated.
- `doc_cosmology` returns `fix` first in all four births, with a different craft rubric each loop.
- The failing calls of dry-1 P3's four seed calls were not printed (RC-08 explains why they were ignored).
- The dry-2 P7 fan-out's partial fragments were not inspected.
- RC-12's mechanism, that one writer holding both layers leaks by paraphrase, is an inference; only its rates are measured.

## 5. The plan agreed with the owner (2026-09-27)

1. **Stop list in the Opus protocol, now.** Only documents change, no code. The conductor stops before approve on a fixed list:
   - a roster item whose writer never ran,
   - a band ✗,
   - a critic that never ran,
   - a new validator error owned by this phase.

   It reports in a fixed format (phase, condition, ids, counts, command output). The owner carries the question to the development tab, which recommends one of three options: continue as-is, end the birth and keep it, or fix here and start a new birth. The owner decides. While a birth waits, the development tab only reads. "Critic ended at fix" is recorded but does not stop a birth: under that rule dry-2 would have stopped at P1, P2, P4, P5 and P7, and under the structural list only at P5 and P6.
2. **The gates in code, one commit each, with class tests.** Those are RC-01, RC-02, RC-04, RC-05, RC-08, RC-14 and RC-16. RC-02's fix replaces the test at `test_design_prompts.py:135`.
3. **A regression pack over the four archived births.** It is model-free, and this tab may write and run it (owner, 2026-09-27). It asserts that the known faults trip the new gates, with dry-2 P6 as the main case.
4. **Counts and names.**
   - *NPC band:* a per-writer reservation allowance and a ledger against the band (RC-03).
   - *Names:* a script-side name generator. It draws from wider banks with varied length and spreads openings and endings within the campaign. It assigns person and god names, or offers two or three candidates. For places it offers root compounds to choose from. It logs every draw. The blacklist, the Turkish-letter ban and the registry check stay (RC-13).
5. **A new test birth in the Opus tab** once steps 2-4 are green. It replaces dry-2 for the door and uniqueness measurements. The development tab hands over the exact instructions.
6. **Cost.** A per-agent ledger from the journals with correct labels (RC-09). Delivered read bundles, the read-budget lever (RC-06). A door on `absorb_skeleton` (RC-07). Then a birth that measures cost, then slice 2.
7. **`_test-dry-2`:** disarmed on 2026-09-27 and not resumed. It is kept as the regression pack's main case.
