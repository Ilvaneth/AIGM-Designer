# Dry run 1 — `_test-dry-1` (protocol `docs/dry-run-and-playtest.md`, parts A-C)

*Written by the development tab on 2026-09-26 from the campaign's artifacts (`design/design.json`, the staging folders, `state.md`, `calendar.json`, `playtest/`, `dev-queue.md`) and the two judges it ran, because the conductor tab stopped before writing its report. Ids, codes, counts and script output only.*

**Outcome in one line:** the pipeline ran **end to end for the first time** — P0-P9 approved (P9 = the first live `design integrate`), a character created from the fixed persona, a ten-turn session 1 played against the player agent, `save` and `end` run. The conductor tab stopped inside the end pack's `detail` (`site_bell_barge_wreck`, begun, no fan-out), so the report, part D (`_test-dry-2`) and the judges were left to the development tab. Leak test: **PASS** (after one scanner fix). Load budget: **PASS**. Playtest judge: 11/12, `news_voiced` fails. Readability judge: 6/8, `native_knowledge` and `names_hold` fail.

## 1. Run

| | |
|---|---|
| Command | `designer.py new _test-dry-1 --scale short --party-size 1 --seed DRY-0001 --lang tr` |
| Dials | scale short · tone grimdark · magic low · era renaissance · danger gritty · content mix mystery, politics, war · party 1 at level 1 (band 1-5) · no wishes |
| Model | Opus 5.5, conductor and agents |
| Code under test | `56de330` (slice 1e tooling) |
| Rolls | 437 public, 34 secret |
| Registry | 20 npc, 15 place, 14 event, 11 seed, 11 node, 8 site, 4 god, 4 faction, 3 signature, 3 era, 3 district, 3 settlement, 3 beat, 3 chapter, 2 region, 2 item, 2 socket, 1 break, 1 premise, 1 polity, 1 arc, 1 pc, 1 thread |
| Overlay | 3 sites detailed (`site_hearthfen`, `site_lowmill` at birth; `site_songhallow` by `detail --trigger approach` at load), 5 skeleton |

## 2. Per phase (calibration, plan item 19.7)

| Phase | Status | Minutes | Output tokens | Roster | Writer fragments merged | Critic returns | Phase / skeleton critics |
|---|---|---|---|---|---|---|---|
| P1 | approved | 16 | 521.330 | 1 | 7 | 4 | pass |
| P2 | approved | 29 | 744.302 | 1 | 1 (container, 23 rows) | 4 | pass |
| P3 | approved | 30 | 1.928.456 | 4 | 42 | 10 | pass · skeleton fix → pass |
| P4 | approved | 53 | 3.446.652 | 5 | 13 | 17 | fix · skeleton pass → fix |
| P5 | approved | 51 | 4.884.728 | 10 | 24 | 26 | fix · skeleton fix → pass |
| P6 | approved | 63 | 1.644.256 | 2 | 14 | 6 | pass · skeleton fix → pass |
| P7 | approved | 46 | 2.966.418 | 5 | 32 | 12 | fix · skeleton fix → fix |
| P8 | approved | 9 | 441.455 | 1 | 1 | 3 | pass |
| P9 | approved | 18 | 1.007.343 | 2 | 6 | 5 | pass |
| **total** | | **314 min ≈ 5.2 h** | **17.584.940** | | 140 | 87 | |

Roughly 230 agent calls. Approval waits were zero (auto-approve). The plan's estimate for a `short` birth (item 19.7: ~70 calls, one to two machine hours) is a factor of three low; the numbers above replace it. No merge unit was refused in P1-P9; the phase critic ended at `fix` in P4, P5 and P7 and the P7 skeleton's critics never passed — the card said so, auto-approve approved.

## 3. Failures and gaps

- **The conductor tab stopped** after `end`'s prep: `detail_log` holds `site_bell_barge_wreck` as `begun` (trigger prep, day 2) with no fragment; the guard was left armed in `detail` mode. The development tab marked the entry `abandoned` and disarmed. No report was written; part D never ran.
- **`dev-queue.md`** (the conductor's own findings, all fixed the same day):
  1. `save` says `render_dm.py -c <name> world npcs index`; the CLI took one verb.
  2. `scene --enter` printed the same three day-0 news lines at every scene opening.
  3. The Counting House bundle listed `npc_awoonda` as present although the session-1 pack's day-0 table seats her elsewhere.
  4. `load-pack` flagged `site_songhallow` (T1, 0.1 day) at load; the procedure did not say whether to detail it before the recap; it cost ~10 minutes before session 1 opened.
  5. `character new` step 9 (the global roster mirror) and the name registry `add` wrote outside a `_test-*` campaign.
- **Validator after the session** (`design_check.py`, 16 errors): `refs` — `faction_grainwick_company` links `landmark_the_unrung_tower` (a map-only id the validator did not know), three P9 NPCs without a file (`npc_namound`, `npc_amboun`, `npc_bounwa`: the thread writer created full rows instead of stubs), five `file_unclaimed` rows of `chapter_2.md` (nodes and an item not under `covers:`); `secrecy` — the premise's three clues have `placed_in: null` (no phase wrote the placements back), and `index.md`, `report.md`, `travel-times.md` had no front matter (generated files). All fixed: the map-only ids resolve, generated files are exempt, the P7 chapter prompt claims its rows, the P6 skeleton writes the clue placements back, the P9 thread prompt prefers roster NPCs and stubs new ones.
- `calendar.json` ends with `time: null` while `state.md` says 08:00 — the DM set the date but not the time of day at the last scene.

## 4. Leak scan and load budget

| Check | Result |
|---|---|
| `design_leak_scan.py -c _test-dry-1` | first run: 76 hits, **all in `design/_prompts/**`** — the rendered prompts carry the words "## Secret" by instruction; the scanner no longer treats them as artifacts. Every real artifact (cards, report, world, npcs, index, primer, faces, travel-times, design.json, state, the transcript) clean. |
| `design_approval.py leak-check` on the transcript, the primer, the thread face, world.md, npcs.md | clean |
| `load_budget.py -c _test-dry-1` | 11.604 tokens ≈ 40.615 chars over 7 items (chapter 1: 5.189, the thread: 1.947, world: 1.316, the sheet: 1.115, state: 936, the npcs index: 655, the load pack: 446); budget 40.000 — under |

## 5. P9 — `design integrate`

- Roster `thread_rellick`, `doc_session1`; 6 fragments, 5 critic returns, 18 min, 1.0 M tokens.
- The thread: question `"Seni hiç tanımadan doyuran bir el karşılığında adını bir deftere yazdıysa…"`, antagonist `signature_wardens_of_the_hushbell` (an institution, in the hierarchy), three layers placed (`npc_thilais`, `site_songhallow`, `site_stillhallow`), sites `site_songhallow`, `site_stillhallow`, `site_palelight_reeds`; the mission's verb is active (`bitirmek` — close the line in three ledgers); a `goals.py` record of kind `pc`. Public face rendered to `design/player/thread_rellick.md` (clean).
- The session-1 pack: 7 places for day 0 (`covers:` on the file), the "who is where" table for morning / evening / Wakelight, two opening bangs neither in an inn, the checklist. The pack's table is now what `scene --enter` seats NPCs by on days 0-1.

## 6. The playtest — session 1, ten turns

- PC `Rellick` (human rogue 1, Urchin, `pc_rellick` registered); persona fixed by the protocol. Opening bang A (the Sunk Steps on Wakelight night). Three player rolls, all raw and reported by the agent (Sleight of Hand 1, Insight 16, Sleight of Hand 17), the DM adding the modifiers. Guard: no refusal. `save` and `end` ran: session log, pinned facts, `session_status: closed`, spotlight ledger (`thread_rellick`: 4 scenes), prep with two candidates (`site_bell_barge_wreck`, `site_palelight_reeds`) and a note.
- **Playtest judge** (`playtest/judge-playtest.json`): `fix` — 11 pass, 1 fix: `news_voiced` (none of the five day-0 news lines reached the table through a person, a rumour or a visible change; the session stayed on the bread-debt thread). Passes include `opening_bang`, `describe_before_asking`, `dice_ownership`, `npc_voice` (Thilais's three-item list, Nouma's "Rellum", Waman's rope line), `world_speaks_english`, `no_scaling`, `calendar_advanced`, `no_leak`, `player_agency`, `spotlight`, `pacing`.
- **Readability judge** (`playtest/judge-readability.json`): `fix` — 5 pass, 1 note, 2 fix: `native_knowledge` (the primer printed a god's `church` field with its design note, "(kurulu tapınak; P4 dinî fraksiyon yapabilir)") and `names_hold` (the player map printed `landmark_the_truce_stone`, `waypoint_the_sluice` and four more raw ids). Both fixed: the primer scrubs design notes and names map-only nodes, `render_player check` refuses raw ids and design notes, and the writers' preamble forbids design talk in public fields.
- The scene pack now tells the DM to voice at least one fresh news line per scene and shows a line once per campaign.

## 7. Uniqueness — part D, stopped inside P7

*Written by the conductor tab (Opus) on 2026-09-26. The owner stopped the P7 fan-out by hand, so the comparison itself did not run; this section records the second birth up to that point.*

**Outcome in one line:** `_test-dry-2` (seed `DRY-0002`, code `24f16f5`, resumed from a P1 whose fragments were already on disk) is approved through P6. P7's skeleton is merged, and its fan-out Workflow (`wf_f0705adc-e3f`, 5 entities: `chapter_1`-`chapter_3`, `seedbatch_1`-`seedbatch_2`) was stopped by the owner with nothing merged. P8, `design_compare.py _test-dry-1 _test-dry-2`, the uniqueness judge and `design_critique_stats.py` **did not run**.

### 7.1 Per phase

| Phase | Workflow run | Agents | Seconds | Agent tokens | Units merged / refused | Critics at the end | Card |
|---|---|---|---|---|---|---|---|
| P1 | `wf_bd29c507-ee6` | 11 | 1619 | 1.029.945 | 10 / 0 | premise fix, pass, c2 fix, c2 pass · phase fix (`rubric_leak` ×2, `public_carrion_line_hints_corpse`) · wishes pass | 27 min, output "—" (merged with `--seconds 1600` only); check 1E `no_map` |
| P2 | `wf_cd05b4fd-4f6` | 8 | 1799 | 947.524 | 1 container (21 rows) / 0 | `doc_cosmology` fix, fix, fix (never passed) · phase pass · wishes pass | ⚠ critic not passed; god 4 ✓ |
| P3 skeleton | `wf_cfae2931-81b` | 4 | 1111 | 560.179 | — | skeleton fix → pass | |
| P3 fan-out | `wf_1334afa3-651` | 16 | 849 | 1.581.558 | 28 (27 rows) / 0 | 3 fix → pass · phase pass | 33 min, 2.141.737; check 0E/0W |
| P4 skeleton | `wf_721fb71f-62f` | 5 | 2205 | 889.709 | — | fix, pass, c2 fix | |
| P4 fan-out | `wf_170d7eb8-de1` | 18 | 769 | 1.752.277 | 5 / 0 | 1 fix · phase fix | 50 min, 2.641.986; ⚠ phase and skeleton critics not passed; faction 4 ✓ |
| P5 skeleton | `wf_6ed376ab-a32` | 2 | 1549 | 495.885 | — | pass | |
| P5 fan-out | `wf_a1fc8f1c-97c` | 36 | 1142 | 3.833.443 | 16 (15 rows) / 0 | 3 fix; 4 majors with a second critic · phase fix | 45 min, 4.329.328; **npc 21, band 14-18 ✗**; ⚠ phase critic |
| P6 skeleton | `wf_bd6d3d81-6e6` | 4 | 2017 | 687.583 | 9 / 0 | fix → pass | phase and wishes critic "—" (never ran); site 8 ✓ |
| P6 fan-out | not run | — | — | — | — | — | `begin` listed 0 entities (see 7.2) |
| P7 skeleton | `wf_c0f46a32-4df` | 4 | 2143 | 796.499 | 29 / 0 | fix, fix | 3 beats, 3 chapters, 12 nodes, 8 seeds, 2 sockets, 4 hooks, 3 endings |
| P7 fan-out | `wf_f0705adc-e3f` | 5 started | — | — | nothing merged | — | **stopped by the owner** |
| **total to the stop** | | **108** (+5) | **15.203 s ≈ 4.2 h** | **12.574.602** | | | |

The token figure is the Workflow's subagent total passed to `--tokens`. It is not the same measure as dry-1's column 2, so the two are not directly comparable. Rolls at the stop: 387 public, 27 secret. No merge unit was refused in any phase.

### 7.2 Findings

1. **P6 left the birth with no detailed site (major).** Both roster sites, `site_candlewake_wreck` and `site_stillgate`, had been created as stubs in P1. The P6 skeleton emitted them again as fragments, and the merge marked them `merged` (status merged, stage file under P6's merged folder). `phase P6 begin --json` then listed `entities: []`, and no site writer ran. Both site files still read `# … — skeleton` (`status: skeleton`). `design_check.py` gave 0E/0W because it does not flag an intended-path site left as a skeleton. The card showed the phase and wishes critics as "—" and auto-approve approved it. The conductor did not run a fan-out with zero entities. dry-1 had two sites detailed at birth; dry-2 has none.
2. **The NPC count is over the band again.** It reached 21 against 14-18, as in dry-1 (20). The P5 card shows ✗, and auto-approve passed it.
3. **The names cluster near the owner's banned stems.** The dry-2 NPCs include Cavelor, Celavo, Ceravia, Colevia, Covelan (≈ Corvan), Velocan, Vorelan, Velian, Lovarin, Lorican and Lucaren. That is a Cav-/Cov-/Col-/Cel- and V/L-an/-in family close to the Corv-/Cassiv- blacklist in `naming.yaml`. The blacklist matches full names, so none were refused. This is the likeliest ground a uniqueness judge would fail dry-2 on against dry-1.
4. **Critics ending at `fix` pass silently under auto-approve.** P1 phase, P2 `doc_cosmology` (three `fix` verdicts, never `pass`), P4 phase and skeleton, P5 phase, and the P7 skeleton (fix, fix). This is the same pattern as dry-1's P4/P5/P7.
5. **P1 was resumed with `--seconds` only**, per the owner's instruction, so its card shows the output as "—". The time is recorded; the tokens are not.

### 7.3 State at the stop, and how to resume

- `designer.py -c _test-dry-2 status`: P0-P6 approved; P7 `running`, attempt 1, roster 5, skeleton merged (agent `P7.skeleton.a1`); P8 and P9 pending. The guard is still armed in birth mode.
- The stopped Workflow's partial fragments were **not merged**. A resume re-runs `phase P7 begin --json` and launches `design-fanout` with its output, then merge (with `--tokens`/`--seconds`), check, card and approve. After that: P8, then `design_compare.py _test-dry-1 _test-dry-2`, `playtest.py -c _test-dry-1 judge uniqueness --against _test-dry-2` (plus `--record`) and `design_critique_stats.py _test-dry-2`. This section's uniqueness verdict stays open until then.
