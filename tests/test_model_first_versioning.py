"""Regression checks for release-version behavior coverage."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_model_first_versioning as versioning


class VersionCoverageTests(unittest.TestCase):
    def test_untracked_behavior_file_requires_version_bump(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", root], check=True)
            subprocess.run(["git", "-C", root, "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", root, "config", "user.name", "Test"], check=True)
            (root / "VERSION").write_text("0.1.0\n")
            subprocess.run(["git", "-C", root, "add", "VERSION"], check=True)
            subprocess.run(["git", "-C", root, "commit", "-qm", "initial"], check=True)
            subprocess.run(["git", "-C", root, "update-ref", "refs/remotes/origin/main", "HEAD"], check=True)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "new_behavior.py").write_text("print('new')\n")

            self.assertTrue(versioning.behavior_changed_from_base(root))


if __name__ == "__main__":
    unittest.main()
