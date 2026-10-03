import sys, os, collections
SK = r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts"
sys.path.insert(0, SK)
import design_tables as dt, design_arbiter as arb
# every row of every table
ids = {}; rows_all = []
for name in dt.list_tables():
    doc = dt.load(name)
    tabs = doc.get("tables") or {}
    refs = [name] if doc.get("rows") else []
    refs += [f"{name}#{k}" for k, v in tabs.items() if isinstance(v, dict) and v.get("rows")]
    for ref in refs:
        for r in dt.rows(ref):
            if isinstance(r, dict) and r.get("id"):
                ids.setdefault(r["id"], []).append(ref); rows_all.append((ref, r))
dup = {k: v for k, v in ids.items() if len(v) > 1}
print("rows:", len(rows_all), "| duplicate ids:", len(dup), list(dup)[:5])
dials = dt.load("dials.yaml")["tables"]
dial_vals = {k: {r.get("value") for r in v["rows"]} for k, v in dials.items()}
dial_vals["level_band"] = None
def cond_ids(c):
    if c is None: return set(), []
    if isinstance(c, list):
        s, bad = set(), []
        for x in c:
            a, b = cond_ids(x); s |= a; bad += b
        return s, bad
    s = {x for k in ("any_of", "all_of", "none_of") for x in (c.get(k) or [])}
    bad = []
    for dial, vals in (c.get("dial") or {}).items():
        if dial not in dial_vals: bad.append(f"unknown dial {dial}")
        elif dial_vals[dial] is not None:
            for v in vals or []:
                if v not in dial_vals[dial]: bad.append(f"{dial}={v}")
    return s, bad
problems = collections.Counter(); samples = collections.defaultdict(list)
for ref, r in rows_all:
    for x in r.get("conflicts_with") or []:
        if x not in ids: problems["conflicts_with dangling"] += 1; samples["conflicts_with dangling"].append((r["id"], x))
    s, bad = cond_ids(r.get("requires"))
    for x in s:
        if x not in ids: problems["requires dangling"] += 1; samples["requires dangling"].append((r["id"], x))
    for b in bad: problems["requires bad dial"] += 1; samples["requires bad dial"].append((r["id"], b))
    for w in r.get("weight_by") or []:
        s, bad = cond_ids(w.get("when"))
        for x in s:
            if x not in ids: problems["weight_by dangling"] += 1; samples["weight_by dangling"].append((r["id"], x))
        for b in bad: problems["weight_by bad dial"] += 1; samples["weight_by bad dial"].append((r["id"], b))
    for x in r.get("allowed_via") or []:
        if x not in ids: problems["allowed_via dangling"] += 1; samples["allowed_via dangling"].append((r["id"], x))
idx = dt.conflict_index()
asym = [(a, b) for a, bs in idx.items() for b in bs if a not in idx.get(b, ())]
print("conflict index entries:", sum(len(v) for v in idx.values()) // 2, "pairs | asymmetric:", len(asym))
print("problems:", dict(problems) or "none")
for k, v in samples.items(): print("  ", k, v[:8])
# forbidden rows and their admission
forb = [(ref, r["id"], r.get("allowed_via")) for ref, r in rows_all if r.get("forbidden")]
print("forbidden rows:", len(forb), "| with allowed_via:", [(i, a) for _, i, a in forb if a])
