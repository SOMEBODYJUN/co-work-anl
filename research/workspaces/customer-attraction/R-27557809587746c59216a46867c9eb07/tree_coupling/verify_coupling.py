"""Independent definition-level verifier. No optimizer or probe imports.

The payoff/moment map is rebuilt with Boolean Möbius inversion, independently
of the positive-integral formula used by coupling_probe.py.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def subsets(mask):
    r = mask
    while True:
        yield r
        if not r:
            return
        r = (r-1) & mask


def unit(i, n):
    return tuple(F(j == i) for j in range(n))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def check(layer, rows, equalities, rhs, objective, names):
    n = len(names)
    values = {str(k): F(v) for k, v in layer['positive_values'].items()}
    x = tuple(values.get(str(k), F(0)) for k in names)
    assert layer['variables'] == n and layer['inequalities'] == len(rows)
    assert layer['equalities'] == len(equalities)
    assert all(v >= 0 for v in x)
    assert all(dot(r, x) >= 0 for r in rows)
    assert all(dot(r, x) == b for r, b in zip(equalities, rhs))
    mu = [F(0)]*len(rows)
    for i, val in layer['dual_nonzero']:
        mu[i] = F(val)
    nu = tuple(F(v) for v in layer['dual_equalities'])
    assert all(v >= 0 for v in mu)
    for j in range(n):
        assert sum(v*r[j] for v, r in zip(nu, equalities))-sum(v*r[j] for v, r in zip(mu, rows)) >= objective[j]
    lower = dot(objective, x)
    upper = dot(nu, rhs)
    assert lower == F(layer['lower_bound']) == F(layer['upper_bound']) == upper
    return x, {'layer': layer['layer'], 'exact_optimum': str(lower),
               'inequality_checks': len(rows), 'equality_checks': len(equalities),
               'dual_coordinate_checks': n}


def main():
    obj = json.loads((BASE/'coupling_layers.json').read_text())
    n, p = obj['n'], obj['p']
    actions = {tuple(x['history']): x['action'] for x in obj['strategy_actions']}
    assert set(actions) == {h for d in range(n) for h in product(range(p), repeat=d)}
    terminal = {}
    for d in range(n, -1, -1):
        for h in product(range(p), repeat=d):
            terminal[h] = tuple(h.count(a) for a in range(p)) if d == n else terminal[h+(actions[h],)]
    qs = sorted({tuple(h.count(a) for a in range(p)) for h in product(range(p), repeat=n)})
    vertices = [(q, a) for q in qs for a in range(p) if q[a]]
    nv = len(vertices)
    vu = {v: unit(i, nv) for i, v in enumerate(vertices)}
    edge = [sub(vu[(terminal[h], a)], vu[(terminal[h+(b,)], b)])
            for h, a in actions.items() for b in range(p)]
    dilution_data = []
    dilution = []
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            k = max(F(sum(r[c] for c in range(p) if typ >> c & 1),
                      sum(q[c] for c in range(p) if typ >> c & 1))
                    for typ in range(1, 1 << p) if typ >> a & 1)
            dilution_data.append((q, r, a, k))
            dilution.append(tuple(k*x-y for x, y in zip(vu[(r, a)], vu[(q, a)])))
    def total(q):
        return tuple(sum(q[a]*vu[(q, a)][j] for a in range(p) if q[a]) for j in range(nv))
    root = terminal[()]
    assert list(root) == obj['root']
    opt = tuple(obj['portfolio'].count(a) for a in range(p))
    eq = [total(root)]
    rhs = [F(1)]
    first = {}
    for q in qs:
        support = tuple(a for a in range(p) if q[a])
        if support in first:
            eq.append(sub(total(q), total(first[support])))
            rhs.append(F(0))
        else:
            first[support] = q
    y, summary = check(obj['layers'][0], edge+dilution, eq, rhs, total(opt), vertices)
    summaries = [summary]
    lookup = dict(zip(vertices, y))
    q0, q1, q01, q10 = (3, 0, 0, 0, 0, 0), (0, 3, 0, 0, 0, 0), (2, 1, 0, 0, 0, 0), (1, 2, 0, 0, 0, 0)
    lhs = lookup[(q01, 0)]-lookup[(q10, 1)]
    right = F(3, 2)*(lookup[(q0, 0)]-lookup[(q1, 1)])
    assert lhs == F(1, 8) and right == 0
    peq, prhs = list(eq), list(rhs)
    for a in range(p):
        for b in range(a+1, p):
            pure_a = tuple(n*(j == a) for j in range(p))
            pure_b = tuple(n*(j == b) for j in range(p))
            for k in range(1, n):
                qa = tuple(k*(j == a)+(n-k)*(j == b) for j in range(p))
                qb = tuple((n-k)*(j == a)+k*(j == b) for j in range(p))
                peq.append(tuple(x-y-F(n, k)*(v-w) for x, y, v, w in
                                 zip(vu[(qa, a)], vu[(qb, b)], vu[(pure_a, a)], vu[(pure_b, b)])))
                prhs.append(F(0))
    pair_y, summary = check(obj['layers'][1], edge+dilution, peq, prhs, total(opt), vertices)
    summaries.append(summary)
    pair_lookup = dict(zip(vertices, pair_y))
    # The 15/7 witness has a genuine nonnegative restriction on every pair,
    # though it has no common signed realization across all six topics.
    for a in range(p):
        for b in range(a+1, p):
            pure_a = tuple(n*(j == a) for j in range(p))
            pure_b = tuple(n*(j == b) for j in range(p))
            ca, cb = n*pair_lookup[(pure_a, a)], n*pair_lookup[(pure_b, b)]
            qab = tuple((n-1)*(j == a)+(j == b) for j in range(p))
            cab = dot(total(qab), pair_y)
            assert max(ca, cb) <= cab <= ca+cb

    masks = [s for s in range(1, 1 << p) if s.bit_count() <= n]
    nm = len(masks)
    mi = {s: i for i, s in enumerate(masks)}
    zero = (F(0),)*nm
    def kr(s):
        return unit(mi[s], nm) if s else zero
    cache = {}
    def payoff(q, a):
        key = q, a
        if key in cache:
            return cache[key]
        support = sum(1 << b for b in range(p) if q[b])
        def f(typ):
            return F(1, sum(q[b] for b in range(p) if typ >> b & 1)) if typ >> a & 1 else F(0)
        row = [F(0)]*nm
        for s in subsets(support):
            if s:
                row[mi[s]] = -sum(((-1)**(s.bit_count()-d.bit_count())*f(support & ~d) for d in subsets(s)), F(0))
        row = tuple(row)
        for typ in range(1, 1 << p):
            assert sum(row[i] for i, s in enumerate(masks) if s & typ) == f(typ)
        cache[key] = row
        return row
    prows = [payoff(q, a) for q, a in vertices]
    gamma = [sub(payoff(terminal[h], a), payoff(terminal[h+(b,)], b))
             for h, a in actions.items() for b in range(p)]
    mdilution = [tuple(k*x-y for x, y in zip(payoff(r, a), payoff(q, a))) for q, r, a, k in dilution_data]
    monotone = [sub(kr(s | (1 << a)), kr(s)) for s in [0]+masks if s.bit_count() < n
                for a in range(p) if not s >> a & 1]
    submod = [sub(add(kr(s | (1 << a)), kr(s | (1 << b))), add(kr(s), kr(s | (1 << a) | (1 << b))))
              for s in [0]+masks if s.bit_count() <= n-2 for a in range(p) if not s >> a & 1
              for b in range(a+1, p) if not s >> b & 1]
    alternate = []
    for u in masks:
        for a in subsets(u):
            if a:
                s = u & ~a
                alternate.append(tuple(sum(((-1)**(r.bit_count()+1)*kr(s | r)[j] for r in subsets(a)), F(0)) for j in range(nm)))
    rows_by_layer = [gamma+prows+mdilution, gamma+monotone+mdilution,
                     gamma+monotone+submod+mdilution, gamma+alternate+mdilution]
    rootmask = sum(1 << a for a in range(p) if root[a])
    optmask = sum(1 << a for a in range(p) if opt[a])
    for layer, rows in zip(obj['layers'][2:-1], rows_by_layer):
        _, summary = check(layer, rows, [kr(rootmask)], [F(1)], kr(optmask), masks)
        summaries.append(summary)
    types = list(range(1, 1 << p))
    def true_payoff(q, a):
        return tuple(F(1, sum(q[b] for b in range(p) if typ >> b & 1)) if typ >> a & 1 else F(0)
                     for typ in types)
    true_gamma = [sub(true_payoff(terminal[h], a), true_payoff(terminal[h+(b,)], b))
                  for h, a in actions.items() for b in range(p)]
    true_x, summary = check(obj['layers'][-1], true_gamma,
                       [tuple(F(bool(rootmask & typ)) for typ in types)], [F(1)],
                       tuple(F(bool(optmask & typ)) for typ in types), types)
    summaries.append(summary)
    alias_pairs = [(a, b) for a in range(p) for b in range(a+1, p)
                   if not sum(true_x[i] for i, typ in enumerate(types) if bool(typ >> a & 1) != bool(typ >> b & 1))]
    assert alias_pairs == [(0, 3)]
    source = json.loads((ROOT/obj['distinct_customer_source']).read_text())
    source_x = [F(0)]*len(types)
    for customer in source['customers']:
        typ = sum(1 << a for a in customer['topics'])
        source_x[typ-1] += customer['multiplicity']
    assert sum(source_x) == 22 and all(dot(row, source_x) >= 0 for row in true_gamma)
    assert all(sum(source_x[i] for i, typ in enumerate(types) if bool(typ >> a & 1) != bool(typ >> b & 1)) > 0
               for a in range(p) for b in range(a+1, p))
    print(json.dumps({'exact': True, 'layers': summaries,
                      'same-support-witness-violates-common-signed-identity': {'left': str(lhs), 'right': str(right)},
                      'true_lp_is_labeled_closure': {'equal_coverage_label_pairs': alias_pairs,
                                                     'distinct_22_customer_source_SPE_checked': True}}, indent=2))


if __name__ == '__main__':
    main()
