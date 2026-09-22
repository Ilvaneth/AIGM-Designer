# The Maker's Undoing

**Region**: III. The Cindermoor
**Level range**: 5-7 — internal escalation curve, not a flat band. Wing 1 (The Broken Approach) calibrated for ~level 5, Wing 2 (The Discarded Works) for ~level 6, Wing 3 (The Sealed Collection) for ~level 7. Built and numbered 2026-09-01, session 11, collaboratively with the DM — never played.
**Site type**: Full dungeon, built to `.claude/rules/dungeon-design.md`'s standard
**Location class**: Dungeon
**Dungeon Type**: **Planned Dungeon → Vault** (per `dungeon-design.md`'s Phase 0 DMG taxonomy) — built deliberately, for a purpose, by a single architect
**Payoff type**: **Treasure-heavy** — Marek Stillwright's own masterwork and the undelivered commissions he never returned

**⚠ Two-character party check** (`two-player-scaling.md`): Rooms 9, 10, and 15 are genuinely Deadly-tier for a two-person party — see each room's math below. This is intentional (the wing's own climax fights), not an oversight, but the DM should re-run `py .claude/scripts/encounter_difficulty_check.py ashen-crown --raw-xp <N> --count <N>` against the party's actual level before running any of them, and re-check `py .claude/scripts/solo_burst_check.py ashen-crown --vs construct --full-nova` before the Room 20 Clay Golem fight specifically — its exact HP/Legendary Resistance adjustment was deliberately left for that check, run fresh against the party's real sheet at the time, rather than locked in now against level-5 numbers that will be stale by the time this site is actually reached.

**Standalone, faction-free** — per `dm-notes.md`'s standing rule that at least one site should owe nothing to the plot. No connection to the Concordat, Compact, Choir, or either PC's personal thread.

---

## Phase 1 — Concept & ecology

**What it was**: A private vault, carved into a Cindermoor mountainside by **Marek Stillwright**, a solitary artificer-wizard obsessed with magic item crafting. Not a guild, not a noble house — one man's life's work, hidden from everyone, including the clients who paid him.

**What happened to him**: Killed by his own final creation — the clay guardian in the deepest chamber (Room 20) — in an accident or a genuine malfunction nobody survived to explain. The golem has had no one to answer to since, and has simply kept doing the only thing it was ever told to do: guard.

**Who/what is here now** — three distinct layers, each with its own logic:
- **The beasts** (Wing 1): opportunistic wildlife that found their way in through a breach in the original entrance long after Marek's death. They have no idea what the mountain used to be. **Ecology note, confirmed with the DM**: Griffons and Manticores are both apex predators and would not naturally share overlapping territory — the fix is vertical stratification. The Griffon (Room 5) nests and hunts high, on exposed ledges and open air; the Manticores (Rooms 9-10) claim the deep ground tunnels. Their hunting grounds never cross. Cockatrices (Room 3) are small opportunists near the breach, low enough in the food chain that neither apex predator bothers with them.
- **The failures** (Wing 2): Marek's own earlier, lesser, and ultimately discarded creations — Gargoyles, reskinned in play as "failed golem attempts," stone-and-metal bodies that never worked right and were simply left where they stopped moving, until something (residual animating magic, or simple malfunction) set them stirring again.
- **The guardian** (Wing 3): the Clay Golem, Marek's actual masterwork and the reason he's dead. It has never left the innermost chamber. It does not know its maker is gone.

## Phase 2 — Map (non-linear)

**Two entrances**: the natural **Cave Mouth** (Room 1) — the breach the beasts use, obvious and watched by nothing in particular — and Marek's own **Hidden Path** (Room 16), a warded personal door connecting directly from outside the mountain into the threshold of Wing 3. A party that finds the hidden door first can bypass Wings 1 and 2 entirely — a real, viable shortcut, not a trap dressed as one.

**Verticality**: implicit throughout — Wing 1's rooms range from ground-level tunnels to the Griffon's high ledge (Room 5); Wing 2 is Marek's actual workshop level, roughly level with the mountain's core; Wing 3 is the deepest, coldest, most deliberately built section.

**Loop**: the Hidden Path (Room 16) functions as the loop point — it connects the surface directly to the deep interior, so a party that explored Wings 1-2 fully and a party that used the shortcut both arrive at the same place, just by different costs paid.

## Phase 3 — Room by room

Status column: mark `✅ RESOLVED (session N, day D)` as each room is actually played, per `dungeon-design.md`'s standing rule — this file starts with nothing marked, since it has never been run.

### Wing 1 — The Broken Approach (10 rooms, ~level 5, escalating)

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 1 | **Cave Mouth** | Main entrance — the breach the beasts use. Obvious, unguarded by anything intelligent. | Entrance | — |
| 2 | **Bone Midden** | **1 Cockatrice** (CR 1/2, 100 XP), an outlying member of Room 3's colony, nesting among old bones and the beasts' leftovers. 100 → ×1.5 (2-PC bump, solo) = **150 adjusted, trivial** — a light opener, not the real fight. **Resonance key 1** is here, half-buried, along with the first fragment of Marek's journal (weather-damaged, still legible with a DC 12 Investigation check). | Combat | ✅ RESOLVED (session 12, day 57) — Cockatrice killed (ambushed a rival relic-hunter first, party intervened; Kriv took her surface map before letting her flee). Resonance key 1 + journal fragment 1 found (Investigation 20 vs DC 12). |
| 3 | **The Nesting Cave** | **2 Cockatrice** (CR 1/2, 100 XP each). 200 raw → ×1.5 (2 monsters) → ×2 (2-PC bump) = **400 adjusted, Easy** at level 5. | Combat | ✅ RESOLVED (session 12, day 57) — both killed, one to Fireball, one to Kriv |
| 4 | **Old Stair** | **Trap — rockslide.** Perception DC 13 to notice loose stonework; Dexterity save DC 13, 2d10 bludgeoning on a fail, half on a success. A straightforward mundane hazard, not Marek's work — just erosion. | Trap | ✅ RESOLVED (session 12, day 57) — spotted via passive Perception (Ilvaneth, 15), avoided entirely, never triggered |
| 5 | **The High Ledge** | **1 Griffon** (CR 2, 450 XP). 450 → ×1.5 (2-PC bump, solo) = **675 adjusted, Easy-Medium** at level 5. Nests high; the fight has real vertical positioning if the party lets it. | Combat | ✅ RESOLVED (session 12, day 57) — killed round 1, Scorching Ray (22) + Kriv's crit Goading Attack + follow-up (49) |
| 6 | **Broken Gate** | **2 Cockatrice** (CR 1/2, 100 XP each), the colony's edge, nesting in the gate's warped frame. 200 raw → ×1.5 (2 monsters) → ×2 (2-PC bump) = **400 adjusted, Easy**. The vault's original outer door, breached and warped — this is where the mountain stopped being "wild cave" and started being "built." **Resonance key 2** is set into the door's own dead locking mechanism, along with a second journal fragment (DC 12 Investigation). | Combat | ✅ RESOLVED (session 12, day 57) — both Cockatrice killed by end of round 2 (Wand of Magic Missiles + Shocking Grasp + Kriv's attacks/opportunity attack). Resonance Key 2 + Journal Fragment 2 found and read (Investigation 23 vs DC 12). |
| 7 | **Ambush Floor** | **2 Mimic** (CR 2, 450 XP each), disguised as abandoned crates and a chest. 900 raw → ×2 (3-6 count band... actually 2 monsters → ×1.5) → ×2 (2-PC bump) = **1,800 adjusted, Hard** at level 5. | Combat | ✅ RESOLVED (session 13, day 57) — Ilvaneth found the chest's "too clean" tell (Investigation 19), ruled out magic (Arcana 27), tested it with Mage Hand — Mimic A revealed and killed round 1 (Scorching Ray 21 + Kriv's Goading Attack/2nd attack 37). Mimic B found by systematically Mage Hand/sword-testing the remaining 5 crates, killed by Kriv (Action Surge, 52 dmg then finishing blow). No party damage taken. 900 XP total, 18 gp + an unidentified tarnished signet ring found among the remains. See `encounters/makers-undoing-room7-ambush-floor.md` |
| 8 | **Ward Remnant** | **1 Cockatrice** (CR 1/2, 100 XP), drawn to the residual warmth of a dead containment ward, still faintly discharging. 100 → ×1.5 (2-PC bump, solo) = **150 adjusted, trivial**. Investigation DC 14 identifies the ward as arcane residue, not natural — the first sign this cave was never fully wild. (Reworked from a pure trap 2026-09-02, per the DMG content-ratio fix below — the ward itself no longer deals damage on its own.) | Combat | ✅ RESOLVED (session 13, day 57) — full surprise (both PCs beat passive Perception 11), killed round 1 (Fire Bolt 12 + Kriv's two attacks for 20). No party damage. 100 XP total. The ward itself not yet investigated (DC 14 Investigation) |
| 9 | **Beast Den** | **2 Manticore** (CR 3, 700 XP each) — the pack's core territory. 1,400 raw → ×1.5 (2 monsters) → ×2 (2-PC bump) = **2,800 adjusted, Deadly** at level 5-6. | Combat | ⚠️ PARTIALLY RESOLVED (session 13, day 57) — full surprise achieved, Manticore B killed round 1-2 (crit-heavy opening). Manticore A fought to 8/68 HP then fled Disengage into an unlit side passage, whereabouts unknown — **not killed, a live loose end**. Kriv took 7 damage (the party's first hit of the night). 1,400 XP awarded (full encounter credit). Room not yet searched for the den's own loot |
| 10 | **The Gauntlet** | **2 Manticore, one an alpha** (bonus HP, no new statblock needed) — the wing's climax. Same math as Room 9, **~2,800 adjusted, Deadly** — harder through narrative weight (the pack's leader) and accumulated party attrition, not raw numbers stacked on top of an already-Deadly fight. | Combat | ✅ RESOLVED (session 13, day 57) — Room 9's wounded survivor warned this pair, denying surprise (a direct consequence of not pursuing it). Ilvaneth's Fireball caught both for 35 each; Kriv's natural-20 Action Surge round (49 dmg) killed the Alpha outright. Second Manticore killed round 2. Kriv took 10 more damage (47/64 by fight's end). 1,400 XP awarded |

### Wing 2 — The Discarded Works (5 rooms, ~level 6)

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 11 | **Failures** | **1 Gargoyle** (CR 2, 450 XP), reskinned as a failed golem attempt. 450 → ×1.5 (2-PC bump) = **675 adjusted**, Easy-Medium at level 6 — the wing's own opener. | Combat | ✅ RESOLVED (session 13, day 57) — the party's own unstealthy search let the Gargoyle notice first; it ambushed them (party surprised), but only landed one hit before dying to Kriv's crit + Ilvaneth's advantage-boosted Fire Bolt. 450 XP. Found 16 gp in workshop scrap and a torn note in Marek's hand ("third attempt failed too... the core is too weak, or I'm looking for the wrong thing") |
| 12 | **Testing Hall** | **Trap — Marek's own mechanical trigger**, a leftover test rig. Perception DC 14; Dexterity save DC 14, 3d10 piercing (spring-loaded blades) on a fail, half on success. | Trap | — |
| 13 | **Sanctuary** | Marek's own working-ward, still active — a genuinely safe rest point. No combat, no trap. A long rest taken here is real and earned. | Sanctuary | — |
| 14 | **Components** | **Trap — pressure-plate alarm.** Investigation DC 15; Dexterity save DC 15, 2d10 poison (gas) on a fail, half on success. **If triggered, it alerts Room 15** — the Gargoyles there arrive already aware, no surprise round for the party. Also where the raw crafting-material treasure and **Resonance key 3** are found (with a third journal fragment, DC 13 Investigation). | Trap | ✅ RESOLVED (session 13, day 57) — trap spotted via passive Investigation (Ilvaneth, 17), avoided entirely, never triggered. Resonance Key 3 + Journal Fragment 3 found (Investigation 20, Kriv's help) — **all three keys now in hand, Room 18's Calibration puzzle is solvable**. 38 gp in raw crafting materials also found |
| 15 | **Forge Floor** | **2 Gargoyle** (CR 2, 450 XP each), the wing's real set-piece. 900 raw → ×1.5 (2 monsters) → ×2 (2-PC bump) = **1,800 adjusted, Hard** at level 6. | Combat | ✅ RESOLVED (session 13, day 57) — full surprise (both PCs beat passive Perception 10), both Gargoyles killed within 2 rounds, zero party damage. 900 XP — **Ilvaneth reached level 6** from this fight |

### Wing 3 — The Sealed Collection (5 rooms, ~level 7)

| # | Room | Content | Category | Status |
|---|------|---------|----------|--------|
| 16 | **Hidden Path** | Marek's own secret entrance terminates here — the loop connecting straight from outside the mountain, bypassing Wings 1-2 entirely for a party that finds it first. | Entrance | — |
| 17 | **Wardway** | **Trap — Marek's most advanced personal defense**, born of his own paranoia. Investigation DC 16; Dexterity save DC 16, 4d10 force damage on a fail, half on success. The hardest trap in the site. | Trap | ✅ RESOLVED (session 13, day 57) — triggered safely by an Animate Dead zombie sent ahead as a proxy (DEX save 11 vs DC 16, failed, 20 force damage, zombie survived at 8/28 HP). No party risk |
| 18 | **Calibration** | **Puzzle.** The three Resonance Keys (Rooms 2, 6, 14), read together with their journal fragments, give the correct sequence to assemble into the door mechanism here — solving it is inseparable from having actually read Marek's own story. No keys, no journal fragments read = no solve; the puzzle cannot be brute-forced. | Puzzle | — |
| 19 | **Commissions** | **Treasure — the undelivered work.** A pair of linked communication stones (both here; the intended recipient's name is recorded in Marek's own commission ledger, a real future hook), a dangerous prototype weapon Marek refused to deliver, and a wand/staff commissioned by an independent wizard who died or vanished before collecting it. | Treasure | ✅ RESOLVED (session 13, day 57) — all three unclaimed commissions taken (communication stones addressed to a Karsgate trading house/"V. Marrow," a life-draining prototype shortsword, an unclaimed staff), none yet Identified (needs a 100 gp pearl). Commission ledger also found — an unfinished "Doran Calvane" order, and a worn note on outside funding for "the Golem project" from an illegible Karsgate name |
| 20 | **The Vault** | **Boss fight — Clay Golem** (SRD base, CR 9). **Do not run at base stats** — re-check `solo_burst_check.py --vs construct --full-nova` against the party's real sheet at the time of the fight; expect to add HP margin and Legendary Resistance per `two-player-scaling.md`'s solo-named-boss methodology, since this is exactly that case (a genuine solo individual with real narrative weight). **Treasure**: Ring of Mind Shielding (Marek's own masterwork) + ~400-600 gp (the commission clients' unreturned advance payments, scattered through the room). | Combat | ✅ RESOLVED (session 13, day 57) — reinforced to 190 HP (base 133 + margin above the party's 139.5 combined nova ceiling at level 6). Destroyed in 3 rounds — Kriv's Precision Attack+GWM combo (81 dmg round 1), Ilvaneth's wand/Scorching Ray, no PC damage taken. One of two Animate Dead zombie thralls (Nessa Wren) destroyed by the Golem's Berserk trigger; the other (Perrine Oskold) survived with max HP permanently reduced to 8. 5,000 XP, Ring of Mind Shielding + 568 gp recovered. **The Maker's Undoing is now fully cleared** (Wing 1's escaped Manticore A excepted) |

## Phase 4 — Content variety check

**Room-content ratio, checked against the DMG stocking percentages** (`dungeon-design.md`'s Phase 3 standing rule, added 2026-09-02 after this file's first draft came in at 15% combat — a real arithmetic miss, not a taste call): Combat 11/20 (**55%**, target 50-60% ✓), Trap 4/20 (**20%**, target 10-15% — deliberately above, Marek's own artifice theme, stated reason kept from the original build), Lore/structural 2/20 (**10%**, target 15-20% for "dressed-empty" rooms — Rooms 1 and 16 only, both genuinely structural), Special/puzzle/treasure/sanctuary 3/20 (**15%**, target 10-15% ✓).

- **Combat**: 11 rooms (2, 3, 5, 6, 7, 8, 9, 10, 11, 15, 20) — Cockatrice (×4 across the colony in Rooms 2/3/6/8), Griffon, Mimic, Manticore ×2, Gargoyle ×2, Clay Golem. None reused from elsewhere in this campaign except Gargoyle/Clay Golem, both otherwise-unused. Rooms 2, 6, and 8 were reworked 2026-09-02 from pure lore/trap into light combat-plus-lore/trap rooms specifically to close the ratio gap — each keeps its original non-combat content (keys, journal fragments) alongside a trivial-tier Cockatrice, smoothing Wing 1's pacing with real breathers between the escalating set-pieces (Rooms 3/5/7/9/10) rather than flattening the curve.
- **Hazard/trap**: 4 rooms (4, 12, 14, 17) — DCs escalate 13 → 14 → 15 → 16 alongside the dungeon's own level curve. Room 14's trap has a real tactical consequence if triggered (alerts Room 15). Room 8 is no longer a pure trap (see Combat above) — its Investigation DC 14 now only identifies the residue as arcane, no independent damage roll.
- **Puzzle/exploration**: Room 18 (Calibration) — solvable only by having engaged with Rooms 2, 6, and 14's lore content first, per this file's own design principle that a Vault's exploration rooms are never optional connective tissue when the payoff is Treasure-heavy and the puzzle is story-gated.
- **Treasure**: Room 19 (Commissions) + Room 20 (Ring of Mind Shielding, gp). Every commissioned item has a named, currently-unknown client — a real future hook, not decoration.

## Running this well

**Resting pressure**: genuine only across Wing 1 and the start of Wing 2 — the Sanctuary (Room 13) is a real, earned reset point roughly at the dungeon's midpoint, not a free pass at the start. After Room 13, treat the rest of the delve (Rooms 14-20) as a single resource-attrition push toward the Golem.

**Trap escalation is deliberate** — DC 13 at the entrance, DC 16 at the deepest point, tracking the same 5→7 level curve as the combat encounters. Never apply a flat DC across the whole site.

**The puzzle is the site's real spine** — per this file's Payoff type (Treasure-heavy, not Strategic-info), the point isn't that the lore is the reward, it's that skipping it makes the actual reward (Room 19's items, Room 20's Golem fight avoidable/easier if the command-word angle is ever explored — DM's discretion, not built into this version) unreachable. Don't let a party bypass Rooms 2/6/14 and then hand them the solve anyway.

## Connections

- `gazetteer.md` — Region III, the Cindermoor
- `two-player-scaling.md` — every combat room's math above was computed directly against this file's tables; re-verify before running if the party's level or size changes
- `items-and-loot.md` — Room 20's ~400-600 gp sits within the CR 5-10 treasure band (100-1,000 gp) this file specifies
- `dungeon-design.md` — built to this file's Phase 0-4 standard from the start, including its Payoff-type rule (2026-09-01 addition) and the Room-by-room resolution-tracking convention
