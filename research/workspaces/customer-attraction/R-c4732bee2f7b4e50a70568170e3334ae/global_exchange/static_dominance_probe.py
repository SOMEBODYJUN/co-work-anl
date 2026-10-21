"""Finite probe only: compare worst SPE with worst simultaneous pure NE."""
import json, random, sys
from itertools import combinations_with_replacement
from customer_attraction import Instance, CustomerType, ExactSPESolver

def pne_counts(ins):
    for choices in combinations_with_replacement(range(ins.topic_count),ins.players):
        q=ins.counts(choices,terminal=True); u=ins.topic_payoffs(q)
        good=True
        for a in range(ins.topic_count):
            if not q[a]:continue
            for b in range(ins.topic_count):
                if a==b:continue
                z=list(q);z[a]-=1;z[b]+=1
                if ins.topic_payoff(b,z)>u[a]:good=False;break
            if not good:break
        if good:yield q

def main():
    rng=random.Random(903711)
    for t in range(10000):
        L=5;m=2+t%4
        ins=Instance(tuple(map(str,range(L))),tuple(CustomerType(frozenset(i for i in range(L) if mask>>i&1),2**rng.randrange(5)) for mask in range(1,1<<L) if mask.bit_count()<=2 and rng.random()<0.65),m)
        ss=ExactSPESolver(ins); w=ss.minimum_welfare();pnes=list(pne_counts(ins));pn=min(map(ins.welfare,pnes))
        if w<pn:
            print(json.dumps({'iteration':t,'instance':ins.to_dict(),'worst_spe':w,'worst_spe_counts':list(min(ss.worst_outcomes())),'worst_pne':pn,'pne_counts':[list(q) for q in pnes]},indent=2));return
    print('No counterexample in 10000 finite games')
if __name__=='__main__':main()
