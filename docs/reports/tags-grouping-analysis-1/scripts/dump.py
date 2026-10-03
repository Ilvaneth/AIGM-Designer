import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
ref = sys.argv[1]
keys = sys.argv[2].split(",") if len(sys.argv) > 2 else ["family","requires","conflicts_with","tr"]
for r in dt.rows(ref):
    d = {k: r.get(k) for k in keys if r.get(k) is not None}
    print(r["id"], "|", r.get("label"), "|", json.dumps(d, ensure_ascii=False))
