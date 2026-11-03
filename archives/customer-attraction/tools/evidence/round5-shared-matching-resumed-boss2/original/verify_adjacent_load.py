"""Exact finite checks of adjacent-prefix load reconstruction and positivity."""
from itertools import product
from collections import defaultdict
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def comps(n,k):
    if k==1:yield(n,);return
    for i in range(n+1):
        for a in comps(n-i,k-1):yield(i,)+a

def recover(L,M):
    x=[];y=[];s=0
    for a,b in zip(L,M):s+=a-b;x.append(s);y.append(a-s)
    return tuple(x),tuple(y)

reconstruction=0;uniqueness=0;compatibility=0
for q in range(5):
    pairs=defaultdict(set)
    for P in product(range(3),repeat=q):
        for a in product((0,1),repeat=q):
            Q=tuple(p+b for p,b in zip(P,a))
            L=tuple(P.count(c) for c in range(4));M=tuple(Q.count(c) for c in range(4))
            X=tuple(sum(p==c and z==c+1 for p,z in zip(P,Q)) for c in range(4))
            Y=tuple(sum(p==c and z==c for p,z in zip(P,Q)) for c in range(4))
            assert recover(L,M)==(X,Y);pairs[L,M].add((X,Y));reconstruction+=1
    for v in pairs.values():assert len(v)==1;uniqueness+=1
    for L,M in product(list(comps(q,4)),repeat=2):
        X,Y=recover(L,M);valid=min(X+Y)>=0
        FL=0;FM=0;interlace=True
        for l,m in zip(L,M):
            old=FL;FL+=l;FM+=m;interlace &= old<=FM<=FL
        assert valid==interlace
        if valid:
            assert all(l==x+y for l,x,y in zip(L,X,Y))
            assert all(m==y+(X[c-1] if c else 0) for c,(m,y) in enumerate(zip(M,Y)))
        compatibility+=1
out={'scope':'Exact finite recurrence checks; arbitrary-q proof is analytic','individual_list_reconstructions':reconstruction,'unique_margin_pairs_checked':uniqueness,'margin_compatibility_pairs':compatibility,'passed':True}
(HERE/'adjacent_load_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
