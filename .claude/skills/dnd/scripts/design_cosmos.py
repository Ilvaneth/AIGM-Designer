#!/usr/bin/env python3
"""
design_cosmos.py — P2, the cosmos, rolled by script on the foundation (plan item 25, build item 22b;
docs/p2-build-22.md part 22b; docs/p2-tags.md S0-S7 and the rulings on the 22b questions).

`roll(R, dials, p1, pool=None)` makes every P2 draw through a designer Roller, in the threat's order; a later step
never changes an earlier record:

1. the type and the counts (public): the pantheon type (a P1 row that names a type forces it), the god count, the rank
   split inside the ranks' shares, the great gods (the dualist pantheon's two and two; else the band, raised to the
   floor the P1 rows name), the touched-plane count (the scale's band and the magic dial's modifier, never below 1);
2. the threat's seats (secret): the threat's god (`family_god`: a lesser or power seat), a god behind it (`power_god`:
   any seat), the ruin's god (public: a gods-family ruin seats a fallen lesser or power god; one god with the threat's
   when the threat is a god and the ruin the imprisoned or the departed god), at epic the threat's home plane (a god's
   is reserved here and bound after the pantheon to the outer plane of its public alignment);
3. the planes' seats (every draw secret): the planes P1 names, seated first and shared only when the count is short (the count rises to
   the smallest number that serves every naming row), then the free seats from the baseline, the moon among the
   candidates; their public records come at the end of step 4 (the planes P1 names first, the rest in the baseline's
   order), each with a deviation (never removed), a time rate, a way in and a cost;
4. the pantheon (public, except the seats): the presence, then per god its rank, one or two domains to the scale's
   coverage, an alignment from its first domain, a name and an epithet from the pool; the evil god at standard and
   epic; the pilgrim road's greater god; churches (a greater god's archetype, a line of the domain's church shape for
   the others); a connected web of relations (rel_mirror only in the secret record, with a pinned god); the one
   discoverable god story; where the dead go (one land when a touched plane is reachable by dying); each touched
   plane's keeper (an aligned power, else an SRD creature from the band's middle level to its top + 3);
5. the history (public, except the origin's true layer): the four seated events (the move, the villain's origin, the
   signature institution's founding, the ruin's fall), the ages (the first and the present in place, the ruin's age
   seated), the other events by type, exactly the scale's divergences, a memory per event;
6. magic (public): source, constraint, visibility, taboos, the regulator (three P1 rows override who and how strict),
   who gives the services, wild magic through the dial's gate;
7. the calendar (public), last: the fixed year (12 x 28, a seven-day week; month and day names from the pool), the
   climate among the palette's climates, the moon, the underground count, the festivals (one per greater god and one or
   two folk festivals), the start year and date from the move's time, the dated days inside the campaign's span.

The return is `(public, secret)`: the public half goes to design.json#cosmos, the secret half to
dm-only/dice-log.json#cosmos; the records themselves are on R. A legacy birth (a P1 with no foundation) rolls what its
records allow: no seats, no named planes, no seated events.
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_arbiter as arb  # noqa: E402
import design_tables as dt  # noqa: E402

P, PL, M, H, C = "pantheon.yaml#", "planes.yaml#", "magic.yaml#", "history.yaml#", "calendar.yaml#"
RANKS = ("greater", "lesser", "power")
EVIL = ("NE", "CE", "LE")
MOON = "moon"                                   # the moon's own touched seat (planes.yaml rules.moon_seat): no baseline row
MOON_ROW = "moon_is_a_plane"
GODS_RUINS = ("ruin_dead_god", "ruin_gods_quarrel", "ruin_departed_god", "ruin_imprisoned_god", "ruin_failed_apotheosis")
# the 22b ruling 2: the threat that is a god and the ruin of the imprisoned or the departed god are one god
ONE_GOD_RUINS = ("ruin_imprisoned_god", "ruin_departed_god")
# P1 rows that name one plane between them (the thin place; the two worlds' crossing is the rift: foundation merges)
SAME_PLANE = (("land_thin_place", "target_thin_place"), ("spine_two_worlds", "ruin_planar_rift"))
NOT_TOUCHED = ("baseline_material",)
CASTERS = "the casters themselves, each at their own price"
# the 22b ruling 10: the pantheon type's folk festival (claims.yaml#defaults festivals)
TYPE_FOLK = {"pantheon_dead_gods": ("fest_remembrance", "fest_lament"), "pantheon_silent_gods": ("fest_silence",),
             "pantheon_ancestor_gods": ("fest_remembrance",),
             "pantheon_animist": ("fest_harvest", "fest_thaw", "fest_first_frost", "fest_tide")}
# the 22b ruling 9: the SRD creature that keeps a plane no power keeps, by the index's habitats and types
PLANAR_HABITATS = ("planar_lower", "planar_upper", "planar_inner", "fey", "shadow")
ELEMENT_OF = {"baseline_air": "air", "baseline_earth": "earth", "baseline_fire": "fire", "baseline_water": "water"}
# the 22b audit: every SRD creature of an element (the mephits of two elements stand on both)
ELEMENT_CREATURES = {"fire": ("azer", "salamander", "magmin", "efreeti", "fire-elemental", "magma-mephit", "steam-mephit"),
                     "earth": ("xorn", "gargoyle", "earth-elemental", "dust-mephit"),
                     "air": ("invisible-stalker", "djinni", "air-elemental", "dust-mephit", "ice-mephit"),
                     "water": ("water-elemental", "steam-mephit", "ice-mephit")}
TIME_ROWS = ("time_just_now", "time_unfolding", "time_coming", "time_generation_ago")
REGULATOR_DEFAULTS = ("regulator_identity", "regulator_strictness")
# midwinter is the middle of the hard season: a climate's first season, except below ground, where it is the dark
HARD_SEASON = {"climate_underground": "dark"}
STRICTNESS = ("free", "loose", "strict", "strictest")


# ── the P1 records P2 stands on ────────────────────────────────────────────────────────────────────────────────

def load_p1(campaign: str) -> dict:
    """The approved P0 and P1 records: the foundation and the identity (design.json), the secret and the threat
    (dm-only/dice-log.json). A legacy birth holds none of them."""
    import design_manifest as dm
    from design_io import design_dir, dm_only_dir, read_json
    m = dm.load(campaign)
    log = read_json(dm_only_dir(campaign) / "dice-log.json") or {}
    canon = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities") or {}
    premise = next((r for r in canon.values() if r.get("type") == "premise"), None) or {}
    pinned = ((premise.get("dm_only") or {}).get("pinned") or {}).get("god")
    return {"foundation": m.get("foundation"), "identity": m.get("identity"), "secret": log.get("identity"),
            "threat": log.get("threat"), "naming": read_json(design_dir(campaign) / "naming.json"),
            "pinned_god": {"name": pinned, "premise": premise.get("id")} if pinned else None}


def p1_of(R1) -> dict:
    """The same records from an in-memory P1 Roller (the corpus)."""
    return {"foundation": R1.foundation, "identity": R1.identity, "secret": R1.identity_secret, "threat": R1.threat,
            "naming": R1.naming}


# ── small helpers ────────────────────────────────────────────────────────────────────────────────────────────

def die(R, label: str, n: int, secret: bool = False) -> int:
    """One face of a d`n` (1..n); a single option is recorded as fixed."""
    if n <= 1:
        rec = R._record(label, None)
        rec.update({"notation": "fixed", "raw": 1, "value": 1})
        R._keep(rec, secret)
        return 1
    return int(R.notation(label, f"d{n}", secret=secret)["raw"])


def choose(R, label: str, options: list, secret: bool = False):
    rec_n = die(R, label, len(options), secret)
    R.by_label[label]["value"] = options[rec_n - 1] if not isinstance(options[rec_n - 1], dict) else rec_n
    return options[rec_n - 1]


def weighted(R, label: str, options: list[str], weights: list[float], secret: bool = False) -> str:
    """One weighted draw among ids that are no table's rows (a plane P1 names, the moon among them): the record names
    the die over the options and the option drawn."""
    import design_dice as dd
    if len(options) == 1:
        die(R, label, 1, secret)
        R.by_label[label]["value"] = options[0]
        return options[0]
    rng = dd.derive(R.master, R.phase, "dice", label, R.attempt)
    picked = arb.pick(rng, [{"id": x} for x in options], weights)
    rec = R._record(label, None)
    rec.update({"notation": picked["notation"], "raw": picked["raw"], "value": picked["row_id"], "options": list(options)})
    R._keep(rec, secret)
    return picked["row_id"]


def forced_value(R, label: str, table: str, value, reason: str, secret: bool = False) -> dict:
    """A value an override sets that no table row is (the regulator's who, its strictness): forced, with its reason."""
    rec = R._record(label, table)
    rec.update({"notation": "forced", "raw": None, "row_id": None, "value": value, "forced_by": reason})
    R._keep(rec, secret)
    return rec


def between(R, label: str, lo: int, hi: int, secret: bool = False) -> int:
    """A value in [lo, hi] on one die; the record carries it."""
    lo, hi = int(lo), int(max(lo, hi))
    v = lo + die(R, label, hi - lo + 1, secret) - 1
    R.by_label[label]["value"] = v
    return v


def note(R, label: str, value, why: str, secret: bool = False, table: str | None = None, **extra) -> dict:
    """A record no die made: a value the rules derive (its reason on it)."""
    rec = R._record(label, table)
    rec.update({"notation": "derived", "raw": None, "value": value, "derived_from": why}, **extra)
    R._keep(rec, secret)
    return rec


def public_rows(R) -> list[str]:
    return [x for x, sec in R.ctx.rolled.items() if not sec]


@lru_cache(maxsize=2)
def _overriders_for(sig: tuple) -> dict:
    out = {}
    for name in dt.list_tables():
        for lst in dt.all_row_lists(dt.load(name)).values():
            for r in lst:
                if isinstance(r.get("overrides"), list) and r["overrides"]:
                    out[r["id"]] = r["overrides"]
    return out


def overrides_on(R, default: str) -> list[tuple[str, object]]:
    """(row, to) of every public rolled row that overrides `default` (claims.yaml#defaults), in the order rolled."""
    index = _overriders_for(dt._signature())
    return [(rid, o.get("to")) for rid in public_rows(R) for o in index.get(rid) or []
            if isinstance(o, dict) and o.get("default") == default]


def tagged(rec: dict, pairs) -> dict:
    """Mark a record with the overrides it applies (the promise ledger's `script:override_applied`)."""
    rec["overrides"] = [{"row": r, "default": d} for r, d in pairs]
    return rec


def band(value) -> tuple[int, int]:
    return dt.band(value)


def shift(value, by: int) -> list[int]:
    lo, hi = band(value)
    return [max(1, lo + by), max(1, hi + by)]


def rows_of(ref: str) -> dict:
    return {r["id"]: r for r in dt.rows(ref)}


# ── 1. the type and the counts ───────────────────────────────────────────────────────────────────────────────

def religious_roles(foundation: dict | None, identity: dict | None) -> int:
    """The seated roles of every contest whose archetype hint (after the breaks' merges) is religious."""
    if not foundation:
        return 0
    hints = (identity or {}).get("role_hints") or {}
    contests = {r["id"]: r for r in dt.rows_and_retired("foundation.yaml#contest")}
    n = 0
    for c in foundation.get("contests") or []:
        for k in c.get("roles") or []:
            hint = (hints.get(c["id"]) or {}).get(k, ((contests.get(c["id"]) or {}).get("roles", {}).get(k) or {}).get("hint"))
            n += hint == "religious"
    return n


def great_floor(R, foundation: dict | None, identity: dict | None) -> tuple[int, list[str]]:
    """The floor the P1 rows name for the great gods (claims.yaml combine: the count of distinct great gods the rows
    name; one per seated religious role, at least one among mortals, the unnamed god one of them)."""
    raisers = overrides_on(R, "great_gods_floor")
    if not raisers:
        return 0, []
    floor = 0
    for rid, to in raisers:
        if rid.startswith("contest_"):
            floor = max(floor, religious_roles(foundation, identity))
        elif isinstance(to, int):
            floor = max(floor, to)
        else:
            floor = max(floor, 1)
    return floor, [r for r, _ in raisers]


def split_options(count: int, sc_name: str, greater: int | None) -> list[tuple[int, int, int]]:
    """Every (greater, lesser, power) summing to `count` inside the ranks' share bands; the nearest ones outside them
    when none is inside (a forced greater count, a raised god count)."""
    shares = {r["id"].removeprefix("rank_"): band(r["share"][sc_name]) for r in dt.rows(P + "rank")}
    trips = [(g, l, count - g - l) for g in range(count + 1) for l in range(count + 1 - g)]
    if greater is not None:
        trips = [t for t in trips if t[0] == greater]

    def dist(t) -> int:
        return sum(max(0, shares[k][0] - v) + max(0, v - shares[k][1]) for k, v in zip(RANKS, t))
    best = min(dist(t) for t in trips)
    return [t for t in trips if dist(t) == best]


def roll_counts(R, dials: dict, sc: dict, p1: dict, out: dict) -> None:
    f, ident = p1.get("foundation"), p1.get("identity")
    types = [(r, to) for r, to in overrides_on(R, "pantheon_type") if dt.row(P + "type", str(to))]
    if types:
        rec = R.forced("pantheon_type", P + "type", types[0][1], f"override by {types[0][0]}")
        tagged(rec, [(r, "pantheon_type") for r, _ in types])
    else:
        R.table("pantheon_type", P + "type", avoid=False)
    narrowing = [(r, "pantheon_type") for r, to in overrides_on(R, "pantheon_type") if not dt.row(P + "type", str(to))]
    if narrowing:       # "the silent and dead gods leave the pool": the claims' clash applied it; the record says so
        rec = R.by_label["pantheon_type"]
        tagged(rec, [(o["row"], o["default"]) for o in rec.get("overrides") or []] + narrowing)
    ptype = R.row("pantheon_type")
    out["type"] = ptype
    dualist = dt.row(P + "type", ptype) or {}
    two = {o["default"]: o["to"] for o in dualist.get("overrides") or [] if o.get("default") in ("great_gods_count", "greater_gods_count")}

    gods = R.count("gods_count", sc["gods"])
    greater_fixed = int(two["greater_gods_count"]) if "greater_gods_count" in two else None
    trips = split_options(gods, dials["scale"], greater_fixed)
    g, l, p = trips[die(R, "rank_split", len(trips)) - 1]
    R.by_label["rank_split"]["value"] = {"greater": g, "lesser": l, "power": p}
    if greater_fixed is not None:
        R.by_label["rank_split"]["forced_greater"] = f"override by {ptype}"
        tagged(R.by_label["rank_split"], [(ptype, "greater_gods_count")])

    floor, raisers = great_floor(R, f, ident)
    if "great_gods_count" in two:
        great = int(two["great_gods_count"])
        rec = note(R, "great_gods_count", great, f"override by {ptype}: its two powers are the two great gods at every scale")
        tagged(rec, [(ptype, "great_gods_count")] + [(r, "great_gods_floor") for r in raisers])
    else:
        great = R.count("great_gods_count", sc["great_gods"])
        if great < floor:
            rec = R.by_label["great_gods_count"]
            rec["value"] = great = floor
            rec["raised_to_floor"] = f"the floor {floor}: " + ", ".join(raisers)
        if raisers:
            tagged(R.by_label["great_gods_count"], [(r, "great_gods_floor") for r in raisers])
    if g < great:                     # the greater count is never below the great gods': raised inside the god count
        take = great - g
        shares = {r["id"].removeprefix("rank_"): band(r["share"][dials["scale"]]) for r in dt.rows(P + "rank")}
        for key, lo_of in (("lesser", lambda: shares["lesser"][0]), ("power", lambda: shares["power"][0]),
                           ("lesser", lambda: 0), ("power", lambda: 0)):
            while take and {"lesser": l, "power": p}[key] > lo_of():
                if key == "lesser":
                    l -= 1
                else:
                    p -= 1
                g, take = g + 1, take - 1
        if take:                      # the god count itself is too small: it rises
            g += take
            R.by_label["gods_count"]["value"] = gods = g + l + p
            R.by_label["gods_count"]["raised_to_great"] = f"{great} great gods"
        R.by_label["rank_split"]["value"] = {"greater": g, "lesser": l, "power": p}
        R.by_label["rank_split"]["raised_to_great"] = f"the greater gods raised to the {great} great gods"
    out["counts"] = {"gods": gods, "greater": g, "lesser": l, "power": p, "great": great, "great_floor": floor}

    mod = int(((dt.dial_row("magic", dials.get("magic")) or {}).get("effects") or {}).get("planes_touched_modifier") or 0)
    out["planes_count"] = count = R.count("planes_touched_count", shift(sc["planes_touched"], mod))
    # the 22b ruling 6, in this step (the audit: no later step touches a record of this one): the count rises to the
    # fewest planes that serve every public P1 row naming one
    slots = named_slots(R, dials["scale"])
    need = min_new(slots, set())
    if need > count:
        rec = R.by_label["planes_touched_count"]
        rec["value"] = out["planes_count"] = need
        rec["raised_to_named"] = "the planes P1 names: " + ", ".join(r for s in slots for r in s["rows"])


# ── 2. the threat's seats ────────────────────────────────────────────────────────────────────────────────────

def god_slots(counts: dict) -> list[dict]:
    """The counted gods in order: the greater (the first `great` of them the great gods), the lesser, the powers."""
    out, n = [], 0
    for rank in RANKS:
        for _ in range(counts[rank]):
            n += 1
            out.append({"n": n, "rank": rank, "great": rank == "greater" and n <= counts["great"]})
    return out


def home_candidates(threat: dict | None) -> list[str]:
    """The baseline rows a threat's family is at home on (planes.yaml rules.home_of): a family id, a family by its
    creature, or (the god) the outer planes by alignment."""
    if not threat:
        return []
    fam = threat.get("family")
    creature = (threat.get("creature") or {}).get("index") or ((threat.get("creature") or {}).get("reskin") or {}).get("base")
    out = []
    for r in dt.rows(PL + "baseline"):
        for h in r.get("home_of") or []:
            if h == fam:
                out.append(r["id"])
            elif isinstance(h, dict) and h.get("family") == fam and (h.get("by") == "alignment" or creature in (h.get("creatures") or [])):
                out.append(r["id"])
    return list(dict.fromkeys(out))


def roll_seats(R, dials: dict, p1: dict, slots: list[dict], out: dict, secret: dict) -> None:
    f, threat, ident_secret = p1.get("foundation") or {}, p1.get("threat") or {}, p1.get("secret") or {}
    ruin = f.get("ruin_source")
    nongreat = [s for s in slots if s["rank"] in ("lesser", "power")]
    seats = {"threat_god": None, "power_god": None, "home_plane": None}
    ruin_god = None
    if ruin in GODS_RUINS:
        if nongreat:
            ruin_god = choose(R, "ruin_god", [s["n"] for s in nongreat])
            note_rec = R.by_label["ruin_god"]
            note_rec["derived_from"] = f"{ruin}: the ruin's god is a counted, fallen god without a church faction (lesser or power)"
    out["ruin_god"] = ruin_god
    if threat.get("family") == "family_god":
        if ruin_god is not None and ruin in ONE_GOD_RUINS:
            seats["threat_god"] = ruin_god
            note(R, "seat.threat_god", ruin_god, f"the threat is the god of {ruin}: one god", secret=True)
        else:
            opts = [s["n"] for s in nongreat if s["n"] != ruin_god] or [s["n"] for s in nongreat] or [s["n"] for s in slots]
            seats["threat_god"] = choose(R, "seat.threat_god", opts, secret=True)
    else:
        note(R, "seat.threat_god", None, "the threat is no god", secret=True)
    # every secret label stands in every birth, its value null when the fact does not hold (the audit: labels and
    # the secret count never vary with a secret fact)
    power = (ident_secret.get("secret") or {}).get("greater_power")
    if power and (dt.row("secrets.yaml#greater_power", power) or {}).get("god"):
        opts = [s["n"] for s in slots if s["n"] != seats["threat_god"]] or [s["n"] for s in slots]
        seats["power_god"] = choose(R, "seat.power_god", opts, secret=True)
    else:
        note(R, "seat.power_god", None, "no god stands behind the threat", secret=True)
    if dials["scale"] == "epic":
        # option (d) of the 22b audit: the home is a secret plane record, never a public seat; the god's home is the
        # outer plane of the alignment it rolls in public, bound after the pantheon
        if threat.get("family") == "family_god" and seats["threat_god"]:
            seats["home_by_alignment"] = True
            seats["home_fits"] = None
        else:
            seats["home_fits"] = home_candidates(threat) or None
        note(R, "seat.home_plane", "by_alignment" if seats.get("home_by_alignment") else seats["home_fits"],
             "the threat's home plane (planes.yaml rules.home_of), bound after the pantheon", secret=True)
    secret["seats"] = seats


# ── 3. the planes ────────────────────────────────────────────────────────────────────────────────────────────

def plane_set(name) -> list[str]:
    rules = dt.load("planes.yaml")["rules"]
    rows = dt.rows(PL + "baseline")
    if name == MOON:
        return [MOON]
    if name == "non_material":
        return [r["id"] for r in rows if r["id"] not in ("baseline_material", "baseline_demiplane")]
    if name == "inner":
        return list(rules["sets"]["inner"])
    if name in ("upper", "lower"):
        return [r["id"] for r in rows if r.get("group") == "outer" and r.get("tier") == name]
    return [name]


def named_slots(R, scale: str) -> list[dict]:
    """The P1 rows in this birth that name a plane, as seats to fill (planes.yaml rules.named_planes); rows that name
    one plane between them are one slot."""
    named = dt.load("planes.yaml")["rules"]["named_planes"]
    slots = []
    for rid, spec in named.items():
        if not R.ctx.has(rid) or R.ctx.secret_of(rid):
            continue
        weight = dict(spec.get("weight") or {})
        if spec.get("one_of_each"):
            parts = spec["fits"][:1] if scale == "short" else spec["fits"]      # the upper first at short (the tag pass)
            for part in parts:
                slots.append({"rows": [rid], "part": part, "fits": plane_set(part), "weight": weight})
        else:
            fits = [x for part in spec["fits"] for x in plane_set(part)]
            slots.append({"rows": [rid], "fits": list(dict.fromkeys(fits)), "weight": weight})
    for group in SAME_PLANE:
        joined = [s for s in slots if s["rows"][0] in group and "part" not in s]
        if len(joined) > 1:
            fits = [x for x in joined[0]["fits"] if all(x in s["fits"] for s in joined[1:])]
            merged = {"rows": [r for s in joined for r in s["rows"]], "fits": fits, "weight": joined[0]["weight"]}
            slots = [s for s in slots if s not in joined] + [merged]
    return sorted(slots, key=lambda s: (len(s["fits"]), s["rows"][0], s.get("part") or ""))


def min_new(slots: list[dict], have: set) -> int:
    """The fewest new planes that give every slot a plane of its fits, beside `have`."""
    unhit = [s for s in slots if not set(s["fits"]) & have]
    if not unhit:
        return 0
    first = min(unhit, key=lambda s: len(s["fits"]))
    best, seen = len(unhit), set()
    for x in first["fits"]:
        sig = frozenset(i for i, s in enumerate(unhit) if x in s["fits"])
        if sig in seen:
            continue
        seen.add(sig)
        best = min(best, 1 + min_new(unhit, have | {x}))
    return best


def moon_allowed(R, touched: list[str]) -> bool:
    if MOON in touched:
        return False
    row = dt.row(C + "moon", MOON_ROW)
    return arb.constraint_reason(row, R.ctx, set(), None, "where", dt.conflict_index()) is None


def draw_free(R, label: str, touched: list[str]) -> str:
    """One free touched seat, drawn secretly: the baseline (never the Material), the moon among the candidates."""
    excl = set(touched) | set(NOT_TOUCHED)
    if moon_allowed(R, touched):
        res = arb.arbitrate(PL + "baseline", dt.rows(PL + "baseline"), R.ctx, exclude=excl)
        if die(R, f"{label}.moon_gate", len(res["pool"]) + 1, secret=True) == len(res["pool"]) + 1:
            note(R, label, MOON, "the moon among the free seat's candidates", secret=True)
            return MOON
    return R.table(label, PL + "baseline", avoid=False, exclude=excl, secret=True)["row_id"]


def seat_planes(R, dials: dict, out: dict, secret: dict) -> None:
    """Step 3: the touched planes, rolled the same whatever the threat is (the threat's home is a secret record of its
    own: `bind_home`). Every seat's draw is secret (the design tab, 22b audit): the public sees each touched plane and
    its seat; the planes P1 names first, with their rows, the rest in the baseline's order."""
    count = out["planes_count"]
    touched: list[str] = []
    seated_by: dict = {}
    slots = named_slots(R, dials["scale"])
    for i, s in enumerate(slots):
        label = f"plane.named.{i + 1}"
        rest = slots[i + 1:]
        free = count - len(touched)
        # a plane of its own while the seats allow it (every later slot still served), else one already touched
        fresh = [x for x in s["fits"] if x not in touched and x not in NOT_TOUCHED
                 and free - 1 >= min_new(rest, set(touched) | {x})] if free > 0 else []
        shared = [x for x in touched if x in s["fits"]]
        if fresh:
            pick = weighted(R, label, fresh, [float(s["weight"].get(x, 1)) for x in fresh], secret=True)
            touched.append(pick)
        else:
            pick = weighted(R, label, shared, [1.0] * len(shared), secret=True)
        R.by_label[label]["named_by"] = list(s["rows"]) + ([s["part"]] if s.get("part") else [])
        seated_by.setdefault(pick, []).extend(s["rows"])
    n = 0
    while len(touched) < count:
        n += 1
        touched.append(draw_free(R, f"plane.free.{n}", touched))
    rows = [r["id"] for r in dt.rows(PL + "baseline")] + [MOON]
    order = [x for x in touched if x in seated_by] + sorted((x for x in touched if x not in seated_by), key=rows.index)
    ruin_or_scar = [x for x, by in seated_by.items() if any(r.startswith(("ruin_", "scar_")) for r in by)]
    out["planes"] = [roll_plane(R, f"plane.{k}", k, pid, seated_by.get(pid, []), not ruin_or_scar or pid in ruin_or_scar)
                     for k, pid in enumerate(order, 1)]
    out["moon_seated"] = MOON in touched


HOME_LABELS = ("home.deviation", "home.rate", "home.way", "home.cost", "home.keeper")


def bind_home(R, dials: dict, out: dict, secret: dict, gods: list[dict]) -> None:
    """The end of step 4, at epic (option d of the 22b audit): the threat's home, a secret plane record outside the
    public touched planes and count. A touched plane that fits the home is only linked; otherwise the home is a secret
    touched plane of its own, its deviation, rate, way in, cost and keeper on the secret log, and a P6 site reserved
    for it. The god's home is the outer plane of the alignment it rolled in public. Every label stands in every epic
    birth (null when the home only links, or there is none)."""
    if dials["scale"] != "epic":
        return
    seats = secret["seats"]
    if seats.get("home_by_alignment"):
        god = next(g for g in gods if g["n"] == seats["threat_god"])
        fits = [r["id"] for r in dt.rows(PL + "baseline") if r.get("group") == "outer" and god["alignment"] in plane_alignments(r["id"])]
    else:
        fits = list(seats.get("home_fits") or [])
    linked = [pl for pl in out["planes"] if pl["baseline"] in fits]
    if linked:
        n = choose(R, "seat.home_plane.bound", [pl["n"] for pl in linked], secret=True)
        pid = next(pl["baseline"] for pl in linked if pl["n"] == n)
        secret["home_plane"] = {"baseline": pid, "linked": n, "own": None}
    elif fits:
        pid = choose(R, "seat.home_plane.bound", fits, secret=True)
        own = roll_plane(R, "home", None, pid, [], True, secret=True)
        own["keeper"] = keeper_of(R, dials, "home.keeper", pid, gods, secret=True)
        if own["keeper"] is None:
            note(R, "home.keeper", None, "no SRD creature keeps the plane", secret=True)
        secret["home_plane"] = {"baseline": pid, "linked": None, "own": own, "site": "a P6 site reserved for the home (secret)"}
    else:
        note(R, "seat.home_plane.bound", None, "the threat has no home plane", secret=True)
        secret["home_plane"] = None
    seats["home_plane"] = (secret["home_plane"] or {}).get("baseline")
    if not (secret["home_plane"] or {}).get("own"):
        for label in HOME_LABELS:
            note(R, label, None, "no secret plane of its own", secret=True)


def rate_weigh(on_this: bool):
    """The tag pass's per-plane fits (planes.yaml rules.plane_fits): a non-same rate x2 while the condition row holds,
    on the ruin's or the scar's plane (`on_this`: the plane a ruin or a scar names, or every touched plane when none
    does: ruin_broken_time and scar_time_flow_changed name none)."""
    fits = [f for f in dt.load("planes.yaml")["rules"].get("plane_fits") or [] if f.get("table") == "time_rate"]

    def weigh(row, ctx):
        w = arb.weight_of(row, ctx)
        for fit in fits:
            if on_this and row["id"] in fit["rows"] and any(ctx.has(x) for x in fit["when"]):
                w *= float(fit["x"])
        return w
    return weigh


def roll_plane(R, base: str, k, pid: str, named_by: list[str], on_this: bool, secret: bool = False) -> dict:
    if not secret:
        # the plane and its seat, no die (the seat's draw is secret); the baseline row is named, so the promise ledger
        # reads its hooks as public (build item 22c)
        rec = R._record(base, None if pid == MOON else PL + "baseline")
        rec.update({"notation": "seated", "raw": None, "row_id": None if pid == MOON else pid, "value": pid,
                    "derived_from": ("named by " + ", ".join(named_by)) if named_by else "a touched seat",
                    "seat": "moon" if pid == MOON else "baseline"})
        R._keep(rec, False)
    if pid == MOON:
        dev = R.forced(f"{base}.deviation", PL + "deviation", "dev_is_this_world", "the moon is a place in this world (planes.yaml rules.moon_seat)",
                       secret=secret)["row_id"]
    else:
        dev = R.table(f"{base}.deviation", PL + "deviation", avoid=False, exclude={"dev_removed"}, secret=secret)["row_id"]
    rate = R.table(f"{base}.rate", PL + "time_rate", avoid=False, weigh=rate_weigh(on_this), secret=secret)["row_id"]
    way = R.table(f"{base}.way", PL + "way_in", avoid=False, secret=secret)["row_id"]
    if dev == "dev_reachable_by_death":
        cost = R.table(f"{base}.cost", PL + "cost", avoid=False, where=lambda r: r["id"] in ("cost_the_way_back", "cost_years"),
                       why="a plane reachable by dying (the row's own hook)", secret=secret)["row_id"]
    else:
        cost = R.table(f"{base}.cost", PL + "cost", avoid=False, secret=secret)["row_id"]
    return {"n": k, "baseline": pid, "named_by": list(named_by), "deviation": dev, "rate": rate, "way": way, "cost": cost,
            "keeper": None, "name": None}


# ── 4. the pantheon ──────────────────────────────────────────────────────────────────────────────────────────

def coverage(scale: str) -> tuple[int, set]:
    """(the distinct domains the scale's coverage needs, the domains it names): short Life and three others, standard
    six of the eight, epic all eight."""
    rule = dt.load("pantheon.yaml")["rules"]["domain_coverage"][scale]
    return {"short": (4, {"domain_life"}), "standard": (6, set()), "epic": (8, set())}.get(scale, (0, set())) if rule else (0, set())


def feasible(have: set, draws: int, target: int, named: set) -> bool:
    return len(named - have) <= draws and max(0, target - len(have)) <= draws


def plane_alignments(pid: str | None) -> set:
    row = dt.row(PL + "baseline", pid) if pid and pid != MOON else None
    return set(str((row or {}).get("alignment") or "").split("/")) - {""}


def roll_gods(R, dials: dict, slots: list[dict], out: dict, secret: dict, pool, names: dict) -> list[dict]:
    scale = dials["scale"]
    domains = rows_of(P + "domain_scaffold")
    target, named = coverage(scale)
    have: set = set()
    seats = secret["seats"]
    gods = []
    for i, s in enumerate(slots):
        n = s["n"]
        later = len(slots) - i - 1
        rec = R.forced(f"god.{n}.rank", P + "rank", f"rank_{s['rank']}", "the rank split")
        k = die(R, f"god.{n}.domains_count", 2)
        if not feasible(have, k + 2 * later, target, named):
            k = 2
            R.by_label[f"god.{n}.domains_count"]["raised_to"] = "2: the scale's domain coverage"
        mine: list[str] = []
        for j in range(k):
            left = k - j - 1 + 2 * later

            def ok(r, mine=mine, left=left):
                return r["id"] not in mine and feasible(have | {r["id"]}, left, target, named)
            d = R.table(f"god.{n}.domain.{j + 1}", P + "domain_scaffold", avoid=False, where=ok,
                        why="the scale's domain coverage")["row_id"]
            mine.append(d)
            have.add(d)
        align = choose(R, f"god.{n}.alignment", list(domains[mine[0]]["alignments"]))
        gods.append({"n": n, "id": None, "name": None, "epithet": None, "rank": s["rank"], "great": s["great"],
                     "domains": mine, "alignment": align, "church": None, "fallen": n == out.get("ruin_god")})
    # the evil god (S2): at standard and epic at least one god is evil
    if dt.load("pantheon.yaml")["rules"].get("evil_god") and scale in ("standard", "epic") and not any(g["alignment"] in EVIL for g in gods):
        listing = [g for g in gods if any(set(domains[d]["alignments"]) & set(EVIL) for d in g["domains"])]
        if listing:
            g = choose(R, "evil_god", [x["n"] for x in listing])
            god = next(x for x in gods if x["n"] == g)
            evil = [a for d in god["domains"] for a in domains[d]["alignments"] if a in EVIL]
            god["alignment"] = choose(R, "evil_god.alignment", list(dict.fromkeys(evil)))
        else:
            one = [g for g in gods if len(g["domains"]) == 1] or gods
            g = choose(R, "evil_god", [x["n"] for x in one])
            god = next(x for x in gods if x["n"] == g)
            d = R.table("evil_god.domain", P + "domain_scaffold", avoid=False,
                        where=lambda r: r["id"] != god["domains"][0] and bool(set(r["alignments"]) & set(EVIL)),
                        why="a domain that lists an evil alignment")["row_id"]
            god["domains"] = [god["domains"][0], d]
            god["alignment"] = choose(R, "evil_god.alignment", [a for a in domains[d]["alignments"] if a in EVIL])
        out["evil_god"] = god["n"]
    else:
        out["evil_god"] = next((g["n"] for g in gods if g["alignment"] in EVIL), None)
    names["pinned_seat"] = seats.get("threat_god") or seats.get("power_god")
    name_gods(R, gods, pool, names)
    return gods


def god_language(naming: dict | None, pool: dict | None) -> str | None:
    """The language the gods are named in: the common tongue, else the people's (the 22b ruling 1)."""
    langs = list(((pool or {}).get("languages") or {}))
    for lid in ("common", "people"):
        if lid in langs:
            return lid
    living = [lid for lid in langs if (((naming or {}).get("languages") or {}).get(lid) or {}).get("owner") != "old"]
    return living[0] if living else None


def take(entries: list, eid: str) -> str | None:
    for e in entries:
        if not e.get("used_by"):
            e["used_by"] = eid
            return e["name"]
    return None


def _entry(stock: dict | None, name: str, free_for: tuple) -> dict | None:
    """A god entry of a stock by its name, any language, unused or held by one of `free_for`."""
    for L in ((stock or {}).get("languages") or {}).values():
        for e in L.get("god") or []:
            if e.get("name") == name and e.get("used_by") in (None,) + free_for:
                return e
    return None


def name_gods(R, gods: list[dict], pool: dict | None, names: dict) -> None:
    """Each god a name and an epithet from the pool, in the gods' language and the pool's order, reserved under the id
    the frame carries (god_<slug>). The unnamed god of break_god_name_forbidden goes by its epithet and takes a hidden
    name from the secret stock. The pinned seat's god (the 22c audit) takes its public face like every god; the name the
    premise pinned (P1's `dm_only.pinned.god`, a secret-stock name; a legacy public-stock pin alike) is its true name in
    dm-only and is reserved under its id. Nothing public moves with the pin. No pool, no names."""
    import design_io
    lid = names.get("lang")
    if not pool or not lid:
        return
    L = pool["languages"].get(lid) or {}
    unnamed = names.get("unnamed_god")
    pin = names.get("pinned") or {}
    pinned_n = names.get("pinned_seat")
    pin_name, premise = pin.get("name"), pin.get("premise")
    held = (premise,) if premise else ()
    pin_entry = None
    if pin_name and pinned_n:
        pin_entry = _entry(names.get("secret_pool"), pin_name, held) or _entry(pool, pin_name, held)
    taken = {pin_name} if pin_name else set()
    for g in gods:
        g["lang"] = lid
        if g["n"] == unnamed:
            # the unnamed god goes by its epithet; its id follows the epithet, so the hidden name is in no public field
            entry = next((e for e in L.get("epithets") or [] if not e.get("used_by")), None)
            if entry is None:
                continue
            g["epithet"] = entry["name"]
            g["id"] = "god_" + design_io.slug(entry["name"].removeprefix("the ").removeprefix("The "))
            entry["used_by"] = g["id"]
            if g["n"] != pinned_n or pin_entry is None:
                S = ((names.get("secret_pool") or {}).get("languages") or {}).get(lid) or {}
                hidden = next((e for e in S.get("god") or [] if not e.get("used_by")), None)
                if hidden:
                    hidden["used_by"] = g["id"]
                    names.setdefault("hidden", {})[g["n"]] = hidden["name"]
        else:
            entry = next((e for e in L.get("god") or [] if not e.get("used_by") and e.get("name") not in taken), None)
            if entry is None:
                continue
            g["id"] = "god_" + design_io.slug(entry["name"])
            entry["used_by"] = g["id"]
            g["name"] = entry["name"]
            g["epithet"] = take(L.get("epithets") or [], g["id"])
        if g["n"] == pinned_n and pin_entry is not None:
            pin_entry["used_by"] = g["id"]
            names.setdefault("hidden", {})[g["n"]] = pin_entry["name"]
        # the names ride on the god's first record, its rank
        R.by_label[f"god.{g['n']}.rank"].update({"god_id": g["id"], "name": g["name"], "epithet": g["epithet"]})


def church_weigh(pilgrim: bool):
    """church_pilgrimage x3 belongs to the pilgrim road's own greater god (the tag pass): every other god draws it at
    its plain weight."""
    def weigh(row, ctx):
        w = arb.weight_of(row, ctx)
        if row["id"] == "church_pilgrimage" and not pilgrim and ctx.has("life_pilgrim_road"):
            w /= 3.0
        return w
    return weigh


def roll_pantheon(R, dials: dict, p1: dict, slots: list[dict], out: dict, secret: dict, pool, names: dict) -> None:
    scale = dials["scale"]
    f = p1.get("foundation") or {}
    walk = [(r, to) for r, to in overrides_on(R, "pantheon_presence") if dt.row(P + "presence", str(to))]
    if walk:
        rec = R.forced("pantheon_presence", P + "presence", walk[0][1], f"override by {walk[0][0]}")
        tagged(rec, [(r, "pantheon_presence") for r, _ in walk])
    else:
        R.table("pantheon_presence", P + "presence", avoid=False)
    out["presence"] = R.row("pantheon_presence")
    # the unnamed god (break_god_name_forbidden): one of the great gods, its name hidden
    if R.ctx.has("break_god_name_forbidden") and not R.ctx.secret_of("break_god_name_forbidden"):
        great = [s["n"] for s in slots if s["great"]] or [s["n"] for s in slots if s["rank"] == "greater"] or [slots[0]["n"]]
        names["unnamed_god"] = choose(R, "unnamed_god", great)
        R.by_label["unnamed_god"]["derived_from"] = "break_god_name_forbidden: the unnamed god counts among the great gods"
    gods = roll_gods(R, dials, slots, out, secret, pool, names)
    domains = rows_of(P + "domain_scaffold")
    # the pilgrim road's god (the lifeline) is a greater god
    pilgrim = None
    if (f.get("lifeline") or {}).get("id") == "life_pilgrim_road":
        pilgrim = choose(R, "pilgrim_god", [g["n"] for g in gods if g["rank"] == "greater"])
    out["pilgrim_god"] = pilgrim
    drawn: set = set()
    for g in gods:
        if g["rank"] == "greater":
            # each greater god a church of its own archetype (build item 22c: two great gods drew one watch house)
            g["church"] = {"archetype": R.table(
                f"god.{g['n']}.church", P + "church_archetype", avoid=False, weigh=church_weigh(g["n"] == pilgrim), exclude=set(drawn),
                where=(lambda r: r.get("faction_archetype") != "none") if g["great"] else None,
                why="a great god's church is a faction")["row_id"]}
            drawn.add(g["church"]["archetype"])
        else:
            shapes = list(domains[g["domains"][0]]["church_shape"])
            g["church"] = {"line": choose(R, f"god.{g['n']}.church", shapes)}
    out["gods"] = gods
    roll_relations(R, out, secret, gods)
    # the god story (S2): one discoverable god_secret per campaign at standard and epic, on a greater god
    if scale in ("standard", "epic"):
        g = choose(R, "god_story.god", [x["n"] for x in gods if x["rank"] == "greater"])
        god = next(x for x in gods if x["n"] == g)
        tend = {t for d in god["domains"] for t in domains[d].get("secret_tendency") or []}
        row = R.table("god_story", P + "god_secret", avoid=False, where=(lambda r: r["id"] in tend) if tend else None,
                      why="the god's domains' secret tendency")["row_id"]
        out["god_story"] = {"god": g, "row": row}
    else:
        out["god_story"] = None
    roll_afterlife(R, out, gods)
    roll_keepers(R, dials, out, gods)
    bind_home(R, dials, out, secret, gods)


def roll_afterlife(R, out: dict, gods: list[dict]) -> None:
    """Where the dead go (pantheon.yaml#afterlife; docs/p2-tags.md "Where the dead go"): one land of the dead when a
    touched plane is reachable by dying (that plane is the land), else a roll; the judge named among the Death gods and
    the powers."""
    reach = [pl for pl in out["planes"] if pl["deviation"] == "dev_reachable_by_death"]
    if reach:
        rec = R.forced("afterlife", P + "afterlife", "afterlife_one_land", f"plane {reach[0]['n']} is reachable by dying: it is the land")
        tagged(rec, [("dev_reachable_by_death", "afterlife")])
        out["afterlife"] = {"row": "afterlife_one_land", "plane": reach[0]["n"]}
        return
    row = R.table("afterlife", P + "afterlife", avoid=False)["row_id"]
    out["afterlife"] = {"row": row}
    if row == "afterlife_judge":
        judges = [g["n"] for g in gods if "domain_death" in g["domains"] or g["rank"] == "power"]
        out["afterlife"]["judge"] = choose(R, "afterlife.judge", judges)


def roll_relations(R, out: dict, secret: dict, gods: list[dict]) -> None:
    """One connected web: each god after the first joined to an earlier god, each greater god one more; a polytheist
    web holds a rivalry and an alliance; rel_mirror never in the public web (the 22b ruling 8)."""
    edges: list[tuple[int, int]] = [(gods[i]["n"], choose(R, f"rel.{i}.to", [g["n"] for g in gods[:i]])) for i in range(1, len(gods))]
    for g in gods:
        if g["rank"] != "greater":
            continue
        others = [x["n"] for x in gods if x["n"] != g["n"] and (g["n"], x["n"]) not in edges and (x["n"], g["n"]) not in edges]
        if others:
            edges.append((g["n"], choose(R, f"rel.extra.{g['n']}.to", others)))
    need = {"rel_rivalry", "rel_alliance"} if out["type"] == "pantheon_polytheist" else set()
    rels = []
    for k, (a, b) in enumerate(edges, 1):
        left = len(edges) - k
        missing = need - {r["relation"] for r in rels}
        where = (lambda r, missing=missing: r["id"] in missing) if len(missing) > left else None
        rid = R.table(f"rel.{k}", P + "relationship", avoid=False, exclude={"rel_mirror"}, where=where,
                      why="the polytheist web's rivalry and alliance")["row_id"]
        rels.append({"a": a, "b": b, "relation": rid})
    out["relations"] = rels
    pinned = secret["seats"]["threat_god"] or secret["seats"]["power_god"]
    if pinned is not None and len(gods) > 1:
        me = next(g for g in gods if g["n"] == pinned)
        same = [g["n"] for g in gods if g["n"] != pinned and set(g["domains"]) & set(me["domains"])]
        mirror = choose(R, "rel_mirror.to", same or [g["n"] for g in gods if g["n"] != pinned], secret=True)
        secret["mirror"] = {"a": pinned, "b": mirror, "relation": "rel_mirror"}
    else:
        note(R, "rel_mirror.to", None, "no god is pinned", secret=True)


def keeper_window(level_band) -> tuple[float, float]:
    """A creature keeper's CR (the correction to the 22b ruling 9; the world does not scale): from the campaign band's
    middle level to its top level + 3."""
    lo, hi = (int(level_band[0]), int(level_band[1])) if level_band else (1, 20)
    return float((lo + hi) // 2), float(hi + 3)


def keeper_creatures(pid: str, level_band) -> list[str]:
    """The SRD creatures that may keep a plane no power keeps (the 22b ruling 9), CR inside `keeper_window` (the
    nearest outside it when none is)."""
    return list(_keepers(pid, tuple(level_band) if level_band else None))


@lru_cache(maxsize=512)
def _keepers(pid: str, level_band) -> tuple:
    import design_threat as dth
    idx = dth.srd_index()
    row = dt.row(PL + "baseline", pid) if pid != MOON else {}
    group, tier = (row or {}).get("group"), (row or {}).get("tier")
    axis = {a[0] for a in plane_alignments(pid)}          # L, N, C of the plane's alignments

    def fits(key: str, m: dict) -> bool:
        hab = set((m.get("ecology") or {}).get("habitats") or [])
        if group == "outer" and tier in ("lower", "upper"):
            return f"planar_{tier}" in hab
        if pid in ELEMENT_OF:
            return key in ELEMENT_CREATURES[ELEMENT_OF[pid]]
        if pid == "baseline_chaos":
            return any(key in c for c in ELEMENT_CREATURES.values())
        if pid == "baseline_fey_echo":
            return m.get("type") == "fey"
        if pid == "baseline_shadow_echo":
            return m.get("type") == "undead"
        if pid == "baseline_beyond":
            return m.get("type") == "aberration"
        if pid == "baseline_ethereal":
            return key == "ghost"
        return bool(hab & set(PLANAR_HABITATS))
    cands = sorted(k for k, m in idx.items() if fits(k, m))
    if group == "outer" and tier in ("lower", "upper") and len(axis) == 1 and axis != {"N"}:
        # the 22b audit: a lawful evil plane is the devils', a chaotic evil one the demons' (by the index's alignment),
        # a neutral or mixed one any fiend; the celestials split the same way
        word = {"L": "lawful", "C": "chaotic"}[next(iter(axis))]
        sided = [k for k in cands if str(idx[k].get("alignment") or "").startswith(word)]
        cands = sided or cands
    if not cands:
        return ()
    lo, hi = keeper_window(level_band)
    inside = [k for k in cands if lo <= float(idx[k]["cr"]) <= hi]
    if inside:
        return tuple(inside)
    near = min(min(abs(float(idx[k]["cr"]) - lo), abs(float(idx[k]["cr"]) - hi)) for k in cands)
    return tuple(k for k in cands if min(abs(float(idx[k]["cr"]) - lo), abs(float(idx[k]["cr"]) - hi)) == near)


def keeper_of(R, dials: dict, label: str, pid: str, gods: list[dict], secret: bool = False) -> dict | None:
    """A touched plane's keeper: a power whose alignment is one of the plane's (outer planes only), else an SRD creature
    of that plane (`keeper_creatures`), each on its own die."""
    aligns = plane_alignments(pid)
    powers = [g["n"] for g in gods if g["rank"] == "power" and aligns and g["alignment"] in aligns]
    if powers:
        return {"god": choose(R, label, powers, secret=secret)}
    cands = keeper_creatures(pid, dials.get("level_band"))
    return {"creature": choose(R, label, cands, secret=secret)} if cands else None


def roll_keepers(R, dials: dict, out: dict, gods: list[dict]) -> None:
    for pl in out["planes"]:
        pl["keeper"] = keeper_of(R, dials, f"plane.{pl['n']}.keeper", pl["baseline"], gods)


# ── 5. the history ───────────────────────────────────────────────────────────────────────────────────────────

def roll_history(R, dials: dict, sc: dict, p1: dict, out: dict, secret: dict) -> None:
    hist = sc["history"]
    years = int(hist["years_covered"])
    f, threat = p1.get("foundation") or {}, p1.get("threat") or {}
    ruin = f.get("ruin_source")
    time_row = next((t for t in TIME_ROWS if R.ctx.has(t)), None)
    # the seated events, first; their count is inside the scale's dated events
    seated = []
    if time_row:
        ago = {"time_just_now": 0, "time_unfolding": 0, "time_coming": None}.get(time_row)
        if time_row == "time_generation_ago":
            ago = between(R, "event.move.years_ago", 19 + 1, 19 + 11)
        seated.append({"seat": "move", "years_ago": ago, "time": time_row})
    if threat.get("origin"):
        lo = (seated[0]["years_ago"] or 0) + 1 if seated else 1
        seated.append({"seat": "origin", "years_ago": between(R, "event.origin.years_ago", lo, max(lo, years))})
        secret["origin"] = {"event": "origin", "row": threat["origin"], "true_layer": "P1's chain (dice-log.json#identity)"}
    if (p1.get("identity") or {}).get("institution"):
        seated.append({"seat": "founding", "years_ago": between(R, "event.founding.years_ago", 1, years)})
    if ruin:
        seated.append({"seat": "ruin", "years_ago": between(R, "event.ruin.years_ago", years // 2 + 1, years), "ruin": ruin})
    total = R.count("events_count", hist["dated_events"])
    if total < len(seated):
        R.by_label["events_count"]["value"] = total = len(seated)
        R.by_label["events_count"]["raised_to_seated"] = f"{len(seated)} seated events"
    events = []
    for k, ev in enumerate(seated, 1):
        rec = note(R, f"event.{k}", ev["seat"], "seated by the script (S5)", table="history.seated")
        rec["years_ago"] = ev["years_ago"]
        events.append(dict(ev, n=k, type=None, divergence=None, witnesses=True))
    for k in range(len(seated) + 1, total + 1):
        typ = R.table(f"event.{k}", H + "event_type", avoid=False)["row_id"]
        events.append({"n": k, "seat": None, "type": typ, "years_ago": between(R, f"event.{k}.years_ago", 1, years),
                       "divergence": None, "witnesses": False})
    deep = []
    for k in range(1, R.count("deep_count", hist["deep_past_events"]) + 1):
        deep.append({"n": k, "type": R.table(f"deep.{k}", H + "event_type", avoid=False)["row_id"], "years_ago": None,
                     "divergence": None})
    # exactly the scale's divergences, on the unseated events; every other unseated event's layers agree
    pool = [("event", e["n"]) for e in events if not e["seat"]] + [("deep", e["n"]) for e in deep]
    want = min(int(hist.get("divergences") or 0), len(pool))
    chosen: list = []
    for i in range(want):
        left = [x for x in pool if x not in chosen]
        chosen.append(left[die(R, f"divergence.pick.{i + 1}", len(left)) - 1])
    for kind, n in pool:
        label = f"divergence.{n}" if kind == "event" else f"deep.{n}.divergence"
        target = next(e for e in (events if kind == "event" else deep) if e["n"] == n)
        if (kind, n) in chosen:
            target["divergence"] = R.table(label, H + "divergence", avoid=False, exclude={"div_none"})["row_id"]
        else:
            target["divergence"] = R.forced(label, H + "divergence", "div_none", "the scale's divergences are spent elsewhere (S5)")["row_id"]
    for e in events:
        e["memory"] = R.table(f"memory.{e['n']}", H + "memory", avoid=False)["row_id"]
    for e in deep:
        e["memory"] = R.table(f"deep.{e['n']}.memory", H + "memory", avoid=False)["row_id"]
    # the ages: the first (one of two) and the present in place, the ruin's fall an age, the ones between rolled
    count = R.count("ages_count", hist["ages"])
    middle = count - 2 - (1 if ruin else 0)
    if middle < 0:
        R.by_label["ages_count"]["value"] = count = 2 + (1 if ruin else 0)
        R.by_label["ages_count"]["raised_to_seated"] = "the first age, the ruin's age and the present"
        middle = 0
    ruin_at = 1 + die(R, "ruin_age.place", middle + 1) if ruin else None     # after the first age, among the middle ones
    fixed = {"age_before", "age_founding", "age_now_named_for_fear"}
    rows, drawn = [], []
    for k in range(1, count + 1):
        if k == 1:
            a = R.table("age.1", H + "age_template", avoid=False, where=lambda r: r["id"] in ("age_before", "age_founding"),
                        why="the first age")["row_id"]
        elif k == count:
            a = R.forced(f"age.{k}", H + "age_template", "age_now_named_for_fear", "the present stands in place (S5)")["row_id"]
        elif k == ruin_at:
            a = note(R, f"age.{k}", ruin, "the ruin's fall is an age, named from the ruin source (S5)",
                     table="foundation.yaml#ruin_source")["value"]
        else:
            a = R.table(f"age.{k}", H + "age_template", exclude=set(drawn) | fixed)["row_id"]
        drawn.append(a)
        rows.append({"n": k, "row": a, "ruin": k == ruin_at, "name": None})
    out["ages"] = rows
    out["events"] = events
    out["deep_events"] = deep


# ── 6. magic ─────────────────────────────────────────────────────────────────────────────────────────────────

def roll_magic(R, dials: dict, out: dict) -> None:
    mag = {}
    for sub in ("source", "constraint", "visibility"):
        mag[sub] = R.table(f"magic_{sub}", M + sub)["row_id"]
    taboos = [R.table("magic_taboo.1", M + "taboo")["row_id"]]
    if die(R, "taboo.second", 2) == 2 and taboos[0] != "taboo_none":
        taboos.append(R.table("magic_taboo.2", M + "taboo", exclude={taboos[0], "taboo_none"})["row_id"])
    mag["taboos"] = taboos
    who = overrides_on(R, "regulator_identity")
    claims = dt.load("claims.yaml")
    if who:
        ids = {r for r, _ in who}
        line = next((c["combine"] for c in claims.get("combines") or [] if c["default"] == "regulator_identity"
                     and set(c["rows"]) == ids), None)
        value = line or str(who[0][1])
        rec = forced_value(R, "magic_regulator", M + "regulator", value, "override by " + ", ".join(sorted(ids)))
        tagged(rec, [(r, "regulator_identity") for r, _ in who])
        mag["regulator"] = {"row": None, "who": value}
        services = value
    else:
        rid = R.table("magic_regulator", M + "regulator", avoid=False)["row_id"]
        row = dt.row(M + "regulator", rid) or {}
        mag["regulator"] = {"row": rid, "who": row.get("label")}
        services = row.get("services") or "the regulator"
        if services == "the regulator":
            services = str(row.get("label") or rid)
        elif services == CASTERS:
            church = next((g for g in out["gods"] if (g.get("church") or {}).get("archetype")
                           and "identify" in (dt.row(P + "church_archetype", g["church"]["archetype"]) or {}).get("services", [])), None)
            if church:
                services = f"the church of god {church['n']}"
    mag["services"] = services
    rec = R.by_label["magic_regulator"]
    rec["services"] = services
    strict = overrides_on(R, "regulator_strictness")
    dial = ((dt.dial_row("magic", dials.get("magic")) or {}).get("effects") or {}).get("regulator_strictness")
    if strict:      # the combine: the strictest rule holds
        value = max((str(to) for _, to in strict), key=lambda v: STRICTNESS.index(v) if v in STRICTNESS else -1)
        rec = forced_value(R, "regulator_strictness", "dials.yaml#magic", value, "override by " + ", ".join(r for r, _ in strict))
        tagged(rec, [(r, "regulator_strictness") for r, _ in strict])
    else:
        value = dial
        note(R, "regulator_strictness", value, "the magic dial")
    mag["strictness"] = value
    gate = ((dt.dial_row("magic", dials.get("magic")) or {}).get("effects") or {}).get("wild_magic_roll", {})
    raw = R.notation("wild_gate", gate.get("notation", "d6"))["raw"]
    if raw in (gate.get("on") or []):
        mag["wild"] = R.table("wild_shape", M + "wild", avoid=False, exclude={"wild_no"})["row_id"]
    else:
        mag["wild"] = R.forced("wild_shape", M + "wild", "wild_no", f"gate {gate.get('notation', 'd6')}={raw} not in {gate.get('on')}")["row_id"]
    out["magic"] = mag


# ── 7. the calendar ──────────────────────────────────────────────────────────────────────────────────────────

def allowed_climates(foundation: dict | None) -> dict:
    """climate id → how many of the palette's kinds allow it (their biomes' climates, regions.yaml); {} for a legacy
    birth with no palette."""
    if not foundation:
        return {}
    kinds = list(foundation.get("palette") or []) + list(foundation.get("palette_extra") or [])
    pal = rows_of("foundation.yaml#palette")
    biomes = rows_of("regions.yaml#biome")
    out: dict = {}
    for k in kinds:
        allow = set()
        for b in (pal.get(k) or {}).get("biomes") or []:
            allow |= set((biomes.get(b) or {}).get("climates") or [])
        for c in allow:
            out[c] = out.get(c, 0) + 1
    return out


def span_days(sc: dict) -> tuple[int, int]:
    """The campaign's span (the 22b ruling 4): the scale's sessions x the doom's days per session."""
    per = int(dt.scale_shared()["doom"]["days_per_session_default"])
    lo, hi = band(sc["target_sessions"])
    return lo * per, hi * per


def add_days(date: dict, days: int, cal: dict) -> dict:
    length, months = int(cal["month_length"]), int(cal["months"])
    total = (date["month"] - 1) * length + (date["day"] - 1) + days
    year = date["year"] + total // (length * months)
    total %= length * months
    return {"year": year, "month": total // length + 1, "day": total % length + 1}


def season_months(climate: str | None, cal: dict) -> list[tuple[str, int]]:
    """(season, its first month): the climate's seasons laid in order over the twelve months."""
    seasons = [s["name"] for s in ((dt.row(C + "climate", climate) or {}).get("seasons") or [])] or ["the year"]
    span = int(cal["months"]) // len(seasons)
    return [(name, 1 + i * span) for i, name in enumerate(seasons)]


def roll_calendar(R, dials: dict, sc: dict, p1: dict, out: dict, secret: dict, pool) -> None:
    cal_rules = dt.load("calendar.yaml")["rules"]
    cal = {"months": int(cal_rules["months"]), "month_length": int(cal_rules["month_length"]), "week_days": int(cal_rules["week_days"])}
    note(R, "calendar.year", dict(cal), "the fixed year (S6): twelve months of 28 days, a seven-day week")
    names = (pool or {}).get("calendar") or {}
    import design_dice as dd
    for key, want in (("months", cal["months"]), ("days", cal["week_days"])):
        entries = [e for e in names.get(key) or [] if not e.get("used_by")]
        if len(entries) >= want:
            rng = dd.derive(R.master, R.phase, "names", f"calendar.{key}", R.attempt)
            picked = rng.sample(entries, want)
            for e in picked:
                e["used_by"] = f"calendar.{key}"
            rec = R._record(f"calendar.{key}", "naming.yaml#patterns")
            rec.update({"notation": "draw", "items": [e["name"] for e in picked]})
            R._keep(rec, False)
            cal[f"{key[:-1]}_names"] = [e["name"] for e in picked]
    f = p1.get("foundation")
    # the climate: the palette's climates, weighted by how many kinds allow each; the underground era forces its own
    if dials.get("era") == "underground":
        climate = R.forced("climate", C + "climate", "climate_underground", "the underground era (S6)")["row_id"]
    else:
        allow = allowed_climates(f)
        if allow:
            climate = R.table("climate", C + "climate", avoid=False, where=lambda r: r["id"] in allow, why="the palette's climates",
                              weigh=lambda r, ctx: allow.get(r["id"], 0) * arb.weight_of(dict(r, weight=1), ctx))["row_id"]
        else:
            climate = R.table("climate", C + "climate", avoid=False)["row_id"]
    cal["climate"] = climate
    # the moon: a touched seat forces the place; otherwise the place is never drawn
    if out.get("moon_seated"):
        rec = R.forced("moon", C + "moon", MOON_ROW, "the moon is a touched plane (step 3)")
        moverride = overrides_on(R, "moon")
        if moverride:
            tagged(rec, [(r, "moon") for r, _ in moverride])
    else:
        R.table("moon", C + "moon", avoid=False, exclude={MOON_ROW})
    cal["moon"] = R.row("moon")
    if dials.get("era") == "underground":
        cal["underground_count"] = R.table("underground_count", C + "underground_count", avoid=False)["row_id"]
    roll_festivals(R, out, cal)
    for x in cal["festivals"]:                 # the holy day's festival is dated inside the span, below
        if x["n"] != cal.get("holy_day"):
            x["month"] = between(R, f"festival.{x['n']}.month", 1, cal["months"])
            x["day"] = between(R, f"festival.{x['n']}.day", 1, cal["month_length"])
    # the start year, the anchor and the start date
    years = int(sc["history"]["years_covered"])
    cal["start_year"] = between(R, "start_year", years + 1, years + 300)
    time_row = next((t for t in TIME_ROWS if R.ctx.has(t)), None)
    if time_row:
        anchor = R.table("start_anchor", C + "start_anchor", avoid=False)["row_id"]
    else:
        anchors = dt.rows(C + "start_anchor")
        raw = R.notation("start_anchor.legacy", f"d{len(anchors)}")["raw"]
        anchor = R.forced("start_anchor", C + "start_anchor", anchors[raw - 1]["id"],
                          "a birth with no move time (a legacy birth): the anchor is drawn plainly (build item 22a)")["row_id"]
    cal["start_anchor"] = anchor
    lo, hi = span_days(sc)
    cal["span"] = [lo, hi]
    note(R, "span", [lo, hi], "the scale's sessions x the doom's days per session (the 22b ruling 4)")
    start = {"year": cal["start_year"]}
    fests = cal["festivals"]
    holy = cal.get("holy_day")
    seasons = season_months(climate, cal)
    if anchor == "anchor_festival_eve" and [x for x in fests if x["n"] != holy]:
        fest = choose(R, "start.festival", [x["n"] for x in fests if x["n"] != holy])
        fx = next(x for x in fests if x["n"] == fest)
        eve = add_days({"year": cal["start_year"], "month": fx["month"], "day": fx["day"]}, -1, cal)
        if eve["year"] < cal["start_year"]:                  # a festival on the year's first day: its eve ends the year before
            eve = add_days({"year": cal["start_year"] + 1, "month": fx["month"], "day": fx["day"]}, -1, cal)
        start.update(eve, festival=fest)
    elif anchor == "anchor_season_start":
        name, month = seasons[die(R, "start.season", len(seasons)) - 1]
        start.update({"month": month, "day": 1, "season": name})
    elif anchor == "anchor_midwinter":
        name, month = next(((s, m) for s, m in seasons if s == HARD_SEASON.get(climate)), seasons[0])
        per = max(1, int(cal["months"]) // len(seasons))
        start.update({"month": month + per // 2, "day": 1 if per % 2 == 0 else cal["month_length"] // 2, "season": name})
    else:
        start.update({"month": between(R, "start.month", 1, 12), "day": between(R, "start.day", 1, cal["month_length"])})
    if anchor == "anchor_after_event":
        start["after_move_days"] = between(R, "start.after_move_days", 2, 5)
    elif anchor == "anchor_days_before_doom":
        start["days_to_next_step"] = between(R, "start.days_to_next_step", 3, lo)
    cal["start"] = start
    note(R, "start_date", dict(start), f"the start anchor {anchor}")
    # the dated days, inside the span: offsets 1..its low end from the start date
    dated = {}
    if R.ctx.has("break_dead_month") and not R.ctx.secret_of("break_dead_month"):
        d = add_days(start, between(R, "dated.empty_month", 1, lo), cal)
        dated["empty_month"] = {"month": d["month"], "year": d["year"]}
    if R.ctx.has("break_lawless_day") and not R.ctx.secret_of("break_lawless_day"):
        dated["lawless_day"] = add_days(start, between(R, "dated.lawless_day", 1, lo), cal)
    if holy is not None:
        d = add_days(start, between(R, "dated.holy_day", 1, lo), cal)
        fx = next(x for x in fests if x["n"] == holy)
        fx.update({"month": d["month"], "day": d["day"]})
        dated["holy_day"] = dict(d, festival=holy)
    if R.ctx.has("weak_vulnerable_time"):
        d = add_days(start, between(R, "dated.vulnerable_time", 1, lo, secret=True), cal)
        secret["vulnerable_time"] = d
    else:
        note(R, "dated.vulnerable_time", None, "the weakness keeps no dated time", secret=True)
    cal["dated"] = dated
    out["calendar"] = cal


def roll_festivals(R, out: dict, cal: dict) -> None:
    """One per greater god (its first domain's festival kind; its second's, or a rolled one, when taken), then one or
    two folk festivals: the first of the pantheon type's own kind (the festivals override), each weighed x2 where its
    domain affinity holds a greater god's domain."""
    domains = rows_of(P + "domain_scaffold")
    greater = [g for g in out["gods"] if g["rank"] == "greater"]
    fests, taken = [], set()
    for g in greater:
        label = f"festival.{len(fests) + 1}"
        kinds = [domains[d]["festival_kind"] for d in g["domains"]]
        kind = next((k for k in kinds if k not in taken), None)
        if kind:
            rid = R.forced(label, C + "festival_type", kind, f"god {g['n']}'s {'first' if kind == kinds[0] else 'second'} domain")["row_id"]
        else:
            rid = R.table(label, C + "festival_type", avoid=False, exclude=taken)["row_id"]
        taken.add(rid)
        fests.append({"n": len(fests) + 1, "row": rid, "god": g["n"], "month": None, "day": None})
    gdom = {domains[d]["label"] for g in greater for d in g["domains"]}
    fit = dt.load("calendar.yaml")["rules"].get("festival_fit") or {}
    x = float(fit.get("x", 2))

    def weigh(r, ctx):
        return arb.weight_of(r, ctx) * (x if set(r.get("domain_affinity") or []) & gdom else 1.0)
    folk = die(R, "festivals.folk_count", 2)
    own = TYPE_FOLK.get(out["type"])
    # the 22b audit: when a greater god's festival already is of the type's kind, that festival carries the type's
    # feast (it keeps its god) and the first folk festival is free
    carrier = next((x for x in fests if x["row"] in (own or ())), None)
    if carrier:
        tagged(R.by_label[f"festival.{carrier['n']}"], [(out["type"], "festivals")])
        carrier["type_feast"] = True
    for k in range(folk):
        label = f"festival.{len(fests) + 1}"
        mine = [f for f in own or [] if f not in taken] if k == 0 and not carrier else []
        if mine:
            rec = R.table(label, C + "festival_type", avoid=False, exclude=taken, where=lambda r, mine=mine: r["id"] in mine,
                          why=f"the {out['type']} type's folk festival", weigh=weigh)
            tagged(rec, [(out["type"], "festivals")])
        else:
            rec = R.table(label, C + "festival_type", avoid=False, exclude=taken, weigh=weigh)
        taken.add(rec["row_id"])
        fests.append({"n": len(fests) + 1, "row": rec["row_id"], "god": None, "month": None, "day": None})
    if out["type"] == "pantheon_dualist" and fests:
        tagged(R.by_label["festival.1"], [(out["type"], "festivals")])
    cal["festivals"] = fests
    if R.ctx.has("taboo_casting_on_a_day") and greater:
        cal["holy_day"] = choose(R, "holy_day.festival", [x["n"] for x in fests if x["god"] is not None])
    else:
        cal["holy_day"] = None


# ── the whole roll ───────────────────────────────────────────────────────────────────────────────────────────

STEPS = ("counts", "seats", "planes", "pantheon", "history", "magic", "calendar")


def roll(R, dials: dict, p1: dict, pool: dict | None = None, secret_pool: dict | None = None, on_step=None) -> tuple[dict, dict]:
    """Every P2 draw in the threat's order; returns (public, secret). `pool` and `secret_pool` are the name pools
    (design_names); without them no name is drawn (the in-memory corpus). `on_step(n, name)` is called after each
    step (the order test)."""
    sc = dt.scale_row(dials["scale"])
    out: dict = {"stamped": True}
    secret: dict = {}
    names = {"lang": god_language(p1.get("naming"), pool), "secret_pool": secret_pool, "pinned": p1.get("pinned_god")}
    slots: list = []

    def counts():
        roll_counts(R, dials, sc, p1, out)
        slots.extend(god_slots(out["counts"]))

    def pantheon():
        roll_pantheon(R, dials, p1, slots, out, secret, pool, names)
        if names.get("hidden"):
            secret["hidden_names"] = names["hidden"]
    steps = (counts, lambda: roll_seats(R, dials, p1, slots, out, secret), lambda: seat_planes(R, dials, out, secret),
             pantheon, lambda: roll_history(R, dials, sc, p1, out, secret), lambda: roll_magic(R, dials, out),
             lambda: roll_calendar(R, dials, sc, p1, out, secret, pool))
    for n, (name, step) in enumerate(zip(STEPS, steps), 1):
        step()
        if on_step:
            on_step(n, name)
    return out, secret
