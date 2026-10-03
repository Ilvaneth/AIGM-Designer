import sys, itertools, collections
SK = r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts"
sys.path.insert(0, SK)
import design_tables as dt, design_arbiter as arb, design_foundation as fd, designer
idx = dt.conflict_index()
print("the 5 pairs:", sorted({tuple(sorted((a, b))) for a, bs in idx.items() for b in bs}))
SPAN = {"short": 4, "standard": 11, "epic": 19}
TB = {"short": 1, "standard": 2, "epic": 2}
tones = ["grimdark", "dark fantasy", "heroic", "horror", "political", "swashbuckling", "cosmic"]
mixes = [["war", "politics", "exploration"], ["mystery", "horror", "exploration"], ["politics", "mystery", "war"]]
all_rows = {}
for name in dt.list_tables():
    doc = dt.load(name)
    refs = ([name] if doc.get("rows") else []) + [f"{name}#{k}" for k, v in (doc.get("tables") or {}).items() if isinstance(v, dict) and v.get("rows")]
    for ref in refs:
        for r in dt.rows(ref): all_rows[r["id"]] = r
fails = collections.Counter(); ex = collections.defaultdict(list); drawn = collections.Counter(); n = 0
combos = list(itertools.product(("short", "standard", "epic"), ("low", "medium", "high"),
                                ("medieval", "renaissance", "ancient", "nautical", "underground")))
for i in range(1500):
    sc, mg, era = combos[i % len(combos)]
    d = {"scale": sc, "magic": mg, "era": era, "tone": tones[i % 7], "content_mix": mixes[i % 3],
         "level_band": [1, 1 + SPAN[sc]], "danger": "standard"}
    R = designer.Roller.in_memory(f"AUDIT-{i}", d)
    try:
        out = fd.roll(R, d)
        R.table("tension.1", "tensions.yaml")
        br = []
        for k in range(TB[sc]):
            br.append(R.table(f"break.{k+1}", "trope-breaks.yaml", exclude=set(br))["row_id"])
        R.table("secret_archetype", "secrets.yaml#archetype", secret=True)
        R.table("secret_twist", "secrets.yaml#twist", secret=True)
        R.table("secret_trail", "secrets.yaml#trail", secret=True)
    except SystemExit as e:
        fails["SystemExit"] += 1; ex["SystemExit"].append((i, sc, mg, era, str(e)[:160])); continue
    n += 1
    rolled = [r["row_id"] for r in R.public + R.secret if r.get("row_id")]
    for x in rolled: drawn[x] += 1
    ctx = arb.Context(dials=d, rolled={x: False for x in rolled})
    cp = arb.conflicting_pairs(rolled)
    if cp: fails["conflict"] += 1; ex["conflict"].append((i, cp))
    for x in rolled:
        r = all_rows.get(x)
        if not r: continue
        if r.get("forbidden") and not any(ctx.has(a) for a in r.get("allowed_via") or []):
            fails["forbidden"] += 1; ex["forbidden"].append((i, x))
        # final-state check: a later roll must not break an earlier row's requirement (none_of)
        if not arb.holds(r.get("requires"), ctx):
            forced = any(rec.get("row_id") == x and rec.get("notation") == "forced" for rec in R.public + R.secret)
            fails["requires broken at the end" + (" (forced)" if forced else "")] += 1
            ex["requires broken at the end" + (" (forced)" if forced else "")].append((i, x, r.get("requires")))
    tb = [x for x in rolled if x.startswith("break_")]
    fams = [all_rows[x].get("family") for x in tb]
    if len(fams) != len(set(fams)): fails["two breaks same family (item 10 rule)"] += 1
print("runs ok:", n, "| failures:", dict(fails) or "none")
for k, v in ex.items(): print("  ", k, v[:6])
tb_rows = [k for k in all_rows if k.startswith("break_")]
print("trope rows never drawn:", [k for k in tb_rows if not drawn[k]])
print("tension rows never drawn:", [k for k in all_rows if k.startswith("tension_") and not drawn[k]])
