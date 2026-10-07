# Build item 21 — the polish the fourth test birth asked for

*Written by the development (design and review) tab for the coding tab, 2026-10-07, after `_test-p1-4` (epic; pipeline clean at its review stop: the door passed every unit on the first run, one fix loop, every `D&D:` piece ticked). Two text faults the owner reads on the card, and one false positive of the read guard. The owner approved the work.*

**Two green commits.** After each: the full suite in the background, the exit code read, a summary under "21a" / "21b" in `docs/reports/item18-coding-summaries.md`, a message to the design tab; no commit before its answer; never push.

| Part | What | Commit message |
|---|---|---|
| 21a | the question is short; the story sentence names a generic side by its seat | `Plan item 25, build 21a: a short question and named sides` |
| 21b | the read guard reads command words only | `Plan item 25, build 21b: the guard reads command words, not text` |

## Part 21a

1. **The question is one sentence per contest, short.** In the fourth birth each contest's question ran to about a hundred words (the critic's fix poured the costs into it) and the card could not be read. The prompt says: one sentence per contest, at most about thirty-five words, the costs said elsewhere (the sides' lines, the stakes); the pitch's sentences stay short too. The door refuses a premise row whose `question` holds a contest's question over forty-five words, naming the contest and the count (the retry prompt carries it); `rubric_p1_question_concrete` fails a question that cannot be read in one breath.
2. **A generic side is named by its seat.** The story sentence read "now one household and the other household fight over an inheritance": the contest table's role texts for some contests are placeholders ("a village or family", "the other", "one half of the city", "one rival", "a country", "its neighbour"). Such roles carry `generic: true` (list them for the audit); the story sentence and the prize phrase name a generic side by where the layout seats it ("the household of the end lake", "the half of the city by the gate"), using the seated part's short name; other sides keep their short labels.

**Tests:** a question over the limit refused at the door with its count; the prompt's rule; over the corpus no story sentence names a side by a generic placeholder.

## Part 21b — the guard reads command words, not text

While `_test-p1-4` was armed, 19d's read guard refused one of the design tab's Bash commands because a heredoc's body held the word of a search command: it read the body as commands. The guard parses the command words alone: a heredoc's body, a quoted string's body and a comment are text, not commands. A search command it should catch is still caught whatever text surrounds it.

**Tests:** a heredoc whose body holds "find", "grep -r" or "ls -R" passes; the same words as commands on a parent folder of dm-only are still refused; a quoted argument holding them passes.
