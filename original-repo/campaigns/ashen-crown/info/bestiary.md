# Bestiary — what lives where

All entries are SRD monsters (`.claude/dnd-5e-srd/markdown/11 monsters.md`, 130 entries) — look up stat blocks with:

```bash
py .claude/scripts/srd_lookup.py monster "Ghoul"
```

Organized by region so encounters feel like they belong to a place instead of being drawn from a generic bag. **Ash, bone, and cold** are the campaign's signature — necrotic and undead threats should dominate, with living threats used as contrast.

---

## Signature creatures — the campaign's spine

These recur across all tiers and define the setting's feel. Escalate them rather than replacing them.

**Live-improvised encounters must check this table too — caught 2026-08-29.** A session-7 travel encounter defaulted straight to plain Skeletons (Tier 1) for a level-5 party's Concordat patrol, with no check against the party's actual tier — the same live-improv gap `two-player-scaling.md` already documents for group-spacing, just applied to monster *selection* instead of *formation*. Before picking a signature creature for any improvised fight, check this table's Tier column against the party's current level and escalate accordingly — a level-5 party should be seeing Wights/Specters/Ghasts, not still Skeletons, unless there's a specific in-fiction reason (green recruits, a deliberately weak decoy force) to keep it low-tier.

| Creature | Tier | Where it fits |
|----------|------|---------------|
| **Skeletons**, **Zombies** | 1 | Every ash-king site. Cheap, thematic, everywhere. |
| **Ghouls**, **Ghasts** | 1-2 | Ossuaries, crypts, flooded ruins. |
| **Shadows** | 1-2 | The Gallow Tree, places the Crown has touched. |
| **Specters**, **Wights** | 2 | Barrows, chapels, anywhere oaths were sworn. |
| **Wraiths** | 3 | Sundered Reach, the Grey Kingdom. |
| **Mummies** | 3 | Ashvale Necropolis, Bonewrights' Hall. |
| **Liches** | 4 | The Grey Kingdom. What Ilvaneth is asking to become. |

**The ossuary guardian** (Gallowmere, still dormant): built as a **wight** or **mummy** depending on when the party wakes it, with the "sworn to prevent unearned taking" flavor. Scale to the party's level whenever it triggers.

---

## I. The Marches — levels 1-4

**Wilderness**: Wolves, Giant Rats, Stirges, Giant Spiders, Boars
**Roads**: Bandits, Thugs, Scouts (`16 npcs.md`), Goblins
**Water**: Stirges, Crocodiles, Giant Frogs, Lizardfolk (Sunken Barge)
**Ruins**: Kobolds + a Grick (Riverwatch), Skeletons, Shadows (Gallow Tree)
**The Drowned Mill**: Stirge swarm above, 2 Ghouls below
**Sorrel's Hollow**: Bandits, Bandit Captain (Roskel — give him Veteran stats, he's better than his men)
**The Ash-Kilns**: Cultists, Cult Fanatic (Odric Fenn), and something failed in the deepest kiln — a **Ghast** or a botched **Wight**

## II. The Thornlands — levels 3-6

**Wilderness**: Ettercaps, Giant Spiders, Dryad (Weeping Wood), Wereboar (Ostwick), Owlbears
**Ruins**: Specters (Hallowmere Chapel), Animated Armor, Ochre Jelly (Tithe Barn)
**Crypts**: Wights, Ghasts, Gargoyles
**Concordat forces**: Acolytes, Priests, Mages (`16 npcs.md`), escorted by Skeletons and Zombies as honor guard

## III. The Cindermoor — levels 4-8

**Moor**: Will-o'-Wisps, Harpies (the Crags), Hell Hounds (rare, and a bad sign)
**Barrows**: Skeletons, Wights, Specters, and a **Barrow-Wight** boss (Wight with a Ghost's abilities, or a Mummy reskinned)
**The Drowned Cathedral**: Water Elementals, Shambling Mound, Wights, Chuul
**Kesh Deeps**: Duergar, Grick, Rust Monster, Roper (deep)

## IV. Karsgate — levels 5-10

**Urban**: Thugs, Spies, Assassins, Doppelgangers, Wererats in the undercity
**Undercity**: Otyugh, Carrion Crawlers, Gray Ooze, Cloaker (deep)
**Faction muscle**: Veterans, Knights, Gladiators, Mages
**Hidden**: a **Rakshasa** or **Succubus** operating in high society — the city's real secret

## V. The Ashvale — levels 8-10

**Necropolis**: Mummies, Wraiths, Wights in numbers, Flameskulls, Helmed Horrors (Animated Armor upscaled)
**Concordat**: Mages, Archmage (Sarelle), Priests, undead honor guard
**Chalk Warrens**: Otyugh, Carrion Crawlers, Grells, Purple Worm (deep, as a hazard not a fight)
**Compact forces** (if allied): Veterans, Knights, Warmarshal's guard

## VI. Emberhold — levels 11-14

**Court**: Rakshasa, Doppelgangers, Oni, Vampire Spawn and a **Vampire** noble, Succubi
**Streets**: Gangs of Thugs/Assassins, Wererats, Cult Fanatics
**The Hollow Throne**: Wraiths, Specters, and whatever the throne does to those who linger
**Sieges**: Compact and Concordat forces in open conflict — Knights, Veterans, Mages, Golems

## VII. The Sundered Reach — levels 13-17

**Wilds**: Yetis, Winter Wolves, Remorhazes, Rocs, Chimeras, Manticores
**Frostmere**: **Adult White Dragon** + Ice Mephits, Frost-touched undead
**Kar Vaelth**: Fire Giants, Hill Giants, a Stone Giant oracle, Ettins, Trolls
**The Screaming Fen**: Green Hags (a coven), Will-o'-Wisps, Shambling Mounds, Hydras
**Bonewrights' Hall**: Liches (lesser), Wraiths, Mummy Lords, Bone Golems (Flesh Golem reskinned)

## VIII. The Grey Kingdom — levels 17-20

**The Ash Court**: Liches, Wraiths in numbers, Shadow Dragons (Young/Adult Black Dragon with shadow flavor), Death Knights (Knight + Wight abilities, or use a Lich's action economy)
**The Last Ash-King**: Build as a **Lich** with legendary actions and the Crown's own powers layered on. The final antagonist.
**Ambient**: Shadows and Specters as environmental pressure, not encounters — the realm itself drains.

---

## Encounter-building notes

- **Undead are the theme, but undead alone get monotonous.** Break up crypt crawls with living opposition — faction soldiers, rival hunters, beasts.
- **Humanoid enemies should have faces.** The Sorrel's Hollow deserters, Concordat archivists, Choir cultists — these are people with reasons. An evil party benefits from enemies who aren't obviously monsters.
- **Use `16 npcs.md`** for all human opposition; it has Bandit through Archmage.
- **Verify before the fight.** Run `encounter-verifier` or `srd_lookup.py monster "X"` before combat rather than working from memory.
