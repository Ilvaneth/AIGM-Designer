import sys, itertools, collections
sys.path.insert(0, ".")
import p1sim, claims
claims.install()
combos = list(itertools.product(("short", "standard", "epic"), ("low", "medium", "high"), ("medieval", "renaissance", "ancient", "nautical", "underground")))
empty = collections.Counter(); hits = 0; pools = collections.defaultdict(list)
for i in range(2250):
    scale, magic, era = combos[i % len(combos)]
    d = {"scale": scale, "magic": magic, "era": era, "tone": "heroic", "content_mix": ["war", "mystery", "horror"], "level_band": [1, 1 + p1sim.SPAN[scale]]}
    pl = []
    try:
        _, R, out = p1sim.birth(i, d, pool_log=pl)
    except SystemExit as e:
        empty[str(e)[:100]] += 1; continue
    hits += bool(p1sim.audit_hits(p1sim.rolled(R), d))
    pools[era].extend(pl)
print("claims, 45 dial combos x 50: empty pools", sum(empty.values()), dict(empty), "audited pairs", hits)
for era, p in pools.items(): print(f"  era {era:12} trope pool mean {sum(p)/len(p):.1f} min {min(p)}")
