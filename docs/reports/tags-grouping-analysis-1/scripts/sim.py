import sys, random, collections, io, contextlib
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd, design_tables as dt
TR = "trope-breaks.yaml"
trows = {r["id"]: r for r in dt.rows(TR)}
PROHIB = {i for i, r in trows.items() if r.get("prohibition")}
def dials_for(rng):
    scale = rng.choice(["short","standard","epic"])
    era = rng.choices(["medieval","renaissance","ancient","nautical","underground"],[3,2,1,2,1])[0]
    mix = rng.sample(["exploration","politics","war","horror","mystery"],3)
    tone = rng.choice(["grimdark","dark fantasy","heroic","horror","political","swashbuckling","cosmic"])
    lb = {"short":[1,5],"standard":[1,11],"epic":[1,20]}[scale]
    return {"scale":scale,"magic":rng.choice(["low","medium","high"]),"era":era,"tone":tone,"content_mix":mix,"level_band":lb,"danger":"standard"}
UNAUDITED = {
 "underground_forbidden x mining": ("break_underground_forbidden", {"contest_mine_owners_miners","life_copper_mine","life_iron_coal","life_gemstones"}),
 "border_forbidden x envoy/newcomers/two-kingdom marriage": ("break_border_forbidden", {"contest_foreign_envoy","contest_settlers_newcomers","life_binding_marriage"}),
 "war_is_ritual x mix_war dial": ("break_war_is_ritual", {"DIAL:war"}),
 "war_is_ritual x war_fed_company/occupier": ("break_war_is_ritual", {"contest_war_fed_company","contest_occupier_resistance"}),
 "sky rows x era underground": ("DIAL:underground", {"scar_sky_changed","act_fell_from_sky","land_floating_isles","land_sky_river","spine_floating_archipelago","ruin_fallen_sky_city","ruin_fallen_star","ruin_star_kingdom","spine_river_to_sea","spine_long_coast"}),
 "no_writing x world_is_young": ("break_no_writing", {"break_world_is_young"}),
}
def run(n, seed0=0, taboo_prohib=True):
    hits = collections.Counter(); stats = collections.Counter(); prohib_sizes = []
    for s in range(n):
        rng = random.Random(f"dials{s}")
        d = dials_for(rng)
        R = designer.Roller.in_memory(f"SEED-{s}", d)
        out = fd.roll(R, d)
        count = {"short":1,"standard":2,"epic":2}[d["scale"]]
        tropes = []
        need_prohib = taboo_prohib and "scar_new_taboo" in out["scars"]
        for k in range(count):
            fams = {trows[t]["family"] for t in tropes}
            where = (lambda r, f=fams: r["family"] not in f)
            if need_prohib and k == 0:
                where = (lambda r, f=fams: r["family"] not in f and r["id"] in PROHIB)
                stats["taboo_births"] += 1
            try:
                rec = R.table(f"break.{k+1}", TR, exclude=set(tropes), where=where, why="fam")
            except SystemExit as e:
                stats["empty"] += 1; break
            tropes.append(rec["row_id"])
        rolled = set(R.ctx.rolled) | {"DIAL:"+x for x in d["content_mix"]} | {"DIAL:"+d["era"]}
        stats["births"] += 1
        for name,(a,bs) in UNAUDITED.items():
            if a in rolled and rolled & bs:
                hits[name] += 1
        # prohibition pool size for a taboo draw if it were the SECOND draw after a governance first
    return hits, stats
if __name__ == "__main__":
    n = int(sys.argv[1])
    hits, stats = run(n)
    print(stats)
    for k,v in hits.most_common(): print(f"{v:5d} {100*v/stats['births']:.2f}%  {k}")
