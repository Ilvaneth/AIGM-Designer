# Session 15 — Conversation Log

**Date**: 2026-09-04
**Campaign**: Ashen Crown

---

### Morning — Shestendeliath Hold — Session Briefing

Session opened with the standard `/dm-start-session` checklist: rules reload, session-number confirmation (Session 15 confirmed with the DM), session lock acquired, `sync_state.py`/`rest_check.py` clean, campaign clock current through day 65. Party briefed: both PCs full HP/resources, at Shestendeliath Hold, party fully reunited. Four options offered: introduce Kethrax's garrison to Roskel/the Ashes, reconnect with Sefwyn Marrow, chase the Sorin Vaal/Karsgate lead, or push the Hold restoration — plus The Unquiet Barrow as a standalone no-strings option.

---

### Evening — Shestendeliath Hold, the Great Hall — Household Business

**DM**: "İlvaneth mesaj tasını deattunelayıp yerine pearlunu attunelar ve tası Krive verir. Kriv Roskele ve yeni gelen ashe kardeslere buranın lordunun kendisi oldugunu soyler ve bundan sonra burda kendisi olmadıgı surece en yetkili insan Roskel der. Daha sonra Roskelle teketek konusmaya ve mesaj tasının ona verir. bi durum olursa ben kalede olmadıgımda bana ulasabilsin diye Roskel(tası attuneler)."

Claude narrated: Ilvaneth deattuned her Sending Stone, re-attuned the Pearl of Power, and handed the freed stone to Kriv. Kriv gathered Roskel, Maren, and Dunnel Ashe and declared:

> **Kriv:** "Bu kale benim. Ben Shestendeliath'ın lorduyum — ismim on beş yıldır çürümeye bırakıldı, artık değil. Burada olmadığım her an, sözüm Roskel'in ağzından çıkar. Onu dinleyin, ona itaat edin — ben burada olsaydım nasıl davranacaksanız öyle davranın."

> **Roskel:** "Anlaşıldı, Lordum."

Kriv then pulled Roskel aside privately and gave him the Sending Stone:

> **Kriv:** "Bir şey olursa — ben kalede olmadığımda — bana bununla ulaş."

Roskel attuned it. Mechanically: Ilvaneth's attunement slots now Ring of Protection/Ring of Mind Shielding/Pearl of Power; the Kriv↔Ilvaneth Sending Stone pair repurposed to Kriv↔Roskel.

---

### That Evening — the Great Hall — The Garrison's Introduction

**DM**: "bu aksam kucuk bir ziyafet ile buyuk salonda otururken Kriv getirir Kethrax ve askerlerini."

Claude narrated the household's first dinner interrupted by Kriv bringing in Ser Kethrax and the three other bound retainer wights. Roskel's chair went over as he stood, hand on his sword hilt; Maren pulled Dunnel back; Dunnel didn't flinch.

> **Roskel:** "Lordum... bunlar—"

> **Kriv:** "Bunlar hanemin adamları. On beş yıldır kapıyı bekliyorlar. Şimdi seninle aynı çatının altındasınız — ve bundan sonra da öyle olacak."

> **Kethrax:** "Ser Kethrax. Kapı muhafızlarının kumandanı, Hane Shestendeliath'a bağlı — hayattayken de, şimdi de. Korkmanıza gerek yok; emrimiz yalnızca bu hanenin sınırları içinde geçerlidir, ve Lordumuzun sözü kanunumuzdur. Sizi tanıyorum, sanırım — ya da tanımayı öğreneceğim. Bu evde artık ikimiz de aynı işi yapıyoruz."

> **Dunnel:** "Sekiz yıl insanlar benden korktu... çünkü ne olduğumu bilmiyorlardı. Bunlar en azından... kim olduklarını biliyor."

**DM**: "Kriv Ser kethrax siz tekrar yerinize dönün şu restorasyon işi bitine kadar bir tehlike yok ise ortalarda görünmeyin. Artık Tebam sizi tanıyor sorun olmayacaktır. Kethrax giderkeni Kriv kadehini kaldırır. Kalemizdeki ilk aksam yemegine hosgeldiniz durmayın devam edin, Şerefe"

> **Kethrax:** "Emredersiniz, Lordum. İyi geceler. Kapı sizindir artık, benimle paylaşacaksınız — ama bu gece değil. Bir tehlike olursa, saniyesinde buradayız. Aksi hâlde... gölgede kalırız, dediğiniz gibi."

> **Kriv:** "Kalemizdeki ilk akşam yemeğine hoş geldiniz. Durmayın, devam edin. Şerefe!"

> **Roskel:** "Şerefe, Lordum."

> **Dunnel:** "Şerefe."

---

### Later That Evening — the Great Hall — Closing the Day

**DM**: "Maren sofrayo topla, bize yeni içecek getir, Şimdi Roskel İlvaneth ile beni yalnız bırakın. Kriv: Roskele 300 gp verir, bunun 150 gp si Restorasyon ödemesinin, kalanını kale ihtiyaçları için kullanabilirsin ben yokken. End Day"

Maren cleared the table and brought fresh drinks, then withdrew with Dunnel. Kriv gave Roskel a purse:

> **Kriv:** "Roskel — bekle. Üç yüz altın. Yüz ellisi Kelmar'a — iş bittiğinde ödenecek bakiye, ben burada olmasam da. Kalanı senin takdirin: kale ne isterse, ben yokken sen karar ver."

> **Roskel:** "Anlaşıldı, Lordum. İyi geceler."

Kriv's gold: 1066 → 766 gp (300 gp entrusted to Roskel — 150 gp earmarked for Ostrig Kelmar's remaining Phase 1 balance, 150 gp discretionary). Roskel and Kriv/Ilvaneth left alone; the day closed without further detail. Day advanced 65 → 66, long rest applied, campaign-clock.md's header corrected to match (caught by `clock_check.py`'s Stop hook).

---

### Morning — Shestendeliath Hold — Orna Threk's Map

**DM**: "İlvaneth Relic Hunterdan aldığı haritaya bakar."

Claude checked `planted-hooks.md`'s existing "Orna Threk's territorial map" entry (status: unresolved, "2-3 others still unmarked") and cross-referenced the gazetteer for real, already-built, unplayed, level-appropriate candidate sites before deciding the map's content — landing on The Drowned Cathedral (Cindermoor) and The Unquiet Barrow (Thornlands), both faction-free and matching the party's level 6.

Narrated: the map showed The Maker's Undoing crossed out, a flame-glyph over The Drowned Cathedral, and a bare question mark over an unnamed site in the Thornlands (The Unquiet Barrow — Orna had never actually gone in).

Player OOC correction followed: Sefwyn Marrow cannot be "gone to" as a destination — his file states he's Mobile with no fixed location, and every past contact was Sefwyn-initiated. Claude confirmed the correction, logged it (`bug-log.md`, `npc-inconsistency`), and clarified the real mechanism (traveling toward his usual territory raises contact odds; it isn't a chooseable "go find him" action).

**DM**: "The Unquiet Barrow Haritada işaretli olan yerine yola çıkıyoruz atlarla."

---

### Night 1 — The Thornlands Road — The Barrow Road Ambush

Travel roll (Thornlands, Late tier): Night 1 → Combat, Undead escalated → d4 sub-roll → 1 Ghast + 2 Wight. Both Wights (Stealth 21) and the Ghast (Stealth 22) beat both PCs' passive Perception — full surprise for the undead, caught mid-camp before Tiny Hut went up.

Full combat resolved over 4 rounds — complete blow-by-blow in `session-15-combat-thornlands-barrow-road-undead.md`. Key beats: Kriv paralyzed then un-paralyzed by a mid-fight Constitution-save-modifier correction (his real save is +6 proficient, not the bare +3 ability modifier first used — `bug-log.md`, `combat-geometry`); Ilvaneth's Misty Step + Mirror Image; Kriv's Action-Surge nova (Precision Attack, natural-20 Goading Attack crit — a second live correction added the Goading Attack superiority die's own damage dice to the crit) killing the Ghast outright; Ilvaneth's Fireball catching both Wights and Kriv (accepted deliberately, resisted); Wight B killed by Kriv's opportunity attack as it broke for the wounded Ilvaneth; Wight A finished by the Wand of Magic Missiles. Ilvaneth dropped to 10/45 HP — the closest call of the fight. 925 XP each.

---

### Morning — On the Road, Day 67 — Long Rest

**DM**: "Timy Hut Kurup Long Rest"

Long rest applied (day 66 → 67), both PCs restored to full. `location_check.py` false-flagged "The Drowned Cathedral" (mentioned only as an unpursued lead in `state.md`'s Current Location field, not an actual arrival) twice — resolved both times by rewording the field to avoid the exact matched title; root cause logged (`bug-log.md`, `hook-fragility`) for a future fix to the hook's own matching scope.

Session ended here, mid-journey toward The Unquiet Barrow.
