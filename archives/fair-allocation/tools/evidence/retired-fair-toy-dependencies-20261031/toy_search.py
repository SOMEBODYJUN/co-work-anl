"""Exact integer toy tests; no search result is promoted to a theorem.
Seeds and ranges are fixed below. Python 3 + numpy. Run from any directory.
"""
from itertools import combinations, product, permutations
from random import Random
import json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

def equal_partitions(items,n,q):
    if n==1:
        yield (tuple(items),);return
    first=items[0]
    for rest in combinations(items[1:],q-1):
        b=(first,)+rest;bs=set(b)
        for tail in equal_partitions(tuple(x for x in items if x not in bs),n-1,q):
            yield (b,)+tail

def mms_trials(n,q,values,trials,seed):
    rng=np.random.default_rng(seed);m=n*q
    blocks=list(combinations(range(m),q));ix={b:i for i,b in enumerate(blocks)}
    parts=np.array([[ix[b] for b in p] for p in equal_partitions(tuple(range(m)),n,q)],dtype=np.int32)
    incidence=np.zeros((len(blocks),m),dtype=np.int16)
    for k,b in enumerate(blocks):incidence[k,list(b)]=1
    allocs=np.concatenate([parts[:,p] for p in permutations(range(n))],axis=0)
    max_ratio=(1,1);bad=None;max_witness=None
    for t in range(trials):
        costs=rng.choice(np.array(values,dtype=np.int16),size=(n,m))
        sums=costs@incidence.T
        mus=np.max(sums[:,parts],axis=2).min(axis=1)
        assigned=sums[np.arange(n)[:,None],allocs.T]
        feasible=np.all(assigned<=mus[:,None],axis=0)
        if not feasible.any():
            # exact optimum ratio by rational cross multiplication over candidate ratios
            best=None
            for a in assigned.T:
                pairs=[(int(x),int(mu)) for x,mu in zip(a,mus) if mu]
                r=max(pairs,key=lambda z:z[0]/z[1]) if pairs else (1,1)
                if best is None or r[0]*best[1]<best[0]*r[1]:best=r
            bad={'trial':t,'costs':costs.tolist(),'mms':mus.tolist(),'best_ratio':best};break
    return {'n':n,'q':q,'values':list(values),'requested_trials':trials,'completed_trials':t+1,'seed':seed,'unlabelled_partitions':len(parts),'labelled_allocations':len(allocs),'first_failure':bad}

def mixed_efx(n,edges,profile,orient,include_zero_own=False):
    bundles=[[] for _ in range(n)]
    for e,z in enumerate(orient):bundles[edges[e][z]].append(e)
    def val(i,e):
        u,v=edges[e]
        return profile[e][0] if i==u else profile[e][1] if i==v else 0
    totals=[[sum(val(i,e) for e in b) for b in bundles] for i in range(n)]
    for i in range(n):
        own=totals[i][i]
        for j in range(n):
            if own>=totals[i][j]:continue
            for e in bundles[i]:
                if val(i,e)<0 or include_zero_own and val(i,e)==0:
                    if own-val(i,e)<totals[i][j]:return False
            for e in bundles[j]:
                if val(i,e)>0 and own<totals[i][j]-val(i,e):return False
    return True

def cycle_trials(k,values=(-1,1),seed=20261020,trials=None):
    edges=[(i,(i+1)%k) for i in range(k)];ends=list(product(values,repeat=2))
    profiles=product(ends,repeat=k)
    if trials is not None:
        rng=Random(seed);profiles=(tuple(rng.choice(ends) for _ in edges) for t in range(trials))
    orientations=list(product((0,1),repeat=k));counter=None;done=0
    for p in profiles:
        done+=1
        if not any(mixed_efx(k,edges,p,o,True) for o in orientations):counter=p;break
    return {'graph':'cycle','vertices':k,'endpoint_values':list(values),'seed':seed if trials else None,'profiles_checked':done,'exhaustive':trials is None,'no_EFXplus0_witness':counter}

def optimal_alpha_demo(delta=5):
    # costs [[delta,1,0],[delta,0,1]]; exact all 2^3 allocations
    C=[[delta,1,0],[delta,0,1]];best=None;opts=[]
    for a in product(range(2),repeat=3):
        bs=[[e for e in range(3) if a[e]==i] for i in range(2)]
        sc=sum(C[i][e] for i in range(2) for e in bs[i])
        if sc!=delta:continue
        alpha=(1,1)
        for i in range(2):
            for j in range(2):
                for e in bs[i]:
                    num=sum(C[i][f] for f in bs[i] if f!=e);den=sum(C[i][f] for f in bs[j])
                    if den==0 and num:alpha=('inf',1);break
                    if den and num*alpha[1]>alpha[0]*den:alpha=(num,den)
        opts.append({'assignment':a,'alpha':alpha})
    return {'delta':delta,'costs':C,'minimum_social_cost':delta,'optimal_allocations':opts}

if __name__=='__main__':
    out={'mms':[], 'mixed_graphs':[], 'discarded_alpha_idea':optimal_alpha_demo()}
    out['mms'].append(mms_trials(3,3,(0,1,2),10000,20261020))
    out['mms'].append(mms_trials(3,3,(1,2,3),10000,20261021))
    out['mms'].append(mms_trials(3,3,(1,2,5),10000,20261022))
    out['mixed_graphs'].append(cycle_trials(3))
    out['mixed_graphs'].append(cycle_trials(4))
    out['mixed_graphs'].append(cycle_trials(5))
    out['mixed_graphs'].append(cycle_trials(5,(-2,-1,1,2),trials=10000))
    (HERE/'toy_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))
