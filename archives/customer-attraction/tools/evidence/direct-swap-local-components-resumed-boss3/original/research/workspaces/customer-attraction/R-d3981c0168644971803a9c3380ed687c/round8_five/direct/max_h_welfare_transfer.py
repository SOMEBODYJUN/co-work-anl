"""Attack/synthesize fresh coverage transfer to the tripled weighted maximum H."""
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
from pathlib import Path
import numpy as np,json
from scipy.optimize import linprog
bits=np.array(list(product((0,1),repeat=6)),dtype=float)
p=bits[:,0]+bits[:,1]; tail=bits[:,2:5].sum(axis=1); total=p+tail; safe=np.maximum(total,1)
u=[bits[:,i]/safe for i in (2,3,4)]; K=bits[:,5]/(p+3); gap=u[0]-K
wsource=(total>0).astype(float); wH=((p+bits[:,5])>0).astype(float); gain=wH-wsource
rows=[];names=[]
for a in range(6):
 rows.append(bits[:,a]/(p+3)-K);names.append(f'maxH_{a}')
for j in range(3):
 pref=p+bits[:,2:2+j].sum(axis=1); rem=3-j
 for a in range(6):rows.append(bits[:,a]/(pref+rem)-u[j]);names.append(f'node{j}:floor{a}')
p2=p+bits[:,2];h=u[1]+u[2]+bits[:,3]/((p2+1)*(p2+2))
for qs in combinations_with_replacement(range(6),2):
 c=bits[:,qs].sum(axis=1);comp=np.divide(c,p2+c,out=np.zeros_like(c),where=p2+c>0)
 rows.append(comp-h);names.append(f'tax2_{qs}')
for qs in combinations_with_replacement(range(6),3):
 c=bits[:,qs].sum(axis=1);comp=np.divide(c,p+c,out=np.zeros_like(c),where=p+c>0)
 rows.append(comp-(5/3)*(u[0]+u[1]+u[2]));names.append(f'profit3_{qs}')
for a in range(6):
 FHT=bits[:,5]*bits[:,a]/(p+3)+(1-bits[:,5])*bits[:,a]/(p+1)
 rows.append(FHT-K-8*gap);names.append(f'BNS_{a}')
R=np.array(rows)
out=[]
for zero in (True,False):
 if zero:
  r=linprog(-gain,A_ub=R,b_ub=np.zeros(len(R)),A_eq=[K,gap],b_eq=[1,0],bounds=(0,None),method='highs')
 else:
  r=linprog(-gain,A_ub=R,b_ub=np.zeros(len(R)),A_eq=[gap],b_eq=[1],bounds=(0,None),method='highs')
 o={'zero_gap':zero,'status':'floating_necessary_relaxation_only','success':bool(r.success),'message':r.message}
 if r.success:o.update(gain=float(-r.fun),dual_eq=list(-r.eqlin.marginals),mults={n:float(-v) for n,v in zip(names,r.ineqlin.marginals) if abs(v)>1e-8},support=[{'bits':''.join(str(int(v)) for v in b),'mass':float(z)} for b,z in zip(bits,r.x) if z>1e-8])
 out.append(o)
print([{k:v for k,v in o.items() if k not in ('mults','support')} for o in out]);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
