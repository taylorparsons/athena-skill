"""Repository-only regression for maintained root/install copies."""
import unittest
from pathlib import Path


class TestPackageParity(unittest.TestCase):
    def test_mirrored_resources_match(self):
        root = Path(__file__).resolve().parents[2]
        package = root / "skills/athena"
        if not package.is_dir():
            self.skipTest("standalone installed skill has no repository mirror")
        paths = ["SKILL.md", "scripts/owl.py", "scripts/tests/test_owl.py",
                 "scripts/tests/test_recovery.py", "references/commits.md",
                 "references/recovery.md", "references/evaluation.md", "references/setup.md",
                 "references/benchmarks.md", "references/benchmark-cases.json"]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual((root / path).read_bytes(), (package / path).read_bytes())
