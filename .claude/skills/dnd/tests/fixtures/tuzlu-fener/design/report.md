---
entity: none
type: report
secrecy: public
phase: P8
stamped: []
mirror: design/dm-only/report.md
---

# Design report — Tuzlu Fener

## Public

### Dials and dice
| Dial | Value | Rolled? |
|---|---|---|
| scale | short | — |
| tone | dark fantasy | — |
| magic | low | — |
| era | medieval | — |
| danger | gritty | — |
| party size / start level | 2 / 1 (band 1-5) | — |
| content mix | mystery, exploration, politics | d5=5, d4=1, d3=2 |
| wishes | must: deniz ve tuz kokusu, ölüler gerçekten ölsün · must not: kader/kehanet, seçilmiş kişi | — |
- **Seed:** `TF-4c1e9a07` · **Public rolls:** 10 · **Secret rolls:** 3 (labels only)

### Scale counts (target / actual)
| Type | Band (short) | Actual |
|---|---|---|
| regions | 1-2 | 1 |
| settlements | 1 town + 2-3 villages | 1 town + 1 village |
| factions | 3-4 | 3 |
| named NPCs | 14-18 | 9 (major 2 / supporting 4 / minor 3) |
| sites | 6-8 (2 detailed) | 4 (1 detailed) |
| gods | 3-5 | 3 |
| quest seeds | 6-8 | 2 |
| sockets | party × 2 = 4 | 4 |
*(fixture: below band by design, `_meta.fixture: true`)*

### Signatures and trope breaks
- Tuz Hafızası (magic) — 5 entities · Tuzbağlı (creature) — 5 entities · Yas Tutanlar Divanı (institution) — 5 entities
- Öte yok, herkes biliyor — 6 entities

### Faction board (public)
| Faction | Archetype | Power / intel | HQ | First operation |
|---|---|---|---|---|
| Sazlık Beyliği | state | 3 / 1 | Bey Konağı | Kandil'in sandıkları |
| Yas Tutanlar Divanı | guild | 2 / 3 | Divan Evi | Yas Yılı |
| Gelgit Kardeşliği | criminal | 2 / 2 | Gelgit Mağarası | Sandık Yolu |

### Site directory status
| Site | Tier | Rooms | Act | Status |
|---|---|---|---|---|
| Batık İskele | T1 | 6 | 1 | detailed |
| Gelgit Mağarası | T2 | 11 | 1 | skeleton |
| Kör Fener | T2 | 14 | 1 | skeleton |
| Dipsiz Kuyu | T4 | 12 | 1 | skeleton (off-path) |

### PC sockets
- 4 sockets; 2 bound at `integrate` (Selen, Vorin), 2 live on as seeds

### Validation and critique
- **Validator:** 0 errors, 1 warning (scale: fixture below band)
- **Critique loops per phase:** P1 1 · P2 1 · P3 1 · P4 1 (fix, pass) · P5 1 · P6 1 (fix, pass) · P7 1 · P8 0 · P9 1 · **critique_missing:** 0
- **Failed ids:** none
- **Wishes:** deniz ve tuz kokusu ✓ · ölüler gerçekten ölsün ✓ · kader/kehanet yok ✓ · seçilmiş kişi yok ✓

### Cost
- **Tokens out:** 98 400 (input estimated: ~0.6M) · **Wall clock:** 1:30 · **Agents:** 31 · **Sittings:** 1

## Discoverable

*(nothing)*
