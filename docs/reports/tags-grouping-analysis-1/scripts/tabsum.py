import sys, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
SECRET_FILES = {"secrets.yaml","antagonists.yaml"}
for f in ["dials.yaml","foundation.yaml","trope-breaks.yaml","signatures.yaml","tensions.yaml","secrets.yaml","antagonists.yaml","naming.yaml"]:
    doc = dt.load(f)
    lists = dt.all_row_lists(doc)
    print("=== ", f, "top keys:", [k for k in doc.keys() if k not in ("tables","rows")])
    for sub, rows in lists.items():
        keys = collections.Counter()
        for r in rows:
            keys.update(k for k in r.keys() if k not in ("id","label","hooks","tr","weight","notes","note"))
        fams = collections.Counter(r.get("family") for r in rows)
        print(f"  {sub}: {len(rows)} rows; fields: {dict(keys)}")
        if len(fams)>1 or None not in fams:
            print("     families:", dict(fams))
