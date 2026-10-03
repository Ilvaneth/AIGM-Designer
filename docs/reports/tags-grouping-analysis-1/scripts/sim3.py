import sys, random, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd
from sim import dials_for, trows, TR
LIVED = {"life_deep_lake","life_deep_mouth","life_mushroom_fields","contest_surface_deep","spine_three_depths","spine_mountain_within"}
N = 3000; c = collections.Counter()
for s in range(N):
    d = dials_for(random.Random(f"dials{s}"))
    for mode in ("none", "R7", "lived_only"):
        R = designer.Roller.in_memory(f"SEED-{s}", d)
        fd.roll(R, d)
        rolled = set(R.ctx.rolled)
        excl = set()
        if mode == "R7" and ("land_underground" in rolled or d["era"] == "underground" or rolled & LIVED): excl.add("break_underground_forbidden")
        if mode == "lived_only" and (d["era"] == "underground" or rolled & LIVED): excl.add("break_underground_forbidden")
        tropes = []
        for k in range({"short":1,"standard":2,"epic":2}[d["scale"]]):
            fams = {trows[t]["family"] for t in tropes}
            tropes.append(R.table(f"break.{k+1}", TR, exclude=set(tropes)|excl, where=lambda r, f=fams: r["family"] not in f, why="fam")["row_id"])
        c[mode] += "break_underground_forbidden" in tropes
print(c)
