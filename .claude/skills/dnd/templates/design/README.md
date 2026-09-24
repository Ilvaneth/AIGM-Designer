# `design/` templates — the shape of every bible file

*Skill data (English). Generated content is written in the campaign's narration language. Plan items 3, 9-12, 11.2, 21.H; risks 24.1 #10 and #13.*

| Template | Produces | Phase |
|---|---|---|
| `premise.md` | `design/premise.md` + `design/dm-only/premise-secret.md` | P1 |
| `cosmology.md` | `design/cosmology.md` (+ mirror) | P2 |
| `region.md` | `design/regions/<id>.md` (+ mirror), incl. the travel table | P3 |
| `settlement.md` | `design/settlements/<id>.md` (+ mirror) | P3, `detail` |
| `faction.md` | `design/factions/<id>.md` (+ mirror) | P4 |
| `npc.md` | `design/npcs/<id>.md` (+ mirror); secret NPCs exist in the mirror only | P5, `detail` |
| `site-skeleton.md` | `design/sites/<id>.md` while `status: skeleton` | P6 |
| `site-detailed.md` | the same file after `detail` (+ mirror) | P6, `detail` |
| `chapter.md` | `design/chapters/<id>.md` | P7, `detail` |
| `arc.md` | `design/arc.md` (+ mirror): beats, endings, planted hooks, seeds | P7 |
| `consequence-calculus.md` | `design/consequence-calculus.md` | P4/P7 |
| `thread.md` | `design/threads/<pc id>.md` (+ mirror) | P9 |
| `primer.md` | `design/player-primer.md` — the one file fully open to the player | P8 |
| `report.md` | `design/report.md` | P8 |

## Conventions every file follows

**Front matter.** The first lines of every file are a fenced block:

```
---
entity: npc_yesra          # the file's own registry id (mirrors carry the same id)
type: npc
secrecy: public            # the entity's tier; a mirror file says `secret`
phase: P5
status: detailed           # sites and settlements only: skeleton | detailed | played
stamped: [faction, secret_tr]   # the registry fields this file may never contradict
mirror: design/dm-only/npcs/npc_yesra.md    # the public file names its mirror; the mirror names `mirror_of`
---
```

A file that holds several entities (cosmology, arc, a settlement with its districts and anchor places) names its own entity in `entity:` and lists the rest under `covers: [god_x, era_y, …]`; a document that is no entity (the primer, the report, the consequence calculus, the generated index and travel table) says `entity: none`. Every registry entity's `file` must be a file that claims it one way or the other.

**Three headings, one split.** Prose is organised under `## Public`, `## Discoverable` and `## Secret` (item 11.1). The public file carries the first two; the `## Secret` section is written to the **dm-only mirror** at the same path under `design/dm-only/` (item 11.2). No `## Secret` heading and no secret-tier sentence may exist outside `dm-only/`; the `secrecy` validator checks headings, front matter and sentence overlap. A `secret` entity (opaque slug) has no public file at all.

**Ids inline.** Every reference to another entity is a wiki-link, `[[npc_ilme]]`, never a bare name. The DM translates id → name when narrating; the validator resolves every link; a rename touches the registry and regenerates the files the link scan lists (item 3).

**Stamped fields are repeated, not redefined.** A site's danger tier or an NPC's faction appears in the file exactly as the registry holds it; `detail` may add anything else.

**Language.** Section headings in these templates are English and are kept in the generated files as anchors (`## Public`, `## Map`, `## Room-by-room`); everything under them is in the narration language. Placeholders `<like this>` are replaced; italic guidance lines are removed.

**Tables the scripts parse.** Two tables are machine-read and must keep their columns in order: the detailed site's **room table** (`sites` module parses the `Exits` column, the `[Entrance]` / `[Payoff]` markers and the XP column) and the region's **travel table** (`travel.py` reads the six category subtables).

**Beats are consequences.** Every beat in `arc.md` carries `change_kind` from a closed list plus `state_before` / `state_after`, so "X happens" wording is caught structurally, not by an English text scan on a Turkish bible (24.1 #10).
