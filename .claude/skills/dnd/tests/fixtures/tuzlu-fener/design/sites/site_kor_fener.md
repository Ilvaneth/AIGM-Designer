---
entity: site_kor_fener
type: site
secrecy: public
phase: P6
status: skeleton
stamped: [danger_tier, room_count, act, thread, key_npcs]
covers: [item_kandil_muhru]
mirror: design/dm-only/sites/site_kor_fener.md
---

# Kör Fener — skeleton

## Public

- **Kind / role:** dungeon (planned: kule) · standard
- **Region:** [[region_tuz_ovasi]] · **Act:** 1 · **Danger tier:** **T2** (CR 3-6) · **Room count:** **14** (band 11-19)
- **Thread / trigger:** [[beat_1c]] — Fener'in kime yanacağı burada belli olur.
- **Payoff:** plot_item — [[item_kandil_muhru]] (Kandil Mührü, nadir, uyum) ve kandil odası
- **Key NPCs:** Divan'ın kâtibi (kimse görmez; gün 75'ten sonra burada)
- **Occupants (ecology summary):** Kırk yıllık bekçi (`ghast` çatısında Tuzbağlı, elite; kandili korur), 4 Tuzbağlı ([[creature_tuzbagli]], minion; Fener'e "okunmuş" gelenler), martı ve tuz. Gün 75'ten sonra Divan hizmetlileri (`acolyte` ×2).
- **Attitude to intruders:** test (bekçi yalnızca kandil taşımayana saldırır; kâtip konuşur)

### Telegraphs
| Distance | Telegraph |
|---|---|
| far | Burundan gece bakınca fener sönük, ama camı buğulu: içeride sıcak bir şey var. |
| near | Patikada tuz kabuklu izler yukarı çıkıyor, aşağı inen yok. |
| threshold | Kapıda Divan mührü, taze balmumu. |

### Escape geometry
Kule dıştan sarmal; her katın balkonu var, deniz tarafına atlanır (2d6, cezirde kayaya 4d6). Tünel (Gelgit Mağarası) tek yön içeri.

### If never visited
Gün 75'te kandil taşınır (op_divan_1.step_4), gün 96'da Fener yanar ve kâtibin adı kıyıdaki her kafaya yazılır (doom). Fenerli bir sabah uyanır ve herkes aynı adı bilir, kimse kendi ölülerinin adını hatırlamaz.

- **Reoccupation candidate:** [[faction_divan]]
- **Intended path:** yes · **XP budget:** 2200

## Discoverable

- Kırk yıl önce bekçi "okundu" ve dönmedi ([[event_fener_sondu]]); yaşlılar bunu söyler.
- Kulenin altına deniz tarafından bir tünel açılır; Kardeşlik bilir, söylemez.
