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

## Amendment to 21a part 2 (owner-approved rows, 2026-10-07)

The mechanism (the coding tab's proposal, accepted): every spine row carries `ends_short: [end_a, end_b]`; every generic role carries a `noun`; the story sentence and the prize phrase read "<noun> of <end short>" for a generic side seated at an end. **The generic roles** (`generic: true`): `divided_city` a/b, `merchant_house_divides` a/b, `foreign_envoy` a/b, `war_fed_company` a/b, `fallen_state_remnant` a/b, `shapeshifter` a/b, `relic_pieces` a/b, `two_empires` a/b, `fiend_pact` b only.

**The nouns:** shapeshifter "the household"; merchant_house_divides "the house"; foreign_envoy "the power"; war_fed_company "the country"; fallen_state_remnant "the new power"; relic_pieces "the house"; two_empires "the empire"; fiend_pact b "the rival house"; divided_city "the half of the city".

**`divided_city`** (the owner's choice): both halves stay seated in the heart; each half faces one end and is named "the half of the city toward <end short>" (a toward end_a, b toward end_b).

**The ends' short names:**

| Spine | end_a | end_b |
|---|---|---|
| river_to_sea | the source | the delta |
| great_rift | the rift floor | the rims |
| mountain_passes | the wet slope | the dry slope |
| long_coast | the fjords | the warm bays |
| barren_corridor | the eastern end | the western end |
| lake_basin | the basin | the far mountains |
| lone_mountain | the summit | the foot |
| star_crater | the crater | the outer lands |
| oasis_ring | the oasis | the far desert |
| crossroads | the north | the south |
| archipelago | the inner islands | the outer islands |
| valley_maze | the high valley | the low valley |
| forest_clearings | the clearings | the deep forest |
| mesa_land | the mesa tops | the canyons |
| lake_chain | the upper lake | the lower lake |
| three_depths | the surface | the deep |
| terraces | the high terrace | the low plain |
| two_worlds | this world | the other plane |
| mountain_within | the outer slopes | the inner halls |
| above_below_sea | the coast | the deep sea |
| peninsula | the tip | the mainland |
| strait_two_continents | the western shore | the eastern shore |
| long_wall | the lands within | the lands beyond |
| climate_belt | the frozen north | the scorching south |
| edge_of_civilisation | the known lands | the wild |
| titan_back | the head | the tail |
| floating_archipelago | the high islands | the low islands |
| void_ring | the near side | the far side |
| giant_tree | the branches | the roots |
| world_edge | the inner lands | the cloud sea |

A generic side seated elsewhere than an end (the heart, beside the key place) is named "<noun> of <that part's short>". **Added test:** over the corpus every generic side in a story sentence reads through its noun and a seat, and the two sides of one contest never read the same.

## Part 21c — the guard reads inside a wrapper (owner-approved 2026-10-07)

Found at 21b's audit: a recursive search wrapped in another command passes the guard, because the guard judges a segment by its first word. Most of these passed before 21b too; one got slightly worse (`bash -c "cd x; grep -r y ."` was split by the old regex and is now quoted text). **A third green commit after 21a:** `Plan item 25, build 21c: the guard reads inside a wrapper`.

The guard unwraps before it judges a segment:
- **a command string:** the string argument of `bash -c`, `sh -c`, `zsh -c`, `eval`, `powershell` / `pwsh` `-Command` / `-c` (and `-EncodedCommand`, refused outright while a marker is armed, since it cannot be read), `Invoke-Expression` / `iex`, `cmd /c` is parsed as commands, recursively;
- **a prefix:** `env` (with its `VAR=value` arguments), `sudo`, `time`, `nohup`, `command`, `exec`, `nice`, `timeout <n>`, `xargs` (with its options) and `&` / `.` in PowerShell are skipped to the real command word;
- **a grouping:** a leading `(`, `{` and their closers, and a process substitution `<(...)` / `>(...)`, are commands like `$(...)`.

**Tests:** every case above with `grep -r`, `find`, `ls -R` and `Get-ChildItem -Recurse` on a parent folder of dm-only is refused; the same words as text inside a `bash -c` string's own quotes (`bash -c 'echo "grep -r"'`) pass; 21b's text cases still pass.

## Part 21d — the door counts the pitch too (owner-approved 2026-10-07)

Read in the fourth birth's premise: the player pitch's first two sentences ran past sixty words each, though the prompt asked "three sentences"; 21a's prompt now says "three short sentences", but nothing gates it. **A fourth green commit:** `Plan item 25, build 21d: the door counts the pitch`.

1. **The door** refuses a premise row whose `pitch` is not three sentences, or holds a sentence past 40 words, naming the sentence's number and its count (the retry prompt carries it). A sentence ends at `.`, `?` or `!` followed by a space or the end; a question mark inside quotes ends nothing. The prose file's pitch section and the row's `pitch` stay the same text (the door already compares them, or it does so now).
2. **The prompt** says it: three sentences, each at most about thirty words; the land's breaks and the costs are said elsewhere (the trope breaks, the sides' lines), not in the pitch.
3. **`rubric_p1_legible`** fails a pitch a player cannot read aloud in under half a minute.

**Tests:** a pitch of four sentences and a pitch with a 41-word sentence are refused with their counts; the fourth birth's pitch is refused; a pitch of three 30-word sentences passes; the prompt's and the rubric's words.
