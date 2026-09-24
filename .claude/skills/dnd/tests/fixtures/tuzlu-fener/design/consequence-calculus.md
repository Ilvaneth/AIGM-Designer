---
entity: none
type: calculus
secrecy: discoverable
phase: P4
stamped: []
mirror: design/dm-only/consequence-calculus.md
---

# Consequence calculus — Tuzlu Fener

## Public

*(nothing — this file has no player-facing layer)*

## Discoverable

### Provocation ladders
#### [[npc_sarven]] / [[faction_beylik]] — Bey Sarven
| Rung | What the party did | What the actor does | On the calendar |
|---|---|---|---|
| 1 | Bey'in ilanını küçümser, sandığı Kardeşlik'e verir | Muhafız eşliği kesilir; ödül partiye ödenmez | 3 gün içinde |
| 2 | Kandil gecesini mecliste sorar | Ödül ilanı geri çekilir; parti "kaçakçı" diye anılır | 7 gün |
| 3 | Manifestoyu meclise götürür | Olmar öne sürülür, Bey geri çekilir; tutuklama emri (Kardeşlik'le işbirliği) | 10 gün |
| 4 | Olmar'ı da yakar | Bey Divan'a gider ve partinin bir tanıdığını okuma listesine koydurur | 14 gün |

#### [[npc_ilme]] / [[faction_divan]] — Divan
| Rung | What the party did | What the actor does | On the calendar |
|---|---|---|---|
| 1 | Okuma ricasını reddeder, Yesra'yı sorgular | Partinin okuma ricası reddedilir; İlme kibar kalır | anında |
| 2 | Defter parçasını gösterir | Partinin bir tanıdığı (Tolvan) "izinsiz" okuma listesine alınır | 7 gün |
| 3 | Tuz Evi'ni basar | Partiden biri deftere yazılır; step_3 öne çekilir | 10 gün |
| 4 | Kâtibi arar | Yesra partiye karşı okur (bir PC'den bir anı) — park edilir, masada | 14 gün |

#### [[npc_draskun]] / [[faction_kacakcilar]] — Kardeşlik
| Rung | What the party did | What the actor does | On the calendar |
|---|---|---|---|
| 1 | Kortan'ı atlatır, sandık alır | Partinin kayığı bir gece kaybolur | 2 gün |
| 2 | Kortan'ı yaralar ya da tuzu sorar | Tolvan'ın kayıkları erken alınır (park: party asset) | 5 gün |
| 3 | Sandıkları Bey'e götürür | Gece hana baskın (park: party asset) | 7 gün |
| 4 | Tuzu durdurur | Draskun partiyi cezirde mağaraya çağırır: pazarlık ya da su | 10 gün |

### A / B scenarios by act
#### Act 1
- **A — parti Beylik'e yanaşır:** Beylik kollar, Kardeşlik erken hamle yapar (kayıklar gün 25 → 18), Divan partiyi listeye almaz ama Yesra'yı erken okutur (gün 45 → 30) çünkü Bey'in adamları defteri görmüştür.
- **B — parti Kardeşlik'le anlaşır:** Bey partiyi kaçakçı sayar, Divan tuzun geldiğini görür ve partiye kandil gönderir (court); kervan zamanında çıkar ve parti ona yakın olur.
- **Actors are this act's own:** [[faction_beylik]], [[faction_divan]], [[faction_kacakcilar]], [[npc_sarven]], [[npc_ilme]], [[npc_draskun]]
