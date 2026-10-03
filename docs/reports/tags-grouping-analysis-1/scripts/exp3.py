import sys, collections, random, math, statistics
sys.path.insert(0, r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad")
import varsim as V
N = int(sys.argv[1])
REFS = ["trope-breaks.yaml", "tensions.yaml", "signatures.yaml#institution_form", "signatures.yaml#people_lineage", "signatures.yaml#phenomenon_rule"]
MODELS = [V.Model("today", ), V.Model("soft_all", rule="soft", trope="soft", trope_f=0.25),
          V.Model("hard_all", q="hard", form="hard", lineage="hard", rule="hard", trope="hard", trope_f=0.25),
          V.Model("flat", q="today", form="today", lineage="today_uniform", rule="none")]
def H(c):
    t = sum(c.values()); return -sum(v/t*math.log2(v/t) for v in c.values())
for M in MODELS:
    marg = collections.defaultdict(collections.Counter); cond = collections.defaultdict(list)
    # collision: P(two births with the same contest family share the question row)
    byfam = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for i in range(N):
        dials = V.sample_dials(random.Random(f"x-{i}"))
        s = len(V.ENT)
        out, hv, err, R = V.birth(f"M{i}", dials, None, M)
        if err: continue
        for lab, b, n in V.ENT[s:]:
            if lab in REFS: cond[lab].append(b)
        for r in R.public + R.secret:
            if r.get("table") in REFS and r.get("row_id"):
                marg[r["table"]][r["row_id"]] += 1
                byfam[r["table"]][hv["contest"]][r["row_id"]] += 1
    print(f"\n== {M.name}")
    for ref in REFS:
        hm = H(marg[ref]); hc = statistics.mean(cond[ref])
        # collision prob given the same contest family vs overall
        coll_f = []
        for fam, c in byfam[ref].items():
            t = sum(c.values()); coll_f.append((t, sum((v/t)**2 for v in c.values())))
        tt = sum(t for t, _ in coll_f); cf = sum(t*p for t, p in coll_f)/tt
        t = sum(marg[ref].values()); co = sum((v/t)**2 for v in marg[ref].values())
        print(f"  {ref:36s} H(row) {hm:4.2f}  H(row|history) {hc:4.2f}  info fixed by earlier rolls {hm-hc:4.2f} bits ({100*(hm-hc)/hm:3.0f}%)  "
              f"distinct rows seen {len(marg[ref])}  P(same row | same contest fam) {100*cf:4.1f}% vs any {100*co:4.1f}%")
