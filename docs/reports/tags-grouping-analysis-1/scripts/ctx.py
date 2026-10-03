import sys, collections
sys.path.insert(0, ".")
import p1sim, design_foundation as fd
CON = fd.rows_by_id("contest"); LIFE = fd.rows_by_id("lifeline"); SP = fd.rows_by_id("spine")
full, fams, single = set(), set(), collections.Counter()
N = 3000
for i in range(N):
    d = p1sim.sample_dials(i)
    import designer
    R = designer.Roller.in_memory(f"SIM-{i}", d); out = fd.roll(R, d)
    full.add((d["era"], d["magic"], out["spine"], out["ruin"], out["lifeline"], out["contests"][0]["id"]))
    fams.add((d["era"], d["magic"], SP[out["spine"]]["family"], LIFE[out["lifeline"]]["family"], CON[out["contests"][0]["id"]]["family"]))
print(f"{N} births: distinct (era, magic, spine, ruin, lifeline, contest) contexts at the trope roll: {len(full)}")
print(f"distinct contexts at family level (era, magic, spine fam, lifeline fam, contest fam): {len(fams)}; possible {5*3*6*7*8}")
