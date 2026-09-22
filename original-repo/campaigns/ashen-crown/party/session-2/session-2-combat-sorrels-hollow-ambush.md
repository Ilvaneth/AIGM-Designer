# Combat Log: The Trail Ambush (Sorrel's Hollow) — Session 2

**Encounter**: Relief group ambush on the goat trail between the toll point and the main deserter camp
**Date**: 2026-08-25
**Session**: 2
**Outcome**: Victory — 3 deserters killed, 1 captured (interrogated, then killed). No damage taken. Camp still unaware.
**XP Awarded**: 100 (50 per character)

---

## Combatants

| Name | Side | HP | AC | Notes |
|------|------|----|----|-------|
| Ilvaneth Duskmere | PC | 8/8 | 17 | Wizard 1, cantrips only (both 1st-level slots already spent) |
| Kriv Shestendeliath | PC | 12/12 | 16 | Fighter 1, Chain Mail, Greataxe, Handaxe |
| Deserter 1 | Enemy | 11/11 | 12 | Front of the line, carried a lantern |
| Deserter 2 | Enemy | 11/11 | 12 | Second in line |
| Deserter 3 | Enemy | 11/11 | 12 | Third in line — surrendered at 1 HP, later killed after interrogation |
| Deserter 4 | Enemy | 11/11 | 12 | Rear of the line — fled, run down and killed |

---

## Setup

After clearing the toll point, the party hid the four bodies, tied off their horses, and moved to scout the trail rather than report back to Hesta immediately. They found a game trail branching off the main road — roughly 3 ft wide, dense trees either side forcing single file — and set an ambush at dusk: Kriv concealed among the trees partway up the trail, Ilvaneth hidden in a gap between two beech trunks at the trail's mouth. Stealth: Kriv raw 13 (+1 = 14), Ilvaneth raw 19 (+4 = 23), both clearing the deserters' passive Perception of 10.

A random check (`roll.py`) determined a 4-person relief group came down the trail before dark, traveling single file with a lantern-bearer in front.

**Surprise**: One side surprised — all four deserters were unaware and surprised for their first turn.

---

## Initiative

| Roll | Name |
|------|------|
| 22 | Ilvaneth Duskmere |
| 20 | Deserter 1 |
| 19 | Deserter 2 |
| 11 | Kriv Shestendeliath |
| 10 | Deserter 3 |
| 3 | Deserter 4 |

---

## Round 1

**► Ilvaneth Duskmere** — **Fire Bolt** at Deserter 1: **15+5 = 20** vs AC 12 — **hit**. Damage: **4 fire**. Deserter 1: **11 → 7/11 HP**.

**► Deserter 1** — Surprised. No action.

**► Deserter 2** — Surprised. No action.

**► Kriv Shestendeliath** — Attacks Deserter 1 with Greataxe: **12+5 = 17** vs AC 12 — **hit**. Damage: **8**. Deserter 1: **7 → 0/11 HP — dead**.

**► Deserter 3** — Surprised. No action.

**► Deserter 4** — Surprised. No action.

---

*Combat Status — End of Round 1*

    == COMBAT: Round 1 ==
    INITIATIVE        HP          AC   STATUS
    ─────────────────────────────────────────
      Ilvaneth (PC)    8/8        17   —
      Kriv (PC)        12/12      16   —
      Deserter 1       0/11       12   DEAD
      Deserter 2       11/11      12   —
      Deserter 3       11/11      12   —
      Deserter 4       11/11      12   —

---

## Round 2

**► Ilvaneth Duskmere** — **Fire Bolt** at Deserter 2: **13+5 = 18** vs AC 12 — **hit**. Damage: **9 fire**. Deserter 2: **11 → 2/11 HP**.

**► Deserter 2** — No longer surprised. Panics, tries to flee back up the trail without disengaging — provokes an Opportunity Attack.

**► Kriv Shestendeliath (Opportunity Attack)** — **18+5 = 23** vs AC 12 — **hit**. Damage: **12**. Deserter 2: **2 → 0/11 HP — dead**.

**► Kriv Shestendeliath (turn)** — Attacks Deserter 3 with Greataxe: **19+5 = 24** vs AC 12 — **hit**. Damage reported as **10**; ruled at the table to leave Deserter 3 at **1/11 HP** rather than the strictly-correct 13 (raw 10 + STR 3) that would have killed him outright — a deliberate table call to keep the surrender beat that followed. *(Correct math for damage going forward: DM adds Kriv's +3 STR to reported raw damage.)*

**► Deserter 3** — At 1 HP, **surrenders** — drops weapon, begs for mercy. Kriv accepts.

**► Deserter 4** — No longer surprised. Breaks and flees back toward the camp, using full movement (30 ft). No reaction available to stop him (Kriv's reaction already spent this round; Ilvaneth's turn already passed).

---

*Combat Status — End of Round 2*

    == COMBAT: Round 2 ==
    INITIATIVE        HP          AC   STATUS
    ─────────────────────────────────────────
      Ilvaneth (PC)    8/8        17   —
      Kriv (PC)        12/12      16   —
      Deserter 1       0/11       12   DEAD
      Deserter 2       0/11       12   DEAD
      Deserter 3       1/11       12   SURRENDERED
      Deserter 4       11/11      12   FLEEING

---

## Round 3

**► Ilvaneth Duskmere** — Moves up the trail to reacquire sight of the fleeing Deserter 4 (near the edge of her 60 ft darkvision, target partly obscured by brush at a bend — attack at disadvantage). **Fire Bolt**: raw 15 / 16, lower (15) used → **15+5 = 20** vs AC 12 — **hit**. Damage: **10 fire**. Deserter 4: **11 → 1/11 HP**, still fleeing (limping).

**► Kriv Shestendeliath** — Moves 30 ft to the trail's bend, throws a **Handaxe** at long range (disadvantage): raw 10 / 13, lower (10) used → **10+5 = 15** vs AC 12 — **hit**. Damage: **4+3 = 7**. Deserter 4: **1 → 0/11 HP — dead**.

---

## Combat Over

Deserters 1, 2, and 4 dead. Deserter 3 alive, surrendered, at 1 HP. Neither PC took any damage. No alarm reached the camp.

**Aftermath**: Kriv interrogated Deserter 3 (Intimidation: raw 18+4 = 22 vs DC 12 — clean success). The captive gave up the camp's location (~¼ mile down the trail, unfortified clearing), Sergeant **Roskel**'s name and that he "once served a noble house," the night watch pattern (2 people, one at the fire, one at the trail mouth), remaining headcount (~4-5, down from ~12), and low morale. Kriv then killed him. Ilvaneth looted and concealed all the bodies (branches and leaves) while the interrogation ran.

---

## Resources Expended

| Character | Resource | Detail |
|-----------|----------|--------|
| Ilvaneth | — | Cantrips only; no spell slots available this fight |
| Kriv | — | Second Wind and Breath Weapon unused |

---

## Key Moments

1. Ilvaneth's opening Fire Bolt and Kriv's follow-up killed the lead deserter before the rest could react.
2. A failed flight attempt (Deserter 2) turned into a clean opportunity-attack kill.
3. Deserter 3's surrender, accepted rather than finished off — a table ruling that stood even after a damage-math correction would have killed him.
4. Deserter 4 nearly escaped to warn the camp — no reaction was available to stop him mid-flight, and he was only run down by both PCs closing distance and taking difficult (disadvantage) shots the following round.
5. The captured Deserter 3 gave the party their first real intelligence on the camp: numbers, layout, watch pattern, and Sergeant Roskel's name.

---

## Final Party Status

| Name | HP | Spell Slots | Resources |
|------|----|-------------|-----------|
| Ilvaneth Duskmere | 8/8 | 1st: 0/2 (restored to 2/2 after the long rest that followed) | Arcane Recovery 1/1 (unused) |
| Kriv Shestendeliath | 12/12 | — | Second Wind 1/1, Breath Weapon 1/1 (both unused) |

---

## XP

| Source | XP |
|--------|----|
| Deserter ×4 | 100 |
| **Total** | **100** |
| **Per character** | **50** |

Both PCs crossed the level-2 threshold from this award (Ilvaneth 325/300, Kriv 300/300) — level-up not yet applied.
