import sys, collections, time
sys.path.insert(0, ".")
import p1sim
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
t = time.time(); hit_births = 0; pairs = collections.Counter(); empty = collections.Counter(); pools = []
for i in range(N):
    try:
        d, R, out = p1sim.birth(i, pool_log=pools)
    except SystemExit as e:
        empty[str(e)[:90]] += 1; continue
    h = p1sim.audit_hits(p1sim.rolled(R), d)
    hit_births += bool(h); pairs.update(h)
print(f"N={N} births with an audited pair: {hit_births} ({100*hit_births/N:.2f}%) empty pools: {sum(empty.values())} {dict(empty)}  {time.time()-t:.0f}s")
print("trope pool size (after constraints+usage): mean %.1f min %d" % (sum(pools)/len(pools), min(pools)))
for p, c in pairs.most_common(): print("  ", c, p)
