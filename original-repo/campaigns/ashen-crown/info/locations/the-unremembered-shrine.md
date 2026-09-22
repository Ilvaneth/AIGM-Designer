# The Unremembered Shrine

**Region**: IV. Karsgate (a day's travel from the city, unmarked on any map)
**Level range**: 9-10 — deliberately high for the region; a real "return when ready" site
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard
**Location class**: Dungeon
**Dungeon Type**: **Planned Dungeon** (Temple sub-purpose) — per Phase 0's DMG taxonomy, added 2026-09-02.
**Payoff type**: **Treasure-heavy** — the First Ember is a real, substantial magic item (Tier 3-caliber), distinguishing this from a pure Strategic-info site even though the lore weight is also real.
**Faction status**: Completely independent — one of the five faction-free neutral sites built 2026-08-29, per `dm-notes.md`'s standing "at least one site should owe nothing to the plot" rule

**⚠ Two-character party check** (`two-player-scaling.md`): real threats here are a small number of mummies (CR 3 each, **never more than one encountered at a time**) and a single solo boss-tier guardian — but per the 2026-08-29 correction, solo alone isn't enough. **The High Ward (Room 8) runs at ~100-110 HP** (a base wraith's 67 is well short of surviving this party's burst) **and has Legendary Resistance (2/day)** — she's meant to be a real test for a party that's forced the fight rather than earned passage, and a single lucky save-or-suffer spell shouldn't be the whole encounter. She has no Legendary Actions — the point of Room 8 is a single, weighty confrontation, not a drawn-out multi-round grind.

---

## Phase 1 — Concept & ecology

**What it was**: A temple to Ossara, Keeper of Names, built and consecrated generations before the schism that produced the orthodox Ember Crown temple, the Ashlord Concordat, and the Cinder Choir — the original, unblemished form of the faith all three later factions trace back to and argue over. **No faction currently knows this site exists.** Not even Cair Dunnow, which preserves the closest surviving fragment of the old rites, has any record of it — this predates even their own tradition.

**Why it was sealed**: The priesthood who kept this shrine chose, deliberately, to seal it and remove themselves from history rather than let it be found, corrupted, or fought over during an early succession crisis long before the current one. They did not die and leave it — **they mummified themselves alive, by ritual, and remained as its guardians**, a final act of devotion rather than an accident of preservation.

**Ecology now**: The self-mummified priesthood (**ash mummies** — reskinned SRD mummies, wrapped in ceremonial ash-cloth rather than ordinary linen) still stand their posts, millennia later, animated by the same devotion that sealed them in. One, the shrine's original High Ward, has changed into something closer to a **wraith** — the ritual didn't hold perfectly on her, and what she became is angrier and far more dangerous than her fellow guardians, though not malicious in any petty sense: she still believes she is protecting something worth protecting.

## Phase 2 — Map (non-linear)

**Entrance**: a genuinely hidden cliff-face door, found only through a specific combination of an old, nearly-illegible marker stone and a matching astronomical alignment (a real puzzle, not a passive roll alone — see Room 1). **No rumor, no map, no NPC in the game currently points to this site** — it should be found through pure exploration or a DM-seeded, very rare clue, never handed out casually.

**Verticality and loops**: the shrine descends in three ritual tiers (Outer, Middle, Inner), each sealed from the last by a ward the party must satisfy rather than simply unlock, with a side passage connecting the Middle tier back to the Outer tier so a retreating party isn't forced back through the same guardians twice.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Marker Stone** | The actual entrance puzzle — a worn stone carved with star patterns, matched against the sky (or a DC 17 History/Investigation check as a fallback) to reveal the door. No door is visible without solving this. | Puzzle | — |
| 2 | **The Outer Vestibule** | Ash-cloth banners, perfectly preserved in the sealed, airless dark — real environmental storytelling, no fight, the party's first confirmation this is genuinely undisturbed. | Lore | — |
| 3 | **The Ward of the First Tier** | A binding glyph that tests intent, not strength — a DC check or a genuine act of respect (an offering, correctly performed) opens the way; forcing it magically or physically wakes every guardian in the shrine at once, a real and costly mistake. | Puzzle | — |
| 4 | **The Outer Cloister** | The first ash mummy, alone, posted at this threshold for millennia — a real fight, but isolated per the site's own design. | Combat | — |
| 5 | **The Reliquary of Names** | A side chamber, genuinely undisturbed — scrolls and ash-tablets recording the shrine's own true history of the schism, contradicting or completing whatever the party has already learned from the Concordat and Choir's own accounts. Real lore payoff, no combat. | Lore | — |
| 6 | **The Middle Sanctum** | A second ash mummy, guarding the passage down — same design as Room 4, encountered separately. | Combat | — |
| 7 | **The Sealed Archive** | The side passage connecting back to the Outer tier — also holds a genuine, physical treasure cache: ceremonial ash-era grave-goods and a worked-silver reliquary, valuable both as coin and as an artifact Corvin Thale would pay well to authenticate. | Treasure | — |
| 8 | **The Inner Sanctum — the First Ward's Vigil** | The final chamber. **The High Ward**, the wraith-shifted guardian, still stands over the shrine's original altar. She does not attack on sight — per `npc-consistency.md`'s own logic even for a guardian, she tests whether the party has actually earned passage (did they solve Room 1 properly, did they respect Room 3's ward) before deciding whether they're worthy visitors or violators. Combat here should be avoidable for a party that's shown real respect throughout, and a genuine, dangerous fight for one that hasn't. | Combat | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02): against Treasure-heavy bands — Combat 3/8 (**37.5%, below the 50-60% target**), Trap 0/8 (**0%, below target**), Special 3/8 (**37.5%, well above the 10-15% target**), Structural 2/8 (**25%, above the 15-20% target**). **Accepted as a deliberate, one-off deviation, DM decision 2026-09-02** — this site is genuinely puzzle-dominant by design (every ward is a test of intent, not a lock to force), the deliberate tonal contrast this file's own "Running this well" section already names. Not treated as a new "Puzzle-heavy" Payoff-type band since this is currently the only example of the shape — revisit if a second genuinely puzzle-dominant site appears.

- **Combat**: two ash mummies (Rooms 4, 6), always separate; the High Ward (Room 8), a solo boss-tier reskinned wraith, avoidable through demonstrated respect
- **Puzzle/exploration**: the Marker Stone entrance (Room 1), the intent-based ward (Room 3) — real puzzles, not blind rolls alone
- **Lore/treasure without combat**: the Outer Vestibule (Room 2), the Reliquary of Names (Room 5), the Sealed Archive (Room 7)
- **The reward, deliberately not Crown-related** (this is a neutral site, not a sixth fragment): **the First Ember**, an amulet holding a fragment of Ossara's original, undivided authority over death — mechanically a genuine Tier 3-caliber item (death ward-adjacent utility, resistance to necrotic damage, DM's final numbers when it's actually found), and narratively significant lore that could recontextualize what the Concordat, the Choir, and the orthodox temple all currently believe about their own shared origin.

## Running this well

**This site rewards patience and respect over force**, all the way down — every ward is a test of intent, not a lock to pick, and the final encounter is explicitly designed to be avoidable for a party that's played it right. This is a deliberate tonal contrast to most of this campaign's faction-tied sites, which assume conflict — here, the "right" answer is reverence, and the mechanical reward for getting it right is a boss fight skipped, not just loot gained.

## Connections

- `gazetteer.md` — Region IV, unmarked, a day from Karsgate
- No faction ties whatsoever — deliberately, per the standing "faction-free site" rule
- `locations/cair-dunnow.md` — thematically the closest thing to a predecessor, though Cair Dunnow itself doesn't know this site exists
- `factions/ashlord-concordat.md`, `factions/cinder-choir.md` — the Reliquary of Names (Room 5) could genuinely inform or contradict either faction's own account of the schism, at the DM's discretion when the party actually shares what they found
