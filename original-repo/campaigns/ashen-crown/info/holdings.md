# Holdings Ledger — the numbers behind `power-base.md`

**Why this file exists**: `power-base.md` describes what the five Gallowmere holdings *are* — the fiction, the cost, the enabler. It has always been explicit that it contains "zero income, upkeep, or risk mechanics" (`system-register.md`, ⚠️ Provisional). This file is that missing machinery: a real, script-computed ledger, not prose. Built 2026-08-30 per the DM's direct request to close the `holding-management` `❌ Missing` gap in `system-register.md`.

**Read `power-base.md` first** for the fiction (what each holding is, what it cost to get, who's involved). This file only carries the numbers and status a script needs to compute income, upkeep, and risk — it doesn't restate the story.

Run everything through `holding_status.py` — never hand-compute accrued income or hand-pick a risk outcome. Same discipline as `rest_check.py`/`character_modifier.py`: the fact is diffable, so it's a lookup, not a judgment call.

```
py .claude/scripts/holding_status.py ashen-crown --status              # all holdings, accrued income / pool balance shown
py .claude/scripts/holding_status.py ashen-crown --collect <slug> [--amount N]   # Business: accrued net income. Pool: N gp or full remaining balance
py .claude/scripts/holding_status.py ashen-crown --risk-check <slug>   # roll for unwanted attention, tier-scaled
```

---

## The rule that got violated once already — read before adding numbers to any `Held` entry

**A `Held` holding's Income/Upkeep numbers must trace back to something that actually happened in play** — a negotiated cut, a stated arrangement, an NPC's own file explicitly offering it (`npc-consistency.md`'s core rule, applied here: an NPC commitment that was never established is exactly as fabricated as an NPC offer made against their own self-interest). **Never fill them in as a plausible placeholder so the system has a live example to point at** — that's what happened to the Ash-Kilns entry below (caught by the DM, 2026-08-30, corrected same day; see `bug-log.md`).

This is different from a `Not yet taken` holding's *projected* numbers, which are explicitly speculative defaults for future negotiation and say so — those are fine to estimate ahead of time. The line is `Held` vs. `Not yet taken`: once a holding is marked `Held`, every number attached to it is a claim about what already happened, not a forecast.

## How the numbers work

**Two holding types — don't default to Business.** Added 2026-08-30 after the DM caught Fennick's debt book modeled as a perpetual weekly income, the same shape of error as the Ash-Kilns fabrication above, just structural instead of numeric: some holdings are operating businesses that genuinely regenerate value over time (a trade route, a working kiln); others are a **fixed pool** of something finite (a debt ledger, a one-time cache) that depletes as it's collected and does not refill on its own. Modeling a Pool holding with Income/Upkeep would silently give it infinite money it doesn't have. Check which kind a holding actually is — per its own fiction, not by default — before writing its numbers:

- **`Type: Business`** (the default if unstated, for backward compatibility with entries written before this distinction existed) — uses `**Income**`/`**Upkeep**`/`**Last collected**`, accrues per week, never depletes. The Ash-Kilns and the Docks are this type.
- **`Type: Pool`** — uses `**Total pool**`/`**Remaining pool**` instead. `--collect` pays out up to the remaining balance (never more) and permanently reduces it — no weekly regeneration, no `Last collected` day-math. Once `Remaining pool` hits 0, the holding is spent; that's a real, felt consequence, not a bug. Fennick's debt book is this type.

- **Income / Upkeep** (Business type only) are stated per in-fiction week (7 days), matching `world-events.md`'s existing 7-day cadence so this doesn't introduce a second, incompatible clock.
- **Accrued income never decays.** It simply accumulates from `**Last collected**` until the party actually collects — consistent with `campaign-clock.md`'s "the world moves off-screen" principle. Nothing is lost by not checking in every session; the payout is just bigger the longer it's left.
- **Risk tier** governs `--risk-check`'s odds of a complication on a d20 (rolled via `roll.py --owner dm-table`, never invented):
  | Tier | Complication on |
  |------|------------------|
  | Low | 1-2 |
  | Medium | 1-5 |
  | High | 1-10 |
- A risk-check complication is **not** auto-resolved by the script — it flags that one is warranted (and the roll that produced it) and points back at the holding's own `power-base.md` entry and Notes for what a real complication should look like at the table. The script computes the diffable fact (did a complication trigger); writing the actual complication is a judgment call, same division of labor `holding_status.py`'s sibling scripts already use.
- **Only a `Held` holding accrues or can be collected/risk-checked.** `Not yet taken` holdings carry a *projected* Income/Upkeep/Risk so the numbers exist the moment the party actually takes one — see `dungeon-design.md`/`faction-design.md`'s own precedent of building the standard before it's needed, not scrambling once it's live.

---

## Holdings

### The Ash-Kilns

**Status**: Held (access/leverage only — **no cash income established**)
**Taken**: Day 33 (session 5) — Odric Fenn turned without a fight
**Income**: *not established.* Checked against `npcs/odric-fenn.md`'s own "What he can offer" (2026-08-30, after the DM caught this): legitimacy for the site, the cell's cooperation, screening records, ash-supply access, and Choir-doctrine intel — **no weekly gold arrangement was ever negotiated in play.** An earlier version of this entry stated 40 gp/week income and 12 gp/week upkeep with no basis in any session — a fabricated fact, not a recorded one. Corrected; see `bug-log.md`.
**Risk tier**: Medium — a Cinder Choir cell operating under the party's protection, a caged failed "returner" in the fourth kiln, and both the Concordat and the Choir have reasons to eventually notice a shift in the region's ash supply
**Notes**: `holding_status.py --collect` cannot be run for this holding until real numbers exist — and real numbers only get written here **after** an actual scene establishes them (the party asking Fenn for a cut, a negotiated arrangement, something that happens at the table). Per `power-base.md`'s own tracker: "build them the moment the party actually tries to draw a number from it, not before." This holding's real value right now is the ash supply, the screening records (blackmail material), and the correspondence — not gold. A risk-check complication should draw on Fenn's own file first (does his cover slip, does Yeva Ashwright's circuit visit — `campaign-clock.md`, ~day 52 — connect to it) before inventing something unrelated.
→ `locations/the-ash-kilns.md`, `npcs/odric-fenn.md`

### Docks / smuggling route

**Status**: Not yet taken — Planning (per `power-base.md`'s tracker: scouted, two live strategies discussed, not yet acted on)
**Projected income**: 60 gp/week — moving goods without inspection, a lever on every merchant in Gallowmere
**Projected upkeep**: 15 gp/week — buying loyalty across the underpaid garrison, or whatever arrangement is struck with Kell
**Projected risk tier**: High — runs directly through Captain Kell, who is himself an Ironclad Compact instrument; discovery risks Compact attention, not just a local complication
**Notes**: Activate this entry (flip Status to Held, set Taken/Last collected to the day it's actually secured) the moment the party closes on either strategy already on the table — buying out the garrison quietly, or dealing with Kell directly.
→ `npcs/doreth-kell.md`, `locations/the-drowned-mill.md`

### The refugee camp

**Status**: Damaged (per `power-base.md`) — not a gold-income holding even once secured
**Notes**: This holding's value is **labor, eyes, and recruits, not coin** — `holding_status.py` intentionally has no Income/Upkeep numbers for it and will skip it in `--collect`. If it's ever actually built up, model its yield as companions/informants/`jobs-and-opportunities.md` entries, not gold — a different kind of payout than the other four. The Wend family con already spent goodwill here that would need repairing first (`npcs/alis-wend.md`).
→ `npcs/alis-wend.md`

### Fennick's debt book

**Status**: Not yet taken — party doesn't know it exists yet
**Type**: Pool — **corrected 2026-08-30, DM caught this too, same session as the Ash-Kilns fix.** A debt book is roughly forty households' worth of *existing* obligations (`npcs/fennick-orle.md`), not an operating business — it can't generate weekly income the way a trade route or a kiln can. Modeling it that way was the same mistake as the Ash-Kilns entry, just less obviously wrong. See `holding_status.py`'s Pool handling below (distinct from `Held`+Income/Upkeep's `Business` handling).
**Projected total pool**: ~150 gp (a rough estimate — ~40 households, modest sums per `items-and-loot.md`'s cost reference; the real number should be set from Fennick's actual ledger the moment the party ever sees it, not assumed)
**The leverage-vs-cash choice**: per Fennick's own file, the book's real value is *obligation as ongoing leverage* — calling in debts for cash is a one-time act that burns that leverage permanently (people stop being beholden once they've paid). Collecting the pool (fully or partially) should be played as that explicit trade-off, not free money with no cost. Holding it uncollected and using it as leverage in scenes (a favor called in, a threat, political pressure) has real value that isn't gold and isn't tracked by `holding_status.py` at all — same category as the refugee camp's non-gold value below.
**Projected risk tier**: Medium — Fennick himself is the risk; this is Ilvaneth's oldest working relationship in Gallowmere, and taking it without his cooperation costs that relationship directly
**Notes**: How it's taken (steal it, extort him, partner with him) changes the real pool size and risk at activation time — the number above is a starting default, not a locked value; adjust before flipping Status to Held if the fiction calls for it, same discipline as the Ash-Kilns correction.
→ `npcs/fennick-orle.md`

### Shestendeliath Hold — restoration

**Status**: **Held — Phase 1 active** (day 60, session 14: Ostrig Kelmar hired, `npcs/ostrig-kelmar.md`)
**Type**: Project — tracks gp invested toward each phase's total cost, not weekly income/upkeep. There is no income at all until the house is functional again. Not yet built into `holding_status.py` as an automated tracker (still just two numbers by hand — not worth a script for one holding of this type yet).
**Phase 1 cost**: 300 gp total, 2-3 weeks. **Invested so far**: 150 gp (deposit, day 60, split 75/75). **Remaining**: 150 gp due on completion, estimated ~day 74-81 — **day 65, session 15: this balance is now physically held in trust by Roskel** (Kriv gave him 300 gp total, 150 gp earmarked for this payment, 150 gp discretionary for the Hold — see `party/companions/roskel.md`), ready to pay Kelmar the moment the work is done. Not yet counted as "Invested" until it's actually paid over.
**Notes**: Full detail, all three phases, in `info/shestendeliath-restoration.md`. Phase 2 (living staff/lands, Greyholt) and Phase 3 (legal recognition, gated on Tain's attainder research) remain unstarted — this entry only tracks Phase 1's physical repairs.
→ `info/shestendeliath-restoration.md`, `npcs/ser-kethrax.md`, `npcs/ostrig-kelmar.md`, `locations/shestendeliath-hold.md`

### Armed force — the Sorrel's Hollow deserters

**Status**: Superseded — per `power-base.md`'s tracker, 11 of 12 deserters died in the original clearing; only Sergeant Roskel survived and is run as a companion (`info/companions.md`), not a holding
**Notes**: No income/upkeep entry here by design — a companion's resources are tracked on their own companion sheet, not this ledger. If the party ever rebuilds a real armed-force holding from scratch (new recruits, not Roskel), give it a fresh entry here rather than retrofitting this one.
