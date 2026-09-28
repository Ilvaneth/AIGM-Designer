"""
_campaign.py — a throwaway copy of the fixture bible for script tests.

Root resolution is project-scoped, so a script under this project's skill
always finds campaigns under <project>/campaigns/. Tests therefore copy the
fixture to campaigns/_test-<name>-<pid>/ (gitignored, plan item 22.6) and
remove it afterwards. Scripts are driven as subprocesses, the way the DM runs
them, with a clean environment.
"""

import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCRIPTS = SKILL / "scripts"
PROJECT = SKILL.parent.parent.parent
FIXTURE = HERE / "fixtures" / "salt-lantern"
CAMPAIGNS = PROJECT / "campaigns"


USED = PROJECT / "used.json"


class TestCampaign:
    """Copy the fixture under campaigns/_test-*/; `run` drives a script against it. The project's used.json is
    snapshotted when the first live test campaign is made and restored when the last is removed: an approve a
    test drives stamps the birth order there, and a test must leave the owner's store as it found it."""

    _live = 0
    _used_snapshot = None

    def __init__(self, label: str):
        self.name = f"_test-{label}-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        self.dir = CAMPAIGNS / self.name
        if TestCampaign._live == 0:
            TestCampaign._used_snapshot = USED.read_bytes() if USED.is_file() else None
        TestCampaign._live += 1
        self._removed = False
        shutil.copytree(FIXTURE, self.dir)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}

    def remove(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        if self._removed:
            return
        self._removed = True
        TestCampaign._live -= 1
        if TestCampaign._live == 0:
            if TestCampaign._used_snapshot is not None:
                USED.write_bytes(TestCampaign._used_snapshot)
            elif USED.is_file():
                USED.unlink()

    def run(self, script: str, *args: str, check: bool = False) -> subprocess.CompletedProcess:
        proc = subprocess.run([sys.executable, str(SCRIPTS / script), "-c", self.name, *args],
                              capture_output=True, text=True, env=self.env, encoding="utf-8")
        if check and proc.returncode != 0:
            raise AssertionError(f"{script} {' '.join(args)} failed ({proc.returncode}):\n"
                                 f"{proc.stdout}\n{proc.stderr}")
        return proc

    def path(self, rel: str) -> Path:
        return self.dir / rel

    def json(self, rel: str):
        return json.loads(self.path(rel).read_text(encoding="utf-8"))

    def write_json(self, rel: str, data) -> None:
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def temp_files(self) -> list:
        return [p for p in self.dir.rglob(".*.tmp")]

    def reopen(self, phase: str, status: str = "merged", **fields) -> None:
        """The fixture's phases are all approved and an approved phase is frozen; tests that drive a phase reopen it first."""
        m = self.json("design/design.json")
        m["phases"][phase]["status"] = status
        m["phases"][phase].update(fields)
        self.write_json("design/design.json", m)


class MarkerGuard:
    """Keep the real runtime marker (the read guard's active-design.json) out of a test's way and
    never leave the guard armed behind: designer.py arms it, and an armed marker blocks the
    developer's own shell."""

    def __init__(self):
        sys.path.insert(0, str(SCRIPTS))
        from paths import runtime_dir
        self.marker = runtime_dir() / "active-design.json"

    def __enter__(self):
        self.backup = self.marker.read_bytes() if self.marker.is_file() else None
        if self.marker.is_file():
            self.marker.unlink()
        return self

    def __exit__(self, *exc):
        if self.marker.is_file():
            self.marker.unlink()
        if self.backup is not None:
            self.marker.write_bytes(self.backup)
        return False
