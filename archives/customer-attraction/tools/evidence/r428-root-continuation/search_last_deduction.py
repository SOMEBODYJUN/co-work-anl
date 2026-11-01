"""Finite attack on candidate F_k(b) <= 2 R_actual - u_last.

Floating point is used only to find candidates; no zero-counterexample theorem.
"""
from functools import lru_cache
from itertools import product
import json, random, sys
import numpy as np

def compositions(n,q):
    if q==1:
        yield (n,)
    else:
        for a in range(n+1):
            for c in compositions(n-a,q-1):
                yield (a,)+c

def run(seed=117,trials=1000,q=5,k=3,prefix=0):
    rng=random.Random(seed)
    masks=np.array(list(product((0,1),repeat=q))[1:],dtype=float)
    inc=np.eye(q,dtype=int)
    for trial in range(trials):
        weights=np.array([rng.randrange(0,12) if rng.random()<.55 else 0 for z in masks],dtype=float)
        b=np.array([rng.randrange(prefix+1) for _ in range(q)],dtype=int)
        # A legal background is a nonnegative integral combination of catalog actions.
        bg=masks@b
        terminals=list(compositions(k,q))
        loads=masks@np.array(terminals).T
        R=np.where(loads>0,loads/np.maximum(1,bg[:,None]+loads),0)
        profits=weights@R
        pay=np.array([masks.T@(weights/np.maximum(1,bg+loads[:,z])) for z in range(len(terminals))])
        F=max(profits)
        floors={}
        @lru_cache(None)
        def outcomes(c):
            if sum(c)==k:
                return frozenset((terminals.index(c),))
            children=[outcomes(tuple(np.array(c)+a)) for a in inc]
            floor=max(min(pay[z,a] for z in child) for a,child in enumerate(children))
            floors[c]=floor
            return frozenset(z for a,child in enumerate(children) for z in child if pay[z,a]>=floor-1e-9)
        root=(0,)*q
        outs=outcomes(root)
        for z in outs:
            if F<=2*profits[z]-max(pay[z])+1e-8:
                continue
            target=terminals[z]
            @lru_cache(None)
            def paths(c):
                if sum(c)==k:
                    return [()]
                return [(a,)+s for a in range(q) if c[a]<target[a] and pay[z,a]>=floors[c]-1e-9
                        and z in outcomes(tuple(np.array(c)+inc[a]))
                        for s in paths(tuple(np.array(c)+inc[a]))]
            for path in paths(root):
                if F>2*profits[z]-pay[z,path[-1]]+1e-8:
                    result=dict(trial=trial,seed=seed,q=q,k=k,background=b.tolist(),masks=masks.astype(int).tolist(),weights=weights.astype(int).tolist(),F=F,R=profits[z],path=path,payoffs=[pay[z,a] for a in path],gap=F-2*profits[z]+pay[z,path[-1]])
                    print(json.dumps(result));return result
        if trial%100==0:
            print(f"checked {trial}",file=sys.stderr,flush=True)
    print(json.dumps(dict(trials=trials,q=q,k=k,prefix=prefix,status="no_hit")))

if __name__=='__main__':
    run(*map(int,sys.argv[1:]))
