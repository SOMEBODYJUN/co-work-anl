"""Checkpoint lifecycle tests against real isolated bare Git remotes."""
import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("wcg_checkpoint", ROOT / "research/weighted_congestion_frontier/tools/checkpoint.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def run(repo, *args):
    env = {k: v for k, v in os.environ.items() if k not in c.ROUTING}
    return subprocess.check_output(["git", *args], cwd=repo, env=env,
                                   stderr=subprocess.DEVNULL).decode().strip()


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        common = (ROOT / run(ROOT, "rev-parse", "--git-common-dir")).resolve()
        self.tmp = tempfile.TemporaryDirectory(prefix="checkpoint-test-", dir=common)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        run(self.root, "init", "--bare", str(self.remote))
        self.repo = self.root / "work"
        run(self.root, "clone", str(self.remote), str(self.repo))
        run(self.repo, "config", "user.name", "Fixture")
        run(self.repo, "config", "user.email", "fixture@example.invalid")
        self.scope = self.repo / c.SCOPE
        self.scope.mkdir(parents=True)
        self.note = self.scope / "note.md"
        self.note.write_text("baseline\n")
        (self.repo / "outside.md").write_text("outside baseline\n")
        run(self.repo, "add", ".")
        run(self.repo, "commit", "-m", "baseline")
        self.branch = "wcg/work/fixture/session"
        run(self.repo, "branch", "-M", self.branch)
        run(self.repo, "push", "origin", self.branch)
        self.before = run(self.repo, "rev-parse", "HEAD")
        env = patch.dict(os.environ, {}, clear=False)
        env.start()
        self.addCleanup(env.stop)
        for key in ("WCG_CHECKPOINT_TOKEN_FILE", "WCG_CHECKPOINT_ASKPASS", "GIT_ASKPASS"):
            os.environ.pop(key, None)

    def save(self, **kw):
        args = argparse.Namespace(repo=str(self.repo), paths=[], message=None, token_file=None)
        vars(args).update(kw)
        return c.save(args)

    def peer(self, filename, text):
        directory = self.root / "peer"
        if not directory.exists():
            run(self.root, "clone", "--branch", self.branch, str(self.remote), str(directory))
            run(directory, "config", "user.name", "Peer")
            run(directory, "config", "user.email", "peer@example.invalid")
        (directory / c.SCOPE / filename).write_text(text)
        run(directory, "add", ".")
        run(directory, "commit", "-m", "peer work")
        run(directory, "push", "origin", self.branch)

    def test_save_and_descriptor_hash_replay(self):
        self.note.write_text("new reusable result\n")
        result = self.save()
        self.assertEqual(result["status"], "pushed")
        self.assertTrue(result["created_commit"])
        self.assertEqual(run(self.remote, "rev-parse", self.branch), result["commit"])
        descriptor = json.loads(Path(result["assets"][0]["descriptor"]).read_text())
        self.assertEqual(descriptor["sha256"], hashlib.sha256(self.note.read_bytes()).hexdigest())
        blob = subprocess.check_output(["git", "cat-file", "blob", result["commit"] + ":" + descriptor["path"]], cwd=self.remote)
        self.assertEqual(hashlib.sha256(blob).hexdigest(), descriptor["sha256"])

    def test_repeat_has_no_empty_commit(self):
        self.note.write_text("result\n")
        first = self.save()
        second = self.save()
        self.assertEqual(first["commit"], second["commit"])
        self.assertFalse(second["created_commit"])

    def test_scope_preserves_unrelated_dirty_file(self):
        outside = self.repo / "outside.md"
        outside.write_text("uncommitted other research\n")
        self.note.write_text("result\n")
        self.save()
        self.assertEqual(run(self.repo, "show", "HEAD:outside.md"), "outside baseline")
        self.assertEqual(outside.read_text(), "uncommitted other research\n")

    def test_unrelated_staged_file_is_not_committed(self):
        (self.repo / "outside.md").write_text("another staged result\n")
        run(self.repo, "add", "outside.md")
        self.note.write_text("result\n")
        with self.assertRaisesRegex(c.Stop, "outside scope"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.assertEqual(run(self.repo, "diff", "--cached", "--name-only"), "outside.md")

    def test_explicit_paths_include_root_file_and_spaces(self):
        (self.repo / "outside.md").write_text("included\n")
        spaced = self.scope / "边界 情况.md"
        spaced.write_text("exact boundary\n")
        result = self.save(paths=["outside.md", c.SCOPE])
        self.assertEqual(set(result["files"]), {"outside.md", c.SCOPE + "/边界 情况.md"})

    def test_deleted_file_committed_without_blob_descriptor(self):
        self.note.unlink()
        result = self.save()
        self.assertEqual(result["assets"], [])
        self.assertEqual(run(self.repo, "ls-tree", "HEAD", c.SCOPE + "/note.md"), "")

    def test_network_failure_retry_saves_once(self):
        self.note.write_text("saved offline\n")
        original = c.git
        def offline(repo, *args, **kwargs):
            if args and args[0] in {"fetch", "push"}:
                return subprocess.CompletedProcess(args, 1, b"", b"offline")
            return original(repo, *args, **kwargs)
        with patch.object(c, "git", offline):
            with self.assertRaisesRegex(c.Stop, "Remote confirmation"):
                self.save()
        saved = run(self.repo, "rev-parse", "HEAD")
        self.assertNotEqual(saved, self.before)
        result = self.save()
        self.assertEqual(result["commit"], saved)
        self.assertFalse(result["created_commit"])

    def test_lost_push_response_is_confirmed(self):
        self.note.write_text("response lost\n")
        original = c.git
        def lost(repo, *args, **kwargs):
            result = original(repo, *args, **kwargs)
            if args and args[0] == "push":
                return subprocess.CompletedProcess(args, 1, b"", b"lost response")
            return result
        with patch.object(c, "git", lost):
            self.assertEqual(self.save()["status"], "pushed")

    def test_remote_disjoint_changes_merge_automatically(self):
        self.peer("peer.md", "peer asset\n")
        self.note.write_text("our asset\n")
        result = self.save()
        self.assertEqual((self.scope / "peer.md").read_text(), "peer asset\n")
        self.assertEqual(self.note.read_text(), "our asset\n")
        self.assertEqual(result["remote_tip"], run(self.remote, "rev-parse", self.branch))
        self.assertEqual(run(self.repo, "status", "--porcelain"), "")

    def test_remote_real_conflict_aborts_preserves_local_snapshot(self):
        self.peer("note.md", "different peer version\n")
        self.note.write_text("our different version\n")
        with self.assertRaisesRegex(c.Stop, "Conflicts"):
            self.save()
        self.assertEqual(self.note.read_text(), "our different version\n")
        self.assertNotEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.assertEqual(run(self.repo, "status", "--porcelain"), "")

    def test_dirty_other_work_blocks_divergence_without_loss(self):
        self.peer("peer.md", "peer\n")
        outside = self.repo / "outside.md"
        outside.write_text("unsaved other work\n")
        self.note.write_text("our\n")
        with self.assertRaisesRegex(c.Stop, "other tracked work"):
            self.save()
        self.assertEqual(outside.read_text(), "unsaved other work\n")
        self.assertEqual(self.note.read_text(), "our\n")

    def test_live_writer_lock_blocks_second_checkpoint(self):
        cache = self.repo / ".git/wcg-checkpoint"
        cache.mkdir()
        with (cache / "writer.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(c.Stop, "Another checkpoint"):
                self.save()

    def test_detached_head_and_board_branch_rejected(self):
        run(self.repo, "checkout", "--detach")
        with self.assertRaisesRegex(c.Stop, "Detached"):
            self.save()
        run(self.repo, "checkout", "-b", "wcg/board")
        with self.assertRaisesRegex(c.Stop, "board.py"):
            self.save()

    def test_paths_and_credentials_rejected_before_commit(self):
        fake = "ghp_" + "A" * 32
        self.note.write_text(fake)
        with self.assertRaisesRegex(c.Stop, "Credential-like"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.note.write_text("result\n")
        for path in ("../outside.md", "missing-path.md"):
            with self.assertRaises(c.Stop):
                self.save(paths=[path])
        with self.assertRaises(c.Stop):
            self.save(message=fake)

    def test_staged_secret_reverted_to_head_does_not_leak(self):
        self.note.write_text("ghp_" + "A" * 32)
        run(self.repo, "add", c.SCOPE)
        self.note.write_text("baseline\n")
        result = self.save()
        self.assertFalse(result["created_commit"])
        self.assertEqual(result["commit"], self.before)

    def test_external_auth_remembers_path_only(self):
        credential = self.root / "credential.txt"
        secret = "ghp_" + "A" * 32
        credential.write_text(secret)
        result = self.save(token_file=str(credential))
        self.assertEqual(run(self.repo, "config", "--local", "wcg.tokenFile"), str(credential))
        self.assertNotIn(secret, json.dumps(result))
        self.assertNotIn(secret, (self.repo / ".git/config").read_text())

    def test_inherited_git_routing_cannot_touch_another_index(self):
        decoy = self.root / "decoy-index"
        decoy.write_bytes(b"do not change")
        self.note.write_text("result\n")
        with patch.dict(os.environ, {"GIT_INDEX_FILE": str(decoy), "GIT_DIR": "/missing"}):
            self.assertEqual(self.save()["status"], "pushed")
        self.assertEqual(decoy.read_bytes(), b"do not change")

    def test_remote_moves_between_local_commit_and_push(self):
        self.note.write_text("our\n")
        original = c.git
        moved = False
        def interleave(repo, *args, **kwargs):
            nonlocal moved
            if args and args[0] == "push" and not moved:
                moved = True
                self.peer("peer.md", "concurrent peer\n")
            return original(repo, *args, **kwargs)
        with patch.object(c, "git", interleave):
            result = self.save()
        self.assertEqual(result["status"], "pushed")
        self.assertEqual((self.scope / "peer.md").read_text(), "concurrent peer\n")
        self.assertEqual(self.note.read_text(), "our\n")

    def test_missing_identity_works_for_commit_and_auto_merge(self):
        self.peer("peer.md", "peer\n")
        run(self.repo, "config", "--unset", "user.name")
        run(self.repo, "config", "--unset", "user.email")
        self.note.write_text("ours\n")
        with patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}):
            self.assertEqual(self.save()["status"], "pushed")
        self.assertEqual(run(self.repo, "show", "-s", "--format=%an", "HEAD"), "WCG Researcher")

    def test_complete_launcher_runs_outside_checkout(self):
        self.note.write_text("CLI result\n")
        script = ROOT / "research/weighted_congestion_frontier/tools/checkpoint.sh"
        result = subprocess.run(["bash", str(script), "--repo", str(self.repo)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "pushed")

    def test_invalid_or_in_repo_token_file_refused(self):
        external = self.root / "invalid.txt"
        external.write_text("placeholder")
        with self.assertRaisesRegex(c.Stop, "exactly one"):
            self.save(token_file=str(external))
        internal = self.scope / "credential.txt"
        internal.write_text("ghp_" + "A" * 32)
        with self.assertRaisesRegex(c.Stop, "outside the repository"):
            self.save(token_file=str(internal))

    def test_conflicting_push_destination_refused(self):
        run(self.repo, "remote", "set-url", "--push", "origin", str(self.root / "different.git"))
        self.note.write_text("result\n")
        with self.assertRaisesRegex(c.Stop, "identical fetch and push"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)


if __name__ == "__main__":
    unittest.main()
