# Combat Difficulty Doctrine — Ashen Crown

*Yazıldı 2026-09-10, session 25 devamı. **v2 — 2026-09-17, session 31 sonrası, oyuncunun kendi kök-neden analiziyle revize edildi** (bkz. altta "v2 revizyonu" bölümü — Kule-i Mensuh'ta bile bir "boss-tier" düşman (Legendary Resistance + Actions'lı, HP190) sadece 2 round'da düştü). Kök sebep düşman sayısı/CR değil — mekanik unsurların üst üste binmesi. Bu dosya, her yeni encounter kurulurken (ya da rastgele bir encounter'ı gerçek bir sahneye çevirirken) kontrol edilecek somut bir checklist.*

## ★ v2 revizyonu (2026-09-17, session 31 sonrası) — ZORUNLU, her boss/önemli encounter'da

Oyuncunun kendi teşhisi: v1'in Legendary Resistance/Actions eklemesi işe yaramadı çünkü **asıl sorun "control nova" değil "damage nova."** LR sadece save-or-suck büyülere karşı işliyor, ham hasara (GWM+manevra zinciri, Wizard'ın hasar büyüleri) hiçbir şey yapmıyor. Altı maddelik yeni, ZORUNLU kontrol listesi — her boss/mini-boss/önemli set-piece için hepsi uygulanır (v1'in "uygulama seviyeleri" tablosu hâlâ geçerli ama bu altı madde boss-tier için opsiyonel değil):

1. **HP hesabı artık round-1 alfa değil, çok-roundlu.** `burst_check.py`'nin round-1 rakamını taban alma — **round-1 burst + 2×ortalama sürdürülebilir round DPR** formülünü kullan. Boss'un gerçekten 3+ round hayatta kalması hedef.
2. **Direnç/bağışıklık artık "ara sıra" değil, her boss'un varsayılan tasarım katmanı.** Her boss'a narratif olarak haklı bir direnç/zayıflık profili ver (örn. fiziksel dirençli+force'a zayıf zırhlı dehşet; necrotic dirençli+radiant'a zayıf undead). Hem nova'yı gerçekten yarılar hem partiye "doğru silahı bul" taktik katmanı katar.
3. **Terrain/pozisyon koruması — yeni, şu ana kadar hiç yoktu.** Önemli boss'larda en az biri: (a) bir koşul sağlanana kadar hedef alınamaz (bir ward/kalkan kırılmalı), (b) hareket/görüşü engelleyen fiziksel engeller, ya da (c) boss'ta bir mobilite aracı (teleport/uçuş/faz değişimi) — her round aynı mesafede durup tam nova yemesin.
4. **Boss öncesi kaynak tüketimi — tutarlı, her seferinde.** Parti boss odasına her zaman %100 kaynakla (tüm slotlar, Action Surge hazır) giriyorsa HP ne olursa olsun sorun tekrarlanır. Her boss encounter'ından hemen önce en az bir gerçek kaynak-tüketen engel/tuzak/mini-fight zorunlu.
5. **Destek yaratıklar gerçek HP/AC taşımalı, tek vuruşluk mook olmamalı.** GWM'nin "kill/crit → bonus action" zinciri zayıf mook'ları es geçip partiye boss'a kadar zincirleme saldırı hakkı veriyor — boss'u koruyan yaratıklar tek vuruşta düşmemeli.
6. **Terrain/direnç/kaynak-tüketimi/destek-yaratık dörtlüsü + v1'in Legendary Resistance/Actions'ı birlikte, standart bir kontrol listesi gibi.** Biri diğerinin yerine geçmez — hepsi aynı anda, her boss-tier encounter'da.

## ★ v3 revizyonu (2026-09-17, aynı gün, session 31) — Düşman itemizasyonu, ZORUNLU

Oyuncunun teşhisi: parti 30 session boyunca biriktirdiği tam attunement'lı, optimize item setiyle savaşıyor (3/3 slot dolu, Wardensteel gibi slot-dışı eşyalar), ama karşılaştıkları NPC/boss'lar düz stat block — sıfır item. CR/encounter matematiği "standart" (item'sız) bir parti varsayıyor, bu da nova sorununu daha da büyütüyor. **Her önemli NPC/boss artık kendi item ekonomisiyle tasarlanmalı:**

1. **İmza silah** — boss'un partiye verdiği hasarı da güçlendiren, gerçek bir tehdit hissi yaratan büyülü bir silah (Wardensteel'in düşman versiyonu gibi düşün).
2. **Direnç/güç item'ı** — v2'nin #2 maddesindeki (tematik direnç/zayıflık profili) bu boss'a özel bir eşya (kolye, pelerin, çekirdek vb.) üzerinden taşınır — soyut bir stat satırı değil, somut bir nesne.
3. **Ekstra mekanik yok.** Bu item'lar savaş boyunca normal şekilde işler, "kırma/sökme" gibi ayrı bir alt-sistem gerekmez — boss ölünce item'lar doğal olarak standart loot'a döner, gücü de onunla birlikte söner.
4. **Kendi kendini besleyen ödül döngüsü.** Zor bir boss'u yenen parti onun imza item'ını kazanır, güçlenir — bir sonraki boss buna göre (kendi item ekonomisiyle) tasarlanmalı. Parti güçlendikçe düşman da güçlenmeli, sabit kalmamalı.
5. **Destek yaratıklar ayrı bir ekonomi.** Mekanik olarak ağır olmalılar (gerçek HP/AC — GWM'nin kill/crit-zinciriyle partinin onları geçip doğrudan boss'a ulaşmasını engellemek için, v2 madde #5 ile aynı), AMA **hiçbir loot bırakmazlar.** Sadece boss'un kendi imza item'ları (madde 1-2) gerçek ödüldür — destek yaratıklar sadece action-economy/dayanıklılık katmanı, item ekonomisinin parçası değil.

Bu, v1+v2'nin üstüne eklenen üçüncü katman — hepsi birlikte, her boss-tier encounter'da standart.

---

## Teşhis — neden kolay geliyor

1. **Sürpriz neredeyse her zaman elde ediliyor** (gözlem + gizlilik + kılık değiştirme rutini iyi çalışıyor).
2. **Kriv'in tek-tur alfa saldırısı** (Extra Attack + GWM + bonus action) tek round'da 60-130 hasar basabiliyor (bkz. karakter sayfasının Burst Reference tablosu).
3. **İlvaneth'in Cloak of Displacement'ı** gelen attack-roll saldırılarını büyük ölçüde etkisiz kılıyor.

Üçü birlikte: düşman sayısı/CR ne olursa olsun, fight round 1-2'de biter, PC'ler neredeyse hiç hasar almaz.

## Her encounter kurulurken kontrol edilecek 6 madde

### 1. Farkındalık durumu — sürpriz her zaman garanti değil
Varsayılan artık **"parti bu kadar ün yaptıysa, akıllı düşmanlar hazırlıklı olur."** Bir encounter kurarken sor: bu düşman/lokasyon, partinin tekrarlayan taktiğine (gizli yaklaşım, disguise, gece baskını) karşı gerçekçi olarak tedbirli mi? Eğer öyleyse: gerçek nöbetçi rotasyonu, büyülü alarm, ya da en azından bir kısmının sürpriz DIŞI kalması (mixed surprise, session 25'in Onur Muhafızları odasındaki gibi — Kriv'in stealth'i başarısız oldu, Wight uyanık kaldı).

### 2. Bir "çapa" düşman — tek turda öldürülemeyen
Her gerçek (rastgele olmayan) encounter'da en az bir kombatan, partinin **gerçekçi bir alfa saldırısını** (burst_check.py'nin raporladığı rakam, GWM dahil ama Action Surge hariç normal bir round için) yiyip hâlâ ayakta kalacak kadar dayanıklı olmalı — yüksek HP, yüksek AC, ya da direnç/bağışıklık kombinasyonuyla. Amaç: en az bir düşmanın round 2'de gerçekten hareket etmesi.

### 3. Attack-roll'a bağlı olmayan taktikler — Cloak of Displacement'ı atlar
Cloak of Displacement **sadece attack roll'lara dezavantaj verir** — bu bir kural boşluğu değil, zaten kuralın kendisi. Düşman listesine ara sıra ekle:
- **Save-bazlı AoE büyüler** (Fireball, Cone of Cold, Stinking Cloud vb.) — cloak'u tamamen atlar.
- **Grapple/Restrain/Silence** gibi attack-roll içermeyen etkiler.
- Bunları kullanan en az bir spellcaster/özel yetenekli düşman, özellikle İlvaneth'i hedefleyen encounterlarda.

### 4. Hasar tipi direnci/bağışıklığı — ara sıra, tematik olarak
Kriv'in Barrow-King's Blade'i undead'e karşı ekstra güçlü (+1d8 radyan); İlvaneth'in birincil hasarları ateş/nekrotik. Ara sıra (her fight değil, ama düzenli aralıklarla, tematik olarak haklı çıkarılabildiğinde): construct, belirli fiend/celestial türleri, ya da özel bir büyüyle korunmuş düşmanlar bu hasar tiplerine dirençli/bağışık olsun — alfa saldırının matematiğini gerçekten bozar.

### 5. Boss-tier fightlerde Legendary Resistance / Legendary Actions
Baron Halvern Doskarn emsali (`burst_check.py` ile HP ayarlandı, Legendary Resistance 2/gün eklendi) — **her gerçek boss/mini-boss için standart.** "Sırası olmayan" bir anda hareket edebilme (Legendary Actions) ve başarısız bir save'i bir kez reddetme (Legendary Resistance), tek-round-temizleme sorununu kökten çözer.

### 6. Çok dalgalı encounterlar
Önemli fightlerde, ilk sürpriz/alfa saldırısı harcandıktan hemen sonra (gürültü, alarm, zamanlanmış devriye) **ikinci bir dalga** gelsin. Sürpriz avantajı sadece ilk dalgada işler — parti artık slot/bonus action harcamış, ikinci dalga gerçek bir mücadele olur.

## Uygulama seviyeleri — her fight aynı ağırlıkta olmasın

| Encounter türü | Uygulanacak maddeler |
|---|---|
| Rastgele/doku (travel table, küçük tehdit) | Genelde hiçbiri — bunlar zaten hafif olmalı |
| Standart dungeon odası | 1-2 madde (genelde #1 ve/veya #2) |
| Önemli set-piece (bir ipliğin gerçek fightı) | 3-4 madde |
| Faction lideri / boss-tier yüzleşme | Hepsi, VE yukarıdaki v2 revizyonunun 6 maddesi ZORUNLU (opsiyonel değil) |

## Not
Bu bir "oyuncuyu cezalandırma" listesi değil — amaç sürpriz + alfa saldırı stratejisini *bazen* gerçekten test etmek, her zaman değil. Parti hâlâ akıllı oynarsa (gerçek keşif, doğru hedef seçimi) ödüllendirilmeli; bu doktrin sadece "her zaman otomatik kazanma" hissini kırmak için.

---

## Ek İlke — Eski Dungeonların Yeniden İşgali

*2026-09-10, session 25 devamı — "dungeon kalmadı" hissine ve "art arda combat/hazine" isteğine karşı ikinci bir cevap, Combat Difficulty Doctrine'i tamamlıyor.*

Zaten temizlenmiş dungeonlar kalıcı olarak boş kalmak zorunda değil. Yeni bir işgalci, aktif bir iplikten seçilirse (rastgele değil), hem "neden şimdi burada" sorusunu cevaplar hem de 12 maddelik öncelik listesine somut bir sahne kazandırır. **Ödül sorunu görünürden küçük** — yeni işgalci kendi hazinesini getirir (aynı loot tekrarlanmaz), ve zaten birçok dungeon %100 keşfedilmedi (Karsgate Undercity'nin Carrion Tangle/Bone Market/Flooded Archive gibi hiç girilmemiş odaları).

**Somut eşleşmeler (hazır, kullanılabilir):**
- **The Debased Mint'in kalıntıları** — Concordat, Sarelle'in Ashvale kaybı sonrası kaynak arayışıyla ya da kayıp bir tarama biriminin izini sürerken House Doskarn'ın harabesine yeniden el atabilir.
- **Ash-Kilns'in derin fırını** — Cinder Choir'ın manifaktür programı taşıp eski, temizlenmiş alanlara sızmış olabilir.
- **Karsgate Undercity'nin temizlenmiş kısımları** — Red Tally (Sella Dray) ya da Coalback (Ossa Vahn) genişleme çabasıyla eski wererat/otyugh bölgelerine yerleşmiş olabilir.
- **Kesh Deeps** — yeni bir duergar/goblin dalgası ya da farklı bir tehdit sızmış olabilir.

**★ Teslimat kuralı — bunlar asla zorla/aniden sahneye sokulmaz.** Standard 10 (situations not plots) ve Standard 1'in re-engagement araç setine uygun şekilde, bu reoccupation'lar **her zaman mevcut mekanizmalar üzerinden organik olarak öne çıkmalı**: bir Faction Moves güncellemesi, bir NPC'nin rastgele bahsettiği bir söylenti, bir travel encounter sonucu, ya da başka bir iplik takip edilirken tesadüfen keşfedilmesi. Asla "bu oturum X dungeonuna gideceksiniz" şeklinde zorlanmaz — parti kendi yönünü seçer, DM sadece dünyanın bu ihtimalleri barındırdığından emin olur.
