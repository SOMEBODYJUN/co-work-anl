"""Jointly choose early multipliers with a reachable leafwise square error.

The restricted cone allows arbitrary terminal normalized multipliers and requires
each changed leaf's actual divergence to be t(e_old_reply-e_new_reply), t>=0.
Float LP only proposes certificates; accepted upper/lower bounds use Fraction.
"""
from fractions import Fraction as F
from itertools import combinations, product
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from paired_lift_search import data, dot, normalize


def build(actions,p,n):
    old_e,old_l,c,keys,_,root=data(actions,p,n)
    bar=normalize(actions,p,n,root)
    e,l,bc,_,_,_=data(bar,p,n)
    assert bc==c
    ends={h:h for h in product(range(p),repeat=n)}
    for d in range(n-1,-1,-1):
        for h in product(range(p),repeat=d):
            ends[h]=ends[h+(actions[h],)]
    changed={h for h in actions if len(h)==n-1 and actions[h]!=bar[h]}
    incidence={(h,s):[F(0)]*len(e) for h in changed for s in set(h)}
    for j,(h,a) in enumerate(keys):
        target,source=ends[h][:-1],ends[h+(a,)][:-1]
        if target in changed:
            incidence[(target,actions[h])][j]+=1
        if source in changed:
            incidence[(source,a)][j]-=1
    equalities=[]; inequalities=[]
    zero=[F(0)]*len(e)
    for h in sorted(changed):
        a,b=actions[h],bar[h]
        ka=incidence.get((h,a),zero);kb=incidence.get((h,b),zero)
        for s in set(h)-{a,b}:
            equalities.append(incidence[(h,s)])
        equalities.append([x+y for x,y in zip(ka,kb)])
        inequalities.append([-x for x in ka])
    equalities=[row for row in equalities if any(row)]
    inequalities=[row for row in inequalities if any(row)]
    count=len(e)+len(l)+1
    eq=[tuple(row)+(F(0),)*(len(l)+1) for row in equalities]
    inc=[tuple(row)+(F(0),)*(len(l)+1) for row in inequalities]
    certificate_rows=[tuple(row[t] for row in e+l)+(-c[t],) for t in range(len(c))]
    return e,l,c,eq,inc,certificate_rows,changed


def optimize(actions,p,n,support):
    e,l,c,eq,inc,rows,changed=build(actions,p,n)
    mask=sum(1<<a for a in support)
    o=tuple(F(bool(mask&T)) for T in range(1,1<<p))
    ub=rows+inc;b=[-z for z in o]+[F(0)]*len(inc)
    objective=[F(0)]*(len(e)+len(l))+[F(1)]
    result=linprog(np.array(objective,float),A_ub=np.array(ub,float),b_ub=np.array(b,float),
        A_eq=np.array(eq,float) if eq else None,b_eq=np.zeros(len(eq)) if eq else None,
        bounds=(0,None),method="highs")
    if not result.success:
        return dict(status="floating_infeasible_or_error",message=result.message)
    x=tuple(F(float(z)).limit_denominator(10**7) for z in result.x)
    upper_ok=min(x)>=0 and all(dot(row,x)<=rhs for row,rhs in zip(ub,b)) and all(dot(row,x)==0 for row in eq)
    y=tuple(F(float(z)).limit_denominator(10**7) for z in result.ineqlin.marginals)
    z=tuple(F(float(t)).limit_denominator(10**7) for t in result.eqlin.marginals)
    dual_columns=tuple(sum(y[i]*ub[i][j] for i in range(len(ub)))
        +sum(z[i]*eq[i][j] for i in range(len(eq))) for j in range(len(objective)))
    lower_ok=all(t<=0 for t in y) and all(t<=v for t,v in zip(dual_columns,objective))
    lower=dot(y,b) if lower_ok else None
    return dict(status="candidate_checked",upper=str(x[-1]) if upper_ok else None,
        lower=str(lower) if lower is not None else None,
        changed_leaves=len(changed),early_rows=len(e),terminal_rows=len(l),
        equality_rows=len(eq),incidence_inequality_rows=len(inc),
        upper_sparse=[[j,str(t)] for j,t in enumerate(x) if t] if upper_ok else None,
        dual_ub_sparse=[[j,str(t)] for j,t in enumerate(y) if t] if lower_ok else None,
        dual_eq_sparse=[[j,str(t)] for j,t in enumerate(z) if t] if lower_ok else None)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,default=Path("evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json"))
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--limit",type=int,default=70)
    args=parser.parse_args()
    source=json.loads(args.source.read_text());p=source["parameters"]["topics"];n=source["parameters"]["players"]
    records=[];maximum_lower=F(0);maximum_upper=F(0);bad=0
    for i,cone in enumerate(source["cone_proofs"][:args.limit]):
        actions={tuple(x["history"]):x["action"] for x in cone["actions"]}
        for support in combinations(range(p),min(n,p)):
            result=optimize(actions,p,n,support)
            result.update(cone=i,support=support)
            records.append(result)
            if result.get("lower"):
                maximum_lower=max(maximum_lower,F(result["lower"]))
                if F(result["lower"])>2:
                    bad+=1
                    print(json.dumps(dict(cone=i,support=support,exact_lower=result["lower"])),flush=True)
            if result.get("upper"):
                maximum_upper=max(maximum_upper,F(result["upper"]))
        if i%10==0:
            print(json.dumps(dict(cones_processed=i+1,max_exact_lower=str(maximum_lower),max_exact_upper=str(maximum_upper))),flush=True)
    report=dict(scope="restricted leafwise-square joint multiplier template; no universal theorem",
        source=str(args.source),records=records,exact_lower_above_two=bad,
        max_exact_lower=str(maximum_lower),max_exact_upper=str(maximum_upper))
    args.output.write_text(json.dumps(report,indent=2)+"\n")


if __name__=="__main__":
    main()
