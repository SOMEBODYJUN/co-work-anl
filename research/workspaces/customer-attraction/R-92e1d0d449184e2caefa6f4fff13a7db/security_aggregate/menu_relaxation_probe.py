"""Diagnostic only: root menus whose tails meet the aggregate-security bound.

This does not impose a continuation SPE. It attacks an explicitly proposed
one-step induction interface, using common nonnegative customer masses.
"""
import itertools, json
import numpy as np
from scipy.optimize import linprog


def feature(k, a, profile):
    return np.array([float(bool(t & (1 << a))) / sum(bool(t & (1 << b)) for b in profile)
                     if t & (1 << a) else 0.0 for t in range(1, 1 << k)])


def run(k=3, n=3):
    types = (1 << k)-1
    tails = list(itertools.combinations_with_replacement(range(k), n-1))
    opponents = list(itertools.combinations_with_replacement(range(k), n-2))
    queries = np.ones(k)/k
    # Fixed uniform local dual is a valid upper bound on each v_(n-1)(a).
    local = [[sum((feature(k, c, (a,c)+q) for q in opponents), np.zeros(types))/len(opponents)
              for c in range(k)] for a in range(k)]
    static = [sum((queries[a]*feature(k,a,(a,)+b) for a in range(k)), np.zeros(types))
              for b in tails]
    best = None
    for menu in itertools.product(tails, repeat=k):
        root = [feature(k,a,(a,)+menu[a]) for a in range(k)]
        actual = (0,)+menu[0]
        cover = np.array([float(any(t & (1 << a) for a in actual)) for t in range(1,1 << k)])
        rows = []
        for a in range(k):
            rows.append(np.r_[root[a]-root[0],0])
            tailpay = sum((feature(k,b,(a,)+menu[a]) for b in menu[a]), np.zeros(types))
            rows.extend(np.r_[(n-1)*v-tailpay,0] for v in local[a])
        rows.extend(np.r_[-f,1] for f in static)
        result = linprog(np.r_[cover,-n], A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                         A_eq=[np.r_[np.ones(types),0]], b_eq=[1], bounds=[(0,None)]*(types+1), method='highs')
        if result.success and (best is None or result.fun < best['gap']):
            best={'gap':float(result.fun),'k':k,'n':n,'menu':menu,'weights':result.x[:-1].tolist(),'t':float(result.x[-1])}
    return best


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
