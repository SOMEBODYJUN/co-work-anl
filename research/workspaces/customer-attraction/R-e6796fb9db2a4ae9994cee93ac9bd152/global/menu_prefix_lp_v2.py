from fractions import Fraction as F
from itertools import product
from scipy.optimize import linprog
import numpy as np,json

def solve(m):
 k=m-2;rr=[]
 for bits in product(range(2),repeat=m):
  es=bits[:k];a,b=bits[-2:];p=sum(es);c=p+a+b;w=int(c>0)
  us=[F(e,c) if e else F(0) for e in bits];ub=us[-1]
  R=[];L=[];bj=0;bs=[]
  for j,e in enumerate(bits):
   bs.append(bj);bj+=e
   if j<k:
    R.append(us[j]-(F(a,bs[j]+m-j) if a else 0))
    L.append(ub-F(e,p+a+1))
  for d,l in [(0,0),(0,m),(1,0),(1,m),(m,0),(m,m)]:
   G=m*us[-2]+ub/2-F(d,p+1)-F(l,2*m*(p+a+1))+F(d*l,m*(p+1)*(p+2))
   H=[m*us[j]-F(d,bs[j]+m-j) for j in range(m)]
   q=2*w-int(d>0)
   rr.append((bits,d,l,[G]+R+L+H,q))
 n=len(rr[0][3]);res=linprog(np.zeros(n),A_ub=np.array([[float(x) for x in r[3]] for r in rr]),b_ub=np.array([float(r[4]) for r in rr]),bounds=(0,None),method='highs')
 ans={'m':m,'success':res.success}
 if res.success:
  sol=[F(float(x)).limit_denominator(1000000) for x in res.x]; ans['coeff']=[str(x) for x in sol]; ans['worst']=str(min(r[4]-sum(x*y for x,y in zip(r[3],sol)) for r in rr))
 return ans
if __name__=='__main__':print(json.dumps([solve(m) for m in range(3,14)],indent=2))
