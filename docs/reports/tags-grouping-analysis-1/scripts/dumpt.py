import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
for r in dt.rows("trope-breaks.yaml"):
    print(r["id"], "|", r["family"], "|", r["label"], "| tags", r.get("tags"), "| cw", r.get("conflicts_with"), "| proh" if r.get("prohibition") else "", "| ov", r.get("overrides"))
