---
entity: faction_divan
type: faction
secrecy: public
phase: P4
stamped: [archetype, objective]
mirror: design/dm-only/factions/faction_divan.md
---

# Yas Tutanlar Divanı

## Public

### Phase 1 — Identity & Belief
- **Archetype:** `guild` (Ormis'in kurumu; ayrı bir kilise yok) · **Founded:** [[event_divan_kurulusu]], yıl 292 · **Alignment range:** LN–LE
- **Public position:** Ölülerin son anısını ailenin önünde bir kez okur, yasını tutar, adını deftere yazar ki unutulmasın.
- **Relation to the gods:** [[god_ormis]] — okuma Ormis'e "okunur"; Divan onun adıyla mühür basar.
- **Signature presentation:** Siyah yün, kandil isi kokusu, beline asılı mühür; "yas hakkıdır".

### Phase 2 — Power & Resources
- **Power:** 2 · **Intel:** 3 · **Reach:** her cenaze, her aile; Kamışlı hariç
- **Military:** yok; gerekirse `guard` ×3 (Bey'den ödünç) ve `priest` ×1 ([[npc_ilme]])
- **Magical:** Tuz Hafızası ([[signature_tuz_hafizasi]]); İlme'nin rahip büyüleri · **Economic:** okuma ücreti, mühür ücreti, Bey'in borcu · **Territory:** [[place_divan_evi]], [[place_tuz_evi]]
- **Assets on the map:** [[place_divan_evi]], [[place_tuz_evi]], [[npc_yesra]] (kontrol)
- **HQ:** [[place_divan_evi]]

### Phase 3 — Structure & People
- **Leader:** [[npc_ilme]] (sözcü) · **Heir:** [[npc_yesra]]
- **Key web:** [[npc_ilme]] (sözcü), [[npc_yesra]] (okuyucu), Sessiz Kâtip (kimse görmez; adı söylenmez)
- **Access chain:** kapıdaki hizmetli → Yesra (okuma işleri) → İlme; kâtiple kimse görüşmez.
- **Recruitment and exit terms:** okuyucular çocukken seçilir; ayrılan mührünü bırakır ve bir daha okuyamaz.
- **Services to the party:** okuma (aile izniyle, 5 gp mühür + 1 gp kandil), yas tutma (ücretli), bilgi (kim ne zaman ölmüş: defter)
- **Stances:**
  | Toward | Stance | Reason |
  |---|---|---|
  | [[faction_beylik]] | +1 | Bey borçludur; borçlu bey iyi beydir |
  | [[faction_kacakcilar]] | 0 | görünürde ilgisiz |
  | party | 0 | yeni gelenler okunacak ölü değildir, henüz |

### Phase 4 — Intelligence & Operations
- **Network:** her cenazede bir kulak; intel gecikmesi 2 gün
- **Decision logic / doctrine:** aggression `2`; target preference `objective-holder`; move weights: alliance → spy, persuade; loss → persuade, bribe; gain → consolidate; exposure → persuade, assassinate; death → consolidate; betrayal → assassinate
- **Reaction doctrine:**
  | Trigger | Doctrine |
  |---|---|
  | alliance | Yeni ittifakın ölülerini ilk o okumak ister; kandil gönderir |
  | loss | Aileleri yas için toplar, kaybı Beylik'in ihmaline bağlar |
  | gain | Yeni okumaları deftere işler, mühür dağıtır |
  | exposure | Yesra'yı öne sürer; o hatırlamaz, Divan da öyle der |
  | death | İlme ölürse Yesra sözcü olur; kâtip aynı kalır |
  | betrayal | İhanet edenin son anısı erken okunur |
- **First operation:** **Yas Yılı** (`op_divan_1`) — objective: bu yıl on iki okuma
  | Step | Kind | Due day | Defender | Text |
  |---|---|---|---|---|
  | 1 | timed | 0 | — | Üç izinsiz okuma (tamamlandı; `news_0002`) |
  | 2 | timed | 20 | — | Kamışlı'da bir okuma: Ameli'nin annesi |
  | 3 | party-only | 45 | — | Yesra'nın son okuması |
  | 4 | contested | 75 | [[faction_beylik]] | Kandil Kör Fener'e taşınır |
  | doom | timed | 96 | — | Fener yanar |
  - **Abandon if:** `alive(npc_s01) == dead or control(site_kor_fener) == party`
  - **Metric:** okuma 3/12
- **Default policy toward the party:** court; okuma teklif eder
- **Vulnerabilities:** Yesra'nın boşlukları; defterin kopyasının kayıp olması

## Discoverable

- **True belief vs cover:** Üyeler okumanın merhamet olduğuna inanır; İlme okumanın okuyucudan bir şey aldığını bilir ve bunu "yasın bedeli" sayar.
- **Provocation ladder:** rung 1 partinin okuma ricası reddedilir → rung 2 partinin bir tanıdığı "izinsiz" okunur → rung 3 partiden biri deftere yazılır → rung 4 Yesra partiye karşı okur
- **What it wants independent of the party, and what it will have done in 60 days:** On iki okuma ve kandilin Fener'e taşınması; gün 20'de Kamışlı'ya gider, gün 45'te Yesra'yı okutur, gün 60'ta kervanı hazırlar.

