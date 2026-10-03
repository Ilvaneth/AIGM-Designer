import sys, collections, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
SECRET = {"secrets.yaml", "antagonists.yaml"}
for f in ["foundation.yaml","trope-breaks.yaml","tensions.yaml","signatures.yaml","secrets.yaml","antagonists.yaml","dials.yaml","naming.yaml"]:
    doc = dt.load(f)
    lists = dt.all_row_lists(doc)
    print("==", f, "header keys:", [k for k in doc if k not in ("tables","rows")])
    for name, rows in lists.items():
        keys = collections.Counter()
        req = collections.Counter(); conf = 0; wb = 0
        for r in rows:
            keys.update(r.keys())
            rq = r.get("requires")
            if rq:
                conds = rq if isinstance(rq, list) else [rq]
                for c in conds:
                    for k in c: req[k]+=1
            conf += len(r.get("conflicts_with") or [])
            wb += len(r.get("weight_by") or [])
        fams = collections.Counter(r.get("family") for r in rows)
        hdr = {}
        try: hdr = dt.roll_header(f + ("#"+name if name!="rows" else ""))
        except Exception as e: hdr = {"err": str(e)}
        print(f"  [{name}] rows={len(rows)} fams={len([x for x in fams if x])} conflicts_with_entries={conf} weight_by={wb} requires_keys={dict(req)}")
        print("     fields:", sorted(k for k in keys if k not in ("id","label","hooks","tr")))
        print("     roll:", {k:v for k,v in hdr.items() if k not in ("fantastic_cap_by_magic",)} if hdr else None)
