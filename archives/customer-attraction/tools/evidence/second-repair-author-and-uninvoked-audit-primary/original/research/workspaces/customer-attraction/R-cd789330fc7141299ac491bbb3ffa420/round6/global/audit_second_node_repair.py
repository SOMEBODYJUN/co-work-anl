"""Expanded-unit implementation audit; no canonical verifier/oracle import."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
reports=[]
for m in (3,4):
    old=(frozenset(range(m)),frozenset(range(m,m+m*(m+1))))
    old_n=m+m*(m+1);caps=(2,m-2)+(1,)*(m-2);banks=[];cur=old_n
    for c in caps:banks.append(frozenset(range(cur,cur+c)));cur+=c
    topics=tuple(a|b for a in old for b in banks);k=len(topics)
    masks=tuple(sum(1<<a for a,T in enumerate(topics)if x in T)for x in range(cur))
    assert len(set(topics))==k
    @lru_cache(None)
    def bc(h):return h if len(h)==m else bc(h+(ba(h),))
    @lru_cache(None)
    def ba(h):
        free=[a for a,c in enumerate(caps)if h.count(a)<c];assert free
        return max((F(caps[a],bc(h+(a,)).count(a)),-a,a)for a in free)[2]
    def core(h):
        if all(a in(0,1)for a in h)and h.count(0)<=2 and h.count(1)<=m-2:
            return 0 if h.count(0)<2 else 1
        return ba(h)
