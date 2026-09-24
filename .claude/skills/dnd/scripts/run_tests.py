#!/usr/bin/env python3
"""
run_tests.py — run the skill's test suite (stdlib unittest; pytest is not installed).

Run:  py .claude/skills/dnd/scripts/run_tests.py [-v] [pattern]

Discovers `tests/test_*.py` under the skill directory. A pattern narrows the
run (`test_paths*`). Exit 0 when everything passes, 1 otherwise.
"""

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent.parent / "tests"


def main(argv) -> int:
    verbosity = 2 if "-v" in argv else 1
    pattern = next((a for a in argv if not a.startswith("-")), "test_*.py")
    suite = unittest.defaultTestLoader.discover(str(TESTS), pattern=pattern,
                                                top_level_dir=str(TESTS))
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
