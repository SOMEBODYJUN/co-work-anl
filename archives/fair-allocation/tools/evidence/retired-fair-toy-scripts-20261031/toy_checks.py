"""Exact integer toy searches. These finite checks are not proofs of existence."""
import itertools as it
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent

def key_allocations(sizes, n=4):
    """Columns are objects; allocation indicators have dimensions [alloc,agent,obj]."""
    m=sum(sizes); rank=m//n
    rows=[]
    for ass in it.product(*(list(it.permutations(range(n), s)) for s in sizes)):
        a=sum((tuple(x) for x in ass), ())
        if all(a.count(i)==rank for i in range(n)):
            rows.append(a)
    owners=np.array(rows,dtype=np.int16)
    return owners, (owners[:,None,:]==np.arange(n)[None,:,None]).astype(np.int64)

def ordered_ef1_witness(V, owners, X):
    # U[a,i,j] is observer i's value for recipient j's bundle.
    U=np.einsum('ig,ajg->aij',V,X)
    own=U[:,np.arange(4),np.arange(4)]
    mask=np.ones(len(X),dtype=bool)
    for i in range(4):
        for j in range(4):
            maxgood=(X[:,j,:]*V[i]).max(axis=1)
            mask &= own[:,i]>=U[:,i,j]-maxgood
            if i<j: mask &= own[:,i]>=U[:,i,j]
    ix=np.flatnonzero(mask)
    return len(ix), (owners[int(ix[0])].tolist() if len(ix) else None)

def key_search():
    rng=np.random.default_rng(20261020)
    out=[]
    for sizes,trials in [([3,3,2],5000),([3,3,3,3],500)]:
        owners,X=key_allocations(sizes)
        minw=len(X); worst=None
        distributions={'uniform_0_10':0,'binary':0,'powers_of_two':0}
        fail=None
        for t in range(trials):
            mode=t%3; m=sum(sizes)
            if mode==0: V=rng.integers(0,11,(4,m)); name='uniform_0_10'
            elif mode==1: V=rng.integers(0,2,(4,m)); name='binary'
            else: V=2**rng.integers(0,15,(4,m)); name='powers_of_two'
            distributions[name]+=1
            k,w=ordered_ef1_witness(V,owners,X)
            if k<minw: minw=k; worst={'valuations':V.tolist(),'witness':w,'count':k}
            if not k: fail=V.tolist(); break
        # Reproduce Lemma 12 obstruction: top sets for agents 3 and 4.
        separation_count=None
        if sizes==[3,3,2]:
            separation_count=sum(len(set(a[[2,4,5]]))==3 and len(set(a[[0,1,4,5]]))==4 for a in owners)
        out.append({'sizes':sizes,'rank':sum(sizes)//4,'feasible_labelled_allocations':len(X),
                    'trials':sum(distributions.values()),'seed':20261020,'distribution_counts':distributions,
                    'counterexample':fail,'minimum_witness_count':minw,'worst_observed_instance':worst,
                    'lemma12_top_separation_allocations':separation_count})
    return out

def copies_allocations(c,n):
    opts=[list(it.combinations(range(n),q)) for q in c]
    rows=[]
    for choices in it.product(*opts):
        X=np.zeros((n,len(c)),dtype=np.int64)
        for g,rec in enumerate(choices): X[list(rec),g]=1
        rows.append(X)
    return np.array(rows)

def sd_witnesses(rankings,X):
    n=len(rankings); mask=np.ones(len(X),dtype=bool)
    for i,order in enumerate(rankings):
        counts=np.cumsum(X[:,:,order],axis=2)
        for j in range(n): mask &= np.all(counts[:,i,:]>=counts[:,j,:]-1,axis=1)
    ix=np.flatnonzero(mask)
    return len(ix), (X[int(ix[0])].tolist() if len(ix) else None)

def copies_search():
    rng=np.random.default_rng(20261021); result=[]
    for n,c,trials in [(3,[1,1,2,2,2,1],5000),(4,[1,2,3,1,2,3],2000)]:
        X=copies_allocations(c,n); minw=len(X); worst=None; fail=None
        for t in range(trials):
            rankings=[rng.permutation(len(c)).tolist() for _ in range(n)]
            k,w=sd_witnesses(rankings,X)
            if k<minw: minw=k;worst={'rankings':rankings,'witness':w,'count':k}
            if k==0: fail=rankings;break
        result.append({'n':n,'copies':c,'allocation_count':len(X),'trials':t+1,'seed':20261021,
                       'counterexample':fail,'minimum_witness_count':minw,'worst_observed_instance':worst})
    return result

if __name__=='__main__':
    answer={'boundary':'all arithmetic integral; sampled valuation/ranking profiles only',
            'keys':key_search(),'copies':copies_search()}
    (ROOT/'toy_results.json').write_text(json.dumps(answer,indent=2))
    print(json.dumps(answer,indent=2))
