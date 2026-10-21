"""Alternating finite attack on the lowest-static-CCE welfare bridge.

The CCE dual multipliers are fixed during each customer-weight LP. All
full ordered-history SPE constraints are kept. A candidate is valid only
after rational reconstruction checks all node deviations and dual columns.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import ROOT, counts, benchmark
from customer_attraction import Instance, CustomerType, ExactSPESolver


def terminal(actions, history, m):
    h = tuple(history)
    while len(h) < m:
        h += (actions[h],)
    return h


def rows(actions, m, k):
    masks = range(1, 1 << k)
    def utility(hist, pos, mask):
        load = sum((mask >> a) & 1 for a in hist)
        return F(1, load) if mask >> hist[pos] & 1 else F(0)
    G = []
    for h, chosen in actions.items():
        t = len(h)
        actual = terminal(actions, h, m)
        for a in range(k):
            if a == chosen:
                continue
            dev = terminal(actions, h + (a,), m)
            G.append([utility(actual, t, b) - utility(dev, t, b) for b in masks])
    path = terminal(actions, (), m)
    W = [F(any(mask >> a & 1 for a in path)) for mask in masks]
    profiles = list(counts(m, k))
    C = [[F(any(q[a] and (mask >> a & 1) for a in range(k))) for mask in masks] for q in profiles]
    regret = []
    for a in range(k):
        block = []
        for q, c in zip(profiles, C):
            row = []
            for mask, w in zip(masks, c):
                load = sum(q[t] for t in range(k) if mask >> t & 1)
                mg = (F(m) if load == 0 else F(m + 1, load + 1)) if mask >> a & 1 else F(0)
                row.append(w - mg)
            block.append(row)
        regret.append(block)
    return G, W, C, regret, path


def reconstruct(weights, actions, m, k, lam, data):
    G, W, C, regret, path = data
    vec = [F(float(x)).limit_denominator(10**7) for x in weights]
    mult = [F(x) for x in lam]
    spe_slacks = [sum(a*b for a,b in zip(row, vec)) for row in G]
    welfare = sum(a*b for a,b in zip(W, vec))
    lower = []
    for j, row in enumerate(C):
        dual_row = [row[t] - sum(mult[a]*regret[a][j][t] for a in range(k)) for t in range(len(vec))]
        lower.append(sum(a*b for a,b in zip(dual_row, vec)))
    gamma = min(lower)
    valid = min(vec) >= 0 and min(mult) >= 0 and min(spe_slacks, default=F(0)) >= 0 and gamma > welfare
    return {'valid_strict_failure': valid, 'W':str(welfare), 'CCE_lower':str(gamma),
            'gap':str(gamma-welfare), 'min_SPE_slack':str(min(spe_slacks, default=F(0))),
            'weights':{str(i+1):str(x) for i,x in enumerate(vec) if x},
            'lambda':list(map(str,mult)), 'path':list(path),
            'actions':[[list(h),a] for h,a in sorted(actions.items(),key=lambda x:(len(x[0]),x[0]))]}


def iterate(actions, inst, rounds=8):
    m,k=inst.players,inst.topic_count
    data=rows(actions,m,k)
    G,W,C,R,path=data
    lam=benchmark(inst)['deviation_multipliers']
    trace=[]
    for it in range(rounds):
        H=[[float(C[j][t]-sum(F(lam[a])*R[a][j][t] for a in range(k)))
            for t in range(len(W))] for j in range(len(C))]
        # gamma <= every genuine static profile's dual expression.
        aub=np.vstack([np.column_stack([-np.array(G,float), np.zeros(len(G))]),
                       np.column_stack([-np.array(H,float), np.ones(len(H))])])
        res=linprog([0.0]*len(W)+[-1.0],A_ub=aub,b_ub=np.zeros(len(aub)),
                    A_eq=[list(map(float,W))+[0.0]],b_eq=[1.0],
                    bounds=[(0,None)]*len(W)+[(None,None)],method='highs')
        if not res.success:
            return {'status':res.message,'trace':trace}
        candidate=reconstruct(res.x[:-1],actions,m,k,lam,data)
        trace.append({'round':it,'numeric_lower':res.x[-1],'rational':candidate})
        if candidate['valid_strict_failure']:
            return {'status':'exact_counterexample','trace':trace}
        ww=res.x[:-1]
        # Positive integer scaling perturbs only the next discovery iteration.
        rounded=[max(0,round(float(x)*10**6)) for x in ww]
        game=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),v)
                     for mask,v in enumerate(rounded,1) if v),m)
        newlam=benchmark(game)['deviation_multipliers']
        if newlam==lam:
            break
        lam=newlam
    return {'status':'no_exact_failure_in_this_run','trace':trace}


def main():
    base=ROOT/'research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c'
    raw=json.loads((base/'dynamic_security/strong_iid_472_five_topics.json').read_text())
    inst=Instance(tuple(map(str,raw['topics'])),tuple(CustomerType(frozenset(a for a in raw['topics'] if int(mask)>>a&1),v)
                  for mask,v in raw['weights'].items()),raw['players'])
    actions={tuple(h):a for h,a in raw['actions']}
    out={'strong_iid_policy':iterate(actions,inst)}
    pne=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction/worst_pne_welfare_failure.json').read_text()))
    solver=ExactSPESolver(pne)
    cert=solver.worst_certificate()
    out['pne_policy']=iterate(dict(cert.actions),pne)
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
