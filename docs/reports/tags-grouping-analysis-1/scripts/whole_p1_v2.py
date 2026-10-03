"""Whole-P1 measurement on the REAL step-2 rolls (after build item 10; 2026-10-03). The first two runs
(whole_p1.py) used p1sim's approximation of the identity; this one calls design_foundation and design_identity
as designer.preroll_p1 does, and counts the same things the owner's review ruled out. Model-free scratch script."""
import sys, os, tempfile, collections
sys.stdout.reconfigure(encoding="utf-8")
os.environ["DESIGN_USED_PATH"] = os.path.join(tempfile.gettempdir(), "whole_v2_used.json")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1sim
from p1sim import dt, fd, designer, arb
import design_identity as di

S = "signatures.yaml#"
life = {r["id"]: r for r in dt.rows("foundation.yaml#lifeline")}
contest = {r["id"]: r for r in dt.rows("foundation.yaml#contest")}
tens = {r["id"]: r for r in dt.rows("tensions.yaml")}
practice = {r["id"]: r for r in dt.rows(S + "institution_practice")}
form = {r["id"]: r for r in dt.rows(S + "institution_form")}
power = {r["id"]: r for r in dt.rows(S + "institution_power")}
rule = {r["id"]: r for r in dt.rows(S + "phenomenon_rule")}
FORCED = {k: (v["roles"]["b"] or {}).get("lineage_forced") for k, v in contest.items() if (v["roles"].get("b") or {}).get("lineage_forced")}


def prize_lists():
    """The eight prize contests' lifeline lists, read from the tables' own requirements."""
    out = {}
    for cid, row in contest.items():
        ids = arb._condition_ids(row.get("requires"))
        lifes = {x for x in ids if x.startswith("life_")}
        if lifes:
            out[cid] = lifes
    return out


NEED = prize_lists()


def check(i):
    d = p1sim.sample_dials(i)
    R = designer.Roller.in_memory(f"SIM-{i}", d)
    out = fd.roll(R, d)
    foundation = fd.build(out, d["level_band"])
    ident = di.roll(R, d, foundation)
    identity = di.build(ident, [r["row_id"] for r in R.public if r.get("row_id")])
    sec = di.roll_secret(R, d, foundation, identity, used_pairs=set())
    recs = R.public + R.secret
    ids = [r["row_id"] for r in recs if r.get("row_id")]
    exempt = set()
    for r in recs:
        for x in r.get("conflict_exempt") or []:
            exempt.add(frozenset((r.get("row_id"), x)))
    hit = collections.defaultdict(list)
    pairs = [p for p in arb.conflicting_pairs(ids, tokens=set(R.ctx.tokens)) if frozenset(p) not in exempt]
    if pairs:
        hit["clash"].append("a conflicting pair")
    cons = [c["id"] for c in out["contests"]]
    lf = out["lifeline"]
    if any(k in NEED and lf not in NEED[k] for k in cons):
        hit["heading"].append("prize x lifeline")
    ppl, inst, ph = ident["people"], ident["institution"], ident["phenomenon"]
    if ppl["role"] == "b" and cons[0] in FORCED and ppl["lineage"] != FORCED[cons[0]]:
        hit["heading"].append("the people's role x lineage")
    arche = inst["archetype"]
    if inst["role"] is None:
        hit["heading"].append("the institution has no role")
    if arche not in practice[inst["practice"]]["hints"]:
        hit["institution"].append("practice x archetype")
    if arche not in form[inst["form"]]["hints"]:
        hit["institution"].append("form x archetype")
    if arche not in power[inst["power"]]["hints"]:
        hit["institution"].append("power x archetype")
    kind = rule[ph["rule"]]["kind"]
    want = {"spell": "user_casters", "self": "user_no_one"}.get(kind)
    if (want and ph["user"] != want) or (kind == "usable" and ph["user"] == "user_no_one"):
        hit["user"].append("user x rule kind")
    for q in ident["questions"]:
        if contest[q["contest"]]["family"] not in tens[q["id"]]["families"]:
            hit["question"].append("question outside the contest's family")
    v, s = sec["villain"], sec["secret"]
    if (s["chooser"] == "chooser_the_villain") != (v["tie"] == "bond_caused_it"):
        hit["secret"].append("chooser and tie disagree")
    return hit


N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
tier, why, anyhit = collections.Counter(), collections.Counter(), 0
for i in range(N):
    hit = check(i)
    anyhit += bool(any(hit.values()))
    for k, v in hit.items():
        tier[k] += bool(v)
        for w in set(v):
            why[(k, w)] += 1


def pc(n):
    return f"{100 * n / N:.1f}%"


print("births", N, "| the real foundation, identity and secret rolls")
for k, label in (("clash", "1 a conflicting pair (rows and tokens, public and secret)"),
                 ("heading", "2 outside its heading (prize, the people's role, a roleless institution)"),
                 ("institution", "3 the institution against its role's archetype (practice, form, power)"),
                 ("user", "4a a user against the rule's kind"), ("question", "4b a question outside its contest's family"),
                 ("secret", "5 the chooser and the villain's tie disagree")):
    print(label + ":", tier[k], pc(tier[k]))
print("any of them:", anyhit, pc(anyhit))
for (k, w), n in sorted(why.items()):
    print("   ", k, w, n)
