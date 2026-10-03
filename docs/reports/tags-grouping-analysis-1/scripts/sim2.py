import sys, random, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd
from sim import dials_for, trows, TR
PAIRS = {
 "magic_is_nobility x any magic dial's own regulator (P2/P4 hook clash)": ("break_magic_is_nobility", {"DIAL:low","DIAL:medium","DIAL:high"}),
 "world_is_young (300y) x epic scale (history 500y)": ("break_world_is_young", {"DIAL:epic"}),
 "dungeons_inhabited (every site negotiate) x mix_horror (a site test/enslave per act)": ("break_dungeons_inhabited", {"DIAL:horror"}),
 "war_is_ritual x mix_war (fronts, sieges)": ("break_war_is_ritual", {"DIAL:war"}),
 "no_kings (state faction is a guild) x P4 quota forcing archetype_state (every scale)": ("break_no_kings_only_guilds", {"DIAL:short","DIAL:standard","DIAL:epic"}),
}
hits = collections.Counter(); N = 3000; any_hit = 0
for s in range(N):
    d = dials_for(random.Random(f"dials{s}"))
    R = designer.Roller.in_memory(f"SEED-{s}", d)
    fd.roll(R, d)
    tropes = []
    for k in range({"short":1,"standard":2,"epic":2}[d["scale"]]):
        fams = {trows[t]["family"] for t in tropes}
        tropes.append(R.table(f"break.{k+1}", TR, exclude=set(tropes), where=lambda r, f=fams: r["family"] not in f, why="fam")["row_id"])
    rolled = set(R.ctx.rolled) | {"DIAL:"+x for x in d["content_mix"]} | {"DIAL:"+d["magic"], "DIAL:"+d["scale"]}
    h = False
    for name,(a,bs) in PAIRS.items():
        if a in rolled and rolled & bs: hits[name] += 1; h = True
    any_hit += h
for k,v in hits.most_common(): print(f"{v:5d} {100*v/N:.2f}%  {k}")
print("any:", any_hit, f"{100*any_hit/N:.2f}%")
