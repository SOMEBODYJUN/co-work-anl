"""Full-policy MILP attack on quadratic fresh theta-floor, m=3.
No result of infeasibility is a general proof. A feasible numerical output must be
rationalized and independently replayed before it can be called a counterexample.
"""
import argparse, itertools, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=6);ap.add_argument('--bound',type=float,default=20);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
p=args.p;A=range(p);E=list(itertools.combinations(A,2));d=p+len(E);ei={e:p+i for i,e in enumerate(E)}
vars=[];lb=[];ub=[];integer=[]
def var(name,l,u,i=0):
    q=len(vars);vars.append(name);lb.append(l);ub.append(u);integer.append(i);return q
for i in range(d):var('x'+str(i),-args.bound,args.bound)
M=20*args.bound+20
X={(a,b):var('X'+str((a,b)),-3*args.bound,3*args.bound) for a in A for b in A if a!=b}
Y={(a,b):var('Y'+str((a,b)),-3*args.bound,3*args.bound) for a,b in X}
Z={(a,b,c):var('z'+str((a,b,c)),0,1,1) for a,b in X for c in A if c not in (a,b)}
B={(a,b):var('b'+str((a,b)),0,1,1) for a,b in X}
R={a:var('R'+str(a),-3*args.bound,3*args.bound) for a in A}
L=var('L',-3*args.bound,3*args.bound)
T={(h,a):var('t'+str((h,a)),0,1,1) for h in E for a in A if a not in h}
rows=[];lower=[];upper=[]
def row(co,lo=-np.inf,hi=np.inf):rows.append(co);lower.append(lo);upper.append(hi)
def coeff(a,S):
    co={a:1}
    for b in S:
        if b!=a:co[ei[tuple(sorted((a,b)))]]=1
    return co

def add(*terms):
    co={}
    for v,fac in terms:
        for j,q in v.items():co[j]=co.get(j,0)+fac*q
    return {j:q for j,q in co.items() if q}
for a,b in X:
    cs=[c for c in A if c not in (a,b)]
    row({Z[a,b,c]:1 for c in cs},1,1)
    for c in cs:
        z=Z[a,b,c]
        for e in cs:
            # c chosen => v_c >= v_e
            co=add((coeff(c,(a,b,c)),1),(coeff(e,(a,b,e)),-1),({z:-M},1))
            row(co,lo=-M)
        for q,v in [(X[a,b],coeff(a,(a,b,c))),(Y[a,b],coeff(b,(a,b,c)))]:
            co=add(({q:1},1),(v,-1),({z:M},1));row(co,hi=M)
            co=add(({q:1},1),(v,-1),({z:-M},1));row(co,lo=-M)
for a in A:
    bs=[b for b in A if b!=a]
    row({B[a,b]:1 for b in bs},1,1)
    for b in bs:
        z=B[a,b]
        for e in bs:row({Y[a,b]:1,Y[a,e]:-1,z:-M},lo=-M) if e!=b else None
        row({R[a]:1,X[a,b]:-1,z:M},hi=M)
        row({R[a]:1,X[a,b]:-1,z:-M},lo=-M)
    row({L:1,R[a]:-1},lo=0)
row({L:1,R[0]:-1},0,0)
for h in E:
    es=[e for e in A if e not in h]
    row({T[h,e]:1 for e in es},1,1)
    for e in es:
        # t chosen => marginal - L >= 1
        co=add((coeff(e,h+(e,)),1),({L:-1,T[h,e]:-M},1));row(co,lo=1-M)
ii=[];jj=[];vv=[]
for i,co in enumerate(rows):
    for j,v in co.items():ii.append(i);jj.append(j);vv.append(v)
mat=coo_matrix((vv,(ii,jj)),shape=(len(rows),len(vars))).tocsr()
start=time.time();res=milp(np.zeros(len(vars)),integrality=np.array(integer),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat,lower,upper),options={'time_limit':args.seconds,'mip_rel_gap':0})
report={'object':'full ordered-history quadratic fresh m=3 thetafloor MILP attack','p':p,'m':3,'coefficient_bound':args.bound,'gap_target':1,'variable_count':len(vars),'constraint_count':len(rows),'status':res.status,'message':res.message,'seconds':time.time()-start,'success':res.success}
if res.x is not None:
    report['solution']={name:float(v) for name,v in zip(vars,res.x) if name.startswith('x') or name=='L' or (name.startswith(('z','b','t')) and v>0.5)}
args.output.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
