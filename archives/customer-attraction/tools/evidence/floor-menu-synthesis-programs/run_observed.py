"""One call to each unmodified solve(4); passive return-frame capture only."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import platform
import runpy
import sys
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
SOURCES = [ROOT / 'round19-menu_synthesis.py', ROOT / 'round19-prefix_menu_synthesis.py']

def digest(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def plain(v):
    if isinstance(v, dict):
        return {str(k): plain(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [plain(x) for x in v]
    if hasattr(v, 'tolist'):
        return plain(v.tolist())
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    raise TypeError(type(v).__name__)

def main():
    out = BASE / 'replay'
    out.mkdir(exist_ok=False)
    captured = []
    events = []
    for src in SOURCES:
        before = digest(src)
        env = runpy.run_path(str(src), run_name='floor_menu_observed_import')
        returns = []
        def observer(frame, event, arg):
            if event == 'return' and frame.f_code.co_filename == str(src) and frame.f_code.co_name == 'solve':
                returns.append(plain({k: frame.f_locals[k] for k in ('m', 'cols', 'X', 'w', 'o', 'A', 'c', 'res')}))
                if 'names' in frame.f_locals:
                    returns[-1]['names'] = plain(frame.f_locals['names'])
        stdout, stderr = io.StringIO(), io.StringIO()
        start = time.time()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            sys.setprofile(observer)
            try:
                result = env['solve'](4)
            finally:
                sys.setprofile(None)
        elapsed = time.time() - start
        assert len(returns) == 1 and digest(src) == before
        tag = 'prefix' if 'prefix' in src.name else 'aggregate'
        (out / f'{tag}-stdout.txt').write_text(stdout.getvalue())
        (out / f'{tag}-stderr.txt').write_text(stderr.getvalue())
        captured.append({'tag': tag, 'source': str(src), **returns[0]})
        events.append({'tag': tag, 'source': str(src), 'source_before': before, 'source_after': digest(src), 'call': 'solve(4)', 'solve_returns': len(returns), 'seconds': elapsed, 'status': int(result.status), 'fun': float(result.fun), 'main_calls': 0, 'LP_calls_by_source_contract': 1})
    import numpy, scipy
    (out / 'capture.json').write_text(json.dumps(captured, ensure_ascii=False, indent=2) + '\n')
    event = {'identity': 'two original function calls, not original main/default sweep or historical replay', 'calls': events, 'python': platform.python_version(), 'numpy': numpy.__version__, 'scipy': scipy.__version__, 'observer': digest(Path(__file__)), 'capture': digest(out / 'capture.json'), 'default_main_calls': 0, 'LP_calls': 2, 'exact_audit_calls': 0}
    (out / 'execution.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(event, ensure_ascii=False))

if __name__ == '__main__':
    main()
