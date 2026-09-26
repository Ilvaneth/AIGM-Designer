# D&D Skill — Combat Discipline

Load this file the moment combat starts (`combat.py init` is called), alongside `SKILL-scripts.md`. It exists because knowing a rule and applying it under the pressure of a fast-moving fight are two different failure modes — this file fixes the first with reference tables, and the second with concrete, checkable triggers to stop and check at specific moments, not vague vigilance.

**In the same breath as `combat.py init`, also run:**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c <campaign> triggers --all
```
This prints every PC's own `## Combat Triggers` section straight from their character sheet — the mechanical backstop for the "crit/kill bonus action" and similar rules below.

**Then, at the start of EVERY turn — PC *and* NPC, not just once at combat init — run:**
```bash
# a PC's own turn: prints their Combat Triggers + Passive Item Effects
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c <campaign> turn "<PC name>"

# an NPC/monster turn: prints the DEFENSES of the PCs it can act against
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c <campaign> turn "<NPC name>" --targets "<PC>,<PC>"

# --round N on either form restates the narration weight for that round; from round 3 on it
# says so explicitly, because a fight written full-weight in round one thins out by round four.
```
This is a hard gate, not a reminder to remember: it is the *only* sanctioned way a turn begins. Do **not** roll a die, call for a player's roll, or narrate a single action of that turn before it has run.

**Run it on enemy turns too — that half is not optional.** The gate used to be keyed on who *acts*, and printed "no PC triggers to check" on an NPC's turn. But a defensive passive belongs to whoever is *targeted*: a Cloak of Displacement's disadvantage, a damage immunity, a reaction like Riposte or Counterspell all apply on the enemy's turn, and that is exactly where they kept getting missed — in one session the same Cloak was skipped twice after the player had flagged it, because the printed checklist only ever appeared on the wrong turn. `--targets` prints each named PC's `## Defenses` section; with no `--targets` it prints every PC in the campaign.

**Reading it is not applying it.** The output is a checklist to cross-reference against each individual roll *before* you make it: advantage/disadvantage before the attack roll, resistance/immunity/vulnerability before the damage total, a reaction before you move on to the next attack. A multiattack is resolved one attack at a time for this reason — a Cloak that switches off on the first hit cannot be applied correctly to three attacks rolled in one batch.

**Dice ownership (see SKILL.md for the full table).** Every die tied to a player's character — d20 test, initiative, damage and effect dice — is rolled by that player, never by you. You roll NPC and monster dice, and damage arriving at a PC from a trap or hazard. Watch the handoff points inside a single resolution: an NPC attack that triggers a PC's saving throw, and an NPC's failed save that leads into the PC's damage dice, are where a DM-held die most often crosses the line by accident. `dice.py` refuses a PC-owned roll outright — if it stops you, that is the rule working, so ask the player for the number.

---

## Initiative & Surprise

1. **Determine surprise.** A side unaware of the threat is surprised: it cannot take an action or reaction on its first turn, and cannot move either — but it still exists in the initiative order from the start.
2. **Roll initiative for every combatant before anyone acts** — including a surprised combatant, and including a combatant who *readied* an action for this exact moment. Surprise removes a turn's worth of action; it never removes the initiative roll itself, and it never grants the ambusher a free round that happens *before* initiative exists.
   - Wrong: "Surprise round — the ambusher acts, then we roll initiative."
   - Right: roll initiative for everyone, then run round 1 normally, with the surprised side simply passing when their turn comes up.
   - The practical difference matters: if the surprised side would have rolled higher initiative than the ambusher, they still act *before* the ambusher's second action, the moment their own surprised turn passes.
3. **A readied action is the same rule, not an exception.** Readying still happens on the reader's own turn, in the established order; it resolves later as a reaction when the trigger fires. Never resolve a readied (or any declared) attack against a hostile creature before `combat.py init` has been run for the scene — if it hasn't, stop, roll initiative first, then resolve the action at its proper place in the order.
4. **Establish positions before resolving anything with an area or a chase.** Know roughly where each combatant stands and how far apart, *before* rolling an AoE spell or narrating a group splitting up. This prevents two common errors: an escort/formation being treated as spread across an unrealistic distance, and an area spell's actual origin/shape being glossed over (see below).

## Action Economy

| Type | What it covers |
|---|---|
| **Movement** | Up to speed, splittable before/after the action |
| **Action** | Attack, Cast a Spell, Dash, Disengage, Dodge, Help, Hide, Ready, Search, Use an Object |
| **Bonus Action** | Only if a class feature, spell, or item explicitly grants one |
| **Reaction** | Opportunity attack, a few spells (Shield, Counterspell, etc.), a readied action's trigger |
| **Free** | Draw/sheathe a weapon, open an unstuck door, a short sentence |

**A turn is not over until the player says it is.** Resolving one action does not imply the others (bonus action, a second spell, giving a command to a summon) were declined — ask whether they want to do anything else before advancing the turn pointer, and name known once-per-rest resources the character hasn't used yet (Action Surge, an unspent Second Wind, unburned spell slots) rather than waiting for the player to remember them unprompted.

## Attack Resolution

1. Declare target and the specific attack/spell.
2. Roll d20 + modifier vs. target AC (per the dice-ownership rule above — PC rolls their own).
3. Natural 20: always hits, critical (double the *dice*, not flat modifiers, on the damage roll). Natural 1: always misses.
4. On a hit, roll damage dice + modifiers.
5. Spell save DC = 8 + spellcasting modifier + proficiency bonus (already computed on each character sheet — use the sheet's stated DC, don't re-derive it live unless checking for an error).

**A multi-attack turn resolves one hit at a time, never as a pre-committed block.** State the target's remaining HP (or at least "still standing" vs. "looks close to dropping") after each individual attack lands, before rolling or resolving the next one in the same Attack action. The instant a declared target's HP hits 0 with attacks still unresolved, stop — ask where the remainder goes (a different enemy in reach, or explicitly wasted if the player chooses). Never silently mark leftover attacks in a sequence "moot."

**Crit-or-kill bonus actions never offer themselves — check for them.** The moment a melee attack either scores a natural 20 or drops a target to 0 HP, before narrating the kill/crit and moving on, check that attacker's `tracker.py triggers <name>` output (pulled at combat start, per above) for a triggered bonus action — Great Weapon Master's "crit or kill → one more melee attack as a bonus action" is the concrete example this campaign has already needed twice. If one applies, offer it before advancing the turn.

**A retreating or repositioning enemy can provoke an Opportunity Attack — check reach, don't wait to be asked.** Trigger: a hostile creature leaves any PC's reach without taking the Disengage action. The moment a fleeing/repositioning enemy's movement is narrated, check whether it left a PC's melee reach first; if so, offer that PC the reaction before the enemy's move fully resolves.

### Battle Master maneuvers — which die goes where

Not universally in every free SRD dataset, so this table is written down rather than resolved from memory each time. **Every maneuver's own text says whether its superiority die goes to the attack roll, the damage roll, or neither — never both, and never the player's free choice.**

| Maneuver | Die goes to | Effect | Doubles on a crit? |
|---|---|---|---|
| **Precision Attack** | Attack roll | Add the die to the attack roll, before or after the roll (declare before knowing hit/miss) | No — never a damage die |
| **Goading Attack** | Damage roll | Add to damage; target WIS-saves or has disadvantage on attacks against anyone but the maneuver's user until the end of their next turn | Yes — it's a damage die |
| **Distracting Strike** | Neither | On a hit, the next ally's attack against that target has advantage. Die is still spent, adds to no roll | N/A |
| **Bait and Switch** | Neither (AC bonus) | No attack required — swap places with a willing creature within 5 ft; add the die as an AC bonus to either of them until the start of the user's next turn | N/A |
| **Lunging Attack** | Damage roll | +5 ft reach on one melee attack; on a hit, add the die to damage | Yes — it's a damage die |

**For any maneuver not listed here**: read what its own text does with the die — attack roll, damage roll, or a rider effect with no roll at all — and slot it into one of the three columns above before using it, rather than guessing from the name.

**Worked example** (Goading Attack, on a crit): base weapon dice (doubled) + static modifier (never doubled) + superiority die (doubled, since it's a damage die) — e.g. `2d12 + 6 + 2d8`, not `2d12 + 6 + 1d8`.

## Damage & Healing

- **Damage types**: Bludgeoning, Piercing, Slashing, Fire, Cold, Lightning, Thunder, Poison, Acid, Necrotic, Radiant, Force, Psychic.
- **Resistance** halves; **Vulnerability** doubles; **Immunity** zeroes.

**Check the target's resistances/immunities before finalizing ANY damage roll against it — every hit, not just the first one of the fight.** This is the exact mirror of the PC-side discipline above (checking a PC's own Combat Triggers/Passive Item Effects before resolving a roll against them): a monster's defensive traits are just as easy to silently skip, and skipping them just as silently makes a fight easier than it was designed to be — which then gets misdiagnosed as "monsters need to be stronger" when the real fix was to apply what the stat block already grants. Concrete, recurring case: devils (Bone Devils, Erinyes, Pit Fiends, etc.) are immune to fire and poison and resistant to cold and to nonmagical bludgeoning/piercing/slashing — a fire-enchanted weapon's flat fire-damage dice must be dropped from every hit against one, every time, not just noticed after a player flags it.

**`lookup.py` now prints a `-- DEFENSES --` block for every monster**, built from the SRD 5.1 text bundled at `data/srd-5.1-yaml/` (the earlier dataset dropped these fields on import, which is how devils came to take fire damage across two rooms of a dungeon). Read that block before finalizing damage; it lists immunities, resistances, vulnerabilities and condition immunities as the stat block states them.

Two cases still need your own judgement:
- **A custom or reskinned creature** (a "Senior Bone Devil", a homebrew boss) inherits its family's baseline. Look up the base creature and apply its defenses unless the encounter's own notes deliberately change them.
- **`-- DEFENSES: none listed in the dataset --`** means the record carries no defensive line. For a creature whose family has a well-known baseline (devils immune to fire and poison, elementals to their own element, many undead to necrotic), apply that baseline rather than reading the silence as "no resistances", and treat it as a data gap worth reporting.

**Never assume a monster's natural weapons are magical — check the stat block for an explicit trait.** "Attacks are magical" only applies when the stat block says so outright (an Erinyes' "Hellish Weapons," a Pit Fiend's "Magic Weapons"). A Rakshasa's claws, a Bone Devil's sting, a Spinagon's tail — none of these are magical unless stated, so a PC's resistance to nonmagical bludgeoning/piercing/slashing (a Warden's Core, a barbarian's Rage) applies in full against them. This is the mirror-image mistake of the fire-immunity one above: extending a special case (devils-are-usually-dangerous) into a blanket assumption instead of reading the specific trait. When two or more similar-looking fiends appear across a session, re-check each one's own stat block rather than carrying the last one's "magical" ruling forward.

**A PC's own passive resistance/immunity is exactly as easy to skip as a monster's, and just as costly when it's silently missed.** The `tracker.py turn <NPC> --targets` gate prints it every enemy turn for this reason — read the printed Defenses block before finalizing the damage total, not just before the attack roll. A missed resistance under-costs the encounter's real difficulty in the same direction a missed monster resistance over-costs it.

### At 0 HP
1. Falls unconscious and prone.
2. Death saving throws begin on that creature's own turn: d20, no modifiers. 10+ succeeds, 9-or-under fails. Natural 20 regains 1 HP and wakes the creature up. Natural 1 counts as two failures.
3. Three successes stabilizes (unconscious, not dying). Three failures kills.
4. Taking damage while at 0 HP is an automatic failure; a critical hit against them counts as two failures.

### Massive damage
If the damage remaining *after* a hit drops a creature to 0 HP is itself ≥ that creature's max HP, it dies outright instead of starting death saves.

## Concentration

**The instant a concentrating PC takes damage, stop and ask for the check — before resolving the next attack in a multiattack, before moving to the next combatant.** This is not optional bookkeeping to catch up on later; a missed check mid-fight is invisible until someone notices the spell should have ended, at which point the last several turns have to be reconstructed. Trigger: any damage at all, from any source, to a creature concentrating on a spell — including damage from an ally's own AoE, a trap, or a saving throw the creature failed.

- **DC = 10, or half the damage taken, whichever is higher** (round down). State the DC out loud when you ask.
- **This is the PC's own roll** — ask for their raw d20, don't roll it. Apply their CON save bonus and any advantage source (War Caster, Resilient (Constitution)) the same way any other PC roll is resolved.
- **A multiattack resolves one hit at a time for this reason too**: if the first of three attacks against a concentrating PC lands, ask for the concentration check right then — don't wait until all three attacks are rolled and total the damage after the fact. The save might succeed or fail before the remaining attacks even matter to the spell.
- Track what's currently being concentrated on (via `tracker.py concentrate`) the moment it's cast, so the question "does this creature even have a concentration spell active right now" never depends on memory.

## Common Conditions

| Condition | Effect |
|---|---|
| Blinded | Auto-fail sight-based checks; attacks against have advantage, its own attacks have disadvantage |
| Charmed | Can't attack the charmer; charmer has advantage on social checks against it |
| Frightened | Disadvantage on checks/attacks while the fear source is visible; can't willingly move closer to it |
| Grappled | Speed 0; ends if the grappler is incapacitated or something moves the grappled creature out of reach |
| Incapacitated | No actions, no reactions |
| Invisible | Heavily obscured; its attacks have advantage, attacks against it have disadvantage |
| Paralyzed | Incapacitated; auto-fails STR/DEX saves; attacks against have advantage; a hit within 5 ft is a crit |
| Poisoned | Disadvantage on attack rolls and ability checks |
| Prone | Disadvantage on its own attacks; melee attacks against it have advantage, ranged attacks against it have disadvantage; standing costs half movement |
| Restrained | Speed 0; its attacks have disadvantage; attacks against it have advantage; disadvantage on DEX saves |
| Stunned | Incapacitated; auto-fails STR/DEX saves; attacks against have advantage |
| Unconscious | Incapacitated, drops held items, falls prone; auto-fails STR/DEX saves; attacks against have advantage; a hit within 5 ft is a crit |

## Armor and Stealth

Some armor imposes disadvantage on DEX (Stealth) checks — this is a rules-as-written property of the armor itself, not a house rule, and it applies to every wearer, every time, whether or not it's dramatically convenient:

| Armor | Stealth |
|---|---|
| Padded | Disadvantage |
| Leather, Studded Leather | — |
| Hide, Chain Shirt, Scale Mail, Breastplate, Half Plate | — |
| Ring Mail | Disadvantage |
| Chain Mail, Splint, Plate | Disadvantage |

**Before ruling a Stealth check, check the wearer's actual armor and any equipment that overrides the default** (a specific magic armor identified as not imposing it, an item granting advantage that cancels the disadvantage) — read the character's own sheet, don't apply the table from memory alone. When advantage and disadvantage both apply from different sources, they cancel: roll a single die, no re-roll.

## Cover

- **Half cover** — +2 AC, +2 DEX saves (low wall, furniture, another creature).
- **Three-quarters cover** — +5 AC, +5 DEX saves (arrow slit, portcullis).
- **Total cover** — can't be targeted directly.

## Environmental Hazards

- **Difficult terrain**: half movement speed to cross.
- **Falling**: 1d6 bludgeoning per 10 feet fallen, capped at 20d6.
- **Suffocation**: survives (1 + CON modifier) minutes without air, then drops to 0 HP after CON-modifier more rounds (minimum 1).
- **Fire exposure**: typically 1d10 fire per round of contact, may ignite flammable gear.

## Rooms of a designed site — mark as you go

In a designed campaign a site's rooms are tracked by `site_progress.py`, and that record — not memory — is what `load-pack`, `end` and the
validator read. When the party enters a room: `python3 ${CLAUDE_SKILL_DIR}/scripts/site_progress.py -c <name> enter <site id> <room> --day N --session N`;
when it is cleared, `clear`; a room bypassed, `skip … --reason`; a new way through, `shortcut --from --to --how`; a rest inside,
`rest <site> <room> --kind short|long --day N`. The site's overlay status flips to `played` from these marks, never by hand, and the
first `enter` opens the record from the detailed file's room table. Combat in a room that was never marked entered is the sign you
skipped this.

## Before running a deliberately-unfinalized solo boss

See `SKILL-encounter-design.md` for how the fight should have been built in the first place; this section covers tuning one at the table.



Some prepared dungeons leave their final boss's exact HP/Legendary Resistance unset on purpose, to be tuned against the party's real sheet at the time of the fight rather than guessed months in advance. Immediately before that fight:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/burst_check.py --campaign <name> --vs <creature-type-or-keyword> --target-hp <base-HP>
```

This reads every PC's own `## Burst Reference` table (see `templates/character-sheet.md`) and sums the single worst-case round of damage the party can put on one target, then reports whether the boss's base HP survives the opening round. If it doesn't (or barely does), raise HP, add Legendary Resistance, or build in a hard phase/escape trigger before running the fight — don't run the base stat block unmodified just because a source lists it that way.

## Narrating Combat — pacing discipline

**Open every combat, and every new room of one, with a real description before asking for an action.** The room, what the enemies look like, where everyone stands and how far apart — all of it comes *before* "what do you do", not after the player asks for it. A fight that opens on a bare initiative order gives the player nothing to make a decision with.

**Speed never costs description.** "Don't ask, just run it" means skip the confirmations between turns — it does not mean collapsing turns into bare mechanics. Several NPC turns played back to back still get one real sensory sentence each, with the mechanics in their own block afterwards. The pace lives in not stopping to ask; it never lives in dropping the fiction.

**This holds for the whole fight, not just the opening rounds — a long combat is exactly where narration quietly erodes.** A multi-round boss fight that opens with full sensory weight and by round four is down to "Rajah'a vuruyorsun, 30 hasar" has drifted, one small compression at a time, into the failure mode this section exists to prevent — even though every individual message looked reasonable in isolation. When a fight runs long, treat *every* attack — not just the first one against a new enemy — as owed the same one-or-two-sentence beat the opening got: what it looks like landing (or missing), not just what it rolled. If a turn is genuinely trivial (a mook's last gasp, a foregone miss), a single combined line is fine per the rule below — but that's a deliberate call about *that* attack, not a pace creeping downward over the course of the fight.

**Scale the narration to what the fight actually is.** A campaign-defining fight — a chapter's final boss, a named antagonist built up over months, a creature the party has been hunting — is written at full weight from its first round, not after the player asks for more. Deciding how many paragraphs a moment deserves is a judgement you make when the fight starts; the default two-block shape is a floor, not a ceiling.

**Never batch more than one combatant's turn into a single message.** Every turn — PC or NPC, including a surprised combatant's skipped turn — gets its own narrated beat before the next combatant acts, even when Claude is the one rolling for an NPC. Rolling several turns via tool calls and then presenting them as one compressed jump (e.g. straight to "Round 2" with a status summary) is technically accurate but costs the table the experience of watching the fight happen. Before writing any message that shows a round-end status block, count how many turns have passed since the table last saw an update — if it's more than one, split the message.

**The combat tracker (`combat.py`/`tracker.py` state) is the single source of truth for HP, initiative order, and conditions — re-read it before narrating a turn, don't reconstruct it from memory.** Two concrete failure modes this prevents:
- Feeding a monster's *already-damaged* HP back into the tracker as if it were its max HP (re-derive max HP from the stat block, not from the last combat message).
- Re-rolling initiative when the actual intent was only to correct an HP value — a state update should touch only the field that changed.

**Keep a running kill/defeat tally for the encounter, as a structured count, not a narrative impression.** At the end of a multi-wave or reinforcement-heavy fight, XP is calculated from this tally — recounting from memory ("I think it was four") is exactly how a fight ends up under- or mis-reported. Track it the same deliberate way the tracker state itself is tracked.

**Narration comes first, mechanics come after, in two visibly separate blocks — never interleaved.** A hit reported as "24 vs AC21 — hit! [description], 21 damage" puts the mechanics first and the description as an afterthought; that ordering is wrong even when every sensory word is present. The narration block must be readable with zero dice, zero AC, zero damage numbers in it — a pure account of what happened in the fiction — and the mechanical reference sits in its own block immediately after, separated by a visual break (e.g. an em dash `—` on its own line). This applies down to the level of a single attack within a multiattack turn, not just once per combatant-turn — a boss's 3-attack Multiattack gets three narration beats, not one paragraph covering all three followed by three mechanics lines.

**Worked example — NPC multiattack (three attacks, one combatant's turn):**

> Her left claw carves an arc through the air, ice-sheathed fingers catching the light like a scythe at the last moment — it lands on his shoulder plate, the metal cracks with a sound like a scream, and the cold reaches bone instantly.
>
> The right claw follows through the gap the first one opened — this time it finds flesh instead of armour, tearing along his side; the hot blood starts freezing the moment it meets her touch.
>
> And then her hand reaches for his chest almost *gently*, with a healer's reflex three hundred years out of date. He slides back a step and the touch closes on empty air.
>
> **—**
> Frost Claw 1: 24 vs AC21 — hit, 21 damage.
> Frost Claw 2: 30 vs AC21 — hit, 21 damage.
> Harrow Touch: 14 vs AC21 — miss.
> Kriv: 143 → 101/143 HP.

**Worked example — PC attack (one hit):**

> The blade seats itself in the crack running down the golem's chest — radiant light bleeds out through the stone, blinding for a heartbeat, and the crack widens until a slab of it shears off and hits the floor.
>
> **—**
> Attack: 27 vs AC18 — hit. Damage: 1d12(6)+1d8(3)+STR9+GWM10 = 35.

The player must always be able to reconstruct the real HP/position/resource state from the mechanics block alone — the narration block's job is purely to make the moment land, never to carry information the mechanics block doesn't also state plainly. A trivial/low-stakes hit (one of a rolled group of random mooks, say) can collapse both blocks into a single line if the table's pace calls for it — but a boss, a PC, or any narratively significant moment keeps the two-block separation every time.
