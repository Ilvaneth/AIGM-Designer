import sys, re
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_tables as dt
pat = re.compile(r"soylu|lord|kral|taht|taç|varis|hanedan|prens|asil|savaş|ordu|yeraltı|derin|demir|çelik|maden|yazı|kitap|matbaa|ay\b|gece", re.I)
for r in dt.rows("foundation.yaml#contest"):
    txt = " / ".join(f"{k}:{v.get('tr')}[{v.get('hint')}]" for k,v in r["roles"].items()) + " || esc: " + "; ".join(r.get("escalation") or [])
    if pat.search(txt) or pat.search(str(r.get("tr"))): print(r["id"], "::", txt)
print("----")
for sub in ("lifeline","ruin_source","spine"):
    for r in dt.rows(f"foundation.yaml#{sub}"):
        s = str(r.get("tr"))
        if pat.search(s): print(r["id"], "::", s[:260])
print("----")
for i in ("break_world_is_young","break_war_is_ritual","break_underground_forbidden","break_iron_is_sacred","break_no_writing","break_night_is_safe","break_moon_trades","break_dragons_rule","break_humans_minority","break_the_enemy_won","break_maps_are_illegal","break_border_forbidden"):
    r = dt.row("trope-breaks.yaml", i); print(i, "::", r["statement"])
for i in ("ruin_age_of_mages",):
    print(i, dt.row("foundation.yaml#ruin_source", i).get("tr"))
for v in ("renaissance","underground"):
    r = [x for x in dt.rows("dials.yaml#era") if x["value"]==v][0]; print(v, str(r.get("effects"))[:400])
