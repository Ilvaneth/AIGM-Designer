# Downtime Activities

**Why this file exists**: `system-register.md` flagged `downtime-activities` `❌ Missing` since the campaign began — the moment the party spends real in-fiction days between adventures (a week in a city, a stretch waiting on a clock like Tain's attainder research or Yeva's circuit visit), nothing existed to resolve what that time actually does. Built 2026-08-30 per direct DM request, alongside `holdings.md`/`holding_status.py` — the two are meant to be used together (Holding Management, below, IS this file's bridge to that system).

**This is a homebrew layer, not an SRD import.** The free SRD included with this project has no downtime chapter — these numbers (days, gold, DCs) are original campaign house rules, built to fit this party's pace and this table's tone, not lifted from a book this project can't verify against its own local SRD files. Say so if a player asks; don't present them as official 5e rules.

Run every check through `downtime_check.py` — it looks up the real modifier via `character_modifier.py` (never hand-picked) and tells the DM exactly what to ask for, same discipline as every other roll in this campaign (`CLAUDE.md`'s ownership table: the player rolls, Claude states the modifier).

```
py .claude/scripts/downtime_check.py ashen-crown --menu
py .claude/scripts/downtime_check.py ashen-crown --research <character> <skill> <dc> "<topic>"
py .claude/scripts/downtime_check.py ashen-crown --carouse <character> [--skill Persuasion|Deception|Intimidation] [--spend modest|comfortable|lavish]
py .claude/scripts/downtime_check.py ashen-crown --craft <character> "<item>" <value_gp>
py .claude/scripts/downtime_check.py ashen-crown --resolve <character> <raw_d20>
py .claude/scripts/downtime_check.py ashen-crown --status
```

---

## The activities

### 1. Research

Use when a PC spends downtime chasing an open question — `state.md`'s Open Threads, a personal-arc lead (Ilvaneth's mother, Kriv's betrayer), or something a scene surfaced ("Tain is digging into who signed the attainder" is Tain's own research, not the party's, but the same pattern applies if a PC wants to dig too).

- **Time**: 1-3 days, DM's call based on the venue (a real archive is faster than asking around).
- **Skill**: pick what fits the topic — Investigation (physical/documentary), History (lore/genealogy), Arcana (magical theory), Religion (faith/theology), Nature, or another skill if the topic calls for it.
- **DC by obscurity**:
  | Obscurity | DC | Example |
  |-----------|----|----|
  | Common knowledge, just needs organizing | 10 | Public records, well-known history |
  | Specialized, needs the right venue | 15 | Guild/temple archives, a specific expert |
  | Secret or deliberately obscured | 20 | Concordat internal records, a suppressed scandal |
  | Actively hidden/warded | 25 | Something someone worked to bury |
- **Outcome**: success reveals real information — pull from what's actually true in the campaign's own files (an NPC's Current knowledge & stance, a faction file, an Open Thread), never invent a fact wholesale to fit the roll. A failure can still cost the time/gold and reveal a half-truth or a red herring, DM's call, same as any other failed check in this campaign.
- **Run it**: `--research <character> <skill> <dc> "<topic>"` → prints the ask (skill, DC, modifier). Player reports raw. `--resolve <character> <raw>` → pass/fail against the stored DC.

### 2. Carousing

Use when a PC spends downtime socializing, drinking, gambling, working a room — the DMG's classic "what did carousing get me" beat, reframed for a Neutral Evil pair who'd carouse to work an angle as much as to relax.

- **Time**: a few nights within the week.
- **Cost**: gp spent scales the outcome table's floor — modest (10 gp), comfortable (25 gp), lavish (50 gp). Spent regardless of the roll's result (`gold_spend`).
- **Check**: Persuasion, Deception, or Intimidation — the player's choice of *how* they carouse (charming a room vs. running a con vs. muscling respect), DC 10.
- **Outcome table** — roll 1d8 via `roll.py --owner dm-table` (this is a DM-table roll, not the PC's check, same as any random-table lookup in this campaign) after the Persuasion/Deception/Intimidation check resolves. Success shifts the table up one band (treat a roll of 1-2 as 3-4 instead); failure shifts it down one band (treat 7-8 as 5-6 instead):

  | 1d8 | Outcome |
  |-----|---------|
  | 1-2 | A real complication — a debt, an enemy made, a compromising scene witnessed. Draw on the campaign's own NPCs/factions rather than inventing someone new when possible. |
  | 3-4 | Nothing notable — an ordinary night, spend logged, no further effect. |
  | 5-6 | A useful rumor (pull from `rumors.md`'s pool, or a real fact the campaign already knows that fits the scene) or a minor contact made. |
  | 7-8 | A real opening — a genuine lead, a `jobs-and-opportunities.md`-worthy contact, or a disposition shift with someone already on the board. |

- **Run it**: `--carouse <character> [--skill ...] [--spend ...]` → spends the gold immediately (`gold_spend`), prints the ask. `--resolve` → pass/fail, then roll the 1d8 yourself via `roll.py 1d8 --owner dm-table` and apply the shift.

### 3. Crafting

Use when a PC wants to make a mundane item themselves rather than buy it — `items-and-loot.md` still governs buying/selling; this is only for building something with a tool proficiency.

- **No roll required** — crafting in this campaign is a time-and-cost commitment, not a check, unless the DM wants to add a complication for a rushed or unusual job (judgment call, not the default).
- **Time**: 1 day per 25 gp of the finished item's market value (round up, minimum 1 day).
- **Cost**: half the item's market value, in raw materials, spent up front (`gold_spend`).
- **Requires**: proficiency with the relevant tool (check the character's own Notable Items/Proficiencies — same discipline as `character_modifier.py`'s equipment lookup, don't assume).
- **Run it**: `--craft <character> "<item>" <value_gp>` → pure calculator, prints days + materials cost, no state stored (nothing to resolve later).

### 4. Training

Use when a PC wants to pick up a new tool or language proficiency they don't already have. Low priority, kept minimal on purpose.

- **Time**: 10 days. **Cost**: 50 gp (a tutor, materials, lost work).
- **No roll.** At the end of the time+cost, the proficiency is simply gained — add it to the character's sheet directly.
- Not currently wired into `downtime_check.py` as its own flag — resolve by hand (it's just a day/gold bookkeeping entry) unless this gets used often enough to be worth a calculator too.

### 5. Recuperating

Use for a lingering nonmagical ailment or a level of exhaustion that a long rest alone won't clear (per the SRD's own exhaustion/disease rules — check `srd_lookup.py condition "Exhaustion"` before assuming what a rest does and doesn't fix).

- **Time**: DM's call based on the ailment, typically 3-7 days of real downtime (not just a long rest).
- Not wired into `downtime_check.py` — this is rare enough, and the actual mechanical resolution (removing an exhaustion level, curing a disease) already runs through `update_character.py condition_remove` once the time has passed. No new machinery needed.

### 6. Holding Management

**This is the bridge to `holdings.md`/`holding_status.py`.** Spending downtime "running the business" is itself a legitimate downtime activity — it's what actually justifies collecting accrued income and checking for trouble, rather than those happening for free with no time cost.

- **Time**: a few days of the week, doesn't have to be the PC's whole week — can be layered with something else DM's call.
- **Run it**: `py .claude/scripts/holding_status.py ashen-crown --collect <holding>` for the payout, `py .claude/scripts/holding_status.py ashen-crown --risk-check <holding>` to see if anything went wrong while it was being run. See `holdings.md` for the full holding list and current numbers.

---

## How this fits a session

Offer downtime the same way `sandbox-index.md` already asks for "at least three visible options" — a week in a city is itself one of those options, not an automatic default. When the party settles into downtime:

1. Ask each PC what they're spending the week on (can differ per PC — Ilvaneth researching while Kriv manages a holding is the normal case, not an exception).
2. Resolve each via the flags above.
3. Advance the in-fiction day count in `state.md` by however long the longest activity took, same as any other time skip — check `rest_check.py`/`world_events_check.py`/`campaign-clock.md` afterward, exactly like any other multi-day jump.

Downtime is not a narrative void — `scene-variety.md`'s Downtime/Personal category still applies. A mechanically-resolved week can and should still get a real narrated beat (a quiet scene between Kriv and Ilvaneth, an ascension cost surfacing), not just a wall of dice results.
