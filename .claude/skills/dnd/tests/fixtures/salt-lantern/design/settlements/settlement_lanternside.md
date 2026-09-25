---
entity: settlement_lanternside
type: settlement
secrecy: public
phase: P3
status: detailed
stamped: [scale, polity, ruler_at_birth]
covers: [district_quayside, district_upper_lanternside, place_weary_gull, place_mourners_hall, place_reeves_manor, place_salt_market, place_temple_of_velune, place_salt_house]
mirror: design/dm-only/settlements/settlement_lanternside.md
---

# Lanternside — town

## Public

Kırık bir dalgakıranın ardında, tuz kokusunun her şeye sindiği bir liman. Aşağıda halat ve hamal sesi, yukarıda kapalı kapılar ve hiç sönmeyen kandiller. Atla gelen ilk önce Reeve's Manor'un gri çatısını, sonra rıhtımda kurumaya asılmış balıkları görür.

- **Scale:** town · **Population:** ~2400 · **Wealth:** modest · **Law:** 3, kept by Reeve'in liman muhafızı (on iki kişi)
- **Polity:** [[polity_reedmarch]] · **Ruler:** [[npc_sarven]] (Reeve) · **Region:** [[region_saltmere]]
- **Districts:** [[district_quayside]] Quayside — gündüz hamal, gece Brotherhood; [[district_upper_lanternside]] Upper Lanternside — kapılar kapalı, kandiller yanık
- **Economy:** sells tuz, tuzlu balık; needs kereste, demir; price modifier ×1.0
- **What the settlement fears:** Lantern bir daha yanarsa.
- **Local problem:** [[seed_gulls_debt]] — hancının kayıkları Brotherhood'a rehin.

### Anchor locations
| Place | Kind | Owner | Services | Note |
|---|---|---|---|---|
| [[place_temple_of_velune]] Temple of Velune | temple | [[npc_olmar]] | ayin, ücretli şifa, cenaze | denize bakan alçak tapınak; sabah tuzu buradan dökülür |
| [[place_weary_gull]] Weary Gull | inn | [[npc_tolvan]] | oda, yemek, söylenti, kayık | Quayside'ın tek hanı; iki kayığı rehin |
| [[place_salt_market]] Salt Market | market | — | tuz, balık, halat, yağ | rıhtımda, sabah kurulur |
| [[place_reeves_manor]] Reeve's Manor | seat | [[npc_sarven]] | huzur, hüküm, vergi | Salt Council burada toplanır |
| [[place_mourners_hall]] Mourners' Hall | guild_hall | [[npc_ilme]] | okuma ruhsatı, yas tutma, defter kaydı | kandil hiç sönmez |
| [[place_salt_house]] Salt House | signature | [[npc_yesra]] | tuz okuması (ruhsatla) | tek odalı; yalnızca burada, yalnızca mühürle |

### Small points *(budget 12; filled by `detail`, permanent once named)*
| Place | District | Kind | Owner | Services | Filled |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

### People here
- [[npc_sarven]] — Reeve, [[place_reeves_manor]] (sabah meclis, öğleden sonra kimseyi kabul etmez)
- [[npc_olmar]] — rahip, [[place_temple_of_velune]] (şafakta tuz döker)
- [[npc_ilme]] — Court sözcüsü, [[place_mourners_hall]] (cenaze günleri Salt House'ta)
- [[npc_yesra]] — okuyucu, [[place_salt_house]]; akşamları [[place_weary_gull]]
- [[npc_tolvan]] — hancı, [[place_weary_gull]]
- [[npc_kortan]] — geceleri rıhtımda, gündüz [[site_sunken_pier]]'de

### Rumours on day 0
- Üç yıl önce batan Vesper'in bir sandığı gelgitte kıyıya vurmuş; hamallar kimin aldığını söylemiyor.
- Court bu ay üç ölü için okuma yaptı; ailelerden ikisi istememişti.

## Discoverable

### Three truths
- **Obvious:** Kasabayı Reeve yönetir, Court cenazeleri; ikisi birbirine kibar, hiçbiri Brotherhood'dan söz etmez.
- **Discoverable:** Liman muhafızının yarısı Brotherhood'dan para alır; Reeve'in tuz vergisi üç yıldır eksik ve meclis nedenini sormaz.

### Prices
| Item | Price | Note |
|---|---|---|
| bir gece oda (Weary Gull) | 5 sp | Tolvan partiye "bedava" der |
| bir çuval tuz | 2 gp | vergi dahil |
| kandil (okuma için) | 1 gp | Court mührü ayrıca 5 gp |
| kayık kiralama (gün) | 1 gp | cezirde yarı fiyat |

