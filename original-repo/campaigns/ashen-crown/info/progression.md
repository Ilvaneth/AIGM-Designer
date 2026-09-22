# Progression — level 1 to 20

The campaign is planned as Chapter 1 (levels 1-10) and Chapter 2 (levels 11-20). Nothing existed to actually get them there. This is the pacing plan.

---

## Standing rule — level-up happens at the next long rest, not the instant XP crosses the threshold

**Decided at the table (2026-08-26).** `update_character.py`'s `xp_add` auto-advances the XP threshold and prints `** LEVEL UP **` the moment a character's total crosses it — that's correct as a *notification*, but the mechanical benefits (HP roll, new features, ASI/feat, new spells known/prepared, updated spell slot maximums) are **not applied until the party actually takes a long rest**, in-fiction. A level-up crossed mid-dungeon (e.g., from a boss kill) is banked, not immediately playable — the character keeps fighting at their current-level stats until they rest.

**Why**: matches how a long rest already resets/restores everything else (HP, slots, features) — leveling up folds into that same moment instead of interrupting a scene (leaving a dungeon, walking to camp) with a multi-question character-build conversation. It also means a level-up earned right before a second fight doesn't retroactively make that fight easier than it was actually played.

**Mechanically**: the XP number and the `** LEVEL UP **` flag can update immediately (that's just bookkeeping — track it, don't hide it from the player). But HP Maximum, class features, spell slots, and prepared spells on the character sheet stay at the *old* level's values until the next long rest, at which point the full level-up conversation (HP die roll, ASI/feat, new spells, etc.) happens as part of resolving that rest — same trigger point as `rest_check.py`.

---

## The two-player XP quirk

XP is divided among characters. **With two PCs, they level roughly twice as fast per encounter as a four-person party would** — the same goblin fight gives each of them 50 XP instead of 25.

This partly offsets the difficulty problem in `two-player-scaling.md`, but not fully: they level faster *and* every fight is harder. Expect them to feel under-levelled for their XP total. That's normal for this size party — don't "fix" it by throwing harder encounters at them.

## XP required (cumulative, per character)

| Level | XP | Level | XP |
|-------|-----|-------|-----|
| 2 | 300 | 12 | 100,000 |
| 3 | 900 | 13 | 120,000 |
| 4 | 2,700 | 14 | 140,000 |
| 5 | 6,500 | 15 | 165,000 |
| 6 | 14,000 | 16 | 195,000 |
| 7 | 23,000 | 17 | 225,000 |
| 8 | 34,000 | 18 | 265,000 |
| 9 | 48,000 | 19 | 305,000 |
| 10 | 64,000 | 20 | 355,000 |

**Current**: Ilvaneth **225 / 300**, Kriv **200 / 300** — level 1, close to level 2. Encounter XP is shared equally; roleplay awards are individual, which is why the two differ.

---

## Recommended: hybrid milestone

Pure XP to level 20 requires ~710,000 total encounter XP across the campaign. That is a great deal of bookkeeping and it pushes toward grinding fights, which is exactly the "chasing your tail" problem the table already objected to.

**Use milestone levelling for the main beats, and XP for the texture.**

- Award XP for combat as normal — it makes fights feel like they count
- **Also** level the party on story milestones regardless of XP total, when they've earned it
- Award **full XP for encounters resolved without combat** — bribed, bluffed, avoided, or turned. This party's whole character is getting what they want without a straight fight; never tax them for playing well
- **Award roleplay XP on top** — see `roleplay-and-xp.md`. Tier-scaled, max 3 instances per character per session. Never withheld as punishment.

## Chapter 1 milestones — levels 1-10

| Level | Earned by |
|-------|-----------|
| 2 | ✔ Nearly there — the ossuary job and the goblin ambush |
| 3 | Resolving the Thornwick lead; first real site cleared (Drowned Mill, Riverwatch, or similar) |
| 4 | First power-base holding taken, **or** the Weeping Tower |
| 5 | Sorrel's Hollow resolved — killed, cleared, or recruited |
| 6 | The Ash-Kilns taken; first faction learns the party exists as a player |
| 7 | Hollowmoor Barrows — they learn what the Crown actually costs |
| 8 | Karsgate: contact established with a faction at chapterhouse level |
| 9 | Second fragment acquired, by any means |
| 10 | **Chapter 1 climax** — Ashvale Necropolis. They walk out of it as a power, not a pair of thieves |

## Chapter 2 milestones — levels 11-20

| Level | Earned by |
|-------|-----------|
| 11 | Arrival at Emberhold; recognized at court |
| 12 | First capital power play — a house turned, an archive breached, a rival removed |
| 13 | The Concordat's role in the Emperor's death exposed or seized as leverage |
| 14 | Faction alignment locked: allied, subverted, or at war with one of the three |
| 15 | Into the Sundered Reach |
| 16 | Frostmere — the dragon's fragment |
| 17 | Kar Vaelth or the Bonewrights' Hall; the full truth about the last ash-king |
| 18 | All obtainable fragments gathered |
| 19 | Entry to the Grey Kingdom |
| 20 | The Ash Court — and the choice the whole campaign has been building toward |

---

## Session pacing

Rough targets, not a schedule:

| Tier | Levels | Sessions | Feel |
|------|--------|----------|------|
| 1 | 1-4 | 8-12 | Local, scrappy, survival-focused. Every gold piece matters |
| 2 | 5-10 | 12-18 | Regional power. Holdings, factions, real leverage |
| 3 | 11-16 | 12-18 | Kingdom-scale. Politics as dangerous as combat |
| 4 | 17-20 | 6-10 | Mythic. The Crown, the Grey Kingdom, the price |

**Total: roughly 40-60 sessions.** Sessions 1 and 2 are done.

---

## Level 2 — the concrete checklist

They are close. When it lands, apply exactly this (verified against the SRD):

**Ilvaneth — Wizard 1 → 2**
- HP: **8 → 14** (+4 average d6, rounded up, +2 CON)
- Hit dice: 2d6
- 1st-level spell slots: **2 → 3**
- Spells prepared: **4 → 5** (INT +3 + level 2)
- Spellbook: **+2 new spells** of her choice, 1st or 2nd level as available
- **Arcane Tradition** — her goal points at Necromancy or Abjuration; hers to choose
- Proficiency bonus unchanged (+2)

**Kriv — Fighter 1 → 2**
- HP: **12 → 20** (+6 average d10, rounded up, +2 CON)
- Hit dice: 2d10
- **Action Surge (1/short rest)** — one extra action on his turn. For a two-character party this is a genuinely large gain; make sure it isn't forgotten
- Proficiency bonus unchanged (+2)

> Found in testing: the notes below jumped from Kriv's level 3 straight to level 4 and never mentioned Action Surge — the very next thing that happens to him.

## Levelling the two PCs

- **Ilvaneth (Wizard)**: level 2 gives Arcane Tradition. Her stated goal points hard at **Necromancy** (raising and commanding the dead, and the School's `Undead Thralls`) or **Abjuration** (survival, wards, and the ward-breaking she's already doing). Let her choose, but note that Necromancy is thematically the campaign's own spine.
  - Spellbook growth: 2 new spells per level, plus anything she transcribes from found books. **Harn's Spellbook at the Weeping Tower is a deliberate windfall** — see `treasure.md`.
- **Kriv (Fighter)**: level 3 gives Martial Archetype. **Champion** for simplicity, **Battle Master** for tactical depth — the latter helps a two-person party considerably (Trip Attack and Menacing Attack cover for a missing third character).
  - Level 4 ASI: STR 17→18 is the obvious pick.

## Ascension stages

Both PCs are on one-way transformation tracks driven by fragment acquisition, not level — but with level floors so plot luck can't outrun the campaign. See `ascension-tracks.md`.

| Stage | Fragments | Level floor | Kriv | Ilvaneth |
|-------|-----------|-------------|------|----------|
| 0 | 1 (**now**) | — | Runs warm | Unwelcome dreams |
| 1 | 2 | 7 | Scales, darkvision | The dead notice her |
| 2 | 3 | 11 | Fire immunity, claws | Stops eating, drinking, breathing |
| 3 | 4 | 15 | Frightful presence, truesight | Stops aging; survives 0 HP |
| 4 | 5+ | 17 | **Wings** | Cannot be permanently killed |

These are on top of normal class progression, and they are the reason a two-character party can survive tier 3-4 content. Do not hand them out early to compensate for difficulty — fix difficulty with `two-player-scaling.md` and companions instead.

## Companions

Per `two-player-scaling.md`, this party needs help. If they recruit a Sorrel's Hollow deserter or hire muscle, level that companion **one level behind the party** and use sidekick-style progression. Don't let a companion outshine either PC — they're insurance, not a third protagonist.

## Awarded so far

### Combat / milestone XP

| Source | Ilvaneth | Kriv | Note |
|--------|----------|------|------|
| Session 1 — the ossuary job | 100 | 100 | Milestone award |
| Session 2 — goblin ambush (road to Thornwick) | 50 | 50 | 2 Goblins, 100 raw ÷ 2 |
| Session 2 — Sorrel's Hollow toll point | 50 | 50 | 4 Deserters, 100 raw ÷ 2 |
| Session 2 — Sorrel's Hollow trail ambush | 50 | 50 | 4 Deserters, 100 raw ÷ 2 |
| Session 2 — Sorrel's Hollow camp assault | 388 | 387 | 3 Deserters + Roskel (Veteran, CR 3), 775 raw ÷ 2 |
| **Combat/milestone subtotal** | **638** | **637** | |

### Roleplay XP (`roleplay-and-xp.md`, max 3 instances/character/session)

| Character | Instance | XP |
|-----------|----------|-----|
| Ilvaneth | Conning the Wend family — Neutral Evil played straight | 25 |
| Ilvaneth | Ash on the ward plate — solved the ossuary seal in-fiction, no combat | 25 |
| Ilvaneth | Comprehend Languages on the inscription — prepared for a purpose, then used | 25 |
| Kriv | Backing the con without hesitation — the bond played as reflex | 25 |
| Kriv | Comprehend Languages on the inscription (shared instance) | 25 |
| Kriv | Kept his word to Hesta, followed through straight | 20 |
| **Roleplay subtotal** | Ilvaneth 75 · Kriv 70 | *(both at the 3-instance cap for session 2)* |

### Running total

| | Ilvaneth | Kriv |
|---|----------|------|
| **Total XP** | **713** | **707** |
| **To level 3 (900)** | 187 to go | 193 to go |

*Both reached level 2 partway through the camp assault award; already applied to their character sheets.*
