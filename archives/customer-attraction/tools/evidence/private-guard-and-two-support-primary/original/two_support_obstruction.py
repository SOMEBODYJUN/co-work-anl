"""Exact rational candidate certificates for SPE paths on at most two themes.

Only uses valid actual-node floor comparisons and the last-two tax bound.
Finite LPs are candidate generators; every reported accepted dual is exact.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))

def coeffs(m,path):
    # j counts membership in an arbitrary m-term optimum comparison tuple.
    atoms=[(b,c,j) for b,c in product(range(2),repeat=2) for j in range(m+1) if b or c or j]
    W=[F(bool(b+c)) for b,c,j in atoms]
    O=[F(bool(j)) for b,c,j in atoms]
    n=[path.count(a) for a in range(2)]
    rows=[]; names=[]
    def add(name,func):
        names.append(name); rows.append(tuple(func(b,c,j) for b,c,j in atoms))
    def util(b,c,a):
        bits=(b,c);d=n[0]*b+n[1]*c
        return F(bits[a],d) if bits[a] else F(0)
    for i,a in enumerate(path):
        prefix=path[:i]; k=m-i
        def pref(b,c):return prefix.count(0)*b+prefix.count(1)*c
        for Q in range(2):
            add(f'node{i+1}:K:{Q}',lambda b,c,j,Q=Q:util(b,c,a)-F((b,c)[Q],pref(b,c)+k))
        add(f'node{i+1}:sum-opt',lambda b,c,j:m*util(b,c,a)-F(j,pref(b,c)+k))
        add(f'node{i+1}:cover',lambda b,c,j:m*k*util(b,c,a)+F(pref(b,c),pref(b,c)+k)-bool(j))
    prefix=path[:-2];a=path[-2];z=path[-1]
    def pref(b,c):return prefix.count(0)*b+prefix.count(1)*c
    def H(b,c):
        p=pref(b,c)
        return util(b,c,a)+util(b,c,z)+F((b,c)[a],(p+1)*(p+2))
    add('last-two:cover',lambda b,c,j:F(m,2)*H(b,c)+F(pref(b,c),pref(b,c)+1)-bool(j))
    add('last-two:sum-pairs',lambda b,c,j:F(m*(m-1),2)*H(b,c)-F(j*(m-j),pref(b,c)+1)-F(j*(j-1),pref(b,c)+2))
    for Q,R in [(0,0),(0,1),(1,1)]:
        def pair(b,c,j,Q=Q,R=R):
            d=(b,c)[Q]+(b,c)[R];p=pref(b,c)
            return H(b,c)-(F(d,p+d) if d else F(0))
        add(f'last-two:pair:{Q},{R}',pair)
    return atoms,tuple(W),tuple(O),names,rows

def recover_dual(m,path):
    atoms,W,O,names,G=coeffs(m,path)
    mat=np.array(G,dtype=float)
    res=linprog(-np.array(O,dtype=float),A_ub=-mat,b_ub=np.zeros(len(G)),A_eq=[np.array(W,dtype=float)],b_eq=[1],bounds=(0,None),method='highs')
    assert res.success,res.message
    beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
    mu=[F(float(-x)).limit_denominator(10**7) for x in res.ineqlin.marginals]
    residual=[beta*w-o-sum(mu[i]*G[i][j] for i in range(len(G))) for j,(w,o) in enumerate(zip(W,O))]
    ok=all(x>=0 for x in mu) and all(x>=0 for x in residual)
    return {'path':list(path),'proposal':-res.fun,'beta':str(beta),'exact_dual_ok':ok,'dual':{name:str(x) for name,x in zip(names,mu) if x},'minimum_residual':str(min(residual))}

def main():
    report={'scope':'Uniform in all finite common catalogs and all full-history pure SPE with a specified two-label on-path word; LP row source uses actual moves and the true last-two tax inequality. Uncertified floating values are not theorems.','m':{}}
    for m in range(2,11):
        # Relabel symmetry, retain all ordered path patterns (order matters).
        rows=[recover_dual(m,(0,)+tail) for tail in product(range(2),repeat=m-1)]
        worst=max(rows,key=lambda x:x['proposal'])
        report['m'][str(m)]={'worst_proposal':worst['proposal'],'worst_path':worst['path'],'all_exact_dual_ok':all(x['exact_dual_ok'] for x in rows),'every_certificate_below_two':all(F(x['beta'])<=2 and x['exact_dual_ok'] for x in rows),'patterns':rows}
        print(m,worst['proposal'],worst['path'],report['m'][str(m)]['every_certificate_below_two'],flush=True)
    (HERE/'two_support_obstruction.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
