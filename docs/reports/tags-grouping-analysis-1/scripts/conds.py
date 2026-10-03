import sys, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
P1 = ["foundation.yaml", "trope-breaks.yaml", "tensions.yaml", "signatures.yaml"]
lists = collections.Counter(); n_conds = 0; ids_ref = collections.Counter(); rows_total = 0; kinds = collections.Counter()
per_table_rows = {}
def walk(cond, where):
    global n_conds
    if cond is None: return
    if isinstance(cond, list):
        for c in cond: walk(c, where)
        return
    for k in ("any_of", "all_of", "none_of"):
        if cond.get(k):
            n_conds += 1; kinds[(where, k)] += 1
            lists[tuple(sorted(cond[k]))] += 1
            for x in cond[k]:
                ids_ref[x.split("_")[0]] += 1
    if cond.get("dial"): kinds[(where, "dial")] += 1
for f in P1:
    for key, rows in dt.all_row_lists(dt.load(f)).items():
        ref = f + ("#" + key if key else "")
        if f == "signatures.yaml" and key in ("phenomenon", "people", "institution"): continue   # the old seed rows item 10 replaces
        per_table_rows[ref] = len(rows); rows_total += len(rows)
        for r in rows:
            walk(r.get("requires"), "requires")
            for wb in r.get("weight_by") or []:
                walk(wb.get("when"), "weight_by")
print("P1 public rows (new tables):", rows_total)
print("condition lists over row ids:", n_conds, "; by kind:", dict(kinds))
print("ids referenced by prefix:", dict(ids_ref))
rep = [(l, c) for l, c in lists.items() if c > 1]
print("distinct id-lists:", len(lists), "; lists used more than once:", len(rep))
for l, c in sorted(rep, key=lambda x: -x[1])[:12]:
    print(f"  x{c} len {len(l)}: {list(l)[:6]}{'...' if len(l) > 6 else ''}")
nonpal = [(l, c) for l, c in lists.items() if any(not x.startswith("land_") for x in l)]
print("lists naming non-palette rows (implicit tags):", len(nonpal))
for l, c in nonpal: print(f"  x{c} {list(l)}")
# pair-matrix size
tabs = list(per_table_rows.items())
cross = sum(a * b for i, (_, a) in enumerate(tabs) for (_, b) in tabs[i + 1:])
print("cross-table row pairs (the conflicts_with matrix to review):", cross)
