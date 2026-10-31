#!/usr/bin/env python3
"""Asynchronous Git chat: one prompt-defined actor per Work conversation.

Messages have separate files. Failed sends retain stable IDs for retry; ordinary
pushes reload the latest remote history while leaving the caller's checkout alone.
"""
from __future__ import annotations
import argparse
import copy
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import time
import uuid

PREFIX = Path('research/weighted_congestion_frontier/board')
SCHEMA = 3
SECRET = re.compile(r'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}')
UUID = re.compile(r'[0-9a-f]{32}')
KINDS = {'message', 'discussion', 'progress', 'help', 'objection',
         'review_request', 'review', 'barrier', 'result'}
INTENT_KEYS = {'id', 'actor', 'kind', 'body'}
BODY_KEYS = {'text', 'thread', 'reply_to', 'asset', 'save', 'to', 'mentions'}
ADDRESS = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}')
DEFAULT_SAVE = 'shared'


class BoardError(Exception):
    pass


class Conflict(BoardError):
    pass


class ValidationError(BoardError):
    pass


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def guard(value):
    if SECRET.search(encode(value)):
        raise ValidationError('Credential-like content cannot enter the public board.')


def valid_id(value):
    if not isinstance(value, str) or not UUID.fullmatch(value):
        raise ValidationError('Message IDs must be 32 lowercase hex characters.')


def address(value):
    if not isinstance(value, str) or not ADDRESS.fullmatch(value):
        raise ValidationError('Use a safe Worker or save ID (letters, digits, dot, underscore, hyphen).')
    return value


def save_of(event):
    return event['body'].get('save', DEFAULT_SAVE)


def participants(event):
    target = event['body'].get('to')
    return frozenset((event['actor'], target)) if target else frozenset()


def visible(event, actor=None):
    return not participants(event) or actor in participants(event)


def attention(event, actor, by_id):
    body = event['body']
    if body.get('to'):
        return body['to'] == actor
    if event['actor'] == actor:
        return False
    parent = by_id.get(body.get('reply_to'))
    return actor in body.get('mentions', []) or bool(parent and parent['actor'] == actor)


def asset_shape(asset):
    if not isinstance(asset, dict) or set(asset) != {'branch', 'commit', 'path', 'sha256'}:
        raise ValidationError('Asset needs exactly branch, commit, path and sha256.')
    if not all(isinstance(value, str) for value in asset.values()):
        raise ValidationError('Asset descriptor fields must be strings.')
    if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', asset['commit']):
        raise ValidationError('Use a full immutable commit ID.')
    path = PurePosixPath(asset['path'])
    if (path.is_absolute() or '..' in path.parts or not path.parts or
            ':' in str(path) or any(c in asset['path'] for c in '\x00\r\n')):
        raise ValidationError('Asset path must be repository-relative.')
    if not re.fullmatch(r'[0-9a-f]{64}', asset['sha256']):
        raise ValidationError('Use a full SHA-256 digest.')


def validate_intent(intent):
    guard(intent)
    if not isinstance(intent, dict) or set(intent) != INTENT_KEYS:
        raise ValidationError('A message needs exactly id, actor, kind and body.')
    valid_id(intent['id'])
    actor = intent['actor']
    if not isinstance(actor, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,100}', actor):
        raise ValidationError('Use the simple role ID from this conversation\'s prompt.')
    if not isinstance(intent['kind'], str) or intent['kind'] not in KINDS:
        raise ValidationError('Unknown message kind.')
    body = intent['body']
    if not isinstance(body, dict) or not set(body) <= BODY_KEYS:
        raise ValidationError('Message body supports text, thread, reply_to and asset.')
    if not isinstance(body.get('text'), str) or not body['text'].strip():
        raise ValidationError('Messages need nonempty text.')
    if 'thread' in body and (not isinstance(body['thread'], str) or
            not body['thread'].strip() or len(body['thread']) > 160 or
            any(c in body['thread'] for c in '\r\n')):
        raise ValidationError('Thread must be a nonempty single-line label of at most 160 characters.')
    if 'reply_to' in body:
        valid_id(body['reply_to'])
    if 'save' in body:
        address(body['save'])
    if 'to' in body:
        address(body['to'])
        if body['to'] == actor:
            raise ValidationError('A direct message needs another Worker.')
    if 'mentions' in body:
        mentions = body['mentions']
        if not isinstance(mentions, list) or len(mentions) != len(set(mentions)):
            raise ValidationError('mentions must be a list of distinct Worker IDs.')
        for person in mentions:
            address(person)
        if body.get('to') and set(mentions) - {actor, body['to']}:
            raise ValidationError('A direct message cannot notify an outside participant.')
    if 'asset' in body:
        asset_shape(body['asset'])
    if intent['kind'] == 'result' and 'asset' not in body:
        raise ValidationError('A result message needs a pushed frozen asset.')


def empty_state():
    return {'events': [], 'last_time': 0}


def current_metadata(value):
    return (isinstance(value, dict) and set(value) == {'schema'} and
            type(value['schema']) is int and value['schema'] == SCHEMA)


def transition(state, event):
    """Return a new validated state; a failed message never mutates its input."""
    if not isinstance(event, dict) or set(event) != INTENT_KEYS | {'schema', 'seq', 'time'}:
        raise ValidationError('Invalid message record fields.')
    validate_intent({key: event[key] for key in INTENT_KEYS})
    if type(event['schema']) is not int or event['schema'] != SCHEMA:
        raise ValidationError('Unsupported message schema.')
    if type(event['seq']) is not int or event['seq'] != len(state['events']) + 1:
        raise ValidationError('Noncontiguous message sequence.')
    if type(event['time']) is not int or event['time'] < 0:
        raise ValidationError('Invalid message time.')
    if any(old['id'] == event['id'] for old in state['events']):
        raise Conflict('Duplicate message ID.')
    if 'reply_to' in event['body']:
        parent = next((old for old in state['events'] if old['id'] == event['body']['reply_to']), None)
        if parent is None:
            raise ValidationError('reply_to is not an existing message.')
        if save_of(parent) != save_of(event):
            raise ValidationError('A reply cannot cross research saves.')
        if participants(parent) and participants(event) != participants(parent):
            raise ValidationError('A private reply must keep the same two participants.')
    out = copy.deepcopy(state)
    out['events'].append(copy.deepcopy(event))
    out['last_time'] = event['time']
    return out


def git(cwd, *args, check=True, timeout=45):
    env = os.environ.copy()
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE',
                'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
                'GIT_IMPLICIT_WORK_TREE', 'GIT_GRAFT_FILE', 'GIT_SHALLOW_FILE',
                'GIT_PREFIX', 'GIT_INTERNAL_SUPER_PREFIX'):
        env.pop(key, None)
    env['GIT_TERMINAL_PROMPT'] = '0'
    try:
        result = subprocess.run(['git', *args], cwd=cwd, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise BoardError('Git timed out; retry using the saved message ID.') from exc
    if check and result.returncode:
        detail = SECRET.sub('[REDACTED]', result.stderr.decode(errors='replace'))
        raise BoardError('Git operation failed: ' + detail.strip()[:1000])
    return result


def utc(value):
    return time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(value))


def retry_pause(event_id, attempt):
    jitter = int(hashlib.sha256(f'{event_id}:{attempt}'.encode()).hexdigest()[:4], 16) / 65535
    time.sleep(min(0.5, 0.03 * 2 ** min(attempt, 4)) * (0.5 + jitter))


def render(state, now=None, selected=None, actor=None):
    lines = ['# 研究公屏', '', '每个 Work 对话使用一个稳定发布标识署名；程序可自动生成。',
             '消息随时发布、异步回复；同题的多条研究路线可以同时推进。',
             '子 agent 的发现由所在对话转述。', '',
             '研究资产统一保存在 main；公屏用于异步研讨，消息中的冻结文件附带 commit 和 SHA-256。', '',
             '## 最近消息', '']
    allowed = [e for e in state['events'] if visible(e, actor)]
    displayed = allowed[-50:] if selected is None else [e for e in selected if visible(e, actor)]
    by_id = {event['id']: event for event in state['events']}
    for event in displayed:
        path = f"events/{event['seq']:08d}_{event['id']}.json"
        body = event['body']
        lines += [f"### {event['seq']} · {event['actor']} · {event['kind']}", '',
                  f'[完整消息]({path}) · {utc(event["time"])}', '']
        if 'thread' in body:
            lines += ['话题：' + body['thread'], '']
        if body.get('to'):
            lines += [f'双方私聊：{event["actor"]} → {body["to"]}（同仓可读，不是权限隔离）', '']
        if 'save' in body:
            lines += ['研究存档：' + body['save'], '']
        if body.get('mentions'):
            lines += ['提及：' + ' '.join('@' + p for p in body['mentions']), '']
        if 'reply_to' in body:
            parent = by_id[body['reply_to']]
            target = f"events/{parent['seq']:08d}_{parent['id']}.json"
            lines += [f"回复 [{parent['actor']} · {parent['seq']}]({target})", '']
        lines += [body['text'], '']
        if 'asset' in body:
            lines += ['冻结资产：', '', '```json', encode(body['asset']).strip(), '```', '']
    if not displayed:
        lines += ['公屏已就绪，直接发送第一条消息。' if not state['events'] else '本次筛选没有消息。', '']
    return '\n'.join(lines) + '\n'


class Board:
    def __init__(self, repo, branch='wcg/board', retries=20, clock=time.time):
        if type(retries) is not int or not 1 <= retries <= 50:
            raise ValidationError('Retry limit must be an integer from 1 to 50.')
        self.repo = Path(git(repo, 'rev-parse', '--show-toplevel').stdout.decode().strip())
        self.remote = git(self.repo, 'remote', 'get-url', 'origin').stdout.decode().strip()
        if SECRET.search(self.remote) or re.search(r'https?://[^/]*@', self.remote):
            raise ValidationError('Origin must not embed a credential.')
        git(self.repo, 'check-ref-format', 'refs/heads/' + branch)
        self.branch, self.retries, self.clock = branch, retries, clock
        common = git(self.repo, 'rev-parse', '--git-common-dir').stdout.decode().strip()
        self.cache = (self.repo / common).resolve() / 'wcg'
        self.cache.mkdir(parents=True, exist_ok=True)
        namespace = hashlib.sha256(f'{SCHEMA}:{branch}'.encode()).hexdigest()[:12]
        self.outbox = self.cache / namespace
        self.outbox.mkdir(exist_ok=True)

    def scratch(self):
        return tempfile.TemporaryDirectory(prefix='board-', dir=self.cache)

    def setup(self, directory):
        git(directory, 'init', '--quiet')
        git(directory, 'config', 'user.name', 'WCG Researcher')
        git(directory, 'config', 'user.email', 'wcg@users.noreply.github.com')
        git(directory, 'remote', 'add', 'origin', self.remote)

    def checkout(self, directory):
        git(directory, 'fetch', '--quiet', '--no-tags', '--depth=1',
            'origin', 'refs/heads/' + self.branch)
        git(directory, 'checkout', '--quiet', '--detach', 'FETCH_HEAD')
        return git(directory, 'rev-parse', 'HEAD').stdout.decode().strip()

    def decode(self, directory):
        root = Path(directory) / PREFIX
        meta = root / 'meta.json'
        try:
            self.check_paths(directory)
            if meta.is_symlink() or not current_metadata(json.loads(meta.read_text())):
                raise ValidationError('Use the explicit migrate command to create the current chat board.')
            events = root / 'events'
            if events.is_symlink():
                raise ValidationError('Board paths must be ordinary directories.')
            state = empty_state()
            for path in sorted(events.glob('*.json')):
                if path.is_symlink():
                    raise ValidationError('Message records must be ordinary files.')
                event = json.loads(path.read_text())
                state = transition(state, event)
                if path.name != f"{event['seq']:08d}_{event['id']}.json":
                    raise ValidationError('Message filename/sequence mismatch.')
            return state
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ValidationError('Unreadable board metadata or message record.') from exc

    def check_paths(self, directory):
        path = Path(directory)
        for part in PREFIX.parts:
            path = path / part
            if path.is_symlink():
                raise ValidationError('Board paths must be ordinary directories.')

    def load(self, directory):
        self.checkout(directory)
        return self.decode(directory)

    def write_empty(self, directory):
        root = Path(directory) / PREFIX
        root.mkdir(parents=True, exist_ok=True)
        (root / 'events').mkdir(exist_ok=True)
        (root / 'meta.json').write_text(encode({'schema': SCHEMA}))
        (root / 'README.md').write_text(
            '# 研究公屏\n\n[最近消息](BOARD.md)。\n\n'
            '使用 main 的 tools/work.py read / send --text，按提示词角色号直接交流。\n')
        (root / 'BOARD.md').write_text(render(empty_state()))

    def initialize(self):
        found = git(self.repo, 'ls-remote', '--exit-code', 'origin',
                    'refs/heads/' + self.branch, check=False)
        if found.returncode == 0:
            self.read()
            return 'already initialized'
        if found.returncode != 2:
            raise BoardError('Cannot establish whether board branch exists.')
        with self.scratch() as directory:
            self.setup(directory)
            self.write_empty(directory)
            git(directory, 'add', str(PREFIX))
            git(directory, 'commit', '--quiet', '-m', 'Initialize asynchronous WCG chat')
            git(directory, 'push', '--quiet', 'origin', 'HEAD:refs/heads/' + self.branch, check=False)
            self.read()
        return 'initialized'

    def migrate(self, expected_head):
        """Replace the inspected noncurrent board by fast-forward; retain current chat."""
        if not isinstance(expected_head, str) or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', expected_head):
            raise ValidationError('Migration needs the full inspected remote commit ID.')
        with self.scratch() as directory:
            self.setup(directory)
            head = self.checkout(directory)
            self.check_paths(directory)
            meta = Path(directory) / PREFIX / 'meta.json'
            try:
                current = not meta.is_symlink() and current_metadata(json.loads(meta.read_text()))
            except (OSError, ValueError):
                current = False
            if current:
                state = self.decode(directory)
                return {'status': 'already-current', 'head': head, 'events': len(state['events'])}
            if head != expected_head:
                raise Conflict('Remote board changed after inspection; inspect its new commit before migrating.')
            root = Path(directory) / PREFIX
            if root.is_symlink():
                root.unlink()
            elif root.exists():
                shutil.rmtree(root)
            self.write_empty(directory)
            git(directory, 'add', '--all', str(PREFIX))
            git(directory, 'commit', '--quiet', '-m', 'Replace board with asynchronous research chat')
            try:
                git(directory, 'push', '--quiet', 'origin', 'HEAD:refs/heads/' + self.branch)
            except BoardError:
                self.read()  # Confirm a lost push response or another completed migration.
            state = self.read()
            return {'status': 'migrated', 'events': len(state['events'])}

    def read(self):
        with self.scratch() as directory:
            self.setup(directory)
            return self.load(directory)

    @contextlib.contextmanager
    def seen_lock(self, actor, save):
        key = hashlib.sha256(f'{address(actor)}:{address(save)}'.encode()).hexdigest()
        path = self.cache / ('seen-' + key + '.json')
        with (self.cache / ('seen-' + key + '.lock')).open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield path

    def seen(self, actor, save):
        with self.seen_lock(actor, save) as path:
            if not path.exists():
                return set()
            result = json.loads(path.read_text())
            if not isinstance(result, list):
                raise ValidationError('Unread cursor is damaged; preserve it before resetting.')
            for ident in result:
                valid_id(ident)
            return set(result)

    def acknowledge(self, actor, save, ids):
        state = self.read()
        by_id = {e['id']: e for e in state['events']}
        for ident in ids:
            valid_id(ident)
            event = by_id.get(ident)
            if event is None or save_of(event) != save or not visible(event, actor):
                raise ValidationError('Cannot acknowledge an absent or unrelated message.')
            if not attention(event, actor, by_id):
                raise ValidationError('This message is not addressed to this inbox.')
        with self.seen_lock(actor, save) as path:
            old = json.loads(path.read_text()) if path.exists() else []
            if not isinstance(old, list):
                raise ValidationError('Unread cursor is damaged.')
            for ident in old:
                valid_id(ident)
            with tempfile.NamedTemporaryFile(mode='w', dir=self.cache, delete=False) as stream:
                temporary = Path(stream.name)
                try:
                    stream.write(encode(sorted(set(old) | set(ids))))
                    stream.flush()
                    os.fsync(stream.fileno())
                except BaseException:
                    temporary.unlink(missing_ok=True)
                    raise
            try:
                os.replace(temporary, path)
            finally:
                temporary.unlink(missing_ok=True)
        return {'status': 'read', 'actor': actor, 'save': save, 'ids': ids,
                'meaning': 'read receipt only; not mathematical adoption'}

    def check_asset(self, asset):
        asset_shape(asset)
        guard(asset)
        git(self.repo, 'check-ref-format', 'refs/heads/' + asset['branch'])
        with self.scratch() as directory:
            self.setup(directory)
            git(directory, 'fetch', '--quiet', '--no-tags', 'origin', 'refs/heads/' + asset['branch'])
            if git(directory, 'merge-base', '--is-ancestor', asset['commit'], 'FETCH_HEAD', check=False).returncode:
                raise ValidationError('Asset commit is not on the named remote branch.')
            entry = git(directory, 'ls-tree', asset['commit'], '--', asset['path']).stdout
            if not entry.startswith((b'100644 blob ', b'100755 blob ')):
                raise ValidationError('Asset must name an ordinary file.')
            content = git(directory, 'cat-file', 'blob', asset['commit'] + ':' + asset['path']).stdout
            if hashlib.sha256(content).hexdigest() != asset['sha256']:
                raise ValidationError('Asset hash disagrees with the pushed frozen file.')

    def publish(self, intent):
        validate_intent(intent)
        pending = self.outbox / (intent['id'] + '.json')
        while True:
            try:
                saved = json.loads(pending.read_text())
            except FileNotFoundError:
                saved = None
            if saved is not None:
                if saved != intent:
                    raise Conflict('A message ID cannot be reused for changed content.')
                break
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.outbox, delete=False) as f:
                temporary = Path(f.name)
                f.write(encode(intent))
                f.flush()
                os.fsync(f.fileno())
            try:
                try:
                    os.link(temporary, pending)
                except FileExistsError:
                    continue
            finally:
                temporary.unlink(missing_ok=True)
            break
        error = None
        for attempt in range(self.retries):
            try:
                with self.scratch() as directory:
                    self.setup(directory)
                    state = self.load(directory)
                    existing = next((e for e in state['events'] if e['id'] == intent['id']), None)
                    if existing:
                        if {key: existing[key] for key in INTENT_KEYS} != intent:
                            raise Conflict('Remote message ID belongs to different content.')
                        pending.unlink(missing_ok=True)
                        return existing
                    if 'asset' in intent['body']:
                        self.check_asset(intent['body']['asset'])
                    event = dict(intent, schema=SCHEMA, seq=len(state['events']) + 1, time=int(self.clock()))
                    updated = transition(state, event)
                    root = Path(directory) / PREFIX
                    events = root / 'events'
                    events.mkdir(exist_ok=True)
                    (events / f"{event['seq']:08d}_{event['id']}.json").write_text(encode(event))
                    (root / 'BOARD.md').write_text(render(updated))
                    git(directory, 'add', str(PREFIX))
                    git(directory, 'commit', '--quiet', '-m', f"board: {event['actor']} {event['kind']} {event['id']}")
                    git(directory, 'push', '--quiet', 'origin', 'HEAD:refs/heads/' + self.branch)
                    confirmed = self.read()
                    found = next((e for e in confirmed['events'] if e['id'] == intent['id']), None)
                    if found:
                        pending.unlink(missing_ok=True)
                        return found
                    raise BoardError('Remote confirmation missing; message remains pending.')
            except (Conflict, ValidationError):
                raise
            except BoardError as exc:
                error = exc
                if attempt + 1 < self.retries:
                    retry_pause(intent['id'], attempt)
        raise BoardError(f"{error} Pending message ID: {intent['id']}")


def make_intent(actor, kind, body, event_id=None):
    return {'id': event_id or uuid.uuid4().hex, 'actor': actor, 'kind': kind, 'body': body}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--branch', default='wcg/board')
    parser.add_argument('--retries', type=int, default=20)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    migrate = sub.add_parser('migrate', help='Explicitly replace an inspected noncurrent board with an empty chat')
    migrate.add_argument('--expected-head', required=True)
    view = sub.add_parser('view')
    view.add_argument('--json', action='store_true')
    view.add_argument('--thread')
    view.add_argument('--limit', type=int)
    view.add_argument('--save')
    view.add_argument('--actor')
    view.add_argument('--peer')
    view.add_argument('--inbox', action='store_true')
    view.add_argument('--unread', action='store_true')
    ack = sub.add_parser('ack', help='Record a local read receipt, not mathematical acceptance')
    ack.add_argument('--actor', required=True)
    ack.add_argument('--save', default=DEFAULT_SAVE)
    ack.add_argument('--event-id', action='append', required=True)
    sub.add_parser('pending')
    for command in ('retry', 'discard'):
        operation = sub.add_parser(command)
        operation.add_argument('--event-id', required=True)
        operation.add_argument('--actor')
    say = sub.add_parser('say')
    say.add_argument('--actor', required=True)
    say.add_argument('--event-id')
    text = say.add_mutually_exclusive_group(required=True)
    text.add_argument('--text')
    text.add_argument('--text-file')
    say.add_argument('--kind', choices=sorted(KINDS), default='message')
    say.add_argument('--thread')
    say.add_argument('--reply-to')
    say.add_argument('--asset-json')
    say.add_argument('--save')
    say.add_argument('--to')
    say.add_argument('--mention', action='append', default=[])
    args = parser.parse_args()
    client = Board(args.repo, args.branch, retries=args.retries)
    if args.command == 'init':
        print(client.initialize())
    elif args.command == 'migrate':
        print(encode(client.migrate(args.expected_head)), end='')
    elif args.command == 'view':
        if args.limit is not None and args.limit < 0:
            raise ValidationError('View limit must be nonnegative; zero shows all messages.')
        state = client.read()
        if args.actor is not None:
            address(args.actor)
        if args.save is not None:
            address(args.save)
        if args.peer is not None:
            address(args.peer)
            if args.peer == args.actor:
                raise ValidationError('A private conversation needs another Worker.')
        if (args.inbox or args.peer or args.unread) and not args.actor:
            raise ValidationError('Personal views require an explicit Worker ID.')
        by_id = {e['id']: e for e in state['events']}
        selected = [e for e in state['events']
                    if (args.save is None or save_of(e) == args.save)
                    and visible(e, args.actor if args.inbox or args.peer else None)
                    and (not args.thread or e['body'].get('thread') == args.thread)]
        if args.peer:
            selected = [e for e in selected if participants(e) == {args.actor, args.peer}]
        if args.inbox:
            selected = [e for e in selected if attention(e, args.actor, by_id)]
        if args.unread:
            if not args.save:
                raise ValidationError('Unread queries require a research save.')
            seen = client.seen(args.actor, args.save)
            selected = [e for e in selected if e['id'] not in seen]
        limit = args.limit if args.limit is not None else (0 if args.json else 50)
        if limit:
            selected = selected[-limit:]
        print(encode(dict(state, events=selected)) if args.json else render(
            state, selected=selected, actor=args.actor if args.inbox or args.peer else None), end='')
    elif args.command == 'ack':
        print(encode(client.acknowledge(address(args.actor), address(args.save), args.event_id)), end='')
    elif args.command == 'pending':
        print(encode([p.stem for p in sorted(client.outbox.glob('*.json'))]), end='')
    elif args.command in ('retry', 'discard'):
        valid_id(args.event_id)
        if args.actor is not None:
            address(args.actor)
        path = client.outbox / (args.event_id + '.json')
        try:
            saved = json.loads(path.read_text())
        except FileNotFoundError:
            saved = None
        if saved is not None:
            validate_intent(saved)
            if args.actor is not None and saved['actor'] != args.actor:
                raise ValidationError('Pending messages must be retried or discarded by their sender.')
            if participants(saved) and args.actor != saved['actor']:
                raise ValidationError('A private pending operation requires its sender Worker ID.')
        if args.command == 'discard':
            path.unlink(missing_ok=True)
            print('Local pending message discarded.')
        else:
            found = client.publish(saved) if saved is not None else next(
                (e for e in client.read()['events'] if e['id'] == args.event_id), None)
            if found is None:
                raise BoardError('No pending or remote message with that ID.')
            if not visible(found, args.actor):
                raise ValidationError('A private replay requires a participant Worker ID.')
            print(encode(found), end='')
    else:
        body = {'text': Path(args.text_file).read_text() if args.text_file else args.text}
        for key in ('thread', 'reply_to'):
            if getattr(args, key) is not None:
                body[key] = getattr(args, key)
        if args.asset_json:
            body['asset'] = json.loads(Path(args.asset_json).read_text())
        for key in ('save', 'to'):
            if getattr(args, key) is not None:
                body[key] = getattr(args, key)
        mentions = set(args.mention)
        mentions.update(re.findall(r'(?<![A-Za-z0-9_])@([A-Za-z0-9][A-Za-z0-9._-]{0,63})', body['text']))
        if mentions:
            body['mentions'] = sorted(mentions)
        print(encode(client.publish(make_intent(args.actor, args.kind, body, args.event_id))), end='')


if __name__ == '__main__':
    try:
        main()
    except (BoardError, OSError, ValueError, KeyError, TypeError) as exc:
        print('ERROR: ' + str(exc), file=__import__('sys').stderr)
        raise SystemExit(2)
