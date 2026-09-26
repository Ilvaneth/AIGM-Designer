# The dry run and the playtest — the protocol for slice 1e

*Plan item 22.2-22.5. Like `docs/tuning-births.md`, this runs in a separate **Opus** tab (effort medium) that never edits the skill, the tables, the prompts or the plan; it writes reports under `docs/reports/` and the Fable development tab analyses and fixes. Findings are ids, codes, counts, paths and exact error text. The Workflow tool needs the owner's opt-in in that tab ("workflow kullan"). Rule 5 of the tuning protocol holds: never a `design/dm-only/…` or `design/_staging/…` path in a Bash command.*

## Part A — the dry-run birth (`_test-dry-1`)

The birth loop of `docs/tuning-births.md` (birth 1, straight through), with these differences:

```bash
py .claude/skills/dnd/scripts/designer.py new _test-dry-1 --scale short --party-size 1 --seed DRY-0001 --lang tr
```

- P1 → P8 exactly as the tuning protocol says (`preroll`, `begin --json`, the Workflow, `merge --tokens --seconds`, `check`, `card`, `approve`; refused units come back through `begin --json`). `phase P8 merge` now renders the primer, `world.md`, `npcs.md`, `design/index.md`, `design/report.md`, `design/travel-times.md` and `reference/travel-encounters.md` itself.
- After P8: the after-P8 block of the tuning protocol, then the **automated leak test** and the **load budget**:

```bash
py .claude/skills/dnd/scripts/design_leak_scan.py -c _test-dry-1 --extra docs/reports/dry-run-1.md
py .claude/skills/dnd/scripts/load_budget.py -c _test-dry-1
```

  Both must pass (exit 0). The leak scan also takes `--journal <the Workflow transcript folder>` to scan the agents' journals; run it once with that folder if the tool result named one.

## Part B — the character and `design integrate` (P9)

`character new` is a DM procedure that asks the player; here the conductor plays both parts from this description, without AskUserQuestion:

> **Persona (fixed for the dry run):** a level-1 human rogue from the start settlement (the map's hub), Urchin background, standard array (DEX first, CHA second), Turkish narration. The player's sentence: *"Bu limanda büyüdüm; kime borçlu olduğumu bilmiyorum ama biri beni tanıyor."* Origin: the hub's polity; answer the primer's socket questions in one line each, as that character would.

1. Follow `SKILL-commands.md → /dm:dnd character new`, steps 1.5 (origin: the primer section of the hub's polity, its socket questions), 1-9 (name-uniqueness check, sheet from `templates/character-sheet.md`, `character.py calc`, the party line in state.md), then register the PC: `registry.py -c _test-dry-1 add --type pc --name "<Name>" --summary "<class, origin settlement>" --origin play --file characters/<Name>.md`.
2. `design integrate`: `preroll --phase P9`, `phase P9 begin --json` (the roster is `thread_<pc>` + `doc_session1`; the JSON says `design-fanout`), the Workflow, `phase P9 merge --tokens --seconds` (it renders the thread's public face under `design/player/` and the indexes), `check`, `card`, `approve`. Record in the report: what the thread writer read, whether the mission is an active verb, whether the session-1 pack has two opening bangs neither in an inn.

## Part C — session 1 with the player agent

The DM is the conductor tab itself, running the load procedure of `SKILL-commands.md` on `_test-dry-1` (steps 0.5-0.9: the clock, the graph, the faction check, the **load pack**, then the recap). Then:

```bash
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 start --pc "<Name>" --persona "<the persona above, in Turkish, three sentences>" --session 1
```

The loop, **ten turns** (a turn = one DM narration + one player answer):

1. Open with one of the session-1 pack's two bangs (never an inn; `scene --enter <place>` first, as load step 5.5 says). Write the narration to the table **and** record it: `playtest.py -c _test-dry-1 turn --dm "<the narration>"` — it prints the player agent's prompt.
2. Spawn the player: the Agent tool, `subagent_type: "player"`, the printed prompt as the task. It returns `{message_tr, rolls[], ooc_tr}`; record it: `playtest.py -c _test-dry-1 turn --player "<message_tr>"` (append the rolls as `(zar: …)` at the end of the message when there are any).
3. Answer as the DM: dice ownership (the player's raw roll + your modifiers; you roll the world's dice with `--owner`), describe before asking, `calendar.py` after every scene, `site_progress.py` if a site is entered, the news voiced through a person. Every scene change: `scene --enter`.
4. After turn 10: `/dm:dnd save` and `/dm:dnd end` as the procedures say (the end pack, `detail` on the 1-3 sites it names, the spotlight ledger), then `playtest.py -c _test-dry-1 stop`.

Then the judges, each one fresh agent (`general-purpose`, effort medium), with the prompt `playtest.py judge <kind>` prints; save each return as JSON and record it:

```bash
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 judge playtest      > judge-playtest.prompt.md
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 judge readability   > judge-readability.prompt.md
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 judge playtest --record campaigns/_test-dry-1/playtest/judge-playtest.return.json
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 judge readability --record campaigns/_test-dry-1/playtest/judge-readability.return.json
py .claude/skills/dnd/scripts/design_leak_scan.py -c _test-dry-1
```

The leak scan now includes the transcript. The owner reads the transcript too (`campaigns/_test-dry-1/playtest/transcript.md`): the agent is a smoke test and cannot measure fun.

## Part D — the second birth and the uniqueness check (`_test-dry-2`)

Part A again with `--seed DRY-0002` (P1-P8 only; no character, no playtest), then:

```bash
py .claude/skills/dnd/scripts/design_compare.py _test-dry-1 _test-dry-2
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 judge uniqueness --against _test-dry-2   > judge-uniqueness.prompt.md
py .claude/skills/dnd/scripts/playtest.py -c _test-dry-1 judge uniqueness --record campaigns/_test-dry-1/playtest/judge-uniqueness.return.json
```

`design_compare` must print DISTINCT (no shared name, no shared row of the unique tables); the judge answers whether the two could be the same campaign.

## The report — `docs/reports/dry-run-1.md`

English, ids and codes only, the tuning report's sections 1-3 for each birth (run, per phase, failures) plus:

4. **Calibration** (plan item 19.7): per phase and in total, agents, wall-clock, tokens; approval waits are zero in auto-approve mode, so the numbers are machine time.
5. **Leak scan and load budget** — the two scripts' last lines, before and after the playtest.
6. **P9** — the thread's read list, the mission verb, the session-1 pack's counts.
7. **The playtest** — turns, rolls made by the player agent, the guard's refusals if any, the three judges' verdicts and their `fix` findings, the DM's own observations (a rule that fired at the wrong moment, a tool that behaved wrongly, a place the procedure fell silent).
8. **Uniqueness** — `design_compare`'s verdict lines and the judge's.

The development tab then fixes what the reports name and records the calibration in the plan (item 19.7 and 24.1 #16).
