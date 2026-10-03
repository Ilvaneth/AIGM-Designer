import sys, time, collections, random, statistics
sys.path.insert(0, r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad")
import varsim as V
S = int(sys.argv[1]); B = int(sys.argv[2]); which = sys.argv[3] if len(sys.argv) > 3 else "all"
REFS = ["foundation.yaml#spine", "foundation.yaml#ruin_source", "foundation.yaml#lifeline", "foundation.yaml#contest",
        "foundation.yaml#action", "foundation.yaml#scar", "trope-breaks.yaml", "tensions.yaml",
        "signatures.yaml#people_lineage", "signatures.yaml#institution_form", "signatures.yaml#people_trait",
        "signatures.yaml#institution_practice", "signatures.yaml#phenomenon_rule", "secrets.yaml#archetype", "naming.yaml#family"]
MODELS = {
 "today_code": (V.Model("today"), False),
 "today_intended": (V.Model("today"), True),
 "hard_all_f25": (V.Model("hard", q="hard", form="hard", lineage="hard", rule="hard", trope="hard", trope_f=0.25), True),
 "soft_all_x3": (V.Model("soft", q="soft", form="soft", lineage="soft", rule="soft", trope="soft", trope_f=0.25), True),
}
if which != "all":
    MODELS = {k: v for k, v in MODELS.items() if k in which.split(",")}
for name, (M, intended) in MODELS.items():
    first_fb = collections.defaultdict(list)     # ref -> birth index of the first usage fallback per sequence
    rep_any = collections.defaultdict(lambda: [0, 0])   # ref -> [draws that repeat an earlier birth's row, draws]
    rep_near = collections.defaultdict(lambda: [0, 0])  # repeat of a row from the last 3 births
    rep_by_birth = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))  # ref -> window -> counts
    empties = collections.Counter(); births_ok = 0
    same_head = collections.defaultdict(lambda: [0, 0])  # (heading kind) -> [same row, pairs]
    t0 = time.time()
    for s in range(S):
        store = V.Store(intended=intended)
        hist = []          # per birth: ref -> set(rows), headings
        fb_seen = set()
        for b in range(B):
            dials = V.sample_dials(random.Random(f"d-{s}-{b}"))
            out, hv, err, R = V.birth(f"Q{s}-{b}", dials, store, M)
            if err:
                empties[err.split(":")[0] + (":" + err.split(":")[1] if ":" in err else "")] += 1
                store.births.append({})
                hist.append(({}, None))
                continue
            births_ok += 1
            rows = collections.defaultdict(set)
            for r in R.public + R.secret:
                ref = r.get("table")
                if ref in REFS and r.get("row_id"):
                    rows[ref].add(r["row_id"])
                    if r.get("usage_fallback") and ref not in fb_seen:
                        fb_seen.add(ref); first_fb[ref].append(b + 1)
            win = "01-10" if b < 10 else ("11-20" if b < 20 else "21+")
            for ref, got in rows.items():
                earlier = set().union(*[h[0].get(ref, set()) for h in hist]) if hist else set()
                near = set().union(*[h[0].get(ref, set()) for h in hist[-3:]]) if hist else set()
                for x in got:
                    rep_any[ref][1] += 1; rep_near[ref][1] += 1; rep_by_birth[ref][win][1] += 1
                    if x in earlier: rep_any[ref][0] += 1; rep_by_birth[ref][win][0] += 1
                    if x in near: rep_near[ref][0] += 1
            # predictability: births sharing the contest family, do they share the question / trope rows?
            cf = hv["contest"]
            for (h_rows, h_hv) in hist:
                if h_hv and h_hv["contest"] == cf:
                    for ref in ("tensions.yaml", "trope-breaks.yaml", "signatures.yaml#institution_form"):
                        same_head[ref][1] += 1
                        if rows.get(ref, set()) & h_rows.get(ref, set()):
                            same_head[ref][0] += 1
            hist.append((dict(rows), hv))
            store.record(R)
        for ref in REFS:
            if ref not in fb_seen:
                first_fb[ref].append(None)
    print(f"\n==== {name} (intended waits={intended}) S={S} B={B}: births ok {births_ok}, empty pools {dict(empties)}, {time.time()-t0:.0f}s")
    print(f"{'table':42s} {'1st fallback: median / % seqs':>30s} {'repeat any%':>11s} {'rep<=3%':>8s} {'rep% b1-10/11-20/21+':>22s}")
    for ref in REFS:
        fbs = [x for x in first_fb[ref] if x is not None]
        med = statistics.median(fbs) if fbs else None
        a = rep_any[ref]; n = rep_near[ref]
        w = rep_by_birth[ref]
        ws = "/".join(f"{100*w[k][0]/w[k][1]:.0f}" if w[k][1] else "-" for k in ("01-10", "11-20", "21+"))
        print(f"{ref:42s} {str(med):>12s} / {100*len(fbs)/S:5.0f}%        {100*a[0]/max(a[1],1):9.1f} {100*n[0]/max(n[1],1):8.1f} {ws:>22s}")
    for ref, (k, n) in same_head.items():
        print(f"   same contest family -> shares {ref}: {100*k/max(n,1):.1f}% of {n} pairs")
