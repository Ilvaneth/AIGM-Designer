# Encounter: The Wayside Grave

| Field | Value |
|-------|-------|
| **Location** | An unmarked track east of Harrowgate, off every road — the day's ride toward Shestendeliath Hold, day 51 |
| **Trigger** | Travel roll — The Thornlands table, result 9 (Undead) |
| **Encounter Type** | Combat — solo, daytime |
| **Difficulty** | Light, HP-corrected (see DM Notes) — travel texture, not a set piece; thematically foreshadows the Hold's own oath-bound dead |

---

## Description / Read-Aloud Text

> *The track has thinned to a deer path. A weathered grave marker leans out of the bracken beside it — no name cut into it, just a chipped sigil too worn to read. As the horses draw level with it, the air around the stone goes cold.*

---

## Enemies

| Name | Count | HP Each | AC | Speed | Initiative |
|------|-------|---------|-----|-------|------------|
| Specter | 1 | **48** (corrected from base SRD 22 — see DM Notes) | 12 | 0 ft., fly 50 ft. (hover) | +2 |

Stat block: SRD **Specter** (CR 1, 200 XP), HP raised. Incorporeal Movement. Sunlight Sensitivity — **daytime encounter, disadvantage on its attack rolls and on sight-based Perception**. Life Drain: +4 to hit, reach 5 ft., 10 (3d6) necrotic, DC 10 CON save or max HP reduced by the damage taken (until a long rest).

---

## Tactics

**No surprise either way** — it rises into plain view as the party passes, not from hiding. Roll initiative for everyone per `combat-rules.md`.

**If it drops below half HP**: doesn't flee (mindless-bound, not tactical) — keeps attacking whoever's nearest until destroyed.

**Morale**: none — fights to destruction.

---

## Rewards

### Loot

None — no body, no possessions. Destroying it just ends it.

### XP

200 raw ÷ 2 = **100 XP each**.

---

## DM Notes

**Corrected live, mid-fight, session 9 — see `bug-log.md`, `combat-geometry`.** Originally built at the base SRD Specter's 22 HP, reasoning "daytime + solo keeps this light." That skipped `two-player-scaling.md`'s own solo-HP-sizing technique ("size HP against the party's actual burst, not the CR table") — 22 HP is below even Kriv's single-PC floor (25/round from the Barrow-King's Blade alone, per `solo_burst_check.py`), meaning he could end the fight before it got a single action. Caught immediately by the DM before any damage was dealt. Raised to 48 HP (comfortably above the 37.5 floor `solo_burst_check.py --check-hp` recommends) via `combat_status.py --update '{"name": "Specter", "hp_max": 48}'` — the patch key didn't exist yet either, added in the same fix. Daytime and solo still keep this well short of a real boss; the point is texture and a thematic echo (an oath-broken dead thing, same category as what's waiting at the Hold) that now actually survives long enough to land at least one Life Drain before going down, rather than being a complete non-event.
