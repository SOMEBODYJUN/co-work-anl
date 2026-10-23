"""Target the merge-tie obstruction to anonymous SPE realization.

LP is discovery only. Every rational point and policy claim is subsequently
checked by Fraction arithmetic and exhaustive anonymous-policy enumeration.
"""
import argparse
import json
import math
import random
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from anonymous_extremal_probe import (
    Instance, CustomerType, ExactSPESolver, anonymous_outcomes, counts_layer, incr)


def row(p, q, a):
    return tuple(F(int(bool(mask & (1 << a))),
                   max(1, sum(q[b] for b in range(p) if mask & (1 << b))))
                 for mask in range(1, 1 << p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=9872331)
    ap.add_argument('--p', type=int, default=4)
    ap.add_argument('--m', type=int, default=3)
    ap.add_argument('--cap', type=int, default=200000)
    ap.add_argument('--output')
    args = ap.parse_args()
    rng = random.Random(args.seed)
    p,m=args.p,args.m
    n=(1<<p)-1
    states=counts_layer(p,m-1)
    summary=dict(candidate='all full-history outcomes attained by count-based pure SPE',
        p=p,m=m,seed=args.seed,requested=args.trials,completed=0,capped=0,
        invalid_rationalizations=0,strict_outcome_set_gaps=0,
        strict_welfare_gaps=0,first_outcome_gap=None,first_welfare_gap=None,
        anonymous_policies=0)
    for trial in range(args.trials):
        # A merge state contains at least two different labels.  Choose any
        # feasible tie pair; unlike iid integers, every sample lies on a tie face.
        q=rng.choice([q for q in states if sum(x>0 for x in q)>=2
                      and sum(x==0 for x in q)>=2])
        c,d=rng.sample([a for a in range(p) if not q[a]],2)
        rows=[row(p,incr(q,a),a) for a in range(p)]
        eq=[rows[c][i]-rows[d][i] for i in range(n)]
        ub=[[rows[a][i]-rows[c][i] for i in range(n)]
            for a in range(p) if a not in (c,d)]
        w=[F(0)]*n
        for repeat in range(4):
            result=linprog([rng.gauss(0,1) for _ in range(n)],
                A_ub=np.array(ub,dtype=float),b_ub=np.zeros(len(ub)),
                A_eq=np.array([[1]*n,eq],dtype=float),b_eq=[1,0],
                bounds=(0,None),method='highs')
            if not result.success:
                break
            weight=rng.randrange(1,5)
            w=[x+weight*F(float(v)).limit_denominator(100000)
               for x,v in zip(w,result.x)]
        total=sum(w)
        if not total:
            continue
        w=[x/total for x in w]
        if sum(w)!=1 or sum(x*y for x,y in zip(eq,w)) or any(
                sum(x*y for x,y in zip(r,w))>0 for r in ub):
            summary['invalid_rationalizations']+=1
            continue
        # An interior all-type baseline is retained exactly whenever it lies
        # on the same best-response tie face.
        base=[F(1,n)]*n
        if not sum(x*y for x,y in zip(eq,base)) and all(
                sum(x*y for x,y in zip(r,base))<=0 for r in ub):
            scale=rng.randrange(1,12)
            w=[x+scale*y for x,y in zip(base,w)]
        scale=math.lcm(*(x.denominator for x in w))
        iw=[int(x*scale) for x in w]
        instance=Instance(tuple(map(str,range(p))),tuple(
            CustomerType(frozenset(a for a in range(p) if mask&(1<<a)),x)
            for mask,x in enumerate(iw,1) if x),m)
        solver=ExactSPESolver(instance)
        full=solver.outcomes()
        try:
            anon,witnesses,npol=anonymous_outcomes(instance,args.cap)
        except OverflowError:
            summary['capped']+=1
            continue
        summary['completed']+=1
        summary['anonymous_policies']+=npol
        assert anon<=full
        if full!=anon:
            summary['strict_outcome_set_gaps']+=1
            if summary['first_outcome_gap'] is None:
                missing=min(full-anon)
                summary['first_outcome_gap']=dict(trial=trial,
                    instance=instance.to_dict(),weights=iw,tie_state=q,
                    tie_actions=[c,d],full_outcomes=sorted(full),
                    anonymous_outcomes=sorted(anon),
                    missing=missing,full_certificate=solver.certificate(missing).to_dict(),
                    anonymous_policies=npol)
        wf=min(map(instance.welfare,full));wa=min(map(instance.welfare,anon))
        if wf<wa:
            summary['strict_welfare_gaps']+=1
            bad=min(t for t in full if instance.welfare(t)==wf)
            summary['first_welfare_gap']=dict(trial=trial,
                instance=instance.to_dict(),weights=iw,tie_state=q,
                tie_actions=[c,d],full_welfare=wf,anonymous_welfare=wa,
                full_outcomes=sorted(full),anonymous_outcomes=sorted(anon),
                full_certificate=solver.certificate(bad).to_dict(),
                anonymous_policy_count=npol,
                anonymous_witnesses=[dict(terminal=t,actions=[
                    dict(counts=k,action=a) for k,a in sorted(pol.items())])
                    for t,pol in sorted(witnesses.items())])
            break
        if trial and trial%100==0:
            print(json.dumps({k:v for k,v in summary.items()
                if not k.startswith('first_')}),flush=True)
    payload=json.dumps(summary,indent=2)
    if args.output:
        Path(args.output).write_text(payload+'\n')
    print(payload)


if __name__=='__main__':
    main()
