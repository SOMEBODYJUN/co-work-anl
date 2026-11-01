"""One unchanged original main; passive Python profile records LP calls/returns."""
from pathlib import Path
import contextlib, hashlib, json, platform, runpy, shutil, sys, time
import numpy, scipy

BASE = Path(__file__).resolve().parent
SOURCE = Path('/workspace/scratch/c0ab78c47566/round14-fresh-global-two-source.py')
RUNTIME = BASE / 'runtime'
RUNTIME.mkdir(exist_ok=False)
SCRIPT = RUNTIME / 'probe_fresh_global_two.py'
shutil.copyfile(SOURCE, SCRIPT)
argv = [str(SCRIPT), '--q', '6', '--cases', '4', '--seed', '71213', '--max-background', '4', '--output', 'bounded_probe.json']
calls = []; pending = {}; main_calls = 0

def observe(frame, event, arg):
    global main_calls
    if event == 'call' and frame.f_code.co_filename == str(SCRIPT) and frame.f_code.co_name == '<module>':
        main_calls += 1
    if frame.f_code.co_name != 'linprog' or not frame.f_code.co_filename.endswith('/scipy/optimize/_linprog.py'):
        return
    if event == 'call':
        parent = frame.f_back
        assert parent.f_code.co_filename == str(SCRIPT)
        f = parent.f_locals; a = frame.f_locals
        rec = dict(case=f['case'], L=f['L'], actual=f['actual'], response=list(f['response']), compare=[f['T'], f['S']],
                   c=a['c'].tolist(), A_ub=a['A_ub'].tolist(), b_ub=a['b_ub'].tolist(),
                   A_eq=a['A_eq'].tolist(), b_eq=a['b_eq'], bounds=a['bounds'], method=a['method'])
        pending[id(frame)] = rec
    elif event == 'return':
        rec = pending.pop(id(frame))
        rec['result'] = dict(success=bool(arg.success), status=int(arg.status), message=str(arg.message),
                             fun=None if arg.fun is None else float(arg.fun),
                             x=None if arg.x is None else arg.x.tolist(), nit=int(arg.nit))
        calls.append(rec)

before = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
start = time.perf_counter(); exception = None; exit_code = 0
sys.argv = argv
with (BASE/'stdout.txt').open('w') as out, (BASE/'stderr.txt').open('w') as err:
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            sys.setprofile(observe)
            runpy.run_path(str(SCRIPT), run_name='__main__')
    except BaseException as exc:
        import traceback
        exit_code = 1; exception = repr(exc)
        traceback.print_exc(file=err)
    finally:
        sys.setprofile(None)
elapsed = time.perf_counter()-start
assert not pending
(BASE/'lp-capture.json').write_text(json.dumps(calls, indent=2)+'\n')
report = dict(event='one unchanged original main via runpy with passive sys.setprofile', argv=argv,
              original_main_calls=main_calls, lp_calls=len(calls), exit_code=exit_code, exception=exception,
              elapsed_seconds=elapsed, source_sha256_before=before,
              source_sha256_after=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
              python=sys.version, numpy=numpy.__version__, scipy=scipy.__version__, platform=platform.platform(),
              capture='lp-capture.json', stdout='stdout.txt', stderr='stderr.txt',
              output='runtime/bounded_probe.json', outputs=sorted(p.name for p in RUNTIME.iterdir()))
(BASE/'execution.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
raise SystemExit(exit_code)
