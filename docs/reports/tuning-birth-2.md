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
