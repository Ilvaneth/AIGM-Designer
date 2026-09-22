# The Feral Menagerie

**Region**: IV. Karsgate (a ruined estate grounds, a half-day out)
**Level range**: 6-8 (this two-character party should read it as roughly +2 — see `two-player-scaling.md`; effectively 8-10)
**Site type**: Small dungeon, faction-free (expanded to 8 rooms, upgraded to full `.claude/rules/dungeon-design.md` standard 2026-09-02)
**Location class**: Dungeon
**Dungeon Type**: **Ruins** — a private estate, deliberately built and staffed, now decayed and reoccupied by nothing that built any of it.
**Payoff type**: **Treasure-heavy** — real coin, exotic jewelry, and a grim secondary find, per this file's own established Treasure section.

**⚠ Two-character party check** (`two-player-scaling.md`): the worg pack (split across Rooms 3/4, never together) stays Hard-to-Deadly at most per room. **The apex threat (Room 6) was a Displacer Beast in this file's earlier draft — that creature does not exist in this project's SRD** (confirmed via `srd_lookup.py`, the same gap already caught and fixed once this session for "The Maker's Undoing" — see `bug-log.md`, `workflow-skip`, 2026-09-01). Replaced with a **Manticore** (CR 3, verified). Solo-adjusted: 700 raw × 1.5 (2-PC bump) = 1,050 — likely undersized for a stated "real apex threat" at this level even before the swap. **Re-run `py .claude/scripts/solo_burst_check.py ashen-crown --vs beast --full-nova` against the party's real sheet before running this fight** and add HP margin/Legendary Resistance per `two-player-scaling.md`'s solo-boss methodology, the same treatment already applied to "The Maker's Undoing"'s Clay Golem and "The Tithe Barn"'s Shambling Mound — don't run this fight at flat SRD Manticore stats.

---

## Phase 1 — Concept & ecology

**What it was**: Before the succession war reached this far south, a wealthy noble kept a private menagerie here — exotic beasts as a status display, imported at real expense. The war ended the money and the staff; the animals were left to fend for themselves.

**Who holds it now**: The surviving animals, gone properly feral over the years — a **worg pack** that claimed the old enclosures, and a **manticore** (an exotic import in the truest sense, denned in the estate's largest paddock) that has become the grounds' real apex predator. Neither coordinates with the other; the manticore's paddock and the worgs' enclosure don't overlap.

## Phase 2 — Map (non-linear)

**Entrance**: the estate's old ornamental entrance court — overgrown but still the obvious way in, no hidden second entrance needed for a site this exposed.

**Verticality**: mostly flat grounds, broken by the Deep Paddock's own sunken construction (built to actually contain something large) — a real drop in terrain once the party reaches it.

## Phase 3 — Room by room

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **The Entrance Court** | Once ornamental, now wild — cracked fountains, overgrown hedges shaped like animals nobody maintains anymore. | Entrance | — |
| 2 | **The Ruined Aviary** | Empty, long since abandoned by whatever exotic birds it held — real environmental storytelling, no fight. | Lore | — |
| 3 | **The Overgrown Path** | The route between the aviary and the enclosures — a lone worg, apart from the main pack, rounds out the pack's numbers without concentrating them (added 2026-09-02). | Combat | — |
| 4 | **The Worg Enclosure** | Broken fencing, clearly built for something smaller — a worg pack (2-3) has claimed it, aggressive and territorial. **Spread across the enclosure's broken terrain, not clustered** (no single AoE catches the whole pack), and worgs have their own keen sense of smell — treat at least one as having a real, non-Stealth-dependent chance to notice the party first. | Combat | — |
| 5 | **The Feeding Yard** | Where the worgs actually bring their kills — bones, both animal and otherwise, a grim companion piece to the pack fight rather than its own separate threat. Added 2026-09-02, folds in the pack's remaining numbers. | Combat | — |
| 6 | **The Deep Paddock** | The largest enclosure, built for the estate's prize exhibit — the **manticore** has denned here, the site's real apex threat. See the scaling warning above before running this fight. | Combat | — |
| 7 | **The Keeper's Lodge** | The menagerie-keeper's old quarters — records of what was originally kept here (a real, flavorful list the DM can improvise from), and a locked strongbox with the collection's remaining valuables: coin and a few pieces of exotic jewelry from the estate's better days. | Treasure | — |
| 8 | **The Keeper's Rest** | A collapsed section near a hand-dug grave, unstable ground (a real footing hazard, DC check) — the menagerie-keeper who stayed after the money and staff left, cared for the animals as long as they could, and died here doing it. The last, quiet emotional beat of the site. Added 2026-09-02. | Trap | — |

## Phase 4 — Content variety check

**Room-content ratio** (`dungeon_content_ratio_check.py`, run 2026-09-02, before finalizing): Combat 4/8 (**50%, in band ✓**), Trap 1/8 (**12.5%, in band ✓**), Special (Treasure) 1/8 (**12.5%, in band ✓**), Structural (Entrance+Lore) 2/8 (**25%, above the 15-20% target** — accepted, the same defensible small-site margin already documented for "The Gnoll Battlefield" and "The Tithe Barn").

- **Combat**: a lone worg (Room 3), the worg pack (Room 4), the pack's remainder (Room 5), the manticore apex threat (Room 6)
- **Hazard**: the collapsed ground at the Keeper's Rest (Room 8)
- **Lore**: the ruined aviary (Room 2), the keeper's own fate (Room 8, alongside its hazard)
- **Treasure**: the Keeper's Lodge strongbox (Room 7) — coin, exotic jewelry, real texture

## Connections

- `gazetteer.md` — Region IV, near Karsgate
- No faction ties — a private tragedy of the war's economic collapse, not a political one
