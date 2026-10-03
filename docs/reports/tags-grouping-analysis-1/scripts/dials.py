import sys
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
for d in ["scale","tone","magic","era","danger","content_mix"]:
    print(d, [(r.get("value"), r.get("weight")) for r in dt.rows("dials.yaml#"+d)])
print(dt.load("dials.yaml").get("fixed"))
for r in dt.rows("dials.yaml#era"):
    print(r["value"], {k:v for k,v in (r.get("effects") or {}).items() if k in ("summary","note","tech","sky")}, str(r.get("effects"))[:300])
