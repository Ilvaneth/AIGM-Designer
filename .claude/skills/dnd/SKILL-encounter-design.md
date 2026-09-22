# D&D Skill — Encounter Design

Read this when building any encounter that is not random texture: a set piece, a mini-boss, a faction leader, a chapter finale. It exists because "the fight was too easy" is almost never solved by adding monsters or raising CR — the causes are structural, and each has its own fix.

The diagnosis this file is built on came from a party of two at high level, but nothing in it is specific to that table. A party that opens with surprise, concentrates its damage into one round, and neutralises incoming attack rolls will flatten an encounter built to its CR budget, whatever the party size.

## Why a correctly-built fight still collapses

1. **Surprise is achieved almost every time.** Scouting, stealth and disguise are repeatable, and a party that has drilled them will keep winning the first round before it starts.
2. **One character's alpha strike ends the fight.** Extra Attack plus a damage feat plus a bonus-action trigger chains into a single round far above the DPR the encounter maths assumes.
3. **Attack rolls against the party mostly miss.** One item or spell that imposes disadvantage on attack rolls (a displacement effect, blur, heavy cover) turns most incoming attacks into nothing.

Together these end a fight in round one or two with the party barely scratched — regardless of how many monsters were in the room.

## The boss-tier checklist — all of it, every time

For a boss, mini-boss or narratively significant set piece, none of these is optional.

1. **Size HP for multiple rounds, not for round one.** Take the party's realistic opening burst (`burst_check.py` reports it from the sheets) and add two rounds of sustained DPR on top. A boss that survives the alpha strike but dies in round two produced the same anticlimax.
2. **Give every boss a resistance profile by default.** Not occasionally — by default, and justified in the fiction: an armoured horror resistant to physical damage and weak to force; an undead resistant to necrotic and weak to radiant. This halves the nova and gives the party a real tactical question (find the right weapon) instead of repeating the same opening.
3. **Protect the boss with terrain or position.** At least one of: it cannot be targeted until a condition is met (a ward broken, a channel cut), physical obstacles that break line of sight or movement, or a mobility tool of its own (teleport, flight, phase). A boss that stands at the same range for three rounds eats the full nova every round.
4. **Spend the party's resources before the boss room.** If they arrive at 100% — every slot, every once-per-rest feature ready — no HP total will save the fight. Every boss encounter gets at least one real resource-draining obstacle, trap or skirmish immediately before it.
5. **Support creatures need real HP and AC.** A crit-or-kill bonus-action chain turns one-hit mooks into free extra attacks on the way to the boss. Anything guarding the boss must survive a hit.
6. **Answer the attack-roll shutdown directly.** Include effects that never make an attack roll: save-based area spells, grapple, restrain, silence. At least one enemy per significant fight should be able to threaten the character who is hardest to hit with attacks.
7. **Use Legendary Resistance and Legendary Actions — knowing what they do.** Legendary Resistance answers a control nova (save-or-suck), not a damage nova; it does nothing about raw damage. Legendary Actions matter more: acting outside the initiative order is what breaks the one-round clear.
8. **Consider a second wave.** Once the surprise and the alpha strike are spent, a second wave arriving on a timer (noise, an alarm, a patrol) is a genuine fight, because the party is now spending what it has left.

## Enemy itemisation

A long-running party fights with a full set of attuned, optimised gear while the creatures they face are plain stat blocks. The CR maths assumes an unequipped party on both sides, which widens the gap every time the party levels or loots. So:

1. **A signature weapon.** A boss carries a magic weapon that makes its damage a real threat — the mirror of what the party's own best weapon does to it.
2. **A defensive item.** Carry the resistance profile from point 2 above on a concrete object — an amulet, a cloak, a core — rather than an abstract stat line.
3. **No extra subsystem.** These items work normally during the fight. When the boss dies they become loot, and its power goes with them.
4. **A self-feeding reward loop.** The party that beats a hard boss takes its signature item and gets stronger; the next boss is designed against that stronger party. Enemy power tracks party power instead of standing still.
5. **Support creatures are a separate economy.** They are mechanically heavy (real HP and AC, per point 5 above) but drop **nothing**. Only the boss's own items are the reward; support creatures are an action-economy layer, not a loot layer.

## How much to apply — not every fight is a boss

| Encounter type | What to apply |
|---|---|
| Random / texture (travel table, minor threat) | Usually nothing — these are meant to be light |
| Standard dungeon room | One or two points (often awareness and an anchor enemy) |
| Significant set piece (a thread's real fight) | Three or four points |
| Faction leader / boss-tier confrontation | All of it, plus the itemisation section |

## Two more levers

**Awareness — surprise is not guaranteed.** The default assumption for a known party is that intelligent enemies prepare for them. When building an encounter, ask whether this enemy or location would realistically expect the party's repeated tactic (a quiet approach, a disguise, a night raid). If so: real guard rotations, an alarm ward, or simply part of the force staying unsurprised while the rest is caught out.

**An anchor enemy.** Every non-random encounter wants at least one combatant who can take the party's realistic alpha strike and still act — through HP, AC, resistance, or all three. The goal is modest and specific: at least one enemy still moving in round two.

## What this is not

This is not a list for punishing players. The aim is for the surprise-plus-alpha-strike strategy to be genuinely tested *sometimes*, not always. A party that scouts well, picks the right target and plays smart should still be rewarded for it — what this doctrine removes is the feeling that the fight was won before initiative was rolled.

## Reoccupying cleared dungeons

A cleared dungeon does not have to stay empty. When a new occupant is chosen from an active thread rather than at random, it answers "why is something here now" in the same move, and gives a live storyline a concrete place to happen. The reward problem is smaller than it looks: a new occupant brings its own treasure rather than repeating the old loot, and most dungeons were never explored to completion anyway.

**Delivery rule — never forced.** A reoccupation surfaces the way anything else does: a faction move, a rumour an NPC mentions, a travel encounter, or a discovery made while chasing something else. Never announce that the party is going back to a location. They choose the direction; your job is only to make sure the world contains the possibility.
