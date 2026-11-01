"""Exact illustrative regression of the general local/globally signed family.

No SPE solver, LP, scipy, or approximate arithmetic is imported. The general
proof is the explicit cancellation of each omitted-X edge with a Y singleton.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def compositions(n, p):
    if p == 1:
        yield (n,)
    else:
        for first in range(n + 1):
            for rest in compositions(n - first, p - 1):
                yield (first,) + rest


def main():
    m, k = 2, 4
    X, Y = tuple(range(k + 1)), tuple(range(k + 1, 2*k + 1))
    p = len(X) + len(Y)
    rows = [(frozenset((x, y)), 1) for x in X for y in Y]
    rows += [(frozenset((y,)), -1) for y in Y]

    def payoff(q, a, customers=rows):
        assert q[a]
        return sum((F(w, sum(q[b] for b in B)) for B, w in customers if a in B), F())

    def cover(A, customers=rows):
        return sum(w for B, w in customers if B.intersection(A))

    qs = list(compositions(m, p))
    vertices = [(q, a) for q in qs for a in range(p) if q[a]]
    assert all(payoff(q, a) >= 0 for q, a in vertices)

    # Every endpoint pair is explicitly reconstructed by one common nonnegative
    # unit-customer game. This also checks whole-topic payoff vectors, not only
    # the one player's value used in a dilution comparison.
    packets = 0
    for q, r in combinations(qs, 2):
        A = {a for a in range(p) if q[a] or r[a]}
        absent = next(x for x in X if x not in A)
        positive = [(B, w) for B, w in rows if len(B) == 2 and absent not in B]
        assert len(positive) == k*k and all(w == 1 for B, w in positive)
        for v in (q, r):
            S = {a for a in range(p) if v[a]}
            assert cover(S) == cover(S, positive)
            for a in S:
                assert payoff(v, a) == payoff(v, a, positive)
        packets += 1

    # The sharp universal ratio only depends on endpoint supports; an exhaustive
    # interest subset calculation therefore needs at most 2m labels here.
    dilution_checks = 0
    for a in range(p):
        endpoint = [q for q in qs if q[a]]
        for q in endpoint:
            for r in endpoint:
                A = tuple(b for b in range(p) if q[b] or r[b])
                kappas = []
                for bits in product((0, 1), repeat=len(A)):
                    B = {b for b, bit in zip(A, bits) if bit}
                    if a in B:
                        kappas.append(F(sum(r[b] for b in B), sum(q[b] for b in B)))
                kap = max(kappas)
                assert payoff(q, a) <= kap * payoff(r, a)
                dilution_checks += 1

    # A complete history-dependent formal strategy, constructed directly from
    # all ordered histories. Signed customers are not called a legal CAG input.
    terminals, actions = {}, {}
    for d in range(m, -1, -1):
        for h in product(range(p), repeat=d):
            if d == m:
                terminals[h] = tuple(h.count(a) for a in range(p))
            else:
                choices = [(payoff(terminals[h+(a,)], a), a) for a in range(p)]
                best = max(v for v, a in choices)
                a = min(a for v, a in choices if v == best)
                actions[h] = a
                terminals[h] = terminals[h+(a,)]
    comparisons = 0
    for h, a in actions.items():
        for b in range(p):
            assert payoff(terminals[h], a) >= payoff(terminals[h+(b,)], b)
            comparisons += 1

    b = [1 if a in X else -1 for a in range(p)]
    assert sum(b) == 1
    h_direct = sum(w * (z := sum(b[a] for a in B)) * (z-1) for B, w in rows)
    h_pairs = -sum(b[a] * b[c] * (2*cover({a,c})-cover({a})-cover({c}))
                   for a in range(p) for c in range(a+1, p))
    assert h_direct == h_pairs == -2*k
    assert all(cover({a}) == k for a in range(p))
    for a, c in combinations(range(p), 2):
        d = 2*cover({a,c})-cover({a})-cover({c})
        assert d == (2*k if (a in X) == (c in X) else 2*k-2)

    root = terminals[()]
    result = {'exact': True, 'm': m, 'k': k, 'p': p,
              'terminal_counts': len(qs), 'payoff_vertices': len(vertices),
              'pairs_with_explicit_common_nonnegative_realization': packets,
              'sharp_dilution_comparisons': dilution_checks,
              'complete_ordered_histories': len(actions), 'SPE_graph_comparisons': comparisons,
              'hypermetric_value': str(h_pairs),
              'root_count': root, 'root_signed_coverage': cover({a for a in range(p) if root[a]}),
              'scope': 'Illustrative regression of a general nonnegative-gluing obstruction; not a legal-client SPE or half counterexample.'}
    (HERE / 'global_customer_gluing_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
