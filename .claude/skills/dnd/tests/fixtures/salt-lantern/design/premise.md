---
entity: premise_salt_lantern
type: premise
secrecy: public
phase: P1
stamped: [question_tr, signatures, trope_breaks]
covers: [signature_salt_memory, signature_saltbound, signature_court_of_mourners, break_no_afterlife]
mirror: design/dm-only/premise-secret.md
---

# Premise — Salt Lantern

## Public

### The question
- **Theme as a question:** *"Unutmak bir kurtuluş mudur, yoksa ikinci bir ölüm mü?"*
- **Tension rows rolled:** `tension_memory_salvation` — hatıra ile kurtuluş arasındaki gerilim; kıyı halkı ölüleri okuyarak hem hatırlar hem bırakır.
- **The world's default answer:** Unutmak merhamettir. Ölüyü bir kez okur, yasını tutar, sonra bırakırsın; kalanlar yaşamaya devam eder.
- **What the finale turns on:** Blind Lantern yanacaksa kimin adına yanacak? Parti, hatırlanmanın bedelini kimin ödeyeceğine karar vermek zorunda kalır.

### Three signatures — things true only here
- **Magic phenomenon:** **[[signature_salt_memory]] — Salt Memory.** Boğulan birinin son saati vücudunda biriken tuz kristalinde kalır. Kristali dilde eriten okuyucu o saati bir kez, içeriden yaşar. Bir kristal, bir okuma; okuyucu bazen kendi anılarından birini unutur, derler. Appears in: [[faction_court_of_mourners]], [[npc_yesra]], [[place_salt_house]], [[site_blind_lantern]], [[item_consumed_ledger]]
- **Culture or creature:** **[[signature_saltbound]] — Saltbound.** Okunmadan gömülen boğulmuşlar bazen tuz düzlüğünden yürüyerek çıkar: tuz kabuklu, sessiz, kandil ışığında hareketsiz, karanlıkta yürüyen. Ghoul çatısı üstünde yeniden giydirilmiştir ([[creature_saltbound]]). Appears in: [[site_bottomless_well]], [[site_sunken_pier]], [[settlement_reedham]], [[region_saltmere]]
- **Institution:** **[[signature_court_of_mourners]] — Court of Mourners.** Okumayı ruhsatlayan, her okumayı deftere işleyen ve ücret karşılığı yas tutan kurum. Okuma için aile izni, bir kandil ve Court mührü gerekir. Appears in: [[faction_court_of_mourners]], [[npc_ilme]], [[npc_yesra]], [[place_mourners_hall]], [[god_ormis]]

### Trope break(s)
- [[break_no_afterlife]] — **Ölümden sonra hiçbir şey yoktur ve bunu herkes bilir.** Tapınaklar öte dünya vaat etmez; [[god_isken]] yalnızca bitirir. Hatırlanmak tek öte dünyadır, bu yüzden okuma bir gelenek değil bir zorunluluktur. How it shows: ilk üç oturumda her cenaze, her kandil ve her "adını söyle" ricası bunu hissettirir. Touches: [[god_isken]], [[faction_court_of_mourners]], [[signature_salt_memory]], [[settlement_lanternside]], [[thread_selen]], [[event_great_flood]]

### Forbidden defaults — checked
- Kehanet / seçilmiş kişi: yok; Lantern'in yanması bir kehanet değil, bir takvim adımıdır (op_court_1).
- Kara kuledeki karanlık lord: Blind Lantern bir kule, ama içindeki kişi sessiz bir kâtiptir ve halkın yüzü olan kurum kötü değildir, yanılmıştır.
- Bozuk kilise: Court bir kilise değil bir lonca; kötülüğü inançta değil defterdedir.
- Han açılışı: parti hanla değil borçla başlar (Tolvan odayı bedava verir, karşılığında bir iş ister).

### Naming languages
- `marshtongue` — kıyı halkı, sound family `liquid_vowel`; samples: Velune, Sarven, Yesra
- `cragspeak` — yayla halkı, sound family `harsh_consonantal`; samples: Draskun, Vorin, Kortan
*(full definition in `design/naming.json`)*

### Player pitch
Saltmere'de ölülerin son saati tuz kristalinde kalır ve Court of Mourners onu ailenin önünde bir kez okur. Ölümden sonra hiçbir şey olmadığını herkes bilir; bu yüzden hatırlanmak her şeydir. Kırk yıldır sönük Blind Lantern'in altında bir şeyler yeniden yanmaya hazırlanıyor.

## Discoverable

- Lanternside'da herkes bir okuyucunun "unutkan" olduğunu bilir; kimse bunun okumanın kendisinden geldiğini söylemez. [[npc_yesra]] son okuyucudur ve hikâyelerini iki akşam aynı anlatamaz.
- Court bu ay üç okuma yaptı; ailelerden ikisi okumayı istememişti (bkz. `news.json`, `news_0002`).
