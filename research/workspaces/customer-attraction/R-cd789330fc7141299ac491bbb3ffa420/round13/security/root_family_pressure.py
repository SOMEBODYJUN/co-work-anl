"""One named analytic relaxation: complete optimal root-query family, m=5.

Not a search over games. Every column is a customer membership type in a
relaxation of one actual path and its five true root-deviation branches.
All rows are legitimate aggregated original-SPE comparisons/profit bounds.
The pricing factorization is exact because rows are affine in each branch
histogram after actual membership and optimal multiplicity are fixed.
"""
from itertools import product
from math import comb
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
M=5
BETA={1:1.,2:1.5,3:5/3,4:1499/750}
BITS=list(product((0,1),repeat=4))

def rat(a,b): return a/b if a else 0.
def profit_count(p,c): return rat(c,p+c)
def subset_profit(p,c,k):
    return sum(comb(c,d)*comb(5-c,k-d)*profit_count(p,d)
               for d in range(max(0,k-(5-c)),min(c,k)+1))

def col(a,j,x,y):
    c=sum(a); w=float(c>0); o=float(j>0)
    u=np.array([rat(v,c) for v in a]); rows=[]; names=[]
    def put(n,z): names.append(n);rows.append(z)
    # All actual-node guaranteed payoff queries, including exact final BR.
    for i in range(5):
        p=sum(a[:i]); k=5-i
        for q in range(5):put(f'act:{i}:a{q}',u[i]-rat(a[q],p+k))
        put(f'act:{i}:opt',5*u[i]-rat(j,p+k))
    # Existing exact arbitrary-background suffix-profit theorems.
    for k in (1,2,3,4):
        p=sum(a[:5-k]); v=sum(u[5-k:])
        put(f'act:profit{k}',comb(5,k)*BETA[k]*v-subset_profit(p,j,k))
    # Root family: t=1 branches multiplicity j, t=0 branches 5-j.
    seqs=[(1,x,j),(0,y,5-j)]
    vs=[sum(mult*rat(z[i],t+sum(z)) for t,z,mult in seqs) for i in range(4)]
    put('root:IC',5*u[0]-rat(j,1+sum(x)))
    for k in range(4):
        rem=4-k
        for q in range(5):
            rhs=sum(mult*rat(a[q],t+sum(z[:k])+rem) for t,z,mult in seqs)
            put(f'root:child{k}:a{q}',vs[k]-rhs)
        rhs=sum(mult*rat(j,t+sum(z[:k])+rem) for t,z,mult in seqs)
        put(f'root:child{k}:opt',5*vs[k]-rhs)
        put(f'root:child{k}:ownT',vs[k]-rat(j,1+sum(x[:k])+rem))
        # Whole menus of all five root-family actions are legal everywhere.
        men=j*x[k]+(5-j)*y[k]
        for i in range(5):
            put(f'act:{i}:rootmenu{k}',5*u[i]-rat(men,sum(a[:i])+5-i))
        # Own future branch action is also a legal current deviation.
        for ell in range(4):
            rhs=sum(mult*rat(z[ell],t+sum(z[:k])+rem) for t,z,mult in seqs)
            put(f'root:child{k}:own{ell}',vs[k]-rhs)
    # Full-suffix profit comparisons in every genuine root child subtree.
    for k in (1,2,3,4):
        offset=4-k; v=sum(vs[offset:]); coef=comb(5,k)*BETA[k]
        rhs=sum(mult*subset_profit(t+sum(z[:offset]),j,k) for t,z,mult in seqs)
        put(f'root:profit{k}:opt',coef*v-rhs)
        rhs=sum(mult*subset_profit(t+sum(z[:offset]),c,k) for t,z,mult in seqs)
        put(f'root:profit{k}:actual',coef*v-rhs)
    return np.array(rows),w,o,names

def main():
    cols=[]; desc=[]; ws=[];os=[]
    for a in product((0,1),repeat=5):
        for j in range(6):
            # Irrelevant histogram parts have zero coefficient.
            xp=BITS if j else [BITS[0]]
            yp=BITS if j<5 else [BITS[0]]
            for x in xp:
                for y in yp:
                    r,w,o,names=col(a,j,x,y)
                    cols.append(r);ws.append(w);os.append(o);desc.append((a,j,x,y))
    mat=np.array(cols).T
    res=linprog(-np.array(os),A_ub=-mat,b_ub=np.zeros(len(names)),
                A_eq=[ws],b_eq=[1],bounds=(0,None),method='highs')
    out={'scope':'Named all-root-optimal-query affine relaxation, not a game/SPE search',
         'success':res.success,'message':res.message,'rows':len(names),'columns':len(desc)}
    if res.success:
        out.update(beta_float=-res.fun,half_closed_float=-res.fun<=2+1e-8,
          active_rows=[{'name':n,'multiplier_float':float(-v)} for n,v in zip(names,res.ineqlin.marginals) if v<-1e-8],
          atoms=[{'actual':a,'opt_multiplicity':j,'root_if_t1':x,'root_if_t0':y,'mass_float':float(z)}
                 for (a,j,x,y),z in zip(desc,res.x) if z>1e-8],
          min_row_slack_float=float(min(mat@res.x)))
    (HERE/'root_family_pressure_discovery.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('atoms','active_rows')},indent=2))

if __name__=='__main__':main()
