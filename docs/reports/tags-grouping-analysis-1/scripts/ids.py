import sys, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
for sub in ["spine","ruin_source","lifeline","contest","scar","action","break_target","palette"]:
    print("##", sub)
    for r in dt.rows("foundation.yaml#"+sub):
        print(f"  {r['id']:34} fam={r.get('family','-'):12} {r.get('label','')[:60]:60} req={r.get('requires')}")
