# `site-progress.json` — a site is a graph, not a list

Plan item 9.5 (play side), 13.3, 16.5, 21.D (`SKILL-combat.md` marks rooms). The site counterpart of `tracker.json`, at the campaign root beside it.

Written only by `site_progress.py` (`open`, `enter`, `clear`, `skip --reason`, `shortcut`, `status`). `save` reports "Sunken Pier: 2/6 oda"; a `skipped` room requires a reason; an unreasoned skip shows in the validator. `site_progress.py` is also the writer of the overlay's `status: played` and `seen_in_play` for the site.

## Shape

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "written_by": "site_progress.py open",
    "written_at": "2026-09-24T20:00:00Z"
  },
  "sites": {
    "site_sunken_pier": {
      "opened_day": null,
      "opened_session": null,
      "entered_via": null,
      "entrances": ["1", "4"],
      "payoff_room": "6",
      "min_depth": 3,
      "room_count": 6,
      "current_room": null,
      "rooms": {
        "1": {"state": "unseen", "day": null, "session": null, "reason": null},
        "2": {"state": "unseen", "day": null, "session": null, "reason": null},
        "3": {"state": "unseen", "day": null, "session": null, "reason": null},
        "4": {"state": "unseen", "day": null, "session": null, "reason": null},
        "5": {"state": "unseen", "day": null, "session": null, "reason": null},
        "6": {"state": "unseen", "day": null, "session": null, "reason": null}
      },
      "shortcuts_earned": [],
      "rests": [],
      "notes": []
    }
  }
}
```

## Fields

| Field | Meaning |
|---|---|
| `entrances[]`, `payoff_room`, `min_depth`, `room_count` | copied from the site file's `Exits` column (the `sites` module parses only that column) when the record is opened at `detail` time; `min_depth` is the shortest entrance → payoff path and is what the validator measures |
| `opened_day` / `opened_session` / `entered_via` | first entry; `entered_via` is a room id from `entrances` |
| `current_room` | where the party is; the answer to "which room were we in" after a compaction |
| `rooms[id].state` | `unseen` / `seen` / `cleared` / `skipped` |
| `rooms[id].reason` | mandatory for `skipped` ("the party's route bypassed it via 2 → 5") |
| `shortcuts_earned[]` | `{"from": "2", "to": "6", "how_tr": "...", "day": 12}`: a loop back to the payoff opens only when earned in play (a map, a learned secret) |
| `rests[]` | `{"room": "3", "kind": "short", "day": 12}`: rest pressure is read from here |
| `notes[]` | free lines the DM appends at `save` (a door forced, an alarm raised) |

A record exists only for sites whose overlay `status` is `detailed` or later; a skeleton site has no record, and a `played-improvised` site gets one at `end` when `detail` backfills it.
