# `overlay.json` — play-time truth for designed entities

Errata 24.2 #2, owner decision 24.6 #3, plan items 14.1, 15.1 (`overlay` module), 16.1, 16.5.

**Immutable means the stamped fields.** Everything about a designed entity that play can change lives here, keyed by entity id, so the bible is never rewritten and the generated files (`world.md`, `npcs.md`, `design/index.md`) can render registry ⊕ overlay with a "changed since birth" marker on every overlaid value.

Writers, and the fields each may write:

| Writer | Fields |
|---|---|
| `factions.py simulate` | `control`, `ruler`, `alive`, `location`, `_meta.threat_stage`, `price_modifiers`, `pending_scenes`, `_meta.simulated_to_day` |
| `factions.py` (react, op, set) | `control`, `alive`, `ruler` |
| `site_progress.py` | `status` (`detailed` → `played`), `seen_in_play` |
| `campaign_graph.py` | `seen_in_play` (from `discovered` edges), `alive` (from a death edge) |
| `registry.py play-set` | any overlay field, by the DM's explicit call, always with a reason |
| `registry.py merge` | `status` only (`skeleton` → `detailed` / `detailed-stale` / `played-improvised`), because `detail` is what changes it |

Any other field on an entity (a stamped field above all) is refused by `design_check.py overlay`.

## Shape

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "written_by": "registry.py merge --phase P6",
    "written_at": "2026-09-24T20:00:00Z",
    "simulated_to_day": 0,
    "threat_stage": 1,
    "doom_day": 96,
    "doom_moved": []
  },
  "entries": {
    "site_sunken_pier": {
      "status": {"value": "detailed", "birth": "skeleton", "writer": "registry.py merge", "day": 0, "news": null, "reason": "P6 birth-detailed site"}
    },
    "site_tide_cave": {
      "status": {"value": "skeleton", "birth": "skeleton", "writer": "registry.py merge", "day": 0, "news": null, "reason": null}
    },
    "site_blind_lantern": {
      "status": {"value": "skeleton", "birth": "skeleton", "writer": "registry.py merge", "day": 0, "news": null, "reason": null}
    },
    "site_bottomless_well": {
      "status": {"value": "skeleton", "birth": "skeleton", "writer": "registry.py merge", "day": 0, "news": null, "reason": null}
    }
  },
  "pending_scenes": [],
  "price_modifiers": {}
}
```

## Entry record

Each overlaid field is an object, never a bare value, so the writer and the day are always present (the `overlay` module errors otherwise):

| Key | Meaning |
|---|---|
| `value` | the current value |
| `birth` | the registry's birth value, copied when the field is first overlaid; the "changed since birth" marker is `value != birth` |
| `writer` | the script and verb |
| `day` | campaign day of the change |
| `news` | the `news.json` record id that carried it, or null |
| `reason` | free text only for `registry.py play-set`; null for simulation writes (the news record is the reason) |

Allowed field names and their closed values:

| Field | On | Values |
|---|---|---|
| `status` | site, settlement | `skeleton` / `detailed` / `detailed-stale` / `played` / `played-improvised` |
| `seen_in_play` | any | `true` / `false` |
| `alive` | npc | `alive` / `threatened` / `wounded` / `fled` / `captured` / `dead` |
| `location` | npc | a settlement, place, site or region id |
| `ruler` | settlement, polity | an npc id |
| `control` | site, settlement, place | a faction id, or `party`, or null (abandoned) |

## `pending_scenes` (charter rule 3: brake = park, never halt)

A simulated move that touches a party asset, or a removing outcome against the `load_bearing` set, is parked here instead of resolved. `load` prints these first; the dead-time skip stops on the first pending day.

```json
{
  "id": "scene_0001",
  "day": 23,
  "actor": "faction_tide_brotherhood",
  "move": "sabotage",
  "target": "place_weary_gull",
  "why": "party_asset",
  "capped_from": "destroyed",
  "capped_to": "threatened",
  "line_tr": "Tide Brotherhood Weary Gull'un kayıklarını kesmeye gelir; ne olacağı masada belli olur.",
  "status": "pending",
  "resolved_day": null,
  "resolution": null
}
```

`why` ∈ `party_asset` / `load_bearing` / `tier_mismatch`; `status` ∈ `pending` / `played` / `dismissed`.

## `price_modifiers` (the light economy)

Keyed by settlement id; each entry carries `until_day` so the modifier expires without a second write. The field ships with the overlay in v3.0; the `--economy` dial that feeds it is on the cut list.

```json
{
  "settlement_lanternside": [
    {"goods": "silah", "modifier": 1.3, "from_day": 30, "until_day": 60, "writer": "factions.py simulate", "news": "news_0009"}
  ]
}
```

## `_meta.doom_day` and `_meta.doom_moved`

The BBEG's doom day is fixed at birth (charter rule 2) and moves only through a party-caused structured block; each move is appended to `doom_moved` as `{"day": 41, "from": 96, "to": 110, "block": "op_court_1.step_3", "news": "news_0021"}` so the history is auditable.
