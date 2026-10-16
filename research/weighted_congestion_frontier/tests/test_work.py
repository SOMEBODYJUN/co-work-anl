"""One-program conversation lifecycle with real local Git and fake credentials."""
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCOPE = "research/weighted_congestion_frontier"
TOOLS = ROOT / SCOPE / "tools"
WORK = TOOLS / "work.py"
ROUTING = {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
           "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
           "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE",
           "GIT_PREFIX", "GIT_INTERNAL_SUPER_PREFIX"}


def clean_env():
    return {k: v for k, v in os.environ.items()
            if k not in ROUTING | {"WCG_CHECKPOINT_TOKEN_FILE", "WCG_CHECKPOINT_ASKPASS",
                                   "WCG_WORK_ASKPASS", "GIT_ASKPASS"}}


def git(repo, *args, check=True):
    result = subprocess.run(["git", *args], cwd=repo, env=clean_env(),
                            capture_output=True, text=True, timeout=45)
    if check and result.returncode:
        raise AssertionError(result.stderr)
    return result


def value(repo, *args):
    return git(repo, *args).stdout.strip()


class WorkTests(unittest.TestCase):
    def test_automatic_actor_is_stable_and_creates_no_work_branch(self):
        result = self.work("start", "--token-file", str(self.credential),
                           "--remote", str(self.remote))
        self.assertEqual(result.returncode, 0, result.stderr)
        first = json.loads(result.stdout.splitlines()[0])
        self.assertRegex(first["actor"], r"^W[0-9a-f]{12}$")
        self.assertEqual(first["branch"], "main")
        result = self.work("start", "--remote", str(self.remote))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout.splitlines()[0])["actor"], first["actor"])
        self.assertEqual(value(self.remote, "for-each-ref", "--format=%(refname)",
                               "refs/heads/wcg/work"), "")

    def test_legacy_branch_migration_preserves_commit_index_and_dirty_files(self):
        self.start()
        git(self.repo, "switch", "-c", "wcg/work/001/legacy")
        note = self.repo / SCOPE / "note.md"
        note.write_text("legacy committed proof\n")
        git(self.repo, "add", str(note))
        git(self.repo, "commit", "-m", "valuable legacy result")
        legacy = value(self.repo, "rev-parse", "HEAD")
        outside = self.repo / "outside.md"
        outside.write_text("staged work\n")
        git(self.repo, "add", "outside.md")
        note.write_text("legacy committed proof\nplus unstaged derivation\n")
        (self.repo / "untracked.txt").write_text("untracked idea\n")
        self.advance_main("peer.md", "new peer result\n")
        result = self.work("start", "--remote", str(self.remote))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(value(self.repo, "branch", "--show-current"), "main")
        self.assertEqual(git(self.repo, "merge-base", "--is-ancestor", legacy, "HEAD",
                             check=False).returncode, 0)
        self.assertEqual(value(self.repo, "show", ":outside.md"), "staged work")
        self.assertIn("plus unstaged derivation", note.read_text())
        self.assertEqual((self.repo / "untracked.txt").read_text(), "untracked idea\n")
        self.assertEqual((self.repo / "peer.md").read_text(), "new peer result\n")
        self.assertTrue(value(self.repo, "for-each-ref", "--format=%(refname)",
                              "refs/wcg/recovery"))

    def setUp(self):
        common = (ROOT / value(ROOT, "rev-parse", "--git-common-dir")).resolve()
        self.tmp = tempfile.TemporaryDirectory(prefix="work-entry-test-", dir=common)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        self.seed = self.root / "publisher"
        self.repo = self.root / "new conversation"
        git(self.root, "init", "--bare", str(self.remote))
        self.seed.mkdir()
        git(self.seed, "init", "--initial-branch=main")
        git(self.seed, "config", "user.name", "Fixture")
        git(self.seed, "config", "user.email", "fixture@example.invalid")
        git(self.seed, "remote", "add", "origin", str(self.remote))
        scope = self.seed / SCOPE
        (scope / "tools").mkdir(parents=True)
        for name in ("work.py", "board.py", "checkpoint.py"):
            shutil.copy2(TOOLS / name, scope / "tools" / name)
        (scope / "note.md").write_text("baseline\n")
        (self.seed / "outside.md").write_text("outside baseline\n")
        git(self.seed, "add", ".")
        git(self.seed, "commit", "-m", "fixture")
        git(self.seed, "push", "origin", "main")
        init = subprocess.run([sys.executable, str(self.seed / SCOPE / "tools/board.py"),
                               "--repo", str(self.seed), "init"],
                              env=clean_env(), capture_output=True, text=True, timeout=45)
        self.assertEqual(init.returncode, 0, init.stderr)
        self.token = "ghp_" + "fixture" * 5
        self.credential = self.root / "credential with spaces.txt"
        self.credential.write_text("GitHub token:\n" + self.token + "\n")

    def work(self, *args, repo=None, env=None):
        return subprocess.run([sys.executable, str(WORK), "--repo", str(repo or self.repo), *args],
                              cwd=self.root, env=env or clean_env(),
                              capture_output=True, text=True, timeout=45)

    def start(self):
        result = self.work("start", "--actor", "001", "--token-file", str(self.credential),
                           "--remote", str(self.remote))
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout.splitlines()[0])

    def advance_main(self, path, text):
        file = self.seed / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
        git(self.seed, "add", path)
        git(self.seed, "commit", "-m", "remote advance")
        git(self.seed, "push", "origin", "main")

    def read(self):
        result = self.work("read", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_start_recovers_missing_repo_remembers_role_and_external_path(self):
        self.assertFalse(self.repo.exists())
        first = self.start()
        self.assertEqual(first["actor"], "001")
        self.assertEqual(first["branch"], "main")
        self.assertEqual(value(self.repo, "config", "wcg.actor"), "001")
        self.assertEqual(value(self.repo, "config", "wcg.tokenFile"), str(self.credential))
        self.assertNotIn(self.token, first.__str__())
        self.assertNotIn(self.token, (self.repo / ".git/config").read_text())
        self.assertEqual(self.read()["events"], [])
        second = self.work("start", "--actor", "001", "--remote", str(self.remote))
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout.splitlines()[0])["branch"], first["branch"])
        other = self.work("start", "--actor", "002", "--remote", str(self.remote))
        self.assertEqual(other.returncode, 2)
        self.assertEqual(value(self.repo, "branch", "--show-current"), first["branch"])

    def test_existing_dirty_clone_is_preserved_when_starting(self):
        git(self.root, "clone", "--branch", "main", str(self.remote), str(self.repo))
        note = self.repo / SCOPE / "note.md"
        note.write_text("staged research\n")
        git(self.repo, "add", SCOPE + "/note.md")
        note.write_text("staged research\nunstaged continuation\n")
        loose = self.repo / "untracked with spaces.txt"
        loose.write_text("independent idea\n")
        first = self.start()
        self.assertEqual(first["branch"], "main")
        self.assertEqual(note.read_text(), "staged research\nunstaged continuation\n")
        self.assertEqual(value(self.repo, "show", ":" + SCOPE + "/note.md"), "staged research")
        self.assertEqual(loose.read_text(), "independent idea\n")

    def test_missing_invalid_and_in_repo_credentials_fail_early(self):
        for content in (None, "placeholder\n", self.token + "\n" + "ghp_" + "other" * 7):
            bad = self.root / "bad credential.txt"
            if content is not None:
                bad.write_text(content)
            result = self.work("start", "--actor", "001", "--token-file", str(bad),
                               "--remote", str(self.remote))
            self.assertEqual(result.returncode, 2)
            self.assertFalse(self.repo.exists())
            self.assertNotIn(self.token, result.stdout + result.stderr)
        self.start()
        inside = self.repo / "credential.txt"
        inside.write_text(self.token)
        result = self.work("--token-file", str(inside), "read")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(value(self.repo, "config", "wcg.tokenFile"), str(self.credential))
        self.credential.unlink()
        stale = self.work("read")
        self.assertEqual(stale.returncode, 2)

    def test_sync_preserves_staged_unstaged_and_untracked_work(self):
        self.start()
        note = self.repo / SCOPE / "note.md"
        note.write_text("staged result\n")
        git(self.repo, "add", SCOPE + "/note.md")
        note.write_text("staged result\nunstaged details\n")
        outside = self.repo / "outside.md"
        outside.write_text("other dirty research\n")
        untracked = self.repo / SCOPE / "新 idea.txt"
        untracked.write_text("local unpublished experiment\n")
        self.advance_main("peer.md", "new remote result\n")
        result = self.work("sync")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(note.read_text(), "staged result\nunstaged details\n")
        self.assertEqual(value(self.repo, "show", ":" + SCOPE + "/note.md"), "staged result")
        self.assertEqual(outside.read_text(), "other dirty research\n")
        self.assertEqual(untracked.read_text(), "local unpublished experiment\n")
        self.assertEqual((self.repo / "peer.md").read_text(), "new remote result\n")
        self.assertEqual(value(self.repo, "stash", "list"), "")
        self.assertEqual(git(self.repo, "merge-base", "--is-ancestor",
                             value(self.seed, "rev-parse", "HEAD"), "HEAD", check=False).returncode, 0)

    def test_committed_conflict_aborts_merge_and_restores_dirty_work(self):
        self.start()
        note = self.repo / SCOPE / "note.md"
        note.write_text("our committed result\n")
        git(self.repo, "add", SCOPE + "/note.md")
        git(self.repo, "commit", "-m", "local result")
        before = value(self.repo, "rev-parse", "HEAD")
        outside = self.repo / "outside.md"
        outside.write_text("staged other work\n")
        git(self.repo, "add", "outside.md")
        (self.repo / "untracked.txt").write_text("local idea\n")
        self.advance_main(SCOPE + "/note.md", "competing remote result\n")
        result = self.work("sync")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(value(self.repo, "rev-parse", "HEAD"), before)
        self.assertEqual(note.read_text(), "our committed result\n")
        self.assertEqual(outside.read_text(), "staged other work\n")
        self.assertEqual(value(self.repo, "show", ":outside.md"), "staged other work")
        self.assertEqual((self.repo / "untracked.txt").read_text(), "local idea\n")
        self.assertFalse((self.repo / ".git/MERGE_HEAD").exists())
        self.assertEqual(value(self.repo, "stash", "list"), "")

    def test_uncommitted_conflict_keeps_complete_backup_and_local_bytes(self):
        self.start()
        note = self.repo / SCOPE / "note.md"
        local = "our uncommitted result\n"
        note.write_text(local)
        loose = self.repo / "untracked.txt"
        loose.write_text("untracked research\n")
        self.advance_main(SCOPE + "/note.md", "competing remote result\n")
        result = self.work("sync")
        self.assertEqual(result.returncode, 2)
        self.assertIn("our uncommitted result", note.read_text())
        self.assertIn("competing remote result", note.read_text())
        self.assertEqual(value(self.repo, "show", "refs/stash:" + SCOPE + "/note.md") + "\n", local)
        self.assertEqual(value(self.repo, "show", "refs/stash^3:untracked.txt"), "untracked research")
        self.assertTrue(value(self.repo, "stash", "list"))
        retry = self.work("sync")
        self.assertEqual(retry.returncode, 2)
        self.assertTrue(value(self.repo, "ls-files", "-u"))

    def test_sync_preserves_preexisting_stash(self):
        self.start()
        note = self.repo / SCOPE / "note.md"
        note.write_text("previous saved experiment\n")
        git(self.repo, "stash", "push", "-m", "previous user stash")
        old_stash = value(self.repo, "rev-parse", "refs/stash")
        note.write_text("current unpublished result\n")
        self.advance_main("peer.md", "new peer result\n")
        result = self.work("sync")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(note.read_text(), "current unpublished result\n")
        self.assertEqual(value(self.repo, "rev-parse", "refs/stash"), old_stash)
        self.assertEqual(value(self.repo, "show", "refs/stash:" + SCOPE + "/note.md"),
                         "previous saved experiment")

    def test_read_and_multiple_senders_share_topic_without_registration(self):
        self.start()
        for text in ("我先核对这个边界。", "这个问题可以从另一表示继续。"):
            result = self.work("send", "--thread", "gap-A", "--text", text)
            self.assertEqual(result.returncode, 0, result.stderr)
        second_repo = self.root / "second conversation"
        started = self.work("start", "--actor", "002", "--token-file", str(self.credential),
                            "--remote", str(self.remote), repo=second_repo)
        self.assertEqual(started.returncode, 0, started.stderr)
        other = self.work("send", "--thread", "gap-A", "--text", "我稍后独立检查。", repo=second_repo)
        self.assertEqual(other.returncode, 0, other.stderr)
        state = self.read()
        self.assertEqual([event["actor"] for event in state["events"]], ["001", "001", "002"])
        self.assertTrue(all(event["body"]["thread"] == "gap-A" for event in state["events"]))
        self.assertNotIn("members", state)
        self.assertNotIn("ideas", state)
        self.assertEqual(value(self.repo, "branch", "--show-current"), "main")
        self.assertEqual(value(second_repo, "branch", "--show-current"), "main")
        self.assertNotEqual(self.repo, second_repo)

    def test_checkpoint_pushes_and_result_asset_can_be_sent_with_saved_configuration(self):
        self.start()
        note = self.repo / SCOPE / "note.md"
        note.write_text("a reusable exact boundary\n")
        result = self.work("checkpoint", "-m", "checkpoint: exact boundary")
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "pushed")
        self.assertEqual(value(self.remote, "rev-parse", receipt["branch"]), receipt["commit"])
        descriptor = Path(receipt["assets"][0]["descriptor"])
        asset = json.loads(descriptor.read_text())
        self.assertEqual(asset["sha256"], hashlib.sha256(note.read_bytes()).hexdigest())
        sent = self.work("send", "--kind", "result", "--text", "边界证书已提交。",
                         "--thread", "gap-A", "--asset-json", str(descriptor))
        self.assertEqual(sent.returncode, 0, sent.stderr)
        event = self.read()["events"][-1]
        self.assertEqual(event["actor"], "001")
        self.assertEqual(event["body"]["asset"], asset)
        repeated = self.work("checkpoint")
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(repeated.stdout)["commit"], receipt["commit"])

    def test_new_archive_checkpoint_uses_saved_topic_scope(self):
        started = self.work("start", "--actor", "001", "--save", "unrelated-machines",
                            "--token-file", str(self.credential), "--remote", str(self.remote))
        self.assertEqual(started.returncode, 0, started.stderr)
        note = self.repo / "research/current/unrelated_machines/boundary.md"
        note.parent.mkdir(parents=True)
        note.write_text("new archive boundary\n")
        old_note = self.repo / SCOPE / "note.md"
        old_note.write_text("old archive draft remains local\n")
        peer = self.repo / "research/workspaces/unrelated-machines/peer/note.md"
        peer.parent.mkdir(parents=True)
        peer.write_text("peer draft remains local\n")
        result = self.work("checkpoint", "-m", "new archive checkpoint")
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "pushed")
        self.assertIn(note.relative_to(self.repo).as_posix(), receipt["files"])
        self.assertNotIn(SCOPE + "/note.md", receipt["files"])
        self.assertEqual(value(self.remote, "show", "main:" + SCOPE + "/note.md"), "baseline")
        self.assertEqual(value(self.remote, "show", "main:" + note.relative_to(self.repo).as_posix()),
                         "new archive boundary")
        self.assertEqual(value(self.remote, "ls-tree", "-r", "main", "--", peer.relative_to(self.repo).as_posix()), "")
        self.assertEqual(old_note.read_text(), "old archive draft remains local\n")
        self.assertEqual(peer.read_text(), "peer draft remains local\n")
        self.assertEqual(value(self.repo, "branch", "--show-current"), "main")

    def test_missing_repo_and_nonempty_destination_report_actionable_errors(self):
        result = self.work("read")
        self.assertEqual(result.returncode, 2)
        self.repo.mkdir()
        keep = self.repo / "keep.txt"
        keep.write_text("existing material\n")
        result = self.work("start", "--actor", "001", "--token-file", str(self.credential),
                           "--remote", str(self.remote))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(keep.read_text(), "existing material\n")

    def test_sync_and_checkpoint_share_writer_lock(self):
        self.start()
        with (self.repo / ".git/wcg-checkpoint/writer.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            for command in ("sync", "checkpoint"):
                result = self.work(command)
                self.assertEqual(result.returncode, 2)

    def test_inherited_git_routing_does_not_touch_external_index(self):
        decoy = self.root / "decoy-index"
        decoy.write_bytes(b"leave this alone")
        env = dict(clean_env(), GIT_INDEX_FILE=str(decoy), GIT_DIR="/missing")
        result = self.work("start", "--actor", "001", "--token-file", str(self.credential),
                           "--remote", str(self.remote), env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(decoy.read_bytes(), b"leave this alone")

    def test_uploaded_nonexecutable_program_works_as_git_askpass(self):
        uploaded = self.root / "uploaded work with spaces.py"
        shutil.copyfile(WORK, uploaded)
        uploaded.chmod(0o644)
        spec = importlib.util.spec_from_file_location("uploaded_work_fixture", uploaded)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        env = module.environment(self.credential)
        env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
        auth = subprocess.run(["git", "-c", "credential.helper=", "credential", "fill"],
                              input="protocol=https\nhost=github.com\n\n",
                              env=env, cwd=self.root, capture_output=True, text=True, timeout=15)
        self.assertEqual(auth.returncode, 0, auth.stderr)
        fields = dict(line.split("=", 1) for line in auth.stdout.splitlines())
        self.assertEqual(fields["username"], "x-access-token")
        self.assertEqual(fields["password"], self.token)
        helper = Path(env["GIT_ASKPASS"])
        self.assertTrue(os.access(helper, os.X_OK))
        self.assertNotIn(self.token, helper.read_text())
        for directory in module._ASKPASS_DIRECTORIES:
            directory.cleanup()

    def test_pending_retry_discard_and_replay_keep_original_message_id(self):
        self.start()
        sent = self.work("send", "--text", "可稍后回复。")
        self.assertEqual(sent.returncode, 0, sent.stderr)
        event = json.loads(sent.stdout)
        replay = self.work("retry", event["id"])
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(json.loads(replay.stdout)["id"], event["id"])
        self.assertEqual(len(self.read()["events"]), 1)
        missing_reply = "f" * 32
        pending_id = "e" * 32
        invalid = self.work("send", "--text", "尚不存在的回复对象。",
                            "--reply-to", missing_reply, "--event-id", pending_id)
        self.assertEqual(invalid.returncode, 2)
        pending = self.work("pending")
        self.assertEqual(pending.returncode, 0, pending.stderr)
        self.assertEqual(json.loads(pending.stdout), [pending_id])
        retry = self.work("retry", pending_id)
        self.assertEqual(retry.returncode, 2)
        discarded = self.work("discard", pending_id)
        self.assertEqual(discarded.returncode, 0, discarded.stderr)
        self.assertEqual(json.loads(self.work("pending").stdout), [])
        self.assertEqual(len(self.read()["events"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
