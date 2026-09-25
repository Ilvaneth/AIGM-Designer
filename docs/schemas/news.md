# `news.json` — what the world did, as the party could see it

Plan item 7.7 (5), 13.1(c), 16.3(a), 24.1 #20 (form and volume), errata 24.2 #16 (`refs[]`), charter rule 5 (the LLM only renders `line_tr`).

Written by `factions.py simulate` for every resolved move, and once by P8 for the day-0 slice (the primer's "current rumours"). Records are append-only; a record is never edited after the day it was written, a correction is a new record. The DM reads the records whose `reach` includes the party's current region when a scene opens, at most 2-3 lines, delivered through a person, a rumour or a visible change.

## Shape

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "written_by": "design_seed.py --phase P8",
    "written_at": "2026-09-24T19:55:00Z",
    "next_id": 4,
    "last_day": 0
  },
  "records": [
    {
      "id": "news_0001",
      "day": 0,
      "source": "birth",
      "faction": "faction_tide_brotherhood",
      "move": null,
      "outcome": null,
      "roll": null,
      "region": "region_saltmere",
      "settlement": "settlement_lanternside",
      "visibility": "public",
      "kind": "rumour",
      "line_tr": "Üç yıl önce batan Vesper gemisinin bir sandığı gelgitte kıyıya vurmuş; iskele hamalları sandığı kimin aldığını söylemiyor.",
      "refs": ["event_vesper_wreck", "site_sunken_pier", "faction_tide_brotherhood"],
      "reach": ["settlement_lanternside", "region_saltmere"],
      "secrecy": "public",
      "seen_by_party": false,
      "parked_as": null,
      "step": null
    },
    {
      "id": "news_0002",
      "day": 0,
      "source": "birth",
      "faction": "faction_court_of_mourners",
      "move": null,
      "outcome": null,
      "roll": null,
      "region": "region_saltmere",
      "settlement": "settlement_lanternside",
      "visibility": "rumored",
      "kind": "portent",
      "line_tr": "Court bu ay üç ölü için okuma yaptı, ama ailelerden ikisi okumayı istememişti.",
      "refs": ["faction_court_of_mourners", "npc_ilme"],
      "reach": ["settlement_lanternside"],
      "secrecy": "discoverable",
      "seen_by_party": false,
      "parked_as": null,
      "step": "op_court_1.step_1"
    },
    {
      "id": "news_0003",
      "day": 0,
      "source": "birth",
      "faction": null,
      "move": null,
      "outcome": null,
      "roll": null,
      "region": "region_saltmere",
      "settlement": "settlement_reedham",
      "visibility": "public",
      "kind": "rumour",
      "line_tr": "Reedham'da bu kış üçüncü kez, tuz düzlüğünden gelen birinin kapıyı çalıp içeri girmeden gittiği anlatılıyor.",
      "refs": ["settlement_reedham", "site_bottomless_well", "creature_saltbound"],
      "reach": ["settlement_reedham"],
      "secrecy": "public",
      "seen_by_party": false,
      "parked_as": null,
      "step": null
    }
  ]
}
```

## Fields

| Field | Values / meaning |
|---|---|
| `id` | `news_NNNN`, monotone |
| `day` | campaign day the event happened |
| `source` | `birth` / `simulate` / `play` (the DM registering something the party caused, via `registry.py play-set --news`) |
| `faction` | acting faction id or null |
| `move` | `seize` / `sabotage` / `bribe` / `spy` / `persuade` / `assassinate` / `besiege` / `negotiate` / `hold` / `consolidate` or null (item 7.7 plus 24.1 #9's `hold` / `consolidate`) |
| `outcome` | `success` / `fail` / `parked` / `capped` or null |
| `roll` | the opposed check as resolved by the seeded in-process rng: `{"label": "simulate:d12:faction_x:seize:place_y", "attacker": 9, "defender": 7, "margin": 2}` or null. Stored so a week is reproducible and auditable (24.1 #8) |
| `region`, `settlement` | where it happened; `settlement` null for the wild |
| `visibility` | `public` (anyone there would know) / `rumored` (a rumour the party can catch) / `secret` (only the actors know; the DM reads it, never narrates it unprompted) |
| `kind` | `control` / `stance` / `operation_step` / `death` / `succession` / `economy` / `rumour` / `portent` / `pending_scene` |
| `line_tr` | one line in the narration language, "what the party would see"; the only field the LLM writes, at `end`, from the structured fields |
| `refs[]` | registry ids the record touches; `detail` and `load` match a record to a site through this |
| `reach[]` | settlement and region ids where the news is heard; a public settlement record reaches its region a week later (simulate appends) |
| `secrecy` | the tier of the *record*; a `secret` record is excluded from the `end` summary and the primer |
| `seen_by_party` | set by `save` when the DM narrated it; the feed never repeats a seen record |
| `parked_as` | `pending_scenes[].id` in the overlay when the move was parked |
| `step` | `<operation id>.<step id>` in `factions.json` when the record advanced or failed an operation step; the threat table reads BBEG steps from here |

## Volume rule (24.1 #20)

`scale.yaml` caps records per simulated week; `simulate` writes one record per resolved move and one per cascade reaction, never a record for a `hold`. The `end` summary lists the week's records minus `secret` ones.
