---
entity: site_batik_iskele
type: site
secrecy: public
phase: P6
status: detailed
stamped: [danger_tier, room_count, act, thread, key_npcs]
covers: [item_tuz_defteri]
mirror: design/dm-only/sites/site_batik_iskele.md
---

# Batık İskele — dungeon (ruin), T1, 6 rooms (Act 1)

## Public

### Phase 1 — Concept & ecology
- **What this place is:** Fenerli'nin üç yıl önce, Kandil'in battığı fırtınada çöken eski ahşap iskelesi. Kazıkların yarısı ayakta, ambarlar yarı su altında; Kardeşlik enkazdan çıkardığı sandıkları buraya taşıdı çünkü kimse çökük bir iskeleye girmez. Metle su bele çıkar, cezirde kumsal açılır.
- **Danger tier:** **T1** (CR 0-2) · **Role:** minor · **Room count:** **6** · **Payoff:** plot_item — [[item_tuz_defteri]] (defter parçası) ve Kandil'in sandıkları
- **Thread:** [[beat_1a]] · **Key NPCs:** [[npc_kortan]] · **Attitude to intruders:** capture (Kardeşlik soru sorar, sonra bağlar)
- **Ecology:** Üst ambarda iki Kardeşlik haydutu (`bandit`, minion) nöbet tutar, gündüz uyur. Su basmış alt ambarda iki Tuzbağlı ([[creature_tuzbagli]], minion) durur: Kandil'in okunmadan gömülen iki tayfası, sandıkların yanında bekler ve karanlıkta yürür; Kardeşlik onları kandille tutar. Kortan sandık odasında, kandili elinde.
- **Telegraphs:** far — dalgakıranın kırık ucunda gece fener yanar, kimse yakmaz (Kortan'ın işareti); near — kazıkların dibinde tuz kabuğu bağlamış ayak izleri, hepsi denize doğru; threshold — ilk ambarın kapısında taze kesilmiş halat ve bir Kardeşlik düğümü.
- **Escape geometry:** Cezirde 4. odadan kumsala; metle 1. odadan geri yürüyüş yoluna, ama su bele kadar ve Tuzbağlılar suda hızlı. Giriş ve çıkış aynı yol olmak zorunda değil: 1'den girip 4'ten çıkmak mümkün.
- **Rest pressure / sanctuary:** 2. oda boşaltıldıysa kısa dinlenme mümkün; uzun dinlenme yok (met gece gelir, su 2'ye çıkar).

### Phase 2 — Map
- **Entrances (≥2):** room 1 (kırık yürüyüş yolundan, her saat), room 4 (kumsaldan, yalnızca cezirde: günde iki kez, dörder saat)
- **Verticality:** üst ambar (1-3) kazıklar üstünde; alt ambar (5-6) su seviyesinde, 4'ten 5'e iki metrelik çukur.
- **Loop:** 1 → 2 → 3 → 5 → 4 → 1: alt ambardan kumsala çıkan, yürüyüş yolundan geri dönmez. Payoff (6) 5'ten çıkan tek kapı, döngüde değil.
- **Minimum depth:** 3 rooms (4 → 5 → 6)
- **Sketch:** Yürüyüş yolu (1) ambar kapısına (2) açılır; 2'den çürük döşemeli geçit (3) alt ambara inen merdivene; alt ambar (5) su içinde, batıda kumsal ağzı (4), doğuda kilitli sandık odası (6).

### Phase 3 — Room-by-room
| # | Room | Category | Content | Exits | XP |
|---|---|---|---|---|---|
| 1 | Kırık Yürüyüş Yolu [Entrance] | structural | Kazıklar üstünde ıslak tahta; her üçüncü tahta yok. Kapıda taze halat ve düğüm (threshold telegraf). Metle su dizde. | 2 (kapı), 4 (kumsal, cezirde) | 0 |
| 2 | Üst Ambar | combat | 2 haydut (`bandit`), gündüz uyur, gece zar atar. Kandil yanık. İlk ses Kortan'a ulaşmaz (su sesi). Kazanırsa parti: 6 gp, bir Kardeşlik düğümü. | 1, 3 | 50 |
| 3 | Çürük Döşeme | trap | Geçidin ortası çürük: DEX DC 12 ya da 1d6 ve 5. odaya düşüş (suya, Tuzbağlıların yanına). Tell: tahtalar tuz beyazı, üstlerinde ayak izi yok. | 2, 5 (merdiven) | 0 |
| 4 | Kumsal Ağzı [Entrance] | special | Cezirde açılan alçak geçit; içeride gelgit çizgisi ve kazınmış saat işaretleri. Met yaklaşınca su yükselir: dört saat. 5'e iki metre çukur, tek yön. | 1 (cezirde), 5 (tek yön, çukur) | 0 |
| 5 | Su Basmış Ambar | combat | Bele kadar su. 2 Tuzbağlı ([[creature_tuzbagli]]) sandıkların dibinde durur; kandil taşıyan yaklaşırsa hareketsiz, kandil sönerse suda yürür. Vuruş yiyen bir dakika adını unutur (CON DC 10). Geri tırmanış 4'e DEX DC 12. | 3, 4 (tırmanış DC 12), 6 (kilitli; anahtar Kortan'da ya da Thieves' Tools DC 13) | 400 |
| 6 | Sandık Odası [Payoff] | special | Kuru, yüksek platform; altı sandık, üstünde Kandil mührü. [[npc_kortan]] kandil elinde: savaş değil pazarlık teklif eder (sandığın biri karşılığında çıkış). Bir sandıkta [[item_tuz_defteri]]: on iki yaprak, "tüketilenler" başlığı. Savaşılırsa Kortan `bandit captain`, +450 XP, bütçe dışı. | 5 | 0 |

- **Total XP:** 450 vs budget 450 · **Rooms:** 6 vs stamp 6

### Phase 4 — Content variety check
| Category | Rooms | Share | Band |
|---|---|---|---|
| combat | 2 | 33 % | ~50 % |
| trap | 1 | 17 % | ~10 % |
| special | 2 | 33 % | 10-15 % |
| structural | 1 | 17 % | 15-20 % |
*(altı odalık minor bir sitede bantlar kabadır; validator minor rol için ±20 puan tolerans uygular)*

### Boss
Yok (minor site). Kortan bir patron değil, bir kapıdır: pazarlık edilir ya da geçilir.

### Loot
| Where | What | Rarity / attunement | Note |
|---|---|---|---|
| room 2 | 6 gp, bir Kardeşlik düğümü | — | düğüm Kortan'la pazarlıkta işe yarar |
| room 6 | [[item_tuz_defteri]] (defter parçası) | plot | 2. ipucu; Kortan neyin olduğunu bilmez |
| room 6 | Kandil'in sandıkları ×6: 4 tuz (Bey'in vergisi, sandık başına 5 gp ödül), 1 halat ve yelken, 1 Divan mührüyle kapalı (defter) | — | Bey'e götürülürse op_beylik_1 metriği ilerler |

## Running this well
- Telegrafları sırayla ver: fener (uzaktan), izler (yaklaşırken), düğüm (kapıda). Parti düğümü tanıyorsa Kortan'ın kim olduğunu bilir.
- 5. odada kandil kuraldır: kandil yanıyorsa Tuzbağlılar durur. Kandili söndüren ya da düşüren partiye suda iki Tuzbağlı gelir; bu odanın savaşı seviye 1 için ölümcül olabilir, telegraf açık.
- Kortan pazarlıkçıdır; "bir sandık senin, biri benim, defter kimin?" sorusunu partiye bırak.
- Üç seviye erken bir parti (yani bu parti, seviye 1): 2. odayı alır, 3'te düşer, 5'te kandil yoksa kaçar. Kaçış 4'ten kumsala, cezirdeyse.

## Connections
- **Before:** [[seed_martinin_borcu]] — Tolvan'ın "küçük işi" bu sandıktır · **After:** [[item_tuz_defteri]] Yesra'nın boşluklarıyla eşleşir ([[beat_1b]]'ye yol); sandıklar Bey'e giderse op_beylik_1 ilerler, Kardeşlik'e kalırsa op_kardeslik_1.step_1
- **News:** Sandıklar taşınırsa "eski iskelede gece kayık sesleri kesildi"; Kortan ölürse Kardeşlik'in bekçisi değişir ve fener bir daha yanmaz.

## Discoverable

- Kumsal girişini Tolvan bilir (kayıkçı); cezir saatlerini gelgit çizgisindeki işaretler söyler.
- Tuzbağlıların kandille durduğunu Yesra söyler, sorulursa.
