#!/usr/bin/env python3
"""Exact two-agent/two-good-type check; finite evidence, no novelty claim.

Each agent has positive additive values (1,a) and (1,b). Multiplicities
are A,B. Fractional Pareto optimality is checked twice: a positive-weight
support interval, and exact vertices of the fractional domination polygon.
Fairness uses own-value/own-entitlement >= alpha * trimmed-other/other-entitlement.
"""
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import platform


def support_fpo(A, B, a, b, x, y):
    lo, hi = F(0), None
    for total, own, ratio in ((A, x, F(1)), (B, y, b/a)):
        if own:
            lo = max(lo, ratio)
        if own < total:
            hi = ratio if hi is None else min(hi, ratio)
    return hi is None or lo <= hi


def domination_fpo(A, B, a, b, x, y):
    u1, u2 = x+a*y, A-x+b*(B-y)
    # px+qy <= r. Last inequalities enforce weak domination.
    lines = [(F(-1), F(0), F(0)), (F(1), F(0), F(A)),
             (F(0), F(-1), F(0)), (F(0), F(1), F(B)),
             (F(-1), -a, -u1), (F(1), b, F(A)+b*B-u2)]
    vertices = {(F(x), F(y))}
    for (p,q,r), (s,t,u) in combinations(lines, 2):
        det = p*t-s*q
        if det:
            vx, vy = (r*t-u*q)/det, (p*u-s*r)/det
            if all(c*vx+d*vy <= e for c,d,e in lines):
                vertices.add((vx,vy))
    for vx, vy in vertices:
        v1, v2 = vx+a*vy, F(A)-vx+b*(B-vy)
        if v1 >= u1 and v2 >= u2 and (v1 > u1 or v2 > u2):
            return False
    return True


def quality(A, B, a, b, x, y, w1=F(1), w2=F(1)):
    result = F(1)
    for own, other, vals, wi, wj in (
        ((x,y), (A-x,B-y), (F(1),a), w1,w2),
        ((A-x,B-y), (x,y), (F(1),b), w2,w1)):
        own_u = sum(n*v for n,v in zip(own, vals))
        other_u = sum(n*v for n,v in zip(other, vals))
        for n,v in zip(other, vals):
            if n and other_u-v > 0:
                result = min(result, own_u*wj/((other_u-v)*wi))
    return result


def instance(A, B, a, b, w1=F(1), w2=F(1), crosscheck=True):
    allocations = []
    for x,y in product(range(A+1), range(B+1)):
        supported = support_fpo(A,B,a,b,x,y)
        if crosscheck:
            assert supported == domination_fpo(A,B,a,b,x,y), (A,B,a,b,x,y)
        allocations.append({"counts_agent1":[x,y], "fpo":supported,
                            "quality":str(quality(A,B,a,b,x,y,w1,w2))})
    best = max(F(row["quality"]) for row in allocations if row["fpo"])
    return {"A":A,"B":B,"a":str(a),"b":str(b),
            "weights":[str(w1),str(w2)],"best_fpo_quality":str(best),
            "efx_allocations":[r["counts_agent1"] for r in allocations if r["quality"]=="1"],
            "best_fpo_allocations":[r["counts_agent1"] for r in allocations
                                    if r["fpo"] and F(r["quality"])==best]}


def main():
    # Includes no goods, absent types, identical valuations, one item, small
    # rational values and unequal entitlements. Strict positivity is required.
    checked_instances = checked_allocations = 0
    vals = tuple(map(F, ("1/2","1","2","3")))
    for A,B,a,b in product(range(4),range(4),vals,vals):
        out = instance(A,B,a,b)
        checked_instances += 1
        checked_allocations += (A+1)*(B+1)
        if a == b:
            assert out["best_fpo_quality"] == "1"
    paper = instance(2,2,F(10),F(9))
    assert paper["efx_allocations"] == [[1,1]]
    assert paper["best_fpo_quality"] == "10/11"
    assert F(paper["best_fpo_quality"])*11 == 10
    # Paper's explicit fractional domination witness, exact reverse checks.
    assert F(11,10)*10 == 11
    assert 2+F(9,10)*9 > 10
    family = [instance(2,2,F(k),F(k-1)) for k in (3,4,5,10,100)]
    weighted = [instance(2,2,F(10),F(9),F(w),F(1)) for w in (1,2,3)]
    return {"status":"finite exact crosscheck; known counterexample reproduced",
            "source":"https://arxiv.org/html/2601.03438v1#S1.SSx2",
            "python":platform.python_version(),
            "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "arithmetic":"fractions.Fraction; no numerical solver",
            "checked_instances":checked_instances,"checked_allocations":checked_allocations,
            "paper_counterexample":paper,"parameter_family":family,
            "weighted_examples":weighted,
            "limits":"Finite grid does not prove a universal approximation bound. "
                     "All valuations positive. Compressed counts: no bit-polynomial algorithm claim."}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
