# salt-lantern — campaign folder (fixture)

This is a **test fixture**: a hand-written micro `short` bible in the designer's layout (plan 24.3, slice 0). It is never played; it exists so every schema has a real instance and slice 1's scripts, prompts and validator can be tuned against it without a full birth.

Reading line for a real campaign in this layout (owner decision 24.6 #1):

- **Player-open:** `design/player-primer.md`, the player map, the approval cards, and each PC thread's public face (`design/threads/*.md`).
- **DM-open, player-avoid:** everything else under `design/` outside `dm-only/`, plus `factions.json`, `goals.json`, `graph.json`, `news.json`.
- **DM-only:** `design/dm-only/**` — the canonical registry, every Secret section, the dice log of secret rolls. The owner-player never opens it; the conductor never reads it; only fresh-context agents do, through the read guard.
