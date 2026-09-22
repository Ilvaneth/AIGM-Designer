# Treasure and Magic Items

SRD magic items (`10 magic items.md`, 247 entries) — look up with:

```bash
py .claude/scripts/srd_lookup.py item "Cloak of Elvenkind"
```

The original sandbox said "a magic weapon" and "coin." This is the actual progression.

---

## Campaign-specific items

Named pieces with story attached. These carry more weight than a generic +1.

### The Ashen Crown fragments
Not items in the usual sense. Each fragment is warm to the touch, hard to look away from, and faintly resists being set down.

**Their effects are not loot — they are the two ascension tracks.** Every fragment the party acquires advances *both* PCs, in different directions, with different costs. See **`ascension-tracks.md`** — that file is the authority; don't duplicate its numbers here.

- **Kriv**: the dormant Shestendeliath dragon blood wakes. Scales, breath, presence, and eventually wings. One-way.
- **Ilvaneth**: the Crown's preservation pattern takes hold. She stops needing to eat, stops aging, stops dying. One-way.
- **Full Crown**: the campaign's endgame. Not a stat block. A choice.

### Named items by site

| Item | Where | What it is |
|------|-------|-----------|
| **Harn's Spellbook** | The Weeping Tower | Ovelt Harn's working book. Spells above Ilvaneth's level to transcribe, plus his research notes on surviving death. |
| **The Tally Book** | Sefwyn Marrow | Their private skim-ledger. Not magical. Worth more than most magic items to the right buyer. |
| **The Debt Book** | Fennick's storeroom | Forty households' obligations. Power, not loot. |
| **Wardensteel** | Shestendeliath Hold | **Kriv's house blade.** Grey fire, not red. A **Flame Tongue** that starts as +1 and unlocks properties as he reclaims the house — a weapon that levels with his arc rather than a static drop. |
| **The Warden's Oathplate** | Shestendeliath Hold vault | **Dwarven Plate**, reskinned as Shestendeliath ceremonial armour, dragonborn-sized. |
| **The Charge-Roll** | Shestendeliath Hold | The Ash-Warden houses' sworn record — **which house was charged with which fragment.** The party's map to the rest of the Crown, arriving through Kriv's inheritance rather than Ilvaneth's research. |
| **The Shestendeliath Signet** | Corran's collateral room | Not magical. Proof of identity — worth more to Kriv than any weapon. |
| **The Barrow-King's Blade** | Hollowmoor Barrows | Ash-king era. A **Sun Blade** reskinned as grey fire. Alternative if the party reaches the barrows before the Hold. |
| **The Screening Records** | Ash-Kilns | The Choir's list of who they've been watching in Gallowmere. Blackmail at town scale. |
| **The Vaelthorn Seal** | Corran's collateral room | A destroyed house's signet. Possibly Kriv's own. |
| **The Cathedral Mold** | Drowned Cathedral | The Crown's original casting mold. Whoever holds it can theoretically make a *counterfeit* fragment. Enormous plot leverage. |

---

## Progression by tier

Rough pacing, not a strict schedule — but tracked against real numbers now, not just a menu. Derived 2026-08-25 from the actual campaign shape: `gazetteer.md` lists **~31 real sites** (~21 in Chapter 1, ~10 in Chapter 2) against `progression.md`'s **40-60 total sessions**. That's not every session getting an item — most sites give coin, information, or story, not gear — but it's enough density that a tier running dry for several sessions is a pacing miss worth catching, not just bad luck.

**Target**: roughly **5-8 permanent magic items per tier bracket**, for the party of two combined (so each PC nets a handful per bracket) — on top of the consumables/coin, which flow much more freely. Track actual counts in the Awarded-so-far log below; if a bracket is running under-target with its sessions running out, that's the signal to put a loot-bearing site back in front of the party (see "keeping pace" below), not to force an item into an unrelated scene.

### Tier 1 (levels 1-4) — the Marches, early Thornlands
Consumables and small permanents. The party should feel every single item. **Target: 5-8 permanent items combined**, ~8-12 sessions.

**Coin**: 50-300 gp per site
**Items**: Potion of Healing (multiple), Potion of Climbing, Oil of Slipperiness, Spell Scrolls (1st-2nd), Bag of Holding, Cloak of Elvenkind, Boots of Elvenkind, Goggles of Night, Bracers of Archery, +1 weapon (one, from a real fight)

*Status as of session 2 end*: **0 permanent magic items, 2 sessions in, target 8-12.** Already behind pace — see "keeping pace" below.

### Tier 1-2 (levels 5-8) — Cindermoor, Karsgate, late Thornlands
**Target: 5-8 permanent items combined**, ~12-18 sessions.

**Coin**: 300-1,500 gp per site
**Items**: +1 armor/shield, Cloak of Protection, Ring of Protection, Wand of Magic Missiles, Pearl of Power, Flame Tongue, Mithral Armor, Periapt of Wound Closure, Elven Chain, Handy Haversack, Boots of Elvenkind, Amulet of Proof against Detection and Location, Wand of Web
**Avoid — flat stat-floor items**: both PCs already sit at 18 in their primary stat (Ilvaneth INT 18, Kriv STR 18) — a floor-19 item (Headband of Intellect, Gauntlets/Belt of Ogre Power) doesn't even raise the modifier (18 and 19 are both +4) and would be a genuinely wasted slot. Standing DM/table decision (confirmed 2026-08-30, after this exact item nearly got offered again) — don't offer these to this party at any tier, prefer a real ability-score-boosting item (Manual/Tome, an ASI-granting effect) only once a score is actually below the relevant threshold.

### Tier 2-3 (levels 9-14) — Ashvale, Emberhold
**Target: 6-9 permanent items combined**, ~12-18 sessions.

**Coin**: 1,500-10,000 gp
**Items**: +2 weapons and armor, Amulet of Health, Boots of Speed, Cloak of Displacement, Ring of Free Action, Staff of Fire/Frost, Rod of Absorption, Robe of Eyes, Scimitar of Speed, Dwarven Plate, Ioun Stones, Necklace of Fireballs. **No Belt of Giant Strength** — same flat-stat-floor issue as Tier 1-2's note above; Kriv's STR 18 is already at the modifier ceiling a hill/stone belt would set.

### Tier 3-4 (levels 15-20) — Sundered Reach, Grey Kingdom
**Target: 6-9 permanent items combined**, ~6-10 sessions — fewer sessions, but each one (Frostmere, the Bonewrights' Hall, Kar Vaelth) is built to deliver.

**Coin**: hoard-scale; the Frostmere dragon alone should be transformative
**Items**: +3 weapons and armor, Staff of Power, Robe of the Archmagi (Ilvaneth's endgame gear), Holy Avenger, Defender, Luck Blade, Ring of Spell Turning, Ring of Regeneration, Cubic Gate, Sphere of Annihilation, Manual/Tome stat-boost books, Ring of Three Wishes

### Keeping pace

If a tier is meaningfully under its target with its session budget running out, the fix is **visibility, not a gift** — surface a loot-bearing site as one of the session's live options (`sandbox-index.md`'s "three visible options" rule already requires this), and let the party choose to walk into it. Never hand an item mid-scene just to hit a number; that breaks the same trust as fudging a die roll.

**Right now**: Tier 1 is behind (see status line above). Checked both candidate sites against the party's actual level (3) with the two-player +2 adjustment applied:

- **The Drowned Mill — the right fit now.** Nominal 1-3, adjusted effective 3-5 — the party sits right at the floor. Real math: the stirge swarm alone is ~250 adjusted XP (solid Medium/Hard), the two ghouls alone are ~800 adjusted (exactly Deadly at level 3, and ghoul paralysis makes it feel worse than the number), both together (if the party is loud) is ~1250 — well past Deadly, real TPK risk. The site's own design already assumes a careful party avoids waking both at once. Genuinely playable now, with caution.
- **The Weeping Tower — not yet.** Nominal 3-5, adjusted effective 5-7 — 2-4 levels above the party's current 3. Better revisited around level 5, or approached as a negotiation with the guardian (the file explicitly allows talking past it) rather than a fight if the party goes early.

**The Drowned Mill is the one to put in front of the party next**, not the Weeping Tower. See `sandbox-index.md`'s session checklist, step 4a — it's now a required check at every session start, not just a one-time note, specifically so this doesn't depend on any one session remembering it.

---

## Placement notes

- **Imbalance flag resolved (2026-08-26)**: after two items to Kriv, the Bag of Holding went to Ilvaneth, evening the count for this shopping trip (Kriv: Blade + Cloak, Ilvaneth: Web scroll + Bag of Holding). Next meaningful item should still lean Ilvaneth-ward if one comes up soon, since Kriv's two items are individually stronger (a Sun Blade and a Cloak vs. a spell scroll and a utility bag) — track the *weight*, not just the count.
- **Match the item to the character — and keep it even.** Ilvaneth: Pearl of Power, Robe of the Archmagi, spellbooks, save/defense items (not a flat INT-floor item — see the "avoid" note above). Kriv: Wardensteel, the Oathplate, Defender, save/defense or damage items (not a flat STR-floor item, same reason). A two-person party means every item lands hard — and it also means an imbalance is immediately visible. Track it: if the last two meaningful items both went to one PC, the next one doesn't.
- **Necromantic flavor over generic.** A Cloak of Protection found in a barrow should be grave-wrappings that don't rot. Same mechanics, different world.
- **Sell-value matters for this party.** They're building a power base; gold buys holdings. Bulky, valuable, hard-to-move treasure (the Drowned Mill's brandy casks, Corran's collateral) is often more interesting than a magic sword.
- **Log what's been given** below so item pacing stays honest.

## Awarded so far

| Session | Item | To whom |
|---------|------|---------|
| 1 | Ashen Crown fragment | Ilvaneth |
| 1 | Grave goods (silver bracelet, bone bead necklace, old coins) — **sold to Corran, session 2, 11 gp** (5 Ilvaneth, 6 Kriv) | Split |
| 2 | 2 stolen horses | Split — still unsold, Demirnal's brand, Corran won't touch branded livestock |
| 4 | **The Barrow-King's Blade** (Sun Blade, reskinned as a grey-fire greataxe) — Hollowmoor Barrows deep chamber, after defeating the Warden | Kriv — Tier 1's first permanent magic item |
| 4 | **Cloak of Elvenkind** — bought from Corvin Thale, The Sable Casket, Harrowgate, 200 gp (haggled from 250) | Kriv — Tier 1's 2nd permanent item, though a purchase rather than a find; still counts toward pacing |
| 4 | **Bag of Holding** — bought from Corvin Thale, traded the Hollowmoor ceremonial pieces (220 gp credit, Deception 21) + 120 gp cash toward the 350 gp price | Ilvaneth — Tier 1's 3rd permanent item, balances the last two going to Kriv |
| 4 | **Harn's Spellbook** + **Pearl of Power** — the Weeping Tower, resolved socially (Deception 14, then an honest answer) past the bound guardian. Pearl reflavored from a generic locked-box find after the table flagged a STR item as thematically wrong for a mind/self-preservation site | Ilvaneth — both directly tied to her personal arc site |
| 5 | **+1 Dagger** — a nameless shrine nook, The Widow's Hollow (first faction-free, arc-free site — see `dm-notes.md`) | Ilvaneth |
| 5 | **Mithral Chain Mail** — the Widow's own hoard, given freely as part of a bargain (no fight). Removes Kriv's long-standing Chain Mail Stealth disadvantage | Kriv — balances recent items leaning Ilvaneth-ward (Pearl, Bag of Holding, Spellbook, Dagger) |
| 5 | 400 gp + ~150 gp jewelry from the Widow's hoard | Split |
| 6 | **+1 Dagger, dwarven runes** (folk-ward vs. goblinoids) — the Sealed Vault, Kargrim's Reach room 11 | Unclaimed, stored in the Bag of Holding |
| 6 | 220 gp + ~100 gp worked silver — the Sealed Vault, Kargrim's Reach room 11 | Split (gold); silver unsold |
| 6 | **Periapt of Wound Closure** — the basilisk's hoard, Kargrim's Reach room 20. Swapped in after the DM/players flagged a flat-stat item (Gauntlets of Ogre Power) as a poor RP fit | Unclaimed, stored in the Bag of Holding |
| 6 | 350 gp + ~120 gp raw silver ore — the basilisk's hoard, Kargrim's Reach room 20 | Split (gold); silver unsold |
| 8 | **Wand of Magic Missiles** — bought from Corvin Thale, The Sable Casket, Harrowgate, 250 gp (haggled from 300, Persuasion 25) | Ilvaneth — Tier 1-2's 1st permanent item |
| 8 | **Ring of Protection** — bought from Corvin Thale, same visit, 750 gp (haggled from 900, same negotiation) | Ilvaneth — Tier 1-2's 2nd permanent item |
| 8 | 265 gp (Corvin's payout for the Verrick collection job, via a false cost account) + 90 gp (Marsh's coin + effects) | Split |
