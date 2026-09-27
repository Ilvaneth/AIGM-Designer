# Dry run 2 — `_test-dry-3` (protocol `docs/dry-run-and-playtest.md` part D, `docs/tuning-births.md` with the stop check)

*Written by the conductor tab (Opus) on 2026-09-27. P1-P8 only: no character, no playtest. Ids, codes, counts and script output only.*

**Outcome in one line:** the first birth with the stop check live ran **P1-P8 to approval** and stopped four times. Three stops were the pipeline's and one was the content's, and each was answered by the development tab through the owner:

| Stop | Phase | Cause | Answer |
|---|---|---|---|
| 1 | P6 | validator false alarm | fixed in `e6eaf74` |
| 2 | P7 | arc template link, and refusals flipping back to merged | fixed in `9cb4002`; P7 rerun whole |
| 3 | P7 | a real bad `refs` id in `chapter_3` | one correction round, no code change |
| 4 | P8 | approval snapshots counted as secret corpus; P8 approved with its render failed | fixed in `09ec2c8`; renders run by hand after approval |

Results:

- **dry-2's P6 regression did not recur:** P6 detailed two sites.
- **NPC count:** 17 public NPCs, inside the band 14-18 for the first time (dry-1: 20, dry-2: 21).
- **Leak scan:** CLEAN.
- **Load budget:** PASS.
- **Uniqueness judge:** `pass`.
- **`design_compare`:** NOT DISTINCT on two shared unique-table rows. This is a pipeline cause (`used.json` is never written by the birth), not the birth.

## 1. Run

| | |
|---|---|
| Command | `designer.py new _test-dry-3 --scale short --party-size 1 --seed DRY-0003 --lang tr` |
| Dials | scale short · tone dark fantasy (rolled) · magic medium (rolled) · era nautical (rolled) · danger standard (rolled) · content mix politics, horror, war (rolled) · party 1 · no wishes |
| Model | Opus 5.5, conductor and agents |
| Code under test | `605576c` at the start; `e6eaf74` from the P6 re-check on; `9cb4002` from the P7 rerun on; `09ec2c8` for the hand renders and the after-P8 block. No prompt, table or production generation code changed under a running phase (see 3.1). |
| Start / end | 2026-09-27 12:16:32 → 20:04:53 (guard disarmed); 7 h 48 min elapsed including four stop waits (≈ 7, 14, 17 and 15 min) |
| Machine time (sum of Workflow durations) | 22.507 s ≈ 375 min ≈ 6.3 h |
| Rolls | 444 public, 31 secret |
| Registry (public projection) | 17 npc, 11 event, 11 node, 9 place, 8 site, 7 seed, 5 god, 5 era, 4 faction, 3 signature, 3 district, 3 settlement, 3 beat, 3 chapter, 2 region, 2 item, 2 socket, 1 break, 1 premise, 1 plane, 1 polity, 1 arc; plus the secret rows `npc_s01`, `item_s01` |
| Detailed at birth | 2 sites (`site_tithemourn`, `site_hushgate`), 6 skeleton |
| Transcript folders | `~/.claude/projects/C--Users-armag-Desktop-Campaign-Designer/c0f7afc8-114d-4073-a311-d8ce77039510/subagents/workflows/<run id>/` |

Workflow runs (persisted scripts under `…/c0f7afc8-…/workflows/scripts/<workflow>-<run id>.js`):

| Phase | Skeleton | Fan-out |
|---|---|---|
| P1 | — | `wf_8e89ebd2-6ff` |
| P2 | — | `wf_f71690ff-bff` |
| P3 | `wf_f3ea4815-90d` | `wf_d7d9af9c-0b0` |
| P4 | `wf_c253a7b2-08a` | `wf_68de90dd-509` |
| P5 | `wf_7a0892e3-8ab` | `wf_e577a82b-841` |
| P6 | `wf_d5c34477-872` | `wf_e0084666-7eb` |
| P7 attempt 1 | `wf_682c6368-3f9` | `wf_e1b4342d-489` |
| P7 attempt 2 | `wf_2263a2bd-43f` | `wf_5b15b1d2-0ba`, then `wf_532981cf-961` (the `chapter_3` correction round) |
| P8 | — | `wf_1b58bc13-512` |

## 2. Per phase (calibration, plan item 19.7)

The token column is **Workflow totalTokens (total context, not output)**, the `subagent_tokens` figure each Workflow reported and passed to `merge --tokens`. Minutes are the card's (sum of the phase's Workflow durations).

| Phase | Status | Min | Agents | Workflow totalTokens (total context, not output) | Roster | Units merged / refused | Critics at the end | Validator | Band |
|---|---|---|---|---|---|---|---|---|---|
| P1 | approved | 19 | 9 | 765.949 | 1 | 11 / 0 | premise fix → pass, c2 fix → pass · phase fix (`rubric_leak` → `signature_cairn_tribunal`, `mutation_states_secret`) · wishes pass | 1E `no_map` (expected) | — |
| P2 | approved | 35 | 11 | 1.160.430 | 1 | 1 container (24 rows) / 0 | `doc_cosmology` fix, fix, pass · phase fix → pass · wishes pass | 1E `no_map` (expected) | god 5 (3-5) ✓ |
| P3 | approved | 38 | 4 + 21 | 547.585 + 1.888.526 = 2.436.111 | 5 | 37 + 13 / 0 | skeleton fix → pass · regions pass · settlements fix → pass ×3 · phase fix → pass · wishes pass | 0E / 0W | polity 1 (1-1) ✓ · region 2 (1-2) ✓ |
| P4 | approved | 56 | 5 + 19 | 835.307 + 1.963.961 = 2.799.268 | 4 | 10 + 6 (5 rows) / 0 | skeleton fix, fix, c2 fix (never passed) · `faction_reach_council` pass → fix · `faction_cairn_tribunal`, `faction_wakehounds` fix → pass · calculus pass · phase fix → fix (`rubric_leak` → P4, `skeleton_board_seed_names_secret_den`) · wishes pass | 0E / 0W | faction 4 (3-4) ✓ |
| P5 | approved | 54 | 4 + 42 | 586.245 + 4.089.615 = 4.675.860 | 10 | 18 + 20 (18 rows) / 0 | skeleton fix → pass · 3 majors with c2, all pass · `npc_ahralf`, `npc_irn`, `npc_hehaald` fix → pass · 5 phase fixes, all pass · phase fix → fix (`rubric_leak` → `npc_hehaald`; `note_consistency` → `npc_skeik`) · wishes pass | 0E / 0W | npc 17 (14-18) ✓ |
| P6 | approved (after stop 1) | 64 | 2 + 15 | 556.680 + 1.491.410 = 2.048.090 | 2 | 13 + 2 / 0 | skeleton pass · `site_tithemourn` pass · `site_hushgate` fix, fix, pass · phase fix → pass · wishes pass | 1E `exit_dangling` (false; 0E after `e6eaf74`) | site 8 (6-8) ✓ |
| P7 attempt 1 | stopped (stop 2), rerun | 52 | 4 + 16 | 657.096 + 1.809.048 = 2.466.144 | 4 → 9 | 28 + 21 / **5 refused** | skeleton fix → pass · `chapter_1` fix → pass · `seedbatch_1` fix, fix, pass · phase fix | 1E `dangling_link` | seed 7 (6-8) ✓ |
| P7 attempt 2 | approved (after stop 3) | 47 | 2 + 14 + 4 | 456.698 + 1.539.504 + 318.252 = 2.314.454 | 4 | 26 + 23 + 1 / 0 | skeleton pass · `chapter_2`, `seedbatch_1` fix → pass · `chapter_3` pass, then its revision pass · phase fix → fix → fix (`rubric_leak` → `arc_1` ×2) · wishes pass | 1E `dangling_ref`, then 0E / 0W | seed 7 (6-8) ✓ |
| P8 | approved (stop 4 after) | 10 | 6 | 575.257 | 1 | 1 (0 rows) / 0 | primer fix → pass · phase pass · wishes pass | 0E / 0W | — |
| **total** | | **375** | **178** | **19.241.563** | | | | | |

The P7 card counts both attempts (99 min, 4.780.598). `design_critique_stats.py _test-dry-3` found 90 critic returns over 28 entities:

- **Verdicts:** first verdict pass 17 / fix 11, final pass 27 / fix 1. Every first `fix` ended as `pass`.
- **Loops used:** 0 ×10, 1 ×11, 2 ×5, 3 ×2.
- **Second critics:** 4 pairs, one disagreement with the first critic's final verdict.
- **Rubrics that failed most:**
  - `rubric_leak` 29/130
  - `rubric_p5_voice_distinct` 4/16
  - `rubric_p3_settlement_fears` 3/9
  - `rubric_skeleton_structure` 3/24
- **Rubrics seen at least 5 times that never failed:** 19.

**Against the earlier births:**

- **dry-1:** 314 min to P9, 17,58 M in a column the root-cause analysis showed was total context too.
- **dry-2:** 12,57 M and 4,2 h to its stop inside P7.
- **dry-3:** P1-P8 at 19,24 M and 6,3 h of machine time, of which 2,47 M and 52 min went to the rerun P7 attempt 1.
- **The estimate:** the plan's `short` estimate (≈ 70 calls, 1-2 h) stays a factor of three or more low.

Approval waits are zero (auto-approve). The four stop waits are not machine time.

## 3. Failures, stops and findings

No traceback, no Workflow that returned `failed` or nothing, no null agent (178/178 done), no blocked read, no failed seed call (`design_seed` 0 failed in every phase). S1 held on every first `begin` after a skeleton merge (entities = roster in P1-P8, both P7 attempts).

### 3.1 The four stops

**Stop 1 — P6, attempt 1, S4 + gate closed (pipeline: validator false alarm).**

```text
phase P6 check → designer: P6 validator — 1 errors, 0 warnings
  error    sites     exit_dangling                ×1   site_hushgate
  (card) error · site_hushgate · `exit_dangling` — room 4 exits to 30, which is not a room
phase P6 approve → exit 1
designer: P6 gate closed — validator: validator errors on 1 entit(ies) of this phase [site_hushgate]. Fix the cause, or approve --force --reason TEXT (a tuning birth never forces: it stops and reports)
```

- **Cause (development tab):** the validator read the `30` inside the parenthesised exit note of room 4 ("2 (… 30 ft)") as a room number. The site was correct.
- **Fix:** validator only, `e6eaf74` ("Validator: a parenthesised note in a room's exits is never an exit (dry-3's first live stop)"). `docs/tuning-births.md` now documents the exception.
- **Answer:** `devam`. `phase P6 check` gave 0E / 0W, the card showed `Kapı: açık ✓`, and `approve` exited 0.

**Stop 2 — P7, attempt 1, S4 + gate closed, and refused units not re-listed (pipeline: two causes).**

```text
phase P7 merge → exit 1
  ✗ node_the_captains_hall: stamped field(s) changed without --revise: chapter
  ✗ node_the_envoys_table: stamped field(s) changed without --revise: chapter
  ✗ node_the_hearing_of_sezyth: stamped field(s) changed without --revise: chapter
  ✗ node_the_quarry_vote: stamped field(s) changed without --revise: chapter
  ✗ node_the_tide_readers_seat: stamped field(s) changed without --revise: chapter
designer: P7 5 unit(s) refused and marked failed — the next `phase P7 begin --json` lists them with the reason: …
phase P7 begin --json → "entities": []   (design.json P7 roster grew from 4 to 9)
phase P7 check → error    refs      dangling_link                ×1   arc_1
  ([[thread_premise]] in design/arc.md does not resolve)
card → **Başarısız:** —
phase P7 approve → exit 1
designer: P7 gate closed — validator: validator errors on 1 entit(ies) of this phase [arc_1]. Fix the cause, or approve --force --reason TEXT (a tuning birth never forces: it stops and reports)
```

- **Causes (development tab):**
  - The arc template proposed the non-existent link `[[thread_premise]]`.
  - The refused node units flipped silently back to `merged` at the next reconcile. That is why `begin` listed nothing, the card said `Başarısız: —`, and the gate named only the validator error.
- **Fix:** `9cb4002` ("dry-3's second stop: a refusal stays failed and goes to its writer; stamps compare ids; the arc template links nothing that cannot exist").
- **Answer:** `yeniden koş P7`, which `docs/tuning-births.md` now defines. The two commands, run separately:
  - `phase P7 rerun --reason "STOP P7 attempt 1: arc template link + refusals flipped to merged; fixed in 9cb4002"` printed "designer: P7 rerun restored the stores of P6's approval", "design_manifest: 0 phase(s) after P7 marked stale" and "P7 reset to attempt 2".
  - `preroll --phase P7`: exit 0. The socket rolls came out different (attempt-derived draws).
- **Then:** the whole P7 loop ran again. P1-P6 stay as measured.

**Stop 3 — P7, attempt 2, S4 + gate closed (content: a bad `refs` id).**

```text
phase P7 check → error    refs      dangling_ref                 ×1   chapter_3
  (card) error · chapter_3 · `dangling_ref` — refs names calculus_act_1, which does not exist
phase P7 approve → exit 1
designer: P7 gate closed — validator: validator errors on 1 entit(ies) of this phase [chapter_3]. Fix the cause, or approve --force --reason TEXT (a tuning birth never forces: it stops and reports)
```

- **Cause:** a real content error. The P4 calculus document's id is `calculus__test_dry_3`, and it is a container, not a registry entity. No code changed.
- **Answer:** `devam` after one correction round:
  - `design_revise.py … round --phase P7 --scope entity --entity chapter_3 --action replace --text "…"` recorded `rev_0001`. It reran `chapter_3` and marked as affected `arc_1`, `beat_the_pardons_price`, `item_the_unlit_candle`, `node_the_cistern_crossing`, `node_the_missing_receipt` and `node_the_oathlight_muster`.
  - `begin` listed only `chapter_3` (render attempt 3).
  - The rewrite (`wf_532981cf-961`) passed its critic.
- **Result:** check 0E / 0W, gate open, approved.

**Stop 4 — after the P8 approval (conductor stop, outside S1-S6; pipeline: approval snapshots read as secret, and a P8 gate hole).**

```text
phase P8 merge →
designer: render_player primer failed (exit 1); the P8 card cannot be approved until it passes
render_player: player-primer.md refused: dm-only sentence (240 chars); dm-only sentence (265 chars); dm-only sentence (138 chars); dm-only sentence (44 chars); dm-only sentence (51 chars); dm-only sentence (111 chars); dm-only sentence (76 chars); … (32 hits, 7 distinct)
phase P8 card → **Kapı:** açık ✓
phase P8 approve → exit 0   (approved)
render_player.py check …/player-primer.md → exit 2: … does not exist (the primer is written by `render_player.py primer` after P8)
design_approval.py leak-check P7.card.md → LEAK: dm-only sentence (75 chars); dm-only sentence (358 chars); dm-only sentence (320 chars); …
design_leak_scan.py -c _test-dry-3 → 12 artifact(s) against 2 secret name(s) and 21312 dm-only sentence(s) — 317 HIT(S)
  ✗ design\entities.json … ✗ design\_approval\P7.card.md   (exit 1)
```

`world.md`, `npcs.md`, `state.md`, `design/index.md`, `design/report.md`, `design/travel-times.md` and `reference/travel-encounters.md` were not rendered either. The conductor halted the after-P8 block before the judge and the disarm and reported.

- **Cause (development tab):** the approval snapshots under the dm-only snapshot folder hold a copy of `design/`, and the leak corpus counted their public sentences as secret. So the primer refusal, the P7 card's LEAK and the 317 hits were all false positives. Separately, a failed P8 render did not close the gate.
- **Fix:** both in `09ec2c8` ("dry-3's P8 stop: approval snapshots are not the secret corpus; a failed P8 render closes the gate").
- **Answer:** `önce düzeltme`. Because P8 was already approved, `merge` does not re-render, so the renders were run **by hand after the approval**, in order, each exiting 0:

| Command | Result |
|---|---|
| `render_player.py facts` | 16 facts |
| `render_player.py news --day 0` | +9 records, `next_id` 19 |
| `render_player.py primer` | 21.474 chars, clean |
| `render_dm.py all` | world 4.452 · npcs 2.949 · index 20.841 · state 1.918 · report 1.902 |
| `map_travel.py travel-times` | 3.971 chars |
| `map_travel.py encounters` | 2 region tables |

Then the after-P8 block ran from the top (section 4).

### 3.2 Findings for the development tab

1. **The rerun reason is handed to the agents as a creative direction and shown on the player's card.**
   - After `phase P7 rerun --reason "…"`, every P7 `begin --json` carried the reason verbatim in `directions`, so the skeleton, chapter and seed writers all received it.
   - The P7 card printed it as "**Yönler (önceki turlardan):** STOP P7 attempt 1: arc template link + refusals flipped to merged; fixed in 9cb4002".
   - The correction round's text joined it as a second direction.
2. **Raw wiki-links on the player's surface.** The P7 card's public one-liners for `seed_the_shuttered_house`, `seed_the_sled_road_chart` and `seed_the_widows_stone` print `[[settlement_greyreach]]`, `[[place_notched_altar]]`, `[[npc_ord]]`, `[[region_tithemarch]]`, `[[npc_hernhre]]`, `[[settlement_vowstill]]`, `[[place_cistern_house]]`, `[[npc_vaizy]]` and `[[site_hallowkeep]]` unresolved. The "Bir yerlinin bildiği" lines below them are clean.
3. **`⚠ Yazılmamış küçük taslak: item ×1`** on the P7 and P8 cards ("onayı durdurmaz"). The development tab ruled it a warning, not S6, since item stubs never close the gate. It is recorded here for the fix after the birth.
4. **The card's `eleştiri` column drops a first `c1:fix`.**
   - P1 `premise__test_dry_3`: the Workflow returned `fix, pass, c2:fix, c2:pass`; the card shows `c1:pass → c1:pass → c2:fix → c2:pass`, and "varlık düzeltme döngüsü 1" against the Workflow's `fix_loops: 2`.
   - P5 `npc_ahralf`: the Workflow returned `fix, pass, c2:pass`; the card shows `c1:pass → c1:pass → c1:pass → c2:pass`.
   - Other entities (`npc_hehaald`, `npc_irn`, `site_hushgate`) show their first `fix` correctly.
5. **`render_player.py news --day 0` is not idempotent.** `phase P8 merge` had already written 9 day-0 records (`next_id 10`). The hand render added 9 more (`next_id 19`), so `news.json` now holds 18 day-0 records.
6. **`design_compare` reads NOT DISTINCT on two shared unique rows** (`naming.yaml: family_sibilant_soft`, `pantheon.yaml: presence_walking`).
   - **Cause (development tab):** the birth never writes the table rows it used to `used.json`, so cross-campaign exclusion does not work.
   - The birth itself is not at fault. The development tab fixes the pipeline after the birth.
7. **Naming.**
   - **A Turkish noun as a god's name:** `god_sivil` "Sivil" is a Turkish common noun, yet passed the door's Turkish-noun blacklist.
   - **Short names:** `god_sta` "Sta", and `npc_ord` "Ord" and `npc_ske` "Ske" are three letters. "Ske" also sits a near-typo from `npc_skeik` "Skeik".
   - **Shared name:** `faction_cairn_tribunal` (P3 skeleton) and `signature_cairn_tribunal` (P1) share the full name "the Cairn Tribunal". The door did not refuse the duplicate; possibly an intended pairing of the signature with its institution.
8. **Placeholder-like ids for secret rows:** `npc_s01` (P4 skeleton) and `item_s01` (P6 skeleton).
9. **Biomes against the era:** the P3 map lists lava field, volcano and ash biomes for most coastal nodes of an `era_nautical` coast. This is a reading note, not checked against the tables.
10. **The skeletons kept re-emitting P1 stubs:**
    - The P6 skeleton re-emitted `site_hushgate`, a P1 stub, as a fragment and roster entry, exactly as dry-2 did with its sites. This time `begin` listed it and its writer ran, so RC-02 holds.
    - The P7 attempt-1 skeleton critic flagged `item_the_unlit_candle` (`p7_owned_stub_unassigned`). This is the likely item behind finding 3.
11. **Critic chains ending at `fix`** (recorded; not a stop):
    - P4: the phase critic, the skeleton (never passed, including its second critic) and `faction_reach_council`.
    - P5: the phase critic.
    - P7: the phase critic, `fix → fix → fix` over the attempt and the correction round.
    - For comparison, dry-2 ended at `fix` in six of seven phases.
12. **Calibration:** P5 is again the widest fan-out, with 42 agents and 4,09 M. P7 is the costliest phase, even measured per attempt.

## 4. Leak scan and load budget

After `09ec2c8` and the hand renders (the after-P8 block run from the top):

| Check | Result |
|---|---|
| `design_check.py -c _test-dry-3` | refs, stamps, secrecy, overlay, map, sites: 0 errors, 0 warnings |
| `render_player.py check design/player-primer.md` | clean (exit 0) |
| `design_approval.py leak-check` on every card | P0-P6, `P7.attempt-1`, P7 and P8: clean |
| `design_leak_scan.py -c _test-dry-3` | `19 artifact(s) against 2 secret name(s) and 2459 dm-only sentence(s) — CLEAN` (exit 0) |
| `load_budget.py -c _test-dry-3` | `6.806 tokens ≈ 23.821 chars over 5 item(s); budget 40.000 — under budget`: chapter 1 3.786, world 1.272, the npcs index 754, state 548, the load pack 445 (no PC sheet or thread; P9 not run) |

Before the fix, the same scan read 317 hits over 12 artifacts (stop 4, false positives), and the load budget measured only 2 items (4.232 tokens) because the DM files had not been rendered.

## 5. P9 — not run

Part D is P1-P8 only: no character, no `design integrate`.

## 6. The playtest — not run

Part D runs no session and no playtest or readability judge.

## 7. Uniqueness

- **`design_compare.py _test-dry-1 _test-dry-3`** (exit 1):

```text
design_compare: _test-dry-1 vs _test-dry-3 — NOT DISTINCT
  names          distinct
  unique_tables  2 shared row(s)
  other_tables   98 shared row(s) of 287 (tables that may repeat)
  map            different
  demographics   different
    row naming.yaml: family_sibilant_soft
    row pantheon.yaml: presence_walking
```

  The cause is the pipeline's: `used.json` is not written at birth (finding 3.2 #6). The owner's instruction was not to stop on it.

- **The uniqueness judge:** one fresh `general-purpose` agent ran on `playtest.py -c _test-dry-1 judge uniqueness --against _test-dry-3` (58.805 tokens, 25 s). Its return is saved at `campaigns/_test-dry-1/playtest/judge-uniqueness.return.json` and recorded with `--record`: "playtest: judge uniqueness recorded — pass; 6 finding(s), 0 not passed".

| Check | Verdict | Gist (paraphrased) |
|---|---|---|
| `same_campaign` | pass | cannot be the same campaign with the names changed: a ring world whose dead return monthly as light, against crimes carved as stone debts, embodied dreams and gods on trial |
| `three_sentences_a` | pass | three premise facts true only of dry-1 |
| `three_sentences_b` | pass | three premise facts true only of dry-3 |
| `question_distinct` | note | the questions differ in kind (honesty vs loyalty to a loved one, against who may forgive on the dead's behalf), but both lean on answering to the dead and read close side by side |
| `signatures_distinct` | note | no signature reskins another, but Wakelight (dry-1) and Nightwake (dry-3) share a name pattern and a "recurring, time-boxed supernatural hour" shape |
| `defaults_absent` | pass | no forbidden default; dry-3's gods on trial are named as a conscious break |

- **`design_critique_stats.py _test-dry-3`:** ran; summary in section 2.
- **Final state:** `designer.py -c _test-dry-3 disarm` printed "designer: guard disarmed". `status` now reads mode birth, guard unarmed, P0-P8 approved (P7 at attempt 2) and P9 pending. The campaign is kept under `campaigns/_test-dry-3/`.
