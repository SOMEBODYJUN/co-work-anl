"""One explicit strategy-cone attack on the r-variable recursive stair.

For fixed true SPE action maps, maximize a common strict gap against every
branch of the proposed max. Float LP only proposes points. Positive witnesses
are rationalized and verified at every ordered history, including unit clones.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import StrategyCertificate,verify_certificate
from tests.audits.customer_attraction_strategy_lp import (
    StrategyCone,payoff_row,dot,integer_clones,instance_from_clones,
)
from attack_minimum_gap import unit_check,serial
HERE=Path(__file__).resolve().parent


def counts(p,h):
    return tuple(h.count(a) for a in range(p))


def profit_row(p,b,c):
    answer=[]
    for mask in range(1,1<<p):
        bc=sum(b[a] for a in range(p) if mask&(1<<a))
        cc=sum(c[a] for a in range(p) if mask&(1<<a))
        answer.append(Fraction(cc,bc+cc) if cc else Fraction(0))
    return tuple(answer)


def floor_row(p,b,r,a):
    return tuple(Fraction(1,sum(b[t] for t in range(p) if mask&(1<<t))+r)
                 if mask&(1<<a) else Fraction(0) for mask in range(1,1<<p))


def recover(rows,eq,floating,n):
    support=[i for i in range(n) if floating[i]>1e-8]+[n]
    active=[(eq,Fraction(1))]+[(row,Fraction(0)) for row in rows
             if abs(sum(float(a)*x for a,x in zip(row,floating)))<1e-7]
    basis={}
    for row,rhs in active:
        v=[row[i] for i in support]+[rhs]
        for j in sorted(basis):
            z=v[j]
            if z:v=[a-z*b for a,b in zip(v,basis[j])]
        pivot=next((j for j,x in enumerate(v[:-1]) if x),None)
        if pivot is None:
            if v[-1]:return None
            continue
        z=v[pivot];basis[pivot]=[x/z for x in v]
        if len(basis)==len(support):break
    if len(basis)!=len(support):return None
    result=[Fraction(0)]*len(support)
    for j in sorted(basis,reverse=True):
        row=basis[j];result[j]=row[-1]-sum(row[k]*result[k] for k in range(j+1,len(result)))
    out=[Fraction(0)]*(n+1)
    for i,x in zip(support,result):out[i]=x
    return tuple(out)


def attack(name,p,m,O):
    source=ROOT/"evidence/certificates/customer_attraction"/(name+".json")
    obj=json.loads(source.read_text());s=obj.get("strategy",obj)
    actions={tuple(v["history"]):v["action"] for v in s["actions"]}
    cone=StrategyCone(p,m,actions);n=(1<<p)-1
    b=(0,)*p;r=m;A=actions[()];child=tuple(int(i==A) for i in range(p))
    root_portfolios=tuple(counts(p,h) for h in combinations_with_replacement(range(p),r))
    child_portfolios=tuple(counts(p,h) for h in combinations_with_replacement(range(p),r-1))
    objective=profit_row(p,b,counts(p,O))
    u=payoff_row(p,cone.root,A)
    rows=[tuple(row)+(Fraction(0),) for row in cone.rows]
    row_names=["SPE"]*len(rows)
    # O must really be a maximizing r-theme portfolio.
    for c in root_portfolios:
        rows.append(tuple(x-y for x,y in zip(objective,profit_row(p,b,c)))+(Fraction(0),))
        row_names.append("O_optimal")
    for a in range(p):
        rows.append(tuple(x-2*r*y for x,y in zip(objective,floor_row(p,b,r,a)))+(Fraction(-1),))
        row_names.append("root_floor")
    for c in child_portfolios:
        rows.append(tuple(x-2*v-y for x,v,y in zip(objective,u,profit_row(p,child,c)))+(Fraction(-1),))
        row_names.append("child_profit")
    for a in range(p):
        rows.append(tuple(x-2*v-2*(r-1)*y for x,v,y in zip(objective,u,floor_row(p,child,r-1,a)))+(Fraction(-1),))
        row_names.append("child_floor")
    eq=tuple(cone.welfare)+(Fraction(0),)
    c=np.zeros(n+1);c[-1]=-1
    res=linprog(c,A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),
                A_eq=np.array([eq],dtype=float),b_eq=[1],
                bounds=[(0,None)]*n+[(None,None)],method="highs")
    report={"source":str(source.relative_to(ROOT)),"topics":p,"players":m,
            "root_comparison_portfolio":O,"row_count":len(rows),"spe_rows":len(cone.rows),
            "root_portfolios":len(root_portfolios),"child_portfolios":len(child_portfolios),
            "floating_status":res.message,"floating_bound_is_not_a_certificate":True}
    if not res.success:return report
    q=tuple(Fraction(float(x)).limit_denominator(10**8) for x in res.x)
    if dot(eq,q)!=1 or any(x<0 for x in q[:n]) or any(dot(row,q)<0 for row in rows):
        q=recover(rows,eq,res.x,n)
    exact=q is not None and dot(eq,q)==1 and all(x>=0 for x in q[:n]) and all(dot(row,q)>=0 for row in rows)
    report.update({"floating_gap":float(-res.fun),"exact_primal_valid":exact})
    if not exact:return report
    report["normalized_gap"]=q[-1]
    beta=Fraction(float(-res.eqlin.marginals[0])).limit_denominator(10**8)
    mu=tuple(Fraction(float(-x)).limit_denominator(10**8) for x in res.ineqlin.marginals)
    # r_B >=0, while d is free: the d dual residual must equal zero.
    target=tuple([Fraction(0)]*n+[Fraction(1)])
    residual=tuple(beta*w-sum(z*row[j] for z,row in zip(mu,rows))-v
                   for j,(w,v) in enumerate(zip(eq,target)))
    dual=all(x>=0 for x in mu) and all(x>=0 for x in residual[:n]) and residual[-1]==0
    report["exact_dual_bound"]=beta if dual else None
    report["exact_dual_optimal"]=dual and beta==q[-1]
    report["dual_nonzero_multipliers"]=[(i,x) for i,x in enumerate(mu) if x] if dual else None
    if q[-1]>0:
        clones=integer_clones(q[:n]);instance=instance_from_clones(p,m,clones)
        cert=StrategyCertificate(actions,cone.root)
        check=verify_certificate(instance,cert);check.assert_valid()
        independent=unit_check(instance,cert)
        actual_u=instance.topic_payoffs(cone.root)[A]
        Froot=max(dot(profit_row(p,b,c),clones) for c in root_portfolios)
        hroot=max(dot(floor_row(p,b,r,a),clones) for a in range(p))
        Fchild=max(dot(profit_row(p,child,c),clones) for c in child_portfolios)
        hchild=max(dot(floor_row(p,child,r-1,a),clones) for a in range(p))
        rhs=max(2*r*hroot,2*actual_u+max(Fchild,2*(r-1)*hchild))
        assert Froot>rhs
        report.update({"status":"exact_counterexample","instance":instance.to_dict(),
                       "strategy":cert.to_dict(),"unit_audit":independent,
                       "Froot":Froot,"hroot":hroot,"Fchild":Fchild,"hchild":hchild,
                       "actual_first_payoff":actual_u,"right_hand_side":rhs,
                       "strict_gap":Froot-rhs})
    else:report["status"]="no_positive_gap_in_selected_cone_and_O"
    return report


def main():
    cases=[("root_tax_failure",6,4,(0,1,2,3)),
           ("prefix_balance_failure",6,4,(0,3,4,5))]
    reports=[]
    for case in cases:
        report=attack(*case);reports.append(report)
        (HERE/"recursive_step_attack.json").write_text(json.dumps(serial(reports),indent=2)+"\n")
        print(serial({k:v for k,v in report.items() if k not in ("instance","strategy","dual_nonzero_multipliers")}),flush=True)
        if report.get("status")=="exact_counterexample":break


if __name__=="__main__":main()
