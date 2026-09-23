# Session Log — Ashen Crown

*Bu kampanya, 2026-09-06'da başka bir repo/araçtan (`C:/Users/armag/Desktop/Ashen-Crown_New_DM/original-repo/`) bu yapıya taşındı — 19 oturumluk tam geçmiş orijinal repo'da (`party/session-log.md`, 54KB) korunuyor, burada tekrarlanmadı. Bundan sonraki oturumlar burada, bu formatta kaydedilecek. Sadece son 2 tam oturum burada tutulur — daha eskisi `session-log-archive.md`'ye taşınır, 3-5 maddelik özeti `state.md → ## Continuity Archive`'da kalır.*

---

## Session 36 — 2026-09-22 — Ember Court dungeon crawl (Oda 3-11), Ascension Stage 4, gün 203
**Location:** The Ember Court (Kaal hanesinin sınır düzlemi) — Oda 3-11  **In-world date:** Gün 203 (zaman düzlemde esnek)  **Duration:** —

### Recap
**Yükleme düzeltmesi.** Önceki save Ember Court'un 24 odasını hiç oynanmamış atlayıp "Iskra/Sathriel kalıcı öldü, eve dönüldü, uzun mola bitti" diye kaydetmişti. Oyuncu bunu ilk mesajında yakaladı — gerçek durum (sadece Oda 1-2 oynanmış, geri kalanı henüz oynanmamış) düzeltildi, Iskra/Sathriel'in "kalıcı öldü" kaydı "ağır yaralı, Oda 24'te reform halinde" olarak geri alındı (graph.json ve goals.json dahil).

**Ascension Stage 4.** Level 17 + 8/9 fragman eşiği session 35 sonunda zaten sağlanmıştı ama hiç işlenmemişti — oyuncunun sorusuyla yakalanıp hemen uygulandı. Kriv: gerçek kanatlar (Warden's Oathplate'i yararak çıktı, 60ft uçuş), 9d6 nefes/40ft koni, Truesight 60ft, Legendary Resistance 1/gün, + kanatlar açıkken Intimidation/Persuasion'da durumsal avantaj (oyuncu mantığıyla canlı onaylandı). İlvaneth: necrotic/poison/disease/exhaustion tam bağışıklık, sıradan yollarla kalıcı öldürülemiyor (24 saatte reform), undead'i isteğe bağlı komuta — bedel artık özellikle yetimhane anılarını hedefliyor.

**Oda 3-11 sırayla temizlendi.** Ledger Salonu (9× Lemure, Kriv GWM zinciriyle 4'ünü, İlvaneth Fire Bolt'la 1'ini, kalan 4'ü ikinci GWM turuyla bitirdi). Baş Yazmanın Odası (özel güçlendirilmiş Spinagon, CR¼→8). Sözleşme Kasası (Bone Devil + gerçek loot: master Kaal borç kayıtları + kırık Sözleşme Taşı parçaları, Bag of Holding'e kondu — Toll the Dead ile öldürüldü). Kor Köprüsü Karakolu (4× Barghest, İlvaneth'in Sickening Radiance'ı + Kriv'in GWM'i tek turda hepsini bitirdi, parti hiç hasar almadı). Borçlular Galerisi'nde bağlı bir ruhla (Kriv Persuasion 26) savaşsız bilgi alışverişi — ileride Besleme Salonu/Yargı Çukuru/Kor Tahtı tehditleri + Sözleşme Taşı'nın tamamının muhtemelen Tahtı tutanda olduğu öğrenildi. Besleme Salonu (2× Erinyes CR12 — Kriv'in Action Surge'lü Disarming/Goading Attack zinciri + İlvaneth'in Vampiric Touch'ı ikisini de düşürdü, İlvaneth 20 piercing hasar aldı ama zehir Stage 4 bağışıklığıyla etkisizdi). Ceza Hücreleri (kıdemli Bone Devil, CR9→12 — İlvaneth'in Protection from Evil and Good'u Kriv'e fiend direnci verdi, fire immunity ilk kez doğru uygulandı). Gözetmenin Odası (kıdemli Rakshasa Yönetici — Suggestion'ı Kriv'in WIS save'iyle savuşturuldu, tek turda öldürüldü). Yargı Çukuru (Rakshasa Şampiyonu — stok stat, oyuncu "champion" adına yakışmadığını belirtti, gelecekte gerçek güçlendirme istendi).

**Rakshasa'ların Limited Magic Immunity'si ilk kez karşılaşıldı** — İlvaneth'in 6. seviye ve altı büyüleri (Fire Bolt, Toll the Dead, Vampiric Touch, Sickening Radiance dahil) rakshasa'lara karşı işe yaramıyor, sadece 7.+ seviye büyüler ya da fiziksel saldırılar geçerli. İlvaneth bunu tanıyıp Kriv'i uyardı, kendi rolünü büyüden fiziksel desteğe (Protection from Evil and Good gibi hedefi rakshasa olmayan büyüler) kaydırdı.

**Oda 12'nin eşiğinde durduruldu** (3× Rakshasa askeri bekliyor) — oyuncu `/dm:dnd save` çağırdı.

### Key Events
- **Kayıt hatası düzeltildi:** Iskra Vantrel ve Sathriel kalıcı ölmedi, Ember Court Oda 24'te reform halindeler — Whisper Court goal tracker PERMANENT_LOSS'tan THREATENED'a geri alındı.
- **Ascension Stage 4 işlendi (her ikisi de)** — bkz. yukarı.
- **Ember Court Oda 1-11 tamamen temizlendi**, parti Oda 12'nin eşiğinde.
- **Master Kaal borç kayıtları + kırık Sözleşme Taşı parçaları ele geçirildi** (Oda 5).
- **Yapısal DM süreç düzeltmeleri (SKILL-combat.md'ye genel kural olarak işlendi):** (1) bir PC'nin pasif özelliği (Cloak of Displacement) sadece basılmakla kalmayıp fiilen her NPC saldırısında uygulanmalı; (2) canavar direnç/bağışıklıkları her hasar hesabında kontrol edilmeli, `lookup.py`'nin veri eksikliği "direnç yok" anlamına gelmiyor (devil fire/poison immunity örneği, hem Oda 8 hem Oda 9'da yaşandı, Oda 9'dan itibaren düzeltildi); (3) PC save'leri hep oyuncudan gelir, DM bir kez ihlal edip düzeltti.
- XP: Oda 3 (Lemure) 45 + Oda 4 (Spinagon) 1.950 + Oda 5 (Bone Devil) 2.500 + Oda 6 (Barghest×4) 2.200 + Oda 8 (Erinyes×2) 8.400 + Oda 9 (Bone Devil kıdemli) 4.200 + Oda 10 (Rakshasa yönetici) 5.000 + Oda 11 (Rakshasa şampiyon) 5.000 = **+29.295/kişi.** İkisi de **261.257 XP, Level 17** (Level 18 eşiğine 3.743 kaldı).

### DM Calibration
**Oyuncunun cevabı (2026-09-22, `/dm:dnd end`):** *"Bu oturumda Opus yardımı ile majör değişiklik ve geliştirmeler yapıldı."* — oturumun ağırlık merkezi masadaki oyun kadar skill'in kendisiydi: AIGM refactor dalında faction forward-model'i (`factions.py`), dakika hassasiyetli takvim + düzlem oranları (`calendar.py`), encounter-design doktrininin skill'e taşınması, zar sahipliğini dışarıdan zorlayan hook, ve display/telefon sisteminin tamamen sökülmesi. Genel DM kuralları `DM Style Notes`'tan skill'in kendisine taşındı — kampanya dosyaları artık olguları, skill kuralları taşıyor.

Oturum içi düzeltmeler de yoğundu: kayıt/devamlılık hatası (dungeon atlama), gözden kaçan bir mekanik kazanım (Ascension Stage 4), ve tekrar eden combat-hatası kalıpları (pasif efekt uygulama, canavar direnci) hepsi canlı yakalanıp kalıcı olarak (hem bu kampanyaya hem skill'in genel SKILL-combat.md'sine) işlendi.

**Kapanışta düzeltilen kayıt (oyuncu kararı):** gün sayacı kanonik — **gün 203 = 37 Ashfall = Cinderday.** Kesh Amara toplantısının eski "Restday" etiketi yanlıştı; örüntü Cinderday geceleri olarak düzeltildi (state.md, session-log.md, npcs.md). Sarelle'in Ashvale'deki Restday zayıflığı ayrı ve doğru bir olgu, değiştirilmedi.

### Session Recap
**Öne çıkanlar:** Bir önceki oturumun kayıt hatası düzeltildi (Iskra/Sathriel yaşıyor, dungeon gerçekten oynandı); her iki karakter de Ascension Stage 4'e ulaştı (Kriv gerçek kanatlar kazandı); Ember Court'un 11 odası temizlendi, Oda 12'nin eşiğinde durdu; birden fazla yapısal DM süreç hatası (pasif efekt uygulama, canavar direnci, PC zar sahipliği) yakalanıp skill seviyesinde kalıcı olarak düzeltildi.

**Açık iplikler (bir sonraki oturuma taşınan):**
- **Ember Court'ta 13 oda daha var** (Oda 12-24) — asıl hedef hâlâ Oda 24'teki Kor Beşiği, saat işliyor.
- **Oda 12'de 3× Rakshasa askeri bekliyor** — henüz girilmedi.
- **Rakshasa'ların Limited Magic Immunity'si** — İlvaneth'in taktik repertuarını Oda 24'e kadar etkileyecek, 7.+ seviye büyülere (Teleport, Power Word Pain/Stun, Meteor Swarm, Wish) yönelmesi gerekebilir.
- **Kor Beşiği'nin reform saati** — ne kadar süre kaldığı hâlâ belirsiz, "birkaç saat" diye tasarlandı.
- **Son Crown parçası (9/9)** — Ser Oskar Thrune, Bonewrights' Hall — hâlâ gidilmedi, Ember Court'un dışında.

---

## Session 37 — 2026-09-23 — Ember Court tamamlandı (Oda 12-24), İskra/Sathriel kalıcı öldü, Level 18, gün 204-205
**Location:** The Ember Court (Oda 12-24) → Emberhold (Sonnward Promenade konağı)  **In-world date:** Gün 204-205  **Duration:** —

### Recap
**Oda 12-23 tek oturumda, rest almadan temizlendi.** Oda 12 (3× Rakshasa Asker, Kriv'in GWM nova'sı üç round'da hepsini bitirdi, Protection from Evil and Good Kriv'i korudu). Oda 13 (2× Bearded Devil, sürpriz saldırı + Kriv'in GWM'i ikisini de tek turda bitirdi). **Vezra (Erinyes, Oda 15)** ile savaşsız müzakere — bilgi verdi: Sözleşme Taşı onarılırsa İskra/Sathriel'in sözleşmesi iptal edilip reform durdurulabilir. Oda 16'nın sözleşme-hukuku bilmecesi doğru cevaplanıp savaşsız geçildi. Oda 17 (haberci Ossian) sessizce geçildi. Oda 18'in (Eski Borçlar Hazinesi) lanet-tuzağı İlvaneth'in Investigation'ıyla tam çözüldü, hazineye dokunulmadı (bedel riski). Oda 20 (7× Lemure + özel Spinagon, CR8) — Kriv'in GWM zinciri + İlvaneth'in Toll the Dead'i temizledi. Oda 23 (2× Bone Devil Kıdemli, CR12) — uzun, gerçek bir dövüş: Kriv Trip Attack ile birini deviripprone yaptı, İlvaneth'in Toll the Dead'leri ikisini de bitirdi.

**★★★★★★★★ ODA 24 — FİNAL BOSS. Rakshasa Rajah (özel/benzersiz, CR19) + Pit Fiend (CR20 stok).** Kriv'in açılış turunda Pit Fiend'in mace'ini Disarming Attack ile düşürdü. Action Surge nova'sıyla Pit Fiend'i tek başına bitirdi. Rajah'ın Dominate Person'ı iki kez başarısız oldu (Kriv+İlvaneth ikisi de WIS save'i geçti). Kriv, Rajah'ın çift pençe saldırısıyla **4 HP'ye kadar düştü** — İlvaneth, Wish'in güvenli/bedelsiz etkisiyle ("20 yaratığa tam HP + Greater Restoration") onu anında tam iyileştirdi. Rajah, Trip Attack ile prone edilip Kriv'in nova'sı + İlvaneth'in Draconic Transformation nefesiyle bitirildi. **İskra Vantrel ve Sathriel, Kor Beşiği'nde savunmasız halde bulundu ve Kriv tarafından kılıçla infaz edildi — bu kez kalıcı ve geri dönüşsüz.** Whisper Court'un otuz yıllık operasyonu sona erdi (`factions.py react` ile House Ilvane/Corr/Sablewood gün 210-211'de öğrenecek). Efreeti Bottle ilk kez açıldı (d100: 51, 1 saat hizmet) — savaşta yardım etti, sonra şişeye geri döndü (2 kullanım hakkı kaldı, 24 saat kilitli).

**Oda 18'e dönüş.** Rajah öldüğü için lanet-sözleşmesinin imza yetkisi de öldü (İlvaneth'in Arcana 25 ile doğrulandı) — hazine artık güvenli. Toplam +55.000 gp (ana yığın + gizli bölme) + kendini güncelleyen borç defteri + hapsedilmiş bir kül-ruhu alındı; defterde 15 yıllık, artık geçersiz bir "House Shestendeliath" kaydı bulundu.

**Teleport ile Emberhold'a dönüş, long rest.** Düzlemde 8s15dk geçti (x2 oranla dışarıda 16.5 saat) — gün 204 öğleden sonra → gün 205 sabah. **Level 18'e geçildi (ikisi de)** — Kriv: Superiority Dice artık d12, +9 HP. İlvaneth: Spell Mastery (Mage Armor+Invisibility slotsuz), 5. seviye slot 3'e çıktı, +2 yeni büyü (Control Weather, Foresight), +7 HP. **İlvaneth'in 20. Ascension rüyası:** İskra'nın kendi hatırası — Whisper Court'un gerçek tepesi İskra değilmiş, bilinmeyen bir üst-otorite ("Marek Vantrel" adı/unvanı) hâlâ bir yerde. **Oyuncu talebiyle Oda 24'ün XP'si (+23.500/kişi) eklenmedi** — loot yeterli ödül sayıldı.

### Key Events
- **★★★★★★★★ Dungeon tamamen temizlendi (24/24 oda).**
- **İskra Vantrel ve Sathriel kalıcı olarak öldü** — Whisper Court liderliksiz, Goal Tracker PERMANENT_LOSS.
- **Rakshasa Rajah + Pit Fiend yenildi** — kampanyanın en ağır dövüşü, Kriv 4 HP'ye kadar düştü, Wish ile kurtuldu.
- **Loot:** Kaal'ın Zulüm Bıçakları (Legendary), Boyun Eğmeyenin Tacı (Very Rare), İblis Topuzu (Legendary), Kaal Muhafızının Bileziği, Sözleşme Taşı'nın son parçaları, ~116.000 gp toplam (Oda 24 + Oda 18).
- **Level 18'e geçildi (ikisi de).**
- **Yeni açık iplik (DM-only, Ascension rüyası):** Whisper Court'un gerçek üst-otoritesi hâlâ bilinmiyor — "Marek Vantrel."
- **Efreeti Bottle ilk kez kullanıldı** — 2 kullanım hakkı kaldı.
- XP: Oda 12 (8.850) + Oda 13 (700) + Oda 14 (3.450) + Oda 20 (1.985) + Oda 23 (8.400) = **+23.385/kişi** (Oda 24'ün +23.500'ü oyuncu talebiyle atlandı). İkisi de **284.642 XP, Level 18.**

### DM Calibration
Oturum boyunca birkaç canlı düzeltme yapıldı: (1) inisiyatif hesabında bir kez çift modifikatör hatası (oyuncu yakaladı, anında düzeltildi, sıralama değişmedi). (2) Bir PC'nin turu yanlışlıkla atlandı (round 3, İlvaneth) — fark edilip geriye dönük telafi edildi. (3) Devil'lerin "saldırıları büyülü" varsayımı bir ara rakshasa/spinagon'a da genellendi, oyuncu sorunca stat block kontrol edildi — sadece stat block'ta açıkça yazan yaratıklar (Pit Fiend, Erinyes) büyülü sayılmalı, varsayılmamalı. (4) Magic Resistance'ın (büyülere karşı avantaj) bir maneuver'a (Trip Attack, büyüsel değil) yanlışlıkla uygulandığı bir an oldu, düzeltildi. (5) Bir spell'in (Ice Storm) concentration gerektirmediği ilk yanlış kaydedildi, `lookup.py` ile kontrol edilip düzeltildi.

### Session Recap
**Öne çıkanlar:** Ember Court'un 24 odası tek oturumda (session 36-37 birleşik) tamamen temizlendi; İskra Vantrel ve Sathriel kalıcı olarak öldü, Whisper Court'un otuz yıllık operasyonu sona erdi; final boss (Rakshasa Rajah + Pit Fiend) yenildi, Kriv 4 HP'ye kadar düşüp Wish ile kurtuldu; Level 18'e ulaşıldı; büyük bir loot haulu (~116.000 gp + birden fazla Legendary eşya) alındı; Whisper Court'un gerçek üst-otoritesinin hâlâ bilinmediğine dair yeni bir DM-only iplik açıldı.

**Açık iplikler (bir sonraki oturuma taşınan):**
- **"Marek Vantrel"** — Whisper Court'un gerçek üst-otoritesi, DM-only, oyunculara henüz açıklanmadı.
- **Son Crown parçası (9/9)** — Ser Oskar Thrune, Bonewrights' Hall — hâlâ gidilmedi.
- **Sözleşme Taşı'nın son parçaları** — artık onarılabilir durumda ama henüz onarılmadı, gelecekte bir kullanımı olabilir.
- **Hapsedilmiş kül-ruhu** — İlvaneth yanında taşıyor, kaderi henüz kararlaştırılmadı.
- **Kendini güncelleyen borç defteri** — Kaal'a borçlu ölümlü ailelerin kaydı, gerçek bir siyasi kaldıraç, henüz kullanılmadı.
- **Üç hanenin (Corr/Sablewood/Ilvane) Whisper Court'un gerçek doğasını (rakshasa+doppelganger) öğrenmesi** — gün 210-211'de gerçekleşecek, parti henüz bilgilendirmedi.
