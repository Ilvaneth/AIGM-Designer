---
entity: premise_tuzlu_fener
type: premise
secrecy: secret
phase: P1
stamped: [question_tr, signatures, trope_breaks]
mirror_of: design/premise.md
---

# Premise — Tuzlu Fener (dm-only)

## Secret

### The big secret
- **Archetype:** `secret_magic_is_actually` + twist `twist_institution_knows`
- **The truth:** Tuz Hafızası anıyı okumaz, tüketir. Her okuma ölünün son saatini yok eder ve okuyucudan da eş ağırlıkta bir anı alır. Tüketilen anılar kaybolmaz: Kör Fener'in kandilinde birikir. Divan bunu kuruluşundan beri bilir; "tüketilenler defteri" bunun için tutulur.
- **Who knows:** [[npc_s01]] (tamamen), [[faction_divan]] (kâtip dışında yalnızca defterin var olduğunu; [[npc_ilme]] okumanın anı götürdüğünü bilir ve merhamet sayar, defterin amacını bilmez)
- **Why it is hidden:** Okuma bir gelenek olarak kaldıkça kandil dolar; gerçek bilinirse kimse okutmaz ve Fener hiç yanmaz.

### Three-clue trail
| # | Act | Layer | Clue | Placed in | Surfaces how |
|---|---|---|---|---|---|
| 1 | 1 | surface | Yesra kendi anılarının yarısını kaybetmiş ve kaybettiğini bilmiyor | [[npc_yesra]] | aynı hikâyeyi iki akşam farklı anlatır; Insight DC 12 boşluğu gösterir |
| 2 | 1 | investigation | Defter parçası: "tüketilenler" başlığı altında Fenerli ölülerinin adları, Yesra'nın okumalarıyla eşleşir | [[site_batik_iskele]] (6. oda, [[item_tuz_defteri]]) | sandık açılır; adlar Yesra'nın boşluklarıyla eşleştirilir |
| 3 | 1 | deep | Defterin aslı ve el yazısı: İlme'nin değil, Sessiz Kâtip'in eli; kandil odasında biriken ışık adları fısıldar | [[site_kor_fener]] (kandil odası) | odaya girilir; Kandil Mührü kandili söndürebilir |

### The villain's answer
- **BBEG:** [[npc_s01]] (Nerun, Sessiz Kâtip) embodies the answer *"Unutulmak ölümdür; öyleyse ben hiç unutulmayacağım, kim unutulursa unutulsun."*; visibility pattern `behind_visible_front` ([[npc_ilme]] görünen yüzdür).
- **Why they are right, from where they stand:** Öte yoksa hatırlanmak tek yaşamdır; Nerun yüz yılın tüketilmiş anılarını bir tek ada dönüştürerek kıyının ilk ölümsüzü olmak ister. Divan'ın her okuması onun mantığını doğrular: halk zaten hatırlanmak için ölülerini tüketiyor.

### DM pitch
Divan'ın sessiz kâtibi Nerun, yüz yılın tüketilmiş anılarını Kör Fener'de yakıp kendi adını kıyıdaki her kafaya yazmak istiyor. Parti bir hancının borcuyla başlar, bir okuyucunun boşluklarıyla şüphelenir, bir defter parçasıyla emin olur ve doksan altıncı günde Fener'in kime yanacağına karar verir. Draskun tuzu taşır, İlme merhametle yanılır, Yesra bedeli önceden ödemiştir. Parti geç kalırsa Fener yine yanar; dünya ölçeklenmez.

### Signature mechanic
`short` never rolls one — yok.
