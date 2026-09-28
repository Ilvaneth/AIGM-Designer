# P1 foundation — the owner-approved rows (2026-09-28)

*Source material for the P1 foundation tables (plan item 25). Every list below was approved by the owner in the development tab on 2026-09-27/28, in Turkish, and is kept here verbatim so nothing is lost before the tables are built. The YAML tables under `.claude/skills/dnd/data/design/` are built from this file: English ids and labels (development artifacts), these Turkish phrases as the rows' `tr` fields, plus the fields the plan names (family, gates, compatibility, columns). A change to a row is made here first, with the owner.*

Common rules (plan item 25):
- A row another campaign used is not drawn again while the table has rows; rows of the same family wait three births. Eylem and yara are grammar, not exhausted: a verb or scar used in the last three births waits, and a target + verb pair never repeats.
- Absent from every table: light and fuel (candle, wax, tallow, lamp), hush and bells, ledgers and tolls, the rights of the dead, courts and trials, tides, salt. Behind every break stands a living person's choice (the secret carries it); no "ancient evil awakens" (`forbidden.yaml`). No "Empire" (`forbidden_monolithic_empire` lexical); kingdom, dynasty, league instead.
- The dials weight rows (era, tone, magic, scale); gates are listed per table.

---

## 1. Palet — yer türleri (22)

**Olağan (14)**

| Tür | Mevcut biyomlar |
|---|---|
| dağ | high_mountains, foothills |
| yayla | pine_uplands, grazing_hills, moor |
| ova | river_valley |
| bozkır | steppe |
| orman | old_forest, jungle |
| bataklık | fen, salt_marsh |
| çöl | sand_desert, stone_desert, dunes, salt_flats |
| soğuk topraklar | tundra |
| volkanik | volcanic |
| nehir | river_delta, river_valley |
| göl | lake_country |
| kıyı ve deniz | sea_cliffs, salt_marsh |
| ada | kıyı biyomları |
| yeraltı | caverns, fungus_deeps |

`dead_city_lands` ve `drowned_lands` bir yer türüne değil yıkıntı kaynağına bağlanır.

**Fantastik (8)**

| Tür | Ne |
|---|---|
| yüzen adalar | havada asılı kayalar ve üstlerindeki köyler |
| kristal orman | ağaçları kristalden bir orman |
| taşlaşmış deniz | dalgaları taş kesilmiş, üstünde yürünen bir deniz |
| dev kemikleri | bir titanın iskeletinin üstünde ve içinde kurulmuş toprak |
| göğe akan nehir | yukarı doğru akan, havada bir su yolu |
| cam çölü | eski bir büyü savaşının camlaştırdığı kum |
| dev mantar ormanı | yüzeyde, ağaç boyu mantarlar |
| ince yer | bir düzlemin dünyaya değdiği yer; düzlemi P2 seçer |

**Kurallar:** büyü low → yalnızca ince yer; medium → en fazla bir fantastik; high → en fazla iki (büyü kadranı artık none almaz, en az low; 2. adımın kararı). Her palette en az bir yükselti (dağ, yayla, volkanik) ve en az bir su (nehir, göl, kıyı). Sayı: short 4-5, standard 6-8, epic 9-12. Palet satırları kampanyalar arasında dışlanmaz.

---

## 2. Omurga — dünyanın iskeleti (6 aile, 30)

Sütunlar: kalp · zıt uçlar (çekişmenin tarafları buraya oturur) · kilit yer (kırılmanın O hedefi) · yolculuk. Palet türleri script tarafından parçalara dağıtılır; iki uç farklı tür alır, kilit yer genelde bir yükselti ya da sudur.

**1. Tek hat**

| Omurga | Kalp | Zıt uçlar | Kilit yer | Yolculuk |
|---|---|---|---|---|
| Kaynaktan denize bir nehir | orta akıştaki köprü-şehir | kaynaktaki dağ halkları / deltadaki liman | nehrin tek geçilebilir sığlığı | nehir boyunca aşağı ve yukarı, mavnayla ve yoldan |
| Dev bir yarık | iki yakayı bağlayan köprü | yarığın tabanı / kenarlardaki yaylalar | köprü ya da tabana inen merdiven | kenarlar boyunca ve aşağıya iniş |
| Sıradağ boyunca geçitler | en büyük geçitteki kale-şehir | dağın yağmur alan yamacı / kurak yamacı | ana geçit | geçitten geçide, mevsime bağlı |
| Uzun bir kıyı şeridi | büyük liman | bir uçta buzul fiyortları / öbür uçta sıcak koylar | kıyıyı ikiye bölen burun | gemiyle kıyı boyunca; kara yolunu dağlar keser |
| Çorak koridor | koridorun ortasındaki han-şehir | koridorun iki ucundaki iki uygarlık | yoldaki tek su kaynağı | konaktan konağa, suya bağlı |

**2. Merkezli**

| Omurga | Kalp | Zıt uçlar | Kilit yer | Yolculuk |
|---|---|---|---|---|
| Dağlarla çevrili çanak, ortasında göl | göldeki ada-şehir | verimli havza / dağların ötesindeki bilinmeyen | havzadan çıkan tek geçit | göl üstünden ve kıyı yollarından içeri doğru |
| Tek dev dağ | yamaçtaki en büyük şehir | zirve / etek | zirveye çıkan yol ya da dağın içine inen ağız | halkalar halinde yukarı ve aşağı |
| Gökten düşen bir taşın krateri | kraterin ortasındaki taş | krater içi (değişmiş) / krater dışı | kenardan inen tek yol | kenardan merkeze |
| Vaha ve çevresindeki halka | vaha | vaha / çölün öbür yakası | vahanın suyu | vahadan dışa seferler; geri dönmek zorunlu |
| Dört yol ağzı | kavşak şehri | dört yöndeki dört farklı iklim ve ülke | kavşağın kendisi | merkezden dışa, dört koldan |

**3. Parçalı**

| Omurga | Kalp | Zıt uçlar | Kilit yer | Yolculuk |
|---|---|---|---|---|
| Takımadalar | en büyük ada | iç adalar / uzak ve vahşi dış adalar | adaları bağlayan tek güvenli boğaz | adadan adaya gemiyle, mevsime bağlı |
| Vadiler labirenti | en geniş vadi | birbirinden dağlarla ayrılmış, her biri başka bir halkın vadisi | vadileri bağlayan tüneller ve geçitler | geçitlerden; her vadi ayrı bir dünya |
| Sonsuz ormanın açıklıkları | en büyük açıklık | açıklıklar / ormanın derinliği | açıklıkları bağlayan patikalar | açıklıktan açıklığa, yolsuz |
| Mesa ülkesi | en büyük masa dağın üstündeki şehir | yaşanan mesa tepeleri / aradaki vahşi kanyonlar | mesaları bağlayan köprüler ve ip yollar | mesadan mesaya, kanyonlara iniş |
| Göller zinciri | iki gölü bağlayan boğazdaki şehir | zincirin iki ucundaki göller | göller arasındaki boğaz | gölden göle, suyla |

**4. Katmanlı**

| Omurga | Kalp | Zıt uçlar | Kilit yer | Yolculuk |
|---|---|---|---|---|
| Yüzey, orta derinlik ve derin | orta katmandaki şehir | yüzey / en derin katman | katmanları bağlayan büyük kuyu ya da kaldırgaç | aşağı ve yukarı |
| Basamaklar | orta terastaki şehir | en üstteki yayla / en alttaki ova | teraslar arası merdivenler ve şelaleler | basamak basamak |
| Üst üste iki dünya | iki dünyanın örtüştüğü şehir | bizim dünya / öbür düzlem | geçiş noktaları | iki katman arasında gidip gelme |
| Dağın içi ve dışı | dağın içindeki şehir | dağın dışı / dağın içi | dağın kapıları | kapılardan içeri ve dışarı |
| Deniz üstü ve deniz altı | kıyı şehri ya da bir resif | kıyı halkı / deniz altı halkları | sualtı mağaraları | dalış ve sualtı yolları |

**5. Sınır**

| Omurga | Kalp | Zıt uçlar | Kilit yer | Yolculuk |
|---|---|---|---|---|
| Yarımada | boyuna yakın şehir | yarımadanın ucu / anakara | boyun, tek kara geçişi | yarımadanın içinde; dışarı boyundan ya da denizden |
| Boğaz ve iki kıta | iki yakadaki ikiz şehir | iki kıta | boğaz | boğazı geçmek, iki kıyı boyunca gitmek |
| Uzun bir sur boyunca sınır | surun ana kapısı | surun içi / dışı | kapılar | sur boyunca ve kapılardan dışarı |
| İklim kuşağı | kuşağın ortasındaki şehir | donmuş kuzey / kavrulan güney | kuşağın daraldığı yer | kuşak boyunca doğu-batı, kenarlara seferler |
| Uygarlığın kenarı | son büyük şehir | bilinen topraklar / haritasız vahşi | sınır kalesi ya da son köprü | sınırdan vahşiye doğru |

**6. Fantastik**

| Omurga | Kalp | Zıt uçlar | Kilit yer | Yolculuk |
|---|---|---|---|---|
| Bir titanın sırtı | sırttaki şehir | baş / kuyruk | canlının içine inen yol | sırt boyunca |
| Yüzen takımada | en büyük yüzen ada | yüksek adalar / yere yakın adalar | adaları bağlayan zincirler ve rüzgâr yolları | uçan gemiler ve köprüler |
| Dipsiz bir boşluğun çevresindeki halka | boşluğa bakan şehir | halkanın iki karşı yakası | boşluğun üstündeki tek köprü | halka boyunca ya da köprüden |
| Tek dev ağaç (dağ boyunda) | gövdedeki şehir | dallardaki ülke / köklerdeki ülke | gövde | yukarı dallara, aşağı köklere |
| Dünyanın kenarı | uçurumun kenarındaki şehir | iç topraklar / uçurumun ötesindeki bulut denizi | kenardan aşağı inen tek yol | kenara doğru ve aşağıya |

Dev ağaç bir "dünya ağacı" değildir; mitolojiye gönderme yoktur.

**Kurallar:** era nautical → kıyı şeridi, takımadalar, boğaz, deniz üstü ve altı, yarımada ağır; era underground → katmanlar, dağın içi, yarık, vadiler labirenti, göller zinciri ağır, yüzey nadir. Titanın sırtı ve yüzen takımada yalnızca büyü high; boşluğun halkası, dev ağaç, dünyanın kenarı, üst üste iki dünya en az medium, üst üste iki dünya ayrıca palette ince yer ister. Küçük ölçeğe uygun: tek dağ, krater, vaha, çanak, mesa, yarımada, basamaklar; büyük ölçeğe uygun: nehir, iklim kuşağı, boğaz ve iki kıta, uygarlığın kenarı, geçitler (ağırlık, yasak değil).

---

## 3. Yıkıntı kaynağı — tehlikeli yerleri ne bıraktı (8 aile, 40)

Sütunlar: ne oldu (P2'de bir çağ) · kalıntı (kırılmanın Y hedefi) · bıraktığı mekânlar (P6; YAML'da `sites.yaml`'ın 10 türüne bağlanır) · bıraktığı tuhaflık (olgu imzasının zemini).

**1. Düşmüş krallıklar**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Yol yapan krallık | ülkeyi taş yollarla ve kalelerle ören krallık iç savaşla çöktü | taş yol ağı ve yol kaleleri | yol kaleleri, köprü kuleleri, gömülü hazine odaları | eski yollar yürüyeni hâlâ bir yere götürüyor |
| Su krallığı | sarnıçlar ve su kemerleri kuran krallık suyunu kaybedince dağıldı | su kemerleri ve sarnıçlar | sarnıçlar, kanallar, bent odaları | suyu yönlendiren eski büyü hâlâ çalışıyor |
| Büyücü-krallar hanedanı | büyüyle yöneten hanedan kendi büyüsüyle yıkıldı | saray-kuleler | kuleler, deney mahzenleri, bekçi golemleri | büyü hâlâ hanedanın kanını tanıyor |
| Şehir devletleri | birbirine düşen şehirler birbirini bitirdi | surlu, boş şehirler | terk edilmiş şehirler, tüccar mahzenleri, sur kuleleri | şehirlerin koruma büyüleri hâlâ yabancıyı uzaklaştırıyor |
| Bozkır birliği | dev bir göçebe birliği dağıldı | saray-kentler ve taş anıtlar | terk edilmiş saray-kentler, han mezarları, at kaleleri | anıtlar birliğin sınırlarını hâlâ çiziyor; sınırı geçen bunu hisseder |

**2. Savaşlar**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Büyü savaşı | iki büyücü okulunun savaşı toprağı camlaştırdı | cam çölü ve savaş kuleleri | yarı gömülü kuleler, büyü tuzakları, kaçmış savaş yaratıkları | cam kum büyüyü kırıyor ve yansıtıyor |
| Devler ve ejderhalar | iki büyük soy arasında savaş | ejderha kemikleri ve dev kaleleri | dev kaleleri, ejderha inleri, savaş alanları | kemiklerin yakınında ateş başka türlü yanıyor |
| Kuşatılmış ülke | yüz yıl kuşatılan bir ülke sonunda düştü | iç içe surlar ve kuşatma tünelleri | surlar, lağım tünelleri, cephanelikler | kuşatma büyüleri hâlâ tetikte |
| Kardeş savaşı | bir halkın iki kolu birbirini bitirdi | iki yakada ikiz kaleler | ikiz kaleler, gizli sığınaklar, ortak ama yasaklı tapınak | iki kolun kanı birbirine değince bir şey oluyor |
| Göksel savaş | düzlemler arası bir savaş bu dünyada çarpıştı | düşmüş savaş makineleri, yaralı toprak | çarpma kraterleri, düşmüş gök kaleleri, düzlem yarıkları | savaş alanında iyilik ve kötülük elle tutulur hale geliyor |

**3. Tanrılar**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Ölmüş bir tanrı | bir tanrı öldü, bedeni toprağa düştü | dağ gibi bir tanrı bedeni | bedenin içindeki mağaralar, çevresindeki tapınak-kentler | tanrının son dileği bedenin yakınında gerçekleşmeye çalışıyor |
| Tanrıların kavgası | tanrıların savaşı bir ülkeyi yarıp geçti | toprağa saplı tanrı silahları | silahların çevresindeki yarıklar, tapınak kaleleri | silahın yakınında o tanrının alanı güçlü |
| Terk eden tanrı | bir tanrı halkını bırakıp gitti | boş tapınaklar ve kutsal kentler | tapınak labirentleri, kutsal hazineler, bekçi yaratıklar | tapınaklar hâlâ ibadet bekliyor, dua edeni dinliyor |
| Hapsedilmiş tanrı | ölümlüler bir tanrıyı hapsetti ve bedelini ödedi | hapishane-tapınak | mühür odaları, bekçi tarikatının kaleleri | hapishanenin çevresine tanrının gücü sızıyor |
| Tanrılaşamayan ölümlü | bir büyücü tanrılığa yükselmeye çalıştı ve başaramadı | yükseliş kulesi | kule, ayin mahzenleri, yarı tanrılaşmış hizmetkârlar | kulede dilekler yarım gerçekleşiyor |

**4. Büyü**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Büyücüler çağı | büyünün bol olduğu çağ bir gecede bitti | büyüyle çalışan, şimdi durmuş bir şehir | durmuş büyü makineleri, akademi mahzenleri | bazı büyüler hâlâ kendi kendine çalışıyor |
| Başarısız deney | bir akademinin deneyi bir bölgeyi dönüştürdü | deney merkezi | laboratuvar-zindanlar, kaçan yaratıkların inleri | bölgede canlılar birbirine karışıyor |
| Yaratılmış halklar | büyücülerin yarattığı hizmetkâr halklar isyan etti | yaratım havuzları | yaratım salonları, isyan kaleleri | torunlar yaratıcılarının komutlarını hâlâ içlerinde duyuyor |
| Golem ordusu | savaş için kurulan golemler emir veren kalmayınca durdu | bekleyen golem ordusu | dökümhaneler, ordunun beklediği ovalar | golemler doğru sözü bekliyor |
| Kuruyan kaynak | bir büyü pınarı tükendi, ona bağlı uygarlık çöktü | kurumuş kaynak | kaynağın çevresindeki kuleler, kaynağa inen tüneller | kaynağın yakınında büyü tuhaf davranıyor |

**5. Doğa ve felaket**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Büyük sel | sel bir ovayı yuttu | sular altındaki şehirler | batık şehirler, sudan çıkan kuleler, sualtı mahzenleri | batık şehirlerde hava cepleri; sualtı halkları yerleşmiş |
| Püskürme | bir yanardağ bir ülkeyi lav altına gömdü | lavın dondurduğu şehir | lav altındaki şehir, lav tüpleri, ateş yaratıklarının inleri | lav tüplerinde ateş yaratıkları hâlâ yaşıyor |
| Buz çağı | buzullar bir uygarlığı örttü | buzun altındaki şehir | buz mağaraları, donmuş kaleler | buzda donmuş canlılar çözülmeyi bekliyor |
| Salgın | bir salgın bir ülkeyi boşalttı | karantina şehirleri, hastane-kaleler | boş şehirler, hastane zindanları, yasak vadiler | salgının bıraktığı bağışıklık bir halkta güce dönüştü |
| Gökten düşen taş | bir yıldız ya da ay parçası düştü | krater ve gök taşı | krater, gök taşının içi, çevresindeki kasabalar | gök taşının yakınında canlılar değişiyor |

**6. Emek ve hırs**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Maden hücumu | bir cevher için dağlar delindi, cevher bitince herkes gitti | terk edilmiş maden şehri | galeriler, dökümhaneler, derine inen kuyular | madenciler derinde bir şeye ulaşmıştı |
| Bitmeyen yapı | bir hükümdarın dev yapısı halkını tüketti | yarım kalmış dev yapı | yapının içi, taş ocakları, işçi köyleri | yapı kendi kendine büyümeye devam ediyor |
| Tüccar hazineleri | bir tüccar birliği hazinelerini tek yerde topladı, sonra dağıldı | hazine kasaları | kasa-zindanlar, tuzaklı depolar, liman mahzenleri | kilitler yalnızca eski birliğin mühürlerini tanıyor |
| Geri dönen orman | bir krallık ormanı tüketti; orman geri geldi ve krallığı yuttu | ormanın içindeki şehir | ağaçların yuttuğu saraylar, orman ruhlarının inleri | orman eski şehrin sakinlerine kin tutuyor |
| Simya taşkını | bir simya loncasının üretimi toprağı ve suyu değiştirdi | simya işlikleri | işlikler, zehirli bataklık, dönüşmüş canlıların inleri | bölgenin bitkileri iksir etkisi taşıyor |

**7. Eski halklar**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Terk edilmiş cüce şehri | cüceler derinden gelen bir şeyden kaçtı | derin şehir ve büyük kapısı | yeraltı şehri, dökümhaneler, mühürlü derin kapı | cüce runeleri yabancılara karşı hâlâ çalışıyor |
| Elflerin çekildiği orman | elfler başka bir düzleme çekildi | boş ağaç-şehirler | ağaç-saraylar, fey geçitleri, bekçi yaratıklar | ormanda zaman farklı akıyor |
| Devlerin ülkesi | devler bir zamanlar bu toprağı yönetiyordu | insana göre dev yapılar | dev kaleleri, dev merdivenler, dev hazineleri | devlerin taşları hâlâ onların sözünü dinliyor |
| Ejderhalar çağı | ejderhalar hüküm sürdü, sonra birbirini yok etti | inler ve hazineler | inler, hazine mağaraları, ejderha tapınakları | ejderha soyundan gelenler hâlâ hak iddia ediyor |
| Kanatlı halkın dağları | kanatlı bir halk ortadan kayboldu | yalnızca uçarak ulaşılan tepe şehirleri | tepe şehirleri, yuvalar, rüzgâr kuleleri | rüzgâr onların yollarını hâlâ taşıyor |

**8. Düzlemler ve gök**

| Kaynak | Ne oldu | Kalıntı | Mekânlar | Tuhaflık |
|---|---|---|---|---|
| Düzlem yarığı | bir düzlemin kapısı açıldı, sonra kapandı | yarığın izi | yarık çevresindeki dönüşmüş toprak, düzlem yaratıklarının kaleleri | yarık bölgesinde o düzlemin bir kuralı geçerli |
| Düşen gök şehri | havada uçan bir şehir düştü | şehrin parçaları | parçalanmış saraylar, hâlâ havada duran parçalar | parçalar yeniden havalanmak istiyor |
| Düzlem istilası | başka bir düzlemden gelen ordu geri püskürtüldü | istilacıların kaleleri | istilacı kaleleri, esir kampları, kapı kalıntıları | istilacıların bıraktığı yaratıklar çoğalıyor |
| Zamanın kırıldığı yer | bir büyü zamanı kırdı | zamanı donmuş bir şehir | zamanın farklı aktığı sokaklar | şehirde geçmişten ve gelecekten parçalar dolaşıyor |
| Yıldızlara uzanan krallık | bir gözlemevi-krallık yıldızlardan bir şey çağırdı | gözlemevleri | gözlemevleri, çağrı odaları, yıldız yaratıklarının inleri | belli gecelerde gökyüzü yaklaşıyor |

**Kurallar:** palete tür getirenler: büyü savaşı → cam çölü; ölmüş tanrı → dev kemikleri; büyük sel → `drowned_lands`; terk edilmiş şehirler → `dead_city_lands`; gökten düşen taş → krater; düşen gök şehri → havada duran parçalar. Ton: cosmic → yıldızlara uzanan krallık, zamanın kırıldığı yer; horror → başarısız deney, salgın; heroic → ejderhalar çağı, devlerin ülkesi. Era: underground → cüce şehri, maden hücumu; nautical → büyük sel. Büyü low → büyücüler çağı iyi oturur. Mezar yalnızca han mezarlarında (onaylı).

---

## 4. Can damarı — neyle yaşıyorlar, neyi kaybedemezler (7 aile, 60)

Sütunlar: nerede (palet türleri; script yalnızca paletin getirdiği türlere uyan satırları çeker ve damarı omurgaya yerleştirir) · kimler, ne üretir (meslekler P5'e, mallar P3'e) · zayıf nokta (kırılmanın tutacağı yer) · duyu.

**1. Su**

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta | Duyu |
|---|---|---|---|---|
| Dağlardan inen kar suyu | dağ, ova, nehir | sulama ustaları, çiftçiler / tahıl, sebze | tek bir kaynaktan geliyor | taşlarda soğuk su şırıltısı |
| Nehrin yıllık taşkını | nehir, ova | taşkın bekçileri, çiftçiler / tahıl, keten | taşkın gelmezse ya da fazla gelirse | ıslak balçık kokusu |
| Derin yeraltı gölü | yeraltı, çöl | kuyucular, su taşıyıcılar / su, kör balık | tek bir göl; kirlenirse biter | mağara serinliği, damla sesi |
| Vaha pınarları | çöl | pınar bekçileri, hurmacılar / su, hurma | pınarlar birbirine bağlı; biri kurursa hepsi kurur | hurma şerbeti kokusu |
| Sıcak su kaynakları | volkanik, dağ, soğuk topraklar | şifacılar, seracılar / kış sebzesi, şifa | ısıları yanardağa bağlı | kükürt ve buhar |
| Yağmur mevsimi | orman, ova, bataklık | çeltikçiler / pirinç | yağmur gecikirse | yağmur öncesi toprak kokusu |
| Buzul | soğuk topraklar, dağ | buz kesiciler / buz, temiz su | buzul çekiliyor | buzun çatırtısı |
| Sisten su toplayan ağlar | kıyı, çöl | ağ örücüler / su | sis gelmezse | ıslak ağların serinliği |

**2. Geçiş yeri**

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta | Duyu |
|---|---|---|---|---|
| Kışın açık kalan tek geçit | dağ | rehberler, hancılar, katırcılar / konak, hizmet | çığ ve kar | donmuş nefes, katır teri |
| Nehrin tek sığ geçidi | nehir | salcılar, köprücüler / geçiş, pazar | nehir yatak değiştirirse | ıslak halat ve katran |
| Doğal liman | kıyı, ada | liman işçileri, kılavuzlar / ticaret, balık | tek bir girişi var | katran ve balık kokusu |
| Kervan yolunun ortasındaki konak | çöl, bozkır | hancılar, deveciler / hizmet, takas | yol değişirse | baharat ve deve kokusu |
| Yarığın üstündeki köprü | dağ | köprü bakıcıları / geçiş | tek bir taşıyıcı ayağı var | rüzgârın uğultusu |
| Boğazdaki geçit | kıyı | kürekçiler, kılavuzlar / geçiş, balık | akıntılar | deniz esintisi |
| Yeraltının yüzeye açılan ağzı | yeraltı | kaldırgaç ustaları, taşıyıcılar / yüzey ile derin arasında takas | tek bir ağzı var | yukarı vuran ılık hava, pas kokusu |
| Bataklığı geçen tahta yol | bataklık | yol ustaları, sazcılar / geçiş | tahtalar çürür | çürük saz ve mantar |
| Buz yolu (kışın donan göl ya da nehir) | göl, soğuk topraklar | kızakçılar / kış ticareti | erken çözülme | kızak demirinin buzda sürtünmesi |

**3. Canlılar**

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta | Duyu |
|---|---|---|---|---|
| Yak sürüleri | dağ, yayla, soğuk topraklar | çobanlar, keçeciler / süt, yün, keçe | sürü hastalığı, otlak | yağlı yün kokusu |
| Yılda bir gelen balık göçü | nehir, kıyı, göl | balıkçılar, kurutucular / kuru balık, yağ | göç yolu değişirse | duman ve balık |
| İpekböceği bahçeleri | ova, orman | dut bahçıvanları, dokumacılar / ipek | ipekböceği hastalığı | dut yaprağı, kaynayan koza |
| Arı ormanları | orman, yayla | arıcılar / bal, polen, ilaç | arılar ölürse | bal ve reçine |
| At sürüleri | bozkır, ova | at yetiştiricileri, süvariler / at, kımız | otlak, at hırsızları | ter ve deri |
| Geyik göçü | soğuk topraklar, orman | avcılar, göçebeler / et, deri, boynuz | göç yolu | kar ve reçine |
| İstiridye yatakları | kıyı | dalgıçlar / inci, istiridye | yataklar hastalanırsa | deniz yosunu |
| Evcil dev böcekler | yeraltı, çöl | böcek terbiyecileri / taşıma, ipek, kitin | kraliçe ölürse | ekşi kitin kokusu |
| Grifon yuvaları | dağ, yayla | grifon terbiyecileri / binek, haberci | yumurta hırsızları | tüy ve kan |

**4. Maden ve kaynak**

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta | Duyu |
|---|---|---|---|---|
| Bakır madeni | dağ | madenciler, dökümcüler / bakır, tunç | damar tükenirse, madeni su basarsa | yanık metal, yeşil pas |
| Demir ve kömür | dağ, yayla | madenciler, kömürcüler, demirciler / demir, silah | ormanlar kömür için tükeniyor | kömür dumanı |
| Kereste ormanı | orman | ormancılar, gemi ustaları / kereste, gemi | orman tükenirse | talaş ve reçine |
| Turba bataklığı | bataklık, soğuk topraklar | turba kesiciler / kışlık yakacak | bataklık kuruyor | turba dumanı |
| Taş ocağı (mermer, granit) | dağ, yayla | taşçılar, heykeltıraşlar / yapı taşı | ocak çökerse | taş tozu |
| Değerli taşlar | yeraltı, dağ | kazıcılar, kuyumcular / mücevher | tükenme, sahtecilik | keskinin tıkırtısı |
| Boya kaynakları (deniz salyangozu, kök boyaları) | kıyı, ova | boyacılar / boya, kumaş | kaynak tükenirse | keskin boya kokusu |
| Katran ve zift | orman, kıyı | zift ustaları / gemi katranı | orman yangını | katran kokusu |
| Kehribar kıyıları | kıyı, soğuk topraklar | toplayıcılar / kehribar | fırtınalar | reçine ve deniz |

**5. Ekin**

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta | Duyu |
|---|---|---|---|---|
| Teras pirinci | dağ, yayla, orman | çeltikçiler / pirinç | teraslar çökerse, su gelmezse | çamur ve pirinç |
| Zeytinlikler | kıyı, yayla | zeytinciler / zeytin, yemeklik yağ, sabun | kuraklık, zeytin sineği | ezilen zeytin |
| Bağlar | yayla, ova | bağcılar, şarapçılar / şarap | bağ hastalığı | mayalanan üzüm |
| Keten tarlaları | ova, nehir | ketenciler, dokumacılar / keten, yelken bezi | taşkın olmazsa | ıslatılan keten |
| Buğday ovası (bölgenin ambarı) | ova | çiftçiler, değirmenciler / tahıl | kuraklık, çekirge | un ve saman |
| Hurma ve incir bahçeleri | çöl | bahçıvanlar / hurma, incir | pınar kurursa | olgun hurma |
| Baharat bahçeleri | orman, kıyı | baharatçılar / baharat | hastalık, korsanlar | karanfil ve biber |
| Mantar tarlaları | yeraltı | mantarcılar / yiyecek, ilaç | küf, spor hastalığı | toprak ve küf |
| Çay yamaçları | dağ, yayla | çaycılar / çay | don | yaş çay yaprağı |

**6. Zanaat**

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta | Duyu |
|---|---|---|---|---|
| Ünlü çelik (kılıç dövme) | dağ | demirciler / silah | ustaların sırrı; bir usta ölürse | örs sesi |
| Cam üfleme | kıyı, çöl | camcılar / cam, mercek | kum ve odun | erimiş camın sıcağı |
| Halı dokuma | yayla, bozkır | dokumacılar, boyacılar / halı | yün ve boya | yün ve kök boyası |
| Gemi yapımı | kıyı | gemi ustaları / gemiler | kereste | talaş ve katran |
| Çini ve seramik | ova, nehir | çömlekçiler / çini | kil yatağı | pişen kil |
| Deri ve zırh işçiliği | bozkır, ova | tabaklar, zırhçılar / deri, zırh | sürüler | tabakhane kokusu |
| İksir ve ilaç | orman, bataklık | şifacılar, simyacılar / ilaç, iksir | bitkiler tükenirse | acı otlar |
| Yay yapımı | orman | yaycılar / yay, ok | akçaağaç ve boynuz | reçine ve tutkal |

**7. Antlaşma ve düzen** (duyu sütunu yok)

| Can damarı | Nerede | Kimler, ne üretir | Zayıf nokta |
|---|---|---|---|
| Devlerle barış (devler dağda, insanlar ovada) | dağ, ova | sınır elçileri / güvenlik, takas | söz bozulursa |
| Ejderhanın koruması (ejderha korur, bölge besler) | her yer | ejderha hizmetkârları / koruma | ejderha yaşlanıyor |
| Fey ile pazarlık (orman bereket verir, halk karşılığını öder) | orman | pazarlıkçılar / bereket | karşılık aksarsa |
| Deniz halkıyla ortak av | kıyı | balıkçılar / balık | anlaşma |
| Paralı muhafızlar (bir birlik bölgeyi korur, bölge öder) | her yer | muhafızlar / güvenlik | ödeme aksarsa |
| İki krallığı bağlayan evlilik | her yer | elçiler / barış | bir ölüm |
| Ortak su hakkı (yukarı ve aşağı köyler suyu sırayla kullanır) | nehir, ova | su bekçileri / sulama | kuraklık |
| Hac yolu (hacılar gelir, bölge onlarla yaşar) | her yer | hancılar, rehberler / hizmet | hacılar gelmezse |

**Kurallar:** dev böcekler ve grifonlar büyü medium ve üstünde (dev böcekler era underground'da da); ejderha ve fey satırları büyü low ve üstünde. Tuz, balmumu, lamba yağı, don yağı, katır çanı ve geçiş ücreti yok; büyü meta olarak hiçbir satırda yok.

---

## 5. Çekişme — kampanyanın ana fay hattı (8 aile, 40)

Sütunlar: A ve B (varsayılan olarak omurganın iki ucunda; farklıysa adın yanında) · üçüncü (short'ta roller burada biter) · 4. rol (standard ve epic) · parantez: P4 için faksiyon arketipi ipucu · ödül (damar, kalp, kalıntı ya da yeni) · tırmanma (ilk kıvılcım → en sert hali). Kırılmanın "kazanan" zarı rollerden birini seçer.

Ölçek: short 1 çekişme, 3 rol · standard 1 çekişme, 4 rol · epic 2 çekişme (ana 4 rol; başka bir aileden, omurganın başka bir yerinde ikinci 3 rol). Rolü olmayan faksiyonlar ana çekişmeye tavır takınır (P4'e söz).

**1. Aynı şeye iki el**

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| İki varis (naip kalpte) | büyük varis (devlet) | küçük varis ve ordusu (askerî) | tacı ve hazineyi tutan naip (devlet) | tahtı isteyen yabancı bir krallık | kalp | taç giyme tarihi → iç savaş |
| Aynı limanı isteyen iki şehir (kilit yerin iki yanında) | eski liman şehri (lonca) | yeni kurulan rakip şehir (ticaret) | limanı kullanan kaçakçılar (suç) | denizciler loncası | damar | gemilere el koyma → kıyı savaşı |
| İki halk, bir otlak | sürü sahibi yayla klanları (askerî) | tarlasını genişleten ova köyleri (devlet) | iki tarafa da at ve silah satan tüccarlar (ticaret) | otlağın ortasındaki kutsal yerin bekçileri (din) | damar | sürü baskınları → kan davası |
| İki inanç, bir kutsal yer (kutsal yer kilit yerde) | kutsal yerin eski bekçileri (din) | aynı yeri kendi tanrısının sayan yeni inanç (din) | hacılarla geçinen kasaba (lonca) | yeri kazmak isteyen bilginler (bilgin) | kalıntı | hacıların yolunun kesilmesi → kutsal yerde kan |
| Bir nehir, iki yaka | yukarı akıştakiler (devlet) | aşağı akıştakiler (devlet) | suyu yönlendiren bent ustaları (lonca) | nehirde yaşayan bir halk | damar | suyu kesme → bent yıkma |

**2. Eski ve yeni**

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| Yerleşikler ve yeni gelenler (gelenler bir uçta) | toprağın eski sahipleri (devlet) | toprağın ihtiyacı olan şeyi getiren yeni gelenler (ticaret) | ikisinden de kazanan tüccarlar (ticaret) | korkan halkı örgütleyen biri (direniş) | damar | yasaklar → mahalle yangınları |
| Eski düzen ve reformcular | eski soylular (devlet) | reform isteyen genç hükümdar ya da meclis (devlet) | reformdan kazanacak loncalar (lonca) | eski düzenin askerleri (askerî) | kalp | yeni yasalar → darbe girişimi |
| Eski zanaat, yeni zanaat | eski yöntemle üreten loncalar (lonca) | yeni bir alaşım ya da makine getirenler (bilgin) | işsiz kalan işçiler (direniş) | yeni yöntemi silah olarak isteyen bir devlet | damar | boykot → makine kırma → kan |
| Eski tanrılar, yeni inanç | eski tapınaklar (din) | hızla yayılan yeni inanç (din) | taraf seçmeye zorlanan hükümdar (devlet) | iki inancı da reddeden büyücüler (bilgin) | kalp | vaazlar → tapınak yakma |
| Dönenler ve kalanlar | yıllar önce sürülüp geri dönen halk (askerî) | onların topraklarına yerleşmiş olanlar (devlet) | dönüşü destekleyen yabancı bir güç (devlet) | iki taraftan da evlenmiş karışık aileler | kalp | eski evlerin kapısını çalmak → silahlı dönüş |

**3. Güçlü ve zayıf**

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| İşgalci ve direniş (işgalci kalpte) | bölgeyi tutan dış güç (askerî) | dağlardaki direniş (direniş) | işbirlikçi yerel soylular (devlet) | iki taraftan da kazanan kaçakçılar (suç) | kalp | vergiler ve askerler → ayaklanma |
| Başkent ve sınır boyu (başkent kalpte) | başkent (devlet) | sınır lordları ve korucular (askerî) | sınırın öbür yanındaki halk | iki tarafa da asker kiralayan paralı birlik (askerî) | damar | yardımın kesilmesi → sınırın kopması |
| Beyler ve köylüler | toprak sahibi beyler (devlet) | köylü birliği (direniş) | köylülere silah vermeyi düşünen bir din önderi (din) | beylerin paralı muhafızları (askerî) | damar | angarya → köylü ayaklanması |
| Maden sahipleri ve madenciler | madeni elinde tutan aile (lonca) | madenciler (direniş) | cevheri alan dış tüccarlar (ticaret) | madenin genişlemesine öfkelenen derin bir halk | damar | grev → maden baskını |
| Büyücüler ve büyüsüzler | büyüyü tekelinde tutan bir soy ya da kurum (bilgin) | büyüsüz çoğunluk (direniş) | gizlice büyü öğreten kaçak ustalar (suç) | büyüyü tümden yasaklamak isteyen bir inanç (din) | kalp | yasaklar → büyücü avı |

**4. Açanlar ve kapayanlar**

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| Kapalı kalıntı (kalıntı kilit yerde) | kalıntıyı açmak isteyenler (bilgin) | kapalı tutmak isteyen bekçiler (din) | gizlice parça çıkaran yağmacılar (suç) | açılırsa kazanacak dış bir güç | kalıntı | izin istekleri → gece kazıları → bekçilerle çatışma |
| Yolu açanlar ve kapayanlar | yolu ticarete açmak isteyenler (ticaret) | yabancıyı dışarıda tutmak isteyenler (devlet) | kapalı yolda kaçakçılık yapanlar (suç) | yolun öbür ucundaki ülke | damar | kervan yasakları → kervan yakma |
| Yasak topraklar | yasak toprakları keşfetmek isteyenler (bilgin) | girişi engelleyenler (askerî) | oradan gelen şeyleri satanlar (suç) | yasak topraklarda yaşayanlar | kalıntı | devriyeler → sınır ötesine seferler |
| Bilgiyi yayanlar ve saklayanlar | bir zanaatı ya da büyüyü herkese açmak isteyenler (bilgin) | onu sır tutan lonca (lonca) | bilgiyi çalıp satan casuslar (suç) | bilgiyi silaha çevirmek isteyen bir devlet | damar | kopyalama → suikast |
| Kapıyı açanlar ve kapayanlar (palette ince yer gerekir) | düzlem geçidini açık tutmak isteyenler (ticaret) | kapatmak isteyenler (din) | öbür düzlemden gelenler | geçidin yanındaki köyler | kalıntı | ayinler → geçitte savaş |

**5. Yarış**

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| Hazineye koşan gruplar | kraliyetin resmî seferi (devlet) | paralı bir birlik (askerî) | yerli halkın avcıları | bir büyücünün gizli seferi (bilgin) | kalıntı | haritaların çalınması → yolda pusu |
| Boş taht, üç ev | en güçlü ev (devlet) | en zengin ev (ticaret) | en eski ev (din) | halkın sevdiği bir yabancı (direniş) | kalp | evlilik ittifakları → zehir → açık savaş |
| Yeni toprağa ilk yerleşen | bir krallığın yerleşimcileri (devlet) | özgür yerleşimciler (direniş) | toprağın yerli halkı | toprak satan dolandırıcılar (suç) | yeni | sınır taşları → yerleşim yakma |
| Canavar için ödül | bir şövalye tarikatı (askerî) | avcılar loncası (lonca) | canavarı koruyan köylüler | canavarın parçalarını isteyen simyacılar (bilgin) | kalp | tuzaklar → rakibi canavara yem etmek |
| Yeni kaynağı ilk kim alacak | devlet (devlet) | loncalar (lonca) | kaynağın üstünde yaşayan halk | kaçakçılar (suç) | yeni | hak iddiaları → kaynağın başında kan |

**6. Kardeş kavgası**

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| Bir halkın iki kolu | kırılmayı bir ceza sayan kol (din) | onu bir fırsat sayan kol (ticaret) | iki kolu birleştirmeye çalışan yaşlılar | kollardan birini kullanan dış bir güç | kalp | ayrı pazarlar → ayrı ordular |
| Bir tarikatın bölünmesi | eski önderlik (din) | kopan genç kol (direniş) | tarikatın hazinesini tutan kâhya (lonca) | bölünmeden kazanan rakip bir inanç | kalıntı | tarikattan kovma → kardeş kanı |
| İkiye bölünmüş şehir (kalp ikiye bölünmüş) | şehrin bir yarısı (devlet) | öbür yarısı (devlet) | iki yarıyı bağlayan kapının bekçileri | yeniden birleşmek isteyen gençler (direniş) | kalp | kapıların kapanması → köprüde çatışma |
| Kardeş hükümdarlar | ülkenin yarısını yöneten büyük kardeş (devlet) | öbür yarısını yöneten küçük kardeş (devlet) | hâlâ yaşayan eski hükümdar, anneleri ya da babaları | iki kardeşe de kız vermiş komşu krallık | kalp | sınır anlaşmazlığı → kardeş savaşı |
| Bölünen aile | aile reisinin kolu (lonca) | ayrılan kol (ticaret) | aile zanaatının sırrını bilen tek usta | rakip bir lonca | damar | müşteri çalma → sabotaj → cinayet |

**7. İnsan ve insan-dışı** (iki tarafın da haklı çıkarları var; hiçbiri doğuştan kötü değil)

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| İnsanlar ve devler | ovaya yayılan krallık (devlet) | dağlarda eski haklarını savunan dev klanları | iki tarafla da ticaret yapanlar (ticaret) | devlerle yaşamayı öğrenmiş sınır köyleri | damar | sınır taşları → dev baskınları → savaş |
| İnsanlar ve ejderha | kasabalar birliği (devlet) | bölgeyi yurdu sayan ejderha ve hizmetkârları | ejderhaya boyun eğip korunan bir inanç (din) | ejderha avcıları (askerî) | damar | sürü kayıpları → ejderha avı |
| İnsanlar ve fey | ormanı açan köyler (devlet) | ormanın fey sahipleri | iki dünya arasında aracılık eden druidler (din) | fey ile gizlice pazarlık eden bir soylu | damar | ağaç kesimi → kaybolan çocuklar → orman savaşı |
| Yüzey ve derin | yüzeydeki madenciler (lonca) | derinlerde yaşayan halk | iki dünya arasında taşıyıcılık yapanlar (ticaret) | derin halktan kaçıp yüzeye sığınanlar | damar | tünel kapatma → tünel savaşı |
| Kara ve deniz halkı | kıyı şehirleri (devlet) | deniz halkı (tritonlar, balık halkları) | iki halktan evlenmiş kıyı aileleri | denizin dibini kazmak isteyen tüccarlar | damar | ağlar ve mızraklar → kıyı akınları |

**8. Görünmeyen el** (üçüncünün oyunu herkesin bildiği bir söylenti olarak kalır, kanıtlanmamıştır)

| Çekişme | A | B | Üçüncü | 4. rol | Ödül | Tırmanma |
|---|---|---|---|---|---|---|
| İki tarafı birbirine düşüren tüccar evi | bir rakip (devlet) | öbür rakip (devlet) | ikisine de silah ve para veren tüccar evi (ticaret) | gerçeği bilen bir kaçak | damar | küçük saldırılar → büyük savaş; sonunda tüccar ikisini de alır |
| Yabancı elçi | yerel bir güç (devlet) | öbür yerel güç (devlet) | ikisine de dost görünen uzak bir krallığın elçisi (devlet) | elçinin planını sezen bir casus şebekesi (suç) | kalp | armağanlar → suikastlar → işgal bahanesi |
| Savaştan beslenen birlik | bir ülke (devlet) | komşusu (devlet) | iki tarafa da kiralanıp savaşı uzatan paralı birlik (askerî) | barış isteyen tüccarlar (ticaret) | damar | sınır olayları → bitmeyen savaş |
| Yıkılmış devletin artığı | yeni güçlerden biri (devlet) | öbürü (devlet) | eski devleti yeniden kurmak isteyen gizli hayranları | mirasçı olduğunu bilmeyen biri | kalp | eski simgeler → darbe |
| Kılık değiştiren | bir köy ya da aile | öbürü | iki tarafı birbirine düşüren kılık değiştirmiş bir yaratık ya da fey | ondan şüphelenen bir avcı | damar | suçlamalar → kan davası |

**Kurallar:** kötü hiçbir satırda varsayılan olarak taraf değildir; "görünmeyen el" üçüncüsü bir faksiyondur. Bağı P1'in gizli zarı belirler. Fısıldayan danışman, doğuştan kötü halklar ve "kötü tarikat" yok; inanç rolleri meşru taraflardır. "Kapıyı açanlar" palette ince yer ister; ejderha ve fey satırları büyü low ve üstünde; "yüzey ve derin" yeraltında, "kara ve deniz halkı" nautical'da ağır; political → 2, 6, 8. aileler, war → 3 ve 5. aileler ağır.

---

## 6. Kırılma — en son kurulur, önceki parçalardan birini vurur

Zar beş parçayı seçer: **hedef** (temelin taşıyıcı parçalarından biri), **eylem**, **yara**, **zaman**, **kazanan** (çekişmenin rolü). Çekişme kırılmadan önce de vardır; kırılma onu sarsar. Etki alanı ölçekle genişler (short bir bölge, epic birçok ülke). Her kırılmanın arkasında yaşayan birinin kararı vardır; sır bunu taşır.

**Hedef kısaltmaları:** D can damarı · Y yıkıntının kalıntısı · O omurganın kilit yeri · K kalp · R çekişmenin bir rolü · İ ince yer (palette varsa).

**Eylem (21)**

| Eylem | Hedef | Örnek |
|---|---|---|
| yok oldu | D, Y, O, K, R | kalp şehir bir gecede yok oldu |
| ele geçirildi | D, Y, O, K, İ | geçidi dışarıdan bir güç tuttu |
| tersine döndü | D, O | nehir göğe akıyor; sürüler ters yöne göçüyor |
| ikiye bölündü | D, O, K, R | kara bir yarıkla bölündü; bir halk ikiye ayrıldı |
| bozuldu | D, Y, O, K | kutsal su zehre döndü |
| canlandı | Y, O | titanın kemikleri kıpırdadı; dağ yürüdü |
| gökten düştü | D, O, K | bir ay kalbin üstüne düştü |
| durdu | D, O, K | nehir akışının ortasında dondu; bir şehirde zaman durdu |
| açıldı | Y, O, İ | ölü tanrının bedeni yarıldı, içi açıldı |
| kapandı | D, O, İ | düzlemlere giden bütün yollar kapandı |
| bir düzlemle birleşti | O, K, İ | kalp şehir yarı yarıya başka bir düzlemde |
| gerçek yüzünü gösterdi | D, Y, O | dağ aslında uyuyan bir canlıydı |
| bekçilerine döndü | D, Y, R | eski yapılar onları yapanlara saldırıyor |
| sınırsız yayıldı | D, Y, İ | halkı besleyen mantar her şeyi yiyor |
| göçüp gitti | D, K, R | balık göçü başka bir denize gidiyor; başkent yürüyüp gitti |
| yandı | D, O, K | şehir yandı, külleri hâlâ sıcak |
| yükseldi | Y, O, K, R | denizden yeni bir kara çıktı; bir hükümdar tanrılığa yükseldi |
| battı | Y, O, K | kalp şehir yer altına gömüldü ve hâlâ orada |
| ikizlendi | D, K, İ | kalp şehrin bir ikizi belirdi |
| unutuldu | Y, K, R | herkes bir şehrin adını ve yolunu unuttu |
| doğdu | D, Y, İ | savaş alanından yeni bir tanrı doğdu; yaradan bir ejderha soyu çıktı |

**Yara (18)** — sayısı ölçekle: short 1, standard 2, epic 3. Her yara bir kolondur.

| Yara | İndiği kat |
|---|---|
| haritada yeni bir yer türü (fantastik paletten) | P1 palet, P3 harita |
| yolların değişmesi | P3 harita, omurga |
| zehirli ya da lanetli bir kuşak | P3, P6 |
| erişilmez bir bölge | P3 harita; P7'de sonraki bir perde onu açar |
| büyünün bir kuralı değişti | P2 büyü (olgu imzası bununla birleşebilir) |
| bir tanrı değişti | P2 panteon |
| bir düzlemle sınır inceldi | P2 düzlemler |
| gökyüzü değişti | P2 takvim |
| mevsimler bozuldu | P2 iklim ve takvim |
| zamanın akışı değişti (bir bölgede hızlı ya da yavaş) | P2, P3 |
| bir halk yerinden oldu | P3, P5 |
| yeni bir halk ortaya çıktı (kırılmanın dönüştürdükleri) | P5 (halk imzası bununla birleşebilir) |
| bir devlet yıkıldı, yerinde boşluk kaldı | P3, P4 |
| canlılar değişti | P6 canavarlar |
| yeni bir kaynak doğdu | P3 ekonomi, çekişme |
| bir bilgi ya da zanaat kayboldu | P3; P6'da harabeler onu saklar |
| yeni bir yasak ya da tabu | P2 ve P3, kültür ve yasa |
| yeni bir inanç (yasaklı "kötü tarikat" değil, bir taraf) | P2, P4 |

Bilerek dışarıda: "ölüler geri dönüyor, ölümün kuralı değişti" (altı doğumun çekim alanı).

**Zaman (4):** az önce (oyun kırılmanın hemen ardında başlar) · bir kuşak önce (dünya yaranın etrafında yeniden kurulmuş) · şimdi oluyor (kırılma kampanya boyunca açılır) · yaklaşıyor (işaretler görülüyor, kampanya ona karşı bir yarış).

**Kazanan:** kırılmanın güçlendirdiği çekişme rolü; dengesizlik fay hattını harekete geçirir.

**Tırmanış:** D&D'nin dört oyun katmanı (seviye 1-4 yerel, 5-10 bölgesel, 11-16 kıtasal, 17-20 dünya ve düzlemler) kırılmanın basamaklarıdır; parti onunla önce yerel bir belirti olarak karşılaşır, sonunda kalbine ulaşır. Basamak sayısı seviye bandından: short 1-2, standard 3, epic 4. Her basamak P7'ye söz olarak iner.

**Reddedilen:** 64 hazır olay satırı ("köprü çöktü" gibi) efsanevi bir hikâye için küçük bulundu; kırılma olay listesinden değil bu beş parçadan kurulur.

---

## 7. Oynanış kipleri — P7'nin sırasında tasarlanacak aday liste

Motor P0'dan çıktı (errata 24.2 #21). Bu satırlar kampanyanın tamamını değil, 2-3 oturumluk bir bloğu anlatır; bloklar dünyada ne varsa ona göre seçilir. Liste onaylı değil, P7'nin sırası gelince konuşulacak.

soruşturma · geri sayım · kuşatma · savaş cephesi · yolculuk · keşif · derine iniş · av · yarış · entrika · sınırda kurmak · savunma · sürgün ve dönüş · paralı birlik · hayatta kalma · sonuç zinciri. Kehanet ve parça toplama yasak kalır.

---

# Step 2 — the identity (approved 2026-09-28, discussion continuing)

Every identity table follows step 1's rules. The three signatures share one shape: a **home** in the foundation, a **visible** piece and a **behaving** piece, plus one or two framing rolls; the writer joins them, names them and makes them specific.

**P0 ruling (owner, 2026-09-28):** the magic dial never takes `none`; its minimum is `low`. `dials.yaml#magic` loses `magic_none` (plus `test_design_tables.py` and `SKILL-design.md`'s dial line).

## 8. Halk imzası

Kuruluş: **ev** can damarı (yara "yeni bir halk ortaya çıktı" ise o yeni halk) · **soy** (zar; paletten ve damardan ağırlık) · **iki özellik**, biri **görünen** (beden, bir canlıyla bağ, yer ve hareket) biri **davranan** (âdet, inanç, toplumsal düzen, kırılmayla ilişki) aileden · **yabancıya tavrı**. Her ölçekte iki özellik; büyük kampanyalar zenginliği daha çok halktan alır (P3, P5).

**Soy (15):** insan (en yüksek ağırlık) · cüce (yeraltı, dağ) · elf (orman) · buçukluk (ova, nehir) · gnom (yeraltı, zanaat) · yarı-elf, yarı-ork (karışık soylar) · ejderdoğan (ejderha satırlarıyla) · tiefling (düzlem satırlarıyla) · dev soyu (oynanamaz; dağ) · deniz halkı, merfolk (oynanamaz; kıyı) · kertenkele halkı, lizardfolk (oynanamaz; bataklık) · kentaurlar (oynanamaz; bozkır) · goblin ya da kobold halkı (oynanamaz; kötü değil, bir kültür) · fey halkı (oynanamaz; büyü low ve üstü) · karışık halk (kanla değil kültürle tanımlanan). Soy oynanamazsa oyuncunun karakteri bu halkın arasında büyümüş olabilir.

**1. Beden** (görünen)

| Özellik | Masada |
|---|---|
| tenleri yaşadıkları toprağın rengini alır | bir yabancıyı ilk bakışta tanırlar |
| yaşlandıkça boynuzları uzar; boynuz yaşın ve saygının ölçüsüdür | boynuzu kırılan biri onurunu kaybetmiştir |
| kırılmadan beri gölgeleri yok | gölgesi olan her yabancı dikkat çeker |
| her kış bir mevsim boyu uyurlar; uyanık kalanlar köyü korur | kışın köyler savunmasızdır |
| suyun altında bir süre nefes alabilirler | sualtı yolları yalnızca onlarla açılır |
| soğuğu hissetmezler | kışın dağ yolları yalnızca onlarla geçilir |
| bedenleri can damarının izini taşır (bakırcıların yeşil tırnakları, ipekçilerin ipek gibi saçları) | kimin nereden geldiği bedeninden okunur |
| kırk yılda ihtiyarlarlar, her şeyi erken ve hızlı yaparlar | liderleri gençtir, sabırsızdır |

**2. Âdet** (davranan)

| Özellik | Masada |
|---|---|
| misafir üç gün kutsaldır; dördüncü gün gitmeyen düşman sayılır | parti üç gün dokunulmazdır |
| yetişkin olunca adlarını değiştirirler; çocukluk adını yalnızca aile bilir | birinin çocukluk adını bilmek büyük bir güçtür |
| kimse kendi sofrasında yemez; her akşam başka bir evde yenir | her akşam yeni bir ev, yeni bir söylenti |
| pazarlık bir sanattır; fiyatı ilk söyleyen utanır | alışveriş bir sosyal karşılaşmaya döner |
| önemli kararlar bir yarışla verilir (at, kürek, tırmanış) | parti bir tarafın yarışçısı olabilir |
| yabancıya yüzlerini göstermezler; maske ya da peçe takarlar | kimin kim olduğu belirsizdir |
| tarihlerini şarkıyla değil dansla anlatırlar | bir ipucu bir dansın içinde saklıdır |

**3. Bir canlıyla bağ** (görünen)

| Özellik | Masada |
|---|---|
| her çocuk bir yavru hayvanla birlikte büyür; ikisi aynı gün yetişkin sayılır | hayvanına zarar veren kişiye zarar vermiş olur |
| sürüleriyle aynı rüyayı görürler; sürü tehlikeyi rüyada haber verir | baskını önceden bilirler |
| dev kuşlarla birlikte uçarlar (büyü medium ve üstü) | haberleri ve baskınları havadan gelir |
| arılarla konuşurlar; kovana bir meclis gibi danışılır | kovanın kararı köyün kararıdır |
| dev böcekler hem evleri hem gemileridir (büyü medium ve üstü ya da yeraltı) | köy yer değiştirebilir |
| kurtlarla birlikte avlanırlar; av kurtla paylaşılmazsa uğursuzluk gelir | ormanda kurtlar onların gözüdür |
| balıkçılığı yunuslarla birlikte yapar, işaretle anlaşırlar | denizde yalnız değillerdir |

**4. İnanç** (davranan)

| Özellik | Masada |
|---|---|
| kırılmayı bir ceza sayar, kefaretini ödemeye çalışırlar | kırılmaya karşı çıkana düşman olurlar |
| kırılmayı bir armağan sayar, onu büyütmek isterler | kırılmayı durdurmak isteyenlere direnirler |
| dünyanın bir gün tersine dönüp başa geleceğine inanırlar | her şeye bir döngünün işareti olarak bakarlar |
| her dağın bir ruhu olduğuna, dağa sormadan kazılmayacağına inanırlar | maden açmak bir pazarlık gerektirir |
| tanrılara değil can damarına taparlar (nehre, sürüye, madene) | damara dokunmak kutsala dokunmaktır |
| yalanın havayı bozduğuna inanırlar; yalan söyleyen fırtına getirir | fırtına çıkınca bir suçlu aranır |
| demirin uğursuz olduğuna inanırlar; aletleri taştan, kemikten ve bronzdan yaparlar | demir silahlı yabancıya güvenilmez |

**5. Toplumsal düzen** (davranan)

| Özellik | Masada |
|---|---|
| yöneticilerini ustalık yarışmalarıyla seçerler | lider olmak için bir şey yapmak gerekir |
| her karar herkesin önünde, açık havada alınır; kapalı kapı ardında karar yoktur | gizli anlaşmalar büyük bir suçtur |
| en gençler yönetir; kırkını geçen danışman olur | liderler cesur ama deneyimsizdir |
| aileler yerine atölyeler vardır: çocuk öğrendiği zanaatın adını taşır | birinin ustası onun ailesidir |
| biri barışta, biri savaşta olmak üzere iki başkanları vardır | savaş ilan edilince yönetim el değiştirir |
| kimse bir yerde yedi yıldan fazla kalmaz; köyler dönüşümlü yer değiştirir | bir yeri tanıyan kimse kalmamıştır |
| dışarıyla yalnızca köyün yabancı elçisi konuşur | her kapı bir elçiden geçer |

**6. Kırılmayla ilişki** (davranan)

| Özellik | Masada |
|---|---|
| kırılmadan önceki dünyayı hatırlayan tek halktır | geçmişin bilgisi onlardadır |
| kırılmanın dönüştürdüğü ilk kuşaktır (yeni halk yarasıyla birleşir) | eski halk onlardan korkar |
| kırılmanın yarasını bedenlerinde taşırlar | yaraya en yakın onlardır |
| kırılmadan kaçıp buraya gelmişlerdir; eski yurtları yaranın içinde kaldı | geri dönmek isterler |
| kırılmayı önceden sezip hazırlanmışlardır; şimdi en güçlü onlardır | neyi nasıl bildikleri merak edilir |
| kırılmadan kazananlardır, bu yüzden sevilmezler | kıskançlığın hedefidirler |
| kırılmanın olduğu yeri kutsal sayar, kimseyi yaklaştırmazlar | kırılmanın kalbine giden yol onlardan geçer |

**7. Yer ve hareket** (görünen)

| Özellik | Masada |
|---|---|
| hiç durmazlar; sürüleriyle, sallarıyla ya da kervanlarıyla hep yoldadırlar | onları bulmak bir arayış olur |
| dikey yaşarlar; evleri yamaçlara ve uçurumlara oyulmuştur | köyleri tırmanılarak gezilir |
| gündüz yeraltında, gece yüzeyde yaşarlar | gündüz köyleri boş görünür |
| suyun üstünde yaşarlar: yüzen köyler, kazık üstünde evler | köye kayıkla girilir |
| ağaçların tepesinde yaşarlar; yere inmek bir törendir | yerde karşılaşılırlarsa bir sebebi vardır |
| mevsime göre iki yurt arasında göç ederler (yazın yayla, kışın ova) | aynı köy yarım yıl boştur |
| tek bir büyük yapının içinde yaşarlar (dev bir kale, bir kazı, bir gemi) | halkın evi aynı zamanda bir zindandır |

**Yabancıya tavrı (6):** misafirperver ve meraklı (kapılar açık, sorular çok) · tüccar (yabancı bir alışveriş fırsatıdır) · temkinli (yabancı önce sınanır) · kapalı (yalnızca tek bir kapıdan konuşulur) · nedenli bir düşmanlık (geçmişte yaşanmış bir şey yüzünden) · ikiye bölünmüş (yarısı açık, yarısı kapalı).

**Vaadi:** P3 yerleşimler ve bölge · P4 çekişmede bir halk rolü varsa o rol · P5 bu halktan NPC'ler, iki özellik görünür · P6 bu halka ait bir mekân · P8 primerin kültür bölümü · P9 oyuncunun karakteri bu halktan olabilir ya da aralarında büyümüş olabilir.

**Kurallar:** atılan eski satırlar: ölülerini çalan halk, ölümsüz memurlar, haraç toplayan devler, fener balıkları, mumdan çocuklar, hesap tutan kargalar, tuz yürüyenleri, ışığa gelen güveler, büyü izi süren tazılar, adını veren halk (taşlaşan halk dry-4'te kullanıldı). Doğuştan kötü halk yok (hiçbir soy hizalanmayı sabitlemez). Başka bir kampanyanın çektiği özellik satırı bir daha çekilmez; soy ve tavır tekrar edebilir, bir önceki doğumun halkıyla aynı soy bir doğum bekler.

## 9. Kurum imzası

Kuruluş: **ev** çekişmenin rollerinden biri (zar; halk bir rolü aldıysa başkası) · **biçim** (rolün arketip ipucundan ağırlık) · **uygulama** (davranan: başka kimsenin yapmadığı iş) · **işaret** (görünen) · **güç kaynağı**. Tek uygulama, kampanyada tek kurum imzası; diğer kurumlar P4'te faksiyon olarak gelir.

**Biçim (14):** tarikat · lonca · bölük · hane (bir aile) · meclis · birlik · okul · kardeşlik · manastır · gezgin topluluk (kervan, filo, tiyatro) · gizli cemiyet (kötü değil) · beratlı şirket · boylar birliği · milis. Ağırlık: devlet → meclis, hane · din → tarikat, manastır · askerî → bölük, tarikat, milis · lonca → lonca · ticaret → şirket, birlik · bilgin → okul · suç → gizli cemiyet · direniş → kardeşlik, milis.

**Uygulama (8 aile, 40)**

| Aile | Uygulama | Partiye ne verir |
|---|---|---|
| Koruma | omurganın kilit yerini tutarlar (geçit, köprü, boğaz) | geçiş izni, oradaki görevler ve düşmanlar |
| Koruma | tek yolun bekçileridir | kervan korumaları, yol haritaları |
| Koruma | suru yapan ve tutan ustalardır | sur ötesine seferler, onarım görevleri |
| Koruma | kalıntının kapısını tutarlar | kalıntıya girmenin tek yasal yolu |
| Koruma | sürüleri ve göç yollarını korurlar | avcılara ve hırsızlara karşı görevler |
| Taşıma | haberi ve tarihi oyunlarla taşıyan gezgin tiyatrodur | söylentiler, kılık değiştirme, halkın nabzı |
| Taşıma | tehlikeli sularda ve yollarda kılavuzluk ederler | rehberler, yol bilgisi |
| Taşıma | dev kuşlarla ya da hızlı atlarla haber taşırlar | mektuplar, yetiştirilmesi gereken acil işler |
| Taşıma | kervanları düzenlerler | kervan işleri, uzak ülkelerle bağlantı |
| Taşıma | nehrin ya da boğazın salcıları ve kayıkçılarıdır | geçiş, kaçakçılık söylentileri |
| Yapma | eski krallığın yapılarını (sarnıçlar, yollar, kuleler) onarıp çalışır tutarlar | kalıntılara giriş, eski bilgiler |
| Yapma | golem ve makine dökerler | koruyucu yapılar, bozulan makineler |
| Yapma | can damarının eşsiz zanaatını yaparlar (ünlü çelik, cam, halı) | eşsiz eşyalar, ustanın sırrı |
| Yapma | gemi ve köprü yaparlar | gemi, köprü, yapım sırasında sabotaj |
| Yapma | kırılmanın yarasını onarmaya çalışırlar | yaranın içine seferler |
| Bilme | harita çizer ve saklarlar | haritalar, yasak topraklar |
| Bilme | kalıntıyı incelerler | kazı görevleri, eski yazıların çözülmesi |
| Bilme | kaybolanı ararlar (kayıp bir bilgi ya da zanaat) | arayış görevleri |
| Bilme | ölmekte olanı saklarlar (tohumlar, türler, şarkılar) | koruma ve toplama görevleri |
| Bilme | gökyüzünü izlerler | göğün işaretleri, yaklaşan kırılmanın haberi |
| Bakım | kırılmanın yetimlerini büyütürler | yetimler, kayıp çocuklar, geçmişin sırları |
| Bakım | şifacıdırlar | iyileşme, salgın görevleri |
| Bakım | kıtlıkta halkı besleyen ambarları tutarlar | ekinin dağıtımı, kıtlığın siyaseti |
| Bakım | ebedirler, doğumları gözetirler | doğan çocukların işaretleri |
| Bakım | sürüleri ve binekleri iyileştirirler | sürü hastalığı görevleri |
| Savaş | canavar avcılarıdır | av sözleşmeleri, canavar bilgisi |
| Savaş | sınırın ve kalelerin süvarileridir | sınır görevleri |
| Savaş | savaşın yerine teke tek dövüşen şampiyonlardır | düellolar; parti bir tarafın şampiyonu olabilir |
| Savaş | paralı bir bölüktür | iş, rakipler, bozulan sözleşmeler |
| Savaş | ejderha ya da dev avlarlar | büyük av, ejderhanın hazinesi |
| Ticaret | kraliyet beratıyla bir malın tekelini tutarlar | ticaret görevleri, tekelin düşmanları |
| Ticaret | kalıntıdan çıkan eşyaları satarlar | hazine, sahte eserler |
| Ticaret | can damarının ürününü tek elden satarlar | pazar, kaçakçılar |
| Ticaret | uzak ülkelerle takas yapan yabancı bir tüccar evidir | yabancı mallar, casusluk |
| Ticaret | yarı gizli bir kaçakçılar birliğidir | kaçak yollar, yasa dışı işler |
| İnanç | can damarını ayakta tutan ayini yaparlar (her bahar nehri yola getiren ayin gibi) | ayin bozulursa her şey bozulur |
| İnanç | hacıları kutsal yere götürürler | hac yolu görevleri |
| İnanç | kutsal yeri korurlar | kutsal yerin sırları |
| İnanç | kırılmayı yorumlayıp ona taparlar ("yeni bir inanç" yarasıyla birleşir) | yeni inancın müritleri ve düşmanları |
| İnanç | terk eden tanrının boş tapınaklarında hâlâ ibadet ederler | tapınak labirentlerine giriş |

**İşaret (18):** yüzlerine ya da ellerine bir işaret boyarlar · hep tek bir renk giyerler · bir hayvan maskesi takarlar · mesleklerinin aletini hep üstlerinde taşırlar (bir anahtar, bir çekiç, bir halat) · giriş töreninden kalan bir yara izi taşırlar · yanlarında hep bir hayvan taşırlar (bir şahin, bir kertenkele) · silah taşımazlar · evlenmezler, aileleriyle bağlarını keserler · yalnızca ikişer ikişer yolculuk ederler · toprak sahibi olamazlar · hiçbir hükümdarın önünde diz çökmezler · kurumlarına bir kez giren bir daha çıkamaz · kazançlarının yarısını halka dağıtırlar · gece yolculuk etmezler · yalnızca kendi dillerini konuşurlar, dışarıyla tercümanla anlaşırlar · saçlarını hiç kesmezler · her üye bir sır taşır ve ölene dek saklar · yılda bir kez bütün üyeler kalpte toplanır.

**Güç kaynağı (10):** tekel (vazgeçilmezlik) · yer: kilit yeri ya da kalıntıyı tutarlar (bir mekân varlığı) · bilgi: yolu, haritayı ya da bir sırrı bilirler (casusluk, pazarlık) · silah (askerî güç) · halkın sevgisi (isyan ya da destek) · kutsallık (dokunulmazlık) · hazine (satın alma) · bir yaratıkla bağ (beklenmedik güç) · berat: bir hükümdardan yazılı bir hak (yasal dayanak) · korku (yıldırma).

**Vaadi:** P3 merkezi bir yerleşimde · P4 çekişmedeki rolün faksiyonu kurumun kendisi; güç kaynağı varlıklarını, uygulaması hizmetlerini belirler · P5 önderi ve üyeleri, işaret görünür · P6 tuttuğu ya da koruduğu bir mekân · P7 uygulamasından doğan görevler · P8 yerlilerin bildikleri.

**Kurallar:** atılan eski satırlar: ölüleri okuyan tarikat, geçiş ücreti, bağlı mahkeme, lamba yakıcılar, sayım dairesi, sessizlik tarikatı, gelgit nöbeti, para olmayan bir şeyin pazarı, misafirlik yasasının bekçileri, ölülerin haklarının bekçileri, gerçeği tartanlar, yasayı tutan koro, defter evi. Kötü tarikat yok; gizli cemiyet varsayılan olarak kötü değildir, inanç kurumları meşru taraflardır. Başka bir kampanyanın çektiği uygulama satırı bir daha çekilmez; biçim, işaret ve güç tekrar edebilir.

## 10. Olgu imzası

Kuruluş: **ev** yıkıntı kaynağının tuhaflığı (yara "büyünün bir kuralı değişti" ise o kural; kural 8. aileden çekilir) · **kural** (davranan) · **belirti** (görünen) · **sınır** · **kim kullanır** (diğer iki imzaya bağlanabilir).

**Kural (8 aile, 40)**

| Aile | Kural | Masada |
|---|---|---|
| Büyünün davranışı | her büyü saatlerce orada kalan ve okunabilen bir yankı bırakır | gizlice büyü yapılamaz; iz süren biri bulur |
| Büyünün davranışı | sert bir yüzeye çarpan büyü geri dönebilir | taşın ve camın yakınında büyü risklidir |
| Büyünün davranışı | büyünün unsuru ters döner: ateş dondurur, buz yakar | düşmanın dirençleri ters işler |
| Büyünün davranışı | her büyü çevresinde bitki ve küçük canlılar büyütür | büyü yapılan savaş alanı ormana döner |
| Büyünün davranışı | her büyünün uzakta bir yerde bir ikizi olur | başka bir yerde istenmeyen bir etki doğar |
| Beden ve kan | bir topluluk yaralarını paylaşır | birini yaralamak herkesi yaralar |
| Beden ve kan | kalıntının yakınında uzun yaşayanlar yavaş yavaş değişir | uzun kalan partide işaretler belirir |
| Beden ve kan | hayvanlar yalanı sezer, yalancıya yaklaşmaz | at ve köpek bir yalanı ele verir |
| Beden ve kan | kan bağı büyüyü güçlendirir; bir akrabanın büyüsü iki kat işler | aileler güçlü, akraba düşman tehlikeli |
| Beden ve kan | her büyü, yapanın teninde bir iz bırakır | kimin ne kadar büyü yaptığı bedeninden okunur |
| Yer ve yol | büyü görünür yollar boyunca akar | yolların kesiştiği yerler değerli ve çekişmeli |
| Yer ve yol | aynalar belli koşullarda kapıdır | kaçış ve baskın yolları |
| Yer ve yol | yollar yürüyeni istediği yere değil, gitmesi gereken yere götürür | yolculuk bir yön arayışına döner |
| Yer ve yol | mesafeler gece değişir; gece yolculuğu kısa da sürebilir uzun da | gece yürüyüşü bir kumar |
| Yer ve yol | bazı kapılar her açılışta başka bir yere açılır | kapılar bir harita olur |
| Madde | kalıntının maddesi (cam, taş, kemik) büyüyü emer | o maddeden zırh büyüye karşı korur |
| Madde | bir taş ağırlığını kaybeder, havada durur | uçan yapılar, düşen şeyler |
| Madde | su bir kez aktığı yolu hatırlar ve oraya geri döner | su yönlendirilebilir, kuruyan yataklar geri gelir |
| Madde | metal bir ustanın elinde canlanır | dökülen şeyler kendiliğinden kıpırdar |
| Madde | ateş yaktığı şeyin şeklini dumanında gösterir | duman okunur, iz sürülür |
| Zaman | kalıntının yakınında zaman farklı akar | içeride bir gün, dışarıda bir hafta |
| Zaman | olacak bir şeyin gölgesi önceden düşer | pusu ve tuzak önceden sezilebilir |
| Zaman | belli bir yerde bir an her gün yeniden yaşanır | tekrar eden an bir bilmecedir |
| Zaman | büyüler geç tutar; etkisi bir süre sonra gelir | büyü bir plan gerektirir |
| Zaman | büyü, yapanı yaşlandırır | büyücüler yaşlarından yaşlı görünür |
| Söz ve işaret | birinin gerçek adını bilen ona emredebilir | adlar saklanır (halkın "çocukluk adı" âdetiyle birleşebilir) |
| Söz ve işaret | doğru çizilen her işaret küçük bir büyüdür | duvarlarda işaretler, herkeste biraz büyü |
| Söz ve işaret | büyü sözle değil hareketle yapılır; eli bağlı biri büyü yapamaz | büyücüyü susturmak değil, bağlamak gerekir |
| Söz ve işaret | bir halkın dili büyünün dilidir; onu konuşan küçük büyüler yapar | dil öğrenmek güç kazanmaktır |
| Söz ve işaret | ad konan bir yer yavaş yavaş adına benzer | yer adları bir silahtır |
| Doğa ve canlılar | güçlü bir duygu havayı değiştirir | öfkeli bir kalabalık fırtına getirir |
| Doğa ve canlılar | canavarlar büyünün kokusuna gelir | her büyü bir karşılaşma riskidir |
| Doğa ve canlılar | mevsimler bir canlıya bağlıdır; dev bir hayvanın uykusu kışı getirir | o canlıya dokunmak mevsimi bozar |
| Doğa ve canlılar | toprak can damarını korur; damara zarar veren toprağın öfkesiyle karşılaşır | doğa bir taraf olur |
| Doğa ve canlılar | gölgeler kendi başına hareket eder | bir gölge casus olabilir |
| Kırılmadan doğan | kırılmadan beri büyü tek yönde çalışır (kalpten dışarı ya da yukarıdan aşağı) | nerede durduğun, ne yapabileceğini belirler |
| Kırılmadan doğan | her büyü kırılmayı biraz daha büyütür | büyücüler sorumlu tutulur |
| Kırılmadan doğan | kırılmadan beri bazı insanlar büyüyle doğuyor | yeni yeteneklilerden korkulur |
| Kırılmadan doğan | büyü kırılmanın hedefine yakınken güçlü, uzakta zayıf | gücün bir coğrafyası olur |
| Kırılmadan doğan | her büyünün yarısı başka bir yerde çıkar | büyü tam kontrol edilemez |

**Belirti (16):** havada bir renk · bir koku (ozon, bakır, yanık şeker) · bir uğultu ya da çıtırtı · yerde bir titreşim · camda ve suda kırağı desenleri · bedende işaretler · hayvanların huzursuzluğu · pusulaların sapması · geç kalan yansımalar · ters düşen gölgeler · durgun suda halkalar · bitkilerin bir yöne eğilmesi · ağızda metal tadı · dikleşen saçlar · havada asılı kalan toz · ani bir serinlik.

**Sınır (12):** demir onu keser · akan suyu geçemez · kalıntıdan bir günlük yolun ötesinde biter · yalnızca yeraltında işler · uyuyanlara işlemez · ateş onu dağıtır · soğukta güçlenir, sıcakta zayıflar · yüksekte güçlenir, alçakta zayıflar · bir soyun kanı ona karşı koyar (halk imzasına bağlanabilir) · kurumun işareti onu durdurur (kurum imzasına bağlanabilir) · kalıntının maddesi onu emer · bir kez tetiklenince bir gün bekler.

**Kim kullanır (8):** herkes · kimse, olgu kendiliğinden olur · yalnızca imza halkı · yalnızca imza kurumunun eğitimlileri · yalnızca kırılmanın dokundukları · yalnızca çocuklar · yalnızca büyücüler · yalnızca o toprakta doğanlar.

**Kadran:** büyü low → 1, 6 ve 8. ailelerin ağırlığı düşer; medium ve high → hepsi açık (none yok). İmza mekaniği ölçeğin zarına bağlı kalır; short'ta çıkmaz, çıkarsa bu kuralın üstüne kurulur.

**Vaadi:** P2 büyü sistemi bu kuralla tutarlı · P3 kuralın güçlü ve zayıf olduğu yerler · P5 onu kullanan NPC'ler · P6 kuralın en güçlü olduğu mekân, sınamaları kuralı kullanır · P8 yerlilerin bildikleri · masada DM kuralı dövüşte ve yolculukta uygular.

**Kurallar:** atılan eski satırlar: maddede yaşayan anı, gelgit büyüsü, günah çıkarma bedeli, kan defteri, "hush" bölgeleri, bir saatliğine görünen ölüler, sesi saklayan taş, rüya sızıntısı. Zamana kilitli doğaüstü saatler yok (dry-1'in Wakelight'ı, dry-3'ün Nightwake'i). Hiçbir satır büyüye sahip olmayı ya da onu satmayı anlatmaz. Başka bir kampanyanın çektiği kural satırı bir daha çekilmez; belirti, sınır ve kullanan tekrar edebilir.

## 11. Soru (tension)

Kuruluş: **ev** çekişme (zarın ağırlığı çekişmenin ailesinden) · çekişmenin A ve B tarafları sorunun iki kutbunu taşır (yazar atar, kapı ikisinin de kutup taşıdığını denetler) · kötü bir kutbu korkunç uç noktasına taşır (gizli zar, #22) · soru sayısı çekişme sayısına eşit: short ve standard 1, epic 2 (`scale.yaml` `tensions`, bugün [1, 2], buna göre değişir; d2 ile ikinci soru zarı kalkar) · soru tırmanışla büyür: her basamak soruyu kendi ölçeğinde sorar (P7'ye söz) · yazar soyut kutbu kampanyanın terimleriyle somut bir soruya çevirir. **Tabloda örnek soru yok** (örnekler doğumları kendine çeker); YAML'da yalnızca kutuplar ve aile ağırlıkları.

Aileler: 1 Aynı şeye iki el · 2 Eski ve yeni · 3 Güçlü ve zayıf · 4 Açanlar ve kapayanlar · 5 Yarış · 6 Kardeş kavgası · 7 İnsan ve insan-dışı · 8 Görünmeyen el.

| # | Kutuplar | Aileler |
|---|---|---|
| 1 | miras ve özgürlük | 2, 6 |
| 2 | düzen ve merhamet | 3, 8 |
| 3 | bilgi ve akıl sağlığı | 4 |
| 4 | inanç ve kanıt | 2, 4 |
| 5 | güç ve benlik | 3, 5 |
| 6 | hatırlamak ve kurtulmak | 2, 6 |
| 7 | sadakat ve gerçek | 6, 8 |
| 8 | ilerleme ve bedeli | 2, 4 |
| 9 | hayatta kalmak ve onur | 1, 3 |
| 10 | adalet ve barış | 3, 6 |
| 11 | ait olmak ve dönüşmek | 2, 7 |
| 12 | görev ve arzu | 5, 6 |
| 13 | doğa ve egemenlik | 1, 7 |
| 14 | gizlilik ve açıklık | 4, 8 |
| 15 | intikam ve bırakmak | 3, 6 |
| 16 | saflık ve karışım | 2, 7 |
| 17 | kalıcılık ve değişim | 2 |
| 18 | bir kişi ve çoğunluk | 1, 3 |
| 19 | hırs ve kanaat | 5 |
| 20 | misafirlik ve kuşku | 2, 7 |
| 21 | fedakârlık ve değer | 3, 5 |
| 22 | yasa ve vicdan | 3 |
| 23 | doğuştan hak ve emekle hak | 1, 5 |
| 24 | ustalık ve hayret | 4, 7 |
| 25 | yurt ve ufuk | 2, 4 |
| 26 | affetmek ve hesap sormak | 2, 6 |
| 27 | beden ve ruh | 4, 7 |
| 28 | son ve devam | 2, 4 |
| 29 | güvenlik ve özgürlük (yeni) | 3, 4 |
| 30 | umut ve gerçek (yeni) | 4, 8 |
| 31 | kan bağı ve seçilmiş aile (yeni) | 6, 7 |
| 32 | sahip olmak ve paylaşmak (yeni) | 1, 5 |
| 33 | kazanmak ve haklı olmak (yeni) | 5, 8 |

Atılanlar: sessizlik ve tanıklık, borç ve lütuf. Yasa ve vicdan, adalet ve barış, affetmek ve hesap sormak kalır (mahkeme artık kurumda da çekişmede de yok).

**Vaadi:** P4 her tarafın öğretisi kendi kutbunu taşır, ilişkilerin gerekçeleri sorudan gelir · P5 NPC'ler soruda bir yerde durur, kötünün cevabı dm-only · P7 sonlar sorunun olası cevaplarıdır, her basamak soruyu kendi ölçeğinde sorar · P8 primer yerlilerin soruyu nasıl tartıştığını anlatır · P9 her oyuncu karakterinin hikâyesi soruya bir yerden dokunur.

**Kurallar:** başka bir kampanyanın çektiği kutup satırı bir daha çekilmez. "Hükümdarlar kurayla seçilir" trope break'i ile "doğuştan hak ve emekle hak" birlikte çıkmaz.

## 12. Trope break

Kuruluş: **bağ** (zar: can damarı, yıkıntı, çekişme, kırılma, halk, kurum ya da olgu; yazar tersine dönen kuralı o parçayla açıklar, kapı bağın kimliğini denetler) · yara "yeni bir yasak ya da tabu" ise trope break'lerden biri yasak satırlarından (haritalar yasak, silah yasağı) · sayı: short 1, standard ve epic 2, ikisi farklı ailelerden. Tutulan satırlar mevcut yükümlülüklerini (P2, P3, P5, P6 `hooks`) taşır; yeni satırlara inşada aynı biçimde yazılır; hepsi söz defterine girer.

| Aile | Trope break | Masada |
|---|---|---|
| Yönetim ve güç | hükümdarlar kurayla seçilir | her kura bir siyasi kriz |
| Yönetim ve güç | lordlar yoktur; loncalar yönetir | güç, zanaat ve para demek |
| Yönetim ve güç | savaşları ordular değil şampiyonlar yapar | parti bir ülkenin şampiyonu olabilir |
| Yönetim ve güç | (yeni) silah taşımak yalnızca bir sınıfa açıktır | silahlı bir parti ya ayrıcalıklıdır ya suçlu |
| Yönetim ve güç | (yeni) büyü soyluluktur; büyüsüz soylu yoktur | büyücü bir PC doğuştan bir statüye sahiptir |
| Yönetim ve güç | (yeni) ülkeleri ejderhalar yönetir | hükümdarla konuşmak bir ejderhayla konuşmak demek |
| Halklar ve canlılar | elfler geçen yüzyıl geldi | elfler yeni, yabancı ve kuşkuyla karşılanan bir halktır |
| Halklar ve canlılar | devler köylüdür; toprağı onlar işler | devler dost, hatta işveren olabilir |
| Halklar ve canlılar | canavarların antlaşmaları vardır | her canavar karşılaşması önce bir pazarlıktır |
| Halklar ve canlılar | hayvanlar konuşur ve toprak sahibidir | ormanın bir sahibi, bir sözü vardır |
| Halklar ve canlılar | (yeni) insanlar azınlıktır; dünya başka soyların | insan bir PC yabancıdır |
| Halklar ve canlılar | (yeni) soyların yurtları alışılmışın tersidir (cüceler denizci, elfler bozkır göçebesi) | beklenti her soyda bozulur |
| Halklar ve canlılar | (yeni) dünyanın tüccarları goblinlerdir | her pazar onlarındır |
| Tanrılar ve gök | tanrılar tapınma değil tanık ister | bir mucizeyi görmek bir görevdir |
| Tanrılar ve gök | tanrıların ölümlü ataların ruhları olduğunu herkes bilir | din bir aile işidir |
| Tanrılar ve gök | ayda yaşayanlar vardır ve ticaret yaparlar | gökten gelen mallar ve yabancılar |
| Tanrılar ve gök | (yeni) tanrıların büyüsü yalnızca kutsal yerlerde işler | rahip bir PC kutsal yerden uzaklaştıkça güç kaybeder |
| Tehlikenin yeri | gece güvenli, gündüz tehlikelidir | yolculuk ve baskın gece yapılır |
| Tehlikenin yeri | (yeni) şehirler tehlikeli, vahşi doğa güvenlidir | sığınak ormandır, tuzak şehir |
| Tehlikenin yeri | (yeni) zindanlar boş değildir; her harabe birilerinin evidir ve kapısı çalınır | zindana girmek önce bir ziyarettir |
| Tehlikenin yeri | (yeni) büyük bir canavarı öldüren onun yükünü devralır | zafer bir bedel getirir, öldürmek bir karardır |
| Zaman ve tarih | dünya genç; yazılı tarih üç yüz yıllık | kadim sırlar yok, yakın geçmişin sırları var |
| Zaman ve tarih | eski düşman kazandı ve herkes iyi | "kötülerin" dünyası sıradan bir dünyadır |
| Zaman ve tarih | yılda bir ay büyü çalışmaz | büyücüler o ay için hazırlanır |
| Bilgi, madde ve yaşam | demir kutsal ve nadirdir | demir silah bir hazinedir |
| Bilgi, madde ve yaşam | haritalar yasaktır | yol bilgisi en değerli şeydir |
| Bilgi, madde ve yaşam | doğumlar nadirdir ve herkesin önünde olur | her çocuk bir olaydır |
| Bilgi, madde ve yaşam | (yeni) kimse doğrudan yalan söyleyemez; herkes lafı dolandırır | her konuşma bir bilmecedir |
| Bilgi, madde ve yaşam | (yeni) yazı bilinmez; bilgi ezberde taşınır, söz el sıkışmaktır | tanıklar ve ezberciler değerlidir |

**Atılan 25 satır:** ölüler (ölüler uygar olanlar, ölülerin oyu, sıradan diriliş, hatırlanan yeniden doğuş, öbür dünya yok) · para ve defter (yıllarla ödenen borç, iblislerin bankaları, tanrıların darp ettiği para, satılan anılar, satılan adlar, yazı tekeli) · mahkeme ve yasa (tanrılar yargılanıyor, yasa bir şarkı) · ışık (güneş yeni yakıldı) · büyü bir meta (hava bir kaynak, büyü bir kamu hizmeti) · temelle ya da imzalarla çakışan (kara bir halka, şehir devletleri ve tek yol, hareket eden başkent, yürüyen orman, yıldızlar yok, kimse yaşlılıktan ölmez, hastalar büyücü, yarayı taşıyan iyileştirme, ejderha kemiğinden para).

**Kurallar:** kurayla hükümdar ile "doğuştan hak ve emekle hak" birlikte çıkmaz; "tanrılar ataların ruhları" ile sır "tanrılar insandı" birlikte çıkmaz. Goblinler kötü değil; ejderha hükümdarlar bir kara kule efendisi değil; "eski düşman kazandı" `forbidden_monolithic_empire`'ın tek istisnası. Başka bir kampanyanın çektiği satır bir daha çekilmez.

## 13. Çakışmaların hakemi: script (owner ruling 2026-09-28)

Model hiçbir tablo kuralının hakemi değildir.
1. **Çakışma veridir.** Her satır `conflicts_with` (birlikte çıkamayacağı satırlar, başka tablolardan da) ve `requires` (çıkması için şart: "palette ince yer", "büyü high", "yeraltı") taşır. Tablolarda "ağır" diye yazılanlar ağırlıktır, "gerekir" ya da "yalnızca" diye yazılanlar şarttır.
2. **İki yönlü:** tablo okunurken çakışmalar simetrik yapılır; A B'yi yasaklıyorsa B de A'yı yasaklamış sayılır.
3. **Havuz zardan önce süzülür:** başka kampanyada kullanılmış, o ana kadar atılmış herhangi bir zarla iki yönden biriyle çakışan ve şartı sağlanmayan satırlar çıkarılır, zar sonra atılır. "Atıp beğenmezsen yeniden at" kalkar.
4. **Havuz boşalırsa durur:** preroll hata verir, doğum başlamaz; asla "yine de tut" demez.
5. **Her dışlama kayda geçer:** zar kaydı dışlanan satırı ve nedenini yazar.
6. **Kapı son kez denetler:** öncül kayıt olurken çekilen bütün satır kimlikleri çakışma listesine karşı yeniden denetlenir.
7. **Test:** model kullanmayan bir test binlerce tohumla bütün P1 zarlarını atar ve tek bir çakışan set çıkmadığını kanıtlar.
8. **Yazının kendi çelişkileri:** satırlar tersine dönen kuralın "asla" cümlelerini taşır; kelimeyle yakalanabilenleri kapı yakalar (`forbidden.yaml`'ın kelime kalıpları gibi), kalanında eleştirmen her söz için bir hüküm yazar ve kararı söz defteri ile kapı verir.

Bugün bulunan iki delik (aynı iş kaleminde kapanır): `designer.py` `table_until` sekiz denemeden sonra çakışan satırı sessizce tutuyor; trope break çekilirken adayın kendi `conflicts_with` listesi daha önce atılmış zarlarla (soru) karşılaştırılmıyor, bu yüzden "kurayla hükümdar" ile "doğuştan hak ve emekle hak" bugün birlikte çıkabilir.

İnşada her tablonun çakışma ve şart listesi satırlar gibi sahibine onaylatılır.

## 14. Sır — yalnızca yapı (owner ruling 2026-09-28: the development tab builds the rows; the owner, who is also the player, does not see them)

**Ev: kırılma.** Sır kırılmanın gerçek nedenidir: neden oldu, kim seçti. Her kırılmanın arkasındaki yaşayan birinin kararını sır taşır.

Dört parça, hepsi gizli zar, satırlar dm-only:
- **Arketip** (gerçekte neler oluyor): bugünkü 24 satırdan çekim alanındaki 2'si çıkar; temelde zaten açık olan bir şeyi sır yapan satırlar çakışma kuralıyla dışlanır (ör. yıkıntı "hapsedilmiş tanrı" ise "tanrılar tutsak" sır olamaz); ağırlık kırılmanın eyleminden ve zamanından gelir.
- **Seçen** (yeni): kırılmayı kim seçti: kötü, çekişmenin bir rolü, imza kurumu, imza halkı, sıradan biri (ölmüş ya da unutulmuş) ya da bir güçle pazarlık eden bir ölümlü. Seçen her zaman bir kişidir.
- **Dönüş** (twist): bugünkü 12 satır kalır; 3 yeni: seçen ne yaptığını bilmiyordu; seçen şimdi geri almaya çalışıyor; halk sırrı biliyor ama kimse inanmıyor.
- **İz** (trail): çekim alanındaki 1 satır çıkar; yaklaşık 10 satıra çıkar (ör. iz, yara ve hayatta kalan; nesne, yapan ve sahibi; av izi ve in; ele geçirilen mektup ve hain).

**İpuçları ve tırmanış:** ipuçları perde perde açılır, son ipucu tırmanışın en üst basamağındadır. Her ipucunun yeri (NPC, mekân, yerleşim) söz defterine vadeli söz olarak girer; dry-4'ün "`clue_unplaced` ama kapı açık" durumu kapanır.

**Vaadi:** P2 sırrın bağlandığı tanrı ve kırılmanın tarihli olayı · P5 ve P6 ipuçlarını taşıyanlar · P4 sırrı bilen faksiyon (dönüş öyleyse) · P7 sonlar sırrın açılmasına göre dallanır (geri alınabilir ya da alınamaz) · kart yalnızca spoiler'sız özeti gösterir (arketip sınıfı, yeni mi, perde başına ipucu sayısı, eleştirmenlerin uyumu).

**Kurallar:** çakışmaların hakemi script; başka bir kampanyanın çektiği arketip bir daha çekilmez.

## 15. Kötü — yalnızca yapı (owner ruling 2026-09-28: the development tab builds the rows, the owner does not see them)

Görünürlük, biçim ve köken P4'ten P1'in gizli zarlarına taşınır (#22); P4 cepheyi, kıyamet saatini, teğmenleri ve kötünün faksiyon arketipini tutar ve taşınan zarları okur. **Ev: kırılma ve soru.**

Altı parça, hepsi gizli zar:
- **Görünürlük** (5 satır, temiz).
- **Biçim** (12 kullanılabilir; kara kule efendisi, fısıldayan danışman, gizlice kötü hükümdar havuza hiç girmez; birkaç yeni satır eklenecek).
- **Köken** (9 kullanılabilir; uyanan kadim kötülük havuza girmez; "olgu onu aldı" olgu imzasına bağlanır).
- **Kırılmayla bağ** (yeni, 6): onu yarattı · ondan yararlanıyor · onu tamamlamak istiyor · korkunç bir bedelle geri çevirmek istiyor · onu durdurmaya çalıştı, başaramadı ve şimdi öfkeli · kırılmanın ürünü, onunla doğdu.
- **Kutup** (yeni): script A'nın ya da B'nin kutbunu seçer; kötü onu uç noktasına taşır, dünyanın çoğunluğu öbür kutba yakındır.
- **Seçenle uyum** (kural): sırrın seçeni "kötü" ise bağ "onu yarattı" olmak zorundadır; hakem script.

Kötü varsayılan olarak açık çekişmede bir taraf değildir; görünürlük nerede durduğunu belirler (bir rolün arkasında, görünmeyen elin arkasında, çekişmenin dışında ya da bir süreç olarak). **Tırmanış:** her basamakta farklı bir yüzle vardır; 1. katmanda işleri ve adamları, son katmanda kendisi (P7 ve P4'e söz).

**Vaadi:** P4 faksiyon, cephe, kıyamet saati, teğmenler · P5 dosyası iki bağımsız eleştirmenle (24.6 #6) · P6 ini; boss kontrol listesi v2 ve kötünün kendi imza silahı ile direnç eşyası gerçek ganimet · P7 son basamak kötüyle yüzleşme · kart yalnızca spoiler'sız özet.

**Kurallar:** yasaklı biçimler ve köken havuza girmez; çakışmaların hakemi script; başka bir kampanyanın çektiği biçim ve köken çifti bir daha çekilmez.

## 16. Adlar ve kökler

1. **Diller ve evleri:** short 2, standard ve epic 3 dil. 1. dil imza halkının dili; 2. dil ortak dil ya da çekişmenin öbür tarafının dili; 3. dil (standard ve üstü) kurumun ya da ikinci bir halkın dili. Kurum işareti "yalnızca kendi dillerini konuşurlar" çıkarsa kurumun dili ayrı bir dil olur.
2. **Ses ailesi:** `naming.yaml#family` 10 satırdan 20-24'e genişler. Ailenin değiştirilmesini (bir ses bankası değişir, bir ses kümesi yasaklanır) yazar değil script zarla yapar.
3. **Kökler (#20, kesinleşti):** zarla, ağırlık temelin konu alanlarından (palet toprak ve su, can damarı zanaat, canlı ve bitki); dil başına short 8-10, standard 12, epic 15. Sözlük 115 kökten 300-400'e genişler, açıklamalar nötrleşir. Çekim alanındaki kökler (candle, hush, still, wake…) sözlükte kalır (#18); bir kampanya onları ancak zarla çekerse kullanabilir.
4. **Kalıplar:** bütün kalıplardan örnekler silinir, yalnızca biçim kalır; "Court of…", "…Assize" ve ay kalıbı "…tide" çıkar. Kurum kalıplarının biçim kelimeleri (Order, Guild, Company, House, Council, League, Brotherhood…) kurum imzasının biçim tablosundan gelir.
5. **Ad havuzu, yer ve kurum için de:** script her yer, kurum, imza, ay ve gün adı için kalıp × zarla gelen köklerden 3-5 aday üretir; yazar birini seçer. Yazar hiçbir özel adı icat etmez; naming.json'daki örnek adlar da havuzdan gelir. Kişi ve tanrı adları bugünkü gibi `design_names.py` havuzundan.
6. **Kapı:** her özel ad havuzda olmalı. Sahibinin yasak listesi, modelin sevdiği adlar, mitoloji yasağı, Türkçe kelimenin ad olamaması, başka kampanyaların kaydettiği adların tekrar edilememesi ve Türkçe ek alabilme şartı aynen kalır.

**Vaadi:** P2 tanrı adları, aylar, günler havuzdan · P3 yer adları havuzdan, bölgelerin dilleri · P4 faksiyon adları biçim kelimeleri ve köklerden · P5 kişi adları havuzdan · P8 primerin diller bölümü.

## 17. Temel cümlesi, yazarın yazdıkları, kapı ve kart

**Şablon (script):** script hiçbir parçaya ek eklemez; her satırın Türkçe parçası kendi başına duran bir isim öbeği ya da tam cümle olarak yazılır, bağlantı ayrı kelimelerle ("ile", "arasında") kurulur. Eylemin üç zaman biçimi vardır (az önce ve bir kuşak önce → "tersine döndü"; şimdi oluyor → "tersine dönüyor"; yaklaşıyor → "tersine dönmek üzere"); her eylem satırı üçünü taşır, eksiğini bir test yakalar. Beş cümle:
1. Dünya [omurga]: kalbi [kalp], bir ucunda [uç], öbür ucunda [uç].
2. Çok önce [yıkıntı, ne oldu]; geride [kalıntı] kaldı.
3. Bugün halk [can damarı] ile yaşıyor.
4. [A] ile [B] arasında eski bir gerilim var; üçüncüsü [üçüncü rol].
5. [Zaman], [hedef] [eylem]. Yarası: [yara]. Bundan güçlü çıkan: [kazanan].

Cümle kimliğin girdisidir, okuyucunun metni değil; kartta tırmanışın basamak sayısıyla birlikte görünür.

**2. adımın zar sırası (script):** halk (soy, iki özellik, tavır) → kurum (halkın almadığı rol, biçim, uygulama, işaret, güç) → olgu (kural, belirti, sınır, kullanan) → soru → trope break (bağ) → sır (arketip, seçen, dönüş, iz; gizli) → kötü (görünürlük, biçim, köken, bağ, kutup; gizli) → adlar (aileler, değişimleri, kökler, havuzlar). Çakışma süzgeci her zardan önce.

**Yazar (tek ajan) yazar:**
- *açık öncül:* somut soru; üç imza (havuzdan ad, yerlinin ağzından bir paragraf: kural, görünüşü, gündelik hayata dokunuşu); trope break'ler bağlarıyla; diller (hangi halk hangisini konuşur); oyuncu pitch'i (üç cümle, sır yok); yalnızca bu dünyada doğru olabilecek üç cümle;
- *gizli ayna (dm-only):* sır (kırılmanın gerçek nedeni, seçen, dönüş); ipuçları (perde ve basamak, tür, yer sözü); kötü (biçim, köken, bağ, sorunun cevabı); DM pitch'i; zar çıkarsa imza mekaniği taslağı;
- *notlar:* her imzanın hangi varlıklarda görüneceği (söz defterine girer).

**Yazar yapamaz:** temeli değiştirmek; zar seçmek ya da yeniden atmak; özel ad icat etmek; örnek ad yazmak. "Önceki kampanyalar" listesini görmez (eleştirmende).

**Kapı (script):** her imza evinin kimliğini taşır; temelin damgaları değişmemiştir; satırlar arası çakışma yoktur; bütün özel adlar havuzdadır; sözler deftere yazılmıştır; açık dosyaya sır sızmamıştır.

**Eleştirmenler (zanaat):** iki eleştirmen ve faz eleştirmeni; yeni ölçütler: soru somut mu; üç cümle gerçekten yalnızca bu dünyada mı doğru; öncül önceki kampanyalardan farklı mı; her söz için bir hüküm.

**Kart:** temel cümlesi, oyuncu pitch'i, imzaların birer satırı, trope break'ler, sırrın spoiler'sız özeti, açık söz sayısı.

## 18. P1'in bütün taraması: düzeltmeler (owner-approved 2026-09-28; where they differ from the sections above, these hold)

**Sıra**
1. **Trope break 2. adımın ilk zarıdır.** Tersine çevirdiği varsayımlar (soyların yurtları, silah, canavar antlaşmaları, tanrı büyüsü…) sonraki zarlarca okunur. Bağı yalnızca temel parçalarına yaslanır: can damarı, yıkıntı, çekişme, kırılma (§12'deki halk, kurum ve olgu seçenekleri düşer).
2. **Omurga paletten önce atılır.** Omurga gerektirdiği yer türlerini palete zorla koyar (takımadalar → ada ve kıyı, yüzey ve derin → yeraltı, vaha → çöl…), kalanı zarla gelir.
3. **Ad havuzu P1'in zarlarının sonunda kurulur** (bugün `designer.py` onu P2'den başlatıyor); sırrın tanrısı ve imza adları da havuzdan gelir.

**Bağlantılar**
4. **Yıkıntıdan ya da yaradan doğan tek fantastik yer türü büyü sınırından muaftır** (düşük büyülü dünyada son büyü savaşından kalan tek cam çölü gibi). "Krater" ve "havada duran parçalar" palet türü değildir, P3'te simge yer (landmark) olur.
5. **Kurum yalnızca arketip ipucu olan bir rolden çekilir** (devlet, din, askerî, lonca, ticaret, bilgin, suç, direniş); dev klanları, ejderha, fey gibi roller kurum olamaz.
6. **Olgu tek kuraldır:** her yıkıntı satırı tuhaflığına uyan 2-3 kural ailesini (`olgu_families`) taşır, kural havuzu bunlara süzülür; "büyünün bir kuralı değişti" yarası varsa havuz yalnızca 8. aile ve olgunun evi kırılmadır, yıkıntının tuhaflığı kendi mekânlarında yerel renk olarak kalır (P6'ya söz). Kapı kuralın ailesini evin listesine karşı denetler; bir test binlerce tohumla kanıtlar. Eşleşmeler tablo kurulurken sahibine onaylatılır.
7. **Seçen ile kötünün bağı iki yönlüdür:** seçen kötüyse bağ "onu yarattı", bağ "onu yarattı" ise seçen kötüdür.
8. **Eylem uyumu ayrıntılıdır:** eylem ile can damarı ailesi, kalıntı türü ve kilit yer türü için ayrı uyum tabloları (script). Kazanan, kırılmanın yok ettiği rol olamaz. Kalp yok olduysa kampanya kalbin kalıntılarında ya da en yakın uçta başlar.
9. **Sır ve kötü tablolarının çakışma listelerini geliştirme sekmesi kurar;** sahibi yalnızca sayıları görür.
10. **Küçükler:** kurum işareti "yalnızca kendi dillerini konuşurlar" en az üç dil ister (short'ta çekilmez); epic'te kötünün kutbu ve kurumun rolü ana çekişmeden gelir.

**Katlar**
11. **Sözler zarları geçemez.** P2 iklimi, P3 bölge biyomları (short'ta 1-2 bölgeye karşı 4-5 palet türü: türler harita düğümlerinde yaşar), P3 yerleşim malları, P4 faksiyon kotası, P6 mekân türleri ve P7 açılış sahnesi bugün temelden habersiz zar atıyor; bir söz zarla atılmış bir satırı ezemez. **Yol:** yeni test doğumu önce yalnızca P1'i koşar; inceleme durağında sıradaki faz konuşulur, o fazın zar bağları inşa edilir, doğum oradan devam eder. Doğum hiçbir zaman henüz bağlanmamış bir kata çıkmaz.
