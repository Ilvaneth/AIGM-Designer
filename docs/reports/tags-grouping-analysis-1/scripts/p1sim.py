"""Shared P1 simulator: foundation (real code) + an approximation of the identity rolls (item 10 not built yet)."""
import sys, random, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd, design_tables as dt, design_arbiter as arb

SPAN = {"short": 4, "standard": 11, "epic": 19}
def weighted(rng, sub):
    rows = dt.rows("dials.yaml#" + sub)
    return rng.choices([r["value"] for r in rows], [r.get("weight", 1) for r in rows])[0]

def sample_dials(i):
    rng = random.Random(f"DIALS-{i}")
    scale = weighted(rng, "scale")
    start = rng.choice([1, 1, 1, 3, 5])
    mix = rng.sample(["exploration", "politics", "war", "horror", "mystery"], 3)
    return {"scale": scale, "magic": weighted(rng, "magic"), "era": weighted(rng, "era"), "tone": weighted(rng, "tone"),
            "danger": weighted(rng, "danger"), "content_mix": mix, "level_band": [start, min(20, start + SPAN[scale])]}

TB = "trope-breaks.yaml"
def identity(R, d, out, pool_log=None):
    head = dt.roll_header(TB)
    n = int(head["count_by_scale"][d["scale"]])
    fams, ids = [], []
    tb_rows = {r["id"]: r for r in dt.rows(TB)}
    for k in range(1, n + 1):
        if pool_log is not None:
            res = arb.arbitrate(TB, dt.rows(TB), R.ctx, exclude=set(ids), where=lambda r: r["family"] not in fams, usage=R._usage(TB, True))
            pool_log.append(len(res["pool"]))
        rid = R.table(f"break.{k}", TB, exclude=set(ids), where=lambda r: r["family"] not in fams, why="another family")["row_id"]
        ids.append(rid); fams.append(tb_rows[rid]["family"])
        R.table(f"break.{k}.tie", TB + "#tie", avoid=False)
    for k in range(len(out["contests"])):
        R.table(f"tension.{k+1}", "tensions.yaml", exclude={R.row(f"tension.{j+1}") for j in range(k)})
    S = "signatures.yaml#"
    R.table("sig.lineage", S + "people_lineage", avoid=False)
    R.table("sig.trait.v", S + "people_trait", where=lambda r: r.get("kind") == "visible", why="visible")
    R.table("sig.trait.b", S + "people_trait", where=lambda r: r.get("kind") == "behaving", why="behaving")
    R.table("sig.attitude", S + "people_attitude", avoid=False)
    R.table("sig.form", S + "institution_form", avoid=False)
    R.table("sig.practice", S + "institution_practice")
    R.table("sig.isign", S + "institution_sign", avoid=False)
    R.table("sig.power", S + "institution_power", avoid=False)
    ruin = fd.rows_by_id("ruin_source")[out["ruin"]]
    fams_ok = ["born_of_break"] if "scar_magic_rule_changed" in out["scars"] else list(ruin.get("olgu_families") or [])
    R.table("sig.rule", S + "phenomenon_rule", where=lambda r: r["family"] in fams_ok, why="the ruin's families")
    R.table("sig.psign", S + "phenomenon_sign", avoid=False)
    R.table("sig.limit", S + "phenomenon_limit", avoid=False)
    R.table("sig.user", S + "phenomenon_user", avoid=False)

def birth(i, d=None, usage_fn=None, pool_log=None):
    d = d or sample_dials(i)
    R = designer.Roller.in_memory(f"SIM-{i}", d)
    if usage_fn:
        R._usage = usage_fn
    out = fd.roll(R, d)
    identity(R, d, out, pool_log)
    return d, R, out

def rolled(R):
    return {r["row_id"] for r in R.public + R.secret if r.get("row_id")}

# audited pairs: (a, b) where a/b is a row id or "dial:<name>=<value>"
AUDIT = [
 ("break_rule_by_lottery", "contest_two_heirs"), ("break_rule_by_lottery", "contest_sibling_rulers"),
 ("break_no_kings_only_guilds", "contest_two_heirs"), ("break_no_kings_only_guilds", "contest_empty_throne"),
 ("break_no_kings_only_guilds", "contest_lords_peasants"), ("break_no_kings_only_guilds", "contest_old_order_reform"),
 ("break_no_kings_only_guilds", "life_binding_marriage"),
 ("break_iron_is_sacred", "life_iron_coal"), ("break_iron_is_sacred", "life_famous_steel"),
 ("break_underground_forbidden", "dial:era=underground"), ("break_underground_forbidden", "spine_three_depths"),
 ("break_underground_forbidden", "spine_mountain_within"), ("break_underground_forbidden", "life_deep_lake"),
 ("break_underground_forbidden", "life_deep_mouth"), ("break_underground_forbidden", "life_mushroom_fields"),
 ("break_underground_forbidden", "contest_surface_deep"),
 ("dial:magic=high", "ruin_age_of_mages"), ("dial:era=renaissance", "break_no_writing"),
 ("dial:era=underground", "break_moon_trades"), ("dial:era=underground", "break_night_is_safe"),
 ("break_dragons_rule", "contest_two_heirs"),
]
def has(tok, ids, d):
    if tok.startswith("dial:"):
        k, v = tok[5:].split("=")
        return d.get(k) == v
    return tok in ids
def audit_hits(ids, d):
    return [(a, b) for a, b in AUDIT if has(a, ids, d) and has(b, ids, d)]
