"""Run unmodified 3203B original once with read-only return observation.

No code/parameters/return values are replaced; no early stop. The source has
top-level execution and writes its original full report into a fresh runtime.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import gzip
import hashlib
import json
import runpy
import sys

BASE = Path(__file__).resolve().parent


def main():
    source = BASE / 'original/time/partial_core_independent_audit.py'
    runtime = BASE / 'runtime/time'
    runtime.mkdir(parents=True, exist_ok=False)
    target = runtime / source.name
    target.write_bytes(source.read_bytes())
    captures = []
    calls = Counter()

    def observe(frame, event, argument):
        if frame.f_code.co_filename != str(target):
            return
        name = frame.f_code.co_name
        if event == 'call':
            calls[name] += 1
        if event == 'return' and name == 'audit':
            local = frame.f_locals
            captures.append({
                'prefix_names': local['prefix_names'], 'tail_names': local['tail_names'],
                'slacks_in_original_order': list(map(str, local['slacks'])),
                'D_dominance_in_original_order': list(map(str, local['dominance'])),
                'policy': [{'history': h, 'action': a} for h, a in local['policy'].items()],
                'actual_six_action_profile': local['actual'],
            })

    assert not target.with_suffix('.json').exists()
    old_profile = sys.getprofile()
    try:
        sys.setprofile(observe)
        namespace = runpy.run_path(str(target), run_name='__main__')
    finally:
        sys.setprofile(old_profile)
    assert source.read_bytes() == target.read_bytes()
    assert len(captures) == calls['audit'] == 2
    generated = target.with_suffix('.json').read_bytes()
    frozen = (BASE / 'original/time/partial_core_independent_audit.json').read_bytes()
    assert generated == frozen
    names = list(namespace['names'])
    coverage = namespace['S']
    units = sorted(set().union(*coverage.values()))
    signatures = Counter(tuple(i for i, a in enumerate(names) if x in coverage[a]) for x in units)
    current = {
        'scope': 'passive original audit returns only; no modified computations or early stop',
        'original_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'original_audit_calls': calls['audit'], 'original_pay_path_calls': calls['pay_path'],
        'native_report_byte_identical': True,
        'generated_report_size': len(generated),
        'generated_report_sha256': hashlib.sha256(generated).hexdigest(),
        'native_topics': names,
        'native_unit_interest_multiplicities': [{'topics': a, 'multiplicity': v} for a, v in sorted(signatures.items())],
        'captured_original_audits': captures,
    }
    payload = (json.dumps(current, separators=(',', ':')) + '\n').encode()
    with (BASE / 'replay/original-return-observation.json.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as out:
            out.write(payload)
    (BASE / 'replay/original-return-observation-identity.json').write_text(json.dumps({
        'uncompressed_size': len(payload), 'uncompressed_sha256': hashlib.sha256(payload).hexdigest(),
        'audit_calls': calls['audit'], 'pay_path_calls': calls['pay_path'],
        'source_unmodified': True, 'normal_original_completion': True,
        'generated_report_byte_identical': True,
        'generated_report_sha256': hashlib.sha256(generated).hexdigest(),
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
