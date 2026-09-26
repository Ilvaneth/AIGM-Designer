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

## 7. Uniqueness — not run

Part D (`_test-dry-2`, `design_compare`, the uniqueness judge) waits for the Opus tab.
