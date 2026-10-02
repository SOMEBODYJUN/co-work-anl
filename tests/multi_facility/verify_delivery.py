"""Reproduce the standalone delivery; NOT the upstream structural checker."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import platform
import py_compile
import subprocess
import sys
import tempfile
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'tests'/'multi_facility'))
from multi_facility_spe.two_exists import Instance, evaluate_continuation
from definition_check import check_certificate, check_ne


def run():
    sources = sorted((ROOT/'multi_facility_spe').glob('*.py')) + sorted((ROOT/'tests'/'multi_facility').glob('*.py'))
    for path in sources:
        py_compile.compile(str(path), doraise=True)
    frozen = {}
    with tempfile.TemporaryDirectory(prefix='kfac-verify-') as tempdir:
        temp = Path(tempdir)
        for name, script in [('kfac_two_exact', 'run_exact_audit.py'),
                             ('kfac_two_reverse', 'run_reverse_audit.py'),
                             ('kfac_lexmax_barrier', 'run_lexmax_barrier_audit.py')]:
            output = temp/(name+'.json')
            subprocess.run([sys.executable, str(ROOT/'tests'/'multi_facility'/script),
                            '--output', str(output)], cwd=ROOT, check=True, capture_output=True, text=True)
            actual = json.loads(output.read_text())
            expected = json.loads((ROOT/'evidence'/'runs'/(name+'.json')).read_text())
            actual.pop('python', None)
            expected.pop('python', None)
            assert actual == expected, 'Frozen arithmetic result mismatch: '+name
            frozen[name] = 'exact match (Python version excluded from comparison)'
        output = temp/'cli_certificate.json'
        subprocess.run([sys.executable, '-m', 'multi_facility_spe',
                        str(ROOT/'examples'/'multi_facility'/'rational.json'),
                        '--output', str(output)], cwd=ROOT, check=True, capture_output=True, text=True)
        check_certificate(json.loads(output.read_text()))
        # Repeating with the same output must refuse to overwrite it.
        refusal = subprocess.run([sys.executable, '-m', 'multi_facility_spe',
                        str(ROOT/'examples'/'multi_facility'/'rational.json'),
                        '--output', str(output)], cwd=ROOT, capture_output=True, text=True)
        assert refusal.returncode != 0
    complete_evaluations, default_evaluations, certs = 0, 0, 0
    for path in sorted((ROOT/'evidence'/'certificates'/'multi_facility').glob('*.json')):
        certificate = json.loads(path.read_text())
        check_certificate(certificate)
        certs += 1
        instance = certificate['instance']
        if instance['k'] <= 5:
            original = tuple(certificate['on_path']['layout'])
            for layout in product(range(instance['m']), repeat=instance['k']):
                probabilities = evaluate_continuation(certificate, layout)
                check_ne(instance, layout, probabilities)
                complete_evaluations += 1
                if sum(a != b for a, b in zip(original, layout)) >= 2:
                    default_evaluations += 1
    valid = dict(m=2, k=3, clients=[dict(weight='1/3', sites=[0])])
    invalid = []
    for field, value in [('m', 0), ('k', 0), ('m', 1.5), ('k', True), ('clients', {})]:
        obj = copy.deepcopy(valid)
        obj[field] = value
        invalid.append(obj)
    for weight in ['0', '-1', '1/0', 1.5, True]:
        obj = copy.deepcopy(valid)
        obj['clients'][0]['weight'] = weight
        invalid.append(obj)
    for sites in [[-1], [2], [0.5], [True], '0']:
        obj = copy.deepcopy(valid)
        obj['clients'][0]['sites'] = sites
        invalid.append(obj)
    rejected = 0
    for obj in invalid:
        try:
            Instance.from_json(obj)
        except (ValueError, TypeError, ZeroDivisionError):
            rejected += 1
    assert rejected == len(invalid)
    # A declaration of a different default is not the proved certificate schema.
    altered = copy.deepcopy(certificate)
    altered['default_rule'] = 'arbitrary unverified behavior'
    try:
        check_certificate(altered)
    except AssertionError:
        pass
    else:
        raise AssertionError('Invalid default declaration accepted')
    code_hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    return dict(schema_version=1, claim='SC-K-2-E', python_version=platform.python_version(),
                observed_upstream_main='d196aa294cd2ef6feb75fe1e72f2593029879dab',
                upstream_observation='public commit/main.patch, not a Git fetch',
                source_sha256=code_hashes, frozen_replays=frozen,
                compiled_files=len(sources), saved_certificates_verified=certs,
                complete_rule_layout_evaluations=complete_evaluations,
                default_rule_evaluations=default_evaluations,
                malformed_inputs_rejected=rejected, additional_bad_default_rejected=1,
                CLI='exact witness verified; overwriting existing output refused',
                limitations=['Finite checks are not a general proof.',
                    'No polynomial-time claim.', 'No external peer review or novelty certification.',
                    'Original repository structural checks and old regressions were not run.',
                    'This script does not fetch or push upstream; initial delivery Git access failed.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an existing validation record')
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'source_sha256'}, indent=2))
