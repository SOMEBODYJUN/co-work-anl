"""Exact Farkas obstruction to coupling one particular root refinement.
It does not exclude other refinements of the original 38 atoms.
"""
from pathlib import Path
from fractions import Fraction as F
import json
HERE=Path(__file__).parent
run=json.loads((HERE/'couple_root_refinement.json').read_text());cells=json.loads((HERE/'root_menu_completion_exact.json').read_text())['positive_refinements'];cols=run['column_specs']
lam=[F(float(x)).limit_denominator(100) for x in run['dual_rows']];nu=[F(float(x)).limit_denominator(100) for x in run['dual_equalities']]
assert min(lam)>=0 and sum(lam)==1

def off(h,j,k):
 c=sum(n*v[k] for t,v,n in h);z=F()
 for t,v,n in h:
  total=t+sum(v);den=t+sum(v[:j])+4-j;u=F(v[j],total) if v[j] else F();z+=n*(4*u-F(c-v[k],den))/5
 return z
residuals=[]
for a,h in cols:
 lhs=sum(lam[4*j+k]*off(h,j,k) for j in range(4) for k in range(4))
 lhs+=sum(nu[i]*F(sum(n for t,v,n in h if t==r['t'] and tuple(v)==tuple(r['replies'])),5) for i,r in enumerate(cells) if a==r['atom'])
 assert lhs<=0;residuals.append(lhs)
budget=sum(n*F(r['mass']) for n,r in zip(nu,cells));assert budget>0
report={'scope':'no coupling of the particular 92-cell root refinement can meet all 16 cross-root-menu BR rows; no statement about other root refinements or full 2396-point completion','columns':len(cols),'marginals':len(cells),'lambda':[str(x) for x in lam],'nu':[str(x) for x in nu],'column_inequalities_verified_exactly':True,'minimum_column_dual_slack':str(min(-x for x in residuals)),'positive_impossibility_budget':str(budget),'positive_impossibility_budget_float':float(budget)}
(HERE/'root_coupling_obstruction_exact.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('lambda','nu')},indent=2))
