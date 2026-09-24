---
entity: none
type: cosmology
secrecy: public
phase: P2
stamped: []
covers: [god_velune, god_ormis, god_isken, plane_dipsiz, era_tufan, era_fenerler, era_sessizlik, event_buyuk_tufan, event_divan_kurulusu, event_fener_sondu, event_kayip_gemi]
mirror: design/dm-only/cosmology.md
---

# Cosmology — Tuzlu Fener

## Public

### Pantheon — `pantheon_silent_gods`
Tanrılar cevap vermez. Kıyı halkı yine de her sabah tuz döker, kandil yakar ve adlarını söyler; cevap beklemek değil, hatırlanmak içindir.

#### [[god_velune]] — Velune, "Dalgaların Anası"
- **Rank:** greater · **Domains:** Tempest, Nature · **Alignment:** N · **Symbol:** üç dalga üstünde bir tuz kristali
- **As worshipped:** Sabah tuzu denize dökülür; fırtınada adı söylenmez, çünkü fırtına onun konuşmasıdır. Balıkçı çıkmadan önce tapınağa bir kabuk bırakır.
- **Church / cult:** Velune Tapınağı ([[place_velune_tapinagi]]), rahibi [[npc_olmar]]; ayrı bir hizip değil, Beylik'in kurumu.
- **Disposition to mortals:** kayıtsız; fırtınayla konuşur, tuzla susar.
- **Relations:** [[god_ormis]] ile rekabet (deniz alır, kandil tutar); [[god_isken]] ile sessizlik.

#### [[god_ormis]] — Ormis, "Kandil Tutan"
- **Rank:** greater · **Domains:** Knowledge, Light · **Alignment:** LN · **Symbol:** yanan kandil, altında kapalı defter
- **As worshipped:** Her evde bir kandil; Kandil Gecesi'nde Divan bedava okuma yapar. Ormis'e dua edilmez, ona "okunur".
- **Church / cult:** [[faction_divan]] — Yas Tutanlar Divanı onun adıyla okur ve defter tutar.
- **Disposition to mortals:** sessiz; kandil yanınca orada sayılır.
- **Relations:** [[god_velune]] ile rekabet; [[god_isken]] ile ittifak (biri bitirir, öteki hatırlatır).

#### [[god_isken]] — İsken, "Sessiz Olan"
- **Rank:** lesser · **Domains:** Death · **Alignment:** N · **Symbol:** sönmüş kandil
- **As worshipped:** Sessiz Gün'de kimse konuşmaz; ölülerin adı söylenmez, yalnızca yazılır. İsken'den bir şey istenmez; o gelir, bitirir, gider.
- **Church / cult:** yok; her evde bir sönmüş kandil.
- **Disposition to mortals:** nazik.
- **Relations:** [[god_ormis]] ile ittifak; [[god_velune]] ile sessizlik.

### Planes
- **Baseline:** SRD kozmolojisi, tek değişiklikle: öte dünya düzlemleri kıyı halkı için yoktur. Ölen gitmez, biter ([[break_no_afterlife]]).
- **Touched planes (0-1):** yok. [[plane_dipsiz]] (Su Düzlemi'nin bu dünyadaki adı) vardır ama dokunulmamıştır: kimse oraya gitmez, oradan kimse gelmez.
- **Rule for the primer:** Banishment ve Plane Shift çalışır; gönderilen Dipsiz'e gider ve geri gelirse gittiğini hatırlamaz. Diriltme büyüleri bu dünyada bilinmez; SRD'de olsalar da hiçbir tapınak öğretmez.

### Magic
- **Availability:** düşük · **Source:** arcane (nadir), divine (Ormis ve Velune, sessiz), Tuz Hafızası (yalnızca okuyucular) · **Visibility:** tuz okuması görülür bir törendir; öteki büyüler şüpheyle karşılanır.
- **Constraints and cost:** Tuz Hafızası'nda bir kristal bir okuma; okuyucu "bazen unutur".
- **Taboos:** izinsiz okuma; ölünün tuzunu satmak; kandili söndürmek.
- **Regulator:** [[faction_divan]] — mühür verir, mühürsüz okuyanı yasaklar, defter tutar.
- **Signature phenomenon:** **[[signature_tuz_hafizasi]]** — boğulanın son saati tuzunda kalır; dilde eritilirse bir kez yaşanır.
- **Wild magic:** hayır (`wild_no`).

### History

#### Ages
| Order | Age | Span | What the age is remembered for |
|---|---|---|---|
| 1 | [[era_tufan]] Tufan Çağı | ~1200 yıl önce, süresi bilinmez | Deniz ovayı aldı, tuzla geri verdi |
| 2 | [[era_fenerler]] Fenerler Çağı | yıl 1 - 372 | Fenerler dikildi, gemiler geldi, Divan kuruldu |
| 3 | [[era_sessizlik]] Sessizlik Çağı | yıl 372 - 412 (bugün) | Fener söndü, gemiler azaldı, okumalar arttı |

#### Events — as taught
| Year | Event | Public account | Witnesses still alive |
|---|---|---|---|
| ~ -1200 | [[event_buyuk_tufan]] Büyük Tufan | Velune öfkelendi, ovayı aldı, tuzla geri verdi; o günden beri ölüler tuzda kalır | — |
| 292 | [[event_divan_kurulusu]] Divan'ın Kuruluşu | Okuma vahşi ve tehlikeliydi; Divan onu düzene soktu, aileleri korudu | — |
| 372 | [[event_fener_sondu]] Fener'in Sönüşü | Bekçi boğuldu, fener yağsız kaldı, Beylik yeni bekçi bulamadı | [[npc_sarven]], [[npc_tolvan]], [[npc_ilme]] |
| 409 | [[event_kayip_gemi]] Kandil'in Batışı | Fırtına gemiyi Kırık Dalgakıran'a attı; Beylik'in tuz vergisi ve dört can denize gitti | [[npc_tolvan]], [[npc_draskun]], [[npc_sarven]] |

### Calendar
- **Months (30 days each):** Buzay, Sisay, Tuzay, Kandilay, Sazay, Gelgitay, Dalgay, Kurumay, Yasay, Ormisay, Velunay, İskenay
- **Day names:** Tuzgünü, Sazgünü, Dalgagünü, Kandilgünü, Sisgünü, Sessizgün
- **Seasons and their felt tone, per month:** Buzay: soğuk, gri gök, keskin tuz kokusu · Sisay: sis sabahları, ıslak halat · Tuzay: rüzgâr döner, düzlük parlar · Kandilay: ılık akşamlar, kandil isi · Sazay: sazlık yeşerir, sivrisinek · Gelgitay: büyük gelgitler, çürük yosun · Dalgay: fırtına, tuz serpintisi · Kurumay: sıcak, düzlük çatlar, ölü balık · Yasay: yas ayı, kandil isi ve gül suyu · Ormisay: berrak geceler, deniz fosforu · Velunay: ilk fırtına, ıslak taş · İskenay: sessiz kar, kapalı kapılar
- **Moon:** Kandil, 30 günlük döngü, gün 0'da yeni ay
- **Festivals:** Tuz Dökümü (1 Tuzay, [[god_velune]]) · Kandil Gecesi (30 Kandilay, [[god_ormis]]) · Sessiz Gün (15 İskenay, [[god_isken]])
- **Start date:** 12 Kandilay 412 = campaign day 0 (`calendar.py init --date "12 Kandilay 412" --months "Buzay,Sisay,Tuzay,Kandilay,Sazay,Gelgitay,Dalgay,Kurumay,Yasay,Ormisay,Velunay,İskenay" --day-names "Tuzgünü,Sazgünü,Dalgagünü,Kandilgünü,Sisgünü,Sessizgün"`)

## Discoverable

- Yaşlılar Fener'in sönüşünü başka anlatır: bekçi boğulmadı, "okundu" ve bir daha görülmedi.
- Divan'ın kuruluş yılı defterlerde 292'dir ama Tuz Evi'nin kapı taşında daha eski bir tarih kazınmıştır.
- Kandil'de dört değil beş kişi vardı; beşincinin adı hiçbir listede yok.
