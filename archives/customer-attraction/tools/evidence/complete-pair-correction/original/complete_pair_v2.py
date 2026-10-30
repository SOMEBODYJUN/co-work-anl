"""Corrected complete two-topic coupling for the old n=3,p=6 tree.

The old 15/7 certificate is preserved and only encoded selected pair
differences. This new version adds the independent missing pair relation.
Fraction primal/dual checks certify precisely this finite LP.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[5]
spec = importlib.util.spec_from_file_location('coupling_v1', BASE.parent/'coupling_probe.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def main():
    obj = json.loads((BASE.parent/'coupling_layers.json').read_text())
    n, p = obj['n'], obj['p']
    assert n == 3
    actions = {tuple(x['history']): x['action'] for x in obj['strategy_actions']}
    z = {}
    for d in range(n, -1, -1):
        for h in product(range(p), repeat=d):
            z[h] = tuple(h.count(a) for a in range(p)) if d == n else z[h+(actions[h],)]
    qs = sorted({z[h] for h in product(range(p), repeat=n)})
    vertices = [(q, a) for q in qs for a in range(p) if q[a]]
    nu = len(vertices)
    unit = {v: old.row_unit(i, nu) for i, v in enumerate(vertices)}
    rows = [old.minus(unit[(z[h], a)], unit[(z[h+(b,)], b)]) for h, a in actions.items() for b in range(p)]
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            k = max(F(sum(r[c] for c in range(p) if typ >> c & 1), sum(q[c] for c in range(p) if typ >> c & 1))
                    for typ in range(1, 1 << p) if typ >> a & 1)
            rows.append(tuple(k*x-y for x, y in zip(unit[(r, a)], unit[(q, a)])))
    def total(q):
        return tuple(sum(q[a]*unit[(q, a)][j] for a in range(p) if q[a]) for j in range(nu))
    eq, rhs = [total(z[()])], [F(1)]
    first = {}
    for q in qs:
        support = tuple(a for a in range(p) if q[a])
        if support in first:
            eq.append(old.minus(total(q), total(first[support])))
            rhs.append(F(0))
        else:
            first[support] = q
    for a in range(p):
        for b in range(a+1, p):
            pa = tuple(n*(j == a) for j in range(p))
            pb = tuple(n*(j == b) for j in range(p))
            qa = tuple(2*(j == a)+(j == b) for j in range(p))
            qb = tuple((j == a)+2*(j == b) for j in range(p))
            A, B = unit[(pa, a)], unit[(pb, b)]
            X, Y = unit[(qa, a)], unit[(qa, b)]
            Z, W = unit[(qb, a)], unit[(qb, b)]
            eq.append(tuple(z-y-3*(aa-bb) for z, y, aa, bb in zip(Z, Y, A, B)))
            eq.append(tuple(x-w-F(3, 2)*(aa-bb) for x, w, aa, bb in zip(X, W, A, B)))
            # Third independent condition, absent from the old 15/7 layer.
            eq.append(tuple(2*x+2*w-z-3*bb for x, w, z, bb in zip(X, W, Z, B)))
            rhs.extend([F(0)]*3)
    opt = tuple(obj['portfolio'].count(a) for a in range(p))
    result = old.solve('v2-complete-common-signed-two-topic-coupling', rows, eq, rhs, total(opt), vertices)
    result.update(n=n, p=p, strategy_actions=obj['strategy_actions'], root=z[()], portfolio=obj['portfolio'],
                  corrects='coupling_layers.json selected-pair-difference layer was incorrectly named all-two-topic-coupling')
    (BASE/'complete_pair_v2.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('positive_values', 'dual_nonzero', 'dual_equalities', 'strategy_actions')}))


if __name__ == '__main__':
    main()
