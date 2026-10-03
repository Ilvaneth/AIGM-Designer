import sys, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
sys.argv = ["x","1","none","ext"]
import design_tables as dt
src = open(r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad\claims.py", encoding="utf-8").read()
ns = {}; exec(src.split("CL = CORE")[0], ns)   # CORE, EXT only
EXT = ns["EXT"]
where = {}
for sub in ("spine","ruin_source","lifeline","contest","palette"):
    for r in dt.rows(f"foundation.yaml#{sub}"): where[r["id"]] = (sub, r.get("family"))
for r in dt.rows("trope-breaks.yaml"): where[r["id"]] = ("trope", r["family"])
topics = collections.defaultdict(lambda: collections.defaultdict(list))
for rid, cl in EXT.items():
    for t, v in cl.items():
        topics[t][v].append(rid)
for t, vals in topics.items():
    print(f"topic {t}:")
    for v, ids in vals.items():
        tabs = collections.Counter(where.get(i, ("dial", None))[0] for i in ids)
        fams = sorted({f"{where[i][0]}/{where[i][1]}" for i in ids if i in where})
        print(f"   {v:10} rows {len(ids)} in {dict(tabs)} families {fams}")
# trope-side: how many parent tables each clashing trope spans
print()
for rid, cl in EXT.items():
    if not rid.startswith("break_"): continue
    parents = set()
    for other, ocl in EXT.items():
        if other == rid: continue
        if any(t in ocl and ocl[t] != v for t, v in cl.items()):
            parents.add(where.get(other, ("dial",))[0] if not other.startswith("dial:") else other.split("=")[0])
    print(f"{rid:32} clashes with parents: {sorted(parents)}")
tagv = collections.Counter(t for r in dt.rows("trope-breaks.yaml") for t in r.get("tags") or [])
print("\ntrope 'tags' vocabulary:", dict(tagv.most_common()))
