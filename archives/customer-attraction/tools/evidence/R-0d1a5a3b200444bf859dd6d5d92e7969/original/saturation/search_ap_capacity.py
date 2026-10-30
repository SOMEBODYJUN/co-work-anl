"""Independent 192-type root-max/AP compression. Necessary rows, no SPE claim."""
from fractions import Fraction as F
from itertools import product
import scipy.optimize as so
import numpy as np
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
states=[(b,d) for b in product([0,1],repeat=5) for d in range(6)]
def q(a,b):return F(a,b) if a else F(0)
def rows(b,d):
 c,*aa=b;s=sum(b);u=[q(x,s) for x in b];out={}
 for i in range(1,5):
  out[f'size{i+1}']=c-b[i]
  bg=sum(b[:i]);k=5-i
  out[f'opt_ic{i+1}']=5*u[i]-q(d,bg+k)
  for j in range(5):out[f'ic{i+1}:A{j+1}']=u[i]-q(b[j],bg+k)
  if k>=2:
   A=4*(k-1);a=2*A+k*k
   for j in range(5):
    ss=q(b[j],bg+k)
    ff=d*(q(b[j],bg+k)+q(1-b[j],bg+1))
    out[f'AP{i+1}:A{j+1}']=5*a*u[i]-5*(a-2)*ss-2*ff
    out[f'GAP{i+1}:A{j+1}']=10*A*u[i]+5*k*c-5*(a-2)*ss-2*ff
   ff=q(d*d,bg+k)+q(d*(5-d),bg+1)
   out[f'AP{i+1}:OPT']=25*a*u[i]-5*(a-2)*q(d,bg+k)-2*ff
   out[f'GAP{i+1}:OPT']=50*A*u[i]+25*k*c-5*(a-2)*q(d,bg+k)-2*ff
 return out
names=list(rows(*states[0]));R=np.array([[float(rows(*st)[n]) for n in names] for st in states]);v=np.array([float(q(b[0],sum(b))) for b,d in states]);cc=np.array([b[0] for b,d in states]);o=np.array([int(d>0) for b,d in states]);
M=np.column_stack([-v,-cc,R]);
if __name__ == "__main__":
 import sys
 z=F(sys.argv[1]) if len(sys.argv)>1 else F(21,100)
 res=so.linprog([float(z),1]+[0]*len(names),A_ub=M,b_ub=-o,
               bounds=[(0,None),(None,None)]+[(0,None)]*len(names),method='highs')
 if not res.success:raise RuntimeError(res.message)
 aa,bb=res.x[:2]
 obj={'status':'discovery_only','rho':str(z),'objective':res.fun,
      'alpha':float(aa),'beta':float(bb),
      'rows':{n:float(l) for n,l in zip(names,res.x[2:]) if l>1e-8}}
 print(json.dumps(obj),flush=True)
