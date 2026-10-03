import sys, collections, random, statistics
sys.path.insert(0, r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad")
import varsim as V
N = int(sys.argv[1])
for M in (V.Model("today"), V.Model("hard_all", q="hard", form="hard", lineage="hard", rule="hard", trope="hard", trope_f=0.25)):
    per = collections.defaultdict(list); tot = collections.defaultdict(list)
    for i in range(N):
        dials = V.sample_dials(random.Random(f"x-{i}"))
        s = len(V.ENT)
        out, hv, err, R = V.birth(f"E{i}", dials, None, M)
        if err: continue
        b = collections.Counter()
        for lab, bits, n in V.ENT[s:]:
            key = lab if not lab.startswith("dice:") else "dice:" + lab.split(":")[1].rsplit(".", 1)[0]
            per[key].append(bits); b["layout+dice" if lab.startswith("dice:") else ("foundation" if lab.startswith("foundation") else "identity")] += bits
        for k, v in b.items(): tot[k].append(v)
    print("==", M.name)
    for k, v in sorted(per.items()):
        print(f"  {k:45s} mean bits/draw {statistics.mean(v):5.2f}  eff.pool {2**statistics.mean(v):6.1f}  draws/birth {len(v)/N:4.2f}")
    print("  totals per birth:", {k: round(statistics.mean(v), 1) for k, v in tot.items()})
