from itertools import product
import numpy as np
from scipy.optimize import linprog

def data(m):
 cols=list(product(range(1<<m),range(m+1),range(m+1))); X=[]; w=[];o=[]
 names=['G']+[f'direct_actual:{i}:{j}' for i in range(m) for j in range(m)]+[f'direct_cmp:{i}' for i in range(m)]+[f'direct_reply:{i}' for i in range(m)]
 for mask,d,l in cols:
  J=[(mask>>i)&1 for i in range(m)]; c=sum(J); u=[j/c if c else 0 for j in J]; bkg=[sum(J[:i]) for i in range(m)]; p=sum(J[:-2]);a,b=J[-2:]
  G=m*u[-2]+u[-1]/2-d/(p+1)-l/(2*m*(p+a+1))+d*l/(m*(p+1)*(p+2))
  row=[G]+[u[i]-J[j]/(bkg[i]+m-i) for i in range(m) for j in range(m)]+[u[i]-d/(m*(bkg[i]+m-i)) for i in range(m)]+[u[i]-l/(m*(bkg[i]+m-i)) for i in range(m)]
  X.append(row);w.append(int(c>0));o.append(int(d>0))
 return cols,names,np.array(X),np.array(w),np.array(o)

def solve(m):
 cols,names,X,w,o=data(m)
 A=np.column_stack([X,-w]);c=np.array([0]*X.shape[1]+[1]);
 res=linprog(c,A_ub=A,b_ub=-o,bounds=[(0,None)]*len(c),method='highs')
 print(m,res.status,res.fun,flush=True)
 if res.success:
  print(' multipliers',[(n,round(float(v),8)) for n,v in zip(names,res.x[:-1]) if v>1e-7],flush=True)
  print(' positive primal types',[(cols[k],round(float(v),9)) for k,v in enumerate(-res.ineqlin.marginals) if v>1e-7],flush=True)
 return res
if __name__=='__main__':
 for m in range(3,9):solve(m)
