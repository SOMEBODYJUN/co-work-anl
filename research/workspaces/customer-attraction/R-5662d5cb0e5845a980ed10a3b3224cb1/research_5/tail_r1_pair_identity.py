"""Independent exact identity: r=1 alpha=gamma=1 tail projection = strong PAIR."""
from fractions import Fraction as F
from itertools import product

def share(n,d):return F(n,d) if n else F()
checked=0
for p,a,b,z in product(range(5),range(2),range(2),range(2)):
 D=(p+1)*(p+2);ell=p+a
 tail=share(b,p+z+b)+min(share(z-y,p+z+y)+F(y,ell+1) for y in range(2))
 pair=F(z+b,p+1)-F(z*b+a,D)
 assert tail==pair,(p,a,b,z,tail,pair)
 checked+=1
print({'states':checked,'identity':'tail r1 alpha=gamma=1 Q=actual B equals actual strong PAIR(forced Z,B)','exact':True})
