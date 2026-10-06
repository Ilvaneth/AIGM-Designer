#!/usr/bin/env python3
"""
design_promises.py — the promise ledger (plan item 25, the principle's third rule: every floor is inspected; errata
24.2 #23; docs/p1-build-12.md).

P1 promises the later floors a great deal: the hooks of every rolled row, the overrides nobody applies yet, what the
layout seated, the stubs a phase reserves, the secret's three clues. A promise is a record: what, from which row and
phase, due at which phase, and how it is checked. The ledger is built at P1's preroll, after the naming rolls, and
grows at every merge by what the registry reserved.

  public   design.json#promises          a list
  secret   design/dm-only/promises.json  a promise whose source row is a secret roll, or whose text names one

The public ledger is a function of the public rolls alone: a secret row's promise never joins or removes a public
one (the same sentence due at the same phase from a public and a secret row is one promise in each ledger), so
nothing the owner can read tells what was rolled in secret.

A promise:
  id          `prm_<hash of due and text>` (a secret one hashes its ledger too): the same birth and seed give the same ids
  source      hook | override | foundation | stub | placement | concretise | clue_stage | clue | note (a signature's `appears`)
  from        the row id, the entity id or the foundation piece; `from_phase` the phase that made it
  also        further sources of the same promise (two promises with one due phase and one text are one promise)
  due         a phase (P0-P9), `validator` (the full validator run) or `play` (recorded, never gates a birth)
  text        the hook's `must` sentence or the generated sentence, in English as the tables hold it
  name        the source row's label, for the card (the tables carry no Turkish since build item 13a)
  check       `script:<rule>` where a script can decide today (RULES; a hook names its rule in the table: `check:
              <rule>`), else `critic`
  status      open | kept | not_kept | waived; `verdict` {phase, attempt, by} once judged; `waiver` the owner's sentence

Inspection (Part 12b). `phase check` runs the script rules on every promise due at or before the phase. The phase
critic returns a verdict per critic-judged promise due at its phase; `phase merge` stores id and verdict. The gate:
a due script promise not kept closes it (`promise`), so does a due critic promise without a verdict
(`promise_unjudged`); a critic's `not_kept` does not: the card lists it and the owner decides, by `promise waive` or
a rerun. A secret promise shows nowhere public but as a count and an id.

The sources today are the rows rolled in P0 and P1 (SOURCE_PHASES). A later floor plugs in at two places, each one
line: its phase joins SOURCE_PHASES once its tables' hooks are reviewed (docs/p1-tags.md, rule 9), and a promise a
script can decide gets its rule in RULES. An override is not applied here: it is a promise due at the phase that owns
the default (claims.yaml#defaults); the ones a roll already applies are kept by script.

A legacy birth (no `promises` in design.json) has no ledger and is left as it was built.

  design_promises.py -c CAMP counts [--phase PN]     the ledger's counts (public by due phase and status; secret: three counts)
  design_promises.py -c CAMP list [--phase PN] [--status S] [--secret]
                                                     the public ledger; --secret the secret one (dm-only readers alone)
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import design_dir, dm_only_dir, is_stub, read_json, stamp_meta, write_json_atomic  # noqa: E402

KEY = "promises"                         # design.json#promises
SOURCE_PHASES = ("P0", "P1")             # the phases whose rolled rows are sources; a later floor joins at its turn
DUE_OTHER = ("validator", "play")
DUE_ALIASES = {"names": "P1", "slice2": "play"}     # claims.yaml#defaults: the naming rolls are P1's; slice 2 is play
DUE_ORDER = dm.PHASES + DUE_OTHER
SOURCES = ("hook", "override", "foundation", "stub", "placement", "concretise", "clue_stage", "clue", "note")
STATUSES = ("open", "kept", "not_kept", "waived")
NO_TABLE = ("dice", "tokens")            # dice-log records that name no table row
PART_WORDS = {"key_place": "the key place", "heart": "the heart", "end_a": "the first end", "end_b": "the second end",
              "end_c": "the third end", "end_d": "the fourth end"}
# overrides a roll applies itself, so a script can say they are kept: P2's preroll forces the pantheon type a trope
# break names; P1's naming rolls give language 2 to the contest's other side; P1's lineage roll inverts its weights
SCRIPT_APPLIED = ("pantheon_type", "second_language", "lineage_palette_weights")


def secret_path(campaign: str) -> Path:
    return dm_only_dir(campaign) / "promises.json"


def pid(due: str, text: str, secret: bool = False) -> str:
    """A promise's id. A secret promise's differs from the public one of the same sentence, so an id a gate prints
    never points at a public promise."""
    return "prm_" + hashlib.sha256(f"{'secret|' if secret else ''}{due}|{text}".encode("utf-8")).hexdigest()[:10]


def due_of(phase) -> str:
    """A hook's or a default's phase as a due value that exists."""
    due = DUE_ALIASES.get(str(phase), str(phase))
    if due not in DUE_ORDER:
        raise SystemExit(f"design_promises: {phase!r} is no phase a promise can be due at — a table fault")
    return due


class Ledger:
    """Promises keyed by (ledger, due, text): in one ledger the same due phase and the same text are one promise
    with two sources. The public and the secret ledger never merge into each other."""

    def __init__(self, public=(), secret=()):
        self.items: dict = {}
        for hidden, promises in ((False, public), (True, secret)):
            for p in promises:
                self.items[(hidden, p["due"], p["text"])] = dict(p)

    def add(self, source: str, origin: str, from_phase: str, due: str, text: str, name: str, check: str = "critic",
            secret: bool = False, **extra) -> dict:
        key = (bool(secret), due, text)
        have = self.items.get(key)
        src = {"source": source, "from": origin, "from_phase": from_phase}
        if have is None:
            have = self.items[key] = dict({"id": pid(due, text, bool(secret)), **src, "due": due, "text": text, "name": name,
                                           "check": check, "status": "open", "verdict": None, "waiver": None, "also": []}, **extra)
        else:
            first = {k: have[k] for k in src}
            if src != first and src not in have["also"]:
                have["also"].append(src)
            if check != "critic":
                have["check"] = check
        return have

    def split(self) -> tuple[list[dict], list[dict]]:
        return ([p for (hidden, _, _), p in self.items.items() if not hidden],
                [p for (hidden, _, _), p in self.items.items() if hidden])


# ── the sources ──────────────────────────────────────────────────────────────────────────────────────────────

def rolled_rows(dials: dict, public: list[dict], secret: list[dict]) -> list[tuple]:
    """(table ref, row, the phase that rolled it, rolled secretly) for every row the campaign stands on from the
    source phases: the dial rows and the scale row (P0), every table row of the dice logs (P1)."""
    out: list[tuple] = []
    seen: set = set()

    def put(ref, row, phase, hidden):
        if row and (ref, row["id"]) not in seen:
            seen.add((ref, row["id"]))
            out.append((ref, row, phase, hidden))
    if "P0" in SOURCE_PHASES:
        for dial in ("scale", "tone", "magic", "era", "danger"):
            put(f"dials.yaml#{dial}", dt.dial_row(dial, dials.get(dial)), "P0", False)
        for value in dials.get("content_mix") or []:
            put("dials.yaml#content_mix", dt.dial_row("content_mix", value), "P0", False)
        put("scale.yaml", dt.scale_row(dials["scale"]), "P0", False)
    for recs, hidden in ((public, False), (secret, True)):
        for r in recs:
            ref = r.get("table")
            if r.get("phase") in SOURCE_PHASES and r.get("row_id") and ref and ref not in NO_TABLE and ".yaml" in ref:
                put(ref, dt.row(ref, r["row_id"]), r["phase"], hidden)
    return out


def hooks_of(ref: str, row: dict) -> list[dict]:
    """The row's own hooks and the `hooks_common` its table and its sub-table give it."""
    name, _, sub = ref.partition("#")
    doc = dt.load(name)
    common = list(doc.get("hooks_common") or [])
    node = (doc.get("tables") or {}).get(sub) if sub else None
    if isinstance(node, dict) and node.get("own_hooks_only"):
        common = []         # a public sub-table of a secret file (build item 18c: the hand) takes none of the file's hooks
    if isinstance(node, dict):
        common += list(node.get("hooks_common") or [])
    return list(row.get("hooks") or []) + common


def names_secret(text: str, secret_rows: list[dict]) -> bool:
    """Does a sentence name a secretly rolled row? By its id alone: a label is ordinary words (`the villain`), and a
    public hook that happens to carry them must stay public, or its absence would tell what was rolled."""
    low = text.lower()
    return any(re.search(r"(?<![a-z0-9_])" + re.escape(row["id"].lower()) + r"(?![a-z0-9_])", low) for row in secret_rows)


def place_text(foundation: dict, seat: str | None) -> str:
    """A seat of the layout in words, with its preposition: a part of the spine with the land it lies on, or a
    place along it."""
    parts = foundation["layout"]["parts"]
    palette = {r["id"]: r for r in dt.rows("foundation.yaml#palette")}
    land = lambda k: (palette.get(k) or {}).get("text", {}).get("name") or k
    if seat in parts:
        return f"at {PART_WORDS.get(seat, seat)} ({land(parts[seat])})"
    if seat and seat.startswith("along:"):
        return f"along the spine, on {land(seat.split(':', 1)[1])}"
    return "along the spine"


def levels_text(lo: int, hi: int) -> str:
    return f"level {lo}" if lo == hi else f"levels {lo}-{hi}"


def clue_levels(level_band, top_step) -> list[list[int]]:
    """The secret's three clue stages as level ranges (the owner's ruling 3 of 2026-10-04): the first in the first
    third of the band, the second in the middle third, the third on the escalation's top step, never before the
    second's first level. One rule for every scale and every band."""
    lo, hi = int(level_band[0]), int(level_band[1])
    n = hi - lo + 1
    a = max(1, math.ceil(n / 3))
    first = [lo, min(hi, lo + a - 1)]
    b = max(1, math.ceil((n - a) / 2))
    mid_lo = min(hi, first[1] + 1)
    middle = [mid_lo, min(hi, mid_lo + b - 1)]
    top = [max(lo, int(top_step[0])), min(hi, int(top_step[1]))]
    third = [min(top[1], max(top[0], middle[0])), top[1]]
    return [first, middle, third]


def build(dials: dict, public: list[dict], secret: list[dict], foundation: dict, identity: dict,
          identity_secret: dict | None) -> tuple[list[dict], list[dict]]:
    """The ledger of a birth from its rolls alone (no registry yet): (public promises, secret promises)."""
    import design_foundation as fd
    L = Ledger()
    rows = rolled_rows(dials, public, secret)
    secret_rows = [row for _, row, _, hidden in rows if hidden]

    def add(source, origin, from_phase, due, text, name, check="critic", hidden=False, **extra):
        return L.add(source, origin, from_phase, due_of(due), text, name, check,
                     secret=hidden or names_secret(text, secret_rows), **extra)

    # 1. hooks: every hook of every rolled row, and the common hooks of its table and sub-table
    for ref, row, phase, hidden in rows:
        for h in hooks_of(ref, row):
            add("hook", row["id"], phase, h["phase"], str(h["must"]), row.get("label") or row["id"], check_of(h, row), hidden)

    # 2. overrides: due at the phase that owns the default; two rolled rows with a `combines` line are one promise
    override_promises(rows, add)

    # 3. the foundation's columns: what the layout seated is promised to P3's map; the escalation's steps to P7; the
    #    break as a dated event to P2, the opening to P7, the day-0 news to P8; every scar's named floors
    layout = foundation["layout"]
    life = fd.rows_by_id("lifeline")[foundation["lifeline"]["id"]]
    ruin = fd.rows_by_id("ruin_source")[foundation["ruin_source"]]
    contests = fd.rows_by_id("contest")
    where = lambda seat: place_text(foundation, seat)
    add("foundation", "layout.lifeline", "P1", "P3", f"the map places the lifeline ({life['text']['name']}) {where(layout['lifeline'])}", life["label"])
    add("foundation", "layout.remnant", "P1", "P3", f"the map places the ruin's remnant ({ruin['text']['remnant']}) {where(layout['remnant'])}", ruin["label"])
    add("foundation", "layout.break", "P1", "P3", f"the map shows where the break struck, {where(layout['break_at'])}", "The break")
    for n, seated in enumerate(layout["contests"], 1):
        crow = contests[seated["contest"]]
        for role, seat in seated["seats"].items():
            add("foundation", f"layout.contest.{n}.{role}", "P1", "P3",
                f"the map seats {crow['roles'][role]['text']} {where(seat)}", crow["label"])
        add("foundation", f"layout.contest.{n}.prize", "P1", "P3",
            f"the map places the prize of the contest ({crow['text']['name']}) {where(seated['prize']['at'])}", crow["label"])
    tiers = fd.rows_by_id("escalation_tier")
    band = foundation["escalation"]["level_band"]
    steps = []
    for n, tid in enumerate(foundation["escalation"]["tiers"], 1):
        t = tiers[tid]
        lo, hi = max(int(band[0]), int(t["levels"][0])), min(int(band[1]), int(t["levels"][1]))
        steps.append([lo, hi])
        add("foundation", f"escalation.{n}", "P1", "P7", f"step {n} of the arc is the break at this scale: {t['label']}; the party plays it at {levels_text(lo, hi)}", t["label"])
    brk = foundation["break"]
    action, time = fd.rows_by_id("action")[brk["action"]], fd.rows_by_id("time")[brk["time"]]
    told = next((l["text"] for l in foundation.get("rendering") or [] if l["label"] == "The break"),
                f"{time['text']['name']}: {action['label']}").split(";")[0]
    add("foundation", "break.event", "P1", "P2", f"a dated event of the history is the break ({told})", action["label"])
    add("foundation", "break.opening", "P1", "P7", "the opening meets the break through its target", action["label"])
    add("foundation", "break.news", "P1", "P8", "the day-0 news carries the break's latest sign", action["label"])
    scars = fd.rows_by_id("scar")
    for sid in brk["scars"]:
        row = scars[sid]
        hooked = {due_of(h["phase"]) for h in row.get("hooks") or []}
        for floor in row.get("floors") or []:
            if due_of(floor) not in hooked:
                add("foundation", sid, "P1", floor, f"the scar shows on this floor: {row['text']['name']}", row["label"])

    # 5. what the writer must make concrete: an action row with `concretise: true`
    if action.get("concretise"):
        add("concretise", action["id"], "P1", "P1", f"the premise says concretely what it was in this world: {action['label']}", action["label"])

    # 3b. the move's columns (build item 18d, G6): the start to P3; the public creature families to P6; the villain's
    #     own creatures to P6, secret
    move = foundation.get("move")
    if move:
        add("foundation", "move.start", "P1", "P3", f"the start is a village or a small town {where(move['start'])}, where step 1 of the plan lands", "The start")
        if move.get("families"):
            add("foundation", "move.families", "P1", "P6", "the occupants of the sites and the travel encounters weigh the campaign's creature "
                f"families: {', '.join(move['families'])}", "The creature families")
    facts = ((identity_secret or {}).get("secret") or {}).get("facts")
    if facts:
        add("foundation", "threat.families", "P1", "P6", "the villain's own creatures (" + ", ".join(facts["creature_types"]["secret"])
            + ") stand among the occupants of its sites and its lair", "The villain's creatures", hidden=True)

    # 6. the secret's clues (secret). Build item 18d: three stages, three clues each: the chain's own (`clue_stage`, its
    #    levels the validator reads) and the two promised to P5 and P6 (`clue`); a legacy birth keeps its archetype's three
    stages = ((identity_secret or {}).get("secret") or {}).get("stages")
    if stages:
        for st in stages:
            n, (lo, hi) = st["n"], st["levels"]
            reveal = "; its clues reveal how the villain is stopped" if st.get("reveals") else ""
            chain = st["clues"][0]
            add("clue_stage", f"secret.stage{n}", "P1", "P6",
                f"stage {n}'s first clue ({st.get('shape')}) sits {where(chain['at'])} ({chain['why']}), on a site or a node the party "
                f"plays at {levels_text(lo, hi)}; the stage's conclusion: {st['conclusion']}{reveal}", f"The secret's stage {n}",
                hidden=True, clue=n, levels=[lo, hi])
            add("clue", f"secret.stage{n}.person", "P1", "P5", f"a person holds a second clue of stage {n}, met at {levels_text(lo, hi)}{reveal}",
                f"The secret's stage {n}", hidden=True, stage=n, levels=[lo, hi])
            add("clue", f"secret.stage{n}.site", "P1", "P6", f"a site holds a third clue of stage {n}, played at {levels_text(lo, hi)}{reveal}",
                f"The secret's stage {n}", hidden=True, stage=n, levels=[lo, hi])
    elif identity_secret and identity_secret["secret"].get("archetype") and dt.row("secrets.yaml#archetype", identity_secret["secret"]["archetype"]):
        arch = dt.row("secrets.yaml#archetype", identity_secret["secret"]["archetype"])
        trail = dt.row("secrets.yaml#trail", identity_secret["secret"]["trail"])
        for n, (lo, hi) in enumerate(clue_levels(band, steps[-1]), 1):
            add("clue_stage", arch["id"], "P1", "P6",
                f"clue {n} of the secret ({arch['clue_shape'][f'act{n}']}; the trail carries it as: {(trail.get('acts') or {}).get(f'act{n}') or (trail.get('stages') or {}).get(f'stage{n}')}) "
                f"sits on a site or a node the party plays at {levels_text(lo, hi)}", f"The secret's clue {n}", hidden=True, clue=n, levels=[lo, hi])
    return L.split()


def override_promises(rows: list[tuple], add) -> None:
    """Every override of a rolled row as a promise due at its default's phase (claims.yaml#defaults); where
    claims.yaml#combines names two rolled rows, one promise carries the combined sentence."""
    claims = dt.load("claims.yaml")
    defaults = claims.get("defaults") or {}
    overrides = []
    for ref, row, phase, hidden in rows:
        ov = row.get("overrides")
        for o in ov if isinstance(ov, list) else []:
            if o.get("default") not in defaults:
                raise SystemExit(f"design_promises: {row['id']} overrides {o.get('default')!r}, no default of claims.yaml — a table fault")
            overrides.append((row, phase, hidden, o))
    combined: set = set()
    for c in claims.get("combines") or []:
        both = [x for x in overrides if x[3]["default"] == c["default"] and x[0]["id"] in c["rows"]]
        if {x[0]["id"] for x in both} == set(c["rows"]):
            d = defaults[c["default"]]
            for row, phase, hidden, o in both:
                combined.add((row["id"], c["default"]))
                add("override", row["id"], phase, d["phase"], f"{d['what']}: {c['combine']}", row.get("label") or row["id"],
                    hidden=hidden, default=c["default"], to=c["combine"])
    for row, phase, hidden, o in overrides:
        if (row["id"], o["default"]) in combined:
            continue
        d = defaults[o["default"]]
        applied = o["default"] in SCRIPT_APPLIED and (o["default"] != "pantheon_type" or bool(dt.row("pantheon.yaml#type", str(o.get("to")))))
        add("override", row["id"], phase, d["phase"], f"{d['what']}: {o.get('to')}", row.get("label") or row["id"],
            "script:override_applied" if applied else "critic", hidden, default=o["default"], to=o.get("to"))


# ── the ledger on disk ───────────────────────────────────────────────────────────────────────────────────────

def has_ledger(manifest: dict) -> bool:
    return isinstance(manifest.get(KEY), list)


def load_secret(campaign: str) -> list[dict]:
    return (read_json(secret_path(campaign)) or {}).get(KEY) or []


def save(campaign: str, public: list[dict], secret: list[dict], written_by: str, manifest: dict | None = None) -> None:
    data = manifest if manifest is not None else dm.load(campaign)
    data[KEY] = public
    if manifest is None:
        dm.save(campaign, data, written_by)
    doc = {"_meta": {"schema_version": 1, "campaign": campaign}, KEY: secret}
    stamp_meta(doc, campaign, written_by)
    write_json_atomic(secret_path(campaign), doc)


def build_for(campaign: str) -> tuple[int, int]:
    """P1's preroll, after the naming rolls: build the ledger from the rolls on disk (P1 at its current attempt),
    then add what the registry already holds. A rebuilt ledger starts open: a P1 rerun judged nothing yet."""
    m = dm.load(campaign)
    attempt = int((m["phases"].get("P1") or {}).get("attempt") or 1)
    now = lambda r: r.get("phase") != "P1" or int(r.get("attempt") or 1) == attempt
    log = read_json(dm_only_dir(campaign) / "dice-log.json") or {}
    public, secret = build(m["dials"], [r for r in m.get("dice_log") or [] if now(r)], [r for r in log.get("rolls") or [] if now(r)],
                           m["foundation"], m["identity"], log.get("identity"))
    save(campaign, public, secret, "designer.py preroll --phase P1 (promises)")
    sync(campaign, "P1")
    m = dm.load(campaign)
    return len(m[KEY]), len(load_secret(campaign))


def sync(campaign: str, phase: str | None = None) -> int:
    """After a merge: the stubs the registry reserved (source `stub`, due at their owner phase) and the placements the
    premise made (the god and the event it names, due P2; each clue's place, due P6) join the ledger; an open stub
    promise whose row is gone leaves it. Returns the promises added. A legacy birth has no ledger: nothing is done."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return 0
    canon = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    L = Ledger(m[KEY], load_secret(campaign))
    before = set(L.items)
    for key, p in list(L.items.items()):
        if p["source"] == "stub" and p["status"] == "open" and p["from"] not in canon:
            del L.items[key]
            before.discard(key)
    for eid, row in canon.items():
        hidden = row.get("secrecy") == "secret"
        if is_stub(row) and row.get("owner_phase") in dm.PHASES:
            made = row.get("created_phase") if row.get("created_phase") in dm.PHASES else (phase or "P1")
            # a stub of a type the orphan-stub gate only warns about is listed and judged, and does not close the gate
            minor = {} if row.get("type") in dm.BLOCKING_STUB_TYPES else {"minor": True}
            L.add("stub", eid, made, row["owner_phase"], f"{eid} is written: its row filled and its file on disk",
                  f"a reserved {row.get('type')}" if hidden else str(row.get("name") or eid), "script:stub_written", secret=hidden, **minor)
        if row.get("type") == "signature" and not hidden:
            # build item 13b: where the writer says a signature will appear is a promise to that floor
            for n in row.get("appears") or []:
                if isinstance(n, dict) and n.get("phase") in dm.PHASES and str(n.get("text") or "").strip():
                    L.add("note", eid, "P1", n["phase"], str(n["text"]).strip(), str(row.get("name") or eid))
        if row.get("type") == "premise":
            dm_only = row.get("dm_only") or {}
            pinned = dm_only.get("pinned") or {}
            for kind, rule, text in (("god", "god_registered", "the god the premise names is in the registry"),
                                     ("event", "event_dated", "the event the premise names is a dated event of the history")):
                if pinned.get(kind):
                    L.add("placement", eid, "P1", "P2", f"{text}: {pinned[kind]}", f"The premise's {kind}", f"script:{rule}",
                          secret=True, kind=kind, subject=str(pinned[kind]))
            for c in dm_only.get("clues") or []:
                L.add("placement", eid, "P1", "P6", f"clue {c.get('n')} of the secret has its place: a site, an NPC or an item of the registry",
                      f"The secret's clue {c.get('n')}", "script:clue_placed", secret=True, kind="clue", clue=c.get("n"))
    public, secret = L.split()
    if len(public) != len(m[KEY]) or set(L.items) != before or len(secret) != len(load_secret(campaign)):
        save(campaign, public, secret, f"design_promises.py sync{' --phase ' + phase if phase else ''}")
    return len(set(L.items) - before)


def reopen(campaign: str, phase: str, manifest: dict | None = None) -> int:
    """A phase's rerun reopens the promises that phase judged (a P1 rerun rebuilds the ledger at its preroll)."""
    data = manifest if manifest is not None else dm.load(campaign)
    if not has_ledger(data):
        return 0
    secret = load_secret(campaign)
    n = 0
    for p in data[KEY] + secret:
        if (p.get("verdict") or {}).get("phase") == phase:
            p.update({"status": "open", "verdict": None, "waiver": None})
            n += 1
    if n:
        save(campaign, data[KEY], secret, f"designer.py phase {phase} rerun (promises reopened)", manifest=manifest)
    return n


# ── the script rules that exist today (docs/p1-build-12.md, section 3) ───────────────────────────────────────

class State:
    """What the rules read, loaded once."""

    def __init__(self, campaign: str):
        self.campaign = campaign
        self.manifest = dm.load(campaign)
        self.canon = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
        self.naming = read_json(design_dir(campaign) / "naming.json") or {}

    def named(self, etype: str, name: str) -> list[dict]:
        low = str(name).strip().lower()
        return [e for e in self.canon.values() if e.get("type") == etype and not is_stub(e)
                and low in [str(x).strip().lower() for x in [e.get("name")] + list(e.get("aliases") or []) if x]]

    def latest(self, phase: str, label: str) -> dict | None:
        recs = [r for r in self.manifest.get("dice_log") or [] if r.get("phase") == phase and r.get("label") == label]
        return max(recs, key=lambda r: int(r.get("attempt") or 1)) if recs else None


def rule_stub_written(S: State, p: dict) -> bool:
    """The orphan-stub check, per stub: the row is filled."""
    row = S.canon.get(p["from"])
    return bool(row) and not is_stub(row)


def rule_clue_placed(S: State, p: dict) -> bool:
    """The validator's `clue_unplaced`, per clue: its place is a site, an NPC or an item of the registry."""
    clues = ((S.canon.get(p["from"]) or {}).get("dm_only") or {}).get("clues") or []
    where = next((c.get("placed_in") for c in clues if c.get("n") == p.get("clue")), None)
    return (S.canon.get(where) or {}).get("type") in ("site", "npc", "item")


def rule_god_registered(S: State, p: dict) -> bool:
    return bool(S.named("god", p.get("subject")))


def rule_event_dated(S: State, p: dict) -> bool:
    return any(e.get("day") is not None or e.get("year") is not None for e in S.named("event", p.get("subject")))


def rule_override_applied(S: State, p: dict) -> bool:
    """An override a roll applies itself (SCRIPT_APPLIED)."""
    default = p.get("default")
    if default == "pantheon_type":
        rec = S.latest("P2", "pantheon_type")
        return bool(rec) and rec.get("row_id") == p.get("to") and rec.get("notation") == "forced"
    if default == "second_language":
        langs = list((S.naming.get("languages") or {}))
        return S.naming.get("rolled") is True and langs[1:2] == ["other_side"]
    if default == "lineage_palette_weights":
        return bool(S.latest("P1", "people.lineage"))
    return False


def rule_arc_skeleton(S: State, p: dict) -> bool:
    """A P0 hook: the arc skeleton and the counts come from the scale's row (design_manifest derives them)."""
    m = S.manifest
    want = dm.arc_skeleton(m["dials"]["scale"], int(m["dials"]["level_band"][0]))
    shape = lambda rows: [(c.get("chapter"), c.get("act"), list(c.get("level_band") or [])) for c in rows or []]
    return shape(m.get("arc_skeleton")) == shape(want)


def sources(p: dict) -> list[dict]:
    """Every source of a promise: its first and the ones that joined it."""
    return [{k: p[k] for k in ("source", "from", "from_phase")}] + list(p.get("also") or [])


# P1 promises the rolls already apply: the identity record states the fact, so a script reads it (the audit of 12a)

def rule_rolls_by_scale(S: State, p: dict) -> bool:
    """The scale dial's P1 hook: the trope breaks and the questions the scale counts, and the signature mechanic
    rolled as the scale's chance says."""
    m = S.manifest
    sc = dt.scale_row(m["dials"]["scale"])
    ident = m.get("identity") or {}
    mechanic = (S.latest("P1", "mechanic") or {}).get("row_id")
    chance = int(sc["signature_mechanic_chance"])
    return (len(ident.get("trope_breaks") or []) == int(sc["trope_breaks"]) and len(ident.get("questions") or []) == int(sc["tensions"])
            and mechanic == ("no" if chance <= 0 else "yes" if chance >= 100 else mechanic) and mechanic in ("yes", "no"))


def rule_people_home(S: State, p: dict) -> bool:
    """The people signature's home is the lifeline; with the new-people scar rolled it is that scar."""
    m = S.manifest
    want = "scar_new_people" if "scar_new_people" in m["foundation"]["break"]["scars"] else "lifeline"
    return ((m.get("identity") or {}).get("people") or {}).get("home") == want


def rule_phenomenon_home(S: State, p: dict) -> bool:
    """The phenomenon signature's home is the ruin source's strangeness; with the scar that changed a rule of magic
    it is the break."""
    m = S.manifest
    want = "break" if "scar_magic_rule_changed" in m["foundation"]["break"]["scars"] else "ruin_source"
    return ((m.get("identity") or {}).get("phenomenon") or {}).get("home") == want


def rule_question_on_contest(S: State, p: dict) -> bool:
    """Every contest carries a question of its own, and the break's winner is one of the main contest's roles."""
    m = S.manifest
    f, ident = m["foundation"], m.get("identity") or {}
    asked = {q.get("contest") for q in ident.get("questions") or []}
    return all(c["id"] in asked for c in f["contests"]) and f["break"]["winner"] in f["contests"][0]["roles"]


def rule_scar_land_kind(S: State, p: dict) -> bool:
    """The new-land scar: a fantastic kind was drawn for it and stands in the palette."""
    rec = S.latest("P1", "foundation.palette.scar")
    f = S.manifest["foundation"]
    row = dt.row("foundation.yaml#palette", rec["row_id"]) if rec and rec.get("row_id") else None
    return bool(row) and bool(row.get("fantastic")) and rec["row_id"] in list(f["palette"]) + list(f["palette_extra"])


def rule_prohibition_drawn(S: State, p: dict) -> bool:
    """The new-prohibition scar: the first trope break is a prohibition row, tied to the break."""
    breaks = (S.manifest.get("identity") or {}).get("trope_breaks") or []
    row = dt.row("trope-breaks.yaml", breaks[0]["id"]) if breaks else None
    return bool(row) and bool(row.get("prohibition")) and breaks[0].get("tie") == "tie_break"


# one small table: a floor that binds a promise to a script adds its rule here (and names it on the hook: `check: <rule>`)
RULES = {"stub_written": rule_stub_written, "clue_placed": rule_clue_placed, "god_registered": rule_god_registered,
         "event_dated": rule_event_dated, "override_applied": rule_override_applied, "arc_skeleton": rule_arc_skeleton,
         "rolls_by_scale": rule_rolls_by_scale, "people_home": rule_people_home, "phenomenon_home": rule_phenomenon_home,
         "question_on_contest": rule_question_on_contest, "scar_land_kind": rule_scar_land_kind,
         "prohibition_drawn": rule_prohibition_drawn}


def rule_of(p: dict):
    check = str(p.get("check") or "")
    return RULES.get(check.split(":", 1)[1]) if check.startswith("script:") else None


def check_of(hook: dict, row: dict) -> str:
    """A hook's check: the script rule it names (`check: <rule>` on the hook, in the table), else the critic."""
    rule = hook.get("check")
    if not rule:
        return "critic"
    if rule not in RULES:
        raise SystemExit(f"design_promises: a hook of {row['id']} names the rule {rule!r}, which is not in RULES — a table fault")
    return f"script:{rule}"


# ── inspection: the script rules, the critic's verdicts, the gate, the owner's waiver (Part 12b) ─────────────

def due_by(p: dict, phase: str) -> bool:
    """Is the promise due at `phase` or before it? (`validator` and `play` never gate a phase)"""
    return p["due"] in dm.PHASES and phase in dm.PHASES and dm.PHASES.index(p["due"]) <= dm.PHASES.index(phase)


def gates(p: dict) -> bool:
    """Does a script promise close the gate when it is not kept? A stub of a type the orphan-stub gate only warns
    about (design_manifest.BLOCKING_STUB_TYPES) is listed and judged, and does not stop an approval."""
    return not p.get("minor")


def _attempt(manifest: dict, phase: str) -> int:
    return int((manifest["phases"].get(phase) or {}).get("attempt") or 1)


def run_rules(campaign: str, phase: str) -> dict:
    """`phase check`: every script promise due at or before the phase is decided now (a waived one stays waived).
    Returns the counts {kept, not_kept}; the verdicts are stored in the ledger the promise stands in."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return {}
    S = State(campaign)
    secret = load_secret(campaign)
    out = Counter()
    changed = False
    for p in m[KEY] + secret:
        rule = rule_of(p)
        if not rule or p["status"] == "waived" or not due_by(p, phase):
            continue
        status = "kept" if rule(S, p) else "not_kept"
        out[status] += 1
        if p["status"] != status or not p.get("verdict"):
            p.update({"status": status, "verdict": {"phase": phase, "attempt": _attempt(m, phase), "by": "script"}})
            changed = True
    if changed:
        save(campaign, m[KEY], secret, f"designer.py phase {phase} check (promises)")
    return {"kept": out["kept"], "not_kept": out["not_kept"]}


def script_failures(campaign: str, phase: str) -> tuple[list[str], list[str]]:
    """The gate's `promise`: the ids of the script promises due at or before the phase that are not kept as the
    stores stand now (read live, never from a stored verdict): (public ids, secret ids)."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return [], []
    S = State(campaign)
    bad = lambda promises: [p["id"] for p in promises if rule_of(p) and gates(p) and p["status"] != "waived"
                            and due_by(p, phase) and not rule_of(p)(S, p)]
    return bad(m[KEY]), bad(load_secret(campaign))


def unjudged(campaign: str, phase: str) -> tuple[list[str], list[str]]:
    """The gate's `promise_unjudged`: the critic-judged promises due at this phase that carry no verdict."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return [], []
    left = lambda promises: [p["id"] for p in promises if p["check"] == "critic" and p["due"] == phase and p["status"] == "open"]
    return left(m[KEY]), left(load_secret(campaign))


def judge(campaign: str, phase: str, entries: list[dict], by: str = "critic") -> tuple[int, int]:
    """Store a critic's verdicts: `{id, verdict: kept | not_kept}` for the critic-judged promises due at this phase.
    A secret promise's verdict goes to the secret ledger. Returns (stored, ignored): an id that is unknown, not the
    critic's to judge, not due at this phase or waived is ignored."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return 0, len(entries)
    secret = load_secret(campaign)
    index = {p["id"]: p for p in m[KEY] + secret}
    stored = 0
    for e in entries:
        p = index.get(e.get("id"))
        if p is None or p["check"] != "critic" or p["due"] != phase or p["status"] == "waived" or e.get("verdict") not in ("kept", "not_kept"):
            continue
        p.update({"status": e["verdict"], "verdict": {"phase": phase, "attempt": _attempt(m, phase), "by": by}})
        stored += 1
    if stored:
        save(campaign, m[KEY], secret, f"design_approval.py critique --phase {phase} (promise verdicts)")
    return stored, len(entries) - stored


def waive(campaign: str, promise_id: str, sentence: str) -> dict:
    """The owner accepts a not-kept promise as it stands: recorded with the sentence in the ledger and the revision
    log. The log names the promise by its id alone: a secret promise's text and source never reach a public record."""
    from design_io import now_iso
    m = dm.load(campaign)
    if not has_ledger(m):
        raise SystemExit("design_promises: this birth has no ledger (a legacy birth)")
    secret = load_secret(campaign)
    p = next((x for x in m[KEY] + secret if x["id"] == promise_id), None)
    if p is None:
        raise SystemExit(f"design_promises: no promise {promise_id}")
    if p["status"] != "not_kept":
        raise SystemExit(f"design_promises: {promise_id} is {p['status']}; only a promise judged not kept is waived")
    if not str(sentence or "").strip():
        raise SystemExit("design_promises: a waiver needs the owner's one sentence")
    p.update({"status": "waived", "waiver": {"sentence": sentence.strip(), "at": now_iso()}})
    entry = {"at": now_iso(), "scope": "promise", "phase": p["due"] if p["due"] in dm.PHASES else None,
             "reason": sentence.strip(), "affected": 0, "commit": None, "promise": promise_id}
    m.setdefault("revision_log", []).append(entry)
    entry["id"] = f"rev_{len(m['revision_log']):04d}"
    save(campaign, m[KEY], secret, "designer.py promise waive", manifest=m)
    dm.save(campaign, m, "designer.py promise waive")
    return p


# ── the counts and the lists (the card, the report, the prompts) ─────────────────────────────────────────────

def counts(public: list[dict], secret: list[dict], phase: str | None = None) -> dict:
    """The ledger in numbers: the public promises due at `phase` by status, the open ones by due phase, the secret
    ones as three counts (the owner's ruling 2: never a secret promise's text; a waived one leaves the three)."""
    by_status = Counter(p["status"] for p in public if p["due"] == phase)
    open_by = Counter(p["due"] for p in public if p["status"] == "open")
    sec = Counter(p["status"] for p in secret)
    return {"due": {"total": sum(by_status.values()), **{s: by_status.get(s, 0) for s in STATUSES}},
            "open_by_due": {d: open_by[d] for d in DUE_ORDER if open_by.get(d)},
            "secret": {"open": sec.get("open", 0), "kept": sec.get("kept", 0), "not_kept": sec.get("not_kept", 0)}}


def line_of(p: dict) -> str:
    """A promise in one line: the source row's name, the due phase, the sentence."""
    how = "" if p["check"] == "critic" else " (checked by script)"
    return f"{p['name']} (due {p['due']}){how}: {p['text']}"


def card_lines(campaign: str, phase: str) -> list[str]:
    """The card's block. Before its due phase a promise is open work, never an error. A public promise judged not
    kept is listed by its row's name, due phase and sentence; a secret one only adds to the secret count."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return []
    c = counts(m[KEY], load_secret(campaign), phase)
    d = c["due"]
    lines = [f"- **Promises due at this phase:** {d['total']} (kept {d['kept']}, not kept {d['not_kept']}, waived {d['waived']}, open {d['open']})",
             "- **Open promises by due phase:** " + (" · ".join(f"{k} {v}" for k, v in c["open_by_due"].items()) or "—")
             + " — open work until each phase's turn, not errors",
             f"- **Secret promises:** {c['secret']['open']} open, {c['secret']['kept']} kept, {c['secret']['not_kept']} not kept"]
    broken = [p for p in m[KEY] if p["status"] == "not_kept"]
    if broken:
        lines.append(f"- ⚠ **Promises judged not kept:** {len(broken)} — the owner decides: accept one as it stands "
                     "(`designer.py promise waive <id> \"<one sentence>\"`), or rerun the phase")
        lines += [f"  - `{p['id']}` · {line_of(p)}" for p in sorted(broken, key=lambda p: (DUE_ORDER.index(p["due"]), p["id"]))]
    return lines


def report_line(campaign: str, phase: str) -> str | None:
    """`phase PN report`: counts and ids only (the conductor pastes it as printed)."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return None
    c = counts(m[KEY], load_secret(campaign), phase)
    d, s = c["due"], c["secret"]
    broken = [p["id"] for p in m[KEY] if p["status"] == "not_kept"]
    return (f"- promises: due here {d['total']} (kept {d['kept']}, not kept {d['not_kept']}, waived {d['waived']}, open {d['open']})"
            f" · judged not kept {len(broken)}{' [' + ', '.join(broken[:12]) + ']' if broken else ''}"
            f" · secret {s['open']} open, {s['kept']} kept, {s['not_kept']} not kept")


def list_command(campaign: str, phase: str) -> str:
    return f"py {Path(__file__).resolve().as_posix()} -c {campaign} list --phase {phase} --secret"


def prompt_block(campaign: str, phase: str, audience: str, secret_reader: bool) -> str:
    """The prompts' block "Promises due at this phase" (section 6): the public promises due now, by id, source row's
    name and sentence. The writer (`audience: writer`) gets every one; the phase critic (`critic`) the ones it judges,
    with the entry its return owes. No secret promise is printed: an agent that already reads dm-only material is
    given the command that lists them."""
    m = dm.load(campaign)
    if not has_ledger(m) or phase not in dm.PHASES:
        return ""
    due = [p for p in m[KEY] if p["due"] == phase and p["status"] != "waived"]
    if audience == "critic":
        due = [p for p in due if p["check"] == "critic"]
        head = ("**Promises due at this phase — your verdicts.** The rows this campaign rolled promised what follows, and "
                "each is due now. For every promise return one entry in `promises[]`: `{id, verdict: kept | not_kept, note}` "
                "(`note` is a short slug, never quoted text; your reasoning goes to the critique file). Judge what the "
                "phase's files and rows hold, not what they intend. A promise without your verdict closes the approval gate.")
    else:
        head = ("**Promises due at this phase.** The rows this campaign rolled promised what follows, and each is due now: "
                "what you write keeps every one of them. The phase critic returns a verdict per promise; one a script "
                "checks closes the approval gate when it is not kept.")
    lines = [head] + [f"- `{p['id']}` — {p['name']}: {p['text']}" + ("" if p["check"] == "critic" else " *(checked by script)*")
                      for p in sorted(due, key=lambda p: p["id"])]
    if not due:
        lines.append("- (no public promise is due at this phase)")
    if secret_reader:
        tail = (" Return a verdict for each of their ids too; what you reason about them goes to "
                f"`design/dm-only/_staging/{phase}/`, never to a public file." if audience == "critic" else
                " Keep them as you keep the others.")
        lines.append(f"The secret promises due at this phase are not printed here. Run `{list_command(campaign, phase)}` and "
                     "read them from its output; their sentences never leave dm-only and never enter your return." + tail)
    return "\n".join(lines)


def listing(campaign: str, phase: str | None, status: str | None, secret: bool) -> list[str]:
    """`promise list`: one ledger's promises, a line each: id, status, check, then the name, the due phase and the sentence."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return []
    rows = load_secret(campaign) if secret else m[KEY]
    rows = [p for p in rows if (not phase or p["due"] == phase) and (not status or p["status"] == status)]
    return [f"{p['id']}  {p['status']:<8}  {'critic' if p['check'] == 'critic' else 'script':<6}  {line_of(p)}"
            + (f"  [waived: {p['waiver']['sentence']}]" if p.get("waiver") else "")
            for p in sorted(rows, key=lambda p: (DUE_ORDER.index(p["due"]), p["id"]))]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the promise ledger (plan item 25, errata 24.2 #23)")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    c = sub.add_parser("counts")
    c.add_argument("--phase")
    ls = sub.add_parser("list", help="the public ledger; with --secret the secret one (dm-only: an agent that reads dm-only, the development tab)")
    ls.add_argument("--phase")
    ls.add_argument("--status", choices=STATUSES)
    ls.add_argument("--secret", action="store_true")
    a = ap.parse_args(argv)
    m = dm.load(a.campaign)
    if not has_ledger(m):
        print("design_promises: this birth has no ledger (a legacy birth is left as it was built)")
        return 0
    if a.verb == "list":
        for line in listing(a.campaign, a.phase, a.status, a.secret):
            print(line)
        return 0
    out = counts(m[KEY], load_secret(a.campaign), a.phase)
    if a.phase:
        d = out["due"]
        print(f"design_promises: due at {a.phase} — {d['total']} (kept {d['kept']}, not kept {d['not_kept']}, waived {d['waived']}, open {d['open']})")
    print("design_promises: open by due phase — " + (", ".join(f"{k} {v}" for k, v in out["open_by_due"].items()) or "none"))
    s = out["secret"]
    print(f"design_promises: secret — {s['open']} open, {s['kept']} kept, {s['not_kept']} not kept")
    return 0


if __name__ == "__main__":
    sys.exit(main())
