"""
test_cosmos_roll.py — build item 22b: the cosmos rolled on the foundation, in the threat's order (design_cosmos.py;
docs/p2-build-22.md part 22b; docs/p2-tags.md S0-S7 and the rulings on the 22b questions).

Over the shared corpus (its P1 prerolls, extended to P2 on a copy of each birth's context: the corpus is never changed)
every birth is held to the part's tests: no clash the arbiter rules out; every count inside its band or raised with its
reason; the secret seats absent from the public records; every P1-named plane touched; the domain coverage and the evil
god; a festival per greater god plus one or two folk festivals; the dualist's two and two; exactly 1 / 2 / 3
divergences; every touched plane kept; every dated day inside the span; the start anchor on the move's time; every
override applied. The order: a later step never changes an earlier step's records. On disk: a script-rolled birth's P2
preroll names its gods, months and days from the pool and writes the cosmos; the legacy fixture still prerolls.
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid
from collections import Counter

from _campaign import CAMPAIGNS, SCRIPTS, USED, MarkerGuard, TestCampaign
import _corpus

sys.path.insert(0, str(SCRIPTS))
import design_arbiter as arb  # noqa: E402
import design_cosmos as dc  # noqa: E402
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

ANCHOR_BY_TIME = {"time_just_now": {"anchor_after_event"}, "time_unfolding": {"anchor_after_event"},
                  "time_coming": {"anchor_days_before_doom"},
                  "time_generation_ago": {"anchor_festival_eve", "anchor_season_start", "anchor_market_day", "anchor_midwinter"}}
REGULATOR_OVERRIDERS = ("break_magic_is_nobility", "break_casting_forbidden", "contest_casters_casterless")
SECRET_LABELS = ("seat.", "rel_mirror.", "dated.vulnerable_time", "plane.named.", "plane.free.")


def cosmos_of(d: dict, R1, on_step=None):
    """P2 rolled in memory on a copy of a corpus birth's context."""
    R = designer.Roller.in_memory(R1.master, d, phase="P2")
    R.ctx = copy.deepcopy(R1.ctx)
    pub, sec = dc.roll(R, d, dc.p1_of(R1), on_step=on_step)
    return R, pub, sec


def ordinal(date: dict) -> int:
    return int(date["year"]) * 336 + (int(date["month"]) - 1) * 28 + int(date["day"]) - 1


def faults(d: dict, R1, R, pub: dict, sec: dict) -> list[str]:
    """Every way a birth's cosmos breaks the part's tests, one line each (none on a sound birth)."""
    out = []
    sc = dt.scale_row(d["scale"])
    rec = R.by_label
    lo_hi = dt.band
    # no clash the arbiter rules out, over every P0-P2 row and token
    pairs = arb.conflicting_pairs(list(R.ctx.rolled), tokens=list(R.ctx.tokens), exempt=set(R1.exempt) | set(R.exempt))
    if pairs:
        out.append(f"clash {pairs}")
    # the counts inside their bands, or raised with the reason on the record
    c = pub["counts"]
    g_lo, g_hi = lo_hi(sc["gods"])
    if not (g_lo <= c["gods"] <= g_hi or rec["gods_count"].get("raised_to_great")):
        out.append(f"gods {c['gods']} outside {sc['gods']}")
    if c["greater"] + c["lesser"] + c["power"] != c["gods"]:
        out.append("the rank split does not sum to the god count")
    if c["great"] > c["greater"]:
        out.append("more great gods than greater gods")
    great_lo, great_hi = lo_hi(sc["great_gods"])
    dual = pub["type"] == "pantheon_dualist"
    if dual and (c["great"], c["greater"]) != (2, 2):
        out.append(f"dualist with {c['greater']} greater and {c['great']} great gods")
    if not dual and not (great_lo <= c["great"] <= great_hi or rec["great_gods_count"].get("raised_to_floor")):
        out.append(f"great gods {c['great']} outside {sc['great_gods']} with no floor")
    if c["great"] < c["great_floor"] and not dual:
        out.append(f"great gods {c['great']} under the floor {c['great_floor']}")
    mod = int(((dt.dial_row("magic", d["magic"]) or {}).get("effects") or {}).get("planes_touched_modifier") or 0)
    p_lo, p_hi = dc.shift(sc["planes_touched"], mod)
    if len(pub["planes"]) != pub["planes_count"]:
        out.append("the touched planes differ from the count")
    if not (p_lo <= pub["planes_count"] <= p_hi or rec["planes_touched_count"].get("raised_to_named")):
        out.append(f"touched {pub['planes_count']} outside [{p_lo}, {p_hi}]")
    # the secret seats in no public record
    if any(r["label"].startswith(SECRET_LABELS) for r in R.public) or {"seats", "mirror", "home_plane"} & set(pub):
        out.append("a secret seat in a public record")
    if any(r.get("row_id") == "rel_mirror" for r in R.public):
        out.append("rel_mirror in the public web")
    # every plane P1 names is touched
    named = dt.load("planes.yaml")["rules"]["named_planes"]
    seated = {r for pl in pub["planes"] for r in pl["named_by"]}
    for rid in named:
        if R1.ctx.has(rid) and not R1.ctx.secret_of(rid) and rid not in seated:
            out.append(f"{rid} names a plane no touched plane carries")
    if any(not pl.get("keeper") for pl in pub["planes"]):
        out.append("a touched plane without a keeper")
    import design_threat as dth
    cr = lambda k: float(dth.srd_index()[k]["cr"])
    w_lo, w_hi = dc.keeper_window(d["level_band"])
    for pl in pub["planes"]:
        k = (pl.get("keeper") or {}).get("creature")
        if k and not w_lo <= cr(k) <= w_hi and any(w_lo <= cr(x) <= w_hi for x in dc.keeper_creatures(pl["baseline"], d["level_band"])):
            out.append(f"the keeper {k} (CR {cr(k)}) outside [{w_lo}, {w_hi}]")
        g = (pl.get("keeper") or {}).get("god")
        if g is not None:
            god = next(x for x in pub["gods"] if x["n"] == g)
            if god["rank"] != "power" or god["alignment"] not in dc.plane_alignments(pl["baseline"]):
                out.append(f"the keeper god {g} does not fit {pl['baseline']}")
    # where the dead go: drawn in every birth; one land when a touched plane is reachable by dying; the judge
    after = pub.get("afterlife") or {}
    reach = [pl["n"] for pl in pub["planes"] if pl["deviation"] == "dev_reachable_by_death"]
    if not after.get("row"):
        out.append("no afterlife")
    elif reach and (after["row"], after.get("plane")) != ("afterlife_one_land", reach[0]):
        out.append("a plane reachable by dying, and the dead go elsewhere")
    elif not reach and after["row"] == "afterlife_one_land":
        out.append("one land of the dead with no plane reachable by dying")
    if after.get("row") == "afterlife_judge":
        judge = next((x for x in pub["gods"] if x["n"] == after.get("judge")), None)
        if not judge or not ("domain_death" in judge["domains"] or judge["rank"] == "power"):
            out.append("the judge of the dead is no Death god and no power")
    if any(pl["deviation"] == "dev_removed" for pl in pub["planes"]):
        out.append("a touched plane removed")
    if (dc.MOON in [pl["baseline"] for pl in pub["planes"]]) != (pub["calendar"]["moon"] == dc.MOON_ROW):
        out.append("the moon's seat and the moon roll disagree")
    # the domains: coverage, alignment from the first domain, the evil god
    target, need = dc.coverage(d["scale"])
    have = {x for g in pub["gods"] for x in g["domains"]}
    if len(have) < target or not need <= have:
        out.append(f"domain coverage {len(have)} of {target}")
    if d["scale"] in ("standard", "epic") and not any(g["alignment"] in dc.EVIL for g in pub["gods"]):
        out.append("no evil god")
    for g in pub["gods"]:
        if not 1 <= len(g["domains"]) <= 2 or len(set(g["domains"])) != len(g["domains"]):
            out.append(f"god {g['n']} with domains {g['domains']}")
        if g["rank"] == "greater" and not (g.get("church") or {}).get("archetype"):
            out.append(f"greater god {g['n']} without a church archetype")
        if g["great"] and (dt.row("pantheon.yaml#church_archetype", g["church"]["archetype"]) or {}).get("faction_archetype") == "none":
            out.append(f"great god {g['n']}'s church is no faction")
    # the threat's seats
    seats = sec.get("seats") or {}
    rank_of = {g["n"]: g["rank"] for g in pub["gods"]}
    if (R1.threat or {}).get("family") == "family_god" and rank_of.get(seats.get("threat_god")) not in ("lesser", "power"):
        out.append("the threat's god is not a lesser or power god")
    if pub.get("ruin_god") is not None and rank_of.get(pub["ruin_god"]) not in ("lesser", "power"):
        out.append("the ruin's god is greater")
    if R1.foundation["ruin_source"] in dc.GODS_RUINS and pub.get("ruin_god") is None and (c["lesser"] + c["power"]):
        out.append("a gods-family ruin without its god")
    home = sec.get("home_plane")
    if d["scale"] == "epic" and "home_plane" not in sec:
        out.append("an epic birth without its home record")
    if home and home.get("linked") and pub["planes"][home["linked"] - 1]["baseline"] != home["baseline"]:
        out.append("the home links a plane it is not")
    if home and not home.get("linked") and (not home.get("own") or home["baseline"] in [pl["baseline"] for pl in pub["planes"]]):
        out.append("the home is neither a linked public plane nor a secret plane of its own")
    if home and home.get("own") and home["own"]["deviation"] == "dev_removed":
        out.append("the secret home plane removed")
    if d["scale"] == "epic" and (dc.home_candidates(R1.threat) or seats.get("home_by_alignment")) and not seats.get("home_plane"):
        out.append("an epic threat with a home plane and no home seat")
    if seats.get("home_by_alignment"):
        god = next(g for g in pub["gods"] if g["n"] == seats["threat_god"])
        if god["alignment"] not in dc.plane_alignments(seats["home_plane"]):
            out.append(f"the god's home {seats['home_plane']} is not the plane of its alignment {god['alignment']}")
    if any(r.get("table") == "planes.yaml#baseline" and r.get("notation") != "seated" or r["label"].startswith("plane.")
           and r.get("raw") is not None and r["label"].count(".") == 1 for r in R.public):
        out.append("a touched plane's seat drawn in public")
    if any("alignment" in str(e.get("why")) for r in R.public for e in r.get("excluded") or []):
        out.append("a public draw bent by the home plane's alignment")
    pinned = (R1.identity_secret or {}).get("secret", {}).get("pin", {}).get("god")
    if pinned and len(pub["gods"]) > 1 and not sec.get("mirror"):
        out.append("a pinned god without its secret mirror")
    # the web: connected, the polytheist's rivalry and alliance
    edges = {(r["a"], r["b"]) for r in pub["relations"]}
    reach, frontier = {pub["gods"][0]["n"]}, [pub["gods"][0]["n"]]
    while frontier:
        x = frontier.pop()
        for a, b in edges:
            for y in ((b,) if a == x else (a,) if b == x else ()):
                if y not in reach:
                    reach.add(y)
                    frontier.append(y)
    if len(reach) != len(pub["gods"]):
        out.append("the web of relations is not connected")
    if pub["type"] == "pantheon_polytheist" and not {"rel_rivalry", "rel_alliance"} <= {r["relation"] for r in pub["relations"]}:
        out.append("a polytheist web without a rivalry and an alliance")
    if (d["scale"] in ("standard", "epic")) != bool(pub["god_story"]):
        out.append("the god story at the wrong scale")
    # the history: the seated events, the ages, exactly the scale's divergences
    seats_ev = [e["seat"] for e in pub["events"] if e["seat"]]
    if seats_ev != ["move", "origin", "founding", "ruin"]:
        out.append(f"seated events {seats_ev}")
    ages = pub["ages"]
    if len(ages) != rec["ages_count"]["value"] or ages[0]["row"] not in ("age_before", "age_founding") or ages[-1]["row"] != "age_now_named_for_fear":
        out.append("the ages are not in place")
    if sum(1 for a in ages if a["ruin"]) != 1:
        out.append("the ruin's age is not seated once")
    if len([r for r in R.public if r["label"].startswith("age.")]) != len(ages):
        out.append("the age records differ from the ages")
    div = sum(1 for e in pub["events"] + pub["deep_events"] if e.get("divergence") not in (None, "div_none"))
    if div != int(sc["history"]["divergences"]):
        out.append(f"{div} divergences, not {sc['history']['divergences']}")
    if any(e["seat"] and e.get("divergence") for e in pub["events"]):
        out.append("a seated event has a divergence row")
    if any(e.get("memory") is None for e in pub["events"] + pub["deep_events"]):
        out.append("an event without a memory row")
    # magic: the overrides applied
    who = [o for o in REGULATOR_OVERRIDERS if R1.ctx.has(o)]
    mreg = rec["magic_regulator"]
    if who and (mreg.get("notation") != "forced" or mreg.get("row_id") is not None):
        out.append(f"the regulator rolled although {who} override who")
    if not who and not mreg.get("row_id"):
        out.append("the regulator not rolled")
    if not pub["magic"].get("services"):
        out.append("no one gives the magic services")
    if ({"break_casting_forbidden", "contest_casters_casterless"} & set(R1.ctx.rolled)) and rec["regulator_strictness"].get("notation") != "forced":
        out.append("the strictness not forced")
    if R1.ctx.has("break_gods_among_mortals") and rec["pantheon_presence"].get("row_id") != "presence_walking":
        out.append("gods among mortals without the walking presence")
    if R1.ctx.has("break_gods_are_ancestors_known") and pub["type"] != "pantheon_ancestor_gods":
        out.append("the ancestors' break without the ancestor gods")
    if R1.ctx.has("break_moon_trades") and pub["calendar"]["moon"] != dc.MOON_ROW:
        out.append("the moon trades without the moon as a place")
    # the calendar: the fixed year, the festivals, the anchor, the span
    cal = pub["calendar"]
    if (cal["months"], cal["month_length"], cal["week_days"]) != (12, 28, 7):
        out.append("the year is not 12 x 28 with a seven-day week")
    greater = [g["n"] for g in pub["gods"] if g["rank"] == "greater"]
    fests = cal["festivals"]
    if sorted(x["god"] for x in fests if x["god"] is not None) != sorted(greater) or not 1 <= len(fests) - len(greater) <= 2:
        out.append(f"{len(fests)} festivals for {len(greater)} greater gods")
    own = dc.TYPE_FOLK.get(pub["type"])
    if own and not any(x["row"] in own for x in fests):
        out.append(f"the {pub['type']} type's folk festival is lost")
    if len({x["row"] for x in fests}) != len(fests):
        out.append("a festival twice")
    if any(not (1 <= x["month"] <= 12 and 1 <= x["day"] <= 28) for x in fests):
        out.append("a festival off the calendar")
    time_row = next((t for t in ANCHOR_BY_TIME if R1.ctx.has(t)), None)
    if time_row and cal["start_anchor"] not in ANCHOR_BY_TIME[time_row]:
        out.append(f"the start anchor {cal['start_anchor']} against {time_row}")
    start = ordinal(cal["start"])
    lo = cal["span"][0]
    if cal["start"]["year"] != cal["start_year"]:
        out.append("the start date is not in the start year")
    for key, day in cal["dated"].items():
        if key == "empty_month":
            first = ordinal({"year": day["year"], "month": day["month"], "day": 1})
            ok = first <= start + lo and first + 27 >= start + 1
        else:
            ok = 1 <= ordinal(day) - start <= lo
        if not ok:
            out.append(f"the dated day {key} outside the span")
    if sec.get("vulnerable_time") and not 1 <= ordinal(sec["vulnerable_time"]) - start <= lo:
        out.append("the vulnerable time outside the span")
    if R.ctx.has("taboo_casting_on_a_day") and "holy_day" not in cal["dated"]:
        out.append("the holy-day taboo without its dated festival")
    for brk in ("break_dead_month", "break_lawless_day"):
        if R1.ctx.has(brk) and {"break_dead_month": "empty_month", "break_lawless_day": "lawless_day"}[brk] not in cal["dated"]:
            out.append(f"{brk} without its dated day")
    if d["era"] == "underground" and (cal["climate"] != "climate_underground" or not cal.get("underground_count")):
        out.append("the underground era without its climate and count")
    if d["era"] != "underground":
        allow = dc.allowed_climates(R1.foundation)
        if cal["climate"] == "climate_underground" or (allow and cal["climate"] not in allow):
            out.append(f"the climate {cal['climate']} not of the palette")
    return out


_ROLLED: list = []


def rolled() -> list:
    """Every corpus birth's cosmos, rolled once per test process."""
    if not _ROLLED:
        for d, R1 in _corpus.births():
            R, pub, sec = cosmos_of(d, R1)
            _ROLLED.append((d, R1, R, pub, sec))
    return _ROLLED


class Corpus(unittest.TestCase):
    """The part's tests over every corpus birth."""

    @classmethod
    def setUpClass(cls):
        cls.rolled = rolled()

    def test_every_birth_holds_the_parts_tests(self):
        bad = Counter()
        first = {}
        for d, R1, R, pub, sec in self.rolled:
            for f in faults(d, R1, R, pub, sec):
                key = f.split(" ")[0] + " " + " ".join(f.split(" ")[1:4])
                bad[key] += 1
                first.setdefault(key, (R1.master, f))
        self.assertFalse(bad, "\n".join(f"{n} x {first[k][1]} (first {first[k][0]})" for k, n in bad.most_common()))

    def test_every_domain_type_and_presence_is_reached(self):
        doms = Counter(x for _, _, _, pub, _ in self.rolled for g in pub["gods"] for x in g["domains"])
        self.assertEqual(set(doms), {r["id"] for r in dt.rows("pantheon.yaml#domain_scaffold")})
        self.assertEqual({pub["type"] for *_, pub, _ in self.rolled}, {r["id"] for r in dt.rows("pantheon.yaml#type")})
        self.assertEqual({pub["presence"] for *_, pub, _ in self.rolled}, {r["id"] for r in dt.rows("pantheon.yaml#presence")})

    def test_the_counts_spread_over_their_bands(self):
        for scale in ("short", "standard", "epic"):
            sc = dt.scale_row(scale)
            got = {pub["counts"]["gods"] for d, _, _, pub, _ in self.rolled if d["scale"] == scale}
            lo, hi = dt.band(sc["gods"])
            self.assertLessEqual(set(range(lo, hi + 1)), got, scale)

    def test_every_afterlife_is_reached_and_the_keepers_window(self):
        rows = Counter(pub["afterlife"]["row"] for *_, pub, _ in self.rolled)
        self.assertEqual(set(rows), {r["id"] for r in dt.rows("pantheon.yaml#afterlife")}, "the forced land too")
        self.assertEqual(dc.keeper_window([1, 5]), (3.0, 8.0))
        self.assertEqual(dc.keeper_window([5, 16]), (10.0, 19.0))
        self.assertEqual(dt.row("pantheon.yaml#afterlife", "afterlife_one_land")["weight"], 0, "forced only")
        self.assertEqual(dt.row("planes.yaml#deviation", "dev_reachable_by_death")["overrides"],
                         [{"default": "afterlife", "to": "afterlife_one_land"}])
        self.assertIn("afterlife", dt.load("claims.yaml")["defaults"])

    def test_the_rolls_are_the_same_on_the_same_seed(self):
        d, R1, _, pub, sec = self.rolled[7]
        _, again, sec2 = cosmos_of(d, R1)
        self.assertEqual((json.dumps(pub, sort_keys=True), json.dumps(sec, sort_keys=True)),
                         (json.dumps(again, sort_keys=True), json.dumps(sec2, sort_keys=True)))


class Order(unittest.TestCase):
    """A later step never changes an earlier step's records (every corpus birth)."""

    def test_no_step_changes_an_earlier_record(self):
        dump = lambda recs: json.loads(json.dumps(recs, sort_keys=True, default=str))
        for d, R1 in _corpus.births():
            snaps = []
            R = designer.Roller.in_memory(R1.master, d, phase="P2")
            R.ctx = copy.deepcopy(R1.ctx)
            dc.roll(R, d, dc.p1_of(R1), on_step=lambda n, name: snaps.append((name, dump(R.public), dump(R.secret))))
            self.assertEqual([s[0] for s in snaps], list(dc.STEPS))
            for name, pub, sec in snaps:
                self.assertEqual(pub, dump(R.public[:len(pub)]), f"{R1.master}: a public record of the step '{name}' changed later")
                self.assertEqual(sec, dump(R.secret[:len(sec)]), f"{R1.master}: a secret record of the step '{name}' changed later")


class Seats(unittest.TestCase):
    """The threat's seats: the pinned god's mirror and the home plane are dm-only; the one god of the imprisoned ruin."""

    def test_the_seats_stay_secret_and_the_one_god_rule_holds(self):
        one = two = homes = own = 0
        for d, R1, R, pub, sec in rolled():
            threat = R1.threat or {}
            seats = sec["seats"]
            text = json.dumps([R.public, pub], default=str)
            self.assertNotIn("seat.", text)
            if threat.get("family") == "family_god" and pub.get("ruin_god") is not None:
                if R1.foundation["ruin_source"] in dc.ONE_GOD_RUINS:
                    self.assertEqual(seats["threat_god"], pub["ruin_god"])
                    one += 1
                else:
                    self.assertNotEqual(seats["threat_god"], pub["ruin_god"])
                    two += 1
            home = sec.get("home_plane")
            if home:
                homes += 1
                own += bool(home.get("own"))
        self.assertTrue(one and two and homes and own, (one, two, homes, own))


def public_view(R, pub) -> str:
    """What a birth shows in public: its public records (without their time stamps), its cosmos, and the labels and
    the count of its secret records (design.json#dice_log_secret)."""
    recs = [{k: v for k, v in r.items() if k != "ts"} for r in R.public]
    return json.dumps({"public": recs, "cosmos": pub, "secret_labels": [r["label"] for r in R.secret],
                       "secret_count": len(R.secret)}, sort_keys=True, default=str)


class Swap(unittest.TestCase):
    """Nothing public varies with a secret fact: each corpus birth rolled twice, the second time with the threat and
    the secret of another birth of its scale swapped in (the arbiter's context stays the birth's own); the public
    records, the cosmos, the secret labels and their count are the same, at every scale."""

    def test_the_public_face_is_blind_to_the_secret(self):
        by_scale: dict = {}
        for d, R1 in _corpus.births():
            by_scale.setdefault(d["scale"], []).append((d, R1))
        swapped = Counter()
        for scale, rows in by_scale.items():
            for i, (d, R1) in enumerate(rows):
                _, R2 = rows[(i + 1) % len(rows)]
                R, pub, _ = cosmos_of(d, R1)
                S = designer.Roller.in_memory(R1.master, d, phase="P2")
                S.ctx = copy.deepcopy(R1.ctx)
                p1 = dict(dc.p1_of(R1), threat=R2.threat, secret=R2.identity_secret)
                spub, _ = dc.roll(S, d, p1)
                self.assertEqual(public_view(R, pub), public_view(S, spub), f"{R1.master} with {R2.master}'s secret")
                swapped[scale] += 1
        self.assertEqual(set(swapped), {"short", "standard", "epic"})


def pools_of(d: dict, R1) -> tuple[dict, dict]:
    """A corpus birth's name pool and secret stock, drawn in memory as P1's preroll draws them on disk."""
    import design_names as dn
    pool = {"_meta": {}, "rolled": True, "languages": {}, "calendar": {}}
    secret = {"_meta": {}, "rolled": True, "languages": {}}
    dn.fill_pool(pool, R1.naming, R1.master, d, R1.foundation, "P1", 1, secret=secret, registered=set())
    dn.fill_secret(secret, R1.naming, R1.master, d, "P1", 1, pool, registered=set())
    return pool, secret


def pin_of(R1, secret: dict) -> dict | None:
    """The premise's pin as a P1 writer makes it: a god of the secret stock when the chain pins a god."""
    if not ((R1.identity_secret or {}).get("secret") or {}).get("pin", {}).get("god"):
        return None
    name = next(e["name"] for L in secret["languages"].values() for e in L.get("god", []))
    return {"name": name, "premise": "premise_x"}


class SwapNames(unittest.TestCase):
    """The swap test with the names (the 22c audit): rolled with a pool, the gods' public names and languages do not move
    with the threat, the secret or the pin; the pin is the pinned seat's god's true name, in dm-only alone."""

    def test_the_names_are_blind_to_the_secret(self):
        by_scale: dict = {}
        for d, R1 in _corpus.births(150):
            by_scale.setdefault(d["scale"], []).append((d, R1))
        pinned = 0
        for scale, rows in by_scale.items():
            for i, (d, R1) in enumerate(rows):
                _, R2 = rows[(i + 1) % len(rows)]
                pool, secret = pools_of(d, R1)
                outs = []
                for threat_of in (R1, R2):
                    pl, sp = copy.deepcopy(pool), copy.deepcopy(secret)
                    S = designer.Roller.in_memory(R1.master, d, phase="P2")
                    S.ctx = copy.deepcopy(R1.ctx)
                    p1 = dict(dc.p1_of(R1), threat=threat_of.threat, secret=threat_of.identity_secret, pinned_god=pin_of(threat_of, sp))
                    pub, sec = dc.roll(S, d, p1, pl, sp)
                    outs.append(public_view(S, pub))
                    seat = sec["seats"]["threat_god"] or sec["seats"]["power_god"]
                    if p1["pinned_god"] and seat is not None:
                        pinned += 1
                        self.assertEqual(sec["hidden_names"][seat], p1["pinned_god"]["name"], "the pin is the god's true name")
                        self.assertNotIn(p1["pinned_god"]["name"], json.dumps(pub), "the true name is in no public record")
                self.assertTrue(all(g["id"] for g in json.loads(outs[0])["cosmos"]["gods"]), "every god named from the pool")
                self.assertEqual(outs[0], outs[1], f"{R1.master}: the public names moved with {R2.master}'s secret")
        self.assertTrue(pinned, "some births pin a god")


class OnDisk(unittest.TestCase):
    """A script-rolled birth's P2 preroll: the cosmos on design.json, its seats in dm-only, the gods, months and days
    named from the pool and reserved there; the legacy fixture still prerolls, nameless."""

    @classmethod
    def setUpClass(cls):
        cls.guard = MarkerGuard().__enter__()
        cls.used_backup = USED.read_bytes() if USED.is_file() else None
        cls.name = f"_test-cosmos-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        run = lambda *a: subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "designer.py"), *a], capture_output=True,
                                        text=True, encoding="utf-8", check=True)
        run("new", cls.name, "--party-size", "2", "--seed", "COSMOS-0001", "--lang", "tr", "--scale", "standard")
        run("-c", cls.name, "preroll", "--phase", "P1")
        cls.out = run("-c", cls.name, "preroll", "--phase", "P2").stdout
        cls.dir = CAMPAIGNS / cls.name

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(CAMPAIGNS / cls.name, ignore_errors=True)
        if cls.used_backup is not None:
            USED.write_bytes(cls.used_backup)
        elif USED.is_file():
            USED.unlink()
        cls.guard.__exit__(None, None, None)

    def json(self, rel):
        return json.loads((self.dir / rel).read_text(encoding="utf-8"))

    def test_the_cosmos_is_written_and_named_from_the_pool(self):
        m = self.json("design/design.json")
        cosmos = m["cosmos"]
        self.assertTrue(cosmos["stamped"])
        self.assertIn("designer: cosmos", self.out)
        pool = self.json("design/dm-only/name-pool.json")
        lid = dc.god_language(self.json("design/naming.json"), pool)
        names = {e["name"]: e.get("used_by") for e in pool["languages"][lid]["god"]}
        for g in cosmos["gods"]:
            if g["name"]:
                self.assertEqual(names[g["name"]], g["id"], "the name is reserved under the frame's id")
                self.assertTrue(g["id"].startswith("god_") and g["epithet"])
        self.assertTrue(all(g["id"] for g in cosmos["gods"]))
        cal = cosmos["calendar"]
        self.assertEqual((len(cal["month_names"]), len(cal["day_names"])), (12, 7))
        self.assertEqual(len(set(cal["month_names"])), 12)
        log = self.json("design/dm-only/dice-log.json")
        self.assertIn("seats", log["cosmos"])
        self.assertNotIn("seats", json.dumps(cosmos))
        public = [r for r in m["dice_log"] if r["phase"] == "P2"]
        self.assertFalse([r for r in public if r["label"].startswith(SECRET_LABELS)])
        for pl in cosmos["planes"]:
            self.assertIsNone(pl["name"], "a plane is named in 22n, not here")

    def test_the_legacy_fixture_still_prerolls(self):
        c = TestCampaign("cosmos")
        try:
            c.reopen("P2", "pending")
            c.run("designer.py", "preroll", "--phase", "P2", "--attempt", "9", check=True)
            m = c.json("design/design.json")
            self.assertEqual(m["cosmos"]["events"][0]["seat"], None, "a legacy birth seats no event")
            self.assertTrue(all(g["name"] is None for g in m["cosmos"]["gods"]), "a legacy pool names no god")
        finally:
            c.remove()


if __name__ == "__main__":
    unittest.main()
