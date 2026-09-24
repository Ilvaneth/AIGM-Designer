---
entity: npc_<slug>
type: npc
secrecy: public
phase: P5
tier: supporting
stamped: [faction]
mirror: design/dm-only/npcs/npc_<slug>.md
---
<!-- the mirror's front matter lists the secret stamps too: stamped: [faction, secret_tr] -->


# <Name> — <role>

*Plan item 8.3, the Ashen Crown dossier standard plus four additions (heir, voice samples, offer / want, what changes if they die). Major and supporting NPCs get the full dossier; a **minor** NPC gets the index row and the three lines under "Minor" only, and is promoted by `detail` when the player latches on. A `secret` NPC (opaque slug) has this whole file in the mirror.*

## Public

- **Appearance:** <species, age, one concrete physical detail, what they wear, how they move>
- **Role / CR / location:** <role> · CR <n> (`<SRD stat block>`, level <n> if a class NPC) · usually at [[place_<id>]] in [[settlement_<id>]]
- **Faction:** [[faction_<id>]] · **Tier:** <major / supporting / minor> · **Alignment:** <…>
- **Demeanor:** <how they come across in the first minute>
- **Speech quirk:** <one line> · **Voice samples:**
  - *"<two or three sentences in their own voice — the register every scene keeps>"*
  - *"…"*
- **Schedule:** <when and where they can be found>
- **What they can offer the party / want from the party:** <service, information, work / what they would ask in return>
- **Attitude toward party:** <hostile → unfriendly → neutral → friendly → allied>
- **Current goal:** <what they are actively doing right now>

### Personality
- **Trustworthy ↔ Deceptive:** <…>
- **Ambitious ↔ Content:** <…>
- **Loyal ↔ Opportunistic:** <…>
- **Brave ↔ Cowardly:** <…>

### Relationships *(≥2; each carries the one reason line both dossiers share)*
- **Knows / Owes / Hates / Fears / Allied with:** [[npc_<id>]] — <reason>
- **Heir / heir of:** [[npc_<id>]] *(succession, item 7)*

### Known Facts — what they actually know and how
*Baseline from living memory (which events they witnessed) plus what the role implies; appended in play with the channel each fact came through.*
- day 0 — <fact> — <witnessed / told by [[npc_<id>]] / read in … / role>

## Discoverable

- **Motivation with history:** <what they want and the dated event that made them want it>
- **Weakness derived from personality:** <…>
- **What changes if they die:** <who succeeds, which thread breaks, in one or two lines>
- **Goal tracker** *(major only; mirrored from `goals.json`)*: goal <…>; metric <…>; threatened → <move>; blocked → <move>; permanent loss → <move>

## Secret
*(written to `design/dm-only/npcs/npc_<slug>.md`)*

- **Secret:** <the stamped secret>
- **Surfacing path:** <how it can come out — a check, a witness, a document, a slip>
- **Truth of a PC** *(if this NPC carries a PC's truth)*: [[pc_<id>]] — <what they know>
- **Notes for the DM:** <what to protect, what to let slip, what the villain's plan needs from this person>

---

### Minor *(index row + three lines; delete the sections above for a minor NPC)*
- **One physical detail:** <…>
- **What they want:** <…>
- **Speech tic:** <…>
