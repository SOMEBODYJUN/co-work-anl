"""Unrestricted full-history SPE existence via outcome-witness DAG.

Numerical MILP is only a candidate generator. Its selected witness is unfolded
to a complete ordered-history strategy; exact fixed-cone reoptimization and
independent Fraction checks certify any reported candidate. No count-Markov
restriction is imposed on strategies: different desired outcomes at the same
count state may select different actions.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests/audits'))
from customer_attraction import ExactSPESolver, StrategyCertificate
from customer_attraction_strategy_lp import (StrategyCone, payoff_row,
    coverage_row, integer_clones, independently_verify, instance_from_clones,
    serializable, dot)


def counts(p, n):
    if p == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in counts(p - 1, n - a):
                yield (a,) + tail


def inc(q, a):
    return q[:a] + (q[a] + 1,) + q[a + 1:]


def query_row(p, q, a):
    m = sum(q)
    return tuple(Fraction(m, m + (m - 1) * sum(q[b] for b in range(p)
                 if mask & (1 << b))) if mask & (1 << a) else Fraction(0)
                 for mask in range(1, 1 << p))


def build(p, q, objective, seconds=30, fixed_clones=None):
    m = sum(q)
    n = (1 << p) - 1
    states = tuple(k for d in range(m + 1) for k in counts(p, d))
    leaves = tuple(counts(p, m))
    below = {k: tuple(c for c in leaves if all(x <= y for x, y in zip(k,c)))
             for k in states}
    y, z, x, t = {}, {}, {}, {}
    idx = n
    for k in states:
        for c in below[k]: y[k,c] = idx; idx += 1
        if sum(k) < m: t[k] = idx; idx += 1
    for k in t:
        for a in range(p):
            for c in below[inc(k,a)]:
                z[k,c,a] = idx; idx += 1
                x[k,a,c] = idx; idx += 1
    lo = np.zeros(idx)
    hi = np.ones(idx, dtype=float)
    integrality = np.zeros(idx, dtype=np.uint8)
    for j in (*y.values(), *z.values(), *x.values()):
        hi[j] = 1; integrality[j] = 1
    root = (0,) * p
    for c in leaves:
        lo[y[c,c]] = hi[y[c,c]] = 1
        lo[y[root,c]] = hi[y[root,c]] = int(c == q)
    if fixed_clones is not None:
        w = coverage_row(p, [a for a,v in enumerate(q) if v])
        scale = dot(w, fixed_clones)
        if scale <= 0:
            raise ValueError('fixed input must have positive candidate root welfare')
        for j,v in enumerate(fixed_clones):
            lo[j] = hi[j] = float(Fraction(v,scale))
    rs, cs, ds, lb, ub = [], [], [], [], []
    def add(row, lower=-np.inf, upper=np.inf):
        i = len(lb)
        for j,v in row.items():
            if v: rs.append(i); cs.append(j); ds.append(float(v))
        lb.append(lower); ub.append(upper)
    w = coverage_row(p, [a for a,v in enumerate(q) if v])
    add({j:v for j,v in enumerate(w) if v}, 1, 1)
    # Every on-path player can guarantee |T|/m by choosing T, so summing
    # the m actual utilities gives |T| <= W(root)=1 for every topic T.
    # Thus all subgame payoffs and thresholds are at most one; big-M=1.
    for a in range(p):
        add({j:1 for j in range(n) if (j+1) & (1 << a)}, upper=1)
    for k in t:
        for c in below[k]:
            row = {y[k,c]:-1}
            for a in range(p):
                if c[a] == k[a]: continue
                j = z[k,c,a]
                row[j] = 1
                add({j:1, y[inc(k,a),c]:-1}, upper=0)
                rr = {j:1, t[k]:1}
                for b,v in enumerate(payoff_row(p,c,a)):
                    if v: rr[b] = -v
                add(rr, upper=1)
            add(row, 0, 0)
        for a in range(p):
            add({x[k,a,c]:1 for c in below[inc(k,a)]}, 1, 1)
            for c in below[inc(k,a)]:
                j = x[k,a,c]
                add({j:1, y[inc(k,a),c]:-1}, upper=0)
                rr = {j:1, t[k]:-1}
                for b,v in enumerate(payoff_row(p,c,a)):
                    if v: rr[b] = v
                add(rr, upper=1)
    matrix = coo_matrix((ds,(rs,cs)), shape=(len(lb),idx)).tocsc()
    cost = np.zeros(idx); cost[:n] = -np.array(objective,dtype=float)
    started = time.monotonic()
    result = milp(cost, integrality=integrality, bounds=Bounds(lo,hi),
                  constraints=LinearConstraint(matrix, lb, ub),
                  options={'time_limit':seconds, 'mip_rel_gap':0.0})
    meta = {'topics':p, 'players':m, 'root_counts':q, 'variables':idx,
            'binary':len(y)+len(z)+len(x), 'rows':len(lb),
            'status':int(result.status), 'message':result.message,
            'seconds':time.monotonic()-started,
            'floating_value':float(-result.fun) if result.fun is not None else None,
            'floating_bound_not_a_certificate':True}
    if result.x is None: return None,meta
    actions = {}
    def expand(h, k, c):
        if len(h) == m: return
        admissible = [a for a in range(p) if (k,c,a) in z]
        a = max(admissible, key=lambda a: result.x[z[k,c,a]])
        if result.x[z[k,c,a]] < .9: raise AssertionError('nonintegral z witness')
        actions[h] = a
        for b in range(p):
            if b == a: d = c
            else:
                d = max(below[inc(k,b)], key=lambda d:result.x[x[k,b,d]])
                if result.x[x[k,b,d]] < .9: raise AssertionError('nonintegral x witness')
            expand(h+(b,), inc(k,b), d)
    expand((),root,q)
    cone = StrategyCone(p,m,actions)
    if cone.root != q: raise AssertionError('witness root mismatch')
    return cone,meta


def exact_optimize(cone, objective):
    r = linprog(-np.array(objective,dtype=float), A_ub=-cone.matrix,
                b_ub=np.zeros(len(cone.rows)), A_eq=[cone.welfare], b_eq=[1],
                bounds=(0,None), method='highs')
    if not r.success: return {'certified':False, 'status':r.message}
    v = tuple(Fraction(float(x)).limit_denominator(10**7) for x in r.x)
    if not cone.verify(v) or dot(cone.welfare,v) != 1:
        v = cone.recover_vertex(r.x)
    if v is None or not cone.verify(v) or dot(cone.welfare,v) != 1:
        return {'certified':False, 'status':'exact_recovery_failed'}
    clones = integer_clones(v)
    if not independently_verify(cone,clones): raise AssertionError('exact full-history failure')
    inst = instance_from_clones(cone.topics,cone.players,clones)
    return {'certified':True,'value':dot(objective,v), 'integer_clones':clones,
            'welfare':inst.welfare(cone.root),'optimal_welfare':inst.optimal_welfare(),
            'nodes':len(cone.actions),'deviation_checks':len(cone.actions)*(cone.topics-1),
            'strategy':StrategyCertificate(cone.actions,cone.root).to_dict()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root',required=True)
    ap.add_argument('--query',type=int)
    ap.add_argument('--budget',action='store_true',help='optimize m*g(query)+R')
    ap.add_argument('--portfolio')
    ap.add_argument('--seconds',type=float,default=30)
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    q = tuple(map(int,args.root.split(','))); p=len(q)
    if args.query is not None:
        objective = query_row(p,q,args.query)
        mode = {'query':args.query,'weak_factor':Fraction(2*sum(q)-1,2)}
        if args.budget:
            m = sum(q)
            R = tuple(Fraction((m-1)*sum(q[b] for b in range(p) if mask & (1<<b)),
                       m+(m-1)*sum(q[b] for b in range(p) if mask & (1<<b)))
                       for mask in range(1,1<<p))
            objective = tuple(m*g+r for g,r in zip(objective,R))
            mode = {'query':args.query,'exact_budget':'m*g+R'}
    else:
        J = tuple(map(int,args.portfolio.split(',')))
        objective = coverage_row(p,J); mode={'portfolio':J}
    cone,meta = build(p,q,objective,args.seconds)
    report = {'scope':'unrestricted outcome-witness DAG candidate generation',
              'universal_bound_proved':False,'mode':mode,'milp':meta,
              'exact_candidate':exact_optimize(cone,objective) if cone else None}
    args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
    summary = dict(report)
    if summary['exact_candidate']:
        summary['exact_candidate'] = {k:v for k,v in summary['exact_candidate'].items()
            if k not in ('strategy','integer_clones')}
    print(json.dumps(serializable(summary)),flush=True)


if __name__ == '__main__': main()
