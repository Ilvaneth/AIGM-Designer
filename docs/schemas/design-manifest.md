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
    "tone": "dark fantasy",
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
    {"phase": "P1", "table": "tensions.yaml", "label": "tension.1", "notation": "d30", "raw": 22, "row_id": "tension_memory_salvation", "excluded": ["tension_legacy_freedom"], "ts": "2026-09-24T18:03:02Z"},
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
- `dice_log[].table`: `<file>#<subtable>`; `row_id` the table row rolled; `excluded[]` the rows `used.json` made the dice skip.

## Rules the fixture demonstrates

- `dice_log_secret` carries **labels and a count only**; results live in `design/dm-only/dice-log.json`, same record shape as `dice_log`.
- `seeded[]` is the idempotency ledger `design_seed.py` consults before every store call (`design_manifest.py seeded --add`); the key is `<store>:<id>` (`graph:node:<id>`, `graph:edge:<from>:<to>:<type>`, `factions:<from>:<to>` for a stance) and never carries a value.
- `approval` records the sha256 of the card the user saw and of the public projection at that moment, plus the commit, so "what was approved" is reconstructible.
- `ask_log` (24.6 #6): `{"at", "question_tr", "answer": "evet" | "hayır" | "spoiler vermeden cevaplanamaz", "agent"}`; the question is stored, never the agent's reasoning.
- `totals.tokens_in` stays 0 when the harness reports output deltas only; `report.md` says the input figure is estimated (item 19.11).
