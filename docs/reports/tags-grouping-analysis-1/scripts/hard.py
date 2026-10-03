import sys, pickle, collections, statistics
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt, design_arbiter as arb, design_foundation as fd
B = pickle.load(open(r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad\births.pkl","rb"))
def stats(name, xs):
    xs = sorted(xs); print(f"{name:52} min {xs[0]:3} p5 {xs[int(.05*len(xs))]:3} med {statistics.median(xs):5}  share0 {sum(1 for x in xs if x==0)/len(xs):.3f}  share<5 {sum(1 for x in xs if x<5)/len(xs):.3f}")
lin = dt.rows("signatures.yaml#people_lineage")
forms = dt.rows("signatures.yaml#institution_form")
tens = dt.rows("tensions.yaml")
spines = dt.rows("foundation.yaml#spine")
hard_lin, hard_form, hard_ten, hard_spine = [], [], [], []
scar_rule = 0; time_coming_rule = 0; craft_life = 0
contests = fd.rows_by_id("contest"); lifes = fd.rows_by_id("lifeline")
for b in B:
    ctx = arb.Context(dials=b["dials"]); [ctx.add(r, False) for r in b["rows"]]
    hard_lin.append(sum(1 for r in lin if arb.weight_of(r, ctx) > 1))
    c = contests[b["out"]["contests"][0]["id"]]
    hints = {v.get("hint") for k, v in c["roles"].items() if v.get("hint")}
    # form group for ONE hinted role (as the institution takes one role): min over roles
    hard_form.append(min(sum(1 for f in forms if h in (f.get("hints") or [])) for h in hints))
    hard_ten.append(sum(1 for t in tens if c["family"] in t["families"]))
    ctx0 = arb.Context(dials=b["dials"])
    hard_spine.append(sum(1 for r in spines if arb.holds(r.get("requires"), ctx0) and arb.weight_of(r, ctx0) > 1))
    if "scar_magic_rule_changed" in b["out"]["scars"]:
        scar_rule += 1
        if "time_coming" in b["rows"]: time_coming_rule += 1
    if lifes[b["out"]["lifeline"]]["family"] == "craft" and b["out"]["target"] == "target_lifeline": craft_life += 1
n = len(B)
stats("lineage: rows a soft weight favours (hard group)", hard_lin)
stats("institution_form: rows for the role's hint (hard group)", hard_form)
stats("tension: rows listing the contest family (hard group)", hard_ten)
stats("spine: rows the dials boost (hard group)", hard_spine)
print(f"births with scar_magic_rule_changed: {scar_rule/n:.3f} per birth (of them time_coming: {time_coming_rule}); born_of_break group 5 rows (3 when coming) -> dry after ~{5/(scar_rule/n):.0f} births under avoid_used")
print(f"births where the break strikes a craft lifeline (action group 4): {craft_life/n:.3f} per birth")
