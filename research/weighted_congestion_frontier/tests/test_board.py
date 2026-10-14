"""Real local Git remotes, not mocked state-only success.

All fixtures are infrastructure examples, not mathematical conjectures.
"""
import concurrent.futures
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "wcg_board", Path(__file__).resolve().parents[1] / "tools/board.py")
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


def call(directory, *args):
    return subprocess.check_output(["git", *args], cwd=directory,
                                   stderr=subprocess.DEVNULL).decode().strip()


def proposal(actor, suffix="", claim=True):
    return b.make_intent(actor, "propose", {
        "title": "Fixture " + suffix, "claim_version": "TEST v1",
        "statement": "Exact fixture statement " + suffix,
        "obligation": "Check a particular boundary " + suffix,
        "mechanism": "Enumerate the finite fixture in exact arithmetic",
        "next_check": "Compare both endpoints", "claim": claim,
        "lease_seconds": 60})


class BoardTests(unittest.TestCase):
    def setUp(self):
        repo_root = Path(__file__).resolve().parents[3]
        common = Path(call(repo_root, "rev-parse", "--git-common-dir"))
        fixture_root = (repo_root / common).resolve() / "wcg-tests"
        fixture_root.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="fixture-", dir=fixture_root)
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        call(self.root, "init", "--bare", str(self.remote))
        self.repo = self.root / "work"
        call(self.root, "clone", str(self.remote), str(self.repo))
        call(self.repo, "config", "user.name", "Fixture")
        call(self.repo, "config", "user.email", "fixture@example.invalid")
        (self.repo / "asset.md").write_text("Frozen infrastructure fixture.\n")
        (self.repo / "folder").mkdir()
        (self.repo / "folder/child.md").write_text("child\n")
        call(self.repo, "add", ".")
        call(self.repo, "commit", "-m", "fixture")
        call(self.repo, "branch", "-M", "work")
        call(self.repo, "push", "origin", "work")
        self.now = 1000
        self.client = b.Board(self.repo, clock=lambda: self.now)
        self.client.initialize()
        self.asset = {
            "branch": "work", "commit": call(self.repo, "rev-parse", "HEAD"),
            "path": "asset.md",
            "sha256": hashlib.sha256((self.repo / "asset.md").read_bytes()).hexdigest()}

    def tearDown(self):
        self.tmp.cleanup()

    def race(self, intents):
        barrier = threading.Barrier(len(intents))
        original = b.git
        used, lock = set(), threading.Lock()

        def synchronized(cwd, *args, **kwargs):
            if args and args[0] == "push":
                thread = threading.get_ident()
                with lock:
                    first = thread not in used
                    used.add(thread)
                if first:
                    barrier.wait(timeout=15)
            return original(cwd, *args, **kwargs)

        def publish(intent):
            try:
                client = b.Board(self.repo, clock=lambda: self.now)
                return client.publish(intent)
            except b.Conflict as error:
                return error

        with patch.object(b, "git", synchronized):
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(intents)) as pool:
                return list(pool.map(publish, intents))

    def identity(self, actor, parent=None, role="researcher"):
        body = {"role": role, "runtime_id": "/root", "requested_model": "requested",
                "actual_model": "unknown", "requested_effort": "ultra",
                "actual_effort": "unknown", "budget_seconds": 3600}
        if parent is not None:
            body["parent"] = parent
        return b.make_intent(actor, "register", body)

    def test_registration_is_frozen_and_idempotent_after_retry(self):
        intent = self.identity("team/root")
        first = self.client.publish(intent)
        again = self.client.publish(intent)
        self.assertEqual(first, again)
        self.assertEqual(len(self.client.read()["members"]), 1)
        with self.assertRaises(b.Conflict):
            self.client.publish(self.identity("team/root"))
        member = self.client.read()["members"]["team/root"]
        self.assertEqual(member["actual_model"], "unknown")
        self.assertEqual(member["registered_event"], first["id"])

    def test_registered_child_keeps_parent_and_own_public_voice(self):
        self.client.publish(self.identity("team/root"))
        self.client.publish(self.identity("team/child", "team/root"))
        idea = self.client.publish(proposal("team/child"))["id"]
        reply = self.client.publish(b.make_intent("team/root", "discussion", {
            "idea": idea, "text": "Parent and child both have equal research voices."}))
        state = self.client.read()
        self.assertEqual(state["ideas"][idea]["owner"], "team/child")
        self.assertEqual(state["members"]["team/child"]["parent"], "team/root")
        self.assertIn(reply, state["events"])
        rendered = b.render(state, self.now)
        self.assertIn("已登记身份", rendered)
        self.assertIn("team/child", rendered)
        self.assertIn("unknown / unknown", rendered)

    def test_identity_collision_race_accepts_one_registration(self):
        results = self.race([self.identity("shared/root"), self.identity("shared/root")])
        self.assertEqual(sum(isinstance(x, b.Conflict) for x in results), 1)
        self.assertEqual(len(self.client.read()["members"]), 1)

    def test_distinct_teams_register_concurrently_without_coordinator(self):
        results = self.race([self.identity("one/root"), self.identity("two/root")])
        self.assertTrue(all(isinstance(x, dict) for x in results))
        self.assertEqual(len(self.client.read()["members"]), 2)

    def test_five_teams_seven_members_can_register_and_exchange_replies(self):
        # Thirty-five signatures exercised by Python publishers, not real LLMs.
        def team(number):
            parent = f"team_{number}/root"
            actors = [parent] + [f"team_{number}/member_{j}" for j in range(6)]
            client = b.Board(self.repo, clock=lambda: self.now)
            for index, actor in enumerate(actors):
                client.publish(self.identity(actor, parent if index else None))
            return actors
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            groups = list(pool.map(team, range(5)))
        actors = [actor for group in groups for actor in group]
        state = self.client.read()
        self.assertEqual(len(actors), 35)
        self.assertEqual(len(set(actors)), 35)
        self.assertEqual(set(state["members"]), set(actors))
        idea = self.client.publish(proposal(actors[0]))
        peer = self.client.publish(b.make_intent(actors[-1], "help", {
            "idea": idea["id"], "reply_to": idea["id"],
            "text": "Cross-team request on this concrete fixture."}))
        reply = self.client.publish(b.make_intent(actors[0], "discussion", {
            "idea": idea["id"], "reply_to": peer["id"],
            "text": "A specific answer keeps the requesting member attribution."}))
        final = self.client.read()
        self.assertEqual(reply["body"]["reply_to"], peer["id"])
        self.assertEqual(final["ideas"][idea["id"]]["owner"], actors[0])
        self.assertEqual(len(final["events"]), 38)

    def test_identity_boundaries_reject_bad_metadata_and_parent(self):
        self.client.publish(self.identity("one/root"))
        bad = [self.identity("no_member"), self.identity("two/child", "one/root"),
               self.identity("one/child", "one/missing"), self.identity("one/child", role="director")]
        for field, value in [("budget_seconds", 0), ("budget_seconds", True),
                             ("budget_seconds", 86401), ("actual_model", ""),
                             ("actual_model", "model\nspoof"), ("runtime_id", "x" * 161)]:
            intent = self.identity("one/child")
            intent["body"][field] = value
            bad.append(intent)
        for intent in bad:
            with self.subTest(body=intent["body"]):
                with patch.object(b, "retry_pause", side_effect=AssertionError("Validation must fail fast")):
                    with self.assertRaises(b.BoardError):
                        self.client.publish(intent)
        for budget, role in ((1, "paper_writer"), (86400, "extractor")):
            intent = self.identity("one/end_" + str(budget), role=role)
            intent["body"]["budget_seconds"] = budget
            self.client.publish(intent)
        self.assertEqual(len(self.client.read()["members"]), 3)
        for retries in (0, True, 51):
            with self.assertRaises(b.BoardError):
                b.Board(self.repo, retries=retries)

    def test_registration_cli_generates_unique_root_and_preserves_dirty_work(self):
        (self.repo / "asset.md").write_text("Uncommitted caller work.\n")
        script = Path(b.__file__).resolve()
        events = []
        for _ in range(2):
            output = subprocess.check_output([sys.executable, str(script), "--repo", str(self.repo),
                       "register", "--runtime-id", "/root"], text=True)
            events.append(json.loads(output))
        self.assertNotEqual(events[0]["actor"], events[1]["actor"])
        self.assertTrue(all(x["actor"].endswith("/root") for x in events))
        self.assertEqual((self.repo / "asset.md").read_text(), "Uncommitted caller work.\n")
        self.assertIn("asset.md", call(self.repo, "status", "--short"))

    def test_same_scope_parallel_proposals_have_one_owner(self):
        results = self.race([proposal("A"), proposal("B")])
        self.assertEqual(sum(isinstance(x, b.Conflict) for x in results), 1)
        state = self.client.read()
        self.assertEqual(len(state["ideas"]), 1)
        self.assertEqual(len(state["events"]), 1)

    def test_distinct_obligations_parallel_both_succeed(self):
        results = self.race([proposal("A", "one"), proposal("B", "two")])
        self.assertTrue(all(isinstance(x, dict) for x in results))
        self.assertEqual(len(self.client.read()["ideas"]), 2)

    def test_claim_race_without_coordinator(self):
        idea = self.client.publish(proposal("A", claim=False))["id"]
        intents = [b.make_intent(actor, "claim", {
            "idea": idea, "next_check": "Boundary", "lease_seconds": 60})
                   for actor in ("A", "B")]
        results = self.race(intents)
        self.assertEqual(sum(isinstance(x, b.Conflict) for x in results), 1)
        self.assertEqual(len(self.client.read()["events"]), 2)

    def test_expiry_takeover_fences_old_owner_but_allows_sharing(self):
        event = self.client.publish(proposal("A"))
        idea, old_token = event["id"], event["id"]
        self.now = 1060  # Exactly at expiry: takeover is allowed.
        new = self.client.publish(b.make_intent("B", "claim", {
            "idea": idea, "next_check": "Resume exact boundary", "lease_seconds": 60}))
        for kind in ("renew", "release", "finish"):
            body = {"idea": idea, "lease_token": old_token, "text": "salvage",
                    "lease_seconds": 60, "asset": self.asset}
            with self.assertRaises(b.Conflict):
                self.client.publish(b.make_intent("A", kind, body))
        self.client.publish(b.make_intent("A", "discussion", {
            "idea": idea, "text": "Independent salvage remains open."}))
        current = self.client.read()["ideas"][idea]
        self.assertEqual(current["owner"], "B")
        self.assertEqual(current["lease_token"], new["id"])

    def test_release_allows_continuation_finish_concludes_only_work_unit(self):
        event = self.client.publish(proposal("A"))
        idea = event["id"]
        self.client.publish(b.make_intent("A", "release", {
            "idea": idea, "lease_token": idea, "text": "A useful precise handoff."}))
        claim = self.client.publish(b.make_intent("B", "claim", {
            "idea": idea, "next_check": "New endpoint check", "lease_seconds": 60}))
        self.client.publish(b.make_intent("B", "finish", {
            "idea": idea, "lease_token": claim["id"], "text": "Fixture concluded.",
            "asset": self.asset}))
        with self.assertRaises(b.Conflict):
            self.client.publish(b.make_intent("C", "claim", {
                "idea": idea, "next_check": "duplicate", "lease_seconds": 60}))
        self.assertEqual(self.client.read()["ideas"][idea]["status"], "done")

    def test_lost_push_response_is_idempotent(self):
        original = b.git
        lost = False

        def lose_once(cwd, *args, **kwargs):
            nonlocal lost
            result = original(cwd, *args, **kwargs)
            if args[0] == "push" and not lost:
                lost = True
                raise b.BoardError("Simulated lost response after actual push.")
            return result

        intent = proposal("A")
        with patch.object(b, "git", lose_once):
            self.client.publish(intent)
        self.assertTrue(lost)
        self.assertEqual(len(self.client.read()["events"]), 1)
        self.assertFalse((self.client.outbox / (intent["id"] + ".json")).exists())
        again = self.client.publish(intent)
        self.assertEqual(again["id"], intent["id"])
        self.assertEqual(len(self.client.read()["events"]), 1)

    def test_committed_result_recovers_after_asset_branch_is_deleted(self):
        intent = b.make_intent("A", "result", {"text": "Frozen fixture", "asset": self.asset})
        original = b.git

        def lose_response(cwd, *args, **kwargs):
            result = original(cwd, *args, **kwargs)
            if args[0] == "push":
                raise b.BoardError("Lost response.")
            return result

        self.client.retries = 1
        with patch.object(b, "git", lose_response):
            with self.assertRaises(b.BoardError):
                self.client.publish(intent)
        call(self.repo, "push", "origin", "--delete", "work")
        recovered = self.client.publish(intent)
        self.assertEqual(recovered["id"], intent["id"])
        self.assertEqual(len(self.client.read()["events"]), 1)

    def test_asset_network_failure_preserves_pending_without_blocking_other_messages(self):
        intent = b.make_intent("A", "result", {"text": "Frozen fixture", "asset": self.asset})
        self.client.retries = 1
        with patch.object(self.client, "check_asset", side_effect=b.BoardError("Offline")):
            with self.assertRaises(b.BoardError):
                self.client.publish(intent)
        self.assertTrue((self.client.outbox / (intent["id"] + ".json")).exists())
        self.client.publish(b.make_intent("B", "discussion", {"text": "Unrelated useful message."}))
        self.client.publish(intent)
        self.assertEqual(len(self.client.read()["events"]), 2)

    def test_same_event_concurrent_retry_is_atomic_and_idempotent(self):
        intent = proposal("A")
        results = self.race([intent, intent])
        self.assertEqual(results[0]["id"], results[1]["id"])
        self.assertEqual(len(self.client.read()["events"]), 1)

    def test_frozen_asset_hash_branch_commit_and_file_type(self):
        self.client.check_asset(self.asset)
        for change in ({"sha256": "0" * 64}, {"commit": "1" * 40},
                       {"path": "../asset.md"}):
            with self.assertRaises(b.BoardError):
                self.client.check_asset(dict(self.asset, **change))
        tree = call(self.repo, "show", self.asset["commit"] + ":folder").encode() + b"\n"
        with self.assertRaises(b.BoardError):
            self.client.check_asset(dict(self.asset, path="folder",
                                         sha256=hashlib.sha256(tree).hexdigest()))

    def test_outbox_disappearing_during_same_id_confirmation_is_normal(self):
        intent = proposal("A")
        self.client.publish(intent)
        pending = self.client.outbox / (intent["id"] + ".json")
        pending.write_text(b.encode(intent))
        original = Path.read_text
        disappeared = False

        def disappear(path, *args, **kwargs):
            nonlocal disappeared
            if path == pending and not disappeared:
                disappeared = True
                path.unlink()
                raise FileNotFoundError(path)
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", disappear):
            event = self.client.publish(intent)
        self.assertTrue(disappeared)
        self.assertEqual(event["id"], intent["id"])
        self.assertEqual(len(self.client.read()["events"]), 1)

    def test_read_and_publish_preserve_dirty_checkout_and_fetch_head(self):
        (self.repo / "asset.md").write_text("Uncommitted work.\n")
        (self.repo / "untracked.md").write_text("Preserve me.\n")
        call(self.repo, "fetch", "origin", "work")
        before = (call(self.repo, "status", "--porcelain"),
                  call(self.repo, "rev-parse", "HEAD"),
                  (self.repo / ".git/FETCH_HEAD").read_bytes())
        self.client.read()
        self.client.publish(proposal("A"))
        after = (call(self.repo, "status", "--porcelain"),
                 call(self.repo, "rev-parse", "HEAD"),
                 (self.repo / ".git/FETCH_HEAD").read_bytes())
        self.assertEqual(before, after)

    def test_future_discussion_does_not_extend_other_actors_new_lease(self):
        future = b.Board(self.repo, clock=lambda: self.now + 86400)
        future.publish(b.make_intent("A", "discussion", {"text": "Clock skew fixture"}))
        event = self.client.publish(proposal("B"))
        self.assertEqual(self.client.read()["ideas"][event["id"]]["lease_until"], 1060)

    def test_inherited_git_index_and_worktree_do_not_route_scratch_commands(self):
        (self.repo / "draft.md").write_text("Important staged draft.\n")
        call(self.repo, "add", "draft.md")
        index = self.repo / ".git/index"
        before = (index.read_bytes(), call(self.repo, "status", "--porcelain"))
        overrides = {"GIT_INDEX_FILE": str(index),
                     "GIT_DIR": str(self.repo / ".git"),
                     "GIT_WORK_TREE": str(self.repo),
                     "GIT_OBJECT_DIRECTORY": str(self.repo / ".git/objects")}
        with patch.dict(os.environ, overrides):
            self.client.read()
            self.client.publish(proposal("A"))
        after = (index.read_bytes(), call(self.repo, "status", "--porcelain"))
        self.assertEqual(before, after)

    def test_scope_whitespace_does_not_bypass_dedup(self):
        intent = proposal("A")
        self.client.publish(intent)
        duplicate = proposal("B")
        for key in b.SCOPE:
            duplicate["body"][key] = "  " + duplicate["body"][key] + " \n "
        duplicate["body"]["next_check"] = "Different test name"
        with self.assertRaises(b.Conflict):
            self.client.publish(duplicate)

    def test_mathematical_symbol_case_is_not_silently_identified(self):
        first, second = proposal("A"), proposal("B")
        first["body"]["statement"] = "Bound W under the specified definition"
        second["body"]["statement"] = "Bound w under the specified definition"
        self.client.publish(first)
        self.client.publish(second)
        self.assertEqual(len(self.client.read()["ideas"]), 2)

    def test_required_fields_unknown_ids_and_lease_bounds(self):
        bad = proposal("A")
        del bad["body"]["obligation"]
        with self.assertRaises(b.BoardError):
            self.client.publish(bad)
        for seconds in (0, 59, 10801, True):
            bad = proposal("A")
            bad["body"]["lease_seconds"] = seconds
            with self.assertRaises(b.BoardError):
                self.client.publish(bad)
        with self.assertRaises(b.BoardError):
            self.client.publish(b.make_intent("A", "discussion", {
                "idea": "a" * 32, "text": "Unknown idea"}))
        with self.assertRaises(b.BoardError):
            self.client.publish(b.make_intent("A", "discussion", {
                "reply_to": "b" * 32, "text": "Unknown reply"}))
        self.assertEqual(len(self.client.read()["events"]), 0)

    def test_credential_content_is_rejected_before_persisting(self):
        intent = b.make_intent("A", "discussion", {
            "text": "ghp_" + "x" * 24})  # Synthetic, never a real credential.
        with self.assertRaises(b.BoardError):
            self.client.publish(intent)
        self.assertFalse((self.client.outbox / (intent["id"] + ".json")).exists())

    def test_live_smoke_cli_against_local_remote_and_frozen_source(self):
        source = Path(__file__).resolve().parents[1] / "tools/board.py"
        target = self.repo / "research/weighted_congestion_frontier/tools/board.py"
        target.parent.mkdir(parents=True)
        target.write_bytes(source.read_bytes())
        call(self.repo, "add", ".")
        call(self.repo, "commit", "-m", "Freeze source for live smoke fixture")
        call(self.repo, "branch", "main")
        call(self.repo, "push", "origin", "main")
        script = Path(__file__).resolve().parents[1] / "tools/live_smoke.py"
        result = subprocess.run([sys.executable, str(script), "--repo",
                                 str(self.repo), "--live"], capture_output=True,
                                text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["verified"])
        self.assertEqual(sum("conflict" in x for x in report["claims"]), 1)
        self.assertEqual(self.client.read()["ideas"][report["idea"]]["status"], "done")

    def test_live_smoke_requires_explicit_flag_before_writing(self):
        script = Path(__file__).resolve().parents[1] / "tools/live_smoke.py"
        result = subprocess.run([sys.executable, str(script), "--repo", str(self.repo)],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(len(self.client.read()["events"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
