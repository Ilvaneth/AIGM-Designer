import sys, itertools, collections
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_foundation as fd, designer
SPAN = {"short": 4, "standard": 11, "epic": 19}; TB = {"short": 1, "standard": 2, "epic": 2}
PAIRS = {
 "kurayla hükümdar x miras yoluyla taht": ("break_rule_by_lottery", {"contest_two_heirs", "contest_sibling_rulers"}),
 "lordlar yok x soylu/taht/bey çekişmesi": ("break_no_kings_only_guilds", {"contest_two_heirs", "contest_empty_throne", "contest_sibling_rulers", "contest_lords_peasants", "contest_old_order_reform", "life_binding_marriage"}),
 "demir nadir x demir/çelik can damarı": ("break_iron_is_sacred", {"life_iron_coal", "life_famous_steel"}),
 "yeraltı yasak x yeraltı temeli": ("break_underground_forbidden", {"spine_three_depths", "spine_mountain_within", "life_deep_lake", "life_deep_mouth", "life_mushroom_fields", "contest_surface_deep", "ERA_UNDERGROUND"}),
}
hits = collections.Counter(); n = 0
combos = list(itertools.product(("short", "standard", "epic"), ("low", "medium", "high"), ("medieval", "renaissance", "ancient", "nautical", "underground")))
for i in range(3000):
    sc, mg, era = combos[i % len(combos)]
    d = {"scale": sc, "magic": mg, "era": era, "tone": "political", "content_mix": ["war", "politics", "exploration"], "level_band": [1, 1 + SPAN[sc]]}
    R = designer.Roller.in_memory(f"LIT-{i}", d)
    fd.roll(R, d); R.table("tension.1", "tensions.yaml")
    br = []
    for k in range(TB[sc]): br.append(R.table(f"break.{k+1}", "trope-breaks.yaml", exclude=set(br))["row_id"])
    rolled = {r["row_id"] for r in R.public + R.secret if r.get("row_id")}
    if era == "underground": rolled.add("ERA_UNDERGROUND")
    n += 1
    for name, (a, bs) in PAIRS.items():
        if a in rolled and rolled & bs: hits[name] += 1
print("runs:", n)
for name in PAIRS: print(f"  {name}: {hits[name]} runs")
