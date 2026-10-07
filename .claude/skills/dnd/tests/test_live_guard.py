"""
test_live_guard.py — build 19c: the tests never touch a live guard, and a script that rewrites a tracked file keeps
that file's line endings.

The suite runs on its own runtime directory (AIGM_TEST_RUNTIME, set by _campaign.py at import; paths.runtime_dir()
honours it inside the temporary directory only), so a suite run in the main working tree during a live birth leaves
the project's .runtime/active-design.json as it found it: not removed, not rewritten, not read.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from _campaign import PROJECT, RUNTIME, SCRIPTS, MarkerGuard, TestCampaign
from _layouts import clean_env

sys.path.insert(0, str(SCRIPTS))
import paths  # noqa: E402
import build_design_index as bdi  # noqa: E402

TESTS = Path(__file__).resolve().parent
LIVE = PROJECT / ".runtime" / "active-design.json"

# a campaign test that arms the guard (designer.py new) and one that disarms it (designer.py abandon)
CAMPAIGN_TESTS = ("test_designer.NewBirth.test_new_rolls_blank_dials_and_auto_approves_p0",
                  "test_designer.NewBirth.test_abandon_disarms_and_drops_used_rows")


class SuiteRuntime(unittest.TestCase):

    def test_the_suite_runtime_is_its_own(self):
        here = paths.runtime_dir().resolve()
        self.assertEqual(here, RUNTIME.resolve())
        self.assertNotEqual(here, (PROJECT / ".runtime").resolve())
        self.assertTrue(here.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.assertEqual(MarkerGuard().marker.resolve(), here / "active-design.json")

    def test_a_script_a_test_starts_uses_it(self):
        c = TestCampaign("live-guard")
        try:
            out = subprocess.run([sys.executable, str(SCRIPTS / "paths.py"), "runtime-dir"], capture_output=True,
                                 text=True, env=c.env, encoding="utf-8", check=True).stdout.strip()
        finally:
            c.remove()
        self.assertEqual(Path(out).resolve(), RUNTIME.resolve())

    def test_the_override_is_honoured_inside_the_temporary_directory_only(self):
        with mock.patch.dict(os.environ, {"AIGM_TEST_RUNTIME": str(PROJECT / "not-a-temp-runtime")}):
            self.assertIsNone(paths.test_runtime())
            self.assertEqual(paths.runtime_dir().resolve(), (PROJECT / ".runtime").resolve())
        self.assertFalse((PROJECT / "not-a-temp-runtime").exists())
        with mock.patch.dict(os.environ, {"AIGM_TEST_RUNTIME": tempfile.gettempdir()}):
            self.assertIsNone(paths.test_runtime(), "the temporary directory itself is not a test's own")
        with mock.patch.dict(os.environ, {"AIGM_TEST_RUNTIME": ""}):
            self.assertEqual(paths.runtime_dir().resolve(), (PROJECT / ".runtime").resolve())

    def test_a_test_process_leaves_no_used_folder(self):
        """Build item 20b: each test process makes its own used.json folder and removes it at exit."""
        env = {k: v for k, v in os.environ.items() if k not in ("AIGM_TEST_RUNTIME", "DESIGN_USED_PATH")}
        out = subprocess.run([sys.executable, "-c", "import _campaign; print(_campaign.USED.parent); print(_campaign.RUNTIME)"],
                             cwd=str(TESTS), capture_output=True, text=True, env=env, encoding="utf-8", check=True).stdout.split()
        used, runtime = Path(out[0]), Path(out[1])
        self.assertTrue(used.name.startswith("aigm-used-"))
        self.assertFalse(used.exists(), "the used.json folder outlived its process")
        self.assertFalse(runtime.exists(), "the runtime folder outlived its process")

    def test_a_layout_project_keeps_its_own_runtime(self):
        self.assertNotIn("AIGM_TEST_RUNTIME", clean_env())


class LiveMarker(unittest.TestCase):
    """A live marker (or a sentinel standing in for one) survives campaign tests that arm and disarm the guard:
    the same bytes and the same modification time, so it was never removed and written back."""

    def test_campaign_tests_leave_the_live_marker_untouched(self):
        sentinel = None
        if not LIVE.is_file():
            LIVE.parent.mkdir(parents=True, exist_ok=True)
            sentinel = json.dumps({"campaign": f"_test-live-guard-sentinel-{os.getpid()}",
                                   "mode": "design", "note": "test_live_guard.py; removed at the test's end"}).encode()
            LIVE.write_bytes(sentinel)
        try:
            before = (LIVE.read_bytes(), LIVE.stat().st_mtime_ns)
            # a fresh process, as a real suite run: _campaign.py makes its own runtime directory there
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith(("DND_", "CLAUDE_")) and k != "AIGM_TEST_RUNTIME"}
            proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", *CAMPAIGN_TESTS], cwd=str(TESTS),
                                  capture_output=True, text=True, env=env, encoding="utf-8")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(LIVE.is_file(), "a campaign test removed the live marker")
            self.assertEqual((LIVE.read_bytes(), LIVE.stat().st_mtime_ns), before,
                             "a campaign test rewrote the live marker")
        finally:
            if sentinel is not None and LIVE.is_file() and LIVE.read_bytes() == sentinel:
                LIVE.unlink()


class KeepLineEndings(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="aigm-eol-"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_the_helper_keeps_crlf_and_lf_and_writes_a_new_file_in_lf(self):
        crlf, lf, new = self.tmp / "crlf.txt", self.tmp / "lf.txt", self.tmp / "new.txt"
        crlf.write_bytes(b"a\r\nb\r\n")
        lf.write_bytes(b"a\nb\n")
        for p in (crlf, lf, new):
            paths.write_text_keeping_eol(p, "x\ny\r\nz\n")
        self.assertEqual(crlf.read_bytes(), b"x\r\ny\r\nz\r\n")
        self.assertEqual(lf.read_bytes(), b"x\ny\nz\n")
        self.assertEqual(new.read_bytes(), b"x\ny\nz\n")

    def test_the_index_build_keeps_its_files_line_endings(self):
        eco, idx = bdi.output_paths()
        eco_copy, idx_copy = self.tmp / eco.name, self.tmp / idx.name
        eco_copy.write_bytes(eco.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        idx_copy.write_bytes(idx.read_bytes().replace(b"\r\n", b"\n"))
        before = (eco_copy.read_bytes(), idx_copy.read_bytes())
        with mock.patch.object(bdi, "output_paths", return_value=(eco_copy, idx_copy)):
            self.assertEqual(bdi.main([]), 0)
        self.assertEqual((eco_copy.read_bytes(), idx_copy.read_bytes()), before)

    def test_every_script_that_rewrites_a_tracked_file_keeps_its_endings(self):
        for name in ("build_design_index.py", "design_tables.py", "merge_srd_defenses.py", "build_rules_index.py",
                     "build_srd.py", "build_supplemental.py", "data_pull.py"):
            text = (SCRIPTS / name).read_text(encoding="utf-8")
            self.assertIn("write_text_keeping_eol(", text, name)
            self.assertNotIn('newline="\\n")', text, name)


if __name__ == "__main__":
    unittest.main()
