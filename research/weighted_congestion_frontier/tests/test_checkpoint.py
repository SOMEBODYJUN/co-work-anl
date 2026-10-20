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
        # These historical checkpoint fixtures exercise the explicit legacy
        # archive. Unbound-current behavior is tested separately below.
        run(self.repo, "config", "--local", "wcg.save", "shared")
        self.scope = self.repo / c.SCOPE
        self.scope.mkdir(parents=True)
        self.note = self.scope / "note.md"
        self.note.write_text("baseline\n")
        (self.repo / "outside.md").write_text("outside baseline\n")
        run(self.repo, "add", ".")
        run(self.repo, "commit", "-m", "baseline")
        self.branch = "main"
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

    def test_preexisting_out_of_scope_commit_cannot_hitchhike_on_checkpoint(self):
        (self.repo / "outside.md").write_text("unrelated earlier draft\n")
        run(self.repo, "add", "outside.md")
        run(self.repo, "commit", "-m", "earlier unrelated work")
        earlier = run(self.repo, "rev-parse", "HEAD")
        self.note.write_text("intended scoped result\n")
        with self.assertRaisesRegex(c.Stop, "outside checkpoint scope.*outside.md"):
            self.save(paths=[c.SCOPE])
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(run(self.repo, "show", "HEAD:" + c.SCOPE + "/note.md"), "intended scoped result")
        self.assertEqual(run(self.repo, "merge-base", "--is-ancestor", earlier, "HEAD"), "")

    def test_explicit_backlog_scope_has_complete_receipt_and_descriptors(self):
        (self.repo / "outside.md").write_text("explicitly included earlier draft\n")
        run(self.repo, "add", "outside.md")
        run(self.repo, "commit", "-m", "earlier draft")
        earlier = run(self.repo, "rev-parse", "HEAD")
        self.note.write_text("current result\n")
        result = self.save(paths=[c.SCOPE, "outside.md"])
        expected = {"outside.md", c.SCOPE + "/note.md"}
        self.assertEqual(set(result["files"]), expected)
        self.assertEqual(set(result["outgoing_files"]), expected)
        self.assertEqual(set(result["outgoing_commits"]), {earlier, result["commit"]})
        self.assertEqual(result["pushed_head"], run(self.remote, "rev-parse", "main"))
        self.assertEqual({d["asset"]["path"] for d in result["assets"]}, expected)
        for descriptor in result["assets"]:
            asset = descriptor["asset"]
            blob = subprocess.check_output(["git", "cat-file", "blob", asset["commit"] + ":" + asset["path"]], cwd=self.remote)
            self.assertEqual(hashlib.sha256(blob).hexdigest(), asset["sha256"])

    def test_historical_secret_overwritten_by_safe_text_is_not_pushed(self):
        self.note.write_text("ghp_" + "A" * 32)
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "accidental credential")
        self.note.write_text("safe final text\n")
        with self.assertRaisesRegex(c.Stop, "Credential-like content in outgoing history"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(self.note.read_text(), "safe final text\n")

    def test_historical_secret_deleted_before_checkpoint_is_not_pushed(self):
        deleted = self.scope / "temporary.txt"
        deleted.write_text("ghp_" + "A" * 32)
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "temporary file")
        deleted.unlink()
        run(self.repo, "add", "-A")
        run(self.repo, "commit", "-m", "remove temporary file")
        with self.assertRaisesRegex(c.Stop, "Credential-like content in outgoing history"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)

    def test_historical_credential_filename_and_commit_metadata_are_rejected(self):
        special = self.scope / "githubtoken.txt"
        special.write_text("placeholder\n")
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "temporary placeholder")
        special.unlink()
        run(self.repo, "add", "-A")
        run(self.repo, "commit", "-m", "remove placeholder")
        with self.assertRaisesRegex(c.Stop, "Credential-like filename in outgoing history"):
            self.save()
        # A separate local reset only changes this disposable test fixture.
        run(self.repo, "reset", "--hard", self.before)
        self.note.write_text("ordinary text\n")
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "ghp_" + "A" * 32)
        with self.assertRaisesRegex(c.Stop, "Credential-like commit metadata"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)

    def test_historical_symlink_removed_before_checkpoint_is_rejected(self):
        link = self.scope / "link"
        link.symlink_to("note.md")
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "temporary symlink")
        link.unlink()
        run(self.repo, "add", "-A")
        run(self.repo, "commit", "-m", "remove symlink")
        with self.assertRaisesRegex(c.Stop, "Outgoing nonregular file"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)

    def test_peer_changes_outside_scope_do_not_block_disjoint_merge(self):
        directory = self.root / "outside-peer"
        run(self.root, "clone", "--branch", "main", str(self.remote), str(directory))
        run(directory, "config", "user.name", "Peer")
        run(directory, "config", "user.email", "peer@example.invalid")
        (directory / "outside.md").write_text("already-published peer change\n")
        run(directory, "add", "outside.md")
        run(directory, "commit", "-m", "peer unrelated area")
        run(directory, "push", "origin", "main")
        self.note.write_text("our scoped change\n")
        result = self.save(paths=[c.SCOPE])
        self.assertEqual(result["status"], "pushed")
        self.assertEqual(result["outgoing_files"], [c.SCOPE + "/note.md"])
        self.assertEqual((self.repo / "outside.md").read_text(), "already-published peer change\n")

    def test_historical_secret_in_merge_resolution_is_not_pushed(self):
        self.note.write_text("left side\n")
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "left side")
        left = run(self.repo, "rev-parse", "HEAD")
        run(self.repo, "checkout", "-b", "fixture-side", self.before)
        self.note.write_text("right side\n")
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "right side")
        right = run(self.repo, "rev-parse", "HEAD")
        run(self.repo, "checkout", "main")
        failed = subprocess.run(["git", "merge", "--no-edit", right], cwd=self.repo,
                                capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        self.note.write_text("ghp_" + "A" * 32)
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "resolve merge")
        self.assertEqual(len(run(self.repo, "rev-list", "--parents", "-n", "1", "HEAD").split()), 3)
        self.note.write_text("safe final result\n")
        with self.assertRaisesRegex(c.Stop, "Credential-like content in outgoing history"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(run(self.repo, "merge-base", "--is-ancestor", left, "HEAD"), "")

    def test_default_scope_includes_own_workspace_and_leaves_peer_draft(self):
        run(self.repo, "config", "--local", "wcg.actor", "R-self")
        run(self.repo, "config", "--local", "wcg.save", "topic-a")
        own = self.repo / "research/workspaces/topic-a/R-self/note.md"
        peer = self.repo / "research/workspaces/topic-a/R-peer/note.md"
        own.parent.mkdir(parents=True)
        peer.parent.mkdir(parents=True)
        own.write_text("our organized draft\n")
        peer.write_text("peer unfinished draft\n")
        result = self.save()
        self.assertEqual(result["files"], [own.relative_to(self.repo).as_posix()])
        self.assertEqual(run(self.remote, "show", "main:" + own.relative_to(self.repo).as_posix()), "our organized draft")
        self.assertEqual(run(self.remote, "ls-tree", "-r", "main", "--", peer.relative_to(self.repo).as_posix()), "")
        self.assertEqual(peer.read_text(), "peer unfinished draft\n")

    def test_unrelated_archive_defaults_select_its_topic_and_common_registers_only(self):
        run(self.repo, "config", "--local", "wcg.actor", "R-self")
        run(self.repo, "config", "--local", "wcg.save", "unrelated-machines")
        topic_paths = ["research/current/unrelated_machines", "research/questions/unrelated_machines",
                       "research/reviews/unrelated_machines", "research/unrelated_machines",
                       "tests/audits/unrelated_machines", "examples/unrelated_machines",
                       "evidence/runs/unrelated_machines", "evidence/certificates/unrelated_machines",
                       "history/source/literature/unrelated_machines"]
        common_paths = ["README.md", "RESEARCH_STATE.md", "CLAIMS.md", "FAILED_ROUTES.md",
                        "research/current/claims.md", "research/assets.json", "research/review_status.json",
                        "research/graph.json", "research/index.html", "research/source_crosswalk.json",
                        "research/source_crosswalk.md", "research/catalog.json", "research/CATALOG.md"]
        own_path = "research/workspaces/unrelated-machines/R-self"
        expected_files = []
        for name in topic_paths + [own_path]:
            path = self.repo / name / "note.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("archive asset\n")
            expected_files.append(path.relative_to(self.repo).as_posix())
        for name in common_paths:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("common register\n")
            expected_files.append(name)
        excluded = ["research/workspaces/unrelated-machines/R-peer/note.md",
                    "research/workspaces/shared/R-self/note.md",
                    "research/current/unrelated_machines_extra/note.md",
                    "history/source/literature/weighted_congestion/note.md",
                    "history/source/literature/unrelated_machines_extra/note.md"]
        for name in excluded:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("unpublished unrelated draft\n")
        self.note.write_text("old topic draft must stay local\n")
        self.assertEqual(set(c.default_paths(self.repo)), set(topic_paths + common_paths + [own_path]))
        result = self.save()
        self.assertEqual(set(result["files"]), set(expected_files))
        self.assertEqual(set(result["outgoing_files"]), set(expected_files))
        self.assertEqual(run(self.remote, "show", "main:" + c.SCOPE + "/note.md"), "baseline")
        for name in excluded:
            self.assertEqual(run(self.remote, "ls-tree", "-r", "main", "--", name), "")
            self.assertEqual((self.repo / name).read_text(), "unpublished unrelated draft\n")
        self.assertEqual(self.note.read_text(), "old topic draft must stay local\n")

    def test_unbound_checkpoint_uses_current_topic_and_only_own_current_workspace(self):
        run(self.repo, "config", "--local", "--unset", "wcg.save")
        run(self.repo, "config", "--local", "wcg.actor", "R-self")
        current = self.repo / "research/current/unrelated_machines/boundary.md"
        own = self.repo / "research/workspaces/unrelated-machines/R-self/note.md"
        excluded = [self.repo / "research/workspaces/unrelated-machines/R-peer/note.md",
                    self.repo / "research/workspaces/shared/R-self/note.md"]
        for path in [current, own] + excluded:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("local exact asset\n")
        self.note.write_text("legacy draft stays local\n")
        result = self.save()
        self.assertEqual(result["status"], "pushed")
        expected = {p.relative_to(self.repo).as_posix() for p in (current, own)}
        self.assertEqual(set(result["files"]), expected)
        self.assertEqual(set(result["outgoing_files"]), expected)
        self.assertEqual(run(self.remote, "show", "main:" + c.SCOPE + "/note.md"), "baseline")
        for path in excluded:
            self.assertEqual(run(self.remote, "ls-tree", "-r", "main", "--", path.relative_to(self.repo).as_posix()), "")
            self.assertEqual(path.read_text(), "local exact asset\n")
        self.assertEqual(self.note.read_text(), "legacy draft stays local\n")

    def test_unbound_checkpoint_with_only_legacy_paths_requires_explicit_scope(self):
        run(self.repo, "config", "--local", "--unset", "wcg.save")
        self.note.write_text("legacy draft stays local\n")
        with self.assertRaisesRegex(c.Stop, "No default checkpoint paths for archive unrelated-machines"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(self.note.read_text(), "legacy draft stays local\n")

    def test_unrelated_archive_precommitted_old_topic_cannot_hitchhike(self):
        run(self.repo, "config", "--local", "wcg.save", "unrelated-machines")
        self.note.write_text("precommitted old-topic draft\n")
        run(self.repo, "add", c.SCOPE)
        run(self.repo, "commit", "-m", "old topic draft")
        current = self.repo / "research/current/unrelated_machines/note.md"
        current.parent.mkdir(parents=True)
        current.write_text("new topic asset\n")
        with self.assertRaisesRegex(c.Stop, "outside checkpoint scope.*weighted_congestion_frontier/note.md"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(current.read_text(), "new topic asset\n")

    def test_unknown_archive_defaults_include_only_common_registers_and_own_workspace(self):
        run(self.repo, "config", "--local", "wcg.actor", "R-self")
        run(self.repo, "config", "--local", "wcg.save", "new-topic")
        own = self.repo / "research/workspaces/new-topic/R-self/note.md"
        peer = self.repo / "research/workspaces/new-topic/R-peer/note.md"
        unregistered = self.repo / "research/current/new_topic/note.md"
        for path in (own, peer, unregistered):
            path.parent.mkdir(parents=True)
            path.write_text("local asset\n")
        (self.repo / "README.md").write_text("shared research map\n")
        self.note.write_text("old topic local draft\n")
        self.assertEqual(set(c.default_paths(self.repo)), {"README.md", own.parent.relative_to(self.repo).as_posix()})
        result = self.save()
        self.assertEqual(set(result["files"]), {"README.md", own.relative_to(self.repo).as_posix()})
        self.assertEqual(run(self.remote, "show", "main:" + c.SCOPE + "/note.md"), "baseline")
        self.assertEqual(peer.read_text(), "local asset\n")
        self.assertEqual(unregistered.read_text(), "local asset\n")

    def test_archive_with_no_effective_default_paths_requires_explicit_scope(self):
        run(self.repo, "config", "--local", "wcg.save", "new-topic")
        self.note.write_text("old topic local draft\n")
        with self.assertRaisesRegex(c.Stop, "No default checkpoint paths.*supply explicit paths"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.assertEqual(run(self.repo, "diff", "--cached", "--name-only"), "")
        result = self.save(paths=[c.SCOPE + "/note.md"])
        self.assertEqual(result["status"], "pushed")

    def test_explicit_shared_archive_preserves_legacy_topic_defaults(self):
        run(self.repo, "config", "--local", "wcg.save", "shared")
        self.note.write_text("legacy archive asset\n")
        result = self.save()
        self.assertEqual(result["files"], [c.SCOPE + "/note.md"])
        self.assertEqual(run(self.remote, "show", "main:" + c.SCOPE + "/note.md"), "legacy archive asset")

    def test_deleted_unrelated_archive_asset_remains_in_default_scope(self):
        run(self.repo, "config", "--local", "wcg.save", "unrelated-machines")
        path = self.repo / "research/current/unrelated_machines/note.md"
        path.parent.mkdir(parents=True)
        path.write_text("obsolete new topic asset\n")
        run(self.repo, "add", path.relative_to(self.repo).as_posix())
        run(self.repo, "commit", "-m", "baseline archive asset")
        run(self.repo, "push", "origin", "main")
        path.unlink()
        result = self.save()
        self.assertEqual(result["files"], [path.relative_to(self.repo).as_posix()])
        self.assertEqual(run(self.remote, "ls-tree", "-r", "main", "--", path.relative_to(self.repo).as_posix()), "")

    def test_default_workspace_save_and_explicit_scope_for_peer(self):
        run(self.repo, "config", "--local", "wcg.actor", "R-self")
        own = self.repo / "research/workspaces/shared/R-self/note.md"
        peer = self.repo / "research/workspaces/shared/R-peer/note.md"
        own.parent.mkdir(parents=True)
        peer.parent.mkdir(parents=True)
        own.write_text("own draft\n")
        peer.write_text("explicitly handled peer file\n")
        first = self.save()
        self.assertEqual(first["outgoing_files"], [own.relative_to(self.repo).as_posix()])
        result = self.save(paths=[peer.parent.relative_to(self.repo).as_posix()])
        self.assertEqual(result["outgoing_files"], [peer.relative_to(self.repo).as_posix()])
        self.assertEqual(run(self.remote, "show", "main:" + peer.relative_to(self.repo).as_posix()), "explicitly handled peer file")

    def test_precommitted_peer_workspace_is_not_in_default_scope(self):
        run(self.repo, "config", "--local", "wcg.actor", "R-self")
        peer = self.repo / "research/workspaces/shared/R-peer/note.md"
        peer.parent.mkdir(parents=True)
        peer.write_text("precommitted peer draft\n")
        run(self.repo, "add", "research/workspaces")
        run(self.repo, "commit", "-m", "peer draft included earlier")
        self.note.write_text("our result\n")
        with self.assertRaisesRegex(c.Stop, "outside checkpoint scope.*R-peer/note.md"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)

    def test_workspace_ids_cannot_escape_default_scope(self):
        run(self.repo, "config", "--local", "wcg.actor", "../peer")
        with self.assertRaisesRegex(c.Stop, "Invalid local actor/save"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)

    def test_invalid_archive_without_actor_is_rejected(self):
        run(self.repo, "config", "--local", "wcg.save", "../weighted_congestion")
        self.note.write_text("draft\n")
        with self.assertRaisesRegex(c.Stop, "Invalid local actor/save"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)

    def test_unavailable_remote_baseline_never_pushes_unexamined_history(self):
        self.note.write_text("local checkpoint remains recoverable\n")
        original = c.git
        pushes = []
        def unavailable(repo, *args, **kwargs):
            if args and args[0] == "fetch":
                return subprocess.CompletedProcess(args, 1, b"", b"offline")
            if args and args[0] == "push":
                pushes.append(args)
            return original(repo, *args, **kwargs)
        with patch.object(c, "git", unavailable):
            with self.assertRaisesRegex(c.Stop, "Remote confirmation unavailable"):
                self.save()
        self.assertEqual(pushes, [])
        self.assertNotEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)


    def test_explicit_new_branch_first_publish_keeps_main_and_correct_descriptors(self):
        run(self.repo, "switch", "-c", "research/topic-selection")
        run(self.repo, "config", "--local", "wcg.researchBranch", "research/topic-selection")
        self.note.write_text("new topic selected questions\n")
        result = self.save()
        self.assertEqual(result["status"], "pushed")
        self.assertEqual(result["branch"], "research/topic-selection")
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(run(self.remote, "rev-parse", "research/topic-selection"), result["commit"])
        self.assertTrue(all(a["asset"]["branch"] == "research/topic-selection" for a in result["assets"]))
        self.assertEqual(self.save()["commit"], result["commit"])

    def test_unbound_side_branch_is_rejected(self):
        run(self.repo, "switch", "-c", "research/topic-selection")
        self.note.write_text("preserved draft\n")
        with self.assertRaisesRegex(c.Stop, "explicitly configured research branch"):
            self.save()
        self.assertEqual(run(self.repo, "rev-parse", "HEAD"), self.before)
        self.assertEqual(self.note.read_text(), "preserved draft\n")

    def test_new_branch_initial_publish_still_audits_prior_out_of_scope_commit(self):
        run(self.repo, "switch", "-c", "research/topic-selection")
        run(self.repo, "config", "--local", "wcg.researchBranch", "research/topic-selection")
        (self.repo / "outside.md").write_text("earlier outside-scope asset\n")
        run(self.repo, "add", "outside.md")
        run(self.repo, "commit", "-m", "earlier asset")
        self.note.write_text("topic asset\n")
        with self.assertRaisesRegex(c.Stop, "outside checkpoint scope"):
            self.save()
        self.assertEqual(run(self.remote, "rev-parse", "main"), self.before)
        self.assertEqual(run(self.remote, "for-each-ref", "--format=%(refname)", "refs/heads/research"), "")


if __name__ == "__main__":
    unittest.main()
