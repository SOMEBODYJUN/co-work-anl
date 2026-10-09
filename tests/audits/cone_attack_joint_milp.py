"""Finite full-history joint strategy/multiplicity MILP candidate generator.

Big-M is justified by SPE root guarantees, not guessed. Floating MILP results
only generate complete action maps; each claimed ratio is then obtained by the
existing rational strategy-cone LP and checked with Fraction on the full tree.
No floating MILP upper bound is a mathematical certificate.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import product,combinations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from customer_attraction import StrategyCertificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row,serializable,payoff_row
from cone_attack_credible_variants import exact_export,verify


def joint_candidate(p,path,portfolio,time_limit):
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
    objective=np.zeros(count);objective[:n]=-np.array(coverage_row(p,portfolio),dtype=float)
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
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--topics',type=int,default=4)
    ap.add_argument('--path',action='append',default=[])
    ap.add_argument('--seconds',type=float,default=40)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--verify',type=Path)
    ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args()
    if args.verify:verify(args.verify);return
    if args.self_test:
        checked=0
        for m in (2,3):
            for path in product(range(2),repeat=m):
                cone,meta=joint_candidate(2,path,(0,1),10)
                if cone is None or meta['status']!=0:raise AssertionError((path,meta))
                result=cone.optimize((0,1))
                if not result['certified'] or not result['dual_optimal']:raise AssertionError('exact LP test')
                proof=exact_export(cone,result)
                expected=Fraction(m+1,m) if len(set(path))==1 else Fraction(1)
                if proof['ratio']!=expected:raise AssertionError((path,proof['ratio'],expected))
                checked+=1
        print(json.dumps({'two_topic_fixed_ordered_paths_checked':checked,'all_exact_primal_dual_ratios_match_independent_bound':True}))
        return
    if args.output and args.output.exists():raise FileExistsError(args.output)
    p=args.topics;paths=[tuple(map(int,s.split(','))) for s in args.path or ['0,0,0,0,1','0,0,1,1,1']]
    report={'scope':'MILP-generated full ordered-history SPE strategy cones; floating MIP bounds excluded',
            'universal_bound_proved':False,'batches':[],
            'base_git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for path in paths:
        m=len(path);portfolio=tuple(range(min(p,m)))
        cone,meta=joint_candidate(p,path,portfolio,args.seconds)
        batch={'players':m,'topics':p,'path':path,'milp':meta,'cone_proofs':[]}
        if cone is not None:
            record={'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),
                    'root_counts':cone.root,'portfolio_proofs':[]}
            for J in combinations(range(p),min(p,m)):
                result=cone.optimize(J)
                if result['certified']:record['portfolio_proofs'].append(exact_export(cone,result))
            batch['cone_proofs'].append(record)
        report['batches'].append(batch)
        print(json.dumps(serializable({'path':path,'milp':meta,'exact_ratios':[
            q['ratio'] for c in batch['cone_proofs'] for q in c['portfolio_proofs']]})),flush=True)
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
    if args.output:args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
if __name__=='__main__':main()
