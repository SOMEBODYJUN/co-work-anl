#!/usr/bin/env python3
"""相同机器的工作量守恒、真实凸包槽输出与循环优化器的衔接审计。

The source family and convex decomposition are boss7's
UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1. This checks a direct corollary, not a new family.
Prints a fresh record; never overwrites evidence. No floating-point arithmetic.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import sys

ROOT = Path(__file__).resolve().parents[3]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def independent_loads(times, sigma, m):
    values = [F(0)]*m
    for p, i in zip(times, sigma):
        values[i] += p
    return tuple(values)


def main():
    baseline = module('bridge_baseline', 'tests/audits/unrelated_machines/rounding_and_gap.py')
    local = module('bridge_local', 'tests/audits/unrelated_machines/cyclic_batch_repair.py')
    rows = []
    for m in range(2, 9):
        n = m*m
        times = [F(1)]+[F(1, m+1)]*(n-1)
        p = [list(times) for _ in range(m)]
        x = [[F(1, m)]*n for _ in range(m)]
        # Explicit true OPT components, independently of the slot matcher.
        components = []
        for shift in range(m):
            assignment = [shift]+[(shift+1+(j-1)//(m+1)) % m for j in range(1, n)]
            assert independent_loads(times, assignment, m) == (F(1),)*m
            components.append(assignment)
        for i in range(m):
            for j in range(n):
                assert F(sum(s[j] == i for s in components), m) == x[i][j]
        sigma, reported = baseline.round_slots(p, x, F(1))
        initial = independent_loads(times, sigma, m)
        assert tuple(reported) == initial
        assert sum(initial) == m
        assert max(initial) == F(2*m, m+1)
        end, info = local.optimize(p, sigma, F(1), F(1, 4))
        assert end == tuple(sigma) and info['iterations'] == 0
        # A direct schedule oracle, not the local implementation's criterion.
        count = same_work = nonincreasing = 0
        if m <= 3:
            for assignment in product(range(m), repeat=n):
                actual = independent_loads(times, assignment, m)
                assert sum(actual) == m
                count += 1
                same_work += 1
                if all(a <= b for a, b in zip(actual, initial)):
                    assert actual == initial
                    nonincreasing += 1
        # The allowed relaxed move really needs a receiver to increase.
        high = max(range(m), key=lambda i: initial[i])
        light = next(i for i in range(m) if i != high)
        j = next(j for j in range(1, n) if sigma[j] == high)
        one_move = list(sigma)
        one_move[j] = light
        changed = independent_loads(times, one_move, m)
        assert max(changed) < max(initial) and changed[light] > initial[light]
        rows.append({'m': m, 'n': n, 'initial_makespan': str(max(initial)),
                     'true_OPT': '1', 'sum_work': str(sum(initial)),
                     'optimizer_iterations': info['iterations'],
                     'independent_assignments': count,
                     'same_work_checks': same_work,
                     'coordinate_nonincreasing_load_equal_assignments': nonincreasing,
                     'one_move_makespan': str(max(changed))})
    sources = ['tests/audits/unrelated_machines/rounding_and_gap.py',
               'tests/audits/unrelated_machines/cyclic_batch_repair.py',
               'research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md']
    print(json.dumps({'status': 'passed', 'python': platform.python_version(),
          'arithmetic': 'fractions.Fraction', 'randomness': 'none',
          'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'dependencies_sha256': {s: hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in sources},
          'cases': rows,
          'limitations': ['Finite audits do not prove the invariant for every input.',
                         'The arbitrary-m identity is proved in the mathematical account.',
                         'Family/convex decomposition is reused from boss7, not claimed new.',
                         'This does not extend the separate one-destination fork obstruction to configuration-derived initialization.']},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
