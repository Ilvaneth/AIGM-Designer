# D&D Skill — Travel Encounters

Overland travel is not dead air. Read this file whenever a journey of a day or more begins, alongside `SKILL-combat.md` if a rolled result turns into a fight. The mechanism here is layered and script-backed — the tables themselves are campaign content (kept in the campaign's own `reference/travel-encounters.md`, in whatever language that table runs in), never invented on the spot.

## The mechanism

1. **Roll once per day and once per night of travel, before narrating that leg** — never after, never skipped because the road "seems safe." A quiet result is a real, rolled outcome, not a shortcut.
2. **Two-layer roll**: first a weighted category (Combat / Quiet-Texture / Social / Environmental / Discovery / Faction-Political), then a specific result from that category's own subtable. Both layers are rolled by the script below, never hand-picked.
3. **Tier by party level**: each region defines an Early and a Late tier. Only the Combat subtable escalates between tiers — weather, travelers, and local texture don't scale with character level.
4. Run the roll with:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/travel.py --campaign <name> --region "<region name>" --tier early|late --days N
   ```
   This reads the region's table straight from the campaign's own reference file, rolls for real, prints each day/night's result, and appends every roll to that file's own Roll Log table — so the document and the actual rolls can never disagree.

## Never skip a leg — the reason this file exists

A multi-day journey fast-forwarded with nothing happening is not efficient pacing, it's a missed dimension of the world. Standard 6's "skip the uneventful" instinct applies to genuinely dead time (a scene that has already delivered its content and is now just repeating itself) — it does **not** license skipping a rolled travel leg, a prepared dungeon, or a quest site's own content just to reach a reward faster. **The reward lands at the end of the exploration it was built to reward, not at the first shortcut available.** If a looted map or a piece of information *legitimately* removes the need for a specific room or leg (the party earned the shortcut through play), that's still a choice to surface to the table, not a default the DM takes silently.

## Six things a flat encounter table doesn't do on its own — do them live, every time

**1. Tie Faction/Political results to the campaign's actual clocks.** When the roll lands on this category, do not read a generic flavor line as the final answer — check `state.md → ## Faction Moves` first. If an active faction clock (a patience timer, an investigation, a discovery not yet surfaced) plausibly manifests on this specific road, deliver *that* as the encounter — a rumor, a patrol, a visible sign of the clock advancing — and note it as delivered. Fall back to the region table's own generic line only when nothing active fits.

**2. Track rest and attrition across a multi-leg journey, explicitly.** After each day/night's result resolves, note whether the party takes a short or long rest before the next roll (tie this to `calendar.py rest short|long`, which also advances the clock correctly). Don't let two or three fights in a row pass unremarked while HP, spell slots, and hit dice quietly run dry — if the party is two or more combat nights deep without a long rest, say so plainly before rolling the next leg, the same way `SKILL-combat.md` already insists Action Surge and Second Wind get named instead of assumed.

**3. Scale combat down when the party travels with a real escort.** Per `two-player-scaling.md`'s own standing advice to get this two-person party help: if they're moving with ten or more armed allies (hired muscle, a garrison detachment, a caravan guard), a rolled Combat result resolves as a short, mostly-offscreen victory for the escort — a beat of narration, not a full tracked fight — *unless* the specific table entry is written as an escort-scaled threat (an organized ambush, a hardened patrol built to test a caravan specifically). Don't run the trivial version of a fight as if the party were alone.

**4. Decide bang or texture before narrating, not while narrating.** A result that names a specific, actionable detail — a message naming a location, a demand, a map, someone who recognizes the party — gets delivered as a Standard-13 bang: it forces an immediate choice, no "what do you do?" dead air. A purely atmospheric result (weather, a distant sound, an unremarkable traveler) is texture only — describe it, let the beat pass, don't manufacture urgency it doesn't have. When building or extending a region's table, mark hook-worthy entries so this call doesn't have to be made cold in the moment.

**5. Let Discovery results answer to the world's own open threads.** Before rolling a Discovery subtable, check `state.md → ## Open Threads & Rumours` (and, for a structured/imported campaign, whatever lazy-loaded quest bank applies) for anything that plausibly surfaces on this route. If one fits, manifest that thread instead of a disconnected generic result, and advance or resolve it in `state.md` accordingly. Only fall back to the table's own generic entry when no open thread applies — a Discovery roll should feel like the world remembering what's unresolved, not a random unconnected prop.

**6. A region without its own table is a gap to fill, not a reason to reuse a neighboring one silently.** If travel enters a region the campaign's reference file doesn't cover yet, that's a signal to author a new regional table (same layered format, same six rules) before the next journey through it — not to quietly borrow a different region's flavor and hope it fits. Flag the gap to the table when it's noticed.

## Building or extending a region table

Each region in the campaign's own `reference/travel-encounters.md` needs:
- A level range and a one-line tonal identity distinct from every other region (don't reskin — a swamp-refugee borderland and a folk-horror moor should never produce interchangeable results).
- A weighted d12 Category table (start from 4/12 Combat, 1/12 Quiet-Texture, 1/12 Social, 1/12 Environmental, 3/12 Discovery, 2/12 Faction-Political — this specific table's own starting weights, previously tuned live after combat came up too rarely at an even split; re-tune for *this* table if actual play says otherwise, don't assume the ratio transfers untested).
- Six d6 subtables (one per category) for the Early tier.
- A Late-tier Combat subtable only — the other five categories carry over unchanged.
- Combat entries at unmodified SRD/bestiary stats, difficulty tuned by monster **count**, never by inflating HP — the same standing default `SKILL-combat.md` uses everywhere else.

## Resolving a multi-creature Combat result fairly

A rolled group doesn't get a hand-built encounter file the way a dungeon fight does, so this discipline applies live, from memory, every single roll:
- **Spread them out.** Don't cluster a rolled group tightly enough for one area spell to catch all of them.
- **At least one is plausibly not surprised.** Most creatures worth rolling have their own way of noticing prey — don't default to "the whole group is surprised" just because the party rolled well on Stealth.
- **A named or tougher individual is fine even in a random result** — a rolled group doesn't forbid one member having real HP behind it.
- **Don't over-build these.** Random encounters are texture, not set pieces — no Legendary Resistance, no deliberate HP-buffering past what's fair. That treatment belongs to named bounties and dungeon bosses, not a routine road encounter. The point is only: don't let the *entire* rolled group die in one nova before any of them act — not "make every road fight memorable."

## Logging

Every roll — including a "quiet" result — gets a line in the region file's own Roll Log: route, leg count, each day/night's rolled category and subtable result, and how it was actually resolved in play. `travel.py` appends the roll itself automatically; add the resolution note by hand once the scene plays out, the same way a dungeon encounter's outcome gets written up after the fact.
