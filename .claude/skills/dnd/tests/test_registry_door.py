"""
test_registry_door.py — the registry door after critique analysis 1 (2026-09-26): the classes the critics spent
most fix loops on are refused at merge, deterministically. A public row may keep a canonical link to a secret
entity, but the projection never carries a secret id; a mirror sentence repeated in the public file or restated
in the public notes is refused; a public notes file naming a secret entity is refused; a stub needs
`status: pending`; a secret npc's id is opaque; names on the blacklist, Turkish letters in a name, a Turkish
common noun as a name, a name another campaign registered, and duplicate names within a group are refused;
descriptive lowercase Turkish aliases stay allowed.
"""

import json
import sys
import unittest

from _campaign import TestCampaign, MarkerGuard, SCRIPTS

sys.path.insert(0, str(SCRIPTS))

from test_tuning_birth_1 import FRONT, fragment, row  # noqa: E402


class Door(unittest.TestCase):

    def setUp(self):
        self.guard = MarkerGuard().__enter__()
        self.c = TestCampaign("door")

    def tearDown(self):
        self.c.remove()
        self.guard.__exit__(None, None, None)

    def merge(self, phase="P5"):
        return self.c.run("registry.py", "merge", "--phase", phase)

    def canonical(self):
        return self.c.json("design/dm-only/entities.json")["entities"]

    def test_projection_never_carries_a_secret_id(self):
        canon = self.canonical()
        self.assertIn("npc_s01", canon["item_consumed_ledger"]["refs"], "the canonical link stays")
        pub = self.c.json("design/entities.json")["entities"]
        self.assertNotIn("npc_s01", pub["item_consumed_ledger"]["refs"])
        self.assertFalse([r for r in pub["npc_draskun"].get("relations") or [] if r.get("to") == "npc_s01"])
        self.assertNotIn("npc_s01", json.dumps(pub))

    def test_mirror_sentences_and_secret_names_in_public_files_or_notes_are_refused(self):
        pub = self.c.path("design/npcs/npc_tune_m.md")
        mir = self.c.path("design/dm-only/npcs/npc_tune_m.md")
        secret_line = "Gerçekte kırk yıl önce feneri kendisi söndürdü ve o geceyi kimseye anlatmadı."
        pub.write_text(FRONT.format(eid="npc_tune_m", etype="npc", secrecy="public", phase="P5", link="mirror: design/dm-only/npcs/npc_tune_m.md") + "\n" + secret_line + "\n", encoding="utf-8")
        mir.write_text(FRONT.format(eid="npc_tune_m", etype="npc", secrecy="secret", phase="P5", link="mirror_of: design/npcs/npc_tune_m.md").replace("## Public", "## Secret") + "\n" + secret_line + "\n", encoding="utf-8")
        frag = fragment("npc_tune_m", row("npc_tune_m", "npc", "Marrow Quill", file="design/npcs/npc_tune_m.md"),
                        prose={"file": "design/npcs/npc_tune_m.md"}, dm_only_prose={"file": "design/dm-only/npcs/npc_tune_m.md"})
        self.c.write_json("design/_staging/P5/npc_tune_m.json", frag)
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("repeated verbatim in the public file", proc.stderr)
        pub.write_text(FRONT.format(eid="npc_tune_m", etype="npc", secrecy="public", phase="P5", link="mirror: design/dm-only/npcs/npc_tune_m.md"), encoding="utf-8")
        notes = self.c.path("design/_staging/P5/npc_tune_m.notes.md")
        notes.write_text("Konduktöre not: " + secret_line + "\n", encoding="utf-8")
        self.c.write_json("design/_staging/P5/npc_tune_m.json", frag)
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("restates the mirror", proc.stderr)
        secret_name = self.canonical()["npc_s01"]["name"]
        notes.write_text(f"Konduktöre not: {secret_name} bu sahnede görünmez.\n", encoding="utf-8")
        self.c.write_json("design/_staging/P5/npc_tune_m.json", frag)
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("names 1 secret entity", proc.stderr)
        notes.write_text("Konduktöre not: sesi kısık, gözleri hep kapıda.\n", encoding="utf-8")
        self.c.write_json("design/_staging/P5/npc_tune_m.json", frag)
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)

    def test_stubs_need_pending_and_secret_npcs_an_opaque_id(self):
        self.c.write_json("design/_staging/P5/npc_tune_nofile.json", fragment("npc_tune_nofile", row("npc_tune_nofile", "npc", "Dorran Vale", file=None)))
        self.c.write_json("design/_staging/P5/npc_hidden_baron.json", fragment("npc_hidden_baron", row("npc_hidden_baron", "npc", "Opaque Nine", secrecy="secret")))
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("without a file is a stub", proc.stderr)
        self.assertIn("a secret npc's id is opaque", proc.stderr)
        ok = row("npc_tune_stub2", "npc", "Dorran Vale", status="pending", owner_phase="detail", reserved_by="thread_selen")
        self.c.write_json("design/_staging/P5/npc_tune_stub2.json", fragment("npc_tune_stub2", ok))
        proc = self.merge()
        self.assertIn("npc_tune_stub2", self.canonical())

    def test_blacklist_turkish_names_registered_names_and_duplicates_are_refused(self):
        cases = {
            "npc_tune_odin": row("npc_tune_odin", "npc", "Odin Harker"),
            "npc_tune_corvane": row("npc_tune_corvane", "npc", "Corvane Tull"),
            "npc_tune_kael": row("npc_tune_kael", "npc", "Kael Brightwater"),
            "settlement_tune_kizil": row("settlement_tune_kizil", "settlement", "Kızıl Kule"),
            "faction_tune_konsey": row("faction_tune_konsey", "faction", "The Reed Board", aliases=["Konsey"]),
            "npc_tune_rendric": row("npc_tune_rendric", "npc", "Rendric Corr"),
            "npc_tune_sarven2": row("npc_tune_sarven2", "npc", "Sarven Holt"),
            "site_tune_pier2": row("site_tune_pier2", "site", "Sunken Pier"),
        }
        for eid, r in cases.items():
            self.c.write_json(f"design/_staging/P5/{eid}.json", fragment(eid, r))
        proc = self.merge()
        self.assertEqual(proc.returncode, 1)
        err = proc.stderr
        self.assertIn("npc_tune_odin: 'Odin Harker' is on naming.yaml's blacklist", err)
        self.assertIn("npc_tune_corvane: 'Corvane Tull' carries a banned stem", err)
        self.assertIn("npc_tune_kael: 'Kael Brightwater' is on naming.yaml's blacklist", err)
        self.assertIn("carries Turkish letters", err)
        self.assertIn("'Konsey' is a Turkish common noun used as a proper name", err)
        self.assertIn("is a name another campaign registered", err)
        self.assertIn("first name 'sarven' collides with npc_sarven's", err)
        self.assertIn("name 'Sunken Pier' is already site_sunken_pier's", err)
        for eid in cases:
            self.assertNotIn(eid, self.canonical())
        # allowed: a lowercase Turkish descriptor as an alias, a signature named like a faction, a fresh name
        fine = row("npc_tune_fine", "npc", "Wender Hask", aliases=["hancı", "the Wick"])
        self.c.write_json("design/_staging/P5/npc_tune_fine.json", fragment("npc_tune_fine", fine))
        self.c.run("registry.py", "merge", "--phase", "P5", check=True)
        self.assertIn("npc_tune_fine", self.canonical())


if __name__ == "__main__":
    unittest.main()
