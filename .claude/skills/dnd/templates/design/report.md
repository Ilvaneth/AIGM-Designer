---
entity: none
type: report
secrecy: public
phase: P8
stamped: []
mirror: design/dm-only/report.md
---

# Design report — <campaign name>

*Plan item 15.3. One page at the end of birth, built by script from `design.json` and the public projection. What the user sees for final approval is this report's public part plus the primer. Hidden entities are counted, never named.*

## Public

### Dials and dice
| Dial | Value | Rolled? |
|---|---|---|
| scale | <…> | — |
| tone | <…> | d7 = <n> → <row> |
| … | … | … |
- **Seed:** `<master seed>` · **Public rolls:** <n> (`design.json → dice_log`) · **Secret rolls:** <n> (labels only)

### Scale counts (target / actual)
| Type | Band | Actual |
|---|---|---|
| regions | <lo-hi> | <n> |
| settlements | <…> | <n> |
| factions | <…> | <n> |
| named NPCs | <…> | <n> (major <n> / supporting <n> / minor <n>) |
| sites | <…> | <n> (detailed at birth <n>) |
| gods | <…> | <n> |
| quest seeds | <…> | <n> |
| sockets | party × <2 / 3> | <n> |

### Signatures and trope breaks
- <the three signatures and the break(s), each with its entity count>

### Faction board (public)
| Faction | Archetype | Power / intel | HQ | First operation (name only) |
|---|---|---|---|---|
| <name> | <…> | <n> / <n> | <place> | <name> |

### Site directory status
| Site | Tier | Rooms | Act | Status |
|---|---|---|---|---|
| <name> | T<n> | <n> | <n> | skeleton / detailed |

### PC sockets
- <n> sockets, all unbound until `design integrate`

### Validation and critique
- **Validator:** <errors> errors, <warnings> warnings (last run <when>)
- **Critique loops per phase:** P1 <n> · P2 <n> · … · **critique_missing:** <n>
- **Failed ids:** none / <count, phase>
- **Wishes:** <per-wish ✓ from the `wishes` rubric>

### Cost
- **Tokens out:** <n> (input estimated: <n>) · **Wall clock:** <h:mm> · **Agents:** <n> · **Sittings:** <n>

## Discoverable

*(nothing)*

## Secret
*(written to `design/dm-only/report.md`)*

- **Secret-layer abstract for the DM:** archetype class <…>, novelty vs `used.json` <yes / no>, clue count per act <n / n / n>, critic agreement <…>
- **dm-only criteria that failed, if any:** <count and module names>
