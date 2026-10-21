"""Exact recovery and exhaustive type-column audit, not an SPE solver."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
import joint_menu_lp as joint
import repeated_prefix_two_branches_lp as branch

HERE=Path(__file__).resolve().parent
def independent_solve(equations,targets,unknowns):
    basis={}
    for row,target in zip(equations,targets):
        row=list(row)+[target]
        for pivot,base in sorted(basis.items()):
            if row[pivot]:
                mul=row[pivot];row=[v-mul*w for v,w in zip(row,base)]
        pivot=next((i for i,v in enumerate(row[:-1]) if v),None)
        if pivot is None:
            assert not row[-1],('inconsistent',row[-1]);continue
        mul=row[pivot];row=[v/mul for v in row];basis[pivot]=row
        if len(basis)==unknowns:break
    if len(basis)!=unknowns:raise ValueError(('rank',len(basis),unknowns))
    sol=[F(0)]*unknowns
    for pivot,row in sorted(basis.items(),reverse=True):
        sol[pivot]=row[-1]-sum((v*x for v,x in zip(row[pivot+1:-1],sol[pivot+1:])),F(0))
    return sol

def positive_certificate():
    m=5;rows=[];targets=[];cells=[]
    for bits in product(range(2),repeat=7):
      for d in range(m+1):
       for l in range(m+1):
        for h in sorted(set([max(0,d+l-m),min(d,l)])):
         rr=branch.vals(m,bits,d,l,h)
         names=list(rr);rows.append(list(rr.values()));targets.append(F(2*int(any(bits[:3]))-int(d>0)));cells.append((bits,d,l,h))
    A=np.array(rows,float);t=np.array(targets,float)
    res=linprog(np.ones(len(names)),A_ub=A,b_ub=t,bounds=(0,None),method='highs')
    assert res.success,res.message
    support=[i for i,v in enumerate(res.x) if v>1e-8]
    active=[i for i,v in enumerate(t-A@res.x) if abs(v)<1e-7]
    eq=[[rows[i][j] for j in support] for i in active]
    multipliers=independent_solve(eq,[targets[i] for i in active],len(support))
    assert min(multipliers)>=0
    residuals=[target-sum((mu*row[j] for j,mu in zip(support,multipliers)),F(0)) for target,row in zip(targets,rows)]
    assert min(residuals)>=0,min(residuals)
    report={'status':'exact_internal_candidate','claim':'m=5 actual path C,C,C,A,B has 2W>=OPT5',
      'scope':'all 128 memberships and all feasible d,ell,h; affine h endpoints suffice',
      'multipliers':{names[j]:str(v) for j,v in zip(support,multipliers)},
      'columns_checked':len(rows),'minimum_residual':str(min(residuals)),
      'zero_residual_columns':sum(v==0 for v in residuals)}
    (HERE/'five_player_repeated_prefix_half_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def relaxation_boundary():
    m=5;rows=[];W=[];O=[];cells=[]
    for bits in product(range(2),repeat=m):
      for d in range(m+1):
       for l in range(m+1):
        for h in range(max(0,d+l-m),min(d,l)+1):
         rr=joint.cell_rows(m,bits,d,l,h)
         names=list(rr);rows.append(list(rr.values()));W.append(F(int(any(bits))));O.append(F(int(d>0)));cells.append((bits,d,l,h))
    A=np.array(rows,float).T
    res=linprog(-np.array(O,float),A_ub=-A,b_ub=np.zeros(len(names)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
    assert res.success,res.message
    support=[i for i,v in enumerate(res.x) if v>1e-8]
    active=[j for j,v in enumerate(A@res.x) if abs(v)<1e-7]
    eq=[[W[i] for i in support]]+[[rows[i][j] for i in support] for j in active]
    sol=independent_solve(eq,[F(1)]+[F(0)]*len(active),len(support))
    assert min(sol)>=0
    slacks=[sum((x*rows[i][j] for x,i in zip(sol,support)),F(0)) for j in range(len(names))]
    assert min(slacks)>=0,min(slacks)
    welfare=sum((x*W[i] for x,i in zip(sol,support)),F(0));opt=sum((x*O[i] for x,i in zip(sol,support)),F(0))
    assert welfare==1 and opt>2
    report={'status':'exact_relaxation_boundary_only','m':m,'welfare':str(welfare),'comparison_coverage':str(opt),'half_violation':str(opt-2),
      'not_an_SPE_counterexample':True,'scope':'nonnegative combinations of the listed aggregated menu and actual-node guarantee rows plus nonnegative columns',
      'point':[{'bits':list(cells[i][0]),'d':cells[i][1],'ell':cells[i][2],'h':cells[i][3],'mass':str(x)} for x,i in zip(sol,support)],
      'row_slacks':{name:str(v) for name,v in zip(names,slacks)}}
    (HERE/'joint_menu_exact_boundary.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k not in ('point','row_slacks')}

if __name__=='__main__':
    print(json.dumps({'positive':positive_certificate(),'boundary':relaxation_boundary()},indent=2))
