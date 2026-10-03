# P0 and P1 tags — the owner-approved rules and rows

*Source material for build item 7c (the claims system). Written by the development (design and review) tab with the owner, table by table, in roll order. Background: `docs/reports/tags-grouping-analysis-1.md`. A tag is changed here first, with the owner; the YAML tables follow this file. Secret and villain rows never appear here, only their counts.*

## 1. The rules (owner-approved 2026-10-02)

Four relations between rows, all read from tags, never from text: **clashes** (hard), **requires** (hard), **overrides** (hard), **fits** (soft).

1. **Claim.** A row that states a fact about the world carries it as `topic: value`. A claim is written only where the row's sentence, hook or dial effect says so literally. Theme and association are never claims.
2. **Clashes are declared one by one.** Two values of one topic do not clash by default. The closed registry lists, pair by pair, which two claims cannot stand together.
3. **Scope lives in the topic's name.** The land's rule and one people's own order are different topics; a foreign polity carries no claim. A clash may be declared across topics.
4. **Clash or override, one test.**
   - Against a *rolled row* or a *dial's value*: **clashes**. The later row leaves the pool; what was rolled first stays.
   - Against a *default* (a dial effect, a quota, a scale number, another row's hook): **overrides**. The trope break stays and the default is rewritten as it says.
5. **Requires.** A row that names something by "the X" is not drawn unless X was rolled.
6. **Fits.** A theme link is a weight only (×2-3), never hard. Theme lists (dragons, craft) are not turned into claims.
7. **The dials are the root.** Dial rows carry claims too. The owner may set a dial, so no roll changes it; every later roll yields to it.
8. **Inspection.**
   - Every row carries its own "reviewed" stamp; a changed or new row turns the test red.
   - A hard group that falls under five rows turns the test red.
   - The development tab tags the secret rows; the owner sees counts only. Topics that belong to the secret alone stay out of the owner-visible registry.

9. **One target, one owner** (added the same day). Every effect and every hook names what it sets (P4's quota, P2's calendar, the site types). The "who sets what" chart below is kept during the review; a second owner of one target is brought to the owner at once. Where two owners are really needed, how they combine is written (multiplied, or one overrides the other); an unwritten second owner turns the test red. Effects are structured and a script can scan them; hooks are prose and are caught only as the review reads them, each read hook gaining a target tag. The hooks of the P2-P8 tables stay unscanned until their floors' turn.

**A limit.** In P1 an override is data only. The code that applies it is built when the floor that reads the overridden default is bound (P4's quota at P4, the calendar at P2). Until then each override stands in the promise ledger as a promise with a due phase.

**First topic list** (grows and is settled during the review): the land's rule · nobility · iron · below ground · writing · how plentiful magic is · the form of war · crossing the border · the world's age. "Sky" is left out on purpose until the era dial is reviewed.

## 2. The review, table by table

### P0 — scale (`dials.yaml#scale`, `scale.yaml`; approved 2026-10-02)

- **No claims.** Scale is a size, not a fact about the world. The three rows carry no claim, clash or requirement.
- **Scale is the home of overridable defaults.** Registered so far; how each is rewritten is settled at the trope-break table:

| Default | Today | Overridden by |
|---|---|---|
| the forced `state` faction (`factions.quota.state`) | 1 at every scale | "no lords; guilds rule" |
| the years history covers (`history.years_covered`) | short and standard 200, epic 500 | "the world is young; written history is three hundred years" (clashes at epic only) |

- **Owner rulings (2026-10-02), for the floors' turn:**
  - *Planes (P2):* at least one touched plane at every scale. `planes_touched` at short becomes 1 (today `[0, 1]`).
  - *Gods and churches (P2, P4; narrows errata 24.2 #11):* an epic world may hold 9-14 gods, but not every god is a great, widely worshipped power. Fallen, weak and little-followed gods are story value and are never faction-strength. One or more gods, by the kind of story, are great powers with followers and servants; those may be factions. "A church faction per god" goes.
    - Great powers (gods whose church is a faction): short 0-1 of 3-5 gods, standard 1-2 of 6-9, epic 2-4 of 9-14. The roll inside the band is weighted by the story: a ruin source of the gods family, a religious contest role, a religion-heavy tone push it up. The other gods keep a name, a domain and a story, and no faction.
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
- **Open for the build item:** the seven tone weights in `foundation.yaml` (cosmic 3, heroic 2, horror 2); the voice examples go to item 15's cleanup list. Legacy births keep their old tone values untouched.

### P0 — magic (`dials.yaml#magic`; approved 2026-10-02)

- **Claim:** topic "how plentiful magic is", values `low` scarce, `medium` middling, `high` plentiful.
- **Clashes:** one candidate, settled at the ruin-source table: `plentiful` with the ruin "the age of mages" (the age of plentiful magic ended overnight).
- **Requires:** the requirements keyed on this dial already stand in the tables (fantastic landform kinds, griffons, giant insects); untouched.
- **The regulator had two owners** (the dial named who; P2's `magic.yaml#regulator` rolls who). Ruling: the dial sets only **how strict** (low: strict, licence or hunt; medium: loose; high: nearly free); P2's roll sets **who**. The dial's hook "the mage guild exists" goes; the service menu (identify, training, a price list) belongs to whoever the regulator is.
- **`high` sat in the attractor.** "Magic is infrastructure and the city bills for it" and "lamps" go. The infrastructure idea stays without the bill (owner, the same day): "the city's ward, its lift, its bridge run on magic; they are nobody's property". The P3 hook asks for at least one such settlement.
- **Note for P2:** the dial no longer guarantees a service provider (medium used to promise a guild selling identify and training), and P2's regulator table has a "nobody" row. At P2's turn "who gives the service" is answered for every regulator row.
- **Overridable defaults:** the caster share of the roster (0.08 / 0.15 / 0.30) and the regulator, both by "magic is nobility; there is no magicless noble". Sketch for the trope-break table: with that trope P2's regulator roll is not made, the regulator is the nobility, and the primer's "what a caster risks by casting in public" becomes "what a commoner risks by casting".
- **Note for P4 (rule 9):** the faction list has five sources (the scale's quota, the contest's roles, the institution signature, the great gods' churches, the magic regulator). Likely rule: the regulator is no new faction, it sits on an existing one.

### P0 — era (`dials.yaml#era`; approved 2026-10-02)

- **Claims:** `era_renaissance` → writing: printed (clashes with the trope break "writing is unknown"). `era_underground` → below ground: lived in (clashes with the trope break "going underground is forbidden"). Medieval, ancient and nautical carry none. The dial is the root, so in those births the trope break leaves the pool.
- **The sky (the report's open detail):** the underground era does **not** claim "no sky"; the surface is rare, not gone. The calendar note becomes "the sun and the moon are known but seldom seen; those below count time by what the deep gives" (the bells and tides go with it). The rows that touch the sky (the moon traders, night safe and day dangerous, the "sky changed" scar, the sky-watching institution) are judged one by one at their own tables; the leaning is that night-and-day clashes (it loses its meaning below) and the moon traders do not (a story).
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

### P1 — the spine (`foundation.yaml#spine`; in review from 2026-10-02)

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
- *The same test holds for the other prohibition rows* (maps, weapons, crossing the border, a god's name, a sacred beast).
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
- **Earlier rulings re-read:** the elves' withdrawal against "the elves arrived last century" stays a clash (in the data). The age of dragons against "dragons rule the lands" was ruled no conflict on 2026-09-29; under the working rule it is confirmed only after the two rows' hooks are read together at the trope-break table.
- **No clash, with reasons:** "the world is young" with old ruins (owner, 2026-09-29: sites may be older than the fall, all that is known dates from it; the hooks write different targets, P6's sites and P2's years, the latter an overridable default); the sky ruins with the underground era (the era claims no "no sky"; their sites stand on the rare surface); "writing is unknown" with dwarf runes and merchant seals (the old people's, not today's).
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

- **Rule 9:** the four common hooks each have one owner (P3's economy and goods, P5's trades, the contest's prize, the people signature's home).
- **Note for P2:** the pilgrim road presupposes a holy place and a faith; whether the pilgrims' god must be one of the great gods is asked at P2's turn.

### P1 — the contest (`foundation.yaml#contest`; part 1 approved 2026-10-02)

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

### P1 — the trope break (`trope-breaks.yaml`; in review from 2026-10-03)

Every carried pair is settled here, each after reading both rows' hooks.

**Family 1, governance and power (approved):**

| Row | Claims | Clashes | Overrides | Fits |
|---|---|---|---|---|
| rulers are drawn by lot | the land's rule: by lot | the four "hereditary" rows (two heirs; the empty throne; sibling rulers; the binding marriage); the question "birthright and merit" (in the data) | the state faction's succession rule; the ruler NPC's heir field ("next draw"); the politics mix's `succession` node ("the day of the draw") | |
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
| giants are the peasants | the giants' peace (lifeline), humans and giants (contest): two places and two orders for one people | | ×2 with the ruin "the giants' land" |
| monsters hold treaties | nothing | P6's attitude roll on the treaty people's lairs (negotiate); the horror mix's "test or enslave" site is never one of those lairs | ×2 with the non-human treaty lifelines and the human-and-non-human contests |
| some lands' lord is a beast-person | nothing | | |
| lineage homes are inverted | nothing (the dwarf-city and elven-forest ruins tell the past) | the lineage roll's palette weights (inverted; item 10) | |

- **"The elves arrived last century":** its statement is cut down to its name ("the elves came to this land last century; they have no past here"); the old text also called humans the ancient people of the old ruins, which contradicted four old-peoples ruins.
- **"Animals speak and hold land" becomes the beast-people** (owner): the landholders are a born lineage that is both beast and person (the SRD's five lycanthropes; others by the reskin rule). The row says nothing of a curse, contagion or alignment: tables assign nobody a good or evil part, later floors place the parts (the owner's reading of "no inherently evil people", confirmed). Its P3 hook reads "a beast-lord holds one part of the map" (was: one region; short has 1-2). No clash with the herd and hunt lifelines, nor with the shapeshifter contest (an open lord of a region against an unproven rumour; different targets).
- **Factions asked for:** the treaty people; the beast-lord.
- **Note for the names table:** "trade speaks goblin" touches the language count (two at short); the common tongue being goblin is an override candidate.

**Family 3, gods and the sky (approved 2026-10-03):**

| Row | Clashes | Overrides | Fits |
|---|---|---|---|
| everyone knows the gods are mortal ancestors' spirits | the ruin "a dead god" (a spirit leaves no mountain-sized body); one secret row (the development tab's table) | P2's pantheon-type roll (ancestor gods; the field was in the data, unread) | ×2 with the ruin "the mortal who failed to become a god" |
| the moon is inhabited and trades | nothing (with the underground era: the trope writes P2's planes, the era P2's calendar; the moon ships land on the rare surface) | | ×2 when the era is nautical |
| divine magic works only on holy ground | nothing | | ×2 with "two faiths, one holy place" and the pilgrim road |
| one god's name may not be spoken (prohibition) | nothing | | ×2 with the ruins "the imprisoned god" and "the god who left" |

- The moon is a plane and joins the shared-planes rule (at short the one plane is the moon; a thin place in the palette is where the moon ships land). Its old field "biases the era roll toward nautical" is deleted: a dial is rolled before the trope and cannot be overridden.
- With the great-gods ruling: the god fading for lack of witnesses is one of the fallen, faction-less gods; the unnamed god's hidden priests are a faction, so that god counts among the great powers.
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

**The trope break is closed:** 32 rows.

### P1 — the people signature (`signatures.yaml#people_lineage`, `#people_trait`, `#people_attitude`, item 8's uncommitted tables; approved 2026-10-03)

**Lineage (16 rows): no claims, weights only.** Today's weights stand (human base weight 4; dwarf, elf, halfling, gnome, giant-kin, sea folk, lizardfolk and centaurs by palette kind; gnome by the craft lifelines; dragonborn by the dragon rows; tiefling by the planar rows). Added fits, ×3: giant-kin with the giants' peace, humans and giants, the giants' land, giants against dragons, "giants are the peasants"; the fey people with the fey bargain, humans and fey, the elves' withdrawal; the sea folk with the sea-folk hunt, land and sea folk, the spine above and below the sea, the great flood; the goblin or kobold people with "monsters hold treaties". "Lineage homes are inverted" inverts the palette weights (a lineage whose home kind the palette lacks takes the ×3).

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

### P1 — the institution signature (`signatures.yaml#institution_form`, `#institution_practice`, `#institution_sign`, `#institution_power`, item 8's uncommitted tables; in review from 2026-10-03)

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
| war | they hunt dragons or giants | martial |
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
| P2's history | the ruin source (one age), the break (a dated event), the palette (the origin of a fantastic kind the ruin did not bring), the scale (the numbers) | "the world is young" overrides the years |
| which plane | P2 chooses, among the touched planes, for the thin place, the ruin's plane and the scar; shared to fit the scale's count | |
| the palette's kinds | the spine (forces), the era (forces: underground, nautical), the ruin source (one kind, on top of the count), a scar (one kind, counted toward the cap), the roll for the rest | every combination is written |
| P7's endings | the question (their content), darkness (which is most reachable) | two aspects |
| how clean the sides are (P4), the voice | darkness | |
| the villain's pole | P1's secret roll; darkness `dark` overrides the majority's side | |
| the magic regulator: who | P2's regulator roll | the magic dial no longer names it; "magic is nobility" overrides |
| the magic regulator: how strict; the caster share; the loot multiplier; the wild-magic gate | magic | |
| P4's faction list | scale quota, contest roles, institution, great gods' churches, regulator, trope breaks | six sources: to settle at P4; the scale's count is never exceeded |

Words in two closed lists: `standard` is both a scale and a danger value; to rename at the danger dial.

## 3. Held for the build (owner, 2026-10-02: nothing more goes to the coding tab until P1's review ends)

The plan may still change while the review runs, so the review's results are collected here and turned into build instructions only once P1 is closed. Build item 7a (the arbiter's three faults) was handed over before this ruling and stands.

**The P0 changes that need no tag system (drafted as "7b", not sent):** everything under the "P0 — …" headings above except the claims and the overrides. Choices made while drafting, to confirm when the instruction is written:
- the dial keeps its key `tone`; values `bright`, `shadowed`, `dark`; blank-roll weights 2, 3, 1 (the old rows' weights);
- the 22 tone weights in `foundation.yaml`: heroic (2 ruin sources) → `bright`; horror (2 ruin sources) → the content mix `horror`; political (15 contests) → the content mix `politics`; cosmic (3) deleted;
- legacy births load with their old dial values; a new birth refuses them;
- `danger_standard` → `danger_balanced`, while `effects.state_difficulty` keeps its value (play reads it);
- item 8's uncommitted `signatures.yaml` names tone values in ten places; they are re-pointed when item 8 resumes.

**For item 7c (the claims system):** the claims, clash pairs, overrides and overridable defaults recorded above; `trope-breaks.yaml` already carries an unread field named `overrides` (on the moon traders, an era bias) that must not be confused with the new relation.
