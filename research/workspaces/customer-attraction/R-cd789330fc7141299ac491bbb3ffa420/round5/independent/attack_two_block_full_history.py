"""Target the same general two-block safety candidate with full history ties.

This changes discovery only. Exact policy-cone and static-query inequalities
are checked before a separation can be reported.
"""
from fractions import Fraction
from functools import lru_cache
import argparse
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[6]))
from customer_attraction import CustomerType, ExactSPESolver, Instance
from attack_two_block import compositions


def run(players, topics, tries, seed, diagnostic=False):
    rng = random.Random(seed)
    masks = tuple(range(1, 1 << topics))
    members = tuple(tuple((mask >> a) & 1 for a in range(topics)) for mask in masks)
    coefficient = {}
    for q in compositions(players, topics):
        for a in range(topics):
            if q[a]:
                coefficient[q,a] = tuple(Fraction(t[a],sum(x*y for x,y in zip(t,q)))
                                         if t[a] else Fraction(0) for t in members)
    static = tuple(compositions(players-1,topics))
    best = None
    for trial in range(tries):
        weights = tuple(rng.randrange(1,4) if rng.random() < .3 else 0 for _ in masks)
        if not any(weights):
            continue
        instance = Instance(tuple(map(str,range(topics))),
                            tuple(CustomerType(frozenset(a for a in range(topics) if t[a]),w)
                                  for t,w in zip(members,weights) if w),players)
        solver = ExactSPESolver(instance)
        path = min(solver.ordered_outcomes(),
                   key=lambda h: sum(instance.player_payoffs(h)[:2]))
        cert = solver.certificate(on_path=path,
                                  action_selector=lambda h,c: rng.choice(c),
                                  continuation_selector=lambda h,c: rng.choice(c))
        exact_rows = []
        ic_labels = []
        @lru_cache(None)
        def follow(h):
            if len(h)==players:
                return instance.counts(h,terminal=True)
            return follow(h+(cert.actions[h],))
        for h,prescribed in cert.actions.items():
            z = follow(h)
            for a in range(topics):
                ic_labels.append((h,prescribed,a))
                exact_rows.append(tuple(x-y for x,y in
                                        zip(coefficient[z,prescribed],coefficient[follow(h+(a,)),a])))
        z = follow(())
        objective = tuple(x+y for x,y in zip(coefficient[z,path[0]],coefficient[z,path[1]]))
        raw = [1]*topics if trial%2==0 else [rng.randrange(0,13) for _ in range(topics)]
        if not sum(raw):
            raw[0]=1
        query = tuple(Fraction(a,sum(raw)) for a in raw)
        security_rows = tuple(tuple(sum(p*x for p,x in zip(query,t)) /
                                   (1+sum(x*y for x,y in zip(t,q))) for t in members)
                              for q in static)
        matrix = -np.array(exact_rows+list(security_rows),dtype=float)
        rhs = np.r_[np.zeros(len(exact_rows)),-np.ones(len(security_rows))]
        lp = linprog(np.array(objective,dtype=float),A_ub=matrix,b_ub=rhs,bounds=(0,None),method='highs')
        if not lp.success:
            continue
        if diagnostic:
            dual=lp.ineqlin.marginals
            return {'status':'float dual diagnostic only','path':list(path),
                    'query':list(map(str,query)),'objective':lp.fun,
                    'ic_support':[{'history':list(h),'prescribed':a,'deviation':d,
                                   'multiplier':float(-dual[j])}
                                  for j,(h,a,d) in enumerate(ic_labels) if dual[j]<-1e-7],
                    'static_support':[{'background':list(q),'multiplier':float(-dual[len(exact_rows)+j])}
                                      for j,q in enumerate(static) if dual[len(exact_rows)+j]<-1e-7],
                    'scope':'Diagnostic for reconstructing a general mechanism; not an exact certificate.'}
        best = lp.fun if best is None else min(best,lp.fun)
        if lp.fun < 2-1e-7:
            ws = tuple(Fraction(float(w)).limit_denominator(10**8) for w in lp.x)
            if any(sum(a*w for a,w in zip(row,ws))<0 for row in exact_rows):
                continue
            sec = min(sum(a*w for a,w in zip(row,ws)) for row in security_rows)
            pair = sum(a*w for a,w in zip(objective,ws))
            if pair < 2*sec:
                return {'status':'exact separation','players':players,'topics':topics,
                        'seed':seed,'trial':trial,'path':path,
                        'weights':{str(mask):str(w) for mask,w in zip(masks,ws) if w},
                        'query':list(map(str,query)),'pair_payoff':str(pair),
                        'security_lower_bound':str(sec),'strategy':cert.to_dict(),
                        'scope':'Only the two-block safety candidate, not Q-CAG-HALF.'}
        if trial%10==0:
            print(json.dumps({'trial':trial,'best_float':best}),flush=True)
    return {'status':'no exact separation found','players':players,'topics':topics,
            'tries':tries,'best_float':best,
            'scope':'Finite attack only; no positive theorem.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--players',type=int,default=4)
    parser.add_argument('--topics',type=int,default=6)
    parser.add_argument('--tries',type=int,default=50)
    parser.add_argument('--seed',type=int,default=441023)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--diagnostic',action='store_true')
    args=parser.parse_args()
    result=run(args.players,args.topics,args.tries,args.seed,args.diagnostic)
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
