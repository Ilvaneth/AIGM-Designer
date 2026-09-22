# Sandbox Index — how to run Ashen Crown as a living world

Written 2026-08-23 after the table flagged that sessions 1-2 ran as a single unbranching line: job → heist → lead → travel → lead → travel. Every scene was a direct consequence of the last, no independent content existed, and the Chapter 1 "build a power base" arc note had nothing attached to it the party could actually take.

**This layer fixes that.** Read this file at the start of every session.

---

## The rule

Nothing in this campaign is purely a side quest and nothing is purely main plot. Every site is also a favor someone wants done, a secret someone wants kept, or a resource someone else is already using. Every NPC has an agenda that generates work independent of the Crown.

When the party finishes anything, they should have **at least three visible options** and no obvious "correct" one.

---

## Files

### People — everyone wants something
| File | Who | Their real agenda |
|------|-----|-------------------|
| `npcs/mother-vey.md` | Gallowmere fence | Keep Gallowmere belonging to no faction |
| `npcs/fennick-orle.md` | Barkeep, gossip broker | Own the town's *debts*, not its coin |
| `npcs/sefwyn-marrow.md` | "The Grey Tally" | Stop being someone's instrument; skimming a private relic archive |
| `npcs/doreth-kell.md` | Garrison commander | Escape south before the war arrives |
| `npcs/sarelle-duskbourne.md` | Concordat leader | Administer the Crown, and have *someone else* pay its price |
| `npcs/coren-ashvale.md` | Compact Warmarshal | Keep the war profitable — but the Concordat took his family's tombs |
| `npcs/hesta-bram.md` | Thornwick innkeeper | Keep her village alive; watched the crypt excavation |
| `npcs/corran.md` | Thornwick trader | Own the village when the war ends |
| `npcs/alis-wend.md` | Refugee mother | The party's victim — the live consequence thread |
| `npcs/orell-tain.md` | Concordat archivist | Wants fragments kept apart, permanently; losing that argument to Sarelle |

### The world — start here
**`gazetteer.md`** is the master map: eight regions tiered from level 1 to 20, every settlement and site named and placed. Read it when the party wonders where to go. It exists because the first pass gave them one town, one village, and nowhere else — which is why everything kept routing back to Gallowmere.

| Region | Levels | Contains |
|--------|--------|----------|
| I. The Marches | 1-4 | Gallowmere, Sallow Ford, Nettlecombe + 7 sites |
| II. The Thornlands | 3-6 | Thornwick, Harrowgate, Ostwick + 4 sites |
| III. The Cindermoor | 4-8 | Cair Dunnow + 4 sites |
| IV. Karsgate | 5-10 | The city — 5 districts + undercity |
| V. The Ashvale | 8-10 | Ironhold, Ashvale Necropolis (Ch.1 climax) |
| VI. Emberhold | 11-14 | The capital — Chapter 2 opens here |
| VII. The Sundered Reach | 13-17 | The ash-kings' country; a dragon with a fragment |
| VIII. The Grey Kingdom | 17-20 | Shadowfell echo — the endgame |

### Places — each one is a fight, a treasure, and a complication
| File | Level | Also is |
|------|-------|---------|
| `locations/gallowmere.md` | — | Home base; the Chapter 1 prize |
| `locations/sallow-ford.md` | 1-4 | Toll town; launder the stolen horses; first Compact contact |
| `locations/thornwick.md` | — | Village with five real locations, not one tavern |
| `locations/harrowgate.md` | 3-6 | Market town, orthodox temple archive, **an empty magistracy** |
| `locations/karsgate.md` | 5-10 | **The city** — both faction chapterhouses, undercity, urban territory |
| `locations/the-drowned-mill.md` | 1-3 | Kell wants it, Vey owns it — no neutral way to loot it |
| `locations/sorrels-hollow.md` | 2-4 | Kriv's only living lead + recruitable armed force |
| `locations/the-ash-kilns.md` | 2-5 | Cult cell + best power-base target in town |
| `locations/the-weeping-tower.md` | 3-5 | Ilvaneth's ambition made into a dungeon |
| `locations/hollowmoor-barrows.md` | 4-6 | The great false lead — no fragment, but the truth about the Crown's price |
| `locations/vaelthorn-crypt.md` | visited | Unresolved: the Concordat came back and *left* something |
| `locations/ashvale-necropolis.md` | 8-10 | Chapter 1 climax — not a Chapter 1 destination. **Built to full standard session 11, 2026-09-02** — 22 rooms, Concordat garrison vs. Ashvale ghost guardians (real, exploitable faction conflict), Sarelle Duskbourne survives by design (not a kill-boss). Seams into `the-chalk-warrens.md`'s Room 10 |
| `locations/the-makers-undoing.md` | 5-7 | Standalone, faction-free Vault — built session 11, collaboratively with the DM, room-by-room; never played. 20 rooms, internal escalation curve |
| `locations/the-debased-mint.md` | 7-9 | **A genuine fragment site** — House Doskarn's own secret mint, Karsgate Undercity. Built session 11; a direct thematic mirror to Kriv's own ascension (unmanaged fragment corruption, generations compressed). 18 rooms, never played |
| `locations/the-unquiet-barrow.md` | 6-7 | Standalone, faction-free — campaign's first **Maze**-type site, Thornlands. Self-rearranging rooms, a single recurring Xorn predator, whoever's buried here deliberately never named. 18 rooms, never played |

Another ~15 sites are named and outlined in `gazetteer.md` — flesh one out when the party heads for it.

### ⚠ Read these two before running any fight
| File | Why |
|------|-----|
| **`two-player-scaling.md`** | **This party is two characters.** Every level range in every other file assumes four. The session 2 goblin ambush was mathematically *Deadly* and was run without realizing. Read the thresholds table before building any encounter. |
| **`.claude/rules/dungeon-design.md`** | **Read before building any multi-room dungeon.** Four-phase standard (concept/logic, non-linear map, four content types per room, DM pacing) written after The Widow's Hollow was called out as thin (session 5) — a room count alone doesn't mean a full dungeon. |
| `encounters/` | Runnable encounter files in the framework's format. `py .claude/scripts/load_encounter.py ashen-crown <name>` |

### Systems
| File | Use |
|------|-----|
| `gazetteer.md` | The map. Where to go next, at every tier. |
| **`ascension-tracks.md`** | **What the fragments are doing to both PCs.** Stage gates, powers, costs, and the running tracker. Advance it every time they gain a fragment. |
| **`roleplay-and-xp.md`** | RP rewards, Inspiration, and the rule that the DM enforces mechanics — never personalities, never roleplay |
| **`system-register.md`** | **What's built, what's tested, what's still missing.** Check before relying on any system. |
| **`bug-log.md`** | **Every bug/gap found, categorized and dated.** Check its frequency table before treating a new bug as one-off. |
| `kriv-thread.md` | Kriv's full arc — House Shestendeliath, the traitor, the sister, the blood |
| `chapter-2.md` | Levels 11-20 — three acts, Emberhold/Sundered Reach/Grey Kingdom, and the five endings |
| `campaign-clock.md` | **What the factions are doing right now.** Advance at every session start. |
| `progression.md` | XP and milestone pacing 1→20; what each PC gets on level-up |
| `bestiary.md` | What lives where, by region and tier. All SRD-grounded. |
| `treasure.md` | Magic item progression by tier + named campaign items + what's been awarded |
| `rumors.md` | d12 pool, tagged true/half/false. Roll when they drink, listen, or ask around. Log what's been given. |
| `jobs-and-opportunities.md` | Keep 2-3 `OPEN` in front of the party at all times |
| `power-base.md` | The five holdings in Gallowmere — the machinery of the Chapter 1 arc |
| `faction-subplots.md` | Internal fractures in all three factions — the party can exploit or ally |
| **`faction-renown.md`** | **The party's numeric standing with each faction.** Run `py .claude/scripts/faction_renown_check.py ashen-crown --status` before any scene where faction attitude matters |
| `.claude/rules/trap-mechanics.md` | Structured DC/trigger/effect/countermeasure template — read before placing or resolving any trap |
| `.claude/rules/chase-mechanics.md` | Round-by-round pursuit/evasion structure — read before running any chase scene |
| `travel-encounters.md` | Five regional d10 tables. Roll per day/night, log results. |
| `dm-notes.md` | Plot state, session records, standing house rules |

### Lookups
```bash
py .claude/scripts/srd_lookup.py monster "Ghoul"
py .claude/scripts/srd_lookup.py item "Flame Tongue"
py .claude/scripts/srd_lookup.py spell-list "Wizard" "2nd Level"
```

---

## Personal threads — keep BOTH live, every session

**`kriv-thread.md` is required reading** alongside this file. Kriv's arc was originally three breadcrumbs against Ilvaneth's full architecture; it now runs in parallel with its own sites, antagonists, treasure, and endings. Never run a session where one PC's thread is live and the other's is dormant.

| | **Ilvaneth** | **Kriv** |
|---|---|---|
| **Question** | Can I stop being nothing? | Is legitimacy real, or just who holds the sword? |
| **Dedicated site** | The Weeping Tower | **Shestendeliath Hold** |
| **Second site** | Hollowmoor Barrows (the price) | Sorrel's Hollow → Karsgate (the traitor) |
| **Living antagonist** | Sarelle (offers her everything) | **Vharkoss** (the uncle who sold the house) |
| **Complicating kin** | Her mother, unplaced | **Sethra** — his sister, alive, a Compact officer who *doesn't want the house restored* |
| **Named treasure** | Harn's Spellbook → Robe of the Archmagi | **Wardensteel**, the Oathplate, **the Charge-Roll** |
| **Faction leverage** | Cinder Choir (if she dies and returns) | Ironclad Compact (via Sethra) |
| **Ascension** | The Crown's pattern — stops aging, stops dying | **Draconic awakening** — scales, breath, presence, wings |
| **Endgame** | Endings 1 & 2 | Endings 3 & 4 |

**The wedge**: House Shestendeliath were **Ash-Wardens** — sworn to keep the fragments *apart*, and chosen for the office because they carry **dragon blood**. Kriv's blood wakes as fragments are gathered (`ascension-tracks.md`), so his inheritance says scatter them and his blood says bring them closer. The conflict is inside him before it's ever between them.

**They both know.** Neither hides what they're becoming — they swore never to lie to each other and they haven't. Kriv is becoming something that will never let her go; Ilvaneth is losing the memory of why she'd want to stay. Both watch. Neither asks the other to stop.

**The revelation**: the fragment they already carry is very likely his family's — a surviving retainer fled south with the fragment *and* the hatchling heir, and hid one in the ossuary while leaving the other at the orphanage. Kriv was in Gallowmere because the fragment was. See `kriv-thread.md`.

- **The Wend family**: the con will surface. Play it as complication, not punishment.

---

## Session checklist

**At the start:**
0. Skim `system-register.md`. If tonight is likely to need something marked ❌, build it *before* play, not mid-scene.
0a. Run `py .claude/scripts/settlement_density_check.py ashen-crown --check` — computes this directly (population from `gazetteer.md` vs. actual location count) instead of checking by hand. If the party is heading toward a settlement it flags, flesh it out now before they arrive. Structural count only, not a content-quality judgment — still read `dm-notes.md`'s settlement-scaling table for the required categories (inn, religious site, etc.) once a settlement is flagged.
0b. Run `py .claude/scripts/open_threads_check.py ashen-crown` — advisory, flags `state.md`'s Open Threads entries that have sat 20+ in-fiction days with no movement. Added 2026-08-30 after two entries were caught already-resolved but never marked (the events they described had happened, the checkbox just never got flipped). Not every flagged entry needs action — check each one honestly before touching it.
0c. Run `py .claude/scripts/foreshadowing_check.py ashen-crown` — advisory, flags `info/planted-hooks.md`'s deliberately-planted narrative details (Chekhov's guns — the signal horn, the crypt ward stone, etc.) sitting unresolved 25+ days. Distinct from Open Threads: this is specifically for planted items/details set up to pay off later, not general plot facts. Added 2026-08-30, same session as the Open Threads staleness check, sharing its pattern.
1. `py .claude/scripts/sync_state.py ashen-crown --check` — if it reports drift, something was played and never written down. Fix it before continuing.
1a. `py .claude/scripts/rest_check.py ashen-crown --check` — if it reports DRIFT or NO RECORD, a long rest is owed before anything else happens. Run `--apply` before continuing.
2. Advance `campaign-clock.md` by the in-fiction days elapsed. What fired?
3. What has moved **off-screen**? Sarelle collects. Sefwyn tracks. Kell saves. Fennick lends.
4. What are the party's three visible options right now? Which `LATENT` job has its trigger been met?
4b. **At least one standalone, no-strings site should exist and be findable at all times** — see `dm-notes.md`'s note on session 5 table feedback. Every other site in this sandbox is deliberately interwoven with a favor/secret/faction; that's good density but means there's normally no pure "just go explore" option. `locations/the-widows-hollow.md` is the first one. If it gets resolved (looted, hag dealt with or bypassed), the next one to build doesn't need a reason to exist — that's the point.
4a. **Loot pacing check** (`info/treasure.md`): as of session 2's end, Tier 1 is behind target (0 permanent items, target 5-8 by session 8-12). If the party is near Gallowmere with nothing more urgent pulling them elsewhere, **the Drowned Mill must be one of the three visible options** (level-appropriate right now — Weeping Tower is not, see the file). Don't skip this step just because it's not the only thing going on.

**During play — write it when it happens, not at the end:**
5. Every HP change, gold change, or resource spend → `update_character.py` immediately.
6. Location, session number, quest status, and day count → edit `state.md` when they change in play.
7. Roll travel encounters *before* narrating any journey, and log the rolls. **After a multi-night journey resolves** (or any time the in-fiction day is about to advance), run `rest_check.py --check` — DRIFT means run `--apply` before the next scene, not after.
7a. Awarding roleplay XP → `award_rp_xp.py ashen-crown <character> <session> "<reason>"`, never a hand-added row. It enforces the 3/session cap itself.

**At the end:**
8. `py .claude/scripts/sync_state.py ashen-crown --sync`
9. Log rumors given, XP awarded, ascension progress, and clock movement back into the relevant files.
