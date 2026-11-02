"""One fixed existing complete strategy tests the inferred H4 endpoint bridge.

This is a candidate-specific LP, not a search over player counts or strategies.
The endpoint definition alpha=1 is reconstructed, not author-confirmed H4.
Floating LP values only propose exact Fraction candidates, checked below.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
from pathlib import Path
import importlib.util
import json
import sys

import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
SPEC=importlib.util.spec_from_file_location("strategy_lp",ROOT/"tests/audits/customer_attraction_strategy_lp.py")
LP=importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name]=LP
SPEC.loader.exec_module(LP)

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),F(0))

def run(alpha):
    raw=json.loads((ROOT/"evidence/certificates/customer_attraction/portfolio_matching_failure.json").read_text())
    acts={tuple(r["history"]):r["action"] for r in raw["actions"]}
    cone=LP.StrategyCone(5,2,acts)
    masks=range(1,1<<5)
    path=(4,0)
    target=(1,3)
    portfolios=list(combinations_with_replacement(range(5),2))
    actual_load=[sum(bool(mask&(1<<a)) for a in path) for mask in masks]
    erows={a:tuple(F(bool(mask&(1<<a)),1)/(1+alpha*c)
                   for mask,c in zip(masks,actual_load)) for a in range(5)}
    grow=tuple(F(bool(c),1)/(1+alpha*c) for c in actual_load)
    drows={}
    for i,h in enumerate(((),(4,))):
        for a in target:
            drows[i,a]=LP.payoff_row(5,cone.terminals[h+(a,)],a)
    matchrows=[tuple(drows[0,p[0]][j]+drows[1,p[1]][j] for j in range(31))
               for p in permutations(target)]
    # z >= each matching sum. Maximize endpoint_sum - G - z.
    objective=tuple(erows[1][j]+erows[3][j]-grow[j] for j in range(31))+(F(-1),)
    rows=[tuple(-v for v in r)+(F(0),) for r in cone.rows]
    bounds=[F(0)]*len(rows)
    for r in matchrows:
        rows.append(r+(F(-1),));bounds.append(F(0))
    cover=LP.coverage_row(5,target)
    for p in portfolios:
        if p==target:continue
        # Closed optimum constraints; all tied optima are checked after recovery.
        r=LP.coverage_row(5,p)
        rows.append(tuple(v-u for v,u in zip(r,cover))+(F(0),));bounds.append(F(0))
    res=linprog(-np.array(objective,float),A_ub=np.array(rows,float),b_ub=np.array(bounds,float),
                A_eq=np.array([cone.welfare+(F(0),)],float),b_eq=[1],bounds=(0,None),method="highs")
    report={"alpha":str(alpha),"source_strategy":"portfolio_matching_failure", "status":res.message,
            "scope":"one complete six-node strategy cone; inferred endpoint definition"}
    if not res.success:return report
    vals=tuple(F(float(x)).limit_denominator(10**6) for x in res.x)
    exact=(dot(cone.welfare,vals[:-1])==1 and cone.verify(vals[:-1])
           and all(dot(r,vals)<=b for r,b in zip(rows,bounds)))
    report.update(proposed_objective=str(dot(objective,vals)),exact_feasible=exact)
    if not exact:return report
    mult=vals[:-1]
    opt=dot(cover,mult)
    optimum=[p for p in portfolios if dot(LP.coverage_row(5,p),mult)==opt]
    def debt(p):
        matches=[]
        for perm in set(permutations(p)):
            s=F(0)
            for i,(h,a) in enumerate(zip(((),(4,)),perm)):
                s+=dot(LP.payoff_row(5,cone.terminals[h+(a,)],a),mult)
            matches.append(s)
        return sum((dot(erows[a],mult) for a in p),F(0))-max(matches)-dot(grow,mult)
    report.update(values={str(i):str(v) for i,v in zip(masks,mult) if v},
                  opt=str(opt),optimal_portfolios=[list(p) for p in optimum],
                  optimal_h4_debts={str(p):str(debt(p)) for p in optimum},
                  all_optima_fail=all(debt(p)>0 for p in optimum))
    return report

if __name__=="__main__":
    report={"claim_status":"candidate-specific finite diagnostic, not a universal theorem",
            "results":[run(F(1)),run(F(1,2))]}
    out=Path(__file__).with_name("probe_inferred_h4.json")
    out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
