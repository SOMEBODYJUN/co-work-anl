from itertools import product
import numpy as np
from scipy.optimize import linprog

def rows(m,co):
 p,a,b,d,l=co; c=p+a+b
 P=p/c if c else 0; A=a/c if c else 0; B=b/c if c else 0
 G=m*A+B/2-d/(p+1)-l/(2*m*(p+a+1))+d*l/(m*(p+1)*(p+2))
 return [G,P-(m-2)*a/m,(m-2)*B-p/(p+a+1),m*B-d/(p+a+1),m*B-l/(p+a+1),P-(m-2)*b/m,P-(m-2)*d/m**2,P-(m-2)*l/m**2,(m-2)*A-p/(p+2),A-b/(p+2),m*A-d/(p+2),m*A-l/(p+2)]

def solve(m):
 cols=list(product(range(m-1),range(2),range(2),range(m+1),range(m+1)))
 X=np.array([rows(m,x) for x in cols]);w=np.array([int(sum(x[:3])>0) for x in cols]);o=np.array([int(x[3]>0) for x in cols]);
 # lambda row <= beta*w-o
 A=np.column_stack([X,-w]);c=np.array([0]*X.shape[1]+[1]);
 res=linprog(c,A_ub=A,b_ub=-o,bounds=[(0,None)]*len(c),method='highs')
 print(m,res.status,res.fun)
 if res.success:
  print(' multipliers',res.x)
  print(' positive primal types',[(cols[k],float(v)) for k,v in enumerate(-res.ineqlin.marginals) if v>1e-7])
 return res
if __name__=='__main__':
 for m in range(3,13):solve(m)
