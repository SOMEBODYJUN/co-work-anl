"""Run the unmodified frozen verifier once in a disposable isolated layout.

The output directory must not exist. The frozen report is never overwritten.
This driver does not solve an LP or construct a complete SPE strategy.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'original/research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/parent'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    selected = ['verify_suffix_envelope.py', 'suffix_envelope_input.json', 'suffix_envelope_exact.json']
    bindings = []
    for name in selected:
        item = next(x for x in manifest if x['path'].endswith('/parent/' + name))
        source = SOURCE / name
        assert source.stat().st_size == item['size'] and digest(source) == item['sha256']
        bindings.append({'name': name, 'id': item['id'], 'sha256': item['sha256'], 'bytes': item['size']})
    with tempfile.TemporaryDirectory(prefix='original-layout-', dir=out) as temporary:
        runtime = Path(temporary)
        for name in selected[:2]:
            shutil.copy2(SOURCE / name, runtime / name)
        command = [sys.executable, str(runtime / selected[0])]
        start = time.perf_counter()
        process = subprocess.run(command, cwd=runtime, capture_output=True)
        elapsed = time.perf_counter() - start
        (out / 'stdout.txt').write_bytes(process.stdout)
        (out / 'stderr.txt').write_bytes(process.stderr)
        report = runtime / selected[2]
        if report.exists():
            shutil.copy2(report, out / selected[2])
        event = {
            'operation': 'one-unmodified-original-main-on-frozen-integer-input',
            'python': platform.python_version(), 'assertions_enabled_in_driver': __debug__,
            'original_main_calls': 1, 'LP_calls': 0, 'SPE_solver_calls': 0,
            'argv': command, 'cwd': str(runtime), 'exit_code': process.returncode,
            'elapsed_seconds': elapsed, 'stdout_bytes': len(process.stdout),
            'stderr_bytes': len(process.stderr), 'source_bindings': bindings,
            'driver_sha256': digest(Path(__file__)),
            'output_report_exists': report.exists(),
            'report_byte_equal_to_frozen': report.exists() and report.read_bytes() == (SOURCE / selected[2]).read_bytes(),
            'scope': '72 prefix safety rows, 18563 suffix comparison multisets, and all 12x12 penultimate/last choices in this fixed catalog; no complete SPE realization.'
        }
        if report.exists():
            event['report_sha256'] = digest(report)
        (out / 'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(event, ensure_ascii=False, indent=2))
        assert process.returncode == 0
        assert event['report_byte_equal_to_frozen']


if __name__ == '__main__':
    main()
