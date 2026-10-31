from itertools import product
import numpy as np
from scipy.optimize import linprog

def run(m,k,rule):
    masks=range(1,1<<k)
    def outcome(h):
        while len(h)<m: h=h+(rule(h),)
        return h
    def payoff(h,a):
        return np.array([int(mask>>a&1)/sum(mask>>x&1 for x in h) if mask>>a&1 else 0 for mask in masks])
    rows=[]
    for i in range(m):
        for h in product(range(k),repeat=i):
            a=rule(h); inc=payoff(outcome(h),a)
            for b in range(k): rows.append(inc-payoff(outcome(h+(b,)),b))
    actual=outcome(())
    u=payoff(actual,actual[0])
    best=None
    for opts in product(range(k),repeat=m):
        if tuple(sorted(opts))!=opts:continue
        obj=np.array([int(any(mask>>t&1 for t in opts)) for mask in masks])
        res=linprog(-obj,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[u],b_eq=[1],bounds=(0,None),method='highs')
        if res.success and (best is None or -res.fun>best[0]): best=(-res.fun,opts,res.x,actual)
    print('m',m,'k',k,'best',None if best is None else best[:2],flush=True)
    if best is not None:print([(i+1,round(w,7)) for i,w in enumerate(best[2]) if w>1e-7],flush=True)
if __name__=='__main__':
    def cross(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        group=range(3) if h[1]<3 else range(3,6)
        return next(x for x in group if x not in h)
    run(3,6,cross)
