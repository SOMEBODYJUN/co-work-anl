"""Construct the EF/EFX allocation in FC-LEMMA-R2-2C-v1.
Input columns are binary tuples, allowing duplicates. No loops.
Naive maximum matching; all arithmetic integral. Output checked independently.
"""
from collections import deque
from itertools import product
from random import Random
from pathlib import Path
import json

def matching(words,w,n):
    m=len(words);adj=[[e for e,b in enumerate(words) if b[i]!=w[i]] for i in range(n)]
    right=[-1]*m;left=[-1]*n
    def aug(i,seen):
        for e in adj[i]:
            if seen[e]:continue
            seen[e]=1
            if right[e]<0 or aug(right[e],seen):
                right[e]=i;left[i]=e;return True
        return False
    for i in range(n):aug(i,[0]*m)
    return left,right,adj

def missing_word(types,n):
    # First missing lexicographic word, using distinct prefix counts.
    pref=()
    for i in range(n):
        p0=pref+(0,);count=sum(b[:i+1]==p0 for b in types)
        pref=p0 if count<(1<<(n-i-1)) else pref+(1,)
    assert pref not in types
    return pref

def construct(words,n):
    m=len(words);X=[[] for _ in range(n)];rounds=0
    if n==1:return [list(range(m))],rounds
    if m<n:
        for e in range(m):X[e].append(e)
        return X,rounds
    types={b for b in words};represent={}
    for e,b in enumerate(words):represent.setdefault(b,e)
    if len(types)==1<<n:
        used=set();a=0
        for b in sorted(types):
            if b[0]:continue
            comp=tuple(1-x for x in b)
            X[a]=[represent[b],represent[comp]];used.update(X[a]);a+=1
            if a==n:break
        for e in range(m):
            if e not in used:X[0].append(e)
        return X,rounds
    w=missing_word(types,n)
    while True:
        left,right,adj=matching(words,w,n)
        if all(e>=0 for e in left):break
        S={i for i in range(n) if left[i]<0};T=set();q=deque(S)
        while q:
            i=q.popleft()
            for e in adj[i]:
                if e in T:continue
                T.add(e)
                if right[e]>=0 and right[e] not in S:S.add(right[e]);q.append(right[e])
        assert len(T)<len(S)
        opts=[]
        for i in S:
            v=w[:i]+(1-w[i],)+w[i+1:]
            if v not in types:opts.append(v)
        assert opts
        old_size=sum(e>=0 for e in left);w=opts[0];rounds+=1
        # Recompute the maximum matching; proof guarantees strict increase.
        new_left,_,_=matching(words,w,n)
        assert sum(e>=0 for e in new_left)>old_size
    for i,e in enumerate(left):X[i].append(e)
    for e,j in enumerate(right):
        if j<0:
            i=next(i for i in range(n) if words[e][i]!=w[i]);X[i].append(e)
    return X,rounds

def check(words,X,n):
    def c(i,b):return len({words[e][i] for e in b})
    m=len(words);flat=[e for b in X for e in b]
    assert sorted(flat)==list(range(m))
    ef=all(c(i,X[i])<=c(i,X[j]) for i in range(n) for j in range(n))
    efx=all(c(i,[f for f in X[i] if f!=e])<=c(i,X[j]) for i in range(n) for j in range(n) for e in X[i])
    assert efx and (m<n or ef)
    return ef,efx

if __name__=='__main__':
    rng=Random(20261020);trials=0;max_rounds=0
    for n in range(2,9):
        for m in (n-1,n,2*n,4*n,100):
            for _ in range(100):
                words=[tuple(rng.randrange(2) for _ in range(n)) for e in range(m)]
                X,r=construct(words,n);check(words,X,n);trials+=1;max_rounds=max(max_rounds,r)
        if (1<<n)<=256:
            words=list(product((0,1),repeat=n));X,r=construct(words,n);check(words,X,n);trials+=1
    out={'lemma':'FC-LEMMA-R2-2C-v1','seed':20261020,'random_n':list(range(2,9)),'random_m':'n-1,n,2n,4n,100','random_trials_per_pair':100,'total_cases_including_full_cube':trials,'max_matching_flip_rounds_observed':max_rounds,'assertions':'complete; EFX always; EF if m>=n; matching strictly increases'}
    p=Path(__file__).resolve().parent/'construct_rank2_results.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
