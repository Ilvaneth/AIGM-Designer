#!/usr/bin/env python3
"""
design_door.py — P1's door (plan item 25, "The door, the critics and the card"; docs/p1-build-13.md, Part 13b).

The door is the script between the writer's output and the phase's record: `registry.py merge --phase P1` asks it
about every unit of a birth whose P1 the script rolled (a foundation, an identity, rolled names, a promise ledger).
A legacy birth is checked as it always was. A refusal is one line per fault and names what is wrong; a line the
conductor reads never carries a secret row, a secret-stock name or a sentence of dm-only prose (those go to
design/dm-only/door-log.json, and the conductor sees a count).

  7   the rolls are the writer's ground: three signatures (slot, home, rolled rows as design.json#identity holds
      them), the trope-break entities exactly the rolled ones with their ties, the premise with the rolled question
      ids; the preroll's records (foundation, identity, the ledger's script-built part, naming.json) are sealed
  8   the final set holds no conflict: every row P1 stands on, public and secret, tokens included
  9   every proper noun is pooled: a signature's name is one of its slot's candidates; a person's or god's given name
      is from its language's stock; a place-like name is from a stock or built by pattern 6 or 7 from pooled parts; a
      secret entity is named from the secret stock; in prose a capitalised word that opens nothing belongs to a
      pooled or registered name or to naming.yaml#rules.capitalised_common
  10  each signature's `appears` notes are structured, name a later phase and cover every floor its tables promised
      (design_promises.sync enters them into the ledger, source `note`)
  11  no secret in the public file: no secret row's id or statement, no secret-stock name; the premise's
      spoiler-safe abstract is the archetype's class and nothing else
  12  a lexical "never" pattern (forbidden.yaml's one row) is scanned in the public prose
  21a the premise's question is one sentence per contest, each at most QUESTION_WORDS words
  21d the premise's pitch is three sentences, each at most PITCH_WORDS words, the same text as the prose file's
      pitch section
  20a every premise, signature and break row matches the script's frame (design_frame.py) in every field the rolls
      set: a changed or missing frame field is refused by its name
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import campaign_dir, design_dir, dm_only_dir, now_iso, read_json, stamp_meta, write_json_atomic  # noqa: E402

SEAL = "p1_seal"                 # design.json#p1_seal: the hashes of what the preroll wrote
SLOTS = ("people", "institution", "phenomenon")
ROLLED = {"people": ("lineage", "visible", "behaving", "attitude"), "institution": ("form", "practice", "sign", "power"),
          "phenomenon": ("rule", "sign", "limit", "user")}
SIGNATURE_TABLES = {"people": ("people_lineage", "people_trait", "people_attitude"),
                    "institution": ("institution_form", "institution_practice", "institution_sign", "institution_power"),
                    "phenomenon": ("phenomenon_rule", "phenomenon_sign", "phenomenon_limit", "phenomenon_user")}
PLACE_STOCKS = {"settlement": ("places",), "region": ("regions",), "district": ("buildings", "places"),
                "place": ("places", "inns", "buildings", "ships"), "site": ("sites", "places", "buildings")}
SCRIPT_SOURCES = ("hook", "override", "foundation", "concretise", "clue_stage", "clue")
# registry fields that hold no prose: ids, closed values, paths
NO_PROSE_KEYS = {"id", "type", "file", "secrecy", "origin", "created_phase", "lang", "row", "tie", "home", "slot", "name", "aliases",
                 "status", "owner_phase", "reserved_by", "refs", "stamped", "rolled", "tensions", "signatures", "trope_breaks",
                 "kind", "phase", "dm_only", "secret_class", "secret_class_tr", "naming_languages",
                 "hook"}     # build item 18e: an `appears` note's hook is a table's own sentence, checked word for word
WORD = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z][A-Za-z'’]*(?![0-9_])")
# build item 21a (the fourth test birth: each contest's question ran to about a hundred words and the card could not be
# read): the prompt asks one sentence per contest of about thirty-five words; the door refuses one past this
QUESTION_WORDS = 45
# build item 21d (the fourth test birth's pitch ran two sentences past sixty words): three sentences, each at most this
PITCH_WORDS = 40
PITCH_SENTENCES = 3
OPENERS = ".!?:;|—–#>"


# build item 18a, the one-way rule at the door: a writer's structured field that fills a story slot names a story or
# a stage piece, never texture. (entity type, dotted field path) → the slot it fills; build item 18e names the fields
# (the clues' places, the god pin's piece). A list is judged item by item; an absent or empty field is not judged.
STORY_FIELDS: dict = {("premise", "dm_only.clues.piece"): "clue_place", ("premise", "dm_only.pinned.piece"): "secret_pin"}   # 18e


def _field_values(node, path: str) -> list:
    head, _, rest = path.partition(".")
    if isinstance(node, list):
        return [v for item in node for v in _field_values(item, path)]
    if not isinstance(node, dict) or head not in node:
        return []
    value = node[head]
    if rest:
        return _field_values(value, rest)
    return [v for v in (value if isinstance(value, list) else [value]) if v not in (None, "")]


def story_field_errors(eid: str, row: dict, fields: dict | None = None) -> list[str]:
    """A field that fills a story slot with a texture piece, one line each."""
    import design_arbiter as arb
    errs = []
    for (etype, path), slot in (STORY_FIELDS if fields is None else fields).items():
        if row.get("type") != etype:
            continue
        for piece in _field_values(row, path):
            if not arb.slot_accepts(slot, piece):
                errs.append(f"{eid}: `{path}` names {piece!r}, a {arb.piece_layer(piece) or 'layerless'} piece, where "
                            f"{arb.STORY_SLOTS[slot]} takes a story or a stage piece")
    return errs


def applies(manifest: dict, phase: str) -> bool:
    """A birth whose P1 the script rolled: a foundation, an identity, a ledger and a seal. A legacy birth has none."""
    return phase == "P1" and all(isinstance(manifest.get(k), (dict, list)) for k in ("foundation", "identity", "promises", SEAL))


def door_for(campaign: str, canonical: dict, incoming: list, phase: str):
    """The door of a merge: P1's (this module) or P2's (design_cosmos_door.py, build item 22c); None for a legacy
    birth's phase."""
    m = dm.load(campaign)
    if applies(m, phase):
        return Door(campaign, canonical, incoming)
    if phase == "P2":
        import design_cosmos_door as cd
        if cd.applies(m):
            return cd.CosmosDoor(campaign, canonical, incoming)
    return None


def seal_p2(campaign: str) -> dict:
    """P2's preroll: stamp the cosmos's seal (design_cosmos_door.py)."""
    import design_cosmos_door as cd
    return cd.seal(campaign)


# ── 7. the seal ──────────────────────────────────────────────────────────────────────────────────────────────

def _hash(node) -> str:
    return hashlib.sha256(json.dumps(node, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]


def seal_of(campaign: str, manifest: dict | None = None) -> dict:
    """The hashes of what the preroll wrote and no agent may change: the foundation, the identity, the script-built
    part of both ledgers (ids, due phases and sentences; a verdict is no change), naming.json's languages, calendar
    and candidates (`assignments` is P3's to fill)."""
    m = manifest or dm.load(campaign)
    naming = read_json(design_dir(campaign) / "naming.json") or {}
    secret = (read_json(dm_only_dir(campaign) / "promises.json") or {}).get("promises") or []
    built = lambda rows: sorted((p["id"], p["due"], p["text"]) for p in rows if p.get("source") in SCRIPT_SOURCES)
    return {"foundation": _hash(m.get("foundation")), "identity": _hash(m.get("identity")),
            "promises": _hash([built(m.get("promises") or []), built(secret)]),
            "naming": _hash({k: naming.get(k) for k in ("languages", "calendar", "candidates")})}


def seal(campaign: str) -> dict:
    """P1's preroll (and the owner's reroll of a candidate slot): stamp the seal."""
    m = dm.load(campaign)
    m[SEAL] = seal_of(campaign, m)
    dm.save(campaign, m, "design_door.py seal")
    return m[SEAL]


def seal_errors(campaign: str, manifest: dict) -> list[str]:
    now, was = seal_of(campaign, manifest), manifest.get(SEAL) or {}
    names = {"foundation": "design.json#foundation", "identity": "design.json#identity",
             "promises": "the promise ledger's script-built part", "naming": "design/naming.json"}
    return [f"{names[k]} differs from what the preroll stamped; the rolls are the writer's ground, never its choice "
            "(restore it: rerun the preroll, or undo the edit)" for k in names if now[k] != was.get(k)]


# ── 8. the final set holds no conflict ───────────────────────────────────────────────────────────────────────

def conflict_errors(campaign: str) -> tuple[list[str], list[dict]]:
    """(the refusal lines, the dm-only detail). A pair that involves a secret row is said only as "a conflict in the
    secret layer"."""
    import design_arbiter as arb
    import design_dice as dd
    rolled, tokens = dd.prior_rolls(campaign, "P2", with_tokens=True)
    m = dm.load(campaign)
    recs = list(m.get("dice_log") or []) + list((read_json(dm_only_dir(campaign) / "dice-log.json") or {}).get("rolls") or [])
    exempt = {frozenset((r.get("row_id"), x)) for r in recs for x in r.get("conflict_exempt") or []}
    pairs = arb.conflicting_pairs(list(rolled), tokens=set(tokens), exempt=exempt)
    lines, hidden = [], []
    for a, b in pairs:
        if rolled.get(a) or rolled.get(b) or tokens.get(a) or tokens.get(b):
            hidden.append({"kind": "conflict", "pair": [a, b]})
        else:
            lines.append(f"the rolled rows {a} and {b} conflict; the final set of P1 holds no conflicting pair (a table fault: report it)")
    if hidden:
        lines.append("a conflict in the secret layer (the pair is in the dm-only door log)")
    return lines, hidden


# ── 9. every proper noun is pooled ───────────────────────────────────────────────────────────────────────────

class Names:
    """The campaign's pooled names: the public stocks, the candidates, the calendar; the secret stock apart."""

    def __init__(self, campaign: str | None, naming: dict | None = None, pool: dict | None = None, secret_pool: dict | None = None):
        import design_names as dn
        self.naming = naming if naming is not None else read_json(dn.naming_path(campaign)) or {}
        self.pool = pool if pool is not None else dn.load_pool(campaign) or {}
        self.secret_pool = secret_pool if secret_pool is not None else dn.load_secret(campaign) or {}
        self.rules = dt.load("naming.yaml")["rules"]
        words = dt.load("naming.yaml")["words"]
        self.building_words = list(words["building_words"])
        roots = {r["root"]: r for r in dn.lexicon_roots()}
        self.natural_tails = {r for L in (self.naming.get("languages") or {}).values() for r in L.get("roots") or []
                              if dn.slot_fits(roots[r], "tail")}
        stock = lambda key: {e["name"] for L in (self.pool.get("languages") or {}).values() for e in L.get(key, [])}
        self.stocks = {key: stock(key) for key in ("person", "god", "places", "regions", "inns", "buildings", "ships", "epithets", "sites")}
        self.calendar = {e["name"] for v in (self.pool.get("calendar") or {}).values() for e in v}
        self.candidates = {slot: [c["name"] for c in s.get("names", [])] for slot, s in (self.naming.get("candidates") or {}).items()}
        sec = lambda *keys: {e["name"] for L in (self.secret_pool.get("languages") or {}).values() for k in keys for e in L.get(k, [])}
        self.secret = {"person": sec("person"), "god": sec("god"), "place": sec("place", "site")}

    def public(self) -> set:
        out = set(self.calendar)
        for names in self.stocks.values():
            out |= names
        for names in self.candidates.values():
            out |= set(names)
        return out

    def secret_all(self) -> set:
        return set().union(*self.secret.values())

    def composed(self, name: str, secret: bool = False) -> bool:
        """Pattern 6 (`<a pooled person name>'s <a building word or a natural tail>`) or pattern 7 (`<a building
        word> of <a pooled god name>`), from pooled parts."""
        persons = self.secret["person"] if secret else self.stocks["person"]
        gods = self.secret["god"] if secret else self.stocks["god"]
        m = re.fullmatch(r"([A-Z][a-z]+)['’]s ([A-Za-z]+)", name)
        if m and m.group(1) in persons and (m.group(2) in self.building_words or m.group(2).lower() in self.natural_tails):
            return True
        m = re.fullmatch(r"([A-Z][a-z]+) of ([A-Z][a-z]+)", name)
        return bool(m and m.group(1) in self.building_words and m.group(2) in gods)


def bare(name: str) -> str:
    return re.sub(r"^[Tt]he ", "", str(name or "").strip())


_PLANES: list | None = None


def plane_names() -> list[str]:
    """The planes' names a P1 text may not carry (build item 19a: the thin place's plane is chosen at P2): every
    baseline plane's label of planes.yaml and its local name, but the Material Plane and the demiplanes."""
    global _PLANES
    if _PLANES is None:
        out = []
        for r in dt.rows("planes.yaml#baseline"):
            if r["id"] in ("baseline_material", "baseline_demiplane"):
                continue
            m = re.match(r"^(?:The )?(.*?)(?: \((?:the )?(.*)\))?$", str(r.get("label") or ""))
            out += [x for x in (m.group(1), m.group(2)) if x]
        _PLANES = out
    return _PLANES


def planes_in(text: str) -> list[tuple[int, str]]:
    """(line, name) of every plane's name in a text: a name with `Plane` in any case, every other as a name is written
    (capitalised: "the grey country" and "what in the nine hells" are ordinary words)."""
    found = []
    for no, line in enumerate(str(text or "").split("\n"), 1):
        for name in plane_names():
            flags = re.IGNORECASE if "Plane" in name else 0
            if re.search(r"(?<![\w])" + re.escape(name) + r"(?![\w])", line, flags):
                found.append((no, name))
    return found


def question_sentences(text: str) -> list[tuple[str, int]]:
    """(sentence, words) for each question a premise's `question` holds: a sentence ends at its question mark."""
    parts = [p for p in re.split(r"(?<=\?)\s+", str(text or "").strip()) if p.strip()]
    return [(p, len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", p))) for p in parts]


def words_in(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", str(text or "")))


def sentences(text: str) -> list[str]:
    """A text's sentences (build item 21d): a sentence ends at `.`, `?` or `!` followed by a space or the end; inside
    quotes (straight or curly) a stop ends nothing, unless the closing quote follows it directly and a space or the end
    follows the quote: then the sentence ends after the quote (a pitch that quotes its question)."""
    text = " ".join(str(text or "").split())
    out, cur, quoted = [], [], False
    for i, c in enumerate(text):
        cur.append(c)
        nxt = text[i + 1] if i + 1 < len(text) else " "
        if c in "“”\"":
            opens = c == "“" or (c == '"' and not quoted)
            if quoted and not opens and i > 0 and text[i - 1] in ".?!" and nxt == " ":
                out.append("".join(cur).strip())
                cur = []
            quoted = opens
            continue
        if c in ".?!" and not quoted and nxt == " " and not (i + 1 < len(text) and text[i + 1] in ".?!"):
            out.append("".join(cur).strip())
            cur = []
    rest = "".join(cur).strip()
    if rest:
        out.append(rest)
    return [s for s in out if s]


def pitch_errors(eid: str, pitch) -> list[str]:
    """Three sentences, each at most PITCH_WORDS words (build item 21d); the sentence named by its number and count."""
    said = sentences(pitch)
    errs = []
    if len(said) != PITCH_SENTENCES:
        errs.append(f"{eid}: `pitch` holds {len(said)} sentence(s); it is three short sentences (a threat with a face, the "
                    "question, the first session's task), the land's breaks and the costs said elsewhere")
    for n, s in enumerate(said, 1):
        w = words_in(s)
        if w > PITCH_WORDS:
            errs.append(f"{eid}: `pitch` sentence {n} has {w} words; each is at most about thirty (refused past {PITCH_WORDS})")
    return errs


def plain(text: str) -> str:
    """A text without its `*` / `_` emphasis, whitespace folded (build item 21d: a pitch set in italics is the same pitch)."""
    text = re.sub(r"\*+", "", str(text or ""))
    text = re.sub(r"(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])", "", text)
    return " ".join(text.split())


def template_guidance(heading: str) -> set[str]:
    """The guidance lines the premise template sets under a heading (its whole-line italic instructions), plain."""
    path = Path(__file__).resolve().parent.parent / "templates" / "design" / "premise.md"
    lines = path.read_text(encoding="utf-8").split("\n") if path.is_file() else []
    start = next((i for i, l in enumerate(lines) if l.strip().lower() == heading.lower()), None)
    out = set()
    for l in lines[start + 1:] if start is not None else []:
        if l.lstrip().startswith("#"):
            break
        if re.fullmatch(r"\s*\*[^*].*\*\s*", l):
            out.add(plain(l))
    return out


def section_text(text: str, heading: str) -> str | None:
    """The prose under a `###` heading up to the next heading, plain (comments, the template's own guidance line and
    emphasis taken out, whitespace folded); None if absent."""
    lines = str(text or "").split("\n")
    start = next((i for i, l in enumerate(lines) if l.strip().lower() == heading.lower()), None)
    if start is None:
        return None
    guide = template_guidance(heading)
    body = []
    for l in lines[start + 1:]:
        if l.lstrip().startswith("#"):
            break
        if plain(l) not in guide:
            body.append(l)
    return plain(re.sub(r"<!--.*?-->", " ", "\n".join(body), flags=re.S))


def later_floor(phase) -> bool:
    """A floor after P1 a signature's note may name: P2-P9, or `play` (build item 18f: the phenomenon's play hook,
    the test birth's P1-1 #4; a play promise closes no phase's gate, build item 12b)."""
    return phase == "play" or (phase in dm.PHASES and dm.PHASES.index(phase) > 1)


def name_errors(eid: str, row: dict, names: Names, identity: dict) -> list[str]:
    """Section 9, the registry names. The refusal of a secret entity names no stock: it says where to look."""
    import design_names as dn
    etype, name = row.get("type"), str(row.get("name") or "").strip()
    secret = row.get("secrecy") == "secret"
    if not name:
        return []
    if etype == "signature":
        slot = row.get("slot")
        if slot in SLOTS and name not in names.candidates.get(slot, []):
            return [f"{eid}: the {slot} signature's name {name!r} is none of its four candidates (design/naming.json#candidates.{slot}); "
                    "take one of them as it stands"]
        return []
    if etype in ("npc", "god"):
        given, kind = dn.given_of(name), "god" if etype == "god" else "person"
        if secret:
            if given in names.stocks[kind] or given not in names.secret[kind]:
                return [f"{eid}: a secret {etype} is named from the secret stock (run `design_names.py -c CAMP secret --lang L --kind {kind}`), "
                        "never from a public list and never invented"]
            return []
        if given in names.secret[kind]:
            return [f"{eid}: a public entity may not take a name of the secret stock; take the next unused name from the list in your prompt"]
        if given not in names.stocks[kind]:
            return [f"{eid}: the given name {given!r} is not on a rolled {kind} list; names are rolled, never invented"]
        return []
    if etype in PLACE_STOCKS:
        if secret:
            if not (name in names.secret["place"] or bare(name) in names.secret["place"] or names.composed(name, secret=True)):
                return [f"{eid}: a secret {etype} is named from the secret stock (run `design_names.py -c CAMP secret --lang L --kind place|site`)"]
            return []
        allowed = set().union(*(names.stocks[k] for k in PLACE_STOCKS[etype]))
        if name in names.secret_all() or bare(name) in names.secret_all():
            return [f"{eid}: a public entity may not take a name of the secret stock"]
        if not (name in allowed or f"the {bare(name)}" in allowed or f"The {bare(name)}" in allowed or names.composed(name)):
            return [f"{eid}: the {etype} name {name!r} is in no stock of its kind ({', '.join(PLACE_STOCKS[etype])}) and is not built from "
                    "pooled parts (`<pooled person>'s <building word or natural tail>`, `<building word> of <pooled god>`); "
                    "take a name from the stock in your prompt"]
    return []


def strip_markup(text: str) -> str:
    """Prose without what carries no prose: the front matter, comments, code spans, wiki-links, urls."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = "\n" * parts[1].count("\n") + parts[2]       # the line numbers stay the file's
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\[\[[^\]\n]*\]\]", " ", text)
    return re.sub(r"https?://\S+", " ", text)


def stray_capitals(text: str, known: set, common: set) -> list[tuple[int, str]]:
    """(line, word) for every capitalised word that opens no sentence, heading, list item or table cell and belongs
    to no known name (multi-word names matched whole; a person's or a god's single words stand alone too) and is not
    on the closed list of capitalised common words."""
    known = set(known) | {c for c in common if " " in c}       # a term of several words is matched whole, like a name
    whole = sorted((n for n in known if " " in n), key=len, reverse=True)
    single = {n for n in known if " " not in n}
    out = []
    for no, line in enumerate(strip_markup(text).split("\n"), 1):
        for n in whole:
            if n in line:
                line = line.replace(n, " " * len(n))
            alt = n[0].upper() + n[1:]              # `the Thorn March` opens a sentence as `The Thorn March`
            if alt != n and alt in line:
                line = line.replace(alt, " " * len(alt))
        for m in WORD.finditer(line):
            word = re.sub(r"['’]s?$", "", m.group(0))
            if not word[:1].isupper() or word in single or word in common:
                continue
            before = line[:m.start()].rstrip(" \t*_\"“‘'’([{")
            if not before or before[-1] in OPENERS or re.fullmatch(r"\s*(?:[-*+]|\d+[.)])", before) or re.search(r"(?:^|\s)[-–—]$", before):
                continue
            out.append((no, word))
    return out


def prose_strings(node, path: str = "") -> list[tuple[str, str]]:
    """(field path, text) for the prose a public registry row carries (its dm_only layer apart)."""
    if isinstance(node, str):
        return [(path, node)]
    if isinstance(node, dict):
        return [x for k, v in node.items() if k not in NO_PROSE_KEYS for x in prose_strings(v, f"{path}.{k}" if path else str(k))]
    if isinstance(node, list):
        return [x for i, v in enumerate(node) for x in prose_strings(v, f"{path}[{i}]")]
    return []


# ── a signature's rolled ground (module functions: the frame builds on them too, build item 20a) ─────────────

def home_id_of(identity: dict, foundation: dict, slot: str) -> str:
    """A signature's home as an id: the lifeline's row (or the new-people scar), the institution's contest and
    role, the ruin source's row (or the break)."""
    ident, f = identity[slot], foundation
    if slot == "people":
        return f["lifeline"]["id"] if ident["home"] == "lifeline" else ident["home"]
    if slot == "institution":
        return f"{f['contests'][0]['id']}.{ident['role']}"
    return f["ruin_source"] if ident["home"] == "ruin_source" else "break"


def rolled_of_identity(identity: dict, slot: str) -> dict:
    ident = identity[slot]
    if slot == "people":
        return {"lineage": ident["lineage"], "visible": ident["traits"]["visible"], "behaving": ident["traits"]["behaving"], "attitude": ident["attitude"]}
    return {k: ident[k] for k in ROLLED[slot]}


def hooks_by_floor_of(identity: dict, slot: str) -> dict:
    """The later floors a signature's tables promised, each with the hooks that promise it (W4, build item 18e: an
    `appears` note restates one of them)."""
    import design_promises as dp
    out: dict = {}
    for sub in SIGNATURE_TABLES[slot]:
        ref = f"signatures.yaml#{sub}"
        for rid in rolled_of_identity(identity, slot).values():
            row = dt.row(ref, rid)
            for h in dp.hooks_of(ref, row) if row else []:
                if later_floor(h["phase"]):
                    out.setdefault(h["phase"], set()).add(str(h["must"]))
    return out


# ── the door ─────────────────────────────────────────────────────────────────────────────────────────────────

class Door:
    """One merge's door. `whole` are the faults of the whole phase (the seal, a conflict): every unit is refused
    with them. `unit_errors` are a unit's own."""

    def __init__(self, campaign: str, canonical: dict, incoming: list[tuple[str, dict]]):
        import design_identity as di  # noqa: F401  (the tables it reads are loaded once)
        self.campaign = campaign
        self.root = campaign_dir(campaign)
        self.m = dm.load(campaign)
        self.identity, self.foundation = self.m["identity"], self.m["foundation"]
        self.rows = dict(canonical.get("entities") or {})
        self.rows.update(dict(incoming))
        self.names = Names(campaign)
        self.hidden: list[dict] = []
        log = read_json(dm_only_dir(campaign) / "dice-log.json") or {}
        self.secret_identity = log.get("identity") or {}
        attempt = int((self.m["phases"].get("P1") or {}).get("attempt") or 1)
        self.secret_rows = [dt.row(r["table"], r["row_id"]) for r in log.get("rolls") or []
                            if r.get("phase") == "P1" and int(r.get("attempt") or 1) == attempt and r.get("row_id") and ".yaml" in str(r.get("table"))]
        self.secret_rows = [r for r in self.secret_rows if r]
        self.common = set(dt.load("naming.yaml")["rules"]["capitalised_common"])
        persons = [str(r.get("name")) for r in self.rows.values() if r.get("type") in ("npc", "god", "pc") and r.get("name")]
        public_rows = [r for r in self.rows.values() if r.get("secrecy") != "secret"]
        self.known_public = self.names.public() | {str(n) for r in public_rows for n in [r.get("name")] + list(r.get("aliases") or []) if n}
        self.known_public |= {w for n in self.names.stocks["person"] | self.names.stocks["god"] for w in [n]}
        self.known_public |= {w for n in persons for w in n.split() if w[:1].isupper()}
        self.known_public |= {bare(n) for n in list(self.known_public)}
        labels = {str(L.get("label")) for L in (self.names.naming.get("languages") or {}).values()}
        self.known_public |= {n for n in labels if n}
        self.known_all = self.known_public | self.names.secret_all() | {str(r.get("name")) for r in self.rows.values() if r.get("name")}
        self.known_all |= {bare(n) for n in list(self.known_all)}
        self.whole, hidden = conflict_errors(campaign)
        self.hidden += hidden
        self.whole = seal_errors(campaign, self.m) + self.whole
        import design_frame as dfr
        self.frame = dfr.build(campaign, self.m)          # build item 20a: the rows' rolled fields, as the script wrote them

    # 7
    def home_id(self, slot: str) -> str:
        return home_id_of(self.identity, self.foundation, slot)

    def rolled_of(self, slot: str) -> dict:
        return rolled_of_identity(self.identity, slot)

    def hooks_by_floor(self, slot: str) -> dict:
        return hooks_by_floor_of(self.identity, slot)

    def floors_of(self, slot: str) -> list[str]:
        """The later floors a signature's tables promised: the phases of its rolled rows' hooks."""
        return sorted(self.hooks_by_floor(slot))

    def signature_errors(self, eid: str, row: dict) -> list[str]:
        slot = row.get("slot")
        if slot not in SLOTS:
            return [f"{eid}: a signature names its slot (`slot`: people, institution or phenomenon)"]
        errs = []
        if row.get("home") != self.home_id(slot):
            errs.append(f"{eid}: `home` must be {self.home_id(slot)!r}, the {slot} signature's home in design.json#identity")
        if row.get("rolled") != self.rolled_of(slot):
            errs.append(f"{eid}: `rolled` must hold the {slot} signature's rolled rows as design.json#identity.{slot} has them "
                        f"({', '.join(ROLLED[slot])}); the rolls are the writer's ground, never its choice")
        notes = row.get("appears")
        bad = [n for n in notes or [] if not (isinstance(n, dict) and later_floor(n.get("phase"))
                                                and isinstance(n.get("text"), str) and n["text"].strip())]
        if not isinstance(notes, list) or bad:
            errs.append(f"{eid}: `appears` is a list of {{phase, hook, text}} notes, each naming a phase after P1 (or `play`) and saying where the signature shows there")
        else:
            hooks = self.hooks_by_floor(slot)
            missing = [p for p in sorted(hooks) if p not in {n["phase"] for n in notes}]
            if missing:
                errs.append(f"{eid}: no `appears` note for {', '.join(missing)}; the signature's tables promised those floors, one note each")
            for n in notes:          # W4 (build item 18e): the note restates its table's hook; the promise binds the hook
                if n["phase"] in hooks and n.get("hook") not in hooks[n["phase"]]:
                    errs.append(f"{eid}: the `appears` note for {n['phase']} names no hook its tables gave that floor (`hook` restates one, word for word)")
        dm_only = row.get("dm_only") or {}
        if dm_only.get("true_rule") and dm_only.get("serves_clue") not in (1, 2, 3):
            errs.append(f"{eid}: a signature's hidden truth exists only as the medium of a stage's clue: `dm_only.serves_clue` names the stage (1, 2 or 3)")
        return errs

    def break_errors(self, eid: str, row: dict) -> list[str]:
        rolled = {b["id"]: b for b in self.identity["trope_breaks"]}
        if row.get("row") not in rolled:
            return [f"{eid}: `row` {row.get('row')!r} is no trope break this campaign rolled ({', '.join(rolled)})"]
        if row.get("tie") != rolled[row["row"]]["tie"]:
            return [f"{eid}: `tie` must be {rolled[row['row']]['tie']!r}, the tie recorded for {row['row']}"]
        return []

    def premise_errors(self, eid: str, row: dict) -> list[str]:
        errs = []
        want = [q["id"] for q in self.identity["questions"]]
        if list(row.get("tensions") or []) != want:
            errs.append(f"{eid}: `tensions` must be the rolled question id(s) {want}")
        errs += pitch_errors(eid, row.get("pitch"))          # build item 21d
        # build item 22c (the audit): a pinned god is named from the secret stock alone; it is that god's true name, and P2
        # gives the god its public face like every god's
        pinned = ((row.get("dm_only") or {}).get("pinned") or {}).get("god")
        if pinned:
            import design_names as dn
            if dn.given_of(str(pinned)) not in self.names.secret["god"]:
                errs.append(f"{eid}: `dm_only.pinned.god` is a god name of the secret stock (run `design_names.py -c CAMP secret "
                            "--lang L --kind god`); it becomes the god's true name, never a public one")
        contests = [q.get("contest") for q in self.identity["questions"]]
        for n, (_, words) in enumerate(question_sentences(row.get("question"))):
            if words > QUESTION_WORDS:
                who = contests[n] if n < len(contests) else f"question {n + 1}"
                errs.append(f"{eid}: `question` holds a question of {words} words for {who}; one sentence per contest, at most about "
                            f"thirty-five words (refused past {QUESTION_WORDS}): say the costs in the sides' lines and the stakes")
        sigs = [r for r in self.rows.values() if r.get("type") == "signature"]
        for slot in SLOTS:
            n = sum(1 for r in sigs if r.get("slot") == slot)
            if n != 1:
                errs.append(f"{eid}: the premise needs exactly one {slot} signature entity beside it ({n} found)")
        have = [r.get("row") for r in self.rows.values() if r.get("type") == "break"]
        for b in self.identity["trope_breaks"]:
            if have.count(b["id"]) != 1:
                errs.append(f"{eid}: the rolled trope break {b['id']} needs exactly one break entity ({have.count(b['id'])} found)")
        # 11: the spoiler-safe abstract is the twist's class and nothing else (build item 20a: read in the twist table,
        # where every twist stands; the archetype table lacks twist_greater_power, whose class the door then refused)
        arch = dt.row("secrets.yaml#twist", (self.secret_identity.get("secret") or {}).get("twist") or "")
        if arch and row.get("secret_class") != arch.get("hides_in"):
            errs.append(f"{eid}: `secret_class` is the twist's class as its row gives it (`hides_in`) and nothing else")
        elif not arch and (self.secret_identity.get("secret") or {}).get("facts") and row.get("secret_class") != "threat":
            errs.append(f"{eid}: `secret_class` is `threat` when no twist was rolled (build item 18e)")
        return errs

    # 9 (prose), 11, 12
    def leak_errors(self, where: str, text: str) -> list[str]:
        """No secret row's id or statement and no secret-stock name in a public text. The line names the kind, never
        the row or the name. (A row's label is ordinary words a public sentence may carry: the statement is the row's
        own sentence.)"""
        errs = []
        low = text.lower()
        ids = sum(1 for r in self.secret_rows if re.search(r"(?<![a-z0-9_])" + re.escape(r["id"]) + r"(?![a-z0-9_])", low))
        said = sum(1 for r in self.secret_rows for key in ("statement", "rule", "cause")
                   if isinstance(r.get(key), str) and len(r[key]) >= 24 and r[key].lower() in low)
        named = sum(1 for n in self.names.secret_all() if re.search(r"(?<![\w'])" + re.escape(n) + r"(?![\w])", text))
        if ids:
            errs.append(f"{where}: names {ids} secretly rolled row(s) by id; a secret roll stays in dm-only")
        if said:
            errs.append(f"{where}: repeats {said} sentence(s) of a secretly rolled row; the secret layer is written in the mirror alone")
        if named:
            errs.append(f"{where}: carries {named} name(s) of the secret stock; a secret entity's name never stands in a public text")
        return errs

    def never_warnings(self, where: str, text: str) -> list[str]:
        out = []
        for row in dt.rows("forbidden.yaml"):
            for pat in (row.get("lexical") or {}).get("en") or []:
                if re.search(pat, text, flags=re.I):
                    out.append(f"{where}: reads like {row['id']} ({row['label']}); no people is evil by birth")
        return out

    def prose_errors(self, uid: str, frag: dict, rows: list[tuple[str, dict]]) -> tuple[list[str], list[str]]:
        errs, warns = [], []

        def file_of(key):
            v = frag.get(key)
            rel = v.get("file") if isinstance(v, dict) else v if isinstance(v, str) else None
            f = self.root / str(rel) if rel else None
            return (rel, f.read_text(encoding="utf-8", errors="replace")) if f is not None and f.is_file() else (None, None)
        rel, text = file_of("prose")
        if text is not None and not str(rel).startswith("design/dm-only/"):
            for no, word in stray_capitals(text, self.known_public, self.common)[:12]:
                errs.append(f"{uid}: {rel} line {no}: the capitalised word {word!r} is no pooled or registered name; write a common "
                            "noun in lower case, or take a name from the pools")
            errs += self.leak_errors(f"{uid}: {rel}", text)
            warns += self.never_warnings(f"{uid}: {rel}", text)
            for no, name in planes_in(text)[:6]:
                errs.append(f"{uid}: {rel} line {no}: names a plane ({name}); no plane is named at P1: the thin place's plane is chosen at P2")
            # build item 21d: the prose file's pitch and the premise row's `pitch` are one text
            said = section_text(text, "### The player pitch")
            for eid, row in rows:
                if row.get("type") == "premise" and said is not None and said != plain(row.get("pitch")):
                    errs.append(f"{eid}: the pitch in {rel} (its `### The player pitch` section) and the row's `pitch` differ; "
                                "they are the same three sentences")
        for eid, row in rows:
            if row.get("secrecy") == "secret":
                continue
            for path, value in prose_strings(row):
                for _, word in stray_capitals(value, self.known_public, self.common)[:4]:
                    errs.append(f"{eid}: field {path}: the capitalised word {word!r} is no pooled or registered name")
                for _, name in planes_in(value)[:2]:
                    errs.append(f"{eid}: field {path}: names a plane ({name}); no plane is named at P1: the thin place's plane is chosen at P2")
                errs += self.leak_errors(f"{eid}: field {path}", value)
        mrel, mtext = file_of("dm_only_prose")
        if mtext is not None:
            stray = stray_capitals(mtext, self.known_all, self.common)
            if stray:
                self.hidden.append({"kind": "capitalised", "unit": uid, "file": mrel, "words": [{"line": no, "word": w} for no, w in stray]})
                errs.append(f"{uid}: {len(stray)} capitalised word(s) in the dm-only prose are no pooled or registered name "
                            "(the words and their lines are in the dm-only door log)")
            planes = planes_in(mtext)
            if planes:          # build item 19a: the mirror names no plane either; the conductor sees a count
                self.hidden.append({"kind": "plane", "unit": uid, "file": mrel, "words": [{"line": no, "word": w} for no, w in planes]})
                errs.append(f"{uid}: the dm-only prose names {len(planes)} plane(s); no plane is named at P1: the thin place's "
                            "plane is chosen at P2 (the names and their lines are in the dm-only door log)")
        return errs, warns

    def unit_errors(self, uid: str, frag: dict, rows: list[tuple[str, dict]]) -> tuple[list[str], list[str]]:
        import design_frame as dfr
        errs = list(self.whole)
        for eid, row in rows:
            if self.frame is not None:
                errs += dfr.frame_errors(self.campaign, self.frame, eid, row, self.rows)
            if row.get("type") == "signature":
                errs += self.signature_errors(eid, row)
            elif row.get("type") == "break":
                errs += self.break_errors(eid, row)
            elif row.get("type") == "premise":
                errs += self.premise_errors(eid, row)
            errs += story_field_errors(eid, row)
            errs += name_errors(eid, row, self.names, self.identity)
        e2, warns = self.prose_errors(uid, frag, rows) if frag else ([], [])
        return errs + e2, warns

    def close(self) -> None:
        """What the conductor may not read goes to the dm-only door log."""
        if not self.hidden:
            return
        path = dm_only_dir(self.campaign) / "door-log.json"
        doc = read_json(path) or {"_meta": {"schema_version": 1, "campaign": self.campaign}, "entries": []}
        doc["entries"].append({"at": now_iso(), "phase": "P1", "found": self.hidden})
        stamp_meta(doc, self.campaign, "design_door.py")
        write_json_atomic(path, doc)
