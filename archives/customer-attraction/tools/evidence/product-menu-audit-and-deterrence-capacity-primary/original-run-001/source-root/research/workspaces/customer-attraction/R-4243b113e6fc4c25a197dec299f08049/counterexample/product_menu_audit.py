"""Independent literal-client Fraction audit of product full-history menus.
No repository game, SPE solver, certificate verifier, or root product code imports.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[5]


def load(name):
    obj = json.loads((ROOT / 'examples/customer_attraction' / (name + '.json')).read_text())
    cert = json.loads((ROOT / 'evidence/certificates/customer_attraction' / (name + '.json')).read_text())
    p, m = len(obj['topics']), obj['players']
    clients = [frozenset(c['topics']) for c in obj['customers'] for _ in range(c['multiplicity'])]
    actions = {tuple(row['history']): row['action'] for row in cert['actions']}
    assert set(actions) == {h for d in range(m) for h in product(range(p), repeat=d)}
    assert all(0 <= a < p for a in actions.values())
    return {'name': name, 'p': p, 'm': m, 'clients': clients, 'actions': actions,
            'declared_counts': tuple(cert['terminal_counts'])}


def continuation(g, h):
    h = tuple(h)
    while len(h) < g['m']:
        h += (g['actions'][h],)
    return h


def payoff(g, s, i):
    return sum((F(1, sum(a in c for a in s)) for c in g['clients'] if s[i] in c), F(0))


def kernel(g, t, z):
    return sum((F(1, 1 + sum(a in c for a in z)) for c in g['clients'] if t in c), F(0))


def component_audit(g):
    rows = []
    for d in range(g['m']):
        for h in product(range(g['p']), repeat=d):
            z = continuation(g, h)
            for a in range(g['p']):
                zz = continuation(g, h + (a,))
                gap = payoff(g, z, d) - payoff(g, zz, d)
                assert gap >= 0, (g['name'], h, a, gap)
                rows.append(gap)
    actual = continuation(g, ())
    assert tuple(actual.count(a) for a in range(g['p'])) == g['declared_counts']
    menus = [[continuation(g, actual[:i] + (a,)) for a in range(g['p'])]
             for i in range(g['m'])]
    K = [[[kernel(g, t, menus[i][a]) for a in range(g['p'])]
          for t in range(g['p'])] for i in range(g['m'])]
    return actual, menus, K, {'histories': len(g['actions']), 'spe_comparisons': len(rows),
                             'minimum_spe_gap': min(rows)}


def marginals(q, p1, p2):
    return ([sum((q[a*p2+b] for b in range(p2)), F(0)) for a in range(p1)],
            [sum((q[a*p2+b] for a in range(p1)), F(0)) for b in range(p2)])


def product_distribution(p, q):
    return [x*y for x in p for y in q]


def greedy_coupling(p, q, reverse=False):
    pp, qq = list(p), list(q)
    out = [F(0)]*(len(p)*len(q))
    order = list(reversed(range(len(q)))) if reverse else list(range(len(q)))
    for a in range(len(p)):
        for b in order:
            z = min(pp[a], qq[b])
            out[a*len(q)+b] += z
            pp[a] -= z
            qq[b] -= z
    assert not any(pp) and not any(qq)
    return out


def fs(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, (list, tuple)): return [fs(z) for z in x]
    if isinstance(x, dict): return {str(k): fs(z) for k,z in x.items()}
    return x


def main(output):
    g1 = load('eight_cce_welfare_gap')
    g2 = load('worst_pne_welfare_failure')
    assert g1['m'] == g2['m']
    m, p1, p2 = g1['m'], g1['p'], g2['p']
    z1, menu1, k1, a1 = component_audit(g1)
    z2, menu2, k2, a2 = component_audit(g2)
    pairs = list(product(range(p1), range(p2)))
    P = len(pairs)
    histories = [h for d in range(m) for h in product(range(P), repeat=d)]
    actions = {}
    for h in histories:
        h1, h2 = tuple(pairs[a][0] for a in h), tuple(pairs[a][1] for a in h)
        actions[h] = pairs.index((g1['actions'][h1], g2['actions'][h2]))
    # Literal product clients, each belonging to one disjoint component.
    clients = [(j, c) for j,g in enumerate((g1,g2)) for c in g['clients']]
    def cont(h):
        h = tuple(h)
        while len(h) < m: h += (actions[h],)
        return h
    def pu(s, i):
        return sum((F(1, sum(pairs[a][j] in c for a in s))
                    for j,c in clients if pairs[s[i]][j] in c), F(0))
    def pk(t, s):
        return sum((F(1, 1+sum(pairs[a][j] in c for a in s))
                    for j,c in clients if pairs[t][j] in c), F(0))
    spe_rows = []
    for h in histories:
        d = len(h)
        z = cont(h)
        assert tuple(pairs[a][0] for a in z) == continuation(g1, tuple(pairs[a][0] for a in h))
        assert tuple(pairs[a][1] for a in z) == continuation(g2, tuple(pairs[a][1] for a in h))
        for b in range(P):
            zz = cont(h+(b,))
            gap = pu(z,d)-pu(zz,d)
            assert gap >= 0, (h,b,gap)
            spe_rows.append((h,b,gap))
    actual = cont(())
    assert tuple(pairs[a][0] for a in actual) == z1
    assert tuple(pairs[a][1] for a in actual) == z2
    menus = [[cont(actual[:i]+(a,)) for a in range(P)] for i in range(m)]
    K = [[[pk(t,menus[i][a]) for a in range(P)] for t in range(P)] for i in range(m)]
    for i,t,a in product(range(m),range(P),range(P)):
        t1,t2 = pairs[t]
        b1,b2 = pairs[a]
        assert tuple(pairs[x][0] for x in menus[i][a]) == menu1[i][b1]
        assert tuple(pairs[x][1] for x in menus[i][a]) == menu2[i][b2]
        assert K[i][t][a] == k1[i][t1][b1]+k2[i][t2][b2]
    samples = [
        ([F(1,10),F(2,10),F(3,10),F(4,10)], [F(4,10),F(3,10),F(2,10),F(1,10)]),
        ([F(1,7),F(1,7),F(2,7),F(3,7)], [F(2,9),F(1,9),F(4,9),F(2,9)]),
        ([F(0),F(1,3),F(2,3),F(0)], [F(1,5),F(0),F(1,5),F(3,5)]),
        ([F(1,2),F(0),F(0),F(1,2)], [F(0),F(1,2),F(1,2),F(0)]),
    ]
    sample_rows = []
    def inspect(p,q,dist,label):
        assert marginals(dist,p1,p2) == (p,q)
        assert sum(dist) == 1 and min(dist) >= 0
        psi1 = [min(sum((p[t]*k1[i][t][a] for t in range(p1)),F(0)) for a in range(p1)) for i in range(m)]
        psi2 = [min(sum((q[t]*k2[i][t][a] for t in range(p2)),F(0)) for a in range(p2)) for i in range(m)]
        full = [min(sum((dist[t]*K[i][t][a] for t in range(P)),F(0)) for a in range(P)) for i in range(m)]
        assert full == [x+y for x,y in zip(psi1,psi2)]
        direct = min(sum((dist[t]*K[i][t][a] for t in range(P)),F(0))
                     for i in range(m) for a in range(P))
        assert direct == min(full)
        return {'label':label,'p1':p,'p2':q,'joint':dist,'psi1':psi1,'psi2':psi2,
                'per_position_product_min':full,'full_menu_min':direct,
                'sum_of_separate_position_minima':min(psi1)+min(psi2)}
    for j,(p,q) in enumerate(samples):
        for name,dist in [('independent',product_distribution(p,q)),
                          ('positive_coupling',greedy_coupling(p,q)),
                          ('negative_coupling',greedy_coupling(p,q,True))]:
            sample_rows.append(inspect(p,q,dist,f'sample_{j}_{name}'))
    # Solve only to obtain candidate certificates; all bounds below are exact Fractions.
    import numpy as np
    from scipy.optimize import linprog
    columns = [(i,a) for i in range(m) for a in range(P)]
    mat = [[K[i][t][a] for i,a in columns] for t in range(P)]
    # Maximize v with query distribution q; each full menu column gives v <= q.K_col.
    lp = linprog(np.array([0.0]*P+[-1.0]),
                 A_ub=np.array([[-float(mat[t][c]) for t in range(P)]+[1.0] for c in range(len(columns))]),
                 b_ub=np.zeros(len(columns)),A_eq=np.array([[1.0]*P+[0.0]]),b_eq=np.array([1.0]),
                 bounds=[(0,None)]*P+[(None,None)],method='highs')
    assert lp.success, lp.message
    qopt = [F(float(x)).limit_denominator(10**8) for x in lp.x[:P]]
    dual = [F(float(-x)).limit_denominator(10**8) for x in lp.ineqlin.marginals]
    assert sum(qopt) == sum(dual) == 1 and min(qopt+dual) >= 0
    lower = min(sum((qopt[t]*mat[t][c] for t in range(P)),F(0)) for c in range(len(columns)))
    upper = max(sum((dual[c]*mat[t][c] for c in range(len(columns))),F(0)) for t in range(P))
    assert lower == upper, ('unverified numerical LP certificate',lower,upper)
    op,oq = marginals(qopt,p1,p2)
    optimal = inspect(op,oq,qopt,'certified_full_menu_optimizer')
    assert optimal['full_menu_min'] == lower
    # Independent coupling with the same optimal marginals must attain the identical optimum.
    independent_optimal = inspect(op,oq,product_distribution(op,oq),'optimal_marginals_independent_coupling')
    assert independent_optimal['full_menu_min'] == lower
    welfare = sum(any(pairs[a][j] in c for a in actual) for j,c in clients)
    report = {
        'status':'all exact checks passed',
        'scope':'finite independent verification of product menu separability, not half equivalence',
        'basis':'literal separate clients; Fraction throughout; no repository solver/verifier imports',
        'components':[{'name':g1['name'],'actual':z1,**a1},{'name':g2['name'],'actual':z2,**a2}],
        'product':{'players':m,'topics':P,'clients':len(clients),'histories':len(histories),
                   'spe_comparisons':len(spe_rows),'minimum_spe_gap':min(z for _,_,z in spe_rows),
                   'actual':actual,'actual_pairs':[pairs[a] for a in actual],
                   'actual_payoffs':[pu(actual,i) for i in range(m)],'welfare':welfare},
        'menu':{'positions':m,'forced_actions_each':P,'query_topics':P,
                'entries_verified':m*P*P,'Z':menus,'K':K},
        'sample_checks':sample_rows,
        'exact_value_certificate':{'value':lower,'query_distribution':qopt,
            'dual_distribution_over_position_action_columns':dual,'column_labels':columns,
            'primal_lower':lower,'dual_upper':upper,'optimal_marginal_check':optimal,
            'optimal_independent_check':independent_optimal},
        'complete_product_strategy':[{'history':h,'action':actions[h]} for h in histories],
    }
    with Path(output).open('x') as out: out.write(json.dumps(fs(report),indent=2)+'\n')
    print(json.dumps(fs({k:v for k,v in report.items() if k in ['status','scope','components','product']}),indent=2))
    print('Exact product menu value:',lower)
    print('Optimal marginals:',fs(op),fs(oq))
    print('Per-position psi1:',fs(optimal['psi1']),'psi2:',fs(optimal['psi2']))
    print('Report:',output)

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    main(p.parse_args().output)
