"""Optimizer-free independent verification of complete_pair_v2.json.

Also reconstructs each pair's three signed customer masses and verifies all
six specified pure/mixed payoff values directly. This catches the rank defect
that invalidated the old layer's 'complete pair' scope label.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('old_fraction_verifier', BASE.parent/'verify_coupling.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def main():
    obj = json.loads((BASE/'complete_pair_v2.json').read_text())
    n, p = obj['n'], obj['p']
    assert n == 3
    actions = {tuple(x['history']): x['action'] for x in obj['strategy_actions']}
    assert set(actions) == {h for k in range(n) for h in product(range(p), repeat=k)}
    z = {}
    for k in range(n, -1, -1):
        for h in product(range(p), repeat=k):
            z[h] = tuple(h.count(a) for a in range(p)) if k == n else z[h+(actions[h],)]
    qs = sorted({z[h] for h in product(range(p), repeat=n)})
    vertices = [(q, a) for q in qs for a in range(p) if q[a]]
    dim = len(vertices)
    unit = {x: v.unit(i, dim) for i, x in enumerate(vertices)}
    rows = [v.sub(unit[(z[h], a)], unit[(z[h+(b,)], b)]) for h, a in actions.items() for b in range(p)]
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            kappa = max(F(sum(r[j] for j in range(p) if typ >> j & 1), sum(q[j] for j in range(p) if typ >> j & 1))
                        for typ in range(1, 1 << p) if typ >> a & 1)
            rows.append(tuple(kappa*x-y for x, y in zip(unit[(r, a)], unit[(q, a)])))
    def total(q):
        return tuple(sum(q[a]*unit[(q, a)][j] for a in range(p) if q[a]) for j in range(dim))
    eq, rhs = [total(z[()])], [F(1)]
    first = {}
    for q in qs:
        support = tuple(a for a in range(p) if q[a])
        if support in first:
            eq.append(v.sub(total(q), total(first[support])))
            rhs.append(F(0))
        else:
            first[support] = q
    pair_records = []
    for a in range(p):
        for b in range(a+1, p):
            pa = tuple(3*(j == a) for j in range(p))
            pb = tuple(3*(j == b) for j in range(p))
            qa = tuple(2*(j == a)+(j == b) for j in range(p))
            qb = tuple((j == a)+2*(j == b) for j in range(p))
            A, B = unit[(pa, a)], unit[(pb, b)]
            X, Y, Z, W = unit[(qa, a)], unit[(qa, b)], unit[(qb, a)], unit[(qb, b)]
            eq.extend([tuple(z-y-3*(aa-bb) for z, y, aa, bb in zip(Z, Y, A, B)),
                       tuple(x-w-F(3, 2)*(aa-bb) for x, w, aa, bb in zip(X, W, A, B)),
                       tuple(2*x+2*w-z-3*bb for x, w, z, bb in zip(X, W, Z, B))])
            rhs.extend([F(0)]*3)
            pair_records.append((a, b, pa, pb, qa, qb))
    opt = tuple(obj['portfolio'].count(a) for a in range(p))
    y, summary = v.check(obj, rows, eq, rhs, total(opt), vertices)
    lookup = dict(zip(vertices, y))
    reconstructions = 0
    nonnegative_pairs = 0
    for a, b, pa, pb, qa, qb in pair_records:
        ca, cb = 3*lookup[(pa, a)], 3*lookup[(pb, b)]
        cab = v.dot(total(qa), y)
        masses = [(frozenset([a]), cab-cb), (frozenset([b]), cab-ca),
                  (frozenset([a, b]), ca+cb-cab)]
        for q, topic in [(pa, a), (pb, b), (qa, a), (qa, b), (qb, a), (qb, b)]:
            direct = sum((mass/F(sum(q[j] for j in typ)) for typ, mass in masses if topic in typ), F(0))
            assert direct == lookup[(q, topic)]
            reconstructions += 1
        nonnegative_pairs += all(mass >= 0 for typ, mass in masses)
    assert summary['exact_optimum'] == '2'
    print(json.dumps({'exact': True, 'summary': summary,
                      'complete_pair_payoff_reconstructions': reconstructions,
                      'pairs_with_nonnegative_reconstructed_customer_masses': nonnegative_pairs}, indent=2))


if __name__ == '__main__':
    main()
