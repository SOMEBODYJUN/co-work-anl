"""Attack a single all-input conjecture, not prove it by finite tests.
Conjecture: OPT_m <= sum_{x:c_x>0}(2-1/(c_x+1)) for every pure SPE.
For a finite list of complete strategy seeds, optimize the customer cone exactly
as a discovery LP; any numerical witness must be separately rationally verified.
"""
import itertools,json,random,sys
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

OUT=Path(__file__).parent
rng=random.Random(231024)
def attack(p,m,trial):
    masks=range(1,1<<p)
    topics=tuple(str(a) for a in range(p))
    inst=Instance(topics,tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),rng.randrange(1,9)) for mask in masks),m)
    solver=ExactSPESolver(inst)
    target=min(solver.outcomes(),key=lambda c:sum(t.multiplicity*(2-1/(sum(c[a] for a in t.topics)+1)) for t in inst.customers if sum(c[a] for a in t.topics)))
    cert=solver.certificate(target)
    actions=cert.actions
    def leaf(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    def payoff(mask,h,a):
        return Fraction(int(mask>>a&1),sum(mask>>b&1 for b in h)) if mask>>a&1 else Fraction()
    rows=[]
    for h,action in actions.items():
        actual=leaf(h); actual_u=[payoff(mask,actual,action) for mask in masks]
        for a in range(p):
            if a!=action:
                alt=leaf(h+(a,)); rows.append([float(payoff(mask,alt,a)-u) for mask,u in zip(masks,actual_u)])
    c=np.array([float(2-Fraction(1,1+sum(mask>>a&1 for a in leaf(())))) if any(mask>>a&1 for a in leaf(())) else 0 for mask in masks])
    for support in itertools.combinations(range(p),min(m,p)):
        o=np.array([float(any(mask>>a&1 for a in support)) for mask in masks])
        res=linprog(-o,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=c[None,:],b_eq=[1],bounds=(0,None),method='highs')
        if res.success and -res.fun>1+1e-8:
            vals=[Fraction(float(x)).limit_denominator(100000) for x in res.x]
            den=1
            import math
            for x in vals:den=math.lcm(den,x.denominator)
            ints=[int(x*den) for x in vals]
            new=Instance(topics,tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),w) for mask,w in zip(masks,ints) if w),m)
            obj={'kind':'occupancy_bound_candidate','p':p,'m':m,'trial':trial,'numerical_violation':-res.fun,'comparison':support,'instance':new.to_dict(),'actions':[{'history':h,'action':a} for h,a in actions.items()],'terminal':leaf(())}
            f=OUT/'occupancy_candidate_failure.json';f.write_text(json.dumps(obj,indent=2));print('CANDIDATE',p,m,trial,-res.fun,flush=True);return True
    print('seed',p,m,trial,'max done',flush=True)
    return False
if __name__=='__main__':
    for trial in range(20):
        p,m=[(4,3),(5,3),(4,5),(5,4),(6,3)][trial%5]
        if attack(p,m,trial):break
