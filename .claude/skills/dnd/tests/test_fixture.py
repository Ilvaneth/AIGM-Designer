"""
test_fixture.py — the tuzlu-fener fixture bible is internally consistent.

A hand-written micro `short` campaign in the designer's layout (plan 24.3,
slice 0). These checks are the shape of slice 1's `design_check.py` modules
(refs, stamps, secrecy, overlay, map, sites) run by hand on one bible, so the
fixture is a tested artifact rather than a pile of examples, and the schema
docs' claims (projection rules, stamp snapshot, Exits column) are exercised
on real data.
"""

import json
import re
import shutil
import tempfile
import unittest
from collections import deque
from pathlib import Path

from _layouts import bash_payload, clean_env, install_skill, run_hook, skill_of

SKILL = Path(__file__).resolve().parent.parent
PROJECT = SKILL.parent.parent.parent
FIX = SKILL / "tests" / "fixtures" / "tuzlu-fener"
DESIGN = FIX / "design"
DM_ONLY = DESIGN / "dm-only"

WIKI = re.compile(r"\[\[([a-z0-9_]+)\]\]")
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
ROOM_ROW = re.compile(r"^\| (\d+) \| (.+?) \| (\w+) \| .*? \| (.+?) \| (\d+) \|$", re.M)
EXIT_ID = re.compile(r"^\s*(\d+)")
OVERLAY_FIELDS = {"status", "seen_in_play", "alive", "location", "ruler", "control"}
MAP_ONLY_PREFIXES = ("landmark_", "waypoint_")
GRAPH_EXTRA_IDS = {"party"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def front_matter(path: Path) -> dict:
    m = FRONT.match(path.read_text(encoding="utf-8"))
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm


def covers(fm: dict) -> set:
    raw = fm.get("covers", "")
    return {x.strip() for x in raw.strip("[]").split(",") if x.strip()}


def prose_files():
    return sorted(p for p in DESIGN.rglob("*.md") if "_staging" not in p.parts)


def stamp_snapshot_of(ent: dict) -> dict:
    """Public stamps plus the secret ones `dm_only.stamped_fields` names."""
    secret = {k: ent["dm_only"][k] for k in ent.get("dm_only", {}).get("stamped_fields", [])}
    return {**ent["stamped"], **secret}


def public_files():
    return [p for p in prose_files() if DM_ONLY not in p.parents]


class Registry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.canon = load(DM_ONLY / "entities.json")
        cls.ents = cls.canon["entities"]
        cls.public = load(DESIGN / "entities.json")["entities"]
        cls.stamps = load(DM_ONLY / "_snapshots" / "stamps.json")["stamps"]

    def test_every_json_store_parses(self):
        for p in sorted(FIX.rglob("*.json")):
            with self.subTest(p.relative_to(FIX).as_posix()):
                load(p)

    def test_ids_match_keys_and_type_prefix(self):
        for eid, ent in self.ents.items():
            self.assertEqual(ent["id"], eid)
            self.assertTrue(eid.startswith(ent["type"] + "_"), eid)
            self.assertIn(ent["secrecy"], ("public", "discoverable", "secret"), eid)
            self.assertIn("stamped", ent, eid)

    def test_projection_is_the_two_mechanical_rules(self):
        expected = {eid: {k: v for k, v in ent.items() if k != "dm_only"}
                    for eid, ent in self.ents.items() if ent["secrecy"] != "secret"}
        self.assertEqual(self.public, expected)

    def test_stamp_snapshot_matches_the_canonical_stamps(self):
        self.assertEqual(self.stamps, {eid: stamp_snapshot_of(ent) for eid, ent in self.ents.items()})

    def test_no_secret_field_sits_in_the_public_stamps(self):
        for eid, ent in self.ents.items():
            self.assertNotIn("secret_tr", ent["stamped"], eid)
            for k in ent.get("dm_only", {}).get("stamped_fields", []):
                self.assertIn(k, ent["dm_only"], f"{eid}: stamped secret {k} missing from dm_only")

    def test_registry_refs_resolve(self):
        for eid, ent in self.ents.items():
            for ref in ent.get("refs", []):
                self.assertIn(ref, self.ents, f"{eid} -> {ref}")

    def test_every_entity_file_exists_and_claims_it(self):
        for eid, ent in self.ents.items():
            with self.subTest(eid):
                path = FIX / ent["file"]
                self.assertTrue(path.is_file(), ent["file"])
                if path.suffix == ".md" and path.parent != FIX / "characters":
                    fm = front_matter(path)
                    self.assertTrue(fm.get("entity") == eid or eid in covers(fm),
                                    f"{ent['file']} does not claim {eid}")

    def test_secret_entities_live_only_in_dm_only(self):
        for eid, ent in self.ents.items():
            if ent["secrecy"] == "secret":
                self.assertTrue(ent["file"].startswith("design/dm-only/"), eid)
                self.assertNotIn(eid, self.public)

    def test_manifest_entities_equal_the_registry(self):
        manifest = load(DESIGN / "design.json")
        self.assertEqual(set(manifest["entities"]), set(self.ents))
        for eid, row in manifest["entities"].items():
            self.assertEqual(row["file"], self.ents[eid]["file"], eid)

    def test_roles_have_holders(self):
        for fid, f in ((k, v) for k, v in self.ents.items() if v["type"] == "faction"):
            for role in ("leader", "heir"):
                self.assertIn(f[role], self.ents, f"{fid}.{role}")
                self.assertEqual(self.ents[f[role]]["type"], "npc", f"{fid}.{role}")
            self.assertIn(f["hq"], self.ents, f"{fid}.hq")
        for sid, s in ((k, v) for k, v in self.ents.items() if v["type"] == "settlement"):
            self.assertIn(s["ruler_at_birth"], self.ents, f"{sid}.ruler")


class Prose(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ents = load(DM_ONLY / "entities.json")["entities"]
        cls.public_text = {p: p.read_text(encoding="utf-8") for p in public_files()}
        cls.all_text = {p: p.read_text(encoding="utf-8") for p in prose_files()}

    def test_every_wiki_link_resolves(self):
        for p, text in self.all_text.items():
            for ref in set(WIKI.findall(text)):
                self.assertIn(ref, self.ents, f"{p.relative_to(FIX).as_posix()} -> [[{ref}]]")

    def test_every_prose_file_has_front_matter(self):
        for p in self.all_text:
            fm = front_matter(p)
            self.assertIn("entity", fm, p.relative_to(FIX).as_posix())
            self.assertIn(fm.get("secrecy"), ("public", "discoverable", "secret"), p.name)

    def test_no_secret_heading_outside_dm_only(self):
        for p, text in self.public_text.items():
            self.assertNotIn("\n## Secret", text, p.relative_to(FIX).as_posix())

    def test_mirrors_point_at_each_other(self):
        for p in self.public_text:
            fm = front_matter(p)
            mirror = fm.get("mirror", "null")
            if mirror != "null":
                mpath = FIX / mirror
                self.assertTrue(mpath.is_file(), mirror)
                back = front_matter(mpath).get("mirror_of")
                self.assertEqual(back, p.relative_to(FIX).as_posix(), mirror)
                self.assertEqual(front_matter(mpath).get("secrecy"), "secret", mirror)

    def test_secret_names_and_secret_lines_never_leak_into_public_files(self):
        leaks = []
        secret_names = [ent["name"] for ent in self.ents.values() if ent["secrecy"] == "secret"]
        secret_lines = [ent["dm_only"]["secret_tr"] for ent in self.ents.values()
                        if ent.get("dm_only", {}).get("secret_tr") not in (None, "yok")]
        haystacks = dict(self.public_text)
        for extra in ("world.md", "npcs.md", "state.md", "design/entities.json", "design/naming.json",
                      "graph.json", "factions.json", "design/news.json", "common-knowledge.json"):
            haystacks[FIX / extra] = (FIX / extra).read_text(encoding="utf-8")
        for p, text in haystacks.items():
            for name in secret_names:
                if name in text:
                    leaks.append(f"{p.relative_to(FIX).as_posix()}: secret name")
            for line in secret_lines:
                if line in text:
                    leaks.append(f"{p.relative_to(FIX).as_posix()}: secret line")
        self.assertEqual(leaks, [])

    def test_primer_carries_no_ids(self):
        text = (DESIGN / "player-primer.md").read_text(encoding="utf-8")
        self.assertEqual(WIKI.findall(text), [])
        self.assertNotIn("npc_", text.split("---", 2)[-1])


class Stores(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ents = load(DM_ONLY / "entities.json")["entities"]

    def test_overlay_entries_resolve_and_carry_writer_and_day(self):
        overlay = load(DESIGN / "overlay.json")
        for eid, fields in overlay["entries"].items():
            self.assertIn(eid, self.ents, eid)
            for field, rec in fields.items():
                self.assertIn(field, OVERLAY_FIELDS, f"{eid}.{field}")
                self.assertNotIn(field, self.ents[eid]["stamped"], f"{eid}.{field} is stamped")
                for key in ("value", "birth", "writer", "day"):
                    self.assertIn(key, rec, f"{eid}.{field}.{key}")
        self.assertEqual(overlay["_meta"]["doom_day"], self.ents["arc_1"]["doom_day"])

    def test_map_nodes_cover_every_site_and_settlement(self):
        m = load(DESIGN / "map.json")
        node_ids = {n["id"] for n in m["nodes"]}
        for eid, ent in self.ents.items():
            if ent["type"] in ("site", "settlement"):
                self.assertIn(eid, node_ids, eid)
        for n in m["nodes"]:
            if not n["id"].startswith(MAP_ONLY_PREFIXES):
                self.assertIn(n["id"], self.ents, n["id"])
            self.assertIn(n["region"], self.ents)
        for e in m["edges"]:
            self.assertIn(e["from"], node_ids, e["id"])
            self.assertIn(e["to"], node_ids, e["id"])
        # connected over public nodes
        adj = {n["id"]: set() for n in m["nodes"]}
        for e in m["edges"]:
            adj[e["from"]].add(e["to"])
            adj[e["to"]].add(e["from"])
        seen, todo = set(), deque([m["nodes"][0]["id"]])
        while todo:
            cur = todo.popleft()
            if cur in seen:
                continue
            seen.add(cur)
            todo.extend(adj[cur])
        self.assertEqual(seen, set(adj))
        hubs = [n for n in m["nodes"] if n.get("hub")]
        self.assertEqual(len(hubs), 1)

    def test_news_refs_and_reach_resolve(self):
        for rec in load(DESIGN / "news.json")["records"]:
            for ref in rec["refs"] + rec["reach"]:
                self.assertIn(ref, self.ents, f"{rec['id']} -> {ref}")
            self.assertIn(rec["visibility"], ("public", "rumored", "secret"))

    def test_factions_goals_graph_channels_use_registry_ids(self):
        for f in load(FIX / "factions.json")["factions"]:
            self.assertEqual(self.ents[f["id"]]["type"], "faction")
            self.assertEqual(f["id"], self.ents[f["id"]]["board_id"])
            for asset in f["assets"]:
                self.assertIn(asset, self.ents, f"{f['id']} asset {asset}")
            for other in f["stances"]:
                self.assertTrue(other == "party" or other in self.ents, other)
            self.assertEqual(set(f["reactions"]), {"alliance", "loss", "gain", "exposure", "death", "betrayal"})
            self.assertGreaterEqual(len(f["operation"]["steps"]), 2)
        for g in load(FIX / "goals.json")["goals"]:
            self.assertIn(g["id"], self.ents, g["id"])
            self.assertEqual(set(g["responses"]), {"threatened", "blocked", "permanent_loss"})
        graph = load(FIX / "graph.json")
        node_ids = {n["id"] for n in graph["nodes"]}
        for n in graph["nodes"]:
            self.assertIn(n["id"], self.ents, n["id"])
            if self.ents[n["id"]]["secrecy"] == "secret":
                self.assertEqual(n["name"], n["id"], "secret node carries its id, not its name")
        for e in graph["edges"]:
            self.assertIn(e["from"], node_ids | GRAPH_EXTRA_IDS, e["id"])
            self.assertIn(e["to"], node_ids | GRAPH_EXTRA_IDS, e["id"])
        for ch in load(FIX / "channels.json")["channels"]:
            for pid in ch["participants"]:
                self.assertIn(pid, self.ents, f"{ch['id']} -> {pid}")
        for fact in load(FIX / "common-knowledge.json")["facts"]:
            for ref in fact["refs"]:
                self.assertIn(ref, self.ents, f"{fact['id']} -> {ref}")

    def test_staging_fragments_match_the_registry_rows(self):
        for frag in sorted((DESIGN / "_staging").rglob("*.json")):
            data = load(frag)
            row = data["registry"]
            self.assertEqual(row, self.ents[data["id"]], frag.name)
            self.assertTrue((FIX / data["prose"]["file"]).is_file(), frag.name)


class DetailedSite(unittest.TestCase):
    """The room table is machine-readable and agrees with the stamp and the progress record."""

    @classmethod
    def setUpClass(cls):
        cls.ents = load(DM_ONLY / "entities.json")["entities"]
        cls.site = cls.ents["site_batik_iskele"]
        text = (FIX / cls.site["file"]).read_text(encoding="utf-8")
        cls.rows = ROOM_ROW.findall(text)
        cls.progress = load(FIX / "site-progress.json")["sites"]["site_batik_iskele"]

    def exits(self, cell: str):
        return [EXIT_ID.match(part).group(1) for part in cell.split(",") if EXIT_ID.match(part)]

    def test_room_count_matches_the_stamp(self):
        self.assertEqual(len(self.rows), self.site["stamped"]["room_count"])
        self.assertEqual({r[0] for r in self.rows}, set(self.progress["rooms"]))

    def test_entrances_payoff_and_exits_resolve(self):
        ids = {r[0] for r in self.rows}
        entrances = [r[0] for r in self.rows if "[Entrance]" in r[1]]
        payoff = [r[0] for r in self.rows if "[Payoff]" in r[1]]
        self.assertGreaterEqual(len(entrances), 2)
        self.assertEqual(len(payoff), 1)
        self.assertEqual(sorted(entrances), sorted(self.progress["entrances"]))
        self.assertEqual(payoff[0], self.progress["payoff_room"])
        for r in self.rows:
            for ex in self.exits(r[3]):
                self.assertIn(ex, ids, f"room {r[0]} exit {ex}")
            self.assertIn(r[2], ("combat", "trap", "special", "structural"), r[0])

    def test_minimum_depth_is_the_shortest_entrance_to_payoff_path(self):
        adj = {r[0]: self.exits(r[3]) for r in self.rows}
        payoff = next(r[0] for r in self.rows if "[Payoff]" in r[1])
        best = None
        for start in (r[0] for r in self.rows if "[Entrance]" in r[1]):
            dist = {start: 1}
            todo = deque([start])
            while todo:
                cur = todo.popleft()
                for nxt in adj[cur]:
                    if nxt not in dist:
                        dist[nxt] = dist[cur] + 1
                        todo.append(nxt)
            if payoff in dist and (best is None or dist[payoff] < best):
                best = dist[payoff]
        self.assertEqual(best, self.site["min_depth"])
        self.assertEqual(best, self.progress["min_depth"])

    def test_xp_sum_equals_the_budget(self):
        self.assertEqual(sum(int(r[4]) for r in self.rows), self.site["xp_budget"])


class Names(unittest.TestCase):

    def test_no_fixture_name_collides_with_the_name_registry(self):
        registry = load(PROJECT / ".name_registry.json")["entries"]
        used = {e["name"].lower() for e in registry.values()}
        used_first = {n.split()[0] for n in used}
        banned = load(DESIGN / "naming.json")["banned"]
        ents = load(DM_ONLY / "entities.json")["entities"]
        for eid, ent in ents.items():
            if ent["type"] in ("npc", "pc", "god", "faction", "settlement"):
                name = ent["name"].lower()
                self.assertNotIn(name, used, eid)
                self.assertNotIn(name.split()[0], used_first, eid)
                for stem in banned:
                    self.assertNotIn(stem, name, f"{eid} uses banned stem {stem}")


class HooksOnTheFixture(unittest.TestCase):

    def test_dice_guard_treats_the_fixture_pcs_as_players(self):
        tmp = Path(tempfile.mkdtemp(prefix="dnd-fixture-"))
        try:
            project = tmp / "proj"
            install_skill(skill_of(project))
            shutil.copytree(FIX, project / "campaigns" / "tuzlu-fener")
            (project / ".runtime").mkdir()
            (project / ".runtime" / "active-campaign.json").write_text(
                json.dumps({"name": "tuzlu-fener"}), encoding="utf-8")
            env = clean_env()
            roll = 'py .claude/skills/dnd/scripts/dice.py d20+3 --owner Selen --label "Stealth"'
            self.assertEqual(run_hook(skill_of(project), "dice_guard.py", bash_payload(roll), env).returncode, 2)
            roll = 'py .claude/skills/dnd/scripts/dice.py d20+3 --owner "Vorin Tegrik" --label "Athletics"'
            self.assertEqual(run_hook(skill_of(project), "dice_guard.py", bash_payload(roll), env).returncode, 2)
            roll = 'py .claude/skills/dnd/scripts/dice.py d20+2 --owner "Kortan" --label "Deception"'
            self.assertEqual(run_hook(skill_of(project), "dice_guard.py", bash_payload(roll), env).returncode, 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
