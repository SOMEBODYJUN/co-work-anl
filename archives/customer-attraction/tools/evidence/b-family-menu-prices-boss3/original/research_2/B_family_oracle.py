"""Exact cuts from the full single actual-i->B branch row space.

Discovery uses SciPy; every returned cut has nonnegative rational weights,
and its complete 448-type max table is recomputed with Fraction. No true
branch utility is replaced by an actual utility. M-bit dummy query rows are
only nonnegative-profit rows, so no empty catalog action is required.
"""
from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import linprog
from max_branch_lp import branch_rows

def share(bit,den):return F(bit,den) if bit else F(0)
def selected_value(actual,d,hidden,ell,source,weights):
    i=source-1;b=actual[5];seq=actual[:i]+(b,)+hidden;den=sum(seq);c=sum(actual)
    actualpay=[share(t,c) for t in actual];pay=[share(t,den) for t in seq]
    p=sum(seq[:-2]);r,s=seq[-2:];labels=actual+(0,)+hidden;answer=F(0)
    for name,weight in weights.items():
        fields=name.split(':')
        if name=='IC':v=actualpay[i]-share(b,den)
        elif name=='M':v=6*share(r,den)-F(d,p+1)+F(d*ell,6*(p+1)*(p+2))
        elif name=='Z':v=6*share(s,den)-F(ell,p+r+1)
        elif fields[0]=='CAP':v=-F(hidden[int(fields[-1])-1])
        elif fields[0]=='actual':
            ai=int(fields[1])-1;hj=int(fields[3])-1
            v=actualpay[ai]-F(hidden[hj],6-ai+sum(actual[:ai]))
        else:
            k=int(fields[1])-1;pos=i+k;dd=6-pos+sum(seq[:pos])
            if fields[0]=='internalopt':v=6*pay[pos]-F(d,dd)
            else:
                assert fields[0]=='internal';query=int(fields[2])-1
                v=pay[pos]-F(labels[query],dd)
        answer+=weight*v
    return answer

def project(source,weights):
    """One-based source; weight names from max_branch_lp.branch_rows."""
    table={};nh=6-source
    for bits in product(range(2),repeat=6):
        for d in range(7):
            table[bits,d]=max(selected_value(bits,d,h,ell,source,weights) for h in product(range(2),repeat=nh) for ell in (0,6))
    kappa=sum(weight for name,weight in weights.items() if name.startswith('CAP:'))
    return table,kappa

def separate(masses,K,source,denominator=10**8,tolerance=1e-9):
    """masses maps (actual_tuple,d) to Fraction or numeric mass; K is scalar.

    Returns None if this selected row system is numerically lift-feasible.
    Otherwise returns an exact valid cut and its exact value on supplied
    rational masses. A float caller obtains exactness for its decimal masses.
    """
    masses={key:F(str(value)) for key,value in masses.items() if value}
    K=F(str(K));cells=list(masses);i=source-1;nh=6-source
    nn,_=branch_rows((0,)*7,(i,5),(0,)*nh,0,0)
    cols=[];eqcols=[]
    for ci,(bits,d) in enumerate(cells):
        for h,ell in product(tuple(product(range(2),repeat=nh)),(0,6)):
            names,vals=branch_rows(bits+(0,),(i,5),h,d,ell);assert names==nn
            cols.append([float(v) for v in vals]);eqcol=[0]*len(cells);eqcol[ci]=1;eqcols.append(eqcol)
    mat=np.array(cols).T;eq=np.array(eqcols).T
    rhs=np.array([float(K) if name.startswith('CAP:') else 0 for name in nn])
    obj=np.zeros(len(cols)+1);obj[-1]=-1
    sol=linprog(obj,A_ub=np.column_stack((-mat,np.ones(len(nn)))),b_ub=rhs,A_eq=np.column_stack((eq,np.zeros(len(cells)))),b_eq=[float(masses[key]) for key in cells],bounds=[(0,None)]*len(cols)+[(None,None)],method='highs')
    if not sol.success:raise RuntimeError(sol.message)
    if sol.x[-1]>=-tolerance:return None
    weights={name:F(round(max(0.,-v)*denominator),denominator) for name,v in zip(nn,sol.ineqlin.marginals) if round(max(0.,-v)*denominator)>0}
    table,kappa=project(source,weights)
    pv=sum(table[key]*mass for key,mass in masses.items())+kappa*K
    if pv>=0:raise ArithmeticError('rounded dual failed exact selected-point separation')
    return {'source':source,'weights':weights,'table':table,'kappa':kappa,'point_value':pv,'discovery_common_slack':float(sol.x[-1])}
