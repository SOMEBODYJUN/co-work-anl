"""Conservative dynamic SPE floors using only myopic-ceiling action pruning.

At a node, child terminal sets are a superset of SPE outcomes. The dynamic
max-min floor is valid; retain an action if its immediate (uncrowded-future)
ceiling reaches that floor, rather than requiring its final payoff to reach
it. That last distinction separates this relaxation from exact SPE BI.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from copy_protection_dp import CustomerType,Instance,ExactSPESolver,compositions

class MyopicCeilingFloor:
    def __init__(self,instance):
        self.ins=instance;self.k=instance.topic_count;self.m=instance.players
        self.level={};self.allowed={};self.terminals=lru_cache(None)(self._terminals)
        self.pay=lru_cache(None)(instance.topic_payoffs)
        self.cost=lru_cache(None)(self._cost)

    def add(self,b,a):return b[:a]+(b[a]+1,)+b[a+1:]

    def myopic(self,b,a):
        return sum((F(c.multiplicity,1+sum(b[t] for t in c.topics))
                    for c in self.ins.customers if a in c.topics),F())

    def _terminals(self,b):
        r=self.m-sum(b)
        if not r:return frozenset({b})
        children=[self.terminals(self.add(b,a)) for a in range(self.k)]
        floor=max(min(self.pay(q)[a] for q in children[a]) for a in range(self.k))
        allowed=tuple(a for a in range(self.k) if self.myopic(b,a)>=floor)
        assert allowed
        self.level[b]=floor;self.allowed[b]=allowed
        return frozenset(q for a in allowed for q in children[a])

    def floor(self,b):self.terminals(b);return self.level[b]

    def _cost(self,b):
        if sum(b)==self.m:return F()
        self.terminals(b)
        return self.level[b]+min(self.cost(self.add(b,a)) for a in self.allowed[b])

    def root(self):return self.cost((0,)*self.k)


def smoke():
    stats={'instances':0,'prefixes':0,'paths':0,'strict_outcome_relaxations':0}
    worst=None
    for k in range(1,4):
        sigs=[frozenset(t for t in range(k) if mask>>t&1) for mask in range(1,1<<k)]
        for bits in product([0,1],repeat=len(sigs)):
            cs=tuple(CustomerType(s) for s,v in zip(sigs,bits) if v)
            for m in range(1,5):
                ins=Instance(tuple(map(str,range(k))),cs,m)
                dp=MyopicCeilingFloor(ins); exact=ExactSPESolver(ins)
                for n in range(m):
                    for b in compositions(n,k):
                        assert exact.outcomes(b)<=dp.terminals(b)
                        assert dp.floor(b)<=exact.threshold(b)
                        if exact.outcomes(b)<dp.terminals(b):stats['strict_outcome_relaxations']+=1
                        stats['prefixes']+=1
                for path in exact.ordered_outcomes():
                    pay=ins.player_payoffs(path);b=(0,)*k
                    for i,a in enumerate(path):
                        assert pay[i]>=dp.floor(b)
                        assert a in dp.allowed[b]
                        b=dp.add(b,a)
                    assert sum(pay)>=dp.root()
                    stats['paths']+=1
                stats['instances']+=1
                if (o:=ins.optimal_welfare()):
                    ratio=dp.root()/o
                    if worst is None or ratio<worst[0]:worst=(ratio,k,m,ins.to_dict(),str(dp.root()),o)
    stats['worst_ratio']=str(worst[0]);stats['worst']=worst[1:]
    return stats

if __name__=='__main__':
    import json
    print(json.dumps(smoke(),indent=2))
