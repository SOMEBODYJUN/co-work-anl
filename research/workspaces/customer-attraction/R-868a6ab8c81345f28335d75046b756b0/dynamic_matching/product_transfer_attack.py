"""Target Cartesian-product convexification of SM-opt-exists, using Fraction.

This is not an unstructured extra SM sample run. For a three-role component,
the second-role IC can transfer surplus between Cartesian components. Compute
the exact relaxed first-role value barL(A), and seek a component whose *every*
optimal permutation has barL(T1)+L2(T2)+L3(T3) < OPT-W. Such a component would
yield a finite Cartesian-product counterexample after controlling rounding.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver


def transfer_value(inst, solver, a):
    p=inst.topic_count
    h=[0]*p; h[a]+=1
    theta=solver.threshold(h)
    leaves=[]
    for b in range(p):
        k=h[:]; k[b]+=1
        best=max(inst.topic_payoff(c,tuple(k[j]+(j==c) for j in range(p))) for c in range(p))
        for c in range(p):
            t=tuple(k[j]+(j==c) for j in range(p))
            if inst.topic_payoff(c,t)==best:
                leaves.append((inst.topic_payoff(a,t),inst.topic_payoff(b,t)-theta,(b,c)))
    feasible=[(d,[(F(1),bc)]) for d,v,bc in leaves if v>=0]
    for d0,v0,bc0 in leaves:
        if v0>=0: continue
        for d1,v1,bc1 in leaves:
            if v1<=0: continue
            q=v1/(v1-v0)
            feasible.append((q*d0+(1-q)*d1,[(q,bc0),(1-q,bc1)]))
    return min(feasible,key=lambda x:x[0]), theta, leaves


def inspect(inst):
    solver=ExactSPESolver(inst)
    p,m=inst.topic_count,inst.players
    O=inst.optimal_welfare()
    ts=[t for t in product(range(p),repeat=m) if inst.welfare(inst.counts(t))==O]
    bars=[transfer_value(inst,solver,a) for a in range(p)]
    best=None
    for z in solver.ordered_outcomes():
        W=inst.welfare(inst.counts(z))
        if O<=W: continue
        ls=[]
        for i in range(m):
            h=inst.counts(z[:i])
            ls.append([min(inst.topic_payoff(a,t) for t in solver.outcomes(tuple(h[j]+(j==a) for j in range(p)))) for a in range(p)])
        value,t=max((bars[t[0]][0][0]+ls[1][t[1]]+ls[2][t[2]],t) for t in ts)
        gap=F(O-W)-value
        if best is None or gap>best[0]: best=(gap,z,t,W,O,value,ls,bars)
    return best


def main():
    best=None; n=0
    # A deterministic finite attack on the stated product-convexified claim.
    for weights in product(range(3),repeat=7):
        if not any(weights): continue
        customers=tuple(CustomerType(frozenset(j for j in range(3) if mask>>j&1),weights[mask-1]) for mask in range(1,8) if weights[mask-1])
        inst=Instance(('A','B','C'),customers,3)
        out=inspect(inst); n+=1
        if out is not None and (best is None or out[0]>best[0]):
            best=(out[0],weights,out)
            print(json.dumps({'instances':n,'best_gap':str(out[0]),'weights':weights,'path':out[1],'best_opt':out[2],'W':out[3],'OPT':out[4],'max_convex_SM':str(out[5])}),flush=True)
        if out is not None and out[0]>0:
            print('FOUND',repr((weights,out)),flush=True); return
    print('DONE',n,repr(best),flush=True)

if __name__=='__main__': main()
