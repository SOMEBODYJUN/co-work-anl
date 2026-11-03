"""Necessary credibility of a largest disjoint optimal topic after ABC.
All 64 old atoms have d=1. Choose the largest residual T, relabel it T0,
and average the other four T marginals. This preserves every comparison
involving T0 or a fixed topic, and preserves necessary averaged other-T
comparisons. Eleven LPs cover every potentially low last BR.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())

def build(last):
 p=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=p['atoms'];N=len(atoms)
 assert all(sum(a['AB_hist'][4:])==1 for a in atoms)
 r=[F(a['mass_numerator'],int(p['denominator'])) for a in atoms];bits=[list(map(int,a['bits'])) for a in atoms]
 u=[sum(rr*F(b[j],sum(b[:5])) for rr,b in zip(r,bits) if b[j]) for j in range(5)]
 G=sum(rr/F(sum(b[:3])+1) for rr,b in zip(r,bits))
 residual=[rr/F(sum(b[:3])+1) for rr,b in zip(r,bits)]
 copy=[rr/F(sum(b[:3])+2) for rr,b in zip(r,bits)]
 fixed_base=[sum(rr*F(b[j],sum(b[:3])+1) for rr,b in zip(r,bits)) for j in range(10)]
 fixed_coeff=[[-rr*F(b[j],(sum(b[:3])+1)*(sum(b[:3])+2)) for rr,b in zip(r,bits)] for j in range(10)]
 rows=[];rhs=[];names=[]
 def add(a,b,name):rows.append(a);rhs.append(b);names.append(name)
 for i in range(5):
  coeff=[rr/F(sum(b[:i])+5-i) for rr,b in zip(r,bits)]
  add(coeff,u[i],f'T0_path_floor_{i}')
  add([-v/F(4) for v in coeff],u[i]-sum(coeff)/4,f'Tother_path_floor_{i}')
 add([-v for v in residual],-G/5,'T0_has_largest_residual')
 if last<10:
  base=fixed_base[last];coeff=fixed_coeff[last]
  own=[rr/F(sum(b[:3])+1+b[last]) for rr,b in zip(r,bits)]
 else:
  base=F(0);coeff=copy;own=copy
 for j in range(10):
  add([a-b for a,b in zip(fixed_coeff[j],coeff)],base-fixed_base[j],f'last_BR_fixed_{j}')
 add([a-b for a,b in zip(copy,coeff)],base,'last_BR_T0_copy')
 add([-a/F(4)-b for a,b in zip(residual,coeff)],base-G/4,'last_BR_other_T')
 return atoms,r,bits,u,G,rows,rhs,names,own

def main():
 report=[]
 for last in range(11):
  atoms,r,bits,u,G,rows,rhs,names,own=build(last)
  result=linprog(np.array(own,dtype=float),A_ub=np.array(rows,dtype=float),b_ub=np.array(rhs,dtype=float),bounds=(0,1),method='highs')
  entry={'last_reply':('ABCDEUVWXY'[last] if last<10 else 'T0'),'status':result.message}
  if result.success:
   entry.update({'minimum_T0_payoff_proposal':float(result.fun),'onpath_D':float(u[3]),'margin_proposal':float(result.fun)-float(u[3]),'x':result.x.tolist(),'dual':result.ineqlin.marginals.tolist(),'lower':result.lower.marginals.tolist(),'upper':result.upper.marginals.tolist()})
  report.append(entry);print({k:v for k,v in entry.items() if k not in ('x','dual','lower','upper')},flush=True)
 (HERE/'max_topic_security_proposal.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
