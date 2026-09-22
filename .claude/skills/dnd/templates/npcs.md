# NPCs — <campaign-name>

| Name | Role | Faction | Location | Attitude | Notes |
|------|------|---------|----------|----------|-------|
| | | | | | |

---

### <Name>
- **Role:** | **CR/Level:** | **Location:**
- **HP:** | **AC:** | **Attack:** | **Notable abilities:**
- **Demeanor:** | **Motivation:** | **Secret:**
- **Speech quirk:**
- **Attitude toward party:** neutral (scale: hostile → unfriendly → neutral → friendly → allied)
- **Faction:** <faction name or "independent">
- **Current goal:** <what this NPC is actively doing or trying to achieve right now — update each session>
- **Schedule:** <when and where they can typically be found>

### Personality
- **Trustworthy ↔ Deceptive:** <e.g. "Mostly trustworthy — lies only to protect family">
- **Ambitious ↔ Content:** <e.g. "Deeply ambitious — wants the guild master's seat">
- **Loyal ↔ Opportunistic:** <e.g. "Situationally loyal — will defect if the cost is high enough">
- **Brave ↔ Cowardly:** <e.g. "Brave in defence of others, cowardly about personal risk">

### Relationships
- **Knows:** <NPC name> — <context: how they know them and what they know>
- **Owes:** <NPC name> — <what the debt is and whether they've acknowledged it>
- **Hates:** <NPC name or entity> — <reason — is it personal, ideological, or inherited?>
- **Fears:** <NPC name or entity> — <reason>
- **Allied with:** <NPC name> — <nature of alliance — mutual benefit, loyalty, blackmail?>
*(fill only applicable entries — minimum 2 defined relationships per NPC)*

### Goal Tracker *(major NPCs and faction leaders only — anyone with a single, central, campaign-level goal, not every walk-on)*
*Structured, not just prose — mirrors `xp.py`'s loud "LEVEL UP PENDING" flag so a crossed threshold is never a silent state.md edit. Backed by `scripts/goals.py` and `<campaign>/goals.json` — see that script's own docstring for the CLI. Create the record with `goals.py add`, update progress with `goals.py set`/`achieve`, and mirror the current values here by hand so the prose stays readable without opening the JSON.*
- Hedef: <one sentence>
- İlerleme metriği: <a concrete number if numeric ("Fragment: 5/9"), otherwise a plain yes/no-answerable condition — never a vague "more worried">
- Eşik tepkileri:
  - Tehdit altında → <a pre-written move, phrased as an action, not a mood>
  - Engellendi → <a pre-written move>
  - Kalıcı kayıp → <a decisive, irreversible pre-written move>

### Known Facts — What They Actually Know & How
*The source of truth checked before writing this NPC's dialogue (see SKILL.md's "Narration principles" — mandatory source-of-knowledge check). A dated ledger, not a summary: one line per fact, naming the channel it came through. This NPC never references, hints at, or reacts to anything not listed here — no DM meta-knowledge, no other PC's private information, no fact from a scene this NPC wasn't in and wasn't told about.*
- <date/session> — <fact> — <channel: witnessed directly / told by NPC X / read in document Y / overheard / inferred from Z, and how confident they are in it>
*(seed this with whatever the NPC plausibly already knew before their first scene — background/role implies some baseline — then append as they learn more)*

### Notes
