---
entity: premise_<campaign slug>
type: premise
secrecy: public
phase: P1
stamped: [question_tr, signatures, trope_breaks]
covers: [signature_<magic>, signature_<culture>, signature_<institution>, break_<row>]
mirror: design/dm-only/premise-secret.md
---

# Premise — <campaign name>

*Plan item 4. The premise runs first; everything downstream derives from it. The public file is what the player approves; the big secret and the DM pitch live only in the mirror.*

## Public

### The question
- **Theme as a question:** *"<the one question the campaign tries to answer>"*
- **Tension rows rolled:** `<tension id>` (+ `<second id>` if two) — <one line on how they combine>
- **The world's default answer:** <what most people in this world would say>
- **What the finale turns on:** <the party's answer, stated as a choice they will face — no outcome>

### Three signatures — things true only here
- **Magic phenomenon:** **<name>** — <the unique rule in two sentences; who can use it, what it costs>. Appears in: [[<id>]], [[<id>]], [[<id>]] *(≥3 entities, validator counts)*
- **Culture or creature:** **<name>** — <who they are; SRD reskin if any>. Appears in: [[<id>]], [[<id>]], [[<id>]]
- **Institution:** **<name>** — <what it does, who fears it, what it regulates>. Appears in: [[<id>]], [[<id>]], [[<id>]]

### Trope break(s)
- `<break id>` — **<the break in one line>**. How it shows: <where the player will feel it in the first three sessions>. Touches: [[<id>]], [[<id>]], [[<id>]], [[<id>]], [[<id>]] *(≥5, validator counts)*

### Forbidden defaults — checked
*<one line per forbidden default that the premise was tempted by and how it was avoided, or "none tempted">*

### Naming languages
- `<language key>` — <culture>, sound family `<family>`; samples: <three names>
- `<language key>` — …
*(full definition in `design/naming.json`)*

### Player pitch
*Three sentences, spoiler-free: the question, the signatures, the trope break — what the player will experience as different. This is the text on the approval card.*

<sentence one> <sentence two> <sentence three>

## Discoverable

- <one or two things a curious native could learn about the world's question in Act 1 — the surface of the secret, never the secret>

---

<!-- MIRROR FILE. Everything from here on is written to `design/dm-only/premise-secret.md`, never to this public file; the public file ends above this line. The mirror starts with its own front matter: -->

<!--
---
entity: premise_<campaign slug>
type: premise
secrecy: secret
phase: <PN>
stamped: [<the public stamps>, <the secret stamps>]
mirror_of: <this public file's path>
---
-->

## Secret

### The big secret
- **Archetype:** `<secrets.yaml row id>` + twist `<twist id>`
- **The truth:** <one paragraph: what is actually true about the world's nature>
- **Who knows:** [[<npc id>]] (fully), [[<faction id>]] (in part)
- **Why it is hidden:** <who benefits from the lie>

### Three-clue trail
| # | Act | Layer | Clue | Placed in | Surfaces how |
|---|---|---|---|---|---|
| 1 | 1 | surface | <what the party can notice> | [[<npc or site id>]] | <check / conversation / document> |
| 2 | 2 | investigation | <what connects clue 1 to a cause> | [[<site id>]] | <how> |
| 3 | 3 | deep | <what proves the truth> | [[<site id>]] | <how> |
*(in `short`, all three sit in Act 1 in chapter order; the validator checks act order and placement)*

### The villain's answer
- **BBEG:** [[<npc id>]] embodies the answer *"<their answer to the question>"*; visibility pattern `<antagonists.yaml row>`.
- **Why they are right, from where they stand:** <two sentences that make the villain a position, not a monster>

### DM pitch
<Three to five sentences: the campaign with the secret included — what the DM is steering toward and why it will land.>

### Signature mechanic
*(rolled; `short` never has one)* — <none / name, track, thresholds, gains, costs, tracker id>
