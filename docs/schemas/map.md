# `map.json` — the map is a graph; the picture derives from it

Plan item 6.1, 6.2, 15.1 (`map` module), 24.4 (SVG rendering is slice 4; the graph half ships in slice 1).

Written by the P3 skeleton through `registry.py merge` (nodes and edges are merged like entities, keyed by id). `travel-times.md` is **generated** from shortest paths over `edges`, never written by hand, which makes "a place reached via a hub can never be closer than the hub" automatic. Coordinates are proposed by the LLM on a 100×100 grid and validated by script: an edge's drawn length must be monotone with its `days` inside a region (a 2-day route may not draw longer than a 5-day one).

## Shape

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "tuzlu-fener",
    "fixture": true,
    "written_by": "registry.py merge --phase P3",
    "written_at": "2026-09-24T18:40:00Z",
    "grid": 100,
    "unit": "days on horseback",
    "player_map": "design/player-map.svg",
    "dm_map": "design/dm-only/dm-map.svg"
  },
  "regions": {
    "region_tuz_ovasi": {"bbox": [10, 20, 90, 85], "danger_tier": 2, "biome": "tuz bataklığı", "polity": "polity_sazlik"}
  },
  "nodes": [
    {"id": "settlement_fenerli", "kind": "settlement", "x": 42, "y": 61, "region": "region_tuz_ovasi", "terrain": "kıyı", "secrecy": "public", "hub": true},
    {"id": "settlement_kamisli", "kind": "settlement", "x": 68, "y": 44, "region": "region_tuz_ovasi", "terrain": "sazlık", "secrecy": "public", "hub": false},
    {"id": "site_batik_iskele", "kind": "site", "x": 36, "y": 70, "region": "region_tuz_ovasi", "terrain": "kıyı", "secrecy": "public", "hub": false},
    {"id": "site_gelgit_magarasi", "kind": "site", "x": 24, "y": 52, "region": "region_tuz_ovasi", "terrain": "kayalık kıyı", "secrecy": "discoverable", "hub": false},
    {"id": "site_kor_fener", "kind": "site", "x": 14, "y": 78, "region": "region_tuz_ovasi", "terrain": "burun", "secrecy": "public", "hub": false},
    {"id": "site_dipsiz_kuyu", "kind": "site", "x": 80, "y": 28, "region": "region_tuz_ovasi", "terrain": "tuz düzlüğü", "secrecy": "public", "hub": false},
    {"id": "landmark_kirik_dalgakiran", "kind": "landmark", "x": 30, "y": 66, "region": "region_tuz_ovasi", "terrain": "kıyı", "secrecy": "public", "hub": false},
    {"id": "waypoint_sazlik_yolu", "kind": "waypoint", "x": 56, "y": 52, "region": "region_tuz_ovasi", "terrain": "sazlık", "secrecy": "public", "hub": false}
  ],
  "edges": [
    {"id": "r_fenerli_iskele", "from": "settlement_fenerli", "to": "site_batik_iskele", "days": 0.5, "terrain": "kıyı", "road": "track", "region": "region_tuz_ovasi", "note_tr": "Dalgakıranın kırık ucundan görünür."},
    {"id": "r_fenerli_yol", "from": "settlement_fenerli", "to": "waypoint_sazlik_yolu", "days": 1, "terrain": "sazlık", "road": "road", "region": "region_tuz_ovasi", "note_tr": null},
    {"id": "r_yol_kamisli", "from": "waypoint_sazlik_yolu", "to": "settlement_kamisli", "days": 1, "terrain": "sazlık", "road": "road", "region": "region_tuz_ovasi", "note_tr": null},
    {"id": "r_kamisli_kuyu", "from": "settlement_kamisli", "to": "site_dipsiz_kuyu", "days": 1.5, "terrain": "tuz düzlüğü", "road": "none", "region": "region_tuz_ovasi", "note_tr": "Kamışlı'dan kimse bu yola çıkmaz."},
    {"id": "r_fenerli_gelgit", "from": "settlement_fenerli", "to": "site_gelgit_magarasi", "days": 1, "terrain": "kayalık kıyı", "road": "none", "region": "region_tuz_ovasi", "note_tr": "Yalnızca cezirde geçilir."},
    {"id": "r_fenerli_fener", "from": "settlement_fenerli", "to": "site_kor_fener", "days": 1.5, "terrain": "burun", "road": "track", "region": "region_tuz_ovasi", "note_tr": null},
    {"id": "r_gelgit_fener", "from": "site_gelgit_magarasi", "to": "site_kor_fener", "days": 1, "terrain": "kayalık kıyı", "road": "none", "region": "region_tuz_ovasi", "note_tr": "Kıyı boyunca, cezirde."},
    {"id": "r_iskele_dalgakiran", "from": "site_batik_iskele", "to": "landmark_kirik_dalgakiran", "days": 0.25, "terrain": "kıyı", "road": "none", "region": "region_tuz_ovasi", "note_tr": "Kırık ucuna yürüyerek; gece fener burada yanar."}
  ],
  "insets": []
}
```

## Fields

| Node | |
|---|---|
| `id` | the registry id for settlements and sites; `landmark_` / `waypoint_` ids are map-only (not registry entities) |
| `kind` | `settlement` / `site` / `landmark` / `waypoint` |
| `x`, `y` | integers on the grid |
| `region` | region id |
| `terrain` | free text in the narration language, used by the travel table |
| `secrecy` | the player map draws only `public` nodes; `discoverable` and `secret` are on the DM map |
| `hub` | true for the settlement whose travel table is the region's default |

| Edge | |
|---|---|
| `id` | `r_<from>_<to>` |
| `from`, `to` | node ids; edges are undirected for travel |
| `days` | days on horseback, half days allowed |
| `terrain`, `road` | `road` ∈ `highway` / `road` / `track` / `none`; feeds the travel table's category weights |
| `region` | the region whose travel table applies |
| `note_tr` | one line the DM may read out; null allowed |

`insets` holds regions unreachable by normal travel (item 6.2): `{"id": "region_x", "label_tr": "...", "reachable": false, "entry": "site id or null"}`.

## What `design_check.py map` verifies

Graph connected across `public` nodes; every site and settlement in the registry has a node and vice versa; every node inside its region's bbox; drawn length monotone with `days` within a region; `travel-times.md` equals the generated shortest-path table; exactly one hub per region.
