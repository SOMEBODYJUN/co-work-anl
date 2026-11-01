from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
lam=list(map(F,['7/36','1/3','5/9','5/72','5/18','1/3','1/6']))
def rho(bits,d,l,p):
 a,b,c,q,r=bits;s=a+b+c
 al,be,ga=[F(v,p+s) if v else F() for v in (a,b,c)]
 def u(v,*o):return F(v,p+sum(o)+v) if v else F()
 D=(p+1+a)*(p+2+a)
 row=[3*al-F(3*q,p+3),3*al-F(3*r,p+3),2*ga-F(d,p+1+a+b),2*ga-F(l,p+1+a+b),2*be-F(d,p+1+a)+F(d*l,2*D),al-u(c,q,r),2*u(r,c,q)-F(d,p+1+c+q)]
 G=sum((x*y for x,y in zip(lam,row)),F())
 return 2*al+int(p+s>0)-min(1,d)-G
records=[];bad=[]
for bits in product(range(2),repeat=5):
 for d,l in [(0,0),(1,0),(1,2),(2,0),(2,2)]:
  vals=[rho(bits,d,l,p)*(p+1)*(p+2)*(p+3) for p in range(1,5)]
  coeff=[]
  while vals:
   coeff.append(vals[0]);vals=[v-u for u,v in zip(vals,vals[1:])]
  # Polynomial degree<=3 because all denominators divide L, so forward
  # differences give exact nonnegative binomial basis on integer p>=1.
  root=rho(bits,d,l,0)
  if min(coeff)<0 or root<0:bad.append({'bits':bits,'d':d,'ell':l,'newton':list(map(str,coeff)),'p0':str(root)})
  for p in [5,9,50,1000]:
   from math import comb
   assert sum((v*comb(p-1,k) for k,v in enumerate(coeff)),F())==rho(bits,d,l,p)*(p+1)*(p+2)*(p+3)
  records.append({'bits':bits,'d':d,'ell':l,'newton':list(map(str,coeff)),'p0':str(root)})
print('bad',bad[:20],len(bad))
Path(__file__).with_suffix('.json').write_text(json.dumps({'lambda':list(map(str,lam)),'scope':'exact rational degree-three polynomial all memberships and every integer p>=0','bad':bad,'rows':records},indent=2))
