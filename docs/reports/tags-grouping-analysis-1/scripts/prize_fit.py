import sys, collections, os, tempfile, math, copy
sys.stdout.reconfigure(encoding='utf-8')
os.environ["DESIGN_USED_PATH"] = os.path.join(tempfile.gettempdir(), "prize_used.json")
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\docs\reports\tags-grouping-analysis-1\scripts")
import p1sim
from p1sim import fd, designer, dt, arb
life = {r["id"]: r for r in dt.rows("foundation.yaml#lifeline")}
crow = {r["id"]: r for r in dt.rows("foundation.yaml#contest")}
ruin = {r["id"]: r for r in dt.rows("foundation.yaml#ruin_source")}
FAM = lambda *f: {i for i, r in life.items() if r["family"] in f}
IDS = lambda *i: {"life_" + x for x in i}
NEED = {
 "contest_one_harbour": IDS("natural_harbour", "strait_crossing", "shipbuilding", "fish_run", "oyster_beds", "sea_folk_hunt", "dye_sources", "amber_shores"),
 "contest_one_pasture": IDS("yak_herds", "horse_herds", "deer_migration", "wheat_plain", "carpet_weaving", "leather_armour", "vineyards", "flax_fields"),
 "contest_two_banks": IDS("snowmelt", "river_flood", "shared_water_right", "river_ford", "flax_fields", "tile_ceramics", "fish_run"),
 "contest_old_new_craft": FAM("craft"), "contest_share_keep_knowledge": FAM("craft"), "contest_split_family": FAM("craft"),
 "contest_mine_owners_miners": IDS("copper_mine", "iron_coal", "quarry", "gemstones", "peat_bog", "famous_steel"),
 "contest_open_close_road": FAM("passage") | IDS("pilgrim_road"),
}
base = {k: copy.deepcopy(v) for k, v in crow.items()}
_holds = arb.holds
def holds(cond, ctx):
    if isinstance(cond, dict) and "_and" in cond:
        return all(holds(c, ctx) for c in cond["_and"])
    return _holds(cond, ctx)
arb.holds = holds
arb.CONDITION_KEYS = tuple(arb.CONDITION_KEYS) + ("_and",)
def apply(on):
    for k, r in crow.items():
        r.clear(); r.update(copy.deepcopy(base[k]))
    if not on: return
    for k, L in NEED.items():
        r = crow[k]; conds = [{"any_of": sorted(L)}]
        if r.get("requires"): conds.append(r["requires"])
        r["requires"] = {"_and": conds}
        r["weight_by"] = list(r.get("weight_by") or []) + [{"when": {"any_of": sorted(L)}, "x": 3}]
    gods = [i for i, r in ruin.items() if r["family"] == "gods"]
    crow["contest_one_shrine"]["weight_by"] = list(crow["contest_one_shrine"].get("weight_by") or []) + [{"when": {"any_of": gods}, "x": 2}]
def run(on, N=3000):
    apply(on)
    freq = collections.Counter(); fam = collections.Counter(); mis = 0; births_mis = 0; draws = 0; empty = 0
    for i in range(N):
        d = p1sim.sample_dials(i)
        R = designer.Roller.in_memory(f"SIM-{i}", d)
        try:
            out = fd.roll(R, d)
        except SystemExit as e:
            empty += 1; continue
        lf = out["lifeline"]; bad = False
        for c in out["contests"]:
            cid = c["id"]; freq[cid] += 1; fam[crow[cid]["family"]] += 1; draws += 1
            if cid in NEED and lf not in NEED[cid]: mis += 1; bad = True
        births_mis += bad
    ent = -sum((v/draws) * math.log2(v/draws) for v in freq.values())
    return dict(freq=freq, fam=fam, mis=mis, births_mis=births_mis, draws=draws, ent=ent, empty=empty, N=N)
a = run(False); b = run(True)
for name, r in (("TODAY", a), ("AFTER", b)):
    print(name, "births", r["N"], "contest draws", r["draws"], "births with a mismatch", r["births_mis"], f"{100*r['births_mis']/r['N']:.1f}%", "empty pools", r["empty"],
          f"entropy {r['ent']:.3f} of {math.log2(40):.3f}", "rows seen", len(r["freq"]), "min/max", min(r["freq"].values()), max(r["freq"].values()))
print("\nthe eight rows: today -> after (draws, % of draws)")
for k in NEED:
    print(f"  {crow[k]['tr']['name']:<38} {a['freq'][k]:>4} ({100*a['freq'][k]/a['draws']:.1f}%) -> {b['freq'][k]:>4} ({100*b['freq'][k]/b['draws']:.1f}%)")
k = "contest_one_shrine"; print(f"  {crow[k]['tr']['name']:<38} {a['freq'][k]:>4} -> {b['freq'][k]:>4}")
print("\nfamilies: today -> after")
for f in a["fam"]: print(f"  {f:<22} {100*a['fam'][f]/a['draws']:.1f}% -> {100*b['fam'][f]/b['draws']:.1f}%")
rest_a = sorted(((v, k) for k, v in a["freq"].items() if k not in NEED)); rest_b = sorted(((v, k) for k, v in b["freq"].items() if k not in NEED))
print("\nother 32 rows: today min/max", rest_a[0][0], rest_a[-1][0], " after min/max", rest_b[0][0], rest_b[-1][0], rest_b[-1][1])
