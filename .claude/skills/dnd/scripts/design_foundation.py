#!/usr/bin/env python3
"""
design_foundation.py — P1's first step, the foundation, built by script with no model (plan item 25, step 1;
docs/p1-foundation-rows.md §1-6 and §18; the owner's rulings on items 3-5 of the build, 2026-09-28).

`roll(R, dials)` makes the step's draws through a designer Roller (so every draw passes design_arbiter) in this order:

1. the spine (`foundation.yaml#spine`);
2. the palette: the spine's `forces`, one of its `forces_one_of`, the era's forced kinds, then a height and a water if
   none came, then the rest up to the scale's count; fantastic kinds up to the magic dial's cap (a `cap_exempt` kind
   never counts); an `implies` kind comes along;
3. the ruin source: its `adds_palette` kind comes on top of the count (+1), skips the kind's own magic requirement and
   is the only exempt one;
4. the lifeline, seated on the spine;
5. the contest (epic: a second one from another family, three roles, on another part of the spine);
6. the break: target (a role target names the role), action (it must strike that target and fit its family or kind;
   a target + action pair another birth used waits as usage), scars (the new-land scar needs room in the cap and adds
   a fantastic kind; a closed thin place bars the thinner-border scar), time, winner (the scale's roles of the main
   contest, never the role the break destroyed; the struck role when a role rose);
7. the escalation: the tiers of play the level band touches.

`build(records)` turns the records into the foundation (public, stamped in design.json), with the merge rules (one
crater; the planar rift is the two worlds' crossing point), the start (a destroyed heart moves it) and the Turkish
foundation sentence from five templates. The sentence adds no suffix to any fragment.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_tables as dt  # noqa: E402

F = "foundation.yaml"
PAIR_KEY = "foundation.yaml#break_pair"     # used.json: target piece + action, never repeated
PIECE_OF_TARGET = {"target_lifeline": "lifeline", "target_remnant": "remnant", "target_key_place": "key_place",
                   "target_heart": "heart", "target_role": "role", "target_thin_place": "thin_place"}


def ref(sub: str) -> str:
    return f"{F}#{sub}"


def rows_by_id(sub: str) -> dict:
    return {r["id"]: r for r in dt.rows(ref(sub))}


def header(sub: str) -> dict:
    return dt.roll_header(ref(sub))


def is_capped(row: dict) -> bool:
    """A fantastic kind the cap counts (the thin place never does)."""
    return bool(row.get("fantastic")) and not row.get("cap_exempt")


def tiers_touched(level_band) -> list[str]:
    lo, hi = int(level_band[0]), int(level_band[1])
    return [t["id"] for t in dt.rows(ref("escalation_tier")) if t["levels"][0] <= hi and t["levels"][1] >= lo]


def roll(R, dials: dict, used_pairs: set | None = None) -> dict:
    """Every step-1 draw through the Roller; returns the ids the build needs (the records are on R)."""
    palette_rows = rows_by_id("palette")
    scale, magic, era = dials["scale"], dials["magic"], dials.get("era")
    pal_head = header("palette")
    cap = int(pal_head["fantastic_cap_by_magic"][magic])
    out: dict = {"palette": [], "palette_extra": []}

    # 1. the spine
    spine_id = R.table("foundation.spine", ref("spine"))["row_id"]
    spine = rows_by_id("spine")[spine_id]
    out["spine"] = spine_id

    # 2. the palette
    palette: list[str] = out["palette"]

    def add_forced(kind: str, why: str, label: str | None = None) -> None:
        if kind in palette:
            return
        R.forced(label or f"foundation.palette.{len(palette) + 1}", ref("palette"), kind, why)
        palette.append(kind)
        for imp in palette_rows[kind].get("implies") or []:
            add_forced(imp, f"implied by {kind}")

    for kind in spine.get("forces") or []:
        add_forced(kind, f"forced by {spine_id}")
    if spine.get("forces_one_of"):
        choice = spine["forces_one_of"]
        rec = R.table(f"foundation.palette.{len(palette) + 1}", ref("palette"), avoid=False,
                      where=lambda r, c=choice: r["id"] in c, why=f"one of {spine_id}'s kinds", exclude=set(palette))
        palette.append(rec["row_id"])
    for dial, by_value in (pal_head.get("forces_by_dial") or {}).items():
        for kind in (by_value or {}).get(dials.get(dial), []):
            add_forced(kind, f"forced by the {dial} dial ({dials.get(dial)})")
    count = R.count("foundation.palette_count", pal_head["count_by_scale"][scale])

    def capped_now() -> int:
        return sum(1 for k in palette if is_capped(palette_rows[k]))

    def draw_kind(where, why: str) -> None:
        room = capped_now() < cap
        rec = R.table(f"foundation.palette.{len(palette) + 1}", ref("palette"), avoid=False, exclude=set(palette),
                      where=lambda r: where(r) and (room or not is_capped(r)), why=why)
        palette.append(rec["row_id"])
        for imp in palette_rows[rec["row_id"]].get("implies") or []:
            add_forced(imp, f"implied by {rec['row_id']}")

    if not any(palette_rows[k].get("height") for k in palette):
        draw_kind(lambda r: bool(r.get("height")), "a height")
    if not any(palette_rows[k].get("water") and not palette_rows[k].get("fantastic") for k in palette):
        draw_kind(lambda r: bool(r.get("water")) and not r.get("fantastic"), "a water")
    while len(palette) < count:
        draw_kind(lambda r: True, "the palette")

    # 3. the ruin source
    ruin_id = R.table("foundation.ruin", ref("ruin_source"))["row_id"]
    ruin = rows_by_id("ruin_source")[ruin_id]
    out["ruin"] = ruin_id
    if ruin.get("adds_palette") and ruin["adds_palette"] not in palette:
        R.forced("foundation.palette.ruin", ref("palette"), ruin["adds_palette"],
                 f"brought by {ruin_id}: on top of the count, exempt from the cap and the kind's magic requirement")
        out["palette_extra"].append(ruin["adds_palette"])

    # 4. the lifeline (seated by the layout, build item 6b)
    life_id = R.table("foundation.lifeline", ref("lifeline"))["row_id"]
    life = rows_by_id("lifeline")[life_id]
    out["lifeline"] = life_id

    # 5. the contest
    roles_by_scale = header("contest")["roles_by_scale"]

    def role_claims(row: dict, roles: list[str]) -> dict:
        """The claims of the roles the scale seats (a role's claim is silent when the role is not seated)."""
        merged: dict = {}
        for key in roles:
            merged.update((row["roles"].get(key) or {}).get("claims") or {})
        return merged

    def seat_claims(n: int, cid: str, roles: list[str]) -> None:
        row = rows_by_id("contest")[cid]
        toks = [t for key in roles for t in dt.claim_tokens((row["roles"].get(key) or {}).get("claims"))]
        R.add_tokens(f"foundation.contest.{n}.claims", toks, f"the seated roles of {cid}: {', '.join(roles)}")

    roles1 = list(roles_by_scale[scale])
    c1 = R.table("foundation.contest.1", ref("contest"),
                 where=lambda r: not R.ctx.clashes(role_claims(r, roles1)), why="a seated role's claim")["row_id"]
    out["contests"] = [{"id": c1, "roles": roles1}]
    seat_claims(1, c1, roles1)
    if int(header("contest")["contests_by_scale"][scale]) > 1:
        fam1 = rows_by_id("contest")[c1]["family"]
        roles2 = ["a", "b", "third"]
        c2 = R.table("foundation.contest.2", ref("contest"), exclude={c1},
                     where=lambda r: r["family"] != fam1 and not R.ctx.clashes(role_claims(r, roles2)),
                     why="another family, and a seated role's claim")["row_id"]
        out["contests"].append({"id": c2, "roles": roles2})
        seat_claims(2, c2, roles2)
    main = rows_by_id("contest")[c1]
    main_roles = out["contests"][0]["roles"]

    # 6. the break
    remnant_kind = ruin["remnant_kind"]
    key_kind = spine["key_kind"]
    life_family = life["family"]
    actions = rows_by_id("action")

    def fits(act: dict, piece: str) -> bool:
        if piece not in act["targets"]:
            return False
        table = act.get("fits") or {}
        return {"lifeline": life_family in table.get("lifeline", []),
                "remnant": remnant_kind in table.get("remnant", []),
                "key_place": key_kind in table.get("key_place", [])}.get(piece, True)

    target_id = R.table("foundation.break.target", ref("break_target"), avoid=False,
                        where=lambda r: any(fits(a, r["piece"]) for a in actions.values()), why="an action can strike it")["row_id"]
    piece = PIECE_OF_TARGET[target_id]
    out["target"] = target_id
    role = None
    if piece == "role":
        role = main_roles[int(R.notation("foundation.break.role", f"d{len(main_roles)}")["raw"]) - 1]
        out["target_role"] = role
    spent = {a for a in actions if f"{piece}|{a}" in (used_pairs or set())}
    rec = R.table("foundation.break.action", ref("action"), where=lambda r: fits(r, piece), why="fits the target",
                  also_used=spent)
    act_id = rec["row_id"]
    rec["used_keys"] = {PAIR_KEY: f"{piece}|{act_id}"}     # approve writes it; the pair never repeats
    act = actions[act_id]
    out["action"] = act_id

    barred = set((act.get("bars_scars_on_target") or {}).get(piece, []))
    scars: list[str] = []
    for n in range(1, int(header("scar")["count_by_scale"][scale]) + 1):
        room = capped_now() < cap

        def scar_ok(r, room=room):
            return r["id"] not in barred and (room or not r.get("needs_fantastic_room"))
        sid = R.table(f"foundation.break.scar.{n}", ref("scar"), exclude=set(scars), where=scar_ok,
                      why="the target, the action and the fantastic cap")["row_id"]
        scars.append(sid)
        if rows_by_id("scar")[sid].get("needs_fantastic_room"):
            rec = R.table("foundation.palette.scar", ref("palette"), avoid=False, exclude=set(palette) | set(out["palette_extra"]),
                          where=lambda r: is_capped(r), why="the scar's new kind (it counts toward the cap)")
            palette.append(rec["row_id"])
    out["scars"] = scars
    out["time"] = R.table("foundation.break.time", ref("time"))["row_id"]

    destroyed = role if (piece == "role" and "role" in (act.get("destroys") or [])) else None
    if act.get("winner_is_target_role") and piece == "role":
        R.forced("foundation.break.winner", "dice", role, f"{act_id} on a role: the role that rose is the winner")
        out["winner"] = role
    else:
        candidates = [k for k in main_roles if k != destroyed]
        out["winner"] = candidates[int(R.notation("foundation.break.winner", f"d{len(candidates)}")["raw"]) - 1]
    # a destroyed heart moves the start (owner, 2026-09-28): to its ruins when the action leaves some, else end_a
    if piece == "heart" and "heart" in (act.get("destroys") or []):
        out["start"] = "heart_ruins" if act.get("leaves_ruins") else "end_a"
    else:
        out["start"] = "heart"

    # the layout: the palette on the spine's parts, the lifeline and the contests' roles seated on them
    out["layout"] = lay_out(R, spine, palette + out["palette_extra"], life, out["contests"], out)
    # the layout's tokens (build item 7c): a heart below ground is a land lived in below; the remnant on the heart
    lay_tokens = []
    if out["layout"]["parts"].get("heart") == "land_underground":
        lay_tokens.append(dt.token("below_ground", "lived_in"))
    if out["layout"]["remnant"] == "heart":
        lay_tokens.append("layout:remnant_on_heart")
    R.add_tokens("foundation.layout.tokens", lay_tokens, "the layout")

    # 7. the escalation
    out["escalation"] = tiers_touched(dials["level_band"])
    for n, tier in enumerate(out["escalation"], 1):
        R.forced(f"foundation.escalation.{n}", ref("escalation_tier"), tier, "the tiers the level band touches")
    return out


# ── the layout (build item 6b; owner, 2026-09-29) ────────────────────────────────────────────────────────────

END_PARTS = ("end_a", "end_b", "end_c", "end_d")


def _choose(R, label: str, options: list):
    if len(options) == 1:
        return options[0]
    return options[int(R.notation(label, f"d{len(options)}")["raw"]) - 1]


def lay_out(R, spine: dict, kinds: list[str], life: dict, contests: list[dict], out: dict) -> dict:
    """The palette's kinds on the spine's parts: the key place on a kind its key_kind stands on, the ends on
    different kinds, the heart on its preference; every other kind along the spine. The lifeline sits on a part (or
    an along node) whose kind its `where` holds; an everywhere row on any part. The contests' roles: a on end_a, b on
    end_b, the third on the heart, the fourth along, unless the row's `seats` say otherwise; epic's second contest
    on the parts the first left free, else along. The ruin's remnant: by a merge rule, else where the ruin's own kind
    lies, else an end or an along node, never the heart without a merge. The break lies where its target is; a prize
    lies on its piece, a new resource where the break struck (owner, 2026-09-29)."""
    doc = dt.load(F)
    wanted = spine["parts"]
    order = ["key_place"] + [p for p in END_PARTS if p in wanted] + ["heart"]
    lands = (doc.get("key_kind_lands") or {}).get(spine["key_kind"])
    parts: dict[str, str] = {}
    for part in order:
        def allowed(k, part=part):
            if part == "key_place" and lands is not None and k not in lands:
                return False
            if part.startswith("end_") and k in [parts[p] for p in parts if p.startswith("end_")]:
                return False
            return True
        cand = [k for k in (wanted.get(part) or []) if k in kinds and allowed(k)]
        fresh = [k for k in cand if k not in parts.values()]      # variety: a kind no part holds yet comes first
        cand = fresh or cand
        if not cand:
            placed = set(parts.values())
            free = [k for k in kinds if allowed(k)]
            cand = [k for k in free if k not in placed] or free
        if not cand:
            raise SystemExit(f"design_foundation: no palette kind for the spine's {part} — a table fault")
        parts[part] = _choose(R, f"foundation.layout.{part}", cand)
    along = [k for k in kinds if k not in parts.values()]

    # the lifeline
    where = set(life.get("where") or [])
    seats = [p for p in order if not where or parts[p] in where]
    seats += [f"along:{k}" for k in along if where and k in where]
    if life["family"] == "passage" and "key_place" in seats:
        life_seat = "key_place"
    else:
        if not seats:
            raise SystemExit(f"design_foundation: the lifeline {life['id']} finds no part of its kind — a table fault")
        life_seat = _choose(R, "foundation.layout.lifeline", seats)

    # the ruin's remnant
    ruin = rows_by_id("ruin_source")[out["ruin"]]
    merged = merges(out["spine"], out["ruin"])
    if merged:
        remnant = "key_place" if out["ruin"] == "ruin_planar_rift" else "heart"
    else:
        own = ([ruin["adds_palette"]] if ruin.get("adds_palette") else []) + list((ruin.get("requires") or {}).get("any_of") or [])
        spots = [p for p in order if p != "heart" and parts[p] in own] + [f"along:{k}" for k in along if k in own]
        spots = spots or [p for p in order if p.startswith("end_")] + [f"along:{k}" for k in along]
        remnant = _choose(R, "foundation.layout.remnant", spots)

    # the contests
    rows = rows_by_id("contest")
    seated: list[dict] = []
    taken: set = set()
    for n, c in enumerate(contests):
        row = rows[c["id"]]
        if n == 0:
            seat = {"a": "end_a", "b": "end_b", "third": "heart", "fourth": "along"}
            for role, where_to in (row.get("seats") or {}).items():
                if role == "prize":
                    continue
                seat[role] = {"end": "end_a" if role == "a" else "end_b", "beside_key_place": "key_place"}.get(where_to, where_to)
            if "third" in seat and seat["third"] in (seat.get("a"), seat.get("b")):
                seat["third"] = next((p for p in ("end_a", "end_b", "key_place") if p not in (seat["a"], seat["b"])), "along")
        else:
            free = [p for p in order if p not in taken]
            seat = {r: (free.pop(0) if free else "along") for r in ("a", "b", "third")}
        seat = {r: p for r, p in seat.items() if r in c["roles"]}
        taken |= {p for p in seat.values() if p != "along"}
        prize = row["prize"]
        at = (row.get("seats") or {}).get("prize")
        if at == "thin_place":
            at = next((p for p, k in parts.items() if k == "land_thin_place"), "along:land_thin_place")
        elif at is None:
            at = {"lifeline": life_seat, "heart": "heart"}.get(prize)
        seated.append({"contest": c["id"], "seats": seat, "prize": {"kind": prize, "at": at}})

    # where the break struck, from its target; then the prizes a place follows from
    piece = PIECE_OF_TARGET[out["target"]]
    thin = next((p for p, k in parts.items() if k == "land_thin_place"), "along:land_thin_place")
    break_at = {"lifeline": life_seat, "remnant": remnant, "key_place": "key_place", "heart": "heart",
                "role": seated[0]["seats"].get(out.get("target_role")), "thin_place": thin}[piece]
    for c in seated:
        if c["prize"]["at"] is None:
            c["prize"]["at"] = {"remnant": remnant, "new": break_at}[c["prize"]["kind"]]
    return {"parts": parts, "along": along, "lifeline": life_seat, "remnant": remnant, "break_at": break_at,
            "contests": seated}


# ── the build: merges, start, the sentence ───────────────────────────────────────────────────────────────────

def merges(spine_id: str, ruin_id: str) -> list[dict]:
    """The owner's merge rules (2026-09-28): the spine's `merges_with` names the ruins it is one place with."""
    note = ((rows_by_id("spine").get(spine_id) or {}).get("merges_with") or {}).get(ruin_id)
    return [{"spine": spine_id, "ruin": ruin_id, "note": note}] if note else []


def landmarks(spine_id: str, ruin_id: str) -> list[str]:
    """The P3 landmarks the foundation brings; a merge makes the ruin's crater the spine's."""
    spine, ruin = rows_by_id("spine")[spine_id], rows_by_id("ruin_source")[ruin_id]
    out = [spine["landmark"]] if spine.get("landmark") else []
    if ruin.get("landmark") and not (merges(spine_id, ruin_id) and ruin["landmark"] in out):
        out.append(ruin["landmark"])
    return out


def _cap(text: str) -> str:
    if not text:
        return text
    first = {"i": "İ", "ı": "I"}.get(text[0], text[0].upper())
    return first + text[1:]


def _role_phrase(contest: dict, key: str) -> str:
    return contest["roles"][key]["tr"]


def target_phrase(out: dict) -> str:
    spine = rows_by_id("spine")[out["spine"]]
    piece = PIECE_OF_TARGET[out["target"]]
    if piece == "lifeline":
        return rows_by_id("lifeline")[out["lifeline"]]["tr"]["name"]
    if piece == "remnant":
        return rows_by_id("ruin_source")[out["ruin"]]["tr"]["remnant"]
    if piece == "key_place":
        return spine["tr"]["key_place"]
    if piece == "heart":
        return spine["tr"]["heart"]
    if piece == "role":
        return _role_phrase(rows_by_id("contest")[out["contests"][0]["id"]], out["target_role"])
    return rows_by_id("palette")["land_thin_place"]["tr"]["name"]


def sentence(out: dict) -> str:
    """The five templates of item 25, step 1 #7; the fragments are joined by separate words, never suffixed."""
    spine = rows_by_id("spine")[out["spine"]]
    ruin = rows_by_id("ruin_source")[out["ruin"]]
    life = rows_by_id("lifeline")[out["lifeline"]]
    contest = rows_by_id("contest")[out["contests"][0]["id"]]
    act = rows_by_id("action")[out["action"]]
    time = rows_by_id("time")[out["time"]]
    st = spine["tr"]
    if st.get("ends"):
        s1 = f"Dünya {st['name']}: kalbi {st['heart']}, bir ucunda {st['ends'][0]}, öbür ucunda {st['ends'][1]}."
    else:
        s1 = f"Dünya {st['name']}: kalbi {st['heart']}, uçlarında {st['ends_both']}."
    s2 = f"Çok önce {ruin['tr']['what']}; geride {ruin['tr']['remnant']} kaldı."
    s3 = f"Bugün halk {life['tr']['name']} ile yaşıyor."
    roles = out["contests"][0]["roles"]
    s4 = f"{_cap(_role_phrase(contest, 'a'))} ile {_role_phrase(contest, 'b')} arasında eski bir gerilim var; üçüncüsü {_role_phrase(contest, 'third')}"
    s4 += f"; dördüncüsü {_role_phrase(contest, 'fourth')}." if "fourth" in roles else "."
    lead = time["tr"]["lead"]
    form = act["forms"][time["tense"]]
    head = _cap(lead) + (" " if lead.endswith(":") else ", ")
    scars = ", ".join(rows_by_id("scar")[s]["tr"]["name"] for s in out["scars"])
    winner = _role_phrase(contest, out["winner"])
    # a break still coming has left no wound yet: its scars are its first signs
    scar_word = "İlk izleri" if time["id"] == "time_coming" else ("Yaraları" if len(out["scars"]) > 1 else "Yarası")
    s5 = f"{head}{target_phrase(out)} {form}. {scar_word}: {scars}. Bundan güçlü çıkan: {winner}."
    return " ".join([s1, s2, s3, s4, s5])


def build(out: dict, level_band) -> dict:
    """The foundation as design.json keeps it: public, stamped, the identity's input."""
    spine_id, ruin_id = out["spine"], out["ruin"]
    return {
        "stamped": True,
        "spine": spine_id,
        "palette": list(out["palette"]),
        "palette_extra": list(out["palette_extra"]),
        "ruin_source": ruin_id,
        "lifeline": {"id": out["lifeline"], "seat": out["layout"]["lifeline"]},
        "layout": out["layout"],
        "contests": out["contests"],
        "break": {"target": out["target"], "target_role": out.get("target_role"), "action": out["action"],
                  "scars": out["scars"], "time": out["time"], "winner": out["winner"]},
        "escalation": {"tiers": out["escalation"], "steps": len(out["escalation"]), "level_band": list(level_band)},
        "merges": merges(spine_id, ruin_id),
        "landmarks": landmarks(spine_id, ruin_id),
        "start": out["start"],
        "sentence_tr": sentence(out),
    }
