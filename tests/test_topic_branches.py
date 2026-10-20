"""New-topic recovery, communication and checkpoints against isolated Git remotes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "topic_work_fixtures", ROOT / "research/weighted_congestion_frontier/tests/test_work.py")
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
git, value = fixtures.git, fixtures.value


class TopicBranchTests(unittest.TestCase):
    setUp = fixtures.WorkTests.setUp
    work = fixtures.WorkTests.work
    read = fixtures.WorkTests.read
    branch = "research/new-topic"
    board_branch = "topics/new-board"

    def prepare(self):
        git(self.seed, "push", "origin", "HEAD:refs/heads/" + self.branch)
        result = subprocess.run([
            sys.executable, str(self.seed / fixtures.SCOPE / "tools/board.py"),
            "--repo", str(self.seed), "--branch", self.board_branch, "init"],
            env=fixtures.clean_env(), capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.work("start", "--actor", "R-topic", "--save", "or-optimization-selection",
                           "--research-branch", self.branch, "--board-branch", self.board_branch,
                           "--token-file", str(self.credential), "--remote", str(self.remote))
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout.splitlines()[0])

    def test_recovery_and_board_are_isolated(self):
        receipt = self.prepare()
        self.assertEqual(receipt["branch"], self.branch)
        self.assertEqual(receipt["board_branch"], self.board_branch)
        self.assertEqual(receipt["research_prompt"], "research/topic_selection/BOSS_START.md")
        self.assertEqual(self.read()["events"], [])
        sent = self.work("send", "--text", "candidate, not a theorem")
        self.assertEqual(sent.returncode, 0, sent.stderr)
        self.assertEqual(len(self.read()["events"]), 1)
        old = subprocess.run([sys.executable, str(fixtures.TOOLS / "board.py"),
                              "--repo", str(self.repo), "view", "--json"],
                             env=fixtures.clean_env(), capture_output=True, text=True, timeout=45)
        self.assertEqual(json.loads(old.stdout)["events"], [])

    def test_checkpoint_and_descriptor_use_bound_branch(self):
        self.prepare()
        previous_main = value(self.remote, "rev-parse", "main")
        note = self.repo / "research/topic_selection/candidate.md"
        note.parent.mkdir(parents=True)
        note.write_text("An exact candidate, still unproved.\n")
        result = self.work("checkpoint", "-m", "save new topic candidate")
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "pushed")
        self.assertEqual(receipt["branch"], self.branch)
        self.assertEqual(value(self.remote, "rev-parse", self.branch), receipt["commit"])
        self.assertEqual(value(self.remote, "rev-parse", "main"), previous_main)
        self.assertTrue(all(row["asset"]["branch"] == self.branch for row in receipt["assets"]))
        descriptor = receipt["assets"][0]["descriptor"]
        sent = self.work("send", "--text", "candidate saved", "--asset-json", descriptor)
        self.assertEqual(sent.returncode, 0, sent.stderr)

    def test_sync_preserves_dirty_work_and_does_not_import_main(self):
        self.prepare()
        dirty = self.repo / "outside.md"
        dirty.write_text("valuable local continuation\n")
        (self.seed / "main-only.md").write_text("old project advance\n")
        git(self.seed, "add", "main-only.md")
        git(self.seed, "commit", "-m", "main only")
        git(self.seed, "push", "origin", "main")
        result = self.work("sync")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(dirty.read_text(), "valuable local continuation\n")
        self.assertFalse((self.repo / "main-only.md").exists())
        # A peer advance on the selected branch must be imported safely.
        git(self.seed, "switch", "--detach", "HEAD~1")
        (self.seed / "topic-peer.md").write_text("peer new-topic result\n")
        git(self.seed, "add", "topic-peer.md")
        git(self.seed, "commit", "-m", "topic peer")
        git(self.seed, "push", "origin", "HEAD:refs/heads/" + self.branch)
        result = self.work("sync")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(dirty.read_text(), "valuable local continuation\n")
        self.assertTrue((self.repo / "topic-peer.md").is_file())

    def test_rebinding_and_same_branch_are_rejected(self):
        self.prepare()
        result = self.work("start", "--remote", str(self.remote), "--research-branch", "main")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(value(self.repo, "config", "wcg.researchBranch"), self.branch)
        other = self.root / "other-clone"
        result = self.work("start", "--remote", str(self.remote), "--research-branch", self.branch,
                           "--board-branch", self.branch, repo=other)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(value(other, "config", "--get", "wcg.researchBranch") if
                         git(other, "config", "--get", "wcg.researchBranch", check=False).returncode == 0
                         else "", "")


if __name__ == "__main__":
    unittest.main()
