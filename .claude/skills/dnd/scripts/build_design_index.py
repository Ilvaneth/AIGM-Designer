#!/usr/bin/env python3
"""
build_design_index.py — builds data/design/srd-index-2014.json, the SRD in the shape the designer
queries (plan item 18.1), and refreshes the generated rows of data/design/monster-ecology.yaml
(item 9.8, 17 #20; v0 from SRD fields, curated rows kept as they are).

Sources: data/dnd5e_srd.json (the built JSON: monsters, magic items, spells, equipment) joined with
data/srd-5.1-yaml/ (monsters, creatures and NPC appendices for immunities, resistances, legendary
actions and spellcasting; 09-running for traps, diseases, poisons and madness; 03-beyond1st for
backgrounds and languages; 04-equipment for trade goods). The gods appendix is not read (errata
24.2 #19). The OGL 1.0a notice is carried in the index header.

Candidate lists are filtered script-side from this index; the LLM only chooses and reskins
(item 18.2). CR is the SRD's; the designer's own estimator (item 18.4) shifts it one band when a
reskin moves HP, AC or damage by more than 25%.

CLI:
  build_design_index.py                 build the index and refresh monster-ecology.yaml (v0 rows only)
  build_design_index.py --check         exit 1 if the committed index or ecology differs from a fresh build
  build_design_index.py --stats         counts
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import data_dir  # noqa: E402

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("build_design_index: pyyaml is required") from exc

OGL_NOTICE = ("This work includes material taken from the System Reference Document 5.1 (\"SRD 5.1\") by Wizards of the "
              "Coast LLC, available under the Open Game License 1.0a; see data/srd-5.1-yaml/00-legal.yaml.")
RULESET = "2014"
INDEX_FILE = "srd-index-2014.json"
ECOLOGY_FILE = "monster-ecology.yaml"

HABITATS = ["any", "coast", "water", "river", "lake", "marsh", "bog", "salt", "cliff", "forest", "deep_forest", "jungle",
            "farmland", "grassland", "steppe", "hills", "moor", "mountain", "cold", "tundra", "desert", "sand", "rock",
            "canyon", "volcanic", "fire", "underground", "cave", "deep", "fungus", "ruins", "urban", "open", "sky",
            "planar_upper", "planar_lower", "planar_inner", "fey", "shadow"]
SOCIAL_ROLES = ["leader", "elite", "minion", "ambient", "solo"]
ARCHETYPES = ["state", "religious", "guild", "criminal", "martial", "scholarly", "resistance", "cult", "trade"]
SIZES = ("Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan")

NPC_AFFINITY = {
    "acolyte": ["religious"], "priest": ["religious"], "druid": ["religious", "resistance"],
    "cultist": ["cult"], "cult fanatic": ["cult"],
    "bandit": ["criminal", "resistance"], "bandit captain": ["criminal"], "thug": ["criminal", "guild"],
    "assassin": ["criminal"], "spy": ["criminal", "state", "trade"],
    "guard": ["state", "guild"], "veteran": ["martial", "state"], "knight": ["martial", "state"],
    "berserker": ["martial", "resistance"], "gladiator": ["martial", "guild"],
    "mage": ["guild", "scholarly"], "archmage": ["scholarly", "guild"],
    "noble": ["state", "trade"], "commoner": [], "scout": ["resistance", "martial"], "tribal warrior": ["resistance"],
}
PEOPLES = ("goblin", "hobgoblin", "bugbear", "orc", "kobold", "gnoll", "lizardfolk", "sahuagin", "merfolk", "drow",
           "duergar", "deep gnome", "svirfneblin", "grimlock", "troglodyte", "centaur", "satyr", "minotaur", "gnome",
           "halfling", "dwarf", "elf", "human")


# ── SRD sources ──────────────────────────────────────────────────────────────────

def srd_json() -> dict:
    return json.loads((data_dir() / "dnd5e_srd.json").read_text(encoding="utf-8"))


def yaml_doc(name: str):
    return yaml.safe_load((data_dir() / "srd-5.1-yaml" / name).read_text(encoding="utf-8"))


def is_stat_block(node) -> bool:
    if not isinstance(node, dict) or not isinstance(node.get("content"), list) or not node["content"]:
        return False
    first = node["content"][0]
    return isinstance(first, str) and bool(re.match(r"^\*(%s) " % "|".join(SIZES), first))


def walk_blocks(node, source: str, out: dict):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "content":
                continue
            if is_stat_block(value):
                out.setdefault(key, (source, value["content"]))
            else:
                walk_blocks(value, source, out)


def parse_block(lines: list) -> dict:
    text_lines = [x for x in lines if isinstance(x, str)]
    rec = {"damage_immunities": [], "damage_resistances": [], "damage_vulnerabilities": [], "condition_immunities": [],
           "has_legendary": False, "legendary_resistance": False, "spellcaster": False, "actions": [], "traits": []}
    section = "traits"
    for line in text_lines:
        for field, key in (("Damage Immunities", "damage_immunities"), ("Damage Resistances", "damage_resistances"),
                           ("Damage Vulnerabilities", "damage_vulnerabilities"), ("Condition Immunities", "condition_immunities")):
            m = re.match(r"^\*\*%s\*\*\s*(.+)$" % field, line)
            if m:
                rec[key] = [p.strip() for p in re.split(r",|;", m.group(1)) if p.strip()]
        if line.strip() == "**Legendary Actions**":
            rec["has_legendary"] = True
            section = "legendary"
            continue
        if line.strip() in ("**Actions**", "**Reactions**"):
            section = "actions"
            continue
        if line.startswith("***Legendary Resistance"):
            rec["legendary_resistance"] = True
        if re.match(r"^\*\*\*(Innate )?Spellcasting", line):
            rec["spellcaster"] = True
        m = re.match(r"^\*\*\*([^.*]+)\.?\*\*\*?", line)
        if m and section in ("traits", "actions"):
            rec[section].append(m.group(1).strip())
    return rec


def yaml_monsters() -> dict:
    out: dict = {}
    for name, source in (("11-monsters.yaml", "monsters"), ("15-creatures.yaml", "creatures"), ("16-npcs.yaml", "npcs")):
        walk_blocks(yaml_doc(name), source, out)
    return out


def _variants(name: str) -> set:
    """Spellings a name may go by: 'Elf, Drow' ↔ 'Drow'; 'Vampire, Bat Form' ↔ 'Vampire'; 'Giant Rat (Diseased)' ↔ 'Giant Rat'."""
    n = name.strip()
    out = {n}
    no_paren = re.sub(r"\s*\([^)]*\)", "", n).strip()
    out.add(no_paren)
    m = re.search(r"\(([^)]*)\)", n)
    if m:
        out.add(m.group(1).strip())
    parts = [p.strip() for p in no_paren.split(",")]
    if len(parts) > 1:
        out.add(parts[0])
        out.add(parts[-1])
        out.add(" ".join(reversed(parts)))
    out.add(re.sub(r",\s*[\w\s]+ Form$", "", n).strip())
    return {x.lower() for x in out if x}


def match_block(name: str, ym: dict):
    """The YAML stat block for a JSON monster name, or (None, None)."""
    if name in ym:
        return ym[name]
    wanted = _variants(name)
    best = None
    for key, block in ym.items():
        if wanted & _variants(key):
            if best is None or len(key) < len(best[0]):
                best = (key, block)
    if best is None and name.lower().startswith("swarm of ") and "Swarm of Insects" in ym:
        return ym["Swarm of Insects"]
    return best[1] if best else (None, None)


# ── ecology heuristics (v0) ────────────────────────────────────────────────────

def speeds(speed_text: str) -> dict:
    out = {"walk": 0}
    for m in re.finditer(r"(?:(fly|swim|burrow|climb|hover)\s+)?(\d+)\s*ft", speed_text or ""):
        out[m.group(1) or "walk"] = int(m.group(2))
    return out


def cr_value(raw) -> float:
    try:
        return float(raw)
    except (TypeError, ValueError):
        if isinstance(raw, str) and "/" in raw:
            a, b = raw.split("/")
            return float(a) / float(b)
    return 0.0


KEYWORD_HABITATS = [
    (r"shark|sea |sea-|kraken|octopus|eel|crab|plesiosaur|hippocampus|quipper|seahorse|sahuagin|merfolk|dragon turtle|marid|water elemental|merrow", ["coast", "water"]),
    (r"crocodile|frog|toad|hydra|lizardfolk|will-o|black dragon|swamp|bullywug|chuul", ["marsh", "bog", "water"]),
    (r"purple worm|ankheg|bulette|umber|grick|roper|piercer|darkmantle|drow|duergar|deep gnome|gibbering|carrion|otyugh|gelatinous|ochre|black pudding|gray ooze|rust monster|gargoyle|xorn|earth elemental|dao|cloaker|ghast|ghoul", ["underground", "cave"]),
    (r"red dragon|fire giant|salamander|azer|efreeti|fire elemental|magma|hell hound|magmin|fire snake", ["volcanic", "fire", "mountain"]),
    (r"white dragon|frost giant|remorhaz|mammoth|saber-toothed|polar bear|winter wolf|ice mephit|yeti", ["cold", "tundra", "mountain"]),
    (r"blue dragon|brass dragon|camel|hyena|jackal|gnoll|scorpion|mummy|djinni|air elemental|dust mephit|sphinx|vulture", ["desert", "sand", "open"]),
    (r"green dragon|owlbear|treant|dryad|blink dog|ettercap|giant spider|wolf|boar|elk|deer|owl|awakened|satyr|centaur|shambling|unicorn|pixie|sprite|badger|weasel|dire wolf|worg|bear", ["forest"]),
    (r"lion|elephant|rhinoceros|giant hyena|ogre|tiger|ape|baboon|giant constrictor|giant crocodile|behir|couatl|giant ape", ["jungle", "grassland"]),
    (r"harpy|griffon|roc|wyvern|manticore|chimera|hippogriff|eagle|hawk|peryton|stone giant|cloud giant|storm giant|hill giant|silver dragon|copper dragon|gold dragon|bronze dragon|pegasus|cockatrice|basilisk|orc|goblin|hobgoblin|bugbear|kobold|ettin|troll|cyclops", ["hills", "mountain"]),
    (r"rat|bat|spider|centipede|zombie|skeleton|wight|wraith|specter|ghost|shadow|banshee|vampire|lich|mimic|animated|flying sword|rug|medusa|minotaur|gargoyle|mummy|invisible stalker|homunculus|shield guardian|flesh golem|clay golem|stone golem|iron golem|doppelganger|wererat", ["ruins", "underground"]),
    (r"commoner|noble|guard|bandit|thug|spy|assassin|acolyte|priest|mage|archmage|knight|veteran|cultist|cult fanatic|gladiator|berserker|scout|tribal warrior|druid|wererat|werewolf|wereboar|werebear|weretiger", ["urban", "farmland"]),
]
TYPE_DEFAULTS = {
    "beast": ["forest", "grassland"], "humanoid": ["urban", "hills"], "dragon": ["mountain"], "monstrosity": ["hills", "ruins"],
    "fiend": ["planar_lower"], "undead": ["ruins", "underground"], "elemental": ["planar_inner"], "giant": ["hills", "mountain"],
    "construct": ["ruins", "urban"], "plant": ["forest", "marsh"], "fey": ["forest", "fey"], "celestial": ["planar_upper"],
    "aberration": ["underground", "deep"], "ooze": ["underground", "cave"],
}


def guess_habitats(name: str, mtype: str, spd: dict) -> list:
    low = name.lower()
    tags: list = []
    for pattern, habs in KEYWORD_HABITATS:
        if re.search(pattern, low):
            tags += habs
    base = mtype.split(" ")[0].lower() if mtype else ""
    if "swarm" in base:
        base = "beast"
    if not tags:
        tags += TYPE_DEFAULTS.get(base, ["any"])
    if spd.get("swim") and "water" not in tags:
        tags.append("water")
    if spd.get("burrow") and "underground" not in tags:
        tags.append("underground")
    if spd.get("fly") and base in ("beast", "monstrosity", "dragon") and "sky" not in tags:
        tags.append("sky")
    if base == "fiend":
        tags = ["planar_lower"] + [t for t in tags if t != "planar_lower"]
    if base == "celestial":
        tags = ["planar_upper"] + [t for t in tags if t != "planar_upper"]
    seen, out = set(), []
    for t in tags:
        if t not in seen and t in HABITATS:
            seen.add(t)
            out.append(t)
    return out[:4]


LEADER_NPCS = ("bandit captain", "knight", "mage", "archmage", "priest", "assassin", "druid", "noble", "cult fanatic")


def guess_role(name: str, mtype: str, cr: float, has_legendary: bool, source: str) -> str:
    low = name.lower()
    if has_legendary or cr >= 11:
        return "solo"
    if source == "npcs" and low in LEADER_NPCS:
        return "leader"
    if re.search(r"captain|chief|lord|king|queen|boss|matron|patriarch|elder", low):
        return "leader"
    base = mtype.split(" ")[0].lower()
    if cr <= 0.25 and base in ("beast",) or "swarm" in base and cr <= 0.5:
        return "ambient"
    if cr <= 1:
        return "minion"
    if cr >= 5:
        return "elite"
    return "elite" if base in ("dragon", "giant", "fiend", "celestial", "aberration") else "minion"


def guess_affinity(name: str, mtype: str, source: str) -> list:
    low = name.lower()
    if source == "npcs":
        return list(NPC_AFFINITY.get(low, []))
    base = mtype.split(" ")[0].lower()
    if base == "undead":
        return ["cult"]
    if base == "fiend":
        return ["cult"]
    if any(p in low for p in ("goblin", "hobgoblin", "bugbear", "orc", "kobold")):
        return ["martial", "criminal"]
    if "were" in low or "doppelganger" in low:
        return ["criminal"]
    return []


def is_people(name: str, mtype: str) -> bool:
    low = name.lower()
    return mtype.lower().startswith("humanoid") and any(p in low for p in PEOPLES)


# ── the index ─────────────────────────────────────────────────────────────────

def build_monsters(js: dict, ym: dict) -> dict:
    out = {}
    for m in js["monsters"]:
        name = m["name"]
        source, lines = match_block(name, ym)
        parsed = parse_block(lines) if lines else parse_block([])
        spd = speeds(m.get("speed", ""))
        cr = cr_value(m.get("cr"))
        mtype = m.get("type", "") or ""
        base = mtype.split(" (")[0]
        subtype = mtype[len(base) + 2:-1] if "(" in mtype else ""
        out[m["index"]] = {
            "name": name, "cr": cr, "xp": m.get("xp"), "type": base, "subtype": subtype, "size": m.get("size"),
            "alignment": m.get("alignment"), "ac": m.get("ac"), "hp": m.get("hp"), "speed": spd, "senses": m.get("senses"),
            "languages": m.get("languages"), "source": source or "monsters", "yaml_matched": lines is not None,
            "has_legendary": parsed["has_legendary"], "legendary_resistance": parsed["legendary_resistance"],
            "spellcaster": parsed["spellcaster"] or "Spellcasting:" in m.get("description", ""),
            "damage_immunities": parsed["damage_immunities"], "damage_resistances": parsed["damage_resistances"],
            "damage_vulnerabilities": parsed["damage_vulnerabilities"], "condition_immunities": parsed["condition_immunities"],
            "traits": parsed["traits"], "actions": parsed["actions"],
        }
    return out


def build_items(js: dict) -> tuple[dict, dict]:
    items, by_rarity = {}, {}
    for it in js["magic_items"]:
        desc = it.get("description", "")
        body = desc.split("\n\n", 1)[1] if "\n\n" in desc else desc
        effect = re.split(r"(?<=[.!?])\s", body.strip(), maxsplit=1)[0][:220] if body.strip() else ""
        items[it["index"]] = {"name": it["name"], "rarity": it["rarity"], "category": it["category"],
                              "attunement": bool(it["attunement"]), "effect": effect}
        by_rarity.setdefault(it["rarity"], []).append(it["index"])
    return items, {k: sorted(v) for k, v in by_rarity.items()}


def build_spells(js: dict) -> tuple[dict, dict]:
    spells, by_class = {}, {}
    for s in js["spells"]:
        planar = bool(re.search(r"\bplane\b|planar|Ethereal|Astral|Elemental Plane", s.get("description", "")))
        spells[s["index"]] = {"name": s["name"], "level": s["level"], "school": s.get("school"), "classes": s.get("classes", []),
                              "concentration": bool(s.get("concentration")), "ritual": bool(s.get("ritual")), "planar_ref": planar}
        for c in s.get("classes", []):
            by_class.setdefault(c, {}).setdefault(str(s["level"]), []).append(s["index"])
    return spells, {c: {lvl: sorted(ids) for lvl, ids in lv.items()} for c, lv in by_class.items()}


def _text(node) -> str:
    c = node.get("content", node) if isinstance(node, dict) else node
    if isinstance(c, list):
        return "\n".join(str(x) for x in c if isinstance(x, str))
    return str(c)


def build_hazards() -> dict:
    doc = yaml_doc("09-running.yaml")
    root = doc if "Traps" in doc else doc[next(iter(doc))]
    traps = []
    for name, node in root["Traps"]["Sample Traps"].items():
        if name == "content":
            continue
        text = _text(node)
        dcs = [int(x) for x in re.findall(r"DC (\d+)", text)]
        dmg = re.findall(r"(\d+d\d+)", text)
        kind = "magic" if "*Magic trap*" in text else "mechanical"
        top_dc = max(dcs) if dcs else 10
        tier = "T1" if top_dc <= 12 else "T2" if top_dc <= 15 else "T3" if top_dc <= 17 else "T4"
        traps.append({"name": name, "kind": kind, "dcs": sorted(set(dcs)), "damage_dice": sorted(set(dmg))[:6], "tier_hint": tier})
    diseases = [{"name": n, "summary": _text(node).split("\n")[0][:200]} for n, node in root["Diseases"]["Sample Diseases"].items()
                if n != "content"]
    pnode = root["Poisons"]["Poisons"]
    ptable = pnode.get("table") if isinstance(pnode, dict) else None
    if ptable is None and isinstance(pnode, dict):
        for v in pnode.values():
            if isinstance(v, dict) and "table" in v:
                ptable = v["table"]
    poisons = []
    if ptable:
        for item, typ, price in zip(ptable["Item"], ptable["Type"], ptable["Price per Dose"]):
            gp = int(re.sub(r"[^\d]", "", price)) if re.search(r"\d", price) else None
            poisons.append({"name": item, "type": typ, "price_gp": gp})
    madness = {}
    for key, label in (("Short-Term Madness", "short"), ("Long-Term Madness", "long"), ("Indefinite Madness", "indefinite")):
        node = root["Madness"]["Madness Effects"].get(key)
        table = node.get("table") if isinstance(node, dict) else None
        if table is None and isinstance(node, dict):
            for v in node.get("content", []):
                if isinstance(v, dict) and "table" in v:
                    table = v["table"]
        if table:
            cols = list(table.keys())
            madness[label] = [{"roll": r, "effect": e} for r, e in zip(table[cols[0]], table[cols[1]])]
    return {"traps": traps, "diseases": diseases, "poisons": poisons, "madness": madness}


def build_backgrounds_languages() -> tuple[list, dict]:
    doc = yaml_doc("03-beyond1st.yaml")
    root = doc[next(iter(doc))]
    backgrounds = [k for k in root["Backgrounds"] if k not in ("content", "Proficiencies", "Languages", "Equipment",
                                                                "Suggested Characteristics", "Customizing a Background")]
    langs = {}
    for key, label in (("Standard Languages", "standard"), ("Exotic Languages", "exotic")):
        node = root["Languages"].get(key, {})
        table = None
        for v in (node.get("content", []) if isinstance(node, dict) else []):
            if isinstance(v, dict) and "table" in v:
                table = v["table"]
        if table is None and isinstance(node, dict) and "table" in node:
            table = node["table"]
        langs[label] = list(table["Language"]) if table and "Language" in table else []
    return backgrounds, langs


def build_equipment(js: dict) -> tuple[dict, list]:
    equipment = {e["index"]: {"name": e["name"], "category": e["category"], "cost": e.get("cost"), "weight": e.get("weight")}
                 for e in js["equipment"]}
    doc = yaml_doc("04-equipment.yaml")
    goods = []

    def find_goods(node):
        if isinstance(node, dict):
            if "Trade Goods" in node and isinstance(node["Trade Goods"], dict) and "table" in node["Trade Goods"]:
                t = node["Trade Goods"]["table"]
                return [{"cost": c, "goods": g} for c, g in zip(t["Cost"], t["Goods"])]
            for v in node.values():
                r = find_goods(v)
                if r:
                    return r
        return None
    goods = find_goods(doc) or []
    return equipment, goods


def source_hashes() -> dict:
    out = {}
    for name in ("dnd5e_srd.json",):
        out[name] = hashlib.sha256((data_dir() / name).read_bytes()).hexdigest()[:16]
    for name in ("11-monsters.yaml", "15-creatures.yaml", "16-npcs.yaml", "09-running.yaml", "03-beyond1st.yaml", "04-equipment.yaml"):
        out[name] = hashlib.sha256((data_dir() / "srd-5.1-yaml" / name).read_bytes()).hexdigest()[:16]
    return out


def build_index(ecology: dict) -> dict:
    js = srd_json()
    ym = yaml_monsters()
    monsters = build_monsters(js, ym)
    for mid, rec in monsters.items():
        eco = ecology.get(mid)
        rec["ecology"] = ({"habitats": eco["habitats"], "social_role": eco["social_role"], "faction_affinity": eco["faction_affinity"],
                           "people": eco["people"], "curated": eco["curated"]} if eco else None)
    items, by_rarity = build_items(js)
    spells, by_class = build_spells(js)
    backgrounds, languages = build_backgrounds_languages()
    equipment, goods = build_equipment(js)
    return {
        "_meta": {"schema_version": 1, "ruleset": RULESET, "ogl_notice": OGL_NOTICE, "built_by": "build_design_index.py",
                  "sources": source_hashes(), "counts": {"monsters": len(monsters), "items": len(items), "spells": len(spells),
                                                         "equipment": len(equipment)}},
        "monsters": monsters, "items": items, "items_by_rarity": by_rarity, "spells": spells, "spells_by_class_level": by_class,
        "hazards": build_hazards(), "backgrounds": backgrounds, "languages": languages, "equipment": equipment, "trade_goods": goods,
    }


# ── monster-ecology.yaml ────────────────────────────────────────────────────────

ECOLOGY_HEADER = """# monster-ecology.yaml — every SRD monster's habitats, social role, faction affinity and reskin note
# (item 9.8, 17 #20, 18.1). GENERATED rows (`curated: false`) come from build_design_index.py's
# heuristics over the SRD's type, name and speeds; CURATED rows (`curated: true`) are hand-written and
# survive a rebuild. Habitats use regions.yaml's ecology tags plus the planar ones; a site's Combat
# rows and a region's Combat subtable are filtered from here by habitat and tier before the LLM
# chooses and reskins (item 18.2). A `people: true` row is a culture, never an inherently evil race
# (forbidden_inherently_evil_races): its members have alignments, settlements and a naming language.
schema_version: 1
table: monster-ecology
consumed_by: [P3, P5, P6, validator]
plan: "item 9.8, 17 #20, 18.1-18.2, 24.4"
generated_by: build_design_index.py
habitat_vocabulary: [%s]
social_roles: [%s]
hooks_common:
  - {phase: P6, must: "a site's ecology lists occupants from rows whose habitats include the site's region tags and whose CR sits in the site's tier"}
  - {phase: P3, must: "a region's Combat subtable draws only rows of its ecology tags at its tier"}
rows:
""" % (", ".join(HABITATS), ", ".join(SOCIAL_ROLES))


def yq(s: str) -> str:
    return '"' + str(s).replace("\\", "\\\\").replace('"', "'") + '"'


def ecology_row_text(r: dict) -> str:
    hooks = r.get("hooks") or [{"phase": "P6", "must": "candidate for sites in its habitats at its tier; reskin by the SRD's Modifying Creatures"}]
    lines = [f"  - id: {r['id']}", f"    label: {yq(r['label'])}", f"    srd: {r['srd']}", f"    cr: {r['cr']}",
             f"    type: {yq(r['type'])}", f"    source: {r['source']}", f"    habitats: [{', '.join(r['habitats'])}]",
             f"    social_role: {r['social_role']}", f"    faction_affinity: [{', '.join(r['faction_affinity'])}]",
             f"    people: {'true' if r['people'] else 'false'}", f"    reskin: {yq(r.get('reskin', ''))}",
             f"    curated: {'true' if r.get('curated') else 'false'}", "    hooks:"]
    for h in hooks:
        lines.append(f"      - {{phase: {h['phase']}, must: {yq(h['must'])}}}")
    return "\n".join(lines) + "\n"


def load_ecology(path: Path) -> dict:
    if not path.is_file():
        return {}
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {r["srd"]: r for r in (doc.get("rows") or []) if isinstance(r, dict) and r.get("srd")}


def generate_ecology(monsters: dict, existing: dict) -> list:
    rows = []
    for mid in sorted(monsters):
        m = monsters[mid]
        old = existing.get(mid)
        if old and old.get("curated"):
            row = dict(old)
            row.update({"cr": m["cr"], "type": m["type"], "source": m["source"], "label": m["name"]})
            rows.append(row)
            continue
        rows.append({"id": f"eco_{mid.replace('-', '_')}", "label": m["name"], "srd": mid, "cr": m["cr"], "type": m["type"],
                     "source": m["source"], "habitats": guess_habitats(m["name"], m["type"], m["speed"]),
                     "social_role": guess_role(m["name"], m["type"], m["cr"], m["has_legendary"], m["source"]),
                     "faction_affinity": guess_affinity(m["name"], m["type"], m["source"]),
                     "people": is_people(m["name"], m["type"]), "reskin": "", "curated": False})
    return rows


def ecology_text(rows: list) -> str:
    return ECOLOGY_HEADER + "".join(ecology_row_text(r) for r in rows)


# ── main ──────────────────────────────────────────────────────────────────────

def render_index(index: dict) -> str:
    return json.dumps(index, ensure_ascii=False, indent=1, sort_keys=False) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="build the designer's SRD index and refresh monster-ecology v0 rows")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args(argv)
    design = data_dir() / "design"
    eco_path = design / ECOLOGY_FILE
    idx_path = design / INDEX_FILE

    existing = load_ecology(eco_path)
    js = srd_json()
    monsters = build_monsters(js, yaml_monsters())
    rows = generate_ecology(monsters, existing)
    ecology = {r["srd"]: r for r in rows}
    index = build_index(ecology)
    new_eco = ecology_text(rows)
    new_idx = render_index(index)

    if a.stats:
        c = index["_meta"]["counts"]
        curated = sum(1 for r in rows if r.get("curated"))
        print(f"monsters {c['monsters']} (yaml-matched {sum(1 for m in monsters.values() if m['yaml_matched'])}, "
              f"legendary {sum(1 for m in monsters.values() if m['has_legendary'])}, spellcasters {sum(1 for m in monsters.values() if m['spellcaster'])}), "
              f"ecology rows {len(rows)} (curated {curated}), items {c['items']}, spells {c['spells']}, equipment {c['equipment']}, "
              f"traps {len(index['hazards']['traps'])}, diseases {len(index['hazards']['diseases'])}, poisons {len(index['hazards']['poisons'])}")
        return 0
    if a.check:
        stale = []
        if not eco_path.is_file() or eco_path.read_text(encoding="utf-8").replace("\r\n", "\n") != new_eco:
            stale.append(ECOLOGY_FILE)
        if not idx_path.is_file() or idx_path.read_text(encoding="utf-8").replace("\r\n", "\n") != new_idx:
            stale.append(INDEX_FILE)
        if stale:
            print("build_design_index: stale: " + ", ".join(stale), file=sys.stderr)
            return 1
        print("build_design_index: current")
        return 0
    eco_path.write_text(new_eco, encoding="utf-8", newline="\n")
    idx_path.write_text(new_idx, encoding="utf-8", newline="\n")
    print(f"build_design_index: wrote {eco_path.name} ({len(rows)} rows) and {idx_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
