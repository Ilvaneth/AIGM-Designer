# Build item 11 — the names

*Written by the development (design and review) tab for the coding tab, 2026-10-04. The design is plan item 25 (step 2, piece 8), errata 24.2 #17, #18, #20, #25, and the owner's decisions of 2026-10-04 recorded at the end of this file ("The owner's decisions"); where a decision there differs from the plan or from an earlier decision, the later decision holds. The data: `docs/p1-build-11-bags.md` (the seventeen bags and the trial generator), `docs/p1-build-11-lexicon.md` (the 505 roots), `docs/p1-build-11-filters.md` (the two new filter lists). Where a source and this file differ, stop and report.*

**What it closes.** The writer still builds every place, institution, month and day name and picks the naming roots; that is where the attractor leaks. Measured: the ten sound families' banks give names like Woowoomb and Tittdimm (the hand-written samples are not what they produce), and 10 families with 115 roots run out in a few births.

**Two green commits, in this order.** After each: the full suite green (the exit code), no commit before the audit, no push.

| Part | What | Commit message |
|---|---|---|
| 11a | the tables (bags, lexicon, tails, patterns, word lists, filters) and the part-bag generator for person and god names | `Plan item 25, build 11a: the name tables and the part-bag generator` |
| 11b | the languages rolled by script, the calendar's roots, the candidate pools and stocks, the secret stock | `Plan item 25, build 11b: the languages and the name pools by script` |

**Limits.**
- The door's new rule (a proper noun outside the pools is refused) is item 13; here the door keeps what it checks today for persons and gods, plus the one addition of section 12. The writer's prompt, the critics and the card are item 14: keep `phase P1 begin` and the present card working with the least change, and list in the summary what you had to adapt.
- Legacy births (a `naming.json` whose languages carry `onsets` / `nuclei` / `codas` and no `bag`) keep loading and keep drawing names the old way; `test_regression_births` stays green. The fixture is a legacy birth.
- Run nothing that calls a model. No secret row and no secret-stock name in a summary.
- A contradiction between rows is settled by the script from data, never by the model.

---

## Part 11a

### 1. `naming.yaml#family`: seventeen part bags

Replace the ten rows by the seventeen bags of `docs/p1-build-11-bags.md`, as given (ids `family_<key>`; fields `group` A-E, `openings`, `middles`, `middle_chance`, `endings`, `vowel_join`, `real_ok`; an English `label`, a Turkish `tr.name`). Delete from every row: `onsets`, `nuclei`, `codas`, `length`, `forbidden_clusters`, `best_for`, `samples_person`, `samples_god`, `feel`, the per-family `hooks`. Delete the P1 line of `hooks_common` (no mutation, decision 16). `roll.notation` follows the row count; `avoid_used: true` stays.

### 2. The generator (`design_names.py`)

A person or god name of a bag language: one opening, a middle with the bag's chance, one ending, joined by the trial's rules (decision 13): a doubled letter at a join is dropped; a vowel never meets a vowel at a join; a `vowel_join` bag never joins consonant to consonant; at least five letters; no four consonants in a row; no two-letter chunk repeated at once, no three-letter chunk repeated anywhere. Then the existing `acceptable` (shape, blacklists, the registry's names, near-typos, the ending and opening caps), with the bag's `forbidden_clusters` and `onsets` checks skipped for a bag language, and the real-name filter of section 5. A legacy language (no `bag`) keeps `_raw_name`.

### 3. `naming.yaml#lexicon`: 505 roots

Replace `lexicon.roots` and `place_tails` by `docs/p1-build-11-lexicon.md`: each root `{root, pos, tags: [..]}`, no `meaning`, no `domains`; the 22 settlement tails as their own list `lexicon.settlement_tails`; the 21 untagged roots with `tags: []`. A closed tag list `lexicon.tags` with what calls each tag (decision 6): `called_by: {palette: [land ids]}` or `{lifeline_family: [...]}` or nothing. The water lifeline family calls `fresh water` or `sea` by the kind the lifeline sits on (the layout); the treaty family calls nothing; `land_thin_place` calls nothing; `land_giant_bones` calls `animal`.

### 4. `naming.yaml#patterns`, without examples

Every `examples` field goes (a test keeps them out). The patterns, each a structured row a script can fill (slots, not prose):
- **place** (decision 23): seven patterns; the word lists `region_words` (12) and `building_words` (12).
- **institution** (decisions 25, 26): four patterns. `signatures.yaml#institution_form` gains `name_words` per form (the travelling form's `Fleet` carries a requirement: the palette holds a sea or fresh-water kind). The form's `label` stays what it is; only the name word is new. This changes 14 stamped rows.
- **people** (27): three. **phenomenon** (28): two, with `phenomenon_tails` (12).
- **month** (29): three rollable patterns and the `High` / `Last` pattern; **day**: one.
- **old tongue** (30): a bag word alone, or with one of `site_words` (8; plural allowed).
- **god epithet** (32): four. **ship** (32): two.
- **Adjective roots** (35): a root whose first tag is `colour` or `direction and age` is an adjective (derive it; do not hand-mark 32 rows). Each pattern slot says whether it takes adjectives: no in "of the …", months, days, people, phenomenon; yes in place names, `the` + root + form word, inns, ships, "the … One".
- Deleted with their rows: "Court of…", "…Assize", "…tide", "Keepers of the…", "{Head}bound", "the {Adj} Ones", "the {Noun} Who {Verb}s", "{Name}'s {Noun}" (ship), and "The {Noun} Watch", "Guild of {Noun}s", "{Head} Fellowship" as patterns of their own (the form words carry them now).
- `rules.modes` and the header comment are rewritten to say what the script does; `rules.turkish_suffixing` stays as it is.

### 5. The filters

`blacklist.real_given` and `blacklist.real_places` from `docs/p1-build-11-filters.md`. They work inside the generators only (a hit is dropped and the next candidate drawn); the door does not read them. `real_given` is skipped for a bag with `real_ok: true`.

### 6. The stamps

Every family row, every root, every pattern row and each word list carries a reviewed stamp like the other P1 tables (`reviewed.json`); written before the summary, committed after the audit.

### Tests of 11a

- The tables: 17 bags in 5 groups (4, 4, 3, 3, 3); 484 tagged roots and 21 untagged, no root twice, every tag in the closed list, every `called_by` id exists in `foundation.yaml`; 22 settlement tails; no `examples`, `meaning`, `samples_*`, `best_for` anywhere in `naming.yaml`; the deleted patterns are gone; every form has `name_words`.
- **The yield, per bag, with every filter on:** over 200 seeds each bag gives 100 accepted names (the epic need is the named-NPC band's top plus the spares; take the number from `scale.yaml`, not from this file). A bag that fails turns the test red.
- **The overlap:** two births on one bag share at most 25 of 100 names (measured 1 to 17 on 20 seeds; report the worst over 200).
- No generated name equals an entry of any blacklist; no name of a bag without `real_ok` equals a `real_given` entry.
- A legacy language still draws names by the old path.
- The existing tests that assert the old family shape (`test_design_tables.py` around the `naming.yaml#family` loops, the suffix-friendly check) are rewritten to the new shape, not deleted.

## Part 11b

### 7. The order

The naming rolls move to the end of P1's rolls: after the secret, the villain and the mechanic gate. The old `naming_family.N` rolls between the question and the secret go.

### 8. The languages (public rolls, each through the arbiter)

- **Living languages by scale:** short 2, standard and epic 3.
  - Language 1: the signature people's (`owner: people`).
  - Language 2: the common tongue (`owner: common`); with `break_no_common_tongue` rolled it is the contest's other side's (`owner: other_side`: the main contest's side the people does not hold; when the people holds no role, role `b`). This is the override the review recorded for that row: apply it here, as data read by script.
  - Language 3 (standard, epic): the contest's other side's; with `isign_own_language` rolled, the institution's (`owner: institution`). When language 2 is already the other side's and the sign is not rolled, there is no third living language.
- **The old tongue** (`owner: old`): in every campaign, beside the living ones, not counted among them.
- **Bags:** one per language, `avoid_used`; the living languages come from different groups; the old tongue's bag comes from a group no living language of the campaign uses. Labels `naming_family.1..3` and `naming_family.old`.

### 9. The roots (public rolls)

- **Count per living language:** short 10, standard 18, epic 24 (decision 44; the plan's 12 and 15 were measured too thin). The old tongue has no roots (its names are bag words; this supersedes the last clause of decision 8).
- **The share (decision 33):** half of a language's roots (rounded up) are drawn among the roots that carry a tag the language calls; the rest are drawn from the whole lexicon. When the called pool is too small, the remainder is drawn freely.
- **What a language calls (decision 8):** the people's language: the tag the lifeline's family calls and the land tag(s) of the kind the people sits on (the layout: its role's seat when it holds a role, else the lifeline's part). Every other living language: every land tag a palette kind calls.
- **The floor (decision 36):** a language's draw holds at least two roots usable as a natural tail (`tail` or `either`, not a settlement tail) and a floor of roots usable as a head: short 5, standard 9, epic 12, of which at least four are not adjectives (the three signature slots each need four different noun roots). Make the draw satisfy it by construction; report in the summary how.
- **No sharing (decision 7):** a root belongs to one language of the campaign; the calendar's roots (section 10) are also distinct from every language's.
- **Usage:** rolled roots go to `used.json` at approve and are not drawn again while the lexicon has rows (errata #20); a real birth ignores the test births, as elsewhere.
- **Settlement tails:** 7 per living language, drawn from the 22; they may repeat across campaigns; two languages of one campaign share at most two tails.

### 10. The calendar's roots (decision 34)

A draw of its own: 14 month roots and 9 day roots, only from roots whose tags include crop, weather and season, cold, animal, forest, sky or fresh water, never an adjective; the palette's called tags take the same half share. One month pattern is rolled for the campaign (`month`, `moon` or `fall`). P2 keeps rolling the year's shape and the week; it takes its names from this stock (the P2 prompt line that says months come "from patterns.month" is adapted with the least change).

### 11. The record and the pools

- **`design/naming.json`** is written by the script at the preroll, public and stamped: per language its owner, bag, group, roots, settlement tails; the calendar's pattern and roots. The writer no longer writes or edits it (the least prompt change: delete that task from `P1.premise.md` and say where the names come from). A language's label is derived, in English (the owner's ruling of 2026-10-04, `docs/p1-build-13.md`): "the <people's name> tongue" once the people is named, "the common tongue", "the old tongue" (decision 31); until then the owner word. No `label_tr`.
- **The signature candidates** (decision 38), public, in `naming.json#candidates`: four each for the people (language 1), the institution and the phenomenon (the language of decision 43). The institution's candidates use the rolled form's `name_words` (`design.json#identity.institution.form`); the House form uses its one pattern with four family names from the language's bag. The four candidates of a slot differ in root, and where the slot has several patterns, in pattern.
- **The stocks,** in the existing dm-only pool file, per living language: persons and gods as today (from the bag); places (patterns 1 and 2), regions (3), inns (4), buildings (5), ships where the palette holds water, god epithets. For the old tongue: sites. For the calendar: one name per month root in the rolled pattern, four `High` / `Last` names, one name per day root. Sizes: at least three times what the scale can use (regions, settlements, sites, gods from `scale.yaml`); report the numbers. A stock is topped up when it runs low, as persons are today.
- **Inns and ships draw from the whole lexicon** (decision 44): pattern 4 and the two ship patterns take their colour root and their animal, sea or sky root from the lexicon at large, outside the languages' root sets and without recording usage. Measured: only 12 % of 12-root languages hold both a colour and an animal root.
- **Spread and joins in a stock (decision 37):** one head root appears in at most three names of a stock; no doubled letter at a join; head and tail differ; a compound is at most 12 letters; the `real_places` filter; every existing naming rule of the door (blacklists, Turkish letters, names another campaign registered).
- **The prompts' Names paragraph** lists, per language, what it lists today plus the new stocks, and no longer says a place may be "a compound of the language's roots in the same shape": the writer takes a name from a stock or a candidate list and invents none. Patterns 6 and 7 are composed by the writer from a pooled person or god name and a building word; say so in the paragraph.

### 12. The secret stock (decision 41)

A separate dm-only file holds, per language, a stock for secret entities (persons, gods, places, old-tongue sites), drawn under its own rng label and disjoint from the public stocks. No public output, no rendered prompt and no card prints a name of it: a prompt that may name a secret entity gives the agent a command to run (`design_names.py -c CAMP secret --lang L --kind K`) and the agent reads the names from its output. The door's existing rule (a secret entity takes no public pool name) gains its mirror for persons and gods: a public entity takes no secret-stock name. Places and the rest are item 13's.

### 13. The owner's reroll (decision 40)

`design_names.py -c CAMP reroll --slot people|institution|phenomenon`: four fresh candidates for one slot (the next attempt of that draw), the old four kept in the record as discarded. It is the owner's tool at the review stop: outside `_test-*` campaigns it asks for `--onay` like approve does, and no prompt or workflow calls it.

### Tests of 11b (thousands of seeds, every scale, magic, era and tone)

- The languages: the count by scale; the owners under both overrides and under both at once; the living bags in different groups; the old tongue's bag in a group of its own; no empty pool.
- The roots: the count; the half share (at least half of every language's roots carry a called tag whenever the called pool allowed it; report how often it did not); the floor of heads (5, 9, 12 by scale, four of them nouns) and of two natural tails in every draw; no root in two languages or in a language and the calendar; the calendar's roots only from the nature tags and never adjectives.
- A landlocked palette never gets a `sea` root in the called half (it may get one in the free half; report the rate).
- The pools: four distinct candidates per slot; the form word is one of the rolled form's `name_words`; `Fleet` never without water; no adjective root in a slot that bars it; one head in at most three names of a stock; every stock meets three times the scale's need; no candidate or stock name on any blacklist or in the registry of another campaign.
- Secrecy: the secret stock is disjoint from the public stocks; no name of it appears in `design.json`, `naming.json`, the public dice log, a rendered prompt or the card; the door refuses a public person with a secret-stock name.
- The reroll: four new candidates, the old ones recorded, `--onay` asked outside `_test-*`.
- Legacy: a birth whose P1 predates this keeps its `naming.json` and its pool; nothing is re-rolled for it.
- The whole-P1 measurement (`whole_p1_v2.py`) still reports zeros.

## The summary (each part)

Changed files; new and changed tests; the suite's count and exit code; what was adapted to keep `phase P1 begin`, the P2 prompt and the card working; anything unexpected. For 11a: per bag, the yield's worst seed, the overlap's worst pair, the count the filters dropped over 2,000 draws, and a file of 200 names per bag from a fixed seed (for the development tab's reading, outside the repository). For 11b: the stock sizes per scale; how often the called pool was too small; the rate of off-palette roots in the free half; one full printed pool for a `_test-` seed at each scale (public part only).

---

## The owner's decisions (the record, 2026-10-04; the numbers are cited above)

### Part 1 — languages, sound families, root tags (owner, 2026-10-04)

A "language" is a naming style: one sound family (person and god names) plus a handful of rolled roots (place, institution, month and day names). Nobody speaks it.

1. **A language's sound family** is rolled; the languages of one campaign come from different sound groups (each family carries a group), so a listener can tell the languages apart. `best_for` is deleted; no lineage or palette weight on the family roll.
2. **Whose the languages are.** Language 1: the signature people's. Language 2: the common tongue (cities, months, days). Language 3 (standard, epic): the contest's other side's. Two exceptions already ruled: the trope break "there is no common tongue" gives language 2 to the contest's other side; the institution sign "they speak only their own language" gives language 3 to the institution.
3. **With "there is no common tongue", language 3 is the ruin's old tongue:** a dead language that lives only in the names of the sites the ruin source left (a column for P6). New; not in the plan.
4. **Roots follow the world.** A root carries one or two tags; a called tag weighs its roots ×3.
5. **War, oath and holy roots are called by nothing** (neither the contest nor the ruin source weighs roots).
6. **The tag list (22, closed).**
   - Land tags, called by a palette kind: heights (mountain, highland) · flatland (plain, steppe) · forest (forest, giant fungus, crystal forest) · fresh water (river, lake, marsh, sky river) · sea (coast, island, stone sea) · arid (desert, glass desert) · fire (volcanic) · cold (cold lands) · deep (underground) · sky (floating isles, sky river) · stone (crystal forest, stone sea, glass desert). The thin place calls nothing; giant bones call the animal tag.
   - Livelihood tags, called by the lifeline's family: animal (creatures) · crop (crop) · mine (mine) · craft (craft) · road (passage). The water family calls fresh water or sea by where the lifeline sits; the treaty family calls nothing.
   - Uncalled tags: settlement · colour · direction and age · weather and season · war and watch · holy and oath.
   - The old domains death, light, dark, silence, trade, song, body and time go. Their roots stay in the lexicon (errata #18), each moved to a tag above or left untagged (base chance only); decided row by row in the lexicon part.
7. **Languages share no root:** a root belongs to one language of a campaign.
8. **What calls which language's roots.** The people's language: the lifeline's tag and the land the people sits on. The common tongue and the other side's language: every land tag of the palette. The ruin's old tongue: nothing (a flat draw).
9. Families keep waiting across campaigns (`avoid_used`), as today.

### Part 2 — the sound families (owner, 2026-10-04)

10. **Person and god names are built from name parts, not from single sounds.** Measured with the real generator: the ten families' onset / nucleus / coda banks give names like Woowoomb, Tittdimm, Cecicinci; the hand-written `samples_person` are not what the banks produce. A family is now a bag of openings, optional middles and endings; the script joins one of each.
11. **Bags are large (about 50 openings, 30-50 endings) and a campaign uses the whole bag.** Measured: 12 × 10 parts never gave 60 names; the whole bag gives 100 in 20 of 20 seeds for every bag, and two births on one bag share 1 to 17 of 100 names.
12. **Seventeen bags in five sound groups** (the owner asked for 22; five failed the measurement or the test "the world is neither Turkish nor one real culture": desert courtly, lowland merchant, alien x/z/q, the -tl bag, the measured-syllable bag). A: hard upland, northern, guttural, eastern. B: liquid coast, nasal round, airy, open-syllable isle. C: sung, courtly, antique. D: rustic, misty vale, old isle. E: sibilant, lake folk, old mountain. The parts and the trial generator: `docs/p1-build-11-bags.md`. A bag can be added later as one row.
13. **Shape rules the trial used and the build keeps:** a doubled letter at a join is dropped; no vowel meets a vowel at a join; `vj` bags never join consonant to consonant; at least five letters; no four consonants in a row; no two-letter chunk repeated at once and no three-letter chunk repeated anywhere; then the existing `acceptable` (the blacklists, near-typos, the ending and opening caps).
14. **A real-name filter** (a list of common real given names and short English words) drops a generated name that equals one; it is off for the rustic bag (owner: a real English name suits a villager). It works inside the generator, so nothing reaches the door; a test proves every bag still yields the epic need with the filter on. The owner sees the list's size and the count dropped per bag, not the list.
15. `samples_person`, `samples_god`, `best_for` and the per-family writer hooks are deleted.
16. **No mutation** (owner, 2026-10-04; changes errata 24.2 #20's "the script mutates them"): a large bag already differs between births and the registry refuses a name another campaign holds; a mutation would break parts the owner approved.

### Part 3 — the lexicon (owner, 2026-10-04)

17. **A root carries no gloss:** the `meaning` field is deleted (the glosses carried the attractor: tide "debt", lamp "mourning"). This closes item 15's "lexicon glosses".
18. **Each language rolls its own settlement tails**, 6-8 of the 22 (-ham, -wick, -thorpe, …), so a place's ending tells whose it is. Natural tails (ford, mere, crag) are ordinary roots of their tags.
19. **The lexicon: 484 tagged roots and 21 untagged, 505 in all** (the plan said 300-400; the owner approved every row, tag by tag; `docs/p1-build-11-lexicon.md`). All 115 old roots are placed; no root is listed twice. 302 heads, 140 tails, 42 either.
20. **The attractor's roots stay but are called by nothing** (owner, row by row): barrow, still, salt, tide, wake, lantern, lamp, candle, tallow, wax, toll, hush, bell, choir, song, mourn, grave, coin, tithe, debt, crown. The owner keeps ash, ember and cinder under the fire tag (called by volcanic land only).
21. The six uncalled tags (settlement, colour, direction and age, weather and season, war and watch, holy and oath) weigh nothing: their roots come by base chance like the untagged ones.

### Part 4 — the patterns (owner, 2026-10-04)

22. **The direction and age roots are ordinary heads** (Northwick, Oldham); no pattern of their own.
23. **Place patterns (seven; every example is deleted from the table):**
    1. head + one of the language's settlement tails (village, town, city);
    2. head + a natural tail root (a village or a natural place);
    3. `the` + head + a region word (a region);
    4. `The` + a colour root + an animal root (an inn, a tavern);
    5. head + a building word (a quarter, a market, a building);
    6. a pooled person name + `'s` + a building word or a natural tail (a place called by its owner);
    7. a building word + `of` + a pooled god name (a temple).
    Region words: March, Reach, Vale, Fells, Moors, Wold, Coast, Isles, Deeps, Wastes, Heights, Fens. Building words: Market, Hall, Gate, Bridge, Cross, Wharf, Stair, Well, Mill, Tower, Shrine, Temple.
24. **A named place keeps its name in the Turkish narration, always** (owner, 2026-10-04, stated as important): "Wool Market" is written Wool Market in play, never "yün çarşısı". A proper noun is whatever the pool gave; it is never translated.
25. **Institution form words** (the word the rolled form puts in the name; `signatures.yaml#institution_form` gains a `name_words` list): Order · Guild · Company (the martial form only) · House · Council · League · School · Brotherhood, Sisterhood or Fellowship (rolled) · Cloister · Caravan, Fleet or Troupe for the travelling form (rolled; Fleet only when the palette holds a sea or fresh-water kind) · Society · Chartered Company (the owner's choice over "Charter") · Confederacy · Militia. "Privileged company" and "Travelling company" go as name words.
26. **Institution patterns (four):** `the` + root + form word; form word + `of the` + root; `the` + a pooled place name + form word; `House` + a family name from the language's person bag (the House form only, and its only pattern). "Court of…", "…Assize" and "Keepers of the…" are deleted. P4's other factions use the same patterns and words.
27. **People patterns (three):** root + `folk`; root + `kin`; root + `born`. "{Head}bound" and "the {Adj} Ones" are deleted.
28. **Phenomenon patterns (two, new):** `the` + root + a phenomenon tail, joined (the Thornfall) or apart (the Thorn Gift). Phenomenon tails (twelve): fall, song, call, turn, rise, bloom, mark, gift, shift, wane, sight, bind. Removed at the review: sleep, dream, change, breath.
29. **Month patterns:** root + `month`; root + `moon`; root + `fall`; and `High` or `Last` + root. The script rolls ONE of the first three per campaign and every month candidate uses it; the fourth names a special month or a feast. "…tide" stays deleted. Day: root + `day`.
30. **The ruin's old tongue exists in every campaign** (owner, 2026-10-04; widens decision 3). Nobody speaks it and it is not counted among the languages; it names only the sites the ruin source left (a column for P6). With "there is no common tongue" it is also the third language, as decision 3 says. Its names are words of its own sound bag (not English compounds), alone or with a site word: Vault, Deep, Hall, Gate, Stair, Spire, Tomb, Well (plural allowed). Its bag comes from a sound group no living language of the campaign uses.
31. **A language has no proper name.** The narration says "<the people's name>'in dili", "ortak dil", "eski dil".
32. **God epithets (four):** root + `bearer`; `Mother` or `Father` + `of` + root (plural); `Lord` or `Lady` + `of` + root (plural); `the` + a colour or age root + `One` (the owner keeps it). "the {Noun} Who {Verb}s" is deleted. **Ships (two):** `the` + an animal, sea or sky root; `the` + colour + animal. "{Name}'s {Noun}" is deleted.

### Part 5 — the pool (owner, 2026-10-04)

A trial built two sample campaigns' pools from the approved lexicon, bags and patterns (the development tab's throwaway script). It showed four faults, ruled on as follows.

33. **A share, not a weight** (replaces decision 4's ×3): half of a language's roots come from the tags it calls, half are drawn freely from the whole lexicon. Measured before: with 505 roots a ×3 weight gave 4 called roots of 12, and a landlocked world drew "cove".
34. **The calendar draws its own roots**, apart from the languages': one root per month and per day plus spares, only from the nature tags (crop, weather and season, cold, animal, forest, sky, fresh water), the palette's called tags first. A language's roots are left for places and institutions.
35. **Adjective roots (colour, direction and age)** are not used in the "of the …" patterns, in month and day names, in people names or in phenomenon names. They are used in place names, in `the` + root + form word, in inn and ship names and in "the … One".
36. **A language's draw always holds at least five heads and two natural tails**; the script ensures it while drawing, and a test counts that every scale's need of place names is met. Measured before: at short scale (8 roots, 6 tails) 15 of 2,000 draws could build fewer than 30 place names, the worst 11.
37. **Spread and joins in the pooled compounds** (found in the trial, to be written as rules): one head root appears in at most a few names of a stock (the trial gave Monkcote, Monktoft, Monkend, Monkfork); no doubled letter at a join (Hooffolk); head and tail differ; a length cap.
38. **Candidates and stocks:** four candidates for each signature name, the writer picks one; bulk names (places, regions, inns, months, days, ruin sites) come from a stock per language, as persons do today.
39. **The card shows the chosen names only;** the candidates stay in the file.
40. **The owner's reroll:** one command gives four fresh candidates for one signature slot at the review stop; only the owner uses it.
41. **A secret stock:** a separate dm-only stock from the same bags and roots for secret entities; printed in no public output; the door looks both ways.
42. **Famous real places are filtered;** an obscure real village name passes.
43. **Which language names what.** The people's name: the people's language. The institution: the common tongue; its own language when it has one; the other side's when there is no common tongue. The phenomenon: the common tongue; the people's language when there is none. Places: the region's language (P3 assigns it; P1 prepares a stock per language). Ruin sites: the old tongue. Months and days: the calendar's own roots.
44. **Root counts raised after a measurement** (owner, 2026-10-04: "standard and epic may need more"). Over 1,500 draws per case, one head in at most three names: at 12 roots a standard language can build as few as 15 place names (median 27) and holds as few as 5 heads for 6 regions; at 15 an epic campaign's three languages together reach exactly the 72 names that three times its 24 settlements ask, with nothing left for play. The counts become short 10, standard 18, epic 24, with a head floor of 5, 9 and 12 (four of them nouns). A birth then uses about 43, 77 and 95 of the 505 roots (the languages plus the calendar's 23), so the lexicon turns over in about twelve, seven and five births. The same measurement showed that a language rarely holds both a colour and an animal root (12 %), so inn and ship names draw those from the whole lexicon.
45. **Everything is written in English** (owner, 2026-10-04; `docs/p1-build-13.md`): the Turkish glosses of this file's review were for the owner only; a language's label is English; the Turkish suffix rules belong to play. Where a decision above speaks of Turkish narration in a design file, this holds.
