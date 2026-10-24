"""Attack POP: sum_{r=1}^m Theta_r(empty) >= OPT_m.

POP is a necessary consequence of TB-ANY after adding an empty topic and
following it m times. This is only a finite, targeted bridge attack.
"""
import argparse
from fractions import Fraction
from itertools import combinations
from math import lcm
import json
import random
import time
import numpy as np
from scipy.optimize import linprog
from customer_attraction import CustomerType, ExactSPESolver, Instance
from multicone_attack import local_certificate, data_from_actions, rational_vertex


def attempt(inst):
    p, m = inst.topic_count, inst.players
    D = lcm(*range(1, m + 1))
    rows = set()
    objective = [0] * ((1 << p) - 1)
    theta = []
    for r in range(1, m + 1):
        game = Instance(inst.topics, inst.customers, r)
        solver = ExactSPESolver(game)
        actions, _, _ = local_certificate(solver, ())
        rr, pp, _, DD = data_from_actions(p, r, actions, ())
        rows.update(rr)
        objective = [a + b * (D // DD) for a, b in zip(objective, pp)]
        theta.append(str(solver.threshold((0,) * p)))
    cmp = max((s for k in range(1, min(p, m) + 1) for s in combinations(range(p), k)),
              key=lambda s: inst.welfare(tuple(int(j in s) for j in range(p))))
    cmask = sum(1 << j for j in cmp)
    objective = [v - D * bool(B & cmask) for B, v in enumerate(objective, 1)]
    rows = sorted(rows)
    lp = linprog(objective, A_ub=-np.array(rows, dtype=float), b_ub=np.zeros(len(rows)),
                 A_eq=np.ones((1, len(objective))), b_eq=[1], bounds=(0, None), method='highs')
    if not lp.success:
        return {'status':'LP failure', 'message':lp.message}
    out = {'status':'nonnegative cone minimum', 'value':float(lp.fun / D),
           'p':p, 'm':m, 'constraints':len(rows), 'initial_theta':theta}
    if lp.fun >= -1e-7:
        return out
    out['status'] = 'negative float proposal'
    mass = rational_vertex(lp.x, rows)
    if mass is None:
        return out
    val = sum(a * y for a, y in zip(objective, mass)) / D
    if val >= 0:
        return out
    scale = lcm(*(v.denominator for v in mass))
    ints = [int(v * scale) for v in mass]
    new = Instance(tuple('T'+str(j) for j in range(p)), tuple(
        CustomerType(frozenset(j for j in range(p) if B >> j & 1), w)
        for B, w in enumerate(ints, 1) if w), m)
    roots = [ExactSPESolver(Instance(new.topics, new.customers, r)).threshold((0,) * p)
             for r in range(1, m + 1)]
    assert sum(roots) < new.optimal_welfare()
    out.update({'status':'exact POP / TB-ANY counterexample', 'instance':new.to_dict(),
                'theta':list(map(str, roots)), 'sumTheta':str(sum(roots)),
                'OPT':new.optimal_welfare(), 'exact_cone_value':str(val)})
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--trials', type=int, default=100)
    ap.add_argument('--seed', type=int, default=2026102403)
    args = ap.parse_args(); rng = random.Random(args.seed); best=1e9; start=time.time()
    for it in range(args.trials):
        p=rng.choice((4,5,6)); m=rng.choice((3,4,5,6))
        types=tuple(CustomerType(frozenset(j for j in range(p) if B >> j & 1),w)
                    for B in range(1,1<<p)
                    if (w:=rng.choice((0,0,0,0,0,1,2,5,10))))
        inst=Instance(tuple('T'+str(j) for j in range(p)),types,m)
        out=attempt(inst); best=min(best,out.get('value',best))
        if out['status'].startswith('exact'):
            print(json.dumps({'iteration':it,'seed':args.seed,**out},indent=2));break
        if it%10==0:print(json.dumps({'iteration':it,'elapsed':time.time()-start,
                                    'best_scaled_cone_minimum':best,'latest':out}),flush=True)
    else:print(json.dumps({'status':'finite cone attack only','trials':args.trials,
                           'seed':args.seed,'best_scaled_cone_minimum':best,'elapsed':time.time()-start}))
