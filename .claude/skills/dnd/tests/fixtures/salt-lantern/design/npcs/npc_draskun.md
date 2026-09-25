---
entity: npc_draskun
type: npc
secrecy: public
phase: P5
tier: major
stamped: [faction]
mirror: design/dm-only/npcs/npc_draskun.md
---

# Draskun — Tide Brotherhood'un reisi

## Public

- **Appearance:** Yarı-ork, otuzlarında, uzun kollu ve sessiz; sol dişi kırık, boynunda üç ilmekli düğüm. Konuşurken elindeki halatı düğümler, cevabı düğümde verir.
- **Role / CR / location:** reis · CR 2 (`bandit captain`) · usually at [[site_tide_cave]]; cezirde rıhtımda
- **Faction:** [[faction_tide_brotherhood]] · **Tier:** major · **Alignment:** NE
- **Demeanor:** Az konuşur, sözünü tutar, sebebini söylemez.
- **Speech quirk:** Konuşurken halat düğümler; cevap düğümde gelir (bir ilmek evet, iki hayır, boş ilmek "sorma"). · **Voice samples:**
  - *"Deniz verir. Biz taşırız. Kime, sormazsın."* (boş ilmek)
  - *"Tolvan'ın kayıkları yirmi beşinci gün benim. Ondan önce bir sandık getirirsen, sayılır."*
- **Schedule:** Cezirde mağarada, mette rıhtımda; asla gündüz kasabanın yukarısında.
- **What they can offer the party / want from the party:** kayık, gece geçişi, enkaz malı, bilgi (kim ne taşıdı) / sandık taşımalarını, soru sormamalarını ister.
- **Attitude toward party:** neutral
- **Current goal:** Crate Run (op_tide_1): sandıklar mağaraya, tuz Mourners' Hall'a.

### Personality
- **Trustworthy ↔ Deceptive:** Sözünü tutar, sebebini söylemez.
- **Ambitious ↔ Content:** Kıyının tek taşıyıcısı olmak.
- **Loyal ↔ Opportunistic:** Bir kişiye sadık, korkudan; kimse bilmez.
- **Brave ↔ Cowardly:** Cesur; cezirde daha cesur.

### Relationships
- **Heir:** [[npc_kortan]] — ikinci adamı; soru sormaya başladı.
- **Controls:** [[npc_tolvan]] — kayıklar rehin.
- **Fears (unnamed):** tuzu götürdüğü kişi.

### Known Facts — what they actually know and how
- day 0 — Vesper'i kayalığa çeken fener Reeve'in adamlarınındı — witnessed ([[event_vesper_wreck]]; manifestoyu bu yüzden aldı)
- day 0 — Sandıkların birinde Court'un defteri var — told by kâtip (sorulmadan)
- day 0 — Kortan tuzun nereye gittiğini soruyor — witnessed (düğümle sordu)
- day 0 — Parti hana yerleşti ve Tolvan onlara bir iş verecek — told by rıhtım hamalı (gün 1)

## Discoverable

- **Motivation with history:** Lantern söndükten sonra gemiler kesilince kıyı taşıyıcısız kaldı; Draskun yayladan indi ve boşluğu doldurdu. Üç yıl önce enkazı ilk o buldu ve o gece biri ona "adın anılacak" dedi; o günden beri tuz taşır.
- **Weakness derived from personality:** Kortan'a güvenmek zorundadır ve bunu bilir.
- **What changes if they die:** [[npc_kortan]] reis olur ve Court bağlantısı kopar; tuz Court'a gitmez, kandil eksik kalır (doom bir kez ertelenir); [[thread_selen]]'in antagonisti Kortan'a geçer.
- **Goal tracker** (`goals.json` `npc_draskun`): tuz çuvalı 4/10; threatened → Tolvan'ın kayıklarını alır; blocked → tuzu Court'a kendi taşır; permanent loss → mağarayı cezirde bırakır, Lantern'e sığınır.
