---
entity: npc_sarven
type: npc
secrecy: public
phase: P5
tier: supporting
stamped: [faction]
mirror: design/dm-only/npcs/npc_sarven.md
---

# Sarven — Fenerli Beyi

## Public

- **Appearance:** İnsan, elli beş yaşlarında, kısa boylu ve geniş omuzlu; sol elinde tuz yanığından kalma beyaz bir leke, gri pelerinin altında hep aynı yıpranmış deri yelek. Yürürken ellerini arkasında kenetler.
- **Role / CR / location:** Bey, tuz meclisinin başı · CR 3 (`knight`) · usually at [[place_bey_konagi]] in [[settlement_fenerli]]
- **Faction:** [[faction_beylik]] · **Tier:** supporting · **Alignment:** LN
- **Demeanor:** Sabırlı, ölçülü, her sözü meclise dayandırır; konu Kandil'e gelince sesi bir perde alçalır.
- **Speech quirk:** Her cümleye "meclis der ki" diye başlar. · **Voice samples:**
  - *"Meclis der ki, sandık getirene beş altın. Ben derim ki, sandığı bana getirin, meclise değil."*
  - *"O gece fırtınaydı. Meclis der ki fırtınaydı. Başka bir şey söyleyen varsa gelsin, önümde söylesin."*
- **Schedule:** Sabah meclis, öğleden sonra kimseyi kabul etmez; akşam tapınakta yeğeniyle.
- **What they can offer the party / want from the party:** ödül (sandık başına 5 gp), muhafız eşliği, mühürlü kayıt / sandıkları ve kim bulursa onun sessizliğini ister.
- **Attitude toward party:** neutral
- **Current goal:** Kandil'in sandıklarını meclisten önce bulmak (op_beylik_1).

### Personality
- **Trustworthy ↔ Deceptive:** Güvenilir görünür; bir kez sattı ve o bir kez her şeyi belirledi.
- **Ambitious ↔ Content:** Korumacı; yeni bir şey istemez, elindekini kaybetmemek ister.
- **Loyal ↔ Opportunistic:** Beylik'e sadık, kendine değil.
- **Brave ↔ Cowardly:** Mecliste cesur, denizde değil.

### Relationships
- **Heir:** [[npc_olmar]] — yeğeni; oğlu Kandil'de değildi ama meclis öyle sanıyor.
- **Owes:** [[npc_ilme]] — Divan Bey'in borcunu tutar.
- **Fears:** [[npc_draskun]] — manifestoyu ona sattı.

### Known Facts — what they actually know and how
- day 0 — Kandil'in yükünde Beylik'in tuz vergisi vardı — role (Bey; yükleme belgesi)
- day 0 — Kardeşlik enkazı ilk buldu ve sandıkları eski iskeleye taşıdı — told by [[npc_draskun]] (manifesto satışı sırasında)
- day 0 — Divan bu ay üç okuma yaptı, ikisi izinsiz — told by [[npc_ilme]] (borç görüşmesi)
- day 0 — Fener kırk yıl önce söndü, bekçi dönmedi — witnessed (o gece limandaydı, [[event_fener_sondu]])

## Discoverable

- **Motivation with history:** Üç yıl önce ([[event_kayip_gemi]]) Kandil'le birlikte Beylik'in yıllık vergisi battı; meclis o günden beri eksik vergiyi sormaz ve Sarven sorulmasından korkar. Vergiyi bulmak değil, kimsenin aramamasını sağlamak ister.
- **Weakness derived from personality:** Meclis önünde küçük düşmekten ölümden çok korkar; bir tehdit değil bir tanık onu kırar.
- **What changes if they die:** [[npc_olmar]] bey olur, doktrin savunmaya kayar; Bey'in borcu Divan'ın elinde koz olmaktan çıkar, Divan Olmar'ı doğrudan sıkıştırır.
