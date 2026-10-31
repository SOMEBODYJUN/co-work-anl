"""Real isolated Git remotes: concurrent peers, routed chat and scoped main saves."""
import concurrent.futures
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import test_work as fixtures

SPEC = importlib.util.spec_from_file_location(
    "collaboration_race_board", fixtures.TOOLS / "board.py")
board = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(board)


class CollaborationConcurrencyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.WorkTests("test_automatic_actor_is_stable_and_creates_no_work_branch")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_ten_independent_clones_chat_and_publish_only_their_own_workspaces(self):
        f = self.fixture
        peers = [(f"P{i:02d}", f.root / f"peer-{i:02d}") for i in range(10)]
        for actor, repo in peers:
            started = f.work("start", "--actor", actor, "--remote", str(f.remote), repo=repo)
            self.assertEqual(started.returncode, 0, started.stderr)
            self.assertEqual(json.loads(started.stdout.splitlines()[0])["save"], "customer-attraction")
            desk = repo / "research/workspaces/customer-attraction" / actor
            (desk / "notes").mkdir()
            (desk / "notes/boundary.md").write_text("exact fixture for " + actor + "\n")
            (repo / "unpublished-local.txt").write_text("preserve " + actor + "\n")

        def chat(index):
            actor, repo = peers[index]
            peer = peers[(index + 1) % len(peers)][0]
            for command in (("dm", "--to", peer, "--text", "PRIVATE-" + actor),
                            ("send", "--mention", peer, "--text", "PUBLIC-" + actor)):
                result = f.work(*command, repo=repo)
                if result.returncode:
                    raise AssertionError(result.stderr)
            return actor

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            self.assertEqual(set(pool.map(chat, range(10))), {p[0] for p in peers})
        client = board.Board(peers[0][1])
        state = client.read()
        self.assertEqual(len(state["events"]), 20)
        self.assertEqual(len({e["id"] for e in state["events"]}), 20)
        for index, (actor, repo) in enumerate(peers):
            public = f.work("read", "--json", repo=repo)
            self.assertEqual(public.returncode, 0, public.stderr)
            self.assertEqual(len(json.loads(public.stdout)["events"]), 10)
            self.assertNotIn("PRIVATE-", public.stdout)
            result = f.work("inbox", "--json", repo=repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            incoming = json.loads(result.stdout)["events"]
            self.assertEqual(len(incoming), 2)
            expected_sender = peers[(index - 1) % len(peers)][0]
            self.assertEqual({e["actor"] for e in incoming}, {expected_sender})
            ack = f.work("ack", *(e["id"] for e in incoming), repo=repo)
            self.assertEqual(ack.returncode, 0, ack.stderr)
            self.assertEqual(json.loads(f.work("inbox", "--json", repo=repo).stdout)["events"], [])

        def publish(item):
            actor, repo = item
            result = f.work("checkpoint", "-m", "workspace fixture " + actor, repo=repo)
            if result.returncode:
                raise AssertionError(result.stderr)
            receipt = json.loads(result.stdout)
            if receipt["status"] != "pushed":
                raise AssertionError(receipt)
            return actor, repo, receipt

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            receipts = list(pool.map(publish, peers))
        for actor, repo, receipt in receipts:
            self.assertEqual(fixtures.value(repo, "branch", "--show-current"), "main")
            self.assertEqual((repo / "unpublished-local.txt").read_text(), "preserve " + actor + "\n")
            self.assertEqual(fixtures.git(f.remote, "merge-base", "--is-ancestor",
                                         receipt["commit"], "main", check=False).returncode, 0)
            for asset in receipt["assets"]:
                data = fixtures.git(f.remote, "show", asset["asset"]["commit"] + ":" + asset["asset"]["path"]).stdout
                self.assertEqual(hashlib.sha256(data.encode()).hexdigest(), asset["asset"]["sha256"])
        for actor, _ in peers:
            path = "research/workspaces/customer-attraction/" + actor + "/notes/boundary.md"
            self.assertEqual(fixtures.value(f.remote, "show", "main:" + path), "exact fixture for " + actor)
        self.assertEqual(set(fixtures.value(f.remote, "for-each-ref", "--format=%(refname)",
                                            "refs/heads").splitlines()),
                         {"refs/heads/main", "refs/heads/wcg/board"})

    def test_direct_message_survives_offline_and_lost_push_reply_without_duplication(self):
        f = self.fixture
        f.start()
        client = board.Board(f.repo, retries=1)
        intent = board.make_intent("001", "message", {"text": "private exact boundary", "to": "002", "save": "customer-attraction"})
        original = board.git

        def offline(cwd, *args, **kwargs):
            if args and args[0] == "fetch":
                raise board.BoardError("offline fixture")
            return original(cwd, *args, **kwargs)

        with patch.object(board, "git", offline):
            with self.assertRaises(board.BoardError):
                client.publish(intent)
        pending = client.outbox / (intent["id"] + ".json")
        self.assertEqual(json.loads(pending.read_text()), intent)
        lost = [False]

        def lose_reply(cwd, *args, **kwargs):
            result = original(cwd, *args, **kwargs)
            if args and args[0] == "push" and not lost[0]:
                lost[0] = True
                raise board.BoardError("pushed but response was lost")
            return result

        with patch.object(board, "git", lose_reply):
            with self.assertRaises(board.BoardError):
                client.publish(intent)
        event = client.publish(intent)
        self.assertEqual(event["id"], intent["id"])
        self.assertFalse(pending.exists())
        self.assertEqual(len(client.read()["events"]), 1)
        self.assertNotIn("private exact boundary", board.render(client.read()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
