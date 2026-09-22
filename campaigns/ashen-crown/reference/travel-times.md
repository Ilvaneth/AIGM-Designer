# Travel Times — Shestendeliath Hold as center

Fixed reference distances, locked in 2026-09-09 (session 24) after a chaining error was caught and corrected live. **Do not re-derive these from scratch — read this file.** A route reached only via a hub can never be shorter than the hub's own distance; these are already chained correctly.

**Oynanmış / sabit (gerçek oyunda gerçekleşti, asla değişmez):**
| Route | Days |
|-------|------|
| Shestendeliath Hold ↔ Greyholt | birkaç saat (aynı gün gidiş-dönüş) |
| Shestendeliath Hold ↔ Harrowgate | 1,5-2 gün |
| Shestendeliath Hold ↔ Gallowmere | 2 gün |

**Zincirleme hesaplanmış (Harrowgate ya da Gallowmere hub'ı üzerinden, orijinal `campaign-clock.md` mesafe tablosundan türetildi — henüz Hold'dan doğrudan oynanmadı, ama artık sabit kabul ediliyor):**
| Route | Via | Days |
|-------|-----|------|
| Shestendeliath Hold ↔ Thornwick | Harrowgate (+½ gün) | ~2-2,5 gün |
| Shestendeliath Hold ↔ Ostwick | Harrowgate (+1-2 gün) | ~2,5-4 gün |
| Shestendeliath Hold ↔ Cindermoor (Cair Dunnow, Hollowmoor Barrows, Harpy Crags, Kesh Deeps, Drowned Cathedral, The Maker's Undoing, The Unquiet Barrow) | Harrowgate (+3-4 gün) | ~4,5-6 gün |
| Shestendeliath Hold ↔ Sallow Ford | Gallowmere (+2 gün) | 4 gün |
| Shestendeliath Hold ↔ Karsgate | Harrowgate → Millward Crossing (+7 gün toplam Harrowgate'ten) | ~8,5-9 gün |
| Shestendeliath Hold ↔ Emberhold | Harrowgate → **Karsgate** → Emberhold (kampanyanın kendi haritasında doğrulandı, "Bölüm 2" oku Karsgate'ten devam ediyor, Harrowgate'ten değil) | Hold↔Karsgate ~8,5-9 gün + Karsgate↔Emberhold ~4-5 gün ek = **~12,5-14 gün toplam** — bkz. `chapter-2-geography.md`, tahmini/DM-sabit, henüz oynanmadı |
| Karsgate ↔ Emberhold | doğrudan | ~4-5 gün — tahmini/DM-sabit |

**Kural:** Bir yere sadece tek bir hub üzerinden ulaşılıyorsa (haritada Hold'a doğrudan çizgisi yoksa), o yerin mesafesi hub'ın kendi mesafesinden asla daha kısa olamaz — her zaman hub mesafesi + hub'dan hedefe mesafe olarak topla. Yeni bir rota gerçekten oynanırsa, gerçek sonucu bu tabloya işle ve değiştir; oynanmamış sayılar sadece gerçek oyun onları düzeltene kadar sabit kalır.
