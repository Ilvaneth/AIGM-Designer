---
entity: npc_s01
type: npc
secrecy: secret
phase: P4
tier: major
stamped: [faction, secret_tr]
mirror_of: null
---

# Nerun — Sessiz Kâtip (secret entity; this file has no public counterpart)

## Public

*(nothing — the entity is secret; Fenerli knows only that "the Divan has a scribe who writes and never speaks")*

## Discoverable

- Divan Evi'nin arka odasında biri yazar; kapıdaki hizmetli "kâtip" der, İlme "kâtip yazar, konuşmaz" der. Kimse yüzünü tarif edemez.

## Secret

- **Appearance:** İnsan, yaşı belirsiz (altmış görünür, yüz yirmi yaşındadır: her okuma ona bir yıl verir); ince, tuz beyazı saç, mürekkepli parmaklar, gözleri hep defterde. Hiç soru sormaz.
- **Role / CR / location:** BBEG, Divan'ın gerçek başı · CR 6 (`mage`, seviye 9; büyülerine ek olarak Tuz Hafızası: bir eylemle bir hedeften bir anı okur, WIS DC 14, başarısızlıkta hedef bir dakika kendi adını unutur ve Nerun 1d8 geçici HP alır) · usually at [[place_divan_evi]] (arka oda); gün 75'ten sonra [[site_kor_fener]] kandil odası
- **Faction:** [[faction_divan]] · **Tier:** major · **Alignment:** LE · **Visibility pattern:** `behind_visible_front` — [[npc_ilme]] yüzü
- **Demeanor:** Tespit eder; "sen korkuyorsun", "bu üçüncü sorun". Hiç yükselmez.
- **Speech quirk:** hiç soru sormaz; her cümlesi bir tespit. · **Voice samples:**
  - *"Adını üç kez söyledin. Unutulmaktan korkuyorsun. Ben de korkuyordum; artık korkmuyorum."*
  - *"Onlar zaten gitmişti. Ben yalnızca kalanı topladım. Sen de topluyorsun; buna anı diyorsun."*
- **Schedule:** Gündüz arka oda, gece Tuz Evi'nde tek başına okuma.
- **Attitude toward party:** hostile (görünmez); İlme aracılığıyla court
- **Current goal:** Defteri doldurup Fener'i yakmak (`goals.json` `npc_s01`: okuma 3/12; threatened → Yesra'nın okumasını öne alır; blocked → İlme'yi kurban eder; permanent loss → defteri kendi yakar)

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı; yalan söylemez, susar.
- **Ambitious ↔ Content:** Sınırsız, sessiz.
- **Loyal ↔ Opportunistic:** Yalnızca defterine.
- **Brave ↔ Cowardly:** Başkalarının eliyle; Draskun'la, İlme'yle, kandille.

### Relationships
- **Controls:** [[npc_ilme]] — İlme onun yüzü; kendisi sesi.
- **Commands:** [[npc_draskun]] — tuzu taşıtır; vaat "adın anılacak".
- **Heir:** [[npc_ilme]] — Nerun ölürse mühür ve defter İlme'ye geçer; İlme ne yapacağını bilmez.
- **Truth of:** [[pc_vorin]] — Vorin'in babasını "gönüllü" olarak ilk okuyan odur.

### Known Facts
- day 0 — Yesra'nın altı boşluğu, hangi okumadan geldiği — witnessed (defter)
- day 0 — Kandil'de defterin kopyası ve kurye battı; kopya Batık İskele'de — told by [[npc_draskun]]
- day 0 — Bey'in borcu, Tolvan'ın rehini, Ameli'nin annesi — role (defter, her cenaze)
- day 0 — Parti Fenerli'ye geldi — told by İlme (gün 1'den itibaren)

### Motivation with history
Yedinci kâtip; ilk kâtibin notunu on altısında okudu: "Okuma anıyı tüketir; tüketilen kaybolmaz, birikir." Kırk yıl önce bekçiyi okuttu ve kandilin Fener'de biriktiğini gördü ([[event_fener_sondu]]). O günden beri defteri doldurur: on iki okuma daha ve kandil kıyıdaki her kafaya tek bir adı yazacak kadar dolu olacak. Öte yoksa hatırlanmak tek yaşamdır; Nerun ilk ölümsüz olmak istiyor.

### Weakness
Kendi adının unutulmasından korkar; adını söyleyen biri karşısında durur (bir tur hareket edemez, WIS DC 12 ile kurtulur, günde bir kez). Adını yalnızca İlme, Draskun ve defter bilir.

### What changes if they die
Divan biter ya da dürüstleşir; İlme mührü alır. Fener yanmaz. Kandil odasındaki birikmiş anılar sahiplerine dönmez ama Tuzbağlılar durur. Draskun Divan bağlantısız bir kaçakçı olur.

### Boss checklist (reference party: 2 PC, level 5)
- **Multi-round HP sizing:** mage 40 HP + kandil odasında her tur 1d8 geçici HP (okuma); referans partinin patlaması ~35/tur → üç tur.
- **Resistance by default:** kandil odasında ateşe direnç (kandil onun); büyülere değil.
- **Terrain protection:** kandil odası dar, sarmal merdiven tek sıra; Nerun balkonda, parti aşağıda.
- **Pre-boss attrition:** bekçi (ghast reskin) ve 4 Tuzbağlı 12. ve 13. odalarda.
- **Tanky adds:** bekçi; hiçbir şey düşürmez.
- **Signature weapon + defensive item:** [[item_kandil_muhru]] (nadir, uyum; koruma yüzüğü çatısı) ve defterin aslı (silah değil, hedef).
