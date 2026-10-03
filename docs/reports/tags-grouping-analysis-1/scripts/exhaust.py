"""Cross-birth variety cost of hard groups (used rows excluded across births, as used.json does)."""
import sys, random, collections, statistics
sys.path.insert(0, ".")
import p1sim, design_foundation as fd, design_tables as dt
ten = dt.rows("tensions.yaml"); rules = dt.rows("signatures.yaml#phenomenon_rule")
CON = fd.rows_by_id("contest"); RUIN = fd.rows_by_id("ruin_source")
births = []
for i in range(1500):
    d, R, out = p1sim.birth(i)
    births.append((CON[out["contests"][0]["id"]]["family"], RUIN[out["ruin"]].get("olgu_families") or [], "scar_magic_rule_changed" in out["scars"]))
def seq_run(mode, table, key, L=40, reps=300):
    firsts, falls, fits = [], [], []
    for rep in range(reps):
        rng = random.Random(f"{mode}-{table}-{rep}")
        seq = rng.sample(births, L); used = set(); first = None; nf = 0; nfit = 0
        for b, (cfam, ofams, magic_scar) in enumerate(seq, 1):
            rows = ten if table == "tension" else rules
            fit = (lambda r: cfam in (r.get("families") or [])) if table == "tension" else \
                  (lambda r: r["family"] in (["born_of_break"] if magic_scar else ofams))
            if mode == "hard":
                grp = [r for r in rows if fit(r)]
                pool = [r for r in grp if r["id"] not in used] or grp
                if not [r for r in grp if r["id"] not in used]:
                    nf += 1; first = first or b
                pick = rng.choice(pool)
            elif mode == "weighted":
                pool = [r for r in rows if r["id"] not in used]
                if not pool: pool = rows; nf += 1; first = first or b
                pick = rng.choices(pool, [3 if fit(r) else 1 for r in pool])[0]
            else:
                pool = [r for r in rows if r["id"] not in used]
                if not pool: pool = rows; nf += 1; first = first or b
                pick = rng.choice(pool)
            nfit += fit(pick); used.add(pick["id"])
        firsts.append(first or L + 1); falls.append(nf); fits.append(nfit / L)
    print(f"{table:9} {mode:9} first repeat at birth ~{statistics.median(firsts):>4} (median), repeats in {L} births: {statistics.mean(falls):5.1f}, group-fit rate {statistics.mean(fits):.2f}")
for t in ("tension", "rule"):
    for m in ("hard", "weighted", "free"):
        seq_run(m, t, None)
