"""Exact promise slices; compare implementation with canonical outcome filtering."""
from fractions import Fraction as F
from functools import lru_cache
from customer_attraction import Instance, CustomerType, ExactSPESolver

class PromiseSlices:
    def __init__(self, instance):
        self.I=instance;self.S=ExactSPESolver(instance)
    @lru_cache(None)
    def outcomes(self,k,t):
        if sum(k)==self.I.players:
            u=self.I.topic_payoffs(k)
            return frozenset({k}) if all(not k[a] or u[a]>=t[a] for a in range(len(k))) else frozenset()
        M=self.S.threshold(k);answer=set()
        for a in range(len(k)):
            kk=list(k);kk[a]+=1;tt=list(t);tt[a]=max(tt[a],M)
            answer.update(self.outcomes(tuple(kk),tuple(tt)))
        return frozenset(answer)

def compositions(r,p):
    if p==1:
        yield(r,);return
    for n in range(r+1):
        for tail in compositions(r-n,p-1):yield(n,)+tail

def check(I):
    P=PromiseSlices(I);p=I.topic_count;checks=0
    for n in range(I.players+1):
        for k in compositions(n,p):
            Q=P.S.outcomes(k)
            # Empty commitments and several genuine coordinate slices.
            promises=[(F(0),)*p]
            for q in Q:
                u=I.topic_payoffs(q)
                promises.append(tuple(u[a] if k[a] else F(0) for a in range(p)))
                promises.append(tuple(u[a]+F(1,7) if k[a] else F(0) for a in range(p)))
            for t in promises:
                actual=P.outcomes(k,t)
                expected=frozenset(q for q in Q if all(not k[a] or I.topic_payoff(a,q)>=t[a] for a in range(p)))
                assert actual==expected
                checks+=1
    return checks

if __name__=='__main__':
    from pathlib import Path
    import json
    base=Path(__file__).parent
    J=json.loads((base/'blind_input.json').read_text())
    cases=[Instance(('empty',),(),3),
           Instance(('one',),(CustomerType(frozenset({0}),3),),3),
           Instance(('empty','one'),(CustomerType(frozenset({1}),2),),3),
           Instance(('dup0','dup1'),(CustomerType(frozenset({0,1}),4),),3),
           Instance.from_dict(J['instance'])]
    counts=[check(I) for I in cases]
    print(json.dumps({'status':'exact promise recurrence and finite implementation regression',
                      'cases':len(cases),'slice_queries':counts,'total':sum(counts)},indent=2))
