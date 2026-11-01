"""Definition-level Fraction audit; no imported solver or peer verifier.

The witness is an abstract terminal-payoff array, NOT a customer instance.
All same-support count cycles of arbitrary length reduce to the 15 checks here.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/tree_coupling/support_conservation_obstruction.json'
EXPECTED_SHA = '0630620fb969b6ebac2a0d4b7c46f4a5f818775eba7db6fdaf16050fb7f89ca5'


def counts(h, p):
    return tuple(h.count(a) for a in range(p))


def support(q):
    return tuple(a for a, n in enumerate(q) if n)


def main():
    raw = SOURCE.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_SHA
    data = json.loads(raw)
    n, p = data['n'], data['p']
    assert (n, p) == (3, 6)
    policy = {tuple(z['history']): z['action'] for z in data['strategy_actions']}
    y = {(tuple(z['q']), z['a']): F(z['value']) for z in data['y']}
    terminal = {}
    for depth in range(n, -1, -1):
        for h in product(range(p), repeat=depth):
            if depth == n:
                terminal[h] = counts(h, p)
            else:
                expected = 0 if not h else (3 if h[0] < 3 else 0) if depth == 1 else min(a for a in range(3) if a not in h) if h[1] < 3 else min(a for a in range(3, 6) if a not in h)
                assert policy[h] == expected
                terminal[h] = terminal[h + (policy[h],)]
    qs = sorted(set(terminal[h] for h in product(range(p), repeat=n)))
    vertices = {(q, a) for q in qs for a in support(q)}
    assert set(y) == vertices and len(y) == 126
    assert all(v >= 0 for v in y.values())

    incentives = 0
    for h, chosen in policy.items():
        for b in range(p):
            assert y[terminal[h], chosen] >= y[terminal[h + (b,)], b]
            incentives += 1

    dilution = 0
    for a in range(p):
        applicable = [q for q in qs if q[a]]
        for q, r in product(applicable, repeat=2):
            if q == r:
                continue
            ratios = []
            for mask in range(1, 1 << p):
                if mask >> a & 1:
                    rq = sum(r[b] for b in range(p) if mask >> b & 1)
                    qq = sum(q[b] for b in range(p) if mask >> b & 1)
                    ratios.append(F(rq, qq))
            assert y[q, a] <= max(ratios) * y[r, a]
            dilution += 1

    classes = defaultdict(list)
    coverage = {}
    for q in qs:
        classes[support(q)].append(q)
        value = sum(q[a] * y[q, a] for a in support(q))
        if support(q) in coverage:
            assert coverage[support(q)] == value
        coverage[support(q)] = value
    assert Counter(map(len, classes.values())) == {1: 26, 2: 15}
    assert coverage[support(terminal[()])] == 1
    comparison = counts(tuple(data['portfolio']), p)
    assert support(comparison) == (1, 2, 4)
    assert coverage[support(comparison)] == F(9, 4)

    cyclic_slacks = Counter()
    for group in classes.values():
        for q, r in combinations(group, 2):
            # The two-edge directed loop q -> r -> q.
            slack = sum((r[a] - q[a]) * (y[q, a] - y[r, a]) for a in support(q))
            assert slack >= 0
            cyclic_slacks[str(slack)] += 1
    assert cyclic_slacks == {'0': 1, '1/8': 9, '3/16': 2, '1/4': 3}

    # Verify the universal two-point identity independently on all customer
    # types and every same-support pair, rather than relying on log calculus.
    customer_checks = 0
    for group in classes.values():
        for q, r in combinations(group, 2):
            for mask in range(1, 1 << p):
                qb = sum(q[a] for a in range(p) if mask >> a & 1)
                rb = sum(r[a] for a in range(p) if mask >> a & 1)
                if not qb:
                    assert not rb
                    continue
                actual = sum((r[a] - q[a]) * (F(int(mask >> a & 1), qb) - F(int(mask >> a & 1), rb)) for a in support(q))
                assert actual == F((qb - rb) ** 2, qb * rb) >= 0
                customer_checks += 1

    print(json.dumps({'claim': 'B8-SAME-SUPPORT-CYCLIC-GRADIENT-OBSTRUCTION-v1',
        'source_sha256': EXPECTED_SHA, 'incentives': incentives,
        'dilution_inequalities': dilution, 'support_classes': len(classes),
        'cyclic_generators': sum(cyclic_slacks.values()),
        'cyclic_slacks': dict(sorted(cyclic_slacks.items())),
        'single_customer_identity_checks': customer_checks,
        'root': '1', 'comparison': '9/4',
        'scope': 'abstract relaxation only; every same-support cycle, arbitrary length'}, indent=2))


if __name__ == '__main__':
    main()
