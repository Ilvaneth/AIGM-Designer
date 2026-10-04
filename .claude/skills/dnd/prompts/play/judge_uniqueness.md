---
role: judge
kind: uniqueness
schema: judge
---
## You judge whether two births could be the same campaign

Campaigns **{{campaign}}** and **{{against}}** at `{{campaign_dir}}` and its sibling. Read nothing but what is below and, if you need more, the two public premises (`design/premise.md` of each; never `design/dm-only/`). The script already compared names, table rows, maps and rosters: {{script_verdicts}}.

{{premises}}

One finding per check, `pass` / `fix` / `note`, one Turkish sentence each (plan item 22.3, item 4's rubric across campaigns):

- `same_campaign` — could these be the same campaign with the names changed? `fix` if yes.
- `three_sentences_a` — three sentences that could only be true in campaign A, taken from its premise; `fix` if you cannot find three.
- `three_sentences_b` — the same for B.
- `question_distinct` — the two thematic questions differ in kind, not only in wording.
- `signatures_distinct` — no signature of one is a reskin of a signature of the other.
- `defaults_absent` — neither premise makes a people evil by birth (the one unchanging rule; no other theme is excluded, and a classic theme in both premises is no fault by itself).

Overall `fix` if `same_campaign` is `fix` or two other checks are. Return exactly:
```json
{{schema}}
```
