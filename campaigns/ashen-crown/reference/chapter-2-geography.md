# Chapter 2 Coğrafyası — Emberhold, The Sundered Reach, The Grey Kingdom

Session 26 tasarım geçişinde oluşturuldu — `travel-times.md`'nin bıraktığı "Shestendeliath Hold ↔ Emberhold: TBD" boşluğunu kapatıyor, ve Chapter 2'nin üç bölgesinin somut ölçeğini/nüfusunu/ziyaret noktası sayısını sabitliyor. **Henüz hiçbiri oyunda gerçekleşmedi — tahmini, ama sabit kabul edilecek** (tıpkı `travel-times.md`'nin "zincirleme hesaplanmış" satırları gibi; gerçek oyun bir rotayı değiştirirse, o zaman güncellenir).

---

## Seyahat Süreleri (travel-times.md'ye ek)

**★ Rota düzeltmesi (2026-09-11, oyuncunun kampanya haritasıyla doğrulandı):** Emberhold, Harrowgate'ten ayrı bir dal değil — kampanyanın kendi Chapter 1 haritasında Karsgate'in hemen altında "Emberhold – İmparatorluk Başkenti (Bölüm 2) →" oku var, **Karsgate'ten devam ediyor.** Gerçek rota: **Harrowgate → Karsgate → Emberhold.**

| Rota | Gün |
|------|-----|
| Shestendeliath Hold ↔ Emberhold | **~12,5-14 gün** (Harrowgate → Karsgate → Emberhold zincirlemesi: Hold↔Karsgate ~8,5-9 gün + Karsgate↔Emberhold ~4-5 gün) |
| Karsgate ↔ Emberhold (doğrudan) | ~4-5 gün — haritadaki devam eden ok, ayrı bir dal değil |
| Emberhold ↔ The Sundered Reach (sınır) | ~6-8 gün (kuzeye, krallığın yazılı sınırının ötesine) |
| Sınır ↔ Frostmere | ~1-2 gün ek |
| Sınır ↔ Kar Vaelth | ~2-3 gün ek |
| Frostmere ↔ Kar Vaelth (bölge içi) | ~3-4 gün |
| Kar Vaelth ↔ The Bonewrights' Hall | ~2-3 gün (aynı eski uygarlığın kalıntıları, nispeten yakın) |
| Kar Vaelth ↔ The Screaming Fen | ~2-3 gün (bataklık, bölgenin kenarında) |
| Emberhold ↔ The Grey Kingdom | **Normal seyahatle ulaşılamaz** — sadece tamamlanmış Crown, Hollow Throne'un kendisi, ya da en derin siteler (Bonewrights' Hall gibi) üzerinden bir geçişle. "Gün" kavramı geçerli değil. |

---

## Emberhold (Perde 1)

- **Nüfus:** ~120.000 (outline'ın kendi rakamı, sabit kanon).
- **Ölçek:** Şehri bir uçtan diğerine yürüyerek geçmek yarım gün ile tam gün arası sürer — Gallowmere ya da Harrowgate'ten çok daha büyük, Karsgate'e yakın ya da ondan biraz büyük bir ölçek.
- **Mahalleler (7):**
  1. **Palace District** — Hollow Throne, Chancellery, resmi saray binaları.
  2. **The Grand Archive Çeyreği** — Concordat'ın başkentteki gücü, kütüphane/arşiv kompleksi. **★ Ayrıca The Grand Spire burada** — Kindled Circle'ın ana merkezi (Grand Archmagister Ebrim Voss), Concordat'ın arşivine tam bir siyasi/entelektüel karşı ağırlık olarak aynı çeyrekte duruyor.
  3. **The Ember Quarter** — yanmış, hiç yeniden inşa edilmemiş, Ash Reeve'in kontrolünde.
  4. **Cinder Cathedral Çeyreği** — Choir'ın kamuya açık yüzü.
  5. **Noble Row** — House Sablewood, House Corr, House Ilvane konakları (üçü de aynı geniş mahallede, ayrı bloklar).
  6. **The Reeks** (Karsgate'teki isimle bilinçli bir eko, ama farklı bir yer) — Sunken Ledger'ın olduğu yeraltı/liman-yakını mahalle.
  7. **Old Quarter** — Kule-i Mensuh'un bulunduğu, çoğu terk edilmiş eski akademi bölgesi.
- **Ziyaret noktası sayısı — düzeltildi (2026-09-11, oyuncu: "120.000 nüfuslu şehirde bu kadar az nokta olmaz"):** 13 dungeon-ölçekli site (bkz. `chapter-2-dungeon-directory.md`, Perde 1 — The Grand Spire eklendi, #31) + tahminen **30-40+ küçük ölçekli nokta** (dükkanlar, hanlar, tapınaklar, loncalar — Karsgate'in Hall of Wards/Wagered Crown/Drift Market'ine eşdeğer, ihtiyaç oldukça isimlendirilip eklenecek, hepsi önceden üretilmeyecek — erken üretimin bayatlama riskini önlemek için).

## The Sundered Reach (Perde 2)

- **Nüfus:** Neredeyse hiç sivil yok — bir sınır bölgesi/harabe ülke. Kar Vaelth'te ~40-60 ateş devi (Umm-Halad hariç, o ayrı yaşıyor). Dağınık, isimsiz birkaç mülteci/münzevi kampı olabilir, ihtiyaç oldukça DM tarafından eklenir.
- **Ölçek:** Krallığın kendisinden daha büyük bir vahşi bölge — dört ana site (Frostmere, Kar Vaelth, Bonewrights' Hall, Screaming Fen) birbirinden günlerle ayrı, aralarında gerçek, doldurulmamış vahşi doğa var (travel.py ile roll edilecek, Chapter 1'in Thornlands/Cindermoor tablolarına eşdeğer yeni bir bölgesel tablo gerekecek — henüz `reference/travel-encounters.md`'ye eklenmedi, bir sonraki ihtiyaç anında yapılmalı).
- **Ziyaret noktası sayısı:** 10 dungeon-ölçekli site (bkz. dungeon directory, Perde 2) — bu bölgede küçük ölçekli "dükkan" tarzı noktalar yok, tamamen vahşi/keşif odaklı.

## The Grey Kingdom (Perde 3)

- **Nüfus:** "Her sovereign who ever wore the Crown" — binlerce ölü soylu + onların kendi ash-grey halkı, outline'ın kendi tabiriyle "content" bir şekilde hüküm sürüyorlar. Gerçek bir sayı vermek anlamsız — bu bir yankı-krallık, Emberhold'un kendi nüfusunun ölü bir yansıması.
- **Ölçek:** Emberhold'un birebir coğrafi yansıması — aynı sokaklar, aynı mahalleler, ash-grey ve nüfusu ölü.
- **Ziyaret noktası sayısı:** 8 dungeon-ölçekli site (bkz. dungeon directory, Perde 3) — bu bölge, doğası gereği (bir yankı, sınırlı bir final perdesi) daha az küçük-ölçekli yan nokta içeriyor, kasıtlı olarak yoğunlaştırılmış.

---

## Notlar
- Bu dosyadaki tüm sayılar **tahmini/DM-tarafı sabit** — `travel-times.md`'nin kendi kuralıyla aynı: gerçek oyun bir rotayı/ölçeği değiştirirse, o zaman (ve sadece o zaman) güncellenir, önceden tahmin edilerek değil.
- **Travel-encounters.md — hangi bölgeler gerektiriyor, hangileri gerektirmiyor (2026-09-11 netleştirildi):** Şehir-ölçekli yerler (Emberhold, Grey Kingdom) kendi İÇİNDE bir travel tablosu gerektirmez — Chapter 1'de Karsgate/Gallowmere/Harrowgate'in hiçbiri kendi içinde travel.py kullanmadı, sahne-sahne oynandı. Sadece ONLARA GİDEN yol gerektirir (tıpkı "Karsgate Yaklaşımları" gibi). İkisi de artık tamam: **"Emberhold Yaklaşımları"** (Harrowgate↔Emberhold, seviye 11-14) ve **"The Sundered Reach"** (seviye 15-17) — bkz. `travel-encounters.md`. Grey Kingdom zaten normal seyahatle ulaşılmadığı için hiç gerektirmiyor.
