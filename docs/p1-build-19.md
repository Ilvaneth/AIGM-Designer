# Build item 19 — what the second P1-only test birth showed

*Written by the development (design and review) tab for the coding tab, 2026-10-06, after `_test-p1-2` (the first birth on the threat chain; its story reads as a D&D campaign: a marilith that was once a monster hunter, a deceived house besieging the empty throne's city). Five faults it showed, each fixed at its cause. Where this file and `docs/p1-build-18.md` differ, this file holds.*

**Two green commits, in this order.** After each: the full suite (about 25 minutes, run in the background with a long timeout), the exit code read, a summary appended to `docs/reports/item18-coding-summaries.md` under "19a" / "19b", a message to the design tab; no commit before its answer; never push.

| Part | What | Commit message |
|---|---|---|
| 19a | the public face of a deceived hand; the public check line goes; plane names; the pitch carries the question; critics judge their rubrics | `Plan item 25, build 19a: what the second test birth showed` |
| 19b | a villain that hides among people can pass as one | `Plan item 25, build 19b: a hidden villain can pass as a person` |

## Part 19a

1. **The deceived hand's public face.** The card's first line read "An unwitting faction is about to besiege the city inside the mountain": the hand's public subject told the player that the side was deceived, which is the secret's core. A hand's public subject names only what the world sees: `hand_deceived_side` is named by the deceived role's short name ("The richest house is about to besiege …"); that it was deceived lives in dm-only alone. Read every hand's subject for the same fault (a subject that states what the world does not know) and list what you change; the traitor ("a traitor within") and the shapechangers stay unless you find the world could not know them. The writer's prompt says the same for the prose: the public files name the deceived side by its name and never say it was deceived. Test: no public surface (the card, the premise, the rendering, the public ledger) of a birth with the deceived hand carries "unwitting", "deceived" or the hand's row label.
2. **The public "No people evil by birth — checked" section goes.** In both test births it was where the public text leaked (the first: a hint of the undying court; the second: why the house marches). The rule stays, judged by `rubric_p1_forbidden` on the prose; the template loses the section, the prompt stops asking for a public line, and the rubric's question stops expecting one. A legacy premise that holds the section still loads.
3. **No plane is named at P1.** The second birth's mirror named a plane for the thin place (the critic caught it; the door had let it pass, a plane's label being a known word). The thin place's plane is chosen at P2: the prompt says the writer names no plane, and the door refuses a plane's name (the labels of `planes.yaml`) in P1 prose, public or dm-only, with the reason in the retry prompt.
4. **The pitch carries the campaign's question** (the owner's decision, 2026-10-06). The player pitch's three sentences now do three jobs: a threat with a face; the question, asked in this world's words and never answered; the first session's task where step 1 lands. The prompt, the template's comment and `rubric_p1_legible` say so (the legibility rubric fails a pitch without the question; `rubric_p1_question_concrete` judges the question itself, as now).
5. **A critic judges its rubrics' questions only.** The second birth's phase critic sent the premise back for "the pitch omits the question", which no rubric and no prompt asked for then: a whole rewrite round spent on a critic's own taste. The critic prompts say: each finding names the rubric whose question the text fails; a fault no rubric asks about is a `note`, never a `fix`. `design_approval.py critique` refuses a `fix` finding whose rubric id is not among the rubrics the prompt gave that critic.

**Tests of 19a:** the deceived hand's public surfaces (above); the template and the prompt without the check line; a plane's name refused in public and in dm-only P1 prose; the pitch rule in the prompt and the rubric; a `fix` on a rubric the critic was not given refused at the record.

## Part 19b — a villain that hides among people can pass as one

The second birth's villain is a marilith with the visibility "a mystery among candidates": it hides among people the houses already suspect, yet a marilith cannot pass as a person (the writer left it to P4 and P5). A rolled set must be possible at the table:

- **The rule:** the visibilities that hide the villain *as a person among people* (a mystery among candidates; and any other row whose rule says the villain walks among them: read them and list) need a creature that can pass as one: a humanoid, or an SRD creature with the Shapechanger trait, a Change Shape action, or a disguise spell it casts at will or daily (`srd-index-2014.json`'s traits, actions and spells). Otherwise a **mask** is rolled from a small new secret table (a disguise item such as a hat of disguise, a possessed or bound mortal who fronts for it, a mortal agent who wears its name, a glamour bought from a power), recorded in the threat and promised to P4 or P6 (the mask is an item at a site, or an NPC).
- The visibilities that put a face in front of it (behind a visible front, known but the wrong person) or do not hide it (known and untouchable, known but nowhere to be found) need no mask.
- The mask is a fourth candidate for the weakness where it fits (strip the mask and the mystery breaks); the fit list says which.

**Tests of 19b:** over the corpus, no hidden-among-people villain without a creature that passes or a mask; the mask's promise in the ledger; the variety report unchanged in its shares (the families still drawn).

## The summary (each part)

Changed files; the suite's count, exit code and time; for 19a the list of hand subjects read and changed, and two fresh births' story sentences and pitches; for 19b the creatures that pass as people by the SRD, the mask rows, and how often a mask is rolled.

*Also from this birth, for the protocol (the design tab's own): the test birth's conductor no longer runs `designer.py commit` (a test campaign is git-ignored, the command says "nothing to commit", and the permission classifier refused it once).*

## Added from the birth's report (2026-10-06; part of 19a)

`docs/reports/p1-test-birth-2.md` section 6 adds four small faults:

6. **Agents and Bash.** Two critics listed the dm-only directory with Bash and the phase critic wrote its staging critique with a Bash heredoc (the classifier refused the one, the quoting broke the other); the writer wrote a helper script into the conductor's scratchpad. The writer's and the critics' prompts say: list files with Glob, read with Read, write with Write; never Bash on a design path; write no helper scripts.
7. **The report says who asked a fix.** `phase P1 report`'s `fix reasons` line groups its reasons by the critic that gave them (entity critic n, phase critic, wishes).
8. **A promise that flipped is shown.** When a critic judged a promise not kept and a later return kept it, the report says so in one line (`judged not kept, then kept after fix N: <id>`).
9. **The protocol's channel** (the design tab's own): the next protocol says that the review answer comes from the design tab by SendMessage and carries the owner's word.

## Part 19c — the tests never touch a live guard (added 2026-10-06)

Reported by the coding tab during 19a's suite: the tests' marker guard removes `.runtime/active-design.json` at each campaign test's exit, so a suite run in the main working tree during a live birth could disarm that birth's read guard. Every test that arms, disarms or reads the marker works on its own runtime directory (a temporary project root, or an override the paths module honours in tests only), never the project's `.runtime`; a test arms the real marker, runs a campaign test and finds the marker unchanged. One green commit after 19b: `Plan item 25, build 19c: the tests never touch a live guard`.
