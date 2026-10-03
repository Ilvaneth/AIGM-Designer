import sys, collections, random
sys.path.insert(0, r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad")
import varsim as V
N = int(sys.argv[1]); M = V.Model("today")
kind = collections.Counter(); births = 0; nclash = 0
def k(x):
    if "=" in x: return "dial " + x.split("=")[0]
    return x.split("_")[0]
for i in range(N):
    dials = V.sample_dials(random.Random(f"x-{i}"))
    out, hv, err, R = V.birth(f"C{i}", dials, None, M)
    if err: continue
    births += 1
    c = V.clashes(V.facts(R, dials))
    if c: nclash += 1
    for a, b in c: kind[k(a) + " x " + k(b)] += 1
print("births", births, "with a clash", nclash, f"{100*nclash/births:.2f}%")
for kk, v in kind.most_common(): print(f"  {kk}: {v}")
