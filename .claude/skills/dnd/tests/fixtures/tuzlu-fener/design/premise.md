---
entity: premise_tuzlu_fener
type: premise
secrecy: public
phase: P1
stamped: [question_tr, signatures, trope_breaks]
covers: [signature_tuz_hafizasi, signature_tuzbagli, signature_divan, break_no_afterlife]
mirror: design/dm-only/premise-secret.md
---

# Premise — Tuzlu Fener

## Public

### The question
- **Theme as a question:** *"Unutmak bir kurtuluş mudur, yoksa ikinci bir ölüm mü?"*
- **Tension rows rolled:** `tension_memory_salvation` — hatıra ile kurtuluş arasındaki gerilim; kıyı halkı ölüleri okuyarak hem hatırlar hem bırakır.
- **The world's default answer:** Unutmak merhamettir. Ölüyü bir kez okur, yasını tutar, sonra bırakırsın; kalanlar yaşamaya devam eder.
- **What the finale turns on:** Kör Fener yanacaksa kimin adına yanacak? Parti, hatırlanmanın bedelini kimin ödeyeceğine karar vermek zorunda kalır.

### Three signatures — things true only here
- **Magic phenomenon:** **[[signature_tuz_hafizasi]] — Tuz Hafızası.** Boğulan birinin son saati vücudunda biriken tuz kristalinde kalır. Kristali dilde eriten okuyucu o saati bir kez, içeriden yaşar. Bir kristal, bir okuma; okuyucu bazen kendi anılarından birini unutur, derler. Appears in: [[faction_divan]], [[npc_yesra]], [[place_tuz_evi]], [[site_kor_fener]], [[item_tuz_defteri]]
- **Culture or creature:** **[[signature_tuzbagli]] — Tuzbağlı.** Okunmadan gömülen boğulmuşlar bazen tuz düzlüğünden yürüyerek çıkar: tuz kabuklu, sessiz, kandil ışığında hareketsiz, karanlıkta yürüyen. Ghoul çatısı üstünde yeniden giydirilmiştir ([[creature_tuzbagli]]). Appears in: [[site_dipsiz_kuyu]], [[site_batik_iskele]], [[settlement_kamisli]], [[region_tuz_ovasi]]
- **Institution:** **[[signature_divan]] — Yas Tutanlar Divanı.** Okumayı ruhsatlayan, her okumayı deftere işleyen ve ücret karşılığı yas tutan kurum. Okuma için aile izni, bir kandil ve Divan mührü gerekir. Appears in: [[faction_divan]], [[npc_ilme]], [[npc_yesra]], [[place_divan_evi]], [[god_ormis]]

### Trope break(s)
- [[break_no_afterlife]] — **Ölümden sonra hiçbir şey yoktur ve bunu herkes bilir.** Tapınaklar öte dünya vaat etmez; [[god_isken]] yalnızca bitirir. Hatırlanmak tek öte dünyadır, bu yüzden okuma bir gelenek değil bir zorunluluktur. How it shows: ilk üç oturumda her cenaze, her kandil ve her "adını söyle" ricası bunu hissettirir. Touches: [[god_isken]], [[faction_divan]], [[signature_tuz_hafizasi]], [[settlement_fenerli]], [[thread_selen]], [[event_buyuk_tufan]]

### Forbidden defaults — checked
- Kehanet / seçilmiş kişi: yok; Fener'in yanması bir kehanet değil, bir takvim adımıdır (op_divan_1).
- Kara kuledeki karanlık lord: Kör Fener bir kule, ama içindeki kişi sessiz bir kâtiptir ve halkın yüzü olan kurum kötü değildir, yanılmıştır.
- Bozuk kilise: Divan bir kilise değil bir lonca; kötülüğü inançta değil defterdedir.
- Han açılışı: parti hanla değil borçla başlar (Tolvan odayı bedava verir, karşılığında bir iş ister).

### Naming languages
- `sazca` — kıyı halkı, sound family `liquid_vowel`; samples: Velune, Sarven, Yesra
- `kayaca` — yayla halkı, sound family `harsh_consonantal`; samples: Draskun, Vorin, Kortan
*(full definition in `design/naming.json`)*

### Player pitch
Tuz Ovası'nda ölülerin son saati tuz kristalinde kalır ve Yas Tutanlar Divanı onu ailenin önünde bir kez okur. Ölümden sonra hiçbir şey olmadığını herkes bilir; bu yüzden hatırlanmak her şeydir. Kırk yıldır sönük Kör Fener'in altında bir şeyler yeniden yanmaya hazırlanıyor.

## Discoverable

- Fenerli'de herkes bir okuyucunun "unutkan" olduğunu bilir; kimse bunun okumanın kendisinden geldiğini söylemez. [[npc_yesra]] son okuyucudur ve hikâyelerini iki akşam aynı anlatamaz.
- Divan bu ay üç okuma yaptı; ailelerden ikisi okumayı istememişti (bkz. `news.json`, `news_0002`).
