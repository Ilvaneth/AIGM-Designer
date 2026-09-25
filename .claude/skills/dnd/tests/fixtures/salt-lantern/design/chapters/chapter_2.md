---
entity: chapter_2
type: chapter
secrecy: public
phase: P7
stamped: [act, level_band]
covers: [node_c2_tide_cave, node_c2_lantern, node_c2_reedham]
mirror: design/dm-only/chapters/chapter_2.md
---

# Chapter 2 — Tide and Lantern (Act 1, levels 3-5)

## Public

- **Drive:** Parti defter parçasının ne olduğunu biliyor; tuzun nereye gittiğini ve Lantern'in kime yanacağını öğrenmek zorunda.
- **Locations:** [[region_saltmere]], [[settlement_reedham]], kayalık kıyı
- **Intended-path sites:** [[site_tide_cave]] (T2), [[site_blind_lantern]] (T2) · **Off-path sites in reach:** [[site_bottomless_well]] (T4)
- **Key NPCs:** [[npc_draskun]], [[npc_ameli]], [[npc_ilme]], [[npc_yesra]]
- **XP share:** 3300 of the band's budget (Tide Cave 1100 + Blind Lantern 2200)
- **Content mix vs the dial:** site 2 / social 1 / exploration 1

### Nodes
#### [[node_c2_tide_cave]] — Tide Cave
- **What is here:** Brotherhood'un deposu; tuzun nereye gittiği ve manifestonun kimde olduğu.
- **What is at stake:** Tuz Court'a ulaşırsa kandil tamamlanır.
- **Ways in:** Kortan'ın pazarlığı; cezirdeki kayık izi; Sarven'in manifestosu
- **Sites / NPCs:** [[site_tide_cave]], [[npc_draskun]]
- **If the party never arrives:** Gün 40'ta tuz Court'a gider (op_tide_1.step_3).

#### [[node_c2_lantern]] — Blind Lantern
- **What is here:** Sönük fener, biriken kandil, bekçi; kimin adına yanacağı.
- **What is at stake:** Doksan altıncı günde Lantern yanar; kime yanacağı burada belli olur.
- **Ways in:** mağaradan tünel; burun patikası; gün 75'te kandil kervanı
- **Sites / NPCs:** [[site_blind_lantern]], [[npc_ilme]]
- **If the party never arrives:** Gün 96'da Lantern kâtibe yanar (op_court_1.step_4 ve doom).

#### [[node_c2_reedham]] — The silence of Reedham
- **What is here:** Kapıyı çalanlar, okunmayan ölüler, düzlüğe bakan köy.
- **What is at stake:** Köy okumayı reddederse Saltbound'lar gelir; kabul ederse Court gelir.
- **Ways in:** `news_0003`; Ameli'nin Lanternside'a gelişi; [[socket_witnessed_reading]]
- **Sites / NPCs:** [[settlement_reedham]], [[npc_ameli]], [[site_bottomless_well]]
- **If the party never arrives:** Gün 20'de Ameli'nin annesi okunur (op_court_1.step_2); gün 96'da kuyu yürür.

### Beats this chapter can land
- [[beat_1b]] — [[node_c2_tide_cave]] (tuz), [[node_c2_reedham]] (Ameli'nin annesi) ya da Yesra'nın okuması üzerinden
- [[beat_1c]] — [[node_c2_lantern]] üzerinden

### A / B scenario for this act
- **A — parti tuzu durdurur (mağara):** Court kandili eksik bulur, Yesra'nın okumasını öne alır (gün 45 → 30), kervan yine çıkar ama Lantern yarım yanar.
- **B — parti Reedham'ı seçer (köy):** Court köyü deftere alır, Brotherhood tuzu teslim eder, Lantern tam yanar; parti Lantern'e kervanla birlikte gider.

## Discoverable

- Kandil kervanı gün 75'te Mourners' Hall'dan çıkar; kasabadan görünür, iki hafta önceden hazırlığı fark edilir (Ilme "Yesra dinlenecek" der).
- Salt Mother'in adı Reedham'da bir ninnide geçer; Ameli söyler.
