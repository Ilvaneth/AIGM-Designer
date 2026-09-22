# Travel Encounters — Ashen Crown

Roll d10 per day/night of overland travel **before** narrating the journey. Log every roll below. Tables are regional — see `gazetteer.md` for the map.

**Narrate nights by their absolute in-fiction day number, not a per-journey counter.** Added 2026-08-30, DM-proposed, after a relative "Night 1"/"Gece 1" convention repeatedly collided with `travel_roll_check.py`'s own detection of it (recapping a past journey's "Night 1" kept re-triggering the check meant to catch a FRESH unrolled night). Write "Gece 49" (the actual `state.md` day), never "Gece 1" meaning "the first night of this particular leg" — this also gives the table a real, unambiguous anchor for which calendar day a given night was, instead of "which journey's Night 2 was this again." `travel_roll_check.py` now checks the mentioned day number directly against `state.md`'s current day, which is both more precise than the old heuristic and immune to the recap collision by construction — a reference to a past day can never equal today's day.

**Roll them for real.** These tables are parsed directly by `roll.py`, so the results and this document can never disagree:

```bash
py .claude/scripts/roll.py --travel ashen-crown thornlands 5
```
```bash
py .claude/scripts/roll.py --tables ashen-crown
```

Never hand-pick a number and call it a roll — use the script, then log the result below.

Monster references are SRD entries; look up with `py .claude/scripts/srd_lookup.py monster "X"`.

**Before resolving any multi-creature result into an actual encounter — read this every time, not just the first time:** per `two-player-scaling.md`'s group-specific techniques (added 2026-08-29), a random encounter doesn't get a pre-built file the way a dungeon fight does, so this discipline has to be applied live, from memory, every single roll:
- **Spread them out.** Don't cluster a rolled group tightly enough for one Thunderwave/Fireball to catch all of them.
- **At least one is plausibly not surprised** — most of these creatures (wolves, goblins, undead, harpies) have their own way of noticing prey; don't default to "the whole group is surprised" just because the party rolled well on Stealth.
- **A named or tougher individual is fine even in a random result** — a goblin band's roll doesn't forbid one goblin having real HP behind it, the same way Roskel did.
- **Don't over-build these.** Random encounters are texture, not set pieces — no Legendary Resistance, no deliberate HP-buffering past what's fair. That treatment is for named bounties and dungeon bosses (`regional-threats.md`, boss rooms), not a routine road encounter. The point here is just: don't let the *entire* rolled group die in one nova before any of them act, not "make every road fight memorable."

---

## The Marches (Gallowmere ↔ Sallow Ford ↔ southern roads) — levels 1-4

**Layered format, added session 9, 2026-08-30** — see the Thornlands section above for how this works. Content here is deliberately its own flavor, not a reskin: the Marches is a **refugee-heavy, war-torn borderland** on marsh/wetland terrain near Sallow Ford, not Thornlands' forest-and-old-dead. Living threats (goblins, bandits, wildlife) dominate here; the undead theme hasn't reached this region yet in the fiction.

**Tier**: use **Early** below level 3, **Late** at level 3-4 (the top of this region's own range) or on a significant return visit once the party has clearly outgrown it.

### Early tier

#### Category

**Weighted d12, set 2026-08-30 (DM-specified: 4/12 Combat, 1/12 Quiet/Texture, 1/12 Social, 1/12 Environmental, 3/12 Discovery, 2/12 Faction/Political)** — replaces the original even d8 split after live dev-mode testing showed combat coming up too rarely.

| d12 | Category |
|-----|----------|
| 1-4 | Combat |
| 5 | Quiet/Texture |
| 6 | Social |
| 7 | Environmental |
| 8-10 | Discovery |
| 11-12 | Faction/Political |

#### Quiet/Texture

| d6 | Result |
|----|--------|
| 1 | Cart ruts run deep in dried mud — this road sees real traffic |
| 2 | A burned-out homestead, long cold — the war got here first |
| 3 | Reeds and marsh grass line the road; frogs everywhere at dusk |
| 4 | A scarecrow in a field, oddly well-kept — someone still tends this land |
| 5 | Distant lowing of cattle — a farm still working, for now |
| 6 | A weathered signpost, half its names scratched out |

#### Social

| d6 | Result |
|----|--------|
| 1-2 | A refugee family or small group, heading toward Gallowmere |
| 3 | A Compact toll collector, off duty, willing to talk for a coin |
| 4 | A peddler with a cart of odds and ends — cheap goods, better rumors |
| 5 | A one-armed veteran, walking home from the war |
| 6 | Children playing at "soldiers" near a farmstead — a grim little detail |

#### Environmental

| d6 | Result |
|----|--------|
| 1 | The road turns to standing water after rain — slow going |
| 2 | A sudden downpour, no shelter in sight |
| 3 | Marsh gas — an eerie smell, harmless but unsettling |
| 4 | A rickety plank bridge over a swollen ditch |
| 5 | Thick morning mist off the wetlands, burns off by midday |
| 6 | Biting insects swarm near standing water — miserable, not dangerous |

#### Combat

| d6 | Result |
|----|--------|
| 1 | Goblin band — 4x Goblin (SRD, unmodified) |
| 2 | Wildlife — 3x Wolf, 2x Boar, or 4x Giant Rat near a farmstead |
| 3 | Deserters/bandits demanding a toll — 3x Bandit |
| 4 | Stirges near standing water — 4x Stirge |
| 5 | A desperate refugee turned highwayman — 1x Bandit Captain (solo; may resolve without violence) |
| 6 | Two factions' patrols cross paths nearby — tense, not necessarily hostile to the party at first |

#### Discovery

| d6 | Result |
|----|--------|
| 1 | A distant, unmarked structure off the road — a ruined watchtower, mill, or shrine, worth the detour |
| 2 | Wagon tracks veer sharply off the main road, days old, toward something out of sight |
| 3 | A local farmer's warning about a "bad patch" of land nearby — obviously hiding something |
| 4 | A crude but specific hand-drawn map, dropped or hidden, pointing to a real nearby site |
| 5 | Smoke rising from a spot that shouldn't have anyone living there |
| 6 | An old boundary marker, freshly re-carved beneath the weathering — someone's been back recently |

#### Faction/Political

| d6 | Result |
|----|--------|
| 1 | A Compact toll patrol — the real business of Sallow Ford |
| 2 | Concordat scouts passing, watching more than acting |
| 3 | A recruitment poster nailed to a dead tree |
| 4 | Two factions' patrols pass each other without incident — tense, wary |
| 5 | A courier riding hard, ignoring the party entirely |
| 6 | A checkpoint demanding papers — Compact-run, bribable |

### Late tier (level 3-4, or a significant return visit)

Quiet/Texture, Social, Environmental, Discovery, and Faction/Political are unchanged from Early. Only **Combat** escalates:

#### Combat

| d6 | Result |
|----|--------|
| 1 | Goblin band, reinforced — 6x Goblin + 1x Goblin Boss (all SRD, unmodified) |
| 2 | Wildlife, bolder — 5x Wolf, or 1x Owlbear (solo) |
| 3 | Bandits, organized — 5x Bandit + 1x Bandit Captain |
| 4 | Stirges, worse — 6x Stirge |
| 5 | The highwayman has built a small gang — 1x Bandit Captain + 3x Bandit |
| 6 | A faction patrol turns hostile — a real skirmish, 3x Scout |

## The Thornlands (Gallowmere ↔ Thornwick ↔ Harrowgate) — levels 3-6

**Layered format, added session 9, 2026-08-30** — roll Category first (Layer 1), then roll on that category's own subtable (Layer 2). Built as the template region for this format; see `two-player-scaling.md` and `bug-log.md` (`combat-geometry`) for why: single-line combat results were being improvised live with no check against party burst, which is exactly the failure class that produced tonight's HP-sizing bugs. Every Combat subtable entry below is pre-authored at **unmodified SRD stats, difficulty tuned by count** — the standing default — never inflated HP.

**Tier**: use **Early** below level 6, or before `consequences.md`'s "Sarelle Duskbourne — Pattern of Losses" threshold has fired. Switch to **Late** once either condition is met — this mirrors `bestiary.md`'s own signature-creature escalation rule (a level 5+ party should be seeing Wights/Specters, not still Skeletons) rather than inventing a new threshold system.

### Early tier

#### Category

**Weighted d12, set 2026-08-30 (DM-specified: 4/12 Combat, 1/12 Quiet/Texture, 1/12 Social, 1/12 Environmental, 3/12 Discovery, 2/12 Faction/Political)** — replaces the original even d8 split after live dev-mode testing showed combat coming up too rarely.

| d12 | Category |
|-----|----------|
| 1-4 | Combat |
| 5 | Quiet/Texture |
| 6 | Social |
| 7 | Environmental |
| 8-10 | Discovery |
| 11-12 | Faction/Political |

#### Quiet/Texture

| d6 | Result |
|----|--------|
| 1 | Fair weather; a distant village bell marks the hour |
| 2 | A large deer herd's tracks cross the road, undisturbed in days |
| 3 | A cold, day-old campfire — someone else's road, not yours |
| 4 | Wildflowers unusually thick this stretch |
| 5 | An hour of light rain, then clear — mud, no real delay |
| 6 | A distant smoke column — a controlled burn, farmers clearing fields |

#### Social

| d6 | Result |
|----|--------|
| 1-2 | Merchant convoy — trade, news, or a job offer |
| 3 | Refugees heading south, with news of the north |
| 4 | A traveling minstrel or storyteller — a rumor for the price of a drink |
| 5 | A circuit priest of the Ember Crown, moving between shrines |
| 6 | A local hunting party — minor trade, local knowledge |

#### Environmental

| d6 | Result |
|----|--------|
| 1 | Fog rolls in, visibility drops |
| 2 | A storm forces early shelter |
| 3 | A washed-out stretch of road — detour, lost time |
| 4 | A swollen creek crossing — a check or a delay |
| 5 | Unseasonable cold — minor exhaustion risk without proper gear |
| 6 | A fallen tree blocks the road — a minor, bypassable obstacle |

#### Combat

| d6 | Result |
|----|--------|
| 1 | Toll gang — 3x Bandit (SRD, unmodified) |
| 2 | Beasts — 2x Giant Spider, or 1x Owlbear (solo) |
| 3 | Undead — roll d4: 1) 3x Skeleton 2) 2x Specter 3) 1x Wight + 2x Skeleton 4) 4x Skeleton (all SRD, unmodified) |
| 4 | Wolf pack — 4x Wolf |
| 5 | Concordat party, undead honor guard escort. **Dangerous** — the party is carrying a fragment. Scale per `consequences.md`'s Pattern-of-Losses state if it's already fired |
| 6 | A rival relic-hunter or Grey Tally operative — solo, may resolve as Social instead of Combat depending on approach |

#### Discovery

| d6 | Result |
|----|--------|
| 1 | A weathered signpost pointing toward a place not on any map the party carries |
| 2 | A freshly cut trail marker leading off the road, into the trees |
| 3 | Distant ruins glimpsed through a break in the canopy — worth investigating |
| 4 | A dead courier's undelivered message, naming a specific location |
| 5 | An old shrine, half-swallowed by roots, visible just off the path |
| 6 | Fresh grave-digging, recent, leading back toward wherever the digger came from |

#### Faction/Political

| d6 | Result |
|----|--------|
| 1 | A Compact courier passing through — not hostile, bribable for information |
| 2 | A Concordat inspection party, observed at a distance — avoidable |
| 3 | Evidence of recent faction activity — burned banners, a skirmish site |
| 4 | A recruiting party for one of the three factions |
| 5 | A real checkpoint/toll manned by an actual faction, not bandits |
| 6 | A rumor or notice posted at a crossroads shrine — draw from `rumors.md` |

### Late tier (level 6+, or Pattern-of-Losses fired)

Quiet/Texture, Social, Environmental, Discovery, and Faction/Political are unchanged from Early — weather, travelers, and local texture don't scale with party level. Only **Combat** escalates, per `bestiary.md`'s signature-creature rule:

#### Combat

| d6 | Result |
|----|--------|
| 1 | Toll gang, hardened — 4x Bandit + 1x Veteran (SRD, unmodified) |
| 2 | Beasts — 3x Giant Spider, or 2x Owlbear |
| 3 | Undead, escalated — roll d4: 1) 2x Wight 2) 1x Wight + 2x Specter 3) 3x Specter 4) 1x Ghast + 2x Wight (all SRD, unmodified) |
| 4 | Wolf pack, larger — 6x Wolf |
| 5 | Concordat party, hardened per the Pattern-of-Losses consequence — larger escort, a named investigator-tier priest (see `npcs/`), decoys possible |
| 6 | A rival relic-hunter's own hired muscle accompanies them now — no longer solo |

## The Cindermoor — levels 4-8

**Layered format, added session 9, 2026-08-30** — see the Thornlands section above for how this works. Deliberately distinct from both Thornlands (organized old-dead, forest) and the Marches (mundane war-refugee borderland, marsh): the Cindermoor is **isolated folk-horror moorland** — Cair Dunnow's insular unfriendliness, barrows, will-o'-wisps, a landscape that feels actively strange rather than merely dangerous. Nothing here answers to a faction; per `gazetteer.md`'s Region Control table the Cindermoor is unclaimed, and faction presence should read as an intrusion, not routine business.

**Tier**: use **Early** below level 7, **Late** at level 7-8 (the top of this region's own range).

### Early tier

#### Category

**Weighted d12, set 2026-08-30 (DM-specified: 4/12 Combat, 1/12 Quiet/Texture, 1/12 Social, 1/12 Environmental, 3/12 Discovery, 2/12 Faction/Political)** — replaces the original even d8 split after live dev-mode testing showed combat coming up too rarely.

| d12 | Category |
|-----|----------|
| 1-4 | Combat |
| 5 | Quiet/Texture |
| 6 | Social |
| 7 | Environmental |
| 8-10 | Discovery |
| 11-12 | Faction/Political |

#### Quiet/Texture

| d6 | Result |
|----|--------|
| 1 | The ground is spongy underfoot; boot-prints fill with dark water behind you |
| 2 | A ring of pale mushrooms, unnaturally perfect, just off the path |
| 3 | Distant, wordless singing carried on the wind — gone when you stop to listen |
| 4 | Sun-bleached sheep bones, arranged in a neat row along a fence line |
| 5 | The moor's own silence — no birds, no insects, just wind through heather |
| 6 | A moss-covered standing stone, older than anything else in the region |

#### Social

| d6 | Result |
|----|--------|
| 1-2 | Moor folk from Cair Dunnow — suspicious, unhelpful, watching from a distance |
| 3 | A relic-hunter working the same ground, wary of competition |
| 4 | A traveling tinker who knows the safe paths through the barrows |
| 5 | An old moor-woman who trades cryptic advice for a small kindness |
| 6 | A funeral procession from Cair Dunnow — the party is not welcome to approach |

#### Environmental

| d6 | Result |
|----|--------|
| 1 | Fog that doesn't behave — thickens and thins with no wind to explain it |
| 2 | A storm forces shelter in a barrow — a real complication, not just flavor |
| 3 | Boggy ground — a failed check means sinking to the waist |
| 4 | Will-o'-wisps flicker at the path's edge, tempting a wrong turn |
| 5 | An unnatural cold spot, gone as quickly as it came |
| 6 | The moor's own disorientation — a check to avoid walking in a circle |

#### Combat

| d6 | Result |
|----|--------|
| 1 | Harpies from the Crags — 3x Harpy (SRD, unmodified) |
| 2 | Wights or specters from an opened barrow — roll d4: 1) 2x Wight 2) 1x Wight + 2x Skeleton 3) 3x Specter 4) 1x Ghast |
| 3 | Hell hound — solo, rare, a sign something worse is near |
| 4 | A will-o'-wisp — solo, leads the party into a real hazard before revealing itself |
| 5 | Moor beasts — a wolf pack, 4x Wolf |
| 6 | Sefwyn Marrow or a rival relic-hunter, here for the same find — may resolve as Social instead |

#### Discovery

| d6 | Result |
|----|--------|
| 1 | A half-collapsed barrow entrance, unexplored, visible from the path |
| 2 | A relic-hunter's abandoned camp — a map left behind, pointing further out |
| 3 | A ring of standing stones, one leaning stone marking a clear direction |
| 4 | Smoke or light flickering where nothing should be, deep in the moor |
| 5 | A trail of disturbed earth leading to a freshly opened barrow |
| 6 | Cair Dunnow markers warning outsiders away from a specific, nearby site |

#### Faction/Political

| d6 | Result |
|----|--------|
| 1 | A single Concordat scholar, alone, cataloguing a barrow — unusual, out of place here |
| 2 | Signs a faction has been probing Cair Dunnow's isolation — and met resistance |
| 3 | A rival relic-hunter crew, openly marking territory |
| 4 | Cair Dunnow's own unofficial watch, warning outsiders off a specific site |
| 5 | Evidence someone official has already been through recently |
| 6 | A faction courier, lost on the moor, asking the party for directions |

### Late tier (level 7-8)

Quiet/Texture, Social, Environmental, Discovery, and Faction/Political are unchanged from Early. Only **Combat** escalates:

#### Combat

| d6 | Result |
|----|--------|
| 1 | Harpies, more of them — 5x Harpy (SRD, unmodified) |
| 2 | Wights/specters, escalated — roll d4: 1) 3x Wight 2) 2x Wight + 2x Specter 3) 1x Ghast + 2x Wight 4) 2x Ghast |
| 3 | A hell hound pack — 2x Hell Hound |
| 4 | Two will-o'-wisps, working together |
| 5 | Moor beasts, bolder — 6x Wolf |
| 6 | The rival relic-hunter crew turns openly hostile — a real confrontation, not a stand-off |

## The Ashvale and the north road — levels 8-10

**Layered format, added session 9, 2026-08-30** — see the Thornlands section above for how this works. Distinct from the other three converted regions: the Ashvale is a **militarized convergence zone** — every faction has real, visible, routine presence here (unlike Cindermoor's "intrusion" framing), open chalk downland terrain, and the Concordat's own working necropolis pulling everything toward it. This is Chapter 1's approach to its climax; faction traffic should feel expected, not anomalous.

**Tier**: use **Early** below level 10, **Late** at level 10 (top of range) or once the party is actually engaging Ashvale Necropolis itself.

### Early tier

#### Category

**Weighted d12, set 2026-08-30 (DM-specified: 4/12 Combat, 1/12 Quiet/Texture, 1/12 Social, 1/12 Environmental, 3/12 Discovery, 2/12 Faction/Political)** — replaces the original even d8 split after live dev-mode testing showed combat coming up too rarely.

| d12 | Category |
|-----|----------|
| 1-4 | Combat |
| 5 | Quiet/Texture |
| 6 | Social |
| 7 | Environmental |
| 8-10 | Discovery |
| 11-12 | Faction/Political |

#### Quiet/Texture

| d6 | Result |
|----|--------|
| 1 | Chalk dust hangs in the air; the road here is white as bone |
| 2 | A funeral pyre's cold ashes, official, recent — someone important died here |
| 3 | A milestone marker, freshly re-carved with an unfamiliar sigil |
| 4 | A distant marching cadence, gone before you can place its direction |
| 5 | Broken ground where the chalk gives way to old excavation |
| 6 | A raven perched on a boundary stone, unnervingly still, watching |

#### Social

| d6 | Result |
|----|--------|
| 1 | Ironhold traders, gruff, incurious, moving fast |
| 2 | A Compact quartermaster looking to offload surplus, cheap |
| 3 | A necropolis laborer, off-shift, willing to talk for coin |
| 4 | A pilgrim family, lost, asking directions to a shrine that isn't Choir-aligned |
| 5 | A retired Concordat clerk, bitter, with real gossip |
| 6 | A war-orphan runner carrying messages between camps |

#### Environmental

| d6 | Result |
|----|--------|
| 1 | Chalk downs — exposed, no cover for miles |
| 2 | A sudden dust storm off the exposed ground |
| 3 | A sinkhole where old tunnels collapsed beneath the chalk |
| 4 | Unseasonable heat radiating off the pale stone |
| 5 | A dry riverbed, cracked, water rights disputed nearby |
| 6 | Distant thunder with no rain — a mundane quarry blast, far off |

#### Combat

| d6 | Result |
|----|--------|
| 1 | Compact column, Ironhold traffic — 3x Scout + 1x Veteran (SRD, unmodified; usually avoidable, professional) |
| 2 | Chalk country beasts — 1x Manticore, or 1x Chimera (solo) |
| 3 | Mummies or wraiths wandered from the necropolis — roll d3: 1) 1x Mummy 2) 2x Wraith 3) 1x Mummy + 1x Wraith |
| 4 | Cinder Choir pilgrims, hostile if recognized — 4x Cult Fanatic |
| 5 | Ambush — someone knows they're coming. 4x Scout, a real tactical threat, not random banditry |
| 6 | A fragment-bearer's omen — no combat; the piece they carry reacts to something nearby |

#### Discovery

| d6 | Result |
|----|--------|
| 1 | A half-buried necropolis marker, pointing toward an older, unlisted site |
| 2 | An old excavation, abandoned mid-dig — something stopped the work here |
| 3 | A dead Concordat courier, papers naming a specific destination |
| 4 | Chalk-carved warnings leading toward a sealed tunnel entrance |
| 5 | A pilgrim trail worn deep by many feet, leading toward an unmarked shrine |
| 6 | Fresh tracks converging from multiple directions toward one unmarked point |

#### Faction/Political

| d6 | Result |
|----|--------|
| 1 | A real Concordat convoy, escorting cargo north — visible, routine here |
| 2 | Compact/Concordat tension made visible — a standoff, a bribe changing hands |
| 3 | Cinder Choir presence, more open than elsewhere — a shrine, a preacher |
| 4 | Ashvale Necropolis's own gate guard, visible from a distance |
| 5 | A faction messenger demanding the party identify themselves |
| 6 | Evidence the Concordat is actively searching for someone — unconfirmed if it's the party |

### Late tier (level 10, or engaging the necropolis itself)

Quiet/Texture, Social, Environmental, Discovery, and Faction/Political are unchanged from Early. Only **Combat** escalates:

#### Combat

| d6 | Result |
|----|--------|
| 1 | Compact column, hardened — 5x Veteran (SRD, unmodified) |
| 2 | Chalk beasts, worse — 2x Manticore, or 1x Chimera + 2x Manticore |
| 3 | Necropolis undead, escalated — roll d3: 1) 2x Mummy 2) 1x Mummy + 2x Wraith 3) 3x Wraith |
| 4 | Cinder Choir, organized — 6x Cult Fanatic |
| 5 | Ambush, better-equipped — 6x Scout + 1x Veteran |
| 6 | The fragment-bearer's omen intensifies — still no combat, but the sign is unmistakable this time |

## The Sundered Reach — levels 13-17

**Layered format, added session 9, 2026-08-30** — see the Thornlands section above for how this works. Distinct from every other region: the Sundered Reach is **frozen wilderness over a dead empire** — no living population beyond scattered exiles and the isolated, cold-blooded creatures that call it home, mythic-tier apex predators (a dragon, giants, a hag), and killing weather as a real mechanical threat, not flavor. No faction has any real reach here.

**Tier**: use **Early** below level 16, **Late** at level 16-17 (top of range) or once the party is closing on the campaign's actual endgame content here.

### Early tier

#### Category

**Weighted d12, set 2026-08-30 (DM-specified: 4/12 Combat, 1/12 Quiet/Texture, 1/12 Social, 1/12 Environmental, 3/12 Discovery, 2/12 Faction/Political)** — replaces the original even d8 split after live dev-mode testing showed combat coming up too rarely.

| d12 | Category |
|-----|----------|
| 1-4 | Combat |
| 5 | Quiet/Texture |
| 6 | Social |
| 7 | Environmental |
| 8-10 | Discovery |
| 11-12 | Faction/Political |

#### Quiet/Texture

| d6 | Result |
|----|--------|
| 1 | Wind-carved ice sculptures, eerie and beautiful, untouched by any hand |
| 2 | The bones of something vast, frozen into a glacier wall |
| 3 | An ancient buried road, dragon-script still visible where wind bares it |
| 4 | Silence so complete you can hear your own heartbeat |
| 5 | Aurora light flickers even in daylight — the sky itself feels wrong here |
| 6 | A frozen waterfall, perfectly still, centuries old |

#### Social

| d6 | Result |
|----|--------|
| 1 | A hardy trapper or exile, the only living thing for miles, wary |
| 2 | A hag's isolated hut, smoke rising — not hostile unless provoked |
| 3 | Frost giant traders, rare, transactional, uninterested in politics |
| 4 | A lost expedition's last survivor, half-mad, with a warning |
| 5 | An ash-king era ghost, harmless, replaying a memory on a loop |
| 6 | A creature bound by an old oath, willing to talk if approached correctly |

#### Environmental

| d6 | Result |
|----|--------|
| 1 | Killing weather — real shelter needed, real consequences for going without |
| 2 | A whiteout blizzard — navigation becomes genuinely dangerous |
| 3 | Thin ice over a hidden crevasse |
| 4 | Bone-deep cold that no ordinary gear fully defeats |
| 5 | Avalanche risk on a narrow pass |
| 6 | The ground itself is wrong — old magic bleeding through, minor but unnerving |

#### Combat

| d6 | Result |
|----|--------|
| 1 | Yetis — 2x Yeti (SRD, unmodified) |
| 2 | Winter wolves — 4x Winter Wolf |
| 3 | A remorhaz under the ice — solo, real danger |
| 4 | An apex hunter — 1x Roc, 1x Chimera, or 1x Manticore (solo) |
| 5 | Giant sign — a Kar Vaelth patrol, 2x Fire Giant |
| 6 | The dead of the old kingdoms — roll d3: 1) 2x Wraith 2) 1x Mummy 3) 1x Mummy + 1x Wraith |

#### Discovery

| d6 | Result |
|----|--------|
| 1 | An ash-king era ruin, partially buried — its deeper half still intact below the ice |
| 2 | A frozen expedition's last camp — a map among the gear, pointing further in |
| 3 | Dragon-script carved into an exposed stone face, leading toward what it warns of |
| 4 | An old battlefield, preserved by the cold — a banner still marks whose it was |
| 5 | A hidden entrance, half-sealed by ice, into something older than the Reach itself |
| 6 | Tracks in the snow, too large and too fresh to be harmless — leading onward |

#### Faction/Political

| d6 | Result |
|----|--------|
| 1 | No faction has real reach here — any presence at all is a genuine anomaly, worth noting specifically |
| 2 | A lone Concordat or Compact scout, hopelessly out of their depth |
| 3 | Evidence of a previous expedition's fate — a warning left behind |
| 4 | Kar Vaelth's giants patrol territory they consider theirs |
| 5 | Something wearing an old ash-king banner, no longer aligned with anyone living |
| 6 | A desperate, unanswered message left for whoever reads it next |

### Late tier (level 16-17, or the endgame content here)

Quiet/Texture, Social, Environmental, Discovery, and Faction/Political are unchanged from Early. Only **Combat** escalates:

#### Combat

| d6 | Result |
|----|--------|
| 1 | Yetis, more — 4x Yeti (SRD, unmodified) |
| 2 | Winter wolves, pack grown — 6x Winter Wolf |
| 3 | A remorhaz, actively hunting — no longer just "under the ice" |
| 4 | Two apex predators together — 1x Roc + 1x Chimera |
| 5 | Giant sign, worse — 4x Fire Giant, a real patrol in force |
| 6 | Dragon sign — the Frostmere Adult White Dragon itself, hunting far from home (solo) |

---

## Roll log

| When | Route | Rolls | Outcome |
|------|-------|-------|---------|
| Session 2 | Gallowmere → Thornwick (5 nights) | 3, 9, 2, 6, 4 | N1 quiet · **N2 goblin band — played out, both goblins killed, Ilvaneth dropped to 3/8 then long-rested** · N3 quiet · N4 travelers (passed at distance) · N5 quiet |
| Session 2 | Sorrel's Hollow → Thornwick (1 night) | 2 | Quiet passage |
| Session 2 | Thornwick → Gallowmere (5 nights) | 1, 10, 6, 9, 1 | N1 quiet · N2 Concordat party + undead honor guard — hidden successfully, no contact · N3 refugees passed at distance · N4 2 Skeletons — fought and killed, 100 XP · N5 quiet |
| Session 2 | Gallowmere → Thornwick/Harrowgate (5 nights) | 8, 10, 10, 3, 2 | N1 beasts (owlbear) — resolved, owlbear killed at its lair, 70 gp · N2 Concordat party + undead honor guard — ambushed and wiped out (12 killed, second fragment recovered), day 19-20 · N3 (same-again roll) superseded — party left the main road before this night · N4-N5 not played, route changed |
| Session 3 | Off-road, Thornlands → Harrowgate (back trail, bypassing Thornwick, 1 night) | 5 | Merchant convoy — trade, news, or a job offer |
| Session 3 | Harrowgate → Cindermoor (Hollowmoor Barrows / Harpy Crags, 3 nights) | 1, 3, 9 | N1 quiet · N2 weather — fog/storm forcing shelter in a barrow · N3 hell hound — rare, dangerous, killed |
| Session 3 | Final leg to the Harpy Crags (1 night) | 4 | Weather — unnatural fog, played as a navigation hazard (no shelter needed this time) |
| Session 3 | Harpy Crags → Hollowmoor Barrows (1 night) | 10 | Sefwyn Marrow makes contact — the campaign-clock thread fires |
| Session 4 | Hollowmoor Barrows → Harrowgate (back road, avoiding the main Thornlands route, 3 nights) | 2, 4, 4 | N1 quiet · N2 weather (fog) · N3 weather (storm, shelter taken) |
| Session 4 | Harrowgate → the Weeping Tower (back road toward Gallowmere, marsh country, 3 nights) | 4, 5, 3 | N1 merchant convoy — passed at a distance, no contact · N2 merchant convoy — same · N3 quiet |
| Session 4 | Weeping Tower → hidden camp spot near Gallowmere (riverside waterfall trail, 1 night) | 10 | Faction patrol — Concordat scouts, being resolved in play |
| Session 5 | Gallowmere → Thornwick (4 nights) | 1, 9, 8, 3 | N1 quiet · N2 goblin band · N3 deserters/bandits demanding a toll · N4 quiet |
| Session 7 | Millward Crossing → Harrowgate (5 nights) | 3, 2, 5, 10, 3 | N1 quiet · N2 quiet · N3 merchant convoy — rumor #1 (the drowned mill) traded, no purchase · N4 Concordat search patrol (2 Wight + 2 Skeleton + investigator-priest, escalated per party level) — observed from hiding (Stealth 21/16), avoided via a side trail, no contact · N5 quiet |
| Session 7 | Harrowgate → Ostwick (2 nights) | 4, 8 | N1 merchant convoy — **resolved**, rumor #12 traded (false lead about a Gallowmere fragment), no purchase, day 48-49 · N2 beasts (wereboar sign near Ostwick) — pending, picked up at Session 8's start (state.md's day/location had drifted after N1 and were corrected first, see `bug-log.md`) |
| Session 8 | Ostwick → Harrowgate (return leg, day 50) | 5 | Merchant convoy — trade, news, or a job offer — being resolved in play |
| Session 9 | Harrowgate → Shestendeliath Hold (off-road, day 51, 1-day ride) | 9 | Undead — a lone specter rises from an unmarked wayside grave. **Resolved**: killed round 1 (Scorching Ray 24 dmg, then Kriv's Barrow-King's Blade 36 dmg incl. vs-undead bonus). 100 XP each. See `encounters/thornlands-wayside-specter.md` |
| Session 10 | Greyholt → Harrowgate (day 52, ~1 day, Late tier — Pattern-of-Losses fired) | Category 10 → Discovery, Subtable 4 | A dead courier's undelivered message, naming a specific location — being resolved in play |
| Session 10 | Harrowgate → Kesh Deeps (Cindermoor, days 53-56, 4 nights, Early tier — party below the region's level 7 Late-tier trigger) | N1: Cat 8→Discovery, Sub 2 · N2: Cat 2→Combat, Sub 1 · N3: Cat 4→Combat, Sub 6 · N4: Cat 12→Faction/Political, Sub 1 | N1: a relic-hunter's abandoned camp, a map left behind pointing further out · N2: 3x Harpy (unmodified SRD) · N3: Sefwyn Marrow or a rival relic-hunter, same find, may resolve as Social · N4: a lone Concordat scholar cataloguing a barrow, out of place — being resolved in play |
| Session 12 | Kesh Deeps → Harrowgate (Cindermoor, day 56, Night 1) | N1: Cat 2→Combat, Sub 5 (Moor wolves) | **Cancelled by the DM before resolution** — the party redirected toward The Maker's Undoing instead of Harrowgate; Night 1 never happened in the final timeline. Roll voided, not carried forward. |
| Session 12 | Kesh Deeps → The Maker's Undoing (Cindermoor, day 56 onward, ~2 days, Early tier) | N1: Cat 11→Faction/Political, Sub 1 · N2: Cat 6→Social, Sub 3 | N1: a lone Concordat scholar (Perrine Oskold), killed · N2: a rival relic-hunter working the same ground, wary of competition — being resolved in play |
| Session 14 | The Maker's Undoing → Harrowgate (Cindermoor, day 57 onward, 3 nights, Late tier — level 6, Pattern-of-Losses fired) | N1: Cat 2→Combat, Sub 4 (two will-o'-wisps) · N2: Cat 4→Combat, Sub 6 (rival relic-hunter crew turns hostile) · N3: Cat 2→Combat, Sub 6 (same result — reinterpreted as a *different*, unconnected crew, since N2's Orna Threk and both her Scouts ended up dead — see `campaign-clock.md`'s day 60 entry) | N1: Wisp A killed, Wisp B fled (14/22 HP) · N2: Orna Threk (named this session — the unnamed half-orc rival relic-hunter from The Maker's Undoing) + 2 Scouts, all killed · N3: a 3-Thug scavenger crew, all killed (one surrendered, executed anyway). Arrived Harrowgate day 60 |
| Session 14 | **Party split, day 60**: Ilvaneth solo → Ostwick (Thornlands, 2 nights, Late tier) | N1: Cat 4→Combat, Sub 3 (Undead escalated, d4→1: 2× Wight) · N2: Cat 9→Discovery (early tier), Sub 5 (an old shrine, half-swallowed by roots) | N1: **flagged to the DM as a likely-fatal fight for a solo level-6 PC against 2-PC-calibrated Deadly math** — given the choice to hide, Ilvaneth's Stealth 20 vs passive Perception 13 avoided the encounter entirely, no fight. N2: not yet resolved, journey paused to cut to Kriv's thread |
| Session 14 | **Party split, day 60**: Kriv + Ostrig Kelmar's crew → Shestendeliath Hold (Thornlands, 1 night/day's ride, Late tier) | N1: Cat 11→Faction/Political (early tier), Sub 3 (evidence of recent faction activity — burned banners, a skirmish site) | Resolved — real Concordat/Compact skirmish evidence found, see `campaign-clock.md` day 61 |
| Session 14 | Kriv solo → Harrowgate (day 61, Shestendeliath Hold → Harrowgate, Thornlands, 1 night, Late tier), to collect Roskel | N1: Cat 11→Faction/Political (early tier), Sub 2 (a Concordat inspection party, observed at a distance — avoidable) | Resolved — close call, Stealth 10 vs Perception 11, patrol noticed something but didn't pursue |
| Session 14 | Kriv + Roskel → Shestendeliath Hold (day 62, Harrowgate → Hold, Thornlands, 1 night, Late tier) | N1: Cat 12→Faction/Political (early tier), Sub 2 (same result — another Concordat inspection party, avoidable) | Resolved cleanly — with Roskel along, avoided without incident |
| Session 14 | Ilvaneth + Maren + Dunnel Ashe → Shestendeliath Hold (day 63 onward, Ostwick → Hold, Thornlands, 2 nights, Late tier) | N1: Cat 9→Discovery (early tier), Sub 1 (a weathered signpost pointing toward a place not on any map) · N2: Cat 7→Environmental (early tier), Sub 4 (a swollen creek crossing) | Being resolved in play |
| Session 16 | The Unquiet Barrow → Shestendeliath Hold (day 67 onward, Thornlands, 1 night, Late tier) | N1: Cat 5→Quiet/Texture (early tier), Sub 3 (a cold, day-old campfire — someone else's road, not yours) | Uneventful — a stranger's abandoned camp, no contact. Arrived Hold day 68 |
| Session 16 | Shestendeliath Hold → Harrowgate (day 68, 1-day ride, Thornlands, Late tier) | Cat 5→Quiet/Texture (early tier), Sub 1 (fair weather; a distant village bell marks the hour) | Uneventful. Arrived Harrowgate evening day 68 |
| Session 16 | Harrowgate → Thornwick via the Weeping Wood (day 69, Thornlands, Late tier) | Cat 10→Discovery (early tier), Sub 6 (fresh grave-digging, recent, leading back toward wherever the digger came from) | Being resolved in play |
| Session 17 | Thornwick → Gallowmere (5 nights, Thornlands, Late tier) | N1: Cat 6→Social (early), Sub 5 (circuit priest of the Ember Crown) · N2: Cat 11→Faction/Political (early), Sub 3 (evidence of recent faction activity — burned banners, a skirmish site) · N3: Cat 9→Discovery (early), Sub 3 (distant ruins glimpsed through the canopy) · N4: Cat 4→**Combat (late tier)**, Sub 5 (Concordat party, hardened per the Pattern-of-Losses consequence — larger escort, a named investigator-tier priest, decoys possible) · N5: Cat 6→Social (early), Sub 3 (refugees heading south, news of the north) | N1-N3 resolved (priest's road news — the Choir's manufacture cover story; a skirmish site glimpsed, not investigated; a pre-dynastic watchtower ruin investigated, 34 gp + a partial ash-king-era inscription found). **N4 resolved as a full combat** — the hardened convoy was Ysolde Marrenth (Sarelle's own investigator) personally escorting it; entire convoy destroyed, see `session-17-combat-hardened-convoy.md`. N5 resolved (circuit priest, road news). |
| Session 17 | Gallowmere → Shestendeliath Hold (5 nights, Thornlands, Late tier) — traveling as a full caravan: 27 turned/loyal soldiers, Alis Wend's group of 6 civilians, both PCs | N1: Cat 6→Social (early), Sub 1 (merchant convoy — trade, news, job offer) · N2: Cat 2→**Combat (late tier)**, Sub 1 (a hardened toll gang — 4 Bandits + 1 Veteran, SRD unmodified) · N3: Cat 7→Environmental (early), Sub 1 (fog rolls in) · N4: Cat 6→Social (early), Sub 3 (refugees heading south) · N5: Cat 11→Faction/Political (early), Sub 3 (evidence of recent faction activity) | Being resolved in play — N2's combat trivial given the caravan's own 27-soldier escort, narrate accordingly |
| Session 18 | Thornwick → The Drowned Cathedral, Cindermoor (4 nights, Cindermoor Late tier, party level 7) | N1: Cat 3→**Combat (late tier)**, Sub 4 (2 Will-o'-Wisp, working together) · N2: Cat 8→Discovery (early), Sub 6 (Cair Dunnow markers warning outsiders away from a specific, nearby site) · N3: Cat 4→**Combat (late tier)**, Sub 5 (6x Wolf, bolder) · N4: Cat 1→**Combat (late tier)**, Sub 5 (6x Wolf, bolder) | Being resolved in play |
| Session 19 | The Drowned Cathedral → Cair Dunnow, Cindermoor (2 nights, Cindermoor Late tier, party level 7) | N1: Cat 5→Quiet/Texture (early), Sub 1 (spongy ground, boot-prints fill with dark water) · N2: Cat 10→Discovery (early), Sub 2 (a relic-hunter's abandoned camp — a map left behind, pointing further out) | Resolved — map found and read (Investigation 24), pointed to the Moor-Ghost's own territory |
| Session 19 | Cair Dunnow → Karsgate, cutting cross-country toward Millward Crossing's road (6 nights, Cindermoor Late tier, party level 7) | N1: Cat 10→Discovery (early), Sub 5 (a trail of disturbed earth, a freshly opened barrow) · N2: Cat 3→**Combat (late tier)**, Sub 1 (5x Harpy, unmodified SRD) · N3: Cat 9→Discovery (early), Sub 3 (a standing-stone ring, one leaning stone marking a direction) · N4: Cat 2→**Combat (late tier)**, Sub 6 (a rival relic-hunter crew — new, not Orna Threk's — turns hostile) · N5: Cat 6→Social (early), Sub 3 (a relic-hunter working the same ground, wary of competition) · N6: Cat 1→**Combat (late tier)**, Sub 3 (2x Hell Hound) | Being resolved in play |
