import sys, random, collections, statistics
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import designer, design_foundation as fd, design_tables as dt
from sim import dials_for, trows, PROHIB, TR
LIVED = {"life_deep_lake","life_deep_mouth","life_mushroom_fields","contest_surface_deep","spine_three_depths","spine_mountain_within","land_underground"}
def sequence(seqno, nbirths, claims):
    used = set(); out = []
    for b in range(nbirths):
        rng = random.Random(f"seq{seqno}-{b}")
        d = dials_for(rng); d["scale"] = rng.choice(["short","standard","epic"])
        R = designer.Roller.in_memory(f"S{seqno}-{b}", d)
        R._usage = lambda ref, avoid, u=used: ({"used_elsewhere": set(u)} if ref == TR else {})
        o = fd.roll(R, d)
        rolled = set(R.ctx.rolled)
        excl = set()
        if claims and (rolled & LIVED or d["era"] == "underground"):
            excl.add("break_underground_forbidden")
        taboo = "scar_new_taboo" in o["scars"]
        count = {"short":1,"standard":2,"epic":2}[d["scale"]]
        tropes = []
        for k in range(count):
            fams = {trows[t]["family"] for t in tropes}
            is_taboo = taboo and k == count - 1   # the prohibition draw taken last (after a free draw) at standard/epic
            if is_taboo:
                where = lambda r, f=fams: r["family"] not in f and r["id"] in PROHIB
            else:
                where = lambda r, f=fams: r["family"] not in f
            try:
                rec = R.table(f"break.{k+1}", TR, exclude=set(tropes) | excl, where=where, why="fam")
            except SystemExit:
                out.append(("empty", b, is_taboo)); break
            tropes.append(rec["row_id"])
            out.append(("draw", b, is_taboo, bool(rec.get("usage_fallback")), len(PROHIB - excl - set(tropes[:-1]) - {x for x in PROHIB if trows[x]["family"] in fams})))
        used |= set(tropes)
    return out
for claims in (False, True):
    fb_taboo = fb_all = n_taboo = n_all = 0; first_fb = []; sizes = collections.Counter(); empties = 0
    for s in range(20):
        res = sequence(s, 40, claims)
        ff = None
        for r in res:
            if r[0] == "empty": empties += 1; continue
            _, b, is_taboo, fb, size = r
            n_all += 1; fb_all += fb
            if is_taboo:
                n_taboo += 1; fb_taboo += fb; sizes[size] += 1
            if fb and ff is None: ff = b
        first_fb.append(ff if ff is not None else 99)
    print(f"claims={claims}: draws {n_all}, fallback {fb_all} ({100*fb_all/n_all:.1f}%); taboo draws {n_taboo}, taboo fallback {fb_taboo} ({100*fb_taboo/max(1,n_taboo):.1f}%); empties {empties}; first fallback birth median {statistics.median(first_fb)}; taboo group size dist {sorted(sizes.items())}")
