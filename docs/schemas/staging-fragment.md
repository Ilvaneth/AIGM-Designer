# `design/_staging/<phase>/<id>.json` — the commit record of one agent's work

Plan item 19.3 (staging protocol), 19.1 (schema-only returns), 13.3 (in-play `detail` uses the same path), errata 24.2 #4.

Every fan-out agent writes its prose file **first** and its fragment **last**. The fragment is the commit record: it names the prose path and byte size, and prose without a fragment is treated as absent by `design_manifest.py reconcile`. The conductor runs `registry.py merge --phase N`, which upserts the `registry` object into the canonical registry, applies `graph` and `seeds` through `design_seed.py` (consulting `seeded[]`), regenerates the projection, and moves the fragment to `_staging/<phase>/merged/`. `design phase <n>` archives the whole folder to `_staging/<phase>.attempt-<k>/`.

**No free text outside the registry fields.** Anything an agent wants to say goes to `_staging/<phase>/<id>.notes.md`, which reaches the conductor only through `design_check.py --redact` / `design_approval.py`. A `warnings[]` string from an agent that just read a secret is a leak.

## Shape

```json
{
  "schema_version": 1,
  "id": "site_batik_iskele",
  "type": "site",
  "phase": "P6",
  "attempt": 2,
  "agent": "P6.site_batik_iskele.a2",
  "mode": "birth",
  "written_at": "2026-09-24T19:28:14Z",
  "prose": {
    "file": "design/sites/site_batik_iskele.md",
    "bytes": 7420,
    "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
  },
  "dm_only_prose": {
    "file": "design/dm-only/sites/site_batik_iskele.md",
    "bytes": 1210,
    "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
  },
  "notes": "design/_staging/P6/site_batik_iskele.notes.md",
  "registry": {
    "id": "site_batik_iskele",
    "type": "site",
    "name": "Batık İskele",
    "aliases": ["Eski İskele"],
    "summary": "Fenerli'nin üç yıl önce çöken eski iskelesi; altında Kandil gemisinin sandıkları ve onları bekleyenler.",
    "file": "design/sites/site_batik_iskele.md",
    "secrecy": "public",
    "created_phase": "P6",
    "origin": "birth",
    "kind": "dungeon",
    "role": "minor",
    "region": "region_tuz_ovasi",
    "danger_tier": 1,
    "room_count": 6,
    "act": 1,
    "thread": "beat_1a",
    "key_npcs": ["npc_draskun"],
    "payoff": "plot_item",
    "telegraphs": [
      {"distance": "far", "text_tr": "Dalgakıranın kırık ucunda gece fener yanar; kimse yakmaz."},
      {"distance": "near", "text_tr": "Kazıkların dibinde tuz kabuğu bağlamış ayak izleri, hepsi denize doğru."},
      {"distance": "threshold", "text_tr": "İlk ambarın kapısında taze kesilmiş halat ve bir Kardeşlik düğümü."}
    ],
    "escape_tr": "Cezirde 4. odadan kumsala; metle 1. odadan geri, ama su bele kadar.",
    "attitude": "capture",
    "xp_budget": 450,
    "min_depth": 3,
    "intended_path": true,
    "if_never_visited_tr": "Kardeşlik sandıkları on gün içinde taşır; defter Gelgit Mağarası'na gider.",
    "reoccupation": "faction_kacakcilar",
    "stamped": {"danger_tier": 1, "room_count": 6, "act": 1, "thread": "beat_1a", "key_npcs": ["npc_draskun"]},
    "refs": ["settlement_fenerli", "npc_draskun", "faction_kacakcilar", "item_tuz_defteri", "creature_tuzbagli", "beat_1a"],
    "dm_only": {"clue": {"secret_clue": 2}}
  },
  "graph": {
    "nodes": [{"id": "site_batik_iskele", "type": "place", "name": "Batık İskele", "tags": ["site", "tier1"], "summary": "Çökmüş eski iskele; Kardeşlik deposu."}],
    "edges": [{"from": "faction_kacakcilar", "to": "site_batik_iskele", "type": "controls", "since_session": 0, "note": "birth"}]
  },
  "seeds": [
    {"store": "site_progress", "op": "open", "args": {"site": "site_batik_iskele", "entrances": ["1", "4"], "payoff_room": "6", "min_depth": 3, "room_count": 6}}
  ],
  "counts": {"words": 1180, "rooms": 6, "telegraphs": 3},
  "status": "staged"
}
```

## Fields

| Field | Meaning |
|---|---|
| `phase`, `attempt`, `agent` | the Workflow label; the attempt suffix defeats the journal cache on a retry (item 19.5) |
| `mode` | `birth` / `detail` / `integrate` / `revise`; in-play `detail` writes under `_staging/detail/` |
| `prose`, `dm_only_prose` | file, byte size, sha256; `dm_only_prose` null when the entity has no secret section |
| `notes` | the free-text file, or null |
| `registry` | the full entity row as [entities.md](entities.md) defines it, including `dm_only`; merge upserts it by id and refuses a stamped-field change without `--revise` |
| `graph` | nodes and edges for `campaign_graph.py`; ids resolve against the registry; edge `since_session` is 0 at birth |
| `seeds[]` | store calls for `design_seed.py`: `store` ∈ `factions` / `goals` / `graph` / `channels` / `calendar` / `site_progress` / `names`; `op` the script verb; `args` its arguments. The ledger key is `<store>:<id>` |
| `counts` | numbers the phase card may print; never text |
| `status` | `staged` when written; merge sets `merged` in the manifest, not here |

## Agent return schema (the Workflow `schema` option)

What the agent returns to the script is smaller than the fragment and carries no prose: `{entity_id, status: "staged" | "failed", fragment: "<path>", counts: {...}}`. The conductor learns names only from the projection.
