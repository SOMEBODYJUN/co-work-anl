"""Targeted falsification of BG-AGG: V_b >= r v_(r+1)(b).

A fixed rational query p yields a lower bound on v.  Every LP uses all ordered
histories of one complete strategy, a legal topic-count prefix, and every
multiset of r static competitors. Numerical lack of separation is not evidence
for the general candidate. This is exploratory, not a mathematical asset.
"""
import itertools as it, json, math, sys, time
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

rng=np.random.default_rng(482019)
output=Path(__file__).with_suffix('.json')
records=[]
best=-1e9
start=time.time()
for k,r in [(4,3),(5,3),(4,4),(5,4),(5,5)]:
    types=np.array([[bool(mask&(1<<a)) for a in range(k)] for mask in range(1,1<<k)],float)
    histories=[h for d in range(r) for h in it.product(range(k),repeat=d)]
    hist_desc=sorted(histories,key=lambda h:-len(h))
    leaf_counts={h:np.bincount(h,minlength=k) for h in it.product(range(k),repeat=r)}
    multis=list(it.combinations_with_replacement(range(k),r))
    for trial in range(30):
        b=rng.integers(0,5,size=k)
        if trial%3==0: b=np.array([rng.integers(1,25)]+[0]*(k-1))
        base=types@b
        coeff={h:types.T/np.maximum(1,base+types@counts)[None,:] for h,counts in leaf_counts.items()}
        w=rng.exponential(1,size=len(types))
        if trial%3==0: w*=rng.integers(0,2,size=len(types))
        leaves={h:h for h in leaf_counts}
        policy={}
        for h in hist_desc:
            opts=[h+(a,) for a in range(k)]
            vals=[coeff[leaves[ha]][ha[-1]]@w for ha in opts]
            choice=int(np.argmax(np.array(vals)+rng.uniform(0,1e-11,size=k)))
            policy[h]=choice;leaves[h]=leaves[opts[choice]]
        actual=leaves[()]
        V=sum(coeff[actual][a] for a in actual)
        rows=[]
        for h in histories:
            assigned=leaves[h]
            ua=coeff[assigned][policy[h]]
            for a in range(k):
                rows.append(np.r_[-ua+coeff[leaves[h+(a,)]][a],0.])
        p=rng.integers(1,5,size=k).astype(float);p/=p.sum()
        if trial%2==0:p=np.ones(k)/k
        q=types@p
        for z in multis:
            counts=np.bincount(z,minlength=k)
            query=q/(1+base+types@counts)
            rows.append(np.r_[-query,1.])
        objective=np.r_[V,-r]
        sol=linprog(objective,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=np.r_[np.ones(len(types)),0.][None,:],b_eq=[1.],bounds=[(0,None)]*(len(types)+1),method='highs')
        gap=-sol.fun if sol.success else None
        rec={'k':k,'r':r,'b':b.tolist(),'trial':trial,'p':p.tolist(),'gap':gap,'success':sol.success}
        records.append(rec)
        if gap is not None and gap>best:
            best=gap;print('BEST',rec,flush=True)
        if gap is not None and gap>1e-8:
            output.write_text(json.dumps({'claim':'BG-AGG','records':records,'positive':rec,'weights':sol.x[:-1].tolist(),'s':sol.x[-1],'policy':{','.join(map(str,h)):a for h,a in policy.items()}},indent=2))
            sys.exit(0)
        if time.time()-start>95:break
    if time.time()-start>95:break
output.write_text(json.dumps({'claim':'BG-AGG','records':records,'best':best,'status':'finite numerical non-separation only; no general evidence'},indent=2))
print('DONE',len(records),'best',best,'time',time.time()-start)
