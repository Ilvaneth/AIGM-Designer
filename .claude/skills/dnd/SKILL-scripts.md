# D&D Skill — Scripts Reference

Full syntax for all Python helper scripts. Load this file once at `/dm:dnd load`, then it stays in context for the session.

> **Path note:** commands below use `${CLAUDE_SKILL_DIR}` for the skill directory. This file is read verbatim, so that token is **not** auto-expanded here — substitute the absolute skill-dir path (from `SKILL.md`) before running any command, or it will fail with a broken `/scripts/…` path.

---

## Dice Script — `scripts/dice.py`

**MANDATORY for DM-side dice.** Every die the DM owns — NPC/monster attacks and saves,
environmental and trap damage, random tables — must be produced by invoking this script via Bash.
**Never sample dice mentally or with inline `random` calls.** Dice belonging to a player character
are never rolled here; the player rolls them (see SKILL.md "Dice ownership").

**`--owner` is required on every roll** — name whose die it is. If the owner resolves to a
player character in the active campaign the script refuses to roll (exit 3) and tells you to ask
the player. That refusal is the rule working, not a bug: ask for the raw number instead.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+8 --owner "Bone Devil" --label "Sting vs Kriv AC22"
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py 5d6 --owner "Bone Devil" --label "Sting poison damage"
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20 adv --owner "Erinyes" --label "WIS save (Magic Resistance)"
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py 4d6 --owner trap --label "Falling rocks onto the party"
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+2 --owner "Goblin" --silent   # integer only
```

Owners that are not characters — `trap`, `environment`, `table`, a monster name — always roll.
Pass `--campaign <name>` if no campaign is marked active. Flags nat 20 (CRITICAL HIT) and nat 1
(FUMBLE) automatically.

---

## Ability Scores Script — `scripts/ability-scores.py`
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py roll
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py pointbuy
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py pointbuy --check STR=15 DEX=10 CON=15 INT=8 WIS=11 CHA=12
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py modifiers STR=15 DEX=10 CON=15 INT=8 WIS=11 CHA=12
```
Roll mode: generates 3 arrays (4d6kh3 × 6 each). Point buy mode: prints cost table; `--check` validates against the 27-point budget.

---

## XP Script — `scripts/xp.py`
Awards XP for combat and qualifying non-combat encounters. Reads character files from the campaign directory and updates XP. All tables (difficulty thresholds, CR→XP, level advancement) are codified in the script — the DM only decides the difficulty tier or provides a monster list.

**Combat XP is the raw CR sum ÷ party size.** The DMG encounter-size multiplier (×1.5/×2/×3) is
off by default: it exists to express how much harder a group fight *feels*, and awarding that
inflated number as XP levels a party far faster than the CR budget intends. `--group-multiplier`
restores the DMG behaviour for a single call.

```bash
# Preview — no files modified:
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py calc --level 3 --players 2 --difficulty hard --type combat
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py calc --level 3 --players 2 --monsters "goblin:1/4:3,hobgoblin:1:1"

# Award after a combat encounter — difficulty-rated (use when full monster list is unavailable):
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py award \
  --campaign <name> --characters "Max of Thraxx,Ethros the 19th" --difficulty hard --type combat

# Award after a combat encounter — exact CR calculation (preferred for standard combats):
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py award \
  --campaign <name> --characters "Max of Thraxx,Ethros the 19th" \
  --monsters "goblin:1/4:3,hobgoblin:1:1" --note "Ambush in the alley"

# Award for a qualifying non-combat encounter:
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py award \
  --campaign <name> --characters "Max of Thraxx,Ethros the 19th" --difficulty medium --type noncombat \
  --note "guild informant interrogation"
```

**Difficulty tiers:** `easy` `medium` `hard` `deadly`
**Encounter types:** `combat` `noncombat` (both use the same difficulty threshold table)
**Monster CR formats:** `1/4`, `0.25`, `1/2`, `0.5`, `1/8`, `0.125`, or integer (`1`, `5`, `10`)
**Monster count:** omit for 1 (e.g. `"dragon:10"`); explicit for groups (e.g. `"goblin:1/4:3"`)
**Monster multiplier** (applied automatically): ×1 (1), ×1.5 (2), ×2 (3–6), ×2.5 (7–10), ×3 (11–14), ×4 (15+)

`award` updates the character file XP field and flags LEVEL UP PENDING if a threshold is crossed. The `--note` label prints to terminal only — not stored.

---

## Combat Script — `scripts/combat.py`
```bash
# Order initiative and print tracker. NPC entries are rolled here; every "pc" entry
# must carry the player's own raw d20 as "init" — the script never rolls for a PC
# (it exits 2 and names the PCs whose roll is missing).
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py init '<JSON>'
# JSON: [{"name":"Flerb","dex_mod":0,"hp":12,"ac":16,"type":"pc","init":14},
#        {"name":"Goblin","dex_mod":1,"hp":7,"ac":15,"type":"npc"}, ...]

# Reprint tracker from saved state
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py tracker '<JSON>' <round_num>

# Resolve a single NPC/monster attack
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py attack --atk 4 --ac 15 --dmg 2d6+2
# A PC's attack: pass the player's own raw d20 — never let the script roll it
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py attack --atk 15 --ac 18 --dmg 1d12+9 --d20 13
```
`init` outputs `STATE_JSON:` line — store in `state.md` under `## Active Combat` between turns.

---

## Character Script — `scripts/character.py`
```bash
# Full stat block from raw scores
python3 ${CLAUDE_SKILL_DIR}/scripts/character.py calc --class fighter --level 1 \
    STR=15 DEX=10 CON=15 INT=9 WIS=11 CHA=14 \
    --proficient STR CON Athletics Intimidation Perception Survival

# Level-up — run this BEFORE presenting any level-up info to the player, never
# reason about what a level grants from memory (added 2026-09-14, after a
# proficiency-bonus band change got missed entirely). Prints HP, a loud flag if
# the proficiency-bonus band changed (recompute every proficient stat + every
# attack/save-DC on the sheet when it fires), ASI/feat eligibility, class
# features gained at exactly this level, subclass features (with --subclass),
# and spell slot changes for casters. See SKILL.md's level-up discipline note.
python3 ${CLAUDE_SKILL_DIR}/scripts/character.py levelup --class fighter --subclass "battle master" --from 1 --hp-roll 7 --con-mod 2

# XP tracking
python3 ${CLAUDE_SKILL_DIR}/scripts/character.py xp --level 1 --gained 150
```

---


---

## Tracker Script — `scripts/tracker.py`
Tracks conditions, concentration, timed effects, and death saves. State persists at `~/.claude/dnd/campaigns/<name>/tracker.json`.

```bash
CAMP=my-campaign

# Timed effects — duration: 10r (rounds), 60m (minutes), 8h (hours), indef
# Append 'conc' to mark as concentration (auto-sets concentration field)
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect start "Max of Thraxx" "Web" 10r conc
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect start "Ethros the 19th" "Disguise Self" 1h
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect start "Ethros the 19th" "Hunter's Mark" indef
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect end   "Max of Thraxx" "Web"   # narrative end (broken/dispelled)
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect tick  "Max of Thraxx"         # call on actor's turn — decrements rounds, prints expiry

# Conditions
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP condition add "Ethros the 19th" poisoned
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP condition remove "Ethros the 19th" poisoned
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP condition clear "Ethros the 19th"

# Concentration (auto-clears previous if switching spells)
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP concentrate "Max of Thraxx" "Bless"
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP concentrate "Max of Thraxx" break

# Death saves
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" success
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" failure
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" stable
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" reset

# Status / clear
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP status
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP status "Ethros the 19th"
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP clear           # conditions + concentration + effects
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP clear --all     # also clears death saves

# Combat Triggers + Passive Item Effects — prints a PC's own "## Combat Triggers"
# AND "## Passive Item Effects — Quick Reference" sections from their character
# sheet (see SKILL-combat.md). Run --all at TWO points: (1) at /dm:dnd load, right
# after reading character files — passive item effects (Stealth advantage from a
# cloak, doubled speed from boots, etc.) are easy to lose in a long Notable Items
# list, especially in a fresh tab with no carried-over context; (2) the instant
# combat.py init is called for a scene, so crit/kill/reaction triggers are fresh.
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP triggers --all
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP triggers "Max of Thraxx"   # one PC, re-check mid-fight/mid-scene

# Turn start (PCs only) — mandatory, run this at the start of EVERY PC turn, not
# just once at combat init. Merges effect-tick + triggers into one unskippable
# call with a loud banner — added 2026-09-14 because "pull triggers once at
# combat start" reliably stopped happening turn-to-turn (feats/item passives/
# Ascension gains missed mid-fight, a real repeated failure). No-ops safely on
# an NPC/monster name. See SKILL-combat.md — nothing about a PC's turn should
# be narrated or rolled before this has run.
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP turn "Max of Thraxx"
```

**When to run:** condition applied/removed; caster begins/loses concentration (immediately, not end of turn); PC drops to 0 HP; each death save rolled; end of encounter → `clear`; combat start → `triggers --all`; **the start of every single PC turn thereafter → `turn <name>`, no exceptions.**

---

## Calendar Script — `scripts/calendar.py`
```bash
# One-time setup (run during /dm:dnd new):
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP init \
    --date "15 Harvestmoon 1247" \
    --time "morning" \
    --months "Frostfall,Deepwinter,Thawmonth,Seedtime,Bloomtide,Highsun,Harvestmoon,Duskfall" \
    --month-length 30 \
    --day-names "Sunday,Moonday,Ironday,Windday,Earthday,Fireday,Starday"

# Time advancement
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP advance 8 hours
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP advance 2 days
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP rest short   # +1 hour
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP rest long    # +8 hours

# Query / manual set
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP now
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP set "22 Harvestmoon 1247" evening
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP time night
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP events
```

**When to run:** at the end of **every scene that costs in-world time** — not only rests and travel. A day
that never reaches evening is the signature of a clock that only moves for long rests. Scene costs live in
the script (`scene --list`), so the DM picks a type rather than inventing a duration:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP scene conversation    # +30m
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP scene meeting         # +1h30m
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP scene research        # +3h
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP scene summit          # +4h, a negotiation that decides something
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP scene feast           # +4h, a banquet or ceremony
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP advance 20 minutes    # anything else
```

**One clock, one source.** `calendar.json` is authoritative; `state.md`'s date line is a copy produced by
`calendar.py -c $CAMP stateline`, never composed by hand. `calendar.py -c $CAMP check` compares the two and
exits 2 with a loud banner when they disagree — run it at `/dm:dnd load` and `/dm:dnd save`.

**Other planes.** Time elsewhere can run at a different rate than the material plane. Declare it on arrival
and the arithmetic follows automatically: `material_minutes = local_minutes x rate`.

```bash
calendar.py -c $CAMP plane enter "The Ember Court" --rate 3    # 1h inside = 3h outside
calendar.py -c $CAMP plane enter "Feywild" --rate-range 0.5:30 # rate rolled once, hidden from players
calendar.py -c $CAMP plane rate --rate 6                       # revise it mid-stay
calendar.py -c $CAMP plane status
calendar.py -c $CAMP plane exit                                # prints experienced vs elapsed
```

While a plane is active, `advance`/`scene` count the time the **party experiences**; the material clock moves
by that amount times the rate, so the world they return to is already correct. `now` prints both.

**Legacy note:** when manually updating `state.md` date — use `calendar.py set` to keep them in sync.

**Long Rest discipline (added 2026-09-14, after a live confusion where a rest called mid-afternoon mechanically landed on "9 PM" and then got narrated as "morning" anyway):**
1. **Check the 24-hour rule before granting one.** A character can't gain the benefit of more than one long rest in a 24-hour period (and needs ≥1 hour since the last one ended). If a player calls for a Long Rest sooner than that, say so plainly — don't silently grant or silently block it.
2. **`rest long` adds a flat +8 hours from whatever hour it currently is — it does not know the party intends to sleep through to morning.** If the party settles in mid-afternoon/evening intending to rest for the night (the overwhelmingly common case), prefer `calendar.py set "<next day>" morning` over `rest long`, so the party actually wakes at a natural hour instead of a mechanically-precise but narratively-odd one (e.g. 9 PM). Reserve the bare `rest long` `+8h` add for a rest genuinely taken at an odd hour where the party explicitly wants to stop resting the instant the mechanical minimum is met.

---

## Campaign Search — `scripts/campaign_search.py`
Keyword search across campaign files. Use this **before** loading full files into context when looking up a specific past event, NPC detail, or plot thread.

```bash
CAMP=my-campaign

# Search all default files (state, log, archive, world, npcs):
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP Lasswater

# Narrow to specific files:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP "merchant letter" --files log,archive

# Multi-keyword AND search:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP VARETH Kel

# More context lines around each match:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP Harwick -C 6
```

File keys: `state`, `log`, `archive`, `world`, `seeds`, `npcs`, `npcsfull`
Default files searched: state, log, archive, world, npcs

**When to use:** Any time a player asks about a past event, NPC detail, location, or plot thread that may not be in active context. Run this first — only escalate to a full `Read` if the search returns insufficient context.

---

## Session Recap — `scripts/session_recap.py`

Deterministic state-diff between two character snapshots. Computes the mechanical change set (HP/temp/level/hit dice/death saves/conditions/concentration/exhaustion/inspiration/spell slots) from data so narration never recomputes it — recaps are the single thing an LLM is most likely to hallucinate. Reads `<campaign>/characters/*.md` and merges live `tracker.json` conditions/concentration. Zero LLM calls.

```bash
CAMP=my-campaign

# Snapshot the party now — sets the baseline (writes to <campaign>/.recap/,
# rolling last → prev). Run this at session START (e.g. /dm:dnd load) so there
# is a baseline to diff against later.
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py snapshot --campaign $CAMP

# Diff the baseline against current state → one-paragraph summary, then ADVANCE
# the baseline to "now" so the next diff chains from here. Run at /dm:dnd save
# (end of session) for a since-start recap, or each turn for a since-last-turn
# recap — either way it advances, so consecutive diffs never re-report old deltas.
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff --campaign $CAMP
# → "Aldric: took 18 damage (30→12 HP); gained Poisoned; spent 2 level 1 slots."

# Same comparison without moving the baseline (ad-hoc "what changed so far?"):
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff --campaign $CAMP --no-roll

# Structured change list instead of prose:
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff --campaign $CAMP --json

# Diff two snapshot files directly (no campaign lookup):
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff-files before.json after.json
```

---

## Oracle — `scripts/oracle.py`

Dice-driven solo/improv oracles (Mythic chaos factor, Ironsworn yes/no, Random Event Focus, scene-meaning word pairs). Keeps pacing transparent and rollable instead of invented. Rolls are stdlib-random and seedable (`--seed N`). The chaos factor persists in `state.md → ## Session Flags` as `chaos_factor: N`. Zero LLM calls.

```bash
CAMP=my-campaign

# Chaos factor (1-9): show / set / adjust (persisted to state.md)
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py chaos --campaign $CAMP
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py chaos set --campaign $CAMP --value 7
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py chaos adjust --campaign $CAMP --pc-lost

# Yes/no oracle — likelihood + chaos modifier → verdict + d100
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py ask --likelihood likely --campaign $CAMP
# → "NO-BUT  (d100=82, likelihood=likely, chaos=8)"

# Random Event Focus (d100 → direction label)
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py event

# Scene-meaning word pair (action / subject)
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py scene
```

Likelihoods: `sure-thing`, `likely`, `50/50`, `unlikely`, `no-way`. Verdict suffixes: `-and` (extreme, on doubles), `-but` (qualified, near threshold).

---

## Private Channels — `scripts/channels.py`

Who was party to a private exchange, and what passed through it. The check that catches an NPC citing
a troop count they could only have read over someone else's Sending Stone.

```bash
channels.py -c $CAMP list [--verbose]
channels.py -c $CAMP add --id stone-sethra --type sending-stone     --name "Sending Stone — Kriv/Sethra" --participants "Kriv Shestendeliath,Sethra Shestendeliath"
channels.py -c $CAMP fact stone-sethra --day 206 --text "Order to raise 200 soldiers"     --keywords "200 asker,200 soldiers"

# Before an NPC says something that may not be theirs to know (exit 2 = it isn't):
channels.py -c $CAMP check "Hold'da 200 asker toplanıyor" --speaker "Vessa Kettring"
channels.py -c $CAMP who "200 asker"
```

Channel types: `sending-stone`, `private-meeting`, `letter`, `spell`, `other`. Record the fact the
moment the exchange happens — the leak always comes later, once you have forgotten it was private.

---

## Faction Board — `scripts/factions.py`

The chessboard between factions: objectives, running operations with in-world due days, a weekly
move-point budget, an intelligence rating, and stances toward every other faction and the party.
Without it, "the rivals respond when the party allies with someone" has no data to compute from and
degrades into whatever the DM can reconstruct from prose at session end — which is how factions come
to feel like scenery.

```bash
CAMP=my-campaign
python3 ${CLAUDE_SKILL_DIR}/scripts/factions.py -c $CAMP list          # the board at a glance
python3 ${CLAUDE_SKILL_DIR}/scripts/factions.py -c $CAMP show whisper-court

# Build it
factions.py -c $CAMP add --id house-corr --name "House Corr" --power 3 --intel 2     --objective "Hold the seat without paying for open war" --assets "Chancellery influence; old money"
factions.py -c $CAMP stance --from house-corr --to house-ilvane --level -2   # -3..+3, or --to party
factions.py -c $CAMP set house-corr --reaction "alliance=Makes itself indispensable to the winner first"
factions.py -c $CAMP op house-corr --name "First among three"     --step "Buy the succession clerk@209" --step "Force a vote while Ilvane is weak@216"     --abandon-if "Veskin rules the seat vacant"

# Run it
factions.py -c $CAMP tick --day 207        # refresh budgets, surface due/overdue steps
factions.py -c $CAMP react --actor house-corr --trigger alliance --visibility public --day 204     --event "House Corr backed the party openly at the Chancellery"
factions.py -c $CAMP move whisper-court --spend 1 --day 204 --text "Buys the clerk's brother"
factions.py -c $CAMP step house-ilvane 1   # mark step 1 complete
factions.py -c $CAMP sweep --day 204       # end-of-session forward pass
factions.py -c $CAMP check --day 204       # quiet unless the board needs a move (exit 2)
```

**`react` is the important one.** Give it the event, who caused it, how visible it was
(`public` / `rumored` / `secret`) and the day. It prints, for every faction: whether they learn it at
all (secret events only reach intel 2+), on what day (delay shrinks with intelligence), their stance
toward the actor, their standing doctrine for that trigger, their current operation and their
remaining budget — then separates those **compelled to answer** from those merely aware. Write a move
for each compelled faction before play moves on.

**A plan's countable prerequisite lives on the operation**, not in a second tracker: coin raised,
votes secured, troops sworn, fragments held. `op <id> --metric "gp raised:6000/40000"` sets it,
`metric <id> --add 1500` moves it, and `sweep` prints how far short the plan still is — a faction
whose plan needs 40,000 gp and holds 6,000 is not about to act, and the board should say so.

`check` flags three things: a faction with no operation, a step past its due day, and a faction
that has **never moved** once it has been on the board longer than a fortnight. A future-dated step is
not activity — a faction can sit on a plan for weeks and raise nothing, which is exactly how two great
houses sat out two whole sessions in silence. Pass `--day N` when adding a faction so the grace period
is measured from when it actually joined the board.

**Move points** scale with `power` and refresh weekly. Spending them is what makes a move cost
something; when the party destroys a faction's asset, lower its `power` and the budget falls with it.
A faction that is out of points this week cannot also be acting everywhere — that is the constraint
that turns "they watch and wait" from a free default into a decision.

**Triggers** for `--trigger`: `alliance`, `loss`, `gain`, `exposure`, `death`, `betrayal`, `other`.
Each faction can carry a doctrine line per trigger (`set --reaction "loss=..."`).

---

## Goal Tracker — `scripts/goals.py`

Structured NPC/faction goal tracking, backed by `<campaign>/goals.json`. Built so a crossed threshold gets the same loud, unmissable treatment `xp.py` gives a level-up (`⚠⚠⚠ ... HEDEFE ULAŞILDI`) instead of living only in prose that's easy to forget to check. See `templates/npcs.md`'s Goal Tracker section for the record format, and SKILL.md's "Goal Tracker check" (same cadence as the continuity micro-save) for when to touch this during play.

```bash
CAMP=my-campaign

# Numeric-metric goal (e.g. "fragments collected toward 9"):
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py add --campaign $CAMP --id sarelle --name "Sarelle Duskbourne" \
  --kind npc --goal "One-sentence goal" --metric-type numeric --current 0 --target 9 \
  --metric-label "Crown fragments (in her possession)" \
  --threatened "Pre-written move when the goal is at risk" \
  --blocked "Pre-written move when actively thwarted" \
  --permanent-loss "Pre-written, irreversible move when the goal becomes impossible"

# Boolean-metric goal (a yes/no-answerable condition, not a numeric count):
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py add --campaign $CAMP --id coren --name "Coren Ashvale" \
  --kind npc --goal "One-sentence goal" --metric-type boolean \
  --condition "The concrete yes/no fact that would mean this goal landed" \
  --threatened "..." --blocked "..." --permanent-loss "..."

# Update progress — prints the threshold banner automatically if target/condition is now met:
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py set --campaign $CAMP --id sarelle --current 6 --session 32
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py achieve --campaign $CAMP --id coren --session 32

# Mark a threatened/blocked/permanent_loss state (prints that record's pre-written response):
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py status --campaign $CAMP --id sarelle --value threatened

# Full board — also flags any record with an incomplete threshold-response set:
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py check --campaign $CAMP

# Quick listing / single-record detail:
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py list --campaign $CAMP [--kind npc|faction]
python3 ${CLAUDE_SKILL_DIR}/scripts/goals.py show --campaign $CAMP --id sarelle
```

**When to use:** only for NPCs/factions with a single, central, campaign-level goal worth tracking across sessions (faction leaders, a named antagonist) — not every walk-on. Update the moment something in play moves the metric (a fragment recovered, an agent exposed); don't batch it for `/dm:dnd save`. Run `check` at save time as a backstop, per SKILL-commands.md's Goal Tracker sweep.

---

## Deterministic Graph Extraction — `scripts/graph_extract_deterministic.py`

Zero-LLM relationship extractor. Pattern-matches session-log sentences against the bundled verb-table seed (`data/graph/verb_table_seed.yaml`) and emits typed edge proposals in the exact shape `campaign_graph.py` consumes. ~50% recall (clean subject-verb-object only), ~95% precision, no Claude API call. Usually driven through `campaign_graph.py extract --deterministic` rather than directly:

```bash
CAMP=my-campaign

# Propose edges (stdout), no writes:
# Who is off the board — read before writing any opening scene:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py gone --campaign $CAMP --type npc
# add-node refuses a name that already exists (including aliases), because two
# nodes for one character split its edges and a death on one leaves the other
# reading as alive. --allow-duplicate-name if they really are different people.

# Deaths written in prose but never recorded as edges (exit 2 = found some):
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py gone --campaign $CAMP --audit

python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py extract --campaign $CAMP --deterministic

# One-shot auto-apply high-confidence proposals into graph.json (idempotent):
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py extract --campaign $CAMP \
    --deterministic --apply --min-confidence high
```

---

## Data Commands — `scripts/sync_srd.py`, `scripts/build_srd.py`, and `scripts/lookup.py`

Dataset is bundled at `${CLAUDE_SKILL_DIR}/data/dnd5e_srd.json`. No runtime download required.

**Monster defenses** (damage immunities/resistances/vulnerabilities, condition immunities, saving
throws, skills, senses) come from the SRD 5.1 text bundled at `${CLAUDE_SKILL_DIR}/data/srd-5.1-yaml/`
(OGL 1.0a, see `00-legal.yaml`). `build_srd.py`'s importers drop these fields, so
`merge_srd_defenses.py` puts them back; re-run it after any dataset rebuild or the
`-- DEFENSES --` block disappears from monster lookups.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/merge_srd_defenses.py --dry-run   # report, write nothing
python3 ${CLAUDE_SKILL_DIR}/scripts/merge_srd_defenses.py             # merge (backs the JSON up first)

# Check / rebuild dataset (only needed when upstream sources update):
python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py             # rebuild if 5e-bits or FoundryVTT has new commits
python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py --check     # check upstream SHAs, don't rebuild
python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py --force     # always rebuild
python3 ${CLAUDE_SKILL_DIR}/scripts/build_srd.py --status   # show current dataset metadata

# Lookup during play (CLI):
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py spell "fireball"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py item "cloak of protection"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py feature "sneak attack"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py condition "poisoned"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py monster "goblin"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py monster "dragon" --all   # all fuzzy matches

# Rules prose — grappling, cover, resting, travel pace, traps, madness, planes:
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py rules "grappling"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py rules "cover"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py rules "travel pace"


# Programmatic (importable from other scripts):
from lookup import lookup, lookup_record, lookup_with_level, suggest
lookup("fireball", category="spell")                  # → formatted string
lookup_with_level("sneak attack", category="feature", level=3)  # → level-resolved string
suggest("poisonned", category="condition")            # → [("Poisoned", "conditions"), ...]
```

**Did-you-mean recovery.** A mistyped name doesn't dead-end. When a lookup misses, the CLI prints a `Did you mean: …?` line and the display's SRD modal offers tappable near-miss chips — both powered by `suggest()`, which fuzzy-matches the query against real names (`poisonned` → Poisoned, `fireballl` → Fireball, `gobblin` → Goblin). Suggestions respect the category when one is given, and search all categories otherwise. Use the suggested name rather than guessing at a spelling.

**Rules lookups.** 212 entries from the SRD 5.1 chapters on combat, general mechanics, running the
game, spellcasting procedure, conditions, equipment and the planes — built by
`build_rules_index.py` into `data/dnd5e_rules.json`. **Use it instead of answering a rules question
from memory**: grapple and escape contests, cover degrees, suffocation, falling, exhaustion levels,
long/short rest, travel pace, hiding and unseen attackers, traps, madness. Rebuild with
`python3 ${CLAUDE_SKILL_DIR}/scripts/build_rules_index.py` if the YAML source changes.

**When to use:** combat (monster stat blocks before using them); spellcasting (range, components, duration, at-higher-levels); conditions (rule text before applying); loot and equipment; NPC generation (monster stat block as mechanical base). The display companion's character sheet modal handles lookups automatically during play — these CLI calls are for DM reference outside the UI.

---


---

## Entity Registry — `scripts/registry.py` (designed campaigns)

The registry is the catalogue of everything a designed campaign contains (plan item 3; `docs/schemas/entities.md`). Two files: the **canonical** registry at `design/dm-only/entities.json`, which the play tab never opens, and its **public projection** at `design/entities.json`, regenerated on every write by two mechanical rules (drop every `secret` entity, drop every `dm_only` object). Stamped fields are frozen at birth; their birth values sit in `design/dm-only/_snapshots/stamps.json`. Play-time truth (status, seen_in_play, alive, location, ruler, control) lives in `design/overlay.json`, never in the registry.

```bash
py registry.py -c <campaign> show <id>                   # one entity, public projection
py registry.py -c <campaign> list [--type npc] [--secrecy discoverable]
py registry.py -c <campaign> play-set <id> <field> <value> --day <N> --reason "<why>" [--news news_0012]
py registry.py -c <campaign> add --type place --name "<name>" --summary "<one line>"   # a place improvised in play
py registry.py -c <campaign> check-stamps                # exit 1 if any stamped field drifted from birth
```

- `play-set` is the DM's only pen on a designed entity: `alive` (alive / threatened / wounded / fled / captured / dead), `location`, `ruler`, `control` (a faction id, `party`, or `null`), `status` (sites and settlements), `seen_in_play`. A stamped field is refused: the bible is not rewritten in play.
- `add` registers a place, NPC or site that appeared in play (`--origin play`) so the index and the validator can see it; a site added this way starts as `played-improvised` and is backfilled by `detail` at `end`.
- `merge --phase PN [--revise LOG_ID]`, `project` and `export --public` belong to the designer's conductor, not to a play session. `merge` refuses a change to any stamped field without a revision id and writes nothing when any fragment is bad.
- Never `cat` the canonical file or the `_snapshots` folder in a play tab; `show` without `--dm` reads the projection.

## Site Progress — `scripts/site_progress.py` (designed campaigns)

A designed site is a graph, not a list (plan item 9.5). `site-progress.json` records every room of a detailed site as unseen / seen / cleared / skipped; the DM marks rooms as the party moves, `save` prints the line, and "which room were we in" survives a compaction.

```bash
py site_progress.py -c <campaign> enter <site_id> <room> --day <N> --session <N>    # first entry must be through an entrance
py site_progress.py -c <campaign> clear <site_id> <room> --day <N> --session <N>
py site_progress.py -c <campaign> skip  <site_id> <room> --reason "<why the route bypassed it>" --day <N> --session <N>
py site_progress.py -c <campaign> shortcut <site_id> --from <room> --to <room> --how "<what was earned>" --day <N>
py site_progress.py -c <campaign> rest  <site_id> <room> --kind short|long --day <N>
py site_progress.py -c <campaign> status                                             # "Batık İskele: 3/6 oda, 1 temizlendi — şu an oda 5"
```

- `open <site_id>` is run by `detail` when a site becomes detailed (it reads the room table's `Exits` column); a skeleton site has no record and cannot be entered — that is the "no improvising a designed site" rule made mechanical.
- The first `enter` writes the overlay's `status: played` and `seen_in_play`; nothing else touches those for a site.
- A skipped room without a reason is a validator finding; the reason is the party's route, not the DM's mood.

## Design Check — `scripts/design_check.py` (designed campaigns)

The structural validator (plan item 15.1). In play the DM runs only the fast form, at every `save`:

```bash
py design_check.py -c <campaign> --fast      # refs + stamps + secrecy; reports, never blocks the session
py design_check.py -c <campaign> --only <site_id>   # after a `detail` run, that entity alone
```

Output is redacted in every mode: a finding names an id, a field, a file and a code, never a secret name or a line of prose. The full run (`--modules refs,stamps,secrecy,overlay,map,sites`) belongs to the designer's phases and to `end`.

## Solo Boss Nova-Ceiling — `scripts/burst_check.py`

For a deliberately-unfinalized solo boss (see `SKILL-combat.md`) — sums every PC's own `## Burst Reference` table into a party-wide "worst case, one round, one target" figure, and checks it against a boss's HP.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/burst_check.py --campaign ashen-crown --vs undead --target-hp 90
python3 ${CLAUDE_SKILL_DIR}/scripts/burst_check.py --campaign ashen-crown   # no filter, no target — just report the ceiling
```

Run this immediately before the fight, against the party's real current sheets — not once, months earlier, from memory.

---

## Continuity Autosave — `scripts/autosave_checkpoint.py`, `scripts/install_autosave_hook.py`

Behind-the-scenes continuity checkpoint for long sessions, so a context compaction never loses the player's place. Two layers; see the *Continuity micro-save* rule in SKILL.md and the `/dm:dnd autosave` command.

```bash
# Opt-in: register the Stop hook (writes ~/.claude/settings.json, idempotent)
python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py
python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py --uninstall
python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py --status

# The hook target (also runnable by hand to force a snapshot or inspect state)
python3 ${CLAUDE_SKILL_DIR}/scripts/autosave_checkpoint.py --status
python3 ${CLAUDE_SKILL_DIR}/scripts/autosave_checkpoint.py --campaign <name> --snapshot-only
```

`autosave_checkpoint.py` runs as a Claude Code **Stop hook** (after each turn). It reads the active campaign from `<runtime-dir>/active-campaign.json` (written at `/dm:dnd load`) and the `autosave` flag from that campaign's `state.md`. It **no-ops** when no campaign is active (e.g. a non-D&D session), when `autosave: off`, or when already inside a hook-driven continuation. Every turn it snapshots `state.md` to the runtime dir; every N turns (default 10, `DND_AUTOSAVE_EVERY` to override) it emits a Stop-hook `block` decision that prompts the DM to flush continuity before yielding. The hook is **opt-in** — the in-model micro-save cadence works without it.

**When to use:** offer `install_autosave_hook.py` to players running long imported modules who hit compaction mid-session. The flag toggle (`/dm:dnd autosave on|off`) is the in-session control.

## Designer Hooks — `scripts/hooks/design_read_guard.py`, `dice_guard.py` during a designer run

`design_read_guard.py` is a PreToolUse hook on Read | Grep | Bash. It is armed only while a designer command runs, through `<runtime-dir>/active-design.json` (campaign, mode `birth` | `detail` | `playtest`, the arming session). While armed, the main session (the blind conductor) is denied every path under `design/dm-only/` and `design/_staging/` and the registry verbs that print dm-only content; the designer's fresh-context agents read them. In `playtest` the DM reads freely and the player agent is confined to the player-facing allowlist. Unarmed, nothing is guarded: the DM's own reads of a finished file are free. While a birth or `detail` run is armed, `dice_guard.py` also refuses a `dice.py` roll from an agent: agents never roll, the conductor pre-rolls every labelled die with `design_dice.py`.

## Lazy Corpus — `scripts/corpus_check.py`

Imported (structured) campaigns keep the full module text as a lazily-loaded reference layer instead of inlining it. Layout:

```
<campaign>/
  world.md           # load-time core (Foundations, Three Truths, factions)
  world-nodes.md     # lazy: full Quest Seed Bank + Adventure Nodes (per-act read)
  arc.md             # lazy: full act/chapter tree (state.md holds current+next only)
  source-index.md    # chapter-id -> source file -> one-line scope
  source/<id>.md     # lazy: one file per chapter, the module's source text
```

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/corpus_check.py --campaign <name>
```

Validates that every chapter id in `source-index.md` has a matching `source/<id>.md` (and vice-versa) and that `arc.md` exists. Run it at the end of `/dm:dnd import`. A campaign with no `source/` layer (dynamic, sandbox, or a pre-v2.2.0 import) is reported as a clean no-op — nothing to validate, and its load path is unchanged.
