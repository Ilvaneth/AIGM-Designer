---
entity: settlement_fenerli
type: settlement
secrecy: public
phase: P3
status: detailed
stamped: [scale, polity, ruler_at_birth]
covers: [district_iskele, district_yukari, place_yorgun_marti, place_divan_evi, place_bey_konagi, place_tuz_pazari, place_velune_tapinagi, place_tuz_evi]
mirror: design/dm-only/settlements/settlement_fenerli.md
---

# Fenerli — town

## Public

Kırık bir dalgakıranın ardında, tuz kokusunun her şeye sindiği bir liman. Aşağıda halat ve hamal sesi, yukarıda kapalı kapılar ve hiç sönmeyen kandiller. Atla gelen ilk önce Bey Konağı'nın gri çatısını, sonra rıhtımda kurumaya asılmış balıkları görür.

- **Scale:** town · **Population:** ~2400 · **Wealth:** modest · **Law:** 3, kept by Bey'in liman muhafızı (on iki kişi)
- **Polity:** [[polity_sazlik]] · **Ruler:** [[npc_sarven]] (Bey) · **Region:** [[region_tuz_ovasi]]
- **Districts:** [[district_iskele]] İskele — gündüz hamal, gece Kardeşlik; [[district_yukari]] Yukarı Fenerli — kapılar kapalı, kandiller yanık
- **Economy:** sells tuz, tuzlu balık; needs kereste, demir; price modifier ×1.0
- **What the settlement fears:** Fener bir daha yanarsa.
- **Local problem:** [[seed_martinin_borcu]] — hancının kayıkları Kardeşlik'e rehin.

### Anchor locations
| Place | Kind | Owner | Services | Note |
|---|---|---|---|---|
| [[place_velune_tapinagi]] Velune Tapınağı | temple | [[npc_olmar]] | ayin, ücretli şifa, cenaze | denize bakan alçak tapınak; sabah tuzu buradan dökülür |
| [[place_yorgun_marti]] Yorgun Martı | inn | [[npc_tolvan]] | oda, yemek, söylenti, kayık | İskele'nin tek hanı; iki kayığı rehin |
| [[place_tuz_pazari]] Tuz Pazarı | market | — | tuz, balık, halat, yağ | rıhtımda, sabah kurulur |
| [[place_bey_konagi]] Bey Konağı | seat | [[npc_sarven]] | huzur, hüküm, vergi | tuz meclisi burada toplanır |
| [[place_divan_evi]] Divan Evi | guild_hall | [[npc_ilme]] | okuma ruhsatı, yas tutma, defter kaydı | kandil hiç sönmez |
| [[place_tuz_evi]] Tuz Evi | signature | [[npc_yesra]] | tuz okuması (ruhsatla) | tek odalı; yalnızca burada, yalnızca mühürle |

### Small points *(budget 12; filled by `detail`, permanent once named)*
| Place | District | Kind | Owner | Services | Filled |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

### People here
- [[npc_sarven]] — Bey, [[place_bey_konagi]] (sabah meclis, öğleden sonra kimseyi kabul etmez)
- [[npc_olmar]] — rahip, [[place_velune_tapinagi]] (şafakta tuz döker)
- [[npc_ilme]] — Divan sözcüsü, [[place_divan_evi]] (cenaze günleri Tuz Evi'nde)
- [[npc_yesra]] — okuyucu, [[place_tuz_evi]]; akşamları [[place_yorgun_marti]]
- [[npc_tolvan]] — hancı, [[place_yorgun_marti]]
- [[npc_kortan]] — geceleri rıhtımda, gündüz [[site_batik_iskele]]'de

### Rumours on day 0
- Üç yıl önce batan Kandil'in bir sandığı gelgitte kıyıya vurmuş; hamallar kimin aldığını söylemiyor.
- Divan bu ay üç ölü için okuma yaptı; ailelerden ikisi istememişti.

## Discoverable

### Three truths
- **Obvious:** Kasabayı Bey yönetir, Divan cenazeleri; ikisi birbirine kibar, hiçbiri Kardeşlik'ten söz etmez.
- **Discoverable:** Liman muhafızının yarısı Kardeşlik'ten para alır; Bey'in tuz vergisi üç yıldır eksik ve meclis nedenini sormaz.

### Prices
| Item | Price | Note |
|---|---|---|
| bir gece oda (Yorgun Martı) | 5 sp | Tolvan partiye "bedava" der |
| bir çuval tuz | 2 gp | vergi dahil |
| kandil (okuma için) | 1 gp | Divan mührü ayrıca 5 gp |
| kayık kiralama (gün) | 1 gp | cezirde yarı fiyat |

