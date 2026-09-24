---
entity: arc_1
type: arc
secrecy: public
phase: P7
stamped: [beats, endings]
covers: [beat_1a, beat_1b, beat_1c, seed_martinin_borcu, seed_kamisli_sessizligi, socket_borc, socket_kayip_gemi, socket_divan_egitimi, socket_tuz_okuma]
mirror: design/dm-only/arc.md
---

# Arc — Fener Kime Yanar

## Public

- **Theme (the question):** see [[premise_tuzlu_fener]] — *Unutmak bir kurtuluş mudur, yoksa ikinci bir ölüm mü?*
- **Resolution shape:** Parti hatırlanmanın bedelini kimin ödeyeceğine karar verir; kıyı ya okumayı bırakır ya dürüst okumayı öğrenir. Ne olursa olsun Fener bir cevap olur.
- **Acts:** 1 · **Beats:** 3 · **Chapters:** [[chapter_1]], [[chapter_2]] · **Doom day:** 96

### Beats

#### [[beat_1a]] — Sandıklar (Act 1, inciting)
- **change_kind:** `knowledge`
- **state_before:** Kandil enkazının yükü denizde kayıp sanılıyor.
- **state_after:** Yükün bir kısmı Divan'a ait bir defterdir ve Kardeşlik onu taşımaktadır.
- **what_changes:** Kayıp bir gemi bir sır taşıyordu ve sır hâlâ kıyıda; parti bunu bilen dördüncü taraf olur.
- **world_pressure:** `op_kardeslik_1.step_1` — Kardeşlik sandıkları gün 10'da mağaraya taşıyor; parti ondan önce ya da sonra öğrenir, ama öğrenir.
- **telegraph scene:** Tolvan'ın "küçük işi" ve dalgakıranın kırık ucunda gece yanan fener.
- **delivery paths (2-3):** [[site_batik_iskele]] — 6. odadaki sandık; [[npc_tolvan]] — "o gece"yi anlatır; `news_0001` — sandık söylentisi partiyi rıhtıma çeker.
- **fallbacks (all three written at birth):**
  - *cost:* Parti sandıklara geç kalırsa defter parçası mağaraya gider ve Tolvan kayıkları kaybeder; parti mağarada öğrenir, hansız.
  - *secondary:* Kortan defter parçasını Bey'e satar; Bey saklar, Olmar bulur ve partiye getirir.
  - *deferred:* Defter parçası gün 40'ta tuzla birlikte Divan Evi'ne taşınır; parti onu orada, İlme'nin masasında görür.
- **status:** `pending`

#### [[beat_1b]] — Okuma (Act 1, midpoint shift)
- **change_kind:** `loss`
- **state_before:** Tuz okuması yas için hayırlı bir gelenek sayılır.
- **state_after:** Bir okumanın bir anıyı yok ettiği bilinir; Yesra'nın boşlukları ve defter parçası bunun kanıtıdır.
- **what_changes:** Kasabanın en nazik geleneği bir kayıp mekanizmasıdır; parti bunu bilen ilk kişilerdir ve Yesra'nın bir sonraki okuması artık bir cinayettir.
- **world_pressure:** `op_divan_1.step_3` — gün 45'te Yesra'nın son okuması, partinin önünde.
- **telegraph scene:** Yesra'nın aynı hikâyeyi iki akşam farklı anlatması; İlme'nin "Yesra dinlenecek" demesi.
- **delivery paths (2-3):** [[npc_yesra]] — boşluklar ve defter parçası eşleşir; [[site_gelgit_magarasi]] — tuz çuvalları boğulmuş tuzudur, Yesra kokusundan tanır; [[npc_ilme]] — bir okuma yapar ve bir anısını kaybettiğini masada gösterir.
- **fallbacks (all three written at birth):**
  - *cost:* Parti Yesra'yı korursa okuma Ameli'nin annesine kayar ve Kamışlı bedelini öder.
  - *secondary:* İlme kendisi bir okuma yapar ve bir anısını kaybettiğini masada gösterir.
  - *deferred:* Kanıt gün 75'te kandil kervanıyla gelir: taşınan kandil adları fısıldar.
- **status:** `pending`

#### [[beat_1c]] — Fener (Act 1, resolution)
- **change_kind:** `control`
- **state_before:** Kör Fener sönük; Divan'ın kandili Fenerli'de birikiyor.
- **state_after:** Fener'in kime yandığı bellidir: Divan'ın kâtibine, Ormis'e ya da hiç kimseye.
- **what_changes:** Kıyının hafızası bir kişinin eline geçer ya da serbest kalır; her iki durumda da okuma bir daha eskisi gibi olmaz.
- **world_pressure:** `op_divan_1.step_4` — gün 75'te kandil Fener'e taşınır, gün 96'da yanar.
- **telegraph scene:** Kervan hazırlığı (iki hafta önce), burundan görünen buğulu cam.
- **delivery paths (2-3):** [[site_kor_fener]] — kandil odası; Divan'ın kâtibiyle yüzleşme (İlme aracılığıyla ya da doğrudan); `news_0002` — üç izinsiz okuma zincirinin sonu.
- **fallbacks (all three written at birth):**
  - *cost:* Parti Fener'e geç kalırsa Fener yanar ve parti adını ilk unutan olur; savaş kandil odasında sürer, kaybedilen anılar geri gelmez.
  - *secondary:* İlme mührü alır ve Fener'i kendisi söndürür; Divan biter, İlme de.
  - *deferred:* Doom bir kez ertelenir (kervan durdurulursa +14 gün); Fener bekler, Tuzbağlılar yürür.
- **status:** `pending`

### Endings
- **Win:** Fener yanmaz ya da Ormis'e yanar; defter yakılır, kıyı okumayı bırakır ya da dürüst okumayı öğrenir (aile izni, tek okuma, okuyucunun bedeli açıkça söylenir). Seeds of a next arc: Kamışlı'nın kuyusu hâlâ orada; Kardeşlik reissiz; Beylik borçsuz ama fenersiz.
- **Loss:** Fener kâtibe yanar; kıyıdaki herkes onun adını bilir ve kendi ölülerinin adını unutur. Dünya sonrası: Divan tek kurum, Fenerli bir yas kasabası, parti adını hatırlayan son kişiler.
- **Pyrrhic:** Fener söndürülür ama defterle birlikte Selen'in ağabeyinin ve Vorin'in babasının son anıları da gider; okuma biter, hatırlanmak da.

### Planted hooks
| Hook | Planted where | Payoff hint | Status | Planted day |
|---|---|---|---|---|
| Dalgakıranın kırık ucunda gece yanan fener | [[region_tuz_ovasi]] (far telegraf) | Kortan'ın işareti; sandık gecesi | planted | — |
| Yesra'nın yarım kalan hikâyesi ("adı... neydi...") | [[npc_yesra]] | 1. ipucu; defter parçasıyla eşleşir | planted | — |
| Tolvan'ın tezgâhındaki üç ilmekli düğüm | [[place_yorgun_marti]] | Kardeşlik'in rehini; Kortan'la pazarlık anahtarı | planted | — |

### Quest seed bank
#### [[seed_martinin_borcu]] — Martı'nın Borcu
- **Hook:** Tolvan odayı bedava verir, karşılığında "küçük bir iş" ister. · **Complication:** Borç para değil, bir sandıktır: Kardeşlik Tolvan'dan Batık İskele'deki bir sandığı istiyor. · **Resolution:** Sandık teslim edilir (defter parçası gider) ya da borç başka türlü kapanır (Kortan'la pazarlık, Bey'in ödemesi, kayıkların zorla alınması). · **Reward:** Han üssü olur; Tolvan "o gece"yi anlatır.
- **Tied to:** [[npc_tolvan]], [[faction_kacakcilar]] · **Site:** [[site_batik_iskele]]

#### [[seed_kamisli_sessizligi]] — Kamışlı'nın Sessizliği
- **Hook:** Ameli Fenerli'ye gelir; Divan'a değil, hana gider. · **Complication:** Kapıyı çalan Ameli'nin annesidir: okunmadan gömüldü, Tuzbağlı oldu, evini hatırlıyor. · **Resolution:** Anne yatıştırılır (kandil ışığı, adının söylenmesi) ya da yok edilir; köy okumayı kabul eder ya da reddeder ve sonuç Divan'a gider. · **Reward:** Kamışlı partiye kapı açar; kuyunun yolu ve telegrafları anlatılır.
- **Tied to:** [[npc_ameli]], [[settlement_kamisli]] · **Site:** [[site_dipsiz_kuyu]]

### Hook sockets *(party × 2 in `short`; two bound at `integrate`, two live on as seeds)*
| Socket | Kind | Node | NPC | Question (primer) | Bound to |
|---|---|---|---|---|---|
| [[socket_borc]] | debt | [[node_c1_marti]] | [[npc_tolvan]] | Fenerli'de birine borcun var mı, ya da borcu olan birine bağlı mısın? | [[pc_selen]] |
| [[socket_kayip_gemi]] | family_at_event | [[node_c1_iskele]] | [[npc_sarven]] | Üç yıl önce Kandil battığında ailenden biri o gemide miydi? | [[pc_vorin]] |
| [[socket_divan_egitimi]] | trained_under | [[node_c1_divan]] | [[npc_ilme]] | Yas Tutanlar Divanı'nda hiç eğitim aldın mı, ya da oradan gönderildin mi? | — |
| [[socket_tuz_okuma]] | witnessed | [[node_c2_kamisli]] | [[npc_yesra]] | Hiç bir tuz okumasında bulundun mu? O günden ne hatırlıyorsun? | — |

## Discoverable

- Portentler sıralıdır: üç izinsiz okuma (gün 0), Kamışlı'da okuma (gün 20), Yesra'nın son okuması (gün 45), kervan (gün 75). Dikkatli bir parti üçüncüden önce deseni görür.
