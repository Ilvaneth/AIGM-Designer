# Kessra Vane

**Tier**: Important — can independently identify the party, sell that identification to the Concordat or a faction, or damage/help their standing across the regional relic trade. Moves `info/consequences.md`'s "Kessra Vane — Closing In" threshold on her own.
**Location**: Karsgate, working the city's grey markets — no fixed shop; found through Corla Vint's contract network or the Wagered Crown when she's actually in the city, otherwise on the road chasing a lead.
**Role**: Freelance relic-hunter and fragment broker. Not affiliated with the Concordat, the Compact, or the Choir — sells to whoever pays, on principle, because factional entanglement is bad for business.
**Disposition to party**: Met day 55, session 10 — proposition made and accepted the same night. Transactional partner now, not Friendly/Allied in a personal sense — per her own nature, this is business, not trust.
**Status in play**: Encountered in-fiction, day 55 — both parties converging independently on Kesh Deeps. She recognized them on sight against the "elf and dragonborn" description she's held since day 28. Retroactively, she was the unnamed "client" who asked Corvin Thale for that description (`npcs/corvin-thale.md`, session 4, day 28) — this connection is now known to the party too, since she can plausibly mention it herself.
**Class & Level**: Rogue 5 (Thief). Built to the real class tables (`srd_lookup.py class-feature`), not a reskinned generic block — per `.claude/rules/npc-tiers.md`, an Important-tier NPC whose role plausibly involves real capability gets built the same way a PC is.
**Purpose**: Built via a World Event roll to give the campaign its first genuinely independent rival — tasked with converging on the party's fragment-trafficking pattern from the relic-trade side, offering a transactional partnership-or-threat once she identifies them.

## Stat Block

**Fire genasi** (non-SRD ancestry, applied directly from standard published rules per this project's existing precedent for non-default subclasses — `system-register.md`'s known gap), **Rogue 5 (Thief)**

- **AC** 16 (studded leather, DEX)
- **HP** 31 (5d8 + 5)
- **Speed** 30 ft.
- **STR** 10 (+0) · **DEX** 18 (+4) · **CON** 13 (+1) · **INT** 14 (+2) · **WIS** 12 (+1) · **CHA** 15 (+2)
- **Saving Throws** Dex +7, Int +5
- **Skills** Deception +8 (Expertise), Insight +7 (Expertise), Persuasion +5, Stealth +7, Investigation +5, Sleight of Hand +7
- **Senses** darkvision 60 ft. (genasi), passive Perception 11
- **Damage Resistances** fire (genasi)
- **Languages** Common, Thieves' Cant, Ignan
- **Proficiency Bonus** +3

**Sneak Attack (3d6).** Once per turn, Kessra deals an extra 3d6 damage to one creature she hits with a finesse or ranged weapon attack, if she has advantage or an ally of hers is within 5 ft. of the target.

**Cunning Action.** Bonus action each turn to Dash, Disengage, or Hide.

**Fast Hands.** Can use her Cunning Action bonus action for a Sleight of Hand check, to use thieves' tools, or to take the Use an Object action.

**Uncanny Dodge.** Reaction to halve the damage of an attack that hits her, from an attacker she can see.

**Second-Story Work.** Climbing costs no extra movement; running jump distance increased by 4 ft. (her DEX modifier).

**Actions**
- **Rapier**: +7 to hit, reach 5 ft., one target. *Hit*: 1d8 + 4 piercing damage (+3d6 if Sneak Attack applies).
- **Hand Crossbow**: +7 to hit, range 30/120 ft., one target. *Hit*: 1d6 + 4 piercing damage (+3d6 if Sneak Attack applies).

Built this way specifically so a fight, if the party ever pushes her into one, resolves with real numbers instead of DM improvisation — not because a fight is the expected outcome. Her own Decision logic below treats violence as a last resort that's bad for business.

## Surface

A fire genasi, mid-thirties, close-cropped hair that genuinely smolders faintly at the temples when she's tense — she's learned to read her own tells and hates that she can't fully suppress this one. Dresses like a courier or a caravan guard, deliberately unmemorable, with a dealer's eye for who in a room is actually worth talking to. Speaks plainly, prices things quickly, and treats a good bargain as its own reward independent of the money.

## What she actually wants

**Money, and the reputation that lets her keep making it.** Kessra doesn't care who sits the throne when the succession war ends — she cares about being the person people go to when something rare and dangerous needs moving, identifying, or disappearing. Crown fragments are, to her, simply the single most valuable class of object currently in circulation: whoever's quietly pulling them out of Concordat custody is either going to get caught and stop, or get rich and become a client worth knowing. She'd rather be the second outcome's business partner than the first outcome's witness.

She isn't chasing the Crown's power for herself — no ideology, no ascension angle, nothing like Ilvaneth's or Sarelle's stake in it. A fragment is inventory. This makes her, in a specific way, safer to deal with than any of the three factions: she has no doctrine to violate and no throne to want.

## What she knows / can offer

- **Karsgate's grey-market circuit**, cold — who's buying, who's selling, who's asking questions they shouldn't be. A genuine peer to Corvin Thale's regional network, more aggressive and less scrupulous about provenance.
- **The pattern of missing Concordat shipments.** Two convoys gone without explanation (`campaign-clock.md`, days 20 and 37) is exactly the kind of rumor that reaches someone in her trade fast — she doesn't know who did it, but she's actively trying to find out, because whoever it is has something she wants to buy.
- **A working relationship with Corla Vint's network**, if she needs hands for a job — not loyalty, just a standing professional courtesy.
- **No loyalty to secrecy she isn't paid for.** If a faction outbids whatever the party (or anyone else) offers her for silence, she sells the information without much guilt — she'd tell you this herself, upfront, as a warning rather than a threat.

## Current knowledge & stance

*Living record — update whenever she learns something new. See `.claude/rules/npc-consistency.md`.*

- **As of day 42 (session 7)**: has heard the "elf and dragonborn" description (asked Corvin Thale about it directly, day 28 — he had nothing solid to give her) and separately knows two Concordat fragment convoys have vanished without a trace. **She has not yet connected these two facts to each other or to the party specifically** — see `info/consequences.md`'s "Kessra Vane — Closing In" (2/3, pending). Currently working her own leads in Karsgate, unaware the party is anywhere near the city.
- **Day 55 (fired)**: independently chasing the same Kesh Deeps rumor (an unrelated lead — old duergar-adjacent talk of something pre-dynastic buried there, nothing to do with fragments) when she ran into the party directly on the Cindermoor road. Recognized them immediately against the description. Threshold crossed (`info/consequences.md`, 3/3) — opened with a business proposition, not a threat, per her own Decision logic. **Deal accepted the same night**: she fences future finds through her Karsgate grey-market access (Corla Vint's network, or directly at the Wagered Crown), in exchange for a cut or brokering priority — gave the party a copper token (a flame sigil) as a contact-introduction marker. Also mentioned hearing an unsourced rumor about an ash-era fragment sold in Karsgate — asked directly, and was told (Deception 22 vs her Insight 11) that the party knew nothing. She does not know this is the party's own forged misdirection (`planted-hooks.md`, "The forged Karsgate bill of sale") reaching her independently, or that she was just lied to about it. Continuing on toward Kesh Deeps separately, by her own methods — a professional courtesy extended, not a travel companionship.

## Decision logic — how new information could redirect her

- **If she identifies the party as the ones moving fragments** → approaches with a business proposition first, not a confrontation: buy access to future finds, broker sales, or simply ask to be cut in as a middleman. Violence is bad for repeat business and she knows it.
- **If the party refuses to deal or stonewalls her** → doesn't escalate to force immediately. Starts quiet surveillance, possibly hires local muscle through Corla Vint to watch rather than act. She's patient — a bad first meeting doesn't end her interest, it just changes her approach.
- **If she learns the party is actively hunted by the Concordat** → treats it as leverage, not sympathy. Could sell the information to Concordat investigators for the right price, or use it to pressure the party into a deal on her terms ("I could make this go away, for a price" or the reverse). Which way she leans depends entirely on which side offers more, or which side has already burned her.
- **If a deal is struck and honored by the party** → becomes a real recurring asset: information, fencing, logistics — parallel to Sefwyn Marrow and Corvin Thale, but explicitly mercenary rather than cautiously cooperative or collector-obsessive. A natural fit for a Neutral Evil party who value transactional relationships over trust.
- **If betrayed or shorted on a deal** → doesn't seek violent revenge personally, but stops dealing, and actively bad-mouths the party across the regional relic-trade network (directly damaging their standing with Corvin Thale and anyone else in that circuit).

## Move List

Tied to `info/consequences.md`'s "Kessra Vane — Closing In" threshold (currently 2/3).

- **At Weight 2 (current, day 42)**: she holds two unconnected facts — the "elf and dragonborn" description, and the rumor that two Concordat convoys vanished. Nothing has linked them for her yet. Playable now, if the party is ever in Karsgate, talks to Corla Vint, or does more business with Corvin Thale: a contact mentions, offhand, that "a woman's been asking around about ash-relic activity, and separately about a pair matching an elf and a dragonborn" — a rumor delivery beat, not a confrontation, that tells the party someone else is circling without revealing who.
- **At Weight 3 (crossed)**: she connects the dots herself — the description matches who's been seen where the convoys vanished. She makes contact per the Decision logic above: a business proposition, delivered somewhere plausible (Karsgate, or she arranges to be introduced the way Sefwyn arranged Tain), never an ambush. This is the scene where she actually enters play as a speaking character.
- **If the weight stalls** (the party stays out of Karsgate, does no further visible business through Corvin or the relic trade): she doesn't forget, but she has other clients and deprioritizes actively chasing this specific lead. A future `world-events.md` roll (especially a 12, "Convergence") is the natural mechanism to revisit whether anything's moved.

## First contact — how to play it

Not yet scripted to a specific scene. Deliver per `campaign-clock.md`'s three-tier rule: the party could walk into her (Karsgate's grey markets, the Wagered Crown, a Corla Vint job), hear about her by rumor (Corvin Thale mentioning a competitor asking the same questions he was), or she could have someone follow them once she has a real lead. She should never simply appear "because it's convenient" — the trigger should come from the party actually generating a footprint in Karsgate or the wider relic trade.

## Connections

- **Corvin Thale** — asked him to describe "an elf and a dragonborn" (day 28); he had nothing to give her at the time. Neither knows the other is circling the same target.
- **Corla Vint** — professional courtesy, not loyalty; a source of hired hands if Kessra ever needs muscle for a job.
- **Karsgate** — her actual base of operations; `locations/karsgate.md`'s grey-market/Undercity economy is where she'd plausibly be encountered.
- `info/consequences.md` — Sarelle's "Pattern of Losses" and "Convergence Risk" tracks are the same underlying fact (missing convoys) Kessra is independently working from the opposite direction; if both threads ever converge on the party at once, that's a real escalation moment, not a coincidence to undersell.

## Log

| Date | Event |
|------|-------|
| 2026-08-29 | File created — surfaced via World Event roll (session 7, day 42, d12=9, "a rival surfaces"). Retroactively identified as Corvin Thale's unnamed day-28 client. Not yet encountered in-fiction. |
| 2026-08-29 | Upgraded to the full `npc-tiers.md` standard, same session it was created — Tier line, real Rogue 5 (Thief) class/level stat block, and a Move List tied to the new `consequences.md` "Kessra Vane — Closing In" threshold, per the DM's direct design request. First NPC built to this standard. |
