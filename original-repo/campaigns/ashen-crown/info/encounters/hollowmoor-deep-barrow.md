# Encounter: Hollowmoor Barrows — The Deep Barrow (The Warden)

| Field | Value |
|-------|-------|
| **Location** | The deep barrow at Hollowmoor's center, behind the carved stone door |
| **Trigger** | Party opens the deep barrow door — fully warned in advance (inscription translated, Sefwyn's warning, a dead intruder's remains at the threshold) |
| **Encounter Type** | Social-first is possible — the Warden is not mindless. Combat only if it goes that way |
| **Difficulty** | Deadly on its own for this level-3 two-player party — 700 raw × 1.5 (single monster, bumped for 2 PCs) = **1,050 adjusted**, above the 800 Deadly threshold. See `two-player-scaling.md`. **Do not run as a forced fight** — the party has already been telegraphed clearly and is choosing to open this door with full information. |

---

## Who it is

The last ash-king assembled the Crown and came back wrong. The people who loved him — his own household guard — were the ones who put him down, and then stayed to make sure no one else made the same mistake. **The Warden was one of them.** Centuries of guarding turned that guard into a Wight: not mindless, not evil in the cartoonish sense, but bound to a vow that has outlasted every reason it was made.

**Voice**: hollow, formal, tired — a soldier reciting an order they no longer believe in but will not break.

**What it wants**: to keep the vow. No one leaves this barrow carrying the idea that the Crown can be completed safely. It would genuinely rather the party simply understood and left than have to fight — but it will fight, and it will not lose on purpose.

## Stat block

**1 Wight** (SRD, CR 3, 700 XP) — run as written, AC 14, HP 45, Multiattack (2 longsword or 2 longbow, or Life Drain in place of one). See `srd_lookup.py monster "Wight"` for the full block. Sunlight Sensitivity is irrelevant underground.

## Enemies

| Name | Count | HP Each | AC | Speed | Initiative |
|------|-------|---------|-----|-------|------------|
| The Warden | 1 | 45 | 14 | 30 ft. | +2 |

### Attack Details

| Enemy | Attack Name | Attack Bonus | Damage | Type | Special |
|-------|------------|--------------|--------|------|---------|
| The Warden | Longsword (Multiattack, ×2) | +4 | 1d10+2 (avg 7, two-handed) | Slashing | — |
| The Warden | Life Drain (replaces one longsword) | +4 | 1d6+2 (avg 5) necrotic | Necrotic | DC 13 CON save or HP max reduced by damage taken until a long rest |

**Retinue** (optional, only if the party escalates loudly or lingers): 2 Skeletons from the outer mounds could plausibly still be drawn if the fight is noisy enough to reach them — but both outer-mound Skeletons are already destroyed this session, so there is no live retinue left. Play the Warden alone.

## Social path — try this first if the party engages verbally

The Warden speaks before it fights, if given the chance:

> **Entrance**: "You read the door. And still you opened it." *(A statement, not a question — it already knows.)*

If the party talks rather than draws steel, the Warden will test them: does *this* party understand what the inscription said, or do they think they're the exception? A Neutral Evil party arguing "we just want the fragments, not to complete the Crown" or "we understand the cost and accept it for ourselves, not for anyone else" is a genuine opening — the Warden isn't interested in stopping fragment-collecting, only in stopping *completion*, and it can be reasoned with with an Insight/Persuasion-worthy argument (DM judgment call on the roll, not pre-set). It will not simply hand over the magic weapon, but it may let the party leave, or even talk, without a fight if convinced they're not fools rushing toward the same ending.

If the party tries to lie or bull past it, it knows — centuries of guarding this door have made it hard to fool.

## Combat beats (if it comes to that)

| Beat | Line |
|------|------|
| **Bloodied** (below 22 HP) | "Do you understand yet? I did not want this either." |
| **On a kill / a PC drops to 0** | "Then you'll wait here too. Everyone does, eventually." |
| **Defeat / death** | "...someone else will have to watch, then." *(Not fear — something closer to relief.)* |

Never explain the plot further mid-fight — the inscription already said everything it needs to say. Speak between rounds, not instead of acting.

## Terrain

Stone chamber, older and larger than the outer mounds — room to maneuver, but no easy retreat once the door is opened (it doesn't lock the party in, but closing it again mid-fight costs an action and doesn't stop an undead that doesn't need to breathe). A stone sarcophagus at the center — the "king who was never a king" — undisturbed unless the party desecrates it (DM discretion on consequence if they do; nothing mechanical, purely narrative weight).

## Rewards

- **Magic weapon** of the ash-king era (per `info/locations/hollowmoor-barrows.md`) — ideal for Kriv. Concrete item TBD at time of reward; pick something Tier 1-appropriate from `info/treasure.md`'s progression when the moment comes.
- Old ceremonial grave-wealth, real money to a collector or Concordat archivist.
- If resolved socially instead of by combat: **award the same XP as defeating it** (per the established precedent in `sorrels-hollow-toll.md` — talking past a fight is worth the same as winning it).

### XP

| Enemy | XP | Notes |
|-------|-----|-------|
| The Warden (Wight) | 700 | Split 2 ways = 350/character. Award for defeat OR a genuine social resolution. |
