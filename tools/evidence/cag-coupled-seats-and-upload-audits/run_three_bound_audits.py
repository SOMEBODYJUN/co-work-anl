"""Exactly one new original CLI run each for three previously unbound codes.

Random and uploaded successful same-SHA records are reused, never rerun here.
All output is confined to this new external evidence tree.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/cag-coupled-seats-and-upload-audits'
M = E / 'replay-tree'
O = E / 'runs'
O.mkdir(exist_ok=True)
assert json.loads((E / 'input-structure-and-run-readiness.json').read_text())['status'].startswith('passed')
rows = json.loads((E / 'source-manifest.json').read_text()) + json.loads((E / 'dependency-manifest.json').read_text())
byid = {r['id']: r for r in rows}
probe = subprocess.run([sys.executable, '-I', '-B', '-c',
    'import sys,json;print(json.dumps({"version":sys.version,"optimize":sys.flags.optimize,"isolated":sys.flags.isolated}))'],
    check=True, capture_output=True, text=True)
runtime = json.loads(probe.stdout)
assert runtime['optimize'] == 0 and runtime['isolated'] == 1
jobs = [
    ('prefix-seats', '311146e332d3bac3e525', ['6d08e55bce1a5336932c'],
     ['--output', str(O / 'prefix-seats-report.json')]),
    ('priced-projection', 'b7956ea98f712cf7917f',
     ['a3926198d09da05d88b8', 'e34d11916a2c223f010d', '999293c4e866618a72f6',
      '14e0922138e43b337600', '52369ae591b07d52c7df'], []),
    ('nine-plus-arithmetic', '06319e5bab2a4043ed15', [],
     ['--output', str(O / 'nine-plus-arithmetic-report.json')]),
]
records = []
for name, ident, dependency_ids, extra in jobs:
    assert not (O / (name + '-run.json')).exists(), 'No repeat of completed source run'
    for current in [ident] + dependency_ids:
        r = byid[current]
        assert hashlib.sha256((M / r['path']).read_bytes()).hexdigest() == r['sha256']
    if '--output' in extra:
        assert not Path(extra[1]).exists()
    command = [sys.executable, '-I', '-B', str(M / byid[ident]['path'])] + extra
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    process = subprocess.run(command, cwd=M, capture_output=True, text=True, timeout=180)
    stdout, stderr = O / (name + '.stdout.txt'), O / (name + '.stderr.txt')
    with stdout.open('x') as f:
        f.write(process.stdout)
    with stderr.open('x') as f:
        f.write(process.stderr)
    record = {'source_id': ident, 'source_sha256': byid[ident]['sha256'], 'name': name,
        'dependency_bindings': [{k: byid[d][k] for k in ['id', 'path', 'size', 'sha256']} for d in dependency_ids],
        'command': command, 'cwd': str(M), 'runtime': runtime, 'started_utc': started,
        'elapsed_seconds': round(time.monotonic() - clock, 3), 'exit_code': process.returncode,
        'source_CLI_invocations_this_batch': 1, 'stdout_bytes': len(process.stdout.encode()),
        'stderr_bytes': len(process.stderr.encode()),
        'reason': 'Saved old report does not bind this auditor code SHA; one canonical run now supplies explicit code/input binding.',
        'scope': 'frozen concrete input or embedded finite parameter domain only; no general six-player half certification'}
    (O / (name + '-run.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({k: record[k] for k in ['name', 'exit_code', 'elapsed_seconds', 'stdout_bytes']}), flush=True)
    assert process.returncode == 0 and process.stdout, name
    json.loads(process.stdout)
(O / 'new-run-summary.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
