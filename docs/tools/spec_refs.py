"""The design tab's last-read check (owner, 2026-10-08): every backticked reference in a specification is looked up
in the repository, so a wrong id, path or table never reaches the coding tab.

    py docs/tools/spec_refs.py docs/p2-build-22.md [more specs...]

A reference is reported as missing when it is a path that does not exist, a `file.yaml#table` whose table is not there,
or a row-like id (lowercase words joined by underscores) that no table, script or test names. New rows a specification
introduces are expected among the missing: read the list, never trust it blindly."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".claude" / "skills" / "dnd"
DATA = SKILL / "data" / "design"
TICK = re.compile(r"`([^`\n]+)`")
ROWLIKE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


def corpus() -> str:
    parts = []
    for base, globs in ((DATA, ("*.yaml",)), (SKILL / "scripts", ("*.py",)), (SKILL / "tests", ("*.py",)),
                        (SKILL / "prompts", ("**/*.md",)), (SKILL / "templates", ("**/*.md",))):
        for g in globs:
            for f in base.glob(g):
                parts.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def find_path(ref: str) -> bool:
    ref = ref.split(":")[0].rstrip("/")
    return any((b / ref).exists() for b in (ROOT, ROOT / "docs", SKILL, DATA, SKILL / "scripts", SKILL / "tests"))


def table_exists(ref: str) -> bool:
    name, _, sub = ref.partition("#")
    f = DATA / name
    if not f.exists():
        return False
    text = f.read_text(encoding="utf-8")
    return not sub or re.search(rf"^\s+{re.escape(sub)}:\s*$", text, re.M) is not None


def main(specs: list[str]) -> int:
    text_all = corpus()
    missing = 0
    for spec in specs:
        seen = set()
        for ref in TICK.findall(Path(spec).read_text(encoding="utf-8")):
            ref = ref.strip()
            if ref in seen:
                continue
            seen.add(ref)
            if "#" in ref and ref.split("#")[0].endswith(".yaml"):
                ok, kind = table_exists(ref), "table"
            elif "/" in ref or re.search(r"\.(py|md|yaml|json|js)$", ref):
                ok, kind = find_path(ref), "path"
            elif ROWLIKE.match(ref):
                ok, kind = re.search(rf"(?<![A-Za-z0-9_]){re.escape(ref)}(?![A-Za-z0-9_])", text_all) is not None, "id"
            else:
                continue
            if not ok:
                missing += 1
                print(f"{spec}: {kind} not found: {ref}")
    print(f"spec_refs: {missing} reference(s) not found (new rows a specification adds are expected here)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
