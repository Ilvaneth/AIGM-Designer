# Two-Player Scaling — read before building any encounter

**This party is two characters.** Every level range in `bestiary.md`, `gazetteer.md`, and every published adventure assumes four. Ignoring this will kill Ilvaneth and Kriv, repeatedly, by accident.

---

## The rule that gets forgotten

Encounter difficulty uses an **adjusted XP** total: raw monster XP × a multiplier based on how many monsters there are.

| Monsters | Multiplier |
|----------|-----------|
| 1 | ×1 |
| 2 | ×1.5 |
| 3-6 | ×2 |
| 7-10 | ×2.5 |
| 11-14 | ×3 |
| 15+ | ×4 |

**With fewer than three characters, use the next higher multiplier.** So for this party, two monsters is ×2, three monsters is ×2.5, and so on.

## Thresholds for THIS party (2 characters)

Per-character values doubled. Compare **adjusted** XP against these.

| Level | Easy | Medium | Hard | **Deadly** |
|-------|------|--------|------|--------|
| 1 | 50 | 100 | 150 | **200** |
| 2 | 100 | 200 | 300 | **400** |
| 3 | 150 | 300 | 450 | **800** |
| 4 | 250 | 500 | 750 | **1,000** |
| 5 | 500 | 1,000 | 1,500 | **2,200** |
| 6 | 600 | 1,200 | 1,800 | **2,800** |
| 7 | 700 | 1,500 | 2,200 | **3,400** |
| 8 | 900 | 1,800 | 2,800 | **4,200** |
| 9 | 1,100 | 2,200 | 3,200 | **4,800** |
| 10 | 1,200 | 2,400 | 3,800 | **5,600** |
| 11 | 1,600 | 3,200 | 4,800 | **7,200** |
| 12 | 2,000 | 4,000 | 6,000 | **9,000** |
| 13 | 2,200 | 4,400 | 6,800 | **10,200** |
| 14 | 2,500 | 5,000 | 7,600 | **11,400** |
| 15 | 2,800 | 5,600 | 8,600 | **12,800** |
| 16 | 3,200 | 6,400 | 9,600 | **14,400** |
| 17 | 4,000 | 7,800 | 11,800 | **17,600** |
| 18 | 4,200 | 8,400 | 12,600 | **19,000** |
| 19 | 4,800 | 9,800 | 14,600 | **21,800** |
| 20 | 5,600 | 11,400 | 17,000 | **25,400** |

## Worked example — the session 2 goblin ambush

2 Goblins × 50 XP = **100 raw**
Two monsters → ×1.5, bumped to **×2** for a two-person party
**200 adjusted = exactly Deadly at level 1**

And it played that way: one arrow took Ilvaneth from 8 to 3 HP. A second hit drops her. This was run without realizing it — don't repeat the mistake blind.

---

## What this means in practice

- **A "level 4-6" site in `bestiary.md` is a level 6-8 site for this party.** Read every level range in these files as roughly +2 unless the party has help.
- **Two PCs have no action economy.** Four enemies get four turns against their two. Numbers hurt this party far more than a single big monster does — a single CR 3 creature is often safer for them than five CR 1/4 creatures.
- **No healer.** Kriv has Second Wind (self only), Ilvaneth has nothing. Downed means downed. Keep Potions of Healing in the loot flow deliberately — `treasure.md` lists them at tier 1 for exactly this reason.
- **A single bad round can end a character.** At low levels especially, build in escape routes, surrender options, and enemies with morale. Not every fight should be to the death — and for a Neutral Evil party, enemies who can be bought, bluffed, or turned are more interesting anyway.

## Fixing it properly — get them help

The two-player problem has an in-fiction solution the campaign is already set up for. Push these:

1. **The Sorrel's Hollow deserters** (`locations/sorrels-hollow.md`) — a dozen soldiers and a veteran sergeant, recruitable. Two or three of them as regular companions transforms the party's survivability and costs only coin and loyalty.
2. **Hirelings.** Gallowmere and Harrowgate both support hiring muscle. Cheap, expendable, thematically perfect for this party.
3. **Sidekick rules** — give one recurring NPC a proper sidekick class progression so they level alongside the party.
4. **The refugee camp** (`power-base.md`) — several hundred desperate people is a recruitment pool.

**Recommendation**: steer toward at least one permanent companion before the party attempts anything above Marches-tier. A two-person party at level 8 walking into Ashvale Necropolis without support is not a challenge, it's an ending.

## The surprise+AoE trap — why "Deadly" hasn't actually felt deadly

**Confirmed by a full retroactive audit, 2026-08-29** (the DM flagged combat as too easy, "yenilmez gibiyiz" — the audit checked every logged fight from session 2 through 6): the adjusted-XP formula above is being computed correctly every time, but it doesn't model one specific interaction that has quietly neutralized it in most fights — **surprise removes a full round of enemy actions, and this party's burst/AoE (Thunderwave at level 1, Fireball by level 5, Scorching Ray crits) then compresses several enemies' HP pools into that same dead round.** The result: encounters rated **Deadly on paper have been resolved with zero party HP lost**, including the session-3 twelve-body convoy ambush and the session-6 Millward Road convoy (both 2,400+ adjusted XP, both "wiped with zero casualties").

**This is not a math error and not a one-off** — it's the default outcome of any fight the party can approach on their own terms, at every level checked (1 through 5). The fix is not a higher CR; CR has already been pushed to Deadly multiple times and still got flattened.

**What actually produced tension, every time it happened** (per the same audit):
- **Surprise was denied.** Hollowmoor's "skeletons" surprised the *party* instead. Kargrim's Reach's Room 3 and Groth's Hall were built "alert, no surprise" — both were the tense fights in that dungeon. The hell hound tracked the party by scent through Invisibility and Stealth (`noise-and-detection.md`'s tools already do this — it just needs to be used more often, not just for one hell hound).
- **The alpha strike didn't cleanly finish the target.** Roskel took 3 full rounds and hit Kriv for real damage. The Web Gallery ettercap survived long enough to land 18 damage on Ilvaneth (37% HP, the closest call in five sessions). The Warden got a full turn in before Action Surge ended it.
- **The encounter was a single strong creature, not a group.** A solo monster has one HP pool that survives round 1 regardless of surprise and gets a real turn — this is structurally nova-resistant in a way a group of weaker enemies never is. (Confirmed encouraging: all five `regional-threats.md` bounties are solo creatures — already built the right way for this reason, without it being planned.)

**Building for real tension going forward — concrete techniques, not vibes:**

1. **Not every encounter should be surprisable.** Give a real fraction of fights a genuine detection chance the party can't stealth past on a good roll alone: rotating patrols, a sentry with blindsight/tremorsense/keen senses, or a creature that tracks by something other than sight (scent, vibration) the way the hell hound already did. This should be the norm for anything meant to matter, not a rare exception.
2. **Solo is necessary but NOT sufficient — corrected 2026-08-29.** The DM caught this directly: the campaign's own audit already had two counter-examples sitting in it. The Kargrim's Reach basilisk and the Widow's Hollow ochre jelly were BOTH solo creatures, and both still went down in one hit with zero HP lost — "the basilisk never got a turn" is a direct quote from the same audit that recommended solo creatures. Solo avoids the *group multiplier problem* (many weak HP pools, one nova clears them all), but it does nothing by itself if the one HP pool is still smaller than the party's round-1 burst. **The actual fix has three layers, and a real boss needs at least two of them:**
   - **Size HP against the party's actual burst, not the CR table.** Estimate this party's realistic max coordinated round-1 damage (a Fireball/upcast blast plus Kriv's full attack routine, with Action Surge if it's a real set piece — commonly 60-100+ damage by mid-to-high level) and give a "must survive to act" boss HP with real margin above that, not just whatever the standard stat block says. A basilisk's ~52 HP was never going to survive that math regardless of being solo.
   - **Resistance or immunity to this party's signature damage types** (fire, thunder, radiant-vs-undead) cuts the effective burst directly — already technique #4 below, but it matters *most* for a solo boss specifically, since there's only one HP pool for it to protect.
   - **Legendary Actions and/or Legendary Resistance**, the SRD's own answer to this exact problem (already used on SRD dragons) — Legendary Resistance (2-3/day) stops a single save-based effect from neutralizing the fight outright; Legendary Actions let the boss act between other combatants' turns, keeping later rounds dynamic even when round 1 goes badly. Homebrewing these onto a non-dragon boss statblock is the same kind of standard-rules adaptation already used elsewhere in this project (Battle Master maneuvers, non-default subclasses) — follow the published pattern, don't invent a new one.

   **Not every fight needs this** — routine/non-climactic encounters can and should stay as ordinary groups for texture and variety; making *everything* a reinforced solo boss would just trade one monotony for another, per the DM's own point. Reserve the full treatment for fights actually meant to be memorable.

   **Even a properly floor-checked solo boss can still die in round 1 with zero party damage — caught the same session, immediately after the fix above.** The wayside Specter fix above only modeled Kriv's *plain* weapon floor (34/round vs undead). The very next fight — a real prepared boss, 95 HP, checked against that floor beforehand — still went down in round 1 for 114 total damage (Kriv's 4-attack Action Surge round with 3 Battle Master maneuvers spent = 83, plus Ilvaneth emptying a Wand of Magic Missiles = 31), because the floor check never modeled Superiority Dice maneuver bonus damage, Action Surge doubling the attack count, or a caster's actual burst option (Fireball, Scorching Ray, a full-charge wand) at all. The DM's own hand math confirmed the real ceiling: `solo_burst_check.py --full-nova` now computes it directly — Kriv's Action-Surge-and-full-maneuver ceiling alone is **~86 vs undead**, and a caster's real nova (Fireball ≈28, a full wand ≈31+) stacks on top, putting this party's genuine level-5 round-1 ceiling in the **110-130+** range, not the ~34-68 the floor-only check suggested.

   **The DM's own fix, and the one to use going forward: stop chasing HP upward, and reserve each tool for what it actually solves.**
   - **A genuine solo NAMED individual boss** (a dragon, a lich, a specific unique antagonist with real narrative weight as one person) — HP sized with real margin *plus* **Legendary Resistance/Actions**, so it survives a bad round and gets to act between other turns regardless. This is the only case Legendary Actions belongs in.
   - **Everything else meant to be a serious fight** (not a specific named individual) — **add more enemies, not more HP on one pool.** Multiple targets force the party to split attacks and maneuvers instead of concentrating an entire nova into one HP bar; this is the same fix the group-encounter techniques above already use, now understood to apply to "boss-tier" fights too, not just routine groups. A genuine solo boss and a "serious fight with several targets" are different design choices, not degrees of the same thing — pick deliberately, per encounter, rather than defaulting to solo-and-scale-HP as if it were the only option for anything meant to matter.
   - Run `py .claude/scripts/solo_burst_check.py <campaign> --vs <type> --full-nova` before finalizing a real boss's stats — it prints the martial-PC nova ceiling directly off the character sheets (Action Surge + every Battle Master maneuver die spent), and reminds you to add each caster's actual burst option by hand since spell-slot choice can't be reliably guessed.

   **Default to UNMODIFIED base SRD stats on each enemy when using the multiple-enemy fix — don't inflate their HP too.** Validated same session via two live disposable-test playthroughs (`bug-log.md`, `combat-geometry`): two wraiths at a lightly-raised 80 HP each ran a real, tense 2-round fight; three wraiths at **base SRD 67 HP each, no modification at all** ran an even better one — 4 full rounds, real stakes each round (the party actually got lucky; a slightly different spread of dice and they take real damage), and the DM's own assessment was that it was the more satisfying fight of the two. The practical reasons this is the better default, not just an equally-valid alternative:
   - **Less DM computation per encounter** — stock stat block numbers, no HP math to justify or re-verify later.
   - **A smoother, more natural difficulty curve** — length comes from the party needing multiple rounds to grind down several separate HP pools (each individually vulnerable to a decisive hit, the way a real fight should feel), not from one bloated pool absorbing hits indefinitely.
   - **Enemy count is the tuning dial, not HP.** Want a longer or more dangerous fight? Add another enemy at stock stats rather than inflating the ones already there. Want it shorter? Use fewer.
   - HP inflation is still the right call **only** for the genuine solo-named-boss case above (paired with Legendary Resistance/Actions) — that case has just one HP pool by definition and needs the margin. For every "more enemies" fight, start from unmodified SRD numbers and only raise HP if a specific narrative reason calls for a tougher individual within the group (a sergeant/leader, per the existing group-technique guidance above), not as a default scaling response to party level.

   **Live-improvised SOLO encounters need this too — caught session 9, 2026-08-30 (`bug-log.md`, `combat-geometry`).** A travel-table "Undead" result was built on the spot as a single base-SRD Specter (22 HP) for a level 5 two-PC party — daytime and solo were assumed to make it automatically "light," but nobody actually checked its HP against what this party can do in one round. Kriv's Barrow-King's Blade alone averages 25 damage/round (2 attacks, Extra Attack) — comfortably enough to end a 22 HP target before it ever acted. This is the exact "solo is necessary but not sufficient" failure this section already exists to prevent, just never before applied to a *live-improvised* solo result — the group-spacing technique above got that exact extension on 2026-08-29, the solo-HP-sizing technique never did, until now. **The concrete trigger, going forward**: the instant a travel/random table result or an on-the-spot ruling produces a SOLO enemy, run `py .claude/scripts/solo_burst_check.py <campaign> --check-hp <N>` before finalizing its stats — it reads both PCs' actual Attacks tables and computes a real single-PC damage floor (not a full nova estimate, just "would the strongest PC alone drop this before it acts"), and flags REVIEW if the proposed HP doesn't clear 1.5x that floor. This doesn't replace judgment for real bosses (still use the three-layer treatment above) — it's the minimum floor check for anything, including "just texture," that's going to actually stand and trade blows for at least one round.

3. **Groups need a different fix than solo bosses — HP buffering is the wrong tool here.** The DM asked directly whether routine group encounters got the same reinforcement pass; they hadn't, and they need one, because groups were the *original* and most common victims of the surprise+AoE trap (the goblin band, 4 stirges, the kobold Warren Entrance all died to a single nova before acting). Buffing every mook's HP would just make routine fights slower without making them tenser — the actual fix is preventing one AoE from resolving the whole group at once:
   - **Split into sub-groups by room/area**, already the default in several sites built today (Riverwatch's kobold band, the Sunken Barge's lizardfolk camp, the Gnoll Battlefield, the Feral Menagerie's worg pack) — never let the full count be in one nova's blast radius or one Thunderwave's cube at once.
   - **Even within a sub-group, physically spread the members** so a 15-20 ft AoE can't cleanly catch all of them — 2 gnolls standing 20+ ft apart survive a Fireball's radius better than 2 standing shoulder to shoulder.
   - **Give at least one member of a sub-group a reason not to be surprised** — a sentry with better passive Perception, a creature with keen senses, or simply positioning one member out of the initial ambush's line of sight. A group that's *entirely* surprised is a group that entirely doesn't act; a group with even one alert member returns fire immediately and changes the fight's shape.
   - **A tougher leader/sergeant within an otherwise-normal group** (noticeably more HP than the rank and file, no other mechanical change needed) gives a group fight a "boss" moment even while the mooks still die fast and normally — the Sorrel's Hollow camp's Roskel is the campaign's own proven example of this working.

   **Sweep note**: `the-gnoll-battlefield.md` and `the-feral-menagerie.md` both now have all three group-specific techniques applied — sub-group split, member spacing, and an alert-sentry note (gnolls' and worgs' own keen sense of smell, giving a real chance to notice the party regardless of Stealth). The gnoll pack leader also runs at roughly double normal HP as a real sergeant-tier presence within an otherwise ordinary group fight.

   **Live-improvised encounters need this too, not just prepared files — caught 2026-08-29.** Session 7: a travel-table result ("Concordat party, undead honor guard escort, Dangerous") was improvised live as 6 skeletons + 2 priests (3,600 adjusted XP, ~1.6× Deadly at level 5) and narrated as a standard marching column — clustered, no spacing, no alert exception. The DM caught it before committing: with surprise, a single Fireball plus Kriv's full attack routine would have cleanly resolved most of the group for near-zero risk, the exact trap this file exists to prevent. The three techniques above had only ever been applied to *prepared* encounter files (Gnoll Battlefield, Feral Menagerie) — nothing carried them into on-the-spot improvisation. **The concrete trigger**: the instant a travel/random encounter table result names 3+ enemies and the party currently holds surprise, apply sub-group spacing and consider an alert exception **before** describing enemy positions to the table — not after, since revising positions after the party has already seen a clustered formation and started planning around it isn't a fair mid-course correction.
3. **Spread formations deliberately**, the same lesson already in `combat-rules.md` for escorts — an enemy who's ever heard what this party's spells do (increasingly true in-world, given Sarelle's own post-loss "operational hardening") shouldn't cluster into a novable clump by default.
4. **Vary resistance/immunity against this party's signature damage types** (fire, thunder) often enough that the default nova doesn't always work — forces real tactical decisions instead of a repeatable opener.
5. **When an encounter is built to Deadly on the standard table and the party is likely to get surprise, build past Deadly on purpose**, or split the encounter so surprise can only ever be partial (some enemies alert, some not) — Kargrim's Reach already proved this works.
6. **Vary how fights start.** Not every encounter needs to open with the party scouting unseen and choosing the engagement. Mid-transit reveals, an enemy already braced, or a target who's adapted after a previous loss (Sarelle's convoys are the existing precedent — this should generalize to other repeat threats, not stay unique to her) all deny the free setup that makes the nova-and-done pattern so reliable.

## Building encounters — quick method

1. Pick monsters, sum raw XP
2. Apply multiplier, **then bump one step** for two PCs
3. Compare to the table above
4. Target **Medium** for routine fights, **Hard** for set pieces
5. Reserve **Deadly** for moments the party can see coming and choose to walk into
