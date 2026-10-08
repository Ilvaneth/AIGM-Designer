# P2 (cosmos) survey — what it rolls, what it leaves to the writer, what P1 promises it

*Written 2026-10-08 for the design tab's row review with the owner, the way P1 was rebuilt (docs/p1-tags.md, docs/p1-threat-first.md). Read-only survey at HEAD dc9bc08; no campaign file and no dm-only file was read. Paths are relative to `.claude/skills/dnd/` unless they start with `docs/`.*

**In one paragraph.** P2 makes about 58-75 public dice records at standard scale, and none are secret. Of its 28 sub-tables (262 rows), 18 are rolled. The other 10 sub-tables are never rolled: every planes table, plus the pantheon's domains, ranks, churches, relations and god secrets. The writer chooses from those as it likes. The five P2 tables carry no `layer`, `claims`, `requires`, `conflicts_with` (beyond one pair) or `weight_by`, and no reviewed stamp. The only foundation input any P2 roll reads is the ancestor-gods override. P1 promises P2 72 live hooks and 8 overrides. One override is applied by script; everything else goes to the critic.

---

## A. What P2 does today

### A.1 The preroll, in order (`scripts/designer.py:362-403`)

| # | Label(s) | Table | How many | avoid_used | Constraint / gate |
|---|---|---|---|---|---|
| 1 | `pantheon_type` | `pantheon.yaml#type` | 1 | False | **Forced** when a rolled trope break's `overrides` names `pantheon_type` with a `to` that is a type row id (:366-374). Today only `break_gods_are_ancestors_known` → `pantheon_ancestor_gods` qualifies. |
| 2 | `pantheon_presence` | `#presence` | 1 | False | none (:377) |
| 3 | `magic_source`, `magic_constraint`, `magic_visibility`, `magic_regulator` | `magic.yaml#…` | 1 each | True | none. The regulator is rolled even when a P1 row overrides it (:378-379). |
| 4 | `magic_taboo.1`, `taboo.second` (d2), `magic_taboo.2` | `#taboo` | 1-2 | True | A second taboo on a d2 = 2, if the first ≠ `taboo_none`. It excludes the first taboo and `taboo_none` (:380-382). |
| 5 | `wild_gate`, `wild_shape` | dial `magic.effects.wild_magic_roll`; `#wild` | 2 | False | Gate: d6 on [1] at low, [1,2] at medium, [1,2,3] at high (`dials.yaml:110,124,137`). A hit draws from `#wild` minus `wild_no`; a miss forces `wild_no` (:383-388). |
| 6 | `climate` | `calendar.yaml#climate` | 1 | **True** | none: it reads no palette, spine or era (:389-390) |
| 7 | `year_shape`, `week`, `moon`, `start_anchor` | `calendar.yaml#…` | 1 each | False | none (:389-390) |
| 8 | `ages_count`, `age.n` | `history.yaml#age_template` | 3-5 (`scale.history.ages`) | True | distinct within the birth (:391-394) |
| 9 | `events_count`, then `event.n`, `divergence.n`, `memory.n` per event | `#event_type`, `#divergence`, `#memory` | 8-12 events × 3 | False | none; types may repeat (:395-398) |
| 10 | `deep_count`, `deep.n` | `#event_type` | 3-5 | False | none (:399-400) |
| 11 | `festival.n` | `calendar.yaml#festival_type` | **fixed at the top of the gods band**: 5 / 9 / 14 | False | distinct (:401-403). At epic, 14 of 16 rows are drawn. |

**Never rolled:**
- The number of gods (band 3-5 / 6-9 / 9-14) and the great gods (0-1 / 1-2 / 2-4, `scale.yaml:59,91,123`).
- The rank split (`pantheon.yaml#rank` shares).
- Each god's domains, alignment, symbol, church archetype, relations and secret.
- The touched-plane count (1 / 1-2 / 3-6 plus the magic dial's `planes_touched_modifier`, which no script reads).
- Every `planes.yaml` table. Its header (`planes.yaml:17`) and the plan (`docs/campaign-designer-plan.md:632`) both promise deviation, rate, way-in and cost rolls that were never built.
- The regulator's strictness: a dial effect with no record.

The prompt's scale line shows these bands raw (`scripts/design_prompts.py:128`); it does not mention the great gods.

### A.2 What the writer decides freely (`prompts/design/P2.cosmos.md:24-28`, `templates/design/cosmology.md`)

| Area | Left to the writer |
|---|---|
| Pantheon | How many gods within the band; the greater / lesser / power split; which gods are "great" (church = faction). This is absent from the prompt. For each god: 1-2 domains under the coverage rule (`pantheon.yaml:19`), alignment, symbol, worship, disposition, church (a faction or an institution), relations (picked from 11 patterns) and a secret with a tier (picked from 12 rows). Also which god embodies the villain's answer and which the world's (`P2.cosmos.md:24`). Only the name and the epithet come from a pool. |
| Planes | A verdict for each of the 26 baseline rows (unchanged / renamed / merged / removed / is-this-world / touched). Which planes are touched and how many. For each touched plane: way in, cost, time rate, keeper, a reserved P6 site id and the local name (no pool). The primer's rule line on spells. |
| Magic | The availability text. The signature phenomenon written "as a rule with a cost" (P1 rolled its rule, sign, limit and user). Which faction regulates, and who sells identify and training. How the unapplied overrides change the rolled regulator. |
| History | The years, spans and order of the rolled ages; age names (no pool; three labels are `{Name}`, `{Thing}`, `{Rulers}` templates). Which event falls in which age. Event names (no pool), years, taught and true texts. Which slot is the break or move, the villain's origin, the institution's founding, the start settlement's founding and the ruin's age (`history.yaml:14` "pins"). Witness roles. |
| Calendar | The per-month tone from the season template. Moon names and the moon's phase on day 0 (no pool). Festival names (no pool), dates and the god of each. The start day and year. The `calendar.py init` line. Month and day names come from the pool. |

The writer also fills every registry field: rank, domains, `day`/`year`, `dm_only.happened`, stamps. P1 has a script-built frame for its rows (`scripts/design_frame.py`, build 20a); P2 has none.

---

## B. The P2 sub-tables

Counts are rows. "Rolled" refers to A.1. Hooks are given as self (P2) / back (P1) / forward (P3-P9).

### B.1 `pantheon.yaml` (7 sub-tables, 56 rows; hooks 22 self / 2 back / 36 forward; common hooks: P2, P4, P8)

| Sub-table | Rows | Columns | Rolled | Verdict |
|---|---|---|---|---|
| `type` | 5 (weights 3/1/1/2/1) | rule, effects {cleric_spells, festivals, primer_line}, hooks; dead ↔ silent `conflicts_with` | yes | **Thin** next to the DMG ch.1 religion systems (loose and tight pantheons, mystery cults, monotheism, dualism, animism, forces and philosophies): monotheism, animism/spirits and philosophies are missing. Two of the five rows are absences (dead, silent) and carry 3 of 8 weight. A test pins the exact five ids (`tests/test_design_tables.py:294`). |
| `presence` | 6 | rule, hooks | yes | Adequate. It clashes with type and the trope breaks and nothing stops it (D.16). `presence_through_phenomenon` hooks P1, which is backward (:114). |
| `domain_scaffold` | 8 | alignments, symbol_kinds, church_shape, folk_ask_for, festival_kind, faction_affinity, secret_tendency | no | These are the PHB's seven domains plus the DMG's Death. **The SRD 5.1 prints only the Life domain** (`data/srd-5.1-yaml/02-classes.yaml`), so this is a ruleset question. `festival_kind`, `faction_affinity` and `secret_tendency` are read by no script. Life, Light and Nature offer no evil alignment. |
| `rank` | 3 | share by scale, can, cannot, naming | no | The shares add up to 2-6 / 5-10 / 9-15 against the gods band of 3-5 / 6-9 / 9-14. "Greater" (`can: have a church with a faction`) overlaps `scale.great_gods`: two owners of one target (rule 9). |
| `church_archetype` | 11 | hierarchy, services, fracture_seed, faction_archetype | no | Rich. It overlaps P4's faction archetypes; tribunal and watch house belong to the lamp/tribunal family. |
| `relationship` | 11 | shows_in_worship, shows_in_factions | no | Good variety. `rel_mirror` assumes a villain's god (:387). |
| `god_secret` | 12 (7 secret tier, 5 discoverable) | tier | no | "Every god has one" (:396), so 6-14 secrets per birth that are tied to nothing: finding 4's class. `godsecret_villains_patron` duplicates P1's pin relation. |

### B.2 `planes.yaml` (5 sub-tables, 56 rows; hooks 35 self / 3 back / 18 forward; header `avoid_used: false`)

| Sub-table | Rows | Columns | Rolled | Verdict |
|---|---|---|---|---|
| `baseline` | 26: Material, 2 transitive, 4 elemental + Chaos, 16 Outer by alignment + hub, demiplanes | group, srd, spells, alignment/tier/shape (outer), touch_bias (3) | no | The Great Wheel is complete. **Missing:** the Feywild and the Shadowfell, which SRD spells name (Dispel Evil and Good sends undead to the Shadowfell and fey to the Feywild; Forbiddance; `data/srd-5.1-yaml/08-spellcasting.yaml`). Also the Far Realm (`power_elder_mind`: "outside the planes the gods keep") and the energy planes. The 16 Outer rows repeat one hook word for word. `touch_bias` is read by no script, and its `tone_shadowed` (:74) survives the deleted tone planes modifier (`docs/p1-tags.md:61`). |
| `deviation` | 8 (unchanged ×3, renamed ×2) | rule | no (the header says yes) | `dev_secret_holds` would be a *public* roll naming where the secret lies, and it still says "Act 3 clue" (:307). `dev_is_this_world` cites the retired `secret_planes_are_one` (:302). `dev_inverted`'s hook is a prose requirement (:299). |
| `time_rate` | 6 | rate / rate_range | no | Good D&D (the Feywild-style time warp). `rate_fast` names "the doom clock" (:335). |
| `way_in` | 8 | rule | no | Good. `way_mirror` and `way_phenomenon` hook P1, which is backward (:385, :390). |
| `cost` | 8 | label only | no | Good. `cost_name` points at "naming.json's rite of naming" (:411), which no table defines. |

### B.3 `magic.yaml` (6 sub-tables, 56 rows; hooks 13 self / 6 back / 37 forward)

| Sub-table | Rows | Rolled | Verdict |
|---|---|---|---|
| `source` | 12 | yes | Broad. It does not read the dial's claim (scarce / middling / plentiful) or the ruin's `magic: faded`. `source_the_sleeper`'s P7 hook "the doom is the waking" (:97-99) makes texture the doom (G10). `source_a_dying_thing` creates a secret of its own (:79-81). `source_names` and `source_the_phenomenon` hook P1, which is backward. |
| `constraint` | 10 | yes | Fine. `constraint_none_known` reads "the constraint is the secret" (:151-153). |
| `visibility` | 6 | yes | Fine. `avoid_used` on a 6-row table spends it in six births. |
| `taboo` | 12 (1-2 drawn) | yes | Fine. `taboo_none`, and any taboo at all, sit beside `break_casting_forbidden` unchecked. `taboo_casting_on_a_day` needs a festival, which nothing seats. Two rows hook P1, which is backward. |
| `regulator` | 9 (signature institution ×3) | yes | It is rolled even when one of three P1 rows overrides it (D.8). No row says who sells identify and training (`docs/p1-tags.md:72`). `regulator_church` asks for a "Law-adjacent" domain (:262), which does not exist. |
| `wild` | 7 | gated | Fine. `wild_dead_god_static` requires a dead or silent pantheon, but only in prose (:306). `wild_planar_bleed` needs a touched plane, and no roll sets one (:296). |

### B.4 `calendar.yaml` (6 sub-tables, 45 rows; hooks 18 self / 2 back / 25 forward)

| Sub-table | Rows | Columns | Rolled | Verdict |
|---|---|---|---|---|
| `climate` | 8 (temperate ×3, maritime ×2) | seasons with a four-sense tone, hazards | yes, avoid True | The season templates are good and feed the felt-season rubric. **There is no link to the palette, spine or era.** `climate_underground` can be drawn in any era, and P3's biome filter (`scripts/designer.py:415-416`) then restricts every region to the two biomes that list it (`regions.yaml`: caverns, fungus deeps). `avoid_used` pushes toward the climates other births did not use, not toward ones that fit the land. |
| `year_shape` | 4 | months, intercalary, year_days | yes | Fine. `year_thirteen_moons` requires one moon, in prose only (:138). |
| `week` | 4 | days | yes | Fine. Every week length divides 30. |
| `moon` | 7 | — | yes | `moon_is_a_plane` needs a plane roll. `moon_tidal` hooks P1, which is backward. Clashes: D.7. |
| `festival_type` | 16 | domain_affinity | yes, distinct | Count = the top of the gods band, whatever gods are written; epic gets 14 of 16 (no variety). `domain_affinity` is unread. `fest_naming` points at the missing rite of naming (:232). |
| `start_anchor` | 6 | — | yes | It does not read the break's time (G2) or the start (D3). |

### B.5 `history.yaml` (4 sub-tables, 49 rows; hooks 13 self / 2 back / 34 forward)

| Sub-table | Rows | Rolled | Verdict |
|---|---|---|---|
| `age_template` | 14 | 3-5, distinct, avoid True | Positional rows (`age_founding` comes first, `age_before` is the deep past, `age_now_named_for_fear` is the present) are mixed with thematic ones. A draw of 3-5 often lacks the present row the prompt always asks for (`P2.cosmos.md:27`). The ruin's age is not drawn from the ruin. `age_dimming`'s hook says "a clock the doom completes" (:61, G10). |
| `event_type` | 16 | 11-17 draws (dated + deep), avoid False | Broad (compare the DMG's cataclysms). The move is not among the rolled events, and the types do not read the break's action or the villain's origin. |
| `divergence` | 12 (`div_none` ×3; 6 secret, 5 discoverable, 1 public tier) | 8-12, **public** | The secret tiers are 6/14 of the weight, about 43 % of draws, and they appear in the public log (D.14). |
| `memory` | 7 | 8-12 | Fine. `mem_the_dead`'s P1 hook is a prose requirement (:251). |

**The lamp / silence / tribunal family across P2:**
- Rows: `pantheon_silent_gods`; Light's symbols (lamp, candle, beacon); the lamplighters and tribunal churches; `church_watch_house`; `church_tribunal`; `rel_silenced_one`; `rel_trial`; `godsecret_not_silent`; `fest_lighting`; `fest_lament`; `fest_silence`; `age_silence`; `age_dimming`; `age_reckoning`; `evtype_silencing`; Death's "extinguished lamp".
- Errata #30 keeps the history rows among them as general rows; the rest are the owner's call.

---

## C. P1 → P2 links

### C.1 P2 hooks per source table

| Source | P2 hooks | Live | Notes |
|---|---|---|---|
| `foundation.yaml` | 21 (4 table-wide + 17 on rows) | 21 | Plus 2 overrides on `contest_casters_casterless` (:1438), plus the ledger's generated `break.event` (`scripts/design_promises.py:257`) |
| `signatures.yaml` | 1 (`phenomenon_rule` table-wide, :210) | 1 | |
| `trope-breaks.yaml` | 13 | 13 | Plus 6 overrides on 4 rows due at P2 (:88, :171, :219, :408) |
| `secrets.yaml` | 23 | 14 | 9 sit on retired rows (8 archetypes, 1 chooser) |
| `antagonists.yaml` | 25 | 21 | 1 retired (`bond_product_of_it`). 3 sit on tables P4 rolls (`front_trial` :399, `doom_god_answers` :440, `lever_date` :453), so they can never be kept at P2. |
| `dials.yaml` | 1 (`era_underground` :202) | 1 | Plus the magic effects: wild gate (used), strictness (no record), planes modifier (unused) |
| `scale.yaml` | 1 (`counts_epic` :128, 500 years) | 1 | Plus the counts in A.1 |
| `claims.yaml` | 4 defaults owned by P2 (:83-86) | — | `regulator_strictness`, `regulator_identity`, `pantheon_type`, `great_gods_floor` |
| `tensions.yaml`, `naming.yaml` | 0 | 0 | naming supplies the god, epithet, month and day pools |
| ledger placements | 2 (`design_promises.py:417-421`) | 2 | The pinned god and the pinned event, checked by `god_registered` / `event_dated` |

**Totals:** 85 hooks, 72 of them live. Of the 8 overrides, 1 is applied by script.
- Every live hook is judged by the critic: none carries a `check:` rule.
- Hooks on secret rows go to the secret ledger.

### C.2 The hooks grouped by what they ask

| # | Group | Sources (live hooks) | Today |
|---|---|---|---|
| L1 | **The move as a dated event** | action common, time common (`foundation.yaml:1958, :2335`); secrets common (`secrets.yaml:26`); twist `secret_history_looping`. Total: 4, plus the generated `break.event`. | **Promised.** No roll dates it, the time rows carry no years (`foundation.yaml:2338-2357`), and the move is not among the rolled event types. |
| L2 | **The past P1 names** | ruin common "one age of the history is this fall" (:416); `break_the_enemy_won` "the founding event is the defeat" (:323). Total: 2. | **Promised.** The age roll ignores the ruin (`designer.py:393-394`). |
| L3 | **Origins of fantastic kinds** | palette common (:50). Total: 1. | **Promised.** |
| L4 | **Which plane** | `land_thin_place`; `target_thin_place`; seven ruin rows (celestial war, elven withdrawal, planar rift, planar invasion, devils' bargain, demon gate, sleeping realm); `act_merged_with_plane`; `scar_plane_thinned`; `break_moon_trades`; `break_dreams_are_a_place`. Total: 13. | **Ignored by the rolls**: no plane is rolled. The rule "shared to fit the scale's count; at short all one plane" (`docs/p1-tags.md:167`) is the writer's job. |
| L5 | **The magic system against P1** | phenomenon common; `scar_magic_rule_changed`; `scar_time_flow_changed`; `break_magic_is_nobility`. Total: 4 hooks. Overrides: `regulator_identity` ×3, `regulator_strictness` ×2. | The wild gate is scripted. **The overrides are ignored**: the regulator is rolled anyway, and a critic judges the result. |
| L6 | **Gods named by public P1 rows** | `scar_god_changed`, `scar_new_belief`, and the trope breaks ancestors, holy ground, forbidden name, gods among mortals, the chosen, the dead rise. Total: 8. Overrides: `pantheon_type` ×2, `great_gods_floor` ×1. | **One override scripted** (ancestors → forced type; `script:override_applied`, `design_promises.py:489-494`). "Among mortals" narrows the type in text only (`trope-breaks.yaml:219`), so it is unapplied, and so is its great-gods floor. The rest is critic-judged. |
| L7 | **The gods and powers of the threat (secret)** | `god_relation` ×5; `greater_power` ×4; `twist_greater_power`; `family_god`; `power_pact`; `power_serves`; `origin_bargain`; `origin_conversion`. Total: 15, plus the placement for the pinned god. | P1 rolls the pin's relation (`design_identity.py:379-386`). At P2 it is **promised**; `god_registered` checks only that the name exists as a god. |
| L8 | **The villain's past in the history (secret)** | the shapes heir, peacemaker, survivor and oathkeeper; the origins choice, loss, awakened, refused death, cursed and forbidden knowledge; `power_curse`; the weaknesses true name, prophecy, law of nature and rite; `secret_the_hero_failed`; `trail_omen_divination_dead`. Total: 17. | **Promised.** The public event, divergence and memory rolls do not read them. |
| L9 | **The calendar** | `scar_sky_changed`, `scar_seasons_broken`, `era_underground`, `break_night_is_safe`, `break_dead_month`, `break_lawless_day`, `weak_vulnerable_time`. Total: 7 (plus `lever_date`, which comes from P4). | **Promised.** Climate, moon and year are rolled blind to them. |
| L10 | **Scale** | epic covers 500 years. Total: 1. | Shown in the scale line; no check. |

L1-L10 together: 4+2+1+13+4+8+15+17+7+1 = 72.

---

## D. Structural gaps against the P1 method

1. **Planes have no roll at all.**
   - The header, the plan and the prompt all expect rolls (`planes.yaml:17`, plan :632, `P2.cosmos.md:25`); `preroll_p2` makes none.
   - `scale.planes_touched` and `planes_touched_modifier` (`dials.yaml:111,125,138`) are read by no script.
   - 13 P1 promises (L4), the moon trade, the fiend lord's domain and `source_the_planes` all need a chosen plane.
2. **Counts the writer picks.** These are not rolled:
   - the gods count, the great gods (with the raisers listed in `docs/p1-tags.md:583`) and the rank split;
   - the touched planes.
   - `great_gods` is read by no script and does not appear in the P2 prompt.
   - The festival count is the gods band's top, not the gods the birth actually has (`designer.py:402`).
3. **The pantheon ignores the foundation and the threat.**
   - Type and presence have no `requires`/`weight_by`, so they do not read:
     - the ruin's gods family (5 rows, `foundation.yaml:500-535`; ruling `docs/p1-tags.md:168`);
     - `family_god` (`antagonists.yaml:211`);
     - `power_god` (`secrets.yaml:161`);
     - the religious contest roles;
     - the pilgrim road (`docs/p1-tags.md:191`).
   - The pantheon rule (`pantheon.yaml:22`), the prompt (:24), the template (:13, :85) and the rubric (`rubrics.yaml:41`) all demand "the villain's god" in every birth. W1 pins a god only when the threat calls for one (`design_identity.py:379-386`). **The writer decides it: W1 reopened.**
4. **Texture secrets** (finding 4, `docs/p1-threat-first.md:14, :54`).
   - Every god has a secret (`pantheon.yaml:396`); 7 of the 12 rows are secret tier.
   - Other hidden truths of their own: the divergence secret tiers, `constraint_none_known`, `source_a_dying_thing`, `dev_secret_holds`.
   - The prompt says "the big secret usually hides in this layer" (`P2.cosmos.md:16`). The template has "Where the big secret hides in this layer" (`cosmology.md:88`) and "the big secret's origin" as a pin (`history.yaml:14`).
5. **History ignores the chain.**
   - The ages are drawn without the ruin (`designer.py:393-394`).
   - The move, the villain's origin, the institution's founding and the start's founding are not seated by script.
   - The time rows give no years, so "a generation ago" becomes whatever year the writer picks.
   - Villain shapes that need a treaty, a disaster or an oath event, and `origin_choice_in_history` "has a divergence", meet public event and divergence rolls that may contain none of these.
6. **Climate against the palette, era and spine.** Already listed in plan Floors #11 (plan :923) and `docs/p1-tags.md:161`.
   - `calendar.yaml#climate` has no `requires`.
   - The palette kinds already carry biomes, and the biomes carry climates (`regions.yaml`), so the pool is derivable.
   - `era_underground` does not force `climate_underground`, and other eras do not exclude it. P3 then restricts every region to two biomes (`designer.py:415-416`).
7. **Calendar clashes nothing prevents.**
   - `year_thirteen_moons` (`calendar.yaml:132-138`) with `moon_two` / `moon_dark` / `moon_none_stars`.
   - `break_moon_trades` (`trope-breaks.yaml:177-188`) with `moon_none_stars` / `moon_dark`.
   - `break_night_is_safe` ("the moon marks the working hours") with `moon_none_stars`.
   - `start_anchor` with the time row (G2, `docs/p1-threat-first.md:107`) and with the plan's first step at the start (D3).
8. **Overrides unapplied.**
   - `regulator_identity`: `trope-breaks.yaml:88`, `:408`; `foundation.yaml:1438`.
   - `regulator_strictness` ×2.
   - `great_gods_floor`, and the type narrowing (`trope-breaks.yaml:219`).
   - `designer.py:371` applies only an override whose `to` is a row id. `SCRIPT_APPLIED` lists `pantheon_type` alone among P2's defaults (`design_promises.py:77, :341`).
9. **Requirements written as prose hooks** (rule 5: a row that names "the X" needs `requires`).
   - `wild_dead_god_static` :306, `year_thirteen_moons` :138, `regulator_church` :262, `regulator_the_dead` :278, `mem_the_dead` :251, `godsecret_usurper` :442, `evtype_silencing` :160, `dev_inverted` :299.
   - Plus the **15 P1-phase hooks inside P2 tables**, which can never be kept because P1 is sealed before P2 rolls (`presence_through_phenomenon`, `godsecret_is_the_phenomenon`, `way_mirror`, `way_phenomenon`, `cost_name`, `source_names`, `source_the_phenomenon`, `taboo_naming`, `taboo_the_phenomenon_unlicensed`, `regulator_signature_institution`, `wild_overflow`, `moon_tidal`, `fest_naming`, `evtype_naming`, `mem_the_dead`).
10. **Stale references.**
    - The "rite of naming" (`planes.yaml:411`, `calendar.yaml:232`) exists in no table.
    - "Act 3" (`planes.yaml:307`) and the retired archetype (`planes.yaml:302`).
    - "Church faction only in epic" (`pantheon.yaml:21`, `P2.cosmos.md:24`, `cosmology.md:23`) is superseded by `great_gods`.
    - The template's planes count "0-1 / 1-2 / 3+" (`cosmology.md:31`); the real counts are 1 / 1-2 / 3-6.
    - The template's magic "Source" list (`cosmology.md:35`) does not match the table's rows.
    - P4-rolled rows hook P2 (`antagonists.yaml:399, 440, 453`).
11. **Texture as the doom** (G10, `docs/p1-threat-first.md:115`): `source_the_sleeper` (`magic.yaml:94-99`), `age_dimming` (`history.yaml:61`), `godsecret_fading` (`pantheon.yaml:432`), `rel_trial` (:393), `rate_fast` (`planes.yaml:335`).
12. **Inspection is missing.**
    - P2's own 150 row-level and 8 common forward hooks never enter the ledger (`SOURCE_PHASES = ("P0", "P1")`, `design_promises.py:66`).
    - No P2 table is in `reviewed.json` (its `_meta.tables` lists none).
    - No P2 table has a `layer` key (required by `docs/p1-threat-first.md:30`).
    - There is no P2 frame and no `design_check.py` module for gods, domains, festivals or event counts.
    - Only 3 rubrics exist (`rubrics.yaml:41-43`). None asks whether the cosmos serves the threat (its power, weakness and lair have a place) or whether it reads as D&D: a cleric PC can pick a god and a domain, and the planes answer the SRD spells.
13. **Names without pools** (errata #25, plan :595): plane local names, ages, events, festivals and moons. `naming.yaml`'s patterns stop at place, institution, people, phenomenon, month, day, old tongue, god epithet and ship (:778-813). `docs/p1-tags.md:809` already lists the planes.
14. **Secrecy.**
    - Every P2 roll is public.
    - 6 of the 12 divergence rows are secret tier (about 43 % of draws), so the public log can tell the owner, who is also the player, things like "this event never happened" or "the villain of the story was the victim".
    - Any binding to the pin or the threat (L7, L8) must be a secret roll or a forced secret record. The machinery already exists:
      - P1's secret rows enter P2's context (`design_dice.py:175-200`);
      - the arbiter moves exclusions that name them to the secret side and hides the true die size (`public_view`).
    - The P2 tables use none of this.
15. **Usage contradictions.**
    - The headers of pantheon, magic, calendar and history say `avoid_used: true`.
    - The preroll passes `avoid=False` for type, presence, year, week, moon, anchor, events, divergence, memory, deep events and festivals (`docs/p1-tags.md:607`, still open).
    - Meanwhile `design_compare.py:30` treats all of `pantheon.yaml` as unique across campaigns.
16. **Inner clashes nothing prevents:**
    - `presence_walking` × `pantheon_dead_gods`;
    - `presence_never` × `break_gods_among_mortals`;
    - any taboo or `taboo_none` × `break_casting_forbidden`;
    - `pantheon_dead_gods` / `pantheon_silent_gods` × `break_gods_among_mortals`;
    - `visibility_invisible` × `constraint_echo` (soft).

---

## E. Proposed review order

**Already ruled; do not re-decide** (`docs/p1-tags.md` §§2-3):
- At least one touched plane at every scale.
- The planes the foundation names are shared to fit the count; at short they are one plane.
- Great gods: 0-1 / 1-2 / 2-4, raised by a religious contest role, by "gods among mortals" (at least 1) and by the unnamed god's priests. Their churches count inside P4's total.
- The dial sets how strict the regulator is; P2's roll sets who. Three rows override who.
- Who gives the magic services is answered for every regulator row.
- The pantheon follows a gods-family ruin, and the ruin's god is a fallen, faction-less god.
- P2 writes the origin of every fantastic kind the ruin did not bring.
- The climate derives from the palette.
- The empty month and the lawless day fall inside the campaign's span.
- No real-world mythology names.
- Months are 30 days.

| Session | Sub-tables (rows) | The owner decides |
|---|---|---|
| **S0 — Method** (no rows) | — | 1. The `layer` of each P2 table (proposal: the pinned god and the move's and origin's events are **story**; the planes the foundation names are **stage**; calendar, festivals, climate, most of magic and the unpinned gods are **texture**). 2. The roll order: the threat's pin and powers first (secret), then the planes P1 names, then the pantheon, the history's seated events, magic, and the calendar last. 3. Which of the 10 unrolled sub-tables become rolls. 4. Whether the counts (gods, great gods, ranks, planes) are rolled. 5. P2 joins the ledger's `SOURCE_PHASES` and gets a frame. 6. What happens to the 15 backward P1 hooks (delete, or turn into `requires`). 7. Whether P2 may hold any secret beyond the threat's (finding 4). |
| **S1 — Pantheon I** | type (5), presence (6), rank (3); the counts | 1. Add the DMG systems (monotheism, animism, philosophies)? Keep two absence rows at 3/8 weight? (The test pins the five ids.) 2. How the type follows a gods-family ruin (weights or `requires`). 3. Apply "gods among mortals" as conflicts (dead, silent, `presence_never`) and set its great-gods floor. 4. A `family_god` threat or a `power_god` patron: one of the scale's gods? Which rank? Read in secret? 5. Do "greater" rank and "great" god merge (rule 9)? Roll the gods, great gods and rank split? 6. The pilgrim road's god: a great god? 7. presence × type clashes. |
| **S2 — Pantheon II** | domain_scaffold (8), church_archetype (11), relationship (11), god_secret (12) | 1. Domains: the SRD has only Life; keep the PHB's 7 plus the DMG's Death? 2. Roll domains to the coverage rule, alignment from the scaffold, church and relations, for every god or only the great ones? 3. God secrets: keep one per god, cut, or allow only as a medium of the threat's secret? Which of the 12 survive? `godsecret_villains_patron` against the pin. 4. At least one evil god whose cult can be a hand? Gods of the peoples? 5. `rel_mirror` and "the villain's god" in every birth, or only when W1 pins one? 6. Who owns a church's form, P2's church or P4's archetype? 7. The lamp/tribunal rows. |
| **S3 — Planes** | baseline (26), deviation (8), time_rate (6), way_in (8), cost (8) | 1. Roll the touched count (scale plus magic's +1). Seat the planes P1 names first, by rule (devils → the lawful evil plane, demons → the chaotic evil plane, the elves' withdrawal → …). 2. Add the Feywild and the Shadowfell (named in SRD spells), the Far Realm, the energy planes? 3. Deviation: rolled for every row, or only for touched or flagged ones? Delete `dev_secret_holds` / `dev_is_this_world` or fix them. 4. Roll rate, way and cost per touched plane; where the keeper comes from. 5. Define the "rite of naming" or reword `cost_name`. 6. Pools for plane names. 7. One common hook in place of the 16 copies. |
| **S4 — Magic** | source (12), constraint (10), visibility (6), taboo (12), regulator (9), wild (7) | 1. The three regulator overrides become a forced record (no roll). 2. Who sells identify and training under each of the 9 rows. 3. Does the source read the dial's claim and the ruin's `faded`? 4. Texture-as-doom (`source_the_sleeper`) and self-secrets (`source_a_dying_thing`, `constraint_none_known`). 5. Taboos under "casting is forbidden"; the taboo day needs a seated festival. 6. Turn the wild rows' prose requirements into `requires`. 7. `avoid_used` on 6- and 7-row tables. 8. A phenomenon that is a spell during "the empty month" (`docs/p1-tags.md:526`). |
| **S5 — History** | age_template (14), event_type (16), divergence (12), memory (7) | 1. Seat by script: the move (its year from the time row), the ruin's age, the villain's origin event (secret), the institution's founding, the start's founding. Do they count inside the 8-12? 2. Divergence: secret tiers rolled secretly, cut, or kept only where the threat uses them? 3. Seat the positional ages (first, deep, present) and roll only the middle. 4. The same 3-5 ages and 8-12 events at short? The witness lists against P5's NPC caps. 5. `age_dimming`'s doom hook; names for `{Name}`/`{Thing}`/`{Rulers}` and events (pools?). 6. Event repeats and the deep past sharing one table. 7. `mem_the_dead` as a `requires`. |
| **S6 — Calendar** | climate (8), year_shape (4), week (4), moon (7), festival_type (16), start_anchor (6) | 1. Derive the climate pool from the palette kinds' biomes; force `climate_underground` in the underground era and exclude it elsewhere; drop `avoid_used`. 2. A moon is required by the moon trade, night is safe, thirteen moons and the vulnerable time; does `moon_is_a_plane` count as a touched plane? 3. The festival count: from the gods actually written (one per greater god, one per season), not the band's top; bind by `domain_affinity`. 4. Seat the dead month, the lawless day, the taboo day and the dead days as dates; who sets "inside the span" before P7's doom? 5. Start anchor from the break's time (G2) and the plan's first step (D3): keep the 6 rows? 6. The underground calendar (`dials.yaml:202`, `calendar.yaml:112`). 7. Pools for moon and festival names. |
| **S7 — Writer, critic, card** | `P2.cosmos.md`, `templates/design/cosmology.md`, rubrics (3) | 1. Rewrite both to the chain: drop "the big secret hides here", keep the villain's god only when pinned, use the great gods and the real planes counts and the source rows. 2. Rubrics: rewrite the gods/question one around the pin and the threat's powers; add a D&D legibility rubric (a cleric PC chooses god and domain; the planes answer the SRD spells; the threat's dates are on the calendar). 3. Script rules for the ledger (gods count, domain coverage, festivals per greater god, a dated move event, a touched plane per foundation-named plane). 4. Reviewed stamps for the P2 tables. |

Every session ends the way P1's did: the decisions go to `docs/p1-tags.md` (or a new `docs/p2-tags.md`), the specification goes to the coding tab, and the tests that pin row lists (`tests/test_design_tables.py:292-406`) change with the rows.
