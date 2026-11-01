"""Execute the unchanged flow source once in isolation; observe two LP returns."""
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


def main():
    runtime = Path(sys.argv[1]).resolve()
    assert not runtime.exists(), 'Use a fresh runtime'
    runtime.mkdir(parents=True)
    original = HERE/'original/circuit_flow_probe.py'
    script = runtime/original.name
    script.write_bytes(original.read_bytes())
    before = hashlib.sha256(script.read_bytes()).hexdigest()
    lp_events = []
    original_main_calls = 0

    def observe(frame, event, arg):
        nonlocal original_main_calls
        if frame.f_code.co_filename == str(script) and frame.f_code.co_name == 'main' and event == 'call':
            original_main_calls += 1
        parent = frame.f_back
        if (event == 'return' and frame.f_code.co_name == 'linprog' and parent is not None
                and parent.f_code.co_filename == str(script)):
            lp_events.append({'status': int(arg.status), 'success': bool(arg.success),
                              'fun': float(arg.fun) if arg.fun is not None else None,
                              'variables': len(arg.x) if arg.x is not None else None,
                              'message': str(arg.message)})

    stdout, stderr = io.StringIO(), io.StringIO()
    old_argv, old_cwd = list(sys.argv), Path.cwd()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.perf_counter()
    try:
        sys.argv = [str(script)]
        os.chdir(runtime)
        sys.setprofile(observe)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            runpy.run_path(str(script), run_name='__main__')
    finally:
        sys.setprofile(None)
        sys.argv = old_argv
        os.chdir(old_cwd)
    elapsed = time.perf_counter()-tick
    replay = HERE/'replay'
    replay.mkdir(exist_ok=True)
    (replay/'stdout.txt').write_text(stdout.getvalue())
    (replay/'stderr.txt').write_text(stderr.getvalue())
    produced = runtime/'circuit_flow_certificate.json'
    expected = HERE/'original/circuit_flow_certificate.json'
    (replay/'circuit_flow_certificate.json').write_bytes(produced.read_bytes())
    data = json.loads(produced.read_text())
    event = {'kind': 'one-unchanged-original-main-with-read-only-profile',
             'started_utc': started, 'elapsed_seconds': elapsed, 'runtime': str(runtime),
             'source_sha256_before': before,
             'source_sha256_after': hashlib.sha256(script.read_bytes()).hexdigest(),
             'original_main_calls': original_main_calls, 'lp_events': lp_events,
             'new_report_bytes': produced.stat().st_size,
             'new_report_sha256': hashlib.sha256(produced.read_bytes()).hexdigest(),
             'frozen_report_sha256': hashlib.sha256(expected.read_bytes()).hexdigest(),
             'new_report_byte_equal': produced.read_bytes() == expected.read_bytes(),
             'assertions_enabled': sys.flags.optimize == 0, 'normal_return': True,
             'source_functions_or_arrays_modified': False, 'stderr_bytes': len(stderr.getvalue().encode()),
             'new_bound': data['bound'], 'scope': 'one fixed policy and comparison in abstract payoff relaxation'}
    (replay/'execution.json').write_text(json.dumps(event, indent=2)+'\n')
    assert before == event['source_sha256_after']
    assert original_main_calls == 1 and len(lp_events) == 2
    assert all(e['success'] for e in lp_events)
    assert not stderr.getvalue()
    print(json.dumps(event))


if __name__ == '__main__':
    main()
