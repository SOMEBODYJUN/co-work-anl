#!/usr/bin/env python3
"""Run the unchanged two exact audits, preserving all generated stdout."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'original'
OUTPUT = ROOT / 'replay'
OUTPUT.mkdir(exist_ok=True)

def run(name):
    relative = Path('tests/audits/weighted_congestion/structural_reconstruction') / (name + '.py')
    result = subprocess.run([sys.executable, '-B', str(relative)], cwd=SOURCE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (OUTPUT / (name + '.json')).write_bytes(result.stdout)
    (OUTPUT / (name + '.stderr.txt')).write_bytes(result.stderr)
    assert result.returncode == 0, result.stderr.decode()
    frozen = SOURCE / 'evidence/runs/weighted_congestion/structural_reconstruction' / (name + '.json')
    old, new = json.loads(frozen.read_bytes()), json.loads(result.stdout)
    differences = {key: {'old': old.get(key), 'new': new.get(key)}
                   for key in old.keys() | new.keys() if old.get(key) != new.get(key)}
    assert not differences, differences
    return {'script': str(relative), 'source_sha256': hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest(),
            'exit_code': result.returncode, 'byte_equal': frozen.read_bytes() == result.stdout,
            'differences': differences, 'full_result': new,
            'scope': 'unchanged finite exact inputs; no enormous asymptotic game or infinite tail enumeration'}

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        rows = list(executor.map(run, ['near_degree_audit', 'raw_resource_audit']))
    result = {'runs': rows, 'all_passed': True}
    (OUTPUT / 'comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
