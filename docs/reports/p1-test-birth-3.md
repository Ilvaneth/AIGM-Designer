# Test birth P1-3 — report (`_test-p1-3`)

*Conductor: the Opus test-birth tab, 2026-10-07, under `docs/p1-test-birth-3.md`. Decisions came from the design and review tab (session `local_39bf34e9-…`) carrying the owner's word. Nothing in the skill, the tables or the prompts was edited; nothing was committed or pushed. The conductor never read dm-only.*

## 1. Run

- **Campaign:** `_test-p1-3` · **seed:** `P1T-0003` · **scale:** epic · party 1, level 1 → band 1-20 · 10 chapters · `--lang tr` · `--ask-approval` (auto_approve false).
- **Dials (rolled live):** tone `tone_shadowed` · magic `magic_high` · era `era_medieval` · danger `danger_gritty` · content mix `mix_exploration`, `mix_war`, `mix_politics` · wishes none.
- **Model:** Opus 5.5 (`claude-opus-5-5`) for the conductor and every agent (inherited); premise effort `high` (from the prompt's front matter), 2 critics.
- **Times (UTC):** `new` 11:23:56 · P0 approved ~11:25 · preroll P1 11:25:47 · run 1 merged 11:49:32 · run 2 merged 12:04:08 · card 12:04:19 · P1 approved 12:14:05 (after the review stop).
- **Workflow runs** (both `design-fanout`, both completed):
  - `wf_ae88e5d7-edc`: 9 agents, 1,401 s; transcript `C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\2e920d33-3c71-468b-bbbc-ff971fcf128b\subagents\workflows\wf_ae88e5d7-edc`
  - `wf_8a46f676-22d`: 8 agents, 850 s; transcript `…\subagents\workflows\wf_8a46f676-22d` (same parent)

## 2. Phases

### P0

`new` printed the seven roll lines above; the card showed the dials, the rolls and the ten-chapter arc skeleton (act 1: chapters 1-4, levels 1-9; act 2: 5-7, levels 9-14; act 3: 8-10, levels 14-20). REVIEW block sent; answer **`devam`**; `phase P0 approve --onay` → exit 0.

### P1

**Preroll:** 61 public rolls, 15 secret (labels only); escalation 4 steps (`tier_local` → `tier_regional` → `tier_continental` → `tier_world`, forced); two contests (`contest_one_pasture`, `contest_casters_casterless`); hand `hand_werewolves`, move state `move_done`; break `time_unfolding` / `target_heart` / `act_cursed`; scars `scar_unreachable_region`, `scar_sky_changed`, `scar_new_people`; breaks `break_underground_forbidden`, `break_rule_by_lottery` (both `tie_break`); people `lineage_lizardfolk`; institution `form_house` / `practice_keep_the_old_works` / `power_monopoly`; phenomenon `rule_shared_wounds` / `limit_iron_cuts` / `user_the_people`; tensions `tension_survival_honour`, `tension_sacrifice_worth`; mechanic `mech_meter`; naming families `family_guttural`, `family_lake_folk`, `family_courtly`, old `family_old_isle`. Promises 114 public, 29 secret.

**S1:** `begin --json` listed exactly `premise__test_p1_3`, `"workflow": "design-fanout"`. Pass.

**Story sentence (card, public):**
> A cursed pack is laying a curse on the largest floating island; now the herd-owning highland clans and the lowland villages fight over the land between them.

**Names chosen:** people Coalborn (of Coalborn / Strawfolk / Sandkin / Moonborn), institution House Ilaro, phenomenon the Talon Bloom; premise name "the cursed heart".

**Agents and null returns:** 17 agents over two runs, 0 errors, 0 empty results, 0 null returns.

**Run 1 (`wf_ae88e5d7-edc`), chain:** writer (staged) → critic 1 `fix` → fix → critic 1 `pass` → critic 2 `fix` → fix → critic 2 `pass` → phase critic `pass` → wishes critic `pass`. Workflow result: `fix_loops 2`, verdicts `fix, pass, c2:fix, c2:pass`, `phase_fixes []`. **The merge refused all six units** (section 3).

**Run 2 (`wf_8a46f676-22d`), chain:** writer (staged, attempt 2) → critic 1 `pass` → critic 2 `pass` → phase critic `fix` → fix writer (the phase fix) → critic `pass` → phase critic `pass` → wishes critic `pass`. Workflow result: `fix_loops 0`, verdicts `pass, c2:pass`, `phase_fixes [{premise__test_p1_3, fixed: true, verdict: pass}]`. All six units merged. **The phase critic's fix reached the writer.**

**Critic returns by rubric id** (verdicts other than plain `pass`; every other listed rubric passed):

| Run | Critic | Verdict | Findings |
|---|---|---|---|
| 1 | entity critic 1, round 1 | fix | `rubric_p1_secret_trail` fix/`stage2_clue_reveals_where_not_who_why`; `rubric_p1_signatures_pervade` note/`people_age_vs_curse_age_unstated`; `rubric_english_names` note/`institution_name_tongue_differs_from_language_list` |
| 1 | entity critic 1, round 2 | pass | `rubric_p1_secret_trail` note/`known_villain_absent_from_public_text` |
| 1 | entity critic 2, round 1 | fix | `rubric_p1_question_concrete` fix/`sides_blurred_bought_swords` |
| 1 | entity critic 2, round 2 | pass | — |
| 1 | phase critic | pass | `rubric_p1_legible` note/`start_hunt_needs_way_out`, note/`public_face_unshown` |
| 1 | wishes critic | pass | (no findings) |
| 2 | entity critic 1 | pass | `rubric_p1_secret_trail` note/`known_villain_absent_from_public` |
| 2 | entity critic 2 | pass | `rubric_p1_secret_trail` note/`no_public_trace_of_known_warden`; `rubric_p1_only_true_here` note/`bite_check_vs_cannot_tell` |
| 2 | phase critic, round 1 | fix | `rubric_p1_question_concrete` [premise__test_p1_3] fix/`side_a_hires_blades_in_first_session`; `rubric_p1_question_concrete` [signature_coalborn] fix/`both_sides_hire_contradicts_side_a`; `rubric_leak` note/`keeping_hint_in_discoverable` |
| 2 | entity critic after the phase fix | pass | `rubric_p1_secret_trail` note/`known_warden_absent_public`, note/`leash_holder_beyond_rolls` |
| 2 | phase critic, round 2 | pass | `rubric_p1_legible` note/`known_warden_absent_public`; `rubric_leak` note/`keeping_hint_in_discoverable` |
| 2 | wishes critic | pass | (no findings) |

`rubric_p1_legible` judged in every entity critic and phase critic return (pass, with notes).

**The door:** run 1, six units refused (section 3); run 2, all six passed. No fragment was refused twice → no `door` stop.

**Promises:** due at P1 9, kept 9, not kept 0, waived 0; open P2 10 · P3 27 · P4 13 · P5 13 · P6 12 · P7 15 · P8 8 · P9 2 · validator 2 · play 1; secret 32 open, 1 kept, 0 not kept. The run-2 merge added 4 promises (stubs and placements). Script-checked: 7 kept, 0 not kept.

**`D&D:` line:** ✓ villain · ✓ hand · ✓ goal · ✓ weakness · ✓ lair · ✓ start · ✓ families · ✓ stages 3×3 · ✓ breaks bend.

**Secret (spoiler-safe card line):** the threat rolled, hidden · hidden facts 3 of 4 · twist yes · stages 3 × 3 clues.

**Validator:** 0 errors, 0 warnings. **Gate:** open ✓. **Stops S1-S8:** none.

**Real cost per role** (`design.json` → `phases.P1.cost`; both runs recorded, the refused run 1 included):

| Role | Run 1 agents / req / output / cache read | Run 2 agents / req / output / cache read |
|---|---|---|
| writer | 1 / 29 / 64,147 / 5,349,628 | 1 / 20 / 13,951 / 1,777,896 |
| fix | 2 / 28 / 12,641 / 2,218,592 | 1 / 13 / 5,082 / 994,644 |
| critic | 2 / 21 / 16,415 / 2,004,227 | 2 / 35 / 14,766 / 3,727,006 |
| critic2 | 2 / 18 / 17,616 / 1,760,490 | 1 / 10 / 7,657 / 778,218 |
| phase_critic | 1 / 19 / 13,870 / 1,640,971 | 2 / 30 / 23,146 / 2,714,547 |
| wishes_critic | 1 / 3 / 673 / 165,776 | 1 / 3 / 694 / 165,776 |
| **total** | **9 / 118 / 125,362 / 13,139,684** | **8 / 111 / 65,296 / 10,158,087** |

Phase total: 17 agents, 229 requests, output 190,658, input 458, cache write 1,604,061, cache read 23,297,771; Workflow context (peak sum) 2,139,836 (`--tokens` 1,223,436 + 916,400). Card: "2.139.836 tokens, 38 min".

**Wall-clock per round:** run 1 1,401 s (23.4 min); run 2 850 s (14.2 min); review stop ~10 min (card 12:04:19 → approve 12:14:05).

## 3. Failures

**Door refusal, run 1.** Command: `py .claude/skills/dnd/scripts/designer.py -c _test-p1-3 phase P1 merge --tokens 1223436 --seconds 1401 --run-dir "…\wf_ae88e5d7-edc"` → **exit 1**:

```text
✗ break_rule_by_lottery: stamped must be an object
  ✗ break_rule_by_lottery: name missing
  ✗ break_underground_forbidden: stamped must be an object
  ✗ break_underground_forbidden: name missing
  ✗ premise__test_p1_3: stamped must be an object
  ✗ premise__test_p1_3: name missing
  ✗ signature_coalborn: stamped must be an object
  ✗ signature_house_ilaro: stamped must be an object
  ✗ signature_talon_bloom: stamped must be an object
designer: P1 6 unit(s) refused and marked failed — the next `phase P1 begin --json` lists them with the reason: break_rule_by_lottery, break_underground_forbidden, premise__test_p1_3, signature_coalborn, signature_house_ilaro, signature_talon_bloom
designer: P1 6 critic return(s) recorded
design_cost: P1 run wf_ae88e5d7-edc: 9 agents. 118 requests. output 125.362. cache read 13.139.684 (peak context summed 1.227.461)
registry: merged 0 unit(s) from P1 (0 row(s)); refused 6: break_rule_by_lottery, break_underground_forbidden, premise__test_p1_3, signature_coalborn, signature_house_ilaro, signature_talon_bloom
design_seed: P1: 0 call(s) made, 0 already seeded, 0 failed
designer: P1 partial
```

**Cost of the refused run:** 9 agents, 118 requests, output 125,362, cache read 13,139,684, peak context 1,227,461, 1,401 s; 66 % of the phase's real output went into a run whose every unit was refused. Its cost row is recorded with `"merged": true` although 0 units merged.

The next `begin --json` listed six entries: the premise (`render_attempt 2`, prompt with the reason) and the five rows with their `last_error` and no `prompt_cmd`. The JSON was passed unfiltered; run 2 rewrote all six and the door passed them.

Writer return counts differ across run 1: the first writer returned `counts` with `appears_notes 24, fragments 6`; the two fix writers returned `mechanic_steps 6, mechanic_thresholds 3` (one) and neither (the other), without `fragments`. The last fix's fragment is the one the door refused. (Conductor's observation from the returns; the fragment itself was not read.)

No tracebacks.

## 4. Review rounds

1. **P0 review stop** → `devam` (design tab, owner's word) → `phase P0 approve --onay`, exit 0.
2. **P1 review stop, attempt 1, open** → `disarm`, REVIEW block sent (story, card, report, both merges, runs) → `devam` → `arm --mode birth`, `phase P1 approve --onay`, exit 0 (`card be4697fb4747…, commit None`).

No `düzelt`, `isim yenile`, `vazgeç` or `yeniden koş` round.

## 5. Leak test

`design_approval.py -c _test-p1-3 leak-check campaigns/_test-p1-3/design/_approval/P1.card.md` → `design_approval: clean`, exit 0. The card was also scanned clean when written ("leak scan clean"). End block: `phase P1 report` exit 0 (status approved, gate open); `status --json` exit 0 (P0, P1 approved; P2-P9 pending; 68 public rolls, 15 secret, 26 tables); `disarm` → guard disarmed. P2 not started.

## 6. Observations

- The door refused every unit of run 1 on shape (`stamped must be an object`, `name missing`) after two critics had passed it; the critics judge the prose, not the fragment's shape, so a shape fault survives the whole chain and costs a full run.
- The refusal came from a fix writer's fragment, not the first writer's (counts changed across fixes); a fix agent seems able to rewrite the fragment's shape.
- Run 1's cost row says `merged: true` with 0 units merged; the label is misleading for a fully refused run.
- `begin --json` after the refusal lists the five rows without `prompt_cmd`; the Workflow handled it (the premise writer rewrote all six).
- The phase critic's fix reached the writer in run 2 (`phase_fixes` fixed → pass), the first live test of build 18f's path; it did not appear as `phase_fix_due` at the gate because the Workflow resolved it inside the run.
- The phase critic's two fixes in run 2 both hit `rubric_p1_question_concrete` (side A hiring blades in session one; both sides hiring) — the same area critic 2 flagged in run 1 (`sides_blurred_bought_swords`); the "hired guards" value and the survival-vs-honour question pull against each other.
- Recurring note across critics: the known warden / villain has no public trace (`known_villain_absent_from_public*`, `no_public_trace_of_known_warden`, `known_warden_absent_public`); never escalated to fix.
- The pitch opens on a threat with a face (werewolf pack led by a grey she-wolf) and a session-one job (follow the pack's trail before the full moon); `D&D:` all ✓.
- The story sentence names the threat and the contest but not the second contest (casters vs the casterless) nor the escalation; it reads as local.
- Epic name stocks were drawn in full (persons 258, ruin sites 120, …), all unused at P1.
- Wall time per run fell from 23 to 14 minutes on the second run (no entity fix loops).
