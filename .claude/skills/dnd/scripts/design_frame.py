#!/usr/bin/env python3
"""
design_frame.py — P1's registry frame (plan item 25, build item 20a; docs/p1-build-20.md).

Everything in P1's registry rows that is not prose is decided by the rolls, so the script writes it: at `phase P1
begin` the frame of every row the writer owes (the premise, one signature per slot, one break per rolled trope
break) goes to `design/_staging/P1/<premise id>.frame.json`, each row with its fields as the rolls set them and its
text fields standing empty and named under `fill`. The writer copies each row into its fragment, fills the named
fields and copies every other field unchanged; the door (design_door.py) compares each row with the frame it
rebuilds here and refuses a changed or missing frame field by its name (the third test birth lost a whole round to
`stamped must be an object` / `name missing`: the prompt gave the fields without their shape).

A signature's id follows the name the writer picks from its four candidates (`signature_<slug of the name>`), so its
`id` and `name`, and the premise's `signatures` (those three ids), are the writer's to fill; the door checks that
they agree. An `appears` note stands for each hook a signature's tables gave a later floor: its phase and hook are
the frame's, its text the writer's.

    py design_frame.py -c CAMPAIGN show        print the frame (it holds dm-only fields: a developer's command)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import design_dir, dm_only_dir, now_iso, read_json, slug, write_json_atomic  # noqa: E402

FRAME_SUFFIX = ".frame.json"
SLOTS = ("people", "institution", "phenomenon")
SIGNATURE_KIND = {"people": "creature", "institution": "institution", "phenomenon": "magic"}
PREMISE_FILE = "design/premise.md"
EMPTY = ""


def premise_id(campaign: str) -> str:
    return f"premise_{campaign.replace('-', '_')}"


def frame_rel(campaign: str) -> str:
    return f"design/_staging/P1/{premise_id(campaign)}{FRAME_SUFFIX}"


def signature_id(name: str) -> str:
    """The id a signature takes from its name: `the Harrow Brotherhood` → `signature_harrow_brotherhood`."""
    import design_door as door
    return "signature_" + slug(door.bare(name))


def _row(eid, etype: str, name, lang, **fields) -> dict:
    return {"id": eid, "type": etype, "name": name, "aliases": [], "summary": EMPTY, "file": PREMISE_FILE, "secrecy": "public",
            "created_phase": "P1", "origin": "birth", "lang": lang, **fields, "refs": []}


def build(campaign: str, manifest: dict | None = None) -> dict | None:
    """The frame of a birth whose P1 the script rolled; None for a legacy birth."""
    import design_door as door
    m = manifest or dm.load(campaign)
    if not door.applies(m, "P1"):
        return None
    ident, found = m["identity"], m["foundation"]
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    langs = naming.get("languages") or {}
    # the premise's and the breaks' language: the second living language (the common tongue, or the other side's when
    # "there is no common tongue" was rolled: design_names.language_owners)
    common = next((lid for lid in ("common", "other_side", "people") if lid in langs), EMPTY)
    secret = ((read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("identity") or {}).get("secret") or {}
    staging = "design/_staging/P1"

    signatures = {}
    for slot in SLOTS:
        hooks = door.hooks_by_floor_of(ident, slot)
        notes = [{"phase": p, "hook": h, "text": EMPTY} for p in sorted(hooks) for h in sorted(hooks[p])]
        cand = (naming.get("candidates") or {}).get(slot) or {}
        reg = _row(EMPTY, "signature", EMPTY, cand.get("language") or EMPTY, kind=SIGNATURE_KIND[slot], slot=slot,
                   home=door.home_id_of(ident, found, slot), rolled=door.rolled_of_identity(ident, slot), rule=EMPTY,
                   appears=notes, stamped={"kind": SIGNATURE_KIND[slot], "slot": slot})
        signatures[slot] = {"fragment": f"{staging}/signature_<slug of the name you pick>.json",
                            "candidates": [c["name"] for c in cand.get("names") or []],
                            "registry": reg,
                            "fill": ["id", "name", "aliases", "summary", "rule", "refs", "appears[].text"]}

    breaks = {}
    for b in ident["trope_breaks"]:
        label = (dt.row("trope-breaks.yaml", b["id"]) or {}).get("label") or b["id"]
        reg = _row(b["id"], "break", label, common, row=b["id"], tie=b["tie"], stamped={"row": b["id"]})
        breaks[b["id"]] = {"fragment": f"{staging}/{b['id']}.json", "registry": reg, "fill": ["aliases", "summary", "refs"]}

    pid = premise_id(campaign)
    twist = secret.get("twist")
    arch = dt.row("secrets.yaml#twist", twist) if twist else None
    pin = secret.get("pin") or {}
    pinned = ({"god": EMPTY, "relation": pin.get("relation"), "event": pin.get("event") or "the move"} if pin.get("god")
              else {"piece": pin.get("piece"), "event": pin.get("event") or "the move"})
    clues = [{"n": s["n"], "levels": list(s["levels"]), "kind": EMPTY, "piece": s["clues"][0]["piece"], "how": EMPTY, "placed_in": None}
             for s in secret.get("stages") or []]
    breaks_ids = [b["id"] for b in ident["trope_breaks"]]
    premise = _row(pid, "premise", "The premise", common, question=EMPTY, pitch=EMPTY,
                   tensions=[q["id"] for q in ident["questions"]], signatures=[], trope_breaks=breaks_ids,
                   secret_class=(arch or {}).get("hides_in") or "threat",
                   stamped={"question": EMPTY, "signatures": [], "trope_breaks": list(breaks_ids)},
                   dm_only={"secret_twist": twist, "secret": EMPTY, "villain_answer": EMPTY, "dm_pitch": EMPTY,
                            "pinned": pinned, "clues": clues, "stamped_fields": ["secret_twist"]})
    fill = ["summary", "question", "pitch", "signatures", "refs", "stamped.question", "stamped.signatures",
            "dm_only.secret", "dm_only.villain_answer", "dm_only.dm_pitch", "dm_only.clues[].kind", "dm_only.clues[].how"]
    if pin.get("god"):
        fill.append("dm_only.pinned.god")
    return {"_meta": {"schema_version": 1, "campaign": campaign, "written_by": "design_frame.py", "written_at": now_iso(),
                      "what": "P1's registry rows as the rolls set them (build item 20a)"},
            "how": ("Copy each row's `registry` into its own fragment (the path under `fragment`), fill the fields its "
                    "`fill` names and copy every other field unchanged: the door refuses a changed or missing frame "
                    "field. `stamped` stays an object; its filled values equal the row's own fields of the same name."),
            "premise": {"fragment": f"{staging}/{pid}.json", "registry": premise, "fill": fill},
            "signatures": signatures, "breaks": breaks}


def write(campaign: str) -> Path | None:
    """`phase P1 begin`: write the frame beside the premise's fragment path."""
    frame = build(campaign)
    if frame is None:
        return None
    path = design_dir(campaign).parent / frame_rel(campaign)
    write_json_atomic(path, frame)
    return path


# ── the door's comparison ────────────────────────────────────────────────────────────────────────────────────

def _diff(frame, got, fill: set, path: str = "") -> list[tuple[str, str]]:
    """(kind, dotted path) for each frame field the row lacks, changes or reshapes; filled fields are not compared."""
    out = []
    for key, want in frame.items():
        p = f"{path}{key}"
        if p in fill:
            continue
        if key not in got:
            out.append(("missing", p))
            continue
        have = got[key]
        if isinstance(want, dict):
            if not isinstance(have, dict):
                out.append(("shape", p))
            else:
                out += _diff(want, have, fill, p + ".")
        elif isinstance(want, list) and any(f.startswith(p + "[].") for f in fill):
            if not isinstance(have, list) or len(have) != len(want) or not all(isinstance(x, dict) for x in have):
                out.append(("changed", p))
            else:
                for w, h in zip(want, have):
                    out += _diff(w, h, fill, p + "[].")
        elif have != want:
            out.append(("changed", p))
    return list(dict.fromkeys(out))


def frame_errors(campaign: str, frame: dict, eid: str, row: dict, rows: dict) -> list[str]:
    """A P1 row against its frame: the fields named, never their values (a dm-only field's value is secret)."""
    etype = row.get("type")
    if etype == "premise" and eid == frame["premise"]["registry"]["id"]:
        entry = frame["premise"]
    elif etype == "signature" and row.get("slot") in frame["signatures"]:
        entry = frame["signatures"][row["slot"]]
    elif etype == "break" and row.get("row") in frame["breaks"]:
        entry = frame["breaks"][row["row"]]
    else:
        return []           # an unknown slot or break row is refused by the door's own checks
    where = frame_rel(campaign)
    say = {"missing": "is missing; the script's frame sets it",
           "changed": "differs from the script's frame; the rolls set it",
           "shape": "must be an object, as the script's frame has it"}
    errs = [f"{eid}: `{p}` {say[kind]} (copy it unchanged from {where})" for kind, p in _diff(entry["registry"], row, set(entry["fill"]))]
    stamped = row.get("stamped")
    if isinstance(stamped, dict):
        for key in entry["registry"]["stamped"]:
            if key in stamped and key in row and stamped[key] != row[key]:
                errs.append(f"{eid}: `stamped.{key}` must equal the row's own `{key}`")
    if etype == "signature" and row.get("name") and eid != signature_id(row["name"]):
        errs.append(f"{eid}: a signature's id is `signature_<slug of its name>`: {signature_id(row['name'])}")
    if etype == "premise":
        sigs = sorted(k for k, r in rows.items() if r.get("type") == "signature")
        if sorted(row.get("signatures") or []) != sigs:
            errs.append(f"{eid}: `signatures` lists the ids of the three signature rows beside it ({', '.join(sigs) or 'none'})")
    return errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="P1's registry frame (build item 20a)")
    ap.add_argument("-c", "--campaign", required=True)
    ap.add_argument("verb", choices=["show"])
    a = ap.parse_args(argv)
    frame = build(a.campaign)
    if frame is None:
        print("design_frame: a legacy birth has no frame", file=sys.stderr)
        return 1
    print(json.dumps(frame, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
