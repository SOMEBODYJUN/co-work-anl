"""One new execution per four unbound primary codes; waterfill is reused.

Run only after inspect_inputs.py succeeded. No author generator, optimizer,
repository solver, Git, network, identity, or public-board operation is called.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/independent-security-and-waterfill-audit-primary'
MIRROR = E / 'replay-tree'
OUT = E / 'runs'
OUT.mkdir(exist_ok=True)
assert json.loads((E / 'input-structure-and-readiness.json').read_text())['status'].startswith('passed')
probe = subprocess.run([sys.executable, '-I', '-B', '-c',
    'import json,sys;print(json.dumps({"version":sys.version,"optimize":sys.flags.optimize,"isolated":sys.flags.isolated}))'],
    capture_output=True, text=True, check=True)
runtime = json.loads(probe.stdout)
assert runtime['optimize'] == 0 and runtime['isolated'] == 1
sources = {x['id']: x for x in json.loads((E / 'source-manifest.json').read_text())}
deps = {x['id']: x for x in json.loads((E / 'dependency-manifest.json').read_text())}
jobs = [
    ('individual-34', '263d8b8cde0651ffc00a', ['1384d853217106a4f948'],
     ['--output-dir', str(OUT / 'individual-34-files')]),
    ('lift-flow', '0494c0e5b61617175486', [], []),
    ('selected-budgets', 'cb88477459c73d47fafe',
     ['c00b6ac7a4b315507e33', 'bc3a57d93d51b69d628c', '760c140a12ae10efa5c4',
      '464b5462eddc2fab21e2', '480334724777cf80164f'], []),
    ('selected-cones', 'c0b20181754a4455d3cb', ['7a48fb9d35ad4f79eb56'], []),
]
records = []
for name, source_id, input_ids, extra in jobs:
    source = sources[source_id]
    script = MIRROR / source['path']
    assert hashlib.sha256(script.read_bytes()).hexdigest() == source['sha256']
    for ident in input_ids:
        row = deps[ident]
        assert hashlib.sha256((MIRROR / row['path']).read_bytes()).hexdigest() == row['sha256']
    record_path = OUT / (name + '-run.json')
    assert not record_path.exists(), 'Do not repeat a completed source run'
    stdout, stderr = OUT / (name + '.stdout.txt'), OUT / (name + '.stderr.txt')
    argv = [sys.executable, '-I', '-B', str(script)] + extra
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    with stdout.open('x') as fo, stderr.open('x') as fe:
        result = subprocess.run(argv, cwd=MIRROR, stdout=fo, stderr=fe, timeout=180)
    record = {'name': name, 'source_id': source_id, 'source_sha256': source['sha256'],
              'actual_inputs': [{k: deps[i][k] for k in ['id', 'path', 'size', 'sha256']} for i in input_ids],
              'command': argv, 'cwd': str(MIRROR), 'runtime': runtime, 'started_utc': started,
              'elapsed_seconds': round(time.monotonic() - clock, 3), 'exit_code': result.returncode,
              'source_execution_count_this_batch': 1, 'stdout_path': str(stdout.relative_to(ROOT)),
              'stderr_path': str(stderr.relative_to(ROOT)),
              'reason': 'Prior reports and current exact source have no saved shared code-SHA run binding; this one new run binds canonical real inputs, preserving historical reports.',
              'scope': 'exact frozen inputs/embedded finite fixtures only; no universal six-player half claim'}
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({'name': name, 'exit_code': result.returncode,
                      'elapsed_seconds': record['elapsed_seconds']}, ensure_ascii=False), flush=True)
    assert result.returncode == 0, name
(OUT / 'new-run-summary.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
