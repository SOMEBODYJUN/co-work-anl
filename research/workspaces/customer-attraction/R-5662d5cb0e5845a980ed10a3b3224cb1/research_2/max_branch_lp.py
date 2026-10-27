"""Independent true branches including a maximum-cardinality root action.

Compared with branch_family_lp, every column retains a shared largest-theme
membership bit M. All CAP rows are |M|-|H|, not an unpriced size relaxation.
This is a sufficient certificate LP; an optimum above two is not a game.
"""
from itertools import product
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog

_cert_path=Path(__file__).with_name('root_lines_certificate_v2.json')
ROOT_LINES=json.loads(_cert_path.read_text())['lines'] if _cert_path.exists() else []

def qf(n,d): return F(n,d) if n else F(0)
def menus(pre,x,y,ell,d,n):
    den=pre+x+y
    return [n*qf(x,den)-F(d,pre+1)+F(d*ell,n*(pre+1)*(pre+2)),n*qf(y,den)-F(ell,pre+x+1)]
def base_rows(bits,d,ell):
    n=len(bits)-1;act=bits[:n];m=bits[-1];z=sum(act);u=[qf(a,z) for a in act]
    names=['Mactual','Zactual'];vals=menus(sum(act[:-2]),act[-2],act[-1],ell,d,n)
    for i in range(n):
        denom=n-i+sum(act[:i])
        for j,t in enumerate(bits):
            names.append(f'floor:{i+1}:{j+1}');vals.append(u[i]-F(t,denom))
        names.append(f'optfloor:{i+1}');vals.append(n*u[i]-F(d,denom))
    for j,t in enumerate(act):names.append(f'CAP:{j+1}');vals.append(F(m-t))
    for j,line in enumerate(ROOT_LINES):
        names.append(f'rootline:{j}');vals.append(F(line['B'])*u[0]+F(line['C'])*m-int(d>0))
    return names,vals
def branch_rows(bits,spec,hidden,d,ell):
    n=len(bits)-1;act=bits[:n];m=bits[-1];source,query=spec;z=sum(act)
    au=[qf(a,z) for a in act];branch=(bits[query],)+hidden
    old=act[:source];pre=sum(old);term=old+branch;bz=sum(term);pay=[qf(a,bz) for a in branch]
    labels=bits+hidden
    names=['IC','M','Z'];vals=[au[source]-pay[0]]+menus(sum(term[:-2]),term[-2],term[-1],ell,d,n)
    for i in range(n):
        denom=n-i+sum(act[:i])
        for j,t in enumerate(hidden):
            names.append(f'actual:{i+1}:hidden:{j+1}');vals.append(au[i]-F(t,denom))
    for j,t in enumerate(hidden):names.append(f'CAP:hidden:{j+1}');vals.append(F(m-t))
    for k in range(1,len(branch)):
        denom=n-source-k+pre+sum(branch[:k])
        for j,t in enumerate(labels):
            names.append(f'internal:{k+1}:{j+1}');vals.append(pay[k]-F(t,denom))
        names.append(f'internalopt:{k+1}');vals.append(n*pay[k]-F(d,denom))
    return names,vals
def solve(n=6,specs=None):
    specs=[(0,n),(n-4,n-1),(n-3,n-1)] if specs is None else specs
    bitslist=list(product(range(2),repeat=n+1));cells=list(product(bitslist,(0,1,n)));nc=len(cells)
    base_names,_=base_rows(bitslist[0],0,0)
    bn={s:branch_rows(bitslist[0],s,(0,)*(n-s[0]-1),0,0)[0] for s in specs}
    off={};nv=len(base_names)
    for s in specs:off[s]=nv;nv+=len(bn[s])
    first_t=nv;toff={}
    for s in specs:toff[s]=nv;nv+=nc
    beta=nv;nv+=1;rr=[];cc=[];vv=[];rhs=[]
    def add(vals,limit):
        row=len(rhs);rhs.append(float(limit))
        for col,val in vals:
            if val:rr.append(row);cc.append(col);vv.append(float(val))
    for ci,(bits,d) in enumerate(cells):
        for ell in (0,n):
            _,vals=base_rows(bits,d,ell)
            add(list(enumerate(vals))+[(toff[s]+ci,1) for s in specs]+[(beta,-int(sum(bits[:n])>0))],-int(d>0))
        for s in specs:
            for hidden in product(range(2),repeat=n-s[0]-1):
                for ell in (0,n):
                    _,vals=branch_rows(bits,s,hidden,d,ell)
                    add([(off[s]+j,v) for j,v in enumerate(vals)]+[(toff[s]+ci,-1)],0)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nv)).tocsc();obj=np.zeros(nv);obj[beta]=1
    bounds=[(0,None)]*first_t+[(None,None)]*(nv-first_t-1)+[(0,None)]
    lp=linprog(obj,A_ub=mat,b_ub=rhs,bounds=bounds,method='highs')
    out={'n':n,'specs':specs,'states':len(rhs),'variables':nv,'status':lp.message}
    if lp.success:
        out.update(beta=lp.x[-1],active_base={key:float(v) for key,v in zip(base_names,lp.x) if v>1e-8},active_branches={str(s):{key:float(lp.x[off[s]+j]) for j,key in enumerate(bn[s]) if lp.x[off[s]+j]>1e-8} for s in specs})
    return out
if __name__=='__main__':print(json.dumps(solve(),indent=2))
