"""Observe one unchanged worst_tax.py sample; stop before the second draw.

This is an explicitly bounded prefix, not an 80-iteration original replay.
No original source, function, returned array or random state is changed.
"""
from pathlib import Path
import contextlib
import datetime
import gzip
import hashlib
import io
import json
import os
import runpy
import sys
import time

HERE = Path(__file__).resolve().parent


class PlannedStop(Exception):
    pass


def main():
    runtime = Path(sys.argv[1]).resolve()
    assert not runtime.exists(), 'Fresh runtime required'
    runtime.mkdir(parents=True)
    mapping = {'original/worst_tax.py': 'security/static/worst_tax.py',
               'related/tax_probe.py': 'security/static/tax_probe.py'}
    mapping.update({f'dependencies/customer_attraction/{n}': f'customer_attraction/{n}'
                    for n in ['__init__.py', 'model.py', 'exact.py', 'certificate.py']})
    before = {}
    for source, name in mapping.items():
        target = runtime/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((HERE/source).read_bytes())
        before[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    script = runtime/'security/static/worst_tax.py'
    replay = HERE/'first-sample'
    replay.mkdir(exist_ok=True)
    capture = {'lp_results': [], 'optimizer_calls': 0}

    def observe(frame, event, arg):
        parent = frame.f_back
        if (event == 'call' and parent is not None
                and parent.f_code.co_filename == str(script)
                and parent.f_locals.get('it') == 1):
            raise PlannedStop('Before first Python call of second iteration')
        own = frame.f_globals.get('__file__') == str(script)
        if own and frame.f_code.co_name == 'optimize':
            if event == 'call':
                capture['optimizer_calls'] += 1
                capture['seed_game'] = parent.f_locals['ins'].to_dict()
                capture['selected_terminal_counts'] = list(parent.f_locals['target'])
                capture['sigma'] = [{'history': list(h), 'action': int(a)}
                                    for h, a in sorted(frame.f_locals['sigma'].items(),
                                                       key=lambda x: (len(x[0]), x[0]))]
            elif event == 'return':
                (fun, comp, weights), root, gamma = arg
                capture['selected_result'] = {'fun': float(fun), 'comparator': list(comp),
                                              'weights': weights.tolist(), 'root': list(root)}
                capture['gamma_rows'] = len(gamma)
                payload = json.dumps([[str(x) for x in row] for row in gamma],
                                     separators=(',', ':')).encode()
                (replay/'original-gamma.json.gz').write_bytes(gzip.compress(payload, mtime=0))
        if (event == 'return' and frame.f_code.co_name == 'linprog' and parent is not None
                and parent.f_code.co_name == 'optimize'
                and parent.f_globals.get('__file__') == str(script)):
            capture['lp_results'].append({'comparator': list(parent.f_locals['cc']),
                                          'success': bool(arg.success), 'status': int(arg.status),
                                          'message': str(arg.message),
                                          'fun': None if arg.fun is None else float(arg.fun)})

    stdout, stderr = io.StringIO(), io.StringIO()
    old_cwd = Path.cwd()
    old_path = list(sys.path)
    old_argv = list(sys.argv)
    stopped = False
    normal_return = False
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.perf_counter()
    try:
        os.chdir(runtime)
        sys.path.insert(0, str(runtime))
        sys.argv = [str(script)]
        sys.setprofile(observe)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(script), run_name='__main__')
                normal_return = True
            except PlannedStop:
                stopped = True
    finally:
        sys.setprofile(None)
        sys.path[:] = old_path
        sys.argv = old_argv
        os.chdir(old_cwd)
    elapsed = time.perf_counter()-tick
    (replay/'stdout.txt').write_text(stdout.getvalue())
    (replay/'stderr.txt').write_text(stderr.getvalue())
    after = {name: hashlib.sha256((runtime/name).read_bytes()).hexdigest() for name in before}
    event = {'kind': 'unchanged-source-first-sample-with-read-only-profile-and-planned-stop',
             'started_utc': started, 'elapsed_seconds': elapsed,
             'runtime': str(runtime), 'script': str(script),
             'source_sha256_before': before, 'source_sha256_after': after,
             'sources_unchanged': before == after,
             'planned_stop_before_second_draw': stopped, 'original_normal_return': normal_return,
             'completed_samples': capture['optimizer_calls'],
             'lp_attempts': len(capture['lp_results']),
             'original_80_samples_completed': False,
             'arrays_functions_and_random_state_changed': False,
             'candidate_file_written': (runtime/'security/static/tax_candidate.json').exists(),
             'stderr_bytes': len(stderr.getvalue().encode()),
             'assertions_enabled': sys.flags.optimize == 0}
    (replay/'execution.json').write_text(json.dumps(event, indent=2)+'\n')
    (replay/'capture.json').write_text(json.dumps(capture, indent=2)+'\n')
    assert before == after
    assert capture['optimizer_calls'] == 1 and len(capture['lp_results']) == 15
    assert stopped or event['candidate_file_written']
    assert not stderr.getvalue()
    print(json.dumps(event))


if __name__ == '__main__':
    main()
