"""Whole-P1 measurement (2026-10-03): how many births of TODAY's tables hold something the owner's review
ruled out. Real foundation roller; the identity rolls are p1sim's approximation (item 10 is not built), and the
institution's role is drawn here among the seated hinted roles. Model-free scratch script, not a test."""
import sys, os, tempfile, random, collections
sys.stdout.reconfigure(encoding="utf-8")
os.environ["DESIGN_USED_PATH"] = os.path.join(tempfile.gettempdir(), "whole_used.json")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1sim
from p1sim import dt


def A(s):
    return set(s.split())


def L(*x):
    return {"life_" + i for i in x}


life = {r["id"]: r for r in dt.rows("foundation.yaml#lifeline")}
contest = {r["id"]: r for r in dt.rows("foundation.yaml#contest")}
tens = {r["id"]: r for r in dt.rows("tensions.yaml")}


def FAM(*f):
    return {i for i, r in life.items() if r["family"] in f}


NEED = {"contest_one_harbour": L("natural_harbour", "strait_crossing", "shipbuilding", "fish_run", "oyster_beds", "sea_folk_hunt", "dye_sources", "amber_shores"),
        "contest_one_pasture": L("yak_herds", "horse_herds", "deer_migration", "wheat_plain", "carpet_weaving", "leather_armour", "vineyards", "flax_fields"),
        "contest_two_banks": L("snowmelt", "river_flood", "shared_water_right", "river_ford", "flax_fields", "tile_ceramics", "fish_run"),
        "contest_old_new_craft": FAM("craft"), "contest_share_keep_knowledge": FAM("craft"), "contest_split_family": FAM("craft"),
        "contest_mine_owners_miners": L("copper_mine", "iron_coal", "quarry", "gemstones", "peat_bog", "famous_steel"),
        "contest_open_close_road": FAM("passage") | L("pilgrim_road")}
HERED = {"contest_two_heirs", "contest_empty_throne", "contest_sibling_rulers", "life_binding_marriage"}
NOBLE = {"contest_two_heirs", "contest_empty_throne", "contest_old_order_reform", "contest_occupier_resistance", "contest_capital_marches",
         "contest_lords_peasants", "life_binding_marriage", "contest_treasure_race", "contest_first_settlers", "contest_humans_giants",
         "contest_sibling_rulers"}
HERDS = L("yak_herds", "horse_herds", "deer_migration")
NOMAD_OK = HERDS | L("fish_run", "caravan_inn", "giant_insects", "pilgrim_road")
FORCED = {"contest_humans_giants": "lineage_giant_kin", "contest_humans_fey": "lineage_fey", "contest_land_sea_folk": "lineage_merfolk"}
ARCH = {"hold_the_key_place": A("state martial guild"), "keep_the_one_road": A("state martial guild"), "wall_builders": A("guild state martial"),
        "hold_the_remnant_gate": A("religious martial scholarly"), "guard_the_herds": A("martial resistance guild"),
        "players": A("guild resistance criminal"), "pilots": A("guild trade criminal"), "couriers": A("state guild trade"),
        "caravan_masters": A("trade guild"), "ferrymen": A("guild trade criminal"), "keep_the_old_works": A("guild scholarly state"),
        "golem_founders": A("guild scholarly martial"), "lifeline_craft": A("guild"), "ship_and_bridge": A("guild trade"),
        "mend_the_wound": A("religious scholarly resistance"), "mapmakers": A("scholarly guild state criminal"),
        "study_the_remnant": A("scholarly religious"), "seek_the_lost": A("scholarly religious"),
        "keep_the_dying": A("scholarly religious resistance"), "watch_the_sky": A("scholarly religious"),
        "raise_the_orphans": A("religious resistance state"), "healers": A("religious guild scholarly resistance"),
        "keep_the_granaries": A("state religious guild"), "midwives": A("religious guild"), "herd_healers": A("guild religious"),
        "monster_hunters": A("martial guild resistance"), "border_riders": A("martial state"), "champions": A("martial state"),
        "free_company": A("martial trade criminal"), "dragon_giant_hunters": A("martial"), "royal_monopoly": A("trade guild state"),
        "sell_the_remnant": A("trade criminal scholarly"), "sole_seller": A("trade guild"), "foreign_house": A("trade"),
        "smugglers_union": A("criminal trade"), "keep_the_lifeline_rite": A("religious"), "pilgrim_guides": A("religious trade"),
        "guard_the_holy_place": A("religious martial"), "worship_the_break": A("religious resistance"), "empty_temples": A("religious")}
for _r in dt.rows("signatures.yaml#institution_practice"):       # once item 8 is in, the table's own hints
    if _r.get("hints"):
        ARCH[_r["id"].replace("practice_", "")] = set(_r["hints"])
SPELL = {"rule_" + x for x in A("echo rebound inverted_element spells_grow_life spell_twins kin_doubles spell_marks delayed_spells "
                                "casting_ages gesture_magic monsters_smell_magic one_way_magic spells_feed_the_break geography_of_power half_spells")}
USABLE = {"rule_" + x for x in A("mirror_doors true_names signs_are_spells tongue_of_magic metal_wakes shared_wounds")}
SURFACE_RULES = {"rule_night_distances", "rule_seasons_bound_to_a_beast", "rule_feelings_make_weather"}
WAR_PRACTICES = {"practice_" + x for x in A("monster_hunters border_riders champions free_company dragon_giant_hunters")}


def check(i):
    d, R, out = p1sim.birth(i)
    rec = {r["label"]: r["row_id"] for r in R.public + R.secret if r.get("row_id")}
    got = set(rec.values())
    era, magic = d["era"], d["magic"]
    lf = out["lifeline"]
    pal = set(out["palette"]) | set(out.get("palette_extra") or [])
    cons = [c["id"] for c in out["contests"]]
    main, roles, ug = cons[0], out["contests"][0]["roles"], era == "underground"
    heart_below = out["spine"] in ("spine_three_depths", "spine_mountain_within") or out["layout"]["parts"].get("heart") == "land_underground"
    tropes = {v for k, v in rec.items() if k.startswith("break.") and not k.endswith(".tie")}
    ties = {v for k, v in rec.items() if k.endswith(".tie")}

    def T(x):
        return "break_" + x in tropes

    hit = collections.defaultdict(list)
    c = hit["clash"]                      # 1. literal clashes the review ruled
    if T("rule_by_lottery") and got & HERED: c.append("lottery x hereditary")
    if T("no_kings_only_guilds") and (got & NOBLE or ("contest_humans_fey" in cons and "fourth" in roles)): c.append("no lords x nobility or a throne")
    if T("war_is_ritual") and "contest_war_fed_company" in cons: c.append("champions x the war-fed company")
    if T("dragons_rule") and got & HERED: c.append("dragons rule x hereditary")
    if T("giants_are_peasants") and got & {"life_giant_peace", "contest_humans_giants"}: c.append("giant peasants x giants as a power")
    if T("gods_are_ancestors_known") and out["ruin"] == "ruin_dead_god": c.append("ancestor gods x a dead god")
    if T("night_is_safe") and ug: c.append("night is safe x underground era")
    if T("underground_forbidden") and (ug or heart_below): c.append("descent forbidden x a heart below")
    if T("no_writing") and era == "renaissance": c.append("no writing x renaissance")
    if "tie_break" in ties and out["time"] == "time_coming": c.append("tie is the break x coming")
    if out["ruin"] == "ruin_age_of_mages" and magic == "high": c.append("age of mages x magic high")
    if out["time"] == "time_coming" and set(out["scars"]) & {"scar_new_people", "scar_magic_rule_changed"}: c.append("coming x a product scar")
    if ug and (set(out["scars"]) & {"scar_sky_changed", "scar_seasons_broken"} or out["action"] == "act_fell_from_sky"): c.append("underground era x sky scar or action")
    if era == "nautical" and "land_coast" not in pal: c.append("nautical without a coast")
    if T("no_direct_lies") and got & {"rule_beasts_sense_lies", "trait_lies_foul_the_air"}: c.append("no lies x lie rows")
    if ug and got & (SURFACE_RULES | {"trait_winter_sleep", "trait_two_homes", "practice_watch_the_sky", "isign_no_night_travel"}): c.append("underground era x night, season, weather rows")
    if "trait_iron_is_unlucky" in got and lf in L("iron_coal", "famous_steel"): c.append("iron unlucky x iron lifeline")
    if {"trait_guest_three_days", "stranger_hostile_for_cause"} <= got or {"trait_one_envoy", "stranger_hospitable"} <= got: c.append("trait x attitude")
    if "trait_seven_year_rotation" in got and got & {"trait_never_stop", "trait_one_great_building"}: c.append("trait x trait")
    if "isign_unarmed" in got and (rec.get("sig.power") == "power_arms" or rec.get("sig.practice") in WAR_PRACTICES): c.append("unarmed x arms")
    if {"isign_no_marriage", "form_house"} <= got or {"isign_own_no_land", "power_place"} <= got: c.append("sign x form or power")
    if ({"limit_remnant_matter_absorbs", "rule_remnant_drinks_magic"} <= got or {"limit_a_day_from_remnant", "rule_geography_of_power"} <= got
            or ("limit_underground_only" in got and got & SURFACE_RULES)): c.append("limit x rule")
    h = hit["heading"]                    # 2. drawn outside its heading, or naming something never rolled
    if any(k in NEED and lf not in NEED[k] for k in cons): h.append("prize x lifeline")
    if main in FORCED and rec.get("sig.lineage") != FORCED[main]: h.append("the people's role x lineage")
    pr = rec.get("sig.practice", "")
    if pr == "practice_wall_builders" and out["spine"] != "spine_long_wall" and out["ruin"] != "ruin_besieged_land": h.append("the wall")
    if pr == "practice_empty_temples" and out["ruin"] != "ruin_departed_god": h.append("the departed god")
    if pr == "practice_guard_the_herds" and lf not in HERDS: h.append("the herds (practice)")
    if pr == "practice_lifeline_craft" and lf not in FAM("craft"): h.append("the craft")
    if pr in ("practice_raise_the_orphans", "practice_mend_the_wound") and out["time"] == "time_coming": h.append("the break's orphans or wound under coming")
    if "trait_herd_dreams" in got and lf not in HERDS: h.append("their herds (trait)")
    if "trait_never_stop" in got and lf not in NOMAD_OK: h.append("nomads on a fixed lifeline")
    rng = random.Random(f"INST-{i}")      # 3. the institution against its role (the role is this script's approximation)
    people_role = "b" if main in ("contest_humans_giants", "contest_humans_fey", "contest_land_sea_folk", "contest_surface_deep") else None
    hinted = [k for k in roles if k != people_role and (contest[main]["roles"].get(k) or {}).get("hint")]
    if hinted and contest[main]["roles"][rng.choice(hinted)]["hint"] not in ARCH[pr.replace("practice_", "")]:
        hit["institution"].append("practice x role archetype")
    rule, user = rec.get("sig.rule"), rec.get("sig.user")       # 4. rolls with no meaning; a far question
    spell_ok = rule in SPELL and user in ("user_casters", "user_everyone")
    self_ok = rule not in SPELL and rule not in USABLE and user == "user_no_one"
    if rule not in USABLE and not spell_ok and not self_ok: hit["user"].append("user x rule kind")
    fams = [contest[k]["family"] for k in cons]
    if any(f not in tens[rec[f"tension.{n + 1}"]]["families"] for n, f in enumerate(fams)): hit["question"].append("question outside the contest's family")
    return hit


N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
tier, why, any12, any123 = collections.Counter(), collections.Counter(), 0, 0
for i in range(N):
    hit = check(i)
    for k, v in hit.items():
        tier[k] += bool(v)
        for w in set(v):
            why[(k, w)] += 1
    any12 += bool(hit["clash"] or hit["heading"])
    any123 += bool(hit["clash"] or hit["heading"] or hit["institution"])


def pc(n):
    return f"{100 * n / N:.1f}%"


print("births", N)
print("1 a literal clash:", tier["clash"], pc(tier["clash"]))
print("2 outside its heading / names something unrolled:", tier["heading"], pc(tier["heading"]))
print("1 or 2:", any12, pc(any12))
print("3 institution practice against its role (approximate):", tier["institution"], pc(tier["institution"]))
print("1, 2 or 3:", any123, pc(any123))
print("4a a user roll with no meaning:", tier["user"], pc(tier["user"]))
print("4b a question outside the contest's family:", tier["question"], pc(tier["question"]))
for (k, w), n in sorted(why.items(), key=lambda x: (x[0][0], -x[1])):
    print(f"   {k:<12} {w:<52} {n:>5} {pc(n)}")
