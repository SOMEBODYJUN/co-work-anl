"""Exact attacks on the stated TB-ANY bridge, never a Q-CAG-HALF proof.

A count-state memo stores all local SPE outcomes; the minimizing path is
unrestricted and need not itself be an SPE path. Fractions are exact.
"""
from functools import lru_cache
from fractions import Fraction
import argparse, json, random, time
from customer_attraction import Instance, CustomerType, ExactSPESolver


def attack(inst):
    solver = ExactSPESolver(inst)
    p, m = inst.topic_count, inst.players
    @lru_cache(None)
    def J(c):
        if sum(c) == m:
            return Fraction(inst.welfare(c)), ()
        children = []
        for a in range(p):
            d = tuple(c[j]+(j==a) for j in range(p))
            v, tail = J(d)
            children.append((v, (a,)+tail))
        v, path = min(children)
        return solver.threshold(c)+v, path
    value, path = J((0,)*p)
    opt = inst.optimal_welfare()
    if value < opt:
        rows=[]
        for i,a in enumerate(path):
            c=inst.counts(path[:i])
            L=[]
            for b in range(p):
                d=tuple(c[j]+(j==b) for j in range(p))
                L.append(min(inst.topic_payoff(b,z) for z in solver.outcomes(d)))
            rows.append({'prefix':list(path[:i]),'action':a,'L':list(map(str,L)),'Theta':str(max(L))})
        return {'instance':inst.to_dict(),'path':path,'W':inst.welfare(inst.counts(path)),
                'OPT':opt,'J':str(value),'gap':str(value-opt),'rows':rows,
                'path_is_SPE':path in set(solver.ordered_outcomes())}
    return None

if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--trials',type=int,default=400); ap.add_argument('--seed',type=int,default=2026102401)
    args=ap.parse_args(); rng=random.Random(args.seed); start=time.time()
    for it in range(args.trials):
        p=rng.choice((3,4,5)); m=rng.choice((3,4,5,6))
        types=[]
        for mask in range(1,1<<p):
            w=rng.choice((0,0,0,1,2,3,5,10,20))
            if w: types.append(CustomerType(frozenset(j for j in range(p) if mask>>j&1),w))
        inst=Instance(tuple('T'+str(j) for j in range(p)),tuple(types),m)
        bad=attack(inst)
        if bad:
            print(json.dumps({'status':'TB-ANY counterexample','iteration':it,'seed':args.seed,**bad},indent=2)); break
        if it%50==0: print(json.dumps({'iteration':it,'elapsed':time.time()-start}),flush=True)
    else: print(json.dumps({'status':'finite negative only','trials':args.trials,'seed':args.seed,'elapsed':time.time()-start}))
