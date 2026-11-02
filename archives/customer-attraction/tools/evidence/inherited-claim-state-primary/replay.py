"""Run the frozen finite claim-state diagnostic in a disposable original layout."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

base = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
for item in json.loads((base / 'manifest.json').read_text()):
    raw = (base / 'original' / item['path']).read_bytes()
    assert len(raw) == item['size']
    assert hashlib.sha256(raw).hexdigest() == item['sha256']
relative = Path('research/workspaces/customer-attraction/R-a5cc2a7008c548ec9b48d8386b872229/variable_induction/audit_claim_state.py')
with tempfile.TemporaryDirectory(prefix='claim-state-', dir=args.out.resolve()) as temporary:
    root = Path(temporary) / 'source'
    shutil.copytree(base / 'original', root)
    start = time.perf_counter()
    result = subprocess.run([sys.executable, str(root / relative)], cwd=root, capture_output=True)
    elapsed = time.perf_counter() - start
    report = (root / relative).with_suffix('.json').read_bytes()
frozen = (base / 'original' / relative).with_suffix('.json').read_bytes()
(args.out / 'stdout.txt').write_bytes(result.stdout)
(args.out / 'stderr.txt').write_bytes(result.stderr)
(args.out / 'report.json').write_bytes(report)
event = {'original_entry_executions': 1, 'returncode': result.returncode,
         'seconds': elapsed, 'generated_equals_frozen': report == frozen,
         'stdout_equals_frozen': result.stdout == frozen,
         'scope': 'finite canonical-dependent diagnostic, not a universal credit bound'}
(args.out / 'event.json').write_text(json.dumps(event, indent=2) + '\n')
print(json.dumps(event, indent=2))
assert result.returncode == 0 and report == frozen and result.stdout == frozen
