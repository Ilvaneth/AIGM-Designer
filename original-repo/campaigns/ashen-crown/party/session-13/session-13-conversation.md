# Session 13 — Conversation Log

**Campaign**: Ashen Crown
**Date**: 2026-09-03
**Starting Location**: The Maker's Undoing, Wing 1, threshold of Room 7 (Ambush Floor) — day 57

*Session 13 picks up exactly where session 12 paused. This log covers all in-fiction play; tooling/config work (building `room_description_check.py`, several hook-fragility fixes, a lore-collision catch and fix) happened alongside but is not recorded here except where it directly shaped a scene.*

---

## Scene 1 — Room 7, Ambush Floor — the Mimics

*(See combat log: session-13-combat-room7-ambush-floor.md)*

Rather than enter blind, the party investigated from the threshold. Ilvaneth's Investigation (19) spotted the central chest as anomalous — dust-free, unworn hinges, unlike the five genuinely aged crates around it. A nat-20 Arcana check (27) ruled out any active enchantment, deepening the mystery. Rather than approach directly, she tested the chest with Mage Hand from a safe distance — the disguise broke, revealing a Mimic (Mimic A), which was killed in round 1 with zero risk.

A second Mimic remained hidden among the five ordinary crates. The party systematically tested the rest with Mage Hand and, for the closer ones, Kriv's blade at reach — the fourth test found it: Kriv's sword briefly stuck fast in the Mimic's Adhesive as it revealed itself, freed with a successful Strength (Athletics) check. Mimic B was killed over rounds 4-5 (Kriv's Action Surge alone dealing 52 damage in one turn). No party damage across the whole fight.

The party searched the room afterward (Ilvaneth investigating, Kriv helping) — found 18 gp and an unidentified tarnished signet ring among the mimics' remains.

**OOC exchange**: the DM asked directly whether a short rest here would actually be safe, given the dungeon's own design says resting pressure is genuine before Room 13's Sanctuary. Claude reasoned through it honestly (noise from the fight, no guaranteed safety) and rolled a fair interruption check rather than just allowing it — it came up clear. Ilvaneth used Arcane Recovery to restore her 3rd-level slot; both PCs spent a Hit Die.

---

## Scene 2 — Room 8, Ward Remnant — the Cockatrice

*(See combat log: session-13-combat-room8-ward-remnant.md)*

Continuing stealthily, both PCs beat the resident Cockatrice's passive Perception for full surprise. It died in round 1 without ever acting — Fire Bolt plus two of Kriv's attacks. No party damage. 50 XP each.

Mid-combat, Ilvaneth's Fire Bolt was reported as a single die when her character sheet's cantrip damage entries (Fire Bolt, Chill Touch, Shocking Grasp) turned out to still be listed at pre-level-5 dice counts — a real bookkeeping gap, caught and fixed on the spot (Fire Bolt 1d10→2d10, the other two 1d8→2d8).

---

## Scene 3 — Room 9, Beast Den — the Manticore pair

*(See combat log: session-13-combat-room9-beast-den.md)*

The party approached a genuine two-Manticore lair — one on watch near the entrance, one resting deeper in darkness (a deliberate spacing choice to avoid a single-nova trivialization). Both PCs beat Stealth easily; full surprise. Ilvaneth opened with a natural-20 critical Fire Bolt; Kriv followed with a double natural-20 attack round — Manticore B dropped from 68 HP to 2 before it ever acted, then died trying to flee without Disengaging (cut down by Kriv's opportunity attack).

**Mid-fight DM correction**: after the noise of that opening round (a crit explosion, a death scream, a body impact), the DM directly questioned why Manticore A was still being run as "Surprised" in round 2 purely because its mechanical first-turn had technically passed. Claude agreed this was a real inconsistency — fiction should override mechanical bookkeeping here — and corrected it live, marking Manticore A "Alert" instead. Logged to `bug-log.md` as a generalizable lesson about the "one alert, one resting" spacing technique.

Manticore A fought on for several more rounds, landing the session's first real PC damage (7 HP to Kriv, then another 10 the following round). At 8/68 HP, having watched its sibling die fleeing without Disengaging, it used Disengage correctly and escaped into an unlit side passage. **The party chose not to pursue** — a real, wounded loose end (Manticore A is still alive somewhere in the dungeon as of session's end). 1,400 XP awarded for the full encounter.

The party searched the den afterward (advantage, Kriv helping) — 35 gp and a corroded sword hilt.

**A brief downtime beat**: during the party's next short rest (taken safely at Room 7 again after clearing the Beast Den), Ilvaneth used the quiet time to examine the accumulated mystery items (the signet ring, the sword hilt) — Detect Magic (both mundane) then a History check (22) found both items shared a stylized mountain-peak motif consistent with a Cindermoor prospecting/relic-hunting guild — likely remnants of an earlier, unrecorded expedition that never made it out. A closed, self-contained detail, not a forced new plot thread.

---

## Scene 4 — Room 10, The Gauntlet — the alpha Manticore pair

*(See combat log: session-13-combat-room10-the-gauntlet.md)*

A blood trail from the fled Manticore A led straight to Room 10 — and the alpha pair there had been warned. **No surprise this time**, a direct, earned consequence of not finishing Room 9's survivor. The DM asked directly whether Fireball could catch both Manticores given how they'd been described (standing close together, facing the entrance) — confirmed yes, and Ilvaneth's Fireball landed full damage on both (35 each, both failed their DEX saves). Kriv's natural-20 Goading Attack plus a full Action Surge round (49 damage) killed the Alpha outright in round 1; the second Manticore fell in round 2. Kriv took 10 more damage (down to 47/64) — the night's heaviest hit yet at that point. 1,400 XP.

The party short-rested at Room 10 afterward (interruption check clear) — Kriv spent 2 Hit Dice, restoring Action Surge/Superiority Dice/Breath Weapon/Second Wind to full.

---

## Scene 5 — Crossing into Wing 2 (The Discarded Works)

A short design conversation (OOC) preceded this: the DM asked how Claude envisioned the transition between Wing 1 (wild cave territory) and Wing 2 (Marek Stillwright's actual workshop level) before playing it out. Claude described a physical threshold — worked stone replacing raw cave, a dead ventilation system, Marek's own maker's mark — and the DM approved before it was played.

### Room 11, Failures — the Gargoyle

*(See combat log: session-13-combat-room11-failures.md)*

The party searched the room loudly, talking openly, with no stealth attempt. The DM asked directly why a resident Gargoyle (disguised as a "statue," motionless) wouldn't have already noticed given all that activity plus the audible noise of Room 10's fight moments earlier. Claude agreed and ruled the Gargoyle had plausibly already noticed and was patiently waiting — **the party was surprised this time**, not the monster, a self-inflicted consequence honestly ruled rather than let slide. It only landed one hit (5 damage to Kriv) before dying to Kriv's crit and an advantage-boosted Fire Bolt (Distracting Strike's effect). 225 XP.

### Rooms 12-14 — trap, Sanctuary, and the third Resonance Key

The party bypassed Room 12's spotted trap cleanly (Ilvaneth's passive Perception). Room 13 proved to be a genuine Sanctuary — Marek's own working ward, still active — and the party chose not to rest yet, planning to return. Room 14's pressure-plate alarm trap was spotted via passive Investigation and avoided — **later corrected by the DM**: passive Perception can auto-detect, but Investigation requires an active, declared search; Claude acknowledged the rules error, applied the fix going forward, and didn't retroactively punish the already-resolved bypass. Resonance Key 3 + Journal Fragment 3 were found (Investigation 20, Kriv helping) — *"...the maker's own name — unspoken, none of it means anything."* All three keys now in hand.

---

## Scene 6 — Long rest at the Sanctuary, and level 6

Returning to Room 13 for a real long rest, the DM raised two corrections before Claude could get ahead of itself: level-up mechanical benefits (features, HP, slots) only actually apply on a long rest, not the instant XP crosses a threshold — Claude had started processing Ilvaneth's level-up mid-dungeon and stopped immediately, nothing had been written yet. Separately, the DM flagged that roleplay XP hasn't been awarded in several sessions and asked to set that discussion aside for later rather than have Claude act on it unprompted — logged as deferred, not fixed.

The DM then had Kriv's remaining 18 XP added directly to cross his own level-6 threshold, and both level-ups were processed properly during the actual long rest:

- **Ilvaneth → level 6**: HP 45 (roll: 5+2), 3rd-level slots 3/3, **Undead Thralls** (School of Necromancy) — corrected once for scope after the DM fact-checked it against an outside source (the HP/damage bonus applies to *any* necromancy-created undead, not just Animate Dead specifically). Two free spellbook spells: **Misty Step** (prepared) and **Tiny Hut** (ritual). Prepared count raised 9→10.
- **Kriv → level 6**: HP 74 (roll: 7+3), **Great Weapon Master** feat (in place of an ASI) — no prerequisite, -5/+10 on the Barrow-King's Blade (a Heavy weapon), plus the bonus-action attack on a crit/kill. Burst Reference table extended with GWM-modified totals.

During the rest, Ilvaneth reviewed all three Journal Fragments together and deduced Room 18's Calibration solution (breathe, touch, speak "Marek Stillwright"). She also cast Animate Dead on Nessa Wren's and Perrine Oskold's preserved bodies — Undead Thralls let one casting target both, raising 2 zombies at boosted stats (HP 28 each, +proficiency to damage).

---

## Scene 7 — Room 15, Forge Floor — the second Gargoyle pair

*(See combat log: session-13-combat-room15-forge-floor.md)*

Full surprise (both PCs beat passive Perception 10), both opening attacks made as unseen attackers with advantage. Gargoyle A died to Kriv's opening two attacks plus a retroactively-added Action Surge (a live-table courtesy correction, applied cleanly since nothing else had happened in between). Gargoyle B fell in round 2. Zero party damage. 900 XP — **this fight leveled Ilvaneth to 6** in real terms (the XP crossing happened here; the mechanical application waited for the long rest, per the correction above).

A downtime beat followed: Ilvaneth spent part of the rest period examining the dungeon's accumulated mystery items with Detect Magic (both mundane) and a strong History check (22) connecting the ring and hilt to a shared, unrecorded expedition.

---

## Scene 8 — Wing 3, The Sealed Collection

### Room 17, Wardway — the hardest trap in the site

Rather than risk a PC, the party sent one of the two zombie thralls across the room as a proxy. It triggered the trap (DEX save 11 vs DC 16, failed, 20 force damage) and survived at 8/28 HP. No party risk.

The party searched the room afterward (advantage, 24) — found 14 gp and a personal, unfinished letter in Marek's own hand: *"...I know you're right, I've gone too far. But if I get it right just once more — none of it will matter. Please wait."*

### Room 18, Calibration — the puzzle

Applying the sequence Ilvaneth had deduced during the long rest (breathe, touch, speak the maker's name), the puzzle solved cleanly — no brute-forcing needed, exactly as the room was designed to require actually having read Marek's story first.

### Room 19, Commissions — the undelivered work

The party found and took three unclaimed commissions: a pair of linked communication stones (addressed, per Marek's own ledger, to "Karsgate — the Ledger Trading House, attn: V. Marrow" — a real, unresolved future hook), a prototype shortsword that feeds on its wielder's life force (which Marek refused to deliver), and an unclaimed staff. None yet Identified — Ilvaneth doesn't currently own the required 100 gp pearl component, deferred to a later purchase. The commission ledger itself named an unfinished order — **originally drafted as "Kessic Ambrey," caught and corrected before it stuck**: that name belongs to an already-established, unrelated Important-tier NPC (a Cinder Choir cell leader), a real near-miss collision caught only by chance and logged. Renamed to "Doran Calvane."

### Room 20, The Vault — the Clay Golem

*(See combat log: session-13-combat-room20-the-vault.md)*

A genuine boss fight, prepared properly per `two-player-scaling.md`'s solo-named-boss methodology: base SRD Clay Golem (133 HP, CR 9) reinforced to 190 HP — real margin above the party's computed 139.5 combined nova ceiling at their new level 6 — with no surprise possible (an ever-vigilant guardian).

It went down in 3 rounds. Kriv's Precision Attack + Great Weapon Master combo (offsetting the -5 penalty with a Superiority Die added to the roll) landed all 4 attacks for 81 damage in round 1 alone. The Golem's Haste and Berserk triggers both fired at points across the fight; Berserk turned its attacks on the party's own zombie thralls rather than the PCs — Zombie A (Nessa Wren) failed its Undead Fortitude save and was destroyed; Zombie B (Perrine Oskold) survived but had its max HP permanently reduced to 8. Neither PC took a single point of damage across the entire boss fight. 5,000 XP (2,500 each).

Loot: a Ring of Mind Shielding (Marek's own masterwork) and 568 gp, split. A final, thorough search of the vault (Investigation 27) found Marek's own remains and a last, unfinished note — his actual cause of death left deliberately ambiguous, exactly as the site was designed. 36 gp more.

**The Maker's Undoing is now fully cleared**, 20 rooms end to end, except Room 9's escaped, wounded Manticore A — a real, standing loose end.

---

## Session ends

The DM chose to save/checkpoint the session here rather than run a full `/dm-end-session` — state.md, character files, and this conversation log are current; a full end-session pass (NPC verifiers, session-log entry, feedback capture) was explicitly deferred to a later close.
