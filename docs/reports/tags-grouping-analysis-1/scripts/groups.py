import sys, collections, statistics
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
T = dt.rows("tensions.yaml")
cf = sorted({r["family"] for r in dt.rows("foundation.yaml#contest")})
print("tension group size by contest family:", {f: sum(1 for r in T if f in r["families"]) for f in cf})
print("tension memberships per row: mean", statistics.mean(len(r["families"]) for r in T), "-> f =", round(statistics.mean(len(r["families"]) for r in T)/len(cf), 3))
F = dt.rows("signatures.yaml#institution_form")
hints = ["state","religious","martial","guild","trade","scholarly","criminal","resistance"]
print("form group size by hint:", {h: [r["id"] for r in F if h in (r.get("hints") or [])] for h in hints})
# hint frequency among contest roles with a hint
C = dt.rows("foundation.yaml#contest")
hc = collections.Counter()
for c in C:
    for k, v in c["roles"].items():
        if v.get("hint"): hc[v["hint"]] += 1
print("role hints over all contest roles:", dict(hc))
R = dt.rows("foundation.yaml#ruin_source")
of = collections.Counter(f for r in R for f in r["olgu_families"])
print("olgu family listed by ruins:", dict(of), "mean per ruin", statistics.mean(len(r["olgu_families"]) for r in R), "-> f =", round(statistics.mean(len(r["olgu_families"]) for r in R)/8, 3))
print("rule pool size per ruin (rows):", collections.Counter(5*len(r["olgu_families"]) for r in R))
L = dt.rows("signatures.yaml#people_lineage")
print("lineages with a condition:", sum(1 for r in L if r.get("weight_by")), "of", len(L))
# contest: per-family hints; lifeline requires
print("trope rows per family:", dict(collections.Counter(r["family"] for r in dt.rows("trope-breaks.yaml"))))
print("prohibition rows:", sum(1 for r in dt.rows("trope-breaks.yaml") if r.get("prohibition")))
