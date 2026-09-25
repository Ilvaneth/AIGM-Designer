---
entity: npc_ilme
type: npc
secrecy: secret
phase: P5
stamped: [faction, secret_tr]
mirror_of: design/npcs/npc_ilme.md
---

# Ilme Lampwright (dm-only)

## Secret

- **Secret:** Okumanın anıyı götürdüğünü bilir ve bunu merhamet sayar; defterin Lantern için tutulduğunu bilmez. [[npc_s01]]'in görünen yüzüdür (visibility pattern `behind_visible_front`) ve kâtibin vârisidir.
- **Surfacing path:** Yesra'nın boşluklarıyla yüzleştirilirse savunur; defterin aslını görürse ([[site_blind_lantern]], kandil odası) çöker ve konuşur. [[item_lamp_seal]] Nerun ölürse ona geçer ve Lantern'i kendisi söndürür (beat_1c secondary fallback).
- **Notes for the DM:** Court'un ihanet adayı. Ekran dışında ölmez (load-bearing: 3. ipucunun tanığı). Partiye karşı asla ilk hamleyi yapmaz; kâtip yapar, Ilme açıklar.
