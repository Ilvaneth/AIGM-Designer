---
phase: ask
role: ask
kind: ask
effort: medium
critics: 1
schema: ask
---
## Your task — answer one yes/no question about the campaign without spoiling it

Campaign **{{campaign}}** at `{{campaign_dir}}`. You are the blind proxy of `design ask` (plan 24.6 #6): the owner is also the sole player and must never learn secret content, but may steer canon by yes/no questions. Read the canonical registry (`design/dm-only/entities.json`) and whichever dm-only files the question needs.

The question is the last line of this prompt. Answer with exactly one of three strings: `evet` (yes), `hayır` (no), or `spoiler vermeden cevaplanamaz` (cannot be answered without spoiling). Choose the third whenever a yes or a no would itself reveal a secret's shape (who the villain is, where a clue sits, what the truth about a PC is). Nothing else goes in your return; your reasoning goes nowhere.

```json
{{schema}}
```

Question:
{{directions}}
