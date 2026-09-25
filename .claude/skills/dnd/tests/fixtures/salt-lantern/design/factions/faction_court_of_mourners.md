---
entity: faction_court_of_mourners
type: faction
secrecy: public
phase: P4
stamped: [archetype, objective]
mirror: design/dm-only/factions/faction_court_of_mourners.md
---

# Court of Mourners

## Public

### Phase 1 — Identity & Belief
- **Archetype:** `guild` (Ormis'in kurumu; ayrı bir kilise yok) · **Founded:** [[event_court_founding]], yıl 292 · **Alignment range:** LN–LE
- **Public position:** Ölülerin son anısını ailenin önünde bir kez okur, yasını tutar, adını deftere yazar ki unutulmasın.
- **Relation to the gods:** [[god_ormis]] — okuma Ormis'e "okunur"; Court onun adıyla mühür basar.
- **Signature presentation:** Siyah yün, kandil isi kokusu, beline asılı mühür; "yas hakkıdır".

### Phase 2 — Power & Resources
- **Power:** 2 · **Intel:** 3 · **Reach:** her cenaze, her aile; Reedham hariç
- **Military:** yok; gerekirse `guard` ×3 (Reeve'den ödünç) ve `priest` ×1 ([[npc_ilme]])
- **Magical:** Salt Memory ([[signature_salt_memory]]); Ilme'nin rahip büyüleri · **Economic:** okuma ücreti, mühür ücreti, Reeve'in borcu · **Territory:** [[place_mourners_hall]], [[place_salt_house]]
- **Assets on the map:** [[place_mourners_hall]], [[place_salt_house]], [[npc_yesra]] (kontrol)
- **HQ:** [[place_mourners_hall]]

### Phase 3 — Structure & People
- **Leader:** [[npc_ilme]] (sözcü) · **Heir:** [[npc_yesra]]
- **Key web:** [[npc_ilme]] (sözcü), [[npc_yesra]] (okuyucu), Silent Scribe (kimse görmez; adı söylenmez)
- **Access chain:** kapıdaki hizmetli → Yesra (okuma işleri) → Ilme; kâtiple kimse görüşmez.
- **Recruitment and exit terms:** okuyucular çocukken seçilir; ayrılan mührünü bırakır ve bir daha okuyamaz.
- **Services to the party:** okuma (aile izniyle, 5 gp mühür + 1 gp kandil), yas tutma (ücretli), bilgi (kim ne zaman ölmüş: defter)
- **Stances:**
  | Toward | Stance | Reason |
  |---|---|---|
  | [[faction_reedmarch]] | +1 | Reeve borçludur; borçlu reeve iyi beydir |
  | [[faction_tide_brotherhood]] | 0 | görünürde ilgisiz |
  | party | 0 | yeni gelenler okunacak ölü değildir, henüz |

### Phase 4 — Intelligence & Operations
- **Network:** her cenazede bir kulak; intel gecikmesi 2 gün
- **Decision logic / doctrine:** aggression `2`; target preference `objective-holder`; move weights: alliance → spy, persuade; loss → persuade, bribe; gain → consolidate; exposure → persuade, assassinate; death → consolidate; betrayal → assassinate
- **Reaction doctrine:**
  | Trigger | Doctrine |
  |---|---|
  | alliance | Yeni ittifakın ölülerini ilk o okumak ister; kandil gönderir |
  | loss | Aileleri yas için toplar, kaybı Reedmarch'ın ihmaline bağlar |
  | gain | Yeni okumaları deftere işler, mühür dağıtır |
  | exposure | Yesra'yı öne sürer; o hatırlamaz, Court da öyle der |
  | death | Ilme ölürse Yesra sözcü olur; kâtip aynı kalır |
  | betrayal | İhanet edenin son anısı erken okunur |
- **First operation:** **Year of Mourning** (`op_court_1`) — objective: bu yıl on iki okuma
  | Step | Kind | Due day | Defender | Text |
  |---|---|---|---|---|
  | 1 | timed | 0 | — | Üç izinsiz okuma (tamamlandı; `news_0002`) |
  | 2 | timed | 20 | — | Reedham'da bir okuma: Ameli'nin annesi |
  | 3 | party-only | 45 | — | Yesra'nın son okuması |
  | 4 | contested | 75 | [[faction_reedmarch]] | Kandil Blind Lantern'e taşınır |
  | doom | timed | 96 | — | Lantern yanar |
  - **Abandon if:** `alive(npc_s01) == dead or control(site_blind_lantern) == party`
  - **Metric:** okuma 3/12
- **Default policy toward the party:** court; okuma teklif eder
- **Vulnerabilities:** Yesra'nın boşlukları; defterin kopyasının kayıp olması

## Discoverable

- **True belief vs cover:** Üyeler okumanın merhamet olduğuna inanır; Ilme okumanın okuyucudan bir şey aldığını bilir ve bunu "yasın bedeli" sayar.
- **Provocation ladder:** rung 1 partinin okuma ricası reddedilir → rung 2 partinin bir tanıdığı "izinsiz" okunur → rung 3 partiden biri deftere yazılır → rung 4 Yesra partiye karşı okur
- **What it wants independent of the party, and what it will have done in 60 days:** On iki okuma ve kandilin Lantern'e taşınması; gün 20'de Reedham'a gider, gün 45'te Yesra'yı okutur, gün 60'ta kervanı hazırlar.

