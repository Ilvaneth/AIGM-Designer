import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
ids_by_file = {}
for ref, r in dt._every_row():
    ids_by_file.setdefault(ref.split("#")[0], set()).add(r["id"])
owner = {i: f for f, s in ids_by_file.items() for i in s}
def cond_ids(c):
    if c is None: return set()
    if isinstance(c, list):
        s=set()
        for x in c: s|=cond_ids(x)
        return s
    return {x for k in ("any_of","all_of","none_of") for x in (c.get(k) or [])}
from collections import Counter
cnt = Counter()
for ref, r in dt._every_row():
    f = ref.split("#")[0]
    refs = set(r.get("conflicts_with") or []) | cond_ids(r.get("requires")) | set().union(*[cond_ids(w.get("when")) for w in (r.get("weight_by") or [])] or [set()])
    for x in refs:
        of = owner.get(x, "?")
        if of != f:
            cnt[(f, of)] += 1
for k, v in sorted(cnt.items()): print(k, v)
