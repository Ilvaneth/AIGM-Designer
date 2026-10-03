"""Variety model of P1: today vs claims (negative filter) vs soft grouping vs hard grouping.
Read-only: imports the skill's scripts, never writes the repository."""
import math, random, sys, collections, itertools
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd, design_arbiter as arb, design_tables as dt, design_dice as dd

# ── entropy capture ───────────────────────────────────────────────────────────
ENT = []          # (label, bits, pool_size)
CUR = {"label": None}
_orig_pick = arb.pick


def _H(ws):
    t = sum(ws)
    return -sum((w / t) * math.log2(w / t) for w in ws if w > 0)


def pick(rng, pool, weights):
    ENT.append((CUR["label"], _H(weights), len(pool)))
    return _orig_pick(rng, pool, weights)


arb.pick = pick
designer.arb.pick = pick
_orig_table = designer.Roller.table


def table(self, label, ref, *a, **k):
    CUR["label"] = ref
    return _orig_table(self, label, ref, *a, **k)


designer.Roller.table = table
_orig_notation = designer.Roller.notation


def notation(self, label, notation, secret=False):
    if notation.startswith("d") and notation[1:].isdigit():
        n = int(notation[1:])
        ENT.append(("dice:" + label.split(".")[0] + "." + label.split(".")[1] if "." in label else "dice:" + label,
                    math.log2(n) if n > 0 else 0, n))
    return _orig_notation(self, label, notation, secret)


designer.Roller.notation = notation

# ── dials ─────────────────────────────────────────────────────────────────────
DIALW = {d: [(r["value"], r.get("weight", 1)) for r in dt.rows("dials.yaml#" + d)]
         for d in ("scale", "tone", "magic", "era", "danger")}
SPAN = {s: int(dt.scale_row(s)["level_span"]) for s in ("short", "standard", "epic")}


def sample_dials(rng, fixed=None):
    d = {}
    for k, vals in DIALW.items():
        vs, ws = zip(*vals)
        d[k] = rng.choices(vs, ws)[0]
    d["content_mix"] = rng.sample(["exploration", "politics", "war", "horror", "mystery"], 3)
    if fixed:
        d.update(fixed)
    d["level_band"] = [1, 1 + SPAN[d["scale"]]]
    return d


def dial_entropy():
    return sum(_H([w for _, w in vals]) for vals in DIALW.values())


# ── usage store (used.json in memory) ────────────────────────────────────────
class Store:
    def __init__(self, intended=False):
        self.births = []           # list of dict ref -> set(row)
        self.pairs = []
        self.intended = intended   # True: avoid only where the header says avoid_used (the plan's intent)

    def usage(self, ref, avoid):
        head = dt.roll_header(ref)
        out = {}
        if self.intended:
            avoid = avoid and bool(head.get("avoid_used"))
        if avoid:
            out["used_elsewhere"] = set().union(*[b.get(ref, set()) for b in self.births]) if self.births else set()
        if head.get("row_wait"):
            n = int(head["row_wait"])
            out["row_wait"] = set().union(*[b.get(ref, set()) for b in self.births[-n:]]) if self.births else set()
        if head.get("family_wait"):
            n = int(head["family_wait"])
            fams = {r["id"]: r.get("family") for r in dt.rows(ref)}
            rows = set().union(*[b.get(ref, set()) for b in self.births[-n:]]) if self.births else set()
            out["family_wait"] = {fams[r] for r in rows if fams.get(r) is not None}
        return out

    def record(self, R):
        b = collections.defaultdict(set)
        for r in R.public + R.secret:
            ref, row = r.get("table"), r.get("row_id")
            if row and ref and ref != "dice" and dt.records_usage(ref):
                b[ref].add(row)
            for key, val in (r.get("used_keys") or {}).items():
                self.pairs.append(val)
        self.births.append(dict(b))


# ── the audit's literal clashes (for measuring the clash rate) ────────────────
CLASH = [("break_rule_by_lottery", "contest_two_heirs"), ("break_rule_by_lottery", "contest_sibling_rulers"),
         ("break_dragons_rule", "contest_two_heirs")]
CLASH += [("break_no_kings_only_guilds", x) for x in ("contest_two_heirs", "contest_empty_throne", "contest_lords_peasants",
                                                       "contest_old_order_reform", "life_binding_marriage")]
CLASH += [("break_iron_is_sacred", x) for x in ("life_iron_coal", "life_famous_steel")]
CLASH += [("break_underground_forbidden", x) for x in ("spine_three_depths", "spine_mountain_within", "life_deep_lake",
                                                        "life_deep_mouth", "life_mushroom_fields", "contest_surface_deep",
                                                        "era=underground")]
CLASH += [("ruin_age_of_mages", "magic=high"), ("break_no_writing", "era=renaissance"),
          ("break_moon_trades", "era=underground"), ("break_night_is_safe", "era=underground")]
CLASH_OF = collections.defaultdict(set)
for a, b in CLASH:
    CLASH_OF[a].add(b)
    CLASH_OF[b].add(a)


def facts(R, dials):
    s = set(R.ctx.rolled)
    s |= {f"{k}={v}" for k, v in dials.items() if isinstance(v, str)}
    return s


def clashes(fs):
    return [(a, b) for a, b in CLASH if a in fs and b in fs]


# ── grouping models ──────────────────────────────────────────────────────────
TROPE = dt.rows("trope-breaks.yaml")
CONTEST_FAMS = sorted({r["family"] for r in dt.rows("foundation.yaml#contest")})


def synthetic_membership(f, seed, headings):
    """Each trope row listed under each heading with probability f (at least one heading)."""
    rng = random.Random(str(seed))
    mem = {}
    for r in TROPE:
        hs = {h for h in headings if rng.random() < f}
        if not hs:
            hs = {rng.choice(headings)}
        mem[r["id"]] = hs
    return mem


class Model:
    """name; question/form/lineage/phenomenon/trope: 'today' | 'soft' | 'hard'; claims: bool."""
    def __init__(self, name, q="soft", form="soft", lineage="soft", rule="hard", trope="none", claims=False,
                 trope_f=0.25, trope_mem_seed=0, soft_x=3.0, trope_headings=("contest",)):
        self.name, self.q, self.form, self.lineage, self.rule, self.trope = name, q, form, lineage, rule, trope
        self.claims, self.soft_x = claims, soft_x
        self.trope_headings = trope_headings
        self.mem = {}
        if trope != "none":
            # one membership table per heading kind
            heads = {"contest": CONTEST_FAMS,
                     "spine": sorted({r["family"] for r in dt.rows("foundation.yaml#spine")}),
                     "lifeline": sorted({r["family"] for r in dt.rows("foundation.yaml#lifeline")}),
                     "era": [v for v, _ in DIALW["era"]]}
            for i, h in enumerate(trope_headings):
                self.mem[h] = synthetic_membership(trope_f, (trope_mem_seed, i), heads[h])


def heading_values(R, dials, out):
    rows = lambda sub: fd.rows_by_id(sub)
    return {"contest": rows("contest")[out["contests"][0]["id"]]["family"],
            "spine": rows("spine")[out["spine"]]["family"],
            "lifeline": rows("lifeline")[out["lifeline"]]["family"],
            "era": dials["era"]}


class Empty(Exception):
    pass


def draw(R, store, label, ref, rows=None, where=None, exclude=None, mult=None, secret=False):
    rows = rows if rows is not None else dt.rows(ref)
    if mult:
        rows = [dict(r, weight=float(r.get("weight", 1)) * mult(r)) for r in rows]
    head = dt.roll_header(ref)
    use = store.usage(ref, True) if store else {}
    CUR["label"] = ref
    try:
        res = arb.arbitrate(ref, rows, R.ctx, exclude=exclude, where=where, usage=use, secret=secret)
    except arb.EmptyPool:
        raise Empty(ref)
    rng = dd.derive(R.master, R.phase, ref, label, R.attempt)
    rec = R._record(label, ref)
    rec.update(arb.pick(rng, res["pool"], res["weights"]))
    if res["usage_fallback"]:
        rec["usage_fallback"] = res["usage_fallback"]
    R._keep(rec, secret)
    return rec


def claims_where(R, dials):
    fs = facts(R, dials)
    return lambda r: not (CLASH_OF.get(r["id"], set()) & fs)


def identity(R, store, dials, out, M):
    """Step 2 as plan item 25 + the review orders it (items 7-10 of the build are not coded yet)."""
    scale = dials["scale"]
    contest_rows = fd.rows_by_id("contest")
    main = contest_rows[out["contests"][0]["id"]]
    hv = heading_values(R, dials, out)
    cw = claims_where(R, dials) if M.claims else (lambda r: True)
    # 1. trope breaks (first roll of step 2), families distinct; the new-taboo scar draws one from the prohibitions
    n_tb = int(dt.roll_header("trope-breaks.yaml")["count_by_scale"][scale])
    breaks, fams = [], set()

    def in_group(r):
        return all(hv[h] in M.mem[h][r["id"]] for h in M.trope_headings)
    for n in range(1, n_tb + 1):
        prohib = (n == 1 and "scar_new_taboo" in out["scars"])
        base = lambda r, prohib=prohib: (r["family"] not in fams) and (r.get("prohibition") or not prohib) and cw(r)
        if M.trope == "hard":
            where = lambda r, base=base: base(r) and in_group(r)
            mult = None
        elif M.trope == "soft":
            where, mult = base, (lambda r: M.soft_x if in_group(r) else 1.0)
        else:
            where, mult = base, None
        rec = draw(R, store, f"break.{n}", "trope-breaks.yaml", where=where, exclude=set(breaks), mult=mult)
        breaks.append(rec["row_id"])
        fams.add(next(r["family"] for r in TROPE if r["id"] == rec["row_id"]))
        draw(R, store, f"break_tie.{n}", "trope-breaks.yaml#tie", exclude={R.row(f"break_tie.{k}") for k in range(1, n)})
    # 2. people
    fs = set(R.ctx.rolled)

    def lineage_in(r):
        return any(arb.holds(w.get("when"), R.ctx) for w in r.get("weight_by") or [])
    lin_rows = dt.rows("signatures.yaml#people_lineage")
    if M.lineage == "hard":
        grp = [r for r in lin_rows if lineage_in(r)]
        lin_rows = [dict(r, weight_by=[]) for r in (grp or lin_rows)]
    elif M.lineage == "today_uniform":
        lin_rows = [dict(r, weight_by=[]) for r in lin_rows]
    draw(R, store, "sig_people.lineage", "signatures.yaml#people_lineage", rows=lin_rows)
    draw(R, store, "sig_people.visible", "signatures.yaml#people_trait", where=lambda r: r["kind"] == "visible")
    draw(R, store, "sig_people.behaving", "signatures.yaml#people_trait", where=lambda r: r["kind"] == "behaving")
    draw(R, store, "sig_people.attitude", "signatures.yaml#people_attitude")
    # 3. institution: a role of the main contest with an archetype hint
    roles = [k for k in out["contests"][0]["roles"] if (main["roles"].get(k) or {}).get("hint")]
    role = roles[int(R.notation("sig_institution.role", f"d{len(roles)}")["raw"]) - 1]
    hint = main["roles"][role]["hint"]
    form_rows = dt.rows("signatures.yaml#institution_form")
    if M.form == "hard":
        form_rows = [r for r in form_rows if hint in (r.get("hints") or [])] or form_rows
        mult = None
    elif M.form == "soft":
        mult = lambda r: 3.0 if hint in (r.get("hints") or []) else 1.0
    else:
        mult = None
    draw(R, store, "sig_institution.form", "signatures.yaml#institution_form", rows=form_rows, mult=mult)
    draw(R, store, "sig_institution.practice", "signatures.yaml#institution_practice")
    draw(R, store, "sig_institution.sign", "signatures.yaml#institution_sign")
    draw(R, store, "sig_institution.power", "signatures.yaml#institution_power")
    # 4. phenomenon: the rule's pool is the ruin's olgu_families (or family 8 with the magic-rule scar)
    ruin = fd.rows_by_id("ruin_source")[out["ruin"]]
    olgu = {"born_of_break"} if "scar_magic_rule_changed" in out["scars"] else set(ruin["olgu_families"])
    if M.rule == "hard":
        draw(R, store, "sig_phenomenon.rule", "signatures.yaml#phenomenon_rule", where=lambda r: r["family"] in olgu)
    elif M.rule == "soft":
        draw(R, store, "sig_phenomenon.rule", "signatures.yaml#phenomenon_rule",
             mult=lambda r: 3.0 if r["family"] in olgu else 1.0)
    else:
        draw(R, store, "sig_phenomenon.rule", "signatures.yaml#phenomenon_rule")
    draw(R, store, "sig_phenomenon.sign", "signatures.yaml#phenomenon_sign")
    draw(R, store, "sig_phenomenon.limit", "signatures.yaml#phenomenon_limit")
    draw(R, store, "sig_phenomenon.user", "signatures.yaml#phenomenon_user")
    # 5. the question: one per contest, weighted x3 by the contest's family
    qs = []
    for n, c in enumerate(out["contests"], 1):
        fam = contest_rows[c["id"]]["family"]
        ingrp = lambda r, fam=fam: fam in (r.get("families") or [])
        if M.q == "hard":
            rec = draw(R, store, f"question.{n}", "tensions.yaml", where=ingrp, exclude=set(qs))
        elif M.q == "soft":
            rec = draw(R, store, f"question.{n}", "tensions.yaml", exclude=set(qs), mult=lambda r, g=ingrp: 3.0 if g(r) else 1.0)
        else:
            rec = draw(R, store, f"question.{n}", "tensions.yaml", exclude=set(qs))
        qs.append(rec["row_id"])
    # 6-7. secret and villain (counts only, never printed)
    for sub in ("archetype", "twist", "trail"):
        draw(R, store, f"secret_{sub}", f"secrets.yaml#{sub}", secret=True)
    for sub in ("visibility", "villain_shape", "origin"):
        draw(R, store, f"villain_{sub}", f"antagonists.yaml#{sub}", secret=True)
    # 8. names
    nf = []
    for n in range(1, int(dt.load("naming.yaml")["roll"]["count_by_scale"][scale]) + 1):
        nf.append(draw(R, store, f"naming_family.{n}", "naming.yaml#family", exclude=set(nf))["row_id"])
    return hv


def birth(seed, dials, store, M):
    R = designer.Roller.in_memory(seed, dials)
    R._usage = (lambda ref, avoid: store.usage(ref, avoid)) if store else (lambda ref, avoid: {})
    start = len(ENT)
    pairs = set(store.pairs) if store else set()
    try:
        out = fd.roll(R, dials, pairs)
    except SystemExit as e:
        return None, None, "foundation_empty", R
    mid = len(ENT)
    try:
        hv = identity(R, store, dials, out, M)
    except (Empty, SystemExit) as e:
        return out, None, f"identity_empty:{e}", R
    return out, hv, None, R


def bits(start, stop=None):
    return sum(b for _, b, _ in ENT[start:stop])
