"""New terminal identities after fifth-player deviations; exploratory global LP.

The finite type domain is complete. Floating results are diagnostics until an
exact feasible point or dual certificate is reconstructed and verified.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,time
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba'
PREV=ROOT/'research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent'
sys.path[:0]=[str(OLD/'parent'),str(PREV)]
import joint_system as js
import fourth_indexed_projection as fp

PAT=fp.PATTERNS
NAMES=['source','terminal_own_B','terminal_own_C','terminal_own_T','terminal_opt_average']+['terminal_actual_'+str(i+1) for i in range(6)]+['terminal_B_average','terminal_C_average','reverse_terminal','price','capacity']
NF=len(NAMES)
NW=5+2*NF
PRICE=NF-2;CAP=NF-1;REVERSE=NF-3
WP=['old_'+str(i) for i in range(5)]+['new_'+fam+'_'+x for fam in ('B','C') for x in NAMES]

@lru_cache(maxsize=1)
def old_system():
    types,rows=js.build()
    original=json.loads((OLD/'parent/joint_system.json').read_text())
    for i,c in enumerate(original['menu_cuts']):rows.append(('same-menu-joint:'+str(i),js.from_weights(c['weights'])))
    for cut in original['pair_cuts']:rows.append(js.row(types,{k:v for k,v in cut.items() if k!='separation_slack'}))
    data=json.loads((PREV/'fourth_indexed_projection.json').read_text())
    lookup={(tuple(map(int,z['actual_bits'])),z['d']):F(z['coefficient']) for z in data['coefficients']}
    norm=F(data['scale']*data['integer_weights'][0])
    rows.append(('complete-indexed-actual-fourth',[lookup[t]/norm for t in types]+[F()]))
    assert len(rows)==702
    return types,rows

def share(n,d):return F(n,d) if n else F()

def row_parts(a,d,h):
    """Exact affine r=0 coefficient and independent-reply multiplicities.

    B-family excludes i=j; C-family includes every i,j. Each new reply identity
    is shared by the source IC, all its terminal comparisons, and its price.
    """
    p=sum(a[:3]);ell=sum(a[:5]);whole=sum(a)
    raw=[F(x,60) for x in fp.compact_rows(a,h)]+[F()]*(2*NF)
    zs={}
    nb=sum(n*b for n,(t,b,c) in zip(h,PAT));nc=sum(n*c for n,(t,b,c) in zip(h,PAT))
    for fam in range(2):
        off=5+fam*NF
        for ni,(t,b,c) in zip(h,PAT):
            if not ni:continue
            vb=share(b,p+t+b+c)
            for nj,(_,bj,cj) in zip(h,PAT):
                if not nj:continue
                count=ni*nj-(ni if fam==0 and (t,b,c)==(_,bj,cj) else 0)
                if not count:continue
                y=(bj,cj)[fam]
                den=p+t+y+1
                raw[off]+=count*(vb-share(y,p+t+y))
                for j,q in enumerate((b,c,t,F(d,6),*a,F(nb,6),F(nc,6)),1):raw[off+j]-=count*F(q,den)
                raw[off+REVERSE]+=count*share(c,p+t+b+c)
                raw[off+PRICE]+=count*share(a[5],whole)
                key=(fam,p,ell,t,b,y)
                zs[key]=zs.get(key,0)+count
    return raw,zs

def delta(key):
    fam,p,ell,t,b,y=key;off=5+fam*NF;den=p+t+y+1
    out={off:share(y,(p+t+y)*den)}
    out.update({off+j:F(1,den) for j in range(1,REVERSE)})
    out[off+REVERSE]=-F(1,p+t+b+1)
    out[off+PRICE]=-F(1,ell+1)
    out[off+CAP]=-F(1)
    return out

def projection(a,d,weights):
    p=sum(a[:3]);ell=sum(a[:5])
    z={key:max(F(),sum(weights[j]*v for j,v in delta(key).items())) for key in product(range(2),(p,),(ell,),range(2),range(2),range(2))}
    return max(sum(x*y for x,y in zip(row_parts(a,d,h)[0],weights))+sum(n*z[k] for k,n in row_parts(a,d,h)[1].items()) for h in fp.HISTS[d])

def build_lp():
    types,rows=old_system();nb=len(rows);nt=len(types)
    zkeys=sorted({(fam,sum(a[:3]),sum(a[:5]),t,b,y) for a,d in types for fam,t,b,y in product(range(2),range(2),range(2),range(2))})
    zi={k:nb+NW+i for i,k in enumerate(zkeys)}
    ng=nb+NW+len(zi);rho=ng+nt;nvar=rho+1
    rr=[];cc=[];vv=[];rhs=[]
    def add(items,b):
        i=len(rhs);rhs.append(float(b))
        for j,v in items:
            if v:rr.append(i);cc.append(j);vv.append(float(v))
    for k,(a,d) in enumerate(types):
        add([(j,c[k]) for j,(_,c) in enumerate(rows)]+[(ng+k,1),(rho,int(d>0))],int(any(a)))
    add([(j,c[-1]) for j,(_,c) in enumerate(rows)]+[(nb+5+CAP,30),(nb+5+NF+CAP,36)],0)
    for key,j in zi.items():add([(nb+k,v) for k,v in delta(key).items()]+[(j,-1)],0)
    print('building complete projection',len(types),len(zkeys),flush=True)
    # Raw rows depend on a through only p,ell, actual profit constants and
    # individual actual-query membership. All 448 types remain present.
    for k,(a,d) in enumerate(types):
        for h in fp.HISTS[d]:
            raw,zs=row_parts(a,d,h)
            add([(nb+j,v) for j,v in enumerate(raw)]+[(zi[key],count) for key,count in zs.items()]+[(ng+k,-1)],0)
        if k%64==0:print('built',k,'constraints',len(rhs),flush=True)
    A=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    obj=np.zeros(nvar);obj[rho]=-1
    bounds=[(0,None)]*ng+[(None,None)]*nt+[(0,None)]
    return types,rows,zkeys,A,np.array(rhs),obj,bounds,ng

def main():
    start=time.time();types,rows,zkeys,A,b,obj,bounds,ng=build_lp()
    print('LP',A.shape,'nnz',A.nnz,'build seconds',time.time()-start,flush=True)
    result=linprog(obj,A_ub=A,b_ub=b,bounds=bounds,method='highs',options={'time_limit':500})
    report={'scope':'floating full-type necessary-system budget diagnostic; not a proof or SPE','success':bool(result.success),'status':result.message,'matrix_shape':list(A.shape),'nnz':int(A.nnz),'seconds':time.time()-start}
    if result.x is not None:
        report['rho']=float(result.x[-1]);report['minimum_slack']=float(np.min(b-A@result.x))
        report['new_weights']={k:float(v) for k,v in zip(WP,result.x[len(rows):len(rows)+NW]) if abs(v)>1e-10}
        report['old_weights']={k:float(v) for (k,_),v in zip(rows,result.x[:len(rows)]) if abs(v)>1e-10}
        np.savez_compressed(HERE/'new_reply_budget_float.npz',x=result.x,marginals=result.ineqlin.marginals)
    (HERE/'new_reply_budget_float.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
