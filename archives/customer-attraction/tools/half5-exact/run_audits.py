"""Replay the frozen five-provider certificate and the review-only row check.

This is a runner and integrity check, not a new independent proof verifier.
No floating search or LP solver is used. Run Python without -O: the supplied
verifiers intentionally express proof obligations as assertions.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def run(script, *args):
    result = subprocess.run([sys.executable, str(script), *map(str, args)],
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout


def main():
    if not __debug__:
        raise SystemExit('Assertions are required: do not use Python -O.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ARCHIVE/'evidence/half5-exact/replay')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    certificate = read(HERE/'certificate.json')
    kcols = read(HERE/'active_k_columns.json')
    weights = {k: int(v) for k, v in certificate['integer_multipliers'].items()}
    assert len(weights) == 53 and min(weights.values()) > 0
    assert int(certificate['common_denominator']) == 10**22
    assert int(certificate['beta_numerator']) == 2*10**22
    assert set(weights) == set(kcols['row_K_coefficients'])
    weighted_k = sum(weights[k]*int(kcols['row_K_coefficients'][k]) for k in weights)
    assert weighted_k == -2264870
    cert_hash = hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest()
    assert cert_hash == kcols['certificate_sha256']
    # The current exact proof never calls the unsafe, unused PC2 TAX parser.
    pc2 = read(HERE/'components/priced_player2.json')
    assert not any(k.startswith('TAX:') for c in pc2 for k in c['multipliers'])
    local = json.loads(run(HERE/'components/verify_local_components.py'))
    assert (local['component_count'], local['coefficient_states']) == (36, 47872)
    (output/'local.json').write_text(json.dumps(local, indent=2)+'\n')
    run(HERE/'verify_certificate.py', '--manifest', HERE/'row_manifest.json',
        '--output', output/'global.json')
    global_check = read(output/'global.json')
    assert global_check['status'] == 'passed'
    assert global_check['conditional_cases'] == 6144
    assert global_check['minimum_scaled_integer_residual'] == '0'
    assert global_check['K_column_residual'] == '2264870'
    assert global_check['zero_cases'] == 2 and global_check['negative_cases'] == []
    assert global_check['certificate_sha256'] == cert_hash
    semantics = json.loads(run(HERE/'literal_semantics.py'))
    assert semantics['status'] == 'passed'
    assert semantics['family_histogram_entries_checked'] == 157483008
    assert semantics['fixed_row_cases_checked'] == 878592
    (output/'semantics.json').write_text(json.dumps(semantics, indent=2)+'\n')
    minimum_covered = min(int(v) for k, v in global_check['minimum_by_actual_mask'].items()
                          if k != '00000')
    assert minimum_covered == 1788637526774492965820
    epsilon = Fraction(minimum_covered, 120*10**22)
    expected = Fraction(89431876338724648291, 60000000000000000000000)
    assert epsilon == expected
    programs = {p.relative_to(HERE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (HERE/'verify_certificate.py',
                          HERE/'components/verify_local_components.py',
                          HERE/'literal_semantics.py', Path(__file__).resolve())}
    summary = dict(status='passed', scope='same-implementation replay plus literal row cross-check',
                   certificate_sha256=cert_hash, weighted_K_column=str(weighted_k),
                   covered_residual_minimum=str(minimum_covered), epsilon=str(epsilon),
                   improved_factor=str(2-epsilon), coverage_ratio=str(1/(2-epsilon)),
                   local_components=36, local_coefficient_states=47872,
                   main_conditional_cases=6144, pc2_tax_rows=0,
                   python=sys.version.split()[0], program_sha256=programs)
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
