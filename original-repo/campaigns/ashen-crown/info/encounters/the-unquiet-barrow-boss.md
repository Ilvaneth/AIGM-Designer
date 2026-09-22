# Encounter: The Center — The Barrow's True Guardian

| Field | Value |
|-------|-------|
| **Location** | The Unquiet Barrow, Room 18 — the boss, per `two-player-scaling.md`'s solo-boss methodology |
| **Trigger** | Reaching the barrow's true center — the treasure this whole site was built to protect |
| **Encounter Type** | Combat — solo boss, genuine named individual. `solo_burst_check.py --vs elemental --full-nova` computed a combined party nova ceiling of **139.5** (Kriv alone 108.0 w/ Action Surge+maneuvers+GWM, Ilvaneth 31.5 w/ Wand of Magic Missiles) — this boss is sized with real margin above that, plus Legendary Resistance/Actions per the file's own guidance for a genuine solo named boss. |
| **Difficulty** | Reinforced far past base Xorn CR5 — intentional, this is the whole site's payoff fight. |

---

## Enemy

**The Barrow-Warden** — an Elder Xorn, the barrow's true, original guardian (distinct from the two wandering Xorn already killed in Rooms 3 and 7).

| Stat | Value |
|------|-------|
| HP | **240** (reinforced — real margin above the 139.5 combined nova ceiling) |
| AC | **20** (natural armor, +1 over base Xorn) |
| Speed | 20 ft., burrow 20 ft. |
| STR/DEX/CON/INT/WIS/CHA | 17(+3) / 10(+0) / 22(+6) / 11(+0) / 10(+0) / 11(+0) |
| Senses | darkvision 60 ft., tremorsense 60 ft., passive Perception 16 |
| Resistances | piercing/slashing from nonmagical weapons that aren't adamantine |

**Multiattack.** 3 Claw (+6, 1d6+3 slashing) + 1 Bite (+6, 3d6+3 piercing).

**Legendary Resistance (2/day).** If the Barrow-Warden fails a saving throw, it can choose to succeed instead.

**Legendary Actions (3/round, regains at start of its turn; only one at a time, only at the end of another creature's turn).**
- **Claw (Costs 1 Action).** One claw attack, +6, 1d6+3 slashing.
- **Reposition (Costs 1 Action).** Burrows up to half its speed without provoking opportunity attacks.
- **Tremor Pulse (Costs 2 Actions).** Each creature within 10 ft must make a DC 15 Dexterity saving throw or take 2d8 force damage and be knocked prone.

---

## Rewards

### XP
Elder Xorn treated as CR 9 equivalent for this fight (5,000 XP) — reflects the Legendary Resistance/Actions reinforcement, per `two-player-scaling.md`'s solo-boss guidance rather than base CR5.

### Treasure
The single real prize this whole site was built to protect — DM's choice, substantial enough to justify the delve (see `the-unquiet-barrow.md` Room 18).
