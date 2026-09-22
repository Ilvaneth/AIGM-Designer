# Session 12 — Conversation Log

**Campaign**: Ashen Crown
**Date**: 2026-09-03
**Starting Location**: Outside Kesh Deeps, the Cindermoor — day 56, evening

*Recovered retroactively from the raw session transcript via `/dm-recover-session-log`, after a context-window compaction left the normal incremental log empty. Session 11 was a pure design/tooling session (no in-fiction play); this session picks up exactly where session 10 left the party. Extensive system/tooling work (script fixes, `CLAUDE.md` trimming, a full Turkish-content purge of system files, `bug-log.md`/`system-register.md` archival, `dm-end-session` scope-narrowing) also happened throughout this session but is out of scope for this log — only in-fiction play is recorded here.*

---

## Scene 0 — A bookkeeping correction: the gibbering mouther

Before any new play, the DM asked Claude to re-verify whether Shestendeliath Hold's lower cistern (a gibbering mouther) had actually been cleared. Cross-checking `session-9-conversation.md` against `shestendeliath-hold.md`, `state.md`, and `session-log.md` confirmed a real state-drift bug: the fight *had* happened in session 9 (Scene 7 — 225 XP each, 55 gp and a Potion of Healing already on both character sheets), but three files still read "not encountered." The root cause was a bug in `location_resolution_check.py` itself — its marker regex matched "ENCOUNTERED" inside the literal text "NOT ENCOUNTERED," permanently suppressing a claim that should have kept resurfacing. Both the script and the stale content were fixed the same turn; Shestendeliath Hold is now fully closed out (garrison, great hall, lower cistern all resolved, Kethrax Allied at the gate). This was a records correction, not new play — no new scene occurred at the Hold.

---

## Scene 1 — Departure from Kesh Deeps — the marginal note

Sorting through the Kesh Deeps dig's own duergar records near Kaelth Ashborn's memorial chamber before departing, the party found a half-legible marginal note from an earlier surveyor:

> *"...ve yüksek moor'da, dağa oyulmuş mühürlü kapı — üç adam yuttu, hiçbirini geri vermedi. Duergarlar bile oraya yaklaşmıyor, batıl inanç diyorlar. Ben de öyle diyorum artık."*

No name, no date — dismissed by the duergar themselves as superstition. This became the party's real lead toward **The Maker's Undoing** (level 5-7, standalone, faction-free), roughly a day and a half to two days' travel into the Cindermoor's higher, more barren reaches.

*(An earlier attempt to reach the party via Kessra Vane's contact token — narrated as a two-way message — was caught and retracted by the DM: the token is a one-directional contact method only, per her own file. That scene never happened and is not part of this log.)*

The party initially set out toward Harrowgate instead (Tain's research, Roskel's second summons, the restoration). **That first night's travel — a 4-Wolf pack ambush on the Harrowgate road — was played out in full and then explicitly cancelled and deleted by the DM** ("Son gece iptal. Tamamını sil.") once the party redirected toward the Kesh Deeps clue instead. It is not part of this log or this session's canon.

---

## Scene 2 — Night 1, Cindermoor road — Perrine Oskold

*(See combat log: session-12-combat-perrine-oskold.md)*

Following the real clue, the party set out into the Cindermoor toward The Maker's Undoing. Near a stone barrow, they found a second Concordat archivist at work — a gnome woman, meticulous, cleaning carved symbols by lantern-light, wearing the same grey-ash Concordat travel cloak as Nessa Wren. Kriv approached from behind intending a direct kill, as with the previous archivist; his stealth failed at the last moment, and she nearly escaped before Ilvaneth's Wand of Magic Missiles ended it in a single volley.

Her effects — a survey notebook, Concordat travel authorization papers naming her **Perrine Oskold**, and 15 gp — confirmed she was on the same barrow-survey assignment as Nessa Wren, and had been overdue for a planned rendezvous with her. The party preserved her body with Gentle Repose and added it to the Bag of Holding, beside Nessa Wren's. `info/consequences.md`'s "Ashlord Concordat — Missing Archivists" threshold now sits at **2/3**.

---

## Scene 3 — Night 2, Day 57 — the rival relic-hunter

After a full rest, the party continued toward The Maker's Undoing. Before making camp, a figure was spotted watching from a rock's shadow — a heavily-built half-orc woman, road-worn leather armor, a mining pick and a map tube on her back. She closed the distance without fully committing, wary but not hostile:

> **Unnamed relic-hunter:** "Bu toprakları biliyorum, yabancılar bilmez. Siz de mi aynı hikayeyi duydunuz — dağa oyulmuş kapı, kimsenin geri dönmediği?"

She was independently chasing the same "sealed door" rumor as the party — not Kessra Vane, someone entirely new, and she never gave a name. Ilvaneth talked her down (Deception 10+4=14 vs her wariness) into believing the party wasn't competition. Kriv made small talk, drawing out one useful thread: someone in Karsgate has been asking unusually pointed questions of local merchants lately — she doesn't know who, and doesn't want to.

Rather than let her walk off toward the same dungeon unmonitored, the party made a deliberate call: **follow her in and let her draw out whatever's waiting inside first.** Both PCs succeeded on the trailing Stealth check (Kriv 13+1=14 vs her passive Perception 15 — a near miss that put her slightly more alert but not aware; Ilvaneth 15+4=19, clean). About half an hour later she reached the mountain's rocky shoulder and the half-hidden Cave Mouth, and went straight in.

---

## Scene 4 — Arrival at The Maker's Undoing — Room 1 (Cave Mouth) & Room 2 (Bone Midden)

*(See combat log: session-12-combat-room2-bone-midden.md)*

The party's actual first-arrival cinematic for the dungeon itself was delivered slightly late — narrated retroactively once the fighting had already started, and logged as a missed trigger per `cinematic-moments.md`. The wide→close, once written:

> *Cindermoor'un yüksek kesimleri, gündüz bile griye çalan bir ışıkla aydınlanır — rüzgârın hiç durmadığı, ağaçsız, kayalık bir yayla. Buraya kadar gelen çok az kişi, geri dönenler daha da az. Dağın yamacında, otların ve döküntülerin arasında yarı gizli bir yarık: insan eliyle açılmamış gibi duran ama insan eliyle kapatılmış olduğu belli bir mağara ağzı, kesme taş izleri hâlâ görünür kenarlarında.*
>
> *İçeride hava değişir — nem, toz, ve altında bir şey daha: metal, kül, uzun zamandır kimsenin dokunmadığı bir işçiliğin kokusu.*

Following the relic-hunter into Room 2, a scream broke the silence — a Cockatrice had ambushed her, nearly petrifying her before she wrenched free on a last-second save. The party chose to intervene, killing the Cockatrice in a single round. Kriv then turned his intimidation on her directly, taking her (limited) surface map before letting her flee for good.

Searching the room afterward (Ilvaneth, Kriv assisting) turned up **Resonance Key 1** and the first fragment of Marek Stillwright's own journal — the opening line of what will become a three-part sequence needed to solve Room 18's puzzle.

---

## Scene 5 — Room 3 (The Nesting Cave)

*(See combat log: session-12-combat-room3-nesting-cave.md)*

Advancing carefully, Ilvaneth scouted ahead and spotted two more Cockatrice nesting together — but Kriv's own stealth check came back a natural 1, and he was spotted before the party could set up an ambush. A single Fireball all but ended the fight before either creature acted: one Cockatrice vaporized outright, the other burned to 8 HP and finished by Kriv. No damage taken. A partial-success Nature check afterward yielded one intact Cockatrice petrification gland — a real, if unplaced, alchemical trade good.

---

## Scene 6 — Room 4 (Old Stair)

No combat. Ilvaneth's passive Perception (15) caught the rockslide trap rigged into the loose stonework before it triggered — Kriv jumped clear, Ilvaneth eased past the edge. The trap remains untriggered.

---

## Scene 7 — Room 5 (The High Ledge)

*(See combat log: session-12-combat-room5-high-ledge.md)*

A Griffon, nesting on a high ledge with Keen Sight, spotted Kriv on approach (Ilvaneth stayed hidden). The fight ended in a single round: Ilvaneth's fully-advantaged Scorching Ray landed all three rays, and Kriv's natural 20 on a Goading Attack — doubling both weapon and maneuver dice on the crit — delivered the single hardest hit of the session (33 damage on one attack, 49 total that turn). The Griffon was thrown from its own ledge. Kriv took 6 damage from its beak; no other losses.

---

## Scene 8 — Room 6 (Broken Gate)

*(See combat log: session-12-combat-room6-broken-gate.md)*

Two more Cockatrice, nesting in the vault's original — breached and warped — outer door frame: the first real sign the mountain had ever been built rather than just wild cave. Ilvaneth was spotted (Cockatrice B bit her for 4, she resisted the petrification save on a 22), Kriv stayed unseen through his opening attacks and dropped Cockatrice A outright. Cockatrice B took two rounds to bring down, attempting to flee at 2 HP before Kriv's opportunity attack finished it mid-air. A follow-up Investigation check turned up **Resonance Key 2** and the second journal fragment. The sequence so far: *"birincisi, dışarının nefesi"* → *"ikincisi, elin ağırlığı."* The third piece is in Room 14.

---

## Scene 9 — Room 7 (Ambush Floor) — threshold, session paused here

The DM flagged mid-scene that room descriptions needed more sensory texture (light, smell, sound) — acknowledged and applied from this point forward. Room 7 was described in full:

> *Koridor genişleyip alçak tavanlı bir depoya açılıyor. Hava burada daha ağır — nem, küf, ve altında tatlımsı, hafif çürük bir koku, tam olarak neyden geldiği belirsiz. Duvarlar boyunca eski ahşap sandıklar istiflenmiş... Odanın ortasında, tek başına duran bir sandık dikkat çekiyor — diğerlerinden biraz daha temiz, biraz daha az tozlu, kapağı hafifçe aralık, içeriden soluk bir metal parıltısı sızıyor.*

Per `the-makers-undoing.md`, Room 7 holds 2 Mimic (Hard-tier for this party) disguised among the crates — the deliberately "too-clean" central chest is the obvious bait. **The party had not yet decided how to approach this room when real play paused** — the rest of this session (through the point this recovery was run) was entirely system/tooling discussion, not further in-fiction content. Room 7 remains unresolved, at the threshold, description delivered but no action taken.

---

## Session end state (as of this recovery)

Party is inside The Maker's Undoing, Wing 1, standing at the entrance to Room 7 (Ambush Floor). Rooms 1-6 cleared; Resonance Keys 1-2 and Journal Fragments 1-2 in hand (Key/Fragment 3 still in Room 14). Both PCs at full or near-full resources aside from what's spent in the logged fights above. No `/dm-end-session` has been run yet.
