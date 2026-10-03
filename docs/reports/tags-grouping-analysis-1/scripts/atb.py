import sys
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
def none_tc(r):
    rq = r.get("requires"); cs = rq if isinstance(rq, list) else [rq] if rq else []
    return any("time_coming" in (c.get("none_of") or []) for c in cs)
for key, rows in dt.all_row_lists(dt.load("signatures.yaml")).items():
    atb = [r["id"] for r in rows if r.get("after_the_break")]
    guarded = [r["id"] for r in rows if none_tc(r)]
    if atb or guarded:
        print(key, "after_the_break:", len(atb), "guarded by none_of time_coming:", len(guarded), "unguarded:", sorted(set(atb) - set(guarded)))
