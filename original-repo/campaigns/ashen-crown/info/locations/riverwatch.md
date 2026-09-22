# Riverwatch

**Region**: I. The Marches
**Level range**: 2-4
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard
**Location class**: Dungeon
**Dungeon Type**: **Ruins** (per Phase 0's DMG taxonomy, added 2026-09-02) — an abandoned military structure, not built or maintained by its current occupants. Carries real Lair texture (the kobold band's own ecology, the grick's den) without being a Lair itself — nobody here designed this space.
**Payoff type**: **Treasure-heavy** — mostly modest/scavenged junk per Ruins' own weight, but a real specific cache (the Compact strongbox) survived, matching Ruins' "modest unless a specific cache survived" rule.

**⚠ Two-character party check** (`two-player-scaling.md`): the kobold band is roughly a dozen strong, but per the room design they're never fought all at once — the rooms deliberately split them (the tunnel clutch, the living-quarters group, the watch post). Fighting the full band together would be ~300 raw XP × the 15+ monster multiplier (bumped to ×4 for two PCs) = 1,200 adjusted, Deadly at level 2 — don't let a single alarm bring the entire band to one room. The grick alone (Room 8) is 450 raw → adjusted 675, a fair Hard fight at this level range.

---

## Phase 1 — Concept & ecology

**What it was**: A border watchtower, garrisoned to watch the southern road before the succession war moved the actual fighting elsewhere and the crown stopped paying for it. Abandoned, not destroyed — the tower still mostly stands.

**Who holds it now**: A kobold band, maybe a dozen strong, moved into the tower's lower levels and cellars over the last two years. They've been stripping the road of anything a careless traveler drops or a wrecked cart leaves behind, and — per `gazetteer.md`'s original hook — have accumulated a genuinely odd pile of loot as a result: not treasure by design, just months of scavenged debris that happens to include real value mixed in with junk.

**Ecology**: The kobolds avoid the flooded cellar entirely — a **grick** has denned there, and rather than fight it, the kobolds have taken to feeding it scraps to keep it docile, effectively (and mostly unintentionally) turning it into a guard the tower's actual defenders don't have to pay or feed properly themselves.

## Phase 2 — Map (non-linear)

**Multiple entrances**: the collapsed main gate (loud, obvious), a supply tunnel around the back (kobold-sized, a tight squeeze for anyone larger), and the tower's old chimney flue (a vertical climb, bypasses the ground floor entirely).

**Verticality**: three levels — the ruined upper tower (open to the sky in places), the ground floor (kobold living quarters), and the flooded cellar (the grick's den) — with a working, kobold-maintained rope-and-pulley system between upper tower and ground floor that the party can use or sabotage.

**Loop**: the supply tunnel and the main gate both lead to the ground floor from different sides, so a party that enters one way can leave the other without backtracking through wherever the fight happened.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Collapsed Gate** | The obvious entrance — rubble, an old warning sign in a script nobody local reads anymore. Watched (from Room 5) rather than independently guarded. | Entrance | — |
| 2 | **The Supply Tunnel** | Kobold-dug, cramped for a Medium creature — difficult terrain for anyone not Small. A second, smaller kobold clutch (2, guarding the band's actual supply route) rounds out the "roughly a dozen" total the header already commits to — added 2026-09-02, per the DMG content-ratio fix below; nobody would leave the tunnel they actually use for supply runs unwatched. | Combat | — |
| 3 | **Ground Floor — Living Quarters** | Most of the band lives here — bedrolls, a cookfire, and the beginnings of the "odd pile of loot": broken cartwheels, a dented shield, a genuinely fine merchant's lockbox (still locked) among the junk. | Combat | — |
| 4 | **The Rope Hoist** | The pulley system connecting ground floor to upper tower — sabotage drops anyone using it, or the party can use it to bypass Room 3 entirely from above. | Puzzle | — |
| 5 | **Upper Tower — Watch Post** | Open to the sky, the original watch position — a real, if weathered, spyglass survives, and the sentry keeps their own small hoard here, separate from the band's communal pile. | Combat | — |
| 6 | **Upper Tower — Collapsed Section** | Unstable footing, a real environmental hazard (a DC check to cross without triggering a partial collapse) rather than a combat room. | Trap | — |
| 7 | **The Cellar Stair** | The one route down — narrow, and the kobolds have rigged a simple noise-trap (strung bells) to warn them if the grick's den is disturbed from above. | Trap | — |
| 8 | **The Flooded Cellar — the Grick's Den** | Waist-deep water, poor visibility, the grick itself, and — half-submerged — the genuinely valuable core of the "odd loot pile": a strongbox from a wrecked Compact supply wagon, untouched because the kobolds won't go near the grick to get it. | Combat | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02 as part of this file's upgrade to the current standard — verified by the script itself, not hand-counted): Combat 4/8 (**50%**, target 50-60% ✓ — the Room 2 tunnel clutch was added specifically to clear this band, see the room table), Trap 2/8 (**25%**, above the 10-15% target — an 8-room site swings ~12.5% per room, so this reads as one room over rather than a real imbalance; both traps are genuinely the kobolds' own rigging, not padding), Puzzle 1/8 (**12.5%**, in the 10-15% Special band), Entrance 1/8 (**12.5%**, below the 15-20% Structural target — a small site with only one true structural room; not padded further since Room 2's tunnel is now Combat, not a second Entrance).

- **Combat**: the tunnel clutch (Room 2), the living-quarters band (Room 3), the watch-post sentry (Room 5), the grick (Room 8, a genuine Medium threat for this level range)
- **Hazard**: the collapsed section (Room 6), the noise-trap bells (Room 7)
- **Exploration/puzzle**: the rope hoist as an alternate route (Room 4), the locked merchant's lockbox (Room 3) needing a key or a Thieves' Tools check
- **Treasure**: the kobold band's communal junk-pile (mostly worthless, a few real items), the sentry's separate personal hoard (Room 5), and the real prize — the Compact strongbox in the flooded cellar, guarded by the one thing the kobolds themselves are too scared to retrieve it past

## Connections

- `gazetteer.md` — Region I, along the southern road
- `factions/ironclad-compact.md` — the strongbox is Compact property, lost in an unreported wagon wreck; recovering it (or being caught with it) has real, if minor, faction consequences
