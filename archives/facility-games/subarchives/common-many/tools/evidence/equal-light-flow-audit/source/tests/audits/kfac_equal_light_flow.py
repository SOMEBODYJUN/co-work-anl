"""Independent exact enumeration audit for the equal movable-weight flow.

The oracle imports neither production validation nor production certificates.
It enumerates ALL legal assignments before testing every global minimizer for
the box, H, and deviations to every original menu option.  These finite checks
support the implementation; they do not establish a universal theorem.

Run: python3 tests/audits/kfac_equal_light_flow.py --output NEW_REPORT.json
Existing outputs are never overwritten.
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


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
SEED = 20261007
FIXTURE_PATHS = (
    'examples/multi_facility/equal_light_flow_rerouting.json',
    'examples/multi_facility/equal_light_flow_negative_base.json',
    'examples/multi_facility/equal_light_flow_ties.json',
    'examples/multi_facility/equal_light_flow_binary_q.json',
)


def _rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError('The independent oracle requires exact rational input')
    try:
        if isinstance(value, str) and len(value) > 4000:
            # Output denominators can exceed Python's decimal digit ceiling.
            # Parse independently in short chunks without changing process state.
            def integer(text):
                sign = -1 if text.startswith('-') else 1
                digits = text[1:] if text[:1] in ('+', '-') else text
                if not digits or any(ch not in '0123456789' for ch in digits):
                    raise ValueError('Invalid decimal integer')
                result = 0
                for start in range(0, len(digits), 9):
                    chunk = digits[start:start + 9]
                    result = result * (10 ** len(chunk)) + int(chunk)
                return sign * result
            parts = value.strip().split('/')
            if len(parts) == 1:
                return F(integer(parts[0]))
            if len(parts) == 2:
                return F(integer(parts[0]), integer(parts[1]))
            raise ValueError('Invalid rational fraction')
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('Invalid exact rational') from exc


def _normalize(q, c, w, A):
    """Small definition-level parser, independent of the constructor."""
    q, c, w = tuple(q), tuple(map(_rational, c)), tuple(map(_rational, w))
    if len(q) != len(c) or len(w) != len(A):
        raise ValueError('Dimension mismatch')
    if any(type(v) is not int or v <= 0 for v in q):
        raise ValueError('Invalid facility multiplicity')
    if any(q[t] < q[t + 1] for t in range(len(q) - 1)):
        raise ValueError('Multiplicities are not nonincreasing')
    if any(v < 0 or v > 1 for v in c):
        raise ValueError('Invalid initial slack')
    if any(v <= 0 or v >= 1 for v in w) or len(set(w)) > 1:
        raise ValueError('Weights must be equal and strictly between zero and one')
    menus = []
    for row in A:
        row = tuple(row)
        if not row or any(type(t) is not int or t < 0 or t >= len(q) for t in row):
            raise ValueError('Invalid original menu')
        menus.append(tuple(sorted(set(row))))
    return q, c, w, tuple(menus)


def assignment_values(q, c, w, menus, assignment):
    """Compute loads by individual transfers and Psi by marginal slot sums."""
    if len(assignment) != len(w):
        raise AssertionError('Incomplete assignment')
    loads = list(c)
    home_counts = [0] * len(q)
    destination_counts = [0] * len(q)
    for i, site in enumerate(assignment):
        if type(site) is not int or site not in menus[i]:
            raise AssertionError('Assignment uses an option outside the original menu')
        home = min(menus[i])
        home_counts[home] += 1
        destination_counts[site] += 1
        loads[home] -= w[i]
        loads[site] += w[i]
    delta = w[0] if w else F(1, 2)
    # Deliberately sum marginal costs; do not call production objective helpers.
    value = sum(((c[t] + delta * (slot - home_counts[t])) / q[t]
                 for t in range(len(q))
                 for slot in range(destination_counts[t])), F(0))
    return tuple(loads), value


def check_properties(q, w, menus, assignment, loads):
    """Check all original options, including deviations that leave the box."""
    assert all(F(0) <= x <= F(1) for x in loads), 'Full-box inequality failed'
    checked = 0
    for i, site in enumerate(assignment):
        external = (loads[site] - w[i]) / q[site]
        assert external <= (1 - w[i]) / q[min(menus[i])], 'H inequality failed'
        for target in menus[i]:
            assert external <= loads[target] / q[target], 'Original-menu NE failed'
            checked += 1
    return checked


def enumerate_minimizers(q, c, w, A):
    """Enumerate the unconstrained domain, then check EVERY global minimum."""
    q, c, w, menus = _normalize(q, c, w, A)
    minimum, minimizers, assignment_count = None, [], 0
    outside_box_count = 0
    for assignment in product(*menus):
        loads, value = assignment_values(q, c, w, menus, assignment)
        assignment_count += 1
        outside_box_count += any(x < 0 or x > 1 for x in loads)
        if minimum is None or value < minimum:
            minimum, minimizers = value, [(assignment, loads)]
        elif value == minimum:
            minimizers.append((assignment, loads))
    assert minimum is not None  # product over no customers contains the empty tuple.
    deviation_count = sum(check_properties(q, w, menus, a, loads)
                          for a, loads in minimizers)
    return dict(minimum=minimum, minimizers=tuple(a for a, _ in minimizers),
                assignment_count=assignment_count,
                outside_box_assignment_count=outside_box_count,
                original_options_checked=deviation_count)


def audit_instance(obj, solver=None):
    if solver is None:
        from multi_facility_spe.equal_light_flow import equal_weight_box_ne
        solver = equal_weight_box_ne
    oracle = enumerate_minimizers(**obj)
    result = solver(**obj)
    q, c, w, menus = _normalize(**obj)
    assignment = tuple(result['assignment'])
    assert assignment in oracle['minimizers'], 'Solver did not return a global minimum'
    loads, value = assignment_values(q, c, w, menus, assignment)
    assert isinstance(result['objective'], str)
    assert all(isinstance(x, str) for x in result['X'])
    assert tuple(map(_rational, result['X'])) == loads, 'Reported loads are incorrect'
    assert _rational(result['objective']) == value == oracle['minimum']
    assert type(result['augmentations']) is int and result['augmentations'] == len(w)
    check_properties(q, w, menus, assignment, loads)
    return oracle, result


def rerouting_fixture():
    """The third augmentation reroutes two previously assigned customers."""
    return dict(q=[1, 1, 1], c=['1/2', '1/4', '0'], w=['1/4'] * 3,
                A=[[0, 1], [1, 2], [0]])


def fixed_cases():
    yield 'grid_empty', dict(q=[], c=[], w=[], A=[])
    specifications = (
        (1, ((1,), (2,), (7,)), ('0', '1/2', '1'), ('1/3', '1/2', '2/3'), 4),
        (2, ((1, 1), (2, 2), (3, 1)), ('0', '1/2', '1'), ('1/3', '1/2', '2/3'), 3),
        (3, ((1, 1, 1), (3, 2, 1)), ('0', '1'), ('1/3', '2/3'), 2),
    )
    for m, multiplicities, slacks, deltas, max_n in specifications:
        menus = tuple(tuple(t for t in range(m) if mask & (1 << t))
                      for mask in range(1, 1 << m))
        for q in multiplicities:
            for c in product(slacks, repeat=m):
                yield f'grid_m{m}', dict(q=list(q), c=list(c), w=[], A=[])
                for n in range(1, max_n + 1):
                    for delta in deltas:
                        for A in product(menus, repeat=n):
                            yield f'grid_m{m}', dict(q=list(q), c=list(c), w=[delta] * n,
                                                   A=[list(row) for row in A])


def special_cases():
    yield 'negative_b', dict(q=[7, 3, 1], c=['0', '0', '0'], w=['3/4'] * 4,
                             A=[[0, 1, 2], [0, 2], [1, 2], [0]])
    yield 'ties', dict(q=[1, 1], c=['1', '0'], w=['1/2'] * 2,
                      A=[[0, 1], [0, 1]])
    yield 'duplicates_and_order', dict(q=[2, 1], c=['3/4', '0'], w=['1/4'] * 2,
                                      A=[[1, 0, 1], [0, 1, 0]])
    yield 'large_denominators', dict(q=[17, 11, 1],
                                    c=['1/170141183460469231731687303715884105727',
                                       '1', '1/618970019642690137449562111'],
                                    w=['1/162259276829213363391578010288127'] * 4,
                                    A=[[0, 1], [0, 2], [1, 2], [0, 1, 2]])
    yield 'large_binary_q', dict(q=[(1 << 20000) + 1, 1 << 8192, 1],
                                c=['1/2', '1/3', '2/3'], w=['2/7'] * 3,
                                A=[[0, 1], [1, 2], [0, 1, 2]])
    yield 'multiple_reverse_reroutes', rerouting_fixture()


def seeded_cases(seed=SEED, count=120):
    rng = Random(seed)
    for _ in range(count):
        m = rng.randrange(1, 6)
        n = rng.randrange(0, 7)
        denominator = rng.choice((2, 3, 7, 19, 97))
        delta = F(rng.randrange(1, denominator), denominator)
        q = sorted((rng.randrange(1, 18) for _ in range(m)), reverse=True)
        c = [str(F(rng.randrange(20), 19)) for _ in range(m)]
        A = []
        for _i in range(n):
            row = [t for t in range(m) if rng.randrange(2)]
            A.append(row or [rng.randrange(m)])
        yield dict(q=q, c=c, w=[str(delta)] * n, A=A)


def invalid_cases():
    base = dict(q=[2, 1], c=['1/2', '0'], w=['1/3'], A=[[0, 1]])
    updates = (
        ('dimension_c', {'c': ['0']}), ('dimension_A', {'A': []}),
        ('q_zero', {'q': [2, 0]}), ('q_negative', {'q': [2, -1]}),
        ('q_unsorted', {'q': [1, 2]}), ('q_bool', {'q': [2, True]}),
        ('q_float', {'q': [2, 1.0]}), ('q_fraction', {'q': [2, F(1)]}),
        ('q_string', {'q': [2, '1']}),
        ('c_negative', {'c': ['-1/3', '0']}), ('c_large', {'c': ['4/3', '0']}),
        ('c_float', {'c': [0.5, '0']}), ('c_bool', {'c': [True, '0']}),
        ('c_bad_string', {'c': ['x', '0']}), ('c_zero_denominator', {'c': ['1/0', '0']}),
        ('w_zero', {'w': ['0']}), ('w_one', {'w': ['1']}),
        ('w_negative', {'w': ['-1/3']}), ('w_large', {'w': ['4/3']}),
        ('w_bool', {'w': [True]}), ('w_float', {'w': [0.5]}),
        ('w_bad_string', {'w': ['x']}), ('w_zero_denominator', {'w': ['1/0']}),
        ('w_unequal', {'w': ['1/3', '1/2'], 'A': [[0, 1], [0, 1]]}),
        ('menu_empty', {'A': [[]]}), ('menu_negative', {'A': [[-1, 0]]}),
        ('menu_large', {'A': [[0, 2]]}), ('menu_bool', {'A': [[False, 1]]}),
        ('menu_float', {'A': [[0.0, 1]]}), ('menu_fraction', {'A': [[F(0), 1]]}),
        ('menu_string', {'A': [['0', 1]]}),
        ('nonempty_without_sites', {'q': [], 'c': [], 'A': [[]]}),
    )
    for name, change in updates:
        yield name, {**base, **change}


def run(random_cases=120):
    """Return a deterministic, JSON-serializable finite audit report."""
    if type(random_cases) is not int or random_cases < 0:
        raise ValueError('random_cases must be a nonnegative integer')
    from multi_facility_spe.equal_light_flow import equal_weight_box_ne
    counts, groups = Counter(), Counter()
    fixtures = {path: json.loads((ROOT / path).read_text(encoding='utf-8'))
                for path in FIXTURE_PATHS}
    specials = list(special_cases())
    records = list(fixed_cases()) + specials
    records.extend(('canonical_fixture', obj) for obj in fixtures.values())
    records.extend(('seeded_random', obj) for obj in seeded_cases(count=random_cases))
    for group, obj in records:
        oracle, result = audit_instance(obj, equal_weight_box_ne)
        counts['instances'] += 1
        groups[group] += 1
        counts['legal_assignments'] += oracle['assignment_count']
        counts['outside_box_assignments_in_optimization_domain'] += oracle['outside_box_assignment_count']
        counts['global_minimizers_checked'] += len(oracle['minimizers'])
        counts['all_original_options_checked_at_minimizers'] += oracle['original_options_checked']
        counts['solver_augmentations'] += result['augmentations']
        counts['instances_with_multiple_global_minimizers'] += len(oracle['minimizers']) > 1
        if group == 'multiple_reverse_reroutes':
            assert result['reverse_assignment_traversals'] >= 2
            assert result['max_assignment_reroutes_per_augmentation'] >= 2
            counts['multiple_reverse_reroute_fixtures'] += 1
    for name, obj in invalid_cases():
        try:
            equal_weight_box_ne(**obj)
        except ValueError:
            counts['invalid_inputs_rejected'] += 1
        else:
            raise AssertionError(f'Invalid input accepted: {name}')
    paths = ('multi_facility_spe/equal_light_flow.py',
             'tests/audits/kfac_equal_light_flow.py', 'tests/test_equal_light_flow.py',
             'history/source/notes/multi_facility/equal_light_flow_pro_report_2026-10-07.md',
             *FIXTURE_PATHS)
    return dict(
        schema_version=1, status='all_passed', seed=SEED,
        audit='independent_equal_movable_weight_global_minima',
        repository_head_at_run=subprocess.run(
            ['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
            capture_output=True, text=True).stdout.strip(),
        source_identity='Hashes identify the audited working-tree bytes; HEAD does not assert a clean tree.',
        python_version=sys.version.split()[0],
        parameters=dict(
            random_cases=random_cases,
            grid=[dict(m=0, n=[0]),
                  dict(m=1, q=[[1], [2], [7]], c_values=['0', '1/2', '1'],
                       delta_values=['1/3', '1/2', '2/3'], n=[0, 1, 2, 3, 4]),
                  dict(m=2, q=[[1, 1], [2, 2], [3, 1]], c_values=['0', '1/2', '1'],
                       delta_values=['1/3', '1/2', '2/3'], n=[0, 1, 2, 3]),
                  dict(m=3, q=[[1, 1, 1], [3, 2, 1]], c_values=['0', '1'],
                       delta_values=['1/3', '2/3'], n=[0, 1, 2])],
            grid_menus='All nonempty subsets, independently for each labeled customer',
            empty_customer_grid='One case per q,c pair; no redundant delta choices',
            random_generator=dict(m_range=[1, 5], n_range=[0, 6], q_range=[1, 17],
                                  c_grid_denominator=19,
                                  delta_denominators=[2, 3, 7, 19, 97],
                                  menus='Independent fair site inclusion; empty replaced by a random singleton'),
            special_q_encoding='q_hex entries are exact Python hexadecimal integers; decode with int(value, 16)',
            special_inputs=[dict(name=name, q_hex=[hex(q) for q in obj['q']],
                                 c=obj['c'], w=obj['w'], A=obj['A'])
                            for name, obj in specials],
            optimization_domain='All original legal assignments, without box or H prefiltering'),
        counts=dict(counts), instance_groups=dict(groups),
        fixture_inputs=fixtures,
        source_sha256={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                       for path in paths},
        limitations=['Finite enumeration is not a universal proof or a runtime complexity proof.',
                     'All counts were reproduced by this checked-in audit; pasted ZIP counts are not reused.',
                     'The source ZIP was not supplied; this is an independent reconstruction.',
                     'SC-K-UNIFORM-LIGHT-FLOW-2 already covered this equal-weight multi-facility subclass; no first-discovery claim is made.',
                     'The new checked scope is the unconstrained all-minimizer box/H property and the canonical n-augmentation integer-cost flow implementation.',
                     'Only equal movable weights are supported; general unequal-weight polynomial time remains open.',
                     'No external peer review or literature-priority certification.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--random-cases', type=int, default=120)
    args = parser.parse_args()
    if args.random_cases < 0:
        parser.error('random-cases must be nonnegative')
    if args.output and args.output.exists():
        parser.error('Refusing to overwrite an existing audit report')
    report = run(random_cases=args.random_cases)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects against an output appearing mid-audit.
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
