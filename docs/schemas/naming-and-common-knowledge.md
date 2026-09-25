# `naming.json` and `common-knowledge.json`

Two small stores the designer emits beside the seven main ones. Plan items 4.6, 11.5, 24.1 #18.

## `design/naming.json` — the campaign's naming languages

Written by P1 from `naming.yaml`'s sound families (rolled, then mutated); read by every later phase that names something, and by `name_registry check`. Two modes per language (24.1 #18): `phonetic` for persons and gods, `compound` from a root lexicon for places and institutions. `tr_suffix_friendly` languages end names in a vowel or a single consonant so Turkish case endings attach cleanly (Sarven'in, Lanternside'a).

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "written_by": "registry.py merge --phase P1",
    "written_at": "2026-09-24T18:10:00Z"
  },
  "languages": {
    "marshtongue": {
      "label_tr": "Marshtongue — kıyı halkının dili",
      "family": "liquid_vowel",
      "onsets": ["v", "m", "r", "l", "s", "n", "y", ""],
      "nuclei": ["a", "e", "i", "o", "u"],
      "codas": ["n", "r", "l", "s", "m", ""],
      "length": [2, 3],
      "forbidden_clusters": ["rr", "ll", "sr"],
      "tr_suffix_friendly": true,
      "modes": {"person": "phonetic", "god": "phonetic", "place": "compound", "institution": "compound"},
      "roots": {"lantern": "ışık/uyarı", "salt": "hafıza/koruma", "reed": "sınır/gizlenme", "tide": "borç/dönüş", "lamp": "yas/anma", "mere": "sığ su", "side": "kıyı yerleşimi", "ham": "köy"},
      "samples": ["Velune", "Ormis", "Sarven", "Ilme", "Yesra", "Tolvan", "Olmar"]
    },
    "cragspeak": {
      "label_tr": "Cragspeak — yayla ve kaya halkının dili",
      "family": "harsh_consonantal",
      "onsets": ["d", "t", "k", "v", "g", "dr", "kr"],
      "nuclei": ["a", "o", "u", "ı"],
      "codas": ["k", "n", "sk", "rt", "r"],
      "length": [2, 2],
      "forbidden_clusters": ["kk", "tt"],
      "tr_suffix_friendly": true,
      "modes": {"person": "phonetic", "god": "phonetic", "place": "compound", "institution": "compound"},
      "roots": {"crag": "dayanma", "oath": "yemin", "forge": "biçim verme", "march": "sınır toprağı"},
      "samples": ["Draskun", "Vorin", "Tegrik", "Kortan"]
    }
  },
  "assignments": {
    "polity_reedmarch": "marshtongue",
    "region_saltmere": "marshtongue",
    "faction_court_of_mourners": "marshtongue",
    "faction_tide_brotherhood": "cragspeak",
    "pc_vorin": "cragspeak"
  },
  "banned": ["Kriv Shestendeliath", "Ilvaneth Duskmere", "Rendric Corr", "Thessaly Ondrel"]
}
```

**The world speaks English, the narration is Turkish** (errata 24.2 #17): every language produces English-language fantasy names — `phonetic` mode for persons and gods, `compound` mode from the English `roots` lexicon for places and institutions (Lanternside, Saltmere, Reedham) — and `tr_suffix_friendly` means the name takes a Turkish suffix cleanly after an apostrophe (Lanternside'a, Saltmere'de). `banned[]` holds exact names already used in this root plus a profanity/brand filter, never word stems (errata #18: crown, hollow, ember may recur). `samples[]` are the names this campaign actually produced from the language, appended at phase approval. A **secret entity's name is never appended**: `naming.json` sits outside `dm-only/`, and the sample list is one of the secondary leak channels risk 24.1 #11 lists.

## `common-knowledge.json` — what a native already knows

Written by P8 at the campaign root beside `channels.json`; read by `channels.py check` before it flags a fact as leaked, and by `render_player.py` for the primer. Every fact is public-tier by definition; a fact with an `origin` list is known to natives of those polities or settlements only (item 11.4).

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "salt-lantern",
    "fixture": true,
    "written_by": "design_seed.py --phase P8",
    "written_at": "2026-09-24T19:56:00Z"
  },
  "facts": [
    {"id": "ck_001", "keywords": ["divan", "okuma", "tuz", "ölü", "anı"], "text_tr": "Court of Mourners ölülerin son anısını tuzdan okur; okuma için aile izni ve bir kandil gerekir.", "origin": "all", "refs": ["faction_court_of_mourners"]},
    {"id": "ck_002", "keywords": ["öte", "ölüm", "ruh", "cennet"], "text_tr": "Ölümden sonra hiçbir şey yoktur; bunu herkes bilir, tapınaklar da inkâr etmez.", "origin": "all", "refs": ["god_isken"]},
    {"id": "ck_003", "keywords": ["fener", "kör", "burun"], "text_tr": "Blind Lantern kırk yıldır yanmıyor; oraya giden balıkçı dönmedi.", "origin": ["polity_reedmarch"], "refs": ["site_blind_lantern", "event_lantern_dimmed"]},
    {"id": "ck_004", "keywords": ["reeve", "sarven", "fenerli", "yönetim"], "text_tr": "Lanternside'ı Reeve Sarven yönetir; Reedmarch vergisini tuzdan alır.", "origin": ["polity_reedmarch"], "refs": ["npc_sarven", "polity_reedmarch"]},
    {"id": "ck_005", "keywords": ["kamışlı", "tuz düzlüğü", "kuyu"], "text_tr": "Reedham'ın doğusundaki tuz düzlüğüne kimse girmez; orada bir kuyu olduğu söylenir.", "origin": ["settlement_reedham", "settlement_lanternside"], "refs": ["site_bottomless_well"]}
  ]
}
```

`keywords[]` are lower-case stems `channels.py check` matches against a claim; `origin` is `"all"` or a list of polity / settlement ids; `refs[]` resolve against the registry like every other reference.
