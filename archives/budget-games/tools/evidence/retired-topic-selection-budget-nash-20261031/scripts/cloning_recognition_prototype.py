"""Floating prototype of the proved active-cell/gradient LP algorithm.
This is NOT a certified rational implementation. Mathematical correctness of
the exact LP algorithm is in CLONING_AND_SEPARABLE_TOYS.md, section 5.
The hand cases below include degenerate/tie, positive-entry, dimension-2,
and genuine failure cases. No random seed or sampling is used.
"""
from itertools import combinations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

def lp_common_max(A,I,U):
    C=A[list(I),:];R,m=C.shape
    rows=[C[:,s]-C[:,j] for j in U for s in range(m)]
    return linprog(np.zeros(R),A_ub=np.array(rows) if rows else None,
                   b_ub=np.zeros(len(rows)) if rows else None,
                   A_eq=np.ones((1,R)),b_eq=[1],bounds=[(0,None)]*R,
                   method='highs')

def recognize(A,tol=1e-9):
    A=np.array(A,dtype=float);R,m=A.shape;examined=[]
    for size in range(1,R+1):
        for I in combinations(range(R),size):
            # Variables: delta_1,...,delta_m,z,eta.
            J=[]; witnesses=[];outside=set(range(R))-set(I)
            eq=[np.r_[np.ones(m),0,0]]
            beq=[1]
            for r in I:eq.append(np.r_[A[r],-1,0]);beq.append(0)
            for j in range(m):
                ub=[np.r_[-A[r],1,1] for r in outside]
                row=np.zeros(m+2);row[j]=-1;row[-1]=1;ub.append(row)
                obj=np.zeros(m+2);obj[-1]=-1
                res=linprog(obj,A_ub=np.array(ub),b_ub=np.zeros(len(ub)),
                            A_eq=np.array(eq),b_eq=beq,
                            bounds=[(0,None)]*m+[(None,None),(0,1)],method='highs')
                if res.success and res.x[-1]>tol:
                    J.append(j);witnesses.append(res.x[:m])
            if not J:continue
            U=[j for j in J if lp_common_max(A,I,[j]).success]
            common=lp_common_max(A,I,U)
            examined.append(dict(I=list(I),J=J,U=U,common=common.success))
            if not common.success:
                return dict(property=False,active_rows=list(I),accessible_coordinates=J,
                            maximizable_coordinates=U,delta_witness=np.mean(witnesses,axis=0).tolist(),
                            examined_cells=examined)
    return dict(property=True,examined_cells=examined)

if __name__=='__main__':
    cases=[
        ('linear',[[1,2,3]],True),
        ('Leontief_3',[[1,0,0],[0,1,0],[0,0,1]],True),
        ('two_resources_nonsmooth',[[3,1],[1,3]],True),
        ('three_resources_common_gradient',[[2,0,1],[0,2,1]],True),
        ('three_resources_failure',[[2,0,1.5],[0,2,1.5]],False),
        ('strictly_positive_failure',[[3,1,2.5],[1,3,2.5]],False),
    ]
    out=[]
    for name,A,expected in cases:
        r=recognize(A);assert r['property']==expected,(name,r)
        r['name']=name;r['A']=A;out.append(r)
        print(name,r['property'],r.get('delta_witness',''),flush=True)
    Path(__file__).with_name('cloning_recognition_prototype.json').write_text(json.dumps(dict(arithmetic='float64 SciPy HiGHS; 1e-9 positive-margin tolerance; not a proof certificate',cases=out),indent=2))
