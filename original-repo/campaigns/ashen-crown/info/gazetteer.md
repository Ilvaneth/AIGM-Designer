# Gazetteer — The Hollow Kingdoms

The master map. Eight regions, tiered by level, spanning the whole campaign from level 1 to 20.

**The problem this solves**: the original sandbox had one border town, one village, and five nearby sites — so every thread routed back to Gallowmere and the party had nowhere new to go. This is the whole kingdom.

Sites marked **[full]** have their own file in `locations/`. Sites marked **[sketch]** are named, placed, and outlined here — flesh them out when the party heads that way.

---

## Regional Topography & Texture

**Why this exists**: no elevation or physical-geography framework existed anywhere in this file — individual site names implied terrain (a "moor," a "chalk escarpment," a mine) without ever tying them into a coherent map the party's actual journey moves through. Built 2026-08-28 after the DM asked directly whether different regions carry different textures and elevations, and pointed out that terrain should be what determines which creatures roam where — not the reverse. This also grounds `travel-encounters.md`'s existing regional tables in physical logic rather than leaving them as an arbitrary monster list per region.

**The overall shape of the journey**: the party's physical path across Chapter 1 is a real ascent, not a flat crawl — low border country, up into old exposed highland, back down through a river city, up again into chalk country. This isn't decorative; sightlines, weather, and travel difficulty should reflect it every time the party crosses a regional boundary.

| Region | Elevation | Terrain | Signature texture |
|--------|-----------|---------|--------------------|
| I. The Marches | Sea level to low rolling hills | Coastal river-delta borderland — Nettlecombe's coast, Sallow Ford's crossing, the Sunken Barge's marsh | Damp, brackish air; woodsmoke from refugee fires; mud underfoot most of the year; crowded, watchful roads |
| II. The Thornlands | Low-to-moderate rolling hills | Worked farmland, hedgerows, old stone — the kind of country that's been plowed for centuries | Harvest smells, birdsong, old stone farmhouses — undercut by how many of those hills are actually barrows |
| III. The Cindermoor | **High, exposed plateau** — a real climb up from the Thornlands | Treeless moor, older than the dynasty, dotted with hidden lakes (the Drowned Cathedral's lake among them) | Wind that doesn't stop, fog that behaves wrong, peat and heather, grey light even at noon, real isolation |
| IV. Karsgate | Back down to river-valley elevation, but internally tiered | A walled city on a river — the Kingsward sits visibly higher than the Reeks, and the Undercity is below all of it, literally beneath the city's own foundations | Woodsmoke and river-damp in the Reeks and Riverside; incense and old stone in the Kingsward; the Undercity smells like the flood that drowned it, still |
| V. The Ashvale | **Moderate-to-high chalk downland** — climbing again after Karsgate | Chalk escarpments and exposed hill country, pale stone underfoot everywhere | White dust that gets into everything, wind-scoured ridgelines, a starker, paler light than the green Thornlands ever had |
| VI. Emberhold | High, deliberately — an imperial capital built on defensible ground | The seat of a throne nobody currently sits on | To be textured in full when Chapter 2 opens; provisionally: old imperial stone, ash-and-gold Ember Crown iconography everywhere, a city holding its breath |
| VII. The Sundered Reach | **The highest, coldest ground in the campaign** — real mountains and ice | Broken terrain, glaciers, volcanic fire-giant country, ruins older than the current kingdom's memory | Ash-fall mixing with snow, brutal cold, the particular silence of a landscape nothing has successfully lived in for a long time |
| VIII. The Grey Kingdom | Elevation-agnostic — a Shadowfell echo, not a physical place in the normal sense | A mirror of the Hollow Kingdoms, reached through the Crown itself | To be textured in full at the endgame; provisionally: everything is present and slightly wrong, the way a memory is present and slightly wrong |

**Regional hazards already reflect this terrain, not just monster variety** — check before assuming a new one is needed:
- The Marches' stirges "near water" (`travel-encounters.md`) already reflects the delta/marsh ecology
- The Thornlands' undead-heavy table (skeletons, specters, wights at Hallowmere) reflects how much of this "farmland" is actually old grave-ground
- The Cindermoor's weather and will-o'-wisp entries already reflect a genuinely exposed highland, not generic "spooky moor" flavor
- The Ashvale's "chalk country beasts — manticore, chimera" entry already reflects real chalk-downland apex predators

No table needed new entries after this pass — the existing regional tables were already better-grounded in terrain than the elevation framework around them, which is exactly the gap this section closes.

---

## CHAPTER 1 — Levels 1-10

### I. The Marches — *levels 1-4*
The southern border country. Refugees, smugglers, and everyone the capital would rather not see. Poor, crowded, and the only part of the kingdom the war hasn't reached — yet.

**Settlements**
- **Gallowmere** — border town, ~1,200 and swelling. The party's home base and the Chapter 1 prize. **[full]** `locations/gallowmere.md`
- **Sallow Ford** — river crossing two days west. Ironclad Compact toll station; everything moving north pays here. **[full]** `locations/sallow-ford.md`
- **Nettlecombe** — fishing hamlet, ~90 people, downriver. Half-emptied. **[full]** `locations/nettlecombe.md` — the villagers have stopped burying their dead at sea and won't say why.

**Sites**
- **The Drowned Mill** — stirges, ghouls, a smuggler's cache three people want. **[full]**
- **The Weeping Tower** — a dead wizard's failed work on surviving death. Ilvaneth's site. **[full]**
- **Sorrel's Hollow** — deserter camp; Kriv's only living lead. **[full]**
- **The Ash-Kilns** — Cinder Choir cell; best power-base target in Gallowmere. **[full]**
- **The Gallow Tree** — the town's namesake, a great dead oak outside the walls where the old lords hanged people. Nothing grows within twenty feet of it. **[full]** `locations/the-gallow-tree.md` — a **shadow** or two, and something buried at the roots that the Cinder Choir has been leaving offerings for.
- **Riverwatch** — collapsed border watchtower, now a **kobold** warren with a **grick** in the cellars. **[full]** `locations/riverwatch.md` — they've been stripping the road and have accumulated a genuinely odd pile of loot.
- **The Sunken Barge** — a merchant barge wrecked in the shallows, claimed by **lizardfolk** who are more interested in trade than violence if approached correctly. **[full]** `locations/the-sunken-barge.md`

### II. The Thornlands — *levels 3-6*
The agricultural heartland north of the Marches. Farms, hedgerows, small villages. The Vaelthorn line's ancestral country — and where the Concordat has been digging.

**Settlements**
- **Thornwick** — village of ~35 households, the Vaelthorn crypt on its hill. **[full]** `locations/thornwick.md`
- **Harrowgate** — real market town, ~4,000. Temple of the old imperial cult, a proper market, a magistrate. The first place the party can spend serious money. **[full]** `locations/harrowgate.md`
- **Ostwick** — farming village, ~200. **[full]** `locations/ostwick.md` — a **wereboar** in the surrounding woods; the villagers know exactly who it is and are protecting him.
- **Greyholt** — hamlet, under 100, a few hours' walk from Shestendeliath Hold. Named session 10, day 51 — the unnamed "nearest village" whose "the hold doesn't like visitors" rumor kept looters away for fifteen years. Whether any of the old Shestendeliath tenant families still live here is an open question, not yet played — see `info/shestendeliath-restoration.md`'s Phase 2.

**Sites**
- **Shestendeliath Hold** — Kriv's ancestral seat, burned fifteen years ago, garrison still on duty. The Charge-Roll (fragment map), Wardensteel, and the gate ledger that names the traitor. **[full]** `locations/shestendeliath-hold.md`
- **The Vaelthorn Crypt** — emptied by the Concordat, who came back and *left something*. **[full]**
- **The Weeping Wood** — old-growth forest between Thornwick and Harrowgate. **Ettercaps**, **giant spiders**, and a **dryad** who will bargain. **[full]** `locations/the-weeping-wood.md` — the dryad remembers the ash-kings and is the oldest living witness in the region.
- **The Tithe Barn** — abandoned granary, now an **ochre jelly** and **swarm** problem, plus three seasons of hoarded grain the refugee camp desperately needs. **[full]** `locations/the-tithe-barn.md` — direct power-base fuel.
- **Hallowmere Chapel** — ruined roadside chapel. **Specters**. **[full]** `locations/hallowmere-chapel.md` — the chapel's burial register survives and names Crown-era interments.

### III. The Cindermoor — *levels 4-8*
Bleak, treeless moor country. Older than the dynasty, older than the kingdom. Nothing farms here and the people who stayed are strange about it.

**Settlements**
- **Cair Dunnow** — moor village, ~150, insular, unfriendly, practices funeral rites nobody else does. **[full]** `locations/cair-dunnow.md` — they know more about the ash-kings than any scholar and will not tell outsiders.

**Sites**
- **Hollowmoor Barrows** — the great false lead. No fragment; the truth about the Crown's price. **[full]**
- **The Drowned Cathedral** — a pre-dynastic temple sunk into a moor lake. **Water elementals**, **wights**, and a **shambling mound** in the flooded nave. **[full]** `locations/the-drowned-cathedral.md` — where the Crown was *forged*, not where a piece is hidden.
- **Kesh Deeps** — abandoned iron mine. **Duergar** have moved in from below and are extending it. **[full]** `locations/kesh-deeps.md` — they're mining toward something and they know it.
- **The Harpy Crags** — rocky outcrops, a **harpy** flight, and the wreckage of everyone who listened. **[full]** `locations/harpy-crags.md`
- **The Maker's Undoing** — a solitary artificer-wizard's sealed private vault, carved into a Cindermoor mountainside. Faction-free, standalone — no one's claim but its own. **[full]** `locations/the-makers-undoing.md`

### IV. Karsgate — *levels 5-10*
**The city.** Regional seat, ~30,000 people, walls, guilds, nobility, an undercity, and open chapterhouses for both the Concordat and the Compact. This is where Chapter 1's politics happen and where a party with a power base becomes a party with *reach*.

**[full]** `locations/karsgate.md` — districts, factions, NPCs, and the undercity.

**Sites near Karsgate — five faction-free neutral sites, built 2026-08-29**
- **The Gnoll Battlefield** — an old war skirmish site, scavenged by a gnoll pack. **[full]** `locations/the-gnoll-battlefield.md`
- **The Giant's Cairn** — a burial mound claimed by a lone ogre, Grask Bonepile. **[full]** `locations/the-giants-cairn.md`
- **The Feral Menagerie** — a ruined noble's exotic-beast pit, now feral (worgs, a displacer beast). **[full]** `locations/the-feral-menagerie.md`
- **The Driftway Fair** — a recurring, faction-blind traveling market. **[full]** `locations/the-driftway-fair.md`
- **The Unremembered Shrine** — a hidden, pre-schism temple to Ossara, unknown to any faction. Level 9-10, deliberately high — a real "return when ready" site. **[full]** `locations/the-unremembered-shrine.md`

**Karsgate's immediate hinterland — four map-derived sites, built 2026-08-29**
- **The Mill** — a watermill outside the walls, its independent miller under quiet Ironclad Compact pressure to fold into the Grain Exchange. **[full]** `locations/the-mill.md`
- **Outer Farm** — a working farm using war refugees as under-terms labor; a moral-choice site, no faction ties. **[full]** `locations/outer-farm.md`
- **The Caravan Halt** — a recurring waystation on the Karsgate road, a day out from the city; the last reliable stop for road news before arrival. **[full]** `locations/the-caravan-halt.md`
- **Stonebridge** — the old river-crossing checkpoint on the Karsgate road, city-watch controlled but quietly pressured by the Concordat to flag travelers matching certain descriptions. **[full]** `locations/stonebridge.md`

### V. The Ashvale — *levels 8-10*
The chalk country in the north. Ancestral ground of the Ashvale line — minor nobility three generations before they became the Ironclad Compact's ruling family.

**Settlements**
- **Ironhold** — Compact fortress-town, ~8,000, functionally a company headquarters with walls. **[full]** `locations/ironhold.md` — Coren Ashvale is here when he's anywhere.

**Sites**
- **Ashvale Necropolis** — Concordat's working seat, where the fragments go. **Chapter 1 climax.** **[full]**
- **The Chalk Warrens** — natural cave system beneath the necropolis. **Otyugh**, **carrion crawlers**, and the way in that isn't the front gate. **[full]** `locations/the-chalk-warrens.md` — confirmed as the necropolis's own "way in," not just a nearby cave

---

## CHAPTER 2 — Levels 11-20

### VI. Emberhold, the Capital — *levels 11-14*
The imperial city. An empty throne, a paralyzed court, and three factions maneuvering openly in the streets. Chapter 2 opens here: the stakes stop being regional and the party's Chapter 1 power base becomes their credential to be in the room at all.

**Key locations** **[sketch]**
- **The Hollow Throne** — the palace. Nobody sits in the throne room; the court meets in an antechamber because of what happens to people who linger.
- **The Grand Archive** — Concordat power center. Proof the Concordat engineered the Emperor's death is filed here.
- **The Ember Quarter** — burned in the riots after the Emperor's death, never rebuilt, now ruled by whoever's strongest that month.
- **The Cinder Cathedral** — the Choir's public face, tolerated because nobody dares close it.

**Threats**: **rakshasa** and **doppelganger** infiltrators in the court, **oni**, **vampire** nobility, assassins, and political warfare where the wrong conversation is more lethal than a fight.

### VII. The Sundered Reach — *levels 13-17*
The far north, beyond the kingdom's writ. This is where the old realms were before the Hollow Kingdoms — the ash-kings' actual country. Broken terrain, ruins older than history, and things that were never driven out because nobody ever tried.

**Sites** **[sketch]**
- **Frostmere** — a frozen lake with an **adult white dragon** beneath it, and a Crown fragment in its hoard, taken as tribute centuries ago.
- **The Bonewrights' Hall** — where the Crown was broken. **Liches**, **wraiths**, and the surviving records of the men who decided to shatter it.
- **Kar Vaelth** — the first ash-king's seat. **Giants** squat in the ruins. **Fire giants** and a **stone giant** oracle who remembers.
- **The Screaming Fen** — **hags**, **will-o'-wisps**, a coven who trade in exactly the kind of knowledge Ilvaneth wants and price it accordingly.

### VIII. The Grey Kingdom — *levels 17-20*
Not a place on the map. A Shadowfell echo of the Hollow Kingdoms, reached through the Crown itself or through the deepest sites. This is where the last ash-king went when he assembled the Crown and stopped being himself.

**The endgame.** **[sketch]**
- **The Ash Court** — a mirror of Emberhold, populated by everyone who ever wore the Crown, all of them still there, all of them still *reigning*.
- **The Grey Throne** — where a completed Ashen Crown must be brought.
- **The Last Ash-King** — not a corpse. Still ruling. The campaign's true final antagonist, and the answer to what Ilvaneth is actually asking for.

**Threats**: **liches**, **death knights** (reskinned SRD), **wraiths** and **specters** in numbers, **shadow dragons**, and the Crown's own price.

---

## Region Control

**Living tracker, not flavor text** — lives here (not a separate file) per `world-reactivity-design.md`'s single-source-of-truth reasoning. Updated whenever `world-events.md`'s d12 table rolls a 1 or 2, or a session's play directly changes who holds a region. When control changes, it must be a real, integrated change: which faction has visible presence and NPCs reachable there, prices, available jobs — not a line nobody acts on.

| Region | Current control | How it could change |
|--------|-----------------|----------------------|
| I. The Marches | Contested — no single power; Ironclad Compact toll station at Sallow Ford, garrison at Gallowmere nominally crown but Compact-retained | Refugee pressure, a garrison defection, either major faction moving in force |
| II. The Thornlands | Local self-governance (Thornwick, Harrowgate); Ashlord Concordat has active excavation presence (Vaelthorn crypt, ongoing digs) but no territorial claim | Concordat formalizing its dig-site presence into real control, or Harrowgate's Compact-retained Garrison House tipping into open control (`npcs/renata-kroll.md`'s standing offer is the party's own lever here) |
| III. The Cindermoor | Unclaimed — Cair Dunnow is insular and self-isolating, no faction has bothered to try | Very low priority for any faction; would take a deliberate push (a fragment site being discovered here, e.g. the Drowned Cathedral) |
| IV. Karsgate | Contested — both Concordat and Compact hold open chapterhouses, neither dominant | Undercity territory shifts, a chapterhouse-level incident, either faction consolidating visible civic influence |
| V. The Ashvale | Split — Ironclad Compact (Ironhold, ancestral Ashvale seat) vs. Ashlord Concordat (Ashvale Necropolis, occupied territory per `faction-subplots.md`'s Coren Ashvale fracture) | This is the single most volatile region on the map — see `campaign-clock.md`'s "Compact patience" clock (~day 120) for the scheduled version of this tension |
| VI. Emberhold | Power vacuum — empty throne, paralyzed court, three factions maneuvering openly (Chapter 2) | Not yet relevant at Chapter 1 pace; tracked here for when the campaign reaches it |
| VII. The Sundered Reach | No mortal control — ash-kings' abandoned country, monsters and ruins | Effectively static until Chapter 2's endgame content engages it |
| VIII. The Grey Kingdom | The Last Ash-King — absolute, unchallenged | Static; this is the endgame's own antagonist, not a contestable region |

---

## Where the fragments are

The Crown was broken into pieces and scattered. Known and suspected:

| # | Location | Status |
|---|----------|--------|
| 1 | Gallowmere ossuary | **Party holds it** — very likely the Shestendeliath fragment; see `kriv-thread.md` |
| 2 | Vaelthorn crypt, Thornwick | Taken by Concordat → Ashvale Necropolis |
| 3 | *(named in the delivery order as "third")* | Concordat holds it |
| 4 | Frostmere — a white dragon's hoard | Untouched, Sundered Reach |
| 5 | The Drowned Cathedral, Cindermoor | Not a fragment site — the **forge** |
| ? | Remainder | Unplaced — leave room for the table's discoveries |

Do not fix the total number yet. Let the count firm up as the party learns more; it's better to have room than a locked answer.

**The map to the rest is the Charge-Roll** at Shestendeliath Hold — the Ash-Warden houses' sworn record of which house was charged with which fragment. It comes to the party through *Kriv's inheritance*, not Ilvaneth's research. Keep it that way.
