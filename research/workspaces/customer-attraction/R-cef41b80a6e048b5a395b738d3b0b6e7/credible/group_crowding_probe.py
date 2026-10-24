"""One explicit nonabsorbing all-history counterexample candidate.

There are g groups of two labels. Until a group repeats, prescribe the first
label of a fresh group; at the last node prescribe the opposite label of the
previous group. Once a group repeats, follow the most recently used repeated
group and balance its two labels. This tries to deter early joining by later
crowding while leaving many early singleton groups on the actual path.

The LP varies all unit-client type multiplicities, retains EVERY history IC,
and tests a designated m-topic comparison. This is not an unrestricted scan.
"""
from itertools import product
from functools import lru_cache
import json
import numpy as np
from scipy.optimize import linprog


def test(m=5,g=4):
    q=2*g
    masks=np.arange(1,1<<q)
    inc=np.array([((masks>>a)&1) for a in range(q)],dtype=float)
    def policy(h):
        counts=[sum(a//2==j for a in h) for j in range(g)]
        repeated={j for j,c in enumerate(counts) if c>=2}
        if repeated:
            chosen=next(a//2 for a in reversed(h) if a//2 in repeated)
            a,b=2*chosen,2*chosen+1
            return a if h.count(a)<=h.count(b) else b
        fresh=[j for j,c in enumerate(counts) if c==0]
        if len(h)==m-1 or not fresh:
            return h[-1]^1
        return 2*fresh[0]
    @lru_cache(None)
    def leaf(h):
        return h if len(h)==m else leaf(h+(policy(h),))
    def value(a,z):
        load=np.sum(inc[list(z)],axis=0)
        return np.divide(inc[a],load,out=np.zeros_like(load),where=load>0)
    rows=[]
    nodes=0
    for d in range(m):
        for h in product(range(q),repeat=d):
            nodes+=1
            a=policy(h)
            good=value(a,leaf(h))
            for b in range(q):
                if b!=a:
                    rows.append(value(b,leaf(h+(b,)))-good)
    actual=leaf(())
    comparison=tuple(range(1,2*(m-2),2))+(2*g-2,2*g-1)
    assert len(comparison)==m
    W=np.maximum.reduce(inc[list(actual)])
    O=np.maximum.reduce(inc[list(comparison)])
    res=linprog(-O,A_ub=np.asarray(rows),b_ub=np.zeros(len(rows)),
                A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
    out={'candidate':'fresh-singletons then terminal pair; crowd any earlier joined group',
         'm':m,'groups':g,'actual':actual,'comparison':comparison,
         'all_ordered_decision_histories':nodes,'IC_rows':len(rows),
         'status':res.message}
    if res.success:
        out['comparison_over_W']=-res.fun
        out['positive_types']=[(int(b),float(w)) for b,w in zip(masks,res.x) if w>1e-8]
    return out


if __name__=='__main__':
    print(json.dumps(test(),indent=2))
