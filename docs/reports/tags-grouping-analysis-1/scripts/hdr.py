import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
for s in ["spine","palette","ruin_source","lifeline","contest","break_target","action","scar","time"]:
    h = dt.roll_header(f"foundation.yaml#{s}")
    print(s, json.dumps({k:v for k,v in h.items() if k not in ("note",)}, ensure_ascii=False)[:300])
print("trope", dt.roll_header("trope-breaks.yaml"))
print("tension", dt.roll_header("tensions.yaml"))
d = dt.load("dials.yaml")
for s in ["scale","tone","magic","era","danger","content_mix"]:
    print(s, [(r["value"], r.get("weight",1)) for r in dt.rows(f"dials.yaml#{s}")])
print(dt.load("foundation.yaml")["phenomenon_rule_families"] if "phenomenon_rule_families" in dt.load("foundation.yaml") else "")
