# `entities.json` — the registry (canonical) and its public projection

Plan item 3, errata 24.2 #1 / #2 / #14, owner decision 24.6 #1.

Two files, one shape:

- **Canonical:** `design/dm-only/entities.json`. Every entity, every field. Written only by `registry.py merge` (upsert by id from staging fragments) and `design_revise.py` (the one sanctioned writer of stamped fields). Never opened by the conductor.
- **Projection:** `design/entities.json`. Regenerated from the canonical file on every merge by two mechanical rules: **drop every entity whose `secrecy` is `secret`**, then **drop the `dm_only` object of every remaining entity**. Nothing else changes, so the projection needs no schema of its own. It is the only registry the conductor, `campaign_search.py`, the phase cards and `render_player.py` read.

## Envelope

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "written_by": "registry.py merge --phase P9",
    "written_at": "2026-09-24T20:00:00Z",
    "stamp_snapshot": "design/dm-only/_snapshots/stamps.json",
    "projection": "design/entities.json",
    "counts": {"god": 3, "npc": 8, "site": 4, "faction": 3, "settlement": 2}
  },
  "entities": {}
}
```

`entities` is an object keyed by id (an object, not a list, so merge is an upsert and lookups are O(1)). `_meta.counts` is recomputed on every merge from the canonical file, so the scale check sees the full count while the card only prints "scale band ✓".

## Common fields (every entity)

| Field | Type | Notes |
|---|---|---|
| `id` | string | equals the key |
| `type` | enum | the id prefix without the underscore |
| `name` | string | in the narration language; secret entities keep it here only |
| `aliases` | string[] | every name play has used; the "in-play name ≠ file name" fix (16.2) |
| `summary` | string | one line, public voice even on secret entities (used by the index) |
| `file` | string or null | prose file relative to the campaign dir; null for a registry stub (`status: pending`, errata 24.2 #10) |
| `secrecy` | enum | `public` / `discoverable` / `secret` |
| `created_phase` | string | `P0` … `P9`, or `play` for entities registered during play (`registry.py add --origin play`) |
| `origin` | enum | `birth` / `detail` / `play` |
| `stamped` | object | the frozen **public and discoverable** fields; validated against the snapshot |
| `refs` | string[] | ids this entity's prose links to (maintained by merge from the wiki-link scan) |
| `dm_only` | object or absent | every secret field of a non-secret entity; stripped from the projection. Its `stamped_fields[]` names the secret fields that are frozen too (an NPC's `secret_tr`, the premise's archetype), so no secret text ever sits in `stamped`; the snapshot at `_snapshots/stamps.json` is `stamped` ∪ those fields |

Play-mutable state is **not** here: `status`, `seen_in_play`, an NPC's current `location`, a settlement's current `ruler`, control, alive/dead/fled, price modifiers and the threat stage live in [overlay.json](overlay.md). The registry keeps the birth value under the type-specific field (`ruler_at_birth`, `location_at_birth`, `control_at_birth`).

## Type-specific fields

| Type | Fields (stamped ones in bold) |
|---|---|
| `god` | **`rank`** (greater / lesser / power), **`domains`** (SRD cleric domains), `alignment`, `symbol`, `church` (a faction or institution id or name, always filled, errata 24.2 #11), `disposition`, `relations[]` (`{to, kind}`) |
| `plane` | `baseline` (SRD plane id), `touched` (bool), `deviation`, `time_rate`, `entry_site` |
| `era` | `order`, `span_tr` |
| `event` | **`day`** (negative = years before day 0 × 360, or an explicit `year`), `year`, `era`, `taught_tr` (public layer), witnesses[] (npc ids); `dm_only.happened_tr` |
| `polity` | `government`, **`ruler_at_birth`** (npc), `capital` (settlement), `law_level` 1-5, `faction` (the `state` faction that carries stances and economy) |
| `region` | **`danger_tier`** 1-5, `biome`, `climate`, `polity`, `identity_tr` (one line), `landmarks[]`, `travel_table` (file) |
| `settlement` | `scale` (village / town / city / metropolis), `population`, `wealth`, `law` 1-5, `polity`, **`ruler_at_birth`**, `region`, `districts[]`, `anchors[]` (place ids), `small_point_budget`, `economy` (`{sells[], needs[], price_modifier}`), `fear_tr`, `problem` (seed id) |
| `district` | `settlement`, `character_tr` |
| `place` | `settlement`, `district` or null, `kind` (inn / temple / shop / guild_hall / market / seat / signature / other), `owner` (npc), `services[]`; permanent once created (errata 24.2 #14) |
| `faction` | **`archetype`** (state / religious / guild / criminal / martial / scholarly / resistance / cult / trade), **`objective`**, `power` 1-5, `intel` 0-3, `hq` (site or place id), `leader` (npc), `heir` (npc), `controller` (`world` / `party`), `board_id` (its `factions.json` id, identical by construction) |
| `npc` | **`faction`**, `role`, `tier` (major / supporting / minor; the one field `detail` may raise), `species`, `gender`, `alignment`, `stat_anchor` (SRD block, `{block, level}`), `cr`, `location_at_birth`, `goal_tracked` (bool), `heir_of` / `heir`, `voice_seed`, `axes` (four personality axes), `relations[]`; `dm_only`: **`secret_tr`**, `surfacing_tr`, `weakness_tr`, `truth_of` (pc id when the NPC carries a PC's truth) |
| `site` | **`danger_tier`**, **`room_count`**, **`act`** (errata 24.2 #9), **`thread`** (faction / npc / seed / beat id), **`key_npcs[]`**, `kind` (dungeon / stronghold / wilderness / urban / planar / social), `role` (minor / standard / major / capstone), `region`, `payoff` (treasure / lore / ally / plot_item / access), `telegraphs` (exactly 3: `{distance: far|near|threshold, text_tr}`), `escape_tr`, `attitude` (kill / capture / enslave / ignore / negotiate / test), `xp_budget`, `min_depth`, `intended_path` (bool), `if_never_visited_tr`, `reoccupation` (faction id); `dm_only`: `clue` (`{secret_clue: 1|2|3}`) when a big-secret clue sits here |
| `item` | `rarity`, `attunement` (bool), `kind` (plot / signature / loot), `location` (site or npc), `srd_base` |
| `creature` | `srd_base`, `cr`, `reskin_tr`, `habitat[]`, `role` (leader / elite / minion / ambient / solo), `stat_block_file` |
| `chapter` | **`act`**, **`level_band`** `[lo, hi]`, `order`, `nodes[]`, `intended_sites[]`, `xp_share`, `content_mix` (`{site, social, exploration}`) |
| `node` | `chapter`, `location` (any place-like id), `stake_tr`, `ways_in[]`, `if_never_arrives_tr`, `sites[]`, `npcs[]` |
| `seed` | `hook_tr`, `complication_tr`, `resolution_tr`, `reward_tr`, `tied_to[]` (≥1 npc/faction), `site` or null |
| `thread` | `pc`, `question_tr`, `antagonist` (npc), `layers` (3 × `{act, secrecy, placed_in}`), `sites[]`, `crossings[]`, `mission` (goals.json id); `dm_only.truth_tr` |
| `socket` | `kind`, `node`, `npc`, `question_tr` (the primer's spoiler-free form), `bound_to` (pc id or null) |
| `pc` | `player`, `sheet` (file), `origin_settlement` (settlement id), `class`, `level`, `thread` |
| `premise` | **`question_tr`**, `tensions[]`, `world_default_tr`, **`signatures[]`**, **`trope_breaks[]`**, `pitch_tr`; `dm_only`: `secret_archetype`, `secret_twist`, `secret_tr`, `villain_answer_tr`, `clues[]` (`{n, act, layer, placed_in, how_tr}`), `dm_pitch_tr` |
| `signature` | **`kind`** (magic / creature / institution), `rule_tr` (as a native knows it), `refs[]` counted by the `signatures` module (≥3); `dm_only.true_rule_tr` |
| `break` | **`row`** (`trope-breaks.yaml` id), `refs[]` counted (≥5) |
| `arc` | `acts`, **`beats[]`**, `chapters[]`, `doom_day`, **`endings`** (`{win_tr, loss_tr, pyrrhic_tr}`); `arc new` creates `arc_2` and archives `arc_1` |
| `beat` | `act`, `chapter`, **`change_kind`** (control / knowledge / status / relationship / loss / access / threat), `state_before_tr`, `state_after_tr`, **`world_pressure`** (`<operation id>.<step id>` in `factions.json`), `delivery_paths[]` (2-3 ids or news ids), `fallbacks` (`{cost_tr, secondary_tr, deferred_tr}`); play status lives in `state.md`'s arc pointer, never here |

Secrecy on a **field** is expressed by placing it in `dm_only`; secrecy on an **entity** by `secrecy: secret`. A `discoverable` entity is in the projection: the projection is what the *DM* may see, and the owner's reading line is drawn by the CLAUDE.md rule (24.6 #1), not by this file.

## Example — a supporting NPC with a secret field (canonical form)

```json
{
  "id": "npc_yesra",
  "type": "npc",
  "name": "Yesra Saltreader",
  "aliases": ["Saltreader Yesra", "Blind Reader"],
  "summary": "Lanternside'ın son tuz okuyucusu; kendi anılarının yarısını kaybetmiş, kaybettiğini bilmiyor.",
  "file": "design/npcs/npc_yesra.md",
  "secrecy": "public",
  "created_phase": "P5",
  "origin": "birth",
  "faction": "faction_court_of_mourners",
  "role": "salt_reader",
  "tier": "supporting",
  "species": "insan",
  "gender": "kadın",
  "alignment": "NG",
  "stat_anchor": {"block": "acolyte", "level": null},
  "cr": 0.25,
  "location_at_birth": "place_salt_house",
  "goal_tracked": false,
  "heir_of": null,
  "heir": null,
  "voice_seed": "cümleyi yarım bırakıp 'neydi...' der",
  "axes": {"trust": "güvenilir, yalanı hatırlayamaz", "ambition": "hiç kalmadı", "loyalty": "Court'a değil, ölülere sadık", "courage": "suya karşı cesur, Court'a karşı korkak"},
  "relations": [
    {"to": "npc_ilme", "kind": "fears", "reason_tr": "Ilme onun okumalarını sayıyor"},
    {"to": "npc_tolvan", "kind": "knows", "reason_tr": "Weary Gull'da her akşam aynı masa"}
  ],
  "stamped": {"faction": "faction_court_of_mourners"},
  "refs": ["faction_court_of_mourners", "npc_ilme", "npc_tolvan", "place_salt_house", "site_sunken_pier"],
  "dm_only": {
    "secret_tr": "Her okuma bir anısını götürdü; boşlukları Court'un 'tüketilenler' defterinde sayılı.",
    "surfacing_tr": "Aynı hikâyeyi iki akşam üst üste farklı anlatır; Insight DC 12 boşluğu görür; defter (site_sunken_pier) adını listeler.",
    "weakness_tr": "Bir anıyı geri almak için her şeyi verir.",
    "clue": {"secret_clue": 1},
    "stamped_fields": ["secret_tr"]
  }
}
```

The same entity in the projection is identical minus the `dm_only` object. A secret entity such as the true BBEG `npc_s01` appears only in the canonical file:

```json
{
  "id": "npc_s01",
  "type": "npc",
  "name": "Nerun",
  "aliases": ["Silent Scribe"],
  "summary": "(gizli varlık — herkese açık dosyalarda görünmez)",
  "file": "design/dm-only/npcs/npc_s01.md",
  "secrecy": "secret",
  "created_phase": "P4",
  "origin": "birth",
  "faction": "faction_court_of_mourners",
  "role": "bbeg",
  "tier": "major",
  "species": "insan",
  "gender": "erkek",
  "alignment": "LE",
  "stat_anchor": {"block": "mage", "level": 9},
  "cr": 6,
  "location_at_birth": "place_mourners_hall",
  "goal_tracked": true,
  "heir": "npc_ilme",
  "voice_seed": "hiç soru sormaz; her cümlesi bir tespit",
  "axes": {"trust": "aldatıcı", "ambition": "sınırsız, sessiz", "loyalty": "yalnızca defterine", "courage": "başkalarının eliyle"},
  "relations": [{"to": "npc_ilme", "kind": "controls", "reason_tr": "Ilme onun yüzü; kendisi sesi"}],
  "stamped": {"faction": "faction_court_of_mourners"},
  "refs": ["faction_court_of_mourners", "npc_ilme", "item_consumed_ledger", "site_blind_lantern"],
  "dm_only": {
    "secret_tr": "Salt Memory'nin ölüleri ikinci kez öldürdüğünü bilir ve defteri bunun için tutar.",
    "surfacing_tr": "Üçüncü ipucu (site_blind_lantern) defterin el yazısını Ilme'nin değil, onun eline bağlar.",
    "weakness_tr": "Kendi adının unutulmasından korkar; adını söyleyen biri karşısında durur.",
    "visibility_pattern": "behind_visible_front",
    "stamped_fields": ["secret_tr"]
  }
}
```

## What `design_check.py refs` verifies against this file

Every `[[id]]` in prose resolves; every entity's `file` exists and its front-matter `entity:` matches the key; ids unique across registry and `name_registry`; no first-name collisions; every role (ruler, leader, heir, socket NPC) has a living holder; counts per type within the scale band unless `_meta.fixture`.
