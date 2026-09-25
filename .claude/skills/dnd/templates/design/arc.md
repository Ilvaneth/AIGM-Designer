---
entity: arc_1
type: arc
secrecy: public
phase: P7
stamped: [beats, endings]
covers: [beat_<id>, seed_<id>, socket_<id>]
mirror: design/dm-only/arc.md
---

# Arc — <campaign name>

*Plan item 10, risk 24.1 #10. Two layers: beats are the spine (mandatory consequences, never events), chapters are situations. `state.md → Campaign Arc` holds only the pointer and status; this file holds the design. A pre-empted beat is resolved with `arc fallback`, which picks one of the three fallbacks written here; the bible is never rewritten.*

## Public

- **Theme (the question):** see [[thread_premise]]
- **Resolution shape:** <the emotional / thematic truth if the party succeeds — no events>
- **Acts:** <1 (short) / 3> · **Beats:** <3 / 6> · **Chapters:** [[chapter_1]], [[chapter_2]], …

### Beats
*`change_kind` ∈ control / knowledge / status / relationship / loss / access / threat. `state_before` and `state_after` are the world's state, not the party's action. `world_pressure` names a real `factions.json` operation step.*

#### [[beat_<id>]] — <label> (Act <n>)
- **change_kind:** `<kind>`
- **state_before:** <the fact about the world that is true until this beat lands>
- **state_after:** <the fact that is true afterwards — what is different, not what happened>
- **what_changes:** <one sentence, consequence-shaped; the critique pass rejects "X happens">
- **world_pressure:** `<operation id>.<step id>` — <what the faction is doing that makes this inevitable>
- **telegraph scene:** <the earlier scene that makes the beat feel earned>
- **delivery paths (2-3):** [[site_<id>]] — <how>; [[npc_<id>]] — <how>; <event> — <how>
- **fallbacks (all three written at birth):**
  - *cost:* <the beat lands anyway, and the party pays for having pre-empted it>
  - *secondary:* <the consequence lands through a second actor or place>
  - *deferred:* <the consequence waits, and the world shows the delay>
- **status:** `pending` *(current / complete / skipped are play-time; the pointer lives in state.md)*

#### [[beat_<id>]] — …

### Endings *(designed at birth, each consequence-shaped)*
- **Win:** <the world after> — seeds of a next arc: <…>
- **Loss:** <the world after> — <…>
- **Pyrrhic:** <the world after> — <…>

### Planted hooks *(3-5 per act; `foreshadowing_check.py` flags one unresolved for 25+ days)*
| Hook | Planted where | Payoff hint | Status | Planted day |
|---|---|---|---|---|
| <an object, a line, a signpost> | [[<id>]] | <what it pays off, in one line the DM can read without the secret> | planted | — |

### Quest seed bank *(6-8 / 15-20 / 30+ by scale; about half tied to sites; every seed has a concrete outcome)*
#### [[seed_<id>]] — <title>
- **Hook:** <how the party hears of it> · **Complication:** <what makes it hard> · **Resolution:** <what a solved seed looks like> · **Reward:** <…>
- **Tied to:** [[npc_<id>]] / [[faction_<id>]] · **Site:** [[site_<id>]] or —

## Discoverable

- <what an attentive party can see of the spine before it lands: the portents, the names that keep recurring>

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/arc.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: arc_1
type: arc
secrecy: secret
phase: <PN>
stamped: [<the public stamps>, <the secret stamps>]
mirror_of: <this public file's path>
---
-->

## Secret

- **The villain's pre-emptions:** <how the BBEG tries to land its own beats first>
- **Clue-to-beat map:** <which beat surfaces which clue>
- **Fallback notes the player must not see:** <…>
