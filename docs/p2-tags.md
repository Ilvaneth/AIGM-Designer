# P2 tags — the cosmos's review with the owner

*Opened 2026-10-08 by the design tab, on the survey `docs/reports/p2-survey.md`. P2 is reviewed the way P1 was (`docs/p1-tags.md`): the method first, then table by table with the owner; the rulings here hold over the plan's P2 lines where they differ.*

## S0 — the method (owner-approved 2026-10-08)

1. **Layers.** Story: the threat's god when the threat pins one, the move's dated event, the villain's origin event, the ruin's age. Stage: the planes P1 names (the thin place, the ruin's and the scars' planes) and the climate. Texture: the calendar, the festivals, the unpinned gods, most of magic. The one-way rule holds: texture never fills a story slot.
2. **Roll order.** The threat's pin and powers first (secret), then the planes P1 names, then the pantheon, the history's seated events, magic, and the calendar last.
3. **The writer writes and never decides.** The ten unrolled sub-tables become rolls: the planes (baseline seat, deviation, time rate, way in, cost), the gods' domains, ranks, church archetypes and relations, the god secrets as far as they survive (rule 6).
4. **The counts are rolled:** gods, great gods, the rank split, the touched planes.
5. **P2 keeps its own promises.** P2 joins the promise ledger's `SOURCE_PHASES`, and its rows get a frame at `phase P2 begin` that the door checks (as P1's since build 20a).
6. **P2 holds no secret of its own.** A secret at P2 is the threat's: the pinned god's secret, the true layer of the villain's origin event, a divergence only where the threat's secret uses it. Every other god secret and divergence becomes public or discoverable texture, or goes.
7. **The fifteen hooks inside P2's tables that are due at P1** (sealed before P2 rolls) become `requires` where they are a real dependency and are deleted otherwise.

Already ruled before this review (`docs/p1-tags.md` §§2-3) and not decided again: at least one touched plane at every scale; the planes the foundation names are shared to fit the count (one plane at short); great gods 0-1 / 1-2 / 2-4, raised by a religious contest role, by "gods among mortals" (at least one) and by the unnamed god's priests, their churches inside P4's total; the dial sets how strict the regulator is and P2's roll sets who (three rows override who); who gives the magic services is answered for every regulator row; the pantheon follows a gods-family ruin, whose god is fallen and faction-less; P2 writes the origin of every fantastic kind the ruin did not bring; the climate derives from the palette; the empty month and the lawless day fall inside the campaign's span; no real-world mythology names; months of 30 days.

## S1 — Pantheon I: type, presence, rank, the counts (owner-approved 2026-10-08)

**Type** (`pantheon.yaml#type`). Kept: polytheist (3), dualist (1), dead gods (1), silent gods (2), ancestor gods (1; also forced by its break). Changes:
- **One new row** (a religious system of the DMG's the table lacked): `pantheon_animist` (weight 1): "spirits in every river, hill and beast; the land itself answers"; the greater ones are great spirits (a mountain, a river, the sky), the lesser and the powers local spirits; clerics serve a spirit; festivals follow the land's seasons. Philosophies (clerics of an ideal) were offered and not taken: a cleric without a god weakens the D&D feel. Monotheism was approved first and then removed (2026-10-08, at the specification's last check): its one god could not fill the epic band of great gods.
- **`pantheon_dualist` sets the great gods:** its two powers are the two greater gods and the two great gods at every scale (one church per side), whatever the scale's band; at short this takes two of P4's few faction seats, which P4's tag pass weighs.
- `pantheon_polytheist`'s hook "the villain's god and the world's god are different gods" is rewritten: a villain's god exists only when the threat pins one (P1's W1); the web holds at least one rivalry and one alliance.
- `pantheon_dead_gods`: what answers prayers now is public or discoverable texture (S0 #6), not a god's secret, unless the threat's secret uses it.
- `pantheon_silent_gods` stays but never stands with `presence_omens` or `presence_walking` (the gods would be speaking).

**Presence** (`pantheon.yaml#presence`). All six kept. `presence_walking` is forced when `break_gods_among_mortals` is rolled. `presence_through_phenomenon`'s hook due at P1 is deleted (S0 #7).

**Rank and the counts.** The three ranks stay (greater, lesser, power). The god count is rolled in the scale's band, the rank split within the ranks' shares summing to it, and the great gods (whose churches are P4 factions) in their band with its floors; the great gods are chosen among the greater gods. **The threat's god:** when the threat is a god (`family_god`: an avatar, a fallen or an imprisoned god) it is one of the counted gods, of rank lesser or power; when the power behind the villain is a god (`power_god`) it is a counted god of any rank; both are rolled secretly, and the pantheon shows only the god's public face. **The pilgrim road's god** (the lifeline) is a greater god.

## S2 — Pantheon II: domains, churches, relations, god secrets (owner-approved 2026-10-08)

**Domains** (`pantheon.yaml#domain_scaffold`). All eight stay. A god's domain is a fact of the world, not a rule text: the SRD 5.1 prints only the Life domain's subclass, and a player who wants another reads it in their own book (the skill prints no non-SRD rule text). Each god's 1-2 domains are rolled to the scale's coverage rule, and its alignment from its domain's `alignments`. **At standard and epic at least one god is evil** (its cult can be a hand). Light's church shape loses "order of lamplighters", and its "a temple on a height" becomes "a sun temple on a height" (the owner's tired images).

**Churches** (`church_archetype`, 11 rows kept). The archetype is rolled for the greater gods only; the great gods among them carry it into P4 as factions. Lesser gods and powers take one church line rolled from their domain's `church_shape`. P2's row owns the church's form; P4's faction follows its `faction_archetype`.

**Relations** (`relationship`, 11 rows kept). The script builds one connected web: each god after the first is joined to an earlier god by a rolled relation, and each greater god takes one more; a polytheist web holds at least one rivalry and one alliance. `rel_mirror` is drawn only when the threat pins a god. Hooks that made a relation a god's secret (the silenced one, the usurped, the stolen domain) become discoverable stories under S0 #6.

**God secrets** (`god_secret`). The seven secret-tier rows are deleted (is dead, is two gods, backs the villain, is bound, usurper, is the phenomenon, is the land; the threat's own rows already carry the patron and the bound god). The five discoverable rows stay as texture (was mortal, lies about its domain, fading, younger than claimed, not silent but unheard): **one per campaign at standard and epic, none at short**, on a greater god. The domains' `secret_tendency` lists keep only these five; the silent gods' and the silenced one's "why" is a discoverable story, not a secret.

## S3 — Planes (owner-approved 2026-10-08)

**Baseline** (`planes.yaml#baseline`, 26 rows kept, own labels for the Product Identity names). **Three new rows**, each with a label of this table's own (the names are not in the SRD 5.1): the fey echo (the bright echo of the world: archfey, hags, fey courts, the elves' withdrawal), the shadow echo (the dark echo: shadows, the undead's road), and the realm beyond (aberrations: the threat family "from beyond"). The energy planes were offered and not taken.

**Rolls, in order** (none was rolled before):
1. The touched count: short 1, standard 1-2, epic 3-6, plus the magic dial's `planes_touched_modifier`; never below 1.
2. The planes P1 names are seated first as touched (the thin place's plane, the ruin's, a scar's, the move's), shared to fit the count.
3. **At epic** one free touched seat goes to the threat's home plane, rolled secretly (a devil the Nine Hells, a demon the chaotic evil plane, a fey or a hag the fey echo, a thing from beyond the realm beyond, a genie or an elemental its element, a fallen celestial an upper plane, an undead or a shadow the shadow echo), so an epic finale can stand on the villain's plane.
4. Each touched plane rolls a deviation (unchanged, renamed, merged, removed, inverted, a place in this world, reachable by dying), a time rate, a way in, a cost and a keeper (a power-rank god of the pantheon that fits the plane, else an SRD creature of that plane). Untouched planes stay unchanged unless a break names them.
5. A touched plane's name comes from a name pool (errata #25).

**Changes:** `dev_secret_holds` ("the big secret's home") is deleted (S0 #6). `cost_name` is rewritten without the undefined rite: "the traveller's true name is taken; they answer to no other". The sixteen copies of the outer planes' hook become one common hook.

## S4 — Magic (owner-approved 2026-10-08)

**The principle: no magic row changes a character's spellcasting by the rules.** A row says how the world sees magic, rules it and makes it pay; a player character's spells work as the 2014 rules write them (the line of build 18b's class cores).

**Constraint** (`magic.yaml#constraint`). Kept: components, caste, licence, echo. Deleted: time, place, price in self, exhaustion, witness (each turned a character's spells off or charged them), and none known (a P2 secret, S0 #6). **New row** `constraint_law_and_folk`: "magic's only limits are the law and what the folk will bear" (the classic D&D world).

**Source** (`magic.yaml#source`). Kept: the planes, the dead, the land, blood, names, bargains, the phenomenon, study, nobody knows. `source_the_gods` loses its secret: "magic flows from the gods; the churches call a wizard's formulae prayers in another tongue". `source_a_dying_thing` is public: everyone knows the source is running out. `source_the_sleeper` is deleted (texture as the doom, against G10).

**Visibility** (6) and **taboo** (12) are kept. `taboo_casting_on_a_day` requires a seated holy day in the calendar; `taboo_the_phenomenon_unlicensed` requires a phenomenon someone can use.

**Regulator** (9, kept). The three rows that override who regulates become forced records with their reason (no free choice by the writer).

**Wild** (7, kept). `wild_dead_god_static` requires the dead gods type or a dead-god ruin; `wild_overflow` requires a phenomenon that can overflow.

## S5 — History (owner-approved 2026-10-08)

**Seated by the script** (story layer; seated before any roll and counted inside the scale's events): the move (its date from P1's time row), the ruin's fall (an age named from the ruin source), the villain's origin event (secret; its true layer comes from P1's secret chain), the signature institution's founding.

**Ages** (`age_template`, 14 rows kept). The first age and the present stay in place, the ruin's age is seated, and only the ages between are rolled. The present age is named for what the folk fear of the threat's public face. `age_dimming` loses its doom hook (G10). `{Name}`, `{Thing}` and `{Rulers}` come from the name pools.

**Event types** (16) are kept.

**Divergence** (taught against true). At most one per campaign at short, two at standard, three at epic; every other event's layers agree. The secret rows: "the disaster was caused", "the villain of the story was the victim" and "someone survived who should not have" become discoverable texture; "it never happened", "the miracle was a device or a rite" and "the price was hidden" are deleted. The campaign's secret comes from P1's chain alone.

**Memory** (7) is kept. Witness lists are written for the seated story events only, so they do not swell P5's people.

**The amounts by scale:** short 3 ages, 5-7 events, 2 deep-past events; standard unchanged (3-5, 8-12, 3-5); epic 4-6 ages, 10-14 events, 3-5 deep-past events.

## S6 — Calendar (owner-approved 2026-10-08)

**The year is fixed, not rolled: twelve months of 28 days, a seven-day week** (Greyhawk's and Eberron's shape): every month is exactly four weeks and one turn of the moon. This replaces the earlier ruling "months of 30 days", and the `year_shape` and `week` tables leave the rolls. Why: in play a seven-day week inside a 45-day month made time hard to follow; every classic D&D calendar has twelve months whose weeks fit them. A world differs by its names, seasons, moon and festivals.

**Climate** (8): rolled only among the climates the palette's land kinds allow; the underground era forces `climate_underground`, which is excluded in every other era; no cross-campaign avoid. **Underground:** the months are counted by the light's cycle or by a great clock, one of the two rolled.

**Moon** (7): a P1 row that needs a moon (the moon trade, night is safe, a weakness on an eclipse or a moon night) excludes `moon_none_stars`; `moon_is_a_plane` counts as a touched plane and is drawn only when a touched seat is free.

**Festivals** (16): one per greater god (its domain's festival) and one or two folk festivals rolled (not the gods band's top, which drew 14 of 16 at epic). Names from the pools, as the months'.

**Dated days:** the empty month and the lawless day (P1), the taboo's holy day, and any other dated day are seated inside the campaign's span (the scale's sessions × days per session with the slack; 40-60 days at short, as `docs/p1-tags.md` already ruled for the empty month).

**Start anchor** (6) follows P1's move time: "happening now", a few days after the move's last step; "about to", a counted number of days before its next step (`anchor_days_before_doom` is reworded to it); "a generation ago", rolled among festival eve, season start, market day and midwinter.

## S7 — The writer, the critics, the card (owner-approved 2026-10-08)

1. **The prompt and the template are rewritten on the chain** (as P1's in build 18e): the script writes P2's frame (ids, types, every rolled field) at `phase P2 begin`; the writer writes prose on it, takes every proper noun from the pools, and decides nothing a table decides. "The big secret usually hides in this layer" is deleted.
2. **Rubrics.** `rubric_p2_gods_carry_question` is rewritten on the threat: the threat's god and powers stand in the cosmos, the planes P1 names are there, and each side of the question has a god or a rite to call on. `rubric_p2_history_diverges` is rewritten: the move, the ruin's age and the villain's origin are on the timeline, and the divergences that exist do not compete with the campaign's secret. `rubric_p2_calendar_felt` stays. **New** `rubric_p2_dnd_legible`: a cleric or paladin player can choose a god and a domain; the planes answer the SRD's plane spells; no magic row breaks a class's rules; the threat's dates stand on the calendar.
3. **Script checks** (the door and the ledger): the god count and the domain coverage; at least one evil god at standard and epic; a festival per greater god; the four seated story events; every plane P1 names is touched; months of 28 days and a seven-day week.
4. **The P2 card**, without dice or row ids (as P0's since build 20b): the gods with their ranks and domains, the touched planes, magic in words, the ages, the calendar and the start date.

**The review of P2 is complete.** The specification follows as build item 22 (`docs/p2-build-22.md`), part by part, to the coding tab on the owner's word; the P2 tables get their reviewed stamps when the rows are written.

## The tag system holds for P2 (owner, 2026-10-08)

Asked by the owner after the review: P1's nine tag rules (`docs/p1-tags.md` §1: claims, clashes declared pair by pair, overrides, requires, fits, the dials as the root, per-row reviewed stamps and the five-row floor, one target one owner) apply to P2 in full. The review above named only the clashes it met; a full tag pass comes first in build 22 (`docs/p2-build-22.md`, 22a-0): the coding tab drafts every row's claims, the candidate clash pairs (P2 against P2, P1 and the dials), the overrides, requires and fits, the "who sets what" chart's P2 targets and the clash share before; the design tab audits; the owner reviews the new topics and the clash pairs; then the rows are built.
