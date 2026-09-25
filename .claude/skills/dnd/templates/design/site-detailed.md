---
entity: site_<slug>
type: site
secrecy: public
phase: P6
status: detailed
stamped: [danger_tier, room_count, act, thread, key_npcs]
mirror: design/dm-only/sites/site_<slug>.md
---

# <Site name> — <kind>, T<n>, <room count> rooms (Act <n>)

*Plan item 9.4-9.6, 24.1 #13. The four-phase format: Concept & ecology / Map / Room-by-room / Content variety check, then Running this well and Connections. The room table is machine-read: keep its columns, the `Exits` column and the `[Entrance]` / `[Payoff]` markers; the `sites` module measures the minimum depth on it and `site_progress.py` opens its record from it.*

## Public

### Phase 1 — Concept & ecology
- **What this place is:** <two or three sentences — history, why it is here, what it is now>
- **Danger tier:** **T<n>** (CR <band>) · **Role:** <minor / standard / major / capstone> · **Room count:** **<n>** · **Payoff:** <type> — <what>
- **Thread:** [[<id>]] · **Key NPCs:** [[npc_<id>]] · **Attitude to intruders:** <…>
- **Ecology:** <who lives where and why; leader / elite / minion / ambient / solo roles; what they eat, guard, fear; reskins noted (`creature_` ids)>
- **Telegraphs:** far — <…>; near — <…>; threshold — <…> *(made concrete here)*
- **Escape geometry:** <the retreat route that differs from the entry; what it costs>
- **Rest pressure / sanctuary:** <where a short rest is possible, what a long rest risks, the wandering check>

### Phase 2 — Map
- **Entrances (≥2):** room <n> (<how>), room <n> (<how, condition>)
- **Verticality:** <levels, drops, climbs>
- **Loop:** <which rooms form the loop that lets a retreat use a different route — the loop leads back to exits, never to the payoff>
- **Minimum depth:** <n> rooms (shortest entrance → payoff path) — **stamped by the validator at detail time**
- **Sketch:** <ASCII or a one-paragraph walk-through of the graph>

### Phase 3 — Room-by-room
*Category ∈ combat / trap / special / structural. XP is the raw creature XP, no group multiplier. `Exits` lists room ids with the means and any condition (`3 (kapı)`, `5 (cezirde)`, `2 (tek yön)`, `6 (kilitli, anahtar 4)`); `[Entrance]` and `[Payoff]` go in the Room column.*

| # | Room | Category | Content | Exits | XP |
|---|---|---|---|---|---|
| 1 | <name> [Entrance] | structural | <what is here — sensory line, then mechanics> | 2 (kapı), 4 (…) | 0 |
| 2 | <name> | combat | <creatures ×n (`<SRD block>`), their tactics, what they want> | 1, 3 | <xp> |
| 3 | <name> | trap | <trigger, DC, effect, tell> | 2, 5 | <xp> |
| 4 | <name> [Entrance] | special | <a choice, a puzzle, a negotiation> | 1, 5 (tek yön) | 0 |
| 5 | <name> | combat | … | 3, 4, 6 (kilitli) | <xp> |
| 6 | <name> [Payoff] | special | <the payoff and its guardian> | 5 | <xp> |

- **Total XP:** <sum> vs budget <n> · **Rooms:** <count> vs stamp <n> (±10 %)

### Phase 4 — Content variety check
| Category | Rooms | Share | Band |
|---|---|---|---|
| combat | <n> | <%> | ~50 % |
| trap | <n> | <%> | ~10 % |
| special | <n> | <%> | 10-15 % |
| structural | <n> | <%> | 15-20 % |

### Boss *(if any — the six-point checklist is mandatory, sized against a reference party at the tier's intended level, never the actual party)*
- **Who:** [[npc_<id>]] or `creature_<id>`, CR <n> · **Room:** <n>
- **Multi-round HP sizing:** <HP vs the reference party's burst; `burst_check.py` result>
- **Resistance by default:** <what it resists and why in fiction>
- **Terrain protection:** <what the room gives the boss>
- **Pre-boss attrition:** <what the party has spent by room <n>>
- **Tanky adds:** <what stands between the party and the boss; adds drop nothing>
- **Signature weapon + defensive item** *(real loot, attunement stated)*: [[item_<id>]], [[item_<id>]]

### Loot
| Where | What | Rarity / attunement | Note |
|---|---|---|---|
| room <n> | <item> | <…> | <from `loot-budget.yaml` for T<n>; plot items are `item_` entities> |

## Running this well
- <three or four lines: the pacing, the moment to let the telegraph land, the choice that matters, what a party three levels early sees and where it runs>

## Connections
- **Before:** [[<id>]] — <what leads here> · **After:** [[<id>]] — <what the payoff opens>
- **News:** <what the occupants' defeat or survival writes into the world (the `if never visited` plan, now with an outcome)>

## Discoverable

- <what a survivor, a map or a local can tell: a second entrance, the guardian's habit, the tide>

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/sites/site_<slug>.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: site_<slug>
type: site
secrecy: secret
phase: <PN>
stamped: [<the public stamps>, <the secret stamps>]
mirror_of: <this public file's path>
---
-->

## Secret

- **Clue placement:** <which clue, in which room, how it surfaces>
- <the true occupant, the thread payoff, what the villain wants from this place>
