---
entity: faction_beylik
type: faction
secrecy: public
phase: P4
stamped: [archetype, objective]
mirror: design/dm-only/factions/faction_beylik.md
---

# Sazlık Beyliği

## Public

### Phase 1 — Identity & Belief
- **Archetype:** `state` · **Founded:** Fenerler Çağı'nın ilk yüzyılı ([[era_fenerler]]) · **Alignment range:** LN–N
- **Public position:** Tuz ovasının koruyucusu; vergi alır, liman tutar, fener yakar (yakardı).
- **Relation to the gods:** [[god_velune]] — Velune Tapınağı Beylik'in kurumudur; sabah tuzunu Bey'in rahibi döker.
- **Signature presentation:** Gri pelerin, tuz kristali rozet, "meclis der ki" diye başlayan her cümle.

### Phase 2 — Power & Resources
- **Power:** 3 · **Intel:** 1 · **Reach:** Fenerli ve Sazlık Yolu; düzlükte yok
- **Military:** liman muhafızı, `guard` ×12; Bey'in yanında `knight` ×1 (Bey'in kendisi)
- **Magical:** yok · **Economic:** tuz vergisi (üç yıldır eksik) · **Territory:** [[settlement_fenerli]], [[settlement_kamisli]] (kâğıtta)
- **Assets on the map:** [[place_bey_konagi]], [[settlement_fenerli]], [[place_velune_tapinagi]]
- **HQ:** [[place_bey_konagi]]

### Phase 3 — Structure & People
- **Leader:** [[npc_sarven]] · **Heir:** [[npc_olmar]]
- **Key web:** [[npc_olmar]] (rahip, yeğen), liman muhafız başı (adsız, minor renk)
- **Access chain:** muhafız başı → tuz meclisi kâtibi → Bey; Olmar'la konuşan doğrudan Bey'e ulaşır.
- **Recruitment and exit terms:** muhafızlığa Fenerli doğumlu her erkek ve kadın; ayrılan pelerini bırakır, kimse sormaz.
- **Services to the party:** huzur (ödül ilanı: her sandığa 5 altın), muhafız eşliği (Bey'in izniyle), kayıt ve mühür (evlilik, satış)
- **Stances:**
  | Toward | Stance | Reason |
  |---|---|---|
  | [[faction_divan]] | +1 | Divan cenazeleri tutar, Bey'in borcunu tutar; Bey Divan'a kibar olmak zorunda |
  | [[faction_kacakcilar]] | −2 | Kardeşlik vergi kaçırır ve Bey'in manifestosunu tutar |
  | party | 0 | henüz tanımıyor |

### Phase 4 — Intelligence & Operations
- **Network:** liman muhafızı ve tahsildar; intel gecikmesi 7 gün
- **Decision logic / doctrine:** aggression `1`; target preference `rival`; move weights: alliance → negotiate; loss → hold, spy; gain → consolidate; exposure → bribe; death → consolidate; betrayal → negotiate, seize
- **Reaction doctrine:**
  | Trigger | Doctrine |
  |---|---|
  | alliance | Divan'la rakip bir ittifak görürse meclisi toplar, ittifak teklif eder |
  | loss | Kaybettiği şeyi geri ister, alamazsa vergi keser |
  | gain | Kazancı vergiye sayar ve meclise sunar |
  | exposure | Borcu açığa çıkarsa Olmar'ı öne sürer, kendisi geri çekilir |
  | death | Olmar bey olur; doktrin savunmaya kayar |
  | betrayal | İhanet edeni limandan sürer, Divan'a şikâyet eder |
- **First operation:** **Kandil'in sandıkları** (`op_beylik_1`) — objective: kayıp tuz vergisini bulup meclisi yatıştırmak
  | Step | Kind | Due day | Defender | Text |
  |---|---|---|---|---|
  | 1 | timed | 5 | — | Sandıklar için ödül ilanı: her sandığa beş altın |
  | 2 | contested | 30 | [[faction_kacakcilar]] | Liman muhafızı Batık İskele'yi basar |
  | 3 | timed | 50 | — | Bulunan tuz vergiye sayılır, meclis yatışır |
  - **Abandon if:** `control(site_batik_iskele) == party or alive(npc_sarven) == dead`
  - **Metric:** sandık 0/6
- **Default policy toward the party:** watch; sandık getirene court
- **Vulnerabilities:** Bey'in borcu; muhafızın yarısı satın alınmış

## Discoverable

- **True belief vs cover:** Meclis Beylik'in güçlü olduğuna inanır; Bey, Beylik'in Divan'a borçlu olduğunu bilir.
- **Provocation ladder:** rung 1 muhafız eşliği kesilir → rung 2 ödül ilanı geri çekilir, parti "kaçakçı" diye anılır → rung 3 tutuklama emri
- **What it wants independent of the party, and what it will have done in 60 days:** Sandıkları bulup vergiyi kapatmak; gün 30'da iskeleyi basar (kazanırsa sandıkların yarısını alır, kaybederse muhafız başı ölür ve Bey Divan'dan borç ister), gün 50'de meclise "bulduk" der.

