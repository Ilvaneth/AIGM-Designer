# Combat Log: The Gauntlet — Session 13

**Encounter**: The Gauntlet (The Maker's Undoing, Wing 1, Room 10)
**Date**: 2026-09-03
**Session**: 13
**Outcome**: Victory — both Manticores killed, no surprise on either side
**XP Awarded**: 1,400 total (700 each)

---

## Combatants

| Name | Side | HP | AC | Notes |
|------|------|----|----|-------|
| Ilvaneth Duskmere | PC | 38/38 | 17 | Wizard 5 |
| Kriv Shestendeliath | PC | 47/64 (end) | 20 | Fighter 5 |
| Manticore (Alpha) | Enemy | 84/84 → 0 (dead) | 14 | Sergeant-tier bump (68 base +16) |
| Manticore | Enemy | 68/68 → 0 (dead) | 14 | Standard |

---

## Setup

Following a blood trail left by the wounded Manticore that fled Room 9, the party reached Room 10 — a wide hall with stalactites and a thin shaft of daylight from above. The alpha pair stood alert, warned by their fleeing kin. Kriv's Stealth (7+1=8) was beaten by an alerted Perception check (advantage, 14); Ilvaneth's (19+4=23) held. **No surprise on either Manticore** — a direct, earned consequence of not pursuing Room 9's survivor.

**Surprise**: none. Full participation from round 1 on both sides.

---

## Initiative

| Roll | Name |
|------|------|
| 20 | Manticore |
| 19 | Manticore (Alpha) |
| 18 | Ilvaneth Duskmere |
| 10 | Kriv Shestendeliath |

---

## Round 1

**► Manticore** — 3 Tail Spike at Kriv (range): **16, 11, 12** — all vs AC 20, all **miss**.

**► Manticore (Alpha)** — 3 Tail Spike at Kriv: **11, 15** (miss), **23** (**Hit**) — damage 7+3 = **10 piercing**. *Kriv at 47/64 HP.*

**► Ilvaneth Duskmere** — Fireball, both Manticores caught in the 20-ft radius (positioned close together). Damage: 8d6 (6,4,5,4,6,3,6,1) = **35 fire** to each.
- Manticore DEX save: **11** vs DC 15 — **Fail**, full damage. *33/68 HP.*
- Manticore (Alpha) DEX save: **6** vs DC 15 — **Fail**, full damage. *49/84 HP.*

**► Kriv Shestendeliath** — The Barrow-King's Blade (+9) at the Alpha, Action Surge for 4 attacks:
- Attack 1: **3+9 = 12** vs AC 14 — **Miss**.
- Attack 2 (Goading, natural 20 — automatic crit): 2d12 (3,6) +6 = 15, + Superiority Die 2d8 (8,5) = 13. Total **28 radiant**.
- Action Surge, Attack 1: **13+9 = 22** vs AC 14 — **Hit**. Damage: 4+6 = **10 radiant**.
- Action Surge, Attack 2: **8+9 = 17** vs AC 14 — **Hit**. Damage: 5+6 = **11 radiant**.
Total: **49 radiant damage**. *Manticore (Alpha) at 0/84 HP — **DEAD**.*

*(DM correction, mid-round: `active_index` had drifted — the tracker was still pointing at Ilvaneth's turn after Kriv's had already fully resolved, because the turn-advance call was skipped. Corrected in `combat_state.json` before continuing. See bug-log.md.)*

---

*Combat Status — End of Round 1*

    == COMBAT: Round 2 ==
    INITIATIVE        HP          AC   STATUS
    ─────────────────────────────────────────
    ► Manticore (Enemy)  33/68      14   —
      Ilvaneth Duskmere (PC) 38/38  17   —
      Kriv Shestendeliath (PC) 47/64 20  —
      Manticore (Alpha) (Enemy) 0/84 14  DEAD

---

## Round 2

**► Manticore** — Multiattack (Bite + 2 Claw) at Kriv: **12, 11, 16** — all vs AC 20, all **miss**.

**► Ilvaneth Duskmere** — Fire Bolt at the Manticore: **9+7 = 16** vs AC 14 — **Hit**. Damage: 7+8 = **15 fire**. *Manticore at 18/68 HP.*

**► Kriv Shestendeliath** — The Barrow-King's Blade (+9) at the Manticore:
- Attack 1: **8+9 = 17** vs AC 14 — **Hit**. Damage: 3+6 = **9 radiant**.
- Attack 2: **12+9 = 21** vs AC 14 — **Hit**. Damage: 6+6 = **12 radiant**.
Total: **21 radiant damage**. *Manticore at 0/68 HP — **DEAD**.*

---

## Combat Over

Both Manticores dead. The Room 9 survivor remains loose elsewhere in the dungeon, unaddressed.

---

## Resources Expended

| Character | Resource | Detail |
|-----------|----------|--------|
| Ilvaneth | Fireball | 3rd-level spell slot (now 2/2 → 1/2) |
| Ilvaneth | Fire Bolt | Cantrip, no cost |
| Kriv | Action Surge ×1 | Consumed, not yet restored |
| Kriv | Superiority Die ×1 | Round 1's Goading Attack |

---

## Key Moments

1. Both Manticores denied surprise this time — a direct consequence of leaving Room 9's wounded survivor alive and unpursued.
2. Ilvaneth's Fireball catching both Manticores in one blast, landing full damage on each (both failed their DEX saves) — 35 damage apiece from a single spell.
3. Kriv's natural-20 Goading Attack plus a full Action Surge round (49 total damage) dropping the Alpha from 49 HP to exactly 0 in one turn.
4. A real tracker-state correction mid-fight (`active_index` drift) — caught and fixed without losing track of the actual combat state.
5. Both PCs closing in on level 6 by the fight's end (13,438 / 14,000 and 13,307 / 14,000 XP).

---

## Final Party Status

| Name | HP | Spell Slots | Resources |
|------|----|-------------|-----------|
| Ilvaneth Duskmere | 38/38 | 1st: 3/4 · 2nd: 1/3 · 3rd: 1/2 | — |
| Kriv Shestendeliath | 47/64 | — | Action Surge 0/1, Superiority Dice 2/4 |

---

## XP

| Source | XP |
|--------|-----|
| Manticore (Alpha, CR 3) | 700 |
| Manticore (CR 3) | 700 |
| **Total** | **1,400** |
| **Per character** | **700** |
