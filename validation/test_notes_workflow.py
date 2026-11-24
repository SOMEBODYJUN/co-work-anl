"""Local real-Git exercise; synthetic notes never enter the production branch."""
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
import atexit
import tempfile
BASE = Path(tempfile.mkdtemp(prefix='notes-workflow-', dir=ROOT.parent))
atexit.register(shutil.rmtree, BASE, ignore_errors=True)
SEED = BASE / 'seed'
SEED.mkdir()
for name in ['work.py', '.notes-project.json', '.gitattributes', '.gitignore']:
    shutil.copy2(ROOT / name, SEED / name)
shutil.copytree(ROOT / '.agents', SEED / '.agents', ignore=shutil.ignore_patterns('__pycache__'))
(SEED / 'tools').mkdir()
shutil.copy2(ROOT / 'tools/checkpoint.py', SEED / 'tools/checkpoint.py')
shutil.copy2(ROOT / 'tools/notes_queue.py', SEED / 'tools/notes_queue.py')
(SEED / 'README.md').write_text('Synthetic persistence fixture.\n')
for name in ['input/pdf', 'input/previous-notes', 'input/teacher', 'work', 'output']:
    (SEED / name).mkdir(parents=True, exist_ok=True)
    (SEED / name / '.gitkeep').touch()
REMOTE = BASE / 'origin.git'


def run(cwd, args, success=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=90)
    if (r.returncode == 0) != success:
        raise AssertionError((args, r.returncode, r.stdout, r.stderr))
    return r


def git(cwd, *args):
    return run(cwd, ['git', *args])


def work(cwd, *args, success=True):
    r = run(cwd, [sys.executable, str(cwd / 'work.py'), *args], success=success)
    return json.loads(r.stdout) if success else r


git(BASE, 'init', '--bare', '-q', str(REMOTE))
git(SEED, 'init', '-q', '-b', 'work/notes')
git(SEED, 'config', 'user.name', 'Synthetic Workflow Test')
git(SEED, 'config', 'user.email', 'test@example.invalid')
git(SEED, 'add', '.')
git(SEED, 'commit', '-qm', 'Synthetic local template seed')
git(SEED, 'remote', 'add', 'origin', str(REMOTE))
git(SEED, 'push', '-q', '-u', 'origin', 'work/notes')

first = BASE / 'cold'
credential = BASE / 'auth.txt'
credential.write_text('ghp_' + 'A' * 32)
r = run(BASE, [sys.executable, str(SEED / 'work.py'), '--repo', str(first), 'start',
               '--actor', 'BossTest', '--remote', str(REMOTE), '--token-file', str(credential)])
assert json.loads(r.stdout)['status'] == 'notes-runtime-ready'
assert json.loads(r.stdout)['actor'] == 'BossTest'
assert work(first, 'doctor')['branch'] == 'work/notes'
run(first, [sys.executable, 'work.py', 'checkpoint', '--help'])

import fitz
doc = fitz.open(); page = doc.new_page(width=240, height=160)
page.insert_text((18, 40), 'Synthetic source: x + 1 = 2.')
doc.save(first / 'input/pdf/synthetic.pdf'); doc.close()
(first / 'input/previous-notes/synthetic.md').write_text('Synthetic old note.\n')
opened = work(first, 'notes', 'init', 'fixture')
assert opened['input_count'] == 2 and not opened['changed_sources']
run(first, [sys.executable, '.agents/skills/math-notes-evidence-audit/scripts/prepare_pdf.py',
            'input/pdf/synthetic.pdf', '--out', 'work/fixture/prepared'])
(first / 'output/fixture').mkdir()
(first / 'output/fixture/source-transcript.md').write_text('Synthetic transcription for persistence testing only.\n')
(first / 'output/fixture/study-notes.md').write_text('Synthetic study note; not independently reviewed.\n')
paths = ['input', 'work/fixture', 'output/fixture']
saved = work(first, 'checkpoint', *paths, '-m', 'Synthetic local workflow checkpoint', '--local-only')
assert saved['status'] == 'local-only'
pushed = work(first, 'checkpoint', *paths, '-m', 'Synthetic local workflow checkpoint')
assert pushed['status'] == 'pushed'

second = BASE / 'restored'
r = run(BASE, [sys.executable, str(SEED / 'work.py'), '--repo', str(second), 'start',
               '--actor', 'BossOther', '--remote', str(REMOTE)])
assert json.loads(r.stdout)['status'] == 'notes-runtime-ready'
state = work(second, 'notes', 'status', 'fixture')
assert not state['changed_sources'] and state['input_count'] == 2
for path in ['work/fixture/checkpoint.json', 'work/fixture/input-map.json',
             'output/fixture/study-notes.md', 'work/fixture/prepared/manifest.json',
             'work/fixture/prepared/source.pdf']:
    assert (first / path).read_bytes() == (second / path).read_bytes(), path

# Real dirty-work synchronization against a concurrently advanced bare remote.
journal = first / 'work/fixture/journal.md'
journal.write_text('Uncommitted synthetic continuation.\n')
with (second / 'README.md').open('a') as stream:
    stream.write('\nSynthetic peer edit for local sync validation.\n')
assert work(second, 'checkpoint', 'README.md', '-m', 'Synthetic peer edit')['status'] == 'pushed'
assert work(first, 'sync')['status'] == 'synced'
assert journal.read_text() == 'Uncommitted synthetic continuation.\n'
assert 'Synthetic peer edit' in (first / 'README.md').read_text()

# Refusals retain existing source data and workspaces.
snapshot = (first / 'work/fixture/checkpoint.json').read_bytes()
work(first, 'notes', 'init', 'fixture', success=False)
assert (first / 'work/fixture/checkpoint.json').read_bytes() == snapshot
work(first, 'start', '--actor', 'BossWrong', '--remote', str(REMOTE), success=False)
with (first / 'input/previous-notes/synthetic.md').open('a') as stream:
    stream.write('Changed source, deliberately detectable.\n')
assert work(first, 'notes', 'status', 'fixture')['changed_sources'] == ['input/previous-notes/synthetic.md']

for path in ['input/pdf/synthetic.pdf', 'input/previous-notes/synthetic.md',
             'work/fixture/checkpoint.json', 'output/fixture/study-notes.md',
             'work/fixture/prepared/pages/p0001.png']:
    assert run(first, ['git', 'check-ignore', path], success=False).returncode == 1, path

result = {'cold_start_with_external_credential': True, 'pdf_preparation': True, 'scoped_local_checkpoint': True,
          'push_and_remote_confirmation': True, 'fresh_clone_restore': True,
          'dirty_sync_preserves_draft': True, 'existing_run_not_overwritten': True,
          'wrong_owner_rejected': True, 'source_change_detected': True,
          'source_output_checkpoint_and_image_evidence_trackable': True,
          'test_remote': 'local-bare-only', 'user_notes_reviewed': 0}
print(json.dumps(result, indent=2))
