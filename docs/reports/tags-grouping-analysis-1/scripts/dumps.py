import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
def c(x): return json.dumps(x, ensure_ascii=False, separators=(",",":"))
for sub in ["people_lineage","people_trait","people_attitude","institution_form","institution_practice","institution_sign","institution_power","phenomenon_rule","phenomenon_sign","phenomenon_limit","phenomenon_user"]:
    print("=====", sub, c(dt.roll_header(f"signatures.yaml#{sub}")))
    for r in dt.rows(f"signatures.yaml#{sub}"):
        d = {k: r.get(k) for k in ("family","kind","playable","hints","form_word","requires","weight_by","after_the_break") if r.get(k) is not None}
        print(" ", r["id"], "|", r.get("label"), "|", c(d))
print("===== tensions", c(dt.roll_header("tensions.yaml")))
for r in dt.rows("tensions.yaml"):
    print(" ", r["id"], "|", r.get("label"), "|", c({k:r.get(k) for k in ("families","conflicts_with","weight_by","requires") if r.get(k)}))
