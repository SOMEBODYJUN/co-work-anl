"""Attack ROW inside the one root-tax / 69-customer full SPE strategy cone.

ROW: OPT-W <= sum_{T in an optimal m-tuple J} V_iT, with every V taken at
the same actual node i and followed by the same complete strategy.
No new strategy sampling is performed. LP only generates rational candidates.
"""
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
    StrategyCone,coverage_row,payoff_row,dot,integer_clones,instance_from_clones,
)
from attack_minimum_gap import serial,unit_check
HERE=Path(__file__).resolve().parent


def recover(rows,w,floating):
    support=[i for i,x in enumerate(floating) if x>1e-8]
    active=[(w,Fraction(1))]+[(row,Fraction(0)) for row in rows
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
    solution=[Fraction(0)]*len(support)
    for j in sorted(basis,reverse=True):
        solution[j]=basis[j][-1]-sum(basis[j][k]*solution[k] for k in range(j+1,len(solution)))
    out=[Fraction(0)]*len(floating)
    for i,x in zip(support,solution):out[i]=x
    return tuple(out)


def main():
    source=ROOT/"evidence/certificates/customer_attraction/root_tax_failure.json"
    obj=json.loads(source.read_text());s=obj["strategy"]
    actions={tuple(v["history"]):v["action"] for v in s["actions"]}
    p=6;m=4;cone=StrategyCone(p,m,actions)
    path=[]
    while len(path)<m:path.append(actions[tuple(path)])
    tuples=list(combinations_with_replacement(range(p),m))
    tuples.remove((0,1,2,3));tuples.insert(0,(0,1,2,3))
    report={"scope":"one fixed complete root-tax strategy cone, all Gamma retained",
            "source":str(source.relative_to(ROOT)),"players":m,"topics":p,
            "actual_path":path,"cases":[],"universal_ROW_proved":False}
    checked_duals=0;failed_duals=0
    best=None
    for J in tuples:
        O=coverage_row(p,set(J))
        rows=list(cone.rows)+[tuple(x-y for x,y in zip(O,coverage_row(p,set(K)))) for K in tuples]
        A_ub=-np.array(rows,dtype=float)
        # Positions 1--3 have the same actual prefix/future-A multiset. Their
        # supplied terminal payoff rows are explicitly checked equal below.
        objectives=[]
        for i in range(m):
            h=tuple(path[:i])
            V=tuple(payoff_row(p,cone.terminals[h+(t,)],t) for t in J)
            objective=tuple(o-w-sum(v[j] for v in V) for j,(o,w) in enumerate(zip(O,cone.welfare)))
            objectives.append((i,V,objective))
        assert objectives[0][2]==objectives[1][2]==objectives[2][2]
        for i,V,objective in (objectives[0],objectives[3]):
            result=linprog(-np.array(objective,dtype=float),A_ub=A_ub,b_ub=np.zeros(len(rows)),
                           A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method="highs")
            case={"J":J,"actual_position":i+1,"float_status":result.message}
            if not result.success:
                report["cases"].append(case);failed_duals+=1;continue
            values=tuple(Fraction(float(x)).limit_denominator(10**8) for x in result.x)
            if dot(cone.welfare,values)!=1 or any(x<0 for x in values) or any(dot(row,values)<0 for row in rows):
                values=recover(rows,cone.welfare,result.x)
            primal=values is not None and dot(cone.welfare,values)==1 and all(x>=0 for x in values) and all(dot(row,values)>=0 for row in rows)
            beta=Fraction(float(-result.eqlin.marginals[0])).limit_denominator(10**8)
            mu=tuple(Fraction(float(-x)).limit_denominator(10**8) for x in result.ineqlin.marginals)
            residual=tuple(beta*w-sum(z*row[j] for z,row in zip(mu,rows))-o for j,(w,o) in enumerate(zip(cone.welfare,objective)))
            dual=all(x>=0 for x in mu) and all(x>=0 for x in residual)
            checked_duals+=dual;failed_duals+=not dual
            case.update({"exact_primal":primal,"exact_dual_upper_bound":beta if dual else None,
                         "normalized_gap":dot(objective,values) if primal else None,
                         "dual_nonzero_multipliers":[(j,x) for j,x in enumerate(mu) if x] if dual else None})
            report["cases"].append(case)
            if primal:
                value=dot(objective,values);best=value if best is None else max(best,value)
                if value>0:
                    clones=integer_clones(values);instance=instance_from_clones(p,m,clones)
                    cert=StrategyCertificate(actions,cone.root)
                    verify_certificate(instance,cert).assert_valid()
                    audit=unit_check(instance,cert)
                    Vs=[dot(v,clones) for v in V]
                    W=instance.welfare(cone.root);OPT=instance.optimal_welfare()
                    assert OPT==dot(O,clones) and OPT-W>sum(Vs)
                    report.update({"status":"exact_ROW_counterexample","instance":instance.to_dict(),
                                   "strategy":cert.to_dict(),"unit_audit":audit,"J":J,
                                   "actual_position":i+1,"V_iT":Vs,"V_sum":sum(Vs),
                                   "W":W,"OPT":OPT,"net_gap":OPT-W,
                                   "strict_ROW_gap":OPT-W-sum(Vs),
                                   "MG_slack":m*min(audit["payoffs"])-(OPT-W),
                                   "half_slack":2*W-OPT})
                    finish(report,checked_duals,failed_duals,best)
                    return
    report["status"]="no_positive_ROW_point_found_in_this_fixed_cone"
    finish(report,checked_duals,failed_duals,best)


def finish(report,checked,failed,best):
    report.update({"lp_cases":len(report["cases"]),"checked_exact_duals":checked,
                   "failed_exact_duals":failed,"maximum_exact_primal_gap":best})
    (HERE/"row_attack.json").write_text(json.dumps(serial(report),indent=2)+"\n")
    print(json.dumps(serial({k:v for k,v in report.items() if k not in ("cases","instance","strategy")}),indent=2),flush=True)


if __name__=="__main__":main()
