"""Finite coupling-layer probe, with Fraction checks of accepted LP vectors.

Uses the complete source strategy, not just benchmark deviations. A relaxed
point is not a customer instance. The layer name records its precise scope.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import argparse
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parent


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def submasks(mask):
    r = mask
    while True:
        yield r
        if r == 0:
            return
        r = (r-1) & mask


def row_unit(i, n):
    return tuple(F(j == i) for j in range(n))


def minus(a, b):
    return tuple(x-y for x, y in zip(a, b))


def plus(a, b):
    return tuple(x+y for x, y in zip(a, b))


def solve(label, rows, eqrows, eqrhs, objective, names):
    result = linprog(-np.array(objective, dtype=float),
                     A_ub=-np.array(rows, dtype=float), b_ub=np.zeros(len(rows)),
                     A_eq=np.array(eqrows, dtype=float), b_eq=np.array(eqrhs, dtype=float),
                     bounds=(0, None), method='highs')
    out = {'layer': label, 'variables': len(objective), 'inequalities': len(rows),
           'equalities': len(eqrows), 'status': result.message}
    if not result.success:
        return out
    values = tuple(F(float(x)).limit_denominator(10**8) for x in result.x)
    primal = all(x >= 0 for x in values) and all(dot(r, values) >= 0 for r in rows)
    primal = primal and all(dot(r, values) == b for r, b in zip(eqrows, eqrhs))
    mus = tuple(F(float(-x)).limit_denominator(10**8) for x in result.ineqlin.marginals)
    nus = tuple(F(float(-x)).limit_denominator(10**8) for x in result.eqlin.marginals)
    slack = tuple(sum(nu*r[j] for nu, r in zip(nus, eqrows))
                  -sum(mu*r[j] for mu, r in zip(mus, rows))-objective[j]
                  for j in range(len(objective)))
    dual = all(x >= 0 for x in mus) and all(x >= 0 for x in slack)
    out.update(primal_exact=primal, dual_exact=dual,
               lower_bound=str(dot(objective, values)) if primal else None,
               upper_bound=str(dot(nus, eqrhs)) if dual else None,
               positive_values={str(name): str(value) for name, value in zip(names, values) if value},
               dual_nonzero=[(i, str(x)) for i, x in enumerate(mus) if x],
               dual_equalities=[str(x) for x in nus])
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='coupling_layers.json')
    args = parser.parse_args()
    source = ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/tree_duality/pair_dilution_obstruction.json'
    obj = json.loads(source.read_text())
    n, p = obj['n'], obj['p']
    actions = {tuple(x['history']): x['action'] for x in obj['strategy_actions']}
    assert set(actions) == {h for d in range(n) for h in product(range(p), repeat=d)}
    terminals = {}
    for d in range(n, -1, -1):
        for h in product(range(p), repeat=d):
            terminals[h] = tuple(h.count(a) for a in range(p)) if d == n else terminals[h+(actions[h],)]
    counts = sorted(set(terminals[h] for h in product(range(p), repeat=n)))
    vertices = [(q, a) for q in counts for a in range(p) if q[a]]
    vi = {v: i for i, v in enumerate(vertices)}
    nu = len(vertices)
    units = [row_unit(i, nu) for i in range(nu)]
    edge_rows = [minus(units[vi[(terminals[h], a)]], units[vi[(terminals[h+(b,)], b)]])
                 for h, a in actions.items() for b in range(p)]
    dilution = []
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            k = max(F(sum(r[c] for c in range(p) if mask >> c & 1),
                      sum(q[c] for c in range(p) if mask >> c & 1))
                    for mask in range(1, 1 << p) if mask >> a & 1)
            dilution.append(tuple(k*x-y for x, y in zip(units[vi[(r, a)]], units[vi[(q, a)]])))
    def total(q):
        return tuple(sum(q[a]*units[vi[(q, a)]][j] for a in range(p) if q[a]) for j in range(nu))
    root = terminals[()]
    opt = tuple(obj['portfolio'].count(a) for a in range(p))
    eq = [total(root)]
    eqrhs = [F(1)]
    first = {}
    for q in counts:
        support = tuple(a for a in range(p) if q[a])
        if support in first:
            eq.append(minus(total(q), total(first[support])))
            eqrhs.append(F(0))
        else:
            first[support] = q
    outputs = [solve('graph+dilution+same-support-totals', edge_rows+dilution, eq, eqrhs,
                     total(opt), vertices)]
    pair_eq, pair_rhs = list(eq), list(eqrhs)
    for a in range(p):
        for b in range(a+1, p):
            pure_a = tuple(n*(j == a) for j in range(p))
            pure_b = tuple(n*(j == b) for j in range(p))
            for k in range(1, n):
                qa = tuple(k*(j == a)+(n-k)*(j == b) for j in range(p))
                qb = tuple((n-k)*(j == a)+k*(j == b) for j in range(p))
                pair_eq.append(tuple(x-y-F(n, k)*(v-w) for x, y, v, w in
                                     zip(units[vi[(qa, a)]], units[vi[(qb, b)]],
                                         units[vi[(pure_a, a)]], units[vi[(pure_b, b)]])))
                pair_rhs.append(F(0))
    outputs.append(solve('graph+dilution+same-support-totals+all-two-topic-coupling',
                         edge_rows+dilution, pair_eq, pair_rhs, total(opt), vertices))

    masks = [mask for mask in range(1, 1 << p) if mask.bit_count() <= n]
    mi = {mask: i for i, mask in enumerate(masks)}
    nm = len(masks)
    zero = (F(0),)*nm
    def kr(mask):
        return row_unit(mi[mask], nm) if mask else zero

    @lru_cache(None)
    def payoff(q, a):
        # Integral of t^(q_a-1) times independent-support probabilities.
        # Expand only product_{b in R}(1-t^q_b); all coefficients rational.
        others = sum(1 << b for b in range(p) if b != a and q[b])
        row = list(zero)
        for r in submasks(others):
            base_power = q[a]-1+sum(q[b] for b in range(p) if (others & ~r) >> b & 1)
            beta = sum((F((-1)**s.bit_count(), base_power+1+sum(q[b] for b in range(p) if s >> b & 1))
                        for s in submasks(r)), F(0))
            assert beta > 0
            marginal = minus(kr(r | (1 << a)), kr(r))
            row = [x+beta*y for x, y in zip(row, marginal)]
        # Definition-level check on every Boolean interest type.
        for typ in range(1, 1 << p):
            actual = sum(row[j] for j, mask in enumerate(masks) if mask & typ)
            expected = F(1, sum(q[b] for b in range(p) if typ >> b & 1)) if typ >> a & 1 else F(0)
            assert actual == expected
        return tuple(row)

    prows = [payoff(q, a) for q, a in vertices]
    gamma = [minus(payoff(terminals[h], a), payoff(terminals[h+(b,)], b))
             for h, a in actions.items() for b in range(p)]
    rootmask = sum(1 << a for a in range(p) if root[a])
    optmask = sum(1 << a for a in range(p) if opt[a])
    # Every same-support conservation identity follows algebraically here.
    for q in counts:
        row = tuple(sum(q[a]*payoff(q, a)[j] for a in range(p) if q[a]) for j in range(nm))
        assert row == kr(sum(1 << a for a in range(p) if q[a]))
    mdilution = []
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            k = max(F(sum(r[c] for c in range(p) if typ >> c & 1),
                      sum(q[c] for c in range(p) if typ >> c & 1))
                    for typ in range(1, 1 << p) if typ >> a & 1)
            mdilution.append(tuple(k*x-y for x, y in zip(payoff(r, a), payoff(q, a))))
    monotone = []
    for mask in [0]+masks:
        if mask.bit_count() >= n:
            continue
        for a in range(p):
            if not mask >> a & 1:
                monotone.append(minus(kr(mask | (1 << a)), kr(mask)))
    submod = []
    for mask in [0]+masks:
        if mask.bit_count() > n-2:
            continue
        for a in range(p):
            if mask >> a & 1:
                continue
            for b in range(a+1, p):
                if mask >> b & 1:
                    continue
                submod.append(minus(plus(kr(mask | (1 << a)), kr(mask | (1 << b))),
                                    plus(kr(mask), kr(mask | (1 << a) | (1 << b)))))
    # Complete alternation up through all available order/moment pairs:
    # (-1)^(|A|+1) Delta_A C(S) >= 0, S disjoint A, |S union A| <= n.
    alternating = []
    for union in masks:
        for a in submasks(union):
            if not a:
                continue
            s = union & ~a
            row = tuple(sum(((-1)**(r.bit_count()+1)*kr(s | r)[j] for r in submasks(a)), F(0)) for j in range(nm))
            alternating.append(row)
    for label, rows in [
        ('common-signed-moments+positive-payoffs+dilution', gamma+prows+mdilution),
        ('common-monotone-moments+dilution', gamma+monotone+mdilution),
        ('common-submodular-moments+dilution', gamma+monotone+submod+mdilution),
        ('common-locally-coverage-moments+dilution', gamma+alternating+mdilution),
    ]:
        outputs.append(solve(label, rows, [kr(rootmask)], [F(1)], kr(optmask), masks))
    types = list(range(1, 1 << p))
    def true_payoff(q, a):
        return tuple(F(1, sum(q[b] for b in range(p) if typ >> b & 1)) if typ >> a & 1 else F(0)
                     for typ in types)
    true_gamma = [minus(true_payoff(terminals[h], a), true_payoff(terminals[h+(b,)], b))
                  for h, a in actions.items() for b in range(p)]
    outputs.append(solve('true-nonnegative-common-customer-types', true_gamma,
                         [tuple(F(bool(rootmask & typ)) for typ in types)], [F(1)],
                         tuple(F(bool(optmask & typ)) for typ in types), types))
    (BASE/args.output).write_text(json.dumps({'n': n, 'p': p, 'source': str(source.relative_to(ROOT)),
                                             'distinct_customer_source': obj['unit_customer_source'],
                                             'strategy_actions': obj['strategy_actions'], 'root': root,
                                             'portfolio': obj['portfolio'], 'layers': outputs}, indent=2)+'\n')
    for out in outputs:
        print(json.dumps({k: v for k, v in out.items() if k not in ('positive_values', 'dual_nonzero', 'dual_equalities')}))


if __name__ == '__main__':
    main()
