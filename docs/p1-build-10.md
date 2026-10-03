# Build item 10 — P1 step 2 by script: the identity's rolls

*Written by the development (design and review) tab for the coding tab, 2026-10-03. The design is plan item 25 (step 2 and "Review of the whole P1"), errata 24.2 #22, and the rulings of `docs/p1-tags.md`. All the data this item reads is in the tables since builds 7c, 8 and 9; this item writes the rolls that read it. Where a source and this file differ, stop and report.*

**What it closes.** The whole-P1 measurement after builds 7a to 8 (`docs/p1-tags.md`): four things still wrong in most births, all of them rolls: the people's role against the lineage (4.1 %), the institution's practice against its role's archetype (69.6 %), a user rolled for a rule nobody uses (69.1 %), a question from outside its contest's family (77.1 %).

**Two green commits, in this order.** After each: the full suite green (the exit code), no commit before the audit, no push.

| Part | What | Commit message |
|---|---|---|
| 10a | the public identity: trope breaks, people, institution, phenomenon, question; the old rolls and the old sub-tables go | `Plan item 25, build 10a: P1 step 2 by script, the public identity` |
| 10b | the secret and the villain rolled in P1; P4 reads them | `Plan item 25, build 10b: the secret and the villain rolled in P1` |

**Limits.**
- The naming rolls stay as they are (item 11). The promise ledger, the door, the writer's prompt, the critics and the card are items 12 to 14: here, keep `phase P1 begin` and the present card working with the least change, and list in the summary what you had to adapt.
- An override is still data: collect the rolled rows' overrides into the record, apply none (the one P2 already applies stays).
- Legacy births (no identity record) keep loading; `test_regression_births` stays green.
- Run nothing that calls a model. No secret row in a summary.

---

## The order of step 2

After the foundation (step 1, unchanged): **trope break(s) → people → institution → phenomenon → question(s) → secret → villain → the signature-mechanic gate.** Every draw goes through the arbiter against everything rolled before it, as in step 1.

## Part 10a

### 1. The trope breaks

- Count by scale: 1, 2, 2. The second comes from another family (`families_distinct`, build 7a).
- **The "new prohibition" scar.** When `scar_new_taboo` is among the scars, the **first** trope break is drawn from the rows with `prohibition: true`, and its tie is `tie_break`, not rolled. This forced tie is the one exception to "`tie_break` conflicts with `time_coming`" (under "coming" the taboo reads as the break's first sign).
- **The tie of every other trope break:**
  - when one of the trope row's own weights holds on a rolled **lifeline, contest or ruin source** row, the tie is that piece (`tie_lifeline`, `tie_contest`, `tie_ruin_source`) and is not rolled; when several hold, the largest weight wins, then the order lifeline, contest, ruin source;
  - otherwise the tie is rolled from the tie table (the arbiter keeps `tie_break` out under `time_coming`).
- **Merge rules.** When a trope break is rolled beside a row its `merges_with` names, record the merge. Two of them change the contest's role hints for everything after: `break_dragons_rule` with `contest_humans_dragon` (role `b` → `state`, role `a` → `resistance`); `break_the_enemy_won` with `contest_occupier_resistance` (hints unchanged; the record says the victors are role `a`).

### 2. The people signature

- **Home:** the lifeline; the scar `scar_new_people`, when rolled, is the home instead.
- **The people's role.** When the main contest holds a role with `people_role: true` that the scale seats and the break did not destroy (the struck role under an action that destroys a role), the signature people **is** that role.
- **Lineage:** forced when the role says `lineage_forced`; otherwise rolled with the table's weights, the role's `lineage_weight` when it has one, and, under `break_lineage_homes_inverted`, the palette weights inverted (a weight whose condition names palette kinds applies when the condition does **not** hold).
- **Traits:** one `visible` and one `behaving` row. `trait_won_by_the_break` is drawn only when the people holds no role or its role is the foundation's winner.
- **Attitude:** rolled.

### 3. The institution signature

- **Home:** one of the main contest's seated roles that has an archetype hint (after the merge rules), that the people did not take and that the break did not destroy; rolled among them. Report in the summary whether a birth can be left with no such role, and how often.
- **Practice:** drawn only from the rows whose `hints` hold the role's archetype.
- **Form:** the practice's `form` when it names one; otherwise drawn from the forms whose `hints` hold the archetype.
- **Power:** drawn from the powers whose `hints` hold the archetype.
- **Sign:** rolled freely.

### 4. The phenomenon signature

- **Home and rule:** the ruin source's strangeness, the rule drawn from the ruin's `olgu_families`; with `scar_magic_rule_changed` the home is the break and the rule comes from the family `born_of_break` alone.
- **Sign and limit:** rolled.
- **User, by the rule's `kind`:** `spell` → `user_casters`, not rolled; `self` → `user_no_one`, not rolled; `usable` → rolled among the rule's `users` when it lists them, otherwise among the user rows except `user_no_one`.

### 5. The question

- One per contest (scale: 1, 1, 2), each drawn only from the rows whose `families` hold that contest's family; the second excludes the first. The `tension.second` d2 roll goes.

### 6. What goes

- The old rolls `sig_phenomenon`, `sig_people`, `sig_institution` and the old sub-tables `phenomenon`, `people`, `institution` of `signatures.yaml`, with every reference to them.
- The question's old ×3 weight (`family_weight`): the family is now the heading.

### 7. The record

`design.json#identity`, public and stamped like `#foundation`, printed at preroll: the trope breaks with their ties and merges; the people (home, role, lineage, traits, attitude); the institution (role, archetype, form, practice, sign, power); the phenomenon (home, rule, kind, sign, limit, user); the question(s); the overrides of every rolled row, as data.

### Tests of 10a (thousands of seeds, every scale, magic, era and tone)

- No conflicting set (rows and tokens); no empty pool.
- The people's role and its lineage always agree; the institution's practice, form and power always sit under its role's archetype; the user always follows the rule's kind; every question is of its contest's family.
- With `scar_new_taboo` the first trope break is a prohibition tied to the break; a fit bond sets the tie; `tie_break` never stands with `time_coming` otherwise.
- The floor, reported per table: practices per archetype after the constraints, traits by kind, rules per ruin source, questions per family, the prohibition rows at the scar's draw. **If a table whose rows are not drawn again falls under five, do not fail the suite: stop and report the number** (the prohibition draw's worst case is known to be near four).
- The public dice log names no secret row.

## Part 10b

### 8. The secret (every roll secret)

Archetype, chooser, twist, trail, each through the arbiter. When the chooser is `chooser_contest_role`, a further secret roll picks which seated role.

### 9. The villain (rolled secretly in P1; P4 stops rolling them)

- **Visibility, shape, origin** move from `preroll_p4` to P1. P4 keeps the front template, the doom shape, the lieutenants and the BBEG's faction archetype, and reads the three moved rolls where it read its own.
- **The shape and origin pair** is recorded at approve and never drawn again in another campaign (as the break's target and action pair is); the two tables' rows may otherwise repeat. Secret usage stays hashed.
- **The tie to the break** (`antagonists.yaml#break_tie`): when the chooser is `chooser_the_villain` the tie is `bond_caused_it`, not rolled; otherwise it is rolled and `bond_caused_it` is out. The equivalence holds in both directions in every birth.
- **The pole:** a secret roll picks role `a`'s or role `b`'s pole of the main contest's question. The record carries the darkness dial's `majority_pole` beside it.

### 10. The record

The secret and the villain go to dm-only only. The public record and the card show what they show today (the archetype's class, nothing else).

### Tests of 10b

- Over thousands of seeds: no conflicting set across the public and the secret rows; no empty pool; the chooser and tie equivalence; no forbidden shape or origin; the archetype pool's floor.
- A secret row never appears in `design.json`, in the public dice log or through a die's size.
- P4's preroll reads the moved rolls; no label is rolled twice; a birth that already holds P4 rolls from before (a legacy birth) still loads.
- The shape and origin pair is written at approve, hashed, and excluded in the next birth.

## The summary (each part)

Changed files; new and changed tests; the suite's count and exit code; the floor's report; what was adapted to keep `phase P1 begin` and the card working; anything unexpected.
