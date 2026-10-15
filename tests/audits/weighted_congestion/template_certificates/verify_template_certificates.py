#!/usr/bin/env python3
"""Exact checks for finite-action compression and all-state selector certificates.

No LP status is accepted as evidence. Tiny test matrices use exhaustive rational
vertex enumeration; large game matrices only verify explicit certificates.
Default: stdout only. --output creates a NEW file and refuses overwriting.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = ROOT / 'examples/weighted_congestion/template_certificates/exact_fixtures.json'


def game(raw):
    weights = tuple(map(Q, raw['weights']))
    fees = tuple(tuple(map(Q, p)) for p in raw['fees'])
    strategies = tuple(tuple(frozenset(a) for a in family) for family in raw['strategies'])
    assert weights and fees and len(weights) == len(strategies)
    assert all(w > 0 for w in weights) and all(f for f in strategies)
    assert all(len(set(f)) == len(f) for f in strategies)
    assert all(a >= 0 for p in fees for a in p)
    assert all(0 <= e < len(fees) for f in strategies for s in f for e in s)
    return weights, fees, strategies


def states(g):
    return tuple(product(*(range(len(f)) for f in g[2])))


def cost(g, s, i):
    """Literal original-resource oracle: recompute loads after any deviation."""
    weights, fees, strategies = g
    total = Q(0)
    for e in strategies[i][s[i]]:
        load = sum((weights[j] for j, f in enumerate(strategies) if e in f[s[j]]), Q(0))
        total += sum((a * load ** k for k, a in enumerate(fees[e])), Q(0))
    return total


def columns_and_coefficients(g):
    weights, fees, strategies = g
    positions = tuple((i, b) for i, f in enumerate(strategies) for b in range(len(f)))
    d = max(len(p) - 1 for p in fees)
    signatures = tuple(frozenset(positions[j] for j in range(len(positions)) if mask >> j & 1)
                       for mask in range(1, 1 << len(positions)))
    cols = tuple((sig, k) for sig in signatures for k in range(d + 1))
    coeff = {col: Q(0) for col in cols}
    for e, fee in enumerate(fees):
        sig = frozenset((i, b) for i, f in enumerate(strategies)
                        for b, action in enumerate(f) if e in action)
        if sig:
            for k, a in enumerate(fee):
                coeff[sig, k] += a
    return cols, tuple(coeff[col] for col in cols)


def basis(weights, s, i, col):
    sig, k = col
    if (i, s[i]) not in sig:
        return Q(0)
    load = sum((w for j, w in enumerate(weights) if (j, s[j]) in sig), Q(0))
    return load ** k


def dot(a, b):
    assert len(a) == len(b)
    return sum((x * y for x, y in zip(a, b)), Q(0))


def matrix(g, alpha, selector, cols):
    rows = []
    for s, (i, b) in zip(states(g), selector):
        assert 0 <= i < len(g[0]) and 0 <= b < len(g[2][i])
        t = tuple(b if j == i else x for j, x in enumerate(s))
        rows.append(tuple(basis(g[0], s, i, col) - alpha * basis(g[0], t, i, col)
                          for col in cols))
    assert len(rows) == len(states(g)) == len(selector)
    return tuple(rows)


def primal(B, a):
    assert a and all(x >= 0 for x in a)
    margins = tuple(dot(row, a) for row in B)
    return min(margins) > 0, margins


def dual(B, lam):
    assert len(lam) == len(B) and all(x >= 0 for x in lam) and sum(lam) == 1
    values = tuple(dot(col, lam) for col in zip(*B))
    return max(values) <= 0, values


def linear_solve(rows, rhs):
    """Unique rational square solve; singular choices are skipped."""
    n = len(rhs)
    A = [list(map(Q, row)) + [Q(v)] for row, v in zip(rows, rhs)]
    assert len(A) == n and all(len(row) == n + 1 for row in A)
    for j in range(n):
        pivot = next((i for i in range(j, n) if A[i][j]), None)
        if pivot is None:
            return None
        A[j], A[pivot] = A[pivot], A[j]
        scale = A[j][j]
        A[j] = [x / scale for x in A[j]]
        for i in range(n):
            if i != j:
                factor = A[i][j]
                A[i] = [x - factor * y for x, y in zip(A[i], A[j])]
    return tuple(row[-1] for row in A)


def tiny_alternative(B):
    """Find max_a min(Ba) on simplex, then explicitly verify one alternative."""
    r, q = len(B), len(B[0])
    units_q = [tuple(Q(j == k) for j in range(q)) for k in range(q)]
    constraints = [u + (Q(0),) for u in units_q] + [tuple(row) + (Q(-1),) for row in B]
    candidates = []
    for active in combinations(constraints, q):
        x = linear_solve([tuple([Q(1)] * q + [Q(0)]), *active], [1] + [0] * q)
        if x is not None and all(dot(row, x) >= 0 for row in constraints):
            candidates.append(x)
    assert candidates
    best = max(candidates, key=lambda x: x[-1])
    if best[-1] > 0:
        ok, margins = primal(B, best[:-1])
        assert ok and min(margins) == best[-1]
        return 'primal'
    units_r = [tuple(Q(j == k) for j in range(r)) for k in range(r)]
    inequalities = units_r + [tuple(-v for v in col) for col in zip(*B)]
    for active in combinations(inequalities, r - 1):
        lam = linear_solve([tuple([Q(1)] * r), *active], [1] + [0] * (r - 1))
        if lam is not None and all(dot(row, lam) >= 0 for row in inequalities):
            assert dual(B, lam)[0]
            return 'dual'
    raise AssertionError('No exact alternative found')


def audit(path):
    raw = json.loads(path.read_text())
    results = []
    compression_checks = margin_checks = minimizer_pairs = 0
    for item in raw['games']:
        g = game(item)
        ss = states(g)
        cols, a = columns_and_coefficients(g)
        alpha = Q(item['alpha'])
        selector = []
        for s in ss:
            for i, f in enumerate(g[2]):
                assert cost(g, s, i) == sum((v * basis(g[0], s, i, col) for col, v in zip(cols, a)), Q(0))
                compression_checks += 1
                for b in range(len(f)):
                    t = tuple(b if j == i else x for j, x in enumerate(s))
                    row = tuple(basis(g[0], s, i, col) - alpha * basis(g[0], t, i, col) for col in cols)
                    assert dot(row, a) == cost(g, s, i) - alpha * cost(g, t, i)
                    margin_checks += 1
            selector.append(max(((i, b) for i, f in enumerate(g[2]) for b in range(len(f))),
                                key=lambda ib: cost(g, s, ib[0]) - alpha * cost(g, tuple(ib[1] if j == ib[0] else x for j, x in enumerate(s)), ib[0])))
        B = matrix(g, alpha, selector, cols)
        ok, margins = primal(B, a)
        assert ok == item['no_alpha_pne']
        record = {'name': item['name'], 'states': len(ss), 'columns': len(cols),
                  'no_alpha_pne': ok, 'selected_margins': list(map(str, margins)),
                  'selector': selector}
        # The Hamming resource selector has unique minimizer at ANY target.
        for target in ss:
            for s in ss:
                resource_distance = sum(len({i for i, f in enumerate(g[2]) if e in f[s[i]]}
                                            ^ {i for i, f in enumerate(g[2]) if e in f[target[i]]})
                                        for e in range(len(g[1])))
                player_distance = sum(len(f[s[i]] ^ f[target[i]]) for i, f in enumerate(g[2]))
                assert resource_distance == player_distance
                assert (resource_distance == 0) == (s == target)
                minimizer_pairs += 1
        results.append(record)
    # Opposite switches of one player: a nontrivial cancellation dual.
    g = game(raw['dual_game'])
    cols, _ = columns_and_coefficients(g)
    sel = ((0, 1), (0, 0))
    B = matrix(g, Q(3, 2), sel, cols)
    ok, values = dual(B, (Q(1, 2), Q(1, 2)))
    assert ok
    small = {'primal': 0, 'dual': 0}
    for entries in product((-1, 0, 1), repeat=4):
        B = tuple(tuple(map(Q, entries[j:j + 2])) for j in (0, 2))
        small[tiny_alternative(B)] += 1
    rng = random.Random(241015)
    for r, q in ((1, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 3)):
        for _ in range(12):
            B = tuple(tuple(Q(rng.randint(-3, 3), rng.randint(1, 3)) for _ in range(q)) for _ in range(r))
            small[tiny_alternative(B)] += 1
    return {'schema_version': 1, 'status': 'PASS', 'arithmetic': 'fractions.Fraction; no tolerance',
            'seed': 241015, 'python_version': sys.version.split()[0],
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input': str(path.relative_to(ROOT)), 'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'compression_cost_checks': compression_checks, 'literal_deviation_margin_checks': margin_checks,
            'minimizer_target_state_pairs': minimizer_pairs,
            'tiny_matrix_alternatives': small, 'explicit_dual_values': list(map(str, values)),
            'games': results,
            'limitations': 'Finite exact implementation audit; no uniform d/log d existence or nonexistence theorem.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    report = audit(args.input.resolve())
    payload = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as out:
            out.write(payload)
    print(payload, end='')


if __name__ == '__main__':
    main()
