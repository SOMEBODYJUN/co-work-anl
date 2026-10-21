"""Independent exact algebra audit; finite audit is not the general proof."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sympy as sp

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

m=sp.symbols('m',integer=True,positive=True)
d,l=sp.symbols('d l',real=True)
corner_checks=0
for b in (0,1):
 expr=1-m/(m-1+b)-sp.Rational(b,2)/m+d/(m-1)+l*(m-1-2*d)/(2*m*m*(m-1))
 expected={
  0:[0,(m-3)/(2*m*(m-1)),1,1-(m+1)/(2*m*(m-1))],
  1:[(m+1)/(2*m*(m-1)),1/m,m/(m-1)-1/(2*m),1]
 }[b]
 for (dv,lv),target in zip(((1,0),(1,m),(m,0),(m,m)),expected):
  assert sp.simplify(expr.subs({d:dv,l:lv})-target)==0
  # A polynomial with nonnegative coefficients in t=m-3 proves sign on m>=3.
  num,den=sp.fraction(sp.factor(target))
  t=sp.symbols('t',nonnegative=True)
  num_poly=sp.Poly(sp.expand(num.subs(m,t+3)),t)
  den_poly=sp.Poly(sp.expand(den.subs(m,t+3)),t)
  assert all(c>=0 for c in num_poly.all_coeffs())
  assert all(c>=0 for c in den_poly.all_coeffs()) and den_poly.eval(0)>0
  corner_checks+=1
report={'status':'all exact checks passed','full_binary_identity_cases':cases,'compressed_cases':compressed,'symbolic_corner_checks':corner_checks,'scope':'Audit of formulas; general proof in common_penultimate_theme_half.md','python_sympy':sp.__version__}
print(json.dumps(report,ensure_ascii=False,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
