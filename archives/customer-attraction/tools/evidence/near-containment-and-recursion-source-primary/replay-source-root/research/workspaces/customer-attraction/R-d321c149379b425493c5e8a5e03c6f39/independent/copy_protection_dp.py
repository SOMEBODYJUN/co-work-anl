"""Exact arithmetic exploratory first-contained-follower lower floor.

This is a lower bound, not a replacement for set-valued SPE enumeration.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver


def compositions(n, k):
    if k == 0:
        if n == 0: yield ()
        return
    if k == 1:
        yield (n,); return
    for v in range(n+1):
        for tail in compositions(n-v,k-1): yield (v,)+tail

class CopyProtectionFloor:
    def __init__(self, instance):
        self.instance=instance
        self.k=instance.topic_count
        self.customers=instance.customers
        self.sets=tuple(frozenset(i for i,c in enumerate(self.customers) if a in c.topics)
                        for a in range(self.k))
        self.dominated=tuple(tuple(a for a in range(self.k) if self.sets[a] <= self.sets[t])
                             for t in range(self.k))
        self.complement=tuple(tuple(a for a in range(self.k) if a not in self.dominated[t])
                             for t in range(self.k))
        self.floor=lru_cache(None)(self._floor)
        self.state_cost=lru_cache(None)(self._state_cost)

    def add(self,b,topics):
        q=list(b)
        for a in topics:q[a]+=1
        return tuple(q)

    def external(self,b,t,q):
        # b are already fixed players, q future counts, and t is the inserted provider.
        return sum((F(c.multiplicity, 1+sum(b[a]+q[a] for a in c.topics))
                    for c in self.customers if t in c.topics),F())

    def subset_counts(self,n,allowed):
        for qsmall in compositions(n,len(allowed)):
            q=[0]*self.k
            for a,v in zip(allowed,qsmall):q[a]=v
            yield tuple(q)

    def _floor(self,b,r):
        assert r>=1
        candidates=[]
        for t in range(self.k):
            terms=[]
            # No later action contained in t.
            for q in self.subset_counts(r-1,self.complement[t]):
                terms.append(self.external(b,t,q))
            # First contained follower occurs after ell-1 noncontained actions.
            for ell in range(1,r):
                for q in self.subset_counts(ell-1,self.complement[t]):
                    bp=tuple(b[a]+q[a]+int(a==t) for a in range(self.k))
                    terms.append(self.floor(bp,r-ell))
            assert terms
            candidates.append(min(terms))
        return max(candidates)

    def _state_cost(self,b,r):
        # Any path pays this floor at every successive prefix; arbitrary actions relax SPE.
        if not r:return F()
        return self.floor(b,r)+min(self.state_cost(self.add(b,[a]),r-1) for a in range(self.k))

    def root(self):return self.state_cost((0,)*self.k,self.instance.players)


def smoke():
    stats={'instances':0,'prefixes':0,'paths':0}
    for k in range(1,4):
        sigs=[frozenset(t for t in range(k) if mask>>t&1) for mask in range(1,1<<k)]
        for bits in product([0,1],repeat=len(sigs)):
            cs=tuple(CustomerType(s) for s,v in zip(sigs,bits) if v)
            for m in range(1,5):
                ins=Instance(tuple(map(str,range(k))),cs,m)
                dp=CopyProtectionFloor(ins); solver=ExactSPESolver(ins)
                for n in range(m):
                    for b in compositions(n,k):
                        assert dp.floor(b,m-n)<=solver.threshold(b)
                        stats['prefixes']+=1
                for path in solver.ordered_outcomes():
                    b=(0,)*k; pay=ins.player_payoffs(path)
                    for i,a in enumerate(path):
                        assert pay[i]>=dp.floor(b,m-i)
                        b=dp.add(b,[a])
                    assert sum(pay)>=dp.root()
                    stats['paths']+=1
                stats['instances']+=1
    return stats

if __name__=='__main__':
    import json
    print(json.dumps(smoke(),sort_keys=True))
