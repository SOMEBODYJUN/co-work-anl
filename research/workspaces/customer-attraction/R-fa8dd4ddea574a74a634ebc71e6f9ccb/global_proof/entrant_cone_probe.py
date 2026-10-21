"""Probe alpha=1 entrant m M <= W+G_C on exact full strategy cones; no universal conclusion.

The seed selects legal integer customer instances, exact set-valued BI chooses
a complete SPE, and floating LP only discovers new weights in that fixed cone.
Any positive candidate is rationalized and independently rechecked exactly.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import math
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
import numpy as np
from scipy.optimize import linprog
from customer_attraction import CustomerType, Instance, ExactSPESolver, verify_certificate


def cone(cert, m, p):
    masks = tuple(range(1, 1 << p))
    def terminal(h):
        while len(h) < m:
            h += (cert.actions[h],)
        return h
    def coefficient(h, a):
        counts = [h.count(j) for j in range(p)]
        return tuple(F(int(bool(s & (1 << a))), sum(counts[j] for j in range(p) if s & (1 << j)))
                     if s & (1 << a) else F(0) for s in masks)
    rows = []
    for h, a in cert.actions.items():
        good = coefficient(terminal(h), a)
        for b in range(p):
            if b != a:
                bad = coefficient(terminal(h + (b,)), b)
                rows.append(tuple(x-y for x,y in zip(good,bad)))
    actual = terminal(())
    loads = tuple(sum(actual.count(j) for j in range(p) if s & (1 << j)) for s in masks)
    goals = []
    for a in range(p):
        goals.append(tuple(m*F(int(bool(s & (1 << a))), 1+c)
                           -int(c>0)-(F(1,1+c) if c else 0)
                           for s,c in zip(masks,loads)))
    return masks, rows, goals, actual


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--players',type=int,default=3)
    ap.add_argument('--topics',type=int,default=5)
    ap.add_argument('--rounds',type=int,default=30)
    ap.add_argument('--seed',type=int,default=9021)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    if a.players < 1 or a.topics < 1 or a.rounds < 0:
        ap.error('players/topics must be positive and rounds nonnegative')
    if a.output.exists():
        ap.error('refusing to overwrite an existing result')
    rng=random.Random(a.seed)
    best=0.0
    checks=0
    for step in range(a.rounds):
        size=rng.randint(min(2,(1<<a.topics)-1),min(12,(1<<a.topics)-1))
        weights={s:rng.randint(1,12) for s in rng.sample(range(1,1<<a.topics),size)}
        inst=Instance(tuple(map(str,range(a.topics))),tuple(CustomerType(frozenset(j for j in range(a.topics) if s>>j&1),w) for s,w in weights.items()),a.players)
        solver=ExactSPESolver(inst)
        targets=sorted(solver.outcomes())
        target=rng.choice(targets)
        cert=solver.certificate(target,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
        masks,rows,goals,actual=cone(cert,a.players,a.topics)
        mat=-np.array(rows,dtype=float).reshape((-1,len(masks)))
        for query,g in enumerate(goals):
            res=linprog(-np.array(g,dtype=float),A_ub=mat,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
            checks+=1
            if not res.success:
                raise RuntimeError(res.message)
            value=-res.fun
            if value>best+1e-8:
                best=value
                print(json.dumps({'step':step,'query':query,'gap':value}),flush=True)
            if value>1e-7:
                fr=[F(float(x)).limit_denominator(10**7) for x in res.x]
                den=math.lcm(*(x.denominator for x in fr))
                ints=[int(x*den) for x in fr]
                common=math.gcd(*ints)
                ints=[w//common for w in ints]
                exact_rows=[sum(x*w for x,w in zip(row,ints)) for row in rows]
                exact_goal=sum(x*w for x,w in zip(g,ints))
                if min(exact_rows,default=F(0))<0 or exact_goal<=0:
                    print('rationalization rejected',flush=True)
                    continue
                candidate=Instance(inst.topics,tuple(CustomerType(frozenset(j for j in range(a.topics) if s>>j&1),w) for s,w in zip(masks,ints) if w),a.players)
                report=verify_certificate(candidate,cert)
                report.assert_valid()
                record={'status':'exact_auxiliary_counterexample','parameters':vars(a)|{'output':str(a.output)},'step':step,'query':query,'gap':str(exact_goal),'actual':actual,'instance':candidate.to_dict(),'certificate':cert.to_dict(),'minimum_incentive_slack':str(min(exact_rows,default=F(0)))}
                a.output.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
                print(json.dumps({'found':str(a.output),'gap':str(exact_goal)}),flush=True)
                return
    a.output.write_text(json.dumps({'status':'finite_probe_only','parameters':vars(a)|{'output':str(a.output)},'LP_checks':checks,'maximum_positive_normalized_gap':best},indent=2)+'\n')
    print(json.dumps({'LP_checks':checks,'best':best}),flush=True)


if __name__=='__main__':
    main()
