"""Restricted count-Markov full SPE joint MILP candidate generator.
All candidates must be unfolded and independently checked by exact strategy cone.
Numerical MILP statuses/bounds prove no game bound.
"""
from __future__ import annotations
import sys,time,json,argparse
from pathlib import Path
from itertools import product
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import StrategyCertificate
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,serializable
from cone_attack_credible_variants import exact_export

def counts(p,total):
    if p==1:yield (total,);return
    for i in range(total+1):
        for q in counts(p-1,total-i):yield (i,)+q

def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]

def candidate(p,path,J,seconds):
    m=len(path);n=(1<<p)-1
    nodes=tuple(q for d in range(m) for q in counts(p,d));u={};z={};idx=n
    for q in nodes:
        for a in range(p):u[q,a]=idx;idx+=1
    for q in nodes:
        for a in range(p):z[q,a]=idx;idx+=1
    lo=np.zeros(idx);hi=np.full(idx,m,dtype=float);integrality=np.zeros(idx,dtype=np.uint8)
    for j in z.values():hi[j]=1;integrality[j]=1
    q=(0,)*p
    for a in path:lo[z[q,a]]=hi[z[q,a]]=1;q=inc(q,a)
    rootq=q;root=(0,)*p;hi[u[root,path[0]]]=1
    rows=[];cols=[];data=[];lower=[];upper=[]
    def add(row,lb=-np.inf,ub=np.inf):
        i=len(lower)
        for j,x in row.items():
            if x:rows.append(i);cols.append(j);data.append(float(x))
        lower.append(lb);upper.append(ub)
    def expr(q,t):
        if sum(q)<m:return {u[q,t]:1}
        if not q[t]:return {}
        return {j:x for j,x in enumerate(payoff_row(p,q,t)) if x}
    def diff(q,t,child,ct):
        r={u[q,t]:1}
        for j,x in expr(child,ct).items():r[j]=r.get(j,0)-x
        return r
    w=coverage_row(p,[a for a,x in enumerate(rootq) if x])
    add({j:x for j,x in enumerate(w) if x},1,1)
    add({j:1 for j in range(n)},ub=m*p)
    for a in range(p):
        row={j:1 for j in range(n) if (j+1)&(1<<a)};row[u[root,path[0]]]=-m;add(row,ub=0)
    add({u[root,a]:x for a,x in enumerate(rootq) if x},1,1)
    for q in nodes:
        add({z[q,a]:1 for a in range(p)},1,1)
        for a in range(p):
            zz=z[q,a]
            for t in range(p):
                row=diff(q,t,inc(q,a),t);row[zz]=m;add(row,ub=m)
                row=diff(q,t,inc(q,a),t);row[zz]=-m;add(row,lb=-m)
            for b in range(p):
                if b==a:continue
                row=diff(q,a,inc(q,b),b);row[zz]=-m;add(row,lb=-m)
    matrix=coo_matrix((data,(rows,cols)),shape=(len(lower),idx)).tocsc()
    objective=np.zeros(idx);objective[:n]=-np.array(coverage_row(p,J),dtype=float)
    started=time.monotonic()
    out=milp(objective,integrality=integrality,bounds=Bounds(lo,hi),constraints=LinearConstraint(matrix,lower,upper),options={'time_limit':seconds,'mip_rel_gap':0.0,'presolve':True})
    meta={'p':p,'m':m,'path':path,'portfolio':J,'variables':idx,'binary':len(z),'rows':len(lower),'seconds':time.monotonic()-started,'status':int(out.status),'message':out.message,'floating_value':float(-out.fun) if out.fun is not None else None,'floating_bound_not_certificate':True}
    if out.x is None:return None,meta
    policy={q:max(range(p),key=lambda a:out.x[z[q,a]]) for q in nodes}
    actions={h:policy[tuple(h.count(a) for a in range(p))] for d in range(m) for h in product(range(p),repeat=d)}
    cone=StrategyCone(p,m,actions)
    if cone.root!=rootq:raise AssertionError('root path')
    return cone,meta

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--path',default='0,0,0,1,1');ap.add_argument('--portfolio',default='2,3,4,5,6');ap.add_argument('--seconds',type=float,default=40);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    path=tuple(map(int,args.path.split(',')));J=tuple(map(int,args.portfolio.split(',')))
    cone,meta=candidate(args.topics,path,J,args.seconds)
    report={'scope':'count-Markov strategies only, expanded to full ordered histories; numerical MILP bounds excluded','universal_bound_proved':False,'milp':meta,'batches':[]}
    if cone:
        result=cone.optimize(J)
        record={'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),'root_counts':cone.root,'portfolio_proofs':[]}
        if result['certified']:record['portfolio_proofs'].append(exact_export(cone,result))
        report['batches']=[{'players':len(path),'topics':args.topics,'cone_proofs':[record]}]
    args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
    print(json.dumps(serializable({'milp':meta,'exact_ratios':[q['ratio'] for b in report['batches'] for c in b['cone_proofs'] for q in c['portfolio_proofs']]})),flush=True)
if __name__=='__main__':main()
