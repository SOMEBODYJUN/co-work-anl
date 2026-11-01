"""Candidate search only: symmetric signed quadratic fresh games.

Full ordered-history policies and theta witnesses are jointly chosen. A positive
floating answer must be rationally reconstructed and independently verified.
This auxiliary game is not the CAG half-coverage claim.
"""
from __future__ import annotations
import argparse, itertools, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


def run(p, m, seconds):
    edges = list(itertools.combinations(range(p), 2))
    eidx = {e:p+i for i,e in enumerate(edges)}
    n = p+len(edges)
    nodes = [h for d in range(m) for h in itertools.permutations(range(p), d)]
    v = {}; z = {}; witness = {}; nv=n
    for h in nodes:
        for a in range(p): v[h,a]=nv;nv+=1
        for a in range(p):
            if a not in h: z[h,a]=nv;nv+=1
    for H in itertools.combinations(range(p),m-1):
        for a in range(p):
            if a not in H: witness[H,a]=nv;nv+=1
    theta=nv;nv+=1
    lower=np.full(nv,-m-1.,dtype=float);upper=np.full(nv,m+1.,dtype=float)
    lower[:n]=-1.;upper[:n]=1.
    integer=np.zeros(nv,dtype=np.uint8)
    for j in list(z.values())+list(witness.values()):
        lower[j]=0;upper[j]=1;integer[j]=1
    lower[z[(),0]]=upper[z[(),0]]=1
    ri=[];ci=[];data=[];lbs=[];ubs=[]
    def add(row,lb=-np.inf,ub=np.inf):
        i=len(lbs)
        for j,x in row.items():
            if x:ri.append(i);ci.append(j);data.append(float(x))
        lbs.append(lb);ubs.append(ub)
    def terminal(a,H):
        row={a:1}
        for b in H:
            if b!=a:row[eidx[tuple(sorted((a,b)))]]=1
        return row
    def value(h,a):
        return {v[h,a]:1} if len(h)<m else terminal(a,h)
    def diff(left,right):
        row=dict(left)
        for j,x in right.items():row[j]=row.get(j,0)-x
        return row
    big=2*(m+1)
    for h in nodes:
        acts=[a for a in range(p) if a not in h]
        add({z[h,a]:1 for a in acts},1,1)
        for a in acts:
            for t in range(p):
                row=diff(value(h,t),value(h+(a,),t))
                row[z[h,a]]=big;add(row,ub=big)
                row=diff(value(h,t),value(h+(a,),t))
                row[z[h,a]]=-big;add(row,lb=-big)
            for b in acts:
                if a==b:continue
                row=diff(value(h,a),value(h+(b,),b))
                row[z[h,a]]=-big;add(row,lb=-big)
    for H in itertools.combinations(range(p),m-1):
        acts=[a for a in range(p) if a not in H]
        add({witness[H,a]:1 for a in acts},1,1)
        for a in acts:
            row=terminal(a,H);row[theta]=-1;row[witness[H,a]]=-big
            add(row,lb=-big)
    obj=np.zeros(nv);obj[theta]=-1;obj[v[(),0]]=1
    A=coo_matrix((data,(ri,ci)),shape=(len(lbs),nv)).tocsc()
    started=time.monotonic()
    sol=milp(obj,integrality=integer,bounds=Bounds(lower,upper),
             constraints=LinearConstraint(A,np.array(lbs),np.array(ubs)),
             options={'time_limit':seconds,'mip_rel_gap':0.})
    report={'scope':'finite auxiliary full ordered-history signed fresh quadratic search',
            'p':p,'m':m,'seconds':time.monotonic()-started,'status':int(sol.status),
            'message':sol.message,'variables':nv,'rows':len(lbs),
            'objective':None if sol.fun is None else -float(sol.fun),
            'universal_result':False}
    if sol.x is not None:
        report['coefficients']=sol.x[:n].tolist()
        report['theta_lower']=float(sol.x[theta]);report['root_payoff']=float(sol.x[v[(),0]])
        report['policy']={','.join(map(str,h)):max((a for a in range(p) if a not in h),key=lambda a:sol.x[z[h,a]]) for h in nodes}
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=5);ap.add_argument('--m',type=int,default=3)
    ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();report=run(args.p,args.m,args.seconds)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('coefficients','policy')}))
