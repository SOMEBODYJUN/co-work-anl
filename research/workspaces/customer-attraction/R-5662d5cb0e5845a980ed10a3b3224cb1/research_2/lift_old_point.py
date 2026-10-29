"""Can new nested B-copy graphs extend the old exact actual marginals?

This tests only an enlarged necessary-condition projection. Feasible is not
an SPE completion; infeasible would reject those old actual marginals only.
"""
from itertools import product
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from nested_branch_lp import nested_rows
from max_branch_lp import branch_rows

ROOT=Path(__file__).resolve().parents[5]
POINT=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json'

def marginal():
    j=json.loads(POINT.read_text());cells=defaultdict(F);K=F(0)
    for col in j['columns']:
        if col['kind']=='K':K+=F(col['weight'])
        if col['kind']=='hist' and F(col['weight']):
            cells[(tuple(map(int,col['actual_bits'])),col['d'])]+=F(col['weight'])
    W=sum(v for (bits,d),v in cells.items() if sum(bits))
    assert W==F(j['W'])
    return list(cells.items()),K

def solve(source,query_kind,plain=False,separate=False):
    cells,K=marginal();n=6;hsize=n-source-1 if plain else 2*n-2*source-3
    columns=[];eqcolumns=[];names=None
    for ci,((act,d),mass) in enumerate(cells):
        for hidden in product(range(2),repeat=hsize):
            childells=(0,n) if not plain and source<=n-4 else (0,)
            for ell,childell in product((0,n),childells):
                nn,vals=branch_rows(act+(0,),(source,n-1),hidden,d,ell) if plain else nested_rows(act+(0,),source,hidden,d,ell,childell,query_kind)
                if names is None:names=nn
                assert names==nn
                columns.append([float(v) for v in vals]);col=[0]*len(cells);col[ci]=1;eqcolumns.append(col)
    mat=np.array(columns).T;eq=np.array(eqcolumns).T
    rhs=np.array([float(K) if name.startswith('CAP:') else 0 for name in names])
    if separate:
        obj=np.zeros(mat.shape[1]+1);obj[-1]=-1
        lp=linprog(obj,A_ub=np.column_stack((-mat,np.ones(len(names)))),b_ub=rhs,A_eq=np.column_stack((eq,np.zeros(len(cells)))),b_eq=[float(v) for _,v in cells],bounds=[(0,None)]*mat.shape[1]+[(None,None)],method='highs')
    else:
        lp=linprog(np.zeros(mat.shape[1]),A_ub=-mat,b_ub=rhs,A_eq=eq,b_eq=[float(v) for _,v in cells],bounds=(0,None),method='highs')
    out={'source':source+1,'query_kind':query_kind,'plain':plain,'variables':mat.shape[1],'rows':len(names),'status':lp.message,'feasible':bool(lp.success)}
    if separate and lp.success:
        out.pop('feasible')
        out['original_feasible_at_t0']=bool(lp.x[-1]>=-1e-9)
        out.update(common_slack=lp.x[-1],multipliers={name:float(-v) for name,v in zip(names,lp.ineqlin.marginals) if -v>1e-9})
    return out
if __name__=='__main__':
    print(json.dumps([solve(i,kind) for kind in ['A','terminal'] for i in range(4)],indent=2))
