"""One unmodified source __main__ run, with passive profile counts and returned globals."""
import contextlib
import datetime
import gzip
import hashlib
import io
import json
from pathlib import Path
import platform
import runpy
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'round16-seven-maxima-source.py'
OUT = ROOT / 'original-event'
OUT.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = sha(SOURCE)
assert before == 'bbff2b9a73fb15b000992d9ab14db9f5178f2de8ef8a249838415e2eb13a175a'
counts = {'build': 0, 'mixed_coeffs': 0, 'linprog': 0}
def profile(frame, event, arg):
    if event != 'call':
        return
    name = frame.f_code.co_name
    if frame.f_code.co_filename == str(SOURCE) and name in ('build', 'mixed_coeffs'):
        counts[name] += 1
    if name == 'linprog' and frame.f_globals.get('__name__') == 'scipy.optimize._linprog':
        counts['linprog'] += 1

stdout, stderr = io.StringIO(), io.StringIO()
argv = list(sys.argv)
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.perf_counter()
status = 0
try:
    sys.argv = [str(SOURCE)]
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        sys.setprofile(profile)
        ns = runpy.run_path(str(SOURCE), run_name='__main__')
except BaseException:
    status = 1
    traceback.print_exc(file=stderr)
finally:
    sys.setprofile(None)
    sys.argv = argv
elapsed = time.perf_counter() - t0
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
(OUT / 'stdout.txt').write_text(stdout.getvalue())
(OUT / 'stderr.txt').write_text(stderr.getvalue())
assert before == sha(SOURCE)
if status == 0:
    import numpy, scipy
    def opt(r):
        return {'success': bool(r.success), 'status': int(r.status), 'message': str(r.message),
                'fun': None if r.fun is None else float(r.fun),
                'x': None if r.x is None else r.x.tolist(), 'nit': int(r.nit)}
    payload = {'source_sha256': before, 'excluded': ns['args'].excluded,
               'route': ns['route'], 'names': ns['names'], 'types': ns['typ'],
               'A': ns['A'].tolist(), 'b': ns['b'].tolist(), 'res': opt(ns['res']),
               'sep': opt(ns['sep']) if 'sep' in ns else None}
    raw = (json.dumps(payload, separators=(',', ':')) + '\n').encode()
    (OUT / 'capture.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    versions = {'python': platform.python_version(), 'numpy': numpy.__version__, 'scipy': scipy.__version__}
else:
    versions = {'python': platform.python_version()}
event = {'identity': 'wrapper invoking original unmodified __main__ once with default arguments',
         'wrapper_argv': argv, 'source_argv': [str(SOURCE)], 'cwd': str(Path.cwd()),
         'start_utc': start, 'end_utc': end, 'elapsed_seconds': elapsed, 'exit_code': status,
         'assertions_enabled': __debug__, 'versions': versions, 'counts': counts,
         'original_main_calls': 1, 'direct_CLI_calls': 0, 'SPE_solver_calls': 0,
         'source_sha256_before': before, 'source_sha256_after': sha(SOURCE),
         'stdout_sha256': sha(OUT / 'stdout.txt'), 'stderr_sha256': sha(OUT / 'stderr.txt')}
if status == 0:
    event.update({'capture_sha256': sha(OUT / 'capture.json.gz'), 'capture_uncompressed_sha256': hashlib.sha256(raw).hexdigest(),
                  'capture_uncompressed_bytes': len(raw), 'matrix_shape': list(ns['A'].shape),
                  'res_status': int(ns['res'].status), 'sep_status': int(ns['sep'].status) if 'sep' in ns else None})
(OUT / 'execution.json').write_text(json.dumps(event, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(event, ensure_ascii=False))
raise SystemExit(status)
