"""Authenticated entry-point lifecycle using real isolated local Git remotes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import board as b
import checkpoint as c

ROOT = Path(__file__).resolve().parents[3]
ENTRY = ROOT / c.SCOPE / "tools/board.sh"


class EntryTests(unittest.TestCase):
    def setUp(self):
        common = (ROOT / c.value(ROOT, "rev-parse", "--git-common-dir")).resolve()
        self.tmp = tempfile.TemporaryDirectory(prefix="board-entry-test-", dir=common)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote, self.repo = self.root / "remote.git", self.root / "work"
        c.git(self.root, "init", "--bare", str(self.remote))
        c.git(self.root, "clone", str(self.remote), str(self.repo))
        c.git(self.repo, "config", "user.name", "Fixture")
        c.git(self.repo, "config", "user.email", "fixture@example.invalid")
        (self.repo / "asset.md").write_text("baseline\n")
        c.git(self.repo, "add", ".")
        c.git(self.repo, "commit", "-m", "fixture")
        self.client = b.Board(self.repo)
        self.client.initialize()
        self.token = "ghp_" + "fixture" * 5
        self.credential = self.root / "credential with spaces.txt"
        self.credential.write_text(self.token + "\n")

    def entry(self, *args, cwd=None):
        env = {k: v for k, v in os.environ.items()
               if k not in (*c.ROUTING, "WCG_CHECKPOINT_TOKEN_FILE",
                            "WCG_CHECKPOINT_ASKPASS", "GIT_ASKPASS")}
        return subprocess.run(["bash", str(ENTRY), *args], cwd=cwd or self.repo,
                              env=env, capture_output=True, text=True, timeout=45)

    def test_explicit_then_remembered_file_and_dirty_work(self):
        (self.repo / "asset.md").write_text("uncommitted research\n")
        before = c.value(self.repo, "rev-parse", "HEAD")
        first = self.entry("--token-file", str(self.credential), "register",
                           "--runtime-id", "python-fixture")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(c.value(self.repo, "config", "--get", "wcg.tokenFile"),
                         str(self.credential))
        second = self.entry("view", "--json")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn(json.loads(first.stdout)["actor"], json.loads(second.stdout)["members"])
        self.assertNotIn(self.token, first.stdout + first.stderr + second.stdout + second.stderr)
        self.assertNotIn(self.token, (self.repo / ".git/config").read_text())
        self.assertEqual(c.value(self.repo, "rev-parse", "HEAD"), before)
        self.assertEqual((self.repo / "asset.md").read_text(), "uncommitted research\n")
        # The configured shared ASKPASS handles a real Git prompt for this exact host.
        env = dict(os.environ, GIT_ASKPASS=str(ROOT / c.SCOPE / "tools/checkpoint.py"),
                   WCG_CHECKPOINT_ASKPASS="1", WCG_CHECKPOINT_TOKEN_FILE=str(self.credential))
        output = subprocess.check_output([env["GIT_ASKPASS"], "Password for 'https://github.com':"], env=env)
        self.assertEqual(output.decode().strip(), self.token)

    def test_repo_argument_from_outside_and_native_auth(self):
        result = self.entry("--repo", str(self.repo), "view", "--json", cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["members"], {})
        self.assertNotEqual(c.git(self.repo, "config", "--get", "wcg.tokenFile", check=False).returncode, 0)

    def test_inside_or_invalid_credentials_fail_before_registration(self):
        inside = self.repo / "credential.txt"
        inside.write_text(self.token)
        for path in (inside, self.root / "missing.txt"):
            result = self.entry("--token-file", str(path), "register", "--runtime-id", "fixture")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(self.token, result.stdout + result.stderr)
        self.credential.write_text("not a token\n")
        result = self.entry("--token-file", str(self.credential), "register", "--runtime-id", "fixture")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.client.read()["members"], {})
        self.assertNotEqual(c.git(self.repo, "config", "--get", "wcg.tokenFile", check=False).returncode, 0)

    def test_stale_remembered_file_is_an_explicit_failure(self):
        c.git(self.repo, "config", "wcg.tokenFile", str(self.credential))
        self.credential.unlink()
        result = self.entry("view")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR:", result.stderr)

    def test_help_and_board_error_exit_codes_are_preserved(self):
        help_result = self.entry("--help", cwd=self.root)
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("register", help_result.stdout)
        bad = self.entry("register", "--runtime-id", "fixture", "--budget-seconds", "0")
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(self.client.read()["members"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
