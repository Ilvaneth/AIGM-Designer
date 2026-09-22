# Session 10 — Conversation Log

**Campaign**: Ashen Crown
**Date**: 2026-09-01
**Starting Location**: Shestendeliath Hold, great hall, eastern Thornlands — day 51, dusk, post-combat

---

## Scene 0 — A state-drift correction

Session opened mid-confusion: a second, parallel tab had continued running "Session 9" against the same campaign files while this tab started fresh as "Session 10," producing a real two-writer conflict (stale headers, a location file presenting an already-resolved dungeon as unexplored). Resolved by direct DM confirmation — this tab is the authoritative Session 10, the other tab's actual play content (the wraith fight, oath-hall, vault, cistern) is canon. Built `session_lock.py` and wired it into session start/end so this can't recur silently. See `bug-log.md`'s `state-drift` entries for the full diagnosis.

## Scene 1 — The garrison takes command

Kriv addressed Kethrax and the garrison formally: *"Kethrax, askerler rahat. Artık Lordunuz döndü, emirleri benden alacaksınız."* Kethrax's reply, quieter than his usual formality: *"Sizinleyiz, lordum. Her zaman sizinleydik — sadece kiminle olduğumuzu bilmiyorduk."* The garrison began clearing debris. Kriv and Ilvaneth departed for Harrowgate, promising to return with people who could actually rebuild.

## Scene 2 — Greyholt

A short ride away, the party found **Greyholt** for the first time — a hamlet under a hundred people, wary of the Hold by long habit. Kriv chose only to observe from a distance (too early to approach) after a brief look at the settlement's larger stone house, once a steward's residence.

## Scene 3 — The dead courier

On the road toward Harrowgate, a strong Investigation check (25) found a dead Concordat courier's abandoned effects: a guild token, an undelivered letter warning of unusual duergar activity threatening Kesh Deeps' iron shipments, and (on the body itself) a cut pack-strap — proof he was deliberately followed, not just a victim of exposure.

## Scene 4 — Marsh, one last time

Before disposing of Marsh's body (carried in the Bag of Holding since Ostwick), the party searched it once more: a hidden brass key and a note — *"Oda 4, arka kapı — Wren'e söyleme"* — pointing to an unexamined room at Ostwick's Hollow Sheaf. Ilvaneth read Marsh's business ledger properly for the first time: a real pattern of exploiting war-fleeing families across multiple towns, with two more named but "unprocessed."

## Scene 5 — Harrowgate: the liquidation

At Borgha Kresk's forge and Corvin Thale's shop, the party sold off a full round of spare gear — mundane Chain Mail, a Greataxe, a citrine gem to Borgha (88 gp); a Mithral Chain Mail and a Periapt of Wound Closure to Corvin (455 gp, after an initial pricing correction that had the strong Persuasion roll pushing the price *down* instead of up). The Shestendeliath house treasury itself was melted down rather than sold intact — Kriv personally oversaw the assessment (Smith's Tools 15) and pulled aside gem insets and a small silver hairpin before the melt — 500 gp for the raw metal, deliberately chosen to strip the identifying house sigil. Total: just over 1,000 gp, split.

Delivered the dead courier's warning to Borgha, who now gives the party her real price with no haggling in thanks. Sent a sealed courier recalling **Roskel** from Gallowmere to Harrowgate — *"Gallowmere'daki operasyon askıya alındı sana burada ihtiyacım var... artık çilen bitti."*

## Scene 6 — The road to Kesh Deeps: the harpy fight

Night 2 of the four-night journey: three harpies in a rocky pass. Ilvaneth's Scorching Ray opened the fight; Kriv, unseen, dropped Harpy A with a surprise Goading Attack — then failed his own Wisdom save against its Luring Song and spent a round charmed, breaking free at the very end of his turn. Fireball (Ilvaneth) caught A and B together after B closed distance; Magic Missile finished the survivors. All three killed. Feathers harvested for Cole at Vestry & Cole.

## Scene 7 — Kessra Vane

Night 3: a fire genasi relic-hunter, **Kessra Vane**, approached the camp openly, hands visible. She'd independently chased the same abandoned-camp trail the party found on Night 1 (marked "K.V.") and recognized them on sight against a description she'd held since day 28. Her first line asserting the description was already tied to missing Concordat convoys was a real continuity error, corrected live (see `bug-log.md`) — the honest version has her connecting the dots for the first time, right there. Struck a fencing/business partnership: Karsgate grey-market access for a cut of future finds. Gave a contact token. Asked about a rumor of an ash-era fragment sold in Karsgate — unknowingly asking about the party's own session-5 forged misdirection. Ilvaneth denied all knowledge and the lie held (Deception 22 vs. Insight 11).

## Scene 8 — Nessa Wren

Night 4, the final night: a lone Concordat archivist, **Nessa Wren**, found cataloguing ash-king symbols at a barrow under Sarelle Duskbourne's own written authorization. Kriv put a blade to her throat from hiding. Under threat, she gave up her purpose (a region-wide symbol survey, unconnected to hunting the party specifically) and everything she knew about duergar (Sunlight Sensitivity, Duergar Resilience). Ilvaneth's Arcana (20) confirmed her notebook's symbols matched sites the party had already seen — and that Sarelle's search is systemic, not party-specific. Ilvaneth ordered the kill: *"Bitir işini Kriv. Alacağımızı aldık."* Nessa's body was preserved with Gentle Repose and kept — a future Animate Dead target.

A World Events roll (d12=3, "Sarelle vs. Tain advances") fired the same night: off-screen, Orell Tain found a second Ash-Warden house sharing Shestendeliath's exact attainder irregularity — Kriv's "deliberate pattern" theory just became evidence-backed.

## Scene 9 — Kesh Deeps: entry and the outpost

Arrived at Kesh Deeps at dawn (a full cinematic first-arrival). Scouted the area: Ilvaneth found a hidden ventilation shaft and spotted the entrance guard before it saw them (Sunlight Sensitivity working against it). A stealth kill on the guard took two hits to finish; Ilvaneth then raised the corpse as an **animated duergar zombie** via Animate Dead (Pearl of Power refunding the slot). 

Following the vent shaft to Room 5, Ilvaneth's own approach was noticed (a tie against passive Perception counts as detected). Kriv's surprise attack opened the fight against the Duergar Outpost — four duergar, three still surprised. All four fell across four rounds without a single failed save going the party's way; the last, fleeing at 8 HP, was run down. 400 XP each. A search found 36 gp and a hand-drawn tunnel map showing the rooms ahead, including Room 9's guard rotation.

## Scene 10 — The Living Quarters and the dig face

Room 6 held the duergar's own mining-lore records — read via a ritual Comprehend Languages: generations of belief in a "stone that speaks," a pre-dynastic structure beneath the mine, and a note that the Chief himself would be present when they broke through. Room 7 (Ore Processing) and Room 8 (the Deep Shaft, crossed carefully after a DEX check) were passed without incident.

At Room 9, Kriv deliberately drew attention while Ilvaneth readied Fireball from hiding. The Chief (a sergeant-tier duergar, 52 HP) and a second guard were caught together by the release — both failed their saves, one died outright. Kriv finished the wounded Chief the following round. 300 XP each.

## Scene 11 — The breakthrough

Ilvaneth searched the fallen (39 gp, the Chief's rank medallion) while Kriv spent several hours breaking through the dig face's stone by hand — the zombie posted at the passage door, Ilvaneth taking a short rest nearby. The wall gave way to a sealed, untouched ash-king era memorial chamber: a preserved signet ring inside a cinerary urn (Investigation 23), and a long wall inscription (read via a second Comprehend Languages ritual) naming **Kaelth Ashborn, Record-Keeper, Last of the Third Dynasty** — a fragment of real history, confirming the site's duergar mining-lore without resolving anything about the wider Ashen Crown plot.

## Scene 12 — Exit, and a design correction

Leaving via Room 4 (the Cave-In), a failed group Acrobatics check triggered a falling-debris hazard — both PCs took minor damage after successful DEX saves. A DM design question followed: why didn't Kesh Deeps' "Level range: 5-8" header mean the same fixed encounters stayed equally hard across all four levels? Confirmed as a real, campaign-wide gap (all 38 location files share it) and fixed the same session — `encounter_difficulty_check.py`, a new standing rule in `dungeon-design.md`, and a tracked cleanup item for the remaining files.

Exited via Room 3 to the surface, evening light over the Cindermoor. Kesh Deeps fully cleared.

---

**Session paused**: day 56, evening, outside Kesh Deeps.
