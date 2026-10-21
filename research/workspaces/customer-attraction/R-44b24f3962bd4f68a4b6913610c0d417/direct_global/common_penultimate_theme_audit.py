"""Independent exact algebra audit; finite audit is not the general proof."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import platform

def frac(x,p,q):
 return F(x,p+x+q) if x else F(0)

def audit_identity(m,a,b,p,T,R):
 d=sum(T);ell=sum(R);h=sum(x*y for x,y in zip(T,R));D=(p+1)*(p+2)
 alpha=frac(a,p,b);beta=frac(b,p,a)
 S=sum((alpha-frac(t,p,r) for t,r in zip(T,R)),F(0))
 Z=sum((beta-frac(r,p,a) for r in R),F(0))
 V=sum((frac(R[i],p,T[i])-frac(R[j],p,T[i]) for i in range(m) for j in range(m) if i!=j),F(0))
 assert S==m*alpha-F(d,p+1)+F(h,D)
 assert Z==m*beta-F(ell,p+a+1)
 assert V==F(d*ell-m*h,D)
 G=S+Z/F(2*m)+V/F(m)
 compact=m*alpha+beta/2-F(d,p+1)-F(ell,2*m*(p+a+1))+F(d*ell,m*D)
 assert G==compact
 rho=2*int(p+a+b>0)-int(d>0)-compact
 assert G+rho==2*int(p+a+b>0)-int(d>0)
 if not a or p==m-2:
  assert rho>=0,(m,a,b,p,T,R,rho)
 return rho

cases=0
for m in (3,4):
 for a,b,p in product(range(2),range(2),range(m-1)):
  for bits in product(range(2),repeat=2*m):
   audit_identity(m,a,b,p,bits[:m],bits[m:]);cases+=1

# Every feasible compressed (d,ell,h), including empty/repeated comparison labels.
compressed=0
for m in (3,4,5,6,7,11,31):
 for a,b,p in product(range(2),range(2),range(m-1)):
  if a and p!=m-2:continue
  for d,ell in product(range(m+1),repeat=2):
   # h cancels, but each boundary overlap is still reconstructed independently.
   hs={max(0,d+ell-m),min(d,ell)}
   for h in hs:
    T=[1]*d+[0]*(m-d)
    R=[1]*h+[0]*(d-h)+[1]*(ell-h)+[0]*(m-d-ell+h)
    assert len(R)==m and sum(R)==ell and sum(x*y for x,y in zip(T,R))==h
    # Direct V audit is quadratic, so use it only for manageable m.
    if m<=7:
     audit_identity(m,a,b,p,T,R)
    else:
     alpha=frac(a,p,b);beta=frac(b,p,a)
     rho=2*int(p+a+b>0)-int(d>0)-m*alpha-beta/2+F(d,p+1)+F(ell,2*m*(p+a+1))-F(d*ell,m*(p+1)*(p+2))
     assert rho>=0,(m,a,b,p,d,ell,h,rho)
    compressed+=1

# After multiplying each corner difference by L=2*m**2*(m-1)*(m-1+b),
# the result is a polynomial of degree <=4. Five distinct exact zero values
# certify its identity; this is polynomial identity verification, not sign sampling.
corner_checks=0
for b in (0,1):
 for corner in range(4):
  for m in range(3,8):
   d,ell=((1,0),(1,m),(m,0),(m,m))[corner]
   raw=F(1)-F(m,m-1+b)-F(b,2*m)+F(d,m-1)+F(ell*(m-1-2*d),2*m*m*(m-1))
   expected={0:[F(0),F(m-3,2*m*(m-1)),F(1),F(1)-F(m+1,2*m*(m-1))],1:[F(m+1,2*m*(m-1)),F(1,m),F(m,m-1)-F(1,2*m),F(1)]}[b][corner]
   assert (raw-expected)*(2*m*m*(m-1)*(m-1+b))==0
  corner_checks+=1
# Numerators/denominators of the eight target corners in t=m-3 have the
# following nonnegative coefficient lists (low to high). Denominators all
# have positive constant coefficient. These are exact shifts of the displayed
# rational formulas, independently compared above.
shifted=[([0],[1]),([0,1],[12,10,2]),([1],[1]),([8,9,2],[12,10,2]),([4,1],[12,10,2]),([1],[3,1]),([16,11,2],[12,10,2]),([1],[1])]
for numerator,denominator in shifted:
 assert all(c>=0 for c in numerator+denominator) and denominator[0]>0
report={'status':'all exact checks passed','full_binary_identity_cases':cases,'compressed_cases':compressed,'polynomial_corner_identities':corner_checks,'degree_bound':4,'exact_roots_per_identity':5,'scope':'Audit of formulas; general proof in common_penultimate_theme_half.md','python':platform.python_version()}
print(json.dumps(report,ensure_ascii=False,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
