# Tuning birth 2 — `_test-tune-2` (the resume test)

*Slice 1c, item 8, birth 2 of `docs/tuning-births.md`. Written by the conductor tab on 2026-09-25. The report holds only ids, codes, counts and verbatim script output; the development tab reads the campaign under `campaigns/_test-tune-2/` itself.*

**Outcome:** the birth **stopped in P5** on a Python traceback, as the protocol requires. P1-P4 ran straight through: every merge unit was accepted and every phase approved. In P5 the fan-out was stopped with TaskStop about 10 minutes in, and the following `phase P5 merge` crashed inside `registry.py` (3.1).

- **Resume test: FAIL.** Step 1 crashed and step 2 (`resumeFromRunId`) was never run.
- **Leak test:** partial. The validator reports 0 secrecy errors and every card P0-P4 passes `leak-check`. No primer exists, because P8 was never reached.

## 1. Run

| | |
|---|---|
| Campaign | `_test-tune-2` |
| Command | `designer.py new _test-tune-2 --scale short --party-size 1 --seed TUNE-0002 --lang tr` |
| Seed | `TUNE-0002` |
| Rolled dials | tone d7→3 `tone_heroic` · magic d4→4 `magic_high` · era d5→2 `era_renaissance` · danger d4→1 `danger_lethal` · content mix d5→4 `mix_horror`, d4→4 `mix_mystery`, d3→1 `mix_exploration` |
| Fixed dials | scale short, party 1, start level 1 (band 1-5), lang tr, no wishes |
| Code under test | `2b58344` (the five birth-1 fix commits `4e3486c`..`2b58344` on top of `784d214`) |
| Model | Opus 5.5 (`claude-opus-5-5`); the conductor and every agent (inherited) |
| Session effort | low (conductor tab) |
| Start / stop | 20:24:23 (`new`) → 23:24:40 (`disarm`), local time |
| Total wall-clock | 3 h 00 min, of which Workflows ≈ 175 min |
| Agents | 68 in the finished runs, plus 29 started in the stopped P5 fan-out (28 results in its journal). 0 null, 0 errors. |
| Subagent tokens | 7.41 M in the finished runs; the stopped run reported no usage |
| Rolls | 277 public, 30 secret |
| Transcript root | `C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\4079d22e-8912-4091-9a35-13053fad09bf\subagents\workflows\<run id>\` |
| Script root | `C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\4079d22e-8912-4091-9a35-13053fad09bf\workflows\scripts\<workflow>-<run id>.js` |

| Phase | Workflow | Run id | Agents | Duration | Tokens | Tool uses |
|---|---|---|---|---|---|---|
| P1 | design-fanout | `wf_8ee637f6-60b` | 9 | 1284 s | 817 017 | 137 |
| P2 | design-fanout | `wf_e57d2dbd-bdd` | 8 | 1818 s | 879 132 | 123 |
| P3 | design-skeleton | `wf_57e89628-94b` | 4 | 1431 s | 608 714 | 116 |
| P3 | design-fanout | `wf_8df79fa9-6e3` | 12 | 762 s | 1 118 481 | 164 |
| P4 | design-skeleton | `wf_59ca3120-918` | 5 | 1909 s | 856 048 | 143 |
| P4 | design-fanout | `wf_0f9322e7-8bd` | 26 | 950 s | 2 466 880 | 365 |
| P5 | design-skeleton | `wf_e3b2be83-f17` | 4 | 1783 s | 663 499 | 118 |
| P5 | design-fanout, **stopped** | `wf_16fad664-7a3` (task `ww4008hmx`) | 29 started / 28 results | ≈ 590 s | not reported | — |

Every merge was passed `--tokens <subagent_tokens> --seconds <duration>` from the Workflow's usage block. For the stopped run the conductor passed `--tokens 0 --seconds 590`.

## 2. Per phase

| Phase | Workflow(s) | Agents | Null | Fix loops | Critic verdicts (skeleton · entities · phase · wishes) | Merge units merged / refused | Validator (grouped `phase PN check`) | Approve | Wall-clock |
|---|---|---|---|---|---|---|---|---|---|
| P0 | — | 0 | — | — | — | — | — | auto | <1 min |
| P1 | fanout | 9 | 0 | 2 | — · premise `fix`→`pass`, c2 `fix`→`pass` · pass · pass | 11 / 0 (11 rows) | 1 E: map `no_map` | ok | 22 min |
| P2 | fanout | 8 | 0 | 2 | — · doc_cosmology `fix`,`fix`,`pass` · pass · pass | 1 container / 0 (23 rows) | 2 E: map `no_map`, stamps `bad_tier` site_moonford | ok | 31 min |
| P3 | skeleton + fanout | 4 + 12 | 0 | 2 | `fix`,`pass` · region_stormfell `fix`→`pass`, settlement_redmouth `pass`, villagebatch_1 `fix`→`pass` · pass · pass | skeleton 34 / 0; fan-out 5 / 0 (6 rows) | 21 E: refs `role_unfilled` ×12 (4 factions: leader, heir, hq empty), `dangling_link` ×5, `dangling_ref` ×3 (settlement_redmouth → npc_stodar, place_hush_press, place_tidewell_exchange), stamps `bad_tier` site_moonford | ok | 37 min |
| P4 | skeleton + fanout | 5 + 26 | 0 | 5 | `fix`,`fix`,`c2:fix` (never `pass`) · cairnmarch, veinreaders and rainwrights `fix`→`pass`, margin_house `pass`, calculus_walking_crown `fix`,`fix`,`pass` · fix → phase fixes on rainwrights and margin_house, both `pass` · pass | skeleton 12 / 0; fan-out 5 / 0 (4 rows; calculus container 0 rows) | 1 E: stamps `bad_tier` site_moonford | ok | 49 min |
| P5 | skeleton + fanout (stopped) | 4 + 29 | 0 | — | `fix`,`pass` (3 critic fixes applied) · — · — · — | skeleton 16 / 0; fan-out: **traceback** | not run | not run | 40 min, stopped |
| P6-P8 | not reached | | | | | | | | |

Second critics:
- **P1:** two critics on the premise, as planned.
- **P4:** the skeleton had 2 critics.
- **P5:** no entry had `critics: 2`; see 5.

Card figures, as recorded by the `--tokens/--seconds` fix:

| Phase | Time | Tokens |
|---|---|---|
| P1 | 21 dk | 817.017 |
| P2 | 30 dk | 879.132 |
| P3 | 37 dk | 1.727.195 |
| P4 | 48 dk | 3.322.928 |

Skeleton counts, as returned:
- **P3:** roster `region_stormfell, settlement_redmouth, villagebatch_1`. 1 region, 1 polity, 1 town, 2 villages, 3 landmarks, 2 districts, 8 anchors, 8 npc / 4 faction / 3 site / 3 seed / 1 event stubs, map 14 nodes / 16 edges, 34 fragments.
- **P4:** roster 4 factions + `calculus_walking_crown`. 10 stance edges, npc stubs 5 new / 1 updated, place stubs 2, 20 seeds, 19 operation steps, 2 antagonists, 0 regional villains.
- **P5:** 16 npcs (3 major, 5 supporting, 8 minor), 2 batches, 15 stubs filled / 1 new (`npc_kadrun`), 26 public / 6 dm-only relations, 18 witness facts, graph 16 nodes / 58 edges, 5 channels.

## 3. Failures

### 3.1 P5 — traceback in `registry.py merge` after the stop (birth ends here)

Command: `designer.py -c _test-tune-2 phase P5 merge --tokens 0 --seconds 590`, run at 23:24:06, about 15 s after TaskStop:

```
Traceback (most recent call last):
  File "C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts\registry.py", line 598, in <module>
    sys.exit(main())
             ~~~~^^
  File "C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts\registry.py", line 578, in main
    return merge(args.campaign, args.phase, args.revise, args.day)
  File "C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts\registry.py", line 321, in merge
    e2, w2 = prose_errors(u["id"], u["frag"], root, u["container"])
             ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts\registry.py", line 222, in prose_errors
    f = root / str(info.get("file", ""))
                   ^^^^^^^^
AttributeError: 'str' object has no attribute 'get'
designer: P5 14 critic return(s) recorded

design_seed: P5: 77 call(s) made, 2 already seeded, 0 failed
designer: P5 partial
MERGE EXIT 0
```

Four things in this output matter:
- `designer.py` exited **0** although `registry.py` crashed.
- `design_seed` still made 77 calls after the failed merge.
- No `registry: merged …` line was printed.
- The failing input was a staged fragment whose prose-info field is a string where `prose_errors` expects a dict. Its id is not visible to the conductor. The two batches are the likely candidates, since they are the only units `begin` shows as `staged`.

### 3.2 Graph seeding failures (merge exit 1, units merged)

**P3 fan-out** (`phase P3 merge`, merge exit 1): `design_seed: P3: 31 call(s) made, 3 already seeded, 9 failed`.

```
✗ campaign_graph.py add-edge: error: source 'settlement_redmouth' not found (no id or name match).
```

The same line appears for `settlement_oathvale`, `settlement_barrowcrag`, `site_candlemere`, `site_drowned_margin`, `site_blackcairn`, `site_ironfell_rows` and `site_moonford`, plus `target 'faction_cairnmarch' not found`.

**P4 fan-out** (`phase P4 merge`, merge exit 1): `design_seed: P4: 40 call(s) made, 0 already seeded, 15 failed`. The same `add-edge` error names:
- as source: `npc_grutak`, `npc_stegor`, `npc_olavene`, `npc_krotan`, `npc_mavelis`, `npc_tarnek`, `npc_selvarin`, `npc_nomeris`
- as target: `faction_veinreaders` ×3, `faction_margin_house`, `faction_rainwrights` ×2, `site_drowned_margin`

Graph nodes for settlements, sites, npcs and factions merged in earlier units are never created before edges reference them.

### 3.3 Merge warnings (no refusal)

```
! doc_cosmology: prose is 25040 bytes, fragment says 25157                    (P2)
! faction_margin_house: stub's reserved stamp(s) archetype changed by its filler   (P4 skeleton)
! faction_veinreaders: dm_only_prose is 4937 bytes, fragment says 4936        (P4 fan-out)
```

### 3.4 No refused units, no blocked reads

No merge unit was refused in P1-P4, and no read was blocked.

## 4. Leak test and resume test

### Leak test — incomplete (P8 not reached)

| Check | Result |
|---|---|
| `design_check.py -c _test-tune-2` | exit 1: refs 0, stamps 1 (`site_moonford: danger_tier must be an integer 1-5`), **secrecy 0**, overlay 0, map 0, sites 0 |
| `render_player.py check` on the primer | exit 2: `render_player: campaigns/_test-tune-2/design/player-primer.md does not exist (the primer is written by render_player.py primer after P8)`. The birth-1 traceback on this path is fixed. |
| `design_approval.py leak-check` | P0, P1, P2, P3 and P4 clean; P5 has no card |

Against birth 1 (43 secrecy errors, a P1 card leak, P5 secret rolls printed as public), every secrecy signal is now clean up to P4. P5's preroll printed "113 public rolls, 16 secret": the npc secrets are now labels only.

### Resume test — FAIL (step 1 crashed; step 2 not run)

| | Count |
|---|---|
| `begin --json` before the fan-out | 10 pending (8 × `P5.npc` + `npcbatch_1`, `npcbatch_2`) |
| Stopped at | 23:23:50, about 10 min after launch (23:14); journal: 29 `started`, 28 `result` |
| `begin --json` after the crashed merge | 10 entries: 8 npcs `pending` (attempt 1, render_attempt 1), `npcbatch_1` and `npcbatch_2` `staged` (attempt 1, **render_attempt 2**) |
| Entities merged from the stopped run | 0 (merge crashed) |
| `resumeFromRunId` | not attempted (traceback, per protocol) |

The finished agents' fragments are on disk; 28 journal results were recorded before the stop. None of them reached the registry, so the "no entity written twice" check could not run. Once the merge is fixed, the same run can be resumed:

```
Workflow({scriptPath: "C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\4079d22e-8912-4091-9a35-13053fad09bf\workflows\scripts\design-fanout-wf_16fad664-7a3.js", resumeFromRunId: "wf_16fad664-7a3"})
```

## 5. Observations

**Fixed since birth 1, confirmed live**
- Per-unit merge: document, batch and calculus containers merged in P2, P3 and P4 with zero refusals.
- Named roster items now enter the fan-out: the P4 factions and the P5 npcs.
- An approved phase stayed approved. No re-approval was needed.
- The skeleton critic runs (P3, P4, P5).
- Cards show time, tokens and a per-entity critic chain.
- The P5 secret rolls are secret.
- Count dice no longer over-draw: P3 drew 35 rolls, against 53 in birth 1.
- `render_player check` on a missing file prints a clean message instead of a traceback.

**P5, the resume path**
- `designer.py phase merge` returns 0 when `registry.py` crashes (3.1).
- A stopped Workflow reports no usage, so `--tokens` has no value to pass. The conductor passed 0.
- After the stop, both batches show `staged` with `render_attempt 2` while the npcs stay at 1.
- The P5 roster carries no entry with `critics: 2` or `effort: high`, though the skeleton returned 3 majors; the plan asks for two critics at high effort on the BBEG and the lieutenants. The P4 skeleton returned `antagonists: 2`, which are probably among them.

**P3 / P4**
- Faction ids and display names diverge: `faction_margin_house` is named "the Tidewell Company" and `faction_cairnmarch` "the Hearthward Council". Both ids are taken from the polity or signature entity rather than from the faction's own name.
- `site_moonford` was created in P2 without a valid `danger_tier`. The `bad_tier` error carried through every phase to the end; no later phase owns or fixes it.
- The P3 settlement writer invented three ids (`npc_stodar`, `place_hush_press`, `place_tidewell_exchange`); the P4 skeleton then created them, which resolved the dangling refs. Order-dependent.
- The four P3 factions have no leader, heir or hq until P4 (`role_unfilled` ×12). The P3 check flags them as errors instead of `pending`.
- The P4 skeleton's critics never returned `pass` (`fix`, `fix`, `c2:fix`), yet the skeleton merged and the phase approved. The card shows no skeleton verdict.
- The P4 calculus container merged 0 registry rows.
- In the begin JSON, each `files` list mixes absolute Windows paths and relative `design/` paths, and lists the same file in both forms.

**Cards**
- "dilek eleştirmeni —" appears on every card, although every Workflow returned `wishes_verdict: pass` (there are no wishes in a test birth).
- The P4 card says "faz eleştirmeni pass". The Workflow's phase critic returned `fix` and then its phase fixes passed; the card shows only the final state.
- The `dil` column is `—` for all P1 and P2 rows, and for `faction_rainwrights` and `faction_veinreaders` in P3.
- The public one-liner of `npc_tarnek` (P1) says "oyuncunun vadisindeki" ("in the player's valley"), which is meta-language in a player-facing line.

**Conductor**
- `preroll --phase P2` was run twice by mistake. The second call was idempotent (status showed 78 public rolls, the expected total), so no re-roll happened.
- The conductor used the protocol's loop exactly; nothing was hand-filtered.

## Resume, second attempt (2026-09-25/26, code `6ed2f98`)

*This section continues the birth from where 3.1 left it. It ran in the same conductor tab after the development tab's commit `6ed2f98` ("a registry crash is a conductor failure, graph nodes before edges, critic record kinds, majors' critics, stubs pass the validator"). The protocol step 1 in `docs/tuning-births.md` now reads `phase P5 merge --seconds <elapsed>`, with no `--tokens`.*

**Outcome in one line:** the birth **reached P8**, and every phase P0-P8 is approved.
- **Resume test: PASS** by the protocol's criteria, with the caveats in R.3.
- **Leak test: FAIL on one validator line.** The cause is a missing front matter on the rendered primer, not a leak; the primer check is clean and all nine cards pass `leak-check` (R.4).

### R.1 Run

| | |
|---|---|
| Start / stop | 23:40:11 (re-merge) → 03:25:24 (`disarm`), 3 h 45 min, of which about 62 min was the account session limit (R.5). |
| Workflow time | ≈ 155 min over 8 runs |
| Agents | 109 (the resume counted 48: 10 replayed from cache and 38 live) |
| Subagent tokens | ≈ 10.34 M |
| Rolls at the end | 400 public, 30 secret |
| Model | Opus 5.5; the conductor at low effort |

| Phase | Workflow | Run id | Agents | Duration | Tokens | Tool uses |
|---|---|---|---|---|---|---|
| P5 | design-fanout, **resumed** | `wf_16fad664-7a3` (task `wh2dy0ij8`) | 48 (10 cached) | 718 s | 2 957 267 | 437 |
| P6 | design-skeleton, **failed** | `wf_da8bbc14-eae` | 1 (error) | 146 s | 197 838 | 35 |
| P6 | design-skeleton | `wf_09916877-7c2` | 4 | 2251 s | 785 222 | 154 |
| P6 | design-fanout | `wf_a8d5b296-86e` | 12 | 1703 s | 1 425 183 | 205 |
| P7 | design-skeleton | `wf_34dacc4c-d4b` | 4 | 1767 s | 685 074 | 125 |
| P7 | design-fanout | `wf_d9198efc-7a9` | 24 | 1358 s | 2 855 677 | 423 |
| P8 | design-fanout | `wf_578e7763-26f` | 8 | 761 s | 755 931 | 101 |
| P8 | design-fanout (refused unit, attempt 2) | `wf_f5ed48b2-33e` | 8 | 618 s | 680 313 | 89 |

Scripts are under `...\workflows\scripts\<workflow>-<run id>.js` and transcripts under `...\subagents\workflows\<run id>\`, with the same roots as section 1.

### R.2 Per phase

| Phase | Agents | Null | Fix loops | Critic verdicts (skeleton · entities · phase · wishes) | Merge units merged / refused | Validator | Approve | Card time / tokens |
|---|---|---|---|---|---|---|---|---|
| P5 | 48 (resume) | 0 | 6 | — · lorevan, grutak, selvarin, tarnek, npcbatch_1 and npcbatch_2 `fix`→`pass`; olavene, drogan, dunkar and kadrun `pass` · fix → 7 phase fixes, 6 `pass`, drogan `fix` · pass | re-merge 18 / 0 (16 rows); after resume 12 / 0 (10 rows) | 0 E, 0 W | ok | 61 dk / 3 620 766 |
| P6 | 1 (failed) + 4 + 12 | 0 | 2 | `fix`,`pass` · saltgut_lock `fix`,`fix`,`pass`; waxfen `pass` · fix → waxfen `pass` · pass | skeleton 10 / 0; fan-out 7 / 0 | 0 E, 0 W | ok | 68 dk / 2 408 243 |
| P7 | 4 + 24 | 0 | 4 | `fix`,`fix` (never `pass`) · chapter_1 `fix`×3 (then phase fix `pass`), chapter_2 `fix`→`pass`, chapter_3 `pass` (then phase fix `fix`), seedbatch_1 `pass`, seedbatch_2 `fix`→`pass` · fix · pass | skeleton 29 / 0; fan-out 24 / 0 (22 rows) | 0 E, 0 W | ok | 52 dk / 3 540 751 |
| P8 | 8 + 8 | 0 | 1 + 1 | — · primer_polity_cairnmarch `fix`→`pass` (both runs) · fix, then fix · pass | run 1: 0 / **1 refused**; run 2: 1 / 0 (container, 0 rows) | 0 E, 0 W | run 1 **refused**; run 2 ok | 23 dk / 1 436 244 |

Skeleton counts, as returned by each skeleton run:
- **P6:** 8 sites (4 minor, 3 standard, 1 major, 0 capstone), roster `site_saltgut_lock, site_waxfen`. 6 skeletons written, 3 over-tier, 3 intended-path, 2 clues on sites, map +3 nodes / +5 edges, graph 8 / 18, 2 item stubs.
- **P7:** 3 beats, 3 chapters, 12 nodes (4 / 3 / 5), 3 planted hooks, 7 seeds, 2 sockets, 3 endings, 32 assignments.
- **Scale bands on the cards:** npc 16 (14-18 ✓) · site 8 (6-8 ✓) · seed 8 (6-8 ✓).

### R.3 Resume test — PASS (with caveats)

| Step | Result |
|---|---|
| `begin --json` before the stop (first session) | 10 pending |
| `phase P5 merge --seconds 590` (no `--tokens`) at 23:40:11 | `registry: merged 18 unit(s) from P5 (16 row(s))` (16 npc stubs filled, `npcbatch_1` and `npcbatch_2` containers with 0 rows), 0 refused, `design_seed: P5: 1 call(s) made, 79 already seeded, 0 failed`, exit 0. The `registry.py` traceback of 3.1 is fixed. |
| `phase P5 begin --json` after it | **0 pending**. All 10 writers had finished before the TaskStop. |
| Path taken | **`resumeFromRunId`**, not a fresh run |
| Resume call 1 (script path + run id, no `args`) | failed in 8 ms: `Error: design-fanout: args.entities is missing; run designer.py phase PN begin --json first` (workflow.js:43) |
| Resume call 2 (script path + run id + the original pre-stop `args`) | ok. Journal went from 29 started / 28 results to 67 / 66; the tool counted 48 agents, 10 replayed from cache and 38 live. |
| Per-id `attempt` in `design.json` after the resume merge | all 10 roster items at `attempt: 1`, status `critiqued`. **No id was re-attempted.** |
| Card count vs skeleton | card `npc: 16 açık, bant 14-18 ✓`; the skeleton returned 16 npcs ✓ |

Caveats:
- **The writers came back from the cache, but their critics and fix agents ran live.** The 38 live agents included 6 entity fix loops and 7 phase fixes. They re-wrote fragments that had already merged at 23:40, and the post-resume merge merged 12 units (10 rows) a second time. The `attempt` counter does not see this, because a fix keeps the attempt. The protocol's criterion "no entity written twice (the registry's attempt per id)" therefore passes, but prose was written twice for the fixed ids.
- **Critic chains double up across stop and resume.** The P5 card shows `npc_lorevan` as `c1:fix → c1:fix → c1:pass → c1:pass` and the phase critic as `fix → pass → fix`.
- **P5 time is over-counted.** `wall_s` is 3681 = 1783 + 590 + 590 + 718: the stopped run's 590 s was added once by the first session's crashed merge and once by this re-merge. Token out is 3 620 766 = 663 499 + 2 957 267 + 0.
- **Resume needs the original args.** A bare `resumeFromRunId` fails; the protocol should say to pass the original `args`.

### R.4 Leak test (after P8) — FAIL on one line

| Check | Result |
|---|---|
| `design_check.py -c _test-tune-2` | exit 1: refs 0, stamps 0, **secrecy 1**, overlay 0, map 0, sites 0. The one line: `✗ [secrecy] design/player-primer.md has no secrecy in its front matter` |
| `render_player.py check` on the primer | `render_player: clean` (exit 0) |
| `design_approval.py leak-check` P0-P8 | all 9 **clean** |
| `designer.py status --json` | P0-P8 `approved` (attempt 1; rosters 0, 1, 1, 3, 5, 10, 2, 5, 1), P9 `pending`. 400 public, 30 secret rolls. |
| `disarm` | `designer: guard disarmed` at 03:25:24 |

The primer was produced by the conductor running `render_player.py -c _test-tune-2 facts` (14 facts), `news` (+7 records, day 0) and `primer` (21 690 chars, clean). Neither the protocol loop nor `designer.py phase P8 approve` does this (R.6).

### R.5 Failures

```
# P6 skeleton, run wf_da8bbc14-eae (Workflow tool)
[P6.skeleton.a1] failed: You've hit your session limit · resets 1am (Europe/Istanbul)

# designer.py -c _test-tune-2 phase P6 merge --tokens 197838 --seconds 146
registry: no staging folder C:\Users\armag\Desktop\Campaign-Designer\campaigns\_test-tune-2\design\_staging\P6
design_seed: no merged fragments for P6
designer: P6 merged                     (exit 0; the phase is "merged" with nothing in it)
```

The same `begin --json` was re-run after the reset (01:00) and succeeded.

```
# designer.py -c _test-tune-2 phase P6 merge --tokens 1425183 --seconds 1703   (exit 1, 7 units merged)
✗ site_progress.py -c: usage: site_progress.py [-h] -c NAME
                        {open,enter,clear,skip,shortcut,rest,note,status} ...
site_progress.py: error: unrecognized arguments: --payoff-room 11 --room-count 18
design_seed: P6: 10 call(s) made, 38 already seeded, 1 failed
```

The following refusal was worked through by the protocol (rerun with the `begin --json`, attempt 2, reason in the prompt), which then merged:

```
# designer.py -c _test-tune-2 phase P8 merge --tokens 755931 --seconds 761   (exit 1)
✗ primer_polity_cairnmarch: public file <P8 staging>/primer_polity_cairnmarch.section.md front matter needs secrecy: public|discoverable (has None)
designer: P8 1 unit(s) refused and marked failed — the next `phase P8 begin --json` lists them with the reason: primer_polity_cairnmarch
registry: merged 0 unit(s) from P8 (0 row(s)); refused 1: primer_polity_cairnmarch

# designer.py -c _test-tune-2 phase P8 approve   (exit 1)
design_manifest: P8 has failed entities (primer_polity_cairnmarch); rerun the pending list or drop them via revise before approving
```

Merge warnings, with no refusal:

```
! seedbatch_1: prose is 58987 bytes, fragment says 49293     (P7)
! seedbatch_2: prose is 58987 bytes, fragment says 58977     (P7)
```

Both batches write the same prose file.

Blocked commands (read guard, false positives on a string, no read):
1. A conductor note that quoted the P8 refusal line, with its staging path, into the scratchpad via heredoc.
2. A `sed` filter in the conductor's own command whose pattern contained the staging folder token.

In both cases the guard reported `the conductor may not read dm-only content (design/_staging/…)`. The protocol's rule 5 names dm-only paths, but staging paths trip the guard in the same way.

### R.6 Observations

**Fixed since the first session, confirmed live**
- The P5 re-merge no longer crashes.
- Graph seeding: P5-P8 had 0 `add-edge` failures, against 9 and 15 in P3/P4.
- `site_moonford`'s `bad_tier` is gone (P6 skeleton).
- The validator was 0 E / 0 W on P5, P6, P7 and P8.
- The wishes critic now shows `pass` on the cards.
- Refused units come back through `begin --json` with `attempt 2` and `last_error` in the prompt, as the protocol now says.

**Player card and primer, the owner as player**
- **P7 card spoils the arc.** It lists the three beats, the three chapter summaries and all 12 node one-liners as public rows, and they state future outcomes: which vote is bought, which deed passes to whom, the day and place the Progress stops. They are `secrecy: public`, so every leak scan passes, but they read as a plot synopsis to the owner.
- **The rendered primer carries a stray front matter block.** The section file's own front matter (`entity`, `type`, `secrecy`, `phase`, `stamped`, `mirror`) appears as visible text under "## Cairnmarch — buradan olan karakterler için", while the primer itself has no front matter, which causes the one validator error.
- **The primer mixes Turkish and English headings.** After the Turkish section come English headings: "The pitch", "The land and who rules it", "The gods as worshipped", "Calendar and festivals", "Money and prices", "Languages and peoples", "Magic and its keepers", "Famous places", "History as taught", "What everyone says is dangerous", "What people are talking about (day 0)", "Questions for your backstory", "The player map". These look like `render_player.py`'s own section titles.
- `item_stillcloak`'s public one-liner names its SRD base item and its attunement. This is fine by the attunement rule; noted only because it is mechanics on the player card.
- **P8 card reads "(bu faz henüz varlık üretmedi)"** although the primer section merged (container, 0 rows). The primer itself, the phase's real output, is not shown on the card.

**Critics**
- Skeleton critics ended at `fix` without a `pass` in P4 (earlier session) and P7 (`fix`,`fix`), yet the skeletons merged and the phases approved.
- The phase critic ended at `fix` in P5, P6, P7 and P8 (P8 `fix → fix`), and every phase approved automatically. Per-entity: `npc_drogan` (P5) and `chapter_3` (P7) end at a `fix` verdict.
- Recurring phase-critic finding `rubric_leak` "public restates mirror / secret content in public writer notes": P5 ×5, P6 ×1, P7 ×4.

**P8 and the protocol**
- `designer.py phase P8 approve` does not run `render_player.py facts / news / primer`, and the protocol loop does not tell the conductor to. The after-P8 block then checks a primer that only exists if the conductor improvises (conductor choice, R.4).
- The P8 roster was a single primer section (`primer_polity_cairnmarch`, one polity) with `files: []` in the begin JSON.

**Accounting**
- A merge after a failed Workflow (P6, session limit) marks the phase `merged` with no staging folder, and adds its 146 s and 197 838 tokens to the phase. The P6 card shows 68 dk.
- In P7 the two seed batches write the same prose file, and their fragments disagree on its size (R.5).

**Conductor**
- The protocol loop was followed exactly. Beyond it, the conductor passed the original args on the second resume call and ran `render_player` before the after-P8 block.
