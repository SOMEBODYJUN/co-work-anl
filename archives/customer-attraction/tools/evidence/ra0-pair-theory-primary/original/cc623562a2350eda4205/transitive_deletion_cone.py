"""Fixed full-policy, transitive customer cone attack to optimal-query deletion bridge.

Uniform query is security optimal by catalog automorphism averaging. A negative
result must still check the entire optimal-query face, not merely uniform.
"""
from itertools import product
from functools import lru_cache
from math import comb,lcm
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import linprog

def build(g,n):
    k=2*g;masks=np.arange(1,1<<k,dtype=int)
    inc=((masks[:,None]>>np.arange(k))&1)
    groups=[tuple(sorted((int(i[:g].sum()),int(i[g:].sum())))) for i in inc]
    orbits=sorted(set(groups));R=np.array([[int(t==o) for o in orbits] for t in groups])
    def policy(h):
        if not h:return 0
        if len(h)==1:return g if h[0]<g else 0
        choices=range(g) if h[1]<g else range(g,k)
        return next(a for a in choices if a not in h)
    @lru_cache(None)
    def finish(h):
        while len(h)<n:h+=(policy(h),)
        return h
    @lru_cache(None)
    def row(a,z):
        load=inc[:,list(z)].sum(axis=1)
        return (np.divide(inc[:,a],load,out=np.zeros(len(masks)),where=load!=0))@R
    G=[]
    for d in range(n):
        for h in product(range(k),repeat=d):
            z=finish(h);u=row(z[d],z)
            G.extend(u-row(a,finish(h+(a,))) for a in range(k) if a!=z[d])
    z=finish(());load=inc[:,list(z)].sum(axis=1)
    W=(load>0).astype(float)@R
    D=np.zeros(len(orbits))
    for i in range(n):
        for a in range(k):D+=row(a,z[:i]+(a,)+z[i+1:])/k
    size=R.sum(axis=0)
    return np.array(G),W-D,size,orbits,z

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--g',type=int,default=4);ap.add_argument('--n',type=int,default=4);ap.add_argument('--output',type=Path);args=ap.parse_args()
    G,c,size,orbits,z=build(args.g,args.n)
    # Customer normalization is total multiplicity.
    lp=linprog(c,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[size],b_eq=[1],bounds=(0,None),method='highs')
    if not lp.success:raise RuntimeError(lp.message)
    data=dict(status='floating fixed full-policy transitive cone screen; no general proof',g=args.g,n=args.n,orbits=orbits,path=z,weights=lp.x.tolist(),gap=lp.fun,rows=len(G))
    print(json.dumps(data),flush=True)
    if args.output:args.output.write_text(json.dumps(data,indent=2))
