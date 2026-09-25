---
entity: none
type: calculus
secrecy: discoverable
phase: P4
stamped: []
mirror: design/dm-only/consequence-calculus.md
---

# Consequence calculus — Salt Lantern

## Public

*(nothing — this file has no player-facing layer)*

## Discoverable

### Provocation ladders
#### [[npc_sarven]] / [[faction_reedmarch]] — Reeve Sarven
| Rung | What the party did | What the actor does | On the calendar |
|---|---|---|---|
| 1 | Reeve'in ilanını küçümser, sandığı Brotherhood'a verir | Muhafız eşliği kesilir; ödül partiye ödenmez | 3 gün içinde |
| 2 | Vesper gecesini mecliste sorar | Ödül ilanı geri çekilir; parti "kaçakçı" diye anılır | 7 gün |
| 3 | Manifestoyu meclise götürür | Olmar öne sürülür, Reeve geri çekilir; tutuklama emri (Brotherhood'la işbirliği) | 10 gün |
| 4 | Olmar'ı da yakar | Reeve Court'a gider ve partinin bir tanıdığını okuma listesine koydurur | 14 gün |

#### [[npc_ilme]] / [[faction_court_of_mourners]] — Court
| Rung | What the party did | What the actor does | On the calendar |
|---|---|---|---|
| 1 | Okuma ricasını reddeder, Yesra'yı sorgular | Partinin okuma ricası reddedilir; Ilme kibar kalır | anında |
| 2 | Defter parçasını gösterir | Partinin bir tanıdığı (Tolvan) "izinsiz" okuma listesine alınır | 7 gün |
| 3 | Salt House'u basar | Partiden biri deftere yazılır; step_3 öne çekilir | 10 gün |
| 4 | Kâtibi arar | Yesra partiye karşı okur (bir PC'den bir anı) — park edilir, masada | 14 gün |

#### [[npc_draskun]] / [[faction_tide_brotherhood]] — Brotherhood
| Rung | What the party did | What the actor does | On the calendar |
|---|---|---|---|
| 1 | Kortan'ı atlatır, sandık alır | Partinin kayığı bir gece kaybolur | 2 gün |
| 2 | Kortan'ı yaralar ya da tuzu sorar | Tolvan'ın kayıkları erken alınır (park: party asset) | 5 gün |
| 3 | Sandıkları Reeve'e götürür | Gece hana baskın (park: party asset) | 7 gün |
| 4 | Tuzu durdurur | Draskun partiyi cezirde mağaraya çağırır: pazarlık ya da su | 10 gün |

### A / B scenarios by act
#### Act 1
- **A — parti Reedmarch'a yanaşır:** Reedmarch kollar, Brotherhood erken hamle yapar (kayıklar gün 25 → 18), Court partiyi listeye almaz ama Yesra'yı erken okutur (gün 45 → 30) çünkü Reeve'in adamları defteri görmüştür.
- **B — parti Brotherhood'la anlaşır:** Reeve partiyi kaçakçı sayar, Court tuzun geldiğini görür ve partiye kandil gönderir (court); kervan zamanında çıkar ve parti ona yakın olur.
- **Actors are this act's own:** [[faction_reedmarch]], [[faction_court_of_mourners]], [[faction_tide_brotherhood]], [[npc_sarven]], [[npc_ilme]], [[npc_draskun]]
