"""Exact reconstruction of two saved ADM discovery points, not a general theorem.

For each finite input, backward induction enumerates every attainable SPE
terminal count vector. Ordered histories with the same counts have identical
continuation games; their strategies may still be chosen independently.
An action's selected child can be supported precisely when its payoff exceeds
the minimum credible continuation payoff of every other action. This proves
the recursion by induction, including arbitrary ties and repeated actions.
The final certificates check both sides of the finite max-min problem using
Fractions. No original discovery entry point or floating LP is executed.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys


def unique_solution(matrix, rhs, n):
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    pivots = []
    for col in range(n):
        pivot = next((i for i in range(len(pivots), len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        row = len(pivots)
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[row])]
        pivots.append(col)
    if any(not any(row[:n]) and row[n] for row in a) or len(pivots) != n:
        return None
    result = [F(0)] * n
    for row, col in enumerate(pivots):
        result[col] = a[row][n]
    return result


def reconstruct(record):
    ins = record['instance']
    m, q = ins['players'], len(ins['topics'])
    types = [(tuple(t['topics']), t['multiplicity']) for t in ins['customers']]

    def step(c, action):
        return tuple(v + (a == action) for a, v in enumerate(c))

    def utility(action, c):
        return sum((F(w, sum(c[a] for a in ts)) for ts, w in types if action in ts), F(0))

    def insertion(action, c):
        return sum((F(w, 1 + sum(c[a] for a in ts)) for ts, w in types if action in ts), F(0))

    @lru_cache(None)
    def outcomes(c):
        if sum(c) == m:
            return frozenset([c])
        children = [outcomes(step(c, a)) for a in range(q)]
        threshold = max(min(utility(a, z) for z in children[a]) for a in range(q))
        return frozenset(z for a in range(q) for z in children[a] if utility(a, z) >= threshold)

    path = tuple(record['path'])
    z = tuple(path.count(a) for a in range(q))
    c = (0,) * q
    menu = set()
    for i, actual in enumerate(path):
        assert z in outcomes(step(c, actual))
        actual_u = utility(actual, z)
        for action in range(q):
            children = outcomes(step(c, action))
            assert actual_u >= min(utility(action, y) for y in children)
            menu.update(y for y in children if utility(action, y) <= actual_u)
        c = step(c, actual)
    menu = sorted(menu)
    assert len(menu) == record['Dsize']
    assert len(outcomes((0,) * q)) == record['outcomes']
    welfare = sum(w for ts, w in types if any(z[a] for a in ts))
    assert welfare == record['W']

    # This rationalization is a proposed exact witness, then checked exactly.
    p = [F(str(v)).limit_denominator(10000) for v in record['p']]
    assert all(v >= 0 for v in p) and sum(p) == 1
    kernel = [[insertion(a, y) for a in range(q)] for y in menu]
    values = [sum((x * y for x, y in zip(row, p)), F(0)) for row in kernel]
    value = min(values)
    support = [a for a in range(q) if p[a]]
    inactive = [a for a in range(q) if not p[a]]
    tight = [i for i, v in enumerate(values) if v == value]
    dual = None
    # At a dual vertex, a zero-probability query can also have a tight bound.
    # Retain those possible active inequalities when extracting a vertex.
    for size in range(1, min(len(tight), q + 1) + 1):
        for chosen in combinations(tight, size):
            for extra_size in range(len(inactive) + 1):
                for extra in combinations(inactive, extra_size):
                    constrained = support + list(extra)
                    equations = [[kernel[i][a] for i in chosen] for a in constrained]
                    equations.append([F(1)] * size)
                    weights = unique_solution(equations, [value] * len(constrained) + [F(1)], size)
                    if weights is None or any(w < 0 for w in weights):
                        continue
                    upper = [sum((w * kernel[i][a] for i, w in zip(chosen, weights)), F(0)) for a in range(q)]
                    if max(upper) <= value:
                        dual = (chosen, weights, upper)
                        break
                if dual is not None:
                    break
            if dual is not None:
                break
        if dual is not None:
            break
    assert dual is not None, 'No exact upper witness found'
    chosen, weights, upper = dual
    assert sum(weights) == 1
    assert min(values) == max(upper) == value
    assert abs(float(value) - record['value']) < 1e-12
    assert abs(float(value - F(welfare, m)) - record['gap']) < 1e-12
    return {
        'name': record['name'], 'players': m, 'topics': q,
        'root_outcomes': len(outcomes((0,) * q)), 'menu_size': len(menu),
        'ordered_actual_path_supported': True, 'actual_welfare': welfare,
        'terminal_count_menu': menu, 'insertion_kernel': kernel,
        'query_distribution': p, 'menu_query_values': values,
        'dual_menu_counts': [menu[i] for i in chosen],
        'dual_weights': weights, 'dual_query_values': upper,
        'maxmin_value': value, 'welfare_per_player': F(welfare, m),
        'gap': value - F(welfare, m),
        'scope': 'Two finite saved menu problems; negative gaps are not counterexamples or universal proof.'
    }


def main():
    folder = Path(__file__).resolve().parent
    source = folder / 'adm_discovery.json'
    raw = source.read_bytes()
    expected = '722a62da78868eb1a07d09aed464e983287a9c6a233767f12c2cd4f76ea41499'
    assert hashlib.sha256(raw).hexdigest() == expected
    data = json.loads(raw)
    result = {
        'source_sha256': expected,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'original_reported_checked': data['checked'],
        'new_saved_records_reconstructed': len(data['records']),
        'original_discovery_runs': 0,
        'records': [reconstruct(r) for r in data['records']]
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, default=lambda v: str(v) if isinstance(v, F) else v)
    print()


if __name__ == '__main__':
    main()
