import sys, json
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
def short(r):
    keep = {k: v for k, v in r.items() if k not in ("tr","hooks","sense","text","yields","weak_point","label_tr","notes","forms","example","desc","plays","gives")}
    return json.dumps(keep, ensure_ascii=False)[:400]
for ref in sys.argv[1:]:
    print("==", ref, dt.roll_header(ref))
    for r in dt.rows(ref):
        print(short(r))
