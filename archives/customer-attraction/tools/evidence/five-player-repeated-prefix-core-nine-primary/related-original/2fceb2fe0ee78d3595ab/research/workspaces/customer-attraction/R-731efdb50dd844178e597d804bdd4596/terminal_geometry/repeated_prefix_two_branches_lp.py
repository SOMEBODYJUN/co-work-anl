"""Explore C^(m-2) A B with a genuine third-last deviation to B.

All constraints are necessary for the original given full-history SPE; a
relaxation point is not a counterexample.  m may exceed the number of bits.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def vals(m,bits,d,l,h):
 c,a,b,q,r,v,z=bits;p=(m-3)*c;s=(m-2)*c+a+b;t=p+b+q+r;bg=p+c
 uC=F(c,s) if c else F(0);uA=F(a,s) if a else F(0);uB=F(b,s) if b else F(0)
 zQ=F(q,t) if q else F(0);zR=F(r,t) if r else F(0)
 ta=p+a+v+z;zV=F(v,ta) if v else F(0);zZ=F(z,ta) if z else F(0)
 D=(bg+1)*(bg+2)
 out={'S':m*uA-F(d,bg+1)+F(h,D),'Z':m*uB-F(l,bg+a+1),
      'V':F(d*l-m*h,D),'TT_diag':F(l,bg+1)-F(h,D)-F(d,bg+2),
      'TT_off':F((m-1)*(l-d),bg+1)+F(d*d-d-(m-1)*h,D),
      'C_to_B_true':uC-(F(b,t) if b else F(0)),
      'C_to_A_true':uC-(F(a,ta) if a else F(0))}
 for k,e in enumerate(bits):
  out[f'menu_to_{k}']=F(l-m*e,bg+1)+F(d*e-h,D)
  out[f'C_floor_{k}']=uC-F(e,p+3)
  out[f'A_floor_{k}']=uA-F(e,bg+2)
  out[f'B_exact_{k}']=uB-F(e,bg+a+1)
  out[f'Q_floor_{k}']=zQ-F(e,p+b+2)
  out[f'R_exact_{k}']=zR-F(e,p+b+q+1)
  out[f'V_floor_{k}']=zV-F(e,p+a+2)
  out[f'Z_exact_{k}']=zZ-F(e,p+a+v+1)
 for label,mult in [('T',d),('L',l)]:
  out[f'C_floor_{label}']=m*uC-F(mult,p+3)
  out[f'A_floor_{label}']=m*uA-F(mult,bg+2)
  out[f'B_exact_{label}']=m*uB-F(mult,bg+a+1)
  out[f'Q_floor_{label}']=m*zQ-F(mult,p+b+2)
  out[f'R_exact_{label}']=m*zR-F(mult,p+b+q+1)
  out[f'V_floor_{label}']=m*zV-F(mult,p+a+2)
  out[f'Z_exact_{label}']=m*zZ-F(mult,p+a+v+1)
 return out

def run(m):
 cells=[];R=[];W=[];O=[]
 for bits in product(range(2),repeat=7):
  for d in range(m+1):
   for l in range(m+1):
    for h in sorted(set([max(0,d+l-m),min(d,l)])):
     rr=vals(m,bits,d,l,h);R.append(list(rr.values()));W.append(int(any(bits[:3])));O.append(int(d>0));cells.append((bits,d,l,h))
 A=csr_matrix(np.array(R,float).T)
 z=linprog(-np.array(O,float),A_ub=-A,b_ub=np.zeros(A.shape[0]),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
 report={'m':m,'success':z.success,'message':z.message,'rows':A.shape[0],'cells':len(R)}
 if z.success:
  report.update(ratio=-z.fun,multipliers={k:str(F(float(-v)).limit_denominator(10**8)) for k,v in zip(rr,z.ineqlin.marginals) if v < -1e-8},
    point=[{'bits':list(cells[i][0]),'d':cells[i][1],'ell':cells[i][2],'h':cells[i][3],'mass':str(F(float(x)).limit_denominator(10**8))} for i,x in enumerate(z.x) if x>1e-8])
 return report

if __name__=='__main__':
 pa=argparse.ArgumentParser();pa.add_argument('--max-m',type=int,default=12);args=pa.parse_args();reports=[]
 for m in range(3,args.max_m+1):
  report=run(m);reports.append(report)
  print(json.dumps({k:v for k,v in report.items() if k not in ('multipliers','point')}),flush=True)
  Path(__file__).with_name('repeated_prefix_two_branches_lp.json').write_text(json.dumps({'scope':'necessary-condition relaxation only','reports':reports},indent=2)+'\n')
