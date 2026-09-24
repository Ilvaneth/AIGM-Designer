---
entity: chapter_1
type: chapter
secrecy: public
phase: P7
stamped: [act, level_band]
covers: [node_c1_marti, node_c1_iskele, node_c1_divan]
mirror: design/dm-only/chapters/chapter_1.md
---

# Chapter 1 — Fenerli'ye Varış (Act 1, levels 1-3)

## Public

- **Drive:** Bir yer, bir iş, bir sebep: parti Fenerli'ye gelir, hana yerleşir ve kasabanın sorusunu duyar.
- **Locations:** [[settlement_fenerli]], [[region_tuz_ovasi]]
- **Intended-path sites:** [[site_batik_iskele]] (T1) · **Off-path sites in reach:** [[site_gelgit_magarasi]] (T2, cezirde), [[site_dipsiz_kuyu]] (T4, over-tier, Kamışlı'dan telegraflı)
- **Key NPCs:** [[npc_tolvan]] (ilk masa), [[npc_yesra]] (aynı masa), [[npc_ilme]] (kasabanın öteki yüzü), [[npc_kortan]] (iskele), [[npc_sarven]] (ödül)
- **XP share:** 900 of the band's budget (Batık İskele 450 + sosyal/keşif 450)
- **Content mix vs the dial (mystery / exploration / politics):** site 1 / social 2 / exploration 0 — gizem ağırlıklı, keşif 2. bölümde

### Nodes
#### [[node_c1_marti]] — Yorgun Martı ve borç
- **What is here:** Han, hancı, rehin kayıklar. Tolvan odayı bedava verir ve "küçük bir iş" ister.
- **What is at stake:** Tolvan kayıkları kaybederse han biter ve Kardeşlik limanı tutar.
- **Ways in:** kalacak yer aramak; `news_0001` söylentisi; [[socket_borc]]
- **Sites / NPCs:** [[npc_tolvan]], [[npc_yesra]]
- **If the party never arrives:** Gün 25'te Kardeşlik kayıkları alır (op_kardeslik_1.step_2).

#### [[node_c1_iskele]] — Batık İskele
- **What is here:** Çökük iskelenin altında sandıklar ve Kardeşlik'in bekçisi.
- **What is at stake:** Defter parçası kimin eline geçerse ilk sorunun cevabı ondadır.
- **Ways in:** Tolvan'ın borcu; gece yanan fener (telegraf); Bey'in sandık ilanı
- **Sites / NPCs:** [[site_batik_iskele]], [[npc_kortan]]
- **If the party never arrives:** Gün 10'da sandıklar mağaraya taşınır (op_kardeslik_1.step_1).

#### [[node_c1_divan]] — Divan'ın okumaları
- **What is here:** Divan Evi, Tuz Evi, üç izinsiz okuma; İlme'nin merhameti ve Yesra'nın boşlukları.
- **What is at stake:** Okuma bir gelenek mi bir tüketim mi; Yesra'nın bir sonraki okuması kime mal olur.
- **Ways in:** `news_0002`; Yesra'nın masası; [[socket_divan_egitimi]]
- **Sites / NPCs:** [[place_divan_evi]], [[place_tuz_evi]], [[npc_ilme]], [[npc_yesra]]
- **If the party never arrives:** Gün 20'de Kamışlı'da bir okuma daha (op_divan_1.step_2).

### Beats this chapter can land
- [[beat_1a]] — [[node_c1_iskele]] ya da [[node_c1_marti]] üzerinden

### A / B scenario for this act
- **A — parti Bey'e yanaşır (sandıkları götürür):** Beylik partiyi kollar, Kardeşlik kayıkları erken alır, Divan partiyi "okunacak" listeye almaz.
- **B — parti Kardeşlik'le anlaşır (sandık taşır):** Bey partiyi kaçakçı sayar, Divan tuzun geldiğini görür ve partiye kandil gönderir.

## Discoverable

- Kasabada bir hafta geçiren Yesra'nın aynı hikâyeyi farklı anlattığını fark eder; Tolvan bunu ilk gece ima eder.
- İlme partiyi gün 5'ten sonra izletir; handaki müdavim hamal Divan'ın kulağıdır (sahne rengi, kayıtlı NPC değil).
