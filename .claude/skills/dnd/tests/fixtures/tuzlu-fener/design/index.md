---
entity: none
type: index
secrecy: public
phase: P8
stamped: []
mirror: null
---

# Master index — Tuzlu Fener

*Generated from the public projection ⊕ overlay at every `save`; never hand-edited. One table per type: id, name, aliases, file, status, seen, region, one line. Secret entities are absent by construction.*

## Settlements and places
| Id | Name | Aliases | File | Status | Seen | Region | Summary |
|---|---|---|---|---|---|---|---|
| settlement_fenerli | Fenerli | — | design/settlements/settlement_fenerli.md | detailed | no | region_tuz_ovasi | Kırık bir dalgakıranın ardındaki tuz limanı |
| settlement_kamisli | Kamışlı | — | design/settlements/settlement_kamisli.md | detailed | no | region_tuz_ovasi | Sazlık Yolu'nun sonunda on dört hane |
| district_iskele | İskele | aşağı mahalle | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Liman, han, pazar |
| district_yukari | Yukarı Fenerli | yukarı mahalle | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Bey konağı, Divan evi, tapınak |
| place_yorgun_marti | Yorgun Martı | han | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | İskele'nin tek hanı |
| place_divan_evi | Divan Evi | — | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Divan'ın taş evi |
| place_bey_konagi | Bey Konağı | — | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Sarven'in konağı |
| place_tuz_pazari | Tuz Pazarı | — | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Rıhtımdaki pazar |
| place_velune_tapinagi | Velune Tapınağı | — | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Denize bakan tapınak |
| place_tuz_evi | Tuz Evi | okuma evi | design/settlements/settlement_fenerli.md | — | no | region_tuz_ovasi | Okumaların yapıldığı ev |

## Sites
| Id | Name | Aliases | File | Status | Seen | Region | Summary |
|---|---|---|---|---|---|---|---|
| site_batik_iskele | Batık İskele | Eski İskele | design/sites/site_batik_iskele.md | detailed | no | region_tuz_ovasi | Çöken eski iskele, Kandil'in sandıkları |
| site_gelgit_magarasi | Gelgit Mağarası | Kardeşlik ini | design/sites/site_gelgit_magarasi.md | skeleton | no | region_tuz_ovasi | Cezirde girilen mağara, Fener'e tünel |
| site_kor_fener | Kör Fener | Fener | design/sites/site_kor_fener.md | skeleton | no | region_tuz_ovasi | Kırk yıldır yanmayan fener |
| site_dipsiz_kuyu | Dipsiz Kuyu | düzlükteki kuyu | design/sites/site_dipsiz_kuyu.md | skeleton | no | region_tuz_ovasi | Tufan öncesi şehrin kuyusu (T4) |

## NPCs
| Id | Name | Aliases | File | Tier | Seen | Location | Summary |
|---|---|---|---|---|---|---|---|
| npc_sarven | Sarven | Bey Sarven, Bey | design/npcs/npc_sarven.md | supporting | no | place_bey_konagi | Fenerli'nin beyi |
| npc_olmar | Olmar | — | design/npcs/npc_olmar.md | minor | no | place_velune_tapinagi | Bey'in yeğeni, Velune rahibi |
| npc_ilme | İlme Kandilci | Sözcü, İlme | design/npcs/npc_ilme.md | supporting | no | place_divan_evi | Divan'ın sözcüsü |
| npc_tolvan | Tolvan | hancı | design/npcs/npc_tolvan.md | supporting | no | place_yorgun_marti | Yorgun Martı'nın hancısı |
| npc_yesra | Yesra Tuzokur | Tuzokur Yesra, Kör Okuyucu | design/npcs/npc_yesra.md | supporting | no | place_tuz_evi | Son tuz okuyucusu |
| npc_draskun | Draskun | Düğümcü | design/npcs/npc_draskun.md | major | no | site_gelgit_magarasi | Kardeşlik reisi |
| npc_kortan | Kortan | — | design/npcs/npc_kortan.md | minor | no | site_batik_iskele | Draskun'un ikinci adamı |
| npc_ameli | Ameli | — | design/npcs/npc_ameli.md | minor | no | settlement_kamisli | Kamışlı'nın sesi |

## Factions
| Id | Name | Aliases | File | Archetype | HQ | Summary |
|---|---|---|---|---|---|---|
| faction_beylik | Sazlık Beyliği | Bey'in adamları | design/factions/faction_beylik.md | state | place_bey_konagi | Tuz vergisi ve liman |
| faction_divan | Yas Tutanlar Divanı | Divan | design/factions/faction_divan.md | guild | place_divan_evi | Okuma ve defter |
| faction_kacakcilar | Gelgit Kardeşliği | Kardeşlik, düğümcüler | design/factions/faction_kacakcilar.md | criminal | site_gelgit_magarasi | Enkaz ve tuz kaçakçıları |

## Gods, planes, ages, events
| Id | Name | File | Summary |
|---|---|---|---|
| god_velune | Velune | design/cosmology.md | Denizin tanrıçası |
| god_ormis | Ormis | design/cosmology.md | Bilginin ve ışığın tanrısı |
| god_isken | İsken | design/cosmology.md | Ölümün tanrısı |
| plane_dipsiz | Dipsiz | design/cosmology.md | Su Düzlemi, dokunulmamış |
| era_tufan / era_fenerler / era_sessizlik | Tufan / Fenerler / Sessizlik | design/cosmology.md | Üç çağ |
| event_buyuk_tufan / event_divan_kurulusu / event_fener_sondu / event_kayip_gemi | Tufan / Divan / Fener / Kandil | design/cosmology.md | Dört olay |

## Arc, chapters, seeds, sockets, threads
| Id | Name | File | Summary |
|---|---|---|---|
| arc_1 | Fener Kime Yanar | design/arc.md | Tek perde, üç beat |
| chapter_1 | Fenerli'ye Varış | design/chapters/chapter_1.md | Seviye 1-3 |
| chapter_2 | Gelgit ve Fener | design/chapters/chapter_2.md | Seviye 3-5 |
| beat_1a / beat_1b / beat_1c | Sandıklar / Okuma / Fener | design/arc.md | knowledge / loss / control |
| seed_martinin_borcu / seed_kamisli_sessizligi | Martı'nın Borcu / Kamışlı'nın Sessizliği | design/arc.md | İki tohum |
| socket_borc / socket_kayip_gemi / socket_divan_egitimi / socket_tuz_okuma | dört soket | design/arc.md | İkisi bağlı |
| thread_selen / thread_vorin | Düğüm / Yemin | design/threads/ | PC iplikleri |
| item_tuz_defteri / item_kandil_muhru | Defter parçası / Kandil Mührü | design/sites/ | plot / signature |
| creature_tuzbagli | Tuzbağlı | design/sites/site_dipsiz_kuyu.md | ghoul reskin |
