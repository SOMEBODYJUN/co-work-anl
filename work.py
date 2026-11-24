#!/usr/bin/env python3
"""Restore the notes branch, retain source fingerprints, and save scoped work."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import uuid

REMOTE = 'https://github.com/SOMEBODYJUN/co-work-anl.git'
BRANCH = 'work/notes'
IDENT = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}')
SECRET = re.compile(rb'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----')
ROUTING = {'GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE',
           'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_SHALLOW_FILE',
           'GIT_IMPLICIT_WORK_TREE', 'GIT_GRAFT_FILE', 'GIT_PREFIX', 'GIT_INTERNAL_SUPER_PREFIX'}


def token(path):
    values = set(re.findall(rb'(?:github_pat_|ghp_)[A-Za-z0-9_]{12,}', Path(path).read_bytes()))
    if len(values) != 1:
        raise ValueError('Credential file must contain exactly one GitHub token')
    return values.pop().decode()


@contextmanager
def environment(repo, supplied=None):
    env = {k: v for k, v in os.environ.items() if k not in ROUTING}
    env['GIT_TERMINAL_PROMPT'] = '0'
    path = supplied or (config(repo, 'wcg.tokenFile') if (repo / '.git').exists() else '')
    if not path:
        yield env
        return
    path = Path(path).expanduser().resolve()
    if path.is_relative_to(repo):
        raise ValueError('Keep credentials outside the repository')
    token(path)
    with tempfile.TemporaryDirectory(prefix='.notes-auth-', dir=repo.parent) as directory:
        helper = Path(directory) / 'askpass'
        helper.write_text('#!/bin/sh\nexec ' + shlex.join([sys.executable, str(Path(__file__).resolve())]) + ' "$@"\n')
        helper.chmod(0o700)
        env.update(GIT_ASKPASS=str(helper), NOTES_ASKPASS='1', WCG_CHECKPOINT_TOKEN_FILE=str(path))
        count = int(env.get('GIT_CONFIG_COUNT', '0'))
        env.update(GIT_CONFIG_COUNT=str(count + 1))
        env[f'GIT_CONFIG_KEY_{count}'] = 'credential.helper'
        env[f'GIT_CONFIG_VALUE_{count}'] = ''
        yield env


def git(repo, *args, env=None, check=True):
    clean = {k: v for k, v in os.environ.items() if k not in ROUTING}
    clean['GIT_TERMINAL_PROMPT'] = '0'
    result = subprocess.run(['git', *args], cwd=repo, env=env or clean,
                            capture_output=True, timeout=600)
    if check and result.returncode:
        raise ValueError(SECRET.sub(b'[REDACTED]', result.stderr).decode(errors='replace').strip()[:1500])
    return result


def config(repo, key):
    return git(repo, 'config', '--local', '--get', key, check=False).stdout.decode().strip()


def checked_repo(path):
    repo = Path(path).resolve()
    if not (repo / '.git').exists() or Path(git(repo, 'rev-parse', '--show-toplevel').stdout.decode().strip()) != repo:
        raise ValueError('Run start in an independent notes clone first')
    if git(repo, 'branch', '--show-current').stdout.decode().strip() != BRANCH:
        raise ValueError('This entry point requires the work/notes branch')
    if not (repo / '.notes-project.json').is_file():
        raise ValueError('This checkout is not a notes project')
    return repo


def sync(repo, env):
    cache = repo / '.git/wcg-checkpoint'
    cache.mkdir(exist_ok=True)
    with (cache / 'writer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for name in ['MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply']:
            if (repo / '.git' / name).exists():
                raise ValueError('Finish the pending Git operation before sync')
        if git(repo, 'ls-files', '-u').stdout:
            raise ValueError('Resolve existing file conflicts before sync')
        git(repo, 'fetch', '--quiet', '--no-tags', 'origin', '+refs/heads/' + BRANCH + ':refs/remotes/origin/' + BRANCH, env=env)
        tip = git(repo, 'rev-parse', 'origin/' + BRANCH).stdout.decode().strip()
        if not git(repo, 'merge-base', '--is-ancestor', tip, 'HEAD', check=False).returncode:
            return {'status': 'synced', 'remote_tip': tip, 'preserved_work': True}
        stash = None
        if git(repo, 'status', '--porcelain').stdout:
            git(repo, 'stash', 'push', '--quiet', '--include-untracked', '-m', 'notes sync ' + uuid.uuid4().hex)
            stash = git(repo, 'rev-parse', 'refs/stash').stdout.decode().strip()
        merged = git(repo, '-c', 'user.name=Notes Worker', '-c', 'user.email=notes@users.noreply.github.com',
                     'merge', '--no-edit', tip, check=False)
        if merged.returncode:
            git(repo, 'merge', '--abort', check=False)
        if stash:
            restored = git(repo, 'stash', 'apply', '--index', stash, check=False)
            if restored.returncode:
                raise ValueError('Local work retained in stash ' + stash + '; resolve restoration conflicts')
            if git(repo, 'rev-parse', 'refs/stash').stdout.decode().strip() == stash:
                git(repo, 'stash', 'drop', '--quiet', 'stash@{0}')
        if merged.returncode:
            raise ValueError('Remote merge needs resolution; original local work has been restored')
        return {'status': 'synced', 'remote_tip': tip, 'preserved_work': True}


def finish_start(payload):
    repo = checked_repo(payload['repo'])
    if repo != Path(__file__).resolve().parent:
        raise ValueError('Start handoff must target the checked-out work.py')
    actor = payload['actor']
    if not IDENT.fullmatch(actor):
        raise ValueError('Use a simple explicit Boss ID')
    if config(repo, 'wcg.actor') not in {'', actor}:
        raise ValueError('This clone belongs to another Boss; use an independent directory')
    if git(repo, 'remote', 'get-url', 'origin').stdout.decode().strip() != payload['remote']:
        raise ValueError('Remote differs from the requested repository')
    with environment(repo, payload.get('token_file')) as env:
        before = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        result = sync(repo, env)
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != before:
            return subprocess.call([sys.executable, str(repo / 'work.py'), '_notes-start-v1'],
                                   env={**env, 'NOTES_START_V1': json.dumps(payload)})
    for key, value in [('wcg.actor', actor), ('wcg.branch', BRANCH)]:
        git(repo, 'config', '--local', key, value)
    if payload.get('token_file'):
        git(repo, 'config', '--local', 'wcg.tokenFile', str(Path(payload['token_file']).expanduser().resolve()))
    print(json.dumps(dict(result, repo=str(repo), branch=BRANCH, actor=actor,
                          entry='START-HERE.md', prompt='prompts/launch-prompt.md',
                          status='notes-runtime-ready', input_count=len(inputs(repo))), ensure_ascii=False))
    return 0


def start(args):
    repo = Path(args.repo).resolve()
    if args.branch != BRANCH:
        raise ValueError('Use work/notes for note work')
    if SECRET.search(args.remote.encode()) or re.search(r'https?://[^/]*@', args.remote):
        raise ValueError('Use a credential-free remote URL')
    if not IDENT.fullmatch(args.actor):
        raise ValueError('Use a simple explicit Boss ID')
    repo.parent.mkdir(parents=True, exist_ok=True)
    if not repo.exists():
        with environment(repo, args.token_file) as env:
            with tempfile.TemporaryDirectory(prefix='.notes-clone-', dir=repo.parent) as temp:
                clone = Path(temp) / 'clone'
                git(repo.parent, 'clone', '--quiet', '--depth', '1', '--single-branch',
                    '--branch', BRANCH, args.remote, str(clone), env=env)
                if not (clone / '.notes-project.json').is_file():
                    raise ValueError('Remote branch is not a notes project')
                clone.rename(repo)
    else:
        checked_repo(repo)
    payload = {'repo': str(repo), 'actor': args.actor, 'remote': args.remote,
               'token_file': str(Path(args.token_file).expanduser().resolve()) if args.token_file else None}
    with environment(repo, args.token_file) as env:
        return subprocess.call([sys.executable, str(repo / 'work.py'), '_notes-start-v1'],
                               env={**env, 'NOTES_START_V1': json.dumps(payload)})


def inputs(repo):
    return [{'path': p.relative_to(repo).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted((repo / 'input').rglob('*')) if p.is_file() and p.name != '.gitkeep' and not p.is_symlink()]


def notes(repo, args):
    if not IDENT.fullmatch(args.run):
        raise ValueError('Use a simple RUN ID')
    path = repo / 'work' / args.run
    actor = config(repo, 'wcg.actor')
    if not actor:
        raise ValueError('Run start with your Boss ID first')
    if args.action == 'init':
        path.mkdir(parents=True, exist_ok=False)
        state = {'schema': 1, 'run': args.run, 'owner': actor, 'status': 'awaiting_inputs',
                 'active_notes': [], 'completed_notes': [], 'blocked_notes': [],
                 'next_action': '核实原稿与旧稿的课次和页段；原图独立初读后才比较旧稿。'}
        (path / 'checkpoint.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        (path / 'input-map.json').write_text(json.dumps({'schema': 1, 'expected_notes': None,
            'pairing_status': 'not_started', 'source_inventory': inputs(repo), 'notes': []}, ensure_ascii=False, indent=2) + '\n')
    state = json.loads((path / 'checkpoint.json').read_text())
    mapping = json.loads((path / 'input-map.json').read_text())
    expected = {r['path']: r['sha256'] for r in mapping['source_inventory']}
    actual = {r['path']: r['sha256'] for r in inputs(repo)}
    return {'checkpoint': state, 'current_actor': actor, 'input_count': len(actual),
            'changed_sources': sorted(p for p in expected if expected[p] != actual.get(p)),
            'new_sources': sorted(actual.keys() - expected.keys()),
            'workspace': str(path), 'completion_certified': False}


def main():
    if (os.environ.get('NOTES_ASKPASS') == '1' and len(sys.argv) == 2
            and sys.argv[1].startswith(('Username', 'Password'))):
        if sys.argv[1].startswith('Username'):
            print('x-access-token')
        elif sys.argv[1].startswith('Password'):
            print(token(os.environ['WCG_CHECKPOINT_TOKEN_FILE']))
        return 0
    if sys.argv[1:] == ['_notes-start-v1']:
        return finish_start(json.loads(os.environ.pop('NOTES_START_V1')))
    default = Path(__file__).resolve().parent
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument('--repo', default=str(default if (default / '.git').exists() else Path.cwd() / 'co-work-notes'))
    selected, remaining = pre.parse_known_args()
    if remaining and remaining[0] == 'checkpoint':
        repo = checked_repo(selected.repo)
        return subprocess.call([sys.executable, str(repo / 'tools/checkpoint.py'), '--repo', str(repo), *remaining[1:]])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default=str(default if (default / '.git').exists() else Path.cwd() / 'co-work-notes'))
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('start')
    p.add_argument('--actor', required=True); p.add_argument('--token-file')
    p.add_argument('--remote', default=REMOTE); p.add_argument('--branch', default=BRANCH)
    sub.add_parser('sync'); sub.add_parser('doctor')
    p = sub.add_parser('notes'); q = p.add_subparsers(dest='action', required=True)
    for action in ['init', 'status']:
        q.add_parser(action).add_argument('run')
    sub.add_parser('checkpoint', help='Save explicit paths; use checkpoint --help for options', add_help=False).add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command == 'start':
        return start(args)
    repo = checked_repo(args.repo)
    if args.command == 'checkpoint':
        return subprocess.call([sys.executable, str(repo / 'tools/checkpoint.py'), '--repo', str(repo), *args.args])
    if args.command == 'sync':
        with environment(repo) as env:
            result = sync(repo, env)
    elif args.command == 'doctor':
        versions = {}
        for name in ['PyMuPDF', 'Pillow', 'jsonschema']:
            try: versions[name] = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError: versions[name] = None
        result = {'branch': BRANCH, 'actor': config(repo, 'wcg.actor'), 'dependencies': versions,
                  'visual_tool': 'must-be-checked-in-the-current-conversation',
                  'subagents': 'must-be-checked-in-the-current-conversation'}
    else:
        result = notes(repo, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as exc:
        print('ERROR: ' + SECRET.sub(b'[REDACTED]', str(exc).encode()).decode(), file=sys.stderr)
        raise SystemExit(2)
