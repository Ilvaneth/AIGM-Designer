# P0 and P1 tags — the owner-approved rules and rows

*Source material for build item 7c (the claims system). Written by the development (design and review) tab with the owner, table by table, in roll order. Background: `docs/reports/tags-grouping-analysis-1.md`. A tag is changed here first, with the owner; the YAML tables follow this file. Secret and villain rows never appear here, only their counts.*

## 1. The rules (owner-approved 2026-10-02)

Four relations between rows, all read from tags, never from text: **clashes** (hard), **requires** (hard), **overrides** (hard), **fits** (soft).

1. **Claim.** A row that states a fact about the world carries it as `topic: value`. A claim is written only where the row's sentence, hook or dial effect says so literally. Theme and association are never claims.
2. **Clashes are declared one by one.** Two values of one topic do not clash by default. The closed registry lists, pair by pair, which two claims cannot stand together.
3. **Scope lives in the topic's name.** The land's rule and one people's own order are different topics; a foreign polity carries no claim. A clash may be declared across topics.
4. **Clash or override, one test.**
   - Against a *rolled row* or a *dial's value*: **clashes**. The later row leaves the pool; what was rolled first stays.
   - Against a *default* (a dial effect, a quota, a scale number, another row's hook): **overrides**. The rolled row stays (most often a trope break, also a foundation row such as "casters and the casterless") and the default is rewritten as it says.
5. **Requires.** A row that names something by "the X" is not drawn unless X was rolled.
6. **Fits.** A theme link is a weight only (×2-3), never hard. Theme lists (dragons, craft) are not turned into claims.
7. **The dials are the root.** Dial rows carry claims too. The owner may set a dial, so no roll changes it; every later roll yields to it.
8. **Inspection.**
   - Every row carries its own "reviewed" stamp; a changed or new row turns the test red.
   - A hard group that falls under five rows turns the test red. This holds for tables whose rows are not drawn again across campaigns (they run out); a table whose rows may repeat (forms, signs, limits, the tie, the time) is exempt.
   - The development tab tags the secret rows; the owner sees counts only. Topics that belong to the secret alone stay out of the owner-visible registry.

9. **One target, one owner** (added the same day). Every effect and every hook names what it sets (P4's quota, P2's calendar, the site types). The "who sets what" chart below is kept during the review; a second owner of one target is brought to the owner at once. Where two owners are really needed, how they combine is written (multiplied, or one overrides the other); an unwritten second owner turns the test red. Effects are structured and a script can scan them; hooks are prose and are caught only as the review reads them, each read hook gaining a target tag. The hooks of the P2-P8 tables stay unscanned until their floors' turn.

**A limit.** In P1 an override is data only. The code that applies it is built when the floor that reads the overridden default is bound (P4's quota at P4, the calendar at P2). Until then each override stands in the promise ledger as a promise with a due phase.

**The topic registry as the review left it (six topics):** the land's rule (hereditary, a throne, by lot, a guild council, a dragon sovereign) · nobility (exists, none) · below ground (lived in) · writing (printed) · how plentiful magic is (scarce, middling, plentiful, faded) · the form of war (by armies, by champions). The first list also held iron, crossing the border, the world's age and (deferred) the sky; no row ended up claiming any of them: the prohibitions claim nothing, and "the world is young" left the table.

## 2. The review, table by table

### P0 — scale (`dials.yaml#scale`, `scale.yaml`; approved 2026-10-02)

- **No claims.** Scale is a size, not a fact about the world. The three rows carry no claim, clash or requirement.
- **Scale is the home of overridable defaults.** Registered so far; how each is rewritten is settled at the trope-break table:

| Default | Today | Overridden by |
|---|---|---|
| the forced `state` faction (`factions.quota.state`) | 1 at every scale | "no lords; guilds rule" |

- **Owner rulings (2026-10-02), for the floors' turn:**
  - *Planes (P2):* at least one touched plane at every scale. `planes_touched` at short becomes 1 (today `[0, 1]`).
  - *Gods and churches (P2, P4; narrows errata 24.2 #11):* an epic world may hold 9-14 gods, but not every god is a great, widely worshipped power. Fallen, weak and little-followed gods are story value and are never faction-strength. One or more gods, by the kind of story, are great powers with followers and servants; those may be factions. "A church faction per god" goes.
    - Great powers (gods whose church is a faction): short 0-1 of 3-5 gods, standard 1-2 of 6-9, epic 2-4 of 9-14. The roll inside the band is weighted by the story: a ruin source of the gods family and a religious contest role push it up (the tone no longer carries a religion weight). The other gods keep a name, a domain and a story, and no faction.
    - The church factions count inside the scale's faction total. The quota's forced `religious` faction is the first great god's church, not an extra one.
    - A religious contest role's faction is a great god's church; two religious roles (two faiths, one holy place) need two great gods. The contest sets the band's lower bound, at short too.

### P0 — tone becomes the darkness dial (`dials.yaml#tone`; approved 2026-10-02)

The owner asked whether tone could go. It carried two things: a genre (horror, political, swashbuckling, cosmic), which the content mix and the foundation already carry, and a degree of darkness, which nothing else sets and which the model would otherwise always set the same way. **Ruling: tone shrinks to three values**, the old heroic, dark fantasy and grimdark: **bright · shadowed · dark** (aydınlık · gölgeli · karanlık). The loss of swashbuckling is accepted.

- **No claims.** Darkness is a mood, not a fact about the world.
- **It carries four things and nothing else:**

| Carries | Bright | Shadowed | Dark |
|---|---|---|---|
| the most reachable ending (P7) | win | pyrrhic | pyrrhic or loss |
| the sides (P4) | allies won by deed exist | mixed | no faction is clean |
| the villain's pole (P1, secret layer) | the majority holds the other pole | the majority holds the other pole | **overrides:** the majority lives by the villain's pole |
| the narration's voice | clear, encouraging | uneasy | bleak and exact |

- **Deleted with the four genre rows:** their hooks (the signature creature, the court / exchange / tribunal list, the three-region hub) and every other tone effect: site-type weights, faction-archetype weights, secret-archetype bias, pantheon bias, NPC-secret bias, the era bias, the rest-pressure modifier, the planes modifier.
- **Deleted by hand:** dark fantasy's P2 hook "the big secret is pinned to a deep-past event" (the secret is the break's true cause, and the break is recent). The surviving hooks stay: no faction is clean, complicity, the holy place that is dangerous, the ally by deed, the win's named cost.
- **For the build item:** the 22 tone weights in `foundation.yaml` (section 3 says where each goes); the voice examples go to item 15's cleanup list. Legacy births keep their old tone values untouched.

### P0 — magic (`dials.yaml#magic`; approved 2026-10-02)

- **Claim:** topic "how plentiful magic is", values `low` scarce, `medium` middling, `high` plentiful.
- **Clashes:** one candidate, settled at the ruin-source table: `plentiful` with the ruin "the age of mages" (the age of plentiful magic ended overnight).
- **Requires:** the requirements keyed on this dial already stand in the tables (fantastic landform kinds, griffons, giant insects); untouched.
- **The regulator had two owners** (the dial named who; P2's `magic.yaml#regulator` rolls who). Ruling: the dial sets only **how strict** (low: strict, licence or hunt; medium: loose; high: nearly free); P2's roll sets **who**. The dial's hook "the mage guild exists" goes; the service menu (identify, training, a price list) belongs to whoever the regulator is.
- **`high` sat in the attractor.** "Magic is infrastructure and the city bills for it" and "lamps" go. The infrastructure idea stays without the bill (owner, the same day): "the city's ward, its lift, its bridge run on magic; they are nobody's property". The P3 hook asks for at least one such settlement.
- **Note for P2:** the dial no longer guarantees a service provider (medium used to promise a guild selling identify and training), and P2's regulator table has a "nobody" row. At P2's turn "who gives the service" is answered for every regulator row.
- **Overridable defaults:** the caster share of the roster (0.08 / 0.15 / 0.30) and the regulator, both by "magic is nobility; there is no magicless noble". Sketch for the trope-break table: with that trope P2's regulator roll is not made, the regulator is the nobility, and the primer's "what a caster risks by casting in public" becomes "what a commoner risks by casting".
- **Note for P4 (rule 9):** the faction list has several sources (the scale's quota, the contest's roles, the institution signature, the great gods' churches, the magic regulator; the trope breaks joined later, six in all). Likely rule: the regulator is no new faction, it sits on an existing one.

### P0 — era (`dials.yaml#era`; approved 2026-10-02)

- **Claims:** `era_renaissance` → writing: printed (clashes with the trope break "writing is unknown"). `era_underground` → below ground: lived in (clashes with the trope break "going underground is forbidden"). Medieval, ancient and nautical carry none. The dial is the root, so in those births the trope break leaves the pool.
- **The sky (the report's open detail):** the underground era does **not** claim "no sky"; the surface is rare, not gone. The calendar note becomes "the sun and the moon are known but seldom seen; those below count time by what the deep gives" (the bells and tides go with it). The rows that touch the sky (the moon traders, night safe and day dangerous, the "sky changed" scar, the sky-watching institution) are judged one by one at their own tables; the leaning is that night-and-day clashes (it loses its meaning below) and the moon traders do not (a story). *Outcome:* "night is safe" and the night curfew clash with the underground era; the moon traders do not; the scars "the sky changed" and "the seasons broke" and the action "fell from the sky" are not drawn there; the sky-watching practice left its table; three phenomenon rules (night distances, the seasons' beast, feelings and weather) are not drawn there.
- **Nautical forces the coast.** As underground forces `land_underground`, nautical forces `land_coast` into the palette, and the spines with no sea (the oasis, the barren corridor and the like) weigh ×0.25. Otherwise "a port hub" and "a site reachable only by sea" can be impossible.
- **`economy_bias` is deleted** on all five rows: the lifeline owns P3's economy, and the lists held dropped goods (salt, light).
- **Attractor hooks:** renaissance loses the bank, the exchange, credit and the "prices with credit and letters" primer section, and keeps the printing house; ancient's "temple (also the bank)" loses the bank; ancient's "tombs and temples outnumber planned dungeons" goes (tombs only as the approved khan tombs; the ruin source owns site types). The nautical lighthouse stays.
- **Ancient's "polities are city-states unless a trope break says otherwise" goes:** the contest and the spine own the polity's shape.
- **Nautical's `content_mix_bias` goes:** the content mix is the player's order or its own roll.
- **Overridable default:** the era's equipment rule (`srd_equipment`), by "iron is sacred and rare".
- **Travel has two owners with a written combination:** the era names the vehicle (horse, ship, coach, foot), the spine names the route.
- **Note for P6:** the underground era's monster habitat filter must apply only to the palette's underground parts; the rare surface kinds keep their own creatures.

### P0 — danger (`dials.yaml#danger`; approved 2026-10-02)

Clean: no claim, clash or requirement (danger is how hard play is, not a fact about the world); every target has one owner; no hook contradicts P1. One rename: `standard` → `balanced` (dengeli), because `standard` is also a scale value.

### P0 — content mix (`dials.yaml#content_mix`; approved 2026-10-02)

- **No claims.** The mix is what is played. Some hooks speak about the world, though, and meet trope breaks:
- **Overridable defaults**, settled at the trope-break table:
  - war's node kinds (siege, muster, supply line) and its P4 hook, by "wars are fought by champions, not armies" (the trope stays; the nodes become duels, the choosing of champions, parley, raids);
  - politics' `succession` and `election` nodes, by the governance tropes (rule by lottery, no lords).
- **Politics:** the `trial` node goes (the court cluster); `court` stays as the ruler's presence and is renamed `audience`.
- **Horror and "every ruin is someone's home" (corrected the same day):** both hooks write one field, the site's attitude to intruders (one rolled value of six). The trope **overrides** P6's attitude roll: `kill` and `ignore` leave the pool; negotiate, test, capture and enslave stay (the door is answered first in all four). The trope's hook becomes "every site's inhabitants answer the door; no site's attitude is kill or ignore". Horror's "test or enslave" hook stands untouched.
- **Exploration:** "one region is unmapped" becomes "one part of the map is unmapped" (part of a region at short, a region above).
- Horror's `haunting` node stays.
- **Note for P6:** politics and war give planar sites weight 0; a planar site the foundation promises (the thin place, a planar rift) is seated first, and the mix spreads the rest.

**Working rule (2026-10-02).** No pair is left open. Two rows that can stand together get one of three written verdicts: clashes, overrides, or "no clash". "No clash" may be written only after checking that the two rows' hooks do not write the same target, and its reason is recorded. Earlier leanings given without that check (the moon traders in the underground era, item 8's five "no conflict" pairs) are not rulings; they are re-read with their hooks at their own tables.

### P1 — the spine (`foundation.yaml#spine`; approved 2026-10-02)

**What the spine carries.** A spine is geography: almost no claims. Its real work is to be the antecedent later rows require (a wall, a river, a strait); that is already data (`key_kind`, `parts`), so the requirement is written on the row that needs it, at that row's table. The owner also confirms, row by row, which spines read under the nautical era (the others weigh ×0.25 there).

**Where the "below ground: lived in" claim sits (the report's open detail; approved).** Never on the palette kind `land_underground`: caves on the map do not mean people live in them, and the forbidden-descent taboo lives best exactly there. Four sources carry it: (1) the underground era; (2) the spines whose city is below ground; (3) the layout, when the heart or a contest side is seated on `land_underground`; (4) other rows whose sentence says so, at their own tables. The trope break is rolled after the whole foundation and sees all four.

**"Two civilisations" at short (approved, reading a):** a civilisation is not a state. Inside short's one polity it is two cultures or cities, the contest's two sides at the ends. The same reading holds for the crossroads' four lands and the strait's two continents.

**Family 1, single line (approved):**

| Spine | Claim | Under nautical |
|---|---|---|
| a river from source to sea | none | reads (the delta port) |
| a great rift | none on the row; the layout decides (rule 3) when the floor is seated on `land_underground` | ×0.25 |
| passes along a range | none | ×0.25 |
| a long coastline | none | ×3 (as today) |
| a barren corridor | none | ×0.25 |

No clash, override or requirement in the family.

**Family 2, centred (approved):** no claims; all five weigh ×0.25 under nautical (the lake basin, the lone mountain, the crater of a fallen stone, the oasis and its ring, the crossroads). The lone mountain's "mouth into the mountain" is left to the layout rule. The crossroads' four lands follow reading (a). The crater presupposes a fallen stone: with the ruin sources "a stone fell from the sky" or "the celestial war" the two are one crater (approved earlier); with any other ruin it is old geography of unknown date. No clash: the two rows write different targets.

**Family 3, fragmented (approved):** no claims. Under nautical: the archipelago ×3 (as today); the lake chain ×1 (owner: a seafaring campaign on great lakes reads); the valley maze, the forest clearings and the mesa land ×0.25. The valley maze's tunnels carry no claim: people live in the valleys, not in the tunnels.

**A prohibition is not an impossibility (owner, 2026-10-02).** "Going underground is forbidden" breaks no rule when the underground exists: the player may go down anyway, someone trades in the forbidden place, someone guards it. A prohibition row does not clash with a row merely because the forbidden thing exists or is used.

- *The one limit (approved):* a prohibition needs a majority that keeps it. It clashes only where the forbidden thing is the whole land's ordinary daily life. For "going underground is forbidden" that is three cases: the underground era, a spine whose heart city is below ground, and a layout that seats the heart on `land_underground`. A contest side living below is no clash; it is the side that breaks the ban.
- *This narrows the four sources above:* source 3 is the heart only, not a contest side.
- *The same test holds for the other prohibition rows* (maps, weapons, crossing the border, a god's name; later also casting, the ruins and the night; the sacred beast left the table).
- *Effect on the audit:* its largest group (43 in 3,000 births: forbidden descent with the deep-lake lifeline, the surface-and-deep contest and the like) is no longer a contradiction.

**Family 4, layered (approved):**

| Spine | Claim | Under nautical |
|---|---|---|
| surface, middle depth and the deep | below ground: lived in (the heart is below) | ×0.25 |
| terraces | none | ×0.25 |
| two worlds, one over the other | none (magic medium or high and the thin place, as today) | ×0.25 |
| the mountain's inside and outside | below ground: lived in (the heart is below) | ×0.25 |
| above and below the sea | none | ×3 (as today) |

Notes: in "two worlds" one contest side sits on the other plane, so a region and a faction lie on another plane (for P3's and P4's turn). The undersea peoples are no registry topic; they are a fit for the sea-folk lineage and the land-and-sea contest, at those tables.

**Family 5, frontier (approved):** no claims. Under nautical: the peninsula and the strait with two continents ×3 (as today); the long wall, the climate belt and the edge of civilisation ×0.25. "Crossing the border is forbidden" does not clash with the long wall; it is proposed as a fit at the trope-break table.

**Family 6, fantastic (approved):** no claims; the magic requirements stand as today. Under nautical: the floating archipelago ×1 (owner: ships, though the sea is the sky); the titan's back, the void ring, the giant tree and the world's edge ×0.25. The titan's back shows openly that the land is a creature; any secret row that makes a secret of that clashes with it (the development tab's table, counts only). The giant tree's root land may sit on `land_underground`; the heart is in the trunk, so no claim arises.

**The spine is closed:** 30 rows, two claims, no clash, no override, no new requirement.

### P1 — the palette (`foundation.yaml#palette`; approved 2026-10-02)

- **No claims on any of the 22 kinds.** Landform kinds are geography. The magic gates and the fantastic cap stand as data and are untouched. The palette is an antecedent table: lifelines, some contests and the break's targets require its kinds, at their own tables.
- **Two fantastic kinds named an event that was never rolled** (the palette is rolled before the ruin source, so rule 5 cannot apply). Their text loses the cause: the glass desert becomes "a desert whose sand has turned to glass" (was: glazed by an old mage war), the giant's bones "a land built on and inside a giant skeleton" (was: a titan's). The ruin source says why when it brings the kind (the mage war, the dead god; they merge as today).
- **New promise (P2):** P2 writes the origin of every fantastic kind the ruin source did not bring.
- **Note for P2 and P3:** the climate must derive from the palette. At short 4-5 kinds sit in 1-2 regions and the roll can give cold lands with a desert (the climate-belt spine forces both); P2's climate roll reads no palette today.

### P1 — the ruin source (`foundation.yaml#ruin_source`; approved 2026-10-02)

- **One claim in 40 rows.** "The age of mages" (the age of plentiful magic ended overnight) carries "how plentiful magic is: faded" and clashes with `plentiful` only: it is not drawn when the magic dial is high; it stays at medium and keeps its ×2 at low. The other 39 rows tell a past event and claim nothing about today's world.
- **Requirements** (the palette kinds some rows need) stand as approved and are untouched. The table is an antecedent: institution practices, the break's remnant target and the phenomenon signature lean on it, at their tables.
- **Whose plane (new promises, P2):** four rows name another plane (the planar rift, the planar invasion, the celestial war, the elves who withdrew to another plane); only the rift had a promise. All four get: "P2 chooses this row's plane among the touched planes". **Rule for P2:** the planes the foundation names are shared so that they fit the scale's plane count; at short they are all one plane (the thin place, the ruin's plane and the "border with a plane thinned" scar).
- **The gods family and the pantheon (note for P2, no claim):** five rows say what befell a god; P2 rolls the pantheon type without reading the ruin. When the ruin is of the gods family the pantheon roll follows it. The ruin's god counts among the scale's gods and is one of the fallen, faction-less ones.
- **Earlier rulings re-read:** the elves' withdrawal against "the elves arrived last century" was a clash in the data; the trope break has since left the table, and the `conflicts_with` entry goes with it. The age of dragons against "dragons rule the lands" was ruled no conflict on 2026-09-29; under the working rule it is confirmed only after the two rows' hooks are read together at the trope-break table.
- **No clash, with reasons:** the sky ruins with the underground era (the era claims no "no sky"; their sites stand on the rare surface); "writing is unknown" with dwarf runes and merchant seals (the old people's, not today's).
- **Tone weights:** as in section 3 (horror's two rows to the content mix, heroic's two to `bright`, cosmic's three deleted).

### P1 — the lifeline (`foundation.yaml#lifeline`; approved 2026-10-02)

- **59 of 60 rows carry no tag.** The lifeline is what the land lives on; almost no row states a fact on the registry's topics. The `where` requirements stand as data.
- **The underground rows** (the deep lake, the mouth of the underground, the mushroom fields, the giant insects, the gemstones) carry no claim and do not clash with "going underground is forbidden" (the prohibition ruling). The audit's largest group closes.
- **One row claims:** "the marriage binding two kingdoms" → nobility: exists; the land's rule: hereditary. It clashes with "no lords; guilds rule" (its statement says there is no nobility) and with "rulers are drawn by lot" (a ruler by lot has no dynasty). The lifeline is rolled first, so in those births the two trope breaks leave the pool.
- **Five pairs carried to the trope-break table**, to be judged there with the trope's hooks (leanings, not rulings):

| Pair | Leaning |
|---|---|
| "iron is sacred and rare" with iron-and-coal, famous steel | no clash, a fit: the rare iron's mine is this land |
| "giants are the peasants" with the giants' peace (giants in the mountains, people on the plain) | clash: two places and two orders for one people |
| "animals speak and hold land" with the herd and hunt lifelines (yak, horse, deer) | read the hooks |
| "crossing the border is forbidden" with the pilgrim road, the caravan inn, the natural harbour, the marriage | read the hooks: a land that lives on those who cross may meet the prohibition's limit |
| "dragons rule the lands" with the dragon's protection | no clash, a fit |

*Outcome at the trope-break table:* iron is a fit with a merge rule (the lifeline's smiths are the iron priesthood); the giants row left the table in the consistency pass; the animals row became the beast-people and clashes with nothing; the border clashes with nothing; the dragon's protection is a fit.

- **Rule 9:** the four common hooks each have one owner (P3's economy and goods, P5's trades, the contest's prize, the people signature's home).
- **Note for P2:** the pilgrim road presupposes a holy place and a faith; whether the pilgrims' god must be one of the great gods is asked at P2's turn.

### P1 — the contest (`foundation.yaml#contest`; approved 2026-10-02)

**Claims: 12 of 40 rows.**

| Contest | Claim |
|---|---|
| two heirs | nobility: exists · the land's rule: hereditary |
| the empty throne, three houses | nobility: exists · the land's rule: hereditary |
| sibling rulers | the land's rule: hereditary |
| the old order and the reformers | nobility: exists (the old nobles) |
| occupier and resistance | nobility: exists (the third role, collaborating local nobles) |
| the capital and the marches | nobility: exists (the border lords) |
| lords and peasants | nobility: exists |
| the race for the treasure | the land's rule: a throne (the crown's expedition) |
| first to settle the new land | the land's rule: a throne (a kingdom's settlers) |
| humans and giants | the land's rule: a throne (the kingdom spreading over the plain) |
| humans and fey | nobility: exists, on the fourth role (a noble bargaining with the fey) |
| the company that feeds on war | war: fought by armies (two countries in an unending war) |

**Declared clash pairs:** nobility exists × "no lords; guilds rule"; hereditary × "rulers are drawn by lot"; a throne × "no lords; guilds rule". A throne does not clash with the lottery (a ruler by lot still sits a throne). War by armies × "wars are fought by champions". "No lords" leaves the pool in ten contests (about a quarter of births) and with the marriage lifeline; the lottery in three.

- **A claim on a role counts only when the scale seats that role** (humans and fey: no clash at short, a clash at standard and epic).
- **War as the escalation's last step** (about ten rows: "→ civil war", "→ kin war") is no claim. With "wars are fought by champions" the trope overrides that step (a duel of champions); settled at the trope-break table.
- **"Casters and the casterless" overrides** (a foundation row over defaults): the regulator is side A, P2's regulator roll is not made, and the strictness is strict. A rolled row comes before a default, whoever rolls it.
- **"Two branches of one people" is re-tied:** its sides were defined by their view of the break, which is rolled after the contest and may still be coming. The row becomes "the branch that calls the old fall a punishment" against "the branch that calls it an opening": the ruin source, which always exists and is old.
- **Carried to the trope-break table:** "crossing the border is forbidden" with settlers and newcomers, the foreign envoy, the road's openers and closers; "giants are the peasants" with humans and giants; "dragons rule the lands" with humans and the dragon and with the heir contests; "magic is nobility" with casters and the casterless (leaning: a fit).

**The prize and the lifeline (part 2, approved 2026-10-02).** Eight contests name a specific thing (a harbour, a pasture, a river, a craft, a mine, a road) while their prize is "the lifeline", which is rolled separately. Measured on the real roller over 3,000 births (`docs/reports/tags-grouping-analysis-1/scripts/prize_fit.py`): 18.6 % of births held such a contest with a lifeline that does not fit (16.1 % counting the main contest alone), four to five times the first audit's whole 3.5 %. This is the owner's "roll inside its heading", and the lifeline is rolled first:

| Contest | Requires one of these lifelines; ×3 when it holds |
|---|---|
| two cities wanting one harbour | natural harbour, strait crossing, shipbuilding, fish run, oyster beds, sea-folk hunt, dye sources, amber shores |
| two peoples, one pasture | yak herds, horse herds, deer migration, wheat plain, carpet weaving, leather and armour, vineyards, flax fields |
| one river, two banks | snowmelt, river flood, shared water right, river ford, flax fields, tile and ceramics, fish run |
| old craft, new craft | the craft family (8) |
| those who share and those who keep knowledge | the craft family (8) |
| the split family | the craft family (8) |
| mine owners and miners | copper mine, iron and coal, quarry, gemstones, peat bog, famous steel |
| the road's openers and closers | the passage family (9), the pilgrim road |

"Two faiths, one holy place" (prize: the remnant) gets no requirement; it weighs ×2 when the ruin source is of the gods family.

*Measured after the change (same 3,000 seeds, no cross-campaign usage modelled):* mismatches 0; no empty pool; all 40 rows still drawn; the contest pool keeps at least 27 of 40 rows (median 30); entropy 5.258 → 5.167 bits of 5.322. The eight rows fall from 1.3-3.4 % of draws each to 0.6-1.2 %; the holy-place contest rises from 72 to 108 draws; the family shares move by at most two points (open-and-close 9.4 → 7.6 %, race 16.5 → 18.2 %).

### P1 — the break (`foundation.yaml#break_target`, `#action`, `#scar`, `#time`, `#escalation_tier`; approved 2026-10-02)

- **No claims.** The break is an event. The six targets, the 21 actions and the four times carry no tag; the compatibility tables stand as approved.
- **"Coming" and the scars that are the break's product.** Under "coming" the break has not happened, and the scars read as its first signs; 16 of 18 read so. Two cannot: "a new people appeared (those the break transformed)" and "a rule of magic changed" (the phenomenon's home becomes the break, its rule drawn from the "since the break" family). When either is rolled, `time_coming` leaves the time pool (time is rolled after the scars). Under "coming" the foundation sentence writes "İlk izleri:" in place of "Yarası:".
- **The underground era and the sky** (deferred from the era dial): the scars "the sky changed" and "the seasons broke" and the action "crushed by something that fell from the sky" are not drawn in the underground era (their floors are empty there, and the heart is below). The scar pool is 16 of 18 there, the action pool 20 of 21.
- **The plane promise** ("P2 chooses this row's plane among the touched planes", shared to fit the scale) also goes on the action "merged with a plane" and the scar "the border with a plane thinned".
- **Every scar names its targets** (the generic hook "the map, peoples, polities, economy or law carry this scar" goes):

| Scar | Lands on |
|---|---|
| a new landform kind on the map | a fantastic kind in the palette (P1); its map node (P3) |
| the roads changed | the map's edges and main line (P3) |
| a poisoned or cursed belt | a region or belt (P3); a site and its creatures there (P6) |
| an unreachable region | a region marked closed (P3); the act that opens it (P7) |
| a rule of magic changed | the phenomenon signature (P1); the magic system (P2) |
| a god changed | that god in the pantheon (P2) |
| the border with a plane thinned | the touched plane (P2) |
| the sky changed | the calendar (P2) |
| the seasons broke | the climate and the calendar (P2) |
| time's flow changed in a region | a magic or plane rule (P2); that region (P3) |
| a people was displaced | a refugee settlement (P3); NPCs of that people (P5) |
| a new people appeared | the people signature (P1); NPCs of that people (P5) |
| a state fell | one polity's status (P3); a faction that wants the void (P4) |
| the creatures changed | the creature ecology (P6) |
| a new resource was born | the goods (P3); the contest's prize when the prize is "new" (P4) |
| a knowledge or craft was lost | a missing trade or good (P3); a ruin that keeps it (P6) |
| a new prohibition or taboo | a trope break from the prohibition rows (P1); the law (P3) |
| a new belief | its place in the pantheon (P2); a faction (P4) |

- **"A state fell":** new promise: the fallen state is never the polity a seated contest role rules; P3 names which state (at short, a neighbouring or an earlier one).
- **No clash, with reasons:** the two contests whose prize is "new" do not presuppose the break (the new thing is new on its own; the break only strikes where it lies; with the "new resource" scar the two merge, as in the data). "Fell from the sky" with the crater spine or the fallen-stone ruin: a second fall on the same place, different targets (geography, today's event).
- **Carried on:** the "new prohibition" scar (first or second trope break) to the trope-break table; "a new belief" and "a god changed" against the great-gods ruling to P2 and P4.

**The foundation is closed** (spine, palette, ruin source, lifeline, contest, break).

### P1 — the trope break (`trope-breaks.yaml`; approved 2026-10-03)

Every carried pair is settled here, each after reading both rows' hooks. The section follows the order of the discussion: seven of the first 33 rows left the table and six were added; "giants are the peasants" left last (section 4). The final table is 31 rows: the family tables below plus the six added rows.

**Family 1, governance and power (approved):**

| Row | Claims | Clashes | Overrides | Fits |
|---|---|---|---|---|
| rulers are drawn by lot | the land's rule: by lot | the four "hereditary" rows (two heirs; the empty throne; sibling rulers; the binding marriage); the question "birthright and merit" (in the data) | the state faction's succession rule; the ruler NPC's heir field ("next draw"); the politics mix's `succession` and `election` nodes ("the day of the draw") | |
| no lords; guilds rule | nobility: none; the land's rule: a guild council | the eight "nobility exists" rows, the three "a throne" rows, sibling rulers (hereditary) | the scale's forced state faction (archetype guild); the era's "seat of rule" anchor (a guild hall); the politics mix's `succession` node ("the choosing of masters") | ×2 with a contest whose side a or b is a guild |
| wars are fought by champions | war: by champions | the company that feeds on war | the "→ war" last escalation step of about ten contests (a challenge of champions); the war mix's node kinds (duel, the choosing of champions, parley, raid); martial factions' assets (champions) | |
| bearing arms is one class's right (prohibition) | none | nothing | | ×2 with lords and peasants |
| magic is nobility | nobility: exists | nothing outside its family | P2's regulator roll (the nobility itself); the caster share (as many as the nobles); the primer's line (what a commoner risks by casting) | ×2 with casters and the casterless: both override the regulator and say the same thing, side a is the nobility |
| dragons rule the lands | the land's rule: a dragon sovereign | the four "hereditary" rows (a mortal's crowning and a dragon sovereign answer "who rules" twice) | the state faction's leader (a dragon) | ×2 with the dragon's protection |
| crossing the border is forbidden (prohibition) | none | nothing | | ×2 the long wall; ×3 the road's openers and closers; ×2 the forbidden lands |

- *No clash, with reasons:* champions with occupier and resistance (the trope's own hook says a seize move is a challenge; one target, one answer). Dragons with "a throne" and "nobility exists" (a dragon's realm is a kingdom; its household stands beside nobles) and with the age-of-dragons ruin (its sites are dead dragons' old lairs, the trope's hook is about a living ruler's lair; the owner's ruling of 2026-09-29 stands). The border with the pilgrim road, the caravan inn and the natural harbour (the rows do not say the travellers come from beyond the border) and with the newcomers, the envoy, the returners and the occupier (people who crossed; the trope's own hooks want a faction that profits from crossing and a chapter that crosses).
- **A merge rule: "dragons rule the lands" with "humans and the dragon".** Left to the writer, one dragon would head both sides (the trope makes it the state faction's leader, the contest makes it side b). The script writes the answer: side b (the dragon and its servants) takes the hint `state` and is the sovereign and its household; side a (the league of towns) takes `resistance`; the third (the faith that bows to the dragon) and the fourth (the dragon hunters) stay. Side b may then be the institution signature's home. A test keeps the pair.
- **Note for P4 (grown):** trope breaks ask for factions too (the border two, the armed class one; more below). The faction list has six sources. Rule to build at P4: a trope's faction sits on an existing faction where it can; the scale's count is never exceeded.

**Family 2, peoples and creatures (approved 2026-10-03): six rows; two rows leave the table.**

- **Removed by the owner:** "killing a sacred beast is forbidden" (too weak for a trope break: it inverts no D&D assumption and touches one encounter; kept as a candidate for the people signature's belief traits, with the promise that the sacred animal is never the one the lifeline kills) and "humans are a minority" (a rolled minority lineage was discussed, also as a merge with "the elves arrived last century"; the owner judged that it complicates the work and adds little). The table holds 31 rows; the prohibition rows are five (maps, weapons, a god's name, going underground, crossing the border). Item 10's note "the lineage roll reads 'humans are a minority'" goes with the row. Whether either is replaced is decided when the prohibition draw is settled.

| Row | Clashes | Overrides | Fits |
|---|---|---|---|
| monsters hold treaties | nothing | P6's attitude roll on the treaty people's lairs (negotiate); the horror mix's "test or enslave" site is never one of those lairs | ×2 with the non-human treaty lifelines and the human-and-non-human contests |
| some lands' lord is a beast-person | nothing | | |
| lineage homes are inverted | nothing (the dwarf-city and elven-forest ruins tell the past) | the lineage roll's palette weights (inverted; item 10) | |

- **"Animals speak and hold land" becomes the beast-people** (owner): the landholders are a born lineage that is both beast and person (the SRD's five lycanthropes; others by the reskin rule). The row says nothing of a curse, contagion or alignment: tables assign nobody a good or evil part, later floors place the parts (the owner's reading of "no inherently evil people", confirmed). Its P3 hook reads "a beast-lord holds one part of the map" (was: one region; short has 1-2). No clash with the herd and hunt lifelines, nor with the shapeshifter contest (an open lord of a region against an unproven rumour; different targets).
- **Factions asked for:** the treaty people; the beast-lord.

**Family 3, gods and the sky (approved 2026-10-03):**

| Row | Clashes | Overrides | Fits |
|---|---|---|---|
| everyone knows the gods are mortal ancestors' spirits | the ruin "a dead god" (a spirit leaves no mountain-sized body); one secret row (the development tab's table) | P2's pantheon-type roll (ancestor gods; the field was in the data, unread) | ×2 with the ruin "the mortal who failed to become a god" |
| the moon is inhabited and trades | nothing (with the underground era: the trope writes P2's planes, the era P2's calendar; the moon ships land on the rare surface) | | ×2 when the era is nautical |
| divine magic works only on holy ground | nothing | | ×2 with "two faiths, one holy place" and the pilgrim road |
| one god's name may not be spoken (prohibition) | nothing | | ×2 with the ruins "the imprisoned god" and "the god who left" |

- The moon is a plane and joins the shared-planes rule (at short the one plane is the moon; a thin place in the palette is where the moon ships land). Its old field "biases the era roll toward nautical" is deleted: a dial is rolled before the trope and cannot be overridden.
- With the great-gods ruling: the unnamed god's hidden priests are a faction, so that god counts among the great powers.
- *Note for P3:* "each god's holy ground is a map node" needs a node of its own only for the great gods; a fallen god's holy ground may be a small shrine in a settlement.

**Family 4, where danger lies (approved 2026-10-03):**

| Row | Clashes | Overrides | Fits |
|---|---|---|---|
| night is safe, day is dangerous | the underground era (both write P2's calendar; below there is no night or day) | | |
| cities are dangerous, the wild is safe | nothing | P3's travel tables' default (the wild is dangerous): a new overridable default | ×2 with the spine "the edge of civilisation" |
| every ruin is someone's home | nothing | P6's attitude roll (`kill` and `ignore` leave; ruled with the content mix) | |
| who slays a great monster inherits its burden | nothing | | ×2 with the contest "a bounty on the monster" |
| going underground is forbidden (prohibition) | the underground era; the two spines whose heart city is below; a layout that seats the heart on `land_underground` | | ×2 when the palette holds `land_underground`; ×2 with the underground lifelines |

- "Night is safe": its P6 hook loses "the signature creature" (there is none) and reads "the ecology's apex hunts by day".
- "Every ruin is someone's home": its P5 hook "each site's householder is an NPC" would eat half the NPC budget (6-8 sites against 14-18 named NPCs at short). Only a site detailed at birth has a named householder; the others carry one sentence in the site row and are named when the site is detailed.

**The owner's test for a trope break (2026-10-03):** it inverts a D&D assumption and is felt at the table. Five more rows leave under it: "the world is young" (P1's design already does this in every campaign: a recent break, a recent secret, no ancient evil), "births are rare" (not weak but misplaced: it raises a "why" that competes with the break and the secret; it behaves like a scar), "the elves arrived last century", "the world's merchants are goblins" and "the gods want witnesses, not worship" (too narrow or too abstract). With them go: the overridable default `history.years_covered` (no overrider left), the clash with the elven-withdrawal ruin, the goblin language note. **26 rows remain:** governance 7, peoples 4, gods 4, danger 5, time 2, knowledge 4; five prohibitions.

**Family 5, time and history (approved): two rows.**

| Row | Clashes | Overrides | Fits |
|---|---|---|---|
| the old enemy won and everyone is fine | nothing | the state faction's identity (the victors) | ×3 with occupier and resistance; ×2 with the ruin "the besieged land" |
| one month a year magic does not work | nothing | the scale's weekly volatility budget (doubled in that month; slice 2) | |

- Merge rule: with "occupier and resistance" the victors are side a (the occupier); the collaborating local nobles (the third role) are the state faction under them. The trope asks for a resistance faction.
- Note for P2 and P7: the empty month must fall inside the campaign's span (40-60 days at short), or the row is never lived.

**Family 6, knowledge, matter and life (approved): four rows.**

| Row | Clashes | Overrides | Fits |
|---|---|---|---|
| iron is sacred and rare | nothing | the era's equipment rule (iron goods ×5 and licensed) | ×2 with the copper-mine lifeline, the ancient era, and the two iron lifelines |
| maps are forbidden (prohibition) | nothing | P8's player map (only the primer's named places) | ×2 when exploration is in the mix; ×2 with the race for the treasure |
| nobody can tell a direct lie | nothing so far (the mystery mix's contradicting NPCs may be mistaken; the hidden-hand contests work by evasion) | | |
| writing is unknown | the renaissance era | P6's loot (scrolls) and the wizard's spellbook (knots, memory or signs): a new overridable default | |

- Merge rule: "iron is sacred" with "iron and coal" or "famous steel": both write who works iron; the lifeline's smiths are the iron priesthood, and the land is where the world's sacred iron comes from.
- Factions asked for: the iron priesthood; the guides' guild.
- Carried on: "animals sense a lie" (phenomenon) and "a liar brings a storm" (people trait) presuppose that lying is possible; the institution's written charter, its "deciphering old writings" and the secret's "letter" trail against "writing is unknown".
- Text fixes so that rows can stand together: the monsters' "sealed" treaties become "sworn"; the moon "charter" becomes "the right to the moon trade".
- Note for play: "nobody" includes the PCs; a Deception check there is an evasion, and the primer says so.

**Six rows added by the owner (2026-10-03); the table holds 32 rows:** governance 7, peoples 4, gods 5, danger 7, time 3, knowledge 6. Eight prohibitions: weapons, the border (governance); a god's name (gods); going underground, the ruins, the night (danger); maps, magic (knowledge). A seventh candidate, "only one born a stranger may rule", was not taken.

| Row (family) | Hooks | Clashes | Overrides | Fits |
|---|---|---|---|---|
| there is no common tongue; each people speaks its own (knowledge) | P5: every NPC carries its languages, one is an interpreter. P8: which tongue is spoken where | nothing | the names table's default "the second language is the common tongue" (it is the contest's other side's) | |
| the gods live among mortals; each has a house, and its door is knocked on (gods) | P2: each great god has a house and receives petitioners; a fallen god's house is empty or shut. P3: the house is a map node. P6: a god's house is no dungeon and a god is no boss. P8: how a god is addressed | nothing in the public tables (the secret table: the development tab) | the great-gods band's lower bound (at least 1); P2's pantheon-type roll (the silent-gods and dead-gods types leave) | ×2 with a ruin of the gods family |
| one day a year no law holds (time) | P2: the calendar names the day. P4: every faction has a plan for it. P7: a beat falls on it. P8: what natives do that day | nothing | | |
| casting is forbidden; casters hide (knowledge, prohibition) | P3: the law ladder punishes casting. P4: one faction hunts casters, another shelters them. P5: caster NPCs hide what they are. P8: what befalls a caught caster | the magic dial `high` (the prohibition's limit: magic is the city's daily work there); "magic is nobility" | the magic dial's strictness (strictest); P2's regulator roll (the hunters) | ×2 at magic `low`; ×2 with casters and the casterless |
| entering the ruins is forbidden; whoever touches the remnant is a criminal (danger, prohibition) | P3: the ways to the ruins are watched. P4: one faction guards the ruins, another sells what comes out. P6: every ruin site is entered against the law, and its loot needs a fence. P8: what natives say of the ruins | only a layout that puts the remnant on the heart (the crater merge) | | ×3 with the sealed remnant; ×2 with the forbidden lands and the race for the treasure |
| going out at night is forbidden; the night is the watch's (danger, prohibition) | P3: settlements shut their gates at dusk. P4: the night watch is a faction or a faction's asset. P5: an NPC works by night against the law | the underground era (no night below) | | |

- **The ban on casting does not cover the gods' magic** (owner): priests stand outside it and are often its enforcers; wizard, sorcerer, bard and warlock PCs are criminals.
- Merge rule: "casting is forbidden" with "casters and the casterless": both override the regulator; side a (the body that holds magic) is the ban's one licensed exception and its enforcer.
- The lawless day, like the empty month, is placed inside the campaign's span.
- Factions asked for: the caster hunters and those who shelter casters; the ruins' guards and the sellers; the night watch.

**The table's structure (approved 2026-10-03; the report's two open details among them):**

- **The trope break stays step 2's first roll, after the whole foundation.** Every clash written here has the trope yield to the foundation; the people, institution and phenomenon rolls read it.
- **With the "new prohibition" scar the prohibition row is drawn first** (at short it is the one trope break), and the second comes from another family. All eight prohibitions are then on the table, and the second draw keeps more than twenty rows. That prohibition's tie is not rolled: it is the break. *Worst case to measure in the final run:* the prohibition pool can fall to four (the underground era takes two rows, magic `high` one, a remnant on the heart one).
- **The tie.** (a) When the trope break has a fit bond with a foundation piece (sacred iron with an iron lifeline, the border with the road's openers and closers, ancestor gods with the failed-apotheosis ruin), the tie is that piece and is not rolled. (b) Under "coming" the tie cannot be the break (an established order is not explained by an event still to come); the one exception is the scar's prohibition, read as the break's first sign.
- **Cleanup:** the unread `tags` field is deleted (19 values, two spelling drifts). The old unread `overrides` fields: the ancestor gods' becomes the new relation, the moon traders' is deleted. `prohibition: true` stays.

**The trope break is closed:** 31 rows (governance 7, peoples 3, gods 5, danger 7, time 3, knowledge 6) after "giants are the peasants" left in the consistency pass.

### P1 — the people signature (`signatures.yaml#people_lineage`, `#people_trait`, `#people_attitude`, item 8's uncommitted tables; approved 2026-10-03)

**Lineage (16 rows): no claims, weights only.** Today's weights stand (human base weight 4; dwarf, elf, halfling, gnome, giant-kin, sea folk, lizardfolk and centaurs by palette kind; gnome by the craft lifelines; dragonborn by the dragon rows; tiefling by the planar rows). Added fits, ×3: giant-kin with the giants' peace, humans and giants, the giants' land, giants against dragons; the fey people with the fey bargain, humans and fey, the elves' withdrawal; the sea folk with the sea-folk hunt, land and sea folk, the spine above and below the sea, the great flood; the goblin or kobold people with "monsters hold treaties". "Lineage homes are inverted" inverts the palette weights (a lineage whose home kind the palette lacks takes the ×3).

**The people's role was unmarked in the data.** The design says "when the contest has a people's role, the signature people is that role", but no role said so; a birth could make the signature people both "the giant clans in the mountains" and halflings. Ten roles are marked as a people's role (peoples who live in the land and carry no archetype hint):

| Contest | The people's role | Lineage |
|---|---|---|
| humans and giants | b: the giant clans in the mountains | giant-kin, forced |
| humans and fey | b: the forest's fey owners | the fey people, forced |
| land and sea folk | b: the sea folk | the sea folk, forced |
| surface and deep | b: the people living in the deep | dwarf, gnome, goblin or kobold ×3 |
| mine owners and miners | fourth: a deep people | dwarf, gnome, goblin or kobold ×3 |
| the race for the treasure | third: the native people's hunters | rolled |
| first to settle the new land | third: the land's native people | rolled |
| who takes the new resource first | third: the people living on the resource | rolled |
| one river, two banks | fourth: a people living in the river | rolled |
| the forbidden lands | fourth: those who live in the forbidden lands | rolled |

When the main contest has a marked role and the scale seats it (fourth roles only at standard and epic), the signature people is that role; for the first three the lineage is not rolled. Left out on purpose: peoples from outside the land (beyond the border, from the other plane), the dragon and its servants (no people), and peoples that carry an archetype hint (the institution is drawn from those roles).

- The signature people never takes the role the break destroyed (vanished, migrated, forgotten).
- When the people holds a role, the trait "they gained by the break" is drawn only if that role is the foundation's winner.

**Traits: 39 rows** (owner, option b: every row that clashed or needed a new requirement leaves, so the table carries no clash and no new requirement). Removed, 12: the childhood name; a liar brings a storm; iron is unlucky; winter sleep; two seasonal homes; never stopping; the seven-year rotation; one great building; the guest sacred for three days; the one envoy; the same dream as the herd; living on the water. Added, 1: "they hold one animal sacred; whoever kills it is cast out" (belief family; the idea removed from the trope breaks; promise: the sacred animal is never the one the lifeline kills). By family: body 7, custom 5, creature bond 6, belief 6, social order 5, relation to the break 7, place and movement 3; 16 visible and 23 behaving.

- **No claims:** a trait tells one people's own order, not the land's ("the youngest rule" does not clash with "rulers are drawn by lot").
- **Requirements** that stand in the data stay (palette kinds, the magic gate, the eight "since the break" rows not drawn under "coming").
- **Fits:** below ground by day ×2 with "night is safe"; fled the break ×3 with the scar "a people was displaced"; the first changed generation ×3 with "a new people" (in the data); the bee council ×3 with the bee forests; giant-insect homes ×3 with the giant-insect lifeline; giant birds ×3 with the griffon eyries; hunting with wolves ×2 with the deer migration; fishing with dolphins ×2 with the fish run and the oyster beds; the mountain's spirit ×2 with the mine lifelines; workshops instead of families ×2 with the craft lifelines; history danced ×2 with "writing is unknown"; haggling as an art ×2 with the attitude "merchant".
- **Re-read under the working rule:** "below ground by day" with "going underground is forbidden" is no clash (the earlier item-8 recommendation is withdrawn: different targets, and the people is the one that breaks the ban).

**Attitude to strangers (6 rows):** no tags.

### P1 — the institution signature (`signatures.yaml#institution_form`, `#institution_practice`, `#institution_sign`, `#institution_power`, item 8's uncommitted tables; approved 2026-10-03)

**The role's archetype is the heading (approved).** The institution is a contest role, and that role's faction is the institution itself; yet only the form read the role (as a weight), while the practice, the sign and the power were rolled blind (a smugglers' role could draw "midwives"; a regent's house "monster hunters"). Not measurable on real code (item 10's rolls do not exist yet); by count, a practice fits a given archetype in about a third of draws. Ruling: the form, the practice and the power are drawn only from the rows under the role's archetype (state, religious, martial, guild, trade, scholarly, criminal, resistance). Every practice and power row carries the archetypes it fits; the form rows' `hints` turn from a weight into a requirement. No heading falls under five rows.

**Practices: 33 rows** (approved 2026-10-03; seven removed, four reworded).

| Family | Practice | Archetypes it fits |
|---|---|---|
| guard | they hold the spine's key place | state, martial, guild |
| guard | they keep the one road | state, martial, guild |
| guard | they hold the remnant's gate | religious, martial, scholarly |
| carry | a travelling theatre carrying news and history in plays | guild, resistance, criminal |
| carry | they pilot dangerous waters and roads | guild, trade, criminal |
| carry | they carry messages by giant birds or fast horses | state, guild, trade |
| carry | they organise the caravans | trade, guild |
| carry | the river's or the strait's ferrymen | guild, trade, criminal |
| make | they repair the remnant's works and keep them running | guild, scholarly, state |
| make | they cast golems and machines | guild, scholarly, martial |
| make | they build ships and bridges | guild, trade |
| know | they draw and keep maps | scholarly, guild, state, criminal |
| know | they study the remnant | scholarly, religious |
| know | they seek what was lost | scholarly, religious |
| know | they keep what is dying (seeds, species, songs) | scholarly, religious, resistance |
| care | they are healers | religious, guild, scholarly, resistance |
| care | they keep the granaries that feed the people in famine | state, religious, guild |
| care | they are midwives | religious, guild |
| care | they heal herds and mounts | guild, religious |
| war | they are monster hunters | martial, guild, resistance |
| war | the riders of the border and its forts | martial, state |
| war | champions who settle disputes in single combat | martial, state |
| war | a free company | martial, trade, criminal |
| war | they hunt dragons | martial |
| trade | they hold the monopoly of one good | trade, guild, state |
| trade | they sell what comes out of the remnant | trade, criminal, scholarly |
| trade | the sole sellers of the lifeline's product | trade, guild |
| trade | a foreign merchant house trading with far lands | trade |
| trade | a half-secret smugglers' union | criminal, trade |
| faith | they perform the rite that keeps the lifeline alive | religious |
| faith | they lead pilgrims to the holy place | religious, trade |
| faith | they guard the holy place | religious, martial |
| faith | they interpret the break and worship it | religious, resistance |

Rows per heading: guild 18, religious 12, trade 12, martial 10, state 9, scholarly 9, criminal 7, resistance 5.

- **Removed (owner: a row that names something never rolled, or that clashes with a dial, leaves):** the wall's builders and keepers; worship in the departed god's empty temples; guarding the herds and migration routes; the lifeline's unique craft; raising the break's orphans; mending the break's wound; watching the sky.
- **Reworded so that no rule is needed:** the champions ("in place of war" announced the champions trope without it); the monopoly ("by royal charter" presupposed a throne and writing); studying the remnant gives "the deciphering of old knowledge" (was: old writings); "the old kingdom's works" becomes "the remnant's works".
- **Two clashes:** "they hold the remnant's gate" is not drawn in the contest "the sealed remnant" (side b already holds it); "they guard the holy place" is not drawn in "two faiths, one holy place".
- **Fits, ×3:** the pilots with "maps are forbidden" (the trope's guides' guild is the institution); the border riders with "crossing the border is forbidden"; selling the remnant's finds and holding its gate with "entering the ruins is forbidden"; the champions with "wars are fought by champions"; the pilgrim guides with the pilgrim road; worshipping the break with the scar "a new belief" (in the data). The mapmakers do not clash with "maps are forbidden" (the prohibition ruling: secret or licensed mapmakers).

- **Four practices name their own form** and the form is then not rolled: the travelling theatre (a travelling company), the free company (a company), the smugglers' union (a secret society), the foreign merchant house (a house). The other 29 roll the form under the archetype.

**Forms (14 rows), by archetype (approved 2026-10-03).** The old `hints` were too narrow under a hard heading (a scholarly institution would always be a school):

| Form | Archetypes |
|---|---|
| order | religious, martial, scholarly |
| guild | guild, trade |
| company | martial |
| house | state, guild, trade, criminal |
| council | state |
| league | trade, guild, criminal |
| school | scholarly |
| brotherhood | resistance, religious, guild, martial, criminal |
| cloister | religious, scholarly |
| travelling company | guild, trade, criminal, resistance |
| secret society | criminal, scholarly, resistance |
| privileged company (was: chartered company) | trade |
| confederacy | state, martial, resistance |
| militia | martial, resistance |

Each heading holds three to five forms. Forms may repeat across campaigns, so rule 8's floor of five does not apply (it is for tables that run out). "Chartered" presupposed a written charter (a clash with "writing is unknown"); the row becomes the privileged company, a privilege being grantable by word.

**Power sources (10 rows), by archetype (approved):**

| Power | Archetypes |
|---|---|
| monopoly | trade, guild, state |
| place: they hold the key place or the remnant | state, martial, religious, scholarly |
| knowledge: they know the road, the map or a secret | scholarly, criminal, guild, trade, resistance |
| arms | martial, state, criminal, resistance |
| the people's love | resistance, religious, guild |
| sanctity | religious |
| treasure | trade, guild, state, criminal |
| a bond with a creature | martial, religious, scholarly, resistance |
| privilege: a right granted by the rulers (was: a charter, a written right from a ruler) | guild, trade, scholarly, martial |
| fear | criminal, martial, state |

**Signs: 13 rows, rolled freely, no tags** (owner, option b). Removed, 5, each of which clashed with something: they carry no weapons (a war practice, the arms power); they do not marry (the form "house"); they may own no land (the power "place"); they kneel to no ruler (the state archetype); they do not travel by night (the underground era). Signs may repeat, so thirteen do not run out; "they speak only their own language" still needs three languages (standard and epic), which leaves twelve at short.

**The institution signature is closed:** practices 33, forms 14, signs 13, powers 10; the role's archetype is the heading of the form, the practice and the power.

### P1 — the phenomenon signature (`signatures.yaml#phenomenon_rule`, `#phenomenon_sign`, `#phenomenon_limit`, `#phenomenon_user`, item 8's uncommitted tables; approved 2026-10-03)

- **The rule is already drawn under a heading** (the ruin source's two or three rule families; family 8 alone with the "a rule of magic changed" scar), so no rule clashes with the ruin.
- **The user roll made sense for six rules only.** Every rule carries its kind, and the user is rolled for the usable ones alone:

| Kind | Count | Who uses it |
|---|---|---|
| a rule of spellcasting ("every spell leaves an echo", "casting ages the caster") | 15 | whoever casts; not rolled |
| something that happens by itself ("time runs differently near the remnant", "shadows move on their own") | 19 | no one; not rolled |
| usable | 6 | rolled |

The six usable rules: mirrors are doors; a true name commands; a rightly drawn sign is a small spell; one people's tongue is the tongue of magic (the user is the signature people); metal wakes in a master's hand; a community shares its wounds (the user is the signature people or the institution). The lock between the three signatures stays where it means something.

- **Four rules stay with a rule each** (owner): "beasts sense a lie" clashes with "nobody can tell a direct lie"; "distances change at night", "the seasons are bound to a beast" and "a strong feeling changes the weather" share one rule, not drawn in the underground era (no night, season or weather below). All 40 rules stay.
- **Limits: 8 rows** (four removed): "the remnant's matter absorbs it" (the same sentence as a rule), "it works only underground" (against the night, weather and season rules), "once triggered it waits a day" (meaningless for standing rules), "it ends a day's road from the remnant" (a second centre beside "magic is strong near the break's target"). The limits may repeat.
- **Signs (16 rows):** sensory marks, no tags.
- **No clash, with reasons:** "a rightly drawn sign is a small spell" with "writing is unknown" (a sign is not writing; the trope writes the library and the written clue, the rule the magic system); the spell rules with "casting is forbidden".
- **Fits, ×2:** "every spell leaves an echo" with "casting is forbidden" (the hunters follow the trace); "one people's tongue is the tongue of magic" with "there is no common tongue"; the limit "iron cuts it" with "iron is sacred and rare".
- **Cleanup:** the true-name rule's weight on the removed childhood-name trait goes.
- **Note for P2:** under "one month a year magic does not work", a phenomenon whose rule is a spell rule stops in that month too.

**The phenomenon signature is closed:** rules 40, signs 16, limits 8, users 8.

### P1 — the question (`tensions.yaml`; approved 2026-10-03)

- **No claims** (the poles are abstract). One clash, in the data and approved: "birthright and merit" with "rulers are drawn by lot".
- **No clash, with reasons:** "faith and proof" with "the gods live among mortals" (the poles do not name the gods; the writer builds the question in the contest's terms); "loyalty and truth", "secrecy and openness" with "nobody can tell a direct lie" (sharper there); "law and conscience" with the lawless day (a fit).
- **The contest's family becomes the heading** (owner; replaces the ×3 weight approved on 2026-09-29): a question is drawn only from the rows of its contest's family; at epic each contest draws its own. By the weights about half of the births drew a question from outside the contest's family: no contradiction, but a strained premise (two cities wanting one harbour made to carry "flesh and spirit").
- **Two narrow families grow from five to eight** by giving existing rows one more family (no new row): "one thing, two hands" gains winning and being right, ambition and contentment, justice and peace; "the hidden hand" gains power and self, the one and the many, security and freedom. The other six families hold seven to eleven.
- **Rule 9:** two owners write P7's endings on different aspects: the question gives their content (the possible answers), the darkness dial says which is most reachable.

**Every built table of P0 and P1 is reviewed.** Not yet written, so not yet reviewed: the secret and villain tables (item 9; built by the development tab, counts only to the owner; the notes gathered for them: the titan's back, the ancestor gods, the gods among mortals, the letter trail against "writing is unknown", the darkness dial's majority pole, the chooser and villain equivalence) and the names tables (item 11; notes: no common tongue, the language count).

### The whole-P1 measurement of today's tables (2026-10-03)

`docs/reports/tags-grouping-analysis-1/scripts/whole_p1.py`, 3,000 births: the real foundation roller, the identity rolls as `p1sim.py` approximates them (item 10 is not built), today's tables (the removed rows still in them). It counts births that hold something this review ruled out.

| What | Births | Share |
|---|---|---|
| 1. a literal clash the review ruled | 784 | 26.1 % |
| 2. a row drawn outside its heading, or naming something never rolled | 1,118 | 37.3 % |
| 1 or 2 | 1,610 | 53.7 % |
| 3. the institution's practice against its role's archetype (the role is the script's approximation) | 2,105 | 70.2 % |
| 1, 2 or 3 | 2,593 | 86.4 % |
| a user roll with no meaning (not a contradiction) | 2,079 | 69.3 % |
| a question outside its contest's family (not a contradiction; the script does not apply today's ×3 weight, with it about half) | 2,360 | 78.7 % |

The largest single causes: prize against lifeline 18.6 %; the tie "the break" under "coming" 9.0 %; "coming" with a product scar 5.0 %; "their herds" with no herd lifeline 5.0 %; the people's role against the lineage 4.9 %; nomads on a fixed lifeline 4.3 %; the underground era with night, season and weather rows 3.2 % and with the sky scars or action 2.9 %; the departed god's temples without that ruin 2.5 %; nautical without a coast 2.2 %. The first audit had counted 3.5 %, on four literal groups.

**What the figure does and does not say.** Each counted case is removed by a rule approved above, so on these cases the rate after the change is zero by construction. It is no proof that nothing else exists: the review read every row against the topics found, and a pair nobody noticed is not counted. The proof on the built system is the coding tab's many-seeds test (item 10), which must hold every pair and heading recorded in this file.

### Who sets what (rule 9)

| Target | Owner | Note |
|---|---|---|
| site-type weights (P6) | content mix; era adds types | tone's weights deleted |
| faction-archetype weights (P4) | era | tone's weights deleted |
| planes touched (P2) | scale (at least 1), magic's modifier | tone's modifier deleted |
| rest pressure | danger | tone's modifier deleted |
| the content mix | the dial itself | era nautical's bias deleted |
| P3's economy and goods | the lifeline | the era's `economy_bias` deleted |
| the polity's shape | the contest and the spine | ancient's city-state hook deleted |
| travel | the era (vehicle) and the spine (route) | combined, no overlap |
| a site's attitude to intruders (P6) | P6's attitude roll | "every ruin is someone's home" narrows the pool; horror's hook asks for test or enslave |
| where sites stand (P6) | the spine (the key place and the ends each hold or border a site) | shared without overlap: the ruin source says which sites, the content mix which types weigh, the danger dial how many are over tier |
| P2's history | the ruin source (one age), the break (a dated event), the palette (the origin of a fantastic kind the ruin did not bring), the scale (the numbers) | |
| which plane | P2 chooses, among the touched planes, for the thin place, the ruin's plane and the scar; shared to fit the scale's count | |
| the palette's kinds | the spine (forces), the era (forces: underground, nautical), the ruin source (one kind, on top of the count), a scar (one kind, counted toward the cap), the roll for the rest | every combination is written |
| P7's endings | the question (their content), darkness (which is most reachable) | two aspects |
| how clean the sides are (P4), the voice | darkness | |
| the villain's pole | P1's secret roll; darkness `dark` overrides the majority's side | |
| the magic regulator: who | P2's regulator roll | the magic dial no longer names it. Three rows override it: "magic is nobility" (the nobility), the contest "casters and the casterless" (side a), "casting is forbidden" (the hunters). Their pairs are written: nobility with the contest agree (side a is the nobility); the ban with the contest agree (side a is the licensed exception); nobility with the ban clash |
| the magic regulator: how strict; the caster share; the loot multiplier; the wild-magic gate | magic | |
| P4's faction list | scale quota, contest roles, institution, great gods' churches, regulator, trope breaks | six sources: to settle at P4; the scale's count is never exceeded |

| P2's pantheon type | P2's roll | the ruin source's gods family leads it; "the gods are ancestors" sets it; "the gods live among mortals" narrows it |
| the great gods' count | the scale's band | raised by a religious contest role, by "the gods live among mortals" (at least 1), by the unnamed god's hidden priests |
| the lineage roll's weights | the palette and the foundation's rows | "lineage homes are inverted" inverts them; a marked people's role forces the lineage |
| the institution's form, practice and power | the role's archetype (the heading) | four practices name their form |
| the question | the contest's family (the heading) | |
| the tie | the roll | a fit bond with a foundation piece sets it; the scar's prohibition is tied to the break |

Words in two closed lists: `standard` was both a scale and a danger value; the danger value is renamed `balanced`.

## 3. Held for the build (owner, 2026-10-02: nothing more goes to the coding tab until P1's review ends)

The plan may still change while the review runs, so the review's results are collected here and turned into build instructions only once P1 is closed. Build item 7a (the arbiter's three faults) was handed over before this ruling and stands.

**The P0 changes that need no tag system (drafted as "7b", not sent):** everything under the "P0 — …" headings above except the claims and the overrides. Choices made while drafting, to confirm when the instruction is written:
- the dial keeps its key `tone`; values `bright`, `shadowed`, `dark`; blank-roll weights 2, 3, 1 (the old rows' weights);
- the 22 tone weights in `foundation.yaml`: heroic (2 ruin sources) → `bright`; horror (2 ruin sources) → the content mix `horror`; political (15 contests) → the content mix `politics`; cosmic (3) deleted;
- legacy births load with their old dial values; a new birth refuses them;
- `danger_standard` → `danger_balanced`, while `effects.state_difficulty` keeps its value (play reads it);
- item 8's uncommitted `signatures.yaml` names no tone value (an earlier count of ten was a search that matched the word "stone").

**For item 7c (the claims system):** the claims, clash pairs, overrides and overridable defaults recorded above. `trope-breaks.yaml` carries two old unread `overrides` fields: the ancestor gods' (the pantheon type) becomes the new relation, the moon traders' (an era bias) is deleted.

**For 7b, replacing the draft's rule of thumb:** which spines weigh ×0.25 under nautical is the owner-approved list in the spine section (×3: the long coast, the archipelago, above and below the sea, the peninsula, the strait; ×1: the river to the sea, the lake chain, the floating archipelago; ×0.25: the other 22).

**Build item 7a, audited 2026-10-03 (the development tab read the four scripts' diff and ran the suite: 469 tests, exit code 0).** All five parts do what was asked: the public die is counted over the rows not publicly excluded and the real die goes to dm-only; a phase stands only on the phases before it; a table's own `avoid_used` wins over the caller's argument; the usage fallback drops one kind at a time (family wait, used elsewhere, row wait, the pair last) and names what it dropped; `families_distinct` is read by a general path as a constraint. Notes for later items:
- *The header rule was read narrowly:* for `file#sub` only the sub-table's own header binds; a file-level header does not speak for its sub-tables. P2-P6 make many `avoid=False` calls on sub-tables whose file header says `avoid_used: true` (pantheon, calendar, history, regions, settlements, factions, antagonists); that contradiction is settled at those phases' turn.
- *The same fault sat in the time table* (four rows, exhausted by the fifth birth); the same fix closed it.
- *One gap, from the instruction's own wording:* the command-line `design_dice.py roll` no longer sees the earlier rolls of its own phase and attempt, so hand rolls inside one phase are not filtered against each other (only `families_distinct` reads them). No script or prompt calls that command, the preroll's `Roller` keeps its own stack, so no birth is affected; the fix (add the same phase's current-attempt rows to the command's context) was asked for with the commit.

## 4. The consistency pass (2026-10-03)

The development tab re-read this file whole after the review. The file follows the order of the discussion, so earlier sections held statements that later rulings replaced; those were brought in line (the removed trope breaks' leftovers, the topic registry, the tone weights' count, the faction sources' count, the outcomes of the pairs that had been carried forward, the chart's missing owners, rule 4's and rule 8's wording). No two standing rulings were found to contradict each other. Checked by count: the trope break families (7 + 4 + 5 + 7 + 3 + 6 = 32), the eight prohibitions, the rows that clash with "no lords" (eight nobility rows, three throne rows, sibling rulers), the four hereditary rows, the phenomenon kinds (15 + 19 + 6 = 40), the practices per archetype.

Four small points were open; the owner ruled on them the same day (below).
1. *A pair without a verdict:* the practice "they hunt dragons or giants" with "giants are the peasants" (the institution would hunt the land's farm labourers).
2. *A text fix of the kind already approved:* the courier practice gives the party "letters"; with "writing is unknown" it should give "messages".
3. *A pair without a written verdict, covered by the prohibition ruling:* "going out at night is forbidden" with the trait "below ground by day, on the surface by night" (the people is the one that breaks the ban).
4. *Rule 8's scope:* the floor of five was worded for every hard group, but the time (four rows), the tie (four) and the forms were never meant by it; the wording now exempts tables whose rows may repeat.

**The owner's rulings on the four points:**
1. "Giants are the peasants" leaves the trope breaks (31 rows; the peoples family holds three: monsters hold treaties, the beast-people, lineage homes inverted). Its clash with the giants' peace and with humans and giants, its fit with the giants' land and the giant-kin lineage's weight on it go with it. The practice becomes "they hunt dragons" (the giants leave its sentence and its weight list). With "dragons rule the lands" the dragon hunters do not clash: a faction that wants the sovereign dead is a story, and in the merge with "humans and the dragon" they are the fourth role.
2. The courier practice gives "messages", not "letters".
3. "Going out at night is forbidden" with the trait "below ground by day, on the surface by night": no clash (the prohibition ruling; the people is the one that breaks the ban).
4. Rule 8's floor of five holds only for tables whose rows are not drawn again across campaigns.

**Where P1 stands.** The plan of P0 and P1 is closed for every table that exists. P1 itself closes only when the coding tab has built it: 7b (the P0 dials), 7c (the claims system and the table changes of this file), 8 (the signature tables, redone to this file), 9 (the secret and villain tables), 10 (step 2's rolls), 11 (the names), 12 (the promise ledger), 13 (the door), 14 (the writer, the critics, the card), 15 (the attractor cleanup), then the test birth that runs P1 alone.

**Build item 7b, audited 2026-10-03 (the dials' diff read, the suite run on the working tree: 471 tests, exit code 0).** The six parts do what was asked. Accepted as the coding tab reported them: `arc.yaml`'s `node_court` renamed `node_audience` and `node_trial` deleted (the mix's node names are bound to those rows by a test); `planes.yaml`'s `touch_bias` cleaned of the deleted tone ids; a neutral hook on the two rows the deletions left hookless (`magic_medium`: "the primer states how loosely casting is watched"; `era_ancient`: "few roads: the river routes and the wilderness carry the travel"); no validator read `churches_as_factions`. One correction asked with the commit: the three tone rows' `label` fields in English (Bright, Shadowed, Dark) like every other dial row, the Turkish names in a `tr` field.

**Build item 7c-1, audited 2026-10-03 (the registry, the context class, the roller and the foundation script read; the suite run: 494 tests, exit code 0).** The mechanism does what `docs/p1-build-7c.md` asks: six topics and seven clash pairs in a closed registry; a rolled row's claims and the dial rows' claims enter the context as tokens; a seated role's claims and the two layout tokens are kept on records of their own so that later phases find them; a token set by a secret row stays secret, and one also set publicly is public; the condition grammar gained `all` and `any`; `conflicting_pairs` expands tokens; overrides are data with their two tests. Accepted as reported: `claims.yaml` is a registry file outside the table list; the tokens live beside the rolled rows, not among them. **The stamp:** the coding tab writes the stamps before its summary so that the suite can be green, and commits them only after the audit; a committed stamp therefore means "audited", and `git diff` on `reviewed.json` is the list of rows a commit changed. The floor's first report (900 seeds): no table whose rows are not drawn again falls under five (the lifeline's smallest pool is 12, the trope break's 24, the contest's 29).

**Build item 7c-2, audited 2026-10-03 (the foundation tables' diff read line by line against `docs/p1-build-7c.md`; the suite run: 502 tests, exit code 0).** Every change of part 7c-2 is in the data as specified: the two palette texts and the P2 origin promise; the age of mages' claim and the four plane promises; the marriage's two claims; the twelve contest claims (two of them on a role); the eight prize requirements with their ×3 and the holy-place contest's ×2; the ten people's roles with their lineage data; the re-tied "two branches"; the casters' two overrides; `time_coming` against the two product scars; the underground era's two scars and one action; the eighteen scars' named targets; "İlk izleri:" in the sentence. Measured by the coding tab and accepted: mismatches between prize and lifeline 0 in 3,000 seeds, all 40 contests still drawn; the first contest's pool never under 27; epic's second contest's pool never under 23 (the older "another family" rule, not the new requirements); 56 of 341 stamps changed. The "new prohibition" scar's floors are now P1 and P3 (the table of this file gave it no P2 target). Note for 7c-3: `designer.py`'s P2 preroll already applies the ancestor gods' `pantheon_type` override; it keeps doing so, read from the new list form.

**Build item 7c-3, audited 2026-10-03 (the rebuilt trope-break table read row by row against `docs/p1-build-7c.md`, the question's and the roller's diff read; the suite run: 516 tests, exit code 0).** The table holds 31 rows in the six families, eight prohibitions; the eight removed rows are gone from the committed data and the six new rows carry the approved sentences and hooks; claims, further clashes, overrides, weights and the five merge rules are on the rows as specified; the tie "the break" conflicts with `time_coming`; six questions gained a family; P2's preroll still applies the one existing override (the ancestor gods' pantheon type), read from the list form. Accepted as reported: two `combine` lines the specification had not written, both in the sense of this file's rulings ("the treaty people's lairs are negotiate; every other site's pool loses kill and ignore"; "the ban's strictest rule holds; side a enforces it"). Measured by the coding tab: the trope-break pool's smallest size is 24 at the first draw and 17 at the second; no clash pair stands together over 1,620 seeds; all 31 rows are drawn. **For item 10:** the prohibition rows' smallest pool is 3 of 8 at a second draw whose first row came from the danger family; the ruling "the scar's prohibition is drawn first" avoids that case, and its own worst case (four) is to be measured there.

**Build item 8, audited 2026-10-03 (the eleven sub-tables read by script against `docs/p1-build-8.md`; the suite run: 543 tests, exit code 0).** The tables match the specification: 16 lineages with the four added weights; 39 traits (7, 5, 6, 6, 5, 7, 3 by family; 16 visible, 23 behaving) with the sacred-animal row and the eleven weights; 14 forms, 33 practices and 10 powers under the eight archetypes (practices per archetype 18, 12, 12, 10, 9, 9, 7, 5); the two practice clashes, the seven ×3 weights, the four practices that name their form, the six text changes; 13 signs; 40 rules by kind (15 spell, 6 usable, 19 self) with the two fixed users, the one clash and the three rules kept out of the underground era; 8 limits; no claim on any signature row; 203 new stamps. Accepted as reported: the English labels the coding tab wrote for the renamed rows; the era condition written as the list of the four other eras, with a test that turns red when an era is added; `rule_true_names` losing the note that named the removed trait; `practice_seek_the_lost` keeping its ×3 with the "lost knowledge" scar. The stash's stale note in the plan file is discarded; the development tab writes the plan's delivery notes for 7a to 8. **For item 11 (names):** the form words that sit too close ("Company", "Trading Company", "Travelling company"; "Guild" and "League" beside the Turkish "birlik" of two rows; "Order", "Brotherhood", "Cloister").

**The whole-P1 measurement repeated after builds 7a to 8 (2026-10-03, the same 3,000 seeds, `whole_p1.py`; commit `63a6c9f`).**

| What | Before | After builds 7a to 8 |
|---|---|---|
| 1. a literal clash the review ruled | 26.1 % | 0 |
| 2. a row outside its heading, or naming something never rolled | 37.3 % | 4.1 % |
| 1 or 2 | 53.7 % | 4.1 % |
| 3. the institution's practice against its role's archetype | 70.2 % | 69.6 % |
| a user roll with no meaning | 69.3 % | 69.1 % |
| a question outside its contest's family | 78.7 % | 77.1 % |

What is left is exactly what item 10 builds, the rolls of step 2: the people's role forcing the lineage (the 4.1 %), the archetype heading of the institution, the user rolled for usable rules only, the question drawn under its contest's family. The data for all four is in the tables; the script still rolls them the old way. The measurement is repeated after item 10.

**The secret and villain tables: how the owner is assured without seeing a row (approved 2026-10-03).** (a) Seven criteria the owner set, which the rows are written and audited against (`docs/p1-build-9.md` section 1). (b) A burn sample: three archetypes and three villain shapes written to the tables' standard, shown to the owner, never in the tables. (c) The development tab reads every row and reports counts per criterion. (d) The owner may ask one-sentence questions answered only yes, no, or "not answerable without a spoiler".

**Build item 9, audited 2026-10-03 (every row of the secret and villain sub-tables read against the seven criteria; the suite run: 569 tests, exit code 0). Counts only; the row-level notes are in `docs/reports/item9-audit-SPOILER.md`, which the owner does not open.**

| Sub-table | Rows | Pass every criterion | To correct |
|---|---|---|---|
| secret: archetype | 26 | 25 | 1 (one word of the attractor in a clue shape) |
| secret: chooser | 6 | 6 | 0 |
| secret: twist | 15 | 15 | 0 |
| secret: trail | 10 | 10 | 0 |
| villain: visibility | 5 | 5 | 0 |
| villain: shape (usable) | 16 | 14 | 2 (the defensible reason is not stated in the row) |
| villain: origin (usable) | 9 | 9 | 0 |
| villain: tie to the break | 6 | 6 | 0 |

Every archetype is told as the break's true cause with a person who chose it, and carries three clue stages; no row protects the party. Two conflicts with public rows are added (a secret the foundation already half shows). The visibility table may repeat (the approved rule is that the shape and origin pair is not drawn again). The coding tab's own decisions are accepted (four archetypes removed, not two; one twist replaced; hashed stamp keys for the secret tables). The burn sample (`docs/reports/item9-burn-sample.md`: three archetypes, three shapes, in no table) is for the owner to read.

**The burn sample was read and its level approved by the owner (2026-10-03);** build item 9 is committed after the five corrections. The specification of item 10 (step 2's rolls, two commits) is `docs/p1-build-10.md`.

**Build item 10a, audited 2026-10-03 (`design_identity.py` read line by line; 586 tests green; committed as `db19171` after two corrections).** The public identity's rolls follow `docs/p1-build-10.md`. Two owner rulings came out of the audit, both with no exception left:
- *The institution always has a home.* In 1 of 2,700 births the break destroyed the contest's only role with an archetype. The break may no longer strike the last seated role that can house the institution (a constraint beside the winner's rule, in the foundation); the placeholder that rolled an archetype outside the contest is gone, and a missing home stops the preroll.
- *The form always sits under the role's archetype.* Two practices named a form their own archetype list was wider than (66 of 2,700 births). `practice_free_company` now fits `martial` only and `practice_smugglers_union` `criminal` only (practices per archetype: trade 10, criminal 6; the others unchanged). No exemption remains in the test.
The floor over 2,700 seeds: no table whose rows are not drawn again under five (the resistance archetype's practices 5, a ruin source's rules 5, epic's second question 5, the prohibition rows at the scar's draw 5).

**Build item 10b, audited 2026-10-03 (`roll_secret` read; the suite run).** The secret (archetype, chooser, twist, trail, and the role when the chooser is a contest role) and the villain (visibility, shape, origin, tie, pole) are rolled secretly in P1; P4 reads the three moved rolls; the shape and origin pair is recorded hashed and not drawn again; the chooser is the villain exactly when the tie is "caused it". Accepted as reported: a legacy birth whose P1 predates this keeps rolling the three in P4; the chooser's role may be the role the break destroyed (a role that chose its own end is a story).

**The whole-P1 measurement on the real rolls (2026-10-03, `whole_p1_v2.py`, 3,000 births; it calls `design_foundation` and `design_identity` as the preroll does).**

| What | Tables as they stood | After builds 7a to 8 | After build 10 |
|---|---|---|---|
| a literal clash | 26.1 % | 0 | 0 |
| a row outside its heading (prize, the people's role) | 37.3 % | 4.1 % | 0 |
| the institution against its role's archetype | 70.2 % | 69.6 % | 0 |
| a user against the rule's kind | 69.3 % | 69.1 % | 0 |
| a question outside its contest's family | 78.7 % | 77.1 % | 0 |
| the chooser and the villain's tie disagreeing | not measured | not measured | 0 |
| any of them | 86.4 % (the first three) | 71.1 % | 0 |

The measured cases do occur in the sample (in 600 births: a forced-lineage role 28 times, a prize contest 47, a usable rule 92, a form named by its practice 40, the "new prohibition" scar 77), so the zeros are not an empty result. As before, this counts what the review found and ruled; it is no proof that nothing else exists.

## 5. Where the work stands (2026-10-03, the end of this review tab's session)

**Delivered, audited and pushed:** build items 1-7, 6b, 7a, 7b, 7c (three commits), 8, 9, 10a, 10b (HEAD `4bb5cef` plus the documents). The plan's 24.3 carries their delivery notes; errata 24.2 #26 says this file holds over the plan's items 2 and 25.

**Next: item 11, the names.** Its tables are approved by the owner like the others (full row lists, in Turkish, in small parts). What is already decided (errata 24.2 #20 and #25; `docs/p1-foundation-rows.md` section 16; the notes of `docs/reports/tags-grouping-analysis-1.md` section 8):
- 20-24 sound families (10 today), mutated by script, never by the writer; a lexicon of 300-400 roots (115 today) with neutral glosses; patterns without examples ("Court of…", "…Assize" and the month pattern "…tide" go); languages by scale (short 2, standard and epic 3); roots rolled, weighted by the foundation's domains, 8-10 per language at short, 12 at standard, 15 at epic.
- The name pool is built at the end of P1's rolls: 3-5 candidates for every place, institution, signature, month and day name; persons and gods keep coming from `design_names.py`. The writer invents no proper noun; the door refuses one outside the pools (item 13).
- Notes this review gathered for it: "there is no common tongue" overrides the default "the second language is the common tongue" (it is the contest's other side's); the institution sign "they speak only their own language" needs three languages; the institution's form words sit too close ("Company", "Trading Company", "Travelling company"; "Guild" and "League"; "Order", "Brotherhood", "Cloister") and are settled here; the institution's form word comes from the rolled form (`design.json#identity.institution.form`).

**Then:** 12 (the promise ledger: every override and every hook of a rolled row becomes a promise with a due phase; the secret's three clue stages mapped to a one-act campaign), 13 (the door), 14 (the writer's prompt, the critics, the card; the prompt does not yet name the archetype's `cause` field or the chooser), 15 (the attractor cleanup), then the test birth that runs P1 alone (the Opus tab; this tab only writes its instructions). The notes for 12-15 are in `docs/reports/tags-grouping-analysis-1.md` section 8.

**Notes left for the later floors** (each recorded at its table above): P2 (the planes shared to fit the scale; the pantheon type following a gods-family ruin; the great gods' band and its raisers; the origin of fantastic landform kinds; the climate from the palette; who gives the magic services under each regulator; the empty month and the lawless day inside the campaign's span), P3 (a region and a faction on another plane; holy grounds as nodes; which state fell), P4 (the faction list's six sources and the rule "never above the scale's count"; the `cult` archetype; eight attractor rows in P4's own tables), P6 (the habitat filter under the underground era; planar sites seated before the mix; a site's attitude pool under two trope breaks).

**Working arrangement** (the owner's standing orders): the coding tab commits one item after this tab's audit and never pushes; this tab pushes after each audited commit and commits its own documents by path; instructions for the coding tab go in plain-text code blocks, items named in words ("Kalem 11"); no secret or villain row is shown to the owner, only counts (row-level notes go to a file marked SPOILER); no model-run test in this tab; the full suite takes about eleven minutes (run it in the background).

## 6. The audits of builds 13a onward (the specifications of 2026-10-04)

**Build item 13a, audited 2026-10-04 (every changed row's old Turkish read against its new English, 519 rows: foundation 245, signatures 203, trope breaks 35, questions 33, dials 3; the door, the manifest setting, the foundation's rendering, the cards and the common preamble read; the suite run on the working tree: 609 tests, exit code 0).** The translation is faithful: no change of meaning in the trope breaks or the signatures. Four corrections asked before the commit, all in `foundation.yaml`:
- `act_fell_from_sky`: the three forms say "buried under"; the owner's approved wording is "crushed by something that fell from the sky".
- `contest_land_sea_folk`, role b: "the merfolk"; the approved name is "the sea folk", merfolk only in the note.
- `contest_shapeshifter`: the name "the one in another guise" becomes "the shapeshifter", as its label.
- `life_iron_coal`: the text reads the Turkish as charcoal (rightly: its weak point is the forests used up for it); the label follows: "Iron and charcoal".

Accepted as reported: the writing language is a fixed manifest field (`write_lang`), a birth without it is a legacy birth; the door names the field or the file and the line, never the text; the foundation's rendering is a labelled list and each action keeps three English forms; the suffix rules live in `data/play/turkish-suffixing.yaml`; the two command words `onay` and `devam` stay Turkish (the owner types them); the registry's field names still end in `_tr` until build 14a renames them; the Turkish left in the later floors' prompts, templates and renderers is listed in the coding tab's summary for those floors' turn. The secret and villain tables held no Turkish and were not touched. For build 16a: the note of `scar_new_belief` still says "not the forbidden evil cult"; it goes with that row of `forbidden.yaml`.

**Build item 13a committed as `c08d437` with the four corrections (checked in the commit) and pushed.**

**Build item 16a, audited 2026-10-04 (every changed line of the tables, prompts, templates and scripts read; the suite run on the working tree: 611 tests, exit code 0).** `forbidden.yaml` holds one row, `forbidden_inherently_evil_races`, unchanged; the twelve defaults are gone with their structural checks, lexical patterns and `allowed_via` lists, and no reference to them is left. The freed values are ordinary rows with hooks of their own: three villain shapes, one origin, the religious villain faction, two opening scenes, two plot engines, three thread truths, one cult doctrine. The development tab read the five freed villain rows against the criteria of build 9: all five pass (each has a reason a decent person could defend; none spares the party); counts only to the owner. The P1 rubric asks the one remaining question (is any people evil by birth; fiends and the undead are creatures). Accepted as reported: three barred values stay as their tables' own mechanical rules, each worded so (`fracture_none`, as the specification asked; `cultdoc_unspecified`, which the specification had freed: an unspecified doctrine is no theme and gives P4 nothing to build; `verb_find_out_who`, never one of the twelve); a few conflicts on the freed shapes and origin for pairings that cannot describe one villain (their list goes into 16c's file); the structural checks of the old list had never been applied in code. Measured by the coding tab: over 1,800 seeds every shape and origin is drawn, no conflicting set, no empty pool. The remaining row's Turkish lexical pattern is build 13b's.

**Build item 16a committed as `af54309` and pushed.**

**Build item 16b, audited 2026-10-04 (the thirty-one rows read in the tables against `docs/p1-build-16.md`, every change on an existing row read, `whole_p1_v2.py` run on the working tree, the suite run: 621 tests, exit code 0).** The thirty-one rows stand with the ids, families, labels, statements and roles the owner approved; none of the seven removed rows entered. The rulings are in the data: ten weights (three of them on existing rows: the sealed remnant, the order that splits, the beast-person lord), three merges (the dead with the monsters' treaties, the dark lord with "the enemy won", the dark lord's contest with his fall), one conflict (`break_magic_sold` with the spring that ran dry), the requirements (sea or lake or underground for the deep minds, coast or island for the pirates, magic at medium or high for the magic trade); nothing was written for a pair ruled "no clash". The whole-P1 measurement over 3,000 births: no conflicting pair, no heading miss, no institution against its archetype, no user against its rule's kind, no question outside its family, no chooser and tie disagreeing. Accepted as reported:
- the lifeline's id is `life_enchanters` (the specification's `lifeline_enchanters` was the development tab's slip; corrected there);
- the relic's prize is conditional (`prize_with`: the remnant with the sundered relic, else new), one line in `design_foundation.py`;
- the eight lists that mean "a lifeline of the craft family" took the new lifeline;
- the ruling "the elemental lord's contest is weighed by its treaty like the others" has no row to stand on (the treaty lifeline was removed at the review) and wrote nothing;
- `break_magic_sold`'s claim `magic: plentiful` also clashes with the age of mages (`magic: faded`) through the registry's existing pair: a literal contradiction the pairs table had not listed; told to the owner;
- the new contests carry no content-mix weight (36 of the old 40 do); no ruling asked for one.
The technical fields the coding tab wrote (remnant kinds, sites, rule families, texts, escalation steps, hooks) are listed in `docs/reports/item16b-technical-fields.md`; the hints and prizes are the development tab's proposals, unchanged. Measured by the coding tab over 2,700 seeds: every new row drawn, no empty pool, the floors hold (the smallest five).

**Build item 16b committed as `80a4bc4` and pushed. The owner then approved dial weights for the eleven new contests (`docs/p1-build-16.md`, Part 16d): horror, mystery and exploration call a contest for the first time.**

**Build item 16c, audited 2026-10-04 (every added secret and villain row read against the seven criteria; the public-figure rule read in `design_identity.py`; the suite run on the working tree: 622 tests, exit code 0). Counts only; the row-level notes are in `docs/reports/item16c-audit-SPOILER.md`, which the owner does not open.**

| Sub-table | Before | Added | After | Pass every criterion | To correct |
|---|---|---|---|---|---|
| secret: archetype | 26 | 5 | 31 | 4 | 1 (its first clue is an ordinary sight beside two public rows: two conflicts to add) |
| villain: shape | 19 | 2 | 21 | 2 | 0 |
| villain: origin | 10 | 3 | 13 | 2 | 1 (the living person's choice is not stated in the row) |

The fifth criterion is read as the owner's ruling of 2026-10-04 changed it: the dead and the undead are general material; courts, money and debt, light as a fuel, hush and bells, tides and salt stay out. The rule for the public dark lord does what the specification asked: with the contest rolled and the villain's visibility the known one, the villain is that public figure (the shape set, not rolled; its pole that role's when the contest is the main one); with any other visibility the villain is someone else; without the contest nothing changes. Accepted as reported: the attractor word list of build 9's test lost the seven words of the dead. Measured by the coding tab over 1,800 seeds: no empty pool, no conflicting set, the chooser and tie equivalence holds, no secret row in a public record, the archetype pool's smallest size 25.

**Build item 16c committed as `ed8d6ba` with the two corrections (checked in the commit: the archetype's two conflicts, the origin's choice in its hook) and pushed.**

**Build item 16d, audited 2026-10-04 (the eleven contests' weights compared by script with the approved table of `docs/p1-build-16.md`; the suite run on the working tree: 623 tests, exit code 0).** The eleven rows carry exactly the approved weights (horror 2, mystery 2, exploration 1, war 3, politics 1, the nautical era for the pirates, none for the elemental lord), written as the old rows write theirs; the relic's and the dark lord's weights with their ruins stand beside the new ones. One old test that pinned the rows weighted by horror and by politics was brought up to date. Item 16 is complete with this commit.

**Build item 16d committed as `bed5e0d` and pushed. Item 16 is complete.**

**Build item 11a, audited 2026-10-04 (the seventeen bags and the 505 roots compared by script with the approved lists; the patterns, the word lists, the generator and the prompt line read; the 3,069 sample names read; the suite run on the working tree: 642 tests, exit code 0).** The bags' openings, middles and endings, groups and flags are identical to `docs/p1-build-11-bags.md`; every root's position and tags are identical to `docs/p1-build-11-lexicon.md`, with no root added; 22 settlement tails, 22 tags with what calls each; the patterns are structured rows without examples and none of the deleted patterns is left; the generator's join and shape rules are the trial's. Two corrections asked before the commit (`docs/p1-build-11-filters.md`, "Added at the audit of build 11a"):
- 75 names the samples showed are added to `real_given` (the northern, eastern and antique bags spell real names of their languages; also Arwen, Asgard, Ilmatar, Morana, Europe);
- the list is split: `plain_words` (the plain-words block and eight more: among them Koran, Naval, Males, and a word that reads obscene) applies to every bag, the rustic one too; `real_given` keeps the names and stays off for a `real_ok` bag.

Accepted as reported: the need is 86 names per language (`scale.yaml`: the epic band's top plus the spares), not the specification's round 100, and every bag gives it on 200 seeds; the worst overlap between two births on one bag is 15 of 86; bag parts are quoted in the YAML ("On", "No" and "Yes" read as booleans otherwise); the old "no final -gh" check is dropped (the owner approved the old-isle bag with its two -gh endings); `rules.turkish_suffixing` stays where build 13a moved it; the acceptance checks run cheap first, with the same results. Two limits to remember: asked for 200 names, three bags stop short (airy 117, liquid coast 118, sibilant 142), which matters only if play adds many persons to one language; and the northern, eastern and antique bags will keep spelling real names the list does not hold. The coding tab's context was full after this part; a new coding tab takes over with `docs/reports/coding-tab-handoff.md`.

**Build item 11a committed as `17ab33a` with its two corrections (checked: `real_given` 599, `plain_words` 118) and pushed. A new coding tab took over.**

**Build item 11b, audited 2026-10-04 (the three sample pools read, one per scale; the door's, the conductor's and the prompts' diff read; the name module's rolls read by their rules in `naming.yaml#rules.draw`; the suite run on the working tree: 667 tests, exit code 0).** The machine does what `docs/p1-build-11.md` asks: the naming rolls stand at the end of P1; the languages by owner with both overrides; the old tongue in every campaign from a group of its own; roots 10, 18, 24 with the half share, the head floor and no sharing; the calendar's own roots and one month pattern; four candidates for each signature; stocks per language; a separate secret stock that no public output prints, with the door's mirror rule; the owner's reroll; `naming.json` written by the script and taken out of the writer's tasks. Read in the samples: the languages tell apart, the called half follows the world, the old tongue's sites stand apart from the living names. Seven corrections asked before the commit (`docs/p1-build-11.md`, "Corrections from the audit of build 11b"): eight roots that do not end a place name become heads only; a region word follows the palette; a building's root is not its word; the one-root ship is a creature or one of five words; sixteen more adjectives; the god epithets in the singular with "the" (the owner's ruling, decision 46); two small rules for the calendar. Measured by the coding tab: the called pool fell short in 6 of 6,313 language draws; every stock holds three times the scale's need; the whole-P1 measurement over 3,000 births reports zeros. A limit: about a quarter of the free half's roots carry a land tag the palette does not call (889 sea roots in 531 landlocked births), as decision 33 allows.

**Build item 11b committed as `f47caa2` with the seven corrections and pushed (2026-10-04).** On the way the coding tab reverted the uncommitted `naming.yaml` by mistake and rewrote it; the development tab therefore compared the committed table again with the approved lists (seventeen bags and 505 roots identical, the eight roots heads only, sixteen adjectives, ten non-creatures, the lists 599 / 115 / 175), read the reprinted pools (the corrections show: no Coast in a landlocked world, creature ships, epithets in the singular) and ran the suite on the commit: 674 tests, exit code 0. Two more small rules came out of the second reading and stand as part 11c of `docs/p1-build-11.md` (`inn` a head only; no season root under the `fall` month pattern). **The owner's standing permission (2026-10-04):** after the development tab's first audit says "accepted", the coding tab applies the corrections and commits on a green suite without asking again; the development tab checks every commit before it pushes.

**Build item 11c committed as `b51bd66` (its two rules checked in the data) and pushed.**

**Build item 12a, audited 2026-10-05 (`design_promises.py` read whole, the validator's, the card's, the conductor's, the prompt's and the documents' diff read; the suite run on the working tree: 695 tests, exit code 0).** The ledger does what `docs/p1-build-12.md` asks: a public list in `design.json#promises` and a secret one in dm-only; the sources (every hook of every row rolled in P0 and P1 with its tables' common hooks, the overrides at their default's phase with the combined sentence where two rolled rows have one, what the layout seated, the scars' floors, the escalation's steps, the break's event, opening and news, the stubs and placements a merge reserves, the action that must be made concrete, the secret's three clue stages by level range); one promise for one due phase and one sentence; `EXPECTED_UNTIL` gone and each validator module and the two codes naming their first phase; the card's three count lines; a rerun reopening what the phase judged; no ledger for a legacy birth. Accepted as reported:
- **the public ledger is a function of the public rolls alone:** a promise goes to the secret ledger only when its source row was rolled secretly or its sentence carries a secret row's id; a label's ordinary words do not move it. The specification's "a promise whose text names a secret roll is secret" would have let a gap in the public ledger tell what was rolled; the coding tab's reading closes that, and a test rebuilds the public ledger without the secret rolls over 2,400 births;
- the row's English `name` where the specification asked for a Turkish field (build 13a);
- two due aliases of `claims.yaml` (`names` is P1, `slice2` is play); a sixth script rule for the P0 hooks (all of them say the arc skeleton comes from the scale's row, which the rule counts); `override_applied` for the three overrides a roll applies itself;
- the third clue never opens before the second's first level;
- `dm_only.pinned: {god, event}` on the premise row, the one field the ledger reads for P2's two placements.
Measured by the coding tab over 2,400 seeds: 107 to 135 promises per birth by scale (18 of them secret in every birth), 25 to 36 with more than one source. **For 12b:** the script rules are defined and tested but not yet run in the flow, so 12a's card shows every promise open; `clue_unplaced` closes no gate today (the finding stands on P1's premise row, which P6's gate does not own), which the `clue_placed` promise will; about ten promises due at P1 are facts the rolls already apply and could be script rules. **Where "act" still decides:** the P1 writer prompt and the card's secret abstract (build 14), the P6 skeleton prompt (P6's turn), the validator's `clue_order` check (to follow the stages' level ranges in 12b).

**Build item 12a committed as `634b8b2` and pushed.**

**Build item 12b, audited 2026-10-05 (the gate's, the validator's, the conductor's, the prompt renderer's and the critic schema's diff read; the hooks that gained a rule read in the tables; the suite run on the working tree: 705 tests, exit code 0).** Delivery and inspection do what `docs/p1-build-12.md` asks: the block "Promises due at this phase" reaches the phase's writer (a single writer, or the skeleton agent of a fan-out phase) and its phase critic; the secret promises are given as a command, only to prompts that already read dm-only; the phase critic returns an id, a verdict and a slug per promise, and a return with free text is refused; the script rules run at `phase check`; a due script promise not kept closes the gate (`promise`), a due critic promise without a verdict closes it (`promise_unjudged`), a critic's "not kept" leaves it open and is listed on the card; a secret promise is an id and a count everywhere; the owner's waiver and the listing; the Opus protocol's stop S7. The four notes of the 12a audit are met: the rules run in the flow; `clue_order` reads the stages' level ranges in a birth with a ledger; seven kinds of P1 promise the rolls already apply are script rules bound in the tables by a `check:` field on the hook (a median of six per birth, all kept over 2,400 seeds), four to five public promises stay with the P1 critic; no verdict, waiver or card line tells a secret promise. Two corrections asked before the commit (the specification's last section): the mystery mix's clue hook is due at P6, where a clue's place is set, not at P1 (the coding tab found it and left the row for the audit); `promise list --dm-only` is refused while the read guard is armed. Accepted as reported: the rule binding lives in the data; the stub kinds the orphan gate only warns about are judged and listed without closing the gate; `promise_unjudged` looks at the promises due at that phase alone; a waiver applies to a not-kept promise only; `validator` and `play` promises close no phase's gate. For the later floors: three writers (P3's skeleton, P8's, P9's first session) read no dm-only, so a secret promise due there is only judged.

**Build item 12b committed as `d82d0f6` with its two corrections (checked in the commit) and pushed.**

**Build item 13b, audited 2026-10-05 (`design_door.py` read whole; the registry hookup, the prompt line and the tables' diff read; the public rows' own capitalised words and the closed list printed; the suite run on the working tree: 715 tests, exit code 0).** P1's door does what `docs/p1-build-13.md` asks: the three signatures carry their slot, home and rolled rows as the identity record holds them, the trope breaks are the rolled ones with their ties, the premise the rolled question ids; the foundation, the identity, the ledger's script-built part and `naming.json` are sealed by hash, and a changed seal refuses every unit; the final set, public and secret with tokens, is rechecked for conflicts, a secret pair said only as "a conflict in the secret layer"; a signature's name is one of its four candidates, a person's or god's from its stock, a place-like name from its stocks or built by pattern 6 or 7, a secret entity's from the secret stock and never the other way; in public prose a capitalised word that opens nothing must be pooled, registered or on the closed list, and the dm-only prose is scanned against both pools with only a count for the conductor; each signature needs one `appears` note for every floor its tables promised, and the notes enter the ledger; no secret row's id or sentence and no secret-stock name in a public text; the premise's abstract is the archetype's class alone; what the conductor may not read goes to a dm-only door log. One correction asked before the commit: `Hells`, `Nine Hells` and `Abyss` join the closed list (two approved rows name them in their own statements), with a test that no public row's own text carries a capitalised word the door would refuse. Limits recorded in the specification: a word that opens a sentence is not read; titles before a name wait for P5; faction, item and plane names have no pool yet.

**Build item 13b committed as `5dc49dd` with its correction (checked) and pushed.**

**Build item 14a, audited 2026-10-05 (the new `P1.premise.md` and the premise template read whole; the field-name helper, the prompt selection and the skill line read; the suite run on the working tree: 722 tests, exit code 0).** The writer's prompt does what `docs/p1-build-14.md` asks: it stands on the script's records (foundation, identity, naming and candidates, the promises due at P1), reads the secret layer itself and takes the clue stages' level ranges and the secret names by command; it no longer carries the earlier-campaigns block (the two critic prompts keep it); the secret is told as the break's true cause from the archetype's `cause` field with the chooser; the clues go by stage with the kind of place only; the list "what you never do" gives the five refusals with their reason; every sentence added one by one since build 11 is in the new text (`naming.json`, `dm_only.pinned`, `slot` / `home` / `rolled` / `appears`, `row` / `tie`, `secret_class_tr`); the template's headings pass the door's prose scan. Accepted as reported: the old prompt lives on as `P1.premise.legacy.md` for a birth without a foundation (the specification's test asked that such a birth render as before); the roll list left the prompt; `clues[]` is `{n, levels, kind, place_kind, how}`; `text_field` reads the three renamed fields and still loads the old names. The prompt file grew from 594 to 1,033 words and renders at about 3,400 for a standard birth, 1,043 of them the name stocks: whether that length costs the writer attention only the test birth can show. **For 14b:** five fields of the premise row still end in `_tr` with English content; the card's secret line still counts clues per act.

**Build item 14a committed as `af3fca2` and pushed.**

**Build item 14b, audited 2026-10-05 (the three script-built P1 cards read, the rubrics' diff read; the suite run on the working tree: 730 tests, exit code 0).** The six P1 rubrics stand as `docs/p1-build-14.md` lists them and none says "rerun"; the critics' P1 prompts open with the craft-only note (the rolled rows are given, a failed rubric is a rewrite on the same rolls, only the owner rerolls); the card is in the layout the owner approved, in English, with no roll label, row id or candidate list, the secret as its archetype's class and "the villain: rolled, hidden", the secret promises as three counts, and four moves that exist; the premise row's last `_tr` names took English names through `text_field`; the card's leak scan reads the secret stock and the secret rows' ids and sentences. Three corrections asked before the commit (the specification's last section): the language line prints labels, not owner keys; "not run yet" where the door or the validator has not run; the rubric "differs from the earlier campaigns" does not fault a rolled row or a general theme that recurs (errata #31). Accepted as reported: the gate line under CHECKS, the promise id on a not-kept line, "open N" in the due line, the sixth rubric's question as two sentences, the new card for P1 alone.

**Builds 14b (`0155af6`) and 15 (`ad8809b`) checked and pushed (2026-10-05).** *Correction of this note:* the development tab pushed them before reading its own suite's result, and wrote "736 tests, exit code 0" here without having it. That run ended with three errors, none of them the commits': it ran in the shared working tree while the coding tab was already editing the critics' prompts for part 14c (the three errors are unfilled placeholders of the half-edited `critic.md` and `phase_critic.md`). The coding tab's own run on the two commits was green (736, exit code 0). The development tab now runs its suite in a separate clean checkout of the commit it audits (a git worktree), reads the result before it writes or pushes anything, and the clean run's result is recorded below. 14b's three corrections are in the reprinted card and the rubric (the language labels, "not run yet", the narrowed "differs from the earlier campaigns"). Build 15 is small and as specified: one leftover deleted (a half sentence in the question table's header comment that named the two dropped pole pairs), `age_lanterns` renamed `age_of_thing` with an alias so that an older birth and an older usage record still read, no history row removed; left alone as the rows' own substance: "court" in the kingdom of the dead, the name parts "Bell" and "Lamp" of two bags. The coding tab reported an example list in that history row's hint; the owner took its first word out (part 14c).

**The owner's questions of 2026-10-05 and what came of them.** (1) "Is the full suite P0 to P1 run end to end?": the pieces are tested and several chains run together, but nothing walks the road after the writer in one piece; item 17 (the dry walk of P1, `docs/p1-build-17.md`) is built before the test birth. (2) "Did we bring what the critics criticise up to date?": the six P1 rubrics, yes; the critics' prompts and the rubrics of every phase, no. Part 14c (`docs/p1-build-14.md`): no `rerun` from a P1 critic, the critics are told what was rolled, the naming rubric becomes the second net behind the door, and the cliché rubric goes (owner: it asks every entity to prove it is not its genre default, the same taste errata #31 set aside).

**Part 14c, a light audit (2026-10-05, this tab's context nearly full).** Checked by search in the working tree: `rubric_cliche` is in no data, prompt or script file; the naming rubric carries the new question; the history hint reads "(roads, walls, mills)"; the two critic prompts take their verdict options and "what to read" from placeholders the renderer fills. The coding tab's suite on it: 742 tests, exit code 0. **Not done by the development tab: reading the diff line by line and its own suite run.** Accepted for commit on that basis; the next development tab runs the suite on the commit in the clean checkout before it pushes.

## 7. Where the work stands (2026-10-05, the end of this development tab's session)

**Pushed (origin/main `686d52f` plus this note):** 13a, 16a-d, 11a-c, 12a, 12b, 13b, 14a, 14b, 15. Every one audited as section 6 says. For 14b and 15 the development tab's own clean suite run was still running when this was written: its log is `%TEMP%\claude\C--Users-armag-Desktop-Campaign-Designer\3b6ceab2-943b-45fb-b0c9-07a308000151\scratchpad\suite15-clean2.log` (last lines: the count and `exit=`); if that file is gone or red, run the suite again on `ad8809b`.

**In the working tree, not pushed:**
- part 14c (`docs/p1-build-14.md`, "Part 14c"): written, the coding tab's suite green; to be committed by the outgoing coding tab as `Plan item 25, build 14c: the critics know the rolls`; then the suite in the clean checkout, then the push;
- item 17 (`docs/p1-build-17.md`): `tests/test_p1_dry_walk.py` is **written and has never been run** (untracked). Running it, fixing every fault it finds in the product, and the summary of those faults are open. It is model-free; an Opus coding tab can do it.

**Then:** the instructions for the test birth that runs P1 alone (the Opus tab; `docs/tuning-births.md` and `docs/dry-run-and-playtest.md` are the protocols, stop S7 is new). The development tab writes them, never runs them. After that birth: bind P2's rolls at P2's turn, and so on floor by floor (plan item 25, "Floors" #11).

**How this tab audits now (learned the hard way on 2026-10-05):**
- the suite runs in a **separate clean checkout** of the commit, never in the working tree the coding tab is editing: `git worktree add --detach .runtime/wt-audit <commit>` (`.runtime/` is git-ignored; the checkout must not live under the system temp directory, where the skill's own `used.json` guard misreads it), then `py .claude/skills/dnd/scripts/run_tests.py` inside it, in the background (about 25 minutes, 742 tests);
- **the result is read before anything is written or pushed**; a command that reads the log is never chained with the commit or the push. On 2026-10-05 this tab pushed 14b and 15 and wrote "exit code 0" without having read a red log; the red was the coding tab's half-edited files, not the commits, but the statement was false and is corrected in section 6;
- secret and villain rows: counts to the owner, row-level notes in a file named `*-SPOILER.md`, a warning before any tool call that prints them.

**Open notes for the later floors** (each recorded where it arose): titles before a pooled name wait for P5; faction, item and plane names have no pool yet; three writers (P3's skeleton, P8's, P9's first session) read no dm-only, so a secret promise due there is only judged; the P6 skeleton prompt still places clues "in act order"; three bags stop short of 200 names (airy 117, liquid coast 118, sibilant 142); the northern, eastern and antique bags keep spelling real names; the P2-P9 prompts, the player-file renderer and their tables still hold Turkish (the list is in the coding tab's 13a summary); other entity types keep their `_tr` field names until their floors.

**The clean run on builds 14b and 15 (read 2026-10-05, after section 7 was written):** in the clean checkout `.runtime/wt-audit` at `ad8809b`: 736 tests, OK, exit code 0, five skipped. The five are tests that read the archived test births under `campaigns/_test-*`: those folders are git-ignored, so a clean checkout does not hold them; the coding tab's run in the main working tree, which does, had them green. A clean run therefore proves the code and the tables, and the archived-birth pack is proved only by a run in the main tree (when the coding tab is idle) or by copying those folders into the checkout. The first step "a" of the next development tab is done by this note.

**Build item 14c, audited 2026-10-05 by the next development tab (the commit's diff read line by line; the suite run in the clean checkout `.runtime/wt-audit` at `a908859`: 742 tests, OK, exit code 0, five skipped, the archived-birth tests as above).** `b534149` does what Part 14c asks: for P1 of a birth with a foundation and a seal the entity critic and the phase critic are offered `pass`, `fix` and `note` with the reason, the return schema's enums lose `rerun`, and `design_approval.py critique` refuses a P1 return that says `rerun` (a legacy birth and the other phases keep the three verdicts); both critics are told to read `design.json#foundation` and `#identity` and the candidates, dm-only critics the secret identity record (`dice-log.json#identity`); the phase critic's P1 line names what it reads, P1 having no skeleton; the naming rubric carries the new question; `rubric_cliche` is in no table, prompt, script, test or the skill; the history hint reads "(roads, walls, mills)". Three small notes, none blocking: `scripted_p1` has two definitions (`design_approval.py`: foundation, identity, promises and seal present; `design_prompts.py`: foundation and seal), which agree on every birth today; one assertion in `test_p1_critics.py` (the earlier-campaigns block) tests a string against itself and proves nothing; the plan's risk register still said the cliché judgement lives in `rubrics.yaml` (marked withdrawn by this tab). *Order of events:* the outgoing development tab pushed `a908859`, which carried `b534149`, before this clean run; the run, read after, is green, so nothing pushed is red.

**The instructions for the test birth that runs P1 alone** are `docs/p1-test-birth-1.md` (written 2026-10-05; the Opus tab runs them after item 17 is audited, on the owner's word).

**Build item 17, audited 2026-10-05 (the product's diff read line by line, the test read; the suite run in the clean checkout `.runtime/wt-audit` at `4402177`: 753 tests, OK, exit code 0, five skipped, the archived-birth tests as above).** The dry walk does what `docs/p1-build-17.md` asks: at each scale it walks new, preroll, begin, a stand-in writer built from the records, merge through the door, check, stand-in critics, card, approve and a second campaign on the same `used.json`; the eight wrong turns each fail where they should (about 15 seconds a walk, 105 for the file). **One fault in the product, fixed:** the card said "door: not run yet" after a passing door, because the merge that records the critics' returns alone deletes `merge.report.json` (birth 2, 3.1) and runs no door; each merge the door ran now records `phases.<PN>.door = {at, units, refused}`, `rerun` clears it, the card reads it, and a legacy birth without the field still reads the file. The coding tab's first attempt (keeping the report) broke the test that pins 3.1 and was reverted. Accepted as reported: the prompt points the writer at `naming.json#candidates` and does not print the candidates (as 14a was audited; 17's "carries the candidates" was loosely worded); the test's assertions print no secret row, secret-stock name or prompt text when they fail. Two notes: `rerun` does not clear the validator's last result, so before `check` a rerun's card can show the previous attempt's count (the test birth's protocol always runs `check` before the card); the test backs up and restores the project's `used.json`, which a killed run would leave dirty.

**Item 25's P1 build is complete with this audit.** Next: the test birth that runs P1 alone, `docs/p1-test-birth-1.md`, in a new Opus tab on the owner's word (scale standard, the owner's choice of 2026-10-05).

## 8. The test birth that runs P1 alone (`_test-p1-1`, 2026-10-05)

**At its first review stop** (attempt 1, gate open, door passed on the third run, 8 of 8 promises due at P1 kept, validator 0, 21 minutes): the development tab answered `düzelt` with a sentence that names no secret: rewrite only the two public passages the phase critic flagged under `rubric_leak` (`signature_wright_song`, `break_ruins_forbidden`), keep every rolled fact. The phase critic gave `fix` on both passes and no phase fix reached the writer (`phase_fixes: []`).

**The owner's rulings at that stop:**
- *A visible bodily trait does not contradict its lineage's body.* `trait_horns_with_age` is barred with `lineage_human`, `lineage_dwarf`, `lineage_elf`, `lineage_half_elf`, `lineage_halfling`, `lineage_gnome`, `lineage_half_orc`, `lineage_merfolk`, `lineage_centaur`; it stays open to the tiefling, dragonborn, giant-kin, fey, goblinoid, lizardfolk and mixed peoples. (The birth rolled horned halflings.)
- `trait_old_at_forty` stays open to every lineage: on a long-lived people (elves above all) it reads as what the break did to them, a hook worth meeting.
- In test births the owner may see the secret layer for now, to check the attempts; the secret and villain table rows stay counts only.

**Held for after the birth** (the code does not change under a waiting birth; each is specified once the birth's report is in):
1. The first run's writer read the dm-only dice log with Bash and the auto-mode classifier refused it ("PII Data Handling"); the second run succeeded. The prompts tell the agents to read dm-only with the Read tool. The refused run's cost (about 95,000 tokens) reached no ledger, since a failed run is not merged.
2. The phase critic's `fix` did not reach the writer at P1: find why `phase_fixes` stayed empty and close it (the finding that matters most).
3. The writer's first `appears` was refused for its shape: check that the prompt shows the `{phase, text}` shape once.
4. The card's "The value" line lacks "who lives on it".
5. The protocol said the development tab reads dm-only at a review stop; the guard covers every tab (`session_id` empty) and the classifier refused disarming it. The protocol changes: the birth tab disarms at the review stop and arms again before it continues.
6. The horns rule above.

**The birth was ended (`bitir`, owner, 2026-10-05) after its second review stop** (the leak closed on the rewrite: phase critic `fix → fix → pass`, checked against the mirror). The owner read the story and found it strange; his diagnosis: the lifeline is texture, and a die rolled for texture cannot carry the main story. Two searches found eight paths by which the story becomes abstract or texture-borne (the lifeline is the break's target or the contest's prize in 52.6 % of 1,800 births; the break is a faceless target × verb; nothing balances distinctness with legibility; signatures breed secrets of their own; the villain's motive is a value; world-state trope breaks; an institution hook on P7; the palette's size). The owner asked for the root solution; the proposal is `docs/p1-threat-first.md`: the layers (story, stage, texture) as a machine rule, and P1's story rebuilt as one chain that starts from the villain's concrete goal, acted through a visible hand. The held list above folds into it.

**Build item 18a, audited 2026-10-05 (the scripts' diff read; the contests, targets, actions and layers compared by script with `docs/p1-build-18-rows.md`; the suite run in the clean checkout at `c0dfc40`: 769 tests, OK, exit code 0, five skipped).** The layers stand on every P0 and P1 table (`frame` for the P0 dials and `scale.yaml`, `stage` for the era and the spine, `story` and `texture` as the specification lists); the story slots and the one-way rule are in the arbiter (a texture candidate barred at the roll, a set holding one refused) and in the door (the field list waits for 18e); `target_lifeline` and the two contests are retired and still readable; the 23 prizes, the stage gates and the dropped weights match the approved table; the lifeline is rolled last. Two corrections asked before the commit and checked in it: `prize_at` on the four contests whose disputed land is one side's own (the marches, the fey's forest, the coven's villages, the elemental lord's farmed land), and `key_kinds` on the six key-place prizes (from the spines' eight real kinds; the smallest contest pool over 3,000 seeds is 33 of 49). Accepted as reported: the calendar's names drawn before the stocks (a building and a special month could share a name; found by the suite, older than 18a); the lineage weight test's threshold (the old one leaned on lifelines the deep contests required); the coding tab's six readings of its open questions. **Not pushed:** the owner pushes the night's commits after his own look.

**Build item 18b, audited 2026-10-06 (the identity roller's diff read, the trope rows and the palette's counts checked; the suite run in the clean checkout at `cc37145`: 777 tests, OK, exit code 0, five skipped).** The eight world states are `layer: story` with their joins, never tied to the lifeline and never drawn without a join (900 of 3,000 births hold one); the two bent rows keep the class cores (the caster's spellbook and scrolls by right of the art, the cleric's and the paladin's features beyond holy ground at a price); the P8 hook stands on eighteen rows; the palette's count follows the spine's breadth. Corrections asked and checked in the commit: the public record omits a join to the threat; the enemy won also joins a fallen-kingdoms ruin; three more rows with the P8 hook; the writing row's caster clause. **Decided at this audit** (the owner asleep; weighed in `docs/reports/item18-night.md`): the threat is rolled before the trope breaks (G4's order) and a world state's join to the threat is judged on the rolled threat, which supersedes part 18b's sentence about weighing the threat. Not pushed.

**Build item 18c-1, audited 2026-10-06 (the threat roller and the tables read, the fit lists read in `docs/reports/item18c-fits-SPOILER.md`; the suite run in the clean checkout at `35d1080`: 790 tests, OK, exit code 0, five skipped).** The threat is rolled inside the foundation after the contest (family, creature in its CR window or a reskin, power source on the humanoid families above short, visibility, shape, origin, goal, weakness, lair), every roll secret; the chooser and the tie retired; the variety over 1,000 seeds per scale: 15-18 families, no consecutive repeat, 922-970 distinct sets. Decided at this audit and logged in `docs/reports/item18-night.md`: the god's weaknesses widened to seven by genuine fit (the floor of five on every `avoid_used` pool); the goal joins the contest by the prize, a role goal or the move; the law of nature also fits the fey; lair forms for every family at five or more, a dragon's colour weighing its lair; **a leak closed:** a world state joins only a public piece (a secret villain no longer decides whether "dragons rule" is drawn). Not pushed.

**Build item 18c-2, audited 2026-10-06 (the move's diff and the verbs' rows read; the suite run in the clean checkout at `e512a4b`: 800 tests, OK, exit code 0, five skipped).** The move is public: hand (27, with its creature family and the moon fit), target, verb (23, with the hands that make each), time, state, the timeline and the start (never the heart). Decided at this audit and logged in `docs/reports/item18-night.md`: the move joins the contest also when it strikes a side's holding; guard relations in the goal → target relation; summoned also into the heart and the key place; dragons rule and the gods among mortals weigh ×3; **the move's order became hand → target → verb** (the specification amended); the thin place weighs ×3 where it stands; poison and plague also strike a role; carrying off destroys nothing, driving out destroys the heart only. Over 3,000 seeds every target, verb and hand is reached and every world state stands between 47 and 125. A fault the coding tab found: the public hand inherited the villain file's hooks into the public ledger. Not pushed.

**Build item 18d, audited 2026-10-06 (the secret's tables, the twists' texts and the promises read; the suite run in the clean checkout at `f24f717`: 811 tests, OK, exit code 0, five skipped).** The secret is the threat's hidden half: four facts (three with a known villain), three stages with a conclusion each and three clues per conclusion (one placed by the chain, one promised to P5, one to P6), the twist always with mystery and about half without, the keeping (16 rows), eleven trails, the hero bound at P9, every new row's promises; the public ledger is identical with and without the secret rolls. Corrections asked and checked in the commit: a hand's base is inside (the heart or the deceived side's seat) for the traitor, the deceived side and the shapechangers; the twenty twists rewritten by hand (no break and no destroying verb, one sentence each, the protector a story actor, the old kingdom's fall repeated, the reshaped monsters victims, the greater power's statement). Carried into 18e: a twist that names a piece needs it. Not pushed.

**Build item 18e, audited 2026-10-06 (the summary, the questions and six fresh spine sentences read; the suite run in the clean checkout at `53e66ca`: 822 tests, OK, exit code 0, five skipped).** The writer's prompt stands on the chain and decides nothing the tables decide (W1-W7: the god pin with its rolled relation only for the god family, the patron's will or the greater power; the clues at the chain's pieces; the stakes the prize and the goal; the mechanic from six shapes); `appears` binds its hook; a true rule only as a clue's medium; the P1 rubrics on the chain with `rubric_p1_legible`; the card opens on the story sentence, counts the hidden facts and carries the `D&D:` line and its gate; four twists that name a piece require it. Three faults the coding tab found and fixed: the door read a hook's sentence as invented names; the ledger was saved only on a new promise; requirements first written on retired copies. **Not accepted as finished:** the story sentence's grammar and the verbs' fit to their targets' kinds (a city "carried off"); specified as part 18e-2, before 18f. Not pushed.

**Build item 18e-2, audited 2026-10-06 (the summary's twenty sentences and eight fresh ones read; the verb × kind list read; the suite run in the clean checkout at `77d5339`: 825 tests, OK, exit code 0, five skipped).** The story sentence is in active voice with the hand as its subject ("A generation ago, a dragon sealed the thin place; now the slaver lords and the escaped slaves fight over the people taken."); every verb fits only the kinds of target its phrase reads true for (a city is no longer carried off), over 3,000 seeds; roles carry a kind (group, settlement, person, creature) and short names, places and remnants their shorts (37 of 53 ruins); a power behind the villain (the twist or the patron's goal) has its kind rolled, and a god is pinned only when the kind is a god. A fault the coding tab found: two villain family labels cut by an unquoted comma in YAML. Accepted; the next coding tab (Coder-5-Opus) took over from the handoff for 18e-2 and 18f. Not pushed.

**Build item 18f-1, audited 2026-10-06 (the diff read: only the replaced assertions changed; the suite run in the clean checkout at `d8147bd`: 826 tests, OK, exit code 0, five skipped, 25.4 min).** One shared many-seed corpus (`tests/_corpus.py`: 3,000 in-memory P1 prerolls over every scale, magic, era, tone, content mix, danger and start band; read-only, checked by a digest on each read) feeds eleven test modules; the tests whose dials the corpus does not hold keep their own seeds. The suite fell from 51.3 to about 23-25 minutes. Two brittle proofs replaced: a rare case shown "exercised" by luck now proven without dice (the last institution home protected); P4's rolls no longer written into P1's context in a test. Not pushed.

**Build item 18f-2, audited 2026-10-06 (the summary, the measurement and twenty fresh sentences read; the suite run in the clean checkout at `5f600c3`: 837 tests, OK, exit code 0, five skipped, 24.4 min).** The dry walk walks the chain with three new wrong turns (a texture piece in a clue's place, a hidden truth serving no clue, a missing lair closing the `D&D:` gate); the whole-P1 measurement over the corpus: texture in no story slot, the lifeline neither target nor prize (52.6 % before item 18), a hand, a goal, a weakness and a lair in every birth, all 19 families, three stages with three clues each, every world state joined. The test birth's pipeline faults are fixed (the play floor's notes, a stale last error, the card after a correction round, reason codes checked and required, the old tongue's line, an unmerged run's cost, rerun clearing the validator), and **the fault that mattered most**: a phase critic's `fix` on a row the premise writes now goes back to the premise's writer (`design-fanout.js` had looked among the roster's units only; my specification had left it out of 18f's list, the coding tab found the cause at my request). **Item 18 is complete.** The second P1-only test birth's protocol is `docs/p1-test-birth-2.md`. Not pushed.

**The second P1-only test birth (`_test-p1-2`, 2026-10-06) and build item 19a.** The first birth on the threat chain read as a D&D campaign (a marilith that was once a monster hunter, a deceived house besieging the empty throne's city, a weakness in a person it loves); one Workflow round, a clean door, every `D&D:` piece ticked; the phase critic's fix reached the writer (18f). Its faults, fixed in 19a (audited 2026-10-06; the suite in the clean checkout at `c585244`: 853 tests, OK, exit code 0, five skipped): the deceived hand leaked through its subject, its row id and its label (the row is now "a side of the contest", the deceit only in the writer's prompt); "a bound elemental" became "an elemental" in public; an unnoticed move's hand is a secret roll (the move's order now time, state, hand, target, verb); the public "no people evil by birth — checked" section is gone (it leaked in both births); no plane is named at P1; the pitch carries the campaign's question (the owner's decision); a critic's `fix` on a rubric it was not given is refused; agents list, read and write with Glob, Read and Write, never Bash; the report groups fix reasons by critic and shows a promise that flipped. Not pushed.

**Build item 19b, audited 2026-10-07 (the summary and the mask rows read; the suite run in the clean checkout at `aafa7eb`: 860 tests, OK, exit code 0, five skipped).** A villain whose visibility hides it as a person among people (a mystery among candidates) can pass as one: a humanoid, a creature whose SRD text gives it a humanoid form (shapechangers, change shape, illusory appearance), a caster of a disguise spell, or the vampire in its own form; otherwise a mask is rolled (a disguise item or a glamour promised to P6, a possessed mortal or an agent who wears its name promised to P4). Over the corpus 599 of 3,000 villains hide among people, 255 pass by themselves and 344 carry a mask; the mask is a weakness where it fits. `build_design_index.py` records the daily spells and the humanoid forms. Accepted. 19c (the tests never touch a live guard; a rewritten file keeps its line endings) goes to the next coding tab. Not pushed.

**Build item 19c, audited 2026-10-07 (the diff of `paths.py`, the guard and the rewrite helper read; the suite run in the clean checkout at `310eb2b`: 871 tests, OK, exit code 0, five skipped; the checkout stayed clean after the suite rebuilt the design index, so the line endings hold).** The tests work on their own runtime directory (a variable honoured only inside the temporary directory) and a fresh-process test proves a live marker keeps its bytes; every script that rewrites a tracked file keeps its line endings. Two holes closed in the same commit: a command naming the test or runtime variable is refused while a marker is armed; the read guard now watches Glob and PowerShell as well as Read, Grep and Bash (the owner approved the settings change). Found at this audit and specified as 19d: a search through a parent folder of dm-only. Not pushed.

**Build item 19d, audited 2026-10-07 (the guard's diff read; the suite run in the clean checkout at `a574ee0`: 873 tests, OK, exit code 0, five skipped).** While a marker is armed, a search from a folder that holds `design/dm-only` (a Grep or Glob judged against the files actually there, read as ripgrep reads its globs; a recursive Bash or PowerShell search or listing whatever its filters) is refused for the conductor, an ad-hoc agent and the playtest player; designer agents and the DM at the table stay free. The birth protocol says to search outside the campaign if a search is needed. **Item 19 is complete** (19a-19d). Not pushed.

