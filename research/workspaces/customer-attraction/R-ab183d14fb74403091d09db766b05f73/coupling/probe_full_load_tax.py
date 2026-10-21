"""Search complete strategy cones for the explicitly stronger full-load-tax bridge.

This is discovery only. A reported positive violation is accepted only after
Fraction recovery of one common nonnegative customer vector and every ordered
history incentive. Q-CAG-HALF is not the objective of this script.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import random
import sys
import time

import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def counts(n, p):
    if p == 1:
        yield (n,)
    else:
        for j in range(n + 1):
            for tail in counts(n - j, p - 1):
                yield (j,) + tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--rounds', type=int, default=20)
    ap.add_argument('--seed', type=int, default=661093)
    ap.add_argument('--bridge', choices=['full-tax','entry'], default='full-tax')
    ap.add_argument('--output', default='full_load_tax_probe.json')
    args = ap.parse_args()
    n, p = args.players, args.topics
    types = tuple(range(1, 1 << p))
    terminals = tuple(counts(n, p))
    @lru_cache(None)
    def loads(q):
        return tuple(sum(q[a] for a in range(p) if b >> a & 1) for b in types)
    @lru_cache(None)
    def pay(q, a):
        return tuple(F(1, ell) if b >> a & 1 else F(0)
                     for b, ell in zip(types, loads(q)))
    cov = {q: tuple(int(v > 0) for v in loads(q)) for q in terminals}
    targets = tuple(sum(1 << a for a in t) for t in combinations(range(p), min(n, p)))
    cover = {t: tuple(int(bool(t & b)) for b in types) for t in targets}
    template = Instance(tuple('T' + str(a) for a in range(p)), (), n)
    rng = random.Random(args.seed)
    masses = None
    best = F(-100)
    witness = None
    records = []
    start = time.time()
    for step in range(args.rounds):
        if masses is None or step % 8 == 0:
            if step % 24 == 0:
                masses = tuple(F(n if b == 1 else 1 if b.bit_count() == 1 else 0) for b in types)
            else:
                masses = tuple(F(rng.randint(0, 9) if rng.random() < .2 else 0) for b in types)
        table = {q: tuple(sum((v*w for v,w in zip(pay(q,a), masses)), F(0)) if q[a] else F(0)
                          for a in range(p)) for q in terminals}
        solver = ExactSPESolver(template)
        solver._payoffs.update(table)
        outcomes = solver.outcomes()
        def objective_root(q):
            return sum((F(1)+F(v, v+1))*w for v,w in zip(loads(q),masses) if v)
        root = min(outcomes, key=lambda q: (objective_root(q), q))
        cert = solver.certificate(root)
        actions = dict(cert.actions)
        z = {}
        for k in range(n, -1, -1):
            for h in product(range(p), repeat=k):
                z[h] = tuple(h.count(a) for a in range(p)) if k == n else z[h+(actions[h],)]
        gamma = set()
        for h, a in actions.items():
            for b in range(p):
                row = tuple(x-y for x,y in zip(pay(z[h],a),pay(z[h+(b,)],b)))
                assert sum((v*w for v,w in zip(row,masses)),F(0)) >= 0
                if any(row):
                    gamma.add(row)
        gamma = tuple(gamma)
        mat = -np.array(gamma, dtype=float)
        eq = np.array([cov[root]],dtype=float)
        tau = tuple(F(v,v+1) for v in loads(root))
        if args.bridge == 'full-tax':
            target = max(targets,key=lambda t: sum(v*w for v,w in zip(cover[t],masses)))
            obj = tuple(F(v)-w for v,w in zip(cover[target],tau))
        else:
            entry = {a:tuple(F(n,v+1) if b >> a & 1 else F(0) for b,v in zip(types,loads(root))) for a in range(p)}
            target = max(range(p),key=lambda a:sum(v*w for v,w in zip(entry[a],masses)))
            obj = entry[target]
        res = linprog(-np.array(obj,dtype=float),A_ub=mat,b_ub=np.zeros(len(gamma)),
                      A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
        rec = {'round':step,'root':root,'target':target,'unique_true_rows':len(gamma),
               'ordered_histories':len(actions),'LP_success':bool(res.success)}
        masses = None
        if res.success:
            candidate = tuple(F(float(v)).limit_denominator(10**7) for v in res.x)
            if all(v >= 0 for v in candidate) and sum(v*w for v,w in zip(cov[root],candidate)) == 1 and all(sum((v*w for v,w in zip(row,candidate)),F(0)) >= 0 for row in gamma):
                masses = candidate
                score = sum((v*w for v,w in zip(obj,candidate)),F(0))
                rec['exact_O_minus_tau_over_W'] = str(score)
                if score > best:
                    best = score
                    witness = {'root':root,'target':target,'types':{str(b):str(w) for b,w in zip(types,candidate) if w},
                               'actions':[{'h':h,'a':a} for h,a in actions.items()],
                               'exact_score':str(score),'complete_common_nonnegative_customers':True}
                    print(json.dumps({'round':step,'new_exact_score':str(score),'n':n,'p':p}),flush=True)
        records.append(rec)
        (BASE/args.output).write_text(json.dumps({'players':n,'topics':p,'seed':args.seed,
            'Q_CAG_HALF':'OPEN','tested_bridge':('OPT <= W + sum_x c_x/(c_x+1)' if args.bridge == 'full-tax' else 'm max_T sum_x_in_T 1/(c_x+1) <= W'),
            'best_exact_score':str(best),'positive_bridge_violation':best>1,
            'witness':witness,'history':records,'elapsed_seconds':time.time()-start},indent=2)+'\n')
        if best > 1:
            break
    print(json.dumps({'completed':len(records),'best_exact_score':str(best),'elapsed':time.time()-start}),flush=True)


if __name__ == '__main__':
    main()
