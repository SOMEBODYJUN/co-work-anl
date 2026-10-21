"""Fixed-policy cone attack on P + new coverage >= fresh OPT_2.

Every background is the legal prefix consisting of repetitions of action 0.
This is a floating discovery search; positive deficits require exact audit.
"""
from itertools import combinations_with_replacement
from pathlib import Path
import argparse, json, random, time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).parent

def run(q, cases, seed, max_background):
    rng=random.Random(seed)
    masks=np.arange(1,2**q)
    inc=np.array([[(int(x)>>a)&1 for x in masks] for a in range(q)])
    pairs=list(combinations_with_replacement(range(q),2))
    found=None; best=0.; solved=0; seen=set(); started=time.time()
    for case in range(cases):
        L=1+case%max_background
        p=L*inc[0]
        utils=np.zeros((q,q,len(masks)))
        for a in range(q):
            for b in range(q):
                c=inc[a]+inc[b]
                utils[a,b]=np.divide(inc[a],p+c,out=np.zeros(len(masks)),where=c>0)
        wt=np.array([rng.expovariate(1)*rng.choice((0,0,0,1,1,3)) for _ in masks])
        if not wt.any(): continue
        response=[]
        for a in range(q):
            vals=np.array([utils[b,a]@wt for b in range(q)])
            mx=max(vals); choices=np.flatnonzero(vals>=mx-1e-9)
            response.append(int(rng.choice(list(choices))))
        pay=[utils[a,response[a]]@wt for a in range(q)]
        actual=int(max(range(q),key=lambda a:pay[a]+rng.random()*1e-9))
        key=(L,actual,tuple(response))
        if key in seen: continue
        seen.add(key)
        rows=[]
        for a in range(q):
            chosen=response[a]
            for b in range(q):
                if b!=chosen: rows.append(utils[b,a]-utils[chosen,a])
        for a in range(q):
            if a!=actual: rows.append(utils[a,response[a]]-utils[actual,response[actual]])
        A=np.array(rows)
        B=response[actual]
        fresh=(p==0)
        current=utils[actual,B]+utils[B,actual]+fresh*np.maximum(inc[actual],inc[B])
        for T,S in pairs:
            obj=current-fresh*np.maximum(inc[T],inc[S])
            res=linprog(obj,A_ub=A,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
            solved+=1
            if res.success and res.fun<best-1e-9:
                best=float(res.fun)
                found=dict(q=q,background=[0]*L,actual=actual,reply=response,compare=[T,S],deficit=best,weights={str(int(mask)):float(w) for mask,w in zip(masks,res.x) if w>1e-9},case=case,seed=seed)
                (HERE/'fresh_global_two_best.json').write_text(json.dumps(found,indent=2)+'\n')
                print(json.dumps(found),flush=True)
                if best < -1e-8: return dict(cases=case+1,policies=len(seen),solved=solved,best=best,seconds=time.time()-started,found=found)
        if (case+1)%100==0: print(json.dumps(dict(progress=case+1,policies=len(seen),solved=solved,best=best,seconds=time.time()-started)),flush=True)
    return dict(cases=cases,policies=len(seen),solved=solved,best=best,seconds=time.time()-started,found=found)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--q',type=int,default=6); ap.add_argument('--cases',type=int,default=2000);ap.add_argument('--seed',type=int,default=71213);ap.add_argument('--max-background',type=int,default=4);ap.add_argument('--output',default='fresh_global_two_probe.json');args=ap.parse_args()
    result=run(args.q,args.cases,args.seed,args.max_background)
    (HERE/args.output).write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result))
