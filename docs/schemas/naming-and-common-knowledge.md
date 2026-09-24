# `naming.json` and `common-knowledge.json`

Two small stores the designer emits beside the seven main ones. Plan items 4.6, 11.5, 24.1 #18.

## `design/naming.json` — the campaign's naming languages

Written by P1 from `naming.yaml`'s sound families (rolled, then mutated); read by every later phase that names something, and by `name_registry check`. Two modes per language (24.1 #18): `phonetic` for persons and gods, `compound` from a root lexicon for places and institutions. `tr_suffix_friendly` languages end names in a vowel or a single consonant so Turkish case endings attach cleanly (Sarven'in, Fenerli'ye).

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "tuzlu-fener",
    "fixture": true,
    "written_by": "registry.py merge --phase P1",
    "written_at": "2026-09-24T18:10:00Z"
  },
  "languages": {
    "sazca": {
      "label_tr": "Sazca — kıyı halkının dili",
      "family": "liquid_vowel",
      "onsets": ["v", "m", "r", "l", "s", "n", "y", ""],
      "nuclei": ["a", "e", "i", "o", "u"],
      "codas": ["n", "r", "l", "s", "m", ""],
      "length": [2, 3],
      "forbidden_clusters": ["rr", "ll", "sr"],
      "tr_suffix_friendly": true,
      "modes": {"person": "phonetic", "god": "phonetic", "place": "compound", "institution": "compound"},
      "roots": {"fener": "ışık/uyarı", "tuz": "hafıza/koruma", "saz": "sınır/gizlenme", "gelgit": "borç/dönüş", "kandil": "yas/anma"},
      "samples": ["Velune", "Ormis", "Sarven", "İlme", "Yesra", "Tolvan", "Nerun"]
    },
    "kayaca": {
      "label_tr": "Kayaca — yayla ve kaya halkının dili",
      "family": "harsh_consonantal",
      "onsets": ["d", "t", "k", "v", "g", "dr", "kr"],
      "nuclei": ["a", "o", "u", "ı"],
      "codas": ["k", "n", "sk", "rt", "r"],
      "length": [2, 2],
      "forbidden_clusters": ["kk", "tt"],
      "tr_suffix_friendly": true,
      "modes": {"person": "phonetic", "god": "phonetic", "place": "compound", "institution": "compound"},
      "roots": {"kaya": "dayanma", "kor": "yemin", "dövmek": "biçim verme"},
      "samples": ["Draskun", "Vorin", "Tegrik", "Kortan"]
    }
  },
  "assignments": {
    "polity_sazlik": "sazca",
    "region_tuz_ovasi": "sazca",
    "faction_divan": "sazca",
    "faction_kacakcilar": "kayaca",
    "pc_vorin": "kayaca"
  },
  "banned": ["kriv", "ilvaneth", "ashen", "corr", "ondrel"]
}
```

`banned[]` holds the worn-vocabulary soft-ban and every stem `name_registry` already carries; `samples[]` are the names this campaign actually produced from the language, appended at phase approval.

## `common-knowledge.json` — what a native already knows

Written by P8 at the campaign root beside `channels.json`; read by `channels.py check` before it flags a fact as leaked, and by `render_player.py` for the primer. Every fact is public-tier by definition; a fact with an `origin` list is known to natives of those polities or settlements only (item 11.4).

```json
{
  "_meta": {
    "schema_version": 1,
    "campaign": "tuzlu-fener",
    "fixture": true,
    "written_by": "design_seed.py --phase P8",
    "written_at": "2026-09-24T19:56:00Z"
  },
  "facts": [
    {"id": "ck_001", "keywords": ["divan", "okuma", "tuz", "ölü", "anı"], "text_tr": "Yas Tutanlar Divanı ölülerin son anısını tuzdan okur; okuma için aile izni ve bir kandil gerekir.", "origin": "all", "refs": ["faction_divan"]},
    {"id": "ck_002", "keywords": ["öte", "ölüm", "ruh", "cennet"], "text_tr": "Ölümden sonra hiçbir şey yoktur; bunu herkes bilir, tapınaklar da inkâr etmez.", "origin": "all", "refs": ["god_isken"]},
    {"id": "ck_003", "keywords": ["fener", "kör", "burun"], "text_tr": "Kör Fener kırk yıldır yanmıyor; oraya giden balıkçı dönmedi.", "origin": ["polity_sazlik"], "refs": ["site_kor_fener", "event_fener_sondu"]},
    {"id": "ck_004", "keywords": ["bey", "sarven", "fenerli", "yönetim"], "text_tr": "Fenerli'yi Bey Sarven yönetir; Beylik vergisini tuzdan alır.", "origin": ["polity_sazlik"], "refs": ["npc_sarven", "polity_sazlik"]},
    {"id": "ck_005", "keywords": ["kamışlı", "tuz düzlüğü", "kuyu"], "text_tr": "Kamışlı'nın doğusundaki tuz düzlüğüne kimse girmez; orada bir kuyu olduğu söylenir.", "origin": ["settlement_kamisli", "settlement_fenerli"], "refs": ["site_dipsiz_kuyu"]}
  ]
}
```

`keywords[]` are lower-case stems `channels.py check` matches against a claim; `origin` is `"all"` or a list of polity / settlement ids; `refs[]` resolve against the registry like every other reference.
