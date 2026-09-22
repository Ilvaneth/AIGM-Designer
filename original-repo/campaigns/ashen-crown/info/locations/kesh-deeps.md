# Kesh Deeps

**Region**: III. The Cindermoor
**Level range**: 5-8 — **calibrated and tested at level 5 only** (session 10, 2026-09-01). The stated range is when this site is a reasonable *destination*, not a promise the fixed encounters below stay equally challenging across all four levels — see the scaling note below before running this for a party above level 6.
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard
**Location class**: Dungeon
**Dungeon Type**: **Mine** (per `dungeon-design.md`'s Phase 0 DMG taxonomy, added 2026-09-01) — dug for a practical purpose, not treasure-keeping. Treasure is deliberately modest; the real payoff is below.
**Payoff type**: **Strategic-info** — the duergar's mining-lore records (Room 6) and the ash-king memorial chamber beyond Room 9 are this site's actual reward, not gold. Per `dungeon-design.md`'s Phase 0 rule, these rooms' content must never be paced faster than the combat rooms.

**⚠ Two-character party check** (`two-player-scaling.md`): a duergar checkpoint of 4 (Room 5) is 800 raw XP at the 3-6 monster multiplier, bumped to ×2.5 for two PCs = 2,000 adjusted — Hard at level 5 (confirmed live, `encounters/kesh-deeps-duergar-outpost.md`), drops to Medium at level 8 with the exact same monster count. The dig-face confrontation (Room 9, the Chief + 2 duergar) scales the same way.

**Scaling for a higher-level party in this range**: before running either fight for a party above level 6, run `py .claude/scripts/encounter_difficulty_check.py <campaign> --raw-xp <N> --count <N>` (defaults to the party's real current level) and add duergar (not HP) until it lands back at Hard — per `two-player-scaling.md`'s own "more enemies, not more HP" default. Do not assume the room's written monster count is level-agnostic just because the header states a range.

---

## Phase 1 — Concept & ecology

**What it was**: An iron mine, worked for generations until a cave-in decades ago made the deeper shafts unsafe and unprofitable to clear. Abandoned by its original owners, left to rot on the surface records as a dead asset.

**Who holds it now**: **Duergar**, arrived from somewhere below in the last several years, have reopened and extended the deepest shafts — not for the iron, which they consider a poor use of the effort. Per `gazetteer.md`'s original hook, **they're mining toward something specific, and they know it**: their own instinct and old duergar mining-lore has them convinced there's a sealed pre-dynastic structure just beyond their current dig line — plausibly connected, at the DM's discretion, to the same ash-king era complex whose surface expression is `the-drowned-cathedral.md`, elsewhere in this same region. They are close. They have not broken through yet.

## Phase 2 — Map (non-linear)

**Verticality is the entire point** — the mine runs in distinct levels: the original surface workings (long abandoned, structurally sound), the mid-level shafts (where the duergar actually live and work), and the new excavation at the bottom (freshly dug, unstable, and closest to whatever they're digging toward). Two entrances exist: the original mine mouth (obvious, likely watched) and a secondary ventilation shaft the duergar themselves use to move ore and supplies without being seen from the main entrance.

## Phase 3 — Room by room

| # | Room | Content | Status |
|---|------|---------|--------|
| 1 | **The Mine Mouth** | The original, obvious entrance — abandoned equipment, a rusted winch still technically functional | ✅ RESOLVED (session 10, day 56) — stealth kill on the entrance guard |
| 2 | **The Ventilation Shaft** | The duergar's actual supply route — narrow, easy to miss, bypasses Room 1's watch entirely | *(PENDING — not confirmed as delivered in play; see `dungeon-design.md`'s 2026-09-01 standing rule)* |
| 3 | **Surface Workings — Old Tunnels** | Structurally sound but empty, the original mine's abandoned reach — ambient signs of the old operation (broken carts, a collapsed support beam) rather than a fight | *(PENDING — not confirmed as delivered in play)* |
| 4 | **The Cave-In** | The blockage that originally ended mining here — the duergar have since cleared and reinforced a path through it, but the old danger is still visible in the walls | ✅ RESOLVED (session 10, day 56) — hazard triggered, 2d6 damage resolved per `bug-log.md`'s trap-ownership fix |
| 5 | **Duergar Outpost** | A guarded checkpoint marking the transition from abandoned mine to active duergar territory — the first real combat encounter for a party pushing deeper | ✅ RESOLVED (session 10, day 56) — Hard-tier fight, per `encounters/kesh-deeps-duergar-outpost.md` |
| 6 | **The Living Quarters** | Where the duergar band actually lives — modest, functional, and where their own mining-lore records (a real Investigation find) explain what they think they're digging toward | *(PENDING — this is the site's Strategic-info payoff room; not confirmed as delivered, see standing rule)* |
| 7 | **The Ore Processing Floor** | Where whatever iron they still bother extracting gets sorted — mundane, but a real environmental-storytelling room showing their actual priorities have shifted away from the mine's original purpose | *(PENDING — not confirmed as delivered in play)* |
| 8 | **The Deep Shaft** | The new excavation itself — unstable, freshly dug, genuinely dangerous footing as its own hazard, separate from any monster | *(PENDING — not confirmed as delivered in play)* |
| 9 | **The Dig Face** | The current end of the excavation — the duergar's leader and remaining strength concentrated here, this close to their goal. A DC check on the exposed rock face confirms something ancient and worked (not natural) lies just beyond — confirmation of the theory, not a full breakthrough yet, leaving the DM room to decide exactly what's on the other side when the party actually gets there | ✅ RESOLVED (session 10, day 56) — Chief + guards fight, then Kriv broke through to the ash-king memorial chamber (Kaelth Ashborn) |

## Phase 4 — Content variety check

- **Combat**: duergar outpost (Room 5), the dig-face confrontation (Room 9)
- **Hazard**: the cave-in (Room 4), the deep shaft's unstable footing (Room 8)
- **Exploration/lore**: the old surface workings (Room 3), the duergar's own mining-lore records (Room 6), the dig face's confirmation of something ancient beyond (Room 9)
- **Treasure**: modest — this is a working mine, not a hoard site; whatever coin/goods the duergar have are practical, not a windfall. The real reward is information (what's actually down there) and, if the party chooses to let them finish, a genuine strategic choice about whether that's wise

## Connections

- `gazetteer.md` — Region III, the Cindermoor
- `locations/the-drowned-cathedral.md` — a plausible, DM's-choice connection to the same ash-king era complex, not yet confirmed
