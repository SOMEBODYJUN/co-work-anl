"""Join two truthful menu projections through common actual/T marginals.

This remains a relaxation: it does not enforce cross-label comparisons across
the two menu systems. It is valid for every actual instance and full SPE.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack
import repeated_prefix_two_branches_lp as A
import repeated_prefix_optimal_menu_lp as B

def run(m):
    colsA=[];colsB=[];projA=[];projB=[];W=[];O=[]
    for bits in product(range(2),repeat=7):
      for d in range(m+1):
       for ell in range(m+1):
        for h in sorted(set([max(0,d+ell-m),min(d,ell)])):
            rr=A.vals(m,bits,d,ell,h);colsA.append(list(rr.values()));W.append(int(any(bits[:3])));O.append(int(d>0))
            projA.append(((bits[0]*4+bits[1]*2+bits[2])*(m+1)+d))
    for bits in product(range(2),repeat=3):
      for counts in B.compositions(m,8):
        rr,d=B.vals(m,bits,counts);colsB.append(list(rr.values()));projB.append(((bits[0]*4+bits[1]*2+bits[2])*(m+1)+d))
    na=len(colsA);nb=len(colsB);n=na+nb;ra=len(colsA[0]);rb=len(colsB[0])
    matA=np.array(colsA,float).T;matB=np.array(colsB,float).T
    i1,j1=np.nonzero(matA);i2,j2=np.nonzero(matB)
    G=coo_matrix((np.concatenate([-matA[i1,j1],-matB[i2,j2]]),
      (np.concatenate([i1,i2+ra]),np.concatenate([j1,j2+na]))),shape=(ra+rb,n)).tocsr()
    M=coo_matrix((np.concatenate([np.ones(na),-np.ones(nb)]),
       (np.array(projA+projB),np.arange(n))),shape=(8*(m+1),n)).tocsr()
    E=vstack([M,coo_matrix(np.array(W+[0]*nb,float).reshape(1,n))]).tocsr()
    z=linprog(-np.array(O+[0]*nb,float),A_ub=G,b_ub=np.zeros(ra+rb),A_eq=E,
        b_eq=[0]*(8*(m+1))+[1],bounds=(0,None),method='highs')
    report={'m':m,'success':z.success,'message':z.message,'columns_A':na,'columns_B':nb,'rows':ra+rb,'marginals':8*(m+1)}
    if z.success:report['ratio']=-z.fun
    return report

if __name__=='__main__':
    reports=[]
    for m in [5,6,7,8]:
        r=run(m);reports.append(r);print(json.dumps(r),flush=True)
        Path(__file__).with_name('glued_menus_lp.json').write_text(json.dumps({'scope':'necessary-condition relaxation only','reports':reports},indent=2)+'\n')
