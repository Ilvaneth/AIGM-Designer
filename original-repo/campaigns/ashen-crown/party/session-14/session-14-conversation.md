# Session 14 — Conversation Log

**Campaign**: Ashen Crown
**Session**: 14
**Date**: 2026-09-03

---

### Morning — The Maker's Undoing, Room 13 (Sanctuary) — Session Start

**DM**: Confirmed this is a new session — Session 14 — after The Maker's Undoing was fully cleared through the Clay Golem boss fight and both PCs reached level 6 in session 13.

**Claude**: Loaded standing rules, confirmed session lock, synced state, briefed the table on party status and the loose end (Manticore A, fled Room 9 at 8/68 HP).

**DM**: "İlvaneth Level 6 Wizard 3rd level spell slotu 2/3 olacak. Sentuary Rooma gidip Short rest atıyoruz. İlva Arcane Recovery 3rd level slot."

**Claude**: Confirmed the 3rd-level slot figure was already correct (2/3) — the earlier summary text had a typo, not a data error. Ran the short rest: Ilvaneth spent her Arcane Recovery to restore a 3rd-level slot (0/1 remaining until next long rest); Kriv's short-rest features (Action Surge, Superiority Dice) fully restored via `features_restore_all`.

---

### The Maker's Undoing, side-den off Room 9 — Hunting Manticore A

**DM**: "Dungeondan çıkmadan Manticoreun peşine düşüyoruz. İlvanethin 1 zombiside yanlarında."

**Claude**: Tracked the wounded Manticore A via Kriv's Survival check (raw 20, total 20) to a hidden side-den. Set up the ambush — Ilvaneth's zombie thrall (Perrine Oskold) sent in first as an opening move.

**DM**: "İlva Zombie yi gönderiyor."

**Claude**: Initiative rolled for all four combatants. The zombie thrall attacked; Manticore A's counterattack (3 hits, 16 damage) destroyed it after two Undead Fortitude saves (one success, one failure). Kriv's Barrow-King's Blade finished Manticore A in melee (Fire Bolt miss from Ilvaneth first, then Kriv's two attacks — first missed, second hit for 21 radiant including the vs-undead bonus, killing it outright). 100 XP each (mop-up award). Kriv harvested tail spikes/hide.

**DM (OOC mid-combat)**: "Zombie İlvanethin İnitiativinden faydalanır aynıdır İlva ile. İlva 4, Kriv 7." — establishing the new standing rule that player-controlled summons share the controller's initiative and are entirely player-rolled going forward. Logged in `dm-notes.md`, and `combat_status.py` extended with a real `"ally"` type + `add_combatant` patch support to make this trackable going forward (see `bug-log.md`/`system-register.md` day 2026-09-03 entries).

---

### The Maker's Undoing → Harrowgate — 3-Night Journey

**DM**: "Zindandan çıkıp Harrowgate e dönüyoruz geceleri Long Restte İlvaneth Tiny Hut castler içerisinde dinlenirler. OOC: Bundan sonraki, yollardaki Long Restler de İlvaneth Sürekli Tiny Hut Castler onun içerisinde dinlenirler."

**Claude**: Established the new standing travel routine (Ilvaneth ritual-casts Tiny Hut nightly, no watch needed) in `state.md`. Rolled 3 nights of Cindermoor Late-tier travel.

**Night 1 — 2 Will-o'-Wisp.** Full surprise against the party (their own Invisibility trait leaves no legitimate detection method). Both opening attacks missed. Round 2: Wisp A hit Kriv for 10 lightning. Ilvaneth's Fire Bolt (halved by fire resistance, 9 dmg) then killed Wisp A via Kriv's Goading Attack + vs-undead bonus (21 radiant). Wisp B, reduced to 14/22 by an upcast Thunderwave (halved by resistance, 8 dmg), fled — not pursued. 225 XP each.

**Night 2 — Orna Threk.** The unnamed half-orc rival relic-hunter from The Maker's Undoing (Room 2) returned, named for the first time, with 2 hired Scouts, confronting the party directly on the road.

**DM (in character, Orna)**: *"Kaçmama izin verdiniz. Sanırım bunu bir zayıflık olarak okumam gerekiyordu... O zindan benimdi."*

**DM**: "İlvaneth Aoe içerisine Krivi almadan Fireball" — Fireball caught all three clustered in the narrow pass, killing both Scouts outright and burning Orna to 28/65. Kriv finished her: "Kriv: Sebi şimdi tek darbede öldüreceğim ve Yüce Büyücü İlvaneth seni zombiesi yapacak sonsuza kadar hizmetkarım olacaksın Ha HAaa Haaaa... Atak 1 Pres. Str. GWM 15 5. Atak 2 Goading GWM 19." Both attacks hit; combined for 52 damage, killing Orna outright. 325 XP each. Searched the bodies (Investigation 25) — 76 gp and Orna's own hand-drawn territorial map (logged as a planted hook). Orna's body preserved with Gentle Repose.

**Night 3 — the scavenger crew.** A different, unconnected 3-Thug crew tried to shake the party down at their campfire.

**DM (in character, the thug leader)**: *"Yükünüz ağır görünüyor... Paylaşmayı düşünün — ya da burada bırakın."*

**DM**: "Kriv: Elini havaya kaldırır sorun istemiyoruz sadece yoldan geçiyoruz diyerek konuşan adamın yanına yürüyerek Fire Breath Atar." Initiative was rolled fully first (no free pre-initiative round, per `combat-rules.md`). Ilvaneth's Fireball (Kriv positioned outside the blast) killed 2 of 3 outright. The third surrendered:

**DM (in character, Thug C)**: *"Dur, dur! Teslim oluyorum! Ne isterseniz— sadece öldürmeyin!"*

**DM**: "kriv kılıcı ile dograr" — executed the surrendering thug anyway. Kriv earned 275 roleplay XP for the honest Neutral Evil cruelty. 150 XP each for the fight. Arrived Harrowgate the next morning, day 60.

---

### Harrowgate, day 60 — Downtime

Several real gaps were caught and fixed this session: the Ring of Mind Shielding (Room 20 loot, never recorded on a sheet since session 13) was found missing when the DM asked directly — added to Ilvaneth's sheet and attuned. Ring of Protection's AC/save bonus (missed since day 51) was corrected on her sheet (AC 17→18, all six saves +1).

**The Ashgate Conservatory.** Collected the commissioned Remove Curse scroll from Yveth Corrane (220 gp), bought Identify components (pearl + owl feather, 120 gp).

**DM (in character, Yveth)**: *"Tam zamanında. Ağımdan geçti — üç haftadır beklediğim bir teslimat oldu ama sonunda geldi... 220 altın, anlaştığımız gibi."* Also passed along overheard gossip about a wild ghast killed near Gallowmere — the actual off-screen resolution of the Ash-Kilns' World Events fire (the caged failed "returner" broke free, killed 2, covered up by Kell's garrison).

Identified Room 19's items: Sending Stones (addressed to "Karsgate — the Ledger Trading House, attn: V. Marrow" — an unconfirmed echo of Sefwyn Marrow's surname), a dangerous life-draining prototype shortsword (+1d6 necrotic on hit, 1d4 necrotic feedback to the wielder), and a +1 Quarterstaff (Ilvaneth took it, replacing her mundane one). The tarnished signet ring from Room 7 turned out to be non-magical but matched Marek Stillwright's ledger — it belonged to "Doran Calvane," an unfinished commission client who was killed by the Room 7 Mimics while looking for his own blade.

Sold accumulated loot (harpy feathers, petrification gland, three batches of Manticore materials, raw crafting materials, corroded hilt, Doran Calvane's ring) for 273 gp.

**Ironmonger's Row — Borgha Kresk.**

**DM (in character, Borgha)**: *"Demek geri döndünüz... Kesh Deeps?"*

Reported the cleared duergar threat. Borgha relayed thanks and gave a small gift (duergar-steel arrowheads and a knife). The "Report the Kesh Deeps warning" quest closed.

**Hiring Ostrig Kelmar (new NPC, dwarf mason/foreman).**

**DM (in character, Kelmar)**: *"Şestendeliath, öyle mi? Duydum o ismi — yanmış bir malikane, doğuda, kimsenin yaklaşmadığı. Hikayeler var. Ben hikayelere inanmam ama ekibim inanabilir... İşi dürüstçe anlat, adil öde, sorun olmaz."*

Kriv negotiated with Ilvaneth's help (Persuasion 13) — standard terms, 300 gp total, 2-3 weeks, 150 gp deposit paid. This activated Shestendeliath Hold's Phase 1 as a real, tracked holding in `holdings.md`.

**Inn — inventory review.** Reviewed the Bag of Holding's full contents at the DM's request. Discarded a torn journal page; burned Nessa Wren's and Perrine Oskold's research notebooks.

---

### Party Split, day 60

**DM**: "Party kendi arasında plan yaparlar. Dungeondan buldukları mesaj stonunu İlvaneth Inn e gidere Pearlü bırakıp Attuneliyecek sonra kitabına Remove curse skillni ekleyecek. Oradan Ostwicke Doğru yola çıkacak. Kriv, Ustabaşıların toparlanmasını beklerken Hold için bir kaç aylık yiyecek stoğu alır. Sonra ustaları da alarak holun yolunu tutar."

Ilvaneth unattuned the Pearl of Power, attuned a Sending Stone in its place, and copied Remove Curse into her spellbook (150 gp, 6 hours — no Necromancy Savant discount). Kriv bought several months' food stockpile (250 gp).

**DM (correction)**: "Stonelardan birini Kriv alır, party kendi arasında haberleşsin diye. yazmayı unuttum." — Kriv took the other Sending Stone so the split party could reach each other.

**DM**: "Devan Durmak yok" / "Sıra ile oynayalım" — the two threads would be run in alternating turns.

---

### Kriv's Thread — Harrowgate → Shestendeliath Hold

Departed with Kelmar's crew and the food stockpile. En route, Investigation (nat 20) found the aftermath of a real Concordat/Compact skirmish — burned Concordat banners, a Compact-style buckle, no bodies. This resolved `consequences.md`'s pending question: Ilvaneth's day-39 forged evidence held, and real Concordat-Compact friction has opened (`faction-subplots.md`).

**DM (OOC)**: "ser kethrax ve askerlerinden ustalar ve isciler korkmazmı? oyle ise Kriv Holda yaklasınca kervana dur ve bekle der holda gider, Kethraxa ve askerlerine alt sarnıca gitmelerini emreder." — caught and fixed a real continuity gap: the mundane work crew would be terrified of the undead garrison. Kriv had the caravan wait while he ordered Kethrax's garrison to withdraw to the lower cistern first.

**DM (in character, Kethrax)**: *"Emredersiniz. Sarnıçta bekleriz — çağırdığınızda hazırız."*

Kriv worked alongside the crew on the remaining debris (~65-70% already cleared by the garrison over the prior 9 days). Then departed solo for Harrowgate to collect Roskel — a close call avoiding a Concordat inspection patrol (Stealth 10 vs Perception 11).

**Reunion with Roskel** (given a race for the first time — half-orc — per `narration.md`'s sweep policy, since he'd never been assigned one in play before).

**DM (in character, Roskel)**: *"Efendim. Mektubunuzu aldım — 'acınız sona erdi' demiştiniz, başka bir şey söylemediniz. Neye hazırlanayım?"*

**DM**: "Holda doğru yola çıkıyoruz giderken yolda Kriv Roskele; Artık bir kalemiz var Şu anda rstorasyonu devam ediyor, yakında insanlar da gelecek, sen benim yokluğumda kaledeki yetkili olacaksın..."

**DM (in character, Roskel)**: *"Bir kale... Yirmi yıl bir bayrağın altında hizmet ettim, sonra hiçbir şeyin altında sürüklendim. Şimdi bana bir kale ve bir yetki mi veriyorsunuz? Hayal kırıklığına uğratmam."*

Named Roskel steward of Shestendeliath Hold. This resolved and superseded "Roskel's second summons" clock. Returned to the Hold together (day 63), avoiding another Concordat patrol cleanly.

---

### Ilvaneth's Thread — Harrowgate → Ostwick

Solo journey. Night 1: a rolled encounter (2× Wight, Undead escalated) was flagged to the DM as a likely-fatal fight for a solo level-6 character against 2-PC-calibrated Deadly math.

**DM**: "Saklanıyorum." — Stealth 20 vs passive Perception 13, avoided entirely.

Night 2: found an old, pre-Ember-Crown shrine to a stag-headed nature spirit.

**DM**: "eski staffını bırakır" — left her old mundane quarterstaff as an offering, received a minor 24-hour boon.

**Ostwick — Maren Ashe.**

**DM (in character, Maren)**: *"Sen... geri geldin. Yalnız... Kriv nerede?"*

**DM**: "Ayakta konuşabileceğimiz şeyler değil, oturup nerede konuşabiliriz ev uygun mu, hem birer çay içeriz."

Moved the conversation indoors.

**DM (in character, Maren)**: *"Neden soruyorsun bunu bana bu kadar direkt? Kimsin sen, ve bunu neden istiyorsun?... Onu avlamak için mi bahane arıyorsun?"*

**DM**: "Kriv burada değil, sen kardeşini kurtarmak istiyor musun bana onu söyle." / "Salak Karı seninle konuşmuştuk ya bir çözüm olabilir araştıracağım demiştim hatırladın mı? Sen domuzu tercih ediyorsan bilemem artık..."

**DM (in character, Maren)**: *"...Hatırlıyorum... Sekiz yıldır kimse bana bunu söylemedi... Gerçek mi? Onu gerçekten kurabilir misin?"*

**DM**: "Evet kurtarabilirim ama bir bedeli var bedel ödemeye hazır mısın?" Then, when Maren asked what the price was: "Bundan sonra sen ve kardeşin benim tebam olacaksınız. Emirlerimi takip edeceksiniz, artık ben ne diyorsam onu yapacaksınız ve bu şimdiden itibaren başlıyor anlaştık mı ne dersin??"

**DM (in character, Maren)**: *"Tebaanız... ne demek bu tam olarak? Ne isteyeceksin bizden?... Dunnel'ın da rızası olmadan onun adına söz veremem — ama benim için... eğer gerçekten onu kurtarabiliyorsan... Anlat bana ne bekliyorsun. Sonra karar veririm."*

**DM**: "Ostwickten ayrılıp Kalem de yaşayacaksınız, bana hizmet edeceksiniz, merak etme başını sokacak güvenli bir çatın olacak ve karnın da doyacak. Ama sadece sen olmaz kardeşin de gelecek anlaşma bu. Gelmez ise onu ikna etmek senin görevin. Ne dedin??"

**DM (in character, Maren)**: *"Kale nerede olursa olsun — güvenliyse, yeterli. Kabul ediyorum kendi adıma... Onu bulmaya gidiyorum."*

**Finding Dunnel Ashe** (first real appearance in play).

**DM**: "Maren' nin arkasından Invisibility kullanıp gidiyorum, kardeşini bulmaya gittiği yere. Bulunca Remove Curse." / "Görünmezden yaklaşıp remove Curse" (Stealth 14 total, successful approach).

Cast Remove Curse on Dunnel directly — cured after eight years. Invisibility broke automatically per the spell's own rule (ends if the target casts a spell).

**DM (in character, Dunnel)**: *"Ben... hissediyorum. Gitti mi? Gerçekten gitti mi?"*

**DM**: "Merhaba Dunnel, artık özgürsün yamuk bedeninden, kötü düşüncelerden, saklanmaktan, yalnızlıktan kurtuldun. Artık tek düşüncen hanımıma nasıl yardımcı olurum olacak..."

**DM (in character, Dunnel)**: *"Sekiz yıl... sekiz yıl ormanın kenarında, kendimden korkarak yaşadım... Ne istersen. Kız kardeşim güvendiyse, ben de güvenirim... Kale'ye gideriz, hizmet ederiz. Bu borcu ödeyeceğim."*

**DM**: "Bugün burada sizin evinizde dinlenelim yarın yola çıkacağız. Krive dön." — rested at the farmstead overnight, cutting to Kriv's thread.

Before departing Ostwick the next day:

**DM**: "Ostwickten ayrılmadan aileye bir işim var siz ben gelene kadar bekleyin diyorum. Inn e dönüyorum Marshın oda 4 te gizli stashi vardı onu soyacağım. Inn de 4 numaralı odayı kiralıyorum."

This resolved a genuinely forgotten planted hook — the dead Lonca courier's hidden key (day 52), never actually recorded on a sheet, pointing to an unexamined room at The Hollow Sheaf. Investigation (nat 20, total 27) found a hidden strongbox under a floorboard — Marsh's own stash, 230 gp.

---

### Reunion — Shestendeliath Hold, day 65

**DM**: "İlva dönene kadar Kriv ve Roskel işlere yardım eder. party Hold da bir araya gelir."

Both threads' local clocks converged; Ilvaneth traveled from Ostwick with the Ashe siblings (2 nights — a noted-but-unfollowed signpost, a swollen creek crossed via Misty Step + a guide rope for Maren/Dunnel). The full party — Kriv, Roskel, Ilvaneth, Maren Ashe, and Dunnel Ashe — reunited at Shestendeliath Hold, alongside Kelmar's mid-Phase-1 crew and Kethrax's still-hidden garrison.

**DM**: "End Session yapma!!! Tüm oturumun kaydını al." — explicitly declined the full end-session flow (no story-teller handoff, no verifier agents), requesting only that the session's conversation be recorded via checkpoint log.

---

*This log covers the full session from start through the Hold reunion. State (character sheets, `state.md`, `campaign-clock.md`, `holdings.md`, `consequences.md`, `faction-subplots.md`, and multiple NPC files) was kept synced live throughout play, not deferred to end-of-session — see those files for full mechanical detail (exact rolls, HP totals, XP awards). This conversation log preserves the actual dialogue and DM decisions in sequence.*
