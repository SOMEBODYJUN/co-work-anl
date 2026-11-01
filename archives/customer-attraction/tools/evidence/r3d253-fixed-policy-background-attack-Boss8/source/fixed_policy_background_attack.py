"""Test the general background-security bridge on a history-complete policy cone.

Only discovery: no negative answer means no mathematical conclusion.
"""
import json
import sys
import numpy as np
from scipy.optimize import linprog
from background_security_attack import compositions


def policy(history):
    if not history:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    group = range(3) if history[1] < 3 else range(3,6)
    return next(a for a in group if a not in history)


def all_histories(p,r):
    yield ()
    level=[()]
    for _ in range(1,r):
        level=[h+(a,) for h in level for a in range(p)]
        yield from level


def attack(prefix, queries, rng):
    p,r=6,3
    masks=np.arange(1,2**p)
    inc=np.array([[(int(mask)>>a)&1 for a in range(p)] for mask in masks])
    base=inc@np.array(prefix)

    def terminal(h):
        while len(h)<r:
            h=h+(policy(h),)
        return h

    def coefficients(h,who):
        load=base+inc[:,h].sum(axis=1)
        return inc[:,h[who]]/np.where(load>0,load,1)

    rows=[]
    for h in all_histories(p,r):
        actual=terminal(h)
        cur=len(h)
        for a in range(p):
            dev=terminal(h+(a,))
            rows.append(coefficients(actual,cur)-coefficients(dev,cur))
    gamma=np.array(rows)
    actual=terminal(())
    load=inc[:,actual].sum(axis=1)
    welfare=load/np.where(base+load>0,base+load,1)
    backgrounds=list(compositions(r-1,p))
    static=np.array([inc.T/(1+base+inc@np.array(k)) for k in backgrounds])
    best=0
    for it in range(queries):
        q=np.ones(p)/p if it==0 else rng.dirichlet(np.ones(p)*rng.choice([.1,1,10]))
        fp=np.einsum('bam,a->bm',static,q)
        lp=linprog(np.r_[welfare,-r],
             A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],
                        np.c_[-fp,np.ones(len(backgrounds))]],
             b_ub=np.zeros(len(gamma)+len(backgrounds)),
             A_eq=[np.r_[np.ones(len(masks)),0]],b_eq=[1],
             bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
        if not lp.success: raise RuntimeError(lp.message)
        if lp.fun < best:
            best=lp.fun
            if best < -1e-8:
                return {"prefix":prefix,"query":q.tolist(),"gap":float(lp.fun),
                        "weights":{int(a):float(w) for a,w in zip(masks,lp.x[:-1]) if w>1e-10}}
    return None


if __name__=='__main__':
    rng=np.random.default_rng(102)
    trials=int(sys.argv[1]) if len(sys.argv)>1 else 100
    for it in range(trials):
        prefix=tuple(int(a) for a in rng.choice([0,0,1,2,4,8],size=6))
        found=attack(prefix,30,rng)
        if found:
            print(json.dumps({"iteration":it,**found}),flush=True)
            break
    else:
        print(json.dumps({"status":"no negative numerical candidate","trials":trials}),flush=True)
