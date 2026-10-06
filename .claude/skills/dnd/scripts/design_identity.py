#!/usr/bin/env python3
"""
design_identity.py — P1's second step, the identity's rolls, made by script with no model (plan item 25, step 2 and
"Review of the whole P1"; docs/p1-build-10.md; the rulings of docs/p1-tags.md).

`roll(R, dials, foundation)` makes the public identity's draws through a designer Roller (every draw passes
design_arbiter against everything rolled before it), on the foundation step 1 built, in this order:

1. the trope break(s): the scale's count, from different families. With the "new prohibition" scar the first is
   drawn from the prohibition rows and tied to the break (the one exception to "the break's tie never stands with a
   break still coming"). Every other tie: a fit of the row's own on a rolled lifeline, contest or ruin source sets it
   (the largest weight, then that order); otherwise it is rolled. A row rolled beside one its `merges_with` names is
   recorded as merged; `merge_role_hints` rewrites the contest's role hints for everything after. A world state (a
   row whose layer is story, build item 18b) is drawn only where one of its `joins` holds, records the join, and
   is never tied to the lifeline; a join to the threat is a requirement the threat's roll honours (18c), kept in
   dm-only;
2. the people: home (the lifeline, or the "a new people" scar), the role (the main contest's seated people's role
   the break did not destroy), the lineage (forced by the role, or rolled with the role's weights and, under
   "lineage homes are inverted", the palette weights inverted), a visible and a behaving trait, the attitude;
3. the institution: one of the main contest's seated roles with an archetype hint, that the people did not take and
   the break did not destroy (the foundation never destroys the last one); the practice, the form (the practice's
   own when it names one, always a form of that archetype) and the power under that archetype; the sign rolled
   freely;
4. the phenomenon: the rule from the ruin source's families (from the break's family alone with the "a rule of
   magic changed" scar), the sign, the limit, and the user by the rule's kind;
5. the question(s): one per contest, of that contest's family.

`build(out)` is `design.json#identity`: public and stamped like `#foundation`. An override is data here: the rolled
rows' overrides are collected, none is applied.

`roll_secret(R, dials, foundation, identity)` makes the secret draws after the public ones (build item 10b), every
one of them secret:

6. the secret: archetype, chooser (with `chooser_contest_role` a further roll picks which seated role), twist, trail;
7. the villain: visibility, shape, origin (a shape and origin pair another campaign drew waits as usage and is
   written, hashed, at approve; the two tables' rows may otherwise repeat), the tie to the break (`bond_caused_it`,
   not rolled, exactly when the chooser is the villain) and the pole: role a's or role b's side of the main
   contest's question, with the darkness dial's `majority_pole` beside it. A shape whose row says `same_figure_with`
   a rolled public row (build item 16c) is that row's public figure exactly when the visibility is the one the row
   gives: then the shape is not rolled and the pole is that role's; with any other visibility the shape is barred.

Its return goes to dm-only alone (`dice-log.json#identity`); design.json and the card never hold it.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_arbiter as arb  # noqa: E402
import design_dice as dd  # noqa: E402
import design_foundation as fd  # noqa: E402
import design_tables as dt  # noqa: E402

BREAKS = "trope-breaks.yaml"
TIES = "trope-breaks.yaml#tie"
QUESTIONS = "tensions.yaml"
S = "signatures.yaml#"
TIE_OF_PIECE = (("lifeline", "tie_lifeline"), ("contest", "tie_contest"), ("ruin_source", "tie_ruin_source"))
USER_OF_KIND = {"spell": "user_casters", "self": "user_no_one"}
HEADINGS = ("state", "religious", "martial", "guild", "trade", "scholarly", "criminal", "resistance")
SECRETS = "secrets.yaml#"
VILLAIN = "antagonists.yaml#"
VILLAIN_PAIR_KEY = "antagonists.yaml#shape_origin_pair"     # used.json: shape|origin, hashed, never repeated


def named(cond) -> list[str]:
    """The row ids a condition names."""
    out: list[str] = []
    if isinstance(cond, list):
        for c in cond:
            out += named(c)
    elif isinstance(cond, dict):
        for key in ("any_of", "all_of", "none_of"):
            out += list(cond.get(key) or [])
        for key in ("all", "any"):
            out += named(cond.get(key) or [])
    return out


def is_world_state(row: dict) -> bool:
    """A trope break that says who rules or what dominates the world (build item 18b): layer story, with joins."""
    return dt.layer(BREAKS, row["id"]) == "story"


def joins_of(row: dict, foundation: dict, scale: str, threat: dict | None = None) -> list[dict]:
    """The joins of a world state that hold on what is rolled, in the row's order: each `{piece, how, ...}` with the
    piece's id where one is rolled. Every join is to a public piece (the 18c-1 audit): a join to the threat holds only
    when the villain itself is public (its visibility known) and the rolled threat meets the requirement; with no
    threat (a legacy roll) it does not hold. A join to a hand reads the move's public hand."""
    contests = foundation["contests"]
    prizes = foundation["layout"]["contests"]
    kinds = set(foundation["palette"]) | set(foundation["palette_extra"])
    ruin = fd.rows_by_id("ruin_source")[foundation["ruin_source"]]
    main_row = fd.rows_by_id("contest")[contests[0]["id"]]
    gone = destroyed_role(foundation)
    out = []
    for j in row.get("joins") or []:
        if j.get("scales") and scale not in j["scales"]:
            continue
        base = {"piece": j["piece"], "how": j["how"]}
        if j.get("always"):
            out.append(dict(base, contest=contests[0]["id"]))
        elif j.get("any_of"):
            hit = next((c["id"] for c in contests if c["id"] in j["any_of"]), None)
            if hit:
                out.append(dict(base, contest=hit))
        elif j.get("prize"):
            hit = next((c["contest"] for c in prizes if c["prize"]["kind"] == j["prize"]), None)
            if hit:
                out.append(dict(base, contest=hit))
        elif j.get("people_side"):
            role = next((k for k in contests[0]["roles"] if (main_row["roles"].get(k) or {}).get("people_role") and k != gone), None)
            if role:
                out.append(dict(base, contest=contests[0]["id"], role=role))
        elif j.get("palette"):
            if j["palette"] in kinds:
                out.append(dict(base, kind=j["palette"]))
        elif j.get("ruins"):
            if ruin["id"] in j["ruins"]:
                out.append(dict(base, ruin_source=ruin["id"]))
        elif j.get("hand"):
            # the move's public hand (build item 18c): a dragon hand for the dragons, a trading or outside hand for the moon
            hrow = dt.row("antagonists.yaml#hand", str((foundation.get("move") or {}).get("hand") or ""))
            if hrow and (hrow.get("moon") if j["hand"] == "moon" else j["hand"] in (hrow.get("families") or [])):
                out.append(dict(base, hand=hrow["id"]))
        elif j.get("ruin_family"):
            families = j["ruin_family"] if isinstance(j["ruin_family"], list) else [j["ruin_family"]]
            if ruin["family"] in families:
                out.append(dict(base, ruin_source=ruin["id"]))
        elif j.get("threat"):
            import design_threat as dth
            if threat is not None and threat["visibility"] in dth.PUBLIC_VISIBILITY and threat_holds(j["threat"], threat):
                out.append(dict(base, threat=dict(j["threat"])))
    return out


def threat_holds(req: dict, threat: dict) -> bool:
    """A world state's requirement on the threat, judged on the rolled threat."""
    if req.get("villain"):
        return True
    if req.get("family"):
        return threat["family"] == f"family_{req['family']}"
    if req.get("creature"):
        return threat["creature_type"] == req["creature"]
    return False


def destroyed_role(foundation: dict) -> str | None:
    """The main contest's role the break destroyed (the struck role under an action that destroys a role)."""
    brk = foundation["break"]
    if fd.PIECE_OF_TARGET[brk["target"]] != "role":
        return None
    act = fd.rows_by_id("action")[brk["action"]]
    return brk.get("target_role") if "role" in (act.get("destroys") or []) else None


def fit_tie(row: dict, R, pieces: dict) -> tuple[str, str] | None:
    """(tie id, reason) when one of the trope row's own weights holds on a rolled lifeline, contest or ruin source
    row: the largest weight wins, then the order lifeline, contest, ruin source. A world state's tie is never the
    lifeline (build item 18b: the tie of a world state fills a story slot)."""
    best = None
    for rule in row.get("weight_by") or []:
        x = float(rule.get("x", 1))
        if x <= 1 or not arb.holds(rule.get("when"), R.ctx):
            continue
        ids = set(named(rule.get("when")))
        for order, (piece, tie) in enumerate(TIE_OF_PIECE):
            if piece == "lifeline" and is_world_state(row):
                continue
            hit = sorted(ids & set(pieces[piece]))
            if hit and (best is None or (-x, order) < best[0]):
                best = ((-x, order), tie, f"{row['id']} fits {hit[0]} (×{rule.get('x')})")
    return (best[1], best[2]) if best else None


def lineage_weigh(role_row: dict, inverted: bool):
    """The people's lineage weights: the role's `lineage_weight` on the rows' own (or, under "lineage homes are
    inverted", the inverted homes); None when neither applies (the rows' own weights stand)."""
    role_weight = role_row.get("lineage_weight") or {}
    if not (inverted or role_weight):
        return None

    def weigh(r, ctx):
        return (inverted_weight(r, ctx) if inverted else arb.weight_of(r, ctx)) * float(role_weight.get(r["id"], 1))
    return weigh


def inverted_weight(row: dict, ctx) -> float:
    """"Lineage homes are inverted": a weight whose condition names palette kinds applies when it does not hold."""
    w = float(row.get("weight", 1))
    for rule in row.get("weight_by") or []:
        ids = named(rule.get("when"))
        palette_only = bool(ids) and all(i.startswith("land_") for i in ids) and not (rule.get("when") or {}).get("dial")
        if arb.holds(rule.get("when"), ctx) != palette_only:
            w *= float(rule.get("x", 1))
    return w


def roll(R, dials: dict, foundation: dict) -> dict:
    """Every public step-2 draw through the Roller; returns what `build` needs (the records are on R)."""
    scale = dials["scale"]
    sc = dt.scale_row(scale)
    brk = foundation["break"]
    scars = set(brk["scars"])
    contests = foundation["contests"]
    contest_rows = fd.rows_by_id("contest")
    main, main_row = contests[0], contest_rows[contests[0]["id"]]
    seated = list(main["roles"])
    destroyed = destroyed_role(foundation)
    out: dict = {}

    # 1. the trope breaks, their ties and merges
    break_rows = {r["id"]: r for r in dt.rows(BREAKS)}
    pieces = {"lifeline": [foundation["lifeline"]["id"]], "contest": [c["id"] for c in contests],
              "ruin_source": [foundation["ruin_source"]]}
    taboo = "scar_new_taboo" in scars
    hints = {c["id"]: {k: (contest_rows[c["id"]]["roles"].get(k) or {}).get("hint") for k in c["roles"]} for c in contests}
    breaks: list[dict] = []
    threat = getattr(R, "threat", None)
    joinable = lambda r: not is_world_state(r) or bool(joins_of(r, foundation, scale, threat))
    for n in range(1, int(sc["trope_breaks"]) + 1):
        drawn = {b["id"] for b in breaks}
        if n == 1 and taboo:
            rid = R.table(f"break.{n}", BREAKS, exclude=drawn, where=lambda r: bool(r.get("prohibition")) and joinable(r),
                          why="the new-prohibition scar draws a prohibition")["row_id"]
            R.forced(f"break_tie.{n}", TIES, "tie_break", "scar_new_taboo: the prohibition is the break's own", exempt={"time_coming"})
            tie, how = "tie_break", "scar"
        else:
            rid = R.table(f"break.{n}", BREAKS, exclude=drawn, where=joinable, why="a world state joins a story piece")["row_id"]
            fit = fit_tie(break_rows[rid], R, pieces)
            if fit:
                R.forced(f"break_tie.{n}", TIES, fit[0], fit[1])
                tie, how = fit[0], "fit"
            else:
                tie, how = R.table(f"break_tie.{n}", TIES, avoid=False,
                                   slot="world_state_tie" if is_world_state(break_rows[rid]) else None)["row_id"], "rolled"
        row = break_rows[rid]
        join = None
        if is_world_state(row):
            join = joins_of(row, foundation, scale, threat)[0]       # the first that holds, in the row's order
            ties = {t["id"]: t for t in dt.rows(TIES)}
            errs = arb.slot_errors([("world_state_tie", ties[tie]["piece"]), ("world_state_tie", join["piece"])])
            if errs:
                raise SystemExit(f"design_identity: {rid}: " + "; ".join(errs) + " — a table fault")
            # every join is public (the 18c-1 audit): a join to the villain holds only when the villain is known
        merged = [{"with": other, "note": note} for other, note in (row.get("merges_with") or {}).items() if R.ctx.has(other)]
        for cid, change in (row.get("merge_role_hints") or {}).items():
            if cid in hints:
                hints[cid].update({k: v for k, v in change.items() if k in hints[cid]})
        rec = {"id": rid, "tie": tie, "tie_by": how, "merges": merged}
        if join is not None:
            rec["join"] = join
        breaks.append(rec)
    out["trope_breaks"] = breaks

    out["role_hints"] = hints
    break_ids = {b["id"] for b in breaks}

    # 2. the people
    people_role = next((k for k in seated if (main_row["roles"].get(k) or {}).get("people_role") and k != destroyed), None)
    role_row = main_row["roles"].get(people_role) or {}
    lineage_ref = S + "people_lineage"
    if role_row.get("lineage_forced"):
        lineage = R.forced("people.lineage", lineage_ref, role_row["lineage_forced"], f"the people's role {people_role} of {main['id']}")["row_id"]
        lineage_by = "role"
    else:
        weigh = lineage_weigh(role_row, "break_lineage_homes_inverted" in break_ids)
        lineage = R.table("people.lineage", lineage_ref, weigh=weigh)["row_id"]
        lineage_by = "rolled"
    trait_ref = S + "people_trait"
    visible = R.table("people.trait.visible", trait_ref, where=lambda r: r["kind"] == "visible", why="a visible trait")["row_id"]
    winner_ok = people_role is None or people_role == brk["winner"]
    behaving = R.table("people.trait.behaving", trait_ref,
                       where=lambda r: r["kind"] == "behaving" and (r["id"] != "trait_won_by_the_break" or winner_ok),
                       why="a behaving trait; the break's winners only as the foundation's winner")["row_id"]
    attitude = R.table("people.attitude", S + "people_attitude")["row_id"]
    out["people"] = {"home": "scar_new_people" if "scar_new_people" in scars else "lifeline", "role": people_role,
                     "lineage": lineage, "lineage_by": lineage_by, "traits": {"visible": visible, "behaving": behaving},
                     "attitude": attitude}

    # 3. the institution
    main_hints = hints[main["id"]]
    homes = [k for k in seated if main_hints.get(k) and k != people_role and k != destroyed]
    if not homes:        # the foundation never destroys the last such role (design_foundation.institution_homes)
        raise SystemExit(f"design_identity: no seated role of {main['id']} can house the institution — a table fault")
    role = fd._choose(R, "institution.role", homes)
    archetype = main_hints[role]

    def under(r):
        return archetype in (r.get("hints") or [])
    practice = R.table("institution.practice", S + "institution_practice", where=under, why="the role's archetype")["row_id"]
    own_form = dt.row(S + "institution_practice", practice).get("form")
    if own_form:
        form = R.forced("institution.form", S + "institution_form", own_form, f"{practice} names its form")["row_id"]
    else:
        form = R.table("institution.form", S + "institution_form", where=under, why="the role's archetype")["row_id"]
    power = R.table("institution.power", S + "institution_power", where=under, why="the role's archetype")["row_id"]
    sign = R.table("institution.sign", S + "institution_sign")["row_id"]
    out["institution"] = {"role": role, "archetype": archetype, "form": form, "form_by": "practice" if own_form else "rolled",
                          "practice": practice, "sign": sign, "power": power}

    # 4. the phenomenon
    ruin = fd.rows_by_id("ruin_source")[foundation["ruin_source"]]
    changed = "scar_magic_rule_changed" in scars
    families = ["born_of_break"] if changed else list(ruin["olgu_families"])
    rule_id = R.table("phenomenon.rule", S + "phenomenon_rule", where=lambda r: r["family"] in families,
                      why="the break's rule family" if changed else "the ruin source's rule families")["row_id"]
    rule = dt.row(S + "phenomenon_rule", rule_id)
    psign = R.table("phenomenon.sign", S + "phenomenon_sign")["row_id"]
    limit = R.table("phenomenon.limit", S + "phenomenon_limit")["row_id"]
    user_ref = S + "phenomenon_user"
    if rule["kind"] in USER_OF_KIND:
        user = R.forced("phenomenon.user", user_ref, USER_OF_KIND[rule["kind"]], f"a rule of kind {rule['kind']}")["row_id"]
    else:
        allowed = set(rule.get("users") or [])
        user = R.table("phenomenon.user", user_ref,
                       where=lambda r: (r["id"] in allowed) if allowed else r["id"] != "user_no_one",
                       why="the rule's own users" if allowed else "a usable rule has a user")["row_id"]
    out["phenomenon"] = {"home": "break" if changed else "ruin_source", "rule": rule_id, "kind": rule["kind"],
                         "sign": psign, "limit": limit, "user": user}

    # 5. the question(s): one per contest, of the contest's family
    questions: list[dict] = []
    for n, c in enumerate(contests, 1):
        fam = contest_rows[c["id"]]["family"]
        qid = R.table(f"tension.{n}", QUESTIONS, exclude={q["id"] for q in questions},
                      where=lambda r, fam=fam: fam in (r.get("families") or []), why="the contest's family")["row_id"]
        questions.append({"contest": c["id"], "family": fam, "id": qid})
    out["questions"] = questions
    return out


def villain_in_context(ctx) -> bool:
    """Did an earlier phase roll the villain's shape? (P1 does since build item 10b; a legacy birth's P4 still rolls
    visibility, shape and origin itself.)"""
    return any(ctx.has(r["id"]) for r in dt.rows(VILLAIN + "villain_shape"))


def roll_secret(R, dials: dict, foundation: dict, identity: dict, used_pairs: set | None = None) -> dict:
    """The secret and the villain: every draw secret, through the arbiter against everything rolled before it."""
    if used_pairs is None:
        used_pairs = dd.used_values(R.campaign, VILLAIN_PAIR_KEY) if R.campaign else set()
    main = foundation["contests"][0]

    # 6. the secret (build item 18c: the chooser is no longer rolled; the villain always chose)
    archetype = R.table("secret_archetype", SECRETS + "archetype", secret=True)["row_id"]
    chooser, chooser_role = "chooser_the_villain", None
    twist = R.table("secret_twist", SECRETS + "twist", secret=True)["row_id"]
    trail = R.table("secret_trail", SECRETS + "trail", secret=True)["row_id"]

    # 7. the villain: its visibility, shape and origin come from the threat (design_threat.py, rolled before the move);
    #    the tie to the break is retired (the move is always the villain's; 18c-2 rolls the move's state)
    threat = R.threat
    visibility, shape, origin = threat["visibility"], threat["shape"], threat["origin"]
    figure = threat.get("public_figure")
    tie = None
    if figure and figure["main"]:            # the public figure carries its own role's pole
        side = figure["role"]
        rec = R._record("bbeg_pole", None)
        rec.update({"notation": "fixed", "raw": None, "value": side, "derived_from": "the villain is that role's public figure"})
        R._keep(rec, True)
    else:
        side = ("a", "b")[int(R.notation("bbeg_pole", "d2", secret=True)["raw"]) - 1]
    tone = dt.dial_row("tone", dials.get("tone")) or {}
    return {"secret": {"archetype": archetype, "chooser": chooser, "chooser_role": chooser_role, "twist": twist, "trail": trail},
            "villain": {"visibility": visibility, "shape": shape, "origin": origin, "tie": tie,
                        "pole": {"question": identity["questions"][0]["id"], "contest": main["id"], "role": side},
                        "public_figure": {"contest": figure["contest"], "role": figure["role"]} if figure else None,
                        "majority_pole": (tone.get("effects") or {}).get("majority_pole")}}


def overrides_of(row_ids) -> list[dict]:
    """The overrides the rolled rows carry, as data: `{row, default, to}`; none is applied here."""
    index = {r["id"]: r for name in dt.list_tables() for lst in dt.all_row_lists(dt.load(name)).values() for r in lst}
    out = []
    for rid in row_ids:
        ov = (index.get(rid) or {}).get("overrides")
        for o in ov if isinstance(ov, list) else []:
            out.append(dict({"row": rid}, **o))
    return out


def build(out: dict, row_ids) -> dict:
    """The identity as design.json keeps it: public, stamped."""
    return {"stamped": True, "trope_breaks": out["trope_breaks"], "role_hints": out["role_hints"], "people": out["people"],
            "institution": out["institution"], "phenomenon": out["phenomenon"], "questions": out["questions"],
            "overrides": overrides_of(row_ids)}


def line(identity: dict) -> str:
    """One line for the preroll's printout."""
    p, i, ph = identity["people"], identity["institution"], identity["phenomenon"]
    return (f"breaks {', '.join(b['id'] + ' (' + b['tie'] + ')' for b in identity['trope_breaks'])}; "
            f"people {p['lineage']} [{p['traits']['visible']}, {p['traits']['behaving']}] role {p['role'] or '-'}; "
            f"institution {i['archetype']} on role {i['role'] or '-'}: {i['form']}, {i['practice']}; "
            f"phenomenon {ph['rule']} ({ph['kind']}, {ph['user']}); "
            f"questions {', '.join(q['id'] for q in identity['questions'])}")
