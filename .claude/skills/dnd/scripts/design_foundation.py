#!/usr/bin/env python3
"""
design_foundation.py — P1's first step, the foundation, built by script with no model (plan item 25, step 1;
docs/p1-foundation-rows.md §1-6 and §18; the owner's rulings on items 3-5 of the build, 2026-09-28).

`roll(R, dials)` makes the step's draws through a designer Roller (so every draw passes design_arbiter) in this order:

1. the spine (`foundation.yaml#spine`);
2. the palette: the spine's `forces`, one of its `forces_one_of`, the era's forced kinds, then a height and a water if
   none came, then the rest up to the count the spine's breadth and the scale give (build item 18b); fantastic kinds up to the magic dial's cap (a `cap_exempt` kind
   never counts); an `implies` kind comes along;
3. the ruin source: its `adds_palette` kind comes on top of the count (+1), skips the kind's own magic requirement and
   is the only exempt one;
4. the contest (epic: a second one from another family, three roles, on another part of the spine); its prize fills a
   story slot (build item 18a: never the lifeline);
   then the threat (build item 18c; `design_threat.roll`, every roll secret, dm-only): family, creature, power
   source, visibility, shape, origin, goal, weakness, lair;
5. the break: target (a role target names the role; the target fills a story slot; the goal's join, "the move
   strikes a contest role", is recorded for the move of 18c-2 to honour), action (it must strike that
   target and fit its kind;
   a target + action pair another birth used waits as usage; an action that destroys a role never strikes the last
   seated role that can house the institution), scars (the new-land scar needs room in the cap and adds
   a fantastic kind; a closed thin place bars the thinner-border scar), time, winner (the scale's roles of the main
   contest, never the role the break destroyed; the struck role when a role rose);
6. the lifeline, last (build item 18a: texture hangs on the story, never the other way), seated on the spine;
7. the escalation: the tiers of play the level band touches.

A set whose story slot holds a texture piece is refused (`design_arbiter.slot_errors`): a table fault.

`build(records)` turns the records into the foundation (public, stamped in design.json), with the merge rules (one
crater; the planar rift is the two worlds' crossing point), the start (a destroyed heart moves it) and the English
rendering: a labelled list built from the rows' English fields (build item 13a: a campaign is written in English).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_tables as dt  # noqa: E402

F = "foundation.yaml"
PAIR_KEY = "foundation.yaml#break_pair"     # used.json: target piece + action, never repeated
# target_lifeline is retired (build item 18a); a legacy birth that rolled it still reads
PIECE_OF_TARGET = {"target_lifeline": "lifeline", "target_remnant": "remnant", "target_key_place": "key_place",
                   "target_heart": "heart", "target_role": "role", "target_thin_place": "thin_place"}


def ref(sub: str) -> str:
    return f"{F}#{sub}"


def rows_by_id(sub: str) -> dict:
    """Every row of a sub-table by id, the retired ones too: a lookup of rolled ids, never a pool."""
    return {r["id"]: r for r in dt.rows_and_retired(ref(sub))}


def slots(foundation: dict) -> list[tuple[str, str]]:
    """The story slots a built foundation fills, as (slot, piece): the move's target and every contest's prize."""
    out = [("move_target", PIECE_OF_TARGET[foundation["break"]["target"]])]
    out += [("contest_prize", c["prize"]["kind"]) for c in foundation["layout"]["contests"]]
    return out


def header(sub: str) -> dict:
    return dt.roll_header(ref(sub))


def institution_homes(contest: dict, seated: list[str]) -> list[str]:
    """The seated roles of a contest that can house the signature institution: an archetype hint, no people's role."""
    return [k for k in seated if (contest["roles"].get(k) or {}).get("hint") and not (contest["roles"].get(k) or {}).get("people_role")]


def is_capped(row: dict) -> bool:
    """A fantastic kind the cap counts (the thin place never does)."""
    return bool(row.get("fantastic")) and not row.get("cap_exempt")


def tiers_touched(level_band) -> list[str]:
    lo, hi = int(level_band[0]), int(level_band[1])
    return [t["id"] for t in dt.rows(ref("escalation_tier")) if t["levels"][0] <= hi and t["levels"][1] >= lo]


def roll(R, dials: dict, used_pairs: set | None = None, villain_pairs: set | None = None) -> dict:
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
    # build item 18b: the count follows the spine's breadth (a tight spine one dominant feature, a wide one a journey)
    count = R.count("foundation.palette_count", pal_head["count_by_spine"][spine["breadth"]][scale])
    # the ends lie on different kinds (build item 6b): the count never falls under the spine's ends (the crossroads'
    # four at short, inside its band)
    ends = sum(1 for p in spine["parts"] if p.startswith("end_"))
    if count < ends:
        R.by_label["foundation.palette_count"]["value"] = count = ends

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
    # what the forced kinds and the needs gave before the fill: above the count, they stand and nothing is drawn
    R.by_label["foundation.palette_count"]["before_fill"] = len(palette)
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

    # 4. the contest (the lifeline no longer comes before it: build item 18a)
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
    def key_fits(r: dict) -> bool:
        """A key-place prize stands on a spine whose key place is one of the row's kinds (owner, the 18a audit)."""
        return not r.get("key_kinds") or spine["key_kind"] in r["key_kinds"]

    c1 = R.table("foundation.contest.1", ref("contest"), slot="contest_prize",
                 where=lambda r: key_fits(r) and not R.ctx.clashes(role_claims(r, roles1)),
                 why="the spine's key place, and a seated role's claim")["row_id"]
    out["contests"] = [{"id": c1, "roles": roles1}]
    seat_claims(1, c1, roles1)
    if int(header("contest")["contests_by_scale"][scale]) > 1:
        fam1 = rows_by_id("contest")[c1]["family"]
        roles2 = ["a", "b", "third"]
        c2 = R.table("foundation.contest.2", ref("contest"), exclude={c1}, slot="contest_prize",
                     where=lambda r: r["family"] != fam1 and key_fits(r) and not R.ctx.clashes(role_claims(r, roles2)),
                     why="another family, the spine's key place, and a seated role's claim")["row_id"]
        out["contests"].append({"id": c2, "roles": roles2})
        seat_claims(2, c2, roles2)
    main = rows_by_id("contest")[c1]
    main_roles = out["contests"][0]["roles"]
    # the main prize's kind as a token (build item 18e): a twist that names the prize requires its kind
    R.add_tokens("foundation.prize.tokens", [f"prize:{(main.get('prize_with') or {}).get(ruin_id, main['prize'])}"], "the main contest's prize")

    # 4b. the threat (G4: after the contest, before the move); secret, kept on R for dm-only
    import design_threat as dth
    threat = dth.roll(R, dials, spine, palette + out["palette_extra"], ruin_id, out["contests"], villain_pairs)
    R.threat = threat

    # 5. the move (build item 18c; docs/p1-build-18.md section 6): the hand, the target on the way to the goal, the
    #    verb, the time, the state, the stronger role; public. The labels keep `foundation.break.*` (the break is the move)
    remnant_kind = ruin["remnant_kind"]
    key_kind = spine["key_kind"]
    actions = {r["id"]: r for r in dt.rows(ref("action"))}
    targets = {r["piece"]: r for r in dt.rows(ref("break_target"))}

    def fits(act: dict, piece: str) -> bool:
        if piece not in act["targets"]:
            return False
        table = act.get("fits") or {}
        return {"remnant": remnant_kind in table.get("remnant", []),
                "key_place": key_kind in table.get("key_place", [])}.get(piece, True)

    story = lay_out_story(R, spine, palette + out["palette_extra"], out["contests"], out)
    hand_id = R.table("move.hand", "antagonists.yaml#hand", why="the hand")["row_id"]
    hand = dt.row("antagonists.yaml#hand", hand_id)
    R.add_tokens("move.hand.tokens", [f"hand_family:{x}" for x in hand.get("families") or []], "the hand's creature families")
    allowed = move_targets(threat["goal"], main, ruin_id, palette + out["palette_extra"], story)
    # the order is hand → target → verb (the 18c-2 answer): the goal decides what must be struck, the verb is how the
    # hand strikes it; the target among those the hand can strike with one of its verbs
    hand_verbs = [a for a in actions.values() if not a.get("by") or hand_id in a["by"]]
    target_id = R.table("foundation.break.target", ref("break_target"), avoid=False, slot="move_target",
                        where=lambda r: r["piece"] in allowed and any(fits(a, r["piece"]) for a in hand_verbs),
                        why="on the way to the goal, and the hand has a verb that strikes it",
                        weigh=lambda r, ctx: allowed[r["piece"]]["weight"])["row_id"]
    piece = PIECE_OF_TARGET[target_id]
    out["target"] = target_id
    join_by = allowed[piece]["join_by"]
    spent = {a for a in actions if f"{piece}|{a}" in (used_pairs or set())}
    rec = R.table("foundation.break.action", ref("action"), also_used=spent,
                  where=lambda r: (not r.get("by") or hand_id in r["by"]) and fits(r, piece),
                  why="the hand can make it, and it strikes the target")
    act_id = rec["row_id"]
    act = actions[act_id]
    out["action"] = act_id
    rec["used_keys"] = {PAIR_KEY: f"{piece}|{act_id}"}     # approve writes it; the pair never repeats
    role = None
    if piece == "role":
        # the institution is never left homeless (owner, 2026-10-03): a verb that destroys a role never strikes the
        # last seated role of the main contest that carries an archetype hint and is no people's role
        homes = institution_homes(main, main_roles)
        protected = homes[0] if (len(homes) == 1 and "role" in (act.get("destroys") or [])) else None
        roles = [k for k in main_roles if k != protected]
        role = roles[int(R.notation("foundation.break.role", f"d{len(roles)}")["raw"]) - 1]
        out["target_role"] = role
        if protected:
            rec["protected_role"] = {"role": protected, "why": "the last seated role with an archetype hint that is no people's role"}

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
    # the move's state (the old tie, re-read); a move still coming has none
    state = None if out["time"] == "time_coming" else R.table("move.state", "antagonists.yaml#move_state")["row_id"]

    destroyed = role if (piece == "role" and "role" in (act.get("destroys") or [])) else None
    if act.get("winner_is_target_role") and piece == "role":
        R.forced("foundation.break.winner", "dice", role, f"{act_id} on a role: the role that rose is the winner")
        out["winner"] = role
    else:
        candidates = [k for k in main_roles if k != destroyed]
        out["winner"] = candidates[int(R.notation("foundation.break.winner", f"d{len(candidates)}")["raw"]) - 1]

    # 6. the lifeline, last (build item 18a): its palette fit stays; the story is rolled and reads nothing of it
    life_id = R.table("foundation.lifeline", ref("lifeline"))["row_id"]
    life = rows_by_id("lifeline")[life_id]
    out["lifeline"] = life_id

    # the layout: the palette on the spine's parts, the lifeline and the contests' roles seated on them
    out["layout"] = lay_out_finish(R, story, palette + out["palette_extra"], life, out)
    # the layout's tokens (build item 7c): a heart below ground is a land lived in below; the remnant on the heart
    lay_tokens = []
    if out["layout"]["parts"].get("heart") == "land_underground":
        lay_tokens.append(dt.token("below_ground", "lived_in"))
    if out["layout"]["remnant"] == "heart":
        lay_tokens.append("layout:remnant_on_heart")
    R.add_tokens("foundation.layout.tokens", lay_tokens, "the layout")

    # the start (finding D3): a small settlement at a part that is not the heart, where step 1 lands; the timeline (G2)
    out["start"], start_why = start_part(out["layout"], out["time"], hand_id, out["winner"])
    families = [threat["creature_type"] if f == "villain" else f for f in hand.get("families") or []]
    out["move"] = {"hand": hand_id, "verb": act_id, "target": target_id, "target_role": out.get("target_role"),
                   "time": out["time"], "state": state, "at": "end" if out["time"] == "time_coming" else "start",
                   "join_by": join_by, "goal_join": threat["goal"]["join"],
                   "winner": out["winner"], "start": out["start"], "start_why": start_why, "start_kind": "a village or a small town",
                   "families": families}
    threat["families"] = {"public": families, "secret": [threat["creature_type"]]}      # finding D4; P6 weighs them
    out["spine_sentence"] = spine_sentence(out)

    # 7. the escalation
    out["escalation"] = tiers_touched(dials["level_band"])
    for n, tier in enumerate(out["escalation"], 1):
        R.forced(f"foundation.escalation.{n}", ref("escalation_tier"), tier, "the tiers the level band touches")

    # the one-way rule (build item 18a): no story slot holds a texture piece; such a set is a table fault
    import design_arbiter as arb
    errs = arb.slot_errors([("move_target", piece)] + [("contest_prize", c["prize"]["kind"]) for c in out["layout"]["contests"]])
    if errs:
        raise SystemExit("design_foundation: " + "; ".join(errs) + " — a table fault")
    return out


# ── the move's targets and the start (build item 18c) ───────────────────────────────────────────────────────────

# the goal's piece → the targets on the way to it: the piece itself, a piece that guards it, a contest role; the
# guards of the 18c-2 answer: the thin place guards the remnant and the heart, the remnant the heart, the key place the
# heart and the disputed land
GOAL_TARGETS = {"heart": ("heart", "role", "key_place", "remnant", "thin_place"), "key_place": ("key_place", "role"),
                "disputed_land": ("role", "key_place"), "remnant": ("remnant", "key_place", "role", "thin_place"),
                "thin_place": ("thin_place", "remnant", "key_place", "role"), "role": ("role", "heart"),
                "new": ("remnant", "thin_place", "key_place", "role")}
TARGET_PIECES = ("remnant", "key_place", "heart", "role", "thin_place")


def side_parts(story: dict) -> set:
    """The parts the main contest's sides sit on (an end, the key place, the heart), and the key place, which borders
    the ends: a piece standing there is a side's holding (the 18c-2 answer)."""
    seats = {p for p in story["contests"][0]["seats"].values() if p != "along"}
    return seats | ({"key_place"} if seats & {"end_a", "end_b", "end_c", "end_d"} else set())


def move_targets(goal: dict, main_row: dict, ruin_id: str, kinds, story: dict) -> dict:
    """The pieces the move may strike, each with how it joins the contest (`prize_piece | role | side_holding`, None
    when the goal joins already) and its weight. A goal that joins by its prize or as a role goal: the targets on the
    way to it. A goal that joins through the move: every joinable piece (the prize's piece, a contest role, a piece
    standing on a side's part), the ones on the way to the goal weighing x3. The thin place weighs x3 more wherever it
    is allowed (the 18c-2 answer)."""
    has_thin = "land_thin_place" in kinds
    on_way = {p for p in GOAL_TARGETS[goal["piece"]] if p != "thin_place" or has_thin}
    thin = lambda p: 3.0 if p == "thin_place" else 1.0      # a planar gate stands in few worlds: where it does, it weighs
    if goal["join"] != "move":
        return {p: {"join_by": None, "weight": thin(p)} for p in on_way}
    prize = (main_row.get("prize_with") or {}).get(ruin_id, main_row["prize"])
    sides = side_parts(story)
    spot = {"remnant": story["remnant"], "key_place": "key_place", "thin_place": thin_part(story["parts"]) if has_thin else None}
    out = {}
    for p in TARGET_PIECES:
        if p == prize:
            by = "prize_piece"
        elif p == "role":
            by = "role"
        elif p in spot and spot[p] in sides:
            by = "side_holding"
        else:
            continue
        out[p] = {"join_by": by, "weight": (3.0 if p in on_way else 1.0) * thin(p)}
    return out


def hand_base(layout: dict, hand_id: str | None, winner: str | None) -> str:
    """The hand's base (the 18d answer): a hand from outside at the far end (end_b); a hand inside by nature in the heart,
    or, for the deceived side, on the seat of the side the move made stronger."""
    hand = dt.row("antagonists.yaml#hand", str(hand_id or "")) or {}
    if hand.get("base") != "inside":
        return "end_b"
    if hand.get("id") == "hand_deceived_side" and winner:
        seat = (layout["contests"][0]["seats"].get(winner) or "heart")
        return "heart" if seat == "along" else seat
    return "heart"


def start_part(layout: dict, time_id: str, hand_id: str | None = None, winner: str | None = None) -> tuple[str, str]:
    """The start (finding D3): never the heart. The part nearest the move's target (the target's own part when it is an
    end, the key place or a place along the spine; else the first end); a move still coming starts at the hand's base,
    and where that base is the heart, at the first end."""
    if time_id == "time_coming":
        base = hand_base(layout, hand_id, winner)
        if base != "heart":
            return base, "the move is coming: the start is the hand's base"
        return "end_a", "the move is coming from the heart (a hand inside): the nearest end"
    at = layout.get("break_at")
    if at and at != "heart" and (at.startswith(("end_", "along:")) or at == "key_place"):
        return at, "the part where the move struck"
    return "end_a", "the move struck the heart (or a seat on it): the nearest end"


# ── the layout (build item 6b; owner, 2026-09-29) ────────────────────────────────────────────────────────────

END_PARTS = ("end_a", "end_b", "end_c", "end_d")


def _choose(R, label: str, options: list):
    if len(options) == 1:
        return options[0]
    return options[int(R.notation(label, f"d{len(options)}")["raw"]) - 1]


def lay_out(R, spine: dict, kinds: list[str], life: dict, contests: list[dict], out: dict) -> dict:
    """The whole layout in one call (a caller that has rolled everything): the story half, then the finish."""
    return lay_out_finish(R, lay_out_story(R, spine, kinds, contests, out), kinds, life, out)


def lay_out_story(R, spine: dict, kinds: list[str], contests: list[dict], out: dict) -> dict:
    """The layout's story half (build item 18c: drawn before the move, which reads which piece stands on a side's
    part): the parts, the remnant, the contests' seats and their prizes but a legacy lifeline's and a new one's.
    The palette's kinds on the spine's parts: the key place on a kind its key_kind stands on, the ends on
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
        prize = (row.get("prize_with") or {}).get(out["ruin"], row["prize"])     # the relic's pieces: the ruin's remnant, else new
        at = (row.get("seats") or {}).get("prize")
        if at == "thin_place":
            at = next((p for p, k in parts.items() if k == "land_thin_place"), "along:land_thin_place")
        elif at is None:
            # build item 18a: the key place is the spine's; the disputed land lies between the sides, along the spine,
            # unless `prize_at` names the side whose own land it is (owner, the 18a audit); a seat is the house of role
            # a, whose inheritance it is; a legacy lifeline prize sat on the lifeline
            disputed = seat.get(row["prize_at"], "along") if row.get("prize_at") else "along"
            at = {"heart": "heart", "key_place": "key_place", "disputed_land": disputed, "seat": seat.get("a")}.get(prize)
        seated.append({"contest": c["id"], "seats": seat, "prize": {"kind": prize, "at": at}})
    for c in seated:
        if c["prize"]["at"] is None and c["prize"]["kind"] == "remnant":
            c["prize"]["at"] = remnant
    return {"order": order, "parts": parts, "along": along, "remnant": remnant, "contests": seated}


def lay_out_finish(R, story: dict, kinds: list[str], life: dict, out: dict) -> dict:
    """The layout's second half, after the move and the lifeline: the lifeline's seat (texture, rolled last), where
    the break struck, and the prizes a place follows from (a new one where the break struck; a legacy lifeline's on
    the lifeline). A kind a scar brought after the story half lies along the spine."""
    order, parts, remnant, seated = story["order"], story["parts"], story["remnant"], story["contests"]
    along = list(story["along"]) + [k for k in kinds if k not in parts.values() and k not in story["along"]]
    where = set(life.get("where") or [])
    seats = [p for p in order if not where or parts[p] in where]
    seats += [f"along:{k}" for k in along if where and k in where]
    if life["family"] == "passage" and "key_place" in seats:
        life_seat = "key_place"
    else:
        if not seats:
            raise SystemExit(f"design_foundation: the lifeline {life['id']} finds no part of its kind — a table fault")
        life_seat = _choose(R, "foundation.layout.lifeline", seats)
    piece = PIECE_OF_TARGET[out["target"]]
    break_at = {"lifeline": life_seat, "remnant": remnant, "key_place": "key_place", "heart": "heart",
                "role": seated[0]["seats"].get(out.get("target_role")), "thin_place": thin_part(parts)}[piece]
    for c in seated:
        if c["prize"]["at"] is None:
            c["prize"]["at"] = {"new": break_at, "lifeline": life_seat}[c["prize"]["kind"]]
    return {"parts": parts, "along": along, "lifeline": life_seat, "remnant": remnant, "break_at": break_at,
            "contests": seated}


def thin_part(parts: dict) -> str:
    return next((p for p, k in parts.items() if k == "land_thin_place"), "along:land_thin_place")


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


def _role_phrase(contest: dict, key: str) -> str:
    return contest["roles"][key]["text"]


def target_phrase(out: dict) -> str:
    spine = rows_by_id("spine")[out["spine"]]
    piece = PIECE_OF_TARGET[out["target"]]
    if piece == "lifeline":
        return rows_by_id("lifeline")[out["lifeline"]]["text"]["name"]
    if piece == "remnant":
        return rows_by_id("ruin_source")[out["ruin"]]["text"]["remnant"]
    if piece == "key_place":
        return spine["text"]["key_place"]
    if piece == "heart":
        return spine["text"]["heart"]
    if piece == "role":
        return _role_phrase(rows_by_id("contest")[out["contests"][0]["id"]], out["target_role"])
    return rows_by_id("palette")["land_thin_place"]["text"]["name"]


def prize_phrase(out: dict, seated: dict) -> str:
    """The main contest's prize in words, from the rows' English fields."""
    spine = rows_by_id("spine")[out["spine"]]["text"]
    contest = rows_by_id("contest")[seated["contest"]]
    kind = seated["prize"]["kind"]
    if kind == "disputed_land":
        side = contest.get("prize_at")
        return f"the land of {contest['roles'][side]['text']}" if side else "the land between them"
    return {"heart": spine["heart"], "key_place": spine["key_place"], "remnant": rows_by_id("ruin_source")[out["ruin"]]["text"]["remnant"],
            "seat": f"the seat of {contest['roles']['a']['text']}", "new": "a new thing both want",
            "thin_place": rows_by_id("palette")["land_thin_place"]["text"]["name"]}.get(kind, "")


def spine_sentence(out: dict) -> str:
    """The spine sentence (build item 18e; docs/p1-threat-first.md): one public sentence from the story pieces alone,
    "<the target> <was struck>, by <the hand>; now <side a> and <side b> fight over <the prize>". A slot that would hold
    texture or nothing is a table fault."""
    move = out["move"]
    hand = (dt.row("antagonists.yaml#hand", move["hand"]) or {}).get("text", {}).get("name")
    act = rows_by_id("action")[out["action"]]
    tense = rows_by_id("time")[out["time"]]["tense"]
    main = out["layout"]["contests"][0]
    contest = rows_by_id("contest")[main["contest"]]
    parts = {"the hand": hand, "the target": target_phrase(out), "the verb": act["forms"][tense],
             "side a": contest["roles"]["a"]["text"], "side b": contest["roles"]["b"]["text"], "the prize": prize_phrase(out, main)}
    empty = [k for k, v in parts.items() if not v]
    if empty or PIECE_OF_TARGET[out["target"]] == "lifeline" or main["prize"]["kind"] == "lifeline":
        raise SystemExit(f"design_foundation: the spine sentence has no {', '.join(empty) or 'story piece'} — a table fault")
    s = f"{parts['the target']} {parts['the verb']}, by {parts['the hand']}; now {parts['side a']} and {parts['side b']} fight over {parts['the prize']}."
    return s[0].upper() + s[1:]


def rendering(out: dict) -> list[dict]:
    """The foundation in English, for the owner's eyes and the writer's: a labelled list built from the rows' own
    English fields (build item 13a; the Turkish five-template sentence is gone). No sentence is assembled: every
    line is `label: the rows' fragments`, and every rolled piece is named."""
    spine = rows_by_id("spine")[out["spine"]]
    palette = rows_by_id("palette")
    ruin = rows_by_id("ruin_source")[out["ruin"]]
    life = rows_by_id("lifeline")[out["lifeline"]]
    contests = rows_by_id("contest")
    act = rows_by_id("action")[out["action"]]
    time = rows_by_id("time")[out["time"]]
    st = spine["text"]
    ends = " / ".join(st["ends"]) if st.get("ends") else st["ends_both"]
    lines = [
        {"label": "The world's shape", "text": f"{st['name']}; heart: {st['heart']}; ends: {ends}; key place: {st['key_place']}"},
        {"label": "The lands", "text": ", ".join(palette[k]["text"]["name"] for k in list(out["palette"]) + list(out["palette_extra"]))},
        {"label": "The past", "text": f"{ruin['text']['what']}; remnant: {ruin['text']['remnant']}"},
        {"label": "The value", "text": life["text"]["name"]},
    ]
    for n, c in enumerate(out["contests"]):
        row = contests[c["id"]]
        sides = f"{_role_phrase(row, 'a')} against {_role_phrase(row, 'b')}"
        rest = "".join(f"; {key}: {_role_phrase(row, key)}" for key in ("third", "fourth") if key in c["roles"])
        lines.append({"label": "The conflict" if n == 0 else "The second conflict", "text": f"{row['text']['name']}: {sides}{rest}"})
    main = contests[out["contests"][0]["id"]]
    scars = ", ".join(rows_by_id("scar")[s]["text"]["name"] for s in out["scars"])
    # a break still coming has left no wound yet: its scars are its first signs
    scar_word = "first signs" if time["id"] == "time_coming" else ("scars" if len(out["scars"]) > 1 else "scar")
    lines.append({"label": "The break", "text": f"{time['text']['name']}: {target_phrase(out)} {act['forms'][time['tense']]}; "
                                                f"{scar_word}: {scars}; stronger for it: {_role_phrase(main, out['winner'])}"})
    return lines


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
        "move": out["move"],
        "spine_sentence": out.get("spine_sentence"),
        "rendering": rendering(out),
    }
