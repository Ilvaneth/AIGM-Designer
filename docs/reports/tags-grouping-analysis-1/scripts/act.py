import sys, json, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
acts = dt.rows("foundation.yaml#action")
for a in acts:
    print(a["id"], a["targets"], json.dumps(a.get("fits"), separators=(",",":")))
doc = dt.load("foundation.yaml")
print("key_kinds", doc.get("key_kinds")); print("remnant_kinds", doc.get("remnant_kinds"))
# group sizes: actions per (piece, value)
lifefams = sorted({r["family"] for r in dt.rows("foundation.yaml#lifeline")})
out = {}
for piece, vals in [("lifeline", lifefams), ("remnant", doc["remnant_kinds"] if isinstance(doc["remnant_kinds"], list) else list(doc["remnant_kinds"])), ("key_place", doc["key_kinds"] if isinstance(doc["key_kinds"], list) else list(doc["key_kinds"]))]:
    for v in vals:
        n = sum(1 for a in acts if piece in a["targets"] and v in (a.get("fits") or {}).get(piece, []))
        out[(piece, v)] = n
for piece in ("heart","role","thin_place"):
    out[(piece,"*")] = sum(1 for a in acts if piece in a["targets"])
for k,v in sorted(out.items(), key=lambda kv: kv[1]): print(k, v)
