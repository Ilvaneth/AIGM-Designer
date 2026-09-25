---
entity: faction_<slug>
type: faction
secrecy: public
phase: P4
stamped: [archetype, objective]
mirror: design/dm-only/factions/faction_<slug>.md
---

# <Faction name>

*Plan item 7. The four-phase dossier, adopted as is. Every field the validator counts (7.4) is here: fracture, secret, endgame, betrayal candidate, a stance toward every faction, power and intel, assets, an HQ that exists, doctrine for the six triggers, a first operation with dated steps, an heir. The `factions.json` row is seeded from the front matter and the Operations phase, never written by hand.*

## Public

### Phase 1 — Identity & Belief
- **Archetype:** `<state / religious / guild / criminal / martial / scholarly / resistance / cult / trade>` · **Founded:** [[event_<id>]] or <year> · **Alignment range:** <…>
- **Public position:** <what it says it is for>
- **Relation to the gods:** [[god_<id>]] — <how>
- **Signature presentation:** <colours, marks, the sentence people use to describe them>

### Phase 2 — Power & Resources
- **Power:** <1-5> · **Intel:** <0-3> · **Reach:** <where it can act>
- **Military:** <typical forces, anchored to an SRD NPC stat block: `<block>` ×n>
- **Magical:** <…> · **Economic:** <…> · **Territory:** [[settlement_<id>]], [[site_<id>]]
- **Assets on the map:** [[place_<id>]], [[site_<id>]], [[npc_<id>]] (control) *(assets are registry entities; a move can only take or break something that exists)*
- **HQ:** [[site_<id>]] or [[place_<id>]]

### Phase 3 — Structure & People
- **Leader:** [[npc_<id>]] · **Heir:** [[npc_<id>]] *(succession rule: the organisation never goes leaderless; doctrine shifts slightly on succession)*
- **Key web:** [[npc_<id>]] (<role>), [[npc_<id>]] (<role>), …
- **Access chain:** <who must be satisfied before whom, to reach the leader>
- **Recruitment and exit terms:** <how one joins, what leaving costs>
- **Services to the party** *(guilds especially)*: <training / identify / fencing / information / dues>
- **Stances** *(−3 … +3; mirrored into `factions.json`)*:
  | Toward | Stance | Reason (one line, shared by both dossiers) |
  |---|---|---|
  | [[faction_<id>]] | <n> | <reason> |
  | party | <n> | <reason> |

### Phase 4 — Intelligence & Operations
- **Network:** <how it learns things; intel delay in days>
- **Decision logic / doctrine** *(machine fields, charter rule 5)*: aggression `<0-3>`; target preference `<objective-holder / rival / weakest / party-never>`; move weights per trigger below
- **Reaction doctrine** *(all six triggers, canonical list in `factions.yaml`)*:
  | Trigger | Doctrine |
  |---|---|
  | alliance | <what it does when a rival allies> |
  | loss | <…> |
  | gain | <…> |
  | exposure | <…> |
  | death | <…> |
  | betrayal | <…> |
- **First operation** *(`factions.py op`)*: **<name>** — objective <…>
  | Step | Kind | Due day | Defender | Text |
  |---|---|---|---|---|
  | 1 | <timed / contested / party-only> | <day> | [[faction_<id>]] or — | <what the step does> |
  | 2 | … | … | … | … |
  - **Abandon if:** <structured predicate on the overlay, e.g. `control(site_x) != faction_self`>
  - **Metric:** <label current/target> or —
- **Default policy toward the party:** <ignore / watch / court / block>
- **Vulnerabilities:** <two>

## Discoverable

- **True belief vs cover:** <what members believe that outsiders do not hear>
- **Provocation ladder:** *(see `consequence-calculus.md`)* rung 1 <…> → rung 2 <…> → rung 3 <…>
- **What it wants independent of the party, and what it will have done in 60 days if the party never appears:** <the critique-pass answer, in two sentences>

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/factions/faction_<slug>.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: faction_<slug>
type: faction
secrecy: secret
phase: <PN>
stamped: [<the public stamps>, <the secret stamps>]
mirror_of: <this public file's path>
---
-->

## Secret

- **Secret:** <the thing that would break it if known>
- **Internal fracture:** <who wants what, and the line it splits along>
- **Betrayal candidate:** [[npc_<id>]] — <why, and what it would take>
- **Endgame:** <what victory looks like for this faction — the world after>
- **Ties to the antagonist hierarchy:** <if any: [[npc_<id>]] is its lieutenant / its front>
