---
entity: chapter_<n>
type: chapter
secrecy: public
phase: P7
stamped: [act, level_band]
mirror: design/dm-only/chapters/chapter_<n>.md
---

# Chapter <n> — <title> (Act <n>, levels <lo>-<hi>)

*Plan item 10.4, 13.3. A chapter is a situation: hub-and-spoke nodes entered in any order. Only the current chapter's file is read at `load`. On entering a new act, `detail` makes the nodes concrete with everything the simulation has done up to that day.*

## Public

- **Drive:** <what the party wants or needs while this chapter runs>
- **Locations:** [[settlement_<id>]], [[region_<id>]], …
- **Intended-path sites:** [[site_<id>]] (T<n>), [[site_<id>]] (T<n>) · **Off-path sites in reach:** [[site_<id>]] (T<n>, over-tier, telegraphed)
- **Key NPCs:** [[npc_<id>]] (<why now>), …
- **XP share:** <n> of the band's budget (~70 % from intended-path sites)
- **Content mix vs the dial:** site <n> / social <n> / exploration <n> — <matches / adjusted because …>

### Nodes *(3-5)*
#### [[node_<id>]] — <name>
- **What is here:** <the situation in two sentences>
- **What is at stake:** <for whom, and what it costs to ignore>
- **Ways in:** <two or three — a rumour, an NPC, a site, a news record>
- **Sites / NPCs:** [[site_<id>]], [[npc_<id>]]
- **If the party never arrives:** <what the world does here instead, on a day — wired to a faction operation step>

#### [[node_<id>]] — …

### Beats this chapter can land
- [[beat_<id>]] — via <which node or site>

### A / B scenario for this act *(from this act's own ecosystem, item 7.6)*
- **A — if the party sides with / succeeds at <…>:** <what the act's powers do>
- **B — if the party fails / refuses / is late:** <what the act's powers do>

## Discoverable

- <what the party learns by living in this chapter for a week: which node is hot, who is watching them>

## Secret
*(written to `design/dm-only/chapters/chapter_<n>.md`)*

- <which node carries a clue, which NPC is the villain's eye here, the pre-emption the villain will try>
