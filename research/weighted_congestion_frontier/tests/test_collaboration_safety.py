"""Independent adversarial checks; every remote and identity is a local fixture."""
import copy
import json
import subprocess
import unittest
from unittest.mock import patch

# Import modules, not TestCase classes: discovery must not rerun their suites.
import test_board as board_fixture
import test_work as work_fixture


class PrivateRoutingSafetyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = board_fixture.BoardTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.client = self.fixture.client
        self.board = board_fixture.b

    def publish(self, actor="Alice", text="public note", **body):
        return self.client.publish(board_fixture.message(actor, text, **body))

    def test_private_text_absent_from_default_markdown_json_and_thread_exports(self):
        public = self.publish(text="visible public finding", thread="same-topic")
        private = self.publish(text="PRIVATE_SENTINEL_A_B", to="Bob", thread="same-topic")
        for args in (("view",), ("view", "--json"),
                     ("view", "--thread", "same-topic"),
                     ("view", "--json", "--thread", "same-topic", "--limit", "1")):
            result = self.fixture.cli(*args)
            self.assertNotIn("PRIVATE_SENTINEL_A_B", result.stdout)
            self.assertIn("visible public finding", result.stdout)
        index = board_fixture.call(self.fixture.remote, "show",
                                   "wcg/board:" + str(self.board.PREFIX / "BOARD.md"))
        self.assertNotIn("PRIVATE_SENTINEL_A_B", index)
        self.assertIn("visible public finding", index)
        exported = json.loads(self.fixture.cli("view", "--json").stdout)
        self.assertEqual([e["id"] for e in exported["events"]], [public["id"]])
        self.assertNotIn(private["id"], self.board.render(self.client.read()))

    def test_inbox_only_delivers_direct_messages_mentions_and_replies_to_recipient(self):
        dm = self.publish(text="alice to bob", to="Bob", save="topic")
        mention = self.publish(text="question for bob", mentions=["Bob"], save="topic")
        unrelated = self.publish(text="ordinary public text", save="topic")
        bob = json.loads(self.fixture.cli("view", "--json", "--actor", "Bob",
                                          "--save", "topic", "--inbox").stdout)
        charlie = json.loads(self.fixture.cli("view", "--json", "--actor", "Charlie",
                                              "--save", "topic", "--inbox").stdout)
        self.assertEqual({e["id"] for e in bob["events"]}, {dm["id"], mention["id"]})
        self.assertNotIn(unrelated["id"], {e["id"] for e in bob["events"]})
        self.assertEqual(charlie["events"], [])
        conversation = json.loads(self.fixture.cli("view", "--json", "--actor", "Alice",
                                                   "--peer", "Bob", "--save", "topic").stdout)
        self.assertEqual([e["id"] for e in conversation["events"]], [dm["id"]])

    def test_private_reply_cannot_become_public_change_recipient_or_cross_save(self):
        parent = self.publish(to="Bob", save="topic", text="private parent")
        for actor, body in (("Alice", {"save": "topic"}),
                            ("Alice", {"save": "topic", "to": "Charlie"}),
                            ("Charlie", {"save": "topic", "to": "Bob"}),
                            ("Bob", {"save": "other", "to": "Alice"})):
            with self.subTest(actor=actor, body=body):
                with self.assertRaises(self.board.ValidationError):
                    self.publish(actor, "invalid reply", reply_to=parent["id"], **body)
        reply = self.publish("Bob", "valid private reply", to="Alice", save="topic",
                             reply_to=parent["id"])
        self.assertEqual(len(self.client.read()["events"]), 2)
        self.assertNotIn(reply["id"], self.board.render(self.client.read()))

    def test_public_reply_cannot_cross_save_and_legacy_messages_use_shared(self):
        old = self.publish(text="legacy unscoped event")
        with self.assertRaises(self.board.ValidationError):
            self.publish(text="wrong save", save="other", reply_to=old["id"])
        self.publish(text="compatible reply", save="shared", reply_to=old["id"])
        shared = json.loads(self.fixture.cli("view", "--save", "shared", "--json").stdout)
        self.assertEqual(len(shared["events"]), 2)

    def test_message_id_cannot_be_reused_to_change_route_or_mentions(self):
        original = board_fixture.message("Alice", "fixed text", to="Bob", save="topic")
        self.client.publish(original)
        for body in ({"to": "Charlie", "save": "topic"},
                     {"to": "Bob", "save": "other"},
                     {"to": "Bob", "save": "topic", "mentions": ["Bob"]}):
            altered = copy.deepcopy(original)
            altered["body"] = dict(text="fixed text", **body)
            with self.subTest(body=body):
                with self.assertRaises(self.board.Conflict):
                    self.client.publish(altered)
        self.assertEqual(len(self.client.read()["events"]), 1)

    def test_private_pending_retry_and_discard_check_sender_before_mutation(self):
        intent = board_fixture.message("Alice", "offline private text", to="Bob")
        original = self.board.git
        def offline(directory, *args, **kwargs):
            if args and args[0] == "fetch":
                raise self.board.BoardError("fixture offline")
            return original(directory, *args, **kwargs)
        self.client.retries = 1
        with patch.object(self.board, "git", offline):
            with self.assertRaises(self.board.BoardError):
                self.client.publish(intent)
        pending = self.client.outbox / (intent["id"] + ".json")
        for command in ("retry", "discard"):
            bad = self.fixture.cli(command, "--event-id", intent["id"], "--actor", "Charlie", check=False)
            self.assertNotEqual(bad.returncode, 0)
            self.assertTrue(pending.exists())
            self.assertEqual(self.client.read()["events"], [])
        retried = self.fixture.cli("retry", "--event-id", intent["id"], "--actor", "Alice")
        self.assertEqual(json.loads(retried.stdout)["id"], intent["id"])
        self.assertFalse(pending.exists())
        self.assertEqual(len(self.client.read()["events"]), 1)

    def test_unread_queries_do_not_mark_messages_and_ack_is_precise(self):
        one = self.publish(to="Bob", save="topic", text="first")
        two = self.publish(to="Bob", save="topic", text="second")
        query = ("view", "--actor", "Bob", "--save", "topic", "--inbox", "--unread", "--json")
        first = json.loads(self.fixture.cli(*query, "--limit", "1").stdout)
        self.assertEqual([e["id"] for e in first["events"]], [two["id"]])
        self.assertEqual(len(json.loads(self.fixture.cli(*query).stdout)["events"]), 2)
        self.fixture.cli("ack", "--actor", "Bob", "--save", "topic", "--event-id", two["id"])
        remaining = json.loads(self.fixture.cli(*query).stdout)["events"]
        self.assertEqual([e["id"] for e in remaining], [one["id"]])
        invalid = self.fixture.cli("ack", "--actor", "Charlie", "--save", "topic",
                                    "--event-id", one["id"], check=False)
        self.assertNotEqual(invalid.returncode, 0)
        self.assertEqual([e["id"] for e in json.loads(self.fixture.cli(*query).stdout)["events"]], [one["id"]])

    def test_explicit_empty_view_identifiers_are_rejected_not_treated_as_public_defaults(self):
        for option in ("--actor", "--save", "--peer"):
            with self.subTest(option=option):
                result = self.fixture.cli("view", "--json", option, "", check=False)
                self.assertNotEqual(result.returncode, 0)
        result = self.fixture.cli("view", "--json", "--actor", "Alice", "--peer", "Alice", check=False)
        self.assertNotEqual(result.returncode, 0)


class WorkspaceSafetyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = work_fixture.WorkTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.start()
        self.repo = self.fixture.repo
        self.own = self.repo / "research/workspaces/unrelated-machines/001"

    def test_repeated_start_and_workspace_prepare_never_overwrite_drafts(self):
        readme = self.own / "README.md"
        readme.write_text("custom current research\n")
        note = self.own / "unpublished.md"
        note.write_text("valuable unfinished proof\n")
        work_fixture.git(self.repo, "add", readme.relative_to(self.repo).as_posix())
        status = work_fixture.value(self.repo, "status", "--porcelain")
        before = {p.name: p.read_bytes() for p in (readme, note, self.own / "workspace.json")}
        for args in (("workspace",), ("start", "--remote", str(self.fixture.remote))):
            result = self.fixture.work(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name: p.read_bytes() for p in (readme, note, self.own / "workspace.json")}, before)
        self.assertEqual(work_fixture.value(self.repo, "status", "--porcelain"), status)

    def test_visit_rejects_traversal_and_local_symlink_without_reading_target(self):
        for actor, path in (("../001", "README.md"), ("001", "../outside.md"),
                            ("001", "/etc/passwd"), ("001", "a\\b"),
                            ("001", "a:b"), ("001", "\nREADME.md")):
            with self.subTest(actor=actor, path=path):
                result = self.fixture.work("visit", actor, "--path", path)
                self.assertNotEqual(result.returncode, 0)
        private = self.fixture.root / "fixture-private"
        private.mkdir()
        (private / "README.md").write_text("MUST_NOT_READ_PRIVATE_TARGET\n")
        (self.own.parent / "peer-link").symlink_to(private, target_is_directory=True)
        result = self.fixture.work("visit", "peer-link")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("MUST_NOT_READ_PRIVATE_TARGET", result.stdout + result.stderr)

    def test_visit_fetches_remote_file_without_touching_head_index_or_drafts(self):
        relative = "research/workspaces/unrelated-machines/peer/README.md"
        self.fixture.advance_main(relative, "published peer reasoning\n")
        outside = self.repo / "outside.md"
        outside.write_text("staged unrelated research\n")
        work_fixture.git(self.repo, "add", "outside.md")
        outside.write_text("unstaged continuation\n")
        head = work_fixture.value(self.repo, "rev-parse", "HEAD")
        index = work_fixture.value(self.repo, "show", ":outside.md")
        status = work_fixture.value(self.repo, "status", "--porcelain")
        result = self.fixture.work("visit", "peer")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["text"], "published peer reasoning\n")
        self.assertEqual(work_fixture.value(self.repo, "rev-parse", "HEAD"), head)
        self.assertEqual(work_fixture.value(self.repo, "show", ":outside.md"), index)
        self.assertEqual(work_fixture.value(self.repo, "status", "--porcelain"), status)
        self.assertEqual(outside.read_text(), "unstaged continuation\n")

    def test_published_identity_collision_requires_explicit_resume(self):
        readme = self.own / "README.md"
        readme.write_text("existing worker research\n")
        result = self.fixture.work("checkpoint")
        self.assertEqual(result.returncode, 0, result.stderr)
        original = json.loads((self.own / "workspace.json").read_text())
        other = self.fixture.root / "independent-clone"
        refused = self.fixture.work("start", "--actor", "001", "--remote", str(self.fixture.remote), repo=other)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("--resume", refused.stderr)
        resumed = self.fixture.work("start", "--actor", "001", "--resume", "--remote", str(self.fixture.remote), repo=other)
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertEqual(work_fixture.value(other, "config", "--local", "wcg.instance"), original["instance"])
        self.assertEqual((other / readme.relative_to(self.repo)).read_text(), "existing worker research\n")
        refs = work_fixture.value(self.fixture.remote, "for-each-ref", "--format=%(refname)", "refs/heads").splitlines()
        self.assertEqual(set(refs), {"refs/heads/main", "refs/heads/wcg/board"})

    def test_daily_sync_rejects_other_branch_and_detached_head_without_mutation(self):
        for branch in ("unrelated-topic", None):
            if branch:
                work_fixture.git(self.repo, "switch", "-c", branch)
            else:
                work_fixture.git(self.repo, "checkout", "--detach")
            head = work_fixture.value(self.repo, "rev-parse", "HEAD")
            result = self.fixture.work("sync")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(work_fixture.value(self.repo, "rev-parse", "HEAD"), head)
            work_fixture.git(self.repo, "switch", "main")

    def test_empty_private_recipient_never_falls_back_to_public_send_or_read(self):
        for command in ("dm", "send"):
            result = self.fixture.work(command, "--to", "", "--text", "PRIVATE_EMPTY_DESTINATION")
            self.assertNotEqual(result.returncode, 0, "An empty direct recipient was treated as public")
        result = self.fixture.work("dm", "--to", "", "--json")
        self.assertNotEqual(result.returncode, 0)
        public = self.fixture.work("read", "--json")
        self.assertEqual(public.returncode, 0, public.stderr)
        self.assertNotIn("PRIVATE_EMPTY_DESTINATION", public.stdout)
        self.assertEqual(json.loads(public.stdout)["events"], [])

    def test_visit_rejects_remote_symlink_leaf_and_explicit_empty_save(self):
        path = self.fixture.seed / "research/workspaces/unrelated-machines/peer/linked.md"
        path.parent.mkdir(parents=True)
        path.symlink_to("../../../../outside.md")
        work_fixture.git(self.fixture.seed, "add", "research/workspaces")
        work_fixture.git(self.fixture.seed, "commit", "-m", "fixture historical symlink")
        work_fixture.git(self.fixture.seed, "push", "origin", "main")
        result = self.fixture.work("visit", "peer", "--path", "linked.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("outside baseline", result.stdout)
        result = self.fixture.work("--save", "", "read", "--json")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
