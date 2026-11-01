"""One original SIX_SEARCH CLI configuration, with read-only return capture."""
from pathlib import Path
import contextlib
import datetime
import hashlib
import io
import json
import os
import runpy
import sys
import time

HERE = Path(__file__).resolve().parent


def plain(x):
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [plain(v) for v in x]
    return x.item() if hasattr(x, 'item') else x


def main():
    runtime = Path(sys.argv[1]).resolve()
    assert not runtime.exists(), 'Fresh runtime required'
    runtime.mkdir(parents=True)
    placements = {'original/SIX_SEARCH.py': 'SIX_SEARCH.py',
                  'related/six_1/spe_dp.py': 'six_1/spe_dp.py'}
    before = {}
    for original, name in placements.items():
        f = runtime/name
        f.parent.mkdir(exist_ok=True, parents=True)
        f.write_bytes((HERE/original).read_bytes())
        before[name] = hashlib.sha256(f.read_bytes()).hexdigest()
    script, helper = runtime/'SIX_SEARCH.py', runtime/'six_1/spe_dp.py'
    output = runtime/'new_best.json'
    argv = [str(script), '--seed', '981773', '--count', '1', '--topics', '7', '--out', str(output)]
    capture = {'original_main_calls': 0, 'original_sample_calls': 0, 'original_solve_calls': 0}

    def observe(frame, event, arg):
        name, source = frame.f_code.co_name, frame.f_code.co_filename
        if source == str(script) and name == 'main' and event == 'call':
            capture['original_main_calls'] += 1
        if source == str(script) and name == 'sample' and event == 'return':
            capture['original_sample_calls'] += 1
            capture['weights'] = plain(arg)
        if source == str(helper) and name == 'solve' and event == 'return':
            capture['original_solve_calls'] += 1
            capture['result'] = plain(arg)

    stdout, stderr = io.StringIO(), io.StringIO()
    old_path, old_argv, old_cwd = list(sys.path), list(sys.argv), Path.cwd()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.perf_counter()
    try:
        os.chdir(runtime)
        sys.path.insert(0, str(runtime))
        sys.argv = argv
        sys.setprofile(observe)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            runpy.run_path(str(script), run_name='__main__')
    finally:
        sys.setprofile(None)
        sys.path[:] = old_path
        sys.argv = old_argv
        os.chdir(old_cwd)
    elapsed = time.perf_counter()-tick
    replay = HERE/'replay'
    replay.mkdir(exist_ok=True)
    (replay/'stdout.txt').write_text(stdout.getvalue())
    (replay/'stderr.txt').write_text(stderr.getvalue())
    (replay/'capture.json').write_text(json.dumps(capture, indent=2)+'\n')
    if output.exists():
        (replay/'new_best.json').write_bytes(output.read_bytes())
    after = {name: hashlib.sha256((runtime/name).read_bytes()).hexdigest() for name in before}
    event = {'kind': 'one-original-cli-configuration-with-read-only-profile',
             'started_utc': started, 'elapsed_seconds': elapsed, 'argv': argv,
             'source_sha256_before': before, 'source_sha256_after': after,
             'sources_unchanged': before == after, 'normal_return': True,
             'main_calls': capture['original_main_calls'], 'sample_calls': capture['original_sample_calls'],
             'solve_calls': capture['original_solve_calls'], 'configured_trials': 1,
             'default_1000_trials_replayed': False, 'lp_calls': 0,
             'original_witness_requested': False, 'original_exact_verify_calls': 0,
             'original_output_written': output.exists(), 'stderr_bytes': len(stderr.getvalue().encode()),
             'arrays_functions_and_random_state_modified': False}
    (replay/'execution.json').write_text(json.dumps(event, indent=2)+'\n')
    assert before == after
    assert event['main_calls'] == event['sample_calls'] == event['solve_calls'] == 1
    assert len(capture['weights']) == 128 and capture['weights'][0] == 0
    assert all(isinstance(x, int) and x >= 0 for x in capture['weights'])
    assert not stderr.getvalue()
    if output.exists():
        data = json.loads(output.read_text())
        assert data['weights'] == capture['weights'] and data['result'] == capture['result']
    print(json.dumps({'event': event, 'customers': sum(capture['weights']), 'result': capture['result']}))


if __name__ == '__main__':
    main()
