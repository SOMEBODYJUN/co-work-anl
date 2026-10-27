"""All true actual-last-theme deviations, independently projected branches.

Experimental sufficient customerwise certificate LP. The forced source action
is actual final B; all followers are those of the same original SPE. Each
branch is allowed its full true last-two six-comparison menu. Common actual
membership identities are preserved, hidden membership is independently
maximized per branch (a relaxation of actual games).
"""
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog

def qf(n,d): return F(n,d) if n else F(0)
def menu(pre,x,y,ell,d,n):
    den=pre+x+y
    return n*qf(x,den)+qf(y,2*den)-F(d,pre+1)-F(ell,2*n*(pre+x+1))+F(d*ell,n*(pre+1)*(pre+2))
def menus(pre,x,y,ell,d,n):
    den=pre+x+y
    return [n*qf(x,den)-F(d,pre+1)+F(d*ell,n*(pre+1)*(pre+2)), n*qf(y,den)-F(ell,pre+x+1)]

def base_rows(act,d,ell):
    n=len(act);z=sum(act);u=[qf(a,z) for a in act]
    names=['Mactual','Zactual']; vals=menus(sum(act[:-2]),act[-2],act[-1],ell,d,n)
    for i in range(n):
        denom=n-i+sum(act[:i])
        for j,t in enumerate(act):
            names.append(f'floor:{i+1}:{j+1}');vals.append(u[i]-F(t,denom))
        names.append(f'optfloor:{i+1}');vals.append(n*u[i]-F(d,denom))
        names.append(f'Kfloor:{i+1}');vals.append(n*u[i])
    for j,t in enumerate(act):
        names.append(f'CAP:{j+1}');vals.append(-F(t))
    return names,vals

def branch_rows(act,source,hidden,d,ell):
    n=len(act);z=sum(act); au=[qf(a,z) for a in act]
    branch=(act[-1],)+hidden;old=act[:source];pre=sum(old)
    term=old+branch;bz=sum(term);pay=[qf(a,bz) for a in branch]
    labels=act+hidden
    names=['IC','M','Z'];vals=[au[source]-pay[0]]+menus(sum(term[:-2]),term[-2],term[-1],ell,d,n)
    for i in range(n):
        denom=n-i+sum(act[:i])
        for j,t in enumerate(hidden):
            names.append(f'actual:{i+1}:hidden:{j+1}');vals.append(au[i]-F(t,denom))
    for j,t in enumerate(hidden):
        names.append(f'CAP:hidden:{j+1}');vals.append(-F(t))
    for k in range(1,len(branch)):
        denom=n-source-k+pre+sum(branch[:k])
        for j,t in enumerate(labels):
            names.append(f'internal:{k+1}:{j+1}');vals.append(pay[k]-F(t,denom))
        names.append(f'internalopt:{k+1}');vals.append(n*pay[k]-F(d,denom))
    return names,vals

def solve(n=6,sources=None):
    sources=list(range(n-2)) if sources is None else sources
    actuals=list(product(range(2),repeat=n));ds=(0,1,n)
    cells=list(product(actuals,ds));nc=len(cells)
    base_names,_=base_rows(actuals[0],0,0)
    branch_names={s:branch_rows(actuals[0],s,(0,)*(n-s-1),0,0)[0] for s in sources}
    off={};nv=len(base_names)
    for s in sources:off[s]=nv;nv+=len(branch_names[s])
    toff={}
    for s in sources:toff[s]=nv;nv+=nc
    beta=nv;nv+=1
    rr=[];cc=[];vv=[];rhs=[]
    def add(vals,limit):
        row=len(rhs);rhs.append(float(limit))
        for col,val in vals:
            if val:rr.append(row);cc.append(col);vv.append(float(val))
    for ci,(act,d) in enumerate(cells):
        for ell in (0,n):
            _,vals=base_rows(act,d,ell)
            add(list(enumerate(vals))+[(toff[s]+ci,1) for s in sources]+[(beta,-int(sum(act)>0))],-int(d>0))
        for s in sources:
            for hidden in product(range(2),repeat=n-s-1):
                for ell in (0,n):
                    _,vals=branch_rows(act,s,hidden,d,ell)
                    add([(off[s]+j,v) for j,v in enumerate(vals)]+[(toff[s]+ci,-1)],0)
    kvals=[]
    for j,name in enumerate(base_names):
        if name.startswith('Kfloor:'):kvals.append((j,-1))
        if name.startswith('CAP:'):kvals.append((j,1))
    for s in sources:
        for j,name in enumerate(branch_names[s]):
            if name.startswith('CAP:'):kvals.append((off[s]+j,1))
    add(kvals,0)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nv)).tocsc()
    obj=np.zeros(nv);obj[beta]=1
    bounds=[(0,None)]*toff[sources[0]]+[(None,None)]*(nv-toff[sources[0]]-1)+[(0,None)]
    lp=linprog(obj,A_ub=mat,b_ub=rhs,bounds=bounds,method='highs')
    out={'n':n,'sources':[s+1 for s in sources],'states':len(rhs),'variables':nv,'status':lp.message}
    if lp.success:
        out.update(beta=lp.x[-1],active_base={key:float(v) for key,v in zip(base_names,lp.x) if v>1e-8},active_branches={s+1:{key:float(lp.x[off[s]+j]) for j,key in enumerate(branch_names[s]) if lp.x[off[s]+j]>1e-8} for s in sources})
    return out

if __name__=='__main__':
    print(json.dumps(solve(),indent=2))
