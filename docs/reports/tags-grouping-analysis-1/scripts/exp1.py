import sys, time, collections, random, statistics
sys.path.insert(0, r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad")
import varsim as V
N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
MODELS = [
    V.Model("today(plan: soft q/form/lineage, hard rule)"),
    V.Model("claims(neg filter)", claims=True),
    V.Model("soft trope x3 by contest (f=.25)", trope="soft", trope_f=0.25),
    V.Model("hard trope by contest (f=.25)", trope="hard", trope_f=0.25),
    V.Model("hard trope by contest (f=.5)", trope="hard", trope_f=0.5),
    V.Model("hard trope by contest+spine+lifeline+era (f=.5)", trope="hard", trope_f=0.5, trope_headings=("contest","spine","lifeline","era")),
    V.Model("hard everything (q,form,lineage,rule, trope f=.25)", q="hard", form="hard", lineage="hard", rule="hard", trope="hard", trope_f=0.25),
    V.Model("soft everything (rule soft x3)", q="soft", form="soft", lineage="soft", rule="soft", trope="soft", trope_f=0.25),
    V.Model("flat (no weights, rule unfiltered)", q="today", form="today", lineage="today_uniform", rule="none"),
]
t0 = time.time()
print("dial entropy bits:", round(V.dial_entropy(), 2))
for M in MODELS:
    tot = []; fnd = []; idn = []; per = collections.defaultdict(list); clash = 0; fails = collections.Counter(); ok = 0
    for i in range(N):
        rng = random.Random(f"dials-{i}")
        dials = V.sample_dials(rng)
        s = len(V.ENT)
        out, hv, err, R = V.birth(f"S{i}", dials, None, M)
        if err:
            fails[err.split(":")[0] + ":" + (err.split(":")[1] if ":" in err else "")] += 1
            continue
        ok += 1
        seg = V.ENT[s:]
        tot.append(sum(b for _, b, _ in seg))
        for lab, b, n in seg:
            per[lab].append(b)
        if V.clashes(V.facts(R, dials)):
            clash += 1
    keys = ["trope-breaks.yaml", "tensions.yaml", "signatures.yaml#institution_form", "signatures.yaml#people_lineage", "signatures.yaml#phenomenon_rule"]
    print(f"\n== {M.name}: ok {ok}/{N}, empty-pool {dict(fails)}, clash births {clash} ({100*clash/max(ok,1):.2f}%)")
    print(f"   P1 bits/birth (given dials): mean {statistics.mean(tot):.1f}  -> effective outcomes 2^{statistics.mean(tot):.0f}")
    for k in keys:
        v = per.get(k, [])
        # per-birth sum for that table
        print(f"   {k}: mean bits per draw {statistics.mean(v):.2f} (eff. pool {2**statistics.mean(v):.1f}), draws {len(v)}")
print("secs", round(time.time()-t0,1))
