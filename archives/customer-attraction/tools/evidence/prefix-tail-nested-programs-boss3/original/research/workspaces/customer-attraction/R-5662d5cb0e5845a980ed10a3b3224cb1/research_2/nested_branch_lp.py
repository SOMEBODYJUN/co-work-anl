"""True B-then-A nested deviations at actual positions three and four.

Each outer B branch retains its first follower's exact IC to the actual A,
with the new child continuation kept as separate named topics. For the
fourth-position B branch, A is a penultimate query, so its true last reply is
also inserted in the common six-optimal-theme reply menu as a seventh theme.
This is a discovery LP, never a game counterexample.
"""
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from max_branch_lp import qf,menus,base_rows,branch_rows

def nested_rows(bits,source,hidden,d,ell,ellchild=0,query_kind='A'):
    n=len(bits)-1;act=bits[:n];m=bits[-1];a,b=act[-2:]
    old=act[:source];pa=n-source-1
    hp,hc=hidden[:pa],hidden[pa:]
    query=a if query_kind=='A' else hp[-1]
    pseq=old+(b,)+hp;cseq=old+(b,query)+hc
    assert len(pseq)==len(cseq)==n
    pden=sum(pseq);cden=sum(cseq)
    pp=[qf(t,pden) for t in pseq];cp=[qf(t,cden) for t in cseq]
    au=[qf(t,sum(act)) for t in act];labels=bits+hidden
    names=['outer-IC','inner-IC','parent:M','parent:Z']
    vals=[au[source]-pp[source],pp[source+1]-cp[source+1]]+menus(sum(pseq[:-2]),pseq[-2],pseq[-1],ell,d,n)
    if source<=n-4:
        names+=['child:M','child:Z'];vals+=menus(sum(cseq[:-2]),cseq[-2],cseq[-1],ellchild,d,n)
    if source==n-3:
        pre=sum(pseq[:-2]);q,r=pseq[-2:];y=cseq[-1];den=pre+q+r
        for count,dd,ll in [(n+1,d+query,ell+y),(n+2,d+query+q,ell+y+r)]:
            names += [f'extended:{count}:M',f'extended:{count}:Z']
            vals += [count*qf(q,den)-F(dd,pre+1)+F(dd*ll,count*(pre+1)*(pre+2)), count*qf(r,den)-F(ll,pre+q+1)]
    for i in range(n):
        denom=n-i+sum(act[:i])
        for j,t in enumerate(hidden):
            names.append(f'actual:{i+1}:hidden:{j+1}');vals.append(au[i]-F(t,denom))
    for j,t in enumerate(hidden):names.append(f'CAP:hidden:{j+1}');vals.append(F(m-t))
    for lab,seq,pay,start in [('parent',pseq,pp,source+1),('child',cseq,cp,source+2)]:
        for pos in range(start,n):
            denom=n-pos+sum(seq[:pos])
            for j,t in enumerate(labels):
                names.append(f'{lab}:floor:{pos+1}:{j+1}');vals.append(pay[pos]-F(t,denom))
            names.append(f'{lab}:optfloor:{pos+1}');vals.append(n*pay[pos]-F(d,denom))
    return names,vals

def solve(n=6,nested_sources=None,query_kind='A'):
    nested_sources=[n-4,n-3] if nested_sources is None else list(nested_sources)
    specs=[('max',0)]+[('nested',source) for source in nested_sources]
    bitslist=list(product(range(2),repeat=n+1));cells=list(product(bitslist,(0,1,n)));nc=len(cells)
    base_names,_=base_rows(bitslist[0],0,0)
    def size(spec):return n-1 if spec[0]=='max' else 2*n-2*spec[1]-3
    def local(spec,bits,hidden,d,ell,childell):
        if spec[0]=='max':return branch_rows(bits,(0,n),hidden,d,ell)
        return nested_rows(bits,spec[1],hidden,d,ell,childell,query_kind)
    bn={s:local(s,bitslist[0],(0,)*size(s),0,0,0)[0] for s in specs}
    off={};nv=len(base_names)
    for s in specs:off[s]=nv;nv+=len(bn[s])
    first_t=nv;toff={}
    for s in specs:toff[s]=nv;nv+=nc
    beta=nv;nv+=1;rr=[];cc=[];vv=[];rhs=[]
    def add(vals,lim):
        row=len(rhs);rhs.append(float(lim))
        for col,val in vals:
            if val:rr.append(row);cc.append(col);vv.append(float(val))
    for ci,(bits,d) in enumerate(cells):
        for ell in (0,n):
            _,vals=base_rows(bits,d,ell)
            add(list(enumerate(vals))+[(toff[s]+ci,1) for s in specs]+[(beta,-int(sum(bits[:n])>0))],-int(d>0))
        for s in specs:
            childells=(0,n) if s[0]=='nested' and s[1]<=n-4 else (0,)
            for hidden in product(range(2),repeat=size(s)):
                for ell,childell in product((0,n),childells):
                    _,vals=local(s,bits,hidden,d,ell,childell)
                    add([(off[s]+j,v) for j,v in enumerate(vals)]+[(toff[s]+ci,-1)],0)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nv)).tocsc();obj=np.zeros(nv);obj[beta]=1
    bounds=[(0,None)]*first_t+[(None,None)]*(nv-first_t-1)+[(0,None)]
    lp=linprog(obj,A_ub=mat,b_ub=rhs,bounds=bounds,method='highs')
    out={'n':n,'query_kind':query_kind,'states':len(rhs),'variables':nv,'status':lp.message}
    if lp.success:out.update(beta=lp.x[-1],active_base={key:float(v) for key,v in zip(base_names,lp.x) if v>1e-8},active_branches={str(s):{key:float(lp.x[off[s]+j]) for j,key in enumerate(bn[s]) if lp.x[off[s]+j]>1e-8} for s in specs})
    return out
if __name__=='__main__':print(json.dumps(solve(),indent=2))
