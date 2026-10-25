"""Finite CAG attack: individual fullslot floor with three players left.

The two fixed background slots need only be legal, so a positive result would
reject the stronger arbitrary-background floor, not the actual-position floor.
All ordered three-tail histories and true continuations are retained.
"""
import argparse, itertools, json, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=4);ap.add_argument('--background',default='0,1');ap.add_argument('--time',type=float,default=60);ap.add_argument('--out',required=True);args=ap.parse_args()
k=args.k;n=3;bg=tuple(int(a) for a in args.background.split(',') if a!='');types=list(range(1,1<<k));p=np.ones(k)/k
inc=np.array([[(t>>a)&1 for t in types]for a in range(k)],float)
hist=[h for d in range(n+1)for h in itertools.product(range(k),repeat=d)]
idx={};keys=[];lb=[];ub=[];ints=[]
def var(key,lo=0,hi=1,integer=0):
    idx[key]=len(keys);keys.append(key);lb.append(lo);ub.append(hi);ints.append(integer)
for t in types:var(('w',t))
for h in hist:
    var(('Q',h))
    for j in range(len(h)):var(('U',h,j))
    if len(h)<n:
        var(('V',h))
        for a in range(k):var(('Y',h,a),integer=1)
var(('R',))
rows=[];rlo=[];rhi=[]
def row(r,lo=-np.inf,hi=np.inf):rows.append(r);rlo.append(lo);rhi.append(hi)
def eq(r,v=0):row(r,v,v)
eq({idx[('w',t)]:1 for t in types},1)
for h in hist:
    d=len(h)
    if d==n:
        load=np.bincount(bg+h,minlength=k)@inc
        r={idx[('Q',h)]:1}
        for ti,t in enumerate(types):r[idx[('w',t)]]=-(p@inc[:,ti])/(1+load[ti])
        eq(r)
        for j in range(n):
            r={idx[('U',h,j)]:1}
            for ti,t in enumerate(types):
                if inc[h[j],ti]:r[idx[('w',t)]]=-1/load[ti]
            eq(r)
    else:
        eq({idx[('Y',h,a)]:1 for a in range(k)},1)
        for a in range(k):
            child=h+(a,);y=idx[('Y',h,a)]
            row({idx[('V',h)]:1,idx[('U',child,d)]:-1},lo=0)
            row({idx[('V',h)]:1,idx[('U',child,d)]:-1,y:1},hi=1)
            carry=[(('Q',h),('Q',child))]+[(('U',h,j),('U',child,j))for j in range(d)]
            for ka,kb in carry:
                row({idx[ka]:1,idx[kb]:-1,y:1},hi=1)
                row({idx[kb]:1,idx[ka]:-1,y:1},hi=1)
for a in range(k):row({idx[('R',)]:1,idx[('Q',(a,))]:-1},hi=0)
c=np.zeros(len(keys));c[idx[('R',)]]=-1;c[idx[('V',())]]=1
A=lil_matrix((len(rows),len(keys)))
for i,r in enumerate(rows):
    for j,v in r.items():A[i,j]=v
start=time.time()
res=milp(c,integrality=np.array(ints),bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),rlo,rhi),options={'time_limit':args.time,'mip_rel_gap':1e-8})
out={'k':k,'remaining':n,'background':bg,'p':p.tolist(),'status':int(res.status),'message':res.message,'gap_float':None if res.fun is None else float(-res.fun),'dual_bound':getattr(res,'mip_dual_bound',None),'seconds':time.time()-start}
if res.x is not None:
    out['w']=[float(res.x[idx[('w',t)]])for t in types]
    out['sigma']=[[list(h),int(np.argmax([res.x[idx[('Y',h,a)]]for a in range(k)]))]for h in hist if len(h)<n]
open(args.out,'w').write(json.dumps(out,indent=2)+'\n')
print(json.dumps({a:v for a,v in out.items()if a not in {'w','sigma'}},indent=2))
