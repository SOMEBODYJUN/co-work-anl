import numpy as np
from scipy.optimize import linprog
from functools import lru_cache
from itertools import combinations_with_replacement, combinations
import random, json
from pathlib import Path

def run(m,k,n=100):
    rng=np.random.default_rng(138+m)
    masks=np.arange(1,1<<k)
    member=((masks[:,None]>>np.arange(k))&1).astype(float)
    profiles=list(combinations_with_replacement(range(k),m))
    @lru_cache(None)
    def pay(q,a):
        q=np.array(q)
        loads=member@q
        return np.divide(member[:,a],loads,out=np.zeros(len(masks)),where=loads>0)
    def incr(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
    allstates=[]
    for depth in range(m):
        for h in combinations_with_replacement(range(k),depth):
            q=tuple(h.count(a) for a in range(k));allstates.append(q)
    optsets=list(combinations(range(k),min(m,k)))
    best=0
    x=rng.exponential(1,size=len(masks))
    for t in range(n):
        if t%10==0:x=rng.exponential(1,size=len(masks))*(rng.random(len(masks))<.4)
        acts={};outs={}
        for q in reversed(allstates):
            cand=[incr(q,a) if sum(q)==m-1 else outs[incr(q,a)] for a in range(k)]
            vals=[pay(cand[a],a)@x for a in range(k)]
            a=max(range(k),key=lambda a:(vals[a]+rng.uniform(0,1e-9)))
            acts[q]=a;outs[q]=cand[a]
        zero=(0,)*k;out=outs[zero];a=acts[zero];u=pay(out,a)
        rows=[]
        for q in allstates:
            inc=pay(outs[q],acts[q])
            for b in range(k):
                child=incr(q,b);ob=child if sum(child)==m else outs[child]
                row=inc-pay(ob,b)
                if np.max(np.abs(row))>1e-10:rows.append(row)
        support=optsets[t%len(optsets)]
        obj=(member[:,support].sum(axis=1)>0).astype(float)
        res=linprog(-obj,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[u],b_eq=[1],bounds=(0,None),method='highs')
        if res.success:
            ratio=-res.fun
            if ratio>best+1e-6:
                best=ratio
                print(m,k,t,best,support,out,flush=True)
                data={'m':m,'k':k,'ratio':ratio,'opt':support,'out':out,'weights':[(int(a),float(v)) for a,v in zip(masks,res.x) if v>1e-7], 'acts':[[list(q),a] for q,a in acts.items()]}
                Path(__file__).with_name(f'first_floor_best_{m}_{k}.json').write_text(json.dumps(data,indent=2))
            if ratio>2*m-1+1e-6:return
            x=res.x+rng.exponential(.001,size=len(masks))
        else:x=rng.exponential(1,size=len(masks))
    print('DONE',m,k,best,flush=True)
if __name__=='__main__':
    import sys
    run(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)>3 else 100)
