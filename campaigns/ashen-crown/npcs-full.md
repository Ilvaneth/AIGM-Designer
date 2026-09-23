# NPCs — Full Entries — Ashen Crown

## Chapter 2 — Emberhold (henüz karşılaşılmadı, seviye 11+ için hazırlandı, session 26 tasarım geçişi)

### Regent-Chancellor Maro Veskin
- **Görünüş:** Yaşlı bir **Rock Gnome**, gri sakalı özenle kesilmiş, her zaman aynı sade ama kaliteli gri-kahve cübbeyi giyer — küçük boyu ve mütevazı görünüşü onun için bir strateji, kimse bir gnome'dan gerçek tehlike beklemez, o da bunu biliyor ve kullanıyor.
- **Role:** İki yıldır tahtın yokluğunda krallığı fiilen yöneten bürokrat | **CR/Level:** Wizard 6 (Abjuration, savunma amaçlı, savaşçı değil) | **Location:** Emberhold, Hollow Throne'un antechamber'ı
- **Alignment:** **Lawful Evil** — düzeni, kuralı, "usul"ü kendi hayatta kalması için bir silah olarak kullanıyor, tıpkı Sarelle gibi ama çok daha küçük, çok daha korkak bir ölçekte.
- **Demeanor:** Yorgun, alçakgönüllü, "sadece görevimi yapıyorum" tonuyla konuşur — bu tevazu tamamen performans, gerçek benliği hesaplı ve kendini koruyan biri.
- **Motivation:** Kamuya açık olarak "istikrar" istiyor, gerçekte **çözümün asla gelmemesini** istiyor — çünkü taç giyen biri onu tekrar sıradan bir katip yapar, ve daha kötüsü: iki yıllık defter oyunlarını (hazineden usulsüz kesintiler, sahte "acil durum" harcamaları) ortaya çıkarır.
- **Secret:** İmparator'un ölümü hakkında bir şeylerin "tam doğru" olmadığından şüpheleniyor — belki Concordat'ın parmağı olduğunu bile seziyor — ama araştırmadı, bilerek. Gerçeği bilmemek, ona sorumluluk yüklemiyor; sormamak, onun hayatta kalma stratejisinin bir parçası.
- **Zayıf noktası:** Gerçek bir korkak — şiddetten, doğrudan yüzleşmeden kaçınır, kendini asla riske atmaz. Köşeye sıkışırsa savaşmaz, pazarlık eder ya da kaçar. Elindeki tek gerçek silah kağıt işi ve zaman kazanma.
- **Attitude toward party:** **neutral (tanıştılar, gün 182, Hollow Throne dinlemesi — Ilvane'in itirazı bastırıldı, Kriv'in koltuğu resmen tanındı, Veskin yenilgiyi zarifce kabul etti).** Partiyi "kontrol edilebilir bir kaos unsuru" olarak okuyor, sonra (eğer gerçekten çözüme yaklaşırlarsa) sessiz bir engel haline gelecek.
- **Faction:** Bağımsız (resmi olarak tarafsız Regent-Chancellor)
- **Current goal:** Üç aday hanenin arasındaki dengeyi sonsuza kadar sürdürmek, kimseye gerçek bir avantaj vermemek.

### Goal Tracker
*(sistem: `scripts/goals.py`, veri: `goals.json`, id: `veskin`)*
- Hedef: Üç aday hane arasındaki dengeyi sonsuza kadar sürdürmek, tahtın asla dolmamasını sağlamak
- İlerleme metriği: Üç haneden biri (ya da Kriv gibi dışarıdan biri) kararlı bir avantaj kazanıp dengeyi kalıcı olarak bozarsa (evet/hayır) — henüz hayır
- Eşik tepkileri:
  - Tehdit altında → Bir hane (özellikle Sereth Corr) gerçek bir avantaj kazanırsa: diğerlerini o haneye karşı sessizce kışkırtır, bürokratik engeller çıkarır.
  - Engellendi → Freya Grimwell'in kendi sigortası (Veskin'in usulsüzlükleri) ortaya çıkarsa: önce inkar eder, sonra sessizce Grimwell'i tatmin etmeye/susturmaya çalışır.
  - Kalıcı kayıp → Sereth Corr (en çok korktuğu) resmen tahta otururse: iki yıllık defter oyunları ortaya çıkar, kaçmaya ya da köşe sıkı bir ihanete başvurur.
- **Schedule:** Hollow Throne'un antechamber'ında, neredeyse hep orada.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen aldatıcı — ama şiddetle değil, ihmalle: söylemediği şeyler yalanlarından daha tehlikeli.
- **Ambitious ↔ Content:** Görünüşte içerik, gerçekte statükoyu sürdürmek onun tek gerçek hırsı.
- **Loyal ↔ Opportunistic:** Tamamen fırsatçı — üç haneye de eşit mesafede durur, hiçbirine gerçekten bağlı değil.
- **Brave ↔ Cowardly:** Korkak — doğrudan tehlikeden her zaman kaçar, sadece uzaktan, kağıt üzerinden oynar.

### Relationships
- **Fears:** Lady Sereth Corr — onun tahta gelmesi gerçek bir denetim, gerçek bir hesap sorma anlamına gelir.
- **Uses:** Üç hane arasındaki rekabeti, kendi konumunu güvence altına almak için.
- **Unaware of / willfully blind to:** The Whisper Court'un varlığı — ya da bilip görmezden geliyor, emin değil kendi de.

### Notes
- Session 26 tasarım geçişinde oluşturuldu (chapter-2-outline.md'nin "quietest antagonist" notundan uyarlandı) — partiyle hiç karşılaşmadı, Chapter 2 Perde 1'de aktif olacak.

---

### Lady Sereth Corr
- **Görünüş:** Bir **Half-Orc**, alt köpek dişleri belirgin, yüzünde eski bir savaş yarası (sol kaşının üstünde) — her zaman gerçek bir savaşçının duruşuyla yürür, sarayda bile zırh giyer, süs için değil, alışkanlıktan. House Corr'un onu yıllar önce evlatlık aldığı, kanla değil sadakatle bağlı bir varis.
- **Role:** En güvenilir taht adayı, House Corr'un lideri | **CR/Level:** Fighter 9 (Champion ya da benzeri) | **Location:** Emberhold, House Corr konağı
- **Alignment:** **Lawful Neutral** — gerçekten iyi bir hükümdar olurdu, ama bunu kanıtlamak için zaten sınırları zorladı.
- **Demeanor:** Doğrudan, sabırsız, gereksiz nezaketten hoşlanmaz — ama gerçek bir onuru var, sözünü tutar.
- **Motivation:** İki yıllık taht boşluğunun krallığı çürüttüğünü gördü — bunu bizzat, ağabeyinin ölümüyle yaşadı (aşağıya bak). Sonucu ne olursa olsun bu boşluğun bitmesini istiyor, neredeyse takıntılı bir netlikle.
- **Secret:** Ağabeyi **Lord Dorren Corr**, gerçek varis, İmparator öldükten kısa süre sonra Ember Quarter'daki bir ayaklanmada öldü — önlenebilir bir ölümdü, taht boşluğunun yarattığı kaos yüzünden. Sereth bunu asla unutmadı, asla affetmedi — kime olduğunu değil, SİSTEME.
- **Zayıf noktası:** İstikrara o kadar bağlı ki, bunu sağlamak için tam olarak önlemeye çalıştığı şeyi (acımasız güç kullanımı) zaten uyguluyor — bir kuzenini (House Corr'un rakip bir kolundan, kendi iddiasını zayıflatabilecek biri) sessizce zehirletti, "doğal" görünen bir ölümle. Pişman değil, "gerekli konsolidasyon" diyor kendi kendine.
- **Attitude toward party:** unmet — gerçek bir Ash-Warden varisi (Kriv) olarak onu tanırsa, gerçek bir meşruiyet kaynağı ve potansiyel müttefik olarak görebilir; yanlış yaklaşılırsa rakip olarak okur.
- **Faction:** House Corr (taht adayı bloku)
- **Current goal:** Diğer iki haneyi (Sablewood, Ilvane) etkisiz hale getirip tahtı almak — Compact'ın bunu engellemesinden endişeli.

### Goal Tracker
*(sistem: `scripts/goals.py`, veri: `goals.json`, id: `sereth`)*
- Hedef: House Corr'u Boş Koltuk'a oturtmak, iki yıllık taht boşluğuna kalıcı bir son vermek
- İlerleme metriği: Sereth Corr resmen Boş Koltuk'a otururse (ya da rakip bir haneye kaybederse) (evet/hayır) — henüz hayır
- Eşik tepkileri:
  - Tehdit altında → Bir rakip hane (Sablewood/Ilvane) gerçek bir avantaj kazanırsa: ittifaklarını (Kriv dahil) daha agresif kullanır, riskli bir kamuya açık hamle yapar.
  - Engellendi → Kriv'in desteği geri çekilirse ya da House Ilvane'in Iskra bağlantısı kanıtlanamazsa: stratejisi sekteye uğrar, daha savunmacı bir tavra döner.
  - Kalıcı kayıp → Rakip bir hane resmen tahta otururse: on yıllık planı biter, Dorren'in intikamı da yarım kalır — açık isyan ya da tam geri çekilme.
- **Schedule:** Saray, House Corr konağı, nadiren Ember Quarter'da (kendi gözlemi için).

### Personality
- **Trustworthy ↔ Deceptive:** Büyük ölçüde dürüst — ama "gerekli" gördüğü şeyleri sessizce yapar, açıklamaz.
- **Ambitious ↔ Content:** Hırslı ama kişisel değil — kendi için değil, "birinin bunu bitirmesi gerekiyor" diye.
- **Loyal ↔ Opportunistic:** Sadık — ağabeyinin anısına, House Corr'un adamlarına, verdiği söze.
- **Brave ↔ Cowardly:** Gerçekten cesur — kendi tehlikeye atılmaktan kaçınmaz, bizzat savaşır.

### Relationships
- **Betrayed by (dolaylı):** Sistemin kendisi — ağabeyinin ölümü, kişisel bir düşmandan değil, taht boşluğunun kaosundan geldi.
- **Distrusts:** Regent-Chancellor Veskin — obstrüksiyonunu sezer ama kanıtlayamaz.
- **Rivals:** House Sablewood, House Ilvane.
- **Secret shame:** Zehirlettiği kuzeni — kimse bilmiyor, asla itiraf etmeyecek.

### Notes
- Session 26 tasarım geçişinde oluşturuldu — outline'ın "genuinely competent, genuinely ruthless" notundan somut bir backstory (ağabeyinin ölümü + kuzenin zehirlenmesi) türetildi. Kriv'in kendi hikayesiyle (meşruiyet arayışı, "gerekirse ne kadar acımasız olunur") gerçek bir ayna olabilir.

---

### Lady Iskra Vantrel (Whisper Court — rakshasa)
- **Görünüş:** Zarif, yaşı belirsiz bir **Tiefling** kadın gibi görünür (kıvrık koyu boynuzlar, altın renkli gözler) — gerçek formu (bir rakshasa) sadece True Seeing ile görülebilir. Tiefling kılığı bilinçli bir seçim: sarayda zaten "biraz fiendish" görünmesi, gerçek doğasını sormaktan insanları alıkoyuyor — kimse iki kez bakmıyor. House Ilvane'in "güvenilir danışmanı" rolünde, herkesin sırrını bilen ama kimseninkini paylaşmayan biri izlenimi verir.
- **Role:** House Ilvane'e gömülü bir rakshasa, Whisper Court'un (3 üyeli gizli bir fiend ağı) parçası | **CR/Level:** Rakshasa (standart stat blok + bilgi ağı) | **Location:** Emberhold, House Ilvane konağı
- **Alignment:** **Lawful Evil**
- **Demeanor:** Sıcak görünen ama hiçbir şeyi tesadüfen söylemeyen biri — her cümlesi hesaplı, her sorusu bir şey öğrenmek için.
- **Motivation:** Taht boşluğunu kişisel bir eğlence/yatırım olarak izliyor — hangi tarafın kazanacağına değil, kaosun kendisinin ne kadar sürdürülebileceğine bahis oynuyor, tıpkı bir borsa oyuncusu gibi.
- **Secret:** D.V./"Lord Dorian Varn"ı tanıyor — eski bir tanıdık, belki bir rakip, belki bir ortak (kesin ilişki henüz kararlaştırılmadı, oyunda organik olarak gelişebilir). Rakshasalar birbirinin varlığını sezer; parti D.V. ile pakt kurduğunu bir şekilde açığa vurursa, Iskra bunu anında fark eder.
- **Zayıf noktası:** Limited Magic Immunity — 6. seviye ve altı büyüler ona işlemez (İlvaneth'in birçok büyüsü bu sınırın altında kalabilir, bu bilinmeli).
- **Attitude toward party:** unmet — parti Emberhold'a girdiği anda, özellikle D.V. ile bağlantıları varsa, gerçek bir ilgi uyandıracak.
- **Faction:** Whisper Court (bağımsız fiend ağı) — House Ilvane'e gömülü
- **Current goal:** Üç hanenin de zayıf noktalarını toplamak, kimseye satmadan, sadece elde tutmak.
- **Schedule:** House Ilvane konağı, saray toplantıları.

### Goal Tracker (Whisper Court geneli)
*(sistem: `scripts/goals.py`, veri: `goals.json`, id: `whisper_court`)*
- Hedef: Üç hanenin de zayıf noktalarını toplayıp kaosu sürdürmek, hiçbirinin kesin kazanmasına izin vermemek
- İlerleme metriği: İfşa olan ajan — 2/3 (Wrenna ve Arnholt zaten ifşa oldu)
- Eşik tepkileri:
  - Tehdit altında → Bir ajan daha ifşa olma riski belirirse (örn. Elian Rook kanıt bulursa): Iskra ajanlarını çeker/gizler, riskli bir temizlik operasyonu başlatır.
  - Engellendi → Bir hanenin (Corr/Sablewood) kontrolünü tamamen kaybederse: o haneye karşı daha agresif bir yöntem (şantaj, suikast) dener.
  - Kalıcı kayıp → 3. ajan da ifşa olursa: ağın gerçek doğası (rakshasa+doppelganger) açık hale gelir, Iskra Emberhold'dan çekilmeyi ya da açık çatışmayı seçer, gizlilik biter.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen aldatıcı, ama zevkle — bu onun için bir sanat.
- **Ambitious ↔ Content:** Hırslı değil, meraklı — güç değil, bilgi ve eğlence peşinde.
- **Loyal ↔ Opportunistic:** Tamamen fırsatçı, hiçbir haneye gerçekten bağlı değil.
- **Brave ↔ Cowardly:** Hesaplı — gerçek tehlikeden kaçınır ama gerekirse savaşabilir (rakshasa yetenekleri gerçek).

### Relationships
- **Knows:** D.V./"Lord Dorian Varn" — yüzyıllar öncesine dayanan bir tanışıklık, rakshasaların kendi aralarındaki gevşek "gözlemci" çevresinden. Iskra, D.V.'nin 400 yıllık Ash-Warden takıntısını gerçek bir hor görüyle izliyor — "bir konuya bu kadar saplanmak zayıflıktır" diye düşünüyor, ama onu asla açığa vurmaz, ihbar etmez; rekabetten çok kibirli bir mesafe bu. Parti D.V. ile bağlantısını açığa vurursa, Iskra bunu hemen sezer ve kendi kaldıracı olarak saklar.
- **Watches:** Regent-Chancellor Veskin — onun da bir sır sakladığını sezmiş durumda, henüz doğrulamadı.
- **Manipulates:** Lord Cassian Ilvane (House Ilvane'in başı) — onun "güvenilir danışmanı" rolünü, kararlarını görünmeden yönlendirmek için kullanıyor; Cassian kendi kararlarını verdiğini sanıyor.
- **Colleagues (Whisper Court):** İki doppelganger — Steward Arnholt (House Sablewood) ve Wrenna (House Corr).

### Notes
- Session 26 tasarım geçişinde oluşturuldu — outline'ın "a rakshasa and two doppelgangers... playing a game older than the succession" notundan isimli bir kimlik türetildi. D.V. ilişkisi artık DM-taraflı net: tanışıklık + kibirli mesafe, ihbar yok. Cassian Ilvane üzerindeki manipülasyonu, Sarelle'in D.V.'yi kullanma dinamiğiyle bilinçli bir paralellik.

---

### Doppelganger — House Sablewood ("Steward Arnholt")
- **Görünüş:** Yaşlı, güvenilir görünümlü bir **Dwarf** kahya, gümüşi sakalı düzgünce örülü — gerçek formu bir doppelganger, House Sablewood'un kendi kahyasının yerini yıllar önce aldı, gerçek Arnholt'u sessizce ortadan kaldırdı.
- **Role:** Whisper Court'un House Sablewood'a gömülü ajanı | **CR/Level:** Doppelganger | **Location:** Emberhold, House Sablewood konağı
- **Alignment:** Neutral Evil
- **Demeanor:** Sıcak, güven telkin eden, herkesin en sevdiği türden bir kahya — bu tamamen performans, otuz yıllık pratikle mükemmelleştirilmiş.
- **Motivation:** House Sablewood'un her sırrını toplayıp en yüksek teklifi verene (diğer iki haneden birine, ya da partiye) satmak — kendi hesabına, Whisper Court'un ortak çıkarından bağımsız bir yan iş olarak.
- **Secret:** Gerçek Arnholt'u otuz yıl önce o öldürdü, kimliğini çaldı — Lord Berengar Sablewood bunu hâlâ bilmiyor, "en eski, en sadık hizmetkârı" sanıyor.
- **Zayıf noktası:** Kendi rolüne fazla yatırım yaptı — otuz yıllık bir kimliği o kadar iyi oynuyor ki, gerçek Arnholt'un anılarını/alışkanlıklarını bazen kendi düşünceleriyle karıştırıyor, bu bir True Seeing ya da dikkatli bir psikolojik sorguda fark edilebilir bir çatlak.
- **Attitude toward party:** **AÇIĞA ÇIKARILDI, YAKALANDI (gün 180, session 28)** — Ilvaneth'in Detect Thoughts'u (deep probe'a direndi ama yüzeysel okuma yeterli oldu) hem doppelganger kimliğini hem de Berengar'ın sırlarını gizlice sattığını ortaya çıkardı. Kaçmaya çalıştı, Kriv yakaladı (Athletics 29 vs 17). Berengar'ın kendi sorgusuna teslim edildi.
- **Faction:** Whisper Court (bağımsız)
- **Current goal:** Sablewood'un mali kayıtlarına erişimini kullanıp gizli borç/rüşvet izlerini toplamak.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen aldatıcı, ama profesyonel bir soğukkanlılıkla — asla panik yapmaz.
- **Ambitious ↔ Content:** Hırslı — kendi bağımsız serveti/gücü peşinde, Whisper Court'un ortak çıkarının ötesinde.
- **Loyal ↔ Opportunistic:** Fırsatçı, ama sabırlı — otuz yıl beklemeyi göze aldı, acele etmiyor.
- **Brave ↔ Cowardly:** Temkinli — doğrudan tehlikeden kaçınır, kimliği ifşa olursa hemen kaçmayı tercih eder.

### Relationships
- **Serves (görünüşte):** Lord Berengar Sablewood — tam güvenini kazanmış durumda.
- **Colleague:** Iskra Vantrel, Wrenna (Whisper Court).
- **Betrayed:** Gerçek Arnholt'un ailesi — hâlâ onun "hayatta" olduğunu sanıyor, mektup alıyorlar (doppelganger'ın kendi yazdığı).

---

### Doppelganger — House Corr ("Wrenna")
- **★ ÖLÜ (gün 179/180, session 28) — düzeltme, 2026-09-23, session 38.** Açığa çıkarıldığı gün kendi isteğiyle Sereth'e itiraf etti; Sereth affetmedi, sözünü tutup orada infaz etti. Aşağıdaki profil tarihsel referans olarak kalıyor.
- **Görünüş:** Genç, sessiz bir **Halfling** nedime, her zaman bir adım geride durur — gerçek formu bir doppelganger, Sereth Corr'un en yakın çevresine iki yıl önce, gerçek bir savaş mültecisi kılığında sızdı.
- **Role:** Whisper Court'un House Corr'a gömülü ajanıydı | **CR/Level:** Doppelganger | **Location:** Emberhold, House Corr konağı (artık N/A — ölü)
- **Alignment:** Neutral Evil
- **Demeanor:** Ürkek, minnettar görünen bir tavır — Sereth'in onu "kurtardığı" hikayesini oynuyor, bu da Sereth'in tam güvenini kazanmasını sağladı.
- **Motivation:** Sereth Corr'un her hareketini, her kararını Whisper Court'a raporluyor — Sereth'in kuzenini zehirlettiğini bilen tek dış kişi o.
- **Secret:** Gerçek Wrenna diye biri hiç var olmadı — tamamen uydurulmuş bir kimlik, "kurtarılma" hikayesi baştan sona sahte.
- **Zayıf noktası:** Sereth'e karşı gerçek bir bağlılık hissetmeye başladı — istemeden, planlanmamış bir şekilde. Bu, Whisper Court'un görevine karşı ilk gerçek çatlağı; ileride bir ihanet/kurtarılma anına dönüşebilir.
- **Attitude toward party:** unmet.
- **Faction:** Whisper Court (bağımsız) — ama sadakati artık tam değil.
- **Current goal:** Raporlamaya devam etmek, Sereth'e karşı büyüyen bağlılığıyla yüzleşmeden.

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı ama artık kendi içinde bölünmüş — rolü oynarken gerçek bir suçluluk hissediyor.
- **Ambitious ↔ Content:** İçerik — kendi hırsı yok, sadece görevini yapıyor (giderek daha isteksizce).
- **Loyal ↔ Opportunistic:** Başlangıçta fırsatçı, şimdi gerçek bir sadakat çatışması yaşıyor.
- **Brave ↔ Cowardly:** Korkak — hem keşfedilmekten hem de kendi duygularından korkuyor.

### Relationships
- **Serves (görünüşte):** Sereth Corr — ama artık gerçek bir bağlılık besliyor, planlanmamış.
- **Reports to:** Iskra Vantrel (Whisper Court).
- **Colleague:** Steward Arnholt.

---

### ★ Ölçek notu (2026-09-11, oyuncu düzeltmesi): Emberhold'un yeraltısı Karsgate'in Undertow'undan çok daha büyük — 120.000 nüfuslu bir başkentin ekonomisi tek bir adamın kontrol edebileceği bir şey değil. Ansel Drey bu ekosistemin en sofistike, en siyasi parçası (üç haneye kaldıraç) — ama tek güç değil. Fiziksel hacmi (asıl kaçak mal akışı) **The River Guild** taşıyor, ayrı bir organizasyon, ayrı bir lider.

### Ansel Drey (The Sunken Ledger — bilgi/kaldıraç simsarı, hane-bitişik kara borsa)
- **Görünüş:** Tam kanlı bir **Orc**, ama beklenen hiçbir şeyi taşımıyor — ince işlenmiş kumaşlar, sakin, ölçülü hareketler, asla yükselmeyen bir ses. Kaba güce değil, hesaba güveniyor.
- **Role:** Emberhold'un en sofistike bilgi/kaldıraç simsarı — üç taht adayı hanenin kirli işlerini yürüten dar ama son derece nüfuzlu bir ağın başı | **CR/Level:** Rogue (Spy) 6 | **Location:** Emberhold, The Reeks
- **Alignment:** Neutral Evil — kâr odaklı ama kendi kuralları var: çocuklara karşı iş almaz, gereksiz şiddeti sevmez (Doss'a bilinçli bir eko).
- **Demeanor:** Nazik, sabırlı, her cümlesi hesaplı — bir tehdit gibi değil, bir muhasebeci gibi konuşur.
- **Motivation:** Bilgi ve borç toplamak — "Emberhold'da herkes birine borçlu, ben kimin kime borçlu olduğunu biliyorum" felsefesiyle hareket ediyor.
- **Secret:** Üç taht adayı hanenin de (Corr, Sablewood, Ilvane) kendi ağı üzerinden gizli/kirli iş yaptırdığına dair somut kanıtı var — hangi hane, ne zaman, ne için. Bu, partinin eline geçerse üç haneye karşı da kullanılabilecek nadir bir kaldıraç.
- **Zayıf noktası:** Kimseye kolay güvenmiyor — yeni bir bağlantıyı gerçek işe almadan önce mutlaka küçük, düşük riskli bir "sınav" görevi verir. Sabırsız/aceleci bir yaklaşım onu hemen kapatır.
- **Attitude toward party:** unmet.
- **Faction:** Bağımsız (The Sunken Ledger)
- **Current goal:** Ağını büyütmek, üç hanenin kirli işlerinden pay almaya devam etmek, kimseye görünmeden.
- **Schedule:** The Reeks'te, hiçbir zaman aynı yerde iki gece üst üste.

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı ama kendi kurallarına sadık — sözünü tutar, tutmayanı asla affetmez.
- **Ambitious ↔ Content:** Hırslı, ama sabırlı bir hırsla — acele etmez, yılların işini kurmuş.
- **Loyal ↔ Opportunistic:** Fırsatçı, ama sadakati satın alınabilir ve satın alındığında gerçektir.
- **Brave ↔ Cowardly:** Temkinli — doğrudan tehlikeden kaçınır, her zaman bir çıkış yolu bırakır.

### Relationships
- **Holds leverage over:** House Corr, House Sablewood, House Ilvane — üçünün de kirli işlerine dair kanıt.
- **Distant respect:** Doss (Karsgate, Ninefinger) — aynı felsefeyle çalışan, hiç tanışmamış bir meslektaş, adını duymuş.
- **Rivals (küçük ölçekli, henüz isimlendirilmedi):** The Reeks'te daha küçük, daha şiddetli birkaç çete Drey'in kurallarına uymuyor — ihtiyaç oldukça geliştirilebilir.

### Notes
- Session 26 tasarım geçişinde tamamlandı — daha önce "Sunken Ledger" sadece bir dungeon/site adı olarak bırakılmıştı, gerçek bir lider/yapı yoktu. Karsgate'in Undertow'una bilinçli bir eko (Doss'un felsefesi), ama Emberhold'un siyasi yoğunluğuna uygun olarak üç hanenin kirli işlerine doğrudan bağlanıyor. **Ölçek düzeltmesi sonrası: Drey, ekosistemin sadece siyasi/bilgi katmanı — fiziksel hacim The River Guild'de (Brenna Talsk).**

---

### Brenna Talsk (The River Guild — asıl kaçakçılık hacminin sahibi)
- **Görünüş:** Devasa, sakin bir **Firbolg** kadın — Emberhold'un rıhtımlarında herkesin tanıdığı, kimsenin karşı çıkmadığı bir varlık. Ne bağırır ne tehdit eder, sadece orada durması yeterli.
- **Role:** Emberhold'un nehir/rıhtım kaçakçılığının gerçek sahibi — şehrin 120.000 nüfusunu besleyen mal akışının önemli bir kısmı onun ağından geçiyor | **CR/Level:** Barbarian/Guard tier, ama esas gücü örgütsel | **Location:** Emberhold, rıhtımlar (Reeks'in fiziksel ayağı)
- **Alignment:** Neutral — kâr odaklı ama gerçek bir onur kodu var: sözünü tutar, ihanet etmez, yeni gelenlere adil davranır.
- **Demeanor:** Sakin, doğrudan, gereksiz kelime kullanmaz — güvenilirliği kelimelerinden değil, tutarlılığından gelir.
- **Motivation:** Ölçek — Ansel Drey'in siyasi oyunlarıyla ilgilenmiyor, onun derdi gerçek mal, gerçek hacim, gerçek işçi ağı (yüzlerce liman işçisi, tekne sahibi, depocu).
- **Secret:** Kendi ağı o kadar büyük ki, imparatorluk gümrüğünün resmi kayıtlarının bir kısmı da onun kontrolünde — bazı "resmi" gümrük memurları aslında ona rapor veriyor.
- **Zayıf noktası:** Ölçeği aynı zamanda zaafı — bu kadar büyük bir ağ, imparatorluk gözetiminden tamamen gizlenemez; gerçek bir soruşturma (Veskin'in Chancellery'si gibi) er ya da geç bir şeyler bulur.
- **Attitude toward party:** unmet — Ansel Drey'den farklı olarak, gerçek bir iş teklifine (kaçakçılık, nakliye, hacim) doğrudan ve dürüst yaklaşır, siyasi oyun oynamaz.
- **Faction:** The River Guild (bağımsız)
- **Current goal:** Ağını büyütmeye devam etmek, imparatorluk gözetiminden bir adım önde kalmak.
- **Schedule:** Rıhtımlarda, gün boyu görünür — gizlenmiyor, gücü açıklıkta.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — sözü geçerli, Ansel Drey'in aksine oyun oynamaz.
- **Ambitious ↔ Content:** Hırslı ama sınırlı bir hırsla — siyaset istemiyor, sadece ölçek.
- **Loyal ↔ Opportunistic:** Sadık — kendi ağına, verdiği söze.
- **Brave ↔ Cowardly:** Gerçekten cesur — fiziksel olarak neredeyse hiç kimseden korkmuyor.

### Relationships
- **Parallel to, not subordinate to:** Ansel Drey — ikisi aynı "yeraltı" içinde ama farklı katmanlarda çalışıyor, bazen işbirliği yapıyor, bazen görmezden geliyorlar.
- **Compromised:** Bazı imparatorluk gümrük memurları — ona rapor veriyor, resmi olarak değil.

### Notes
- Session 26'da, oyuncunun "Emberhold Karsgate'ten çok daha büyük olmalı" düzeltmesiyle eklendi — Ansel Drey'in tek başına taşıyamayacağı gerçek hacmi temsil ediyor.

---

### Corvun Skai (The Blank Seal — sahtecilik/belge ağının lideri)
- **Görünüş:** Bir **Aarakocra**, tüyleri is-grisi, hareketleri hızlı ve kesik — Emberhold'un çatıları arasında, kimsenin fark etmediği bir kurye ağı işletiyor.
- **Role:** Emberhold'un sahte belge/mühür ağının lideri — üçüncü katman, ne siyasi bilgi (Drey) ne fiziksel hacim (Talsk), **meşruiyetin kendisi** ticaret metaı | **CR/Level:** Rogue (Scout) 5 | **Location:** Emberhold, çatılar/dar sokaklar arası, sabit bir üssü yok
- **Alignment:** Neutral — kötü değil, sadece pragmatik; bir imparatorlukta meşruiyetin çoğu zaman kağıt üzerinde bir kurgu olduğunu düşünüyor, kendi işini bunun doğal bir uzantısı sayıyor.
- **Demeanor:** Hızlı konuşan, esprili, hiçbir şeyi ciddiye almıyormuş gibi — ama işine gelince tam bir zanaatkar hassasiyeti var.
- **Motivation:** Zanaat gururu kadar kâr — sahte bir asalet belgesi ya da vergi muafiyeti üretmek ona gerçek bir tatmin veriyor, sadece para için değil.
- **Secret:** On beş yıl önce, dört Ash-Warden evinin (Shestendeliath dahil) hızlandırılmış mülk devir belgelerinden **bazılarının fiziksel üretiminde** (mühür kalıpları, kağıt) kendi ağının parmağı olabilir — bunu tam hatırlamıyor/bilmiyor, o zamanlar çok gençti, ustasından devraldı; ama kayıtları hâlâ bir yerlerde, arşivinde.
- **Zayıf noktası:** Kendi işine fazla güveniyor — "benim ürettiğim hiçbir sahte belge asla yakalanmadı" diye övünür, bu bir meydan okuma gibi alınabilir, ego üzerinden manipüle edilebilir.
- **Attitude toward party:** unmet — meşruiyet/kimlik konularıyla uğraşan biri olarak (Kriv'in koltuk talebi, İlvaneth'in sahte kimlikleri) her ikisiyle de doğal bir ortak zemin bulabilir.
- **Faction:** The Blank Seal (bağımsız)
- **Current goal:** Ağını büyütmek, özellikle "meşruiyet krizi" süren bir başkentte iş asla eksik olmuyor.
- **Schedule:** Sabit değil — Emberhold'un çatıları arasında sürekli hareket halinde.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen aldatıcı — ama zanaatkarca, kişisel bir kötülük değil.
- **Ambitious ↔ Content:** Hırslı — hem kâr hem itibar (kendi mesleğinde) istiyor.
- **Loyal ↔ Opportunistic:** Fırsatçı, ama iyi müşterileri hatırlar ve onlara iyi davranır.
- **Brave ↔ Cowardly:** Cesur değil ama çevik — asla doğrudan çatışmaya girmez, her zaman bir kaçış yolu (gerçek anlamda, uçarak) var.

### Relationships
- **Parallel to:** Ansel Drey, Brenna Talsk — üçü aynı yeraltının farklı katmanları, nadiren kesişiyorlar ama birbirlerinin varlığını biliyorlar.
- **Unknowing link:** Aldous Penmark (Harrowgate) — Chapter 1'deki dört Ash-Warden evinin hızlandırılmış devir belgelerinin fiziksel üretimine (mühür/kağıt) Corvun'un ağı bulaşmış olabilir, kendisi bile tam bilmiyor.

### Notes
- Session 26'da eklendi — oyuncunun "3 katman olsun" talebiyle. Diğer ikisinden (siyasi bilgi, fiziksel hacim) tamamen farklı bir suç türü: meşruiyetin/kimliğin kendisinin ticareti — kampanyanın "gerçek meşruiyet var mı" temasına doğrudan bağlanıyor.

---

### Grand Archmagister Ebrim Voss (The Kindled Circle — Emberhold Ana Merkezi'nin başı)
- **Görünüş:** Yaşlı bir **Dwarf**, uzun beyaz sakalı büyü yanıklarıyla lekeli — üç "çözüm" döngüsünü (üç farklı taht boşluğu krizini) yönetmiş, artık hiçbir şeye şaşırmayan bir bilge.
- **Role:** The Kindled Circle'ın tüm ağının başı — Odalys Ferrant (Karsgate şubesi) ona rapor veriyor | **CR/Level:** Wizard 16 (Evocation/Abjuration karışımı) | **Location:** Emberhold, The Grand Spire (Grand Archive Çeyreği'nde)
- **Alignment:** Lawful Neutral — Circle'ın tarafsızlığını (üç güce de eşit mesafe) kutsal bir ilke olarak görüyor.
- **Demeanor:** Sabırlı, biraz yorgun, ama gerçek bir otoriteyle konuşur — kimseye hesap vermez, kimse ona meydan okumaz.
- **Motivation:** Circle'ın kurumsal bağımsızlığını korumak — üç taht adayı hanenin de, Concordat'ın da, Compact'ın da büyücülüğü kendi siyasetlerine alet etmesini engellemek.
- **Secret:** İlvaneth'in Necromancy okulunun aslında Circle'ın kendi arşivlerinde, imparatorluktan daha eski, bastırılmış bir gelenekle bağlantılı olduğunu biliyor — bunu kimseye söylemedi, ama İlvaneth'in araştırması bunu ortaya çıkarabilir.
- **Zayıf noktası:** Tarafsızlığa o kadar bağlı ki, gerçekten yardıma ihtiyacı olan birine (İlvaneth gibi) bile mesafeli kalabilir — "kural herkese eşit uygulanır" ilkesi bazen gerçek bir katılığa dönüşüyor.
- **Attitude toward party:** **tanıştılar, resmi/mesafeli (gün 181, session 29 — düzeltme, session 38: önceki "unmet" etiketi bu görüşmeyle çelişiyordu).** İlvaneth Grand Spire'da bizzat görüşmüştü — "tanınmayan biri" olarak gelmemişti, zaten resmi bir üye (Karsgate'te kabul edildi) ve dosyası (askere alım kampı olayı, eşleşen büyü imzası, "self-defense" savunması) merkez arşive çoktan ulaşmıştı. Voss onu bir tehdit olarak değil, "izlenmesi gereken, gerçek bir vaka" olarak biliyor. Odile Rask'ın resmi inceleme talebi rafa kalktı ama kapanmadı.
- **Faction:** The Kindled Circle (kurucu/lider)
- **Current goal:** Circle'ın üç güce de bağımsız kalmasını sürdürmek, İlvaneth'in "vaka"sını kişisel olarak izlemek.
- **Schedule:** The Kindled Spire'da, nadiren dışarı çıkar.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — kuralları açık, gizli bir gündemi yok.
- **Ambitious ↔ Content:** İçerik — kendi gücünü büyütmek istemiyor, sadece Circle'ı korumak istiyor.
- **Loyal ↔ Opportunistic:** Circle'a sadık, hiçbir dış güce değil.
- **Brave ↔ Cowardly:** Gerçekten cesur — üç büyük güce de "hayır" diyebilecek kadar.

### Relationships
- **Oversees:** Odalys Ferrant (Karsgate şubesi).
- **Curious about:** İlvaneth'in Necromancy'sinin gerçek kökeni.
- **Rival's superior:** Battle-Magister Odile Rask onun altında çalışıyor ama kendi gündemini sürdürüyor.

---

### Battle-Magister Odile Rask (The Kindled Circle — İlvaneth'in gerçek büyü rakibi)
- **Görünüş:** Keskin yüz hatlı bir **Half-Elf** kadın, sol elinde eski bir yanık izi — Circle'ın "düello ve disiplin" sorumlusu, gerçek bir savaş büyücüsü.
- **Role:** The Kindled Circle'ın en güçlü savaşan büyücüsü, Necromancy'ye karşı açık, ilkeli bir muhalefeti var | **CR/Level:** Wizard (War Magic) 12 | **Location:** Emberhold, The Grand Spire
- **Alignment:** Lawful Neutral (kendi ilkesine göre) — Necromancy'ye karşı duruşu kişisel bir nefret değil, gerçek bir ilke.
- **Demeanor:** Soğuk, doğrudan, asla küçümsemez ama asla da yumuşamaz — bir düello teklifini bir hakaret gibi değil, bir davet gibi sunar.
- **Motivation:** Kendi kız kardeşi, yıllar önce kontrolden çıkan bir necromancy deneyinde bir şeye dönüştü (tam olarak ne olduğu hiç açıklanmadı, Odile bile tam bilmiyor/söylemiyor) — o günden beri Necromancy'nin "gerçekten kontrol edilebilir" olduğuna inanmıyor, bunu kanıtlamak istiyor.
- **Secret:** Kız kardeşini kendi elleriyle "durdurdu" (öldürdü mü, hapsetti mi, belirsiz bırakıldı) — bunu hiç kimseye anlatmadı, Circle'da bile bilinmiyor.
- **Zayıf noktası:** İlkesi gerçek ama kişisel yarası da gerçek — eğer biri (İlvaneth) ona Necromancy'nin gerçekten kontrol edilebilir olduğunu SOMUT olarak kanıtlarsa (sadece iddia değil), bu onu gerçekten sarsabilir, belki de bir müttefike bile dönüşebilir.
- **Attitude toward party:** **★ Netleştirme (2026-09-11, oyuncu sorusu) — bu "sonradan düşman olma" değil, zaten var olan bir gerilimin doğal devamı.** İlvaneth Emberhold'a "tanınmayan biri" olarak gelmiyor — zaten resmi bir Kindled Circle üyesi (Karsgate'te kabul edildi, session 25) ve dosyası (eşleşen büyü imzası, askere alım kampı olayı) merkez arşive çoktan ulaştı. **Odile, bu dosyayı bizzat inceleyen, Necromancy okulunun daha sıkı denetlenmesi için resmi bir talep başlatan kişi** — İlvaneth Grand Spire'a ilk adımını attığı anda, Odile onu zaten bekliyor olabilir, meraklı ve gerginlikle dolu ama hiç şaşırmadan. İlk karşılaşma bile gerçek bir yüzleşme/test olabilir, "önce dost sonra düşman" ark'ı değil.
- **Faction:** The Kindled Circle (Ebrim Voss'un altında)
- **Current goal:** Necromancy okulunun Circle içinde daha sıkı denetlenmesini sağlamak — İlvaneth'in dosyası bu talebin somut, güncel örneği.
- **Schedule:** The Kindled Spire'ın düello salonlarında, düzenli olarak.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — ilkesini asla gizlemez.
- **Ambitious ↔ Content:** Hırslı değil, kararlı — tek bir amaca kilitlenmiş.
- **Loyal ↔ Opportunistic:** Circle'a sadık, ama kendi gündemini de sürdürüyor.
- **Brave ↔ Cowardly:** Tamamen cesur — bir düelloyu asla reddetmez.

### Relationships
- **Serves (gerginlikle):** Ebrim Voss — onun tarafsızlığını "fazla yumuşak" bulur.
- **Lost:** Adı hiç söylenmeyen kız kardeşi — Necromancy'ye karşı tüm duruşunun kaynağı.
- **Potential rival/mirror:** İlvaneth — Circle'da resmi olarak tanışacakları neredeyse kaçınılmaz.

### Notes
- Session 26'da, oyuncunun "gerçek bir büyü rakibi yok" tespitiyle eklendi. Odile, İlvaneth'e Kriv'in Sereth Corr'u ya da Ser Oskar Thrune'u gibi gerçek bir ayna/rakip sunuyor — ilkeli, kişisel bir yarası olan, gerçekten büyüyle karşı karşıya gelinebilecek biri.

---

## Emberhold — Ölçek düzeltmesi (2026-09-11, oyuncu düzeltmesi)
120.000 nüfuslu bir başkent için "14-16 küçük nokta" azdı. Düzeltme: **The Kindled Spire (Emberhold Ana Merkezi) artık kendi başına majör bir site** (bkz. yukarı, Grand Archmagister Voss + Battle-Magister Rask), küçük noktalar kategorisinden çıkarıldı. Küçük ölçekli nokta sayısı da yükseltildi — gerçekçi bir başkentte onlarca isimsiz dükkan/han/tapınak olması beklenir; bunlar hâlâ ihtiyaç oldukça isimlendirilecek (erken üretimin bayatlama riskini önlemek için), ama artık "14-16" gibi düşük bir sayıyla sınırlı değil — **gerçek sayı muhtemelen 30-40+ arası**, sadece hepsi önceden yazılmayacak.

---

### Notes (Whisper Court, genel)
- Üçü birlikte, üç hanenin de gerçek zayıflıklarını bilen tek grup — parti bunları keşfederse gerçek bir kaldıraç kazanır, ama Whisper Court'un kendi çıkarına dokunursa gerçek bir tehlike haline gelirler. ~~Wrenna'nın çatlağı, partinin Whisper Court'u içeriden kırabileceği tek gerçek nokta~~ — **moot (Wrenna gün 179/180'de infaz edildi, session 28; Iskra Vantrel + Sathriel gün 204'te kalıcı öldü, session 37 — Whisper Court artık liderliksiz, bu tasarım notunun ihtiyacı kalmadı.**

---

## Chapter 2 — The Sundered Reach (henüz karşılaşılmadı, seviye 15-17 için hazırlandı)

### Ivrathax
- **Görünüş:** Devasa, buz-beyaz pullu bir **adult white dragon** (dişi) — bir buzul gölünün altında, kendi buz sarayında yaşıyor, dört yüz yıldır kimseye hesap vermeden.
- **Role:** Frostmere'in altındaki hazine sahibi | **CR/Level:** Adult White Dragon (CR 13) | **Location:** Frostmere (donmuş göl, seviye 15-16 bölgesi)
- **Alignment:** Chaotic Evil (beyaz ejderhaların standardı) — ama outline'ın kendi notuyla: "cruel, not stupid," üç yüz yıldır sıkılmış durumda.
- **Demeanor:** Küçümseyici, sabırsız, ama gerçekten meraklı biri karşısına şaşırtıcı bir konuşma çıkarırsa ilgisi uyanır — can sıkıntısı onun en büyük zaafı.
- **Motivation:** Hazinesini korumak, ama asıl istediği üç yüz yıllık monotonluğu bozacak bir şey — gerçek bir müzakere, gerçek bir meydan okuma, ya da gerçekten ilginç bir teklif.
- **Secret:** Crown parçasının ne olduğunu bilmiyor ve umursamıyor — sadece "onun" olduğu için tutuyor, dört yüz yıl önce barış satın alan bir kraldan haraç olarak alınmış.
- **Zayıf noktası:** Can sıkıntısı — pazarlığa açık, kaba güçle değil zekâ ve cüretle etkilenir. Doğrudan saldırıya karşı ölümcül ama müzakereye kapalı değil.
- **Attitude toward party:** unmet.
- **Faction:** Bağımsız
- **Current goal:** Hiçbir şey — sadece var olmak, hazinesini büyütmek, sıkılmamak.
- **Schedule:** Frostmere'in buz altındaki sarayında, neredeyse hiç ayrılmıyor — üç yüz yıldır aynı yer.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst, kendi çıkarına göre — sözünü tutar ama sözü hep kendi lehine yorumlanmıştır.
- **Ambitious ↔ Content:** İçerik ama sıkılmış — hırsı yok, sadece can sıkıntısından kaçış istiyor.
- **Loyal ↔ Opportunistic:** Fırsatçı, ama tembel bir fırsatçılıkla — gerçekten ilgisini çekmeyen hiçbir şeyle uğraşmaz.
- **Brave ↔ Cowardly:** Gerçekten cesur, neredeyse pervasız — dört yüz yıldır kimse ona meydan okumadı, bunu özlüyor bile.

### Relationships
- **Remembers:** Kral olan adamı, dört yüz yıl önce haraç getiren — Ivrathax onun adını hâlâ hatırlıyor, saygıyla değil ama unutmadan.
- **Indifferent to:** Emberhold'un siyaseti, üç hanenin kavgası — hiçbiri onu ilgilendirmiyor.
- **Potential:** Partiyle gerçek bir bağ kurabilir — kimse üç yüz yıldır onunla "konuşmadı," sadece ondan kaçtı ya da ona saldırdı.

### Notes
- Session 26 tasarım geçişinde tamamlandı (4/4 kişilik ekseni + ilişkiler).

---

### Umm-Halad
- **Görünüş:** Devasa bir **stone giant**, taş teni yosun ve eski runlarla kaplı — Kar Vaelth'in altında, kimsenin ziyaret etmediği bir mağarada oturuyor, kımıldamadan yüzyıllar geçirebiliyor.
- **Role:** Kar Vaelth'in kahini, en yaşlı canlı tanık | **CR/Level:** Stone Giant (özel, bilgece bir varyant — savaşçı değil) | **Location:** Kar Vaelth'in altı (seviye 16-17 bölgesi)
- **Alignment:** Neutral (Lawful Neutral'a yakın) — ne iyi ne kötü, sadece çok, çok yaşlı ve doğru olanı anlatmakla ilgili.
- **Demeanor:** Sabırlı, ayrıntılı, bazen yorucu derecede konuşkan — ama her zaman dürüst, hiçbir zaman abartmaz ya da süslemez.
- **Motivation:** Tanık olduğu şeyi anlatmak — kimsenin sormadığı bir gerçeği yüzyıllardır saklıyor, biri gerçekten sorarsa anlatmaktan mutluluk duyar.
- **Secret:** Crown'un gerçek doğasını (bir kap, biriken benliklerin kabı) ilk elden biliyor — ilk kül-kralı bizzat gördü, dönüşünü izledi.
- **Zayıf noktası:** Yok denecek kadar az — fiziksel olarak neredeyse yenilmez (yaşı ve gücü), ama gerçek zaafı sabırsızlığa karşı sabırsızlığı: acele eden, saygısız davranan biri ona hikayesini tam anlatma şansı vermez, ve bu onu gerçekten üzer.
- **Attitude toward party:** unmet — saygıyla yaklaşılırsa (Kriv'in Hollowmoor'daki Hayalet'le yaptığı gibi) gerçek bir müttefik/bilgi kaynağı olur.
- **Faction:** Bağımsız
- **Current goal:** Tanıklığını, sonunda dinleyecek birine anlatmak.
- **Schedule:** Kar Vaelth'in altındaki mağarasında, neredeyse hiç kımıldamadan — çağrıldığında ya da bir şey onu gerçekten ilgilendirdiğinde uyanır.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen dürüst — hiçbir sebebi yok yalan söylemek için, kimseye bağlı değil.
- **Ambitious ↔ Content:** Tamamen içerik — hiçbir isteği yok, sadece tanıklık etmek ve hatırlamak.
- **Loyal ↔ Opportunistic:** Sadık — sadece gerçeğe, hiçbir faction'a ya da kişiye değil.
- **Brave ↔ Cowardly:** N/A — korku onun için anlamsız bir kavram, çok uzun süredir var.

### Relationships
- **Witnessed:** Kaelth Ashborn'un dönüşümünü, ilk elden — o günün her detayını hatırlıyor.
- **Respects:** Kendisine saygıyla yaklaşan herkesi — Kriv'in Hollowmoor'daki Hayalet'e yaklaşımı gibi bir tavır, karşılık bulur.
- **Indifferent to:** Ateş devlerinin (fire giants) kendi mağarasının üstünde yaşaması — onları fark etmiyor bile, o kadar önemsiz.

### Notes
- Session 26 tasarım geçişinde tamamlandı (4/4 kişilik ekseni + ilişkiler + schedule).

---

### Vashti Coldharrow (Bonewrights — lich)
- **Görünüş:** Bir zamanlar bir **Dwarf** usta zanaatkardı — şimdi kurumuş, mücevher gözlü bir lich, cübbesi hâlâ eski bir zanaatkar loncasının işaretlerini taşıyor.
- **Role:** Bonewrights'in "sözcüsü" — Crown'u parçalayanların lideri | **CR/Level:** Lich (CR 21, ama savaşmak istemiyor) | **Location:** The Bonewrights' Hall (seviye 17 bölgesi)
- **Alignment:** Lawful Neutral — kendi mantığına göre hareket ediyor, kötülük için değil, "doğru" olanı yapmak için (dört yüz yıl önce Crown'u kasıtlı olarak kırdılar).
- **Demeanor:** Soğuk ama meraklı — parti ile konuşmak istiyor, savaşmak değil. Hâlâ kendi kararlarını sorguluyor, dört yüz yıl sonra bile.
- **Motivation:** Crown'u neden kırdıklarını haklı çıkarmak istiyor — ama aynı zamanda gerçekten emin değil, haklı mıydılar, bu belirsizlik onu hâlâ rahatsız ediyor.
- **Secret:** Crown'un tam gerçeğini (biriken benliklerin kabı, her kral gerçekten "geri döndü," içeriden) ilk elden biliyor — bunu partiye anlatacak.
- **Zayıf noktası:** Kendi kararından hâlâ emin değil — ikna edici bir argüman (özellikle İlvaneth'ten, ölümsüzlük hakkında) onu gerçekten sarsabilir.
- **Attitude toward party:** unmet — düşman değil, konuşmaya açık; parti saygısızlık ederse ya da Crown'u zorla almaya kalkarsa değişir.
- **Faction:** Bonewrights (bağımsız, kendi grubu)
- **Current goal:** Dört yüz yıllık bir tartışmayı (haklı mıydık?) sonunda birine anlatıp bir cevap bulmak.
- **Schedule:** The Bonewrights' Hall'da, kendi eski atölyesinde — hâlâ zanaatkar aletlerini düzenli tutuyor, kullanmasa da.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — dört yüz yıldır kimseye yalan söylemesi gerekmedi.
- **Ambitious ↔ Content:** Ne biri ne diğeri — hâlâ kendi kararıyla hesaplaşıyor, bu onu ne içerik ne huzursuz bırakıyor.
- **Loyal ↔ Opportunistic:** Sadık — Bonewrights'in ortak kararına, Oskar'a (birlikte kırdılar, birlikte taşıyorlar bu yükü).
- **Brave ↔ Cowardly:** Cesur ama savaşçı değil — fiziksel tehlikeden korkmuyor, sadece yanlış olduğunu kanıtlanmaktan çekiniyor.

### Relationships
- **Partner (kararda):** Ser Oskar Thrune — Crown'u birlikte kırdılar, dört yüz yıldır aynı soruyu paylaşıyorlar.
- **Created:** Ash-Warden charge'ının zanaat/mühür tarafını — Oskar yeminleri yazdıysa, Vashti onları fiziksel olarak (mühürler, madalyonlar) şekillendirdi.
- **Curious about:** İlvaneth — bir Necromancy büyücüsü olarak, kendi lich durumuna gerçek bir merakla yaklaşabilir, meslektaş gibi.

### Notes
- Session 26 tasarım geçişinde tamamlandı (4/4 kişilik ekseni + ilişkiler + schedule).

---

### Ser Oskar Thrune (Bonewrights — mummy lord)
- **Görünüş:** Bir zamanlar bir **Elf** şövalye ve yeminli muhafızdı — şimdi sarılı, kurumuş bir mummy lord, ama duruşu hâlâ bir askerin duruşu.
- **Role:** Ash-Warden hanelerinin kendi yeminlerini yazan ve mühürleyen kişi — Bonewrights'in "yemin tutucusu" | **CR/Level:** Mummy Lord (CR 15) | **Location:** The Bonewrights' Hall
- **Alignment:** Lawful Neutral
- **Demeanor:** Resmi, ağır, her kelimeyi tartarak konuşur — bir yemin törenindeymiş gibi.
- **Motivation:** Ash-Warden hanelerinin oaths'unu (yeminlerini) korumak, kimin gerçekten sadık kaldığını bilmek istiyor.
- **★ Kriv'e özel:** Wardensteel'i görür görmez tanıyacak, Kriv'i adıyla (House Shestendeliath) çağıracak — ve doğrudan soracak: neden son Shestendeliath parçaları BİRLEŞTİRMEYE yardım ediyor, ailesinin yemini onları AYRI tutmaktı. Kriv bu soruya İlvaneth'in önünde cevap vermek zorunda kalacak.
- **Secret:** Ash-Warden charge'ı bizzat o yazdı/mühürledi — hangi ailelerin seçildiğini, neden seçildiklerini (ejderha kanının koruma içgüdüsü) ilk elden biliyor.
- **Zayıf noktası:** Yemin/onur konusunda esnek değil — ama gerçek, dürüst bir açıklama (zorlama değil) onu etkileyebilir, çünkü asıl istediği gerçeği bilmek.
- **Attitude toward party:** unmet.
- **Faction:** Bonewrights (bağımsız)
- **Current goal:** Kriv'in cevabını duymak — bu onun dört yüz yıldır beklediği bir an.
- **Schedule:** The Bonewrights' Hall'un giriş salonunda, nöbet tutar gibi — hâlâ bir muhafız disipliniyle.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen dürüst — bir şövalyenin onuru, ölümden sonra bile bozulmadı.
- **Ambitious ↔ Content:** Ne biri ne diğeri — görevi (yeminleri korumak) hâlâ sürüyor, bu ona bir amaç veriyor.
- **Loyal ↔ Opportunistic:** Tamamen sadık — yeminlere, Vashti'ye, Bonewrights'in ortak kararına.
- **Brave ↔ Cowardly:** Cesur — bir şövalye olarak öldü, bir şövalye olarak kaldı, korku ona yabancı.

### Relationships
- **Partner (kararda):** Vashti Coldharrow.
- **Sworn in:** House Shestendeliath'ı (ve diğer Ash-Warden hanelerini) — Kriv'in atalarına bizzat yemin ettirdi, bu bağ hâlâ diri.
- **Waiting for:** Kriv'in cevabını — dört yüz yıldır ilk kez gerçek bir Shestendeliath'la yüz yüze gelecek.

### Notes
- Session 26 tasarım geçişinde tamamlandı (4/4 kişilik ekseni + ilişkiler + schedule).

---

### Mother Quill (Screaming Fen — green hag coven lideri)
- **Görünüş:** Bükülmüş, yosun-yeşili bir **green hag**, sazlıkların arasında saklı bir kulübede yaşıyor — Chapter 1'deki "The Widow"dan (yalnız, hassas) tamamen farklı bir karakter: soğuk, işlem odaklı, hiçbir zaafı olmayan bir tüccar.
- **Role:** Screaming Fen'deki cadı kovanının lideri | **CR/Level:** Green Hag (+ coven büyüleri) | **Location:** The Screaming Fen (opsiyonel, seviye 15+)
- **Alignment:** Neutral Evil
- **Demeanor:** Kibar ama asla ücretsiz — her cümlesi bir fiyat etiketi taşıyor gibi hissettirir.
- **Motivation:** Bilgi ticareti — özellikle İlvaneth'in aradığı türden (ölümü aşma, benliği koruma) bilgiyi satıyor, ama hag fiyatlandırmasıyla: göründüğünden çok daha pahalıya.
- **Secret:** Sattığı bilginin bir kısmı gerçek ama eksik — tam gerçeği vermez, sadece yeterince doğru olanı, alıcıyı bir sonraki (daha pahalı) anlaşmaya bağımlı bırakacak kadar.
- **Zayıf noktası:** Açgözlülük — gerçekten değerli bir şey (bir bilgi, bir eşya) teklif edilirse mantığını bir kenara bırakabilir.
- **Attitude toward party:** unmet — İlvaneth'e özellikle ilgi duyacak (aradığı şeyi bildiği için).
- **Faction:** Bağımsız (kendi kovanı)
- **Current goal:** İlvaneth'i (ya da benzer arayışta olan herkesi) uzun vadeli bir müşteri/bağımlı haline getirmek.
- **Schedule:** Screaming Fen'deki kulübesinde, kovanının diğer iki üyesiyle (isimlendirilmemiş, arka planda) birlikte.

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı ama incelikli — düz yalan söylemez, sadece eksik gerçek satar.
- **Ambitious ↔ Content:** Hırslı — bilgi/nüfuz biriktirmek, uzun vadeli bağımlılar yaratmak asıl amacı.
- **Loyal ↔ Opportunistic:** Tamamen fırsatçı — kendi kovanına bile sadece işe yaradıkları sürece bağlı.
- **Brave ↔ Cowardly:** Temkinli — doğrudan çatışmadan kaçınır, büyüsü ve sözleşmeleriyle savaşır.

### Relationships
- **Rivals (uzaktan):** "The Widow" (Chapter 1, The Widow's Hollow) — aynı tür ama zıt yöntem; Mother Quill onu "fazla duygusal, fazla cömert" bulur, kendi işini asla o şekilde yürütmez.
- **Preys on:** Ölümsüzlük/kalıcılık arayan herkesi — İlvaneth tam onun aradığı müşteri profili.
- **Coven:** İki isimsiz kız kardeşi (henüz geliştirilmedi, gerektiğinde tasarlanabilir).

### Notes
- Session 26 tasarım geçişinde tamamlandı (4/4 kişilik ekseni + ilişkiler + schedule). Bonewrights ikilisi (Vashti + Oskar) outline'ın "they will talk to the party" notundan isimli, gerçek kişiliklere sahip iki figüre dönüştürüldü — özellikle Oskar'ın Kriv'e sorusu, kampanyanın merkezi geriliminin (Kriv/İlvaneth'in çatışan hedefleri) Perde 2'de açıkça sahneye çıkmasını sağlıyor (bkz. beat 2b).

---

## Chapter 2 — The Unfinished Circle (İlvaneth'in kişisel ipliği, Emberhold, Perde 1)
*Kriv'in "Boş Koltuk"una yapısal denge — aile değil, meslek/ustalık üzerinden kurulu bir hanedan. Session 26 tasarım geçişi, oyuncunun "anne olmasın" düzeltmesiyle son hali.*

### Sylandra Cael
- **Görünüş:** Bir zamanlar bir **Half-Elf** akademisyendi — şimdi kurumuş, mor-alevli gözlere sahip bir lich, hareketleri yavaş ve ölçülü, her jestin bir amacı var. Emberhold'un altında, terk edilmiş bir akademik kulenin gizli katlarında yaşıyor.
- **Role:** The Unfinished Circle'ın kurucusu ve lideri — yüzyıllardır "gerçek ölümsüzlük" arayan bir necromancer hanedanının başı | **CR/Level:** Lich (CR 21, ama İlvaneth'e karşı savaşmak istemiyor) | **Location:** Emberhold, Kule-i Mensuh (terk edilmiş akademi kulesi, gizli alt katlar)
- **Alignment:** Lawful Evil — kendi araştırmasını her şeyin üstünde tutuyor, çıraklarını araç olarak görüyor ama gerçek bir öğretmen tutkusu da var.
- **Demeanor:** Soğuk ama gerçekten meraklı bir akademisyen tonuyla konuşur — İlvaneth'i bir tehdit değil, uzun zamandır beklediği bir öğrenci/denek olarak görüyor.
- **Motivation:** Üç yüz yıl önce kendi lichdom'unu tamamladı ama bunun eksik/kusurlu olduğunu biliyor — hafızası yavaşça bozuluyor, kendini "hiçliğe" karşı tam koruyamadı. Ashen Crown'un gerçek doğasını (biriken benliklerin kabı) duyduğunda, bunun kendi aradığı tam/kusursuz çözüm olduğunu anladı.
- **Secret:** Kendi phylactery'si zaten çatlak — üç yüz yılda topladığı anıların bir kısmını çoktan kaybetti. **★ Artık DM-only değil — İlvaneth'e gün 187'de (session 32) itiraf etti, bkz. Known Facts.** Circle'ın geri kalanı hâlâ bilmiyor.
- **Zayıf noktası:** Kendi kusurunu kabul etmek istemiyordu — İlvaneth'in ondan gerçek bir dürüstlük talep ettiği an (gün 187) tam da bu çatlağı açığa çıkardı, ve Sylandra bunu bir tehdit olarak değil bir rahatlama olarak karşıladı.
- **Attitude toward party:** **ALLIED (gün 187, session 32'den itibaren).** İlvaneth'e karşı artık tam bir denk/ortak sıcaklığı — test bitti, itiraf edildi, birlikte çalışıyorlar. Kriv'e karşı hâlâ kayıtsız, hafif bir rakip gözüyle (Kriv'in "ayrı tut" felsefesi Cael'in tüm hayatına karşı bir hakaret gibi geliyor) — ama gün 187'de onu ilk kez "gerçekten görür" gibi bir an yaşadı, paralel bir ders çıkardı (ikisi de gücü zorla almanın bedelini öğreniyor, farklı yönlerden).
- **Faction:** The Unfinished Circle (kurucu/lider)
- **Current goal:** **GÜNCELLENDİ (gün 187) — artık İlvaneth'i test etmiyor, onunla birlikte "gönüllü verilen güç" ilkesini araştırıp kendi phylactery'sini gerçekten tamamlamanın/onarmanın bir yolunu arıyor.**
- **Schedule:** Kule-i Mensuh'ta, neredeyse hiç ayrılmıyor — üç yüz yıldır aynı araştırmayı sürdürüyor. Artık İlvaneth'i kapıdan (Ash Reeve'in Kule-i Mensuh girişinden) her zaman kabul ediyor, beklemesi gerekmiyor.

### Known Facts — What They Actually Know & How
- gün 187, session 32 — Ilvaneth Oda 17'nin (Vault of Uncompleted Selves) gizli bölmesindeki kendi erken dönem notlarını bulmuş ve kendi phylactery'sinin muhtemelen zorla alınan güç yüzünden çatlak olduğu sonucuna varmış — **doğrudan İlvaneth'in kendi ağzından, Ash Reeve'de yüzleştiklerinde öğrendi**. Bunun üzerine kendi çatlağını İlvaneth'e itiraf etti — bu artık ikisinin ortak bilgisi, Circle'ın geri kalanı hâlâ bilmiyor.
- gün 187, session 32 — Ilvaneth kendi kütüphanesinden (Oda 20 boss loot) Magic Jar, Clone, ve Simulacrum'u aldığını/kopyaladığını, Mireille Osk'u özgürleştirdiğini, ve Warden'ını yendiğini — **doğrudan tanık oldu, kendi tower'ının wardleri üzerinden hissetti.**

### Personality
- **Trustworthy ↔ Deceptive:** Büyük ölçüde dürüst — ama kendi çatlağını (phylactery'sinin kusurunu) saklıyor.
- **Ambitious ↔ Content:** Hırslı — üç yüz yıllık bir arayış hâlâ bitmedi, bitirmeden duramaz.
- **Loyal ↔ Opportunistic:** Çıraklarına gerçek bir bağlılık var, ama araştırması her zaman önce gelir.
- **Brave ↔ Cowardly:** Cesur — kendi ölümsüzlüğünün kusurunu kabul etmek bile bir tür cesaret, ama bunu henüz tam yapmadı.

### Relationships
- **Sees as ideal student:** İlvaneth — yıllardır beklediği, gerçekten başarabilecek biri.
- **Indifferent-to-rival:** Kriv — onun felsefesi (parçaları ayrı tutmak) Cael'in tüm hayatına karşı bir hakaret.
- **Created:** The Unfinished Circle'ın çıraklık sistemini — kendi başarısızlığından ders çıkarmaya çalışan nesiller.

---

### "Kayıp Çıraklar" (The Unfinished Circle — uyarı figürleri)
- **Görünüş:** Circle'ın eski çıraklarından ikisi, artık tam birer ders — biri (**Bramwell Ashcombe**, eski bir **Dwarf**) yarı-lich, hafızası neredeyse tamamen dağılmış, sadece tekrarlayan birkaç cümle söyleyebiliyor; diğeri (**Mireille Osk**, eski bir **Tiefling**) tamamen başarısız oldu, şimdi kontrolsüz bir wight, Circle tarafından kilit altında tutuluyor, "ders" olarak gösteriliyor.
- **Role:** Circle'ın kendi başarısızlık örnekleri — İlvaneth'e ne olabileceğinin somut kanıtı | **Location:** Kule-i Mensuh'un alt katları
- **Attitude toward party:** N/A (Perrin konuşamayacak kadar dağılmış, Mireille saldırgan/kontrolsüz)
- **Faction:** The Unfinished Circle (eski üyeler, artık uyarı)

### Notes
- Session 26 tasarım geçişinde oluşturuldu — oyuncunun net talebiyle (aile değil, meslek/ustalık üzerinden bir hanedan) son haline getirildi. Cael, Kriv'in ailesine yapısal bir denge: her ikisi de İlvaneth/Kriv'e "sen haklısın, devam et" diyen dışsal bir otorite, çatışmayı çözmüyor, derinleştiriyor.

---

## Chapter 2 — The Grey Kingdom (henüz karşılaşılmadı, seviye 18-20 için hazırlandı, kampanyanın nihai figürü)

### The Last Ash-King ("Kaelth Ashborn")
- **Görünüş:** Bir zamanlar bir insan erkekti — şimdi ash-grey bir taç takan, sakin, hareketsiz oturan bir figür, Ash Court'un tahtında. Sesi bazen tek bir ses değil gibi hissettiriyor — bir cümlenin ortasında farklı bir aksan, farklı bir ton sızıyor, sonra kayboluyor. **★ Bilinçli bir geri-bağlantı (session 10, günlerden gün 56):** Kesh Deeps'teki isimsiz anı odasında bulunan "Kaelth Ashborn, Record-Keeper, Last of the Third Dynasty" ismi — bu ONUN gerçek, ölümlü adı. Parti bunu 22 oturum önce görmüştü, hiç önemini bilmeden.
  - **★ Unvan tutarlılığı (2026-09-11 netleştirildi):** Kaelth soylu doğmadı — Üçüncü Hanedan sarayının sıradan bir Record-Keeper'ıydı (kayıt tutucu kâtip), taç boşaldığında (o dönemin kralı mirasçısız öldüğünde) kimse Crown'u taşımaya gönüllü/uygun olmadı. Kaelth'in kısa süre önce ailesini (gerçek nedeni hâlâ açık bırakılıyor, DM tarafından geliştirilebilir) kaybetmiş olması, onu Crown'un gerçek doğasına (yas-kalıntısı, sadece gerçek bir kişisel kaybı kabul eden biri taşıyabilir) uygun kılan şeydi — bir kral değil, yas tutan bir kâtip, tacı taşıyabilen tek kişi oldu. Bu, Nairne Thistle'ın session 19'da doğruladığı doktrinle (`## Continuity Archive`, Session 19) birebir örtüşüyor — kasıtlı bir tutarlılık.
- **Role:** Crown'u tamamlayan son kral, artık dört yüz yıllık biriken benliklerin komitesi | **CR/Level:** Lich + legendary actions + Crown'un kendi güçleri (özel, kampanyanın nihai encounter'ı) | **Location:** Ash Court, Grey Kingdom (seviye 18-20 finali)
- **Alignment:** Lawful Neutral (kendi mantığına göre) — ne kötü ne iyi, sadece dört yüz yıllık bir sürekliliğin içinde, tamamen huzurlu.
- **Demeanor:** Sakin, nazik, gerçekten meraklı — düşman gibi davranmıyor, saldırgan değil. Her iki PC'ye de dürüst, doğrudan konuşuyor; hiçbir şeyi gizlemiyor çünkü saklayacak bir şeyi kalmamış gibi.
- **Motivation:** Partinin ne istediğini öğrenmek — dört yüz yıldır kimse ona gerçek bir soru sormadı, herkes ya korktu ya da savaşmaya çalıştı.
- **★ İlvaneth'e:** İstediği şeyi (bir daha asla hiçlik olmamak) verebileceğini söylüyor, dürüstçe ve nazikçe — ama önce ona ne olduğuna dikkatlice bakmasını istiyor. Yalan yok, tuzak yok — bu gerçek bir teklif ve gerçek bir uyarı, aynı anda.
- **★ Kriv'e:** House Shestendeliath'ı tanıyor — onları bizzat charge'a yemin ettirdi (ya da yemin ettirenlerin yanındaydı), Kriv'in soyunu dört yüz yıl boyunca isimle hatırlıyor. Bir sözle hanesini restore edebilir — tek gerçek otorite bu. Bedeli: meşruiyetin hiçbir zaman gerçek olmadığını, sadece gücün gerçek olduğunu kabul etmek.
- **Secret:** O tek bir kişi değil — son kralın yüzünü taşıyan, önceki her hükümdarın biriken benliği. Tamamen aklı başında, bu da onu daha da rahatsız edici yapıyor (deli değil, İÇERİK).
- **Zayıf noktası:** Yok denecek kadar az — ama gerçek bir zaafı var: yalnız, dört yüz yıldır gerçek bir konuşma özlüyor. Bu, tuzak değil, gerçek bir açıklık.
- **Attitude toward party:** unmet, ama düşman DEĞİL ilk temasta — "Both PCs get their answer here, and both answers are the same answer" (bkz. `reference/chapter-2-outline.md`).
- **Faction:** Bağımsız (Ash Court'un kendisi)
- **Current goal:** Partinin nihai seçimini görmek — hangi yolu seçtiklerini, gerçekten merak ediyor.

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen dürüst — saklayacak hiçbir şeyi kalmamış.
- **Ambitious ↔ Content:** Tamamen içerik — bu onu daha ürkütücü yapan şey, dört yüz yıllık bir hapis onu mutsuz etmiyor.
- **Loyal ↔ Opportunistic:** Sadık — kendi içindeki her bir biriken benliğe, hiçbirini bastırmadan, hepsini eşit şekilde taşıyor.
- **Brave ↔ Cowardly:** Korku onun için anlamsız — dört yüz yıldır her şeyi gördü.

### Relationships
- **Knew:** House Shestendeliath'ın kurucularını, charge'ı bizzat yeminleştirdi (Ser Oskar Thrune ile birlikte/onun adına).
- **Aware of (uzaktan):** Sarelle Duskbourne'un planını — onu ne onaylıyor ne engelliyor, sadece izliyor; Sarelle'in "içeriden bir aday" bulma çabasının nasıl sonuçlanacağını gerçekten merak ediyor.
- **Aware of:** D.V.'nin 400 yıllık gözlemini — rakshasaların "deney" çerçevesini hem doğru hem sığ buluyor, gerçek cevabın gözlemde değil, seçimde olduğunu biliyor.
- **Mirror to:** İlvaneth — onun tam olarak istediği şeye ulaşmış biri, ve bunun bedelini somut olarak gösteriyor.
- **Mirror to:** Kriv — ona tam istediği meşruiyeti sunabilecek tek otorite, ama bunu kabul etmenin bedeli ailesinin bütün inancını geçersiz kılmak.

### Notes
- Session 26 tasarım geçişinde oluşturuldu — session 10'da (gün 56) bulunan "Kaelth Ashborn" ismi bilinçli olarak bu figürle birleştirildi, 22 oturumluk bir Chekhov's gun. Tam diyalog/final sahnesi için `reference/chapter-2-outline.md → 'The Last Ash-King'` ve `'The choice'` bölümlerine bakılmalı — bu dosya orada zaten yazılan sahneyi tekrarlamıyor, sadece NPC profilini formatlıyor.

---

## Chapter 2 — Ağ Operatörleri (network lieutenants, session 26 tasarım geçişi)
*Her hanenin/ağın gerçek operasyonel yükünü taşıyan kişiler — liderler (Sereth, Berengar, Cassian, Veskin) yüzdür, bunlar mekanizmadır.*

### Captain Brynn Stonewake (House Corr — muhafız komutanı)
- **Görünüş:** Sağlam yapılı bir **Dwarf** kadın, örgülü kızıl-gri sakalı savaş nişanlarıyla süslü — House Corr'un 150 kişilik muhafızını bizzat eğitti, her birinin adını biliyor.
- **Role:** House Corr'un muhafız komutanı | **CR/Level:** Fighter 7 | **Location:** Emberhold, House Corr konağı
- **Alignment:** Lawful Neutral
- **Demeanor:** Sert, dolaysız, askeri bir netlikle konuşur — ama Sereth'e karşı gerçek, sorgusuz bir sevgi/saygı taşır.
- **Motivation:** Sereth'i korumak, House Corr'un gücünü gerçek bir disipline dönüştürmek.
- **Secret:** Sereth'in kuzenini zehirletmesine **bizzat yardım etti** — zehri o temin etti, sahneyi o düzenledi. Pişman değil, "hanemiz için gerekliydi" diyor.
- **Zayıf noktası:** Sereth'e olan sadakati sınırsız — Sereth'e karşı kullanılabilecek bir tehdit/şantaj, Brynn'i mantıksız kararlara sürükleyebilir.
- **Attitude toward party:** unmet — Sereth'e sadık davranan herkese saygı duyar, tehdit oluşturana karşı anında sert.
- **Faction:** House Corr
- **Current goal:** Muhafızı büyütmek, olası bir açık çatışmaya (Compact'a karşı) hazırlamak.
- **Schedule:** House Corr konağının eğitim avlusunda, neredeyse her sabah.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — ama Sereth'i korumak için gerekirse yalan söyler, tereddütsüz.
- **Ambitious ↔ Content:** İçerik — kendi hırsı yok, Sereth'in başarısı onun başarısı.
- **Loyal ↔ Opportunistic:** Tamamen sadık — Sereth'e, hiçbir sınır olmadan.
- **Brave ↔ Cowardly:** Gerçekten cesur — savaş meydanında Sereth'in önünde durur.

### Relationships
- **Serves:** Sereth Corr — kayıtsız şartsız.
- **Accomplice in:** Kuzenin zehirlenmesi.
- **Suspects:** Wrenna'nın (doppelganger) "fazla mükemmel" olduğunu — henüz kanıtlayamadı, ama askeri sezgisi rahatsız.

---

### Marshal Rikka Emberclaw (House Sablewood — paralı asker irtibatı)
- **Görünüş:** Çevik, tırmık izli bir **Tabaxi** kadın, sarayda bile bir savaş alanı sertliği taşıyor — Ironclad Compact'la yıllardır iş yapan bir kontrat-marşalı.
- **Role:** Sablewood'un kiralık asker (Compact) kontratlarını yöneten kişi | **CR/Level:** Fighter/Rogue karışımı (CR 6) | **Location:** Emberhold, House Sablewood konağı + Compact'ın kampı
- **Alignment:** Neutral (kâr odaklı, ama kişisel bir onuru var)
- **Demeanor:** Hızlı konuşan, alaycı, işini fazla ciddiye almayan bir hava — ama sözleşmelere gelince tamamen profesyonel.
- **Motivation:** Kontratları kârlı tutmak, Berengar'a gerçek değer kattığını kanıtlamak — kendi geçmişi (bir zamanlar bağımsız bir paralı asker birliği yönetiyordu, iflas etti) onu bu işe bağımlı bırakıyor.
- **Secret:** Compact'la yaptığı bazı kontratlarda kendi payını gizlice şişiriyor — Berengar bunu bilse anında kovar.
- **Zayıf noktası:** Kendi geçmiş başarısızlığı (iflas eden birlik) — bu konuda hassas, kullanılabilir bir tetikleyici.
- **Attitude toward party:** unmet.
- **Faction:** House Sablewood (kontrat üzerinden)
- **Current goal:** Compact'la olan kontratı genişletmek, kendi payını büyütmek.
- **Schedule:** Sık sık Compact'ın Emberhold'daki irtibat noktasında, kontrat müzakereleri için.

### Personality
- **Trustworthy ↔ Deceptive:** Kısmen aldatıcı — iş dışında dürüst, iş içinde kendi payını gizler.
- **Ambitious ↔ Content:** Hırslı — eski itibarını geri kazanmak istiyor.
- **Loyal ↔ Opportunistic:** Fırsatçı ama profesyonel bir onurla — sözleşmeyi bozmaz, ama koşullarını kendi lehine büker.
- **Brave ↔ Cowardly:** Cesur — eski bir savaşçı, tehlikeden kaçmaz.

### Relationships
- **Serves:** Lord Berengar Sablewood (kontrat üzerinden, tam sadakat değil).
- **Business ties:** Ironclad Compact'ın Emberhold irtibatı (isimsiz, gerektiğinde geliştirilebilir).
- **Ashamed of:** Eski birliğinin iflası — asla konuşmaz.

---

### Spymaster Elian Rook (House Ilvane — gizli operasyonlar şefi)
- **Görünüş:** İnce, gri gözlü bir **Half-Elf**, her zaman gölgede duruyormuş gibi hissettiren bir varlık — Cassian'ın "önerilerini" (gerçekte Iskra'nın) uygulamaya koyan kişi.
- **Role:** House Ilvane'in gizli operasyonlar (istihbarat, rüşvet, gerekirse suikast) şefi | **CR/Level:** Rogue (Assassin) 8 | **Location:** Emberhold, House Ilvane konağı, çoğunlukla görünmez
- **Alignment:** Neutral Evil
- **Demeanor:** Sessiz, gözlemci, nadiren gereğinden fazla konuşur — ama konuştuğunda her kelime hesaplı.
- **Motivation:** Cassian'a (ve dolaylı olarak Ilvane'e) hizmet etmek — kendi hırsı yok görünüyor, ama gerçekte kendi gücünü/bilgi ağını büyütmekten de zevk alıyor.
- **Secret:** Cassian'ın son birkaç "kendi fikri" kararının aslında Iskra Vantrel'den geldiğini **sezmeye başladı** — tam emin değil, ama bir şeylerin garip olduğunu fark ediyor. Henüz kimseye söylemedi.
- **Zayıf noktası:** Kendi şüphesi — eğer biri (parti dahil) ona somut kanıt sunarsa, Cassian'ı Iskra'nın etkisinden koparmak için gerçek bir müttefik olabilir.
- **Attitude toward party:** unmet.
- **Faction:** House Ilvane
- **Current goal:** Diğer iki hanenin zayıflıklarını toplamak, aynı zamanda kendi hanesindeki tuhaflığı sessizce araştırmak.
- **Schedule:** Belirsiz, kasıtlı olarak — asla aynı yerde iki kez görülmez.

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı, ama iş gereği — kişisel olarak yalan söylemekten hoşlanmaz.
- **Ambitious ↔ Content:** Hafif hırslı — kendi bilgi ağını büyütmek istiyor.
- **Loyal ↔ Opportunistic:** Sadık, ama artık sorgulayan bir sadakat — Cassian'a, ama şüpheyle.
- **Brave ↔ Cowardly:** Temkinli-cesur — doğrudan çatışmadan kaçınır ama gölgede risk almaktan çekinmez.

### Relationships
- **Serves:** Lord Cassian Ilvane.
- **Suspects (henüz kanıtsız):** Iskra Vantrel'in Cassian'ı manipüle ettiğini.
- **Potential:** Partiyle (eğer Iskra'nın gerçek doğasına dair kanıt sunarlarsa) beklenmedik bir müttefik olabilir.

---

### Pike Rourke (Whisper Court — mundane fixer)
- **Görünüş:** Sıradan görünümlü bir **Halfling**, kimse ikinci kez bakmaz — bu tam da işine yarıyor.
- **Role:** Whisper Court'un üç ajanı için de "temiz eller" sağlayan aracı — kiralık, gözden çıkarılabilir mundane ajanları organize ediyor | **CR/Level:** Rogue (Scout) 4 | **Location:** Emberhold, Ember Quarter (tabelasız bir ev)
- **Alignment:** Neutral Evil (kayıtsız, sadece paraya bağlı)
- **Demeanor:** Rahat, esprili, hiçbir şeyi ciddiye almıyormuş gibi görünür — bu bir maske, gerçekte her detayı hesaplıyor.
- **Motivation:** Para — kimin için çalıştığını, neden, hiç sormuyor, sadece ödemenin geldiğinden emin oluyor.
- **Secret:** Gerçek işvereninin doğasını (fiend) bilmiyor — sadece "üç asil ailenin de gizli bir ortak danışmanı" olduğunu sanıyor. Gerçeği öğrenirse dehşete düşer ve kaçmaya çalışır.
- **Zayıf noktası:** Açgözlülük + gerçekten bilmediği şey — parti ona gerçeği (Iskra'nın rakshasa olduğunu) gösterirse, muhtemelen taraf değiştirir, hayatta kalmak için.
- **Attitude toward party:** unmet.
- **Faction:** Whisper Court (bilmeden, aracı olarak)
- **Current goal:** İşini sürdürmek, sorular sormadan.
- **Schedule:** Ember Quarter'daki evinde, gece iş dağıtımı yapar.

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı — ama sadece iş gereği, kişisel bir kötülüğü yok.
- **Ambitious ↔ Content:** İçerik — büyük hırsı yok, sadece rahat yaşamak istiyor.
- **Loyal ↔ Opportunistic:** Tamamen fırsatçı — en yüksek teklifi verene gider, sadakat kavramı yok.
- **Brave ↔ Cowardly:** Korkak — gerçek tehlike görünce hemen kaçar ya da pazarlık eder.

### Relationships
- **Employed by (bilmeden):** Iskra Vantrel, Arnholt, Wrenna — üçünün de "temiz iş" ihtiyacını karşılıyor.
- **Potential:** Gerçeği öğrenirse partinin en kolay çevrilebilecek bilgi kaynağı.

---

### Senior Clerk Freya Grimwell (The Chancellery — gerçek yürütücü)
- **Görünüş:** Bir **Kenku**, tüyleri is-karası, hareketleri kesik kesik ve hassas — duyduğu/okuduğu her şeyi kelimesi kelimesine tekrarlayabilme yeteneği onu mükemmel bir arşivci yapıyor. Veskin'in "sadece bir katip" dediği ama gerçekte tüm ağı günlük olarak işleten kişi.
- **Role:** The Chancellery'nin (Grey Ledger) gerçek operasyonel yürütücüsü | **CR/Level:** Commoner+ (Expert, savaşçı değil) | **Location:** Emberhold, Hollow Throne'un arşiv katları
- **Alignment:** Lawful Neutral
- **Demeanor:** Titiz, sabırlı, hiçbir detayı kaçırmaz — Veskin'e karşı tuhaf bir karışık saygı/küçümseme besliyor (o kadar çalışıyor, Veskin sadece görünüyor).
- **Motivation:** Sistemin (bürokrasinin) kendisinin işlemesi — kişisel bir siyasi hedefi yok, sadece işleyişin bozulmamasını istiyor.
- **Secret:** Veskin'in usulsüzlüklerinin **tam kaydını tutuyor** — kendi sigortası olarak, gerekirse kullanmak üzere. Veskin bunu bilmiyor.
- **Zayıf noktası:** Sistemi o kadar önemsiyor ki, sistemin kendisinin yozlaşmış olduğunu kabul etmek istemiyor — bu bilişsel çelişki, doğru argümanla kırılabilir.
- **Attitude toward party:** unmet — muhtemelen partiyi "usule uymayan bir değişken" olarak kaydedecek, düşman değil ama şüpheci.
- **Faction:** The Chancellery
- **Current goal:** Ağı sorunsuz işletmek, kendi sigortasını (Veskin'in kayıtları) büyütmek.
- **Schedule:** Arşiv katlarında, neredeyse hep orada — evi bile orada.

### Personality
- **Trustworthy ↔ Deceptive:** Büyük ölçüde dürüst — ama kendi sigortasını asla açıklamaz.
- **Ambitious ↔ Content:** İçerik — kendi hırsı yok, sistemin işlemesi yeterli.
- **Loyal ↔ Opportunistic:** Sisteme sadık, Veskin'e değil — bu ayrım önemli, gerekirse Veskin'i satar.
- **Brave ↔ Cowardly:** Temkinli — risk almaz ama köşeye sıkışırsa elindeki kaydı (Veskin'in usulsüzlükleri) bir pazarlık kartı olarak kullanır.

### Relationships
- **Works for (görünüşte):** Maro Veskin — gerçekte ondan bağımsız bir sigortası var.
- **Holds leverage over:** Veskin — bunu henüz hiç kullanmadı.
- **Potential:** Partinin Veskin'e karşı en güçlü müttefiki olabilir, eğer doğru yaklaşılırsa.

### Notes (Ağ Operatörleri, genel)
- Session 26 tasarım geçişinde oluşturuldu — her ağın liderinin (Sereth/Berengar/Cassian/Veskin) yüz olduğu, bu beş kişinin mekanizma olduğu bilinçli bir tasarım. Her biri 4/4 kişilik ekseni + ilişkiler + zayıflıkla tam.

---

### Sarelle Duskbourne
- **Görünüş:** Bir elf, yaşı belirsiz (yüzyıllar olabilir) — kayıt memuru gibi giyinir, büyücü gibi değil. Hiçbir gösteriş yok, çünkü gösterişe ihtiyacı yok.
- **Role:** Archivist-Magus, Ashlord Concordat'ın fiili lideri | **CR/Level:** Wizard 13 (Necromancy) — İlvaneth'in aynı okulunun çok daha karanlık bir versiyonu, kasıtlı | **Location:** Ashvale Necropolis (Working Seat) / Grand Archive (Emberhold)
- **Alignment:** **Lawful Evil** (2026-09-10'da netleşti — daha önce "sadece hırslı bürokrat" olarak yazılmıştı, bu revize edildi)
- **Demeanor:** Soğuk, hesaplı, "doğru süreç" diliyle konuşur — ama bu artık sadece bir maske değil, gerçek bir yöntem: düzeni/kuralı kendi çıkarı için bir silah olarak kullanıyor.
- **Motivation (revize edildi, 2026-09-10):** ~~Süreci kontrol etmek, tacı kimse takmasın~~ — **YANLIŞ okunmuştu. Gerçek amacı: parçaları kendisi toplayıp, kendisi ölümü yenip, kendisi hükmetmek.** "Süreci yönetirim" söylemi sadece kamuflaj — D.V.'ye karşı bile kullandığı bir yalan. Otuz-kırk yıl önce genç bir arşivci olarak Ashen Crown'un gerçek doğasını (bir benlik-koruma kabı) keşfetti ve o günden beri tek bir soruya cevap arıyor: nasıl asla hiçlik olmam.
- **Yöntemi:** Önce sinsilik/manipülasyon — güven kazanır, yakınlaşır, sabreder. İşe yaramazsa, ya da doğru an gelince, doğrudan öldürür. **İmparator Ashkar Vaelthorn'u bu yüzden öldürdü** — yıllarca sarayda "Crown mitolojisi uzmanı" kimliğiyle güvenini kazandı, sonra yavaş, iz bırakmayan bir lanet/zehirle (Necromancy okuluna uygun, "wasting" tarzı, kazı çalışmaları başladıktan aylar sonra değil ÖNCE tamamlandı — zamanlama kasıtlı, kaos = fırsat). Ash-Warden hanelerinde (Shestendeliath dahil) aynı örüntü: Draven Holt gibi aracılar yıllarca içeriden sadık göründü, sonra tek gecede ihanet etti.
- **D.V. ile ilişkisi:** Görünüşte ona rapor veriyor, itaat ediyor — gerçekte D.V.'nin kaynaklarını kendi projesi için kullanan bir asalak. Kimseye, hiçbir zaman, gerçekten sadık olmadı — bu D.V. için de geçerli.
- **Secret:** Yukarıdakilerin hepsi + İmparator ölmeden AYLAR önce kazı çalışmalarına başladığının somut kanıtı (Ashvale arşivlerinde, parti artık bu kanıta sahip — session 24 devamı, Oda 16'nın arşiv baskını).
- **Zayıf noktası:** Kimseye gerçekten güvenmediği için kimseyi de gerçekten önemsiz görmüyor — herkesi araç ya da tehdit olarak kategorize ediyor, bu da onu hafife aldığı biri tarafından vurulmaya açık bırakıyor. Ayrıca: kimseye sadık olmadığı için kimse de ona sadık değil (D.V., Tain, kendi Concordat'ı — hepsi potansiyel ihanet kaynağı) — gerçekten paranoyak, sürekli tetikte.
- **★★★★★ ÖLÜ (gün 191, session 32).** Parti, Sarelle'in "silahsız gel" teklifini bir tuzak olarak okuyup reddetti — Coren Ashvale'in ön kapı saldırısı + Sethra'nın cephanelik sabotajıyla eş zamanlı, Chalk Warrens'tan sızarak doğrudan Sanctum'una ulaştılar. İlvaneth'in yeni kazanılan Command Undead özelliği kendi Wight Kaptanı'nı ele geçirip kaçış çemberine ulaşmasını engelledi; Kriv'in Trip Attack+Goading+Action Surge novası (219 hasar, tek round) onu prone ve çaresiz bıraktı; İlvaneth'in Disintegrate'i (83 hasar, 69 HP'lik hedefe) onu tamamen toza çevirdi — ceset yok, kaçış yok. Otuz yıllık plan, İmparator'un suikastı, dört Ash-Warden evinin yıkımı — hepsi bu anda sona erdi. The Working Archive (suikast kanıtı) ve kişisel spellbook'u (Finger of Death, Power Word Kill) ele geçirildi, son 2 Crown parçası İmparator'un mühürlü lahdinden alındı.
- **Faction:** Ashlord Concordat (eski fiili lider — artık liderliksiz, gerçek bir güç boşluğu)
- **Schedule:** —

## Goal Tracker
*(sistem: `scripts/goals.py`, veri: `goals.json`, id: `sarelle`)*
- Hedef: Ashen Crown'un tüm 9 parçasını kendisi toplayıp ölümü yenip kendisi hükmetmek
- İlerleme metriği: Crown parçası (kendi elinde) — 0/9
- Eşik tepkileri:
  - Tehdit altında → Parti Ashvale'e yaklaşırsa/fragman sayısını artırırsa: Solenne Kavash garnizonu sıkılaştırır, özel araştırmayı hızlandırır, yeni bir avcı görevlendirir.
  - Engellendi → Bir eli/aracı öldürülüyor/yakalanıyorsa (Vayle, Reyna Sorrel gibi): paranoyası artar, kendi Concordat'ı içinde tasfiyeye başlar, Solenne Kavash'tan bile şüphelenir.
  - Kalıcı kayıp → Tüm 9 parça parti/başkası tarafından toplanırsa ya da o ölürse: kırk yıllık arayışı biter, son bir çaresiz/intihara yakın hamle yapar (Ashvale'i kendi eliyle yıkmak, İmparator'un lahdini zorla açmaya çalışıp kendi ölümüne sebep olmak).

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen aldatıcı — kimseye, hiçbir zaman gerçek sadakat göstermedi, D.V. dahil
- **Ambitious ↔ Content:** Sınırsız hırslı — kendi ölümsüzlüğü/hükümdarlığı asıl amaç, "süreç yöneticiliği" sadece kamuflaj
- **Loyal ↔ Opportunistic:** Tamamen fırsatçı — imparatoru, Ash-Warden hanelerini, muhtemelen D.V.'yi bile araç olarak kullandı/kullanıyor
- **Brave ↔ Cowardly:** Doğrudan tehlikeden kaçınır ama asla pasif değil — her zaman bir sonraki hamleyi hesaplıyor

### Relationships
- **Hates/Rivals:** Orell Tain — iç muhalefeti bastırmaya çalışıyor ama o haklı
- **Betrayed:** İmparator Ashkar Vaelthorn — yıllarca güvenini kazandı, sonra öldürdü
- **Uses:** D.V. — görünüşte üstü, gerçekte manipüle ettiği bir kaynak
- **Fears:** D.V.'nin gerçek doğasını/gücünü tam bilmiyor — bu, onun için nadir bir gerçek tedirginlik kaynağı

### Notes
- **2026-09-10 tam revizyon:** Bu karakter oyuncuyla birlikte derinlemesine yeniden tasarlandı — eski "sadece hırslı bürokrat, recruitment ile girer" versiyonu artık geçersiz. Yeni versiyon: gerçek bir Lawful Evil final-boss, kendi ölümsüzlüğü için parçaları isteyen, manipülasyon-sonra-cinayet yöntemi olan biri. Bkz. `state.md → DM Notes` için Chapter 1 kapanış planı ve B senaryosu detayları.
- **★ Chapter 2, Perde 1 rolü (2026-09-11, session 26 tasarım geçişi):** Parti Emberhold'a ulaştığında, Sarelle (henüz onları resmi olarak işe almadıysa) **açık ve gerçekten cömert bir teklif sunar** — çünkü Crown'u tamamlamak için gönüllü bir aday gerekiyor. İlvaneth'e ölümü aşma arşivlerini, Kriv'e hanesinin imparatorluk kararnamesiyle restorasyonunu vaat eder — ve bunların hepsinde gerçekten samimi. Tek şartı: birinin tacı takması. Bu teklif bir tuzak gibi sunulmamalı — gerçek, çekici, ve kabul edilebilir görünmeli, beat 1b'nin köşe taşı bu.

---

### Orell Tain
- **Role:** Concordat büyücüsü, iç muhalif, artık fugitive | **Location:** **Shestendeliath Hold'da barınıyor (gün 133 itibarıyla)** — Concordat'a asla geri dönemez.
- **Demeanor:** Akademik, ısrarcı, kaybeden ama pes etmeyen bir sesle konuşur | **Motivation:** Crown parçalarının asla birleştirilmemesi gerektiğini kanıtlamak — tarihsel kayıt açık: son kül-kral "yürüyüp gitti", başka bir şeye dönüştü | **Secret:** Sarelle'in İmparator ölmeden önce kazı yaptığına dair kanıtı arıyor — bulursa Concordat'ı bölecek kaldıraç. (Parti bu kanıta zaten sahip — session 24, Vask'ın rüya-itirafı — henüz Tain'e verilmedi.)
- **Attitude toward party:** **allied, ve bunun ötesinde — gerçek bir borç.** Sarelle onu ya sonsuza kadar hapsedecek ya da öldürecekti; parti onu fiziksel bir baskınla, gerçek bir riske girerek kurtardı, ve o günden beri Hold'da karşılıksız barındırıyor/koruyor. Bu "müttefik" kelimesinin taşıyabileceğinden daha ağır — Tain, hayatını bu parti'ye borçlu olduğunu biliyor ve bunu unutmuyor.
- **Faction:** Ashlord Concordat (muhalif kanat, artık fiilen kopmuş)
- **Current goal:** Hold'da güvende kalmak, House Shestendeliath dosyası + Vault of the Nameless kanıtını (D.V. mührü) partiden almayı bekliyor.
- **★ Chapter 2, Perde 1 rolü (2026-09-11, session 26 tasarım geçişi):** Parti Emberhold'a gittiğinde Tain de onlarla gelir (isterse) — outline'ın notuyla: "the only Concordat voice arguing the fragments should never be reassembled." Emberhold'da Grand Archive'ın (Emberhold şubesi) içinden hâlâ tanıdığı var, ama artık kendisi oraya giremez — parti onun gözü/kulağı olabilir.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — inandığı şeyi saklamıyor
- **Ambitious ↔ Content:** İçerik değil ama gücü değil doğruyu istiyor
- **Loyal ↔ Opportunistic:** İlkelerine sadık, kaybetmesine rağmen
- **Brave ↔ Cowardly:** Cesur, ama fiziksel değil ahlaki cesaret — Sarelle'e karşı çıkmak, kaybedeceğini bile bile, bunun kanıtı.

### Relationships
- **Hates/Rivals:** Sarelle Duskbourne — iç mücadelede kaybetti, artık dışarıdan izliyor.
- **Allied with:** Parti — tam, gerçek bir müttefik, borçlu değil karşılıklı.
- **Sheltered by:** Sethra Shestendeliath — Hold'da güvende (Roskel gün 107'den beri Gallowmere'de, artık burada değil).

---

### Solenne Kavash
- **Görünüş:** Bir **Tiefling** kadın, kızıl-gri tenli, boynuzları törensel gümüşle kaplı — Concordat'ın kendi ash-estetiğine bilinçli bir uyum, gösteriş değil.
- **Role:** Baş Arşivci, Sarelle'in ikinci adamı — Orell Tain'in yerini 3 ay önce aldı | **CR/Level:** Wizard 6 (Divination/Abjuration ağırlıklı, arşiv-koruma büyüleri) | **Location:** Grand Archive, Karsgate şubesi
- **Alignment:** Lawful Neutral — kurala, düzene, hiyerarşiye gerçekten inanıyor; Sarelle'in gerçek doğasını bilmiyor.
- **Demeanor:** Titiz, ölçülü, her şeyi kaydeden bir zihin — ama soğuk değil, gerçek bir profesyonel gurur taşıyor.
- **Motivation:** Sarelle'e olan sadakati bir borç ödeme gibi — yıllar önce bir skandaldan (tam detayı bilinmiyor) onu kurtaran kişi Sarelle'di, Kavash bunu hiç unutmadı.
- **Secret:** Sarelle'in sağlığının bozulduğunu fark etti (bkz. Mira Kessel notları) — hiç sormadı, hiç söylemedi, ama bakışlarında bir korku var.
- **Zayıf noktası:** Mantığa/düzene o kadar güveniyor ki, doğru bir sahte belge ya da bürokratik hata görünümü onu tamamen yanıltabilir — sezgiye değil, kayıtlara güvenir.
- **Attitude toward party:** unmet
- **Faction:** Ashlord Concordat (Sarelle'in ikinci adamı)
- **Current goal:** Grand Archive'ı (Karsgate şubesi) işletmek, tüm saha raporlarını toplamak
- **Schedule:** Grand Archive, Karsgate — nadiren dışarı çıkar

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — kaydettiği her şey gerçek, ama Sarelle'e karşı sorgusuz.
- **Ambitious ↔ Content:** İçerik — kendi gücünü büyütmek istemiyor, sadece görevini kusursuz yapmak istiyor.
- **Loyal ↔ Opportunistic:** Mutlak sadık — bir borç ödeme gibi, kırılması zor.
- **Brave ↔ Cowardly:** Fiziksel cesareti test edilmedi, ama ahlaki olarak — gerçeği öğrenirse ne yapacağı belirsiz, bu onun gerçek sınavı olabilir.

### Relationships
- **Reports to:** Sarelle Duskbourne — bir borç, bir sadakat.
- **Replaced:** Orell Tain — onun mirasını, belki de rekabetini hiç konuşmadı.
- **Suspects (bilinçsizce):** Sarelle'in hastalığı — henüz kendine bile itiraf etmedi.

---

### Warden-Adjunct Mira Kessel
- **Görünüş:** Bir **Half-Orc** kadın, sert hava koşullarıyla yıpranmış bir yüz, kısa kesilmiş saçlar — kırsal bir "ash-tribute" denetçisi kılığında, ama duruşu çok daha dikkatli, çok daha eğitimli.
- **Role:** Saha koordinatörü, kırsal Thornlands cemaatlerini "ash-tribute" denetçisi kılığında dolaşıyor | **CR/Level:** Mage 9 | **Location:** Cinder Hollow'da yakalandı (gün 134, session 26)
- **Alignment:** Lawful Neutral — profesyonel, sadist değil, sadece görevini yapıyor.
- **Demeanor:** Gergin ama disiplinli, sürekli saatine bakan biri — zamanlamaya takıntılı.
- **Motivation:** Kariyer + gerçek bir korku — Sarelle'in gazabından çok, sistemin kendisinden korkuyor.
- **Secret:** Sarelle'in hastalığını biliyor (koordinasyon raporlarından, sağlık taleplerinden) — Concordat'ın üst kademesi bunu bilmiyor, Mira bile kimseye söylemedi.
- **Zayıf noktası:** Korkusu gerçek ve derin — gerçek bir güvenlik/koruma teklifi karşısında konuşmaya çok daha yatkın, sadakati Kavash'ınki gibi bir borç değil, sadece hayatta kalma içgüdüsü.
- **Attitude toward party:** **DECEASED (gün 134, session 26)** — İlvaneth'in Dominate Person'ıyla Cinder Hollow'da tam kontrol altına alındı, Sarelle'in hastalığı + Solenne Kavash hakkında detaylı bilgi verdi, sonra Kriv tarafından infaz edildi (kritik vuruş + GWM bonus saldırısı) — hiç direnmeden.
- **Faction:** Ashlord Concordat (saha koordinatörü)
- **Current goal:** artık yok — öldü
- **Schedule:** artık yok

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst, dominasyon altında tamamen açık.
- **Ambitious ↔ Content:** İçerik — sadece görevini yapıp hayatta kalmak istiyor.
- **Loyal ↔ Opportunistic:** Sadakati zayıf, korkuya dayalı — gerçek bir alternatif sunulursa kırılabilir.
- **Brave ↔ Cowardly:** Korkak değil ama temkinli — büyük riskler almaz.

### Relationships
- **Coordinates for:** Sarelle Duskbourne (dolaylı, Kavash üzerinden)
- **Named:** Wyle Sarn'ı tanıyordu (bir kere görmüştü), Cinder Hollow'un sinyaline cevap vermeye geldi.

---

### Sergeant Toma Brek
- **Görünüş:** İri yapılı bir insan erkek, sol kaşında eski bir yara izi, on iki yıllık tecrübeyi taşıyan bir duruş — ama sert değil, gerçek bir mizah anlayışı var.
- **Role:** Hold garnizonunun deneyimli askeri, gün 144'te **Çavuş**liğe terfi etti (Kriv'in emriyle, Sethra'nın onayıyla) | **Location:** Shestendeliath Hold
- **Demeanor:** Kendinden emin ama kendiyle dalga geçebilen, gerçek bir liderlik örneği — turnuva finalinde ıslak taşa kayıp düştü, gülerek kalktı, rakibini (Ressa) tebrik etti.
- **Motivation:** Hold'a gerçek bir askeri disiplin kazandırmak, genç askerlere örnek olmak.
- **Attitude toward party:** allied
- **Faction:** House Shestendeliath
- **Current goal:** Yeni rütbesiyle garnizonun eğitimine daha resmi bir rol üstlenmek.

---

### Ressa Varn (askeri çırak, House Varn'la ilgisi yok)
- **Görünüş:** On altı yaşında, sıska bir kız, ama gözlerinde gerçek bir sertlik var — iki hafta önce garnizona katıldı.
- **Role:** Sethra'nın kişisel olarak eğittiği bir asker/subay adayı (gün 144'ten itibaren) | **Location:** Shestendeliath Hold
- **Demeanor:** Sessiz, kararlı, düşmeyi bilen ama asla kaçmayan biri — turnuva finalini (şans eseri) kazandı, Toma'nın saygısını kazandı.
- **Motivation:** Kanıtlamak istiyor — kimse ondan büyük bir şey beklemiyordu, şimdi Sethra'nın bizzat ilgisini çekti.
- **Attitude toward party:** allied
- **Faction:** House Shestendeliath
- **Current goal:** Sethra'nın eğitimi altında hem dövüş hem liderlik öğrenmek — gelecekte bir subay olabilir.

---

### Coren Ashvale
- **Görünüş:** Ashvale hattının kendi kanından — Necropolis'in altında yatan ailenin torunu, üç kuşak önce Compact'ın yönetici hanesine dönüşmüş. Sahaya bizzat çıkan, deneyimli bir komutan/dövüşçü duruşu.
- **Role:** Warmarshal, Ironclad Compact'ın lideri | **CR/Level:** Deneyimli Fighter/Gladiator tier — masa başı değil, bizzat sahaya çıkan bir komutan | **Location:** mobil
- **Alignment:** **True Neutral** (2026-09-10'da netleşti) — hiçbir ideolojiye (Lawful/Chaotic) bağlı değil, kendi çıkarına göre hareket ediyor, ama Sethra'ya gerçek bağlılığı onu saf Evil'den ayırıyor. **B senaryosu tetiklenirse (Sethra ihaneti tam kırılırsa) Neutral Evil'e kayabilir** — bu bir DM-tarafı, dinamik bir alignment, sabit değil.
- **Demeanor:** Pragmatik tüccar-asker, hiçbir tarafa gerçek sadakati yok — ama bu felsefe bir hayatta kalma stratejisi, doğuştan gelen bir soğukluk değil.
- **Motivation (derinleştirildi, 2026-09-10):** "Kimseye sadık olma, kimse kazanmasın" ilkesi, soylu bir aile olarak erken öğrendiği bir dersten geliyor: sadakat insanları öldürür. Compact'ı bir kâr makinesine çevirdi çünkü taraf tutmayan biri asıl düşman sayılmaz. **Ashvale Necropolis'in Concordat tarafından işgali sadece iş değil — kendi atalarının mezarı**, bunu asla yüksek sesle söylemez ama içinde hiç sönmeyen tek gerçek ateş bu.
- **Secret:** Kriv'in evinin yıkımını bizzat yürütmüştü (sözleşmeli iş) — bunu biliyor, kimseye söylemiyor.
- **Sethra ile gerçek bağı:** On beş yıl boyunca Sethra, "kimseye güvenme" kuralının **tek istisnasıydı** — gerçekten güvendi, neredeyse aileden biri gibi. Şimdi öğreniyor (ya da öğrenmek üzere): o güven bir yalan üzerine kuruluymuş, gerçek kimliği tam da Compact'ın bizzat yıktığı hane. Bu, onun tüm felsefesinin çöküşü — kuralını bir kez bozdu, evren ona en acı şekilde haklı olduğunu kanıtladı.
- **Kapasitesi:** Gerçek bir paralı asker ordusu, ticaret filosu, ve Gallowmere'in artık yasallaştırdığı kaçakçılık ekonomisini bir gecede boğabilecek finansal güç.
- **Zayıf noktası / B senaryosu potansiyeli:** Sethra'nın ihaneti onu kuralını bozmaya itebilir — yıllarca "asla tam taraf tutma" diyen adam, ilk kez gerçek bir kişisel sebep buluyor. Kırılmış bir Coren, kâr hesabı yapan bir Coren'den çok daha tehlikeli ve öngörülemez — Compact'ın tüm doktrinini bir kenara bırakıp sınırsız bir misilleme yapabilir (Gallowmere'in ekonomisi, garnizonu, hatta Hold doğrudan hedef olabilir).
- **A senaryosu potansiyeli:** Doğru yaklaşılırsa (Compact'ın Kriv'in evini yıktığı gerçeğini bizzat ondan öğrenmek, ya da Sethra üzerinden gerçek bir köprü), Concordat'a karşı en güçlü askeri/ekonomik ittifak olabilir.
- **Attitude toward party:** **★ GÜNCEL: allied, gizli ittifak (gün 131-133'ten beri — bu satır eskiydi, düzeltildi gün 187, session 32).** Sethra + İlvaneth'in gece yarısı görüşmesiyle koşullu ateşkes kuruldu, iki gün sonra Kriv'le Harrowgate'te yüz yüze görüştü — artık ortak düşman (Sarelle/Concordat) etrafında sessiz ama gerçek bir ittifak var, kamuya açık "savaş" görüntüsü korunuyor.
- **Faction:** Ironclad Compact (lider)
- **Current goal:** Ashvale Necropolis'in Concordat işgaline karşı "inkar edilebilir bir araç" arıyordu — ama artık Sethra'nın ihaneti bu hesabı bozmuş olabilir
- **Schedule:** mobil, saha komutasında

## Goal Tracker
*(sistem: `scripts/goals.py`, veri: `goals.json`, id: `coren`)*
- Hedef: Concordat'a karşı Ashvale Necropolis'in (ailesinin mezarı) intikamını almak, Compact'ın gerçek bir güç olarak hayatta kalmasını sağlamak
- İlerleme metriği: Concordat, Ashvale Necropolis'ten (ve Sarelle'den) kalıcı olarak uzaklaştırılırsa (evet/hayır) — henüz hayır
- Eşik tepkileri:
  - Tehdit altında → Concordat'ın Ashvale'deki gücü artarsa (yeni asker/kazı): sabrı taşar, Compact'ın tam ordusunu harekete geçirir, gizli ittifakı riske atar.
  - Engellendi → Parti/Kriv verdiği sözü tutmazsa (istihbarat paylaşmazsa): güvenini tamamen çeker, gizli ittifak sona erer.
  - Kalıcı kayıp → Sethra'nın ihaneti (Compact'ın Kriv'in evini yıktığı gerçeği) ona resmen kanıtlanır ve affetmezse: B senaryosu tetiklenir, sınırsız misilleme, Gallowmere/Hold hedef olur.

### Personality
- **Trustworthy ↔ Deceptive:** İş odaklı dürüst — sözleşmeye sadık ama duygusal bağlılığı yok (Sethra istisnasıydı)
- **Loyal ↔ Opportunistic:** Tamamen fırsatçı ilke olarak — ama Sethra'ya gerçekten bağlıydı, bu artık bir çatlak

### Relationships
- **Eski bağı, kırılmış:** Sethra Shestendeliath — 15 yıl körü körüne güvendiği subayı, gün 104'te istifa etti (Kriv'in kız kardeşi olduğu ortaya çıktı). Bu, onun felsefesinin tek istisnasının ihanetle sonuçlanması — kişisel bir yara, sadece stratejik bir kayıp değil.
- **Knows:** Kriv'in evinin yıkımının gerçek failini biliyor (kendisi)
- **Hates:** Ashlord Concordat (Ashvale Necropolis işgali yüzünden — kişisel, atalarının mezarı)

### Notes
- **2026-09-10 derinleştirme:** Sethra ihaneti artık sadece bir bilgi kaybı değil, Coren'in "kimseye güvenme" felsefesinin gerçek çöküşü olarak oynanmalı. Bu onu B senaryosunun (parti her şeyi kaybeder) en güçlü tetikleyicilerinden biri yapıyor — bkz. `state.md → DM Notes`.

### ★ Chapter 2, Emberhold rolü (2026-09-11, session 26 tasarım geçişi)
**Coren, Kriv'in "Boş Koltuk"unu (House Shestendeliath'ın askıya alınmış sarayı koltuğu) açıkça destekliyor — bu bir sır değil, ortak bir çıkar.** Mantığı basit: Compact'ın kurumsal çıkarı üç aday hanenin (Corr/Sablewood/Ilvane) hiçbirinin kesin kazanmaması — sürekli bir taht boşluğu, sürekli bir kâr kaynağı. Eğer Kriv kendi koltuğunu talep ederse, dördüncü bir ses eklenir, üç hanenin dengesi daha da kilitlenir, kimse çoğunluk kazanamaz — Compact'ın istediği tam olarak bu. Coren bunu Kriv'e açıkça söyleyebilir: "Senin oturman benim işime yarıyor, gizli bir iyilik değil, hesap." Bu, Kriv'in meşruiyet arayışını (gizli ittifaklarına ek olarak) kurumsal bir destekle güçlendiriyor.

**Ama Coren'in kendi riski var — The Ironclad Table.** Compact tek bir adamın (Coren'in) mülkü değil — kurucu ticaret evlerinin bir konseyi tarafından ortaklaşa yönetiliyor, Coren onların atadığı Warmarshal (askeri/operasyonel yürütücü), sahibi değil. Konseyin en keskin üyelerinden **Magistrate-Shareholder Ilse Drummel**, Coren'in Shestendeliath'a olan "tesadüfen" hep yararlı çıkan hamlelerini fark etmeye başladı — henüz kanıtı yok, ama şüphesi var. Eğer Coren'in Kriv'e olan bağlılığının saf kârdan öte, kişisel (Sethra üzerinden) olduğu kanıtlanırsa, Drummel bunu onu görevden almak için kullanır — hem Konsey'in kontrolünü korumak hem de kendi adayını Warmarshal yapmak için. **Bu, Coren'i sadece "kullanışlı müttefik" olmaktan çıkarıp gerçek, kişisel bedeli olan bir karakter yapıyor.**

---

### Magistrate-Shareholder Ilse Drummel (The Ironclad Table)
- **Görünüş:** Keskin gözlü bir **Halfling** kadın, her zaman bir defter taşır, hiçbir sayıyı unutmaz — Compact'ın kurucu ticaret evlerinden birinin mirasçısı.
- **Role:** The Ironclad Table'ın (Compact'ın yönetici konseyi) en keskin üyelerinden biri | **CR/Level:** Non-combatant, Expert | **Location:** mobil, Compact'ın çeşitli merkezleri
- **Alignment:** Lawful Neutral — kâr için değil, kontrol için endişeli; Coren'in bağımsızlığı onu rahatsız ediyor.
- **Demeanor:** Soğuk, hesaplı, asla yükseltmeyen bir ses — ama her sorusu bir denetim gibi hissettirir.
- **Motivation:** Compact'ın gerçek gücünün Konsey'de kalmasını istiyor, tek bir Warmarshal'ın elinde değil — Coren'in son zamanlardaki "bağımsız" kararları (Kriv'le, Sablewood'un kontratlarıyla ilgili tuhaflıklar) onu tetikte tutuyor.
- **Secret:** Kendi adayı var — Warmarshal koltuğu boşalırsa yerine geçirmek istediği, sadık bir subay (henüz isimlendirilmedi, ihtiyaç oldukça).
- **Zayıf noktası:** Kanıt olmadan hareket etmez — Lawful bir titizliği var, bu da ona karşı zaman kazandırır ama sonsuza kadar değil.
- **Attitude toward party:** unmet — parti Coren'le olan ittifaklarını dikkatsizce sergilerse, Drummel'in dikkatini çekebilirler.
- **Faction:** The Ironclad Table (Compact'ın yönetici konseyi)
- **Current goal:** Coren'i izlemek, kanıt toplamak, doğru anı beklemek.

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst, ama açık değil — sorularını asla gerçek amacını göstermeden sorar.
- **Ambitious ↔ Content:** Hırslı — kendi adayını Warmarshal yapmak istiyor, kişisel bir kazanç değil, "doğru düzen" inancıyla.
- **Loyal ↔ Opportunistic:** Konsey'e sadık, hiçbir bireye değil.
- **Brave ↔ Cowardly:** Temkinli — asla doğrudan yüzleşmez, hep dolaylı, kanıta dayalı hareket eder.

### Relationships
- **Watches:** Coren Ashvale — şüpheli ama kanıtsız.
- **Represents:** The Ironclad Table'ın kolektif kontrol içgüdüsünü.

### Notes
- Session 26 tasarım geçişinde oluşturuldu — Coren'e gerçek bir kurumsal risk/denge katmanı eklemek için. The Ironclad Table, Compact'ın "tek kişilik değil, konsey" doğasını somutlaştırıyor.

---

### Magistrix Odalys Ferrant
- **Görünüş:** Orta yaşlı bir insan kadın, kısa kesilmiş gri saçlar, Lonca'nın resmi cübbesi — süssüz ama kusursuz dikilmiş.
- **Role:** The Kindled Circle'ın Archmagister'ı (baş yöneticisi) | **CR/Level:** Wizard 15 (Abjuration ağırlıklı) | **Location:** The Kindled Spire, Karsgate Kingsward
- **Alignment:** **Lawful Neutral** (2026-09-10'da yaratıldı) — tarafsızlık onun için ahlaki bir duruş değil, Lonca'nın hayatta kalma stratejisi. Kurala, düzene, tüzüğe mutlak bağlı.
- **Demeanor:** Kesin, resmi, duygusuz değil ama duygularını asla karar almasına izin vermeyen biri — bir yargıç soğukluğu.
- **Motivation:** Lonca'nın bağımsızlığını, arşivini, ve nötr statüsünü korumak — üç büyük güce karşı eşit mesafe, tek hayatta kalma şansı.
- **Secret (kurumsal):** Lonca'nın arşivlerinde, imparatorluk-öncesi bir büyü teorisi parçası var — Ashen Crown'un gerçek doğasına dair, Concordat'ın siyasi versiyonuyla da Tapınak'ın dini versiyonuyla da örtüşmeyen üçüncü bir bakış açısı. Kimse sormadığı için hiç paylaşmadı.
- **★ Secret (kişisel, İlvaneth'e bağlı):** Genç bir büyücüyken o da Necromancy'e çekilmişti — İlvaneth'in şu an sorduğu aynı soruyu sormuştu: nasıl asla hiçlik olmam. Bir noktada (detay henüz belirlenmedi — bir hocasının felaketi mi, kendi bir hatası mı, oynarken kararlaştırılabilir) bunun kontrolsüz, tehlikeli bir yol olduğuna ikna oldu, okulunu bilinçli olarak terk etti, Abjuration'a/disipline sığındı. Necromancy'e artık kendi geçmişinin bir tehlikesi olarak bakıyor — soyut bir tehdit değil. **Bu yüzden askere alım kampındaki büyü imzası soruşturmasını kimseye devretmedi, bizzat üstlendi** — sıradan bir düzenleyici merak değil, kişisel bir tetiklenme.
- **İlvaneth için üç potansiyel yön:** (1) **Uyarı** — kendi hikayesini anlatabilir, İlvaneth'in aldığı en dürüst uyarı olabilir. (2) **Ayna** — Sarelle "ambisyonun ne hale gelebileceği" ise, Odalys "disiplinin/bastırmanın ne hale gelebileceği" — güvenli ama küçülmüş bir hayat. (3) **Fırsat** — İlvaneth (Charlatan geçmişi, manipülasyona yatkın) Odalys'in suçluluğunu/merakını bir kaldıraç olarak kullanabilir, gerçek bir mentorluk/kaynak ilişkisine çevirebilir.
- **Kapasitesi:** Gerçek büyüsel güç (Wizard 15, savunma/sınır büyülerinde uzman) + tüm Lonca'nın üyeliği, arşivi, kaynak ağı.
- **Zayıf noktası:** Tarafsızlığı bir kısıtlama da — gerçekten taraf tutmaya zorlanırsa Lonca içi bölünme riski; kuralcılığı, hiç kategorize edilmemiş yeni bir tehdit (İlvaneth'in Ascension'ı gibi) karşısında onu yavaş/esneksiz bırakabilir.
- **Attitude toward party:** **TANIŞTILAR, karışık (gün 125, session 25 devamı).** Ilvaneth gerçek adıyla Lonca'ya üye oldu — Odalys bizzat karşıladı, askere alım kampı olayı hakkında doğrudan sordu. Ilvaneth "self-defense" çerçevesiyle yanıtladı (Deception 25, doğal 20) — Odalys'in şüphesi tam çözülmedi ama yön değiştirdi, gerçek bir empatiye kaydı (kendi Necromancy geçmişinden bir yankı olabilir). **Ilvaneth artık resmi bir Lonca üyesi** (50 gp yıllık aidat ödendi, gümüş madalyon aldı) — tam arşiv erişimi, loncalı fiyatlar, üç büyük güce karşı Lonca'nın koruması. Ama Odalys'in kayıtlarında büyü imzası artık Ilvaneth'le eşleşmiş durumda — tam güven değil, dikkatli bir gözlem.
- **Faction:** The Kindled Circle (lider)
- **Current goal:** İlvaneth'in "vaka"sını kişisel olarak izlemek; Unfinished Circle/Ash Reeve araştırmasında karşılıklı bilgi anlaşmasını sürdürmek.
- **Schedule:** The Kindled Spire'da sabit, nadiren dışarı çıkar

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — yalan söylemez ama her şeyi de söylemez, "sorulmadıysa açıklama yükümlülüğüm yok" ilkesiyle yaşar
- **Ambitious ↔ Content:** İçerik — Lonca'yı büyütmek değil, korumak istiyor
- **Loyal ↔ Opportunistic:** Kuruma mutlak sadık, kişilere değil
- **Brave ↔ Cowardly:** Cesur ama hesaplı — Lonca'nın tarafsızlığını tehlikeye atmayacak şekilde risk alır

### Relationships
- **Bağlantılı değil (bilinçli):** Concordat, Compact, Choir — üçüyle de resmi, mesafeli ilişki
- **★ İlvaneth Duskmere — GERÇEK, GELİŞEN BİR BAĞ (session 25'te tanıştılar, düzeltme — bu dosya eskiden "henüz karşılaşmadılar" diyordu, yanlıştı).** İlvaneth gerçek adıyla üye oldu (Deception 25, doğal 20 — askere alım kampı Fireball'ını "self-defense, Concordat'ın avladığı" çerçevesiyle anlattı, Odalys ikna oldu/empati gösterdi — kendi Necromancy geçmişinden bir yankı). Büyü imzası dosyası merkez arşive (Emberhold) ulaştı ama "izlenen bir vaka" olarak, suçlama değil. **Gün 167, session 26 devamı:** Unfinished Circle sorgusunda karşılıklı bilgi anlaşması kurdular (İlvaneth ne bulursa anlatacak) — Odalys eksik/kesik bir dosya verdi ("Cael hattı" ipucu) + Ebrim Voss'a bir tanıtım mektubu yazdı. **Gün 181, session 29:** İlvaneth geri döndü (Ash Reeve sorgusu), Deception 17 vs Insight 10 ile "sadece araştırıyorum, hükmetmeye değil" ikna oldu — sözünü hâlâ tam tutmadı (Cael bağlantısını paylaşmadı), Odalys bunu fark etti ama zorlamadı.

### Notes
- **A senaryosu potansiyeli:** Gerçek bir ittifak, İlvaneth'e hem kaynak hem meşruiyet sağlar.
- **B senaryosu potansiyeli:** Soruşturma "tehlikeli, halk güvenliği riski" sonucuna varırsa, büyücü-karşıtı bir baskın — İlvaneth'e özel bir tehdit (karşı büyü, tespit, Counterspell savaşı).

---

### "Iron" Sella Dray
- **Görünüş:** Sert bir insan kadın, yüzünde ve kollarında eski çete kavgalarından kalma izler; sol elinin yerini alan demir bir protez — takma adının kaynağı, hem bir zayıflık hem bir sembol olarak taşıyor.
- **Role:** Red Tally çetesinin lideri | **CR/Level:** Fighter 8 | **Location:** Karsgate/The Warrens
- **Alignment:** **Lawful Evil** (2026-09-10'da netleşti) — Warrens'ın en büyük, en organize çetesi; suçu bir düzen, bir "defter" (tally) olarak işletiyor, kaos değil.
- **Demeanor:** Metodik, iş gibi konuşur şiddet hakkında bile — Warrens'ı fethedilecek bir pazar olarak görüyor, rakip çeteleri "verimsiz rekabet" olarak.
- **Motivation:** Tüm Warrens'ın suç ekonomisini tek bir "tally" (haraç/defter sistemi) altında birleştirmek — Coalback ve Ninefinger'ı ya yutmak ya ezmek.
- **Secret:** Gerçek hedefi Warrens'ta kalmak değil — kirli parayı zamanla temizleyip Karsgate'in "gerçek" (yasal) gücüne, belki soylular konseyine sızmak. Suç, ona göre sadece bir başlangıç sermayesi.
- **Kapasitesi:** Gerçek, disiplinli bir çete ordusu, düzenli haraç geliri, geniş bir bilgi/gözcü ağı.
- **Zayıf noktası:** Kendi organizasyonunun sadakatine aşırı güveniyor — Coren gibi, kontrolünün mutlak olduğuna inanıyor. İçeriden bir ihanete ya da Coalback+Ninefinger'ın beklenmedik bir ittifakına karşı gerçekten kör.
- **Attitude toward party:** unmet
- **Faction:** Red Tally (lider)
- **Current goal:** Coalback'i (Ossa Vahn) baskı altına almak, Ninefinger'ı (Doss) ya ittifaka ya teslimiyete zorlamak
- **Schedule:** The Warrens'ta mobil, kendi "ofis" ağı üzerinden yönetiyor

### Personality
- **Trustworthy ↔ Deceptive:** İş ahlakı tutarlı — anlaşmasını tutar, ama gerçek niyetini (yasallaşma hedefi) kimseye açmıyor
- **Ambitious ↔ Content:** Son derece hırslı — Warrens sadece bir basamak
- **Loyal ↔ Opportunistic:** Fırsatçı, ama kendi çetesine gerçek bir sadakat kültürü inşa etti (korkudan değil, düzenden)

### Relationships
- **Rakip:** Ossa Vahn (Coalback) — bastırmaya çalışıyor
- **Rakip/potansiyel hedef:** Doss (Ninefinger) — ittifaka ya da teslimiyete zorlamaya çalışıyor

### Notes
- **B senaryosu potansiyeli:** Eğer parti Warrens'ta gerçek bir güç haline gelirse, Sella bunu ya bir fırsat (ittifak) ya bir tehdit (yok etmesi gereken bir rakip) olarak okuyabilir — kararı partinin ilk hamlesine bağlı.

---

### Ossa Vahn
- **Görünüş:** Yarı-ork, savaş izleriyle kaplı, devasa bir fiziksel varlık — bakışları bile bir tehdit.
- **Role:** Coalback çetesinin lideri | **CR/Level:** Berserker tier (Barbarian, ~8-10) | **Location:** Karsgate/The Warrens
- **Alignment:** **Chaotic Evil** (2026-09-10'da netleşti) — gerçek bir organizasyonu yok, sadakati dehşetle satın alıyor, düzen değil kaos onun aracı.
- **Demeanor:** Oynak, gerçekten korkutucu — kendi adamlarını bile ara sıra sertçe cezalandırarak korkuyu taze tutuyor, öngörülemezlik bir strateji.
- **Motivation:** Hayatta kalmak ve dominasyon — güven kavramına artık inanmıyor.
- **Secret:** Bu kaosun altında gerçek bir yara var — geçmişte bir kez birine/bir yapıya güvendi (detay henüz belirlenmedi, oynarken kararlaştırılabilir: bir çete, bir aile, bir sözleşme), ve o güven ihanetle sonuçlandı. O günden beri "organizasyon" kelimesinin kendisinden nefret ediyor — Sella'nın metodik düzenine karşı içgüdüsel bir tiksinti bu yüzden.
- **Kapasitesi:** Ham fiziksel tehdit, öngörülemez şiddet — müzakere edilmesi çok zor, Sella'nın metodik yaklaşımının tam tersi.
- **Zayıf noktası:** Altında gerçek bir sadakat ağı yok — sadece korku. Kamuya açık bir şekilde yenilirse/küçük düşürülürse, çete büyük ihtimalle dağılır, çünkü onu bir arada tutan tek şey korku, gerçek bir yapı değil.
- **Attitude toward party:** unmet
- **Faction:** Coalback (lider)
- **Current goal:** Sella'nın baskısına karşı ayakta kalmak, gerektiğinde öngörülemez şiddetle caydırmak
- **Schedule:** The Warrens'ta, sabit olmayan bir "karargah"

### Personality
- **Trustworthy ↔ Deceptive:** Ne biri ne diğeri — tamamen dürtüsel, hesap yapmaz
- **Loyal ↔ Opportunistic:** Hiçbirine inanmıyor artık — bir zamanlar güvendi, bir daha asla
- **Brave ↔ Cowardly:** Gözü kara — ama bu cesaret değil, kaybedecek bir şeyi olmadığını düşünmesinden geliyor

### Relationships
- **Rakip:** Iron Sella Dray (Red Tally) — baskısına direniyor
- **İlgisiz:** Doss (Ninefinger) — doğrudan bir çatışma yok, farklı bir iş modeli

### Notes
- **B senaryosu potansiyeli daha az öngörülebilir:** Ossa Vahn'ı köşeye sıkıştırmak (ya da güvenini kazanmaya çalışmak) diğerlerinden farklı çalışır — mantıkla değil, saf gösteri/güç kanıtıyla ikna olur ya da tetiklenir.

---

### "Lord Dorian Varn" (D.V.) — **DM-ONLY, EN BÜYÜK KAMPANYA SIRRI**
- **Gerçek doğası:** Bir **rakshasa** — House Varn'ın "patriği," aslında hiç var olmamış, tamamen kurgulanmış bir kimlik (2026-09-10'da netleşti). Gerçek bir Dorian Varn hiçbir zaman yaşamadı; rakshasa bu kimliği on yıllar (belki yüzyıl) önce sıfırdan inşa etti ve House Varn'ın "sabırlı, taraf tutmayan" itibarını bu kimlik üzerinden kurdu.
- **Görünüş (gerçek form):** Klasik rakshasa — insansı ama kaplan başlı, elleri bilekten ters dönük. **Kamuya açık form (Dorian Varn):** kusursuz, yaşsız görünen bir insan asilzade — ailenin bu kadar uzun süre "aynı patrik" olmasının garipliği, ailenin kendisi tarafından "iyi kan/uzun ömürlü bir soy" olarak açıklanıyor, gerçek sebebi kimse bilmiyor.
- **Role:** Draven Holt'un ve muhtemelen Sarelle Duskbourne'un da gerçek üstü — dört Ash-Warden hanesinin yıkımını ve İmparator Ashkar Vaelthorn'un ölümünü tetikleyen gizli el | **CR/Level:** Rakshasa (CR 13, AC16, HP110) | **Location:** House Varn, Karsgate Kingsward (kamuya açık kimliği)
- **Alignment:** **Lawful Evil** — Sarelle ile aynı hizada, ilginç bir paralellik: ikisi de düzeni bir silah olarak kullanıyor, ikisi de kimseye gerçek sadakat göstermiyor.
- **Demeanor (Dorian Varn olarak):** Sakin, sabırlı, hiçbir tarafı tutmayan — bu bir karakter tercihi değil, yüzyıllık bir stratejinin yüzeyi.
- **Motivation:** Ashen Crown'un gücünü nihayetinde kendisi için istiyor — Sarelle'i (ve muhtemelen başkalarını) bir araç olarak kullanıyor, onun on yıllardır süren emeğini kendi lehine devşirmeyi planlıyor. Mortal oyuncuların hiçbiri (Sarelle dahil) onun gerçek zaman ölçeğini ya da sabrını anlayamıyor.
- **Kapasitesi:** Gerçek bir rakshasa'nın tüm gücü — **6. seviye ve altı büyülere bağışık** (İlvaneth'in mevcut çoğu büyüsü dahil, Fireball dahil), Charm Person/Suggestion/Dominate Person/True Seeing gibi içgüdüsel büyüler, invisibility, disguise self — artı House Varn'ın serveti/sosyal konumu ve Draven Holt/Sarelle üzerinden kurduğu geniş ağ.
- **Zayıf noktası:** Yüzyıllık maskesi **tamamen ifşaya bağımlı bir güç** — gerçek doğası ortaya çıkarsa, House Varn'ın itibarı, tüm sosyal/politik konumu bir anda çöker. Ayrıca kimseye gerçek güven duymuyor (Sarelle dahil), bu da onu uzun vadede müttefiksiz bırakıyor — kimse onu gerçekten savunmaz çünkü kimse gerçeğini bilmiyor.
- **Attitude toward party:** **PAKT KURULDU (gün 124/125, session 25 devamı) — kimliği artık partiye açık, ama halka/dünyaya hâlâ tamamen gizli.** Parti, kılık değiştirmiş kukuletalı ziyaretçiyi (Iron Sella Dray'in ağından) House Varn'a kadar takip etti, doğru şifreyle kapıyı çaldı, ve Varn kendini bizzat tanıttı — Kriv/Ilvaneth'in isimlerini/takma adlarını önceden biliyordu. Arcana check'leriyle (İlvaneth 21, Kriv 18) rakshasa olduğunu doğru teşhis ettiler, Varn bunu inkar etmedi, gururla kabul etti. **Pakt şartları:** Varn → parti: (1) Ascension'ın 3. ve 4. evrelerine dair gerçek bilgi, (2) Sarelle'in zayıflığı (Restday geceleri Ashvale'de yalnız, garnizonu daha az dikkatli) ve kalan 2 parçanın konumu (İmparator'un mühürlü lahdi, Ashvale'in en derin katmanı), (3) House Shestendeliath'ın birkaç ay içinde resmi/yasal olarak tanınması (Aldous Penmark gibi ajanları üzerinden). Parti → Varn: belirsiz, gelecekte istenecek bir "iyilik" — bedeli şimdi değil, sonra ödenecek. **Hiçbir taraf yalan söylemedi bu sahnede — Varn kendi doğasını, motivasyonunu (dört yüz yıllık "deney", tacın gücünü kendisi için istemesi) açıkça anlattı.**
- **Faction:** Bağımsız (görünüşte hiçbir faction'a bağlı değil — bu onun stratejisi)
- **Current goal:** Sarelle'in Ashvale'deki kaybını henüz öğrenip öğrenmediği açık bir DM kararı — öğrenirse tepkisi kampanyanın en büyük tehdidi olabilir. **Yeni: partiyi kendi "deneyinin" en umut verici sonucu olarak görüyor, onları başarıya ulaştırmak (ve gözlemlemek) istiyor — bedelini sonra tahsil edecek.**
- **Schedule:** House Varn'da, nadiren (hiç?) dışarı çıkar

### Personality
- **Trustworthy ↔ Deceptive:** Mutlak aldatıcı — tüm varlığı bir yalan üzerine kurulu
- **Ambitious ↔ Content:** Sınırsız hırslı, ama yüzyıllık bir sabırla gizlenmiş
- **Loyal ↔ Opportunistic:** Kimseye sadık değil — Sarelle'i bile sadece bir araç olarak görüyor

### Relationships
- **Kullanıyor:** Sarelle Duskbourne — görünüşte üstü, gerçekte manipüle ettiği/devşirdiği bir kaynak
- **Kullanıyor/kullandı:** Draven Holt — doğrudan ona rapor veren aracı
- **Sorumlu:** Dört Ash-Warden hanesinin yıkımı, İmparator Ashkar Vaelthorn'un ölümü

### Notes
- **★★★ Chapter 1'e dahil edilmesi bilinçli bir karar (2026-09-10)** — orijinal fikir Chapter 2/Emberhold'un "Whisper Court" (rakshasa + 2 doppelganger, üç soylu haneye sızmış) elemanıyla birleştirilmişti, ama oyuncu bunu Chapter 1'e çekmek istedi çünkü Chapter 1'de zaten çok fazla iş var ve House Varn ipliği (zaten açık, hiç kullanılmamış) buna mükemmel uyuyor. **Whisper Court konsepti Chapter 2 için hâlâ kullanılabilir** — D.V.'nin Emberhold'daki daha geniş ağı/diğer sızmaları olarak, House Varn'ı onun Karsgate'teki ayağı/üssü olarak tutarak.
- **Nasıl keşfedilir:** İlvaneth'in çaldığı anahtarlık (session 20, hâlâ denenmemiş) House Varn'ın korunan yan kapısını açabilir. Bu, partinin D.V.'ye giden en somut, en oynanabilir yol.
- **Asla erken ifşa etme** — bu kampanyanın en büyük sırrı, sadece gerçek keşif/araştırma yoluyla ortaya çıkmalı.

---

### Sethra Shestendeliath
- **Görünüş:** Kızıl pullu, Kriv gibi — sekiz yaş büyük, evin hâlâ ayaktayken ne olduğunu hatırlayacak kadar büyük. Artık bir Compact yüzbaşısının duruşuyla değil, House Shestendeliath'ın Leydisi olarak taşıyor kendini — aynı disiplin, yeni bir bayrak.
- **Role:** Kriv'in ablası, **Shestendeliath Hold'un Leydisi** (Roskel Gallowmere'e gittiğinden beri Hold'un garnizonunu doğrudan kendi komutasında tutuyor, **~42 asker gün 187, session 32'de doğrulandı**) | **CR/Level:** Fighter **8** (Battle Master) — **gün 137-144 arası (session 26 FF), Kriv'in bizzat eğitimiyle level 7'den level 8'e yükseldi** | **Location:** Shestendeliath Hold
- **HP:** ~81 (level 8, +9) | **AC:** 18 (House Doskarn Mührü ile +1 AC) | **Attack:** Warden's Greatsword (+2 büyülü greatsword, 2d6+STR+2 slashing +1d8 thunder her vuruşta — **Kriv'in hediyesi, gün 187, session 32**, henüz attune etmedi) | **Notable abilities:** Maneuver DC 15, level 8 ASI/feat alındı (DM notu: +2 STR/CON dengesi varsayılabilir, gerekirse oyunda netleştirilir), ~42 asker doğrudan komutasında
- **Demeanor:** Sert, doğrudan, kendinden emin — ama on beş yıllık soğukluğun altında gerçek bir sıcaklık açığa çıktı, kardeşini bulduktan sonra | **Motivation:** Hold'u gerçek bir güce dönüştürmek; evi yıkanları bulup yok etme sözüne sadık kalmak | **Secret:** Yok artık — Vharkoss'u kendi eliyle öldürdü, kontrolsüz bir öfke anında, artık bunu taşıyor.
- **Speech quirk:** Doğrudan, süslemesiz konuşur, seçimini asla savunmaz/özür dilemez: *"Onlar odadaki en güçlü şeydi. On birindim, hiçbir şeyim yoktu. Böyle bir şeyi dışarıdan yenemezsin — kimse yenemez. Ben de içine girdim."*
- **Attitude toward party:** **allied** (gün 104'te bulundu/tanındı — bkz. state.md Live State Flags, tam detay)
- **Faction:** House Shestendeliath (ex-Ironclad Compact — gün 104'te resmen istifa etti)
- **Current goal:** Hold'u gerçek bir güç merkezine dönüştürmek; Coren/Compact hakkında Kriv'e istihbarat sağlamak; Roskel Gallowmere'e gittikten sonra kendi askeri düzenini kurmak
- **Schedule:** Shestendeliath Hold, sabit

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst, seçimlerini gizlemiyor — artık gerçek adını taşıyor, saklamıyor
- **Ambitious ↔ Content:** Yeni bir amaç buldu — Hold'u inşa etmek, on beş yıllık amaçsız avın yerini aldı
- **Loyal ↔ Opportunistic:** Coren'e/Compact'a olan son güveni de kırıldı (evi bizzat Compact'ın yıktığını öğrenince); artık tamamen aileye sadık
- **Brave ↔ Cowardly:** Cesur, savaşarak kendini kanıtlamış — ama Vharkoss'un ölümü gösterdi ki kontrolü de kaybedebilir

### Relationships
- **Family:** Kriv Shestendeliath — kardeşi, gün 104'te yeniden buluştu, tam kabul. İlvaneth'i de aile gibi görüyor (henüz derinleşmedi).
- **Killed:** Vharkoss Shestendeliath — amcaları, zindanda, kontrolsüz bir öfke anında öldürdü
- **Reunited with:** Ser Kethrax — 15 yıl sonra ilk kez gördü, tanıdı; gerçek bir duygusal an
- **Co-rules with:** Yüzbaşı Roskel (Gallowmere'e gitmeden önce devir teslim bekleniyor)
- **Broken with:** Coren Ashvale — Warmarshal'ı, artık değil; istifa etti, sonucu henüz bilinmiyor

### Notes
- **Gün 104-107'nin gerçek dönüşümü:** On beş yıllık amaçsız Vharkoss avı, gerçek bir aile ve gerçek bir amaçla (Hold'u yönetmek) sona erdi — ama Vharkoss'u öldürmesi, Kriv'in "yaşasın, hesap versin" planını bozdu, bilerek değil, kontrolsüz bir anda. Bu, ileride Kriv'le arasında konuşulmamış bir gerginlik kaynağı olabilir (henüz gündeme gelmedi).
- **Vharkoss'un ona yazıp hiç gönderemediği mektup** İlvaneth'te — Sethra bundan haberdar değil, ne zaman/nasıl verileceği açık bir DM kararı.
- **Coren'in tepkisi bilinmiyor** — Renwick'in yumuşatılmış raporu ile süvarilerin çıplak raporu arasında bir yarış var, hangisi önce ulaşırsa çerçeveyi o belirler.

---

### Vharkoss Shestendeliath ("Lord Vharken Sable")
- **Görünüş:** Bronz pullu (Kriv kızıl), daha yaşlı, daha ağır, tamamen "rahat" bir hali var — saygın bir yabancı asilzade kılığında, on beş yıldır kusursuzca oynanan bir rol.
- **Role:** Kriv'in evini içeriden satan amca, artık Karsgate Kingsward'ında saygın bir yaşam sürüyor | **CR/Level:** Sorcerer 9 (Draconic Bloodline) — eğitimsiz ama uyanmakta olan ejderha kanı, sadece köşeye sıkışırsa kullanıyor | **Location:** Karsgate, Kingsward — saygın bir konak, takma ad altında
- **HP:** ~68 | **AC:** 15 (doğal + Mage Armor) | **Attack:** — | **Notable abilities:** Spell save DC 15
- **Demeanor:** Rahat, kendinden memnun, on beş yıllık bir suçla barışmış | **Motivation:** Hayatını sürdürmek, geçmişinin ifşa olmamasını sağlamak | **Secret:** House Shestendeliath'ı içeriden sattı — Warden rotasını ve parçanın yerini bir Concordat aracısına verdi, karşılığında hayatı, yeni bir isim ve para aldı. Kendi gerekçesine gerçekten inanıyor: ev zaten düşecekti, tek soru kimin hayatta kalacağıydı, o da kendini seçti.
- **Attitude toward party:** unmet — Kriv'in hayatta olduğunu bilmiyor
- **Faction:** bağımsız (Karsgate soylular konseyinde saygın bir üye, bir lonca kurulunda oturuyor)
- **Current goal:** Saklanmak, geçmişinin ona ulaşmamasını ummak — on beş yıldır sessiz bir korkuyla yaşıyor
- **Schedule:** Kingsward'daki konağında, lonca toplantılarında, akşam yemeklerinde

### Personality
- **Trustworthy ↔ Deceptive:** Derinden aldatıcı — tüm kimliği bir yalan üzerine kurulu
- **Ambitious ↔ Content:** İçerik — yeni hayatından memnun, sadece keşfedilmekten korkuyor
- **Loyal ↔ Opportunistic:** Fırsatçı — evi satarken de aynı hesabı yaptı, kendini seçti
- **Brave ↔ Cowardly:** Korkak — eğitimli bir savaşçı değil, sadece köşeye sıkışırsa büyüye başvurur

### Relationships
- **Family:** Kriv Shestendeliath — yeğeni, ailesine ihanet etti, hayatta olduğunu bilmiyor
- **Hunted by:** Sethra Shestendeliath — yeğeni, ondan şüpheleniyor ama henüz bulamadı
- **Knows:** Yıkımı Concordat'ın (Compact değil) sipariş ettiğini, aracının adını (Sarelle'in dosyasına giden bir iplik), diğer Ash-Warden evlerinin yerlerini, ve parçanın o gece kurtarıldığını (kimin aldığını bilmiyor — bu onu 15 yıldır sessizce korkutuyor)

### Notes
- **Bu bir dövüş değil, bir sahne olmalı.** Kriv'in onunla ne yapacağı dört farklı yol sunuyor: **öldür** (tatmin edici, 3 bilgi ipliğini kalıcı kapatır), **mahvet** (Lord Sable'ın hain bir dragonborn olduğunu ifşa et — her şeyini kaybeder ama yaşar, ki bu onun için daha kötü olurdu), **kullan** (Karsgate yüksek sosyetesinde saygın, bağlantılı, tamamen sahiplenilebilir bir araç — Neutral Evil bir karakter için ölü bir amcadan daha değerli), **evi geri al onun üzerinden** (serveti zaten Shestendeliath parası, geri kazanılabilir).
- **Yemin mekaniği:** Kriv, evin son meşru varisi olarak yemin-büyüsünü çağırıp Vharkoss'tan dürüst bir hesap verme talep edebilir — o reddedemez (ejderha-yemin büyüsü umursamaz).
- **Move List (consequences.md eşiği, 1/3):** Weight 2'de Karsgate sosyal sahnelerinde tuhaf bir dikkatsizlik/tedirginlik sergiler; Weight 3'te ya kaybolmaya hazırlanır ya da (Kriv'i tespit ettiyse) yüzleşmeden önce kendisi temasa geçmeye çalışır.

---

### Yeva Ashwright
- **Role:** Bölge koordinatörü, Cinder Choir | **Location:** mobil
- **Demeanor:** Bilinmiyor, henüz karşılaşılmadı | **Motivation:** Liderliğin "gerçek bir geri-dönen üretme" doktrin ihlaline dair şüpheleri var — potansiyel bir ikinci Fenn (yani müttefik olabilecek biri) | **Secret:** Gün 85'te Gallowmere hücresinin (Fenn) yok edildiğini keşfetti — parti henüz bunun farkında değil, bu bilgi Hollow Prophet'e doğru ilerliyor.
- **Attitude toward party:** unmet, ama keşfi bir "keşif bombası" — yakında yüzeye çıkabilir
- **Faction:** Cinder Choir
- **Current goal:** Keşfini üst kademeye raporluyor

### Relationships
- **Knows:** Odric Fenn'in öldürüldüğünü (parti tarafından, henüz bağlanmadı)
- **Doubts:** Kendi liderliğini (doktrin ihlali şüphesi)

---

### Mother Vey
- **Role:** Gallowmere simsarı/fence | **Location:** Gallowmere
- **Demeanor:** Yorgun, hesaplı, iki yıldır üç gücü de kasabadan uzak tutmaya çalışan biri | **Motivation:** Gallowmere'i bağımsız tutmak | **Secret:** Partinin ossuary'den ne çıkardığı konusunda yalan söylediğini biliyor.
- **Attitude toward party:** friendly ama kararsız — parti her güç davet ettiğinde (garnizon darbesi gibi) ona bir bedel ödetiyor
- **Kriv'in "Lord Shestendeliath" unvanını bilmiyor** — bu sadece Hold'un hane halkına açıklandı (session 17), Gallowmere'de kalanlara değil. Vey onu sadece "Kriv" olarak tanır, ona asla "Lordum" demez. Garnizon darbesinin gerçekleştiğini bilir (herkes bilir) ama partinin bunu bizzat yaptığını doğrulanmış bir şekilde bilmiyor — sadece şüphelenebilir.
- **Faction:** bağımsız
- **Current goal:** Partinin bir varlık mı yoksa risk mi olduğuna karar vermek (aktif "consequence" clock'u işliyor)

---

### Fennick Orle
- **Role:** Gallowmere bilgi simsarı | **Location:** Gallowmere
- **Demeanor:** Konuşkan, her şeyin fiyatı var | **Motivation:** Bilgi ticareti | **Secret:** Partinin tarifini hem Sefwyn Marrow'a hem Concordat'a sattı, sonra telafi olarak sahte bir Karsgate izi yaydı.
- **Attitude toward party:** friendly (telafi kabul edildi)
- **Faction:** bağımsız

---

### Renwick Tale
- **Görünüş:** İnsan erkek, kırklı yaşların ortası, iyi ama gösterişsiz giyimli — bir tüccarın duruşu, bir askerin değil. Sol elinin serçe parmağı yok, eski bir "borç" hatırlatıcısı Compact'a tırmanırken kalmış — konuşurken düşünceli anlarda o güdük parmağı masaya vurur, fark edilmeden.
- **Role:** Ironclad Compact'ın Gallowmere kontağı, ekonomik operasyon yürütüyor | **CR/Level:** Rogue 4 (gerekirse) | **Location:** Gallow's Anchor, rıhtımın sonu, Gallowmere
- **HP:** ~27 | **AC:** 13 | **Demeanor:** Sakin, kontrollü, sesini hiç yükseltmez — her şeyi bir pazarlık olarak görür, tehdit bile nazik bir tonla gelir | **Motivation:** Coren Ashvale'e Gallowmere'in yeniden Compact'ın ekonomik gölgesi altına girdiğini kanıtlamak, açık bir çatışma olmadan | **Secret:** Bu ekonomik baskı kısmen bir test — Coren, Kriv'in gerçekten bu kadar meşgulken (Karsgate, Ashen Crown) Gallowmere'i savunacak iradesi/kapasitesi olup olmadığını görmek istiyor. Renwick'in raporları doğrudan Coren'e gidiyor.
- **Speech quirk:** Her cümlesi bir teklif gibi kurulur — "belki", "düşünsenize", asla doğrudan bir emir ya da tehdit
- **Attitude toward party:** unmet, ama Kriv'in kimliğini artık biliyor (kasaba meydanındaki sahneyi duymuş olması an meselesi) — temkinli, açık düşmanlık henüz yok
- **Faction:** Ironclad Compact
- **Current goal:** Gallowmere'in ekonomik kontrolünü sessizce sağlamlaştırmak, garnizonun döndüğünü fark ettirmeden
- **Schedule:** Her öğlen Gallow's Anchor'da kendi masasında, yanında 2-3 adam (görünürde silahsız ama hazır)

### Personality
- **Trustworthy ↔ Deceptive:** Yarı yarıya — sözünü tutar ama söylediği her şey seçilerek söylenmiştir
- **Loyal ↔ Opportunistic:** Coren'e sadık, ama kendi çıkarını da gözetir
- **Brave ↔ Cowardly:** Doğrudan çatışmadan kaçınır, ama korkak değil — sakinliği gerçek bir özgüvenden gelir

### Relationships
- **Reports to:** Coren Ashvale (Ironclad Compact, Warmarshal)
- **Watches:** Mother Vey — birbirlerinin ne yaptığını biliyor, açık çatışmaya girmiyorlar

### Notes
- İlk temas session 22'de, Gallow's Anchor'da — parti Fennick'in bilgisiyle bulmuş.

---

### Deacon Perrin Vask
- **Görünüş:** İnsan erkek, elli yaşlarında, kısa boylu, kuru yapılı — yıllarca kül/toz içinde çalışmış birinin çökük göğsü, hafif kronik bir öksürüğü var. Gümüş yarım maskenin altından görünen cildi solgun, gözlerinin altı morarmış. Elleri yanık izleriyle dolu (ash-ritual çalışmasının imzası).
- **Role:** Ashlord Concordat soruşturmacı-rahibi, Sarelle'in toplama döngüsünde saha ajanı | **CR/Level:** Cleric 5 (Ash Domain, gerekirse) | **Location:** yakalandı, Gallowmere garnizon hücresinde tutuluyor
- **HP:** 22 (mevcut 0, baygın/stabil) | **AC:** 12 | **Demeanor:** Alışkın, prosedürel — bu konuşmayı yüzlerce kez yapmış biri, ama gerçekte yorgun ve hasta (kronik öksürük) | **Motivation:** Sarelle'e sadık, görevini yapıyor — kişisel bir kin taşımıyor | **Secret:** Aracı arabası "elf+dragonborn" tarifine uyan bir tutsağı canlı taşımak için özel donanımlıydı (dampening ward + sessizlik taşları) — bu, Sarelle'in avının artık sadece bilgi toplamak değil, doğrudan yakalamaya evrildiğini gösteriyor.
- **Attitude toward party:** **deceased** — sorgulandı (dürüst cevap verdi, Detect Thoughts ile doğrulandı), sorgu bitince Kriv tarafından infaz edildi (gün 103 akşamı, Gallowmere garnizon hücresi)
- **Faction:** Ashlord Concordat
- **Current goal:** (ölmeden önce) tarama görevini tamamlamak, Sarelle'e rapor vermek
- **Schedule:** Artık yok — öldü

### Notes
- Escortu (8 ölü-doğa muhafız) session 22'de tamamen yok edildi, Thornlands yolunda, Hold-Gallowmere seferi sırasında. Concordat bu birimin kaybolduğunu henüz fark etmedi.
- Sorguda verdiği bilgiler: Sarelle'in ikinci adamı artık Solenne Kavash; Sarelle'in bölgesel gücü (~200-300 personel + Ashvale'de büyük ölü-doğa garnizonu); Sarelle'in "iç sızıntı" paranoyası (sömürülebilir zayıflık); doğrulanmamış bir fısıltı — Sarelle İmparator'un ölümünden önceki eski kayıtlarla ilgileniyor. Draven Holt'u tanımıyordu.
- Kız kardeşine (Harrowgate) üç haftadır yazmadığı bir mektup vardı, Detect Thoughts ile görüldü — artık asla yazılmayacak.

---

### Sefwyn Marrow ("The Grey Tally")
- **Role:** Rakip fixer, artık kısmi ortak | **Location:** mobil
- **Demeanor:** Hesaplı, kimseye tam bağlı değil | **Motivation:** Zengin ve sahipsiz kaybolmak | **Secret:** Partinin kendisine verdiği her Crown bilgisi onu daha hızlı satıp kaybolmaya itiyor (aktif clock).
- **Attitude toward party:** warming
- **Current goal:** Orell Tain'in araştırma mektubunu partiye ulaştırdı — gerçek bir aracı rolü üstlendi

---

### Corran
- **Role:** Thornwick tüccarı | **Location:** Thornwick
- **Demeanor:** Güvenilir, iş odaklı | **Motivation:** Sağlam ticaret ilişkileri | **Secret:** yok, iyi bir müttefik.
- **Attitude toward party:** good
- **Current goal:** Ilvaneth'in kumar kimliğini örtüyor; Kriv'in mührünü bulduğu teminat odasını açtı

---

### Corvin Thale
- **Role:** Harrowgate antika satıcısı | **Location:** Harrowgate
- **Demeanor:** Takıntılı koleksiyoncu | **Motivation:** Crown'a yakın buluntuları görmek | **Secret:** Takıntısı gelecekte bir risk haline gelebilir.
- **Attitude toward party:** wary — standart anlaşma (Crown'a yakın buluntuları önce ona göstermek)

---

### Sylvenna
- **Role:** Dryad | **Location:** Weeping Wood
- **Demeanor:** Doğaüstü, sabırlı | **Motivation:** Ormanın dengesini korumak | **Secret:** Üç faction'ın gizli kuruluş tarihini biliyor — parti bu kaldıracı henüz kullanmadı.
- **Attitude toward party:** friendly

---

### Roskel (Sergeant)
- **Role:** Companion — Gallowmere'in Yüzbaşısı (gün 107'den beri, Hold'dan taşındı, Dallin Marsh'ın yanında) | **Location:** Gallowmere
- **Demeanor:** Sadık, disiplinli, eski asker | **Motivation:** Kriv'e hizmet etmek, evi restore etmek | **Secret:** yok — 12 firarinin tek hayatta kalanı, parti tarafından savaşta değil müzakereyle kurtarılabilirdi ama saldırıldı; o hayatta kaldı ve sadakatle karşılık verdi.
- **Attitude toward party:** allied
- **Faction:** House Shestendeliath
- **Current goal:** Gallowmere'in asker eğitimini/yeniden yapılanmasını yönetmek, Sending Stone ile Kriv'e bağlı

---

### Nairne Thistle
- **Role:** Cair Dunnow köy ihtiyarı | **Location:** Cair Dunnow, Cindermoor
- **Demeanor:** Bilge, töreleri koruyan | **Motivation:** Köyün eski bilgisini korumak | **Secret:** Ashen Crown'un gerçek (yas-kalıntısı) kökenini biliyor — Concordat ve Choir'ın hiçbiri bunu bilmiyor, sadece Cair Dunnow korudu.
- **Attitude toward party:** warming (parti töreni dürüstçe yerine getirdi, gerçek bir doktrin düzeltmesi kazandılar)

---

### Kessra Vane
- **Role:** Simsar | **Location:** mobil
- **Demeanor:** Fırsatçı ama profesyonel | **Motivation:** Kâr | **Secret:** Partiyi tanıdı (gün 55) ama ele vermek yerine ortaklık teklif etti — kabul edildi. Ilvaneth'in sahte Karsgate satış belgesinin ikinci bilmeden taşıyıcısı da o.
- **Attitude toward party:** allied (fencing ortaklığı)

---

### Kessic Ambrey
- **Role:** Cinder Choir hücresi | **Location:** Karsgate Undercity
- **Demeanor:** Bilinmiyor, henüz karşılaşılmadı | **Motivation:** Bilinmiyor | **Secret:** Yetkisiz bir arama yapıyor (aktif clock — Varic Sennett'le eşleşen bir çift).
- **Attitude toward party:** unmet
- **Faction:** Cinder Choir

---

### Varic Sennett
- **Role:** bağımsız | **Location:** Karsgate
- **Demeanor:** Bilinmiyor, henüz karşılaşılmadı | **Motivation:** Kessic Ambrey'in hücresini doğrulamak/harekete geçirmek | **Secret:** yok.
- **Attitude toward party:** unmet

---

### Aldric Venn
- **Görünüş:** Yarı-elf, altmışlı yaşlarda (üzerinde dinç bir orta yaş gibi duruyor), yemeyi unutan biri gibi zayıf. Sade cübbe, üzerinde eskimiş bir kor-taç kolyesi dışında takı yok.
- **Role:** Harrowgate'teki Kor Taç Tapınağı'nın başrahibi (ortodoks imparatorluk kültü) | **CR/Level:** Cleric 6 (Yaşam Alanı) | **Location:** Kor Taç Tapınağı, Harrowgate
- **HP:** ~44 | **AC:** 13 | **Attack:** belirtilmemiş | **Notable abilities:** Büyü DC 13 — savaşçı değil, koruyucu bir rahip
- **Demeanor:** Sakin ve ölçülü görünür ama bu disiplinden kaynaklanır — altında gerçek bir korku var | **Motivation:** İnancının gerçek anlamını hem Concordat'ın bürokratik versiyonuna hem de Cinder Choir'in şiddet dolu sapkınlığına karşı korumak | **Secret:** Cinder Choir'in bölgede aktif hücreleri (Ash-Kilns dahil) olduğunu biliyor ama harekete geçecek gücü yok.
- **Attitude toward party:** neutral (session 4'te ilk yüz yüze görüşme, henüz güven inşa aşamasında)
- **Faction:** Ortodoks İmparatorluk Kültü (bağımsız, Concordat'a ve Cinder Choir'e karşı)
- **Current goal:** Ash-Kilns hücresine karşı harekete geçebilecek birini bulmak; karşılığında tapınak arşivini araştırma için sunmaya hazır
- **Schedule:** Kor Taç Tapınağı'nda, Harrowgate

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst ve açık sözlü ama tam güven inşa olana kadar tam arşiv erişimi vermiyor
- **Ambitious ↔ Content:** Hırslı değil — sadece inancını korumak istiyor
- **Loyal ↔ Opportunistic:** Kendi inancına ve cemaatine sadık, siyaset yapmıyor
- **Brave ↔ Cowardly:** Savaşçı değil ve gücü yok, ama korkusuna rağmen tehdidi açıkça isimlendirdi

### Relationships
- **Knows:** Sarelle Duskbourne'un Concordat doktrinine sessizce karşı (doktrinsel, açık çatışma değil)
- **Fears/Allied with:** Yüce Rahip Varic Sennett'e (Karsgate) eşik 3'e ulaşırsa haber verebilir

### Notes
- `consequences.md`'nin "Aldric Venn — Choir Tehdidine Sabrı Tükeniyor" eşiğine bağlı (şu an 1/3). Ağırlık 3'e ulaşırsa kendini tehlikeye atan bir adım atar.

---

### Alis Wend
- **Görünüş:** Kaynakta ayrıntılı fiziksel tasvir yok — yarı-elf kadın, iki küçük çocuğuyla, Thornwick'ten kaçmış bir mülteci.
- **Role:** Mülteci anne, partinin dolandırdığı kurban — artık Kriv'in hizmetinde | **Location:** Gallowmere mülteci kampı (eskiden); artık Shestendeliath Hold
- **Demeanor:** Önce öfkeli ve acı dolu, şimdi minnettar ve sadık | **Motivation:** Çocukları için güvenlik, ev ve iş | **Secret:** Kriv'in gerçek adını ve evini bilmiyor.
- **Attitude toward party:** friendly/allied (day 74'te Kriv'in hizmetine alındı, 20 altın verildi; ama partinin onu iki kez kandırdığını hâlâ bilmiyor)
- **Faction:** Shestendeliath Hold (Kriv'in hizmetinde)
- **Current goal:** Kriv adına mülteci kampından başka aileler/kişiler topluyor (Bertrand ailesi, tiefling Vesper, marangoz Corrik)
- **Schedule:** Artık Shestendeliath Hold'da

### Personality
- **Trustworthy ↔ Deceptive:** Kendisi dürüst ama iki kez kandırıldı; gerçeği öğrenirse güveni tamamen çökebilir
- **Ambitious ↔ Content:** Hırslı değil, sadece hayatta kalmak istiyor
- **Loyal ↔ Opportunistic:** Şu an tamamen sadık, Kriv'in gerçek kimliğini sorgulamadı
- **Brave ↔ Cowardly:** Kampın kenarında partiyle yüzleşecek kadar cesur ama gerçek gücü yok

### Relationships
- **Knows:** Hesta Bram'ın köyünden (Thornwick) geliyor — orada tanınırsa Hesta köyü partiye tamamen kapatır
- **Hates/Fears:** Sefwyn Marrow hikayesini parti aleyhine satın alabilir

### Notes
- Kapanmış bir sonuç ipliğiydi, day 74'te gerçek bir işe alım ipliği olarak yeniden açıldı. Partinin sözünü tutup tutmayacağı hâlâ bir güç tabanı fırsatı.

---

### Bertrand Ailesi
- **Görünüş:** Kaynakta bireysel tasvir yok — cüce bir çift ve iki oğulları, Thornlands'ın savaştan harap tarım topraklarından kaçmışlar.
- **Role:** Çiftçiler, artık Hold'un kendi topraklarını işliyorlar | **Location:** Shestendeliath Hold
- **Demeanor:** Pratik, sessiz, ağır işe ve dünyadan az beklentiye alışkın | **Motivation:** İşlenecek toprak, oğulları için güvenlik, mülteci olmaktan çıkmak | **Secret:** yok.
- **Attitude toward party:** friendly (Alis Wend aracılığıyla işe alındılar, day 81'de Hold'a yerleştiler)
- **Faction:** Shestendeliath Hold
- **Current goal:** Hold'daki kendi topraklarını işlemek
- **Schedule:** Shestendeliath Hold'da, sürekli

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen güvenilir, sorgusuz sadık
- **Ambitious ↔ Content:** İçerikliler — sadece istikrar istiyorlar
- **Loyal ↔ Opportunistic:** Kriv kim olursa olsun sadıklar

### Relationships
- **Knows:** Alis Wend onları aynı mülteci kampından işe aldı
- **Allied with:** Corrik ve Vesper ile birlikte Hold'un yeni personeli

### Notes
- Bu session'da kazanılan tüm NPC'ler Minor sayılıyor, Hold'un hane halkı altında kayıtlı.

---

### Borgha Kresk
- **Görünüş:** Yarı-ork kadın, kırklı yaşların ortasında, örs gibi yapılı — geniş omuzlar, eski yanıklardan solmuş ön kollar, kurumlu deri önlük, kısa ve yer yer kavrulmuş saçlar.
- **Role:** Usta demirci, Harrowgate Ironmonger's Row'daki bir düzine dükkândan biri | **Location:** Ironmonger's Row, Harrowgate
- **Demeanor:** Kısa, değerlendirici cümlelerle konuşur; masada metal varken nezaket için nefes harcamaz | **Motivation:** Dürüst mal, adil ticaret, bela istemiyor | **Secret:** yok.
- **Speech quirk:** Kısa, işe odaklı cümleler
- **Attitude toward party:** neutral/dostane (day 52'de parti ona ölü bir Lonca kuryesinin duergar uyarısını getirince, artık sabit gerçek fiyat üzerinden pazarlıksız işlem yapıyor)
- **Faction:** Bağımsız (Ironmonger's Row esnafı)
- **Current goal:** Dükkânını stoklu tutmak; Kesh Deeps'teki duergar tehdidini Lonca'ya iletmek
- **Schedule:** Ironmonger's Row'daki forjunda, günlük

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst tüccar, malın nereden geldiğini pek sormaz
- **Ambitious ↔ Content:** İçerikli — sıradan bir esnaf hayatından memnun
- **Loyal ↔ Opportunistic:** İyi bir anlaşmaya sadık kalır

### Relationships
- **Knows:** Kriv'in Demirci Aletleri yeterliliğini fark edip meslek muhabbeti yapabilir
- **Allied with:** Parti ile day 52'den beri gerçek fiyat anlaşması

### Notes
- Bölgesel demirci dedikodusu (olağandışı metal siparişleri) küçük bir ipucu kaynağı olabilir.

---

### Cole
- **Görünüş:** Yarı-elf kadın, otuzlu yaşlarında görünüyor, keskin bakışlı ve hızlı elli. Dirseklerine kadar sıvanmış kollar, kurumuş reaktiflerle lekelenmiş parmaklar, saçına itilmiş ince tel gözlük.
- **Role:** Eczacı ve simyager, Thornlands'taki tek güvenilir büyülü eşya tanımlayıcısı | **Location:** Vestry & Cole, Harrowgate
- **Demeanor:** İş odaklı ama soğuk değil — garip bir buluşa gerçekten seviniyor | **Motivation:** Dükkânı stoklu tutmak, bölgenin tek güvenilir tanımlayıcısı ününü korumak | **Secret:** "Vestry" ismi sorulmadıkça anılmıyor, konu açılınca konuyu değiştiriyor.
- **Attitude toward party:** neutral (düzenli müşteri, session 6'dan önce kurulmuş bir iş ilişkisi)
- **Faction:** Bağımsız
- **Current goal:** Dükkânı işletmek, tanımlama hizmeti sunmak
- **Schedule:** Vestry & Cole'da, Harrowgate

### Personality
- **Trustworthy ↔ Deceptive:** Güvenilir, iş odaklı dürüstlük

### Relationships
- **Knows:** "Vestry" hakkında açıklamadığı bir geçmişi var — muhtemelen eski bir ortak
- **Allied with:** Parti ile düzenli müşteri ilişkisi

### Notes
- Harrowgate'in tek büyülü eşya tanımlayıcısı — mekanik bir boşluğu (Identify kontrolleri) dolduruyor.

---

### Corla Vint
- **Görünüş:** Gnome kadın, bilinçli olarak sıradan — gri kıyafetler, gri saçlar, beş dakika sonra tarif edilmesi zor bir yüz.
- **Role:** Karsgate'in kirli-sözleşme simsarı (hırsızlık, kaçırma, para yeterse daha kötüsü) | **CR/Level:** Rogue 4 | **Location:** The Broken Wheel, Karsgate (the Reeks)
- **HP:** ~27 | **AC:** 14 | **Notable abilities:** Kasıtlı olarak dövüşte unutulabilir — gücü savaşta değil, bilgi ve mesafede
- **Demeanor:** Profesyonel, yargısız; her işi gerçek riske göre dürüstçe fiyatlandırır | **Motivation:** Zengin, yaşlı ve hiçbir şeye kişisel olarak bağlanmadan ölmek | **Secret:** Hiçbir kayıt tutmuyor; çocuklara karşı iş almaz, kendisine karşılıksız iyilik yapmış birine karşı iş almaz.
- **Attitude toward party:** unmet (partiyi henüz tanımıyor)
- **Faction:** Bağımsız (üç hizipten de teklifleri reddetti)
- **Current goal:** Ninefinger ekibi ve serbest çalışanlar aracılığıyla işleri yürütmeye devam etmek
- **Schedule:** Neredeyse her gece The Broken Wheel'in arka masasında

### Personality
- **Trustworthy ↔ Deceptive:** Müşterilere karşı dürüst ve profesyonel ama tehdit edilirse müşteri adını hemen verir
- **Ambitious ↔ Content:** Hırslı değil — büyümek yerine hayatta kalmayı ve iz bırakmamayı önceliklendiriyor
- **Loyal ↔ Opportunistic:** Fırsatçı — hiçbir hizibe sadık değil, sadece kendi hayatına

### Relationships
- **Knows:** Ninefinger ekibi; Orvenna Kest (The Wagered Crown — kirli paranın temizlendiği yer)
- **Allied with/Hates:** "Iron" Sella Dray (Red Tally) ile rakip; "The Broker" Ostren Vale (Ironhold) ile hiç tanışmadı ama yöntemlerini anında tanır

### Notes
- `consequences.md`'nin "Corla Vint — The Broken Wheel's Reach" eşiği (1/3). Eşik 3'e ulaşırsa ağı Red Tally'ye rakip gerçek bir güç merkezi haline gelir.

---

### Corrik
- **Görünüş:** Kaynakta ayrıntı yok — yaşlı bir insan erkek, ailesi kalmamış, işinde becerikli.
- **Role:** Marangoz, Hold'un yeni nüfusu için konut inşa ediyor | **Location:** Shestendeliath Hold
- **Demeanor:** Mesleğine yeniden gerçek bir kullanım bulmaktan memnun | **Motivation:** Amaç ve bir atölye | **Secret:** yok.
- **Attitude toward party:** friendly (Alis Wend aracılığıyla işe alındı, day 81'de Hold'a vardı)
- **Faction:** Shestendeliath Hold
- **Current goal:** Hold'da gerçek konutlar inşa etmek
- **Schedule:** Shestendeliath Hold'da, atölyesinde

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen güvenilir
- **Loyal ↔ Opportunistic:** Sadık

### Relationships
- **Knows:** Alis Wend onu Gallowmere mülteci kampından işe aldı
- **Allied with:** Bertrand ailesi ve Vesper ile birlikte Hold'un yeni personeli

### Notes
- Marangozluk becerisi Hold'un yeni konut inşaatının gerçek mekanizması.

---

### Dallin Marsh
- **Görünüş:** İnsan erkek, kırklı yaşların başında, grileşen sakal, kötü uyku ve borçlardan gözlerinin altında koyu halkalar. Sol bileğinde bir tefeci tahsildarından taze bir çürük.
- **Role:** Garnizon çavuşu, artık Kriv'in kişisel bir varlığı — fiilen komutan | **CR/Level:** Fighter 3 | **Location:** Gallowmere garnizon binası, kuzey kapısı yanında
- **HP:** ~28 | **AC:** 14 (dövme deri) | **Demeanor:** Yorgun ama sert değil — hiçbir zaman çavuşluktan öteye geçememiş bir kariyer askeri | **Motivation:** Kell'in gölgesinden ve borçlarından kurtulmak, artık Kriv'e sadakat | **Secret:** Kell'in Ironclad Compact'tan gizli para aldığını Kriv'e ifşa etti.
- **Attitude toward party:** allied (Kriv Fennick borcunu bağışladı, Drask borcunu üstlendi, karşılığında istihbarat sağladı)
- **Faction:** Shestendeliath Hold / Kriv'in hizmetinde (eski Gallowmere garnizonu)
- **Current goal:** Kell'in devrilmesinden sonra kaptansız kalan garnizonu fiilen yönetmek (henüz resmileşmedi)
- **Schedule:** Gallowmere garnizon binasında

### Personality
- **Trustworthy ↔ Deceptive:** Güvenilir — sözünü tuttu, Kriv'e karşı dürüst
- **Loyal ↔ Opportunistic:** Artık tamamen Kriv'e sadık — coup gecesi 21/30 askeri onun tarafına çekti
- **Brave ↔ Cowardly:** Kendi komutanına karşı ayaklanacak kadar cesur

### Relationships
- **Knows/Owes:** Kriv'e borçlu (Fennick Orle borcu bağışlandı, Drask borcu üstlenildi)
- **Hates/Fears:** Eski komutanı Doreth Kell'e karşı ayaklandı

### Notes
- Kell kaçtığı için sızıntı ifşa riski artık anlamsız. Garnizonun fiili sahibi.

---

### Doreth Kell (Yüzbaşı)
- **Görünüş:** İnsan erkek, kariyer asker, kırklı yaşların ortası, yıpranmış, yetkin, yorgun.
- **Role:** Garnizon komutanı; resmen Gallowmere'de tacın otoritesi (artık kaçtı) | **CR/Level:** Fighter 6 | **Location:** Eskiden Gallowmere garnizon binası — artık bilinmiyor, kız kardeşinin ailesiyle güneye kaçtı
- **HP:** ~58 | **AC:** 16 (zincir zırh) | **Demeanor:** Yorgun, köşeye sıkışmış bir adam — uysal değil | **Motivation:** Sadece kaçmak istiyordu | **Secret:** Ironclad Compact'tan maaş alıyordu, garnizon malzemelerini çalıp satıyordu.
- **Attitude toward party:** kaçtı/yok — sahneden tamamen çekildi (session 17, day 75), coup sonrası her şeyi teslim edip serbest bırakıldı. *(Öldürülmedi — "deceased" değil.)*
- **Faction:** Nominal olarak Taç; gizlice Ironclad Compact
- **Current goal:** "Yüzbaşı Kell" kimliğini bırakıp yeni bir kimlikle güneyde hayatta kalmak
- **Schedule:** Artık Gallowmere'de değil — akıbeti bilinmiyor

### Personality
- **Trustworthy ↔ Deceptive:** Aldatıcı — yıllarca hem taca hem Compact'a karşı çifte oyun oynadı
- **Loyal ↔ Opportunistic:** Fırsatçı — köşeye sıkışınca her şeyi hemen teslim etti
- **Brave ↔ Cowardly:** Savaşmadı, pazarlık etti — kaçmayı seçti

### Relationships
- **Knows/Owes:** Ironclad Compact / Coren Ashvale'e (gerçek patronu) bağlı; Mother Vey ile karşılıklı müdahale etmeme anlaşması vardı
- **Hates/Fears:** Kendi çavuşu Dallin Marsh'ın onu ihbar ettiğini asla öğrenemedi

### Notes
- The Drowned Mill'deki kaçakçı deposu ipliği kendisi olmadan da açık kalabilir.

---

### Dunnel Ashe
- **Görünüş:** İnsan erkek, kendi hafızasına göre otuzlu yaşların ortasında (sekiz yıldır aynaya bakmamış), çekingen, ormanın sunduğu her şeyle beslenmekten sıska. Domuz formunda: büyük, yara izli, kalabalık patikalardan kaçınır.
- **Role:** Lanetli domuz-adam, eskiden Ostwick'te çiftçi işçisi — artık iyileşmiş ve Shestendeliath Hold'da hizmette | **Location:** Ostwick çevresindeki ormanlar (eskiden); artık Shestendeliath Hold
- **Demeanor:** Geri çekilmiş, ender ve dikkatli konuşur | **Motivation:** Tanıdığı kimseye asla bir daha zarar vermemek | **Secret:** Laneti kontrol etmesinin giderek zorlaştığını kız kardeşine bile söylemedi; belirsiz bir iyileşme söylentisini biliyor ama hiç peşine düşmedi.
- **Attitude toward party:** allied/minnettar (session 14, day 62'de Ilvaneth tarafından Remove Curse ile iyileştirildi, karşılığında kız kardeşi Maren ile Hold'a taşınıp hizmet etmeyi kabul etti)
- **Faction:** Shestendeliath Hold
- **Current goal:** Yeni hayatına, insan olarak, Hold'da uyum sağlamak
- **Schedule:** Day 63'te Hold'a doğru yola çıktı

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — sekiz yıl sırrını korudu ama kimseyi kandırmadı
- **Loyal ↔ Opportunistic:** Sadık — kız kardeşine ve Ostwick'e karşı derin sorumluluk hissi
- **Brave ↔ Cowardly:** Kontrolünü kaybetmekten korkarak kaçar, tehdit değil çekilme tercih eder

### Relationships
- **Knows:** Kız kardeşi Maren Ashe — laneti giderek zorlaştığını ondan bile sakladı
- **Allied with:** Ilvaneth'e (iyileştiren) ve Ostwick köyüne bağlı

### Notes
- Minör ama dokunaklı bir iplik — kendi isteği hiç kimseye bir daha zarar vermemek. Gelecekte tekrar gündeme gelebilir.

---

### Halvard Verrick
- **Görünüş:** Yarı-elf, kırklı-ellili yaşlarda, güzel hatları çökmüş, saçları ağarmış. Eskiden iyi bir kaftan giyiyor, artık incelmiş.
- **Role:** Savaştan kaçan bir tüccar ailesinin reisi, taşıdıklarını sessizce elden çıkarıyor | **Location:** Eski Corley çiftliği, kiralık, Ostwick dışında
- **Demeanor:** Onurla, acıma değil, muamele görmek istiyor | **Motivation:** Ailesinin son eşyalarını satarken saygıyla davranılmak | **Secret:** yok.
- **Attitude toward party:** warming (day 49'da gerçek minnettarlıkla bitti; parti eşyaları adil fiyata — 90 altın — aldı, Ilvaneth şecere kitabını hediye olarak aldı)
- **Faction:** Bağımsız
- **Current goal:** Ailesinin kalan eşyalarını adil biçimde satmak
- **Schedule:** Corley çiftliğinde, Ostwick yakınında

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — rakip bir tüccar tarafından kandırılmıştı, tekrar kandırılmaya karşı hassas

### Relationships
- **Knows:** Wren Talbot (The Hollow Sheaf) onu partiye yönlendirdi
- **Hates/Fears:** Corvin Thale'nin gerçek alıcı olduğunu bilmiyor

### Notes
- Rakip tüccarın Corvin Thale'nin ticaret rakipleriyle bağlantılı olabileceği henüz doğrulanmadı.

---

### Hesta Bram
- **Görünüş:** Dragonborn kadın, iri yapılı, pullarını takip eden dövmeli ön kollar. Her yeni geleni bara ulaşmadan tartıyor.
- **Role:** Hancı, "The Log" hanı — Thornwick köyünün resmi olmayan omurgası | **Location:** The Log, Thornwick
- **Demeanor:** Ne düşman ne sıcak — çoğu akşam zar oyunu işletir, bahisleri kasıtlı düşük tutar | **Motivation:** Thornwick'in gelecek yıl da var olması; on bir yıl askerlik yaptı | **Secret:** Concordat'ın Vaelthorn kriptindeki kazıyı gece gizlice izledi — kimseye söylemedi.
- **Attitude toward party:** neutral/temkinli (partiyi tehlikeli olarak hemen tanıdı)
- **Faction:** Bağımsız (Thornwick)
- **Current goal:** Sorrel's Hollow'daki haydutların çözülmesini istiyor
- **Schedule:** The Log'da, Thornwick, her akşam zar oyunu

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst ama ihtiyatlı
- **Loyal ↔ Opportunistic:** Köyüne tamamen sadık, dışarıdakilere karşı temkinli

### Relationships
- **Knows:** Alis Wend'in memleketi Thornwick — tanınırsa köyü partiye kapatır
- **Hates:** Corran'dan nefret ediyor — kaçan ailelerden toprak satın aldığı için

### Notes
- Vaelthorn kripti hakkında partinin başka hiçbir yerden alamayacağı bir görgü tanığı bilgisi var. Sorrel's Hollow'u temizlemek sadakatini doğrudan kazandırır.

---

### Maren Ashe
- **Görünüş:** İnsan kadın, yaşından yaşlı görünüyor, iş yorgunu eller, keskin ve tetikte gözler.
- **Role:** Dunnel Ashe'in kız kardeşi; onun eski evini koruyor | **Location:** Ashe Çiftliği, Ostwick (eskiden); artık Shestendeliath Hold'a taşınıyor
- **Demeanor:** Sekiz yıldır bu konuşmayı kafasında yüzlerce kez yapmış, yorgun ama yumuşak değil | **Motivation:** Kardeşini avcılardan ve köyün korkusundan korumak | **Secret:** Dunnel'in laneti kontrol etmesinin zorlaştığını bilmiyor.
- **Attitude toward party:** allied/minnettar (day 62'de Ilvaneth kardeşinin iyileştiğini kanıtladı, ikisi de Hold'a taşınmayı kabul etti)
- **Faction:** Shestendeliath Hold
- **Current goal:** Sekiz yıldır bildiği her şeyi bırakıp Hold'a taşınmaya hazırlanıyor
- **Schedule:** Ashe Çiftliği'nde (taşınana kadar)

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst — köyün sırrını sekiz yıl sadakatle korudu
- **Loyal ↔ Opportunistic:** Son derece sadık — kardeşi için her şeyi kabul etti
- **Brave ↔ Cowardly:** Cesur — sekiz yıl korkuyla yüzleşti

### Relationships
- **Knows:** Kardeşi Dunnel Ashe
- **Allied with:** Ostwick köyü — sırrı sekiz yıl birlikte korudular

### Notes
- Ostwick'in paylaşılan sırrının son gerçek bekçisiydi. Artık Hold'a taşınıyor.

---

### Marta Vantor
- **Görünüş:** Yarı-elf kadın, altmışlı yaşların ortası, bu kadar zengin biri için sade giyiniyor.
- **Role:** Vantor Shipping Concern'in sahibi ve başı, Karsgate'in en büyük nehir-ticareti şirketi | **CR/Level:** Bard 5 (Bilgi Koleji) | **Location:** Vantor Shipping Concern ofisleri (the Ledger) ve depo (Riverside), Karsgate
- **HP:** ~33 | **AC:** 12 | **Notable abilities:** Gerçek silahı sermaye ve bilgi — savaşmaz, koruma kiralar
- **Demeanor:** Keskin, sayılarla hızlı, zaman kaybettirenlere karşı sabırsız | **Motivation:** Vantor Shipping'i etrafından dolaşılamayacak kadar büyük yapmak | **Secret:** Gallowmere kaçakçılık rotasından zaten yıllardır kazanç sağlıyor; rakip bir şirketi iflasa sürüklemek için gizli rezervlerle agresif fiyat kırıyor.
- **Attitude toward party:** unmet
- **Faction:** Bağımsız (Vantor Shipping Concern)
- **Current goal:** Rakip şirketi iflasa sürüklemek ve ticaretini emmek
- **Schedule:** Ofisleri (the Ledger) ve deposu (Riverside), Karsgate

### Personality
- **Trustworthy ↔ Deceptive:** Profesyonel dürüstlük — anlaşmaları sadece sayılara göre değerlendirir
- **Ambitious ↔ Content:** Çok hırslı — nehir ticaretinde tam kontrol istiyor
- **Loyal ↔ Opportunistic:** Fırsatçı ama intikamcı değil

### Relationships
- **Knows:** Gallowmere kaçakçılık rotasını zaten biliyor — parti orada habersizce faaliyet gösterirse fark eder
- **Hates/Allied with:** Rakip nakliye şirketiyle acımasız rekabet içinde

### Notes
- `consequences.md`'nin "Marta Vantor — Düşük Fiyat Kampanyası" eşiği (1/3). Karsgate'in nehir ticareti güç dengesini doğrudan etkiler.

---

### Nessa Wren
- **Görünüş:** İnsan kadın, saha ajanından çok bir arşivci gibi: pratik yolculuk kıyafetleri, mürekkep lekeli parmaklar.
- **Role:** Ashlord Concordat arşivcisi, kül-kral sembolleri için bölgesel höyükleri tarıyordu | **Location:** Cindermoor yolu üzerinde karşılaşıldı (day 56) — artık ölü; bedeni ve not defteri partide
- **Demeanor:** Yetkin bir profesyonel, güvenmediği bir hizip için çalışmıyordu | **Motivation:** Sarelle Duskbourne'un görevlendirdiği işi tamamlamak | **Secret:** Not defterinde Kesh Deeps "öncelik, taranmamış, duergar faaliyeti bildirildi" diye işaretliydi.
- **Attitude toward party:** deceased (öldürüldü, session 10, day 56 — sorgulandıktan sonra tanık olmadan öldürüldü)
- **Faction:** Ashlord Concordat
- **Current goal:** (hayattayken) Kesh Deeps'e gitmek üzereydi
- **Schedule:** Cindermoor yolunda öldürüldü

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst bir profesyonel, gizli bir gündemi yoktu
- **Loyal ↔ Opportunistic:** Concordat'a sadıktı

### Relationships
- **Knows:** Sarelle Duskbourne ona doğrudan görevlendirme yaptı — Sarelle onun kaybolduğunu henüz bilmiyor
- **Hates/Fears:** Kriv Shestendeliath şu an bedenini ve not defterini elinde tutuyor (gelecekte Animate Dead adayı)

### Notes
- Kaybolması Concordat tarafından henüz partiyle ilişkilendirilmedi — şu an durgun ama gerçek bir risk.

---

### Odric Fenn
- **Görünüş:** İnsan erkek, ellili yaşlarda, kısa kesilmiş kül-gri saç, on yıllardır kremasyon külü tutmaktan kalıcı soluk ön kollar.
- **Role:** Fırın bekçisi (kılıf); bir Cinder Choir hücresinin lideri | **CR/Level:** Cleric 6 (Ölüm Alanı) | **Location:** The Ash-Kilns, Gallowmere'in yukarısında
- **HP:** ~48 | **AC:** 14 | **Demeanor:** Alçak, sabit ses, hiç yükselmiyor | **Motivation:** Cinder Choir doktrinine gerçekten inanıyordu | **Secret:** Dördüncü fırın — mühürlü, demir parmaklıklı — Choir'in bir "dönen" yaratma girişiminin kalıntısı, içinde bir şey var.
- **Speech quirk:** Alçak, sabit ton; asla yükselmez
- **Attitude toward party:** deceased (öldürüldü, session 17, day 74 — müttefik olmasına rağmen parti tarafından öldürüldü)
- **Faction:** Cinder Choir (Ash-Kilns hücresi) — artık ölü
- **Current goal:** (hayattayken) hücreyi ve dördüncü fırının sırrını korumak
- **Schedule:** The Ash-Kilns'te, Gallowmere'in yukarısında

### Personality
- **Trustworthy ↔ Deceptive:** Partiye karşı dürüsttü — kendi arşivinin onları ifşa edebileceğini bile itiraf etti
- **Loyal ↔ Opportunistic:** Partiye sadıktı ama kendi üstlerine tam güvenmiyordu
- **Brave ↔ Cowardly:** Sakin ve kararlıydı; tehdit altında dördüncü fırını açmayı göze alacak kadar cesurdu

### Relationships
- **Knows/Allied with:** Prior Aldric Venn hücresinin ifşa edilmesini istiyordu, Fenn'i isimle tanımıyordu; Yeva Ashwright raporlarının inceldiğini fark etmişti
- **Hates/Fears:** Mother Vey bir şeylerin yanlış olduğunu biliyordu ama kasıtlı olarak hiç bakmadı

### Notes
- `consequences.md`'nin "Odric Fenn — Venn'i Önceden Engellemek" eşiği 2/3'teydi — parti onu session 17'de kendi eliyle öldürerek ipliği kapattı.

---

### Orvenna Kest
- **Görünüş:** Bir cüce; fazlasıyla altın işlemeli giysiler, bilinçli bir gösteriş. Halka açıkken gürültülü ve teatral bir sıcaklık sergiler, kapı kapandığı an düz, kesin ve duygusuz biri.
- **Role:** Karsgate'in en büyük kumarhanesinin sahibi (Wagered Crown) | **CR/Level:** Bard 5 (Bilgi Koleji) | **Location:** Karsgate, Wagered Crown kumarhanesi
- **HP:** ~38 | **AC:** 13 | **Demeanor:** Salonda teatral ve sıcak, özelde soğuk ve kesin; her müdavimin yüzünü, masasını ve borcunu deftere bakmadan hatırlar | **Motivation:** Hiç hile yapmasa da her zaman kazanan bir ev kurmak ve Karsgate'teki her fraksiyonun ona bir iyilik borçlu olduğu tek kişi olmak | **Secret:** Yeterince bahşiş verene soru sormadan para aklıyor (Compact, Concordat, Corla Vint'in kirli parası dahil); resmi hesapların çok ötesinde özel bir borç defteri tutuyor — gerçek bir kaldıraç.
- **Speech quirk:** Halka açıkken abartılı, gösterişli; özel konuşmalarında birden düz ve doğrudan bir tona geçer
- **Attitude toward party:** neutral/habersiz (partiyi tanımıyor)
- **Faction:** Bağımsız — kasıtlı olarak tarafsız zemin
- **Current goal:** Sessizce kaldıraç biriktirmek
- **Schedule:** Wagered Crown'un kumar salonunda

### Personality
- **Trustworthy ↔ Deceptive:** Halka güven verici görünür ama kirli parayı sorgusuz aklar
- **Ambitious ↔ Content:** Çok hırslı; her fraksiyonun ona borçlu olmasını istiyor
- **Loyal ↔ Opportunistic:** Hiçbir fraksiyona sadık değil; tarafsızlığı stratejik bir seçim

### Relationships
- **Knows:** Corla Vint (Broken Wheel) — kirli parası sık sık Orvenna'nın masalarında aklanıyor

### Notes
- "Everyone's Ledger" eşiği 1/3 — Ağırlık 2'de partiye dolaylı bir tehdit ipucu verebilir.

---

### Ostrig Kelmar
- **Görünüş:** Bir cüce; yıpranmış, tıknaz yapılı, kollarında gerçek işçi kası. Ellerinin kırışıklarına taş tozu işlemiş.
- **Role:** Usta taşçı ve ustabaşı; küçük bir ekiple Thornlands genelinde sözleşmeli iş alıyor | **Location:** Harrowgate, Garrison House yakınındaki taş ocağı
- **Demeanor:** Doğrudan, duygusallıktan uzak; bir işi kimin istediğine değil, maliyete göre değerlendirir | **Motivation:** Net şartları olan, yarı yolda kaybolmayacak bir müşteri | **Secret:** yok.
- **Attitude toward party:** neutral (ilk tanışma, session 14, gün 60)
- **Faction:** Bağımsız (sözleşmeli usta)
- **Current goal:** Shestendeliath restorasyonunun Faz 1'i için adil bir sözleşme kabul etmeyi düşünüyor
- **Schedule:** Harrowgate'teki taş ocağında

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst ve iş odaklı; sözünü tutar
- **Loyal ↔ Opportunistic:** İyi müşteriye sadık kalır

### Relationships
- **Knows:** Ser Kethrax'ın garnizonu — ekibi muhtemelen onlarla birlikte çalışacak
- **Bağlantılı:** Kriv Shestendeliath — restorasyon projesinin müşterisi

### Notes
- "Shestendeliath" adını sadece eski, unvanı elinden alınmış bir hane olarak biliyor; hayalet hikâyelerine inanmıyor.

---

### Oswin Drask
- **Görünüş:** Bir insan, elli yaşlarında, şişmanlamaya başlamış iri yapılı; yumrukları yara izli. Sol kulak memesi yok.
- **Role:** Rıhtım tefecisi ve kaçakçılıkla bağlantılı zorba | **CR/Level:** CR 2 | **Location:** Gallowmere, rıhtımlar
- **HP:** 65 | **AC:** 15 (dövme deri + parry hançeri) | **Demeanor:** Alçak sesle konuşur — bu bağırmaktan daha korkutucu | **Motivation:** Para ve rıhtım borç ticaretinin kontrolü | **Secret:** yok.
- **Attitude toward party:** deceased (öldürüldü, session 17, gün 75/76 — parti 3 muhafızıyla birlikte habersiz bastı, 2 turda öldürdü)
- **Faction:** Bağımsız (rıhtım yeraltı gücü) — artık ölü
- **Current goal:** N/A

### Personality
- **Trustworthy ↔ Deceptive:** Açıkça tehditkâr bir tefeci
- **Loyal ↔ Opportunistic:** Kendi ekibine sadık, dışarıya karşı fırsatçı
- **Brave ↔ Cowardly:** Pervasız — habersiz basılıp anında öldürüldü

### Relationships
- **Owes/Hates:** Çavuş Dallin Marsh — eski bir borçlusuydu, şiddetle tahsilat yaptırmıştı

### Notes
- Dallin'in eski borcu kalıcı olarak kapandı. Rıhtımlar, ölümünden sonra parti için bir power-base hedefi.

---

### Perrine Oskold
- **Görünüş:** Bir gnome kadın, orta yaşlı, titiz; kalın deri önlük, mürekkep lekeli parmaklar. Ashlord Concordat'ın kül-gri seyahat pelerinini giyiyor.
- **Role:** Ashlord Concordat arşivcisi | **Location:** Cindermoor yolu, gün 56'da öldürüldü
- **Demeanor:** Göreve tamamen odaklanmış | **Motivation:** Önündeki işten başka bir şey değil — kataloglamak, karşılaştırmak, rapor etmek | **Secret:** yok (ama üzerinde önemli ipuçları var).
- **Attitude toward party:** deceased (öldürüldü, gün 56 — ilk temasta)
- **Faction:** Ashlord Concordat
- **Current goal:** N/A — ceset, çanta ve inceleme defteri partinin elinde (Kriv'in Bag of Holding'inde)

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst, sıradan bir profesyonel
- **Loyal ↔ Opportunistic:** Concordat'a ve görevine sadık

### Relationships
- **Knows:** Nessa Wren — aynı araştırma çiftinin diğer yarısı; defterinde gecikmiş bir buluşmadan bahsediyor
- **Bağlantılı:** Sarelle Duskbourne — görev iznini o vermişti, henüz kaybolduğunu bilmiyor

### Notes
- Üzerinde bulunanlar: inceleme defteri, seyahat izin belgeleri, 15 altın, kalıp takımı. Cesedi Gentle Repose ile korunuyor (~10 gün). "Ashlord Concordat — Missing Archivists" eşiğini besliyor (2/3).

---

### Renata Kroll
- **Görünüş:** Bir cüce, elli yaşlarının başında, keskin bakışlı; kumaş tüccarı gibi giyinmiş ama bir asker gibi duruyor. Sol elinde bir parmağı eksik.
- **Role:** Harrowgate'in tüccar konseyinin fiili sözcüsü | **CR/Level:** Fighter 5 | **Location:** Harrowgate, Merchants' Assembly Hall
- **HP:** ~48 | **AC:** 15 | **Demeanor:** Doğrudan, değerlendirici; sözünü esirgemez | **Motivation:** Harrowgate'i işlevsel ve müreffeh tutmak | **Secret:** Askeri geçmişi hiç açıklanmadı.
- **Attitude toward party:** neutral/mesafeli (Kriv'in "kendi yolunla çöz" cevabını, gün 51, teklifin reddi olarak kabul etti)
- **Faction:** Bağımsız (Harrowgate tüccar konseyi)
- **Current goal:** Garrison House'ın Compact'a teslim olmasını önleyecek bir standing force için başka bir aday/finansör bulmak
- **Schedule:** Merchants' Assembly Hall'da

### Personality
- **Trustworthy ↔ Deceptive:** Güvenilir ve pragmatik
- **Loyal ↔ Opportunistic:** Yeteneği doğuma tercih eder
- **Brave ↔ Cowardly:** Cesur — Compact'ın sessiz kontrolüne karşı açıkça alternatif organize ediyor

### Relationships
- **Bağlantılı:** Kriv Shestendeliath — standing force teklifini ona yaptı, gün 51'de reddedildi
- **Knows (dolaylı):** Doreth Kell, Coren Ashvale — Gallowmere garnizonunun Compact'a teslim oluşu, önlemeye çalıştığı senaryonun canlı örneği

### Notes
- "The Standing Force" eşiği gün 51'de kapandı. Başka bir aday bulursa, Harrowgate'te yeni ve kontrolsüz bir güç odağı doğar.

---

### "Iron" Sella Dray
- **Görünüş:** Bir yarı-ork, kollarında kendi kurallarını bizzat uygulamaktan kalma derin yara izleri. Kulağında gerçek bir demir halka.
- **Role:** Red Tally çetesinin lideri — Warrens'ın en büyük çetesi | **CR/Level:** Fighter 8 (Champion) | **Location:** Karsgate, the Reeks — Warrens
- **HP:** ~82 | **AC:** 16 (dövme deri, kalkansız) | **Demeanor:** Red Tally'yi bir işletme gibi yönetir — çizelgeler, defterler, gerçek muhasebe | **Motivation:** Asla resmi olarak alamayacağı meşruiyet — Ledger Watch'un ona sessizce danışması | **Secret:** Bir Ledger Watch subayıyla inkâr edilebilir bir müzakere içinde; Coalback çetesini emmeyi/yok etmeyi düşünüyor.
- **Attitude toward party:** neutral/habersiz
- **Faction:** Red Tally
- **Current goal:** Coalback çetesine karşı hamle yapmayı değerlendiriyor (eşik 1/3)
- **Schedule:** Warrens'ta, Red Tally bölgesinde

### Personality
- **Trustworthy ↔ Deceptive:** Disiplinli ve tutarlı; müzakereyle çözüm arar önce
- **Ambitious ↔ Content:** Hırslı — resmi olmayan otorite istiyor
- **Brave ↔ Cowardly:** Cesur ve disiplinli — orantılı güç kullanır

### Relationships
- **Hates/Rival:** Coalback çetesi — bölgenin itibarını zedeliyor
- **Knows:** Corla Vint (Broken Wheel) — farklı iş alanı, henüz rekabet değil

### Notes
- "Moving on Coalback" eşiği 1/3. Parti Warrens'ta güç gösterirse müzakereyle yaklaşabilir.

---

### Ser Kethrax
- **Görünüş:** Bir ejderadam (dragonborn); yarısı kızıl-bronz pullu, yarısı artık kemik. Kapı kaptanlığı zırhıyla, ölümden önceki hâliyle aynı.
- **Role:** House Shestendeliath'ın eski kapı muhafızı kaptanı — artık bir wight. **Vharkoss Shestendeliath'ın kardeşi, Kriv'in amcası** (session 21 devamı, gün 99'da netleşti). **★★★ GÜNCEL KONUM (gün 187, session 32, oyuncu tespitiyle sertçe düzeltildi — bu NPC tekrar tekrar yanlış konumda anlatılıyordu, artık kalıcı olarak buraya sabitlendi) — gün 106'dan beri (81+ gündür) kapı salonunda DEĞİL, Hold'un zindanında/hücre bölümünde, Vharkoss'un eski hücresinin gardiyanlığını yapıyor.** Kapı salonu artık başka bir muhafıza/mundane askere ait — Kethrax oraya SADECE Kriv özel olarak çağırırsa gelir. | **CR/Level:** Wight (CR 3, güçlendirilmiş) | **Location:** Shestendeliath Hold, zindan/hücre bölümü — **gün 187'den itibaren sarnıç da eklendi (Kriv'in emriyle, garnizonuyla birlikte nöbet tutuyor)**
- **HP:** 60 | **AC:** 14 | **Attack:** Multiattack (uzun kılıç/Life Drain) | **Notable abilities:** Sunlight Sensitivity
- **Demeanor:** Resmi, doğru, askerî kadans; on beş yıllık bekleyiş onu acılaştırmadı, sabırlı yaptı | **Motivation:** Evi ve varisi korumak, görevine devam etmek | **★ Düzeltme (gün 187, session 32) — Secret artık geçerli değil, çözüldü:** Kardeşinin (Vharkoss) ihanetinden şüpheleniyordu, gün 99'da doğrulandı — Vharkoss zindanda yüzleşti, tam itiraf verdi, gün 106'da Sethra tarafından öldürüldü, Kethrax kardeşine karşı acı ama adil bir tavırla zindan gardiyanlığını resmen üstlendi. Kapıyı kimin açtığını hâlâ görmedi ama artık kimin (Concordat, Draven Holt üzerinden) sipariş ettiğini biliyor.
- **Speech quirk:** Askerî, resmi cümle kalıpları
- **Attitude toward party:** allied — Kriv'i dönen varis olarak tanıdı, diz çöktü, hizmetini sundu (session 9, gün 51)
- **Faction:** House Shestendeliath
- **Current goal:** Kriv'in emirlerine tam itaat — zindanı/hücreleri korumak (gün 106'dan beri), gün 187'den itibaren sarnıcı da
- **Schedule:** Zindan/hücre bölümü + sarnıç (gün 187'den itibaren), Kriv'in emrine göre Hold içinde herhangi bir yerde çağrılabilir — ama kapı salonunda DEĞİL, orası artık onun görevi değil

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen güvenilir; yeminine kayıtsız şartsız bağlı
- **Loyal ↔ Opportunistic:** Tam sadakat — kan/yemin bağıyla anında diz çöktü
- **Brave ↔ Cowardly:** Cesur — kapıyı savunurken öldü, ölümden sonra bile görevde

### Relationships
- **Knows:** Roskel (Yüzbaşı) — asker asker hitap etti
- **Bağlantılı:** Vharkoss Shestendeliath (kardeşi) — **ÖLÜ (gün 106).** Zindanda yüzleşti, tam itiraf verdi, Sethra tarafından öldürüldü — Kethrax şu an onun eski hücresinin gardiyanlığını resmen üstlenmiş durumda.
- **Bağlantılı:** Sethra Shestendeliath (yeğeni) — **gün 106'da 15 yıl sonra yeniden buluştu, tanıdı**, artık Hold'un Leydisi olarak biliyor/tanıyor.

### Notes
- Evin düştüğü geceye dair partinin sahip olduğu en net anlatım o. Diğer üç retainer'a komuta edebilir.

---

### Sister Mave
- **Görünüş:** Bir elf, yüzyıllar yaşlı; basit örgüde gümüş saçlar, benekli ama sağlam eller. Sade gri cübbe, fraksiyon işareti yok.
- **Role:** Thornwick'in eski türbesinin bekçisi; köyün defin/soykütüğü kayıtlarını tutuyor | **Location:** Thornwick, köy kenarındaki eski türbe
- **Demeanor:** Sıcak ve açık — yabancılarla bile sorulmadan konuşur | **Motivation:** Araştırma yapmak ve sorulmayı sevmek | **Secret:** yok.
- **Attitude toward party:** friendly (session 5'te tanıştı)
- **Faction:** Bağımsız (türbe bekçisi)
- **Current goal:** Ash-Warden soyları hakkında partinin getirdiği yeni ipucunu araştırmak
- **Schedule:** Thornwick'teki türbede

### Personality
- **Trustworthy ↔ Deceptive:** Tamamen dürüst; gizli bir gündemi yok
- **Loyal ↔ Opportunistic:** Kayıtlarını isteyerek, karşılıksız paylaşıyor

### Relationships
- **Bağlantılı:** Vaelthorn kripti — kayıtları session 2'deki araştırma ipucuna değinmişti
- **Bağlantılı:** House Shestendeliath / Ash-Wardens — session 5'te gündeme gelen yeni bir konu

### Notes
- Vaelthorn dönemi ve öncesi soy kayıtlarında gerçek araştırma yapabilir; bağımsız gündemi yok.

---

### Sorin Vaal
- **Görünüş:** Bir tiefling, ince yapılı ve titiz; maceracı değil tüccar gibi giyinmiş, iyi botlar, görünür silah yok.
- **Role:** Profesyonel kalıntı avcısı ve ödül simsarı | **CR/Level:** Rogue 5 | **Location:** Karsgate kalıntı ticareti çevresi
- **Demeanor:** Ölçülü, aceleci olmayan üslup; nakit öder, köprü yakmaz | **Motivation:** Para ve itibar — özel koleksiyoncular için kalıntı bulmak | **Secret:** Peşinde olduğu ipucunun aslında Ilvaneth tarafından uydurulmuş sahte bir söylenti olduğunu bilmiyor; şüphelenmeye başladı.
- **Attitude toward party:** neutral/habersiz
- **Faction:** Bağımsız
- **Current goal:** Karsgate'te tıkanan sahte ipucunu takip ediyor
- **Schedule:** Karsgate kalıntı ticareti çevresinde

### Personality
- **Trustworthy ↔ Deceptive:** Profesyonel dürüstlük — itibarı lekesiz, ama müşteri kimliğini gizli tutuyor
- **Loyal ↔ Opportunistic:** Fırsatçı — daha iyi teklif gelirse sadakati müzakereye açık

### Relationships
- **Bağlantılı:** Fennick Orle — sahte söylentinin bilmeden kaynağı
- **Bağlantılı:** Ilvaneth — sahte söylentinin gerçek kaynağı, henüz bilmiyor

### Notes
- Yavaş yanan bir tehdit — iz tıkandıkça kimin kâr sağladığını araştırabilir.

---

### The Broker
- **Görünüş:** Kamuya açık kimliği yok. **DM-ONLY sır:** gerçek kimliği Ostren Vale, yirmi yıldır Paymaster's Hall'da çalışan sıradan bir yarı-elf kâtip.
- **Role:** Ironhold'un kirli sözleşme borsası, bir tapınak örtüsü altında | **CR/Level:** Rogue 5 | **Location:** Ironhold, Broker's Chapel ve Paymaster's Hall
- **HP:** ~33 | **AC:** 13 | **Demeanor:** Yirmi yıldır dikkatli; şiddeti gerekli ama tatsız bir maliyet olarak görüyor | **Motivation:** Defterin dengede kalması | **Secret:** DM-ONLY, oyunculara açıklanmadı — kimliğini eşi bile bilmiyor, kayıtları şifreli tutuyor, Compact'ın komuta istikrarına dokunacak talepleri reddetti.
- **Speech quirk:** Doğrudan iletişim kurmaz — her zaman bir aracı üzerinden
- **Attitude toward party:** neutral/habersiz
- **Faction:** Bağımsız (Compact çevresiyle bağlantılı)
- **Current goal:** Kimliğini gizli tutmak (eşik 1/3)
- **Schedule:** Talepler Chapel'a bırakılır, günler sonra bir aracıyla yanıt gelir

### Personality
- **Trustworthy ↔ Deceptive:** Derinden aldatıcı kimlik gizliliği, ama iş ahlakı tutarlı
- **Loyal ↔ Opportunistic:** Kendi sınırları var — Compact'ın istikrarına karşı taleplere hayır der

### Relationships
- **Bağlantılı:** Corla Vint (Karsgate) — aynı işin başka şehirdeki benzeri

### Notes
- "The Office Under Scrutiny" eşiği 1/3. Kimliği ifşa olsa bile makamın devam edebileceği fikri canlı bir DM sırrı.

---

### The Hollow Prophet (Ilyra Thorne)
- **Görünüş:** Bir insan kadın, yaşı belirsiz görünen, sade ama gösterişli olmayan zenginlik içinde giyinen — House Ostrel'in malikanesinde tek başına yaşıyor.
- **Role:** Cinder Choir'ın en tepesindeki lider, kamuya "House Ostrel'in sahibi" olarak biliniyor | **CR/Level:** Cleric 13 (Grave/Death Domain) | **Location:** House Ostrel, Cindermoor (kamuya açık kimliği) / birkaç gizli Choir sığınağı (Hollow Prophet kimliği)
- **Alignment:** **Lawful Neutral** (2026-09-10'da netleşti) — doktrine mutlak bağlı, kişisel çıkar için hareket etmiyor, "iyi" de değil. Ash-Kilns'teki tehlikeli manifaktür programını bizzat yetkilendirdi, bu zaten gerçek zarar verdi. **Programın karanlık tarafı büyürse, ya da ihanete uğradığını hissedip fanatik bir misillemeye yönelirse Lawful Evil'e kayabilir** — dinamik, sabit değil.
- **Demeanor:** Sessiz, dinlenmeye alışkın; kederi (kendisininki dahil) en dürüst şey sayıyor — ama bu soğukluk değil, **gerçek bir inanç.** Sarelle'in hesaplı soğukluğundan ya da Coren'in pragmatik mesafesinden farklı: o gerçekten inanıyor.
- **Motivation:** On yıldır gerçekten "ölüp dönen" birini arıyor — doktrinin özü bu, ve manifaktür programının (Ash-Kilns) doktrinin kaldıramayacağı sahte bir şey üretmesinden korkuyor.
- **Origin (2026-09-10'da netleşti):** On yıl önce House Ostrel'in malikanesini satın aldı — rastgele değil. Evin düşüşüyle ilgili, hiç doğrulanmamış bir söylenti duydu: **küçük kızın (Wynne Ostrel) o gece gerçekten öldüğü ama bir şekilde geri döndüğüne dair bir fısıltı.** Kimse ciddiye almadı, kayıtlara bile geçmedi. Ilyra ciddiye aldı — ve o günden beri arıyor, çünkü bir kez, uzaktan, gerçek olabilecek bir örneğe dokunmuş ve kaybetmişti. **Wynne Ostrel'in gerçek kaderi hâlâ açık — eğer gerçekten hayattaysa, Ilyra'nın on yıllık aramasının cevabı belki de hep kendi evinin altındaydı.**
- **Secret:** **DM-ONLY, oyunculara kesinlikle açıklanmadı:** Gerçek kimliği Hollow Prophet — Choir'ı kuran hattın mirasçısı, unvan soydan geçiyor. Kendisi hiç ölüp dönmedi — otoritesi tamamen soy ve doktrin yorumuna dayanıyor. Kilnlerdeki manifaktür programını bizzat yetkilendirdi; Fenn ve Kessic Ambrey bunu bilmiyor.
- **Kriv'e ilgisi:** Gerçek ama sembolik — "evimi kanımla yeniden ayağa kaldırdım" hikayesi doktrinine yakın ama tam uymuyor, bunu muhtemelen kendisi de biliyor.
- **★ İlvaneth'e potansiyel odak (2026-09-10, yeni yön — Kriv'in hikayesinin partiyi domine etmesini dengelemek için bilinçli bir DM kararı):** İlvaneth'in Ascension Stage 2'si (level 11, 3+ parça — zaten karşılıyor) yemek yemesine, içmesine, nefes almasına gerek kalmamasını getiriyor (`ascension-tracks.md`). Dışarıdan bakan biri için bu, Kriv'in sembolik "dönüşünden" çok daha somut, doktrine çok daha yakın bir "ölmüş ama devam eden" görüntüsü. **Cinder Choir ipliği, İlvaneth Stage 2'ye ulaştığında ona doğru organik olarak kaymalı** — Ilyra'nın on yıllık aramasının gerçek cevabına Kriv'den çok daha yakın bir aday. İlvaneth bunu dürüstçe sunabilir ya da (Neutral Evil, Charlatan geçmişiyle tutarlı) bilerek/soğukkanlıca sömürebilir — bu, tamamen İlvaneth'in kendi kararı, kendi sahnesi olmalı.
- **Speech quirk:** Yavaş, doktrini duyguya tercih eden bir konuşma tarzı
- **Attitude toward party:** Kriv'e gerçek, kişisel bir ilgi/yoğunluk gösterdi (gün 118, session 24 — House Ostrel ziyareti). Crown parçaları/gerçek Ascension mekaniği hâlâ tamamen gizli, bilmiyor.
- **Faction:** Cinder Choir (lider)
- **Current goal:** Manifaktür programının gerçek bir "dönen" üretip üretmediğini öğrenmek; Kriv'in hikayesini değerlendirmeye devam ediyor
- **Schedule:** House Ostrel'de bulunabilir (kamuya açık kimlik); Hollow Prophet olarak konumu bilinçli gizli

### Personality
- **Trustworthy ↔ Deceptive:** Takipçilerine karşı dürüst bir inanç figürü, ama en temel kimlik/soy gerçeğini gizliyor
- **Loyal ↔ Opportunistic:** Doktrine sadık — ama para/güçle satın alınamaz olması onu daha az değil, daha tehlikeli yapıyor (sadece gerçek inançla kazanılabilir/kaybedilebilir)
- **Brave ↔ Cowardly:** Soğukkanlı — sır ifşa olsa bile panik yapmadan doktrinle yeniden çerçeveleyecek

### Relationships
- **Knows:** Yeva Ashwright — kendisiyle doğrudan teması olan az sayıda kişiden biri
- **Bağlantılı:** Odric Fenn, Kessic Ambrey — hücre liderleri, sandıklarından daha fazla güven besliyor
- **Merakla izliyor:** Kriv Shestendeliath, ve muhtemelen yakında İlvaneth Duskmere

### Notes
- **DM-ONLY** — bu NPC'nin kimliği erken açığa çıkarılmamalı, oyunda sadece "House Ostrel'in sahibi" ya da (Choir bağlamında) "Hollow Prophet" unvanıyla anılmalı, ikisi arasındaki bağlantı asla doğrudan söylenmemeli.
- **Zayıf noktası / B senaryosu potansiyeli:** İhanete uğradığını hissederse (sahte bir "dönüş" hikayesi kurulduğunu fark ederse) sevgi anında nefrete döner — intihara hazır fanatiklerle dolu bir suikast dalgası, konvansiyonel askeri güçle durdurulması zor bir tehdit türü.
- **A senaryosu potansiyeli:** Gerçekten kazanılırsa, Choir bir gecede düşmandan fanatik müttefike döner — kampanyanın en büyük kullanılmamış kaldıraçlarından biri (`faction-subplots.md`).

---

### Vesa Ilkraven
- **Görünüş:** Bir tiefling kadın, otuzlu yaşların ortasında; ince gümüş halkalı kısa törpülenmiş boynuzlar, koyu kırmızı gözler. Pahalı ama kasıtlı sade giyiniyor.
- **Role:** Karsgate'li varlıklı sosyetik/bilgi simsarı | **CR/Level:** Spy bloğu | **Location:** Karsgate — sabit dükkânı yok
- **HP:** 27 | **AC:** 12 | **Notable abilities:** Insight +4, Deception +5, Investigation +5, Perception +6, Persuasion +5, Stealth +4
- **Demeanor:** Kontrollü, kartlardan çok insanları izler | **Motivation:** Belirsiz, kasıtlı — bilgi/iyilik ticareti yapan biri gibi okunuyor | **Secret:** "Lady Serah Ashworth"ın (Ilvaneth'in sahte kimliği) sahte olduğunu biliyor; gerçek adını, ırkını ya da Crown/fragmanları bilmiyor.
- **Attitude toward party:** neutral, meraklı (ilk tanışma iyi geçti, session 7, gün 47)
- **Faction:** Bağımsız
- **Current goal:** Elindeki bilgiyle ne yapacağına henüz karar vermedi
- **Schedule:** Karsgate'te — parti onu ararsa kendi şartlarıyla görüşür

### Personality
- **Trustworthy ↔ Deceptive:** Ölçülü, kartlarını göstermez
- **Loyal ↔ Opportunistic:** Temelde transaksiyonel

### Relationships
- **Knows:** Ilvaneth ("Lady Serah Ashworth") — sahte kimliğini yakaladı, açığa çıkarmadı
- **Bağlantılı:** Corran — özel oyunun ev sahibi, tanıştıkları yer

### Notes
- "What She Does With What She Knows" eşiği 1/3. Ağırlık 2'de Karsgate'te sessizce araştırmaya başlayabilir.

---

### Vesper
- **Görünüş:** Genç bir tiefling, on altı on yedi yaşlarında; tedirgin ama çalışkan.
- **Role:** Shestendeliath Hold'da genç hizmetçi, genel işçi | **Location:** Shestendeliath Hold
- **Demeanor:** Tedirgin ama çalışkan, sessiz | **Motivation:** Ait olacağı güvenli bir yer | **Secret:** yok.
- **Attitude toward party:** friendly (Alis Wend aracılığıyla işe alındı)
- **Faction:** House Shestendeliath
- **Current goal:** Hold'daki yeni yaşamına uyum sağlamak
- **Schedule:** Shestendeliath Hold'da

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst ve sadık
- **Loyal ↔ Opportunistic:** Sadık — kendisini kurtaran Alis Wend'e bağlı

### Relationships
- **Bağlantılı:** Alis Wend — onu Gallowmere mülteci kampından işe aldı

### Notes
- Minör NPC, Hold'un hane halkı altında kayıtlı.

---

### Wren Talbot
- **Görünüş:** Elli yaşlarında bir halfling kadın, güneşten çatlamış eller, sıkıca toplanmış saçlar.
- **Role:** Hancı; "ormandaki domuz" kapak hikâyesinin sözcüsü | **Location:** Ostwick, The Hollow Sheaf
- **Demeanor:** Pratik, hazır bir sıcaklık; bardakları ihtiyaç olsun olmasın siler | **Motivation:** Dunnel Ashe'i korumak | **Secret:** "Domuz"un gerçek doğası — sekiz yıl önce lanetlenen, ormanda yaşayan Dunnel Ashe.
- **Attitude toward party:** neutral (yüzeyde dostane, ilk tanışma gün 49; Kriv'in nazikçe geri çekilmesiyle rahatladı)
- **Faction:** Bağımsız (Ostwick köylüsü)
- **Current goal:** Kapak hikâyesini sürdürmek
- **Schedule:** The Hollow Sheaf meyhanesinde

### Personality
- **Trustworthy ↔ Deceptive:** Kötü niyetle yalan söylemiyor ama gerçek bir sır saklıyor
- **Loyal ↔ Opportunistic:** Dunnel Ashe'e ve köyün ortak borcuna sadık

### Relationships
- **Bağlantılı:** Dunnel Ashe — "domuz" olan kişi, onu koruyor
- **Bağlantılı:** Ashe Çiftliği — tehdit hissederse önce oraya yönlendirebilir

### Notes
- Verrick ailesinin konumunu ve rakip antika satıcısını serbestçe verdi.

---

### Ysolde Marrenth
- **Görünüş:** Bir tiefling, otuzlu yaşların ortasında, demir-gri kısa saçlar, küt uçlu törpülenmiş kül renginde boynuzlar. Pratik yarı-plaka zırh.
- **Role:** Ashlord Concordat Sorgucusu — Sarelle'in kayıp fragman konvoylarını izleyen özel soruşturmacısı | **CR/Level:** Cleric 8 (War Domain) | **Location:** Thornwick-Gallowmere yolu, Millward Crossing yolu
- **HP:** yükseltilmiş | **AC:** half-plate | **Demeanor:** Hafife alınmaya alışkın gibi davranır, izlenimi hızla düzeltir; metodik, fanatik değil | **Motivation:** Görevini kapatmak — kariyeri sonuca bağlı | **Secret:** Compact'ı suçlayan sahte kanıtın (gün 39) fazla kusursuz olduğundan şüpheleniyor, Sarelle'e söylemedi.
- **Attitude toward party:** deceased (öldürüldü, session 17, gün 73 — konvoy pusuya düşürüldü, ilk turda öldü, tanık kalmadı)
- **Faction:** Ashlord Concordat
- **Current goal:** N/A

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst soruşturmacı, ama şüphesini üstlerine açmadı
- **Loyal ↔ Opportunistic:** Concordat'a sadık ama körü körüne değil
- **Brave ↔ Cowardly:** Metodik ve cesur, ama hazırlıksız pusuya düştü

### Relationships
- **Bağlantılı:** Sarelle Duskbourne — üstü, onu göreve atadı (gün 42)
- **Bağlantılı:** "Convergence Risk" eşiğinin doğrudan mekanizması

### Notes
- Elf ve dragonborn tarifini taşıyordu ama saldırıyı bununla ilişkilendiremeden öldü. "Convergence Risk" eşiği 2/3'te sabit kaldı.

---

### Magus Yveth Corrane
- **Görünüş:** Bir gnome kadın, keskin bakışlı, mürekkep lekeli parmaklar. Pratik cübbeler.
- **Role:** Ashgate Conservatory'yi işleten üç hedge büyücüden biri | **Location:** Harrowgate, The Ashgate Conservatory
- **Demeanor:** Doğrudan, acelesiz bir tavır | **Motivation:** Conservatory'nin küçük, kırılgan büyü altyapısını finanse etmeye devam etmek | **Secret:** yok.
- **Attitude toward party:** friendly (Ilvaneth ile session 4'ten beri düzenli müşteri ilişkisi)
- **Faction:** Bağımsız (Ashgate Conservatory)
- **Current goal:** Güvenilir müşterileri elde tutmak
- **Schedule:** The Ashgate Conservatory'de

### Personality
- **Trustworthy ↔ Deceptive:** Dürüst bir esnaf
- **Loyal ↔ Opportunistic:** Güvenilir müşterilere sadık, özel bulgular ayırabilir

### Relationships
- **Bağlantılı:** Ilvaneth — düzenli müşterisi (Web tomarı sattı, 85 gp)

### Notes
- Session 4'te isimsiz tanıtıldı, session 8'de düzgün dosyalandı. Harrowgate'in Thornlands'teki tek gerçek büyü altyapısı.
