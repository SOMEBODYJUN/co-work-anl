"""Targeted exact test of u+r V' >= (r+1)V on saved complete SPEs.

LP only discovers supports. Every returned value has matching Fraction primal
and dual certificates; every full ordered history of each input is rechecked.
No search for new games or policies is performed.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement as cwr
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).parent

def solve_unique(rows,rhs):
    A=[[F(v) for v in row]+[F(b)] for row,b in zip(rows,rhs)]
    n=len(rows[0]);pivots=[];r=0
    for col in range(n):
        piv=next((j for j in range(r,len(A)) if A[j][col]),None)
        if piv is None:continue
        A[r],A[piv]=A[piv],A[r]
        z=A[r][col];A[r]=[v/z for v in A[r]]
        for j in range(len(A)):
            if j!=r and A[j][col]:
                z=A[j][col];A[j]=[a-z*b for a,b in zip(A[j],A[r])]
        pivots.append(col);r+=1
    assert len(pivots)==n
    assert all(any(row[:n]) or not row[-1] for row in A)
    ans=[F()]*n
    for row,col in zip(A,pivots):ans[col]=row[-1]
    return ans

def check(name):
    game=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    n,k=game['players'],len(game['topics'])
    types=[(frozenset(t['topics']),t['multiplicity']) for t in game['customers']]
    pol={tuple(t['history']):t['action'] for t in cert['strategy']['actions']}
    hs=[h for d in range(n) for h in product(range(k),repeat=d)]
    assert set(pol)==set(hs)
    @lru_cache(None)
    def leaf(h):return h if len(h)==n else leaf(h+(pol[h],))
    def utility(i,z):return sum((F(w,sum(a in s for a in z)) for s,w in types if z[i] in s),F())
    comparisons=0
    for h in hs:
        u=utility(len(h),leaf(h))
        for a in range(k):
            assert u>=utility(len(h),leaf(h+(a,))), (h,a)
            comparisons+=1
    certdata={}
    @lru_cache(None)
    def security(h):
        r=n-len(h)
        backgrounds=list(cwr(range(k),r-1))
        M=[[sum((F(w,1+sum(a in s for a in h+B)) for s,w in types if query in s),F()) for query in range(k)] for B in backgrounds]
        mat=np.asarray(M,dtype=float)
        lp=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(k),0.]],b_eq=[1.],bounds=[(0,None)]*k+[(None,None)],method='highs')
        assert lp.success
        ps=[a for a in range(k) if lp.x[a]>1e-7]
        qs=[j for j,q in enumerate(-lp.ineqlin.marginals) if q>1e-7]
        tight=[j for j,s in enumerate(lp.ineqlin.residual) if abs(s)<1e-7]
        pv=solve_unique([[M[j][a] for a in ps]+[-1] for j in tight]+[[1]*len(ps)+[0]],[0]*len(tight)+[1])
        p=[F()]*k
        for a,q in zip(ps,pv):p[a]=q
        v=pv[-1]
        caps=(-lp.ineqlin.marginals)@mat
        qtight=[a for a in range(k) if abs(caps[a]-lp.x[-1])<1e-7]
        qv=solve_unique([[M[j][a] for j in qs]+[-1] for a in qtight]+[[1]*len(qs)+[0]],[0]*len(qtight)+[1])
        assert min(p)>=0 and sum(p)==1 and qv[-1]==v
        assert min(qv[:-1])>=0 and sum(qv[:-1])==1
        assert min(sum((p[a]*row[a] for a in range(k)),F()) for row in M)==v
        assert max(sum((q*M[j][a] for j,q in zip(qs,qv[:-1])),F()) for a in range(k))==v
        certdata[h]=dict(value=str(v),p=list(map(str,p)),Q=[dict(background=list(backgrounds[j]),probability=str(q)) for j,q in zip(qs,qv[:-1])])
        return v
    z=leaf(())
    rows=[]
    for i in range(n-1):
        h=z[:i];r=n-i
        u=utility(i,z);v=security(h);vp=security(z[:i+1])
        rows.append(dict(history=list(h),r=r,u=str(u),V=str(v),Vnext=str(vp),D=str(u+(r-1)*vp-r*v),L1=str(u+r*vp-(r+1)*v)))
    return dict(instance=name,complete_spe_comparisons=comparisons,actual=z,rows=rows,certificates=[dict(history=list(h),**c) for h,c in certdata.items()],status='targeted exact saved-input test only')

if __name__=='__main__':
    names=['individual_security_failure','aggregate_theta_failure','root_tax_failure','global_decorrelation_failure','local_security_increment','five_individual_security']
    out=[]
    for name in names:
        try:rec=check(name)
        except Exception as e:rec=dict(instance=name,error=repr(e))
        out.append(rec);print(json.dumps(rec),flush=True)
    (HERE/'local_slope_check.json').write_text(json.dumps(out,indent=2)+'\n')
