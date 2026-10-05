# `design.json` — the birth manifest

Plan item 19.4 (schema from the pipeline design pass, `docs/reports/2026-09-24-pipeline-design.md`), errata 24.2 #16 (`mark` / `tokens`, no `update` verb), 24.6 #6 (`ask` log).

Written only by `design_manifest.py init | reconcile | pending | mark | approve | stale | tokens | ask | status`, atomically. **Disk is truth, the manifest is the index, the Workflow journal is an accelerator.** `reconcile` rebuilds `entities[*].status` from the staging fragments and prose paths before every run.

## Shape (the fixture: a birth that completed, all phases approved)

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "designer_version": "dnd 3.0.0",
    "ruleset": "2014",
    "lang": "tr",
    "mode": "play",
    "git_root": "C:/Users/armag/Desktop/Campaign-Designer",
    "created": "2026-09-24T18:00:00Z",
    "written_by": "design_manifest.py approve --phase P9",
    "written_at": "2026-09-24T20:00:00Z"
  },
  "dials": {
    "scale": "short",
    "tone": "shadowed",
    "magic": "low",
    "era": "medieval",
    "danger": "gritty",
    "party_size": 2,
    "start_level": 1,
    "level_band": [1, 5],
    "content_mix": ["mystery", "exploration", "politics"],
    "wishes": {"must": ["deniz ve tuz kokusu", "ölüler gerçekten ölsün"], "must_not": ["kader/kehanet", "seçilmiş kişi"]},
    "lang": "tr",
    "concurrency": 8,
    "economy": false
  },
  "seed": {
    "master": "TF-4c1e9a07",
    "derivation": "random.Random(f'{master}:{phase}:{table}:{label}')"
  },
  "arc_skeleton": [
    {"chapter": "chapter_1", "act": 1, "level_band": [1, 3], "beats": ["beat_1a", "beat_1b"]},
    {"chapter": "chapter_2", "act": 1, "level_band": [3, 5], "beats": ["beat_1c"]}
  ],
  "dice_log": [
    {"phase": "P0", "table": "dials.yaml#content_mix", "label": "content_mix.1", "notation": "d5", "raw": 5, "row_id": "mix_mystery", "excluded": [], "ts": "2026-09-24T18:01:10Z"},
    {"phase": "P1", "table": "tensions.yaml", "label": "tension.1", "notation": "d30", "raw": 22, "row_id": "tension_memory_salvation", "excluded": [{"row": "tension_legacy_freedom", "why": "used_elsewhere"}], "ts": "2026-09-24T18:03:02Z"},
    {"phase": "P1", "table": "trope-breaks.yaml", "label": "break.1", "notation": "d40", "raw": 11, "row_id": "break_no_afterlife_known", "excluded": [], "ts": "2026-09-24T18:03:02Z"},
    {"phase": "P2", "table": "pantheon.yaml#type", "label": "pantheon_type", "notation": "d5", "raw": 4, "row_id": "pantheon_silent_gods", "excluded": [], "ts": "2026-09-24T18:20:44Z"}
  ],
  "dice_log_secret": {
    "file": "dm-only/dice-log.json",
    "count": 3,
    "labels": ["P1.secret_archetype", "P1.secret_twist", "P4.bbeg_visibility"]
  },
  "phases": {
    "P0": {"status": "approved", "attempt": 1, "workflow_run_id": null, "started": "2026-09-24T18:00:30Z", "finished": "2026-09-24T18:02:00Z", "wall_s": 90,
           "skeleton": {"status": "merged", "agent": null},
           "critique": {"phase_loops": 0, "verdicts": [], "entity_loops_total": 0},
           "validator": {"at": "2026-09-24T18:02:00Z", "errors": 0, "warnings": 0},
           "approval": {"rounds": [], "approved_at": "2026-09-24T18:02:30Z", "card_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "registry_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "commit": "0000000"},
           "directions": [], "tokens": {"in": 0, "out": 0, "cache_read": 0, "by_model": {}}, "stale_reason": null},
    "P6": {"status": "approved", "attempt": 2, "workflow_run_id": "wf_example", "started": "2026-09-24T19:10:00Z", "finished": "2026-09-24T19:31:00Z", "wall_s": 1260,
           "skeleton": {"status": "merged", "agent": "P6.skeleton.a1"},
           "critique": {"phase_loops": 1, "verdicts": ["fix", "pass"], "entity_loops_total": 2},
           "validator": {"at": "2026-09-24T19:31:00Z", "errors": 0, "warnings": 1},
           "approval": {"rounds": [{"correction": "Sunken Pier'in ikinci girişi denizden olsun", "scope": "entity", "affected_files": 2, "applied": true, "at": "2026-09-24T19:35:00Z"}],
                        "approved_at": "2026-09-24T19:40:00Z", "card_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "registry_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "commit": "0000000"},
           "directions": ["odaları ıslak ve dar tut"], "tokens": {"in": 0, "out": 61240, "cache_read": 0, "by_model": {"claude-fable-5-1": {"in": 0, "out": 61240}}}, "stale_reason": null}
  },
  "entities": {
    "npc_yesra": {"phase": "P5", "status": "validated", "file": "design/npcs/npc_yesra.md", "stage_file": "design/_staging/P5/npc_yesra.json", "attempt": 1, "critique_loops": 1, "last_error": null, "agent": "P5.npc_yesra.a1"},
    "site_sunken_pier": {"phase": "P6", "status": "validated", "file": "design/sites/site_sunken_pier.md", "stage_file": "design/_staging/P6/site_sunken_pier.json", "attempt": 2, "critique_loops": 1, "last_error": null, "agent": "P6.site_sunken_pier.a2"}
  },
  "seeded": [
    "calendar:init",
    "factions:faction_reedmarch", "factions:faction_court_of_mourners", "factions:faction_tide_brotherhood",
    "goals:npc_s01", "goals:npc_draskun", "goals:pc_selen", "goals:pc_vorin",
    "graph:node:npc_yesra", "graph:edge:e_3",
    "channels:ch_court_inner",
    "names:Yesra Saltreader"
  ],
  "detail_log": [],
  "revision_log": [
    {"at": "2026-09-24T19:35:00Z", "scope": "entity", "phase": "P6", "reason": "Sunken Pier'in ikinci girişi denizden olsun", "affected": 2, "commit": "0000000"}
  ],
  "ask_log": [],
  "totals": {"tokens_in": 0, "tokens_out": 98400, "cache_read": 0, "wall_s": 5400, "agents": 31},
  "validator_last": {"at": "2026-09-24T20:00:00Z", "errors": 0, "warnings": 1}
}
```

The fixture carries all ten phases in the real file; the two shown here are the shapes of a scriptless phase (P0) and a fan-out phase with a correction round (P6). A live manifest also carries `phases[N].roster[]`, the entity ids the phase's skeleton reserved (`design_manifest.py mark --roster`); `pending` is that roster minus what disk proves merged, and `reconcile` turns a phase `partial` when a roster entity's fragment is still in staging.

## Closed lists

- `_meta.mode`: `birth` / `play`. `load` refuses while `birth` (item 19.4); `design_read_guard.py` keys on it together with `active-design.json`.
- `phases[N].status`: `pending` / `prerolled` / `running` / `generated` / `merged` / `validated` / `critiqued` / `awaiting_approval` / `approved` / `partial` / `failed` / `stale` / `needs-check` (in play, after a phase-scope revise).
- `entities[id].status`: `pending` / `staged` / `merged` / `validated` / `critiqued` / `failed`.
- `approval.rounds[].scope`: `fact` / `entity` / `phase` / `direction` (item 19.6). Max three rounds per phase.
- `foundation` (plan item 25, P1 step 1; written by `designer.py preroll --phase P1`, public and stamped): `spine`, `palette` (the kinds in the count), `palette_extra` (the ruin source's kind, on top of the count), `ruin_source`, `lifeline` {id, seat}, `contests` [{id, roles, seat?}], `break` {target, target_role, action, scars, time, winner}, `escalation` {tiers, steps, level_band}, `layout` {parts: {heart, end_a, end_b, [end_c, end_d,] key_place → palette kind}, along: [kinds on the way], lifeline: part or `along:<kind>`, remnant: where the ruin's remnant lies (heart or key place only by a merge rule), break_at: where the break struck (its target's place), contests: [{contest, seats: {role → part or along}, prize: {kind, at}}]} (build item 6b), `merges`, `landmarks`, `start` (`heart`; `heart_ruins` when the break destroyed the heart and left ruins; `end_a` when it left none), `sentence_tr` (the identity's input, shown on the card). A birth whose P1 ran without it is a legacy birth (`design_manifest.legacy_birth`).
- `dice_log[].table`: `<file>#<subtable>`; `row_id` the table row rolled; `excluded[]` every row the arbiter kept out of the pool, each `{row, why}` (`caller`, a `where` reason such as `climate`, `forbidden`, `requires`, `conflict` with `with`, `weight_zero`, `used_elsewhere`, `family_wait` with `family`, `row_wait`, `pair`); an exclusion that names the secret layer goes to `dm-only/dice-log.json#exclusions` instead, and then the public `notation` / `raw` are counted over the rows not publicly excluded while the real die sits beside the secret exclusions (`notation`, `raw` there); `family_taken` when the table's `families_distinct` left a family out; `usage_fallback` names the usage kinds dropped when a table was exhausted (`dropped: family_wait, used_elsewhere`); `tokens` on a record of table `tokens` (notation `derived`): context tokens no row carries by itself, a seated contest role's claims (`foundation.contest.N.claims`) and the layout's (`foundation.layout.tokens`: `claim:below_ground=lived_in` when the heart sits underground, `layout:remnant_on_heart`), which every later phase's context reads back (`claims.yaml`, build item 7c); `used_keys` the non-row values approve writes to `used.json` (a target + action pair). `used.json` also keeps `births`: each campaign's first approval time, the order the waits count in (`design_arbiter.py`, plan item 25).
- `promises[]` (plan item 25's third rule, errata 24.2 #23; written by `designer.py preroll --phase P1`, extended by every `phase merge`; `design_promises.py`): the public promise ledger. A promise is `{id, source, from, from_phase, also[], due, text, name, check, status, verdict, waiver}`: `source` is `hook` / `override` / `foundation` / `stub` / `placement` / `concretise` / `clue_stage`; `from` the row id, the entity id or the foundation piece, `also[]` further sources of the same sentence; `due` a phase, `validator` or `play`; `check` is `script:<rule>` or `critic`; `status` is `open` / `kept` / `not_kept` / `waived`; `verdict` is `{phase, attempt, by}` once judged. An override promise also carries `default` and `to`. The secret promises (a secret roll's hooks, the secret's three clue stages with their `levels`, the placements the premise makes) live in `design/dm-only/promises.json` in the same shape; the card shows them as three counts. The public ledger is a function of the public rolls alone. A legacy birth has no `promises` key and no ledger. Inspection (build item 12b): `phase check` decides every `script:` promise due by then (`verdict.by: script`); the phase critic's return carries `promises[]` (`{id, verdict: kept | not_kept, note}`, a slug for a note) and `phase merge` stores id and verdict (`verdict.by: critic`); the owner's `designer.py promise waive <id> "<sentence>"` sets `status: waived` and `waiver: {sentence, at}` and appends a `revision_log` entry of `scope: promise` that names the promise by its id alone. A stub promise of a type the orphan-stub gate only warns about carries `minor: true`: it is judged and listed, and does not close the gate. The gate's two codes are `promise` (a due script promise not kept) and `promise_unjudged` (a due critic promise without a verdict); a critic's `not_kept` closes nothing and is listed on the card.

## Rules the fixture demonstrates

- `dice_log_secret` carries **labels and a count only**; results live in `design/dm-only/dice-log.json`, same record shape as `dice_log`.
- `seeded[]` is the idempotency ledger `design_seed.py` consults before every store call (`design_manifest.py seeded --add`); the key is `<store>:<id>` (`graph:node:<id>`, `graph:edge:<from>:<to>:<type>`, `factions:<from>:<to>` for a stance) and never carries a value.
- `approval` records the sha256 of the card the user saw and of the public projection at that moment, plus the commit, so "what was approved" is reconstructible.
- `ask_log` (24.6 #6): `{"at", "question_tr", "answer": "evet" | "hayır" | "spoiler vermeden cevaplanamaz", "agent"}`; the question is stored, never the agent's reasoning.
- `totals.tokens_in` stays 0 when the harness reports output deltas only; `report.md` says the input figure is estimated (item 19.11).
