"""
_p1_frame.py — a stand-in writer that fills P1's registry frame (build item 20a): it copies every row of the script's
frame and writes only the fields the frame names under `fill`, as the writer's prompt asks.
"""

import copy
import sys

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_frame as dfr  # noqa: E402

QUESTION = "who keeps what the old keepers left?"
PITCH = "One thing is asked. Three things are only here. One rule is turned over."


def fill(frame: dict, god: str | None = None, question: str = QUESTION, pitch: str = PITCH,
         note=lambda slot: f"at this floor the {slot} shows in what the natives do every day") -> tuple[dict, dict]:
    """(rows by id: the signatures, the breaks, then the premise; the name picked per slot)."""
    rows, picked = {}, {}
    for slot, entry in frame["signatures"].items():
        name = entry["candidates"][0]
        r = copy.deepcopy(entry["registry"])
        r.update(id=dfr.signature_id(name), name=name, summary="what a native would say of it, in one line.",
                 rule="how a native knows it, in a line.")
        for n in r["appears"]:
            n["text"] = note(slot)
        rows[r["id"]], picked[slot] = r, name
    for bid, entry in frame["breaks"].items():
        r = copy.deepcopy(entry["registry"])
        r["summary"] = "the break as a native states it."
        rows[bid] = r
    p = copy.deepcopy(frame["premise"]["registry"])
    sigs = [e for e in rows if e.startswith("signature_")]
    p.update(summary="the question in one line.", question=question, pitch=pitch, signatures=sigs, refs=list(sigs))
    p["stamped"].update(question=question, signatures=list(sigs))
    d = p["dm_only"]
    d.update(secret="the truth of the move, told once and only here.", villain_answer="the pole carried to its end.",
             dm_pitch="what the keeper of the table steers toward.")
    if "god" in d["pinned"]:
        d["pinned"]["god"] = god
    for c in d["clues"]:
        c.update(kind="a thing seen", how="a search")
    rows[p["id"]] = p
    return rows, picked
