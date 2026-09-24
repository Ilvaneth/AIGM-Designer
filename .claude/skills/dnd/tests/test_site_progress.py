"""
test_site_progress.py — room-by-room records: open from the room table, enter
through an entrance, seen/cleared/skipped with reasons, shortcuts, the save
line, and the overlay's played / seen_in_play written on first entry.
"""

import unittest

from _campaign import TestCampaign

SITE = "site_batik_iskele"


class SiteProgress(unittest.TestCase):

    def setUp(self):
        self.c = TestCampaign("progress")

    def tearDown(self):
        self.c.remove()

    def sp(self, *args, check=True):
        return self.c.run("site_progress.py", *args, check=check)

    def test_open_reads_the_room_table(self):
        proc = self.sp("open", SITE, "--force")
        self.assertIn("6 rooms, entrances 1, 4, payoff 6, minimum depth 3", proc.stdout)
        rec = self.c.json("site-progress.json")["sites"][SITE]
        self.assertEqual(sorted(rec["rooms"]), ["1", "2", "3", "4", "5", "6"])
        self.assertEqual(self.sp("open", SITE, check=False).returncode, 1, "already open without --force")

    def test_open_refuses_a_skeleton_without_explicit_rooms(self):
        proc = self.sp("open", "site_kor_fener", check=False)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("no room table", proc.stderr)
        proc = self.sp("open", "site_kor_fener", "--entrances", "1,9", "--payoff", "13", "--rooms", "14",
                       "--min-depth", "7")
        self.assertIn("14 rooms", proc.stdout)

    def test_enter_marks_seen_and_writes_the_overlay_on_first_entry(self):
        proc = self.sp("enter", SITE, "1", "--day", "3", "--session", "1")
        self.assertIn("first entry", proc.stdout)
        rec = self.c.json("site-progress.json")["sites"][SITE]
        self.assertEqual((rec["opened_day"], rec["entered_via"], rec["current_room"]), (3, "1", "1"))
        self.assertEqual(rec["rooms"]["1"]["state"], "seen")
        ov = self.c.json("design/overlay.json")["entries"][SITE]
        self.assertEqual((ov["status"]["value"], ov["status"]["writer"], ov["status"]["birth"]),
                         ("played", "site_progress.py", "skeleton"))
        self.assertIs(ov["seen_in_play"]["value"], True)
        self.sp("enter", SITE, "2", "--day", "3", "--session", "1")
        self.assertEqual(self.c.json("site-progress.json")["sites"][SITE]["current_room"], "2")

    def test_first_entry_must_be_an_entrance(self):
        proc = self.sp("enter", SITE, "5", "--day", "3", "--session", "1", check=False)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not an entrance", proc.stderr)

    def test_clear_skip_shortcut_rest_and_status_line(self):
        self.sp("enter", SITE, "4", "--day", "3", "--session", "1")
        self.sp("clear", SITE, "5", "--day", "3", "--session", "1")
        self.sp("skip", SITE, "2", "--reason", "kumsaldan girdiler, üst ambara çıkmadılar", "--day", "3", "--session", "1")
        self.sp("shortcut", SITE, "--from", "4", "--to", "6", "--how", "Kortan'ın anahtarı", "--day", "3")
        self.sp("rest", SITE, "5", "--kind", "short", "--day", "3")
        self.sp("note", SITE, "kandil söndü")
        rec = self.c.json("site-progress.json")["sites"][SITE]
        self.assertEqual(rec["rooms"]["5"]["state"], "cleared")
        self.assertEqual(rec["rooms"]["2"]["reason"], "kumsaldan girdiler, üst ambara çıkmadılar")
        self.assertEqual(rec["shortcuts_earned"][0]["to"], "6")
        self.assertEqual(rec["rests"][0]["kind"], "short")
        self.assertEqual(rec["notes"], ["kandil söndü"])
        proc = self.sp("status")
        self.assertIn("Batık İskele: 3/6 oda, 1 temizlendi, 1 atlandı — şu an oda 5", proc.stdout)
        self.assertEqual(self.c.temp_files(), [])

    def test_unknown_room_and_missing_record_are_refused(self):
        self.assertEqual(self.sp("enter", SITE, "9", "--day", "1", "--session", "1", check=False).returncode, 1)
        self.assertEqual(self.sp("clear", "site_gelgit_magarasi", "1", "--day", "1", "--session", "1",
                                 check=False).returncode, 1)


if __name__ == "__main__":
    unittest.main()
