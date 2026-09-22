# Encounter: The Vault (Clay Golem)

| Field | Value |
|-------|-------|
| **Location** | The Maker's Undoing, Wing 3, Room 20 (The Vault) |
| **Trigger** | The party enters Marek Stillwright's innermost chamber — his final, actual masterwork, and the reason he's dead. It has never left this room and has no one left to answer to except its last order: guard |
| **Encounter Type** | Boss fight — 1 Clay Golem, genuine solo named individual (per `two-player-scaling.md`'s solo-boss methodology) |
| **Difficulty** | CR 9 base (5,000 XP). Party's real combined nova ceiling at level 6 (`solo_burst_check.py --vs construct --full-nova`): **139.5** — base 133 HP sits just under that. Reinforced per the file's own instruction: HP margin + Legendary Resistance, since this is exactly the "genuine solo named boss" case |

---

## Enemies

| Name | Count | HP Each | AC | Speed | Initiative |
|------|-------|---------|-----|-------|------------|
| Clay Golem | 1 | **190** (base 133 + margin, real headroom above the party's 139.5 combined nova ceiling) | 14 | 20 ft. | -1 |

Stat block: SRD **Clay Golem** (CR 9), reinforced:
- **Immunities**: acid (heals it instead — Acid Absorption), poison, psychic; bludgeoning/piercing/slashing from nonmagical weapons (moot — both PCs' weapons/spells are magical or elemental).
- **Magic Resistance**: advantage on saves vs. spells — Ilvaneth's save-based spells (Thunderwave, Sleep, etc.) are less reliable here; her attack-roll spells (Fire Bolt, Scorching Ray, Magic Missile) are unaffected.
- **Multiattack**: 2 Slam, +8 to hit, 2d10+5 bludgeoning each. On a hit, target makes a DC 15 CON save or its **HP maximum** is reduced by the damage taken (permanent until *greater restoration* or similar) — real, escalating danger, not just HP loss.
- **Haste** (recharge 5-6): +2 AC, advantage on DEX saves, bonus-action Slam, until end of its next turn.
- **Berserk**: starts a turn at ≤60 HP, roll d6 — on a 6, attacks the nearest creature (or object) every turn until destroyed or fully healed.
- **Legendary Resistance (2/day)**: treats a failed save as a success instead.
- **Legendary Action (1/round, recharges at the start of its turn, usable at the end of another creature's turn)**: **Slam** — one Slam attack, same DC 15 max-HP-reduction rider on a hit.
- **No surprise** — an ever-vigilant guardian with one standing order; it doesn't sleep and can't be caught unaware regardless of the party's Stealth.

---

## Rewards

### Treasure
Ring of Mind Shielding (Marek's own masterwork) + ~400-600 gp (commission clients' unreturned advance payments, scattered through the room).

### XP
5,000 total ÷ 2 = 2,500 each.
