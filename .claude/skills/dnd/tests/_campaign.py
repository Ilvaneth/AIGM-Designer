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
FIXTURE = HERE / "fixtures" / "tuzlu-fener"
CAMPAIGNS = PROJECT / "campaigns"


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
