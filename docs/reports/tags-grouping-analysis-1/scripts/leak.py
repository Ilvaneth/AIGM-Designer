import sys, random
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_arbiter as arb, design_tables as dt
rows = dt.rows("pantheon.yaml#type")
ctx = arb.Context(dials={}, rolled={"SECRET_ROW": True})
# a claim token set by a secret row, expanded the way R9 proposes: it clashes with two public rows
conf = {"SECRET_ROW": frozenset({"pantheon_dead_gods", "pantheon_silent_gods"}),
        "pantheon_dead_gods": frozenset({"SECRET_ROW"}), "pantheon_silent_gods": frozenset({"SECRET_ROW"})}
res = arb.arbitrate("pantheon.yaml#type", rows, ctx, conflicts=conf, secret_ids={"SECRET_ROW"})
rec = arb.pick(random.Random("x"), res["pool"], res["weights"])
print("table rows:", len(rows), "| public excluded:", res["excluded"], "| public record:", rec)
print("pool order:", [r["id"] for r in res["pool"]])
