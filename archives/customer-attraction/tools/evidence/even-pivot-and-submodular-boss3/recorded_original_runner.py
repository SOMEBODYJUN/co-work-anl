from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
manifest = json.loads((base / 'even-pivot-submodular-five-manifest.json').read_text())
stage = base / 'boss3_even_pivot_delivery'
evidence_rel = Path('archives/customer-attraction/tools/evidence/even-pivot-and-submodular-boss3')
evidence = stage / evidence_rel
runtime = base / 'boss3_even_pivot_exact_runtime'
runtime.mkdir(exist_ok=False)
evidence.mkdir(parents=True, exist_ok=True)
source_manifest = []
for source in manifest:
    data = Path(source['exported_path']).read_bytes()
    assert len(data) == source['size']
    assert hashlib.sha256(data).hexdigest() == source['sha256']
    rel = Path('original') / source['id'] / Path(source['path']).name
    target = evidence / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    record = dict(source)
    record.pop('exported_path')
    record['stored_path'] = (evidence_rel / rel).as_posix()
    source_manifest.append(record)
    if target.name == 'verify_even_pivot_taxes.py':
        shutil.copyfile(target, runtime / target.name)
        program = target
    elif target.name == 'even_pivot_taxes_verified.json':
        expected = target
(evidence / 'source-manifest.json').write_text(json.dumps(source_manifest, ensure_ascii=False, indent=2) + '\n')
output = evidence / 'exact-replay'
output.mkdir(exist_ok=False)
argv = [sys.executable, '-B', str(runtime / program.name)]
started = datetime.now(timezone.utc).isoformat()
t0 = time.perf_counter()
p = subprocess.run(argv, cwd=runtime, capture_output=True)
seconds = time.perf_counter() - t0
(output / 'stdout.txt').write_bytes(p.stdout)
(output / 'stderr.txt').write_bytes(p.stderr)
generated = runtime / 'even_pivot_taxes_verified.json'
raw = generated.read_bytes() if generated.exists() else b''
(output / 'generated-report.json').write_bytes(raw)
record = {
    'event': 'one unchanged original Fraction CLI execution',
    'argv': argv,
    'cwd': str(runtime),
    'started_utc': started,
    'elapsed_seconds': seconds,
    'exit_code': p.returncode,
    'python': sys.version,
    'optimize': sys.flags.optimize,
    'original_program_sha256': hashlib.sha256(program.read_bytes()).hexdigest(),
    'runtime_program_sha256': hashlib.sha256((runtime / program.name).read_bytes()).hexdigest(),
    'expected_report_sha256': hashlib.sha256(expected.read_bytes()).hexdigest(),
    'generated_report_sha256': hashlib.sha256(raw).hexdigest(),
    'report_byte_equal': raw == expected.read_bytes(),
    'stdout_byte_equal_report': p.stdout == raw,
    'stderr_bytes': len(p.stderr),
    'original_cli_runs': 1,
    'new_optimization_calls': 0,
}
(output / 'event.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(record, ensure_ascii=False, indent=2))
assert p.returncode == 0 and raw == expected.read_bytes() and not p.stderr
