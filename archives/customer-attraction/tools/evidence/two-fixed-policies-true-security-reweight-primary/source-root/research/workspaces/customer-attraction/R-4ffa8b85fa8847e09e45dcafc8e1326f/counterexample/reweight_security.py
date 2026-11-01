"""Attack the general bridge W >= n v_n on two existing complete policies.

This is a candidate falsification tool, not a finite-scale positive theorem.
Every weight LP uses all ordered-history SPE comparisons.  A positive result
is exported only after Fraction rechecking all those comparisons and every
static competition multiset, and checking that the topic subsets differ.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import gcd, lcm
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).parent


def load_policy(name):
    files = {
        'two_groups': 'evidence/certificates/customer_attraction/individual_security_failure.json',
        'allp89': 'evidence/certificates/customer_attraction/global_decorrelation_failure.json',
    }
    raw = json.loads((ROOT / files[name]).read_text())
    policy = {tuple(r['history']): r['action'] for r in raw['strategy']['actions']}
    n = max(map(len, policy)) + 1
    k = max(policy.values()) + 1
    assert len(policy) == sum(k**d for d in range(n))
    return n, k, policy


def prepare(name):
    n, k, policy = load_policy(name)
    masks = np.arange(1, 1 << k, dtype=np.int64)
    bits = np.array([[(b >> a) & 1 for b in masks] for a in range(k)], dtype=np.int64)
    denom = lcm(*range(1, n+1))

    def terminal(h):
        while len(h) < n:
            h += (policy[h],)
        return h

    def util(z, i):
        load = bits[list(z)].sum(axis=0)
        return bits[z[i]] * np.array([denom//x if x else 0 for x in load])

    gamma = []
    for d in range(n):
        for h in product(range(k), repeat=d):
            z = terminal(h)
            for a in range(k):
                row = util(z, d) - util(terminal(h+(a,)), d)
                if row.any():
                    gamma.append(row)
    gamma = np.unique(np.array(gamma), axis=0)
    path = terminal(())
    coverage = np.sign(bits[list(path)].sum(axis=0))
    rivals = list(combinations_with_replacement(range(k), n-1))
    reciprocal = np.array([1/(1+bits[list(b)].sum(axis=0)) for b in rivals])
    return n, k, policy, masks, bits, gamma, path, coverage, rivals, reciprocal


def main():
    rng = np.random.default_rng(20261024)
    reports = []
    for name in ('two_groups', 'allp89'):
        n,k,policy,masks,bits,gamma,path,cov,rivals,recip = prepare(name)
        starts = [np.ones(k)/k, np.array([0,0,.5,0,0,.5]),
                  np.array([0,.5,.5,0,0,0])]
        starts += list(rng.dirichlet(np.ones(k), size=32))
        best = None
        for start_id, p in enumerate(starts):
            for step in range(12):
                beta = recip * (p @ bits)
                objective = np.r_[cov, -n]
                constraints = np.vstack([np.c_[-gamma, np.zeros(len(gamma))],
                                         np.c_[-beta, np.ones(len(beta))]])
                r = linprog(objective, A_ub=constraints, b_ub=np.zeros(len(constraints)),
                            A_eq=[np.r_[np.ones(len(masks)),0]], b_eq=[1],
                            bounds=(0,None), method='highs')
                assert r.success, r.message
                w,t = r.x[:-1],r.x[-1]
                gap = -r.fun
                if best is None or gap > best['float_gap'] + 1e-10:
                    best = {'name':name,'n':n,'k':k,'start':start_id,'step':step,
                            'float_gap':gap, 'W':float(cov@w),'t':float(t),
                            'p':p.tolist(),'weights':w.tolist()}
                # Best exact safety query for these weights, on every static
                # rival multiset; this update never changes the full policy.
                queries = (recip * w) @ bits.T
                q = linprog(np.r_[np.zeros(k),-1],
                            A_ub=np.c_[-queries,np.ones(len(rivals))],
                            b_ub=np.zeros(len(rivals)),
                            A_eq=[np.r_[np.ones(k),0]],b_eq=[1],
                            bounds=(0,None),method='highs')
                assert q.success, q.message
                p2 = q.x[:-1]
                if np.max(np.abs(p2-p)) < 1e-9:
                    break
                p = p2
        # Export a positive candidate only after full exact certification.
        if best['float_gap'] > 1e-8:
            p = [F(float(x)).limit_denominator(10**6) for x in best['p']]
            p = [x/sum(p) for x in p]
            w = [F(float(x)).limit_denominator(10**6) for x in best['weights']]
            d = lcm(*(x.denominator for x in w))
            iw = [int(x*d) for x in w]
            g = gcd(*iw)
            iw = [x//g for x in iw]
            ic = [sum(int(c)*x for c,x in zip(row,iw)) for row in gamma]
            security = [sum(F(x)*sum(p[a] for a in range(k) if int(mask)>>a&1)
                            / (1+sum(int(mask)>>a&1 for a in B))
                            for mask,x in zip(masks,iw)) for B in rivals]
            W = sum(int(c)*x for c,x in zip(cov,iw))
            exact_gap = n*min(security)-W
            distinct = all(any(x and ((int(mask)>>a&1) != (int(mask)>>b&1))
                               for mask,x in zip(masks,iw))
                           for a in range(k) for b in range(a))
            best['exact'] = {'min_scaled_ic':min(ic),'security_lower':str(min(security)),
                             'W':W,'gap':str(exact_gap),'p':list(map(str,p)),
                             'distinct_topic_subsets':distinct}
            if min(ic) >= 0 and exact_gap > 0 and distinct:
                cert = {'identity':'counterexample to W>=n*v_n, not a half counterexample',
                        'players':n,'topics':k,'weights':{str(mask):x for mask,x in zip(masks,iw) if x},
                        'p':list(map(str,p)), 'strategy':[{'history':list(h),'action':a} for h,a in policy.items()],
                        'exact':best['exact']}
                (OUT/(name+'_positive_certificate.json')).write_text(json.dumps(cert,indent=2))
        best.pop('weights')
        reports.append(best)
    (OUT/'reweight_security_results.json').write_text(json.dumps(reports,indent=2))
    print(json.dumps(reports,indent=2))


if __name__ == '__main__':
    main()
