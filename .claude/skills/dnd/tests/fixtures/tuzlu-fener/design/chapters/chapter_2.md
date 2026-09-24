---
entity: chapter_2
type: chapter
secrecy: public
phase: P7
stamped: [act, level_band]
covers: [node_c2_gelgit, node_c2_fener, node_c2_kamisli]
mirror: design/dm-only/chapters/chapter_2.md
---

# Chapter 2 — Gelgit ve Fener (Act 1, levels 3-5)

## Public

- **Drive:** Parti defter parçasının ne olduğunu biliyor; tuzun nereye gittiğini ve Fener'in kime yanacağını öğrenmek zorunda.
- **Locations:** [[region_tuz_ovasi]], [[settlement_kamisli]], kayalık kıyı
- **Intended-path sites:** [[site_gelgit_magarasi]] (T2), [[site_kor_fener]] (T2) · **Off-path sites in reach:** [[site_dipsiz_kuyu]] (T4)
- **Key NPCs:** [[npc_draskun]], [[npc_ameli]], [[npc_ilme]], [[npc_yesra]]
- **XP share:** 3300 of the band's budget (Gelgit 1100 + Fener 2200)
- **Content mix vs the dial:** site 2 / social 1 / exploration 1

### Nodes
#### [[node_c2_gelgit]] — Gelgit Mağarası
- **What is here:** Kardeşlik'in deposu; tuzun nereye gittiği ve manifestonun kimde olduğu.
- **What is at stake:** Tuz Divan'a ulaşırsa kandil tamamlanır.
- **Ways in:** Kortan'ın pazarlığı; cezirdeki kayık izi; Sarven'in manifestosu
- **Sites / NPCs:** [[site_gelgit_magarasi]], [[npc_draskun]]
- **If the party never arrives:** Gün 40'ta tuz Divan'a gider (op_kardeslik_1.step_3).

#### [[node_c2_fener]] — Kör Fener
- **What is here:** Sönük fener, biriken kandil, bekçi; kimin adına yanacağı.
- **What is at stake:** Doksan altıncı günde Fener yanar; kime yanacağı burada belli olur.
- **Ways in:** mağaradan tünel; burun patikası; gün 75'te kandil kervanı
- **Sites / NPCs:** [[site_kor_fener]], [[npc_ilme]]
- **If the party never arrives:** Gün 96'da Fener kâtibe yanar (op_divan_1.step_4 ve doom).

#### [[node_c2_kamisli]] — Kamışlı'nın sessizliği
- **What is here:** Kapıyı çalanlar, okunmayan ölüler, düzlüğe bakan köy.
- **What is at stake:** Köy okumayı reddederse Tuzbağlılar gelir; kabul ederse Divan gelir.
- **Ways in:** `news_0003`; Ameli'nin Fenerli'ye gelişi; [[socket_tuz_okuma]]
- **Sites / NPCs:** [[settlement_kamisli]], [[npc_ameli]], [[site_dipsiz_kuyu]]
- **If the party never arrives:** Gün 20'de Ameli'nin annesi okunur (op_divan_1.step_2); gün 96'da kuyu yürür.

### Beats this chapter can land
- [[beat_1b]] — [[node_c2_gelgit]] (tuz), [[node_c2_kamisli]] (Ameli'nin annesi) ya da Yesra'nın okuması üzerinden
- [[beat_1c]] — [[node_c2_fener]] üzerinden

### A / B scenario for this act
- **A — parti tuzu durdurur (mağara):** Divan kandili eksik bulur, Yesra'nın okumasını öne alır (gün 45 → 30), kervan yine çıkar ama Fener yarım yanar.
- **B — parti Kamışlı'yı seçer (köy):** Divan köyü deftere alır, Kardeşlik tuzu teslim eder, Fener tam yanar; parti Fener'e kervanla birlikte gider.

## Discoverable

- Kandil kervanı gün 75'te Divan Evi'nden çıkar; kasabadan görünür, iki hafta önceden hazırlığı fark edilir (İlme "Yesra dinlenecek" der).
- Tuz Anası'nın adı Kamışlı'da bir ninnide geçer; Ameli söyler.
