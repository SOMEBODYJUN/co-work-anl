"""Exploratory finite-type LP; numerical result is not a proof."""
import itertools,json
import numpy as np
from scipy.optimize import linprog

def f(z,n):return z/n if z else 0.
def row(p,a,b,c,q,r,d,ell,k):
 s=a+b+c; al=f(a,p+s);be=f(b,p+s);ga=f(c,p+s);D=(p+a+1)*(p+a+2)
 # KQ KR P Z SplusV F J BminusA CminusA
 return np.array([3*al-3*q/(p+3),3*al-3*r/(p+3),
  k*ga-d/(p+a+b+1),k*ga-ell/(p+a+b+1),
  k*be-d/(p+a+1)+d*ell/(k*D),
  al-f(c,p+c+q+r),k*f(r,p+c+q+r)-d/(p+c+q+1),be-al,ga-al]), al

def solve(k,ps,mins=True):
 rows=[];rhs=[];keys=[]
 for p in ps:
  for a,b,c,q,r in itertools.product(range(2),repeat=5):
   for d,ell in [(0,0),(0,k),(1,0),(1,k),(k,0),(k,k)]:
    z,al=row(p,a,b,c,q,r,d,ell,k)
    if not mins:z=z[:7]
    rows.append(z);rhs.append(bool(p+a+b+c)+k*al-bool(d));keys.append((p,a,b,c,q,r,d,ell))
 rr=linprog(np.ones(len(rows[0])),A_ub=rows,b_ub=rhs,bounds=(0,None),method='highs')
 return {'k':k,'ps':ps,'mins':mins,'success':rr.success,'status':rr.message,'lambda':rr.x.tolist() if rr.success else None}
if __name__=='__main__':
 for k in [3,4,5,6,8,10,15,20,30,50,100]:
  print(json.dumps(solve(k,list(range(k-2)),True)))
