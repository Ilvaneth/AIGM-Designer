import sys, random, collections, statistics, io, contextlib
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd, design_tables as dt, design_arbiter as arb
N = int(sys.argv[1]); ORDER = sys.argv[2]; SET = sys.argv[3]   # ORDER: none | after | first ; SET: core | ext
CORE = {
 "break_rule_by_lottery": {"rulers":"lottery"}, "break_no_kings_only_guilds": {"rulers":"guilds","nobility":"none"},
 "break_dragons_rule": {"rulers":"dragon"},
 "contest_two_heirs": {"rulers":"hereditary"}, "contest_sibling_rulers": {"rulers":"hereditary"}, "contest_empty_throne": {"rulers":"hereditary"},
 "contest_lords_peasants": {"nobility":"present"}, "contest_old_order_reform": {"nobility":"present"},
 "life_binding_marriage": {"rulers":"hereditary"},
 "break_iron_is_sacred": {"iron":"rare"}, "life_iron_coal": {"iron":"plenty"}, "life_famous_steel": {"iron":"plenty"},
 "break_underground_forbidden": {"deep":"forbidden"}, "dial:era=underground": {"deep":"lived","sky":"none"},
 "spine_three_depths": {"deep":"lived"}, "spine_mountain_within": {"deep":"lived"}, "life_deep_lake": {"deep":"lived"},
 "life_deep_mouth": {"deep":"lived"}, "life_mushroom_fields": {"deep":"lived"}, "contest_surface_deep": {"deep":"lived"},
 "dial:magic=high": {"magic_now":"high"}, "ruin_age_of_mages": {"magic_now":"faded"},
 "dial:era=renaissance": {"writing":"print"}, "break_no_writing": {"writing":"none"},
 "break_moon_trades": {"sky":"present"}, "break_night_is_safe": {"sky":"present"},
}
EXT = dict(CORE)
EXT.update({
 "contest_occupier_resistance": {"nobility":"present"}, "contest_capital_marches": {"nobility":"present"},
 "contest_humans_fey": {"nobility":"present"}, "break_magic_is_nobility": {"nobility":"present"},
 "break_war_is_ritual": {"mass_war":"none"}, "contest_war_fed_company": {"mass_war":"present"},
 "break_world_is_young": {"history":"young"},
})
for r in dt.rows("foundation.yaml#ruin_source"):
    if r["family"] in ("old_peoples",): EXT[r["id"]] = {"history":"ancient"}
CL = CORE if SET=="core" else EXT
def claims_of_ctx(ctx):
    out = collections.defaultdict(set)
    for k,v in ctx.dials.items():
        vs = v if isinstance(v,(list,tuple)) else [v]
        for x in vs:
            for t,val in CL.get(f"dial:{k}={x}",{}).items(): out[t].add(val)
    for rid in ctx.rolled:
        for t,val in CL.get(rid,{}).items(): out[t].add(val)
    return out
def clashes(rid, held):
    return any(held.get(t) and (held[t]-{v}) for t,v in CL.get(rid,{}).items())
class CR(designer.Roller):
    pass
orig = designer.Roller.table
def table(self, label, ref, **kw):
    if ORDER != "none":
        held = claims_of_ctx(self.ctx)
        ex = set(kw.get("exclude") or ())
        ex |= {r["id"] for r in dt.rows(ref) if clashes(r["id"], held)}
        kw["exclude"] = ex
    return orig(self, label, ref, **kw)
designer.Roller.table = table
def wpick(rng, sub):
    rows = dt.rows(f"dials.yaml#{sub}")
    return rng.choices([r["value"] for r in rows], weights=[r.get("weight",1) for r in rows])[0]
BAND = {"short":[1,5],"standard":[1,10],"epic":[1,17]}
pools = collections.defaultdict(list); freq = collections.Counter(); faults = collections.Counter(); cooc = 0; ok = 0
pairfreq = collections.Counter()
def roll_tropes(R, d):
    n_tb = dt.roll_header("trope-breaks.yaml")["count_by_scale"][d["scale"]]; tb, fams = [], []
    for n in range(1, n_tb+1):
        rec = R.table(f"break.{n}", "trope-breaks.yaml", exclude=set(tb), where=lambda r, f=tuple(fams): r["family"] not in f, why="another family")
        tb.append(rec["row_id"]); fams.append(dt.row("trope-breaks.yaml", rec["row_id"])["family"])
for i in range(N):
    rng = random.Random(1000+i)
    d = {k: wpick(rng,k) for k in ("scale","tone","magic","era","danger")}
    d["content_mix"] = rng.sample([r["value"] for r in dt.rows("dials.yaml#content_mix")], 3)
    d["level_band"] = BAND[d["scale"]]
    R = designer.Roller.in_memory(f"SIM-{i}", d)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if ORDER == "first": roll_tropes(R, d)
            out = fd.roll(R, d)
            if ORDER != "first": roll_tropes(R, d)
    except SystemExit as e:
        faults[str(e)[:100]] += 1; continue
    ok += 1
    for rec in R.public:
        if rec.get("row_id"): freq[rec["row_id"]] += 1
        lab = rec["label"]
        if lab.startswith("break."): lab = "break.*"
        if lab.startswith("foundation.contest"): lab = "foundation.contest.*"
        if lab in ("break.*","foundation.spine","foundation.lifeline","foundation.contest.*","foundation.ruin") and str(rec.get("notation","")).startswith("d"):
            pools[lab].append(int(rec["notation"][1:]))
    held = claims_of_ctx(R.ctx)
    bad = [t for t,v in held.items() if len(v)>1]
    if bad: cooc += 1; pairfreq.update(bad)
print(f"ORDER={ORDER} SET={SET} births ok {ok}/{N}; faults {dict(faults)}; births holding a clash {cooc} ({cooc/max(ok,1):.2%}) by topic {dict(pairfreq)}")
for lab, xs in sorted(pools.items()):
    xs=sorted(xs); print(f"   pool {lab:22} min {xs[0]:3} p5 {xs[int(.05*len(xs))]:3} med {statistics.median(xs):5}")
watch = ["break_no_kings_only_guilds","break_rule_by_lottery","break_dragons_rule","break_iron_is_sacred","break_underground_forbidden","break_no_writing","break_moon_trades","break_night_is_safe","break_war_is_ritual","break_world_is_young","contest_two_heirs","contest_sibling_rulers","contest_empty_throne","contest_lords_peasants","life_iron_coal","life_famous_steel","ruin_age_of_mages","contest_surface_deep","spine_three_depths"]
print("   freq per 1000 births:", {w.replace("break_","b:").replace("contest_","c:").replace("life_","l:"): round(1000*freq[w]/ok,1) for w in watch})
