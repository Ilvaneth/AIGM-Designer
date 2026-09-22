# Planted Hooks — Chekhov's guns, tracked so they don't go stale

**What this is, and how it's different from `consequences.md` and `state.md`'s Open Threads**: `consequences.md` tracks faction/NPC *proactive agendas* (a numeric weight escalating toward a threshold). Open Threads tracks general unresolved plot facts. This file is neither — it's specifically for a **deliberately planted narrative detail** (an item, a line, an unexplained object) that was set up on purpose to matter later, with no weight or threshold of its own, just a payoff waiting to happen. A hook here **can** cross-reference or spawn a `consequences.md` entry once it actually starts moving (see each entry's Cross-ref line) — that's the two systems feeding each other, not duplicating.

**Format** — each entry:
```
### <Short name>
**Planted**: Day N, session N — where/how it was introduced
**Payoff hint**: what this was set up to matter for
**Status**: unresolved | resolved (day N, how) | superseded
**Cross-ref**: a consequences.md/state.md pointer, or "none yet"
```

`foreshadowing_check.py` flags any `unresolved` entry sitting 25+ days since planted — advisory, same discipline as `open_threads_check.py`: not everything flagged needs action, some hooks are meant to sit for a long arc.

---

### The unnamed signpost, Ostwick-Hold road
**Planted**: Day 63, session 14 — a weathered signpost at a fork in the road, naming a place not on any map the party carries. Dunnel Ashe (who grew up in this region) doesn't recognize the name either
**Payoff hint**: an unexplored, currently-unnamed site — genuinely blank slate, no faction/personal-arc string attached yet
**Status**: unresolved — deliberately noted rather than followed, party is en route to Shestendeliath Hold with the newly-recruited Ashe siblings
**Cross-ref**: none yet

### Orna Threk's territorial map
**Planted**: Day 58, session 14 — found on Orna Threk's body after the road ambush (Cindermoor, Night 2), Investigation 25
**Payoff hint**: a hand-drawn map marking several sites across the Cindermoor/Thornlands — The Maker's Undoing crossed out (already claimed).
**Status**: **Read, day 66, session 15.** Two other sites are marked, both unclaimed by any faction and unvisited by the party: **The Drowned Cathedral** (Cindermoor — a sunken pre-dynastic temple, marked with a small crude flame-glyph, Orna's own shorthand for "worth real coin") and **The Unquiet Barrow** (Thornlands — marked only with a question mark, no glyph; she'd clearly never actually gone in). No other sites marked — whatever else she was chasing, it wasn't written down here.
**Cross-ref**: `party/characters/ilvaneth-duskmere.md`'s Notable Items, `locations/the-drowned-cathedral.md`, `locations/the-unquiet-barrow.md`

### The toll deserters' signal horn
**Planted**: Day 15ish, session 2 — looted from the Sorrel's Hollow toll group, kept rather than sold
**Payoff hint**: nobody left alive recognizes its use, but it's a real horn with a real signal — a way to lure or mislead someone later, or a red herring if the party ever needs one
**Status**: unresolved
**Cross-ref**: none yet — also listed in `state.md`'s Open Threads

### The Vaelthorn crypt ward stone
**Planted**: Day 10, session 2 — found and deliberately left untouched during the crypt search
**Payoff hint**: whoever placed it has no idea the crypt was disturbed a second time; touching or triggering it later would announce the party to that person
**Status**: unresolved
**Cross-ref**: none yet — also listed in `state.md`'s Open Threads

### The signet ring in Corran's collateral room
**Planted**: Day ~34, session 5 — noted among Corran's pawned heirlooms, "possibly a destroyed noble house's seal"
**Payoff hint**: a live guess this is connected to Kriv's own house, or another house destroyed in the same wave of betrayals — deliberately unconfirmed
**Status**: ✅ RESOLVED, day 83, session 18 — it is **the Shestendeliath signet**, Kriv's own house. Bought from Corran for 40 gp (negotiated down from 60), now worn by Kriv — his first physical proof of identity, per `kriv-thread.md`'s treasure table.
**Cross-ref**: `jobs-and-opportunities.md`'s "The collateral room" entry (CLOSED), `kriv-thread.md`

### Harn's second note, the Weeping Tower
**Planted**: Day ~30, session 4 — a hidden note found after clearing the lower level's failed experiments
**Payoff hint**: Harn wondered if the anchor he needed for his life's work "was something that already existed, unknowingly carried by someone" — a deliberate, unconfirmed hint that the party's own Crown fragment is exactly that anchor. Never stated outright to the party.
**Status**: unresolved
**Cross-ref**: none yet

### The Hollow Prophet's illegible name
**Planted**: Day ~34, session 5 — a schism-era chronicler's marginal note found during Ember Crown archive research, name mostly illegible, "looks like V or Y"
**Payoff hint**: a real but incomplete lead on the Hollow Prophet's true identity/family — DM already knows the answer (Ilyra Thorne, `npcs/the-hollow-prophet.md`) but the party's own clue remains deliberately partial
**Status**: unresolved
**Cross-ref**: `factions/cinder-choir.md`'s Phase 5, `npcs/the-hollow-prophet.md`

### The Warden's Charge's inner band — "what sleeps in the blood"
**Planted**: Day 51, session 9 — the oath-hall at Shestendeliath Hold, an older/archaic inscription layer beneath the formal Warden's Charge text
**Payoff hint**: a deliberate first hint at `kriv-thread.md`'s "real ambition" — House Shestendeliath's dragon blood was the actual reason Ash-Warden houses were chosen for this duty. Kriv feels it resonate with his own ascension-track symptoms (running warm, fire drawing his eye) without understanding why. The full reveal is a DM call, not yet scheduled to a specific day/level — pull this thread deliberately, don't let it go stale by default
**Status**: unresolved
**Cross-ref**: `kriv-thread.md`'s "real ambition — the blood" section, `ascension-tracks.md`

### The forged Karsgate bill of sale
**Planted**: Day 33, session 5 — Ilvaneth forged evidence (an ash-era fragment sold in Karsgate) and gave it to Fennick Orle to spread as misdirection, deflecting the Concordat's search
**Payoff hint**: a live lie now circulating in the world — could be picked up and acted on by someone the party doesn't control (a real buyer showing interest, a Concordat agent chasing the false lead somewhere inconvenient)
**Status**: still live, first real payoff day 55 — the rumor reached Kessra Vane's grey-market circuit in Karsgate independently (she'd chased it herself, found nothing, and asked the party directly, unaware they were its source). Ilvaneth lied and held the lie (Deception 22 vs her Insight 11) — the misdirection is intact and now has a second unwitting carrier. Still nobody has connected it back to the party
**Cross-ref**: `campaign-clock.md`, `npcs/fennick-orle.md`, `npcs/kessra-vane.md`
