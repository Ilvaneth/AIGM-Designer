# The Chalk Warrens

**Region**: V. The Ashvale
**Level range**: 7-9 (a lead-in to Ashvale Necropolis, level 8-10 — see `two-player-scaling.md`)
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard — **the way into the Chapter 1 climax that isn't the front gate**
**Location class**: Dungeon
**Dungeon Type**: **Cave Complex** (per Phase 0's DMG taxonomy, added 2026-09-02) — "a natural cave system," explicit in this file's own Phase 1 opening line. Nothing here was built except the Worked Threshold onward, which belongs to the necropolis, not this site.
**Payoff type**: **Treasure-heavy** — the Ashvale family vaults (Room 9) are real, substantial grave-wealth, plus genuine political weight with Coren Ashvale.

---

## Phase 1 — Concept & ecology

**What it is**: A natural cave system carved into the same chalk escarpment as Ashvale Necropolis itself, running directly beneath it. **This is the confirmed answer to the necropolis file's own "way in" question** — the Concordat garrisons the necropolis's formal entrance and working areas heavily, but has never bothered securing the Warrens because they lead only to the **Ashvale family vaults**, which the Concordat considers untouched, irrelevant ground, not the working archive they actually care about.

**Ecology**: An **otyugh** and several **carrion crawlers** have lived in these caves for generations, feeding on whatever seeps down from above — entirely natural, entirely incidental to the Crown plot. They don't know or care what's happening in the necropolis proper above them.

## Phase 2 — Map (non-linear)

**Multiple entrances**: a natural sinkhole opening onto the moor surface (the way in, unmarked and unguarded), and — at the Warrens' upper end — a worked passage leading directly into the Ashvale family vaults, which in turn connect to the necropolis's own lower levels. **This is the actual bridge between "a cave full of monsters" and "the Chapter 1 climax."**

**Verticality**: the caves descend from the surface sinkhole, level out through the main cavern system, then climb again toward the worked vault entrance — a real up-down-up profile, not a flat crawl.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Sinkhole** | The unmarked surface entrance — easy to miss without knowing to look for it (a Perception/Survival check, or Coren's own information, per `npcs/coren-ashvale.md`) | Entrance | — |
| 2 | **The Descent** | A natural, uneven shaft down — a real climbing/falling hazard, not a fight | Trap | — |
| 3 | **The Dripping Hall** | A lone, outlying carrion crawler (a scout from Room 4's group) — mineral formations, ambient water sound, and clearer sign (webbing, old kills) of the larger tangle ahead. Added 2026-09-02, per the DMG content-ratio fix — the site's own established creature, not a new one. | Combat | — |
| 4 | **The Carrion Tangle** | Carrion crawlers, 2-3, in a narrow, low-ceilinged section that favors their reach over the party's formation | Combat | — |
| 5 | **The Bone Wash** | 2 more carrion crawlers, drawn to the bone-collection like the rest of their kind (Phase 1 already established "several" living in these caves, not just Room 4's group) — centuries of runoff have collected old bones, human and otherwise, unsettling environmental storytelling and a real (if grim) search opportunity once the crawlers are dealt with. Combat added 2026-09-02, per the DMG content-ratio fix. | Combat | — |
| 6 | **The Otyugh's Den** | The otyugh's territory, deeper in — foul, avoidable with caution, and per the standing dungeon-density rule, guards nothing of Crown relevance itself, just its own meal | Combat | — |
| 7 | **The Chalk Falls** | A genuinely striking natural feature — flowstone formations lit by whatever light source the party's carrying, a moment of pure atmosphere between combat rooms | Lore | — |
| 8 | **The Worked Threshold** | A last carrion crawler straggler, drawn this far by the scent of whatever the Ashvale vaults hold — still natural cave ecology, not a Concordat presence (the file's own established fact that they don't bother securing this route stays true). Where natural cave gives way to deliberately cut stone — the unmistakable sign the party has reached something built, not found. Combat added 2026-09-02. | Combat | — |
| 9 | **The Ashvale Family Vaults (Outer)** | Untouched by the Concordat, exactly as the necropolis file promises — real Ashvale grave-wealth, a separate treasure and a separate political object from anything Sarelle's project cares about | Treasure | — |
| 10 | **The Vault Stair** | The final passage up into the necropolis's own lower levels — **the actual seam between this site and `locations/ashvale-necropolis.md`**, where the DM picks up the necropolis's own content | Entrance | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02): Combat 5/10 (**50%, in band ✓**, up from an original 30% — Rooms 5 and 8 gained real fights, using the site's own already-established creatures, per DM decision to fix rather than accept), Trap 1/10 (**10%, in band ✓**), Special 1/10 (**10%, in band ✓**), Structural 3/10 (**30%, above the 15-20% target** — accepted, this site is structurally a lead-in corridor between two other locations, with two necessary seam rooms (Sinkhole entrance, Vault Stair exit) plus one deliberate atmosphere breather (Chalk Falls); the same class of defensible gap as "The Maker's Undoing"'s own Structural shortfall).

- **Combat**: carrion crawlers (Room 4), the otyugh (Room 6) — both avoidable with the right approach, not forced
- **Hazard**: the descent (Room 2)
- **Exploration/atmosphere**: the Bone Wash (Room 5), the Chalk Falls (Room 7) — real sensory and tonal beats, not just connective tissue
- **Treasure**: the Ashvale family vaults themselves (Room 9) — genuine grave-wealth, untouched, and per the necropolis file's own note, "a separate treasure and a separate political object" from the Crown plot specifically. Recovering or disturbing it has real weight with Coren Ashvale, who cares about this ground personally.

## Running this well

**This is a lead-in, not a self-contained dungeon** — Room 10 hands off directly into `ashvale-necropolis.md`'s own content. Don't resolve the necropolis climax by extension just because the party found the back door; treat the seam as a real transition, with its own tension (they're now inside, undetected, with everything that implies) rather than a free pass to the ending.

## Connections

- `locations/ashvale-necropolis.md` — the site this leads directly into; the confirmed answer to that file's "way in" question
- `npcs/coren-ashvale.md` — plausibly the source of information about the sinkhole entrance, as part of his "deniable instrument" offer
- `locations/ironhold.md` — the Ashvale family's other remaining ground, a thematic echo of what's found untouched here
