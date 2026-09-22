# Combat Log: The Barrow Road, Night 1 — Session 15

**Encounter**: 1 Ghast + 2 Wight (Thornlands, Late-tier travel roll, Undead escalated)
**Date**: 2026-09-04
**Session**: 15
**Outcome**: Victory — all three enemies killed, no PC downed. Ilvaneth dropped to 10/45 HP (22%) — the closest call this fight produced.
**XP Awarded**: 1,850 total ÷ 2 = 925 each

---

## Combatants

| Name | Side | HP | AC | Notes |
|------|------|----|----|-------|
| Ilvaneth Duskmere | PC | 45/45 | 18 | Wizard 6, School of Necromancy |
| Kriv Shestendeliath | PC | 74/74 | 20 | Fighter 6, Battle Master |
| Ghast | Enemy | 36/36 | 13 | CR 2 |
| Wight A | Enemy | 45/45 | 14 | CR 3 |
| Wight B | Enemy | 45/45 | 14 | CR 3 |

---

## Setup

Night 1 of the journey from Shestendeliath Hold toward The Unquiet Barrow (following Orna Threk's map). The party made camp at dusk; Ilvaneth had not yet cast Tiny Hut. A Thornlands Late-tier travel roll produced Combat → Undead, escalated → 1 Ghast + 2 Wight (d4 sub-roll). Both Wights (Stealth 21) and the Ghast (Stealth 22) beat both PCs' passive Perception (Ilvaneth 15, Kriv 11) while the party was occupied setting up camp.

**Surprise**: Both PCs surprised — the undead trio closed in undetected and acted freely in round 1 while Ilvaneth and Kriv skipped their first turns.

---

## Initiative

| Roll | Name |
|------|------|
| 22 | Ghast |
| 22 | Ilvaneth Duskmere |
| 14 | Wight B |
| 14 | Kriv Shestendeliath |
| 7 | Wight A |

---

## Round 1

**► Ghast** — Claws at Kriv: **22** vs AC 20 — **Hit**. 5 slashing damage. *Kriv at 69/74 HP.* Kriv's DC 10 CON save vs. paralysis: **18** (raw 15 +3 CON) — succeeded, no paralysis.

**► Ilvaneth** — Surprised, no action.

**► Wight B** — Life Drain at Ilvaneth: **9** vs AC 18 — Miss. Longsword at Ilvaneth: **24 (natural 20) — Critical**. 18 slashing damage. *Ilvaneth at 27/45 HP.*

**► Kriv** — Surprised, no action.

**► Wight A** — Life Drain at Ilvaneth: **10** vs AC 18 — Miss. Longsword at Ilvaneth: **19** vs AC 18 — Hit. 8 slashing damage. *Ilvaneth at 19/45 HP.*

---

*Combat Status — End of Round 1*

    == COMBAT: Round 1 ==
    INITIATIVE        HP          AC   STATUS
    ─────────────────────────────────────────
      Ghast (Enemy)    36/36        13   —
      Ilvaneth (PC)    19/45        18   —
      Wight B (Enemy)  45/45        14   —
      Kriv (PC)        69/74        20   —
      Wight A (Enemy)  45/45        14   —

---

## Round 2 — correction mid-fight

A DM/player exchange caught that Kriv's Constitution save had been resolved against his bare ability modifier (+3) instead of his real, proficient Saving Throws modifier (+6) — see `bug-log.md`, 2026-09-04, `combat-geometry`. Round 1's first Ghast save was unaffected (15+6 still passes). Round 2's Ghast Claws save below, and everything downstream of it, was retroactively corrected before play continued; `character_modifier.py` was extended the same turn to cover saving-throw lookups so this can't recur the same way.

**► Ghast** — Claws at Kriv: **22** vs AC 20 — Hit. 12 slashing damage. *Kriv at 57/74 HP.* Kriv's DC 10 CON save vs. paralysis: raw 5 **+6** (corrected) = **11** — succeeded, no paralysis (originally misresolved as a failure, corrected live).

**► Ilvaneth** — Misty Step (bonus action, 30 ft) to open distance, then **Mirror Image** (action, 2nd-level slot): 3 illusory duplicates active.

**► Wight B** — pressed the attack on Kriv (adjacent). Life Drain: **24 (natural 20) — Critical**. 10 necrotic damage. *Kriv at 47/74 HP.* Kriv's DC 13 CON save vs. max HP reduction: raw 9 +6 = **15** — succeeded, no reduction. Longsword: **21** vs AC 20 — Hit. 4 slashing damage. *Kriv at 43/74 HP.*

**► Kriv** — killed the Ghast (see below), using his full turn.

Precision Attack (1 superiority die) + GWM: raw 15, +4 (GWM-adjusted) +5 (superiority die) = **24** vs AC 13 — Hit.
Goading Attack (1 superiority die) + GWM: raw **20 (natural 20) — Critical**.
Plain + GWM: raw 17, +4 = **21** vs AC 13 — Hit.
Plain + GWM: raw 3, +4 = **7** vs AC 13 — Miss (target already dead).

Attack 1 damage: 1d12+1d8+16 = 3+4+16 = **23**. *Ghast 36→13 HP.*
Attack 2 (crit) damage: 2d12+4d8+16 (base dice doubled + Goading Attack's own superiority die, also part of the damage roll and also doubled — caught and corrected mid-roll, see `bug-log.md`) = (4+9)+(5+8+8+8)+16 = 13+29+16 = **58**. *Ghast 13→0 HP — dead.*

**► Wight A** — switched to Longbow at range against Ilvaneth (out of melee reach after Misty Step).
Mirror Image check 1: **18** (6+ redirects, 3 duplicates) → targets a duplicate. Longbow: **13** vs AC 14 — Miss.
Mirror Image check 2: **1** (no redirect) → targets Ilvaneth directly. Longbow: **19** vs AC 18 — Hit. 9 piercing damage. *Ilvaneth at 10/45 HP.*

---

*Combat Status — End of Round 2*

    == COMBAT: Round 2 ==
    INITIATIVE        HP          AC   STATUS
    ─────────────────────────────────────────
      Ilvaneth (PC)    10/45        18   Mirror Image (3)
      Wight B (Enemy)  45/45        14   —
      Kriv (PC)        43/74        20   —
      Wight A (Enemy)  45/45        14   —
      Ghast (Enemy)     0/36        13   DEAD

---

## Round 3

**► Ilvaneth** — **Fireball** (3rd-level slot), centered to catch both Wights — Kriv, adjacent to Wight B in melee, was caught too (confirmed with the DM before casting). DC 15 DEX save.
Wight A: **6** — failed, full damage.
Wight B: **17** — succeeded, half damage.
Kriv: raw 14 +1 = **15** — succeeded, half damage, further halved by fire resistance (Draconic Ancestry).
Damage: 8d6 = 5+6+3+3+4+5+6+6 = **38**.
Wight A: 38 (full). *45→7 HP.*
Wight B: 19 (half). *45→26 HP.*
Kriv: 19 half → 9 (resistance, rounded down). *43→34 HP.*

**► Wight B** — broke off from Kriv to close on the wounded Ilvaneth, provoking an opportunity attack.

**Kriv (opportunity attack)** — Precision Attack (1 superiority die) + GWM: raw 7, +4 (GWM) +7 (superiority die) = **18** vs AC 14 — Hit. Damage: 1d12+1d8+16 = 3+7+16 = **26**. Wight B had exactly 26 HP — **dead**.

**► Kriv** — normal turn, 2 attacks, no maneuver: raw 3, +9 = **12** vs AC 14 — Miss. Raw 3, +9 = **12** vs AC 14 — Miss.

**► Wight A** — continued Longbow at Ilvaneth (7/45 HP).
Mirror Image check 1: **16** → redirects. Longbow: **10** vs AC 14 — Miss.
Mirror Image check 2: **7** → redirects. Longbow: **21** vs AC 14 — Hit, duplicate destroyed. *2 duplicates remain. Ilvaneth undamaged.*

---

*Combat Status — End of Round 3*

    == COMBAT: Round 3 ==
    INITIATIVE        HP          AC   STATUS
    ─────────────────────────────────────────
      Ilvaneth (PC)    10/45        18   Mirror Image (2)
      Kriv (PC)        34/74        20   —
      Wight A (Enemy)   7/45        14   —
      Ghast (Enemy)      0/36        13   DEAD
      Wight B (Enemy)     0/45        14   DEAD

---

## Round 4

**► Ilvaneth** — Wand of Magic Missiles (1 charge): 3 darts, auto-hit, no save. Damage: 3×(1d4+1) = (2+1)+(4+1)+(1+1) = 3+5+2 = **10**. Wight A had 7 HP — **dead**.

---

## Combat Over

All three enemies dead. Ilvaneth 10/45 HP, Kriv 34/74 HP going into the aftermath. Long rest taken the following morning (day 67) restored both to full.

---

## Resources Expended

| Character | Resource | Detail |
|-----------|----------|--------|
| Ilvaneth | 2nd-level slot ×2 | Misty Step, Mirror Image |
| Ilvaneth | 3rd-level slot ×1 | Fireball |
| Ilvaneth | Wand of Magic Missiles, 1 charge | Killing blow on Wight A |
| Kriv | Action Surge (1/1) | The 4-attack Ghast-killing round |
| Kriv | Superiority Dice ×3 (of 4) | Precision Attack ×2, Goading Attack ×1 |

---

## Key Moments

1. The undead trio's full surprise on both PCs, mid-camp — the danger ran the other way this time, favoring the enemy's opening round rather than the party's usual nova.
2. A live mid-combat correction: Kriv's Constitution save modifier was misread from the Ability Scores table instead of the Saving Throws table, wrongly applying Paralyzed for most of round 2 before the player caught it and the turn was replayed honestly.
3. Kriv's Action Surge nova (Precision Attack, Goading Attack, 2 plain attacks, GWM throughout) one-shot the Ghast in round 2 — a natural 20 crit alone dealt 58 damage after the Goading Attack superiority-die-doubling correction.
4. Ilvaneth's Fireball, deliberately cast to catch both Wights with Kriv accepted as splash damage — brought Wight A to the brink and set up its death two rounds later.
5. Wight B's tactical pivot toward the wounded Ilvaneth cost it an opportunity attack from Kriv, which killed it outright at exactly its remaining HP.

---

## Final Party Status

| Name | HP | Spell Slots | Resources |
|------|----|-------------|-----------|
| Ilvaneth Duskmere | 45/45 (post-rest) | Full (post-rest) | Wand: 6/7 charges |
| Kriv Shestendeliath | 74/74 (post-rest) | — | Full (post-rest) |
