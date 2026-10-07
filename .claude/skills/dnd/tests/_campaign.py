"""
_campaign.py — a throwaway copy of the fixture bible for script tests.

Root resolution is project-scoped, so a script under this project's skill
always finds campaigns under <project>/campaigns/. Tests therefore copy the
fixture to campaigns/_test-<name>-<pid>/ (gitignored, plan item 22.6) and
remove it afterwards. Scripts are driven as subprocesses, the way the DM runs
them, with a clean environment.

The suite's runtime directory is its own (AIGM_TEST_RUNTIME, a temporary
directory paths.runtime_dir() honours inside the temporary directory only):
no test arms, disarms or reads a live birth's guard marker (build 19c).
"""

import atexit
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCRIPTS = SKILL / "scripts"
PROJECT = SKILL.parent.parent.parent
FIXTURE = HERE / "fixtures" / "salt-lantern"
CAMPAIGNS = PROJECT / "campaigns"


# every test reads and writes its own used.json, never the owner's (design_dice.used_path; owner, 2026-09-28): the
# variable is set when the first test module imports this one, so in-process calls and subprocesses both see it
USED = Path(tempfile.mkdtemp(prefix="aigm-used-")) / "used.json"
os.environ["DESIGN_USED_PATH"] = str(USED)
atexit.register(shutil.rmtree, USED.parent, ignore_errors=True)     # build 20b: one folder per process, removed at its exit

# the suite's own runtime directory, set before any test computes a path, so the guard marker every test arms,
# disarms or reads is never the project's .runtime/active-design.json (build 19c); a test process started by
# another test inherits its parent's directory, and only the process that made it removes it
if not os.environ.get("AIGM_TEST_RUNTIME"):
    RUNTIME = Path(tempfile.mkdtemp(prefix="aigm-runtime-"))
    os.environ["AIGM_TEST_RUNTIME"] = str(RUNTIME)
    atexit.register(shutil.rmtree, RUNTIME, ignore_errors=True)
else:
    RUNTIME = Path(os.environ["AIGM_TEST_RUNTIME"])


class TestCampaign:
    """Copy the fixture under campaigns/_test-*/; `run` drives a script against it."""

    def __init__(self, label: str):
        self.name = f"_test-{label}-{os.getpid()}-{uuid.uuid4().hex[:6]}"
        self.dir = CAMPAIGNS / self.name
        shutil.copytree(FIXTURE, self.dir)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(("DND_", "CLAUDE_"))}

    def remove(self):
        shutil.rmtree(self.dir, ignore_errors=True)

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
    """Start and end a test with the suite's runtime marker (the read guard's active-design.json)
    disarmed: designer.py arms it. The marker is the suite's own (RUNTIME above), never a live birth's."""

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
