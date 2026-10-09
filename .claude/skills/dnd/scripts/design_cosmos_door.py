#!/usr/bin/env python3
"""
design_cosmos_door.py — P2's frame, seal and door (plan item 25, build item 22c; docs/p2-build-22.md part 22c,
docs/p2-tags.md S7 #3). P1's are design_frame.py and design_door.py; this module is their P2 counterpart.

**The frame.** Everything in P2's registry rows that is not prose is decided by the cosmos's rolls (design_cosmos.py,
`design.json#cosmos`), so the script writes it: at `phase P2 begin` the frame of every row the writer owes goes to
`design/_staging/P2/doc_cosmology.frame.json`: each `god_`, `plane_`, `era_` and `event_` row with its rolled fields and
an object `stamped`, its prose fields empty and named under `fill`, and the container's own parts (the calendar seed
`calendar.py init` takes, the calendar's festivals, moon, start and dated days). Every name is set: the pool gives the gods theirs (22b) and the
planes, the festivals, the moon, the ages and the events theirs (build item 22n). The threat's own home plane (option d
of 22b) is a secret row of the frame, named from the secret stock.

**The seal.** P2's preroll stamps `design.json#p2_seal`: the hashes of the public cosmos and its dm-only half. The door
refuses a merge when either changed.

**The door** (`registry.py merge --phase P2` and `check` ask it about every unit of a birth whose P2 the script rolled):
  frame   every framed row present, its frame fields unchanged (a changed or missing field refused by its name), no
          god, plane, era or event row beside them; the calendar seed and block as framed; every framed row, festival
          and moon named from the pool (build item 22n)
  S7 #3   the god count and the domain coverage; at least one evil god at standard and epic; a festival per greater
          god; the four seated story events; every plane P1 names touched; twelve months of 28 days and a seven-day
          week; a secret seat's id or fact in no public file (the threat's own home plane, a hidden god name, a
          secretly rolled row's id)
A refusal names what is wrong; what the conductor may not read goes to the dm-only door log.

    py design_cosmos_door.py -c CAMPAIGN show        print the frame (it holds dm-only fields: a developer's command)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import design_dir, dm_only_dir, now_iso, read_json, stamp_meta, write_json_atomic  # noqa: E402

UNIT = "doc_cosmology"
FRAME_SUFFIX = ".frame.json"
PROSE = "design/cosmology.md"
DM_PROSE = "design/dm-only/cosmology.md"
SEAL = "p2_seal"
EMPTY = ""
P2_TYPES = ("god", "plane", "era", "event")
DAYS_A_YEAR = 336
SEATED = ("move", "origin", "founding", "ruin")
EVIL = ("NE", "CE", "LE")
# build item 22n: the planes, the ages and the events take their names from the pool's cosmos section (the roller
# reserves each under its frame id), so `name` is a frame field like any rolled one, never the writer's to fill


def frame_rel() -> str:
    return f"design/_staging/P2/{UNIT}{FRAME_SUFFIX}"


def applies(manifest: dict) -> bool:
    """A birth whose P2 the script rolled (build item 22b) on a P1 the script rolled: a cosmos, a ledger and both seals.
    A legacy birth has none."""
    import design_door as door
    return (isinstance(manifest.get("cosmos"), dict) and manifest["cosmos"].get("stamped") is True
            and all(isinstance(manifest.get(k), (dict, list)) for k in ("foundation", "identity", "promises", door.SEAL, SEAL)))


# ── the seal ─────────────────────────────────────────────────────────────────────────────────────────────────

def _hash(node) -> str:
    return hashlib.sha256(json.dumps(node, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]


def seal_of(campaign: str, manifest: dict | None = None) -> dict:
    m = manifest or dm.load(campaign)
    secret = (read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("cosmos")
    return {"cosmos": _hash(m.get("cosmos")), "cosmos_secret": _hash(secret)}


def seal(campaign: str) -> dict:
    m = dm.load(campaign)
    m[SEAL] = seal_of(campaign, m)
    dm.save(campaign, m, "design_cosmos_door.py seal")
    return m[SEAL]


def seal_errors(campaign: str, manifest: dict) -> list[str]:
    now, was = seal_of(campaign, manifest), manifest.get(SEAL) or {}
    names = {"cosmos": "design.json#cosmos", "cosmos_secret": "the cosmos's dm-only half"}
    return [f"{names[k]} differs from what the preroll stamped; the rolls are the writer's ground, never its choice "
            "(restore it: rerun the preroll, or undo the edit)" for k in names if now[k] != was.get(k)]


# ── the frame ────────────────────────────────────────────────────────────────────────────────────────────────

def _row(eid, etype: str, name, lang, secrecy: str = "public", file: str = PROSE, **fields) -> dict:
    return {"id": eid, "type": etype, "name": name, "aliases": [], "summary": EMPTY, "file": file, "secrecy": secrecy,
            "created_phase": "P2", "origin": "birth", "lang": lang, **fields, "refs": []}


def plane_id(baseline: str) -> str:
    return "plane_" + (baseline.removeprefix("baseline_") if baseline != "moon" else "moon")


HOME_ID = "plane_s01"           # the 22c audit: a secret row's id never names its content (registry.py, as npc_s01)


def _rate(row_id: str) -> dict:
    r = dt.row("planes.yaml#time_rate", row_id) or {}
    return {"row": row_id, "rate": r.get("rate"), "rate_range": r.get("rate_range")}


def _plane(pl: dict, gods: dict, lang, secrecy: str = "public", file: str = PROSE, eid: str | None = None) -> dict:
    keeper = pl.get("keeper") or {}
    keeper = {"god": gods.get(keeper["god"])} if "god" in keeper else ({"creature": keeper["creature"]} if keeper else None)
    return _row(eid or plane_id(pl["baseline"]), "plane", pl.get("name") or EMPTY, lang, secrecy, file, baseline=pl["baseline"], touched=True,
                named_by=list(pl.get("named_by") or []), deviation=pl["deviation"], time_rate=_rate(pl["rate"]),
                way_in=pl["way"], cost=pl["cost"], keeper=keeper, entry_site=None,
                stamped={"baseline": pl["baseline"], "touched": True})


def build(campaign: str, manifest: dict | None = None) -> dict | None:
    """The frame of a birth whose P2 the script rolled; None for a legacy birth."""
    m = manifest or dm.load(campaign)
    if not applies(m):
        return None
    cos = m["cosmos"]
    secret = (read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("cosmos") or {}
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    langs = naming.get("languages") or {}
    common = next((lid for lid in ("common", "other_side", "people") if lid in langs), EMPTY)
    domains = {r["id"]: r["label"] for r in dt.rows("pantheon.yaml#domain_scaffold")}
    gid = {g["n"]: g["id"] for g in cos["gods"]}
    hidden = {int(k): v for k, v in (secret.get("hidden_names") or {}).items()}
    rows: dict = {}

    def put(row: dict, fill: list[str]) -> None:
        rows[row["id"]] = {"registry": row, "fill": fill}

    # the gods
    for g in cos["gods"]:
        rels = [{"to": gid[r["b"] if r["a"] == g["n"] else r["a"]], "kind": r["relation"]}
                for r in cos["relations"] if g["n"] in (r["a"], r["b"])]
        church = dict(g.get("church") or {})
        doms = [domains[d] for d in g["domains"]]
        extra = {"dm_only": {"true_name": hidden[g["n"]]}} if g["n"] in hidden else {}
        story = cos.get("god_story") or {}
        extra["story"] = story.get("row") if story.get("god") == g["n"] else None        # the one discoverable god story
        extra["pilgrim_road"] = cos.get("pilgrim_god") == g["n"]                         # the lifeline's god
        put(_row(g["id"], "god", g["name"] or g["epithet"], g.get("lang") or common, rank=g["rank"], great=g["great"], domains=doms,
                 alignment=g["alignment"], epithet=g["epithet"], church=church, relations=rels, fallen=bool(g.get("fallen")),
                 symbol=EMPTY, disposition=EMPTY, as_worshipped=EMPTY, stamped={"rank": g["rank"], "domains": doms}, **extra),
            ["aliases", "summary", "symbol", "disposition", "as_worshipped", "refs"])
    # the touched planes; the threat's own home plane is secret
    for pl in cos["planes"]:
        put(_plane(pl, gid, common), ["aliases", "summary", "refs"])
    home = secret.get("home_plane") or {}
    secret_rows: dict = {}
    if home.get("own"):
        row = _plane(dict(home["own"], baseline=home["baseline"], named_by=[]), gid, common, "secret", DM_PROSE, HOME_ID)
        row["dm_only"] = {"home_of_the_threat": True}
        secret_rows[row["id"]] = {"registry": row, "fill": ["aliases", "summary", "refs"]}
    # the ages and the events
    for a in cos["ages"]:
        put(_row(f"era_{a['n']}", "era", a.get("name") or EMPTY, common, order=a["n"], row=a["row"], ruin=bool(a["ruin"]), span=EMPTY,
                 stamped={"order": a["n"]}), ["aliases", "summary", "span", "refs"])
    start_year = cos["calendar"]["start_year"]
    st0 = cos["calendar"]["start"]
    for e in cos["events"]:
        ago = e.get("years_ago")
        year = None if ago is None else start_year - int(ago)
        day = None if ago is None else -int(ago) * DAYS_A_YEAR
        if e.get("seat") == "move":         # the move's own day: its last step before the start, or its next step after
            year = start_year if year is None else year
            day = int(st0.get("days_to_next_step") or 0) if ago is None else -int(st0.get("after_move_days") or 0) - int(ago) * DAYS_A_YEAR
        dm_only = {"happened": EMPTY}
        if e.get("seat") == "origin":
            dm_only["origin"] = (secret.get("origin") or {}).get("row")
        row = _row(f"event_{e['n']}", "event", e.get("name") or EMPTY, common, seat=e.get("seat"), event_type=e.get("type"),
                   divergence=e.get("divergence"), memory=e.get("memory"), years_ago=ago, year=year,
                   day=day, witness_list=bool(e.get("witnesses")), era=EMPTY,
                   taught=EMPTY, witnesses=[], stamped={"year": year}, dm_only=dm_only)
        if e.get("seat") == "move":
            row["aliases"] = ["the move"]          # the premise's pin names the move (design_promises: event_dated)
        if e.get("taught_type"):
            row["taught_type"] = e["taught_type"]          # build item 22n: the type the folk remember it by
        fill = ["summary", "era", "taught", "refs"] + (["aliases"] if e.get("seat") != "move" else [])
        if e.get("seat") == "origin" or e.get("divergence") not in (None, "div_none"):
            fill.append("dm_only.happened")
        put(row, fill)
    for e in cos["deep_events"]:
        put(_row(f"event_deep_{e['n']}", "event", e.get("name") or EMPTY, common, seat=None, event_type=e["type"], divergence=e["divergence"],
                 memory=e["memory"], years_ago=None, year=None, day=None, deep=True, witness_list=False, era=EMPTY,
                 taught=EMPTY, witnesses=[], stamped={}, dm_only={"happened": EMPTY}),
            ["aliases", "summary", "era", "taught", "refs"] + (["dm_only.happened"] if e["divergence"] != "div_none" else []))
    # the calendar: the seed calendar.py takes and the container's block
    cal = cos["calendar"]
    months, days = cal.get("month_names") or [], cal.get("day_names") or []
    st = cal["start"]
    date = f"{st['day']} {months[st['month'] - 1]} {st['year']}" if months else EMPTY
    seed = {"store": "calendar", "op": "init", "args": {"date": date, "months": list(months), "month_length": cal["month_length"],
                                                         "day_names": list(days)}}
    block = {"climate": cal["climate"], "moon": {"row": cal["moon"], "names": list(cal.get("moon_names") or [])},
             "underground_count": cal.get("underground_count"),
             "festivals": [{"n": f["n"], "row": f["row"], "god": gid.get(f["god"]) if f["god"] is not None else None,
                            "month": f["month"], "day": f["day"], "name": f.get("name") or EMPTY} for f in cal["festivals"]],
             "start": dict(st), "start_anchor": cal["start_anchor"], "dated": dict(cal.get("dated") or {}),
             "span": list(cal["span"]), "seasons": EMPTY}
    return {"_meta": {"schema_version": 1, "campaign": campaign, "written_by": "design_cosmos_door.py", "written_at": now_iso(),
                      "what": "P2's registry rows as the rolls set them (build item 22c)"},
            "how": ("Every row's `registry` goes under the container's `rows[]` (fragment below), its `fill` fields filled and "
                    "every other field copied unchanged: the door refuses a changed or missing frame field. `stamped` stays "
                    "an object. The container carries `seeds` and `calendar` exactly as framed, `calendar.seasons` filled "
                    "(one felt line per month). A secret row goes under `rows[]` with its `secrecy` as framed, and the dm-only prose's front "
                    "matter `covers` it."),
            "container": {"fragment": f"design/_staging/P2/{UNIT}.json", "id": UNIT, "prose": PROSE, "dm_only_prose": DM_PROSE,
                          "seeds": [seed], "calendar": block, "fill": ["calendar.seasons"]},
            "rows": rows, "secret_rows": secret_rows}


def write(campaign: str) -> Path | None:
    """`phase P2 begin`: write the frame beside the container's fragment path."""
    frame = build(campaign)
    if frame is None:
        return None
    path = design_dir(campaign).parent / frame_rel()
    write_json_atomic(path, frame)
    return path


def framed_rows(frame: dict) -> dict:
    return {**frame["rows"], **frame["secret_rows"]}


def frame_errors(frame: dict, eid: str, row: dict) -> list[str]:
    """A P2 row against its frame: the fields named, never their values."""
    import design_frame as dfr
    entry = framed_rows(frame).get(eid)
    if entry is None:
        if row.get("type") in P2_TYPES:
            return [f"{eid}: no such {row['type']} in the script's frame ({frame_rel()}); P2 writes the framed rows and no other"]
        return []
    say = {"missing": "is missing; the script's frame sets it", "changed": "differs from the script's frame; the rolls set it",
           "shape": "must be an object, as the script's frame has it"}
    errs = [f"{eid}: `{p}` {say[kind]} (copy it unchanged from {frame_rel()})"
            for kind, p in dfr._diff(entry["registry"], row, set(entry["fill"]))]
    stamped = row.get("stamped")
    if isinstance(stamped, dict):
        for key in entry["registry"]["stamped"]:
            if key in stamped and key in row and stamped[key] != row[key]:
                errs.append(f"{eid}: `stamped.{key}` must equal the row's own `{key}`")
    return errs


def container_errors(frame: dict, uid: str, frag: dict) -> list[str]:
    import design_frame as dfr
    c = frame["container"]
    errs = []
    if frag.get("seeds") != c["seeds"]:
        errs.append(f"{uid}: `seeds` must be the calendar seed of the frame, unchanged (copy it from {frame_rel()})")
    got = frag.get("calendar")
    if not isinstance(got, dict):
        errs.append(f"{uid}: `calendar` is missing; the frame's calendar block goes into the container")
    else:
        fill = {f.removeprefix("calendar.") for f in c["fill"]}
        errs += [f"{uid}: `calendar.{p}` differs from the script's frame or is missing (copy it unchanged from {frame_rel()})"
                 for _, p in dfr._diff(c["calendar"], got, fill)]
        if not str(got.get("seasons") or "").strip():
            errs.append(f"{uid}: `calendar.seasons` is empty; write one felt line per month from the climate's seasons")
    return errs


# ── the door's checks of the whole set (S7 #3) ──────────────────────────────────────────────────────────────

def name_errors(frame: dict | None) -> list[str]:
    """Build item 22n: every name P2 makes comes from the pool, so a framed row, a festival or a moon the preroll left
    nameless (a stock that ran dry, a P2 prerolled before 22n) is the preroll's fault: rerun it."""
    if frame is None:
        return []
    errs = [f"{eid}: the pool gave it no name; rerun the P2 preroll (every name P2 makes comes from the pool)"
            for eid, entry in sorted(frame["rows"].items()) if not str(entry["registry"].get("name") or "").strip()]
    if any(not str(entry["registry"].get("name") or "").strip() for entry in frame["secret_rows"].values()):
        errs.append("a secret row of the frame has no name; rerun the P2 preroll")
    block = frame["container"]["calendar"]
    errs += [f"festival {f['n']}: the pool gave it no name; rerun the P2 preroll" for f in block["festivals"] if not f.get("name")]
    want = {"moon_none_stars": 0, "moon_two": 2}.get(block["moon"]["row"], 1)
    if len(block["moon"].get("names") or []) != want:
        errs.append(f"the moon ({block['moon']['row']}) carries {len(block['moon'].get('names') or [])} name(s) of {want}; "
                    "rerun the P2 preroll")
    return errs


def set_errors(cos: dict, rows: dict, scale: str) -> tuple[list[str], set]:
    """The cosmos's script checks over the merged set (the canonical rows and this merge's): the faults, and the
    greater gods' ids (each owes a festival)."""
    import design_cosmos as dc
    errs = []
    gods = [r for r in rows.values() if r.get("type") == "god" and r.get("created_phase") == "P2"]
    if len(gods) != cos["counts"]["gods"]:
        errs.append(f"the cosmos rolled {cos['counts']['gods']} gods and the set holds {len(gods)}")
    labels = {r["id"]: r["label"] for r in dt.rows("pantheon.yaml#domain_scaffold")}
    target, named = dc.coverage(scale)
    have = {d for g in gods for d in g.get("domains") or []}
    want = {labels[d] for d in named}
    if len(have) < target or not want <= have:
        errs.append(f"the gods cover {len(have)} domain(s); the {scale} scale needs {target}" + (" with Life" if want else ""))
    if scale in ("standard", "epic") and not any(g.get("alignment") in EVIL for g in gods):
        errs.append("no god is evil (NE, CE or LE); at standard and epic at least one is")
    greater = {g["id"] for g in gods if g.get("rank") == "greater"}
    return errs, greater


class CosmosDoor:
    """One P2 merge's door. `whole` are the faults of the whole phase (the seal); `unit_errors` a unit's own."""

    def __init__(self, campaign: str, canonical: dict, incoming: list[tuple[str, dict]]):
        import design_door as door
        self.campaign = campaign
        self.root = design_dir(campaign).parent
        self.m = dm.load(campaign)
        self.cos = self.m["cosmos"]
        self.scale = self.m["dials"]["scale"]
        self.rows = dict(canonical.get("entities") or {})
        self.rows.update(dict(incoming))
        self.frame = build(campaign, self.m)
        self.hidden: list[dict] = []
        log = read_json(dm_only_dir(campaign) / "dice-log.json") or {}
        secret = log.get("cosmos") or {}
        self.p1_attempt = attempt = int((self.m["phases"].get("P1") or {}).get("attempt") or 1)
        p1_secret = [r for r in log.get("rolls") or [] if r.get("phase") == "P1" and int(r.get("attempt") or 1) == attempt
                     and r.get("row_id") and ".yaml" in str(r.get("table"))]
        self.secret_ids = sorted({r["row_id"] for r in p1_secret})
        # the fact half (as P1's door): a secret row's own sentence
        self.secret_sentences = sorted({row[k].lower() for r in p1_secret for row in [dt.row(r["table"], r["row_id"]) or {}]
                                        for k in ("statement", "rule", "cause") if isinstance(row.get(k), str) and len(row[k]) >= 24})
        home = secret.get("home_plane") or {}
        # P2's own secret words: the mirror relation; the threat's own home plane (its id and its baseline row; a linked
        # home is a public plane and says nothing by itself)
        self.secret_words = ["rel_mirror"] + ([home["baseline"], HOME_ID] if home.get("own") else [])
        self.secret_names = sorted(set(str(v) for v in (secret.get("hidden_names") or {}).values()) | door.Names(campaign).secret_all())
        self.whole = seal_errors(campaign, self.m) + name_errors(self.frame)

    def leak_errors(self, where: str, text: str) -> list[str]:
        """A secret seat's id or fact in a public text: the threat's own home plane's id, a hidden god's name, a secret
        stock name, a secretly rolled row's id. The line names the kind, never the word."""
        low = text.lower()
        kinds = []
        if any(re.search(r"(?<![a-z0-9_])" + re.escape(x) + r"(?![a-z0-9_])", low) for x in self.secret_ids):
            kinds.append("a secretly rolled row's id")
        if any(re.search(r"(?<![a-z0-9_])" + re.escape(x) + r"(?![a-z0-9_])", low) for x in self.secret_words):
            kinds.append("an id of the cosmos's secret layer")
        if any(s in low for s in self.secret_sentences):
            kinds.append("a sentence of a secretly rolled row")
        if any(re.search(r"(?<![\w'])" + re.escape(n) + r"(?![\w])", text) for n in self.secret_names):
            kinds.append("a secret name")
        return [f"{where}: carries {k}; a secret seat's id or fact stays in dm-only" for k in kinds]

    def unit_errors(self, uid: str, frag: dict, rows: list[tuple[str, dict]]) -> tuple[list[str], list[str]]:
        import design_door as door
        errs = list(self.whole)
        mine = dict(rows)
        framed = framed_rows(self.frame)
        if frag and (frag.get("calendar") is not None or frag.get("seeds") or any(eid in framed for eid in mine)):
            errs += container_errors(self.frame, uid, frag)
            for eid in framed_rows(self.frame):
                if eid not in mine:
                    errs.append(f"{uid}: the framed row {eid} is missing; every row of the frame goes under `rows[]`")
            s_errs, greater = set_errors(self.cos, {**self.rows, **mine}, self.scale)
            errs += [f"{uid}: {e}" for e in s_errs]
            fests = (frag.get("calendar") or {}).get("festivals") or []
            for g in sorted(greater):
                if not any(f.get("god") == g for f in fests):
                    errs.append(f"{uid}: the greater god {g} has no festival; every greater god has one")
            seats = [r.get("seat") for r in mine.values() if r.get("type") == "event" and r.get("seat")]
            if sorted(seats) != sorted(SEATED):
                errs.append(f"{uid}: the four seated story events (the move, the villain's origin, the institution's founding, "
                            f"the ruin's fall) stand once each; the set holds {', '.join(sorted(seats)) or 'none'}")
            named = dt.load("planes.yaml")["rules"]["named_planes"]
            touched = {x for r in mine.values() if r.get("type") == "plane" and r.get("secrecy") != "secret" for x in r.get("named_by") or []}
            ctx_rows = {r.get("row_id") for r in self.m.get("dice_log") or []
                        if r.get("phase") == "P1" and int(r.get("attempt") or 1) == self.p1_attempt}
            for rid in named:
                if rid in ctx_rows and rid not in touched:
                    errs.append(f"{uid}: {rid} names a plane, and no touched plane carries it (`named_by`)")
            args = ((frag.get("seeds") or [{}])[0] or {}).get("args") or {}
            if int(args.get("month_length") or 0) != 28 or len(args.get("months") or []) != 12 or len(args.get("day_names") or []) != 7:
                errs.append(f"{uid}: the calendar is twelve months of 28 days and a seven-day week (the seed's `months`, "
                            "`month_length`, `day_names`)")
        for eid, row in rows:
            if self.frame is not None:
                errs += frame_errors(self.frame, eid, row)
            errs += door.story_field_errors(eid, row)
            if row.get("secrecy") != "secret":
                for path, value in door.prose_strings({k: v for k, v in row.items() if k != "dm_only"}):
                    errs += self.leak_errors(f"{eid}: field {path}", value)
        rel = (frag.get("prose") or {}).get("file") if isinstance(frag.get("prose"), dict) else frag.get("prose")
        f = self.root / str(rel) if rel else None
        if f is not None and f.is_file() and not str(rel).startswith("design/dm-only/"):
            errs += self.leak_errors(f"{uid}: {rel}", f.read_text(encoding="utf-8", errors="replace"))
        return errs, []

    def close(self) -> None:
        if not self.hidden:
            return
        path = dm_only_dir(self.campaign) / "door-log.json"
        doc = read_json(path) or {"_meta": {"schema_version": 1, "campaign": self.campaign}, "entries": []}
        doc["entries"].append({"at": now_iso(), "phase": "P2", "found": self.hidden})
        stamp_meta(doc, self.campaign, "design_cosmos_door.py")
        write_json_atomic(path, doc)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="P2's registry frame (build item 22c)")
    ap.add_argument("-c", "--campaign", required=True)
    ap.add_argument("verb", choices=["show"])
    a = ap.parse_args(argv)
    frame = build(a.campaign)
    if frame is None:
        print("design_cosmos_door: a legacy birth has no P2 frame", file=sys.stderr)
        return 1
    print(json.dumps(frame, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
