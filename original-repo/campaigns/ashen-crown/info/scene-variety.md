# Scene Variety — a reference table, not a random roll

**Why this exists**: the DM flagged directly (2026-08-30) that actual play has felt thin on variety — sessions default into a repeating combat→travel→combat chain, and even non-combat content (Cole, Corvin) has only surfaced when the party explicitly asked an NPC "do you need anything," rather than a scene offering it. This file is the proactive half of the fix: a reference to consult *before* deciding what happens next, not a table to roll blind on (unlike `travel-encounters.md`, which genuinely is randomized). The reactive half — checking whether the last few beats actually varied — isn't yet automated; use this table as the source of truth when deciding that variety is needed.

**The mistake to avoid**: don't force every category through an NPC. That recreates the exact problem this file exists to fix — content feeling like it only exists when a person is standing in front of the party to hand it over. Combat and Exploration in particular should regularly happen with **no NPC present at all**.

---

## Combat — NPC-independent by default

- A travel-encounter roll (`travel-encounters.md`) — already the established mechanism
- A `regional-threats.md` bounty (The Drowned Reeve, The Hollow Reaper, The White Reaver, etc.) — a hunt the party chose, not a story-forced fight
- A site's resident threat encountered while exploring (no dialogue first — the fight *is* the content)
- Being hunted: Sarelle's investigator, a Concordat patrol, a rival gang — the party as the target, not the initiator

## Social/Negotiation — usually NPC-linked

- A deal or negotiation (Corvin Thale, Corla Vint, Sefwyn Marrow, Orvenna Kest)
- A confrontation forcing a hard truth out of someone (the Fennick Orle model — direct, not fished-for)
- A faction-level meeting (Tain, Factor Grine, a Choir contact)
- A social event with its own texture (Corran's card game, the Wagered Crown, the Sonnward Promenade) — content emerges from *being* somewhere, not from asking a specific person a specific question

## Investigation/Puzzle — mixed

- Reading a scene for clues without anyone to ask (`dungeon-design.md`'s environmental storytelling — scorch marks, a barricaded door, worn paths)
- Interrogating someone already captured or cornered
- Archive/library research (the Ember Crown temple archive, the Scriptorium, Sister Mave's records)
- An actual mechanical puzzle or warded obstacle (Kargrim's Reach's Rigged Gallery is the campaign's own worked example)

## Downtime/Personal — often NPC-independent

- A quiet beat between Kriv and Ilvaneth — the bond, an ascension cost surfacing, a memory lost or a hoard-sense flare-up, no third party present
- Crafting, shopping, resource management, training
- Managing a power-base holding directly (Gallowmere's docks/garrison plan, Renata Kroll's Harrowgate offer)
- A personal errand tied to one PC's own thread (`kriv-thread.md`, Ilvaneth's transcendence research) that doesn't route through a negotiation

## Exploration — NPC-independent by default

- First arrival at a new named location (now gets the cinematic wide→close treatment, `cinematic-moments.md`)
- Working through a dungeon's non-combat rooms (`dungeon-design.md`'s density standard — every room has *something*, not just the ones with a fight)
- A journey itself as content, not just a transition (weather, terrain, the road's own texture — `gazetteer.md`'s Regional Topography table)
- Following a rumor or a map to somewhere new, with no NPC guiding the way there

## Faction/Political — mixed, sometimes NPC-free entirely

- A `world-events.md` roll firing, or a `gazetteer.md` Region Control shift — the world moving without anyone physically present to announce it
- A `consequences.md` threshold crossing, delivered as news/rumor rather than a face-to-face scene
- A faction meeting or proposition (genuinely NPC-linked — Tain, Grine, a Choir approach)
- A `jobs-and-opportunities.md` job surfacing organically through the world (see `.claude/rules/npc-consistency.md`'s NPC-job-surfacing note) rather than through the party asking

---

## How to use this

Before deciding what happens next in an open moment (the party has just finished something, or is choosing a direction), glance at what the last 2-3 real beats actually were. If they cluster in one category — especially Combat or Social, the two easiest defaults — deliberately reach for one of the others, and pick a concrete example from the relevant row above rather than inventing from nothing. This is a conscious check, not a dice roll: the party's own choices should still drive *which* thread gets pulled, this table just widens what's available to offer.

**Downtime/Personal specifically is now tracked across windows, not just within one** (Buildable-list item #4, 2026-08-30): `session_pacing_check.py` persists a streak of consecutive 20-turn report windows with zero Downtime/Personal signal, and escalates to an explicit ALERT once it hits 3 (~60 turns with no downtime content at all) — a real multi-window cadence gap, not just this window's mix. A true multi-*session* tracker wasn't built instead because the live transcript has no reliable session-boundary marker to key off of; the turn-window streak answers the same question without that dependency.
