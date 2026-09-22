# Consequences — the cumulative reaction ledger

**What this file is for**: `campaign-clock.md` tracks scheduled/time-based clocks (when does X happen if nothing intervenes). NPC files track individual, in-scene character consistency (`.claude/rules/npc-consistency.md`). Neither one accumulates *cumulative* damage/benefit the party has done to a faction or NPC over time and escalates a reaction once a threshold is crossed. This file is that missing layer. Full design discussion and the reasoning behind every format choice below: `world-reactivity-design.md`.

**The litmus test** (the DM's own words, from that discussion): any consequence here must produce a real, integrated change — new prices, new NPC attitudes, a closed road, a changed map, a spawned side-thread — never just a logged note that gets read once and forgotten.

---

## Format (read before adding an entry)

```markdown
### <Entity Name> — <short label for this specific threshold>
**Threshold**: <N> → <what happens at N> (see `<path>`, Decision logic)
**Status**: pending | crossed-unapplied | applied (day <D>)

| Date | Event | Weight |
|------|-------|--------|
| Day <D> | <what happened, one line> | <integer> |
```

- **Weight is always a plain integer.** The unit/meaning belongs in the `**Threshold**` line's label only, so the column stays trivially summable.
- **`consequence_check.py` sums the Weight column itself, every time** — it never trusts a separately hand-written cumulative total. Same reasoning as `state.md`'s party block being generated from character files: a second hand-maintained number is a second thing that can drift.
- **The threshold's number lives only here**, not duplicated into the entity's own NPC/faction file — that file keeps the *qualitative* reaction (already written, e.g. Sarelle's "pattern recognition, operational hardening") and this file's Threshold line just points back to it by name.
- One entity can have more than one threshold block (see Sarelle below) — each is independent, its own `###` heading, its own table.
- `applied (day D)` entries are done — `consequence_check.py` stops flagging them. Never auto-apply silently (same rule as `rest_check.py --apply`): a reaction gets applied by a deliberate assistant action with the change visible in play, or — as with the backfilled entry below — visible in the file the moment it's built.

---

### Sarelle Duskbourne — Pattern of Losses
**Threshold**: 2 → escalates to pattern recognition + operational hardening (see `npcs/sarelle-duskbourne.md`, Decision logic)
**Status**: applied (day 42)

| Date | Event | Weight |
|------|-------|--------|
| Day 20 | First convoy (9 skeletons, 3 priests) ambushed and wiped out entirely on the Gallowmere-Thornwick road; fragment #2 taken, no survivors, no alarm raised | 1 |
| Day 39 | Second convoy (6 skeletons, 2 priests) ambushed and wiped out near Millward Crossing; fragment #3 taken, forged Ironclad Compact evidence planted at the scene | 1 |

**Backfilled 2026-08-28** — both events already happened in the fiction before this system existed. Applying from zero would have silently erased history the way Sefwyn's "re-initiate contact" clock sat forgotten for 12 days before it was made a real clock (`bug-log.md`, 2026-08-27). Applied immediately on build, day 42: see `npcs/sarelle-duskbourne.md` and `campaign-clock.md`'s "Sarelle collects" entry for the actual in-effect changes (harder future shipments, a dedicated investigator now working both sites).

---

### Sarelle Duskbourne — Convergence Risk
**Threshold**: 3 → she personally connects "an elf and a dragonborn" (the description held since day ~5) to both ambush sites and treats the party as identified, not just a pattern (see `npcs/sarelle-duskbourne.md`, Decision logic)
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day ~5 | Concordat convoy reaches Gallowmere, collects physical descriptions of "an elf and a dragonborn" from Fennick | 1 |
| Day 20 | First ambush site (Gallowmere-Thornwick road) — geographically consistent with the descriptions' origin point | 1 |

Two of three. The forged Ironclad Compact evidence planted at the second ambush (day 39) is the live variable that decides the third weight either way — see Pending Resolutions below. **Do not add a mechanical third weight until that resolves.**

---

### Ashlord Concordat — Missing Archivists
**Threshold**: 3 → Sarelle formally opens an investigation into her own barrow-survey program on the Cindermoor road — a dedicated inquiry, not just a footnote, since two of her own field agents have now vanished on the same assignment within days of each other (see `npcs/sarelle-duskbourne.md`, Decision logic — new branch to add if this crosses 3)
**Status**: pending, 2/3 — one event away

| Date | Event | Weight |
|------|-------|--------|
| Day 56 | Nessa Wren, surveying under Sarelle's written authorization, goes silent — overdue to report | 1 |
| Day 56 | Perrine Oskold, the same assignment, also goes silent — and her own notebook shows she expected to compare findings with Wren, a rendezvous she never made. Whoever eventually reviews her absence finds this note and connects both disappearances at once, not separately | 1 |

**Why this is weighted higher than a simple headcount**: this isn't two independent 1-weight events that happen to add up — Perrine's own note is what actually LINKS them. The next weight (a third missing/compromised asset, or someone actually going looking for either woman) crosses the threshold outright. Distinct from "Sarelle Duskbourne — Convergence Risk" above (that one tracks identifying the party specifically via the elf/dragonborn description) — this tracks the Concordat noticing its own survey program has a hole in it, which could surface the party as a suspect by an entirely separate route if it ever gets that far.

---

## Pending Resolutions

Binary or open-ended outcomes that don't fit the threshold/weight shape above — tracked here so they're a checked fact the next time they're relevant, not re-decided from scratch.

### Does the forged Ironclad Compact evidence (day 39) hold up?
Ilvaneth planted forged evidence (Forgery 26) framing the Compact for the second convoy ambush.
- **RESOLVED, day 60, session 14 — it held.** Sarelle's suspicion shifted to the Compact; real Concordat-Compact friction has opened (see `faction-subplots.md`). Kriv found the aftermath of an actual clash en route to Shestendeliath Hold — burned Concordat banners, a Compact-style buckle, no bodies. The party lit this fire and doesn't know it yet.
**Status**: resolved — not currently discovered by the party as their own doing (they know a Concordat/Compact skirmish happened; they don't yet know their own forgery caused it).

---

### Sefwyn Marrow — Private Tally
**Threshold**: 3 → decides they have "enough" and moves to sell the accumulated knowledge to the highest bidder (Compact or Choir, whichever pays more) and disappear — per `npcs/sefwyn-marrow.md`'s own stated goal, "rich and unowned" (see that file's "What they actually want")
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 25 | Shown the first (ossuary) fragment in person, per the Hollowmoor Barrows meeting | 1 |

**Why this exists**: built 2026-08-29 after the DM asked directly whether NPCs pursue their own agenda independent of the party, not just react to it. Sefwyn's file already established a real, ongoing personal scheme ("their own private tally continues to grow independent of what the party knows about it") with no tracked progress — the same gap `consequences.md` was built to close for factions, just never extended to an individual NPC's arc. **The party's own choices directly control this clock's speed** — showing Sefwyn more (a second or third fragment, deeper Crown knowledge) accelerates it; keeping them at arm's length slows it. This is a deliberate lever, not just flavor: the more useful the party makes Sefwyn as a source, the sooner Sefwyn has enough to leave.

---

### Kessic Ambrey — The Unauthorized Search
**Threshold**: 3 → finds a real lead (possibly the fragment itself) in the Vault of the Nameless, or his search converges with High Prior Sennett's own suspicion and he's caught — see `npcs/kessic-ambrey.md` and `npcs/varic-sennett.md`
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | A decade of quiet, unauthorized searching, per his own file — the baseline before any session-driven progress | 1 |

### Sella Dray — Moving on Coalback
**Threshold**: 3 → she moves decisively against the Coalback gang (absorption or elimination), a real shift in the Warrens' territory — see `npcs/sella-dray.md`
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Existing friction and a standing grievance against Coalback's bad-for-business brutality, per her own file | 1 |

### Orell Tain — Losing the Internal Argument
**Threshold**: 3 → Sarelle finally succeeds in marginalizing or removing Tain from his position entirely, closing off the party's best inside line to the Concordat unless they act first — see `npcs/orell-tain.md`
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Already "losing this argument" per his own file, before any party action touched it | 1 |
| Day 42 | Given the torn Vaelthorn delivery order (proof Sarelle's excavation predates the Emperor's death) — real, usable political ammunition against her for the first time; functionally the "Ashvale proof" his own Decision logic names as the thing that would let him move against her openly | -1 |

**The uncomfortable lever**: Sarelle's own authority within the Concordat is tied to results. Every fragment convoy the party destroys is a real operational failure for her — but a cornered leader under pressure is at least as likely to tighten control and silence internal dissent as she is to lose credibility from it. **The party's own anti-Concordat campaign may be accelerating Tain's downfall, not helping him** — a real strategic tension, not a clean "the enemy of my enemy" story. Don't resolve which way it cuts until it's actually tested in play.

---

### Vesa Ilkraven — What She Does With What She Knows
**Threshold**: 3 → she acts on the leverage — approaches the party directly, sells the lead, or otherwise turns "Lady Serah Ashworth is fake" into something concrete — see `npcs/vesa-ilkraven.md`, Decision logic
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 47 | Caught, via a Deception check, that "Lady Serah Ashworth" is a false identity at Corran's private game — holds the fact but no motive to act on it yet | 1 |

### Marta Vantor — The Underbidding Campaign
**Threshold**: 3 → she successfully bankrupts her rival shipping concern and absorbs its trade, becoming even more dominant in Karsgate's river trade (and Region Control-relevant) — see `npcs/marta-vantor.md`
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Campaign already underway per her own file, funded by undisclosed reserves | 1 |

### Kessra Vane — Closing In
**Threshold**: 3 → she connects the "elf and dragonborn" description to the two missing Concordat convoys and identifies the party as the ones moving fragments — approaches with a business proposition (see `npcs/kessra-vane.md`, Decision logic and Move List)
**Status**: applied (day 55) — reaction delivered in the same scene, not a delayed off-screen beat

| Date | Event | Weight |
|------|-------|--------|
| Day 28 | Asked Corvin Thale directly to describe "an elf and a dragonborn" — got nothing solid at the time, but now has the description on file | 1 |
| Day 42 | Two Concordat convoy disappearances (days 20 and 39) have circulated far enough through the regional relic-trade grapevine to reach her independently of Corvin — she doesn't yet know they're connected to the same description she's holding | 1 |
| Day 55 | Direct visual confirmation — ran into the party in person on the Cindermoor road (both independently converging on Kesh Deeps) and immediately recognized them against the description she's held since day 28 | 1 |

**Threshold crossed, day 55.** She connects the description to the party directly, in person — a stronger trigger than the convoy-pattern route this threshold originally anticipated, but the same endpoint. See `npcs/kessra-vane.md`'s Decision logic: approaches with a business proposition, not a confrontation.

**Why this exists**: built 2026-08-29, same session Kessra was created (World Event roll, d12=9), per the DM's explicit design direction — an Important-tier NPC needs a proactive threshold like this one to actually move on her own, not just react if the party walks into her.

### Coren Ashvale — The Ashvale Grievance
**Threshold**: 3 → moves openly (recruits a deniable instrument, likely the party, to hit the Concordat at Ashvale Necropolis) — see `npcs/coren-ashvale.md`, Decision logic and Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Recently learned of the Concordat's occupation of his family's necropolis, per his own file — already "made this personal" before any party action touched it | 1 |
| Day 73 (World Event, d12=4) | Off-screen — an incident at Ashvale Necropolis (a cost overrun, an accident, a provocation the Concordat's own work caused) sharpens Coren's grievance further. Not yet delivered to the party in-fiction. | 1 |

### Mother Vey — Reading the Party
**Threshold**: 3 → decides definitively whether the party is an asset to Gallowmere's independence or a liability worth quietly selling — see `npcs/mother-vey.md`, Decision logic and Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 1 | Gave a cover story about the ossuary contents that she wasn't fully convinced by | 1 |
| Day 33 | Deflected her follow-up question about what they actually took from the ossuary — she noticed the deflection | 1 |

### Fennick Orle — The Debt Book Grows
**Threshold**: 3 → the debt book reaches critical mass — enough of Gallowmere owes him that he becomes a real, exercisable power lever rather than a barkeep with a hobby — see `npcs/fennick-orle.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Six years of quiet accumulation, per his own file — roughly forty households already on the ledger | 1 |

### Corran — Buying Up Thornwick
**Threshold**: 3 → owns enough of the village that Hesta Bram's fight to keep it independent becomes untenable — a real confrontation between them, not just mutual dislike — see `npcs/corran.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Ongoing land-buying campaign from panic-selling refugee families, per his own file | 1 |

### Orvenna Kest — Everyone's Ledger
**Threshold**: 3 → her private debt ledger becomes deep enough across all three factions that she's a genuine power broker, not just a neutral host — see `npcs/orvenna-kest.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Years of extending credit to every faction equally, per her own file | 1 |

### Corla Vint — The Broken Wheel's Reach
**Threshold**: 3 → her network's reach grows enough to rival Sella Dray's Red Tally as a real power in the Reeks — see `npcs/corla-vint.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Established, trusted broker position, per her own file | 1 |

### Odric Fenn — Preempting Venn
**Threshold**: 3 → Fenn moves first — acts against or around Prior Venn's known intent to expose his cell, before the party does anything about it — see `npcs/odric-fenn.md`, Move List
**Status**: **MOOT — Fenn killed by the party, day 74, session 17.** He never got the chance to act; the whole thread resolves by his death instead. Venn's own threat to the cell is now irrelevant — there's no cell left for him to expose, unless the party keeps it running under new management.

| Date | Event | Weight |
|------|-------|--------|
| Day 33 | Turned to the party's side; alliance formed | 1 |
| Day 33 | Learned (from the party) that Venn wants his cell exposed/removed — a live threat he now knows about and hasn't acted on yet | 1 |

### Aldric Venn — Losing Patience with the Choir Threat
**Threshold**: 3 → he acts on his own, despite having "no real power" — reports to a higher orthodox authority, or takes some desperate, self-endangering step — see `npcs/aldric-venn.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Genuinely frightened, per his own file, and has named the Ash-Kilns cell as a real regional threat with no means to act on it himself | 1 |

### Renata Kroll — The Standing Force
**Threshold**: 3 → she moves forward on funding a standing force regardless of Kriv's answer — finds another candidate, or the Compact formalizes control of the Garrison House first — see `npcs/renata-kroll.md`, Move List
**Status**: applied (day 51) — Kriv declined outright ("solve it your own way"); she proceeds to find another candidate rather than wait further. See `npcs/renata-kroll.md`'s Current knowledge & stance and `campaign-clock.md`.

| Date | Event | Weight |
|------|-------|--------|
| Day 28 | Offered to fund a force under Kriv's command; he asked for time to decide | 1 |
| Day 51 | Kriv deferred again — cited gathering resources/power first, no concrete commitment or timeline, 23 days after the original offer | 1 |
| Day 51 | Same conversation, moments later: told her outright to "solve it your own way," with a pointed warning that rushing would mean failure — a real decline, not a further deferral | 1 |

### Varic Sennett — Confirming the Karsgate Cell
**Threshold**: 3 → he acts on his suspicion, using the cathedral's own resources to move against Kessic Ambrey's cell directly — see `npcs/varic-sennett.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | A years-old pattern of unusual funerary requests and an unexplained missing acolyte, per his own file | 1 |

### The Broker (Ostren Vale) — The Office Under Scrutiny
**Threshold**: 3 → someone gets close enough to genuinely threaten exposing Ostren Vale as the Broker — see `npcs/the-broker.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Twenty years of deliberate, careful concealment, per his own file — a low baseline reflecting real skill, not inevitability | 1 |

### Sethra Shestendeliath — Hunting Vharkoss
**Threshold**: 3 → she independently locates or moves on Vharkoss once she has enough of a lead — see `npcs/sethra-shestendeliath.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Has suspected Vharkoss for years with no location, per her own file | 1 |

### Vharkoss Shestendeliath — The Fifteen-Year Fear
**Threshold**: 3 → his fear that a survivor or the missing fragment will surface finally forces him to act — hire protection, disappear again, or move preemptively — see `npcs/vharkoss-shestendeliath.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Fifteen years of quiet fear that the fragment was never truly lost, per his own file | 1 |

### Corvin Thale — The Collector's Temptation
**Threshold**: 3 → his personal fascination with a truly rare item overrides his usual caution, per Ilvaneth's own Insight read on him — a real exposure risk if the party ever over-trusts him — see `npcs/corvin-thale.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 37 | Personally bought the harvested basilisk eyes/fangs for his own collection — the collector, not the merchant, was visibly speaking | 1 |

### Sylvenna — Losing the Grove
**Threshold**: 3 → the Choked Grove falls entirely to the encroaching ettercaps/spiders — a real, permanent change to `locations/the-weeping-wood.md`'s content and danger level — see `npcs/sylvenna.md`, Move List
**Status**: halted, session 16 (day 69) — the party cleared the Choked Grove's overflow (2 Giant Spiders) and the adjacent Webbed Reach/Ettercap Nest, directly reducing the pressure this threshold tracks. Not closed permanently (ettercaps/spiders can plausibly re-encroach from elsewhere in the wood over time) — but the immediate losing-ground trend is reversed, not just paused.

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Already "losing ground for the first time in longer than she can easily reckon," per her own file | 1 |
| Day 69 | Party cleared Areas 3/4/9 (Webbed Reach, Ettercap Nest, Choked Grove) — Sylvenna's bargain fulfilled | -1 |

### Dallin Marsh — Under Kell's Suspicion
**Threshold**: 3 → Captain Kell notices Dallin's divided loyalty or traces the leak back to him — real risk to the party's own intelligence asset — see `npcs/dallin-marsh.md`, Move List
**Status**: **MOOT, day 75 — Kell fled the coup, there's no one left to trace the leak back to Dallin.**

| Date | Event | Weight |
|------|-------|--------|
| Day 33 | Began actively feeding garrison intelligence to Kriv — a standing, ongoing risk of discovery every time it happens again | 1 |
| Day 74 | Took 330 gp to personally recruit up to 20 of the garrison's 30 soldiers into Kriv's service — a mass defection, not quiet intelligence-leaking. Real coordination and timing risk; a same-night departure of 20 men is impossible for Kell to miss | 1 |

### The Hollow Prophet — The Manufacture Program
**Threshold**: 3 → either a real breakthrough (the manufacture program produces something that works) or a real institutional crisis (Yeva's doubt goes public, the bloodline secret leaks) — a Chapter-1-climax-tier beat — see `npcs/the-hollow-prophet.md`, Move List
**Status**: pending

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | The fourth kiln's caged failure is the program's only concrete result so far | 1 |
| Day 85 | Yeva Ashwright's second visit to the Ash-Kilns (`campaign-clock.md`) finds the cell wiped out — Fenn and his cultists dead, the fourth kiln broken open, no cover story left. She reports it up her own chain, reaching the Hollow Prophet in general terms — the wider Choir network now knows the Gallowmere cell is gone, cause unknown. Per her own Move List's Weight 2 trigger ("a cell leader reporting up, a rumor reaching Yeva's circuit") | 1 |

## Not yet built

Nothing currently flagged. Every faction and every Important-tier NPC identified as of 2026-08-29's full NPC-tier sweep now has at least one threshold block. Per `missing-systems.md`, don't invent a new one speculatively for anyone not yet built — build a block the first time an NPC's own file establishes a real, ongoing scheme with a completion point, following the format above exactly.
