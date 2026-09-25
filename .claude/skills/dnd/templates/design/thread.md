---
entity: thread_<pc slug>
type: thread
secrecy: public
phase: P9
stamped: [pc, antagonist, layers]
mirror: design/dm-only/threads/thread_<pc slug>.md
---

# <PC name>'s thread — <title>

*Plan item 12. One file per PC, written by `design integrate` after `character new`. The public face is the mission and the people and places the character knows; the truth stays in the mirror. All PC thread files are read at every `load`.*

## Public

- **PC:** [[pc_<id>]] — <class, origin [[settlement_<id>]]>
- **Personal thematic question:** *"<the campaign's question from this character's angle — distinct from the other PCs'>"*
- **Mission (the player-facing goal, active voice — take back / prove / destroy, never "find out who"):** <one sentence> · tracker: `goals.json` `<pc id>` (kind `pc`)
- **People they know:** [[npc_<id>]] (<how>), [[npc_<id>]] (<how>)
- **Places they know:** [[place_<id>]], [[site_<id>]]
- **Sockets bound:** [[socket_<id>]] — <the backstory answer that filled it>

### Own sites *(≥1 per act, on or near the intended path)*
| Act | Site | Why it is theirs |
|---|---|---|
| 1 | [[site_<id>]] | <…> |

### Crossing points *(one per act; skipped for a solo party)*
| Act | Where | With | Why the other PC wants to be there |
|---|---|---|---|
| 1 | [[<id>]] | [[pc_<id>]] | <…> |

### Personal mechanical track *(only when the signature mechanic was rolled; all PCs' tracks live in one file)*
<none / pointer to `design/tracks.md`>

## Discoverable

- **Layer 1 (Act 1):** <what the character can learn first — placed in [[<id>]]; how it surfaces>

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/threads/thread_<pc slug>.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: thread_<pc slug>
type: thread
secrecy: secret
phase: <PN>
stamped: [<the public stamps>, <the secret stamps>]
mirror_of: <this public file's path>
---
-->

## Secret

- **The truth:** <something about their past or nature they do not know — pinned to [[event_<id>]] and [[<faction / npc id>]]; fills [[socket_<id>]]>
- **Layer 2 (Act 1 climax / Act 2):** <…> — placed in [[<id>]]
- **Layer 3 (Act 2-3):** <…> — placed in [[<id>]]
- **Personal antagonist:** [[npc_<id>]] — <tied to the hierarchy: whose lieutenant, whose front>
- **If the PC dies:** <the thread becomes a world thread: what its antagonist does next, which layers become seeds>
- **Equal-weight ledger** *(validator: sites, NPCs, layers, beats touched, XP share; ≤35 % imbalance between PCs)*: sites <n> · NPCs <n> · layers 3 · beats <n> · XP share <n>
