"""Numerical discovery only: full reverse-group policy, arbitrary legal background.

Tests the stronger *residual* assertion sum current-player payoffs >= r v_r(b),
which is not claimed to follow from the root aggregate-security conjecture.
All strategy rows are genuine ordered-history comparisons.  Finite local
alternating LP failures/successes do not establish a universal statement.
"""
from pathlib import Path
from functools import lru_cache
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent

def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for a in range(n+1):
        for tail in compositions(n-a, k-1):
            yield (a,)+tail

def policy(h):
    if not h:
        return 0
    if len(h)==1:
        return 3 if h[0]<3 else 0
    group = range(0,3) if h[1]<3 else range(3,6)
    return next(a for a in group if a not in h)

def build(prefix, objective='residual'):
    k=6; r=3
    masks=np.arange(1,(1<<k)-1)  # omit universal indifference ray
    bits=np.array([[(t>>a)&1 for a in range(k)]for t in masks],float)
    base=bits@np.array(prefix)
    @lru_cache(None)
    def finish(h):
        return h if len(h)==r else finish(h+(policy(h),))
    def pay(a,z):
        loads=base+bits@np.bincount(z,minlength=k)
        return bits[:,a]/np.maximum(loads,1)
    rows=[]
    for depth in range(r):
        for h in product(range(k),repeat=depth):
            chosen=policy(h)
            own=pay(chosen,finish(h))
            for a in range(k):
                row=own-pay(a,finish(h+(a,)))
                if np.max(np.abs(row))>1e-12: rows.append(row)
    gamma=np.array(rows)
    background=np.array(list(compositions(r-1,k)))
    loads=base[None,:]+background@bits.T
    coeff=bits[None,:,:]/(1+loads[:,:,None])
    # The claim compares residual profit, not total coverage including prefix.
    z=finish(())
    cover=(sum((pay(a,z) for a in z), np.zeros(len(masks)))
      if objective=='residual' else pay(z[0],z))
    return masks,gamma,coeff,cover

def query(w,coeff):
    mat=np.einsum('bta,t->ba',coeff,w)
    k=mat.shape[1]
    res=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-mat,np.ones(len(mat))],
      b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],
      bounds=[(0,None)]*k+[(None,None)],method='highs')
    assert res.success,res.message
    return res.x[:-1],res.x[-1]

def solve(prefix,p):
    masks,gamma,coeff,cover=build(prefix)
    prev=None
    for it in range(15):
        beta=coeff@p
        res=linprog(np.r_[cover,-3],
          A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]],
          b_ub=np.zeros(len(gamma)+len(beta)),
          A_eq=[np.r_[np.ones(len(masks)),0]],b_eq=[1],
          bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
        if not res.success: return None
        w=res.x[:-1];p,v=query(w,coeff)
        gap=3*v-cover@w
        if prev is not None and abs(gap-prev)<1e-10: break
        prev=gap
    return dict(prefix=prefix,gap=gap,v=v,residual_profit=float(cover@w),p=p.tolist(),
      weights=[(int(t),float(x))for t,x in zip(masks,w)if x>1e-9])

def main():
    rng=np.random.default_rng(373)
    # Symmetry: a background is invariant under label permutations inside groups.
    prefixes=[q for d in range(7) for q in compositions(d,6)
      if q[:3]==tuple(sorted(q[:3],reverse=True)) and q[3:]==tuple(sorted(q[3:],reverse=True))]
    best=None;trace=[]
    for q in prefixes:
        starts=[np.ones(6)/6]+[rng.dirichlet(np.ones(6))for _ in range(3)]
        for p in starts:
            item=solve(q,p)
            if item is None: continue
            trace.append(item)
            if best is None or item['gap']>best['gap']+1e-10:
                best=item
                print(json.dumps(dict(best=best,checked=len(trace))),flush=True)
            if item['gap']>1e-7:
                (HERE/'background_security_probe.json').write_text(json.dumps(dict(best=best,trace=trace),indent=2))
                return
    (HERE/'background_security_probe.json').write_text(json.dumps(dict(best=best,trace=trace),indent=2))
    print(json.dumps(dict(prefixes=len(prefixes),starts=len(trace),best=best)),flush=True)

if __name__=='__main__':main()
