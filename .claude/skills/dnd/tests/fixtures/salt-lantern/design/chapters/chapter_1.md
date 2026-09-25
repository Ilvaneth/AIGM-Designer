---
entity: chapter_1
type: chapter
secrecy: public
phase: P7
stamped: [act, level_band]
covers: [node_c1_gull, node_c1_pier, node_c1_court]
mirror: design/dm-only/chapters/chapter_1.md
---

# Chapter 1 — Arrival at Lanternside (Act 1, levels 1-3)

## Public

- **Drive:** Bir yer, bir iş, bir sebep: parti Lanternside'a gelir, hana yerleşir ve kasabanın sorusunu duyar.
- **Locations:** [[settlement_lanternside]], [[region_saltmere]]
- **Intended-path sites:** [[site_sunken_pier]] (T1) · **Off-path sites in reach:** [[site_tide_cave]] (T2, cezirde), [[site_bottomless_well]] (T4, over-tier, Reedham'dan telegraflı)
- **Key NPCs:** [[npc_tolvan]] (ilk masa), [[npc_yesra]] (aynı masa), [[npc_ilme]] (kasabanın öteki yüzü), [[npc_kortan]] (iskele), [[npc_sarven]] (ödül)
- **XP share:** 900 of the band's budget (Sunken Pier 450 + sosyal/keşif 450)
- **Content mix vs the dial (mystery / exploration / politics):** site 1 / social 2 / exploration 0 — gizem ağırlıklı, keşif 2. bölümde

### Nodes
#### [[node_c1_gull]] — The Weary Gull and the debt
- **What is here:** Han, hancı, rehin kayıklar. Tolvan odayı bedava verir ve "küçük bir iş" ister.
- **What is at stake:** Tolvan kayıkları kaybederse han biter ve Brotherhood limanı tutar.
- **Ways in:** kalacak yer aramak; `news_0001` söylentisi; [[socket_debt]]
- **Sites / NPCs:** [[npc_tolvan]], [[npc_yesra]]
- **If the party never arrives:** Gün 25'te Brotherhood kayıkları alır (op_tide_1.step_2).

#### [[node_c1_pier]] — Sunken Pier
- **What is here:** Çökük iskelenin altında sandıklar ve Brotherhood'un bekçisi.
- **What is at stake:** Defter parçası kimin eline geçerse ilk sorunun cevabı ondadır.
- **Ways in:** Tolvan'ın borcu; gece yanan fener (telegraf); Reeve'in sandık ilanı
- **Sites / NPCs:** [[site_sunken_pier]], [[npc_kortan]]
- **If the party never arrives:** Gün 10'da sandıklar mağaraya taşınır (op_tide_1.step_1).

#### [[node_c1_court]] — The Court's readings
- **What is here:** Mourners' Hall, Salt House, üç izinsiz okuma; Ilme'nin merhameti ve Yesra'nın boşlukları.
- **What is at stake:** Okuma bir gelenek mi bir tüketim mi; Yesra'nın bir sonraki okuması kime mal olur.
- **Ways in:** `news_0002`; Yesra'nın masası; [[socket_court_trained]]
- **Sites / NPCs:** [[place_mourners_hall]], [[place_salt_house]], [[npc_ilme]], [[npc_yesra]]
- **If the party never arrives:** Gün 20'de Reedham'da bir okuma daha (op_court_1.step_2).

### Beats this chapter can land
- [[beat_1a]] — [[node_c1_pier]] ya da [[node_c1_gull]] üzerinden

### A / B scenario for this act
- **A — parti Reeve'e yanaşır (sandıkları götürür):** Reedmarch partiyi kollar, Brotherhood kayıkları erken alır, Court partiyi "okunacak" listeye almaz.
- **B — parti Brotherhood'la anlaşır (sandık taşır):** Reeve partiyi kaçakçı sayar, Court tuzun geldiğini görür ve partiye kandil gönderir.

## Discoverable

- Kasabada bir hafta geçiren Yesra'nın aynı hikâyeyi farklı anlattığını fark eder; Tolvan bunu ilk gece ima eder.
- Ilme partiyi gün 5'ten sonra izletir; handaki müdavim hamal Court'un kulağıdır (sahne rengi, kayıtlı NPC değil).
