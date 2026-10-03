import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
def c(x): return json.dumps(x, ensure_ascii=False, separators=(",",":"))
for sub, fields in [("palette",["label","height","water","fantastic","requires","weight_by","implies","cap_exempt"]),
                    ("spine",["label","family","key_kind","forces","forces_one_of","requires","weight_by"]),
                    ("ruin_source",["label","family","remnant_kind","olgu_families","requires","adds_palette","weight_by"]),
                    ("lifeline",["label","family","where","requires"]),
                    ("contest",["label","family","prize","requires","weight_by","roles"])]:
    print("=====", sub)
    for r in dt.rows(f"foundation.yaml#{sub}"):
        d = {k: r.get(k) for k in fields if r.get(k) is not None}
        if "roles" in d: d["roles"] = {k:(v.get("archetype") if isinstance(v,dict) else v) for k,v in d["roles"].items()}
        print(r["id"], c(d))
