---
entity: npc_tolvan
type: npc
secrecy: public
phase: P5
tier: supporting
stamped: [faction]
mirror: design/dm-only/npcs/npc_tolvan.md
---

# Tolvan — Yorgun Martı'nın hancısı

## Public

- **Appearance:** İnsan, altmışında, iri ve yavaş; sağ kulağında yırtık, önlüğünde hep aynı tuz lekesi. Konuşurken tezgâhı siler.
- **Role / CR / location:** hancı · CR 0 (`commoner`) · usually at [[place_yorgun_marti]] in [[settlement_fenerli]]
- **Faction:** bağımsız · **Tier:** supporting · **Alignment:** NG
- **Demeanor:** Konuşkan, cömert, borcunu saklayan; partiye ilk gece odayı bedava verir.
- **Speech quirk:** Her hikâyeyi "o gece" diye başlatır. · **Voice samples:**
  - *"O gece fırtınaydı, evet, herkes öyle der. Ben de öyle derim. Odanız hazır, para sonra."*
  - *"Kayıklar mı? Kayıklar benim. Şimdilik. Küçük bir iş var, sonra konuşuruz."*
- **Schedule:** Sabah pazar, gün boyu tezgâh, gece geç saate kadar Yesra'yla aynı masa.
- **What they can offer the party / want from the party:** oda, yemek, söylenti, kayık (rehin kalkarsa) / Batık İskele'den bir sandık getirmelerini ister (Kardeşlik'in ondan istediği).
- **Attitude toward party:** friendly
- **Current goal:** Kayıkları geri almak (borç: [[seed_martinin_borcu]]).

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst; borcunu ve o geceyi saklar.
- **Ambitious ↔ Content:** Hanı tutmak, o kadar.
- **Loyal ↔ Opportunistic:** Müşterisine sadık.
- **Brave ↔ Cowardly:** Korkak; kayıkları için değil.

### Relationships
- **Knows:** [[npc_yesra]] — her akşam aynı masa; hikâyelerinin değiştiğini fark eden tek kişi.
- **Owes:** [[npc_draskun]] — iki kayık rehin; gün 25'te alınacak.
- **Fears:** [[npc_sarven]] — Bey'in Kandil gecesini gördü.

### Known Facts — what they actually know and how
- day 0 — Kandil batarken dalgakıranda biri fener salladı — witnessed ([[event_kayip_gemi]]; kime ait olduğunu sanıyor, emin değil)
- day 0 — Kardeşlik sandıkları eski iskeleye taşıdı — inferred (gece kayık sesleri)
- day 0 — Yesra aynı hikâyeyi farklı anlatıyor — witnessed (aylardır)
- day 0 — Fener kırk yıl önce söndü — witnessed (çocuktu)

## Discoverable

- **Motivation with history:** Han babasından kaldı; kayıklar hanın tek geliri. Üç yıl önce kış boş geçince ([[event_kayip_gemi]] sonrası gemiler kesildi) kayıkları Kardeşlik'e rehin verdi. Borcu ödemek değil, borcun ne olduğunu kimsenin duymaması onun için önemli.
- **Weakness derived from personality:** Kayıkları; onları kaybederse han biter ve Tolvan Kamışlı'ya gider.
- **What changes if they die:** Han kapanır; [[seed_martinin_borcu]] Kardeşlik'in lehine kapanır; Yesra'nın boşluklarını fark eden kimse kalmaz.
