"""Target the general root-insurer counterexample interface, never a proof scan.

For each sampled game select a full positive-depth SPE plan, optimize all
customer-type multiplicities in its strategy cone, and ask whether
OPT_m-2W-3*root_regret > 0.  Such a witness compiles to a genuine Q-CAG-HALF
counterexample using the existing padded-insurer theorem. Floating LP is only
discovery; every positive report is independently checked with Fraction over
all ordered histories, and includes the full source plan.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json
import math
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.exact import ExactSPESolver
from customer_attraction.model import CustomerType, Instance

OUT = Path(__file__).resolve().parent


def increment(q, a):
    return q[:a] + (q[a]+1,) + q[a+1:]


def source_plan(solver, prescribed, desired):
    """Retain every ordered history; only root may fail optimality."""
    inst = solver.instance
    p, m = inst.topic_count, inst.players
    actions = {(): prescribed}

    def expand(h, q, target):
        if len(h) == m:
            assert q == target
            return
        floor = solver.threshold(q)
        choices = [a for a in range(p)
                   if target in solver.outcomes(increment(q, a))
                   and inst.topic_payoff(a, target) >= floor]
        chosen = choices[0]
        actions[h] = chosen
        for a in range(p):
            child = increment(q, a)
            child_target = (target if a == chosen else min(
                solver.outcomes(child),
                key=lambda z: (inst.topic_payoff(a, z), z)))
            expand(h+(a,), child, child_target)

    zero = (0,)*p
    for a in range(p):
        child = increment(zero, a)
        target = (desired if a == prescribed else min(
            solver.outcomes(child), key=lambda z: (inst.topic_payoff(a,z), z)))
        expand((a,), child, target)
    return actions


def cone_data(p, m, actions):
    masks = tuple(range(1, 1 << p))

    @lru_cache(None)
    def leaf(h):
        return h if len(h) == m else leaf(h+(actions[h],))

    def row(h, a):
        return tuple(F(1, sum((mask >> b) & 1 for b in h))
                     if (mask >> a) & 1 else F(0) for mask in masks)

    actual_leaf = leaf(())
    actual = row(actual_leaf, actions[()])
    welfare = tuple(int(any((mask >> a) & 1 for a in actual_leaf)) for mask in masks)
    inequalities = []
    for h, action in actions.items():
        if not h:
            continue
        u = row(leaf(h), action)
        for a in range(p):
            if a != action:
                v = row(leaf(h+(a,)), a)
                inequalities.append(tuple(vv-uu for uu,vv in zip(u,v))+(F(0),))
    for a in range(p):
        v = row(leaf((a,)), a)
        inequalities.append(tuple(vv-uu for uu,vv in zip(actual,v))+(F(-1),))
    return masks, welfare, inequalities, actual_leaf


def exact_positive(p, m, actions, vals, support):
    masks, w, rows, actual = cone_data(p,m,actions)
    if any(x < 0 for x in vals):
        return None
    if any(sum(a*b for a,b in zip(row,vals)) > 0 for row in rows):
        return None
    W = sum(F(a)*b for a,b in zip(w, vals))
    O = sum(v for mask,v in zip(masks,vals) if any((mask >> a) & 1 for a in support))
    margin = O-2*W-3*vals[-1]
    if margin <= 0:
        return None
    scale = math.lcm(*(x.denominator for x in vals))
    integer = [int(x*scale) for x in vals]
    # The exact task has a set of coverage subsets, not duplicate action labels.
    signatures=[frozenset(mask for mask,x in zip(masks,integer) if x and (mask>>a)&1)
                for a in range(p)]
    if len(set(signatures)) != p:
        return None
    return {"players":m,"topics":p,"types":[[mask,x] for mask,x in zip(masks,integer) if x],
            "actions":[{"history":h,"action":a} for h,a in sorted(actions.items())],
            "actual":actual,"comparison":support,"delta_bound":integer[-1],
            "W":str(W),"O":str(O),"margin":str(margin),"scale":scale}


def save_seed_source(inst, actions, sample, index):
    """Freeze the exact full ordered plan behind every finite discovery cone."""
    p,m=inst.topic_count,inst.players
    masks,w,rows,actual=cone_data(p,m,actions)
    counts=[0]*(1<<p)
    for t in inst.customers:
        counts[sum(1<<a for a in t.topics)]+=t.multiplicity
    def leaf(h):
        while len(h)<m:
            h=h+(actions[h],)
        return h
    actual_u=inst.player_payoffs(actual)[0]
    root_u=[inst.player_payoffs(leaf((a,)))[0] for a in range(p)]
    delta=max(root_u)-actual_u
    vals=[F(counts[mask]) for mask in masks]+[delta]
    assert all(sum(a*b for a,b in zip(row,vals))<=0 for row in rows)
    assert len(actions)==sum(p**d for d in range(m))
    data={"kind":"full root-only source plan; root may be suboptimal",
          "instance":inst.to_dict(),
          "actions":[[h,a] for h,a in sorted(actions.items())],
          "actual":actual,"root_deviation_payoffs":list(map(str,root_u)),
          "actual_root_payoff":str(actual_u),"root_regret":str(delta),
          "positive_depth_decision_histories":len(actions)-1,
          "all_ordered_positive_depth_IC_verified_exactly":True,
          "W":inst.welfare(inst.counts(actual)),"OPT_m":inst.optimal_welfare()}
    path=OUT/f"seed_source_{sample}_{index}.json"
    path.write_text(json.dumps(data,separators=(",",":")))
    return path.name


def attack(inst, sample, max_sources=2):
    p,m=inst.topic_count,inst.players
    solver=ExactSPESolver(inst)
    zero=(0,)*p
    threshold=solver.threshold(zero)
    sources=[]
    for a in range(p):
        for z in solver.outcomes(increment(zero,a)):
            delta=max(F(0),threshold-inst.topic_payoff(a,z))
            # Root-suboptimal sources are the distinct target of this attack;
            # actual SPE sources remain available after them.
            sources.append((delta == 0,2*inst.welfare(z)+3*delta,a,z))
    sources.sort()
    seen=set()
    report=[]
    for _,_,a,z in sources:
        if (a,z) in seen:
            continue
        seen.add((a,z))
        actions=source_plan(solver,a,z)
        source_file=save_seed_source(inst,actions,sample,len(report))
        blockers=[b for b in range(p) if actions[(b,)*(m-1)] == b]
        if blockers:
            report.append({"prescribed":a,"source_terminal":z,
                           "exact_seed_source":source_file,
                           "exact_screen":"homogeneous terminal reply",
                           "blocking_topics":blockers})
            if len(report)>=max_sources:
                break
            continue
        masks,w,rows,actual=cone_data(p,m,actions)
        A=np.array([[float(v) for v in row] for row in rows])
        best=None
        for support in combinations(range(p),min(m,p)):
            o=tuple(int(any((mask >> b)&1 for b in support)) for mask in masks)
            objective=np.array([2*ww-oo for ww,oo in zip(w,o)]+[3.0])
            res=linprog(objective,A_ub=A,b_ub=np.zeros(len(rows)),
                        A_eq=np.array([list(w)+[0.0]]),b_eq=[1.0],
                        bounds=(0,None),method="highs")
            if not res.success:
                raise RuntimeError(res.message)
            if best is None or res.fun<best:
                best=res.fun
            if res.fun < -1e-7:
                vals=[F(float(v)).limit_denominator(1000000) for v in res.x]
                cert=exact_positive(p,m,actions,vals,support)
                if cert:
                    path=OUT/f"root_regret_positive_{sample}.json"
                    path.write_text(json.dumps(cert,indent=2))
                    print("EXACT POSITIVE",path,flush=True)
                    return {"sample":sample,"positive":str(path)}
        report.append({"prescribed":a,"source_terminal":z,
                       "exact_seed_source":source_file,
                       "numerical_max_repair_margin_per_W":-best})
        if len(report)>=max_sources:
            break
    return {"sample":sample,"players":m,"topics":p,"source_cones":report}


def seed(m,rng,variant):
    # General growing all-big source candidate, with correlated omitted clients.
    p=m+2
    types=[CustomerType(frozenset({0}),m-1)]
    types.extend(CustomerType(frozenset({a}),1) for a in range(1,m+1))
    if variant:
        # Cross-topic clients deliberately leave the private-omission theorem.
        for _ in range(2*p):
            mask=rng.randrange(1,1<<p)
            if mask.bit_count()>1:
                types.append(CustomerType(frozenset(a for a in range(p) if mask>>a&1),rng.randrange(1,4)))
    return Instance(tuple(map(str,range(p))),tuple(types),m)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--players",type=int,nargs="+",default=[3,4])
    parser.add_argument("--variants",type=int,default=2)
    parser.add_argument("--sources",type=int,default=2)
    args=parser.parse_args()
    rng=random.Random(791883)
    report={"purpose":"discover a genuine half counterexample via the general root-insurer interface",
            "seed":791883,"status":"finite discovery only; negative numerical optima are not theorem certificates", "samples":[]}
    for m in args.players:
        for variant in range(args.variants):
            sample=f"m{m}_v{variant}"
            result=attack(seed(m,rng,variant),sample,args.sources)
            report["samples"].append(result)
            (OUT/"root_regret_discovery_report.json").write_text(json.dumps(report,indent=2))
            print(json.dumps(result),flush=True)
            if "positive" in result:
                return


if __name__=="__main__":
    main()
