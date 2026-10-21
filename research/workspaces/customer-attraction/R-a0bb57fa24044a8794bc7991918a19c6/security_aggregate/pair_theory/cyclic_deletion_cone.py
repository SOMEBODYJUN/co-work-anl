"""New transitive cyclic catalog cones; finite floating discovery only."""
import argparse,json,random
from pathlib import Path
from itertools import combinations_with_replacement
from math import lcm
import numpy as np
from scipy.optimize import linprog

def multis(k,n):
    for t in combinations_with_replacement(range(k),n):yield tuple(t.count(a) for a in range(k))

def space(k,n):
    masks=np.arange(1,1<<k,dtype=int);inc=(masks[:,None]>>np.arange(k))&1
    def orbit(mask):
        return min(((mask<<s)|(mask>>(k-s)))&((1<<k)-1) for s in range(k))
    labels=[orbit(int(t)) for t in masks];orbits=sorted(set(labels));R=np.array([[int(t==o) for o in orbits] for t in labels])
    terms=list(multis(k,n));tidx={q:i for i,q in enumerate(terms)}
    load=np.array(terms)@inc.T
    pay=np.einsum('tz,za,zo->tao',np.divide(1.,load,out=np.zeros(load.shape),where=load!=0),inc,R)
    W=(load>0).astype(float)@R
    Ds=np.where(load>0,(n+1)*inc.sum(axis=1)[None,:]/(k*(load+1)),n*inc.sum(axis=1)[None,:]/k)@R
    states=[q for d in range(n) for q in multis(k,d)]
    return dict(k=k,n=n,inc=inc,R=R,orbits=orbits,terms=terms,tidx=tidx,pay=pay,W=W,Ds=Ds,states=states,size=R.sum(axis=0))

def policy_cone(sp,w,rng):
    k=sp['k'];n=sp['n'];pay=sp['pay'];W=sp['W'];tidx=sp['tidx']
    # Exact utility comparison using common LCM denominator and integer weights.
    L=lcm(*range(1,n+1));up=np.rint(pay*L).astype(np.int64)@w;wp=W@w
    end={q:i for q,i in tidx.items()};policy={};G=[]
    for q in reversed(sp['states']):
        zs=[end[q[:a]+(q[a]+1,)+q[a+1:]] for a in range(k)]
        us=[up[z,a] for a,z in enumerate(zs)];best=max(us)
        candidates=[a for a,u in enumerate(us) if u==best]
        mincov=min(wp[zs[a]] for a in candidates);candidates=[a for a in candidates if wp[zs[a]]==mincov]
        a=rng.choice(candidates);end[q]=zs[a];policy[q]=a
        G.extend(pay[zs[a],a]-pay[z,b] for b,z in enumerate(zs) if b!=a)
    z=end[(0,)*k]
    return np.array(G),sp['W'][z]-sp['Ds'][z],dict(policy=[dict(counts=q,action=a) for q,a in policy.items()],terminal=sp['terms'][z])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=7);ap.add_argument('--n',type=int,default=4);ap.add_argument('--samples',type=int,default=2000);ap.add_argument('--seed',type=int,default=78193);ap.add_argument('--output',type=Path);args=ap.parse_args()
    rng=random.Random(args.seed);sp=space(args.k,args.n);best=None
    for i in range(args.samples):
        w=np.array([rng.randrange(1,15) if rng.random()<.5 else 0 for _ in sp['orbits']],dtype=np.int64)
        G,c,meta=policy_cone(sp,w,rng)
        lp=linprog(c,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[sp['size']],b_eq=[1],bounds=(0,None),method='highs')
        if not lp.success:raise RuntimeError(lp.message)
        if best is None or lp.fun<best['gap']-1e-9:
            best=dict(gap=lp.fun,weights=lp.x.tolist(),sample=i,**meta);print(json.dumps(dict(gap=lp.fun,terminal=meta['terminal'],sample=i)),flush=True)
        if lp.fun< -1e-8:break
    if args.output:args.output.write_text(json.dumps(dict(status='floating fixed complete count-policy cyclic cone screen; uniform query security-optimal by averaging; other optimal queries not checked',k=args.k,n=args.n,orbits=sp['orbits'],completed=i+1,best=best),indent=2))
