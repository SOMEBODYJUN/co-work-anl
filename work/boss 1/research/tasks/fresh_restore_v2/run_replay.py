"""Execute the incremental replay from the new clone root using a verified venv."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

SHA = '7394ed770c1b47d134bc51e64aa3bb721dc157e0'
WORK = Path('work/boss 1')
OUT = WORK / 'research/tasks/fresh_restore_v2'
OLD = WORK / 'research/tasks/fresh_restore'
LOCAL = Path('.fresh-v2')
LOGS = LOCAL / 'logs'
PYTHON = os.path.relpath(sys.executable, Path.cwd())
MODELS = WORK / 'research/models'
JST = MODELS / 'jst_portable_20261127'
HOUSE = WORK / 'research/tasks/household_engine'
FORMAL = WORK / 'formal'
LEDGER = WORK / 'compute/ledger.json'
COMMANDS = []
ARTIFACTS = []
EXCLUDED = {'executed_at', 'elapsed_seconds', 'wall_seconds'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def frozen(path):
    return subprocess.check_output(['git', 'show', SHA + ':' + str(path)])


def run(name, args, expected=0):
    argv = [str(arg) for arg in args]
    started = datetime.now(timezone.utc).isoformat()
    t = time.monotonic()
    r = subprocess.run(argv, capture_output=True)
    wall = time.monotonic() - t
    for stream, value in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (LOGS / (name + '.' + stream)).write_bytes(value)
    COMMANDS.append({'label': name, 'argv_from_clone_root': argv, 'started_utc': started,
                    'wall_seconds': wall, 'expected_exit': expected, 'exit_code': r.returncode,
                    'stdout_sha256': digest(r.stdout), 'stderr_sha256': digest(r.stderr)})
    write(LOCAL / 'commands.json', COMMANDS)
    if r.returncode != expected:
        raise RuntimeError(f'{name}: expected {expected}, observed {r.returncode}; see captured stderr')
    print(f'{name}: {r.returncode} ({wall:.3f}s)', flush=True)
    return r.stdout


def track(name, args, inputs, outputs):
    """outputs maps a rebuilt location to its comparable tracked location."""
    old = {p: p.stat().st_mtime_ns if p.exists() else None for p in outputs}
    source_hashes = {}
    for p in inputs:
        assert p.resolve().is_relative_to(Path.cwd().resolve()) and p.is_file(), p
        a, b = digest(p.read_bytes()), digest(frozen(p))
        assert a == b, p
        source_hashes[str(p)] = a
    run(name, args)
    result = {}
    for p, ref in outputs.items():
        a, b = digest(p.read_bytes()), digest(frozen(ref))
        observed = p.stat().st_mtime_ns
        result[str(p)] = {'frozen_reference': str(ref), 'frozen_sha256': b,
                          'rebuilt_sha256': a, 'byte_equal': a == b,
                          'before_mtime_ns': old[p], 'after_mtime_ns': observed,
                          'rewritten_or_created': old[p] != observed}
        assert a == b and old[p] != observed, p
    ARTIFACTS.append({'program': name, 'input_code_sha256': source_hashes, 'output': result})
    write(LOCAL / 'regenerated.json', ARTIFACTS)


def grouped(name, runtime, source, inputs, outputs):
    code = HOUSE / source
    track(name, [runtime, code], [code, *(HOUSE / s for s in inputs)],
          {HOUSE / k: HOUSE / k for k in outputs})


def main():
    root = Path.cwd().resolve()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == SHA
    assert subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() == 'work/cn-crisis'
    assert subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip() == 'https://github.com/SOMEBODYJUN/co-work-anl.git'
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOCAL / 'tmp').mkdir(parents=True, exist_ok=True)
    os.environ['TMPDIR'] = str(root / LOCAL / 'tmp')
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    assert LEDGER.read_bytes() == frozen(LEDGER)
    assert len(read(LEDGER)['runs']) == 12
    cli = [PYTHON, 'work.py', '--workspace', WORK]
    run('python-version', [PYTHON, '-VV'])
    run('node-version', ['node', '--version'])
    run('visible-cores', ['nproc'])
    run('doctor', [PYTHON, 'crisis.py', 'methods', 'doctor'])
    run('pip-check', [PYTHON, '-m', 'pip', 'check'])
    freeze = run('pip-freeze', [PYTHON, '-m', 'pip', 'freeze', '--all'])
    assert sorted(freeze.splitlines()) == sorted((OLD/'resolved-environment.txt').read_bytes().splitlines())
    isolated = run('venv-config', [PYTHON, '-c', 'import sys, pathlib; print(sys.executable, sys.prefix, sys.base_prefix, sep="\\n"); print((pathlib.Path(sys.prefix)/"pyvenv.cfg").read_text())'])
    assert b'include-system-site-packages = false' in isolated
    run('status-before', [*cli, 'status'])
    run('session-start', [*cli, 'session', 'start', '--actor', 'boss 1'])

    prep = Path('tools/prepare_jst_example.py')
    raw = Path('research/models/jst_example/JSTdatasetR6.dta')
    target = JST / 'JSTdatasetR6.dta'
    track('rebuild-portable-inputs', [PYTHON, prep, '--source', raw, '--output', JST], [prep, raw],
          {p: p for p in [target, JST/'panel.csv', JST/'experiment.json', JST/'data_manifest.json']})
    plan = read(MODELS/'compute-current.json')
    single = read(MODELS/'compute-portable-history.json')
    old_job = single['jobs'][0]
    assert old_job in plan['jobs'] and old_job['id'] == 'historical-warning-portable-v3'
    assert len(plan['jobs']) == len({j['id'] for j in plan['jobs']}) == 11
    for j in plan['jobs']:
        source = Path(j['input'])
        assert not source.is_absolute() and source.resolve().is_relative_to(root) and source.is_file()
        csv = read(source).get('csv')
        if csv:
            path = Path(csv)
            assert not path.is_absolute() and path.resolve().is_relative_to(root) and path.is_file()
    single['jobs'][0] = {**old_job, 'id': 'fresh-v2-' + old_job['id']}
    plan_path = OUT / 'replay_plan.json'
    write(plan_path, single)
    run('compute-plan-before', [*cli, 'compute', 'plan', '--file', plan_path])
    run('compute-fresh-v3', [*cli, 'compute', 'run', '--file', plan_path, '--session-seconds', '1800'])
    run('compute-plan-after', [*cli, 'compute', 'plan', '--file', plan_path])
    run('status-during-replay-ledger', [*cli, 'status'])
    ledger = read(LEDGER)
    assert len(ledger['runs']) == 13
    assert ledger['runs'][-1]['id'] == single['jobs'][0]['id'] and ledger['runs'][-1]['status']=='complete'
    assert ledger['runs'][-1]['wall_seconds'] > 0
    shutil.copyfile(LEDGER, LOCAL/'ledger-13.json')
    (LOCAL/'ledger-12.json').write_bytes(frozen(LEDGER))
    LEDGER.write_bytes(frozen(LEDGER))

    grouped('build-examples', 'node', 'build_examples.js', ['engine.js'],
            ['scenarios.json', 'synthetic_household.json', 'loan_input.json'])
    grouped('node-32-regressions', 'node', 'checks.js',
            ['engine.js','synthetic_household.json','scenarios.json'],
            ['checks.json','sample_summary.json','synthetic_strategy_results.csv','legacy_cash_stress.json',
             'sample_baseline_severe_months.json'])
    pyref = HOUSE/'compare_python.py'
    track('python-contracts', [PYTHON, pyref], [pyref,HOUSE/'engine.js',HOUSE/'loan_input.json',
          Path('vendor/numpy-financial/_financial.py'),Path('cncrisis/methods.py')],
          {HOUSE/n:HOUSE/n for n in ['python_reference_checks.json','loan_work_reference.json']})
    grouped('node-migration-monthly','node','compare_migration.js',['engine.js','synthetic_household.json','scenarios.json'],
            ['contract_migration_replay.json'])
    grouped('build-example-html',PYTHON,'build.py',
            ['ui.html','ui.js','engine.js','synthetic_household.json','scenarios.json'],['calculator.html'])
    build = HOUSE/'build.py'
    track('build-formal-html', [PYTHON,build,'--scenarios',FORMAL/'scenarios.json','--output',LOCAL/'calculator.html'],
          [build,HOUSE/'ui.html',HOUSE/'ui.js',HOUSE/'engine.js',HOUSE/'synthetic_household.json',FORMAL/'scenarios.json'],
          {LOCAL/'calculator.html':FORMAL/'calculator.html'})
    run('status-after', [*cli, 'status'])
    run('session-check', [*cli, 'session', 'check', '--actor', 'boss 1'], expected=3)
    assert LEDGER.read_bytes() == frozen(LEDGER)
    assert read(LOGS/'status-before.stdout') == read(LOGS/'status-after.stdout')
    assert (WORK/'research_state.json').read_bytes() == frozen(WORK/'research_state.json')
    print('Recovered the frozen active ledger and original 17-stage status.', flush=True)


if __name__ == '__main__':
    main()
