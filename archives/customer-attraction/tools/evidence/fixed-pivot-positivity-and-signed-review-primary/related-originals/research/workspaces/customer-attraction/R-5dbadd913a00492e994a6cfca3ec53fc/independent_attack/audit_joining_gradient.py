"""Definition-level exact audit, without importing a generator or LP solver.

Inputs are payoff tables, not asserted customer games.  All output stays in
this investigator's own directory.  Existence/optimality of an LP optimum is
not audited: a rational feasible point with objective > 2 suffices here.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
ROOT = HERE.parents[4]
OLD = ROOT / 'research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/tree_coupling/all_pair_identities_obstruction_candidate.json'
NEW = WORK / 'geometry/cross_support_gradient_probe.json'


def load_table(path, old=False):
    raw = path.read_bytes()
    o = json.loads(raw)
    data = o if old else o['best']
    p, m = (o['p'], o['n']) if old else (o['topics'], o['players'])
    rows = data['y']
    y = {(tuple(r['q']), r['a']): F(r['value']) for r in rows}
    assert len(y) == len(rows)
    actions = {tuple(r['history']): r['action'] for r in o['strategy_actions']}
    return o, data, m, p, y, actions, hashlib.sha256(raw).hexdigest()


def all_counts(length, p):
    return sorted({tuple(h.count(a) for a in range(p))
                   for h in product(range(p), repeat=length)})


def plus(b, a):
    return tuple(n + (i == a) for i, n in enumerate(b))


def joining(y, b):
    return tuple(y[plus(b, a), a] for a in range(len(b)))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def audit():
    old, od, m, p, yo, _, old_hash = load_table(OLD, old=True)
    assert (m, p) == (3, 6)
    old_b, old_d = (1, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 1)
    jb, jd = joining(yo, old_b), joining(yo, old_d)
    old_square = dot(tuple(v-u for u, v in zip(old_b, old_d)),
                     tuple(u-v for u, v in zip(jb, jd)))
    assert old_square == -F(3, 13)

    obj, data, m, p, y, actions, new_hash = load_table(NEW)
    assert (m, p) == (3, 6)
    qs, bs = all_counts(m, p), all_counts(m-1, p)
    expected = {(q, a) for q in qs for a in range(p) if q[a]}
    assert set(y) == expected and len(y) == 126 and min(y.values()) >= 0
    histories = [h for k in range(m) for h in product(range(p), repeat=k)]
    assert set(actions) == set(histories)
    assert all(0 <= a < p for a in actions.values())

    def terminal(h):
        while len(h) < m:
            h += (actions[h],)
        return tuple(h.count(a) for a in range(p))

    def welfare(q):
        return sum(q[a]*y[q, a] for a in range(p) if q[a])

    supports = {}
    conservation = []
    for q in qs:
        s = tuple(a for a in range(p) if q[a])
        if s in supports:
            conservation.append(welfare(q)-supports[s])
        else:
            supports[s] = welfare(q)
    assert all(v == 0 for v in conservation)
    covers = lambda s: supports[tuple(sorted(s))]

    graph = []
    for h in histories:
        for a in range(p):
            graph.append(y[terminal(h), actions[h]]-y[terminal(h+(a,)), a])
    assert len(graph) == 258 and min(graph) >= 0

    # Sharp ratio over every possible nonempty customer membership type.
    dilution = []
    for q, a in expected:
        for r, aa in expected:
            if aa != a or q == r:
                continue
            kappa = max(F(sum(r[i] for i in range(p) if mask >> i & 1),
                          sum(q[i] for i in range(p) if mask >> i & 1))
                        for mask in range(1, 1 << p) if mask >> a & 1)
            dilution.append(kappa*y[r, a]-y[q, a])
    assert len(dilution) == 2520 and min(dilution) >= 0

    pair_residuals = []
    for q, a in expected:
        s = tuple(i for i in range(p) if q[i])
        if len(s) == 2:
            aa = next(i for i in s if i != a)
            pair_residuals.append(m*q[a]*y[q, a]-q[a]*covers((a,))
                                  -q[aa]*(covers(s)-covers((aa,))))
    assert len(pair_residuals) == 60 and all(v == 0 for v in pair_residuals)

    potential_rows = data['potential']
    potential = {tuple(r['b']): F(r['value']) for r in potential_rows}
    assert len(potential) == len(potential_rows) == 21 and set(potential) == set(bs)
    cg = []
    monotone = []
    for b in bs:
        for d in bs:
            if b == d:
                continue
            delta = tuple(v-u for u, v in zip(b, d))
            cg.append(dot(delta, joining(y, b))-(potential[d]-potential[b]))
            monotone.append(dot(delta, tuple(u-v for u, v in zip(joining(y, b), joining(y, d)))))
    assert len(cg) == 420 and min(cg) >= 0 and min(monotone) >= 0

    triple_violations = []
    for s in combinations(range(p), 3):
        q = tuple(int(i in s) for i in range(p))
        for a in s:
            c, e = (i for i in s if i != a)
            residual = 6*y[q, a]-(2*covers((a,))
                + covers((a, c))-covers((c,))
                + covers((a, e))-covers((e,))
                + 2*covers(s)-2*covers((c, e)))
            if residual:
                triple_violations.append({'support': list(s), 'action': a,
                                          'residual': str(residual)})
    assert triple_violations
    w, o = welfare(terminal(())), covers(data['target'])
    assert w == 1 and o == F(27, 13) and o > 2*w
    return {'exact': True, 'old_sha256': old_hash, 'new_sha256': new_hash,
        'old_cross_background_square': str(old_square),
        'old_b': list(old_b), 'old_d': list(old_d),
        'old_J_b': list(map(str, jb)), 'old_J_d': list(map(str, jd)),
        'new_history_count': len(histories), 'new_graph_comparisons': len(graph),
        'new_dilution_comparisons': len(dilution),
        'new_two_support_identities': len(pair_residuals),
        'new_potential_states': len(potential), 'new_supergradient_inequalities': len(cg),
        'new_minimum_supergradient_slack': str(min(cg)),
        'new_minimum_monotonicity_slack': str(min(monotone)),
        'new_W': str(w), 'new_comparison_coverage': str(o),
        'new_target': data['target'],
        'new_triple_identity_violation_count': len(triple_violations),
        'new_first_triple_identity_violation': triple_violations[0],
        'scope': 'Feasible abstract CG plus graph/dilution/conservation/two-support table; not a common-client payoff table, SPE counterexample, or proof of LP optimality.'}


if __name__ == '__main__':
    result = audit()
    out = HERE / 'joining_gradient_audit.json'
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
