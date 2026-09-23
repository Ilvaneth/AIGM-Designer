# Dev Queue — Ashen Crown

*Skill-level findings from play, waiting for a development pass. Written during a session (or at `/dm:dnd end`), worked through afterwards in a fresh tab whose whole context is the tool.*

*Play tabs append here. They do not edit the skill — a hook blocks that while a session is open, on purpose: development inside a running session fills the play tab with refactoring, and the change gets written with the campaign in view instead of the tool.*

**Format:** one entry per finding. When it happened, what the tool or rule actually did, and what it should have done. Enough that a tab with no memory of the session can act on it.

---

## Open

- **Duplicate graph nodes for one person.** `npc_kavash` / `npc_solenne_kavash` and `npc_iskra` / `npc_iskra_vantrel` are the same people recorded twice. A death edge on one id left the other reading as alive; `gone --audit` now compares by name, which hides the problem rather than fixing it. Merge the pairs and add a duplicate-name check to `campaign_graph.py add-node`. *(found 2026-09-23, session 38 dev pass)*

- **Chancellery's operation is stale.** Its steps still date from the pre-Kingdom seeding (days 208/212/219, all overdue), and its objective — keep the three houses balanced — may have been overtaken by Kriv founding a Kingdom. Needs a decision: did those steps happen off-screen, are they void, or are they late? Then rewrite objective, stances and power for a Chancellery facing a Kingdom rather than refereeing three houses. *(found 2026-09-23)*

- **A faction that has never moved is not flagged.** `factions.py check` flags silence only when a faction has no operation at all; House Corr and House Sablewood sat out two whole sessions with future-dated steps and raised nothing. Consider flagging "no move on record after N days of existing", not just "no plan". *(found 2026-09-23)*

- **No LICENSE or README.** Needed only if the GitHub repo ever goes public: OGL 1.0a notice for `data/srd-5.1-yaml/` and the JSON built from it, attribution for the upstream fork (`neuralinitiative/claude-dnd-skill`), and a README describing the AIGM vision. *(noted 2026-09-23, repo is private for now)*

## Done

*(move entries here with the commit that closed them)*
