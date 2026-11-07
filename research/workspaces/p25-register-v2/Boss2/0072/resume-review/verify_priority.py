"""Read only the frozen inputs; print the exact audit to stdout."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import json

root = Path(__file__).resolve().parents[6]
ev = root / 'archives/customer-attraction/tools/evidence'
walk = ev / 'R-18-counterexample-search-walks-20261031/original/walk_m5p7_best.json'
floor = ev / 'R-2fc-round3-search-20261031/source'
cred = ev / 'R-373d-credible2-20261031/source'
files = [walk, *sorted(floor.glob('*best.json')), *sorted(cred.glob('*best.json'))]


def read(path):
    return json.loads(path.read_bytes())


def bind(path):
    return {'path': str(path.relative_to(root)), 'sha256': sha256(path.read_bytes()).hexdigest()}


def fixed(path):
    data = read(path)
    ins = data.get('instance')
    if ins is not None:
        m, p = ins['players'], len(ins['topics'])
        clients = [(set(row['topics']), row['multiplicity']) for row in ins['customers']]
    else:
        m, p = data['m'], data['p']
        clients = [(set(i for i in range(p) if mask >> i & 1), w)
                   for mask, w in enumerate(data['weights'], 1) if w]
    rows = data['strategy']['actions']
    strategy = {tuple(row['history']): row['action'] for row in rows}
    hs = [h for k in range(m) for h in product(range(p), repeat=k)]
    assert len(rows) == len(strategy) == len(hs) and set(strategy) == set(hs)
    assert all(0 <= a < p for a in strategy.values())

    def terminal(h):
        while len(h) < m:
            h = (*h, strategy[h])
        return h

    def u(z, t):
        c = Counter(z)
        return sum((Fraction(w, sum(c[i] for i in s)) for s, w in clients if z[t] in s), Fraction())

    def W(z):
        return sum(w for s, w in clients if s.intersection(z))

    z = terminal(())
    assert list(Counter(z)[i] for i in range(p)) == data['strategy']['terminal_counts']
    if 'path' in data:
        assert list(z) == data['path']
    slacks = [u(terminal(h), len(h)) - u(terminal((*h, a)), len(h))
              for h in hs for a in range(p) if a != strategy[h]]
    assert min(slacks) >= 0
    opt = max(map(W, combinations(range(p), min(m, p))))
    d = dict(**bind(path), m=m, p=p, actual=z, utilities=[str(u(z, t)) for t in range(m)],
             W=W(z), OPT=opt, half_slack=2*W(z)-opt, histories=len(hs), nonself=len(slacks),
             minimum_slack=str(min(slacks)), ties=slacks.count(0),
             strategy_action_counts=dict(Counter(strategy.values())),
             customers=sorted((sorted(s), w) for s, w in clients))
    if 'attacked_position' in data:
        t = data['attacked_position']
        assert (W(z), opt, u(z, t)) == (data['W'], data['OPT'], Fraction(data['u']))
        d.update(attacked_position=t, exact_floor_slack=str((2*m-1)*u(z,t)-opt))
    if 'lp_optimized_portfolio' in data:
        J = data['lp_optimized_portfolio']
        assert W(J) == opt and tuple(J) != z
        d.update(static_portfolio=J)
    return d


def rounded():
    path = cred / 'materialized_seed37381021_scale1000000.json'
    d = read(path)
    m, p = 5, 15
    rows = [list(combinations_with_replacement(range(p), j)) for j in range(m+1)]
    types = [(frozenset(i for i in range(p) if mask >> i & 1), w) for mask, w in d['types']]
    W, U = {}, {}
    for z in rows[m]:
        counts = Counter(z)
        pay = [0] * p
        welf = 0
        for s,w in types:
            c = sum(counts[a] for a in s)
            if c:
                assert 60 % c == 0
                welf += w
                for a in s:
                    pay[a] += (60 // c) * w
        W[z], U[z] = welf, pay
    R = {z: {z} for z in rows[m]}
    max_sizes = {}
    for k in reversed(range(m)):
        for h in rows[k]:
            children = [R[tuple(sorted((*h,a)))] for a in range(p)]
            threshold = max(min(U[z][a] for z in child) for a,child in enumerate(children))
            R[h] = {z for a,child in enumerate(children) for z in child if U[z][a] >= threshold}
        max_sizes[k] = max(len(R[h]) for h in rows[k])
    assert len(R[()]) == d['root_outcomes'] == 1
    z, = R[()]
    counts = [z.count(i) for i in range(p)]
    ABCDE = tuple(range(m))
    opt = max(W.values())
    assert counts == d['root_worst_counts'] and W[z] == d['welfare'] and opt == d['optimum']
    assert threshold == d['root_threshold_scaled60']
    assert W[ABCDE] == d['actual_ABCDE_welfare'] and (ABCDE in R[()]) == d['actual_ABCDE_is_SPE_outcome']
    return dict(**bind(path), m=m, p=p, positive_types=len(types), counts=counts, W=W[z], OPT=opt,
                ratio=str(Fraction(opt,W[z])), half_slack=2*W[z]-opt, root_threshold_scaled60=threshold,
                root_outcomes=len(R[()]), max_outcome_count_by_depth=max_sizes,
                ABCDE_welfare=W[ABCDE], ABCDE_is_SPE_outcome=ABCDE in R[()])


def same(a,b,keys):
    x,y=read(a),read(b)
    assert all(x[k] == y[k] for k in keys)
    return {'first':bind(a),'second':bind(b),'equal_fields':list(keys),
            'shared_fields_with_different_values':sorted(k for k in x.keys() & y.keys() if x[k] != y[k]),
            'fields_only_in_first':sorted(x.keys()-y.keys()),'fields_only_in_second':sorted(y.keys()-x.keys())}


if __name__ == '__main__':
    d={'fixed':[fixed(x) for x in files], 'rounded':rounded(),
       'floor_duplicate':same(floor/'m4p6_pos0.best.json',floor/'m4p6_pos0_multi.best.json',
                             ('instance','strategy','W','OPT','u','attacked_position')),
       'strong_duplicate':same(cred/'strong_scan_best.json',cred/'strong_all_scan_best.json',
                              ('weights','source_weights','strategy','path','welfare','optimum','objective','mode'))}
    print(json.dumps(d,ensure_ascii=False,indent=2))
