"""Actual local Git races and complete synthetic audit submission.

All source material and reviewer records in this test are synthetic. Nothing
here can certify an uploaded manuscript or write to the production remote.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import itertools
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUNS = {}
sys.path.insert(0, str(ROOT))
from tools.notes_queue import current_batch, transition
from types import SimpleNamespace


def execute(cwd, command, ok=True):
    r = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=120)
    if (r.returncode == 0) != ok: raise AssertionError((command, r.returncode, r.stdout, r.stderr))
    return r


def git(cwd, *args): return execute(cwd, ['git', *args])


def work(cwd, *args, ok=True):
    if cwd in RUNS:
        args = tuple(RUNS[cwd] if a == 'R' else 'work/' + RUNS[cwd] if a == 'work/R'
                     else a.replace('work/R/', 'work/' + RUNS[cwd] + '/') for a in args)
    r = execute(cwd, [sys.executable, str(cwd / 'work.py'), *args], ok=ok)
    return json.loads(r.stdout) if ok else r


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def exercise(base):
    seed = base / 'seed'; seed.mkdir()
    for name in ['work.py', '.notes-project.json', '.gitignore', '.gitattributes']:
        shutil.copy2(ROOT / name, seed / name)
    for name in ['.agents', 'tools']:
        shutil.copytree(ROOT / name, seed / name, ignore=shutil.ignore_patterns('__pycache__'))
    script = seed / '.agents/skills/math-notes-evidence-audit/scripts/selftest.py'
    fixture = base / 'fixture'
    execute(base, [sys.executable, str(script), '--emit-fixture', str(fixture)])
    source = seed / 'input/pdf/synthetic.pdf'; source.parent.mkdir(parents=True)
    shutil.copy2(fixture / 'project/source.pdf', source)
    old = seed / 'input/previous-notes/synthetic.md'; old.parent.mkdir(parents=True)
    shutil.copy2(fixture / 'project/old.md', old)
    for name in ['work', 'output']: (seed / name).mkdir()
    for n in range(1, 5):
        write(seed / 'tasks' / f'N{n}.json', {'note_id': f'N{n}', 'order': n, 'batch': 1 if n < 4 else 2,
            'status': 'pending', 'pages': 2, 'owner': None, 'run': None, 'workspace': None, 'history': [],
            'source_pdfs': [{'path': 'input/pdf/synthetic.pdf', 'sha256': sha(source)}],
            'previous_markdowns': [{'path': 'input/previous-notes/synthetic.md', 'sha256': sha(old)}]})
    remote = base / 'origin.git'
    git(base, 'init', '--bare', '-q', str(remote))
    git(seed, 'init', '-q', '-b', 'work/notes')
    git(seed, 'config', 'user.name', 'Synthetic Queue Test')
    git(seed, 'config', 'user.email', 'test@example.invalid')
    git(seed, 'add', '.'); git(seed, 'commit', '-qm', 'Synthetic queue fixture')
    git(seed, 'remote', 'add', 'origin', str(remote)); git(seed, 'push', '-q', '-u', 'origin', 'work/notes')
    clones = [base / ('boss' + str(n)) for n in range(3)]
    actors = []
    for n, clone in enumerate(clones):
        RUNS[clone] = 'R' + str(n)
        r = execute(base, [sys.executable, str(seed / 'work.py'), '--repo', str(clone), 'start',
                          '--actor', 'auto', '--remote', str(remote)])
        actor = json.loads(r.stdout)['actor']; actors.append(actor)
        assert actor.startswith('BossNotes-')
        assert work(clone, 'notes', 'init', 'R')['checkpoint']['owner'] == actor
    assert len(set(actors)) == 3
    a, b, c = clones
    # A new RUN/identity cannot overwrite another's state.
    work(a, 'notes', 'init', 'R', ok=False)
    assert work(a, 'start', '--actor', 'auto', '--remote', str(remote))['actor'] == actors[0]
    work(a, 'notes', 'claim', 'R', '--note', 'N4', ok=False)
    # Both requests race for the same single task. Exactly one wins.
    with ThreadPoolExecutor(2) as pool:
        races = list(pool.map(lambda clone: subprocess.run([sys.executable, 'work.py', 'notes', 'claim', RUNS[clone], '--note', 'N1'], cwd=clone,
                           capture_output=True, text=True, timeout=90), [a, b]))
    assert sorted(r.returncode for r in races) == [0, 2], [(r.stdout, r.stderr) for r in races]
    winner = a if races[0].returncode == 0 else b
    loser = b if winner == a else a
    collision = base / 'collision'
    execute(base, [sys.executable, str(seed / 'work.py'), '--repo', str(collision), 'start',
                   '--actor', 'auto', '--remote', str(remote)])
    rejected = work(collision, 'notes', 'init', RUNS[winner], ok=False)
    assert 'another Boss' in rejected.stderr
    assert not (collision / 'work' / RUNS[winner]).exists()
    task = work(winner, 'notes', 'claim', 'R', '--note', 'N1')['tasks'][0]
    assert len(task['history']) == 1  # repeat is idempotent
    journal = loser / 'work' / RUNS[loser] / 'draft.md'; journal.write_text('Uncommitted draft must survive claims.\n')
    assert len(work(loser, 'notes', 'claim', 'R', '--limit', '3')['workspaces']) == 2
    assert journal.read_text().startswith('Uncommitted draft')
    assert work(c, 'notes', 'claim', 'R')['status'] == 'waiting'
    work(loser, 'notes', 'release', 'R', '--note', 'N1', '--reason', 'Wrong owner', '--handoff', 'work/R/draft.md', ok=False)
    # Invalid/incomplete audit records must never close a task.
    target = winner / 'work' / RUNS[winner] / 'notes/N1'
    (target / 'ledger.json').write_text('{}')
    (target / 'manifest.json').write_text('{}')
    work(winner, 'notes', 'submit', 'R', '--note', 'N1', '--manifest', 'work/R/notes/N1/manifest.json',
         '--ledger', 'work/R/notes/N1/ledger.json', '--report', 'work/R/notes/N1/reports/final.json', ok=False)
    assert next(t for t in work(winner, 'notes', 'queue')['tasks'] if t['note_id'] == 'N1')['status'] == 'claimed'
    # Full valid synthetic evidence passes the real audit and preserves both output hashes.
    shutil.copytree(fixture / 'project', target, dirs_exist_ok=True)
    output = winner / 'output/N1'; output.mkdir(parents=True)
    shutil.copy2(target / 'transcription.md', output / 'source-transcript.md')
    shutil.copy2(target / 'study.md', output / 'study-notes.md')
    submitted = work(winner, 'notes', 'submit', 'R', '--note', 'N1', '--manifest', 'work/R/notes/N1/manifest.json',
                     '--ledger', 'work/R/notes/N1/ledger.json', '--report', 'work/R/notes/N1/reports/final.json')
    assert submitted['tasks'][0]['status'] == 'done'
    assert submitted['tasks'][0]['completion']['visual_reading_proven'] is False
    # Saving a handoff is required before a block/release changes shared state.
    handoff = loser / 'work' / RUNS[loser] / 'handoff.md'; handoff.write_text('Synthetic tool outage; stopped before reading. Next: restore tool.\n')
    args = ['R', '--note', 'N2', '--reason', 'Synthetic tool outage', '--handoff', 'work/R/handoff.md']
    work(loser, 'notes', 'block', *args, ok=False)
    work(loser, 'checkpoint', 'work/R', '-m', 'Save synthetic handoff')
    work(loser, 'notes', 'block', *args)
    work(loser, 'notes', 'resume', 'R', '--note', 'N2')
    work(loser, 'notes', 'block', *args)
    args[2] = 'N3'
    work(loser, 'notes', 'release', *args)
    work(c, 'notes', 'claim', 'R', '--note', 'N3')
    # A blocked note is incomplete; batching advances only after other work is settled.
    assert work(c, 'notes', 'queue')['current_batch'] == 1
    restored = base / 'restored'
    execute(base, [sys.executable, str(seed / 'work.py'), '--repo', str(restored), 'start',
                   '--actor', actors[0], '--remote', str(remote)])
    assert (restored / 'output/N1/study-notes.md').read_bytes() == (winner / 'output/N1/study-notes.md').read_bytes()
    assert next(t for t in work(restored, 'notes', 'queue')['tasks'] if t['note_id'] == 'N1')['status'] == 'done'
    # Enumerate small board states to check global capacity and fixed-batch claims.
    checked = 0
    for states in itertools.product(['pending', 'claimed', 'blocked', 'done'], repeat=4):
        tasks = [{'note_id': str(i), 'order': i, 'batch': 1 if i < 3 else 2, 'status': s,
                  'owner': 'peer', 'run': 'peer', 'history': []} for i, s in enumerate(states)]
        before = sum(s == 'claimed' for s in states)
        batch = current_batch(tasks)
        changed, _ = transition(tasks, SimpleNamespace(action='claim', run='R', note=None, limit=3), 'self', 'test')
        assert sum(t['status'] == 'claimed' for t in tasks) <= max(3, before)
        assert all(t['batch'] == batch for t in changed)
        checked += 1
    return {'same_note_race_single_winner': True, 'idempotent_claim': True, 'duplicate_run_owner_rejected': True,
            'max_three_active': True, 'fixed_batch_gating': True, 'dirty_draft_preserved': True,
            'handoff_must_be_published': True, 'owner_enforced': True, 'invalid_submission_rejected': True,
            'complete_synthetic_audit_submission': True, 'cold_restore': True,
            'small_board_states_enumerated': checked, 'test_remote': 'local-bare-only',
            'user_notes_recognized': 0}


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='notes-queue-test-', dir=ROOT.parent) as temp:
        print(json.dumps(exercise(Path(temp)), indent=2))
