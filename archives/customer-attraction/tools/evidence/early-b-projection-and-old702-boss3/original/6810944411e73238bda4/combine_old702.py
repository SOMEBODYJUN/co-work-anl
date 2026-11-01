"""Read-only discovery: old full-domain 702 rows plus the new psi row.

Importing old generators does not replace their separate proof obligations.
No output in another actor's workspace is modified.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.optimize import linprog
from tail3_B_projection import table

ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import new_reply_budget as nr

def solve():
    types,rows=nr.old_system();tt=table()
    new=[tt[(''.join(map(str,a)),d)]/204 for a,d in types]+[0]
    rows=rows+[('actual-fourth-to-B-tail3-psi',new)]
    mat=np.array([[float(x) for x in row] for _,row in rows]);scale=np.max(abs(mat),axis=1);scale[scale==0]=1
    obj=[int(any(a)) for a,d in types]+[0];normal=[int(d>0) for a,d in types]+[0]
    lp=linprog(obj,A_ub=-mat/scale[:,None],b_ub=np.zeros(len(rows)),A_eq=[normal],b_eq=[1],bounds=(0,None),method='highs')
    out={'scope':'full 448 old coefficient types, old 702 valid projections plus one new psi row; float discovery only','rows':len(rows),'columns':len(obj),'status':lp.message}
    if lp.success:
        out.update(W=lp.fun,ratio=1/lp.fun,new_psi_dual=float(-lp.ineqlin.marginals[-1]/scale[-1]),active_types=[{'actual_bits':''.join(map(str,types[j][0])),'d':types[j][1],'mass':float(v)} for j,v in enumerate(lp.x[:-1]) if v>1e-8],K=float(lp.x[-1]))
    return out
if __name__=='__main__':print(json.dumps(solve(),indent=2))
