"""Reproducible real-Git chat tests with independent clones and injected lost replies."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('wcg_board', Path(__file__).resolve().parents[1] / 'tools/board.py')
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


def call(directory, *args):
    return subprocess.check_output(['git', *args], cwd=directory, stderr=subprocess.DEVNULL).decode().strip()


def message(actor='R01', text='同题可以沿不同路线继续。', **extra):
    return b.make_intent(actor, 'message', dict(text=text, **extra))


class BoardTests(unittest.TestCase):
    def setUp(self):
        repo_root = Path(__file__).resolve().parents[3]
        common = Path(call(repo_root, 'rev-parse', '--git-common-dir'))
        fixture_root = (repo_root / common).resolve() / 'wcg-tests'
        fixture_root.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='fixture-', dir=fixture_root)
        self.root = Path(self.tmp.name)
        self.remote = self.root / 'remote.git'
        call(self.root, 'init', '--bare', str(self.remote))
        self.repo = self.root / 'work'
        call(self.root, 'clone', str(self.remote), str(self.repo))
        call(self.repo, 'config', 'user.name', 'Fixture')
        call(self.repo, 'config', 'user.email', 'fixture@example.invalid')
        (self.repo / 'asset.md').write_text('Frozen infrastructure fixture.\n')
        (self.repo / 'folder').mkdir()
        (self.repo / 'folder/child.md').write_text('child\n')
        (self.repo / 'link.md').symlink_to('asset.md')
        call(self.repo, 'add', '.')
        call(self.repo, 'commit', '-m', 'fixture')
        call(self.repo, 'branch', '-M', 'main')
        call(self.repo, 'push', 'origin', 'main')
        self.now = 1000
        self.client = b.Board(self.repo, clock=lambda: self.now)
        self.client.initialize()
        self.asset = {'branch': 'main', 'commit': call(self.repo, 'rev-parse', 'HEAD'),
                      'path': 'asset.md', 'sha256': hashlib.sha256((self.repo / 'asset.md').read_bytes()).hexdigest()}
        self.script = Path(b.__file__).resolve()

    def tearDown(self):
        self.tmp.cleanup()

    def clone(self, name):
        repo = self.root / name
        call(self.root, 'clone', '--single-branch', '--branch', 'main', str(self.remote), str(repo))
        return repo

    def race(self, intents, independent=True):
        repos = [self.clone('peer-' + str(i)) if independent else self.repo for i in range(len(intents))]
        barrier = threading.Barrier(len(intents))
        original = b.git
        used, lock = set(), threading.Lock()

        def synchronized(cwd, *args, **kwargs):
            if args and args[0] == 'push':
                ident = threading.get_ident()
                with lock:
                    first = ident not in used
                    used.add(ident)
                if first:
                    barrier.wait(timeout=15)
            return original(cwd, *args, **kwargs)

        def send(pair):
            repo, intent = pair
            return b.Board(repo, clock=lambda: self.now).publish(intent)

        with patch.object(b, 'git', synchronized):
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(intents)) as pool:
                return list(pool.map(send, zip(repos, intents)))

    def cli(self, *args, check=True):
        result = subprocess.run([sys.executable, str(self.script), '--repo', str(self.repo), *args],
                                capture_output=True, text=True, timeout=30)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def install_noncurrent_board(self):
        repo = self.root / 'noncurrent'
        call(self.root, 'clone', '--single-branch', '--branch', 'wcg/board', str(self.remote), str(repo))
        call(repo, 'config', 'user.name', 'Fixture')
        call(repo, 'config', 'user.email', 'fixture@example.invalid')
        root = repo / b.PREFIX
        (root / 'meta.json').write_text('{"schema": 1}\n')
        (root / 'events').mkdir(exist_ok=True)
        # Deliberately undecodable: migration deletes rather than interprets it.
        (root / 'events/obsolete.json').write_text('noncurrent infrastructure fixture\n')
        (root / 'obsolete.md').write_text('delete the inspected fixture\n')
        call(repo, 'add', '.')
        call(repo, 'commit', '-m', 'Inspected noncurrent infrastructure fixture')
        call(repo, 'push', 'origin', 'wcg/board')
        return repo, call(repo, 'rev-parse', 'HEAD')

    def test_direct_send_and_async_reply_without_registration(self):
        first = self.client.publish(message(thread='WC-TARGET'))
        self.client.publish(message('R02', thread='WC-TARGET'))
        unrelated = self.client.publish(message('R01', text='我先继续另一条路线。', thread='另一话题'))
        self.now += 600
        reply = self.client.publish(message('R02', text='现在补充一个边界。', reply_to=first['id'], thread='WC-TARGET'))
        state = self.client.read()
        self.assertEqual(set(state), {'events', 'last_time'})
        self.assertEqual(len(state['events']), 4)
        self.assertEqual(reply['body']['reply_to'], first['id'])
        filtered = self.cli('view', '--thread', 'WC-TARGET', '--limit', '1').stdout
        self.assertIn(reply['body']['text'], filtered)
        self.assertNotIn(unrelated['body']['text'], filtered)
        self.assertIn('回复 [R01 · 1]', filtered)

    def test_same_topic_concurrent_independent_clones_both_succeed(self):
        intents = [message('R01', thread='同题'), message('R02', thread='同题')]
        results = self.race(intents)
        state = self.client.read()
        self.assertEqual({e['id'] for e in state['events']}, {i['id'] for i in intents})
        self.assertEqual(sorted(e['seq'] for e in results), [1, 2])
        for event in state['events']:
            self.assertEqual(set(event['body']), {'text', 'thread'})

    def test_same_message_race_and_cross_clone_replay_are_idempotent(self):
        intent = message()
        results = self.race([intent, intent])
        self.assertEqual(results[0], results[1])
        self.assertEqual(len(self.client.read()['events']), 1)
        other = b.Board(self.clone('later'))
        self.assertEqual(other.publish(intent), results[0])
        changed = dict(intent, body={'text': 'Different content'})
        with self.assertRaises(b.Conflict):
            other.publish(changed)
        self.assertEqual(len(self.client.read()['events']), 1)

    def test_lost_success_response_recovers_without_duplicate(self):
        original, lost = b.git, False

        def lose_once(cwd, *args, **kwargs):
            nonlocal lost
            result = original(cwd, *args, **kwargs)
            if args[0] == 'push' and not lost:
                lost = True
                raise b.BoardError('Simulated lost response after actual push.')
            return result

        intent = message()
        with patch.object(b, 'git', lose_once):
            event = self.client.publish(intent)
        self.assertTrue(lost)
        self.assertEqual(event['id'], intent['id'])
        self.assertEqual(len(self.client.read()['events']), 1)
        self.assertFalse((self.client.outbox / (intent['id'] + '.json')).exists())

    def test_failed_network_keeps_local_intent_and_retry_cli(self):
        intent = message(text='Retry this exact message.')
        self.client.retries = 1
        with patch.object(self.client, 'load', side_effect=b.BoardError('Offline')):
            with self.assertRaisesRegex(b.BoardError, intent['id']):
                self.client.publish(intent)
        self.assertEqual(json.loads((self.client.outbox / (intent['id'] + '.json')).read_text()), intent)
        self.assertEqual(json.loads(self.cli('pending').stdout), [intent['id']])
        self.client.publish(message('R02', text='Other messages remain independent.'))
        recovered = json.loads(self.cli('retry', '--event-id', intent['id']).stdout)
        self.assertEqual(recovered['body'], intent['body'])
        self.assertEqual(json.loads(self.cli('retry', '--event-id', intent['id']).stdout), recovered)
        self.assertEqual(len(self.client.read()['events']), 2)

    def test_local_discard_changes_no_remote_message(self):
        intent = message()
        self.client.retries = 1
        with patch.object(self.client, 'load', side_effect=b.BoardError('Offline')):
            with self.assertRaises(b.BoardError):
                self.client.publish(intent)
        self.cli('discard', '--event-id', intent['id'])
        self.assertFalse((self.client.outbox / (intent['id'] + '.json')).exists())
        self.assertEqual(self.client.read()['events'], [])

    def test_remote_receipt_recovers_after_asset_branch_disappears(self):
        call(self.repo, 'branch', 'work')
        call(self.repo, 'push', 'origin', 'work')
        asset = dict(self.asset, branch='work')
        intent = b.make_intent('R01', 'result', {'text': 'Frozen file', 'asset': asset})
        original = b.git

        def lose(cwd, *args, **kwargs):
            result = original(cwd, *args, **kwargs)
            if args[0] == 'push':
                raise b.BoardError('Lost response')
            return result

        self.client.retries = 1
        with patch.object(b, 'git', lose):
            with self.assertRaises(b.BoardError):
                self.client.publish(intent)
        call(self.repo, 'push', 'origin', '--delete', 'work')
        self.assertEqual(self.client.publish(intent)['id'], intent['id'])
        self.assertEqual(len(self.client.read()['events']), 1)

    def test_frozen_asset_hash_commit_path_and_regular_file(self):
        self.client.check_asset(self.asset)
        for change in ({'sha256': '0' * 64}, {'commit': '1' * 40}, {'path': '../asset.md'},
                       {'path': 'folder'}, {'path': 'link.md'}, {'commit': True}, {'path': '.'}):
            with self.subTest(change=change):
                with self.assertRaises(b.BoardError):
                    self.client.check_asset(dict(self.asset, **change))
        event = self.client.publish(b.make_intent('R01', 'result', {'text': 'Asset check passed.', 'asset': self.asset}))
        self.assertEqual(event['body']['asset'], self.asset)

    def test_asset_network_failure_does_not_block_other_messages(self):
        intent = b.make_intent('R01', 'result', {'text': 'Frozen file', 'asset': self.asset})
        self.client.retries = 1
        with patch.object(self.client, 'check_asset', side_effect=b.BoardError('Offline')):
            with self.assertRaises(b.BoardError):
                self.client.publish(intent)
        self.client.publish(message('R02'))
        self.client.publish(intent)
        self.assertEqual(len(self.client.read()['events']), 2)

    def test_dirty_checkout_fetch_head_and_staged_index_are_preserved(self):
        (self.repo / 'asset.md').write_text('Uncommitted draft.\n')
        (self.repo / 'draft.md').write_text('Important staged work.\n')
        call(self.repo, 'add', 'draft.md')
        call(self.repo, 'fetch', 'origin', 'main')
        index = self.repo / '.git/index'
        before = (index.read_bytes(), call(self.repo, 'status', '--porcelain'), call(self.repo, 'rev-parse', 'HEAD'),
                  (self.repo / '.git/FETCH_HEAD').read_bytes())
        overrides = {'GIT_INDEX_FILE': str(index), 'GIT_DIR': str(self.repo / '.git'),
                     'GIT_WORK_TREE': str(self.repo), 'GIT_OBJECT_DIRECTORY': str(self.repo / '.git/objects')}
        with patch.dict(os.environ, overrides):
            self.client.read()
            self.client.publish(message())
        after = (index.read_bytes(), call(self.repo, 'status', '--porcelain'), call(self.repo, 'rev-parse', 'HEAD'),
                 (self.repo / '.git/FETCH_HEAD').read_bytes())
        self.assertEqual(before, after)

    def test_cli_text_file_stable_id_and_json_export(self):
        text = self.root / 'message.txt'
        text.write_text('两行内容\n第二行，保留数学符号 W ≠ w。\n')
        event_id = 'a' * 32
        event = json.loads(self.cli('say', '--actor', 'R01', '--event-id', event_id,
                                    '--text-file', str(text), '--thread', 'WC-TARGET').stdout)
        self.assertEqual(event['body']['text'], text.read_text())
        self.assertEqual(json.loads(self.cli('say', '--actor', 'R01', '--event-id', event_id,
                                            '--text-file', str(text), '--thread', 'WC-TARGET').stdout), event)
        self.assertEqual(json.loads(self.cli('view', '--json').stdout)['events'], [event])
        self.assertEqual(self.cli('say', '--actor', 'R01', '--text', 'x', '--text-file', str(text), check=False).returncode, 2)
        self.assertEqual(self.cli('view', '--limit', '-1', check=False).returncode, 2)

    def test_invalid_fields_and_secret_fail_before_network_or_disk(self):
        bad = [message('', text='x'), message('team/root'), message(text=' '), message(thread=''),
               message(thread='line\nbreak'), message(thread='x' * 161), message(reply_to='missing'),
               message(text='ghp_' + 'x' * 24), message(asset={'commit': 'a'}),
               b.make_intent('R01', 'result', {'text': 'missing asset'}),
               b.make_intent('R01', 'unknown', {'text': 'x'}), message(extra='unknown')]
        for intent in bad:
            with self.subTest(intent=intent):
                with patch.object(self.client, 'load', side_effect=AssertionError('Invalid intent reached network')):
                    with self.assertRaises(b.BoardError):
                        self.client.publish(intent)
                self.assertFalse((self.client.outbox / (intent['id'] + '.json')).exists())
        for retries in (0, True, 51):
            with self.assertRaises(b.BoardError):
                b.Board(self.repo, retries=retries)

    def test_unknown_reply_is_rejected_without_retry(self):
        with patch.object(b, 'retry_pause', side_effect=AssertionError('Validation retried')):
            with self.assertRaises(b.ValidationError):
                self.client.publish(message(reply_to='b' * 32))
        self.assertEqual(self.client.read()['events'], [])

    def test_outbox_disappearing_during_confirmation_is_normal(self):
        intent = message()
        self.client.publish(intent)
        pending = self.client.outbox / (intent['id'] + '.json')
        pending.write_text(b.encode(intent))
        original, disappeared = Path.read_text, False

        def disappear(path, *args, **kwargs):
            nonlocal disappeared
            if path == pending and not disappeared:
                disappeared = True
                path.unlink()
                raise FileNotFoundError(path)
            return original(path, *args, **kwargs)

        with patch.object(Path, 'read_text', disappear):
            event = self.client.publish(intent)
        self.assertTrue(disappeared)
        self.assertEqual(event['id'], intent['id'])
        self.assertEqual(len(self.client.read()['events']), 1)

    def test_migration_deletes_inspected_noncurrent_files_by_fast_forward(self):
        _, old_head = self.install_noncurrent_board()
        with self.assertRaises(b.BoardError):
            self.client.read()
        self.assertEqual(self.client.migrate(old_head)['status'], 'migrated')
        self.assertEqual(self.client.read()['events'], [])
        call(self.repo, 'fetch', 'origin', 'wcg/board')
        head = call(self.repo, 'rev-parse', 'FETCH_HEAD')
        self.assertEqual(call(self.repo, 'rev-parse', head + '^'), old_head)
        self.assertNotIn('obsolete', call(self.repo, 'ls-tree', '-r', '--name-only', head))
        self.assertEqual(json.loads(call(self.repo, 'show', head + ':' + str(b.PREFIX / 'meta.json'))), {'schema': 3})

    def test_migration_fences_new_noncurrent_changes(self):
        repo, inspected = self.install_noncurrent_board()
        (repo / b.PREFIX / 'new.txt').write_text('Concurrent change\n')
        call(repo, 'add', '.')
        call(repo, 'commit', '-m', 'Concurrent noncurrent change')
        call(repo, 'push', 'origin', 'wcg/board')
        with self.assertRaises(b.Conflict):
            self.client.migrate(inspected)
        current = call(repo, 'rev-parse', 'HEAD')
        self.assertEqual(call(self.repo, 'ls-remote', 'origin', 'refs/heads/wcg/board').split()[0], current)

    def test_migration_retains_current_messages_and_is_idempotent(self):
        old_head = call(self.repo, 'ls-remote', 'origin', 'refs/heads/wcg/board').split()[0]
        event = self.client.publish(message(text='真实新消息必须保留。'))
        report = self.client.migrate(old_head)
        self.assertEqual(report['status'], 'already-current')
        self.assertEqual(report['events'], 1)
        self.assertEqual(self.client.read()['events'], [event])
        self.assertEqual(json.loads(self.cli('migrate', '--expected-head', old_head).stdout)['events'], 1)

    def test_migration_lost_response_confirms_remote(self):
        _, old_head = self.install_noncurrent_board()
        original = b.git

        def lost(cwd, *args, **kwargs):
            result = original(cwd, *args, **kwargs)
            if args[0] == 'push':
                raise b.BoardError('Lost response')
            return result

        with patch.object(b, 'git', lost):
            self.assertEqual(self.client.migrate(old_head)['status'], 'migrated')
        self.assertEqual(self.client.read()['events'], [])

    def test_concurrent_migration_and_new_chat_message_are_preserved(self):
        repo, old_head = self.install_noncurrent_board()
        original, raced = b.git, False
        event = dict(message('R02', text='迁移后立即发出的真实消息。'),
                     schema=b.SCHEMA, seq=1, time=self.now)

        def simultaneous(cwd, *args, **kwargs):
            nonlocal raced
            if args[0] == 'push' and not raced:
                raced = True
                self.assertFalse(any('force' in arg or arg.startswith('+') for arg in args))
                shutil.rmtree(repo / b.PREFIX)
                self.client.write_empty(repo)
                (repo / b.PREFIX / 'events' / f"00000001_{event['id']}.json").write_text(b.encode(event))
                call(repo, 'add', '--all', '.')
                call(repo, 'commit', '-m', 'Another migration and immediate chat message')
                call(repo, 'push', 'origin', 'wcg/board')
            return original(cwd, *args, **kwargs)

        with patch.object(b, 'git', simultaneous):
            self.assertEqual(self.client.migrate(old_head)['events'], 1)
        self.assertTrue(raced)
        self.assertEqual(self.client.read()['events'], [event])

    def test_metadata_requires_integer_current_schema(self):
        self.assertTrue(b.current_metadata({'schema': b.SCHEMA}))
        for value in ({'schema': float(b.SCHEMA)}, {'schema': True},
                      {'schema': b.SCHEMA, 'extra': 'x'}, [], None):
            self.assertFalse(b.current_metadata(value))

    def test_initialize_current_board_does_not_clear_messages(self):
        event = self.client.publish(message())
        self.assertEqual(self.client.initialize(), 'already initialized')
        self.assertEqual(self.client.read()['events'], [event])

    def test_transition_failure_preserves_input_and_case_sensitive_symbols(self):
        state = b.empty_state()
        event = dict(message(text='W ≠ w'), schema=b.SCHEMA, seq=2, time=0)
        with self.assertRaises(b.BoardError):
            b.transition(state, event)
        self.assertEqual(state, b.empty_state())
        for field, value in [('schema', True), ('seq', True), ('time', True), ('time', -1)]:
            invalid = dict(event, seq=1, **{field: value}) if field != 'seq' else dict(event, seq=value)
            with self.assertRaises(b.BoardError):
                b.transition(state, invalid)
        self.assertIn('W ≠ w', self.client.publish(message(text='W ≠ w'))['body']['text'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
