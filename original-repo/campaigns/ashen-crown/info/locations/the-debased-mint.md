# The Debased Mint

**Region**: IV. Karsgate (the Undercity, beneath an unremarkable warehouse — deliberately built underground from the start, not later buried by the city's growth)
**Level range**: 7-9 (this two-character party should read it as roughly +2 — see `two-player-scaling.md`; built and designed 2026-09-02, collaboratively with the DM — never played)
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard
**Location class**: Dungeon
**Dungeon Type**: **Planned Dungeon** (Vault/Mint) — built deliberately, underground, by House Doskarn itself.
**Payoff type**: **Treasure-heavy** — real mint wealth (raw ash-metal, coin dies, minted currency) alongside the fragment and the family's own tragic history.

**A genuine fragment site** — per the Charge-Roll at Shestendeliath Hold (session 9): House Doskarn was charged with a fragment kept beneath Karsgate's undercity, in the old ash-mint. This is that site.

**⚠ Two-character party check** (`two-player-scaling.md`): every fight here was computed individually — see Phase 3's table for each room's raw/adjusted XP. **Never stack two CR3+ creatures in the same room without recomputing** — an early draft's "2 Wraith together" hit 10,800 adjusted, a real TPK risk; the final roster keeps CR5 threats solo and pairs lower-CR creatures for texture instead. **The boss (Room 18) is deliberately left unlocked** — re-run `py .claude/scripts/solo_burst_check.py ashen-crown --vs undead --full-nova` against the party's real sheet at the time of the fight and add HP margin/Legendary Resistance, the same discipline already applied to "The Maker's Undoing"'s Clay Golem and "The Tithe Barn"'s Shambling Mound.

---

## Phase 1 — Concept & ecology

**What it was**: An Ash-Warden house's own secret mint, built underground from the start for security — House Doskarn's charge was a fragment of the Ashen Crown, and rather than simply guard it in a vault, they built an operation around it: minting a small, deliberately limited currency backed by the fragment's own residual authority, believing they could study and profit from what they'd been sworn to protect. A slow, prideful mistake, not a single dramatic one.

**What happened to them**: The fragment consumed the house from within. Unlike Kriv's own bloodline, which carries dragon-blood specifically bred to eventually bear this cost, House Doskarn had no such inheritance — they simply took the power, generation after generation, with no way to pay what it demanded. **The family is still here, transformed** — not a single dramatic fall, but a slow, layered corruption: mint staff and guards who died and rose as the lesser dead they were always going to become, and the family itself, sunk deeper and deeper into what the fragment made of them, culminating in whoever led the house at the very end.

**A direct mirror, not a coincidence**: this site exists specifically to give Kriv and Ilvaneth a warning made concrete — what unmanaged ascension actually looks like, generations compressed into one place. Nothing here needs to be stated aloud; the site should simply be read, room by room, as what it is.

**Ecology**: the outer staff (Skeletons, Zombies, a Shadow, Ghouls, an Ogre Zombie) died more mundanely and rose simpler — corrupted by proximity, not by the fragment's direct touch. The family itself (Ghast, Mummy, Wight, culminating in Wraiths) endured the fragment's power directly, and their transformation runs correspondingly deeper.

## Phase 2 — Map (non-linear)

**Entrances**: the Sealed Entrance (Room 1), a hidden stair down from an unremarkable Undercity warehouse — and the Ash-Metal Stores (Room 6), reachable directly from a second, cruder delivery tunnel the mint once used to bring in raw material from the surface docks. A party that finds the delivery tunnel first can reach the outer working floor without ever using the main stair.

**Verticality**: three real levels — the Working Floor (mint operations), the Family Quarters (the house's own private wing, cut deeper), and the Vault proper (the deepest, most deliberately secured level).

**Loop**: the delivery tunnel (Room 6) and the main stair (Room 1) both open onto the Working Floor from different points, letting a party retreat by a different route than they entered.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Sealed Entrance** | A hidden stair down from an unremarkable Undercity warehouse — the obvious way in. | Entrance | — |
| 2 | **The Coin Hall** | Where the mint actually operated — **1 Ghast + 3 Skeleton** (former staff, a senior overseer risen more dangerous than the rank and file). 600 raw → ×2 (3-6 count) → ×2.5 (2-PC bump) = **1,500 adjusted, Medium** at level 7. | Combat | — |
| 3 | **The Smelting Chamber** | The old furnaces, cold for years — residual heat pockets and bad air are a real hazard (Investigation to notice, Constitution save to avoid a lungful). | Trap | — |
| 4 | **The Die Vault** | The coin dies and minting tools themselves — worth real coin to a forger or collector, and physical proof of what this place actually made. | Treasure | — |
| 5 | **The Overseer's Ledger Room** | **1 Shadow** (a clerk, quieter and stranger than the others) — 100 → ×1.5 (2-PC bump, solo) = **150 adjusted**, a deliberate breather between Rooms 2 and 6. The mint's own operating records, showing the slow shift from "guarding the fragment" to "using it," are here to read. | Combat | — |
| 6 | **The Ash-Metal Stores** | The second entrance (the delivery tunnel) opens here. **1 Ogre Zombie + 2 Zombie** (laborers, the largest one clearly worked hardest and died hardest). 550 raw → ×2 (3-6 count) → ×2.5 (2-PC bump) = **1,375 adjusted, Medium** at level 7. Raw ash-metal stockpiles, real bulk value. | Combat | — |
| 7 | **The Private Stair** | The house's own entrance to their private wing, distinct from the working floor. | Entrance | — |
| 8 | **The Sitting Room** | Degraded family portraits, the first real sign of what the family became. **1 Mummy** (a family member who tried, and failed, to preserve themselves against the corruption on their own terms — a direct echo of "The Unremembered Shrine"'s self-mummified priesthood, but done alone, out of fear rather than devotion). 700 → ×1.5 (2-PC bump, solo) = **1,050 adjusted, Medium** at level 8, plus real disease risk. | Combat | — |
| 9 | **A Family Chamber** | **1 Wight** — another family member, further along. 700 → ×1.5 = **1,050 adjusted, Medium** at level 8. | Combat | — |
| 10 | **The Nursery** | No fight. Small, sealed, undisturbed. Whatever conclusion the party draws here, let it sit in silence rather than being explained. | Lore | — |
| 11 | **Another Family Chamber** | **1 Ghast + 1 Wight** — two family members, found together, whatever that means for how they died. 1,150 raw → ×1.5 (2 count) → ×2 (2-PC bump) = **3,450 adjusted, Hard-Deadly** at level 8. | Combat | — |
| 12 | **The Family Shrine** | A binding ward keyed to Doskarn blood specifically — a DC check or a genuine act of understanding the family's own history (read from Rooms 8-11) opens it safely. **1 Will-o'-Wisp** haunts the room, deceptive rather than directly aggressive — 450 → ×1.5 = **675 adjusted**, a real but lesser threat that actively tries to mislead whoever's solving the ward. | Puzzle | — |
| 13 | **The Vault Threshold** | The mint's own final security measure, still partially active — a genuine ward-hazard (Investigation to notice, Dexterity save to avoid). | Trap | — |
| 14 | **The Treasury Antechamber** | The bulk of the mint's actual wealth — minted currency, unworked ash-metal, real coin value. **1 Wraith** guards it, whether consciously or not. 1,800 → ×1.5 = **2,700 adjusted, Medium-Hard** at level 9. | Combat | — |
| 15 | **The Last Guard** | **1 Minotaur Skeleton** (the mint's own original security measure, animated long before the family's fall) **+ 1 Wight** (a family member who stayed at this post). 1,150 raw → ×1.5 (2 count) → ×2 (2-PC bump) = **3,450 adjusted, Hard-Deadly** at level 9. | Combat | — |
| 16 | **Sanctuary** | A ritually sealed side-chamber the family themselves once used to safely study the fragment, briefly, before the corruption made that impossible — still genuinely safe. A real rest point before Room 18. | Sanctuary | — |
| 17 | **The Minting Throne** | The house's own final record, in the last clear hand any of them wrote — an honest account of watching the corruption take hold, generation by generation, and the decision to keep going anyway. The emotional core of the site. | Lore | — |
| 18 | **The Vault** | **Boss fight — the last head of House Doskarn**, a Wraith (base stats, deliberately not finalized — see the scaling warning above). Holds the fragment and the remainder of the mint's wealth. | Combat | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, checked before finalizing): Combat 9/18 (**50%, in band ✓**), Trap 2/18 (**11.1%, in band ✓**), Special (Puzzle+Treasure+Sanctuary) 3/18 (**16.7%, slightly above the 10-15% target**), Structural (Entrance+Lore) 4/18 (**22.2%, above the 15-20% target**) — both accepted, the same margin already documented for "The Maker's Undoing" at this room count.

- **Combat**: 9 rooms, using 9 distinct creature types (Skeleton, Zombie, Shadow, Ghast, Ogre Zombie, Mummy, Wight, Will-o'-Wisp, Wraith) — no room repeats the same composition, and no two CR5 creatures are ever paired together.
- **Hazard**: the smelting chamber (Room 3), the vault threshold (Room 13)
- **Puzzle/exploration**: the Family Shrine's blood-ward (Room 12), solvable only by having actually read Rooms 8/9/11's own story first
- **Treasure**: the Die Vault (Room 4), the Ash-Metal Stores (Room 6, alongside its fight), the Treasury (Room 14, alongside its fight), the final vault (Room 18)
- **Lore**: the Nursery (Room 10) and the Minting Throne (Room 17) — deliberately not narrated with explanation; let the table draw its own conclusions

## Running this well

**This site is a mirror, not a lecture.** Never have an NPC or a written note directly compare House Doskarn to Kriv's own bloodline — let the parallel exist entirely in what's found, read, and fought. If a player draws the connection aloud, that's the site working; it should never need to be pointed out.

**Resting pressure**: genuine through the Working Floor and Family Quarters — the Sanctuary (Room 16) is the first real, earned rest point, positioned deliberately right before the site's hardest content (Rooms 17-18).

## Connections

- `gazetteer.md` — Region IV, Karsgate Undercity
- `locations/shestendeliath-hold.md` — the Charge-Roll, where House Doskarn was first named
- `info/kriv-thread.md` — the direct thematic mirror to Kriv's own ascension; no in-fiction NPC should ever state this explicitly
- `info/ascension-tracks.md` — a real, earnable insight into unmanaged fragment corruption, at the DM's discretion when the party reaches Room 17
- `locations/karsgate.md` — the Undercity entrance point
