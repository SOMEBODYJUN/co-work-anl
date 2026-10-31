"""Exactly two new original CLIs; three old same-SHA successes are reused.

No Git, canonical NE solver, identity, network, or shared output is invoked.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/search-and-facility-site-primary'
M = E / 'replay-tree'
O = E / 'runs'
O.mkdir(exist_ok=True)
assert json.loads((E / 'input-structure-and-run-readiness.json').read_text())['status'].startswith('passed')
rows = json.loads((E / 'source-manifest.json').read_text()) + json.loads((E / 'dependency-manifest.json').read_text())
byid = {x['id']: x for x in rows}
probe = subprocess.run([sys.executable, '-I', '-B', '-c',
    'import sys,json;print(json.dumps({"version":sys.version,"optimize":sys.flags.optimize,"isolated":sys.flags.isolated}))'],
    capture_output=True, text=True, check=True)
runtime = json.loads(probe.stdout)
assert runtime['optimize'] == 0 and runtime['isolated'] == 1
jobs = [
    ('five-site-full', 'aba4ae48ffacdaea5c90', ['68753e23b4abb3316644', 'b1d86a5bf34773a9de22']),
    ('five-site-edges', '64fbe1e82a8a643c43b7', ['aba4ae48ffacdaea5c90', '68753e23b4abb3316644', 'b1d86a5bf34773a9de22']),
]
records = []
for name, ident, dependency_ids in jobs:
    output = O / (name + '-report.json')
    record_path = O / (name + '-run.json')
    assert not output.exists() and not record_path.exists(), 'Do not repeat an existing source run'
    for current in [ident] + dependency_ids:
        row = byid[current]
        assert hashlib.sha256((M / row['path']).read_bytes()).hexdigest() == row['sha256']
    command = [sys.executable, '-I', '-B', str(M / byid[ident]['path']), '--output', str(output)]
    started, clock = datetime.now(timezone.utc).isoformat(), time.monotonic()
    process = subprocess.run(command, cwd=M, capture_output=True, text=True, timeout=180)
    with (O / (name + '.stdout.txt')).open('x') as f:
        f.write(process.stdout)
    with (O / (name + '.stderr.txt')).open('x') as f:
        f.write(process.stderr)
    record = {'name': name, 'source_id': ident, 'source_sha256': byid[ident]['sha256'],
        'dependency_bindings': [{k: byid[d][k] for k in ['id', 'path', 'size', 'sha256']} for d in dependency_ids],
        'command': command, 'cwd': str(M), 'runtime': runtime, 'started_utc': started,
        'elapsed_seconds': round(time.monotonic() - clock, 3), 'exit_code': process.returncode,
        'source_original_CLI_invocations_this_batch': 1,
        'reason': 'Old default/edge reports have no recorded same auditor-code SHA run binding; narrow prior 3-case replay does not cover these complete CLI domains.',
        'scope': 'one complete original finite default or edge domain, not universal hardness proof',
        'entry_identity': 'direct __main__ original CLI; edge run_path loads sibling definitions under <run_path>, not sibling main',
        'stdout_bytes': len(process.stdout.encode()), 'stderr_bytes': len(process.stderr.encode())}
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({k: record[k] for k in ['name', 'exit_code', 'elapsed_seconds', 'stdout_bytes']}), flush=True)
    assert process.returncode == 0 and output.is_file() and process.stdout
    assert json.loads(process.stdout) == json.loads(output.read_text())
(O / 'new-run-summary.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
