"""Attack only the residual-entry candidate, never certify universal half.

For one fixed complete-history strategy cone, maximize m-coverable customers
missed by its on-path terminal, normalized by on-path welfare.  Numerical LP
points are accepted only after exact Fraction cone verification.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/audits"))
import numpy as np
from scipy.optimize import linprog
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (
    StrategyCone, coverage_row, dot, integer_clones, instance_from_clones,
    serializable, structural_seeds,
)
from cone_attack_credible_variants import credible_cone


def optimize(cone, support):
    cover = coverage_row(cone.topics, support)
    objective = tuple(v * (1-w) for v,w in zip(cover, cone.welfare))
    res = linprog(-np.array(objective,dtype=float), A_ub=-cone.matrix,
                  b_ub=np.zeros(len(cone.rows)),
                  A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],
                  bounds=(0,None),method="highs")
    if not res.success:
        return None
    values = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
    if not cone.verify(values) or dot(cone.welfare,values)!=1:
        values = cone.recover_vertex(res.x)
    if values is None or not cone.verify(values) or dot(cone.welfare,values)!=1:
        return None
    return {"value":dot(objective,values),"values":values,"support":support}


def run(topics,players,count,seed):
    rng=random.Random(seed)
    sources=list(structural_seeds(topics,players))
    for _ in range(count):
        density=rng.choice([.2,.4,.7,1.])
        sources.append(tuple(rng.randrange(1,12) if rng.random()<density else 0
                             for _ in range((1<<topics)-1)))
    best=Fraction(0);solves=cones=0
    for index,clones in enumerate(sources):
        if not any(clones):continue
        ins=instance_from_clones(topics,players,clones)
        solver=ExactSPESolver(ins)
        targets=sorted(solver.worst_outcomes())
        for target in targets[:2]:
            cone,_=credible_cone(solver,target,rng,"uniform_credible")
            cones+=1
            for support in combinations(range(topics),min(topics,players)):
                result=optimize(cone,support);solves+=1
                if result is None:continue
                if result["value"]>best:
                    best=result["value"]
                    print(json.dumps({"event":"best","topics":topics,"players":players,
                                      "source":index,"cones":cones,"solves":solves,
                                      "value":str(best)},ensure_ascii=False),flush=True)
                if result["value"]>1:
                    integer=integer_clones(result["values"])
                    witness=instance_from_clones(topics,players,integer)
                    certificate=StrategyCertificate(cone.actions,cone.root)
                    verify_certificate(witness,certificate).assert_valid()
                    return {"status":"candidate_refuted","instance":witness.to_dict(),
                            "strategy":certificate.to_dict(),"portfolio":result["support"],
                            "value":result["value"],"welfare":witness.welfare(cone.root),
                            "optimum":witness.optimal_welfare(),"cones":cones,"solves":solves,
                            "topics":topics,"players":players,"seed":seed}
    return {"status":"finite_attack_only","best":best,"cones":cones,"solves":solves,
            "topics":topics,"players":players,"seed":seed}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--topics",type=int,default=5)
    parser.add_argument("--players",type=int,default=3)
    parser.add_argument("--count",type=int,default=30)
    parser.add_argument("--seed",type=int,default=511)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    report=run(args.topics,args.players,args.count,args.seed)
    args.output.write_text(json.dumps(serializable(report),ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(serializable({k:v for k,v in report.items() if k not in ("strategy","instance")})),flush=True)
