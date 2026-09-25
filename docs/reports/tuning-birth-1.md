# Tuning birth 1 — `_test-tune-1`

*Slice 1c, item 8. Protocol `docs/tuning-births.md`, birth 1 (straight through). Written by the conductor tab on 2026-09-25; ids, codes, counts and verbatim script output only. The development tab reads the campaign under `campaigns/_test-tune-1/` itself.*

**Outcome in one line:** the birth **stopped in P5**. P1 merged; P2, P3, P4 and P5 each had a merge refused on a fragment the registry does not accept, so only skeleton stubs reached the registry from P3 onwards. P5's card and approval were refused by the leak scan, and P6 cannot begin without an approved P5. **Leak test: FAIL.** There was no Python traceback during P1-P5; the only traceback came from the after-P8 block (`render_player.py check` on a primer that does not exist).

## 1. Run

| | |
|---|---|
| Campaign | `_test-tune-1` |
| Command | `designer.py new _test-tune-1 --scale short --party-size 1 --seed TUNE-0001 --lang tr` |
| Seed | `TUNE-0001` |
| Rolled dials | tone d7→2 `tone_dark_fantasy` · magic d4→3 `magic_medium` · era d5→4 `era_nautical` · danger d4→2 `danger_gritty` · content mix d5→5 `mix_mystery`, d4→1 `mix_exploration`, d3→1 `mix_politics` |
| Fixed dials | scale short, party 1, start level 1 (band 1-5), lang tr, no wishes, concurrency 8, economy off |
| Model | Opus 5.5 (`claude-opus-5-5`), conductor and every agent (inherited) |
| Session effort | low (conductor tab) |
| Start / stop | 16:24:26 (`new`) → 19:08:50 (`disarm`), local time |
| Total wall-clock | 2 h 44 min, of which Workflows 157 min |
| Agents launched | 48 across 10 Workflow runs, 0 null, 0 errors |
| Subagent tokens | ≈ 5.37 M |
| Transcript root | `C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\4079d22e-8912-4091-9a35-13053fad09bf\subagents\workflows\<run id>\` (each has `journal.jsonl`) |
| Script root | `C:\Users\armag\.claude\projects\C--Users-armag-Desktop-Campaign-Designer\4079d22e-8912-4091-9a35-13053fad09bf\workflows\scripts\<workflow>-<run id>.js` |

Workflow runs:

| Phase | Workflow | Run id | Agents | Duration | Tokens | Tool uses |
|---|---|---|---|---|---|---|
| P1 | design-fanout | `wf_809be016-cc5` | 5 | 1150 s | 505 k | 86 |
| P2 | design-fanout | `wf_63f5d5cc-501` | 6 | 1951 s | 738 k | 119 |
| P2 retry | design-fanout | `wf_d6cc277b-1c9` | 6 | 568 s | 581 k | 84 |
| P3 | design-skeleton | `wf_6f605623-8b5` | 1 | 702 s | 232 k | 48 |
| P3 | design-fanout | `wf_dccb0cc2-edc` | 14 | 850 s | 1379 k | 226 |
| P3 retry (villagebatch_1 only) | design-fanout | `wf_7b18cf32-b0c` | 4 | 298 s | 304 k | 49 |
| P4 | design-skeleton | `wf_9ccdb12f-e1f` | 1 | 1379 s | 377 k | 61 |
| P4 | design-fanout | `wf_6eea70d7-206` | 6 | 807 s | 571 k | 94 |
| P5 | design-skeleton | `wf_2ef6c133-97f` | 1 | 1101 s | 277 k | 51 |
| P5 | design-fanout | `wf_8cf32fb8-915` | 4 | 642 s | 405 k | 81 |

## 2. Per phase

| Phase | Workflow(s) | Agents | Null | Fix loops | 2nd critic | Entity verdicts | Phase / wishes critic | Merge | Validator (phase check) | Card | Approve | Wall-clock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P0 | — | 0 | — | — | — | — | — | — | — | written | auto | <1 min |
| P1 | fanout | 5 | 0 | 0 | 1 | premise `pass`, c2 `fix` | fix / pass | **ok**, 14 fragments | 13 E, 0 W: refs `dangling_link` ×2, `role_unfilled` ×6 (faction_dusk_company ×3, faction_lampwrights ×3); stamps `bad_tier` site_eelhollow; secrecy `file_no_secrecy` ×3; map `no_map` | ok, leak clean at the time | auto | 20 min |
| P2 | fanout ×2 | 6 + 6 | 0 | 1 + 1 | 0 | doc_cosmology `fix`→`pass` (both runs) | fix / pass, then pass / pass | **refused** ×2 | 59 E then 60 E: refs 51 (`dangling_link`), secrecy 6→7, stamps 1, map 1 | "0 entities" card | auto (see 3.5) | 43 min |
| P3 | skeleton + fanout + retry | 1 + 14 + 4 | 0 | 0 + 2 + 0 | 0 | region_bonecrag `fix`→`pass`, region_hushwold `fix`→`pass`, settlement_candlehithe `pass`, villagebatch_1 `pass` (both runs) | pass / pass ×2 | skeleton ok (26 stubs); fan-out **refused** ×2 | 129 E then 130 E: map 15, refs 91 (`dangling_ref` 21+, `dangling_link`), secrecy 18, stamps 5 | stubs only | auto | 33 min |
| P4 | skeleton + fanout | 1 + 6 | 0 | 0 + 1 | 0 | calculus__test_tune_1 `fix`→`pass` | fix / pass | skeleton ok (11 fragments); fan-out **refused** | 138 E: map 15, refs 90, secrecy 27, stamps 6 | stubs only | auto | 37 min |
| P5 | skeleton + fanout | 1 + 4 | 0 | 0 + 0 | 0 | npcbatch_1 `pass` | fix / pass | skeleton ok (15 fragments); fan-out **refused** | 181 E | **refused (leak)** | **refused (leak)** | 31 min, stopped |
| P6-P8 | not reached | | | | | | | | | | | |

Skeleton counts, as returned:

- **P3:** roster `region_bonecrag, region_hushwold, settlement_candlehithe, villagebatch_1`. 2 regions, 3 settlements, 2 villages, 26 stub fragments, 4 facts files, map 13 nodes / 13 edges, graph 29 / 34, 6 npc / 8 place / 2 site / 2 faction stubs. `design_seed` made 26 calls, 0 failed.
- **P4:** roster `faction_harbor_magistracy, faction_lampwrights, faction_blacknet, calculus__test_tune_1`. 4 factions on the board, 3 in the roster, 1 deferred, 6 stance edges, 5 stubs new / 6 updated, 20 seeds, 19 graph edges, `pipeline_findings: 8` (self-reported by the skeleton agent; not visible to the conductor). `design_seed` made 8 calls.
- **P5:** roster 9 named npcs + `npcbatch_1`. 14 persons (3 major, 5 supporting, 6 minor), 2 new npcs (`npc_ghusom`, `npc_liavenar`), 24 public edges, 8 secret edges, 49 graph edges, 5 channels + 3 secret channels. `design_seed`: 3 calls, 11 already seeded.

## 3. Failures

### 3.1 P2 — merge refused, twice (identical)

`designer.py -c _test-tune-1 phase P2 merge` (exit 1), after `wf_63f5d5cc-501` and again after `wf_d6cc277b-1c9`:

```
✗ doc_cosmology.json: fragment needs `id` and a `registry` object
  ✗ event_harpoon_night: stamped field(s) changed without --revise: day
  ✗ god_ughmash: stamped field(s) changed without --revise: domains, rank, secret_tr
registry: merge refused, 3 problem(s); nothing written
designer: P2 4 critic return(s) recorded
```

Two faults here. First, the document-roster fragment `doc_cosmology` has no registry shape. Second, the cosmos writer re-emitted P1's stamped `god_` and `event_` rows with changed stamped fields. The critic passed both times. The retry was rendered with `--attempt 1` again, because `begin --json` had not bumped the attempt.

### 3.2 P3 — fan-out merge refused, twice (identical)

`designer.py -c _test-tune-1 phase P3 merge` (exit 1), after `wf_dccb0cc2-edc` and after the one-entity retry `wf_7b18cf32-b0c`:

```
✗ villagebatch_1: unknown type 'batch'
registry: merge refused, 1 problem(s); nothing written
designer: P3 8 critic return(s) recorded
```

The merge is all-or-nothing. This one fragment blocked the three good ones (`region_bonecrag`, `region_hushwold`, `settlement_candlehithe`), all critic `pass`. The protocol's drop path does not work for a batch id:

```
$ py .claude/skills/dnd/scripts/design_revise.py -c _test-tune-1 round --phase P3 --scope entity --entity villagebatch_1 --action remove --text "tuning: failed twice"
design_revise: no entity villagebatch_1
```

### 3.3 P4 — fan-out merge refused

`designer.py -c _test-tune-1 phase P4 merge` (exit 1), after `wf_6eea70d7-206`:

```
✗ calculus__test_tune_1: unknown type 'calculus'
registry: merge refused, 1 problem(s); nothing written
designer: P4 4 critic return(s) recorded
```

Not retried (see 5, conductor choices).

### 3.4 P5 — fan-out merge, card and approve refused; birth stopped

`designer.py -c _test-tune-1 phase P5 merge` (exit 1), after `wf_8cf32fb8-915`:

```
✗ npcbatch_1: unknown type 'batch'
registry: merge refused, 1 problem(s); nothing written
designer: P5 3 critic return(s) recorded
```

`designer.py -c _test-tune-1 phase P5 card` (exit 1, twice) and `designer.py -c _test-tune-1 phase P5 approve` (exit 1):

```
design_approval: card refused, it would leak: secret name: I…
```

`designer.py -c _test-tune-1 phase P6 begin --json` (exit 1; `preroll --phase P6` had already run, 88 public rolls):

```
designer: P5 is running, not approved; P6 cannot begin
```

The leaking entity is `npc_s01`, a secret npc stub created by the P4 skeleton (see 4). Neither the batch nor the leak can be dropped with `design_revise`, so the birth ends here.

### 3.5 Phase-state regressions (no error text, but they change the loop)

- `phase P2 approve` returned `P2 approved (auto; commit none)` although the P2 merge had been refused and P2 had produced zero entities. Approve does not gate on a refused merge.
- The next `merge` or `begin` flips every earlier phase whose roster never reached the registry back to `partial`. That covered P2 from P3 on, P3 from P4 on, and P4 from P5 on. `phase P3 begin --json` then refused with:

  ```
  designer: P2 is partial, not approved; P3 cannot begin
  ```

  The conductor re-ran `phase PN approve` on each regressed phase before every `begin`, from P3 through P5. The protocol has no instruction for this case.
- Running `phase P2 begin --json` after `approve` put P2 back to `running`.

### 3.6 After-P8 block traceback

`render_player.py -c _test-tune-1 check campaigns/_test-tune-1/design/player-primer.md`, with no primer because P8 was never reached:

```
Traceback (most recent call last):
  File "...\scripts\render_player.py", line 387, in <module>
    sys.exit(main())
  File "...\scripts\render_player.py", line 382, in main
    return cmd_check(a.campaign, a.file)
  File "...\scripts\render_player.py", line 350, in cmd_check
    problems = check_text(campaign, Path(file).read_text(encoding="utf-8"), pub)
  ...
FileNotFoundError: [Errno 2] No such file or directory: 'campaigns\\_test-tune-1\\design\\player-primer.md'
```

### 3.7 Blocked read (guard false positive)

The conductor wrote its own scratch notes with a Bash heredoc into the session scratchpad. The text named the `antagonists.json` path under `design/dm-only/_staging/P4/`, and `design_read_guard.py` blocked the command:

```
BLOCKED by design_read_guard: Design mode 'birth' is armed for _test-tune-1: the conductor may not read dm-only content (design/dm-only/_staging/P4/antagonists.json). ...
```

Nothing was read; the guard matched a path string inside a write. Re-running the note without the path worked.

## 4. Leak test — FAIL

| Check | Result |
|---|---|
| `design_check.py -c _test-tune-1` | exit 1: refs 118, stamps 6, **secrecy 43**, overlay 0, map 15, sites 0 |
| `render_player.py check` on the primer | not run (no primer; traceback 3.6) |
| `design_approval.py leak-check` per card | P0 clean · **P1 LEAK: `secret name: I…; secret name: M…`** · P2 clean · P3 clean · P4 clean · P5 no card (refused) |

The 43 secrecy errors break down as follows:

- **4 × `npc_s01`: secret entity's name appears in** `design/entities.json`, `design/premise.md`, `design/cosmology.md`, `design/_approval/P1.card.md`. The P4 skeleton created a *secret* npc whose name was already public from P1. The public projection now carries it, which is why the P5 card refused. The P1 card was clean when it was written; it leaks after the fact.
- **3 × `## Secret` heading in a public file:** `design/consequence-calculus.md` (calculus__test_tune_1), `design/regions/region_hushwold.md`, `design/settlements/settlement_candlehithe.md`. Fan-out writers wrote secret sections into public prose. These files are on disk even though their fragments never merged.
- **6 × `under dm-only but not secrecy: secret`** and **6 × `does not name design/npcs/<id>.md as mirror_of`:** `npc_krusa`, `npc_liavenar`, `npc_mokrash`, `npc_mushak`, `npc_omuk`, `npc_sorrak`, all from the P5 minors batch.
- **25 × `has no secrecy in its front matter`** on `design/_approval/P*.card.md` and `design/_prompts/**`. The validator scans the conductor's own cards and rendered prompts. That is probably a scope bug, not a leak.

The remaining error classes:

- **refs:** 46 × `refs names <id>, which does not exist`. The top targets are `settlement_candlehithe` ×17, `region_bonecrag` ×6, `god_kragosh` ×4, `region_hushwold` ×3 and `event_southgoing` ×3, plus the P2 gods/events (`god_thaeleri`, `god_lirasael`, `event_wakers_snuffing`, `event_tallow_heresy`, `event_hullcrush`, `event_bleeding_fever`, `event_dusk_accord`). Also 23 unresolved `[[…]]` links in `design/cosmology.md` and 18 in the dm-only mirror, 1 `heir is empty`, and 1 `no prose file and not pending`. Almost all of this follows from the refused merges.
- **stamps:** `site_eelhollow` and `site_stillmouth` fail `danger_tier must be an integer 1-5`; `site_blackbarrow` and `site_saltbarrow` fail `danger_tier is not stamped` and `act is not stamped`.
- **map:** `settlement_candlehithe` and `site_tidegrave` fail `map node has no registry entity`, and 13 nodes name a region (`region_bonecrag` / `region_hushwold`) that does not exist.

## 5. Observations

**Conductor choices.** These were not in the protocol:

- P3 retry: `design-fanout` was re-run with the `begin --json` object filtered to `villagebatch_1` only. The other three entities were already `staged`, and re-running them would have cost about 1 M tokens.
- P4: `calculus__test_tune_1` was **not** retried after its refusal. It is the same class of failure as P2 and P3, which had repeated identically in every retry (3 of 3).
- P3-P5: `phase PN approve` was re-run on each regressed earlier phase before every `begin` (3.5).

**Roster and prompts**

- P4 / P5 (major): after the skeleton merged, `begin --json` listed **only** the non-entity roster items (`calculus__test_tune_1`, `npcbatch_1`). The skeleton roster also named 3 factions (P4) and 9 npcs (P5), including the 3 majors meant for effort high and two critics, but those never entered the fan-out. So no faction dossier and no major or supporting npc dossier was written. Reconcile appears to count an id as done once it has a skeleton stub row.
- P2 / P3 / P4 / P5: every document or batch roster item (`doc_`, `villagebatch_`, `calculus__`, `npcbatch_`) produces a fragment the registry refuses, and the critics pass it. No critic checks the fragment schema.
- P2: the cosmos writer rewrote P1-stamped fields of `god_ughmash` (domains, rank, secret_tr) and `event_harpoon_night` (day). The prompt does not seem to fence P1's stamped rows off.
- P1: premise second critic returned `fix`, but no fix loop ran (`fix_loops: 0`). The card shows "Eleştiri turu: 1 (fix → pass)".
- P3: the skeleton returned 2 villages while preroll drew 3 (`settlement.2`-`settlement.4`); `settlement.4` is unassigned.
- P4: the skeleton created stub id `npc_s01`, which looks like a placeholder and is the secret npc that leaks (4).
- P4: calculus `files` include a second staging root, the `_staging/P4/` folder under `design/dm-only/`.
- Skeleton Workflows: the begin JSON carried `critics: 1` (P3, P5) or `critics: 2` (P4) for the skeleton, but `design-skeleton` returned no critic verdict.

**Preroll**

- P5 (leak): the preroll printed all 14 `npc.N.secret` rows (`npcs.yaml#secret` → `npcsecret_*`) to the conductor as **public** rolls, "113 public rolls, 0 secret". P1 and P4 kept secrets as labels only (3 and 10 secret).
- P2-P5: count dice do not bound the rows drawn. Examples: `ages_count` 3 → age.1-5; `events_count` 1 → event.1-8; `deep_count` 3 → deep.1-5; `region.1.landmarks_count` 3 → 4 landmarks; `region.2.landmarks_count` 1 → 2; `settlement.1.districts_count` 1 → 2 districts; `village_count` 2 → 3 villages; `factions_count` 1 → 3 factions; `faction.N.rungs_count` 1 → 3 rungs; `npcs_count` 1 → 14 npcs.
- P5: secrets and tics repeat across the 14 npcs: `npcsecret_a_borrowed_body`, `_a_bought_vote`, `_bargain`, `_cowardice` and `_a_buried_fortune` ×2 each; `tic_weather_first`, `tic_talks_to_animal` and `tic_swears_by_landmark` ×2 each. This is inside the "≤2" distinctness bar, but 5 of 14 secrets are duplicates.

**Cards**

- All cards show "Süre: 0 dk · Çıktı: 0 token", so minutes and tokens are never recorded.
- The "Eleştiri turu" counter stays at 0 or 1 while the verdict chain grows across runs: P2 shows "1 (fix → pass → pass → pass)" and P3 "0 (pass → pass → pass → pass)". It does not show which entity each verdict belongs to.
- The phase critic's verdict (`fix` in P1, P2 run 1, P4 and P5) is never shown on the card, and nothing acts on it.
- The name table's `dil` column is `—` for every P1 entity and for the P3 district, npc and place rows. The P3/P4 factions, settlements and sites carry `deeptongue` / `lampsong`.
- The P2 card reads "(bu faz henüz varlık üretmedi)" with status `running`, yet the phase was approved. As the player, I could not tell that the cosmos had failed.
- P3 card: `region: 0 açık, bant 1-2 ✗`. The regions exist as prose but not in the registry.
- The redacted validator lines give no entity or file for `dangling_link` / `file_no_secrecy`, so the conductor cannot say which file failed. `phase PN check` also truncates at 40 lines.
- Public one-liners worth a look:
  - `break_light_is_billed`: typo "belediyenindir".
  - `npc_mokrash`: the whole one-liner is "The Second Lamp hanının hancısı.".
  - `place_second_lamp`: mentions "at süvarileri" in a nautical era.
- Wishes are empty in a test birth, so the wishes critic returned `pass` in every phase with nothing to check.

**Timing.** P2's first fan-out (one document) took 32.5 minutes; the retry took 9.5. The P4 skeleton took 23 minutes and the P5 skeleton 18.
