---
entity: faction_kacakcilar
type: faction
secrecy: public
phase: P4
stamped: [archetype, objective]
mirror: design/dm-only/factions/faction_kacakcilar.md
---

# Gelgit Kardeşliği

## Public

### Phase 1 — Identity & Belief
- **Archetype:** `criminal` · **Founded:** Fener söndükten sonra, gemiler azalınca ([[event_fener_sondu]]) · **Alignment range:** N–NE
- **Public position:** "Deniz verir, biz taşırız." Enkaz ve kaçak tuz; kimseye zarar vermeden, sorulmadan.
- **Relation to the gods:** [[god_velune]] — her enkazdan bir kabuk tapınağa bırakılır, kimse görmez.
- **Signature presentation:** Halat düğümü (üç ilmek, biri boş), cezir saatinde çalışma, düğümle mesaj.

### Phase 2 — Power & Resources
- **Power:** 2 · **Intel:** 2 · **Reach:** kayalık kıyı, rıhtım geceleri, Kırık Dalgakıran
- **Military:** `bandit` ×8, `bandit captain` ×2 ([[npc_draskun]], [[npc_kortan]]); üç kayık
- **Magical:** yok · **Economic:** enkaz, kaçak tuz, rehin kayıklar · **Territory:** [[site_gelgit_magarasi]], [[site_batik_iskele]]
- **Assets on the map:** [[site_gelgit_magarasi]], [[site_batik_iskele]], [[place_yorgun_marti]] (rehin yoluyla kontrol)
- **HQ:** [[site_gelgit_magarasi]]

### Phase 3 — Structure & People
- **Leader:** [[npc_draskun]] · **Heir:** [[npc_kortan]]
- **Key web:** [[npc_kortan]] (ikinci adam, iskele bekçisi), [[npc_tolvan]] (borçlu)
- **Access chain:** rıhtımdaki halatçı → Kortan (pazarlık) → Draskun (yalnızca cezirde, mağarada)
- **Recruitment and exit terms:** bir enkaz getiren girer; ayrılan düğümünü çözer ve kıyıyı terk eder, dönerse cezirde mağarada bırakılır.
- **Services to the party:** kayık (sorulmadan), gece geçişi, satın alma (enkaz malı, mühürsüz tuz), bilgi (kim ne taşıdı)
- **Stances:**
  | Toward | Stance | Reason |
  |---|---|---|
  | [[faction_beylik]] | −2 | muhafız iskeleyi basacak; Bey manifestoyu sattı ama sonra korktu |
  | [[faction_divan]] | 0 | görünürde ilgisiz |
  | party | 0 | henüz müşteri mi rakip mi belli değil |

### Phase 4 — Intelligence & Operations
- **Network:** rıhtım hamalları; intel gecikmesi 3 gün
- **Decision logic / doctrine:** aggression `2`; target preference `weakest`; move weights: alliance → spy; loss → seize, sabotage; gain → consolidate; exposure → sabotage; death → hold; betrayal → assassinate
- **Reaction doctrine:**
  | Trigger | Doctrine |
  |---|---|
  | alliance | Rakip ittifakın kayıklarını keser |
  | loss | Kaybı bir gece içinde geri almaya çalışır |
  | gain | Yeni kazancı mağaraya taşır ve saklar |
  | exposure | Tuzun nereye gittiği sorulursa Kortan'ı öne sürer |
  | death | Kortan reis olur; Divan bağlantısı kopar |
  | betrayal | İhanet edeni cezirde mağarada bırakır |
- **First operation:** **Sandık Yolu** (`op_kardeslik_1`) — objective: Kandil'in sandıklarını ve tuzunu Fenerli'den çıkarmak
  | Step | Kind | Due day | Defender | Text |
  |---|---|---|---|---|
  | 1 | timed | 10 | — | Sandıklar Batık İskele'den Gelgit Mağarası'na taşınır |
  | 2 | contested | 25 | [[faction_beylik]] | Liman muhafızına rüşvet; Tolvan'ın kayıkları alınır |
  | 3 | timed | 40 | — | Tuz Divan Evi'ne teslim edilir |
  - **Abandon if:** `control(site_gelgit_magarasi) != faction_kacakcilar or alive(npc_draskun) == dead`
  - **Metric:** tuz çuvalı 4/10
- **Default policy toward the party:** watch; Kortan pazarlık dener
- **Vulnerabilities:** cezire bağımlı; Kortan'ın soruları

## Discoverable

- **True belief vs cover:** Kardeşlik enkaz taşıdığını söyler; asıl yük tuzdur ve tuzun kime gittiğini yalnızca Draskun bilir.
- **Provocation ladder:** rung 1 partinin kayığı bir gece kaybolur → rung 2 Tolvan'ın kayıkları erken alınır → rung 3 gece hana baskın (park: party asset) → rung 4 Draskun partiyi cezirde mağaraya çağırır
- **What it wants independent of the party, and what it will have done in 60 days:** Sandıkları ve tuzu çıkarmak; gün 10'da sandıklar mağarada, gün 25'te kayıklar onların, gün 40'ta tuz Divan'da, gün 60'ta mağara boşalır.

