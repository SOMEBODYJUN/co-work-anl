"""Test only the all-background aggregate reserve conjecture, not Q-CAG-HALF.
The q-player legal prefix consists of topic0 repeated q times.
Each tested cone is a fully specified history-dependent r-player suffix SPE.
"""
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction as Q
import json,random
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent

def attempt(n,r,q,seed):
    rng=random.Random(seed);masks=np.arange(1,1<<n,dtype=int)
    member=np.array([[(mask>>t)&1 for mask in masks] for t in range(n)],dtype=float)
    b=q*member[0]
    pol={};leaves={};ud={}
    def vector(z,t):
        den=b+sum((member[a] for a in z),np.zeros(len(masks)))
        return np.divide(member[t],den,out=np.zeros(len(masks)),where=den>0)
    # Fixed random positive weights choose a lawful exact policy except floating
    # comparison only discovers cones; output will require rational reconstruction.
    weights=np.array([rng.randrange(0,31) if rng.random()<.3 else 0 for _ in masks],dtype=float)
    if not weights.sum():weights[0]=1
    rows=[]
    for k in reversed(range(r)):
        for h in product(range(n),repeat=k):
            zs=[h+(a,) if k==r-1 else leaves[h+(a,)] for a in range(n)]
            coeff=[vector(z,a) for a,z in enumerate(zs)]
            vals=[float(c@weights) for c in coeff]
            best=max(vals);opts=[a for a,v in enumerate(vals) if abs(v-best)<1e-9]
            a=rng.choice(opts);pol[h]=a;leaves[h]=zs[a]
            for t in range(n):
                rows.append(coeff[t]-coeff[a])
    z=leaves[()];c=sum((member[a] for a in z),np.zeros(len(masks)))
    covered=c>0;fresh=b==0
    U=np.divide(c,b+c,out=np.zeros(len(masks)),where=b+c>0)
    V=covered*fresh+U
    best=None
    for ts in combinations(range(n),min(n,r)):
        beta=(sum((member[a] for a in ts),np.zeros(len(masks)))>0)*fresh
        obj=beta-V
        lp=linprog(-obj,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
        if lp.success and (best is None or -lp.fun>best[0]):best=(-float(lp.fun),ts,lp.x)
    if best and best[0]>1e-8:
        return {'n':n,'remaining':r,'prefix_repetitions':q,'seed':seed,'gap_float':best[0],'benchmark':best[1],'terminal':z,'types':{str(mask):str(Q(float(w)).limit_denominator(10**8)) for mask,w in zip(masks,best[2]) if w>1e-10},'policy':[{'history':h,'action':a} for h,a in sorted(pol.items(),key=lambda x:(len(x[0]),x[0]))]}
    return None

def main():
    records=[]
    for n,r,q in [(4,3,1),(5,3,1),(5,4,1),(5,3,3),(6,3,1),(6,4,1)]:
        for seed in range(12):
            result=attempt(n,r,q,10000*n+100*r+10*q+seed)
            if result:
                (HERE/'incumbent_reserve_cone_candidate.json').write_text(json.dumps(result,indent=2)+'\n')
                print(json.dumps({k:result[k] for k in ['n','remaining','prefix_repetitions','seed','gap_float','benchmark','terminal']}));return
        records.append({'topics':n,'remaining':r,'prefix_repetitions':q,'cones_tested':12})
    (HERE/'incumbent_reserve_cone_negative.json').write_text(json.dumps({'status':'finite pressure only; no theorem','tests':records},indent=2)+'\n')
    print(json.dumps(records))
if __name__=='__main__':main()
