# Build item 9 — the audit's row-level corrections (SPOILER: the owner does not open this file)

*Written by the development tab for the coding tab, 2026-10-03. It names rows of the secret and villain tables. The owner, who is also the player, sees only the counts in `docs/p1-tags.md`.*

The audit read all 26 archetypes, 6 choosers, 15 twists, 10 trails, 5 visibilities, 16 usable shapes, 9 usable origins and 6 ties against the seven criteria of `docs/p1-build-9.md`. The tables hold up. Five corrections before the commit:

1. **`secret_world_is_ending_suppressed`, clue `act3`:** "the reckoning, seen whole" uses a word of the ledger cluster. Write it without "reckoning" (for example "the ending's measure, seen whole"). Add "reckoning" to the test's word list.

2. **`shape_collector`:** the rule says what it gathers, not why a decent person could defend it. Give it its reason in the rule (what the completed collection would mend, restore or prevent), in the manner of the warden, the builder and the oath-keeper.

3. **`shape_stranger`:** "a reason the map does not know" names no reason. Say what kind of reason it is (what their own land lost, was promised or was owed here), so that the criterion "a defensible reason" is met by the row and not left to the writer.

4. **Two conflicts to add** (a secret that the foundation already shows half of):
   - `secret_monsters_were_made` with `ruin_failed_experiment` (the ruin shows in public that an experiment reshaped the region's creatures);
   - `secret_land_is_a_body` with `act_true_face` (the break may show in public that the struck place was a living thing; `act_awakened` is already barred).

   The other three public rows that exclude nothing (`ruin_dead_god`, `ruin_departed_god`, `break_dragons_rule`) were re-read and need no conflict: in each the public row tells a different thing from what any archetype hides.

5. **Visibility may repeat.** The approved rule is that a villain's shape and origin **pair** is not drawn again; nothing says so of the visibility, and five rows cannot be a table that runs out. Give `antagonists.yaml#visibility` its own header `avoid_used: false`; its conflict with the public row stays, and the floor no longer applies to it. (Item 10 turns the shape and the origin into a pair that is recorded and never repeated, like the break's target and action; leave them as they are here.)

Accepted as reported: four archetypes removed instead of two (two more could not be told as a break's cause); one twist replaced; the hashed stamp keys for the secret tables; the `bond_` prefix and the `break_tie` sub-table; the chooser and tie tables marked as repeatable; the two renames; only two conflicts between villain rows and public rows (the villain rows are abstract enough).

After the corrections: stamp, the full suite, and the summary in counts only.
