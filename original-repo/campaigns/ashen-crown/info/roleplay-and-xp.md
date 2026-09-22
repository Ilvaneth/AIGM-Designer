# Roleplay, Rewards, and When the DM Speaks Up

The campaign now runs on transformation — both PCs pay escalating costs (`ascension-tracks.md`) and both change over twenty levels. That makes roleplay load-bearing, so it needs rules.

---

## The core distinction

**The DM enforces mechanics, not personalities.**

A player owns their character. The DM does not get to rule on whether someone understands their own creation. But when an ascension cost is active, that is a *condition*, not an opinion — and the DM enforces it exactly like poison or exhaustion.

### Wrong

> "Kriv wouldn't give that away."

### Right

> "Kriv reaches out to hand over the purse — and his hand doesn't open. Roll a WIS save, DC 12."

The player keeps the intent. The transformation decides the outcome. Nobody gets told they're playing wrong.

---

## The DM does not flag roleplay at all

**Decided at the table (2026-08-24): no pre-declared red lines.** Character boundaries emerge through play, not from a form filled in beforehand. The players do not hand over a list of "things my character would never do," and the DM never rules on whether an action fits a character.

The DM's position is simple: **there is no such thing as playing your character wrong.** Not flagged, not questioned, not penalized, not even asked about.

The single exception is mechanical, and it isn't a judgement: when an ascension cost is active, the DM enforces it as a *condition*, in-fiction, with dice. "Kriv reaches for the purse and his hand doesn't open, roll WIS" is the world pushing back, not an opinion about Kriv.

### The oath belongs to the players

The bond between Ilvaneth and Kriv — never lie to each other, never betray each other — is established fiction, not a DM-enforced rule. If a player chooses to break it, that is a story event, not an error. Play the consequences; don't editorialize.

### Characters are supposed to change

This campaign is about becoming something else. "Your character wouldn't do that" is always the wrong call here — what looks like a slip may be the transformation working. The DM's job is to make the world respond, never to referee anyone's reading of their own character.

---

## XP for roleplay

**No XP is ever withheld as punishment.** Withholding is a penalty on the player, not the character, and it teaches people to play safe. Everything below is additive.

### What earns it

| Trigger | Why it's rewarded |
|---------|-------------------|
| **Playing a cost against your own interest** | The single most important one. Kriv refusing to sell something when selling is obviously smart. Ilvaneth crossing off a memory and playing the hole it leaves. This is what makes the ascension design work at all. |
| **Playing Neutral Evil honestly** | Ambition, pragmatism, ruthlessness — including the ugly choices. The refugee con was *correct play*. Never award less for a cruel solution than a kind one; this party isn't kind. |
| **Honouring the bond when it costs something** | Telling each other the truth when a lie would be easier and safer. |
| **Resolving a situation without combat** | Bribed, bluffed, avoided, turned. Already policy in `progression.md` — full encounter XP, no discount. |
| **Making the world real** | Using an NPC's actual agenda, remembering a promise, acting on something learned three sessions ago. |

### How much

Per instance, **maximum 3 per character per session**. Calibrated per level so the reward stays worth about **9-10% of a level** at the cap — meaningful at every tier, never overtaking adventuring.

**Award it with `py .claude/scripts/award_rp_xp.py ashen-crown <character> <session> "<reason>"`** — not by hand-counting rows in the Award log below. The script reads the character's current level, looks up the correct per-instance value from the table, counts existing awards for that character in that session (a "Both" row counts toward each character), and **refuses outright (exit 1, nothing written) if the cap is already hit** — it does not just warn and proceed. Built 2026-08-25 after the DM asked for a hard-enforced cap rather than something tracked by memory; see `system-register.md`. Use `--check` in place of a reason to see the current count without awarding anything.

| Level | XP to next | **Per instance** | Cap (×3) |
|-------|-----------|------------------|----------|
| 1 | 300 | **10** | 30 |
| 2 | 600 | **20** | 60 |
| 3 | 1,800 | **50** | 150 |
| 4 | 3,800 | **125** | 375 |
| 5 | 7,500 | **225** | 675 |
| 6 | 9,000 | **275** | 825 |
| 7 | 11,000 | **325** | 975 |
| 8 | 14,000 | **425** | 1,275 |
| 9 | 16,000 | **475** | 1,425 |
| 10 | 21,000 | **650** | 1,950 |
| 11 | 15,000 | **450** | 1,350 |
| 12-13 | 20,000 | **600** | 1,800 |
| 14 | 25,000 | **750** | 2,250 |
| 15-16 | 30,000 | **900** | 2,700 |
| 17-18 | 40,000 | **1,200** | 3,600 |
| 19 | 50,000 | **1,500** | 4,500 |

> **Why per-level instead of per-tier.** The original version used four flat tier values (25/100/400/1000). Testing showed that swung between **25% of a level at level 1 and 1.4% at level 10** — because XP requirements grow steeply inside a tier while a flat award doesn't. This table is derived from each level's actual gap, so it can't decay.

### Inspiration — use it, it's free

Award **Inspiration** in the moment, at the table, whenever a player plays a cost or a bond well. It's immediate, tactile, and 5e already includes it. Inspiration in the moment, XP at session end. Both, not either.

---

## The specific thing to watch for in this campaign

The ascension costs will get skipped. That is the failure mode.

Powers are fun to hand out and costs are awkward to enforce, so they quietly stop happening, and within three sessions the tracks are a superpower buffet with no spine. **Check every session**: did Kriv's hoard-sense come up? Did Ilvaneth lose anything?

**Keep the memory list written down at the table.** Ilvaneth's losses are meant to be *visible* and *accumulating*. A list the player can look at and count is worth more than any amount of description.

And when the memories start coming from the orphanage — say the specific memory out loud. Name what she's losing. Let Kriv's player hear it.

---

## Award log

| Session | Character | For | XP |
|---------|-----------|-----|-----|
| 2 | Ilvaneth | Conning the Wend family — Neutral Evil played straight, with a plan and a story | 25 |
| 2 | Ilvaneth | Ash on the ward plate — solved the seal from an in-fiction clue, no combat | 25 |
| 2 | Kriv | Backing the con without hesitation; the bond played as reflex | 25 |
| 2 | Both | Comprehend Languages on the inscription — prepared a spell for a purpose, then used it | 25 each |
| 2 | Kriv | Kept his word to Hesta and followed through on the deal, straight, no shortcuts | 20 |
| 5 | Ilvaneth | Turning Odric Fenn through the Venn-threat leverage and calculated vulnerability about the Warden — masterful Neutral Evil manipulation, resolved a Hard encounter without a single blow | 125 |
| 5 | Kriv | Converting Sergeant Dallin Marsh's debt into personal loyalty — turning a collection job into a garrison asset, ambitious Neutral Evil power-base building | 125 |
| 5 | Ilvaneth | A genuinely vulnerable, honest confession of loneliness to the Widow — real personal cost paid as the bargain, not performance | 125 |
| 14 | Kriv | Cold-blooded execution of a surrendered enemy — honest Neutral Evil, no hesitation, in-character mockery of mercy ('Yüce Büyücü seni zombisi yapacak') | 275 |
| 17 | Ilvaneth | Private planning scene at the inn — genuine Neutral Evil ambition (turning Kell's own soldiers to butcher him in his own garrison) and the bond between them plotting together, no audience, no performance | 325 |
| 17 | Kriv | Private planning scene at the inn — genuine Neutral Evil ambition (turning Kell's own soldiers to butcher him in his own garrison) and the bond between them plotting together, no audience, no performance | 325 |
| 17 | Ilvaneth | Publicly named Kriv as Lord Shestendeliath before the whole assembled household — a real, irreversible commitment, genuine warmth for the family they're building, honest Neutral Evil ambition made real | 325 |
| 17 | Kriv | The house is publicly reborn — his name spoken aloud by 33+ people who now belong to it, the culmination of the whole restoration arc | 325 |
| 19 | Ilvaneth | Ash-offering at Cair Dunnow's Old Hearth-Shrine — sacrificed her own kept keepsake from her first childhood pickpocketing (a memento of hardship/why she stays hard), a genuine, costly personal offering, not a prop | 325 |

> **Note**: session 2's awards used the old flat value of 25, which testing later showed was over-generous at level 1 (8% of a level per instance). **Those awards stand** — XP already given is not taken back. The corrected per-level table applies from session 3 onward, where level 1 pays 10 per instance.
