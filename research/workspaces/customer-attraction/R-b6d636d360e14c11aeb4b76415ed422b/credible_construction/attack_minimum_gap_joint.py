"""Exact-target candidate generator adapted from canonical joint MILP.
Only the objective changes to OPT-W-m u_test. Floating bounds are not proofs.
"""
from __future__ import annotations
from itertools import product
from fractions import Fraction
from pathlib import Path
import sys,time,json
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from tests.audits.customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row
from customer_attraction import StrategyCertificate
from attack_minimum_gap import scan,serial

def joint_candidate(p,path,portfolio,time_limit,tested_topic):
    m=len(path);n=(1<<p)-1
    nodes=tuple(h for d in range(m) for h in product(range(p),repeat=d))
    u_index={};z_index={};next_index=n
    for h in nodes:
        for a in range(p):u_index[h,a]=next_index;next_index+=1
    for h in nodes:
        for a in range(p):z_index[h,a]=next_index;next_index+=1
    count=next_index;lo=np.zeros(count);hi=np.full(count,m,dtype=float);integ=np.zeros(count,dtype=np.uint8)
    hi[:n]=m
    for idx in z_index.values():hi[idx]=1;integ[idx]=1
    for d,a in enumerate(path):lo[z_index[path[:d],a]]=hi[z_index[path[:d],a]]=1
    # Root follows path[0]; its actual payoff is at most normalized welfare1.
    hi[u_index[(),path[0]]]=1
    matrix_i=[];matrix_j=[];matrix_x=[];lower=[];upper=[]
    def add(row,lb=-np.inf,ub=np.inf):
        idx=len(lower)
        for j,x in row.items():
            if x:matrix_i.append(idx);matrix_j.append(j);matrix_x.append(float(x))
        lower.append(lb);upper.append(ub)
    def child_expr(h,t):
        if len(h)<m:return {u_index[h,t]:1}
        q=tuple(h.count(a) for a in range(p))
        # Absent actions have utility0; only actual occupied-action utilities
        # enter an incentive comparison.
        if not q[t]:return {}
        return {j:x for j,x in enumerate(payoff_row(p,q,t)) if x}
    def difference(h,t,child,ct):
        out={u_index[h,t]:1}
        for j,x in child_expr(child,ct).items():out[j]=out.get(j,0)-x
        return out
    rootq=tuple(path.count(a) for a in range(p));w=coverage_row(p,(a for a,x in enumerate(rootq) if x))
    add({j:x for j,x in enumerate(w) if x},1,1)
    add({j:1 for j in range(n)},ub=m*p)
    # Root SPE guarantees every topic total s_a <= m*u_root. This also
    # justifies every utility in [0,m] and conditional big-M exactly m.
    for a in range(p):
        row={j:1 for j in range(n) if (j+1)&(1<<a)};row[u_index[(),path[0]]]=-m
        add(row,ub=0)
    add({u_index[(),a]:q for a,q in enumerate(rootq) if q},1,1)
    for h in nodes:
        add({z_index[h,a]:1 for a in range(p)},1,1)
        for a in range(p):
            z=z_index[h,a]
            for t in range(p):
                row=difference(h,t,h+(a,),t);row[z]=m
                add(row,ub=m)
                row=difference(h,t,h+(a,),t);row[z]=-m
                add(row,lb=-m)
            for b in range(p):
                if b==a:continue
                row=difference(h,a,h+(b,),b);row[z]=-m
                add(row,lb=-m)
    A=coo_matrix((matrix_x,(matrix_i,matrix_j)),shape=(len(lower),count)).tocsc()
    objective=np.zeros(count);objective[:n]=-np.array(tuple(v-w-m*u for v,w,u in zip(coverage_row(p,portfolio),w,payoff_row(p,rootq,tested_topic))),dtype=float)
    started=time.monotonic()
    result=milp(objective,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lower),np.array(upper)),
                options={'time_limit':time_limit,'mip_rel_gap':0.0,'presolve':True})
    metadata={'status':int(result.status),'message':result.message,'variables':count,
              'binary_actions':len(z_index),'inequalities_and_equalities':len(lower),
              'seconds':time.monotonic()-started,'floating_objective':float(-result.fun) if result.fun is not None else None,
              'floating_mip_gap':float(result.mip_gap) if hasattr(result,'mip_gap') else None,
              'floating_bound_not_a_certificate':True}
    if result.x is None:return None,metadata
    actions={h:max(range(p),key=lambda a:result.x[z_index[h,a]]) for h in nodes}
    cone=StrategyCone(p,m,actions)
    if cone.root!=rootq:raise AssertionError('MILP action extraction does not realize root path')
    return cone,metadata


def main():
    cases=[(4,(0,1,1),(1,2,3),0),(4,(0,1,1),(0,2,3),0),
           (4,(0,1,2),(1,2,3),0),(4,(0,1,2),(0,2,3),0)]
    reports=[]
    for p,path,J,a in cases:
        cone,meta=joint_candidate(p,path,J,25,a)
        r={"topics":p,"path":path,"portfolio":J,"tested_topic":a,"milp":meta}
        if cone is not None:
            r["strategy"]=StrategyCertificate(cone.actions,cone.root).to_dict()
            r["exact_scan"]=scan(cone,"targeted_joint_milp")
        reports.append(r)
        Path(__file__).with_name("minimum_gap_joint.json").write_text(json.dumps(serial(reports),indent=2)+"\n")
        print(serial({k:v for k,v in r.items() if k not in ("exact_scan","strategy")}),flush=True)
        if cone is not None:
            print(serial({k:v for k,v in r["exact_scan"].items() if k not in ("instance","strategy","duals")}),flush=True)
        if cone is not None and r["exact_scan"]["status"]=="exact_counterexample":break

if __name__=="__main__":main()
