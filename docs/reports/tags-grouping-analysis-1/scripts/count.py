import sys, collections
src = open(r"C:\Users\armag\AppData\Local\Temp\claude\C--Users-armag-Desktop-Campaign-Designer\8d6f4f98-10d0-4c4d-9722-45585aa189da\scratchpad\claims.py", encoding="utf-8").read()
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
ns = {}; exec(src.split("CL = CORE")[0].replace("N = int(sys.argv[1]); ORDER = sys.argv[2]; SET = sys.argv[3]",""), ns)
for name in ("CORE","EXT"):
    CL = ns[name]; ids = list(CL); pairs = 0
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            if any(t in CL[b] and CL[b][t]!=v for t,v in CL[a].items()): pairs += 1
    assign = sum(len(v) for v in CL.values()); topics = {t for v in CL.values() for t in v}
    print(f"{name}: {len(ids)} tagged rows/dial values, {assign} claim assignments on {len(topics)} topics -> {pairs} clashing id pairs a conflicts_with list would need")
