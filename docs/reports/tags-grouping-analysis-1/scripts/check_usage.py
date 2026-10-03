import os, sys, json, tempfile
tmp = os.path.join(tempfile.gettempdir(), "variety_used_check.json")
json.dump({"_meta": {}, "campaigns": {f"_test-b{i}": {"foundation.yaml#action": [f"act_x{i}"], "foundation.yaml#scar": [f"scar_x{i}"]} for i in range(6)},
           "births": {f"_test-b{i}": {"first_approved": f"2026-01-0{i+1}"} for i in range(6)}}, open(tmp, "w"))
os.environ["DESIGN_USED_PATH"] = tmp
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_dice as dd
for ref in ("foundation.yaml#action", "foundation.yaml#scar"):
    print(ref, "avoid=True :", {k: sorted(v) for k, v in dd.usage("_test-new", ref, True).items()})
    print(ref, "avoid=False:", {k: sorted(v) for k, v in dd.usage("_test-new", ref, False).items()})
os.remove(tmp)
