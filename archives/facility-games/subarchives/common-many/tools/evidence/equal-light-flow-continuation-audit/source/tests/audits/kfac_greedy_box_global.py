"""Independent exact attacks and end-to-end greedy-box continuation checks.

Finite checks support the implementation, not the universal proof. The NE
oracle imports no constructor. Defaults are evaluated at their actual labeled
layouts and checked by the original conditional-cost definition.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
from random import Random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests/multi_facility'))
from definition_check import check_certificate, check_ne
from multi_facility_spe.greedy_box import construct, construct_on_path, verify_on_path
from multi_facility_spe.two_exists import Instance, evaluate_continuation


def greedy_reference(obj):
    """Definition-level insertion replay, independent of production greedy."""
    q = Counter()
    home = [-1] * len(obj['clients'])
    weights = [F(c['weight']) for c in obj['clients']]
    layout = []
    last = F(0)
    for _ in range(obj['k']):
        candidates = []
        for t in range(obj['m']):
            if q[t]:
                pool = sum((w for i, w in enumerate(weights) if home[i] == t), F(0))
                score = pool / (q[t] + 1)
            else:
                score = sum((w for i, w in enumerate(weights)
                             if home[i] < 0 and t in obj['clients'][i]['sites']), F(0))
            candidates.append((score, -t))
        last, neg_t = max(candidates)
        t = -neg_t
        if not q[t]:
            for i, c in enumerate(obj['clients']):
                if home[i] < 0 and t in c['sites']:
                    home[i] = t
        q[t] += 1
        layout.append(t)
    return tuple(layout), tuple(home), last


def check_box_interface(cert):
    obj = cert['instance']
    layout, home, gamma = greedy_reference(obj)
    assert tuple(cert['on_path']['layout']) == layout
    assignment = cert['on_path']['site_assignment']
    probabilities = cert['on_path']['probabilities']
    check_ne(obj, layout, probabilities)
    for t in set(layout):
        mass = sum((F(c['weight']) for i, c in enumerate(obj['clients'])
                    if assignment[i] == t), F(0))
        assert layout.count(t) * gamma <= mass <= (layout.count(t) + 1) * gamma
    if not gamma:
        assert all(not c['sites'] for c in obj['clients'])
        return
    for i, c in enumerate(obj['clients']):
        occupied_options = set(c['sites']) & set(layout)
        if not occupied_options:
            assert assignment[i] == -1
            continue
        w = F(c['weight'])
        if w >= gamma or len(occupied_options) == 1:
            assert assignment[i] == home[i]
        else:
            s = assignment[i]
            mass = sum((F(row['weight']) for j, row in enumerate(obj['clients'])
                        if assignment[j] == s), F(0))
            assert (mass - w) / layout.count(s) - gamma <= (gamma - w) / layout.count(home[i])


def abstract_potential(q, c, w, menus, a):
    home = tuple(min(v) for v in menus)
    x = list(c)
    for i, z in enumerate(w):
        x[home[i]] -= z
        x[a[i]] += z
    r = tuple((1 - z) / q[home[i]] for i, z in enumerate(w))
    result = []
    for level in sorted(set(r)):
        result.extend(sorted(min(x[t] / q[t], level) for t in range(len(q))))
        result.append(-sum(a[i] != home[i] for i in range(len(w)) if r[i] == level))
    return tuple(result), tuple(x), r, home


def abstract_attacks():
    counts = Counter()
    for n in range(3):
        for q in ((3, 2), (2, 2), (1, 1)):
            for c in product((F(0), F(1, 2), F(1)), repeat=2):
                for w in product((F(1, 4), F(3, 4)), repeat=n):
                    for menus in product(((0,), (1,), (0, 1)), repeat=n):
                        counts['abstract_inputs'] += 1
                        for a in product(*menus):
                            before, x, r, home = abstract_potential(q, c, w, menus, a)
                            if min(x) < 0:
                                continue
                            counts['abstract_nonnegative_states'] += 1
                            counts['abstract_overflow_states'] += max(x) > 1
                            for i, s in enumerate(a):
                                e = (x[s] - w[i]) / q[s]
                                if e <= r[i]:
                                    for t in menus[i]:
                                        if x[t] / q[t] < e:
                                            b = list(a); b[i] = t
                                            after, y, _, _ = abstract_potential(q, c, w, menus, b)
                                            assert min(y) >= 0 and after > before
                                            counts['H_improvement_attacks'] += 1
                                elif s != home[i]:
                                    b = list(a); b[i] = home[i]
                                    after, y, _, _ = abstract_potential(q, c, w, menus, b)
                                    assert min(y) >= 0 and after > before
                                    counts['foreign_return_attacks'] += 1
    # A real boundary: an H-violating improver can decrease the new potential.
    q, c = (1, 1, 1), (F(1),) * 3
    w, menus = (F(1, 10), F(1, 4)), ((1, 2), (0, 1))
    a, b = (1, 1), (2, 1)
    before, x, r, _ = abstract_potential(q, c, w, menus, a)
    after, _, _, _ = abstract_potential(q, c, w, menus, b)
    assert (x[1] - w[0]) > r[0] and x[2] < x[1] - w[0] and after < before
    counts['omitted_H_guard_counterexamples'] = 1
    return counts


def cases(seed, random_cases):
    masks = ((), (0,), (1,), (0, 1))
    for k in (2, 3, 4):
        for weights in product((1, 2, 5), repeat=2):
            for menus in product(masks, repeat=2):
                yield dict(m=2, k=k, clients=[dict(weight=str(w), sites=list(a))
                                               for w, a in zip(weights, menus)]), True
    specials = [
        dict(m=3, k=3, clients=[]),
        dict(m=3, k=3, clients=[dict(weight='7/11', sites=[])]),
        dict(m=1, k=7, clients=[dict(weight='100', sites=[0]), dict(weight='1/7', sites=[0])]),
        dict(m=3, k=1, clients=[dict(weight='3', sites=[0]), dict(weight='7', sites=[1])]),
        json.loads((ROOT / 'examples/multi_facility/rational.json').read_text()),
        json.loads((ROOT / 'examples/multi_facility/greedy_box_global.json').read_text()),
    ]
    for obj in specials:
        yield obj, obj['k'] <= 4 and obj['m'] <= 3
    rng = Random(seed)
    for trial in range(random_cases):
        m, k, n = rng.randrange(2, 6), rng.randrange(2, 9), rng.randrange(1, 11)
        obj = dict(m=m, k=k, clients=[
            dict(weight=str(F(rng.randrange(1, 41), rng.choice((1, 2, 7, 19)))),
                 sites=[t for t in range(m) if rng.randrange(3)]) for _ in range(n)])
        yield obj, trial < 15 and m <= 3 and k <= 4


def run(random_cases=90):
    seed = 2026100703
    counts = abstract_attacks()
    max_ratio = F(1)
    rng = Random(seed + 1)
    for obj, full in cases(seed, random_cases):
        cert = construct(Instance.from_json(obj))
        check_box_interface(cert)
        checked = check_certificate(cert)
        counts['complete_certificates'] += 1
        counts['actual_labeled_deviations'] += checked['actual_deviations_checked']
        max_ratio = max(max_ratio, F(checked['actual_certificate_factor']))
        audit = cert['greedy_box_audit']
        assert audit['every_microstep_potential_checked']
        assert audit['microsteps'] <= int(audit['assignment_move_bound'])
        counts['on_path_microsteps'] += audit['microsteps']
        counts['home_return_microsteps'] += audit['home_returns']
        for d in cert['deviations']:
            counts['singleton_resets'] += d['audit']['singleton_reset']
            counts['nonsingleton_completions'] += not d['audit']['singleton_reset']
            counts['occupied_target_completions'] += d['site'] in cert['on_path']['layout']
            counts['unopened_target_completions'] += d['site'] not in cert['on_path']['layout']
        if full:
            layouts = product(range(obj['m']), repeat=obj['k'])
        else:
            layouts = [tuple(rng.randrange(obj['m']) for _ in range(obj['k'])) for _ in range(3)]
        on_path = tuple(cert['on_path']['layout'])
        for layout in layouts:
            check_ne(obj, layout, evaluate_continuation(cert, layout))
            counts['complete_rule_layout_evaluations'] += 1
            if sum(s != t for s, t in zip(layout, on_path)) >= 2:
                counts['default_rule_evaluations'] += 1
    fixture = json.loads((ROOT / 'examples/multi_facility/greedy_box_global.json').read_text())
    inst = Instance.from_json(fixture)
    layout, a, audit = construct_on_path(inst)
    assert F(audit['gamma']) == 1
    assert audit['home_returns'] == 2 and audit['strict_improvements'] == 3
    bad = list(a); bad[5] = 4  # Inaccessible destination; verifier must reject it.
    try:
        verify_on_path(inst, layout, bad)
    except ValueError:
        counts['invalid_on_path_rejected'] += 1
    else:
        raise AssertionError('Verifier accepted an inaccessible assignment')
    with tempfile.TemporaryDirectory(prefix='greedy-box-test-') as tempdir:
        output = Path(tempdir) / 'certificate.json'
        command = [sys.executable, '-m', 'multi_facility_spe',
                   str(ROOT / 'examples/multi_facility/greedy_box_global.json'),
                   '--method', 'greedy-box', '--output', str(output)]
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
        check_certificate(json.loads(output.read_text()))
        assert subprocess.run(command, cwd=ROOT, capture_output=True).returncode != 0
        counts['CLI_success_and_overwrite_refusal'] = 1
    paths = ['multi_facility_spe/greedy_box.py', 'multi_facility_spe/two_exists.py',
             'tests/audits/kfac_greedy_box_global.py', 'tests/multi_facility/definition_check.py',
             'examples/multi_facility/greedy_box_global.json']
    return dict(schema_version=1, status='all_passed', seed=seed,
                claims=['SC-K-GREEDY-BOX-EXISTS', 'SC-K-GREEDY-BOX-FINITE-2'],
                counts=dict(counts), largest_verified_factor=str(max_ratio),
                source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
                limitations=['Finite checks are not a universal proof.',
                             'The pasted Pro ZIP and its reported tests were not obtained.',
                             'No OpenAI mathematics-catalogue theorem is used.',
                             'General polynomial total time is unproved.',
                             'Executable off-path repair is finite pure best response, not the imported polynomial scheduler.',
                             'No external peer review or literature-priority certification.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--random-cases', type=int, default=90)
    args = parser.parse_args()
    if args.random_cases < 0:
        parser.error('random-cases must be nonnegative')
    if args.output and args.output.exists():
        parser.error('Refusing to overwrite frozen evidence')
    result = run(args.random_cases)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'source_sha256'}, indent=2))


if __name__ == '__main__':
    main()
