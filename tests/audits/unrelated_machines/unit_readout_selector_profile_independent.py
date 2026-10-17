#!/usr/bin/env python3
"""Independent explicit p=1..4 sharp prescribed-profile certificates.

No repository or other scratch code is imported.  The checker reads the
serialized original machine-by-job matrix, checks every finite edge and
all actual schedules, and verifies the exact profile lower bound by the
root/clause integer count.  It does not enumerate all assignments.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import platform


def make_case(count):
    k = 2 * count - 1
    roots = 2 * count
    positive_units = list(range(roots, roots + k))
    negative_units = list(range(roots + k, roots + count * k))
    m = roots + count * k
    n = count + 2 * count * k
    matrix = [[None] * n for _ in range(m)]
    for v in range(count):
        matrix[2 * v][v] = matrix[2 * v + 1][v] = Fraction(1)
    for v in range(count):
        for sign in (0, 1):
            units = positive_units if sign == 0 else negative_units
            for leaf in range(k):
                j = count + (2 * v + sign) * k + leaf
                matrix[2 * v + sign][j] = Fraction(1, k)
                for unit in units:
                    matrix[unit][j] = Fraction(1)

    def load(sigma):
        result = [Fraction(0)] * m
        for j, i in enumerate(sigma):
            result[i] += matrix[i][j]
        return result

    yes = []
    for chosen in range(count):
        sigma = [2 * v + int(v != chosen) for v in range(count)]
        negative_next = 0
        for v in range(count):
            for sign in (0, 1):
                for leaf in range(k):
                    if sign == 0 and v == chosen:
                        sigma.append(positive_units[leaf])
                    elif sign == 1 and v != chosen:
                        sigma.append(negative_units[negative_next])
                        negative_next += 1
                    else:
                        sigma.append(2 * v + sign)
        yes.append({'positive_variable': chosen, 'sigma': sigma, 'loads': load(sigma)})
    mixed = list(range(0, 2 * count, 2))
    for v in range(count):
        for sign in (0, 1):
            for leaf in range(k):
                mixed.append(positive_units[v] if sign == 0 and leaf == 0 else 2 * v + sign)
    value = Fraction(2 * k - 1, k)
    return {'num_given_schedules': count, 'num_variables': count, 'k': k, 'h': 1,
            'num_machines': m, 'num_jobs': n,
            'clause_capacities': [k, (count - 1) * k],
            'prescribed_root_machines': list(range(0, 2 * count, 2)),
            'processing_times_machine_by_job': matrix,
            'unavailable_edge': None, 'given_yes': yes,
            'prescribed_output': {'sigma': mixed, 'loads': load(mixed)},
            'exact_prescribed_profile_optimum': value,
            'unconstrained_optimum': Fraction(1)}


def check_serialized_case(data):
    """Independently reconstruct domain and count from the full original P."""
    count = data['num_given_schedules']
    k = data['k']
    assert data['h'] == 1 and data['num_variables'] == count
    assert 1 <= count <= 4 and k == 2 * count - 1 and k >= count
    m, n = count * (2 * count + 1), count * (4 * count - 1)
    assert (data['num_machines'], data['num_jobs']) == (m, n)
    raw = data['processing_times_machine_by_job']
    assert len(raw) == m and all(len(row) == n for row in raw)
    matrix = [[None if entry is None else Fraction(entry) for entry in row] for row in raw]
    positive_units = set(range(2 * count, 2 * count + k))
    negative_units = set(range(2 * count + k, m))
    assert len(positive_units) == k and len(negative_units) == (count - 1) * k
    assert positive_units.isdisjoint(negative_units)
    finite = 0
    for j in range(n):
        actual_support = {i for i in range(m) if matrix[i][j] is not None}
        finite += len(actual_support)
        if j < count:
            assert actual_support == {2 * j, 2 * j + 1}
            assert all(matrix[i][j] == 1 for i in actual_support)
        else:
            v, local = divmod(j - count, 2 * k)
            sign, leaf = divmod(local, k)
            assert 0 <= v < count and sign in (0, 1) and 0 <= leaf < k
            parent = 2 * v + sign
            unit_set = positive_units if sign == 0 else negative_units
            assert actual_support == {parent} | unit_set
            assert matrix[parent][j] == Fraction(1, k)
            assert all(matrix[i][j] == 1 for i in unit_set)

    checked_jobs = checked_loads = 0

    def original_loads(record):
        nonlocal checked_jobs, checked_loads
        sigma = record['sigma']
        assert len(sigma) == n
        values = [Fraction(0)] * m
        for j, i in enumerate(sigma):
            assert type(i) is int and 0 <= i < m and matrix[i][j] is not None
            values[i] += matrix[i][j]
        assert list(map(Fraction, record['loads'])) == values
        checked_jobs += n
        checked_loads += m
        return sigma, values

    assert len(data['given_yes']) == count
    for chosen, record in enumerate(data['given_yes']):
        assert record['positive_variable'] == chosen
        sigma, values = original_loads(record)
        assert sigma[:count] == [2 * v + int(v != chosen) for v in range(count)]
        assert values == [Fraction(1)] * m
    sigma, values = original_loads(data['prescribed_output'])
    assert sigma[:count] == list(range(0, 2 * count, 2)) == data['prescribed_root_machines']
    bound = Fraction(2 * k - 1, k)
    assert max(values) == bound == Fraction(data['exact_prescribed_profile_optimum'])
    assert all(values[i] <= 1 for i in positive_units | negative_units)
    assert Fraction(data['unconstrained_optimum']) == 1

    # Symbolic strict-threshold lower bound, not assignment enumeration.
    # At C<bound<2 (count>=2), a positive selector root could retain at
    # most k-2 small ports, so each needs >=2 external ports in the same
    # k physical positive units.  2*count=k+1 makes this impossible.
    if count == 1:
        lower = {'kind': 'unit_selector', 'bound': '1'}
        assert bound == 1
    else:
        assert 1 < bound < 2 and k * (2 - bound) == 1
        assert 2 * count == k + 1 > len(positive_units)
        lower = {'kind': 'strict_threshold_root_and_shared_unit_count',
                 'bound': str(bound), 'external_ports_needed_per_positive_root': 2,
                 'total_external_ports_needed': 2 * count,
                 'actual_positive_unit_count': k,
                 'contradiction_margin': 2 * count - k}
    return {'status': 'passed', 'p': count, 'machines': m, 'jobs': n,
            'matrix_cells_checked': m * n, 'finite_edges_checked': finite,
            'actual_job_assignments_checked': checked_jobs,
            'actual_machine_loads_checked': checked_loads,
            'exact_profile_optimum': str(bound), 'profile_lower_certificate': lower,
            'unconstrained_optimum': '1',
            'assignment_enumeration_performed': False}


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    # Round-trip the full nullable original P before invoking the checker.
    cases = json.loads(json.dumps([make_case(p) for p in range(1, 5)], default=encode))
    checks = [check_serialized_case(case) for case in cases]
    totals = {key: sum(check[key] for check in checks) for key in
              ['matrix_cells_checked', 'finite_edges_checked',
               'actual_job_assignments_checked', 'actual_machine_loads_checked']}
    return {'status': 'passed', 'precision': 'exact Fraction; unavailable edges are null',
            'scope': 'prescribed all-positive profile only; global OPT is 1',
            'method': 'actual original P checking and symbolic integer-capacity profile lower bound',
            'assignment_enumeration_performed': False, 'checks': checks, 'totals': totals,
            'certificates': cases,
            'runtime': {'implementation': platform.python_implementation(),
                        'python_version': platform.python_version()},
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    payload = json.dumps(main(), sort_keys=True, indent=2) + '\n'
    if args.output is None:
        print(payload, end='')
    else:
        with args.output.open('x') as stream:
            stream.write(payload)
