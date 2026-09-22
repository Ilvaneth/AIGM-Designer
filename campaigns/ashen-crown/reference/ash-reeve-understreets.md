# Ash Reeve Understreets — The Path to the Unmade

*Tasarlandı gün 175, session 27 (oyun-dışı tasarım geçişi, oyuncu talebiyle) — Corvun Skai'nin "kestirmesi" retcon edildi: güvenli bir yol değil, Ash Reeve'in eski kanalizasyon/mahzen ağı, üç yüz yıllık başarısız necromancy deneylerinin kalıntılarıyla dolu. Sylandra Cael'e ulaşmadan önce, gatekeeper figür partiden somut bir bedel istiyor: Kule-i Mensuh'ta yaşayan "The Unmade"i yok etmek (ya da koruduğu eşyayı almak).*

**Ton:** Klostrofobik, nemli, unutulmuş — Debased Mint'in "yozlaşmış aile" temasının necromancy versiyonu. Level 11 parti için gerçek bir zorluk hedefleniyor (Combat Difficulty Doctrine tam uygulanıyor, bu bir set-piece).

**Giriş:** Fenn'in gösterdiği duvar paneli, Corvun'un deposundan. Işık kaynağı gerekli — mumlar, büyü, ya da darkvision.

---

## Oda 1 — Çöküş Koridoru (kalabalık, doku)
Dar bir taş koridor, tavan çökmüş kısımlarla dolu (difficult terrain, ara sıra bir STR/DEX check gerektirebilir geçiş için). Duvarlarda eski, silinmiş yazılar. Koridorun sonunda, **8x Zombie** — eski deneylerin kalıntısı, hiçbir komuta altında değil, sadece hareket eden, karanlıkta bekleyen şeyler. Sayı çok ama tek tek zayıf (AC8, HP22) — gerçek tehlike sayı/alan kısıtlaması (dar koridor, hepsi aynı anda saldıramaz).

## Oda 2 — Gerçek Encounter #1: Ghast Sürüsü
Eski bir arşiv odası, raflar çürümüş. **4x Ghoul + 2x Ghast** — Stench (zehir) + paralysis riski gerçek, parti dikkatli olmalı (CON save'ler art arda gelebilir). Ghast'lar Turn Defiance ile ghoul'ları da koruyor.

## Oda 3 — Taşkın Sarnıç (kalabalık + çevresel)
Su basmış bir oda, diz boyu su, görüş kısıtlı. **4x Specter** — incorporeal, duvarlardan/su altından beklenmedik yönlerden geliyor, Life Drain ile max HP düşürüyor (gerçek, kalıcı bir bedel — uzun molaya kadar sürüyor).

## Oda 4 — Gerçek Encounter #2: Wight Nöbetçileri
Eski bir muhafız karakolu. **3x Wight** — Life Drain ile öldürdükleri insanları zombi yapabiliyorlar (bu odada olmaz, kimse insan değil ama mekanik hatırlatma: gelecekte NPC'lere karşı dikkat). Longsword/longbow karışık saldırı, gerçek bir taktik direnç.

## Oda 5 — Mumyalanmış Kütüphane (kalabalık)
**6x Skeleton (shortbow)** + **2x Zombie** — menzilli/yakın karışımı, önceki odalardan yorulmuş bir partiye baskı yapmak için tasarlandı (art arda encounter attrition — Combat Difficulty Doctrine madde 6).

## Oda 6 — Gerçek Encounter #3: Mumya Muhafızları
Kule-i Mensuh'un eşiği. **2x Mummy** — Dreadful Glare (korku+paralysis riski, Cloak of Displacement'ı atlar çünkü save-bazlı) + Rotting Fist'in "mummy rot" laneti (gerçek, kalıcı bir tehdit — Remove Curse gerektirir, parti zaten bu büyüye sahip).

## Oda 7 — Kule-i Mensuh'un Zirvesi: THE UNMADE (final boss)

**The Unmade** — Sylandra Cael'in üç yüz yıl önceki ilk, başarısız kendi-koruma denemesi. Ne lich ne zombi, ikisi arasında donmuş bir şey — CR ~13 muadili, custom stat block.

| | |
|---|---|
| **AC** | 17 (doğal + eski zırh parçaları) |
| **HP** | 380 (burst_check.py ile doğrulandı — parti nova'sı ~245-290, güvenli marj) |
| **Hız** | 30 ft |
| **Direnç** | Necrotic, Radiant, Poison |
| **Bağışıklık** | Charmed, Frightened, Exhaustion, Poisoned |
| **Legendary Resistance** | 3/gün |
| **Legendary Actions** | 3/tur (Claw saldırısı — 1 aksiyon; Kayma — hareket, 1 aksiyon; Umutsuzluk Çığlığı — WIS save korku, 2 aksiyon) |
| **Regeneration** | Turunun başında 15 HP yeniler, **ateş hasarı almadıysa** son turdan beri |

**Multiattack:** İki Pençe atağı + bir Emen Dokunuş.
- **Pençe:** +9 atak, 2d8+5 slashing.
- **Emen Dokunuş:** +9 atak, 3d8 necrotic, hedef geçici olarak max HP kaybeder (Wight'ınkine benzer, uzun molaya kadar).
- **Umutsuzluk Çığlığı (Legendary, 2 aksiyon, kısa/uzun molada 1/gün):** 30 ft, WIS save (DC 16) yoksa 1 dakika korkulu.

**Faz 2 (yarı HP'de tetiklenir):** The Unmade, bedeninin bir kısmını dağıtıp geçici olarak **4x Zombie** çağırır (kendi çürüyen dokusundan) — gerçek bir ikinci dalga, alfa saldırının etkisini böler.

**Zayıf nokta:** Ateş hasarı regenerasyonu durduruyor — Ilvaneth'in Fire Bolt/Fireball'ı burada özellikle değerli.

**Ödül:** Sylandra'nın üç yüz yıl önce kaybettiği bir eşya, The Unmade'in göğsüne gömülü — **"Sylandra'nın İlk Mührü"** (kendi büyüsel imzasını taşıyan, tarihi bir obje, Sylandra'ya götürülecek). Ayrıca oda içinde standart loot (eski, değerli ash-king dönemi kalıntıları, ~500-800 gp değerinde).

---

## Notlar
- Bu, "Kule-i Mensuh" adının ilk somut kullanımı — steering notes'ta adı geçiyordu, artık gerçek bir yer.
- Oda 1, 3, 5 kalabalık/doku; Oda 2, 4, 6 gerçek encounter; Oda 7 final boss — toplam 4 "gerçek" encounter + final boss, oyuncu talebine uygun.
- Sylandra'nın ilk görüşmesi (gün 175'te zaten oynandı — Circle'ın kökeni, Crown teorisi, True Polymorph) **geçerli kalıyor** ama artık bu dungeon'ın SONUNDA gerçekleşecek, başında değil. Zaten söylenenler bir sonraki görüşmede tekrarlanmadan, "Unmade'i hallettiniz, şimdi konuşalım" şeklinde devam edilebilir.
