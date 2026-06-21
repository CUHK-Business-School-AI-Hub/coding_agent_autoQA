from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_TRANSLATIONS = REPO_ROOT / "autoqa-skill" / "scripts" / "check_translations.py"
GROUPS = (
    ("README.md", "README_CN.md", "README_HK.md"),
    (
        "autoqa-skill/references/rookie-qa-pedia.md",
        "autoqa-skill/references/rookie-qa-pedia_CN.md",
        "autoqa-skill/references/rookie-qa-pedia_HK.md",
    ),
    (
        "autoqa-skill/assets/templates/HUMAN-E2E.md",
        "autoqa-skill/assets/templates/HUMAN-E2E_CN.md",
        "autoqa-skill/assets/templates/HUMAN-E2E_HK.md",
    ),
)


class TranslationCheckTest(unittest.TestCase):
    def make_fixture(self, mismatch: bool = False, version_mismatch: bool = False) -> Path:
        root = Path(self.temp.name)
        for group_index, group in enumerate(GROUPS):
            names = " ".join(Path(path).name for path in group)
            for member_index, relative in enumerate(group):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                key = "different" if mismatch and group_index == 0 and member_index == 2 else "section"
                version = "2026-06-20" if version_mismatch and group_index == 1 and member_index == 1 else "2026-06-21"
                path.write_text(
                    f"<!-- sync-version: {version} -->\n<!-- sync-key: {key} -->\n{names}\n",
                    encoding="utf-8",
                )
        return root

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_check(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECK_TRANSLATIONS), "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_matching_groups_pass(self) -> None:
        result = self.run_check(self.make_fixture())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_key_drift_fails(self) -> None:
        result = self.run_check(self.make_fixture(mismatch=True))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sync-key mismatch", result.stdout)

    def test_version_drift_fails(self) -> None:
        result = self.run_check(self.make_fixture(version_mismatch=True))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sync-version mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
