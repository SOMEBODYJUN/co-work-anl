"""Discovery-only complete two-player reply cones, legal one-theme prefix."""
from pathlib import Path
from itertools import product
from fractions import Fraction
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).parent

def run(q,cases,seed,L):
    rng=random.Random(seed);masks=np.arange(1,2**q); inc=np.array([[(int(x)>>a)&1 for x in masks] for a in range(q)]);p=L*inc[0]
    utils=np.zeros((q,q,len(masks)))
    for a in range(q):
        for b in range(q):
            c=inc[a]+inc[b];utils[a,b]=np.divide(inc[a],p+c,out=np.zeros(len(masks)),where=c>0)
    fresh=(p==0);actual=1;B=2;T=3;S=4
    obj=utils[actual,B]+utils[B,actual]+fresh*np.maximum(inc[actual],inc[B])-fresh*np.maximum(inc[T],inc[S])
    best=0.; feasible=0;start=time.time()
    for i in range(cases):
        reply=[rng.randrange(q) for _ in range(q)];reply[actual]=B
        rows=[]
        for a in range(q):
            for b in range(q):
                if b!=reply[a]: rows.append(utils[b,a]-utils[reply[a],a])
        for a in range(q):
            if a!=actual: rows.append(utils[a,reply[a]]-utils[actual,B])
        res=linprog(obj,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
        if res.success:
            feasible+=1
            if res.fun<best-1e-8:
                data=dict(q=q,background=[0]*L,actual=actual,reply=reply,compare=[T,S],deficit=float(res.fun),weights={str(int(mask)):str(Fraction(float(w)).limit_denominator(1000000)) for mask,w in zip(masks,res.x) if w>1e-8},case=i,seed=seed)
                (HERE/'fresh_arbitrary_witness.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data),flush=True);return data
        if (i+1)%1000==0:print(json.dumps(dict(cases=i+1,feasible=feasible,seconds=time.time()-start)),flush=True)
    return dict(q=q,cases=cases,background_repetitions=L,feasible=feasible,best=best,seconds=time.time()-start)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--q',type=int,default=6);ap.add_argument('--cases',type=int,default=10000);ap.add_argument('--seed',type=int,default=71215);ap.add_argument('--background',type=int,default=1);args=ap.parse_args();data=run(args.q,args.cases,args.seed,args.background);(HERE/'fresh_arbitrary_probe.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
