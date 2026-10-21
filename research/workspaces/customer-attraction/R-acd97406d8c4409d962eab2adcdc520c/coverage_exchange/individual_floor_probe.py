"""Finite exploratory probe only: minimize occupied SPE-topic payoff / OPT."""
import json, random, sys, time
from customer_attraction import Instance, CustomerType, ExactSPESolver
from fractions import Fraction
rng=random.Random(20261021)
best=Fraction(1)
for n,k,trials in [(3,5,120),(4,6,60),(5,7,12)]:
    for z in range(trials):
        cs=[]
        for mask in range(1,1<<k):
            if rng.random()<.20:
                cs.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),rng.randint(1,12)))
        inst=Instance(tuple(map(str,range(k))),tuple(cs),n)
        sol=ExactSPESolver(inst); opt=inst.optimal_welfare()
        if not opt:continue
        vals=[]
        for c in sol.outcomes():
            p=inst.topic_payoffs(c)
            v=min(p[i] for i in range(k) if c[i]); vals.append((v,c))
        v,c=min(vals)
        ratio=v/opt
        if ratio<best:
            best=ratio
            print(json.dumps({'n':n,'k':k,'trial':z,'ratio':str(ratio),'2nratio':str(2*n*ratio),'counts':c,'instance':inst.to_dict()}),flush=True)
        if 2*n*v<opt:
            print('FATAL_INDIVIDUAL',flush=True);sys.exit()
print('DONE',best)
