# Critique analysis 1 — what the critics said over three births, and what changed (2026-09-26)

*The owner asked for one analysis pass before the next birth: "we have test data now; analyse, adjust, then continue". Data: the critic returns and manifests of `_test-tune-1`, `_test-tune-2` and `_test-dry-1` on disk (`design_critique_stats.py`, ids, verdicts, rubric ids and reason codes only — no prose). Written by the development tab.*

## 1. The numbers

208 critic returns over 69 critiqued entities (plus the skeleton, phase and wishes critics).

| Question | Answer |
|---|---|
| Do fix loops work? | Yes. First verdict: 30 pass, 39 fix. Final: 66 pass, 3 fix. A first `fix` ended `pass` 38 times of 39. |
| How many loops? | 20 entities needed none, 31 one, 18 two. Loop 2 fell mostly on npc (6), faction (4), chapter, site, batches. |
| Second critic | 6 pairs (premise, BBEG, lieutenants); it disagreed with the first critic's final verdict twice. Too few to judge; kept. |
| Phase critics | P4 3/3 `fix`, P5 3/3 `fix`, P7 2/2 `fix`; P2, P3 always `pass`. Their `fix` findings are almost all the leak class below. |
| Skeleton critics | fix → pass in P3, P5, P6; P4 pass → fix; P7 fix → fix (twice). Their findings: stubs without `status: pending` (6), a duplicate full name (4), read-budget gaps (3), a faction stamp missing (2), a secret id not opaque (2). |

The rubrics that fail (fails / times judged):

| Rubric | Fails | Rate | Reason codes |
|---|---|---|---|
| `rubric_leak` | 66 / 259 | 0.25 | `dm_only_relation_in_public_refs`, `secret_content_in_public_writer_notes`, `public_notes_restate_mirror`, `verbatim_secret_section_sentence`, `secret_tier_hinted_in_public` |
| `rubric_english_names` | 14 / 222 | 0.06 | `mythology_name` ×2, `turkish_operation_name` ×2, `turkish_common_noun_as_alias`, `turkish_proper_noun_konsey_lonca` |
| `rubric_skeleton_stubs` | 13 / 63 | 0.21 | `missing_status_skeleton` ×6, `village_anchor_missing`, `faction_stamp_missing`, `secret_id_not_opaque` |
| `rubric_skeleton_structure` | 12 / 55 | 0.22 | `read_budget_gap` ×3, one-offs |
| `rubric_p5_voice_distinct` | 9 / 18 | 0.50 | `shared_tic_no_differentiator` ×4 |
| `rubric_skeleton_naming` | 6 / 44 | 0.14 | `duplicate_full_name` ×4, near-homophones |
| the rest | ≤2 each | | `rubric_p3_settlement_fears`, `rubric_p6_boss`, `rubric_p7_consequence_shape`, `rubric_p7_three_routes`, `rubric_p8_*` |

Of the 46 first-critic `fix` findings on entities, 29 were `rubric_leak`; of the findings that sent an entity into loop 2, ten of twelve were leak codes. The rubrics of P1 and P2 (forbidden defaults, the hundred-campaigns test, the question, the trail, the signatures, the gods carrying the question, history) were judged five or more times each and never failed. `rubric_cliche` failed once in 243.

Cost, summed over the three births (Opus 5.5):

| Phase | Minutes | Output tokens | Roster items | Tokens per roster item |
|---|---|---|---|---|
| P1 | 37 | 1.34 M | 3 | 446 k |
| P2 | 59 | 1.62 M | 3 | 541 k |
| P3 | 67 | 3.66 M | 11 | 332 k |
| P4 | 100 | 6.77 M | 14 | 484 k |
| P5 | 112 | 8.51 M | 30 | 284 k |
| P6 | 132 | 4.05 M | 4 | 1.01 M |
| P7 | 98 | 6.51 M | 10 | 651 k |
| P8 | 32 | 1.88 M | 2 | 939 k |
| P9 | 18 | 1.01 M | 2 | 504 k |

## 2. What the numbers say

1. **The critics were doing a door's job.** A quarter of every finding and two thirds of the first-critic fixes are structural leaks a script can see: a secret id in a public row's `refs`, a mirror sentence copied into the public file or restated in the public notes, a secret name in the notes. Each such finding cost two agents (a fix and a re-critique) at 100-150 k tokens apiece, and the phase critics of P4, P5 and P7 reported the same class again at phase level. A door refusal costs one re-run and carries the exact reason.
2. **Naming is the second class**, and nothing enforced the blacklist despite the reference saying names were "checked at every phase approval".
3. **The skeleton critic pays for itself**: it turned fix → pass in three phases, and its failures are mechanical (stubs, duplicates, opaque ids) — door material again.
4. **Voice distinctness fails half the time** because the preroll let a speech tic repeat and the writers did not add the differentiator the rubric asks for.
5. **The fix loop itself is sound**: when a critic says fix, the fix lands. It is the *reasons* that were cheap to prevent.
6. **Cost per roster item is highest where one agent writes many things**: P6 (a skeleton that writes every site, then two detailed sites) and P8 (a primer section reading everything). Read budgets are two hops out; that is the next lever, not touched now.

## 3. What changed (commit "Critique analysis 1")

- **The registry door** (`registry.py merge`) refuses, with the reason placed in the retry prompt: a mirror sentence contained in the public file or in the public notes; a secret name or a `## Secret` heading in the public notes; a prose-type row without a file that is not a `status: pending` stub; a secret npc whose id is not opaque; a name on `naming.yaml`'s blacklist (mythology, the owner's banned names, the model's favourites, banned stems, substrings); Turkish letters in a name (breaks and the premise excepted); a Turkish common noun used as a proper name (`blacklist.turkish_as_name`, new; a lowercase Turkish descriptor stays a valid alias); a name another campaign registered in `.name_registry.json`; duplicate full names within persons, places, factions, gods, items and planes, and first-name collisions among persons.
- **The projection** drops every secret id from public rows (refs, relations, heir, public_face, key_npcs …): the canonical link stays for the DM, nothing public says a secret entity exists. The fixture's projection was regenerated.
- **P5 preroll**: speech tics are distinct while the table has unused rows.
- **The critic prompts** say what the door already refused, so they judge meaning and craft instead of re-reporting mechanics.
- `design_critique_stats.py` stays as the instrument; run it after every birth.

## 4. What to watch in the next birth

- `rubric_leak` findings should fall to the "hinted" kind only; if the phase critics still end at `fix` in P4/P5/P7, read their reason codes — the door has a blind spot.
- Loop-2 entities should be mostly craft (voice, consequence shape, three routes), not structure.
- Tokens per roster item in P6 and P8: unchanged by this pass; the read-budget lever waits for one more measurement.
- `design_compare` on `_test-dry-2`: the door's duplicate-name rule is within a campaign; the uniqueness across campaigns is the compare script's job.
