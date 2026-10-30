"""Independent original-model checks of the connected equal-light flow rule.

The definition-level checker imports no solver. Full/default continuations
are evaluated at their actual labeled layouts. Finite checks do not replace
the universal proof or implement the imported polynomial off-path scheduler.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
from random import Random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from multi_facility_spe.greedy_box import construct
from multi_facility_spe.two_exists import Instance, evaluate_continuation
from tests.multi_facility.definition_check import check_certificate, check_ne
from tests.audits.kfac_greedy_box_global import check_box_interface


def inputs(seed, random_cases):
    yield json.loads((ROOT / 'examples/multi_facility/equal_light_flow_complete.json').read_text())
    for k, x, y, n, delta in product(range(2, 5), ('1/2', '1', '3/2'),
                                    ('1/2', '1', '3/2'), range(4), ('1/4', '1/3')):
        yield dict(m=2, k=k, clients=[dict(weight=x, sites=[0]), dict(weight=y, sites=[1])]
                   + [dict(weight=delta, sites=[0, 1]) for _ in range(n)])
    yield dict(m=2, k=3, clients=[])
    yield dict(m=2, k=3, clients=[dict(weight='1/7', sites=[])])
    yield dict(m=1, k=2, clients=[dict(weight='1', sites=[0])])
    yield dict(m=3, k=3, clients=[dict(weight='1/5', sites=[0, 1, 2]) for _ in range(4)])
    rng = Random(seed)
    for _ in range(random_cases):
        m, k = rng.randint(2, 4), rng.randint(2, 6)
        clients = [dict(weight=str(rng.randint(1, 6)), sites=[t]) for t in range(m)]
        for _ in range(rng.randint(0, 5)):
            sites = [t for t in range(m) if rng.randrange(2)]
            clients.append(dict(weight='1/4', sites=sites))
        clients.append(dict(weight='12', sites=list(range(m))))
        yield dict(m=m, k=k, clients=clients)


def run(random_cases=80, seed=2026100709):
    counts = Counter()
    largest = F(1)
    for obj in inputs(seed, random_cases):
        cert = construct(Instance.from_json(obj), on_path_method='equal-light-flow')
        certificate_check = check_certificate(cert)
        largest = max(largest, F(certificate_check['actual_certificate_factor']))
        check_box_interface(cert)
        audit = cert['greedy_box_audit']
        n = len(audit['variable_clients'])
        assert audit['flow_solution']['augmentations'] == n
        counts['certificates'] += 1
        counts['movable_customers'] += n
        counts['unit_augmentations'] += n
        counts['actual_labeled_deviations'] += len(cert['deviations'])
        layout = tuple(cert['on_path']['layout'])
        for row in cert['deviations']:
            counts['singleton_original_pool_resets' if row['audit']['singleton_reset']
                   else 'surviving_source_completions'] += 1
            counts['occupied_targets' if row['site'] in layout
                   else 'unopened_targets'] += 1
        explicit = {layout}
        for row in cert['deviations']:
            changed = list(layout)
            changed[row['facility']] = row['site']
            explicit.add(tuple(changed))
        if obj['m'] ** obj['k'] <= 243:
            for target_layout in product(range(obj['m']), repeat=obj['k']):
                check_ne(obj, target_layout, evaluate_continuation(cert, target_layout))
                counts['complete_rule_layout_evaluations'] += 1
                if target_layout not in explicit:
                    counts['default_layout_evaluations'] += 1
    # Unequal movable weights must fail before a certificate file is created.
    bad = ROOT / 'examples/multi_facility/greedy_box_global.json'
    try:
        construct(Instance.from_json(json.loads(bad.read_text())),
                  on_path_method='equal-light-flow')
    except ValueError:
        counts['unequal_movable_instance_rejected'] += 1
    else:
        raise AssertionError('Unequal movable weights silently fell back')
    with tempfile.TemporaryDirectory(prefix='equal-flow-cli-', dir=ROOT.parent) as d:
        output = Path(d) / 'certificate.json'
        cmd = [sys.executable, '-m', 'multi_facility_spe',
               str(ROOT / 'examples/multi_facility/equal_light_flow_complete.json'),
               '--method', 'equal-light-flow', '--output', str(output)]
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True)
        check_certificate(json.loads(output.read_text()))
        assert subprocess.run(cmd, cwd=ROOT, capture_output=True).returncode != 0
        counts['CLI_success_and_overwrite_refusal'] = 1
        rejected = Path(d) / 'rejected.json'
        bad_cmd = [sys.executable, '-m', 'multi_facility_spe', str(bad),
                   '--method', 'equal-light-flow', '--output', str(rejected)]
        assert subprocess.run(bad_cmd, cwd=ROOT, capture_output=True).returncode != 0
        assert not rejected.exists()
        counts['CLI_unequal_rejection_without_output'] = 1
    paths = ['multi_facility_spe/equal_light_flow.py', 'multi_facility_spe/greedy_box.py',
             'multi_facility_spe/__main__.py', 'multi_facility_spe/two_exists.py',
             'tests/audits/kfac_equal_light_flow_continuation.py',
             'tests/multi_facility/definition_check.py',
             'tests/audits/kfac_greedy_box_global.py',
             'examples/multi_facility/equal_light_flow_complete.json']
    return dict(schema_version=1, status='all_passed', seed=seed,
                random_cases=random_cases, counts=dict(counts),
                largest_verified_factor=str(largest),
                source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                               for p in paths},
                limitations=['Finite original-definition checks are not a universal proof.',
                             'The equal-light original-model subclass was already mathematically covered.',
                             'Only the on-path flow implementation is bit-polynomial.',
                             'Off-path and default code still use finite pure improvements.',
                             'No external review or general unequal-movable-weight polynomial-time result.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--random-cases', type=int, default=80)
    args = parser.parse_args()
    if args.random_cases < 0:
        parser.error('random-cases must be nonnegative')
    if args.output and args.output.exists():
        parser.error('Refusing to overwrite a frozen record')
    report = run(args.random_cases)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'source_sha256'}, indent=2))
