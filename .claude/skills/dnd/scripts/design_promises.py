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
  source      hook | override | foundation | stub | placement | concretise | clue_stage
  from        the row id, the entity id or the foundation piece; `from_phase` the phase that made it
  also        further sources of the same promise (two promises with one due phase and one text are one promise)
  due         a phase (P0-P9), `validator` (the full validator run) or `play` (recorded, never gates a birth)
  text        the hook's `must` sentence or the generated sentence, in English as the tables hold it
  name        the source row's label, for the card (the tables carry no Turkish since build item 13a)
  check       `script:<rule>` where a script can decide today (RULES), else `critic`
  status      open | kept | not_kept | waived; `verdict` {phase, attempt, by} once judged; `waiver` the owner's sentence

The sources today are the rows rolled in P0 and P1 (SOURCE_PHASES). A later floor plugs in at two places, each one
line: its phase joins SOURCE_PHASES once its tables' hooks are reviewed (docs/p1-tags.md, rule 9), and a promise a
script can decide gets its rule in RULES. An override is not applied here: it is a promise due at the phase that owns
the default (claims.yaml#defaults); the ones a roll already applies are kept by script.

A legacy birth (no `promises` in design.json) has no ledger and is left as it was built.

  design_promises.py -c CAMP counts [--phase PN]     the ledger's counts (public by due phase and status; secret: three counts)
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
SOURCES = ("hook", "override", "foundation", "stub", "placement", "concretise", "clue_stage")
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
            due = due_of(h["phase"])
            add("hook", row["id"], phase, due, str(h["must"]), row.get("label") or row["id"],
                "script:arc_skeleton" if due == "P0" else "critic", hidden)

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

    # 6. the secret's three clue stages (secret): the archetype's clue shape and the trail row, each with its levels
    if identity_secret:
        arch = dt.row("secrets.yaml#archetype", identity_secret["secret"]["archetype"])
        trail = dt.row("secrets.yaml#trail", identity_secret["secret"]["trail"])
        for n, (lo, hi) in enumerate(clue_levels(band, steps[-1]), 1):
            add("clue_stage", arch["id"], "P1", "P6",
                f"clue {n} of the secret ({arch['clue_shape'][f'act{n}']}; the trail carries it as: {trail['acts'][f'act{n}']}) "
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
            L.add("stub", eid, made, row["owner_phase"], f"{eid} is written: its row filled and its file on disk",
                  f"a reserved {row.get('type')}" if hidden else str(row.get("name") or eid), "script:stub_written", secret=hidden)
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


# one small table: a floor that binds a promise to a script adds its rule here
RULES = {"stub_written": rule_stub_written, "clue_placed": rule_clue_placed, "god_registered": rule_god_registered,
         "event_dated": rule_event_dated, "override_applied": rule_override_applied, "arc_skeleton": rule_arc_skeleton}


def rule_of(p: dict):
    check = str(p.get("check") or "")
    return RULES.get(check.split(":", 1)[1]) if check.startswith("script:") else None


# ── the counts (the card, the summary) ───────────────────────────────────────────────────────────────────────

def counts(public: list[dict], secret: list[dict], phase: str | None = None) -> dict:
    """The ledger in numbers: the public promises due at `phase` by status, the open ones by due phase, the secret
    ones as three counts (the owner's ruling 2: never a secret promise's text)."""
    by_status = Counter(p["status"] for p in public if p["due"] == phase)
    open_by = Counter(p["due"] for p in public if p["status"] == "open")
    sec = Counter(p["status"] for p in secret)
    return {"due": {"total": sum(by_status.values()), **{s: by_status.get(s, 0) for s in STATUSES}},
            "open_by_due": {d: open_by[d] for d in DUE_ORDER if open_by.get(d)},
            "secret": {"open": sec.get("open", 0), "kept": sec.get("kept", 0), "not_kept": sec.get("not_kept", 0)}}


def card_lines(campaign: str, phase: str) -> list[str]:
    """The card's one block. Before its due phase a promise is open work, never an error."""
    m = dm.load(campaign)
    if not has_ledger(m):
        return []
    c = counts(m[KEY], load_secret(campaign), phase)
    d = c["due"]
    return [f"- **Promises due at this phase:** {d['total']} (kept {d['kept']}, not kept {d['not_kept']}, waived {d['waived']}, open {d['open']})",
            "- **Open promises by due phase:** " + (" · ".join(f"{k} {v}" for k, v in c["open_by_due"].items()) or "—")
            + " — open work until each phase's turn, not errors",
            f"- **Secret promises:** {c['secret']['open']} open, {c['secret']['kept']} kept, {c['secret']['not_kept']} not kept"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the promise ledger (plan item 25, errata 24.2 #23)")
    ap.add_argument("-c", "--campaign", required=True)
    sub = ap.add_subparsers(dest="verb", required=True)
    c = sub.add_parser("counts")
    c.add_argument("--phase")
    a = ap.parse_args(argv)
    m = dm.load(a.campaign)
    if not has_ledger(m):
        print("design_promises: this birth has no ledger (a legacy birth is left as it was built)")
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
