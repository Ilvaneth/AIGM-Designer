# Faction Renown — the party's standing with each faction, as a real number

**Why this exists**: raised session 9 (2026-08-30, DMG Ch.8's Renown mechanic) and left as a known gap while other systems were built first. Closed session 15 (2026-09-03) after a direct DM priority call — `state.md`'s Factions & Reputation table has carried nothing but prose ("Neutral"/"Hostile") for the entire campaign, while the succession war it's meant to track is the campaign's whole spine and already has real per-NPC numeric tracking (`consequences.md`'s thresholds for Sarelle, Renata, etc.). This file is the faction-level equivalent — a number, not a feeling, computed the same way `consequence_check.py` already computes threshold crossings: sum a Weight log, never hand-maintain a running total.

**What this is not**: this does **not** duplicate `consequences.md`'s "Convergence Risk" tracking (whether Sarelle has actually connected "an elf and a dragonborn" to the ambush sites). That's a separate question — *has the party been identified* — from the one this file answers — *given what the faction currently believes about whoever they think they're dealing with, how do they feel about it*. See "Interaction with Convergence Risk" under the Concordat entry below for how the two connect when Convergence Risk actually fires.

---

## The scale

A faction's Renown score is **Baseline + sum of the Weight column** in its own log below — computed fresh every time by `faction_renown_check.py`, never hand-totaled (same reasoning as `consequence_check.py`'s own docstring: a second hand-written number is a second thing that can drift).

| Score | Tier | What it means for play |
|-------|------|-------------------------|
| ≤ -8 | **Hunted** | The faction actively deploys resources to find and stop the party. No safe contact. |
| -7 to -4 | **Hostile** | Acts against the party whenever an opening exists. No fair dealing, no benefit of the doubt. |
| -3 to -1 | **Wary** | Suspicious, minimal cooperation. Worse prices/access than a stranger would get. |
| 0 | **Neutral** | No strong opinion — a stranger's welcome. The default starting point for every faction. |
| 1 to 3 | **Cordial** | Willing to deal fairly. Ordinary access, ordinary prices. |
| 4 to 7 | **Trusted** | Real access — informants share freely, better prices, minor favors granted without asking. |
| ≥ 8 | **Allied** | The faction treats the party as a genuine asset and will spend real resources to help them. |

**Baseline** is a faction's starting institutional stance before any party-specific event — most factions start at 0 (a true stranger), but a faction with a stated doctrinal default (the Cinder Choir's "hostile to unaffiliated Crown-seekers," `dm-notes.md`) starts there instead. The Weight log moves the score up or down from that baseline exactly the way `consequences.md`'s tables already work, and only logs events the faction actually knows about and can attribute to a specific relationship, cell, or (once identified) the party themselves — not private, unattributed party actions the faction has no way to connect yet.

**Tier changes are not automatically narrated as a scene.** Same rule as `campaign-clock.md`'s clock-firing discipline — a tier crossing changes prices, access, and NPC disposition (a real, integrated change, per `consequences.md`'s own litmus test), delivered the next time it's actually relevant in play, never as a DM announcement.

---

## Ashlord Concordat

**Baseline**: 0

Score reflects the Concordat's *institutional* knowledge and attitude toward whatever they currently believe about the party — not the party's own private actions the Concordat can't yet trace to them. Two convoys have been destroyed and two fragments taken (day 20, day 39), but per `consequences.md`'s "Sarelle Duskbourne — Convergence Risk" (currently 2/3, pending), Sarelle has **not yet** connected "an elf and a dragonborn" to either ambush site — so those events are deliberately **not weighted here** yet.

**Interaction with Convergence Risk**: if Convergence Risk ever crosses 3/3, apply an immediate **-6** to this score in one move (not a gradual weight) — that's the moment the Concordat's institutional knowledge actually changes from "two mysterious convoy losses" to "the elf and dragonborn we've been asking about did this." Log it as a dated Weight row same as any other event when it happens.

| Date | Event | Weight |
|------|-------|--------|
| Day 42 | Magus Orell Tain (a Concordat archivist, opposed to Sarelle's own project on scholarly grounds) struck a real, ongoing info-sharing arrangement with the party — not official Concordat policy, but a genuine inside relationship | +2 |

**Current score**: 0 + 2 = **2 (Cordial)** — reflects a real, if unofficial, foothold via Tain, with the much larger Convergence Risk exposure still hanging over it unresolved.

---

## Ironclad Compact

**Baseline**: 0

Purely transactional per `dm-notes.md` — no doctrinal stance either way, moves only on concrete dealings. The day-39 forged evidence (Ilvaneth planted a fake Compact contract fragment at the second ambush site to frame them for the attack) is a **live risk to this score**, not yet applied — if the Compact ever traces that frame-up back to the party, this should take a sharp negative hit (a faction discovering it was deliberately framed for a rival's loss is a serious grievance). Not weighted until that's confirmed in play.

| Date | Event | Weight |
|------|-------|--------|

**Current score**: 0 + 0 = **0 (Neutral)** — no logged interactions yet. Renata Kroll's declined standing-force offer (`consequences.md`, applied day 51) is a Harrowgate-local NPC consequence, not a faction-wide Compact reaction — deliberately not weighted here unless it's shown to reach Warmarshal Ashvale's own attention.

---

## Cinder Choir

**Baseline**: -4 (doctrinal default — `dm-notes.md`: "Hostile by default... treats unaffiliated Crown-seekers as heretics")

| Date | Event | Weight |
|------|-------|--------|
| Day 33 | Turned Odric Fenn (the Ash-Kilns cell leader) into an active ally without combat — traded protection/silence for cooperation and correspondence access | +3 |

**Current score**: -4 + 3 = **-1 (Wary)** — a real, deliberately incomplete recovery from doctrinal Hostile. One cell (Fenn's) is genuinely friendly; the wider Choir hierarchy (Yeva Ashwright, the Hollow Prophet, the unnamed second Karsgate cell) has no reason yet to share that view — this is the tension the score is meant to capture, not a bug to smooth over. Yeva's own "decision point" clock (`campaign-clock.md`, ~day 70) is a live risk that could move this further negative if her suspicion of Fenn resolves against him.

---

## Updating this file

Add a dated Weight row the moment a real faction-facing event resolves in play — same discipline as `consequences.md` and `campaign-clock.md`'s "write state as it happens" rule, not a session-end batch job. Run `py .claude/scripts/faction_renown_check.py ashen-crown --status` after any change to confirm the computed tier, and before any scene where faction attitude matters (pricing, access, an NPC's willingness to help) to make sure the DM's read matches the real number rather than drifting from memory.
