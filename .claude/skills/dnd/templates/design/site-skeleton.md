---
entity: site_<slug>
type: site
secrecy: public
phase: P6
status: skeleton
stamped: [danger_tier, room_count, act, thread, key_npcs]
mirror: design/dm-only/sites/site_<slug>.md
---

# <Site name> — skeleton

*Plan item 9.2. A skeleton is the directory entry with everything the world needs before the party approaches: fixed danger, a thread, three telegraphs, escape geometry, an attitude, what happens if nobody comes. It is never run from as a dungeon, with the one tiered exception for a minor unlinked site (24.6 #5). `detail` replaces this file with the detailed template on approach and may not change a stamped line.*

## Public

- **Kind / role:** <dungeon (planned / lair / tomb / ruin / natural) / stronghold / wilderness / urban / planar / social> · <minor / standard / major / capstone>
- **Region:** [[region_<id>]] · **Act:** <n> · **Danger tier:** **T<n>** (CR <band>) · **Room count:** **<n>** (band <lo-hi>)
- **Thread / trigger:** [[<faction / npc / seed / beat id>]] — <why this place exists in the story>
- **Payoff:** <treasure / lore / ally / plot_item / access> — <one line>
- **Key NPCs:** [[npc_<id>]] (<role here>)
- **Occupants (ecology summary):** <who or what lives here, from `monster-ecology.yaml`, and why they are here>
- **Attitude to intruders:** <kill / capture / enslave / ignore / negotiate / test>

### Telegraphs — how a party knows the danger before stepping in
| Distance | Telegraph |
|---|---|
| far | <what is said or seen from a day away> |
| near | <what the approach shows> |
| threshold | <what the entrance itself says> |

### Escape geometry
<Which way out exists for a party that realises it is out of its depth, and what it costs: a different route, a loop, a tide, a fall.>

### If never visited
<The occupant's own plan on a calendar — what has happened here 60 days after birth if the party never comes; wired to the faction's operation.>

- **Reoccupation candidate:** [[faction_<id>]] — <who moves in when the current occupant is gone>
- **Intended path:** <yes / no> · **XP budget:** <n> (formula for intended-path sites; rolled inside the band for off-path)

## Discoverable

- <what a local, a map or a survivor can tell about the inside before entry>

## Secret
*(written to `design/dm-only/sites/site_<slug>.md`)*

- <the clue this site carries, the true occupant, the thread payoff the party must not learn before entering>
