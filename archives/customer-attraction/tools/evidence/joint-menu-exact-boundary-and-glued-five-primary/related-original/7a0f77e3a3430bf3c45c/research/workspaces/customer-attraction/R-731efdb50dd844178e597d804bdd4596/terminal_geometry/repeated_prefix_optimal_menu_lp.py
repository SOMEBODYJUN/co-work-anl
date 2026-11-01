"""True C->T_i three-player menus for repeated-prefix actual paths.

Contingency counts of (T_i,Q_i,R_i) retain all within-branch intersections.
This is a necessary-condition LP, not a complete-SPE construction.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

patterns=list(product(range(2),repeat=3))
def compositions(n,k):
 if k==1:yield (n,);return
 for x in range(n+1):
  for rest in compositions(n-x,k-1):yield (x,)+rest

def vals(m,bits,counts):
 c,a,b=bits;p=(m-3)*c;s=(m-2)*c+a+b
 uC=F(c,s) if c else F(0);uA=F(a,s) if a else F(0);uB=F(b,s) if b else F(0)
 d=sum(n*t for n,(t,q,r) in zip(counts,patterns));ell=sum(n*q for n,(t,q,r) in zip(counts,patterns));v=sum(n*r for n,(t,q,r) in zip(counts,patterns))
 first=F(0);Q=F(0);R=F(0);tax=F(0);Qden=F(0);Rden=F(0);taxTT=F(0)
 qdiag=[F(0)]*3;rdiag=[F(0)]*3
 pair_actual=[F(0)]*3;pair_T_actual=[F(0)]*3
 for n,(t,q,r) in zip(counts,patterns):
  if not n:continue
  z=p+t+q+r
  first+=F(n*t,z) if t else 0;Q+=F(n*q,z) if q else 0;R+=F(n*r,z) if r else 0
  tax+=F(n*q,(p+t+1)*(p+t+2));Qden+=F(n,p+t+2);Rden+=F(n,p+t+q+1)
  taxTT+=F(2*n*d*(m-d),p+t+1)+F(2*n*d*(d-1),p+t+2)
  for k,e in enumerate((t,q,r)):
   qdiag[k]+=F(n*e,p+t+2);rdiag[k]+=F(n*e,p+t+q+1)
  for k,e in enumerate(bits):
   pair_actual[k]+=F(n*2*e,p+t+2*e) if e else 0
   pair_T_actual[k]+=F(n*d,p+t+1) if not e else F(n*(m-d),p+t+1)+F(2*n*d,p+t+2)
 out={'root_C_T_true':m*uC-first,'pair_TT':m*(m-1)*(Q+R+tax)-taxTT}
 for k,e in enumerate(bits):
  out[f'Q_actual_{k}']=Q-e*Qden;out[f'R_actual_{k}']=R-e*Rden
  out[f'pair_same_actual_{k}']=Q+R+tax-pair_actual[k]
  out[f'pair_T_actual_{k}']=m*(Q+R+tax)-pair_T_actual[k]
  out[f'C_actual_{k}']=uC-F(e,p+3);out[f'A_actual_{k}']=uA-F(e,p+c+2);out[f'B_actual_{k}']=uB-F(e,p+c+a+1)
 for k,(label,mult) in enumerate(zip(('T','Q','R'),(d,ell,v))):
  out[f'Q_all_{label}']=m*Q-mult*Qden;out[f'R_all_{label}']=m*R-mult*Rden
  out[f'Q_diag_{label}']=Q-qdiag[k];out[f'R_diag_{label}']=R-rdiag[k]
  out[f'Q_off_{label}']=(m-1)*Q-mult*Qden+qdiag[k];out[f'R_off_{label}']=(m-1)*R-mult*Rden+rdiag[k]
  out[f'C_all_{label}']=m*uC-F(mult,p+3)
  out[f'A_all_{label}']=m*uA-F(mult,p+c+2)
  out[f'B_all_{label}']=m*uB-F(mult,p+c+a+1)
 return out,d

def run(m):
 R=[];W=[];O=[];cells=[]
 for bits in product(range(2),repeat=3):
  for counts in compositions(m,8):
   rr,d=vals(m,bits,counts);R.append(list(rr.values()));W.append(int(any(bits)));O.append(int(d>0));cells.append((bits,counts))
 A=csr_matrix(np.array(R,float).T)
 z=linprog(-np.array(O,float),A_ub=-A,b_ub=np.zeros(A.shape[0]),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
 report={'m':m,'success':z.success,'message':z.message,'rows':A.shape[0],'cells':len(R)}
 if z.success:
  report.update(ratio=-z.fun,multipliers={k:str(F(float(-v)).limit_denominator(10**8)) for k,v in zip(rr,z.ineqlin.marginals) if v < -1e-8},
    point=[{'bits':list(cells[i][0]),'counts':list(cells[i][1]),'mass':str(F(float(x)).limit_denominator(10**8))} for i,x in enumerate(z.x) if x>1e-8])
 return report

if __name__=='__main__':
 pa=argparse.ArgumentParser();pa.add_argument('--max-m',type=int,default=8);args=pa.parse_args();reports=[]
 for m in range(3,args.max_m+1):
  report=run(m);reports.append(report)
  print(json.dumps({k:v for k,v in report.items() if k not in ('multipliers','point')}),flush=True)
  Path(__file__).with_name('repeated_prefix_optimal_menu_lp.json').write_text(json.dumps({'scope':'necessary-condition relaxation only','reports':reports},indent=2)+'\n')
