---
entity: faction_reedmarch
type: faction
secrecy: public
phase: P4
stamped: [archetype, objective]
mirror: design/dm-only/factions/faction_reedmarch.md
---

# Reedmarch

## Public

### Phase 1 — Identity & Belief
- **Archetype:** `state` · **Founded:** Age of Lanterns'in ilk yüzyılı ([[era_lanterns]]) · **Alignment range:** LN–N
- **Public position:** Tuz ovasının koruyucusu; vergi alır, liman tutar, fener yakar (yakardı).
- **Relation to the gods:** [[god_velune]] — Temple of Velune Reedmarch'ın kurumudur; sabah tuzunu Reeve'in rahibi döker.
- **Signature presentation:** Gri pelerin, tuz kristali rozet, "meclis der ki" diye başlayan her cümle.

### Phase 2 — Power & Resources
- **Power:** 3 · **Intel:** 1 · **Reach:** Lanternside ve Reed Road; düzlükte yok
- **Military:** liman muhafızı, `guard` ×12; Reeve'in yanında `knight` ×1 (Reeve'in kendisi)
- **Magical:** yok · **Economic:** tuz vergisi (üç yıldır eksik) · **Territory:** [[settlement_lanternside]], [[settlement_reedham]] (kâğıtta)
- **Assets on the map:** [[place_reeves_manor]], [[settlement_lanternside]], [[place_temple_of_velune]]
- **HQ:** [[place_reeves_manor]]

### Phase 3 — Structure & People
- **Leader:** [[npc_sarven]] · **Heir:** [[npc_olmar]]
- **Key web:** [[npc_olmar]] (rahip, yeğen), liman muhafız başı (adsız, minor renk)
- **Access chain:** muhafız başı → Salt Council kâtibi → Reeve; Olmar'la konuşan doğrudan Reeve'e ulaşır.
- **Recruitment and exit terms:** muhafızlığa Lanternside doğumlu her erkek ve kadın; ayrılan pelerini bırakır, kimse sormaz.
- **Services to the party:** huzur (ödül ilanı: her sandığa 5 altın), muhafız eşliği (Reeve'in izniyle), kayıt ve mühür (evlilik, satış)
- **Stances:**
  | Toward | Stance | Reason |
  |---|---|---|
  | [[faction_court_of_mourners]] | +1 | Court cenazeleri tutar, Reeve'in borcunu tutar; Reeve Court'a kibar olmak zorunda |
  | [[faction_tide_brotherhood]] | −2 | Brotherhood vergi kaçırır ve Reeve'in manifestosunu tutar |
  | party | 0 | henüz tanımıyor |

### Phase 4 — Intelligence & Operations
- **Network:** liman muhafızı ve tahsildar; intel gecikmesi 7 gün
- **Decision logic / doctrine:** aggression `1`; target preference `rival`; move weights: alliance → negotiate; loss → hold, spy; gain → consolidate; exposure → bribe; death → consolidate; betrayal → negotiate, seize
- **Reaction doctrine:**
  | Trigger | Doctrine |
  |---|---|
  | alliance | Court'la rakip bir ittifak görürse meclisi toplar, ittifak teklif eder |
  | loss | Kaybettiği şeyi geri ister, alamazsa vergi keser |
  | gain | Kazancı vergiye sayar ve meclise sunar |
  | exposure | Borcu açığa çıkarsa Olmar'ı öne sürer, kendisi geri çekilir |
  | death | Olmar reeve olur; doktrin savunmaya kayar |
  | betrayal | İhanet edeni limandan sürer, Court'a şikâyet eder |
- **First operation:** **The Vesper's Crates** (`op_reedmarch_1`) — objective: kayıp tuz vergisini bulup meclisi yatıştırmak
  | Step | Kind | Due day | Defender | Text |
  |---|---|---|---|---|
  | 1 | timed | 5 | — | Sandıklar için ödül ilanı: her sandığa beş altın |
  | 2 | contested | 30 | [[faction_tide_brotherhood]] | Liman muhafızı Sunken Pier'i basar |
  | 3 | timed | 50 | — | Bulunan tuz vergiye sayılır, meclis yatışır |
  - **Abandon if:** `control(site_sunken_pier) == party or alive(npc_sarven) == dead`
  - **Metric:** sandık 0/6
- **Default policy toward the party:** watch; sandık getirene court
- **Vulnerabilities:** Reeve'in borcu; muhafızın yarısı satın alınmış

## Discoverable

- **True belief vs cover:** Meclis Reedmarch'ın güçlü olduğuna inanır; Reeve, Reedmarch'ın Court'a borçlu olduğunu bilir.
- **Provocation ladder:** rung 1 muhafız eşliği kesilir → rung 2 ödül ilanı geri çekilir, parti "kaçakçı" diye anılır → rung 3 tutuklama emri
- **What it wants independent of the party, and what it will have done in 60 days:** Sandıkları bulup vergiyi kapatmak; gün 30'da iskeleyi basar (kazanırsa sandıkların yarısını alır, kaybederse muhafız başı ölür ve Reeve Court'tan borç ister), gün 50'de meclise "bulduk" der.

