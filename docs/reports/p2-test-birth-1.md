**P1: clean** (no traceback, door passed, no refused read or permission refusal, no failed Workflow, gate open with every `D&D:` piece ticked, leak check clean, both critic chains ended in `pass`; one promise a critic judged not kept, `prm_ff4037f49a`, was waived on the owner's word with its reason) · **P2: clean** (same list, first attempt, one fix loop ending in `pass`, 12 of 12 promises kept).

# Test birth P2-1 — the report (`_test-p2-1`)

*Conductor: the Opus test-birth tab, protocol `docs/p2-test-birth-1.md` (on `docs/p1-test-birth-4.md` and `docs/tuning-births.md`). Blind: no dm-only file was read, no file edited, no code patched. Every review block went to the design and review tab (Designer-7-Opus, `local_dc4d3bc7-…`) with SendMessage; its answers carried the owner's word.*

## 1. Run

| | |
|---|---|
| Campaign | `_test-p2-1` |
| Seed | `P2T-0001` |
| Command | `designer.py new _test-p2-1 --scale epic --party-size 4 --seed P2T-0001 --lang tr --ask-approval` |
| Code | HEAD `885e4e5` for the whole birth (no commit landed while it ran) |
| Dials | scale epic (10 chapters, levels 1-20), party 4 at level 1; rolled live: tone `tone_shadowed` (d3 → 2), magic `magic_medium` (d3 → 2), era `era_nautical` (d5 → 4), danger `danger_balanced` (d4 → 3), content mix `mix_war`, `mix_exploration`, `mix_mystery`; wishes none; lang tr |
| Model / effort | conductor Opus 5.5 (`claude-opus-5-5`), effort medium; agents inherit the model, prompt effort `high` |
| Start / end | 2026-10-09T18:35:01+03:00 → 19:29:23+03:00 (54 min wall, review waits included) |
| P1 Workflow | `wf_d90dbb6d-694`, transcript dir `C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\b07b6fac-2380-4888-9e55-d02eb8e4e7c2\subagents\workflows\wf_d90dbb6d-694` |
| P2 Workflow | `wf_9e522f0f-4dd`, transcript dir `…\b07b6fac-2380-4888-9e55-d02eb8e4e7c2\subagents\workflows\wf_9e522f0f-4dd` |
| Final status | P0, P1, P2 `approved` (attempt 0 / 1 / 1); P3-P9 pending; public rolls 282, secret rolls 32, tables 26; guard disarmed |

## 2. The phases

### P0

`new` → exit 0, "P0 awaits `onay`". The card showed the dials and the ten chapter bands (1-3, 3-5, 5-7, 7-9, 9-11, 11-12, 12-14, 14-16, 16-18, 18-20). Review stop sent; answer `devam`; `phase P0 approve --onay` → exit 0.

### P1

**Preroll** (exit 0): 60 public rolls, 14 secret (labels only); promises 111 public, 27 secret. Foundation: spine `spine_oasis_ring`; palette desert, coast, volcanic, island; ruin `ruin_dried_source`; contests `contest_old_order_reform`, `contest_open_close_road`; break `time_coming` / `hand_hag_coven` / `target_key_place` / `act_seized`, scars `scar_new_resource`, `scar_lost_knowledge`, `scar_god_changed`; lifeline `life_oasis_springs`; escalation 4 tiers (local, regional, continental, world). Identity: breaks `break_maps_are_illegal`, `break_cities_dangerous` (both `tie_ruin_source`); people `lineage_mixed`, `trait_skin_of_the_land`, `trait_decisions_in_the_open`, `stranger_hostile_for_cause`; institution `form_house`, `practice_hold_the_key_place`, `power_monopoly`, `isign_one_colour`; phenomenon `rule_mirror_doors`, `psign_tremor`, `limit_cold_strengthens`, `user_the_people`; tensions `tension_legacy_freedom`, `tension_flesh_spirit`; mechanic `mech_meter`. Names: people `family_sung`, common `family_northern`, other side `family_rustic`, old `family_airy`; calendar `pattern_month_moon`.

**S1:** `begin --json` listed exactly `premise__test_p2_1`, `"workflow": "design-fanout"` ✓.

**Workflow** `wf_d90dbb6d-694`: completed; 9 agents, 0 errors, 0 empty; staged `premise__test_p2_1`, failed `[]`; 2 fix loops; verdicts `fix, pass, c2:fix, c2:pass`; phase `pass`; wishes `pass`; 1,191 s.

**Critic returns, by rubric id and reason code:**
- critic 1, round 1 — `fix`: `rubric_p1_question_concrete` fix/`main_question_abstract_pair`; `rubric_p1_secret_trail` fix/`conclusions_generic_no_next_step`; pass: `p1_only_true_here`, `p1_differs_from_earlier`, `p1_signatures_pervade`, `p1_forbidden`, `p1_legible`, `leak`, `english_names`.
- critic 1, round 2 — `pass` on all nine.
- critic 2, round 1 — `fix`: `rubric_p1_secret_trail` fix/`clue2_misses_goal`; notes `p1_secret_trail`/`carrier_route_loop`, `p1_question_concrete`/`closer_seat_at_gates`; the rest pass.
- critic 2, round 2 — `pass` on all nine.
- phase critic — `pass`; notes `p1_legible`/`mechanic_threshold_vs_cities_break`, `p1_question_concrete`/`dm_pitch_contradicts_twist`.
- wishes critic — `pass`, no findings.

**Merge** (`--tokens 1078887 --seconds 1191 --run-dir …wf_d90dbb6d-694`, exit 0): 6 critic returns recorded; 6 units merged (`break_cities_dangerous`, `break_maps_are_illegal`, `premise__test_p2_1`, `signature_amberfolk`, `signature_house_halvborg`, `signature_shieldfall`), refused 0; 4 promises added; seed 0 calls, 0 failed.

**Check:** validator 0 errors, 0 warnings; promises a script checks 6 kept, 0 not kept.

**Card** (5,604 chars, leak scan clean): gate open ✓; `D&D:` ✓ villain · ✓ hand · ✓ goal · ✓ weakness · ✓ lair · ✓ start · ✓ families · ✓ stages 3×3 · ✓ breaks bend; secret: threat rolled, hidden facts 4 of 4, twist yes, stages 3 × 3 clues; names all unused (persons 258, gods 45, places 72, regions 36, inns 72, quarters 72, ships 36, epithets 42, ruin sites 120, months 14, special 4, days 9).

**Promises:** due at P1 8 — kept 7, **not kept 1** (`prm_ff4037f49a`, "Maps are forbidden → the break is stated in one sentence in the player pitch and explained through its tied foundation piece…"), waived 0 → S7. After the waiver: kept 7, not kept 0, waived 1. Secret: 30 open, 1 kept, 0 not kept.

**The story sentence:** A coven of hags is about to seize the oasis's water; now the old nobles and the reformers fight over the oasis.

**The question** (two contests, 32 and 23 words):
- Should the oasis's spring-gates and water-price stay House Halvborg's by right of descent, or pass to the reformers' council to be set by open vote, before the hags take the water itself?
- Should the oasis's water feed every body the caravan road brings, or be shut to strangers to keep the oasis's spirit its own?

**The pitch** (three sentences, 24 / 27 / 28 words): A coven of hags, crones who trade in secret bargains, means to seize the oasis's water, and their signs are already in the wells. Meanwhile the old houses and the reformers fight over the oasis: should its spring-gates and water-price stay the houses' by descent, or be set by open vote? It begins in a salt-fishing village on the desert's far shore, where the wells have soured and a fisher's daughter walked into the night sea; find out why.

**Cost (real, from the transcripts):** 9 agents, 134 requests, output 89,470, cache read 13,819,394 (peak context summed 1,082,850); Workflow context 1,078,887; wall 20 min.

### P2

**Preroll** (exit 0): "cosmos — 11 gods (2 greater, 5 lesser, 4 powers; 2 great), 4 touched plane(s), 11 dated events"; 215 public rolls, 18 secret; promises 57 public, 0 secret from P2; name pools people / common / other side 86 person and 15 god names unused each, old 0. Key public rolls: `pantheon_dualist`, `presence_omens`; planes `baseline_lg` (`dev_reachable_by_death`, `rate_stopped`, `way_tide`, `cost_years`), `baseline_lg_ng` (`dev_unchanged`, `rate_fast`, `way_guide`, `cost_tithe`), `baseline_nine_hells` (`dev_renamed`, `rate_stopped`, `way_mirror`, `cost_the_way_back`), `moon` (`dev_is_this_world`, `rate_stopped`, `way_guide`, `cost_oath`); `afterlife_one_land`; `godsecret_was_mortal` on god 1; 11 events + 3 deep; 6 ages (`age_founding`, `ruin_dried_source`, `age_the_war_of`, `age_of_thing`, `age_reckoning`, `age_now_named_for_fear`); magic `source_the_land`, `constraint_caste`, `visibility_loud`, `taboo_none`, `regulator_signature_institution` (loose), `wild_overflow`; calendar 12 × 28, 7-day week, `climate_hot_dry`, `moon_is_a_plane`, festivals `fest_harvest`, `fest_tide`, `fest_trial`; start 825-07-12, `anchor_days_before_doom`, 198 days to the next step.

**Epic scale held:** 11 gods (band 9-14 ✓), 2 great (2-4 ✓), 4 touched planes (3-6 ✓), 6 ages (4-6 ✓), 11 events (10-14 ✓). No epic secret home plane appears among the public four; whether the threat's family has one is in the secret record, which the conductor does not read.

**S1:** `begin --json` listed exactly `doc_cosmology`, `"workflow": "design-fanout"` ✓.

**Workflow** `wf_9e522f0f-4dd`: completed; 6 agents, 0 errors, 0 empty; staged `doc_cosmology`, failed `[]`; 1 fix loop; verdicts `fix, pass`; phase `pass`; wishes `pass`; 1,463 s.

**Critic returns:**
- entity critic, round 1 — `fix`: `rubric_p2_dnd_legible` fix/`cleric_patron_gaps`; notes `p2_history_diverges`/`event_year_label_vs_date`, `p2_history_diverges`/`deep_event_elaboration`; pass: `p2_gods_carry_question`, `p2_history_diverges`, `p2_calendar_felt`, `leak`, `english_names`.
- entity critic, round 2 — `pass` on all; note `p2_dnd_legible`/`start_rains_offset`.
- phase critic — `pass`; notes `p2_calendar_felt`/`hot_months_close`, `p2_dnd_legible`/`start_rains_offset`, `p2_dnd_legible`/`loud_row_blunts_subtle_spell`, `p2_dnd_legible`/`event_year_cell_vs_date` (on `event_1`), `p2_dnd_legible`/`outside_power_cleric_ambiguous`.
- wishes critic — `pass`, no findings.

`rubric_p2_dnd_legible` judged (it drove the one fix loop) ✓.

**Merge** (`--tokens 892079 --seconds 1463 --run-dir …wf_9e522f0f-4dd`, exit 0): 4 critic returns recorded; 1 unit merged (`doc_cosmology`, container of 35 rows: 11 `god_`, 4 `plane_`, 6 `era_`, 11 `event_`, 3 `event_deep_`), refused 0; no door refusal; seed 1 call, 0 already seeded, 0 failed.

**Check:** validator 0 errors, 0 warnings; promises a script checks 11 kept, 0 not kept.

**Card** (5,642 chars, leak scan clean): gate open ✓; band "god: 11 public, band 9-14 ✓"; names: common 11 used / 101 unused, people 0 / 101, other side 0 / 101, old 0 / 0. Promises due at P2: 12 — kept 12, not kept 0, waived 0; open P3 42 · P4 24 · P5 15 · P6 23 · P7 16 · P8 20 · P9 3 · validator 2 · play 1; secret 27 open, 4 kept, 0 not kept. P1's promises due at P2 were all kept (P1's card listed 8 open for P2; all 12 due here kept).

**Cost (real):** 6 agents, 92 requests, output 138,010, cache read 12,149,856 (peak context summed 894,658); Workflow context 892,079; wall 24 min.

### Per-phase table

| Phase | Workflow | Agents | Null | Fix loops | Critic verdicts | Phase / wishes | Merged / refused | Validator | Wall |
|---|---|---|---|---|---|---|---|---|---|
| P1 | `wf_d90dbb6d-694` | 9 | 0 | 2 (c1 1, c2 1) | fix, pass, c2:fix, c2:pass | pass / pass | 6 / 0 | 0 / 0 | 20 min |
| P2 | `wf_9e522f0f-4dd` | 6 | 0 | 1 | fix, pass | pass / pass | 1 unit (35 rows) / 0 | 0 / 0 | 24 min |

## 3. Failures

None: no traceback, no door refusal, no refused read, no permission refusal, no failed or empty Workflow. Every command exited 0.

## 4. The review rounds

1. **P0** — block with the rolls and the card → `devam` → approved.
2. **P1, attempt 1, S7** (gate open; `prm_ff4037f49a` judged not kept) → owner's word: `vazgeç prm_ff4037f49a: the pitch stays three short sentences (build 21d); the break is stated in its own section of the premise`. Run: `arm --mode birth`; `designer.py -c _test-p2-1 promise waive prm_ff4037f49a "the pitch stays three short sentences (build 21d); the break is stated in its own section of the premise" --onay` → "promise prm_ff4037f49a waived (due P1); recorded in the ledger and the revision log", exit 0; `phase P1 card` (5,390 chars, leak scan clean), `phase P1 report`. The card's diff was the PROMISES line only (and the `produced` stamp), gate open, so per the answer no second block: `phase P1 approve --onay` → exit 0.
3. **P2, attempt 1, open** → `devam` → `arm --mode birth`, `phase P2 approve --onay` → exit 0, then the end block.

## 5. Leak tests

- `design_approval.py -c _test-p2-1 leak-check campaigns/_test-p2-1/design/_approval/P1.card.md` → `design_approval: clean`, exit 0.
- `design_approval.py -c _test-p2-1 leak-check campaigns/_test-p2-1/design/_approval/P2.card.md` → `design_approval: clean`, exit 0.
- Both cards' own write-time leak scans: clean.

## 6. Observations

- P1: the pitch names neither trope break, but only `break_maps_are_illegal`'s promise was judged not kept; `break_cities_dangerous` (same promise shape, presumably) was not flagged — worth checking whether the second break has the same promise row.
- P1: the phase critic noted `dm_pitch_contradicts_twist` and `mechanic_threshold_vs_cities_break` and still passed; the conductor cannot judge either (both touch the secret layer).
- P1: the begin JSON's `workflow` key sits at the top level, not per entity; S1 was read from the top-level key.
- P2: the begin JSON's entity `files` list carries a dm-only path; it went to the Workflow as args only, never into a Bash command.
- P2: god epithets repeat a root: "Mother of the Monk" (Alfdis) and "Lady of the Monk" (Gudolf); "Lady" also sits on male-sounding names (Gudolf, Varnrid) — a reading for the design tab, not a fault the door checks.
- P2: all 11 gods were drawn from the common language's pool; people and other-side god pools stayed unused.
- P2: Heanar's keeper is a god (Varnrid; roll `plane.2.keeper fixed → 11`), the other three keepers are creatures (Planetar, Rakshasa, Deva).
- P2: the dates check: the ruin 373 years ago (123 after the founding at 277) sits at year 452 = the Fall of Thewein, start year 825 ✓.
- `--tokens` was given the Workflow's `subagent_tokens` (total context), as earlier births did; the real output comes from `--run-dir`.
- Cost per role was not broken out on the cards or reports (only totals per run); `design_cost.py` holds the per-role split if needed.
- The design tab's session appeared to `ListAgents` as "Designer-7-Opus [5739c9]", not by its `local_dc4d3bc7-…` id; messages were sent to the id and delivered.
