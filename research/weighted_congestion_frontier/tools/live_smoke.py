#!/usr/bin/env python3
"""Explicit remote chat check using two independent clones and labeled test messages."""
import argparse
import concurrent.futures
import hashlib
from pathlib import Path
import threading
import uuid
from unittest.mock import patch

import board as b


def run(repo, branch='wcg/board'):
    client = b.Board(repo, branch)
    run_id = uuid.uuid4().hex
    actors = ['smoke-' + run_id[:12] + '-A', 'smoke-' + run_id[:12] + '-B']
    thread = '基础设施验收-' + run_id
    initial = client.read()
    commit = b.git(client.repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    path = 'research/weighted_congestion_frontier/tools/board.py'
    frozen = b.git(client.repo, 'show', commit + ':' + path).stdout
    asset = {'branch': 'main', 'commit': commit, 'path': path,
             'sha256': hashlib.sha256(frozen).hexdigest()}
    client.check_asset(asset)
    original_git = b.git
    barrier, lock, first_threads = threading.Barrier(2), threading.Lock(), set()

    def synchronized_git(cwd, *args, **kwargs):
        if args and args[0] == 'push':
            ident = threading.get_ident()
            with lock:
                first = ident not in first_threads
                first_threads.add(ident)
            if first:
                barrier.wait(timeout=30)
        return original_git(cwd, *args, **kwargs)

    with client.scratch() as directory:
        clones = [Path(directory) / 'A', Path(directory) / 'B']
        for clone in clones:
            b.git(directory, 'clone', '--quiet', '--no-checkout', '--single-branch',
                  '--branch', 'main', client.remote, str(clone))
        intents = [b.make_intent(actor, 'message', {
            'thread': thread, 'text': '基础设施测试发布端：同题的独立研究路线可以同时交流。'})
            for actor in actors]

        def send(index):
            return b.Board(clones[index], branch).publish(intents[index])

        with patch.object(b, 'git', synchronized_git):
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                messages = list(pool.map(send, range(2)))
        # Replay from a different clone proves receipts live on the remote board.
        replay = b.Board(clones[1], branch).publish(intents[0])
        if replay != messages[0]:
            raise AssertionError('Independent clone retry changed the original message.')
    reply = client.publish(b.make_intent(actors[0], 'message', {
        'thread': thread, 'reply_to': messages[1]['id'],
        'text': '基础设施测试：稍后回复另一条消息；发送后可以继续工作。'}))
    result = client.publish(b.make_intent(actors[0], 'result', {
        'thread': thread, 'asset': asset,
        'text': '基础设施验收：独立 clone 并发发言、自动重取重发、稳定 ID 去重、异步回复和冻结资产核验通过。'}))
    final = client.read()
    posted = {event['id']: event for event in final['events']}
    expected = [*messages, reply, result]
    if not all(posted.get(event['id']) == event for event in expected):
        raise AssertionError('Published message missing or changed on remote board.')
    if any(sum(e['id'] == event['id'] for e in final['events']) != 1 for event in expected):
        raise AssertionError('Replay duplicated a message in the remote stream.')
    return {'run_id': run_id, 'board_branch': branch,
            'messages': [event['id'] for event in messages],
            'reply_event': reply['id'], 'result_event': result['id'],
            'source_asset': asset, 'initial_events': len(initial['events']),
            'final_events': len(final['events']), 'verified': True,
            'scope': 'Infrastructure publishers only; no mathematical progress claimed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--branch', default='wcg/board')
    parser.add_argument('--live', action='store_true', required=True)
    args = parser.parse_args()
    print(b.encode(run(args.repo, args.branch)), end='')
