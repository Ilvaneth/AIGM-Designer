# Campaign: Ashen Crown
**Created:** 2026-08-23 (migrated to this structure 2026-09-06)  **Last session:** 2026-09-22  **Session count:** 37  **Ruleset:** 2014

## Current Situation
- **★★★★★★★ GÜNCEL (session 36 sonu, 2026-09-22) — Location:** **The Ember Court** (Kaal hanesinin sınır düzlemi, `reference/ember-court.md`). Parti Oda 1-11'i tamamen temizledi (2× Rakshasa muhafız, 4× Barbed Devil, 9× Lemure, Baş Yazman/özel Spinagon, Sözleşme Kasası'nın Bone Devil'i + loot, 4× Barghest, Borçlular Galerisi'nde bilgi alışverişi — savaşsız, 2× Erinyes, kıdemli Bone Devil, kıdemli Rakshasa Yönetici, Rakshasa Şampiyonu). **Oda 12'nin eşiğinde durdu** — içeride 3× Rakshasa askeri bekliyor, henüz girilmedi. **Rest YOK, henüz eve dönülmedi, hâlâ Iskra/Sathriel'in reform saatine karşı yarışıyorlar.**
- **Arkaplan:** Üç hane yemeğinden sonra (Corr/Sablewood/Ilvane, gün 201) parti "Kesh Amara" sözleşme evini (Kingsward Dış Mahalle) buldu — D.V./Elian Rook üzerinden sızdılar (**Cinderday gecesi, 37 Ashfall / gün 203**, imp-muhafızın hafızası silinerek). O geceki toplantıda Iskra, **Sathriel**, bir yazman-imp, ve **Ostwin Kade** (Veskin'in kâtibi) ile karşılaştılar — imp ve Kade öldü, ama Iskra/Sathriel rakshasa doğaları gereği kalıcı ölmedi, ağır yaralı bedenleri Kaal'ın düzlemine (Ember Court) çekildi, Oda 24'teki Kor Beşiği'nde reform oluyorlar. Parti peşlerinden Teleportation Circle'dan geçti — reform tamamlanmadan Oda 24'e ulaşıp onları kalıcı yok etmek bir yarış. *(Session 36'da düzeltilen bir kayıt hatası: önceki save bu 24 odalık dungeon'ı hiç oynanmamış atlayıp "zaten bitti" diye kaydetmişti — bkz. Continuity Archive.)*
- **In-world date:** Duskday, 38 Ashfall 1188 — öğle (11:20)  [Gün 204]  ·  **The Ember Court**'ta (oran **x2**, içeride geçen: 6s 40dk yerel)
  - *Bu satır `calendar.py -c ashen-crown stateline` çıktısıdır — elle yazılmaz, her sahne sonrası oradan kopyalanır. Saat artık `calendar.json`'da dakika hassasiyetinde tutuluyor.*
  - **Düzlem zamanı — ORAN x2 (oyuncu kararı, 2026-09-22):** içeride geçen her saat dışarıda **iki saat**. Ember Court'a giriş Gün 203, 22:00 (Cinderday gecesi); session 36'nın Oda 1-11'i ~4 saat yerel = **8 saat maddi** olarak işlendi (tahmini; oynanırken `calendar.py scene ...` ile netleşir), bu yüzden dışarıda saat 06:00.
  - **★ Yarış:** Iskra ve Sathriel'in Kor Beşiği'nde reformu tamamlaması **gün 206**'da (`factions.py show whisper-court`). Oran x2 olduğu için partinin içeride harcadığı her saat bu tarihe iki kat hızla yaklaşıyor — Oda 12'den Oda 24'e kalan yol, yerel ~24 saatten azına sığmak zorunda.
  - **✓ Çözüldü (2026-09-22, session 36 `/dm:dnd end`, oyuncu kararı):** gün sayacı kanonik — **gün 203 = 37 Ashfall = Cinderday.** Kesh Amara sızmasının eski "Restday gecesi" etiketi yanlış yazılmıştı; Elian Rook'un defterindeki toplantı örüntüsü **Cinderday** geceleridir ve sızma 37 Ashfall gecesi yapıldı. Bütün kayıtlar (state.md, session-log.md, npcs.md) buna göre düzeltildi. Sarelle'in Ashvale'deki zayıf saati ayrı ve doğru bir olgudur — o gerçekten Restday geceleridir, değiştirilmedi.
- **Party:** Ilvaneth Duskmere — High Elf Necromancy Wizard **17** | HP 116/116 | AC **19** | XP **270.807** | Neutral Evil | Proficiency +6 | **9. seviye slot açıldı (True Polymorph, Power Word Kill kullanılabilir)** | Inspiration ✓ | **Ascension Stage 4 aktif** | **★ LEVEL UP PENDING (18, eşik 265.000) — bir sonraki Long Rest'te işlenecek** || Kriv Shestendeliath — Red Dragonborn Battle Master Fighter **17** | HP 196/196 | AC **22** | XP **270.807** | Neutral Evil | Proficiency +6 | Action Surge 2/2, Indomitable 3/3, Hit Dice 13/17 | Inspiration ✓ | **Ascension Stage 4 aktif (uçuş 60ft, 9d6 nefes/40ft koni, Truesight 60ft, Legendary Resistance 1/gün)** | **★ LEVEL UP PENDING (18, eşik 265.000) — bir sonraki Long Rest'te işlenecek**
- **Party status (2026-09-21 güncellendi, session 36 yüklemesi düzeltmesi):** **Wren Marrow himayede.** Sunken Ledger yok edildi. **Üç hane (Corr/Sablewood/Ilvane) gergin bir ittifakta** — Sereth "borç ödeşmesi" (soğuk), Berengar kârla tatmin, Cassian gerçek bir müttefik/borçlu (kendi hanesini temizliyor, kendi evladı-dışı sırrı parti elinde, ona gösterilmedi). **★★★★★★★ Iskra Vantrel ve Sathriel HENÜZ KALICI OLARAK ÖLMEDİ — Oda 24'te (Kor Beşiği) reform oluyorlar, parti Ember Court'ta Oda 3'e ilerliyor, saat işliyor.** **Ostwin Kade (Veskin'in kâtibi) öldü** — Kesh Amara'daki ilk çarpışmada, gönüllü "yeni taraf" adayı olarak. **Aşkalkanı/"Bayan V." ipliği** (Karsgate/House Corvane, 17 yıl önce, AYRI bir "V." izi) hâlâ çözülmedi. **Coren Ashvale ile gizli darbe planı** sürüyor. **Tain'in Concordat devri sürüyor.** Goal Tracker: **Maro Veskin THREATENED**, **Whisper Court THREATENED (Iskra/Sathriel Ember Court'ta reform halinde, henüz kalıcı kapanmadı — düzeltildi, session 36).** Sylandra Cael ile tam ortaklık sürüyor. Ser Aldwin Ashvale (ghost) ile ittifak. **Tobin Wrey hâlâ düşman, henüz haberi yok.**

## Pinned Facts
*Soft facts the DM always keeps — canon the table never wants forgotten.*
- **Content lines/veils: none set** — masa karanlık/gore temaları tam kapsamda istiyor, bu bilinçli bir karar (dm-notes.md'den doğrulandı).
- **Standing rule — eşit anlatı ağırlığı:** Hiçbir oturum bir PC'nin kişisel ipliğini canlı bırakıp diğerini uyutmasın. Bu, Ilvaneth'in ipliği orantısız büyüdükten sonra bilinçli olarak düzeltildi — Kriv'in ipliğine (kriv-thread.md) eşit ağırlık ver.
- **Ascension Tracks geri dönüşsüz:** Her iki karakter de Crown parçası + seviye eşiğiyle kilitleniyor (bkz. reference/ascension-tracks.md). Asla zorlama — ikisi de birbirine yalan söylemiyor, çatışma dürüstçe büyüsün.
- **★ REVİZE (2026-09-18, session 33) — Kriv/Ilvaneth'in yapısal çatışması OYUNDA ORGANİK OLARAK ÇÖZÜLDÜ, artık geçerli değil.** Kriv, İlvaneth'in gücünün kendisine getirdiği somut kazançları (unvan, topraklar, ordu) görüp tam destek veriyor — "ayrı tutma" mirasını umursamıyor, ikisi de birleştirmek istiyor. Bu asla geri zorlanmamalı, dürüst bir oyuncu kararıydı.
- **★ REVİZE (2026-09-18, session 33) — Ashen Crown'un gerçek doğası artık farklı: tac bir yas-kalıntısı değil, panteonun bastırılmış/silinmiş yedinci tanrısı Ashborn'un gücünü hapseden bir MÜHÜR.** Tam detay `## Campaign Arc → resolution`'ın altındaki DM-only blokta. Bu SADECE DM bilgisi, oyunculara asla doğrudan söylenmedi — tamamlanınca Ashborn kısmen serbest kalır, kampanyanın finalini (Act 3) tetikler.

## World State
- **Session 35 başlangıç durumu (tarihsel kayıt — güncel saat için yukarıdaki Current Situation'a bak):** 32 Ashfall 1188 AR (Gün 198), sabah saat 8, Hollowday — Emberhold, House Sablewood malikanesi, misafir odası, uzun mola bitti. **Session 35 devamı — parti "V."nin teklifini reddetti (Kırık Kemer köprüsü, Pike Rourke), Scrying+Invisibility ile mesajın House Ilvane'in duvarları içine (hizmetçi girişi) taşındığını doğruladı, sonra Lord Berengar Sablewood'dan Cassian Ilvane'i (yanlışlıkla önce Iskra Vantrel sanılan bir talepten sonra düzeltildi) kendi evine "komşuca dayanışma" bahanesiyle çağırmasını istedi — bugün öğleden sonra gerçekleşecek. İlvaneth'in 19. Ascension rüyası: Ostrin Vell'in katili — sağ elinin küçük parmağında kırık-daire motifli gümüş bir yüzük takan, sakin/deneyimli bir kadın sesi, "Sessiz olmalıydın, Ostrin" demiş.**
- **YENİ (gün 176) — Emberhold, Chapter 2 aktif faction/NPC durumu:**
  - **The Unmade** (Sylandra Cael'in ilk başarısız kendi-koruma denemesi, Kule-i Mensuh) — **YENİLDİ, YOK EDİLDİ** (gün 176, Ash Reeve Understreets).
  - **Sylandra Cael / The Unfinished Circle** (Ash Reeve, Emberhold altı) — ilk temas kuruldu, **conditional/test aşamasında** — Vashti Coldharrow testi tamamlanana kadar tam güven yok.
  - **The Silent Ledger** (Emberhold'un gizli suikastçı/bilgi ağı) — bir üyesi (Assassin) ve iki ajanı öldürüldü (Ser Aldric Vane'i hedef alan yanlış suikast girişimi), bir jeton ele geçirildi. Kimin arkasında olduğu bilinmiyor.
  - **House Corr (Sereth Corr)** — Ser Aldric Vane üzerinden dolaylı bir dostluk kuruldu, Boş Koltuk için potansiyel sponsor.
  - **Berrin Voss / Voss ve Ortakları Tefecilik Evi** (Ember Quarter) — doğrulanmamış söylenti: House Sablewood tarafından finanse ediliyor, agresif toprak/borç ele geçirme operasyonu yürütüyor.
  - **Tobin Wrey'in ekibi** (bağımsız kalıntı avcıları, Rovan üzerinden) — bilgi paylaşım ittifakı kuruldu, Kar Vaelth (Sundered Reach) konusunda karşılıklı.
  - **Ashlord Concordat — Sarelle panikledi (gün 176)** — D.V.'nin başlattığı söylentiler işe yaramaya başladı, Emberhold'daki bağlantısı Yorath Sable'a yardım istedi, mektup ele geçirildi (parti elinde).
- **Faction states (Chapter 1'den taşınan):**
  - Ashlord Concordat: hostile — **askere alım kampı katliamını artık keşfetti** (gün 127 civarı, söylenti olarak doğrulandı) — devriyeler artmış, "sanki savaş ilan edilmiş gibi." Halka açık ödül ilanı Karsgate'te Doss'un ağı tarafından temizleniyor. **YENİ (gün 133) — Concordat'ın Harrowgate'teki gizli sabotaj operasyonu (Wyle Sarn, Cadmus Thorn üzerinden) ortaya çıkarıldı** — Councilman Vorn'un suikastı, Thorn ve suikastçı "Kesen" yakalandı. Concordat henüz bunun açığa çıktığını bilmiyor.
  - Ironclad Compact: **GİZLİ İTTİFAK (gün 131-133, session 26)** — Sethra + İlvaneth, Coren Ashvale ile açık savaşı önleyen bir ateşkes kurdu (Deception 25 + dürüst itiraf); Coren, iki gün içinde Harrowgate'e gelip Kriv'le bizzat görüştü (gün 133). Kamuya açık olarak Compact-Concordat "savaşı" devam ediyormuş gibi görünecek, ama gerçekte artık ortak düşman (Sarelle/Concordat) etrafında gizli bir ittifak var — karşılıklı istihbarat paylaşımı, Thorn'un bürosu Kriv'e devredildi (~200-250 gp/ay).
  - **★★ Bölgesel politika — RESMEN İLAN EDİLDİ (gün 134, session 26, Konsey oylaması sonrası).** Kriv, Kaptan Ostrig Vane'e doğrudan emir verdi: Concordat personeli artık Gallowmere, Shestendeliath Hold, ve Harrowgate topraklarına ayak basamaz — bu üç bölge artık resmen "House Shestendeliath toprakları," Concordat için yasaklı bölge. Sadece House Shestendeliath ve Ironclad Compact (gizli ittifak sayesinde) bu topraklarda serbest hareket edebilecek. `travel-encounters.md → The Thornlands` bu politikayı yansıtacak şekilde güncellendi (Concordat artık "rutin tehlike" değil "ihlalci"). **Aynı emirle, üç bölgede de (Gallowmere, Hold, Harrowgate) asker alımı hızlandırılması istendi — Ostrig, Roskel, ve Dallin/Roskel'e (Gallowmere) iletilecek.**
  - Cinder Choir: fractured — Gallowmere hücresi (Fenn) parti tarafından yok edildi, keşif zincirin yukarısına ilerliyor
  - **D.V./Lord Dorian Varn (rakshasa):** artık "fractured" ya da "hostile" değil — **pact_with**, kampanyanın en büyük sırrı, oyunculara açık ama dünyaya hâlâ gizli. Belirsiz, gelecekte tahsil edilecek bir borç var.
  - **The Kindled Circle:** Ilvaneth artık resmi üye, ama Odalys Ferrant'ın tam güveni yok — büyü imzası kayıtlarda eşleşmiş durumda, dikkatli bir gözlem altında.
  - **Karsgate Undertow (Doss/Ninefinger + Iron Sella Dray/Red Tally):** her ikisiyle de ittifak/anlaşma kuruldu, kansız — ~650-700 gp/ay potansiyel gelir (henüz akmıyor, tetikleyiciler bekleniyor).
  - **Harrowgate:** yönetim boşluğu dolduruluyor — Ostrig Vane (Garnizon Evi, 45 adam, şartlı kabul) + Renata Kroll (Tüccar Konseyi, destek sözü, 3 gün içinde toplantı).

## Active Quests
- **★★ TAMAMEN ÇÖZÜLDÜ (gün 133 gece, session 26) — Islak Fıçı hanı, "Sessiz" ve Wyle Sarn ipliği.** Councilman Vorn'un suikastı çözüldü: katil "Kesen" ve Ironclad'ın Harrowgate borç bürosu başı Cadmus Thorn yakalandı (ikisi de baygın, sorgulandı, hücrede). İkisi de itiraf etti — gerçek emir veren **Wyle Sarn** (Concordat adjunct'ı, doğrudan Sarelle'e rapor veriyor), aracı **"Sessiz"** (kukuletalı bir kadın, kimliği artık biliniyor — İlvaneth Dominate Person ile Islak Fıçı'da yakaladı, doğal 1 ile WIS save'i başarısız oldu). **Wyle Sarn'ın kendisi de yakalandı** (Nehrin Dirseği'ndeki tuz deposu, gün 133 gece) — İlvaneth Disguise Self ile Sessiz'i taklit edip içeri girdi, Dominate Person ile ele geçirdi (Dark Devotion avantajına rağmen save başarısız). **Sarn'ın tam itirafı:** (1) Sarelle Duskbourne, İmparator Ashkar Vaelthorn'u bizzat, kasıtlı olarak zehirledi (yavaş, ash-ritual kökenli bir zehir, haftalarca "sadık danışman" rolüyle) — bu artık canlı bir tanıktan doğrulanmış bir gerçek, önceki sadece "kazı erken başladı" şüphesinin çok ötesinde. (2) Sarn, Draven Holt'un işinin bir devamı — Sarelle'in kayıt dışı, kişisel operasyonel eli. (3) Harrowgate'te başka Sarelle ajanı yok, Sarn tek başınaydı bu iş için. (4) Sabit bir buluşma yok — Sarelle'e raporu Karsgate Riverside'da bir kitapçı dükkanının arka odasına ("Vesa"ya adresli) şifreli mektupla gönderecekti. **Depoda bulunan somut kanıt (Investigation 27):** Sarelle'in kendi el yazısıyla bir mektup ("Harrowgate işini temiz tut... Sen dahil" — Sarn'ın da feda edilebilir olduğunu gösteriyor), Thorn/Kesen/Sessiz'e yapılan ödemelerin tam mali kaydı (defter), sahte kimlik + 340 gp + tanımlanmamış bir şişe (Sarn'ın seyahat çantasında). **Halworth ve Maren (Konsey üyeleri) zaten ikna oldu (bkz. Live State Flags) — yarınki oylama (gün 134) canlı itiraflar + Lord Kriv'in tutuklamaları üzerinden destekleniyor.**

**★★★ YENİ (gün 134, session 26) — Sarelle Duskbourne'un hastalığı, artık PARTİ BİLGİSİ (DM-only değil).** Kesen, Sessiz, ve Thorn gün 134'te Harrowgate meydanında idam edildi (Konsey oylaması kazanıldıktan sonra) — Wyle Sarn ve Bram Ostley (ayrı bir yolsuzluk ipliği, bkz. aşağı) hayatta, tutsak, Hold'a götürülüyor. Hold yolunda, ölü bir Concordat kuryesinin (Compact devriyesi tarafından öldürülmüş — bkz. Faction Moves) taşıdığı bir mesaj partiyi **Cinder Hollow**'a yönlendirdi — orada **Warden-Adjunct Mira Kessel** (saha koordinatörü, Half-Orc) yakalandı, Dominate Person ile sorgulandı. **Mira'nın itirafı: Sarelle yıllardır ash-ritual pratiğinin bedeli olan yavaş, tüketici bir hastalıkla boğuşuyor — Concordat'ın üst kademesi bilmiyor, kaç yılı kaldığı belirsiz (1-5 yıl arası tahmin).** Bu, Sarelle'in çaresizliğinin/aceleciliğinin gerçek kaynağı — İmparator'u öldürmesi ve Crown'u tamamlama saplantısı sadece güç için değil, ölümden kaçmak için. **Solenne Kavash** (Sarelle'in ikinci adamı, Tiefling, Grand Archive Karsgate) da bunu sezmiş ama hiç sormamış — potansiyel bir kırılma noktası. Mira ayrıca Sarelle'in zayıf saatini (Restday geceleri, Ashvale'de yalnız) bağımsız bir kaynaktan doğruladı.

- **YENİ, AÇIK (gün 137, session 26) — Solenne Kavash'a "sahte anı" planı, henüz uygulanmadı.** İlvaneth, ileride Modify Memory kullanarak Kavash'ın zihnine Sarelle'in kanıtlarını (mektup, defter, olaylar) "gözünün önünde yaşanmış" gibi yerleştirmeyi planlıyor — Kavash'ın sadakatini kırmak/Sarelle'e karşı çevirmek için. Bunun için önce Kavash'la fiziksel/büyüsel temas kurulması gerekiyor (Modify Memory menzili sınırlı, hedefi görmek/charm etmek şart) — henüz nasıl yapılacağı planlanmadı, gelecek bir Karsgate ziyaretinde değerlendirilebilir.
- **YENİ, UZUN VADELİ PROJE (gün 147'den itibaren, session 26 FF) — Shestendeliath Hold'da kalıcı Teleportation Circle.** İlvaneth gün 147'de başlattı (DMG kuralı: aynı noktada, günde bir kez, 365 gün boyunca castlenmesi gerekiyor). **Orell Tain, İlvaneth'in spellbook'undan Teleportation Circle'ı kopyaladı ve günlük ritüeli devralmaya başladı** — Wizard 9 olduğu için 5. seviye slotu var, günlük castı sürdürebilir. **Sayaç: gün 137 (Hold'a varış) = Day 1.** Şu an gün 181, yani **Day 44/365** tamamlanmış durumda (2026-09-14, session 28 sonu güncellendi — önceki not gün 161/Day 24'te kalmıştı). Bu, arka planda ilerleyen bir proje — her oturum/FF'de gün sayısını güncellemek gerekiyor, 365'e ulaşınca Hold'un kendi kalıcı teleportasyon çemberi tamamlanmış olacak (Karsgate/Emberhold'daki Kindled Circle şubeleriyle eşleşen bir sigil gerekecek, ayrı bir adım).
- **Hold yönetim işleri (gün 137, session 26):** Darphane (House Doskarn kalıp takımıyla) inşaatı zaten Sethra'ya Sending Stone ile emredilmişti (önceki bir sohbette, kayıt dışı) — şimdi yeni gelen iki demirci (Master Rasker'ın oğulları) bu işe katkı sağlayabilir. **Harrowgate atamaları:** Alis Wend → tahsil ofisi (Wenna Tolt'un yerine), Dunnel Ashe → yeni gümrük memuru (Bram Ostley'in yerine, o tutuklandı). **Not: Roskel Gallowmere'de, Hold'da değil** — Hold'un 15 askeri doğrudan Sethra'nın komutasında, ayrı bir kale kahyası yok şu an.

**★ BİLGİ SINIRI (2026-09-12, oyuncu talimatı) — Konsey/Renata dahil kimse şu detayları bilmiyor, asla gösterilmedi/söylenmedi:** Sarelle'in kendi el yazısıyla mektup, mali kayıt defteri, zehir şişesi, ve Sarelle hakkındaki hiçbir özel bilgi (İmparator'u zehirlemesi dahil) — bunların hepsi parti + Coren'in özel bilgisi olarak kalıyor. Konsey'in (Renata dahil) bildiği versiyon sadece şu kadar: **"Concordat burada kirli bir operasyon yürütüyordu, bir Konsey üyesini (Vorn) öldürdü, diğerlerini de (Renlow) öldürecekti. Sarn, Thorn, Kesen, ve 'Sessiz' burada Concordat adına işleri çeviriyordu. Lord Kriv hepsini tutukladı, adaleti sağladı."** Halworth ve Maren canlı itirafları (Thorn'un dinleme odasındaki) duydu — bu kadarı halka/Konsey'e açık. Fiziksel kanıtlar (mektup, defter, zehir) hiçbir zaman gösterilmedi, sadece DM/parti bilgisi.
- **Thorn'un borç bürosu Kriv'e devredildi (gün 133)** — Coren'in onayıyla, kağıt üzerinde hâlâ bir "Compact ortak girişimi" gibi görünecek. ~40 aktif sözleşme, düzgün işletilirse ayda 200-250 gp net gelir. Kriv'in kendi adamlarından birini başına atamayı planlıyor, henüz kimse atanmadı.
- **Harrowgate Konsey oylaması — YARIN (gün 134).** Renata Kroll'un sözü verdiği oylama artık bir gün sonra. Konsey binası + 3 üye evi (Halworth, Maren, Renata) Kriv'in adamlarınca korunuyor, soruşturma süresince.
- **Coren Ashvale ile gizli ittifak (gün 131-133).** Kamuya açık Compact-Concordat çatışması sürüyormuş gibi görünecek, ama gerçek düşman artık ortak. Sarelle'in Ashvale kazısını İmparator'dan önce başlattığı gerçeği Coren'e de açıklandı (tam kanıt değil, sadece doğrulama) — nasıl/ne zaman ortaklaşa kullanılacağı kararlaştırılmadı. Coren, Kriv'in "elf" olduğunu bildiğini ima etti ama kullanmayacağını söyledi (bkz. Live State Flags, Cover).
- **Harrowgate — Shestendeliath'a bağlanma süreci başladı (gün 130/131, session 25 devamı).** Kriv, Kaptan Ostrig Vane (Garnizon Evi, 45 adam, Compact retainer parasına bağımlı — kumar borcu yüzünden) ile görüştü: borcunu kapatma karşılığında, Konsey'in gerçek desteği olursa hanenin altına girmeyi kabul etti. Ardından Renata Kroll (Tüccar Konseyi sözcüsü, session 8'de reddedilen "standing force" teklifinin sahibi) ile görüştü — Persuasion 21 ile ikna oldu, Konseyi 3 gün içinde toplayıp Kriv'i destekleyeceğine söz verdi. **Sethra, 10 asker ile Harrowgate'e ulaştı (gün 131).** Açık kalan: Konsey toplantısının sonucu, Compact'ın olası tepkisi (Ostrig'in parası kesilince), ve Ostrig/Renata'yla konuşmaların gizli tutulması gerekiyor.
- **Draven Holt — TAMAMEN SONUÇLANDI: ÖLDÜ (gün 127/128, session 25 devamı)** — Kestrel Waystation'da bulundu (ölü bir kuryenin üstünde çıkan bir mektupla, Speak with Dead ile doğrulandı). Kriv kimliğini açıkladı, tam itiraf aldı: Holt, House Shestendeliath'a tahıl/erzak müfettişi kılığında sızmış, nöbet düzenini/erzak zamanlamasını bir aracıya iletmiş — kendisi de D.V.'nin (Dorian Varn) gerçek kimliğini bu geceye kadar bilmiyordu, 15 yıldır sadece mühürle talimat alıyordu. Dört evin de kendine ait, birbirini hiç tanımayan birer "Holt"u olduğunu doğruladı. Son bilgisi: Varn'ın yeni emri partiyi (tarif üzerinden) genel olarak gözetlemekti — Varn onları zaten izliyor. Kriv, itiraftan hemen sonra Breath Weapon ile infaz etti (DEX save 19 başarılı, yarı hasar 8, yine de öldürdü). Waystation'ın küçük binası şu an yanıyor, duman fark edilebilir.
- **★★★ D.V. pakt sonuçları — YENİ, AÇIK (gün 124/125, session 25 devamı):** (1) **Kalan 2 Ashen Crown parçasının konumu artık biliniyor** — Ashvale Necropolis'in en derin katmanında, İmparator Ashkar Vaelthorn'un kendi mühürlü lahdinde, Sarelle'in kimseye söylemediği bir yerde. Kimse daha önce İmparator'un lahdini açmayı düşünmemişti. (2) **Sarelle'in zayıf saati:** Restday geceleri, Ashvale'de yalnız kendi "özel" araştırmasını yaparken garnizonu daha az dikkatli. (3) **House Shestendeliath'ın resmi/yasal tanınması söz verildi** — Varn'ın ajanları (Aldous Penmark gibi) üzerinden birkaç ay içinde gerçekleşecek, parti hiçbir şey yapmasa da. (4) **Ascension 3. ve 4. evre bilgisi** artık biliniyor (bkz. `reference/ascension-tracks.md` — Varn'ın anlattıkları mekanikle uyumlu). **Açık soru: parti bunları ne zaman/nasıl kullanacak — Ashvale'e Sarelle'in zayıf saatini bekleyip mi gidecekler, yoksa başka bir öncelik mi var?**
- **Karsgate Undertow ittifakı — ŞART YERİNE GETİRİLDİ, KANSIZ (gün 124, session 25 devamı)** — Doss (Ninefinger) ile The Broken Wheel'de %50 pay anlaşması yapılmıştı (Kriv, Persuasion 18). Kriv doğrudan Uzun Defter'e gidip Sella ile bizzat görüştü (Persuasion 15 — asil/otoriter tavır etkili oldu) — tehditle değil, somut leverage'la (Gallowmere'in ordusu + limanları) ikna etti. **Sonuç: Sella, Ninefinger'a bir daha dokunmamayı kabul etti; karşılığında kendi malı da Gallowmere limanlarından güvenli geçiş kazandı, ayrı bir pay ödeyecek.** Üç taraflı bir denge kuruldu — Doss'un %50'lik payı artık akmaya başlayacak (Doss'a haber ulaşınca), Sella'nın ödemesi ayrı bir gelir kalemi. Kimse ölmedi, hiçbir taraf teslim olmadı — Doss'un istediği tam olarak buydu.
- **Vharkoss — TAMAMEN SONUÇLANDI: ÖLDÜ (gün 106)** — Shestendeliath Hold zindanında, Sethra tarafından, kardeşiyle yeniden buluşup gerçeği öğrendikten hemen sonra, kontrolsüz bir öfke anında, hücre parmaklıkları arasından bıçaklanarak. Kriv bilerek müdahale etmedi, sahneyi tamamen Sethra'ya bıraktı. Kethrax (Vharkoss'un kendi kardeşi) hiç kıpırdamadan izledi, sadakati kanından ağır bastı. Vharkoss'un Sethra'ya yazıp hiç gönderemediği mühürlü mektup hâlâ İlvaneth'te, henüz verilmedi — açık bir an bekliyor. **(Önceki kayıt: ömru boyu hapis, gün 99 — artık geçersiz.)** Kriv ve Ilvaneth, Kingsward'daki konağında görünmez şekilde bastılar, tam itiraf aldılar (bkz. Live State Flags — Draven Holt, dört ev örüntüsü, Sethra'nın masumiyeti). Hold'a getirilip yargılandı, ceza kabul edildi, Ser Kethrax (kardeşi) ve askerleri gardiyan. Açık kalan: Draven Holt ipliği takip edilebilir, Sethra'ya haber verilip verilmeyeceği (Vharkoss'un ona yazdığı ama göndermediği mektup hâlâ ellerinde) açık bir soru. **Karsgate son derece zengin hazırlanmış** (`original-repo/.../info/locations/karsgate.md`) — sahneye girmeden önce bu dosya okunmalı.
- **Draven Holt — el yazısı doğrulandı (gün 112, session 23, Investigation 23)** — Vharkoss'un verdiği mühürlü mektubun el yazısı, Hold'un 15 yıllık tedarik sözleşmesindeki "D. Holt" imzasıyla eşleşti. Holt, evin düşüşünden önceki aylarda Concordat adına **tahıl/erzak müfettişi kılığında en az 3 kez Hold'a girip çıkmış** — nöbet düzenini, erzak zamanlamasını öğrenecek erişimi olmuş. Konumu hâlâ bilinmiyor ama artık soyut bir isim değil. **Kriv kişisel olarak Holt'u bulmayı üstlendi** — Sethra Hold'u güçlendirmeye devam edecek, yeni asker alımlarını bizzat (geçmiş/tanıdıkları sorgulayarak) denetleyecek.
- **House Ostrel — ZİYARET EDİLDİ (gün 118, session 24)** — malikanede Ilyra Thorne ile gerçek bir görüşme yapıldı. Öğrenilenler: (1) Ev düştüğü gece ailenin tamamı öldü — ebeveynler + bir oğlan yanarak, anne + kız (**Wynne Ostrel**, portredeki yazıdan çözüldü, Investigation 24) farklı, belirsiz bir şekilde. Ilyra, Wynne'in gerçekten o gece öldüğünden EMİN DEĞİL — kimse cesedini görmedi, sadece varsayıldı. **Yeni açık iplik: Wynne Ostrel hayatta olabilir**, tıpkı Kriv'in kendi hikayesi gibi. (2) Ilyra on yıldır "gerçekten ölüp bilerek geri dönen" birini arıyor — Kriv'in kendi hikayesini (evi kanıyla yeniden ayağa kaldırması) duyunca gerçek bir ilgi/yoğunluk gösterdi. (3) Ilyra'nın planı: bu kişiyi bulduğunda "bekleyenlere" götürüp tahtın gerçek sahibi olarak GÖSTERECEK, iddia etmeyecek — sahte iddiaları geçersiz kılacak. **DM-only: bu doğrudan Cinder Choir doktrini, Ilyra = Hollow Prophet, oyunculara hâlâ açıklanmadı.** (4) Evde açıklanmamış fenomenler: hiç ısınmayan bir çocuk odası (kapalı), gece merdivenlerden inen görünmez bir ağırlık sesi.
- **House Velkarune — KONUM BULUNDU (gün 113, session 24, Harrowgate arşivi, Investigation 25)** — Karsgate'in Kingsward semtinde bir konakları varmış. "Hat, çocuksuz kapandı" (Tain'in bulgusuyla örtüşüyor) — son varis evlenmemiş bir kadınmış, adı kayıtlarda bile geçmiyor. Henüz ziyaret edilmedi.
- **Dört ev artık tam, oyunculara açık, VE üçünün konumu biliniyor: Shestendeliath (Hold), Doskarn (Karsgate Undercity/Debased Mint), Ostrel (Cindermoor), Velkarune (Karsgate Kingsward). Sadece dördünün de gerçek kaderi/fragman durumu tam bilinmiyor.**
- **Draven Holt — Grand Archive'da resmi dosyası bulundu (gün 122, session 24, Karsgate).** Kriv "miras anlaşmazlığı" örtüsüyle sordu. Dosya anormal derecede ince: sadece atama (1170 AR, Thornlands doğu — Shestendeliath Hold çevresi dahil) ve ayrılış (1172 AR, "kişisel sebepler") tarihleri var, hiçbir performans/amiri kaydı yok. Köşede silinmemiş bir not: **"Doğrudan D.V.'ye rapor eder — arşive işlemeyin."** Katip "D.V."yi tanımıyor. **Yeni açık iplik: D.V. kim?** — Draven Holt'un gerçek üstü, muhtemelen Sarelle'e giden zincirde bir halka daha.
- **Yazman Aldous Penmark — İTİRAF ALINDI (gün 113, session 24)** — dört evin mülk devir yazılarını AYNI kişi (Penmark) imzalamış, Harrowgate Magistralık Ofisi'nden. Kriv tek başına yüzleşti, Intimidation 24 ile tam çöktü. Öğrenilenler: (1) Dördü de on beş yıl önce, aynı ay, kukuletalı kimliği belirsiz bir kurye tarafından getirilen emirlerle hızlandırılmış — Penmark hiç isim/yüz görmedi, sadece talimat+para aldı. (2) **Kurye mührü — kitap + çift anahtar motifi — Penmark'ın elindeki mum örneğiyle doğrulandı, ve bu ARTIK ÜÇÜNCÜ karşılaşma**: aynı motif Vharkoss'un Sethra'ya yazıp hiç gönderemediği mektupta (hâlâ Ilvaneth'te) VE bugünkü Harrowgate ödül ilanında da var. Üçü de aynı tek ofise/otoriteye bağlanıyor — kimliği hâlâ doğrulanmadı ama artık tesadüf değil. (3) Penmark mühür örneğini partiye verdi. (4) **House Ostrel'in malikanesi 10 yıl önce özel bir alıcıya satılmış: Ilyra Thorne** — tek seferde nakit, pazarlıksız, hiçbir kişisel bilgi (meslek/aile) kayıtlı değil, yalnız geldi. Hâlâ orada oturuyor olabilir. (5) House Velkarune'un Kingsward konağı hiç satılmadı, hâlâ Concordat mütevelli heyeti adına duruyor, bakımı ödeniyor, kapalı — muhtemelen içindekiler dokunulmamış. Penmark artık canlı bir tanık, tehdit altında hissediyor, partiye minnettar/korkulu bir ilişkiyle ayrıldı.
- **Tain'in gizli defteri alındı (gün 96 akşamı, Grey Hall'dan)** — yıllardır tutulan kişisel notlar. İlk bulgu: House Shestendeliath'ın "mahkumiyeti" tek vaka değil — dördü de aynı ay onaylanmış, aynı imza zinciri, itiraz penceresi hep kapalı. Diğer üç ev henüz isimlendirilmedi, defterin geri kalanı henüz tam okunmadı.
- **Ashvale Necropolis — HENÜZ HİÇ GİDİLMEDİ (2026-09-10'da netleşti — önceki bir taslakta "tamamlandı" yazılmıştı, bu YANLIŞTI, geri alındı).** Parti bilinçli olarak gitmeyi erteliyor — lokasyon seviye 8-10 için tasarlanmış ama Sarelle artık çok daha güçlü/tehlikeli bir versiyonuyla yeniden tasarlandı (Lawful Evil, kendi ölümsüzlüğü için parçaları istiyor, gerçek bir final-boss — bkz. `## DM Notes`, 2026-09-10 büyük revizyon). Parti önce gerçek bir bölgesel güç haline gelmeli (bkz. 10-12 maddelik öncelik listesi + ekonomik hedef tablosu) — ancak o zaman Sarelle'le gerçek bir yüzleşmeye hazır olacaklar. Tain'in Shestendeliath dosyası sözü hâlâ açık, henüz talep edilmedi. **Parti şu an 5 Crown parçası taşıyor** (Ashvale'in 2 parçası henüz alınmadı).
- **Karsgate Undercity keşfi** (açık, aktif — session 20) — The Sump'tan girildi. Ziyaret edilenler: Drowned Concourse (ash-kral heykeli, gray ooze öldürüldü), First Wall, Otyugh's Midden (otyugh öldürüldü), Gray Cistern (eski kaçakçılık kilit kutusu bulundu), Kingsward Geçidi (DOĞRULANDI — House Varn'ın özel bahçesine açılıyor). Vault of the Nameless hâlâ ziyaret edilmedi (ikinci Ash-Warden evinin kimliği orada).
- **The Debased Mint — TAMAMLANDI (session 21).** Tüm 18 oda temizlendi/keşfedildi. Boss (Oda 18, Baron Halvern Doskarn, Wraith, HP220+Legendary Resistance 2 — özel ayarlandı, bkz. Live State Flags) yenildi, **4. Ashen Crown parçası alındı**. Toplam yağma: ~2600 gp nakit + ~1000 gp ham kül-metal + kalıp takımı + 12 mücevher + Elara Doskarn'ın madalyonu + mint'in gizli müşteri defteri (Corvin Thale'in büyükbabasına ait eski bir kayıt içeriyor) + **House Doskarn Mührü** (nadir yüzük, +1 AC, günde 1 Death Ward — kime takılacağı henüz kararlaştırılmadı). Kalıntı: sikkeler/kül-metal henüz kişisel olarak bölünmedi (BoH'ta toplu).
- **House Varn'ın gizemi** (açık, YENİ — session 20) — Kingsward Geçidi'nin çıktığı bahçede, alışılmadık derecede korunan bir yan kapı (3-4 muhafız). Gece geç saatte kukuletalı, kimliği belirsiz bir ziyaretçi içeri alındı, ardından evin derinliklerinden tuhaf bir müzik duyuldu. Ilvaneth muhafızın anahtarlığını çaldı (fark edilmedi) — kapının anahtarı elde ama henüz denenmedi. **★★★ DM-ONLY (2026-09-10 eklendi, ASLA İFŞA ETME):** House Varn'ın "patriği" Lord Dorian Varn, gerçekte hiç var olmamış — tamamen kurgulanmış bir kimlik, gerçek doğası bir **rakshasa**. Bu, kampanyanın en büyük sırrı: **D.V.** — Draven Holt'un ve muhtemelen Sarelle'in bile gerçek üstü, dört Ash-Warden hanesinin yıkımının ve İmparator'un ölümünün arkasındaki gizli el. Bkz. `npcs-full.md`, "Lord Dorian Varn" entry.
- **Tain'i Hold'a getirme emri verildi (gün 107, Barrow'a çıkmadan önce)** — Kriv, Thornwick'teki Sister Mave'in türbesinden Tain'i alıp güvenle Hold'a getirmeleri için 2 asker gönderdi. Yolda birkaç gün sürecek, sonuç henüz bilinmiyor.
- **Orell Tain kurtarıldı, Thornwick'e gönderildi (session 21 devamı, gün 96 akşamı).** Sarelle'in sorgusu altındaydı, Archive'a nakli sırasında (Riverside gümrük binası yan sokağı) parti + Sefwyn tarafından pusuya düşürülüp kurtarıldı — 2 muhafız + 1 sürücü öldürüldü, cesetler nehre atıldı. Tain artık Concordat'a geri dönemez, tam bir fugitive. Sefwyn ile birlikte Thornwick'e, Sister Mave'in türbesine gönderildi — Ilvaneth Nondetection uyguladı (8 saat). Kriv, Sarelle öldüğünde Tain'in Concordat'ta farklı bir pozisyona geçebileceğini ima etti; Tain açıkça onaylamadı ama karşı da çıkmadı ("seni durdurmayacağım"). House Shestendeliath dosyası artık moot (Tain'in Archive erişimi yok) ama kendi gizli defterini verdi — dört Ash-Warden evinin mahkumiyetinin aynı örüntüyle (aynı ay, aynı imza zinciri, itiraz penceresi kapalı) onaylandığını gösteriyor, üç ev henüz isimlendirilmedi.
- **İsimsiz Concordat arşivcisi Ilvaneth'in yüzünü hatırlıyor** (Wagered Crown, session 20) — henüz "elf+dragonborn" tarifiyle bağlantı kurmadı, ama Kriv'le birlikte görülürse risk. **Adı artık biliniyor: Talyn Ambrose** (session 21 devamı, Sefwyn üzerinden) — orta kademe saha ajanı, sivil kıyafetli, son bir ayda rıhtımda iki kez bir Ironclad Compact kuryesiyle görüşmüş. Parti isterse şüpheyi ona yönlendirebilir (gerçek zaman ister, bir gecelik iş değil) — kanıt yok, sadece yer/zaman bilgisi var, gerisini parti inşa etmeli.
- **Sarelle'in kayıp eskortu — yeni açık tehdit (gün 96 akşamı)** — Tain'i Archive'a taşıyan 2 muhafız + 1 sürücü öldürüldü, cesetler nehre atıldı, Tain kayıp. Concordat er ya da geç fark edecek; ne zaman ve nasıl keşfedileceği belirsiz, ama bu artık aktif bir saat — parti/Sefwyn/Tain'in izini sürebilecek yeni bir soruşturma başlatabilir.
- **Corvin Thale'e borçlu ziyaret** (açık) — Drowned Cathedral'ın törensel dövme aletleri.
- **Gallowmere Yeniden Yapılanma Planı — açık, aktif (gün 104, session 22)**: Lonca liderleri toplantısında kurulan somut plan. (1) **İşgücü:** mülteci kampından 15 zanaatkâr (6 ağ örücü, 4 dülger, 3 demirci, 2 genel) Corwin Dale'in rıhtım ekibine katılıyor. Kalan 20 zanaatsız yetişkin de eşleştirildi (gün 104): 8'i Harn Ostwyck'e (üretim artışı için), 6'sı Sella Marrow'a (ambar/konvoy işleri), 6'sı doğrudan dokka yerleştirildi, Harn'ın tayfaları + Corwin'in adamlarından denizcilik/yükleme öğreniyorlar (Kriv'in emriyle, gün 104 — "boşta adam kalmasın"). Kamptaki tüm çalışabilir yetişkinler artık bir işe yerleşmiş durumda, kimse boşta değil. (2) **Askeri eğitim / garnizon dağılımı netleşti (gün 104):** Hold'daki 27 askerden **12'si + Dallin Marsh** Gallowmere'e getirildi (bu sefer için) — **Hold'da geriye 15 asker + Roskel** kaldı (+ Ser Kethrax'ın ayrı ölü-doğa garnizonu, değişmedi). Gallowmere'de bu 12+Dallin çekirdeğe ek olarak: kamptan **12 asker-yaşında genç (16-25)** Dallin'in adamlarınca Gallowmere'de eğitiliyor (bazıları konvoy eskortu olarak pratik yapacak); **8 çocuk (10-15)** arasından subay eğitimine yetenekli olanlar seçilip **Hold'a gönderilecek, Roskel tarafından bizzat eğitilecek** — ayrı, daha üst düzey bir yetiştirme hattı. (3) **Ticaret hattı:** Harn Ostwyck (balıkçılar) için düzenli konvoy — ilk ay haftada 2 sefer (Harrowgate + Thornwick), sonra haftada 1. Sella Marrow'un 3 dolu ambarı (~90-100 yük arabası birikmiş mal) bu konvoyla eritilecek. Genç askerler eskort eğitimi alacak, en az 3 deneyimli asker eşlik edecek. (4) **Kaçakçılık resmen yasal ilan edildi** Kriv'in hükmünde — Sella'nın "resmi olmayan ama gerçek" rotaları artık vergilendirilip meşrulaştırılabilir. (5) **Başlangıç yatırımı, gün 104:** Kriv, kendi kesesinden 180 gp dağıttı (Corwin 50, Harn 30, Sella 100) — kurulum masrafları için, karşılıksız/ilk-adım niyetiyle. (6) **Vergi oranı belirlendi:** İlk yıl %35 (kalkınma, inşa, konvoy sıklığı, asker eğitimi için), sonraki yıllardan itibaren sadece %20 Lord payı. Dört lider de kabul etti. Henüz hiçbir iş fiilen başlamadı — hepsi "yarından itibaren" planlandı.
- **Ordu büyütme girişimi — YENİ (gün 110, session 23)**: Kriv iki koldan asker toplama emri verdi. (1) Sethra'ya Sending Stone ile: Hold'dan atlılar çıkarıp Ironclad'dan ayrılanlar dahil güvenilir paralı asker toplasın. (2) Roskel'e Gallowmere'de: kampın çalışan yetişkinlerine dokunmadan üç kaynaktan yeni adam — yol geçen serbest kılıçlar (ilan/gerçek maaş), henüz seçilmemiş kasaba gençleri, ve sessizce yaklaşılacak hoşnutsuz Ironclad askerleri. Roskel bir hafta içinde gerçek bir sayı getirmeyi taahhüt etti. **Hold tarafı (Sethra raporu, gün 112):** Sending Stone emri gün 109'da ulaştı, aynı gün atlılar çıktı. Şimdiden 4 kişi geldi (2'si eski Ironclad, hâlâ güven inşa ediyorlar), yarın 2 kişi daha bekleniyor. Sethra kendisi Hold'un 15 askerini eğitiyor, 3'ü gerçekten yetenekli. **Draven Holt ipucu:** Hold'un 15 yıllık kayıtlarında imzasız ama okunaklı bir "D. Holt" el yazısı bulundu (bir tedarik sözleşmesinde) — karşılaştırma için gerçek bir örnek gerekiyor, ama gerçek bir başlangıç.

**YENİ EMİR (gün 125, session 25 devamı, Sending Stone ile Sethra'ya):** Kriv, asker alımının hızlandırılmasını emretti — Sethra bugün Roskel/Dallin'e haber uçuracak, mevcut alım hızı iki katına çıkacak. Sebep söylenmedi ("zaman geldi" diye bırakıldı) — Sarelle/Ashvale'e hazırlık, henüz Sethra'ya açıklanmadı.

**Garnizon güncel durumu (Roskel/Dallin raporu, gün 110):** 12 tecrübeli asker (Dallin), 12 çırak genç (6 gündür eğitimde, nöbet/devriyeye hazır ama meydan muharebesine değil), 8 çocuk subay adayı (Roskel'in kişisel gözetiminde, en umutlusu "Mira" adlı bir kız) — toplam 32. **Dallin Marsh Teğmen'e terfi etti** (gün 110) — Kriv'in emriyle bizzat eğitimlere katılacak, formda kalacak.

**Gallowmere Hazinesi — ayrı bütçe hattı (gün 104'te kuruldu):**
Hold'un bütçesinden tamamen bağımsız, kendi kendini finanse eden bir sistem. İki ayrı kese var: Hold masrafları Kriv'in kişisel kesesinden karşılanır (değişmedi); Gallowmere'in masrafları artık kendi vergi gelirinden karşılanır, Kriv'e sadece net kâr gider.

| Kalem | Aylık |
|---|---|
| Tahmini brüt gelir (yerleşik dönem, %35) | ~400-500 gp |
| Garnizon maaşı (12 yeni asker) | -24 gp |
| İnşaat malzemesi (mülteci konutları) | -25 gp |
| Konvoy işletme masrafı | -15 gp |
| Fennick Orle'nin sabit ödemesi (bilgi kaynağı anlaşması) | -15 gp |
| **Net kâr → Kriv'e** | **~325-420 gp/ay** |

*İlk ay (backlog eritme, haftada 2 sefer): daha yüksek brüt (~600-800 gp), aynı masraf tabanı — daha yüksek net.*
*2. yıldan itibaren: oran %20'ye düşer, ama hacim büyümüş olacağı için mutlak net muhtemelen benzer/daha yüksek kalır.*

Henüz fiilen gelir akmadı — ilk konvoy "yarından itibaren" yola çıkacak, ilk gerçek ödeme bir sonraki kontrol noktasında (~1 hafta) beklenir. Kimin defter tuttuğu henüz atanmadı (**Sella Marrow** aday olabilir — Gallowmere'in ambarcılar birliği lideri, çıkar çatışması riski var, DM notu, oyunda organik olarak çözülmeli).

**Karsgate Undertow Geliri — ayrı bütçe hattı (gün 123-124, session 25 devamı kuruldu):**
Gallowmere Hazinesi'nden tamamen ayrı, Karsgate'teki iki yeni anlaşmadan geliyor. ⚠ **İsim karışıklığı notu: bu "Sella", Gallowmere'in ambarcı lideri Sella Marrow DEĞİL — "Iron" Sella Dray, Karsgate/Warrens'taki Red Tally çete lideri. İkisi hiç tanışmadı, alakasız kişiler, sadece isim tesadüfü.**

| Kalem | Aylık | Durum |
|---|---|---|
| Doss/Ninefinger %50 pay | **~350-400 gp** | **AKTİF (gün 154 itibarıyla doğrulandı, session 26 FF)** — 17+ gün geçti, haber Doss'a ulaştı, ödeme akıyor |
| Iron Sella Dray / Red Tally geçiş ücreti | **~300 gp** | **AKTİF (gün 154 itibarıyla doğrulandı)** — ilk konvoy geçti, ödeme akıyor |
| **TOPLAM** | **~650-700 gp/ay** | Kriv'e gidiyor, Gallowmere Hazinesi'nden ayrı tutuluyor |

---

## ★★ Konsolide Hazine Tablosu (gün 154'te oluşturuldu, session 26 FF — aylık, 45 günlük ay bazında)

| Kalem | Aylık (gp) |
|---|---|
| Gallowmere Hazinesi (net) | +325 ila +420 |
| Thorn'un eski borç bürosu (Harrowgate) | +200 ila +250 |
| Karsgate Undertow (Doss + Sella Dray) | +650 ila +700 |
| **YENİ — Harrowgate Lord payı (%10, "tam koruma" gerekçesiyle)** | **+800 ila +1.200** |
| **Toplam gelir** | **~1.975 ila 2.570 gp/ay** |
| **YENİ — Teleportation Circle malzemesi (50 gp/gün × 45 gün, 348 gün daha sürecek)** | **-2.250 gp/ay** |
| **Net** | **~-275 ila +320 gp/ay** (neredeyse dengede) |

*Harrowgate %10 Lord payı, kasabanın toplam ekonomik hacminin ~8.000-12.000 gp/ay civarında olduğu varsayımına dayanıyor (4.000 kişilik gerçek pazar kasabası) — doğrudan vergi değil, tam koruma/himaye karşılığı bir tribute, Renata'nın Tüccar Konseyi üzerinden toplanıp gönderilecek.*

**Güncellenmiş tablo (gün 154, ek gelir kapıları eklendi):**

| Kalem | Aylık (gp) |
|---|---|
| Gallowmere Hazinesi | +325 ila +420 |
| Thorn'un eski borç bürosu | +200 ila +250 |
| Karsgate Undertow | +650 ila +700 |
| Harrowgate Lord payı (%10) | +800 ila +1.200 |
| **YENİ — Darphane** (House Doskarn kalıp takımı + 2 yeni demirci) | **+150 ila +250** |
| **YENİ — Greyholt** (Hallik'in bağlılığı, gün ~145'te resmileşti) | **+80 ila +120** |
| **YENİ — Ashlord Concordat (Tain, gün 195'ten itibaren)** — 400 gp/ay başlangıç, Tain'in kontrolü sağlamlaşınca (birkaç hafta) 1.500-2.000 gp/ay'a çıkacak | **+400 (yakında 1.500-2.000)** |
| **Toplam gelir** | **~2.605 ila 3.340 gp/ay** (Concordat tam oturunca ~3.700-4.940 gp/ay'a çıkar) |
| Teleportation Circle malzemesi (50 gp/gün × 45 gün, 348 gün daha sürecek) | **-2.250 gp/ay** |
| **Net** | **~-45 ila +690 gp/ay** |

### Hold Hazinesi (Treasury) — ayrı, kalıcı bir kasa, gün 154'te kuruldu
Kriv'in kişisel kesesinden bağımsız. **★ Netleştirme (gün 196, session 34): SADECE `## ★★ Konsolide Hazine Tablosu`'ndaki pasif/aylık gelir kalemleri (lordluk payları, Darphane, Karsgate Undertow, Thorn'un borç bürosu, Concordat'ın Tain ödemesi, vb.) buraya akar — vadesi geldiği gün otomatik işlenir, ayrı hatırlatmaya gerek kalmadan. Dungeon/combat loot'u bu kuralın DIŞINDA — her zaman PC'lere (Kriv/İlvaneth) yazılır, genelde 50/50.** Teleportation Circle'ın günlük malzeme masrafı buradan karşılanıyor.

| | gp |
|---|---|
| Kurucu yatırım (Kriv, gün 154) | +500 |
| İlk hafta net geliri (gün 154-161, ~7/45 ay) | +50 |
| Hold garnizon maaşı (18-20 asker × 2 gp/ay, ~7/45 ay) | -6 |
| İkinci yatırım (Kriv, gün 161) | +500 |
| **★ Tam geriye dönük hesap (session 34, gün 196'da yeniden yapıldı — önceki parçalı tahmin yerine geçti).** Hazine mekanizması gün 154'te kuruldu — ondan önceki gelir (Gallowmere gün 104'ten, Karsgate Undertow gün 122'den, Thorn gün 133'ten, Harrowgate gün 134'ten beri teorik olarak aktifti) resmi kasa olmadığı için Hold'un günlük işleyişine harcanmış sayılıyor, tabloya dahil değil. **Gün 154 → gün 196 = 42 gün (0,933 ay):** Gallowmere (+372,5) + Thorn (+225) + Karsgate Undertow (+675) + Harrowgate Lord payı (+1.000) + Darphane (+200) + Greyholt (+100) = brüt +2.572,5 gp/ay − Teleportation Circle malzemesi (-2.250 gp/ay, gün 137'den beri aktif, ~305 gün kaldı) = **net ~+322,5 gp/ay** → 42 günlük pay ~301 gp. | +301 |
| Kriv'in iki yatırımı (gün 154 + gün 161) | +1.000 |
| Ashlord Concordat, Tain'in ilk aylık ödemesi (gün 195, tek seferlik) | +400 |
| **Güncel bakiye (gün 196 itibarıyla, tam hesaplandı)** | **~1.701 gp** |
| *Not: Ember Quarter ortaklığı (10.000 gp yatırım, gün 182, Sereth Corr ile) hâlâ akmıyor — Darphane/Undertow örneklerindeki gecikme bekleniyor, henüz 14 gün geçti. Teleportation Circle'ın -2.250 gp/ay'lık maliyeti brüt gelirin neredeyse tamamını yiyor — Hazine'nin yavaş büyümesinin gerçek sebebi bu, bir hesap hatası değil.*

*Not: eski 1.000 gp (Roskel'e gün 81'de "household expenses" için verilmiş) bu hazineye dahil değil — resmi hazine yokken zaten Hold'un günlük işleyişine harcanmış kabul ediliyor, ayrı bir tahsisattı.*

### Ordu Büyüme Tablosu (gün 161 itibarıyla, güncel sayılar)
*Her lokasyon farklı tarihte başladı — Gallowmere/Hold gün 110'da (gün 125'te 2x hızlandı), Harrowgate gün 134'te (tek hız, sınırsız bütçe).*

| Lokasyon | Komutan | Başlangıç | Gün 161 toplam |
|---|---|---|---|
| Gallowmere | Dallin Marsh/Roskel | gün 110: 32 | **~48-55** |
| Shestendeliath Hold | Sethra | gün 107/110: 15 | **~25-30** |
| Harrowgate | Kaptan Ostrig Vane | gün 134: 45 | **~54-60** |
| **TOPLAM** | | 92 | **~127-145** |

*Aylık alım oranları: Gallowmere/Hold gün 125'ten beri 2x hızda (+16-24 ve +10-16/ay); Harrowgate tek hızda (+15-25/ay). Bir sonraki kontrol noktasında bu tabloyu güncelle — geçen gün sayısı × ilgili oran.*

*Bundan sonra her `/dm:dnd save`'de ya da büyük bir zaman atlamasında, geçen süreye göre net gelir/gider bu bakiyeye işlenmeli — aylık ortalama net (~-45 ila +690 gp) × geçen ay sayısı.*
- **Ash-Kilns ve Drask'ın rıhtım bölgesi** — sahipsiz güç üssü fırsatları.
- **Kell'in rüşvet defteri** — gerçek, kullanılmamış kaldıraç.
- **Greyholt — İLK TEMAS, GERÇEK BİR ÇATLAK AÇILDI (gün 112, session 24).** Kriv, Ilvaneth ve Sethra üçü birlikte gittiler. İlk iki Persuasion denemesi (13, 12) başarısız oldu — Kriv'in gururlu "açıklamak zorunda mıyım" tavrı köylülerin korkusunu haklı çıkardı, neredeyse boş elle döneceklerdi. Son anda Kriv köy ihtiyarı **Hallik**'e (büyükbabası bu toprakları işlemiş eski bir tenant ailesinden) dürüst bir çerçeve sundu — "hanemiz içeriden bir hainin yardımıyla yok edildi, siz de kendi köyünüzde sıkışıp kaldınız, artık böyle olmak zorunda değil" — zorlamadan, sadece davet ederek. Üçüncü Persuasion denemesi (20) gerçekten geçti. Hallik silahını indirdi, birkaç gün içinde (hasat kaldırıldıktan sonra) **yalnız başına Hold'a gelip kendi gözleriyle görmeyi** vaat etti. Henüz bir anlaşma değil — sadece gerçek bir başlangıç, Hallik'in kişisel sözü. Sethra: "İşte bu bir başlangıç."
- **Ilvaneth'in "rüyalar" listesi** — Ascension bedeli, 2 girdi, büyümesi bekleniyor.
- **The Unquiet Barrow — TAMAMLANDI (gün 107).** Elder Xorn (gerçek koruyucu) yenildi, Sethra'nın yardımıyla. Oda 18'in merkezindeki ödül erişilebilir, henüz alınmadı/tanımlanmadı.
- **"The Measure of Ash" — BULUNDU (gün 117, session 24)** — Cindermoor'un güneyinde, çökmüş bir kaya sığınağı altında (Investigation 28, Kriv'in yardımıyla). Yanında, kaçan bir rahibin çürümüş cübbesi + bir günlük parçası: *"Taç bir insanı taşıyamaz demiştim, kimse dinlemedi... Ölçüyü aldım, saklıyorum, bulamazlarsa töreni tamamlayamazlar."* Rahip muhtemelen buraya kaçtıktan sonra tek başına öldü, alet hiç bulunmadı — artık Kriv'de. Drowned Cathedral'ın orijinal dövme törenine ait gerçek bir parça; Corvin Thale'e hâlâ borçlu bir ziyaret var (Reliquary'nin diğer aletleri için).
- **Ilvaneth'in Ring of Free Action'ı** — takılı değil (3 slot da dolu), gerçek bir ekipman kararı bekliyor.
- **Sending Scroll siparişi (gün 113, session 24, The Ashgate Conservatory, Yveth Corrane)** — özel sipariş, ~1 hafta sürer, ~gün 120'de hazır olması bekleniyor. Alışveriş: Revivify elması, 2x Legend Lore takımı, gümüş tozu (Cole'dan, 1000 gp), Scroll of Fly, Scroll of Counterspell, boş spellbook, Sending Scroll siparişi (Yveth'ten, 650 gp toplam). Ilvaneth'in altını: 1251 gp.

## Open Threads & Rumours
- **★★★★★★★ YENİ, AKTİF (gün 203, session 35) — Parti, Kesh Amara'nın Teleportation Circle'ından "The Ember Court"a (Kaal hanesinin sınır düzlemi) geçti.** Tam tasarım `reference/ember-court.md`'de — 24 oda, seviye 17-18. **Asıl hedef: Iskra Vantrel ve Sathriel'in Oda 24'teki "Kor Beşiği"nde reform olan, hâlâ savunmasız özlerini birkaç saat içinde kalıcı olarak yok etmek** (yoksa tam geri dönerler). Rakshasa Rajah + Pit Fiend havuzu koruyor. **Parti şu an Oda 1'de (Varış Odası), 2 rakshasa muhafızla karşı karşıya, henüz savaş başlamadı.**
- **★★★★★★★ YENİ, BÜYÜK, AÇIK (gün 202/203, session 35) — Iskra öldü ama Kaal hanesi hâlâ var, DM-only bir uyarıyla ("Kaal asla gerçekten ölmez").** Parti elinde: Kaal'ın kendi düzlemine açılan bir Teleportation Circle sigili (kopyalandı, Ilvaneth kendi Teleportation Circle büyüsüyle bağlanabilir), üç şehrin (Karsgate/Harrowgate/Emberhold) tam borç kayıtları, kırık bir Sözleşme Taşı (teorik olarak bir Kaal sözleşmesini bozabilir — Cassian'ın kendi "bilinçsiz taraf" statüsü üzerinde denenebilir). Henüz kimse (Cassian dahil) İskra'nın öldüğünü bilmiyor. Kaal hanesinin geri kalanının bu kaybı nasıl/ne zaman fark edeceği, kimin yeni "Emberhold sorumlusu" olacağı — hiçbiri sahnede değil.
- **★★★★★ YENİ, AÇIK (gün 202/203, session 35) — Maro Veskin, Kaal'a "bilgi karşılığı sessizlik" sözleşmesiyle sekiz yıldır bilerek bağlı (Emberhold borç kaydında bulundu) — kendi kâtibi Ostwin Kade da Kesh Amara'da öldü, henüz Veskin'in haberi yok.** Bu, Veskin'e karşı gerçek bir kaldıraç — hem sözleşmesinin kanıtı hem kâtibinin kaybı, ikisi de parti elinde/bilgisinde.
- **★★★★★ YENİ, AÇIK (gün 202, session 35) — "Kesh Amara" ipliği: Iskra'nın (Kaal hanesinin) sözleşme evi bulundu.** D.V.'nin yönlendirmesiyle Elian Rook'a ulaşıldı (artık açık müttefik) — defterinde "Kesh Amara" adı, hep **Cinderday** gecelerine denk gelen üç kayıt olarak geçiyordu. Kriv (Chancellery mülk kayıtları) + İlvaneth (Grand Spire arşivi, Infernal sözlük — "Kesh Amara" = "Ödenmemiş Ev/Sessiz Borç," eski fiend-pact sözleşme yeri tabiri) çapraz doğruladı: **Kingsward Dış Mahalle, 14 numaralı malikane** — dışarıdan sıradan/terk edilmiş görünüyor ama gerçekte hem mundane bir devriye (işçi kılığında) hem de duvara işlenmiş, neredeyse görünmez Abjuration ward'ları (muhtemelen scrying/teleport'a karşı) ile korunuyor. **Parti, tam karşısındaki boş bir şehir evini 1 aylığına kiraladı (15 gp, İlvaneth ödedi)** — gözlem noktası olarak. Bir sonraki Cinderday: **37 Ashfall** — ertesi gece. D.V. de kendi türünden ayrıca soruşturma yapıyor, Sending ile haber verecek.
- **★★★ YENİ, AÇIK (gün 202, session 35) — D.V. (Lord Dorian Varn), Sarelle'in ölümünü ve House Shestendeliath'ın Hollow Throne zaferini zaten kendi kaynaklarından duymuştu** — parti bunu ona anlatmadı, o zaten biliyordu (Karsgate merkezli geniş istihbarat ağı). Iskra Vantrel'in "Kaal'ın kızı" olduğu bilgisini parti verdi, karşılığında değerli bir koz kazandı; ekstra bedel istemedi.
- **★★★ YENİ, AÇIK (gün 202, session 35) — Kaal, rakshasa'ların eski/acımasız bir hanesi/klanı — D.V.'nin doğrulaması + İlvaneth'in Legend Lore'u.** "Kaal'ın kanı hizmet etmez, sadece kiralanır" — Iskra'nın (ve muhtemelen başkalarının) bu haneye bir tür sözleşmeyle bağlı olduğunu gösteriyor. Sözleşmeler onları er ya da geç bu düzleme geri çekiyor. Henüz konumu/gücü/diğer üyeleri bilinmiyor.
- **★★★ YENİ, AÇIK, ARTIK MOOT DEĞİL (gün 198, session 35) — Üç hanenin (Corr/Sablewood/Ilvane) şahsi sırlarını içeren 3 dosya parti elinde**, kullanılmadı henüz — Sereth'in kuzen zehirlemesi, Berengar'ın iflas raporu, Cassian'ın hanesindeki evlilik-dışı çocuk kaydı. Cassian'ın dosyası ondan saklanıyor, ittifak buna rağmen kuruldu ama kırılgan bir zeminde.
- **★★★ YENİ, AÇIK (gün 198, session 35) — Sereth Corr ile ilişki artık "borç ödeşmesi," sıcaklık yok, kalıcı bir gerginlik var.** Kriv, Dorren Corr'un ölümünü/Sereth'in evlatlık oluşunu bir kaldıraç olarak kullandı — Sereth destek verdi ama "bunu unutmayacağım" dedi, açık bir gelecek gerilim kaynağı.
- **★★★ YENİ, AÇIK (gün 198, session 35) — Sonnward Promenade konağının bahçesindeki 30 yıllık boş malikane hâlâ araştırılmadı** (Vell'in "neden bu kadar ucuz bilmiyorum" dediği mülk, gün 182) — Kesh Amara heyecanıyla unutulan eski bir iplik.
- **★★★ YENİ, AÇIK, SAAT İŞLİYOR (gün 184, session 30) — Sundered Garden randevusu ÇÖZÜLDÜ, ama yeni bir tehdit doğdu.** Buluşmaya gelen Sarelle değildi — **Reyna Sorrel**, gün 167'de Kriv'in mesajını taşıyan Concordat kuryesi (Half-Elf, otuzlu yaşlar). Sarelle'e hiç iletmemiş cevabı kendi yazmış — Concordat'ın içindeki artan paranoyadan (Sarn/Kesen/Thorn/Mira Kessel'in art arda kaybolması) korkup kaçmak istiyordu, karşılığında bilgi sunup sığınma istedi. **Verdiği somut bilgi (öldürülmeden önce):** (1) Sarelle neredeyse hiç Ashvale'deki özel odalarından çıkmıyor, hastalık ilerliyor, paranoyakça iki orta kademe arşivciyi yargısız infaz ettirdi. (2) **Ashvale Necropolis'in dış garnizonu Restday geceleri yarı personelli** — Sarelle'in "özel araştırması" için düzenli olarak boşaltılıyor, gerçek bir taktik açık. (3) Solenne Kavash'ın Sarelle'in hastalığından şüphelendiği (henüz sormadı/itiraf etmedi) — gelecekte konuşulabilir bir kanal olabilir. (4) **★ En kritik: Sarelle üç gün önce özel bir avcı görevlendirdi, adı Corbin Vayle — eski bir canavar avcısı, "ölü ya da diri" partiyi arıyor, son işi tek başına genç bir ejderha öldürmüş. İki gün önce Karsgate'e doğru yola çıktı — yakında burada olabilir.** Bilgiyi verdikten hemen sonra **Kriv onu Breath Weapon ile infaz etti** (23 hasar, DEX save başarısız) — sorgusuz, "vaktini çaldığı" gerekçesiyle. Ateşin ışığı bahçe duvarlarının üstünden görülmüş olabilir, kim fark etti belirsiz. Coren'in 6 paralı askeri hâlâ Gallow's Rest'te bekliyor, kullanılmadı.
- **★★★ YENİ, AÇIK (gün 182, session 30) — House Ashveil'ın 32 yıl önceki yok oluşu, Whisper Court'un kanıtlı en eski vakası.** Kriv ve İlvaneth, Kingsward'da 120 gp'ye satın aldıkları terk edilmiş bir malikanede (otuz iki yıldır boş, arması kazınmış) eski hizmetçi **Yara**'yı buldular — her ay gizlice mum yakmaya geliyormuş. Yara'nın anlattığı: Lord Garrick Ashveil bir gece "acil konsey işi" için çağrıldı, geri gelmedi; aynı gece tüm ev sessizce "kayboldu," hiç ceset/kan/iz yok, kapılarda **kırık daire mührü** (Dorren Corr/Iskra Vantrel'e işaret eden mühürle aynı). Kriv, Yara'yı evden kovdu (tablolarını almasına izin verip) — Yara giderken mührü hatırlattı ve gitti, geleceği belirsiz. İlvaneth'in aramasında (Investigation 28) gizli bir panelde **Lord Garrick'in günlüğü** bulundu: ölümünden bir gece önce, güvendiği müsteşarı **Denna Sarth**'ın aslında bir doppelganger'la değiştirildiğinden şüphelendiğini yazmış (kaba bir kroki de var — sivri çene, sola eğik kaş, kulak arkasında doğum lekesi). **Sonuç: Whisper Court'un doppelganger yöntemi en az 32 yıldır sürüyor** — Wrenna/Arnholt sadece son örnekler, kalıcı bir kurumsal taktik. Mahzende ayrıca 430 gp değerinde aile hazinesi bulundu (İlvaneth aldı). Ev artık partinin mülkü, bkz. characters/Kriv Shestendeliath.md.
- **YENİ, AÇIK, KISMEN GELİŞTİ (gün 134/137-144, session 26) — Bram Ostley ve Drenmoor Ticaret Evi ipliği.** Ostley (Harrowgate'in eski gümrük katibi) tutuklandı, vergi kaçakçılığı itiraf etti — Drenmoor Ticaret Evi'ne çalışıyordu, ama adını verirken **büyüsel bir engelle karşılaştı iki kez** (Detect Thoughts'a doğal 20 ile direndi, sonra Dominate Person'a da doğal 20 ile — Dark Devotion değil, kendi başına bir şey). **FF sırasında (gün 137-144) İlvaneth tekrar tekrar denedi, sonunda Dominate Person tuttu** (genel sorguya tam boyun eğdi) — ama Drenmoor'a yönelik sorularda **aynı duvar tekrar belirdi, dominasyona rağmen bile bir şey söyleyemedi.** Bu artık şans değil, gerçek bir büyüsel koruma/geas gibi görünüyor — Drenmoor'un kendi ajanlarını nasıl koruduğuna dair ürkütücü bir ipucu. Ostley'den başka öğrenilenler (Drenmoor'a dair olmayanlar): kaçakçılık lojistiği, mal akışı detayları, muhtemelen başka rüşvet alan görevliler — ama Drenmoor'un kendisi hâlâ tam bir gizem. **Ostley infaz edildi (gün 144, session 26, Kriv tarafından)** — artık daha fazla bilgi çıkarılamayacağı netleşince. Drenmoor ipliği hâlâ açık, tek kalan iz Sethra'nın topladığı defter + genel kaçakçılık deseni.
- **YENİ, AÇIK (gün 134, session 26, Harrowgate-Hold yolu, Thornlands) — yarı gömülü tapınak kalıntısı.** Kanopideki bir açıklıktan görülen, kök/toprağa gömülü eski bir taş yapı, patikadan az uzakta, hiçbir haritada işaretli değil. İlvaneth not aldı, ziyaret ertelendi — dönüşte veya başka bir yolculukta incelenebilir.
- **YENİ, AÇIK, SAAT İŞLİYOR (gün 134, session 26, aynı yol, gece kampı) — "Cinder Hollow" buluşma noktası.** Ölü bir Concordat kuryesi bulundu (boğazı kesilmiş, birkaç saatlik), elinde yok edilmemiş bir mesaj: *"Sessizlik uzadı. Cinder Hollow'a gel, üç gün içinde, ya da bulunacaksın."* İmzasız, ama kitap+çift anahtar mührü taşıyor. Wyle Sarn'a soruldu (bkz. Live State Flags) — Concordat saha ajanları için eski, seyrek kullanılan bir acil durum toplanma noktası/güvenli ev olduğunu doğruladı. Sarn'ın sessizliği (tutuklanması) muhtemelen bu sinyali tetikledi. **Üç günlük bir pencere var** — kim/ne gelirse, parti orada bekleyip yakalayabilir ya da görmezden gelip yoluna devam edebilir. Konum tam olarak bilinmiyor, sadece isim biliniyor.
- **ÇÖZÜLDÜ (gün 109/110, session 23, Harrowgate->Gallowmere yolu): "isimsiz levha" ipliğinin kaynağı bulundu.** Levhayı tazeleyen bir kadınla (**Old Sabeth**, bkz. npcs.md) karşılaşıldı. İşaretler **Külsüz Yer**'e gidiyor — yasını tutacak yeri olmayanlar için, güç/taç aranmayan bir sığınak. **Gün 111/112'de ZİYARET EDİLDİ** (Gallowmere-Hold yolu, Sabeth'in taşıyla ikinci bir levha bulundu) — yosun tutmuş taş zeminli küçük bir açıklık, yüzyıllarca birikmiş kişisel eşyalar. Kriv yetimhane çivisini bıraktı (gerçek bir hafifleme hissetti — çivinin gerçek hikayesi hâlâ açık, gelecekte geliştirilebilir). İlvaneth dört Crown parçasına dokundu, ölüm-düşüncesi değil ama "gerçekten görülme" hissi yaşadı. Yer artık bilinen, tekrar ziyaret edilebilir bir konum — Gallowmere-Hold yolunun kuzeybatısında, ağaçların derininde.
- **Toll deserterlerin sinyal borusu** — çözülmedi, gelecekte bir tuzak/yanlış iz olabilir.
- **Vaelthorn crypt ward stone** — dokunulmadı, kriptin iki kez rahatsız edildiğini kimse bilmiyor.
- **Harn'ın ikinci notu** (Weeping Tower) — partinin kendi Crown parçasının onun nekromantik işi için "çıpa" olabileceğini ima ediyor, hiç doğrulanmadı.
- **Hollow Prophet'in okunaksız ismi** ("V ya da Y gibi görünüyor") — kasıtlı olarak çözülmedi (DM biliyor: Ilyra Thorne — **oyunculara açıklama**).
- **Warden's Charge'ın iç bandı** ("kanda uyuyan şey sadece gerçek bir sebep için uyanır") — Kriv'in ejderha kanı sırrının ilk ipucu, kasıtlı çekilmemiş, stale bırakılmamalı.
- **Sahte Karsgate satış belgesi** — hâlâ canlı, ikinci bilmeyen taşıyıcısı Kessra Vane oldu, kimse partiye kadar izini sürmedi.
- **Orman yangını** (gün 111, Gallowmere-Hold yolu, Concordat kampının izlerini örtmek için Kriv'in çıkardığı) — kuru Emberfall havasında beklenenden hızlı yayıldı, gerçek bir yangına dönüştü. Duman sütunu millerce uzaktan görülebilir. Kim çıkardığına dair iz yok ama "burada bir şey oldu" sinyali daha da büyüdü — kimin/neyin tepki vereceği (yerel halk, bir faction, doğal bir tehlike) henüz belirlenmedi.
- **Taze, boş mezar** (gün 110, Harrowgate->Gallowmere yolu, şafak öncesi) — sığ, örtülmemiş, içi boş (hiç doldurulmamış ya da içindekiler alınmış). Ayak izleri kuzeydoğuya, Gallowmere'in tersi yöne gidiyor. Parti takip etmedi, Gallowmere'i önceliklendirdi — iz soğumadan araştırılabilir ama artık gecikiyor. **İlvaneth'in 7. rüyası (gün 111, Gallowmere'de uzun mola) olası bir bağlantı kurdu:** genç bir haberci, peşinde yaya takipçiler, elindeki mektubu yutarak/yok ederek öldü — "bulamazlar" diye düşünerek. Mezarın boş oluşu artık açıklanabilir: birileri sonradan cesedi almış, muhtemelen mektubu aramak için. Kesin bağlantı değil, ama güçlü bir sezgi.
- **Unfinished Circle araştırması — Odalys Ferrant ile karşılıklı bilgi anlaşması (gün 167, session 26 devamı'nda kuruldu, gün 181, session 29'da devam etti — önceden state.md'ye hiç işlenmemişti, bu satır restore).**
  - **Gün 167 kuruluşu:** Odalys, İlvaneth'e Karsgate'in kısıtlı/eksik Unfinished Circle dosyasını verdi (şart: bulduğu her şeyi Odalys'e eksiksiz anlatacak — iki yönlü bir anlaşma). Dosyanın içeriği: bölünmenin sebebi sapkınlık değil **başarısızlıktı** — biri gerçekten bir şey bulmuş/bulduğunu düşünmüş, takipçilerinin çoğu ölmedi, **kayboldu**, Lonca bunu "ahlaki çöküş" diye kayda geçirmeyi tercih etti çünkü gerçek cevabı bilmiyorlardı. Tek gerçek ipucu, bir soruşturmacının el yazısıyla: **"Cael hattı"** hâlâ pratik yapıyor olabilir, son görülüşü 40 yıl önce; gerçek/tam dosya bölünmeden hemen sonra doğrudan Emberhold'un merkez arşivine gönderilmiş ve **"orada kalması emredilmiş"** — kimin emri olduğu yazmıyor. Odalys aynı gün Ebrim Voss'a bir tanıtım mektubu yazdı (otomatik erişim değil, sadece kapıyı çalmayı kolaylaştıran bir anahtar) — **bu mektup session 27'de kullanıldı**, Voss'la tanışıp Grand Spire üyeliği ve Unfinished Circle/Sylandra Cael ipucu buradan geldi.
  - **Gün 181 devamı (session 29, bugün):** İlvaneth, Karsgate'e TP Circle ile dönüp Odalys'e Voss'un kabulünü + dosya erişimini bildirdi (anlaşmanın kendi payını yerine getirdi), sonra Ash Reeve'e dair ek bir soru sordu (aşağıya bak) — Odalys'in vaadi/uyarısı hâlâ geçerli: phylactery'yi "nasıl yok edilir" değil "nasıl korunur" diye sorarsa güven biter.
  - **Bugünkü ek bulgu (genel notebook, Passive Investigation 24):** bir "kap" (phylactery/kalıcılık aracı) zorla alındığında çatlar, sadece gönüllü verildiğinde bütün kalır — kül-kralların hatası tacı yas nesnesi olarak kabul etmek yerine hak olarak almalarıydı. Ayrıca Ash Reeve Understreets'in **en derin/en eski odası hiç haritalanmamış** — session 27'de "tamamlandı" sayılan dungeon'da gerçekte keşfedilmemiş bir bölüm var. İlvaneth'in çıkardığı sonuç: Sylandra Cael'in çatlak phylactery'si muhtemelen orada, çatlağın sebebi gücü zorla almış olması olabilir. "Cael hattı" ipucuyla (gün 167) birleşince artık güçlü bir isim eşleşmesi var — henüz Odalys'e açıklanmadı.
  - **★★★ ÇÖZÜLDÜ VE DERİNLEŞTİ (gün 187, session 32) — kanıtlanmıştı, doğrulandı.** İlvaneth, Ash Reeve'de Sylandra'yla yüz yüze karşılaşınca kendi sonucunu saklamadan anlattı — Sylandra doğruladı: phylactery'si gerçekten çatlak. Bkz. Live State Flags, yeni açık iplik aşağıda.
- **★★★ YENİ, AÇIK, UZUN VADELİ (gün 187, session 32) — Sylandra Cael ile "gönüllü verilen güç" ortaklığı.** İlvaneth ve Sylandra artık birlikte, Sylandra'nın kendi çatlak phylactery'sini gerçekten onarmanın/tamamlamanın bir yolunu arıyorlar. Henüz somut bir sonraki adım yok — bu, İlvaneth'in kendi Ascension/ölümsüzlük arayışına doğrudan paralel, potansiyel olarak kampanyanın ana temasına (Kriv'in "ayrı tut" mirası vs İlvaneth'in "birleştir" hedefi) bir üçüncü sesle katkıda bulunabilir. Standard 10 gereği zorlanmamalı — organik olarak gelişsin.

## Faction Moves
*Dünyanın parti meşgulken yaptığı ve **partinin görebildiği** şeyler — kısa, olay bazlı bir kayıt. Bir hamle çözüldüğünde buradan düşer.*
*★ Planlar, duruşlar, bütçeler ve istihbarat burada değil: `factions.json` (araç: `scripts/factions.py`). Kim kime düşman, kimin hangi operasyonu hangi güne kadar yürüttüğü oradan sorgulanır — düzyazıdan yeniden kurulmaz. Dengeyi değiştiren her olaydan sonra `factions.py react` çalıştırılır.*

**Canlı (gün 191'den itibaren):**
- **★★★ YENİ, AÇIK (gün 203'ten itibaren, session 35) — Parti fiziksel olarak başka bir düzlemde (Ember Court), Emberhold'daki siyasi momentum kendi başına ilerliyor.** Cassian kendi hanesini temizliyor; Sereth soğuk ama sadık bir ittifakta bekliyor; Berengar kâr peşinde sakin; Coren'in darbe hazırlığı (Ilse Drummel'in izlemesiyle) devam ediyor; Maro Veskin kâtibi Ostwin Kade'nin kaybolduğunu henüz fark etmedi. Parti dönüşünde bu ipliklerin ne kadar ilerlediği netleşmeli.
- **★★★★★★ EN BÜYÜK (gün 198, session 35) — Whisper Court'un gizliliği TAMAMEN BİTTİ (Goal Tracker: threatened, 3/3 ajan ifşa — ama Iskra kendisi hâlâ reform halinde, kalıcı kapanmadı, düzeltildi session 36).** Iskra Vantrel/"V." kimliği açığa çıktı (House Ilvane'in kendi danışmanı, 20 yıldır), 8 aylık bir doppelganger (Corwen kılığında) yakalanıp öldürüldü, Iskra kendisi konaktan kaçtı — muhtemelen Plane Shift ile kendi düzlemine. Artık gizlenmeyecek: bir dahaki hamlesi doğrudan, daha az tedbirli, muhtemelen daha şiddetli olacak — parti bunu tetikledi ama ne zaman/nasıl geri geleceği henüz sahnede yok. **Cassian Ilvane artık gerçek bir müttefik** — kendi hanesini baştan aşağı temizliyor, parti üç hanenin de sırlarını (Corr/Sablewood/Ilvane) elinde tutuyor.
- **★★★★★ YENİ (gün 197, session 35, Kırık Kemer köprüsü, Ember Quarter) — "V." ağının açık teklifi (kalan ağa dokunmama karşılığı karşılıklı çekilme) parti tarafından reddedildi, hem de hakaretle.** Kriv, ağın sözcüsü Pike Rourke'a (Halfling fixer, işvereninin fiend olduğunu bilmiyor) "piyonlarla pazarlık yapmayacağını" söyleyip V.'yi doğrudan yüzleşmeye çağırdı — Pike, kendi üstünü hiç görmediğini itiraf etti (katmanlı anonimlik doğrulandı), bir haftalık cevap süresi tanımıştı ama parti mesajı hemen, açıkça reddetti: "nereye iletirsen ilet, V. duysun, kendi karar versin." **Bu artık "cevapsız" değil, aktif ve hakaret içeren bir ret — ağın tepkisi muhtemelen beklenenden daha hızlı/sert gelecek, henüz sahnede değil.** Pike korkmuş ama gerçek bilgisi sınırlı görünüyor, panik içinde uzaklaştı.
- **★★★★★ YENİ, BÜYÜK (gün 194-196, session 34) — Whisper Court/"V." ağı, aynı günde üç büyük kaybı birden yaşadı: Wren Marrow'un ifşası, Ansel Drey'in (bir müttefik/müşteri, doğrudan üye değil ama değerli bir kanal) öldürülmesi, VE Noter Ostrin Vell'in (kendi ajanları tarafından "temizlenen" bir zayıf halka) infazı — ki bu üçüncüsü parti değil, ağın KENDİSİ yaptı, saatler içinde, sızıntı riskini kapatmak için. Bu, ağın hem ne kadar ciddi tehdit altında hissettiğini hem de ne kadar hızlı/acımasız tepki verebildiğini gösteriyor. Henüz sahnede bir karşı-hamle yok ama bu seviyede bir kayıp dizisi (Wrenna+Arnholt'tan sonra) fark edilmeden kalamaz — bir sonraki Emberhold/Karsgate sahnesinin doğal açılışı.**
- **★★★★ YENİ (gün 194, session 34) — Cassian Ilvane'in koalisyonu Batı Bahçesi'nde herkesin önünde çöktü, House Marrow açıkça House Shestendeliath'a geçti.** Cassian'ın kendisi gerçekten habersiz görünüyordu (Iskra'nın bilmeden manipülasyonuyla tutarlı) — ama bu, House Ilvane'in kamuya açık ikinci büyük siyasi yenilgisi. Iskra Vantrel'in (DM-only) buna nasıl tepki vereceği henüz sahnede yok.
- **★★★★ YENİ (gün 194-195, session 34) — Emberhold'un Reeks yeraltı ağı (Sunken Ledger'ın yıkımı) artık şehir çapında biliniyor.** Undertow, River Guild, Blank Seal — hepsi konuşuyor, Kriv'in adı her cümlede geçiyor (Grimwell'in doğrudan uyarısı). Reeks'teki hiçbir bilgi kaynağı/simsar artık partiyle kolay çalışmayacak — bu, gelecekte bir bilgi ihtiyacı doğduğunda gerçek bir engel olacak.
- **★★★ YENİ (gün 195-196, session 34) — Ilse Drummel (Ironclad Table), Coren'in Kriv'le olan yakınlığını izlemeye devam ediyor — Coren'in kendi darbe planı henüz tamamen gizli ama zaman ilerledikçe risk büyüyor.** Coren birkaç hafta içinde hangi Table üyelerinin sadık kalacağını çıkaracak — bu süreçte bir sızıntı/şüphe artışı olası, henüz sahnede yok.
- **YENİ (gün 195, session 34) — Ashlord Concordat'ın Emberhold şubesi, Tain'in "iç temizlik/reform" raporunu aldı — inanıp inanmadıkları henüz sahnede yok.** Kavash'a bizzat bir ziyaret talep etme riski hâlâ açık, sadece ertelendi.
- **★★★★★ ÇÖZÜLDÜ (gün 192, session 33) — Ashlord Concordat'ın Karsgate liderlik boşluğu kapatıldı, ama gizlice.** Solenne Kavash (Sarelle'in tek gerçek varisi) partiyle yüzleşip öldürüldü. Orell Tain, Kavash'ın mührüyle sahte bir vekillik belgesi hazırlayıp Karsgate Grand Archive'ını devralmaya gitti (gün 192'den itibaren, sonuç birkaç gün/hafta sürecek) — parti destekli ama resmi olarak gizli. **Emberhold/diğer şubeler hâlâ Sarelle'in VE Kavash'ın öldüğünü bilmiyor.** Tain'in devri ne kadar pürüzsüz gideceği (bir sonraki Karsgate ziyaretinde) açık bir soru.
- **★★★ YENİ (gün 192, session 33) — Tobin Wrey'in ekibi (Rovan + 4 kişi) parti tarafından yok edildi, Sundered Reach yolunda.** Kendi açgözlülüğüyle ihanet edip pusu kurmuşlardı (ödeme defterinde bulundu: "Frostmere'e ilk biz varırsak... rakipler kim olursa olsun"). Tobin'in kendisi olay yerinde değildi — ekibinin kaybını ne zaman/nasıl öğreneceği, ve bunu bir ihanet mi yoksa savaş ilanı mı sayacağı henüz sahnede yok. **The Long Coin (Tobin'in topluluğu) artık potansiyel bir düşman, eski bir bilgi-paylaşım müttefiki değil.**
- **★★★ DURAKLATILDI (gün 191-194, session 33) — Emberhold'un üç hane siyaseti (Veskin, Corr/Sablewood/Ilvane, Whisper Court) parti Sundered Reach'teyken kendi mantığıyla ilerliyor.** Parti fiziksel olarak yok, kendi siyasi momentumunu koruyamıyor — House Ilvane/Iskra Vantrel'in bu boşluğu nasıl kullanacağı (bkz. `veskin`/`whisper_court` Goal Tracker'ları) bir sonraki Emberhold sahnesinde netleşmeli, zorlanmadan.
- **★★★★★ GOAL TRACKER: Coren Ashvale HEDEFE ULAŞTI (gün 191, session 32).** Ailesinin mezarının intikamı alındı, Concordat Ashvale'den kalıcı olarak uzaklaştırıldı — Coren'in kendi kişisel arayışı tamamlandı. **Açık soru, henüz sahnede yok:** şimdi ne yapacak? Ashvale'i gerçek bir Ashvale koltuğu olarak mı yeniden kuracak, Compact'ı gerçek bir güç olarak mı büyütecek, yoksa İmparator'un suikast kanıtını siyasi olarak mı kullanacak — organik olarak gelişmeli.
- **★★★★★ YENİ, EN BÜYÜK (gün 191, session 32) — Sarelle Duskbourne öldü, Ashvale düştü.** Concordat'ın Emberhold/Karsgate şubeleri henüz haberi almadı — bu, günler içinde patlayacak bir haber. Solenne Kavash (hayatta, Ashvale'de değildi) liderliği devralmaya çalışabilir ya da Concordat'ın kendi içinde bir güç boşluğu/iç çatışma başlayabilir. House Ilvane, Whisper Court, ve Cinder Choir gibi diğer faction'lar bu haberi aldığında nasıl tepki vereceği (bir fırsat mı, bir tehdit mi olarak okuyacakları) henüz sahnede yok — organik olarak gelişmeli, zorlanmamalı.
- **★★★ GÜNCELLEME (gün 191, session 32) — Parti teklifi reddetti, doğrudan saldırı planladı.** Sarelle'in "silahsız gel" teklifi bir tuzak riski olarak okundu — bunun yerine parti, Restday'in kendi güvenlik açığını (Reyna Sorrel'in bilgisi) silah olarak kullanmaya karar verdi. **Coren Ashvale ile operasyon planlandı (Coren'in kampı, gün 188-191 arası):** Coren + ~148 paralı asker ön kapıya açık bir saldırı düzenleyip garnizonun dikkatini çekecek (diversion). Kriv + İlvaneth, **Chalk Warrens** (Coren'in ailesinin bildiği, Concordat'ın hiç bulamadığı gizli mağara yolu, Vault Stair Junction'a çıkıyor, Outer Garrison'ı bypass ediyor) üzerinden sızıp doğrudan Sarelle'e gidecek. **Sethra + Ressa Varn + Tain + Coren'in 2 güvenilir adamı** aynı yoldan girip ayrılacak, **Munitions Store**'u (cephanelik) sabote edip düşmana ek avantaj sağlayacak. Kriv, operasyon öncesi **Warden's Core**'u attune etti (3/3 slot dolu). Operasyon **Restday gecesi (21 Ashfall)** başlıyor.

<details>
<summary><b>Arşiv — gün 96-190 arası kapanmış/eskimiş hamleler (38 kayıt, 2026-09-22'de katlandı)</b></summary>

*Bunlar tarihsel kayıt. İçlerindeki iki eski "saat" (Coren'in sabrı ~gün 120, Sarelle'in toplama döngüsü) 80+ gündür ölüydü ve canlı gibi duruyordu — faction saatleri artık `factions.json`'daki operasyon adımlarında, son tarihleriyle birlikte tutuluyor.*

- **★★★★★★★ DÜZELTİLDİ (session 36) — Iskra Vantrel ÖLMEDİ, ağır yaralı kaçtı, hâlâ reform halinde.** Kesh Amara'daki Cinderday gecesi toplantısı bir ambusla bitti — Iskra ve kıdemli yoldaşı Sathriel, İlvaneth'in Draconic Transformation nefesi + Kriv'in Action Surge/GWM kombosuyla 2 round'da neredeyse yok edildi, hiç PC hasarı almadan — ama rakshasa doğaları gereği kalıcı ölmediler, Kaal'ın düzlemine (Ember Court) çekilip Oda 24'te reform sürecine girdiler; parti şu an bu dungeon'ı temizleyip onları bitirmeye çalışıyor (session 36'da Oda 1-11 temizlendi, Oda 12'nin eşiğinde). **Son sözü DM-only bir uyarı taşıyordu: "Kaal asla gerçekten ölmez, sadece bir süreliğine sabırsızlanır."** House Ilvane/Corr/Sablewood henüz Iskra'nın kaçtığını/ağır yaralandığını bilmiyor. Maro Veskin'in kendi kâtibi Ostwin Kade aynı gece kalıcı öldü — Veskin bunu henüz fark etmedi, ama er ya da geç kâtibinin kaybolduğunu sorgulayacak.
- **★★★ YENİ, BÜYÜK (gün 187, session 32) — Sarelle DOĞRUDAN TEMAS KURDU, Goal Tracker'ın BLOCKED eşiği tetiklendi.** Vayle + Reyna Sorrel'in art arda kaybı paranoyasını tetikledi (Concordat içinde tasfiyeye başlıyor, Solenne Kavash'tan bile şüpheleniyor — henüz sahnede gösterilmedi, DM-only bir arka plan). Sarnıçta, büyüsel bir "ses" olarak (Sending'e benzer bir yöntem, fiziksel bir ajan riske atmadan) Kriv'e doğrudan ulaştı — **Kriv'in kimliğini/unvanını artık kesin biliyor** (Hollow Throne'daki kamuya açık tanınma duyulmuş). **Chapter 2 Beat 1b ("Sarelle'in Teklifi") resmen telegraph edildi:** Ashvale'e, Restday gecesi, silahsız (tek başına ya da İlvaneth'le) gelmesi için davet — İmparator'un gerçek ölüm nedenini bildiğini biliyor, bunu hem havuç hem kırbaç olarak kullanıyor. Gelmezse "elindeki her şeyi" kullanacağını söyledi. **Parti henüz cevap vermedi.**
- **YENİ (gün 186, session 31) — House Ilvane, iki ajanının kaybını fark etmek üzere.** Elian Rook'un gönderdiği iki ajan (House Ashveil operasyonu) hiç rapor vermedi — parti dungeon'da (Kule-i Mensuh, tüm gün 186) meşgulken, Rook'un bunu ne zaman/nasıl fark edeceği ve Cassian'a söyleyip söylemeyeceği (kendi şüphesi zaten var, bkz. npcs-full.md) henüz sahnede yok. Veskin de bu bilgiyi elinde tutuyor, kendi kartı olarak — üç taraf (parti, Rook, Veskin) aynı olayı farklı açılardan biliyor, kimse tam resmi görmüyor.
- **YENİ (gün 186, session 31) — Whisper Court/Iskra Vantrel, House Ilvane'in art arda üçüncü kaybını (Wrenna, Arnholt, şimdi 2 ajan daha) henüz işlemedi.** Bu, ağın en kötü haftası olmalı — ama parti tüm günü yer altında geçirdiği için tepkisi henüz bilinmiyor.
- **ÇÖZÜLDÜ (gün 186, session 31) — Corbin Vayle öldürüldü, Ashscar Sırtı'nda, Emberhold dışında (bkz. Open Threads).** Concordat henüz ne Reyna Sorrel'in ne Vayle'in kaybını biliyor — iki saha varlığı art arda sessizleşti, er ya da geç fark edilecek, Sarelle'in paranoyak "kayıp ajan" örüntüsüne iki yeni vaka eklenmiş olacak.
- **YENİ (gün 182-185) — House Ilvane, Chancellery itirazının halka açık yenilgisini sindirmeye çalışıyor.** Cassian Ilvane'in "bugün için" geri çekilmesi kalıcı değil — Iskra Vantrel'in (Whisper Court) bu gelişmeye nasıl tepki vereceği henüz sahnede yok, ama Wrenna/Arnholt'un ifşasından sonra ağının iki büyük kaybı üstüne bu üçüncü bir siyasi yenilgi.
- **YENİ (gün 182) — Sereth Corr, kamuya açık desteğini gösterdi (dinlemede tanıklık) — House Sablewood ve House Ilvane'in ikisi de artık Kriv'i House Corr'un doğrudan müttefiki olarak okuyor.** Chapter 2'nin kendi B senaryosu (üç hanenin dışarıdan bir değişkene karşı hizalanması) için somut bir tetikleyici.
- **★★★ YENİ SAAT (gün 184'te dolacak, session 29) — Sundered Garden randevusu.** Kriv'in gün 167'de bıraktığı mesaja (kimliği doğrulanmamış bir kukuletalı kadın aracıyla) 14 gün sonra bir yanıt geldi — imzasız, kül-gri mühürlü, gün 184 gün batımında yalnız buluşma teklif ediyor. Gönderen Sarelle mi, Concordat'ın başka bir eli mi, yoksa tamamen farklı biri mi — henüz belirsiz, DM-only bile değil çünkü DM de henüz karar vermedi. 2 gün kaldı.
- **YENİ (gün 181/182, session 29) — House Ilvane'in genealoji/heraldik geçmişi Karsgate'in genel arşivinde araştırıldı** (kurucu efsane, Cassian'ın kişisel kaydı). Bu ziyaret gizli değildi ama dikkat çekici de değildi — kimse fark etmedi, kimse takip etmedi. Ama İlvaneth'in Kindled Circle içindeki "izlenen vaka" statüsü (Rask/Voss) göz önüne alınca, bu tür araştırma ziyaretlerinin bir noktada birleşip fark edilmesi zamanla artan bir risk.
- **★★★ YENİ (gün 179/180, session 28) — Whisper Court, aynı günde iki ajanını birden kaybetti: Wrenna (infaz edildi) ve Arnholt (yakalandı, Berengar'ın sorgusunda).** Iskra Vantrel'in House Corr VE House Sablewood'daki gözü/kulağı bir anda kör oldu — bu, ağın kendi tarihinde eşi görülmemiş bir kayıp olmalı. Henüz sahnede bir tepki yok ama bu seviyede bir kayıp fark edilmeden kalamaz; sonraki oturumun doğal bir tetikleyicisi — Iskra'nın kendisi (ya da House Ilvane üzerinden bir vekili) partiyle doğrudan temasa geçebilir, ya da sessizce geri çekilip yeni bir yaklaşım kurabilir. Ayrıca: Dorren Corr'un 2 yıl önceki ölümünü tetikleyen "kırık daire" mührü, bu sabahki Silent Ledger tehdit mektubuyla aynı — parti bu bağlantıyı biliyor, Sereth'e henüz tam açıklamadı.
- **★★★ YENİ (gün 178/179) — DM-only: Whisper Court'un (Iskra Vantrel'in ağı, oyunculara henüz açıklanmadı) Kriv'i izlediği artık somut kanıtlı.** Sessiz Defter'in ele geçirilen mektubu, "Efendiler"in Boş Koltuk'a yeni bir yüzün geldiğini zaten not ettiğini gösteriyor — parti bunun kim olduğunu bilmiyor, sadece izlendiklerini biliyor. Sereth Corr, Sablewood/Ilvane'den şüpheleniyor ama emin değil. Bir sonraki hamle: Rookery baskınında (3 gün sonra) gerçek bir isim/ajan ortaya çıkabilir, ya da Whisper Court sessizce geri çekilip izlemeye devam edebilir.
- **YENİ (gün 176-179) — Ashlord Concordat, Sarelle'in Yorath Sable'a yazdığı mektubun kayboluşunu henüz fark etmedi.** Kurye öldürüleli birkaç gün oldu — bu suskunluk süresi uzadıkça (Concordat'ın kendi "Missing Archivists" örüntüsüne bir vaka daha eklenerek) fark edilme ihtimali artıyor. Henüz sahnede bir sonuç yok.
- **★★★ YENİ (gün 176, session 27) — Ashlord Concordat, Sarelle gerçek bir panik içinde.** D.V.'nin başlattığı söylenti kampanyası işe yaramaya başladı — Sarelle, Emberhold'daki bağlantısı Büyük Sorgu-Amiri Yorath Sable'a yardım isteyen bir mektup yazdı, kuryesi parti tarafından öldürüldü, mektup ele geçirildi. Sarelle henüz kuryenin öldüğünü/mektubun kaybolduğunu bilmiyor — bu bilgi boşluğu er ya da geç fark edilecek, tepkisi öngörülemez. Yorath Sable, Emberhold'da gerçek bir Concordat gücü — henüz hiç temas kurulmadı.
- **YENİ (gün 176) — The Silent Ledger (Emberhold'un gizli suikastçı ağı) bir üyesini ve iki ajanını kaybetti** (parti tarafından, yanlışlıkla Ser Aldric Vane sanılarak). Kimin arkasında olduğu bilinmiyor — bir jeton (kuş+defter motifi) ele geçirildi. Ağın gerçek işvereni (Sereth Corr'un rakiplerinden biri, ya da tamamen başka biri) henüz bilinmiyor; kayıp ajanları er ya da geç fark edecekler.
- **YENİ (gün 176) — House Sablewood/Berrin Voss söylentisi doğrulanmayı bekliyor.** Bir sarhoş Sablewood muhafızı iddia etmiş (üç hafta önce, artık kayıp) — Voss'un tefecilik operasyonu House Sablewood tarafından finanse ediliyor, Ember Quarter'da agresif toprak/borç ele geçirme. Somut kanıt yok, sadece bir hancı söylentisi.
- **★★ Ashlord Concordat — Wyle Sarn'ın Harrowgate operasyonu ÇÖKTÜ VE ARTIK GERÇEK BİR ALARM YARATTI (gün 133→144, session 26 FF).** Sarn hâlâ sessiz (tutsak, sonra idam edilmedi ama Hold'da hapiste). Cinder Hollow'a gönderilen Mira Kessel de hiç rapor vermeden kayboldu — iki saha ajanı art arda sessizleşti, Sarelle'in "Missing Archivists" örüntüsüne üçüncü/dördüncü bir vaka daha ekleniyor. İki haftalık boşluktan sonra bu artık göz ardı edilemez — Karsgate'ten gerçek bir soruşturma/arama ekibi gönderilmiş olması muhtemel, ama parti henüz doğrudan bir sonuç görmedi. **Sonraki oturumda bu netleştirilmeli: Concordat'ın tepkisi ne, kim gönderildi, Harrowgate'e mi yoksa Cinder Hollow'un küllerine mi odaklanıyorlar.**
- **Ironclad Compact — Coren Ashvale, Karsgate/Ashvale yakınına döndü (gün 134'ten itibaren), Sarelle'i daha yakından izliyor.** Thornlands'teki tırmanma durmuş durumda, kamuya açık çatışma görüntüsü korunuyor. İki haftalık boşlukta bir gelişme bildirmedi — sessizlik, ya her şey sakin ya da henüz paylaşacak bir şeyi yok.
- **Ashlord Concordat — Yok edilen askere alım kampının keşfi — ARTIK KEŞFEDİLDİ (gün 127 civarı, gezgin bir ozandan söylenti olarak duyuldu, session 25 devamı, Harrowgate yolu).** Concordat gerçekten "çılgına dönmüş," her yöne muhafız/soru gönderiyor, bir tüccarın deyimiyle "sanki bir savaş ilan edilmiş gibi." Parti henüz doğrudan bir sonuç görmedi ama tepki artık aktif ve halk arasında konuşuluyor. Eski not: Kampın check-in yapmaması + yolun üstündeki orman yangını, er ya da geç fark edilecek. Bu, kayıp bir birimden farklı — gerçek bir suç mahalli (7 ceset yerine yanmış kalıntılar, 2 sivil dahil). Keşfedildiğinde Concordat'ın tepkisi çok daha sert olabilir (bir "kayıp" değil, açık bir saldırı olarak okunacak).
- **Ironclad Compact — Renwick'in Coren'i ikna girişimi (gün 110'da başladı):** İlvaneth'in baskısıyla yola çıktı, Coren'e kâr dilinde bir argüman sunacak. Sonucu 3b'nin en olası tetikleyicisi — sonraki oturumun doğal açılış noktası.
- **Ironclad Compact — Coren'in sabrı (~gün 120, ~24 gün kaldı, gün 96 itibarıyla):** Coren, Ashvale Necropolis için inkar edilebilir bir araç bulamazsa kendisi doğrudan harekete geçecek, tam savaş.
- **Cinder Choir — Yeva'nın keşfi ARTIK HOLLOW PROPHET'E ULAŞTI (gün 113, session 24 kalibrasyonu — önceki "yakında yüzeye çıkabilir" ifadesi dört oturumdur ilerlemiyordu, bilinçli olarak tetiklendi; DÜZELTİLDİ session 24 devamı — bilgi kapsamı fazla iddialıydı, geri çekildi).** Ilyra Thorne (Hollow Prophet, DM-only) Fenn'in hücresinin yok edildiğini biliyor, ve Yeva'nın istihbaratı **sadece kamuya zaten açık iki bilgiyi** birleştirdi: (1) "elf+dragonborn" tarifi (Concordat'ın ödül ilanından, gün 5'ten beri dışarıda), (2) Kriv'in kendi bilinçli kararıyla gün 103'te Gallowmere'de yaptığı halka açık kimlik ilanı ("Lord Kriv Shestendeliath, dönen varis, garnizonu ele geçirdi"). **Crown parçaları ve gerçek Ascension/draconic dönüşüm mekaniği HÂLÂ TAMAMEN GİZLİ — Prophet bunları bilmiyor, kimse dışarıdan bilmiyor.** Prophet'in elindeki tek şey: "yıkılmış bir Ash-Warden hanesinin varisi geri döndü, güç kazandı" — bu, Choir'ın "ölüp-dönen gerçek hükümdardır" doktrinine sembolik olarak fazlasıyla yakın okunuyor, muhtemelen yanlış/abartılı bir yorum ama Prophet'in inancı buna hazır bir çerçeve sunuyor. **AŞILDI (gün 118, session 24) — parti, Concordat'tan bile habersiz, doğrudan Ilyra Thorne'un evine gidip onunla yüz yüze görüştü ve Kriv kendi hikayesini (kanıyla evini yeniden ayağa kaldırması) bizzat anlattı.** Ilyra artık gerçek, kişisel bir ilgi/yoğunluk gösteriyor Kriv'e — bu artık soyut bir "duyan biri" değil, doğrudan bir temas. Crown parçaları/gerçek Ascension mekaniği hâlâ tamamen gizli, Ilyra bunları bilmiyor. Sonraki adım tamamen partinin elinde — Ilyra'yla ilişkiyi nasıl geliştirecekleri (ya da geliştirmeyecekleri) DM için canlı bir gözlem konusu.
- **The Kindled Circle (büyücüler loncası, YENİ, gün 113, session 24) — parti hakkında zaten aktif ilgi duyuyor, alışverişten çok daha büyük bir sebeple.** Gün 111'deki askere alım kampı Fireball'ı + kontrolsüz orman yangını (hâlâ Concordat tarafından keşfedilmedi, ayrı bir saat) gerçek bir büyü imzası bıraktı — bu ölçekte, dizginsiz, öldürücü bir büyünün kalıntısı, yetkin bir uzmanın (ya da Lonca'nın kendi tespit yöntemlerinin) fark edebileceği türden. Lonca, bölgede lisanssız, son derece güçlü bir Necromancy büyücüsünün olduğunu öğrendi ve kimliğini/konumunu araştırıyor — **Concordat'tan bağımsız, paralel bir keşif zinciri.** Sonucu henüz belirsiz: düzenleyici bir uyarı mı, bir davet mi, yoksa daha ciddi bir müdahale mi olacağı partinin nasıl tepki vereceğine ve DM'in ilerideki kararına bağlı. **Session 25'te netleşti: soruşturmayı Lonca'nın Archmagister'ı Magistrix Odalys Ferrant bizzat üstlendi** (kimseye devretmedi) — kendi geçmişinde Necromancy'e çekilip vazgeçmiş biri olduğu için kişisel bir tetiklenme, sıradan bir düzenleyici merak değil. Bkz. `npcs-full.md`.
- **Ashlord Concordat — Sarelle, "iç sızıntı" soruşturması başlattı (gece, session 20):** Kayıp konvoylar + iki kayıp arşivci (Nessa Wren, Perrine Oskold) artık tesadüf sayılmıyor. **SONUÇLANDI (gün 96 akşamı): Tain gerçekten tutuklandı, Sarelle bizzat sorguladı, isimleri ("Ilvaneth", "Kriv") biliyordu — kaynağı belirsiz.** Parti + Sefwyn, Tain'i Archive'a nakil sırasında pusuya düşürüp kurtardı — 2 muhafız + sürücü öldürüldü. Tain artık fugitive, Thornwick'te saklanıyor. Sarelle henüz eskortunun kaybolduğunu keşfetmedi (bkz. aşağıdaki madde) — bu keşfedildiğinde tepkisi yeni bir tehdit olacak.
- **Ashlord Concordat — Sarelle'in toplama döngüsü (~20-30 günde bir):** Fragment kurtarma çabaları sürüyor, güvenlik her kayıptan sonra sıkılaşıyor (2 konvoy zaten kayboldu).
- **Sarelle — Convergence Risk (2/3):** Bir bağlantı daha, "elf+dragonborn" tarifini doğrudan partiye bağlar.
- **Concordat — Missing Archivists (2/3):** İki saha ajanı (Nessa Wren, Perrine Oskold) aynı görevde kayboldu; üçüncü bir kayıp resmi bir soruşturma açar.
- **Sefwyn Marrow — Private Tally (1/3):** Partinin paylaştığı her Crown bilgisi onu daha hızlı satıp kaybolmaya itiyor.
- **Kessic Ambrey / Varic Sennett (1/3, eşleşen çift):** Ya Ambrey parçayı bulup yakalanır, ya Sennett hücresine karşı ilk hareket eder.
- **Coren Ashvale — Ashvale Grievance (2/3):** Concordat'a karşı açıkça harekete geçmeye yaklaşıyor.
- **Mother Vey — Partiyi Okumak — ÇÖZÜLDÜ (3/3, gün 110, session 23):** Bugünkü meydan olayı + asker toplama girişimi netleşmesini sağladı. Dükkanında açıkça "Lord Shestendeliath" dedi (gün 103'ten beri bildiğini itiraf etti, ilk kez sesli). Nihai değerlendirmesi: "Artık bir risk değilsiniz, bir bahissiniz" — tehlike gerçek (Concordat ödülü, Compact husumeti) ama getirdikleri düzen de gerçek (Kell sonrası iş, yasal kaçakçılık, gurur duyan gençler). Ne düşman ne kayıtsız şartsız müttefik — dikkatli, gerçekçi bir kabul.
- **Sethra / Vharkoss (1/3, her ikisi de):** Birbirini avlıyor, Kriv'in aile sırrına bağlı.
- **Ashlord Concordat — Gallowmere-Hold yolundaki askere alım kampı YOK EDİLDİ (gün 111, session 23):** Parti, yol üstünde kurulu bir Concordat askere alım standına rastladı — masada partinin "elf+dragonborn" tarif kağıdı vardı. İlvaneth Fireball ile görevli+2 muhafız+2 sivili (sıradaki köylüler) anında öldürdü, Kriv kalan 2 devriye muhafızını bitirdi. Toplam 7 ölü, hiç tanık kalmadı. Bu, kayıp birim örüntüsünden farklı — bu sefer gerçek bir suç mahalli (yanmış cesetler, kömürleşmiş masa) geride kaldı, birileri er ya da geç bulacak. Sivil ölümleri (2 köylü) dahil. Bir tüccar, bir kontrol noktasında normalden çok daha uzun sorgulandığını, "kayıp bir birim"den resmi olmayan bir fısıltıyla bahsedildiğini anlattı — Concordat, Vask'ın birimini henüz resmen açıklamadı ama aramaya başlamış görünüyor.
- **Ashlord Concordat — kayıp tarama birimi (gün 100/101'de yok edildi, gün 104 itibarıyla Concordat henüz fark etmedi):** Deacon Perrin Vask ve 8 muhafızlık escortu Thornlands yolunda tamamen yok edildi/yakalandı, hiçbir tanık kalmadı. Sarelle'in toplama döngüsü, bu birimin check-in yapmamasını er ya da geç fark edecek — üçüncü kayıp saha ekibi (Nessa Wren, Perrine Oskold'dan sonra) olarak Concordat'ta gerçek bir alarm yaratabilir.
- **Ironclad Compact — Renwick'in raporu (gün 103'ten beri bekleniyor):** Renwick Tale, Kriv'in ültimatomunu kabul etti ama Coren Ashvale'e ne rapor edeceği açık — muhtemelen Kriv'in gerçek kapasitesini/iradesini test eden bir değerlendirme olacak, kaynağı belirsiz bir gelecek gelişme.
- **YENİ KANIT (gün 128, session 25 devamı, Karsgate-Harrowgate yolu) — parti, taze bir Concordat-Compact çatışma izi buldu:** kömürleşmiş toprak, kırılmış mızraklar, yarı yanmış iki sancak (Concordat'ın kül-gri + Compact'ın zincir-halka amblemi), kan izleri ama ceset yok. 3b'nin en somut fiziksel kanıtı şu ana kadar — iki faction gerçekten çarpışıyor artık, sadece söylenti değil.
- **Ironclad Compact — Coren'in tepkisi GELMİŞ OLABİLİR (gün 113, session 24, bir Compact kontrol noktası komutanından duyuldu, doğrulanmamış söylenti):** Coren, birkaç gün içinde neredeyse aynı anda iki mesaj almış (muhtemelen Renwick'in yumuşatılmış çerçevesi + Sethra'nın süvarilerinin çıplak raporu), hemen ardından bir toplantıyı iptal edip kendini kapatmış. Sonucu hâlâ bilinmiyor — 3b'nin en güçlü tetikleyicisi şimdi fiilen tetiklenmiş olabilir, ama parti henüz doğrudan bir sonuç görmedi.
- **Ironclad Compact — Sethra'nın istifası, Coren'e gidiyor (gün 104, YENİ):** Sethra, Kriv'in ablası olduğu ortaya çıktı, Compact'tan istifa etti (yazılı, açık). Altı süvarilik eskortu (ikisi Coren'in kendi gözü) durdurulmadan bırakıldı — ana yoldan Coren'e gidiyorlar. **Renwick Tale, kendi hızlı habercisini kestirmeden yolladı (gün 104)** — çerçeveyi kendi belirlemek için: "basit ailevi sebepler, uzun süredir görüşmeyen iki kardeş kavuştu." Süvarilerin resmi raporundan önce ulaşmayı umuyor. Coren'in tepkisi bilinmiyor — iki anlatı da (Renwick'in yumuşatılmış versiyonu ve Compact süvarilerinin çıplak gerçeği) neredeyse aynı anda ulaşabilir, hangisi önce varırsa çerçeveyi o belirler.
- **Ironclad Compact — Renwick Tale, Gallowmere'in sessiz ele geçirilişi — ÇÖZÜLDÜ (gün 103, session 22).** Parti Gallow's Anchor'da doğrudan yüzleşti (Kriv'in ültimatomu, Intimidation 22) — Renwick rıhtımdaki "düzenlemeleri" durdurmayı, gelecekteki her işi önce Kriv'e bildirmeyi kabul etti. El sıkışıldı, açık çatışma yok. Renwick'in Coren'e ne rapor edeceği hâlâ açık bir soru — muhtemelen Kriv'in gerçek kapasitesini/iradesini test eden bir rapor olacak (Renwick'in kendi motivasyonu, oyunculara açıklanmadı).

</details>

## Recent Events
### Session 36 — 2026-09-22 — Ember Court dungeon crawl (Oda 3-11), Ascension Stage 4, gün 203
- **Kayıt hatası düzeltmesi:** Önceki save Ember Court'un (24 oda) tamamını hiç oynanmamış atlayıp "bitti" diye kaydetmişti — oyuncu bunu yükleme sırasında yakaladı ("Biz oyunda en son Dungeondaydık birden eve nasıl ışınlandık"). Gerçek durum: sadece Oda 1-2 oynanmıştı, geri kalanı bu oturumda gerçekten oynandı.
- **Ascension Stage 4 işlendi (her ikisi de)** — level 17 + 8/9 fragman eşiği session 35 sonunda zaten sağlanmıştı ama işlenmemişti, oyuncunun sorusuyla yakalandı. Kriv: uçuş 60ft (gerçek kanatlar, Warden's Oathplate'i yararak çıktı), 9d6 nefes/40ft koni, Truesight 60ft, Legendary Resistance 1/gün — ayrıca kanatlar açıkken Intimidation/Persuasion'da durumsal avantaj (oyuncu mantığıyla onaylandı). İlvaneth: necrotic/poison/disease/exhaustion tam bağışıklık, sıradan yollarla kalıcı öldürülemiyor (24 saatte reform), undead'i isteğe bağlı komuta — bedel: hafıza kaybı artık özellikle yetimhane anılarını hedefliyor.
- **Oda 3-11 temizlendi:** 9× Lemure (Ledger Salonu), Baş Yazman (özel Spinagon CR8), Bone Devil + Sözleşme Kasası'nın loot'u (master Kaal kayıtları + kırık Sözleşme Taşı parçaları, Bag of Holding'e kondu), 4× Barghest (Sickening Radiance ile tek turda), Borçlular Galerisi'nde savaşsız bilgi alışverişi (ileride Oda 8/11/24 tehditleri + Sözleşme Taşı'nın tamamının muhtemelen Tahtı tutanda olduğu öğrenildi), 2× Erinyes, kıdemli Bone Devil (fire immunity uygulanarak), kıdemli Rakshasa Yönetici (Suggestion'ı savuşturuldu, tek turda öldürüldü), Rakshasa Şampiyonu (Limited Magic Immunity ilk kez karşılaşıldı — İlvaneth'in 6. seviye ve altı büyüleri işe yaramıyor bu türe karşı). **Oda 12'nin eşiğinde durdu (3× Rakshasa askeri).**
- **Süreç düzeltmeleri (kalıcı, DM Style Notes'a işlendi):** NPC pasif etkileri (Cloak of Displacement) sadece basılmakla kalmayıp fiilen uygulanmalı; canavar direnç/bağışıklıkları (devil'lerin fire/poison immunity'si) her hasarda kontrol edilmeli, `lookup.py`'nin eksik veri döndürebileceği unutulmamalı — bu artık SKILL-combat.md'de genel bir kural; PC save'leri her zaman oyuncudan gelir, DM asla atmaz (bir kez ihlal edildi, düzeltildi); "şampiyon/kıdemli" etiketli düşmanlar gerçek bir stat farkıyla ayrılmalı, sadece isim değişikliği yetmez.
- **XP:** Kriv & İlvaneth 231.962 → 261.257 (+29.295, Oda 3-11). Level 18 eşiğine 3.743 kaldı — çok yakın.

### Session 35 — 2026-09-20/21 — Kesh Amara baskını, Iskra/Sathriel ağır yaralandı, Level 17, Ember Court'a giriş, gün 202-203
- **Kesh Amara sızması (Kingsward Dış Mahalle):** D.V./Elian Rook üzerinden ulaşılan "Kaal" sözleşme evine **Cinderday gecesi (37 Ashfall, gün 203)** girildi, imp-muhafızın hafızası Modify Memory ile silindi. O geceki toplantıda Iskra Vantrel, kıdemli rakshasa yoldaşı Sathriel, bir yazman-imp, ve Ostwin Kade (Veskin'in gönüllü kâtibi) ile karşılaşıldı.
- **İlvaneth'in Draconic Transformation nefesi + Kriv'in GWM/Trip/Goading/Action Surge kombosu** imp ve Kade'yi anında öldürdü, Iskra ve Sathriel'i 2 round'da ağır yaraladı — ama rakshasa doğaları gereği kalıcı ölmediler, bedenleri Kaal'ın kendi düzlemine (The Ember Court) çekildi, Oda 24'teki Kor Beşiği'nde reform sürecine girdiler.
- **Level 16→17'ye geçildi** (Oda 1-2'nin XP'siyle, dungeon içinde, Long Rest beklenmeden — oyuncu talebi, kalıcı house rule).
- Parti, Kesh Amara'nın Teleportation Circle'inden Ember Court'a geçip Oda 1 (2× Rakshasa muhafız) ve Oda 2'yi (4× Barbed Devil) temizledi, sonra oturum düzgün şekilde `/dm:dnd save` + `/dm:dnd end` ile kapatıldı.

### Session 34 — 2026-09-20 — Wren Marrow himayesi, Reeks katliamı, Level 16, Ironclad Table darbe planı, gün 194-196
- **Batı Bahçesi çeyreklik beyanı:** Wren Marrow'un Cassian'a zorla ittifakı, Kriv'in Persuasion 23'üyle kanıtla ifşa edildi — Cassian'ın koalisyonu çöktü, House Marrow himayeye alındı (10 asker Sonnward garnizonundan). Berengar Sablewood'un borcu ikinci kez ödendi (kanıt), üstüne bir iyilik daha borçlandı.
- **Wren'e suikast girişimi durduruldu** (3 Suikastçı, Whisper Court/Silent Ledger bağlantılı kiralık katiller) — 2 öldü, 1'i sorgulanıp (Dominate Person) infaz edildi. **Reeks'e iz sürüldü: Iona Crask (Ansel Drey'in kapıcısı) Kriv'in zorla geçişinde öldürüldü, ardından Sunken Ledger'a baskın — Ansel Drey işbirliği yaptıktan HEMEN SONRA öldürüldü (İlvaneth'in Chain Lightning'i), 6 muhafızı da öldü.** Kasadan: House Corr/Sablewood/Ilvane'e karşı kanıt, 15 yıllık kırık-daire ödeme kaydı, ~3.440 gp ham nakit.
- **Level 16'ya geçildi (ikisi de)** — Kriv +2 CHA (18), İlvaneth +1 WIS/+1 CHA (16/14), Power Word Stun + Mordenkainen's Magnificent Mansion eklendi.
- **Noter Ostrin Vell öldürüldü** (parti varmadan dakikalar önce) — "Aşkalkanı Emanet Şirketi" paravan şirketi izi Wren'in tehdidinden Chancellery'ye ve 17 yıllık bir Karsgate vakasına (House Corvane) kadar takip edildi, "Bayan V." imzası + kırık daire mührü her yerde. Speak with Dead ile Vell'den tam itiraf + gizli arşiv/servet alındı.
- **Coren Ashvale ile Ironclad Table darbe planı kuruldu** — Coren, Table'dan kopup kendi 900 askeriyle bağımsızlaşmayı kabul etti, Kriv 6.000 gp başlangıç fonu verdi (toplam ihtiyaç ~35-40k gp). Ilse Drummel şüpheli olarak teşhis edildi (Compact'ın Kriv'i araştıran ayrı gözlemcisi).
- **Tain ile aylık ödeme anlaşması** (Concordat'tan, 400 gp/ay başlangıç, yakında 1.500-2.000'e çıkacak) — Emberhold şubesine sahte ama inandırıcı bir "iç temizlik/reform" raporu gönderildi.
- **Odalys Ferrant'a hesap verildi** (Chain Lightning/Reeks olayı) — kabul edildi ama uyarıldı, ikinci bir olayda savunamayacağını söyledi.
- **Kriv'in gear takası:** Warden's Mantle çıktı, Warden's Core geri takıldı (nonmagical B/P/S direnci, lightning zaafı).
- **Ekonomi netleştirildi:** dungeon/combat loot her zaman PC'lere (50/50) yazılır; sadece pasif/aylık gelir tablosu Hold Hazinesi'ne akar.
- **Goal Tracker: Maro Veskin THREATENED'a geçti** — dengeyi koruma hedefi artık gerçek risk altında (Wren Marrow ifşası + 3 hanenin sırlarının parti elinde olması).
- XP: Wren Marrow encounter'ı (Hard noncombat, 4.300/kişi) + Reeks/Sunken Ledger (Deadly combat, Raw 9.800÷2=4.900/kişi) + Wren'e suikast (Deadly combat, Raw 11.700÷2=5.850/kişi). İkisi de **198.762 XP, Level 16.**

### Session 33 — 2026-09-18 — Kavash'ın ölümü, Tain Concordat'ın başına, Level 15/Ascension Stage 3, Ivrathax ile savaşsız ittifak, gün 191-194
- **Solenne Kavash öldürüldü** (Ashvale, müzakere çöktü, Kriv'in Trip+GWM zinciriyle) — Concordat'ın Karsgate liderliği tamamen boşaldı.
- **Orell Tain, Concordat'ın yeni fiili başı oldu** — Kavash'ın mührüyle sahte vekillik, parti destekli, açık bir vicdan uyarısıyla kabul etti.
- **Level 15'e geçildi (ikisi de) — Ascension Stage 3 tetiklendi** (Kriv: Frightful Presence/7d6 breath/Truesight; İlvaneth: yaşlanmıyor, 0 HP'de ölmüyor, ruh görme).
- **Tobin Wrey'in ekibi ihanet edip öldürüldü** (Sundered Reach yolu) — ittifak bitti, muhtemelen yeni bir düşmanlık.
- **Ivrathax ile savaşsız ittifak kuruldu (Persuasion 23) — 8. Crown parçası hediye edildi.** Parti artık 8/9 parça taşıyor.
- Ser Aldwin'in 300 yıllık mektubu Coren'e verildi (duygusal an). Kriv Frostheart + Warden's Mantle'ı attune etti.
- XP: 2.450/kişi (combat, raw÷2) + 4.300/kişi (noncombat, Ivrathax) = 6.750/kişi. İkisi de **183.712 XP.**

### Session 32 — 2026-09-17 — Sylandra ile ortaklık, Sarelle'in düşüşü, gün 186-191
- **Level 14'e geçildi (ikisi de)** — Kriv: Resilient (Wisdom); İlvaneth: Command Undead. XP düzeltmesi: Kule-i Mensuh boss'u CR16'ya düzeltildi (-1500 XP).
- **Sylandra Cael ile tam ortaklık** — kendi çatlak phylactery'sini itiraf etti, "gönüllü verilen güç" araştırması ortak proje oldu, Kule-i Mensuh artık İlvaneth'e her zaman açık.
- **Sarelle Duskbourne DOĞRUDAN TEMAS KURDU** (Goal Tracker BLOCKED eşiği, Vayle+Sorrel kaybı sonrası) — Ashvale'e Restday gecesi davet etti (Chapter 2 Beat 1b world_pressure). **Parti teklifi reddedip doğrudan saldırı planladı.**
- **Ashvale Necropolis'e operasyon:** Coren Ashvale (~148 asker, ön kapı diversion) + Sethra/Ressa/Tain/2 Coren adamı (Munitions Store sabotajı) + Kriv/İlvaneth (Chalk Warrens'tan sızma). Ser Aldwin Ashvale (ghost, Coren'in atası) ile tam ittifak kuruldu.
- **SARELLE DUSKBOURNE ÖLDÜ** — İlvaneth'in Command Undead'i Wight Kaptanı'nı ele geçirdi (kaçışını engelledi), Kriv'in Action Surge novası (219 hasar, tek round) onu prone/çaresiz bıraktı, İlvaneth'in Disintegrate'i tamamen toza çevirdi. **Chapter 1'in gerçek kapanışı.**
- **The Working Archive ele geçirildi** (İmparator'un suikast kanıtı) + Sarelle'in kişisel spellbook'u (Finger of Death, Power Word Kill) + son 2 Crown parçası (İmparator'un mühürlü lahdinden). **Parti artık 7/9 parça taşıyor.**
- XP: +16.025/kişi (Ashvale operasyonu, raw 32.050). İkisi de **176.962 XP** — Level 15 kesin bekliyor.

### Session 31 — 2026-09-16/17 — Kule-i Mensuh (20 oda), Corbin Vayle, gün 185-186
- **Reeks gözcüsüne Modify Memory tuzağı** — House Ilvane'in 2 ajanı yakalandı, Spymaster Elian Rook ifşa oldu, Veskin ile transactional bir anlaşma kuruldu.
- **Corbin Vayle öldürüldü** (Scrying + pusu, Kriv'in Trip Attack + Action Surge novası) — Sarelle'in özel avcı tehdidi çözüldü, Concordat'ın suikast/kaçırma emrine dair somut kanıt ele geçirildi.
- **Kule-i Mensuh (20 oda, oyuncu talebiyle tasarlandı) tamamen temizlendi** — final boss The Warden of the Unfinished (420 HP) düştü, Mireille Osk özgürleştirildi, Sylandra Cael'in kendi geçmişine dair bir sezgi bırakıldı.
- **Üç kalıcı yapısal sistem kuruldu:** Combat Difficulty Doctrine v2+v3 (boss item ekonomisi), XP multiplier ×1 (DMG grup çarpanı kapatıldı), Goal Tracker (`goals.py`).
- XP: ~+30.925/kişi. İkisi de 162.437 XP (sonradan -1500 düzeltmeyle 160.937) — Level 14 kesin bekliyordu.

### Session 29 — 2026-09-15 — Karsgate araştırması, House Ilvane/Ash Reeve ipuçları, Sundered Garden randevusu, gün 181-182
- **Tain'den House Ilvane hakkında genel bilgi alındı** — Lord Cassian Ilvane, eski para/sabırlı oyun bloku, Concordat'ın ash-ritual soy testine hiç girmemiş.
- **Odalys Ferrant'la (Karsgate Kindled Spire) devam eden bilgi anlaşması işletildi** — Voss'a yazdığı tanıtım mektubunun işe yaradığı bildirildi. Ash Reeve/Unfinished Circle sorgusu üzerine Deception 17 vs Insight 10 ile "sadece araştırıyorum" ikna edildi. Yeni bulgu: bir "kap" zorla alındığında çatlar, gönüllü verildiğinde bütün kalır (kül-kralların hatası) + **Ash Reeve Understreets'in en derin odası hiç haritalanmamış** — gün 167'deki "Cael hattı" ipucuyla birleşince Sylandra Cael'e güçlü bir isim eşleşmesi oluştu.
- **House Ilvane genealoji araştırması (Karsgate genel arşivi):** hanenin arması (kırık taç + geyik) — kurucu matriark bilerek kırık bir tacı reddetmiş. Cassian Ilvane evlenmemiş, varissiz; 40 yıl önce "yas-büyüsü/kül-kalıntıları" araştırmasına kısa bir bağış yapmış.
- **Kriv'in gün 167'de bıraktığı mesaja yanıt geldi (Gallow's Rest, Karsgate):** imzasız bir mektup, kül-gri mühürlü — **Sundered Garden'da, gün batımında, üç gün sonra (gün 184) yalnız buluşma teklif ediyor.** Gönderenin kimliği (Sarelle mi, başkası mı) belirsiz.
- **Alışveriş/hazırlık:** İlvaneth Winged Boots + Draconic Transformation'ın tükenmeyen bileşenini aldı; ikisi de yarınki Veskin dinlemesi için attunement'larını yeniden düzenledi (Kriv: BKB deattune/Corr Bıçağı attune; İlvaneth: Ring of Mind Shielding deattune/Winged Boots attune).
- **Emberhold, Grand Spire — Ebrim Voss'la görüşüldü.** Odile Rask'ın resmi inceleme talebi (Fireball/doğrulanmamış kimlik) rafa kalktı, kapanmadı.
- Uzun mola alındı, gün 182 sabahına geçildi — parti hâlâ handa, Hollow Throne'a henüz gitmedi.
- XP yok bu oturumda (qualifying encounter olmadı).

### Session 28 — 2026-09-14 — Sereth'e acil çağrı, Wrenna ifşası, Rookery baskını, gün 179-180
- **Sabah, House Corr'a acil çağrı:** Sereth'in kapısına gece bırakılan imzasız bir mektup ("Kesik Kanat'ın çocuğu... Rookery dahil her şeyi biliyoruz") — Silent Ledger'ın "Efendileri" baskın planını zaten biliyordu. Kriv, Sereth'le özel görüşüp sızıntı ihtimalini gündeme getirdi; Sereth başta savundu ama Persuasion 23 ile ikna oldu, herkesin (kendisi dahil) Detect Thoughts'la sorgulanmasını kabul etti.
- **Wrenna (nedime) — DOPPELGANGER olduğu ortaya çıktı.** Brynn'in bilinçsiz şüphesi (Detect Thoughts) Wrenna'ya yöneldi; Dominate Person işlemedi (humanoid değil — ilk somut kanıt), derin sonda (WIS save başarısız) gerçeği açığa çıkardı: 2 yıldır Lady Iskra Vantrel'e (House Ilvane) rapor veren bir ajan, Rookery sızıntısının kaynağı bizzat oydu. Sereth onu öldürmedi — çift ajan olarak tuttu. House Sablewood'un kahyası Arnholt'un da aynı ağdan olduğu öğrenildi.
- **Sereth, Kriv'i Boş Koltuk için sponsor olmayı kabul etti** — 3 gün sonra (gün 182) Regent-Chancellor Veskin'in dinlemesinde resmen tanıtacak, karşılığında sarayda açıkça yanında durma sözü alındı.
- **Ilvaneth, Sylandra Cael'e Vashti'nin kanıtını teslim etti** — test tamamen kapandı, Circle'ın derin arşivi açıldı, Sylandra'nın kendi phylactery'sinin çatlağına dair küçük bir ipucu sızdı (henüz tam açıklanmadı).
- **Rookery baskını (gece, gün 179):** Sereth'in askerleriyle ortak baskın. Kapıda bir tel tuzağı fark edilip atlatıldı — bina büyük ölçüde tahliye edilmiş, geriye bırakılan bir "karşılama komitesi" (Cipher Handler + 2 Silent Blade, custom stat) sürpriz altında öldürüldü, **hiç hasar alınmadı**. Loot: şifre defteri (rota/ödeme kayıtları, "E.K." kısaltması), gizli bir kutuda House Ilvane mühürlü bir mektup ("V." imzalı, Iskra Vantrel'e işaret ediyor — Sereth'e gösterilmedi, parti sakladı) + gümüş saç tokası (kimliği belirsiz) + 200 gp.
- **XP: +1.100/kişi (Easy combat, Rookery).** İkisi de 121.412 XP, Level 13.
- **Ilvaneth'in 15. Ascension rüyası** (uzun molada) — Cipher Handler'ın son düşüncesi: kendisi "E.K." imiş, House Ilvane'in Boş Koltuk'a karşı zaten aktif strateji kurduğuna dair bir uyarı.
- İkinci uzun mola alındı (Sablewood dönüşü sonrası), gecenin tamamı geçirilip gün 181 sabahına geçildi.

### Session 27 Devamı — Emberhold, Sereth Corr, Sessiz Defter, Vashti Coldharrow, Level 12→13, gün 176-179
- **Sereth Corr ile ilk görüşme (House Corr, gün 176):** Kriv, Sereth'in bahçesinde yalnız görüştü (Ilvaneth Bag of Holding'de gizli eşlik etti). Sereth somut bir kanıt istedi — Vane'i hedef alan suikastın arkasındaki ağı bulmak.
- **Cinder Bell ve Sparrow'un yakalanması (The Reeks):** Dead Notice rüyası Sessiz Defter'in dead-drop noktasını işaret etti. Sparrow, Dominate Person ile yakalandı — işvereni bile kimliğini bilmiyor, ama **"Rookery"** (görev dağıtım merkezi) ve ele geçirilen mektupta çok kritik bir satır öğrenildi: **"boş koltuğa yeni bir yüz geldi... Efendiler bunu zaten not etti."**
- **Sereth'e teslim, gerçek ittifak kuruldu** — House Corr'un desteği sözü alındı, ortak Rookery baskını planlandı (3 gün sonra, henüz gerçekleşmedi).
- **Level 12'ye geçiş:** Kriv ASI (+1 DEX/+1 CHA), Ilvaneth Observant feat + Locate Creature + Mass Suggestion.
- **Vashti Coldharrow'a yolculuk (gün 177-178):** yolda solo bir Stone Golem (Kriv'in Action Surge + kritik Riposte'u tek turda bitirdi) ve 4x Frost-touched Wight (Buz Devriyesi) yenildi.
- **Vashti Coldharrow (460 HP final boss) yenildi — Sylandra'nın testi tamamlandı.** Faz 2'de 3x Specter serbest kaldı, ikisi Sickening Radiance'a yenik düştü. Ödüller: Sylandra için kanıt, Frostheart (Very Rare amulet), ~2.750 gp.
- **Level 13'e geçiş:** proficiency bonus +4→+5 (level 13-16 bandı), Kriv'in Indomitable'ı 2 kullanıma çıktı, Ilvaneth 7. seviye slot açtı (Draconic Transformation, Teleport).
- XP toplamı bu bölümde: 2.000 (Sereth) + 4.425 (Stone Golem) + 3.500 (Buz Devriyesi) + 4.500 (Vashti) = **+14.425/kişi.** İkisi de 120.312 XP, Level 13.

### Session 27 — 2026-09-13 — Karsgate → Emberhold yolculuğu, Chapter 2 başlangıcı, gün 167-176
- **Karsgate'ten ayrılış:** D.V. ile son görüşme (Sarelle'in hastalığı bilgisi karşılıklı çıkar olarak paylaşıldı, borç sayılmadı), Sarelle'e doğrudan meydan okuma mesajı gönderildi (cevapsız kaldı, Riverside/Vesa ipliği çözülmeden bırakıldı).
- **Emberhold yolu (4-5 gün, gerçek travel encounter mekanizmasıyla oynandı):** Regent-Chancellor'ın denetimi (sorunsuz geçildi), haydut pususu (4 Bandit + Bandit Captain, hepsi öldü/infaz edildi — Voss'un tefecilik evine borçlu oldukları öğrenildi), suikast girişimi (1 Assassin + 2 Spy, Ser Aldric Vane sanılarak — Assassin Dominate Person ile ele geçirilip diğerlerini öldürttü, sonra infaz edildi; "Sessiz Defter" adlı suikastçı ağı öğrenildi), Ser Aldric Vane ile gerçek dostluk kuruldu (House Corr bağlantısı), eski bir ash-king savaş alanı keşfedildi (törensel zırh + mühürlü tablet bulundu), Sarelle'in Yorath Sable'a yardım mektubu taşıyan kurye öldürüldü (mektup ele geçirildi — D.V.'nin söylenti kampanyası işe yaramaya başladığının kanıtı).
- **Level 11'e geçildi (her ikisi de) — Ascension Stage 2 tetiklendi:** Kriv (fire immunity, 6d6 breath/2 rest, darkvision 120ft, claws), Ilvaneth (yemek/su/nefes gerekmiyor, hastalık/zehir bağışıklığı, undead komuta 1/rest, hit dice/kısa moladan iyileşemiyor).
- **Emberhold'a varış — Chapter 2 resmen başladı.** Ebrim Voss (Grand Archmagister) ile tanışıldı, Ilvaneth merkez şube üyesi oldu, Unfinished Circle/Sylandra Cael ipucu alındı. Kriv, Boş Koltuk'un dört sponsor adayını (Corr/Sablewood/Ilvane/Veskin) araştırdı. Tobin Wrey ile bilgi paylaşım ittifakı kuruldu. Kriv, Belt of Fire Giant Strength satın aldı (STR 25). Ilvaneth, Efreeti Bottle ayırttı (kapora 1.000 gp, son ödeme 3 Cinderwake).
- **Ash Reeve Understreets (tam dungeon, 6 oda + final boss) tamamlandı:** Corvun Skai/Blank Seal üzerinden geçiş satın alındı. Zombi sürüsü, Ghast/Ghoul sürüsü, Specter'lar, Wight nöbetçileri, Mumya muhafızları, ve final boss **The Unmade** (custom CR13 guardian, Sylandra'nın ilk başarısız kendi-koruma denemesi) yenildi. **Sylandra Cael ile ilk gerçek temas** — tam güven kazanılmadı, **Vashti Coldharrow'u (Sundered Reach) öldürüp kanıt getirme testi** verildi.
- **Level 12'ye XP eşiği geçildi (her ikisi de, 105.887/100.000)** — bir sonraki uzun molada işlenecek.
- XP toplamı bu oturum: bandit pususu (687×2) + suikast (5.375×2) + Ash Reeve dungeon'ı (zombi 600, ghast/ghoul 2.125, specter 1.000, wight 2.625, mumya 1.400, The Unmade 7.500) ≈ +21.312/kişi.

### Session 26 — 2026-09-11/12 — Harrowgate (Wyle Sarn, Konsey), Cinder Hollow, 3 haftalık FF, Karsgate, gün 133-167
- **Wyle Sarn ve "Sessiz" yakalandı (Dominate Person, ikisi de), Kesen/Thorn/Sessiz halka açık idam edildi** — İmparator'un zehirlenmesi Sarn'dan canlı doğrulandı. Sarn hayatta, Hold zindanında.
- **Konsey oylaması kazanıldı — Harrowgate resmen House Shestendeliath'ın himayesinde** (Dahl çekimser, Halworth/Maren/Renata destekliyor), %10 Lord payı.
- **Cinder Hollow'da Mira Kessel yakalandı/infaz edildi — Sarelle'in ölümcül hastalığı öğrenildi**, Solenne Kavash'ın (Sarelle'in ikinci adamı) zayıf noktası tespit edildi.
- **Bram Ostley/Drenmoor Ticaret Evi ipliği** — Ostley infaz edildi, Drenmoor'un büyüsel koruması (Dominate Person'a bile direniyor) çözülemedi, açık kaldı.
- **Üç haftalık zaman atlaması (gün 137-161):** Sethra Fighter 8, yeni asker/subay (Çavuş Toma Brek, Ressa Varn), Hold Hazinesi kuruldu (~1.044 gp), asker sayısı ~92→~127-145, Teleportation Circle Day 24/365 (Tain devraldı), Wardensteel'in nihai tasarımı ("House Shestendeliath'ın Uyanışı," Very Rare) onaylandı.
- **Concordat gerçek bir alarma geçti** (iki saha ajanının kaybı) — arama ekibi Harrowgate'e kadar geldi, Karsgate'e (Ashvale'e rapor) çekildi.
- XP toplam: +1900 (Sarn) + 1200 (Konsey) + 1200 (Mira Kessel) + 3150 (yol savaşları) = +7450/kişi. İkisi de 83.725/85.000 — level 11'e 1.275 kaldı.

### Session 25 — 2026-09-10 — Karsgate (Velkarune, House Varn, Vault of the Nameless), gün 122-123
- **Ashen Crown fragment #5 bulundu** (House Velkarune'un mühürlü konağı) — parti artık 5 parça taşıyor. Sorin Vaal (bağımsız kalıntı avcısı) öldürüldü.
- **D.V.'nin mührü (kitap+çift anahtar) iki kez daha doğrulandı** (Velkarune bakım defteri, Vault of the Nameless lahdi) — toplam 5. karşılaşma, artık kesin bir örüntü.
- House Varn'da canlı bir kukuletalı-ziyaretçi anı gözlemlendi, müdahale edilmedi — açık iplik.
- Vharkoss'un Kingsward konağı resmen kayıp ilan edilmiş, nöbet altında — ziyaret ertelendi.
- **Vault of the Nameless tamamlandı** — isimsiz Ash-Warden mezarı, Threxis'in adıyla açılan mühür, Tain için somut kanıt (D.V. mührü) toplandı.
- **İkisi de Level 10'a ulaştı** (+1100 XP birleşik ödül) — Kriv (Improved Combat Superiority, Trip Attack+Riposte), İlvaneth (Inured to Undeath, Frostbite, Modify Memory, Dominate Person).
- **Büyük bir kampanya-tasarım çalışması yapıldı (oyun-dışı, kalıcı hazırlık):** Sarelle/Coren/Ilyra/Odalys/Karsgate yeraltısı derinleştirildi, D.V.'nin gerçek kimliği (rakshasa, "Lord Dorian Varn") çözüldü, Chapter 1 kapanış planı (A/B senaryo, 12 maddelik öncelik listesi, ekonomik hedef tablosu) oluşturuldu — tam detay `## DM Notes`'ta.
- XP bu oturumda: +1100/kişi. İkisi de ~64.1k/85.000.

### Session 24 — 2026-09-09 — Hold → Greyholt → Harrowgate, gün 112-114
- **Greyholt'ta gerçek bir başlangıç** — iki başarısız denemeden sonra Persuasion 20 ile Hallik'in güveni kazanıldı, hasat sonrası Hold ziyareti vaat edildi.
- Ironclad kontrol noktasında Coren'in tuhaf davranışına dair bir söylenti — 3b tetiklenmiş olabilir, sonuç bilinmiyor.
- **House Ostrel (Cindermoor) ve House Velkarune (Karsgate Kingsward) konumları bulundu**, Harrowgate arşivinde (Investigation 25, History 19).
- **Yazman Aldous Penmark'ın itirafı (Intimidation 24)** — dört evin devrini aynı gizli otorite imzalattı; Ostrel'i satın alan: İlyra Thorne (DM-only). Vharkoss'un mektubuyla aynı mühür (kitap+çift anahtar) doğrulandı.
- İlvaneth'in Ascension rüyası #8 (Vask) — Sarelle'in Ashvale kazısının İmparator'dan önce başladığı doğrulandı, Kriv'e anlatıldı, Tain için saklanıyor.
- Panteon (6 tanrı) ve The Kindled Circle (büyücüler loncası) dünyaya eklendi; yeterlilik bonusu düzeltmesi (+3→+4) her iki karakterde.
- XP: +1100 (Greyholt) + 1600 (Penmark) = +2700/kişi. İkisi de ~52.2-52.4k/64.000.

## Active Combat
*(none — Oda 20 temizlendi, session 37, round 3. Spinagon Özel (fırsat saldırısıyla kaçarken öldü) + 7× Lemure hepsi öldürüldü. Kriv 180/196 HP, İlvaneth 116/116 HP — hiçbir ciddi kayıp yok. +1.985 XP/kişi — ikisi de 276.242 XP, LEVEL UP PENDING (18) hâlâ geçerli.)*

## Live State Flags
*Structured facts designed to survive context compaction.*

**Cover:**
- **KISMEN İYİLEŞTİRİLİYOR (gün 124, session 25 devamı) — Doss'tan istenen iyilik: Ninefinger ağı, Karsgate genelinde (Warrens, Riverside, Kingsward dış mahalleleri) gördükleri "elf+dragonborn" posterlerini indirip yırtacak.** 1-2 gün sürecek, tam kapsamlı değil (Concordat'ın kendi elindeki tarifi ya da başka şehirlerdeki kopyaları etkilemiyor) — sadece Karsgate'te rastgele fark edilme riskini azaltıyor.
- PARTIAL/BLOWN, tırmanıyor — Concordat, gün 5'ten beri "bir elf ve bir dragonborn" tarifini elinde tutuyor; Kessra Vane gün 55'te doğrudan teşhis etti (ama sattırmadı, ortak oldu). Sarelle artık isimlerini de biliyor (gün 96, kaynağı belirsiz — bkz. Active Quests). **Gün 96/97 gece, Karsgate-Hold yolunda bir kavşak türbesinde ödüllü bir "elf+dragonborn" ilanı bulundu** (imzasız, faction belirsiz, birkaç günlük) — tarif artık sadece Concordat'ta değil, halka açık bir ödül avı haline geliyor. Kriv ilanı yırttı ama muhtemelen tek kopya değil.
- **GÜN 103 — Kriv'in kendi seçimi: Gallowmere'de tam kimlik/unvan açığa çıktı, bilinçli ve halka açık** (rıhtım meydanında, tam teçhizat + sancakla). Bu "kaçak tarifi" cover'ından farklı bir katman — artık en azından Gallowmere'de "Kriv" = "Lord Kriv Shestendeliath" bağlantısı kamuya açık. Concordat'ın elindeki "elf+dragonborn" tarifiyle isim/unvan birleşirse, hedef tanımlaması çok daha kesin hale gelir. Geri dönüşü yok, bilerek göze alındı.
- **★★★ GÜN 167, session 26 devamı, Karsgate (bir han, gündüz) — Kriv, kukuletalı bir kadın aracıya doğrudan mesaj bıraktı: "Sarelle'nin peşimden adam koşturmasından sıkıldım. Karsgate'teyim. Konuşmak isterse bu hana haber göndersin."** Kadın (Half-Elf, otuzlu yaşlar, belinde Concordat kül-gri mühürlü bir tomar kutusu) kimin için çalıştığını hiç doğrulamadı — Kriv doğrudan varsaydı, kadın bunu bilerek düzeltmedi: *"Kimin için çalıştığımı söylemedim, ve siz de sormadınız — direkt varsaydınız."* Mesajın gerçekten Sarelle'e ulaşıp ulaşmadığı DM-only bir belirsizlik — kanıtlanmamış. **Bu, Kriv'in bilinçli bir cover kararı: tam konumunu (Karsgate, bu han) meçhul bir aracıya açık verdi.** 14 gün geçti (gün 167→181) — bir yanıt/temas gelmiş olması dramatik olarak beklenir, gün 181'de hana dönüldüğünde kontrol edilmeli.

**YENİ (gün 131, session 26 başı) — Coren Ashvale, İlvaneth'in muhtemelen Concordat'ın aradığı "elf" olduğunu biliyor/tahmin ediyor — açıkça söyledi, tehdit olarak değil ama "bir borç senedi" olarak: kullanmayacağını söyledi, ama hesap tuttuğunu da belirtti. Concordat'a satmadı, satmayacağını ima etti — ama bu gerçek bir kaldıraç, gelecekte geri gelebilir.**

**Kimlik ifşası — kim ne biliyor (2026-09-08 eklendi, gerçek bir kapsam hatasından sonra; gün 103'te BÜYÜK ÖLÇÜDE DEĞİŞTİ):**
- **GÜN 103 — Kriv, Gallowmere'e tam teçhizatlı, pelerinsiz, House Shestendeliath sancağı ve on iki asker eşliğinde girdi** — kendi bilinçli seçimiyle, kimliğini artık gizlemiyor. Rıhtım meydanı (Renwick'in tahsildarlarının tam ortasında para topladığı an) buna tanıktı — balıkçılar, esnaf, sokaktaki herkes gördü. Çoğu "Shestendeliath" ismini tanımıyor ama ne gördüğünü anlıyor: gerçek bir Lord, gerçek bir hane, dönmüş. En az bir yaşlı tayfa ismi tanıdı, fısıldayarak tekrarladı. **Mother Vey de gördü** (dükkan penceresinden, fark edilmeden) — artık unvanı ve bağlantıyı kesin biliyor, kimseyle henüz paylaşmadı. Bu, eski "Gallowmere'de kimse unvanı bilmiyor" varsayımını geçersiz kılıyor — kasaba artık biliyor, ya da çok hızlı öğrenecek.
- **Eski durum (gün 81 - gün 103 arası, artık tarihsel):** Unvan sadece Hold'un hane halkına açıklanmıştı (session 17, büyük ziyafette Ilvaneth tarafından ilan edildi) — Roskel, Dallin Marsh, taşınan 27 asker, Alis Wend ve ailesi, Ser Kethrax, Maren/Dunnel Ashe, vb. Gallowmere'de kalan hiç kimse bilmiyordu.
- **Gallowmere garnizon darbesi (session 17, gün 75) kamuya görünürdü** (27 asker el değiştirdi, Kell kayboldu — kasaba bunu fark etmemesi imkânsız) **ama partinin bunu bizzat kimin/nasıl yaptığı hiç açıklanmadı** — sessiz, kimseyle konuşulmadan yapılan bir operasyondu. Mother Vey gibi biri "garnizon el değiştirdi, Kell gitti" bilgisine sahip olabilir, ama "Kriv ve Ilvaneth bunu yaptı" bağlantısını kurmuş olması gerekmez — bu bağlantıyı kurdurmak istersen bunu bilinçli bir DM kararı olarak yap, otomatik varsayma.
- **Dallin Marsh, gün 81'den beri Gallowmere'de DEĞİL** — tüm garnizonla Hold'a taşındı, Roskel'e bağlı. Gallowmere'de partiye bağlı hiç kimse kalmadı; oradan bir haber geliyorsa taşıyıcısı Mother Vey (ya da benzer bağımsız bir kaynak) olmalı, Dallin değil.

**Faction stances:**
- **Ashlord Concordat: ★★★★★ ÇÖZÜM YOLUNDA — Orell Tain'e devrediliyor (gün 192, session 33).** Sarelle öldü (gün 191). Solenne Kavash, Ashvale'e tek başına geldi (parti ile görüşmek için), Kriv'in tehdidini reddedip karşı çıktı — **Kriv tarafından öldürüldü (Intimidation 26 sonrası müzakere çöktü, savaşta infaz edildi).** Kavash'ın Baş Arşivci mührü + anahtarları parti elinde. **Orell Tain, aynı gün, Kriv'in ikinci bir Intimidation'ıyla (27) ikna edildi — Kavash'ın mührüyle sahte bir 'vekillik' belgesi hazırlayıp Karsgate Grand Archive'ını sessizce devralacak, Sarelle sadıklarını temizleyecek, partiye rapor verecek.** Karsgate/Emberhold şubeleri Sarelle'in VE Kavash'ın öldüğünü henüz bilmiyor — pencere hâlâ açık. Goal Tracker: `tain_takeover` (goals.json).
- Ironclad Compact: **koşullu ateşkes (gün 131, session 26 başı)** — Coren Ashvale, Thornlands'teki tırmanmayı sessizce durdurmayı kabul etti; karşılığında Concordat'ın bir sonraki hamlesi hakkında gerçek istihbarat istiyor. İki gün içinde Harrowgate'te Kriv'le yüz yüze görüşecek (Konsey toplantısından önce).
- Cinder Choir: fractured/unaware — Gallowmere hücresi yok edildi, üst kademe henüz tam bilmiyor

**GÜN 107 — The Unquiet Barrow, Elder Xorn YENİLDİ.** Kriv, Sethra'yı da yanına alarak (Hold'dan en fazla 1 gün uzaklaşma sözüyle) barrow'a döndü — House Doskarn Mührü (+1 AC, günde 1 Death Ward) Sethra'ya hediye edildi. Dış labirent yeniden düzenlenmiş ama iki gezici Xorn zaten ölü (session 16) — parti iz takibiyle hızlıca Oda 17'ye ulaştı, sonra Oda 18'in gerçek koruyucusuyla (Elder Xorn, HP 300, AC19, Legendary Resistance 2/gün) karşılaştı. Kriv+Sethra pusudan saldırdı, İlvaneth Blight+Wand of Magic Missiles kullandı — Xorn 2. round'da yarı canın altına düşünce Earth Glide ile kaçmaya çalıştı, Kriv'in fırsat saldırısıyla (doğal 20, kritik) 59 HP'ye kadar indi ama kaçmayı başardı. İlvaneth (Investigation 25) barrow'un haritalanmamış köklerinde onu buldu, parti peşinden gitti ve köşeye sıkışmış yaratığı bitirdi. **The Unquiet Barrow artık tamamen temizlendi** (session 16'dan beri açık kalan tek iplik kapandı). +1400 XP/kişi (Hard combat). Oda 18'in merkezindeki gerçek ödül (barrow'un tüm tasarımının amacı) erişilebilir hale geldi, henüz alınmadı/tanımlanmadı.

**Bilinen ama henüz gerçekleşmemiş (DM-only, dungeon sıralaması):**
- Vault of the Nameless'ın konumu ve mührün nasıl açılacağı zaten biliniyor (Kriv'in babası Lord Threxis'in adını söylemek — gerçek bir yas gerektiriyor, sahte yas işe yaramaz). İçeride isimsiz bir Ash-Warden mezarı var — **ikinci Ash-Warden evinin kimliğini** doğrulayacak (Tain'in görevi). **Crown parçası YOK burada** (düzeltme, session 20: gerçek fragman The Debased Mint'te — bkz. aşağı).
- **The Debased Mint** — Charge-Roll'un işaret ettiği GERÇEK fragman sitesi (`original-repo/.../locations/the-debased-mint.md`, tam gelişmiş 18 odalı dungeon, seviye 7-9, Ashvale kadar detaylı). House Doskarn'ın gizli mint'i — bir Crown parçasıyla görevlendirilmiş, gücü kötüye kullanmış, tüm aile ölü-doğaya dönüşmüş (Kriv'in Ascension'ına doğrudan ayna, hiçbir NPC bunu sözlü söylemeyecek). Boss oda (Room 18) aile reisinin (Baron Halvern Doskarn, artık Wraith) dönüşmüş hali, fragmanı ve mint'in servetini tutuyor. **Girişi bulundu, aktif keşif altında (session 21, gün 95)** — Riverside'da tabelasız bir depo, teslimat tüneli Oda 6'ya açılıyor. Temizlenen odalar: 6, 2, 5, 3, 4 (bkz. Active Quests). Sıradaki: Oda 7 (Private Stair) ve aile kanadı (Oda 8-17), sonra Oda 16 (Sanctuary — gerçek dinlenme noktası, Oda 18'den hemen önce) ve boss (Oda 18). **Oda 18 boss (Baron Halvern Doskarn, Wraith) session 21'de ayarlandı** — `burst_check.py --vs undead --target-hp 90` partinin tek-round nova hasarının (157.5 ort.) 90 HP'yi kolayca öldüreceğini gösterdi. Final stat: **HP 220**, **Legendary Resistance 2/gün** eklendi, temel Wraith aksiyonları (Life Drain +6, 4d8+3 necrotic, DC14 CON) korundu. Yarı canın altına düşerse Incorporeal Movement ile duvardan kaçmayı deneyebilir — gerçek bir kovalamaca/kapanma anı olarak oynanmalı, otomatik kaçış değil.

**Yeni açık iplikler (session 20 sonu):**
- House Varn'ın özel bahçesindeki aşırı korunan yan kapı — kimin/neyin korunduğu bilinmiyor. Ilvaneth'te kapının anahtarı var (çalıntı, fark edilmedi). Gece geç saatte kukuletalı bir ziyaretçi görüldü, kimliği bilinmiyor.
- **YENİ BAĞLANTI (gün 123/124, session 25 devamı) — Iron Sella Dray'in "Uzun Defter" karargahından çıkan kukuletalı bir ziyaretçi, parti tarafından takip edilip House Varn'ın aynı yan kapısına kadar izlendi** (Ilvaneth Stealth 21, Kriv Stealth 11 — Kriv'in adımı ziyaretçiyi bir an tedirgin etti ama fark edilmediler). Ziyaretçi elinde küçük bir deri çanta taşıyordu, kapı kimlik sorulmadan açıldı — bekleniyordu. **Sella'nın ağı ile House Varn/D.V. arasında olası bir bağlantı — henüz doğrulanmadı, parti bunun ne anlama geldiğini bilmiyor, sadece aynı motifi (kukuletalı, beklenen ziyaretçi) iki kez gördüler.**

**★★★ ÇÖZÜLDÜ, ÖLDÜ (gün 186, session 31) — Corbin Vayle.** Sarelle'in görevlendirdiği özel avcı — İlvaneth'in Ascension rüyası (Reyna Sorrel'in son anısı) onun Karsgate değil Emberhold'a yöneldiğini gösterdi. Hunter's Exchange'deki deposu bulundu (Kriv'in unvan kartıyla Deception 20), kişisel bir eşyası (eldiveni) alındı — bu, ikinci Scrying denemesini başarılı kıldı (Ashscar Sırtı'nda bulundu). Parti görünmez şekilde 60 fite yaklaştı; İlvaneth'in Dominate Person'ı Legendary Resistance ile savuşturuldu, ama Kriv'in Trip Attack + Action Surge nova'sı (6 saldırı) onu tek turda öldürdü, hiç tepki veremeden. **Loot: +1 zıpkın-mızrağı, 2 doz Sessizleştirici zehri, Concordat'ın mühürlü yetki belgesi (parti hedeflerinin "ölü ya da diri" teslimi için açık emir — somut kanıt), 187 gp, kişisel bir ejderha dişi.** +2.200 XP/kişi.
- **Reyna Sorrel — ÖLÜ (gün 184, session 30).** Gün 167'deki kukuletalı kurye, Sarelle'e hiç iletmediği sahte bir cevapla Kriv'i Sundered Garden'a çağırdı, Concordat'ın içindeki paranoyadan kaçıp sığınma istedi. Bilgi verdi (Ashvale garnizonu Restday gecesi yarı personelli, Solenne Kavash'ın şüphesi, Corbin Vayle) — sonra Kriv tarafından Breath Weapon ile infaz edildi. Concordat henüz kaybını fark etmedi.

**★★★★★ Gün 194 akşamı, session 34 — Reeks'te büyük kırılma: Ansel Drey ÖLÜ, Sunken Ledger tamamen yok edildi.** Wren Marrow'a düzenlenen suikast girişimi (3 suikastçı, biri canlı yakalandı-sonra infaz edildi) sorgulanıp Ansel Drey/Sunken Ledger'a kadar takip edildi. Kapıcı **Iona Crask öldürüldü** (Kriv'in zorla geçiş girişimi), ardından Drey'in deposuna girildi — Drey gerçek, somut bilgi verdi (kırık daire mührünün 15 yıllık ödeme geçmişi, Ironclad Table'dan ayrı bir gözetleme ajanı, "Whisper Court" adının bir efsane olarak varlığı) **ama işbirliği sonrası yine de öldürüldü** (İlvaneth'in Chain Lightning'i) — 6 muhafızı da öldü (3'ü teslim olduktan sonra infaz edildi). **Kasadan alınan:** House Corr/Sablewood/Ilvane'e karşı somut kanıt dosyaları, Drey'in 15 yıllık "sessiz iş" hesap defteri (en az 7 kırık-daire kontratı), mühür kalıpları, ~3.280 gp değerinde nakit/mücevher. **Bedel: bu artık geri dönüşü olmayan bir itibar kırılması** — Reeks'in tüm yeraltı ağı (Undertow dahil) bunun işbirlikçi bir simsarı bile korumadıklarını öğrenecek, gelecekte hiçbir bilgi kaynağı kolay güvenmeyecek (bkz. graph.json, `thread_reeks_massacre_reputation`). **Level 16'ya geçildi (ikisi de, aynı uzun molada işlendi) — Kriv +2 CHA (16→18), İlvaneth +1 WIS/+1 CHA (15→16/13→14).**

**★★★ Gün 195 sabahı, session 34 — "Aşkalkanı Emanet Şirketi" ipliği açıldı, Noter Ostrin Vell öldürüldü (parti gelmeden dakikalar önce).** Sereth'in katibinin sicil raporu, Wren Marrow'un depo senedini satın alan paravan şirketi ("Aşkalkanı") en az 5 ayrı mülk/borç devrine bağladı — biri bir **Chancellery katibinin ev senedi** (Grimwell'in de doğruladığı, kurumsal sızma kanıtı). Kefil noter Ostrin Vell'e gidildiğinde ceset bulundu (boğazı kesilmiş, dakikalar önce) — katil kaçarken İlvaneth (Winged Boots + Sleight of Hand 26) çantasını havadan kaptı, içeriğinde Vell'in özel notu: **"Gerçek talimat sahibi: Bayan V. (bkz. eski dosya, 1183 AR)"** + bir kırık daire mühür kalıbı + yarı yanmış bir sayfa ("Kingsward şubesi"). **Speak with Dead ile Vell'den alınanlar:** (1) katil sabah "Aşkalkanı hakkında kimse sizi ziyaret etti mi" diye sormuş, "henüz hayır" cevabı yeterli bulunmamış — düşman gerçek zamanlı izliyor, saatler içinde tepki veriyor. (2) Aşkalkanı 10 yıldır aktif, en az 12 mülk/borç, hep aynı örüntü (kırılgan bir hedef, borç satın alınır, baskı aracı olur), talimatlar hep "V." imzalı mühürlü mektupla, yüz yüze hiç değil. (3) Bir yıl önce bir Chancellery katibinin senedi de aynı yöntemle hızlandırılmış — **önceki noter de benzer bir işten sonra 10 yıl önce aniden emekli olmuş** (Aldous Penmark'ın dört-ev örüntüsüyle yapısal paralellik). (4) **"V." imzası yıllar önce KARSGATE'te de görülmüş** (Vell'in belirsiz hatırası) — kırık dairenin şehirler arası, çok eski bir ağ olduğuna dair ilk somut coğrafi bağlantı. (5) Şömine altında tam bir kopya arşiv + yatak odasında gizli servet (~900 gp + taşlar + kolye) alındı, hepsi parti elinde.

**NPC dispositions (Emberhold, gün 194, session 34 — YENİ):**
- **★★★ Wren Marrow (House Marrow'un varisi) — allied, himaye altında (gün 194, session 34, Veskin'in çeyreklik beyan toplantısı, Batı Bahçesi).** Cassian Ilvane'in yeni müttefiklerinden biri olarak sunuldu, ama Kriv'in doğrudan sorusu + Persuasion 23 ile gerçeği itiraf etti: üç ay önce ailesinin tahıl deposu senedi kimliği belirsiz biri tarafından satın alınmış, tehditle ("House Ilvane'in yanında dur, yoksa deponuz/kardeşinizin sözleşmesi gider") Cassian'a destek vermeye zorlanmış. Tehdit mektubu kırık-daire mührü taşıyor — Dorren Corr'un ölüm mektubu ve Rookery mektubuyla ÜÇÜNCÜ eşleşme, Whisper Court/Iskra Vantrel bağlantısı artık fiziksel kanıtla güçlendi (mektup parti elinde). **Kriv, House Marrow'u alenen himayeye aldı, 10 asker (Brynn'in çekirdeğinden, Sonnward garnizonunun 25'inden) Wren'in evine yerleşti (Sending Stone ile Halden'e emredildi, aynı gün).** Sonnward Promenade konağında geriye 15 asker kaldı. Cassian'ın koalisyonu herkesin önünde çöktü, kendisi de gerçekten habersiz görünüyordu (Iskra'nın bilmeden manipülasyonuyla tutarlı).
- **Lord Berengar Sablewood — borç ikinci kez ödendi, artık YENİ bir iyilik borçlu (gün 194, session 34).** Wren'in zorla ittifakına dair kanıtı karşılıksız verdi (Arnholt borcunun bir parçası olarak), ama parti bunu kullanınca ("Cassian'ın koalisyonu çöker") ayrıca bir iyilik daha borçlu kaldığını açıkça belirtti — gerçek bedeli olan, gelecekte tahsil edilecek bir iyilik.

**NPC dispositions (Emberhold/Ember Court, gün 202/203, session 35/36 — DÜZELTİLDİ session 36 yüklemesi):**
- **★★★★★★★ Lady Iskra Vantrel — İFŞA OLDU → AĞIR YARALI, KAÇTI (gün 202/203, session 35, Kesh Amara → The Ember Court).** Cinderday gecesi toplantısında pusuya düşürüldü, İlvaneth'in Draconic Transformation nefesi + Kriv'in Trip/Goading/Action Surge kombosuyla 2 round'da neredeyse yok edildi — hiçbir PC hasar almadı. Ama kalıcı ölmedi: rakshasa bedeni Kaal'ın kendi düzlemine (Ember Court, Oda 24 — Kor Beşiği) çekildi, birkaç saat içinde tamamlanacak bir reform sürecinde. Son sözü (Infernal, DM-only, ölmeden önce değil kaçarken duyuldu): "Kaal asla gerçekten ölmez, sadece bir süreliğine sabırsızlanır." Kesh Amara'daki mekânda bıraktığı kişisel eşyalar (savaş alanında bulundu): kırık daire + "K" harfli madalyon, House Sablewood/Corr'a yazılmış gönderilmemiş tehdit mektupları, 340 gp. **House Ilvane/Corr/Sablewood henüz haberi yok.**
- **★★★★★★ Sathriel (kıdemli rakshasa, Iskra'nın yoldaşı) — YENİ, AĞIR YARALI, KAÇTI (gün 202/203, session 35, Kesh Amara → The Ember Court).** Iskra ile aynı gece, aynı savaşta ağır yaralandı, aynı şekilde Ember Court'a çekildi — Oda 24'te, Iskra'yla birlikte reform halinde. Kaal hanesinin başka/daha kıdemli bir üyesi, adı sadece bu karşılaşmada öğrenildi. **Kaal Muhafızının Bileziği ve kırık Sözleşme Taşı henüz alınmadı — Oda 24'e ulaşıldığında (ya da onlar kalıcı yok edildiğinde) gerçek loot olacak.**
- **Ostwin Kade (Maro Veskin'in Chancellery kâtibi) — ÖLDÜ (gün 202/203, session 35, Kesh Amara).** Kesh Amara'ya kendi isteğiyle, "yeni taraf" adayı olarak gelmişti (yazman-imp'in tomarında adı yazılıydı) — İlvaneth'in nefes silahıyla anında öldü, kalıcı. Veskin'in bundan haberi yok, kâtibinin kaybolduğunu er ya da geç fark edecek.
- **★★★★★ Lord Cassian Ilvane: suspicious → GERÇEK MÜTTEFİK/BORÇLU (gün 198, session 35).** House Ilvane'in 20 yıllık danışmanı, "V." imzasının gerçek sahibi — kendi doppelganger'ı (Corwen kılığında) yakalanıp öldürüldü, gerçeği ortaya çıktı. Parti onu Dominate Monster'la yakalamadan hemen önce konaktan kaçtı (araba tuzaktı) — Scrying düşük seviyeli büyülere karşı hiç tutmadı, parti bunu D.V./Varn deneyimiyle birleştirip **rakshasa olduğu sonucuna vardı** (oyuncu bilgisi). Geride eldivenleri + "Kaal'ın Aynası" (Infernal yazıtlı, artık işlevsiz bir Abjuration koruma eşyası — "Kaal" ismi çözülmemiş) + üç hanenin sırlarını içeren dosyalar bıraktı. Muhtemelen kendi düzlemine Plane Shift ile kaçtı — konumu bilinmiyor, geri dönüşü kaçınılmaz.
- **★★★★★ Lord Cassian Ilvane: suspicious → GERÇEK MÜTTEFİK/BORÇLU (gün 198, session 35).** Kendi hanesinde 8 aylık bir doppelganger bulunması + en güvendiği danışmanının gerçek yüzü Kriv/İlvaneth tarafından ifşa edildi — derin bir minnet + travma. Kendi hanesini baştan aşağı temizliyor. Parti, Ilvane hanesinin kendi sırrını (dosyalardan biri) ondan sakladı — ittifak gerçek ama tek taraflı bir kaldıraçla dengelenmiş durumda.
- **Corwen (doppelganger, House Ilvane'in kapıcı başı kılığında) — ÖLÜ (gün 198, session 35).** Gerçek Corwen aylar önce öldürülmüştü, bu yaratık sekiz aydır yerini almıştı, Iskra'nın emriyle. Dominate Monster ile sorgulanıp (V.'nin kimliğini, kendi geçmişini itiraf etti) sonra öldürüldü.

**NPC dispositions (Emberhold, gün 182, session 30 — YENİ):**
- **Regent-Chancellor Maro Veskin:** unmet → tanıştılar, resmen mesafeli/yenilgiyle (gün 182) → **transactional/temkinli (gün 185, session 31).** Kriv, House Ashveil'da yakalanan 2 House Ilvane ajanını (Spymaster Elian Rook'un emriyle, gizli bir "sahte belge" ipucunu araştırmaya gönderilmişlerdi — İlvaneth'in Modify Memory tuzağının sonucu) bizzat Veskin'e bildirdi. Veskin kamuya açık bir suçlama istemedi — bunun yerine kendi adamı **Kâtip Freya Grimwell**'i (Kenku) sessizce Sonnward Promenade'a gönderip tutsakları kendi başına sorgulatmayı teklif etti, karşılığında Kriv'den konuyu şimdilik kimseye açmamasını istedi. Kriv kabul etti — Grimwell bu gece Sonnward'a gelecek. Veskin bu bilgiyi kendi kartlarından biri olarak saklıyor, açıkça belirtti.
- **★ YENİ AÇIK İPLİK (gün 185, session 31) — Spymaster Elian Rook ifşa oldu, henüz doğrudan karşılaşılmadı.** House Ilvane'in gizli operasyonlar şefi, iki ajanın itirafıyla adı geçti — kendi şüphesi olan, partiyle potansiyel müttefik olabilecek bir NPC (bkz. npcs-full.md). Freya Grimwell'in sorgusu sonucu bekleniyor.
- **Lord Cassian Ilvane:** unmet → **tanıştılar, itiraz geri çekildi ama "bugün için."** Sabırlı, gerçekten inanan bir tavırla "on beş yıl neredeydiniz" sorusunu sordu — kötü niyetle değil, House Ilvane'in "sadakat" doktrininden. Intimidation 28 karşısında resmi olarak geri adım attı, ama bu kalıcı bir teslimiyet değil — itiraz sadece bugün için askıya alındı, iplik açık.
- **★ Beat 1a TAMAMLANDI (gün 182) — Kriv resmen House Shestendeliath'ın koltuğuna oturdu, Wardensteel'in kilidi açıldı.** Bkz. Campaign Arc.
- **★ YENİ — Ember Quarter ortaklığı (gün 182, session 30, Sereth Corr ile).** İlvaneth 5.000 gp, Sereth (House Corr) 5.000 gp eşleştirdi — toplam **10.000 gp**, House Corr'un mevcut Ember Quarter yeniden-inşa tekeline ortaklık payı olarak. Amaç açıkça belirtildi: hem gerçek bir gelir hattı, hem de House Ilvane'in bölgede bir ekonomik ayak izi edinmesini fiilen engellemek. Beklenen getiri **~600-900 gp/ay** (inşaat ilerledikçe büyüyecek, henüz akmaya başlamadı — Karsgate Undertow/Darphane örneklerindeki gibi bir gecikme beklenir). Ayrıca: Kriv, Sereth'e siyasi destek sözü verdi (karşılığında önce bilgilendirilme şartıyla) — Emberhold'da artık House Corr'a görünür şekilde bağlı bir müttefik.
- **★ Kriv'in Emberhold mülkleri (gün 182, Ostmar Vell'den, Sereth'in önerisiyle):** Sonnward Promenade'da bir konak (1.550 gp) + Kingsward'da otuz yıldır boş, kayıtları eksik bir malikane (120 gp, Vell bile nedenini bilmiyor — açık bir iplik). Anahtarlar yarın teslim edilecek. 25 House Corr askeri (Brynn'in seçtiği çekirdek) üç gün içinde Sonnward konağına yerleşecek, Kriv'in komutası altında.
- **Sylandra Cael (lich, The Unfinished Circle lideri, Kule-i Mensuh):** unmet → conditional/test aşamasında → test tamamlandı → **★★★ TAM İTİRAF VE ORTAKLIK (gün 187, session 32, Ash Reeve'den çıkışta).** Kule-i Mensuh'un tamamen temizlenmesi (Warden öldürüldü, Mireille Osk özgürleştirildi, restricted spellbook alındı) sonrası Sylandra partiyi Ash Reeve'de bekliyordu. İlvaneth, Oda 17'de bulduğu notları ve kendi vardığı sonucu (Sylandra'nın phylactery'sinin de zorla alınan güç yüzünden çatlak olabileceği) SAKLAMADAN anlattı — Sylandra bunu doğruladı: **phylactery'si gerçekten çatlak, üç yüz yılın bir kısmı çoktan kayıp, bunu Circle'dan bile gizliyordu.** İlvaneth bunu onunla birlikte çözmeyi teklif etti, Sylandra kabul etti — **artık tam bir ortaklık: 'gönüllü verilen güç' ilkesini birlikte araştırıyorlar.** Magic Jar/Simulacrum/Clone'un üçünün de Sylandra'nın kendi geçmiş başarısızlıkları olduğu ortaya çıktı (Clone en yakınıydı ama yetersizdi). Kule-i Mensuh artık İlvaneth'e her zaman açık. **ALLIED.** **★ Düzeltme not (gün 187) — kanıt aslında çok önceden teslim edilmişti (gün 179/180, session 28); Live State Flags ve graph.json'daki eski "henüz teslim edilmedi" kaydı hatalıydı, düzeltildi.**
- **Ser Aldric Vane (House Corr'un mercenary kaptanı):** unmet → **friendly, gerçek bir borç.** Bir suikast girişiminde (yanlışlıkla o sanıldı) parti tarafından kurtarıldı, bilmeden. Emberhold'da kapısı açık, Sereth Corr'a bir kelime etmeyi teklif etti — Boş Koltuk için potansiyel bir giriş noktası.
- **Tobin Wrey (bağımsız kalıntı avcısı ekibi lideri, eski Compact subayı):** unmet → **allied, bilgi paylaşımı.** Rovan (ekibinden) üzerinden tanışıldı, Kar Vaelth (Sundered Reach) konusunda karşılıklı bilgi paylaşım anlaşması yapıldı — rekabet değil işbirliği.
- **Grand Archmagister Ebrim Voss (Kindled Circle'ın tüm ağının başı, Emberhold Grand Spire):** unmet → **tanıştılar, resmi/mesafeli.** Ilvaneth merkez şube üyesi oldu (100 gp aidat), Deception 16 ile Necromancy kökeni hakkında sorguyu atlattı (Voss şüpheci ama ikna oldu, 12 vs kendi Insight'ı). Sylandra Cael/Unfinished Circle ipucunu verdi, kendi Crown teorisini paylaştı.
- **★ Lady Sereth Corr (House Corr lideri, Emberhold):** unmet → **allied, gerçek destek sözü verildi (gün 176/177, session 27/28).** Kriv'i bahçesinde tek başına kabul etti, somut bir kanıt istedi — Kriv, Sparrow adlı bir Sessiz Defter/Silent Ledger ajanını (Cinder Bell'de Dominate Person ile yakalandı) ve ele geçirilen bir mektubu teslim etti. Mektupta **"Rookery"** (Reeks'teki eski tuzlama deposu, Sessiz Defter'in görev dağıtım merkezi, 3 gün sonra ödeme bekleniyor) ve çok daha kritik bir satır vardı: **"boş koltuğa yeni bir yüz geldi... Efendiler bunu zaten not etti"** — Kriv'in Boş Koltuk iddiası, kimliği bilinmeyen bir güç tarafından ÇOKTAN fark edilmiş. Sereth, Sablewood ya da Ilvane'in eli olabileceğinden şüpheleniyor ama emin değil. Karşılığında: koltuğa oturduğunda House Corr'un adamları + altını arkasında. Sparrow, Sereth'in hücresinde, Rookery'nin 3 gün sonraki ödemesi konusunda ayrıca konuşulacak.
- **★★★ Wrenna (Sereth Corr'un nedimesi) — YENİ (gün 179/180, session 28) — DOPPELGANGER, AÇIĞA ÇIKARILDI.** Gerçek Wrenna 2 yıl önce öldü, bu bir doppelganger — Whisper Court'a (Lady Iskra Vantrel'e) rapor veriyordu, dün geceki Rookery mektubunun kaynağı bizzat oydu (rutin bir raporu, kasıtsız). Sereth onu öldürmedi — artık **kendi kontrolünde çift ajan**, Iskra'ya ne söyleyeceğini Sereth belirliyor. Aynı zamanda House Sablewood'un kahyası **"Steward Arnholt"**'un da bir doppelganger olduğu öğrenildi (Wrenna'nın itirafı) — henüz kimseye açıklanmadı, DM+parti bilgisi.
- **★★★ "Kırık Daire" mührü — YENİ, BÜYÜK BAĞLANTI (gün 180, session 28, Eski Kışla).** Dorren Corr'un (Sereth'in ağabeyi, isyan gecesi ölen gerçek varis) huzura kavuşturulmasından önce verdiği itiraf: o gece, güvendiği biri sanılan bir kaynaktan sahte bir mesaj almış, kalabalığın en sakin değil en öfkeli kısmına yönlendirilmiş, bilerek yalnız bırakılmış. Mesajın mührü — **kırık bir daire, tam ortasından yarılmış** — bu sabahki Rookery mektubunun mührüyle AYNI. Bu, "Efendiler"in (Silent Ledger'ın gerçek efendisi, muhtemelen Whisper Court/Iskra Vantrel) en az 2 yıldır aktif olduğunu ve House Corr'un meşru varisini bilerek öldürttüğünü gösteriyor — Sereth'e henüz anlatılmadı. Dorren'in son ricası: Sereth'e sevgisini iletmek, onu asla suçlamadığını söylemek.
- **★★★ Lord Berengar Sablewood — YENİ (gün 180, session 28) — unmet → gerçek bir borç.** Parti, House Sablewood'a ilk ziyaretinde, kahyası "Steward Arnholt"ın 30 yıldır bir doppelganger olduğunu VE Berengar'ın sırlarını gizlice sattığını açığa çıkardı (Ilvaneth'in Detect Thoughts'u). Arnholt kaçmaya çalıştı, Kriv yakaladı, Berengar'ın kendi sorgusuna teslim edildi. Berengar artık partiye gerçek bir minnet borcu taşıyor — Kriv'in gelecekte bir karşılık isteyeceğini zaten söylemişti. Whisper Court artık House Sablewood içindeki gözünü kaybetti.
- **★★ Lady Iskra Vantrel / House Ilvane bağlantısı — SERETH'E GÖSTERİLDİ, GÜN 180 AKŞAMI (session 28, önceki bir sekmede oynandı — bu satır önceden yanlışlıkla "gösterilmedi" diye kayıtlıydı, düzeltme).** Parti, Rookery'de House Ilvane'in mührüyle mühürlenmiş, "V." imzalı bir mektup ele geçirmişti (gün 179/180, "Boş Koltuk meselesini bizzat takip ediyorum") — Wrenna'nın ifşasıyla birleşince Iskra Vantrel'e güçlü bir çizgi var. **Kriv, gün 180 akşamı mektubu Sereth'e gösterdi.** Sereth "V." = Iskra Vantrel bağlantısını hemen kurdu, aynı hafta gelen imzasız bir tehdit mektubuyla (farklı el, aynı konu) karşılaştırdı — kesin değil ama Iskra'nın elinin sandığından daha uzağa uzandığından şüpheleniyor. Mektubu (kısmen) saklamış olmaktan rahatsız oldu ama anlayışla karşıladı. **Üç gün geçti — Sereth bu bilgiyi gün 182'deki Veskin dinlemesine kadar düşünmeye vakit buldu**, bugün bunu nasıl kullanacaklarına dair kendi stratejisi olabilir. Gümüş saç tokası hâlâ Ilvaneth'te, henüz gösterilmedi/çözülmedi.
**★ Düzeltme (gün 187, session 32, oyuncu tespitiyle) — Shestendeliath Hold garnizonu artık ~42 asker, "15 asker" değil.** Eski rakam gün 104-110 dönemine aitti (Roskel Gallowmere'e giderken); o zamandan beri gün 110/125'teki hızlandırılmış asker alımı emirleri + gün 137-161 FF'deki büyük sıçrama (üç bölge toplamı ~92→127-145) Hold'un kendi garnizonunu da büyütmüştü, npcs.md hiç güncellenmemişti. Sethra hâlâ komutanları, Kethrax'ın ayrı ölü-doğa garnizonu bundan bağımsız.

**NPC dispositions (Chapter 1'den taşınan):**
- **Halworth (Konsey üyesi, sağ elinde iki parmağı eksik) ve Maren (Konsey üyesi) — İKNA OLDULAR (gün 133 gece, session 26, Garnizon Evi dinleme odası).** Renata'nın şartı yerine getirildi: Thorn'un tam itirafını (Intimidation 19 ile yalvarmadan gerçeğe zorlandı) bizzat dinlediler — Wyle Sarn, altın, Vorn suikastı, Islak Fıçı hanı, "Sessiz," ve Renlow'a yönelik plan. İkisi de artık yarınki Konsey oylamasında (gün 134) Kriv'i gerçek ağırlıkla destekleyecek. Halworth özellikle Islak Fıçı'yı tanıyor, Wyle Sarn'ın hâlâ orada olup olmadığını sordu — açık soru.
- **Magistrix Odalys Ferrant / The Kindled Circle — TANIŞTILAR (gün 125, session 25 devamı).** Ilvaneth gerçek adıyla üye oldu, askere alım kampı olayı hakkında sorgulandı, "self-defense" çerçevesiyle atlattı (Deception 25). Ilvaneth artık resmi Kindled Circle üyesi — tam arşiv erişimi, loncalı fiyat, üç büyük güce karşı koruma (50 gp/yıl aidat ödendi). Odalys'in şüphesi tam bitmedi, büyü imzası kayıtlarda Ilvaneth'le eşleşti — dikkatli bir gözlem altında.
- **"Lord Dorian Varn" / D.V. — ★★★ KİMLİĞİ ÇÖZÜLDÜ VE PAKT KURULDU (gün 124/125, session 25 devamı).** Parti, House Varn'ın gizemini takip edip (kukuletalı ziyaretçi → Sella Dray'in ağı → House Varn'ın yan kapısı) doğrudan Varn'la yüz yüze geldi. Arcana check'leriyle (21, 18) rakshasa olduğunu teşhis ettiler — Varn inkar etmedi, açıkça kabul etti. **Pakt:** Varn → parti: Ascension 3-4. evre bilgisi, Sarelle'in zayıflığı + kalan 2 fragmanın konumu (İmparator'un mühürlü lahdi, Ashvale'in en derin katmanı), House Shestendeliath'ın resmi tanınması (birkaç ay içinde, Penmark gibi ajanları üzerinden). Parti → Varn: belirsiz gelecek bir iyilik borcu. **Bu artık DM-only bir sır değil — oyuncular biliyor, ama dünyanın geri kalanı (Sarelle dahil) hâlâ hiçbir şey bilmiyor.** Tam detay `npcs-full.md`.
- **Coren Ashvale: neutral/sabrı tükeniyor → KOŞULLU ATEŞKES (gün 131, session 26 başı, Sethra + İlvaneth'in gece yarısı görüşmesi).** Sethra'nın dürüst itirafı (Compact'ın House Shestendeliath'ı yıktığını, kendi bilmeden 15 yıl hizmet ettiğini) + İlvaneth'in Deception 25'lik ustaca yön değiştirmesiyle, Coren Thornlands'teki tırmanmayı sessizce durdurmayı kabul etti — karşılığında Concordat'ın hamleleri hakkında gerçek istihbarat istiyor. **İki gün içinde (gün 133 civarı) Harrowgate'e gelip Kriv'le yüz yüze görüşecek**, Konsey toplantısından önce, minimum eskortla. Coren, İlvaneth'in muhtemelen aranan "elf" olduğunu biliyor/tahmin ediyor — kullanmayacağını söyledi ama bir borç senedi olarak tuttuğunu belirtti.
- Renwick Tale: unmet → **wary/professional, anlaşma yapıldı** (gün 103, Gallow's Anchor) — Kriv'in ültimatomunu kabul etti, rıhtım "düzenlemelerini" durdurdu, gelecekteki işleri önce Kriv'e bildirecek. Coren'e ne rapor edeceği belirsiz, muhtemelen Kriv'i test eden bir değerlendirme.
- Greyholt (köy, ~100 kişi altı) / Hallik (köy ihtiyarı, eski Shestendeliath kiracı torunu): unmet → **warming, gerçek bir söz verildi (gün 112, session 24)** — iki başarısız denemeden sonra Kriv'in dürüst çerçevesi ("içeriden bir hain," zorlamayan davet) Hallik'i ikna etti (Persuasion 20). Hallik hasat sonrası birkaç gün içinde yalnız başına Hold'a gelmeyi vaat etti — henüz gerçekleşmedi, ama gerçek bir randevu. Köyün geri kalanı hâlâ temkinli, karar vermiş değil.
- Aldous Penmark (Harrowgate Magistralık Ofisi yazmanı): unmet → **korkulu/işbirlikçi, tam itiraf verdi (gün 113, session 24)** — Kriv'in tek başına Intimidation 24'lük yüzleşmesiyle çöktü. Artık canlı bir tanık ve tehdit altında hissediyor; partiye karşı düşman değil, ama bir daha kimseye bir şey anlatacağından da emin değil. Mühür örneğini partiye verdi.
- "Iron" Sella Dray (Red Tally lideri, Karsgate/Warrens): unmet → **respectful/wary iş ortağı (gün 124, session 25 devamı)** — Kriv'in kimliğini (Lord Shestendeliath) ve gerçek leverage'ını (ordu + Gallowmere limanları) tanıyınca Ninefinger'a dokunmamayı kabul etti, karşılığında kendi malı için güvenli geçiş + ayrı pay anlaşması yaptı. Teslim olmadı, kendi gücünü hatırlattı — ama artık düşman değil, hesaplı bir iş ortağı. Warrens'ın en büyük çetesinin lideri şimdi partiye borçlu bir anlaşmayla bağlı.
- Doss (Ninefinger crew lideri, Karsgate): unmet → warming (gün 122, session 24) → **ALLIED — %50 pay ortaklığı kuruldu (gün 123, session 25 devamı, The Broken Wheel'de).** Kriv'in Persuasion 18'i ile anlaşma kapandı: Warrens'ın çalıntı-mal ağının yarısı (~350-400 gp/ay, Gallowmere ticaretiyle büyüme potansiyeli) partiye akacak — **şartıyla: önce Iron Sella Dray'e (Red Tally lideri) gerçek, somut bir güç gösterisi/mesaj verilmesi gerekiyor**, tercihen kan dökmeden ama bu partinin kararı. Doss ikinci bir jeton verdi (Ninefinger'a tanınma kanıtı). Ödeme, mesaj verildiğinde başlayacak.
- Yağmur Kesk (kalıntı avcısı): unmet → allied (geçici ortak, gün 115) → **DECEASED (gün 117, session 24)** — The Measure of Ash'i birlikte buldukları anda, Ilvaneth'in açık kararıyla ("50-50 dedik ama tek şey bulduk, sana bir şey kalmadı"), Kriv tarafından öldürüldü. On yıllık aramasının tam sonunda, hiç şüphelenmeden. Tanık yok, ceset vadide bırakıldı.
- Deacon Perrin Vask: unmet → yakalandı, sorgulandı (Detect Thoughts ile doğrulandı — dürüst cevap veriyordu) → **gün 103 akşamı, Gallowmere garnizon hücresinde, sorgu bittikten hemen sonra Kriv tarafından infaz edildi.** Sorgudan öğrenilenler: Sarelle'in avı fragman-odaklı + kişisel ölçüsüz bir takıntı; ikinci adamı artık **Solenne Kavash** (Tain'in yerine, 3 ay önce); Sarelle neredeyse hep Karsgate Grand Archive/Grey Hall'da; Concordat'ın bölgesel gücü ~200-300 yaşayan personel + ölü-doğa (Ashvale'de "küçük bir orduya yakın" garnizon); Sarelle içeride bir "sızıntı" olduğuna inanıyor, kendi hiyerarşisinden bile şüpheleniyor (sömürülebilir bir zayıflık); ve **artık DOĞRULANMIŞ bir gerçek (gün 113/114, session 24, Ilvaneth'in Ascension rüyası #8, Vask'ın ölüm anı)** — Sarelle'in Ashvale kazısı gerçekten İmparator ölmeden aylar önce başlamış, ve bunu Konsey'e yalan söyleyerek gizlemiş. **Kriv'e anlatıldı (gün 114) — ikisi de bilinçli olarak sakladı, "vakti gelirse" Orell Tain'e verilecek.** Gerçek bir Concordat-bölücü kaldıraç, hazır bekliyor. **YENİ (gün 133, session 26) — Kriv bu bilgiyi Coren Ashvale'e de doğrudan açıkladı, Tain'den bağımsız olarak; artık Coren da biliyor, ortaklaşa kullanımı henüz kararlaştırılmadı.** Draven Holt'u tanımıyordu, gerçek bir slaç değildi. Escortu (8 ölü-doğa muhafız) tamamen yok edildi, hiçbir tanık kalmadı — Concordat bu birimin sessizce kaybolduğunu er ya da geç fark edecek. Ceset garnizon hücresinde, imha/gömme kararı bekliyor. Esir taşıma arabası (büyü-bastırıcı ward'lı, muhtemelen partinin kendisi için hazırlanmıştı) yol kenarında terk edildi; kelepçeleri + sessizlik taşları alındı (bkz. Ilvaneth'in eşyaları).
- Vharkoss Shestendeliath: **ÖLÜ (gün 106)** — Sethra tarafından hücresinde bıçaklanarak öldürüldü, kardeşiyle (Kethrax) ve Kriv'le buluşmasından hemen sonra. Gerçek pişmanlık göstermişti ölmeden önce ("hak ediyorum" dedi, karşı koymadı). Sethra'ya yazıp hiç gönderemediği mektup hâlâ İlvaneth'te.
- Ser Kethrax: allied → **Vharkoss'un kardeşi olduğu ortaya çıktı** (gün 99) — 15 yıldır kendi kanından şüphelenmenin ağırlığını taşımış. Şimdi resmen zindan gardiyanlığını üstlendi, kardeşine karşı acı ama adil bir tavır sergiliyor.
- Roskel: allied, ama şu an **temkinli/sorgulayıcı** — Vharkoss'un kim olduğunu tam bilmiyor, sert tutuklama emrini sorgusuz uyguladı ama gözlerinde gerçek bir merak/endişe var.
- Ferrin (Vharkoss'un genç muhafızı): **ÖLÜ** — Kriv tarafından uykusunda öldürüldü, gün 96/97 gece, Kingsward-Hold yolunda. Karsgate'te bir kız kardeşi olduğu biliniyor (Vharkoss'tan).
- Orell Tain: kurtarıldı, fugitive, Hold'da ağırlanıyordu → **Ashvale operasyonuna Sethra/Ressa ile bizzat katıldı (Munitions Store sabotajı, gün 191, session 32)** → **★★★ gün 192, session 33 — Concordat'ın yeni fiili başı olarak kuruldu.** Kriv'in teklifine önce şartlı/temkinli yaklaştı, ikinci bir Intimidation'la (27) tam ikna oldu — "karşınızda olmak istemiyorum" dedi, ama gözlerinde eski bir şey sönmedi. Kavash'ın mührüyle Karsgate Grand Archive'ını sessizce devralacak, Sarelle sadıklarını temizleyecek, partiye rapor verecek — ama Crown hakkındaki kendi vicdanına göre hareket edeceği konusunda açıkça uyardı (bkz. Goal Tracker `tain_takeover`).
- Sethra Shestendeliath: unmet → **GÜN 104, Gallowmere garnizon komuta odasında bulundu, tanındı ve kabul edildi; artık PARTİYLE BİRLİKTE, Hold'a vardı (gün 106).** Kriv aile yüzüğünü (Shestendeliath Mührü), Wardensteel'i ve çocukluktan bir hatırayı (kırık kanatlı tahta ejderha oyuncağı, Sethra'nın "tren" sandığı) kanıt olarak gösterdi — kabul etti, sarsıldı, sarıldılar. **Ironclad Compact'tan RESMEN İSTİFA ETTİ** (yazılı mektup, kendi eskortuyla Coren'e gönderildi, gün 104) — artık hizmette değil, Lady Shestendeliath olarak evine döndü. Yol boyunca (Gallowmere→Hold, gün 104-106) Kriv ona geçmişini anlattı: yetimhane, İlvaneth, Sarelle'in ihaneti, dört evin aynı örüntüyle düşmesi, ve **Compact'ın (yani 15 yıl hizmet ettiği kendi kurumunun) evi bizzat yıkan sözleşmeli el olduğu gerçeği** — Sethra bunu öğrenince donakaldı, Coren'e son güven kırıntısını da kaybetti. **Ashen Crown/parçalar konusuna hiç girilmedi, kasıtlı olarak gizli tutuluyor.** **GÜN 107 akşamı, karar:** Kriv, Sethra'ya Hold'un Leydisi olarak kalıp yönetmesini önerdi — Roskel'le birlikte, çatışmasız (o Yüzbaşı, o Leydi). **Kabul etti.** Kendi payına: Coren'i/Compact'ı tanıdığı için gerçek bir istihbarat kaynağı olacağını, Kriv+İlvaneth'in evi yıkanların peşine düşmesini bekleyeceğini, kalede gerçek bir güç (ordu, isim) inşa edeceğini söyledi. **Yeni bir söz verildi: eve zarar verenler bulunacak ve yok edilecek** (Concordat/Draven Holt/Sarelle hattı, Compact/Coren hattı dahil) — bu artık hem Sethra hem Kriv/İlvaneth için ortak, açık bir hedef.

**Roskel planı DEĞİŞTİ (gün 107 akşamı) — session 22'nin "gençler Hold'a gönderilecek, Roskel eğitecek" planının yerine geçti:** Kriv, Roskel'i Gallowmere'e gönderiyor — Dallin tek başına kasabayı ve yeni asker eğitimini taşıyamaz, Roskel'in deneyimi orada gerekli. **Hold'da Sethra'nın yanında kalan: 15 asker, doğrudan onun komutasında** (Kethrax'ın ayrı ölü-doğa garnizonu değişmedi). Sethra, gitmeden önce Roskel'le konuşup devir teslim yapmak istiyor — henüz gerçekleşmedi.

**GÜN 106, Hold'da:** Kethrax'la (kardeşiyle aynı yüzü paylaşan wight muhafızla) 15 yıl sonra yeniden karşılaştı — onu tanıdı, kısa ama gerçek bir an yaşandı. Sonra Vharkoss'la yüzleşti, zindanda; Kriv bilerek karışmadı. Kontrolsüz bir öfke anında Vharkoss'u bıçakla öldürdü — Kriv'in "yaşasın, her gün ölsün" planını bozan, tamamen kendi kararı. Şu an ağır bir duygusal çöküş içinde, zindanın taşında diz çökmüş. Vharkoss'un ona hiç gönderilmemiş mektubu henüz verilmedi (İlvaneth'te).
- Corla Vint: unmet → tanışıldı, neutral/professional — jeton doğrulandı, iş teklifleri sunuldu (Ninefinger fence %15, Gallow's Rest önerisi), 5 gp bahşiş verildi.
- Orvenna Kest: neutral/habersiz → tanıdı, professional — "elf+dragonborn" tarifini ücretsiz uyarı olarak paylaştı; Kessra'ya mesaj teklifini (50 gp ya da açık borç) reddettiler.
- İsimsiz Concordat arşivcisi (Wagered Crown, sivil kıyafetli saha ajanı): Ilvaneth'in yüzünü akılda tuttu (iki büyük kazanç sonrası "ilginç yüz" olarak not aldı) — henüz "elf+dragonborn" tarifiyle bağlantı kurmadı (sadece Ilvaneth'i, yalnız, gördü). Kriv'in yanında görürse bağlantı kurabilir.
- Mother Vey: **friendly, kararını verdi (gün 110)** — "bir risk değil, bir bahis." Unvanı açıkça kabul etti ("Lord Shestendeliath" dedi, yüzüne karşı, ilk kez). Tehlikeyi de düzeni de görüyor, ikisini de dengeli değerlendiriyor — kayıtsız şartsız müttefik değil ama artık düşman da değil.
- Fennick Orle: friendly, ve şimdi Ilvaneth'e doğrudan mektup yazacak kadar samimi (gün 99) — güçlü bir bilgi ağı var, garnizon darbesinin partinin işi olduğunu muhtemelen çözmüş (açıkça söylemedi, laf arasına sıkıştırdı: "o garnizonun tam olarak nasıl el değiştirdiğini hâlâ kimse bana anlatmadı... bazı şeyleri sormamak bir sanattır"). Renwick Tale'in Gallowmere'i ekonomik olarak ele geçirdiğini bedava haber verdi, ama açık uçlu bir iyilik borcu bıraktı ("bir dahaki sefere bir iyilik isteyebilirim, ne olduğunu şimdiden söylemeyeceğim") — kullanılmamış, gelecekte geri gelebilir.
- Sefwyn Marrow: **warming → tam ortak, kendini gerçekten riske attı** — gün 96 akşamı Tain'in kurtarılmasında bizzat yer aldı: borçlu bir nöbetçiyi ayarladı, kaçış arabasını sürdü, üç cesedi nehre attı. Görülseydi Concordat'la ilişkisi tamamen biterdi, bunu bilerek göze aldı. Artık partiyle kalıcı olarak bağlı — kendi deyimiyle, yakalanırsa "geriye tek yol kalır: sizinle." Talyn Ambrose adlı bir Concordat saha ajanını da isim olarak verdi (şüpheyi çekmek için, henüz kullanılmadı).
- Corran: good — güvenilir müttefik
- Corvin Thale: wary — takıntılı, gelecekte risk
- Sylvenna: friendly — kullanılmamış kaldıraç (3 faction'ın kuruluş sırları)
- Roskel: allied — Gallowmere'in Yüzbaşısı
- Nairne Thistle: warming — Session 19'da kazanıldı
- Kessra Vane: allied — fencing ortaklığı

**Yeni bilgi (gün 96/99, Vharkoss itirafı + Grey Hall):**
- Kriv'in evinin yıkımını Concordat sipariş etti (Compact sadece sözleşmeli işi yaptı) — Vharkoss'un doğrudan tanıklığı.
- İçerideki aracının adı: **Draven Holt** — insan, 15 yıl önce orta yaşlı, kimin adına çalıştığını söylemedi. Vharkoss'un sakladığı mühürlü mektup (Concordat kurye mührü, çift anahtar+kitap motifi) partide, henüz kimlik tespiti yapılmadı.
- Aynı ay dört Ash-Warden evi düştü, hepsi aynı imza zinciriyle (Tain'in defteri) — Draven Holt da "siz ilk değilsiniz, son da olmayacaksınız" demiş, sistematik olduğunu doğruluyor. **Üçüncü ev artık isimlendirildi: House Ostrel** (Ilvaneth'in 5. rüyası, gün 99, Hold'da uzun mola) — konum/detay yok, sadece isim. İki ev (Shestendeliath, Doskarn) biliniyor, House Ostrel üçüncü, dördüncüsü hâlâ isimsiz.
- Sethra Shestendeliath masum — o gece evde değildi, hiçbir şey bilmiyor, 15 yıldır Vharkoss'u şüpheyle arıyor. Vharkoss ona yazdığı ama göndermediği bir mektup taşıyordu (parti şu an elinde tutuyor, gönderilmedi).
- **Yeni tehdit — halka açık ödül ilanı:** Kingsward-Hold yolunda bir kavşak türbesinde imzasız, ödüllü bir "elf+dragonborn" ilanı bulundu (gün 96/97) — tarif artık Concordat'ın özel bilgisi değil, açık bir ödül avı. Kriv yırttı ama tek kopya olması olası değil.

**Bilgi/sır durumu (DM-only, oyunculara açıklanmadı):**
- Hollow Prophet'in gerçek kimliği: Ilyra Thorne. **⚠ KRİTİK BAĞLANTI (gün 113, session 24) — oyuncular bu ismi artık BİLİYOR ama Hollow Prophet ile bağlantısını bilmiyorlar.** Penmark'ın kayıtlarından, House Ostrel'in Cindermoor'daki malikanesini 10 yıl önce satın alan kişinin adının "Ilyra Thorne" olduğu öğrenildi (bkz. Active Quests) — bu bilerek yapılmış bir plant, oyuncular şu an bunu sadece "yalnız yaşamak isteyen gizemli bir kadın" olarak biliyor. Asla açıkça bağlantı kurma ("bu Hollow Prophet!" deme) — organik olarak, parti Ostrel malikanesini ziyaret edip Ilyra Thorne'la karşılaşırsa ya da başka bir ipucu bu ikisini birleştirirse ortaya çıksın. Bu, Chapter 1'in en büyük gizli ödüllerinden biri olabilir.
- Kriv'in evinin yıkımı — üç suç ortağı katmanı: Ironclad Compact (uyguladı, Coren biliyor), Vharkoss (içeriden ihanet), Ashlord Concordat (sipariş etti, Sarelle biliyor).
- Ashen Crown'un tam birleşme sonucu: ya "yeniden doğar" ya birleştireni küle çevirir.
- Ilvaneth'in annesinin akıbeti: kasıtlı olarak tanımsız, canlı bir hook.
- Kim Kriv'in evini yıktığının TAM resmi: Chapter 2'ye kadar kasıtlı olarak tam çözülmüyor.

## Campaign Arc
```yaml
type: dynamic
arc_number: 2   # "Chapter 2: The Hollow Throne" (level 11-20)
generated: "2026-09-11 (session 26, oturum-dışı tasarım çalışması, reference/chapter-2-outline.md'den uyarlandı)"
revised: null

theme: "İki insan hiçbir zaman birbirlerine yalan söylemeyeceklerine yemin etti — ama gücün kendisine karşı aynı disiplini göstermediler. Sınırsız güç istediler, ve dünya bunun bedelini ödeyecek."
resolution: "★★★ REVİZE EDİLDİ (2026-09-18, session 33, oyuncu talebiyle — bkz. altta 'Session 33 revizyonu'). Kriv/İlvaneth'in yapısal çatışması (ayrı tutmak vs birleştirmek) OYUNDA ORGANİK OLARAK ÇÖZÜLDÜ — Kriv, İlvaneth'in gücünün kendisine somut kazanç (unvan, topraklar, ordu) getirdiğini görüp tam destek veriyor, ayrı tutma mirasını umursamıyor. Gerçek çatışma artık ikisi arasında değil, dünyayla: tacın tamamlanması, panteonun bastırılmış/silinmiş yedinci tanrısı **Ashborn**'u kısmen serbest bırakıyor. Final artık 'hangi seçimi yapacaklar' değil — **iki Evil karakterin, kurdukları her şeyi (ordu, unvan, birbirlerine bağlılıkları) bir tanrıya karşı gücü ELDE TUTMAK için kullanıp kullanmayacağı.** Kazanırlarsa: gerçek bir apotheosis, bir kurtuluş değil bir fetih. Kaybederlerse: dünya kalıcı, karanlık bir şekilde değişir."

# ★★★ Session 33 revizyonu — tam detay, DM-only, oyunculara asla açıklanmadan:
# Ashborn: panteonun (Ember Sovereign, Vesna, Old Harrow, Vaelkyr, Correlan, Threnody) yedinci, kasıtlı silinmiş üyesi.
# İlk kül-krallar gerçekte ONA hizmet ediyordu. Ember Sovereign'ın ortodoksisi onu bastırdı, tarihten sildi.
# Ashen Crown, bir yas-kalıntısı DEĞİL — Ashborn'un gücünün bir parçasını hapseden bir MÜHÜR, "The Reckoning"de
# (dünyanın kendi takvim sıfır noktası) zorla parçalanmış. Her fragman o gücün bir kırıntısı.
# Kriv/İlvaneth'in Ascension'ları bilmeden bu sızıntının bir yansıması.
# Tamamlanınca: Ashborn kısmen serbest kalır (tam değil) — avatarı + dünyanın her yerinde aynı anda uyanan
# eski kül-kral lejyonları (undead, kül-zırhlı, kendi eski hanedan topraklarını "geri talep ediyor").
# D.V./rakshasa bağlantısı (opsiyonel, güçlü bir olasılık): Draven Holt/dört ev yıkımı hep Ashborn'un
# dönüşünü hazırlıyordu, D.V. bilerek ya da bilmeden bir araçtı — geriye dönük bir anlam kazanabilir.
# Çözüm mekaniği (ONAYLANDI): İKİ CEPHE AYNI ANDA.
#   (1) Dünya cephesi — Kriv'in kurduğu siyasi/askeri ağ (Hold garnizonu, Gallowmere, Harrowgate,
#       Coren'in Compact güçleri, Sereth'in House Corr askerleri) kül-kral lejyonlarına karşı gerçek,
#       kaybedilebilir cepheler tutuyor — zaman satın alıyor. 30+ oturumluk imparatorluk-kurma yatırımının ödemesi.
#   (2) Kişisel cephe — asıl final. Ashborn TAM dönmedi, sadece bir avatar/kırıntı, gücü toplamaya çalışıyor.
#       Kriv + İlvaneth, kendi Ascension'larının zirvesinde, avatarla GÜCÜN SAHİPLİĞİ için çarpışıyor —
#       onu kovmak değil, gücü ONDAN ÇALMAK. Kazanırlarsa tacın gücü nihayet gerçek sahiplerini buluyor
#       (kalıcı, geri dönüşsüz apotheosis — Ascension'ın "Beyond" tier'i, artık gerçek bir son durum).
#       Kaybederlerse Ashborn tam döner, gerçek bir kötü son.
# ★ Apotheosis detayları (2026-09-18, session 33, onaylandı) — reference/ascension-tracks.md'nin her iki
# karakterin de "Beyond" bölümünde tam yazılı: İlvaneth tacın kendisiyle birleşip kırılmaz bir ölümsüzlüğe
# ulaşıyor (hafızası tamamen erime bedeliyle, artık tek bir benlik değil). Kriv gerçek bir ejderhaya
# dönüşüyor, Wardensteel bedeniyle birleşiyor (hazine/insan ayrımı tam kayboluyor bedeliyle — İlvaneth
# artık kelimenin tam anlamıyla onun hazinesinin bir parçası). İkisi de kendi istediklerini tam alıyor.
# 2a (Umm-Halad) artık bu gerçeğin İLK KIRINTISINI veriyor — isim vermeden ama gerçek bir dehşetle uyarıyor.
# Parti muhtemelen (Evil, güç-odaklı karakterler olarak) bu uyarıyı göze alıp reddedecek — bu BİLİNÇLİ bir
# seçim olarak oynanmalı, final "bilseydik yapmazdık" olamayacak şekilde kurulmalı.
# 2b (Ser Oskar Thrune) — KESİN KURAL: müzakere yolu YOK. Thrune, tacı ilk kıran muhafızların yemin
# mirasçısı — parça istenirse DOĞRUDAN SALDIRIR, hiçbir anlaşma/ikna girişimi işe yaramaz. Sadece combat
# ile alınabilir, doktrine uygun gerçek bir boss fight (mummy lord, Bonewrights' Hall).

acts:
  - act: 1
    title: "Emberhold (seviye 11-14)"
    drive: "Ne inşa ettiklerine karar vermek — siyasi bir güç olarak hayatta kalmak"
    beats:
      - id: "1a"
        # ★ "Sponsor at court" — dört yol da geçerli, hiçbiri önceden seçilmedi (Standard 10):
        #   1) Sereth Corr — sponsor olur, karşılığında açık/örtük destek bekler; Kriv "Corr'un adamı" olarak okunur.
        #   2) Berengar Sablewood — tamamen transaksiyonel, somut bir bedel (altın/kaynak/kontrat avantajı) ister.
        #   3) Cassian Ilvane — sponsor olur ama gerçekte Iskra Vantrel yönlendiriyor; Kriv bilmeden Whisper Court'a bağlanmış olabilir, gecikmeli bir komplikasyon.
        #   4) Maro Veskin — hiçbir haneye borçlanmadan, Freya Grimwell'in kanıtıyla zorlanarak; Veskin'i kalıcı, gizli bir düşman yapar.
        #   Ne olursa olsun sonuç: koltuk resmen geri verilir, Kriv artık tanınmış bir hane reisi.
        #   Parti hiçbirine gitmezse: koltuk boş kalır, Kriv tanınmamış bir dışarıdan kalır — bu da geçerli bir sonuç, "meşruiyet gerçek mi" temasına hizmet ediyor, zorlanmıyor.
        #   ★ D.V./sponsor ilişkisi netleştirildi (2026-09-11): D.V.'nin sözü (session 25, "birkaç ay içinde hane resmen tanınacak") SADECE mahkumiyetin/lekenin kaldırılmasıdır — hukuki bir ön koşul, pasif, Kriv hiçbir şey yapmasa da gerçekleşir. Beat 1a'nın "sponsor" süreci AYRI ve SONRAKİ bir adım: hanenin lekesi kalkmış olsa bile, Kriv'in bizzat koltuğa oturması hâlâ sponsor + kanıt sunumu gerektirir. Emberhold'a varış süresi (~12-14 gün + seviye 11'e ulaşma süresi) muhtemelen D.V.'nin "birkaç ay"ının içine denk geliyor — yani parti vardığında mahkumiyet muhtemelen ZATEN kalkmış olacak, "hane kanıtı" tartışmasız hale gelecek, geriye sadece sponsor + fiilen oturma kalacak.
        #   ★ Wardensteel kilidi (2026-09-11, oyuncu onayıyla): Kriv'in house blade'i (Wardensteel, şu an sadece +1) tam bir Flame Tongue'a (+2d6 fire) dönüşme koşulu ("gerçekten haneyi geri almak") artık somut: D.V.'nin sözü + Hold'un restorasyonu sadece ön koşul, GERÇEK kilit açma anı Kriv'in beat 1a'yı tamamlayıp koltuğa fiilen oturduğu an. Bkz. characters/Kriv Shestendeliath.md.
        label: "İki Miras — Boş Koltuk ve Bitmemiş Çember"
        what_changes: "Parti artık isimsiz dışarıdan biri değil — kamuya açık, gerçek, isimli düşmanları olan bir siyasi oyuncu (Kriv'in seçimi: House Shestendeliath'ın askıya alınmış koltuğunu talep etmek ya da etmemek). AYNI ANDA, EŞİT AĞIRLIKTA: İlvaneth, kendi arayışının (hiçlik olmamak) yüzyıllardır süren bir mesleki gelenek olduğunu keşfeder — The Unfinished Circle, Sylandra Cael. İkisi de artık kendi 'hanesiyle' yüzleşiyor, biri kanla, diğeri ustalıkla kazanılan."
        world_pressure: "Kriv için: Sarelle'in 15 yıllık dosyası + mahkemenin meşru bir Ash-Warden varisinin konuşmasını bekleyen siyasi baskısı. İlvaneth için: Kindled Circle'ın merkez şubesindeki bir kayıt/söylenti, onu Kule-i Mensuh'a yönlendirir — tesadüf değil, kasıtlı bir keşif."
        status: complete  # ★★★ TAM KAPANDI (gün 182, session 30, Hollow Throne). İLVANETH TARAFI: session 28'de Sylandra'ya kanıt teslim edildi, tam güven kazanıldı. KRİV TARAFI: House Ilvane (Cassian Ilvane) Chancellery'e resmi itiraz sundu (kayıt-uzmanı gerekçesiyle dinlemeyi geciktirmeye çalıştı) — Sereth Corr'un desteğiyle antechamber'da doğrudan yüzleşildi (Persuasion 26, Corr Bıçağı avantajıyla), Veskin dinlemeyi hemen açmak zorunda kaldı. Hollow Throne salonunda Kriv resmen beyan verdi, Cassian'ın "on beş yıl neredeydiniz" sorusuna karşı sert bir cevap + Intimidation 28 ile geri adım attırdı (itiraz "bugün için" geri çekildi — kalıcı değil). Veskin resmen koltuğu tanıdı, Kriv House Shestendeliath'ın banka'sına fiilen oturdu — **Wardensteel'in kilidi açıldı, kalıcı/slot-dışı attune oldu** (tam "Uyanış" formu: +2 atak/hasar, +2d6 fire, Draconic Wrath, Warden's Aegis). +3400 XP/kişi (hard noncombat). Yan ürün (session 28'den): Wrenna+Arnholt (Whisper Court doppelganger'ları) ifşa edildi, Berengar Sablewood'un borcu kazanıldı, Dorren Corr'un ölüm sırrı çözüldü.
      - id: "1b"
        label: "Sarelle'in Teklifi"
        what_changes: "Tarafsızlık illüzyonu biter — ikisi de artık Crown'un gerçek, kişisel bedelini biliyor, soyut bir tehdit olmaktan çıkar."
        world_pressure: "Sarelle'in doğrudan, cömert teklifi — Grand Archive'daki kanıt (İmparator'un ölümü) hem havuç hem kırbaç olarak"
        status: complete  # ★★★★★ TAM KAPANDI, MAKSİMUM ŞİDDETLE (gün 191, session 32). Sarelle'in world_pressure'ı (doğrudan teklif) teslim edildi (gün 187) — ama parti teklifi bir tuzak olarak okuyup reddetti, doğrudan bir saldırı planladı (Coren'in diversion'ı + Chalk Warrens sızması). Sarelle'in Sanctum'unda yüzleşildi: İlvaneth'in Command Undead'i kaçış yolunu kapattı, Kriv'in Action Surge novası (219 hasar, 1 round) onu prone/çaresiz bıraktı, İlvaneth'in Disintegrate'i (83 hasar, 69 HP'lik hedefe) onu tamamen toza çevirdi. **what_changes fazlasıyla gerçekleşti** — "tarafsızlık illüzyonu"nun ötesine geçildi, tehdit artık soyut değil TAMAMEN ORTADAN KALKMIŞ durumda. The Working Archive (İmparator'un suikast kanıtı) + son 2 Crown parçası ele geçirildi, parti artık 7/9 parça taşıyor. **CHAPTER 1'İN GERÇEK KAPANIŞI.**

  - act: 2
    title: "The Sundered Reach (seviye 15-17)"
    drive: "Kalan parçaları bulmak, Crown'un gerçek bedelini öğrenmek"
    beats:
      - id: "2a"
        label: "Kabın Gerçeği"
        what_changes: "Crown'un gerçek doğası artık soyut lore değil — sadece bir güç kabı değil, adı anılmayan bir şeyin MÜHÜRÜ olduğuna dair ilk gerçek uyarı. Parti bu uyarıyı duyar ama muhtemelen bilerek göz ardı eder — final 'bilseydik yapmazdık' olamaz, bu bilinçli bir seçim olarak kayda geçmeli."
        world_pressure: "Umm-Halad'ın (Kar Vaelth'in taş dev kahini) tanıklığı — isim vermeden (kendisi de bilmiyor/söylemiyor) ama gerçek bir dehşetle: tacın içinde hapsolmuş bir şey var, ve birleştirmek onu serbest bırakabilir."
        status: pending
      - id: "2b"
        label: "Bonewrights'in Yemini"
        what_changes: "Tacın neden kırıldığının gerçek tarihi ortaya çıkıyor — sadece bir kralı durdurmak için değil, kazayla serbest bırakılmaya başlanan bir şeyi yeniden mühürlemek için. **Ser Oskar Thrune bu yemine bağlı — müzakere yolu YOK, parça istenirse doğrudan saldırır.**"
        world_pressure: "Ser Oskar Thrune, Wardensteel'i tanır, Kriv'i adıyla çağırır, gerçek tarihi anlatır — ama bu bir pazarlık değil, bir savaş ilanı. Son parça sadece combat ile alınabilir (mummy lord, doktrine tam uygun boss fight, Bonewrights' Hall)."
        status: pending

  - act: 3
    title: "The Grey Kingdom (seviye 18-20)"
    drive: "Serbest kalan gücü elde tutmak — bir tanrıya karşı"
    beats:
      - id: "3a"
        label: "Serbest Kalış"
        what_changes: "Tac tamamlanır tamamlanmaz, dünya değişir — hiç gecikme, hiç ima (2a'nın belirsiz uyarısı dışında). Ashborn (panteonun silinmiş, yedinci tanrısı) kısmen serbest kalır; avatarı + dünyanın dört bir yanında aynı anda uyanan eski kül-kral lejyonları sahneye çıkar. Parti artık sadece güçlü değil, bir tanrı-adayının doğrudan hedefi."
        world_pressure: "Son parçanın yerine oturduğu an — kaçınılmaz, gerçek bir kataklizma. Gökyüzü değişir, kül-kral lejyonları dünyanın her yerinde aynı anda ayaklanır."
        status: pending
      - id: "3b"
        label: "Fetih"
        what_changes: "Kampanyanın gerçek finali, iki cephe aynı anda: (1) Kriv'in kurduğu siyasi/askeri ağ (Hold, Gallowmere, Harrowgate, Coren'in Compact güçleri, Sereth'in House Corr askerleri) kül-kral lejyonlarına karşı gerçek, kaybedilebilir cepheler tutup zaman satın alıyor. (2) Kriv + İlvaneth, Ascension'larının zirvesinde, Ashborn'un avatarıyla GÜCÜN SAHİPLİĞİ için çarpışıyor — kovmak değil, çalmak. Kazanırlarsa: kalıcı, geri dönüşsüz bir apotheosis — kurtuluş değil fetih. Kaybederlerse: Ashborn tam döner, dünya kalıcı ve karanlık şekilde değişir."
        world_pressure: "Kendi Ascension'larının zirvesi + Ashborn'un aç, sabırsız gücü — düello kaçınılmaz, sonucu oyunda belirlenecek."
        status: pending

current_act: 2  # ★ Act 1 tamamen kapandı (1a + 1b), gün 191, session 32 — Sarelle öldü, Ashvale düştü. Act 2'ye (The Sundered Reach) geçiş açık.
current_beat: "2a"

# ★ gün 194, session 33 — Ivrathax'tan (Frostmere) 8. Crown parçası SAVAŞSIZ alındı (Persuasion 23, "kardeşlik ittifakı").
# Bu resmi bir beat değil (2a/2b'nin ikisi de hâlâ pending) ama Act 2'nin "parçaları topla" drive'ını ilerletti — parti artık 8/9.
# Son parça (9.) Ser Oskar Thrune'da, Bonewrights' Hall'da (beat 2b'nin de mekânı) — 2b'ye gidildiğinde otomatik tetiklenecek.
# Kar Vaelth/Umm-Halad (beat 2a) hâlâ ziyaret edilmedi, bir ipucu (dikili taş) elde.

outstanding_beats:
  - "2a"
  - "2b"
  - "3a"
  - "3b"

steering_notes: >
  ★ Kışkırtılma hesabı (2026-09-11, session 26, oyuncu düzeltmesiyle son hali) —
  reference/chapter-2-consequence-calculus.md: Chapter 1'in "B senaryosu"
  mantığı Chapter 2'nin tüm önemli aktörlerine (Sarelle, Veskin, üç hane
  reisi, Iskra/Whisper Court, Ilse Drummel, yeraltı liderleri) sistemli
  uygulandı. **Chapter 2'nin kendi A/B senaryo çatalı, Chapter 1'in eski
  aktörleri (Coren/Sarelle) üzerine değil, YENİ Emberhold ekosistemi
  üzerine kurulu:** A = dikkatli hareket, dört sesin dengeye kabul edilmesi.
  B = üç hane (Corr/Sablewood/Ilvane), birbirlerinden nefret etmelerine
  rağmen, "dengeyi bozan dışarıdan bir değişkene" (Kriv) karşı fiilen
  hizalanır — Veskin sessizce destekler, Iskra Vantrel elindeki kirli sır
  kanıtlarını bu hizalanmayı pekiştirmek için kullanır. Sonuç silahlı
  çatışma değil, tamamen siyasi/hukuki bir çöküş (koltuk talebi reddedilir).
  Sarelle'in kendi baskısı bundan bağımsız, paralel işler.

  ★ Giriş noktası: reference/chapter-2-master-index.md — tüm Chapter 2
  referans dosyalarının haritası, NPC dizini, ve açık karar noktaları
  burada tek yerde. Aşağıdaki notlar hâlâ geçerli, ama önce oraya bak.

  Chapter 2, reference/chapter-2-outline.md'den (zaten tam gelişmiş, üç perdelik
  bir taslak) bu resmi beat yapısına uyarlandı (session 26, oturum-dışı tasarım).
  Tam sahne/lokasyon/NPC detayı o dosyada kalıyor — bu blok sadece beat
  iskeletini taşıyor, her /dm:dnd load'da tam taslağı okumaya gerek yok.

  Devralınan açık iplikler: D.V.'ye borçlu belirsiz bir iyilik (muhtemelen
  Whisper Court üzerinden tahsil edilecek — D.V. muhtemelen o ağın bir
  parçası), Coren Ashvale ile gizli ittifak (Compact'ın statükosuna —
  "kimse kazanmasın" — doğal bir giriş noktası), Hollow Prophet'in kimliği
  (İlyra Thorne, hâlâ DM-only — Stage 2'ye ulaşınca odağı İlvaneth'e kaymalı,
  bkz. npcs.md), Wynne Ostrel, Vaelthorn crypt.

  ★★★ İlvaneth'in Perde 1 kişisel ipliği (2026-09-11, session 26, oyuncu
  talebiyle netleştirildi) — **"anne" fikri kesin olarak reddedildi, Kriv
  gibi bir aile draması olmak zorunda değil.** Bunun yerine: İlvaneth,
  Emberhold'da **The Unfinished Circle** adlı gizli bir necromancer
  çemberini keşfeder — yüzyıllardır onun aradığı şeyi (hiçlik olmamak)
  arayan bir mesleki hanedan, aile değil. Başında **Sylandra Cael** adlı
  bir lich var (bkz. npcs-full.md). Cael, İlvaneth'in Crown'u tamamlamasını
  GERÇEKTEN İSTİYOR — kendi ömür boyu arayışının boşa gitmediğini kanıtlamak
  için. Bu, İlvaneth'in Kriv'e karşı duran tarafını ÇÖZMÜYOR, GÜÇLENDİRİYOR:
  artık sadece kendi hırsı değil, dışsal bir onay/baskı kaynağı da onu aynı
  yöne itiyor — tıpkı Kriv'in kendi hanesinin onu tersine ittiği gibi.
  Kriv'in "Boş Koltuk"una yapısal bir denge: kan değil ustalık/tanınmayla
  kazanılan bir konum. **Kritik disiplin notu (oyuncunun kendi tarihsel
  hatırlatması):** Bu kampanya başlangıçta İlvaneth'in hikayesi etrafında
  kurulmuştu; Kriv'e bir hane verilince ağırlık fiilen Kriv'e kaydı. Chapter
  2'de bu iplik, Kriv'in "Boş Koltuk"uyla EŞİT ağırlıkta tutulmalı — biri
  diğerini gölgede bırakmamalı. **✓ Bu artık sadece bir niyet değil, arc'ın
  kendi yapısında resmi: beat 1a yeniden adlandırıldı ("İki Miras — Boş
  Koltuk ve Bitmemiş Çember"), her iki what_changes/world_pressure de ikisini
  birden, açıkça, eşit satır sayısıyla adlandırıyor — sadece steering_notes'ta
  bir dipnot değil.**

  "Kim yıktı" ipliği (outline'ın kendi loose-thread listesinde) artık
  Chapter 1'de büyük ölçüde çözüldü (Draven Holt, Concordat'ın siparişi,
  D.V.'nin gölgedeki rolü) — Chapter 2'de yeniden açığa çıkarma, bunun
  yerine Sarelle'le duygusal bir yüzleşme sahnesi olarak kullan.

  ★ KESIN KARAR (session 26, oyuncu talebiyle): Chapter 2'nin arkasında
  hiçbir "büyük tanrı/kozmik kuklacı" yok — D.V. bağımsız, kendi 400 yıllık
  merakıyla hareket eden bir rakshasa olarak kalıyor, Sarelle kendi hırsıyla
  hareket eden gerçek bir antagonist olarak kalıyor. Bu bilinçli bir
  kalibrasyon kararı, gelecekte tekrar gündeme gelirse bu nottan hatırlanmalı.

  ★★ KESIN KARAR (session 26, oyuncu düzeltmesi) — DM'in "her site farklı
  formatta olsun, bazıları tam dungeon olmasın" önerisi REDDEDİLDİ. Oyuncunun
  kendi sözü: "Chapter 1'in dungeonlarını ben tek tek elle oluşturdum, başka
  türlü zayıf kalıyordu, eğlencesi zayıf kalıyordu." **Chapter 2'nin siteleri
  de (Frostmere, Kar Vaelth, Bonewrights' Hall, Grand Archive dahil) Chapter
  1'deki gibi büyük, elle inşa edilmiş, oda-oda/sahne-sahne gerçek dungeonlar
  olarak tasarlanmalı** — outline'ın "heist, not a battle" gibi ifadeleri
  içeriği küçültme gerekçesi olarak kullanılmamalı, o siteler de tam
  gelişmiş, doyurucu set piece'lere dönüştürülmeli. Bu, ileride her site
  gerçek oyuna girmeden önce (Debased Mint/Ashvale'in session 11'de önceden
  inşa edilmesi gibi) ayrı bir tasarım geçişi gerektirecek.

  ★★ KESIN KARAR (session 26, oyuncu düzeltmesi) — **XP ekonomisi saf 5e DMG
  standardında kalmalı, seviye yükseldikçe fazladan şişirilmemeli/kısılmamalı.**
  `xp.py` zaten standart CR/zorluk tablolarını uyguluyor (bu doğru, değişiklik
  gerekmiyor) — DM bunun üstüne kendi takdiriyle ekstra bir çarpan/bonus
  eklemeyecek, sadece tabloyu olduğu gibi uygulayacak. Perde 3'te "az ama
  büyük ödül" tavsiyesi hâlâ geçerli ama bu, standart zorluk/CR hesaplamasının
  doğal bir sonucu olmalı, DM'in bilinçli bir şişirmesi değil.

  ★ GÜNCELLENDİ (gün 176, session 27) — Level 10→11→12 (XP eşiği) geçildi,
  parti Emberhold'a fiilen vardı, Perde 1 artık gerçek anlamda aktif.
  İlvaneth tarafı somut ilerledi (Ash Reeve Understreets dungeon'ı +
  Sylandra Cael testi, Vashti Coldharrow). Kriv tarafı araştırma aşamasında
  (4 sponsor adayı öğrenildi, Ser Aldric Vane/Corr bağlantısı açıldı,
  henüz resmi bir sponsor görüşmesi yapılmadı). Sonraki oturumun doğal
  açılışı: Vashti Coldharrow avı (İlvaneth ipliği) ya da bir sponsora
  resmi başvuru (Kriv ipliği) — ikisi paralel tutulmalı, biri diğerini
  gölgelememeli (bkz. Pinned Facts, eşit ağırlık kuralı).

  ★ Tutarlılık denetimi (2026-09-11, session 26 sonu) — bulunan ve düzeltilen
  gerçek tutarsızlıklar: (1) "Grand Archive" ismi Karsgate (Chapter 1) ve
  Emberhold (Chapter 2 outline) arasında çakışıyordu — artık bir şube ağı
  olarak netleştirildi (bkz. world.md). (2) Kaelth Ashborn'un "Record-Keeper"
  unvanı bir kralla tutarsızdı — artık açıklandı: soylu değildi, gerçek bir
  kayıptan sonra Crown'u taşıyabilen sıradan bir kâtipti (Nairne Thistle'ın
  doktriniyle birebir örtüşüyor). (3) Sarelle'in Perde 1'deki "gerçek teklif"
  davranışı hiç yazılı değildi — artık npcs-full.md'de. (4) Orell Tain'in
  güncel durumu (Hold'da, allied, Emberhold'a gelebilir) hiç güncellenmemişti
  — artık düzeltildi.

  ★ Dungeon master listesi (2026-09-11, session 26) — `reference/chapter-2-dungeon-directory.md`'de 30 site (1×30 oda, 10×20-25, 10×10-19, 9×5-10 dağılımıyla), her biri en az bir iplik/tetikleyiciye bağlı (doğrudan plot ya da Widow's Hollow tarzı söylenti/harita). Tam Phase 1-4 detaylandırması (Debased Mint formatı) henüz yapılmadı — sırayla, ihtiyaç duyulmadan hemen önce yapılacak, hepsi toptan önceden değil.

  ★ Coğrafya (2026-09-11, session 26, sonradan rota düzeltmesiyle netleşti) — `reference/chapter-2-geography.md`'de Emberhold (nüfus ~120k, 7 mahalle) + Sundered Reach (nüfus neredeyse sıfır, 4 ana site günlerle ayrı) + Grey Kingdom (Emberhold'un ölü yansıması) için mesafe/ölçek/nüfus sabitlendi. **★ Rota düzeltmesi — oyuncunun kendi Chapter 1 haritası, Emberhold'u Harrowgate'ten değil Karsgate'ten devam eden bir ok olarak gösteriyor ("Bölüm 2" etiketi).** Gerçek zincirleme: Hold↔Karsgate (~8,5-9 gün, zaten sabit) + Karsgate↔Emberhold (~4-5 gün, yeni) = Hold↔Emberhold ~12,5-14 gün. **İki travel-encounters.md bölgesi tamam:** "Emberhold Yaklaşımları" (**Karsgate**↔Emberhold yolu, seviye 11-14, Perde 1) ve "The Sundered Reach" (seviye 15-17, Perde 2). Emberhold'un/Grey Kingdom'ın kendi İÇİ travel-encounters gerektirmiyor (şehir-ölçekli, sahne-sahne oynanacak). Perde 1-2 artık seyahat açısından tam hazır.

  ★ Haritalar (2026-09-11, session 26) — Oyuncunun paylaştığı gerçek Chapter 1 harita görseli `reference/chapter-1-map.md`'ye tam metinsel döküm olarak kaydedildi (görselin kendisi kaydedilemedi, sadece metin dosyaları yazılabiliyor) — bu, Karsgate'in altındaki "Emberhold → Bölüm 2" okunun asıl kaynağı, rota düzeltmesini bu doğruladı. Aynı lejant/mantıkla `reference/chapter-2-map.md` oluşturuldu (Emberhold'un 7 mahallesi + Sundered Reach siteleri + Grey Kingdom inset'i), VE görsel bir SVG harita çizilip `reference/assets/chapter-2-map.html`'e kaydedildi + Artifact olarak yayınlandı ("The Hollow Throne"). İkisi de gelecekte coğrafi tutarlılık kontrolü için okunmalı — Chapter 1 haritası "Unquiet Barrow hâlâ kırmızı gösteriyor ama temizlendi" gibi bayatlamış detaylar taşıyabilir, her zaman state.md esas alınmalı.

  ★ Quest Seed Bank (2026-09-11, session 26) — `reference/chapter-2-quest-seeds.md`'de 8 yeni tohum (yüzüğün kimliği, rakip simsarlar/Tobin Wrey, Fennick'in iyiliği, Ember Quarter yeniden inşası, Kindled Circle merkez şube, Compact'ın resmi teması, Brynn'in ricası, rakip lich'in mirası) + dungeon iplikleriyle örtüşenlere çapraz referans. Chapter 1'in Quest Seed Bank mantığına eşdeğer, oturum sonlarında organik olarak büyütülmeli.

  ✓ ÇÖZÜLDÜ (2026-09-11, session 26 sonu) — Coren'in Emberhold'daki rolü
  netleşti: Kriv'in "Boş Koltuk"unu AÇIKÇA destekliyor, çünkü dördüncü bir
  ses üç hanenin dengesini kilitler — Compact'ın "kimse kazanmasın" çıkarına
  hizmet eder, gizli bir iyilik değil, ortak/açık bir çıkar. Karşılığında
  Coren'in kendi kurumsal riski var: Compact tek adamın değil, kurucu ticaret
  evlerinin oluşturduğu **The Ironclad Table**'ın (yönetici konsey) elinde —
  konseyin en keskin üyesi **Ilse Drummel** (Halfling), Coren'in Kriv'e olan
  "tesadüfen hep yararlı" hamlelerinden şüpheleniyor, kanıtı yok. Parti
  ittifakı dikkatsizce sergilerse Drummel'in dikkatini çekebilir — bu artık
  gerçek bir kişisel risk taşıyan bir NPC, sadece kullanışlı bir müttefik
  değil. Bkz. `npcs-full.md` → Coren Ashvale (Chapter 2 rolü) + Ilse Drummel.

revision_log: []
```

## Arc History

### Arc 1 — "Cinders of Succession" (level 1-10) — COMPLETE (session 26, gün 133)
Çözüm: parti Gallowmere ve Harrowgate'de gerçek bölgesel güç haline geldi, D.V. ile pakt kurdu, ve Compact-Concordat çatışmasını Coren Ashvale ile gizli bir ittifaka çevirerek sonuçlandırdı (3b). Tam arc kaydı aşağıda, referans için.

```yaml
type: dynamic
arc_number: 1   # "Chapter 1: Cinders of Succession" (level 1-10) — devam ediyor, henüz tamamlanmadı
generated: "2026-08-23 (orijinal repo) — 2026-09-06'da bu yapıya taşındı"
revised: null

theme: "Hayatta kalmak için ne kadar gücü kabul edersin, ve o gücün ailenden/kimliğinden ne kadarını maliyet olarak alacağı."
resolution: "Parti, Gallowmere'de gerçek bölgesel güç haline gelir — bir faction'ın onları oyuncu olarak görmesini zorlar. (Bu, garnizon darbesiyle ÇOKTAN BÜYÜK ÖLÇÜDE GERÇEKLEŞTİ — kalan soru, Karsgate'in bu gücü nasıl test edeceği ve Compact/Concordat çatışmasının nasıl sonuçlanacağı.)"

acts:
  - act: 1
    title: "Gallowmere'in Gölgesinde (erken oyun, Session 1-10 civarı)"
    drive: "Hayatta kalmak, ilk parçayı bulmak, Gallowmere'de bir dayanak kurmak"
    beats:
      - id: "1a"
        label: "Ossuary ve İlk Parça"
        what_changes: "Basit bir soygun işi, ailelerin ve tacın gerçek doğasına dair bir kapı açar."
        world_pressure: "Mother Vey'in ossuary işi"
        status: complete
      - id: "1b"
        label: "Faction'larla İlk Temas"
        what_changes: "Parti, üç büyük gücün de Gallowmere'de bir şekilde var olduğunu ve tarafsız kalamayacaklarını anlar."
        world_pressure: "Ash-Kilns (Choir), erken faction teması"
        status: complete

  - act: 2
    title: "Güç Üssü İnşası (Session 10-17 civarı)"
    drive: "Gallowmere'de gerçek güç kurmak, faction entrikalarına bulaşmak"
    beats:
      - id: "2a"
        label: "Sahte Kanıt ve Açık Çatışma"
        what_changes: "Partinin Compact'a karşı ürettiği sahte kanıt işe yaradı — Concordat ve Compact artık açık çatışma halinde (gün 60), parti bunu bilmiyor."
        world_pressure: "Sarelle'in şüphesi, Thornlands'teki gerçek çarpışmalar"
        status: complete
      - id: "2b"
        label: "Garnizon Darbesi"
        what_changes: "Parti, Gallowmere'in 27-30 kişilik garnizonunu doğrudan ele geçirdi — Chapter 1'in tasarlanan klimaksı (bölgesel güç) ÇOKTAN gerçekleşti, planlanandan önce."
        world_pressure: "Kell'in kaçışı, garnizon koması"
        status: complete

  - act: 3
    title: "Karsgate ve Chapter 1'in Kapanışı"
    drive: "Kriv'in ailesinin sırrını çözmek (Vharkoss + katip), Compact-Concordat çatışmasının sonucunu belirlemek, seviye 10'a ulaşmak"
    beats:
      - id: "3a"
        label: "Karsgate Yüzleşmesi"
        what_changes: "Parti Vharkoss'la ve/veya isimsiz katiple yüzleşir — Kriv'in evinin yıkımının tam resmi netleşmeye başlar (ama Concordat'ın rolü Chapter 2'ye kadar tam açıklanmaz)."
        world_pressure: "Sethra'nın Vharkoss'u avlaması, Orell Tain'in araştırması"
        status: complete
      - id: "3b"
        label: "Chapter 1'in Kapanışı"
        what_changes: "Compact-Concordat çatışması bir şekilde sonuçlanır (Coren'in sabrı taşar, ya da parti müdahale eder) VE/VEYA Yeva'nın keşfi yüzeye çıkar — parti seviye 10'a ulaşır, Chapter 2'nin (Emberhold) kapısı açılır."
        world_pressure: "Coren'in ~gün 120 saati, Yeva'nın keşif bombası"
        status: complete

current_act: 3
current_beat: "3b — LANDED, session 26"

outstanding_beats: []

steering_notes: >
  Beat 3a TAMAMLANDI (session 21 devamı, gün 96-99): parti Vharkoss'la
  doğrudan yüzleşti, tam itiraf aldı (Concordat sipariş etti, aracı Draven
  Holt, dört ev aynı örüntüyle düştü, Sethra masum), yakaladı ve Hold'a
  getirip yargıladı — ömür boyu hapis, Ser Kethrax (ortaya çıkan kardeşi)
  gardiyan. Kriv'in evinin yıkımının resmi büyük ölçüde netleşti; Sarelle'in
  doğrudan rolü hâlâ kasıtlı olarak açıklanmadı (Chapter 2 için saklı, plan
  gereği). Yan ürün olarak: Draven Holt (yeni iplik, mühürlü mektup elinde,
  kimliği belirsiz) ve House Ostrel (üçüncü ev, Ilvaneth'in 5. rüyası) ortaya
  çıktı — dördüncü ev hâlâ isimsiz.

  Aynı süreçte: Orell Tain gerçekten tutuklandı ve parti tarafından fiziksel
  bir baskınla kurtarıldı (3 Concordat mensubu öldürüldü) — Sarelle artık
  partinin isimlerini biliyor (kaynağı belirsiz, muhtemelen Talyn Ambrose).
  Halka açık bir "elf+dragonborn" ödül ilanı bulundu — cover artık ciddi
  şekilde aşınıyor. Kriv, yolda kendi eskisi bir muhafızı (Ferrin) soğukkanlı
  öldürdü — Karsgate'te bir kız kardeşi var, henüz haberi yok, gelecekte bir
  intikam/keşif ipliği olabilir.

  Şimdi sadece 3b kaldı: Compact-Concordat çatışmasının sonucu VE/VEYA
  Yeva'nın keşif bombasının yüzeye çıkması, seviye 10'a ulaşma. Coren'in sabrı
  (~gün 120, gün 99 itibarıyla ~21 gün kaldı) hâlâ en büyük arka plan saati.
  Yeni bir tehdit: Ironclad Compact (Renwick Tale), garnizonun Hold'a taşınmasından
  beri (gün 81) Gallowmere'i sessizce ekonomik olarak ele geçiriyor — parti
  henüz haberdar değil, keşfedilirse 3b'yi hızlandırabilir. Ashvale Necropolis
  hâlâ "ertelendi" — parti artık level 8, güçlü, ama Sarelle bizzat orada
  (Wizard 13) hâlâ ciddi risk, two-player-scaling.md ışığında değerlendirilmeli.
  Seviye 10'a ulaşıldığında (ya da 3b net bir şekilde kapandığında) Chapter 2
  ("The Hollow Throne" — bkz. reference/chapter-2-outline.md, zaten çok gelişmiş
  3 perdelik bir taslak var) `/dm:dnd arc new` mantığıyla resmi Arc 2 olarak
  etkinleştirilmeli — o taslağı YENİDEN ÜRETME, olduğu gibi uyarla.

  Session 22 (gün 99-104) 3b'yi doğrudan ilerletmedi ama dolaylı katkısı var:
  Kriv Gallowmere'de kimliğini halka açık ilan etti, Renwick Tale'i (Compact)
  yüzleştirip anlaşmaya bağladı, ve bir Concordat tarama birimini (Vask + 8
  muhafız) tamamen yok etti/yakaladı — parti artık gerçek, görünür bir bölgesel
  güç (resolution'ın "faction'ı oyuncu olarak görmeye zorlar" kısmına hizmet
  ediyor). Yeni açık uçlar: Concordat'ın kayıp birimi fark etmesi (yeni bir
  saat olabilir), Renwick'in Coren'e ne rapor edeceği, Sarelle'in "iç sızıntı"
  paranoyası (Vask'tan öğrenildi, sömürülebilir bir zayıflık, henüz kullanılmadı).

  Session 22 devamı (gün 104-109) yine 3b'yi doğrudan kapatmadı ama gerçek bir
  yeni world_pressure kaynağı yarattı: Sethra Shestendeliath (Coren'in 15 yıllık
  güvendiği yüzbaşısı) bulundu, Kriv'in ablası olduğu ortaya çıktı, ve Compact'tan
  RESMEN İSTİFA ETTİ — hem Renwick'in yumuşatılmış çerçevesi hem süvarilerin
  çıplak raporu Coren'e ulaşmak üzere, hangisi önce varırsa çerçeveyi o belirler.
  **Bu, 3b'yi hızlandırabilecek en güçlü aday world_pressure — Coren'in tepkisi
  (öfke, intikam, ya da tam tersi bir açılım) bir sonraki oturumun doğal
  başlangıç noktası olmalı.** Ayrıca: parti artık dört Ash-Warden evinin
  tamamının adını biliyor (Shestendeliath, Doskarn, Ostrel, Velkarune) ama
  hiçbirinin konumunu; Kriv, Sethra'ya "evi yıkanlar bulunup yok edilecek" sözü
  verdi — resolution'a hizmet eden yeni, açık bir taahhüt. Vharkoss öldü (Sethra'nın
  eliyle), Draven Holt hâlâ bulunamadı. The Unquiet Barrow (yan-iplik, faction'a
  bağlı değil) tamamen kapatıldı, Cloak of Displacement kazanıldı. İkisi de
  Level 9'a ulaştı.

  Session 23 (gün 109-112) 3b'yi hâlâ doğrudan kapatmadı ama iki paralel
  world_pressure kaynağı daha yarattı. (1) Coren'in Sethra için gönderdiği
  müfreze Gallowmere'de doğrudan yüzleşildi (Kriv'in Intimidation 22'si) —
  savaşsız çözüldü, Sethra iade edilmedi ama açık düşmanlık da yaratılmadı;
  Renwick Tale, İlvaneth'in baskısıyla Coren'i ikna etmeye gönderildi, sonucu
  hâlâ bekleniyor — **bu hâlâ en güçlü tetikleyici aday.** (2) Yeni, beklenmedik
  bir ikinci tetikleyici: parti bir Concordat askere alım kampını tamamen yok
  etti (2 sivil dahil 7 ölü, Fireball + GWM) ve izleri örtmek için kontrolsüz
  bir orman yangını başlattı — henüz keşfedilmedi ama gerçek bir suç mahalli
  geride kaldı. Concordat bunu bulduğunda tepkisi Coren'in tepkisinden bağımsız,
  paralel bir escalation kaynağı olabilir; iki faction'ın aynı anda tetiklenmesi
  3b'yi hızlandırabilir ya da karmaşıklaştırabilir. Ayrıca: Draven Holt artık
  somut bir hedef (el yazısı doğrulandı, Hold'a 15 yıl önce müfettiş kılığında
  girip çıktığı kanıtlandı) — Kriv bizzat peşine düşmeyi üstlendi, kendi
  kişisel-thread'i olarak devam edebilir. Mother Vey'in "partiyi okumak" saati
  kapandı (3/3) — sonucu resolution'ı destekliyor ("risk değil, bahis").
  Ordu büyütme iki koldan başladı (Hold + Gallowmere), Chapter 1'in kapanışına
  doğru partinin gerçek bir askeri güce dönüşmesi somutlaşıyor.

  Session 24 (gün 112-114) 3b'yi hâlâ doğrudan kapatmadı ama gerçek bir sinyal
  ve üç yeni paralel eskalasyon kaynağı üretti. Bir Ironclad kontrol noktası
  komutanı, Coren'in son günlerde tuhaf davrandığını, neredeyse aynı anda gelen
  iki mesajdan (muhtemelen Sethra'nın istifası + Renwick'in çerçevelemesi)
  sonra bir toplantıyı iptal edip kapandığını fısıldadı — **3b'nin en güçlü
  tetikleyicisi artık fiilen tetiklenmiş olabilir**, sonucu hâlâ bilinmiyor.
  Ayrıca: The Kindled Circle (yeni eklenen tarafsız büyücüler loncası), askere
  alım kampı Fireball'ının bıraktığı büyü imzasını fark edip partiyi araştırmaya
  başladı — Concordat'tan bağımsız, paralel bir keşif zinciri. Cinder Choir'ın
  Hollow Prophet'i de Yeva'nın raporu + kamuya açık bilgileri birleştirip
  Kriv'in dönüşünü kendi "ölüp-dönen hükümdar" doktrinine yakın okudu (Crown
  parçaları/gerçek Ascension hâlâ tamamen gizli). Hiçbiri henüz partiye teslim
  edilmedi. Ayrıca partinin elinde artık gerçek bir Concordat-bölücü kaldıraç
  var: Sarelle'in Ashvale kazısının İmparator'dan önce başladığı (Vask'ın
  rüya yoluyla doğrulanan itirafı) — bilinçli olarak saklanıyor, Tain için.
  House Ostrel ve Velkarune'un konumları da artık biliniyor (sırasıyla
  Cindermoor ve Karsgate Kingsward), ikisi de henüz ziyaret edilmedi.

  Session 25 devamı (gün 123-131) 3b'yi doğrudan kapatmadı ama devasa bir
  eşiği geçti: D.V.'nin gerçek kimliği (rakshasa, Lord Dorian Varn) çözüldü
  ve bir pakt kuruldu — bu artık DM-only bir sır değil, kampanyanın en büyük
  gizemi oyunculara açık. Draven Holt bulunup infaz edildi, House
  Shestendeliath'ın yıkımının son "bilinmeyen aracısı" kapandı. Parti
  Karsgate Undertow'da (Doss + Sella Dray) kansız bir denge kurdu. Karsgate'te
  Kindled Circle üyeliği kazanıldı ama Odalys Ferrant'ın şüphesi tam bitmedi.
  **En kritik gelişme: Harrowgate'in Shestendeliath'a bağlanma süreci
  başladı** (Ostrig Vane + Renata Kroll) — bu, Gallowmere'den sonra ikinci
  büyük bölgesel güç kazanımı, ama Sethra'nın kendi uyarısıyla Coren'i
  "bir örüntü" (Compact'ın peş peşe soyulması) olarak okumaya itip 3b'yi
  fiilen tetikleyebilir. **Sethra + İlvaneth şu an Coren'i bulup barışçıl
  bir çözüm denemek için yolda** — bir sonraki oturumun en olası açılışı bu
  görüşmenin sonucu (savaş ya da barış). Ayrıca artık Sarelle'in kalan 2
  fragmanının konumu (İmparator'un lahdi) ve zayıf saati (Restday-dışı
  geceler) biliniyor — Ashvale hâlâ erteleniyor ama artık gerçek bir plan
  var, "belirsiz bir gelecek" değil.

  **Session 26 (gün 131-133) — 3b LANDED.** Parti doğrudan müdahale etti:
  Sethra + İlvaneth, Coren Ashvale ile açık savaşı önleyen bir ateşkes kurdu
  (İlvaneth'in Deception nat 20'si + Sethra'nın dürüst itirafıyla). Aynı
  zamanda Kriv, Harrowgate'te Concordat'ın gizli bir sabotaj operasyonunu
  (Wyle Sarn, Councilman Vorn suikastı) çözüp iki tutsak aldı. Coren,
  Harrowgate'e gelip Kriv'le yüz yüze görüştü — Thorn'un ihanetini öğrenince
  gerçek bir gizli ittifak kuruldu (kamuya açık çatışma görüntüsü korunacak,
  gerçek düşman artık ortak: Sarelle/Concordat). Chapter 1'in resolution'ı
  ("parti bir faction'ı oyuncu olarak görmeye zorlar") hem Gallowmere/
  Harrowgate'teki bölgesel güçle hem de bu ittifakla tam olarak gerçekleşti.
  Chapter 1 formal olarak kapandı, bkz. `## Arc History`. Chapter 2 ("The
  Hollow Throne") aynı oturumda oyun-dışı bir tasarım çalışmasıyla resmi
  Arc 2 olarak etkinleştirildi, `reference/chapter-2-outline.md`'den
  uyarlandı.

revision_log: []
```


## Continuity Archive
*Session-log.md sadece son 2 tam oturumu tutar — daha eskisi session-log-archive.md'ye taşınır, buradaki özet kalır. graph.json ilişkisel durumu (faction üyeliği, disposition) kanonik tutar; buradaki maddeler onu tekrar etmez.*

### Session 34 — 2026-09-20 — Wren Marrow himayesi, Reeks katliamı, Level 16, Ironclad Table darbe planı, gün 194-196
- **Wren Marrow himayeye alındı, Cassian Ilvane'in koalisyonu Batı Bahçesi'nde herkesin önünde çöktü** (Berengar'ın kanıtı + Persuasion 23).
- **Ansel Drey + Sunken Ledger tamamen yok edildi** — üç hanenin sırları + 15 yıllık kırık-daire kanıtı ele geçirildi, işbirlikten hemen sonra infaz edilmesi Reeks'in tüm yeraltı ağını partiden ürküttü (itibar bedeli, kalıcı).
- **Level 16'ya geçildi (ikisi de)** — Kriv CHA 18, İlvaneth WIS 16/CHA 14, Power Word Stun + Mordenkainen's Magnificent Mansion eklendi.
- **Noter Ostrin Vell öldürüldü (ağın kendi temizliği, parti varmadan dakikalar önce)** — "Aşkalkanı Emanet Şirketi" ipliği Speak with Dead ile Karsgate/House Corvane'e (17 yıl önce) kadar takip edildi.
- **Coren Ashvale ile Ironclad Table'a karşı gizli bir darbe planı kuruldu** — 6.000 gp başlangıç fonu verildi (toplam 35-40k gerekiyor), Ilse Drummel şüpheli olarak teşhis edildi.

### Session 33 — 2026-09-18 — Kavash'ın ölümü, Tain'in Concordat'ı devralması, Level 15, Ivrathax ile savaşsız ittifak, gün 191-194
- **Solenne Kavash öldürüldü** (Ashvale, müzakere çöktü, Trip Attack+GWM zinciri) — Concordat'ın Karsgate liderliği tamamen boşaldı; Orell Tain, Kavash'ın sahte vekillik belgesiyle Concordat'ın yeni fiili başı oldu.
- **Level 15'e geçildi (ikisi de) — Ascension Stage 3 tetiklendi** (Kriv: "The Presence" — Frightful Presence, Truesight; İlvaneth: "The Pattern Holds" — yaşlanmıyor, 0 HP'de ölmüyor).
- **Tobin Wrey'in ekibi ihanet edip pusu kurdu, hepsi öldürüldü** — ittifak bitti, yeni bir düşmanlık.
- **Ivrathax ile savaşsız ittifak kuruldu (Persuasion 23, kardeşlerini öldürdükten hemen sonra) — 8. Crown parçası hediye edildi**, parti 8/9 parça taşımaya başladı.
- **Campaign Arc baştan revize edildi (oyun-dışı tasarım geçişi):** Crown'un gerçek doğası artık panteonun silinmiş yedinci tanrısı Ashborn'u hapseden bir mühür — DM-only, Act 3 finalinin temeli (bkz. `## Campaign Arc`).

### Session 32 — 2026-09-17 — Kule-i Mensuh'un tamamlanması, Sylandra ile ortaklık, Sarelle'in düşüşü, gün 186-191
- Level 14'e geçildi (ikisi de); Sylandra Cael ile tam ortaklık kuruldu (kendi çatlak phylactery'sini itiraf etti, "gönüllü verilen güç" ortak araştırması başladı).
- **Sarelle Duskbourne ÖLDÜ** (Disintegrate ile toz oldu) — Ashvale Necropolis düştü, Coren'in kontrolüne geçti. Chapter 1'in gerçek kapanışı.
- Ser Aldwin Ashvale (ghost, Coren'in atası) ile tam ittifak kuruldu, üç yüz yıllık bir mektup/kılıç Coren'e verildi.
- The Working Archive (İmparator'un suikast kanıtı) ele geçirildi; parti 7/9 Crown parçasına ulaştı.
- Kalibrasyon: tracker.py turn gate'i ve mekan/boss tasviri disiplinleri bu oturumda `DM Style Notes`'a kalıcı olarak işlendi.

### Session 26 — 2026-09-11/12 — Harrowgate (Wyle Sarn, Konsey), Cinder Hollow, 3 haftalık FF, gün 131-167
- Councilman Vorn suikastı tam çözüldü (Wyle Sarn/Sessiz/Thorn/Kesen yakalandı, üçü idam edildi) — **İmparator'un zehirlenmesi canlı bir tanıktan doğrulandı.**
- Harrowgate Konsey oylaması kazanıldı — Harrowgate resmen House Shestendeliath himayesinde, %10 Lord payı.
- Cinder Hollow'da Mira Kessel'den **Sarelle'in ölümcül, yıllardır süren hastalığı** öğrenildi; Bram Ostley/Drenmoor Ticaret Evi ipliği büyüsel korumayı aşamadan kapandı (Ostley infaz edildi).
- Üç haftalık zaman atlaması (gün 137-161): Sethra Fighter 8'e yükseldi, Hold Hazinesi kuruldu (~1.044 gp), asker sayısı ~92→~127-145, Teleportation Circle Day 24/365 (Tain devraldı), Wardensteel'in nihai tasarımı ("House Shestendeliath'ın Uyanışı") onaylandı.
- Concordat gerçek bir alarma geçti (iki saha ajanının sessizliği bir arama ekibi çıkardı, izler Karsgate'e gidiyor) — toplam XP +12.350/kişi bu oturumda.

### Session 27 — 2026-09-13 — Karsgate → Emberhold, Chapter 2 başlangıcı, gün 167-176
- Emberhold yolunda haydut pususu + suikast girişimi (Sessiz Defter ağı ilk kez öğrenildi) — Ser Aldric Vane ile dostluk kuruldu, House Corr'a giriş açıldı.
- Level 11'e geçiş, ikisi de — Ascension Stage 2 tetiklendi (Kriv: fire immunity/breath güçlendi; Ilvaneth: yemek/su/nefes gerekmiyor, undead komuta).
- Ash Reeve Understreets (6 oda, tam dungeon) temizlendi — final boss The Unmade (custom CR13) yenildi.
- Sylandra Cael ile ilk temas — tam güven kazanılmadı, Vashti Coldharrow'u öldürüp kanıt getirme testi verildi.

### Session 27 Devamı — 2026-09-13 — Sereth Corr, Sessiz Defter, Vashti Coldharrow, Level 12→13, gün 176-179
- Sereth Corr ile gerçek bir ittifak kuruldu (Sparrow yakalandı, "Efendiler"in Kriv'i izlediği öğrenildi, Rookery lokasyonu bulundu — ortak baskın planlandı).
- Level 11→12→13 aynı oturumda — Kriv ASI/Indomitable 2 kullanım, Ilvaneth Observant + 7. seviye slot (Draconic Transformation/Teleport).
- Vashti Coldharrow (460 HP final boss) yenildi — Sylandra Cael'in testi tamamlandı, kanıt henüz teslim edilmemişti (session 28'de teslim edildi).
- Reagent Hall'da başarısız bir hile girişimi (Efreeti Bottle bakiyesi) — Deception/Insight berabere, tam ödeme ertelendi.
- Level 12 XP eşiği geçildi (bir sonraki uzun molada işlenecek).

### Session 28 — 2026-09-14 — Emberhold (House Corr, Eski Kışla, House Sablewood), gün 179-181
- Wrenna infaz edildi, Arnholt yakalanıp Berengar'a teslim edildi — Whisper Court'un House Corr + House Sablewood'daki gözü aynı gün kör oldu.
- Eski Kışla (8 oda, tam dungeon) temizlendi — Dorren Corr'un revenant'ı, Sereth'in mektubuyla ikna edilip huzura kavuşturuldu; itirafı **"kırık daire" mührü ipliğini açtı** (House Ilvane/Iskra Vantrel'e işaret ediyor), Sereth'e henüz tam açıklanmadı. Loot: Dorren'in Zarafeti, Corr Yatırım Bıçağı, ~3.200 gp, büyük bir silah deposu (Hold'a teslim).
- Sereth'in sponsorluk sözü kesinleşti — gün 182'de Veskin dinlemesinde resmi tanıtım (session 30'da gerçekleşti).
- Büyük envanter satışı (+9.955 gp toplam) + Efreeti Bottle'ın kalan ödemesi yapıldı, artık tamamen İlvaneth'in.
- XP: +7.700/kişi. İkisi de 128.012 XP, Level 13.

### Session 29 — 2026-09-15 — Karsgate araştırması, House Ilvane/Ash Reeve ipuçları, Sundered Garden randevusu, gün 181-182
- Odalys Ferrant'la bilgi anlaşması işletildi — Ash Reeve Understreets'in haritalanmamış en derin odası + "Cael hattı" ipucu, Sylandra Cael'e olası bağ (henüz Odalys'e açıklanmadı).
- House Ilvane'in kurucu efsanesi (kırık bir tacı bilerek reddeden matriark) keşfedildi — tematik bir yankı, henüz kullanılmadı.
- **Sundered Garden randevusu kesinleşti — gün 184, gün batımında** — sonucu session 30'da (Reyna Sorrel) çözüldü.
- Kriv/İlvaneth, ertesi günkü Veskin dinlemesi için attunement'larını yeniden düzenledi (Corr Bıçağı/Winged Boots attune, BKB/Ring of Mind Shielding deattune).
- XP yok bu oturumda (qualifying encounter olmadı).

### Session 30 — 2026-09-15/16 — Hollow Throne, Sereth'in desteği, House Ashveil, Sundered Garden, gün 182-185
- **★★★ Beat 1a TAMAMLANDI** — Kriv resmen House Shestendeliath'ın koltuğuna oturdu (Hollow Throne, Cassian Ilvane'in itirazı bastırıldı), Wardensteel'in kilidi açıldı. +3.400 XP/kişi.
- Sereth Corr'dan 25 asker + 800 gp + Ember Quarter ortaklığı (10.000 gp toplam yatırım) alındı; iki yeni mülk edinildi (Sonnward Promenade konağı, Kingsward'daki House Ashveil malikanesi).
- House Ashveil malikanesinde 32 yıllık bir sır bulundu — Whisper Court'un doppelganger yönteminin en eski somut kanıtı (Lord Garrick'in günlüğü).
- **Reyna Sorrel öldürüldü** (Sundered Garden randevusu, bilgi karşılığında sığınma istedi, infaz edildi) — **Corbin Vayle tehdidi ilk kez öğrenildi.**
- Crown parça sayısı 7'den 9'a revize edildi (Sundered Reach'te 2 ek parça: Ivrathax, Ser Oskar Thrune).

### Session 31 — 2026-09-16/17 — Kule-i Mensuh (20 oda), Corbin Vayle, gün 185-186
- **Reeks gözcüsüne Modify Memory tuzağı** — House Ilvane'in 2 ajanı yakalandı, Spymaster Elian Rook ifşa oldu; Veskin bilgiyi kendi kaldıracı olarak sakladı.
- **Corbin Vayle öldürüldü** (Scrying + pusu) — Sarelle'in özel avcı tehdidi çözüldü, Concordat'ın suikast emrine dair somut kanıt ele geçirildi.
- **Kule-i Mensuh (20 oda) tamamen temizlendi** — final boss The Warden of the Unfinished düştü, Mireille Osk özgürleştirildi (Inspiration).
- Üç kalıcı yapısal sistem kuruldu: Combat Difficulty Doctrine v2+v3 (boss item ekonomisi), XP multiplier ×1, Goal Tracker (`goals.py`).
- XP: ~30.925/kişi. İkisi de 162.437 XP — Level 14 kesin bekliyordu.

### Session 23 — 2026-09-08/09 — Harrowgate → Gallowmere → Hold, gün 109-112
- Kurt sürüsü pususu temizlendi (Ice Storm + GWM); Gallowmere'de Ironclad müfrezesiyle savaşsız yüzleşme (Intimidation 22) — Sethra iade edilmedi.
- **Old Sabeth bulundu, Külsüz Yer'e gerçek ziyaret** — Kriv yetimhane çivisini bıraktı, İlvaneth 4 Crown parçasına dokundu.
- **Bir Concordat askere alım kampı tamamen yok edildi** (7 ölü, 2 sivil dahil) + kontrolsüz bir orman yangını — o zaman keşfedilmemişti (session 25 devamında keşfedildiği öğrenildi).
- Draven Holt'un el yazısı doğrulandı (Investigation 23) — Hold'a 15 yıl önce müfettiş kılığında girip çıktığı kanıtlandı.
- Garnizon terfileri (Dallin, Berta/Hask), iki koldan asker toplama başladı — bu hattın devamı session 26'nın büyük asker-büyüme tablosuna bağlanıyor.

### Session 24 — 2026-09-09 — Greyholt, Harrowgate, Cindermoor, Karsgate, gün 112-122
- Greyholt'ta Persuasion 20 ile Hallik'in güveni kazanıldı (iki başarısız denemeden sonra) — hasat sonrası Hold ziyareti vaat edildi.
- Yazman Aldous Penmark'ın itirafı (Intimidation 24) — dört Ash-Warden evinin devrini de aynı gizli otorite (kukuletalı kurye) imzalattı; House Ostrel'i satın alan kişi İlyra Thorne olarak öğrenildi (DM-only: Hollow Prophet).
- Ascension rüyası #8 (Vask'ın son düşüncesi) — Sarelle'in Ashvale kazısının İmparator'dan önce başladığı ve Konsey'e yalan söylenerek gizlendiği doğrulandı; bu gerçek Kriv/İlvaneth'te saklı tutuluyordu (session 26'da Coren'e de açıklandı, bkz. Live State Flags).
- House Ostrel ve House Velkarune'un konumları bulundu (Cindermoor, Karsgate Kingsward); İlyra Thorne ile derin görüşme, Wynne Ostrel ipliği açıldı.
- Panteon (6 tanrı) ve The Kindled Circle büyücüler loncası dünyaya eklendi; yeterlilik bonusu hatası (+3→+4) düzeltildi.

### Session 25 devamı — 2026-09-10 — Karsgate Undertow, D.V. Pakt, Harrowgate, gün 123-131
- D.V.'nin gerçek kimliği (rakshasa, "Lord Dorian Varn") Arcana ile teşhis edildi (İlvaneth 21, Kriv 18) — dört yüz yıldır Ash-Warden hanelerini "deney" olarak izlediğini itiraf etti, kendisi doğruladı, inkar etmedi.
- Pakt karşılığında öğrenilenler: Ascension'ın 3-4. evresi (bkz. `ascension-tracks.md`), Sarelle'in Restday-dışı gecelerde zayıf olduğu, ve kalan 2 Crown parçasının konumu (İmparator Ashkar Vaelthorn'un mühürlü lahdi, Ashvale'in en derin katmanı).
- Draven Holt bulundu (Kestrel Waystation), tam itiraf verdi — D.V.'nin gerçek adını kendisi de bu geceye kadar bilmiyordu; Kriv Breath Weapon ile infaz etti.
- İlvaneth Ascension rüyası #12: İmparator Ashkar Vaelthorn'un son anı — Sarelle'in ona sonuna kadar sadık göründüğünü, yavaş zehirle öldüğünü doğruladı.
- Harrowgate'in Shestendeliath'a bağlanma süreci başladı — Ostrig Vane (Garnizon Evi kaptanı, Compact'a kumar borcuyla bağlı) şartlı kabul verdi, Renata Kroll (Tüccar Konseyi) 3 gün içinde Konseyi toplayıp desteklemeye söz verdi.
- Sethra, Harrowgate'e el atmanın (Gallowmere'den sonra ikinci kez) Coren'i "bir örüntü" olarak okuyup 3b'yi tetikleyebileceğini uyardı — Kriv gerekirse savaşı göze alacağını söyledi. Sethra + İlvaneth, barışçıl bir çözüm denemek için Coren'i bulmaya gitti, parti ayrıldı.
- İkisi de level 10'a ulaştı bu oturumun başında (Vault of the Nameless + House Velkarune); oturum boyunca toplam ~+8475 XP/kişi kazanıldı, ~73.775/85.000'e ulaşıldı.

### Session 23 — 2026-09-08/09 — Harrowgate → Gallowmere → Hold, gün 109-112
- Thornlands yolunda kurt sürüsü pususu (İlvaneth Ice Storm + Kriv GWM, tek round'da temizlendi).
- Gallowmere'de Ironclad müfrezesiyle savaşsız yüzleşme (Intimidation 22) — Sethra iade edilmedi, açık düşmanlık yaratılmadı.
- **Bir Concordat askere alım kampı tamamen yok edildi (2 sivil dahil 7 ölü, Fireball+GWM)** + kontrolsüz bir orman yangını başlatıldı — henüz keşfedilmedi, gerçek bir suç mahalli.
- Old Sabeth bulundu, Külsüz Yer ipliği çözüldü — Kriv yetimhane çivisini bıraktı, İlvaneth 4 parçaya dokundu.
- **Draven Holt'un el yazısı doğrulandı (Investigation 23)** — Hold'a 15 yıl önce müfettiş kılığında girip çıktığı kanıtlandı, Kriv bizzat peşine düştü.

### Session 22 — 2026-09-08 — Hold → Gallowmere, gün 99-104
- Vask yakalanıp sorgulandı (Detect Thoughts ile doğrulandı), sonra Kriv tarafından infaz edildi — Solenne Kavash (yeni 2. adam), Concordat'ın bölgesel gücü, ve İmparator-öncesi kayıt fısıltısı öğrenildi (bu fısıltı session 24'te Ilvaneth'in Ascension rüyasıyla kesin doğrulandı). +600 XP.
- Kriv Gallowmere'de kimliğini halka açık ilan etti (gün 103), Renwick Tale ile anlaştı (Intimidation 22), kasaba dinleme oturumu + Fennick/Mother Vey ittifakları kuruldu. +1400 XP.
- Gallowmere Yeniden Yapılanma Planı kuruldu (işgücü, asker eğitimi, ticaret konvoyu, vergi %35→%20, ayrı Gallowmere Hazinesi) — Kriv 180 gp yatırım yaptı (hoard-sense DC12, kıl payı geçti).
- Sethra bulundu ve tanındı (aile yüzüğü, Wardensteel, çocukluk hatırası ile doğrulandı) — Compact'tan resmen istifa etti (yazılı mektup). Yol boyunca Kriv ona evin yıkılış gerçeğini anlattı (Crown/parçalar hariç).
- Hold'da Kethrax-Sethra 15 yıl sonra yeniden buluştu; **Vharkoss, Sethra tarafından zindanda bıçaklanarak öldürüldü** (kontrolsüz bir öfke anında, Kriv'in planladığı "yaşasın her gün ölsün" cezası hiç uygulanamadan bozuldu). Vharkoss'un Sethra'ya yazıp hiç gönderemediği mektup hâlâ İlvaneth'te.
- XP toplam: +2900/kişi bu oturumda.

### Session 21 — 2026-09-07 — The Debased Mint, Tain'in Kurtarılışı, Vharkoss'un Yakalanması, gün 95-99
- **The Debased Mint tamamen temizlendi (18 oda)** — Baron Halvern Doskarn (Wraith) yenildi, **4. Ashen Crown parçası alındı**. İkisi de Level 8'e ulaştı.
- Orell Tain, Sarelle'in gözaltısından fiziksel bir baskınla kurtarıldı; gizli defteri alındı — dört Ash-Warden evinin aynı imza zinciriyle düştüğünü doğruluyor.
- **Vharkoss'la yüzleşildi, tam itiraf alındı**: Concordat evi sipariş etti, aracının adı **Draven Holt**, Sethra tamamen masum. Vharkoss yakalanıp Hold'a getirildi, ömür boyu hapis kabul etti.
- Kriv, yolda kendi eski muhafızı Ferrin'i soğukkanlılıkla öldürdü (uykuda, GWM kritik) — Karsgate'te bir kız kardeşi var, haberi yok.
- Ser Kethrax'ın Vharkoss'un kardeşi (Kriv'in ikinci amcası) olduğu ortaya çıktı. Ilvaneth'in 5. rüyası: **House Ostrel**, üçüncü düşen Ash-Warden evinin adı.

### Session 20 — 2026-09-06 — Karsgate, Undercity, gün 93-95
- Karsgate'e varış, Karsgate Undercity (The Sump) tam keşfedildi — 5 wererat, bir gray ooze, bir otyugh öldürüldü (~2025 XP toplam), eski bir kaçakçılık kilit kutusu bulundu.
- Kingsward Geçidi doğrulandı (House Varn'ın özel bahçesine açılıyor); House Varn'ın bahçesinde aşırı korunan bir yan kapı keşfedildi, muhafızın anahtarlığı çalındı (fark edilmedi).
- **Büyük keşif: The Debased Mint** — Charge-Roll'un işaret ettiği gerçek Crown fragman sitesi, House Doskarn'ın 18 odalı yozlaşmış mint'i bulundu (ayrı oturumda oynanacak).
- Ember Crown Katedrali'nde araştırma: Cinder Choir'ın doktrininin kökeni, Katedral'in bastırılmış bir teolojik anlaşmazlığından geliyor — Concordat'ın ash-büyüsü ve Choir'ın inancı aynı unutulmuş kaynaktan besleniyor.
- Ilvaneth Harn'ın kitabını takas etti, 5 scroll kopyaladı; Kriv Boots of Striding and Springing satın aldı.

### Session 19 — 2026-09-05 — Cair Dunnow, gün 89-90
- Moor-Ghost ödülü tek round'da bir ettin öldürmesi olarak çözüldü, bir kurbanın madalyonu kurtarıldı (Cair Dunnow'a iade edilecek).
- Ash-sunu töreni dürüstçe yapıldı — Nairne Thistle warming'e geçti (graph.json'da disposition olarak tutuluyor).
- **Büyük doktrin düzeltmesi:** Ashen Crown aslında bir yas-kalıntısı — gerçek bir kişisel kaybı kabul eden biri taşıyabilir, isimsiz bir kül-kral bunu sonradan iktidar iddiasına çevirmiş. Drowned Cathedral'ın (session 18) bulgusunu doğruluyor.
- Sonraki hedef olarak Karsgate (Vharkoss + isimsiz katip) belirlendi.

## Session Flags
- **session_status: open** (2026-09-22, session 37 `/dm:dnd load` ile açıldı.)
- language: tr (Türkçe anlatım — 2026-09-08'de kesin talep edildi, tüm gelecek oturumlarda geçerli, DM her zaman Türkçe anlatmalı)
- autosave: on
- mirror_to_global_roster: off (2026-09-06, session 20 — tek kampanya var, kampanyalar arası taşıma kullanılmıyor; `/dm:dnd save` bundan sonra sadece `campaigns/ashen-crown/characters/`'ı günceller, global `characters/` kopyasına dokunmaz)
- *(2026-09-22 temizliği: `display_mode`, `roll_mode` ve `xp_multiplier` bayrakları kaldırıldı — display/telefon sistemi skill'den tamamen silindi, zar sahipliği ve çarpansız XP artık skill'in kendi varsayılanı. Bkz. AIGM refactor, git `aigm-refactor` dalı.)*
- **next_session_opening (2026-09-22 güncellendi, session 36 sonunda):** Parti **The Ember Court'ta, Oda 12'nin eşiğinde** — Oda 1-11 tamamen temizlenmiş, **rest alınmamış** (İlvaneth 114/116, Kriv 177/196), loot Bag of Holding'de. İçeride **3× Rakshasa askeri** bekliyor, henüz girilmedi. **Saat işliyor:** Iskra ve Sathriel'in Kor Beşiği'ndeki (Oda 24) reformu **gün 206**'da tamamlanıyor; düzlem oranı **x2** olduğu için içeride geçen her saat dışarıda iki saat — kalan 13 oda yerel ~24 saatten azına sığmak zorunda. Bu, rest'i gerçek bir bedele bağlıyor: uzun mola 8 yerel saat = 16 maddi saat. Açık kararlar: Rakshasa'ların **Limited Magic Immunity**'si (6. seviye ve altı hiç işlemiyor) karşısında İlvaneth'in 7.+ seviye repertuarına (Teleport, Power Word Pain/Stun, Finger of Death) geçip geçmeyeceği; rest riski vs kaynak tükenmesi; Yargı Çukuru'ndaki "şampiyon"un stok stat'la gelmesi üzerine oyuncunun talebi — **bundan sonraki isimli/unvanlı düşmanlar gerçekten güçlendirilmiş stat taşımalı** (`SKILL-encounter-design.md` uygulanarak). **Bang önerisi:** Oda 12'nin kapısı parti dokunmadan açılır ve üç rakshasa zaten ayakta, yayılmış, bekliyor durumdadır — Borçlular Galerisi'ndeki bağlı ruh haber uçurmuş olabilir; kim önce hamle yapacağı artık bir initiative meselesi değil, bir tercih meselesi.
- **Bir sonraki oturumun ilk iş listesi:** (1) `calendar.py -c ashen-crown stateline` ile saati aç ve gün 206'ya kalan farkı yüksek sesle söyle; (2) Ember Court'un x2 oranını her sahne sonunda `calendar.py scene` ile işle; (3) `factions.py tick --day <N>` — Whisper Court'un reform adımı gün 206'da vadesi doluyor.

## DM Style Notes
*Bu bölüm artık SADECE bu kampanyaya özel olguları ve kalibrasyonu taşır. Genel DM kuralları (zar sahipliği, NPC bilgi sınırı, combat anlatımı, tasvir disiplini, NPC üretim standardı, site tasarımı, kayıt titizliği, zaman atlama, parti bölünmesi vb.) 2026-09-22'de skill'in kendisine taşındı — `SKILL.md`, `SKILL-combat.md`, `SKILL-commands.md`. Orada yazan bir kuralı burada tekrarlama; çeliştiği bir upstream metin kaldıysa kuralı burada "override" etmek yerine skill'de düzelt.*

**Masa/kampanya olguları**
- **Parti şehir içi/kısa mesafe seyahatte her zaman atlı — asla yürümez** (2026-09-16, session 30, tekrar eden düzeltme). Sahne geçişlerinde varsayılan atlı anlatılmalı.
- **Full dark/gore kapsamı onaylı** — iki Neutral Evil karakterle tutarlı, sansürsüz içerik beklentisi var. Content line/veil yok (dm-notes.md'den doğrulandı).
- **★ Ilvaneth'in hazır büyüleri `reference/Ilvaneth-hazir-buyuler.md`'den okunur** (2026-09-14'ten itibaren, app tarafından üretiliyor). Karakter sayfasının "Prepared?" sütunu güncel takip için değil, sadece spellbook'un tam içeriği için kanonik. Her Long Rest'ten sonra bu dosya kontrol edilmeli.
- **★ Kriv'in combat kısaltma notasyonu — her zaman bu formatta okunur, tekrar sorulmaz:**
  - **Atak tipi önekleri:** `Raw` = normal saldırı · `GWM` = Great Weapon Master (-5/+10) · `B.A. GWM` / `B.A. Raw` = bonus action saldırısı (crit/kill tetiklemesi) · `Pre. St.` = Precision Attack o saldırıya uygulandı.
  - **Precision Attack ile birleşim:** `GWM<n> Pre.St.<k> (n+k)` — `n` ham d20, `k` manevra zarı; DM atak bonusunu (ve GWM ise -5'i) ayrıca ekler. Precision Attack'in zarı ataka gider, hasara asla.
  - **★ Hasar zarı sırası — Wardensteel (gün 182'den beri ana silahı): `d12 + d6 + d6 + d10`** = silah zarı + Wardensteel'in +2d6 fire'ı (HER vuruşta, koşulsuz) + manevra zarı (sadece manevra kullanıldıysa). **Düzeltildi 2026-09-22:** eski `d12 + d8 + d10` tarifi Barrow-King's Blade'e aitti ve o kılıç gün 187'de (session 32) satıldı — artık geçerli değil.
  - **Sabit modifikatör:** +9 (STR 7 + silah 2, sayfadaki Attacks satırında zaten toplanmış) + GWM kullanıldıysa 10. Crit'te tüm zarlar iki katına çıkar (2d12 + 4d6 [+2d10]).
  - Oyuncu her zaman sadece ham zarları verir; tüm modifikatörleri DM ekler.
- **Lokasyon dosyaları hâlâ eski formatta** — `original-repo/.../info/locations/` altındaki 38 dosya bu skill'in şablonuna adapte edilmedi. Sahneye girmeden önce ilgili dosya okunmalı, olduğu gibi yapıştırılmamalı. (NPC roster'ı 2026-09-06'da tam adapte edildi; yeni üretilen her NPC/lokasyon skill şablonunu kullanır.)

**Bu kampanyanın anlatı dengesi**
- **★★★★★ Eşit anlatı ağırlığı — standing rule.** Hiçbir oturum Kriv'in ipliğini (hane/askerler/Sethra) İlvaneth'inkine (ölümsüzlük arayışı) baskın bırakmamalı. Bu denge daha önce iki kez bozuldu; yapısal düzeltme olarak Cinder Choir/Hollow Prophet ipliği Kriv'den İlvaneth'in Ascension Stage 2'sine kaydırıldı (bkz. `## DM Notes`, 2026-09-10). Yeni büyük iplik/faction dağıtırken bu dengeyi aktif kontrol et.
- **Ascension mekaniği asla zorlanmaz.** Kriv ve İlvaneth'in yapısal çatılması organik büyümeli, bir "ihanet anına" asla itilmemeli. (2026-09-18/session 33: çatışma oyunda organik olarak çözüldü, Kriv tam destek veriyor — geri zorlanmamalı; bkz. Pinned Facts.)

**Zorluk kalibrasyonu**
- **★ Encounter tasarımı — genel doktrin artık skill'de: `SKILL-encounter-design.md`.** Her boss/önemli encounter kurulurken o dosya açılır (boss HP çok-round hesabı, varsayılan direnç profili, terrain koruması, boss öncesi kaynak tüketimi, destek yaratık HP/AC'si, imza silah + direnç item'ı, uygulama seviyeleri tablosu). Bu kampanyaya özel teşhis, kalibrasyon geçmişi ve hazır reoccupation eşleşmeleri `reference/combat-difficulty-doctrine.md`'de kaldı.
- **Dungeon zorluğu bir kademe yukarı** (2026-09-07, session 21): canavar sayısı/CR'ı `two-player-scaling.md`'nin önerisinden bir kademe yüksek, solo boss'larda HP marjı cömert, ardışık odalarda dinlenmeden daha fazla kaynak tüketimi. **Not (2026-09-22):** session 36'da canavar direnç/bağışıklıklarının hiç uygulanmadığı ortaya çıktı (veri seti bu alanları taşımıyordu, artık düzeltildi) — "fightlar kolay" teşhisinin bir kısmı bundan kaynaklanıyor olabilir. Bir sonraki birkaç dövüşte gerçek zorluk yeniden ölçülmeli, doktrin ona göre ayarlanmalı.

**Olumlu kalibrasyon (korunacak yaklaşımlar)**
- **Combatsız, tamamen anlatı/sızma/sorgu odaklı bir oturum çok iyi karşılandı** (2026-09-07, session 21 devamı) — Tain'in kurtarılması, Grey Hall sızması, Vharkoss'un yakalanması. Bir oturumun her zaman bir setpiece dövüşü içermesi gerekmiyor.
- **Büyük NPC/aile sahnelerine tam alan ve zaman verildi** (2026-09-08, session 22) — Sethra'nın gelişi, ikna sahneleri, Vharkoss'un ölümü, Kethrax'la buluşma. Aynı sabır korunmalı.
- **Çok sayıda ipliğin tek oturumda, her birine gerçek zaman ayırarak işlenmesi** (2026-09-11, session 26) — Coren müzakeresi, cinayet soruşturması, sorgular, ittifak kurma; hiçbiri özetlenip geçilmedi.

## DM Notes (hidden from players)
- **★★★ "Şampiyon/kıdemli" etiketli düşmanlar artık gerçekten stok'tan farklı olmalı (2026-09-21, session 36, Ember Court Oda 11, oyuncu tespitiyle).** Oda 11'in "Rakshasa Şampiyonu" tasarımda bilerek stok CR13 (HP110, Oda 10'un "yönetici"siyle birebir aynı) olarak bırakılmıştı — oyuncu bunu "champion" adına yakışmıyor diye eleştirdi (tek turda neredeyse bitti). Bu fight geriye alınmadı ("öldü gitti") ama **bundan sonra Ember Court'ta (ve genel olarak) "şampiyon/kıdemli/özel" etiketi taşıyan her düşman gerçek bir sayısal farkla (HP/AC/ekstra saldırı/legendary resistance) stok versiyondan ayrılmalı** — sadece isim/flavor değişikliği yeterli değil. Oda 4 ve Oda 9'da zaten böyle yapılmıştı (Spinagon CR¼→8, Bone Devil CR9→12) — Oda 11 bu tutarlılığı bozdu, bir daha bozulmamalı.
- **★★★ Goal Tracker sistemi kuruldu (gün 186, session 31) — `scripts/goals.py` + `<campaign>/goals.json`.** Faction/NPC hedeflerini "aklında tut" prensibiyle değil, `xp.py`'nin LEVEL UP PENDING'i gibi yapısal bir eşik-takibiyle izler. Şu an kayıtlı: Sarelle (Crown parçası 0/9), Coren Ashvale, Maro Veskin, Whisper Court (ifşa olan ajan 2/3), Sereth Corr — her birinin `npcs-full.md`'de kendi `## Goal Tracker` bölümü var. **Her sahne geçişinde/continuity micro-save'de kontrol et** (bkz. SKILL.md), `/dm:dnd save`'de `goals.py check` ile tara. Eşik geçilirse script kendisi yüksek sesle uyarır — bunu session sonuna bırakma.
- **★★★ Crown parça sayısı 7'den 9'a revize edildi (2026-09-16, session 30, oyuncu tespitiyle).** Sorun: Act 2'nin (Sundered Reach) kendi "drive"ı world.md'de "kalan parçaları bulmak" diyordu, ama eski 7'lik sayıda kalan 2 parça zaten Ashvale'de (Chapter 1'in bölgesi) — Sarelle düşünce Act 2'nin fragman-arayışı amacı boşta kalıyordu. **Çözüm:** toplam 9'a çıkarıldı — 5 parti elinde, 2 Ashvale'de (Chapter 1 kapanışı, İmparator'un mühürlü lahdi), **2 tanesi de Sundered Reach'te**: 8. parça Ivrathax'ın (Frostmere, genç beyaz ejderha) hazinesinde, 9. parça Ser Oskar Thrune'un (Bonewrights yemin tutucusu, mummy lord) kendi koruduğu — Bonewrights'in orijinal kırılmadan beri elinde tuttuğu tek parça, kendi yeminine uygun bir detay. Bu, Act 2'yi gerçek bir fragman-arayışı yapıyor, sadece lore/Bonewrights yüzleşmesi değil.
- **★ Vashti Coldharrow fight — TASARLANDI (2026-09-13, session 27 sonu, oyun-dışı tasarım geçişi).** Tam tasarım `reference/vashti-coldharrow.md`'de: Emberhold-Sundered Reach yolunun kenarında (dolu Sundered Reach'e girmeden), kısa bir eşik (1 doku/warm-up encounter + custom Huge undead final boss, 460 HP, Legendary Resistance/Actions, fire zaafı, faz 2'de kontrolden çıkan specter'lar). Ödül: kanıt (Sylandra için), Frostheart amuleti (Very Rare), ~2.500-3.000 gp, Sylandra'nın tam güveni. Bir sonraki oturumda doğrudan oynanabilir, ek tasarım gerekmiyor.
- **⚠ Spellbook transcription house rate (fixed gün 114, session 24, caught by the player) — 2 saat sabit + 10 gp/seviye, spell başına, RAW'ın seviyeye göre saat ölçekleyen kuralı DEĞİL.** Session 20'nin kendi emsali (5 büyü, 10 saat, 120 gp) buradan çıkıyor: 5×2sa=10sa ✓, (1+2+3+3+3)×10gp=120gp ✓. Gelecekte bir transkripsiyon sahnesinde bu formülü kullan, RAW'ın "2sa/seviye" kuralını değil.
- **⚠ Proficiency bonus had gone stale since level 5 (caught by the player, gün 113, session 24).** Both character sheets still read "+3 (level 5)" at actual level 9 — should have been **+4** (level 9-12 band). Fixed on both sheets: all proficient skills, saves, spell save DC/attack bonus (Ilvaneth), weapon attack bonuses, breath weapon DC, and Kriv's Battle Master maneuver DC (which had also never absorbed the level 8 STR ASI to 20). None of this session's already-resolved rolls needed retroactive changes — the margins were wide enough that every outcome stays the same either way — but **check proficiency bonus explicitly at every future level-up** (5→6 doesn't change it, but 8→9, 12→13, 16→17 do) rather than assuming the character sheet already tracks it.
- **⚠ STANDING KURAL — Ser Kethrax ve ölü-doğa garnizonu asla sıradan halkın/askerlerin gözü önünde dolaşmaz (2026-09-08, oyuncu talebiyle kesinleşti).** Kethrax ve diğer retainer wight'lar Hold'un mundane hane halkı (Alis Wend, Bertrand ailesi, Corrik'in ekibi, yaşayan 15 asker, vb.) tarafından görülecek şekilde asla serbestçe dolaşmaz — bir wight'ın açıkça görülmesi köylülerde/askerlerde panik, kaos, hatta kendi askerlerinin ona saldırması riski taşır (Kethrax'ın öldürülmesi gibi istenmeyen bir sonuç dahil). **Kethrax'ın gerçek doğasını bilenler sınırlı kalmalı** (Roskel zaten biliyor, session 17). Pratikte: Kethrax ve garnizonu zindanda/gizli koridorlarda/görevli oldukları yerlerde kalır, sadece **çağrıldıklarında** (Kriv ya da yetkili biri tarafından, özel olarak) ortaya çıkar — asla "kapıda karşılıyor" ya da "avluda dolaşıyor" gibi tesadüfi bir görünürlükle sahneye girmez. Bu kalıcı bir kural, her sahne için hatırlanmalı — bugünkü (gün 106) Kethrax'ın Kriv'i kapıda karşılaması bir istisnaydı (özel olarak çağrılmıştı/bekliyordu), genel davranış değil.
- **⚠ Wardensteel — kalıcı, slot-dışı attunement sözü (2026-09-08, oyuncuyla masada anlaşıldı).** Standart 3-attunement-slot kısıtlaması masada bilinçli olarak korunuyor (gelecek loot'lar yerine attunement-gerektirmeyen "yeni oyuncak" kategorisiyle dengelenecek) — **tek istisna Wardensteel.** Kriv'in soy kılıcı, hâlâ unattuned (Barrow-King's Blade + Cloak of Elvenkind + Amulet zaten 3/3 dolu). Hikaye içinde bir eşik geldiğinde (muhtemelen evi tam olarak geri kazandığında, Flame Tongue kilidinin açılmasıyla aynı an, `kriv-thread.md`) Wardensteel Kriv'e **normal 3 slotun DIŞINDA, kalıcı ve otomatik olarak** attune olacak — bir bağ, kazanımlarının karşılığı. Şimdi olması gerekmiyor, ama geldiğinde oyuncuya sorulmadan/hatırlatılmadan uygulanmalı, bu zaten anlaşılmış bir mekanik.
- **⚠ `reference/full-campaign-history.md` — okunmalı, tahmin edilmemeli (2026-09-08 eklendi).** Session 1-18'in (orijinal repo) kararlara/sonuçlara odaklı gerçek bir tarihi — NPC/lokasyon dosyalarının veremediği "ne oldu, neden önemli" sorusuna cevap veriyor. Bu, bu oturumdaki iki gerçek tutarsızlığın (Roskel'in rolü, Gallowmere garnizonunun konumu) doğrudan sebebiydi — ikisi de sıkıştırılmış özetlere güvenip kaynağı kontrol etmemekten kaynaklandı. Kurulu bir geçmiş gerçeği (bir NPC'nin kim olduğu, bir olayın nasıl geliştiği) hakkında emin değilsen, tahmin etmeden önce bu dosyayı oku. `session-log.md`'de (yeni yapı) olmayan ama hâlâ canlı bir iplik gerektiğinde bu dosyaya bak.
- **⚠ Lokasyon indeksi kontrolü zorunlu (session 20, "The Debased Mint" olayından sonra):** `reference/lokasyon-indeksi.md` — yeni bir alt-lokasyona (özellikle Karsgate'in içinde) girmeden önce bu dosyayı tara. Bir özet (world.md, npcs.md, karsgate.md) bir yeri tek satırla anlatıyor diye ayrı, tam gelişmiş bir dosyası olmadığı anlamına gelmez — isimler bile farklı olabilir ("Old Mint" → `the-debased-mint.md`). Session 20'de bu kontrol atlanıp gerçek bir 18 odalık fragman dungeon'ı (Debased Mint) fark edilmeden geçilmişti, oyuncu fark etti.
- **Ölçek notu:** Bu kampanya dış bir repodan göç ettirildi (`C:/Users/armag/Desktop/Ashen-Crown_New_DM/original-repo/campaigns/ashen-crown/`). O repo tam tarihsel arşiv olarak kalıyor — 45 NPC, 38 lokasyon, 19 oturumun tam kaydı orada. Bu yeni yapı sadece "sıcak yol" (hot path) için yalın bir özet; derinlemesine bir NPC/lokasyon/olay gerektiğinde önce `reference/` klasörüne, sonra gerekirse orijinal repo'ya bakılmalı.
- **Chapter 2 taslağı zaten var ve güçlü** — `reference/chapter-2-outline.md`. Chapter 1 kapanınca (level 10 + 3b tamamlanınca) bunu yeniden üretmek yerine olduğu gibi Arc 2'ye uyarla (3 perde: Emberhold 11-14, Sundered Reach 15-17, Grey Kingdom 18-20, 5 tanımlı biten).
- **Ascension Tracks tam mekanik:** `reference/ascension-tracks.md` — evre tablosu, tetikleyiciler, bedeller. Fragman eşiği zaten geçildi (parti şu an **9 parçanın 5'ini** taşıyor — bkz. aşağıdaki 2026-09-16 revizyonu) — **tek kalan eşik level 11** (şu an level 10, 66,861/85,000 ve 66,686/85,000 XP — yakın). İkisi de level 11'e ulaştığında otomatik olarak Stage 2'ye geçerler: Kriv (fire immunity, +2d6 breath, claws, "territory" bedeli), İlvaneth (yemek/su/nefes gerekmez, hastalık/zehir bağışıklığı, undead komuta, "kendini onaramama" bedeli) — bkz. aşağıdaki ★ not, İlvaneth'in Stage 2'si Cinder Choir ipliğiyle doğrudan bağlanmalı.

### ★ 2026-09-10 — Büyük yapısal revizyon: Sarelle, Coren, Ilyra derinleştirildi + Chapter 1 kapanış planı

**Bağlam (2026-09-10'da DÜZELTİLDİ):** Bu bölümün ilk taslağında "parti Ashvale Necropolis'i tamamen temizledi, Sarelle'le karşılaştı ama o kaçtı" yazıyordu — bu **hiç yaşanmadı, tamamen geri alındı.** Gerçek durum: **parti Ashvale Necropolis'e hiç gitmedi.** Oturumun akışı içinde bu sahne oynandı ama sonradan oyuncuyla birlikte "bu çok erken, Sarelle daha güçlü olmalı, parti önce büyümeli" kararına varıldı — ve bu sadece Sarelle'in karakterini güçlendirmekle kalmadı, **tüm Ashvale gezisi oyun-içi zaman çizelgesinden çıkarıldı.** Parti hâlâ Karsgate'te, Vault of the Nameless'ı bitirmiş, 5 parça taşıyor, level 10 (Vault of the Nameless + House Velkarune'nin XP'siyle). Aşağıdaki tüm karakter derinleştirme çalışması (Sarelle, Coren, Ilyra, Odalys, Karsgate yeraltısı, D.V.) **gerçek, kalıcı — sadece HENÜZ oynanmadı, ileride kullanılacak hazırlık.**

**Neden Sarelle yeniden tasarlandı:** Sarelle'in orijinal tasarımı ("bu bir boss fight değil, recruitment ile girer, kaçar") Chapter 2/Emberhold'da çok daha yavaş bir girişi varsayıyordu — parti onu çok daha erken ve agresif bir şekilde bu noktaya getirmeye çalışmıştı (Ashvale sahnesi oynanırken), bu da orijinal tasarımın yetersiz kaldığını gösterdi. Oyuncuyla birlikte üçü de (Sarelle, Coren, Ilyra) yeniden derinleştirildi — tam detay `npcs-full.md`'de, özet:

- **Sarelle Duskbourne → Lawful Evil.** Artık "süreci yönetmek istiyor" değil — **parçaları KENDİSİ için istiyor, kendisi ölümü yenip hükmetmek istiyor.** D.V.'ye sadık görünüyor ama gerçekte onu da manipüle ediyor. Yöntemi: önce sinsilik/güven kazanma, işe yaramazsa doğrudan cinayet — **İmparator Ashkar Vaelthorn'u bizzat bu şekilde öldürdü** (yıllarca güvenini kazandı, sonra yavaş bir lanet/zehirle, kazı başlamadan önce değil sonra değil — zamanlaması kasıtlı). Ash-Warden hanelerinde de aynı örüntü (Draven Holt gibi aracılar).
- **Coren Ashvale → derinleştirildi.** Ashvale Necropolis'in işgali sadece iş değil, kendi atalarının mezarı. Sethra'ya (15 yıllık, "kimseye güvenme" kuralının TEK istisnası) olan güveni ihanetle sonuçlandı — bu onu kırılgan, öngörülemez, B senaryosunun en güçlü tetikleyicilerinden biri yapıyor.
- **Ilyra Thorne/Hollow Prophet → İlvaneth'e bağlandı.** On yıllık arayışının kaynağı netleşti: Wynne Ostrel'in gerçekten ölüp dönmüş olabileceğine dair doğrulanmamış bir söylenti (evi bu yüzden satın aldı). ★★★ **Kriv'in hikayesi partiyi fazla domine ediyordu (oyuncu talebiyle fark edildi) — Cinder Choir ipliği artık İlvaneth'in Ascension Stage 2'sine (level 11, yukarıya bkz.) bağlı olmalı, Kriv'in sembolik hikayesine değil.** Stage 2'nin "yemek/su/nefes gerekmez" özelliği, doktrine Kriv'in hikayesinden çok daha yakın bir "ölmüş ama devam eden" görüntüsü veriyor. İlvaneth Stage 2'ye ulaştığında, Ilyra'nın odağını organik olarak ona kaydır — İlvaneth bunu dürüstçe sunabilir ya da (Neutral Evil, Charlatan geçmişi) soğukkanlıca sömürebilir, bu tamamen oyuncunun kararı olmalı.

**Chapter 1'in gerçek kapanışı için iki senaryo, ikisi de açık tutulmalı — DM önceden karar vermeyecek:**
- **A: Gerçek bölgesel güç.** Sözü geçen liderler, gerçek ordu, gerçek kaynak — sonra Sarelle'le (şimdi çok daha güçlü/tehlikeli bir versiyonuyla) gerçek bir eşleşme.
- **B: Her şeyi kaybedip çıplak intikam.** Oyuncunun kendi sözleri: *"her şey her zaman kahramanların lehine olacak şekilde ilerlememeli, yoksa GOD MODE'da oyun oynuyoruz gibi oluyor."* B senaryosu tetikleyicileri artık sadece Sarelle değil — **her büyük faction'ın kendi misilleme potansiyeli olmalı:**
  - Coren/Ironclad Compact — Sethra ihaneti onu kırılgan/öngörülemez yaptı, tam ölçekli, mantıksız bir misilleme mümkün.
  - Cinder Choir/Ilyra — ihanete uğradığını hissederse, fanatik bir suikast dalgası.
  - The Kindled Circle — büyü imzası soruşturması düşmanca sonuçlanırsa, büyücü-karşıtı bir baskın.
  - Karsgate yeraltısı (Red Tally, Coalback) — büyüyen güç onların bölgesini tehdit ediyor, içeriden ihanet riski.
  - D.V.'nin kendisi — en büyük joker, Sarelle bile ondan çekiniyor artık.
  - **Gerçek B senaryosu tek bir düşman değil, birden fazla cephenin aynı anda açılması** — genç bir gücün büyürken yaptığı hatalar (kimlik ifşası, sivil ölümleri, ihanetler) doğal olarak buna yol açar.

**Chapter 1'in kapanışına kadar (Sarelle ile gerçek yüzleşmeden önce) önceliklendirilecek somut iplikler — hepsi paralel tutulmalı, unutulmamalı:**
1. Coren/Ironclad Compact'ın gerçek sonucu (3b) — ittifak ya da açık savaş
2. Karsgate yeraltısı (Doss/Ninefinger, Red Tally, Coalback) ile gerçek bir ittifak/kontrol
3. Hold'un garnizon büyümesinin hızlandırılması
4. Kriv'in unvanının Karsgate soylular konseyinde resmi tanınması (riskli ama güçlü)
5. The Kindled Circle ile ittifak (araştırıyorlar, düşman değil henüz)
6. Corvin Thale/Kessra Vane/Sefwyn Marrow/Fennick Orle ağının resmi bir koalisyona dönüşmesi
7. Draven Holt'u bizzat bulmak (Kriv'in kişisel görevi, D.V.'ye giden en somut iplik)
8. **House Varn'ın gizemi — artık kampanyanın D.V. sırrına doğrudan bağlı** (kukuletalı ziyaretçi, çalınmış anahtar, hiç kullanılmadı) — bkz. yukarıdaki ★★★ not ve `npcs-full.md`, "Lord Dorian Varn." Bu, partinin D.V.'ye giden en somut, en oynanabilir yol.
9. Vharkoss'un donmuş Kingsward konağı (soruşturma dosyaları, muhtemelen D.V. bağlantısı)
10. Askere alım kampı katliamı henüz keşfedilmedi — keşfedilirse Concordat'ın tepkisi çok sertleşir (B tetikleyicisi, bilinçli tutulmalı)
11. **Karsgate Undercity'nin geri kalanı + The Chalk Warrens** (2026-09-10 eklendi) — "dungeon kalmadı" hissine karşı gerçek, hazır içerik: Carrion Tangle, Choir'ın Undercity Cell'i (Kessic Ambrey, hiç ziyaret edilmedi), Vault of the First Kings, Vault of Ash, The Old Mint, Bone Market, Flooded Archive, Cloaker's Deep (Marta Vantor'un takip edilen bölgesel ödülü). Hiçbiri henüz açık iplik olarak işlenmedi — gerçekten unutulmuş, kullanılmayı bekleyen içerik.
12. **Gerçek bir vergi/gelir tabanı inşa etmek** (2026-09-10 eklendi) — bkz. aşağıdaki ★ Ekonomik Hedef tablosu. "Macera partisi" ekonomisinden (dungeon loot + tek kasaba vergisi) gerçek bir bölgesel-güç ekonomisine geçiş, Chapter 1'in A senaryosunun (gerçek bölgesel güç) somut bir ön koşulu.

### ★ Ekonomik Hedef Tablosu (2026-09-10, oyuncu onayıyla sabitlendi)

**Hedef: "gerçek bölgesel güç" eşiği — ~200 asker, ve en az 1000 gp/ay net kâr (masraf sonrası).**

| Kalem | Aylık |
|---|---|
| 200 asker maaşı + ekipman + lojistik | **-550 gp** |

| Gelir kaynağı | Aylık (aralık) | Koşul |
|---|---|---|
| Gallowmere Hazinesi (mevcut, büyüyen) | +450-500 gp | Zaten işliyor |
| Greyholt vergi tabanı | +60-90 gp | Hallik'in ziyaretiyle resmileşir |
| **Karsgate Undertow ortaklığı (Doss/Ninefinger)** | **+350-400 gp** | **✓ KURULDU (gün 123-124, session 25 devamı) — %50 pay anlaşması, ödeme Doss'a haber ulaşınca başlıyor** |
| **Iron Sella Dray / Red Tally geçiş ücreti** | **+ayrı, henüz net rakam yok** | **✓ KURULDU (gün 124) — Kriv'in üçlü anlaşmasıyla eklendi, orijinal tabloda yoktu; ilk Red Tally konvoyu limanlardan geçtiğinde netleşecek** |
| Doskarn mint/ash-metal işletmesi | +180-250 gp | **KURULUYOR (gün 125, session 25 devamı) — Kriv, Sending Stone ile Sethra'ya emir verdi, bu hafta başlıyor, demirci ustası aranıyor** |
| Ironclad Compact ittifakı (Coren) | +450-550 gp | Şarta bağlı, en büyük tek kalem — 3b'nin gerçek ittifaka dönmesi gerekir |
| Kindled Circle ittifakı | +60-100 gp | Daha çok hizmet, kısmen nakit |
| **TOPLAM GELİR (hepsi kurulursa)** | **1550-1940+ gp/ay** | Sella'nın payı bu rakama henüz dahil değil, ek |
| **NET KÂR (masraf sonrası)** | **~1000-1390+ gp/ay** | ✓ Oyuncunun hedefi karşılandı, iki hat şimdiden aktif |

**Ayrıca tek seferlik bir altyapı yatırımı gerekiyor** (gerçek surlar, garnizon binaları, silah deposu): **~2500-3500 gp bir kerelik.**

**Kritik:** Hiçbir gelir hattı otomatik değil — her biri kendi diplomasisini/kurulumunu/riskini gerektirir. Bu tablo bir tavan değil, **tüm 5 yeni hattı gerçekten kurarsanız ulaşılacak rakam.** Sadece Gallowmere + Compact ittifakı (en büyük iki kalem) bile hedefe yaklaştırır.

**Kritik:** Bunların hiçbiri unutulmamalı. Oyuncu net bir şekilde belirtti: *"Hepsini beğendim. Tümünü ekleyelim oynayacak bir sürü konu çıkacak. Unutmayalım şimdilik."*

**Aynı oturumda devam eden karakter derinleştirme çalışması (2026-09-10, aynı gün içinde):**
- Coren ve Ilyra'ya da Sarelle ile aynı formatta (Alignment dahil, eksiksiz) profil verildi — Coren **True Neutral** (B'de Neutral Evil'e kayabilir), Ilyra/Hollow Prophet **Lawful Neutral** (B'de Lawful Evil'e kayabilir).
- **The Kindled Circle'a bir lider yaratıldı: Magistrix Odalys Ferrant** (Wizard 15, Lawful Neutral) — kendisi de eskiden Necromancy'e çekilmiş, bırakmış biri; İlvaneth'in soruşturmasını bu yüzden bizzat üstlendi. İlvaneth'e üç potansiyel yön sunuyor: uyarı, ayna (disiplinin ne hale gelebileceği), fırsat (istismar edilebilir bir zaaf).
- **Karsgate yeraltısına da tam profil verildi:** Iron Sella Dray (Red Tally, Lawful Evil — gerçek hedefi Warrens değil, kirli parayı temizleyip Karsgate'in yasal gücüne sızmak) ve Ossa Vahn (Coalback, Chaotic Evil — geçmişte bir ihanetten kaynaklanan, organizasyona duyduğu içgüdüsel nefret).
- **★★★ D.V.'nin gerçek kimliği çözüldü: bir rakshasa, House Varn'ın hiç var olmamış "patriği" Lord Dorian Varn kimliğiyle kamufle.** Orijinal fikir Chapter 2'nin "Whisper Court" konseptiyle birleştirilmişti ama oyuncu bunu bilinçli olarak **Chapter 1'e çekti** ("Chapter 1'de zaten çok iş var, bu Rakshasa da eğlenceli olabilir") — House Varn ipliği (zaten açık) buna mükemmel uyuyor. Whisper Court konsepti Chapter 2'de D.V.'nin daha geniş ağı olarak hâlâ kullanılabilir. Tam detay `npcs-full.md`, "Lord Dorian Varn" entry — **bu asla erken ifşa edilmemeli, sadece gerçek keşif yoluyla ortaya çıkmalı.**
- **Genel prensip netleşti:** Bundan sonra her yeni/derinleştirilen NPC eksiksiz olmalı — Görünüş, Alignment (açık), Motivation, Secret, Kapasite, Zayıf nokta, A/B senaryosu potansiyeli. Oyuncu bunu açıkça istedi: *"HER ŞEY TAM olsun isterim eksik istemem."*

**★ Pacing disiplini (2026-09-10, oyuncu onayıyla kayda geçti):** 10 iplik + çoklu derin antagonist artık gerçek bir "fazlalık/dağılma" riski taşıyor — içerik eksikliği değil. Çözüm: **her oturumda 1-2 ipliğe gerçek odak ver, geri kalanı arka planda organik olarak öne çıksın** (bir NPC sahneye çıkar, bir haber/söylenti gelir, bir faction hamlesi fark edilir — `## Faction Moves` disiplini üzerinden). Asla hepsini aynı anda zorlama. Oyuncunun kendi sözü: *"Çok güzel öneri kayıtlara geçsin."*
- **Tüm 49 NPC artık `npcs-full.md`'de** (2026-09-06'da tam adaptasyon tamamlandı) — dışlanmış/curated-dışı NPC kalmadı. Yeni bir NPC gerekirse `/dm:dnd npc` akışıyla üret, aynı şablona uy.
- **Lokasyonlar için hâlâ geçerli bir uyarı:** 38 lokasyon dosyası hiç adapte edilmedi, sadece gerektiğinde okunuyor. Vharkoss/Sethra/Karsgate örneğinde görüldüğü gibi (düzeltildi), ilk özetler zenginliği küçümseyebilir — **bir lokasyon sahneye girmeden HEMEN ÖNCE, özete güvenmeden orijinal dosyayı oku**, özellikle Chapter 1'in klimaksına yakın (Karsgate) olanlar için.
