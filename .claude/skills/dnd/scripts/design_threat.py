#!/usr/bin/env python3
"""
design_threat.py — the threat, P1's story begun from someone who wants something (plan item 25, build item 18c;
docs/p1-threat-first.md "The new core", G1, G4, G8; docs/p1-build-18-rows.md sections 4 and 8).

`roll(R, dials, spine, palette, ruin_id, contests)` makes the threat's draws through a designer Roller, every one of
them secret, after the contest and before the move (G4's step 4; `design_foundation.roll` calls it there, so each
later roll stands on it):

1. the family (`antagonists.yaml#villain_family`): a family the last three births drew waits; weighted by the ruin
   and the content mix; the god at standard and epic only; the two dragon families carry no weight;
2. the creature: an SRD creature of the family whose CR fits the level band's top L (from max(2, L-2) to L+4, to 30
   once L reaches 17), drawn on a die; where none fits, a reskin `{base, target_cr}` of the family's nearest base
   (sites.yaml's reskin rule; the stat work is P5's); the god's creature is always an avatar reskin;
3. the power source: a humanoid family above short draws one;
4. the visibility, the shape (a public figure's shape is forced when its contest is rolled and the visibility is the
   one its row names, as build item 16c ruled), the origin (a shape and origin pair another birth drew waits);
5. the goal: bound to a rolled piece, a goal whose pieces hold the main contest's prize weighing x2; the threat joins
   the contest (`join`): `prize` (the goal's piece is the prize), `role_goal` (a goal that names a contest role by
   nature), else `move` (18c-2's move strikes the prize's piece or a contest role: the only forced case);
6. the weakness, fitted to the family;
7. the lair: its form fitted to the family, its where to the chain (the thin place only where one exists; on the
   move only with a mobile form; a place it built only with a form it can build).

The return is dm-only (`dice-log.json#threat`); design.json and the card never hold it.
"""

from __future__ import annotations

import json
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_dice as dd  # noqa: E402
import design_tables as dt  # noqa: E402
from paths import data_dir  # noqa: E402

V = "antagonists.yaml#"
VILLAIN_PAIR_KEY = "antagonists.yaml#shape_origin_pair"     # used.json: shape|origin, hashed, never repeated
PIECES_ALWAYS = ("heart", "key_place", "disputed_land", "remnant", "role", "new")
# the visibilities under which the villain itself is public (the 18c-1 audit): a world state may join it only then
PUBLIC_VISIBILITY = ("vis_known_untouchable", "vis_known_unknown_where")
DRAGON_COLOURS = ("black", "blue", "green", "red", "white", "brass", "bronze", "copper", "gold", "silver")


def rows_by_id(sub: str) -> dict:
    return {r["id"]: r for r in dt.rows_and_retired(V + sub)}


@lru_cache(maxsize=1)
def srd_creatures() -> dict:
    """SRD monster index → {name, cr, type}."""
    doc = json.loads((data_dir() / "dnd5e_srd.json").read_text(encoding="utf-8"))
    return {m["index"]: {"name": m["name"], "cr": float(m["cr"]), "type": m["type"]} for m in doc["monsters"]}


def cr_window(top_level: int) -> tuple[float, float]:
    """The CR a final fight at the level band's top L stands at: max(2, L-2) to L+4, to 30 once L reaches 17."""
    lo = max(2, top_level - 2)
    return float(lo), float(30 if top_level >= 17 else min(30, top_level + 4))


def candidates(family: dict, top_level: int) -> list[str]:
    lo, hi = cr_window(top_level)
    srd = srd_creatures()
    return sorted((c for c in family.get("creatures") or [] if c in srd and lo <= srd[c]["cr"] <= hi),
                  key=lambda c: (srd[c]["cr"], c))


def creature_of(R, family: dict, top_level: int) -> dict:
    srd = srd_creatures()
    pool = [] if family.get("avatar") else candidates(family, top_level)
    if pool:
        pick = pool[int(R.notation("threat.creature", f"d{len(pool)}", secret=True)["raw"]) - 1]
        return {"index": pick, "name": srd[pick]["name"], "cr": srd[pick]["cr"]}
    lo, hi = cr_window(top_level)
    target = max(lo, min(hi, float(top_level)))
    base = min(family["reskin"], key=lambda b: (abs(srd[b]["cr"] - target), b))
    rec = R._record("threat.creature", None)
    rec.update({"notation": "derived", "raw": None, "value": base, "derived_from": "no SRD creature of the family fits the band: a reskin"})
    R._keep(rec, True)
    return {"reskin": {"base": base, "base_cr": srd[base]["cr"], "target_cr": target}, "avatar": bool(family.get("avatar"))}


def pieces_available(palette) -> set:
    return set(PIECES_ALWAYS) | ({"thin_place"} if "land_thin_place" in palette else set())


def prize_piece(prize_kind: str) -> str:
    """The goal piece a prize kind is: a seat is a role's house."""
    return {"seat": "role"}.get(prize_kind, prize_kind)


def weakness_fits(row: dict, family: dict) -> bool:
    if row.get("fits") and family["id"] not in row["fits"]:
        return False
    return not family.get("weaknesses") or row["id"] in family["weaknesses"]


def where_fits(where: dict, form: dict, palette) -> bool:
    if where["piece"] == "moving":
        return bool(form.get("mobile"))
    if form.get("mobile"):
        return False
    if where["piece"] == "new":
        return bool(form.get("built"))
    return where["piece"] != "thin_place" or "land_thin_place" in palette


def roll(R, dials: dict, spine: dict, palette, ruin_id: str, contests: list[dict], used_pairs: set | None = None) -> dict:
    """Every threat draw, secret, through the Roller; returns the dm-only record."""
    import design_foundation as fd
    scale, top = dials["scale"], int(dials["level_band"][1])
    if used_pairs is None:
        used_pairs = dd.used_values(R.campaign, VILLAIN_PAIR_KEY) if R.campaign else set()

    # 1-3. the family, the creature, the power source
    fam_id = R.table("threat.family", V + "villain_family", secret=True)["row_id"]
    family = rows_by_id("villain_family")[fam_id]
    creature = creature_of(R, family, top)
    power = None
    if family.get("power_source") and scale != "short":
        power = R.table("threat.power_source", V + "power_source", secret=True)["row_id"]

    # 4. the visibility, the shape (a public figure's when its contest is rolled), the origin
    visibility = R.table("bbeg_visibility", V + "visibility", secret=True)["row_id"]
    rolled_public = {c["id"]: n for n, c in enumerate(contests)}
    figure, barred = None, set()
    for row in dt.rows(V + "villain_shape"):
        for public_id, rule in (row.get("same_figure_with") or {}).items():
            if public_id not in rolled_public:
                continue
            if visibility == rule["visibility"]:
                figure = {"shape": row["id"], "contest": public_id, "role": rule["role"], "main": rolled_public[public_id] == 0}
            else:
                barred.add(row["id"])
    if figure:
        shape = R.forced("bbeg_shape", V + "villain_shape", figure["shape"], "the villain is the public figure of a rolled contest", secret=True)["row_id"]
    else:
        shape = R.table("bbeg_shape", V + "villain_shape", secret=True, exclude=barred)["row_id"]
    spent = {o["id"] for o in dt.rows(V + "origin") if dd.hashed(f"{shape}|{o['id']}") in used_pairs}
    rec = R.table("bbeg_origin", V + "origin", secret=True, also_used=spent)
    origin = rec["row_id"]
    rec["used_keys"] = {VILLAIN_PAIR_KEY: f"{shape}|{origin}"}       # approve writes it hashed; the pair never repeats

    # 5. the goal, bound to a rolled piece; joined to the contest by its prize, or the move strikes a role
    have = pieces_available(palette)
    main_row = fd.rows_by_id("contest")[contests[0]["id"]]
    prize = prize_piece((main_row.get("prize_with") or {}).get(ruin_id, main_row["prize"]))
    import design_arbiter as arb
    weigh = lambda r, ctx: arb.weight_of(r, ctx) * (2.0 if prize in r["pieces"] and prize in have else 1.0)
    goal_id = R.table("threat.goal", V + "goal", secret=True, where=lambda r: bool(set(r["pieces"]) & have),
                      why="a piece the chain holds", weigh=weigh)["row_id"]
    goal_row = rows_by_id("goal")[goal_id]
    if prize in goal_row["pieces"] and prize in have:
        piece, join = prize, "prize"
    elif goal_row.get("role_goal"):
        piece, join = "role", "role_goal"
    else:
        options = [p for p in goal_row["pieces"] if p in have]
        piece = options[0] if len(options) == 1 else options[int(R.notation("threat.goal.piece", f"d{len(options)}", secret=True)["raw"]) - 1]
        join = "move"
    goal = {"id": goal_id, "piece": piece, "join": join, "contest": contests[0]["id"]}

    # 6. the weakness; 7. the lair
    weakness = R.table("threat.weakness", V + "weakness", secret=True, where=lambda r: weakness_fits(r, family),
                       why="fits the family")["row_id"]
    colour = next((c for c in DRAGON_COLOURS if f"-{c}-dragon" in str(creature.get("index") or "")), None)
    import design_arbiter as arb
    weigh_form = lambda r, ctx: arb.weight_of(r, ctx) * (3.0 if colour and colour in (r.get("dragon_colours") or []) else 1.0)
    form_id = R.table("threat.lair_form", V + "lair_form", secret=True, where=lambda r: fam_id in (r.get("fits") or []),
                      why="fits the family", weigh=weigh_form)["row_id"]
    form = rows_by_id("lair_form")[form_id]
    where_id = R.table("threat.lair_where", V + "lair_where", secret=True, where=lambda r: where_fits(r, form, palette),
                       why="fits the form and the chain")["row_id"]

    return {"family": fam_id, "creature_type": family["creature_type"], "creature": creature, "power_source": power,
            "visibility": visibility, "shape": shape, "origin": origin,
            "public_figure": {"contest": figure["contest"], "role": figure["role"], "main": figure["main"]} if figure else None,
            "goal": goal, "weakness": weakness, "lair": {"form": form_id, "where": where_id}, "band_top": top}
