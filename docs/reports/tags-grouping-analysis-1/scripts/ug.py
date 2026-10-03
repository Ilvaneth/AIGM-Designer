import sys, random, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd
from sim import dials_for
LIVED = {"life_deep_lake","life_deep_mouth","life_mushroom_fields","contest_surface_deep","spine_three_depths","spine_mountain_within"}
MINES = {"contest_mine_owners_miners","life_copper_mine","life_iron_coal","life_gemstones"}
c = collections.Counter()
N = 3000
for s in range(N):
    d = dials_for(random.Random(f"dials{s}"))
    R = designer.Roller.in_memory(f"SEED-{s}", d)
    out = fd.roll(R, d)
    rolled = set(R.ctx.rolled)
    ug = "land_underground" in rolled
    c["ug_palette"] += ug
    if d["era"] != "underground":
        c["non_ug_era"] += 1
        c["ug_palette_non_ug_era"] += ug
        if ug and not (rolled & LIVED): c["ug_palette_only_non_ug_era"] += 1
    else:
        c["ug_era"] += 1
    if ug and not (rolled & LIVED) and d["era"] != "underground": c["landform_only"] += 1
    if rolled & MINES: c["mines"] += 1
    if rolled & MINES and not ug and d["era"]!="underground": c["mines_no_ug"] += 1
print(c)
