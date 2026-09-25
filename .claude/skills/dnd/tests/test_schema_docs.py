"""
test_schema_docs.py — every JSON example in docs/schemas/ is valid JSON.

The schema docs are the contract slice 1's scripts implement; an example that
does not parse is a contract nobody can read. Each fenced ```json block is
parsed on its own, and the ones that carry a `_meta` block are checked for the
keys every store shares.
"""

import json
import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
PROJECT = SKILL.parent.parent.parent
SCHEMAS = PROJECT / "docs" / "schemas"

BLOCK = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
META_KEYS = {"schema_version", "campaign", "written_by", "written_at"}
EXPECTED_DOCS = {"README.md", "entities.md", "overlay.md", "design-manifest.md", "map.md",
                 "news.md", "site-progress.md", "staging-fragment.md",
                 "naming-and-common-knowledge.md"}


def blocks(path: Path):
    return BLOCK.findall(path.read_text(encoding="utf-8"))


class SchemaDocs(unittest.TestCase):

    def test_every_expected_doc_exists(self):
        self.assertTrue(SCHEMAS.is_dir(), SCHEMAS)
        present = {p.name for p in SCHEMAS.glob("*.md")}
        self.assertEqual(EXPECTED_DOCS - present, set())

    def test_every_json_block_parses(self):
        seen = 0
        for doc in sorted(SCHEMAS.glob("*.md")):
            for i, block in enumerate(blocks(doc)):
                with self.subTest(doc=doc.name, block=i):
                    json.loads(block)
                    seen += 1
        self.assertGreater(seen, 10, "expected at least a dozen examples")

    def test_store_examples_carry_the_shared_meta_keys(self):
        for doc in sorted(SCHEMAS.glob("*.md")):
            for i, block in enumerate(blocks(doc)):
                data = json.loads(block)
                if isinstance(data, dict) and "_meta" in data:
                    with self.subTest(doc=doc.name, block=i):
                        self.assertEqual(META_KEYS - set(data["_meta"]), set())
                        self.assertEqual(data["_meta"]["campaign"], "salt-lantern")

    def test_readme_links_every_doc(self):
        readme = (SCHEMAS / "README.md").read_text(encoding="utf-8")
        for name in EXPECTED_DOCS - {"README.md"}:
            self.assertIn(f"]({name})", readme, name)


if __name__ == "__main__":
    unittest.main()
