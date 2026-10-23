"""Finite diagnostic of a new one-step aggregate induction interface.

No continuation rationality is asserted: a witness only refutes the stated
root-menu implication. Stops immediately at a strict floating candidate.
"""
import itertools, json
import numpy as np
from scipy.optimize import linprog
from menu_relaxation_probe import feature


def security(matrix):
    k,b=matrix.shape
    result=linprog(np.r_[np.zeros(b),1], A_ub=np.c_[matrix,-np.ones(k)], b_ub=np.zeros(k),
                   A_eq=[np.r_[np.ones(b),0]], b_eq=[1], bounds=[(0,None)]*b+[(None,None)],method='highs')
    return result.fun,result.x[:-1]


def diagnostic(k=4,n=3,iterations=2000):
    rng=np.random.default_rng(19274)
    tails=list(itertools.combinations_with_replacement(range(k),n-1))
    opp=list(itertools.combinations_with_replacement(range(k),n-2))
    R=np.array([[feature(k,a,(a,)+b) for b in tails] for a in range(k)])
    T=np.array([[sum((feature(k,c,(a,)+b) for c in b),np.zeros((1<<k)-1)) for b in tails] for a in range(k)])
    C=np.array([[float(any(t & (1<<c) for c in (a,)+b)) for t in range(1,1<<k)] for a in range(k) for b in tails]).reshape(k,len(tails),-1)
    L=np.array([[[feature(k,c,(a,c)+b) for b in opp] for c in range(k)] for a in range(k)])
    incumbent=None
    for iteration in range(iterations):
        w=rng.integers(0,10,(1<<k)-1).astype(float)
        w*=rng.random(len(w))<.45
        if not np.sum(w): continue
        v,_=security(R@w)
        local=[security(L[a]@w) for a in range(k)]
        values=R@w; totals=T@w
        allowed=totals>=np.array([x[0] for x in local])[:,None]*(n-1)-1e-8
        minima=np.min(np.where(allowed,values,np.inf),axis=1)
        minimum=max(minima)
        choices=np.argmin(np.where(allowed,values,np.inf),axis=1)
        feasible=allowed & (values>=minimum-1e-8)
        score=np.where(feasible,C@w-n*v,np.inf)
        a,j=np.unravel_index(np.argmin(score),score.shape)
        gap=score[a,j]
        if incumbent is None or gap<incumbent['gap']:
            menu=[tails[x] for x in choices]; menu[a]=tails[j]
            incumbent={'gap':float(gap),'iteration':iteration,'k':k,'n':n,'actual_action':int(a),
                       'weights':w.tolist(),'menu':menu,'v':float(v),'local_values':[float(x[0]) for x in local],
                       'local_duals':[x[1].tolist() for x in local]}
        if gap < -1e-7:
            return incumbent
    return incumbent


if __name__=='__main__':
    print(json.dumps(diagnostic(),indent=2))
