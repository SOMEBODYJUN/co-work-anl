"""Discover a stronger root-rigidity slope using true intermediate IC.
Numerical exploration only; exact certificates are separate obligations.
"""
import numpy as np
from itertools import product,combinations_with_replacement
from scipy.optimize import linprog
from fractions import Fraction as F
import json
from pathlib import Path
m=5
# masks T,Q,B2,B3,B4,B5; final coordinate is actual root utility u.
bits=np.array(list(product((0,1),repeat=m+1)),dtype=int);N=len(bits);u=N
p=bits[:,0];q=bits[:,1];acts=np.column_stack((p,bits[:,2:]));load=acts.sum(axis=1)
def share(a,den):return np.divide(a,den,out=np.zeros(N,dtype=float),where=den!=0)
profit=[share(acts[:,j],load) for j in range(m)];rows=[];names=[]
def add(name,coeff,uc=0):
 rows.append(np.r_[coeff,uc]);names.append(name)
add('root-real-IC',-profit[0],1)
for j in range(m+1):add(f'root-size-{j}',-bits[:,j],m)
# Node floors use genuine action at that root-T branch node, uncertain later branches.
for stage in range(1,m):
 prefix=acts[:,:stage].sum(axis=1);remaining=m-stage
 for j in range(m+1):add(f'floor-s{stage}-q{j}',profit[stage]-bits[:,j]/(prefix+remaining))
 if stage==m-2:
  H=profit[stage]+profit[stage+1]+acts[:,stage]/((prefix+1)*(prefix+2))
  for j,k in combinations_with_replacement(range(m+1),2):
   a=bits[:,j];b=bits[:,k]
   compare=(a+b)/(prefix+1)-a*b/((prefix+1)*(prefix+2))
   add(f'pair-{j}-{k}',H-compare)
A=np.array(rows)
eq=np.r_[-p,m];objective=np.r_[q/(1+(m-1)*p),-1]
for use_pairs in [False,True]:
 keep=[j for j,n in enumerate(names) if use_pairs or not n.startswith('pair-')]
 res=linprog(-objective,A_ub=-A[keep],b_ub=np.zeros(len(keep)),A_eq=[eq],b_eq=[1],bounds=(0,None),method='highs')
 print('pairs',use_pairs,'success',res.success,'slope',-res.fun if res.success else res.message)
 if res.success:
  duals=[{'name':names[k],'weight':float(-v)} for k,v in zip(keep,res.ineqlin.marginals) if abs(v)>1e-8]
  print(duals)
  out={'scope':'Floating exploratory optimum of a genuine root-branch necessary-condition system; not a certified bound','slope':float(-res.fun),'active_rows':duals,'equality_dual':float(res.eqlin.marginals[0]),'positive_primal':[(int(i),list(map(int,bits[i])) if i<N else 'u',float(v)) for i,v in enumerate(res.x) if v>1e-8]}
  Path(__file__).with_name('probe_middle_rigidity_'+str(use_pairs)+'.json').write_text(json.dumps(out,indent=2)+'\n')
