"""Add the new arbitrary-theme root rows to the old 64-atom support.

This finite LP does not certify all atom types or all SPE strategies.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
namespace={}
source=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
exec(compile(source.split('from pathlib import Path')[0],'<definitions from canonical indexed audit>','exec'),namespace)
evaluate=namespace['evaluate']
p=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=p['atoms'];D=p['denominator']
cols=[];bits=[]
for atom in atoms:
 b=list(map(int,atom['bits']));bits.append(b)
 cols.append(evaluate(b,[atom['AB_hist'],atom['AE_hist'],atom['second_hist']],atom['menus_lh'],True))
row_names=list(cols[0]);rows=[[col[n] for col in cols] for n in row_names]
w=[int(sum(b[:5])>0) for b in bits];o=[int(any(atom['AB_hist'][4:])) for atom in atoms]
root=[F(b[0],sum(b[:5])) if b[0] else F(0) for b in bits];m=5;q=3*m*m-4*m+2
new_names=[]
for a in range(10):
 for r in range(10):
  if a==r:continue
  row=[q*(m*u-b[a])-2*(b[r]-b[a])-2*(m-1)*b[r]*(1-b[a]) for b,u in zip(bits,root)]
  rows.append(row);new_names.append('root_arbitrary_pair:'+str(a)+':'+str(r))
res=linprog(-np.array(o,dtype=float),A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),A_eq=np.array([w],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
support=[i for i,x in enumerate(res.x) if x>1e-8]
active=[i for i,row in enumerate(rows) if abs(sum(float(v)*x for v,x in zip(row,res.x)))<1e-7]
A=[[F(w[j]) for j in support]]+[[row[j] for j in support] for i,row in enumerate(rows) if i in active]
rhs=[F(1)]+[F(0)]*len(active)
pivots={}
for rr,bb in zip(A,rhs):
 rr=list(rr)
 for c,(basis,brhs) in sorted(pivots.items()):
  if rr[c]:
   v=rr[c];rr=[x-v*y for x,y in zip(rr,basis)];bb-=v*brhs
 nz=next((c for c,v in enumerate(rr) if v),None)
 if nz is None:
  assert bb==0
  continue
 v=rr[nz];pivots[nz]=([x/v for x in rr],bb/v)
 if len(pivots)==len(support):break
if len(pivots)!=len(support):raise AssertionError(('active rank',len(pivots),len(support)))
solution=[F(0)]*len(support)
for c,(rr,bb) in sorted(pivots.items(),reverse=True):
 solution[c]=bb-sum(rr[j]*solution[j] for j in range(c+1,len(support)))
point=[F(0)]*len(atoms)
for j,v in zip(support,solution):point[j]=v
assert all(x>=0 for x in point)
assert sum(x*y for x,y in zip(w,point))==1
assert all(sum(x*y for x,y in zip(row,point))>=0 for row in rows)
exact_objective=sum(x*y for x,y in zip(o,point))
assert exact_objective>2
old=[F(a['mass_numerator'],D) for a in atoms]
slacks=[sum(v*x for v,x in zip(row,old)) for row in rows[-len(new_names):]]
report={'scope':'new root inequalities added only on the previously published 64 atom support','universal_bound_proved':False,'old_rows':len(row_names),'new_rows':len(new_names),'floating_new_objective':-res.fun,'status':res.message,'old_point_new_minimum_slack':str(min(slacks)),'old_point_most_violated_rows':[[n,str(s)] for n,s in zip(new_names,slacks) if s==min(slacks)],'new_float_point':['%.17g'%x for x in res.x],'exact_primal_objective':str(exact_objective),'exact_primal_point':[str(x) for x in point],'exact_primal_verified_all_rows':True,'floating_dual_nonzero':[[i,'%.17g'%x] for i,x in enumerate(res.ineqlin.marginals) if abs(x)>1e-10]}
print(json.dumps({k:v for k,v in report.items() if 'point' not in k or 'slack' in k or 'rows' in k},indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
