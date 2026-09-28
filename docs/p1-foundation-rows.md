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

**Kurallar:** büyü none → fantastik yok; low → yalnızca ince yer; medium → en fazla bir fantastik; high → en fazla iki. Her palette en az bir yükselti (dağ, yayla, volkanik) ve en az bir su (nehir, göl, kıyı). Sayı: short 4-5, standard 6-8, epic 9-12. Palet satırları kampanyalar arasında dışlanmaz.

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
| Boş tahta, üç ev | en güçlü ev (devlet) | en zengin ev (ticaret) | en eski ev (din) | halkın sevdiği bir yabancı (direniş) | kalp | evlilik ittifakları → zehir → açık savaş |
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
